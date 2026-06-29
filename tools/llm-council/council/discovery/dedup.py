"""E3 — near-duplicate pain-point dedup (threshold merge-to-canonical) + MMR gap ranking.

A shared lexical similarity (token Jaccard, $0/deterministic) drives two algorithms:
  * dedup_verified — collapse near-duplicate gate-survived pain points. Conservative
                     (bias-to-UNDER-merge) and bounded merge-to-canonical: each non-canonical
                     attaches to at most one canonical, so there is NO transitive closure
                     (A=B,B=C =/=> A=C) — the documented over-merge trap.
  * rank_gaps      — MMR (Carbonell & Goldstein 1998) diversity selection over D4's whitespace
                     gaps: "worst-first" = most-distinct-from-what-the-run-surfaced, near-dups dropped.

Both take an injectable similarity_fn so a future nomic-embed-text path swaps in without touching
either algorithm. Honest merge: union URLs/quotes; corroboration stays keyed on distinct DOMAINS in
scoring.py so syndicated/same-domain sources can't double-count.

Spec: docs/superpowers/specs/2026-06-29-discovery-e3-mmr-dedup-design.md
Research: vault/20_projects/research/2026-06-29-mmr-dedup-similarity-research.md
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

from council.discovery.fusion import CandidatePainPoint
from council.discovery.verify import VerifiedPainPoint

# --- tunable constants (conservative; research gave no short-text number — calibrated vs fixtures) ---
SIM_THRESHOLD = 0.5     # token-Jaccard >= this => "same pain"; biased toward UNDER-merging
MMR_LAMBDA = 0.3        # diversity-dominant gap ranking (research: 0.3-0.5 band for a diversity goal)

_STOPWORDS = frozenset(
    "a an and are as at be but by for from has have in into is it its of on or that the their "
    "this to was were will with your you our we they them then than i me my so if not no can "
    "cant do does dont how what when where which who why".split()
)
_WORD = re.compile(r"[a-z0-9]+")

SimilarityFn = Callable[[str, str], float]


def normalize_tokens(text: str) -> frozenset[str]:
    """Lowercase, extract alphanumeric word tokens, drop stopwords. Deterministic, no deps."""
    return frozenset(t for t in _WORD.findall((text or "").lower()) if t not in _STOPWORDS)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    union = a | b
    if not union:
        return 0.0                       # two empty texts => non-duplicate (under-merge bias)
    return len(a & b) / len(union)


def pain_similarity(a: str, b: str) -> float:
    """Default similarity_fn: token-Jaccard over the normalized tokens of two short texts."""
    return jaccard(normalize_tokens(a), normalize_tokens(b))


def _point_text(point: CandidatePainPoint) -> str:
    return f"{point.title}. {point.summary}"
