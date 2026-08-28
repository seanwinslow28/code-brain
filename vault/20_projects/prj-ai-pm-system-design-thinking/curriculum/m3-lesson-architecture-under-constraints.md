---
title: "M3 — Architecture Under Constraints"
type: lesson
module: M3
status: ready
created: 2026-08-22
anchor: Claude Code's leaked source — the 12 infrastructure primitives
backup_anchor: Perplexity's retrieval architecture
mirror_eligibility: "strongest — most of this exists in his fleet, unnamed"
---

# M3 — Architecture Under Constraints

*Module 3 of 5 · AI PM System Design Thinking · Weeks 4–5*

---

## 0. This is the module where you already know most of it

M2 was mostly new. This one is mostly naming.

You have built, by instinct, most of the infrastructure that makes an AI system survive contact with production. Here is the map — your code on the left, the name it has in the literature on the right. **Read this table slowly. It is the single highest-value page in the curriculum for you**, because every row is something you can already defend from experience and could not previously call by name.

| What you built | What it is called |
|---|---|
| `fallback = "none"` on the Tier C route, so an off-hours miss raises `RouteUnavailable` instead of quietly billing the paid API | **Fail-closed degradation policy.** You chose cost-safety over availability. That is an explicit SLO trade-off |
| The synthesizer tripping to `partial` when it loses its host mid-run | **Circuit breaker** |
| `wol-deferred` — a typed manifest, exit 0, work self-re-queues, instead of the old poll storm | **Graceful degradation with idempotent retry** |
| `RouteUnavailable`, `partial`, `wol-deferred`, `rejected_reasons` | **A stop-reason taxonomy.** Every way a run can end has a name — most systems have exactly two, "worked" and "threw" |
| `check_caps` computing `mtd + predicted` and refusing *before* the API call | **Pre-flight budget check.** The distinction between projecting and merely observing is the whole value |
| `$7/task, $20/day, $50/month` | **Hierarchical rate limiting / cost guardrails** |
| `evaluate_article_depth()` emitting `rejected_reasons` into the manifest | **Quality gate with observable rejection telemetry** |
| The discovery council dropping any claim not traceable to a fetched URL | **Grounding verification gate** |
| `disallowedTools` deny-lists on your read-only agents | **Capability restriction by trust tier** |
| PreToolUse hooks that exit 2 to deny | **A policy enforcement point** — a hard gate that runs before the action, not a request in a prompt |
| The health ledgers and nightly manifests | **System event logging**, separate from the conversation |
| launchd plists carrying an explicit `PATH` | **Environment guards in a staged boot sequence** |

Twelve rows. You designed all of them because something broke and you fixed it, which is a completely legitimate way to arrive at good architecture and a completely useless way to talk about it in an interview.

**What you have NOT built, and this module teaches from zero:**

- **A tool registry** — a data structure that answers *what capabilities exist and what do they do* without executing anything. Your skills are close; a registry is stricter.
- **Session persistence and resumability.** Your agents are one-shot scheduled runs. When one dies, the run dies. Nothing reconstructs mid-task state.
- **Workflow state as distinct from conversation state.** Related to the above and worth its own section.
- **Any threat modelling at all.** You run tool-calling agents with filesystem and network access, and connected MCP servers. You have never asked what an attacker could make them do. §6 is the uncomfortable one.

---

## 1. The first architecture decision: workflow or agent?

Before any of the plumbing, the fork that determines everything downstream.

Anthropic's engineering team — the people who build Claude and Claude Code — published a piece called *Building Effective Agents* that draws the line more usefully than most:

- A **workflow** is a system where the model and its tools are orchestrated through **predefined code paths**. You decided the steps. The model fills in the parts that need language or judgment.
- An **agent** is a system where the model **dynamically directs its own process** — choosing which tools to use and in what order, deciding when it is done.

The distinction is not sophistication. It is **who chose the sequence**: you, in advance, or the model, at runtime.

Their recommendation is more conservative than the market's, and it is the one to carry into a room:

> **Workflows beat agents whenever the task's structure is stable enough to encode in code**, because a workflow pays the inference cost only at decision points *you* chose. Start simple. Add agency only when flexibility genuinely outweighs latency, cost, and compounding error.

They name five workflow patterns that cover most real cases before autonomy is warranted:

1. **Prompt chaining** — decompose into fixed steps, each feeding the next. Add a programmatic check between steps and you have a gate.
2. **Routing** — classify the input, send it down a specialised path. *You built this.* Your HybridRouter is a router with a cost-aware policy.
3. **Parallelisation** — run subtasks simultaneously and aggregate, either by splitting the work or by running the same task several times for a vote.
4. **Orchestrator–worker** — a central model breaks the task down and delegates to workers. Differs from parallelisation because the subtasks aren't known in advance.
5. **Evaluator–optimiser** — one model produces, another critiques, loop until it passes. *You built this too.* Your nightly critic is an evaluator over the synthesizer's output.

