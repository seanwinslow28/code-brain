---
title: "System Constraints"
type: concept
sources:
  - health/tier-c-soak/2026-05-27/2026-05-21-topic-19c-optimal-ollama-models-pi-chatgpt.md
tags: [auto-generated, phase-6]
created: 2026-05-28
updated: 2026-05-28
---

## Definition

System Constraints refers to the hard limits imposed by hardware resources (RAM, VRAM) and software architecture (context windows, streaming protocols) that dictate the feasible operational envelope of an AI agent. These constraints are not merely technical specifications but active determinants of which models can be deployed and how they must be configured to function. The tension arises because the desired capabilities (long context, complex reasoning) often exceed the default capacities of the hardware, requiring specific model architectures or configuration overrides to bridge the gap.

## Context

Sean is evaluating models for different hardware tiers (M4 Max, M4 Pro, RTX 3090). The constraints of each machine directly limit the choice of models and the types of workflows (e.g., long-context summarization vs. fast tool-calling) that are viable. Recognizing these constraints allows for precise hardware-software matching rather than generic model selection.

## Evidence

> This research report identifies the optimal Ollama models for Pi-driven coding and agentic workflows in 2026, categorized by hardware tiers based on available RAM and VRAM.

> The report provides specific model recommendations across three hardware tiers. For Tier A (M4 Max MBP, 48GB), Gemma4:31b is the best overall for agentic reasoning and tool-calling.

> Tier C (RTX 3090/4090, 24GB VRAM) leverages CUDA, suggesting Qwen3.5:35b-A3B-Coding in NVFP4 format for efficient long-context tasks.

## Examples

- Tier A (M4 Max MBP, 48GB) using Gemma4:31b
- Tier B (M4 Pro Mac Mini, 24GB) using Gemma4:26b
- Tier C (RTX 3090/4090, 24GB VRAM) using Qwen3.5:35b-A3B-Coding

## Related Concepts

[[Runtime-Model Coupling]] [[Infrastructure Status]]
