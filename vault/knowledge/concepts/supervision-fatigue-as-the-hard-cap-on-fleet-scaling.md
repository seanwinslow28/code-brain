---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - 02_Areas/Agent-Fleet/daily-fleet-status-2026-09-02.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

As the number of autonomous agents increases, the cognitive load required to monitor their collective state grows non-linearly. This creates a hard cap on scalability because the user's capacity to interpret and act on fleet status reports becomes the bottleneck. The system shifts from being an extension of the user's will to a source of noise that requires active management, effectively reducing the net productivity gain of adding more agents.

## Context

Sean's fleet has grown from 7 active agents in June to 9 active and 8 disabled in September. The increasing complexity of managing 'stale' vs 'healthy' states across multiple domains (creative, job hunt, infrastructure) suggests that Sean is approaching the limit of his ability to supervise this system effectively without automated intervention or simplification.

## Evidence

> Active agents: 9 of 17 | Disabled: 8

> Misaligned or Touching Decline - Vault critic and knowledge-lint agents are stale; need immediate ex

> Daily morning routine successfully executed; planning complete for today.

## Examples

- The fleet status report explicitly categorizes agents as 'Aligned with Protect / Automate' vs 'Misaligned or Touching Decline', requiring Sean to manually triage.
- The presence of 8 disabled agents indicates a history of failed experiments that are no longer monitored, adding to the cognitive overhead of understanding the current system state.

## Related Concepts

[[Supervision as the New AI Edge]] [[Context Management as a Bottleneck]]
