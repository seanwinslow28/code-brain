---
title: "Liability Routing in Agentic Product Design"
type: concept
sources:
  - knowledge/concepts/liability-routing-in-agentic-product-design.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

This mechanism describes a structural failure mode where an AI system generates confident, plausible falsehoods due to epistemic uncertainty, inducing user action that legally binds the deploying organization. Unlike standard technical errors which may trigger error codes or refusals, this specific failure path bypasses safety filters because the model does not recognize its own ignorance as a boundary condition. The organization becomes legally bound by these outputs regardless of Terms-of-Service disclaimers, creating a direct causal link between model calibration and corporate legal exposure.

## Context

Sean is building an AI PM curriculum and product strategy; understanding this liability routing is critical because it defines the hard boundary where 'product quality' ends and 'legal risk' begins. It forces a shift from purely technical metrics (accuracy) to legal defensibility metrics (refusal behavior, grounding).

## Evidence

> The 2nd-order chain PMs must pre-write: hallucination → user acts on it → the company is legally bound by it.

> Terms-of-service disclaimers do not survive contact with a judge.

## Examples

- Air Canada chatbot invented a bereavement-fare policy, leading to a tribunal ruling the airline fully liable.
- NYC's MyCity bot confidently advised small businesses to break labor law without firing any error codes.

## Related Concepts

[[Epistemic Artifacts as Strategic Proof]] [[The Illusion of Competence in Automated Systems]]
