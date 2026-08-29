---
title: "Failure Amplification in Agentic Chains"
type: concept
sources:
  - knowledge/concepts/failure-amplification-in-agentic-chains.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

Failure amplification in agentic chains occurs when a degraded dependency triggers retries across layered agents, converting a single point of failure into system-wide overload. This mechanism couples cost and health causally, as retries magnify small failures into excess tokens, queue congestion, and duplicate writes that exhaust resource caps. Defending against this requires bounded retries with exponential backoff, idempotency keys, and circuit breaking to prevent the cascade from consuming the entire fleet's capacity.

## Context

Sean's vault synthesizer runs show high rejection counts and long durations, suggesting potential retry storms or inefficient sampling. By identifying failure amplification as a distinct mechanism, Sean can distinguish between genuine low-quality outputs and artifacts caused by cascading infrastructure failures. This distinction is critical for debugging why some runs consume significantly more tokens than others without proportional value.

## Evidence

> A degraded dependency can trigger retries across layered agents, converting one failure into excess tokens, queue congestion, duplicate writes, and exhausted caps.

> Retries can magnify small failures into system-wide overload.

## Examples

- Simulating an unavailable MBP model host to graph attempted calls and wasted compute.
- Demonstrating bounded retries, circuit breaking, and clean deferral as recovery mechanisms.

## Related Concepts

[[Coupling Fragility vs Adaptive Capacity in Agent Fleets]] [[Token Waste]]
