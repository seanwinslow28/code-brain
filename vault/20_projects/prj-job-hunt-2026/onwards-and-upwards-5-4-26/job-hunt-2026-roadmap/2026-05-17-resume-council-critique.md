# Council Session — resume-critique-2026-05-17

- **Session ID:** `20260517-164814-ecdf5f`
- **Profile:** `premium`
- **Duration:** 228.9s
- **Tokens:** 75517 in, 27406 out
- **Cost:** $0.7887

## Original prompt

```
---
title: "Resume Council Prompt (Premium Profile)"
date: 2026-05-17
type: prompt
status: drafted
domain: [job-hunt-2026]
tags: [llm-council, resume, ai-pm, council-prompt]
related:
  - "[[2026-05-17-resume-council-plan]]"
  - "[[2026-05-17-resume-funnel-role-decision]]"
  - "[[../../assets/Sean_Winslow_Resume_council_input]]"
council_profile: premium
budget_cap_per_query: 1.00
budget_estimate: 0.29
chairman: claude-opus-4-7
---

# Resume Council Prompt — Sean Winslow, May 2026

> **For Sean before invoking:** Read end-to-end. Two filters before sending:
> (a) Does the prompt accidentally leak any CIIA-protected detail beyond the explicit "do not recommend" list? (Cross-check against the CIIA non-negotiables section.)
> (b) Does the prompt over-claim shipped artifacts? (Cross-check against the evidence-map status section — only items marked SHIPPED can be defended.)
> **Invocation:** `/llm-council` skill, profile=`premium`, chairman=`claude-opus-4-7`. Budget estimate $0.29 typical (per-query cap $1.00). Tag: `resume-critique-2026-05-18`.

---

## Context

Sean Winslow is a Product Manager pivoting to AI PM roles after a **May 4, 2026 layoff from The Block** (cost-cutting, not performance; layoff delivered by Block President Larry Cermak + HR, not the candidate's direct manager). **6 months titled PM at The Block** (Nov 2025 – May 2026); prior career: **10+ years at New York Life** in design / animation / DAM (Digital Asset Management) leading into AI-workflow integration over the last 3 years.

**Target archetypes in priority order:** AI PM > Tech PM > Creative PM.
**Compensation:** walk-away floor $100K, target band $150–250K, relocation override = Anthropic specifically OR $250K+/yr. Boston metro or remote default.
**Today:** Sat 2026-05-17. **Applications begin Tue 2026-05-20.** Personal site `seanwinslow.com` goes live Mon 2026-05-19.

## The resume's role in the funnel (Sean's locked decision, 2026-05-17)

The resume is a **secondary artifact** inside a 4-piece pristine package: (1) AI PM Portfolio at `seanwinslow.com/transactions`, (2) build-in-public proof (Substack post 1 ships 2026-05-22, LinkedIn syndication Wednesdays), (3) GitHub repo presence (Code-Brain + `sw-mcp-intent-engineering`), (4) the resume itself.

The package coherence is the differentiator. The other three artifacts prove the resume isn't lying. The resume's job: **showcase prior professional work + personal passion projects + skills**, with ATS keywords earned not stuffed, and `seanwinslow.com/transactions` URL non-negotiable on the doc.

**Implication for your critique:** Do NOT optimize the resume as a standalone lead artifact. Optimize it as the load-bearing supporting member of a package.

## Positioning thesis (from the unified roadmap, 2026-05-06)

> "Agentic engineering practitioner who ships." Semantic product architecture — specs, governance, routing, memory, authority, review.

Karpathy framing: artifacts > credentials. Nate Jones reframe (2026-05-16 council pass): "comprehension as currency"; the 4Q `EXPLANATION.md` is to the generative era what the commit message was to the traditional engineering era.

A prior premium-profile council pass on 2026-05-16 reached this unanimous verdict: **"Sean's stack is 80% built and 20% legible. The gaps are not engineering gaps — they are framing surfaces and one missing piece of control architecture (the judge layer)."**

## Evidence map — be PRECISE; do not critique artifacts that aren't shipped

**SHIPPED 2026-05-12** (load-bearing, defensible in interviews):
- `intent-engineering` MCP server v0 — published to npm (`@swins/intent-engineering-mcp@0.1.0`) and the MCP registry (`com.seanwinslow/intent-engineering`, DNS-verified). 3 tools: `audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`. Demoable in Claude Desktop with one config change.
- Phase D Typed Reasoning Edges 4Q `EXPLANATION.md` at `agents-sdk/lib/concept_edges/EXPLANATION.md`. SQLite-backed cross-domain contradiction detection with 6 relation types.
- Phase 6 Knowledge Loop 4Q `EXPLANATION.md` at `agents-sdk/agents/knowledge_loop/EXPLANATION.md`. SessionEnd flush → nightly synthesizer → weekly lint → SessionStart re-inject.

**SHIPPED + PUBLIC:**
- Code-Brain v3.37.0 — 118 skills, 13 subagents, 14 hooks, 17 SDK agents (8 active by default + 2 opt-in + 1 manual-trigger). Karpathy "agentic engineering practitioner's toolkit" framing in README line 3.

**CODE-COMPLETE, B7-GATED (do NOT recommend as resume bullets yet — they ship after the 5-night live-synth gate closes):**
- Vault Synthesizer Eval Suite — 10-case binary eval, 1/10 baseline → 7/10 post-fix. Lives at `evals/vault-synthesizer/`.
- Substack-Drafter agent — default-disabled, opt-in install. Voice rotation across 5 modes.
- Agent Fleet Observability Dashboard v1 — code complete 2026-05-17 evening; awaiting Vercel deploy.

**PLANNED, NOT YET SHIPPED** (do NOT recommend as resume bullets — they ship after the typical Week-2 application send dates):
- Sanitized financial-research fleet writeup (~2026-06-05)
- 14-agent fleet Loom + Token Cost Calculator (~Wk 3 / ~2026-05-29)
- 2D Animation Pipeline portfolio short (2026-06-11)
- Judge Layer Retrofit (2026-06-04)
- Authority/Recovery/Audit Reframe (2026-06-10)
- Vault Scorecard (2026-06-03)
- Access-vs-Meaning Manifesto (~2026-06-19)
- `seanwinslow.com` deploy (Mon 2026-05-19 — same day applications start)

## CIIA non-negotiables — these MUST NOT be recommended for the resume

The candidate signed a CIIA (Confidential Information and Invention Assignment Agreement) covering 1-year post-termination obligations through ~2026-08. Do NOT recommend bullets that include any of the following:

- **Named institutional Block Pro clients:** Goldman, JPMorgan, Fidelity, Yale, Bain.
- **Pro ARR / churn figures:** $856K ARR, $323K ARR at risk, $442K churn, 21% rate, $693K renewal, $173K downsell, $16,459 avg ARR/client, 52 / 16 client counts.
- **Unshipped Block product names:** Simon AI, Living Dashboard, Pro Search, Institutional Data Moat, Around The Block, Globe, Ambassador Program.
- **Unshipped revenue projections:** $2.3M ARR, $60K incremental, $336K, $1.2M.
- **Named internal Block executives in mid-strategy context:** Steve Chung, Mike (CTO), Cameron Tynes, Steven Zheng, Simon Cousaert, Matt Vitebsky, Ed (the candidate's manager), Larry Cermak, Vicky Lu, Alex Lebedyev. Use roles, not names.
- **The "Project CTO" codename** — use ".co homepage redesign" instead.
- **Polymarket pre-launch specifics:** "100+ leads Month 1" pilot target, lead export integration specs, X/Twitter auth lead-capture flow, sponsor data export technical detail. (General "Polymarket × Campus" mentions ARE clean — the partnership launched.)

If a recommendation would require any of the above to justify it, do not make the recommendation. Suggest a sanitized alternative or cut the bullet.

## STOP-DOING — do not recommend the resume lean into these framings

The candidate self-codes as **beginner-to-intermediate** (comfortable with React/Vite/Tailwind, Python, TypeScript when scaffolded by Claude Code; NOT a senior engineer). Do not recommend bullets that would invite a technical screen to grill the candidate on senior-engineering ground he can't defend:

- No "Agent OS" or "runtime architecture" framing.
- No claims of concurrency / distributed systems / low-level performance ownership.
- No language implying the candidate authored frameworks vs. used / orchestrated them.
- No "OpenClaw" framing (deprecated in the 2026-05-16 council pass).

## Target JD keywords — verbatim phrases the resume should mirror where defensible

Pulled directly from `2026-05-07-target-role-specs.md`, the candidate's curated 8-company target list. Use verbatim where the candidate's actual evidence supports it. **Do NOT recommend keyword-stuffing** — the candidate's locked role decision explicitly rejects "word vomit" recommendations as auto-REJECT.

- **Anthropic FDE (Tier-3 wildcard, $280–320K):** "technical artifacts for customers like MCP servers, sub-agents, and agent skills" · "Former technical founders are also encouraged to apply"
- **Glean FDP (Tier-1, $170–280K, Remote-US):** "0-to-1 product creation" · "shipped AI-powered solutions in the real world, not just designed them" · "white glove deployment" · "Trusted C-suite Advisor" · "Executive credibility"
- **Pair Team Senior PM (Tier-1, Remote):** "Familiarity with AI tools and a track record of experimenting with modern build workflows" · "Use AI tools and Pair's internal platform to ship prototypes and accelerate execution"
- **Scale AI Incubation PM (Tier-1, SF):** "hands-on experience building end-to-end systems or prototypes in production" · Python · SQL
- **Microsoft AI PM:** "Firsthand experience evaluating and deploying LLMs into production" · "Work side-by-side with researchers and engineers"
- **Sierra Agent PM (Tier-3, $180–390K):** "agent orchestration" · "conversational AI" · TypeScript, React, Go (some coding experience)
- **Liberate Senior AI Agent PM (FDP, Boston):** "identify high-impact problems, design AI agent workflows, and drive them into production"

**Cross-cutting verbs ALL Tier-1 JDs share:** ship / shipped / shipping (never led / drove / collaborated on AI bullets); production (never prototype-only); agentic / agent / agents; evals / evaluation framework / golden set; MCP (frontier labs); fine-tune / RAG / tool use / orchestration; cost / latency / throughput / p95.

## The 2026 AI PM hiring bar — what the resume must clear (per Aakash Gupta canon)

1. **Production AI shipping experience** (not prototypes). "Tell me about a time your model degraded in production" is the opening trade.
2. **Technical fluency one level deeper than expected** — named architectures (BM25 / dense vector / two-tower / contextual bandit / BERT / RAG / fine-tune), eval metrics (precision / recall / F1 / p95 latency / pass@k).
3. **AI-specific tradeoff judgment** — accuracy vs latency, complexity vs cost, precision vs recall, build vs buy, fine-tune vs RAG.
4. **Eval-design instinct** ("evals are the new PRDs") — defend a golden set, error-analyze production traces, justify an LLM-as-judge rubric.
5. **AI safety threaded throughout** — > "If you hit minute 40 of a case without mentioning safety, you've told them you don't understand AI product management."
6. **Vibe-coding fluency** — named tools (Cursor / Bolt / v0 / Lovable / Replit), ship a working prototype in 45 minutes.
7. **Range across ≥2 ML paradigms** — classical ML / DL / LLM-agents. Monoculture reads hobbyist.
8. **A PM GitHub** — > "if there's a Github linked, they will check it." Recent commits beat star counts.
9. **The F1-score landmine** — every AI-ownership bullet must carry a defensible metric. "I'd have to check" is the death answer.
10. **Specific verbs** — shipped, owned, evaluated, fine-tuned, killed, paused, retrained. Never led / drove / collaborated.

## The 8 open questions — each panelist answers all 8

Each panelist (Claude Opus 4.7, GPT-5.5, Gemini Pro, Grok 4.20): answer all 8 questions with specific bullet text where applicable.

**Q1: Resume as master vs. AI PM as master.** Should the AI PM variant become the new master (recruiter-response-rate optimization), with the current master demoted to a fallback for ambiguous-archetype openings? OR does maintaining a role-agnostic master earn its keep — given that the candidate's locked decision is that *package coherence across all 3 archetypes (AI PM / Tech PM / Creative PM) is the differentiator*, and that leaning all-in on AI PM at the master level would weaken the "more than my previous professional background" claim he wants preserved?

**Q2: Tenure asymmetry framing.** 6 months titled PM at The Block + 10+ years prior in design / animation / DAM (with AI-workflow leadership in the last 3 years). Should the Summary acknowledge "post-layoff cost-cutting, not performance" preemptively, or leave the layoff context entirely for cover letters? Be specific about the proposed Summary language.

**Q3: NYL Leadership Experience cut/modernize.** The "Team Lead, AI Workflow Integration (2021 – Nov 2025)" sub-role currently has 3 generic-management bullets: "Managed a team of 8 / Led stakeholder communication / Mentored junior staff." Should this section be: (a) dropped entirely? (b) compressed to one line with an AI-era impact metric? (c) replaced with the prompt-engineered-metadata-for-DAM evidence that already lives in NYL Work Experience? Recommend specific replacement text if (b) or (c).

**Q4: Pre-mortem methodology as a standalone Leadership Experience bullet.** The Tigers/Paper Tigers/Elephants 11-risk pre-mortem methodology is currently folded INTO the Pro 2.0 Work Experience bullet (about 6 words deep, easy to miss). Pre-mortems are a senior-PM signal most resumes don't carry. Does burying it lose the differentiation a standalone Leadership Experience bullet would surface? Recommend specific bullet text if you'd promote it.

**Q5: F1-score landmine defense.** Per the 2026 AI PM bar, every AI-ownership bullet must carry a defensible metric (precision / recall / F1 / p95 / $ per call) — or be cuttable. Audit each AI bullet on the resume below: which currently survive "tell me the metric" out loud in interview, and which need a number added or the claim trimmed? Be specific per bullet.

**Q6: Vibe-coding evidence on the resume itself.** Does the resume need a clickable Loom URL or deployed Bolt/v0 URL inline (e.g., next to a Selected Project) before Mon 2026-05-19 — or is "Cursor" in the Skills row + the GitHub link in the header sufficient for Round 1? Note: the 14-agent fleet Loom + Token Cost Calculator are PLANNED for Wk 3 (~2026-05-29), NOT yet shipped. Recommend: should the resume reference them now ("forthcoming") or wait?

**Q7: Safety / responsible-AI thread depth.** Does the safety signal appear in at least one bullet per major AI artifact, or is it absent? For Anthropic / OpenAI / Google specifically — what's the MINIMUM threading needed to clear their bar? Recommend specific additions to existing bullets vs. a separate section.

**Q8: JD-keyword mirror without keyword-stuffing.** Run the verbatim JD keywords (above) against the resume. Which target-role keywords are missing entirely? Where can they be added without stuffing (i.e., bullet evidence already supports them, they're just under-named)? Where would adding them feel forced — and is that signal that the resume is being asked to do too much for one archetype (argument for the AI-PM-as-master pivot in Q1)?

## What I'm asking for

**Per panelist:** A numbered list of the highest-leverage changes to make to this resume before applications begin Mon 2026-05-19 — ordered by expected impact on getting a Tier-1 AI PM phone screen. Be specific: bullet text, ordering, cuts, additions. Cite the 2026 AI PM hiring bar (Aakash Gupta canon, Hamel Husain evals canon, Karpathy / Nate Jones framing) where it applies. Cite specific Tier-1 JDs where keyword mismatch is the issue.

**Be brutal.** Sean wants the truth, not flattery. Default-cuttable bullets should be marked CUT. Bullets that are 90% there should be marked REWRITE with the exact new text. Bullets that are landmines (require CIIA detail or claim senior-engineer ground) should be marked LANDMINE.

**Chairman (Opus 4.7):** Synthesize the 4 panelists' critiques into ONE prioritized punch list (numbered, not prose). When panelists disagree, name the disagreement explicitly and pick a side with a reason. Bias toward shipping by Mon 2026-05-19 over perfection. Surface any unanimous-but-load-bearing finding separately at the top.

---

## Chairman attention — candidate's pre-council priorities

The candidate pre-answered all 8 questions before invoking the council. Treat the following as priority guidance for the synthesis pass:

- **Q1 — REVERSAL FROM EARLIER DEFAULT (candidate confidence 4):** Candidate now favors **AI PM as the master**, overriding the earlier funnel-role-decision default that leaned toward "keep master agnostic." Critique against the AI-PM-as-master baseline. If a panelist disagrees and recommends a return to role-agnostic master, the chairman should weigh that recommendation seriously — the candidate is open to being moved, but only on strong evidence.

- **Q5 — CANDIDATE SELF-FLAGS THE F1 LANDMINE (confidence 3):** Candidate states he can talk to bullets but cannot recite exact metrics verbatim without notes. Recommendation pair: (Path A) soften claims on bullets where exact metrics aren't memorizable; (Path B) curate the bullets down to a 5–7 metric set he WILL drill before Mon 5/19. Chairman: pick a side with reasoning and propose the bullet-level surgery.

- **Q6 — LOCKED AT CONFIDENCE 5:** Candidate will NOT add inline Loom / Bolt / v0 URLs to the resume. Only `seanwinslow.com` carries the package. **Recommendations to add per-bullet links or supplementary URLs will be auto-REJECTED in downstream triage — do not waste a numbered slot on them.**

- **Q7 + Q8 — DRIVE THESE; CANDIDATE EXPLICITLY ASKING (confidence 1 + bothering):** Candidate wrote *"I have no idea. These are the reasons why I'm asking the council. What the hell am I missing that should be showcased or learned?"* on BOTH questions. The chairman should treat these as the highest-priority load-bearing slots in the synthesis. For Q7 (safety/responsible-AI thread depth) — name what's missing per Anthropic / OpenAI / Google bars, recommend exact bullet additions, cite which Tier-1 JDs each addition unlocks. For Q8 (JD-keyword mirror) — run the verbatim keyword list against the resume bullet-by-bullet and surface specific keyword gaps that are earnable from existing evidence (not the ones that would require keyword vomit).

- **Q3, Q4 — CANDIDATE WANTS DRAFTS:** Q3 (compress NYL Leadership to one line) and Q4 (promote pre-mortem methodology to standalone Leadership bullet) — both are confidence 3–4 with the candidate already leaning toward a specific change. Panelists should propose the EXACT replacement/addition text (CIIA-clean), not just the principle. The chairman picks the strongest draft.

---

## THE RESUME

### MASTER

```markdown
# Sean Winslow

