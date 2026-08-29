---
title: "Hedged Execution Invariant"
type: concept
sources:
  - knowledge/expansions/connections/cost-capped-agentic-workflows-and-agent-health-monitoring.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

Hedged execution is a reliability technique that treats redundancy as a priced mechanism for suppressing tail latency rather than waste. It involves duplicating slow operations only after the primary crosses its p95 completion threshold, then canceling the loser and charging the duplication against a separate hedge budget. This pattern trades a modest resource increase for sharply improved high-percentile latency, effectively escaping wedged model states by accepting the first valid result among parallel attempts.

## Context

Sean's agent fleet faces intermittent latency spikes that degrade user experience without triggering standard failure metrics. By implementing hedged execution, he can benchmark single-model retries against parallel council execution to establish a decision rule for when redundancy becomes resilience, particularly for unreliable local-model routes.

## Evidence

> Duplicate only after the primary crosses its p95 completion threshold; cancel the loser; charge duplication against a separate hedge budget.

> Sometimes deliberately duplicating a slow operation and accepting the first valid result is the cheapest way to suppress tail latency or escape a wedged model.

## Examples

- A benchmarking artifact comparing single-model retry, parallel council execution, and delayed hedging across cost, completion rate, and p95 latency.
- A defensible decision rule for when redundancy is waste versus resilience—especially for unreliable local-model routes.

## Related Concepts

[[Cost-Capped Agentic Workflows]] [[Agent Health]]
