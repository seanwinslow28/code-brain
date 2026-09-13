"""Test bootstrap: make `tracekit` importable from productcraft/trace/."""
import sys
from pathlib import Path

TRACE_DIR = Path(__file__).resolve().parents[1]
if str(TRACE_DIR) not in sys.path:
    sys.path.insert(0, str(TRACE_DIR))