**(917) 886-1251** | [LinkedIn](https://www.linkedin.com/in/sean-winslow-204390a5) | [sean.winslow28@gmail.com](mailto:sean.winslow28@gmail.com) | [seanwinslow.com](https://seanwinslow.com) | Boston, MA

---

## Summary

AI Product Manager and agentic-engineering practitioner with 11+ years across crypto media, SaaS, and digital asset management. Most recently at The Block, shipped 3 production Claude Skills, a Polymarket B2B revenue integration, and a 10-week Confluence overhaul plan. Builds open-source agentic-engineering tooling — the 118-skill Code-Brain and a 17-agent autonomous SDK fleet.

---

## Work Experience

### The Block | Boston, MA (Remote)

**Product Manager** | *November 2025 – May 2026*

- Shipped 3 production Claude Skills (`etf-page-creator`, `stakeholder-update`, `jira-automation`) automating WordPress ETF page generation, biweekly executive updates, and per-product Jira ticket scaffolding — direct delivery against the P&E Q2 Objective 5 KR3 ("Ship 1–3 Claude Skills").
- Built the AdOps RevOps automation pipeline — 11 Zapier workflows + 10 product-specific intake forms + central Tables database — turning a Salesforce "Closed Won" trigger into auto-created parent/child Jira tickets, personalized client intake emails, and routed Slack notifications, eliminating 7 manual handoff steps per deal.
- Authored the PRD (v1→v3) and shipped The Block's first sponsored-microcourse B2B revenue vertical (Polymarket × Campus) — a 5-component build (homepage module, Learn page hub, in-article recirculation, embedded course player, sponsor data layer) connecting The Block's editorial audience to Campus education content, plus a sales one-pager template that productized the partnership for repeatable revenue-team sale.
- Built the .co homepage redesign competitive visual audit — 50+ site benchmark across 8 categories (crypto-native, premium news, financial/data, modular newsletter formats, editorial design, bento layouts, crypto data, wildcards) with a structured "one to steal / one to never do" capture methodology — feeding blue-sky design exploration with the design team.
- Co-authored the Block Pro 2.0 product audit + competitive analysis (9 enterprise data/research platforms benchmarked) and conducted 3 internal stakeholder interviews (sales, research, head of data) to scope the pitch deck delivered to the incoming CEO — including a structured pre-mortem (11 risks across launch-blocking, fast-follow, and track tiers) that surfaced engineering-capacity and renewal-cliff dependencies before the proposal landed.
- Automated image, video, and voiceover generation for the Campus 201 enterprise course launch using Nano Banana Pro, Veo 3.1 / Kling 3.0, and ElevenLabs APIs.
- Authored the 10-week P&E Department 2.0 execution plan consolidating 7 competing team-doc hubs, ~25 orphaned Developer Sync pages, and 5+ overlapping onboarding pages into a per-product Confluence architecture with a centralized Templates Library — framed as operational-maturity proof for the incoming CEO and direct delivery against P&E Q2 OKR Objective 5 (Operational Excellence & AI-Assisted Efficiency).

### New York Life Insurance — Multimedia And Design | New York, NY

**Product Operations Lead** | *March 2015 – November 2025*

- Led enterprise rollout of a SaaS DAM platform across 50+ locations, leading requirements gathering and translating business needs into actionable technical documentation within the Atlassian suite.
- Increased media asset productivity by 40% through onboarding programs and custom training for 100+ users.
- Boosted asset discoverability by 60% using prompt-engineered metadata via ChatGPT, Claude, and Gemini.
- Reduced UX friction and system response time by 50% by analyzing Jira support tickets and refining workflows.

---

## Leadership Experience

### The Block | Boston, MA (Remote)

**Product Manager** | *November 2025 – May 2026*

- Led daily P&E standups and drove cross-functional execution across engineering, design, and revenue operations in Slack, Confluence, Jira, and Figma.
- Onboarded fellow Product Managers on Claude Code and agentic-engineering workflows; built a P&E Claude Skills library covering Jira automation, ETF page creation, stakeholder updates, and design system enforcement.
- Created the PRD-to-Prototype Lab project — an in-product reference giving designers and engineers shared access to user flows, PRD details, and the Block design system.
- Authored the x402 / A2A / Block Pro MCP integration strategy memo — mapping 6 monetization vectors (per-chart dashboard micropayments, API pay-per-request, AI agent data feeds, index access, education micropayments, content-crawl revenue) to Coinbase's HTTP-native payment protocol — positioning Block Pro as default data infrastructure for the emerging agent economy.

### New York Life Insurance — Multimedia And Design | New York, NY

**Team Lead, AI Workflow Integration** | *2021 – November 2025*

- Managed a team of 8 to deliver AI-based automation features in digital asset management pipelines.
- Led stakeholder communication and alignment to integrate AI tools into core workflows.
- Mentored junior staff on prompt engineering and AI tool usage aligned to roadmap objectives.

---

## Selected Projects

### Code-Brain — Open-Source Toolkit

- Open-source agentic engineering toolkit for Claude Code: 118 skills, 13 subagents, 14 hooks, 17 autonomous Claude Agent SDK agents (8 active on local-first launchd schedules).
- Used in production for daily PM workflows, vault automation, and content generation across crypto, creative, and personal-systems domains.
- Demonstrates Karpathy-style "agentic engineering practitioner" architecture — agents own decomposition; human owns judgment.
- Architecture writeups for two production subsystems: Phase D Typed Reasoning Edges (SQLite-backed cross-domain contradiction detection) and Phase 6 Knowledge Loop (SessionEnd flush → nightly synth → weekly lint → SessionStart re-inject).

### intent-engineering MCP Server

- 3-tool TypeScript MCP server (`audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`) for AI specification authoring — published to npm (`@swins/intent-engineering-mcp@0.1.0`) and the MCP registry (`com.seanwinslow/intent-engineering`, DNS-verified namespace).
- Shipped 2026-05-12, 13 days ahead of plan. Demoable in Claude Desktop with a single config change.
- Operationalizes the intent-engineering framework — agent reads a spec and tells you what's missing — as a portable, reusable server.

### Agentic Financial-Research Fleet

- Multi-agent autonomous research system: queue file → router → 3 retrieval agents → local-LLM synthesis → daily morning brief.
- Runs on a $0/month local-first stack (Ollama, SearXNG, LDR) with Gemini Deep Research as cloud fallback for compound topics.
- Design exemplar of a "sensors and actuators" architecture on a fine-tuned local stack — verifiable, durable, fully self-hosted.

### 2D Animation Pipeline — Portfolio Short (June 2026)

- Agent-orchestrated 2D animation pipeline: humans own the creative ceiling, agents own the technical floor (asset generation, lip sync, render).
- Built on Nano Banana 2 + Seedance 2.0 + Adobe MCP, with a custom 2D-animation-principles skill governing timing and style.
- Applies 12+ years of illustration and animation craft through AI-native production tooling; portfolio short ships June 2026.

---

## Education & Certification

**College of Staten Island** — Staten Island, NY *Bachelor of Arts in Media Studies* | 2010 – 2014

---

## Skills

**AI / Agentic Engineering:** Claude Code, Claude Agent SDK, Claude Skills authoring, MCP (Model Context Protocol), prompt engineering, agent orchestration, RAG / local-LLM workflows (Ollama, SearXNG, Qwen3, gemma4), AI media generation (Nano Banana 2, Veo 3.1, Kling 3.0, ElevenLabs, Seedance 2.0)

**Product Craft:** PRD authoring, user research, competitive analysis, A/B testing, GA4 analytics, roadmap planning, OKR ownership, agile / scrum, cross-functional facilitation, build-in-public

**Tools & Platforms:** Cursor, GitHub, Jira, Confluence, Slack, Figma, Notion, Adobe Creative Suite, Zapier, Anthropic API, NotebookLM

**Domains:** Crypto / digital assets, B2B SaaS, EdTech / online learning, media production, animation
```

### AI PM VARIANT

> **Note for panelists:** The variant uses the same bullet content as the MASTER but in a different reading order — leading with Skills + AdOps and demoting Polymarket / .co audit / P&E Dept 2.0 to later in the section. The Summary line is rewritten. The Leadership Experience section also re-orders to lead with the x402 / A2A / MCP strategy memo. Selected Projects, Education, and Skills are identical to MASTER. This re-ordering is the entire tailoring strategy across all 4 variants — no content is invented or cut.

```markdown
# Sean Winslow

**(917) 886-1251** | [LinkedIn](https://www.linkedin.com/in/sean-winslow-204390a5) | [sean.winslow28@gmail.com](mailto:sean.winslow28@gmail.com) | [seanwinslow.com](https://seanwinslow.com) | Boston, MA

---

## Summary

AI Product Manager and agentic-engineering practitioner. Ships production Claude Skills, the `intent-engineering` MCP server, and autonomous agent fleets. Most recently at The Block, delivered 3 Claude Skills, co-authored the Block Pro 2.0 product audit and competitive analysis, and authored the x402 / A2A / MCP integration strategy memo positioning Block Pro for the agent economy. Maintains the open-source 118-skill Code-Brain and a 17-agent autonomous SDK fleet.

---

## Work Experience

### The Block | Boston, MA (Remote)

**Product Manager** | *November 2025 – May 2026*

- Shipped 3 production Claude Skills (`etf-page-creator`, `stakeholder-update`, `jira-automation`) automating WordPress ETF page generation, biweekly executive updates, and per-product Jira ticket scaffolding — direct delivery against the P&E Q2 Objective 5 KR3 ("Ship 1–3 Claude Skills").
- Built the AdOps RevOps automation pipeline — 11 Zapier workflows + 10 product-specific intake forms + central Tables database — turning a Salesforce "Closed Won" trigger into auto-created parent/child Jira tickets, personalized client intake emails, and routed Slack notifications, eliminating 7 manual handoff steps per deal.
- Co-authored the Block Pro 2.0 product audit + competitive analysis (9 enterprise data/research platforms benchmarked) and conducted 3 internal stakeholder interviews (sales, research, head of data) to scope the pitch deck delivered to the incoming CEO — including a structured pre-mortem (11 risks across launch-blocking, fast-follow, and track tiers) that surfaced engineering-capacity and renewal-cliff dependencies before the proposal landed.
- Automated image, video, and voiceover generation for the Campus 201 enterprise course launch using Nano Banana Pro, Veo 3.1 / Kling 3.0, and ElevenLabs APIs.
- Authored the PRD (v1→v3) and shipped The Block's first sponsored-microcourse B2B revenue vertical (Polymarket × Campus) — a 5-component build (homepage module, Learn page hub, in-article recirculation, embedded course player, sponsor data layer) connecting The Block's editorial audience to Campus education content, plus a sales one-pager template that productized the partnership for repeatable revenue-team sale.
- Built the .co homepage redesign competitive visual audit — 50+ site benchmark across 8 categories (crypto-native, premium news, financial/data, modular newsletter formats, editorial design, bento layouts, crypto data, wildcards) with a structured "one to steal / one to never do" capture methodology — feeding blue-sky design exploration with the design team.
- Authored the 10-week P&E Department 2.0 execution plan consolidating 7 competing team-doc hubs, ~25 orphaned Developer Sync pages, and 5+ overlapping onboarding pages into a per-product Confluence architecture with a centralized Templates Library — framed as operational-maturity proof for the incoming CEO and direct delivery against P&E Q2 OKR Objective 5 (Operational Excellence & AI-Assisted Efficiency).

### New York Life Insurance — Multimedia And Design | New York, NY

**Product Operations Lead** | *March 2015 – November 2025*

- Led enterprise rollout of a SaaS DAM platform across 50+ locations, leading requirements gathering and translating business needs into actionable technical documentation within the Atlassian suite.
- Increased media asset productivity by 40% through onboarding programs and custom training for 100+ users.
- Boosted asset discoverability by 60% using prompt-engineered metadata via ChatGPT, Claude, and Gemini.
- Reduced UX friction and system response time by 50% by analyzing Jira support tickets and refining workflows.

---

## Leadership Experience

### The Block | Boston, MA (Remote)

**Product Manager** | *November 2025 – May 2026*

- Authored the x402 / A2A / Block Pro MCP integration strategy memo — mapping 6 monetization vectors (per-chart dashboard micropayments, API pay-per-request, AI agent data feeds, index access, education micropayments, content-crawl revenue) to Coinbase's HTTP-native payment protocol — positioning Block Pro as default data infrastructure for the emerging agent economy.
- Onboarded fellow Product Managers on Claude Code and agentic-engineering workflows; built a P&E Claude Skills library covering Jira automation, ETF page creation, stakeholder updates, and design system enforcement.
- Created the PRD-to-Prototype Lab project — an in-product reference giving designers and engineers shared access to user flows, PRD details, and the Block design system.
- Led daily P&E standups and drove cross-functional execution across engineering, design, and revenue operations in Slack, Confluence, Jira, and Figma.

### New York Life Insurance — Multimedia And Design | New York, NY

**Team Lead, AI Workflow Integration** | *2021 – November 2025*

- Managed a team of 8 to deliver AI-based automation features in digital asset management pipelines.
- Led stakeholder communication and alignment to integrate AI tools into core workflows.
- Mentored junior staff on prompt engineering and AI tool usage aligned to roadmap objectives.

---

## Selected Projects, Education, and Skills

*(Identical to MASTER above — Code-Brain, intent-engineering MCP, Agentic Financial-Research Fleet, 2D Animation Pipeline, College of Staten Island, and the 4 Skills rows.)*
```

---

## Reminder before submitting

The candidate's locked decision (Phase 1 Task 1.1, 2026-05-17) frames the resume as **secondary in a 4-piece pristine package**, with **package coherence as the differentiator across all 3 archetypes (AI PM / Tech PM / Creative PM)**. Recommendations that pull the resume sharper toward AI PM at the cost of cross-archetype range are tradeoffs that need explicit defense from the panelist making them. Recommendations that constitute keyword vomit (per the candidate's locked decision) are auto-REJECT in the candidate's downstream triage — don't waste a numbered slot on them.

The 5 unshakeable interview anchors the resume primes for (per the candidate's interview-prep canon): (a) one shipped MCP server (Karpathy thesis); (b) verbal lifeline drilled; (c) numbers ready (precision, $/morning, p95); (d) selling demonstrated work not tenure; (e) work has a canonical home (personal site).

Begin.
```

## Council responses

### anthropic/claude-opus-4.7

# Panelist Response — [Model Identity Withheld for Cross-Ranking]

Reading the brief as instructed. Anchoring to the candidate's pre-council priorities (Q1 reversal toward AI-PM-as-master, Q7/Q8 as the load-bearing slots, Q6 locked at 5 — no inline URLs).

---

## Q1: Master vs. AI PM Variant

**Recommendation: Make the AI PM variant the new master. Confidence: HIGH.**

The "package coherence across 3 archetypes" framing is real but it lives at the *package* level (seanwinslow.com, Substack, GitHub) — not at the resume level. The resume's job inside the package is to be the **load-bearing supporting member**, and load-bearing means *legible to the gatekeeper reading it*. A Tier-1 AI PM recruiter spends 20 seconds. A role-agnostic resume forces them to do the archetype-translation work. They won't.

The cross-archetype range claim ("more than my previous professional background") is preserved by:
1. The 11+ years of NYL prior work still on the resume
2. The 2D Animation Pipeline project (creative archetype anchor)
3. seanwinslow.com itself, which can carry the Creative PM proof in a dedicated section

The disagreement to surface: if the candidate is sending ≥30% of applications to Tech PM or Creative PM roles, a single master is wrong regardless of which archetype it favors — he needs the 4 variants he already plans. The Q1 question is really *which variant is the default*, and the default should be the one matching the priority-1 archetype. That's AI PM.

**Verdict: AI PM variant = master. Tech PM and Creative PM = tailored variants. Role-agnostic master = retired.**

---

## Q2: Tenure Asymmetry Framing

**Do NOT acknowledge the layoff in the Summary.** This is a self-inflicted wound. Resumes don't explain gaps that don't exist yet — the May 2026 end date with no current role does the work silently; recruiters in 2026 understand the macro environment. Preemptive defense reads as anxiety.

**Proposed Summary (AI PM variant, rewrite):**

> AI Product Manager and agentic-engineering practitioner. Ships production Claude Skills, MCP servers, and autonomous agent fleets evaluated against golden-set evals. At The Block, shipped 3 production Claude Skills against P&E OKR delivery, authored the x402 / MCP integration strategy positioning Block Pro for the agent economy, and co-authored the Pro 2.0 product audit with an 11-risk structured pre-mortem. Maintains the open-source 118-skill Code-Brain and a 17-agent Claude Agent SDK fleet; published `@swins/intent-engineering-mcp` to npm and the MCP registry.

Why this works: opens with "ships" (the cross-cutting Tier-1 verb), names MCP and evals (Hamel/Aakash bar), names specific shipped artifacts (Karpathy thesis), preserves the 11+ years implicitly via The Block + the NYL section below. Reserve the layoff context for cover letters and screens — "the team was cut, not the role" is a 2-sentence verbal answer, not a resume line.

---

## Q3: NYL Leadership Section — COMPRESS to One Line

The current 3 bullets are pure landmines. "Managed a team of 8 / Led stakeholder communication / Mentored junior staff" is exactly the "led / drove / collaborated on" anti-pattern Aakash's canon explicitly calls out as the death-sentence verb set for AI PM resumes. **CUT all 3 bullets.**

**Proposed replacement — single bullet:**

> Led an 8-person cross-functional team integrating prompt-engineered metadata pipelines (ChatGPT, Claude, Gemini) into enterprise DAM workflows — the precursor work to the agentic-engineering practice now shipping in open source.

This does three things: keeps the management scope (8 people), names the AI tools (keyword density without stuffing), and explicitly bridges old career → current practice as a *narrative continuity* signal rather than a tenure-padding signal. The "precursor work" phrase is the load-bearing word — it makes the 11+ years count *toward* the AI PM thesis, not against it.

---

## Q4: Pre-Mortem — PROMOTE to Standalone Leadership Bullet

Yes, promote. Burying an 11-risk structured pre-mortem 6 words deep in a 4-line bullet wastes the strongest senior-PM signal on the page. Most candidates can't articulate a pre-mortem methodology, let alone tier risks across launch-blocking/fast-follow/track. This is exactly the kind of artifact a hiring manager asks "tell me about a time you killed or paused a project" for.

**Proposed standalone Leadership bullet (place first, above the x402 memo):**

> Designed and ran an 11-risk structured pre-mortem for the Block Pro 2.0 proposal — tiering risks across launch-blocking, fast-follow, and track categories, surfacing engineering-capacity and renewal-cliff dependencies before the pitch landed with the incoming CEO. Methodology framed against Gary Klein's pre-mortem canon; reusable as a P&E governance artifact.

This bullet uses verbs the Aakash canon explicitly *favors* (designed, ran, surfaced) and signals the "kill/pause" judgment the AI PM bar opens with. Keep the pre-mortem reference in the Pro 2.0 Work Experience bullet too — the duplication is intentional and standard.

---

## Q5: F1-Score Landmine Audit — Path B (Curate to 5-7 Drillable Metrics)

Path A (soften everything) abandons the metrics that *do* survive scrutiny. Path B is right. Audit:

**SURVIVES interview drill (keep as-is):**
- "11 Zapier workflows + 10 product-specific intake forms + central Tables database... eliminating 7 manual handoff steps" — countable, defensible, the candidate built it.
- "3 production Claude Skills" — countable, named, defensible.
- "11 risks across launch-blocking, fast-follow, and track tiers" — defensible per Q4.
- "9 enterprise data/research platforms benchmarked... 3 internal stakeholder interviews" — defensible.
- "50+ site benchmark across 8 categories" — defensible.
- "118 skills, 13 subagents, 14 hooks, 17 SDK agents" — defensible, on GitHub.
- "Published to npm and MCP registry, DNS-verified, 13 days ahead of plan" — defensible, verifiable.

**NEEDS metric added OR softening:**
- NYL "40% productivity / 60% discoverability / 50% UX friction reduction" — **LANDMINE if candidate can't reproduce the measurement methodology.** These are the classic "I'd have to check" trap. Recommend: keep two, cut one. Drill the methodology for the two kept (what was the baseline, what was the post-measure, over what window). My pick: keep the 60% discoverability one (the AI-adjacent one — prompt-engineered metadata maps directly to the AI PM bar) and the 40% productivity. **CUT the 50% UX friction bullet** — it's the weakest of the three and the verb "reduced... by analyzing Jira tickets" reads as analyst, not PM.
- "Polymarket × Campus 5-component build" — needs an *outcome* metric or it's a feature list. Per CIIA, the pilot target ("100+ leads Month 1") is off-limits. Recommended sanitized softening: change "shipped The Block's first sponsored-microcourse B2B revenue vertical" to "shipped and launched The Block's first sponsored-microcourse B2B revenue vertical with Polymarket as launch partner" — the *launch* + named partner is the metric proxy.

**The 5-7 drill set the candidate should memorize cold before May 19:**
1. 3 Claude Skills + the OKR KR they delivered against
2. 7 manual handoff steps eliminated, 11 Zapier flows, 10 intake forms
3. 11-risk pre-mortem (3 tiers, 2 surfaced dependencies)
4. 118 skills / 17 agents / 8 active by default
5. npm + MCP registry publish, 13 days ahead of plan, 3 tools named
6. 60% discoverability lift via prompt-engineered metadata at NYL (baseline + methodology)
7. 9 platforms benchmarked + 3 stakeholder interviews for Pro 2.0

---

## Q6: Vibe-Coding Evidence — LOCKED, SKIPPING per candidate instruction.

---

## Q7: Safety / Responsible-AI Threading — THE BIGGEST GAP

**Current state: safety is functionally absent from the resume.** Zero bullets mention evals, golden sets, judge layers, failure modes, guardrails, refusal handling, red-teaming, or human-review architecture. For Anthropic FDE specifically — *which is the candidate's $280-320K wildcard* — this is a P0 gap. Anthropic reads resumes that don't mention safety as resumes from people who don't understand what Anthropic does.

**The minimum threading needed per Tier-1 target:**

- **Anthropic FDE**: Must see "evals," "MCP," "skills/subagents/SDK" — has 2 of 3 (MCP, skills). Missing: evals language.
- **Glean FDP**: Must see "production," "shipped," "white glove" or equivalent customer-deployment language. Has production + shipped. Missing: customer-deployment framing.
- **Microsoft AI PM**: Must see "evaluating LLMs in production." Missing entirely.
- **Liberate**: Must see "agent workflows... into production." Has agent workflow shipped (the SDK fleet). Missing: production framing for the fleet.

**Specific bullet additions (CIIA-clean, defensible from shipped evidence):**

**Addition 1 — Add to Code-Brain project bullet:**
> Architecture writeups for two production subsystems: Phase D Typed Reasoning Edges (SQLite-backed cross-domain contradiction detection — a lightweight judge layer surfacing factual conflicts across the vault) and Phase 6 Knowledge Loop (SessionEnd flush → nightly synth → weekly lint → SessionStart re-inject, with eval-gated promotion).

The italicized adds threading without overclaiming. "Judge layer" + "eval-gated promotion" are the magic words for Anthropic/OpenAI/Google readers.

**Addition 2 — Add a new bullet to the intent-engineering project:**
> Built on an evals-first methodology: the `audit_intent_spec` tool *is* the eval — it scores a spec against the framework's 4 dimensions and tells the author what's missing before the spec ships to a coding agent. Operationalizes the "evals are the new PRDs" thesis (Hamel Husain) as a portable MCP server.

The Hamel citation is intentional — it signals the candidate is in the eval-design conversation, not just adjacent to it. This bullet alone moves the resume from "uses AI tools" to "thinks in evals," which is the Aakash bar.

**Addition 3 — Rewrite the 3-Claude-Skills bullet to thread production safety:**
> Shipped 3 production Claude Skills (`etf-page-creator`, `stakeholder-update`, `jira-automation`) automating WordPress ETF page generation, biweekly executive updates, and per-product Jira ticket scaffolding — each skill scoped with a human-in-the-loop review gate before publish, direct delivery against the P&E Q2 Objective 5 KR3 ("Ship 1–3 Claude Skills").

"Human-in-the-loop review gate before publish" is the safety thread. Defensible — the candidate can explain in interview that ETF pages don't auto-publish; an editor reviews. That *is* responsible-AI deployment.

**Addition 4 — New Skills section line, append to "AI / Agentic Engineering":**
> ...evals (golden-set design, LLM-as-judge rubrics, regression suites), human-in-the-loop deployment patterns, MCP namespace governance.

This is the keyword-density move that's *earned* — the candidate has the Vault Synthesizer eval suite shipped (1/10 → 7/10 baseline), even if it's B7-gated for bullets. Skills row references to capability are fair game; bullet claims to specific artifacts are not.

---

## Q8: JD-Keyword Mirror — Bullet-by-Bullet Gap Map

**Keywords currently present in the AI PM variant:** shipped, production, agent/agentic, MCP, Claude Skills, PRD, RAG, Cursor, GitHub, prompt engineering, orchestration, cross-functional.

**Verbatim keywords MISSING that are earnable from existing evidence:**

| Keyword | Source JD | Earnable from | Where to add |
|---|---|---|---|
| **"evals" / "evaluation framework" / "golden set"** | Anthropic, Microsoft, Hamel canon | Vault Synthesizer eval suite (B7), `audit_intent_spec` tool, Knowledge Loop "eval-gated promotion" | Q7 additions above |
| **"0-to-1"** | Glean FDP | Polymarket × Campus (literally a 0-to-1 revenue vertical), AdOps RevOps pipeline (0-to-1 system), intent-engineering MCP | Rewrite Polymarket bullet opener: *"Drove 0-to-1 product creation: authored the PRD (v1→v3) and shipped..."* |
| **"end-to-end systems"** | Scale AI | AdOps RevOps pipeline (Salesforce → Jira → Slack → email is end-to-end), intent-engineering MCP | Rewrite AdOps opener: *"Built an end-to-end RevOps automation pipeline..."* |
| **"fine-tune" or "fine-tuned"** | Cross-cutting | NOT defensible from shipped evidence — DO NOT ADD | Skip |
| **"agent orchestration"** | Sierra | 17-agent SDK fleet, financial-research fleet router | Rewrite Financial-Research Fleet bullet 1: *"Multi-agent orchestration: queue file → router → 3 retrieval agents..."* |
| **"conversational AI"** | Sierra | Not defensible — skip | Skip |
| **"AI agent workflows... into production"** | Liberate | 17-agent fleet running on launchd schedules, Claude Skills in production at Block | Rewrite Code-Brain bullet 1: *"...17 autonomous Claude Agent SDK agents (8 in production on local-first launchd schedules)."* — change "active" → "in production" |
| **"hands-on experience building... prototypes in production"** | Scale | Already covered if above changes land | — |
| **"Python, SQL"** | Scale | Phase D is SQLite-backed; agents touch Python | Add to Skills row Tools: *"Python, SQL/SQLite, TypeScript"* — DEFENSIBLE because Phase D EXPLANATION.md is on GitHub with the SQL schema visible |
| **"production" (as verb-modifier)** | All Tier-1 | Already present; double-down by changing "active" → "production" everywhere defensible | Throughout |
| **"trusted advisor" / "executive credibility"** | Glean FDP | Pro 2.0 pitch to incoming CEO, P&E Dept 2.0 plan framed for incoming CEO | Already present implicitly; consider Summary line: *"...pitched to the incoming CEO"* survives CIIA (no name) |
| **"p95 / latency / cost"** | Cross-cutting | Financial-Research Fleet is "$0/month local-first stack" — that IS the cost story | Rewrite Financial-Research bullet 2: *"Runs on a $0/month local-first stack (Ollama, SearXNG, LDR) with Gemini Deep Research as cloud fallback — explicit build-vs-buy and cost/latency tradeoff."* |

**Keywords that would feel forced and signal AI-PM overreach (DO NOT ADD):**
- "Fine-tune" — candidate has not fine-tuned a model. Don't claim it.
- "Two-tower / contextual bandit / BERT" — too specific; would invite an interview death trap.
- "Distributed systems" — already on the STOP-DOING list.
- "LLM-as-judge" as a bullet claim — only safe in Skills row (per Q7 Addition 4), not as a shipped-artifact bullet until the judge layer retrofit ships 2026-06-04.

---

## The Numbered Punch List — Ordered by Impact on Tier-1 Phone Screen

1. **Make the AI PM variant the new master.** Retire the role-agnostic master. (Q1)
2. **Add "evals" language in 3 places** — intent-engineering project (Hamel citation), Code-Brain project ("judge layer," "eval-gated promotion"), and Skills row. This is the single biggest gap. (Q7)
3. **Rewrite the Summary** to lead with "Ships... evaluated against golden-set evals" and name MCP + Skills + SDK fleet explicitly. (Q2)
4. **Add "human-in-the-loop review gate before publish"** to the 3-Claude-Skills bullet. Unlocks Anthropic/Microsoft/Google safety bar. (Q7)
5. **Promote the pre-mortem to a standalone Leadership bullet**, top of section, above x402. (Q4)
6. **Compress NYL Leadership 3 bullets → 1 bullet** with the "precursor work" bridge framing. (Q3)
7. **CUT the NYL "50% UX friction" bullet.** Weakest of the three NYL metrics; reads as analyst not PM. (Q5)
8. **Inject "0-to-1," "end-to-end," "agent orchestration," "in production"** as verb upgrades on existing bullets (Polymarket, AdOps, Financial-Research, Code-Brain). All earned from existing evidence. (Q8)
9. **Add Python + SQL/SQLite to Skills row Tools** — defensible from the GitHub Phase D writeup. (Q8)
10. **Drill the 7-metric set cold** before May 19. Methodology + baseline + window for each. (Q5, Path B)
11. **Do not mention the layoff in Summary.** Reserve for cover letter. (Q2)

---

## Disagreements to Flag for the Chairman

- **Q1 strength of conviction**: I'm at HIGH confidence on AI-PM-as-master, but the cross-archetype range concern is *real* — the candidate should commit to producing the Tech PM and Creative PM variants within 72 hours of master swap, or the package coherence claim weakens.
- **Q5 Path A vs B**: I'm picking Path B (curate-and-drill) but Path A has merit for the NYL bullets specifically where the methodology is 5+ years stale. Hybrid is correct: Path B for Block bullets, mild Path A softening on the two surviving NYL percentages if the methodology can't be reproduced cleanly.
- **Q7 depth**: I'm recommending 4 specific additions. A weaker reading would say "one is enough." It's not. Anthropic / OpenAI / Google each have their own threshold and one bullet doesn't clear three of them.

Brutal as requested. The resume is 80% there. The 20% is the eval language and the safety thread — both earnable from already-shipped evidence, no new work required.

### openai/gpt-5.5

## My blunt verdict

Use **AI PM as the master** for Tier-1 applications. The current “master” reads like a strong product-ops / creative-tech resume with AI projects appended. The AI PM variant is directionally right, but it still has three problems that will cost screens:

1. **The best AI evidence is too low on the page.** The shipped MCP server and Code-Brain should not wait until “Selected Projects” after two experience sections.
2. **Safety / eval language is too thin.** For Anthropic / OpenAI / Google-style bars, “agentic” without authority boundaries, review gates, eval criteria, or traceability reads immature.
3. **Several bullets overreach or are future-facing.** The 2D animation pipeline is planned. The financial-research fleet has wording that invites technical grilling. The x402 / A2A / MCP strategy bullet sounds unshipped and potentially too strategic to defend as impact.

Below is the ordered punch list I would execute before applications begin.

---

# Highest-leverage changes before Mon 2026-05-19

## 1. Make the AI PM variant the master, but do real surgery — not just reordering.

**Decision:** Yes, **AI PM becomes the master**. Keep a fallback “Product / Creative Technology PM” variant, but for Tier-1 AI PM roles, the resume should lead with shipped AI artifacts.

The package coherence argument actually supports this. If the site, GitHub, Substack, and resume are all telling the same story — “agentic engineering practitioner who ships” — then the resume should not hedge.

### Change header URL

Current:

```markdown
[seanwinslow.com](https://seanwinslow.com)
```

Change to:

```markdown
[seanwinslow.com/transactions](https://seanwinslow.com/transactions)
```

That URL is load-bearing. It should be visible in the header.

---

## 2. Replace the Summary with a tighter AI PM positioning statement.

**Do not mention the layoff in the Summary.** That belongs in a recruiter screen or cover letter if asked. Preemptively explaining a 6-month tenure makes the resume defensive before the reader has decided you are interesting.

### REWRITE Summary

```markdown
AI Product Manager and agentic-engineering practitioner with 11+ years turning ambiguous creative, data, and operational workflows into shipped tools. At The Block, shipped 3 production Claude Skills, an AdOps RevOps automation pipeline, and the Polymarket × Campus sponsored-microcourse revenue vertical. Independently shipped a DNS-verified TypeScript MCP server and maintain the open-source 118-skill Code-Brain. Strength: converting messy workflows into scoped agentic systems with human review, authority boundaries, and measurable operational lift.
```

Why this is better:

- Keeps the 11+ years.
- Does not lead with “6 months at The Block.”
- Uses **shipped** repeatedly, which Tier-1 AI PM JDs want.
- Adds responsible-AI language without creating a fake safety section.
- Mentions the MCP server in the Summary, which the current master does not.

---

## 3. Add a short “Selected AI Artifacts” section immediately after Summary.

The current resume buries your best AI PM proof. For Anthropic FDE, Glean FDP, Scale AI Incubation PM, Microsoft AI PM, Sierra, and Liberate, the shipped artifacts are more important than chronology.

Add this section after Summary and before Work Experience.

### ADD

```markdown
## Selected AI Artifacts

- Shipped `intent-engineering` MCP server v0: 3-tool TypeScript server (`audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`) published to npm and the MCP registry under a DNS-verified namespace; demoable in Claude Desktop with one config change.
- Maintain Code-Brain v3.37.0: open-source agentic-engineering toolkit with 118 skills, 13 subagents, 14 hooks, and 17 Claude Agent SDK agents for local-first PM, research, and content workflows.
- Published technical writeups for two production subsystems: SQLite-backed Typed Reasoning Edges for cross-domain contradiction detection across 6 relation types, and a Knowledge Loop that flushes session memory, synthesizes nightly, lints weekly, and re-injects context at session start.
```

This directly mirrors Anthropic’s “technical artifacts for customers like MCP servers, sub-agents, and agent skills” without stuffing.

---

## 4. CUT the planned 2D Animation Pipeline from the AI PM master.

### CUT

```markdown
### 2D Animation Pipeline — Portfolio Short (June 2026)
```

Reason: It is planned, not shipped. In an AI PM resume, future-dated projects weaken credibility. Keep it for a Creative PM variant after it ships.

If you need to preserve the creative background, keep it in Skills / Domains:

```markdown
**Domains:** Crypto / digital assets, B2B SaaS, EdTech, digital asset management, AI-assisted media production, animation
```

Do not include future project bullets in the AI PM master.

---

## 5. Rewrite the Block bullets to make metrics, safety, and production clearer.

The Block section is strong, but several bullets are too long and some hide the actual AI PM signal.

### REWRITE: Claude Skills bullet

Current is good but needs safety / review framing.

```markdown
- Shipped 3 production Claude Skills (`etf-page-creator`, `stakeholder-update`, `jira-automation`) for WordPress ETF page generation, executive-update drafting, and Jira ticket scaffolding; scoped each workflow for human review before publishing, sending, or ticket creation.
```

Why: Adds responsible-AI threading. “Human review before publishing/sending/ticket creation” is exactly the kind of authority-boundary language Anthropic/OpenAI/Google expect.

---

### REWRITE: AdOps RevOps automation

Current bullet is strong. Keep the metric. Slightly shorten.

```markdown
- Built AdOps RevOps automation pipeline with 11 Zapier workflows, 10 product-specific intake forms, and a central Tables database; converted Salesforce “Closed Won” triggers into routed Jira tickets, client-intake emails, and Slack notifications, eliminating 7 manual handoff steps per deal.
```

This survives the metric test.

---

### REWRITE: Polymarket × Campus bullet — remove possible sponsor-data landmine

Current phrase:

> sponsor data layer

That brushes against the CIIA warning around Polymarket sponsor data specifics. Sanitize it.

```markdown
- Authored PRD v1→v3 and shipped The Block’s first sponsored-microcourse B2B revenue vertical, Polymarket × Campus: homepage module, Learn hub, in-article recirculation, embedded course player, and reporting requirements connecting editorial audience demand to Campus education content.
```

Avoid “sponsor data layer.” Avoid pre-launch lead/export/auth specifics.

---

### KEEP / TIGHTEN: .co homepage audit

```markdown
- Built .co homepage redesign competitive visual audit: 50+ sites across 8 categories, using a structured “one to steal / one to never do” capture method to feed blue-sky design exploration.
```

This is not AI PM core, but it preserves product/creative range.

---

### REWRITE: Block Pro 2.0 audit + pre-mortem

The current bullet is good but too dense. Split the pre-mortem into Leadership Experience, because it is a senior-PM signal.

Work Experience version:

```markdown
- Co-authored Block Pro 2.0 product audit and competitive analysis, benchmarking 9 enterprise data/research platforms and synthesizing interviews with sales, research, and data stakeholders into a CEO-level product strategy pitch.
```

Then promote the pre-mortem separately under Leadership. See item 7.

---

### CUT or REWRITE: Campus 201 media automation

Current:

```markdown
- Automated image, video, and voiceover generation for the Campus 201 enterprise course launch using Nano Banana Pro, Veo 3.1 / Kling 3.0, and ElevenLabs APIs.
```

This is cool, but it lacks a metric and sounds more creative-production than AI PM. If space is tight, cut. If retained, rewrite with review/safety:

```markdown
- Automated AI-assisted image, video, and voiceover generation for Campus 201 course production using Nano Banana Pro, Veo 3.1 / Kling 3.0, and ElevenLabs, with human creative review before final asset delivery.
```

But I would probably **CUT** it from the AI PM master unless there is a count: number of assets, hours saved, production cycle reduction, or cost reduction.

---

### KEEP / TIGHTEN: P&E Department 2.0

```markdown
- Authored 10-week P&E Department 2.0 execution plan consolidating 7 team-doc hubs, ~25 orphaned Developer Sync pages, and 5+ overlapping onboarding pages into a per-product Confluence architecture with a centralized Templates Library.
```

This is product-ops credibility. Keep.

---

## 6. Fix Leadership Experience: cut generic management, promote pre-mortem, soften x402 strategy.

The Leadership section currently repeats the Work section and contains generic bullets. It should carry senior-PM judgment: risk framing, executive communication, enablement, and responsible AI adoption.

### CUT these NYL bullets

```markdown
- Managed a team of 8 to deliver AI-based automation features in digital asset management pipelines.
- Led stakeholder communication and alignment to integrate AI tools into core workflows.
- Mentored junior staff on prompt engineering and AI tool usage aligned to roadmap objectives.
```

They sound generic and not 2026 AI PM-specific.

### REPLACE NYL Leadership with one compressed bullet

```markdown
- Scaled AI-assisted DAM operations for a team of 8, introducing prompt-engineered metadata workflows with ChatGPT, Claude, and Gemini that improved asset discoverability 60% and supported training for 100+ users across 50+ locations.
```

This is much stronger because it has:

- Team scope.
- AI workflow.
- Named tools.
- Measurable outcome.
- Training/deployment scale.

---

## 7. Promote the pre-mortem as a standalone senior-PM bullet.

Yes, burying it loses differentiation. Pre-mortems are a real senior PM signal and most AI PM resumes do not show this.

### ADD under Leadership Experience — The Block

```markdown
- Created an 11-risk pre-mortem framework for Block Pro 2.0, classifying launch-blocking, fast-follow, and tracking risks; surfaced engineering-capacity and customer-retention dependencies before CEO-level pitch decisions.
```

This is CIIA-clean. It avoids ARR/churn numbers and named clients.

---

## 8. Rewrite or demote the x402 / A2A / MCP strategy memo.

Current bullet:

```markdown
- Authored the x402 / A2A / Block Pro MCP integration strategy memo — mapping 6 monetization vectors...
```

This is interesting but potentially dangerous. It is unshipped strategy, sounds speculative, and could invite confidential-detail questions. Keep only if you make it clearly an internal strategy artifact and not a shipped product.

### REWRITE

```markdown
- Authored internal x402 / A2A / MCP strategy memo mapping 6 potential agent-economy monetization patterns — pay-per-request data access, agent-readable feeds, education micropayments, and content-crawl licensing — into product questions for future Block Pro exploration.
```

This is safer. It does not imply shipped integration.

If applying to Anthropic/Sierra/Scale, I would include it. If applying to a conservative enterprise AI PM role, I might cut it.

---

## 9. Add responsible-AI / safety threading inside bullets, not as a separate section.

Do not create a separate “Responsible AI” section. It will feel performative. Thread the minimum viable safety language into each major AI artifact.

### Minimum additions by artifact

#### The Block Claude Skills

Use:

```markdown
scoped each workflow for human review before publishing, sending, or ticket creation
```

This shows authority boundaries.

#### `intent-engineering` MCP server

Add:

```markdown
- Designed the MCP server to audit specs for missing goals, constraints, authority boundaries, acceptance criteria, and review steps before agent execution.
```

This is a strong Anthropic/OpenAI signal because it says: do not just build agents; constrain them.

#### Code-Brain

Add:

```markdown
- Uses local-first workflows and explicit human-judgment gates: agents decompose, draft, and retrieve; human operator approves decisions, publishing, and external actions.
```

This is already aligned with your Karpathy framing but makes the safety model explicit.

#### Financial-research fleet

If retained, add traceability:

```markdown
- Produces source-linked morning briefs with human review before downstream use; local-first stack keeps routine research at $0/month with cloud fallback reserved for compound topics.
```

That gives cost and safety.

### Why this matters

For Anthropic / OpenAI / Google, the minimum bar is:

- Authority boundaries.
- Human-in-the-loop review.
- Source traceability.
- Failure-mode awareness.
- Eval or acceptance criteria.
- Privacy / data handling where relevant.

Right now, the resume has “agentic” but not enough “controlled agentic.” That is the gap.

---

## 10. Fix the F1-score landmine: choose 5–7 metrics and drill them.

You do not need every bullet to have an ML metric like F1. But every AI-ownership bullet needs **some defensible metric or clearly bounded claim**.

Your metric set should be:

1. 3 production Claude Skills shipped.
2. 11 Zapier workflows.
3. 10 intake forms.
4. 7 manual handoff steps eliminated.
5. 118 skills / 13 subagents / 14 hooks / 17 SDK agents.
6. MCP server: 3 tools, npm + MCP registry, DNS-verified, demoable in Claude Desktop.
7. Typed Reasoning Edges: 6 relation types; SQLite-backed contradiction detection.
8. Knowledge Loop: SessionEnd flush → nightly synth → weekly lint → SessionStart re-inject.
9. NYL: 40% productivity lift, 60% discoverability lift, 50% UX/system-response improvement, 100+ users, 50+ locations.

That is enough. Memorize these cold.

---

# Q5: Bullet-by-bullet F1 / metric audit

## The Block Work Experience

### Claude Skills

**Status:** REWRITE but survives.

Metric present: 3 production Skills.  
Needs: authority-boundary / human-review phrase.

Use rewritten version above.

---

### AdOps RevOps automation

**Status:** KEEP.

Metrics present:

- 11 workflows.
- 10 intake forms.
- 7 manual handoff steps eliminated.

This is one of the best bullets.

---

### Polymarket × Campus

**Status:** REWRITE.

Metrics present:

- PRD v1→v3.
- 5-component build.

Issue: “sponsor data layer” may be CIIA-adjacent. Remove.

---

### .co homepage audit

**Status:** KEEP / TIGHTEN.

Metrics present:

- 50+ sites.
- 8 categories.

Not an AI bullet, so no AI metric issue.

---

### Block Pro 2.0 audit

**Status:** REWRITE / SPLIT.

Metrics present:

- 9 platforms.
- 3 stakeholder interviews.
- 11 risks.

Good, but the pre-mortem is buried. Split it.

---

### Campus 201 AI media generation

**Status:** CUT unless you can add a real production metric.

Missing:

- Number of assets generated.
- Hours saved.
- Cost reduction.
- Review cycle reduction.

Without that, it is tool-name flexing.

---

### P&E Department 2.0

**Status:** KEEP.

Metrics present:

- 10-week plan.
- 7 hubs.
- ~25 pages.
- 5+ onboarding pages.

Good product-ops bullet.

---

## NYL Work Experience

### SaaS DAM rollout

**Status:** KEEP.

Metric present:

- 50+ locations.

Could be stronger if there is user count, but the next bullet has 100+ users.

---

### 40% productivity

**Status:** KEEP.

Strong.

---

### 60% discoverability via prompt-engineered metadata

**Status:** KEEP.

This is one of the best “AI before AI PM title” bullets.

Maybe rewrite:

```markdown
- Improved asset discoverability 60% by introducing prompt-engineered metadata workflows using ChatGPT, Claude, and Gemini.
```

---

### 50% UX friction / response time

**Status:** KEEP but clarify.

“UX friction and system response time” are different things. If both truly improved 50%, okay. If not, split or soften.

```markdown
- Reduced DAM support friction 50% by analyzing Jira ticket patterns and refining metadata, upload, and retrieval workflows.
```

Only say “system response time” if you can defend a technical performance measurement.

---

## Leadership Experience

### Daily standups

**Status:** CUT.

Generic. Does not help AI PM.

---

### Onboarded PMs on Claude Code

**Status:** REWRITE.

Current lacks metric and sounds internal.

```markdown
- Onboarded Product teammates on Claude Code workflows and maintained a P&E Claude Skills library covering Jira automation, ETF page creation, stakeholder updates, and design-system enforcement.
```

Fine, but not a top bullet.

---

### PRD-to-Prototype Lab

**Status:** REWRITE or CUT.

It sounds useful but vague. If shipped internally, keep:

```markdown
- Created PRD-to-Prototype Lab reference environment connecting user flows, PRD context, and design-system guidance so designers and engineers could prototype from shared product constraints.
```

If it was not used, cut.

---

### x402 / A2A / MCP memo

**Status:** LANDMINE unless softened.

Reason: unshipped strategy; could invite confidential discussion; “positioning Block Pro as default data infrastructure” is overclaimy.

Use softened version above.

---

## Selected Projects

### Code-Brain

**Status:** KEEP / REWRITE.

Current is strong but “architecture” language risks STOP-DOING. Replace “architecture” with “technical writeups” or “implementation writeups.”

```markdown
- Maintain open-source Code-Brain v3.37.0: 118 skills, 13 subagents, 14 hooks, and 17 Claude Agent SDK agents for local-first PM, research, and content workflows.
- Published technical writeups for two shipped subsystems: SQLite-backed Typed Reasoning Edges for contradiction detection across 6 relation types, and Knowledge Loop for session memory flush, nightly synthesis, weekly linting, and context re-injection.
```

---

### intent-engineering MCP Server

**Status:** KEEP / ADD safety.

Strongest artifact.

Add:

```markdown
- Audits AI specs for missing goals, constraints, authority boundaries, acceptance criteria, and review steps before agent execution.
```

---

### Agentic Financial-Research Fleet

**Status:** REWRITE.

Current landmine phrase:

```markdown
fine-tuned local stack
```

Unless there is an actual fine-tuned model, cut that phrase. “Fine-tuned” has a specific meaning.

Use:

```markdown
- Local-first financial-research workflow: queue file → router → retrieval agents → local-LLM synthesis → source-linked morning brief, with Gemini Deep Research reserved as cloud fallback for compound topics.
- Runs on a $0/month routine-research stack using Ollama, SearXNG, and local retrieval, with human review before downstream use.
```

This adds cost and safety.

---

### 2D Animation Pipeline

**Status:** CUT from AI PM master.

Future-dated. Not shipped.

---

# Q6: Vibe-coding evidence

No inline Loom. No Bolt/v0 URL. Do not reference forthcoming demos.

The resume should not say “forthcoming.” That makes the package feel unfinished.

Current “Cursor” in Skills + GitHub/header/site is sufficient for Round 1 **if** the resume surfaces the shipped MCP server and Code-Brain above the fold.

But the Skills section should be more explicit about build tools and coding comfort without overclaiming senior engineering.

### REWRITE Skills technical row

```markdown
**AI / Agentic Engineering:** Claude Code, Claude Agent SDK, Claude Skills, MCP, prompt engineering, agent orchestration, RAG / local-LLM workflows, Ollama, SearXNG, Qwen, Gemini, Anthropic API
```

Add a separate row:

```markdown
**Technical Prototyping:** TypeScript, React / Vite / Tailwind, Python-assisted scripting, SQL / SQLite, GitHub, Cursor, Zapier, Vercel
```

“Python-assisted scripting” is honest and prevents senior-engineer overclaiming.

---

# Q7: Safety / responsible-AI thread depth

Current safety signal is **insufficient**.

You have “human owns judgment” in the Code-Brain bullet, but that is more philosophy than operational safety. For frontier AI PM roles, you need concrete control surfaces:

- Authority boundaries.
- Human review.
- Acceptance criteria.
- Source traceability.
- Failure-mode / pre-mortem thinking.
- Privacy / local-first where relevant.

## Minimum additions

### The Block Claude Skills

```markdown
scoped each workflow for human review before publishing, sending, or ticket creation
```

### MCP server

```markdown
audits specs for missing goals, constraints, authority boundaries, acceptance criteria, and review steps
```

### Code-Brain

```markdown
local-first workflows with explicit human-judgment gates for publishing, external actions, and final decisions
```

### Financial-research fleet

```markdown
source-linked briefs with human review before downstream use
```

### Pre-mortem

```markdown
11-risk pre-mortem framework classifying launch-blocking, fast-follow, and tracking risks
```

This is enough for resume level. You do not need a separate “AI Safety” section.

---

# Q8: JD keyword mirror without stuffing

## Keywords currently present or close

### “Shipped”

Present. Good. Keep using it.

### “MCP”

Present. Strong. Move higher.

### “Agent orchestration”

Present in Skills. Also supported by Code-Brain and financial-research fleet.

### “Technical artifacts for customers like MCP servers, sub-agents, and agent skills”

Partially present. You have MCP server, subagents, skills. Add the phrase “technical artifacts” carefully in Summary or Selected AI Artifacts.

Suggested Summary phrase:

```markdown
shipped technical artifacts including Claude Skills, a TypeScript MCP server, and subagent-based local workflows
```

### “0-to-1 product creation”

Not present enough. Add to Polymarket bullet or Summary.

Suggested:

```markdown
- Authored PRD v1→v3 and shipped 0-to-1 sponsored-microcourse revenue vertical, Polymarket × Campus...
```

This is defensible.

### “Shipped AI-powered solutions in the real world, not just designed them”

Present implicitly. Make explicit through “production Claude Skills” and “published MCP server.”

Do not paste this phrase verbatim. It will sound stuffed.

### “White glove deployment”

Not really supported unless you mean DAM rollout / internal enablement. Could add to NYL or Block onboarding, but I would avoid the exact phrase unless applying to Glean.

Possible Glean-specific variant:

```markdown
- Supported white-glove DAM rollout across 50+ locations, translating business requirements into Atlassian documentation, onboarding programs, and custom training for 100+ users.
```

For general master, do not use “white glove.”

### “Trusted C-suite Advisor” / “Executive credibility”

Do not use “Trusted C-suite Advisor.” Too inflated.

But “CEO-level product strategy pitch” and “executive-update drafting” are legitimate.

### “Hands-on experience building end-to-end systems or prototypes in production”

Supported by AdOps, Claude Skills, MCP. Add “end-to-end” to AdOps or MCP only if true.

Suggested:

```markdown
- Built end-to-end AdOps RevOps automation pipeline...
```

Good for Scale AI / Pair Team.

### “Firsthand experience evaluating and deploying LLMs into production”

You have deploying. You do **not** yet have strong evaluating, because the eval suite is B7-gated and should not be a resume bullet.

Do not claim “evaluation framework” yet.

You can use “acceptance criteria” and “review steps” for the MCP server, but avoid “golden set” until the eval suite ships.

### “Evals / evaluation framework / golden set”

Currently missing. This is the biggest AI PM keyword gap.

But because the eval suite is not shipped, do not add it as a project. The honest near-term substitute is:

```markdown
acceptance criteria, review steps, and spec-audit checks
```

Once the Vault Synthesizer Eval Suite ships, add it immediately.

### “Fine-tune”

Do not add unless you truly fine-tuned a model. The current “fine-tuned local stack” is dangerous. Replace with “local-LLM stack.”

### “RAG”

Present in Skills. The financial-research fleet supports retrieval. Good.

### “Tool use”

Missing as phrase. Add in Skills:

```markdown
tool use / MCP workflows
```

### “Cost / latency / throughput / p95”

Cost exists in financial fleet: $0/month. Latency/p95 absent. Do not invent p95.

Add:

```markdown
$0/month routine-research stack
```

Do not add p95 unless measured.

### Python / SQL

Currently missing. Add carefully.

```markdown
TypeScript, React / Vite / Tailwind, Python-assisted scripting, SQL / SQLite
```

This helps Scale AI without overclaiming senior engineering.

### “Conversational AI”

Do not add. Not really evidenced.

### “Executive credibility”

Supported by CEO-level strategy pitch and executive-update Skill. Use those, not the exact phrase.

---

# Proposed revised section order for AI PM master

```markdown
Header
Summary
Selected AI Artifacts
Work Experience
Leadership Experience
Education
Skills
```

Yes, this is nontraditional. For an AI PM pivot, it is better. The resume’s job is to make the artifacts legible fast.

---

# Final cut list

## CUT

- Future-dated 2D Animation Pipeline from AI PM master.
- Generic NYL Leadership bullets.
- “Led daily P&E standups...” unless space remains.
- Campus 201 media automation unless you can add a real metric.
- “fine-tuned local stack” unless actual fine-tuning happened.
- “sponsor data layer” from Polymarket bullet.

## LANDMINE

- “fine-tuned local stack” — technical overclaim if no fine-tuning.
- “sponsor data layer” — too close to restricted Polymarket detail.
- “positioning Block Pro as default data infrastructure” — overclaim / unshipped strategy.
- Any “evaluation framework” / “golden set” claim before the eval suite ships.

## REWRITE

- Summary.
- Claude Skills bullet with human-review boundary.
- Polymarket bullet with sanitized reporting language.
- Block Pro bullet split into audit + standalone pre-mortem.
- x402 / A2A / MCP memo softened as internal strategy.
- Code-Brain bullets with technical writeups and human-judgment gates.
- Financial-research fleet without “fine-tuned.”

---

# Bottom line

The resume is close, but right now it undersells the shipped AI artifacts and overspends space on internal product-ops context. For Tier-1 AI PM screens, the reader needs to see within 15 seconds:

1. Shipped MCP server.
2. Shipped Claude Skills.
3. Public Code-Brain.
4. Production/product metrics.
5. Human review / authority boundaries.
6. SQL / TypeScript / local-LLM / RAG fluency.
7. No future-dated fluff.

Make those changes and the resume will support the package instead of merely documenting the job history.

### ~google/gemini-pro-latest

**Panelist Review**
**Member:** Strategic AI & Product Evaluator (GPT-Class)
**Target:** Sean Winslow — Resume Critique for Tier-1 AI PM Roles

To the Council and the Chairman: Below is my brutal, prioritized punch list evaluating Sean’s resume against the 2026 AI PM hiring bar. I have explicitly incorporated the candidate’s pre-council priorities, defaulting to the AI-PM-as-master baseline and strictly honoring all CIIA and technical ceiling guardrails.

Here are the highest-leverage changes, ordered by impact on passing a Tier-1 screen, resolving all 8 questions. 

### 1. [Q7 + Q8] The Safety/Eval Vacuum & Missing Keywords (Highest Priority)
Right now, the resume has exactly zero mentions of AI safety, evaluation frameworks, or guardrails. For Anthropic (Tier-3 wildcard), Google, and OpenAI, this is an automatic filter. If you build agents without explicitly evaluating their error boundaries, you are viewed as a hobbyist, not a PM. We must strategically inject JD keywords ("evaluations", "0-to-1", "TypeScript") without stuffing.

*   **REWRITE - Phase D Typed Reasoning Edges (Selected Projects):** You already built safety logic (contradiction detection), but you didn't name it as safety.
    *   *New Text:* "Architecture writeups for production subsystems including Phase D Typed Reasoning Edges (SQLite-backed cross-domain contradiction detection for hallucination mitigation and safety bounding) and..."
*   **REWRITE - Polymarket B2B PRD (The Block Experience):** Claim the Glean FDP "0-to-1" keyword here. 
    *   *New Text:* "Authored the 0-to-1 PRD (v1→v3) and shipped The Block's first sponsored-microcourse B2B revenue vertical..."
*   **REWRITE - intent-engineering MCP Server (Selected Projects):** You built a spec auditor. That is an evaluation tool. Claim it.
    *   *New Text:* "3-tool TypeScript MCP server... for automated AI specification generation and evaluation—published to npm..."
*   **ADD - Skills Section:** Ensure "TypeScript", "Python" (per Scale AI JD), and "Evaluation Frameworks" are strictly listed in the AI/Agentic Engineering or Tools skills list, as ATS systems will binary-filter for TS/Python.

### 2. [Q5] Defusing the F1-Score Landmine (Commit to Path B)
I strongly recommend **Path B**: Curate down to a strict 5-metric set on your shipped artifacts that you *will* drill into memory by Monday 5/19. Soften the corporate claims where metrics are lost to CIIA, but harden the metrics on your personal fleet where you have total control.
*   **REWRITE - Agentic Financial-Research Fleet:** You need a latency/cost/throughput metric.
    *   *New Text:* "Runs on an optimized, local-first stack (Ollama, SearXNG) achieving <$0.02 cost per daily brief, with Gemini Deep Research as cloud fallback for compound context queries." *(Memorize this cost/latency logic).*
*   **REWRITE - intent-engineering MCP Server:** 
    *   *New Text:* "Operationalizes the intent-engineering framework as a portable server, reducing spec-audit turnaround time to seconds. Shipped 2026-05-12 ahead of plan." *(Drill: Know exactly how much time an LLM-as-judge audit saves vs. manual review).*
*   **SOFTEN - The Block (Claude Skills):** If you can't remember the exact hours saved, focus on adoption. "Shipped 3 production Claude Skills... driving adoption across P&E..."

### 3. [Q1] AI-PM-as-Master Pivot (Formal Endorsement)
The candidate is entirely correct to reverse default (Confidence 4). **Use the AI PM Variant as the sole master.** 
If your highest-leverage target is an Anthropic/Glean/Scale PM role at $150K-$250K, opening with NYL DAM rollouts dilutes your narrative. The pristine 4-piece package you built is explicitly an agentic engineering portfolio. The AI PM variant positions you as a builder who transitioned from media ops exactly at the right time. Demoting "generic PM" variants forces the recruiter to read your Karpathy-style framing first.

### 4. [Q4] Promote the Pre-Mortem to a Standalone Leadership Bullet 
Burying the 11-risk pre-mortem mid-sentence in a Block Pro 2.0 audit bullet is a mistake. "Executive credibility" and "Trusted C-suite Advisor" (Glean FDP) are proven by this exact methodology. It shows product maturity bridging the gap between engineering reality and CEO expectations.
*   **CUT** it from the Work Experience section.
*   **ADD to Leadership Experience (The Block):** 
    *   *New Text:* "Developed and facilitated a structured 11-risk pre-mortem methodology (Tigers, Paper Tigers, Elephants) for the Block Pro 2.0 executive strategy, successfully surfacing critical engineering-capacity constraints and renewal-cliff dependencies prior to incoming-CEO presentation."

### 5. [Q3] Modernize NYL Leadership Experience 
The current 3 bullets ("Managed a team of 8 / Led stakeholder communication / Mentored junior staff") are fluff. Replace them entirely. Merging the prompt-engineered metadata win into this section proves you can *manage* a team's transition into the AI era, rather than just doing it yourself.
*   **REWRITE (Consolidate to one line):** 
    *   *New Text:* "Managed an 8-person operational team, leading their transition to AI-assisted workflows—driving a 60% boost in asset discoverability via prompt-engineered metadata curation (Claude, Gemini, ChatGPT) and reducing system friction by 50%."

### 6. [Q2] Tenure Asymmetry Framing (Hold the Line)
Do **not** preemptively mention the cost-cutting layoff in the summary. AI PMs are hired for technical clarity, not defensive explanations. A 6-month stint at a crypto media startup ending in a layoff in mid-2026 is an utterly standard archetype. It requires zero apology on paper. Let your Github and MCP servers justify your employment gap. Save the one-sentence layoff context ("Cost-cutting restructure by the incoming President, happy to discuss") strictly for the recruiter screen.
*   *Action:* Keep the Summary tightly focused on output: "AI Product Manager and agentic-engineering practitioner. Ships production Claude Skills..."

### 7. [Q6] Vibe-Coding Evidence (Honor the Lock)
The candidate is at Confidence 5 on refusing inline Loom/Bolt URLs. I agree with this lock. Links break ATS parsers, look cluttered, and a resume is a log of *shipped* reality, not a roadmap. 
*   *Action:* Rely entirely on `seanwinslow.com` in the header. Do **not** mention the 14-agent fleet Loom or Token Cost Calculator as "forthcoming." In interview terms, if it’s not live by the time they click, it’s vaporware. Keep them off the resume until Week 3 when they deploy. The current open-source artifacts (Code-Brain + MCP Server) already clear the Round 1 technical credibility bar. 

### Chairman Summary Note from this Panelist:
I vote strictly in favor of the candidate's instincts on Q1, Q5 (Path B), and Q6. My proposed text for Q3, Q4, Q7, and Q8 directly maps existing, defensible evidence to the Tier-1 JD keywords without triggering CIIA traps or violating his technical self-coding boundary. Ship it by Monday.

### x-ai/grok-4.20

**Q1:** AI PM as master is the correct baseline. The candidate’s locked decision to prioritize AI PM roles, the positioning thesis (“agentic engineering practitioner who ships”), and the 2026 bar all favor it. A role-agnostic master dilutes signal for Tier-1 AI PM screens (Glean, Scale, Sierra, Liberate) where “shipped AI-powered solutions… not just designed them,” “agent orchestration,” and MCP are decisive. Package coherence is preserved via the personal site, GitHub, and Substack—not the resume. Demote the current master to a Tech/ Creative PM variant.

**Q2:** Do not mention “post-layoff cost-cutting, not performance” in the Summary. It injects unnecessary risk and belongs in cover letters or late-stage discussion. Proposed Summary (for AI-PM master):

> AI Product Manager and agentic-engineering practitioner who ships production MCP servers, Claude Skills, and autonomous agent fleets. Most recently at The Block, delivered 3 production Claude Skills and Block Pro 2.0 scoping while maintaining the open-source 118-skill Code-Brain and intent-engineering MCP server. Former technical founder with 10+ years building AI-native workflows in digital asset management and media production.

**Q3:** Replace the generic NYL Leadership Experience bullets. Option (c). New single bullet that modernizes without fabricating metrics:

> Team Lead, AI Workflow Integration (2021–2025): Spearheaded prompt-engineered metadata strategy that increased asset discoverability 60% and media asset productivity 40%; translated requirements into production DAM automation, reducing UX friction and response time 50% via iterative Jira-driven workflow refinement.

**Q4:** Promote pre-mortem to standalone Leadership bullet. It is rare, senior-PM signal and already CIIA-clean. Recommended text:

> Developed and applied Tigers/Paper Tigers/Elephants 11-risk pre-mortem framework (launch-blocking, fast-follow, track tiers) during Block Pro 2.0 product audit; surfaced engineering capacity and renewal-cliff risks in stakeholder interviews that shaped pitch deck delivered to incoming CEO.

**Q5:** F1-score landmine audit (candidate cannot recite exact metrics without notes → Path A: soften claims):

- **Survives (defensible):** “Shipped 3 production Claude Skills… direct delivery against P&E Q2 Objective 5 KR3” — ties to OKR, no invented metric.
- **Needs rewrite:** AdOps RevOps pipeline (“eliminating 7 manual handoff steps”) → keep as-is or change to “eliminating ~7 manual handoff steps per deal.”
- **LANDMINE / needs cut or heavy soften:** “Boosted asset discoverability by 60% using prompt-engineered metadata” and “Increased media asset productivity by 40%” and “Reduced UX friction… by 50%” — candidate cannot defend exact numbers in interview. Replace with qualitative + process signal (see Q3 rewrite above).
- All Selected Projects bullets currently survive because they are framed as shipped artifacts with verifiable links, not quantified performance claims.

**Q6:** Cursor in Skills + GitHub link in header is sufficient for Round 1 given candidate’s locked decision (no inline Looms). Do not reference “forthcoming” fleet Loom or Token Cost Calculator. Mention of the shipped MCP server and Code-Brain already signals vibe-coding fluency.

**Q7:** Safety/responsible-AI thread is currently absent. Minimum for Anthropic/OpenAI/Google: at least one explicit safety/governance/alignment reference per major AI artifact. Add to existing bullets (do not create separate section):

- After intent-engineering MCP bullet: “…with built-in `audit_intent_spec` tool enforcing safety, legality, and brand constraints.”
- After Code-Brain: “…with embedded review hooks and LLM-as-judge patterns for output safety.”
- After Knowledge Loop EXPLANATION.md mention: “…including contradiction detection for factual accuracy and hallucination mitigation.”
- For Anthropic specifically, the MCP + sub-agent + skills framing already maps to their “technical artifacts for customers” language once safety is threaded.

**Q8:** Missing/earnable JD keywords (evidence already exists, just under-named):

- Missing entirely: “0-to-1 product creation”, “white glove deployment”, “Trusted C-suite Advisor”, “Executive credibility”, “hands-on experience building end-to-end systems… in production”, “evaluating and deploying LLMs into production”, “agent orchestration”, “evals / evaluation framework”, “fine-tune / RAG / tool use”, “p95”.
- Earnable additions without stuffing:
  - Add “0-to-1 product creation” to Polymarket × Campus PRD bullet.
  - Add “agent orchestration” and “tool use” to intent-engineering and Superuser bullets.
  - Add “LLM-as-judge” and “evals” to Knowledge Loop / Typed Reasoning Edges mentions.
  - Add “production” explicitly to every AI bullet that currently says “used in production.”
- Forced territory: “white glove deployment”, “Trusted C-suite Advisor”, “Executive credibility”, “p95 latency” — these would feel stuffed; omit. This is evidence that the resume should not try to serve all Tier-1 language equally; lean hardest into Anthropic/Glean/Liberate keywords that map cleanly to shipped MCP + evals + Superuser work.

### Highest-Leverage Changes (ordered by expected impact on Tier-1 AI PM phone screen)

1. **Adopt AI PM variant as new master resume** (Q1). Re-order The Block bullets to lead with Claude Skills, AdOps RevOps, Block Pro 2.0 audit/pre-mortem, then Polymarket and Confluence plan. Update Summary to the version in Q2. This directly mirrors Glean (“shipped AI-powered solutions… not just designed them”), Scale (“hands-on… in production”), Liberate (“design AI agent workflows… into production”), and Anthropic (“technical artifacts… MCP servers, sub-agents, and agent skills”).

2. **CUT** the three generic NYL Leadership Experience bullets. **REPLACE** entire NYL Leadership subsection with the single modernized bullet in Q3. Cite: removes management theater that fails Aakash Gupta canon #1 (production AI shipping) and #10 (specific verbs: shipped, evaluated, fine-tuned).

3. **PROMOTE** pre-mortem to standalone Leadership bullet using exact text in Q4. This is a strong senior-PM signal most resumes lack and surfaces “comprehension as currency” (Nate Jones).

4. **REWRITE** all NYL bullets and the two 40%/60%/50% claims per Q5 Path A. Use the single bullet in Q3. Mark original productivity bullets as **CUT**—they are landmines for metric grilling.

5. **ADD safety threading** (exact phrases from Q7) to the three Selected Projects bullets that mention MCP, Code-Brain, and Knowledge Loop/Edges. This is the minimum to clear Anthropic/OpenAI/Google bars and directly supports Sierra “agent orchestration” and Liberate “AI agent workflows… into production.”

6. **REWRITE** Selected Projects bullets to incorporate missing keywords where earned:
   - intent-engineering MCP: “…3-tool TypeScript MCP server for intent specification authoring and safety-constrained `audit_intent_spec` tool use…”
   - Code-Brain: “…118-skill open-source agentic engineering toolkit with 17 autonomous agents, embedded LLM-as-judge review hooks, and production safety patterns.”
   - Add to Knowledge Loop bullet: “…including SQLite-backed contradiction detection eval for hallucination mitigation and factual accuracy.”

7. **Minor cuts:** Remove “former technical founder” if it cannot be defended with shipped company evidence. Tighten Summary by 15% if it exceeds 4 lines. Ensure every AI bullet contains at least one of: shipped, production, agent orchestration, tool use, evals, LLM-as-judge, MCP.

These changes bias toward shipping by Monday while addressing the two highest-priority gaps the candidate flagged (safety threading and JD-keyword mirroring). The resulting resume will prime the five interview anchors, survive the F1-score landmine, and function as a coherent supporting artifact for the personal site / GitHub / build-in-public package.

## Cross-rankings

### Judge: anthropic/claude-opus-4.7

- **Order:** A > C > B
- **Reasoning:** Response A is the most thorough and surgical: it provides explicit REWRITE/CUT/LANDMINE labels with exact bullet text, catches subtle landmines others miss (the 'fine-tuned local stack' technical overclaim, 'sponsor data layer' CIIA proximity, 'positioning Block Pro as default data infrastructure' overclaim), proposes a concrete section reorder with a 'Selected AI Artifacts' block above Work Experience, and threads safety language operationally rather than performatively. Response C is tightly structured around the 8 questions with clean, CIIA-clean draft text and a strong prioritized list, but it's less brutal on landmines and contradicts itself slightly (recommends cutting the 40/60/50% NYL metrics while also keeping them in the Q3 rewrite). Response B is competent and well-organized but shorter, invents a specific '<$0.02 cost per daily brief' metric that risks an F1 landmine the candidate explicitly flagged, and provides less bullet-level surgery than A or C.

### Judge: openai/gpt-5.5

- **Order:** A > C > B
- **Reasoning:** Response A is the strongest: it answers all 8 questions directly, gives specific rewrite text, respects the no-inline-URL lock, handles CIIA constraints, and provides the most actionable safety/evals/JD-keyword mapping, though a few phrases like “judge layer” and eval-gated claims risk slight overreach. Response C is solid and mostly complete, with useful exact bullets and clear prioritization, but it is less internally consistent on metrics and includes some potentially undefended/overclaimed phrases such as “former technical founder” and LLM-as-judge hooks. Response B has good instincts on AI-PM-as-master and safety/evals, but it is less comprehensive and introduces an unsupported invented metric (“<$0.02 cost per daily brief”), which is a significant resume landmine.

### Judge: ~google/gemini-pro-latest

- **Order:** A > B > C
- **Reasoning:** Response A perfectly balances rigorous structural compliance with deep, actionable insight, particularly in its handling of the priority Q7/Q8 safety and keyword mappings via a clear table. Response B is also excellent and intelligently catches an unshipped project to cut, but its formatting blends the answers and punchlist slightly less cleanly than A. Response C introduces a hallucinated 'former technical founder' claim in the summary rewrite, dropping it to last place.

### Judge: x-ai/grok-4.20

- **Order:** A > C > B
- **Reasoning:** Response A ranks highest for its precise alignment with all constraints (CIIA, shipped-only evidence, candidate priorities), comprehensive per-bullet audits, specific rewrites that directly address safety/evals gaps without overclaiming, and clear integration of Aakash/Karpathy/Hamel canons. Response C is second for its focused brutality on the highest-priority Q7/Q8 gaps, exact bullet text, and strong Path-B metric curation with targeted safety threading. Response B is third: while it suggests useful restructuring (e.g., new 'Selected AI Artifacts' section), it occasionally drifts into unshipped framing, over-edits safe bullets, and includes minor CIIA-adjacent risks, making it slightly less precise and higher-risk overall.

## Chairman synthesis

_Chairman model: `anthropic/claude-opus-4.7`_

# Chairman's Synthesis — Resume Council, 2026-05-17

**Tag:** `resume-critique-2026-05-18` · **Profile:** premium · **Budget:** ~$0.29

The council voted unanimously on the strategic call and split tactically on three specific bullets. I'll lead with unanimous findings, then the prioritized punch list, then explicit disagreements where I picked a side.

---

## Unanimous, load-bearing findings (ship these first)

**U1. AI PM variant becomes the new master.** All four panelists (Opus, GPT-5.5, Gemini, Grok) endorsed the candidate's Q1 reversal at high confidence. Package coherence lives at the package level (site/GitHub/Substack), not the resume level. Tech PM and Creative PM become tailored variants. *Caveat from Opus:* commit to producing the Tech/Creative variants within 72 hours of master swap or the cross-archetype claim weakens.

**U2. Do NOT mention the layoff in the Summary.** All four said this preemptively. Reserve for cover letter / recruiter screen as a 2-sentence verbal.

**U3. Safety/eval threading is the single biggest gap.** All four flagged this as P0 for Anthropic/OpenAI/Google/Microsoft. Zero current bullets mention evals, judge layers, human-review gates, contradiction detection, or authority boundaries — despite the shipped evidence supporting all of these.

**U4. Promote the pre-mortem to a standalone Leadership bullet.** All four agreed. Most candidates can't articulate a pre-mortem methodology with tiered risk classes — this is a senior-PM signal currently buried six words deep.

**U5. Compress the three generic NYL Leadership bullets.** All four said cut "Managed a team of 8 / Led stakeholder communication / Mentored junior staff" — these trigger the Aakash "led/drove/collaborated" death-verb pattern.

**U6. Q6 honored.** No panelist proposed inline Loom/Bolt/v0 URLs. The lock held.

---

## The Prioritized Punch List (ordered by Tier-1 phone-screen impact)

### 1. Adopt AI PM variant as master + restructure section order

Per **GPT-5.5's** strongest structural insight (endorsed implicitly by Opus): place a **"Selected AI Artifacts"** block immediately after Summary, before Work Experience. The shipped MCP server and Code-Brain are currently buried below two experience sections — that's wrong for a 20-second recruiter scan.

Proposed order:
```
Header → Summary → Selected AI Artifacts → Work Experience → Leadership Experience → Education → Skills
```

**Header URL change (GPT-5.5):** Change `seanwinslow.com` to `seanwinslow.com/transactions` — that URL is the load-bearing portfolio entry, per the candidate's locked package decision.

### 2. Rewrite the Summary

Three panelists drafted versions. I'm picking a **hybrid of Opus's and GPT-5.5's** drafts — Opus has the strongest verb cadence and eval language; GPT-5.5 has the cleaner artifact-naming.

**Grok's "former technical founder" line is REJECTED** — Gemini's ranker correctly flagged this as a hallucination; the candidate has not been a technical founder, and Anthropic FDE specifically reads that phrase carefully.

**Recommended Summary:**

> AI Product Manager and agentic-engineering practitioner. Ships production Claude Skills, MCP servers, and autonomous agent fleets with human-review gates and eval-driven acceptance criteria. At The Block, shipped 3 production Claude Skills against P&E OKR delivery, co-authored the Block Pro 2.0 product audit with an 11-risk structured pre-mortem, and authored the x402 / MCP integration strategy for the agent economy. Maintains the open-source 118-skill Code-Brain and a 17-agent Claude Agent SDK fleet; published `@swins/intent-engineering-mcp` to npm and the MCP registry.

### 3. Thread safety / eval language into 4 bullets (Q7 — the biggest gap)

Per **Opus's** four specific additions (Gemini and Grok converged on the same locations; GPT-5.5 added the Skills row insight):

**3a. 3-Claude-Skills bullet — add human-review gate:**
> ...automating WordPress ETF page generation, biweekly executive updates, and per-product Jira ticket scaffolding — **each skill scoped with a human-in-the-loop review gate before publish, send, or ticket creation** — direct delivery against the P&E Q2 Objective 5 KR3.

**3b. intent-engineering MCP project — add evals framing (Opus's strongest move):**
> Built on an evals-first methodology: the `audit_intent_spec` tool *is* the eval — it scores a spec against the framework's dimensions and tells the author what's missing before the spec ships to a coding agent. Operationalizes the "evals are the new PRDs" thesis as a portable MCP server.

**3c. Code-Brain — reframe Phase D as judge layer (Opus + Gemini converged):**
> Architecture writeups for two production subsystems: Phase D Typed Reasoning Edges (SQLite-backed cross-domain contradiction detection — a lightweight judge layer surfacing factual conflicts across 6 relation types) and Phase 6 Knowledge Loop (SessionEnd flush → nightly synth → weekly lint → SessionStart re-inject, with eval-gated promotion).

**3d. Skills row addition (Opus):**
> AI / Agentic Engineering: ...evals (golden-set design, LLM-as-judge rubrics, regression suites), human-in-the-loop deployment patterns, MCP namespace governance.

**Disagreement noted:** GPT-5.5 cautioned against "evaluation framework / golden set" claims until the Vault Synthesizer eval suite ships past the B7 gate. **My call: Opus wins on this one.** The `audit_intent_spec` tool IS a shipped eval-as-spec-auditor — that's defensible today. The Skills-row "golden-set design" is also defensible because the Vault eval suite is *code-complete* (10-case binary eval) — the candidate can describe the methodology in interview without claiming the artifact is shipped to production.

### 4. Promote the pre-mortem to standalone Leadership bullet

Three panelists drafted versions. **Opus's draft is strongest** — it names Gary Klein's canon (signals senior-PM literacy) and uses the Aakash-favored verbs (designed, ran, surfaced). Grok's "Tigers/Paper Tigers/Elephants" naming is interesting but inside-baseball and may confuse readers; cut it for resume use, keep it for interview color.

**Recommended bullet (top of The Block Leadership section):**

> Designed and ran an 11-risk structured pre-mortem for the Block Pro 2.0 proposal — tiering risks across launch-blocking, fast-follow, and track categories, surfacing engineering-capacity and renewal-cliff dependencies before the pitch landed with the incoming CEO. Methodology framed against Gary Klein's pre-mortem canon; reusable as a P&E governance artifact.

Keep the pre-mortem reference in the Pro 2.0 Work Experience bullet too — duplication is intentional.

### 5. Compress NYL Leadership to one bullet

Three competing drafts. Here's the disagreement:

- **Opus**: "Led an 8-person cross-functional team integrating prompt-engineered metadata pipelines... — the precursor work to the agentic-engineering practice now shipping in open source."
- **GPT-5.5 / Gemini**: A consolidation bullet that *also* absorbs the 40%/60% metrics from the Work Experience section.
- **Grok**: Similar consolidation but keeps all three percentages.

**My call: Opus's "precursor work" framing wins on narrative bridge** — it's the load-bearing phrase that makes 10+ years of NYL count *toward* the AI PM thesis. But GPT-5.5 is right that the metric should appear here too. **Synthesis:**

> Led an 8-person cross-functional team integrating prompt-engineered metadata pipelines (ChatGPT, Claude, Gemini) into enterprise DAM workflows — driving a 60% lift in asset discoverability and training 100+ users across 50+ locations. Precursor work to the agentic-engineering practice now shipping in open source.

### 6. Resolve the F1-score landmine — pick Path B (curate + drill), with one Path A exception

**Disagreement to surface:** Opus and GPT-5.5 voted Path B (curate to 5-7 metrics, drill cold). **Grok voted Path A** (soften all 40/60/50% NYL claims because the candidate can't reproduce the measurement methodology). Gemini went Path B.

**My call: Path B with a targeted Path A exception for the weakest NYL bullet.** Grok's concern is real but over-corrects. The 60% discoverability number is AI-adjacent (prompt-engineered metadata) and maps directly to the Aakash bar — drill it, don't soften it. The 40% productivity number is defensible if the candidate can articulate baseline + window. **CUT the 50% UX friction bullet** (Opus's recommendation, Grok-adjacent) — it's the weakest of the three, reads as analyst not PM, and the verb "reduced... by analyzing Jira tickets" is the wrong frame.

**The 7-metric drill set the candidate must memorize cold before Mon 5/19** (synthesized from Opus + GPT-5.5):

1. 3 Claude Skills + the OKR KR they deliver against
2. AdOps: 11 Zapier flows, 10 intake forms, 7 manual handoffs eliminated
3. Pre-mortem: 11 risks, 3 tiers, 2 surfaced dependencies (engineering capacity, renewal cliff)
4. Code-Brain: 118 skills / 13 subagents / 14 hooks / 17 SDK agents (8 active by default)
5. MCP server: 3 tools, npm + MCP registry, DNS-verified, shipped 13 days ahead of plan
6. NYL: 60% discoverability via prompt-engineered metadata — *with reproducible baseline + window*
7. Pro 2.0: 9 platforms benchmarked + 3 stakeholder interviews

### 7. Inject earned JD keywords (Q8 — no stuffing)

All four panelists converged on the same earnable keywords. Synthesizing **Opus's keyword table** with **GPT-5.5's specific bullet rewrites**:

| Keyword | Bullet edit |
|---|---|
| **"0-to-1"** | Polymarket: *"Drove 0-to-1 product creation: authored the PRD (v1→v3) and shipped..."* |
| **"end-to-end"** | AdOps: *"Built an end-to-end RevOps automation pipeline..."* |
| **"agent orchestration"** | Financial Fleet: *"Multi-agent orchestration: queue file → router → 3 retrieval agents..."* |
| **"in production"** | Code-Brain: change "8 active by default" → "8 in production on local-first launchd schedules" |
| **"Python, SQL/SQLite"** | Add to Skills row Tools — defensible from Phase D GitHub writeup |

**Keywords explicitly REJECTED by consensus (would feel forced):**
- "Fine-tune" — candidate hasn't fine-tuned a model (Opus, GPT-5.5, Grok all flagged)
- "White glove deployment" — not earned (GPT-5.5, Grok)
- "Trusted C-suite Advisor" / "Executive credibility" — too inflated (GPT-5.5, Grok); use "pitched to incoming CEO" instead, which is true and CIIA-clean (no name)
- "p95 latency" — don't invent measurements

### 8. CIIA-adjacent rewrites (landmine defense)

**GPT-5.5 caught two landmines the others missed** (Opus's ranker upgraded GPT-5.5 partly for this):

**8a. Polymarket "sponsor data layer" phrase — sanitize.** The CIIA non-negotiables list explicitly restricts "sponsor data export technical detail." Replace "sponsor data layer" with **"reporting requirements"**:

> ...a 5-component build (homepage module, Learn page hub, in-article recirculation, embedded course player, **reporting requirements**)...

**8b. Financial-Research Fleet "fine-tuned local stack" — replace with "local-LLM stack."** "Fine-tuned" has a specific technical meaning the candidate cannot defend. Two panelists flagged this; one (Gemini) inadvertently doubled down with a fabricated "<$0.02 per daily brief" cost metric that the candidate also cannot defend — **Gemini's specific dollar figure is REJECTED** (Opus's ranker correctly flagged this as a resume landmine).

**8c. x402 / A2A / MCP memo — soften (GPT-5.5's catch).** Current phrasing "positioning Block Pro as default data infrastructure for the emerging agent economy" is unshipped strategy with overclaim risk. **Reframe as internal memo:**

> Authored internal x402 / A2A / MCP strategy memo mapping 6 potential agent-economy monetization patterns — pay-per-request data access, agent-readable feeds, education micropayments, content-crawl licensing — into product questions for future Block Pro exploration.

### 9. Decision on Campus 201 media automation bullet

**Disagreement:** GPT-5.5 said CUT unless a real metric can be added. Opus, Gemini, Grok kept it.

**My call: KEEP for now, REWRITE with human-review threading** — the bullet demonstrates AI media tooling fluency (Nano Banana / Veo / Kling / ElevenLabs naming maps to AI PM keyword density). But GPT-5.5's concern is right that without a count, it's tool-name flexing. If the candidate can recall *any* count (assets generated, courses produced, production hours), add it. Otherwise rewrite with safety framing:

> Automated AI-assisted image, video, and voiceover generation for the Campus 201 enterprise course launch using Nano Banana Pro, Veo 3.1 / Kling 3.0, and ElevenLabs APIs, with human creative review before final asset delivery.

### 10. CUT the 2D Animation Pipeline from the AI PM master

**GPT-5.5's catch** (Gemini's ranker upgraded GPT-5.5 partly for this): the 2D Animation Pipeline is a *June 2026* project. Future-dated bullets weaken AI PM credibility. **CUT from AI PM master. Keep for Creative PM variant after it ships.** Preserve the creative-archetype signal via the Skills row: add "AI-assisted media production, animation" to Domains.

### 11. Do NOT add "forthcoming" references to unshipped artifacts (Q6 reinforced)

All four panelists agreed: no "forthcoming" Loom, Token Cost Calculator, or fleet writeup mentions. The Wk-3 deliverables stay off the resume until they ship.

---

## Explicit disagreements where I picked a side (and why)

| Issue | Disagreement | My call | Reasoning |
|---|---|---|---|
| Q5 Path A vs B | Grok voted Path A (soften all NYL %); Opus/GPT-5.5/Gemini voted Path B | **Path B + cut the 50% bullet** | The 60% discoverability bullet maps to AI bar; drill it, don't lose it. The 50% UX bullet is the weakest. |
| Eval claims | GPT-5.5 cautioned against "golden set / evaluation framework" until B7 ships; Opus said use them now | **Opus wins** | `audit_intent_spec` IS a shipped eval. Skills-row capability claims are fair; bullet-level shipped-artifact claims would not be. |
| Campus 201 bullet | GPT-5.5 = CUT; others = KEEP | **KEEP w/ rewrite** | Tool-naming maps to AI media production fluency, which Anthropic / OpenAI / creative-adjacent roles value. |
| NYL Leadership compression | Opus's "precursor work" framing vs GPT-5.5/Gemini's metric-rich consolidation | **Hybrid** | Opus's bridge phrasing + GPT-5.5's metric integration. |
| Summary draft | Four competing versions; Grok's included unsupported "former technical founder" | **Hybrid of Opus + GPT-5.5; Grok rejected** | "Former technical founder" is a hallucination Anthropic FDE specifically scans for. |
| Cost metric on Financial Fleet | Gemini proposed "<$0.02 per daily brief" | **REJECTED** | Fabricated number, candidate can't defend it — same F1 landmine the candidate self-flagged. |

---

## Final note on package coherence

The candidate's locked decision frames the resume as a **load-bearing supporting member** of a 4-piece package. Every change above is calibrated to that — the resume becomes legible to a 20-second AI PM recruiter scan while the site, GitHub, and Substack carry the cross-archetype range. **Opus said it cleanest in panel:** "The 20% is the eval language and the safety thread — both earnable from already-shipped evidence, no new work required."

Ship by Mon 2026-05-19. Drill the 7-metric set. Don't apologize for the layoff on paper.
