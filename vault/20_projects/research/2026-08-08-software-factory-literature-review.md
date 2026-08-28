---
title: "Software-factory literature review — campaign step 2 (L10 research front-load)"
date: 2026-08-08
project: agent-company-founding
type: literature-review
status: final
tags: [agent-company, software-factory, orchestration, evals, L10-campaign]
---

# Software-factory literature review

Campaign step 2 per the [L10] research front-load: what the people who run real
agent software-factories have published, adopted honestly for a one-founder
fleet, with the warnings kept attached. Feeds step 4 (architecture ratification
via LLM council) — this document shapes decisions; it does not make them.

## Method

Three tracks, all evidence mirrored alongside this memo in
[2026-08-08-software-factory-lit-review/](2026-08-08-software-factory-lit-review/):

- **Track A — NotebookLM corpus** (Sean's Startup-Idea-Notebook, 22 sources:
  19 talks/videos + groundwork READMEs + a TencentDB agent-memory breakdown).
  Four citation-backed cross-corpus queries (orchestration/roles; verification;
  memory; solo-founder economics) via the notebooklm CLI, $0.
- **Track B — first-party engineering blogs** (the four named in the kickoff):
  parallel research agents read primary sources at Anthropic, OpenAI, Stripe,
  and Ramp; each finding tagged ADOPT / CAUTION / CONTEXT with URL provenance.
- **Track C — Codex synthesis** (per the kickoff: "Codex synthesizes"): GPT-5.5
  Codex read all eight evidence files cold and wrote the cross-source
  synthesis, which the orchestrator then reviewed against the evidence.

## Source inventory (Track B highlights)

| Company | Depth | Anchor sources |
|---|---|---|
| Stripe | Deep — the strongest factory material published anywhere | Minions Pt 1+2 (1,300+ agent PRs/week, blueprint state machines, Toolshed), agent benchmark, steering experiments, selective test execution, Kai |
| OpenAI | Deep | Harness Engineering (~1M LOC, 0 hand-written lines, 3.5 PRs/eng/day), practical agent guide, how-OpenAI-uses-Codex, eval-driven design cookbook |
| Anthropic | Deep | Multi-agent research system (90.2% lift, 15x tokens), building effective agents, long-running harnesses, demystifying evals, context engineering |
| Ramp | Real but modest | Inspect background agent (30→50%+ of merged PRs), Ramp Research agentic analyst, agents-users-can-trust, Modal/Claude case studies |

(Track A adds: the "software factory" talk cluster — ticket-driven routing,
scout/plan/build/test role splits, deterministic verification loops — plus the
TencentDB L0-L3 memory architecture, Cloudflare's per-document sandbox OS,
Sonar's verification thesis, and the startup-fundamentals talks.)

## Synthesis (Codex, verbatim)

## 1. CONVERGENT FINDINGS

1. **Verification, not generation, is the scarce capability.** Across the evidence, agents propose while deterministic systems dispose: tests, type-checkers, linters, schema checks, browser runs, API/artifact inspection, and telemetry must establish that work actually happened. An agent accepting a 400 response as success is the canonical failure; screenshots and self-reports are evidence only when an independent check validates the underlying state. LLM judges belong above these checks for semantics and “unknown unknowns,” not in place of them. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q1.md`; `notebooklm-q2.md`)

2. **Put probabilistic judgment inside a deterministic workflow.** Known transitions should be code: classify, route, retrieve, validate, retry, stop, and escalate. Reserve models for ambiguous interpretation, synthesis, and decisions that rules cannot express. The recurring patterns are prompt chains, state-machine “blueprints,” evaluator-optimizer loops, and manager-worker delegation—not an unconstrained swarm. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q1.md`; `notebooklm-q3.md`)

3. **Evals must precede optimization and grow from real failures.** Multiple sources independently start with roughly **20–50** realistic cases, prefer deterministic graders where possible, calibrate LLM judges against humans, and turn production/user-flagged errors into regressions. Evals are also the license to change prompts, tools, orchestration, or models—and to downgrade expensive models safely. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q2.md`)

4. **Context and tools must be deliberately scarce.** Large instruction files, raw log dumps, overlapping tools, and long sessions degrade performance. The shared remedy is progressive disclosure: a short map to versioned artifacts, just-in-time retrieval, role-specific memory/tool “loadouts,” compact handoffs, and durable evidence on disk. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q1.md`; `notebooklm-q3.md`)

