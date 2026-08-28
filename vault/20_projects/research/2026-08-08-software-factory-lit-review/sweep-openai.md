I have seven solid primary sources read in full. Here is the structured report.

# OpenAI Literature Sweep — Building & Operating Agent Fleets for Software Work

## 1. A Practical Guide to Building Agents (PDF, 34pp)
**URL:** https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf — undated in-body (published ~April 2025; references o1/o3-mini and Agents SDK launch)

- **ADOPT** — Model-selection loop: prototype every task with the most capable model to establish a baseline, then swap in smaller models per task and measure; principles are (1) set up evals first, (2) hit accuracy target with best models, (3) then optimize cost/latency by downgrading where evals stay green.
- **ADOPT** — Orchestration ladder: "maximize a single agent's capabilities first"; split into multiple agents only on two concrete triggers — complex conditional logic prompts can't hold, or **tool overload** ("some implementations manage 15+ well-defined distinct tools while others struggle with fewer than 10 overlapping tools" — overlap, not count, is the failure signal).
- **CONTEXT** — Two multi-agent topologies: **Manager (agents-as-tools)** — central LLM delegates via tool calls and synthesizes, best when one agent should own the user interaction; **Decentralized (handoffs)** — peers transfer full execution + conversation state one-way, best for triage where a specialist should fully take over.
- **ADOPT** — Guardrails as *layered defense*, run concurrently with optimistic execution (tripwire raises an exception mid-run): relevance classifier + safety/jailbreak classifier + PII filter + moderation + rules-based (blocklist, input length caps, regex) + output validation. Build order heuristic: data-privacy and content safety first, then add guardrails from real observed failures.
- **ADOPT** — **Tool risk ratings**: rate every tool low/medium/high on read-vs-write, reversibility, account permissions, financial impact; high-risk tools trigger pause-for-check or human escalation.
- **ADOPT** — Two canonical human-in-the-loop triggers: (1) **exceeding failure thresholds** (retry/attempt limits), (2) **high-risk actions** (irreversible, payments, cancellations) until reliability confidence is earned.

## 2. Harness Engineering: Leveraging Codex in an Agent-First World
**URL:** https://openai.com/index/harness-engineering/ — **Feb 11, 2026** (Ryan Lopopolo). The strongest single source for a software-factory.

- **CONTEXT** — Numbers: 5 months from empty repo → ~1M LOC internal product with **0 lines of manually written code**; ~1,500 PRs merged by 3 engineers driving Codex = **3.5 PRs/engineer/day**, throughput *rising* as team grew to 7; built in an estimated ~1/10th the hand-written time; single Codex runs work one task for **6+ hours** overnight.
- **ADOPT** — PR completion loop: agent reviews its own diff locally, requests additional agent reviews (local + cloud), responds to feedback, and iterates "until all agent reviewers are satisfied" (explicitly a Ralph-Wiggum loop). Humans *may* review but aren't required; review is pushed agent-to-agent.
- **ADOPT** — **AGENTS.md as table of contents, not encyclopedia**: the one-big-AGENTS.md approach "failed in predictable ways" (crowds out task context, everything-important = nothing-important, rots instantly, unverifiable). Instead: ~100-line map pointing into a structured `docs/` system of record (design-docs with verification status, exec-plans active/completed + tech-debt-tracker, product-specs, generated schema docs, llms.txt references) — progressive disclosure, enforced by linters/CI plus a recurring **doc-gardening agent** that opens fix-up PRs for stale docs.
- **ADOPT** — "Anything the agent can't access in-context effectively doesn't exist": Slack decisions and Google Docs are illegible; push all decisions/plans into repo-local versioned artifacts. Prefer "boring," composable, training-set-represented dependencies; sometimes reimplement small utilities in-repo (their map-with-concurrency helper) instead of importing opaque libraries.
- **ADOPT** — **Enforce invariants, not implementations**: rigid layer architecture (Types→Config→Repo→Service→Runtime→UI, cross-cutting only via Providers) enforced by custom Codex-written linters whose *error messages inject remediation instructions into agent context*. "With agents, constraints become multipliers."
- **ADOPT** — Entropy management: manual Friday "AI slop" cleanup (20% of the week) didn't scale; replaced with encoded "golden principles" + recurring background cleanup agents that scan for drift, update quality grades, and open small refactor PRs "reviewable in under a minute and automerged" — continuous garbage collection over burst paydown.
- **CAUTION** — Their own generalization warning: end-to-end autonomy (repro bug → record video → fix → validate → merge) "depends heavily on the specific structure and tooling of this repository and should not be assumed to generalize without similar investment." Also: minimal blocking merge gates are right *only* because agent throughput ≫ human attention makes corrections cheap — "irresponsible in a low-throughput environment."

