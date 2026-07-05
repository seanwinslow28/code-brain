---
title: "Taste as Evaluation Function vs. Activity Proof"
type: concept
sources:
  - knowledge/concepts/taste-as-evaluation-function-vs-activity-proof.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

This mechanism defines the structural tension between quantifiable operational volume and qualitative judgment in automated systems. The system generates 'activity proof' via metrics like 'clusters_sampled' and 'concepts_written', but the actual value is derived from the 'fit_score' which requires nuanced judgment that cannot be fully automated. This creates a dependency where volume must be sufficient to allow taste to operate effectively, but not so high that it dilutes the signal. The mechanism reveals that automation can scale the search space, but it cannot replace the evaluation function that determines value within that space.

## Context

Sean's run data shows increasing 'clusters_sampled' (from 155 to 272) while 'concepts_written' also increases, suggesting an attempt to scale the evaluation function. However, the 'fit_score' remains the ultimate arbiter, meaning that without strong taste, increased activity yields diminishing returns in terms of actual opportunities. This insight is critical for optimizing the job hunt pipeline, as it highlights the need to balance agent throughput with human-in-the-loop calibration.

## Evidence

> The run metrics show a clear increase in 'clusters_sampled' from 155 on 2026-06-23 to 272 on 2026-07-02, indicating a scaling of the evaluation activity.

> The job feed explicitly categorizes roles by 'fit_score' (e.g., '⭐ 3/5', '⭐ 2/5'), which serves as the final evaluation function that overrides raw activity metrics.

## Examples

- On 2026-07-02, the system sampled 272 clusters and wrote 141 concepts, yet only identified 1 medium fit and 5 weak fits, showing the gap between activity volume and high-value outcomes.
- The 'Medium Fits' section lists roles with specific rationales like 'Staff PM title exceeds Sean's eligible bands,' which is a taste-driven evaluation rather than a simple keyword match.

## Related Concepts

[[Job Hunt as Sales Pipeline]] [[Signal vs. Safety Trade-off in Resume Architecture]]
