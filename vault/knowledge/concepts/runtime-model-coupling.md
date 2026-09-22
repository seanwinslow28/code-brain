---
title: "Runtime-Model Coupling"
type: concept
sources:
  - 20_projects/research/2026-09-21-what-jev-is.md
tags: [auto-generated, phase-6]
created: 2026-09-22
updated: 2026-09-22
---

## Definition

This invariant describes the structural dependency where a decision engine's operational viability is strictly bound to its input schema and output constraints, rather than its generative capacity. When a model like Jev is defined as 'not a drop-in replacement for the LLM' because it lacks text generation, it forces the surrounding system architecture to decouple reasoning from expression. This coupling creates a rigid boundary where the agent must handle all semantic formatting externally, turning the model into a pure logic gate rather than a creative partner.

## Context

Sean is evaluating Jev for Devcraft and Productcraft roles. Understanding this coupling prevents him from attempting to use Jev as a general-purpose synthesizer, which would fail because the model 'does not write text, code or rationales'. He must instead design hooks that feed structured state and consume typed choices.

## Evidence

> The docs say outright it is '**not** a drop-in replacement for the LLM behind Claude Code'

> It does not write text, code or rationales

> a `state` (text or JSON) plus a map of typed questions in, one typed answer per question out

## Examples

- Using Jev as a 'typed tool-call risk Noul in a PreToolUse hook'
- Failing to use it for 'counts, dates, arithmetic' because those are modes 2 and 3 which Jev cannot produce

## Related Concepts

[[Runtime-Model Coupling]] [[Constraint-First Automation vs. General Efficiency]] [[The Calibration Bottleneck in Scalable Creative Production]]
