---
title: "Accountability Gap"
type: concept
sources:
  - knowledge/index.md
tags: [auto-generated, phase-6]
created: 2026-06-03
updated: 2026-06-03
---

## Definition

This pattern emerges when a system component fails to produce its expected output, but no explicit error is raised, leaving the downstream consumer to infer the failure from the absence of data. The gap exists between the agent's internal state (which may believe it succeeded) and the user's external reality (which lacks the expected artifact). This gap is dangerous because it shifts the burden of verification from the system to the user, who must manually audit the output to ensure integrity.

## Context

Sean's job hunt and creative work depend on the accuracy and timeliness of his vault's data. An accountability gap means he cannot trust the system to alert him to problems, forcing him to become the auditor of his own automation, which is a inefficient use of his cognitive resources.

## Evidence

> The dependency is invisible in each agent's source, meaning the failure is only detected by the user's manual inspection of the output.

> Sean notices the staleness of his morning brief before the brief itself flags the failure, indicating a lag in error detection.

## Examples

- Sean has to manually check the vault synthesizer's logs to confirm if the daily note was generated, rather than receiving an alert.

## Related Concepts

[[Automation Failure and Daily Note Disruption]] [[Agent Health Monitoring]]
