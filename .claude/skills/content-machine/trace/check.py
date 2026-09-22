#!/usr/bin/env python3
"""Rung-0 checker for a content-machine run — the first line of the run's close ritual (#291).

    python3 .claude/skills/content-machine/trace/check.py creative-studio/content-machine/pieces/<run>

Prints one line per deterministic check, PASS or FAIL with its count, the
findings under a failing check and the notes under any check. Exit 0 when every
check passes, 1 when any fails, 2 when the path is not a run folder. No model,
no network, stdlib only; imports the shared kit from productcraft/trace/. Reads
the private run folder at run time and writes nothing.

Options: --json for a machine-readable list; --repo <path> to resolve
repo-prefixed input paths (creative-studio/…, .claude/…, vault/…) against a
repo root other than the one this file sits in.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from machine import CONTENT_MACHINE, REPO  # noqa: E402
from tracekit.checker import format_report, run_checks  # noqa: E402
from tracekit.engagement import load_engagement  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("run", help="the run folder under pieces/ (or its trace/ subfolder)")
    ap.add_argument("--json", action="store_true", help="emit the checks as JSON instead of the report")
    ap.add_argument("--repo", help="repo root for repo-prefixed input paths")
    a = ap.parse_args(argv)
    path = Path(a.run)
    if not path.is_dir():
        print(f"no run folder at {path}", file=sys.stderr)
        return 2
    eng = load_engagement(path, repo=Path(a.repo) if a.repo else REPO, studio=CONTENT_MACHINE)
    if not eng.records and not any(e.startswith("pass-") for e in eng.errors):
        print(f"no run records under {eng.trace_dir} (expected trace/pass-NN-<seat>-<kind>.md)", file=sys.stderr)
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
