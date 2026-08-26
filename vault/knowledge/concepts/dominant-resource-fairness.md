---
title: "Dominant Resource Fairness"
type: concept
sources:
  - knowledge/concepts/dominant-resource-fairness.md
tags: [auto-generated, phase-6]
created: 2026-08-25
updated: 2026-08-25
---

## Definition

An allocation policy that tracks each workload class's dominant share of scarce resources—such as GPU time, RAM, and latency budget—to prevent starvation in heterogeneous environments. It extends traditional fairness models by acknowledging that pretending diverse machines form a single interchangeable resource pool produces poor allocations when nodes have different bottlenecks. This mechanism enforces minimum service guarantees and queue aging to balance urgent jobs against opportunistic research tasks.

## Context

Sean's workflow involves competing demands from the Substack drafter, knowledge lint, and LoRA experiments. Without DRFH-inspired policies, these creative and technical workloads compete for the same scarce GPU hours, causing unpredictable delays that undermine the reliability of his automated synthesis pipeline.

## Evidence

> DRFH extends Ghodsi et al.’s DRF specifically because pretending heterogeneous machines form one interchangeable resource pool produces poor allocations.

> Track each class’s dominant share of scarce resources such as GPU time, RAM, latency budget, and awake-machine hours; add queue aging and minimum service guarantees.

## Examples

- Interactive workload receives priority during active hours
- Batch research jobs age in queue to prevent starvation

## Related Concepts

[[Capability-Aware Scheduling]] [[Fairness Policy RFC]]
