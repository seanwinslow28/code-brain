---
title: "The Tension Between Eval Rigor and Automation Simplicity"
type: connection
connects:
  - Eval Vocabulary
  - Automation Reliability
  - Intent Engineering
created: 2026-06-29
updated: 2026-06-29
---

## Synthesis

There is a fundamental tension between the need for rigorous evaluation (Eval Vocabulary) and the desire for simple, reliable automations. While evals provide the necessary structure to define success, they can become overly complex if applied to tasks that only require simple automation. This tension arises because Sean's framework demands high-fidelity scoring for agentic systems, but many tasks are better served by deterministic pipelines that bypass the need for such rigorous evaluation entirely.

## Threads

### [[Eval Vocabulary]]

> intent_spec` tool *is* the eval. It scores a spec against the framework's dimensions before that spec reaches a coding agent

### [[Automation Reliability]]

> non-determinism compounding across steps, debugging a thing that behaves differently every run

### [[Intent Engineering]]

> Getting useful intent out of someone who says 'make it pop' is the unsolved 80%

## Implications

- Sean should prioritize building tools that help users identify when evals are unnecessary, reducing cognitive load for simple tasks.
- The 'Agent-or-Automation Advisor' must explicitly address the cost of implementing rigorous evals versus the benefit gained for low-complexity tasks.
