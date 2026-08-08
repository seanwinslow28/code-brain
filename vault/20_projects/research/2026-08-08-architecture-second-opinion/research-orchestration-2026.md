All research complete. Here is the structured report.

# Multi-Agent LLM Failure Modes & Orchestration — State of Knowledge, August 2026

Scope note: Anthropic/OpenAI/Stripe/Ramp engineering blogs excluded per instruction. Everything below is academic work, other companies' material, or 2026 syntheses. Findings tagged against the target architecture (single orchestrator default, coded state-machine pipelines, deterministic gates + LLM judge panel, per-lane earned autonomy).

## A. Failure taxonomies (academic)

**1. MAST — "Why Do Multi-Agent LLM Systems Fail?" (Cemri, Pan et al.)** — https://arxiv.org/abs/2503.13657 (2025; ICML; still the canonical taxonomy cited by everything in 2026)
- CONFIRMS: 14 failure modes in 3 clusters — specification/system-design (~42%), inter-agent misalignment (~37%), task verification (~21%). The largest bucket is *bad specs*, not bad models — coded state-machine pipelines with explicit termination conditions attack the biggest category directly.
- CONFIRMS: Weak/absent verification is its own failure class (~21%) — deterministic gates are the prescribed remedy.
- NEW: MAST's own LLM-as-judge annotation pipeline needed human validation to be trustworthy (kappa 0.88 with experts) — judge output should be treated as annotation, not ground truth.

**2. "Beyond Individual Intelligence" survey (Qi et al., 17 authors)** — https://arxiv.org/abs/2605.14892 (May 2026)
- NEW: First survey to causally chain capability → collaboration → **failure attribution** → self-evolution (LIFE framework). 2026's framing treats fault diagnosis as a first-class architectural stage, not an ops afterthought.
- CHALLENGES (mildly): calls for closed-loop systems that *self*-diagnose and reorganize — a static hand-coded pipeline is positioned as the current-gen answer, not the end state.

**3. Who&When (arXiv 2505.00212, ICML) + Who&When Pro** — https://arxiv.org/abs/2607.09996 (July 10, 2026)
- CONFIRMS (strongly): automated failure attribution is *bad* — best methods hit 53.5% at naming the responsible agent and **14.2%** at finding the decisive error step; o1/R1-class reasoners "fail to achieve practical usability." You cannot rely on an LLM to debug your fleet; deterministic checkpoints and typed manifests (knowing which stage failed by construction) are worth more than any post-hoc attributor.
- NEW: Who&When Pro ships 12,326 labeled failed trajectories across 26 benchmarks — attribution is now a benchmarked subfield; expect tooling, don't expect reliability yet.

**4. DRIFT / TELBench — span-level error localization** — https://arxiv.org/abs/2606.02060 (June 2026)
- NEW: Claim-centric auditing (track each agent claim, check it against trajectory evidence, flag unsupported claims that affect the answer path) improves first-error localization by up to 30pp. A cheap pattern to steal for pipeline observability: log *claims with evidence pointers*, not just outputs.
- CONFIRMS: most trajectory "errors" are harmless exploration; only spans feeding the answer path matter — gate on outputs at stage boundaries, don't police every step.

**5. "Silent Failure … The Entropy Principle" (Liu)** — https://arxiv.org/abs/2606.08162 (June 2026)
- CONFIRMS: from 40K+ trials and 100K+ production interactions: disorder in agent systems accumulates monotonically with interaction rounds without external triggers; the paper's remedy is "deterministic governance" gates (their PIG/ADE proposals) rather than trying to fix the model. This is the academic version of "hooks enforce; subagents judge."
- NEW: silent failure (wrong output, no error signal) is framed as *inevitable* under long horizons — long-running lanes need periodic re-grounding against source-of-truth state, not just error handling.

