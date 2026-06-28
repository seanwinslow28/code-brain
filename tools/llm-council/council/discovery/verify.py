# council/discovery/verify.py
"""Stage 3 — fabrication gate. A pain point survives only if a quote it cites
actually appears at a URL present in the evidence bundle."""

from dataclasses import dataclass

from council.discovery.evidence import EvidenceBundle
from council.discovery.fusion import CandidatePainPoint


@dataclass
class VerifiedPainPoint:
    point: CandidatePainPoint
    verified: bool
    supporting_urls: list[str]


def quote_supported_at_url(*, cited_quote: str, fetched_text: str) -> bool:
    """The single anti-fabrication primitive: does the *cited* quote actually appear in the
    *fetched* text? Substring containment, lowercased — no reverse-containment (that would let a
    fabricated long quote embed a real short one and pass).

    This is the one shared chokepoint for BOTH Stage 3 VERIFY and Stage 5 BACKFILL. Roadmap item
    E1 will upgrade it in place from substring containment to atomic-claim + NLI entailment
    (taking the claim/gap as an extra argument); both call sites inherit that upgrade for free.
    """
    needle = cited_quote.strip().lower()
    return bool(needle) and needle in fetched_text.strip().lower()


def _quote_present_at_url(bundle: EvidenceBundle, url: str, quotes: list[str]) -> bool:
    for rec in bundle.records:
        if rec.url != url:
            continue
        for q in quotes:
            if quote_supported_at_url(cited_quote=q, fetched_text=rec.quote):
                return True
    return False


def verify_pain_points(points: list[CandidatePainPoint], bundle: EvidenceBundle) -> list[VerifiedPainPoint]:
    out: list[VerifiedPainPoint] = []
    for pt in points:
        supporting = [
            u for u in pt.urls
            if bundle.has_url(u) and _quote_present_at_url(bundle, u, pt.quotes)
        ]
        out.append(VerifiedPainPoint(point=pt, verified=bool(supporting), supporting_urls=supporting))
    return out
