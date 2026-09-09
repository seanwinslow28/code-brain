---
title: "Productcraft map research — prior art for cross-studio handoff contracts (#285)"
date: 2026-09-09
project: productcraft
status: filed — resolves Productcraft map ticket #285
tags: [research, productcraft, wayfinder]
cost: $0 (web research by a subagent; no paid research)
---

# R3 — Typed handoff between two autonomous teams that keep separate memories

Research pass, facts and sources only. No recommendation.
Question: what documented patterns exist for a typed handoff between two agent teams (or two org functions) with separate memories and decision records, where one frames a problem and the other designs and proves the system, and the first later reads the second's decisions back?

Compiled 2026-09-09. Draft in progress; sections appended as sources land.

---

## 1. Google Agent2Agent (A2A) — agent cards, tasks, artifacts

Source: A2A Protocol specification, https://a2a-protocol.org/latest/specification/

**The Agent Card is the published interface contract.** A metadata document served by an A2A Server describing what it can be asked to do. Fields: `id`, `name`, `description`, `url` (service endpoint), `provider`, `capabilities` (feature flags: `streaming`, `pushNotifications`, `extendedAgentCard`), `skills` (array of operational capabilities), `securitySchemes` (API key, OAuth2, mTLS), `security`, `interfaces` (supported protocol bindings and versions). `GetExtendedAgentCard` fetches an authenticated, more detailed card — so the contract itself is tiered by trust level.

**The Task is the unit of delegated work and it is stateful and addressable.** Fields:
- `id` — server-generated unique identifier
- `contextId` — logical grouping for related interactions (this is the thread key across multiple tasks)
- `status` — `{ state, message?, timestamp }`
- `artifacts` — array of output results
- `history` — array of exchanged messages
- `metadata` — custom key-value data

**TaskState enum (the lifecycle):** `TASK_STATE_UNSPECIFIED`, `TASK_STATE_SUBMITTED`, `TASK_STATE_WORKING`, `TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_CANCELED`, `TASK_STATE_INPUT_REQUIRED`, `TASK_STATE_REJECTED`, `TASK_STATE_AUTH_REQUIRED`. Three terminal states (completed/failed/canceled) plus a terminal *refusal* (`REJECTED`) and two *interrupted-pending-you* states (`INPUT_REQUIRED`, `AUTH_REQUIRED`). The typed protocol therefore encodes "I will not do this" and "I need more from you" as first-class outcomes, not as free text.

**Message fields:** `messageId`, `contextId`, `taskId`, `role` (`ROLE_USER` = client→server, `ROLE_AGENT` = server→client), `parts` (text / file / structured JSON data), `metadata`, `extensions` (URIs), and — key for cross-referencing — **`referenceTaskIds`**, an explicit list of related task references.

**Artifacts** are the durable outputs, composed of `Part` objects (text, file, structured data), persisted *separately from the conversational messages*. This is the separation that matters for the question: the delivering agent's product is not its trace.

**Delegation loop:** client calls `SendMessage` (or `SendStreamingMessage`) with a `Message` carrying requirements → server returns a `Task` with an `id` → client tracks by polling `GetTask`, streaming (`SubscribeToTask`, receiving `TaskStatusUpdateEvent` / `TaskArtifactUpdateEvent`), or webhooks (`CreatePushNotificationConfig` / `GetPushNotificationConfig` / `ListPushNotificationConfigs` / `DeletePushNotificationConfig`). `ListTasks` gives cursor-based pagination filtered by context, status, or timestamp — i.e. the framing agent can later enumerate everything the delivering agent did under a `contextId`. `CancelTask` is idempotent.

**What crosses, in A2A terms:** *down* — a Message with parts and a contextId; *up* — a Task whose `status.state` is typed, whose `artifacts` are the deliverable, and whose `history` is optionally retrievable. Notably the client does **not** receive the server agent's internal reasoning or memory: A2A is explicitly an opaque-agent protocol. Back-reference is via `contextId` + `referenceTaskIds` + `ListTasks`.

---

## 2. Model Context Protocol — the client/server boundary as a negotiated contract

