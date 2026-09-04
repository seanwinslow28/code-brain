---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-09-04
updated: 2026-09-04
---

## Definition

Legibility debt accumulates when the mechanisms used to monitor or execute automated tasks become increasingly opaque to human oversight, creating a gap between what the system is doing and what the operator can verify. This debt manifests as a reliance on indirect signals (like cost metrics or success flags) rather than direct inspection of the work product, forcing the operator to reconstruct the state of the system from fragmented logs or secondary artifacts. The consequence is that supervision becomes reactive and costly, as errors are only detected after they have propagated through the pipeline.

## Context

Sean's manual tickets reveal a growing need to manually audit and 'sweep' retired author-mode vocabulary and orphaned files because the automated registry does not scan them. This indicates that his current observability tools are failing to provide a complete picture of his creative infrastructure, forcing him to perform manual reconciliation.

## Evidence

> Sweep the retired author-mode vocabulary out of the tracked files the registry does not scan (`creative-studio/CLAUDE.md:52`, `llm-council/SKILL.md:62`...)

> There is a fundamental tension between the velocity of automated execution and the latency of human-readable observability.

## Examples

- An agent writes a summary of a research task, but the original source documents are not linked or archived, making it impossible to verify the summary's accuracy later.
- A cron job runs daily to update a dashboard, but the underlying data schema changes silently, causing the dashboard to display stale or misaligned metrics without alerting the user.

## Related Concepts

[[Operational Visibility vs. Semantic Value in Agent Fleets]] [[Silent Decay in Strategic Pipelines]]
