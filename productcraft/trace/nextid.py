#!/usr/bin/env python3
"""Hand out the next ledger entry id for an engagement (rung 0's sibling; #297).

    python3 productcraft/trace/nextid.py productcraft/ledger/engagements/<eng-id>
    python3 productcraft/trace/nextid.py <eng-folder> --bare     # just the id, for a shell var

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


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    bare = "--bare" in argv[1:]
    if len(args) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    path = Path(args[0])
    if not path.is_dir():
        print(f"{path} is not a directory", file=sys.stderr)
        return 2
    eng = load_engagement(path)
    if not (eng.root / "brief.md").is_file() and not eng.records:
        print(f"{path} holds no brief.md and no pass records: not an engagement folder", file=sys.stderr)
        return 2
    ids = entry_ids(eng)
    sys.stdout.write(ids.next_id + "\n" if bare else ids.report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
