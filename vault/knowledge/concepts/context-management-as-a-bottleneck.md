---
title: "Context Management as a Bottleneck"
type: concept
sources:
  - knowledge/concepts/context-management-as-a-bottleneck.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

This pattern identifies context maintenance as the primary constraint on agent reliability when state accuracy degrades over time. Agents fail to preserve or update critical information across interactions, leading to inconsistent outputs and degraded decision-making quality. The bottleneck emerges not from computational limits but from the inability to maintain semantic coherence.

## Context

Sean's agents struggle with maintaining accurate state across long-running workflows, particularly in job hunt tracking and creative project management. This bottleneck limits their ability to provide reliable support for complex, multi-step tasks.

## Evidence

> Context management acts as a bottleneck when agents fail to maintain accurate state across interactions, leading to degraded agent health and unreliable outputs.

> When an agent has full access but no judgment, it produces 'green' status indicators while silently propagating stale or incorrect context.

## Examples

- Agents losing track of previous decisions in long-running job hunt workflows
- Inconsistent creative project states due to failed context preservation

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Silent Failure Propagation in Agent Fleets]]
