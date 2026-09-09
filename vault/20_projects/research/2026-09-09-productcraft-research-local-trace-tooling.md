---
title: "Productcraft map research — local-only trace tooling for multi-step agent runs (#284)"
date: 2026-09-09
project: productcraft
status: filed — resolves Productcraft map ticket #284
tags: [research, productcraft, wayfinder]
cost: $0 (web research by a subagent; no paid research)
---

# R2 — Local-only tracing for multi-step agent runs

Research file. Facts and sources only, no recommendation.
Question: options for tracing multi-step agent runs on a single laptop, where by default no payload leaves the machine, and a human later reads the trace to find which step went wrong.

Date: 2026-09-09. Drafted after 12 primary-doc calls; appended as research continued.

---

## Comparison table

| | (a) Arize Phoenix self-hosted | (b) OTel Python SDK + console/file exporter | (c) OpenLLMetry / Traceloop SDK | (d) Langfuse self-hosted | (e) Flat per-run JSON/JSONL manifest |
|---|---|---|---|---|---|
| **Install footprint** | `pip install arize-phoenix` (or `uvx arize-phoenix serve`, or `docker run arizephoenix/phoenix`). Single process + a DB. | `pip install opentelemetry-sdk` (+ `opentelemetry-api`). `ConsoleSpanExporter` ships inside `opentelemetry-sdk`, no extra package. | `pip install traceloop-sdk` (thin wrapper over OTel SDK + instrumentation packages). | Docker Compose: langfuse-web + langfuse-worker + Postgres + ClickHouse + Redis/Valkey + S3/MinIO — 6 containers minimum. | Zero. stdlib `json` + `open()`. |
| **Fully offline?** | Yes — docs claim "fully air-gapped" deployment; "Your traces, prompts, and data never leave your infrastructure." Check the Privacy/Network Security config cards to disable outbound. | Yes, trivially — nothing is emitted anywhere but the process you choose. Console exporter → stdout; a file is a 10-line custom `SpanExporter`. | Conditionally — it is an OTel exporter chain; you must set the OTLP endpoint (or a custom exporter) or it defaults to Traceloop's hosted API. Point it at `http://localhost:6006/v1/traces` (Phoenix) or a local exporter. | Yes — "Langfuse can be deployed within a VPC or on-premises in high-security environments. Internet access is optional." Telemetry env var needs confirming. | Yes by construction. |
| **What a record holds** | OpenInference spans: inputs/outputs, LLM prompt+completion, token counts, cost, latency, parent/child, tool calls, retrieval documents, arbitrary attributes. | Whatever you set: `set_attribute()` (str/num/bool/list), `add_event(name, attributes)`, parent/child via `start_as_current_span`, start/end timestamps, `Status`/`record_exception`. Cost is not a built-in — you set it as an attribute. | OpenInference/OpenLLMetry semantic conventions on top of OTel spans — model, prompts, completions, tokens; auto-captured from the wrapped SDK call. | Traces → observations (spans/generations/events) with input, output, metadata, model, usage, cost, latency, parent/child, sessions, users, tags, scores. | Whatever the orchestrator writes. Full freedom: step id, parent, timing, input, output, the moves list, provenance, doc ids. |
| **"Moves with provenance"** | Custom span attributes / span events on the step span; a structured JSON string in one attribute is the common workaround for nested data (OTel attrs are flat). | Same: one `add_event("move", {...})` per move, or a JSON-serialized attribute. Events carry their own timestamp — a natural per-move log. | Same as OTel (you drop to the raw OTel API for custom attributes). | `metadata` dict on the observation (arbitrary nested JSON, unlike OTel attributes which are flat). | Native — a `moves: [...]` array per step with `{op, target, from, to, source_doc, source_span}` is just JSON. |
| **"Which reference docs were in context"** | OpenInference has retrieval span semantics (`retrieval.documents.N.document.id/content/score`) — first-class in the UI. | Manual: a list attribute of doc ids, or one event per doc. | Auto-captured for wrapped vector-DB / retriever calls (Chroma, Pinecone, Qdrant, Weaviate, LanceDB, Marqo, Milvus, LangChain/LlamaIndex retrievers). | `metadata` or a dedicated retrieval observation; UI renders input/output blobs. | A `context_docs: [{path, sha, chunk_id}]` field per step. |
| **How a human reads it** | Web UI at `localhost:6006` — trace waterfall, span detail, filtering, annotations. | Plain text on stdout / a JSONL file — read with `less`, `jq`, or a custom viewer you write. No UI. | Whatever backend you exported to (Phoenix UI, Traceloop UI, console). | Web UI (Next.js app) — trace tree, session view, filtering. | Plain file + `jq`; or a purpose-built viewer, which is what Hamel Husain explicitly recommends building. |
| **License** | Elastic License 2.0 (ELv2) | Apache 2.0 | Apache 2.0 | MIT core, some EE add-ons behind a license key | n/a |
| **Last release** | (see notes below) | (see notes below) | (see notes below) | (see notes below) | n/a |

