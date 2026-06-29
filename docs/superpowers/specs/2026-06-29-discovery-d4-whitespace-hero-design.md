---
title: Discovery D4 — Whitespace Map as hero output
date: 2026-06-29
status: approved
component: tools/llm-council/council/discovery
roadmap_item: D4 (fusion-discovery-council improvement ledger §4/§5)
research: vault/20_projects/research/2026-06-29-whitespace-gap-map-presentation-research.md
informs: render.py, render_substack.py, new whitespace.py
---

# D4 — Whitespace Map as hero output

## Problem

Today both ledger renderers bury the blind-spot/whitespace map as a bare `- {b}` bullet list
*after* the ranked cards ([render.py:41-43](../../../tools/llm-council/council/discovery/render.py),
[render_substack.py:31-33](../../../tools/llm-council/council/discovery/render_substack.py)) — even
though SKILL.md §6 calls it "often the highest-signal section." It lists absences with zero "what to
do about it." Worse, the whitespace map is the *input* to the most-acted-on downstream step (the
Stage-5 agent backfill), and the Week-0 conversion audit (ledger §11) ranked it the next-biggest
felt win after PM4.

## Research grounding (what shaped this design)

From [the gap-map presentation research](../../../vault/20_projects/research/2026-06-29-whitespace-gap-map-presentation-research.md):

- **Each gap = statement → why-it-matters → recommended next *direction*** (not a mandated build) is
  what converts a passive bullet into an actionable insight [NN/G, 3-0].
- **Absence-of-evidence ≠ evidence-of-absence** — a blind spot is *unstudied by this run*, so its
  honest action is "investigate it," never "build on it" [peer-reviewed, 3-0]. This is the central
  guardrail: the map must never assert a gap *is* a confirmed opportunity.
- **Prioritize at the opportunity layer; lead with recommendations; cap the list** [Torres + Infomineo].
- **Pair each gap with a directed next step whose actor controls the inputs** — here the actor is the
  orchestrating agent with WebSearch/WebFetch, so "backfill this gap" is a real action, not a void.
- **No false precision** — don't attach a fabricated confidence number to a gap (it has, by
  definition, no supporting evidence) [OrgVitality].

## Design

### New module: `council/discovery/whitespace.py`

Single public helper, deterministic, $0, no model call. Both renderers call it.

```python
def whitespace_hero(
    *, blind_spots: list[str], tier: str, segment: str,
    verified_count: int, dropped_count: int,
) -> list[str]:
    """Markdown lines for the promoted '## ⭐ Whitespace Map' hero section.
    Deterministic from run metadata only — never fabricates evidence or scores."""
```

Internal helpers (module-private, individually testable):
- `_sharpen_actions(*, has_gaps, tier, segment, verified_count, dropped_count) -> list[str]` —
  builds the ordered "Sharpen the next run" list from the 4 rules below.
- `_drop_rate(verified_count, dropped_count) -> float` — `dropped / (dropped + verified)`, `0.0`
  when the denominator is 0 (guard div-by-zero).

### The rendered hero block

Placed at the very top of each ledger, immediately after the meta header lines, **before** the
ranked cards/angles.

```
## ⭐ Whitespace Map — what this run MISSED

> Gaps below = absence-of-evidence (what the panel and evidence did **not** surface), NOT verified
> claims or confirmed opportunities. The next move for each gap is to **investigate** it — never to
> build on it. Absence of a surfaced gap is not proof of full coverage.

**Sharpen the next run:**
1. Backfill the N gaps below with the agent's own WebSearch/WebFetch (solution-side) — do this first.
2. Add `--segment <audience>` to focus the gather.
3. Widen or reframe the topic — nothing survived verification.
4. Raise tier to `deep` — thin verifiable signal (drop rate 67%).

**Gaps the panel/evidence missed:**
1. <verbatim blind_spot string>
   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in **Web Supplement (gap-fill)** below.
2. …
```

### The 4 "Sharpen the next run" rules (deterministic, conditional)

Evaluated in this fixed order; each line is included only when its condition holds. Numbering is
applied after filtering (so the list is always `1..k` with no gaps).

| # | Condition | Line |
|---|---|---|
| 1 | `len(blind_spots) > 0` | `Backfill the {N} gaps below with the agent's own WebSearch/WebFetch (solution-side) — do this first.` |
| 2 | `segment` is empty/whitespace | `Add `--segment <audience>` to focus the gather.` |
| 3 | `verified_count == 0` | `Widen or reframe the topic — nothing survived verification.` |
| 4 | `tier != "deep"` AND `_drop_rate ≥ 0.50` | `Raise tier to `deep` — thin verifiable signal (drop rate {pct}%).` |

If **no** rule fires (gaps present, segment set, cards verified, low drop rate, deep tier), the
"Sharpen the next run" list is omitted entirely (no empty header).

### Per-gap action

Uniform across gaps (Sean chose per-gap-action + global-list, not keyword classification):

