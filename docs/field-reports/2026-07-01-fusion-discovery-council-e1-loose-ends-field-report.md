# Field Report — fusion-discovery-council E1 loose ends (Item 1, Phase 2)

**Date:** 2026-07-01
**Branch:** `feat/discovery-e1-loose-ends`
**Campaign:** Phase 2 "everything buildable now" — Item 1 of 4 (the scoped E1 cleanup pass)
**Method:** TDD-direct (item was pre-scoped; no brainstorming needed per the campaign prompt)
**Tests:** 297 → **303 passed, 1 skipped** (+6 new). `python3 scripts/validate.py` PASSED.

## What shipped

### 1a — ALCE citation-precision semantics for phantom (unfetched) URLs — DECISION + code
Decided **with Sean: option (c)** — a cited URL never fetched into the evidence bundle is
*unverifiable*, so it counts in the precision **denominator** but can never be a numerator hit
(a hard miss). This is the strongest "verified, not hallucinated" semantics and, critically, it
**kills the edge-case bug** the final E1 review flagged: in a multi-quote point that is verified
(one quote supported) but not all-claims-supported, the old redundancy test counted the phantom
URL as "load-bearing" and inflated precision to **1.0**. New behavior returns **0.5**.

- `verify.py::citation_metrics` now skips non-bundle URLs from the contributing-count and evaluates
  redundancy only among fetched URLs (`bundle_urls`). Redundancy math for real citations is unchanged.
- New decisive test `test_phantom_cited_url_is_a_hard_precision_miss` reproduces the exact
  `1.0 → 0.5` inflation edge case (watched it fail on `main` before the fix).
- Added `test_entailment_at_exact_tau_boundary_accepts` — a τ=0.5 boundary characterization test
  pinning `>=` vs `>` (previously only 0.92/0.10 were tested, leaving the boundary unpinned).

### 1b — E1 plan-doc bug (docs only)
`docs/superpowers/plans/2026-06-30-discovery-e1-entailment-gate.md` Task 3 Step 3 example wrote
`urls = v.supporting_urls` (yields precision 1.0, contradicting its own asserted 0.5 test). Corrected
to `v.point.urls` **and** updated the example + the prose "Definitions" block to reflect the shipped
option-(c) phantom semantics, so a future re-run can't reintroduce the wrong denominator.

### 1c — Code hygiene
- **`_CLAIM_SENT` over-split (TDD):** the old `[^.!?]+[.!?]|[^.!?]+$` split on *every* dot, so
  "Mr. Smith" → `["Mr.", "Smith…"]` and "v3.0" → `["v3.", "0"]`, producing spurious 1-3 char
  fragments that each had to be independently entailed (AND) → false rejects. Replaced with a
  `_CLAIM_BOUNDARY` regex: a boundary is `[.!?]+` followed by whitespace/end (so decimals/versions
  never split) and not preceded by a common abbreviation (`Mr`/`Dr`/`e.g`/…). Trailing punctuation
  is now stripped too, which also fixes a latent substring-match miss (a quote ending in "." failing
  to match a doc without the period). 3 new tests.
- **`install_nli_model.sh`:** dropped the `|| true` after the `hf download` — failures now surface
  (the file-existence check at step 2 and the verify at step 4 still guard idempotency).
- **`test_nli.py`:** removed the unused `import importlib`, hoisted `import pytest` to the top, and
  deleted the duplicated mid-file `import pytest` / `import ... nli`.
- **Empty-bundle session JSON schema uniformity:** the early-return empty-bundle session dict now
  carries `verify_mode="substring-only"` + `citation_precision=None` + `citation_recall=None`,
  mirroring the full path. 1 new test.

## Notes / carried forward
- The empty-bundle early-return path still does **not** write to `sessions_dir` — that's the D3
  sparse-session-store concern (Item 3), out of scope here. Left as-is; D3 will decide whether to
  wire `sessions_dir` on by default.
- No paid runs. $0 this item.

## Verification
- `cd tools/llm-council && uv run pytest tests/ -q` → 303 passed, 1 skipped.
- `python3 scripts/validate.py` → PASSED (53 pre-existing warnings, none in changed files).
