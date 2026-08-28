#!/usr/bin/env python3
"""Regression fixture for the origin gate, built from the walking skeleton (#163).

Every phrase below is real. The INVENTIONS are what the hand-check cut from the
chain draft; the SOURCED lines are what survived because Sean actually said them.
The point of the fixture is not a passing score, it is a permanent, honest record
of what the mechanical layer can and cannot see.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from origin_check import check  # noqa: E402

TRANSCRIPT = os.path.join(
    HERE, "../../../../creative-studio/content-machine/transcripts/2026-08-25-raising-agents-ep1.md"
)

# Cut from the chain draft by hand. The shaper wrote these; Sean never said them.
INVENTIONS = [
    "Concepts. Connections. Real files with real names.",
    "All it could do was hand my own material back to me with the edges sanded off.",
    "It couldn't bring anything new to the table because it had no table to get anything from.",
    "Cool. Thanks.",
    "That's the part that stung.",
    "Here's where it gets better.",
    "Now, I wasn't flying blind here.",
    "come back with the research, the ideas, the notes",
    "to do the actual thinking",
    "Nothing about this is finished.",
    # Contamination class: "report" entered the room in the interviewer's Q11/Q12
    # and the draft adopted it. A word the interviewer supplied is not his word.
    "And I'd been reading a report every morning.",
]

# Sean's own material. A flag on any of these is a false positive.
SOURCED = [
    "I felt like a little kid opening a present on Christmas morning and finding a big ol' turd in the box.",
    "So every night the Mini dialed into an empty pit, got an error back.",
    "The research covers agentic frameworks.",
    "No concepts. No connections. Nada.",
    "It only checked if the process exited, not if it produced anything.",
    # His A1 opened with a literal "Q1:" of his own. A naive parser reads that as the
    # interviewer talking and drops "clean" from his vocabulary, turning his own line
    # into a false leak.
    "Each of those mornings it told me everything ran clean.",
]


def flagged(phrase, transcript):
    return bool(check(phrase, transcript))


def main():
    transcript = open(TRANSCRIPT, encoding="utf-8").read()
    caught = [p for p in INVENTIONS if flagged(p, transcript)]
    missed = [p for p in INVENTIONS if not flagged(p, transcript)]
    false_pos = [p for p in SOURCED if flagged(p, transcript)]

    print(f"recall on real inventions       : {len(caught)}/{len(INVENTIONS)}")
    print(f"false positives on his own words: {len(false_pos)}/{len(SOURCED)}")
    if missed:
        print("\nBlind to (each is built only from words he did say, recombined):")
        for p in missed:
            print(f"  - {p}")
    if false_pos:
        print("\nFalse positives:")
        for p in false_pos:
            print(f"  - {p}")

    # The gate reports; the bar is honesty about its reach, not a high score.
    assert len(caught) >= 7, f"recall regressed: {len(caught)}/{len(INVENTIONS)}"
    assert not false_pos, f"false positives on sourced material: {false_pos}"
    print("\nOK")


if __name__ == "__main__":
    main()