```
N. <verbatim blind_spot>
   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in **Web Supplement (gap-fill)** below.
```

Gaps are numbered in panel order — we do **not** claim a ranking we don't compute (no per-gap score;
honest per research finding 7 / no false precision).

### Empty-gaps path

When `blind_spots` is empty:

```
## ⭐ Whitespace Map — what this run MISSED

_No blind spots surfaced — this run looks well-covered. (Absence of surfaced gaps is not proof of
full coverage.)_
```

Rule 1 is omitted (no gaps to backfill); rules 2–4 still render if their conditions hold (they're
about run quality, independent of gaps), under the "Sharpen the next run:" header.

### Wiring into the renderers

**`render.py` (`render_ledger`)** new section order:
1. Title + meta header (unchanged)
2. **`## ⭐ Whitespace Map`** hero — `whitespace_hero(blind_spots=fr.blind_spots, tier=tier, segment=segment, verified_count=len(cards), dropped_count=dropped_count)`  ← NEW, here
3. `## Ranked Opportunities` (cards) — unchanged
4. `supplement_section(supplement)` (in-CLI Web Supplement; `[]` when None) — unchanged position
5. `## Contradiction Map` — unchanged
6. `## Quote Bank` — unchanged
7. `## Cost Summary` — unchanged

The old `## Blind-spot / Whitespace Map` block (step between Ranked and supplement) is **removed** —
its content is now the hero.

**`render_substack.py` (`render_substack_ledger`)** mirrors exactly: hero after meta header, before
`## Ranked Post Angles`; old `## Blind-spot / Whitespace Map` block removed; `verified_count =
len(angles)`. `render_substack_brief` is untouched.

**Signature change:** `render_ledger` already receives `lens`/`tier`; it needs `segment` to drive
rule 2. `render_substack_ledger` needs `segment` too. Both gain a `segment: str = ""` keyword param.
`pipeline.py` passes the already-normalized `segment` to both render calls (it's in scope —
`run_discovery` normalizes it at the top).

### What does NOT change (scope guard)

- `backfill.py` / `supplement_section` / `verify_supplement.py` — untouched. The Web Supplement keeps
  its `## Web Supplement (gap-fill)` heading and append-at-end behavior; the hero links to it by
  reference only.
- `## Contradiction Map`, `## Quote Bank`, `## Cost Summary` — unchanged content and relative order.
- The gate, scoring, framing — untouched. This is a pure presentation change, $0, no new API.

## Honesty / gate compliance

- The hero is **never** rendered as verified claims; the caveat blockquote states gaps are
  absence-of-evidence explicitly.
- No fabricated confidence/precision on any gap.
- Per-gap action is always "investigate/backfill," never "build" — the absence-of-evidence guardrail
  made operational.

## Testing (TDD)

New `tests/discovery/test_whitespace.py`:
- `_drop_rate`: 0 when denominator 0; correct fraction otherwise.
- Rule 1 present iff gaps exist; says the right N.
- Rule 2 present iff segment empty; absent when segment set.
- Rule 3 present iff verified_count == 0.
- Rule 4 present iff `tier != deep` and drop_rate ≥ 0.50; shows the integer pct; silent at 49%; silent on `deep` tier even at high drop.
- All-rules-silent → no "Sharpen the next run:" header at all.
- Sharpen list renumbered `1..k` after filtering (no numbering gaps).
- Per-gap action line present for each gap; uniform; references "Web Supplement".
- Honesty caveat blockquote present (the "absence-of-evidence" string).
- Empty gaps → "No blind spots surfaced" note, no rule-1 line.

Updates to `test_render.py` / `test_render_substack.py`:
- Hero `## ⭐ Whitespace Map` appears **before** `## Ranked Opportunities` / `## Ranked Post Angles`.
- Old `## Blind-spot / Whitespace Map` heading no longer present.
- Existing supplement byte-identical invariant (`supplement=None` == omitted) still holds.
- Supplement still precedes Contradiction Map (pm lens).

Verify: `cd tools/llm-council && uv run pytest tests/ -q` (was 195 passed, 1 skipped after PM4) +
`python3 scripts/validate.py` (repo root).

## Docs to update (in the same PR)

- SKILL.md §2 (stage 5 reference to the map), §4.1 step 2 ("Read the blind-spot map" — new heading),
  §6 (the "blind-spot / whitespace map" reporting note) — point at the new `## ⭐ Whitespace Map`
  heading and note it now leads the ledger with actions.
- CHANGELOG.md — D4 entry.
- `vault/00_inbox/tickets.md` — mark D4 done in the roadmap ticket (confirm vault-commit inclusion
  with Sean).

## Out of scope (future roadmap)

- E3 (MMR dedup + recency/reach decay of the *gaps* themselves) — would let us genuinely rank gaps;
  until then we present panel order without a rank claim.
- D2 (receipts UI on cards). E1 (entailment gate). Keyword-classified per-gap actions (rejected as
  brittle during brainstorm).