## 3. How OpenAI Uses Codex (business guide)
**URL:** https://openai.com/business/guides-and-resources/how-openai-uses-codex/ — undated (2025; "research preview" era)

- **CONTEXT** — Seven internal use-case families across Security/Product/Frontend/API/Infra/Perf teams: code understanding, refactors/migrations, performance hunting, test coverage, velocity (scaffolds, rollout scripts), staying in flow (fire-and-forget drive-by fixes), exploration ("where else does this bug appear").
- **ADOPT** — Task-sizing rule: Codex works best on well-scoped tasks of **~1 hour of human work / a few hundred lines** — the load-bearing delegation granularity number.
- **ADOPT** — Two-step flow: Ask mode (plan) first, plan becomes input to Code mode — "keeps Codex grounded and helps avoid errors."
- **ADOPT** — Prompt like a GitHub issue: file paths, component names, diffs, doc snippets, and "implement this the same way it's done in [module X]."
- **ADOPT** — Iterate the *environment*, not just prompts: startup script, env vars, internet access "significantly reduces error rate"; treat recurring build errors as environment-config bugs.
- **CONTEXT** — Use the task queue as a lightweight backlog ("point Codex at low-coverage modules overnight, wake up to runnable unit-test PRs"; "merged 4 PRs from meetings"); Best-of-N parallel generations for hard tasks, cherry-pick/combine.

## 4. Eval-Driven System Design cookbook (receipt inspection)
**URL:** https://developers.openai.com/cookbook/examples/partners/eval_driven_system_design/receipt_inspection — 2025

- **ADOPT** — Evals as the *core development process*, not an afterthought: 7-phase flywheel (understand → assemble examples → V0 system → label + build evals → **map evals to business dollars** → improve → production QA). Started from only ~20 expert-labeled samples — deliberately small; "don't over-invest in prompt engineering before you have a benchmark."
- **ADOPT** — Three grader tiers matched to field type: string-check (exact fields), text-similarity with a 0.8 fuzzy threshold (names), score-model LLM-judge with explicit point rubrics (reasoning quality) — mix cheap deterministic and expensive judge graders per field.
- **ADOPT** — Dollar-denominated eval: cost model (audit cost $2, missed-audit cost $30, 1M receipts/yr) turned error rates into "$63K/yr" style figures, which *re-ranked work* — merchant-name accuracy was 15% but financially irrelevant; handwritten-X detection was worth ~$75K/yr. Prioritize by dollar impact, not accuracy deltas.
- **ADOPT** — Improvement waterfall in cost order: model choice → prompt tuning → few-shot/RAG → tools → accessory models → fine-tuning. Downgrading o4-mini → gpt-4.1-mini cut per-item cost ~3x ($0.01→$0.003) with *no* eval regression — evals are what make downgrades safe.
- **CAUTION** — Pipeline "telephone" failure mode: two-stage extract→decide systems fail when correct reasoning runs on bad extraction; eval each stage independently and conditionally to localize root cause.

## 5. Evaluation Best Practices (platform docs)
**URL:** https://developers.openai.com/api/docs/guides/evaluation-best-practices — current (2026)

- **ADOPT** — Five-step workflow: define objective → collect dataset (production traffic + expert-curated + synthetic + historical logs) → define metrics → run/compare → **continuous evaluation on every change, growing the set over time**.
- **ADOPT** — LLM-as-judge calibration: control for response length ("LLMs bias toward longer responses"), require chain-of-thought before scoring, use pairwise or pass/fail formats, and **validate judge agreement with human labels before switching to a cheaper judge model**.
- **CAUTION** — Named anti-patterns: eval sets that don't mirror production traffic; "vibe-based" / "it seems to be working" assessment; academic metrics (BLEU/perplexity) alone; delaying evals until deployment; never calibrating against human feedback.
- **CONTEXT** — Eval focus scales with architecture: single-turn → instruction-following + correctness; single-agent → add tool-selection precision; **multi-agent → add handoff accuracy** as a first-class metric.

