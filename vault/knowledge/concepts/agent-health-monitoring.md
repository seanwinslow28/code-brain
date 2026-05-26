---
title: "Agent Health Monitoring"
type: concept
sources:
  - 02_Areas/Agent-Fleet/daily-fleet-status-2026-05-24.md
tags: [auto-generated, phase-6]
created: 2026-05-26
updated: 2026-05-26
---

## Definition

A monitoring framework that evaluates the status and reliability of agents within Sean's vault ecosystem. This involves tracking whether agents like 'vault-synthesizer' or 'daily-driver morning' run successfully and without error. It reflects a dependency between agent health metrics and the quality of downstream knowledge workflows.

## Context

Sean relies on agents to automate his workflow and maintain consistency across domains. If an agent like 'daily-driver morning' fails or runs with errors, it disrupts the daily note generation and, by extension, affects how knowledge is indexed, synthesized, and reviewed later.

## Evidence

> 'vault-indexer' ran successfully in the early morning, with no errors reported.

> The 'daily-driver morning' agent ran successfully and updated the timeline/vault with minimal delay.

## Examples

- 'vault-synthesizer' ran successfully, with no errors reported.
- The 'daily-driver morning' agent ran successfully and created a daily note in the vault.

## Related Concepts

[[Infrastructure Status and Agent Failure]] [[Indexing and Synthesis]] [[Automation Reliability]]
