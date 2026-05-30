---
type: interview-prep
artifact: story-bank-source-material
project: prj-job-hunt-2026
status: draft
created: 2026-05-30
related:
  - story-bank.md
  - ../onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md  # Task 16
ai-context: "Raw 10-candidate audit feeding the curated Story Bank (story-bank.md). This is the 'show your work' layer — every candidate story with its raw STAR+M ingredients, source files, and a cull verdict. The curated bank pulls the 7 strongest; this file keeps the other 3 warm as swing/backup material."
---

# Story Bank — Source Material (10-Candidate Audit)

> **What this is.** Task 16 Step 1 + Step 2 raw output. Ten candidate stories pulled from solo Code-Brain work + The Block + earlier roles, each converted to STAR+M ingredients. Step 3 culls to 7 in [`story-bank.md`](story-bank.md). This file is the bench — it keeps the cut stories warm and preserves the source-file provenance so any story can be re-grounded fast.
>
> **Why a separate source file.** When an interviewer asks a follow-up ("what was the actual failure rate?"), you need the receipt, not a vibe. Every Action/Metric line below cites the file it came from. That traceability *is* the credibility — it's the same move as a commit message pointing at a diff.

---

## Factual ground-truth + open confirms

Lock these before drilling — every story inherits them.

| Fact | Status | Source |
|---|---|---|
| Laid off from The Block 2026-05-04, cost-cutting (not performance) | ✅ confirmed | personal-context v2.0 |
| The Block role: Associate PM (Technical), Nov 10 2025 → May 4 2026, reported to Ed Rupkus | ✅ confirmed | personal-context v2.0 |
| The Block products: `.Co` + Campus; ETF page workflow, Jira ticket standards, biweekly P&E updates | ✅ confirmed | the-block/ skills (etf-page-creator, jira-ticket-writer, biweekly-jira-update) |
| **~10 years freelancing/permalancing at New York Life** (financial-services); media manager → **AI product operations lead**; the go-to person for AI footage + recommendations | ✅ confirmed 2026-05-30 | Sean direct |
| 2024 pivot: PM classes + AI tools to switch lanes; landed The Block Nov 2025 (first FT job w/ benefits) | ✅ confirmed | personal-context v2.0 |
| The Block: **35 ETF pages** shipped on the repeatable workflow | ✅ confirmed 2026-05-30 | Sean direct |
| Solo-work technical facts (every metric below) | ✅ confirmed | Code-Brain CLAUDE.md + agents-sdk docs |

**Resolved 2026-05-30:** the "decade freelancer" in the personal-context doc and the "financial-services org" in the roadmap's pre-drafted TMAY hook are the **same thing** — New York Life. Sean spent ~10 years there freelancing/permalancing, rising from media manager to AI product operations lead. That means the evangelist arc isn't a side-narrative — *being the AI person was his literal job title at a financial-services giant.* That's a stronger hook than the placeholder, and it's now load-bearing in both the Story Bank and the TMAY.

---

## The 10 candidates

Each: **Situation** (1 sentence) · **Task** (PM accountability) · **Action** (3–4 bullets, named tools/architectures) · **Result** · **M** (the metric line) · **Category** · **Cull verdict**.

### C1 — LDR grounding-collapse catch (the fabrication post-mortem)

- **S:** My local deep-research agent (Qwen3-14B + SearXNG) returned a polished, confident research brief that was substantially fabricated — invented libraries, fake Microsoft docs URLs.
- **T:** Decide whether local research could be trusted for portfolio/job-hunt decisions, and if not, build the guardrail.
- **A:**
  - Diagnosed the failure as *citation-grounding collapse* — the 14B model couldn't ground citations across ≥3 targets at once, so it hallucinated entities (`PureMCPClient`, `MCPCatalog (Central)`, `MCP ADK`) and `learn.microsoft.com` URLs that don't exist.
  - Wrote a routing rule: any research that compounds 3+ independent investigations routes to Gemini Deep Research (cloud, grounded), never local LDR.
  - **Retained the bad output as a labeled specimen** (`status: superseded`, fabrications preserved + annotated) instead of deleting it — a permanent regression fixture.
