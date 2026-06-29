---
title: fusion-discovery-council — Step B / PM4+D1 field report
date: 2026-06-29
branch: feat/discovery-pm4-d1-score-card
status: complete (PR open, pending Sean squash-merge)
suite: 195 passed, 1 skipped · validate.py PASSED
spend: $0 (deep-research on subscription; no OpenRouter)
---

# fusion-discovery-council — Step B / PM4+D1 Field Report

**One-line:** Replaced the discovery engine's toy opportunity score (`intensity * (1 + domains)`) and filler card with a research-grounded **`composite = 100 × value × confidence`** (RICE pattern) and a **PRD-grade card** (who · pain-in-their-words · evidence · auditable size · why-now · heuristic proposed-bet), shared identically by both the PM and Substack lenses. Built brainstorm → deep-research → spec → plan → subagent-driven TDD with two-stage review per task. **$0 API spend**, the anti-fabrication VERIFY gate untouched, full council suite **195 passed / 1 skipped**, `validate.py` PASSED.

## 1. Executive summary

This was the 2026-06-28 conversion audit's **#1 felt-value win** (ledger O2: "it tells me a pain exists, not whether it's worth acting on or *why now*"), shipped with no new API cost. The score is computed deterministically from data already in the verified evidence bundle, so it never invents a number and never weakens the gate.

The session's defining move: when Sean said he "wasn't sure what good looks like" for the scoring math, we ran a **deep-research pass** (5 angles → 20 sources → 86 claims → 23 verified, 2 refuted) against the canonical frameworks before locking the formula. That research **changed the architecture** — from a flat 4-way additive sum to RICE-style `value × confidence` — and corrected the single most load-bearing detail (separating model-consensus from independent-source corroboration to kill the single-source illusion).

## 2. What shipped, by commit

- `a79fdf5` / `f2c4415` — **`scoring.py`**: `score_opportunity` + `ScoreBreakdown` (value = weighted importance/reach/recency; confidence = independent-source corroboration + model consensus, floored at 0.5). Review fix: honest `distinct_sources` rename + mutable-default + netloc case-normalization.
- `71e8d3d` / `46d7b2d` — **`bet.py`**: deterministic pain-shape classifier → labeled heuristic proposed-bet + completeness/coverage tests.
- `e982258` — **`frame.py`**: PRD-grade `IdeaCard` + scored `frame_pm` (threads the bundle, sorts by composite).
- `f5e230f` — **`render.py`**: new card layout (verbatim lead quote · auditable Size/Confidence lines · Why-now · proposed bet + fill-in slot).
- `ad133f3` — **`frame_substack.py`**: substack lens adopts the shared `score_opportunity` (DRY); dropped the toy score + `corroboration` field.
- `a458e0e` — **`render_substack.py`**: reads `score.composite` / `score.distinct_domains`.
- `3dc8f29` — **`pipeline.py`**: threads `bundle` + one `today` into both lenses. Full suite green here.
- `8f9cd89` — **docs**: SKILL §2/§6, CHANGELOG, tickets, spec + the research synthesis note.

## 3. How the execution went

Subagent-driven development (fresh implementer per task → independent spec review → independent code-quality review). The discipline paid off concretely — **three implementers stopped and surfaced genuine plan defects rather than papering over them**:

1. **Task 2 (bet):** the test input `"Export is painfully slow and manual"` hit both `export` (integration-gap, higher priority) and `slow/manual` (workflow-friction). Resolution: `export`/`import` are ambiguous workflow verbs, removed from the integration keyword set — a correctness improvement, not just a test fix.
2. **Task 3 (frame):** a current-month `"2026-06"` recency parses to the 1st (~28 days old → recency ≈ 0.52), below the original `_why_now` "Fresh" threshold of 0.6. Resolution: threshold → 0.5 (exactly one half-life ≈ 30 days), the more defensible "within ~a month = fresh" boundary.
3. **Task 1 review (scoring):** the code-quality reviewer caught that `distinct_authors` actually counted `source_name` (a subreddit/handle/publication — a *channel*, not an author), which would render dishonestly as "N authors." Renamed to `distinct_sources`. Honesty is the whole point of the feature, so this mattered.

