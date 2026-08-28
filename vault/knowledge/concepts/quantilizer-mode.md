---
title: "Quantilizer Mode"
type: concept
sources:
  - knowledge/expansions/goodhart-failure-typing.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

Quantilizer mode is an optimization strategy that samples from the top q-percent of candidates above a quality floor, rather than selecting the single highest-scoring output via argmax. This approach mitigates extremal Goodhart failure by preventing the optimizer from exploiting edge cases in the proxy metric where correlation breaks down. It forces the system to maintain a distribution of acceptable outputs instead of converging on a narrow, potentially corrupted peak.

## Context

Sean's fleet currently uses argmax selection, which is vulnerable to extremal failure when models are pushed beyond their reliable range. Implementing quantilizer mode would provide a concrete control mechanism to stabilize semantic value during high-throughput synthesis runs.

## Evidence

> Add quantilizer mode: sample among outputs above an acceptable quality threshold instead of selecting the single highest-scoring output.

> Generate N candidates, discard those below the factuality and relevance floor, then sample from the top q-percent rather than taking argmax.

> This unlocks an executable vault-synthesizer selection experiment comparing argmax, top-k, and quantilized selection across novelty, unsupported claims, and human usefulness.

## Examples

- Discarding outputs below a factuality floor
- Sampling from the top q-percent of candidates
- Comparing argmax vs. quantilized selection in synthesis runs

## Related Concepts

[[The Taste-Throughput Trade-off in Agentic Synthesis]] [[SRE Error Budget for Agents]] [[Constraint-First Automation vs. General Efficiency]]
