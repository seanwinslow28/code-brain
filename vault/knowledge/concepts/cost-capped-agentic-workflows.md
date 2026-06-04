---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - knowledge/connections/cost-vs-automation-depth-tension.md
tags: [auto-generated, phase-6]
created: 2026-06-04
updated: 2026-06-04
---

## Definition

This pattern describes a constraint architecture where agent execution is gated by strict financial thresholds rather than just technical success. When a specific integration method, such as an MCP bridge, causes costs to double and trigger hard caps, the system forces a retreat to simpler, cheaper patterns. This creates a resilience engineering trade-off where the automation architecture prioritizes sustainability and $0-run local solutions over seamless, complex integrations. The consequence is that Sean must constantly evaluate whether the value of an automated feature justifies its cost, leading to a preference for local, $0-run models for any new automation.

## Context

Sean's infrastructure is currently limited by hard financial caps that break complex integrations. This forces a strategic pivot away from deep, seamless automation toward resilient, low-cost local solutions to avoid triggering these caps.

## Evidence

> drop MCP bridge + context-management beta that doubled cost to $0.97 and tripped the cap 5/29

> Sean must prioritize local, $0-run models for any new automation to avoid cost caps.

## Examples

- Dropping the MCP bridge to avoid tripping the cost cap
- Building a $0/run local summarizer that curates daily_driver's fleet-memory namespace

## Related Concepts

[[Agent Health Monitoring]] [[Vault Maintenance]]
