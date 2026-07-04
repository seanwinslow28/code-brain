---
title: "Probe Design vs. Routing Compliance in Agentic Workflows"
type: concept
sources:
  - knowledge/connections/probe-design-vs-routing-compliance-in-agentic-workflows.md
tags: [auto-generated, phase-6]
created: 2026-07-04
updated: 2026-07-04
---

## Definition

This concept defines a structural tension where agents must choose between executing known linear paths (routing compliance) and discovering unknown problem structures through safe-to-fail experiments (probe design). Routing compliance assumes the solution space is static and fully mapped, allowing for high-throughput execution but failing when the environment shifts. Probe design treats the problem structure itself as the variable to be discovered, requiring slower, iterative feedback loops to distinguish between signal and noise. The mechanism relies on treating failed probes not as errors but as necessary exploration costs that reduce uncertainty about the domain's topology.

## Context

Sean is managing an agent fleet that has grown in complexity (from 3 concepts to 150+ over time). As the number of clusters sampled increases, the cost of blind routing grows. He needs a framework to decide when to stop optimizing for throughput and start optimizing for signal clarity in uncertain environments.

## Evidence

> Linear routing assumes a known structure, while probe design acknowledges that the structure must be discovered through safe-to-fail experiments.

> The error budget must account for the cost of probes that fail to yield signal, treating them as necessary exploration costs rather than pure failures in execution.

## Examples

- Treating a failed probe as an exploration cost rather than a pure failure in execution.
- Shifting optimization goals from throughput to signal clarity in uncertain environments.

## Related Concepts

[[Complexity Override]] [[Agent Fleet Observability Dashboard]] [[SRE Error Budget for Agents]]
