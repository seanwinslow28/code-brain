---
title: "Benchmark Bias vs. Infrastructure Expansion"
type: connection
connects:
  - Benchmarking Artifact
  - Infrastructure Status
  - Runtime Constraint
created: 2026-05-27
updated: 2026-05-27
---

## Synthesis

The tension between benchmark bias and infrastructure expansion reveals a critical flaw in Sean's model selection process: the new Tier C infrastructure is being populated with a model (gemma4) that is only 'best' because the benchmark methodology systematically disadvantaged the superior candidate (devstral). This creates a situation where Sean's new hardware investment is immediately suboptimal, not due to hardware limitations, but due to a methodological error in the evaluation. The consequence is that his production fleet is built on a false premise of optimality, potentially limiting his agentic capabilities until the benchmark is corrected or devstral is re-evaluated with appropriate prompts.

## Threads

### [[Benchmarking Artifact]]

> devstral was designed for agentic-coding with native tool-call templates (Mistral-style); the Topic 20 prompt set uses generic JSON schema prompts that may not match devstral's training.

### [[Infrastructure Status]]

> Tier C | Alienware RTX 5080 16 GB | (none — new tier) | gemma4:26b (MoE 3.8 B active) | ADD as new Tier C production model.

### [[Runtime Constraint]]

> qwen3-14b stays — no candidate beats it on the LM Studio runtime

## Implications

- Sean should re-evaluate devstral using Mistral-style prompts before finalizing Tier C deployment, as the current benchmark may be misleading.
- The 'best balance' claim for gemma4 is contingent on the flawed benchmark, meaning the actual best model for Tier C might be devstral if evaluated correctly.
- Future benchmarks must account for model-specific prompt templates to avoid systematic bias against specialized models.
