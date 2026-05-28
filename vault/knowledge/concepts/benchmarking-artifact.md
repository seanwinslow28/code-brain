---
title: "Benchmarking Artifact"
type: concept
sources:
  - knowledge/expansions/benchmarking-artifact.md
tags: [auto-generated, phase-6]
created: 2026-05-28
updated: 2026-05-28
---

## Definition

A benchmarking artifact functions as a validity-threat taxonomy that classifies measurement failures by construct, internal, external, or statistical conclusion validity rather than merely reporting a score. This mechanism shifts the diagnostic focus from model capability to the structural integrity of the evaluation harness itself. By treating the benchmark prompt format as an interface contract, the artifact exposes the compatibility gap between model-native affordances and evaluator expectations. The core invariant is that a score is invalid if the harness violates construct validity, regardless of the model's performance within that specific constraint.

## Context

Sean needs to distinguish between a model failing a task and a test measuring the wrong capability. This distinction is critical for fleet decision records where the conclusion must be precise about whether the failure is a model defect or a test design flaw. Without this taxonomy, Sean risks optimizing for proxy metrics that collapse under Goodhart's Law once they guide deployment decisions.

## Evidence

> Your current concept names the artifact but does not classify which kind of invalidity is happening.

> This score is invalid because the harness violates construct validity, not because the model failed.

> Treat every benchmark prompt format as an API/interface contract, not a neutral measurement environment.

> Once benchmark scores guide deployment, models and humans optimize to the proxy, and the proxy stops representing capability.

## Examples

- A reusable benchmark postmortem template that concludes 'the test measured JSON-template compliance instead of agentic tool competence.'
- An eval adapter spec for Tier C model selection where Mistral-style tool calls, OpenAI function calls, and plain JSON schema are explicit subtypes with behavioral guarantees.

## Related Concepts

[[Runtime-Model Coupling]] [[Eval Vocabulary]]
