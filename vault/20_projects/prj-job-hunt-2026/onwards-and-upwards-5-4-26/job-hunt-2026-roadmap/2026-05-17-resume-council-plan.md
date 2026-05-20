---
title: "Resume Council Review + Lock Plan"
date: 2026-05-17
type: plan
status: phase-7-in-progress
domain: [job-hunt-2026]
tags: [resume, llm-council, ai-pm, application-prep]
related:
  - "[[2026-05-06-unified-roadmap]]"
  - "[[resume-strengthening-recommendations-2026-05-09]]"
  - "[[the-block-resume-info-ciia-scrub-2026-05-09]]"
  - "[[2026-05-16-council-nate-jones-digest]]"
---

# Resume Council Review + Lock Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to walk this plan task-by-task. Steps use checkbox (`- [ ]`) syntax. Most work is Sean-owned drafting + decision-making; Claude's role is research synthesis, draft pressure-testing, council orchestration, and CIIA/keyword sanity checks — never final resume copy authorship. ("Agents draft / Sean sends" is the Tier-A truth.)

**Goal:** Lock a recruiter-ready master resume + 3 tailored variants (AI PM / Tech PM / Creative PM) by **EOD Mon 2026-05-18**, validated through a single premium LLM Council pass against the 2026 AI PM hiring bar, so Phase 5 Task 5.2 (5 quality apps/week, starting 2026-05-19) can launch unblocked.

**Architecture:** Five sequenced phases. (1) Lock the resume's job-in-the-funnel before redrafting — the unified roadmap deliberately bets URL-first, not PDF-first. (2) Build a structured input packet for the council so we get one high-signal pass instead of three muddled ones. (3) Sean answers the 8 open questions in his own voice (not Claude's). (4) Apply council recs with conflict-resolution rules baked in. (5) Final sanity gates — CIIA, JD-keyword mirror, personal-site link health — before lock and apply.

**Stack:**
- **Resume files** — `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume{,_AI_PM,_Tech_PM,_Creative_PM}.md`
- **Council** — `tools/llm-council/council/` CLI (premium profile: Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20, chairman Opus 4.7), invoked via the `/llm-council` skill. Budget: ~$0.29 typical, $1.00 per-query cap, $7/day circuit breaker.
- **Evidence corpus** — Aakash canon (13 references at `vault/40_knowledge/references/ref-aakash-*.md`), interview-prep folder (4 docs), unified roadmap, resume-strengthening recs, CIIA scrub list.
- **Sanity check** — JD-keyword mirror against `vault/20_projects/research/2026-05-07-target-role-specs.md` verbatim quotes.

**Time-box:** Sat 2026-05-17 (today, ~3 hrs) + Sun 2026-05-18 (~5 hrs). Final lock by Mon 2026-05-19 09:00 — same day the personal site goes live (Task 1 Step 3 of the unified roadmap) and the application cadence begins.

---

## Inputs Already Gathered

Three subagents synthesized the relevant corpora (this file is the consolidation). Key findings carried into the plan below:

### Current resume state (4 files at `assets/`)
- All 4 share identical section spine: Summary → Work Experience → Leadership Experience → Selected Projects → Education → Skills (~95 lines each, ~1 page rendered).
- Tailoring is **reorder + Summary swap only** — no content swaps across variants.
- Strengths: concrete numbers everywhere on Block bullets (3 Skills / 11 Zaps / 7 manual steps / 9 platforms / 11 risks / 50+ sites / 8 categories), OKR linkage on Skills + Confluence bullets, the x402/A2A/MCP strategy memo is a rare PM differentiator, Selected Projects establishes Sean as builder-not-planner, variants don't invent content.
- Known weaknesses (5 from the recs, plus 5 latent): NYL bullets stale; Leadership Experience duplicates Work Experience (NYL "Managed a team of 8 / Led stakeholder communication" reads generic-management); zero outcome metrics on Block work (every bullet is a capability claim); Education one-line and bare; no certifications, talks, or community signal; no per-bullet portfolio anchors despite the `seanwinslow.com` header URL.

### What the 2026 AI PM bar demands (Aakash canon)
- **Named shipped AI products with architectures** (not "led AI initiative" but "rebuilt recommendation engine using two-tower neural network").
- **STAR+M** — business metric AND model metric on the same bullet.
- **≥2 ML paradigms** (classical ML + DL + LLM/agents — monoculture reads hobbyist).
- **GitHub URL in header** — recruiters click; recent commits beat star counts.
- **An MCP server, agent fleet, or eval suite as a flagship portfolio bullet.**
- **Safety thread on every AI bullet** (not a separate section — threaded).
- **Eval-design bullet** with golden-set size + precision/recall/F1 to defend the F1-score landmine ("I'd have to check" is the death answer).
- **Cost economics in at least one bullet** ($/run, $/morning, $/call rejected).
- **Vibe-coding evidence** — Loom URL or deployed Bolt/v0 URL, plus named tools (Cursor, Bolt, v0, Lovable, Replit).
- **Specific verbs** — shipped, owned, evaluated, fine-tuned, killed, paused, retrained. NOT led/drove/collaborated.

