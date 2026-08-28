---
title: "Redundancy as Priced Reliability vs. Waste"
type: connection
connects:
  - Hedged Execution Invariant
  - Cost-Capped Agentic Workflows
  - Agent Health
created: 2026-08-28
updated: 2026-08-28
---

## Synthesis

The pattern emerges when Sean treats redundancy as a priced mechanism for suppressing tail latency rather than waste, trading modest resource increases for sharply improved high-percentile latency. By duplicating slow operations only after the primary crosses its p95 completion threshold and canceling the loser, he charges duplication against a separate hedge budget. This creates a benchmarking artifact that compares single-model retry, parallel council execution, and delayed hedging across cost, completion rate, and p95 latency. The consequence is a defensible decision rule for when redundancy becomes resilience, particularly for unreliable local-model routes.

## Threads

### [[Hedged Execution Invariant]]

> Duplicate only after the primary crosses its p95 completion threshold; cancel the loser; charge duplication against a separate hedge budget.

### [[Cost-Capped Agentic Workflows]]

> Sometimes deliberately duplicating a slow operation and accepting the first valid result is the cheapest way to suppress tail latency or escape a wedged model.

### [[Agent Health]]

> A benchmarking artifact comparing single-model retry, parallel council execution, and delayed hedging across cost, completion rate, and p95 latency.

## Implications

- Sean establishes a defensible decision rule for when redundancy is waste versus resilience—especially for unreliable local-model routes.
- The agent fleet can escape wedged model states by accepting the first valid result among parallel attempts, improving user experience without triggering standard failure metrics.
