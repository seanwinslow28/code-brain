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

- [ ] tier: dr Topic 2 — Anthropic API "MCP connector" mode: research the `mcp_servers` parameter on the Messages API, headless `claude login` OAuth inheritance for the Claude Agent SDK 0.1.x line, scope flow for headless agents (no browser-redirect handling), production patterns + code snippets from 2025-2026 Anthropic docs and case studies, and explicit gaps + roadmap signals about MCP+headless capabilities not yet supported. Cite Anthropic's official documentation + SDK source + dated team blog posts.
- [ ] tier: max Topic 4 — Comprehensive auth-mode + key-generation matrix for Slack, Google Calendar, Gmail, Jira, Confluence, GitHub, Linear. Six axes per service: (a) all available auth modes (PAT, OAuth refresh token, OAuth user token, OAuth bot token, service account with/without domain-wide delegation); (b) generation URL/path for each (e.g., https://github.com/settings/tokens for GitHub PATs); (c) scope/permission picker mechanics; (d) rotation/expiration model (default lifetime, programmatic rotation availability); (e) headless-friendliness (works without browser-redirect handling?); (f) typical admin restrictions (which modes commonly require workspace-admin enablement). Output ranks the headless-friendliest path per service. Cite official docs for each mode.

## Done
