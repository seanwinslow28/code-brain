---
title: "Recovery-Oriented Computing"
type: concept
sources:
  - knowledge/expansions/connections/automation-reliability-and-daily-outputs.md
tags: [auto-generated, phase-6]
created: 2026-08-27
updated: 2026-08-27
---

## Definition

A design philosophy where systems are built to assume failure is inevitable and focus on rapid, dependable recovery rather than prevention. This mechanism requires every producer to support detection, bounded replay, verification, and rollback capabilities. It shifts the metric of success from 'zero failures' to 'time from missing note detected to trustworthy note restored,' ensuring that transient infrastructure issues do not cascade into long-term data loss or context gaps.

## Context

Sean's current vault lacks a formal recovery runbook, leaving him vulnerable to silent decay when agents fail. Implementing this would allow him to treat agent failures as routine maintenance events rather than critical incidents, stabilizing his knowledge base against the inherent fragility of LLM APIs.

## Evidence

> Every daily-output producer must support detection, bounded replay, verification, and rollback; a killed dependency at 08:29 must yield either a verified artifact or an explicit degraded-state manifest by 08:45.

> Designing for rapid, dependable recovery can outperform attempts to prevent every failure.

## Examples

- A fleet-recovery runbook plus an executable GameDay demo that kills Ollama, removes MBP availability, corrupts an intermediate artifact, and measures recovery.
- Track “time from missing note detected to trustworthy note restored.”

## Related Concepts

[[Fault → Error → Failure Taxonomy]] [[Silent Decay in Strategic Pipelines]]
