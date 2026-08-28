#!/usr/bin/env python3
"""The one-artifact rule for coined lines (#162), as a $0 stdlib check.

A coined line lives in exactly one artifact and is never recycled across
mediums. Re-using the good line is the single most tempting thing the machine
can do, because it already worked once, and it is exactly what makes a body of
work read as a bag of catchphrases rather than a run of pieces.

The ledger is git-ignored and local (the repo is public and these are Sean's
best lines):

    creative-studio/content-machine/coined-lines.md

Its shape reuses the corpus rule so there is one convention to remember:

    ## raising-agents-ep-1          <- the artifact the line belongs to
    > everything ran clean          <- a coined line, verbatim
    > not whether it ran. what it made.

Every `>` line is a coined line. Everything else is metadata.

Usage:
    python3 coined_lines.py <draft.md> [--lane expressive|professional]
                            [--artifact <slug>] [--ledger <path>]

--artifact names the piece being drafted, so a line already recorded against
THIS artifact is not a violation. Without it, every ledger hit is reported.

Exit codes mirror origin_check.py: Expressive advises and returns 0,
Professional returns 1 on any hit.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
LEDGER = REPO / "creative-studio" / "content-machine" / "coined-lines.md"

# A recycled line is usually lightly reworded, not pasted, so an exact match is
# not enough on its own. Below this token-overlap ratio a shared phrase is just
# shared vocabulary.
NEAR = 0.8
MIN_TOKENS = 4


def norm(text: str) -> list[str]:
    text = text.lower().replace("’", "'")
    return re.findall(r"[a-z0-9']+", text)


def load_ledger(path: Path) -> list[tuple[str, str]]:
    """(artifact, line) pairs. Missing ledger is not an error: the first piece
    through the machine legitimately has nothing to collide with."""
    if not path.exists():
        return []
    entries, artifact = [], "(unattributed)"
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            artifact = line[3:].strip()
        elif line.startswith(">"):
            coined = line.lstrip("> ").strip()
            if coined:
                entries.append((artifact, coined))
    return entries


def find(draft_tokens: list[str], coined: str) -> tuple[bool, float]:
    """(exact, best_overlap) for one coined line against the draft."""
    ct = norm(coined)
    if len(ct) < MIN_TOKENS:
        return (False, 0.0)
    n = len(ct)
    joined = " ".join(draft_tokens)
    if " ".join(ct) in joined:
        return (True, 1.0)
    cs = set(ct)
    best = 0.0
    for i in range(max(len(draft_tokens) - n + 1, 0)):
        window = set(draft_tokens[i:i + n])
        best = max(best, len(cs & window) / n)
    return (False, best)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--lane", choices=["expressive", "professional"], default="expressive")
    ap.add_argument("--artifact", default=None,
                    help="slug of the piece being drafted; its own lines are not violations")
    ap.add_argument("--ledger", default=str(LEDGER))
    args = ap.parse_args()

    ledger_path = Path(args.ledger)
    entries = load_ledger(ledger_path)
    if not entries:
        print(f"coined-lines: ledger empty or absent ({ledger_path}). Nothing to check against.")
        return 0

    draft_tokens = norm(Path(args.draft).read_text(encoding="utf-8"))
    hits = []
    for artifact, coined in entries:
        if args.artifact and artifact == args.artifact:
            continue
        exact, overlap = find(draft_tokens, coined)
        if exact or overlap >= NEAR:
            hits.append((artifact, coined, "exact" if exact else f"{overlap:.0%} overlap"))

    if not hits:
        print(f"coined-lines: clean against {len(entries)} recorded lines.")
        return 0

    print(f"coined-lines: {len(hits)} line(s) already spent elsewhere.\n")
    for artifact, coined, how in hits:
        print(f"  [{how}] \"{coined}\"")
        print(f"          spent in: {artifact}\n")
    print("A coined line lives in exactly one artifact. Write a new line, or cut the beat.")
    if args.lane == "professional":
        return 1
    print("(Expressive lane: advisory. Sean rules.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
