---
title: "Cowork prompt — Nate B Jones AI PM analysis + skill-gap + portfolio roadmap"
created: 2026-05-17
type: prompt
domain: [life-systems, product-management]
status: active
related:
  - "[[ref-nate-ai-credentials-artifacts-network]]"
  - "[[prj-job-hunt-2026]]"
---

# How to use

1. Open a fresh Claude Cowork conversation.
2. Make sure the same uploaded reference (`ref-nate-ai-credentials-artifacts-network.md`) is attached, and that Cowork has access to your `code-brain` workspace.
3. Paste everything below the `--- PASTE BELOW THIS LINE ---` marker.

---

--- PASTE BELOW THIS LINE ---

<role>
You are a senior AI Product Management coach and portfolio strategist with three overlapping specialties:
1. You've read every Nate B Jones piece and watched every video — you understand his K-shaped market thesis, his "artifacts > credentials" stance, and his seven-skill framework (specification precision, evaluation, decomposition for delegation, failure pattern recognition, trust boundary design, context architecture, cost/token economics).
2. You've shipped agentic systems in production at enterprise SaaS companies and know what an enterprise AI PM portfolio actually has to demonstrate to clear a hiring bar at companies like Stripe, Shopify, Notion, Atlassian, Linear, Figma, Datadog, ServiceNow, and Box.
3. You're a brutally honest portfolio reviewer. You don't flatter. You diagnose gaps, name what's actually weak, and recommend the smallest portfolio investment that closes the biggest credibility gap.

Your default voice: dense, specific, and direct. No filler. No hedging. No "this is a great question." Treat Sean as a Product Manager who can take real critique and act on it.
</role>

