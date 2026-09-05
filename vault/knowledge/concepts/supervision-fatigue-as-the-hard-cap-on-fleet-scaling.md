---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - knowledge/concepts/supervision-fatigue-as-the-hard-cap-on-fleet-scaling.md
tags: [auto-generated, phase-6]
created: 2026-09-05
updated: 2026-09-05
---

## Definition

This pattern defines the inverse relationship between agent fleet size and human oversight capacity, where the cognitive load of verifying low-confidence outputs grows non-linearly with the number of agents. As the volume of generated content increases, the human supervisor becomes the bottleneck not because of lack of time, but because of the diminishing marginal utility of each verification step. The system fails not when agents break, but when the cost of validation exceeds the value of the output.

## Context

Sean's fleet memory shows a progression from small runs (3 concepts) to large runs (125+ concepts). He is hitting limits where the 'rejected_count' and duration_seconds spike, indicating that human triage is becoming the limiting factor in his production pipeline.

## Evidence

> Human ranking degrades past ~7 items; triage-then-rank scales.

> Measurement: Blind two-stage read, rewrite the winner only, flaw-count on all

## Examples

- Implementing a 'stripped-samples arm' to turn arbitrary trimming into a principled noise floor measurement
- Using a 'blind two-stage read' protocol to separate initial triage from final ranking

## Related Concepts

[[The Calibration Bottleneck in Scalable Creative Production]] [[Context Management as a Bottleneck]]
