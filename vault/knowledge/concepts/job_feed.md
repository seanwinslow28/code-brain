---
title: "job_feed"
type: concept
sources:
  - CLAUDE.md
  - agents-sdk/agents/job_feed.py
  - vault/20_projects/prj-job-hunt-2026/target-companies.md
tags: [reference, hand-written, infrastructure]
created: 2026-05-20
updated: 2026-05-20
---

## Definition

`job_feed` is the autonomous SDK agent (added in v3.28.0) that aggregates job listings into Sean's vault for the active `prj-job-hunt-2026` project. It pulls from four free public feeds plus a curated ~40-company ATS watchlist, writes new postings to a SQLite table, and renders a Markdown roll-up. It runs seven times a day (08:00–11:00 fires on launchd) and uses the HybridRouter pointed at Qwen3-14B on the MBP (`fallback_disabled=true`) so each run costs $0.

## Context

The agent exists because job-board polling is the kind of low-stakes, high-frequency task that suits a local model: deduplication and freshness matter more than reasoning quality, and the fallback-disabled router setting keeps the daily $0.50 SDK cap from being burned on a feed pull when the MBP is asleep. It's a deliberately narrow agent — no LLM-written summaries in the rollup, no scoring, just deduped freshness against the watchlist.

## Evidence

> Job Feed (NEW v3.28.0): 8:00–11:00 AM (7 fires); Qwen3-14B on MBP via HybridRouter (`fallback_disabled=true`); 4 free public feeds + ~40-company ATS watchlist; SQLite + Markdown roll-up; $0.00/run.

> The agent is one of 8 active autonomous SDK agents running outside Claude Code sessions on macOS launchd schedules.

## Examples

- A new posting at one of the watchlist companies shows up on the morning 09:00 roll-up that wasn't there at 08:00.
- The Markdown roll-up at `vault/20_projects/prj-job-hunt-2026/` is what the morning Daily Driver agent links to in its brief.
- A feed that returns an HTTP 5xx error gets logged and skipped without affecting the other six feeds.

## Related Concepts

[[knowledge_loop]]