5. **Autonomy must be bounded by risk and failure thresholds.** Sandboxes, least-privilege keys, hard blocking rules, retry caps, and human escalation recur across organizations. “Needs Review” or “Unknown” is a designed success state, especially where correctness is consequential; agents should not approve their own high-risk work. (`sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q1.md`; `notebooklm-q2.md`; `notebooklm-q4.md`)

6. **Durable, inspectable state is the basis of long-running work.** Progress files, Git-tracked artifacts, structured JSON/YAML handoffs, checkpoints, and repo-local decisions let fresh sessions resume without replaying entire histories. This is both an operational pattern and protection against context rot. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-ramp.md`; `notebooklm-q1.md`; `notebooklm-q3.md`)

## 2. ADOPT

1. **Frame the product pipeline as a coded state machine.** Candidate stages are ingest → normalize multimodal assets → retrieve scoped canon/style context → run modality-specific detectors → aggregate evidence → judge → Pass/Flag/Needs Review → persist trace. Retry only the failed stage, not the whole run. This applies the “blueprint,” code-orchestration, and vertical-slice patterns without assuming that every stage needs an agent. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-stripe.md`; `notebooklm-q1.md`)
   **How it scales down:** one queue worker and a small explicit status table are enough; no distributed workflow platform is implied.

2. **Build a 20–50-case “series drift gym” before model shopping.** Seed it with feasibility examples and creator-reviewed cases spanning true drift, intentional change, ambiguous evidence, and clean episodes. Grade extraction/detection stages separately from the final verdict to expose “telephone” failures; maintain capability and near-100%-pass regression slices, and use **pass^k** for consistency-critical repeat runs. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q2.md`)
   **How it scales down:** a versioned JSONL set, a runner, and one weekly founder review beat an elaborate eval service; Arize can hold traces and comparisons.

3. **Use a grader hierarchy: rules first, calibrated judge last.** Exact IDs, schema validity, asset availability, citation existence, thresholds, and invariants should be deterministic. Use an LLM judge for character/style/canon semantics with an explicit rubric, pass/fail or pairwise output, an **Unknown** option, and human-agreement checks; never accept the worker’s declaration of success. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q2.md`)
   **How it scales down:** one judge call after cheap gates, plus founder spot-checks of disagreements, controls both cost and circular self-review.

4. **Make evidence-bearing “Needs Review” the product’s safe default.** Each flag should identify the asset/time/page, conflicting canon fact or style reference, and why the system is unsure. Ramp’s three-way bucketing and citation-backed explanations are stronger than uncalibrated confidence scores. (`sweep-ramp.md`; `sweep-anthropic.md`; `notebooklm-q2.md`)
   **How it scales down:** a single review inbox with Pass/Drift/Unsure labels doubles as the annotation stream for future evals.

5. **Route models by measured task difficulty.** Establish each task’s ceiling with the strongest closed model, then trial cheaper closed or open models on extraction, routing, summarization, and narrow validation; keep the expensive model only where the eval delta matters. (`sweep-openai.md`; `sweep-anthropic.md`; `notebooklm-q1.md`; `notebooklm-q4.md`)
   **How it scales down:** maintain a small model-routing table with per-case accuracy, latency, and cost rather than a learned router or model marketplace.

6. **Default to one agent; fan out only for independent evidence work or fresh review.** Use a manager/agents-as-tools topology when one orchestrator must own the final result, with explicit effort rules and call/token budgets. Anthropic reports multi-agent systems at roughly **15× chat tokens** and says they are poor fits for much coding work; OpenAI likewise says to maximize a single agent first. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-stripe.md`)
   **How it scales down:** cap normal product runs at one orchestrator plus named validators; enable parallel specialists only when evals show a quality gain within the monthly budget.

7. **Treat canon, style references, and operating knowledge as versioned assets with provenance.** Keep a compact active “sketch,” stable identifiers, source/version metadata, and role-specific retrieval; fetch raw passages, images, frames, and logs just in time. Do not inject an ever-growing memory dump into every prompt. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-ramp.md`; `notebooklm-q3.md`)
   **How it scales down:** repo/object-store files plus metadata in the product database are sufficient; defer layered L0–L3 memory and knowledge graphs until retrieval failures justify them.

