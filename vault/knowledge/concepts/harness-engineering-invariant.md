---
title: "Harness Engineering Invariant"
type: concept
sources:
  - knowledge/concepts/harness-engineering-invariant.md
tags: [auto-generated, phase-6]
created: 2026-07-09
updated: 2026-07-09
---

## Definition

This invariant asserts that the reliability of an agentic evaluation is determined not by the intelligence of the individual agents, but by the strict isolation of their inputs and the blindness of their judgment criteria. When evidence bundles are frozen and mappings are kept in separate key files, the system prevents 'judge self-preference' and 'authorship bias.' The mechanism relies on deterministic shuffling (sha256) to ensure that any observed quality difference is attributable to the analysis method (panel vs. single model) rather than positional artifacts or prior knowledge of the source.

## Context

Sean's research into 'Panel-vs-single-model gate' relies on this invariant to validate his infrastructure decisions. Without this rigorous harness, he cannot distinguish between a better model and a better prompt position, making it impossible to justify the cost of a multi-model fleet over a single strong one.

## Evidence

> The two pain-point sets were anonymized + shuffled (sha256-deterministic), then rated by the variance LLM-council... The mapping (Set→arm) was kept in a separate key file; raters were blind.

> Held everything constant except panel breadth: Same evidence bundle — gathered once (46 real-URL records), frozen to disk, fused by both arms.

## Examples

- Using sha256-deterministic shuffling to anonymize pain-point sets before rating.
- Keeping the Set-to-arm mapping in a separate key file inaccessible to raters.

## Related Concepts

[[Control Architecture as Evangelism]] [[Operational Readiness Review]]
