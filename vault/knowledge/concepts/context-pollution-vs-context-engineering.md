---
title: "Context Pollution vs. Context Engineering"
type: concept
sources:
  - knowledge/concepts/context-pollution-vs-context-engineering.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

This mechanism identifies the failure mode where increasing the volume of injected context degrades agent performance because the signal-to-noise ratio drops below the threshold for coherent reasoning. It is not merely about token limits, but about the cognitive load of filtering irrelevant 'world' slices. True context engineering requires curating only the relevant slice of the legible world for the present decision, whereas context pollution occurs when the system dumps all available state into the inference window, treating volume as a proxy for completeness.

## Context

Sean's vault is growing rapidly with daily notes, research transcripts, and project files. Without strict curation, his agents will begin to hallucinate or ignore instructions because the 'legible world' has become too noisy. This concept warns against the intuitive but fatal mistake of assuming more data equals better performance in agentic workflows.

## Evidence

> Dumping every meeting, document, memory, and policy into every inference is not context engineering. It is context pollution.

> The central technical problem in Troyanovsky’s worldview is what I would call discontinuous cognition.

## Examples

- An agent tasked with summarizing a project fails because it gets distracted by irrelevant details from a 2024 email thread included in the context window.
- A synthesizer produces a coherent summary only after the system explicitly filters out all non-project-specific memory files before inference.

## Related Concepts

[[The Context-Memory Bottleneck in Personalized AI]] [[Legibility Debt as a Supervision Failure Mode]]
