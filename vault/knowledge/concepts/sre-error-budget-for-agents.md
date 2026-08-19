---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/expansions/connections/agent-health-monitoring-and-daily-note-generation-interdependence.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

An SRE error budget is a quantitative allowance for failure, defined as the difference between desired availability and actual achieved reliability over a specific period. In agentic systems, this shifts the metric of success from binary health checks to a probabilistic assessment of whether the consumer-facing service met its Service Level Indicators (SLIs). When the accumulated suspicion score exceeds the budgeted threshold, the system must pause expansion and fund reliability work rather than continuing to generate artifacts that degrade in quality. This mechanism forces a trade-off between velocity and trust, treating missed deadlines or stale context as financial debt against future capability.

## Context

Sean's daily note generation has historically suffered from silent failures where agents run but produce unusable output. By defining an error budget for the synthesizer, Sean can objectively decide when to stop adding new agents and instead harden the existing fleet, preventing the accumulation of 'legibility debt' that makes debugging impossible.

## Evidence

> If the monthly error budget exceeds Z, pause fleet expansion and fund reliability work.

> The consumer-facing SLI is X; agent heartbeat Y is only a diagnostic signal.

## Examples

- Allowing 5 failed or degraded mornings per month before triggering a reliability sprint.
- Using the φ Accrual Failure Detector to model health as accumulated evidence rather than a binary state.

## Related Concepts

[[Agent Health Monitoring]] [[Operational Uptime vs. Cognitive Utility Tension]]
