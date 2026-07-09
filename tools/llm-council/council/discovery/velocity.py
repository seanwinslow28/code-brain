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
    """OLS slope over 0..n-1, divided by the series mean (scale-independent), clamped to [-1, 1].
    Assumes a non-negative-mean series (true for pytrends' 0-100 index); a negative mean would
    invert the sign relationship."""
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


def _dedup_preserve(terms: list[str]) -> list[str]:
    seen, out = set(), []
    for t in terms:
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _chunks(items: list[str], n: int) -> "list[list[str]]":
    return [items[i:i + n] for i in range(0, len(items), n)]


def _pytrends_fetch(terms: list[str], window_days: int) -> "dict[str, list[float]]":
    """The ONLY pytrends/pandas touch point. Returns {term: interest_over_time series}.
    Isolated behind this function so all tests inject a pure-list fake and never hit the network."""
    from pytrends.request import TrendReq  # lazy: import cost + optional dep only when used
    req = TrendReq(hl="en-US", tz=0)
    req.build_payload(terms, timeframe=f"today {max(1, window_days // 30)}-m")
    df = req.interest_over_time()
    out: dict[str, list[float]] = {}
    for t in terms:
        if t in getattr(df, "columns", []):
            out[t] = [float(v) for v in df[t].tolist()]
    return out


def _pytrends_available() -> bool:
    try:
        import pytrends  # noqa: F401
        return True
    except Exception:
        return False


class PytrendsProvider:
    """Google-Trends demand slope. measure_batch dedupes, caches per-term, chunks by 5, and maps
    any failure or thin (<2 point) series to None. Never raises."""

    def __init__(self, fetch=None, window_days: int = 90):
        self._fetch = fetch or _pytrends_fetch
        self._window_days = window_days
        self._cache: dict[str, VelocitySignal | None] = {}

    def measure_batch(self, terms: list[str]) -> "dict[str, VelocitySignal | None]":
        out: dict[str, VelocitySignal | None] = {}
        todo: list[str] = []
        for t in _dedup_preserve(terms):
            if t in self._cache:
                out[t] = self._cache[t]
            else:
                todo.append(t)
        for group in _chunks(todo, 5):
            try:
                series_map = self._fetch(group, self._window_days)
            except Exception as e:  # rate-limit / network / parse — degrade this group to None
                _logger.warning("velocity fetch failed for %s (%s) — those cards degrade.", group, e)
                series_map = {}
            for t in group:
                vals = series_map.get(t) or []
                if len(vals) < 2:
                    sig = None
                else:
                    slope = _series_slope(vals)
                    sig = VelocitySignal(term=t, slope=round(slope, 4),
                                         normalized=round(_normalize(slope), 4),
                                         source="pytrends", window_days=self._window_days,
                                         points=len(vals))
                self._cache[t] = sig
                out[t] = sig
        return out


def get_velocity_provider() -> "VelocityProvider | None":
    """Lazy resolver. None (no signal) unless DISCOVERY_VELOCITY=pytrends and pytrends importable.
    Mirrors nli.get_scorer(): opt-in, degrades to None, never crashes a run."""
    if os.environ.get("DISCOVERY_VELOCITY", "").strip().lower() != "pytrends":
        return None
    if not _pytrends_available():
        _logger.warning("DISCOVERY_VELOCITY=pytrends but pytrends is not installed — velocity off.")
        return None
    return PytrendsProvider()
