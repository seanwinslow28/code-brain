# council/discovery/whitespace.py
"""D4 — the promoted '⭐ Whitespace Map' hero section, shared by both renderers.

Deterministic, $0, no model call. The whitespace map is by construction
absence-of-evidence (what the panel/evidence MISSED), so every gap's action is
"investigate/backfill" — never "build" — and no gap carries a fabricated score.
Spec: docs/superpowers/specs/2026-06-29-discovery-d4-whitespace-hero-design.md.
"""

_CAVEAT = (
    "> Gaps below = absence-of-evidence (what the panel and evidence did **not** surface), NOT "
    "verified claims or confirmed opportunities. The next move for each gap is to **investigate** "
    "it — never to build on it. Absence of a surfaced gap is not proof of full coverage."
)

_GAP_ACTION = ("   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in "
               "**Web Supplement (gap-fill)** below.")


def _drop_rate(verified_count: int, dropped_count: int) -> float:
    denom = verified_count + dropped_count
    return (dropped_count / denom) if denom else 0.0


def _sharpen_actions(*, has_gaps: bool, n_gaps: int, tier: str, segment: str,
                     verified_count: int, dropped_count: int) -> list[str]:
    """Ordered 'Sharpen the next run' lines; each included only when its condition holds."""
    out: list[str] = []
    if has_gaps:
        out.append(f"Backfill the {n_gaps} gap{'s' if n_gaps != 1 else ''} below with the agent's "
                   "own WebSearch/WebFetch (solution-side) — do this first.")
    if not (segment or "").strip():
        out.append("Add `--segment <audience>` to focus the gather.")
    if verified_count == 0:
        out.append("Widen or reframe the topic — nothing survived verification.")
    rate = _drop_rate(verified_count, dropped_count)
    # Gate is on the EXACT rate; the displayed percent is rounded for readability only.
    if tier != "deep" and rate >= 0.50:
        out.append(f"Raise tier to `deep` — thin verifiable signal (drop rate {round(rate * 100)}%).")
    return out


def whitespace_hero(*, blind_spots: list[str], tier: str, segment: str,
                    verified_count: int, dropped_count: int) -> list[str]:
    """Markdown lines for the promoted '## ⭐ Whitespace Map' hero section."""
    gaps = [g.strip() for g in (blind_spots or []) if g and g.strip()]
    L: list[str] = ["## ⭐ Whitespace Map — what this run MISSED\n"]

    def _sharpen(has_gaps: bool) -> None:
        actions = _sharpen_actions(has_gaps=has_gaps, n_gaps=len(gaps), tier=tier, segment=segment,
                                   verified_count=verified_count, dropped_count=dropped_count)
        if actions:
            L.append("**Sharpen the next run:**")
            L.extend(f"{i}. {a}" for i, a in enumerate(actions, 1))
            L.append("")

    if not gaps:
        L.append("_No blind spots surfaced — this run looks well-covered. (Absence of surfaced "
                 "gaps is not proof of full coverage.)_\n")
        _sharpen(has_gaps=False)
        return L

    L.append(_CAVEAT)
    L.append("")
    _sharpen(has_gaps=True)
    L.append("**Gaps the panel/evidence missed:**")
    for i, g in enumerate(gaps, 1):
        L.append(f"{i}. {g}")
        L.append(_GAP_ACTION)
    L.append("")
    return L
