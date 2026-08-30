---
title: "Concept Drift as a Systemic Risk"
type: concept
sources:
  - knowledge/concepts/concept-drift-as-a-systemic-risk.md
tags: [auto-generated, phase-6]
created: 2026-08-30
updated: 2026-08-30
---

## Definition

Concept drift is the phenomenon where the statistical relationship between input variables and the target output changes over time, rendering historical models obsolete. Unlike data drift, which is merely a shift in input distribution, concept drift implies that the fundamental rules governing the domain have shifted. This requires active monitoring of model performance against ground truth, not just input validation, to detect when the system's internal logic no longer matches reality.

## Context

In Sean's job hunt and product strategy, market conditions (e.g., AI tooling standards, hiring criteria) are shifting rapidly. Assuming past success patterns will continue without adjusting for these drifts leads to strategic errors. Recognizing this allows him to pivot his approach before his 'model' of the market becomes invalid.

## Evidence

> Data drift is a shift in input distribution; concept drift is a shift in the relationship between inputs and outputs

> Concept drift in housing markets and the reinforcing loop of adverse selection

## Examples

- The changing market made historical data irrelevant for Zillow Offers
- Sellers reacted to the model's pricing errors by adjusting their behavior

## Related Concepts

[[Adverse Selection]] [[Memory Rot and Lifecycle Management]]