Source: MCP specification, Lifecycle (version 2025-06-18), https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle

Three phases: **Initialization** (capability negotiation and protocol version agreement), **Operation**, **Shutdown**.

The client MUST open with an `initialize` request carrying `protocolVersion`, `capabilities`, and `clientInfo` (`name`, `title`, `version`). The server MUST respond with its own `capabilities`, `serverInfo`, and an optional free-text **`instructions`** field. The client then sends `notifications/initialized`.

**Capability vocabulary — this is the typed surface of the boundary:**

| Side | Capability | Meaning |
|---|---|---|
| Client | `roots` | can provide filesystem roots |
| Client | `sampling` | supports LLM sampling requests *from* the server |
| Client | `elicitation` | supports server-initiated elicitation (asking the user) |
| Client | `experimental` | non-standard features |
| Server | `prompts` | offers prompt templates |
| Server | `resources` | provides readable resources |
| Server | `tools` | exposes callable tools |
| Server | `logging` | emits structured log messages |
| Server | `completions` | argument autocompletion |
| Server | `experimental` | non-standard features |

Sub-capabilities: `listChanged` (prompts, resources, tools) and `subscribe` (resources only).

The binding rule: "Both parties **MUST**: Respect the negotiated protocol version [and] Only use capabilities that were successfully negotiated." Version negotiation is explicit — client sends its latest, server answers with the same version or its own latest; a client that can't speak the server's answer SHOULD disconnect. Over HTTP the agreed version is pinned on every subsequent request via the `MCP-Protocol-Version` header.

