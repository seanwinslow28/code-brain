---
title: "Cost Control vs. Unit Economics"
type: concept
sources:
  - knowledge/concepts/cost-control-vs-unit-economics.md
tags: [auto-generated, phase-6]
created: 2026-09-01
updated: 2026-09-01
---

## Definition

This mechanism distinguishes between operational cost containment and economic viability in AI product design. Cost control involves setting hard limits on resource consumption, such as token budgets or daily spend caps, to prevent financial bleed during development. In contrast, unit economics requires calculating the margin of a successful outcome by comparing revenue against the variable cost of delivering that specific value. The tension arises because engineers often conflate these two metrics, optimizing for cheap execution rather than profitable impact.

## Context

Sean has built robust cost control mechanisms in his fleet (caps, budgets) but lacks any unit economic model because his current work is internal infrastructure with no revenue side. This lesson forces him to confront that having a 'green' budget does not mean the product is viable or valuable.

## Evidence

> Cost control is not unit economics. A cap stops a bill. Unit economics asks whether the thing makes money when it works.

> You are genuinely good at the first and have never once done the second — there is no revenue side to your fleet, no cost per successful outcome, no margin.

## Examples

- Setting a $20/day cap on model usage
- Calculating cost per successful article synthesis

## Related Concepts

[[Cost-Capped Agentic Workflows]] [[Revenue Integration]]
