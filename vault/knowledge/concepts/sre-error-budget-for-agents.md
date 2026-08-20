---
title: "SRE Error Budget for Agents"
type: concept
sources:
  - knowledge/connections/proxy-metrics-mask-semantic-decay-in-agentic-fleets.md
tags: [auto-generated, phase-6]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

This concept defines a governance mechanism where the acceptable rate of failure is quantified and capped to prevent reliability degradation from consuming all available resources. When the monthly error budget exceeds a defined threshold, expansion must pause to fund reliability work rather than adding more agents. This approach treats agent reliability as a finite resource that requires active management, similar to traditional SRE practices but applied to autonomous synthesis tasks. It forces a trade-off between velocity and stability by making failure costs explicit.

## Context

Sean's fleet has been expanding without clear error budgets, leading to silent failures in synthesis quality. By defining explicit SLIs for freshness and correctness, he can determine when the cost of new agents outweighs their value. This prevents the accumulation of legibility debt that currently masks the true state of his knowledge infrastructure.

## Evidence

> If the monthly error budget exceeds Z, pause fleet expansion and fund reliability work.

> Silent failures in synthesis quality should trigger reliability sprints rather than new agent deployments.

## Examples

- Pausing fleet expansion when error rates exceed a defined threshold to focus on reliability.
- Triggering reliability sprints when synthesis quality drops below acceptable levels.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Operational Visibility vs. Semantic Value in Agent Fleets]]
