---
title: "Concept Drift as a Systemic Risk"
type: concept
sources:
  - knowledge/concepts/concept-drift-as-a-systemic-risk.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

Concept drift represents a fundamental shift in the causal relationship between input variables and target outputs, rendering historical predictive models obsolete not because the data changed, but because the underlying rules of the domain have altered. Unlike simple data drift, which is merely a statistical shift in input distribution, concept drift implies that the system's internal logic no longer matches reality, requiring active monitoring of performance against ground truth rather than just input validation. This phenomenon creates a hidden risk where systems appear operational while their predictive validity decays silently, leading to strategic errors when past success patterns are assumed to continue without adjustment.

## Context

In Sean's job hunt and product strategy, market conditions such as AI tooling standards and hiring criteria are shifting rapidly. Assuming past success patterns will continue without adjusting for these drifts leads to strategic errors because the 'model' of the market becomes invalid before it is detected. Recognizing this allows him to pivot his approach before his historical data loses its predictive power.

## Evidence

> Concept drift implies that the fundamental rules governing the domain have shifted, requiring active monitoring of model performance against ground truth, not just input validation, to detect when the system's internal logic no longer matches reality.

> Data drift is a shift in input distribution; concept drift is a shift in the relationship between inputs and outputs.

## Examples

- The changing market made historical data irrelevant for Zillow Offers
- Sellers reacted to the model's pricing errors by adjusting their behavior

## Related Concepts

[[Adverse Selection]] [[Memory Rot and Lifecycle Management]]
