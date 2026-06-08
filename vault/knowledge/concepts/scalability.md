---
title: "Scalability"
type: concept
sources:
  - 40_knowledge/references/ref-system-design-114-concepts.md
tags: [auto-generated, phase-6]
created: 2026-06-08
updated: 2026-06-08
---

## Definition

Scalability is defined as the system’s ability to handle increased load without breaking, manifesting through two distinct mechanisms: vertical scaling (adding power to an existing machine) and horizontal scaling (distributing work across multiple machines). This concept establishes a fundamental trade-off between hardware investment and architectural complexity. The mechanism requires distinguishing between capacity expansion via resource density versus capacity expansion via distribution topology.

## Context

Sean is building agent fleets and MCP servers where load handling directly impacts reliability. Understanding the distinction between vertical and horizontal scaling is critical for deciding whether to upgrade his local Mac or distribute tasks across a fleet of agents.

## Evidence

> Scalability is the system’s ability to handle increased load without breaking.

> Vertical scaling means adding more power to your existing machine, such as a larger CPU, more RAM, or a faster disk.

> Horizontal scaling means adding more machines to distribute the work across multiple servers.

## Examples

- Adding more RAM to a single server
- Distributing work across multiple servers

## Related Concepts

[[Availability]] [[Reliability]]