**6. "When Does Multi-Agent Collaboration Help? An Entropy Perspective"** — https://arxiv.org/abs/2602.04234 (Feb 2026, rev. June 2026)
- CHALLENGES: a single agent beats the multi-agent system in ~43.3% of cases studied — multi-agent is not a default upgrade; keep single-orchestrator as default and demand justification per lane.
- CONFIRMS: entropy dynamics are "largely determined during the first round of interaction" — errors cascade from the *start*, so front-load spec quality and first-gate strictness rather than adding late-stage review.

**7. "Recognize Your Orchestrator" (Zhu et al.)** — https://arxiv.org/abs/2606.01351 (May 31, 2026)
- CHALLENGES (a common assumption): the "Reasoning Trap" — the strongest reasoning models often *underperform as orchestrators* due to context squeezing under multi-agent management load. Don't assume the biggest model belongs in the orchestrator seat; a mid-tier model plus coded routing can beat a frontier model doing freeform coordination.
- CONFIRMS: orchestration modeled as competition between task resolution and cumulative context load — the coded-state-machine choice (moving coordination out of the context window entirely) sidesteps the measured collapse mode.

**8. "Invisible Orchestrators" (Fukui)** — https://arxiv.org/abs/2605.13851 (March 2026)
- NEW: hidden-coordinator architectures degraded internal agent behavior in ways *invisible to output-based evaluation*; one model fell 89% → 11% accuracy in multi-agent context. Two takeaways: make orchestration visible to worker agents in their prompts, and re-benchmark any model swap *inside* the multi-agent harness, not solo.

**9. "The Six Sigma Agent" (Patel et al.)** — https://arxiv.org/abs/2601.22290 (Jan 29, 2026)
- CONFIRMS: decompose-to-atomic-tasks + n-way redundant execution + consensus voting: claimed 14,700x reliability gain at 80% *lower* cost using cheap diverse models — supports "many cheap checked runs beat one expensive trusted run" for gate-able atomic steps.
- CHALLENGES (nuance): their reliability math assumes *independent* errors across models — which the judge-panel literature below shows is mostly false in practice. Treat the O(p^⌈n/2⌉) claim as an upper bound.

**10. "Coordination as an Architectural Layer" (Nechepurenko & Shuvalov)** — https://arxiv.org/abs/2605.03310 (May 2026)
- CONFIRMS: coordination defects, not model limits, drive production failures; coordination should be a *configurable layer separable from agent logic* — exactly the state-machine-outside-the-LLM choice. Validated on 100 live prediction-market questions with cost-quality Pareto analysis.

## B. Judge-panel reliability (directly hits the "LLM judge panel" pillar)

**11. "Nine Judges, Two Effective Votes" (Kohli)** — https://arxiv.org/abs/2605.29800 (May 28, 2026)
- CHALLENGES (the most important single result for this architecture): a 9-judge panel across 7 model families carried only ~2 independent votes of information; ~75% of theoretical independence lost to correlated errors; accuracy 8–22pp below the independent-voting ideal; **a single best judge matched or beat the full panel**; better aggregation recovered at most 11% of the gap.
- Implication: don't size the judge panel for statistical comfort. Two genuinely different judges (different family + different *prompt framing/evidence access*) plus deterministic checks ≈ the practical ceiling; the rest is spend.

**12. Supporting 2026 judge studies** — "Reliability without Validity" https://arxiv.org/abs/2606.19544, "When the Judge Changes, So Does the Measurement" https://arxiv.org/abs/2607.08535 (June–July 2026)
- CHALLENGES: no judge uniformly reliable; consistency breaks on formatting/paraphrase/verbosity shifts; temp-0 same-verdict >95% but ~70% at temp 1; swapping judges silently changes what you're measuring.
- CONFIRMS: pins judges at temp 0, version-pin the judge model, and treat a judge swap as a measurement change requiring recalibration.

## C. Practitioner positions — single vs multi-agent (2026 resolution)

