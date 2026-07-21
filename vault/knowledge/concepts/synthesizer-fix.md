---
title: "Synthesizer fix"
type: concept
sources:
  - knowledge/concepts/synthesizer-fix.md
tags: [auto-generated, phase-6]
created: 2026-07-21
updated: 2026-07-21
---

## Definition

This mechanism identifies the separation of model families for generation and evaluation as the highest-leverage intervention for restoring epistemic integrity in agentic workflows. It addresses the core tension between operational efficiency and truth-seeking by enforcing architectural boundaries that prevent self-validation artifacts, ensuring that performance metrics reflect genuine capability rather than internal alignment. The fix requires explicitly decoupling the judge from the candidate panel to eliminate the illusion of competence that arises when a single model family evaluates its own outputs.

## Context

Sean's recent runs show a shift in model usage, but without explicit separation, the quality of insights may be artificially inflated by self-preference. Implementing this fix is necessary to validate the robustness of his synthesizer across diverse inputs and prevent the degradation of taste fidelity as automation scales.

## Evidence

> family separation is the single highest-leverage, lowest-cost lever

> The core tension exists between the operational efficiency of using a single model family for both generation and evaluation versus the epistemic integrity required for genuine discovery

## Examples

- Using Qwen for synthesis and Claude for evaluation
- Using Llama for generation and GPT-4 for grading

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Vault Synthesizer Eval Suite]]
