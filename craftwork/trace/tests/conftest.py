"""Test bootstrap: make `tracekit` importable from craftwork/trace/, and name the reference studio."""
import sys
from pathlib import Path

TRACE_DIR = Path(__file__).resolve().parents[1]
if str(TRACE_DIR) not in sys.path:
    sys.path.insert(0, str(TRACE_DIR))

import reference  # noqa: E402,F401  — loads Productcraft's profile and sets $TRACEKIT_STUDIO
