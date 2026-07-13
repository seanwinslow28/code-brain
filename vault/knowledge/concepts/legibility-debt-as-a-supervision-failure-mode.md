---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/velocity-vs-legibility-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-13
updated: 2026-07-13
---

## Definition

This invariant describes the structural decay of system trust when automated throughput outpaces the capacity for human verification. As Sean scales concept generation from 3 to 153 items per run, the reporting mechanisms fail to keep pace, creating a gap where status updates become unreliable proxies for actual health. This forces supervision to shift from strategic oversight to forensic debugging, eroding confidence in the system's metrics because the user cannot verify state without manual intervention.

## Context

Sean is actively scaling his agent fleet's output volume while simultaneously observing a drop in reliable status reporting. Understanding this debt is critical because it explains why high-volume runs feel less trustworthy despite producing more artifacts.

## Evidence

> As Sean scales the concept generation from 3 to 153 concepts per run, the mechanisms for reporting status lag behind, creating a legibility gap.

> This forces supervision to shift from strategic oversight to forensic debugging, eroding trust in the system's health metrics because the user cannot verify the system's state without manual intervention.

## Examples

- The jump from 3 concepts (run-2026-05-27) to 153 concepts (run-2026-07-02) coincides with a period where status reporting reliability becomes questionable.
- The shift in supervision style from strategic oversight to forensic debugging as the volume of automated outputs increases.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Agent Fleet Observability Dashboard]]
