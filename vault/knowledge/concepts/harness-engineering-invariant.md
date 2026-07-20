---
title: "Harness Engineering Invariant"
type: concept
sources:
  - knowledge/concepts/harness-engineering-invariant.md
tags: [auto-generated, phase-6]
created: 2026-07-20
updated: 2026-07-20
---

## Definition

This invariant posits that agent reliability is inversely proportional to the complexity of its surrounding harness, as every added tool or permission expands the failure surface non-linearly. The maintenance burden scales with the number of external dependencies rather than the intelligence of the underlying model, making simplification a more potent optimization strategy than scaling compute. Consequently, reducing the number of active tools often yields greater stability gains than upgrading to larger language models.

## Context

Sean's vault synthesizer has shifted from qwen3-14b to qwen3.6-35b-a3b-32k, yet the primary metric for success is not raw output volume but the reduction of rejected concepts and debugging time. Understanding this invariant explains why the newer model does not automatically solve previous reliability issues if the input context remains overly complex.

## Evidence

> Whether the harness is small or large, the parts that need care are the same, and they are more specific than “keep it healthy” suggests.

> You are investing in the long-term maintenance of an agent and harness system.

## Examples

- Adding a new MCP server to an agent's configuration increases its potential failure modes from 10 to 50, requiring new logging and error handling for each connection point.
- Removing three rarely-used tools from an agent's definition reduces the time spent debugging 'why did it do that?' by half because there are fewer possible actions to trace.

## Related Concepts

[[Agent Health]] [[SRE Error Budget for Agents]]
