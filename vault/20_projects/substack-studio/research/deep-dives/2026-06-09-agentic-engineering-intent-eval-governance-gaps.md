---
title: "Agentic Engineering — Intent / Eval / Governance Gaps in Creative/SaaS/UX/Marketing AI"
type: research
status: complete
domain: [creative-studio]
tags: [agentic-engineering, ai-agents, intent-engineering, evals, governance, human-in-the-loop, mcp-servers, market-gaps, voiceprint, last30days, research, opportunity]
created: 2026-06-09
last-updated: 2026-06-09
date-range: 2026-05-10 to 2026-06-09
sources: [reddit, x, youtube, web]
coverage: "Multi-pass: ~40 Reddit threads (with ScrapeCreators comments), ~30 X posts, ~10 YouTube videos (8 transcript-backed), ~30 web pages. Pass 1 (--deep) on 'biggest frustrations building AI agents' + Pass 2 (frameworks people wish existed / limitations) + Pass 3 (structured intent / human-in-the-loop / evals) + 4 WebSearch supplements."
tool: "/last30days v3.0 — 3 passes (8 queries) + WebSearch"
ai-context: "Agentic-engineering deepening of the creative-AI gap research, now built from the full three-pass plan the v1 (single-pass) report flagged as missing. Part 1 synthesizes the corpus along three axes — INTENT (make agents do what the human meant), EVAL (prove they did), GOVERNANCE (keep a human in control). Part 2 ranks gaps by frequency x unservedness with verbatim quotes, tagging each Sean-niche (judgment/intent/ownership, creative-team-facing) or NOT-Sean (orchestration/observability/memory/gate infrastructure = capital + eng play). The sharpened wedge from passes 2-3: existing eval tooling 'is designed for ML engineers' and 'most teams do not need research-grade evals first' — i.e. the gap is not 'no eval tools' but 'eval tools built for the wrong audience,' which is exactly the creative/non-engineer slice. Part 3 maps Sean-niche gaps to two SHIPPED MCPs — intent-engineering (@swins/intent-engineering-mcp; thesis: the audit IS the eval) and vault-knowledge (typed reasoning edges) — plus the writing chain, VoicePrint, and design-team agents. Part 4 is clean-sheet ideas biased toward gates and lenses, not generators. Confidence raised to medium (3 passes corroborate Gaps 1-2); the creative slice is still re-aimed from an engineer-skewed corpus — that skew held across all three passes, which is itself a finding. Feeds the combined opportunity report + Substack series."
related: [2026-06-09-claude-code-skills-mcp-gaps-and-opportunities, 2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days, 2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days, tool-shipping-playbook, voiceprint-plugin-build-spec]
---

# Agentic Engineering — Intent / Eval / Governance Gaps

> Research across a **three-pass `/last30days` sweep** (~40 Reddit threads with comments, ~30 X posts, ~10 YouTube videos / 8 transcripts, ~30 web pages), 2026-05-10 → 2026-06-09. Pass 1 `--deep` on *"the biggest frustrations building AI agents and agentic workflows"*; Pass 2 on *frameworks people wish existed / limitations*; Pass 3 on *structured intent / human-in-the-loop / evals*. Raw corpora saved under `~/Documents/Last30Days/`.
>
> This is the **agentic-engineering deepening** of the same niche covered by [[2026-06-09-claude-code-skills-mcp-gaps-and-opportunities]], [[2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days]], and [[2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days]]. Where those three asked *what creatives want*, this one asks *what makes the agents underneath them fail* — and which layer of that failure a solo creative-tools builder should actually touch.

## Quick verdict

