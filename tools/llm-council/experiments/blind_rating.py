"""Render two pain-point sets as anonymized, deterministically-shuffled blind-rating markdown."""

import hashlib

from council.discovery.fusion import CandidatePainPoint

_CRITERIA = (
    "## Rating criteria\n\n"
    "Rate each set on:\n"
    "1. **Signal density** — fraction of points naming a specific, real, recent user frustration (not generic).\n"
    "2. **Evidence grounding** — quotes/URLs that concretely support each point.\n"
    "3. **Distinctness / dup-rate** — are the points non-overlapping, or near-duplicates padding the count?\n"
    "4. **Actionability** — could a PM or creator act on this as an opportunity?\n\n"
    "Pick a winner per criterion, then an overall winner with a one-paragraph rationale. "
    "You are blind to how each set was produced — judge only the content.\n"
)


def _swap(topic: str) -> bool:
    """Deterministic, process-stable: True → A becomes Set 2 (sha256, not salted hash())."""
    return int(hashlib.sha256(topic.encode("utf-8")).hexdigest(), 16) % 2 == 1


def _render_set(points: list[CandidatePainPoint]) -> str:
    if not points:
        return "_(no pain points)_\n"
    lines = []
    for i, p in enumerate(points, 1):
        lines.append(f"{i}. **{p.title}** — {p.summary}")
        for q in p.quotes:
            lines.append(f"   - quote: \"{q}\"")
        for u in p.urls:
            lines.append(f"   - source: {u}")
    return "\n".join(lines) + "\n"


def build_blind_rating(arm_a: list[CandidatePainPoint], arm_b: list[CandidatePainPoint],
                       topic: str) -> tuple[str, dict]:
    if _swap(topic):
        set1, set2, key = arm_b, arm_a, {"Set 1": "B", "Set 2": "A"}
    else:
        set1, set2, key = arm_a, arm_b, {"Set 1": "A", "Set 2": "B"}
    md = (
        f"# Blind pain-point rating\n\n"
        f"Topic: {topic}\n\n"
        f"## Set 1\n\n{_render_set(set1)}\n"
        f"## Set 2\n\n{_render_set(set2)}\n"
        f"{_CRITERIA}"
    )
    return md, key
