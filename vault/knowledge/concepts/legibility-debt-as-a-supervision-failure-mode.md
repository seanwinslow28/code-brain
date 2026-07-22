---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/concepts/legibility-debt-as-a-supervision-failure-mode.md
tags: [auto-generated, phase-6]
created: 2026-07-22
updated: 2026-07-22
---

## Definition

Legibility debt is the structural gap that emerges when automated concept generation velocity exceeds the human supervisor's capacity for semantic verification, creating an illusion of system health driven by high completion rates rather than verified value. This debt accumulates silently because standard observability metrics report successful task completions while ignoring the quality or relevance of the output, forcing the supervisor into a forensic audit mode that erodes trust in the tooling. The mechanism relies on the fact that operational activity is easily quantifiable, whereas semantic integrity requires slow, manual inspection, leading to a systemic trust deficit where the tool appears healthy but generates noise.

## Context

Sean is scaling his agent fleet from generating 3 concepts per run to over 150, yet his ability to verify the quality of these outputs has not scaled proportionally. This creates a critical bottleneck where the value of the automation is obscured by the sheer volume of unverified data, threatening the long-term viability of the vault as a trusted knowledge base because he can no longer distinguish signal from noise without manual intervention.

## Evidence

> As Sean scales the concept generation from 3 to 153 concepts per run, the mechanisms for reporting status lag behind, creating a legibility gap.

> Robust protocol instrumentation masks epistemic blindness, creating an illusion of health that is particularly dangerous in creative contexts.

## Examples

- The fleet generates 103 concepts in one run but Sean cannot verify their quality without manual intervention.
- Dashboards highlight successful completions while ignoring the missing data or silence that indicates a lack of value.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Agent Fleet Observability Dashboard]]
