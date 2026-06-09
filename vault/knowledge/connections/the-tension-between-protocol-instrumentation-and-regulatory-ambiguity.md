---
title: "The Tension Between Protocol Instrumentation and Regulatory Ambiguity"
type: connection
connects:
  - Resilience Engineering: Work-as-Imagined vs Work-as-Done
  - Control Architecture as Evangelism
  - Supervision as the New AI Edge
created: 2026-06-09
updated: 2026-06-09
---

## Synthesis

There is a fundamental tension between the need for precise, automated protocol instrumentation (like OCR and GL coding) and the ambiguity of regulatory requirements (like SOC 2 controls). This tension manifests in the 'work-as-done' where agents must handle exceptions that fall outside clear rules, requiring human-in-the-loop verification. The consequence is that automation cannot be fully autonomous; it must be designed with explicit fallback mechanisms for ambiguous or high-risk scenarios.

## Threads

### [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]

> Exceptions (price/qty mismatch, missing PO, duplicate, fraud flag) route to a human; track exception rate by type + resolution time.

### [[Control Architecture as Evangelism]]

> Core rule: the same person must not create/change a vendor, approve its invoice, AND release payment. Enforced via role-based access.

### [[Supervision as the New AI Edge]]

> The bank-account-change event is the single highest-risk moment in AP and needs dedicated controls (dual approval + independent verification) beyond normal workflow.

## Implications

- Sean must design his AP agent spec to explicitly model exception handling paths, not just the happy path, to demonstrate operational maturity.
- The job hunt narrative should highlight how he balances automation efficiency with regulatory compliance through architectural choices.
