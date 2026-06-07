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


def _tokenize_lower(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


def _ngrams(tokens: list[str], n: int) -> Iterable[tuple[str, ...]]:
    return (tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1))


def extract_distinctive_ngrams(
    target_corpus: str,
    baseline_corpora: list[str],
    top_n: int = 30,
    ns: tuple[int, ...] = (2, 3, 4),
) -> list[tuple[str, ...]]:
    """Extract n-grams over-represented in target vs. baseline.

    Distinctiveness = log( (target_freq + smoothing) / (baseline_freq + smoothing) ).
    Returns top_n n-grams sorted by distinctiveness, descending.
    """
    target_tokens = _tokenize_lower(target_corpus)
    if not target_tokens:
        return []

    target_counts: Counter[tuple[str, ...]] = Counter()
    for n in ns:
        target_counts.update(_ngrams(target_tokens, n))

    baseline_counts: Counter[tuple[str, ...]] = Counter()
    baseline_total = 0
    for corpus in baseline_corpora:
        tokens = _tokenize_lower(corpus)
        baseline_total += len(tokens)
        for n in ns:
            baseline_counts.update(_ngrams(tokens, n))

    target_total = len(target_tokens)
    smoothing = 1e-6

    scored = []
    for ngram, t_count in target_counts.items():
        if t_count < 2:  # require ≥2 in target to filter noise
            continue
        t_freq = t_count / target_total
        b_freq = (baseline_counts.get(ngram, 0) + smoothing) / (baseline_total + smoothing)
        score = t_freq / b_freq
        scored.append((score, ngram))

    scored.sort(reverse=True)
    return [ng for _, ng in scored[:top_n]]


def compute_distance(
    target_features: dict[str, float],
    baseline: dict,
    target_text: str,
) -> float:
    """Compute total absolute z-score distance + n-gram-mismatch penalty.

    Lower = closer to Sean's distribution. Pass threshold is calibrated externally
    against a hand-labeled set (15 real Sean / 15 generic AI) at pre-flight time.
    """
    stdevs = baseline.get("_stdevs", {})
    feature_keys = (
        "sentence_length_mean",
        "sentence_length_stdev",
        "comma_density_per_100w",
        "em_dash_density_per_100w",
        "first_person_freq_per_100w",
    )

    z_total = 0.0
    for key in feature_keys:
        std = stdevs.get(key, 1.0) or 1.0
        z = abs(target_features.get(key, 0.0) - baseline.get(key, 0.0)) / std
        z_total += z

    # N-gram component: count target n-grams from baseline._ngrams that appear in target_text.
    baseline_ngrams: list[tuple[str, ...]] = baseline.get("_ngrams", [])
    if baseline_ngrams:
        target_lower = target_text.lower()
        hits = sum(
            1 for ng in baseline_ngrams if " ".join(ng) in target_lower
        )
        # Penalty rises as match rate falls. 0 hits → +5.0, all hits → +0.
        match_rate = hits / max(len(baseline_ngrams), 1)
        z_total += 5.0 * (1.0 - match_rate)

    return z_total


_META_STOPWORDS = (
    "voice-samples", "calibration", "skill.md", "skill md", "corpus",
    "verbatim", "anchor", "signature move", "why it works", "why it's better",
    "ai wrote", "sean rewrote",
)


def extract_voice_corpus_chunks(
    text: str,
    min_words: int = 60,
    window: int = 100,
) -> list[str]:
    """Isolate ONLY Sean's actual quoted voice from voice-samples.md.

    voice-samples.md interleaves real samples (Markdown blockquotes, `> ...`) with
    heavy analytical commentary (`**Signature moves:** ...`, `**Why it works:** ...`,
    round notes). The naive "any 60-200 word paragraph" extractor swept that
    commentary into the stylometric fingerprint, contaminating it with the
    document's own vocabulary (`skill md`, `pop culture anchoring`) and skewing the
    features toward expository prose. This pulls blockquoted prose only, drops
    italic editor notes and meta lines, and chunks into ~`window`-word samples so
    cross-chunk stdevs are computable. Precision over recall: the inline
    "Sean rewrote:" passages (not blockquoted) are intentionally skipped to keep
    the corpus clean.
    """
    quote_lines: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith(">"):
            continue
        s = s.lstrip(">").strip()
        if not s or s.startswith(("_", "**")):  # blank, italic note, or bold meta
            continue
        low = s.lower()
        if any(stop in low for stop in _META_STOPWORDS):
            continue
        quote_lines.append(s)

    words = " ".join(quote_lines).split()
    chunks: list[str] = []
    for i in range(0, len(words), window):
        w = words[i : i + window]
        if len(w) >= min_words:
            chunks.append(" ".join(w))
    return chunks


def load_baseline(path: Path | str) -> dict:
    """Load stylometry baseline JSON. Raises FileNotFoundError if missing."""
    with open(path, "r") as f:
        return json.load(f)


def save_baseline(baseline: dict, path: Path | str) -> None:
    with open(path, "w") as f:
        json.dump(baseline, f, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else x)
