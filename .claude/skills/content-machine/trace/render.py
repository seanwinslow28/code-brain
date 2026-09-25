#!/usr/bin/env python3
"""Viewer renderer for a content-machine run — the second line of the run's close ritual (#291).

    python3 .claude/skills/content-machine/trace/render.py creative-studio/content-machine/pieces/<run>

Renders one self-contained HTML into the run's trace/ folder (`trace/eval.html`,
or --out <path>): the reading line, the last-good × first-failing transition
matrix on the machine's stages 0–6, the rung-0 list, the train, one folded row
per stage invocation with its inputs, moves, meter and critique, and in-page
labeling that leaves through *Copy label rows*. Runs the rung-0 checks first so
the page shows them; a failing check never blocks the render, because the page
is how Sean sees what failed. Local file only, never a hosted artifact: the run
folder is git-ignored and the page carries his drafts. Stdlib only.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from machine import CONTENT_MACHINE, REPO  # noqa: E402
from tracekit.checker import run_checks  # noqa: E402
from tracekit.engagement import load_engagement  # noqa: E402
from tracekit.labels import decided  # noqa: E402
from tracekit.viewer import render_html  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("run", help="the run folder under pieces/ (or its trace/ subfolder)")
    ap.add_argument("--out", help="write the HTML here instead of <run>/trace/eval.html")
    ap.add_argument("--repo", help="repo root for repo-prefixed input paths")
    a = ap.parse_args(argv)
    path = Path(a.run)
    if not path.is_dir():
        print(f"no run folder at {path}", file=sys.stderr)
        return 2
    eng = load_engagement(path, repo=Path(a.repo) if a.repo else REPO, studio=CONTENT_MACHINE)
    checks = run_checks(eng)
    target = Path(a.out) if a.out else eng.trace_dir / "eval.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_html(eng, checks=checks), encoding="utf-8")
    failing = sum(1 for c in checks if not c.ok)
    labeled = sum(1 for l in eng.labels.values() if decided(l.verdict))
    status = "rung 0 clean" if not failing else f"{failing} of {len(checks)} checks failing (see check.py)"
    print(f"wrote {target} ({target.stat().st_size // 1024} KB) · {len(eng.records)} passes, {labeled} labeled · {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
