---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/connections/resilience-vs-reliability-in-agent-health.md
tags: [auto-generated, phase-6]
created: 2026-06-30
updated: 2026-06-30
---

## Definition

This concept establishes a quantitative threshold for acceptable agent failure, defining health not by the absence of errors but by the stability of three variables: failure rate, recovery path efficiency, and operator attention cost. It transforms agent reliability from an abstract quality into a managed resource that can be spent on feature development or innovation, provided the total error budget is not exhausted. The mechanism enforces a trade-off where higher reliability requires stricter constraints on creative or adaptive behaviors.

## Context

Sean needs to apply this metric to his agent fleet to move beyond simple uptime tracking. By defining explicit error budgets, he can justify periods of lower reliability during complex synthesis tasks, provided the recovery mechanisms are robust and the attention cost remains within bounds.

## Evidence

> A creative agent is not healthy when it succeeds once; it is healthy when its failure rate, recovery path, and operator attention cost stay inside an explicit error budget.

> The tension between SRE error budgets and resilience engineering lies in the balance between strict reliability targets and adaptive capacity.

## Examples

- Tracking operator attention cost as a key metric for agent health alongside failure rates.
- Using error budgets to enforce freezes on feature development when reliability drops below a threshold.

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Agent Health Monitoring]]
