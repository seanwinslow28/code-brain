# Anthropic Engineering Literature Sweep — Agent Fleets for Real Software Work

All pages read in full via WebFetch (not just snippets). Sources ordered roughly by relevance to fleet operations.

## 1. How we built our multi-agent research system
**URL:** https://www.anthropic.com/engineering/multi-agent-research-system — **June 13, 2025**

- **ADOPT** — Orchestrator-worker topology: Opus 4 lead agent + parallel Sonnet 4 subagents beat single-agent Opus by **90.2%** on their internal research eval. Three factors explained 95% of performance variance: token usage (80% alone), tool-call count, and model choice.
- **CAUTION** — Token economics: agents burn ~**4x** the tokens of chat; multi-agent systems ~**15x**. Their explicit rule: only use multi-agent where task value justifies the spend, and it's a poor fit for most coding tasks (fewer parallelizable subtasks, shared-context needs).
- **ADOPT** — Explicit effort-scaling rules in the orchestrator prompt: simple fact-find = 1 agent / 3-10 tool calls; comparison = 2-4 subagents / 10-15 calls each; complex research = 10+ subagents. Without these, early prototypes spawned 50 subagents for trivial queries and duplicated work from vague task descriptions.
- **ADOPT** — Eval design: started with just **20 test cases**; single LLM-judge call with one rubric prompt (factual accuracy, citation accuracy, completeness, source quality, tool efficiency → 0-1 score + pass/fail) was more consistent than multi-judge setups. Human spot-checks still caught what the judge missed (e.g., SEO-content-farm bias).
- **ADOPT** — Subagents write outputs to filesystem and return summaries, rather than piping large results through the lead agent — reduces token copying and information loss.
- **CAUTION** — Production ops: non-deterministic long-running agents need checkpoints/resume (not restart-from-zero), full tracing, and "rainbow deployments" (gradual version shifts) because you can't atomically update agents mid-run. Synchronous subagent execution is a known bottleneck they hadn't solved.

## 2. Building Effective Agents
**URL:** https://www.anthropic.com/engineering/building-effective-agents — **Dec 19, 2024**

- **CONTEXT** — Canonical distinction: *workflows* (LLMs orchestrated through predefined code paths) vs *agents* (LLM dynamically directs its own process). Five composable patterns: prompt chaining, routing, parallelization (sectioning/voting), orchestrator-workers, evaluator-optimizer.
- **ADOPT** — Evaluator-optimizer (generator + judge loop) is recommended specifically when clear evaluation criteria exist and iteration measurably improves output — the validator/judge pattern's origin text.
- **CAUTION** — "Find the simplest solution possible": start with a single optimized LLM call + retrieval + examples; agents trade latency and cost for performance and can compound errors. Many patterns are "a few lines of code" — frameworks add abstraction that obscures prompts and invites unneeded complexity.
- **CAUTION** — Agents require sandboxed testing and guardrails; tool interface design deserves as much effort as human-computer interface design.

## 3. Claude Code best practices (engineering post, now the living docs page)
**URL:** https://www.anthropic.com/engineering/claude-code-best-practices → redirects to https://code.claude.com/docs/en/best-practices — **orig. April 2025, continuously updated**

