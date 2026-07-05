---
title: "Provider Fallback Mechanism"
type: concept
sources:
  - knowledge/concepts/provider-fallback-mechanism.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

A provider fallback is not a retry policy; it is a runtime state machine that decides when a dependency is no longer trustworthy enough to call. This mechanism preserves the mission of the workflow by allowing partial completion rather than forcing a total failure when specific providers become unreliable. It requires explicit degraded behavior protocols to prevent invisible cost leakage from accumulating over time.

## Context

Sean must implement explicit degraded behavior protocols for each provider route to prevent invisible cost leakage. The agent fleet requires a decision artifact defining thresholds for disabling specific providers before their failures contaminate the entire workflow.

## Evidence

> A provider fallback is not a retry policy; it is a runtime state machine that decides when a dependency is no longer trustworthy enough to call.

> Provider fallback should preserve the mission of the workflow, not the illusion that every step completed.

## Examples

- Runtime state machine for dependency trust
- Explicit degraded behavior protocols

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Automation Reliability]]
