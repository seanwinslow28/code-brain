# E2 — Fix FUSE panel self-preference via judge-family separation (design)

**Date:** 2026-06-30
**Feature:** fusion-discovery-council Step D / E2
**Branch:** `feat/discovery-e2-judge-debias`
**Status:** design — approved in brainstorm, pending spec review
**Research:** [`vault/20_projects/research/2026-06-30-llm-judge-self-preference-debias-research.md`](../../../vault/20_projects/research/2026-06-30-llm-judge-self-preference-debias-research.md)

## Problem

The Step-C panel-vs-single-model gate proved the 4-model Fusion panel beats a single strong model
(→ E2 = GO) but flagged a plausible **self-preference confound**: the FUSE judge graded a panel that
included its own model. In code (`tiers.py` + `fusion.py::_build_body`, where `tier.judge` is the
outer `model` and `tier.panel` is `fusion.analysis_models`), the judge is a **literal member of its
own panel in all three tiers**:

| Tier | Judge (today) | Panel (today) | Judge ∈ panel? |
|---|---|---|---|
| `quick` | `~google/gemini-pro-latest` | `~google/gemini-pro-latest`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro` | **yes** |
| `standard` | `anthropic/claude-opus-4.7` | `anthropic/claude-opus-4.7`, `openai/gpt-5.5`, `~google/gemini-pro-latest`, `x-ai/grok-4.3` | **yes** |
| `deep` | `anthropic/claude-opus-4.7` | the standard panel + `deepseek/deepseek-v4-pro`, `mistralai/mistral-medium-3-5` | **yes** |

This is the strongest form of the risk — not just same *family* but the same *model ID* judging its
own output.

## Evidence → decision (why this shape)

From the deep-research pass (19 confirmed findings, 4 primary papers; full note linked above):

- **Family separation is the single highest-leverage, lowest-cost lever** and is the only fix that
  helps under *both* unsettled mechanism accounts of self-preference — recognition (Panickssery 2024)
  and perplexity/familiarity (Wataoka 2024).
- **Authorship-blinding alone is insufficient** (self-preference persists under blinding via implicit
  style recognition) **and unreachable** here — `openrouter:fusion` internalizes the panel and never
  exposes attribution to us to strip (FUSION_SCHEMA §3).
- **A full order-randomized / authorship-blind pipeline (option b) is rejected**: its target (position
  bias) is driven by *near-tie pairwise quality gaps*, which are largely absent in a synthesis/clustering
  judge; and order-swap is *not* reliably beneficial — it hurt models 4–11pp on adversarial data by
  discarding decisive verdicts.

## Goal — one enforceable invariant

> **For every tier, the judge's model family ∉ the set of panel model families.**

`family(model_id)` = strip a leading `~` (OpenRouter floating-alias marker), then take the segment
before the first `/`. E.g. `~google/gemini-pro-latest` → `google`; `anthropic/claude-opus-4.7` →
`anthropic`.

## Design — `tiers.py` changes only

Shape **(a1) "keep the strong judge, drop its family from the panel"** for standard/deep; for `quick`
(whose panel already has no anthropic) keep the 3-model panel and swap the judge to a disjoint family.

| Tier | Judge (after) | Panel (after) | Families: judge vs panel |
|---|---|---|---|
| `quick` | **`openai/gpt-5.5`** *(swap from gemini)* | unchanged: `~google/gemini-pro-latest`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro` | `openai` ∉ {google, x-ai, deepseek} ✓ |
| `standard` | `anthropic/claude-opus-4.7` *(unchanged)* | **drop opus** → `openai/gpt-5.5`, `~google/gemini-pro-latest`, `x-ai/grok-4.3` | `anthropic` ∉ {openai, google, x-ai} ✓ |
| `deep` | `anthropic/claude-opus-4.7` *(unchanged)* | **drop opus** → `openai/gpt-5.5`, `~google/gemini-pro-latest`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro`, `mistralai/mistral-medium-3-5` | `anthropic` ∉ {openai, google, x-ai, deepseek, mistralai} ✓ |

Notes:
- `_STANDARD_PANEL` currently leads with `anthropic/claude-opus-4.7`. After the change it becomes the
  3-vendor `(openai/gpt-5.5, ~google/gemini-pro-latest, x-ai/grok-4.3)`, and `deep` extends it with
  `deepseek` + `mistral` (so deep stays a 5-vendor panel). Standard drops from 4→3 panelists, deep 6→5
  — both remain fully cross-vendor relative to the Opus judge. Step C validated *that a panel beats
  single-model*, not a specific N; a 3-/5-vendor panel is still a panel.
- **quick judge = `openai/gpt-5.5`.** The judge is the *outer* model and makes **no web-tool calls**
  (only panelists do; per FUSION_SCHEMA the web-call count `panel × max_tool_calls` dominates run cost),
  so the swap barely moves quick's spend. **Locked: `openai/gpt-5.5`** (judge strength, validated ID).
  Documented fallback if quick cost ever bites the $0.50 cap: `mistralai/mistral-medium-3-5` (also
  disjoint + validated) — a one-line change, not a re-design.
- **All model IDs stay within the FUSION_SCHEMA-validated set** (`anthropic/claude-opus-4.7`,
  `openai/gpt-5.5`, `~google/gemini-pro-latest`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro`,
  `mistralai/mistral-medium-3-5`) — no new IDs, no 400 risk. The invalid `google/gemini-pro-latest`
  (no tilde) and dotted `mistralai/mistral-medium-3.5` must not be reintroduced.

