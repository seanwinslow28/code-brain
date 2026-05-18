---
title: "Portfolio Gap-Fill + Application-Cadence Reprioritization"
type: design
project: prj-job-hunt-2026
created: 2026-05-18
status: draft
related_roadmap: ../../../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
synthesis_sources:
  - vault/20_projects/prj-job-hunt-2026/nate-jones-portfolio-strategy-2026-05-17.md
  - vault/40_knowledge/references/ref-aakash-ai-pm-interview-2026.md
  - vault/40_knowledge/references/ref-aakash-pm-github-google-hire.md
  - vault/40_knowledge/references/ref-aakash-ai-pm-behavioral-interview.md
  - vault/40_knowledge/references/ref-aakash-claude-code-job-search-os.md
  - vault/20_projects/research/2026-05-18-enterprise-ai-pm-skill-gaps.md
  - vault/20_projects/research/2026-05-18-mcp-prompt-injection-hardening.md  # pending — LDR running
ai-context: "Design doc for an 8-week portfolio gap-fill + application-cadence reprioritization sprint targeting Enterprise AI PM roles. Synthesizes Nate B Jones (Phase 4 NET-NEW projects) + Aakash Gupta (interview-readiness) + Gemini DR-Max (Enterprise-PM accountability shape). Reprioritizes the unified roadmap so applications drop to 1–2/week Tier-1-only until the portfolio-complete gate clears."
---

# Portfolio Gap-Fill + Application-Cadence Reprioritization

> **Status:** draft (2026-05-18). Replaces no prior design; layered on top of the unified roadmap. The terminal output of this spec is a set of new Tasks (16+) to be appended to `2026-05-06-unified-roadmap.md` via the `writing-plans` skill.

---

## 1. Context — Why this design exists

The unified roadmap (Tasks 0–15) is a strong artifact-extraction plan, well-anchored on Nate Jones's seven-skills framework. But two failure modes were drifting toward us:

1. **Premature application cadence.** Master plan Phase 5 Task 5.2 fires the 5/week application volume starting Week 3 (week of 2026-05-19, i.e., tomorrow). Sean's own honest read: "I keep getting told to add things to my bare bones/unfinished portfolio and apply to jobs that are way out of my league... I don't want to show up with a pocket of half-finished and unpolished projects."
2. **Skill-gap blind spots.** The roadmap's existing Nate-aligned Tasks 0–15 demonstrate **technical capability**. They don't yet demonstrate the **PM accountability surface** an Enterprise AI PM hiring manager screens for. A Gemini DR-Max research panel (2026-05-18, $7.00, 80KB report) returned the load-bearing finding:

   > *"Sean has proven he is a highly capable AI Engineer. To prove he is a Tier-1 Enterprise AI PM, he must close the gaps related to business value, organizational adoption, and compliance."*

The five input documents triangulate on the same diagnosis from three directions:

| Source | What it tells us |
|---|---|
| `nate-jones-portfolio-strategy-2026-05-17.md` | Six NET-NEW Phase 4 projects not yet in the roadmap (cost calculator, enterprise AP agent spec, build-vs-buy framework, narrated working session, AgentLens, etc.). Sean's portfolio scores 0 fours, 4 threes, 3 twos against Nate's seven skills — substance exists, packaging doesn't. |
| `ref-aakash-ai-pm-interview-2026.md` | Interview test has shifted to AI-specific behavioral depth in every answer. Vibe-coding rounds (Cursor / Bolt / v0 / Lovable) catch candidates off-guard. Safety must surface by minute 40 of every interview. |
| `ref-aakash-ai-pm-behavioral-interview.md` | 5 behavioral categories + 40 AI-PM-specific questions + STAR+M structure where "+M" = model metrics (precision/recall, F1, latency, cost-per-inference). Sean has zero documented story bank. |
| `ref-aakash-pm-github-google-hire.md` | Shubham Saboo's 6 elements that landed him Senior AI PM at Google. Sean's GitHub needs an audit against these. |
| `ref-aakash-claude-code-job-search-os.md` | "Mass-applying with AI doesn't work." Aakash's $49 productized 18-skill system. Sean's `job_feed` + `target-companies.md` already covers 30% of this but the resume-tailoring / outreach-draft / debrief loops aren't wired. |

