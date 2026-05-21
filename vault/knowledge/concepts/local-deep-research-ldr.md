---
title: "Local Deep Research (LDR)"
type: concept
sources:
  - 00_inbox/research-queue.md
tags: [auto-generated, phase-6]
created: 2026-05-21
updated: 2026-05-21
---

## Definition

A research method used by the system to process deep-research questions using LDR + Qwen3-14B + SearXNG. It is pinned to version 1.5.6 due to bugs in newer versions.

## Context

Understanding LDR's constraints and status is vital for Sean to manage expectations around the efficiency and accuracy of research outputs.

## Evidence

> LDR is pinned to v1.5.6 awaiting upstream PR [LearningCircuit/local-deep-research#4000](https://github.com/LearningCircuit/local-deep-research/pull/4000) — the 1.5.6 → 1.6.9 upgrade attempted on 2026-05-11 hit a confirmed upstream Alembic-runner bug (migration 0007 FK mismatch on `download_attempts → download_tracker`).

> Check status with: `gh pr view 4000 --repo LearningCircuit/local-deep-research --json state,mergedAt`

## Examples

- The upgrade attempt was rolled back due to an Alembic-runner bug.

## Related Concepts

[[Deep Research Queue]] [[Gemini Deep Research]]
