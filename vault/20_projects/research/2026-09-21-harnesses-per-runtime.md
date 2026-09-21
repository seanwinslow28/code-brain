---
title: "Harnesses per runtime — which can carry a Productcraft seat pass (issue #300, pass 2)"
date: 2026-09-21
project: productcraft
status: draft
ticket: https://github.com/seanwinslow28/code-brain/issues/300
tags: [research, productcraft, runtime-registry, harnesses, trace-kit]
cost: $0 web reads + two read-only `codex exec` probes on the ChatGPT subscription (~18K tokens each)
models: "research and synthesis: Fable 5.1 · probe runtime: gpt-5.5 via Codex CLI 0.146.0"
---

# Harnesses per runtime — findings brief

**Question (pass 2 of #300):** which harnesses can carry a seat pass end to end — read a lane manifest and the private corpus on disk, fill a markdown template, write a ledger entry file, and report tokens plus wall-clock in a form the trace kit can meter — and what wiring does each need to become a row in the runtime registry (#286)?

**What a row must satisfy** ([record-template.md](../../../productcraft/trace/record-template.md), [trace/README.md](../../../productcraft/trace/README.md) rung-0 line 7): a verbatim `launch` form; `wall_clock_s` from instants the coordinator writes; a `meter` that is either the split `input` + `output` pair or a single `total`, never an estimate; a `meter_source` value from the checker's vocabulary (today: `Agent-tool usage | codex footer | UNMEASURED`); a `raw_log` the record indexes; and enough in that log to recover `## Corpus read` from the seat's actual file reads. **Every new harness therefore adds one `meter_source` vocabulary entry to `check.py`** — that is a fixed wiring cost shared by every row below.

Everything here is tier B unless marked. Codex 0.146.0 and Claude Code 2.1.274 are on this machine and were exercised; Gemini CLI is installed at 0.1.9, far behind its docs; Pi, Hermes, OpenCode and Aider are not installed.

## Findings summary

1. **Four harnesses carry a pass with config or a thin wrapper: Codex CLI, Claude Code (`claude -p`), Pi, and Hermes.** All four read any path the user can, write files, and report a split token pair in machine-readable form.
2. **Codex is the only credible universal harness, with two caveats.** `[model_providers.<id>]` pins any OpenAI-compatible endpoint, but `wire_api = "responses"` is now *the only supported value*. OpenRouter exposes a stateless Responses endpoint, so the config is expressible; whether the request shapes agree is **not established by primary sources** and is #287's first experiment. Ollama is documented by both OpenAI and Ollama, with a 64K-context floor.
3. **The best-shaped meter is Hermes's `--usage-file**` (split pair, cache, reasoning, cost, an `auxiliary` block, written even on failure). The richest transcript-plus-meter is Codex `--json`. `claude -p --output-format json` gives a split pair plus `total_cost_usd` and `duration_ms`, more than the Agent tool's usage field the records use today.
4. **Gemini CLI carries a pass on Google models only**; its JSON `stats` reports per-model `tokens {input, prompt, candidates, total, cached, thoughts, tool}` (source-confirmed).
5. **OpenCode's headless default auto-rejects every permission that would ask**, and `external_directory` defaults to ask. **Aider is the wrong shape**: no read tool, so the coordinator pre-lists corpus files and `## Corpus read` changes meaning.
6. **Two local facts change the Codex row today**: the `~/.codex/config.toml` default `gpt-6-astra` is rejected by the installed 0.146.0 (`-m gpt-5.5` worked), and the machine's plugin load trips Codex's 2% skills budget — run seats under a clean `CODEX_HOME`.

## Codex CLI — verdict: **yes** (OpenAI) · **yes-with-wrapper** (OpenRouter, unverified wire) · **yes-with-wrapper** (Ollama)

**Launch.** `codex exec [OPTIONS] [PROMPT]`; prompt from stdin when omitted or `-`; `--json` prints JSONL events to stdout; `-o/--output-last-message <file>`; `--output-schema <file>`; `-C <dir>`; `--add-dir <dir>`; `--ephemeral`; `-s read-only|workspace-write|danger-full-access`; `-p <profile>` layers `$CODEX_HOME/<name>.config.toml`; `-c key=value` overrides; `--ignore-user-config` (auth still uses `CODEX_HOME`) [S1]. Default sandbox for `exec` is read-only [S3].

**Pinning.** `model`, `model_provider` (default `openai`); `[model_providers.<id>]` with `name`, `base_url`, `env_key`, `wire_api` (`responses` — "the only supported value"), `query_params`, `http_headers`, `env_http_headers`, retry/timeout keys, `requires_openai_auth`; `openai`, `ollama`, `lmstudio` are reserved ids; `oss_provider = "ollama" | "lmstudio"`; `model_context_window`; `model_reasoning_effort` [S2]. `--oss` and `--local-provider ollama|lmstudio` on the CLI; with neither configured "`codex exec` exits with an error" [S1, S4]. Ollama's own integration doc gives a profile: `model = "gpt-oss:120b"`, `[model_providers.ollama-launch] base_url = "http://localhost:11434/v1/" wire_api = "responses"`, and "a context window of at least 64k tokens" [S6]. OpenRouter's Responses endpoint is `https://openrouter.ai/api/v1/responses`, stateless, tool calling and reasoning supported, rejects `store: true` and `previous_response_id` [S7].

**Disk.** read-only: reads anywhere the user can, writes blocked; workspace-write: reads unrestricted, writes to cwd, `sandbox_workspace_write.writable_roots` and `$TMPDIR`/`/tmp` [S3]. The private corpus and ledger both sit inside the repo (gitignored, not outside cwd), so `-C <repo> -s workspace-write` covers reads and the ledger write with no extra roots.

**Meter.** `--json`: `{"type":"turn.completed","usage":{"input_tokens":17774,"cached_input_tokens":3456,"cache_write_input_tokens":0,"output_tokens":17,"reasoning_output_tokens":10}}` — observed on the probe; the struct is `Usage { input_tokens, cached_input_tokens, cache_write_input_tokens, output_tokens, reasoning_output_tokens }` in `codex-rs/exec/src/exec_events.rs` [S5, P1]. Plain mode prints the final message on stdout and a `tokens used` / `16,196` footer **on stderr**, one number [P1]. That is the `codex footer` source the records already name; `--json` is strictly better — the split pair, and the JSONL is itself the `raw_log`, with `command_execution` items carrying the `cat`/`sed` reads that recover `## Corpus read` and `file_change` items carrying the writes.

**Wiring.** OpenAI: a seat profile file. OpenRouter: one `[model_providers.openrouter]` block plus the wire experiment (API-billed). Ollama: the profile above plus a model that fits the fleet's VRAM (pass 1). All three: a clean `CODEX_HOME` and a pinned `-m` the binary accepts [P0, P1].

## Claude Code — verdict: **yes** (Claude models only)

**Launch.** `claude -p "<prompt>" --output-format json|stream-json --allowedTools "Read,Write,Edit" --permission-mode acceptEdits --add-dir <dir> --max-budget-usd <n> [--bare]`; `--bare` skips hooks, plugins, memory and CLAUDE.md and "will become the default for `-p`"; `--permission-prompts none` for unattended runs [S8]. Today's seats use the Agent tool inside a session; both are launch forms of the same runtime.

**Pinning.** `--model`; provider is Anthropic, Bedrock, Vertex/Agent Platform, Foundry, or a gateway — "Anthropic … doesn't support routing Claude Code to non-Claude models through any gateway" [S9]. Pin cloud models with `ANTHROPIC_DEFAULT_{FABLE,OPUS,SONNET,HAIKU}_MODEL` [S10].

**Disk.** Reads in the working directories are auto-approved; `--add-dir` extends; writes under `acceptEdits` or an allow rule [S8]. Corpus and ledger inside the repo: no extra wiring.

**Meter.** The `result` message carries `usage` (`input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`), `total_cost_usd` (client-side estimate), `modelUsage` per model, `duration_ms`, `duration_api_ms`, `num_turns`. `usage` excludes subagents; per-step `output_tokens` is a placeholder, read it from the result [S11]. The session `.jsonl` transcript is the raw log; `Read` tool_use blocks recover `## Corpus read`.

**Wiring.** None for the Agent-tool form; a wrapper that captures `--output-format json` for the headless form and adds a `claude -p json` meter-source value.

## Pi — verdict: **yes-with-wrapper**

**What it is.** `@earendil-works/pi-coding-agent` in the `badlogic/pi-mono` monorepo (Mario Zechner; MIT) [S12, S13].

**Launch.** `pi -p "<prompt>"` prints and exits; `--mode json` "Output all events as JSON lines"; `--no-session`, `--session <path|id>`, `--session-dir <dir>`; `--tools <list>` / `--no-tools`; `--system-prompt` / `--append-system-prompt`; `@file` inlines a file; stdin is merged into the prompt [S14].

**Pinning.** `--provider <name> --model <id>` (`provider/id[:thinking]`); built-in providers include OpenAI, Anthropic, Google, OpenRouter (`OPENROUTER_API_KEY`), DeepSeek, Groq, xAI, Bedrock; Ollama/LM Studio/vLLM via a custom provider — the docs route this through an extension calling `pi.registerProvider({ baseUrl, apiKey, api: "openai-completions", models: [{ id, contextWindow, maxTokens, cost }] })`; the README also names `~/.pi/agent/models.json` [S13, S15, S16].

**Disk.** "Pi does not include a built-in sandbox"; tools run "with the permissions of the user account that starts it"; no path restriction; containerization is opt-in [S17].

**Meter.** JSON mode `message_update` / `message_end` events carry a top-level `usage`; the session JSONL's `AssistantMessage.usage` is `{ input, output, cacheRead, cacheWrite, reasoning?, totalTokens, cost{input, output, cacheRead, cacheWrite, total} }`; sessions live at `~/.pi/agent/sessions/--<path>--/<timestamp>_<id>.jsonl` [S18, S19]. The session file doubles as raw log with `read` tool calls.

**Wiring.** Install; a wrapper that sums per-message `usage` and points `--session-dir` at `trace/logs/`; an extension file per local provider. `cost` is only as honest as the provider entry.

## Hermes — verdict: **yes-with-wrapper**

**What it is.** Nous Research's open-source agent framework (Python, MIT): CLI plus messaging gateways, a skills/memory "learning loop", seven terminal backends [S20].

**Launch.** `hermes -z "<prompt>"` is "the purest one-shot entry point: single prompt in, final response text out, nothing else on stdout or stderr"; `hermes chat --oneshot -q "<prompt>"` keeps tool output in the transcript; `--query-file -` reads stdin; `--format stream-json` emits JSONL (implies quiet, requires `-q`); `-Q`; exit code reports the turn's outcome [S21].

**Pinning.** `--provider openrouter --model openai/gpt-5.5`, or `HERMES_INFERENCE_MODEL`; `config.yaml` `model: {default, provider, base_url, context_length}`; providers `openrouter`, `openai-api`, `anthropic`, `gemini`, `custom` with `base_url` (Ollama `http://localhost:11434/v1`, LM Studio, vLLM, llama.cpp), named endpoints under `providers:` selected as `custom:<name>`; **minimum context 64,000 tokens** [S22].

**Disk.** `terminal.backend: local` — "The agent has the same filesystem access as your user account"; CLI cwd is the launch dir; Docker backend for isolation [S23].

**Meter.** `--usage-file <path>` with `-z` or `--oneshot` writes `estimated_cost_usd`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `reasoning_tokens`, `total_tokens`, `api_calls`, `model`, `provider`, `session_id`, completion flags and `turn_exit_reason`; main-loop only at top level, side calls under `auxiliary`, grand total under `total_including_auxiliary`; "written even when the run fails" [S21]. Sessions in SQLite `~/.hermes/state.db` with "token counters" [S24].

**Wiring.** Install; config; **disable the memory toolset for seat passes** (`agent.disabled_toolsets: [memory]`) because cross-session memory breaks the fresh-context rule every audit runs under [S23]; capture `--format stream-json` as the raw log (the `-z` path hides tool activity). The meter shape is the best of the set and drops straight into the record.

## Gemini CLI — verdict: **yes-with-wrapper** (Google models only)

**Launch.** `gemini -p "<prompt>"` ("Forces non-interactive mode"; non-TTY also triggers it); `--output-format text|json|stream-json`; `-m <model>`; `--approval-mode default|auto_edit|yolo|plan`; `--include-directories`; `-s/--sandbox` [S25, S26].

**Pinning.** `model.name` / `GEMINI_MODEL`; auth by `GEMINI_API_KEY`, Google OAuth, or Vertex; `GOOGLE_GEMINI_BASE_URL` overrides the base URL but no non-Google provider is documented — **not found in primary sources** for OpenRouter or Ollama [S27].

**Disk.** File tools "operate within a `rootDirectory` (the current working directory or workspace root) for security"; `--include-directories` adds to the workspace [S28, S25]. Sandbox is off unless enabled by flag, `GEMINI_SANDBOX`, or `tools.sandbox`; the macOS `permissive-open` profile "confines writes to the project directory while allowing broad file reads" [S29].

**Meter.** JSON output is `{ response, stats, error? }`; `stats` is `SessionMetrics`: `models[<model>].api {totalRequests, totalErrors, totalLatencyMs}` and `.tokens {input, prompt, candidates, total, cached, thoughts, tool}`, plus `tools` counters — built from `uiTelemetryService.getMetrics()` in `nonInteractiveCli.ts` [S26, S30, S31]. Telemetry to a local file (`telemetry.target: local`, `outfile`) emits `gemini_cli.token.usage` and `gemini_cli.api_response` with `input_token_count`, `output_token_count`, `cached_content_token_count`, `thoughts_token_count`, `tool_token_count`, `duration_ms` [S32].

**Wiring.** Upgrade (0.1.9 installed has none of the above flags [P0]); config; a wrapper lifting `stats.models.*.tokens` and summing `prompt` + `candidates` per model. Raw log: `stream-json` capture.

## OpenCode — verdict: **yes-with-wrapper**

**Launch.** `opencode run [message..] --format json --model provider/model --agent <a> --dir <d> [--auto]` [S33]. In source, a `permission.asked` event is replied `"once"` under `--auto`, otherwise logged "auto-rejecting" and replied `"reject"` [S34].

**Pinning.** `model: "provider/model"`; OpenRouter built in (`openrouter/<model>`); Ollama or any OpenAI-compatible endpoint via `provider.<id> = { npm: "@ai-sdk/openai-compatible", options: { baseURL: "http://localhost:11434/v1" }, models: {...} }` [S35, S36].

**Disk.** Permissions `read`, `edit`, `bash`, `external_directory`, … with `allow|ask|deny`; most default `allow`, `external_directory` and `doom_loop` default `ask`, `.env` reads denied [S37]. Inside the repo this is workable with explicit `allow` rules.

**Meter.** `--format json` streams raw events including `step_finish` [S34]; the token/cost field names were **not confirmed in primary sources this pass**.

**Wiring.** Install; permission rules; a wrapper once the `step_finish` schema is read from source.

## Aider — verdict: **yes-with-wrapper, weak fit**

`aider --message "<prompt>" --yes-always --file <artifact> --read <corpus…> --model <m> --llm-history-file <log>` runs one instruction and exits; models pin as `openrouter/…`, `ollama_chat/…`, or `--openai-api-base` [S38, S39, S40]. It prints `Tokens: N sent, … M received.` and `Cost: $a message, $b session.` after each response, a scrapeable split pair [S41]. But Aider has no read tool: the coordinator pre-selects corpus files and `## Corpus read` stops being the seat's choice. Off the registry unless an edit-only pass kind is defined.

## Registry-row table

| Harness | Launch form | Model + provider pinning | Reads private disk? | Writes files? | Meter source | Wiring cost |
|---|---|---|---|---|---|---|
| Codex CLI (OpenAI) | `codex exec --json -C <repo> -s workspace-write -m <model> [-p <profile>] -` | `model`, `model_reasoning_effort`; ChatGPT/OpenAI auth | yes (read-only and workspace-write read anywhere) | yes (cwd + `writable_roots`) | `turn.completed.usage` split pair (JSONL); `tokens used` footer on stderr as fallback | config; clean `CODEX_HOME`; pin a model 0.146.0 accepts |
| Codex CLI (OpenRouter) | same, `-p openrouter` | `[model_providers.openrouter] base_url env_key wire_api="responses"` | yes | yes | same | config + wire-compatibility experiment |
| Codex CLI (Ollama) | same, `--oss --local-provider ollama -m <model>` or `-p ollama-launch` | `oss_provider`, `[model_providers.ollama-launch] base_url` | yes | yes | same | config; ≥64K context model |
| Claude Code (Agent tool) | Agent tool, fresh context | `model:` on the agent; Claude only | yes (working dirs) | yes | `Agent-tool usage` (today's vocabulary) | none |
| Claude Code (`claude -p`) | `claude -p --output-format json --permission-mode acceptEdits [--bare]` | `--model`; Claude only | yes | yes | `result.usage` split pair + `total_cost_usd`, `duration_ms` | wrapper; vocabulary entry |
| Pi | `pi -p --mode json --session-dir trace/logs "<prompt>"` | `--provider --model`; OpenRouter built in; Ollama via `registerProvider` extension | yes (no sandbox) | yes | `message_end.usage` / session JSONL usage `{input, output, cacheRead, cacheWrite, cost}` | install + wrapper + provider extension |
| Hermes | `hermes chat --oneshot -q "<prompt>" --format stream-json --usage-file <path>` | `--provider --model`; `config.yaml model:`; OpenRouter, custom `base_url` (Ollama) | yes (`terminal.backend: local`) | yes | `--usage-file` JSON (split pair, cache, reasoning, cost, auxiliary) | install + config + disable memory toolset + wrapper |
| Gemini CLI | `gemini -p "<prompt>" --output-format json --approval-mode yolo --include-directories <dirs>` | `-m`; Google models only | yes (workspace = cwd + include dirs) | yes | `stats.models.<model>.tokens {prompt, candidates, cached, thoughts, tool, total}` | upgrade + config + wrapper |
| OpenCode | `opencode run --format json --model provider/model [--auto]` | `provider/model`; OpenRouter built in; Ollama via `@ai-sdk/openai-compatible` | yes with `allow` rules (`external_directory` asks → rejected headless) | yes | `step_finish` event (fields unconfirmed) | install + permission rules + wrapper |
| Aider | `aider --message … --yes-always --file … --read …` | `--model openrouter/… ollama_chat/…` | only files pre-listed | yes | stdout `Tokens: … Cost: …` line | wrapper; changes pass shape |

## What the sources cannot tell us

- Whether Codex's Responses-only client and OpenRouter's stateless Responses endpoint agree on request shape (Codex per-turn statefulness vs OpenRouter's rejection of `previous_response_id`). Config is expressible; behaviour is untested.
- Which models beyond `gpt-oss` Codex's tool calling works with under `--oss`; Ollama's doc names only `gpt-oss:120b`. Pass 1's fit question, not this one.
- Where Codex stores session files (the reference documents `history.persistence`, not a path), and how the plain footer's single number relates to the JSON fields — the two probes were separate sessions, so no reconciliation is possible.
- OpenCode's `step_finish` token and cost field names; Pi's `models.json` schema (docs route custom providers through an extension); whether Gemini headless runs sandboxed by default (the enable paths imply not).
- Whether Hermes's `-z` path records file reads anywhere the coordinator can recover them; the `state.db` schema.
- Anything about seat *quality* on any harness. This pass measures plumbing only.

## Decisions requested (Sean)

1. Adopt the five-column row shape above for #286, and add one `meter_source` value per harness to `check.py`'s vocabulary as rows land.
2. Run #287's first trial on Codex→OpenRouter, since it is the one row whose wiring is expressible but unverified.
3. Rule Aider out of the registry unless an edit-only pass kind is defined.

## Sources (tier-audited: A academic · B primary · C trade · D forum)

- [S1] B — `codex exec --help`, Codex CLI 0.146.0, local invocation 2026-09-21.
- [S2] B — OpenAI, Codex config reference, learn.chatgpt.com/docs/config-file/config-reference.
- [S3] B — OpenAI, Codex sandboxing, learn.chatgpt.com/docs/sandboxing; non-interactive mode, learn.chatgpt.com/docs/non-interactive-mode.
- [S4] B — OpenAI, Codex advanced configuration (OSS providers, profiles), learn.chatgpt.com/docs/config-file/config-advanced.
- [S5] B — openai/codex source, `codex-rs/exec/src/exec_events.rs` (`Usage` struct, `ThreadEvent` variants).
- [S6] B — Ollama docs, Codex CLI integration, docs.ollama.com/integrations/codex.
- [S7] B — OpenRouter docs, Responses API overview, openrouter.ai/docs/api_reference/responses/overview.
- [S8] B — Anthropic, Run Claude Code programmatically, code.claude.com/docs/en/headless; `claude --help` 2.1.274 local.
- [S9] B — Anthropic, Other LLM gateways, code.claude.com/docs/en/llm-gateway.
- [S10] B — Anthropic, Enterprise deployment overview, code.claude.com/docs/en/third-party-integrations.
- [S11] B — Anthropic, Track cost and usage (Agent SDK), code.claude.com/docs/en/agent-sdk/cost-tracking.
- [S12] B — badlogic/pi-mono README (root).
- [S13] B — badlogic/pi-mono `packages/coding-agent/README.md`.
- [S14] B — pi docs `packages/coding-agent/docs/usage.md`.
- [S15] B — pi docs `docs/providers.md`.
- [S16] B — pi docs `docs/custom-provider.md`.
- [S17] B — pi docs `docs/security.md`.
- [S18] B — pi docs `docs/json.md`.
- [S19] B — pi docs `docs/session-format.md`.
- [S20] B — NousResearch/hermes-agent README.
- [S21] B — Hermes docs, CLI commands reference, `website/docs/reference/cli-commands.md` (raw, main).
- [S22] B — Hermes docs, AI providers, hermes-agent.nousresearch.com/docs/integrations/providers.
- [S23] B — Hermes docs, configuration, `website/docs/user-guide/configuration.md` (raw, main).
- [S24] B — Hermes docs, CLI interface, hermes-agent.nousresearch.com/docs/user-guide/cli.
- [S25] B — Gemini CLI reference, geminicli.com/docs/cli/cli-reference.
- [S26] B — google-gemini/gemini-cli `docs/cli/headless.md` (raw, main).
- [S27] B — Gemini CLI configuration reference, geminicli.com/docs/reference/configuration.
- [S28] B — google-gemini/gemini-cli `docs/tools/file-system.md`.
- [S29] B — Gemini CLI sandboxing, geminicli.com/docs/cli/sandbox.
- [S30] B — google-gemini/gemini-cli source `packages/cli/src/nonInteractiveCli.ts`.
- [S31] B — google-gemini/gemini-cli source `packages/core/src/telemetry/uiTelemetry.ts` (`ModelMetrics`, `SessionMetrics`).
- [S32] B — Gemini CLI telemetry, geminicli.com/docs/cli/telemetry.
- [S33] B — OpenCode docs, CLI, opencode.ai/docs/cli.
- [S34] B — anomalyco/opencode source `packages/opencode/src/cli/cmd/run.ts` (dev branch).
- [S35] B — OpenCode docs, config, opencode.ai/docs/config.
- [S36] B — OpenCode docs, providers, opencode.ai/docs/providers.
- [S37] B — OpenCode docs, permissions, opencode.ai/docs/permissions.
- [S38] B — Aider docs, scripting, aider.chat/docs/scripting.html.
- [S39] B — Aider docs, options reference, aider.chat/docs/config/options.html.
- [S40] B — Aider docs, connecting to LLMs, aider.chat/docs/llms.html.
- [S41] B — Aider-AI/aider source `aider/coders/base_coder.py` (`tokens_report`, `cost_report`).
- [P0] B (local observation) — installed versions: codex-cli 0.146.0, Claude Code 2.1.274, gemini 0.1.9; `~/.codex/config.toml` pins `model = "gpt-6-astra"`.
- [P1] B (local observation) — two `codex exec --ephemeral -s read-only` probes, 2026-09-21: default model rejected with HTTP 400 "requires a newer version of Codex"; `-m gpt-5.5` returned the `turn.completed.usage` line quoted above and, in plain mode, `tokens used` / `16,196` on stderr.
- C (not relied on) — search-surfaced Medium, Inventive HQ, knightli.com and explainx.ai guides on Codex OSS mode; used only to locate the primary pages above.
