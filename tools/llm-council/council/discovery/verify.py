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


@dataclass
class CitationMetrics:
    precision: float | None
    recall: float | None


def _premise_for(bundle: EvidenceBundle, urls) -> str:
    return " ".join(r.quote for r in bundle.records if r.url in set(urls))


def _all_claims_supported(quotes, premise: str, scorer) -> bool:
    return all(quote_supported_at_url(cited_quote=q, fetched_text=premise, scorer=scorer) for q in quotes)


def citation_metrics(verified: list[VerifiedPainPoint], bundle: EvidenceBundle, scorer=None) -> CitationMetrics:
    """Reference-free ALCE-style citation precision/recall (NLI-mode only).

    Recall = fraction of verified points whose cited quotes are all supported by the
    concatenated premise of their *cited* urls (point.urls, not just the independently
    verified subset). Precision = over each (point, cited_url) citation, the fraction
    that are non-redundant -- a citation is redundant iff removing it still leaves the
    point supported by the remaining premise. Cited urls (not just supporting_urls) are
    the correct denominator: a url that doesn't independently support the claim can
    still be a genuine (if redundant) citation to test for redundancy.
    """
    if scorer is None:
        return CitationMetrics(None, None)
    points = [v for v in verified if v.verified]
    if not points:
        return CitationMetrics(None, None)

    recalls = []
    contributing = total = 0
    for v in points:
        quotes = v.point.quotes
        urls = v.point.urls
        recalls.append(1.0 if _all_claims_supported(quotes, _premise_for(bundle, urls), scorer) else 0.0)
        for u in urls:
            total += 1
            remaining = [x for x in urls if x != u]
            # redundant iff the point is still supported WITHOUT this citation
            still = bool(remaining) and _all_claims_supported(quotes, _premise_for(bundle, remaining), scorer)
            if not still:
                contributing += 1
    recall = round(sum(recalls) / len(recalls), 4)
    precision = round(contributing / total, 4) if total else None
    return CitationMetrics(precision=precision, recall=recall)
