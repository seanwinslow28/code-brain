---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - knowledge/concepts/supervision-fatigue-as-the-hard-cap-on-fleet-scaling.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This invariant defines the biological limit of human oversight where the cognitive load of reviewing and calibrating agent output grows non-linearly with the volume of generated artifacts. When the rate of automated synthesis exceeds the user's capacity for meaningful integration, a trust deficit emerges because the user perceives the high-volume output as low-value despite its statistical correctness. This fatigue acts as a hard cap on scaling because it forces a decoupling of automation from creativity, requiring manual taste tournaments to realign the system.

## Context

Sean's run logs show a clear correlation between increased duration and higher rejection counts, suggesting that his ability to supervise effectively diminishes as the fleet generates more clusters, ultimately limiting the effective scale of the automated system. The consequence is a forced decoupling of automation from creativity, requiring Sean to implement taste tournaments to realign the system's objective function with his strategic goals.

## Evidence

> This connection reveals a fundamental tension between the theoretical scalability of agent fleets and the biological limits of human supervision.

> The consequence is a forced decoupling of automation from creativity, requiring Sean to implement taste tournaments to realign the system's objective function with his strategic goals.

## Examples

- Run 2026-07-05: Duration of 2728.6 seconds with only 39 connections written, indicating diminishing returns on supervision time as clusters sampled increased.
- Run 2026-08-17: Duration of 2408.1 seconds with 25 connections, showing that even with optimized models, the supervision bottleneck remains a limiting factor for connection density.

## Related Concepts

[[The Taste-Throughput Trade-off in Agentic Synthesis]] [[Tacit Knowledge Erosion vs. Automation Scale]]
