---
type: research-queue
description: Questions consumed by the deep-researcher agent. One unchecked item per question. Agent picks the first unchecked, runs LDR, writes a topical note + a daily-digest line, then marks done with timestamp + output link.
---

# Deep Research Queue

Drop research questions here as `- [ ] question`. The nightly `deep-researcher` agent (02:45) picks the first unchecked item, runs Local Deep Research (LDR + Qwen3-14B + SearXNG), writes the full report to `vault/20_projects/research/`, and marks the question done with a link.

> **Routing rule (v3.26.3, 2026-05-06):** This queue is for **single-shape topics only** — one target, one question, one pattern. Heavy compound topics (≥3 sub-questions, multi-target evaluations like "compare A/B/C on dimensions 1–4", due-diligence matrices) belong on **Gemini DR / DR Max** via the `gemini-deep-research` skill or `agents-sdk/scripts/gemini_dr.py --tier dr|max`, not here. Two independent reasons, both observed 2026-05-05/06:
>
> 1. **Timeout** — LDR has a 900s hard budget. Compound prompts stall around 90 % and produce no output. (Topic 1b, 2026-05-06.)
> 2. **Citation quality collapse** — even when LDR completes, Qwen3-14B can't ground citations across multiple targets and confidently writes fabricated entities, owners, and URLs. (Topic 1a, 2026-05-05 — see the `status: superseded` file in `vault/20_projects/research/`.)
>
> Both topics were re-run on Gemini DR successfully.

## Pending

- [x] Topic 1a — MCP / SDK toolkit survey: catalog mcp-cli, mcp-bridge, mcp-proxy, third-party MCP gateways (e.g., MCP-Hub patterns), and Anthropic Agent SDK features added since 0.1.63 (current pin) that bear on headless tool access. For each: license, last-commit recency, open-issue velocity, headless-friendliness. Output a comparison table ranked by headless-friendliness for personal autonomous agent fleets running on macOS launchd. — done 2026-05-05 16:02 (LDR — **superseded, do not cite**) → [[20_projects/research/2026-05-05-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m]] · re-run 2026-05-06 16:14 via Gemini DR (canonical version) → [[20_projects/research/2026-05-06-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m]]
- [x] Topic 1b — CLI-driven agentic-workflow repo audit + pinning patterns + Gemini CLI extensions: evaluate https://github.com/jackwener/OpenCLI.git and https://github.com/google-gemini/gemini-cli.git for license, maintenance signal, security-review surface (does the repo execute model-output as code?), and fit for invocation from a Python wrapper script per the gemini-image-gen skill pattern. Catalog Gemini CLI extensions from https://geminicli.com/extensions/ for research / agentic-workflow / data-tooling relevance — including any Deep Research extension. Document patterns for pinning/vendoring third-party CLI repos (git submodule pinned to commit SHA, pip install git+url@sha, vendored-copy approach used by last30days/scripts/lib/vendor/bird-search/) so a repo update doesn't break a personal workflow. — done 2026-05-06 15:58 via Gemini DR (LDR timed out at 02:45; canonical example for the routing rule above) → [[20_projects/research/2026-05-06-topic-1b-cli-driven-agentic-workflow-repo-audit-pinning-patt]]
- [x] Topic 3 — Open-source model tool-calling (Qwen3-14B, Phi-4, Gemma 4 OpenAI-format function calling; bypass-MCP vs in-process MCP vs OS-model MCP patterns). Compare what works today on Mac Mini Ollama / MBP LM Studio, what's broken, and 2025-2026 community recipes. Identify which model+pattern combo gives the best headless tool-calling reliability for a 14B-class local model. — done 2026-05-07 02:55 → [[20_projects/research/2026-05-07-topic-3-open-source-model-tool-calling-qwen3-14b-phi-4-gemma]]
- [ ] Topic 5 — Local MCP gateway patterns: a single long-running process that holds OAuth tokens once and serves multiple agents/clients via stdio MCP. Survey 2025-2026 community projects implementing this pattern (mcp-bridge, mcp-proxy, etc.), evaluate their token-refresh / multi-tenant / scope-isolation behavior, and recommend a setup recipe for a personal agent fleet (~14 agents) needing shared OAuth access to Slack, Google, GitHub.
- [ ] Topic 7 — Daily Driver cost-benefit (external lens). Across published case studies of personal autonomous-agent fleets in 2025–2026, what ROI is reported for adding read-only access to Slack/Calendar/Gmail vs. retaining manual handoff? Cite specific blog posts / Hacker News threads / GitHub READMEs documenting time-saved estimates and any common failure modes.
- [x] What are the practical differences between Ollama Modelfile SYSTEM prompts and runtime system messages for Qwen3? — done 2026-05-03 10:52 → [[20_projects/research/2026-05-03-what-are-the-practical-differences-between-ollama-modelfile]]
- [x] What are the key differences between Apple's MLX and GGUF formats for 14B LLMs in 2026? — done 2026-04-26 09:56 → [[20_projects/research/2026-04-26-what-are-the-key-differences-between-apples-mlx-and-gguf-for]]
## Done
