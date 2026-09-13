#!/usr/bin/env python3
"""Viewer renderer — the second Close-checklist trace line (#272 decision 8, built on #290).

    python3 productcraft/trace/render.py productcraft/ledger/engagements/<eng-id>

Renders one self-contained HTML into the engagement's trace/ folder
(`trace/eval.html`, or --out <path>), to productcraft/trace/DESIGN.md. Runs
the rung-0 checks first so the page shows them; a failing check never blocks
the render, because the page is how Sean sees what failed. Local file only,
never a hosted artifact. Stdlib only; writes nothing else.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracekit.checker import run_checks  # noqa: E402
from tracekit.engagement import load_engagement  # noqa: E402
from tracekit.viewer import render_html  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("engagement", help="the engagement folder (or its trace/ subfolder)")
    ap.add_argument("--out", help="write the HTML here instead of <engagement>/trace/eval.html")
    ap.add_argument("--repo", help="repo root for studio-prefixed input paths")
    a = ap.parse_args(argv)
    path = Path(a.engagement)
    if not path.is_dir():
        print(f"no engagement folder at {path}", file=sys.stderr)
        return 2
    eng = load_engagement(path, repo=Path(a.repo) if a.repo else None)
    checks = run_checks(eng)
    target = Path(a.out) if a.out else eng.trace_dir / "eval.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_html(eng, checks=checks), encoding="utf-8")
    failing = sum(1 for c in checks if not c.ok)
    labeled = sum(1 for l in eng.labels.values() if l.verdict)
    status = "rung 0 clean" if not failing else f"{failing} of {len(checks)} checks failing (see check.py)"
    print(f"wrote {target} ({target.stat().st_size // 1024} KB) · {len(eng.records)} passes, {labeled} labeled · {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
