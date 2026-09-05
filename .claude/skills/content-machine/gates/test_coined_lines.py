#!/usr/bin/env python3
"""Fixture for the one-artifact rule (#162), written 2026-09-05 when the ledger
was first armed and the gate turned out not to fire.

Self-contained: no ledger on disk, no private brain. The specimen is a real line
from `raising-agents-ep-1/final.md`, which is a tracked public file.
"""
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from coined_lines import NEAR, find, load_ledger, norm  # noqa: E402

COINED = "I felt like a little kid opening a present on Christmas morning and unwrapped a big ol' turd."

# Overlap is a spectrum and the threshold is a judgment on it, so the fixture
# records the whole spread rather than a pass mark. The two ends are what the
# gate must get right; the middle is where the 80% line was drawn (#162).
CASES = [
    ("exact paste into a tweet",
     "I felt like a little kid opening a present on Christmas morning and unwrapped a big ol' turd.", True),
    ("light reword",
     "Felt like a little kid opening a present on Christmas morning and unwrapping a big ol' turd.", True),
    ("heavy reword",
     "It was like a kid opening a present on Christmas morning and unwrapping a big old turd.", False),
    ("same image, a new sentence",
     "Opening that report was Christmas morning with a turd in the box.", False),
    ("unrelated",
     "The synthesizer produced nothing for two weeks and nothing noticed.", False),
]

LEDGER = """# Coined lines

Prose about the convention. A fenced example must NOT arm the gate:

```
## some-artifact
> a line nobody ever wrote
```

## raising-agents-ep-1

> I felt like a little kid opening a present on Christmas morning and unwrapped a big ol' turd.

## Unregistered backlog

- raising-agents-ep-1 — a plain bullet is metadata, not a coined line
"""


def test_short_draft_still_scores():
    """The defect that made the gate useless on X.

    The window used to be exactly as long as the coined line, so a draft
    SHORTER than the line produced zero windows and scored 0.0 — reported as
    clean. Essay lines run ~18 tokens and a reactive post runs six, so the
    medium the rule was armed for was the one medium it could never fire in.
    """
    short = norm("Christmas morning and a big ol' turd.")
    assert len(short) < len(norm(COINED)), "specimen must be shorter than the coined line"
    _, overlap = find(short, COINED)
    assert overlap > 0.0, "a draft shorter than the coined line scored 0.0 — the X blind spot is back"
    print(f"  short draft ({len(short)} tokens vs {len(norm(COINED))}): scores {overlap:.0%}, not 0%")


def test_duplicates_do_not_deflate():
    """`a` appears three times in the specimen. The numerator is a set
    intersection, so counting duplicates in the denominator penalised a line
    for its own repetition."""
    ct = norm(COINED)
    assert len(ct) > len(set(ct)), "specimen must contain a repeated token to test this"
    # Every unique token, reordered so the exact-substring short circuit cannot
    # fire and the score has to come from the window arithmetic.
    shuffled = " ".join(sorted(set(ct)))
    exact, overlap = find(norm(shuffled), COINED)
    assert not exact, "the reordered draft must not match as an exact substring"
    assert overlap == 1.0, (
        f"a draft holding every unique token scored {overlap:.0%}; the denominator is "
        "counting duplicates again, which penalises a line for its own repetition")
    print(f"  duplicate tokens: {len(ct)} total, {len(set(ct))} unique — "
          f"all-unique draft scores {overlap:.0%}")


def test_spread():
    wrong = []
    print("  overlap spread:")
    for label, draft, should_fire in CASES:
        exact, overlap = find(norm(draft), COINED)
        fires = exact or overlap >= NEAR
        mark = "FIRES " if fires else "silent"
        print(f"    {overlap:5.0%}  {mark}  {label}")
        if fires != should_fire:
            wrong.append((label, overlap, should_fire))
    assert not wrong, f"threshold behaviour changed: {wrong}"
    # The honest gap, pinned so a future threshold change is a decision rather
    # than a drift: a human calls the heavy reword a reuse and the gate does not.
    _, heavy = find(norm(CASES[2][1]), COINED)
    assert 0.6 <= heavy < NEAR, f"heavy reword moved to {heavy:.0%}; re-read the threshold ruling (#162)"


def test_loader_ignores_fences_and_plain_bullets():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "coined-lines.md"
        p.write_text(LEDGER, encoding="utf-8")
        entries = load_ledger(p)
    assert len(entries) == 1, entries
    artifact, line = entries[0]
    assert artifact == "raising-agents-ep-1", artifact
    assert line == COINED, line
    print("  loader: 1 entry — the fenced example and the plain bullet both refused")


def main():
    print("coined-lines fixture")
    test_short_draft_still_scores()
    test_duplicates_do_not_deflate()
    test_spread()
    test_loader_ignores_fences_and_plain_bullets()
    print("\nOK")


if __name__ == "__main__":
    main()
