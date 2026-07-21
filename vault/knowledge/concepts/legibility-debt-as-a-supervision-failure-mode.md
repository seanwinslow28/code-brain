---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/velocity-vs-legibility-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-21
updated: 2026-07-21
---

## Definition

Legibility debt emerges when the rate of automated concept generation outpaces the human capacity to verify semantic integrity, creating a gap between operational activity and perceived value. This debt accumulates silently because standard observability metrics report successful completions rather than the quality or relevance of the output. The supervisor is forced into a forensic mode where they must manually audit the system's health, leading to a systemic trust deficit as the tool appears healthy while generating noise.

## Context

Sean is scaling his agent fleet from 3 concepts per run to over 150, yet his ability to verify the quality of these outputs has not scaled proportionally. This creates a critical bottleneck where the value of the automation is obscured by the sheer volume of unverified data, threatening the long-term viability of the vault as a trusted knowledge base.

## Evidence

> As Sean scales the concept generation from 3 to 153 concepts per run, the mechanisms for reporting status lag behind, creating a legibility gap.

> Robust protocol instrumentation masks epistemic blindness, creating an illusion of health that is particularly dangerous in creative contexts.

## Examples

- The fleet generates 103 concepts in one run but Sean cannot verify their quality without manual intervention.
- Dashboards highlight successful completions while ignoring the missing data or silence that indicates a lack of value.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Agent Fleet Observability Dashboard]]
