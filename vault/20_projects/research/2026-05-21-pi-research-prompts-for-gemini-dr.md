---
type: research-prompts
date: 2026-05-21
purpose: Paste-ready prompts for manual Gemini Deep Research runs on the Pi (pi.dev) developer platform. Saves API budget by routing through Sean's Gemini Advanced subscription web UI instead of the Interactions API. Outputs land in vault/20_projects/research/ for downstream frontmatter + indexing.
target_platform: gemini.google.com (Deep Research mode)
target_count: 7
tags: [research, prompts, gemini-dr, pi.dev, manual-run]
ai-context: "Paste-ready prompts for manual Gemini Deep Research runs on the pi.dev developer platform — routes through Sean's Gemini Advanced web subscription to save API budget after Qwen3-14B failed to ground pi.dev (post-cutoff)."
---

# Pi (pi.dev) — 7 Deep Research Prompts for Manual Gemini DR

> **Why this file exists:** The nightly LDR agent's Qwen3-14B has no training data on `pi.dev` (post-cutoff). On 2026-05-20 it returned "no information found"; on 2026-05-21 it hallucinated Raspberry Pi. The reroute to Gemini DR via the Interactions API was attempted but the API key was expired, and Sean elected to run the prompts manually through his Gemini Advanced web subscription rather than spend ~$20 on the API (May headroom is only $5.80).
>
> **How to use:**
> 1. Open https://gemini.google.com/, switch to **Deep Research** mode.
> 2. Copy one prompt block at a time (each is fenced for clean copy).
> 3. Paste, run, wait for the report to complete (5-30 min each).
> 4. Save each report's markdown export to `vault/20_projects/research/` using ANY filename — Claude will rename + frontmatter them once you're done.
> 5. Ping me with "all 7 are in the research folder" and I'll process them.

---

## Cross-cutting context (do not paste; for your reference)

Every prompt below embeds:
- **Disambiguation safeguard** — explicit "the pi.dev developer platform, NOT Raspberry Pi, NOT Pi Network crypto." This is the #1 design choice — Qwen3-14B's failure on Topic 14 was confusing pi.dev with Raspberry Pi.
- **Fail-loud clause** — "if the platform or claim cannot be verified, say so explicitly; do not substitute a different product." Prevents the Topic 13 "no information found" failure mode from happening invisibly.
- **Researcher profile** — solo dev, post-The-Block (May 2026), 14-agent personal fleet, mixed Python + TypeScript, Obsidian-vault driven, hardware = M4 Max MBP + M4 Pro Mac Mini 24GB + RTX 4090 Alienware.
- **Citation rules** — every non-trivial claim grounded with a 2025-2026 URL + access date, plus a verbatim quote.

---

## Prompt 1 of 7 — Topic 13: Pi platform overview

