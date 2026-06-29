"""Render the idea ledger markdown artifact."""

from council.discovery.backfill import BackfillResult, supplement_section
from council.discovery.frame import IdeaCard
from council.discovery.fusion import FusionResult


def render_ledger(*, topic: str, lens: str, tier: str, cards: list[IdeaCard],
                  quote_bank: list[str], fusion_result: FusionResult,
                  cost_usd: float, dropped_count: int,
                  supplement: "BackfillResult | None" = None) -> str:
    L: list[str] = []
    L.append(f"# Idea Ledger — {topic}\n")
    L.append(f"- **Lens:** `{lens}`  **Tier:** `{tier}`  **Verified ideas:** {len(cards)}")
    L.append(f"- **Cost:** ${cost_usd:.2f}  ·  Pain points dropped by verification: {dropped_count}\n")

    L.append("## Ranked Opportunities\n")
    if not cards:
        L.append("_No pain points survived verification. Low verifiable signal — widen the topic or raise the tier._\n")
    for i, c in enumerate(cards, 1):
        s = c.score
        L.append(f"### {i}. {c.title}  ·  score {s.composite:.0f}/100")
        L.append(f"- **Who:** {c.who}")
        L.append(f'- **Pain (their words):** {c.lead_quote}')
        L.append(f"  - {c.pain}")
        L.append("- **Evidence:** " + ", ".join(c.evidence_urls)
                 + f"  ·  {s.distinct_domains} independent domain(s)")
        L.append(f"- **Size:** importance {s.intensity}/5 · reach {s.reach:.2f} "
                 f"({s.engagement_sum} engagement, {s.distinct_sources} sources, "
                 f"{s.distinct_domains} domains) · recency {s.recency:.2f}")
        L.append(f"- **Confidence:** {s.confidence:.2f}× (sources {s.source_corroboration:.2f}, "
                 f"consensus {s.consensus_ratio:.2f})  →  value {s.value:.2f} × conf = {s.composite:.0f}/100")
        L.append(f"- **Why now:** {c.why_now}")
        L.append("- **Proposed bet** _(heuristic — confirm against evidence)_")
        L.append(f"  - Shape: {c.bet.shape}")
        L.append(f"  - Riskiest assumption: {c.bet.riskiest_assumption}")
        L.append(f"  - Cheapest test: {c.bet.cheapest_test}")
        L.append("  - _Your call: _________________________________")
        L.append("")

    L.append("## Blind-spot / Whitespace Map\n")
    L.extend(f"- {b}" for b in (fusion_result.blind_spots or ["_(none surfaced)_"]))
    L.append("")
    L.extend(supplement_section(supplement))      # Stage 5 — sits next to the gaps it answers ([] if None)
    L.append("## Contradiction Map\n")
    L.extend(f"- {c}" for c in (fusion_result.contradictions or ["_(none surfaced)_"]))
    L.append("")
    L.append("## Quote Bank\n")
    L.extend(f"- {q}" for q in (quote_bank or ["_(empty)_"]))
    L.append("")
    L.append("## Cost Summary\n")
    L.append(f"- Approx cost: ${cost_usd:.2f}")
    L.append(f"- Pain points dropped by verification: {dropped_count}")
    return "\n".join(L)
