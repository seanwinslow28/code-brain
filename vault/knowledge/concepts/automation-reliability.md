---
title: "Automation Reliability"
type: concept
sources:
  - knowledge/connections/the-tension-between-eval-rigor-and-automation-simplicity.md
tags: [auto-generated, phase-6]
created: 2026-06-29
updated: 2026-06-29
---

## Definition

Automation reliability is defined by the stability of outputs across repeated executions, where non-determinism compounding across steps creates debugging challenges that are fundamentally different from static code bugs. When agents behave differently every run, the system loses its deterministic nature, making it impossible to establish a baseline for performance or trust. This instability arises not from logic errors but from the inherent variance in model outputs and context window fluctuations.

## Context

Sean's framework demands high-fidelity scoring for agentic systems, but many tasks are better served by deterministic pipelines that bypass the need for such rigorous evaluation entirely. The tension lies in balancing the need for reliable automation with the complexity of managing non-deterministic agents.

## Evidence

> non-determinism compounding across steps, debugging a thing that behaves differently every run

> The core tension lies in the conflict between Sean's need for rigorous, automated feedback loops (instrumentation) and the inherent ambiguity of human-centric evaluation criteria

## Examples

- Debugging a thing that behaves differently every run

## Related Concepts

[[Eval Vocabulary]] [[Intent Engineering]]
