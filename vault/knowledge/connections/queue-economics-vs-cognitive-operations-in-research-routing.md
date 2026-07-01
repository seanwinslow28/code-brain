---
title: "Queue Economics vs. Cognitive Operations in Research Routing"
type: connection
connects:
  - Deep Research Queue
  - Negative Capability / Failure Literacy
  - Gemini Deep Research
created: 2026-07-01
updated: 2026-07-01
---

## Synthesis

The fundamental tension exists between managing research as a throughput problem governed by queue economics and treating it as a cognitive stage problem requiring specific sensemaking loops. Queue economics demands visibility into arrival rates and WIP to prevent policy theater, while cognitive operations require precise matching of task type to model capability. The consequence is that Sean cannot effectively manage his research fleet without integrating both views; optimizing for speed in the wrong cognitive stage leads to wasted tokens and poor outputs, while ignoring capacity limits results in systemic bottlenecks.

## Threads

### [[Deep Research Queue]]

> A research route is healthy only if arrival rate, service time, and WIP are all visible; otherwise ‘use Gemini for compound topics’ is policy theater.

### [[Negative Capability / Failure Literacy]]

> Do not route by model first; route by cognitive operation: forage, triage, cluster, contradict, synthesize, package.

### [[Gemini Deep Research]]

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[gemini-deep-research]].

## Implications

- Sean must implement a dashboard metric combining WIP age and completion rate to validate routing policies against actual throughput.
- Agent specs must declare their intended cognitive operation before selecting a model, preventing misalignment between task type and tool capability.
- Failure labels in the Vault Critic must distinguish between capacity exhaustion (queue issue) and stage mismatch (cognitive issue).
