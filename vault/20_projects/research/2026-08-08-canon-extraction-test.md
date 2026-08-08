---
title: "Canon-extraction test — the post-ratification condition on D2/D4/D5: PASS"
date: 2026-08-08
project: agent-company-founding
type: feasibility-spike
status: final
tags: [agent-company, canon-extraction, series-bible, evals, D4]
---

# Canon-extraction test — verdict: PASS on all four pre-registered bars

The council's shared dangerous assumption — "canon is a vibe with load-bearing
exceptions; the 32-case spike proves detection when canon is stated, not that
canon is *extractable* from real creators' material" — was the standing
condition on D2/D4/D5. This test answers it. **All four pre-registered bars
pass. D2/D4/D5 stand as ratified; no reopening.**

## Method (protocol frozen before any run — mirrored alongside)

Three creators' real material, extractors fully blind (neutral filenames, no
ground truth, no outside knowledge permitted):

- **A — Pepper&Carrot** (external, CC-BY): 34 pages across episodes 1/2/3 →
  11/16 → 34, spanning a decade of real published evolution, extracted
  **sequentially exactly as the product would** (bible v1 from era 1; each
  later era judged against the prior bible, producing typed evolution events).
- **B — Pencil Test** (Sean's shipped Act 1): 14 sequential production
  frames. Ground truth: the ratified `character.yaml`.
- **C — Grandmaster** (Sean's short in development): 12 design stills,
  shuffled, containing a canonical character transformation, a two-age
  character, and deliberate register experiments. Ground truth:
  `character_seeds.yaml`.

## Results against the bars

| Bar | Threshold | A (P&C) | B (PT) | C (GM) | Verdict |
|---|---|---|---|---|---|
| 1. Fact precision | ≥ 0.80 | ~0.95 | ~0.93 | ~0.90 | **PASS** |
| 2. Identity coverage | ≥ 0.70 | ~0.90 | ~0.95 | ~0.85 | **PASS** |
| 3. Evolution handling | ≥ 2/3 corpora | exemplary | n/a-clean | exemplary | **PASS (3/3)** |
| 4. Cost ceiling | ≤ ~$20 / 50-installment catalog | measured ~47K tokens/episode → ~$1.20 (flash-class) to ~$12 (Sonnet-class) per 50 installments | — | — | **PASS** |

Highlights behind the numbers (full bibles + change reports mirrored in
[2026-08-08-canon-extraction-test/](2026-08-08-canon-extraction-test/)):

- **Precision is hex-level in the register the product will meet most.** The
  Pencil Test extractor's sampled palette landed within a few points of the
  ratified canon (tee `#252e45` vs canon `#243044`; skin `#f0d5bd` vs
  `#F0DFCB`), caught "white soles read as paper," and correctly declared NO
  second character (no hallucinated cast). Its one real error: head-height
  estimate 5.5-6 vs canon 7.0.
- **The hard structural calls all went right.** Grandmaster: wimpy-kid and
  headband-kid unified as one transformed character; young kung-fu warrior
  and elder grandma unified via the frog-button shirt + setting + headband —
  the extractor derived the story's central passed-down-token motif from
  pixels alone, and read the 2-subjects × 3-styles register experiments as a
  deliberate bake-off matrix.
- **Evolution vs drift discrimination worked at production sophistication.**
  P&C stage 2 judged the decade's art maturation intentional (uniform across
  episodes), caught Saffron's real plum→magenta redesign with the exact
  right reasoning ("the gem shade alone would be DRIFT, but it rides the
  deliberate recolor"), and scoped era-34 ceremony attire as occasion wear.
  Stage 3 even **self-audited**: it downgraded stage 2's hair-color
  "evolution" to probable rendering variance when era-3 evidence contradicted
  it.
- **Verification:** orchestrator page-level spot-checks confirmed the
  load-bearing claims verbatim against pixels (Saffron's E03 plum + pink-red
  gem vs E16 magenta + amber gem; dialogue quotes exact). Known-series
  cross-check: every extracted name, school, and plot fact matches the real
  P&C canon.

## The residual failure mode (and why it doesn't reopen anything)

Errors concentrate in **fine attribute values under stylization/lighting**:
glasses shape (round vs canon square), hair color under a golden-hour grade
(black vs canon brown), skin tone (tan vs canon pale), proportion estimates.
Zero errors in character existence, state structure, or evolution logic.
This is exactly the item class D4's **agent-proposes / creator-confirms**
onboarding step exists to catch — the architecture already carries the fix,
which is the same conclusion the drift spike reached for its leg-count
errors. Two spikes, one consistent boundary: **models own structure and
judgment; stated canon facts own fine attributes.**

## Bonus finding — a D4 refinement (adopt; does not reopen)

Stage 3's maintainability note surfaced a real requirement the ratified D4
schema can express but should make explicit policy:

1. **Era-scoped defaults vs timeless facts** — costume/palette defaults carry
   an "as of era N" scope; companions, affiliations, personality, and color-
   scripting are the timeless core that actually holds a series together.
2. **Two-consecutive-era corroboration** before an appearance evolution
   overwrites a default (prevents relitigating cosmetic fields every
   installment — the exact failure A3 caught in A2's hair-color event).
3. **Occasion-wear states** as first-class (a ceremony gown is a state, not a
   redesign).

These map directly onto D4's ratified `applies_from/to` + typed-event fields
— the test validates those fields are load-bearing, not speculative.

## Onboarding economics (second-opinion addition #2, first datapoint)

Measured extraction cost ~47K tokens per 6-page episode on a frontier model.
Projected 50-installment catalog: ~$1.20 at flash-class prices, ~$12 at
Sonnet-class — both under the ~$20/series ceiling, before any batching or
local-model routing. The services-business tripwire does not fire at this
scale. (Method note: measured on Claude subagent token counts; per-price
projection, not a billed figure. Re-measure on the production pipeline.)

## Provenance

Protocol + all proposed bibles + change reports + blind maps:
[2026-08-08-canon-extraction-test/](2026-08-08-canon-extraction-test/).
Condition source: [ratification package](2026-08-08-architecture-ratification-package.md)
(§pre-lock condition) + [second opinion](2026-08-08-architecture-second-opinion.md).
External corpus: Pepper&Carrot by David Revoy, CC-BY 4.0 — used with
attribution, analysis only, no redistribution of pages.
