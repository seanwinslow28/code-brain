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
                            [--stimulus <block.md>]

--artifact names the piece being drafted, so a line already recorded against
THIS artifact is not a violation. Without it, every ledger hit is reported.

--stimulus adds X's second input (#250): the verbatim text of the post being
answered, checked at the same 80% threshold. Two jobs, one threshold — the
one-artifact rule looks backwards at what he has already spent, and the
stimulus check looks sideways at the person he is replying to. Shared
vocabulary passes either way; a lifted run does not.

Exit codes mirror origin_check.py: Expressive advises and returns 0,
Professional returns 1 on any hit.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from origin_check import stimulus_post_text  # noqa: E402  -- one home for the block parser

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
    entries, artifact, fenced = [], "(unattributed)", False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        # A fenced block is documentation about the convention, not the ledger.
        # Without this, the file's own worked example arms the gate with a line
        # nobody ever wrote — which is the #232 failure inverted: a check that
        # looks armed and is firing on a specimen.
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("## "):
            artifact = line[3:].strip()
        elif line.startswith(">"):
            coined = line.lstrip("> ").strip()
            if coined:
                entries.append((artifact, coined))
    return entries


def find(draft_tokens: list[str], coined: str) -> tuple[bool, float]:
    """(exact, best_overlap) for one coined line against the draft.

    Two defects fixed 2026-09-05, both found the moment the ledger was first
    armed (#251), and both of which had made the reworded case unreachable:

    **The window has to shrink to fit the draft.** It used to be exactly as
    long as the coined line, so a draft SHORTER than the line produced zero
    windows and scored 0.0 — silently, as "clean". That is not an edge case,
    it is X: essay lines run 18 tokens and a reactive post runs six, so the
    medium the one-artifact rule was armed for was the one medium where a
    reworded reuse could never fire. The denominator stays the coined line's
    length, so a short draft is not flattered by being short.

    **The denominator counted duplicates.** `n` was `len(ct)` while the
    numerator is a set intersection, so every repeated word in a coined line
    ("a" three times here) deflated its own score. Unique tokens both sides.
    """
    ct = norm(coined)
    if len(ct) < MIN_TOKENS:
        return (False, 0.0)
    joined = " ".join(draft_tokens)
    if " ".join(ct) in joined:
        return (True, 1.0)
    cs = set(ct)
    n = len(cs)
    span = min(len(ct), len(draft_tokens))
    best = 0.0
    for i in range(max(len(draft_tokens) - span + 1, 0)):
        window = set(draft_tokens[i:i + span])
        best = max(best, len(cs & window) / n)
    return (False, best)


def stimulus_lines(block_text: str) -> list[str]:
    """The post being answered, cut into checkable units.

    Sentence-sized, because `find()` windows the draft at the length of the
    unit it is given: hand it a whole multi-sentence post and the window is
    wider than any reply, so a genuine lift of one line scores as noise.
    """
    post = stimulus_post_text(block_text)
    out = []
    for block in post.split("\n"):
        for s in re.split(r"(?<=[.!?])\s+", block):
            s = s.strip()
            if s:
                out.append(s)
    if post and post not in out:
        out.append(post)          # the whole post too, for the flat exact-paste case
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--lane", choices=["expressive", "professional"], default="expressive")
    ap.add_argument("--artifact", default=None,
                    help="slug of the piece being drafted; its own lines are not violations")
    ap.add_argument("--ledger", default=str(LEDGER))
    ap.add_argument("--stimulus", default=None,
                    help="X stimulus block; its post text is checked as a second input (#250)")
    args = ap.parse_args()

    ledger_path = Path(args.ledger)
    entries = load_ledger(ledger_path)
    draft_tokens = norm(Path(args.draft).read_text(encoding="utf-8"))

    # An empty ledger used to return here, before the stimulus check existed and
    # before anyone noticed the ledger had never been created. Both halves of
    # that were the same bug: a gate that reports "nothing to check against" and
    # exits looks identical, in a GATE RECORD, to a gate that ran clean.
    if not entries:
        state = "holds no registered lines" if ledger_path.exists() else "does not exist"
        print(f"coined-lines: ledger {state} ({ledger_path}).")
        print("  UNARMED — the one-artifact rule cannot fire until lines are registered.")

    hits = []
    for artifact, coined in entries:
        if args.artifact and artifact == args.artifact:
            continue
        exact, overlap = find(draft_tokens, coined)
        if exact or overlap >= NEAR:
            hits.append((artifact, coined, "exact" if exact else f"{overlap:.0%} overlap"))

    stim_hits = []
    if args.stimulus:
        block_text = Path(args.stimulus).read_text(encoding="utf-8")
        try:
            units = stimulus_lines(block_text)
        except ValueError as exc:
            print(f"coined-lines: {exc}", file=sys.stderr)
            return 2
        whole = units[-1] if units and "\n" in units[-1] else None
        for line in units:
            exact, overlap = find(draft_tokens, line)
            if exact or overlap >= NEAR:
                stim_hits.append((line, "exact" if exact else f"{overlap:.0%} overlap"))
        # The whole-post unit exists for the flat exact-paste case. If a single
        # line already fired, reporting the post again is the same finding twice.
        if whole and len(stim_hits) > 1:
            stim_hits = [h for h in stim_hits if h[0] != whole]

    if not hits and not stim_hits:
        if entries:
            print(f"coined-lines: clean against {len(entries)} recorded lines"
                  + (" and the stimulus post." if args.stimulus else "."))
        elif args.stimulus:
            print("coined-lines: clean against the stimulus post.")
        return 0

    if hits:
        print(f"coined-lines: {len(hits)} line(s) already spent elsewhere.\n")
        for artifact, coined, how in hits:
            print(f"  [{how}] \"{coined}\"")
            print(f"          spent in: {artifact}\n")
        print("A coined line lives in exactly one artifact. Write a new line, or cut the beat.")

    if stim_hits:
        if hits:
            print()
        print(f"coined-lines: {len(stim_hits)} run(s) lifted from the post being answered.\n")
        for line, how in stim_hits:
            print(f"  [{how}] \"{line}\"")
        print()
        print("That is someone else's sentence. Borrow the structure, never the strings —")
        print("the words are not invented, which is exactly why the origin gate cannot see it.")

    if args.lane == "professional":
        return 1
    print("(Expressive lane: advisory. Sean rules.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