## Non-goals (explicit)

- **No `openrouter:fusion` replacement / panel-then-blind-judge pipeline** (option b) — rejected by research.
- **No order randomization / swap-and-agree** — wrong task shape; can backfire.
- **No authorship-blinding plumbing** — insufficient + unreachable through the fusion black box.
- **No paid verification re-run** — research + Step C cover it; the invariant test is the regression guard.
- **No PoLL / multi-judge jury** — future direction, out of scope for E2.

## Testing (TDD, hermetic, $0 — no live FUSE)

New `tests/discovery/test_tiers.py` coverage:
1. **Invariant (the regression guard):** for every tier, `family(judge) not in {family(m) for m in panel}`.
   This is the load-bearing test — it fails today and must pass after the change, and it permanently
   blocks reintroducing the confound.
2. **Exact post-change membership per tier:** quick judge `openai/gpt-5.5` + unchanged 3-model panel;
   standard judge `anthropic/claude-opus-4.7` + 3-vendor panel with **no** anthropic; deep judge
   `anthropic/claude-opus-4.7` + 5-vendor panel with **no** anthropic but **with** deepseek + mistral.
3. **Validated-ID guard:** every panel + judge ID across all tiers ∈ the FUSION_SCHEMA-validated set.
4. **A small `family()` helper unit test** (tilde stripping, `/` split).

**Update existing tests that encode the old (confounded) design** — these legitimately change because
the design changed (not to make a contorted assertion pass):
- `test_standard_panel_is_four_frontier_vendors` → rename/rewrite to the new 3-vendor anthropic-free panel
  (judge still Opus). This test currently asserts the confound; it must now assert the fix.
- `test_deep_adds_two_more_lineages_and_confirms_cost` → still valid (deepseek + mistral still in deep
  panel; cost unchanged) but verify it doesn't assume opus ∈ panel.
- `test_sonar_never_in_panel`, tier-gating, blind-spot-cap, `get_tier` tests — unaffected.

`_family()` helper: decide placement during planning — likely a small private function in `tiers.py`
(used by both the config-construction sanity and the tests) so production and tests share one definition.

Run: `cd tools/llm-council && uv run pytest tests/ -q` (currently 263 passed / 1 skipped) +
`python3 scripts/validate.py` (repo root). Watch each new test fail before implementing.

## Docs

- **SKILL.md** (`.claude/skills/fusion-discovery-council/SKILL.md`, §6 gate / §2 FUSE): note the
  judge-disjointness invariant — the FUSE judge is deliberately a different model family from every
  panelist to avoid self-preference; cite the research note.
- **CHANGELOG.md**: E2 entry.

## Vault / git discipline

- The research note lives under `vault/20_projects/research/` and is **left unstaged** (Sean owns vault
  commits this cycle). The E2 branch contains **zero vault changes**.
- Branch → PR into `main` → Sean squash-merges. Commit trailer + PR footer per conventions. Final
  whole-branch adversarial review (Code Reviewer, most-capable model) before PR.

## Rollback

Single-file config change; revert `tiers.py` (+ the two doc edits) to restore prior behavior. No data
migration, no schema change, no cost-path change.
