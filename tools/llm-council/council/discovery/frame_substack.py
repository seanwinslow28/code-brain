# council/discovery/frame_substack.py
"""Stage 4 (substack lens) — verified pain points → ranked post angles + a
substack-value-engine handoff brief.

A post angle reframes a *verified* user pain point (the same gate-survived points
frame_pm consumes — no new Fusion call) into the raw material the Substack writing
chain needs: a hook (open loop), a candidate Value-Gate Itch, a Transfer promise, the
whitespace differentiation, and the verbatim evidence that proves the pain is real. It
does NOT write prose and does NOT invent the author's first-person itch or solution —
those slots stay for substack-value-engine to gate.
"""

from dataclasses import dataclass
from datetime import date

from council.discovery.evidence import EvidenceBundle
from council.discovery.fusion import FusionResult
from council.discovery.scoring import ScoreBreakdown, score_opportunity
from council.discovery.verify import VerifiedPainPoint


@dataclass
class PostAngle:
    title: str               # working post title / angle
    audience: str            # who feels the pain (CLI --segment, else the per-pain segment)
    hook: str                # the open-loop / half-told problem
    itch: str                # candidate Value-Gate Itch (the real, checkable problem)
    transfer: str            # Value-Gate Transfer: "After reading, the reader can ___"
    evidence_urls: list[str]
    quotes: list[str]
    whitespace: str          # angle differentiation (from the blind-spot/whitespace map)
    score: ScoreBreakdown


def frame_substack(verified: list[VerifiedPainPoint], fusion_result: FusionResult,
                   bundle: EvidenceBundle, *, segment: str = "",
                   today: date | None = None) -> tuple[list[PostAngle], list[str]]:
    today = today or date.today()
    angles: list[PostAngle] = []
    quote_bank: list[str] = []
    seen_q: set[str] = set()
    whitespace = "; ".join(fusion_result.blind_spots) if fusion_result.blind_spots else ""
    for v in verified:
        if not v.verified:
            continue
        pt = v.point
        score = score_opportunity(pt, v.supporting_urls, bundle, today=today)
        angles.append(PostAngle(
            title=pt.title,
            audience=segment or pt.segment or "readers",
            hook=pt.summary or pt.title,
            itch=f"{pt.title}: {pt.summary}".rstrip(": ").strip(),
            transfer=f"After reading, the reader can address '{pt.title}' themselves.",
            evidence_urls=v.supporting_urls,
            quotes=pt.quotes,
            whitespace=whitespace,
            score=score,
        ))
        for q, u in zip(pt.quotes, v.supporting_urls + [""] * len(pt.quotes)):
            line = f'"{q}" — {u}'.rstrip(" —")
            if line not in seen_q:
                seen_q.add(line)
                quote_bank.append(line)
    angles.sort(key=lambda a: a.score.composite, reverse=True)
    return angles, quote_bank
