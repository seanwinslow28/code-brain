---
title: "Constraint-First Automation vs. General Efficiency"
type: concept
sources:
  - knowledge/connections/the-supervisory-cost-of-taste-transfer.md
tags: [auto-generated, phase-6]
created: 2026-07-09
updated: 2026-07-09
---

## Definition

This pattern identifies the tension between optimizing for raw throughput (general efficiency) and optimizing for specific outcome fidelity (constraint-first automation). General efficiency seeks to minimize cost and time per unit, while constraint-first automation accepts higher initial setup costs to ensure the output aligns with complex, nuanced human standards. The mechanism fails when users apply general efficiency metrics to problems requiring high-fidelity constraint satisfaction.

## Context

Sean's prior runs show a trade-off: qwen3-14b offered high volume but lower fidelity (more rejections), while qwen3.6-35b-a3b-32k offered better alignment but required different supervision strategies. He must choose which efficiency metric serves his current goal.

## Evidence

> The old cadence strangled because three posts waited on unbuilt tools.

> As the number of agents scales, the cost of supervision does not decrease proportionally; instead, it increases because the rubric must become more complex to prevent drift.

## Examples

- The 'old cadence' being strangled by tool dependencies illustrates the failure of general efficiency when constraints are not met.
- The increase in rubric complexity with scaling agents demonstrates the non-linear cost of constraint-first automation.

## Related Concepts

[[The Taste-Fidelity Decoupling in Creative Production]] [[Supervision as the New AI Edge]]
