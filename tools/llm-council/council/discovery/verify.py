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


def _quote_present_at_url(bundle: EvidenceBundle, url: str, quotes: list[str]) -> bool:
    for rec in bundle.records:
        if rec.url != url:
            continue
        hay = rec.quote.strip().lower()
        for q in quotes:
            needle = q.strip().lower()
            if needle and (needle in hay or hay in needle):
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
