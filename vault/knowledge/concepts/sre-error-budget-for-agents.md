---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/concepts/sre-error-budget-for-agents.md
tags: [auto-generated, phase-6]
created: 2026-08-18
updated: 2026-08-18
---

## Definition

This concept reframes agent reliability not as a binary state of uptime but as a managed economic resource where failures are permitted within a calculated tolerance. It establishes that excessive reliability consumes infrastructure and opportunity cost, meaning the acceptable failure budget is determined by comparing the cost of prevention against the cost of recovery. This approach unlocks an agent SLO and error-budget policy specifying successful-output rate, maximum stale-output age, and tolerated deferred runs.

## Context

Sean's vault relies on automated synthesis; understanding that occasional failures are economically rational prevents over-engineering fragile systems for marginal gains in consistency. By treating reliability as a budget rather than an absolute, Sean can allocate engineering effort to feature work until the error rate exceeds the cost of recovery.

## Evidence

> Google’s Marc Alvidrez and Mark Roth argue the opposite in “Embracing Risk,” Chapter 3 of Site Reliability Engineering: excessive reliability consumes infrastructure and opportunity cost.

> This unlocks an agent SLO and error-budget policy specifying successful-output rate, maximum stale-output age, tolerated deferred runs, and when reliability work should displace feature work.

## Examples

- Allowing a local agent to occasionally defer execution rather than incurring the high cost of a cloud fallback for non-critical tasks.
- Defining a specific error budget percentage that triggers a shift from feature development to reliability engineering.

## Related Concepts

[[Agent Health and Cost Efficiency]] [[Operational Uptime vs. Cognitive Utility Tension]]
