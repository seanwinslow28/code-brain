---
title: "Vault Synthesizer Eval Suite"
type: concept
sources:
  - knowledge/connections/self-validation-vs-external-validity-in-agentic-evaluation.md
tags: [auto-generated, phase-6]
created: 2026-07-14
updated: 2026-07-14
---

## Definition

This refers to the specific infrastructure artifact where the evaluation logic was flawed by including the judge within the candidate pool. It represents a concrete instance of the verification-governance inversion, where the tool meant to validate quality instead reinforced its own biases. The suite's design flaw required a retrofit to ensure judges were structurally separated from candidates.

## Context

Sean's prior runs using this suite produced misleadingly high confidence scores because the judge was a literal member of the panel. Correcting this requires auditing all automated evaluation pipelines for similar structural flaws.

## Evidence

> the FUSE judge `anthropic/claude-opus-4.7` was a *literal member* of its own panel in every tier

> Credibility in 'multi-vendor' claims requires explicit architectural separation, not just rhetorical diversity

## Examples

- The FUSE judge being included in the candidate panel
- Prior runs showing high concept counts but low external validity due to self-grading

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Synthesizer fix]]
