---
title: "Eval-Driven Agent Coordination"
type: connection
connects:
  - Eval Vocabulary
  - Autonomous Agent Fleets
  - Intent Engineering
created: 2026-05-22
updated: 2026-05-22
---

## Synthesis

The Eval Vocabulary serves as the critical coordination mechanism between Autonomous Agent Fleets and their dependent systems. By embedding evaluation criteria directly into agent workflows, the system ensures output quality while enabling complex parallel processing. This creates a tension between automation efficiency and evaluation overhead, requiring careful calibration to avoid bottlenecks.

## Threads

### [[Eval Vocabulary]]

> Operationalizes the 'evals are the new PRDs' thesis as a portable MCP server.

### [[Autonomous Agent Fleets]]

> Maintains the open-source 118-skill Code-Brain and a 17-agent Claude Agent SDK fleet; published `@swins/intent-engineering-mcp` to npm and the MCP registry.

### [[Intent Engineering]]

> The `audit_intent_spec` tool *is* the eval — it scores a spec against the framework's dimensions and tells the author what's missing before the spec ships to a coding agent.

## Implications

- System designers must balance the overhead of evaluation checks against gains in output quality and system reliability.
- This coordination pattern enables high-throughput processing but requires ongoing refinement of evaluation criteria to adapt to evolving agent capabilities.
