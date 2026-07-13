---
title: "Synthesizer fix"
type: concept
sources:
  - knowledge/connections/self-validation-vs-external-validity-in-agentic-evaluation.md
tags: [auto-generated, phase-6]
created: 2026-07-13
updated: 2026-07-13
---

## Definition

This concept defines the architectural intervention of enforcing family separation between generation and evaluation models. It posits that model family separation is the single highest-leverage, lowest-cost lever for restoring epistemic integrity in agentic workflows. By decoupling the judge from the candidate pool, the system prevents the structural bias inherent in same-family evaluations.

## Context

Sean needs to implement this fix to validate claims of robustness across diverse inputs. It is a critical step in moving from operational efficiency to genuine discovery in his knowledge vault infrastructure.

## Evidence

> family separation is the single highest-leverage, lowest-cost lever

> The core tension exists between the operational efficiency of using a single model family for both generation and evaluation versus the epistemic integrity required for genuine discovery

## Examples

- Switching from Qwen3.6 to Claude for evaluation while keeping Qwen3.6 for synthesis
- Using Llama-2 as a judge for GPT-4 outputs in benchmarking scenarios

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Vault Synthesizer Eval Suite]]
