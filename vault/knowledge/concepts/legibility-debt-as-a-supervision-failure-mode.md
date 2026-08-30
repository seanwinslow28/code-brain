---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/the-tension-between-operational-mastery-and-architectural-clarity.md
tags: [auto-generated, phase-6]
created: 2026-08-30
updated: 2026-08-30
---

## Definition

This concept defines the accumulation of unarticulated decision logic that occurs when an operator relies on implicit knowledge to supervise automated systems. As the system scales, the gap between what the operator can do and what they can explain widens, creating a debt that must be paid in future debugging, collaboration, or career transitions. This debt is a form of supervision failure because the operator cannot effectively audit or improve the system without explicit documentation of its design principles.

## Context

Sean's fleet has grown significantly, but his ability to supervise it explicitly has not kept pace. This creates a risk that he will be unable to explain his system's design to others or adapt it to new requirements.

## Evidence

> The gap is vocabulary plus the decision surfaces his production path never forced him to touch.

> His ability to run the system successfully masks the lack of explicit vocabulary and decision-making frameworks.

## Examples

- Sean cannot articulate why he chose specific rejection criteria for clusters, relying instead on intuition.
- He has not documented the architectural decisions behind his fleet's model selection process.

## Related Concepts

[[Tacit Knowledge Erosion vs. Automation Scale]] [[The Illusion of Competence in Automated Systems]]
