---
title: "Local Deep Research (LDR)"
type: concept
sources:
  - 00_inbox/research-queue.md
tags: [auto-generated, phase-6]
created: 2026-05-16
updated: 2026-05-16
---

## Definition

A research method that uses a specific model, Qwen3-14B, and data sources like SearXNG to process research questions from the Deep Research Queue.

## Context

LDR is essential for Sean's daily research, but it has known constraints and limitations that prevent it from handling complex or multi-target questions effectively.

## Evidence

> LDR has a 900s hard budget. Compound prompts stall around 90 % and produce no output.

> Even when LDR completes, Qwen3-14B can't ground citations across multiple targets and confidently writes fabricated entities, owners, and URLs.

## Examples

- The LDR system is pinned to v1.5.6 awaiting upstream PR #4000.

## Related Concepts

[[Deep Research Queue]] [[System Constraints]]
