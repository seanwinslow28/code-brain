---
title: "Harness Engineering Invariant"
type: concept
sources:
  - knowledge/connections/velocity-vs-judgment-in-mcp-strengthening.md
tags: [auto-generated, phase-6]
created: 2026-07-22
updated: 2026-07-22
---

## Definition

This invariant posits that agent reliability is inversely proportional to the complexity of its surrounding harness, as every added tool, permission, or reference file expands the failure surface non-linearly. The mechanism involves the introduction of new variables that the agent must manage simultaneously, increasing the probability of context drift or instruction following errors. Simplifying the harness by removing redundant tools often yields greater reliability gains than upgrading the underlying model.

## Context

Sean is considering upgrading models to improve output quality, but the data suggests that reducing the harness complexity (e.g., fewer clusters sampled, less noise) might be more effective. He needs to audit his synthesizer's toolset to identify which components are contributing to the 'illusion of health' rather than actual semantic value.

## Evidence

> This invariant posits that agent reliability is inversely proportional to complexity of its surrounding harness, as every added tool or permission expands the failure surface non-linearly.

> Sean should prioritize pruning his synthesizer's toolset and reference files before attempting to upgrade models, as reducing the harness surface area will improve reliability more than raw compute power.

## Examples

- The reduction in 'clusters_sampled' from ~250 (qwen3-14b era) to ~150 (qwen3.6-35b era) coinciding with a drop in 'rejected_count' suggests that limiting input scope improved output quality.
- The duration of runs remained relatively stable (~1700s) despite model changes, indicating that the bottleneck is not compute time but the complexity of the decision-making process within the harness.

## Related Concepts

[[Velocity vs. Judgment in MCP Strengthening]] [[The Illusion of Health in Autonomous Systems]]
