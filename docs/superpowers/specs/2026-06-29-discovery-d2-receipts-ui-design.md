# D2 — Receipts UI (verification provenance per card)

**Status:** approved (brainstorm + research locked 2026-06-29)
**Roadmap item:** fusion-discovery-council Step B / D2 — the last Step-B item. Closes Step B.
**Cost:** $0 — render-layer only. No model call, no gate change, no new scoring logic.
**Research:** `vault/20_projects/research/2026-06-29-receipts-provenance-ui-research.md`

## Problem

Every card in the ranked ledgers has *already* passed the anti-fabrication gate
(`verified=True`), so a bare "✓ verified" stamp is true for 100% of cards and says nothing
(research: citation-hallucination 11–57% even when links resolve — a binary verified flag is
meaningless). The card's real signal is the **gradient**: how *deeply* corroborated and how
*fresh* the evidence is. That data already lives on `score: ScoreBreakdown` but is currently
spread across float-heavy `Size:`/`Confidence:` detail lines (PM card) or barely shown at all
(substack card, which only prints `Corroboration: N source domain(s)`).

D2 surfaces the gate work *as a glanceable, qualitative headline* on each card in **both**
ledgers — the "verified, not hallucinated" promise made visible, honestly.

## Goal

Add one compact **receipts line** directly under each card's `### N. title · score X/100`
heading (before `Who`/`Audience`), in both `render.py` (PM `IdeaCard`) and
`render_substack.py` (substack `PostAngle`). Two evidence-grounded axes:

```
🧾 well-corroborated · 3 independent domains  ·  fresh · evidence 2026-06-20
```

The existing detail lines (`Size:`, `Confidence:`, `Evidence:`, `Corroboration:`) stay
unchanged as the auditable float trail. The receipt is the headline judgment above them.

## Design

### New module: `council/discovery/receipts.py`

Modeled exactly on `whitespace.py` (the precedent for a shared, deterministic, $0 render
helper both renderers call). Single public entrypoint:

```python
def receipt_line(score: ScoreBreakdown) -> str:
    """One compact receipts line: corroboration tier + freshness badge. Deterministic, $0."""
```

Returns a single markdown line beginning with the `🧾` marker, e.g.
`🧾 single-source · 1 domain  ·  recent · evidence 2026-05-28`.

Plus a one-time legend helper (rendered once per ranked section, D4-`_CAVEAT`-style):

```python
def receipts_legend() -> str:
    """One-time explainer block; NOT per-card. Returns a markdown blockquote line."""
```

### Corroboration tier (off `score.distinct_domains` — the gate-truth count)

Grounded in journalism's two-source rule + NATO Admiralty "multiple independent sources":

| distinct_domains | label              |
|------------------|--------------------|
| 0                | `uncorroborated`   |
| 1                | `single-source`    |
| 2                | `corroborated`     |
| ≥ 3              | `well-corroborated`|

Constants in `receipts.py`, sensitivity-flagged like `scoring.py`:
- `CORROBORATED_AT = 2`   # journalism two-source rule
- `WELL_CORROBORATED_AT = 3`  # Admiralty "multiple independent"; **caps here** — research
  (arXiv 2501.01303: no trust gain 1→5 citations) says higher counts manufacture false
  precision. Distinct from (and consistent with) `scoring.DOMAIN_CEIL=4` score saturation.

