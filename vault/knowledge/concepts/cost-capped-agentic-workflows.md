---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - 00_inbox/gemini-research-queue.md
tags: [auto-generated, phase-6]
created: 2026-05-28
updated: 2026-05-28
---

## Definition

This mechanism establishes a hard financial ceiling on autonomous agent operations by defining tiered budget caps that dictate which model capabilities are accessible for a given task. The system enforces a trade-off between depth and cost, where high-fidelity synthesis is gated behind higher per-query expenditures, while standard iterative research is constrained by daily and monthly aggregate limits. This creates a scarcity model where the agent must prioritize tasks based on available budget headroom rather than technical feasibility alone.

## Context

Sean is actively managing the financial viability of his automated research infrastructure. By capping monthly spend at $50 and daily spend at $20, he forces a strategic decision on when to deploy expensive 'Deep Research Max' runs versus cheaper 'Deep Research' runs, directly impacting the velocity and quality of his knowledge acquisition.

## Evidence

> Budget caps from agents-sdk/config.toml [gemini.budget]: Per-task: $7.00 max, Daily: $20.00, Monthly: $50.00 (bumped from $20 on 2026-05-07 to absorb DR Max runs)

> Tier markers: dr — Deep Research (~$2–4/query, ~20-30 min): standard iterative web research, max — Deep Research Max (~$5–10/query, ~30-60 min): extended synthesis, more sources, higher quality

## Examples

- Sean manually ran Topic 13, 14, 15, 16, 18, and 19 via external tools (Gemini Advanced, ChatGPT) to avoid burning the API budget, resulting in $0 API spend for those queries.

## Related Concepts

[[Gemini Deep Research]] [[Local Deep Research (LDR)]] [[Token Waste]]
