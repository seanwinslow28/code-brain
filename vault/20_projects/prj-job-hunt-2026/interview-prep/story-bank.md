---
type: interview-prep
artifact: story-bank
project: prj-job-hunt-2026
status: draft
created: 2026-05-30
related:
  - story-bank-source-material.md
  - tmay-script.md
  - ../onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md  # Task 16
ai-context: "Curated behavioral Story Bank — 7 STAR+M stories across Aakash Gupta's 5 AI-PM interview categories, with the AI-evangelist arc layered on each. Drilled to <=2:30 spoken. Each carries an explicit M-line. Raw 10-candidate audit + source provenance in story-bank-source-material.md. Proof points feed tmay-script.md."
---

# Behavioral Story Bank

> **How to use this.** Seven stories, one per interview category, each ≤2:30 spoken. STAR+M = Situation · Task · Action · Result · **Metric**. The **M is the difference between a PM and a candidate who sounds like one** — it's the named number or named architecture that proves the story happened. Drill the **bold spoken line** in each; the bullets are recall scaffolding, not a script to read.
>
> **The arc that connects all seven.** Every story bends back to one throughline: *I spent years as the lone AI evangelist inside orgs that wouldn't build it, so after the Block layoff I went and built it myself — with proof.* You don't say that sentence in every story; you let each story demonstrate it. That's what makes a bank of solo-built stories answer "why are you pivoting into AI PM" without you ever having to argue it.
>
> **Drill targets (from the Task 19 grading rubric):** each answer scores 1–10 on timing, structure, impact specificity, confidence, filler (<3/min), weakness-flipping, information control, memorability. Gate C = 3 consecutive 8+/10 across all eight.

---

## Quick-reference matrix

| # | Story | Category | The one-line hook | The M (memorize cold) |
|---|---|---|---|---|
| 1 | Eval suite shipped red | AI Product Experience | "I shipped the scorecard at 1 out of 10 on purpose." | 10 cases · 6 failure modes · 1/10 → 7/10 · 17 days of logs |
| 2 | intent-engineering MCP | AI Product Experience / Strategy | "Karpathy said stop building skills and ship MCP servers — so I did, 13 days early." | 3 tools · npm + registry · 23/25 dogfood · 13 days early |
| 3 | Cluster-bias retrieval | Technical AI Knowledge | "My agent kept hearing the loudest voice in the room." | HDBSCAN cluster-and-sample · depth-gate with logged reject reasons |
| 4 | LDR fabrication catch | AI Ethics / Safety | "I caught my own agent lying and kept the receipt." | 0 fabricated briefs post-fix · 1 routing rule · specimen retained |
| 5 | Judge Layer | AI Product Strategy | "I stopped saying 'I have agents' and started saying 'I run a control architecture.'" | 8-field ActionProposal · 4 policy rules · $0/decision · fail-open |
| 6 | The Block cross-functional | Cross-Functional Collaboration | "I kept delivery legible while the org turned over around me." | [CONFIRM metric] · Jira ticket standard · biweekly P&E update |
| 7 | Substack-Drafter cost tradeoff | Trade-off swing | "Local model first, cloud only on fallback — ten cents a run." | ~$0–0.10/run (cap $0.10) · local-first routing · 0 autonomous publishes |

---

## Story 1 — "I shipped the scorecard at 1 out of 10 on purpose"
**Category: AI Product Experience · eval design**

- **S:** My nightly knowledge-synthesizer agent silently regressed for about nine days — quietly producing near-empty output while every dashboard stayed green.
- **T:** As the person accountable for that agent, I had to build the measurement layer that should have existed *and* be honest about how bad it was.
- **A:**
  - Started with **error analysis on 17 days of real production logs** — I derived the failure taxonomy from actual stderr, not from cases I imagined.
  - That produced a **6-mode failure taxonomy**, which became a **10-case eval suite**.
  - I **shipped it intentionally red — a 1-out-of-10 baseline** — because a green eval suite on day one is a lie; I wanted an honest floor to climb from.
  - Fixed the failures in public, one mode at a time.
- **R:** The silent regression became visible and gated. No synthesizer change ships now without passing the suite.
- **M (say it):** **"Ten cases, six failure modes, one out of ten to seven out of ten — and the taxonomy came from seventeen days of real logs, not my imagination."**
- **Arc layer:** This is the discipline the orgs I evangelized to never built. I built it for myself.
- **Weakness-flip cue:** the nine-day silent regression is the failure — own it in one sentence, then pivot hard to "so I built the thing that makes silent failures loud."

---

## Story 2 — "Karpathy said ship MCP servers, so I did — 13 days early"
**Category: AI Product Experience · AI Product Strategy**

