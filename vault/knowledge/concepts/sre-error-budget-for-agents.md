---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/expansions/connections/cross-domain-bridging-through-agent-health-monitoring.md
tags: [auto-generated, phase-6]
created: 2026-08-30
updated: 2026-08-30
---

## Definition

An SLO-driven enforcement policy that treats agent reliability as a finite resource rather than a binary health state. When the error budget is exhausted, the system triggers specific remediation actions—such as freezing new agent deployments or degrading to minimal output—rather than merely logging failures. This shifts the operational focus from passive monitoring of uptime to active prioritization of cognitive utility against infrastructure cost.

## Context

Sean's fleet runs daily synthesizer jobs that consume significant compute and model tokens. Without an error budget, he risks over-investing in marginal reliability gains while ignoring the opportunity cost of failed runs. Defining a burn-rate alert allows him to make trade-off decisions about when to stop spending resources on a failing pipeline.

## Evidence

> Replace “failure detected” with a user-centered SLI, an SLO, and an enforcement policy.

> Define what happens when the budget is exhausted: freeze new agents, repair the highest-consuming dependency, or degrade to a minimal note.

## Examples

- By 08:35, the daily note contains a complete overnight digest and current fleet status on 29 of 30 days.
- Freeze new agents when the error budget is exhausted.

## Related Concepts

[[Agent Health Monitoring]] [[Operational Uptime vs. Cognitive Utility Tension]]
