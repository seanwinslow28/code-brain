# Spec — fusion-discovery-council E4: velocity scoring channel (v1)

**Date:** 2026-07-09
**Campaign:** Phase 2 "everything buildable now" — Item 2 (the flagship build)
**Branch:** `feat/discovery-e4-velocity-channel`
**Method:** brainstorming → this spec → writing-plans → subagent-driven-development (TDD)
**Baseline:** `main` after PR #112 — **303 passed, 1 skipped**.

## Purpose

Give every idea card a real **"why now"** — a demand *slope*, not just a freshness note off a single
evidence date. This is the layer competitors sell separately (Exploding Topics = velocity,
AnswerThePublic = demand-intent); fusing it into the already-gated card is the unclaimed moat.

E4 v1 ships the **velocity** half (a demand slope). The **demand-intent** half (autocomplete /
People-Also-Ask) is *designed-for but deferred* — it needs a metered API (SerpApi) that v1 does not
take on. The channel's data shape is built to carry it later.

## THE LOAD-BEARING INVARIANT (the moat — do not violate)

Velocity is a **SCORE signal ONLY, NEVER gate-evidence.** Autocomplete/PAA/trend terms produce
*queries and numbers, not URL-anchored quotes* — they must never enter `verify.py`, the
`EvidenceBundle`, or be paraphrased into a sourced claim.

Enforced **structurally**, reviewer-checkable:

1. `velocity.py` imports only stdlib + optional `pytrends`. It imports **nothing** from `verify.py`
   or any `EvidenceBundle`-write path. It takes plain `str` terms and returns numbers.
2. In `pipeline.py`, the velocity provider is resolved and used **strictly after**
   `verify_pain_points` / `citation_metrics` — downstream of the gate by construction.
3. A dedicated test asserts all three:
   - velocity output never appears in `bundle.records`, `evidence_urls`, or `quotes`;
   - `verify_pain_points(...)` output is **byte-identical** with velocity on vs. off (same bundle,
     same verified list) — proving the channel cannot perturb the gate;
   - an import guard: `velocity.py`'s module imports never include `verify`.

## Design decisions (locked in brainstorming, 2026-07-09)

| Decision | Choice | Why |
|---|---|---|
| v1 source | **Stub default + pytrends optional** (no SerpApi) | $0, CI-clean, mirrors E1's optional-dep seam; demand-intent deferred |
| Score folding | **Separate bounded term, `VELOCITY_WEIGHT` defaults to 0.0** | Shipping E4 moves NO existing card's rank until opt-in; §7 over-correction guard; raw slope always shown so a regression is visible |
| Granularity | **Per-card term, topic fallback** | Each card's `why_now` reflects its own pain's slope (the differentiator); falls back to run topic when a card term is sparse |

## Architecture

A new isolated channel producing a **number** (demand slope) that reaches only
`score_opportunity` / `ScoreBreakdown` / `_why_now`. Structurally blind to the gate, mirroring
E1's `nli.get_scorer() → None` seam and the pipeline's `scorer=_UNSET` resolution.

```
run_discovery(topic=...)                 pipeline.py
  └─ gather → fuse → verify (GATE)       ── velocity resolved AFTER this line ──
  └─ frame_pm(verified, ..., topic, velocity_provider)   frame.py
        ├─ collect per-card terms → ONE batched measure_batch(terms)   velocity.py
        ├─ score_opportunity(pt, urls, bundle, velocity=signal)        scoring.py
        └─ _why_now(score)  ← leads with velocity when present         frame.py
```

## Components

### 1. NEW module `council/discovery/velocity.py`

