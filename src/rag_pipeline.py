import os
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = Path(r"E:\Capstone_Project_Dataset_FTTT_2026")
KB_DIR = DATASET_DIR / "kb"
INDEX_DIR = PROJECT_DIR / "outputs" / "rag_index"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 180
CHUNK_OVERLAP = 35


def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping word-based chunks."""
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks



def load_documents():
    """Load Markdown knowledge-base documents and preserve filenames."""
    if not KB_DIR.exists():
        raise FileNotFoundError(f"Knowledge base folder not found: {KB_DIR}")

    documents = []

    for file_path in sorted(KB_DIR.rglob("*.md")):
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        # Exclude superseded policy versions.
        if file_path.stem.endswith("_superseded"):
            continue

        relative_path = str(file_path.relative_to(KB_DIR))
        chunks = split_into_chunks(text)

        for chunk_number, chunk_text in enumerate(chunks, start=1):
            documents.append({
                "source": relative_path,
                "chunk_id": chunk_number,
                "text": chunk_text,
            })

    if not documents:
        raise ValueError(f"No Markdown documents found in {KB_DIR}")

    return documents


def build_index():
    """Create and save the FAISS vector index and chunk metadata."""
    print("Loading knowledge-base documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} text chunks.")

    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    texts = [doc["text"] for doc in documents]

    print("Generating embeddings. First run may download the model...")
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(INDEX_DIR / "knowledge_base.faiss"))

    metadata_path = INDEX_DIR / "chunks.json"
    metadata_path.write_text(
        json.dumps(documents, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nRAG index created successfully!")
    print(f"Documents/chunks: {len(documents)}")
    print(f"FAISS index: {INDEX_DIR / 'knowledge_base.faiss'}")
    print(f"Chunk metadata: {metadata_path}")


def search_knowledge_base(query, top_k=4):
    """Retrieve the most relevant chunks for a customer question."""
    if not query.strip():
        return []

    index_path = INDEX_DIR / "knowledge_base.faiss"
    metadata_path = INDEX_DIR / "chunks.json"

    if not index_path.exists() or not metadata_path.exists():
        raise FileNotFoundError(
            "RAG index not found. Run this file first to build the index."
        )

    model = SentenceTransformer(MODEL_NAME)
    index = faiss.read_index(str(index_path))
    documents = json.loads(metadata_path.read_text(encoding="utf-8"))

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    scores, indices = index.search(
        query_embedding,
        min(top_k, len(documents)),
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        result = documents[int(idx)].copy()
        result["score"] = float(score)
        results.append(result)

    return results


if __name__ == "__main__":
    build_index()

    print("\nTesting retrieval...")
    test_query = "What is the return policy?"
    results = search_knowledge_base(test_query)

    print(f"\nQuery: {test_query}")
    for number, result in enumerate(results, start=1):
        print(f"\n--- Result {number} | Score: {result['score']:.3f} ---")
        print(f"Source: {result['source']}")
        print(result["text"][:700])
