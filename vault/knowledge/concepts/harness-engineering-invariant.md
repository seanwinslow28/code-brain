---
title: "Harness Engineering Invariant"
type: concept
sources:
  - knowledge/connections/maintenance-surface-vs-model-capability-trade-off.md
tags: [auto-generated, phase-6]
created: 2026-07-21
updated: 2026-07-21
---

## Definition

This invariant posits that an agent's reliability is inversely proportional to the complexity of its surrounding harness, as every added tool, permission, or reference file expands the failure surface non-linearly. The mechanism suggests that increasing capability through expansion inevitably degrades stability because the model cannot compensate for the combinatorial explosion of potential interaction points. Consequently, pruning the harness often yields greater reliability gains than upgrading the model's raw intelligence.

## Context

Sean's transition from qwen3-14b to qwen3.6-35b did not solve his quality issues because the larger model operated within a complex harness that masked underlying drift. He must prioritize reducing the number of tools and reference files to stabilize the synthesizer before attempting further capability upgrades.

## Evidence

> This invariant posits that agent reliability is inversely proportional to complexity of its surrounding harness, as every added tool or permission expands the failure surface non-linearly.

> There is a fundamental tension between increasing an agent's capability by adding tools and maintaining its reliability, as the harness complexity grows faster than model intelligence can compensate.

## Examples

- The synthesizer sampling 253 clusters but writing only 109 concepts, indicating that the harness complexity overwhelmed the model's ability to filter effectively.
- Upgrading from qwen3-14b to qwen3.6-35b while maintaining a large toolset resulted in higher rejection counts rather than improved semantic quality.

## Related Concepts

[[Maintenance Surface vs. Model Capability Trade-off]] [[Context Management as a Bottleneck]]
