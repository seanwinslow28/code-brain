---
title: "Provider Preference Configuration"
type: concept
sources:
  - 20_projects/research/2026-05-14-topic-10-openrouter-automatic-routing-provider-preference-co.md
tags: [auto-generated, phase-6]
created: 2026-05-16
updated: 2026-05-16
---

## Definition

A method of defining how requests are routed across different AI model providers using the `provider` field in OpenRouter, with options like `allow_fallbacks`, `sort_by`, and `require_parameters` to control routing behavior.

## Context

This is particularly important for Sean's cost-capped personal agentic workflows (~$5/day across ~14 agents), where optimizing both cost and performance is critical.

## Evidence

> The `provider` field in OpenRouter enables developers to define how requests are routed across different providers. It supports several key parameters: allow_fallbacks, sort_by, and require_parameters.

> This is particularly useful for ensuring high availability and reliability in production environments.

## Examples

- allow_fallbacks: Ensures system reliability by attempting to route requests to a fallback provider if the primary one fails.
- sort_by: Routes requests based on price, throughput, or latency to optimize for cost or speed.

## Related Concepts

[[Agent Health and Daily Routine Automation]] [[Automation Reliability]]