- **R:** Zero fabricated-citation briefs entered the decision pipeline after the rule. The specimen now seeds the eval suite and a planned post-mortem artifact (roadmap Task 25).
- **M:** Failure mode caught *before* it shaped a decision; 1 documented routing rule; 900s local timeout + multi-target citation collapse named as the two independent triggers.
- **Category:** AI Ethics/Safety (primary) · Technical AI Knowledge (secondary)
- **Verdict:** ✅ **KEEP** — this is the strongest safety story; "I caught my own agent lying and built the guardrail" is non-fakeable.

### C2 — Eval suite shipped intentionally red

- **S:** My nightly vault-synthesizer silently regressed for ~9 days — it was producing near-empty output and nothing flagged it.
- **T:** Build the measurement layer that should have existed, and do it honestly.
- **A:**
  - Ran error analysis on 17 days of real production logs first; derived a **6-mode failure taxonomy** from actual stderr, not imagined cases.
  - Built a 10-case eval suite and **shipped it intentionally red — baseline 1/10** — so the score had somewhere honest to climb from.
  - Fixed in public across iterations; documented the progression 1/10 → 7/10.
- **R:** The silent regression became visible and measurable; the suite is now the gate for synthesizer changes.
- **M:** 10 cases, 6 failure modes, 1/10 → 7/10 progression, grounded in 17 days of logs.
- **Category:** AI Product Experience (primary) · eval design
- **Verdict:** ✅ **KEEP** — "evals are the new PRDs"; shipping red on purpose is a memorable, judgment-forward move.

### C3 — Judge Layer / control architecture

- **S:** My autonomous Substack-drafter agent could, in principle, fabricate a quote and attribute it to a real (ex-employer) person — a reputational live wire.
- **T:** Add a control surface between the agent's intent and any action, without rebuilding the agent.
- **A:**
  - Designed an **`ActionProposal` schema** (8 Pydantic fields: intended_action, target_surface, authorization_basis, expected_consequence, exposure_level, human_review_required, + 2 optional) — the agent must declare intent before acting.
  - Wrote a declarative **YAML policy** (4 rules, each with real-incident provenance) evaluated by a local model ($0/decision on gemma4:e4b); outcomes ALLOW / BLOCK / REVISE / ESCALATE / JUDGE_UNAVAILABLE.
  - Chose **intercept, don't rebuild** — wrapped the one already-complete agent rather than retrofitting all 8; **fail-open** with a Pushover alert + ledger entry so cadence survives a judge outage (my manual publish gate stays the canonical control).
- **R:** Reframed my whole fleet from "I have agents with cost limits" to "I run actors inside a control architecture" — the exact phrase in the Anthropic FDE Boston JD.
- **M:** 8-field schema, 4 policy rules, $0/decision, 79+ tests pass; fail-open guarantee (evaluate() never raises).
- **Category:** AI Product Strategy (primary) · AI Ethics/Safety (secondary)
- **Verdict:** ✅ **KEEP** — the council's #1 piece; "control architecture" is the phrase that moves you from interesting to must-talk.

### C4 — Cluster-bias retrieval diagnostic

- **S:** My synthesizer kept surfacing the same few loud topics and missing quieter ones — a retrieval-diversity failure.
- **T:** Diagnose why and fix the retrieval, not just the symptom.
- **A:**
  - Identified the bias: naive top-k retrieval over-samples dense clusters.
  - Implemented **HDBSCAN cluster-and-sample** retrieval (`retrieval_diversity.py`) — cluster the embedding space, sample across clusters, not just by raw similarity.
  - Added an `evaluate_article_depth()` gate so shallow inputs get rejected with logged `rejected_reasons`.