**Reported failure cases** (the spec's own error-handling list): protocol version mismatch, failure to negotiate required capabilities, request timeouts. Example error: `-32602 "Unsupported protocol version"` with `data: { supported: [...], requested: ... }`. Timeout guidance: senders SHOULD time out and issue a cancellation notification; progress notifications MAY reset the clock but implementations SHOULD still enforce a maximum.

**The transferable idea:** MCP does not share memory across the boundary. It shares a *declaration of what each side can be asked for*, agreed once, enforced for the session, versioned, and with a defined failure when the two sides don't line up.

---

## 3. The context-sharing argument: Cognition vs Anthropic

### 3a. Cognition, "Don't Build Multi-Agents"
Source: https://cognition.com/blog/dont-build-multi-agents

Two stated principles:
1. **"Share context, and share full agent traces, not just individual messages."**
2. **"Actions carry implicit decisions, and conflicting decisions carry bad results."**

The Flappy Bird worked example: one subagent misreads the task and builds a Mario Bros. background, another produces a mismatched asset, and the coordinator has no mechanism to reconcile the two interpretations. The diagnosis: **"The decision-making ends up being too dispersed and context isn't able to be shared thoroughly enough."**

Recommended architecture: a **single-threaded linear agent** where "the context is continuous"; for tasks too long for one context, insert an LLM-based history compressor that condenses "actions & conversation into key details, events, and decisions."

Failure modes named: implicit decisions (unstated assumptions surfacing as conflicts later); dispersed decision-making (parallel agents can't see each other's choices); context loss / misunderstanding of the assigned task from missing conversational context.

Note the tension this creates with any A2A/MCP-style opaque handoff: Cognition's position is that passing a *summary* rather than the *full trace* is precisely the defect. Anything that keeps two memories separate is, on this view, buying isolation at the price of implicit-decision conflict — which is the risk a typed contract has to price in.

### 3b. Anthropic, "How we built our multi-agent research system"
Source: https://www.anthropic.com/engineering/multi-agent-research-system

Architecture: "an orchestrator-worker pattern, where a lead agent coordinates the process while delegating to specialized subagents that operate in parallel."

**What the LeadResearcher passes down** — a structured task description with four elements: **objective**, **output format**, **guidance on tools and sources**, and **task boundaries**. Stated consequence of skimping: "without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information."

**What comes back up:** subagents "return findings to the LeadResearcher," which "synthesizes these results and decides whether more research is needed."

**Memory:** the LeadResearcher begins by "saving its plan to Memory to persist the context, since if the context window exceeds 200,000 tokens it will be truncated and it is important to retain the plan." Agents "retrieve stored context like the research plan from their memory rather than losing previous work when reaching the context limit."

**Artifact handoff (directly relevant):** rather than routing all output through the coordinator, "specialized agents can create outputs that persist independently. Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator." That is the reference-not-payload pattern — the same shape as A2A artifacts.

**A separate downstream agent for provenance:** the system "passes all findings to a CitationAgent, which processes the documents and research report to identify specific locations for citations."

**Reported failure modes:** "spawning 50 subagents for simple queries"; "scouring the web endlessly for nonexistent sources"; agents "distracting each other with excessive updates"; duplicated work and gaps from thin task descriptions; ~"15× more tokens than chats"; and "Minor system failures can be catastrophic for agents" because errors compound in stateful long-running runs.

---

## 4. Contract-first spawning and the handoff primitive

### 4a. OpenAI Agents SDK — `handoff()`
Source: https://openai.github.io/openai-agents-python/handoffs/

A handoff is **represented to the model as a tool**: handing off to an agent named "Refund Agent" surfaces as the tool `transfer_to_refund_agent`.

`handoff()` parameters:
- `agent` — "The agent to which things will be handed off"
- `tool_name_override` — overrides the default `transfer_to_<agent_name>`
- `tool_description_override`
- `on_handoff` — "A callback function executed when the handoff is invoked" (the place to do data-fetch or logging at the boundary)
- `input_type` — **"The schema for the handoff tool-call arguments"** — i.e. the typed payload the handing-off agent must fill in
- `input_filter` — filters what history the receiving agent sees
- `is_enabled` — boolean or function, so a handoff can be conditionally available
- `nest_handoff_history` — per-handoff override of RunConfig history nesting

**Default state carried:** "the new agent takes over the conversation, and gets to see the entire previous conversation history," unless an input filter or history configuration narrows it. `HandoffInputData` exposes `input_history`, `pre_handoff_items`, `new_items`, `input_items`, `run_context`. Prebuilt filters live in `agents.extensions.handoff_filters` (e.g. `remove_all_tools`). A recommended system-prompt preamble is shipped at `agents.extensions.handoff_prompt.RECOMMENDED_PROMPT_PREFIX`.

So the SDK gives both ends of the spectrum in one primitive: `input_type` is the typed contract (structured fields only), `input_filter` decides how much raw trace rides along, and the default is Cognition-style full-trace transfer.

---

## 6. Cross-referencing decision records

### 6a. Nygard's original ADR post
Source: Michael Nygard, "Documenting Architecture Decisions," https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions

Problem statement: "One of the hardest things to track during the life of a project is the motivation behind certain decisions" — new arrivals either blindly accept or blindly change decisions they don't understand.

Sections: **Title** ("short noun phrases", e.g. "ADR 1: Deployment on Ruby on Rails 3.0.10"); **Context** — "describes the forces at play, including technological, political, social, and project local"; **Decision** — "describes our response to these forces. It is stated in full sentences, with active voice"; **Status** — proposed / accepted / deprecated / superseded; **Consequences** — "describes the resulting context, after applying the decision. All consequences should be listed here."

Immutability and cross-reference: "ADR numbers will not be reused." When a decision changes, "we will keep the old one around, but mark it as superseded," so the record shows it "is *no longer* the decision." Rationale: "The motivation behind previous decisions is visible for everyone, present and future. Nobody is left scratching their heads to understand, 'What were they thinking?'"

### 6b. MADR
Source: https://adr.github.io/madr/

YAML front-matter: `status` (e.g. "proposed | rejected | accepted | deprecated | **superseded by ADR-0123**"), `date` ("when the decision was last updated"), `decision-makers`, `consulted` ("everyone whose opinions are sought (typically subject-matter experts); and with whom there is a two-way communication"), `informed` ("everyone who is kept up-to-date on progress; and with whom there is a one-way communication").

Sections: Context and Problem Statement; Decision Drivers; Considered Options; Decision Outcome; Consequences; **Confirmation** (how compliance with the decision is validated); Pros and Cons of the Options ("Good, because" / "Bad, because" / "Neutral, because"); **More Information** (where links to related and superseding ADRs live).

The `consulted` / `informed` fields are the notable bit for a two-team handoff: MADR's front-matter already types *which other function was in the loop* on a decision, one-way or two-way.

### 6c. adr.github.io generally
Source: https://adr.github.io/

"An Architectural Decision Record captures a single AD and its rationale; Put it simply, ADR can help you understand the reasons for a chosen architectural decision, along with its trade-offs and consequences." "The collection of ADRs created and maintained in a project constitute its *decision log*." The site frames ADRs inside Architectural Knowledge Management (AKM) and states an aim to "Strengthen the tooling around ADRs, in support of agile practices."

---

## 5. Organizational precedents (in progress)

### 5a. Amazon Working Backwards / PR-FAQ
Source: https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes

"Working Backwards is a systematic way to vet ideas and create new products. Its key tenet is to start by defining the customer experience, then iteratively work backwards from that point until the team achieves clarity of thought around what to build."

Form: the PR/FAQ. Press release "a few paragraphs, always less than one page"; FAQ "five pages or less." The PR must answer "Why will this new product be compelling enough for customers to take action and buy it?" The FAQ carries "all the salient details of the customer experience as well as a clear-eyed and thorough assessment of how expensive and challenging it will be."

Iteration and gate behavior: teams "write ten drafts of the PR/FAQ or more, and to meet with their senior leaders five times or more to iterate, debate, and refine the idea," and "most PR/FAQs never made it to a stage where they were launched as actual products" — i.e. the artifact's primary job is to be *rejected cheaply*, and only survivors cross into build.

*(more to append: SVPG discovery/delivery, Google design docs, Uber/Stripe RFC practice, Cole Medin / Factory Missions)*

---

## 7. SVPG — the discovery/delivery boundary

### 7a. "Discovery vs. Delivery"
Source: https://www.svpg.com/discovery-vs-delivery/

Two simultaneous challenges, not two sequential phases.

- **Discovery** = determining "what the customer solution needs to be," including validating demand and developing a solution that works for multiple customers rather than producing "a series of specials." Optimized for **speed of learning**.
- **Delivery** = ensuring "a robust and scalable implementation that our customers can depend on for consistently reliable value," where the team "can release with confidence." Optimized for **reliability**.

**The artifact that marks the boundary is "production-quality software."** SVPG's definition of production-quality: scalable and performant, carrying "a strong suite of regression tests," and "instrumented to collect the necessary analytics." Discovery deliberately operates *below* that bar — opt-in customer testing and **live-data prototypes** that bypass production standards precisely so they can be thrown away.

**What crosses, and in what form:** not a spec. Once discovery has evidence, "engineers ... build the 'production-quality' software as they see fit" — i.e. the *solution shape plus the evidence* crosses down, and the implementation decision stays on the delivery side.

**Stated failure mode:** wasting engineering effort building production-quality software for an unvalidated solution. The stated purpose of discovery is "to make sure we have some evidence that when we ask the engineers to build production-quality software, it won't be a wasted effort." Secondary failure named: MVP confusion — releasing a discovery-grade artifact to production, where "people feel like this ... is an embarrassment to the brand."

### 7b. "The Product Operating Model: An Introduction"
Source: https://www.svpg.com/the-product-operating-model-an-introduction/

The canonical statement of what crosses the boundary:

> "Product teams working in the product model are assigned problems to solve and desired outcomes to achieve, instead of being given a list of features to build."

Principles named: **Empowerment** — "teams are given problems to solve and empowered with finding the best solution"; **Outcomes over Output** — "teams exist to solve problems for the customer and the business, not to ship features."

**The four-dimension acceptance test** the receiving team must satisfy (this is the closest thing SVPG has to a typed schema on the deliverable):
- *Valuable* — customers will buy or use it
- *Usable* — users can figure out how to operate it
- *Feasible* — engineers can solve it with available resources (technology, skills, time)
- *Viable* — works within business constraints (marketing, sales, finance, legal)

Note: valuable/usable are discovery-side obligations; feasible is the engineering side's contribution back *up*; viable is the business side's. So the risk-clearing is explicitly split across functions rather than owned by the framing side alone.

**Failure modes:** this page does not name the alternative model's failure modes directly. Its only framing is that "Disruptive innovation has occurred in virtually every industry causing companies to realize that old ways of working are not enabling them to compete."

---

## 8. Engineering design docs / RFCs / RFDs

### 8a. Design Docs at Google (Malte Ubl)
Source: https://www.industrialempathy.com/posts/design-docs-at-google/

"Relatively informal documents that the primary author or authors of a software system or application create **before they embark on the coding project**."

**Named sections (the schema):**
1. **Context and scope** — "gives the reader a very rough overview of the landscape in which the new system is being built"
2. **Goals and non-goals** — "A short list of bullet points of what the goals of the system are, and, sometimes more importantly, what non-goals are"
3. **The actual design** — "start with an overview and then go into details": system-context diagram, APIs, data storage, code and pseudo-code
4. **Alternatives considered** — "lists alternative designs that would have reasonably achieved similar outcomes"
5. **Cross-cutting concerns** — security, privacy, observability

**Length:** "The sweet spot for a larger project seems to be around 10-20ish pages"; mini design docs of 1-3 pages for incremental work.

**Review:** three modes described — lightweight (send to the wider team list, discuss in comments); formal design review meetings where the author presents "to an often very senior engineering audience"; and Google's historical model of a single central mailing list where senior engineers reviewed at leisure.

**Upstream link is explicitly weak.** The doc "is not a requirements doc" and the article does not specify how it binds to upstream product decisions. **Downstream:** "It is strongly recommended to update the design doc" when the design changes during implementation — with the acknowledgement that this rarely happens.

**Stated anti-patterns:**
- Skip the doc entirely when it would just say "This is how we are going to implement it" "without going into trade-offs, alternatives, and explaining decision making" — in that case "it would probably have been a better idea to write the actual program right away."
- Implementation-manual docs (step-by-step instructions with no trade-off exploration) carry no value.
- Drift: "design docs, like all documentation, tend to get out of sync with reality over time."

### 8b. Oxide RFDs (RFD 1, "Requests for Discussion")
Source: https://rfd.shared.oxide.computer/rfd/0001

**Metadata fields:** `authors` (names + emails of the RFD owners), `state`, `discussion` (link to the pull request, for RFDs in discussion or beyond), `labels` (comma-separated categories, e.g. control-plane, hardware, process).

**Content expectations:** document the viable options with benefits and drawbacks, reasoning supported by data and references, and the ultimate determination. For technical decisions authors are asked to weigh economic implications, customer outcomes, performance, and security trade-offs.

**State machine (6 states):** `prediscussion` (WIP, actively iterating) → `ideation` (topic described, no active revision expected) → `discussion` (under active review in a PR) → `published` (merged and finalized, updates still possible) → `committed` (implemented; established consensus) — plus `abandoned` (non-viable or deliberately not implemented).

**Scope — when an RFD is required:** company processes or changes to them; architectural or design decisions for hardware or software; customer-facing API or CLI changes; internal API or tool changes; testing design. "RFDs not only apply to technical ideas but overall company ideas and processes as well."

**Numbering and cross-reference:** sequential, zero-padded (0042). Stable short URLs — `{num}.rfd.oxide.computer`, `rfd.oxide.computer/{num}`, and `{num}.rfd.oxide.computer/discussion` for the thread. RFDs cite each other by number (`[rfd5]`, `[rfd21]`).

**Mechanism:** branch named for the RFD number → iterate in `prediscussion` → flip to `discussion` and open a PR (a bot opens it for you if you forget) → 3–5 business days for feedback → merge to master, state becomes `published`.

**Rationale (from the IETF RFC lineage):** "writing down ideas is important: it allows them to be rigorously formulated (even while nascent), candidly discussed and transparently shared."

*Note the structural contrast with Google design docs: Oxide types the document's lifecycle state and gives every document a permanent addressable number, so a later document can cite an earlier decision by ID — the same immutable-ID + supersession property Nygard's ADRs have. Google's design doc has neither a state field nor a canonical ID, and the article concedes the drift that follows.*

---

## 9. Contract-first spawning (agent teams)

Source: Anthropic, Claude Code agent-teams docs, https://code.claude.com/docs/en/agent-teams — plus secondary coverage of Cole Medin's walkthrough (https://www.geeky-gadgets.com/claude-code-agent-teams/).

Secondary-source summary pending primary confirmation (see below): agent teams differ from subagents in that **teammates communicate directly with each other** rather than only with a coordinator, and **contract-first spawning** means defining the interface/dependency contract between agents *before* they begin work, to reduce conflicts in parallel execution. Cole Medin's demonstration builds a payment integration across DB, frontend, and backend-token lanes in parallel.

*(Primary-source detail appended below.)*

*Primary-source confirmation of the Claude Code agent-teams page was not completed: two subagents stalled. The contract-first idea is corroborated by the Systemcraft bench-composition brief (2026-08-22), which recorded Cole Medin's "contract-first spawning" and Factory's "Missions" pattern (serial features, parallel read-only ops) from primary video sources.*

---

## 10. Closing table — every pattern, side by side

Compiled by the session driver from sections 1–9. "Direction" is from the framing side (the team that names the problem) to the delivering side (the team that designs and proves), unless stated.

| Pattern | What crosses | Direction | Form (fields / schema) | Back-reference mechanism | Reported failure modes | Source |
|---|---|---|---|---|---|---|
| **A2A (Google)** | Down: a Message (text / file / structured parts) under a `contextId`. Up: a Task with a typed `status.state`, durable `artifacts`, optional `history` | Both, asynchronous; the delivering agent is opaque (no reasoning or memory crosses) | Agent Card (capabilities, skills, security); Task {id, contextId, status, artifacts, history, metadata}; nine typed states incl. `REJECTED`, `INPUT_REQUIRED` | `contextId` groups tasks; `referenceTaskIds` on messages; `ListTasks` enumerates everything done under a context | Version/capability mismatch; the client never sees why the server decided what it did | a2a-protocol.org/latest/specification |
| **MCP boundary** | A declaration of what each side can be asked for, negotiated once and pinned per session | Both, at initialization | `initialize` with `protocolVersion`, `capabilities` (roots/sampling/elicitation vs prompts/resources/tools/logging), `serverInfo`, optional `instructions` | Protocol version header on every request; capabilities must be re-negotiated on change | Version mismatch (`-32602`), unnegotiated capability use, timeouts without cancellation | modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle |
| **Cognition, single-thread** | Everything: full agent traces, not summaries | One continuous context; against handoffs | A linear agent plus an LLM history compressor when context overflows | None needed: one memory | Implicit decisions conflicting across parallel agents; dispersed decision-making; task misread from missing context | cognition.com/blog/dont-build-multi-agents |
| **Anthropic orchestrator-worker** | Down: objective, output format, tool/source guidance, task boundaries. Up: findings; large outputs persisted externally with lightweight references passed back | Down then up; a separate CitationAgent adds provenance after synthesis | Structured task description (four elements); plan saved to memory before delegation | Reference-not-payload: artifacts stored outside the coordinator, cited by reference; CitationAgent binds claims to sources | Thin task descriptions → duplicated work and gaps; over-spawning; endless search; agents distracting each other; 15× token cost; small failures compound | anthropic.com/engineering/multi-agent-research-system |
| **OpenAI Agents SDK `handoff()`** | A typed payload (`input_type` schema) plus as much prior history as the `input_filter` allows (default: all of it) | One-way transfer of the conversation to the receiving agent | `handoff(agent, input_type, input_filter, on_handoff, is_enabled, nest_handoff_history)`; surfaced to the model as a `transfer_to_<agent>` tool | `on_handoff` callback is the logging point; `HandoffInputData` carries `pre_handoff_items` and `new_items` | Unfiltered history leaks tool noise; filtered history loses context — the SDK ships both ends and leaves the choice to the designer | openai.github.io/openai-agents-python/handoffs |
| **Amazon PR/FAQ** | A one-page press release plus a ≤5-page FAQ: customer experience, cost and difficulty | From product framing into build; most PR/FAQs are meant to die before crossing | PR ("why compelling enough to buy") + FAQ ("salient details… clear-eyed assessment of how expensive and challenging") | Iteration record: ten-plus drafts, five-plus senior reviews before a build decision | Building before the document survives review; the artifact's job is cheap rejection | aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes |
| **SVPG discovery → delivery** | Problems to solve and outcomes to achieve, with discovery evidence and a validated solution shape; never a feature list or spec | Down; feasibility flows back up from engineering, viability from the business | The four-risk acceptance test (valuable, usable, feasible, viable) split across functions; "production-quality" (scalable, tested, instrumented) marks the delivery side | Continuous: discovery and delivery run simultaneously on one team, so the reference is shared context, not a document | Building production-quality software for an unvalidated solution; shipping a discovery-grade prototype as an MVP | svpg.com/discovery-vs-delivery; svpg.com/the-product-operating-model-an-introduction |
| **Google design docs** | A 10–20 page design with context and scope, goals and non-goals, the design, alternatives considered, cross-cutting concerns | From engineering author to reviewers, before coding; upstream link to product decisions explicitly weak ("not a requirements doc") | Five named sections; three review modes | Update-on-change recommended and acknowledged to rarely happen | Docs that restate the implementation with no trade-offs; drift from reality | industrialempathy.com/posts/design-docs-at-google |
| **Oxide RFDs** | Options with benefits and drawbacks, data, and the determination, for any decision (technical or process) | Author to the company, via PR review | Metadata `authors`, `state`, `discussion`, `labels`; six-state lifecycle (prediscussion → ideation → discussion → published → committed, or abandoned); sequential zero-padded numbers with stable URLs | RFDs cite each other by number; a permanent addressable ID per decision | Not stated on RFD 1; the structure exists to prevent Google-style drift | rfd.shared.oxide.computer/rfd/0001 |
| **ADRs (Nygard) / MADR** | One architectural decision with context, decision, status, consequences | Written by the deciding team; read by everyone later | Nygard: title, context, decision, status, consequences; MADR adds `decision-makers`, `consulted` (two-way), `informed` (one-way), Confirmation, More Information (links to related and superseding ADRs) | Numbers never reused; superseded entries kept and marked; MADR front-matter types which other function was consulted or informed | "What were they thinking?" when rationale is lost; unrecorded supersession | cognitect.com (Nygard); adr.github.io/madr |
| **Contract-first spawning (agent teams)** | An interface/dependency contract agreed before parallel work starts | Peer to peer among teammates, not only via a coordinator | Contract defined up front; lanes work in parallel against it | The contract is the shared reference; conflicts are caught against it | Parallel lanes conflicting when the contract is thin (Medin); serial features with parallel read-only ops as the safe shape (Factory) | Systemcraft bench brief 2026-08-22 (primary videos); code.claude.com/docs/en/agent-teams (not re-fetched) |

## What the table shows, as facts

- Every protocol that keeps memories separate (A2A, MCP, Anthropic's workers) crosses **typed artifacts and references, never reasoning**; the one voice against separation (Cognition) argues the price is implicit-decision conflict and prescribes full-trace sharing instead. OpenAI's primitive sits between them: a typed payload plus a filterable history.
- Every organizational precedent that survives drift gives each decision a **permanent id and a lifecycle state** (Oxide RFDs, ADRs, MADR's supersession), and the one that doesn't (Google design docs) reports the drift.
- SVPG and Amazon both cross **problem plus evidence**, not solution specs, and both put the acceptance test on the receiving side.
- MADR is the only pattern found that **types the other function's role in a decision** (`consulted` vs `informed`), which is the closest published shape to a cross-studio back-reference.