Rendered as `{label} · {n} domain(s)` (singular/plural; "independent domain(s)" for n≥2).
A 0-domain card (shouldn't occur post-gate, but handle) reads `uncorroborated · 0 domains`.

### Freshness badge (off `score.recency` + `score.evidence_date`)

Reuses the existing decay (`recency = 0.5^(age/HALFLIFE_DAYS)`, floored at
`scoring.RECENCY_FLOOR=0.3`). **No parallel constants** — import `RECENCY_FLOOR` from
`scoring`; define `FRESH_AT = 0.5` documented as mirroring `frame._why_now`'s existing
"Fresh signal" cutoff and `scoring.RECENCY_NEUTRAL`.

Decision order (date-present gate is FIRST — the honesty trap):

1. `evidence_date == ""` → **`undated · no parseable evidence date`**
   (unparseable dates get `recency=0.5` in scoring; a naive `≥0.5` test would falsely call
   them "fresh" — so date-present is checked before any recency comparison).
2. `recency >= FRESH_AT` → **`fresh · evidence {date}`**
3. `recency > RECENCY_FLOOR` → **`recent · evidence {date}`**
4. else (`recency <= RECENCY_FLOOR`) → **`aging · evidence {date}`**

Freshness is a *freshness* signal, not a *truth* signal (old pain can still be real) — the
one-time legend carries that caveat; per-card text stays terse.

### One-time legend (`receipts_legend`)

Rendered once at the top of the ranked section (after the section heading, before the first
card), only when there is ≥1 card/angle. D4-`_CAVEAT`-style blockquote:

> 🧾 **Receipts** show evidence *depth*, not a verdict — every ranked item already cleared
> the anti-fabrication gate. **Corroboration** = independent source domains backing the pain
> (two-source rule: 1 = single-source, 2 = corroborated, 3+ = well-corroborated).
> **Freshness** = how recent the evidence is — a freshness signal, **not** proof; old pain
> can still be real.

### Wiring

- `render.py::render_ledger` — after `## Ranked Opportunities`, if `cards`: emit
  `receipts_legend()`; inside the per-card loop, emit `receipt_line(c.score)` immediately
  after the `### {i}. {title} · score` heading line.
- `render_substack.py::render_substack_ledger` — same, after `## Ranked Post Angles`, per
  `a.score`. (Brief `render_substack_brief` is a handoff artifact for the value-engine —
  out of scope; leave unchanged.)
- Empty / zero-verified path: no cards → no legend, no receipts, no crash (existing
  "_No pain points survived…_" note unchanged).

## Honesty invariants (sacred — mirror D4 discipline)

1. Receipt restates only what gate + scoring already established. No new claim.
2. A 1-domain card reads `single-source` — never a reassuring stamp. No `✓`/green check.
3. No float in the receipt harder than `confidence` implies (the receipt uses *words*; the
   floats stay in the detail lines).
4. `undated` is never rendered as `fresh` (date-present gate first).
5. Corroboration depth = evidence *breadth*, not proof of importance (legend states it once).
6. Freshness = recency, not truth (legend states it once).

## Testing ($0, deterministic, hermetic — mirror `test_render.py` conventions)

Construct `ScoreBreakdown` directly; assert substrings in rendered markdown.

**`test_receipts.py`** (unit, the helper):
- `well-corroborated` at 3 domains; `corroborated` at 2; `single-source` at 1; `uncorroborated` at 0.
- `fresh` (recency 0.84, date present); `recent` (recency 0.4); `aging` (recency 0.3).
- **`undated` when `evidence_date=""` even though `recency=0.5`** (the honesty trap).
- ≥3 caps at `well-corroborated` (5 domains still `well-corroborated`, no higher tier).
- Legend contains "depth, not a verdict" and the two-source mapping.

**`test_render.py`** (PM, extend existing):
- Well-corroborated fresh card renders the `🧾` line under the heading + legend once.
- Single-source card reads `single-source` (not a stamp).
- Detail lines (`Size:`/`Confidence:`) still present (receipt augments, doesn't replace).
- Empty cards → no `🧾`, no legend, no crash.

**`test_render_substack.py`** (substack, extend existing):
- Angle renders `🧾` line + legend once; single-source angle reads `single-source`;
  aging/undated badge maps correctly; empty angles → no receipts, no crash.

Run: `cd tools/llm-council && uv run pytest tests/ -q` (currently 233 passed, 1 skipped) +
`python3 scripts/validate.py` (repo root).

## Docs

- `.claude/skills/fusion-discovery-council/SKILL.md` §4 (FRAME/output) — describe the receipts line + legend.
- `CHANGELOG.md` — D2 entry.

## Out of scope / optional

- Consensus chip on the receipt — **rejected** (research: false-precision risk; consensus is
  model-agreement, a different axis; stays in the `Confidence:` detail line).
- Optional tidy (only if cheap & adjacent): E3's `rank_gaps` `blindspot(g)` recompute
  (O(gaps²·refs)) one-line precompute. Gap lists tiny — skip unless trivially clean.
