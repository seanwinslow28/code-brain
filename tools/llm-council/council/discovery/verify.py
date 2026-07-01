# council/discovery/verify.py
"""Stage 3 — fabrication gate. A pain point survives only if a quote it cites
actually appears at a URL present in the evidence bundle."""

import logging
import re
from dataclasses import dataclass

from council.discovery.evidence import EvidenceBundle
from council.discovery.fusion import CandidatePainPoint


@dataclass
class VerifiedPainPoint:
    point: CandidatePainPoint
    verified: bool
    supporting_urls: list[str]


_ENTAIL_TAU = 0.5
_CLAIM_SENT = re.compile(r"[^.!?]+[.!?]|[^.!?]+$")
_logger = logging.getLogger("council.discovery.verify")
_degraded_warned = False


def _claim_sentences(text: str) -> list[str]:
    parts = [s.strip() for s in _CLAIM_SENT.findall(text)]
    parts = [p for p in parts if p]
    return parts or ([text.strip()] if text.strip() else [])


def _warn_degraded_once() -> None:
    global _degraded_warned
    if not _degraded_warned:
        _degraded_warned = True
        _logger.warning("NLI scorer unavailable — VERIFY gate running in substring-only (degraded) mode.")


def _claim_supported(claim: str, fetched_text: str, doc_lower: str, scorer) -> bool:
    needle = claim.strip().lower()
    if not needle:
        return True                       # empty fragment never vetoes the AND
    if needle in doc_lower:               # substring pre-filter: fast ACCEPT, never rejects
        return True
    if scorer is None:
        _warn_degraded_once()
        return False                      # degraded: substring-only, exactly as today
    return scorer.entails(premise=fetched_text, hypothesis=claim) >= _ENTAIL_TAU


def quote_supported_at_url(*, cited_quote: str, fetched_text: str, scorer=None) -> bool:
    """Substring pre-filter -> atomic-claim NLI-entailment cascade (E1). Shared by VERIFY + BACKFILL.
    Substring is a fast, high-precision ACCEPT that NEVER rejects; every substring-miss falls through
    to NLI. With scorer=None the gate is substring-only (today's behavior)."""
    doc_lower = fetched_text.strip().lower()
    if not doc_lower:
        return False
    sentences = _claim_sentences(cited_quote)
    if not sentences:
        return False
    return all(_claim_supported(s, fetched_text, doc_lower, scorer) for s in sentences)


def _quote_present_at_url(bundle: EvidenceBundle, url: str, quotes: list[str], scorer=None) -> bool:
    for rec in bundle.records:
        if rec.url != url:
            continue
        for q in quotes:
            if quote_supported_at_url(cited_quote=q, fetched_text=rec.quote, scorer=scorer):
                return True
    return False


def verify_pain_points(points: list[CandidatePainPoint], bundle: EvidenceBundle, scorer=None) -> list[VerifiedPainPoint]:
    out: list[VerifiedPainPoint] = []
    for pt in points:
        supporting = [
            u for u in pt.urls
            if bundle.has_url(u) and _quote_present_at_url(bundle, u, pt.quotes, scorer=scorer)
        ]
        out.append(VerifiedPainPoint(point=pt, verified=bool(supporting), supporting_urls=supporting))
    return out
