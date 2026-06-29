---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/expansions/connections/observability-and-personal-knowledge-infrastructure.md
tags: [auto-generated, phase-6]
created: 2026-06-29
updated: 2026-06-29
---

## Definition

This concept applies Site Reliability Engineering principles to personal agent fleets by defining measurable Service Level Objectives (SLOs) and corresponding error budgets for automation reliability. It shifts the focus from mere status monitoring to quantifiable performance thresholds, such as daily note freshness or manual correction time limits. When these budgets are exhausted, it triggers specific operational responses like blameless postmortems or toil tracking rather than simple alerting.

## Context

Sean is building a personal knowledge infrastructure that relies on automated agents for daily notes and research. Without defined error budgets, he risks accumulating 'toil'—repetitive manual patches for agent failures—which degrades system reliability over time. This concept provides the mathematical framework to decide when to automate further versus when to accept human-in-the-loop costs.

## Evidence

> Borrow SLOs, error budgets, toil tracking, and blameless postmortems from infrastructure operations, but apply them to personal agent fleets.

> Example: “daily note freshness SLO: 95% before 9 AM”; “manual correction budget: under 20 minutes/week”; “agent toil: any recurring human patch after automation failure.”

## Examples

- Daily note freshness SLO: 95% before 9 AM
- Manual correction budget: under 20 minutes/week
- Agent toil: any recurring human patch after automation failure

## Related Concepts

[[Agent Health Monitoring]] [[Automation Reliability]] [[Infrastructure Status]]
