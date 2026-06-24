---
title: "Automation Reliability"
type: concept
sources:
  - knowledge/connections/the-tension-between-eval-rigor-and-automation-simplicity.md
tags: [auto-generated, phase-6]
created: 2026-06-24
updated: 2026-06-24
---

## Definition

Automation Reliability is the property of a system where deterministic pipelines prevent non-determinism from compounding across sequential steps. It relies on minimizing the surface area for failure by avoiding complex evaluation layers when simple, predictable outcomes are sufficient. When reliability is compromised, debugging becomes impossible because the system behaves differently in every run, creating an invisible dependency chain.

## Context

Sean's daily drive agents must function without silent failures that disrupt his morning brief or status updates, making reliability a core infrastructure concern.

## Evidence

> non-determinism compounding across steps, debugging a thing that behaves differently every run

> The tension lies between the chaotic, asynchronous nature of agent interactions and the need for deterministic, consistent outcomes in Sean's product architectures.

## Examples

- Debugging a thing that behaves differently every run

## Related Concepts

[[Eval Vocabulary]] [[Silent Failure Propagation in Agent Fleets]]
