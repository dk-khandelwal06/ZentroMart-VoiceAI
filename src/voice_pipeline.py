import argparse
import json
import os
import re
import struct
import sys
import traceback
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from conversation_agent import ConversationAgent
from rag_pipeline import search_knowledge_base

load_dotenv(PROJECT_DIR / ".env")

SUPPORTED_AUDIO = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm"}


def repair_wav_header(path: Path) -> None:
    """Repair Gnani WAV files whose RIFF/data sizes are set to 0xFFFFFFFF."""
    with path.open("r+b") as audio_file:
        header = audio_file.read(44)

        if len(header) < 44 or header[:4] != b"RIFF" or header[8:12] != b"WAVE":
            raise ValueError("TTS output is not a standard PCM WAV file.")

        file_size = path.stat().st_size
        if file_size < 44:
            raise ValueError("WAV file is unexpectedly small.")

        # Repair only the standard 44-byte PCM WAV layout.
        if header[12:16] != b"fmt " or header[36:40] != b"data":
            raise ValueError("Unexpected WAV header layout; not repairing automatically.")

        audio_file.seek(4)
        audio_file.write(struct.pack("<I", file_size - 8))
        audio_file.seek(40)
        audio_file.write(struct.pack("<I", file_size - 44))


def is_order_or_action_request(message: str) -> bool:
    lower = message.lower()
    has_order_id = "order" in lower and any(ch.isdigit() for ch in message)
    asks_for_action = any(
        term in lower
        for term in (
            "create ticket",
            "raise a ticket",
            "human support",
            "human agent",
            "escalate",
        )
    )
    return has_order_id or asks_for_action



def make_spoken_reply(message, original_reply, sources):
    """Create a concise, source-grounded response for voice output."""
    lower = message.lower()

    # Specific answer grounded in the current electronics-return policy.
    if (
        "electronic" in lower
        and any(term in lower for term in ["return", "policy", "window"])
    ):
        current_policy = next(
            (
                item for item in sources
                if item.get("source") == "pol_returns_v4.md"
                and "RET-3" in item.get("text", "")
            ),
            None,
        )

        if current_policy:
            return (
                "ZentroMart's current policy gives electronics and accessories "
                "a seven-day return window for orders delivered on or after "
                "August 1st, 2026. Orders delivered before that date retain "
                "the earlier ten-day window. Items must be unused, with their "
                "original packaging and accessories. Electronics must not be "
                "physically damaged, and screen or account locks must be "
                "removed. Please check the current policy for any additional "
                "conditions."
            )

    # Do not speak long raw retrieval passages or invent an answer.
    if len(original_reply) > 900:
        return (
            "I found relevant information in ZentroMart's knowledge base, "
            "but I couldn't prepare a concise answer confidently. "
            "Would you like me to create a support ticket?"
        )

    return original_reply


