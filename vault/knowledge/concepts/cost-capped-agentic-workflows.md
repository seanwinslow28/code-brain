---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - knowledge/concepts/cost-capped-agentic-workflows.md
tags: [auto-generated, phase-6]
created: 2026-09-01
updated: 2026-09-01
---

## Definition

A resource-allocation mechanism where task routing is determined by a cost-benefit analysis of model tiers rather than capability uniformity. This approach treats computational expense as a primary constraint, forcing the system to distinguish between high-stakes reasoning tasks that require frontier models and low-stakes execution tasks suitable for lightweight or local alternatives. The invariant here is that economic efficiency is achieved not by optimizing individual model performance, but by minimizing the aggregate spend across a heterogeneous stack of specialized agents.

## Context

Sean is currently operating a fleet with significant variance in cost-per-run (from 3c to 125c). Understanding how to deliberately route tasks to cheaper models for non-critical steps is essential for maintaining the economic viability of his automated synthesis and job-hunt pipelines.

## Evidence

> Practitioners have shifted away from searching for a single 'best' model. Instead, they design multi-tiered model stacks, choosing specific models based on task economics, specialized capabilities, or latency

> He organizes his factory into three distinct tiers: State-of-the-Art (frontier models), Workhorse (fast, highly capable models), and Lightweight/Local models

## Examples

- Using Kimmy K3 for UX/UI design tasks while reserving GPT 5.6 Soul/High for core implementation
- Running parallel 'Best of N' sandbox fleets with mixed configurations to evaluate performance against a single task

## Related Concepts

[[Cost Control vs. Unit Economics]] [[Capability-Aware Scheduling]]
