---
title: "Context Compounding"
type: concept
sources:
  - knowledge/connections/the-scalability-paradox-in-agentic-creative-workflows.md
tags: [auto-generated, phase-6]
created: 2026-07-14
updated: 2026-07-14
---

## Definition

This pattern occurs when the accumulation of memory artifacts exceeds the model's effective attention window, causing it to ignore critical instructions or recent context. A bloated memory makes the model ignore the real instructions, leading to outputs that are technically correct but contextually irrelevant. This compounding effect worsens over time as the vault grows, requiring active pruning strategies to maintain operational clarity. The mechanism highlights the non-linear cost of memory in agentic systems.

## Context

Sean's runs show increasing duration and cluster sampling counts, which likely contribute to context bloat. Understanding this helps him manage the lifecycle of his knowledge vault to prevent performance degradation.

## Evidence

> A bloated memory makes the model ignore the real instructions.

> The value of the 'Creative Partner' is contingent on the agent's ability to prune irrelevant taste signals, not just accumulate them.

## Examples

- Run 2026-07-01 sampled 236 clusters and wrote 125 concepts, a high volume that likely strained context retention compared to later runs with fewer samples.

## Related Concepts

[[Throughput vs. Taste Memory Tension]] [[Memory Rot and Lifecycle Management]]
