---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/concepts/sre-error-budget-for-agents.md
tags: [auto-generated, phase-6]
created: 2026-07-01
updated: 2026-07-01
---

## Definition

An SRE error budget for agents is a quantitative constraint that limits the acceptable rate of automated failure or degradation to preserve long-term system trust and operational stability. Rather than treating fallback as an infinite resource, this mechanism defines a threshold where the cost of reliability (e.g., budget burn, latency) exceeds the value of the output, triggering a shift from automatic recovery to human escalation or hard failure. This transforms agent reliability from a binary uptime metric into a managed trade-off between availability and cost/quality integrity.

## Context

Sean is building autonomous agent fleets that operate with significant financial and temporal costs. Without an error budget, agents may continue to burn resources on low-value or corrupted outputs during provider degradation, eroding trust in the system. Defining this budget allows Sean to make explicit decisions about when to stop automating and start intervening.

## Evidence

> Fallback increases reliability only when it does not hide systemic failure, amplify cost, or degrade user trust.

> The current note treats fallback as uptime. It needs 'what kind of failure happened, and what kind of fallback is allowed?'

## Examples

- A cost-capped agent escalation policy where fallback is allowed until daily budget burn reaches N% or confidence drops below threshold.
- Routing to a secondary provider only if quality/cost/audit conditions hold, rather than automatic failover.

## Related Concepts

[[Provider Fallback Mechanism]] [[Agent Health Monitoring]]
