"""E4 — velocity scoring channel. Produces a demand SLOPE (a number), fed ONLY into scoring —
never the verify gate, never the EvidenceBundle. Optional: get_velocity_provider() returns None
(no signal) unless DISCOVERY_VELOCITY=pytrends AND pytrends is importable, mirroring nli.get_scorer().
This module imports nothing from verify.py — that exclusion is the load-bearing moat invariant."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Protocol

_logger = logging.getLogger("council.discovery.velocity")

VELOCITY_NORM_NEUTRAL = 0.5   # normalized value of a flat / absent trend


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


@dataclass(frozen=True)
class VelocitySignal:
    term: str
    slope: float        # raw OLS slope / mean, clamped to [-1, 1] (regression-visibility field)
    normalized: float   # 0-1 for scoring; 0.5 = flat
    source: str         # "pytrends"
    window_days: int
    points: int


class VelocityProvider(Protocol):
    def measure_batch(self, terms: list[str]) -> "dict[str, VelocitySignal | None]": ...


def _series_slope(values: list[float]) -> float:
    """OLS slope over 0..n-1, divided by the series mean (scale-independent), clamped to [-1, 1]."""
    n = len(values)
    if n < 2:
        return 0.0
    mean_x = (n - 1) / 2.0
    mean_y = sum(values) / n
    num = sum((i - mean_x) * (v - mean_y) for i, v in enumerate(values))
    den = sum((i - mean_x) ** 2 for i in range(n))
    if den == 0:
        return 0.0
    slope = num / den
    return _clamp(slope / (mean_y or 1.0), -1.0, 1.0)


def _normalize(slope: float) -> float:
    return _clamp(0.5 + slope / 2.0, 0.0, 1.0)
