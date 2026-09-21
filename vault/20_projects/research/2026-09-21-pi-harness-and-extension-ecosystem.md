---
title: "Pi harness and extension ecosystem — what an owner can register, and what the community has built (issue #301, pass 1)"
date: 2026-09-21
project: productcraft
status: draft
ticket: https://github.com/seanwinslow28/code-brain/issues/301
tags: [research, productcraft, runtime-registry, harnesses, pi, extensions]
cost: $0
models: "research and synthesis: Fable 5.1"
---

# Pi harness and extension ecosystem — findings brief

**Question (pass 1 of #301):** how far can Pi's extension model carry an owner-customised harness — what an extension can register, how it is loaded and configured, what the built-in prompt actually says and how to replace it, how stable the interface is — and which community add-ons matter for a Productcraft seat pass or a Devcraft coding pass. Builds on the Pi section of [2026-09-21-harnesses-per-runtime.md](2026-09-21-harnesses-per-runtime.md); nothing there is repeated.

Everything is tier B unless marked. Pi is not installed on this machine; every claim below is read from the repository at HEAD (coding-agent **0.87.0, released today**) or the add-on's own repo. The repo has moved: `badlogic/pi-mono` now redirects to **`earendil-works/pi`** (108,110 stars, 13,682 forks, created 2025-08-09) and the npm scope is `@earendil-works/*` [S1].

## Findings summary

1. **The extension surface is wide.** One TypeScript factory receives `ExtensionAPI` and can register tools, slash commands, CLI flags, keyboard shortcuts, providers, renderers and Markdown transformers; subscribe to ~39 lifecycle events (four of them can block or rewrite: `tool_call`, `tool_result`, `context`, `before_agent_start`); contribute skill/prompt/theme paths; replace the footer, header and editor; and persist entries to the session file [S2, S3].
2. **Ollama needs no extension.** The prior note's open item ("Pi's `models.json` schema") is closed: `~/.pi/agent/models.json` declares `{ providers: { ollama: { baseUrl, api: "openai-completions", apiKey: "ollama", compat: { supportsDeveloperRole: false, supportsReasoningEffort: false }, models: [{ id }] } } }` and the file reloads without restart [S4]. Extensions are for auth flows, dynamic discovery or non-OpenAI wire shapes.
3. **The default system prompt is small and mostly tool instruction.** Assembled from source it is roughly **2,450 characters / 356 words (~600 tokens)** before context files and skills: a 27-word preamble, a four-line `<tools>` list, ten `<rules>` bullets, and a 124-word `<docs>` section that points at Pi's own documentation [S5, D1]. An owner replaces the whole prefix with `.pi/SYSTEM.md`, `~/.pi/agent/SYSTEM.md` or `--system-prompt`, appends with `APPEND_SYSTEM.md` / `--append-system-prompt`, or patches individual sections from an extension.
4. **The interface is pre-1.0 and says nothing about stability.** No stability, semver or deprecation policy appears in `extensions.md`, `sdk.md`, `development.md` or either README. The changelog is the only evidence: **39 releases since 2026-05-29, seven with a "Breaking Changes" section**, including today's 0.87.0 and 0.86.0 two days ago [S6].
5. **The ecosystem is large and young.** pi.dev lists **5,462 packages** tagged `pi-package`; the auto-curated awesome list indexes **9,665 extensions** [S7, S8]. The centre of gravity is one author (nicobailon: `pi-mcp-adapter` 972K npm downloads/month, `pi-subagents`, `pi-web-access`) plus sandboxes, memory layers, provider shims and observability plugins. Most repos are under a year old; three of the canonical ones are already archived or four months stale.
6. **For a seat pass, Pi needs almost nothing from the ecosystem**: one owner-written extension (usage summary, optional terminating ledger tool), `models.json` for Ollama, an isolated `PI_CODING_AGENT_DIR`, and `--offline`. For a Devcraft pass the ecosystem matters: `carderne/pi-sandbox` or a container, `cc-safety-net`, and `pi-subagents`.

## 1. The extension model

### What an extension can register

| Registration | API | Notes |
|---|---|---|
| LLM-callable tool | `pi.registerTool({ name, label, description, parameters (TypeBox), execute, promptSnippet?, promptGuidelines?, renderCall?, renderResult? })` | Works at load or later; `promptSnippet` adds a line to `<tools>`, `promptGuidelines` bullets to `<rules>`; a tool result can carry `terminate: true` to end the turn without a follow-up LLM call (`structured-output.ts`) [S2, S9] |
| Provider | `pi.registerProvider(name, { baseUrl, apiKey, api, models, headers, compat })` or a full pi-ai `Provider`; `unregisterProvider` | Nine `api` wire types (`openai-completions`, `openai-responses`, `anthropic-messages`, `google-generative-ai`, `bedrock-converse-stream`, …); OAuth login hooks; `models.json` overrides compose on top [S10] |
| Slash command | `pi.registerCommand(name, { description, handler, getArgumentCompletions? })` | Duplicates get `:1`, `:2` suffixes |
| CLI flag / shortcut | `pi.registerFlag`, `pi.registerShortcut` | Flag readable via `pi.getFlag` |
| Events | `pi.on(event, handler)` | ~39 events; see below |
| Resources | `resources_discover` handler returns `skillPaths`, `promptPaths`, `themePaths` | How an extension ships skills/prompt templates/themes it did not put in the conventional dirs |
| TUI | `ctx.ui.setFooter/setHeader/setWidget/setStatus/setEditorComponent/setTheme/custom()`; `registerMessageRenderer`, `registerEntryRenderer`, `registerMarkdownTransformer` | All no-ops in `-p` and `--mode json` |
| Session state | `pi.appendEntry(customType, data)` (not sent to LLM), `pi.sendMessage` (sent), `pi.sendUserMessage`, `setSessionName`, `setLabel` | Entries land in the session JSONL |
| Runtime control | `setActiveTools`, `setModel`, `setThinkingLevel`, `exec`, `events` bus, `ctx.compact()`, `ctx.newSession/fork/switchSession/reload` | Session-control methods only from command handlers |

**Events that can change the run** (the rest are notifications): `input` (transform or handle the prompt), `before_agent_start` (inject a message; rewrite or patch the system prompt), `context` / `context_with_system` (edit the messages sent per request), `before_provider_headers` / `before_provider_request` (mutate headers or the payload), `tool_call` (mutate args, `{ block, reason, terminate }`), `tool_result` (patch content/usage), `message_end` (replace the finalised message, including its `usage`), `turn_end` / `agent_before_settle` (append entries, force one more request), `session_before_compact` (supply the summary), `user_bash` (swap the shell backend), `project_trust`, `cache_warming_decision` [S2, S3]. Errors in an extension are logged and the agent continues, except `tool_call` errors, which block the tool [S2].

### How an extension is written, loaded and configured

- **Shape.** A `.ts` (or `.js`) module with `export default function (pi: ExtensionAPI) {}`; the factory may be `async` and Pi awaits it before `session_start`. Loaded through jiti, so no compile step. Imports available: `@earendil-works/pi-coding-agent`, `typebox`, `@earendil-works/pi-ai`, `@earendil-works/pi-tui`, Node built-ins, and anything in a sibling `node_modules/` [S2].
- **Locations.** `~/.pi/agent/extensions/*.ts` or `*/index.ts` (global); `.pi/extensions/…` (project, only after the project is trusted); `settings.json` arrays `extensions` (paths) and `packages` (`npm:@scope/pkg@1.2.3`, `git:github.com/user/repo@v1`, local path); `-e/--extension <source>` for one run; `--no-extensions` disables discovery but `-e` still loads [S2, S11, S12].
- **Packages.** `pi install npm:…|git:…|./path` writes to `~/.pi/agent/settings.json` (or `.pi/settings.json` with `-l`) and runs `npm install --omit=dev`; git refs are pinned; a `pi` key in `package.json` (or conventional `extensions/ skills/ prompts/ themes/` dirs) declares resources; the `pi-package` npm keyword puts it in the gallery. Pi packages must list the four `@earendil-works/*` packages as `peerDependencies: "*"` [S11].
- **Config dir and trust.** `PI_CODING_AGENT_DIR` overrides `~/.pi/agent`; `PI_CODING_AGENT_SESSION_DIR` / `--session-dir` override session storage. Non-interactive modes never prompt for trust: with `defaultProjectTrust: "ask"` (the default) they *ignore* project-local `.pi/` resources; `-a/--approve` trusts them for one run, `-na/--no-approve` ignores them [S12, S13].
- **Modes.** `ctx.mode` is `"tui" | "rpc" | "json" | "print"`; `ctx.hasUI` is `false` in `-p` and `--mode json`, where "extensions run but can't prompt" [S2].
- **Shell environment.** The `bash` tool receives `PI_SESSION_ID`, `PI_SESSION_FILE`, `PI_PROVIDER`, `PI_MODEL`, `PI_REASONING_LEVEL` [S13].

### What the built-in system prompt contains

`buildSystemPromptSections()` in `src/core/system-prompt.ts` emits ordered, XML-tagged sections that are diffed and patched mid-conversation rather than resent [S5]:

- `preamble` (untagged): one sentence — *"You are an expert coding assistant operating inside pi, a coding agent harness. You help users by reading files, executing commands, editing code, and writing new files."*
- `<tools>`: one line per active tool from each tool's `promptSnippet` (`read: Read file contents`, `bash: Execute bash commands (ls, grep, find, etc.)`, `edit: …`, `write: Create or overwrite files`) plus a sentence that other custom tools may exist.
- `<rules>`: a bash-for-file-ops rule (only when `bash` is on and `ls`/`grep`/`find` tools are off), each active tool's `promptGuidelines` (read: 1, write: 1, edit: 4, bash: 1), any `promptGuidelines` from extensions, and two fixed bullets ("Be concise in your responses", "Show file paths clearly when working with files").
- `<docs>`: paths to Pi's README, docs and examples and instructions to read them when asked about Pi itself.
- Then, when present: `<addendum>` (from `--append-system-prompt` / `APPEND_SYSTEM.md`), `<project_context>` (each `AGENTS.md`/`CLAUDE.md` wrapped in `<project_instructions path=…>`), `<skills>` (Agent Skills XML, name + description only), `<cwd>`, and any custom sections an extension adds.

Assembled from those strings with placeholder paths, the tool-only prompt is **2,447 characters, 356 words, ~600 tokens** (preamble 27 words, tools 55, rules 141, docs 124) [D1]. Every `AGENTS.md`/`CLAUDE.md` in cwd and its ancestors is concatenated on top, so the prompt an interactive user sees is usually dominated by their own context files, not Pi's [S12].

**Replacing or appending.** `.pi/SYSTEM.md` (project), `~/.pi/agent/SYSTEM.md` (global) or `--system-prompt <text>` replaces the *prefix* (preamble + tools + rules + docs) — "context files and skills are still appended", and so is `<cwd>` [S12, S5]. `APPEND_SYSTEM.md` / `--append-system-prompt` fill `<addendum>`. `--no-context-files` and `--no-skills` remove the other two sections. From an extension, `before_agent_start` can return `systemPrompt` (whole replacement for the run, "a cache miss when it changes") or mutate `event.systemPromptOptions` — `sections`, `selectedTools`, `promptGuidelines` — which Pi diffs and patches; `forceSystemPrompt` is an opaque exact replacement [S2]. `--tools <list>` changes which snippets and guidelines appear at all [S12].

### API stability and versioning

**Not stated in primary sources.** Neither `extensions.md` nor `sdk.md`, `development.md` or the READMEs contain a stability, semver or deprecation statement; the version is 0.87.0 and internal packages are "version-ranged" while externals are pinned [S1, S2]. What the changelog shows: releases go back to 0.10.0 (2025-11-25); since 2026-05-29 there have been 39 releases, and **0.80.7, 0.80.8, 0.83.0, 0.84.0, 0.84.3, 0.86.0 and 0.87.0 each carry a "Breaking Changes" section**. Recent examples touch extension code directly: 0.87.0 removed `shouldStopAfterTurn` and expanded `TurnEndEvent` with required fields; 0.83.0 upgraded bundled TypeBox and removed APIs, "Extensions using removed APIs must migrate" [S6]. Add-on authors treat it the same way — the Langfuse plugin README warns "future versions can bring breaking changes", and `pi-provider-litellm` pins "Pi 0.83.0+ is required" [S20, S17]. Expect roughly one breaking release a month.

## 2. Community add-ons

Stars and last-push dates are from the GitHub API on 2026-09-21; npm downloads from the pi.dev gallery [S7]. Fit column: **seat** = matters for a Productcraft seat pass; **dev** = matters for a Devcraft-style delegated coding pass; **–** = neither. Every row is tier B (the add-on's own repo).

| Repo | Author | Lic. | ★ | Last push | Adds | Status | Fit |
|---|---|---|---|---|---|---|---|
| [nicobailon/pi-mcp-adapter](https://github.com/nicobailon/pi-mcp-adapter) | nicobailon | MIT | 1,517 | 09-21 | Any MCP server behind one ~200-token proxy tool; reads `.mcp.json`; 972K dl/mo | maintained | dev |
| [nicobailon/pi-subagents](https://github.com/nicobailon/pi-subagents) | nicobailon | MIT | 3,722 | 09-21 | Named child Pi sessions, foreground/background, saved workflows; 443K dl/mo | maintained | dev (and a coordinator alternative) |
| [nicobailon/pi-web-access](https://github.com/nicobailon/pi-web-access) | nicobailon | MIT | 1,502 | 09-21 | Web search/fetch/PDF/YouTube across ~25 backends; **zero-config default is Exa's hosted MCP** | maintained | dev (optional) |
| [nicobailon/pi-prompt-template-model](https://github.com/nicobailon/pi-prompt-template-model) | nicobailon | MIT | 317 | 09-21 | `model:` frontmatter in a prompt template switches model when invoked | maintained | **seat** (one template per seat pins its model) |
| [tintinweb/pi-subagents](https://github.com/tintinweb/pi-subagents) | tintinweb | MIT | 1,202 | 09-03 | Claude-Code-style parallel subagents, fleet view, steering | maintained | dev |
| [QuintinShaw/pi-dynamic-workflows](https://github.com/QuintinShaw/pi-dynamic-workflows) | QuintinShaw | MIT | 533 | 09-20 | Code-mode subagents, git-worktree isolation, cost accounting | maintained | dev |
| [narumiruna/pi-extensions](https://github.com/narumiruna/pi-extensions) | narumiruna | MIT | 593 | 09-21 | Monorepo: `pi-plan-mode` (read-only plan mode), `pi-usage`, `pi-goal`, `pi-btw` | maintained | dev |
| [carderne/pi-sandbox](https://github.com/carderne/pi-sandbox) | carderne | MIT | 247 | 09-17 | OS-level sandbox: allow/deny lists for read/write/edit, bash via a fork of Anthropic's `sandbox-runtime`; prompts on block; needs `rg` | maintained | **dev**, seat (read allow-list) |
| [cjermain/pi-less-yolo](https://github.com/cjermain/pi-less-yolo) | cjermain | Apache-2.0 | 162 | 09-21 | Pi in a Docker container sandbox | maintained | dev |
| [pasky/pi-gondolin](https://github.com/pasky/pi-gondolin) | pasky | none | 18 | 02-19 | Tools inside a Gondolin micro-VM (an equivalent now ships in Pi's own examples) | stale | – |
| [kenryu42/cc-safety-net](https://github.com/kenryu42/cc-safety-net) | kenryu42 | MIT | 1,551 | 09-21 | Pre-execution guard blocking destructive git/fs commands and secret-file reads; 13 harnesses | maintained | dev |
| [gotgenes/pi-packages](https://github.com/gotgenes/pi-packages) (`@gotgenes/pi-permission-system`) | gotgenes | MIT (npm) | 229 | 09-21 | Permission enforcement rules per tool; 40K dl/mo | maintained (v33) | dev |
| [MasuRii/pi-permission-system](https://github.com/MasuRii/pi-permission-system) | MasuRii | MIT | 166 | 07-03 | Fork of the above | stale | – |
| [DevMortimer/pi-warden](https://github.com/DevMortimer/pi-warden) | DevMortimer | MIT | 127 | 09-21 | Enforces project rules on every write, holds hard-to-undo actions, catches unverified "done" | maintained | dev |
| [jayzeng/pi-memory](https://github.com/jayzeng/pi-memory) | jayzeng | MIT | 169 | 09-21 | Markdown memory in `~/.pi/agent/memory/`, optional qmd semantic search | maintained | – (breaks fresh-context rule) |
| [chandra447/pi-hermes-memory](https://github.com/chandra447/pi-hermes-memory) | chandra447 | MIT | 451 | 09-14 | Hermes-style persistent memory and learning loop | maintained | – (same) |
| [k0valik/pi-blackhole](https://github.com/k0valik/pi-blackhole) | k0valik | MIT | 188 | 09-21 | Algorithmic compaction + observational memory | maintained | – |
| [balcsida/pi-provider-litellm](https://github.com/balcsida/pi-provider-litellm) | balcsida | MIT | 40 | 09-19 | Native provider for a LiteLLM proxy; `/login litellm`; requires Pi ≥0.83 | maintained | – (no LiteLLM in the fleet) |
| [v2nic/pi-ollama-provider](https://github.com/v2nic/pi-ollama-provider) | v2nic | none | 4 | 06-16 | Native `/api/chat` Ollama provider; author claims Ollama's OpenAI-compat streaming "silently dropped" tool calls (ollama#12557) and that it sets `num_ctx` from model data | stale (3 mo) | **seat** (Ollama rows: the claim needs checking) |
| [mitsuhiko/pi-llamacpp](https://github.com/mitsuhiko/pi-llamacpp) | mitsuhiko | MIT | 145 | 05-11 | Runs and manages Qwen under llama.cpp as a provider | stale (4 mo) | seat (local alt.) |
| [elidickinson/pi-claude-bridge](https://github.com/elidickinson/pi-claude-bridge) | elidickinson | MIT | 411 | 09-21 | Claude Code (Pro/Max subscription) as a Pi provider; 41K dl/mo | maintained | seat? — subscription terms unverified |
| [gotgenes/pi-anthropic-auth](https://github.com/gotgenes/pi-anthropic-auth) | gotgenes | MIT | 267 | 09-20 | Anthropic OAuth compatibility for Pi | maintained | same caveat |
| [xilnick/pi-fallback-provider](https://github.com/xilnick/pi-fallback-provider) | xilnick | MIT | 2 | 09-03 | Fallback chains across providers | low adoption | – |
| [iamaamir/pi-bifrost](https://github.com/iamaamir/pi-bifrost) | iamaamir | none | 52 | 09-21 | Routes each prompt to a model by complexity/price | maintained | – (seats pin models) |
| [langfuse/pi-observability-plugin](https://github.com/langfuse/pi-observability-plugin) | langfuse | MIT | 8 (56K dl/mo) | 09-17 | Traces turns, generations, token/cost splits, tool calls; **defaults to `cloud.langfuse.com`**; self-described experimental | maintained | seat (meter, only self-hosted) |
| [langchain-ai/langsmith-pi-extension](https://github.com/langchain-ai/langsmith-pi-extension) | LangChain | MIT | 3 | 09-10 | Same shape for LangSmith | maintained | – |
| [braintrustdata/braintrust-coding-agent-plugins](https://github.com/braintrustdata/braintrust-coding-agent-plugins) | Braintrust | none | 2 | 09-16 | Same shape for Braintrust | maintained | – |
| [Piebald-AI/splitrail](https://github.com/Piebald-AI/splitrail) | Piebald | MIT | 223 | 09-21 | Cross-harness token/cost monitor that reads Pi sessions | maintained | seat (meter reader; not read this pass) |
| [NikiforovAll/pi-inspect](https://github.com/NikiforovAll/pi-inspect) | NikiforovAll | none | 40 | 05-20 | Dashboard of tools, prompts, skills and the injected system prompt | stale | seat (one-off prompt audit) |
| [edgehero/pi-dispatch](https://github.com/edgehero/pi-dispatch) | edgehero | MIT | 177 | 09-21 | Pi as a service: cron / on-demand / issue-triggered runs in a container, durable queue, spend cap | maintained | seat + dev (scheduled headless passes) |
| [shaftoe/pi-coding-agent-action](https://github.com/shaftoe/pi-coding-agent-action) | shaftoe | MIT | 69 | 09-21 | GitHub Action wrapper | maintained | dev (CI) |
| [arpagon/pi-rewind](https://github.com/arpagon/pi-rewind) | arpagon | MIT | 113 | 03-31 | Per-turn checkpoint, `/rewind`, redo stack | stale | dev |
| [svkozak/pi-acp](https://github.com/svkozak/pi-acp) | svkozak | MIT | 691 | 07-30 | ACP adapter for editor integration | slowing | – |
| [agegr/pi-web](https://github.com/agegr/pi-web) | agegr | MIT | 6,666 | 09-21 | Web UI over Pi | maintained | – |
| [jayminwest/overstory](https://github.com/jayminwest/overstory) | jayminwest | MIT | 1,324 | 05-28 | Multi-agent orchestration with a Pi adapter | **archived** | – |
| [tmustier/pi-agent-teams](https://github.com/tmustier/pi-agent-teams) | tmustier | MIT | 103 | 06-20 | Experimental agent swarm | stale | – |
| [badlogic/pi-skills](https://github.com/badlogic/pi-skills) | Zechner | MIT | 2,549 | 06-06 | Skills usable from Pi, Claude Code, Codex | 3.5 mo quiet | – |
| [Dwsy/pi-extensions-skill](https://github.com/Dwsy/pi-extensions-skill) | Dwsy | MIT | 20 | 06-27 | A skill that teaches an agent to write Pi extensions | stale | seat (authoring aid) |
| [TGYD-helige/pi](https://github.com/TGYD-helige/pi) | TGYD | Apache-2.0 | 67 | 09-21 | MCP-based tool packages: IM, browser, memory, telemetry (`@amaster.ai/pi-memory-mem0`) | maintained | – |
| [irahardianto/pi-mcp-extension](https://github.com/irahardianto/pi-mcp-extension) | irahardianto | MIT | 7 | 05-03 | Earlier MCP client | superseded | – |

TUI-only work (`nicobailon/pi-powerline-footer` 437★, `MasuRii/pi-tool-display` 291★, `lmilojevicc/pi-zentui` 91★) and personal collections (`ogulcancelik/pi-extensions` 544★, `tmustier/pi-extensions` 483★, `HazAT/pi-config` 451★, `ben-vargas/pi-packages` 118★) are real but neither-fit. Two forks are worth knowing as *alternative harnesses*, not add-ons: `can1357/oh-my-pi` (32,310★, "IDE wired in") and `huggingface/tau` (2,827★, a Python port). `mksglu/context-mode` (23,882★) and `wshobson/agents` (39,855★) are multi-harness projects that merely list Pi. Directories: the pi.dev gallery (5,462 packages, gallery membership is the `pi-package` keyword, sorted by npm downloads) [S7]; `shaftoe/awesome-pi-coding-agent` (128★, rebuilt daily by an LLM pipeline, 12,445 resources) [S8]; `qualisero/awesome-pi-agent` (1,098★) is **archived** since June [S8].

## 3. Fit for Sean

### A seat pass on Pi

**Isolate the harness.** Point `PI_CODING_AGENT_DIR` at a seat-only home (e.g. `productcraft/trace/pi-home/`) so Sean's personal `~/.pi/agent` extensions, skills and memory add-ons never load, and run with `-na --no-context-files --no-skills --no-extensions -e <seat extension>` so no `.pi/`, `AGENTS.md` or `CLAUDE.md` from the code-brain tree reaches the prompt [S12, S13]. Add `--offline` (or `enableInstallTelemetry: false` + `PI_SKIP_VERSION_CHECK=1`): by default Pi pings `pi.dev/api/report-install`, checks `pi.dev/api/latest-version`, and adds attribution headers to OpenRouter requests [S14].

**Owner prompt.** Put the seat brief in that home's `SYSTEM.md`. That drops Pi's `<tools>`, `<rules>` and `<docs>` sections, so the brief must itself name `read`/`write`/`edit` and the one rule that matters ("use `read`, not `cat`"); the `<cwd>` section is always appended. If keeping Pi's ~200 words of tool coaching is acceptable, use `APPEND_SYSTEM.md` instead and drop only `<docs>` by naming a `docs` section override from the extension (`systemPromptOptions.sections`). Restrict tools with `--tools read,write,edit,ls` — with `bash` off, every corpus read is a `read` tool call in the session JSONL, which is exactly what `## Corpus read` recovery needs [S5, S12].

**Registrations actually needed** (one file):

1. *Usage summary.* `pi.on("message_end")` summing `usage` for `role === "assistant"`, or `pi.on("agent_end")` iterating `event.messages`; write `{ input, output, cacheRead, cacheWrite, cost }` to `trace/logs/<id>.usage.json` in `session_shutdown`. Both events fire in `-p`; the same numbers are in the session file, so the extension is a convenience, not a requirement [S2, S15].
2. *Optional terminating ledger tool.* A `registerTool` with `terminate: true` whose TypeBox `parameters` are the ledger-entry fields; it validates and writes the file itself and ends the turn without a follow-up LLM call (`structured-output.ts`) [S9]. This turns "fill the template and write the ledger" into a typed contract rather than a hope.
3. *No provider extension for the two fleet routes.* OpenRouter is built in (`OPENROUTER_API_KEY`); Ollama is `models.json` with the compat flags above. Register a provider only if the `v2nic` claim about tool-call loss over Ollama's OpenAI-compat streaming turns out true for the seat models [S4, S16].
4. *Session dir* is a flag, not a registration: `--session-dir trace/logs` [S12].

Launch form for the registry row: `PI_CODING_AGENT_DIR=<home> pi -p --mode json --offline -na --no-context-files --no-skills --no-extensions -e <home>/seat.ts --tools read,write,edit,ls --session-dir trace/logs --model openrouter/<id> "<prompt>"`. `meter_source` value: `pi message_end usage` (or `pi session jsonl usage` if the wrapper reads the file instead).

### A Devcraft coding pass on Pi

Keep `bash`. Then: (a) isolation — `security.md` is explicit that unattended automation belongs in "a container, VM, micro-VM, remote sandbox, or policy-controlled sandbox" [S18]; `carderne/pi-sandbox` is the in-process option (allow/deny lists + Anthropic's sandbox-runtime for bash), `pi-less-yolo` the Docker one; (b) a `tool_call` gate — `cc-safety-net` or Pi's own `protected-paths.ts` / `permission-gate.ts` examples; (c) `git-checkpoint.ts` from the examples for per-turn stash; (d) `pi-subagents` when a pass needs a reviewer or scout; (e) `pi-plan-mode` from `narumiruna/pi-extensions` for read-only planning turns.

### Risks

- **No sandbox is the design, not an omission.** Tools and extensions "run with the permissions of the pi process"; project trust "is not a sandbox" [S18]. A seat pass reading a private corpus is fine on the host; a Devcraft pass with `bash` is not.
- **Extension API churn.** Seven breaking releases in sixteen weeks; an owner extension of thirty lines is cheap to fix, but every third-party package pinned by `pi install` may lag — note `pi-provider-litellm`'s "Pi 0.83.0+" floor and `pi-gondolin` already obsoleted by an upstream example. Pin `pi` itself and run `pi update` on purpose.
- **Phone-home defaults.** Pi: install ping, version check, OpenRouter/NIM/Cloudflare attribution headers (off with `--offline`). `pi-web-access`: Exa's hosted MCP with no key. Langfuse/LangSmith/Braintrust plugins: vendor clouds unless `baseUrl` is set. `pi install` runs `npm install` on the package, so its dependency tree runs on the host [S11, S14, S19, S20].
- **Subscription bridges.** `pi-claude-bridge` and `pi-anthropic-auth` reuse Claude Pro/Max auth from a non-Anthropic client; whether that is within the subscription terms is **not found in primary sources** here and should be checked before a registry row depends on it.
- **Memory add-ons contradict the seat rule.** Every memory extension surveyed writes cross-session state under `~/.pi/agent/`; the isolated home above is what keeps them out.

## What the sources cannot tell us

- The measured size of the default prompt on a real install (the 2,447-character figure is assembled from source strings with placeholder paths, not captured from a run), and how much `<skills>` adds per skill.
- Any stability or deprecation policy for `ExtensionAPI` — silence in the docs is the finding.
- Whether Ollama's OpenAI-compatible streaming actually drops tool calls for the fleet's seat models under Pi's `openai-completions` path; the claim comes from one add-on author citing an Ollama issue, and Pi's own docs recommend the `models.json` route without caveat.
- Whether `agent_end` / `message_end` extension handlers see subagent usage, and whether `cost` on a `models.json` entry with zeros flows into the JSON `usage.cost` field as zero or undefined.
- Whether `--append-system-prompt` accepts `@file` (documented only for prompt arguments).
- The terms question for subscription-auth bridges.
- What `Piebald-AI/splitrail` reads from a Pi session and whether its numbers reconcile with `message_end.usage`.

## Decisions requested (Sean)

1. Adopt the isolated-home launch form above as the Pi registry row for #286, with `pi message_end usage` as its `meter_source` value, and treat the owner extension (usage summary + terminating ledger tool) as the only add-on a seat pass installs.
2. Decide whether the seat brief lives in `SYSTEM.md` (owner writes the tool coaching) or `APPEND_SYSTEM.md` (Pi's ~200 words of tool coaching stay). My recommendation: `SYSTEM.md`, so the prompt is fully owner-authored and the `<docs>` section never reaches a seat.
3. Add one #287 experiment: an Ollama seat pass through `models.json` with a tool call in the transcript, to settle the streaming-tool-call claim before any provider extension is written.
4. Keep `pi-claude-bridge` / `pi-anthropic-auth` off the registry until the subscription-terms question is answered.

## Sources (tier-audited: A academic · B primary · C trade · D forum)

- [S1] B — `earendil-works/pi` repository metadata via GitHub API (stars, forks, license, created, default branch); `packages/coding-agent/package.json` (version 0.87.0, exports, dependencies); root README (pinning policy).
- [S2] B — `packages/coding-agent/docs/extensions.md` (raw, main, 130 KB).
- [S3] B — `packages/coding-agent/src/core/extensions/types.ts` (`ExtensionAPI` overloads, event union).
- [S4] B — `packages/coding-agent/docs/models.md` (`models.json` minimal and compat examples).
- [S5] B — `packages/coding-agent/src/core/system-prompt.ts`; `src/core/tools/{read,write,edit,bash}.ts` (`*ToolSystemPromptContribution` snippet and guideline strings).
- [S6] B — `packages/coding-agent/CHANGELOG.md` (raw, main; release headers and "Breaking Changes" sections 0.10.0 → 0.87.0).
- [S7] B — pi.dev/packages gallery (package count, download-sorted listing, gallery rule) and `docs/packages.md` (Gallery Metadata).
- [S8] B — `shaftoe/awesome-pi-coding-agent` README (stats block, pipeline); `qualisero/awesome-pi-agent` repository metadata (archived flag).
- [S9] B — `packages/coding-agent/examples/extensions/structured-output.ts`; Examples Reference table in extensions.md.
- [S10] B — `packages/coding-agent/docs/custom-provider.md` (API types table, OAuth, `unregisterProvider`).
- [S11] B — `packages/coding-agent/docs/packages.md` (install, sources, manifest, peerDependencies, filtering).
- [S12] B — `packages/coding-agent/docs/usage.md` and `README.md` (SYSTEM.md / APPEND_SYSTEM.md, `--no-extensions -e`, `--tools`, `--session-dir`, trust flags).
- [S13] B — `packages/coding-agent/docs/environment-variables.md`; `docs/settings.md` (Project Trust, `defaultProjectTrust`).
- [S14] B — `docs/settings.md` "Telemetry and update checks" (`enableInstallTelemetry`, attribution headers, `--offline`).
- [S15] B — `packages/coding-agent/docs/json.md` (`message_update.usage`, `agent_end.messages`).
- [S16] B — `v2nic/pi-ollama-provider` README (v2 feature table; Ollama compat claims are the author's).
- [S17] B — `balcsida/pi-provider-litellm` README ("Pi 0.83.0+ is required").
- [S18] B — `packages/coding-agent/docs/security.md` ("No Built-in Sandbox", contained-environment guidance).
- [S19] B — `nicobailon/pi-web-access` README (zero-config Exa MCP, fallback chain); `nicobailon/pi-mcp-adapter` README; `nicobailon/pi-subagents` README; `jayzeng/pi-memory` README; `carderne/pi-sandbox` README.
- [S20] B — `langfuse/pi-observability-plugin` README (experimental warning, default `baseUrl`).
- [S21] B — GitHub API repository metadata for every row in the add-on table (stars, `pushed_at`, license SPDX id, archived flag), 2026-09-21; npm registry `repository.url`, `version`, `time.modified`, `license` for the npm-named packages.
- [S22] B — GitHub repository and code search (`pi-coding-agent`, `pi-mono extension`, `pi.registerTool`, `pi.registerProvider`, topics `pi-coding-agent`, `pi-extension`, `pi-package`, `pi-agent`), 2026-09-21; used to build the candidate list, then each candidate was read from its own repo.
- [D1] B (derived) — default-prompt size computed by assembling the [S5] strings with placeholder paths; not a captured run.
- C (not relied on) — search-surfaced HoangYell "Pi Mono Explained", Parallel "Building a Free CLI Agent with Pi, Ollama, and Gemma", and a dabit3 gist; used only to locate primary pages.
