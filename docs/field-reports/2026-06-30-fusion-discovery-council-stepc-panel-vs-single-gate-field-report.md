# Field Report — fusion-discovery-council Step C: panel-vs-single-model gate

**Date:** 2026-06-30
**Branch:** `feat/discovery-stepc-panel-vs-single-gate`
**Roadmap:** Step C `GATE →` panel-vs-single-model (red-team #4). Closes the question gating **E2** (panel self-preference fix).

## Verdict (one line)

**The 4-model Fusion panel beats a single strong model — the panel earns its cost. E2 is GO.** Blind variance-council rating chose the panel on all four criteria (3 of 4 models overall), at only an ~8% cost premium.

## What shipped

A controlled dual-fuse experiment harness (`tools/llm-council/experiments/`), plus a reusable evidence serializer:

- **`EvidenceBundle.to_dict/from_dict`** (`council/discovery/evidence.py`) — freezes a gathered bundle to disk so a run is reproducible and re-fusable for $0. Also the snapshot groundwork PM3 (longitudinal) will need.
- **`experiments/blind_rating.py`** — renders two pain-point sets as anonymized, sha256-deterministically-shuffled markdown + a separate key. The rater never sees which arm is which.
- **`experiments/panel_vs_single_core.py`** — gather once → fuse the same bundle through the full panel (arm A) vs a single model (arm B), same judge in both, record spend per arm (cost-integrity symmetric across both failure paths).
- **`experiments/panel_vs_single.py`** — `click` CLI: discovery-daily-cap preflight, cost-confirm gate (`--yes`), writes 5 artifacts.

**Tests:** 263 passed / 1 skipped (was 249 baseline; +14). Validator PASS. All hermetic — the build did zero paid calls.

## The experiment

- **Control:** same 46-record evidence bundle, same judge (`claude-opus-4.7`), same standard-tier knobs; only `analysis_models` varied — arm A = `(opus, gpt-5.5, gemini-pro, grok-4.3)`, arm B = `(opus,)`.
- **Topic:** the "AI is a slot machine / stopped chasing prompts for a repeatable system" topic (representative, on-brand, n=1).
- **Blind rating:** variance council (Claude, GPT-5.4-mini, DeepSeek, Mistral; sonnet chairman) judged the two anonymized sets on signal density, evidence grounding, distinctness, actionability.

## Result

| Arm | Pain points | Cost | Blind result |
|---|---|---|---|
| A — full panel | 4 (orthogonal) | $1.34 | **Winner, all 4 criteria** |
| B — opus alone | 5 (incl. 1 weak) | $1.24 | Lost on distinctness + grounding |

Opus-alone produced *more* points but split the core workflow complaint into two overlapping buckets (nondeterminism / "can't build a workflow") and added a 5th point (compulsive "lever-pulling") evidenced only by Reddit memes — diluting signal density and distinctness. The panel's four points were genuinely orthogonal (baseline nondeterminism · provider-driven model churn · missing determinism tooling · craft-erosion identity cost), each mapping to a discrete product opportunity.

**Confound checked:** the panel arm's judge and one rater are Anthropic-family, so an Anthropic-affinity artifact was plausible. But two non-Anthropic raters (DeepSeek, Mistral) backed the panel; only GPT-5.4-mini dissented. Cross-lineage agreement mitigates the confound.

## Honest limits

- **n=1.** One topic. The verdict was clear (panel swept all four criteria), so a tie-break second topic wasn't needed — but generalization to other topic shapes is unproven. Re-run on a second topic if E2's design hinges on the margin.
- **Cost premium is small (~8%).** The panel "earning its cost" is true but the bar was low; if the single model had tied, the panel would have been hard to justify. It didn't tie.

## Spend

Dual-fuse $2.5863 + blind rating $0.1834 = **$2.77** (discovery cap: $10/day, $50/month; pre-run today $0, month-to-date $24.82). Recorded under `tool="discovery"`, `tag="discovery-experiment"` / `panel-vs-single`.

## Process notes

- Research-before-locking paid off again at the meta level: the spec caught that old session bundles **don't persist evidence**, so "re-FUSE an existing bundle" (as the continuation prompt assumed) was impossible — pivoting to gather-once-then-dual-fuse gave a *cleaner* controlled comparison anyway.
- One flaky fix-wave subagent emitted a misleading "completed/deferred" message while still running asynchronously (181s), racing the controller's edits. Recovered by verifying git/test ground truth rather than trusting the summary; the agent's commit (`0908442`) was correct and complete. Lesson: verify subagent claims against git + test output, especially on slow async runs.

## Artifacts (audit trail)

`tools/llm-council/experiments/runs/panel-vs-single-20260630-115751/` (force-added; `experiments/runs/` is otherwise gitignored): `bundle.json`, `arm-A.json`, `arm-B.json`, `blind-rating.md`, `key.json`, `council-verdict.md`.

## In Sean's court (vault commits he owns)

- Commit the decision record: `vault/20_projects/research/2026-06-30-panel-vs-single-model-gate.md` (written, unstaged).
- Mark Step C panel-vs-single **✅ DONE / E2 = GO** in the fusion-discovery roadmap ticket.
- Follow-up tickets surfaced this session: (1) Sonar cost-integrity leak (`gather/sonar.py` bills ~$0.02/run unrecorded, contradicting the "every collector is FREE" docstring); (2) production evidence persistence (deferred to PM3).
