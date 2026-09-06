---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - knowledge/concepts/supervision-fatigue-as-the-hard-cap-on-fleet-scaling.md
tags: [auto-generated, phase-6]
created: 2026-09-06
updated: 2026-09-06
---

## Definition

This mechanism defines the non-linear increase in cognitive overhead required to maintain coherent oversight of an agent fleet, where the cost of verification grows faster than the volume of automated output. It emerges when the human operator becomes the single point of failure for semantic integrity, forced to manually reconcile contradictions that agents silently propagate. The bottleneck is not computational capacity but the finite bandwidth of human attention available to detect and correct these silent divergences before they corrupt downstream artifacts.

## Context

Sean's fleet runs have shown a dramatic increase in concepts written (from 3 to over 120) while the model capability remained static or degraded. This suggests that without a corresponding increase in automated verification mechanisms, Sean's personal cognitive load is becoming the primary constraint on system reliability, making manual supervision unsustainable at current scales.

## Evidence

> The phenomenon where the cognitive load of maintaining coherent context across multiple agents and domains limits the effective scale of automation.

> This bottleneck emerges when the complexity of inter-agent dependencies exceeds the capacity for manual verification.

## Examples

- contradiction (T2): knowledge/concepts/context-management-as-a-bottleneck.md — contradicts supervision-as-the-new-ai-edge
- contradiction (T2): knowledge/concepts/agent-health.md — contradicts context-management-as-a-bottleneck

## Related Concepts

[[Context Management as a Bottleneck]] [[The Context-Memory Bottleneck in Personalized AI]]