```text
You are a senior developer-tools analyst writing a comprehensive platform overview for a solo developer evaluating new AI coding tools in May 2026. The target reader is a Product Manager-turned-builder running a personal autonomous-agent fleet (14 SDK agents on macOS launchd plus 13 Claude Code subagents) on a Mac Mini M4 Pro 24GB + MacBook Pro M4 Max + Alienware RTX 4090.

CRITICAL DISAMBIGUATION (do not skip): The target is the AI developer/coding platform at https://pi.dev/, launched in late 2025 or early 2026. This is NOT Raspberry Pi (the single-board computer at raspberrypi.com), NOT Pi Network (the cryptocurrency at minepi.com), and NOT any other "Pi" branded product. If your first search results are about Raspberry Pi or Pi crypto, you have the wrong target — refine and try again. If after thorough search you cannot confirm that pi.dev is a real, accessible developer platform, say so explicitly with evidence ("the domain resolves but shows X", "no Hacker News thread between Dec 2025 and May 2026 mentions it", etc.) — do NOT substitute a different product to fill the page.

Deliver a single report with these sections, in this order:

1. **What it is** — One paragraph elevator pitch, sourced and quoted from the pi.dev homepage. Include the disambiguation confirmation: "Confirmed: pi.dev is X, distinct from Raspberry Pi and Pi Network."

2. **Product surface** — Table listing every product surface: CLI? IDE? web app? agent harness? cloud sandbox? mobile? VS Code extension? For each: access pattern (download / web / extension marketplace), what it does, and whether it's free or gated.

3. **Pricing tiers** — Table of plans with: tier name, monthly cost, free-tier limits (requests/day, models, context length, plugins), paid-tier ceilings, billing model (subscription vs usage vs hybrid). Include any team/enterprise tier details and trial offers.

4. **Target user** — Who pi.dev is designed for. Distinguish between solo developer / small team / enterprise. Pull from official positioning AND from launch-week reception (HN, Reddit) to surface the gap between marketing claim and community reality.

5. **Key differentiators vs. competitors** — Six-row comparison table covering Pi vs. Claude Code, Cursor, OpenAI Codex CLI, Gemini CLI, Continue.dev, Aider. Columns: model routing (single provider vs multi-provider), headless / agentic mode support, plugin ecosystem (size + maturity), vault / knowledge-base integration, pricing model, opinionated stance (what Pi does that others don't, and vice versa). One row per competitor.

6. **Launch coverage** — Annotated list of every Hacker News thread, Reddit thread, podcast, blog post, and official changelog entry between the launch date and 2026-05-21. For each: URL, date, key quote (one verbatim sentence), and whether the sentiment was positive/negative/mixed.

7. **Open questions** — 3-5 things you could not definitively answer (e.g., "internal architecture is not documented publicly", "no third-party benchmarks exist yet"). Be explicit about gaps.

8. **Sources** — Annotated URL list. Every URL must have an access date and a one-line description of what it provided. Minimum 12 sources, prioritizing primary (pi.dev itself, official docs, official changelog) over secondary (blog posts, podcasts) over tertiary (Reddit, forum posts).

Cite all non-trivial claims with [^N] footnote markers tied to the Sources section. If a claim cannot be cited, omit it rather than guess.
```

---

## Prompt 2 of 7 — Topic 14: Pi extensions / plugins catalog

```text
You are a senior developer-tools analyst building an exhaustive plugin/extension catalog for a solo developer evaluating which Pi (pi.dev) extensions to install. Target reader profile: solo developer running a personal autonomous-agent fleet (~14 SDK agents on macOS launchd plus 13 Claude Code subagents), mixed Python and TypeScript codebases, Obsidian-vault driven knowledge management, daily creative + product-management workflows.

CRITICAL DISAMBIGUATION (do not skip): "Pi" here refers exclusively to the AI developer/coding platform at https://pi.dev/, launched late 2025 / early 2026. This is NOT Raspberry Pi extensions/HATs, NOT Pi Network crypto plugins, NOT PyPI Python packages. The plugin ecosystem you should enumerate is whatever Pi (pi.dev) offers — official marketplace, community catalog, GitHub awesome-list, or other. If pi.dev has no plugin ecosystem and the closest analog is something else, say so explicitly — do NOT pad the report with Raspberry Pi HATs or VS Code extensions.

Deliver a single report with these sections, in this order:

1. **Catalog landscape** — Where do Pi (pi.dev) extensions live? Is there an official marketplace? A community catalog? An awesome-pi GitHub list? What is the submission/review process? Quote the relevant official docs.

2. **Full enumeration table** — Every extension/plugin you can find as of 2026-05-21. Columns:
   - Name
   - Purpose (one short sentence)
   - License (MIT / Apache / proprietary / unknown)
   - Install command (verbatim, copy-pasteable)
   - Last updated (YYYY-MM-DD)
   - Community signal (GitHub stars, marketplace downloads, Discord mentions, blog coverage)
   - Source URL
   Sort alphabetically by name. If there are >50, paginate by category.

3. **Top-10 ranked for Sean's stack** — Re-rank the catalog for this specific reader (solo dev, 14-agent fleet, Python+TS, Obsidian vault, daily creative+PM work). For each of the top 10: (a) what it does, (b) why it ranks here for THIS reader, (c) install steps verbatim, (d) integration notes specific to Obsidian + autonomous agents.

4. **Notable gaps** — Things this reader would need but the ecosystem does not yet offer (e.g., "no native Obsidian plugin exists; closest is X", "no autonomous-agent orchestration helper found"). Be specific so he can scope what to build himself.

5. **Risk flags** — Any extensions with red flags: unmaintained for >6 months, single-maintainer with no backup, license unclear, known security issues, telemetry/privacy concerns. Quote the evidence.

6. **Sources** — Annotated URL list with access dates. Prioritize the official catalog page, then GitHub, then community reviews.

If the entire ecosystem is smaller than expected (say, <10 extensions), report that honestly and explain why (recent launch / closed beta / unclear future / etc.) — do NOT fabricate plugins to make the table look fuller.
```

