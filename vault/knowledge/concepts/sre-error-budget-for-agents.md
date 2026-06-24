---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/expansions/connections/agent-health-monitoring-and-job-hunt-2026-automation-reliability.md
tags: [auto-generated, phase-6]
created: 2026-06-24
updated: 2026-06-24
---

## Definition

An SRE error budget defines a quantified tolerance for failure within an autonomous system, establishing a threshold where reliability work supersedes feature velocity. This mechanism shifts the operational paradigm from preventing all errors to managing the rate of acceptable loss, allowing agents to fail silently up to a defined limit before triggering mandatory remediation protocols. By treating reliability as a finite resource rather than an absolute state, the system enables higher throughput during stable periods while enforcing strict governance when failure rates exceed the budgeted contract.

## Context

Sean needs this concept to articulate his approach to autonomous systems in job-hunt interviews, moving beyond simple monitoring descriptions to demonstrate enterprise-grade reliability thinking. It provides a concrete artifact for his portfolio that shows he understands the trade-offs between velocity and trust in high-risk environments.

## Evidence

> Agent X may silently fail N times per month before feature velocity stops and reliability work becomes mandatory.

> Error budgets let him say, 'I manage autonomous systems with explicit reliability tradeoffs between velocity, cost, and trust.'

## Examples

- A one-page 'Agent Fleet SLO / Error Budget Runbook' showing reliability thinking in employer-native language.

## Related Concepts

[[Automation Reliability]] [[Agent Health Monitoring]]
