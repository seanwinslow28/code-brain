"""Test bootstrap: make `machine` (and through it the shared `tracekit`) importable."""
import sys
from pathlib import Path

TRACE_DIR = Path(__file__).resolve().parents[1]
if str(TRACE_DIR) not in sys.path:
    sys.path.insert(0, str(TRACE_DIR))

import machine  # noqa: E402,F401  — bootstraps productcraft/trace onto sys.path and registers line 8
