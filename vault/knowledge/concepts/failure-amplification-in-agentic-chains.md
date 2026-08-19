---
title: "Failure Amplification in Agentic Chains"
type: concept
sources:
  - knowledge/concepts/failure-amplification-in-agentic-chains.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This mechanism describes how recovery attempts in distributed systems can exponentially increase load on downstream dependencies, turning a minor latency spike into a systemic outage. It highlights that three retries across a five-layer call chain can amplify downstream load 243 times, meaning retries create the outage and its cost rather than merely responding to it. This requires every recovery edge to have a retry owner, attempt ceiling, idempotency requirement, and dollar-token amplification bound.

## Context

Sean's agent fleet involves multiple subprocess wrappers and routers; uncontrolled retries in these chains risk cascading failures that degrade the entire knowledge synthesis pipeline. The transition from qwen3-14b to qwen3.6-35b-a3b-32k shows a shift in how these amplification effects are managed, with varying success rates in concept retention despite similar cluster sampling depths.

## Evidence

> Brooker shows that three retries across a five-layer call chain can amplify downstream load 243×; retries can therefore create the outage and its cost, not just respond to it.

> Every recovery edge has a retry owner, attempt ceiling, idempotency requirement, and dollar/token amplification bound.

## Examples

- Implementing a fleet retry-topology runbook for subprocess wrappers to prevent cascading load spikes.
- Comparing naive retries against single-layer retries, token buckets, capped backoff, and deterministic jitter in failure demos.

## Related Concepts

[[Coupling Fragility vs Adaptive Capacity in Agent Fleets]] [[Silent Failure Propagation in Agent Fleats]]