---

## Version / license facts (confirmed)

| Option | Package / image | Latest version | License | Python req |
|---|---|---|---|---|
| Phoenix | `arize-phoenix` (PyPI) | **20.9.0** | **Elastic-2.0** (ELv2) — classifier on PyPI, repo README: "This software is licensed under the terms of the Elastic License 2.0 (ELv2)." | `>=3.10,<3.15` |
| OTel Python | `opentelemetry-sdk` (PyPI) | **1.44.0** (api pinned `==1.44.0`, semconv `0.65b0`) | **Apache-2.0** | `>=3.10` |
| OpenLLMetry | `traceloop-sdk` (PyPI) | **0.62.3** | **Apache-2.0** | `>=3.10,<4` |
| Langfuse | `langfuse/langfuse` (GitHub) | (release tag not read; repo ~9,200 commits) | **MIT, except the `ee/` folders** — README: "This repository is MIT licensed, except for the `ee` folders." | n/a (Docker) |
| Flat JSONL | stdlib | n/a | n/a | any |

Note: PyPI JSON was read for version/license but the fetcher did not surface the exact upload timestamp for each. Versions above are the latest as served on 2026-09-09.

---

## (a) Arize Phoenix — self-hosted / local

**Install.** Three shapes, all local:
- `pip install arize-phoenix` then `phoenix serve` — "will launch Phoenix locally and make the application available in your browser," UI at `http://localhost:6006`.
- `uvx arize-phoenix serve` — no install step.
- `docker run -p 6006:6006 -p 4317:4317 -i -t arizephoenix/phoenix:latest`. Docs warn: "you should pin the phoenix version for production to the version of phoenix you plan on using. E.x. arizephoenix/phoenix:4.0.0". Image variants `:latest` (root) and `:latest-nonroot`.

**Ports.** 6006 = UI **and** OTLP-HTTP collector. 4317 = OTLP gRPC collector. 9090 = Prometheus metrics (optional).

**Storage.** SQLite by default, directory set by `PHOENIX_WORKING_DIR` (e.g. `-e PHOENIX_WORKING_DIR=/mnt/data`; needs a volume mount to persist). Postgres via `PHOENIX_SQL_DATABASE_URL=postgresql://user:pass@host:5432/db` (Postgres 14+), which replaces SQLite entirely. Other env vars: `PHOENIX_PORT` (default 6006), `PHOENIX_GRPC_PORT` (default 4317).

**Offline.** Yes. Self-hosting docs state deployments can be "fully air-gapped" and "Complete Privacy: Your traces, prompts, and data never leave your infrastructure." Docs also say "No license fees, no usage limits, no feature gates." There is a Privacy / Network Security configuration section to review for outbound calls — worth verifying empirically (e.g. run with network egress blocked) rather than trusting the claim, since the marketing page is the only source read here.

**What a span holds — OpenInference semantic conventions** (`Arize-ai/openinference`, `spec/semantic_conventions.md`):
- Span kind via `openinference.span.kind`, values: `"LLM"`, `"EMBEDDING"`, `"CHAIN"`, `"RETRIEVER"`, `"RERANKER"`, `"TOOL"`, `"AGENT"`, `"GUARDRAIL"`, `"EVALUATOR"`, `"PROMPT"`.
- I/O: `input.value`, `input.mime_type`, `output.value`, `output.mime_type`.
- Tokens: `llm.token_count.prompt`, `llm.token_count.completion`, `llm.token_count.total`, `llm.token_count.prompt_details.cache_read`, `llm.token_count.completion_details.reasoning`.
- Tools: `tool.name`, `tool.parameters` (JSON), `tool.description`.
- Free-form: `metadata` (a JSON **string**), `tag.tags` (list of strings).
- Parent/child, timing: inherited from OTel (these are OTel spans).

**Attaching "the moves this step made, with provenance."** No first-class field. Two workable routes: (1) serialize the move list into `metadata` as JSON — OpenInference already defines `metadata` as a JSON string, so nesting is legal there in a way it is not for raw OTel attributes; (2) one OTel span event per move (`span.add_event("move", {...})`), which gets you a per-move timestamp. Phoenix's UI renders attributes and events on the span detail pane.

**Attaching "which reference documents were in context."** This is the one place Phoenix is materially ahead of the alternatives — retrieval is first-class. Indexed flattening: `retrieval.documents.<index>.document.id`, `.document.content`, `.document.score`, `.document.metadata` (JSON). A `RETRIEVER`-kind span carrying these renders as a document list in the UI, per-document, with scores.

