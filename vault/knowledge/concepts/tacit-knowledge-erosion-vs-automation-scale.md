---
title: "Tacit Knowledge Erosion vs. Automation Scale"
type: concept
sources:
  - knowledge/expansions/tacit-knowledge-erosion-vs-automation-scale.md
tags: [auto-generated, phase-6]
created: 2026-08-30
updated: 2026-08-30
---

## Definition

This concept describes a non-linear degradation of human expertise where the specific cognitive stage automated determines the nature of the resulting skill gap. When automation displaces execution, diagnostic capability often remains intact; however, when it automates interpretation or decision selection, the operator loses the ability to verify the system's internal logic. This creates a structural vulnerability where the human supervisor becomes cognitively dependent on the agent's output without possessing the mental models required to detect subtle failures or mode errors.

## Context

Sean is building an autonomous agent fleet that handles significant portions of his knowledge work and job hunt infrastructure. As he scales this system, he risks losing the 'taste' and diagnostic intuition necessary to supervise these agents effectively. Understanding which cognitive stages are being displaced allows him to intentionally preserve manual practice in high-leverage areas like interpretation and decision-making, preventing a total loss of agency.

## Evidence

> Automating execution preserves diagnosis differently from automating interpretation; the debt belongs to the displaced cognitive stage, not to automation in general.

> Before diagnosing deskilling, test whether the system made competent supervision cognitively impossible: could the operator state what the automation was doing, why, and what it would do next?

## Examples

- Mapping agent functions to Parasuraman's levels of automation to identify which stages Sean must perform manually.
- Designing an Observability Contract that requires agents to expose mode, evidence, decision, uncertainty, and next_action.

## Related Concepts

[[Supervision as the New AI Edge]] [[The Illusion of Competence in Automated Systems]] [[Control Room Observability]]