- **S:** Andrej Karpathy's single top recommendation for 2026 was verbatim "stop building skills and start building MCP servers." I had 118 skills and zero portable, installable artifacts.
- **T:** Ship a real, installable MCP server that publishes my specification-engineering thesis — not a toy.
- **A:**
  - Built **`intent-engineering`** — three tools (audit a spec, scaffold a spec, retrofit an existing one), pinned SDK, MIT license.
  - Published to **npm and the public MCP registry**, DNS-verified, **13 days ahead of my own ship date**.
  - **Dogfooded it on my own 118 skills** — the audit tool found real anti-patterns in my own work, and I folded the results back into the README instead of hiding them.
- **R:** First concrete, installable instance of my thesis; I can hand an interviewer a one-line install and demo it live in Claude Desktop.
- **M (say it):** **"Three tools, live on npm and the MCP registry, twenty-three out of twenty-five on its own dogfood audit, shipped thirteen days early."**
- **Arc layer:** This is the artifact that turns "I'm interested in agents" into "here's one you can install right now."
- **Memorability anchor:** the dogfood result — "I pointed my own quality tool at my own work and published the score."

---

## Story 3 — "My agent kept hearing the loudest voice in the room"
**Category: Technical AI Knowledge**

> This is the story that defuses the "F1 score" trap — the moment an interviewer probes whether you actually understand the ML, or just the vocabulary. Name the architecture out loud.

- **S:** My synthesizer kept surfacing the same few loud topics every night and missing the quieter, often more interesting ones.
- **T:** Diagnose the *why* at the retrieval layer, not patch the symptom at the output.
- **A:**
  - Diagnosed it as a **retrieval-diversity failure**: naive top-k similarity over-samples dense clusters in the embedding space — the loud topics are dense, so they win every time.
  - Replaced it with **HDBSCAN cluster-and-sample** — cluster the embedding space first, then sample *across* clusters instead of by raw similarity.
  - Added an **`evaluate_article_depth()` gate** that rejects shallow inputs and logs an explicit `rejected_reasons` so the filtering is auditable, not a black box.
- **R:** Cross-domain coverage improved; the synthesizer stopped echoing the densest cluster.
- **M (say it):** **"I swapped naive top-k for HDBSCAN cluster-and-sample, and added a depth-gate that logs why it rejected each input — so the retrieval is diverse *and* auditable."**
- **Arc layer:** I'm a PM who can name the clustering algorithm and defend the sampling tradeoff — that's the bridge from creative to technical PM.
- **Confidence cue:** say "embeddings," "top-k," "HDBSCAN," "cluster-and-sample" without hedging. If you can't yet, that's the Task 18 vocab drill, not this story.

---

## Story 4 — "I caught my own agent lying and kept the receipt"
**Category: AI Ethics / Safety**

- **S:** My local deep-research agent returned a polished, confident research brief that was substantially fabricated — invented software libraries, fake Microsoft documentation URLs.
- **T:** Decide whether local research could be trusted for real decisions, and if not, build the guardrail before it cost me.
- **A:**
  - Diagnosed the root cause as **citation-grounding collapse** — a 14-billion-parameter model can't ground citations across three-plus targets at once, so it invents entities that *sound* right.
  - Wrote a **routing rule**: any research compounding three or more independent investigations goes to grounded cloud research, never the local model.
  - **Kept the bad output as a labeled specimen** — fabrications preserved and annotated — instead of deleting the evidence. It's now a permanent regression fixture.
- **R:** Zero fabricated-citation briefs reached a decision after the rule. The specimen seeds my eval suite and a planned public post-mortem.
- **M (say it):** **"Zero bad briefs got through after the fix, one routing rule, and I kept the lying output as an annotated fixture instead of deleting the evidence."**
- **Arc layer:** Safety isn't a slide for me — I found the failure in my own system and engineered around it.
- **Information-control cue:** this is a *strength* story (you caught it), not a confession. Don't over-apologize for the agent — you're the one who caught it.

---

## Story 5 — "I stopped saying 'I have agents' and started saying 'I run a control architecture'"
**Category: AI Product Strategy** — *the flagship; this is the one to make them remember*

- **S:** One of my autonomous agents drafts public writing. In principle it could fabricate a quote and attribute it to a real, ex-employer person — a reputational live wire.
- **T:** Put a control surface between the agent's *intent* and any *action* — without rebuilding the agent.
- **A:**
  - Designed an **`ActionProposal` schema**: before acting, the agent must declare intent in eight typed fields — intended action, target surface, authorization basis, expected consequence, exposure level, whether human review is required.
  - A **declarative YAML policy** (four rules, each traceable to a real incident) is evaluated by a local model at **$0 per decision**; outcomes are ALLOW, BLOCK, REVISE, ESCALATE, or JUDGE-UNAVAILABLE.
  - Chose **intercept, don't rebuild** — wrapped the one finished agent rather than retrofitting all eight — and made it **fail-open** with an alert and a ledger entry, because my manual publish gate stays the canonical control. The judge is defense-in-depth, not the only reviewer.