The Gemini DR-Max report (`vault/20_projects/research/2026-05-18-enterprise-ai-pm-skill-gaps.md`) adds the missing fourth direction: **enterprise PM accountability shape**. The panel (Tier-1 hiring manager + Senior AI Eng Mgr + Fortune 500 Procurement + Compliance/MRM officer) returns 10 JD-driven skills that don't appear on Nate's seven-skill framework, ranked by % of Tier-1 JDs that mention each.

---

## 2. Goals

1. **Reframe the existing portfolio + add 16 NEW artifacts** that demonstrate Enterprise AI PM accountability (business value, organizational adoption, compliance, HITL UX) — not just engineering capability.
2. **Defer mass application cadence** until a defined gate clears. Drop from 5/week → 1–2/week Tier-1-only until the gate. Resume full 5/week only after gate.
3. **Stand up interview-readiness infrastructure** that's measurable (mock-score-able), not just felt — behavioral story bank, TMAY 2-min, AI vocab drill, mock interview infra, GitHub audit.
4. **Lock the operating-model Tier-A truths.** No recommendation in this design pushes below $100K walk-away, requires 5-days-in-office, breaches the agents-draft / Sean-sends boundary, or violates the Friday 4:30 retro / 8:30–9:30 AM sacred / 1–2 PM mandatory break / 5:30 PM hard-stop containers.

---

## 3. Non-Goals (explicit out-of-scope)

