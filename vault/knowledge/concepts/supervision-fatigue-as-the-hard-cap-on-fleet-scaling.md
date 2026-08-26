---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - knowledge/connections/the-automation-paradox-in-personal-knowledge-infrastructure.md
tags: [auto-generated, phase-6]
created: 2026-08-25
updated: 2026-08-25
---

## Definition

Scaling agent fleets increases the volume of 'healthy' outputs, which in turn increases the cognitive load required to filter signal from noise. The mechanism is a feedback loop where each additional agent adds a layer of verification overhead for the user. When the cost of verifying an agent's output exceeds the value of that output, the user stops supervising, leading to either unmonitored drift or complete abandonment of the fleet. This creates a hard cap on scalability because human attention is the bottleneck, not compute.

## Context

Sean's vault synthesizer runs show a progression from 3 concepts (May) to 122 concepts (August). The increase in output volume correlates with an increase in 'rejected_count' and duration. If Sean cannot scale his supervision capacity linearly with agent output, the fleet becomes a liability rather than an asset.

## Evidence

> When agents prioritize completing runs over generating meaningful progress, the user becomes trapped in a loop of supervising healthy but useless outputs.

> The cost of monitoring is weighed against the loss of creative momentum during failures.

## Examples

- The run-2026-07-01T02-30-02.md shows 125 concepts written and 76 rejected, indicating a high-volume, high-noise state requiring significant supervision.
- The run-2026-08-20T02-30-06.md shows 122 concepts written, but the 'lessons remembered' context suggests this is near the limit of Sean's ability to process without fatigue.

## Related Concepts

[[Operational Uptime vs. Cognitive Utility Tension]] [[The Illusion of Health in Autonomous Systems]]
