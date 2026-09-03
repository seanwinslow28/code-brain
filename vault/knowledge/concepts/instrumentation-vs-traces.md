---
title: "Instrumentation vs. Traces"
type: concept
sources:
  - knowledge/concepts/instrumentation-vs-traces.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

This mechanism distinguishes between aggregated operational metrics that indicate system health and the raw, granular logs of individual interactions required for debugging. Instrumentation provides a summary view through data points like manifest counts or rejection rates, while traces capture the complete context of an LLM exchange, including retrieval results and tool outputs. The underlying invariant is that high-level telemetry cannot explain probabilistic failures; deep analysis requires removing all friction from accessing the raw interaction logs to understand the 'why' behind the metrics.

## Context

Sean's current fleet produces nightly manifests and rejection telemetry but lacks a structured trace collection system. This gap limits his ability to debug why agents fail or produce low-quality outputs, as he can see the failure count but not the specific retrieval or reasoning errors that caused it.

## Evidence

> A trace is the log of one complete interaction — for an LLM product, usually the whole exchange, including what was retrieved, which tools fired, and what came back. Not a metric. The raw thing.

> You must remove all friction from the process of looking at data.

## Examples

- Nightly manifest files
- Full LLM request/response logs

## Related Concepts

[[Agent Fleet Observability Dashboard]] [[Control Room Observability]]
