---
type: research-queue
description: Questions for Gemini Deep Research. Tier markers indicate which model to use. Agent picks the first unchecked item, calls the Interactions API, writes a topical note to vault/20_projects/research/, injects a digest into today's daily note, and marks done with timestamp + output link.
---

# Gemini Deep Research Queue

Drop research questions here as `- [ ] {tier} {refined question}`.

**Tier markers:**
- `dr` — Deep Research (~$2–4/query, ~20-30 min): standard iterative web research
- `max` — Deep Research Max (~$5–10/query, ~30-60 min): extended synthesis, more sources, higher quality

The `gemini-dr` script (Phase 2 skill + Phase 3 agent) reads this queue,
calls Gemini's Interactions API in background mode, polls until completion,
and writes the full report to `vault/20_projects/research/`.

Budget caps from `agents-sdk/config.toml [gemini.budget]`:
- Per-task: $7.00 max
- Daily: $10.00
- Monthly: $20.00

## Pending

- [x] tier: dr Topic 2 — Anthropic API "MCP connector" mode: research the `mcp_servers` parameter on the Messages API, headless `claude login` OAuth inheritance for the Claude Agent SDK 0.1.x line, scope flow for headless agents (no browser-redirect handling), production patterns + code snippets from 2025-2026 Anthropic docs and case studies, and explicit gaps + roadmap signals about MCP+headless capabilities not yet supported. Cite Anthropic's official documentation + SDK source + dated team blog posts. — done 2026-05-04 17:22 (manual gemini-dr run, $2.80) → [[20_projects/research/2026-05-04-you-are-a-senior-research-analyst-specializing-in-ai-develop]]

## Deferred (post-severance review)

- [x] tier: max Topic 4 — Auth-mode + key-generation matrix across 7 services (Slack, Google Calendar, Gmail, Jira, Confluence, GitHub, Linear) on six axes (auth modes, generation URL, scope picker, rotation/expiration, headless-friendliness, admin restrictions) with master ranked comparison table for personal-account headless agents. _Originally deferred 2026-05-04 for $3–7 API cost; unblocked 2026-05-08 after severance landed._ — done 2026-05-08 14:27 (manual gemini-dr run, DR Max, 719s, $7.00) → [[20_projects/research/2026-05-08-topic-4-you-are-a-senior-security-architect-specializing-in-headless]]

## Done
