# Field report — fusion-discovery-council E1 entailment-gate BUILD

- **Date:** 2026-07-01
- **Branch:** `feat/discovery-e1-entailment-gate` (off `main` @ `0b0366e`)
- **Method:** superpowers:subagent-driven-development (fresh implementer + task reviewer per task, Opus whole-branch review at the end)
- **Cost:** $0 recurring — local in-process NLI. Model download (~173 MB, one-time, $0) run locally to confirm the label index. No paid discovery runs.

## What shipped

E1 upgrades the shared anti-fabrication chokepoint `verify.py::quote_supported_at_url` from plain
substring containment to a cascade: **substring pre-filter → atomic-claim sentence split → optional
in-process NLI entailment** (injected scorer). Plus ALCE-style citation precision/recall reporting, a
real ONNX NLI adapter with graceful degradation, pipeline/session-JSON wiring, an optional dependency
extra, a model setup script, a degraded-mode render note, and docs.

6 tasks, all TDD, each reviewed and approved (Spec ✅ + Quality Approved):

| Task | Commit | Result |
|------|--------|--------|
| 1 — cascade + atomic-claim split | `cb7663f` | 275 passed/1 skip |
| 2 — thread scorer through VERIFY | `668db6d` | 276 passed/1 skip |
| 3 — ALCE citation precision/recall | `69e10d0` | 279 passed/1 skip |
| 4 — real ONNX NLI adapter (`nli.py`) | `cfec7ca` | 282 passed/2 skip |
| 5 — pipeline + session-JSON wiring | `a9f04ff` | 284 passed/2 skip, validator PASS |
| 6 — deps + setup script + render note + docs | `cc8cd90`, `c69f15f` | 287 passed/1 skip, validator PASS |

Final suite: **287 passed, 1 skipped** (the 1 skip is an unrelated `INTEGRATION=1` live-API test; the
E1 real-model integration test now RUNS + passes because the model is installed locally). Validator PASS.
Baseline before E1 was 268 passed/1 skipped; +19 new tests.

## The four load-bearing invariants — all CONFIRMED (final Opus review, under trace)

1. **Recall-safety** — the substring pre-filter only ever ADDs an accept, never rejects. Enforced
   structurally in `_claim_supported` (bare `if substring: return True` with no `else`), so a substring
   hit cannot cause a rejection and a substring miss always falls through to NLI when a scorer exists.
   Locked by `test_substring_never_rejects_even_if_scorer_would`.
2. **Graceful degradation** — `nli.py::get_scorer()` wraps the entire load path in `try/except Exception`,
   caches `None`, never raises. With no model/deps the gate behaves EXACTLY as pre-E1 (substring-only)
   with a one-time warning. Existing verify/backfill tests unchanged and green.
3. **Label-index correctness** — `_ENTAILMENT_IDX = 1` CONFIRMED against the live model card
   `id2label = {0:contradiction, 1:entailment, 2:neutral}` + real inference (paraphrase 0.993 vs
   contradiction 0.0002). This was the single silent-inversion risk; it is retired with hard evidence.
4. **No deformed tests** — the shared chokepoint's other consumer (Stage 5 BACKFILL) passes `scorer=None`
   by default and is provably unchanged; no pre-existing test was weakened.

## Decisions & deviations worth Sean's eye

- **Task 3 deviation (correct, reviewer-confirmed):** the plan's Step 3 example code used
  `v.supporting_urls` for the precision denominator, which yields precision 1.0 — contradicting its own
  asserted 0.5 test (because `supporting_urls` is already pre-filtered to independently-verified urls).
  The implementer switched to `v.point.urls` (all cited urls), matching the design spec's prose
  "each (point, cited_url)". Hand-traced and focused-pytest-confirmed. **The plan doc itself has the
  bug — ticketed for correction.**
- **Final review Issue 1 (Important, metric-only) → SHIP AS-IS per Sean (2026-07-01):** the ALCE
  precision denominator counts unfetched/phantom cited URLs. Two reviews split on whether this is
  correct; the controller traced the final reviewer's "inflates to 1.0" claim as holding only in a
  narrow multi-quote edge case (common case: phantoms LOWER precision). This is a REPORTED-METRIC-ONLY
  semantics question — the anti-fabrication gate is unaffected. Sean's call: ship, settle the semantics
  deliberately with a fixture later. Ticketed with options (a) keep, (b) exclude non-bundle urls,
  (c) count as hard precision misses.

## Follow-ups filed (`vault/00_inbox/tickets.md`)

- E1: settle ALCE precision semantics for phantom URLs (+ add a τ=0.5 boundary fixture).
- E1: correct the plan-doc Step 3 example bug; minor code-hygiene (`_CLAIM_SENT` abbreviation splitting,
  `install_nli_model.sh` `|| true` swallowing the hf error, `test_nli.py` unused/dup imports,
  empty-bundle session-key uniformity).

## Next (subsequent sessions)

PM3 t1 re-run + verdict (~2026-07-21, ticketed) → PM3 pain-taxonomy persistence. Then PM2/E4
demand-intent scoring; D3 discovery dashboard; Step F buyer-conversation test (Phase 3, gated).
Master plan: `vault/20_projects/research/2026-06-27-fusion-discovery-council-improvement-idea-ledger.md`.
