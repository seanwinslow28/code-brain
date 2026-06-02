---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-06-02
updated: 2026-06-02
---

## Definition

This pattern describes a constraint architecture where agent execution is gated by strict financial thresholds rather than just technical success. When a specific integration method, such as an MCP bridge, causes costs to double and trigger hard caps, the system must revert to cheaper, read-only injection patterns to maintain viability. The mechanism relies on identifying the cost driver of a dependency and replacing it with a low-overhead alternative that preserves the data flow without the financial penalty.

## Context

Sean is operating under tight budget constraints for his agent fleet. The recent failure of the MCP bridge due to cost caps demonstrates that technical elegance must yield to economic sustainability. He needs to ensure that future agent interactions, particularly those involving memory or ticketing, do not inadvertently trigger these caps, which would halt his job-hunt automation entirely.

## Evidence

> drop MCP bridge + context-management beta that doubled cost to $0.97 and tripped the cap 5/29

> Build a $0/run local summarizer ... that curates daily_driver's fleet-memory namespace, so the Opus agent only reads, never writes

## Examples

- Reverting to inject_memories_into_prompt() to avoid the $0.97 cost spike
- Using local models like gemma4:e4b on a Mac Mini for $0/run summarization

## Related Concepts

[[Context Management as a Bottleneck]] [[Agent Health Monitoring]]