- **R:** Cross-domain coverage improved; the synthesizer stopped echoing the loudest cluster.
- **M:** Named architecture (HDBSCAN), explicit depth-gate with logged reject reasons.
- **Category:** Technical AI Knowledge (primary)
- **Verdict:** ✅ **KEEP (as the named-architecture proof)** — this is the story that answers "the F1 score question": you can name embeddings, clustering, sampling tradeoffs cold.

### C5 — intent-engineering MCP server ship

- **S:** Karpathy's single top rec for 2026 was "stop building skills, start building MCP servers"; I had 118 skills and no portable artifact.
- **T:** Ship a real, installable MCP server that publishes my specification-engineering thesis.
- **A:**
  - Built `intent-engineering` MCP (3 tools: audit / scaffold / retrofit), pinned SDK, MIT license, Stdio transport.
  - Published to **npm + the MCP registry** (DNS-verified), 13 days ahead of the 5/25 target.
  - **Dogfooded it on my own 118 skills** — the audit tool found real anti-patterns; folded results back into the README.
- **R:** First concrete, installable instance of my thesis; recruiter-demoable in Claude Desktop end-to-end.
- **M:** 3 tools, npm + registry live, 23/25 dogfood score with zero anti-patterns on the best skills, shipped 13 days early.
- **Category:** AI Product Experience (primary) · AI Product Strategy (secondary)
- **Verdict:** ✅ **KEEP** — the flagship artifact; doubles as the TMAY proof point #1.

### C6 — Agent Fleet Observability Dashboard

- **S:** I had 14 SDK agents running on schedules with no single place to see fleet health; and a privacy problem (some agents touch a private job-feed).
- **T:** Ship a public observability dashboard without leaking private data.
- **A:**
  - Built a single-page static-site generator (no Chart.js, no CDN, inline SVG only) — survives screenshots, <50KB pre-data.
  - Made **privacy structural, not policy**: a public render pass physically never reads the private job-feed DB; two output dirs + a flag are the whole boundary.
  - Wired it to real telemetry across the fleet; auto-builds 06:00 daily via launchd → git push → Vercel.
- **R:** Live at fleet.seanwinslow.com; 55 tests, 85ms build, 0 public leaks of private data in smoke tests.
- **M:** 8+ agents surfaced, 85ms build, 55 tests, single-page <50KB, 0 privacy leaks.
- **Category:** Cross-Functional Collaboration (translates eng→stakeholder) · AI Product Experience
- **Verdict:** 🟡 **SWING** — strong shipping story; overlaps C5/C2. Hold as backup + TMAY proof point #3.

### C7 — The Block: cross-functional PM at a real org

- **S:** At The Block I owned PM workflows across the `.Co` and Campus products with a small Product & Engineering org going through leadership turnover.
- **T:** Keep cross-functional delivery moving (eng + design + content) during instability.
- **A:**
  - Standardized **Jira ticketing** (Epics / Design Stories / Implementation Stories) so eng and design shared one definition of ready/done.
  - Ran the **biweekly Product & Engineering status update** — the cross-team comprehension surface.
  - Built a repeatable **ETF page-creation workflow** (WordPress + a pending-ETF tracking sheet) spanning content + data + publishing.
  - Shipped **35 ETF pages** on that workflow.
- **R:** Cross-functional delivery stayed legible through the turnover; the templates were reusable enough to retain as portfolio reference.
- **M:** 35 ETF pages on a repeatable workflow; Jira ticket standard (Epics/Design/Implementation); biweekly P&E update held through a CPO departure + CEO change.
- **Category:** Cross-Functional Collaboration (primary) — the one *named-org* story
- **Verdict:** ✅ **KEEP** — you need at least one story set inside a real company with real coworkers; this is it. Needs a defensible metric.

### C8 — Substack-Drafter / cost economics + "agents draft, Sean sends"

- **S:** I wanted an agent that drafts public writing weekly without it ever publishing on its own or blowing my model budget.
- **T:** Build it cheap, safe, and voice-consistent.
- **A:**
  - **HybridRouter**: local Qwen3-14B first, cloud Sonnet only on fallback — keeps cost ~$0–0.10/run against a $0.10 cap.
  - 5-week **voice rotation** reading a voice-modes skill verbatim.
  - Hard-wired **"agents draft / Sean sends"** — no autonomous publish, ever (this is the Tier-A boundary the Judge Layer later made executable).
