---
title: "Residual State in Financial Observability"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-09-21
updated: 2026-09-21
---

## Definition

A failure mode where a system's state management retains pre-execution assumptions (such as budget reservations) after the execution has completed successfully, creating a persistent discrepancy between recorded intent and actual outcome. This mechanism causes downstream observers to misinterpret the system's health or resource availability because the cleanup logic fails to reconcile the initial reservation with the final settlement. The tension arises from the asymmetry between the ease of creating a state lock and the complexity of ensuring its release across all exit paths, including clean exits.

## Context

Sean has identified a bug in his fleet's budget tracking where a $4.31 reservation remains active despite only $0.445 being spent, leading to a false impression of high costs. This is a direct threat to the reliability of his automated financial controls and requires immediate investigation into the settlement path.

## Evidence

> vault/health/council-spend-2026-09-14.json still holds only a pre-flight reservation row of $4.31 with status: unknown and no settlement row

> the daily cap reads ~10x the money actually spent and a few more runs would trip a false Budget rejected

## Examples

- The run settled at cost_usd: 0.445 in its session archive, but the health file shows a $4.31 reservation.

## Related Concepts

[[Silent Failure Propagation in Agent Fleets]] [[Operational Uptime vs. Semantic Value in Agent Fleets]]
