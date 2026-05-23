---
title: "comprehension-audit"
type: concept
sources:
  - knowledge/concepts/comprehension-audit.md
tags: [auto-generated, phase-6]
created: 2026-05-23
updated: 2026-05-23
---

## Definition

A structured feedback loop where an AI model is tasked with identifying its own potential errors in a summary by re-evaluating the source material. This introduces a meta-cognitive layer where the model not only produces an analysis but also self-critiques it against original data, thereby surfacing uncertainties and gaps. The mechanism relies on an iterative process where a second pass through the data ensures accuracy, but also introduces caution and increased time requirements.

## Context

For Sean, this concept is crucial in high-stakes contexts such as legal, medical, or financial decision-making. It ensures that he can trust the accuracy of AI-generated summaries by introducing a safeguard against overconfidence in models, enabling more rigorous validation of critical information before action.

## Evidence

> The first time through, it’s trying to give you an answer. The second time, with the verification steps nudging it, it’s trying to catch where its own answer might be wrong.

> The cost is that the second pass takes longer and the revised answer comes back more cautious than the original.

## Examples

- The three-line verification prompt used to recheck summaries against source documents.
- Testing the same paper with two different prompts produces two versions of 'the truth.'

## Related Concepts

[[Vault Synthesizer Eval Suite]] [[Daily Note Generation]]
