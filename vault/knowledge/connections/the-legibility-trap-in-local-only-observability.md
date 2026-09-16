---
title: "The Legibility Trap in Local-Only Observability"
type: connection
connects:
  - Instrumentation vs. Traces
  - Operational Visibility vs. Semantic Value in Agent Fleets
  - Legibility Debt as a Supervision Failure Mode
created: 2026-09-16
updated: 2026-09-16
---

## Synthesis

When Sean restricts data to local-only storage, he eliminates the external semantic enrichment that cloud providers often supply, forcing him to bear the full cost of defining 'semantic value' internally. This creates a tension where high operational visibility (capturing all spans) becomes useless without significant manual effort to structure it into meaningful traces. The consequence is that 'legibility debt' accumulates rapidly in local setups because the infrastructure does not automatically infer context, unlike cloud-based tools that may apply default semantic conventions.

## Threads

### [[Instrumentation vs. Traces]]

> Research file. Facts and sources only, no recommendation. Question: options for tracing multi-step agent runs on a single laptop, where by default no payload leaves the machine, and a human later reads the trace to find which step went wrong.

### [[Operational Visibility vs. Semantic Value in Agent Fleets]]

> Traces → observations (spans/generations/events) with input, output, metadata, model, usage, cost, latency, parent/child, sessions, users, tags, scores.

### [[Legibility Debt as a Supervision Failure Mode]]

> ve a task the customer actually cares about? The trace records the event. Whether the event was good or bad for the product is a separate question, and it is the one product analytics has to answer.

## Implications

- Sean must prioritize tools that enforce semantic conventions (like OpenInference) over raw data capture to prevent legibility debt from making local traces unreadable.
- The cost of 'full freedom' in JSONL manifests may outweigh its flexibility if Sean lacks the time to build custom parsers for every run format.
