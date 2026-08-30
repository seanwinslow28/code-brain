---
title: "Selection Effects Created by Product Architecture"
type: concept
sources:
  - knowledge/connections/the-mechanic-s-blind-spot-internal-consistency-vs-external-validity.md
tags: [auto-generated, phase-6]
created: 2026-08-30
updated: 2026-08-30
---

## Definition

Product architecture inherently shapes the data available for analysis by filtering out user choices and preferences that are not explicitly captured in logs or transactions. This creates a selection bias where the data reflects the system's design rather than the user's true behavior, leading to insights that are 'cheapest and most dangerous' because they appear objective but carry the hidden shape of the collection purpose. Recognizing this effect requires distinguishing between data collected for operational purposes and data that reveals genuine user intent.

## Context

Sean's agent fleet processes data that is 'collected for a different purpose,' which means his insights may be skewed by the architecture's inherent biases rather than reflecting true user behavior. For AI PM work, he must account for these selection effects to avoid building products based on distorted data distributions.

## Evidence

> Data you already have. Logs, transactions, documents, support tickets. Cheapest and most dangerous, because it was collected for a different purpose and carries the shape of that purpose.

> Your agents don't have users whose choices decide which data comes back.

## Examples

- The fleet's indexing pipeline maintains provenance and rejects thin articles, but this internal consistency does not address the external validity problem where data is shaped by user interaction or collected with conflicting incentives.

## Related Concepts

[[Supervision as the New AI Edge]] [[The Illusion of Competence in Automated Systems]]
