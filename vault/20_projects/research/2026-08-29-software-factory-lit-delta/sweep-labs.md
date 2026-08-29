# Sweep — Anthropic + OpenAI first-party writing (2026-08-29)

Research-agent sweep, 10 pieces read (WebFetch; two in full raw text — pieces 8 and 9,
whose quotes are verbatim beyond doubt). Feeds the 2026-08 delta synthesis; complements
`2026-08-08-software-factory-lit-review/sweep-anthropic.md` and `sweep-openai.md`.

---

## PIECE 1 — Building Effective Agents (Anthropic, 2024-12-19)

**URL:** https://www.anthropic.com/engineering/building-effective-agents
**CLASSIFICATION:** Vendor-guidance (foundational taxonomy, distilled from customer deployments)

- Workflows vs. agents: "Workflows are systems where LLMs and tools are orchestrated through predefined code paths. Agents are systems where LLMs dynamically direct their own processes."
- Orchestrator-workers: "A central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results."
- Evaluator-optimizer (origin of the judge role): "One LLM call generates a response while another provides evaluation and feedback in a loop."
- Simplicity wins: "The most successful implementations weren't using complex frameworks or specialized libraries."
- Cost is a design axis: "Agentic systems often trade latency and cost for better task performance."

**Adopt:** simple composable patterns; complexity only when it measurably helps. **Beware:** frameworks that "obscure the underlying prompts and responses"; autonomous agents without sandboxed testing + guardrails. **Evals:** unstated as infrastructure.

## PIECE 2 — How we built our multi-agent research system (Anthropic, 2025-06-13)

**URL:** https://www.anthropic.com/engineering/multi-agent-research-system
**CLASSIFICATION:** Practitioner-testimony (production system, named failures)

- Multi-agent beat single-agent "by 90.2% on research eval" (Opus 4 lead + Sonnet 4 subagents).
- "multi-agent systems use ~15× more tokens than chats"; token usage explains ~80% of performance variance.
- Lead agent plans and spawns 2–10+ parallel subagents with "specific research objectives, output formats, tool guidance, task boundaries"; separate CitationAgent.
- "Upgrading to Claude Sonnet 4 is a larger performance gain than doubling the token budget."
- Coding is the wrong fit: "Most coding tasks involve fewer truly parallelizable tasks than research."
- Tool-testing agent rewriting tool descriptions → "40% decrease in task completion time."

**Adopt (worked):** effort-scaling rules in prompts; parallel tool calling; end-state judging; ~20-query small eval sets; rainbow deployments; checkpoints; full production tracing. **Beware (failed):** 50 subagents for simple queries; endless searching for nonexistent sources; vague delegation → duplicated work; SEO farms over authoritative sources; synchronous blocking; cascading state errors.

**Evals:** BOTH — single-rubric LLM judge (0.0–1.0 + pass/fail) pre-deploy, production tracing + human eval as monitors.
**Roles/mixing:** orchestrator (Opus) / workers (Sonnet) / specialist validator (CitationAgent) / separate judge. Model mixing as explicit cost discipline.

## PIECE 3 — Best practices for Claude Code (Anthropic, living doc; read in full)

**URL:** https://code.claude.com/docs/en/best-practices
**CLASSIFICATION:** Vendor-guidance grounded in internal-team practice

- "Claude's context window fills up fast, and performance degrades as it fills."
- Verification is the central move: "Give Claude a check it can run... It's the difference between a session you watch and one you walk away from." Without one, "you become the verification loop."
- Escalating gate hardness: prompt check → `/goal` per-turn condition → Stop hook that "blocks the turn from ending until it passes" → verification subagent: "a fresh model try to refute the result, so the agent doing the work isn't the one grading it."
- Writer/Reviewer separation: "A fresh context improves code review since Claude won't be biased toward code it just wrote."
- Fan-out: `/batch` splits work "across 5 to 30 subagents. Each subagent works in its own worktree and opens a pull request."
- "Have Claude show evidence rather than asserting success."

**Beware:** "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"; correcting more than twice; judge inflation: "A reviewer prompted to find gaps will usually report some, even when the work is sound... Chasing every finding leads to over-engineering."
**Evals:** gates, concretely (Stop hooks block completion). **Roles:** doer/grader separation; per-subagent model choice (e.g. `model: opus` for security reviewer).

## PIECE 4 — Writing effective tools for agents (Anthropic, 2025-09-11)

