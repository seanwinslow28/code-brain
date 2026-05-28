---
title: "Infrastructure Status and Agent Failure"
type: concept
sources:
  - knowledge/connections/resilience-engineering-vs-uptime-obsession-in-job-hunt-artifacts.md
tags: [auto-generated, phase-6]
created: 2026-05-28
updated: 2026-05-28
---

## Definition

This concept defines the architectural necessity of distinguishing between the control plane, which dictates desired state and routing policies, and the data plane, which executes local logic. It posits that complex systems are always operating in degraded mode, meaning accidents emerge from latent conditions, tight coupling, and exhausted redundancy rather than a single broken box. This reframes failure not as a binary state of being online or offline, but as a loss of capacity to operate within acceptable degradation bounds.

## Context

Sean must shift his job-hunt narrative from maintaining uptime to demonstrating resilience engineering. By framing his infrastructure as a system that manages latent conditions and tight coupling, he signals senior-level thinking that distinguishes him from candidates focused merely on script maintenance.

## Evidence

> Complex systems are always operating in degraded mode; accidents emerge from latent conditions, tight coupling, and exhausted redundancy, not one broken box.

> This concept defines the architectural necessity of distinguishing between the control plane (which dictates desired state and routing policies) and the data plane (which executes local logic).

## Examples

- Distinguishing between control plane policies and data plane execution in infrastructure monitoring.

## Related Concepts

[[Automation Reliability]] [[Agent Health Monitoring]]
