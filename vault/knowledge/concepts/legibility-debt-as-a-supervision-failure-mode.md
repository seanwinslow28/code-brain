---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/velocity-vs-legibility-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-22
updated: 2026-07-22
---

## Definition

Legibility debt is the accumulating gap between the volume of automated output and the human capacity to verify its semantic integrity, forcing supervision into inefficient forensic mode. As agent fleets scale their sampling capacity beyond manual verification thresholds, the system generates more data than can be meaningfully processed, leading to a loss of confidence in the tool's utility. This debt manifests not as system failure, but as a gradual erosion of trust where the user can no longer distinguish between valuable insight and automated noise without exhaustive manual auditing.

## Context

Sean's transition from small runs (3 concepts) to large runs (153 concepts) illustrates this debt; the mechanisms for reporting status lag behind the output volume, making it impossible for him to maintain a clear mental model of what is actually being stored in his vault.

## Evidence

> As Sean scales the concept generation from 3 to 153 concepts per run, the mechanisms for reporting status lag behind, creating a legibility gap.

> Sean must treat manual tickets as the single source of truth for system health, rather than a reflection of agent activity.

## Examples

- The jump from 45 concepts in June to 153 in early July represents a tipping point where Sean can no longer manually verify the quality of every cluster sampled.
- The reliance on 'rejected_count' as a proxy for health is insufficient because it does not capture the semantic quality of the accepted outputs.

## Related Concepts

[[Taste as Evaluation Function vs. Activity Proof]] [[The Verification-Governance Inversion]]