**How a human reads it.** Browser UI on `localhost:6006`: trace waterfall by run, click into a span, see input/output/attributes/events, filter and annotate. This is the strongest "which step went wrong" affordance of the five options.

**Caveat worth flagging.** ELv2 is *not* an OSI open-source license. For personal single-laptop use it is unrestrictive (it forbids offering the software as a managed service to third parties, and forbids circumventing license keys). If the trace tooling ever ships inside a product, that clause matters.

- https://arize.com/docs/phoenix/self-hosting
- https://arize.com/docs/phoenix/self-hosting/deployment-options/docker
- https://arize.com/docs/phoenix/self-hosting/deployment-options/terminal
- https://github.com/Arize-ai/phoenix
- https://github.com/Arize-ai/openinference/blob/main/spec/semantic_conventions.md
- https://pypi.org/project/arize-phoenix/

---

## (b) OpenTelemetry Python SDK + console / file exporter (no collector)

**Install.** `pip install opentelemetry-sdk` (pulls `opentelemetry-api==1.44.0`, `opentelemetry-semantic-conventions==0.65b0`, `typing-extensions>=4.5.0`). The console exporters need nothing else: "The `ConsoleSpanExporter` and `ConsoleMetricExporter` are included in the `opentelemetry-sdk` package."

**Offline.** Yes, unconditionally — there is no default endpoint and no collector. `ConsoleSpanExporter` writes span JSON to stdout. There is **no bundled file exporter**; you subclass `SpanExporter` (an `export(spans)` method that appends `span.to_json()` lines to a `.jsonl`) — about ten lines. Combine with `SimpleSpanProcessor` (write-on-end, good for crash-survivable debugging) rather than `BatchSpanProcessor` if you want the file complete even when the run dies mid-step.

Note: `opentelemetry-sdk[file-configuration]` exists as an extra, but that is *declarative file-based SDK configuration*, not a file exporter — easy to confuse.

**What a span holds.**
- Attributes: `span.set_attribute(key, value)`. Values are strings, numbers, booleans, or **homogeneous lists** of those. **Not nested dicts** — this is the constraint that shapes everything below.
- Semantic attributes: `from opentelemetry.semconv.trace import SpanAttributes` then `set_attribute(SpanAttributes.HTTP_METHOD, "GET")`.
- Events: `span.add_event("Gonna try it!")`, optionally with an attributes dict. Docs describe events as "something happening" during a span's lifetime, essentially "primitive log" entries. Each event carries its own timestamp.
- Parent/child: nesting `with tracer.start_as_current_span("parent")` / `... "child"` makes the child appear nested; context propagates implicitly.
- Status and errors: `span.set_status(Status(StatusCode.ERROR))` and `span.record_exception(ex)`.
- Timing: start/end timestamps are automatic.
- Cost: **not a concept** in vanilla OTel. You set it yourself as an attribute.

**Attaching "the moves this step made, with provenance."** Best fit is `add_event` per move: `span.add_event("move", {"op": "split", "from": "opp-12", "to": ["opp-12a","opp-12b"], "source_quote_id": "q-88"})`. Attribute values inside the event are subject to the same flat-type rule, so anything nested gets `json.dumps`'d into one string field. The per-move timestamp you get for free is genuinely useful when the question is "which move broke it".

**Attaching "which reference documents were in context."** A list attribute of doc ids (`ctx.doc_ids` = list of strings) plus a parallel list of hashes, or one event per document. There is no retrieval convention in vanilla OTel — you would be reimplementing OpenInference's `retrieval.documents.*` by hand, at which point you may as well emit OpenInference-shaped keys so a Phoenix UI can read them later.

**How a human reads it.** Plain text on stdout, or your JSONL file via `less` / `jq` / a small script. No UI. The escape hatch: because the spans are OTel spans, swapping `ConsoleSpanExporter` for `OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")` later gives you the Phoenix UI over the exact same instrumentation. This is the "file now, UI later, no re-instrumentation" path.

- https://opentelemetry.io/docs/languages/python/exporters/
- https://opentelemetry.io/docs/languages/python/instrumentation/
- https://pypi.org/project/opentelemetry-sdk/

---

## (c) OpenLLMetry / Traceloop SDK

**What it is.** An OTel-native auto-instrumentation layer. `pip install traceloop-sdk`. Self-described as "non-intrusive" monitoring of LLM execution using OpenTelemetry.

**What it wraps.**
- LLM providers: OpenAI, **Anthropic**, Bedrock, Cohere, Google Generative AI, Groq, HuggingFace, Mistral, Ollama, Replicate, Vertex AI, LiteLLM.
- Vector DBs: Chroma, Pinecone, Qdrant, Weaviate, LanceDB, Marqo, Milvus.
- Frameworks: LangChain, LlamaIndex, CrewAI, LangGraph, Haystack, Transformers.
- Dependencies confirm the shape: it pulls `opentelemetry-api`/`-sdk` (v1.38.0+) plus OTLP gRPC and HTTP exporters.

