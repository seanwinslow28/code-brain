---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/expansions/connections/cost-capped-workflows-and-agent-health-monitoring.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

An SRE error budget transforms agent reliability from a binary health check into a quantifiable tolerance for failure, allowing the system to trade off availability against cost or quality based on remaining slack. When the burn rate of failures exceeds a defined threshold, the system must execute predetermined remediation steps rather than merely logging errors. This mechanism shifts the operational focus from preventing all errors to managing the acceptable rate of error-induced disruption within a specific time window.

## Context

Sean's agent fleet has historically suffered from silent failures and inconsistent outputs. By defining an explicit error budget, Sean can automate decisions about when to suspend non-critical synthesis runs or escalate to human review, preventing the accumulation of low-quality artifacts that degrade his knowledge vault over time.

## Evidence

> Define a user-visible SLO—such as “95% of scheduled runs produce a usable artifact by its deadline”—then treat the remaining failure allowance as an error budget.

> Its crucial move is converting telemetry into predetermined operating decisions.

## Examples

- When burn rate exceeds X, suspend Y and execute Z.

## Related Concepts

[[Agent Health Monitoring]] [[Operational Readiness Review]]
