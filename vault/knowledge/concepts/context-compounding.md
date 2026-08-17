---
title: "Context Compounding"
type: concept
sources:
  - knowledge/connections/the-scalability-paradox-in-agentic-creative-workflows.md
tags: [auto-generated, phase-6]
created: 2026-08-16
updated: 2026-08-16
---

## Definition

This mechanism describes the phenomenon where a bloated memory state causes the model to ignore real instructions or critical taste signals due to attention dilution. As the context window fills with accumulated data, clusters, and previous outputs, the signal-to-noise ratio drops, leading to a degradation in instruction following. The model does not fail because it lacks information, but because it cannot prioritize the most relevant constraints amidst the compounding weight of irrelevant history. This creates a hidden dependency where system performance is inversely proportional to memory size.

## Context

Sean’s runs show that as clusters sampled and concepts written increase, the duration and rejection counts also rise, suggesting that the model is struggling to process the growing context. The 'bloated memory' directly interferes with the agent's ability to adhere to the specific taste constraints required for high-quality synthesis.

## Evidence

> A bloated memory makes the model ignore the real instructions.

> As Sean scales the concept generation, the system generates more data but loses the specific 'taste' signals that define his creative voice.

## Examples

- The synthesis notes that a 'bloated memory' causes the model to ignore instructions, directly linking context size to instruction failure.
- Sean’s runs with higher clusters sampled (e.g., 186x) show increased rejection counts (36), indicating that the compounding context is causing the model to deviate from taste constraints.

## Related Concepts

[[Throughput vs. Taste Memory Tension]] [[The Taste-Fidelity Decoupling in Creative Production]]
