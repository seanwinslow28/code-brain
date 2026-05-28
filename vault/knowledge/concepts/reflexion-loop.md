---
title: "Reflexion Loop"
type: concept
sources:
  - 20_projects/research/2026-05-27-topic-21-reflexion-style-self-critique-loops-in-production-l.md
tags: [auto-generated, phase-6]
created: 2026-05-28
updated: 2026-05-28
---

## Definition

A production pattern where an autonomous agent captures the specific failure mode of a previous attempt—comprising the action taken, the context, and the outcome—and converts it into a structured lesson that is persisted for future retrieval. This mechanism enforces a dependency between the agent's write path (storing the lesson) and its read path (surfacing the lesson), ensuring that the agent's state evolves based on empirical evidence rather than static configuration. The loop requires a retrieval trigger, such as an always-on prepend or a similarity match, to inject this historical data into the current context window before the next decision point.

## Context

Sean is building a personal autonomous-agent fleet on macOS launchd. Without this loop, his agents will repeat the same configuration errors or tool-use failures indefinitely, wasting token budgets and failing to achieve complex multi-step goals. The minimum-viable implementation for his stack relies on a simple JSON structure and a flat-file or in-context buffer persistence layer.

## Evidence

> The canonical Reflexion-style self-critique loop for production LLM agents involves several key components: the lesson data structure, the persistence layer, and the retrieval trigger.

> The lesson data structure is a critical component of the Reflexion loop, designed to capture key insights from a failed attempt.

## Examples

- Lesson data structure contains: Agent ID, Action Taken, Context, Outcome, Reflection, and Improvement Plan.
- Retrieval trigger options include always-on prepend for simplicity or an explicit recall tool for selective application.

## Related Concepts

[[Local Deep Research (LDR)]] [[Deep Research Queue]]
