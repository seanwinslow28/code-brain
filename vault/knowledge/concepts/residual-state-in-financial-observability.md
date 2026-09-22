---
title: "Residual State in Financial Observability"
type: concept
sources:
  - knowledge/concepts/residual-state-in-financial-observability.md
tags: [auto-generated, phase-6]
created: 2026-09-22
updated: 2026-09-22
---

## Definition

A failure mode where financial tracking systems retain stale pre-flight allocations after a process completes, creating a divergence between recorded intent and actual expenditure. This state persists because the settlement logic fails to release or reconcile the reservation upon clean exit, causing subsequent runs to read inflated budget ceilings. The system interprets the unreleased reservation as active spend, leading to false-positive budget rejections even when the underlying transaction ledger shows zero cost.

## Context

Sean's agent fleet relies on accurate daily caps to prevent runaway costs. When the council spend file holds a stale $4.31 reservation while the actual run cost is $0.445, the observability layer becomes unreliable, masking the true health of the system and risking premature shutdowns.

## Evidence

> vault/health/council-spend-2026-09-14.json still holds only a pre-flight reservation row of $4.31 with status: unknown and no settlement row

> the daily cap reads ~10x the money actually spent and a few more runs would trip a false Budget rejected

## Examples

- The run settled at cost_usd: 0.445 in its session archive, but the health file shows $4.31
- The ledger printed $0.45 estimated rather than the recorded actual

## Related Concepts

[[Operational Uptime vs. Semantic Value in Agent Fleets]] [[Legibility Debt as a Supervision Failure Mode]]
