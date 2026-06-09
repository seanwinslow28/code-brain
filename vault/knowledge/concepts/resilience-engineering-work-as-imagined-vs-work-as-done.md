---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - 20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-06-08-task-26-research-reference-brief.md
tags: [auto-generated, phase-6]
created: 2026-06-09
updated: 2026-06-09
---

## Definition

This concept describes the structural gap between idealized automation flows and the reality of exception handling. In AP systems, the 'work-as-done' is dominated by manual interventions for edge cases like duplicate detection failures or tolerance threshold breaches, rather than the seamless 'work-as-imagined' flow. The system's reliability depends not on preventing all errors, but on how efficiently it routes these exceptions to human judgment when automated controls fail.

## Context

Sean is building an Enterprise AP Agent Spec where correctness-critical claims must be verified against primary sources. Understanding that the 'work-as-done' involves significant exception routing helps him design agents that prioritize robust error handling and verification loops over pure automation speed, ensuring the system remains trustworthy when it deviates from the ideal path.

## Evidence

> Exceptions (price/qty mismatch, missing PO, duplicate, fraud flag) route to a human; track exception rate by type + resolution time.

> The bank-account-change event is the single highest-risk moment in AP and needs dedicated controls (dual approval + independent verification) beyond normal workflow.

## Examples

- Automated duplicate detection can catch a large share pre-payment (one vendor claims 'up to 95%' — marketing ceiling).

## Related Concepts

[[Automation Reliability]] [[Supervision as the New AI Edge]]
