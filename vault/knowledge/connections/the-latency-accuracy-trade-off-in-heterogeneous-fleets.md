---
title: "The Latency-Accuracy Trade-off in Heterogeneous Fleets"
type: connection
connects:
  - Runtime-Model Coupling
  - Benchmarking Artifact
  - System Constraints
created: 2026-06-04
updated: 2026-06-04
---

## Synthesis

The tension between hardware constraints and model capability creates a non-linear trade-off where the 'best' model is not a global optimum but a local optimum defined by the specific tier's memory bandwidth and compute architecture. On Tier C (Alienware RTX 5080), `gemma4:26b` emerges as the superior choice not because it is the most powerful model in absolute terms, but because its MoE architecture (3.8B active) aligns with the 16GB VRAM constraint to deliver 40 tok/s and 80% tool-call accuracy, whereas dense models or mismatched sparse models fail to meet the latency or accuracy thresholds. This pattern implies that fleet optimization requires decoupling model selection from general benchmarks and instead treating each tier as a distinct resource boundary where the 'best' model is the one that maximizes utility within the hard constraints of the hardware.

## Threads

### [[Runtime-Model Coupling]]

> devstral was designed for agentic-coding with native tool-call templates (Mistral-style); the Topic 20 prompt set uses generic JSON schema prompts that may not match devstral's training.

### [[Benchmarking Artifact]]

> Topic 19 §Correction (2026-05-21) flagged that the prior synthesis methodology was biased against newer locally-runnable models.

### [[System Constraints]]

> Topic 20 result on actual hardware (RTX 5080 16 GB): devstral scores 7/20 tool-call schema (35%) — much lower than expected.

## Implications

- Sean should not assume that a model's performance on one tier (e.g., Mac Mini) will translate to another (e.g., Alienware) without re-benchmarking, as the hardware constraints fundamentally alter the effective capability of the model.
- The decision to add `gemma4:26b` to Tier C is driven by the specific balance of active parameters and VRAM, suggesting that future model additions must be evaluated against the specific memory bandwidth of the target tier rather than just parameter count.
