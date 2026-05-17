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

The resume is a **secondary artifact** inside a 4-piece pristine package: (1) AI PM Portfolio at `seanwinslow.com/transactions`, (2) build-in-public proof (Substack post 1 ships 2026-05-22, LinkedIn syndication Wednesdays), (3) GitHub repo presence (Superuser Pack + `sw-mcp-intent-engineering`), (4) the resume itself.

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
- Claude Code Superuser Pack v3.37.0 — 118 skills, 13 subagents, 14 hooks, 17 SDK agents (8 active by default + 2 opt-in + 1 manual-trigger). Karpathy "agentic engineering practitioner's toolkit" framing in README line 3.

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

AI Product Manager and agentic-engineering practitioner with 11+ years across crypto media, SaaS, and digital asset management. Most recently at The Block, shipped 3 production Claude Skills, a Polymarket B2B revenue integration, and a 10-week Confluence overhaul plan. Builds open-source agentic-engineering tooling — the 118-skill Claude Code Superuser Pack and a 17-agent autonomous SDK fleet.

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

### Claude Code Superuser Pack — Open-Source Toolkit

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

AI Product Manager and agentic-engineering practitioner. Ships production Claude Skills, the `intent-engineering` MCP server, and autonomous agent fleets. Most recently at The Block, delivered 3 Claude Skills, co-authored the Block Pro 2.0 product audit and competitive analysis, and authored the x402 / A2A / MCP integration strategy memo positioning Block Pro for the agent economy. Maintains the open-source 118-skill Claude Code Superuser Pack and a 17-agent autonomous SDK fleet.

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

*(Identical to MASTER above — Superuser Pack, intent-engineering MCP, Agentic Financial-Research Fleet, 2D Animation Pipeline, College of Staten Island, and the 4 Skills rows.)*
```

---

## Reminder before submitting

The candidate's locked decision (Phase 1 Task 1.1, 2026-05-17) frames the resume as **secondary in a 4-piece pristine package**, with **package coherence as the differentiator across all 3 archetypes (AI PM / Tech PM / Creative PM)**. Recommendations that pull the resume sharper toward AI PM at the cost of cross-archetype range are tradeoffs that need explicit defense from the panelist making them. Recommendations that constitute keyword vomit (per the candidate's locked decision) are auto-REJECT in the candidate's downstream triage — don't waste a numbered slot on them.

The 5 unshakeable interview anchors the resume primes for (per the candidate's interview-prep canon): (a) one shipped MCP server (Karpathy thesis); (b) verbal lifeline drilled; (c) numbers ready (precision, $/morning, p95); (d) selling demonstrated work not tenure; (e) work has a canonical home (personal site).

Begin.