**The reason each has "kill criteria"** — conditions under which you'd abandon the approach — is that the failure of an agent is not like the failure of a workflow. A workflow fails at a step you can name. An agent fails by taking nineteen steps you didn't anticipate, each individually reasonable, arriving somewhere expensive. **Error compounds along the chain**: a per-step reliability of 95% over ten independent steps is about 60% end-to-end.

That is the whole argument, and it is arithmetic rather than opinion.

### The retrieval fork

The same "what do you actually need" discipline applies to how a system gets its knowledge:

- **Retrieval (RAG)** — look things up at answer time. Best when the knowledge changes, must be cited, or is too large to hold. Costs a retrieval hop and every failure mode in M2's taxonomy.
- **Long context** — put everything in the prompt. Simplest, and it degrades: systems attend to the beginning and end and skim the middle, and cost scales with every token every time.
- **Fine-tuning** — train the model on your data. Changes *behaviour and form* reliably; it is a poor way to install *facts*, which go stale and cannot be cited.

**The crisp version, worth being able to say:** retrieval is for knowledge that changes, fine-tuning is for behaviour that should be consistent, and long context is for when the problem is small enough that you should stop optimising.

---

## 2. The harness, and the 80% nobody tutorialises

In 2026, Anthropic accidentally published the full source of Claude Code — roughly 1,900 files, over 500,000 lines, in an npm package that failed to exclude a source map. Analysis of it produced the most complete public picture of what production agentic infrastructure actually contains.

The headline finding: **the model call is roughly 20% of the system. The other 80% is plumbing** — session persistence, permission pipelines, context budget management, tool registries, error recovery. The boring machinery that separates a demo from something millions of people depend on.

The primitives, in the order you should build them, not the order they appear in the source:

**Day one, non-negotiable:**

- **Tool registry, metadata first.** Define capabilities as data before writing implementation. A `listTools()` that returns what exists without invoking anything. Each entry carries name, description, required permissions, input schema, and side-effect profile. Without it you cannot filter tools by context, cannot introspect without triggering side effects, and every new tool edits orchestration code.
- **Permission system with trust tiers.** Not all tools carry equal risk. Claude Code's shell-execution tool alone runs an **18-module security stack** — pre-approved patterns, destructive-command detection, git-specific checks, sandbox determination — each able to independently block. *Defense in depth: different layers catch different failures.*
- **Session persistence that survives crashes.** The session is more than the transcript: it is conversation plus usage counters plus permission decisions plus configuration. If any is missing on resume, the session behaves differently than the original.
- **Workflow state, and idempotency.** See §3.
- **Pre-turn token budget checks.** Check *before* the expensive call, not after. *You built this in `check_caps`.*
- **Structured streaming events.** Typed events, not text chunks — which tool is being considered, what was denied, why the stream ended.
- **System event logging**, separate from the conversation. The transcript says what was *said*; the log says what the system *did*.
- **A basic verification harness.** A handful of invariant tests: destructive tools always require approval, denied tools never execute, structured outputs validate against schema, budget exhaustion stops gracefully. Run them whenever prompts, models, tools, or routing change. **This is much cheaper and much earlier than a golden dataset** — it is the day-one version of what M5 industrialises.

**Week one:** tool pool assembly (not every conversation needs every tool), transcript compaction, a permission audit trail, a `/doctor` health check, a staged boot sequence, a stop-reason taxonomy, and **provenance-aware context assembly** — see §6, because it is a security control disguised as a data-quality feature.

**Month one:** agent type system, memory with provenance, extensibility.

**The governing principle, and the one most likely to save you five weeks:**

> The common mistake is not under-engineering. It is **over-engineering — building multi-agent coordination before the permission system works.** Premature complexity is where most agent projects die.

### The anecdote to remember

Claude Code's automatic context-compaction routine retried **indefinitely** on failure. One session failed 3,272 consecutive times, silently burning tokens while the user wondered where their limits went. The fix was three lines — a maximum-consecutive-failures constant.

**Three lines of budget guardrail, missing from a product doing billions in revenue.** Hold that next to your own `check_caps`, which projects the spend and refuses before the call. You got that right and they didn't, and until today you didn't have a name for what you'd done.

*(Source-honesty note: this analysis is of leaked source, read by a third party. Treat the architecture as strong evidence and any specific claim about intent as inference. Say which is which.)*

---

## 3. Workflow state is not conversation state

The distinction almost every framework conflates, and the one most likely to come up when someone technical is probing you.

**Conversation state** answers *what have we said?* It is the transcript.

**Workflow state** answers *what step are we in, what side effects have already happened, is this operation safe to retry, and what should happen after a restart?*

