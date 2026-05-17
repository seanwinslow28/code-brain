---
title: "Deep Research Queue"
type: concept
sources:
  - 00_inbox/research-queue.md
tags: [auto-generated, phase-6]
created: 2026-05-16
updated: 2026-05-16
---

## Definition

A system for managing research questions that are processed by the deep-researcher agent, which uses Local Deep Research (LDR) to generate reports and write daily-digest lines.

## Context

This system is critical for Sean's workflow as it ensures that research questions are handled efficiently, with routing rules to prevent system overload and ensure quality results.

## Evidence

> The nightly `deep-researcher` agent (02:45) picks the first unchecked item, runs Local Deep Research (LDR + Qwen3-14B + SearXNG), writes the full report to `vault/20_projects/research/`, and marks the question done with a link.

> Routing rule (v3.26.3, 2026-05-06): This queue is for **single-shape topics only** — one target, one question, one pattern.

## Examples

- - [x] Topic 8 — OpenRouter Python integration patterns for the `agents-sdk/` fleet.

## Related Concepts

[[Local Deep Research (LDR)]] [[Gemini Deep Research]]