---

## Prompt 3 of 7 — Topic 15: Pi + OpenRouter integration

```text
You are a senior platform-integration engineer documenting how to configure Pi (pi.dev) to use OpenRouter (https://openrouter.ai/) as a model provider. Target reader: solo developer running a personal cost-capped agentic workflow on Mac (~$5/day budget across ~14 agents).

CRITICAL DISAMBIGUATION (do not skip): "Pi" = the AI developer/coding platform at https://pi.dev/, launched late 2025 / early 2026. NOT Raspberry Pi, NOT Pi Network crypto. If you cannot find documented OpenRouter integration for pi.dev, say so explicitly and report the closest documented alternative (e.g., generic OpenAI-compatible base_url override) — do NOT invent integration steps.

Deliver a single report with these sections, in this order:

1. **Integration mode** — Does pi.dev support OpenRouter natively (first-class provider config), via OpenAI-compatible base_url override, or via a community extension? Quote the relevant docs.

2. **Auth pattern** — How to inject the OpenRouter API key. Env var (`OPENROUTER_API_KEY`)? Config file (which path)? Per-project vs global? Secret manager integration?

3. **Per-task model routing inside Pi** — Can a single pi.dev project route different tasks (codegen, planning, summarization) to different OpenRouter models? If yes, show the config syntax verbatim. If no, document the workaround.

4. **Cost tracking + per-day caps** — Does pi.dev surface OpenRouter spend in real time? Can the user set a per-day or per-task cap inside Pi, or must that be set OpenRouter-side via the dashboard? Show both flows.

5. **Automatic fallback** — When an OpenRouter model returns 429 or 503, does pi.dev retry on a configured fallback model? Show the fallback config syntax (`allow_fallbacks`, provider ordering, etc.) for both Pi and OpenRouter.

6. **Mixed-provider projects** — Can pi.dev hold an Anthropic key, an OpenRouter key, and an OpenAI key simultaneously in one project, and route different tasks to different providers? Show the config.

7. **Working config example** — One complete, copy-paste-ready config snippet (whatever file format pi.dev uses) that: (a) sets the OpenRouter API key, (b) routes codegen to `anthropic/claude-opus-4-7` via OpenRouter, (c) routes summarization to `openai/gpt-5.4-mini` via OpenRouter, (d) sets a $5/day cap, (e) falls back to `meta/llama-4-405b-free` on rate limit.

8. **Sources** — Annotated URL list with access dates. Prioritize official Pi docs + official OpenRouter docs.

If steps 1-7 cannot be answered from documented sources (i.e., the integration is undocumented or experimental), say so explicitly with evidence.
```

---

## Prompt 4 of 7 — Topic 16: Pi + local Ollama integration