- **R:** It reframed my entire fleet from "agents with cost limits" to "actors inside a control architecture" — which is the exact language in the Anthropic Forward-Deployed JD I'm targeting.
- **M (say it):** **"Eight-field intent schema, four policy rules, zero dollars per decision, and a fail-open guarantee — the evaluate function never raises, so an outage degrades safely instead of silently."**
- **Arc layer:** This is the vocabulary upgrade that moves a hobbyist's agent fleet into enterprise-PM territory.
- **Memorability anchor:** "intercept, don't rebuild" — and "the judge fails *open*, on purpose, because the human is still the real gate."

---

## Story 6 — "I kept delivery legible while the org turned over around me"
**Category: Cross-Functional Collaboration** — *the one story set inside a real company*

> ⚠️ This story needs a defensible metric before you use it in a room. The structure is right; the number is [CONFIRM]. Pull a real one: ETF pages shipped, ticket cycle-time, or update-cadence reliability.

- **S:** At The Block I owned PM workflows across the `.Co` and Campus products while the Product & Engineering org went through real leadership turnover — a departing CPO, an incoming CEO.
- **T:** Keep cross-functional delivery — engineering, design, content — moving and legible during the instability.
- **A:**
  - Standardized **Jira ticketing** into Epics / Design Stories / Implementation Stories so eng and design shared one definition of ready and done.
  - Owned the **biweekly Product & Engineering status update** — the comprehension surface that kept teams aligned when the leadership layer was shifting.
  - Built a repeatable **ETF page-creation workflow** spanning content, data, and publishing — so a recurring deliverable didn't depend on me being in the room.
- **R:** Cross-functional delivery stayed legible through the turnover; the templates were clean enough that I retained them as portfolio reference.
- **M (say it):** **"[CONFIRM — e.g. 'I shipped N ETF pages on a repeatable workflow and ran the P&E update on a reliable biweekly cadence through three months of leadership change.']"**
- **Arc layer:** Even before I built my own AI stack, my instinct was to make work *legible and repeatable* — the same instinct that later produced the eval suite and the judge layer.
- **Weakness-flip cue:** if asked about the layoff here, one factual sentence (cost-cutting, not performance), then pivot to what the reset produced. Don't dwell. (Full handling lives in the TMAY's per-company file.)

---

## Story 7 — "Local model first, cloud only on fallback — ten cents a run"
**Category: Trade-off swing** — *best answer for "tell me about a cost or latency tradeoff"*

> This story exists to convert your one flagged skill gap — cost/token economics — into evidence. Use it when an interviewer asks about tradeoffs, constraints, or "how do you keep AI spend sane."

- **S:** I wanted an agent that drafts public writing every week without ever publishing on its own and without quietly running up a model bill.
- **T:** Build it cheap, safe, and voice-consistent — three constraints that usually fight each other.
- **A:**
  - Built a **HybridRouter**: a local 14B model runs first, and a cloud model is only called on fallback — so the default path is free and the paid path is the exception.
  - Capped spend at **ten cents a run** and instrumented it so the cost is visible, not assumed.
  - Hard-wired **"agents draft, I send"** — no autonomous publish, ever — which later became the boundary my Judge Layer made executable.
- **R:** A working build-in-public engine that respects the wallet, the voice, and the boundary at once.
- **M (say it):** **"Local-first routing, capped at ten cents a run, zero autonomous publishes — I treated cost as a designed constraint, not an afterthought."**
- **Arc layer:** Cost discipline was the one skill the market told me I was light on, so I made it a feature of how I build.
- **Memorability anchor:** "the free path is the default, the paid path is the exception."

---

## Drill protocol (Task 16 Step 5)

1. **Read each bold M-line aloud first** — those are the load-bearing sentences; everything else is scaffolding.
2. **Time each story.** Target 2:00–2:30. Over 2:30 = cut a bullet. Under 1:30 = you dropped the Action detail that proves it.
3. **Three rounds:** round 1 read it, round 2 glance-and-tell, round 3 cold. Story 1 cold without notes is the verification gate.
4. **Then run them through the rig.** Once the Task 19 mock-interview grader is live, record each and grade against the 8 dimensions; iterate any dimension below 8.

## Open items before these are interview-ready

- ⚠️ **Story 6 metric** — pull one real, defensible number from The Block work. This is the only story with a placeholder.
- ⚠️ **NYL specifics** — confirm title/years/scope so the evangelist arc (and the TMAY) rests on facts you can defend under follow-up.
- 🔲 **Council grading** — gated on the Task 19 rig (mock-interview infrastructure); run once it's live.
