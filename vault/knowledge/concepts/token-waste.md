---
title: "Token Waste"
type: concept
sources:
  - 20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/unified-roadmap-completion-log.md
tags: [auto-generated, phase-6]
created: 2026-05-30
updated: 2026-05-30
---

## Definition

The inefficiency incurred when large volumes of low-signal historical data consume context window capacity, thereby increasing cost and latency while degrading the quality of AI reasoning. It occurs when agents are forced to parse irrelevant past actions alongside current strategic decisions, leading to diluted focus and higher operational expenses. Mitigating this requires strict separation of active state from archival history.

## Context

Sean explicitly identified the accumulation of amendments in the parent roadmap as the 'single largest in-context bloat source,' directly impacting the efficiency of his AI-assisted workflow. By offloading this data, he reduces the token cost per session and improves the relevance of the context provided to his agents.

## Evidence

> Cumulatively those 13 entries were the single largest in-context bloat source for sessions opening the roadmap.

> Entries are preserved verbatim in their original (source-file) order, not strictly chronological — the order reflects how Sean built them up across Cowork sessions.

## Examples

- The decision to move the amendments log to a separate file because the 13 inline entries were causing significant bloat in the parent roadmap's context window.
- The convention of writing new completion logs here rather than appending to the parent to keep the active roadmap slim.

## Related Concepts

[[Unified Roadmap]] [[Agent Health]]
