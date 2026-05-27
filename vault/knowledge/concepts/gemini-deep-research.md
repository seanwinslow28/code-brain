---
title: "Gemini Deep Research"
type: concept
sources:
  - 00_inbox/research-queue.md
tags: [auto-generated, phase-6]
created: 2026-05-27
updated: 2026-05-27
---

## Definition

Gemini Deep Research is a cloud-based agent tier that handles complex, multi-step research tasks that exceed the capabilities of local tools. It is characterized by its ability to navigate complex information landscapes and produce detailed, cited reports for compound topics. This tier serves as the fallback and primary engine for high-complexity queries that would otherwise stall or fail in local environments. It absorbs the workload that local agents cannot structurally support.

## Context

Sean uses Gemini DR for heavy compound topics and due-diligence matrices. It is essential for maintaining research quality when local tools hit their limits. This tier represents a shift from local automation to cloud-based reliability for complex tasks.

## Evidence

> Heavy compound topics (≥3 sub-questions, multi-target evaluations like compare A/B/C on dimensions 1–4, due-diligence matrices) belong on Gemini DR / DR Max

> The Gemini Deep Research Agent autonomously plans, executes, and synthesizes multi-step research tasks.

## Examples

- Handling multi-target evaluations
- Absorbing compound topics that stall LDR

## Related Concepts

[[System Constraints]] [[Local Deep Research (LDR)]] [[Deep Research Queue]]
