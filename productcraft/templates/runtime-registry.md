# Runtime registry — the runtimes every -craft team may run a pass on, and how a new one earns its way in

First copy, built on the Productcraft build map's [Runtime registry and model-trial protocol](https://github.com/seanwinslow28/code-brain/issues/286) ticket (2026-09-21) from two tier-audited research briefs ([harnesses per runtime](../../vault/20_projects/research/2026-09-21-harnesses-per-runtime.md), [the Pi harness](../../vault/20_projects/research/2026-09-21-pi-harness-and-extension-ecosystem.md)) and the rulings already in force ([per-seat model delegation, #267](https://github.com/seanwinslow28/code-brain/issues/267); [evals-and-trace design, #272](https://github.com/seanwinslow28/code-brain/issues/272) decision 9). The master skill owns it; Systemcraft inherits it with the backport ticket in `vault/00_inbox/tickets.md`; `craftwork` extracts it for Devcraft and later teams.

**What this file is for.** Seat identity is already separate from runtime: rule 7 puts the seat contract, lane manifest and target in the prompt, and each seat file's `model:` line names the runtime that actually runs. Swapping a runtime is therefore a one-line seat-file edit plus a launch form the coordinator knows. This is the table of launch forms — and the standing each runtime has earned, so that an unmeasured runtime never becomes a seat baseline by drift.

**Rulings adopted here, pending Sean's ratification** (each one is a rule-8 ticket line until he rules): the row shape below; one `meter_source` value per row in the trace kit's vocabulary, held equal by a test; Aider off the registry; Jev off the registry as a seat runtime; Pi's isolated-home form with an owner-authored `SYSTEM.md`; the subscription-auth bridges off until their terms are answered. Overruling any of them is an edit to its row, not a re-litigation of #267.

## A row is a route, not a model

One row per **harness × provider route**. The model and its effort are parameters of a pass — pinned in the seat file for a baseline, in the Route entry for a deviation, in the trial record for a trial — and the record's `runtime:` string carries them. The string convention per row is in the table, so that the registry numbers group correctly across engagements: the model as it ran, prefixed by the route only when the route changes who serves the model.

## The rows

