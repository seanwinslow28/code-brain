---
title: "Context Compounding"
type: concept
sources:
  - knowledge/concepts/context-compounding.md
tags: [auto-generated, phase-6]
created: 2026-07-09
updated: 2026-07-09
---

## Definition

Context compounding is a cognitive load phenomenon where the accumulation of prior context windows dilutes the weight of new, critical instructions. As the memory core grows through repeated agent runs, the model's attention mechanism is forced to distribute focus across an expanding set of historical data points. This causes the 'real instructions' to lose their relative importance, leading to a systemic failure in following specific taste constraints.

## Context

Sean observes that as his vault expands, the synthesizer begins to ignore explicit taste directives because they are buried under layers of accumulated, unpruned context from previous runs. This creates a tension between the desire for comprehensive memory and the need for precise, high-fidelity execution in creative production.

## Evidence

> A bloated memory makes the model ignore the real instructions.

> A cognitive load phenomenon where the accumulation of prior context windows dilutes the weight of new, critical instructions.

## Examples

- Runs with 250+ clusters sampled showing a drop in connection quality or relevance, as the model struggles to prioritize recent taste signals over older data.
- The 'rejected_count' metric spiking when the context window exceeds the model's effective attention span for specific taste constraints.

## Related Concepts

[[Memory Rot and Lifecycle Management]] [[The Taste-Fidelity Decoupling in Creative Production]]
