---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - knowledge/connections/cost-vs-automation-depth-tension.md
tags: [auto-generated, phase-6]
created: 2026-06-05
updated: 2026-06-05
---

## Definition

This pattern describes a constraint architecture where agent execution is gated by strict financial thresholds rather than just technical success. When a specific integration method, such as an MCP bridge, doubles the operational cost and triggers a hard cap, the system forces a retreat to simpler, cheaper patterns. This creates a dynamic where automation depth is inversely proportional to financial risk, prioritizing local, $0-run solutions over seamless but expensive cloud integrations. The invariant here is that sustainability dictates architectural complexity, not user convenience.

## Context

Sean's infrastructure relies on avoiding cost caps to maintain continuous operation. By recognizing that complex integrations like MCP bridges can double costs and trip limits, he can proactively choose local models that ensure reliability without financial interruption.

## Evidence

> drop MCP bridge + context-management beta that doubled cost to $0.97 and tripped the cap 5/29

> Build a $0/run local summarizer ... that curates daily_driver's fleet-memory namespace

## Examples

- Retreating from an MCP bridge after it doubled costs and triggered a hard cap on May 29th.
- Building a local summarizer for the daily_driver namespace to maintain $0/run operations.

## Related Concepts

[[Agent Health Monitoring]] [[Vault Maintenance]]
