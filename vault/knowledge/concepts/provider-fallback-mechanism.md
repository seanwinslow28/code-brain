---
title: "Provider Fallback Mechanism"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-06-23
updated: 2026-06-23
---

## Definition

A resilience pattern where the system is architected to handle transient failures from a primary service provider by implementing specific error-handling logic rather than relying on automatic retries or external fallbacks. The mechanism involves identifying the specific failure mode (such as malformed input due to provider-specific quirks) and writing targeted parsers or validators that strip non-standard data before processing. This approach prioritizes precision in handling edge cases over broad redundancy, ensuring that the system remains functional even when the provider behaves unexpectedly.

## Context

Sean's agent fleet interacts with external APIs like OpenRouter. When these providers introduce unexpected behaviors (like SSE comments), Sean must manually harden his code to handle them. This highlights the fragility of relying on third-party services without robust, specific error handling, requiring constant vigilance and code updates to maintain stability.

## Evidence

> ignoring :-prefixed lines is the spec-correct handling _strip_sse_padding already does

> Fix: strip leading : comment lines / extract the first balanced {…} before json.loads

## Examples

- failed Fusion calls bill OpenRouter but record $0 locally
- record usage.cost on failure too

## Related Concepts

[[Cost-Capped Agentic Workflows]] [[Automation Reliability]] [[Infrastructure Status]]
