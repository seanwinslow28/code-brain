---
title: "Software-factory literature synthesis — 2026-08 delta round (agentic-web sprint)"
date: 2026-08-29
project: agentic-web-startup
type: literature-review
status: final
tags: [agentic-web, software-factory, orchestration, evals, research-sprint]
---

# Software-factory literature synthesis — delta round

Sprint item 1 per the
[kickoff](../../../docs/prompts/2026-08-29-agentic-web-research-sprint-kickoff.md).
**This is a delta round, not a fresh review:** the
[2026-08-08 literature review](2026-08-08-software-factory-literature-review.md) already
synthesized the four first-party blogs plus the notebook's then-22 sources; its findings
stand. This round covers what changed since — 36 sources Sean added to the NotebookLM
notebook after 8/08, three weeks of new published writing (including Uber's "software
factory" post and the Ramp Pragmatic Engineer deep-dive, both from this week), and the
independent-practitioner corpus the 8/08 round never swept. Product-agnostic throughout:
nothing here assumes which territory wins on Sept 1.

## Method

Same three-track shape as 8/08, evidence mirrored in
[2026-08-29-software-factory-lit-delta/](2026-08-29-software-factory-lit-delta/):

- **Track A — NotebookLM corpus** (now 57 sources; 36 added post-8/08). Two
  citation-backed cross-corpus queries succeeded (`notebooklm-q3-evals.md`,
  `notebooklm-q4-models-cost.md`); the other two ratified queries hit a hard client-side
  50MB RPC cap on this notebook regardless of source scoping (tooling lesson recorded
  below), so their ground was covered instead by dumping **14 fulltext transcripts**
  (`transcripts/`, ~645KB) of the factory-core sources straight into Track C. $0.
- **Track B — web sweeps**: three parallel research agents read 31 primary pieces —
  labs (`sweep-labs.md`), production companies (`sweep-companies.md`), independent
  practitioners (`sweep-practitioners.md`) — every claim tagged practitioner vs vendor,
  with negative findings and unfetchable sources named. $0.
- **Track C — Codex synthesis** (per the kickoff): GPT-5.6 Codex read the 8/08 review
  plus all new evidence cold and wrote the cross-source delta synthesis
  (`codex-delta-synthesis.md`, reproduced verbatim below), which the orchestrator then
  spot-checked against the transcripts.

**Transcript caveat:** Track A fulltexts are auto-transcribed YouTube audio — names and
product terms are frequently mangled ("ChemK3", "Grock", "Nath Aston"-class errors).
Quotes from transcripts are verbatim *as transcribed*, not as spoken.

## Source inventory (delta highlights)

| Cluster | Anchors | Class |
|---|---|---|
| Production fleets (new this round) | Uber "Running a Software Factory Efficiently" (8/27), Shopify "Under the River", Ramp Inspect via Pragmatic Engineer (8/25), exe.dev six-months retro (8/27), Stripe Minions Pt 1+2 | practitioner |
| Labs (re-read + new) | OpenAI "Harness engineering" (~1M LOC, 0 hand-written), Anthropic demystifying-evals / multi-agent research / best-practices / tools / context | mixed |
| Independent operators | Huntley (Ralph loop), Ronacher (2 negative-results posts), Willison (×2), Klaassen (compound engineering), Cognition "Don't Build Multi-Agents", Hashimoto, Steinberger, Carson's ai-dev-tasks | practitioner, incl. negative results |
| Notebook talk corpus (post-8/08 adds) | Carson 15-agents, 250-agent hedge fund, Basis ×2 (long-horizon, ontologies+evals), Databricks production playbook, Sonar verifiers, Sakana memory harnesses, exe.dev sandboxes, Thariq/Anthropic, ontology-setup doc | practitioner talks (transcribed) |
| Not obtainable | Yegge original (403 everywhere — his cost figures stay uncited), Allie Miller "build the factory" in written form (does not exist; podcast-only), Vercel/Figma/Airbnb first-person fleet writing (none found) | gap |

## Synthesis (Codex, verbatim)

# Software-factory literature: 2026-08 delta synthesis

## 1. DELTA FINDINGS

1. **CONFIRMS—and makes operational—the 8/08 finding that the environment matters more than generation.** [practitioner] The new production accounts converge on a separable substrate: durable session/event state, a replaceable agent loop, isolated or disposable execution, deterministic nodes around model calls, curated tools, and inspectable artifacts. Stripe interleaves agent and deterministic blueprint nodes; Shopify explicitly separates durable session, cheap-to-recreate harness, and disposable sandbox; Ramp and exe.dev use remote isolated environments; OpenAI makes per-worktree apps, logs, metrics, and browser state legible to agents. This is more specific than the prior round's general call for durable state and sandboxes: the adoptable unit is the interface between state, execution, and evidence, not a monolithic "fleet platform." (sweep-companies.md §§1–2, 4, 6–7; sweep-labs.md §9)

2. **NEW: gate placement is a spectrum, not a consensus architecture.** [practitioner] Stripe uses lint, at most two CI rounds, and mandatory human merge review; Anthropic's internal guidance escalates from a prompt check to a completion-blocking Stop hook and fresh-context verifier; OpenAI instead uses hard architectural linters but "minimal blocking merge gates" after deciding that corrections are cheap at its throughput. The common invariant is not gate hardness at merge; it is that safety- and architecture-critical properties are mechanically hard somewhere, retries are bounded, and evidence survives for review. (sweep-companies.md §§1–2; sweep-labs.md §§3, 9)

3. **SHARPENS the 8/08 eval finding: mature evals are both release gates and production control loops.** [practitioner] Anthropic separates capability suites from near-100%-pass regression suites and says production monitoring catches misses; Uber combines real-PR review benchmarks with production revert rate, F1, MTTR, noise, and cost per outcome; a Databricks customer case runs deterministic, semantic, and behavioral checks on live traces, deflects low-quality cases to humans, and promotes incidents back into the offline set. Only Uber publishes this dual use in a first-party fleet account; most company accounts describe gates but no live eval monitors. (sweep-labs.md §5; sweep-companies.md §§1–7; notebooklm-q3-evals.md §§1–2; transcripts/53-databricks-playbook.md)

4. **NEW: long-horizon work needs trajectory evaluation, not only final-state grading.** [practitioner] Basis argues that a correct result reached through an unsupported or non-compliant path is not trustworthy and uses sparse BEHAVIOR.md contracts plus an agentic judge over the trajectory; Databricks separately checks duplicate or failing tool calls that outcome scoring would miss. [vendor] The accompanying ontology/setup analysis cautions that behavior specs are rubrics, not controls, and should enforce durable invariants rather than exact choreography; critical behavior still needs a tool, deterministic rule, runtime instruction, monitor, or escalation path. (transcripts/25-basis-long-horizon.md; transcripts/43-ontology-agent-setup.md §§"Behavior specs are not controls by themselves," "Process evals versus outcome evals"; notebooklm-q3-evals.md §§2–3)

5. **NEW: cost discipline is now described as an operating system, not merely model downgrading.** [practitioner] Uber decomposes spend into users × sessions × turns × requests × tokens × price, exposes live counters, catalogs 16 spend anti-patterns, uses caching and code-mode batching, and reports cost per 1,000 requests down almost 34% and cost per session down 52% from its June peak. Anthropic reports multi-agent research at about 15× chat tokens and says a model upgrade beat doubling its token budget; Sakana's local experiments show memory adds cost without capability when the task fits in context but ranked recall helps on long-horizon retrieval. (sweep-companies.md §3; sweep-labs.md §2; transcripts/36-memory-harnesses-sakana.md)

6. **CONFIRMS the 8/08 warning that human attention—not code generation—is the binding resource, and adds product judgment as a distinct non-verifiable gate.** [practitioner] The exe.dev operator's layered tests, agent review, CI, and screenshots still end with human judgment because "The tools could tell me that the change worked. They couldn't tell me whether it was worth adding to the system." Ryan Carson likewise says automatic product-improvement loops "don't work with product," limits attention to roughly four or five concurrent tasks despite 10–15 cloud threads, and grounds priorities in customer conversations and paper. (sweep-companies.md §7; transcripts/23-ryan-carson-15-agents.md)

7. **NEW—and in direct tension with the talk circuit: "fleet size" is not a stable operational measure.** [practitioner] Carson's talk is titled "15 AI agents," but his written workflow pauses for human approval after each subtask; his talk says he can track only four or five tasks. The "250+ agents" operator describes 10–20 active chats, about 150 scheduled automations, and roughly 100 research sessions across three machines; the "34-agent workforce" account is promotional, says its product factory remains heavily human-directed, and provides no written operating record. The largest numbers mix concurrent chats, cron jobs, subagents, and named roles, while receipt-bearing prose documents one loop, three agents, three-to-eight agents, or 16 sequential sessions. Count claims should not be used as capacity or economics evidence. (sweep-practitioners.md §§1, 6, 8–10, 12 and Cross-cutting synthesis §1; transcripts/23-ryan-carson-15-agents.md; transcripts/24-hedge-fund-250-agents.md; transcripts/39-agent-workforce-secrets.md)

8. **CONFIRMS—and strengthens with negative results—the single-agent default.** [practitioner] Ronacher found no gain from commands, hooks, or subagents and says non-parallel work became chaotic; Steinberger abandoned orchestrators, worktrees, subagents, most MCPs, and spec-heavy systems; Cognition reports parallel writers making incompatible implicit decisions; Huntley fans out search but serializes builds and tests. Parallelism earns its place for independent research, isolated proofs of concept, context isolation, or fresh review—not merely because work has several steps. (sweep-practitioners.md §§1–2, 4, 7, 10)

9. **SHARPENS the prior "repo as memory" finding into a world-model rule, while limiting its scope.** [practitioner] Basis treats canonical vocabulary, identity, authority, and current-versus-historical status as runtime infrastructure and says long-horizon agents must persist decisions and evidence for a future fresh context. [vendor] The setup analysis explicitly rejects "ontology astronautics": stable IDs, typed schemas, Markdown/YAML canon, and ordinary search may be enough until measured retrieval failures justify graphs or embeddings. Sakana independently finds recall policy—not the mere existence of a memory store—to be the useful unit of evaluation. (transcripts/25-basis-long-horizon.md; transcripts/41-basis-ontologies-evals.md; transcripts/43-ontology-agent-setup.md §§"Ontology & Context Framework," "Memory Framework"; transcripts/36-memory-harnesses-sakana.md)

10. **NEW: production factories expose a maintenance labor category beyond builder/reviewer.** [practitioner] OpenAI runs background "GC" and documentation-gardening agents; Anthropic describes an agent optimizing tool descriptions; Uber measures spend anti-patterns; solo operators mine blocked traces, simplify code, and convert incidents into tests or monitors. This confirms the prior need for trace review but shows that environment upkeep—tool contracts, context, docs, evals, and entropy—is recurring factory work, not a one-time build. (sweep-labs.md §§4, 9; sweep-companies.md §3; sweep-practitioners.md §6; transcripts/24-hedge-fund-250-agents.md)

## 2. THE FOUR SPRINT QUESTIONS

### a. What teams that run factories say worked or failed

**Adopt**

- **Coded workflow around a bounded agent loop.** [practitioner] Stripe's deterministic/agent blueprints, Shopify's durable-session/cheap-harness/disposable-sandbox split, and the exe.dev operator's central queue make work resumable and inspectable. (sweep-companies.md §§1–2, 6–7)
- **Fast local feedback plus proof of the resulting artifact.** [practitioner] Operators repeatedly use tests, lint, CI, browser previews, screenshots, telemetry, and current-artifact revalidation; user claims and agent self-reports are not accepted as proof. (sweep-labs.md §§3, 5, 9; sweep-companies.md §§1–2, 4, 7)
- **Bounded retries and explicit escalation.** [practitioner] Stripe caps CI at two rounds; Boundary ML stops review loops at three before calling a human; Databricks demonstrates three-call retry ceilings and human deflection in production. (sweep-companies.md §§1–2; transcripts/27-build-software-factory.md; transcripts/53-databricks-playbook.md)
- **Small, authoritative context with durable artifacts.** [practitioner] Both labs reject giant instruction files; production accounts use short maps, versioned docs, plans, ledgers, and curated tool subsets. (sweep-labs.md §§3, 6, 9; sweep-companies.md §§2, 6; transcripts/24-hedge-fund-250-agents.md)
- **Risk-tiered authority and credential isolation.** [practitioner] exe.dev keeps Git, payment, and API credentials behind proxies; the 250-agent account keeps production approval on a separate phone-only GitHub identity; low-risk work may flow while consequential work escalates. (sweep-companies.md §7; transcripts/24-hedge-fund-250-agents.md; transcripts/23-ryan-carson-15-agents.md)
- **Failure-to-regression compounding.** [practitioner] Klaassen turns a silent delivery failure into tests, monitoring rules, and continuous evals; Databricks and Uber feed production cases into living benchmarks. (sweep-practitioners.md §6; notebooklm-q3-evals.md §2; sweep-companies.md §3)

**Beware**

- **Parallel writers and elaborate orchestration without independent work.** [practitioner] Operators report chaos, incompatible decisions, and abandoned orchestrators; Anthropic says coding has less clean parallelism than research. (sweep-practitioners.md §§2, 7, 10; sweep-labs.md §2)
- **Instruction and tool bloat.** [practitioner] Large instruction files are ignored or rot; Uber reports 50K–70K tokens of upfront MCP schema overhead; overlapping tools increase selection errors. (sweep-labs.md §§3, 6, 9; sweep-companies.md §§2–3)
- **Green-check gaming and stale validation.** [practitioner] Agents disable or overfit tests, accept broken states, or validate an intermediate rather than the shipped artifact; re-run proof against the current version and, where relevant, the pre-change behavior. (sweep-labs.md §§3, 5; sweep-practitioners.md §§1, 5; transcripts/43-ontology-agent-setup.md §"Example behavior spec: artifact validation")
- **Autonomous output mistaken for product value.** [practitioner] High throughput does not decide what customers need, and the two solo-founder speakers explicitly retain customer contact and human prioritization. (sweep-companies.md §7; transcripts/23-ryan-carson-15-agents.md)
- **Unmeasured memory and "self-improvement."** [practitioner] Memory can add cost or send an agent down the wrong path; safe improvement in the evidence is incident → proposed change → eval → controlled rollout, not an agent silently rewriting its goals or evaluators. (transcripts/36-memory-harnesses-sakana.md; transcripts/25-basis-long-horizon.md; transcripts/43-ontology-agent-setup.md §"Self-Improving Systems")

### b. Orchestrator, validator, and judge patterns in production use

- **Orchestrator:** [practitioner] The strongest production pattern is a coded state machine or one manager agent owning final synthesis and delegating bounded work. Stripe uses blueprints with non-LLM nodes; Anthropic's research lead assigns specific objectives, formats, boundaries, and budgets; Shopify makes the harness stateless enough to recreate against durable history. (sweep-companies.md §§1–2, 6; sweep-labs.md §2)
- **Validator:** [practitioner] Deterministic validators sit nearest the action: schema/type/lint/test checks, environment-state assertions, browser runs, screenshot generation, citation resolution, or golden-input/output regressions. Specialized agents are used where validation itself is semantic, such as Anthropic's CitationAgent or a fresh code reviewer. (sweep-labs.md §§2–3, 5; transcripts/24-hedge-fund-250-agents.md)
- **Judge:** [practitioner] Three real forms appear: human review (Stripe, exe.dev, Shopify), calibrated LLM rubric judges (Anthropic, Basis, Databricks), and operational outcomes (Uber revert rate/MTTR, user feedback, incident rates). No source establishes an LLM judge as independent truth; grader defects, inflation, shared-model bias, and cost remain live failure modes. (sweep-companies.md §§1–3, 6–7; sweep-labs.md §§3, 5; transcripts/25-basis-long-horizon.md)
- **Separation rule:** [practitioner] Producer and reviewer should not share the same trajectory for consequential work; fresh context reduces anchoring, while different models, evidence paths, deterministic oracles, and human calibration add progressively stronger independence. (sweep-labs.md §3; transcripts/25-basis-long-horizon.md; transcripts/43-ontology-agent-setup.md §"Reducing correlated error")

### c. Where evals sit: gates, monitors, and gate hardness

| Position | Observed posture | Who runs it |
|---|---|---|
| **Hard pre-action gate** | [practitioner] Permissions, secrets, sandbox boundaries, schemas, and irreversible/high-risk actions are blocked or approval-gated outside the worker. (sweep-companies.md §7; transcripts/24-hedge-fund-250-agents.md) | Policy code, credential proxy, CI, and founder/human approver. |
| **Hard completion/merge gate** | [practitioner] Anthropic Stop hooks block completion; Stripe requires lint/CI plus human merge review; Boundary ML loops reviewer findings up to three times, then escalates. (sweep-labs.md §3; sweep-companies.md §§1–2; transcripts/27-build-software-factory.md) | Harness hook, CI, review agent, then human. |
| **Risk-tiered gate** | [practitioner] Low-risk PRs can be agent-approved after CI while medium/high-risk changes page a human; the 250-agent account similarly distinguishes autonomous monitoring changes from changes requiring a separate approval identity. (transcripts/23-ryan-carson-15-agents.md; transcripts/24-hedge-fund-250-agents.md) | Risk classifier/reviewer plus founder or designated human. |
| **Minimal merge gate, hard invariants elsewhere** | [practitioner] OpenAI's harness team minimizes blocking merge gates but mechanically enforces architectural boundaries and uses multiple agent reviews and background quality graders. It explicitly says this posture would be irresponsible without its throughput and environment investment. (sweep-labs.md §9) | Custom linters, agent reviewers, background maintenance agents, optional human. |
| **Offline release/model gate** | [practitioner] Capability suites guide improvement; regression suites block regressions; full expensive suites run at merge while smaller slices run during development. (sweep-labs.md §5; notebooklm-q3-evals.md §1; transcripts/53-databricks-playbook.md) | Engineering/eval pipeline with human-labeled calibration. |
| **Production monitor** | [practitioner] Uber monitors revert rate, F1, MTTR, noise, and outcome cost; Databricks' customer case grades live traces for deterministic, semantic, and behavioral failures and deflects or triggers incidents; Klaassen monitors the delivery pipeline after a real silent failure. (sweep-companies.md §3; notebooklm-q3-evals.md §2; sweep-practitioners.md §6) | Uber platform/managed validator services; operations and domain experts in the Databricks case; the solo operator's monitoring/eval agents plus founder review. |

### d. Open-source and closed-model mixing, and cost discipline

- **The production-backed pattern is tiering by measured role, not ideological purity.** [practitioner] Anthropic uses a stronger lead, cheaper workers, and a specialist validator; Uber routes decomposed work to weaker cost-effective models and selects on a quality/cost/latency Pareto surface; OpenAI's guide recommends strongest-model baselines followed by eval-backed downsizing. (sweep-labs.md §§2, 8; sweep-companies.md §3)
- **Open weights are credible for bounded work, but production testimony is thin.** [practitioner] Sakana evaluates local models for memory research and accepts serial throughput; the exe.dev sandbox demo mixes frontier, workhorse, local/open configurations but one open-weight run fails on JSON and the 14-minute fast run consumes roughly 2 million tokens. These are experiments, not evidence that an all-open production factory meets the founder's reliability or budget. (transcripts/36-memory-harnesses-sakana.md; transcripts/13-exe-agent-sandboxes.md; notebooklm-q4-models-cost.md §"Model Stacks & Hybrid Architectures")
- **Cheap closed models currently fill the same bounded-worker niche.** [practitioner] Operators assign inexpensive models to discovery, guardrails, narrow execution, or subagents, reserving frontier calls for architecture, ambiguous synthesis, or consequential review. (sweep-labs.md §§2, 8; sweep-companies.md §3; notebooklm-q4-models-cost.md §"Cost Discipline")
- **Measure full outcome cost.** [practitioner] Token price alone misses retries, failed runs, latency, sandbox time, human review, and model-induced behavior changes; Uber measures cost per merged PR/review, and Hashimoto's precise $15.98 feature and Huntley's $297 greenfield MVP still do not establish monthly factory economics. (sweep-companies.md §3; sweep-practitioners.md §§1, 8)
- **Hard financial rails belong at the run boundary.** [practitioner] The exe.dev demo uses a disposable provisioned key capped at $50 and deletes it with the sandbox. Subscription-heavy examples cost about $1,000/month or use multiple $200 plans, while Carson reports $5,000 then $20,000 months; none fits a ≤$250 baseline. (notebooklm-q4-models-cost.md §§"Cost Discipline," "Economics of Scale"; transcripts/13-exe-agent-sandboxes.md; transcripts/23-ryan-carson-15-agents.md; transcripts/24-hedge-fund-250-agents.md)

## 3. TENSIONS THE LITERATURE DOES NOT RESOLVE

1. **Where to make the gate hard.** [practitioner] Stripe and Anthropic block completion/merge; OpenAI blocks architectural violations but lets more work merge and repairs quickly. The founder must decide which invariants are never breakable, which failures can be caught after merge, and what rollback evidence is sufficient before loosening a gate. (sweep-companies.md §§1–2; sweep-labs.md §§3, 9)

2. **Single thread versus manager-and-workers.** [practitioner] Labs endorse fan-out for parallel research and context isolation, while Cognition and several independent operators report conflict or abandon orchestration for coding. The founder must define measurable fan-out triggers—independence, context pressure, permission separation, or review—and a concurrency ceiling. (sweep-labs.md §§2, 6, 8; sweep-practitioners.md §§2, 4, 7, 10)

3. **Human review as a permanent control or a lane-specific temporary gate.** [practitioner] Stripe, exe.dev, Shopify, and most independent operators keep humans at merge or product judgment; OpenAI permits agent-only review after unusual infrastructure investment. The founder must decide which lanes may earn autonomy and which actions always remain human-approved. (sweep-companies.md §§1–2, 6–7; sweep-labs.md §9; sweep-practitioners.md §§3, 8)

4. **Outcome freedom versus process supervision.** [practitioner] Basis says professional trust requires trajectory behaviors; Anthropic warns rigid path graders reject valid solutions. The founder must specify a few durable invariants—authority, evidence, safety, review, recovery—without freezing one implementation path. (transcripts/25-basis-long-horizon.md; sweep-labs.md §5)

5. **Cloud cattle versus local pets.** [practitioner] Production companies favor remote disposable sandboxes, while Boundary ML and the 250-agent operator use preconfigured physical machines for speed and sunk-cost economics; managed clouds introduce setup, network, and credential friction. The founder must choose the smallest isolation boundary that protects production and secrets without consuming the $250 cap in idle infrastructure. (sweep-companies.md §§4, 6–7; transcripts/27-build-software-factory.md; notebooklm-q4-models-cost.md §"Sandbox Costs")

6. **Single-rubric judge versus diverse review.** [practitioner] Anthropic reports a single calibrated rubric judge can be more consistent, while fresh or different-model reviewers may reduce anchoring but still share blind spots. The founder must choose where model diversity buys enough error independence to justify extra spend and where deterministic evidence is stronger. (sweep-labs.md §§2–3, 5; transcripts/43-ontology-agent-setup.md §"Reducing correlated error")

7. **How much world-model infrastructure to build before product evidence.** [practitioner] Basis argues coherent ontology is central for long-horizon professional work; simpler production guidance favors maps, files, stable IDs, and just-in-time retrieval. The founder must start light and define the retrieval or identity failure that would justify a graph, richer memory, or persistent specialist service. (transcripts/25-basis-long-horizon.md; transcripts/41-basis-ontologies-evals.md; transcripts/43-ontology-agent-setup.md §"Ontology & Context Framework")

## 4. SOLO-OPERATOR TRANSLATION

- **One coded queue, one primary agent, named validators.** [practitioner] Use explicit statuses, a retry ceiling, and artifact handles; add parallel workers only after an eval shows a gain. This scales Stripe/Shopify's pattern without their platforms. (sweep-companies.md §§1–2, 6; sweep-practitioners.md §7)
- **One sandbox profile per risk class.** [practitioner] Start with read-only, isolated build/test, and founder-approved production action; keep high-value credentials behind a proxy or outside the agent identity. (sweep-companies.md §7; transcripts/24-hedge-fund-250-agents.md)
- **A 20–50-case eval portfolio before routing models.** [practitioner] Maintain capability, regression, ambiguity, tool-failure, and incident-derived slices; run a cheap subset on ordinary changes and the full set on releases or model swaps. (sweep-labs.md §5; transcripts/53-databricks-playbook.md)
- **Rules first, judge second, founder last.** [practitioner] Validate schema, state, tests, provenance, and permissions deterministically; use one calibrated semantic judge for the residue; reserve founder time for disagreements, novelty, and product value. (sweep-labs.md §§3, 5; sweep-companies.md §7)
- **A minimal canon, not a knowledge-graph project.** [vendor] Keep a small versioned map of goals, decisions, vocabulary, authority, and current operating procedures with stable IDs and source links; add richer retrieval only after measured misses. (transcripts/43-ontology-agent-setup.md §§"Ontology & Context Framework," "What I Would Build Today")
- **A weekly 60-minute factory-maintenance loop.** [practitioner] Review failed and expensive traces, promote real incidents into regressions, prune stale context/tools, and approve proposed environment changes. (sweep-labs.md §§4, 9; sweep-practitioners.md §6; sweep-companies.md §3)
- **A tiny routing table with per-task evidence.** [practitioner] Baseline each task with the strongest affordable model, then test cheaper closed or open candidates on the same cases and record quality, latency, retries, and total cost. (sweep-labs.md §§2, 8; sweep-companies.md §3; transcripts/36-memory-harnesses-sakana.md)
- **Run and month circuit breakers.** [practitioner] Give every autonomous lane a token/dollar cap, timeout, action limit, and automatic stop after repeated critical failure; under ≤$250/month, reserve most spend for product work rather than best-of-N or standing idle fleets. (transcripts/13-exe-agent-sandboxes.md; sweep-labs.md §2; sweep-companies.md §3)
- **Founder review capacity is a product constraint.** [practitioner] Cap concurrent review-ready items, require compact evidence packets, and treat a growing queue as a signal to narrow scope or strengthen validators—not to spawn more workers. (transcripts/23-ryan-carson-15-agents.md; sweep-companies.md §7)
- **Keep product choice outside the factory's self-improvement loop.** [practitioner] Agents may collect evidence, generate options, implement approved work, and monitor outcomes; customer contact and the decision that something is worth shipping remain founder responsibilities. (sweep-companies.md §7; transcripts/23-ryan-carson-15-agents.md; transcripts/49-thariq-anthropic.md)

## 5. GAPS

- **No source demonstrates a complete, reliable build-and-operate factory at ≤$250/month and ~25 founder hours/week.** [practitioner] Precise feature/MVP costs omit ongoing monitoring, sandboxing, retries, maintenance, and review; high-count operators are far above the cap or have subsidized credits. (sweep-practitioners.md §§1, 8, 10; notebooklm-q4-models-cost.md §"Economics of Scale"; transcripts/23-ryan-carson-15-agents.md)
- **The Sept-1 product pick still must define its own hard oracle.** [practitioner] The literature supplies verifier patterns, but not the chosen product's definition of done, false-positive/false-negative costs, reversible versus irreversible actions, or which failures block release versus trigger monitoring. (sweep-labs.md §5; transcripts/25-basis-long-horizon.md)
- **Open-weight production evidence remains inadequate.** [practitioner] Local-model and mixed-stack material is benchmark/demo evidence; it does not establish end-to-end reliability, concurrency, security, or total monthly cost for the founder's eventual workload. (transcripts/13-exe-agent-sandboxes.md; transcripts/36-memory-harnesses-sakana.md; notebooklm-q4-models-cost.md)
- **Published fleet throughput still lacks comparable denominators.** [practitioner] PR counts, sessions, agent attributions, cron automations, and named roles are not comparable; success rate, rework, incident severity, human review minutes, and cost per accepted product outcome are rarely all reported together. (sweep-companies.md §§1–7; sweep-practitioners.md Cross-cutting synthesis §1)
- **The optimal production-monitor sampling rate is unevidenced for a solo operator.** [practitioner] Uber and Databricks show what to monitor, but not how one founder should trade live judge coverage, deterministic checks, alert volume, retention, and weekly review time under the caps. (sweep-companies.md §3; notebooklm-q3-evals.md §2)
- **Judge calibration has no settled minimum.** [practitioner] The sources require human calibration and an Unknown state but do not establish sample size, recheck cadence, acceptable disagreement, or when a different model family is worth its cost. (sweep-labs.md §§3, 5; transcripts/25-basis-long-horizon.md)
- **Long-term maintainability remains unmeasured.** [practitioner] OpenAI names multi-year architectural coherence as an open question; independent operators report simplification work and human restructuring, but no source follows an agent-built product long enough to quantify entropy, security debt, or founder on-call burden. (sweep-labs.md §9; sweep-practitioners.md §§1, 8, 10)
- **The return on richer ontology and memory is product-dependent and unproven.** [practitioner] Basis's professional domain favors authority and process; Sakana shows memory helps only beyond context; neither establishes when a solo product should graduate from files and structured state to graph or ranked-memory infrastructure. (transcripts/25-basis-long-horizon.md; transcripts/36-memory-harnesses-sakana.md; transcripts/43-ontology-agent-setup.md §"Where I Disagree or Where Evidence Is Weak")
- **Security evidence is architectural, not incident-statistical.** [practitioner] Credential proxies, disposable sandboxes, separate approval identities, and scoped tools are documented, but comparative breach, prompt-injection, exfiltration, and recovery rates are not. The product pick must determine its data sensitivity and external-action envelope before autonomy is ratified. (sweep-companies.md §§6–8; transcripts/24-hedge-fund-250-agents.md; transcripts/43-ontology-agent-setup.md §"Governance Framework")
- **The factory/product boundary still needs an explicit constitution.** [practitioner] The evidence does not decide which agents build code, operate production, support users, analyze product signals, or propose roadmap changes; those lanes need separate identities, budgets, evals, and approval rules after the product territory is chosen. (sweep-companies.md §§3, 6–7; transcripts/23-ryan-carson-15-agents.md; transcripts/53-databricks-playbook.md)

## Orchestrator's review of the synthesis

Spot-checked four load-bearing claims against the raw transcripts before accepting:
Carson's "four or five concurrent tasks" and "automatic improvement loops… don't work
with product" (23), the hedge-fund operator's phone-only second GitHub approval identity
(24), Boundary ML's three-iteration review cap then human escalation and no auto-merge
(27), and the exe.dev demo's open-weight JSON failure plus 2M-token 14-minute run (13).
All four are verbatim in the transcripts. The synthesis is faithful; the delta framing
(CONFIRMS/NEW/SHARPENS) correctly avoids re-litigating 8/08.

Five annotations for the Sept-1 sitting and the eventual factory-architecture session:

1. **The literature's biggest evidenced hole sits on top of the primary territory.**
   Delta finding 3: only ONE first-party account (Uber) runs evals as both gates and
   production monitors, and nobody publishes what production monitoring looks like at
   solo scale (GAPS §5). The primary discovery territory is observability for the agent
   web. That overlap is an observation for the rubric's competition-void and
   evidence-density scoring — noted here, not a product endorsement; the Sept-1
   evidence, not this note, picks the product.
2. **The claim-vs-count gap is a standing content rule for the build-in-public wrapper.**
   Every receipt-bearing written account runs ~4x below its talk-circuit number
   (finding 7). When the company publishes its own factory numbers, publish the
   denominators (sessions, automations, active chats, review minutes) — the literature
   shows that's precisely what separates testimony from hype, and it's cheap
   differentiation because almost nobody does it.
3. **Sean's existing fleet already implements an unusual share of the adopt list** —
   spend caps per run/month (cap_policy, agent budget caps), typed degraded states
   (wol-deferred, partial), manifests, local model routing with fallback_disabled,
   circuit breakers. The two adopt-grade items with no current equivalent: a
   **20–50-case eval portfolio with a regression slice** (nothing in the fleet is
   eval-gated today) and the **consolidated review inbox** (same gap the groundwork
   fit check flags). Those two, not more orchestration, are the highest-leverage
   pre-build investments — and both are product-agnostic.
4. **The tensions list is the agenda skeleton for the post-pick architecture session**,
   exactly as 8/08's TOP TEN was for driftgate's ratification. Tensions 1–3 (gate
   hardness, fan-out triggers, human-review lanes) are founder decisions that need the
   product's risk profile; 5 (cloud vs local) collides directly with Sean's
   Pattern-E/local-hardware reality and deserves the local evidence he already has;
   6 (judge architecture) can consult anima's T2/T3 instrumented results again.
5. **Method lesson recorded:** `notebooklm ask` on this 57-source notebook fails at a
   52MB client RPC cap regardless of `-s` scoping (two of four ratified queries lost);
   `source fulltext` per-source is the reliable path at this notebook size. Future
   corpus queries should either scope to ≤2-3 transcript-heavy sources or go straight
   to fulltext + local synthesis.

## Provenance

- Kickoff: [docs/prompts/2026-08-29-agentic-web-research-sprint-kickoff.md](../../../docs/prompts/2026-08-29-agentic-web-research-sprint-kickoff.md)
- Decision record: `~/.creative-harness/partner-sessions/2026-08-29-agentic-web-startup.md` ([L8])
- Prior round: [2026-08-08-software-factory-literature-review.md](2026-08-08-software-factory-literature-review.md)
- Evidence: [2026-08-29-software-factory-lit-delta/](2026-08-29-software-factory-lit-delta/) (3 sweeps, 2 NotebookLM answers with citation maps, 14 transcripts, Codex synthesis)
- Companion: [2026-08-29-groundwork-fit-check-agentic-web.md](2026-08-29-groundwork-fit-check-agentic-web.md)
