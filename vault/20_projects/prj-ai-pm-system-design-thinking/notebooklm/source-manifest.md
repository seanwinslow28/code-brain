# NotebookLM Source Manifest

Notebook: `bcb4e6aa-9da7-49fe-8c65-46d27110313e` — "System Design Thinking for AI PM"

**Policy (from curriculum-map.md, non-negotiable):**
- **3–5 hand-vetted sources per module.** Never 8–12. The retired notebook took 83 sources in one bulk deep-research import and graded 17% A / 60% C / 20% D — that is the pathology this rule exists to prevent.
- **No bulk research imports, ever.** Every source is added individually and tier-labeled before entry.
- Naming: `M<N> —` for module sources, `P0 —` for program-level.
- Generation always uses `-s` source selection. Never whole-notebook.

**Tier key:** **A** peer-reviewed · **B** primary (vendor engineering doc, primary reporting, official spec) · **C** trade/industry · **D** forum/UGC

| # | Source ID | Title | Kind | Tier | Module | Added |
|---|-----------|-------|------|------|--------|-------|
| 1 | `9f12099b` | AI-PM-system-design-thinking.md (Google AI Search seed) | file | D | P0 | 2026-08-17 |
| 2 | `7c0d4b72` | If you're building with AI, watch this (System Design Overview) | YouTube | C | M3 | 2026-08-17 |
| 3 | `71a69988` | Inside Product Interviews: How to Ace System Design Rounds | YouTube | C | P0 | 2026-08-17 |
| 4 | `a8d8faac` | System Design for Product Managers: How AI Changes Everything | YouTube | C | M3 | 2026-08-17 |
| 5 | `9d283700` | When to Build Your Own Agent Harness — Harrison Chase, LangChain | YouTube | B | M3 | 2026-08-17 |
| 6 | `b7828d5e` | You Can Learn AI Agent System Design In 19 Min (RAG, Vector DB, Evals, Function Calling) | YouTube | C | M3 | 2026-08-17 |
| 7 | `bb367054` | Google PAIR — People + AI Guidebook: User Needs + Defining Success | web | B | M1 | 2026-08-17 |
| 8 | `f0988a1f` | Google ML Crash Course — Thresholds and the confusion matrix | web | B | M1 | 2026-08-17 |
| 9 | `66c038cd` | Amazon abandons AI hiring tool exposed for gender bias (Built In) | web | C | M1 | 2026-08-17 |
| 10 | `2251b249` | M1 — Lesson: Problem, Users & Decision Economics | file | — | M1 | 2026-08-17 |

**Count: 10.**

## Provenance notes

- **#9 is a retelling, not the primary.** The primary is Reuters, Jeffrey Dastin, 10 Oct 2018, which blocks automated fetching (tried twice, `RPCError rpc_code=9`); the Irish Times syndication and NC State's Data Ethics Repository also refused. Built In carries the same facts. **The M1 lesson states explicitly that the account is single-sourced, that Amazon disputed the tool was ever used to evaluate candidates, and that details are not independently verifiable** — treat as illustrative, never as a load-bearing citation.
- **#1 is the Google AI Search seed doc Sean supplied.** Unverified claims and citations; kept as the program's origin artifact and starting scaffold, superseded by the researched map. Do **not** cite it as evidence.
- **#3 and #6** are interview-prep and tutorial content — tier C by construction. The whole "what interviews assess" evidence base is weak (see curriculum-map.md § Sources); treat as hypothesis.

## Sources verified but NOT added

Held for their own modules, or held deliberately:

| Source | Tier | Held for |
|---|---|---|
| Amershi et al., *Guidelines for Human-AI Interaction*, CHI 2019 | A | M4 |
| Sculley et al., *Hidden Technical Debt in ML Systems*, NeurIPS 2015 | A | M3 / M5 |
| *A Systematic Taxonomy of Failure Modes in RAG Systems*, ACL TrustNLP 2026 | A | M2 / M3 |
| Microsoft, *Taxonomy of Failure Modes in Agentic AI Systems v2.0*, June 2026 | B | M3 |
| Amershi et al., *Software Engineering for ML: A Case Study*, ICSE 2019 | A | M2 |
| Nate B Jones — "Your Agent Is 80% Plumbing" (12 primitives) | B | M3 |
| Nate B Jones — the Moat Audit (12 questions) | B | M3 / M5 |
| Nate B Jones + Ryan Wilson — "Stop Designing AI Chatbots, Start Designing AI Relationships" | C | M4 — **take the 5×5 pairings grid and the three relational metrics; leave the Reflexive Intelligence framing, which is coinage and ChatGPT-assisted by disclosure** |
| ASTRIDE (arXiv 2512.04785) / STRIDE-AI (arXiv 2605.17163) | A | M3 — **teach STRIDE plus the agentic threat categories; ASTRIDE is a platform paper and the area is unsettled** |
| Hydari, Iqbal & Ramasubbu, *Stochastic Tax* (arXiv 2605.27320) | A | M1 (cited) / M5 — fresh preprint, date it when spoken |
| The two Gemini DR reports (2026-08-17) | mixed | Program reference; **DR §4 on interview assessment is vendor SEO — hypothesis only** |
