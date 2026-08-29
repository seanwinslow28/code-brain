---
title: "The Illusion of Health in Agent Observability Metrics"
type: connection
connects:
  - Coordinated Omission in Agent Observability
  - Agent Health Monitoring
  - The Illusion of Competence in Automated Systems
created: 2026-08-17
updated: 2026-08-17
---

## Synthesis

Agent health metrics often suffer from coordinated omission, where failures are not recorded because the system stops generating the observations needed to detect them. This tension exists between the apparent improvement in average performance metrics and the actual degradation of agent reliability, as sleeping machines produce no samples. The consequence is a false sense of security where dashboards look healthier precisely when the underlying infrastructure is failing to execute its scheduled tasks.

## Threads

### [[Coordinated Omission in Agent Observability]]

> Coordinated omission occurs when a stalled system stops generating the very observations that would reveal the stall.

### [[Agent Health Monitoring]]

> Health denominators come from expected work, not observed logs.

### [[The Illusion of Competence in Automated Systems]]

> This creates an illusion of competence where averages improve precisely when the system is failing to execute its scheduled tasks.

## Implications

- Sean needs an expected-run ledger that records scheduled, started, completed, deferred, absent, and stale states to capture true agent health.
- Dashboard design must account for missing data points as indicators of failure rather than ignoring them as neutral events.
