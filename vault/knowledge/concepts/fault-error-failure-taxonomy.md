---
title: "Fault → Error → Failure Taxonomy"
type: concept
sources:
  - knowledge/concepts/fault-error-failure-taxonomy.md
tags: [auto-generated, phase-6]
created: 2026-08-25
updated: 2026-08-25
---

## Definition

This mechanism distinguishes between the root cause (fault), the internal state deviation (error), and the externally visible service deviation (failure). It prevents the conflation of all issues into a single 'health' scalar by requiring explicit mapping of how latent errors become observable failures only when a consumer detects the discrepancy. This taxonomy enables rigorous incident analysis by clarifying whether an issue is a transient hardware glitch, a state corruption, or a genuine service outage.

## Context

Sean's vault infrastructure deals with complex dependencies between agents; without this taxonomy, it is difficult to determine if a missed daily note was due to a sleeping laptop (fault) or a broken index (error). Applying this framework allows for precise incident reporting and better fault isolation in his automated knowledge pipeline.

## Evidence

> Agent Health Monitoring and Agent Health are currently synonyms. The Avižienis taxonomy supplies the missing distinctions

> Fault X created latent error Y; it became service failure Z only when consumer C observed the deviation.

## Examples

- Distinguishing between wol-deferred, partial outputs, and citation corruption as distinct event types
- Mapping availability, reliability, integrity, safety, and maintainability as separate dependability attributes

## Related Concepts

[[Silent Failure Propagation in Agent Fleets]] [[Agent Hazard Analysis via STPA]]