```text
You are a senior platform-integration engineer documenting how to configure Pi (pi.dev) to use a local Ollama instance as a model provider, specifically for a solo developer running Ollama on a LAN-reachable Mac Mini (M4 Pro, 24GB unified memory) and occasionally on an Alienware desktop (RTX 4090, 24GB VRAM).

CRITICAL DISAMBIGUATION (do not skip): "Pi" = the AI developer/coding platform at https://pi.dev/, launched late 2025 / early 2026. NOT Raspberry Pi running Ollama. The Ollama project at https://ollama.com/ is the local model runner (which DOES run on Raspberry Pi, irrelevant here). If pi.dev does not document Ollama integration, report the closest workable pattern (OpenAI-compatible base_url override at the Ollama endpoint) — do NOT invent integration steps.

Deliver a single report with these sections, in this order:

1. **Integration mode** — Does pi.dev support Ollama as a first-class provider (named "ollama" in config), or via OpenAI-compatible base_url pointing at `/v1/chat/completions`? Quote the docs.

2. **Config syntax** — Verbatim config snippet for pointing pi.dev at:
   - localhost Ollama (`http://localhost:11434`)
   - LAN-reachable Ollama on Mac Mini (`http://mac-mini.local:11434` or by IP)
   - Tailscale-tunneled Ollama (any documented pattern?)
   Show both cases.

3. **Endpoint shape** — Does pi.dev send OpenAI-format requests to `/v1/chat/completions`, or Ollama-native requests to `/api/chat`? If both are supported, which is recommended? Show a working request body for each.

4. **Context window** — Recommended `num_ctx` settings for code-and-agentic workloads. Should this be set in the Modelfile, per-request, or in pi.dev's config? Quote the docs.

5. **Tool-calling reliability** — Which current Ollama models (Qwen3-14B, Llama-4, Phi-5, Gemma-4, DeepSeek-coder-v3) work reliably with pi.dev's tool-calling protocol as of 2026-05? Report community-tested results with dates and URLs.

6. **Latency vs cloud** — Published or community benchmarks comparing Ollama-on-M4-Pro vs Anthropic/OpenAI for pi.dev workloads. Tokens/sec, time-to-first-token, and tool-call round-trip time.

7. **Gotchas** — Documented or community-reported issues with: streaming responses, `keep_alive` settings, model unloading mid-session, simultaneous-request limits, response truncation. Quote the threads.

8. **Working config for Sean** — One complete, copy-paste-ready config snippet that points pi.dev at the LAN Mac Mini at `mac-mini.local:11434`, uses `qwen3:14b-instruct` for codegen, falls back to cloud Anthropic on local timeout, sets a 30-second timeout, and uses 32k context.

9. **Sources** — Annotated URL list with access dates. Prioritize official Pi docs + official Ollama docs + GitHub issues + r/LocalLLaMA threads.

