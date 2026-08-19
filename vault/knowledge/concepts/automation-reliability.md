---
title: "Automation Reliability"
type: concept
sources:
  - knowledge/concepts/automation-reliability.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This mechanism defines the invariant that automated systems must prioritize deterministic execution and fault tolerance over optimal output quality when operating in unattended environments. It establishes a hierarchy where availability is a prerequisite for any quality metric, meaning that a reliable but lower-fidelity check is superior to an unreliable high-fidelity one. This principle forces the architecture to reject external dependencies that introduce non-deterministic latency or cost structures.

## Context

Sean's job hunt and creative studio workflows depend on consistent daily outputs. If the synthesizer fails due to external API timeouts, the entire day's knowledge synthesis is lost. Prioritizing reliability ensures that the vault remains a stable foundation for downstream creative work, even if it means accepting lower fidelity in the initial verification steps.

## Evidence

> The core tension lies between the desire for high-fidelity verification and the economic reality of scaling that verification across thousands of daily operations.

> High-fidelity checks typically require expensive, slow external models, which breaks headless automation by introducing latency and failure points.

## Examples

- Accepting lower fidelity in exchange for zero marginal cost and guaranteed availability through local execution
- Rejecting option (b) as the cost trap because it cannot gate a headless pipeline

## Related Concepts

[[Runtime-Model Coupling]] [[The Verification-Governance Inversion]]
