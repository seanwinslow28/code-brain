---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/expansions/the-illusion-of-health-in-autonomous-systems.md
tags: [auto-generated, phase-6]
created: 2026-07-01
updated: 2026-07-01
---

## Definition

This pattern redefines reliability from a binary success/failure metric to a quantifiable allowance of coordination risk at agent-to-agent boundaries. Instead of measuring whether individual scripts exit cleanly, it tracks specific failure modes such as stale context, missing artifacts, skipped writes, and silent fallbacks against a defined budget. The unit of reliability becomes the handoff contract, ensuring that the cost of coordination errors is explicitly accounted for rather than hidden in aggregate health metrics.

## Context

Sean needs to operationalize his agent fleet's reliability. By adopting an error budget approach, he can set concrete thresholds (e.g., 'daily note stale > 1 run = yellow') that trigger human intervention before the illusion of health masks a deeper systemic drift.

## Evidence

> Each agent-to-agent boundary gets a budget for stale context, missing artifacts, skipped writes, late outputs, and silent fallbacks.

> The unit of reliability is not the agent; it is the handoff contract.

## Examples

- Setting a threshold where 'context index older than 24h = degraded' forces a review of the indexing pipeline.
- Triggering an incident when a critic agent produces partial outputs twice in a row, indicating a breakdown in the common ground.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Context Management as a Bottleneck]]