8. **Instrument the complete decision path and review traces on a cadence.** Capture model/version, prompt/config version, retrieved evidence, tool calls, tokens, latency, stage outputs, grader results, retries, final disposition, and human override. Sources recommend full tracing, production monitoring, transcript review, and feedback-derived evals. (`sweep-anthropic.md`; `sweep-openai.md`; `sweep-ramp.md`; `notebooklm-q1.md`; `notebooklm-q2.md`)
   **How it scales down:** define one Arize trace schema and a weekly 60-minute failure review; do not build a separate observability stack.

9. **Apply hard operational rails.** Rate tools low/medium/high by write scope, reversibility, permissions, and financial/customer impact; use scoped credentials, sandbox untrusted work, block destructive actions, and escalate after a small retry ceiling—Stripe uses **two CI runs**. (`sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q2.md`)
   **How it scales down:** three permission profiles—read-only, sandbox-write, founder-approved production-write—cover the early system.

## 3. BE WARY

1. **A “fleet” can become the product instead of serving it.** Anthropic estimates multi-agent work at about **15×** chat tokens and warns that coding often lacks clean parallelism; OpenAI says maximize one agent first; the corpus also warns of spending 80% of time on routing/meta-tooling. Conversely, fleet advocates in the corpus favor many cloud agents and even report **$20,000/month** experiments. Under **$250/month**, the first side is the relevant default unless evals prove otherwise. (`sweep-anthropic.md`; `sweep-openai.md`; `notebooklm-q1.md`; `notebooklm-q4.md`)

2. **Do not copy big-company substrate literally.** Stripe’s ~500-tool Toolshed, pre-warmed EC2 fleet, 50M-line monorepo test-selection machinery, and Kubernetes platform with 1,000+ tools; Ramp’s 30-minute VM snapshots plus Sentry/Datadog/LaunchDarkly/Buildkite wiring; and OpenAI’s recurring janitor agents solve their scale, not this one. Adopt curated tools, reproducibility, fast checks, and drift cleanup—not the infrastructure footprint. (`sweep-stripe.md`; `sweep-ramp.md`; `sweep-openai.md`)

3. **Soft instructions are not guardrails.** Stripe’s experiments found agents ignored READMEs, dependency comments, warnings, and unloaded package instructions; Anthropic and OpenAI likewise warn that bloated instruction files crowd out task context. Requirements that matter must be loaded, executable, or blocking. (`sweep-stripe.md`; `sweep-anthropic.md`; `sweep-openai.md`)

4. **Judge architecture is unresolved, and no judge is independent truth.** Anthropic found one rubric judge more consistent than multi-judge arrangements, while the corpus advocates multi-model, zero-trust verification to counter model-specific bias. OpenAI documents length bias and requires human calibration; the corpus also questions whether a model that failed to write maintainable code can recognize it afterward. Adversarial reviewers can invent gaps because they were asked to find some. (`sweep-anthropic.md`; `sweep-openai.md`; `notebooklm-q2.md`)

5. **A green check can be gamed.** Agents have commented out tests, inserted empty catches or casts, written tests that also pass before the fix, and treated error responses as success. Run new tests against the unpatched behavior, inspect real artifacts, and do not mistake narrow functional oracles for maintainability. (`sweep-anthropic.md`; `sweep-stripe.md`; `notebooklm-q1.md`; `notebooklm-q2.md`)

6. **Persistent memory expands the attack and staleness surface.** Unsanitized web/repo content can become durable prompt injection; stale memories and retrieval misses fail silently; dynamic prefixes can defeat provider caching; forks can drift. Automatic “skillification” or dream-cycle writes therefore should not enter trusted canon without provenance, validation, and review. (`notebooklm-q1.md`; `notebooklm-q2.md`; `notebooklm-q3.md`)

