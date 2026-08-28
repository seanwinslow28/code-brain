---
title: "Harness Engineering Invariant"
type: concept
sources:
  - knowledge/concepts/harness-engineering-invariant.md
tags: [auto-generated, phase-6]
created: 2026-08-13
updated: 2026-08-13
---

## Definition

This invariant posits that agent reliability is inversely proportional to the complexity of its surrounding harness, as every added tool or permission expands the failure surface non-linearly. The mechanism suggests that simplifying the operational environment (fewer tools, stricter constraints) yields higher semantic fidelity than increasing computational power. When the harness becomes too permissive, the agent drifts into low-judgment modes because it lacks the structural friction necessary to enforce quality standards.

## Context

Sean's recent runs show a correlation between reduced rejection rates and reduced connection depth, implying that his current harness is too permissive for high-quality synthesis. This suggests that upgrading models without pruning tools may degrade performance rather than improve it.

## Evidence

> This invariant posits that agent reliability is inversely proportional to complexity of its surrounding harness, as every added tool or permission expands the failure surface non-linearly.

> Sean should prioritize pruning his synthesizer's toolset and reference files before attempting to upgrade models, as reducing the harness surface area will improve reliability more than raw compute power.

## Examples

- The drop in rejected_count from 78 (qwen3-14b) to 7 (qwen3.6-35b-a3b-32k) despite similar concept counts.
- The increase in duration_seconds from 47s to 1700s as the harness complexity grew with model size.

## Related Concepts

[[Velocity vs. Judgment in MCP Strengthening]] [[The Illusion of Health in Autonomous Systems]]
