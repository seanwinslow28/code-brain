---
title: "Coordinated Omission in Agent Observability"
type: concept
sources:
  - knowledge/expansions/coordinated-omission-in-agent-observability.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This is a sampling bias where latency measurements exclude periods of system unavailability because the monitoring agent itself fails to issue requests during those outages. When an agent sleeps or stalls, it stops generating telemetry, creating a blind spot that makes the observed performance appear artificially robust compared to the actual user experience. The defect arises when denominators contain only observed work rather than expected scheduled intervals, effectively hiding the cost of missed deadlines from the distribution.

## Context

Sean's fleet relies on precise timing for daily notes and synthesis; if the synthesizer silently misses a run due to sleep or network issues, standard metrics will not reflect this failure, leading to false confidence in system health. Understanding this bias is critical for designing SLOs that measure artifact delivery by deadline rather than just request success rates.

## Evidence

> Coordinated omission is specifically a sampling error: a blocked load generator stops issuing requests, so the missing requests never enter the latency distribution.

> Your article currently says the defect arises when denominators come from expected work; that is backwards. Expected work is the correction—the defective denominator contains only observed work.

## Examples

- A fault-injection demo showing the naïve and corrected p50/p99 while an MBP sleeps or a baton stalls.
- For every missed scheduled interval, record a deadline-relative synthetic latency or explicit omission, never zero samples.

## Related Concepts

[[SRE Error Budget for Agents]] [[Agent Health Monitoring]]