- **Do not build `agentlens`** (Nate Phase 4 Project #8 flagship AgentOps observability layer). 120 hours over 10 weeks. Defer until Tier 1 + Tier 2 inbound check; existing Task 11 dashboard (`fleet.seanwinslow.com`) partially fills this slot at zero marginal cost.
- **Do not pivot to vertical AI product shape.** DR-Max Q4 confirms Sean's stack is HORIZONTAL (Notion/Linear/Atlassian/Glean shape). Lean HORIZONTAL hard; don't manufacture a domain-specific vertical eval to enter the OTHER fork.
- **Do not add strategic-fork forks of target-company repos as a dedicated Task.** Element 4 of Shubham's six is a lightweight 15-min/wk habit, not a Task — cosmetic, low signal-to-noise pre-employment.
- **Do not build AI Product Sense / AI Success Metrics / AI Product Design case practice as standalone Tasks.** Fold AI Product Sense practice into per-company prep packets (Tier 2 A4); skip the other two as out-of-scope.
- **Do not extend Phase C past July 13.** July 4 is the gate floor; July 13 is the hard stop. If gate (A AND C) isn't both-green by 7/4, re-scope, don't extend.

---

## 4. Approach Selection — Why Approach 2 (Compound-Payoff)

Three approaches considered (see brainstorming session transcript). Sean selected **Approach 2 (Compound-Payoff Reprioritization)** for the following reasons:

- **He has the time.** Layoff (2026-05-04) freed full-time deep-work blocks. The constraint Approach 3 (Phased Gate, Balanced) was hedging against — burnout from too much in-flight — doesn't bind here.
- **The gap landscape is large.** 24 deliverables across 8 weeks = ~3/week. Compound payoff means each deliverable doubles as a portfolio artifact AND an interview-prep asset where possible (e.g., per-company packets become Substack posts; vibe-coding reps become ledger rows).
- **DR-Max additions are mostly pure writing.** Of the 7 new DR-Max-surfaced artifacts, 4 require NO coding (DR1 data readiness matrix, DR2 adoption playbook, DR3 system card, DR7 Discovery PRD). Two require LOW coding (DR5 ROI dashboard view, DR6 MCP audit). One requires Figma (DR4 HITL wireframes). The deep-work-token burn is FAR lower than implied by a 24-deliverable count.
- **The "AI Evangelist in non-AI orgs → AI-native operator with proof artifacts" narrative arc is uniquely strong.** Compound Approach maximizes the surface area on which this narrative compounds (every ledger entry adds a proof point).

---

## 5. Gate Definition (Decision E: A AND C, July 4 floor)

The **portfolio-complete gate** that unlocks 5/week application cadence is binary AND-gated:

### Gate A — Artifact-Count

All of the following MUST be shipped + linked on `seanwinslow.com/transactions/`:

- All **16 Tier 1 items** below
- At least **6 of 8 Tier 2 items**
- LinkedIn profile refresh (banner / headline / About / "Open to Work" recruiter-only)
- Behavioral story bank (5–7 STAR+M stories) DOCUMENTED in `vault/20_projects/prj-job-hunt-2026/interview-prep/story-bank.md`

### Gate C — Mock Interview Score

3 consecutive mock interviews (different question types) MUST score **8+/10 across all 8 Aakash dimensions**:

1. Timing (under 2:30 for behavioral, under 4 min for product sense)
2. Structure (clear arc, no rambling)
3. Impact specificity (named metrics, not "improved by a lot")
4. Confidence signals (declarative, no hedging)
5. Filler words (under 5 per response)
6. Weakness flipping ("AI evangelist in non-AI org" arc applied)
7. Information control (no volunteered weaknesses)
8. Memorability (story has a specific scene, not abstract claims)

Mock infra: LLM Council "interview-grader" profile (extension of premium profile) + record-via-Voice-Memos + transcribe-via-Granola-or-Otter + grade-via-Council.

### Gate Floor

**July 4, 2026.** If A AND C aren't both-green by 7/4, the scope re-cuts — Tier 2 items get demoted to Tier 3, NOT extended into Phase D. The application cadence resumes regardless at 7/4 because the longer the cadence stays at 1–2/week, the higher the runway pressure.

**July 13, 2026 hard stop.** Absolute ceiling. By 7/13 cadence is at 5/week no matter what.

---

## 6. Scope — The 24 Deliverables

### Tier 1 (16 items — must close before gate)

**Interview-readiness (Aakash) — 5:**

| ID | Artifact | Time | Owner |
|---|---|---|---|
| A1 | Behavioral story bank (5–7 STAR+M stories sourced from solo Superuser Pack work + the AI-evangelist-at-NYL/Block arc) | 12–15 hrs | Sean writes, Council grades |
| A2 | TMAY 2-min script (Hook → AI Inflection → Proof Points → Why Here; "AI evangelist → AI-native operator" framing) | 4–6 hrs | Sean writes, Council grades |
| A3 | AI technical vocabulary drill (precision/recall, F1, embeddings, RAG vs fine-tune, model drift; PLUS AgentOps vendors — Datadog LLM Obs / LangSmith / Arize / Helicone / Mezmo / Galileo / W&B Weave; PLUS 3 beyond-Nate failure patterns — Planner Misalignment / Schema Violations / Brittle Prompt Dependencies; PLUS "Trust Economics" term) | 8–10 hrs spread across Phase A | Spaced-repetition habit |
| A6 | Mock interview infrastructure: LLM Council "interview-grader" profile + record/transcribe pipeline (Voice Memos → Granola transcription → Council grading on 8 dimensions) | 6–8 hrs | Build once, use 20+ times |
| A11 | GitHub profile audit against Shubham's 6 elements (positioning bio, contribution shape, pinned repos, READMEs polished with Problem/Solution/Tradeoffs/What-I-Learned sections) | 4 hrs | One-shot |

**Portfolio skill-expansion (Nate Phase 4 NET-NEW) — 4:**

| ID | Artifact | Time | Maps to Nate skill |
|---|---|---|---|
| N2 | LDR grounding-collapse post-mortem extracted to standalone repo `seanwinslow/ldr-grounding-collapse` + Substack post (Nate's #2 named "failure post-mortem" artifact) | 8 hrs over 4 days | Failure pattern recognition |
| N4 | `enterprise-ap-agent-spec` (full PRD-grade agent product spec for enterprise AP-automation flow — problem → user stories → eval framework → escalation tree → trust boundary review → cost model at 5K invoices/mo → build-vs-buy memo → SOC 2 + SR-11-7 mapping) | 24 hrs over 10 days | Specification precision (PRIMARY) |
| N5 | `build-vs-buy-framework` (12-dimension vendor-eval rubric across Anthropic Skills / OpenAI Assistants / Vertex Agent Builder / Bedrock Agents / self-host + worked example + Notion template) | 18 hrs over 10 days | Trust boundary, Cost economics — closes the Enterprise-PM vendor-eval blind spot |
| N7 | 35-min narrated working session Loom (real failure being diagnosed live — e.g., the 2026-05-16 cluster-diversity probe → HDBSCAN retrofit). "Almost-unfakeable" per Nate. | 8 hrs over 3 days | All 7 skills in motion |

**Enterprise PM accountability (DR-Max NET-NEW) — 7:**

| ID | Artifact | Severity | Time | Coding? | Closes |
|---|---|---|---|---|---|
| DR1 | `enterprise-data-readiness-matrix.md` — consulting-style rubric for evaluating whether a Fortune 500's data (canonical IDs, embedding hygiene, freshness, lineage, dedup) is "AI-ready" before agent deployment | HIGH | 10–15 hrs | NO | 85% of Tier-1 JDs name this |
| DR2 | `AI-Adoption-Playbook.pdf` — 90-day rollout plan applied to Substack-Drafter agent + "Time-to-Trust" funnel + champion-enablement program (Klarna / BofA Erica / JPM LLM Suite case studies cited) | HIGH | 15–20 hrs | NO | 78% — change management |
| DR3 | `Superuser-System-Card.md` — modeled after Anthropic system cards; maps Sean's 6 failure modes + 7/10 eval baseline to SR-11-7 tiering + EU AI Act Annex IV transparency requirements + post-market monitoring plan | MED/HIGH | 12–15 hrs | NO | Regulatory accountability |
| DR4 | `HITL-Escalation-Wireframes` — Figma prototype showing agent pausing on confidence-threshold drop + compiling "Evidence Pack" + surfacing contextual approval/edit screen to human operator (graceful degradation under 800ms acknowledgement budget) | MED | 20 hrs | NO (Figma) | 70% — HITL UX |
| DR5 | `Executive-ROI-Dashboard-View` — adds CFO-readable view to `fleet.seanwinslow.com` translating telemetry into "Hours Saved" / "Escalation Cost Avoided" / "Estimated SLA Breach Cost" | MED | 10–15 hrs | LOW | 82% — business ROI |
| DR6 | MCP prompt-injection security audit of `@swins/intent-engineering-mcp@0.1.0` + hardening writeup (LDR query running in parallel will inform the checklist) | MED | 4–6 hrs | LOW | Direct DR-Max follow-up flag; GitHub MCP precedent |
| DR7 | `Discovery PRD` (cross-functional translation artifact mapping technical infra to non-technical user persona — your AI-evangelist-at-NYL/Block backstory IS the raw material for this) | MED | 8–10 hrs | NO | 90% — cross-functional translation (the most-cited JD skill) |

### Tier 2 (8 items — ship if Phase B gets through them)

| ID | Artifact | Time | Notes |
|---|---|---|---|
| A4 | Per-company interview prep packets (top 5 from `target-companies.md`; each becomes a Substack post) | 4–6 hrs each × 5 = 20–30 hrs | Absorb AI Product Sense practice into these |
| A5 | Vibe coding reps (2–3/week starting Phase B, alternating Bolt and v0; each rep = `/transactions/` ledger row) | ~2 hrs/rep | Drill + portfolio compound |
| A8 | AI safety story (Substack post) — anchor on LDR grounding-collapse + Judge Layer + the trust-boundary hooks | 6–8 hrs | Story-bank entry that ALSO publishes |
| A9 | "I am my own ML engineer" story (Substack post) — Qwen3-14B routing decision + cluster-and-sample diagnostic | 6–8 hrs | Story-bank entry that ALSO publishes |
| A13 | Sean-specific Job Search OS (8th–9th portfolio artifact) — resume-tailoring + outreach-draft + interview-prep + post-interview-debrief loops; standalone repo framed "I built this for my own search" | 20–25 hrs | Extends `job_feed` + `daily_driver` + `Substack-Drafter` |
| N1 | `vault-synthesizer-evals` standalone extraction + Substack post | 12 hrs over 5 days | Eval suite is buried in monorepo; lift to public repo |
| N3 | `agent-cost-calculator` interactive web tool at `cost.seanwinslow.com` | 16 hrs over 7 days | Rarest senior-level artifact per Nate |
| N6 | "Defeating Cluster Bias in Vault Retrieval" 2,000-word post + standalone `retrieval_diversity.py` + `concept_edges.py` module extraction | 10 hrs | CCA-exam-relevant context-engineering signal |

### Tier 3 (defer, no Task)

- A7 strategic forks of target-company repos (15-min/wk lightweight habit; no Task)
- N8 `agentlens` flagship (deferred to post-gate inbound check)
- Vertical AI eval suite (don't fork from horizontal)
- Aakash AI Product Design / AI Success Metrics standalone case practice (folded into A4)

---

## 7. Sequencing — Phase A / B / C calendar

### Phase A — Weeks 1–3 (2026-05-19 → 2026-06-08)

**Goal:** Interview survival + PM-accountability framing of existing portfolio.

**Ships:**
- **A1** Behavioral story bank locked
- **A2** TMAY 2-min written + Council-graded 8+/10
- **A3** Vocab drill started (spaced repetition habit running)
- **A6** Mock infra live + 2 mock interviews scored
- **A11** GitHub profile audit done
- **DR1** Enterprise Data Readiness Matrix shipped
- **DR3** Superuser System Card shipped
- **DR6** MCP audit + hardening writeup shipped (LDR research findings folded in)
- **DR7** Discovery PRD shipped
- **N2** LDR grounding-collapse extracted to standalone repo + Substack post

**By 6/8: 10 net-new artifacts total — 6 land in `/transactions/` ledger (A11, DR1, DR3, DR6, DR7, N2), 4 are private prep (A1, A2, A3, A6). Story bank locked. Mock score 8+/10 at least once.**

Apps: 1/week Tier-1-only (Anthropic / Stripe / Notion / Datadog / Linear / Atlassian / ServiceNow / Sierra / Decagon / Glean / Box / Figma / Scale AI). 3 apps in Phase A.

### Phase B — Weeks 4–6 (2026-06-09 → 2026-06-29)

**Goal:** Compound payoff — every ship doubles as portfolio AND interview-prep AND ledger entry.

**Ships:**
- **N4** Enterprise AP agent spec
- **N5** Build-vs-buy framework
- **N7** 35-min narrated working session Loom
- **DR2** AI Adoption Playbook
- **DR4** HITL Escalation Wireframes (Figma)
- **DR5** Executive ROI Dashboard view added to `fleet.seanwinslow.com`
- **A4** Per-company packets (top 5; 2 published as Substack posts)
- **A5** Vibe coding reps START (2/week, alternating Bolt + v0; ~6 reps = 6 ledger rows)
- **A8** AI safety story (Substack post)
- **A9** ML engineer story (Substack post)
- **Animation pipeline ships 2026-06-11** (existing master plan commitment, not in 24-item scope)

**By 6/29: ~19 net-new ledger entries added in Phase B (cumulative ~25 since 5/19). Top 5 target-company prep packets locked.**

Apps: 2/week Tier-1-only. 6 apps in Phase B.

### Phase C — Weeks 7–8 (2026-06-30 → 2026-07-13)

**Goal:** Force-multiplier + remaining gap items + GATE EVALUATION.

**Ships:**
- **A13** Job Search OS standalone repo
- **N1** vault-synthesizer-evals standalone repo
- **N3** agent-cost-calculator web tool at `cost.seanwinslow.com`
- **N6** "Defeating Cluster Bias" Substack post + module extraction
- Remaining vibe coding reps (~4 more = 4 ledger rows)
- **GATE EVALUATION Friday 2026-07-04**

**By 7/4: gate criteria evaluated.** If A AND C both-green → ramp to 5/week cadence beginning Monday 7/7. If not both-green by 7/13 → re-cut Tier 2, NOT extend.

---

## 8. Application Cadence Architecture

### Floor (Approach B)

**1–2 ultra-tailored Tier-1-only applications per week** through gate. Each application:

- Tailored intro paragraph naming a specific JD requirement Sean's portfolio addresses
- One specific `/transactions/` ledger row linked in the application as the proof artifact
- Outreach draft to one warm contact (Larry / network) sent same-day where applicable
- Logged in `vault/20_projects/prj-job-hunt-2026/job-feed/applications-log.md`

### Companies in scope (Tier-1 only during Phase A/B/C)

From `target-companies.md` Tier 1: Anthropic, Stripe, Notion, Datadog, Linear, Atlassian (Rovo), ServiceNow (NowAssist), Sierra, Decagon, Glean, Box, Figma, Scale AI, plus Boston-metro AI-native scale-ups (Liberate, Manifold Bio, Pair Team).

### Switch conditions

- **Switch to Approach C (3/week) only if:** by end of Phase B (6/29), zero interview loops have surfaced AND response rate < 5%. Then broaden into Tier-2 companies at 3/week customization-light.
- **Switch to Approach A (zero apps) only if:** a Tier-1 final-round loop lands and Sean needs 5 days of full prep deep-work to maximize that single shot.

---

## 9. Verification gate / acceptance criteria

The design is *implemented* when ALL of these are true:

1. The unified roadmap (`2026-05-06-unified-roadmap.md`) contains new Tasks 16+ enumerating each Tier 1 + Tier 2 deliverable with maps-to + files + step-by-step + verification gate sections in the existing task convention.
2. Task 7 STOP-DOING list is amended with the Tier 3 deferrals from Section 6.
3. This Week's 5 Decisions section is amended with:
   - Decision 6 (NEW): Application cadence drops to 1–2/week Tier-1-only through gate
   - Decision 7 (NEW): Mock infra extends LLM Council premium profile (no standalone Skill)
4. Decision 5 (existing) is amended with the gate-conditional ramp.
5. Verification: `python3 scripts/validate.py` passes with 0 errors after the amendments.
6. Every artifact has a row reserved in `seanwinslow.com/transactions/` ledger schema (no NEW `surface` enum values required).

---

## 10. Risks + mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Deep-work burnout despite pure-writing skew | MED | HIGH | Mandatory 1–2 PM break + 5:30 PM hard stop preserved. Friday retro tracks fatigue score. If fatigue 7+/10 for 2 weeks, scope cuts to Tier 1 only. |
| Tier-1 application response rate < 5% in Phase A (3 apps over 3 weeks = small sample) | HIGH | MED | Sample size is too small to act on in Phase A. Reassess at end of Phase B (6/29) with 9 apps total. |
| Mock interview score plateaus below 8+/10 across 3 consecutive | MED | HIGH | A3 vocab drill running across Phase A catches this early. Add a 4th mock attempt + Council debrief if score is 6–7/10 after attempt 3. |
| DR-Max-surfaced artifacts (DR1–DR7) overlap with already_identified_gaps in unintended ways | LOW | LOW | DR-Max's own validation step de-duplicated. Spot-check during writing-plans pass. |
| MCP prompt-injection LDR query (running in background) returns degraded grounding (Qwen3-14B fabrication risk per the 2026-05-05 incident) | MED | LOW | Single-shape topic per CLAUDE.md routing rule — LDR designed to handle this. If output shows fabricated entities, escalate to a $0.40 Gemini DR (not DR-Max) follow-up. |
| Animation pipeline 6/11 ship slips and consumes Phase B deep-work tokens | MED | MED | Animation is existing master plan commitment. If it slips past 6/13, demote 1 Tier 2 item to absorb the delay. |
| LinkedIn refresh + ledger deploy on 2026-05-19 triggers premature inbound that exceeds 1–2/week capacity | LOW | LOW | Recruiter-only "Open to Work" (not public green frame) keeps inbound throttled. If inbound exceeds 2/week, switch to "I'm in deep portfolio mode — would love to circle back in 4 weeks" with calendar link. |

---

## 11. Open questions (resolved during brainstorm)

| # | Question | Resolution |
|---|---|---|
| Q1 | Application cadence floor | B — 1–2/week Tier-1-only through gate |
| Q2 | Gate definition | E — A (artifact-count) AND C (mock-score 8+/10 × 3) |
| Q3a | Tier triage | Accepted as listed (Tier 1 / Tier 2 / Tier 3) |
| Q3b | Story bank source material | Mostly solo Superuser Pack work; Block + NYL stories framed as "AI evangelist in non-AI orgs" arc |
| Q4 | Approach | 2 — Compound-Payoff Reprioritization |
| Q5 | Research firing | A — Fire DR-Max now (done); LDR oneshot for MCP audit (running) |
| Q6 | Prompt review | Approved with 4-year → 1-year tenure correction |
| Q7 | Final scope | 24 deliverables (16 Tier 1 + 8 Tier 2 + Tier 3 deferred); July 4 floor / July 13 hard stop |

### Still open (do not block design doc commit)

- **MCP audit checklist content** — pending LDR query results (in flight). Will fold into DR6 task definition when LDR completes.
- **Vibe coding tool selection** — alternate Bolt + v0 starting Phase B. Sean's call on the alternating cadence.
- **Per-company packet ordering** — top 5 from `target-companies.md` priority. Default order: Anthropic, Stripe, Notion, Datadog, Linear. Adjust based on inbound signal.

---

## 12. Compounding payoff (why this works)

Every artifact in this scope **either reframes an existing piece of infrastructure for a PM audience OR fills a specific JD-mentioned skill gap**. Net result:

1. **Story bank stops being aspirational.** Every Tier 1 + Tier 2 artifact has a STAR+M story attached. The story bank populates organically as Phase A → B → C proceeds.
2. **Ledger becomes the lead artifact.** `seanwinslow.com/transactions/` grows from 5 entries (current) → ~33+ entries (post-gate). Resume becomes the secondary artifact.
3. **Inbound recruiter signal compounds.** Each Substack post (~6 in scope) is a separate inbound surface. Each `/transactions/` row is a separate URL recruiters can land on. LinkedIn refresh (Mon 5/19) activates the throttled inbound channel.
4. **Interview-readiness is measurable.** Gate C means we'll KNOW whether Sean is ready, not feel it.
5. **The "AI evangelist → AI-native operator" narrative arc has a public artifact spine.** DR7 Discovery PRD is the explicit translation artifact for this arc. N4 enterprise-ap-spec is the proof Sean can do this for someone else's org.

---

## 13. Decisions log (final)

For inclusion in `vault/20_projects/prj-job-hunt-2026/README.md` Decisions section:

- **2026-05-18 — Application cadence drops to 1–2/week Tier-1-only through 2026-07-04 gate.** Switch only if Tier-1 final-round loop lands (then zero apps for that week) or end-of-Phase-B response rate < 5% (then 3/week Tier-2 customization-light).
- **2026-05-18 — Portfolio-complete gate is binary AND-gated: Gate A (16 Tier 1 + 6 Tier 2 artifacts shipped) AND Gate C (3 consecutive 8+/10 mock interviews).** July 4 floor, July 13 hard stop.
- **2026-05-18 — Mock infrastructure extends LLM Council `premium` profile as "interview-grader."** No standalone Claude Skill.
- **2026-05-18 — Stack stays HORIZONTAL.** No vertical AI eval suite. DR-Max Q4 finding.
- **2026-05-18 — `agentlens` flagship deferred.** Existing Task 11 fleet dashboard partially fills the AgentOps observability slot.

---

## 14. References

- Synthesis sources (5): see frontmatter
- Research outputs (2):
  - `vault/20_projects/research/2026-05-18-enterprise-ai-pm-skill-gaps.md` (Gemini DR-Max, $7.00, 14 min, 79 citations)
  - `vault/20_projects/research/2026-05-18-mcp-prompt-injection-hardening.md` (LDR oneshot, $0.00, in flight)
- Master plan + existing roadmap:
  - `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md`
  - `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`
- Operating-model Tier-A truths:
  - `vault/05_atlas/operating-models/job-hunt-2026/operating-model.md`
  - `vault/05_atlas/operating-models/job-hunt-2026/SOUL.md`
  - `vault/05_atlas/operating-models/job-hunt-2026/USER.md`
  - `vault/05_atlas/operating-models/job-hunt-2026/HEARTBEAT.md`

---

*Generated 2026-05-18 in brainstorming session. Next step: `writing-plans` skill converts this design into per-task additions (Tasks 16–39) for `2026-05-06-unified-roadmap.md`.*
