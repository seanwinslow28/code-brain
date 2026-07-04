---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/connections/the-tension-between-reliability-metrics-and-adaptive-capacity-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-04
updated: 2026-07-04
---

## Definition

This concept establishes that agent health is not defined by perfect success rates but by the containment of failure costs within an explicit operational budget. It defines a mechanism where the acceptable error rate is determined by the operator's attention cost and the complexity of the recovery path, rather than technical uptime alone. The invariant here is that a creative agent remains healthy only when its failure frequency and remediation overhead stay within predefined limits. This shifts the engineering focus from preventing all errors to managing the economic and cognitive impact of inevitable errors.

## Context

Sean needs to articulate how his agents manage their own 'error budgets' to avoid overwhelming human operators with noise or requiring excessive manual intervention. This metric is crucial for proving that his systems are sustainable at scale, not just functional in isolation.

## Evidence

> A creative agent is not healthy when it succeeds once; it is healthy when its failure rate, recovery path, and operator attention cost stay inside an explicit error budget.

> There is a fundamental tension between the desire for high availability through provider fallback and the risk of amplifying systemic failure or cost when those fallbacks are unbounded.

## Examples

- The rejection count in fleet runs increasing from 1 to 80 indicates a shift in the error budget consumption, requiring adjustments in sampling strategies.
- Monitoring as detection catches loops and hallucinations, but does not inherently measure the cost of the operator's attention required to resolve them.

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Agent Health Monitoring]]
