---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/connections/the-monitoring-utility-gap-in-personal-knowledge-infrastructure.md
tags: [auto-generated, phase-6]
created: 2026-08-25
updated: 2026-08-25
---

## Definition

This pattern highlights the gap between the intended workflow (work-as-imagined) and the actual execution path taken by agents (work-as-done). When agents deviate from expected paths due to failures or ambiguities, the resulting state may be functionally different despite appearing correct on the surface. Resilience requires monitoring these deviations rather than just assuming adherence to protocol.

## Context

Sean's daily note generation is imagined as a linear pipeline, but agents often take shortcuts or fail silently. This creates a discrepancy between what he expects to see in his vault and what actually exists, undermining his ability to rely on the system.

## Evidence

> Contradict the article’s linear failure story with resilience engineering: Remove the implied chain “unhealthy agent → missing note → reduced produ” and model the daily note as a revisable event-time projection.

> The consequence is that his trust in the system erodes not because of crashes, but because of subtle quality degradation that standard health checks miss.

## Examples

- An agent skips semantic validation to meet a time deadline, resulting in incomplete notes.
- A synthesizer rejects clusters due to strict criteria, leaving gaps in the knowledge graph.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Silent Failure Propagation in Agent Fleets]]
