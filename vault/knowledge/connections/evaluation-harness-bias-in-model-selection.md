---
title: "Evaluation Harness Bias in Model Selection"
type: connection
connects:
  - Benchmarking Artifact
  - Runtime-Model Coupling
  - Automation Reliability
created: 2026-05-28
updated: 2026-05-28
---

## Synthesis

The tension between native model optimization and generic evaluation formats creates a systematic bias where models are ranked by syntax compatibility rather than functional capability. When Sean selects models for his production fleet based on these biased benchmarks, he risks deploying suboptimal agents that appear reliable but lack the specific agentic skills required for complex tasks. This artifact distorts the signal-to-noise ratio in his model selection process, leading to a 'safe' but potentially less capable production environment.

## Threads

### [[Benchmarking Artifact]]

> When a model is optimized for a specific native template (like Mistral-style tool calls) but evaluated using a generic JSON schema, the resulting accuracy score reflects a format mismatch rather than a lack of functional ability.

### [[Runtime-Model Coupling]]

> Runtime-Model Coupling is the phenomenon where the functional capability of a model is not an intrinsic property of the weights alone, but is strictly gated by the inference engine's co

### [[Automation Reliability]]

> Automation Reliability is the measure of an agent's ability to produce structurally valid outputs consistently across varying environmental conditions. It is undermined by 'silent failu

## Implications

- Sean must audit his benchmarking prompts for format alignment with each model's native training distribution before making fleet decisions.
- He should implement a dual-evaluation strategy that tests both functional capability and syntax compatibility to avoid false negatives.