- **ADOPT** — The #1 stated constraint: context window fills fast and performance degrades as it fills. Aggressive `/clear` between tasks; after two failed corrections, clear and rewrite the prompt rather than keep correcting — "a clean session with a better prompt almost always outperforms a long session with accumulated corrections."
- **ADOPT** — Give Claude a check it can run (tests, build exit code, screenshot diff): "it's the difference between a session you watch and one you walk away from." Escalation ladder: check-in-prompt → per-turn goal condition → deterministic Stop hook → fresh-context verification subagent. Demand evidence (test output) not assertions.
- **ADOPT** — Explore → plan → code → commit as the default workflow for non-trivial changes; skip planning when the diff fits in one sentence.
- **CAUTION** — Over-specified CLAUDE.md backfires: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions." Per-line test: would removing this cause mistakes? Move deterministic requirements to hooks, on-demand knowledge to skills.
- **ADOPT** — Scaling patterns: writer/reviewer split across two sessions (fresh context reviewer isn't biased toward code it just wrote); fan-out with `claude -p` over a generated task list with `--allowedTools` scoping; git worktrees for parallel isolated sessions.
- **CAUTION** — Adversarial reviewers "will usually report some gaps even when the work is sound, because that is what it was asked to do" — instruct reviewers to flag only correctness/requirement gaps, or you get over-engineering.

## 4. Effective context engineering for AI agents
**URL:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — **Sep 29, 2025**

- **CONTEXT** — "Context rot": recall accuracy drops as context tokens grow, across all models — the physics behind every other practice here.
- **ADOPT** — Three long-horizon techniques: (1) compaction — summarize, keep architectural decisions and unresolved bugs, drop redundant tool outputs (Claude Code keeps compressed context + 5 most-recent files); (2) structured note-taking to external files (agentic memory); (3) sub-agent architectures where a worker burns tens of thousands of tokens but returns only a **1,000-2,000 token** summary.
- **ADOPT** — Just-in-time retrieval: keep lightweight identifiers (paths, queries, links) in context and load data at runtime via tools rather than pre-loading.
- **CAUTION** — Tool bloat: "if a human engineer can't definitively say which tool applies, an agent can't do better." System prompts should sit at the right "altitude" — neither brittle if-else logic nor vague platitudes.

## 5. Effective harnesses for long-running agents
**URL:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents — **Nov 26, 2025**

- **ADOPT** — Two-phase harness: an *initializer* session sets up the environment (feature list, init.sh, git repo, progress file), then *coding* sessions each make one increment with structured handoffs.
- **ADOPT** — Feature list as JSON, not Markdown (models are less likely to inappropriately edit JSON), 200+ features each with testing steps and a status flag, all initially failing — plus an explicit instruction that removing/editing tests is unacceptable. This defeats "early victory declaration."
- **ADOPT** — Session-start ritual: `pwd` → read progress file → read feature list → review last ~20 git commits → run `init.sh` → run a basic end-to-end smoke test → pick ONE feature. One feature per session prevents context exhaustion mid-implementation.
- **ADOPT** — Forcing browser-automation testing "as a human user would" (not just unit tests/curl) dramatically improved bug-finding vs. self-reported completion.
- **CAUTION** — Blind spots persist: the agent couldn't see browser-native alert modals through its testing tool, so modal-dependent features were consistently buggier — know what your verification loop cannot observe.

## 6. Writing effective tools for AI agents — using AI agents
**URL:** https://www.anthropic.com/engineering/writing-tools-for-agents — **Sep 11, 2025**

- **ADOPT** — Eval-driven tool development: realistic multi-call tasks with verifiable ground-truth outcomes, run in a simple while-loop harness, tracking accuracy, runtime, tool-call count, tokens, errors. Then feed transcripts back to Claude Code to refactor the tools — Claude-optimized Slack/Asana MCP servers measurably beat human-written ones on held-out sets.
- **ADOPT** — Consolidate workflows into single tools (`schedule_event` not `list_users`+`list_events`+`create_event`); namespace with prefixes (`asana_search`) — prefix vs suffix naming had "non-trivial effects" on eval scores.
- **ADOPT** — Token-efficient responses: pagination/filtering/truncation with sensible defaults (Claude Code caps tool responses at **25,000 tokens**); a concise-format option cut Slack thread responses ~1/3 (72 vs 206 tokens); error messages should steer ("try a narrower query") not emit opaque codes.
- **CONTEXT** — Transcript reading found subtle failure modes, e.g. Claude "needlessly appending 2025" to search queries — fixed via tool description, not code.

## 7. Demystifying evals for AI agents
**URL:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents — **Jan 9, 2026**

- **ADOPT** — Start with **20-50 simple tasks drawn from real failures** (bug trackers, support queues, manual pre-release checks) — don't wait for hundreds; early on, effect sizes are large enough that small samples suffice.
- **ADOPT** — Grader hierarchy: prefer deterministic code graders where feasible; LLM graders for nuance but calibrate against humans and give them an "Unknown" escape valve; grade *outcomes*, never specific step sequences (agents find valid paths you didn't anticipate — Opus 4.5 "failed" a flight-booking eval by finding a policy loophole that was actually a better solution).
- **ADOPT** — Metrics: pass@k (at least one of k trials succeeds) for one-shot-value tasks; pass^k (all k succeed) for consistency-critical customer-facing agents — at 75% per-trial, pass^3 ≈ 42%. Split suites into *capability* evals (low pass rates, improvement signal) vs *regression* evals (near-100%, breakage alarm); capability evals lose signal above ~80% pass.
- **CAUTION** — Environment hygiene: trials must start from clean isolated state — Claude gained unfair advantages by reading git history left over from prior trials in some of their internal evals. 0% pass@100 usually means the task is broken, not the agent.
- **ADOPT** — Layer the methods: automated evals pre-launch/CI → production monitoring for drift → A/B tests at scale → weekly transcript reading. "Failures should seem fair" when you read transcripts.

## 8. How Anthropic teams use Claude Code (+ Agent SDK post)
**URLs:** https://www.anthropic.com/news/how-anthropic-teams-use-claude-code (→ claude.com/blog) — **Jul 24, 2025**; https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk — **Sep 29, 2025**

- **CONTEXT** — SDK post codifies the agent loop as **gather context → take action → verify work**, with three verification tiers: rules-based (linters/tests), visual (screenshots), LLM-as-judge (last resort, latency/cost).
- **ADOPT** — Internal numbers: security engineering resolves incident traces "3x as quickly"; inference team cut research time **80%** (~1hr → 10-20 min); growth marketing runs two specialized sub-agents to regenerate hundreds of ad variants in minutes; data-infra saved 20 min mid-outage by feeding dashboard screenshots to Claude.
- **ADOPT** — Cross-team pattern: checkpointed autonomy — autonomous loops (write code → run tests → iterate) with periodic human review — rather than fully hands-off; Claude as "thought partner," with TDD as the guide-rail for security-critical code.
- **CONTEXT** — Non-engineers (legal, marketing, data scientists without TypeScript) ship working internal tools — the fleet's leverage isn't limited to engineering tasks.

---

## What this implies for a solo founder running an agent fleet that builds and operates one product

- **Spend tokens like capital, not like air.** Multi-agent = ~15x token cost and is explicitly a poor fit for most coding work; default to a single well-contexted agent with subagents used only for parallelizable read-heavy research and fresh-context review — and encode effort-scaling rules ("simple task = 1 agent, N calls") so the fleet can't spawn its way into a bill.
- **Your leverage is the harness, not the model.** The long-running-agents playbook — JSON feature list the agent can't edit away, init.sh, one-feature-per-session, git commits + progress file, session-start smoke test — is exactly what lets one human walk away while sessions chain overnight. This is the difference between a fleet and a pile of chat windows.
- **Every agent needs a check it can run; keep the grader separate from the worker.** Tests, build exit codes, screenshot diffs, or a fresh-context reviewer that sees only the diff + criteria — and instruct reviewers to report only correctness gaps, or adversarial review manufactures over-engineering. Demand evidence, not "done."
- **20-50 evals from your own real failures beats zero evals waiting for a benchmark.** Split them capability vs regression, grade outcomes not steps, keep trial environments clean, and read transcripts weekly — as a solo operator, transcript reading IS your production monitoring team.
- **Prune context ruthlessly; write everything durable to disk.** Bloated CLAUDE.md gets ignored, long sessions degrade, and the fix is structural: hooks for must-happen rules, skills for on-demand knowledge, filesystem artifacts + compaction for continuity, subagents that return 1-2K-token summaries. The context window is the fleet's scarcest shared resource — architect around it, don't fight it.