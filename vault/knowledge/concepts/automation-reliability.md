---
title: "Automation Reliability"
type: concept
sources:
  - 20_projects/substack-studio/06-stop-building-agents/2026-06-17-agent-or-automation-advisor-build-spec.md
tags: [auto-generated, phase-6]
created: 2026-06-23
updated: 2026-06-23
---

## Definition

Automation reliability is defined by the compounding risk of non-determinism across multiple LLM nodes within a deterministic pipeline. When an automation relies on bounded steps that call a model, the maintenance burden increases because debugging becomes difficult when behavior varies between runs. This creates a reliability collapse where the project fails not due to logic errors, but due to the inability to predict outcomes in a system that lacks strict state control.

## Context

Sean is building an 'Agent-or-Automation Advisor' to help users avoid this trap before they start coding. He recognizes that people often choose complex agents when simple automations would suffice, leading to high maintenance costs later. This concept is central to his Substack series on stopping the blind construction of agents.

## Evidence

> automations with LLM nodes... the maintenance burden kills it

> non-determinism compounding across steps, debugging a thing that behaves differently every run

## Examples

- A 20-line automation that calls a model at one or two bounded steps instead of a multi-step looping agent.

## Related Concepts

[[Agent Rationalization]] [[Silent Failure Propagation in Agent Fleets]]
