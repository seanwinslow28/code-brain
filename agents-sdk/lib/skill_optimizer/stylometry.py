"""Stylometric feature extraction + n-gram extraction + distance computation.

Used as a deterministic anti-Goodhart anchor in the eval suite. Detects whether
the optimizer is producing prose with Sean's actual statistical fingerprint
(sentence rhythm, punctuation density, n-gram match) vs. surface-imitation prose.
"""
from __future__ import annotations

import json
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Iterable

# Em dash unicode + ASCII-double-dash are both treated as em dashes.
EM_DASH_PATTERNS = (r"—", r"--")

FIRST_PERSON_TOKENS = {"i", "me", "my", "mine", "myself"}


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def extract_features(text: str) -> dict[str, float]:
    """Compute the five stylometric features used by the eval suite."""
    words = _word_count(text)
    if words == 0:
        return {
            "sentence_length_mean": 0.0,
            "sentence_length_stdev": 0.0,
            "comma_density_per_100w": 0.0,
            "em_dash_density_per_100w": 0.0,
            "first_person_freq_per_100w": 0.0,
        }

    sentences = _split_sentences(text)
    sentence_lengths = [_word_count(s) for s in sentences if _word_count(s) > 0]
    mean_len = statistics.mean(sentence_lengths) if sentence_lengths else 0.0
    stdev_len = (
        statistics.stdev(sentence_lengths)
        if len(sentence_lengths) >= 2
        else 0.0
    )

    comma_count = text.count(",")
    em_dash_count = sum(len(re.findall(p, text)) for p in EM_DASH_PATTERNS)

    lower_words = re.findall(r"\b\w+\b", text.lower())
    fp_count = sum(1 for w in lower_words if w in FIRST_PERSON_TOKENS)

    return {
        "sentence_length_mean": float(mean_len),
        "sentence_length_stdev": float(stdev_len),
        "comma_density_per_100w": comma_count / words * 100.0,
        "em_dash_density_per_100w": em_dash_count / words * 100.0,
        "first_person_freq_per_100w": fp_count / words * 100.0,
    }
