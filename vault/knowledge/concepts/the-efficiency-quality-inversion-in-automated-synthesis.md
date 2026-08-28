---
title: "The Efficiency-Quality Inversion in Automated Synthesis"
type: concept
sources:
  - knowledge/expansions/connections/cost-capped-workflows-and-agent-health-monitoring.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

This pattern describes the inverse relationship between raw throughput metrics and the actual utility of generated artifacts, where increasing agent activity often degrades the signal-to-noise ratio of the output. As agents process more clusters or write more concepts without corresponding increases in human acceptance rates, the marginal cost per durable insight rises rather than falls. The system optimizes for activity volume while the user experiences a decline in meaningful synthesis.

## Context

Sean's prior runs show significant variance in concepts written versus rejected counts. Understanding this inversion helps him recognize that higher concept counts do not equate to better vault health, and that monitoring 'cost per accepted artifact' is a more accurate proxy for system value than total output volume.

## Evidence

> Stop reporting dollars per agent or month as the primary efficiency measure.

> Track cost per accepted artifact, cost per novel connection retained after 30 days, and human correction minutes per usable output.

## Examples

- Agent A costs more per run but less per accepted, durable artifact.

## Related Concepts

[[Throughput vs. Activity Illusion in Job Hunt Operations]] [[Supervision Fatigue as the Hard Cap on Fleet Scaling]]