```python
@dataclass(frozen=True)
class VelocitySignal:
    term: str
    slope: float        # raw regression slope over the window, ~[-1, 1] (the regression-visibility field)
    normalized: float   # 0-1 mapped for scoring; 0.5 = flat
    source: str         # "pytrends"
    window_days: int
    points: int         # data points used

class VelocityProvider(Protocol):
    def measure_batch(self, terms: list[str]) -> dict[str, VelocitySignal | None]: ...
        # batch is the primitive (pytrends allows up to 5 terms/request); dedupes + caches.
        # returns None per-term on any failure — never raises.

class PytrendsProvider:  # lazy-imports pytrends; None per-term on any failure
    ...

def get_velocity_provider() -> VelocityProvider | None:
    # DISCOVERY_VELOCITY=pytrends -> PytrendsProvider (or None if import fails)
    # unset / anything else       -> None   (no signal; default)
    # exact get_scorer() mirror
```

- **Slope math:** ordinary-least-squares slope of interest-over-time (0-100 Google Trends series),
  normalized by the series mean so it's scale-independent; clamp raw slope to ~[-1, 1].
- **normalized mapping:** `normalized = clamp(0.5 + slope / 2, 0, 1)` — flat → 0.5, strong rise → ~1,
  strong fall → ~0. Constants tunable and named.
- **Caching:** per-term, process-local, so repeated terms in a run cost one lookup.
- **Never raises:** any pytrends/network/parse failure → that term maps to `None`.

### 2. `council/discovery/scoring.py`

- `ScoreBreakdown` gains four fields:
  - `velocity: float` — 0-1 normalized (0.5 neutral / no-signal),
  - `velocity_raw: float` — the raw slope (0.0 when no signal) — the §7 regression-visibility field,
  - `velocity_source: str` — "" when no signal,
  - `velocity_term: str` — the term measured ("" when no signal).
- New tunable constants: `VELOCITY_WEIGHT = 0.0`, `VELOCITY_NEUTRAL = 0.5`.
- `score_opportunity(..., velocity: VelocitySignal | None = None, velocity_weight: float | None = None)`:
  - `value_base` = today's exact formula, **unchanged**.
  - `centered = (velocity.normalized - 0.5) * 2` → 0 when flat/absent.
  - `value = clamp(value_base * (1 + weight * centered))`, where
    `weight = VELOCITY_WEIGHT if velocity_weight is None else velocity_weight` (a `None`-check, **not**
    `or` — an explicit `velocity_weight=0.0` must force the term off, and `0.0` is falsy).
  - **Default weight 0 → `value` byte-identical to pre-E4.** Rising boosts, falling discounts,
    symmetric and clamped to [0, 1].
  - When `velocity is None`: `velocity=NEUTRAL(0.5)`, `velocity_raw=0.0`, `velocity_source=""`,
    `velocity_term=""`.

### 3. `council/discovery/frame.py`

- `frame_pm(verified, fusion_result, bundle, *, today=None, topic="", velocity_provider=None, velocity_weight=None)`:
  - Derive a term per verified card via `_velocity_term(pt, topic)`; **dedupe**; if a provider is
    present, make **one** `measure_batch(terms)` call; else `signals = {}`.
  - Per card: `signal = signals.get(term)`; pass `velocity=signal` into `score_opportunity`.
- `_velocity_term(pt, topic) -> str`: deterministic — the pain `title`, lowercased, trailing
  punctuation stripped, truncated to the first ~5 words (Google Trends terms are short); **fallback
  to `topic`** when that yields an empty string. (The plan may refine the cleaner; the contract is
  "short query string, topic fallback.")
- `_why_now(score)` rewritten:
  - **With a signal** (`score.velocity_source`): lead with velocity —
    rising → `"Demand accelerating — interest slope +0.4 over 90d (pytrends)."`,
    falling → `"Demand cooling — …"`, ~flat → `"Demand flat — …"`; then append the existing
    freshness sentence.
  - **No signal:** unchanged — today's recency note (graceful degradation).

### 4. `council/discovery/pipeline.py`

- `run_discovery(..., velocity_provider=_UNSET)`:
  `active_vp = get_velocity_provider() if velocity_provider is _UNSET else velocity_provider`.