**Where it sends by default — the important fact.** The default base URL is `https://api.traceloop.com`. Docs: *"This defines the OpenTelemetry endpoint to connect to. It defaults to https://api.traceloop.com"*. Worse for a no-payload-leaves-the-machine requirement: *"If this is not set, and the base URL is set to `https://api.traceloop.com`, the SDK will generate a new API key automatically"* — i.e. the out-of-the-box path silently provisions a cloud account and ships payloads off the laptop. **This one must be actively disarmed.**

**Making it local.** Three levers:
1. `Traceloop.init(exporter=...)` — pass any OTel exporter object. Docs: *"If this is set, Base URL, API key and headers configurations are ignored."* Example given uses `ZipkinExporter(endpoint="http://localhost:9411/api/v2/spans")`; a `ConsoleSpanExporter()`, your file exporter, or `OTLPSpanExporter(endpoint="http://localhost:6006/v1/traces")` substitutes directly. This is the cleanest kill-switch because it bypasses base URL, key and headers in one move.
2. `api_endpoint` param / `TRACELOOP_BASE_URL` env var — repoint OTLP at local Phoenix.
3. `telemetry_enabled` param / `TRACELOOP_TELEMETRY` env var — this is the SDK's **own** anonymous usage telemetry, separate from trace export. Set it off too.

Other params: `app_name`, `api_key` / `TRACELOOP_API_KEY`, `headers` / `TRACELOOP_HEADERS`, `disable_batch` (Python: `disable_batch`; useful so spans flush per-step rather than in batches).

**What a span holds.** OTel spans carrying OpenInference/OpenLLMetry LLM conventions, auto-populated from the wrapped call: model, prompts, completions, token counts, latency, parent/child. Vector-DB calls become retrieval spans automatically.

**Attaching moves and context docs.** No dedicated API. You drop to the raw OTel API (`trace.get_current_span().set_attribute(...)` / `.add_event(...)`) alongside the auto-instrumented spans, so all of section (b)'s constraints and techniques apply verbatim.

**How a human reads it.** Whatever backend you exported to. Pointed at local Phoenix, you get the Phoenix UI. Pointed at a console/file exporter, you get plain text.

**Honest read of the fit.** OpenLLMetry earns its keep when the value is auto-capture of provider SDK calls you did not write instrumentation for. If the orchestrator is your own code and the interesting content is *your* per-step moves rather than raw LLM I/O, it adds a default-cloud dependency for auto-capture you may not need.

- https://github.com/traceloop/openllmetry
- https://www.traceloop.com/docs/openllmetry/configuration
- https://pypi.org/project/traceloop-sdk/

---

## (d) Langfuse self-hosted

**Footprint.** Heaviest of the five by a wide margin. Required components:
- `langfuse-web` container (UI + APIs)
- `langfuse-worker` container (async event processing)
- **Postgres** — transactional data
- **ClickHouse** — OLAP store for traces, observations, scores
- **Redis / Valkey** — cache and queue
- **S3 / blob storage** (MinIO locally) — incoming events, multi-modal inputs, exports

That is six services minimum for a single-laptop trace viewer. Docs position Docker Compose as suitable for "local use and testing" on "a single VM without high availability, scaling, or backups" and explicitly **not recommended for production self-hosting**. Docs read did not state CPU/RAM requirements.

**Offline.** Yes, with one thing to turn off. Self-hosting docs: "Langfuse can be deployed within a VPC or on-premises in high-security environments. Internet access is optional." But the repo README has a dedicated telemetry section stating usage statistics are reported **by default** for self-hosted instances, with the opt-out quoted directly: *"For Langfuse OSS, you can opt out by setting `TELEMETRY_ENABLED=false`."* So: offline yes, but `TELEMETRY_ENABLED=false` is a required step, not optional hygiene. The configuration page read here did not itself list that variable — the README is the source.

**What a record holds.** Traces contain observations of type span / generation / event, each with input, output, `metadata`, model, usage, cost, latency, and parent/child links. Trace-level: sessions, users, tags, and scores (eval results attached after the fact).

**Attaching moves and context docs.** Langfuse's `metadata` accepts arbitrary **nested JSON**, unlike OTel's flat attribute types. That is a real ergonomic advantage for a `moves: [...]` array and a `context_docs: [...]` list — no `json.dumps` into a string field.

**How a human reads it.** Next.js web UI: trace tree, session view, filtering, score annotation.

**License.** MIT for the repository "except for the `ee` folders"; some add-on features require a license key. EE-gated examples named: UI Customization, Organization Creators.

- https://langfuse.com/self-hosting
- https://langfuse.com/self-hosting/configuration
- https://github.com/langfuse/langfuse

---

