---
title: "Constraint-First Automation vs. General Efficiency"
type: concept
sources:
  - 20_projects/research/2026-08-29-software-factory-lit-delta/sweep-companies.md
tags: [auto-generated, phase-6]
created: 2026-09-01
updated: 2026-09-01
---

## Definition

Reliability in agentic systems is achieved by placing LLMs into contained boxes with strict deterministic boundaries, rather than optimizing for general-purpose flexibility. By pre-warming environments, capping CI iterations, and using curated tool subsets, the system prevents error amplification. This approach treats constraints not as limitations on capability, but as essential components of a robust production pipeline that compounds reliability through confinement.

## Context

Sean's 'Fleet Memory Index' and 'vault_synthesizer' runs show varying success rates based on model capacity and context management. Applying constraint-first principles—such as capping iterations and pre-gathering context—can stabilize his automated synthesis processes, reducing the 'rejected_count' and improving the consistency of his knowledge vault updates.

## Evidence

> Putting LLMs into contained boxes compounds reliability

> Standardized on Cursor's rule format, synced across Claude Code and minions

> diminishing marginal returns if an LLM is running against indefinitely many rounds

## Examples

- Stripe uses a 'smaller box' subset of tools for agents to reduce errors compared to the full 500-tool Toolshed.
- Runs on isolated devboxes pre-warmed in ~10 seconds with local linting less than five seconds.

## Related Concepts

[[Context Management as a Bottleneck]] [[The Calibration Bottleneck in Scalable Creative Production]]
