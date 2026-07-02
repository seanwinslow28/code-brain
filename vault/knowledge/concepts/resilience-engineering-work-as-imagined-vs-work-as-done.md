---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/expansions/control-plane-data-plane-split-for-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

This concept defines the structural gap between the control surface an operator believes they are managing and the actual state of the underlying system. In agent fleets, the manifest JSON, daily notes, and dashboard widgets serve as representations that distort reality rather than mirroring it. When these representations become stale or overly optimistic, operators develop false confidence because the visible workflow appears stable while the backstage processes have failed silently.

## Context

Sean's vault relies on automated agents to maintain his knowledge infrastructure. If he trusts the manifest or dashboard without verifying the underlying data plane, he risks making decisions based on a 'work-as-imagined' state that no longer exists, leading to silent failure propagation in his job hunt and creative workflows.

## Evidence

> operators never touch the real system directly; they act through representations

> the daily note, manifest JSON, Obsidian graph, spend logs, and launchd status are not 'observability extras'

> what distortion does it introduce, what action does it enable, and what false confidence might it create

## Examples

- The manifest JSON showing a successful run while the actual file write failed due to a permission error
- A dashboard widget displaying green status for an agent that is actually stuck in a retry loop
- The daily note appearing complete when the synthesizer skipped critical connections due to token limits

## Related Concepts

[[Control Plane / Data Plane Split for Agent Fleets]] [[The Illusion of Health in Autonomous Systems]] [[Fleet Status]]
