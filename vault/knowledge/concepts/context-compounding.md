---
title: "Context Compounding"
type: concept
sources:
  - knowledge/concepts/context-compounding.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

This mechanism describes a non-linear value accumulation where an agent's output quality scales with task duration and complexity, contingent on maintaining coherent state across long operational horizons. Unlike simple task completion which resets context at each step, this pattern requires the agent to iteratively refine hypotheses and build upon previous steps without losing track of the original intent. The primary bottleneck is not computational power but the model's ability to retain and synthesize information over weeks of continuous operation, preventing output degradation into noise.

## Context

Sean's 'Deep Research Queue' and 'Creative Studio Workflows' require agents to work on open-ended tasks for days or weeks. If the system cannot compound context effectively, the output degrades into noise, making long-horizon automation impossible and forcing a return to manual, linear workflows.

## Evidence

> the kind of thing that can make progress on open ended tasks for weeks on end in the face of errors and mistakes and ambiguity.

> what really matters is how smart and general and sample efficient the model is during a session.

## Examples

- A research agent building a comprehensive market analysis over 48 hours by iteratively refining its thesis.
- A creative assistant developing a narrative arc across multiple drafting sessions without losing character consistency.

## Related Concepts

[[Context Management as a Bottleneck]] [[Memory Rot and Lifecycle Management]]
