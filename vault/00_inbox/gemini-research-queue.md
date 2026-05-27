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
- Daily: $20.00
- Monthly: $50.00 (bumped from $20 on 2026-05-07 to absorb DR Max runs)

## Pending

- [x] tier: dr Topic 13 (RE-RUN) — Pi (pi.dev) platform overview. Ran manually via Gemini DR web UI on 2026-05-21 (API key was expired; Sean ran from his Gemini Advanced subscription to avoid burning the $5.80 May budget headroom). $0 API spend. → [[20_projects/research/2026-05-21-topic-13-pi-platform-overview-gemini-dr-manual]]
- [x] tier: dr Topic 14 (RE-RUN) — Pi extensions / plugins catalog. Ran manually via Gemini DR on 2026-05-21. $0 API spend. → [[20_projects/research/2026-05-21-topic-14-pi-extensions-catalog-gemini-dr-manual]]
- [x] tier: dr Topic 15 — Pi + OpenRouter integration. Ran manually via Gemini DR on 2026-05-21. $0 API spend. → [[20_projects/research/2026-05-21-topic-15-pi-openrouter-integration-gemini-dr-manual]]
- [x] tier: dr Topic 16 — Pi + local Ollama integration. Ran manually via ChatGPT on 2026-05-21 (shorter source than the Gemini-DR ones; primarily a config recipe). $0 API spend. → [[20_projects/research/2026-05-21-topic-16-pi-ollama-integration-chatgpt-manual]]
- [~] tier: skipped Topic 17 — Pi + Gemini CLI interoperability. **Skipped 2026-05-21** — Sean's note: Gemini CLI is being deprecated on 2026-06-18 and replaced by the Anti-Gravity CLI. Re-scope as needed under a new Topic if Anti-Gravity ↔ Pi interop becomes interesting.
- [x] tier: dr Topic 18 — Pi + ChatGPT Codex subscription integration. Ran manually via ChatGPT on 2026-05-21 (high-context source — Sean is logged into Codex). $0 API spend. → [[20_projects/research/2026-05-21-topic-18-pi-chatgpt-codex-integration-chatgpt-manual]]
- [x] tier: dr Topic 19 — Optimal Ollama model for Pi-driven coding + agentic workflows. Ran THREE TIMES manually on 2026-05-21 across Perplexity, Gemini DR, and ChatGPT for cross-vendor variance, then synthesized into a single recommendation. $0 API spend. → sources [[20_projects/research/2026-05-21-topic-19a-optimal-ollama-models-pi-perplexity]] · [[20_projects/research/2026-05-21-topic-19b-optimal-ollama-models-pi-gemini-dr]] · [[20_projects/research/2026-05-21-topic-19c-optimal-ollama-models-pi-chatgpt]] · **canonical synthesis** → [[20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi]]

- [x] tier: dr Topic 2 — Anthropic API "MCP connector" mode: research the `mcp_servers` parameter on the Messages API, headless `claude login` OAuth inheritance for the Claude Agent SDK 0.1.x line, scope flow for headless agents (no browser-redirect handling), production patterns + code snippets from 2025-2026 Anthropic docs and case studies, and explicit gaps + roadmap signals about MCP+headless capabilities not yet supported. Cite Anthropic's official documentation + SDK source + dated team blog posts. — done 2026-05-04 17:22 (manual gemini-dr run, $2.80) → [[20_projects/research/2026-05-04-you-are-a-senior-research-analyst-specializing-in-ai-develop]]
- [x] tier: dr Topic 27 — Long-term memory backends for personal LLM-agent fleets (2026): master comparison of Mem0 vs Letta (formerly MemGPT) vs Zep vs Anthropic native memory tool (`memory_20250818`) vs do-nothing baseline across 10 axes + ranked recommendation. **Ran manually TWICE on 2026-05-26 across Gemini DR and Perplexity DR for cross-vendor variance, then synthesized into a single recommendation.** $0 API spend (both via paid web UIs). Both runs independently converged on adopting Anthropic native `memory_20250818` with shared `/memories/fleet/` mount and explicit per-agent namespacing. → sources [[20_projects/research/2026-05-26-topic-27-long-term-memory-backends-gemini-dr-manual]] · [[20_projects/research/2026-05-26-topic-27-long-term-memory-backends-perplexity-dr-manual]] · **canonical synthesis** → [[20_projects/research/2026-05-27-topic-27-synthesis-long-term-memory-backends]]

## Deferred (post-severance review)

- [x] tier: max Topic 4 — Auth-mode + key-generation matrix across 7 services (Slack, Google Calendar, Gmail, Jira, Confluence, GitHub, Linear) on six axes (auth modes, generation URL, scope picker, rotation/expiration, headless-friendliness, admin restrictions) with master ranked comparison table for personal-account headless agents. _Originally deferred 2026-05-04 for $3–7 API cost; unblocked 2026-05-08 after severance landed._ — done 2026-05-08 14:27 (manual gemini-dr run, DR Max, 719s, $7.00) → [[20_projects/research/2026-05-08-topic-4-you-are-a-senior-security-architect-specializing-in-headless]]

## Done
