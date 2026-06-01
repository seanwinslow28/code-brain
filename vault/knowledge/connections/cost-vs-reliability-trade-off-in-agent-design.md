---
title: "Cost vs. Reliability Trade-off in Agent Design"
type: connection
connects:
  - Cost-Capped Agentic Workflows
  - Human-in-the-Loop Gate
  - Automation Reliability
created: 2026-06-01
updated: 2026-06-01
---

## Synthesis

There is a direct tension between the desire for rich, context-aware agent interactions and the economic constraints of running them at scale. Sean's experience shows that adding complexity (like MCP bridges) can exponentially increase costs, forcing a retreat to simpler, local, or $0-run alternatives. This trade-off dictates the architecture of his job-hunt tools, prioritizing reliability and cost-efficiency over feature richness.

## Threads

### [[Cost-Capped Agentic Workflows]]

> drop MCP bridge + context-management beta that doubled cost to $0.97 and tripped the cap 5/29

### [[Human-in-the-Loop Gate]]

> writes a top-N shortlist to a SEPARATE suggestions lane (NOT the hand-curated Manual Todo) for Sean to review and promote

### [[Automation Reliability]]

> recent runs show status=partial / ag_fail=5; don't triage noise

## Implications

- Sean must prioritize local, low-cost models for high-frequency tasks to avoid triggering financial caps.
- Human-in-the-loop gates are essential for maintaining reliability when automated systems are prone to failure or noise.
