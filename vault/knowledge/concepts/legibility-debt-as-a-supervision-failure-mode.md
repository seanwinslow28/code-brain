---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/velocity-vs-legibility-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-14
updated: 2026-07-14
---

## Definition

This pattern describes the structural decay of operational trust that occurs when automated throughput outpaces the human operator's capacity for semantic verification. As the volume of generated artifacts increases, the signal-to-noise ratio in status reporting degrades, forcing supervision to shift from strategic oversight to forensic debugging. The system appears healthy because it is active, but the user cannot verify the quality or relevance of the output without manual intervention, creating a hidden debt that must be paid later.

## Context

Sean's fleet has scaled from 3 concepts per run to over 150, yet his ability to manually audit each concept has not scaled linearly. This creates a dangerous gap where he assumes the system is working because it is running, but he cannot confirm the value of the work until it is too late to correct course efficiently.

## Evidence

> As Sean scales the concept generation from 3 to 153 concepts per run, the mechanisms for reporting status lag behind, creating a legibility gap.

> This forces supervision to shift from strategic oversight to forensic debugging, eroding trust in the system's health metrics because the user cannot verify the system's state without manual intervention.

## Examples

- The jump from 3 concepts written on 2026-05-27 to 153 concepts written on 2026-07-05, while duration increased only from 47s to 2728s, indicates a massive increase in automation density without proportional increases in human-readable insight.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Agent Fleet Observability Dashboard]]