The loudest frustration in agentic engineering is **statefulness** (memory/session loss) — but that is pure infrastructure and a funded race, not the opening. The real opening is one layer up and the three-pass sweep now says it out loud across multiple threads: **"correct behavior was never defined."** The systems half of agentic engineering (memory stores, tracing backends, orchestration frameworks, gate-firewalls) is taken or commoditizing; the **human-interface half — capturing what a human *meant* (intent), proving the agent *did it* (eval), and keeping a human *in the loop* (gates) — is wide open, and unaddressed for anyone who isn't a backend engineer.** Passes 2-3 sharpened the wedge: the eval gap is not "no tools exist," it's that the tools that exist *"[are] designed for ML engineers"* and *"most teams do not need 'research-grade evals' first."* Re-aimed at creative/SaaS/UX/marketing teams, the same three gaps aren't just unserved — nobody is pointing at them. Sean's shipped **[[intent-engineering]] MCP** ("the audit *is* the eval") sits directly on the #1 and #2 gaps; **[[vault-knowledge]] MCP** sits on the provenance edge of the memory gap.

---

# Part 1 — What people struggle with (the findings)

The corpus clusters cleanly onto the three-axis question. Organized by axis, with the overall #1 frustration (memory) noted as the backdrop everything else sits on.

## Backdrop — the #1 overall frustration is statefulness (and it's infra)

