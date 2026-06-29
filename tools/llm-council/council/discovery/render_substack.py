# council/discovery/render_substack.py
"""Render the substack-lens artifacts: a ranked post-angle idea ledger and a
substack-value-engine handoff brief."""

from council.discovery.backfill import BackfillResult, supplement_section
from council.discovery.frame_substack import PostAngle
from council.discovery.fusion import FusionResult
from council.discovery.receipts import receipt_line, receipts_legend
from council.discovery.whitespace import whitespace_hero


def render_substack_ledger(*, topic: str, tier: str, segment: str = "", angles: list[PostAngle],
                           quote_bank: list[str], fusion_result: FusionResult,
                           cost_usd: float, dropped_count: int,
                           supplement: "BackfillResult | None" = None, merged_count: int = 0) -> str:
    L: list[str] = []
    L.append(f"# Substack Idea Ledger — {topic}\n")
    L.append(f"- **Lens:** `substack`  **Tier:** `{tier}`  **Post angles:** {len(angles)}")
    L.append(f"- **Cost:** ${cost_usd:.2f}  ·  Pain points dropped by verification: {dropped_count}\n")
    if merged_count:
        L.append(f"- Merged {merged_count} near-duplicate pain point(s) before ranking.\n")

    # D4 — the whitespace map LEADS the ledger (highest-signal section; feeds the agent backfill).
    L.extend(whitespace_hero(blind_spots=fusion_result.blind_spots, tier=tier, segment=segment,
                             verified_count=len(angles), dropped_count=dropped_count))

    L.append("## Ranked Post Angles\n")
    if not angles:
        L.append("_No pain points survived verification. Low verifiable signal — widen the topic or raise the tier._\n")
    else:
        L.append(receipts_legend())
        L.append("")
    for i, a in enumerate(angles, 1):
        L.append(f"### {i}. {a.title}  ·  score {a.score.composite:.0f}/100")
        L.append(receipt_line(a.score))
        L.append(f"- **Audience:** {a.audience}")
        L.append(f"- **Hook:** {a.hook}")
        L.append(f"- **Transfer:** {a.transfer}")
        L.append(f"- **Corroboration:** {a.score.distinct_domains} source domain(s)")
        L.append("- **Evidence:** " + ", ".join(a.evidence_urls))
        L.append("")
    L.extend(supplement_section(supplement))      # Stage 5 — Web Supplement the hero links to ([] if None)
    L.append("## Quote Bank\n")
    L.extend(f"- {q}" for q in (quote_bank or ["_(empty)_"]))
    L.append("")
    L.append("## Cost Summary\n")
    L.append(f"- Approx cost: ${cost_usd:.2f}")
    L.append(f"- Pain points dropped by verification: {dropped_count}")
    return "\n".join(L)


def render_substack_brief(*, topic: str, segment: str, angles: list[PostAngle]) -> str:
    """A handoff brief consumable by the substack-value-engine skill.

    Pre-fills the candidate Itch + Transfer (Value-Gate slots 1 & 3) and the verbatim
    evidence; leaves Solution (slot 2) for Sean — the gate BLOCKS until that is a real,
    first-person artifact. Chain: substack-value-engine → storytelling-architecture →
    writing-voice-modes → writing-critique → writing-humanity-pass.
    """
    L: list[str] = []
    L.append(f"# Substack Handoff Brief — {topic}\n")
    L.append("> Feed this into `substack-value-engine`. Each angle pre-fills the Value-Gate **Itch**")
    L.append("> and **Transfer** from real evidence; you supply the **Solution** (what you actually did).")
    L.append("> The gate BLOCKS any angle whose Itch isn't genuinely yours or whose Solution isn't a real")
    L.append("> artifact. Chain: substack-value-engine → storytelling-architecture → writing-voice-modes →")
    L.append("> writing-critique → writing-humanity-pass.\n")
    if segment:
        L.append(f"- **Target segment:** {segment}\n")
    if not angles:
        L.append("_No verified pain points — no angles to brief. Widen the topic or raise the tier._")
        return "\n".join(L)
    for i, a in enumerate(angles, 1):
        L.append(f"## Angle {i}: {a.title}  ·  score {a.score.composite:.0f}/100")
        L.append(f"- **Audience:** {a.audience}")
        L.append(f"- **Hook (open loop):** {a.hook}")
        L.append(f"- **Itch (Value-Gate slot 1 — candidate, verify it's genuinely yours):** {a.itch}")
        L.append("- **Solution (slot 2 — you fill):** _What did you actually do? The gate blocks until this is a real run/eval/commit/number._")
        L.append(f"- **Transfer (slot 3 — candidate):** {a.transfer}")
        if a.whitespace:
            L.append(f"- **Whitespace / differentiation:** {a.whitespace}")
        L.append("- **Evidence (proof the pain is real):**")
        if a.quotes:
            for q, u in zip(a.quotes, a.evidence_urls + [""] * len(a.quotes)):
                L.append(f'  - "{q}"' + (f" — {u}" if u else ""))
        else:
            L.append("  - _(no verbatim quotes captured)_")
        L.append("")
    return "\n".join(L)