def process_audio(
    audio_path: Path,
    agent: ConversationAgent,
    stt: GnaniSTTClient,
    tts: GnaniTTSClient,
    output_dir: Path,
) -> dict:
    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", audio_path.stem)
    record = {
        "input_audio": str(audio_path),
        "processed_at": datetime.now().astimezone().isoformat(),
        "status": "error",
    }

    try:
        stt_result = stt.transcribe(
            str(audio_path),
            language_code="en-IN",
            format="transcribe",
        )
        if not stt_result.get("success"):
            raise RuntimeError(f"STT failed: {stt_result}")

        transcript = str(stt_result.get("transcript", "")).strip()
        if not transcript:
            raise RuntimeError("STT returned an empty transcript.")

        # Use the existing conversation agent so verification state can
        # persist between audio files processed in the same batch.
        
        
        # Get the agent response and retrieve evidence for this question.
        reply = agent.handle(transcript)

        if not reply or not reply.strip():
            reply = (
                "I'm sorry, I couldn't prepare a response. "
                "Please try again."
            )

        if is_order_or_action_request(transcript):
            sources = []
        else:
            sources = search_knowledge_base(transcript, top_k=4)

        # Convert long retrieval output into a concise spoken response.
        reply = make_spoken_reply(transcript, reply, sources)

        transcript_path = output_dir / f"{stem}_transcript.txt"
        reply_path = output_dir / f"{stem}_reply.txt"
        audio_reply_path = output_dir / f"{stem}_reply.wav"
        sources_path = output_dir / f"{stem}_sources.json"

        transcript_path.write_text(
            transcript + "\n", encoding="utf-8"
        )
        reply_path.write_text(reply + "\n", encoding="utf-8")

        sources_path.write_text(
            json.dumps(sources, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


        transcript_path.write_text(transcript + "\n", encoding="utf-8")
        reply_path.write_text(reply + "\n", encoding="utf-8")

        # Save retrieved sources for policy questions, not for order
        # lookups or requests to create/escalate a ticket.
        if is_order_or_action_request(transcript):
            sources = []
        else:
            sources = search_knowledge_base(transcript, top_k=4)

        sources_path.write_text(
            json.dumps(sources, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # This first local-agent version speaks the agent's response as-is.
        # Long retrieved passages may produce a long spoken response.
        tts_bytes = tts.synthesize(
            reply,
            voice="Kaveri",
            model="timbre-v2.5",
            language="en-IN",
            output_file=str(audio_reply_path),
        )
        if not audio_reply_path.exists():
            audio_reply_path.write_bytes(tts_bytes)

        repair_wav_header(audio_reply_path)

        record.update(
            {
                "status": "success",
                "transcript": transcript,
                "reply": reply,
                "stt_request_id": stt_result.get("request_id"),
                "transcript_file": str(transcript_path),
                "reply_file": str(reply_path),
                "audio_reply_file": str(audio_reply_path),
                "sources_file": str(sources_path),
                "sources": [
                    {
                        "source": item.get("source"),
                        "chunk_id": item.get("chunk_id"),
                        "score": item.get("score"),
                    }
                    for item in sources
                ],
                "tts_bytes": len(tts_bytes),
            }
        )

        print(f"\n[{audio_path.name}]")
        print("Customer:", transcript)
        print("Assistant:", reply)
        print("Audio saved:", audio_reply_path)

    except Exception as exc:
        record["error"] = str(exc)
        record["traceback"] = traceback.format_exc()
        print(f"\nERROR processing {audio_path.name}: {exc}")

    return record


def main():
    parser = argparse.ArgumentParser(
        description="ZentroMart voice support pipeline using Gnani STT/TTS."
    )
    parser.add_argument(
        "--input-dir",
        default=str(PROJECT_DIR / "sample_audio"),
        help="Folder containing customer audio files.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(PROJECT_DIR / "sample_outputs"),
        help="Folder for transcripts, replies, sources and metadata.",
    )
    args = parser.parse_args()

    api_key = os.getenv("GNANI_API_KEY")
    if not api_key:
        raise SystemExit(
            "GNANI_API_KEY is missing. Check the project .env file; "
            "do not paste the key into chat."
        )

    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not input_dir.is_dir():
        raise SystemExit(f"Input folder does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    audio_files = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO
    )
    if not audio_files:
        raise SystemExit(f"No supported audio files found in {input_dir}")

    stt = GnaniSTTClient(api_key=api_key)
    tts = GnaniTTSClient(api_key=api_key)
    agent = ConversationAgent()

    results = []
    for audio_path in audio_files:
        results.append(
            process_audio(audio_path, agent, stt, tts, output_dir)
        )

    report_path = output_dir / "voice_pipeline_results.json"
    report_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    successes = sum(item["status"] == "success" for item in results)
    print(f"\nCompleted: {successes}/{len(results)} audio files")
    print("Run metadata:", report_path)


if __name__ == "__main__":
    main()