---
title: "MCP Server Hardening"
type: concept
sources:
  - knowledge/concepts/mcp-server-hardening.md
tags: [auto-generated, phase-6]
created: 2026-06-04
updated: 2026-06-04
---

## Definition

This mechanism defines a structural constraint on agent behavior by replacing vague error envelopes with explicit, categorized failure modes that eliminate the agent's ability to improvise recovery paths. When an MCP tool fails, the response must name the specific error category and the required action, effectively removing the 'room' for the model to hallucinate a plausible but destructive workaround. This shifts the burden of reliability from the model's inference capabilities to the tool's interface design, ensuring that failures are handled deterministically rather than through risky agent-side inference.

## Context

Sean is building a complex agent fleet where tools interact with live systems (databases, file systems). If these tools return ambiguous errors, agents like the synthesizer or job-hunt trackers might 'fix' things incorrectly, leading to data loss or broken pipelines. Hardening MCP servers prevents these silent failures from becoming catastrophic hallucinations.

## Evidence

> If your tool fails and the agent recovers gracefully, you built a tool. If your tool fails and the agent hallucinates a workaround, you built a trap.

> The fix is structured error responses that name the error category and action, leaving no room for improvisation.

## Examples

- Returning a structured JSON error with `isError: true` and a specific `error_category` field instead of a generic text message.
- Defining a fixed set of `required_action` values (e.g., 'retry_with_backoff', 'abort', 'notify_user') that the agent must select from, rather than generating free-text recovery plans.

## Related Concepts

[[Agent Health Monitoring]] [[Infrastructure Status]]
