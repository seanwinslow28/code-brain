---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/the-privacy-velocity-trade-off-in-automated-observability.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

Legibility debt accumulates when the drive for operational visibility forces the exposure of sensitive data into public or semi-public channels, bypassing necessary human supervision. This occurs when automation prioritizes the velocity of data extraction over the latency of semantic filtering, creating a gap between what is observable and what is safe to observe. The debt manifests as a growing collection of artifacts that contain high-risk information because the system was designed to be legible rather than secure. This failure mode reveals that supervision cannot be automated away; it must be enforced through structural constraints that prevent sensitive data from entering the observability pipeline in the first place.

## Context

Sean's job-hunt pipeline requires strict semantic isolation, but the agent fleet's need for daily status updates has created a conflict. The `soul-tier-a-conflict` issue kind was introduced to manage this tension, but the underlying mechanism of automated extraction continues to bypass privacy controls. This creates a dependency on manual scrubbing and luck, rather than a robust system that respects the boundary between operational health and strategic secrecy.

## Evidence

> The `soul-tier-a-conflict` issue kind was wired into production by BT5 C3 on 2026-07-05, which is exactly when those reports start.

> There is a fundamental tension between the velocity of automated data extraction and the latency of human-led privacy review.

## Examples

- The introduction of `soul-tier-a-conflict` as a specific issue kind to track conflicts between operational visibility and job-hunt privacy.
- The daily generation of reports by the agent fleet that inadvertently include sensitive SOUL lines due to lack of semantic filtering.

## Related Concepts

[[The Masking Effect of Structural Completeness in Failed Automation]] [[Privacy-Aware Data Routing]]
