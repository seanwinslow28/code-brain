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
from urllib.parse import urlparse

from council.discovery.fusion import FusionResult
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
    score: float
    corroboration: int


def _domains(urls: list[str]) -> int:
    return len({urlparse(u).netloc for u in urls if u})


def frame_substack(verified: list[VerifiedPainPoint], fusion_result: FusionResult,
                   segment: str = "") -> tuple[list[PostAngle], list[str]]:
    angles: list[PostAngle] = []
    quote_bank: list[str] = []
    seen_q: set[str] = set()
    whitespace = "; ".join(fusion_result.blind_spots) if fusion_result.blind_spots else ""
    for v in verified:
        if not v.verified:
            continue
        pt = v.point
        corr = _domains(v.supporting_urls)
        score = float(pt.intensity or 1) * (1 + corr)
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
            corroboration=corr,
        ))
        for q, u in zip(pt.quotes, v.supporting_urls + [""] * len(pt.quotes)):
            line = f'"{q}" — {u}'.rstrip(" —")
            if line not in seen_q:
                seen_q.add(line)
                quote_bank.append(line)
    angles.sort(key=lambda a: a.score, reverse=True)
    return angles, quote_bank
