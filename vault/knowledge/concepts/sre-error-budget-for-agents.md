---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/connections/the-tension-between-reliability-metrics-and-adaptive-capacity-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

This mechanism redefines agent health not as a binary state of success, but as a dynamic equilibrium where failure rates, recovery paths, and operator attention costs remain within an explicit budget. It treats the creative agent's output as a service level objective that must be balanced against the cost of intervention required to maintain it. The invariant is that an agent is only healthy if its operational friction stays predictable and bounded.

## Context

Sean needs to quantify the 'stretch' capability of his agents by tracking how much operator attention their failures require, rather than just counting successful runs.

## Evidence

> A creative agent is not healthy when it succeeds once; it is healthy when its failure rate, recovery path, and operator attention cost stay inside an explicit error budget.

> Your current frame treats monitoring as detection: catch loops, hallucinations, broken states.

## Examples

- Tracking operator attention cost alongside failure rates in the fleet memory index.
- Defining health by the stability of recovery paths rather than single-instance success.

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Agent Health Monitoring]]