If pi.dev has no documented Ollama integration, say so explicitly and present the OpenAI-compat base_url override pattern as the workable alternative.
```

---

## Prompt 5 of 7 — Topic 17: Pi + Gemini CLI interoperability

```text
You are a senior agent-orchestration engineer documenting interoperability patterns between Pi (pi.dev) and the Gemini CLI (https://github.com/google-gemini/gemini-cli) as of May 2026. Target reader: solo developer who already uses Gemini CLI for deep research and wants to invoke it from inside Pi (or vice versa) without rebuilding the workflow.

CRITICAL DISAMBIGUATION (do not skip): "Pi" = the AI developer/coding platform at https://pi.dev/, launched late 2025 / early 2026. NOT Raspberry Pi. Gemini CLI = Google's official command-line interface to Gemini models, with an extensions catalog at https://geminicli.com/extensions/. If neither side documents the other, report that explicitly and present the documented workaround patterns (shell-out, MCP bridge, file-based handoff) — do NOT invent integrations.

Deliver a single report with these sections, in this order:

1. **Direction A: Pi calls Gemini CLI** — Can pi.dev shell out to `gemini` as a sub-tool? Is there a tool-call / function-call definition pattern for this? Show the registration snippet (whatever format pi.dev uses) and a working example: "from inside Pi, invoke `gemini -p '<query>'` and capture the response."

2. **Direction B: Gemini CLI calls Pi** — Does any Gemini CLI extension at https://geminicli.com/extensions/ hand work to pi.dev? Enumerate any extensions mentioning Pi, coding agents, or external CLI delegation. For each: name, purpose, install command, source URL.

3. **MCP bridge** — Does pi.dev expose an MCP server? Does Gemini CLI consume MCP servers? If both, can they share a single MCP server? Quote the docs.

4. **Shared-context patterns** — How to pass files, vault notes, or in-memory state between the two tools. Patterns to evaluate: shared scratch directory, MCP file-resource server, env-var handoff, JSON-over-stdin. Recommend one for Sean's setup.

5. **Working recipe: Gemini Deep Research from inside Pi** — Concrete copy-paste example. Goal: "while coding in Pi, invoke Gemini Deep Research on a question, capture the markdown report, and write it to a file." Show the tool registration, the invocation, and the file-handling step.

6. **Working recipe: Pi codegen from inside Gemini CLI** — Concrete copy-paste example. Goal: "while in a Gemini CLI session, hand a coding subtask to Pi and capture the diff." Show the extension or shell-out config.

7. **Gotchas** — Auth-token sharing (does each tool need its own?), rate-limit interactions, context-window mismatch (Pi 200k vs Gemini DR 2M), output-format mismatches.

8. **Sources** — Annotated URL list with access dates. Prioritize official Pi docs + Gemini CLI repo + the extensions catalog + community recipes.

If either tool does not yet support interop in any documented way, say so and recommend the lowest-friction workaround.
```

---

## Prompt 6 of 7 — Topic 18: Pi + ChatGPT Codex subscription integration

```text
You are a senior platform-integration engineer documenting how to plug an existing ChatGPT Plus / Codex subscription into Pi (pi.dev) as a model provider, instead of using a separate OpenAI API key with usage-based billing. Target reader: solo developer (post-The-Block layoff, May 2026) who already pays for ChatGPT Plus + Codex and wants to avoid double-paying via API.

CRITICAL DISAMBIGUATION (do not skip): "Pi" = the AI developer/coding platform at https://pi.dev/, launched late 2025 / early 2026. NOT Raspberry Pi. "ChatGPT Codex" here means OpenAI's coding agent product available to ChatGPT Plus/Pro/Team/Enterprise subscribers in 2026, NOT the deprecated 2021 Codex model. If pi.dev only supports OpenAI API keys (not ChatGPT subscriptions), say so explicitly and explain why — do NOT invent a subscription-auth flow.

Deliver a single report with these sections, in this order:

1. **Auth mode survey** — What auth modes does pi.dev support for OpenAI / Codex access? Options to evaluate:
   - OpenAI API key (`OPENAI_API_KEY`)
   - ChatGPT browser session cookie / OAuth (like the `codex-cli` browser-login flow)
   - OpenAI Platform service-account token
   - Codex-specific token (if separate)
   Quote the docs for each.

2. **Supported model IDs** — Which model IDs work inside pi.dev when authed via Codex? `gpt-5.5`, `o4-codex`, `gpt-5.4-mini`, `codex-mini-latest`, `gpt-5.5-thinking`? Provide the canonical model-ID list with capabilities (context window, tool calling, vision).

3. **Hybrid workflows** — Can pi.dev orchestrate so that Codex handles code generation while another provider (Anthropic, Gemini) handles planning/review in the same session? Show config syntax.

4. **Subscription limits inside Pi** — When using ChatGPT Plus auth, what rate / usage limits does pi.dev surface? Does it hit the same 50/3hr or weekly Codex caps? How does the user see remaining quota?

5. **Vs. direct OpenAI API key** — Side-by-side comparison: (a) cost (subscription vs usage), (b) rate limits, (c) features available (vision, tool calling, code execution), (d) what's missing in subscription mode that the API offers.

6. **Working config** — Copy-paste config for pi.dev that uses ChatGPT Plus / Codex auth to route codegen to `gpt-5.5-codex` and planning to `gpt-5.5-thinking`, with the Anthropic key as fallback.

7. **Sources** — Annotated URL list with access dates. Prioritize official Pi docs + official OpenAI/Codex docs + community recipes.

If ChatGPT subscription auth is NOT supported by pi.dev, say so explicitly, link the evidence, and present the API-key alternative.
```

---

## Prompt 7 of 7 — Topic 19: Optimal Ollama model for Pi-driven workflows, ranked by hardware tier

```text
You are a senior local-LLM benchmarking analyst recommending the single optimal Ollama model (with 1-2 runners-up) for use inside Pi (pi.dev) workflows on three specific hardware tiers, as of May 2026. Target reader: solo developer running pi.dev across:
- Tier A: M4 Max MacBook Pro, unified memory class typical for a high-end 2024-2025 model (assume 64GB unified memory)
- Tier B: M4 Pro Mac Mini, 24GB unified memory, always-on headless
- Tier C: NVIDIA RTX 3090/4090-class desktop GPU with 24GB VRAM (Alienware)

CRITICAL DISAMBIGUATION (do not skip): "Pi" = the AI developer/coding platform at https://pi.dev/, launched late 2025 / early 2026. NOT Raspberry Pi (and definitely not Raspberry Pi 5 running 4B-parameter models — that is irrelevant here). Ollama = https://ollama.com/. If pi.dev has documented Ollama compatibility notes, prioritize those over generic benchmark posts. If no Pi-specific guidance exists, use general Ollama benchmarks and explicitly flag that.

Deliver a single report with these sections, in this order:

1. **Workload profile** — Pi (pi.dev) tasks split across: (a) tool-calling for agentic loops, (b) code completion + inline edits, (c) multi-turn reasoning for planning, (d) summarization of long context. Each tier should be evaluated against ALL FOUR workloads, not just one.

2. **Tier A — M4 Max MacBook Pro (64GB unified memory)** — Recommend:
   - **Best overall:** model + parameter count + quantization (Q4_K_M, Q5_K_M, MLX-4bit, etc.), expected tokens/sec for codegen, expected memory footprint, workload it shines at.
   - **Runner-up #1:** as above.
   - **Runner-up #2:** as above.
   - **Lightweight session model:** smallest competent alternative for when other apps need RAM.
   Include the `ollama pull <tag>` command verbatim for each.

3. **Tier B — M4 Pro Mac Mini, 24GB unified memory (headless, always-on)** — Same format. Memory is the binding constraint here; assume 16-18GB available for the model. Prioritize: tool-calling reliability > codegen speed.

4. **Tier C — RTX 3090/4090 24GB VRAM (Alienware)** — Same format. CUDA-only models become viable here. Compare against the unified-memory Macs on tokens/sec for the same model+quant.

5. **Cross-tier comparison table** — One table showing: model name, Tier A tok/sec, Tier B tok/sec, Tier C tok/sec, best-fit workload. Lets Sean pick which tier should run which workload.

6. **Specific Pi-compatibility notes** — Any documented Pi (pi.dev) gotchas for specific Ollama models — context window mismatches, tool-call format incompatibilities, streaming bugs. Quote the GitHub issues or community threads.

7. **Sources** — Annotated URL list with access dates. Prioritize:
   - Official Ollama library at https://ollama.com/library
   - r/LocalLLaMA benchmark threads (with dates)
   - GitHub `pi.dev` issue tracker (if public) for compatibility reports
   - Apple Silicon-specific benchmark sites (MLX vs GGUF)

If any tier has no model that competently handles all four workloads at acceptable speed, say so and recommend the workload-routing pattern instead (e.g., "use cloud for planning, local for tool-calling").
```

---

## After all 7 reports land in `vault/20_projects/research/`

Ping Claude with: **"all 7 Pi reports are in the research folder"**

Claude will then:
1. Read each file, infer the topic number from content.
2. Rename to `2026-05-XX-topic-NN-pi-<slug>-gemini-dr-manual.md` matching the existing convention.
3. Apply standard `research-report` frontmatter with `source: gemini-deep-research-manual` and `tier: dr`.
4. Update the LDR queue and Gemini queue: mark Topics 13-19 as done with vault links.
5. Inject digest lines into today's daily note under `<!-- research-digest -->`.
6. Trigger the knowledge-index regen so the synthesizer picks them up tonight.

---

## Cost accounting

- API spend avoided: ~$20 (7 × $2.80 DR-tier estimate).
- May headroom preserved: $5.80 (held for emergencies / a real Gemini DR query that genuinely needs the Interactions API).
- Manual run effort: ~30-60 min total wall time for Sean (most of which is unattended polling).