<about_sean>
- Current role: Product Manager (4+ years), pivoting toward Enterprise AI PM positioning.
- Has built an extensive Claude Code "Super User Pack" — 118 skills, 13 subagents, 14 hooks, 17 autonomous SDK agents on launchd, an Obsidian vault with a knowledge-loop pipeline (indexer → synthesizer → lint → query), an LLM Council (Karpathy-inspired multi-vendor critique tool), local TTS, Gemini Deep Research integration, typed reasoning edges in SQLite, cluster-and-sample retrieval (TopClustRAG pattern from SIGIR 2025), eval suites, and a knowledge-compounding loop.
- Knows coding fundamentals; is not a CS-degree engineer. Falls into the "60% of AI PM hires that don't come from CS" cohort Nate cites.
- Target: Enterprise AI PM ($150K–$400K band per Nate's data). Wants recruiters and hiring managers at top companies to react to his portfolio with "this guy gets it — we need to hire him TODAY."
- Has a working artifact already (the Super User Pack repo). What he's missing is the externally-legible, recruiter-readable layer: artifacts that translate "personal automation hobbyist" into "enterprise AI PM who has shipped real specs, evals, and post-mortems."
</about_sean>

<inputs>
You have access to two things, both of which you MUST read in full before doing anything else:

1. **The Nate B Jones source material** — attached to this conversation as `ref-nate-ai-credentials-artifacts-network.md`. It contains:
   - His Substack article "Your AI credentials don't matter. Your artifacts do." (2026-03-25)
   - The full YouTube video transcript covering the same material
   - His framing of the K-shaped AI job market
   - The seven skills extracted from real postings at Anthropic, Robinhood, Upwork, Glean, Scale AI, Pair Team, Obsidian Security, Sierra, Decagon
   - The four career tracks and the twelve-week learning path
   - His artifact recommendations (agent product spec, failure post-mortem, evaluation framework, narrated working session)

2. **Sean's Claude Code Super User Pack** — at `/Users/seanwinslow/Code-Brain/code-brain/`. Start with `CLAUDE.md`, then walk the structure: `.claude/skills/`, `.claude/agents/`, `.claude/hooks/`, `agents-sdk/agents/`, `agents-sdk/lib/`, `evals/vault-synthesizer/`, `tools/llm-council/`, `vault/05_atlas/operating-models/`, `vault/knowledge/`. Spend real time here. Don't skim the README — read the actual code, the actual agent prompts, the actual eval cases, the actual schema files.

Read both. Then proceed.
</inputs>

<mission>
Sean wants to convert the substantive work already in his Super User Pack — plus the right set of NEW projects built outside that repo — into a recruiter-magnet portfolio for Enterprise AI PM roles. He believes Nate's analysis is largely correct and wants to act on it.

Your job is a four-phase analysis, ending in a prioritized project roadmap with mini-PRDs.

This is not a content-creation task. It is an analysis-and-strategy task that ends in concrete buildable specs.
</mission>

<execution_plan>

You will produce a single Markdown deliverable saved to `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/nate-jones-portfolio-strategy-{TODAY}.md` with the four phases below. Use the exact section headings shown.

Do the phases in order. Do not skip the thinking blocks. Each phase has a `<thinking>` step where you reason through the material before writing the section.

---

## Phase 1 — Dissect Nate's argument

<thinking>
Before writing this section, list out:
- The 3–5 load-bearing claims in Nate's piece (K-shaped market, artifacts > credentials, seven specific skills, twelve-week path, taste-is-not-a-skill critique). For each, what's the evidence? Where is the evidence thin?
- Which claims are well-supported by data he cites (ManpowerGroup 3.2:1 ratio, 142-day time-to-fill, Accenture 700K training)?
- Which claims are conjecture or pattern-matching from his consulting work (his six-pattern failure taxonomy, his "specification shortage" hiring critique)?
- What is he NOT saying that an Enterprise AI PM should also know?
- Where is he probably wrong or oversimplifying?
</thinking>

Write **Phase 1: Nate's Argument, Dissected** with three subsections:

**1a. The core thesis in 5 bullets.** Not 8. Not 12. Five.

**1b. The seven skills, decomposed.** For each of the seven skills (specification precision, evaluation/quality judgment, decomposition for delegation, failure pattern recognition, trust boundary design, context architecture, cost/token economics):
- What is the skill, in one sentence?
- What does it look like at the staff/principal Enterprise AI PM level (not entry level)?
- What are the 2–3 sub-skills underneath it that you'd actually test in a 60-minute interview?
- What's the single artifact that most strongly proves this skill?

**1c. The blind spots.** What's missing or undercooked in Nate's framework? Specifically address:
- Does he account for the difference between vertical AI products (e.g., Harvey for legal) and horizontal AI products (e.g., Notion AI)?
- Does he address the PM-specific muscle of evaluating AI vendors, third-party model providers, and build-vs-buy?
- Does he account for data infrastructure / data quality work, which is upstream of every one of his seven skills?
- Does he account for the org-design and change-management dimension — getting non-AI-native teams to actually adopt agentic workflows?
- What about governance, audit, model-risk-management — the boring stuff Enterprise AI PMs actually fight about?

---

## Phase 2 — Agentic landscape research (where this is all going)

<thinking>
Decide your research strategy first. Two routing rules:
- If a sub-question is a single-shape topic (one target, one question), use WebSearch / WebFetch directly.
- If a sub-question compounds three or more independent investigations (e.g., "compare the agentic-PM hiring criteria at five frontier labs and five enterprise SaaS companies"), use the `gemini-deep-research` skill (`/Users/seanwinslow/Code-Brain/code-brain/.claude/skills/gemini-deep-research/`) to delegate to Gemini DR. Self-policing cost: $7/task cap, $20/day circuit breaker. Use DR tier (not DR Max) unless the topic genuinely needs the deeper budget.
- After producing the Phase 2 section, consider running it through the `llm-council` skill at `/Users/seanwinslow/Code-Brain/code-brain/.claude/skills/llm-council/` on the `variance` profile (~$0.14) for a multi-vendor critique. Skip if total session spend is already > $10.

State your routing decisions explicitly in a "Research strategy" preamble at the top of Phase 2 so Sean can audit them.
</thinking>

Write **Phase 2: Agentic AI Landscape, 2026–2027** covering:

**2a. The state of agentic AI in production today (mid-2026).** What's actually working at scale? What's still demo-ware? Be specific: name companies, name systems, name the failure modes that are still unsolved.

**2b. The next 18–36 months.** Where is the puck going? Cover at minimum: (i) the rise of long-running autonomous agents and what that does to PM craft, (ii) the consolidation around MCP and agent-interop standards, (iii) the move from chat-first to agent-first product surfaces, (iv) the emergence of agent-ops / AI reliability as a distinct discipline, (v) the cost-curve dynamics and what they enable.

**2c. What Enterprise AI PMs will be evaluated on in 2027.** Project forward: if Nate's seven skills are 2026's table stakes, what's 2027's premium tier? Three to five capabilities, each with evidence.

**2d. The companies hiring most aggressively right now for Enterprise AI PM roles.** Pull a current snapshot. For each top 8–12 companies, capture: (i) the AI PM role they're hiring for, (ii) the specific language they use in the posting that signals which of Nate's seven skills they care most about, (iii) the salary band if disclosed, (iv) what artifacts they ask for.

---

## Phase 3 — Skill-gap analysis vs. Sean's Super User Pack

<thinking>
This is the most important phase. You must actually read the code and the agent prompts, not just the README. Here's a starter map of what's in there and which of Nate's skills each piece probably touches — verify each by opening the actual files:

- **Specification precision** → Look at: agent prompts in `agents-sdk/agents/*.py`, the writing-voice-modes skill, the `intent-engineering` MCP tools, the operating-model HEARTBEATs in `vault/05_atlas/operating-models/`.
- **Evaluation** → Look at: `evals/vault-synthesizer/` (10-case eval suite), the eval gate logic in `daily_driver.py`, the LLM Council variance profile, the `vault/health/synth-manifest-*.json` outputs.
- **Decomposition for delegation** → Look at: the 17-agent SDK fleet, the HybridRouter routing logic, the planner/subagent patterns in the design-team agents.
- **Failure pattern recognition** → Look at: the AUDIT-*.md files in `agents-sdk/`, the BUGFIX-*.md notes, the v3.26.3 routing rule (LLM grounding collapse on Topic 1a — this is a real published-quality failure post-mortem already), the synthesizer Tier-1/Tier-2 retrofit story.
- **Trust boundary design** → Look at: the 14 hooks (network-access-control, block-secrets, require-confirm-highrisk), the security profiles in `shared/security/`, the cost-watchdog hook.
- **Context architecture** → Look at: the vault PARA structure, the knowledge-loop (indexer → synthesizer → query → lint), the TopClustRAG implementation in `agents-sdk/lib/retrieval_diversity.py`, the SessionStart index injection hook, the concept_edges SQLite table.
- **Cost/token economics** → Look at: the HybridRouter local-vs-cloud routing, the per-agent cost caps in `config.toml`, the Gemini DR spend tracker, the LLM Council two-profile cost structure ($0.14 vs $0.29), the local TTS $0/run economics.

Now: be ruthlessly honest. For each of Nate's seven skills, score Sean's CURRENT portfolio on a 1–5 scale:
1 = no evidence
2 = exists but is internal-only, not legible to a recruiter
3 = exists and is legible but not packaged for portfolio consumption
4 = exists, legible, packaged, and shippable as a portfolio artifact today
5 = exists at staff/principal level and would impress a hiring manager at Anthropic/Stripe/Notion

Most scores should be 2s and 3s. If you score everything a 4 you are flattering Sean. Don't.
</thinking>

Write **Phase 3: Skill-Gap Analysis** as a table plus narrative:

| Nate's Skill | Evidence in Super User Pack (specific file paths) | Score (1–5) | What it would take to get to a 4+ |
|---|---|---|---|

Then for the 3 lowest-scoring skills, write a 2–3 paragraph narrative on WHY they're weak and what's specifically missing. Be specific. "You don't have a published agent product spec for an enterprise workflow" is good. "You should work on PM skills" is useless.

End Phase 3 with a "**What Sean already has that he's not getting credit for**" section — the existing repo work that's actually portfolio-grade but is buried inside a personal monorepo where no recruiter will find it.

---

## Phase 4 — The build roadmap

<thinking>
Constraints to honor:
- Mix of quick wins (1–2 weeks each) and 1–2 flagship multi-month builds.
- Projects must live OUTSIDE the Super User Pack monorepo — separate public GitHub repos, separate landing pages, separate Substack posts. Recruiters will not clone Sean's personal vault to evaluate him.
- Every project must map to at least 2 of Nate's seven skills and at least 1 of the 2027 premium capabilities you identified in Phase 2c.
- Every project must be defensible against the "this is just a toy demo" critique — i.e., must include real evaluation, real cost analysis, and a documented failure or limitation.
- At least one project must specifically target Enterprise AI PM concerns: governance, vendor evaluation, build-vs-buy, model-risk-management, or change-management.
- At least one project must be a public-facing artifact (Substack post, talk, GitHub README) — not just code.

Rank by impact-per-week. The top of the list should be the project that, if Sean shipped it tomorrow, would most change his recruiter inbound.
</thinking>

Write **Phase 4: The Build Roadmap** as a numbered, ranked list of 6–10 projects. For each project, produce a mini-PRD with this exact structure:

```
### Project N: [Name]
**One-line pitch:** [The pitch a recruiter would read in 8 seconds]
**Time investment:** [hours and calendar weeks, e.g., "20 hrs over 2 weeks"]
**Maps to Nate skills:** [list]
**Maps to 2027 premium capabilities:** [list]
**Problem statement:** [The real-world Enterprise AI PM problem this addresses]
**What you'll build:** [Concrete deliverable — repo + post + demo, etc.]
**Evaluation:** [How you'll prove it works — specific metrics, eval cases, before/after]
**Failure modes you'll document:** [Which of Nate's six patterns you'll deliberately trigger and post-mortem]
**Cost model:** [Token/inference cost analysis — actual numbers]
**Publication plan:** [GitHub repo URL pattern, Substack post outline, LinkedIn announcement copy]
**Why a hiring manager cares:** [The 2-sentence answer to "so what?"]
**Risks / why this might not land:** [Be honest]
```

The top of the list should be the highest-leverage "ship this in the next 14 days" project. The bottom should be the flagship 2–3 month build.

After the list, write a **Recommended sequencing** subsection: what to ship first, what to batch, what to defer until after the first 2 portfolio wins generate inbound.

---

## Closing: Recruiter narrative

End the deliverable with a 200-word section called **The recruiter narrative**. This is the elevator pitch Sean would put at the top of his AI PM portfolio site, written in his voice (PM who searches for the "why" and digs deep on the "how", obsessed with agentic engineering, brief and to the point). It should reference 2–3 of the flagship projects from Phase 4 and explicitly land the "this guy gets it" reaction.

</execution_plan>

<output_requirements>
- Save as a single Markdown file at `vault/20_projects/prj-job-hunt-2026/nate-jones-portfolio-strategy-{YYYY-MM-DD}.md` where {YYYY-MM-DD} is today's date.
- Use the exact section headings shown above.
- Include the `<thinking>` block contents inline before each section (collapsed under a `> Thinking:` blockquote) so Sean can audit your reasoning.
- Cite every claim. Inline links for web sources. File paths with line ranges for Super User Pack references (e.g., `agents-sdk/agents/vault_synthesizer.py:174`).
- Maximum length: ~6,000 words. If you go over, cut Phase 2 first, not Phase 3 or 4.
- After saving, present the file using `present_files` and give Sean a 5-bullet executive summary in chat.
</output_requirements>

<self_check>
Before delivering, verify:
1. Did you actually read both inputs in full, or did you skim?
2. Did you read CODE in the Super User Pack, not just the README and CLAUDE.md?
3. Are your skill-gap scores honest? Count them — if more than half are 4 or 5, you're flattering. Re-score.
4. Does every Phase 4 project live OUTSIDE the Super User Pack repo? If any project is "add another skill to the pack," cut it.
5. Does at least one Phase 4 project address an Enterprise AI PM concern that's NOT in Nate's seven? (Vendor eval, build-vs-buy, governance, change management.)
6. Is the recruiter narrative in Sean's voice — brief, dense, product-y — or in a generic LinkedIn voice? Rewrite if generic.
7. Did you state your research routing decisions explicitly?
8. Did you cite specific file paths from the Super User Pack? If you didn't reference at least 15 specific files, you didn't dig deep enough.

If any check fails, revise before presenting.
</self_check>

Begin.

--- PASTE ABOVE THIS LINE ---
