from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
commands = [
    [sys.executable, str(ROOT / "Part-1A" / ".harness" / "run_harness.py")],
    [sys.executable, str(ROOT / "Part-1B" / ".harness" / "run_evaluation.py")],
]
for command in commands:
    result = subprocess.run(command, cwd=ROOT, check=False)
    if result.returncode:
        raise SystemExit(result.returncode)
