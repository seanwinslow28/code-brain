#!/usr/bin/env python3
"""Hand out the next ledger entry id for an engagement (rung 0's sibling; #297).

    python3 craftwork/trace/nextid.py productcraft/ledger/engagements/<eng-id>
    python3 craftwork/trace/nextid.py <eng-folder> --bare     # just the id, for a shell var
    python3 craftwork/trace/nextid.py <eng-folder> --studio <profile.py>

Stdlib only, read-only: it touches nothing, reads the private ledger at run
time, and prints. Exit 0 always when the path is an engagement, 2 when it is
not — an id is information, never a gate.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracekit.engagement import load_engagement          # noqa: E402
from tracekit.ledger import entry_ids                    # noqa: E402
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
    args = [a for a in argv[1:] if not a.startswith("--")]
    bare = "--bare" in argv[1:]
    if len(args) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    path = Path(args[0])
    if not path.is_dir():
        print(f"{path} is not a directory", file=sys.stderr)
        return 2
    try:
        eng = load_engagement(path, studio=studio)
    except StudioNotFound as e:
        print(e, file=sys.stderr)
        return 2
    if not (eng.root / "brief.md").is_file() and not eng.records:
        print(f"{path} holds no brief.md and no pass records: not an engagement folder", file=sys.stderr)
        return 2
    ids = entry_ids(eng)
    sys.stdout.write(ids.next_id + "\n" if bare else ids.report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
