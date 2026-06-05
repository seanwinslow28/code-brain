---
title: "Agent Health Monitoring"
type: concept
sources:
  - knowledge/connections/silent-failure-and-verification-burden.md
tags: [auto-generated, phase-6]
created: 2026-06-05
updated: 2026-06-05
---

## Definition

Agent Health Monitoring is the operational discipline of verifying autonomous agent completion through explicit observable signals rather than assuming success based on process exit codes. It requires distinguishing between successful execution and silent failure, where an agent completes its task but produces incorrect or missing data. The mechanism relies on statistical sampling, human review, and anomaly detection to catch errors that do not raise exceptions.

## Context

Sean's morning brief depends on the previous day's synthesis being complete. When the synthesizer fails silently, he notices the staleness before the brief flags the failure. This lag in error detection highlights the need for explicit health checks that raise errors rather than relying on silent failures to be detected by absence.

## Evidence

> Sean notices the staleness of his morning brief before the brief itself flags the failure, indicating a lag in error detection.

> Agent Health Monitoring is the operational discipline of verifying autonomous agent completion through explicit observable signals rather than assuming success based on process exit cod

## Examples

- ing output that is wrong, with no error signal. No exception. No confidence flag. It looks identical to correct output.

## Related Concepts

[[Accountability Gap]] [[Automation Failure and Daily Note Disruption]]
