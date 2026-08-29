---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - knowledge/connections/the-efficiency-quality-inversion-in-automated-synthesis.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

This invariant defines the limit of autonomous operation imposed by human cognitive load rather than technical constraints. As the number of agents and their output volume increase, the time required for meaningful supervision grows non-linearly due to context switching and verification overhead. The system hits a hard cap where the cost of oversight exceeds the value of the automated work, forcing a reversion to manual processes or a reduction in automation scope.

## Context

Sean's daily runs show durations increasing from ~47 seconds to over 2700 seconds as complexity grew. This suggests that while the fleet is doing more work, Sean's ability to supervise it efficiently is degrading, creating a bottleneck at the human layer.

## Evidence

> This automates ___, but leaves Sean responsible for ___ under degraded visibility; preserve readiness through ___.

> The core tension lies in the misalignment between the exponential growth of automated concept generation and the linear capacity of human taste to curate them.

## Examples

- Sean must implement 'automation handback' protocols where he periodically performs manual tasks to maintain skill readiness.
- The fleet's success metrics should include a 'taste decay' indicator, not just throughput.

## Related Concepts

[[The Taste-Throughput Trade-off in Agentic Synthesis]] [[The Skill Atrophy Trap in Agentic Workflows]]
