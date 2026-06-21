---
title: "Silent Failure Propagation in Agent Fleets"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-06-20
updated: 2026-06-20
---

## Definition

This pattern describes a class of bugs where an upstream agent produces a valid but semantically empty output (such as `null` content), which downstream agents treat as a successful state rather than an error condition. Because the failure is silent at the source, it propagates through the pipeline until a rigid consumer (like a string joiner) encounters the invalid type and crashes. The critical invariant here is that success in one layer (the run completed) does not guarantee validity in the next layer (the data structure is intact), creating a hidden dependency on non-null assertions across agent boundaries.

## Context

Sean's fleet relies on multiple LLM models (Gemini, Qwen, etc.) returning structured JSON. When one model returns null content due to safety filters or timeouts, the transcript renderer fails catastrophically because it assumes all responses are strings. This breaks the observability loop, preventing Sean from seeing that the run actually succeeded, which masks the true reliability profile of his multi-model strategy.

## Evidence

> gemini-pro returned null; recovered by reconstructing the .md from the session JSON archive

> _render_markdown appends r["content"] (None) to lines, so "\n".join(lines) raises TypeError: sequence item N: expected str instance, NoneType found and the whole transcript fails to write even though the run + spend succeeded

## Examples

- The `llm-council` transcript render crashes when any council model returns null content
- Recovering the .md from the session JSON archive instead of relying on the rendered markdown

## Related Concepts

[[Automation Reliability]] [[Infrastructure Status and Agent Failure]] [[Silent Failure Propagation in Agent Fleets]]
