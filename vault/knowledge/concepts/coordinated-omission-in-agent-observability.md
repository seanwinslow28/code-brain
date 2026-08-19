---
title: "Coordinated Omission in Agent Observability"
type: concept
sources:
  - knowledge/concepts/coordinated-omission-in-agent-observability.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

Observability systems fail when they only record events that occur, ignoring the absence of expected events which may signal critical failures. In agent fleets, if a component stops producing output due to a silent error or resource constraint, the monitoring layer sees no anomaly because it is not tracking the *absence* of data as a failure condition. This omission creates blind spots where systemic decay goes undetected until the missing data causes a downstream dependency to fail.

## Context

Sean’s daily driver and job feed agents depend on consistent data flows. If their monitoring only logs 'success' upon completion, it misses the critical signal of 'no results found', which is often more informative than a successful fetch of irrelevant data.

## Evidence

> Deep Researcher is currently in an empty queue state, indicating a lapse in continuous background research necessary for insight generation.

> Job Feed report noted 'scored=0 mbp=False,' suggesting the pipeline may not be actively finding or scoring opportunities.

## Examples

- The fleet status reports 'status=empty-queue' for Deep Researcher, which is a factual statement of state but omits the implication that no research insights were generated.
- The Job Feed agent logs 'fetch=0 scored=0', which records the action taken (or not taken) but does not explicitly flag the lack of opportunities as a potential system or market issue.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Agent Health Monitoring]]
