---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/expansions/the-illusion-of-health-in-autonomous-systems.md
tags: [auto-generated, phase-6]
created: 2026-07-01
updated: 2026-07-01
---

## Definition

This framework highlights the divergence between the theoretical model of system operation and the actual practices agents and humans employ to keep the system running. It posits that failures arise not from component breakdowns but from the accumulation of local adaptations that, while rational in the moment, erode the shared assumptions necessary for coordinated action. The tension lies in the fact that these adaptations are often invisible to standard observability tools that only monitor the 'imagined' workflow.

## Context

Sean's agent fleet likely develops workarounds for missing context or failed handoffs. Understanding this divergence helps him identify where the fleet is 'working around' problems rather than solving them, which is critical for maintaining trust in automated outputs.

## Evidence

> The missing facet is that “green dashboards” are not just bad summaries; they are part of how systems normalize deviance.

> A green system can still be dangerous if it has lost shared context with its human operator.

## Examples

- Agents silently falling back to cached data when real-time retrieval fails, maintaining uptime but losing freshness.
- Human operators ignoring stale outputs because the dashboard remains green, reinforcing the normalization of deviance.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Silent Failure Propagation in Agent Fleets]] [[Common Ground Breakdown]]
