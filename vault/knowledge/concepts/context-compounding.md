---
title: "Context Compounding"
type: concept
sources:
  - knowledge/concepts/context-compounding.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

Context compounding is a progressive degradation of semantic integrity in an agent's working memory, where forgotten prior instructions or contradictory outputs accumulate over time. This phenomenon causes the model to drift from original user questions or redo previously completed work, effectively breaking the chain of reasoning required for complex tasks. It acts as a silent failure mode that only becomes apparent when the output quality drops below a usable threshold.

## Context

Sean's run logs indicate high rejection counts (e.g., 78 rejections in June vs. 14 in July) which correlate with context management strategies. Recognizing this mechanism allows him to diagnose why certain runs fail not due to model capability, but due to accumulated noise in the prompt window.

## Evidence

> when the model starts contradicting itself or it has to redo the work because it forgot it did that task in the first place or it starts to drift from your questions because it forgot them

> there is a critical tension between the desire to use cost-effective local models and their inherent inability to maintain long-horizon coherence without external support

## Examples

- A run that samples 253 clusters but writes only 109 concepts may be suffering from context compounding where earlier valid insights were overwritten or ignored by later, noisier inputs.

## Related Concepts

[[Harness Engineering Invariant]] [[Memory Rot and Lifecycle Management]]
