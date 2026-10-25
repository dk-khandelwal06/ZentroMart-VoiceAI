
import sys
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
PIPELINE = PROJECT_DIR / "src" / "voice_pipeline.py"

if __name__ == "__main__":
    command = [sys.executable, str(PIPELINE), *sys.argv[1:]]
    raise SystemExit(subprocess.call(command, cwd=PROJECT_DIR))
