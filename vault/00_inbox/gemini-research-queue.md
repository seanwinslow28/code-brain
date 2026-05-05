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

- [ ] tier: max Topic 4 — **DEFERRED 2026-05-04 pending post-severance financial check-in.** Rationale: $3–7 single-call spend is the most expensive item in the queue, and the layoff (2026-05-04) means no income until severance lands. The portfolio-build priority (first public MCP server by 2026-05-25 per [[20_projects/prj-job-hunt-2026/README]]) is informed first by Topic 2's headless-OAuth findings — if Topic 2 surfaces the right auth mode for the personal MCP server, Topic 4's full 7-services × 6-axes matrix can be scoped down or replaced. Re-evaluate after severance lands AND after Topic 2's report is read.
  - Original prompt text (auth-mode + key-generation matrix for Slack, Google Calendar, Gmail, Jira, Confluence, GitHub, Linear; six axes per service: auth modes, generation URL/path, scope/permission picker, rotation/expiration, headless-friendliness, admin restrictions; ranks headless-friendliest path per service).
  - Recommended re-engineering before firing per `phase-4-night-1-2026-05-03.md` §"Topic 4 prompt" — current line is plan-spec language, not prompt-engineered. DR Max output quality scales with prompt precision.

## Done
