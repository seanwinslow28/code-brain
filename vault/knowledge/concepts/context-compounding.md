---
title: "Context Compounding"
type: concept
sources:
  - knowledge/concepts/context-compounding.md
tags: [auto-generated, phase-6]
created: 2026-08-30
updated: 2026-08-30
---

## Definition

Long-horizon autonomous tasks suffer from structural context decay where accumulated irrelevance and contradictions silently degrade plan quality over time. This creates a hard limit on agent performance that cannot be solved by larger models alone, but requires explicit scope constraints to match the honest capacity of the context window. Agents must implement active pruning or summarization mechanisms to prevent this silent degradation from poisoning downstream decisions.

## Context

Sean's personal knowledge vault and fleet memory index rely on accurate context retention across thousands of runs. Understanding context decay helps him design better retrieval strategies and manage the 'poison' that accumulates in long-running agent chains, ensuring his automated systems remain reliable rather than drifting into confident falsity.

## Evidence

> Over long tasks, context accumulates irrelevance, contradictions, and poison; plan quality degrades with horizon length.

> Scope harness tasks to what context can hold honestly — long-horizon autonomy claims deserve your M1 skepticism about stocks (context is a stock; its quality drains).

## Examples

- RAG as a system, not a feature. Retrieval-augmented generation bolts a retrieval loop onto generation.
- Its failure modes are systemic: incomplete or contradictory context in → confident falsity out.

## Related Concepts

[[The Context-Memory Bottleneck in Personalized AI]] [[Silent Decay in Strategic Pipelines]]
