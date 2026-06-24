---
title: "Provider Fallback Mechanism"
type: concept
sources:
  - knowledge/expansions/provider-fallback-mechanism.md
tags: [auto-generated, phase-6]
created: 2026-06-24
updated: 2026-06-24
---

## Definition

A runtime state machine that decides when a dependency is no longer trustworthy enough to call, moving beyond simple retry policies to include circuit breaker semantics with explicit failure thresholds and cool-down windows. This mechanism treats provider weirdness not as a parsing defect but as an operational signal requiring degraded behavior, such as suppressing output or marking runs financially untrusted. It enforces the invariant that the system must preserve the mission of the workflow rather than maintaining the illusion that every step completed successfully.

## Context

Sean's agent fleet relies on multiple external providers (OpenRouter, Fusion) where silent failures can lead to invisible cost leakage or split-brain accounting events. Without this mechanism, failed calls might bill externally while recording zero locally, creating a trust deficit that undermines the integrity of the entire knowledge vault infrastructure.

## Evidence

> A provider fallback is not a retry policy; it is a runtime state machine that decides when a dependency is no longer trustworthy enough to call.

> Fallback is insufficient once a side effect has crossed the boundary; the system now needs compensation, reconciliation, or quarantine.

## Examples

- When OpenRouter bills failed calls but records $0 locally, the system must detect this split-brain accounting event and trigger a reconciliation process.
- If citation verification fails, the agent suppresses FRAME output rather than emitting unverified data, marking the run with a named confidence state.

## Related Concepts

[[Automation Reliability]] [[Silent Failure Propagation in Agent Fleets]]
