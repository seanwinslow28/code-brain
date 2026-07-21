---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/concepts/legibility-debt-as-a-supervision-failure-mode.md
tags: [auto-generated, phase-6]
created: 2026-07-21
updated: 2026-07-21
---

## Definition

Legibility debt is the structural gap that emerges when automated concept generation throughput outpaces the human capacity for semantic verification, creating a false equivalence between operational activity and perceived value. This debt accumulates silently because standard observability metrics track volume rather than trust, allowing the system to appear healthy while the user's ability to validate its output degrades into an unsustainable forensic mode of supervision. The mechanism relies on the user mistaking high cluster sampling counts for meaningful insight, forcing them to abandon the tool not due to failure, but due to the inability to confirm its worth without manual intervention.

## Context

Sean's fleet runs have demonstrated a dramatic increase in concepts written (from 3 to 153) while his ability to verify them has not scaled proportionally. This creates a specific risk where he abandons the tool not because it fails, but because he can no longer confirm its worth without manual intervention.

## Evidence

> As Sean scales the concept generation from 3 to 153 concepts per run, the mechanisms for reporting status lag behind, creating a legibility gap.

> Robust protocol instrumentation masks epistemic blindness, creating an illusion of health that is particularly dangerous in creative contexts.

## Examples

- The jump from 3 concepts written in May to 153 in July represents a 50x increase in output volume without a corresponding increase in verification capacity.
- The 'illusion of health' where high cluster sampling counts (e.g., 272 clusters) mask the fact that only 40 connections were successfully written.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Agent Fleet Observability Dashboard]]