### Roadmap positioning + evidence (2026-05-17)
- Positioning: **"agentic engineering practitioner who ships"** + **"semantic product architecture"** (the council's chairman line). Karpathy framing: artifacts > credentials.
- Archetype: **AI PM > Tech PM > Creative PM**, with Anthropic-specific override.
- Evidence map (status as of 2026-05-17): **SHIPPED 2026-05-12** — `intent-engineering` MCP server v0 (live on npm + MCP registry, DNS-verified), Phase D Typed Reasoning Edges 4Q `EXPLANATION.md`, Phase 6 Knowledge Loop 4Q `EXPLANATION.md`, Vault Synthesizer Eval Suite (B7-gated), Substack-Drafter (B7-gated). **PLANNED** — sanitized financial-research fleet (~2026-06-05), 14-agent fleet Loom + Token Cost Calculator, animation pipeline (2026-06-11), Judge Layer (2026-06-04), Authority/Recovery/Audit reframe (2026-06-10), Vault Scorecard (2026-06-03), Manifesto (~2026-06-19).
- **STOP-DOING** (Task 7, council-amended): no "Agent OS / runtime architecture" framing — Sean self-codes as beginner-to-intermediate and would lose senior-engineer technical screens; no "OpenClaw" framing for the same reason.
- **Hard prerequisite for ship:** `seanwinslow.com` is NOT LIVE until Mon 2026-05-19 — any resume with that URL ships only after deploy.

### CIIA guardrails (must NOT appear on resume)
- Named institutional Block Pro clients: Goldman, JPMorgan, Fidelity, Yale, Bain.
- Pro ARR / churn: $856K ARR, $323K ARR at risk, $442K churn, 21% rate, $693K renewal, $173K downsell, $16,459 avg ARR/client, 52/16 client counts.
- Unshipped product names: Simon AI Living Dashboard, Pro Search, Institutional Data Moat, Around The Block / Globe / Ambassador Program.
- Unshipped revenue projections: $2.3M ARR, $60K incremental, $336K, $1.2M.
- Named internal executives mid-strategy: Steve Chung, Mike, Cameron Tynes, Steven Zheng, Simon Cousaert, Matt Vitebsky, Ed, Larry Cermak, Vicky Lu, Alex Lebedyev (use roles, not names — Larry as a reference is okay outside the resume body).
- The "Project CTO" codename — use ".co homepage redesign" instead.
- Polymarket pre-launch specifics (lead export integration specs, "100+ leads Month 1" pilot target, X auth lead-capture flow, sponsor data export tech detail).

### Sean's own walk-away math
- **$100K floor** (Tier-A truth), **target band** $150–250K, **relocation override** = Anthropic specifically OR $250K+/yr otherwise (Boston metro / remote default).

---

## Phase 1: Lock the Resume's Job (Sat 2026-05-17, 30 min)

> The unified roadmap explicitly reframes the resume as supporting cast, not lead artifact. Before redrafting, Sean decides whether the resume's job is to (a) be the lead artifact, (b) be a clickable index back to `/transactions/`, or (c) be a CIIA-clean printable for ATS systems that won't render URLs well. The answer changes the redraft.

### Task 1.1: Decide the resume's role in the funnel

**Files:**
- Read (no edits): [`2026-05-06-unified-roadmap.md`](2026-05-06-unified-roadmap.md) — search for "replaces the resume as lead artifact" and the "URL-first, not resume-first" language around L298.
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-17-resume-funnel-role-decision.md` (one-page decision doc).

- [ ] **Step 1: Read the roadmap's L286–L298 reframe.** What does "URL-first" actually mean for what the resume must do?

- [ ] **Step 2: Sean answers three questions in writing** (in the decision doc):
  - Q1: For ATS-mediated applications (LinkedIn Easy Apply, company portals that parse PDFs), is the resume the primary artifact? *(Default: yes — most Tier-1 companies still require it.)*
  - Q2: For warm-intro / direct-recruiter conversations, is the URL primary and the resume an attachment? *(Default: yes per roadmap.)*
  - Q3: Should the master resume optimize for ATS keyword scoring OR human-reader signal density? *(Tradeoff: keyword-stuffed resume reads worse to humans; signal-dense resume may miss ATS filters. Pick a primary.)*

- [ ] **Step 3: Write the one-sentence role.** Template: "The 2026-05-19 resume is a [primary/secondary] artifact whose job is to [single function] without compromising [single constraint]."

- [ ] **Step 4: Commit the decision doc** with a one-line summary into `vault/20_projects/prj-job-hunt-2026/README.md` under Artifacts.

---

## Phase 2: Build the Council Input Packet (Sat 2026-05-17, 1.5 hrs)

> The council gets one shot. Quality of the prompt determines quality of the critique. The packet must contain: (a) the resume as it stands today, (b) explicit positioning, (c) target-role JD keywords verbatim, (d) the 8 open questions, (e) CIIA non-negotiables, (f) Sean's walk-away math, (g) the evidence-map status with shipped/planned distinction. Without (g), the council will hallucinate that everything is shipped and produce recommendations that overstate.

### Task 2.1: Pick the resume version that goes to council

**Files:**
- Read: all 4 resume files at `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume*.md`.
- Modify or create: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_council_input.md`.

- [ ] **Step 1: Read all 4 resumes back-to-back** to confirm subagent A's finding that variants are reorder + Summary swap only. (5 min.)

- [ ] **Step 2: Pick the input.** Recommendation: **send the master + the AI PM variant**, NOT all four. Reasoning: AI PM is the top archetype, the council will choke on 4-variant comparison and produce mush; comparing master vs. AI PM lets the council critique the tailoring strategy itself.

- [ ] **Step 3: Create the council input doc** by concatenating the master + AI PM variant under labeled headers (`# MASTER` / `# AI_PM_VARIANT`). Do NOT edit the underlying files — this is a read-only consolidation.

- [ ] **Step 4: Sanity-check** that the resume references the 2026-05-12 shipped artifacts (intent-engineering MCP, Phase D `EXPLANATION.md`, Phase 6 `EXPLANATION.md`). If the current master pre-dates those ships, the council will critique a stale doc. **If stale:** flag this and proceed to Task 2.2 before continuing.

### Task 2.2: Pre-council resume freshness patch (only if Task 2.1 Step 4 flagged stale)

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md`
- Modify: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_AI_PM.md`

- [ ] **Step 1: Add a "Selected Projects" entry for `intent-engineering` MCP v0** (or strengthen the existing one).

  Template (Sean to refine the language):
  ```markdown
  - **intent-engineering MCP server** ([npm](https://www.npmjs.com/package/@swins/intent-engineering-mcp) · [registry](https://registry.modelcontextprotocol.io) · [repo](https://github.com/seanwinslow28/sw-mcp-intent-engineering)) — 3-tool TypeScript MCP server (`audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`) shipped 2026-05-12, 13 days ahead of plan. Published to npm + MCP registry (DNS-verified namespace `com.seanwinslow`). Demoable in Claude Desktop with one config change.
  ```

- [ ] **Step 2: Add a portfolio anchor** to the agent-fleet bullet pointing at `agents-sdk/agents/knowledge_loop/EXPLANATION.md` and `agents-sdk/lib/concept_edges/EXPLANATION.md` (the two 4Q docs shipped 2026-05-12).

- [ ] **Step 3: Hold the eval suite, Substack-Drafter, observability dashboard, financial-research fleet, animation pipeline, Judge Layer, Manifesto, Authority/Recovery/Audit, Vault Scorecard** — these are B7-gated, planned, or in flight. Do NOT add as resume bullets until they're shipped + linkable. If they ship before the apply cadence starts, fold them in via a Task 8 update pass.

- [ ] **Step 4: Re-export the council input doc** with the patched master + AI PM variant.

### Task 2.3: Assemble the council prompt

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-17-resume-council-prompt.md`.

- [ ] **Step 1: Write the council prompt** with these exact sections (template below — fill in literals before invoking):

  ```markdown
  # Resume Council Critique — Sean Winslow, May 2026

  ## Context
  Sean Winslow is a Product Manager pivoting to AI PM roles after a May 4, 2026 layoff
  from The Block (cost-cutting, not performance). 6 months titled PM at The Block;
  prior career: 10+ years at New York Life in design/animation/DAM leading into
  AI-workflow integration. Target archetypes in order: AI PM > Tech PM > Creative PM.
  Walk-away $100K; target $150–250K; relocation override = Anthropic or $250K+.
  Applications begin Mon 2026-05-19. Today is Sat 2026-05-17.

  ## Positioning thesis (from the unified roadmap)
  "Agentic engineering practitioner who ships." Semantic product architecture —
  specs, governance, routing, memory, authority, review.
  Karpathy framing: artifacts > credentials.
  Nate Jones reframe: comprehension as currency; 4Q EXPLANATION.md is to the
  generative era what the commit message was to the traditional engineering era.

  ## Evidence map status (BE PRECISE — don't critique artifacts that aren't shipped)
  SHIPPED 2026-05-12: intent-engineering MCP server v0 (npm + MCP registry,
    DNS-verified); Phase D Typed Reasoning Edges 4Q EXPLANATION.md; Phase 6
    Knowledge Loop 4Q EXPLANATION.md.
  SHIPPED + PUBLIC: Code-Brain (118 skills, 13 subagents, 14 hooks,
    17 SDK agents; Karpathy framing in README).
  CODE-COMPLETE, B7-GATED: Vault Synthesizer Eval Suite (10 binary cases, 7/10
    post-fix); Substack-Drafter; Agent Fleet Observability Dashboard v1.
  PLANNED, NOT YET SHIPPED: financial-research fleet sanitization (~Jun 5);
    14-agent fleet Loom + Token Cost Calculator (~Wk 3); animation pipeline
    (Jun 11); Judge Layer (Jun 4); Authority/Recovery/Audit reframe (Jun 10);
    Vault Scorecard (Jun 3); Manifesto (~Jun 19); seanwinslow.com (Mon May 19).

  ## CIIA non-negotiables (must NOT appear)
  Goldman / JPMorgan / Fidelity / Yale / Bain (client names); $856K / $323K /
    $442K / 21% / $693K / $173K / $16,459 / 52 / 16 (Pro ARR + client counts);
  Simon AI / Living Dashboard / Pro Search / Institutional Data Moat / Around
    The Block / Globe / Ambassador Program (unshipped product names);
  $2.3M / $60K / $336K / $1.2M (unshipped projections); Steve Chung / Mike /
    Cameron / Steven Zheng / Simon Cousaert / Matt Vitebsky / Ed / Larry / Vicky /
    Alex (executive names mid-strategy); "Project CTO" codename;
  Polymarket pre-launch specs ("100+ leads Month 1", X auth flow, sponsor export
    tech detail).

  ## STOP-DOING (do not recommend bullets in this direction)
  No "Agent OS" or "runtime architecture" framing — Sean self-codes as
    beginner-to-intermediate, would lose senior-engineer technical screens.
  No claims of concurrency / distributed systems / low-level perf ownership.

  ## Target JD keywords (verbatim — mirror these where defensible)
  Anthropic FDE: "technical artifacts for customers like MCP servers, sub-agents,
    and agent skills" / "Former technical founders are also encouraged to apply"
  Glean FDP: "0-to-1 product creation" / "shipped AI-powered solutions in the
    real world, not just designed them" / "white glove deployment" / "Trusted
    C-suite Advisor"
  Pair Team: "Familiarity with AI tools and a track record of experimenting with
    modern build workflows" / "Use AI tools and Pair's internal platform to ship
    prototypes and accelerate execution"
  Scale AI: "hands-on experience building end-to-end systems or prototypes in
    production" / Python / SQL
  Microsoft AI PM: "Firsthand experience evaluating and deploying LLMs into
    production" / "Work side-by-side with researchers and engineers"
  Liberate: "identify high-impact problems, design AI agent workflows, and
    drive them into production"
  Cross-cutting: ship/shipped/shipping (never led/drove/collaborated); production
    (never prototype-only); agentic/agent/agents; evals/evaluation framework/
    golden set; MCP (frontier labs); fine-tune / RAG / tool use / orchestration;
    cost / latency / throughput / p95.

  ## The 8 open questions (each panelist should answer all 8)
  [paste the 8 questions verbatim — see Task 2.4]

  ## What I'm asking for
  Each panelist: a numbered list of the highest-leverage changes to make to this
  resume before applications begin Mon 2026-05-19 — ordered by expected impact
  on getting a Tier-1 AI PM phone screen. Be specific: bullet text, ordering,
  cuts, additions. Cite the 2026 AI PM hiring bar (Aakash canon, Hamel Husain
  evals canon, Karpathy/Nate Jones framing) where it applies. Be brutal. Sean
  wants the truth, not flattery.

  Chairman: synthesize the 4 panelists' critiques into ONE prioritized punch
  list. When panelists disagree, name the disagreement and pick a side with a
  reason. Bias toward shipping by Mon 2026-05-19 vs. perfection.

  ## The resume (master + AI PM variant)
  [paste full contents of vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_council_input.md]
  ```

- [ ] **Step 2: Sean reads the prompt end-to-end** before sending. Two filters:
  - Did the prompt accidentally leak any CIIA-protected detail? (Cross-check against the CIIA non-negotiables section.)
  - Does the prompt over-claim shipped artifacts? (Cross-check against the evidence-map status section — only the items marked SHIPPED can be defended.)

- [ ] **Step 3: Save the prompt** to the path above. Commit if desired (no rush).

### Task 2.4: Finalize the 8 open questions for the council

**Files:**
- Append to: the council prompt at `2026-05-17-resume-council-prompt.md`.

- [ ] **Step 1: Use this question set** (synthesized from subagent A's resume-corpus pass + subagent B's Aakash-bar gap list). Sean can edit any of them, but every one is load-bearing:

  1. **Resume as master vs. AI PM as master.** Should the AI PM variant become the new master (recruiter-rate optimization), with the current master demoted to a fallback? Or does maintaining a role-agnostic master still earn its keep?
  2. **Tenure asymmetry framing.** 6 months titled PM at The Block + 10+ years prior in design/animation/DAM (with AI-workflow leadership in the last 3). Should the Summary acknowledge "post-layoff cost-cutting, not performance" preemptively, or leave the layoff context entirely for cover letters?
  3. **NYL Leadership Experience cut/modernize.** "Team Lead, AI Workflow Integration (2021 – Nov 2025)" carries 3 generic-management bullets (managed a team of 8 / led stakeholder comms / mentored junior staff). Drop entirely? Compress to one line with an AI-era metric? Replace with the prompt-engineered-metadata-for-DAM bullet that already lives in NYL Work Experience?
  4. **Pre-mortem methodology as standalone bullet.** The Tigers/Paper Tigers/Elephants 11-risk pre-mortem methodology is currently folded into the Pro 2.0 bullet (A3). Pre-mortems are a senior-PM signal most resumes don't carry — does burying it lose differentiation that a standalone Leadership Experience bullet would surface?
  5. **F1-score landmine defense.** Per Aakash, every AI-ownership bullet must carry a defensible metric (precision/recall/F1/p95/$ per call) or be cuttable. Audit each AI bullet on the resume: which ones currently survive "tell me the metric" — and which need a number added or the claim trimmed?
  6. **Vibe-coding evidence on the resume itself.** Does the resume need a clickable Loom URL or deployed Bolt/v0 URL inline (e.g., next to a Selected Project) before Mon 2026-05-19, or is "Cursor / Bolt / Lovable" in the Skills row sufficient for Round 1? The 14-agent fleet Loom + Token Cost Calculator are PLANNED for Week 3 — should the resume reference them now ("forthcoming") or wait?
  7. **Safety/responsible-AI thread depth.** Does the safety signal appear in at least one bullet per major AI artifact, or is it absent? For Anthropic / OpenAI / Google specifically, what's the minimum threading to clear their bar?
  8. **JD-keyword mirror without keyword-stuffing.** Run the verbatim JD keywords from the prompt above against the resume. Which target-role keywords are missing entirely? Where can they be added without stuffing? Where would adding them feel forced — and is that signal that the resume is being asked to do too much for one archetype (argument for the AI-PM-as-master pivot in Q1)?

- [ ] **Step 2: Decide whether to add a 9th question** about portfolio-piece anchors (D1–D4 from the resume-strengthening recs — Polymarket PRD evolution, AdOps walkthrough, Project CTO visual audit, P&E Dept 2.0). Argument for adding: the council can advise on per-bullet `[↗ writeup]` anchors. Argument against: 8 questions is already pushing the council's attention budget; portfolio anchors require sanitized docs that aren't published yet. **Default: hold for Phase 8 application-cadence iteration; do not add Q9 to this council pass.**

---

## Phase 3: Sean Answers the 8 Open Questions in His Own Voice (Sat 2026-05-17 evening, 1 hr)

> The council's verdict is sharper when Sean has already answered the same questions himself. Pre-answering forces him to commit to opinions before the council validates or contradicts them — protects against passively accepting whatever the chairman says. Per the "agents draft / Sean sends" rule, this is non-delegable.

### Task 3.1: Pre-answer all 8 questions

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-17-resume-pre-council-answers.md`.

- [ ] **Step 1: For each of the 8 questions, write 3–5 sentences of Sean's current best answer.** Not Claude's. Out loud if it helps — type what you'd say to a friend at a bar. Don't research; this is gut + experience.

- [ ] **Step 2: Tag each answer with a confidence level.** 1–5 scale:
  - 1: pure guess
  - 2: leaning, easily overturned by a good argument
  - 3: my current default, would want to hear a reason to change
  - 4: strong opinion, I'd defend it
  - 5: locked, council can't move me

- [ ] **Step 3: Note any question that bothers you to answer.** Bothering = signal there's an underlying decision you've been avoiding. The council can help most where confidence is lowest AND the question can't be ducked. Flag those two or three for chairman attention in the prompt.

---

## Phase 4: Run the Premium LLM Council (Sun 2026-05-18 AM, 30 min wall + ~3:30 wait)

> Per the 2026-05-16 Nate Jones digest precedent, premium-profile runs cost ~$0.62 and complete in ~3:30 wall. Budget headroom is fine. Invocation is via the `/llm-council` skill — Sean drives this; Claude is the orchestrator. Per the Tier-A truth, the resume PDF/markdown that goes out the door is Sean's words.

### Task 4.1: Invoke /llm-council with the assembled prompt

**Files:**
- Read: the prompt at `2026-05-17-resume-council-prompt.md`.
- Output lands at: `vault/health/council-spend-{YYYY-MM}.json` (cost log) + `tools/llm-council/runs/2026-05-18-resume-critique/` (transcripts).

- [ ] **Step 1: Sanity-check the cost budget.** Run the `/llm-council` skill's pre-flight check — `tools/llm-council/council/cli.py --dry-run --profile premium --prompt 2026-05-17-resume-council-prompt.md` (or equivalent per the skill SKILL.md). Confirm the estimate is in the $0.20–$0.40 band and well under the $1.00 per-query cap.

- [ ] **Step 2: Invoke `/llm-council`** with:
  - Profile: `premium`
  - Chairman: Opus 4.7 (default)
  - Prompt file: the prompt assembled in Task 2.3
  - Tag: `resume-critique-2026-05-18`

- [ ] **Step 3: Wait for completion.** ~3–5 min wall per panelist, ~15–20 min total + chairman synthesis. Use the time to start drafting Task 5.1 below from your pre-council answers.

- [ ] **Step 4: Save the transcript directory path** into the README of `prj-job-hunt-2026/` under Artifacts. Confirm `vault/health/council-spend-2026-05.json` updated.

### Task 4.2: Acceptance criteria for a "usable" council output

- [ ] **Step 1: Verify the chairman synthesis exists and is structured as a numbered punch list** — not prose. If it's prose, ask the chairman to re-emit as a numbered list before doing anything else (a single follow-up call, ~$0.05).

- [ ] **Step 2: Confirm each panelist answered all 8 questions.** If a panelist skipped questions, that panelist's input is partial — note which questions are under-covered.

- [ ] **Step 3: Confirm no panelist hallucinated artifacts** (e.g., critiquing an MCP server that doesn't exist yet, or claiming Sean has a Substack post live). Cross-check against the prompt's evidence-map section. Flag any hallucinated critique — those recommendations are dismissable.

- [ ] **Step 4: Tag the highest-disagreement question.** Where the 4 panelists most diverge is the most informative place to spend the next 30 minutes.

---

## Phase 5: Synthesize Council Output → Resume V2 Patches (Sun 2026-05-18 PM, 2–3 hrs)

> Council output is raw material, not gospel. Sean applies conflict-resolution rules + the Tier-A truths (walk-away math, CIIA, no senior-engineer framing) on top of whatever the chairman says.

### Task 5.1: Triage council recommendations into 4 buckets

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-18-resume-council-triage.md`.

- [ ] **Step 1: Read the chairman synthesis end-to-end without editing the resume.** First pass = comprehension only.

- [ ] **Step 2: Re-read each panelist's full critique.** Note where they agreed unanimously (highest confidence to apply), where 3-of-4 agreed (high confidence), where they split 2/2 (Sean's judgment call), and where any panelist contradicted Sean's pre-council answer with confidence ≥4 (rare — this is the council earning its keep).

- [ ] **Step 3: Bucket every actionable recommendation into one of four:**
  - **APPLY** — unanimous or 3-of-4, not CIIA-conflicting, not STOP-DOING-conflicting, matches Sean's archetype targeting. Apply verbatim or with minor wording adjustment.
  - **JUDGE** — split panel, OR conflicts with Sean's confidence-4/5 pre-answer, OR has a tradeoff Sean wants to own. Decision logged with one-sentence rationale.
  - **REJECT** — recommends a CIIA-protected detail, a STOP-DOING framing (Agent OS / runtime / senior-engineer-coded), a metric Sean can't honestly defend, or content that exists only as planned-not-shipped artifacts. Logged with reason.
  - **DEFER** — good but requires a not-yet-shipped artifact (Loom / Token Cost Calculator / animation pipeline / Manifesto / Vault Scorecard / Judge Layer). Logged with the artifact ship date as the un-defer trigger.

- [ ] **Step 4: Total counts per bucket.** Sanity check: if APPLY is >30 items, the council was too generous and Sean is over-rewriting; if APPLY is <5, the council was too soft and Sean should send a sharper follow-up before applying anything. Healthy target: 8–15 APPLY items.

### Task 5.2: Apply the APPLY-bucket changes to the master + AI PM variant

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md`
- Modify: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_AI_PM.md`

- [ ] **Step 1: Apply changes one at a time** to the master. After each change, re-read the surrounding paragraph aloud. If it sounds robotic, rewrite in Sean's voice — the council's draft language is suggestion, not copy.

- [ ] **Step 2: Mirror master changes into the AI PM variant** where applicable. If a change is master-only (e.g., a Tech PM-relevant bullet emphasis), note it and skip.

- [ ] **Step 3: Re-export to PDF** using the existing pipeline (or open both files in a Markdown-to-PDF renderer for a side-by-side visual review).

- [ ] **Step 4: Diff against the pre-council master.** Read the diff. Is the resume materially better, or is it just longer? If longer-without-better, cut. Two pages MAX; one page if a tighter selection survives.

### Task 5.3: Resolve the JUDGE-bucket items

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md`
- Modify: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_AI_PM.md`

- [ ] **Step 1: For each JUDGE item, apply this decision tree:**
  - Does the change pull Sean further toward AI PM signal? → lean APPLY.
  - Does the change require claiming senior-engineer ground? → REJECT.
  - Does the change require a metric Sean can defend out loud in an interview within the next 7 days without notes? → APPLY. Else → reject the metric, keep the qualitative version, OR cut the bullet.
  - Does the change reduce role-agnostic flexibility in exchange for AI PM sharpness? → APPLY (per Decision Q1 default toward AI-PM-as-master). Reverse only if Sean's Q1 pre-answer was confidence-4 or 5 toward keeping master agnostic.

- [ ] **Step 2: Log each judge call in the triage doc** with one sentence: "Applied / rejected because X."

### Task 5.4: Update the Tech PM and Creative PM variants to match the new master

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_Tech_PM.md`
- Modify: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_Creative_PM.md`

- [ ] **Step 1: Apply non-AI-specific master changes** to both variants. Skip any change that's AI PM-specific.

- [ ] **Step 2: For Tech PM:** ensure the AdOps automation pipeline + Confluence Dept 2.0 + intent-engineering MCP still lead. Add Python/SQL/TypeScript explicitly to Skills if the council flagged keyword gaps from the Scale AI / Microsoft JDs.

- [ ] **Step 3: For Creative PM:** ensure the 2D animation pipeline still leads in Selected Projects. If the animation pipeline is still pre-ship on 2026-05-19, mark it "shipping 2026-06-11" or hold off applying to Creative PM roles until then.

---

## Phase 6: Sanity Gates Before Lock (Sun 2026-05-18 PM, 1 hr)

> Three gates must pass before any resume goes to a recruiter. Failing any one of them is grounds for not sending and iterating once more.

### Task 6.1: CIIA scrub gate

**Files:**
- Read: [`the-block-resume-info-ciia-scrub-2026-05-09.md`](../the-block-resume-info-ciia-scrub-2026-05-09.md).
- Read (post-edit): all 4 resume files.

- [ ] **Step 1: For each resume file, grep for the banned terms.** Use a checklist run by Claude with `Grep` over each file: client names (Goldman / JPMorgan / Fidelity / Yale / Bain), ARR/churn figures, unshipped product names, internal executive names, "Project CTO" codename, Polymarket pre-launch specifics.

- [ ] **Step 2: For each hit, decide:** is this Sean's own IP carve-out (CIIA §2.4 — Code-Brain, agent fleet, animation pipeline, AdOps as architecture) or Block-protected? If Block-protected, edit out.

- [ ] **Step 3: Confirm zero hits remain** before proceeding. Document the grep output in the triage doc as the gate-1 receipt.

### Task 6.2: JD-keyword mirror gate

**Files:**
- Read: [`vault/20_projects/research/2026-05-07-target-role-specs.md`](../../research/2026-05-07-target-role-specs.md).
- Read (post-edit): the AI PM variant specifically.

- [ ] **Step 1: For each Tier-1 JD, score the AI PM variant on keyword coverage** out of the verbatim phrase list pulled by subagent B (Anthropic FDE / Glean FDP / Pair Team / Scale AI / Microsoft / Liberate). 1 point per verbatim phrase present, 0.5 for close paraphrase, 0 for absent.

- [ ] **Step 2: Acceptance threshold:** ≥60% of cross-cutting verbs present (ship/production/agentic/evals/MCP/RAG/cost/latency); ≥40% of target-specific phrases per Tier-1 JD. Sub-threshold = add the missing verbatim phrases where defensible without overclaiming.

- [ ] **Step 3: One landmine check** — confirm the resume never says "led" or "drove" or "collaborated on" on an AI bullet. Replace with "shipped / owned / evaluated / deployed / killed / retrained" per Aakash canon.

### Task 6.3: Link-health gate

**Files:**
- Read (post-edit): all 4 resume files.

- [ ] **Step 1: List every URL the resume contains.** Header (`seanwinslow.com`, LinkedIn, GitHub), bullets, Selected Projects, anywhere inline.

- [ ] **Step 2: For each URL, attempt to load it.** Use `curl -I` for HTTP heads; if a Live URL returns non-2xx, that's a hard fail.

- [ ] **Step 3: Specifically check `seanwinslow.com`.** Per the unified roadmap, target deploy is Mon 2026-05-19. **If Sean is sending the resume before the site is live, the URL must NOT be on the resume yet** — substitute with GitHub URL alone, or hold the resume until the site is live (Sean's call, this is gate-3 of three).

- [ ] **Step 4: Confirm `intent-engineering` MCP server links resolve:** `npmjs.com/package/@swins/intent-engineering-mcp`, `registry.modelcontextprotocol.io` (search for `com.seanwinslow/intent-engineering`), and the GitHub repo URL.

---

## Phase 7: Final Read-Aloud + PDF Lock (Mon 2026-05-19 AM, 30 min)

### Task 7.1: Read every bullet out loud

**Files:**
- Read: the locked master + AI PM variant.

- [ ] **Step 1: Read every single bullet out loud.** If it sounds like a robot wrote it, rewrite. Per the original Phase 2 Task 2.2 Step 7 rule: anything that sounds robotic, rewrite; anything you can't defend in an interview, cut.

- [ ] **Step 2: For each bullet, ask: "What's the 30-second story behind this?"** If you can't tell the story, cut the bullet — STAR rehearsal is Phase 6 of the master plan and the resume bullets should map directly to story-bank entries.

- [ ] **Step 3: Have the AI PM variant ready as the lead artifact** for AI PM applications. Master stays as fallback for ambiguous-archetype openings.

### Task 7.2: PDF generation + filename hygiene

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_AI_PM_Resume_2026-05-19.pdf`
- Create: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_2026-05-19.pdf`
- Optional: Tech PM + Creative PM variants if ready.

- [ ] **Step 1: Convert each markdown resume to PDF** via your existing pipeline (Resumake, LaTeX, Marp, or open-in-Markdown-editor-print-to-PDF). Two pages max.

- [ ] **Step 2: Name files for ATS hygiene.** Pattern: `FirstLast_Role_YYYY-MM-DD.pdf`. Avoid spaces (use underscores), avoid version numbers (use dates), avoid "Final" in the filename.

- [ ] **Step 3: Open each PDF in Preview, scan for layout breakage.** Stray newlines, weird spacing around backticks, link colors not blue, font weight regressions.

- [ ] **Step 4: Send the AI PM variant to one trusted human reader** (a PM peer, Maryalice, or one of the references being prepped under Master Plan Task 3.1) and ask: "Honest read — does this make you want to talk to me?" Don't ask for line-by-line edits; ask for a yes/no/maybe gut. (15 min wait.)

### Task 7.3: Lock and update the project README

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/README.md` (Artifacts section).
- Modify: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md` — Task 2.2 status update.

- [ ] **Step 1: Add a line to README.md Artifacts:** "Resume locked 2026-05-19, council-validated. Master + AI PM variant primary; Tech PM + Creative PM variants secondary."

- [ ] **Step 2: Update the master plan's Task 2.2 status block** with the lock date + path to the council triage doc.

- [ ] **Step 3: Confirm the apply-cadence gate is now cleared** — Phase 5 Task 5.1 (target-30-companies list) closed 2026-05-13; Phase 5 Task 5.2 (5 quality apps/week) can begin Tue 2026-05-20 (Task 5.2 Step 2 schedules application slots for Tue + Thu mornings).

---

## Phase 8: Iterate After First Application Wave (Week of 2026-05-19, ongoing)

> The resume is never done. Phase 5 Task 5.3 of the master plan calls for a Week-4 funnel evaluation: <3 phone screens after 20 quality apps = resume needs rewriting. Build the iteration cadence in now so it's not improvised under pressure.

### Task 8.1: Funnel-signal triggers for resume V3

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/applications.md` (per master plan Task 5.2).

- [ ] **Step 1: Track every application's outcome** in the master applications table. Status: sent / replied / phone-screen / advanced / rejected / ghosted.

- [ ] **Step 2: After 10 apps, micro-retro.** Did ≥3 advance to phone screen? If yes, resume signal is working — continue. If no, hold the next 5 apps and iterate.

- [ ] **Step 3: After 20 apps (Week 4 retro per master plan Task 5.3 Step 3),** apply the master plan's diagnostic:
  - <3 phone screens → resume + positioning need rewrite (re-run a lighter council pass, variance profile $0.14 ok)
  - Lots of phone screens, no advancement → story bank needs work (not resume — Phase 6 of master plan)
  - Lots of late-stage rejections → target archetype misaligned (re-rank AI PM / Tech PM / Creative PM)

### Task 8.2: Un-defer artifacts as they ship

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume{,_AI_PM}.md` on each ship.

- [ ] **Step 1: When each DEFER-bucket artifact ships, add a single-line resume bullet referencing it.**
  - 14-agent fleet Loom + Token Cost Calculator (~Wk 3, before Wed 2026-05-29): one Selected Projects line with both links.
  - `seanwinslow.com/transactions/` (Mon 2026-05-19): swap header URL from GitHub-only to canonical site.
  - Vault Synthesizer Eval Suite (when B7 gate clears, ~5 nights from B7 start): one bullet under the agent-fleet entry — "ran a 10-case golden-set eval suite, scored 7/10 post-fix from 1/10 baseline."
  - Substack post 1 ("The Night My Vault Said Nothing", Sedaris voice, 2026-05-22): one bullet under Selected Projects pointing at the Substack URL once live.
  - Vault Scorecard (2026-06-03), Judge Layer (2026-06-04), Animation Pipeline (2026-06-11), Authority/Recovery/Audit (2026-06-10), Financial-Research Fleet (~2026-06-05), Manifesto (~2026-06-19): each gets a single bullet, added on ship-date.

- [ ] **Step 2: Cap resume length at two pages.** Adding without subtracting kills signal density — when adding a new artifact bullet, also pick one of the existing bullets to cut, compress, or demote.

---

## Self-Review

**Spec coverage:** All four user-stated goals are addressed.
- "Plan of action first using /writing-plans" → this document, written in the writing-plans format with bite-sized steps + file paths + decision rationale.
- "Full picture on what I'm trying to achieve" → Goal + Architecture + Inputs Already Gathered sections lay out the positioning thesis, archetype ranking, evidence map status, CIIA guardrails, and walk-away math from the corpus.
- "What's on the unified roadmap and what else I should be including" → Phase 1 + Phase 2.2 surface the shipped 2026-05-12 artifacts (intent-engineering MCP, Phase D, Phase 6) that the existing resume drafts may not yet reference; Phase 8.2 schedules un-defer points for the planned artifacts (Loom, Token Cost Calculator, Eval Suite, animation pipeline, Substack post 1, Vault Scorecard, Judge Layer, Authority/Recovery/Audit reframe, Manifesto, sanitized financial-research fleet).
- "What else to include to make the resume rock solid" → Phase 2.4's 8 council questions cover the Aakash 2026 AI PM bar dimensions (F1-metric defense, vibe-coding evidence, safety threading, JD-keyword mirror, pre-mortem standalone, NYL modernization, tenure framing, AI-PM-as-master question).
- "After absorbing all that we'll know what to ask the premium council" → Phase 2 builds the structured prompt; Phase 4 runs `/llm-council` with budget + acceptance criteria.
- "Lock in my resume to start applying" → Phase 5 → 6 → 7 chain locks the resume in time for the Mon 2026-05-19 apply cadence.

**Placeholder scan:** Two intentional placeholders remain. (a) The exact council prompt requires Sean's pre-council answers to Q1–Q8 (Task 3.1) before final assembly. (b) The PDF generation pipeline (Task 7.2 Step 1) defers to Sean's existing workflow (Resumake / LaTeX / Marp) — not prescribed because Sean already has a working setup per resume-revision-kickoff-prompt-2026-05-10.md. Every other step has concrete content.

**Type consistency:** "Master" and "AI PM variant" refer consistently to `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md` and `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_AI_PM.md`. "Council" always refers to the `/llm-council` skill + `tools/llm-council/council/` CLI in premium profile (Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20, chairman Opus 4.7). Date anchors: today = Sat 2026-05-17, lock target = Mon 2026-05-19 09:00, apply cadence start = Tue 2026-05-20.

**Worth flagging where I made judgment calls:**
- **Send master + AI PM variant only to the council (Task 2.1.2), not all 4.** Reasoning: 4-variant comparison will produce muddled critique; comparing master vs. AI PM lets the council critique the tailoring strategy itself.
- **Pre-answer the 8 questions before invoking the council (Phase 3).** Reasoning: forces Sean to commit to opinions before validation; protects against passive acceptance of the chairman's synthesis.
- **Bucket council output into APPLY / JUDGE / REJECT / DEFER (Task 5.1).** Reasoning: prevents over-rewriting on unanimous-but-wrong recommendations, and gives explicit decision-rationale for split-panel calls.
- **Three explicit sanity gates (CIIA scrub, JD-keyword mirror, link health) before lock (Phase 6).** Reasoning: CIIA is legally non-negotiable, JD-keyword mirror is the highest-leverage ATS lever, and `seanwinslow.com` is the most likely bad-link source given the personal-site-deferred status.
- **Hold portfolio-piece anchors (D1–D4) for Phase 8 application-cadence iteration.** Reasoning: they require sanitized docs not yet published; adding them as council questions over-extends the council attention budget.
- **Set the lock target at Mon 2026-05-19 09:00, same day as personal-site deploy.** Reasoning: applications start Mon 2026-05-19 (Phase 5 Task 5.2 cadence) and the resume should be ready when the apply cadence begins, not a day late.

---

## Execution Handoff

Plan complete and saved to [`2026-05-17-resume-council-plan.md`](2026-05-17-resume-council-plan.md).

Most of this plan is Sean-owned work — drafting, decisions, council invocation, judgment calls. Claude's role is bounded: research synthesis (already done — see Inputs Already Gathered), draft pressure-testing on individual bullets if requested, council prompt assembly help (Task 2.3 Step 1), CIIA grep gate (Task 6.1), JD-keyword mirror scoring (Task 6.2), link-health check (Task 6.3). The resume copy itself is Sean's.

**Two execution options:**

1. **Inline Execution (recommended)** — Walk this plan task-by-task in this session using `superpowers:executing-plans`. Strongly preferred for Phases 2–4 (council prompt + invocation) because the prompt assembly benefits from Sean's edits in real time, and the `/llm-council` invocation is one tool call. Phases 5–7 (synthesis + sanity gates + lock) are also better inline because Sean's voice is non-delegable.

2. **Subagent-Driven (not recommended for this plan)** — Fresh subagent per task with two-stage review. Reasonable for Tasks 6.1–6.3 (mechanical gates) but counterproductive for Tasks 3.1 (pre-council answers) and 5.1–5.3 (council synthesis + voice-preserving edits).

**Suggested kickoff right now:**
- Start with **Task 1.1** (30 min, decides resume's job in the funnel — sets the redraft constraints).
- Then **Task 2.1 Step 4** (5 min, checks whether the resume needs the 2026-05-12 ship freshness patch from Task 2.2 before going to council).
- That sequence gates whether Phase 2.2 is needed at all, before Sean commits to a full Saturday-evening session.

When you're ready, tell me which task you want to walk first.
