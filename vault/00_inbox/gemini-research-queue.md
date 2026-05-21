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

- [ ] tier: dr Topic 13 (RE-RUN) — Pi (pi.dev) platform overview in 2026. What the developer platform at https://pi.dev is (disambiguate from Pi Network crypto and other "Pi" products), launched late-2025 / early-2026. Cover: product surface (CLI vs IDE vs agent harness vs cloud sandbox), pricing tiers + free-tier limits, target user (solo dev vs team), and key differentiators vs Claude Code, Cursor, OpenAI Codex CLI, Gemini CLI, Continue.dev, Aider. Cite the pi.dev homepage + official docs + the 2026 launch coverage on Hacker News / Reddit / changelog. _(LDR re-run of 2026-05-20 was null — Qwen3-14B post-cutoff)_
- [ ] tier: dr Topic 14 (RE-RUN) — Pi extensions / plugins catalog in 2026. Enumerate every Pi extension or plugin available on the official catalog (or community equivalent) as of 2026. For each: name, purpose, license, install command, last-updated, community signal (stars / downloads / Discord mentions). Rank by relevance for a solo developer running a personal autonomous-agent fleet (~14 agents, mixed Python + TypeScript, vault-driven Obsidian knowledge management, daily creative + product-management workflows). Cite the official Pi extensions catalog + 2026 community reviews. _(LDR re-run of 2026-05-21 hallucinated Raspberry Pi)_
- [ ] tier: dr Topic 15 — Pi + OpenRouter integration pattern in 2026. How to configure Pi (pi.dev) to use OpenRouter as a model provider. Cover: auth pattern (`OPENROUTER_API_KEY` env var vs config file), per-task model routing within Pi, cost-tracking + per-day caps, automatic-fallback behavior when a model is rate-limited, and whether Pi can mix OpenRouter with first-party Anthropic/OpenAI keys in the same project. Cite Pi docs + OpenRouter docs + 2026 community recipes.
- [ ] tier: dr Topic 16 — Pi + local Ollama integration pattern in 2026. How to point Pi (pi.dev) at a local Ollama instance (localhost or LAN-reachable Mac Mini / Alienware). Cover: config syntax, OpenAI-compatible endpoint expectations (`/v1/chat/completions`), recommended context-window settings, tool-calling reliability with current Ollama models, latency vs cloud, and any documented gotchas with streaming or `keep_alive`. Cite Pi docs + Ollama docs + 2026 community recipes.
- [ ] tier: dr Topic 17 — Pi + Gemini CLI interoperability in 2026. Can Pi (pi.dev) invoke `gemini` CLI as a sub-tool, or vice versa? Survey integration patterns: shell-out from Pi to `gemini` for specific tasks, any Gemini CLI extension at https://geminicli.com/extensions/ that hands work to Pi, MCP bridge if either side exposes one, and shared-context patterns. Cite Pi docs + Gemini CLI extensions catalog + 2026 community workflows.
- [ ] tier: dr Topic 18 — Pi + ChatGPT Codex (OpenAI coding agent) subscription integration in 2026. How to plug an existing ChatGPT Codex subscription into Pi (pi.dev) — auth pattern, supported model IDs, hybrid workflows where Pi orchestrates Codex for code generation while another model handles planning, and known limitations vs using the OpenAI API key directly. Cite Pi docs + OpenAI Codex docs + 2026 community recipes.
- [ ] tier: dr Topic 19 — Optimal Ollama model for Pi-driven coding + agentic workflows in 2026, ranked by RAM/VRAM tier. Recommend the single best Ollama model (and 1-2 runners-up) for Pi (pi.dev) workloads as of mid-2026, with one row per hardware tier: (a) M4 Max MacBook Pro unified-memory class; (b) M4 Pro Mac Mini 24GB unified memory (always-on headless); (c) NVIDIA RTX 3090/4090-class desktop GPU with 24GB VRAM (Alienware). For each row: model name + parameter count + quantization (Q4_K_M, Q5_K_M, MLX-4bit, etc.), expected tokens/sec, the workload it's best at (tool-calling, code completion, multi-turn reasoning), and the smallest competent alternative for low-RAM sessions. Cite the Ollama library + 2026 r/LocalLLaMA benchmark threads + any published Pi compatibility notes.

- [x] tier: dr Topic 2 — Anthropic API "MCP connector" mode: research the `mcp_servers` parameter on the Messages API, headless `claude login` OAuth inheritance for the Claude Agent SDK 0.1.x line, scope flow for headless agents (no browser-redirect handling), production patterns + code snippets from 2025-2026 Anthropic docs and case studies, and explicit gaps + roadmap signals about MCP+headless capabilities not yet supported. Cite Anthropic's official documentation + SDK source + dated team blog posts. — done 2026-05-04 17:22 (manual gemini-dr run, $2.80) → [[20_projects/research/2026-05-04-you-are-a-senior-research-analyst-specializing-in-ai-develop]]

## Deferred (post-severance review)

- [x] tier: max Topic 4 — Auth-mode + key-generation matrix across 7 services (Slack, Google Calendar, Gmail, Jira, Confluence, GitHub, Linear) on six axes (auth modes, generation URL, scope picker, rotation/expiration, headless-friendliness, admin restrictions) with master ranked comparison table for personal-account headless agents. _Originally deferred 2026-05-04 for $3–7 API cost; unblocked 2026-05-08 after severance landed._ — done 2026-05-08 14:27 (manual gemini-dr run, DR Max, 719s, $7.00) → [[20_projects/research/2026-05-08-topic-4-you-are-a-senior-security-architect-specializing-in-headless]]

## Done