**13. Cognition — "Multi-Agents: What's Actually Working"** — https://cognition.com/blog/multi-agents-working (April 22, 2026)
- CONFIRMS: Cognition formally revised "Don't Build Multi-Agents": "multi-agent systems work best today when **writes stay single-threaded** and the additional agents contribute **intelligence rather than actions**." Single-orchestrator + read-only helpers is now their stated pattern (map-reduce-and-manage via Managed Devins, March 2026, each child in an isolated VM).
- CONFIRMS: dedicated review agents with *clean, unshared* context caught ~2 bugs/PR (58% severe) — fresh-context verification beats shared-context verification; judges/gates should NOT see the builder's context.
- CHALLENGES: "smart friend" escalation fails when the primary model is weak — it can't recognize when to escalate. Earned-autonomy lanes on cheap models need *coded* escalation triggers, not model self-assessment.
- NEW: remaining unsolved: children surfacing discoveries that should redirect sibling work; cross-agent context transfer. They call these "training problems," not engineering problems.

**14. LangChain — "How and when to build multi-agent systems"** — https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems (June 2025, still the referenced framing)
- CONFIRMS: read-heavy work parallelizes; write-heavy doesn't ("actions carry implicit decisions, and conflicting decisions carry bad results"). Cognition-vs-Anthropic was never really a contradiction — it was task-shape dependence.

**15. FlowHunt 2026 synthesis** — https://www.flowhunt.io/blog/multi-agent-ai-system/ (2026)
- CONFIRMS: cross-vendor convergence on one architecture: single orchestrator, ephemeral isolated subagents returning compressed summaries. The 2025 debate "collapsed."
- CHALLENGES (cost realism): multi-agent ≈ 15x token multiplier vs chat; token spend explains ~80% of performance variance; at *equal token budgets* single-agent matches or beats multi-agent on reasoning tasks. Multi-agent pays only for parallelizable read-heavy work, narrow-domain reliability, or security-boundary separation.

## D. Production failure modes & cost incidents

**16. Gravity — "AI Agent Failures: Lessons From 2026"** — https://gravity.fast/blog/ai-agent-failures-lessons-from-2026/ (June 13, 2026)
- CONFIRMS: seven recurring patterns (hallucinated actions, infinite loops/runaway cost, tool misuse, prompt injection, silent failures, context loss, over-automation); mitigations are exactly the architecture's shape: hard iteration caps, token budgets, schema validation, independent result checking, checkpointed subtasks, human gates on irreversible actions.
- NEW: Gartner projects >40% of agentic AI projects canceled by end-2027 (cost, unclear value, inadequate controls) — cost governance is a survival feature, not hygiene.

**17. Cost-blowup incident reporting (grouped)** — Medium postmortem https://medium.com/@sattyamjain96/the-agent-that-burned-4-200-in-63-hours-a-production-ai-postmortem-d38fd9586a85 (Apr 2026); FutureAGI runaway-cost guide https://futureagi.com/glossary/runaway-cost/; LeanOps https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/ (2026)
- CONFIRMS: documented incidents: $47K over 11 days (two agents in an infinite conversation loop, Nov 2025); ~$48K in 14 hours (Apr 2026 — retriever returned imperfect chunks, planner broadened queries forever because the success criterion "comprehensive citations" was **undefined**); $4,200/63-hour retry loop. Root cause is consistently *undefined termination/success criteria* + no per-run budget kill-switch — both solved by coded pipelines with explicit exit conditions and hard caps. Practitioner reports of 70–120x cost spikes on multi-step agents.
- NEW: the failure that costs the most is agent-to-agent loops (two LLMs re-prompting each other) — a mode a single-orchestrator design structurally cannot enter.

**18. Orchestrator anti-patterns** — TrueFoundry https://www.truefoundry.com/blog/multi-agent-architecture, DigitalApplied https://www.digitalapplied.com/blog/multi-agent-orchestration-5-patterns-that-work (2026)
- CONFIRMS: the god-agent orchestrator is now a *named* anti-pattern: it becomes a context-window bottleneck and single point of failure when it does reasoning-heavy work while coordinating; ~40% of agent projects fail on over-engineering. Guidance: measure task shape first, start with supervisor, add fan-out only for genuinely parallel work.

