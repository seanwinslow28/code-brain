---
title: "Synthesizer fix"
type: concept
sources:
  - knowledge/connections/self-validation-vs-external-validity-in-agentic-evaluation.md
tags: [auto-generated, phase-6]
created: 2026-07-20
updated: 2026-07-20
---

## Definition

A strategic intervention where the separation of model families for generation and evaluation is identified as the highest-leverage mechanism for restoring epistemic integrity. This fix addresses the core tension between operational efficiency and truth-seeking by enforcing architectural boundaries that prevent self-validation artifacts. It requires explicitly decoupling the judge from the candidate panel to ensure that performance metrics reflect genuine capability rather than internal alignment.

## Context

Sean's recent runs show a shift in model usage, but without explicit separation, the quality of insights may be artificially inflated by self-preference. Implementing this fix is necessary to validate the robustness of his synthesizer across diverse inputs.

## Evidence

> family separation is the single highest-leverage, lowest-cost lever

> The core tension exists between the operational efficiency of using a single model family for both generation and evaluation versus the epistemic integrity required for genuine discovery

## Examples

- Using Qwen for synthesis and Claude for evaluation
- Using Llama for generation and GPT-4 for grading

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Vault Synthesizer Eval Suite]]
