#!/usr/bin/env python3
"""Rung-0 checker — the first Close-checklist trace line (#272 decision 8, built on #290).

    python3 productcraft/trace/check.py productcraft/ledger/engagements/<eng-id>

Prints one line per deterministic check, PASS or FAIL with its count, then
the findings under a failing check and the notes under any check. Exit 0
when every check passes, 1 when any fails, 2 when the path is not an
engagement folder. No model, no network, stdlib only. Reads the private
ledger at run time and writes nothing.

Options: --json for a machine-readable list; --repo <path> to resolve
studio-prefixed input paths (productcraft/…, systemcraft/…, .claude/…)
against a repo root other than the one found by walking up.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracekit.checker import format_report, run_checks  # noqa: E402
from tracekit.engagement import load_engagement  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("engagement", help="the engagement folder (or its trace/ subfolder)")
    ap.add_argument("--json", action="store_true", help="emit the checks as JSON instead of the report")
    ap.add_argument("--repo", help="repo root for studio-prefixed input paths")
    a = ap.parse_args(argv)
    path = Path(a.engagement)
    if not path.is_dir():
        print(f"no engagement folder at {path}", file=sys.stderr)
        return 2
    eng = load_engagement(path, repo=Path(a.repo) if a.repo else None)
    if not eng.records and not any(e.startswith("pass-") for e in eng.errors):
        print(f"no engagement records under {eng.trace_dir} (expected trace/pass-NN-<seat>-<kind>.md)", file=sys.stderr)
        return 2
    checks = run_checks(eng)
    if a.json:
        print(json.dumps([
            {"name": c.name, "ok": c.ok, "n_ok": c.n_ok, "n_total": c.n_total, "findings": c.findings,
             "notes": c.notes, "n_unverifiable": c.n_unverifiable}
            for c in checks
        ], indent=2, ensure_ascii=False))
    else:
        print(format_report(checks), end="")
    return 0 if all(c.ok for c in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