## E. Durable execution & resumability (2026's new subfield)

**19. Diagrid — "Checkpoints Are Not Durable Execution"** — https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows (Feb 25, 2026)
- CHALLENGES (a likely gap in any hand-rolled harness): checkpointing ≠ durability. LangGraph/CrewAI/ADK snapshot state but provide **no failure detection, no automatic resumption, no duplicate-execution protection** — a crashed process just sits there, and naive resume double-executes side effects. Durable execution means workflows run to completion without a human noticing the crash.
- CONFIRMS: linear workflow-engine-style code (persist at every await point, replay-based resume) is the recommended shape — a coded state machine is halfway there; the missing halves are a watchdog and idempotency keys.

**20. 2026 durable-agent reference architecture (grouped)** — Zylos https://zylos.ai/research/2026-04-24-durable-execution-agent-runtimes/ (Apr 24, 2026); inference.sh https://inference.sh/blog/agent-runtime/durable-execution
- CONFIRMS: consensus four-piece contract: checkpoint after every LLM call/tool result; resume from last checkpoint; retries with backoff; **idempotency keys on every state-writing tool call** tied to workflow state. Named engines: Temporal, Restate, DBOS, Inngest, Dapr Workflows.
- NEW: "From Chatbot to Digital Colleague" (https://arxiv.org/abs/2606.14502, June 2026, 20 authors) formalizes the academic version: persistent "Workspace + Skill" harnesses with state persistence, reusable procedures, task closure, and sandboxed auditable evaluation — the research community converging on what fleet-style harnesses already do.

---

## What the freshest evidence says a 2026 solo-founder fleet should do differently than 2025 wisdom

- **Shrink the judge panel; diversify it instead of enlarging it.** 2025 wisdom said "panel of judges beats one judge." May–July 2026 evidence (Nine Judges; Reliability-without-Validity) says frontier judges' errors are so correlated that 9 judges ≈ 2 effective votes and one good judge matches the panel. Spend the saved tokens on deterministic checks; run judges at temp 0, version-pinned, with *clean context* (Cognition's fresh-context reviewer result), and treat any judge-model swap as a recalibration event.
- **Don't put your smartest model in the orchestrator seat — put your code there.** The 2026 "Reasoning Trap" and god-agent findings invert 2025's "frontier model as lead agent" default: reasoning models degrade under coordination load, and the orchestrator (not the workers) is where failure concentrates. Coded state-machine coordination with the LLM doing only leaf work is now the evidence-backed default, and even Cognition's own revised position is single-threaded writes + agents that contribute "intelligence rather than actions."
- **Upgrade from checkpointing to actual durability.** The 2026 line (Diagrid, Feb 2026; Zylos, Apr 2026) is that saved state without a watchdog, automatic resume, and idempotency keys on side-effectful steps is theater — crashed runs go unnoticed and naive resumes double-fire. A solo founder can't be the watchdog; the harness needs failure *detection* plus idempotent replay, not just state files.
- **Kill-switches beat attribution.** Automated failure attribution is measurably unreliable (14.2% at finding the decisive error step, Who&When), so don't plan to debug cascades after the fact — make them structurally impossible: per-run token/dollar hard caps, explicit machine-checkable success criteria for every stage (every big 2026 cost incident traces to an undefined "done"), iteration ceilings, and no agent-to-agent conversational loops. Log *claims with evidence pointers* per stage (DRIFT) so the pipeline itself tells you which gate failed.
- **Gate hardest at the front, and re-benchmark models inside the harness.** Entropy work shows cascades are decided in the first round and disorder only accumulates on long horizons — so first-stage spec gates return more than late-stage review, and long-running lanes need periodic re-grounding against source-of-truth state. And because a model's solo benchmark says little about its multi-agent behavior (89% → 11% in one 2026 study), earned-autonomy promotion for a lane must be re-earned after any model swap, with escalation triggers in code — weaker models demonstrably cannot tell when to escalate themselves.