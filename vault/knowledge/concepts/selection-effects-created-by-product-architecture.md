---
title: "Selection Effects Created by Product Architecture"
type: concept
sources:
  - knowledge/concepts/selection-effects-created-by-product-architecture.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

Data collected for one purpose inherently carries the shape and biases of that original intent, creating selection effects that distort its utility when repurposed. This bias is particularly dangerous because it is invisible to those who did not design the original collection mechanism, leading to flawed analyses when the data is used for new objectives. The architecture of the product determines what data is captured, how it is structured, and what is ignored, all of which constrain future analytical possibilities.

## Context

Sean's existing data sources—logs, transactions, documents—are collected for operational purposes, not for understanding user choice dynamics or economic incentives. This means his current infrastructure is fundamentally misaligned with the requirements of AI Product Management, which demands an understanding of these external validity layers.

## Evidence

> Data you already have. Logs, transactions, documents, support tickets. Cheapest and most dangerous, because it was collected for a different purpose and carries the shape of that purpose.

> Sean must stop treating his current indexing pipeline as sufficient preparation for AI PM roles, recognizing that technical robustness does not equate to product sense.

## Examples

- Logs and transactions collected for operational purposes carry biases that distort their utility for understanding user choice dynamics.
- The original purpose of data collection constrains its future analytical possibilities, creating selection effects that are invisible to the operator.

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Supervision as the New AI Edge]]
