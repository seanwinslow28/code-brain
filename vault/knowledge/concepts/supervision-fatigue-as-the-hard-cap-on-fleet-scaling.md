---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - 20_projects/research/2026-09-09-productcraft-bench-composition-findings.md
tags: [auto-generated, phase-6]
created: 2026-09-16
updated: 2026-09-16
---

## Definition

This concept defines the non-linear increase in cognitive load required to maintain quality control over automated outputs as the volume of those outputs increases. It posits that 'supervision' is not a fixed cost but a variable cost that scales with the complexity and ambiguity of the agent's domain. When agents operate in high-ambiguity domains (like creative strategy or product positioning), the supervisor must engage in 'double-loop learning' to correct not just the output, but the underlying reasoning, which is exponentially more expensive than correcting syntax. The hard cap is reached when the cost of verification exceeds the value of the automated output.

## Context

Sean's research into 'Productcraft bench composition' reveals a shift from 'six seats' to 'seven seats' with a specific 'Insights & Analytics' role designed to audit evidence. This suggests an awareness that adding more automation (agents) without a dedicated, high-level auditing mechanism leads to quality degradation. The 'rejected_count' in his fleet memory shows he is already filtering out low-quality agent outputs.

## Evidence

> Adopt two boundary adjustments (positioning stays with the Strategist; OKR outcomes are co-signed by the Strategist, the roadmap belongs to Delivery).

> Run the seven seats as a sequential pipeline with two closed audit cycles.

## Examples

- The creation of a 'closed audit cycle' for the Insights & Analytics seat, ensuring that evidence is graded before it influences product decisions.
- The use of 'L4 gate' to confirm or cut seats before build, preventing the accumulation of low-value automation.

## Related Concepts

[[Supervision Fatigue as the Hard Cap on Fleet Scaling]] [[Legibility Debt as a Supervision Failure Mode]] [[The Calibration Bottleneck in Scalable Creative Production]]
