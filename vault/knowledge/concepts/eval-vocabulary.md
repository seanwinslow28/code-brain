---
title: "Eval Vocabulary"
type: concept
sources:
  - 40_knowledge/references/ref-agent-product-analytics-runs-not-sessions.md
tags: [auto-generated, phase-6]
created: 2026-05-29
updated: 2026-05-29
---

## Definition

A structured set of metrics and events that define the boundaries of agent autonomy, specifically distinguishing between task completion and user acceptance. This vocabulary requires instrumenting the correction loop, where user feedback becomes eval cases that refine the roadmap. It establishes that a workflow has earned autonomy only when the rate of user correction drops below a specific threshold. The mechanism relies on real-time telemetry of the agent's internal state rather than just the final output.

## Context

Sean is developing a 'Vault Synthesizer Eval Suite' and needs to define what 'good' looks like for his own agents. By adopting this vocabulary, he can objectively measure the reliability of his automation pipelines and demonstrate product sense in his job hunt by showing how he measures trust, not just uptime.

## Evidence

> The difference between a task that finished and a task the user trusted. Reading that one gap is how you tell which workflows have earned more autonomy.

> The three events to ship this week, the full event schema underneath them, and the prompts that turn that schema into instrumentation in your own stack, your corrections into eval cases, and your numbers into a roadmap.

## Examples

- Using user_correction_submitted as a primary signal for evaluating workflow reliability.

## Related Concepts

[[Agentic Engineering Signal]] [[Vault Synthesizer Eval Suite]]
