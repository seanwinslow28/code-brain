---
title: "Infrastructure Status"
type: concept
sources:
  - 40_knowledge/references/ref-system-design-114-concepts-part-2.md
tags: [auto-generated, phase-6]
created: 2026-06-08
updated: 2026-06-08
---

## Definition

The observable state of the underlying communication channels and network infrastructure that determines the reliability and latency of agent interactions. This status is not just about whether a server is up, but whether the specific transport mechanisms (like WebSocket upgrades or TCP connections) are functional and unblocked by intermediate network devices. It represents the foundational layer upon which all higher-level agent behaviors depend.

## Context

Sean's fleet relies on stable infrastructure to function. If the 'Infrastructure Status' of the WebSocket channel is degraded due to firewall blocks, the entire agentic workflow may fail silently or degrade in performance. Monitoring this status is crucial for diagnosing why agents might not be receiving real-time updates.

## Evidence

> Plus, some proxies/firewalls “block” WebSocket upgrades or long-lived connections, so compatibility can vary.

> WebSockets provide full-duplex, bidirectional communication between client & server over a single TCP connection.

## Examples

- Checking if a firewall is blocking port 443 for WebSocket upgrades.
- Monitoring TCP connection latency to detect network partitions affecting agent sync.

## Related Concepts

[[Runtime-Model Coupling]] [[Agent Health Monitoring]]
