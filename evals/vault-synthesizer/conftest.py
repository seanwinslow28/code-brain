"""Make agents-sdk importable from the eval runner regardless of pytest's CWD.

The agents-sdk/ directory contains top-level packages `agents/` and `lib/`
(no `agents_sdk` wrapper package). Without this, pytest's collection adds
evals/vault-synthesizer/ to sys.path first and the runner's
`from agents import vault_synthesizer` then fails to resolve.

This conftest inserts agents-sdk/ at the front of sys.path so that
`from agents import vault_synthesizer` and `from lib import ...` work
regardless of the invocation CWD.
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_AGENTS_SDK = _REPO_ROOT / "agents-sdk"
if _AGENTS_SDK.exists() and str(_AGENTS_SDK) not in sys.path:
    sys.path.insert(0, str(_AGENTS_SDK))
