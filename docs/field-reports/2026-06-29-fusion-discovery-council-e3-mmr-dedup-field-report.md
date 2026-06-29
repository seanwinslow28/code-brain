---
title: Field report — fusion-discovery-council E3 (near-duplicate dedup + MMR gap ranking)
date: 2026-06-29
branch: feat/discovery-e3-mmr-dedup
roadmap_item: E3 (Step B), closing the D4↔E3 coupling
spec: docs/superpowers/specs/2026-06-29-discovery-e3-mmr-dedup-design.md
plan: docs/superpowers/plans/2026-06-29-discovery-e3-mmr-dedup.md
research: vault/20_projects/research/2026-06-29-mmr-dedup-similarity-research.md
---

# E3 — Near-duplicate pain-point dedup + MMR whitespace-gap ranking

## What shipped

A new `council/discovery/dedup.py` ($0, deterministic, stdlib-only) with a **shared lexical
token-Jaccard similarity** driving two distinct algorithms:

1. **`dedup_verified`** — collapses near-duplicate gate-survived pain points before FRAME via
   **bounded merge-to-canonical** (each candidate compares only to cluster *seeds* — no transitive
   closure, so the A=B,B=C⇒A=C over-merge trap is structurally impossible). The representative is the
   strongest-evidence point (most distinct domains → intensity → quote count → stable index); evidence
   is unioned honestly (URLs/quotes), and corroboration stays keyed on **distinct domains** in
   `scoring.py`, so a same-domain/syndicated merge provably cannot inflate confidence.
2. **`rank_gaps`** — MMR (Carbonell & Goldstein 1998, λ=0.3) ranks D4's whitespace gaps
   **most-distinct-first** (`blindspot(gap) = 1 − max_sim(gap, surfaced pains)`) and drops near-duplicate
   gaps in one pass.

Wired into `pipeline.py` immediately after VERIFY (gate untouched) and before FRAME; both lenses and
the session see the deduped pains + ranked gaps via a single in-place reorder of `fr.blind_spots`. Both
renderers show a `Merged N near-duplicate pain point(s)` note. D4's hero wording now says gaps are
"ranked most-distinct-first" with an explicit "*this is an ordering signal, not a severity or confidence
score*" honesty note — the absence-of-evidence / investigate-only guardrail is preserved verbatim. Two
PM4 carry-forward test nits closed in the same PR.

**9 commits** (7 plan tasks + a hardening commit + spec/plan docs), **233 passed / 1 skipped** (was 212),
repo validator passes.

## The defining move (third time): research before locking the shape

Per the standing practice, a **$0 deep-research pass** preceded the design — and it reshaped the build,
not just confirmed it:

1. **It split one algorithm into two.** The research's open-question #3 established that for *pure dedup
   with no query*, MMR is the wrong tool — a direct similarity-threshold + transitivity-guarded
   clustering is right; MMR belongs on the gap *selection* problem. So the prompt's "same machinery"
   correctly resolved to a **shared similarity function used by two different algorithms**
   (threshold-clustering for dedup, MMR for gaps) — cleaner and more defensible than forcing MMR onto
   dedup, which is what I'd likely have done from first principles.
2. **It stopped me from copying the wrong threshold.** The headline caveat: the standard Jaccard
   0.7–0.9 numbers are calibrated for *long documents*; short 1–2 sentence pain points have few tokens,
   so a single token swap moves the score a lot and no source gives a short-text number. → threshold
   became a conservative tunable (~0.5), biased to under-merge, not a borrowed literature constant.
3. **It named the over-merge trap and its guard.** Transitive closure (Oracle's Jones/James/Jamos) +
   the "start high, bias under-merge" posture (Neo4j / record-linkage) → bounded merge-to-canonical.
   The "connected-components is the guard" claim was *refuted* in verify, so I deliberately did NOT
   lean on it.
4. **It made the honest-merge rule fall out for free.** Fellegi-Sunter's independence caveat (syndicated
   sources double-count) → union URLs but keep corroboration keyed on distinct domains, which
   `scoring.py` already did. Zero new corroboration code.

