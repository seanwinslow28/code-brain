---
title: "Autonomous Agent Fleets"
type: concept
sources:
  - knowledge/concepts/autonomous-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-05-14
updated: 2026-05-14
---

## Definition

A collection of AI agents that operate independently, with predefined behavior rules to manage disruptions caused by external constraints such as network unavailability or hardware absence.

## Context

This is crucial for Sean's system to remain functional during trips, ensuring productivity and data integrity are preserved without manual intervention.

## Evidence

> `vault_synthesizer`, `job_feed`, and `flush` agents are hosted on the MBP, which is off the home LAN during travel

> The system has no notion of scheduled MBP absences — every failure looks identical to 'MBP happened to be asleep.'

## Examples

- `vault_synthesizer` exits cleanly when MBP is unreachable during a trip
- The `job_feed` agent skips scoring due to MBP being offline

## Related Concepts

[[Agent Health Monitoring]] [[Fleet Status]]
