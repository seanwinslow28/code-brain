---
title: "Eval Vocabulary as Control Mechanism"
type: concept
sources:
  - knowledge/concepts/eval-vocabulary-as-control-mechanism.md
tags: [auto-generated, phase-6]
created: 2026-08-18
updated: 2026-08-18
---

## Definition

This concept defines the shift from traditional product requirements documents to executable evaluation criteria that serve as the primary interface for defining AI behavior. It establishes that the ability to write precise, measurable evals is a prerequisite for controlling autonomous agents, replacing vague intent with quantifiable success conditions. This mechanism forces the distinction between 'running' and 'working' by requiring explicit definitions of what constitutes a valid output, thereby exposing the gap between operational uptime and semantic correctness.

## Context

Sean is transitioning from manual oversight to agentic automation in his job hunt and creative studio. Without a robust eval vocabulary, he cannot distinguish between an agent that successfully generated content and one that generated useful content, leaving him vulnerable to the illusion of health described in the primary file.

## Evidence

> The theme of all of it, repeated until it became a kind of liturgy, was this: **evals are the new PRDs.** A product manager who can't write evals is a product manager who can't specify what their AI is supposed to do.

> Sean must redesign his monitoring to detect output quality degradation, not just execution success, to prevent silent knowledge decay.

## Examples

- Treating evals as the new PRDs implies that the specification of AI behavior must be testable and binary-pass/fail rather than descriptive.
- The requirement to specify what the AI is supposed to do shifts the burden from post-hoc review to pre-execution definition.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[SRE Error Budget for Agents]]
