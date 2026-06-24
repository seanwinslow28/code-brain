---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: connection
connects:
  - Provider Fallback Mechanism
  - Automation Reliability
  - Silent Failure Propagation in Agent Fleets
created: 2026-06-24
updated: 2026-06-24
---

## Synthesis

The tension between the imagined reliability of automated workflows and the actual state of distributed dependencies reveals that fallback mechanisms must account for partial failures rather than binary success/failure states. When Sean's agents assume all steps complete, they ignore the reality that providers may bill without recording or fail silently, leading to a gap between intended workflow integrity and actual operational outcome. This gap forces a shift from parser hardening to workflow design, where partial outputs with named confidence states become the norm rather than the exception.

## Threads

### [[Provider Fallback Mechanism]]

> A provider fallback is not a retry policy; it is a runtime state machine that decides when a dependency is no longer trustworthy enough to call.

### [[Automation Reliability]]

> Fallback is insufficient once a side effect has crossed the boundary; the system now needs compensation, reconciliation, or quarantine.

### [[Silent Failure Propagation in Agent Fleets]]

> When a synthesizer fails silently overnight, the morning brief inherits stale context, and the user notices the staleness before the brief flags the failure.

## Implications

- Sean must implement explicit degraded behavior protocols for each provider route to prevent invisible cost leakage from accumulating over time.
- The agent fleet requires a decision artifact defining thresholds for disabling specific providers before their failures contaminate the entire workflow.
