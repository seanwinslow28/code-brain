---
title: "Fault → Error → Failure Taxonomy"
type: concept
sources:
  - knowledge/concepts/fault-error-failure-taxonomy.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This framework distinguishes between internal state anomalies (faults), incorrect intermediate computations (errors), and the deviation of delivered service from its specification (failures). It prevents the conflation of component unavailability with functional failure, allowing for precise attribution of blame and recovery strategies. This taxonomy requires defining SLIs based on user-visible capabilities rather than internal component status to avoid masking semantic decay behind operational uptime.

## Context

Sean's current monitoring likely treats any offline node as a critical failure. By adopting this taxonomy, he can distinguish between a hardware fault (Alienware off) and a service failure (synthesis not completed), enabling more nuanced alerting and less panic-driven intervention.

## Evidence

> A fault may create an erroneous internal state, but a failure occurs only when delivered service deviates from its specification.

> Define SLIs around delivered capabilities: 'nightly synthesis completed by 08:00,' 'sprite job began within its declared execution window,' or 'deferred work remained queued without paid fallback.'

## Examples

- The ComfyUI node crashes (fault), causing a generated image to be missing (error), but the text synthesis completes on time, so the overall service failure is partial.
- A model provider rate limits requests (fault), leading to truncated outputs (error), which constitutes a service failure only if the truncation violates the defined quality SLI.

## Related Concepts

[[SRE Error Budget for Agents]] [[Agent Health Monitoring]]
