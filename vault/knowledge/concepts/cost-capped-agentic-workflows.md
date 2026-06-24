---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-06-24
updated: 2026-06-24
---

## Definition

This mechanism refers to the architectural necessity of decoupling financial accounting from functional success in agent loops. When an agent invocation fails functionally (e.g., due to parsing errors or timeouts) but still consumes API resources, the billing system records a cost while the local state machine records zero progress. This creates a 'leaky bucket' invariant where financial expenditure accumulates independently of value generation, requiring explicit failure-path instrumentation to maintain accurate ROI metrics.

## Context

Sean is building a job-hunt and research fleet where token costs are significant. The current architecture only records spend on success, meaning failed attempts (which still hit OpenRouter) create a blind spot in his cost tracking, potentially masking the true expense of debugging or retry loops.

## Evidence

> failed Fusion calls bill OpenRouter but record $0 locally (`record_spend` is post-success only in `__main__.py`) — record usage.cost on failure too.

> The 'two runs failed' were Phase-2, pre-fix. Residual is confidence only (a few live runs incl. deep).

## Examples

- OpenRouter processing lines are documented SSE keep-alive comments that must be stripped before JSON parsing to prevent `JSONDecodeError`.
- The fix involves hardening `_parse` by extracting the first balanced `{…}` before `json.loads` rather than relying on clean payload returns.

## Related Concepts

[[Token Waste]] [[Fleet Status]]
