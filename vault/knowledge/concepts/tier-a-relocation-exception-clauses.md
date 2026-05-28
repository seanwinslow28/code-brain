---
title: "Tier-A Relocation Exception Clauses"
type: concept
sources:
  - knowledge/expansions/infrastructure-status.md
tags: [auto-generated, phase-6]
created: 2026-05-28
updated: 2026-05-28
---

## Definition

A reliability contract mechanism derived from Google SRE Service Level Objectives, where local inference tiers are defined by explicit error budgets rather than qualitative preferences. This pattern enforces a hard boundary between 'Tier A' (schema validity >= 95%) and 'Tier B' (draft latency focus), triggering a fallback to cloud providers only when the local error budget is exhausted. It transforms the decision of when to displace one local model with another into a concrete, auditable artifact based on reliability thresholds.

## Context

Sean’s job-hunt portfolio requires demonstrating 'portfolio-grade' engineering rigor. By framing his local agent infrastructure as governed by SLOs, he creates a tangible artifact that proves his ability to manage reliability contracts, a key differentiator for AI Product Manager roles.

## Evidence

> Add explicit SLO classes for local inference: Tier A schema validity >= 95%, recall >= 5/5, timeout <= 900s.

> This unlocks a portfolio-grade “Local Agent SRE” one-pager: Sean can show that his fleet is governed by reliability contracts, not vibes.

> It also creates a concrete decision artifact: “When does MBP-Ollama displace LM Studio, and when does it merely join the pool?”

## Examples

- Fallback: cloud only after local error budget burns

## Related Concepts

[[Infrastructure Status]] [[Portfolio Projects]]
