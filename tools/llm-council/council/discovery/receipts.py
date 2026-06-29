# council/discovery/receipts.py
"""D2 — the per-card 'receipts' line: an evidence-depth gradient shared by both renderers.

Deterministic, $0, no model call. Every ranked card already passed the anti-fabrication
gate, so a binary "verified" stamp is meaningless (citation-hallucination runs 11-57% even
when links resolve). The receipt shows the GRADIENT — how deeply corroborated, how fresh —
in WORDS, never a checkmark or a raw float (those stay in the Size:/Confidence: detail lines).

Tiers are grounded in prior art (journalism's two-source rule + the NATO Admiralty
credibility scale for corroboration; the existing scoring.py recency decay for freshness).
The ladder CAPS at 'well-corroborated' (3+ domains): research (arXiv 2501.01303) finds no
trust gain from 1->5 citations, so a higher tier would manufacture false precision.
Spec: docs/superpowers/specs/2026-06-29-discovery-d2-receipts-ui-design.md.
Research: vault/20_projects/research/2026-06-29-receipts-provenance-ui-research.md.
"""

from __future__ import annotations

from council.discovery.scoring import RECENCY_FLOOR, ScoreBreakdown

# --- tunable thresholds (sensitivity-flagged, like scoring.py) ---
CORROBORATED_AT = 2        # journalism two-source rule: 2 independent sources = corroborated
WELL_CORROBORATED_AT = 3   # Admiralty "multiple independent"; ladder CAPS here (no higher tier).
                           # Distinct from (consistent with) scoring.DOMAIN_CEIL=4 score saturation.
FRESH_AT = 0.5             # mirrors frame._why_now's "Fresh signal" cutoff & scoring.RECENCY_NEUTRAL


def _corroboration(distinct_domains: int) -> str:
    n = max(int(distinct_domains), 0)
    if n >= WELL_CORROBORATED_AT:
        label = "well-corroborated"
    elif n >= CORROBORATED_AT:
        label = "corroborated"
    elif n == 1:
        label = "single-source"
    else:
        label = "uncorroborated"
    noun = "domain" if n == 1 else "domains"
    qualifier = "independent " if n >= CORROBORATED_AT else ""
    return f"{label} · {n} {qualifier}{noun}"


def _freshness(recency: float, evidence_date: str) -> str:
    # date-present gate FIRST: unparseable dates get recency=0.5 in scoring, which would
    # otherwise falsely read as 'fresh'. 'undated' is never 'fresh'.
    if not (evidence_date or "").strip():
        return "undated · no parseable evidence date"
    if recency >= FRESH_AT:
        badge = "fresh"
    elif recency > RECENCY_FLOOR:
        badge = "recent"
    else:
        badge = "aging"
    return f"{badge} · evidence {evidence_date}"


def receipt_line(score: ScoreBreakdown) -> str:
    """One compact receipts line: corroboration tier + freshness badge. Deterministic, $0."""
    return f"🧾 {_corroboration(score.distinct_domains)}  ·  {_freshness(score.recency, score.evidence_date)}"


def receipts_legend() -> str:
    """One-time explainer (NOT per-card); a D4-_CAVEAT-style markdown blockquote line."""
    return (
        "> 🧾 **Receipts** show evidence *depth*, not a verdict — every ranked item already "
        "cleared the anti-fabrication gate. **Corroboration** = independent source domains "
        "backing the pain (two-source rule: 1 = single-source, 2 = corroborated, 3+ = "
        "well-corroborated). **Freshness** = how recent the evidence is — a freshness signal, "
        "**not** proof; old pain can still be real."
    )
