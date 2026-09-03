---
title: "Privacy-Aware Data Routing"
type: concept
sources:
  - knowledge/connections/the-privacy-velocity-trade-off-in-automated-observability.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

This concept defines the architectural requirement for separating sensitive data streams from operational observability channels to prevent accidental exposure. It involves implementing hard redaction layers and gitignore rules that ensure sensitive material, such as job-hunt strategies, never enters public or semi-public repositories. The mechanism relies on enforcing boundaries at the point of ingestion, rather than relying on post-hoc scrubbing or luck. This approach treats privacy not as an add-on feature but as a fundamental constraint on data flow, ensuring that operational health metrics do not compromise strategic integrity.

## Context

Sean's operating-model source is currently gitignored to keep material local, but the agent fleet's automated reports have bypassed this protection by quoting sensitive data. This creates a need for a hard redaction layer in the emitter (`knowledge_lint.py`) that prevents any raw SOUL text from entering the report. The current system's reliance on luck for privacy is unsustainable and requires a structural shift to ensure semantic isolation.

## Evidence

> The operating-model source (`vault/05_atlas/operating-models/`) is gitignored precisely so this material stays local.

> Sean must implement a hard redaction layer in the emitter (`knowledge_lint.py`) that prevents any raw SOUL text from entering the report, regardless of whether the report itself is committed or untracked.

## Examples

- The gitignore rule applied to `vault/05_atlas/operating-models/` to keep operating model data local.
- The proposed implementation of a hard redaction layer in `knowledge_lint.py` to block raw SOUL text from reports.

## Related Concepts

[[The Masking Effect of Structural Completeness in Failed Automation]] [[Legibility Debt as a Supervision Failure Mode]]
