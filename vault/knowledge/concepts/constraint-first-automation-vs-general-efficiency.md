---
title: "Constraint-First Automation vs. General Efficiency"
type: concept
sources:
  - 20_projects/research/2026-09-09-productcraft-book-to-seat-findings.md
tags: [auto-generated, phase-6]
created: 2026-09-16
updated: 2026-09-16
---

## Definition

This pattern emerges when automation is driven by strict boundary conditions (cost, format, availability) rather than broad efficiency goals. Instead of optimizing for the fastest path to information, the system optimizes for the most robust path within defined constraints, such as 'zero cost' or 'DRM-free'. This creates a more resilient infrastructure because it avoids dependencies on fragile external factors like subscription renewals or variable pricing, forcing the agent to rely on verified, static data points.

## Context

Sean's research methodology explicitly rejects paid research tools in favor of web sweeps and free canon verification. By imposing a '$0 research' constraint, he forces the agents to prioritize verifiable facts over speculative insights, resulting in a more stable but potentially slower discovery process that avoids financial leakage.

## Evidence

> Cost: $0 research (web sweeps; no paid research invoked). Estimated tier-1 purchase ~$290 in ebooks, several prices unverified at time of writing.

> Web-search budgets ran out in every agent's final pass, so a handful of prices and runtimes are marked unverified rather than guessed.

## Examples

- Marking prices as 'unverified' rather than guessing prevents the introduction of hallucinated financial data into the corpus.
- Using 'DRM-free likely' as a filter criterion ensures long-term accessibility of assets, prioritizing ownership over convenience.

## Related Concepts

[[Cost-Capped Agentic Workflows]] [[Operational Uptime vs. Cognitive Utility Tension]]
