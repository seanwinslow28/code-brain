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
| 11 | `1ab0974b` | Google PAIR — Data Collection + Evaluation | web | B | M2 | 2026-08-17 |
| 12 | `9ac74ee9` | Gebru et al., *Datasheets for Datasets* (arXiv 1803.09010, **PDF**) | web | A | M2 | 2026-08-17 |
| 13 | `dbb721bc` | *A Systematic Taxonomy of Failure Modes in RAG Systems* (ACL TrustNLP 2026, **PDF**) | web | A | M2/M3 | 2026-08-17 |
| 14 | `d269db15` | *Exploring the Role of AI in the Closure of Zillow Offers* (JISE 2024, **PDF**) | web | A | M2 | 2026-08-17 |
| 15 | `5b756d4b` | M2 — Lesson: Data, Feedback & the Model Path | file | — | M2 | 2026-08-17 |
| 16 | `8641160f` | Anthropic — *Building Effective Agents* | web | B | M3 | 2026-08-22 |
| 17 | `ce870d74` | Sculley et al., *Hidden Technical Debt in ML Systems* (NeurIPS 2015, **PDF**) | web | A | M3/M5 | 2026-08-22 |
| 18 | `a06dd429` | Microsoft — *Taxonomy of Failure Modes in Agentic AI Systems v2.0* (**PDF**) | web | B | M3 | 2026-08-22 |
| 19 | `37b21bfc` | M3 — Lesson: Architecture Under Constraints | file | — | M3 | 2026-08-22 |
| 20 | `a7548548` | Amershi et al., *Guidelines for Human-AI Interaction* (CHI 2019, **PDF**) | web | A | M4 | 2026-08-22 |
| 21 | `d98b596c` | Google PAIR — *Errors + Graceful Failure* | web | B | M4 | 2026-08-22 |
| 22 | `ff6fd6a9` | Google PAIR — *Explainability + Trust* | web | B | M4 | 2026-08-22 |
| 23 | `230a9929` | Intercom — *Fin AI Agent outcomes* | web | B | M4 | 2026-08-22 |
| 24 | `8fa09511` | Zhang, Liao & Bellamy, *Effect of Confidence and Explanation on Accuracy and Trust Calibration* (FAT\* 2020, **PDF**) | web | A | M4 | 2026-08-22 |
| 25 | `7a8e6894` | M4 — Lesson: Interaction, Trust & Control | file | — | M4 | 2026-08-22 |
| 26 | `bc1cf6c0` | Hamel Husain — *Your AI Product Needs Evals* | web | B | M5 | 2026-08-24 |
| 27 | `4301f4c3` | Hamel Husain — *Using LLM-as-a-Judge For Evaluation* | web | B | M5 | 2026-08-24 |
| 28 | `af5b612b` | Breck et al., *The ML Test Score* (IEEE Big Data 2017, **PDF**) | web | A | M5 | 2026-08-24 |
| 29 | `1dfcc9f0` | *A Survey on LLM-as-a-Judge* (arXiv 2411.15594, revised through 2026, **PDF**) | web | A | M5 | 2026-08-24 |
| 30 | `0d1f0ebd` | ICONIQ — *2026 State of AI: Bi-Annual Snapshot* (**PDF**) | web | C | M5 | 2026-08-24 |
| 31 | `f7b99e57` | M5 — Lesson: Evidence & Operations | file | — | M5 | 2026-08-24 |

**Count: 31.** Sculley (`ce870d74`) is shared M3/M5 and is included in M5's `-s` selection without being re-added.

## Fetch-quality rule — learned the hard way, 2026-08-17

**A source that was added successfully is not a source that contains anything.** Verify substance before building on it:

```bash
notebooklm source fulltext <id> --notebook <nb> --json | python3 -c "…"   # count topic keywords
```

Three failures caught this way in one sitting, all of which would have silently degraded a module:

1. **`pair.withgoogle.com/guidebook/chapters/data-collection` redirected to the guidebook homepage** and imported 11,456 characters of site navigation under the title "People + AI Guidebook - Home." Zero hits on *label*, *bias*, *training data*. The working URL is the pre-generative edition at `/guidebook-v2/chapters/data-collection/` — 54,761 chars, *label* ×102. The current guidebook reorganised that chapter into "Data + Model Evolution."
2. **arXiv and ACL Anthology landing pages import the abstract, not the paper.** The RAG taxonomy landing page had zero hits on *chunking* — one of its own 33 failure modes. Both were re-added as `/pdf/` URLs: 56,696 and 48,199 chars respectively, with the real content.
3. Terminal-rendered `source fulltext` output is truncated. **Use `--json` and parse from the first `{`** or you will measure the renderer instead of the source.

**Two more, learned 2026-08-22 while sourcing M4:**

