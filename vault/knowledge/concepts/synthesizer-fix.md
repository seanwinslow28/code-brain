---
title: "Synthesizer fix"
type: concept
sources:
  - knowledge/concepts/synthesizer-fix.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This mechanism defines the strategic imperative of decoupling generation and evaluation models to prevent self-referential bias. It posits that family separation is the single highest-leverage, lowest-cost lever for improving epistemic hygiene in agentic workflows. By ensuring the evaluator is not a member of the candidate pool, the system can detect genuine novelty rather than reinforcing existing patterns.

## Context

Sean needs to implement this fix to stop the vault synthesizer from overestimating its own output quality due to model homogeneity. The current reliance on qwen3.6-35b-a3b-32k for both tasks creates a closed loop where internal consistency is mistaken for external truth.

## Evidence

> family separation is the single highest-leverage, lowest-cost lever

> When Sean relies on a single model family for both generation and evaluation, he risks optimizing for internal consistency rather than external truth.

## Examples

- Switching from qwen3.6-35b-a3b-32k to a different model family for the FUSE judge in the Vault Synthesizer Eval Suite.

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Vault Synthesizer Eval Suite]]
