"""One local verification entry point. Does not contact external services."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for command in [
    ["tools/validate.py"],
    ["-m", "unittest", "discover", "-s", "tests", "-v"],
    ["-m", "agent_sdp.verify_trace", "examples/traces/local-exchange.json"],
]:
    subprocess.run([sys.executable, *command], cwd=ROOT, check=True)
print("PASS: documentation, legacy fixtures, reference runtime and signed proof bundle")
