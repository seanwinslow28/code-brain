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


# --- last-run.md autogeneration hooks ---
# Pytest auto-registers these from conftest.py (it does NOT auto-register hooks
# from a parametrized test module like runner.py). Moving them here makes
# last-run.md write on every run.

_RESULTS: list[tuple[str, str, str]] = []


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    case_id = report.nodeid.split("[", 1)[-1].rstrip("]")
    if report.passed:
        _RESULTS.append((case_id, "✅ PASS", ""))
    elif report.skipped:
        notes = str(report.longrepr).splitlines()[-1] if report.longrepr else ""
        _RESULTS.append((case_id, "⏸️ SKIPPED", notes))
    else:
        notes = str(report.longrepr).splitlines()[-1] if report.longrepr else ""
        _RESULTS.append((case_id, "❌ FAIL", notes))


def pytest_sessionfinish(session, exitstatus):
    if not _RESULTS:
        return
    from runner import _load_cases, _write_last_run
    cases_by_id = {c["id"]: c for c in _load_cases()}
    lines = []
    for case_id, status, notes in _RESULTS:
        cat = cases_by_id.get(case_id, {}).get("category", "?")
        lines.append(f"| {case_id} | {cat} | {status} | {notes} |")
    pass_count = sum(1 for _, s, _ in _RESULTS if "PASS" in s)
    total = len(_RESULTS)
    lines.append("")
    lines.append(f"**Baseline pass rate: {pass_count}/{total} ({100*pass_count//total}%) — by design.**")
    _write_last_run(lines)
