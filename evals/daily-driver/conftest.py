"""Make agents-sdk importable from the eval runner regardless of pytest's CWD.

Same pattern as evals/vault-synthesizer/conftest.py — see that file for the
full rationale. Pytest auto-registers hooks from conftest.py but NOT from a
parametrized test module like runner.py, which is why the last-run.md
writer lives here.
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_AGENTS_SDK = _REPO_ROOT / "agents-sdk"
if _AGENTS_SDK.exists() and str(_AGENTS_SDK) not in sys.path:
    sys.path.insert(0, str(_AGENTS_SDK))


_RESULTS: list[tuple[str, str, str]] = []


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    case_id = report.nodeid.split("[", 1)[-1].rstrip("]")
    if report.passed:
        _RESULTS.append((case_id, "PASS", ""))
    elif report.skipped:
        notes = str(report.longrepr).splitlines()[-1] if report.longrepr else ""
        _RESULTS.append((case_id, "SKIPPED", notes))
    else:
        notes = str(report.longrepr).splitlines()[-1] if report.longrepr else ""
        _RESULTS.append((case_id, "FAIL", notes))


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
    lines.append(f"**Pass rate: {pass_count}/{total} ({100*pass_count//total}%).**")
    _write_last_run(lines)