4. **The PAIR guidebook's canonical chapter path is singular — `/guidebook-v2/chapter/<slug>/`, not `/chapters/`** — and the Errors chapter's slug is **`errors-failing`**, not the guessable `errors-graceful-failure`, which 404s. Both `/chapter/` and `/chapters/` resolve for *some* slugs, which is how the plural form got into the M1/M2 notes. Pull the nav links off any working chapter page rather than guessing: `curl -sL <chapter-url> | grep -oE 'href="[^"]*"'`.
5. **`curl` 403 is not the CLI's verdict.** `microsoft.com/en-us/research/wp-content/uploads/.../Guidelines-for-Human-AI-Interaction-camera-ready.pdf` refuses `curl` with a 403 under any user-agent, and imported cleanly through `notebooklm source add` — 92,269 characters, the full paper. Probe with curl to *find* URLs, but let the CLI make the final call, then verify content the usual way.

**One more, 2026-08-24 while sourcing M5:** a source's imported **title can differ from what the URL slug implies**, because the page was renamed after publication. `hamel.dev/blog/posts/llm-judge/` imports as *"Using LLM-as-a-Judge For Evaluation: A Complete Guide"* — the piece was retitled from the "Creating a LLM-as-a-Judge That Drives Business Results" name the curriculum map recorded. Cite the title the page currently carries, not the one in an older note.

Also note: PDFs import with the URL as their title. Cosmetic, but it means `source list` alone can't tell you what a source is.

## Sources verified but rejected

| Source | Why rejected |
|---|---|
| Reuters (Dastin, 10 Oct 2018) — the Amazon primary | Blocks automated fetching, twice (`RPCError rpc_code=9`). Irish Times syndication and NC State's Data Ethics Repository also refused. Built In carries the same facts and is used instead, labelled as a retelling |
| `pair.withgoogle.com/guidebook/chapters/data-collection` | Redirects to homepage — see above |
| arXiv / ACL **abstract** pages | Landing pages, not papers — see above |

## Provenance notes

- **#9 is a retelling, not the primary.** The primary is Reuters, Jeffrey Dastin, 10 Oct 2018, which blocks automated fetching (tried twice, `RPCError rpc_code=9`); the Irish Times syndication and NC State's Data Ethics Repository also refused. Built In carries the same facts. **The M1 lesson states explicitly that the account is single-sourced, that Amazon disputed the tool was ever used to evaluate candidates, and that details are not independently verifiable** — treat as illustrative, never as a load-bearing citation.
- **#1 is the Google AI Search seed doc Sean supplied.** Unverified claims and citations; kept as the program's origin artifact and starting scaffold, superseded by the researched map. Do **not** cite it as evidence.
- **#3 and #6** are interview-prep and tutorial content — tier C by construction. The whole "what interviews assess" evidence base is weak (see curriculum-map.md § Sources); treat as hypothesis.

## Sources verified but NOT added

Held for their own modules, or held deliberately:

| Source | Tier | Held for |
|---|---|---|
| Sculley et al., *Hidden Technical Debt in ML Systems*, NeurIPS 2015 | A | M3 / M5 |
| *A Systematic Taxonomy of Failure Modes in RAG Systems*, ACL TrustNLP 2026 | A | M2 / M3 |
| Microsoft, *Taxonomy of Failure Modes in Agentic AI Systems v2.0*, June 2026 | B | M3 |
| Amershi et al., *Software Engineering for ML: A Case Study*, ICSE 2019 | A | M2 |
| Nate B Jones — "Your Agent Is 80% Plumbing" (12 primitives) | B | M3 |
| Nate B Jones — the Moat Audit (12 questions) | C | **Considered for M5 on 2026-08-24 and SKIPPED as off-spine.** It sits inside a Dec-2025 "9 bets for 2026" post and is about competitive positioning, not evidence or operations. Fetched and read via the Executive Circle MCP (post `de715ba3-14b2-4a90-8279-2ef06ad78507`); nothing in it displaced a source that teaches measurement, rollout, cost or ownership |
| Nate B Jones + Ryan Wilson — "Stop Designing AI Chatbots, Start Designing AI Relationships" | C | **M4 — used, but deliberately NOT imported.** The 5×5 pairings grid and the three relational metrics are extracted into the M4 lesson with tier-C provenance stated inline; the "Reflexive Intelligence" coinage is left behind. Fetched via the Executive Circle MCP, post `b87d7b60-b804-482a-b502-0e07c2deeb1b` |
| ASTRIDE (arXiv 2512.04785) / STRIDE-AI (arXiv 2605.17163) | A | M3 — **teach STRIDE plus the agentic threat categories; ASTRIDE is a platform paper and the area is unsettled** |
| Hydari, Iqbal & Ramasubbu, *Stochastic Tax* (arXiv 2605.27320) | A | M1 (cited) / M5 — fresh preprint, date it when spoken |
| The two Gemini DR reports (2026-08-17) | mixed | Program reference; **DR §4 on interview assessment is vendor SEO — hypothesis only** |
