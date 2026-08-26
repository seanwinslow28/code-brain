---
title: "Coupling Fragility vs Adaptive Capacity in Agent Fleets"
type: concept
sources:
  - knowledge/concepts/coupling-fragility-vs-adaptive-capacity-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-08-25
updated: 2026-08-25
---

## Definition

This concept defines the tension between rigid functional dependencies and the system's ability to degrade gracefully under load or failure. It posits that agent fleets often operate with high coupling, where a single point of failure (like credential expiration) halts downstream processes, rather than exhibiting adaptive capacity where minimal viable outputs are preserved. The mechanism involves identifying 'latent conditions'—such as timing variance or environment drift—that do not break individual components but resonate to cause systemic failure when they coincide.

## Context

Sean's vault synthesizer runs show a clear shift from high-throughput/high-rejection (qwen3-14b era) to lower-throughput/lower-rejection (qwen3.6-35b era). Understanding this trade-off is critical for determining whether the fleet should prioritize volume of synthesis or reliability of output, especially as the job hunt and creative studio domains require consistent, albeit smaller, signals.

## Evidence

> The missing note was the visible boundary crossing; contributing conditions included credential validity, launchd environment, schedule ordering, write-path availability, and absent fallback generation.

> When the morning agent cannot produce the full note, the fleet crosses from base capacity into adaptive capacity: create a minimal skeleton, preserve queued captures, mark provenance and staleness, then reconcile later.

## Examples

- The transition from qwen3-14b (avg 120+ concepts written, ~60 rejected) to qwen3.6-35b (avg 100 concepts written, ~20 rejected) demonstrates a shift toward higher fidelity and lower rejection rates, suggesting improved adaptive capacity despite lower raw throughput.
- The 'rejected_count' metric in the manifest serves as a proxy for coupling fragility; high rejection counts indicate that the system is failing to adapt to latent conditions (e.g., cluster quality variance) rather than gracefully degrading.

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[The Illusion of Health in Autonomous Systems]]