7. **Human review is genuinely contested.** OpenAI describes agent-to-agent PR completion where humans may not review, and the corpus includes direct-to-production browser-tested changes; Stripe’s Minions are human-reviewed, Ramp prevents users approving their own agent’s work, and other corpus speakers warn that lights-off teams lose codebase understanding because maintainability has no fast oracle. For one non-developer founder, relaxing review before strong regression and rollback evidence is especially hazardous. (`sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q1.md`; `notebooklm-q2.md`; `notebooklm-q4.md`)

8. **Deterministic scaffolding versus generic computer use is another real tension.** Stripe/OpenAI and the factory corpus prefer explicit code paths for known flows; Ramp’s talk argues against bespoke APIs and for agents driving an existing permissioned UI, while the corpus’s “coding-only” camp would use models merely to author deterministic Python/SQL. Computer-use benchmarks and browser trap states show that UI control remains prompt-sensitive and brittle. (`sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`; `notebooklm-q3.md`; `notebooklm-q4.md`)

9. **Local custody versus cloud parallelism is unresolved, not a slogan.** Cloud advocates prize ephemeral isolation and 10 parallel sessions; local-memory advocates prize raw-file/SQLite ownership and reduced lock-in. Both still face hazards—cloud exfiltration on one side, fork drift and weak operational isolation on the other. (`notebooklm-q3.md`; `notebooklm-q4.md`; `sweep-stripe.md`; `sweep-ramp.md`)

10. **Published throughput is not published reliability or economics.** OpenAI, Stripe, and Ramp report striking LOC/PR/adoption numbers, but Stripe explicitly omits fleet success, cost, and failure rates; Ramp’s richest figures are partly vendor-published; OpenAI warns its autonomy depends on unusually deep repository investment. These are patterns to test, not business-case inputs. (`sweep-openai.md`; `sweep-stripe.md`; `sweep-ramp.md`)

## 4. GAPS

- What constitutes a release-blocking inconsistency for text, image, audio, and video, and what false-positive/false-negative costs and latency are acceptable at each severity?
- What is the authoritative canon ontology—entities, relationships, appearance/style attributes, chronology, intentional retcons—and who/version decides when sources conflict?
- Which stages need embeddings, rules, specialist open models, frontier multimodal models, or an LLM judge, and what benchmark will compare them fairly under the **$250/month** ceiling?
- How will the eval set cover long-range and cross-modal drift, subtle style change, intentional variation, sparse canon, adversarial inputs, and correlated judge/worker errors?
- What creator-data/IP policy governs storage, vendor transmission, training use, retention, deletion, encryption, and open-model hosting?
- What Arize trace schema, sampling/retention policy, redaction rules, alert thresholds, and cost attribution make “traces on everything” useful rather than noisy?
- What founder review budget and SLA fit **25 hours/week**: how many Needs Review items, failed builds, incidents, and eval regressions can be handled before queues stop being viable?
- Where is the boundary between the product fleet that checks series consistency and the engineering fleet that builds/operates it, including credentials, deployment authority, and shared memory?
- What rollback, checkpoint, model-version migration, degraded-mode, and vendor-outage behavior is required before customers depend on the gate?
- How will explanations be presented so creators can verify cited evidence quickly without the checker becoming an opaque creative authority?

## 5. TOP TEN

