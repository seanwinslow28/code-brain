# Design — fusion-discovery-council PM4 + D1: real opportunity score + PRD-grade card

**Date:** 2026-06-29
**Branch:** `feat/discovery-pm4-d1-score-card`
**Roadmap:** Step B / PM4 + D1 (the 2026-06-28 conversion audit's #1 felt-value win). Maps to ledger O2 ("it tells me a pain exists, not whether it's worth acting on or *why now*").
**Cost:** $0 new API spend — the score is computed deterministically from data already in the evidence bundle + fusion result.

## Goal

The PM-lens idea ledger produces PRD-grade opportunity cards, each with a defensible composite score and a riskiest-assumption / cheapest-test bet. Replace:
- the **toy score** ([frame.py:37](../../../tools/llm-council/council/discovery/frame.py#L37)) `score = float(pt.intensity or 1) * (1 + corr)`, and
- the **filler card** (`workaround` hardcoded + never rendered; `opportunity` a templated string).

with an ODI/RICE-style composite + an honest, auditable card.

## Non-negotiables

- **Verification gate stays sacred.** The score never invents data; cards cite only gate-survived URLs (`v.supporting_urls`). No fabrication anywhere.
- **No new network calls / no API spend.** Everything is derived from `VerifiedPainPoint` + `EvidenceBundle` + `FusionResult` already in memory.
- **TDD** — watch each new helper's tests fail first.
- **Determinism / testability** — `today` is injectable so recency decay is testable without wall-clock.

## Components

### 1. New module `council/discovery/scoring.py`

```python
@dataclass(frozen=True)
class ScoreBreakdown:
    composite: float          # 0-100, the headline rank
    importance: float         # 0-1 normalized
    reach: float              # 0-1 normalized
    recency: float            # 0-1 normalized
    corroboration: float      # 0-1 normalized
    # raw audit fields — render the honest "Size" line:
    intensity: int
    engagement_sum: int
    distinct_authors: int
    distinct_domains: int
    consensus_ratio: float
    evidence_date: str        # parsed date actually used, or ""

def score_opportunity(
    point: CandidatePainPoint,
    supporting_urls: list[str],
    bundle: EvidenceBundle,
    *,
    today: date | None = None,
    weights: dict[str, float] = DEFAULT_WEIGHTS,
) -> ScoreBreakdown: ...
```

**Tunable module-level constants** (no config.toml plumbing this session — YAGNI):
- `DEFAULT_WEIGHTS = {"importance": 0.35, "reach": 0.30, "recency": 0.15, "corroboration": 0.20}` (sum 1.0)
- `REACH_CEIL = 500` (engagement saturation), `BREADTH_CEIL = 8` (authors+domains saturation)
- `HALFLIFE_DAYS = 30`, `RECENCY_FLOOR = 0.3`, `RECENCY_NEUTRAL = 0.5` (unparseable date)
- `DOMAIN_CEIL = 4` (distinct domains for full corroboration credit)

**Component math (each → [0,1]):**

| Component | Formula |
|---|---|
| **importance** | `max(int(point.intensity or 0), 1) / 5`, clamped [0,1] |
| **reach** | `eng_sum` = Σ engagement over `bundle.records` whose `url ∈ supporting_urls`; `breadth` = distinct `source_name` + distinct `urlparse(u).netloc`. `reach = 0.7 * log1p(eng_sum)/log1p(REACH_CEIL) + 0.3 * min(breadth/BREADTH_CEIL, 1)`, clamped [0,1] |
| **recency** | date = parse `point.recency` (defensive: "YYYY-MM" / "YYYY-MM-DD" / "YYYY"); else max parseable `rec.date` among supporting records. age = `(today - date).days` (≥0). `recency = max(0.5 ** (age / HALFLIFE_DAYS), RECENCY_FLOOR)`. Unparseable → `RECENCY_NEUTRAL` |
| **corroboration** | `domains` = distinct netloc; `consensus_ratio` = parsed `point.consensus` ("4/4 models" → 1.0; unparseable → 0.0). `corroboration = 0.6 * min(domains/DOMAIN_CEIL, 1) + 0.4 * consensus_ratio` |

`composite = round(100 * Σ weight_i * component_i, 1)`.

**Helpers (private, also unit-tested):** `_parse_loose_date(s) -> date | None`, `_parse_consensus(s) -> float`.

### 2. New module `council/discovery/bet.py`

```python
@dataclass(frozen=True)
class ProposedBet:
    shape: str                # one of the 5 shapes
    riskiest_assumption: str  # category, not a fabricated specific
    cheapest_test: str        # a test pattern

def classify_pain_shape(point: CandidatePainPoint) -> str: ...
def propose_bet(point: CandidatePainPoint) -> ProposedBet: ...
```

`classify_pain_shape` keyword-matches `title + " " + summary` (lowercased), **first match wins** in this priority order:
1. **trust-gap** — wrong, hallucinat, inaccurate, unreliable, trust, error, made up
2. **cost-pain** — expensive, pricing, price, cost, afford, too much, paywall
3. **integration-gap** — integrat, api, connect, sync, export, import, compat, plugin
4. **workflow-friction** — slow, tedious, manual, workaround, friction, clunky, too many steps
5. **missing-capability** — default fallback

Each shape → a fixed `(riskiest_assumption, cheapest_test)` from a constant map. Rendered under a "heuristic — confirm against evidence" label with a human fill-in slot. **No invented insight** — only a structurally-derived starting category + test pattern.

### 3. `IdeaCard` redesign (`frame.py`)

```python
@dataclass
class IdeaCard:
    title: str
    who: str
    pain: str                 # the summary (secondary line)
    lead_quote: str           # the verbatim quote — pain in their words
    evidence_urls: list[str]
    quotes: list[str]         # full quote list (feeds quote bank)
    score: ScoreBreakdown
    why_now: str              # deterministic from recency component + evidence_date
    bet: ProposedBet
```

Dropped: `workaround` (dead), `opportunity` (filler), bare `score: float`, `corroboration: int` (now inside `ScoreBreakdown`).

`why_now` is derived deterministically — high recency → "Fresh signal — evidence dated {date}"; low → "Older signal (evidence {date}); confirm it's still live"; no date → "Recency unknown — verify the pain is current." No fabrication.

`frame_pm(verified, fusion_result, bundle, *, today=None)` — new `bundle` param (in scope at the call site). Cards sorted by `score.composite` desc.

### 4. `render_ledger` redesign (`render.py`)

Per card:
```
### N. {title}  ·  score {composite}/100
- **Who:** {who}
- **Pain (their words):** "{lead_quote}"
  - {pain}
- **Evidence:** {urls}  ·  corroboration {distinct_domains} domain(s)
- **Size:** importance {intensity}/5 · reach {reach:.2f} ({engagement_sum} engagement, {distinct_authors} authors, {distinct_domains} domains) · recency {recency:.2f} · corroboration {corroboration:.2f}
- **Why now:** {why_now}
- **Proposed bet** _(heuristic — confirm against evidence)_
  - Shape: {shape}
  - Riskiest assumption: {riskiest_assumption}
  - Cheapest test: {cheapest_test}
  - _Your call: _________________________________
```

### 5. Substack lens (shared score)

- `frame_substack(verified, fr, bundle, *, segment="", today=None)` adopts `score_opportunity`.
- `PostAngle.score` becomes `ScoreBreakdown` (was `float`); `PostAngle.corroboration` removed (now `score.distinct_domains`).
- `render_substack.py` reads `a.score.composite` (was `a.score:.1f`) and `a.score.distinct_domains` (was `a.corroboration`). PostAngle's card *shape* is otherwise unchanged — only the score is shared.

### 6. Pipeline wiring

[pipeline.py:120 & 127](../../../tools/llm-council/council/discovery/pipeline.py#L120) — pass `bundle` (and one `today = date.today()`) into both `frame_substack` and `frame_pm`.

## Testing

- **New** `tests/discovery/test_scoring.py` — each component normalized correctly; composite weighting; edge cases (intensity missing/0, unparseable recency → neutral, zero engagement, consensus "4/4"/"3/4"/garbage, recency floor holds, `today` injection).
- **New** `tests/discovery/test_bet.py` — each shape classified by keyword, priority order, default fallback, stable bet text.
- **Update** `test_frame.py`, `test_render.py`, `test_frame_substack.py`, `test_render_substack.py` to the new shapes (RED first).
- **Verify:** `cd tools/llm-council && uv run pytest tests/ -q` (full council suite green) + `python3 scripts/validate.py` (repo root).

## Docs

- `SKILL.md` §2 (FRAME description) + §6 ("what to surface") — note the new score + card shape and that the bet is a labeled heuristic.
- `CHANGELOG.md` `[Unreleased]` entry.
- `tickets.md` — mark Step B / PM4+D1 progress.

## Out of scope (later roadmap steps)

E3 MMR dedup, D4 whitespace-hero, D2 receipts (rest of Step B); E1 entailment gate (Step D). The recency-decay constant here is shared groundwork E3 will build on.
