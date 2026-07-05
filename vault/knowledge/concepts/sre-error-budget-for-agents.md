---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/connections/the-tension-between-reliability-metrics-and-adaptive-capacity-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

This mechanism establishes a quantitative threshold for acceptable failure in probabilistic systems, treating error not as a binary state but as a managed resource. It requires defining explicit limits on failure rates, recovery paths, and operator attention costs to prevent the 'illusion of health' where an agent appears functional but is actually degrading system stability. The invariant here is that a creative agent's health is determined by its ability to stay within these bounds during stress, rather than achieving perfect uptime which is often uninformative about underlying fragility.

## Context

Sean needs to apply this concept to his job hunt by framing his agent fleets as systems with managed error budgets. This demonstrates to potential employers that he understands the trade-offs between reliability and adaptive capacity, a key differentiator for senior engineering roles involving autonomous systems.

## Evidence

> A creative agent is not healthy when it succeeds once; it is healthy when its failure rate, recovery path, and operator attention cost stay inside an explicit error budget.

> The tension lies between defining strict Service Level Objectives for context availability and the reality that agents will inevitably fail to meet them.

## Examples

- Tracking operator attention cost during agent failures
- Defining recovery paths within an explicit error budget

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[The Illusion of Health in Autonomous Systems]]