Unlike the D4 pass, the harness **completed cleanly this time** (103 agents, ~3.8M tokens, 22/25 claims
confirmed, 3 refuted) — no rate-limit abort, so no salvage needed. One $0 pass, four load-bearing
decisions.

## Process notes

- **Subagent-driven execution, 7 tasks + final review.** Fresh implementer per task (cheapest tier for
  pure-transcription tasks, standard for the integration/logic tasks), spec+quality review after each.
  Every per-task review came back Spec ✅ / Approved with only Minor notes. The discipline mostly served
  as a ratchet here because the plan carried complete code — the real value showed up at the *final*
  whole-branch review.
- **The Task-1 "unused imports" finding was plan-mandated.** I'd put the module's full import header in
  Task 1, so `dataclass`/`urlparse`/`VerifiedPainPoint` were unused at the Task-1 commit but consumed at
  Task 2. Adjudicated as resolved-by-Task-2 (the reviewer's import-time-breakage risk was disproven —
  suite green, `verify.py` exists) rather than churning a fix. Worth remembering: writing a whole
  module's imports in the first sub-task guarantees a transient unused-import flag.
- **I strengthened one test at dispatch time.** The plan's transitivity test (`alpha/export/sync…`)
  didn't actually construct the A~B, B~C, A≁C scenario (the would-be bridge pair was already below
  threshold), so it would have passed even without a guard. Replaced it with `export sync feature` /
  `sync feature billing` / `feature billing invoice` (B bridges A and C only if you compare against
  non-seeds), asserting exactly 2 survivors — a real distinguishing test.
- **The final review (Opus, 9/10, Ship) earned its keep.** It confirmed all six invariants on the real
  call path and flagged that the highest-stakes one — merge can't inflate corroboration — rested on two
  *separate* unit tests rather than one end-to-end proof. I folded in one hardening commit: an
  end-to-end same-domain-merge test asserting the rendered card still shows `1 independent domain(s)`,
  plus a defensive `best_sim = -1.0` init (correct even if `threshold` were ever set to 0). Skipped the
  reviewer's blindspot-precompute micro-opt as YAGNI (single-digit gap lists).

## The D4↔E3 coupling, now closed

D4 shipped gaps in panel order with an explicit "no rank claim" caveat *because* there was no similarity
signal over gaps. E3's `rank_gaps` is that signal: gaps are now ordered worst-first (most-distinct-from-
what-the-run-surfaced) and near-duplicate gaps are dropped. The honesty framing held — "most-distinct-
first" is explicitly an ordering signal, **not** a severity score, so a blind spot still carries no
fabricated confidence.

## Vault hygiene

Per the active cycle (Sean on the MBP, Obsidian-Git not running, mid-audit), this branch contains
**zero vault changes** — verified: the branch diff is code + `docs/` + SKILL.md + CHANGELOG only. The
research note (`vault/20_projects/research/2026-06-29-mmr-dedup-similarity-research.md`) is written but
left **unstaged** for Sean, and the E3-done ticket update is left for him.

## Carry-forward (next PR)

- **Remaining Step B: D2 — receipts UI** (verification status inline per card: ✓ verified ·
  corroborated-K-domains · recency badge). Now that corroboration counts are honest (dedup keyed on
  distinct domains), the receipts will mean what they say.
- Then **Step C gates**: panel-vs-single-model (costs real OpenRouter $ — surface estimate + check daily
  cap first) and PM3 longitudinal-signal (E3's dedup is the groundwork for a stable pain key).
- Minor, non-blocking (from the final review): `rank_gaps` recomputes `blindspot` each outer iteration
  (O(gaps²·refs)); a precompute would tidy it but the lists are tiny — not worth it unless gap counts
  grow.
