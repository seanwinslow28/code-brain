---
title: "Deep Research System Constraints"
type: connection
connects:
  - Deep Research Queue
  - Local Deep Research (LDR)
  - Gemini Deep Research
created: 2026-05-14
updated: 2026-05-14
---

## Synthesis

The interaction between the Deep Research Queue, Local Deep Research (LDR), and Gemini Deep Research defines a system that prioritizes quality, efficiency, and scalability in research processing.

## Threads

### [[Deep Research Queue]]

> Drop research questions here as `- [ ] question`. The nightly `deep-researcher` agent (02:45) picks the first unchecked item, runs Local Deep Research (LDR + Qwen3-14B + SearXNG), writes the full report to `vault/20_projects/research/`, and marks the question done with a link.

### [[Local Deep Research (LDR)]]

> LDR has a 900s hard budget. Compound prompts stall around 90 % and produce no output.

### [[Gemini Deep Research]]

> Both topics were re-run on Gemini DR successfully.

## Implications

- This system highlights the importance of categorizing research topics appropriately (simple vs compound) to ensure efficiency and quality of outcomes.
