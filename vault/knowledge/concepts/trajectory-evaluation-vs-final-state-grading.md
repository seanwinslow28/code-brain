---
title: "Trajectory Evaluation vs. Final-State Grading"
type: concept
sources:
  - 20_projects/research/2026-08-29-software-factory-lit-delta/codex-delta-synthesis.md
tags: [auto-generated, phase-6]
created: 2026-08-31
updated: 2026-08-31
---

## Definition

This concept defines the limitation of outcome-based metrics in long-horizon agentic workflows, where a correct final result achieved through non-compliant or unsupported intermediate steps is epistemically untrustworthy. The mechanism requires evaluating the *path* of execution—specifically tool call validity, context adherence, and behavioral contracts—rather than just the terminal output. This shifts the evaluation burden from a binary pass/fail on the artifact to a continuous monitoring of the process integrity, ensuring that the 'how' is as constrained as the 'what'.

## Context

Sean’s recent runs have increased in duration and complexity (e.g., 2700+ seconds for 125 concepts), suggesting longer-horizon tasks. Without trajectory evaluation, these long runs risk producing plausible but structurally invalid outputs that pass final-state grading but fail practical utility.

## Evidence

> Basis argues that a correct result reached through an unsupported or non-compliant path is not trustworthy and uses sparse BEHAVIOR.md contracts plus an agentic judge over the trajectory.

> Databricks separately checks duplicate or failing tool calls that outcome scoring would miss.

## Examples

- A Databricks customer case runs deterministic, semantic, and behavioral checks on live traces, deflecting low-quality cases to humans.
- Uber combines real-PR review benchmarks with production revert rate, F1, MTTR, noise, and cost per outcome.

## Related Concepts

[[Eval Vocabulary as Control Mechanism]] [[Legibility Debt as a Supervision Failure Mode]]
