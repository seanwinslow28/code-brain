#!/usr/bin/env python3
"""Registry numbers — the runtime × seat table for `craftwork/templates/runtime-registry.md` § Numbers (#286).

    python3 craftwork/trace/registry.py productcraft/ledger/engagements/pc-eng-001-* [more engagement folders]
    python3 craftwork/trace/registry.py <eng-folder>... --json
    python3 craftwork/trace/registry.py <eng-folder>... --studio <profile.py>

Prints two markdown tables — one row per runtime, then one per runtime × seat —
holding labeled passes as counts, the rung-0 clean count, median runtime-reported
tokens and wall-clock over measured passes, meter availability, trials and
promotions. Never a percentage. Stdlib only, read-only: it runs the rung-0
checks in memory to find which passes a finding names, reads the private ledger
at run time, and writes nothing — the coordinator pastes the output into the
registry at Close. Exit 0; 2 when a path is not an engagement folder.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracekit.engagement import load_engagement       # noqa: E402
from tracekit.registry import numbers_for, render_markdown  # noqa: E402
from tracekit.studio import StudioNotFound, load_profile  # noqa: E402


def _studio_arg(argv: list[str]):
    """`--studio <file>` or `--studio=<file>`: the profile to load instead of the one found by walking up."""
    for i, a in enumerate(argv):
        if a == "--studio" and i + 1 < len(argv):
            return load_profile(argv[i + 1]), argv[:i] + argv[i + 2:]
        if a.startswith("--studio="):
            return load_profile(a.split("=", 1)[1]), argv[:i] + argv[i + 1:]
    return None, argv


def main(argv: list[str]) -> int:
    try:
        studio, argv = _studio_arg(argv)
    except StudioNotFound as e:
        print(e, file=sys.stderr)
        return 2
    as_json = "--json" in argv[1:]
    paths = [Path(a) for a in argv[1:] if not a.startswith("--")]
    if not paths:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    engagements = []
    for p in paths:
        if not p.is_dir():
            print(f"not an engagement folder: {p}", file=sys.stderr)
            return 2
        try:
            eng = load_engagement(p, studio=studio)
        except StudioNotFound as e:
            print(e, file=sys.stderr)
            return 2
        if not eng.records and not (p / "trace").is_dir() and not (p / "brief.md").is_file():
            print(f"not an engagement folder: {p}", file=sys.stderr)
            return 2
        engagements.append(eng)
    per_runtime, per_pair = numbers_for(engagements)
    if as_json:
        print(json.dumps({"runtimes": [c.as_dict() for c in per_runtime],
                          "cells": [c.as_dict() for c in per_pair]}, indent=2))
    else:
        sys.stdout.write(render_markdown(per_runtime, per_pair))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