The single most-engaged thread in the window is titled **"Stop building AI agents"** ([r/AI_Agents, 1,556 upvotes / 342 comments](https://www.reddit.com/r/AI_Agents/comments/1taei9m/stop_building_ai_agents/)); its top comment (156 upvotes): *"This is the first post in this sub I actually agree with, and I build exactly the same — automations with LLM nodes."* The thread's verdict: *"The maintenance burden is what actually kills these projects."* On X, the highest-signal post in pass 1 names the daily version — [@ashwinhegde19](https://x.com/ashwinhegde19/status/2062581417037779323): *"One of the biggest frustrations in AI workflows is session fragmentation. You spend hours building context… and then start a new session only to re-establish that knowledge."* Pass 2 corroborated it in one viscerally-quoted line — **@Vegas_AI_Guy**: *"The thing nobody tells you about a long-running AI agent: it has no memory. Every session it wakes up blank. What persists isn't the model, it's the files the agent writes to itself and re-reads on boot."* And the most engineering-precise statement of *why* came from a YouTube transcript (*"Why AI Agents Keep Forgetting Things"*): *"These failures are often attributed to the limitations of the language model, yet stronger models continue to break on the exact same tasks. The breakdown usually stems from the infrastructure surrounding the model."*

**This is real and loud — but it is the infrastructure layer.** It belongs to memory stores, vector DBs, and "file-based memory" frameworks (mem0, MemZero). Note it; don't build it (see Part 2, NOT-Sean).

## Axis A — INTENT: agents do what was *said*, not what was *meant*

This is the quiet root cause underneath the noise, and pass 3 surfaced a thread that names it on the nose.

- The most on-the-nose post in the entire sweep — [r/AI_Agents, **"The missing layer in AI agents is not autonomy. It is structured intent"**](https://www.reddit.com/r/AI_Agents/comments/1te40dh/the_missing_layer_in_ai_agents_is_not_autonomy_it/) (22 comments). The title *is* the thesis of this report.
- The sharpest single insight in pass 1, from [r/AI_Governance, "Hot take: AI agents need observability before autonomy"](https://www.reddit.com/r/AI_Governance/comments/1tdp80k/hot_take_ai_agents_need_observability_before/): *"the deeper issue is that most teams don't know what to observe because 'correct behavior' was never defined."*
- The shift in where the work lives, stated repeatedly on X. **@FilipeNevola** (top X item of its pass): *"AI made it much easier to produce code. But producing code is not the hard part anymore. The hard part is deciding what should exist, why it should exist, which rules it needs."* **@levidehaan**: *"I spend the majority of my time thinking about what I want them to do."* **@ollobrains**: *"you are no longer typing every note. You are setting direction, tempo, constraints."*
- The failure mode named precisely (YouTube, ZNITLNX): agents *"will exploit any vague instruction like water leaking through cracks in concrete"* — e.g. *"it might build a login page that only accepts the exact word password because, well, you didn't explicitly tell it not to."* The X-native version: **@meghanatweets** — *"Why Your AI Code Agents Keep Veering Off Track (And How to Fix It)."*
- The only fix anyone proposes is to compile intent up front: *"interview mode, where the AI actually interrogates you first to uncover all your hidden requirements and technical constraints. It then translates your messy human desires into a hyper-strict markdown file,"* until *"the PRD becomes the absolute, undeniable law of the land."*
- And the most-upvoted distillation, from a 94-pt r/AI_Agents observations thread: *"'The agent is only as good as the environment around it' is probably the most underrated point here."*

## Axis B — EVAL: proving the agent did the thing (and the wedge: the tools are built for the wrong people)

Pass 3 made this the **most-discussed single topic** in the sweep — more distinct threads than any other subtopic.

- The thread that quantifies it — [r/aiagents, **"i asked 23 companies how they actually test their AI agents before shipping. the answers genuinely scared me"**](https://www.reddit.com/r/aiagents/comments/1tec4p9/i_asked_23_companies_how_they_actually_test_their/). The decisive reply, and the wedge for this whole report: *"The 17 out of 23 number tracks with what we see. The issue isn't laziness — it's that eval tooling like Braintrust and LangSmith is designed for ML engineers,"* and *"most teams do not need 'research-grade evals' first."*
- The blunt version — [r/AI_Agents, "if you're building ai agents without evaluating them you're shipping blind"](https://www.reddit.com/r/AI_Agents/comments/1u09wn3/if_youre_building_ai_agents_without_evaluating/).
- The despair version — [r/artificial, **"We kept improving the AI. Nothing changed."**](https://www.reddit.com/r/artificial/comments/1tx8pxi/we_kept_improving_the_ai_nothing_changed/) — the team with no way to *measure* whether the agent got better.
- The same question asked four different ways in one month: *"How are you testing your AI Agents?"* · *"Automated Regression Testing of Ai Agents."* · *"How to go about evaluation and Observability while building AI agents?"* · [*"For teams building AI agents: what failures are the hardest to debug?"*](https://www.reddit.com/r/LangChain/comments/1u0f6a8/for_teams_building_ai_agents_what_failures_are/).
- The default stance when no eval exists — [r/aiagents, "how much do you all actually trust autonomous AI agents"](https://www.reddit.com/r/aiagents/comments/1tprazu/how_much_do_you_all_actually_trust_autonomous_ai/): *"Zero. Verify everything if you can. All LLMs can hallucinate."*
- The sophisticated objection — [r/AISystemsEngineering, **"[D] Architectural mitigation of Goodhart's Law in autonomous AI coding agents"**](https://www.reddit.com/r/AISystemsEngineering/comments/1twfvtw/d_architectural_mitigation_of_goodharts_law_in/): evals get gamed the moment you optimize against them.
- The pragmatic production take, ["After 6 months running agents in production… the framework barely matters"](https://www.reddit.com/r/AI_Agents/comments/1tlgz6o/after_6_months_of_running_ai_agents_in_production/): *"Persistent memory, evals, and observability are three of the reasons people choose Mastra,"* and its top comment: *"Sooo…. basic software engineering right? Mapping requirements, guaranteeing auditability, control, consistency. Actually testing the technology before letting it in the wild."*
- The web names the failure exactly: agents *"can complete tasks without errors and exit cleanly, yet produce incorrect output — making this failure hard to catch since monitoring systems report everything is fine."* The math: an agent at 85% success across 8 steps completes the full workflow correctly only **~27%** of the time. Why eval is *hard*: behavior is *"non-deterministic by nature… difficult to snapshot a failure and replay it"* — the dev shorthand is **"ghost debugging."**
- The maturity reframe (YouTube, Celine Xu): stop asking *"why is it inconsistent"* and ask *"Could I tolerate this type of variance? Does the conclusion stay stable?"* — i.e. evals must distinguish acceptable *variation* from fatal *inconsistency*, which generic accuracy metrics can't.

**Every eval artifact in the corpus is a code test, built for ML engineers.** None of them evaluate "did it do what I *meant*" for non-code, subjective output — and the most-upvoted reply in the sweep says the existing tools are aimed at the wrong audience.

## Axis C — GOVERNANCE: keeping a human in control (the gate works; the workflow doesn't)

Pass 3 reframed this axis. The loudest governance posts aren't asking for a firewall — they're saying the human-in-the-loop *process* is broken or fake.

- [r/LangChain, **"Why your human in the loop approval step becomes the bottleneck nobody owns"**](https://www.reddit.com/r/LangChain/comments/1tvamu6/why_your_human_in_the_loop_approval_step_becomes/) — the approval gate as the thing that grinds the team to a halt.
- [r/artificial, **"I think 'human-in-the-loop' may become one of the biggest governance illusions in enterprise AI"**](https://www.reddit.com/r/artificial/comments/1td300k/i_think_humanintheloop_may_become_one_of_the/) (49 upvotes / 51 comments). Top comment: *"the supervision paradox is real when the watchers need watching but theyre also deciding what needs watching in first place."* And: *"ur governance layer is only as good as what the system decides to surface."*
- The visceral why — [r/AI_Agents, **"My agent emailed my boss at 3 AM — the 2-line human-in-the-loop guard that prevents dangerous tool calls"**](https://www.reddit.com/r/AI_Agents/comments/1txacie/my_agent_emailed_my_boss_at_3_am_the_2line/). And the production-database version (YouTube transcript): *"agents have ignored explicit commands to stop a destructive action during a code freeze, proceeding to delete production databases despite the instruction being clearly visible in the prompt history."*
- ["Hot take: AI agents need observability before autonomy"](https://www.reddit.com/r/AI_Governance/comments/1tdp80k/hot_take_ai_agents_need_observability_before/) is the rallying cry, with the caveat: *"Observability is necessary but not sufficient. It tells you what happened,"* and *"it's usually fine until you try to trace something back."*
- The human-in-control philosophy is asserted everywhere but tooled nowhere below enterprise: ZNITLNX — *"We set the guardrails. We write the initial prompt. We approve the final PRD,"* ending on *"have we simply become glorified validators for an endless swarm of highly capable yet deeply forgetful AI interns?"* The [MESSION fintech interview](https://www.youtube.com/watch?v=uphjHEpQWQg): *"responsible AI where the human stays in control"* — agents *"don't make the decision, they pull out all the necessary homework, and the human at the end of the day will decide."* The lecture-grade version (YouTube, "Agent Governance & Safety"): *"Capability without control becomes liability."*

**The tell for Part 2:** in a single 30-day window the sweep surfaced *three funded products* racing to own the gate *infrastructure* — **@michabbb** on ClawPatrol (Deno): *"a security firewall for AI agents… it sits between your agents and prod… and gates every action against rules you write"*; **@agentpmt**: *"embeds human-approval gates, per-agent budgets… Accountability isn't an afterthought, it belongs in the loop"*; **@TheKodeusLabs**: *"agent proposes, owner approves, chain records."* The gate engine is taken. The *who-owns-sign-off-and-how-it-doesn't-become-a-bottleneck* workflow is not.

---

# Part 2 — The gaps nobody is filling

> Ranked by **frequency in the corpus × how unserved it is.** Quotes verbatim. Each gap tagged **Sean-niche** (intent/eval/governance judgment, creative-team-facing — per the [[tool-shipping-playbook]] guardrail) or **NOT-Sean** (orchestration/observability/memory/gate infrastructure = capital + eng play). Confidence **medium**: three passes corroborate Gaps 1-2; the creative slice is re-aimed from an engineer-skewed corpus (the skew held across all three passes — see Methodology).

### Gap 1 — Nobody defines "correct" before launching (highest frequency × emptiest) — **Sean-niche**
The loudest *and* most fillable, now corroborated by a thread literally titled *"the missing layer… is structured intent."* *"Most teams don't know what to observe because 'correct behavior' was never defined."* Agents *"exploit any vague instruction like water leaking through cracks in concrete."* The only proposed fix is a coder PRD — and even its advocates admit the *definition* step is the missing one. Everything downstream (eval, gates) is impossible without it.
**Hard to build because:** the hardness is *human*, not systems — eliciting intent from someone who can't write a spec, and turning fuzzy taste into a checkable artifact. That's an interview-design + UX problem, which is exactly why it's solo-buildable and why no infra vendor will touch it. The trap: a thin "spec generator" that just reformats vague input is worthless; the value is in the elicitation and the audit.

### Gap 2 — Eval tools exist but are built for the wrong audience; agents pass clean but produce wrong output — **Sean-niche**
Highest *topic* frequency in the sweep, and the wedge sharpened in pass 3: *"eval tooling like Braintrust and LangSmith is designed for ML engineers,"* and *"most teams do not need 'research-grade evals' first."* The failure it has to catch: *"agents can complete tasks without errors and exit cleanly, yet produce incorrect output… monitoring systems report everything is fine."* The trio *"persistent memory, evals, and observability"* is named, but eval *infrastructure* is not a **spec-bound eval** that answers "did it do what I meant" in language a non-engineer can act on.
**Hard to build because:** the eval *is* the product — if it's hand-wavy it collapses to vibes, and *"ghost debugging"* (non-determinism) means you can't just diff one run against another. For subjective output (voice, brand, taste) there is no pass/fail test at all, and **Goodhart's Law** means any rubble you publish gets gamed. That unclaimed square — a judgment eval for subjective creative output, for non-ML-engineers — is the most defensible thing in this document.

### Gap 3 — The human-in-control gate is asserted, not tooled (for non-enterprise) — **Sean-niche (team slice) / NOT-Sean (enterprise compliance + gate infra)**
Everyone agrees the role is now *"we set the guardrails… we approve the final PRD"* and *"the human stays in control"* — but below enterprise that's philosophy, and where it *is* tooled, the tools fail socially: *"the approval step becomes the bottleneck nobody owns,"* and HITL risks becoming *"one of the biggest governance illusions."* The *enterprise/regulatory* version (EU AI Act, Singapore IMDA, *"we moved from PDFs to enforced policies in production"*) is a consultancy + big-co build → **NOT-Sean.** The *gate-engine* version (ClawPatrol/Deno firewall, AgentPMT budgets, Kodeus approval-chains) is a funded startup race → **NOT-Sean.** The **lightweight review/approval surface for a small team** — an editor-in-the-loop gate sized for a 5-person studio that's *fast enough nobody disables it* — is unbuilt → **Sean-niche.**
**Hard to build because:** a gate only survives if review is fast enough that people don't turn it off to get their "automation" back. The product is the *speed and clarity* of the human checkpoint, not the checkpoint itself — a UX problem the security-firewall vendors will never solve.

### Gap 4 — Session/intent continuity for non-coders — **Sean-niche (the artifact) / NOT-Sean (the store)**
*"Session fragmentation… start a new session only to re-establish that knowledge,"* and *"it has no memory. Every session it wakes up blank."* For a coder the answer is file-based memory (`agents.md`, the "3-file hack"). For a *creative*, the "context" that keeps getting lost is their **voice, taste, brand rules, reference universe** — and there is no portable artifact for that.
**Hard to build because:** the *storage* (vectors, memory servers) is commodity infra → don't build it. The *artifact* — a portable, human-authored voice/brand spec that survives every new session and doubles as the intent spec (Gap 1) and the eval target (Gap 2) — is the buildable, defensible slice.

### Gap 5 — Observability / tracing / replay backends — **NOT-Sean**
Loud (*"observability before autonomy"*) but **being served** by a funded field — teams are *"cobbling together LangSmith, custom logging, and a lot of hope,"* and *"snapshot a failure and replay it"* is a hard distributed-systems problem with deep pockets already in it. High frequency, low unservedness. Skip.

### Gap 6 — Memory / state persistence / cost tracking — **NOT-Sean**
The #1 *overall* frustration, but pure infra: *"you don't have state persistence, cost tracking, and basic data storage."* The web prices the wrong version at *"$15K–$50K annually on vector stores, $200K+ re-architecting at scale,"* and mem0/MemZero are funded races. That's a platform, not a solo product.

### Gap 7 — Agent gate-firewalls / per-agent budget + audit backends — **NOT-Sean** *(new in passes 2-3)*
Three funded products appeared in one window (ClawPatrol/Deno, AgentPMT, Kodeus). *"a security firewall for AI agents… gates every action against rules you write."* Wire-level gating, sandboxing, budget enforcement, and audit logs are VC + platform territory. High frequency, dropping unservedness fast. Skip the engine; the *human workflow on top* is Gap 3's Sean-niche slice.

### Gap 8 — Another agent framework / orchestration engine — **NOT-Sean**
The highest-engagement production thread's whole thesis is *"the framework you pick barely matters."* Building another loses by definition. Orchestration = Zapier / n8n / LangGraph territory = capital play.

### Overlap flag (don't repeat the sibling reports)
Gaps 1–4 here are the **agentic-engineering root cause** of the creative-facing gaps already documented in [[2026-06-09-claude-code-skills-mcp-gaps-and-opportunities]] (its Gap 2 "write like me," Gap 3 "brand-lock," Gap 4 "trustworthy workflows," and build idea #7 "Approval-Gate Publisher"). That report asked *what creatives want*; this one supplies the *why it keeps failing* — the intent→eval→gate chain — and adds the **intent-spec layer** and the **"eval tools built for the wrong audience" wedge** the skills/MCP report didn't cover. Read them together, not separately.

---

# Part 3 — How Sean is positioned

> Mapped to **shipped** assets, leading with the two MCPs. Do not read capabilities into these beyond what's listed.

## Priority 1 — Point the [[intent-engineering]] MCP straight at Gap 1 + Gap 2 (the flagship fit)
The corpus's #1 and #2 gaps — *"the missing layer… is structured intent"* / *"correct behavior was never defined"* and *"passes clean but wrong"* — are the exact problem the intent-engineering MCP already addresses. Its three tools (`audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`) operationalize **"evals are the new PRDs,"** and its thesis — **the audit *is* the eval**: it scores a spec against the framework *before* that spec ships to a coding agent — is a direct answer to *"the PRD becomes the absolute, undeniable law of the land"* and to ZNITLNX's *"spec compliance reviewer sub-agent."*
- **Action:** position intent-engineering not as a dev tool but as the **define-correct-before-you-build** layer. The two landing-page quotes the market handed us: *"The missing layer in AI agents is not autonomy. It is structured intent"* and *"eval tooling like Braintrust and LangSmith is designed for ML engineers."* The scaffold tool answers Gap 1 (capture intent); the audit tool answers Gap 2 (prove the spec is checkable before a single token is spent) — for the *non-ML-engineer* the existing eval vendors ignore.
- **Honest risk:** today it's framed/packaged for engineers (npm `@swins/intent-engineering-mcp`, MCP registry). The creative-team translation — an interview front-end that emits a spec a non-coder can read — is *not yet built*, and that front-end is the hard, defensible part (Gap 1's elicitation problem). Without it, this stays a dev tool.

## Priority 2 — Use [[vault-knowledge]] MCP for the provenance edge of Gap 4 — **only the defensible slice**
The memory frustration is infra (NOT-Sean), but vault-knowledge owns the *one* part that isn't commodity: **typed reasoning edges** (`concept_edges`: supports / contradicts / evolved_into / supersedes / depends_on / related_to). A vector store answers "what's similar"; typed edges answer "what *contradicts* what, and what *superseded* it" — the missing layer when an agent's compacted summary loses the thread.
- **Action:** frame vault-knowledge as **decision/provenance memory**, not "another memory server" — the thing that lets a human see *why* the agent believes something and trace it back (Gap 3's *"it's usually fine until you try to trace something back"*).
- **Honest risk:** adjacent to the funded memory-infra race (Gaps 5/6). Stay on the typed-edges + provenance differentiator; do not drift into building a general memory store.

## Priority 3 — The writing chain + design-team agents are already the *gate* pattern (Gap 2 + Gap 3 team-slice)
The corpus keeps reinventing "submit homework to a reviewer sub-agent / human approves." Sean already shipped that pattern as judgment gates: the writing chain ([[writing-critique]] → [[writing-humanity-pass]]) is a **spec-bound eval for prose** (it scores against a voice spec — exactly the "did it do what I meant" eval the market lacks *for non-engineers*), and the design-team agents (Design System Enforcer, Visual Polish Auditor) are **brand/quality gates for UI.**
- **Action:** market these as the creative-native answer to *"glorified validators"* and *"the approval step nobody owns"* — the review step *is* the product, sized for a studio not a bank. [[voiceprint-plugin-build-spec|VoicePrint]] is the productized version of the whole loop: interview → emit a voice spec (Gap 1) → that spec is the eval target (Gap 2) → human approves before ship (Gap 3).
- **Honest risk:** subjective evals are the hardest item — if the score is vibes, it dies at "less-robotic-average" like the 16-install humanize skills the sibling report flagged. Lead with the Cheese-Gauntlet eval as *proof it held*, not vibes. Goodhart's Law applies to your own rubric too.

## The throughline
Sean is well-positioned for the **judgment / intent / ownership** half of all three axes and badly positioned for the **memory / tracing / orchestration / gate-firewall** half — and three passes confirm the valuable half is the human-interface one. The asset he already owns (intent-engineering: *the audit is the eval*) is sitting on the loudest, emptiest gap in the dataset, and the market just told us the incumbents are *"designed for ML engineers."* The work is **translation**, not new capability: take the engineer-framed intent→eval→gate loop and re-skin it for the writers, designers, and marketers the agent ecosystem ignores.

---

# Part 4 — What to build (clean-sheet ideas)

> Grounded only in the gaps above. Bias: **gates and lenses, not generators** — the market is flooded with generation and starved of intent, proof, and control. Each names its gap and the genuinely hard part. All are creative/SaaS/UX/marketing-facing, not framework-author-facing.

### 1. Intent Interview → Spec Compiler (for people who can't write a PRD)
**Gap 1.** A guided interview that interrogates a non-technical creator about hidden requirements (audience, voice, brand non-negotiables, what "wrong" looks like) and emits a checkable spec an agent must obey — the *"interview mode → hyper-strict markdown"* pattern, built for a marketer instead of a coder. Natural front-end for the [[intent-engineering]] MCP's `generate_intent_spec_scaffold`.
**Hardest part:** the elicitation. Getting useful intent out of someone who says "make it pop" is the unsolved 80%; reformatting their words is the easy 20%.

### 2. Spec-Bound Eval Card — "did it do what I *meant*?" (for non-ML-engineers)
**Gap 2.** Score any agent output against the intent spec from #1 and return a pass/fail card with the specific clauses it violated — the creative-native version of *"verify against the original PRD success criteria,"* explicitly *not* "designed for ML engineers." For prose this is the [[writing-critique]] analyzer; the build is generalizing it to briefs, landing pages, and campaigns.
**Hardest part:** the eval *is* the product — for subjective output you need a measurable rubric or it collapses to vibes; non-determinism ("ghost debugging") means single-run scores need confidence bands; and Goodhart's Law means the rubric must resist being gamed.

### 3. Drift Lens — show me where it stopped sounding/looking right
**Gap 2 + Gap 4.** Span-by-span highlighting of where output diverged from the target voice/brand spec, so a creator fixes the three spans that broke instead of rewriting the whole thing. A lens, not a generator.
**Hardest part:** defining "drift" measurably without a large labeled corpus of the target voice.

### 4. Lightweight Approval Gate for small creative teams
**Gap 3 (team slice).** Generated content can't ship until it clears a human checkpoint plus voice/brand/fact gates — the editor-in-the-loop, sized for a studio, not a bank. The honest answer to *"the human stays in control"* and the direct fix for *"the approval step becomes the bottleneck nobody owns."*
**Hardest part:** review has to be *fast* or people disable it to get their automation back. The product is the speed of the checkpoint, not the checkpoint — the exact thing the ClawPatrol/AgentPMT gate-engines don't address.

### 5. Portable Voiceprint File — the intent artifact that survives every session
**Gap 4.** One human-authored, portable file that *is* the intent spec (Gap 1), the eval target (Gap 2), and the thing the human approves (Gap 3) — the creative answer to *"session fragmentation"* and *"wakes up blank."* This is [[voiceprint-plugin-build-spec|VoicePrint]] reframed as the cross-cutting fix for all three axes at once.
**Hardest part:** the file has to demonstrably hold a voice longer than a prompt does, with a score that proves it — or it's just another preset.

### 6. Provenance Trace for creative decisions
**Gap 3 + Gap 4, via [[vault-knowledge]].** "Why did the agent write/design it this way?" — a traceable chain back to the brand rules and prior decisions, using typed edges (`supports` / `contradicts` / `supersedes`). Answers *"it's usually fine until you try to trace something back"* for non-engineers.
**Hardest part:** capturing decision rationale at generation time without making the creator do bookkeeping.

**Pattern across all six:** every buildable win is a **gate or a lens** that sits on the intent→eval→control chain — define what "right" means, prove it, keep the human deciding. None is a generator, none is infrastructure, and none requires capital Sean doesn't have. The two MCPs already cover the spine (intent-engineering = define + audit; vault-knowledge = provenance); the rest is the creative-facing front-end the engineer ecosystem won't build.

---

## Methodology & sources

- **Tool:** `/last30days v3.0`. **Three passes, 8 queries + 4 WebSearch supplements**, 2026-05-10 → 2026-06-09. Pass 1 (GENERAL, `--deep`): *"the biggest frustrations building AI agents and agentic workflows."* Pass 2: *"AI agent frameworks people wish existed / framework limitations frustrations / LangChain CrewAI AutoGen problems / what is still missing."* Pass 3: *"structured intent specs / human-in-the-loop approval gates governance / how do you evaluate-test-prove AI agents."* This completes the three-pass plan the v1 (single-pass) report flagged as missing.
- **Sources (combined):** Reddit ~40 threads with ScrapeCreators comments (r/AI_Agents, r/artificial, r/AI_Governance, r/aiagents, r/LangChain, r/AISystemsEngineering, r/GithubCopilot, r/AIforOPS), X ~30 posts, YouTube ~10 videos / 8 transcripts, Web ~30 pages (VentureBeat, MLflow, Towards Data Science / Towards AI, mem0, Oracle, SitePoint, Turion, Zylos, Microsoft Agent Framework devblog, iii.dev, LangChain, daily.dev, Arsum, Inovabeing, DEV, arXiv). Raw dumps under `~/Documents/Last30Days/` (pass slugs: `the-biggest-frustrations-building-ai-agents-…`, `ai-agent-framework-limitations-frustrations-…`, `langchain-crewai-autogen-problems-…`, `building-ai-agents-what-is-still-missing-…`, `structured-intent-specs-…`, `human-in-the-loop-agent-approval-gates-…`, `how-do-you-evaluate-test-prove-ai-agents-…`).
- **Top voices:** the *"structured intent"* and *"23 companies / 17 don't test"* threads (the two load-bearing finds); [@ashwinhegde19](https://x.com/ashwinhegde19/status/2062581417037779323) and @Vegas_AI_Guy (session/memory); @FilipeNevola, @levidehaan, @ollobrains (intent-as-the-work); ClawPatrol/@michabbb, @agentpmt, @TheKodeusLabs (the funded gate-infra race); ZNITLNX and the *"Why AI Agents Keep Forgetting Things"* transcript (failure mechanics).
- **Confidence: medium** (raised from medium-low on the single-pass v1). (1) Three passes now corroborate Gaps 1-2 — the *"structured intent"* thread and the *"eval tools designed for ML engineers"* reply independently confirm the intent→eval thesis the v1 inferred. (2) The corpus stayed **engineer-skewed across all three passes** — no creative/SaaS/UX/marketing-specific source surfaced even when queried sideways. That is itself a finding (the creative version of these gaps is invisible to *both* the infra builders and the creative community), but it means the creative slice is still **re-aimed from engineer-voiced gaps, not directly observed** — same caveat as the sibling reports. (3) Reddit/X/YouTube quotes are verbatim; web findings are search-synthesized and attributed by publication. To harden the creative slice specifically: run the optional team-adoption pass (*"how creative and marketing teams are adopting AI agents"*) — it's the one query that would test the translation directly.
- **Related:** [[2026-06-09-claude-code-skills-mcp-gaps-and-opportunities]], [[2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days]], [[2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days]], [[tool-shipping-playbook]], [[voiceprint-plugin-build-spec]], [[intent-engineering]], [[vault-knowledge]].
