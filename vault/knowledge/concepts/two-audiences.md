---
title: "Two Audiences"
type: concept
sources:
  - knowledge/connections/the-supervision-context-agency-triad-in-product-design.md
tags: [auto-generated, phase-6]
created: 2026-06-05
updated: 2026-06-05
---

## Definition

The Two Audiences invariant describes a structural tension where a product must simultaneously satisfy human stakeholders who approve budgets and autonomous agents who execute workflows. This duality forces the system design to accommodate two distinct sets of requirements: one focused on financial justification and strategic alignment for humans, and another focused on precise state management and tool execution for agents. The mechanism creates a friction point because optimizing for one audience often degrades the experience or utility for the other, requiring explicit boundary objects to translate between these incompatible value systems.

## Context

Sean is navigating the AI Product Manager landscape where he must demonstrate an understanding of this split. His job hunt and creative studio workflows both require him to build systems that serve his own operational needs (as the human stakeholder) while also being robust enough for automated agents to process without failure. Recognizing this invariant helps him frame his portfolio projects as solutions to this specific architectural problem rather than just general productivity tools.

## Evidence

> The Two Audiences invariant describes the tension where a product must simultaneously satisfy human stakeholders who approve budgets and autonomous agents who execute workflows.

> Success depends on designing boundary objects that translate between these two distinct value systems without loss of fidelity.

## Examples

- A dashboard that shows ROI metrics to humans while exposing API endpoints for agent-driven updates
- A workflow where human approval gates trigger automated state transitions for downstream agents

## Related Concepts

[[Boundary Object Theory]] [[Agentic Engineering]]
