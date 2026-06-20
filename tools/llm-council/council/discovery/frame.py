# council/discovery/frame.py
"""Stage 4 (pm lens) — verified pain points → ranked opportunity cards + quote bank."""

from dataclasses import dataclass
from urllib.parse import urlparse

from council.discovery.fusion import FusionResult
from council.discovery.verify import VerifiedPainPoint


@dataclass
class IdeaCard:
    title: str
    who: str
    pain: str
    workaround: str
    opportunity: str
    evidence_urls: list[str]
    quotes: list[str]
    score: float
    corroboration: int


def _domains(urls: list[str]) -> int:
    return len({urlparse(u).netloc for u in urls if u})


def frame_pm(verified: list[VerifiedPainPoint], fusion_result: FusionResult) -> tuple[list[IdeaCard], list[str]]:
    cards: list[IdeaCard] = []
    quote_bank: list[str] = []
    seen_q: set[str] = set()
    for v in verified:
        if not v.verified:
            continue
        pt = v.point
        corr = _domains(v.supporting_urls)
        score = float(pt.intensity or 1) * (1 + corr)
        cards.append(IdeaCard(
            title=pt.title,
            who=pt.segment or "users",
            pain=f"{pt.title}: {pt.summary}",
            workaround="(from evidence — see quotes)",
            opportunity=f"Ship a capability that removes '{pt.title}' for {pt.segment or 'users'}.",
            evidence_urls=v.supporting_urls,
            quotes=pt.quotes,
            score=score,
            corroboration=corr,
        ))
        for q, u in zip(pt.quotes, v.supporting_urls + [""] * len(pt.quotes)):
            line = f'"{q}" — {u}'.rstrip(" —")
            if line not in seen_q:
                seen_q.add(line)
                quote_bank.append(line)
    cards.sort(key=lambda c: c.score, reverse=True)
    return cards, quote_bank
