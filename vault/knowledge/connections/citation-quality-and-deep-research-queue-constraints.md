---
title: "Citation Quality and Deep Research Queue Constraints"
type: connection
connects:
  - Deep Research Queue
  - Citation Quality
  - Gemini Deep Research
created: 2026-05-22
updated: 2026-05-22
---

## Synthesis

The Deep Research Queue imposes constraints on topic complexity to ensure high citation quality. By isolating research questions into single-shape prompts, the queue avoids the pitfalls of multi-target processing that often lead to citation inaccuracies. This constraint is a trade-off between throughput and quality, with significant consequences for the integrity of knowledge generated during critical periods like job hunting.

## Threads

### [[Deep Research Queue]]

> Routing rule (v3.26.3, 2026-05-06): This queue is for single-shape topics only — one target, one question, one pattern.

### [[Citation Quality]]

> Citation quality collapse — even when LDR completes, Qwen3-14B can't ground citations across multiple targets and confidently writes fabricated entities, owners, and URLs.

### [[Gemini Deep Research]]

> The Gemini Deep Research Agent autonomously plans, executes, and synthesizes multi-step research tasks. Powered by Gemini, it navigates complex information landscapes to produce detailed, cited reports.

## Implications

- The isolation of topics to single-shape prompts ensures reliable citations but may slow down research progress during high-volume periods.
- The reliance on Gemini Deep Research for complex topics highlights a structural dependency between the two research systems, requiring careful integration planning to avoid bottlenecks.
