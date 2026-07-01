---
title: "Agent Health Monitoring"
type: concept
sources:
  - knowledge/connections/the-tension-between-reliability-metrics-and-adaptive-capacity-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-01
updated: 2026-07-01
---

## Definition

This concept describes the transition from passive detection of broken states to active assessment of operational maturity through graceful degradation. It identifies that monitoring must evolve beyond simple loop catching to evaluate whether the system preserves its core intent despite component failures. The mechanism requires defining what 'healthy' looks like during partial failure, not just during nominal operation.

## Context

Sean's current monitoring treats health as a binary state, which fails to capture the nuanced reality of his agent fleet's adaptive capacity and creates blind spots in his job-hunt infrastructure reliability.

## Evidence

> Your current frame treats monitoring as detection: catch loops, hallucinations, broken states.

> Sean faces a structural tension where the traditional engineering obsession with reliability (uptime, success rates) clashes with the operational reality of resilience (graceful degradation under surprise).

## Examples

- Evaluating whether the synthesizer's rejected_count correlates with actual loss of intent.
- Analyzing the duration_seconds to identify when monitoring becomes a bottleneck rather than a safeguard.

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[SRE Error Budget for Agents]]
