---
title: "Runtime-Model Coupling"
type: concept
sources:
  - 02_Areas/Agent-Fleet/daily-fleet-status-2026-06-26.md
tags: [auto-generated, phase-6]
created: 2026-06-29
updated: 2026-06-29
---

## Definition

This invariant occurs when the logical dependency of an agent on specific hardware or network conditions is not abstracted away, causing the agent's availability to be directly tied to the physical state of a single machine. Instead of a distributed, resilient architecture where agents can migrate or fallback, the runtime model couples the agent's identity to a specific endpoint (e.g., MBP vs. Mac Mini). This coupling creates a single point of failure for critical cognitive tasks, as the agent cannot function if that specific machine is offline or asleep.

## Context

Sean's infrastructure attempts to balance cost and capability by using different machines for different agents. However, placing the vault-synthesizer on the MacBook Pro (MBP) introduces reliability risks because laptops are not always awake or connected, unlike the Mac Mini which serves as the stable host for indexing.

## Evidence

> The fleet's dependency on specific machine states conflicts with the goal of reliable, always-on operation.

> Prioritize resolving vault-synthesizer errors to link concepts, which is vital for all three domains (creative/life-systems).

> Design a clear restructuring pass: migrate all critical agent dependency from flaky machines (MBP/Alienware) to Mac Mini as the stable host.

## Examples

- The vault-synthesizer is scheduled for 2:30 AM on the MBP, but if the laptop sleeps or loses power, the synthesis step is skipped entirely.
- Critical machines like Alienware and ComfyUI remain offline, preventing full cross-machine agent mesh functionality.

## Related Concepts

[[Infrastructure Status]] [[Automation Reliability]] [[Control Plane / Data Plane Split for Agent Fleets]]