They are different problems. Restoring a transcript does not tell you whether the email was already sent.

**Idempotency** is the property that doing something twice has the same effect as doing it once. Reading is naturally idempotent; charging a card is not. The standard mechanism is an **idempotency key** — a unique identifier attached to a mutating operation so the receiver can recognise a repeat and decline to act twice.

Without this, a crash mid-execution means a retry might double-send, double-charge, or re-run something expensive. **Your `wol-deferred` design already gets this right**: the work re-queues rather than fires blindly, and the manifest records that it deferred rather than failed. What you don't have is resumability *within* a run — if your synthesizer dies at step 7 of 10, nothing picks up at 8.

Model long-running work as explicit named states — `planned`, `awaiting_approval`, `executing`, `waiting_on_external`, `completed`, `failed` — and checkpoint after every side-effecting step.

---

## 4. The determinism boundary

The most PM-specifiable decision in the entire stack, and the one most often left to whoever writes the code.

For every part of your system, decide: **is this enforced in code, or requested in a prompt?**

Models do not count reliably. They do not "feel" layout. They approximate. Asking nicely for a 412-character limit produces a number near 412. Counting it in code produces 412.

Three moves that follow:

**Constraints live in code.** Generate, then *count in code*, flag the exact overage, repair only what is allowed to move, validate again.

**Frozen versus variable.** Mark explicitly what the model may not touch — the legal disclaimer, the citation format, the figure that came from the source system — and what it may. Without the line, you are trusting the model to infer what matters. It will paraphrase your disclaimer because it judged the paraphrase clearer.

**Validate after every transformation, not just at the end.** This is the non-obvious one. It is easy to build a loop that checks a constraint after drafting. It breaks the moment you add a step — a model can draft inside the limit and then violate it during a tone pass, because the check ran at the end and the damage happened in the middle.

The loop, worth memorising: **generate → validate → repair → validate again.** Repair with specifics — *"output is 847 characters, limit is 412, cut 435 while preserving the core claim"* — not "try again."

---

## 5. The debt that accrues while nothing is broken

In 2015 a team at Google led by D. Sculley published *Hidden Technical Debt in Machine Learning Systems*, the paper that established ML systems as a systems problem rather than a modelling problem. It is still the most-cited thing in the field and every term in it is worth owning:

- **CACE — Changing Anything Changes Everything.** No input to a trained system is truly independent; change one and the behaviour of all of them shifts. This is why "just add a feature" is never just adding a feature.
- **Glue code.** The supporting code written to move data into and out of general-purpose packages. The paper measures it at **95% or more of a mature ML codebase.**
- **Pipeline jungles.** Data preparation that grew organically into a thicket of scrapes, joins, and sampling steps nobody can fully trace.
- **Undeclared consumers.** Someone downstream is depending on your output and you don't know they exist. You cannot change anything safely, because you cannot enumerate who breaks.
- **Boundary erosion, entanglement, configuration debt, hidden feedback loops.**

A 2026 line of work extends this to agentic systems with a distinction worth stealing whole: **agentic technical debt is a stock, and the stochastic tax is a flow.** Debt is accumulated design liability. The tax is the ongoing operating burden a probabilistic system imposes **even when nothing is broken and everything is governed well** — because runs vary, tools fail, and adoption keeps surfacing new edge cases. *(Fresh scholarship, 2026 preprint, so date it when you say it.)*

That is your fleet, described: the nightly critic, the lint job, the health ledger. Nobody makes you run those for a bash script.

---

## 6. Security, and the section you should read twice

You run tool-calling agents with filesystem and network access and connected MCP servers. This section is the one with no mirror.

Microsoft's AI Red Team published a *Taxonomy of Failure Modes in Agentic AI Systems*, updated in 2026 on the back of twelve months of red-teaming **deployed** systems. Its core message is that agents face attacks with no analogue in ordinary software security.

**The classical frame** is STRIDE — Microsoft's threat-modelling checklist (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) applied to a diagram of how data flows across trust boundaries. Still the durable name to know.

**The AI-specific additions** — currently being formalised under names like ASTRIDE and STRIDE-AI, both 2025–26 and **not yet settled**, which is itself worth saying out loud:

- **Prompt injection.** Hidden instructions in content the agent reads become instructions the agent follows. The attack surface is *anything the model ingests*: a web page, a document, a ticket, a retrieved chunk.
- **Memory / context poisoning.** Corrupt what the agent remembers and you change decisions it makes later, long after the injection. Which is why **provenance-aware context assembly is a security control**: *"memory without provenance becomes accumulated hallucination,"* and instruction-like text in retrieved context silently becomes a new system prompt.
- **Goal hijacking.** Instructions planted early in a multi-step session redirect the terminal goal. Because they're distributed across steps and memory lookups, they routinely bypass controls applied to individual interactions.
- **Unsafe tool use.** The agent is manipulated into misusing permissions it legitimately holds.
- **Inter-agent trust escalation.** A compromised sub-agent asserts false permissions to an orchestrator that acts without verifying.

