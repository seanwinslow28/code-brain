---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/velocity-vs-legibility-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-09
updated: 2026-07-09
---

## Definition

Legibility debt emerges when the velocity of automated execution outpaces the capacity of reporting mechanisms to reflect system state accurately. This creates a gap where high-volume output masks underlying instability, forcing human supervisors to shift from strategic oversight to forensic debugging. The resulting erosion of trust occurs because health metrics appear robust while epistemic blindness grows, making it difficult to distinguish between genuine progress and silent failure propagation.

## Context

Sean is scaling his agent fleet's concept generation from 3 to over 150 per run, yet the reporting infrastructure remains static. This mismatch means that as throughput increases, the visibility into quality and correctness decreases, creating a dangerous illusion of health where errors are hidden by volume rather than exposed by scrutiny.

## Evidence

> As Sean scales the concept generation from 3 to 153 concepts per run, the mechanisms for reporting status lag behind, creating a legibility gap.

> Robust protocol instrumentation masks epistemic blindness, creating an illusion of health that is particularly dangerous in creative contexts.

## Examples

- The jump from 3 concepts written in May to 153 in July with only marginal improvements in rejection rates indicates a scaling bottleneck in supervision.
- Automated dashboards highlighting successful completions while ignoring missing data creates a false sense of operational stability.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Agent Fleet Observability Dashboard]]