- **R:** A working build-in-public engine that respects both the wallet and the boundary.
- **M:** ~$0–0.10/run (cap $0.10), local-first routing, 0 autonomous publishes.
- **Category:** AI Product Strategy (cost economics — your one named skill gap, turned into a story) · swing
- **Verdict:** 🟡 **SWING (trade-off-eligible)** — best answer for "tell me about a cost/latency tradeoff." Cost economics was flagged as your one beginner skill; this converts it.

### C9 — Tier-1/Tier-2 synthesizer retrofit

- **S:** First-pass synthesizer output was generic; it summarized instead of surfacing the sharp, quotable insight.
- **T:** Raise output quality without a model upgrade.
- **A:** Quote-first prompt (T1), an `evaluate_article_depth()` gate (T1.5), HDBSCAN cluster-and-sample retrieval (T2).
- **R:** Sharper, less generic synthesis; measurable via the C2 eval suite.
- **M:** Multi-tier retrofit, quote-first + depth-gate + diversity-retrieval, measured by the 10-case suite.
- **Category:** Technical AI Knowledge / AI Product Experience
- **Verdict:** ❌ **CUT (merge into C4)** — same architecture family as C4; redundant. Keep as a C4 follow-up detail.

### C10 — The AI-evangelist → AI-native-operator arc (the layoff inflection)

- **S:** For ~10 years I was the AI person inside a financial-services org — New York Life, where I went from media manager to AI product operations lead — then carried that into The Block; the Block layoff (2026-05-04, cost-cutting) reset everything.
- **T:** Convert the reset into momentum instead of a gap.
- **A:**
  - Reframed: "I kept evangelizing AI inside orgs that wouldn't build it — so I went and built it myself."
  - Stood up an 8-week sprint producing hard-to-fake artifacts (MCP server, eval suite, control architecture, live dashboard).
  - Locked a target: AI PM > Tech PM > Creative PM.
- **R:** The layoff becomes the inflection point that produced the proof, not a hole in the timeline.
- **M:** 8+ shipped/in-flight artifacts in an 8-week window; the arc is the throughline of every other story.
- **Category:** Swing — TMAY-eligible / resilience / "why this pivot"
- **Verdict:** ✅ **KEEP (as the TMAY spine, not a standalone behavioral story)** — this is the frame the TMAY script is built on; in the bank it's the connective tissue every story bends back toward.

---

## Cull summary → the 7

| # | Story | Aakash category | Bank slot |
|---|---|---|---|
| C1 | LDR grounding-collapse catch | AI Ethics/Safety | Story 4 |
| C2 | Eval suite shipped red | AI Product Experience | Story 1 |
| C3 | Judge Layer control architecture | AI Product Strategy | Story 5 |
| C4 | Cluster-bias retrieval (HDBSCAN) | Technical AI Knowledge | Story 3 |
| C5 | intent-engineering MCP ship | AI Product Experience / Strategy | Story 2 |
| C7 | The Block cross-functional PM | Cross-Functional Collaboration | Story 6 |
| C8 | Substack-Drafter cost tradeoff | trade-off swing | Story 7 |
| — | C6 Fleet Dashboard | (backup swing) | bench |
| — | C9 Tier-retrofit | (merged into Story 3) | bench |
| — | C10 evangelist arc | TMAY spine | woven through all 7 |

**Coverage check (Aakash's 5 + swings):** AI Product Experience ✅ (S1, S2) · Technical AI Knowledge ✅ (S3) · Cross-Functional ✅ (S6) · AI Ethics/Safety ✅ (S4) · AI Product Strategy ✅ (S5) · trade-off swing ✅ (S7) · TMAY/resilience ✅ (the arc). All five categories covered with two swings to spare.