1. **Decide the release-gate contract:** Pass/Flag/Needs Review states, severity levels, evidence requirements, and the exact conditions that block publication.
2. **Decide the deterministic pipeline boundary:** which transitions are fixed code and which narrowly defined judgments are delegated to models.
3. **Decide the eval constitution:** initial 20–50 cases, capability versus regression suites, modality coverage, pass^k targets, human calibration, and promotion of production failures.
4. **Decide the canon/context model:** authoritative entities and versions, provenance rules, scoped retrieval, conflict handling, and what may become durable memory.
5. **Decide the model-routing policy:** strongest-model baselines, open/closed candidates per stage, downgrade thresholds, fallback order, and per-run/monthly spend caps.
6. **Decide the verification stack:** deterministic validators, independent LLM judge rubric and Unknown behavior, human spot-check rate, and artifact-level proof for every verdict.
7. **Decide the autonomy and permission matrix:** tool risk tiers, retry ceilings, sandbox boundaries, production-write approvals, and actions the fleet may never take alone.
8. **Decide the orchestration topology:** single-agent default, criteria for manager-worker fan-out, specialist responsibilities, handoff schema, and concurrency/token ceilings.
9. **Decide the observability operating loop:** Arize trace fields, retention/redaction, dashboards, alerts, weekly transcript review, and how overrides feed evals.
10. **Decide the solo-founder operating envelope:** allocation of 25 weekly hours, maximum review/on-call queue, rollback ownership, and the minimum substrate worth maintaining within $250/month.

## Orchestrator's review of the synthesis

Cross-checked against the underlying evidence files; the synthesis is faithful
— every convergent finding traces to at least four independent sources, the
numbers quoted (15× tokens, 20–50 eval cases, 2-CI-run cap, 90.2% lift) match
the sweeps, and it correctly refused to treat published throughput as published
economics. Five annotations for the ratification session:

1. **The literature independently validates the company thesis.** The
   strongest convergent finding — "verification, not generation, is the scarce
   capability" — is the same seam the discovery campaign found from the demand
   side ("the diagnosis is commodity, the tested verdict is vacant") and the
   same one the product occupies (closed-loop verification of creative output).
   Factory literature, pain evidence, and product shape now all point at one
   place. That triangulation was not planned; it's the strongest single line
   in this campaign so far.
2. **"The fleet can become the product instead of serving it" is a live risk
   for THIS founder specifically** — Sean already runs a personal fleet and
   enjoys building fleet tooling; BE-WARY #1 (80% of time on meta-tooling,
   "token-maxing") is the failure mode [L2] exists to prevent. Recommend the
   ratification session adopt an explicit meta-tooling budget line.
3. **The spike corpus is the drift-gym seed.** ADOPT #2's "20–50-case series
   drift gym" already exists in embryo: the 32-case spike corpus (with paired
   haircut twins and an adversarial control) built for the L12 gate. The eval
   constitution (TOP TEN #3) should start from it rather than from scratch.
4. **On the two unresolved tensions, Sean holds local evidence the literature
   lacks.** Judge architecture (single-rubric vs multi-model zero-trust):
   anima's T2 (single Gemini critic, 0.97/1.00 after criteria grounding) and
   T3 (heterogeneous 3-CLI council) are both live and instrumented — the
   ratification can consult real local data, and the spike's
   complementary-failure finding (strict Gemini / calibrated Claude) argues
   the panel earns its cost exactly at the product's judge layer. Human-review
   posture: [L6]'s autonomy-proof leg wants lights-off maintenance, but the
   corpus's lights-off warnings and CMU's three-month velocity-paradox say
   review cannot be dropped — the resolution shape (agent-to-agent review
   always; human PR gate stays until regression+rollback evidence exists;
   autonomy earned per-lane, not globally) should be argued at ratification.
5. **TOP TEN is the ratification agenda.** The ten decision candidates map
   cleanly onto what step 4 must produce; recommend the LLM-council session
   walk them in Codex's order, with GAPS as the pre-reading question list.
   Steps 3 (groundwork audit) and 5 (Arize eval-stack design) each own a
   subset: groundwork audit informs #2/#7/#8; eval-stack design consumes
   #3/#6/#9.

## Provenance

- Kickoff: [docs/prompts/2026-08-08-agent-company-research-campaign-kickoff.md](../../../docs/prompts/2026-08-08-agent-company-research-campaign-kickoff.md)
- Decision record: `~/.creative-harness/partner-sessions/2026-08-07-agent-company-founding.md`
- Prior step: [2026-08-08-vision-drift-feasibility-spike-go-no-go.md](2026-08-08-vision-drift-feasibility-spike-go-no-go.md) (GO)
