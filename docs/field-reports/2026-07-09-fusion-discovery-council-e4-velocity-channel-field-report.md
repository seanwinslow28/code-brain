# Field Report — fusion-discovery-council E4 velocity scoring channel (Item 2)

**Date:** 2026-07-09
**Branch:** `feat/discovery-e4-velocity-channel` (off `main` @ e3ced2e)
**Campaign:** Phase 2 "everything buildable now" — **Item 2 of 4** (the flagship build)
**Method:** brainstorming → spec → writing-plans → subagent-driven-development (fresh subagent per task, two-stage review, final whole-branch review on Opus)
**Tests:** 303 → **326 passed, 1 skipped** (+23). `python3 scripts/validate.py` PASSED (53 pre-existing warnings, none in changed files).
**Cost:** $0 (no paid runs; pytrends is an optional, offline-tested dependency).

## What shipped

A **velocity scoring channel** giving each discovery idea card a real "why now" — a demand *slope*, not just a freshness note off one evidence date. It is the "why now" layer competitors sell separately (Exploding Topics velocity), fused into the already-gated card.

### The moat (load-bearing invariant), enforced structurally
Velocity is a **SCORE signal only, never gate-evidence.** Verified three ways, independent of any single test:
- `council/discovery/velocity.py` imports nothing from `verify.py` — a source-level import-guard test locks it against drift.
- In `pipeline.py`, the provider is resolved (line ~159) strictly **after** `verify_pain_points` / `dedup_verified` / `citation_metrics` — downstream of the gate by construction.
- The signal reaches only `score_opportunity(velocity=…)`; `frame_pm` builds `evidence_urls` from `v.supporting_urls` and `quotes` from `pt.quotes`, never from the signal. Grep confirmed `verify`/`evidence`/`dedup`/`fusion` have zero coupling to velocity.
- `test_invariant_velocity_cannot_perturb_the_gate` runs the pipeline with velocity **active** (weight monkeypatched to 0.3 — a score moves 48→60) and proves the gate metrics (verified/dropped/citation precision+recall) stay **byte-identical**, with `on.markdown != off.markdown` to prove velocity genuinely did something.

### Design decisions (locked in brainstorming with Sean)
- **Stub default + pytrends optional.** `get_velocity_provider()` returns `None` unless `DISCOVERY_VELOCITY=pytrends` and pytrends is installed — the exact `nli.get_scorer()→None` mirror. Demand-intent (autocomplete/PAA) deferred (needs SerpApi); the `VelocitySignal`/provider shape can carry it later. pytrends reached only through an injectable `_pytrends_fetch` seam, so every test is offline.
- **Weight defaults to 0.0.** A bounded, tunable velocity nudge folded outside the normalized `VALUE_WEIGHTS`; `centered = (normalized − VELOCITY_NEUTRAL)*2` is 0 when flat/absent, so shipping E4 leaves every existing card's composite **byte-identical** until Sean raises the weight. The raw slope (`velocity_raw`) is always reported for regression visibility (research §7's over-correction guard).
- **Per-card term, topic fallback.** Each card's `why_now` reflects its own pain's slope; the provider batches (pytrends allows 5 terms/request) + caches.
- Session JSON gains run-level `velocity_mode` + `why_now_coverage` (the §9 metric D3/Item 3 will render).

### Files
- **NEW:** `council/discovery/velocity.py`, `tests/discovery/test_velocity.py`
- **EDIT:** `scoring.py` (+4 `ScoreBreakdown` fields, bounded fold), `frame.py` (per-card term, batched measure, velocity-aware `_why_now`), `pipeline.py` (resolution + session metrics), their tests, `pyproject.toml` (optional `velocity` extra), `uv.lock` (pytrends transitive lock).

## Review findings caught + fixed (the process earned its keep twice)
1. **Vacuous guard test (Task 3, Important):** `test_explicit_zero_weight_forces_term_off_not_the_constant` passed identically under the correct `None`-check AND a buggy `or` (both `VELOCITY_WEIGHT` and the explicit value were 0.0). Hardened via monkeypatch so it now **fails under `or` (34.0 vs 22.7), passes under the None-check.**
2. **Under-powered moat test (final review, Minor→fixed):** the invariant test ran velocity inert (weight 0), so it couldn't distinguish "velocity re-ranked but didn't touch the gate" from "velocity did nothing." Strengthened to run velocity active while proving gate-identity — the test now *demonstrates* the separation rather than coexisting with it.
Plus 3 hardenings: `scoring` centers on `VELOCITY_NEUTRAL` (not a hardcoded 0.5); `measure_batch` isinstance-dict guard (never-raises airtight against a misbehaving injected fetch); a >5-term multi-chunk coverage test.

## Notes / carried forward
- **Follow-up ticket owed:** expose `velocity_weight` via config/env so turning the channel up doesn't require editing the `VELOCITY_WEIGHT` constant in `scoring.py`. (Logged in `vault/00_inbox/tickets.md`.)
- **Deliberate spec deviation:** session JSON carries run-level `velocity_mode` + `why_now_coverage` only, not a per-card velocity array (cards aren't serialized today; that array is Item 3/D3's call). Per-card velocity remains visible in `ScoreBreakdown` + the rendered `why_now`.
- **Demand-intent + weight-tuning** are the natural next increments once pytrends signal quality is observed on real runs.

## Verification
- `cd tools/llm-council && uv run pytest tests/ -q` → 326 passed, 1 skipped.
- `python3 scripts/validate.py` → PASSED (53 pre-existing warnings, none in changed files).
