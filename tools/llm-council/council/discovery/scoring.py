# council/discovery/scoring.py
"""PM4 — research-grounded opportunity score. composite = 100 * value * confidence.

value      = weighted(importance, reach, recency)   — "how big / how fresh"
confidence = independent-source corroboration + model consensus (discount multiplier)

RICE-style: confidence MULTIPLIES the value so a thin-evidence pain is discounted, not
propped up by high importance. Reach is log-damped (Reddit "hot" precedent) so one viral
post can't dominate. Constants are TUNABLE and flagged for sensitivity-testing — they
materially change rankings (composite-indicator theory); the card shows the full breakdown.
See vault/20_projects/research/2026-06-29-opportunity-scoring-frameworks-research.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from math import log1p
from urllib.parse import urlparse
import re

from council.discovery.evidence import EvidenceBundle
from council.discovery.fusion import CandidatePainPoint
from council.discovery.velocity import VelocitySignal

# --- tunable constants (sensitivity-test before trusting absolute values) ---
VALUE_WEIGHTS = {"importance": 0.45, "reach": 0.40, "recency": 0.15}   # sum 1.0
REACH_CEIL = 500          # engagement log-saturation point
BREADTH_CEIL = 8          # authors + domains saturation
HALFLIFE_DAYS = 30        # exponential recency decay half-life
RECENCY_FLOOR = 0.3       # anti over-correction — old durable pain isn't crushed
RECENCY_NEUTRAL = 0.5     # unparseable date
DOMAIN_CEIL = 4           # independent domains for full source credit
SOURCE_CEIL = 5           # distinct sources for full source credit
CONF_FLOOR = 0.5          # a single-source pain is halved, never zeroed
CONF_SRC_WT = 0.7         # independent sources dominate confidence
CONF_CONSENSUS_WT = 0.3   # model agreement is a lighter, separate signal
VELOCITY_WEIGHT = 0.0     # E4: velocity term OFF by default — ship moves no card's rank until raised
VELOCITY_NEUTRAL = 0.5    # normalized velocity of a flat / absent trend (no nudge)


@dataclass(frozen=True)
class ScoreBreakdown:
    composite: float            # 0-100 headline = 100 * value * confidence
    value: float                # 0-1
    confidence: float           # CONF_FLOOR-1.0
    importance: float           # 0-1
    reach: float                # 0-1
    recency: float              # 0-1
    source_corroboration: float # 0-1  independent evidence breadth
    consensus_ratio: float      # 0-1  model-panel agreement
    intensity: int
    engagement_sum: int
    distinct_sources: int
    distinct_domains: int
    evidence_date: str          # parsed date used, or ""
    velocity: float = VELOCITY_NEUTRAL   # 0-1 normalized; 0.5 = flat / no signal
    velocity_raw: float = 0.0            # raw slope (regression-visibility); 0.0 when no signal
    velocity_source: str = ""            # "pytrends" when a real signal is attached, else ""
    velocity_term: str = ""              # the term measured, else ""


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _parse_loose_date(s: str) -> date | None:
    s = (s or "").strip()
    for fmt, n in (("%Y-%m-%d", 10), ("%Y-%m", 7), ("%Y", 4)):
        try:
            return datetime.strptime(s[:n], fmt).date()
        except ValueError:
            continue
    return None


def _parse_consensus(s: str) -> float:
    """'4/4 models' -> 1.0, '3/4' -> 0.75, garbage -> 0.0."""
    m = re.search(r"(\d+)\s*/\s*(\d+)", s or "")
    if not m:
        return 0.0
    num, den = int(m.group(1)), int(m.group(2))
    return _clamp(num / den) if den > 0 else 0.0


def score_opportunity(
    point: CandidatePainPoint,
    supporting_urls: list[str],
    bundle: EvidenceBundle,
    *,
    today: date | None = None,
    value_weights: dict[str, float] | None = None,
    velocity: VelocitySignal | None = None,
    velocity_weight: float | None = None,
) -> ScoreBreakdown:
    today = today or date.today()
    value_weights = value_weights or VALUE_WEIGHTS
    supp = set(supporting_urls)
    recs = [r for r in bundle.records if r.url in supp]

    # importance ← intensity (floored at 1)
    intensity = max(int(point.intensity or 0), 1)
    importance = _clamp(intensity / 5)

    # reach ← log-damped engagement + breadth (sources + domains)
    eng_sum = sum(int(r.engagement or 0) for r in recs)
    distinct_sources = len({r.source_name for r in recs if r.source_name})
    # domains come from the gate-truth supporting_urls; engagement/sources from matched records (intentional asymmetry).
    distinct_domains = len({urlparse(u).netloc.lower() for u in supporting_urls if u})
    breadth = distinct_sources + distinct_domains
    reach = _clamp(0.7 * (log1p(eng_sum) / log1p(REACH_CEIL))
                   + 0.3 * min(breadth / BREADTH_CEIL, 1.0))

    # recency ← exp decay on parsed evidence date (floored)
    d = _parse_loose_date(point.recency)
    if d is None:
        rec_dates = [pd for pd in (_parse_loose_date(r.date) for r in recs) if pd]
        d = max(rec_dates) if rec_dates else None
    if d is None:
        recency, evidence_date = RECENCY_NEUTRAL, ""
    else:
        age = max((today - d).days, 0)
        recency = max(0.5 ** (age / HALFLIFE_DAYS), RECENCY_FLOOR)
        evidence_date = d.isoformat()

    value_base = _clamp(value_weights["importance"] * importance
                        + value_weights["reach"] * reach
                        + value_weights["recency"] * recency)

    # E4 — bounded velocity nudge. centered=0 when flat/absent, so the default weight 0 (and any
    # flat signal) leaves value_base untouched. None-check (NOT `or`): explicit 0.0 forces it off.
    weight = VELOCITY_WEIGHT if velocity_weight is None else velocity_weight
    vel_norm = velocity.normalized if velocity is not None else VELOCITY_NEUTRAL
    centered = (vel_norm - 0.5) * 2.0
    value = _clamp(value_base * (1.0 + weight * centered))

    # confidence ← independent sources (dominant) + model consensus (light)
    source_corroboration = _clamp(0.7 * min(distinct_domains / DOMAIN_CEIL, 1.0)
                                  + 0.3 * min(distinct_sources / SOURCE_CEIL, 1.0))
    consensus_ratio = _parse_consensus(point.consensus)
    confidence = _clamp(
        CONF_FLOOR + (1 - CONF_FLOOR) * (CONF_SRC_WT * source_corroboration
                                         + CONF_CONSENSUS_WT * consensus_ratio),
        CONF_FLOOR, 1.0)

    composite = round(100 * value * confidence, 1)
    return ScoreBreakdown(
        composite=composite, value=round(value, 4), confidence=round(confidence, 4),
        importance=round(importance, 4), reach=round(reach, 4), recency=round(recency, 4),
        source_corroboration=round(source_corroboration, 4),
        consensus_ratio=round(consensus_ratio, 4),
        intensity=intensity, engagement_sum=eng_sum, distinct_sources=distinct_sources,
        distinct_domains=distinct_domains, evidence_date=evidence_date,
        velocity=round(vel_norm, 4),
        velocity_raw=round(velocity.slope, 4) if velocity is not None else 0.0,
        velocity_source=velocity.source if velocity is not None else "",
        velocity_term=velocity.term if velocity is not None else "",
    )
