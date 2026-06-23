---
title: "Context Compounding"
type: concept
sources:
  - 20_projects/substack-studio/MIGRATION-REPORT.md
tags: [auto-generated, phase-6]
created: 2026-06-23
updated: 2026-06-23
---

## Definition

This pattern refers to the accumulation of editorial and research artifacts across multiple files to create a dense, reusable knowledge base that reduces the cognitive load for future agentic writing tasks. Instead of treating each post as an isolated event, the system consolidates 'spine' documents, deep-dive research JSONs, and style anchors into a unified folder structure. This compounding effect allows subsequent agents to retrieve not just the immediate draft context, but the entire historical reasoning chain, including discovery sessions and opportunity reports, thereby increasing the fidelity and consistency of the generated content over time.

## Context

Sean's Substack workflow relies on deep research and consistent voice. By consolidating 83 files (including 5 deep-dives and 2 discovery JSONs) into `substack-studio`, he ensures that the 'Raising Claude' series benefits from a growing reservoir of contextual evidence, rather than starting each post from scratch.

## Evidence

> research/ — opportunity-report-creative-agentic.md (spine) + deep-dives/ (5) + last30days/ (6) + discovery/ (2 ledgers + discovery-sessions/ 3 JSONs).

> SERIES-COMMAND-CENTER.md (the drafts README.md, renamed so it doesn't collide with the stub).

## Examples

- The inclusion of 'hero-prompt.txt' and 'kits' in each post folder allows for rapid regeneration of visual assets without re-querying the model.
- The use of '_seed.md' files provides a structured starting point for new posts, leveraging previous editorial decisions.

## Related Concepts

[[Context Compounding]] [[Creative Studio Workflows]]
