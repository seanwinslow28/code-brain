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
from origin_check import check, check_stimulus, looks_like_stimulus  # noqa: E402

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


# ------------------------------------------------------ inverted mode ----
#
# X's reactive route (#249, built #250). The block below is a real public post,
# verified through publish.x.com/oembed the same way #247's 79 specimens were.
# It is nobody's private material, so unlike the transcript above this half of
# the fixture runs on any machine.

STIMULUS = """STIMULUS BLOCK — fixture-cheese — 2026-09-05
Source: https://x.com/BobGolen/status/2087727910509556132
Author: @BobGolen
Post: Explosion at the cheese factory
\x20
\x20     Da brie is everywhere
Media: none
Surface: quote-post
"""

# Must flag. Each is the failure the inversion exists for.
STIMULUS_LEAKS = [
    # A run taken straight out of the post he is answering. The old gate would
    # have CLEARED this if the block were handed over as a transcript, because
    # every word is "traced".
    ("Explosion at the cheese factory, and my agents are everywhere.", "lifted"),
    # Lightly reworded lift: the connective tissue changed, the run did not.
    ("An explosion at my cheese factory would at least be legible.", "lifted"),
    # A claim about his own week, in a form that asserts nothing anyone can check.
    ("I shipped 23 agents in August and not one of them laughed.", "claims"),
]

# Must NOT flag. Sharing the subject is the whole point of replying.
STIMULUS_CLEAN = [
    "The cheese in my fridge is its own small factory of regret.",
    "I have never once trusted a man who explains his own pun.",
    # Naming the person being answered is the form, not a claim about his week.
    "BobGolen has ruined dairy for me personally.",
]

# The mini-transcript route: the same claim, asked and answered, traces.
MINI_TRANSCRIPT = """TRANSCRIPT — x-cheese-ask — 2026-09-05
Lens: none (ASK LIST answer)

Q1: How many agents did you ship in August?
A1: Twenty-three. 23 of them, in August, and not one laughed.
"""


def flagged(phrase, transcript):
    return bool(check(phrase, transcript))


def stimulus_kinds(phrase, transcript=None):
    findings, _ = check_stimulus(phrase, STIMULUS, transcript)
    kinds = set()
    for f in findings:
        if f["lifted"]:
            kinds.add("lifted")
        if f["claims"]:
            kinds.add("claims")
    return kinds


def run_inverted():
    print("\n--- inverted mode (X reactive route) ---")

    # 1. The polarity case, stated as what is actually true rather than as the
    #    scarier version. Handed the block TODAY, check() keeps nothing from it:
    #    author_only() only keeps text inside an answer region, and a block has
    #    no A-lines, so the draft comes back all-untraced — useless noise, not a
    #    laundered pass. The laundering is one obvious convenience edit away
    #    ("a file with no Q/A markers is all his"), and the assertion below is
    #    what proves the danger is real: index the post text as an answer, and
    #    a run lifted straight out of it comes back CLEAN.
    assert looks_like_stimulus(STIMULUS), "the sentinel is how the refusal is detected"
    lift = STIMULUS_LEAKS[0][0]
    laundered = ("TRANSCRIPT — laundered — 2026-09-05\n\n"
                 "A1: Explosion at the cheese factory. Da brie is everywhere.\n")
    still_flagged = {u["token"].lower()
                     for f in check(lift, laundered) for u in f["untraced"]}
    assert not ({"explosion", "cheese", "factory"} & still_flagged), (
        "premise of the whole inversion changed: indexing the post text no longer "
        f"clears the words lifted out of it (still flagged: {still_flagged})")
    assert check(lift, STIMULUS), (
        "a block handed over as a transcript must not come back clean by any route")
    print("  polarity : indexing the post text WOULD clear a lifted line — refusal is load-bearing")

    caught, missed = [], []
    for phrase, kind in STIMULUS_LEAKS:
        (caught if kind in stimulus_kinds(phrase) else missed).append((phrase, kind))
    false_pos = [p for p in STIMULUS_CLEAN if stimulus_kinds(p)]

    print(f"  leaks caught                    : {len(caught)}/{len(STIMULUS_LEAKS)}")
    print(f"  false positives on shared ground: {len(false_pos)}/{len(STIMULUS_CLEAN)}")
    for phrase, kind in missed:
        print(f"    MISSED [{kind}] {phrase}")
    for p in false_pos:
        print(f"    FALSE POSITIVE {p}")

    traced = stimulus_kinds(STIMULUS_LEAKS[2][0], MINI_TRANSCRIPT)
    print(f"  claim with a mini-transcript    : {'clears' if not traced else 'STILL FLAGGED'}")

    assert not missed, f"inverted recall regressed: {missed}"
    assert not false_pos, f"false positives on shared ground: {false_pos}"
    assert not traced, "an ASK LIST answer must clear its claim, or the ASK LIST buys nothing"


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

    run_inverted()
    print("\nOK")


if __name__ == "__main__":
    main()
