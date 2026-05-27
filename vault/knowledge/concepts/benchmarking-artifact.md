---
title: "Benchmarking Artifact"
type: concept
sources:
  - 20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md
tags: [auto-generated, phase-6]
created: 2026-05-27
updated: 2026-05-27
---

## Definition

A benchmarking artifact is a measurement result that captures the performance of a model under a specific, constrained prompt format, which may systematically misrepresent the model's true capabilities if the format does not align with its training distribution. When a model is optimized for a specific native template (like Mistral-style tool calls) but evaluated using a generic JSON schema, the resulting accuracy score reflects a format mismatch rather than a lack of functional ability. This creates a false negative in the evaluation process, where a high-performing model is incorrectly ranked lower than a mediocre model simply because the latter happens to match the evaluation prompt's syntax better. The artifact is not a measure of the model's intrinsic quality, but a measure of its compatibility with the specific evaluation harness.

## Context

This matters to Sean because his production fleet decisions rely on these benchmarks to select models for Tier C. If the benchmark is biased against models like devstral due to prompt mismatch, he risks deploying a suboptimal model (gemma4) simply because the evaluation methodology failed to surface devstral's true potential. This leads to a 'safe' but potentially less capable production environment.

## Evidence

> devstral was designed for agentic-coding with native tool-call templates (Mistral-style); the Topic 20 prompt set uses generic JSON schema prompts that may not match devstral's training.

> devstral scores 7/20 tool-call schema (35%) — much lower than expected.

## Examples

- devstral scores 7/20 tool-call schema (35%) — much lower than expected.
- Topic 19 Tier C recommendation: devstral:24b-small-2505-q4_K_M (~40–55 tok/s, "highest agentic-coding score").

## Related Concepts

[[Agent Health]] [[Infrastructure Status]]
