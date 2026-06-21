---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-06-21
updated: 2026-06-21
---

## Definition

This mechanism refers to the architectural requirement that financial accounting for agent operations must be decoupled from execution success. When spend recording is gated behind a success condition, any failure in the processing logic results in unaccounted resource consumption, creating a blind spot in budget management. True cost control requires instrumentation of usage metrics at the point of request submission or response receipt, regardless of the semantic validity of the returned payload.

## Context

Sean is building an agent fleet for job hunting and research where token costs are a primary constraint. Unrecorded spend from failed Fusion calls distorts his understanding of the true cost of discovery, making it impossible to accurately benchmark the efficiency of different model providers or prompt strategies.

## Evidence

> failed Fusion calls bill OpenRouter but record $0 locally because record_spend is post-success only in __main__.py

> run 1 FusionError did not return parseable and run 2 bare JSONDecodeError Expecting value line 181 column 1 char 990

## Examples

- OpenRouter streaming SSE keep-alive comments as padding that choke the unguarded payload extraction in fuse()
- Stripping leading comment lines and extracting the first balanced JSON object before parsing to prevent JSONDecodeError

## Related Concepts

[[Cost-Capped Agentic Workflows]] [[Automation Reliability]] [[Token Waste]]