| # | Route | `runtime:` string | Launch form (verbatim; values per pass) | Sandbox and disk | Reads corpus + ledger | `meter_source` | Tier steps on the #267 ladder | Standing | Installed here (2026-09-21) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Claude Code, Agent tool | `claude-<model>` — `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5`; `claude-fable-5-1` only for the interactive coordinator's own session | `Agent tool, fresh context, model=<opus\|sonnet\|haiku>, subagent_type=general-purpose` | the session's permission mode; the subagent's tools | yes — the working directory | `Agent-tool usage` (one total) | Sonnet 5 → Opus 5 → row 3; Haiku 4.5 is the downshift floor, never a baseline; Fable only on Sean's word for a named pass | **ruled** (#267): Opus 5 baseline for four seats, Sonnet 5 for three; 26 labeled passes on pc-eng-001 | Claude Code 2.1.274 |
| 2 | Claude Code, headless | as row 1 (same models, same provider) | `claude -p --output-format json --model <model> --permission-mode acceptEdits --allowedTools "Read,Write,Edit" --add-dir <repo> --max-budget-usd <n> --bare "<prompt>"` | `acceptEdits` inside the working directories; `--bare` skips hooks, plugins, memory and CLAUDE.md | yes | `claude -p result.usage` (split pair; also `total_cost_usd`, `duration_ms`) | as row 1 | as row 1 for the model; **the form is unverified** — no pass has run on it; its first pass proves the meter line | Claude Code 2.1.274 |
| 3 | Codex CLI on OpenAI | `codex <model> <effort>` — `codex gpt-5.6-sol high` | `codex exec --json --model gpt-5.6-sol -c model_reasoning_effort="high" --sandbox workspace-write --skip-git-repo-check -C <repo> -o <eng>/trace/logs/pass-NN.last.md "$(cat <eng>/trace/logs/pass-NN.prompt.md)" < /dev/null > <eng>/trace/logs/pass-NN.jsonl 2> <eng>/trace/logs/pass-NN.err` | `workspace-write` with `-C <repo>`: reads anywhere the user can, writes inside the repo | yes — corpus and ledger sit inside the repo, gitignored | `codex turn.completed.usage` (split pair, from the JSONL); `codex footer` when the plain form is used (one total, on stderr) | high → xhigh → stop and ask Sean; `ultra` forbidden (auto-delegates, breaks one-invocation-one-seat) | **ruled** (#267): the escalation target and the default gate vendor; 3 labeled passes on pc-eng-001, 3 pass, rung-0 clean | codex-cli 0.146.0 |
| 4 | Codex CLI → OpenRouter | `codex/openrouter <model> [<effort>]` | row 3's form with `-p openrouter -m <model>` and a `$CODEX_HOME/openrouter.config.toml` holding `[model_providers.openrouter] name = "OpenRouter" base_url = "https://openrouter.ai/api/v1" env_key = "OPENROUTER_API_KEY" wire_api = "responses"` | as row 3 | yes | as row 3 | none — a trial runtime has no tier (below) | **unmeasured**; the wiring is expressible and **unverified**: Codex's Responses-only client against OpenRouter's stateless Responses endpoint is #287's first experiment | codex-cli 0.146.0; API-billed |
| 5 | Codex CLI → Ollama | `codex/ollama <model>` (host in the launch form, not the string) | row 3's form with `--oss --local-provider ollama -m <model>`, or `-p ollama-launch` over `[model_providers.ollama-launch] base_url = "http://<host>:11434/v1/" wire_api = "responses"`; the model needs a ≥64K-context tag | as row 3 | yes | as row 3 | none | **unmeasured**; which models tool-call under `--oss` beyond `gpt-oss` is not established; local fit is arithmetic until a pass runs at the quant it would ship at | codex-cli 0.146.0; Ollama 0.34.1 on MBP, Mac Mini, Alienware (day-gated) |
| 6 | Pi | `pi/<provider> <model>` — `pi/openrouter glm-5.3`, `pi/ollama qwen3.8-27b` | `PI_CODING_AGENT_DIR=productcraft/trace/pi-home pi -p --mode json --offline -na --no-context-files --no-skills --no-extensions -e productcraft/trace/pi-home/seat.ts --tools read,write,edit,ls --session-dir <eng>/trace/logs --model <provider>/<model> "<prompt>"` | no sandbox by design — the host user's permissions; tools cut to `read,write,edit,ls` so every corpus read is a `read` call in the session JSONL; an isolated home keeps personal extensions, skills and memory add-ons out | yes | `pi message_end usage` (split pair per assistant message, summed by the owner extension; the session JSONL holds the same numbers) | none | **unmeasured**; the seat brief lives in the home's `SYSTEM.md` (owner-authored, no `<docs>` section reaches a seat); OpenRouter built in; Ollama through `models.json`, no provider extension unless the tool-call-streaming claim proves true (#287 experiment) | not installed |
| 7 | Hermes | `hermes/<provider> <model>` | `hermes chat --oneshot -q "<prompt>" --format stream-json --usage-file <eng>/trace/logs/pass-NN.usage.json` with `agent.disabled_toolsets: [memory]` in its config and `terminal.backend: local` | the host user's permissions (`local` backend); the memory toolset **off** — cross-session memory breaks the fresh-context rule every audit runs under | yes | `hermes usage-file` (split pair, cache, reasoning, `auxiliary`, written even on failure; the record takes the top-level main-loop numbers) | none | **unmeasured**; the `-z` path hides tool activity, so `--oneshot` + `stream-json` is the raw log; ≥64K context | not installed |
| 8 | Gemini CLI | `gemini <model>` | `gemini -p "<prompt>" --output-format json -m <model> --approval-mode yolo --include-directories <repo>` | file tools confined to the workspace root plus included directories; sandbox off unless flagged | yes | `gemini stats.tokens` (`prompt` + `candidates` per model → input / output; `cached`, `thoughts`, `tool` beside them) | none | **unmeasured**; Google models only — no other provider is documented | gemini 0.1.9, which lacks these flags — upgrade before the first pass |

**Candidates that are not rows yet.** OpenCode (`opencode run --format json --model provider/model --auto`) carries a pass and reaches OpenRouter and Ollama, but its `step_finish` token and cost fields were not confirmed in primary sources; it becomes a row when someone reads that schema from source and names its `meter_source` value. A row without a source-confirmed meter is not a row.

**Two local facts every Codex row carries** (#300, probes of 2026-09-21). `~/.codex/config.toml` pins `model = "gpt-6-astra"`, which the installed 0.146.0 rejects with HTTP 400 — so a pass **always** passes `--model`, never inherits the default, and `gpt-6-astra` stays a dated owner-approved substitution only once a Codex upgrade accepts it. And this machine's plugin load trips Codex's 2% skills budget: the isolation recommended is a seat `CODEX_HOME` carrying the auth file and a seat config, so no personal skill or plugin reaches a seat prompt. That isolation is **unverified**; the plain form ran three passes on pc-eng-001 and remains valid. Which of `CODEX_HOME` and `--ignore-user-config` actually clears the budget is #287's first Codex check.

## Standing — how a runtime earns its way in

Every row carries one of four standings. The first is a ruling; the other three are earned on the evals ladder (#272 decision 9), in order, and a runtime never skips one.

| Standing | What it means | What it permits | How it is reached |
|---|---|---|---|
| **ruled** | Placed by a ratified ruling (#267 today): the seat baselines and the escalation target | Whatever the ruling says: a seat `model:` line, a ladder tier, a gate vendor | Sean's ratification on a map ticket; re-ruled the same way |
| **unmeasured** | Registered, with a launch form and a meter source, and no labeled pass on real work | A **trial** (a shadow pass beside a live engagement's pass, labeled blind); or a **dated, owner-approved substitution** under the availability ladder on Sean's word for a named pass, with `standing: unmeasured` in the Route entry. Never a seat baseline, never a ladder tier, never a gate vendor | Its row lands here with a source-confirmed `meter_source` |
| **substitution-eligible** | One blind-labeled, rung-0-clean trial pass on real work | The coordinator may **propose** it at Route as the substitution for an unavailable runtime — still dated, still owner-approved; a promoted trial output enters the train under rule 7 | The trial's row in the labels file carries `pass`, the checker names no finding on it, and its runtime is on the § Numbers table below. `UNMEASURED` on that pass is honest and does not block this standing; it blocks the next |
| **baseline-eligible** | Enough measured, labeled passes in a seat family that a seat file may name it | A seat's `model:` line, by a dated edit that names the numbers it rests on; a ladder position only by a new ruling | Rung 1 applied to its fails (every fail coded against [trace/taxonomy.md](../trace/taxonomy.md) or honestly uncodeable) **plus a count floor #287 sets** and records here when it does. Until #287 sets the floor, no runtime reaches this standing |

A trial runtime has **no tier**: escalation is defined on the ratified ladder only, and the baseline pass a trial shadows is what the train carries, so a failed trial is a labeled fail and nothing else — never a redraft one tier up on the trial's own row. A row records its runtime's own effort steps (Codex `high` / `xhigh`; a `:thinking` suffix on Pi; Claude's model steps) so a future ruling has a named step to point at, but naming a step is not a tier.

## The trial protocol

How a runtime moves from a row to a number, on real work only (#287's constraint: every experiment is a unit of work Sean would keep).

1. **Register** — the row above with its launch form, sandbox, provider pinning, disk reach and a source-confirmed `meter_source`; the value is added to `METER_SOURCES` in [trace/tracekit/engagement.py](../trace/tracekit/engagement.py) in the same change, or the drift test fails. Standing: unmeasured.
2. **Declare at Open** — a trial is named in the engagement's pass budget as a shadow of a specific planned pass (`shadow_of`), and does not count against the funded cap: it is beside the train, never in it. An API-billed row (4, 8 on an API key) states a per-trial cash cap in the same line; the number is #287's to propose.
3. **Fire on identical inputs** — `kind: trial`, the same input hashes as the baseline pass, the row's launch form verbatim, its artifact written under `trace/trials/`, `## Moves` included. The record's `runtime:` string follows the row's convention. A gate or audit of the trial runs on a different lineage than its author, like any pass.
4. **Label blind** — the viewer hides the runtime, launch form and log path of both passes until both rows carry a verdict (rung-0 line 9 enforces it). Sean labels both as he reads.
5. **Promote or keep** — a trial whose blind label passes while the baseline's fails is *promotable*; promoting it is a dated, owner-approved substitution under rule 7, noted on both records, with one line beginning `promoted: <date>` in the trial record's `## Notes` — the registry numbers read that line and nothing else. An unpromoted trial is still kept work: its artifact and label stay in the engagement.
6. **Count at Close** — `python3 productcraft/trace/registry.py productcraft/ledger/engagements/pc-eng-*` regenerates § Numbers; the coordinator replaces the section with the output. Counts only: the design forbids a percentage below ten passes and the generator prints none at any count. A standing changes only when the numbers say so, by an edit to the row that names them.

The same six steps govern a **launch-form** change on an existing runtime (row 2, or row 3's `--json` form over the footer): the first pass on the new form is an ordinary pass whose meter line proves the wiring, not a trial, because the runtime did not change.

## Numbers

<!-- generated by productcraft/trace/registry.py — replace the block below at every Close; never edit a number by hand -->

Engagements read: pc-eng-001. Counts, never percentages; medians over measured passes only.

| Runtime | Passes | Labeled pass | Rung-0 clean | Measured | Median tokens | Median wall-clock (s) | Trials | Promotable | Promoted |
|---|---|---|---|---|---|---|---|---|---|
| `claude-fable-5-1` | 4 | 4 of 4 | 4 of 4 | 0 of 4 | — | — | 0 | 0 | 0 |
| `claude-opus-5` | 22 | 18 of 22 | 19 of 22 | 22 of 22 | 48,265 | 683 | 0 | 0 | 0 |
| `claude-sonnet-5` | 4 | 3 of 4 | 4 of 4 | 4 of 4 | 80,831 | 537 | 0 | 0 | 0 |
| `codex gpt-5.6-sol high` | 3 | 3 of 3 | 3 of 3 | 3 of 3 | 302,184 | 766 | 0 | 0 | 0 |

| Runtime | Seat | Family | Passes | Labeled pass | Rung-0 clean | Measured | Median tokens | Median wall-clock (s) | Trials | Promoted |
|---|---|---|---|---|---|---|---|---|---|---|
| `claude-fable-5-1` | coordinator | coordination | 4 | 4 of 4 | 4 of 4 | 0 of 4 | — | — | 0 | 0 |
| `claude-opus-5` | business-economics | quantitative | 2 | 2 of 2 | 1 of 2 | 2 of 2 | 59,954 | 687 | 0 | 0 |
| `claude-opus-5` | discovery-lead | discovery synthesis | 6 | 6 of 6 | 6 of 6 | 6 of 6 | 47,769 | 780 | 0 | 0 |
| `claude-opus-5` | growth-distribution | growth | 2 | 1 of 2 | 1 of 2 | 2 of 2 | 90,120 | 847 | 0 | 0 |
| `claude-opus-5` | insights-analytics | evidence grading | 5 | 4 of 5 | 4 of 5 | 5 of 5 | 40,314 | 581 | 0 | 0 |
| `claude-opus-5` | product-leadership | framing | 2 | 1 of 2 | 2 of 2 | 2 of 2 | 63,418 | 924 | 0 | 0 |
| `claude-opus-5` | product-strategist | framing | 5 | 4 of 5 | 5 of 5 | 5 of 5 | 41,372 | 674 | 0 | 0 |
| `claude-sonnet-5` | business-economics | quantitative | 1 | 1 of 1 | 1 of 1 | 1 of 1 | 70,885 | 506 | 0 | 0 |
| `claude-sonnet-5` | delivery-execution | delivery breakdown | 2 | 1 of 2 | 2 of 2 | 2 of 2 | 70,753 | 580 | 0 | 0 |
| `claude-sonnet-5` | growth-distribution | growth | 1 | 1 of 1 | 1 of 1 | 1 of 1 | 90,777 | 568 | 0 | 0 |
| `codex gpt-5.6-sol high` | product-strategist | framing | 1 | 1 of 1 | 1 of 1 | 1 of 1 | 176,279 | 550 | 0 | 0 |
| `codex gpt-5.6-sol high` | red-team-gate | gate | 2 | 2 of 2 | 2 of 2 | 2 of 2 | 342,089 | 869 | 0 | 0 |

Reading the first table honestly: the three Opus passes rung 0 still names are the first train's prose `## Moves` sections, reported and never repaired (#297's rule that a closed engagement's artifacts are not edited to make a check pass); the Business and Growth drafts on Opus were declared Route-time escalations off their Sonnet baselines, so the Sonnet rows for those seats are audits only; the coordinator's four Fable sessions are interactive and unmeasured by design. Every runtime here stands **ruled**; no trial has run.

## Ruled out

| What | Why | What would reopen it |
|---|---|---|
| **Aider** | No read tool: the coordinator would pre-list corpus files with `--read`, so `## Corpus read` stops being what the seat chose and rung-0 line 5 loses its meaning | An *edit-only* pass kind, defined on the record template, where the inputs are pre-listed by law |
| **Jev** (TypeSafe AI) as a seat runtime | A non-generative decision model — choice, score or yes/no from a fed state, no text out. A seat pass, a co-sign, an audit and a gate all write prose, so it cannot carry any of them; rung 0 is deterministic with no model by law, so it has no place there either | Nothing on this registry. Its one Productcraft slot is the unearned rung-2 judge for `overclaimed-pointer` (map fog); its strongest fit is a Devcraft `PreToolUse` shadow guard, which is Devcraft's map, not this one |
| `pi-claude-bridge`, `pi-anthropic-auth` | Reuse Claude Pro/Max auth from a non-Anthropic client; whether that is within the subscription terms was **not found in primary sources** | A primary-source answer on the terms, recorded on the Pi row |
| Codex `ultra` effort | Auto-delegates sub-tasks, breaking one-invocation-one-seat (#267) | A ruling, not a trial |
| `gpt-6-astra` as any default | Rejected by the installed binary; no studio precedent | A Codex upgrade that accepts it, then a dated substitution on a named pass |
| Any memory add-on, on any row | Cross-session state contradicts the fresh-context rule every audit runs under | Never for a seat pass |

## Rules that carry over unchanged

- **A gate runs on a different lineage than the artifact's author** (#267's anchor-vendor rule), and so does a verification pass (#296 clause 4). A trial's audit or gate too.
- **No silent deviations.** A pass on any row other than the seat file's `model:` is a deviation with a one-line why against a named trigger, or a dated owner-approved substitution, or a declared trial — one of the three, in the Route entry.
- **Every invocation records its runtime and its meter line** — the row's `runtime:` string, the launch form verbatim, and the meter as the runtime reported it or `UNMEASURED`. Never an estimate. Dollar figures never enter a record (#272); an API-billed row puts its measured cash on the engagement's Close cost line.
- **The degradation ladder applies on any row.** A runtime that cannot read the private corpus or ledger says so (`grounding: manifest-only | none`) and never fabricates a citation. Every row above reads both today because they sit inside the repo; a row that could not would say so in its "Reads" column.

## Meter-source vocabulary

The authority for `meter_source` in every pass record; [trace/tracekit/engagement.py](../trace/tracekit/engagement.py) mirrors it as `METER_SOURCES` and `tests/test_registry.py` fails when the two drift. A value names **where the number came from**, never how good it is.

| Value | Row | What the coordinator copies |
|---|---|---|
| `Agent-tool usage` | 1 | the one total the Agent tool's usage field reports |
| `claude -p result.usage` | 2 | `input_tokens` → `input`, `output_tokens` → `output`, `cache_read_input_tokens` → `cached`, from the `result` message |
| `codex turn.completed.usage` | 3, 4, 5 | `input_tokens` → `input`, `output_tokens` → `output`, `cached_input_tokens` → `cached`, from the last `turn.completed` event in the JSONL |
| `codex footer` | 3, 4, 5 (plain form) | the `tokens used` number on stderr → `total` |
| `pi message_end usage` | 6 | the summed `usage` of assistant messages: `input`, `output`, `cacheRead` → `cached` |
| `hermes usage-file` | 7 | `input_tokens` → `input`, `output_tokens` → `output`, `cache_read_tokens` → `cached`, top level only; `total_including_auxiliary` goes in `## Notes` |
| `gemini stats.tokens` | 8 | per model: `prompt` → `input`, `candidates` → `output`, `cached` → `cached`, summed across models |
| `UNMEASURED` | any | `meter: null` — the runtime reported nothing the coordinator could copy |