**URL:** https://www.anthropic.com/engineering/writing-tools-for-agents
**CLASSIFICATION:** Practitioner-testimony, guidance-shaped

- Eval-driven tool development; agent self-optimization from its own transcripts beat "manually written expert implementations."
- Concise response formats cut token consumption ~two-thirds; resolve UUIDs to "semantically meaningful and interpretable language."
- Descriptor refinement alone: Sonnet SOTA on SWE-bench "after precise descriptor refinements."

**Beware:** thin API wrappers "without considering agent affordances." **Evals:** gates in the dev loop. **Roles:** agent-as-tool-optimizer — a factory maintenance role distinct from orchestrator/worker/judge.

## PIECE 5 — Demystifying evals for AI agents (Anthropic, 2026-01-09)

**URL:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
**CLASSIFICATION:** Practitioner-testimony (deployment lessons codified)

- Agents act over turns and mutate state; "mistakes can propagate and compound."
- Grade the world, not the words: "The outcome is the final state in the environment at the end of the trial."
- "20-50 simple tasks drawn from real failures is a great start"; eval-driven development — build evals before the agent fulfills them.
- "pass@k measures the likelihood that an agent gets at least one correct solution in k attempts"; pass^k for consistency-critical agents.
- "LLM-as-judge graders should be closely calibrated with human experts"; judge needs an "Unknown" out.
- Grading bugs dominate: fixing a rigid grader moved Opus 4.5's CORE-Bench from 42% to 95%.

**Beware:** rigid path-checking ("agents regularly find valid approaches that eval designers didn't anticipate"); saturated evals; shared state between runs.
**Evals:** explicitly BOTH — CI/CD gates as "first line of defense"; production monitoring "catches issues that synthetic evals miss."

## PIECE 6 — Effective Context Engineering for AI Agents (Anthropic, 2025-09-29)

**URL:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**CLASSIFICATION:** Vendor-guidance

- "Context rot"; finite "attention budget" (n² attention costs).
- Compaction near limits; sub-agents as a context-management device justified from token economics.
- Just-in-time retrieval via "lightweight identifiers (file paths, URLs, queries)."

**Beware:** brittle prompt logic; bloated overlapping toolsets; over-aggressive compaction. **Evals:** unstated.

## PIECE 7 — How Anthropic teams use Claude Code (Anthropic, 2025-07-24)

**URL:** https://claude.com/blog/how-anthropic-teams-use-claude-code
**CLASSIFICATION:** Practitioner-testimony (internal usage survey, marketing-adjacent packaging)

- Autonomous write-test-iterate loops (product design); security incidents "resolve 3x as quickly"; non-engineers ship software (legal phone-tree prototype).
- Cross-team pattern: "human review checkpoints... rather than blindly accepting."

**Evals:** informal gates (tests-in-loop, periodic human checkpoints).

## PIECE 8 — A Practical Guide to Building Agents (OpenAI, 2025-04; PDF read in full — quotes verbatim)

**URL:** https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
**CLASSIFICATION:** Vendor-guidance (customer-deployment distillation, enterprise-audience)

- Model cost procedure: "build your agent prototype with the most capable model for every task to establish a performance baseline. From there, try swapping in smaller models"; step 1 is "Set up evals to establish a performance baseline."
- Single-agent first: "Our general recommendation is to maximize a single agent's capabilities first."
- Two multi-agent patterns: Manager (agents as tools) and Decentralized (handoffs).
- Split triggers: "many conditional statements"; tool overload — "Some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools."
- Layered concurrent guardrails: LLM classifiers (relevance/safety/PII) + moderation + rules-based (blocklist, regex) + tool risk ratings by reversibility and financial impact.
- Human-in-the-loop triggers: "Exceeding failure thresholds" and "High-risk actions."

**Beware:** "it's tempting to immediately build a fully autonomous agent with complex architecture — customers typically achieve greater success with an incremental approach"; DSL-heavy graph frameworks.
**Evals:** gates lightly specified — evals license model downsizing; guardrails as runtime gates. **Roles/mixing:** cheap-validator/expensive-doer split (gpt-4o-mini guardrail classifiers).

## PIECE 9 — Harness engineering: leveraging Codex in an agent-first world (OpenAI, 2026-02-11; full text — quotes verbatim)

**URL:** https://openai.com/index/harness-engineering/ — Ryan Lopopolo
**CLASSIFICATION:** Practitioner-testimony — the strongest factory specimen in either corpus: 5 months, ~1M lines, ~1,500 PRs, 3→7 engineers, real internal users.

