---
title: "Cost-Capped Agentic Workflows and Deep Research Integration"
type: connection
connects:
  - Deep Research Queue
  - Cost-Capped Agentic Workflows
  - Gemini Deep Research
created: 2026-05-21
updated: 2026-05-21
---

## Synthesis

The Deep Research Queue enables Sean to manage agentic workflows within strict budget limits while ensuring the efficient execution of research tasks.

## Threads

### [[Deep Research Queue]]

> Budget caps from `agents-sdk/config.toml [gemini.budget]`:

> Per-task: $7.00 max

### [[Cost-Capped Agentic Workflows]]

> Budget caps from `agents-sdk/config.toml [gemini.budget]`:

> Per-task: $7.00 max

### [[Gemini Deep Research]]

> The `gemini-dr` script (Phase 2 skill + Phase 3 agent) reads this queue,

> calls Gemini's Interactions API in background mode

## Implications

- This integration enables Sean to apply Deep Research methods effectively while maintaining financial discipline.
- It informs future tooling and process optimization to balance cost, speed, and quality of agentic workflows.
