---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - knowledge/index.md
tags: [auto-generated, phase-6]
created: 2026-09-16
updated: 2026-09-16
---

## Definition

This mechanism defines the limit at which human oversight becomes the bottleneck for automated systems. As the volume of agent-generated artifacts increases, the cognitive load required to verify their semantic integrity grows faster than the automation’s ability to self-correct. The 'hard cap' is reached when the time spent reviewing and correcting agent output exceeds the time saved by automating it in the first place, forcing a reduction in throughput or a switch to lower-fidelity models.

## Context

Sean’s daily drive agents rely on the synthesizer for context. If the synthesizer produces too much noise (high rejection/low quality), Sean must spend more time curating the vault manually. The data shows that as the synthesizer scaled up in July/August, the 'rejected_count' spiked, implying a higher burden of review or a system struggling to maintain standards without human intervention.

## Evidence

> run-2026-08-15T02-30-05.md: concepts_written: 123, connections_written: 43, clusters_sampled: 186, rejected_count: 36

> run-2026-07-06T02-30-06.md: model_used: qwen3.6-35b-a3b-32k, concepts_written: 103, connections_written: 47, clusters_sampled: 193, rejected_count: 106

> run-2026-06-29T02-30-04.md: model_used: qwen3-14b, concepts_written: 109, connections_written: 49, clusters_sampled: 253, rejected_count: 76

## Examples

- The June 29th run with qwen3-14b sampled 253 clusters and rejected 76, showing that even smaller models struggled with high-volume semantic filtering.
- The August 15th run maintained a lower rejection rate (36) but still processed 186 clusters, suggesting a tuning of parameters to avoid the fatigue trap seen in July.

## Related Concepts

[[The Efficiency-Quality Inversion in Automated Synthesis]] [[Legibility Debt as a Supervision Failure Mode]]
