---
title: "Prior Art — The Tested Mechanism Library (Kickoff D, Topic 1)"
type: research-pointer
status: complete
domain: [substack-studio]
tags: [pencil-and-prompt, refocus-2026-08, prior-art, prompt-libraries, evals, prompt-registries, prompt-marketplaces, creativity-benchmarks, retractions, gemini-deep-research, research]
created: 2026-08-05
last-updated: 2026-08-05
sources: [gemini-deep-research]
tool: "gemini_dr.py --tier dr (google-genai 2.x, agent=deep-research-preview-04-2026)"
cost_usd: 2.80
wall_seconds: 538
interaction_id: v1_ChdvQkZ6YXZ5OEpMNlYxTWtQbnRMMjJRZxIXb0JGemF2eThKTDZWMU1rUG50TDIyUWc
report: "[[2026-08-05-what-exists-today-weight-post-2025-sources-heavily-across-th]]"
related: [2026-08-05-divergence-mechanisms-evidence-map, 2026-08-05-prior-art-synthesis]
ai-context: "POINTER note, not the report. The full 46KB Gemini Deep Research output lives at vault/20_projects/research/2026-08-05-what-exists-today-weight-post-2025-sources-heavily-across-th.md and is the canonical artifact; this file exists so the substack-studio project can find it and knows why it was commissioned. Topic 1 of Kickoff D. Read the RELIABILITY CAVEAT below before citing anything from the report — it contains at least one verifiable factual error, so treat every specific claim as a lead to verify, not as established fact."
---

# Prior Art — The Tested Mechanism Library

> **This is a pointer note.** The full report is at [[2026-08-05-what-exists-today-weight-post-2025-sources-heavily-across-th]] (46KB, 60 citations). Kickoff D, Topic 1. Run 2026-08-05 on the DR tier, $2.80, 538s.

## Why this was commissioned

The 2026-08-04 partner session loose-locked a refocus for Pencil & Prompt whose riskiest bet is the product: **a public, versioned, TESTED mechanism library** — per-entry beat/tied/lost verdicts, with failures and public retractions shipped rather than buried.

That bet only makes sense if nobody already does it. Sean's standing practice is to research prior art before locking a design decision, so this run asks the direct question: **does any existing library publish per-entry tested verdicts that include honest failures and public retractions?**

Scope covered: prompt/technique libraries publishing per-entry evaluation results; versioned prompt registries with test suites; prompt-pack marketplaces and their trust dynamics; public benchmarks for creative/divergent output; and retraction/changelog practice in prompt-engineering communities.

## What the report concludes

The report's direct answer is **"yes, but barely, and not in this lane."** It names exactly two examples:

- **Techpresso AI Academy** — a public curated prompt library that the report says publishes "honest failures alongside" successful prompts. Human expert curation, no programmatic testing.
- **Aksoy Capital** — a financial research firm running a 1-hour retraction SLA with URL preservation and public correction logs. Genuinely rigorous, but it is algorithmic *financial research*, not a prompt or technique library.

Everything else splits into two camps that both miss the target. Enterprise eval infrastructure (Future AGI, Braintrust, MLflow, Langfuse, DeepEval) has real per-entry rigor — CI/CD eval gates, immutable version snapshots, production traces converted into regression tests — but it is private, engineer-facing, and never published as a public library. Consumer marketplaces (PromptBase, 260k prompts) publish freely but carry no evidence standard at all; the report describes a $2.51B market with a structural trust deficit where "a $1.99 text string provides no cryptographic or statistical guarantee."

On measurement specifically: **CreativityPrism** (academic, scores divergent ideation and names "Logic Inertia" as the failure mode where goal-fixation suffocates divergence) and **Springboards / the "Flint" model** (advertising industry, claims 10–30× more creative diversity than frontier models, judged by human taste rather than deterministic checks) are the two named attempts to benchmark creative/divergent output.

## ⚠️ Reliability caveat — read before citing

The report contains at least one plainly false claim: it states "Claude 3.7's 2M tokens, Gemini 2.0's 10M tokens" as established context-window figures. Neither is true. That is a grounding failure, not a typo.

Consequences for how this gets used:

1. **Treat every specific claim as a lead, not a fact.** Named entities, dollar figures, and percentages need independent verification before any of them appears in a published post.
2. **Citations are opaque.** All 60 sources are Google `vertexaisearch.cloud.google.com/grounding-api-redirect/...` URLs, not direct links. Resolving them is a manual step.
3. **The load-bearing answer rests on two thin examples.** Techpresso is a newsletter-adjacent brand, and Aksoy Capital is out-of-domain. Neither is a prompt/technique library publishing per-entry tested verdicts in the sense the refocus means. The honest reading is closer to **"the white space is real"** than to the report's own "yes, this standard exists."

The strategic conclusion survives the caveat; the supporting details do not, until checked.

## What it means for the refocus

See [[2026-08-05-prior-art-synthesis]] for the cross-topic findings and what should change about build order. In one line: the tested-library bet looks defensible, because the rigor exists but stays private and the public libraries carry no evidence standard — but the verification burden falls on us, and the first public claim needs its own sourcing.
