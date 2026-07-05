---
title: "Agent Health Monitoring"
type: concept
sources:
  - knowledge/concepts/agent-health-monitoring.md
tags: [auto-generated, phase-6]
created: 2026-06-08
updated: 2026-06-08
---

## Definition

Agent Health Monitoring is the operational discipline of verifying autonomous agent completion through explicit observable signals rather than assuming success based on process exit codes. This mechanism requires distinguishing between successful execution and silent failure, where an agent completes its task but produces incorrect or missing data without raising exceptions. The system relies on statistical sampling, human review, and anomaly detection to catch errors that do not raise exceptions, ensuring that the operational status is decoupled from data freshness only when explicit checks are in place.

## Context

Sean's morning brief depends on the previous day's synthesis being complete. When the synthesizer fails silently, he notices the staleness before the brief flags the failure, highlighting a lag in error detection that necessitates explicit health checks to raise errors rather than relying on silent failures to be detected by absence.

## Evidence

> Agent Health Monitoring is the operational discipline of verifying autonomous agent completion through explicit observable signals rather than assuming success based on process exit codes.

> Sean notices the staleness of his morning brief before the brief itself flags the failure, indicating a lag in error detection.

## Examples

- ing output that is wrong, with no error signal. No exception. No confidence flag. It looks identical to correct output.

## Related Concepts

[[Accountability Gap]] [[Automation Failure and Daily Note Disruption]]
