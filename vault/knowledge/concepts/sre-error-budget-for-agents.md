---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/connections/the-tension-between-reliability-metrics-and-adaptive-capacity-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-03
updated: 2026-07-03
---

## Definition

This concept establishes a quantitative threshold for acceptable agent failure, treating creative or operational errors as a finite resource that must be managed against operator attention costs. It defines health not by the absence of errors, but by the stability of the ratio between error frequency and the human effort required to resolve them. The mechanism enforces discipline by forcing engineers to choose between accelerating feature development (burning budget) or investing in reliability engineering (saving budget). This invariant prevents the infinite optimization of edge cases that yields diminishing returns.

## Context

Sean can use this framework to justify why his agents are not 'perfect' but are instead 'cost-effective.' It provides a professional vocabulary for discussing trade-offs with hiring managers who value operational maturity over naive perfectionism. By defining his error budget, he demonstrates an ability to make strategic decisions about where reliability engineering investment is actually needed.

## Evidence

> A creative agent is not healthy when it succeeds once; it is healthy when its failure rate, recovery path, and operator attention cost stay inside an explicit error budget.

> The consequence is that his portfolio must evolve from a collection of working scripts to a demonstration of how his agents stretch under failure.

## Examples

- Calculating the hours saved by automation versus the hours spent debugging it over a month.
- Setting a limit on how many times an agent can retry a failed API call before alerting a human.

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Agent Health Monitoring]]