One number to hold: **MCP became the de facto standard for connecting models to tools, and drew 99 published CVEs in 2025.** You run MCP servers.

**The PM move here is not to become a security engineer.** It is to ask, in the design review, the three questions nobody asks: *what does this agent read that an outsider can write to? what can it do that we could not undo? and what would we see if it were doing something wrong right now?*

---

## 7. Vocabulary, compressed

**Workflow vs agent · prompt chaining · routing · parallelisation · orchestrator–worker · evaluator–optimiser · compounding error · RAG vs fine-tune vs long context · harness · tool registry · trust tiers · defense in depth · policy enforcement point · session persistence · workflow state · idempotency key · stop-reason taxonomy · pre-flight budget check · determinism boundary · frozen vs variable · generate-validate-repair-validate · CACE · glue code · pipeline jungle · undeclared consumers · agentic debt (stock) vs stochastic tax (flow) · STRIDE · prompt injection · context poisoning · goal hijacking · provenance-aware context**

---

## Exercises

**How these run:** I work one fully out loud first, saying why at each step; then you take one of the same shape with me available throughout. No cold start, no prediction, no score.

### Exercise A — The mirror, run properly *(this is the one to do first)*

Take three of your own agents — `vault_synthesizer`, `job_feed`, and `daily_driver` are the natural picks — and produce the **primitive audit**: for each of the twelve day-one and week-one primitives, is it present, partial, or absent, and what is the evidence in the code?

This is not busywork. It produces three things at once: the vocabulary attached to systems you can already defend, a genuine gap list for your own fleet, and **a portfolio artifact** — a real architecture audit of a real system, which is exactly what Grok said an AI PM portfolio should contain.

I'll do `vault_synthesizer` out loud. You take `job_feed`.

### Exercise B — Forward design from a dirty brief

> A legal-services company wants an assistant that answers questions about a client's own uploaded contracts. Roughly 40,000 documents, mostly PDFs, many scanned. Answers must cite the clause they came from. Two engineers, one quarter. Clients are on separate accounts and must never see each other's documents. Legal has asked what happens when it cites a clause that isn't there.
>
> **Design it.**

Produce: workflow or agent, and why, with the kill criteria that would flip your choice; retrieval versus long context versus fine-tuning; where the determinism boundary sits and what's frozen; the tenancy/permission model; three failure modes from M2's taxonomy that this design specifically invites, and your mitigation for each; the stop-reason taxonomy; and **at least two architectures you rejected, with why.**

**Constraint shift, walked the first time:** partway through I'll change something — the scanned PDFs turn out to be 60% of the corpus, or a client asks for on-premise deployment — and we'll re-derive together before you do one alone.

### The written artifact

**An architecture decision record** — the design, the alternatives you rejected, the kill criteria for each, and the systems concept applied by name. Roughly two pages.

This becomes **Golden Loop's systems map input.** The Phase D gate requires a systems map before the PRD; this is where it starts.

---

## Sources for this module

| Source | Tier | What it's for |
|---|---|---|
| [Anthropic — *Building Effective Agents*](https://www.anthropic.com/engineering/building-effective-agents) | **B** primary | The workflow/agent fork and the five patterns |
| [Sculley et al., *Hidden Technical Debt in ML Systems*](https://papers.neurips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf) (NeurIPS 2015) | **A** peer-reviewed | CACE, glue code, pipeline jungles, undeclared consumers |
| [Microsoft — *Taxonomy of Failure Modes in Agentic AI Systems v2.0*](https://www.microsoft.com/en-us/security/blog/2026/06/04/updating-taxonomy-failure-modes-agentic-ai-systems-year-red-teaming-taught-us/) | **B** primary | The security section, grounded in twelve months of red-teaming deployed systems |
| [When to Build Your Own Agent Harness — Harrison Chase, LangChain](https://youtu.be/HI2q3ci3Iuc) *(in notebook)* | **B** primary | Build-vs-buy on the harness itself |
| [RAG failure taxonomy](https://aclanthology.org/2026.trustnlp-main.27.pdf) (ACL TrustNLP 2026) | **A** peer-reviewed | Carried from M2 — the retrieval failure modes this module designs against |

**Honesty notes.** The Claude Code primitives come from third-party analysis of leaked source: strong evidence about architecture, inference about intent. The agentic-security frameworks (ASTRIDE, STRIDE-AI) are 2025–26 and competing; STRIDE itself is the settled part. Say which is which — naming where the ground is firm and where it isn't reads as senior, not hedging.

**Ask me anything.** §6 especially — it is the part of your own fleet you have never looked at through this lens.