## (e) Flat per-run JSON / JSONL manifest written by the orchestrator

**Install footprint.** Zero. `json` + `open()`.

**Offline.** By construction.

**What a record holds.** Entirely your call. Nothing in the other four options can hold anything this cannot; the difference is that everything is hand-rolled, including the reader.

**Attaching moves and context docs.** This is the case where the requirement is native rather than worked around. A step record can be literally:
```json
{"step": 4, "parent": 3, "started": "...", "ended": "...", "tool": "...",
 "input_ref": "...", "output_ref": "...",
 "moves": [{"op": "split", "target": "opp-12", "into": ["opp-12a", "opp-12b"], "because": "q-88"}],
 "context_docs": [{"path": "...", "sha": "...", "chunk_id": 7}]}
```
No flat-attribute restriction, no JSON-in-a-string, no semantic convention to conform to.

**How a human reads it.** `jq`, or a viewer you write. See the Husain note below — this is the specific thing he recommends building.

### Published examples of teams doing this

**Hamel Husain — split the recommendation.** His position is more precise than "roll your own", and the split matters here:
- On the *logging/observability plumbing*: **don't build it.** "For logging and observability infrastructure, use existing tools rather than building from scratch" — he names Langsmith, Braintrust, Humanloop, and Phoenix Arize, on the grounds that they auto-instrument.
- On the *viewer*: build it, after trying the cheap thing first. "First see if using an excel spreadsheet or a jupyter notebook will fit your needs. If not, it is often advantageous to build your own data viewer." He suggests Gradio, Streamlit, or FastHTML to keep the build small.
- The underlying rule, per the same session: don't build what isn't your core product.
- His broader "LOOK AT THE DATA" line — read traces, categorize failures, count them, and let that drive application-specific metrics — is the reason the *reading* affordance is the load-bearing requirement, not the storage format. Error analysis is the thing most teams skip in favor of writing LLM judges or building dashboards.
- Sources: https://hamel.dev/notes/llm/officehours/observability.html ; https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html ; https://hamel.dev/blog/posts/evals-faq/

**Teresa Torres — change sets (Vistaly AI-generated opportunity solution trees).** The canonical post is **https://www.producttalk.org/behind-the-scenes-ai-osts/** (the `/2025/07/change-sets/` URL in the brief 404s). What it actually says:
- The AI service returns **both** an updated tree **and** a change set — "the steps it took to get there", a step-by-step instruction sequence for regenerating the output tree from the current one.
- The operations are a fixed vocabulary: **add, delete, reframe, merge, split**. Worked examples in the post: "Add outcome", "Add opportunity A as a child of that outcome", and a case where "opportunity B merges with opportunity C" and the change set documents which source opportunities and children move between nodes.
- **Provenance** rides on the operations: each operation records which node is affected and how, and separately, "every card is backed by verbatim quotes you can audit." Product Talk frames the problem as incremental synthesis — merging new qualitative data into an existing hierarchical representation "while preserving provenance and editable structure."
- **The failure they found is the interesting part, and it is exactly the failure mode this research question is about.** The change set was supposed to be replayable: apply it in order to the current tree and arrive at the emitted tree. It wasn't. "The tree that the change set generated was different from the tree that the service outputted" — i.e. **the narration diverged from the actual result.** The post's phrasing: "the change set didn't generate the recommendation."
- **What they built is a validation loop, not an audit-and-replay viewer.** An agentic loop where the model generates a change set, calls a validation tool that replays it, and on failure receives correction instructions and regenerates until it validates. The replay is machine-enforced pre-emission rather than human-read post-hoc.
- Related: the *Just Now Possible* episode on Momental ("Building GitHub for Product Management," aired 2026-04-22) covers an OODA-loop document-processing agent maintaining a living knowledge graph and surfacing cross-team conflicts as merge conflicts — https://www.producttalk.org/building-github-for-product-management-how-momental-uses-ai-to-find-merge-conflicts-in-strategy/
- Teresa Torres's own AI build diary discusses traces but for eval, not move-narration: "A trace is a detailed record of an AI interaction. It includes the user input, system prompts, tool calls, intermediate steps, and final LLM responses" and "Observability (being able to see your traces) is everything. But to do this ethically, we have to be transparent with our customers about this." — https://www.producttalk.org/ai-playbook/

