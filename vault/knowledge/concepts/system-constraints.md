---
title: "System Constraints"
type: concept
sources:
  - 00_inbox/research-queue.md
tags: [auto-generated, phase-6]
created: 2026-06-01
updated: 2026-06-01
---

## Definition

System constraints are the hard boundaries imposed by tooling limitations that dictate operational routing, forcing a separation between simple, single-shape queries and complex, multi-target evaluations. When a tool like Local Deep Research (LDR) hits a timeout or citation collapse on compound prompts, the system must divert to a more capable agent like Gemini Deep Research to maintain output integrity. This constraint is not merely a preference but a structural requirement to prevent the generation of fabricated entities and URLs that arise when the model cannot ground citations across multiple targets.

## Context

This matters to Sean because it defines the architectural boundary of his current automated research pipeline. Understanding that LDR is pinned to v1.5.6 due to upstream migration bugs means he cannot simply upgrade to fix the timeout issue; he must rely on the Gemini DR tier for complex tasks until the upstream PR is merged. This constraint directly impacts his ability to scale research output without manual intervention or quality degradation.

## Evidence

> Compound prompts stall around 90 % and produce no output. (Topic 1b, 2026-05-06.)

> Qwen3-14B can't ground citations across multiple targets and confidently writes fabricated entities, owners, and URLs.

> LDR is pinned to v1.5.6 awaiting upstream PR [LearningCircuit/local-deep-research#4000]

## Examples

- Topic 1b, 2026-05-06: Compound prompt stalled at 90% timeout
- Topic 1a, 2026-05-05: Fabricated entities in LDR output
- Upstream Alembic-runner bug (migration 0007 FK mismatch)

## Related Concepts

[[Gemini Deep Research]] [[Local Deep Research (LDR)]] [[Infrastructure Status]]
