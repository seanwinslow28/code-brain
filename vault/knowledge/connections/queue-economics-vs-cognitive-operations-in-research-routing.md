---
title: "Queue Economics vs. Cognitive Operations in Research Routing"
type: connection
connects:
  - Deep Research Queue
  - Negative Capability / Failure Literacy
  - Gemini Deep Research
created: 2026-06-30
updated: 2026-06-30
---

## Synthesis

The tension lies between treating research as a throughput problem (queue economics) versus a cognitive stage problem (sensemaking loops). Queue economics focuses on visibility of arrival rates and WIP to prevent policy theater, while sensemaking loops focus on matching the tool to the specific cognitive operation like foraging or synthesis. The consequence is that Sean cannot effectively manage his research fleet without both metrics: throughput data tells him when to batch or defer, while cognitive labels tell him why a specific output failed. Without integrating these two views, he risks optimizing for speed in the wrong cognitive stage or ignoring capacity limits while chasing perfect sensemaking.

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