## 6. Agents SDK — Orchestrating Multiple Agents
**URL:** https://openai.github.io/openai-agents-python/multi_agent/ — living docs

- **ADOPT** — Two orchestration modes: **via LLM** (agent plans and delegates — flexible, for open-ended tasks) vs **via code** (explicit routing — "more deterministic and predictable in speed, cost and performance"). For a production factory, prefer code-orchestration wherever the flow is known.
- **ADOPT** — Code patterns catalog: structured-output classification then conditional routing; deterministic chaining (research → outline → draft → critique → improve); **evaluator loop** — worker agent in a while-loop with a judge agent "until the evaluator says the output passes"; asyncio parallelization for independent subtasks.
- **CONTEXT** — Agents-as-tools when one agent must own the final answer and synthesize; handoffs when the specialist should respond directly and prompts should stay narrow.
- **ADOPT** — LLM-orchestration hygiene: invest in prompts describing tools/constraints, monitor and iterate from failure patterns, let agents self-reflect on errors, specialize rather than build generalists, and eval the orchestration itself.

## 7. Computer-Using Agent (CUA)
**URL:** https://openai.com/index/computer-using-agent/ — **Jan 23, 2025** (Operator later folded into ChatGPT agent, mid-2025)

- **CONTEXT** — Loop architecture: screenshot perception → chain-of-thought reasoning over current + past screenshots/actions → mouse/keyboard action, repeated to completion; benchmark reality check: OSWorld 38.1% vs human 72.4%, WebArena 58.1%, WebVoyager 87% — computer-use agents remain far below human on complex environments.
- **ADOPT** — Confirmation gates baked into the model: CUA pauses for user confirmation on sensitive actions (logins, CAPTCHA) — mirror this tier in any browser-driving automation.
- **CAUTION** — Prompt specificity swings reliability wildly on the *same task*: tagvenue booking went **8/10 → 3/10** success purely by removing UI hints and date specifics from the prompt. Repeated-simple-interaction tasks hit 10/10; unfamiliar UIs and text editing are weak spots.
- **CONTEXT** — Test-time scaling observed: success rate rises with more allowed steps — budget generous step limits for hard GUI tasks.

---

## What this implies for a solo founder running an agent fleet that builds and operates one product

- **Your job is harness engineering, not coding.** OpenAI's 3-engineers→1M-LOC result came from treating environment design as the product: repo-local docs as the *only* system of record, ~100-line AGENTS.md-as-map, custom linters whose error messages teach the agent, and per-worktree bootable app + logs the agent can read. Every hour spent making the repo legible to agents multiplies across all future runs — this is the highest-leverage investment a solo operator can make.
- **Delegate in ~1-hour chunks and close the loop agent-to-agent.** The working granularity is a well-scoped GitHub-issue-shaped task (~few hundred lines); drive each PR with a worker + agent-reviewer loop that iterates until reviewers pass, reserving your own attention for prioritization, acceptance criteria, and the two canonical HITL gates: retry-threshold breaches and high-risk/irreversible actions (deploys, payments, deletes — rate every tool low/med/high first).
- **Evals are the currency that buys both trust and cost cuts.** Start with ~20 labeled examples, mix cheap deterministic graders with calibrated LLM judges, and denominate failures in dollars (or hours) — that's what tells you which agent failures actually matter, and it's the only safe license to downgrade to cheaper models (a validated 3x cost cut in OpenAI's own example).
- **Budget for entropy as a standing agent, not a cleanup sprint.** Agent fleets replicate whatever patterns exist, good or bad; OpenAI burned 20% of human time on slop cleanup before converting taste into encoded "golden principles" plus scheduled janitor agents opening one-minute-reviewable refactor PRs. A solo founder should stand up the doc-gardener and drift-cleanup cron agents early — they're the difference between compounding and rotting.
- **Match autonomy to throughput and specify ruthlessly at the flaky edges.** Loose merge gates are only safe when agent throughput makes corrections cheap — earn that with the harness before relaxing gates; keep orchestration in code (deterministic routing, evaluator loops) rather than LLM-planned handoffs wherever flows are known; and for browser/GUI automation remember CUA's 8/10→3/10 swing on prompt specificity — vague instructions, not model capability, are usually the failure mode.