Each was a one-question decision relayed back to the same implementer, who fixed and re-verified. The plan + spec were updated in lockstep so they stayed the source of truth.

## 4. The research that changed the design

`deep-research` pass (synthesis: [vault/20_projects/research/2026-06-29-opportunity-scoring-frameworks-research.md](../../vault/20_projects/research/2026-06-29-opportunity-scoring-frameworks-research.md)):

- **Validated** the component choice (importance · reach · recency · corroboration) against ODI (`Importance + max(Importance − Satisfaction, 0)`) and RICE (`Reach × Impact × Confidence / Effort`).
- **Validated** log-damped reach — heavy-tailed engagement (top 1% of accounts ≈ 97% of upvotes); Reddit "hot" uses `log10(net votes)`. Our `log1p/log1p(CEIL)` is the canonical fix. We already had it.
- **Corrected → multiplicative confidence:** RICE deliberately *multiplies* Confidence to discount uncertain ideas. We adopted `value × confidence`, so a thin-evidence pain is discounted, not propped up by high importance.
- **Corrected → single-source illusion** (Evan Miller / Wilson lower bound): model-consensus ("4/4 models") is *not* independent evidence — 4 models agreeing about 1 source is still one source. Corroboration is now driven by distinct independent sources; consensus is a separate, lighter confidence signal.
- **Caveat honored:** composite indicators cause "false precision" and the weights are non-neutral (OECD/JRC; Frontiers RMA 2026) — so weights are tunable constants flagged for sensitivity-testing, and the card shows the full breakdown rather than a black-box number.

## 5. Verification evidence

- Full council suite: **195 passed, 1 skipped** (`uv run pytest tests/ -q`), independently re-run by the coordinator.
- `python3 scripts/validate.py`: **PASSED** (53 pre-existing warnings, none from this work).
- **End-to-end smoke render** of a real card (synthetic bundle): score 62/100, pain leads with the verbatim quote, Size line honestly labeled "sources," Confidence line shows the `value × conf = composite` arithmetic, `www.`-normalization dedups domains, "trust-gap" correctly classified a hallucination pain, fill-in slot present.
- Final whole-implementation review (integrated whole): **9/10, "Ship — nothing blocks the PR."** Zero Critical/Important.

## 6. Carry-forward (next steps in the roadmap)

**Deferred follow-up nits from reviews (all non-blocking, safe today):**
- One seam test for the documented source/domain asymmetry (`distinct_domains` from `supporting_urls` vs `engagement_sum`/`distinct_sources` from matched records).
- Cosmetic: test fixtures populate `source_name` with `author{i}` — rename to `src{i}` for clarity.
- Substack ledger surfaces only `distinct_domains`, not the full PM-card breakdown (intentional; brief carries detail).
- `whitespace` is identical across all post angles (v1; a follow-up could map blind spots to angles).

**Remaining Step B (one step per session, per the master ledger):**
- **E3** — MMR near-duplicate pain-point collapse + recency/reach decay (feeds the score).
- **D4** — whitespace-map-as-hero output (compounds with the agent backfill).
- **D2** — receipts UI (inline per-claim verification status).

**Then Step C gates** (cheap, run before the builds they gate): panel-vs-single-model (`#4`, costs real OpenRouter $ — surface estimate + check the daily cap first) and PM3 longitudinal-signal. Then **Step D** (E1 entailment-gate cost-model decision-with-Sean — do NOT default to paid per-claim; lean local NLI).

## 7. Notes worth keeping

- **Research-before-locking-the-formula** was the highest-leverage decision this session. The weights weren't arbitrary in the end — they're grounded, and the one architectural change (multiplicative confidence) is the property the final review specifically called out as airtight.
- **The honesty rename** (`distinct_sources`) and the **labeled-heuristic bet** are the two places where "the card must not lie" showed up in code review. Both were caught by reviewers, not by the implementers — evidence the two-stage review earns its cost.
- **$0 enforced by construction:** every signal reads the in-memory bundle; there is no network call anywhere in the new code. The deep-research pass ran on the Anthropic subscription.
