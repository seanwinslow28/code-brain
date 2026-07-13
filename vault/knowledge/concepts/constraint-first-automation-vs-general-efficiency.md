---
title: "Constraint-First Automation vs. General Efficiency"
type: concept
sources:
  - knowledge/connections/the-supervisory-cost-of-taste-transfer.md
tags: [auto-generated, phase-6]
created: 2026-07-13
updated: 2026-07-13
---

## Definition

This pattern identifies the trade-off between optimizing for broad operational efficiency and optimizing for specific, taste-encoded constraints. General efficiency seeks to minimize cost and time per unit of output, often by lowering the complexity of the rubric. Constraint-first automation accepts higher per-unit costs to ensure the output adheres to a narrow, high-fidelity aesthetic standard, prioritizing signal over noise.

## Context

Sean's prior runs with qwen3-14b optimized for general efficiency (more concepts written), while his recent runs with qwen3.6-35b optimize for constraint-first automation (fewer concepts, fewer rejections). He must decide which metric aligns with his current strategic goal.

## Evidence

> The old cadence strangled because three posts waited on unbuilt tools.

> Sean must allocate specific time for rubric refinement as a primary deliverable, not just a preparatory step, to prevent taste drift.

## Examples

- The qwen3-14b runs sampled 250+ clusters but wrote ~100 concepts, indicating a broad, less constrained approach.
- The qwen3.6-35b runs sampled ~140 clusters and wrote ~80 concepts with only ~20 rejections, indicating a tighter, constraint-first approach.

## Related Concepts

[[The Taste-Fidelity Decoupling in Creative Production]] [[Supervision as the New AI Edge]]
