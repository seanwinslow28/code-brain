---
title: "Constraint-First Automation vs. General Efficiency"
type: concept
sources:
  - knowledge/concepts/constraint-first-automation-vs-general-efficiency.md
tags: [auto-generated, phase-6]
created: 2026-08-25
updated: 2026-08-25
---

## Definition

This principle dictates that system health is determined solely by the throughput of the current limiting stage, not by the aggregate activity of all stages. It requires identifying the specific constraint and subordinating all other processes to its relief, rather than optimizing for uniform efficiency across the entire pipeline. When automation ignores constraints, it produces output that cannot be consumed, creating inventory waste and masking the true state of the system. The fleet is healthy only if it increases throughput at the current constraint.

## Context

Sean's agent fleet often operates under a general efficiency model, attempting to maintain all components (resume, portfolio, applications) simultaneously. This approach fails during critical phases like interview preparation, where the bottleneck shifts and requires immediate reallocation of resources away from non-constraining activities.

## Evidence

> A pipeline is not a feed; it is a sequence of conversions with one limiting stage.

> The fleet is healthy only if it increases throughput at the current constraint.

## Examples

- Subordinating portfolio production efforts to interview drills when interview conversions drop, even if the portfolio is incomplete.
- Identifying the weekly bottleneck and tracking conversion rates at each stage rather than monitoring the uptime of application feeds.

## Related Concepts

[[Throughput vs. Activity Illusion in Job Hunt Operations]] [[Job Hunt as Sales Pipeline]]