**Load-bearing caution the Torres case supplies:** a self-narrated move list is a *claim* about what the step did, not a *record* of it. It can diverge from the actual output. Any design that has an orchestrator narrate its own moves needs either a validation replay (Vistaly's answer) or a diff of actual before/after state, or the trace will confidently mislead the human reading it.

---

## Claude Agent SDK (Python) and Claude Code — what is exposed for tracing

### 1. Hooks

All Claude Code hook events receive a **common field set**:
`session_id`, `transcript_path` ("Path to conversation JSON"), `cwd`, `permission_mode` (`"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"`, `"bypassPermissions"`), `hook_event_name`, `prompt_id` (UUID for the user prompt; absent until first user input), `effort`, `agent_id` (**present only when the hook fires inside a subagent**), `agent_type`.

Event-specific fields:

| Event | Extra input fields | Matcher values |
|---|---|---|
| `PreToolUse` | `tool_name`, `tool_input`, `tool_use_id` | — |
| `PostToolUse` | `tool_name`, `tool_input`, `tool_response`, `tool_use_id` | — |
| `PostToolUseFailure` | `tool_name`, `tool_input`, `error`, `tool_use_id` | — |
| `SessionStart` | `model` (not always present) | `startup`, `resume`, `clear`, `compact`, `fork` |
| `SessionEnd` | — | `clear`, `resume`, `logout`, `prompt_input_exit`, `other` |
| `Stop` | `last_assistant_message`, `effort` | — |
| `SubagentStop` | `agent_id`, `agent_type` (e.g. `"Explore"`), `last_assistant_message` | — |
| `UserPromptSubmit` | `user_input`, `permission_mode` | — |
| `PreCompact` / `PostCompact` | — | `manual`, `auto` |
| `Notification` | `notification_type` | `permission_prompt`, `idle_prompt`, `agent_needs_input`, `agent_completed`, … |

Hook **output** fields: `hookSpecificOutput` (e.g. `permissionDecision`, `permissionDecisionReason`), `systemMessage`, `additionalContext`, `updatedInput` (PreToolUse can rewrite tool input), `terminalSequence`.

Practical consequence: `PreToolUse` + `PostToolUse` give you a complete per-step in/out pair keyed by `tool_use_id`, with `session_id` as the run key and `agent_id` distinguishing subagent steps — which is enough to write option (e)'s JSONL from outside the orchestrator, no library, no payload leaving the machine.

- https://code.claude.com/docs/en/hooks

### 2. Transcript JSONL on disk (verified locally, 2026-09-09)

**Location:** `~/.claude/projects/<url-encoded-project-path>/<session-uuid>.jsonl`. The directory name is the absolute project path with separators replaced (`/Users/seanwinslow/Code-Brain/code-brain` → `-Users-seanwinslow-Code-Brain-code-brain`). On Windows, `%USERPROFILE%\.claude\`.

**Verified structure** (inspected a real 1,008-line transcript on this machine):
- Record `type` values observed: `user`, `assistant`, `system`, `attachment`, `queue-operation`, `last-prompt`, `custom-title`.
- Top-level keys observed: `type`, `uuid`, `parentUuid` (**the chain link — this is the parent/child spine**), `timestamp`, `sessionId`, `isSidechain`, `cwd`, `gitBranch`, `version`, `entrypoint`, `userType`, `promptId`, `requestId`, `effort`, `message`, `toolUseResult`, `sourceToolAssistantUUID`, `sourceToolUseID`, `isMeta`, `attributionSkill`, `attributionPlugin`, `toolDenialKind`, `permissionMode`, `origin`, `promptSource`, `classifierMetaLines`, `subtype`, `hookCount`, `hookInfos`, `hookErrors`, `hookAdditionalContext`, `preventedContinuation`, `stopReason`, `hasOutput`, `level`, `toolUseID`, `leafUuid`, `agentId`.
- `assistant` records carry `message` with keys `content`, `diagnostics`, `id`, `model`, `role`, `stop_details`, `stop_reason`, `stop_sequence`, `type`, `usage`.
- `usage` is rich: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `cache_creation.ephemeral_5m_input_tokens` / `.ephemeral_1h_input_tokens`, `server_tool_use.{web_search_requests,web_fetch_requests}`, `service_tier`, `speed`, `inference_geo`, and a per-`iterations` breakdown. **Token counts yes; no dollar cost field** — cost is derived, not recorded.
- Tool calls appear as `tool_use` content blocks inside assistant messages (observed names in one session: `Bash` ×120, `Read` ×15, `Edit` ×29, `Write` ×6, `Skill` ×2, `Agent` ×2, `WebFetch`, `ToolSearch`, `AskUserQuestion`, `SendUserFile`). Results come back on `toolUseResult` with `sourceToolUseID` / `sourceToolAssistantUUID` cross-references.
- `attributionSkill` (194 occurrences in that session) records which skill a record is attributable to — a provenance field that already exists.

**Subagent invocation records — verified.** Beside each `<session-uuid>.jsonl` there is a directory `<session-uuid>/` containing:
- `subagents/agent-<id>.jsonl` plus `agent-<id>.meta.json` — one pair per subagent invocation.
- `tool-results/` — large tool payloads spilled to separate files (observed: `hook-<uuid>-3-additionalContext.txt`).

Subagent records carry `agentId`, `isSidechain: true`, their own `cwd` (which can differ from the parent session's — in the sample, the subagent ran in a different repo than the parent), `parentUuid: null` at their root, and the parent's `sessionId` and `promptId`. So the parent↔subagent join is `sessionId` + `promptId` + `agentId`.

Community tooling that already reads this format: `simonw/claude-code-transcripts` (publishing transcripts), `daaain/claude-code-log` (JSONL → HTML/Markdown viewer).

- https://github.com/simonw/claude-code-transcripts
- https://github.com/daaain/claude-code-log

### 3. Claude Code's own OpenTelemetry support

Enable with `CLAUDE_CODE_ENABLE_TELEMETRY=1`. Three signals:

| Signal | Env var | Exporter values |
|---|---|---|
| Metrics | `OTEL_METRICS_EXPORTER` | `otlp`, `prometheus`, `console`, `none` |
| Logs/Events | `OTEL_LOGS_EXPORTER` | `otlp`, `console`, `none` |
| Traces (**beta**) | `OTEL_TRACES_EXPORTER` | `otlp`, `console`, `none` |

Traces additionally require `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`. Transport: `OTEL_EXPORTER_OTLP_PROTOCOL` (`grpc` / `http/json` / `http/protobuf`), `OTEL_EXPORTER_OTLP_ENDPOINT` (e.g. `http://localhost:4317`), signal-specific `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`. Intervals: `OTEL_METRIC_EXPORT_INTERVAL` (default 60000ms), `OTEL_LOGS_EXPORT_INTERVAL` (5000ms), `OTEL_TRACES_EXPORT_INTERVAL` (5000ms).

**Payload-content flags — off by default, which is why the default posture is already "no payload leaves":** `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_ASSISTANT_RESPONSES=1`, `OTEL_LOG_TOOL_DETAILS=1` (tool parameters), `OTEL_LOG_TOOL_CONTENT=1` (tool I/O content), `OTEL_LOG_RAW_API_BODIES=1` **or** `file:<dir>` (full API request/response JSON — note the `file:` form writes bodies to a local directory rather than the exporter).

**Beta span hierarchy** — directly usable as a multi-step run trace:
```
claude_code.interaction          (root span, one per prompt)
├── claude_code.llm_request
├── claude_code.hook             (requires ENABLE_BETA_TRACING_DETAILED=1)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (subagent spans when the Agent tool is used)
```
Span attributes: `claude_code.interaction` → `user_prompt`, `user_prompt_length`, `interaction.sequence`, `interaction.duration_ms`. `claude_code.llm_request` → `model`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `ttft_ms`, `request_id`, `stop_reason`. `claude_code.tool` → `tool_name`, `tool_use_id`, `duration_ms`, `file_path` (Read/Edit/Write), `full_command` (Bash).

**Propagation:** Bash/PowerShell subprocesses inherit a `TRACEPARENT` env var for end-to-end tracing; model requests carry a W3C `traceparent` header to the Anthropic API when `ANTHROPIC_BASE_URL` is unset; **the Agent SDK and `-p` sessions can read an inbound `TRACEPARENT` to parent their spans into a caller's trace.** That last one is how a Python orchestrator's spans and Claude Code's spans end up in one tree.

**Events** (all prefixed `claude_code.`): `user_prompt`, `assistant_response`, `api_request` (attrs incl. `cost_usd`, `input_tokens`, `output_tokens`, `duration_ms`, `request_id`, `speed`, `effort`), `api_error`, `api_refusal`, `api_request_body`, `api_response_body`, `tool_result` (`tool_name`, `tool_use_id`, `success`, `duration_ms`, `error_type`, `tool_parameters`), `tool_decision` (`decision` accept/reject, `source`: `config`/`hook`/`user_permanent`/`user_temporary`/`user_abort`/`user_reject`), `permission_mode_changed`, `auth`, `mcp_server_connection`.

**Metrics:** `claude_code.session.count`, `.lines_of_code.count`, `.pull_request.count`, `.commit.count`, `.cost.usage` (USD), `.token.usage`, `.code_edit_tool.decision`, `.active_time.total`.

**Standard attributes on all signals:** `session.id`, `app.version`, `app.entrypoint`, `organization.id`, `user.account_uuid`, `user.account_id`, `user.id`, `user.email`, `terminal.type`, plus events-only `prompt.id`, `message.uuid`, `client_request_id`.

**Privacy note that matters for a laptop-local design:** `user.email` and `user.account_uuid` are attached to signals by default (`OTEL_METRICS_INCLUDE_ACCOUNT_UUID` defaults true). Fine when the endpoint is `localhost`, worth knowing before any endpoint change. Also: `claude --debug` distinguishes `[3P telemetry]` errors (your exporter) from `[Anthropic telemetry]` lines (Anthropic's separate operational telemetry, which is not the same channel).

**Local-only wiring:** `OTEL_*_EXPORTER=console` needs no listener at all; `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317` with Phoenix on 4317 gives a UI with nothing leaving the machine.

- https://code.claude.com/docs/en/monitoring-usage

### 4. claude-agent-sdk (Python) in-process observability

**Message stream types:** `AssistantMessage` (with `content` blocks — `TextBlock`, `ToolUseBlock` carrying `.name`, `ToolResultBlock`), `ResultMessage`, `TaskNotificationMessage` (background task status, e.g. `"stopped"`), `StreamEvent` (partial-message streaming), `HookEventMessage`.

**`ResultMessage` fields:** `result`, `terminal_reason` (`"success"`, `"aborted_streaming"`, `"aborted_tools"`), `subtype` (`"success"`, `"error"`), `total_cost_usd`, `usage`, `duration_ms`, `num_turns`, `session_id`.

**Hooks in-process:** `ClaudeAgentOptions.hooks: dict[HookEvent, list[HookMatcher]] | None`, with `HookMatcher` configuring `PreToolUse` / `PostToolUse` etc. Two flags surface extra records into the message stream: `include_hook_events: bool = False` and `include_partial_messages: bool = False`.

Practical consequence: iterating the message stream and writing each `ToolUseBlock` / `ToolResultBlock` pair plus the terminal `ResultMessage` to a JSONL is option (e), implemented in roughly twenty lines, with cost and duration already computed by the SDK. `total_cost_usd` has documented accuracy caveats (see the SDK's cost-tracking page).

- https://code.claude.com/docs/en/agent-sdk/python

---

## Source list

**Arize Phoenix / OpenInference**
- https://arize.com/docs/phoenix/self-hosting
- https://arize.com/docs/phoenix/self-hosting/deployment-options/docker
- https://arize.com/docs/phoenix/self-hosting/deployment-options/terminal
- https://github.com/Arize-ai/phoenix
- https://github.com/Arize-ai/openinference/blob/main/spec/semantic_conventions.md
- https://pypi.org/project/arize-phoenix/

**OpenTelemetry Python**
- https://opentelemetry.io/docs/languages/python/exporters/
- https://opentelemetry.io/docs/languages/python/instrumentation/
- https://pypi.org/project/opentelemetry-sdk/

**OpenLLMetry / Traceloop**
- https://github.com/traceloop/openllmetry
- https://www.traceloop.com/docs/openllmetry/configuration
- https://pypi.org/project/traceloop-sdk/

**Langfuse**
- https://langfuse.com/self-hosting
- https://langfuse.com/self-hosting/configuration
- https://github.com/langfuse/langfuse

**Flat manifest / published practice**
- https://hamel.dev/notes/llm/officehours/observability.html
- https://hamel.dev/blog/posts/evals-faq/
- https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html
- https://hamel.dev/blog/posts/revenge/
- https://www.producttalk.org/behind-the-scenes-ai-osts/  ← the change-sets post
- https://www.producttalk.org/ai-playbook/
- https://www.producttalk.org/building-github-for-product-management-how-momental-uses-ai-to-find-merge-conflicts-in-strategy/
- https://www.producttalk.org/vistaly/

**Claude Code / Agent SDK**
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/monitoring-usage
- https://code.claude.com/docs/en/agent-sdk/python
- https://github.com/simonw/claude-code-transcripts
- https://github.com/daaain/claude-code-log
- Local filesystem inspection of `~/.claude/projects/.../*.jsonl` and `.../<session>/subagents/`, 2026-09-09

---

## Gaps / unverified

1. **Exact PyPI upload dates** for arize-phoenix 20.9.0, opentelemetry-sdk 1.44.0 and traceloop-sdk 0.62.3 were not surfaced by the fetcher — versions are current as served 2026-09-09, but "last release date" is unconfirmed. Langfuse's latest release tag was not read at all.
2. **Phoenix's air-gap claim comes from Arize's own marketing/docs page**, not from an independent test. Worth verifying by running it with egress blocked before relying on it.
3. **Langfuse's `TELEMETRY_ENABLED=false`** is confirmed in the repo README but was *not* present on the configuration docs page read here — check the current configuration reference for the canonical default and payload contents.
4. **Phoenix `px.launch_app()` / in-notebook mode, default SQLite path, and `PHOENIX_COLLECTOR_ENDPOINT` default** were not confirmed; the terminal deployment page did not cover them.
5. The Torres change-set post was reached via search after the URL in the brief (`producttalk.org/2025/07/change-sets/`) returned 404; the operations list (add/delete/reframe/merge/split) and the divergence failure are quoted from `behind-the-scenes-ai-osts`, but the post may have a companion piece not found here.
6. Claude Code's beta trace support (`CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`) is **beta** — span names and attributes above are as documented on 2026-09-09 and are liable to change.
