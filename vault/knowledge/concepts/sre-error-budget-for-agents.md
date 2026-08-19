---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/concepts/sre-error-budget-for-agents.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

An SLO-based reliability contract where agent performance is measured by observable outcomes like timeliness and correctness rather than binary active/disabled states. When an agent exhausts its error budget through repeated misses, feature work freezes to trigger reliability engineering, shifting the focus from mere process reachability to value delivery. This mechanism treats fleet health as a dynamic resource management problem rather than a static status check.

## Context

Sean needs to move beyond counting processes to judging whether his fleet delivers actual value. By implementing error budgets, he gains an executable framework to decide whether to improve prompts, repair infrastructure, or retire agents based on data rather than intuition.

## Evidence

> Attach an error-budget policy: repeated misses freeze feature work and trigger reliability work.

> Define each agent by an observable outcome: completion, timeliness, coverage, and correctness.

## Examples

- Daily Driver publishes a validated note by 08:40 on 29 of 30 mornings.
- Agent X was last observed producing valid artifact Y at T; this claim expires at T+n.

## Related Concepts

[[Fleet Status]] [[Agent Health Monitoring]]
