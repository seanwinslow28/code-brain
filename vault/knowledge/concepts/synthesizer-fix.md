---
title: "Synthesizer fix"
type: concept
sources:
  - knowledge/connections/self-validation-vs-external-validity-in-agentic-evaluation.md
tags: [auto-generated, phase-6]
created: 2026-07-22
updated: 2026-07-22
---

## Definition

A strategic intervention where the separation of model families for generation and evaluation is identified as the highest-leverage mechanism for restoring epistemic integrity. This fix requires decoupling the judge from the candidate pool to prevent self-grading artifacts, ensuring that validation metrics reflect external truth rather than internal consistency. The mechanism relies on architectural diversity to break the self-referential loops that compromise automated assessment reliability.

## Context

Sean identified this separation as the single highest-leverage lever for fixing his synthesizer's evaluation flaws, moving from a monolithic model family to a diverse panel to ensure genuine discovery and robustness across inputs.

## Evidence

> family separation is the single highest-leverage, lowest-cost lever

> The core tension exists between the operational efficiency of using a single model family for both generation and evaluation versus the epistemic integrity required for genuine discovery

## Examples

- Switching from qwen3.6-35b-a3b-32k for both synthesis and validation to using external judges
- Implementing a blind judge panel that excludes the primary synthesis model

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Vault Synthesizer Eval Suite]]
