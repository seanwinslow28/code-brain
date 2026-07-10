# council/discovery/frame.py
"""Stage 4 (pm lens) — verified pain points → ranked PRD-grade opportunity cards + quote bank."""

import re
from dataclasses import dataclass
from datetime import date

from council.discovery.bet import ProposedBet, propose_bet
from council.discovery.evidence import EvidenceBundle
from council.discovery.fusion import FusionResult
from council.discovery.scoring import ScoreBreakdown, score_opportunity
from council.discovery.verify import VerifiedPainPoint

_WINDOW_LABEL = "90d"   # display label for the velocity window (PytrendsProvider default)
_MAX_TERM_WORDS = 5


@dataclass
class IdeaCard:
    title: str
    who: str
    pain: str               # the summary line (secondary to the quote)
    lead_quote: str         # pain in their words — the verbatim quote
    evidence_urls: list[str]
    quotes: list[str]
    score: ScoreBreakdown
    why_now: str
    bet: ProposedBet


def _velocity_term(pt, topic: str) -> str:
    """Short Trends query from the pain title; fall back to the run topic when empty."""
    cleaned = re.sub(r"[^\w\s]", " ", (pt.title or "").lower()).strip()
    cleaned = " ".join(cleaned.split()[:_MAX_TERM_WORDS])
    return cleaned or (topic or "").strip().lower()


def _dedup_terms(terms: list[str]) -> list[str]:
    seen, out = set(), []
    for t in terms:
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _why_now(score: ScoreBreakdown) -> str:
    freshness = _freshness_note(score)
    if not score.velocity_source:
        return freshness                                   # no velocity signal -> recency note only
    slope = score.velocity_raw
    if slope > 0.05:
        lead = f"Demand accelerating — interest slope +{slope:.2f} over {_WINDOW_LABEL} ({score.velocity_source})."
    elif slope < -0.05:
        lead = f"Demand cooling — interest slope {slope:.2f} over {_WINDOW_LABEL} ({score.velocity_source})."
    else:
        lead = f"Demand flat — interest steady over {_WINDOW_LABEL} ({score.velocity_source})."
    return f"{lead} {freshness}"


def _freshness_note(score: ScoreBreakdown) -> str:
    if not score.evidence_date:
        return "Recency unknown — verify the pain is current."
    if score.recency >= 0.5:
        return f"Fresh signal — evidence dated {score.evidence_date}."
    return f"Older signal (evidence {score.evidence_date}); confirm it's still live."


def frame_pm(verified: list[VerifiedPainPoint], fusion_result: FusionResult,
             bundle: EvidenceBundle, *, today: date | None = None, topic: str = "",
             velocity_provider=None, velocity_weight=None) -> tuple[list[IdeaCard], list[str]]:
    today = today or date.today()
    # E4 — one batched demand-slope lookup for all verified cards (blind to the gate; score-only).
    signals: dict = {}
    if velocity_provider is not None:
        terms = _dedup_terms([_velocity_term(v.point, topic) for v in verified if v.verified])
        if terms:
            signals = velocity_provider.measure_batch(terms)
    cards: list[IdeaCard] = []
    quote_bank: list[str] = []
    seen_q: set[str] = set()
    for v in verified:
        if not v.verified:
            continue
        pt = v.point
        signal = signals.get(_velocity_term(pt, topic))
        score = score_opportunity(pt, v.supporting_urls, bundle, today=today,
                                  velocity=signal, velocity_weight=velocity_weight)
        cards.append(IdeaCard(
            title=pt.title,
            who=pt.segment or "users",
            pain=f"{pt.title}: {pt.summary}",
            lead_quote=pt.quotes[0] if pt.quotes else "",
            evidence_urls=v.supporting_urls,
            quotes=pt.quotes,
            score=score,
            why_now=_why_now(score),
            bet=propose_bet(pt),
        ))
        for q, u in zip(pt.quotes, v.supporting_urls + [""] * len(pt.quotes)):
            line = f'"{q}" — {u}'.rstrip(" —")
            if line not in seen_q:
                seen_q.add(line)
                quote_bank.append(line)
    cards.sort(key=lambda c: c.score.composite, reverse=True)
    return cards, quote_bank
