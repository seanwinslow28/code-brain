---
title: "Panel-vs-single-model gate — does the Fusion panel earn its cost?"
date: 2026-06-30
type: research
project: fusion-discovery-council
status: complete
tags: [discovery, validation-gate, fusion-panel, evals]
---

# Panel-vs-single-model gate (Step C, red-team #4)

**Decision: the multi-model Fusion panel beats a single strong model. The panel earns its cost → E2 (panel self-preference fix) is GO.**

## The question

Does the 4-model Fusion panel (`opus-4.7 + gpt-5.5 + gemini-pro + grok-4.3`) produce materially better pain points than one strong model (`opus-4.7`) alone? If a single model tied the panel on a blind rating, the panel's cost and the E2 self-preference complexity wouldn't be worth it.

## Method (controlled dual-fuse)

Held everything constant except panel breadth:
- **Same evidence bundle** — gathered once (46 real-URL records), frozen to disk, fused by both arms.
- **Same judge** — `claude-opus-4.7` clustered in both arms.
- **Same tier** — standard, `max_tool_calls=5`.
- **Varied only** the analysis panel: arm A = 4 models, arm B = opus alone.
- **Topic:** "artists/writers/designers who say AI is a slot machine … stopped chasing prompts for a repeatable system" (n=1).
- **Blind rating:** the two pain-point sets were anonymized + shuffled (sha256-deterministic), then rated by the variance LLM-council (Claude, GPT-5.4-mini, DeepSeek, Mistral; sonnet chairman) on signal density, evidence grounding, distinctness, and actionability. The mapping (Set→arm) was kept in a separate key file; raters were blind.

## Findings

| | Confidence | Evidence |
|---|---|---|
| **Panel (arm A) wins all 4 criteria** | High | Variance council chairman synthesis; 3 of 4 models picked the panel overall. Set 1 (=panel) swept signal density, grounding, distinctness; actionability split 2–2 but leaned panel. |
| **Single model dilutes via false breadth** | High | Opus-alone produced 5 points vs the panel's 4, but split the core workflow complaint into two overlapping buckets and added a 5th point ("compulsive lever-pulling") grounded only in Reddit memes — lowering signal-to-noise. |
| **The panel's points were genuinely orthogonal** | High | Four non-redundant buckets, each → a discrete product opportunity: (1) baseline nondeterminism, (2) provider-driven model-update churn, (3) missing determinism tooling (seeds/version-pin), (4) craft-erosion as identity cost. |
| **Cost premium is small (~8%)** | High | Panel $1.34 vs opus-alone $1.24 per fuse. Better quality at a trivial premium. |
| **Not an Anthropic-family artifact** | Medium | The panel arm's judge + one rater are Anthropic, a plausible confound — but two non-Anthropic raters (DeepSeek, Mistral) also backed the panel; only GPT-5.4-mini dissented. Cross-lineage agreement mitigates it. |

## How this changed the roadmap

- **E2 (panel self-preference fix) = GO.** The panel demonstrably adds value, so hardening it against judge self-preference / authorship bias / evidence-order effects is worth building.
- **Quick/single-model tiers are not a quality substitute** for standard on pain-point clustering — the breadth genuinely de-duplicates and orthogonalizes. Keep the panel as the standard default.

## Honest limits

- **n=1.** One topic; the sweep was clean enough not to need a tie-break, but other topic shapes are unproven. Re-run on a second topic if E2's design hinges on the margin.
- The premium being only ~8% means the panel "earns its cost" with little room to spare — if a future single model closed the quality gap, revisit.

## Cost

Dual-fuse $2.5863 + blind rating $0.1834 = **$2.77** (discovery caps $10/day, $50/month; today $0 pre-run, month-to-date $24.82).

## Artifacts

`tools/llm-council/experiments/runs/panel-vs-single-20260630-115751/` — bundle, both arms, blind-rating.md, key.json, council-verdict.md. Harness: `tools/llm-council/experiments/`. Field report: `docs/field-reports/2026-06-30-fusion-discovery-council-stepc-panel-vs-single-gate-field-report.md`.

## Follow-ups surfaced

- **Sonar cost-integrity leak:** `council/discovery/gather/sonar.py` bills OpenRouter ~$0.02/run but never records it, while the gather docstring asserts "every collector is FREE." Tiny but real; separate fix.
- **Production evidence persistence:** deferred to the PM3 longitudinal decision; this gate only persists its own experiment bundle.
