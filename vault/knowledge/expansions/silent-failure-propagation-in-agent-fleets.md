---
title: "How to make `Silent Failure Propagation in Agent Fleets` better"
type: expansion
parent: "[[silent-failure-propagation-in-agent-fleets]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-18
updated: 2026-06-18
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[silent-failure-propagation-in-agent-fleets]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “sentinel values over nulls” as a fleet design pattern**

Anchor it on Tony Hoare’s 2009 talk **“Null References: The Billion Dollar Mistake”** plus Martin Fowler’s **“Special Case”** pattern from *Patterns of Enterprise Application Architecture*.

Pattern to add: every agent output must resolve to one of three explicit states: `valid`, `empty-but-intentional`, or `failed-with-cause`. Never allow raw `null`, empty Markdown, missing JSON fields, or stale files to masquerade as success.

This unlocks a concrete **agent output contract spec** for Code-Brain: frontmatter fields like `producer_status`, `content_freshness`, `source_run_id`, `empty_reason`, and `downstream_safe`. The current concept names the failure, but not the replacement interface. This would let Sean ship a runbook or MCP schema for “failure-aware knowledge artifacts.”

2. **Add “data quality gates” from pipeline engineering, not just agent monitoring**

Anchor it on Barr Moses and Lior Gavish’s book **Data Quality Fundamentals** and Great Expectations’ open-source repo/docs, especially the expectation-suite model.

Pattern to add: treat each nightly artifact like a data product with assertions at the commit boundary: “daily note must include today’s run IDs,” “synthesizer output must cite at least N fresh source files,” “critic expansion cannot be committed if both critics returned timeout,” “stale context must be labeled stale in consumer-visible prose.”

This unlocks an **executable eval suite** for the vault, not just observability. Sean could produce `vault_expectations.yaml` or `knowledge_artifact_tests.py`, then write a portfolio one-pager called “I Applied Data Observability to an Agent Fleet.” The present concept is still incident vocabulary; this turns it into a shippable quality-control system.

3. **Add “Swiss cheese / latent failure” as the contradicting safety frame**

Anchor it on James Reason’s **Human Error** and his Swiss Cheese Model, then pair it with Sidney Dekker’s **The Field Guide to Understanding ‘Human Error’** as the modern corrective.

Pattern to add: stop framing silent failure as one missing health check. Model it as aligned holes across layers: provider response ambiguity, weak adapter normalization, permissive commit rules, stale consumer assumptions, and no user-visible degraded-mode banner.

This unlocks a stronger **postmortem genre**. Instead of “the agent returned null, add a check,” Sean can write incident reviews that identify latent conditions and failed defenses. It also helps with job-hunt positioning: he can show senior judgment by describing agent reliability as a socio-technical control system, not a pile of brittle scripts.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
