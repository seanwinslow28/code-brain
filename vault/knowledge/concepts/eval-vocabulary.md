---
title: "Eval Vocabulary"
type: concept
sources:
  - knowledge/connections/the-tension-between-eval-rigor-and-automation-simplicity.md
tags: [auto-generated, phase-6]
created: 2026-06-29
updated: 2026-06-29
---

## Definition

Eval Vocabulary functions as a semantic contract layer that translates ambiguous human intent into deterministic scoring dimensions before any code generation occurs. This mechanism prevents the compounding of non-determinism by forcing explicit criteria for success, effectively acting as a pre-flight check for agentic workflows. Without this vocabulary, agents operate on implicit assumptions that vary between runs, leading to silent failures that are difficult to debug or reproduce consistently.

## Context

Sean's infrastructure relies on high-fidelity scoring for agentic systems, but many tasks are better served by deterministic pipelines that bypass the need for such rigorous evaluation entirely. Understanding when to apply this vocabulary is critical to avoiding cognitive overload and maintaining automation reliability.

## Evidence

> intent_spec` tool *is* the eval. It scores a spec against the framework's dimensions before that spec reaches a coding agent

> The Eval Vocabulary serves as the critical coordination mechanism between Autonomous Agent Fleets and their dependent systems.

## Examples

- Scoring a spec against the framework's dimensions before it reaches a coding agent

## Related Concepts

[[Automation Reliability]] [[Intent Engineering]]
