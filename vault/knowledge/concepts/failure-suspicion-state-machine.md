---
title: "Failure Suspicion State Machine"
type: concept
sources:
  - knowledge/expansions/coordinated-omission-in-agent-observability.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This is a state transition model that distinguishes between temporary silence and confirmed failure by introducing an intermediate 'suspected' state with evidence and expiry. Instead of immediately converting silence into a failure status, the system tracks whether an agent is overdue, allowing for recovery if it completes late or defers by policy. This prevents the manufacturing of certainty in asynchronous fleets where silence can result from sleep, network partitions, or telemetry failures rather than crashes.

## Context

Sean's agents operate in an asynchronous environment where host sleep and launchd delays are common; collapsing all missing heartbeats into 'unhealthy' triggers unnecessary recovery actions that waste time and resources. A suspicion state allows the system to wait for late completions before escalating, improving reliability without sacrificing responsiveness.

## Evidence

> In an asynchronous fleet, silence cannot prove whether an agent crashed, the host slept, the network partitioned, launchd never fired, or telemetry failed.

> An expected-run ledger that immediately converts silence into failure therefore manufactures certainty.

## Examples

- expected → overdue → suspected, followed by confirmed_failed, deferred_by_policy, or late_completed.
- Add a suspicion state with evidence and expiry to prescribe different recovery actions instead of collapsing every missing heartbeat into 'unhealthy.'

## Related Concepts

[[Agent Health]] [[Infrastructure Status]]