- "Every line of code—application logic, tests, CI configuration, documentation, observability, and internal tooling—has been written by Codex... in about 1/10th the time." "3.5 PRs per engineer per day."
- Job redefinition: "a software engineering team's primary job is no longer to write code, but to design environments, specify intent, and build feedback loops." On failure: "the fix was almost never 'try harder.'"
- Agent-to-agent review: Codex must "review its own changes locally, request additional specific agent reviews both locally and in the cloud... and iterate in a loop until all agent reviewers are satisfied." "Humans may review pull requests, but aren't required to."
- Context: "give Codex a map, not a 1,000-page instruction manual." Big AGENTS.md failed — "When everything is 'important,' nothing is"; "It rots instantly." ~100-line AGENTS.md as ToC over versioned docs/ tree; "Plans are treated as first-class artifacts."
- Legibility: "From the agent's point of view, anything it can't access in-context while running effectively doesn't exist" — Slack/Google-Docs decisions are invisible; everything in-repo.
- Architecture mechanically enforced: fixed layer graph + custom linters whose "error messages... inject remediation instructions into agent context." "This is the kind of architecture you usually postpone until you have hundreds of engineers. With coding agents, it's an early prerequisite."
- Merge philosophy inverts: "minimal blocking merge gates... corrections are cheap, and waiting is expensive. This would be irresponsible in a low-throughput environment."
- Entropy management: manual Friday cleanup "didn't scale" → in-repo "golden principles" + background Codex GC agents that "scan for deviations, update quality grades, and open targeted refactoring pull requests," mostly automerged; doc-gardening agent. "Human taste is captured once, then enforced continuously on every line of code."
- Autonomy: 6-hour unattended runs; per-worktree bootable app instances with CDP + LogQL/PromQL. Caveat: "should not be assumed to generalize without similar investment—at least, not yet."

**Beware:** underspecified environments; monolithic instruction files; pattern-replication drift ("Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones"); manual cleanup as a scaling strategy. Named open question: "how architectural coherence evolves over years in a fully agent-generated system."
**Evals:** BOTH, inverted — hard mechanical gates on architecture/invariants, deliberately minimal merge gates; background quality-grading agents as monitors.
**Roles:** workers, multiple named agent reviewers, doc-gardener, background GC agents, separate security agent (Aardvark), humans escalation-only. Cost currency = human attention, not tokens.

## PIECE 10 — Orchestrating Agents: Routines and Handoffs (OpenAI Cookbook, ~2024-10)

**URL:** https://developers.openai.com/cookbook/examples/orchestrating_agents
**CLASSIFICATION:** Vendor-guidance (educational)

- Routines: "a list of instructions in natural language... along with the tools necessary to complete them"; "The main power of routines is their simplicity and robustness."
- Handoffs via `transfer_to_XXX` functions; exists to solve single-agent bloat.
- Their own caveat: "Swarm... should not be directly used in production."

---

## NOT FETCHED / SKIPPED

- "How OpenAI uses Codex": key figures (engineers run "four and eight parallel agents"; ">90% of the Codex app's code generated by Codex itself") surfaced only in search snippets — treat as snippet-sourced, not page-verified. Piece 9 covers the ground first-party.
- Anthropic "How we're using Claude Code" appendix PDF: not separately fetched; Piece 7 is canonical.

## Cross-cutting synthesis (research agent)

1. **Convergent doctrine:** start single-agent; go multi only when instruction-following/tool selection breaks (OpenAI) or tasks parallelize beyond one context window (Anthropic).
2. **The two production testimonies disagree instructively on gates:** Anthropic pushes harder stop-gates (Stop hooks, adversarial review subagents); OpenAI's harness team *loosened* merge gates because throughput made corrections cheaper than waiting — but only after making architectural invariants mechanically unbreakable. Gate placement migrates from the merge to the linter.
3. **Judge separation is universal and universally flagged as fallible:** doer ≠ grader; calibrate against humans; grader bugs dominate (42%→95% CORE-Bench); reviewers over-report by construction.
4. **Cost discipline has two currencies:** tokens (15× chat; Opus-plans/Sonnet-executes; best-model-first-then-downsize; mini-model guardrails) and human attention (the binding constraint in OpenAI's harness).
5. **Repo-as-memory convergence:** short CLAUDE.md/AGENTS.md as map + on-demand docs; the monolithic instruction file fails identically at both labs.