- Pass `topic=topic, velocity_provider=active_vp` into `frame_pm`.
- Session JSON gains:
  - per-card velocity fields (mirrors `ScoreBreakdown`);
  - run-level `velocity_mode` — `"off"` (no provider) / `"pytrends"`;
  - `why_now_coverage` — fraction of cards carrying a real velocity signal (the §9 metric D3 renders).
- The **empty-bundle early-return** path stays as-is here (its `sessions_dir`/persistence gap is
  Item 3's decision) but its session dict gains `velocity_mode` + `why_now_coverage` for schema
  uniformity (both `0`/`"off"`).

## Data flow

`topic` + verified points → per-card terms (deduped) → one batched provider call → per-card
`VelocitySignal | None` → `score_opportunity` (bounded, weight-0 default) → `ScoreBreakdown` (raw +
normalized + source + term) → `_why_now` string → `IdeaCard` → render + session JSON.

## Degradation (all clean)

| Situation | Behavior |
|---|---|
| No provider (default) | `velocity=None` → scores identical to pre-E4; `_why_now` = recency note; `velocity_mode="off"` |
| Provider on, one term rate-limited/fails | that card's signal `None` → neutral, falls back; other cards unaffected |
| `DISCOVERY_VELOCITY=pytrends` but pytrends not installed | `get_velocity_provider()` returns `None`, whole run degrades cleanly (logged) |

## Testing (TDD, all $0 / offline — NEVER calls live pytrends)

- **`tests/test_velocity.py`** (new): slope math on synthetic series (rising / falling / flat);
  normalization bounds ([0,1], flat→0.5); batch dedupe; per-term failure → `None` (a fake pytrends
  that raises); `get_velocity_provider()` env gating (unset → `None`; `pytrends` + missing import →
  `None`). A `FakeProvider` is the test double everywhere downstream.
- **`tests/test_scoring.py`** (extend): `velocity=None` → composite identical to a pre-E4 fixture
  (characterization); `weight=0` identical *even with* a signal; `weight>0` rising → higher, falling
  → lower, both clamped; `velocity_raw`/`velocity_term`/`velocity_source` populated correctly.
- **`tests/test_frame.py`** (extend): `_why_now` for rising / falling / flat / no-signal; term
  derivation + topic fallback; exactly **one** batched provider call per `frame_pm`.
- **`tests/test_pipeline.py`** (extend): `velocity_provider=_UNSET` resolves via
  `get_velocity_provider`; a `FakeProvider` threads end-to-end; session JSON carries per-card fields
  + `velocity_mode` + `why_now_coverage`; **the invariant test** (verify/bundle byte-identical with
  velocity on vs. off + import guard).
- **Regression:** full suite `303 → still passes` on the default (no-provider) path;
  `python3 scripts/validate.py` PASSED.

## Files

- **NEW:** `council/discovery/velocity.py`, `tests/test_velocity.py`
- **EDIT:** `scoring.py`, `frame.py`, `pipeline.py` + extend `tests/test_scoring.py`,
  `tests/test_frame.py`, `tests/test_pipeline.py`
- **OPTIONAL:** `pyproject.toml` — add `pytrends` as an optional extra (never a hard dependency)

## Out of v1 scope (designed-for, deferred)

- **Demand-intent** (autocomplete / People-Also-Ask) — needs SerpApi (metered). `VelocitySignal` /
  provider shape can carry it later (a second provider or an added field).
- **Turning the weight up** — v1 ships `VELOCITY_WEIGHT=0.0` (opt-in). Live tuning of the weight
  against real runs is a follow-up once pytrends signal quality is observed.
- **`sessions_dir` persistence** of the empty-bundle path — Item 3 (D3) owns that decision.

## Success criteria

1. A run with `DISCOVERY_VELOCITY=pytrends` produces cards whose `why_now` carries a real
   velocity slope + the raw term, per-card.
2. The fabrication gate is **provably untouched** (the invariant test passes).
3. No-signal degrades cleanly (default path scores byte-identical to pre-E4).
4. `why_now_coverage` is emitted in the session JSON — the §9 metric becomes measurable (feeds D3).
