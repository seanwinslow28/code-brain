---
title: "Synthesizer fix"
type: concept
sources:
  - knowledge/concepts/synthesizer-fix.md
tags: [auto-generated, phase-6]
created: 2026-07-09
updated: 2026-07-09
---

## Definition

This mechanism enforces a strict architectural separation between the model family responsible for content generation and the distinct model family tasked with evaluation. By preventing the evaluator from recognizing its own internal patterns, this intervention eliminates the self-preference bias that typically inflates perceived quality in single-vendor workflows. The result is a restoration of epistemic integrity, ensuring that claims of multi-vendor diversity are structurally valid rather than merely rhetorical artifacts of homogenous testing.

## Context

Sean's prior runs demonstrated significant variance in rejection rates and concept counts depending on the model used, indicating that evaluation metrics were likely skewed by the evaluator's own architectural biases. Implementing this fix is critical for validating the credibility of his professional outputs and ensuring that his 'multi-vendor' claims hold up under rigorous, unbiased scrutiny.

## Evidence

> family separation is the single highest-leverage, lowest-cost lever

> removes a textbook bias from the headline 'multi-vendor' claim

## Examples

- The tension lies between the efficiency of using a single model family for both generation and evaluation versus the epistemic integrity required for genuine discovery.
- When the judge is part of the panel, the system optimizes for internal consistency (self-preference) rather than external truth

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Vault Synthesizer Eval Suite]]
