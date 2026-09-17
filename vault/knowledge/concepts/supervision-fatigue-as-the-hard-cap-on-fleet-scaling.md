---
title: "Supervision Fatigue as the Hard Cap on Fleet Scaling"
type: concept
sources:
  - knowledge/concepts/supervision-fatigue-as-the-hard-cap-on-fleet-scaling.md
tags: [auto-generated, phase-6]
created: 2026-09-17
updated: 2026-09-17
---

## Definition

This mechanism defines the inflection point where the marginal cognitive cost of monitoring agent health exceeds the marginal utility of their output. As fleet size increases, the frequency of 'stale' or 'partial' states grows non-linearly, forcing the human operator into a reactive maintenance role rather than a strategic oversight one. The system shifts from an automation engine to a liability generator, where the primary value is no longer creation but the continuous repair of broken dependencies.

## Context

Sean's fleet has expanded significantly, yet the operational metrics show a growing gap between activity and utility. With 9 active agents and 8 disabled ones, the infrastructure requires constant attention to prevent silent decay. The risk is that Sean becomes the bottleneck for his own automation, spending more time managing the 'health' of the system than leveraging its insights.

## Evidence

> The fleet status shows 'Active agents: 9 of 17 | Disabled: 8', indicating a significant portion of the infrastructure is inactive and potentially requiring maintenance or re-evaluation.

> The vault-critic agent has been 'stale' for 389.1 hours, with notes indicating 'status=partial articles=3 codex_fail=1', which likely requires Sean's attention to resolve the partial state.

## Examples

- The daily-driver agent costs '$0.2897' per run, but if Sean spends more time reviewing its output than writing his own notes, the net value becomes negative.
- The 'Claim-6 Drill' status being 'DRILL NOT DUE TODAY' requires manual checking to ensure it doesn't become another stale item.

## Related Concepts

[[Supervision as the New AI Edge]] [[Agent Health Monitoring]]
