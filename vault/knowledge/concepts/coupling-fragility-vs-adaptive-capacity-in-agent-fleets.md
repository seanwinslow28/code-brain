---
title: "Coupling Fragility vs Adaptive Capacity in Agent Fleets"
type: concept
sources:
  - knowledge/expansions/coupling-fragility-vs-adaptive-capacity-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

This concept defines a structural tension where an agent fleet's reliability is determined by the ratio of rigid, unverified dependencies to its ability to absorb failure without collapse. When agents operate under implicit orchestration assumptions rather than explicit promise contracts, the system accumulates coupling fragility; any single point of stale data or silent failure propagates through the chain because the adaptive capacity—the ability to detect saturation and recruit alternate paths—remains latent. The mechanism is not merely about redundancy, but about the visibility of constraints: if an agent cannot verify the freshness and provenance of its input, it cannot safely adapt, forcing the entire fleet into a brittle state where graceful extensibility is impossible.

## Context

Sean's vault synthesizer runs have shown increasing complexity (from 3 to 125 concepts) but also rising rejection rates and duration. Without explicit 'promise contracts' or STPA-based control loops, the growing number of connections between agents creates a hidden debt of coupling fragility that threatens the stability of his personal knowledge infrastructure.

## Evidence

> The missing move is: For each agent, name the controller, controlled process, feedback channel, unsafe control action, and missing constraint. This turns A creates B's unsafe context into an analyzable control loop.

> This fleet is healthy only if it can detect saturation, recruit alternate capacity, and preserve coordination before brittle collapse.

## Examples

- A daily-driver agent consuming stale synth output without freshness metadata
- An observability dashboard showing remaining slack and fallback depth rather than just green/red status

## Related Concepts

[[Control Plane / Data Plane Split for Agent Fleets]] [[Silent Failure Propagation in Agent Fleets]] [[SRE Error Budget for Agents]]
