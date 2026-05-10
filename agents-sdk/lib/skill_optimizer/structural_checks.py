"""Deterministic structural checks for skill_optimizer eval suite.

Each check returns (passed: bool, reason: str). Cheap, deterministic, free.
"""
from __future__ import annotations

import re
from typing import Tuple

# Sensory nouns watched by the anti-pattern over-reference check.
# These are the words Sean's voice tends to over-use when not pruned.
SENSORY_OVERREFERENCE_NOUNS = (
    "coffee",
    "bathroom",
    "ferry",
    "cursor",
    "terminal",
    "screen",
    "mug",
    "keyboard",
)


def _split_paragraphs(text: str) -> list[str]:
    """Split on blank-line paragraph breaks. Strips each paragraph."""
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def substack_format_intro(text: str) -> Tuple[bool, str]:
    """Verify Substack-intro shape: first paragraph length, paragraph breaks, closer length."""
    paragraphs = _split_paragraphs(text)
    if len(paragraphs) < 2:
        return False, "must contain at least one paragraph break (got 0)"

    first_wc = _word_count(paragraphs[0])
    if first_wc < 60:
        return False, f"first paragraph too short: {first_wc} words (need 60-180)"
    if first_wc > 180:
        return False, f"first paragraph too long: {first_wc} words (need 60-180)"

    closer = paragraphs[-1]
    # Take the final sentence of the final paragraph as the closer.
    sentences = re.split(r"(?<=[.!?])\s+", closer)
    closer_sentence = sentences[-1].strip() if sentences else closer
    closer_wc = _word_count(closer_sentence)
    if closer_wc > 12:
        return False, f"closer too long: {closer_wc} words (Sean closer pattern is ≤12)"

    return True, "ok"


def anti_pattern_overreference(text: str) -> Tuple[bool, str]:
    """Fail if any watched sensory noun appears more than 2 times (case-insensitive).

    Two instances are allowed because a callback closer (returning to an opening
    image, transformed) is a documented Sean signature move. Three or more is
    the anti-pattern Sean called "Bad Sean" — falling in love with your own material.
    """
    lower = text.lower()
    for noun in SENSORY_OVERREFERENCE_NOUNS:
        # Word-boundary count to avoid false matches inside other words.
        count = len(re.findall(rf"\b{re.escape(noun)}\b", lower))
        if count > 2:
            return False, f"{noun!r} appears {count} times (max 2)"
    return True, "ok"
