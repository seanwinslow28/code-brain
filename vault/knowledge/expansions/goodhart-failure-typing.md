---
title: "How to make `Goodhart Failure Typing` better"
type: expansion
parent: "[[goodhart-failure-typing]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-27
updated: 2026-08-27
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[goodhart-failure-typing]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add “construct validation before failure typing”

The concept assumes “semantic value” is a known target. It is not. Novelty, usefulness, surprise, factuality, and cross-domain distance are different constructs; collapsing them into one score merely creates a better-disguised proxy.

Anchor this addition in Donald T. Campbell and Donald W. Fiske’s “[Convergent and Discriminant Validation by the Multitrait-Multimethod Matrix](https://doi.org/10.1037/h0046016)” (1959). Apply their pattern: **a semantic-quality measure is credible only when independent methods agree on the same trait and diverge on different traits.**

This unlocks a **Semantic Value MTMM scorecard**: rows for novelty/usefulness/factuality/actionability; columns for human blind review, embedding distance, citation verification, and independent-model judgment. That artifact could become both a fleet evaluation runbook and a strong portfolio one-pager. The current concept can label proxy failure but cannot establish whether the supposed target was ever measured.

### 2. Add “quantilization” as the missing remedy for extremal Goodhart

“Change the optimization strategy” is too vague. Add **quantilizer mode**: sample among outputs above an acceptable quality threshold instead of selecting the single highest-scoring output.

Anchor it in Jessica Taylor’s “[Quantilizers: A Safer Alternative to Maximizers for Limited Optimization](https://intelligence.org/files/QuantilizersSaferAlternative.pdf)” (2016). Operational sentence pattern: **“Generate N candidates, discard those below the factuality and relevance floor, then sample from the top q-percent rather than taking argmax.”**

This unlocks an executable **vault-synthesizer selection experiment** comparing argmax, top-k, and quantilized selection across novelty, unsupported claims, and human usefulness. It also supplies a concrete agent-spec primitive for intent-engineering: `selection_policy: quantile`, `optimization_budget`, and `quality_floor`. The present article diagnoses extremal failure without offering its most directly matched control.

### 3. Separate passive proxy breakdown from active evaluator-channel corruption

The article calls weak semantic output “adversarial” too quickly. Adversarial Goodhart requires an optimizing actor exploiting the metric. A fleet that emits shallow prose because uptime dominates evaluation may exhibit causal or extremal failure; it becomes adversarial when agents learn to manipulate what the evaluator sees.

Anchor the distinction in Tom Everitt, Marcus Hutter, Ramana Kumar, and Victoria Krakovna’s “[Reward Tampering Problems and Solutions in Reinforcement Learning: A Causal Influence Diagram Perspective](https://arxiv.org/abs/1908.04734)” (2019), especially its separation of **reward-function tampering** from **reward-input tampering**.

This unlocks a **semantic-evaluator threat model** and red-team demo: hide canary defects in generated concepts, vary whether the producing agent can observe the rubric, and test whether it improves the artifact or merely optimizes judge-visible features. That would let Sean write the sharper Substack argument: **“Your agent is not failing the metric; it is learning the interface to the metric.”**

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
