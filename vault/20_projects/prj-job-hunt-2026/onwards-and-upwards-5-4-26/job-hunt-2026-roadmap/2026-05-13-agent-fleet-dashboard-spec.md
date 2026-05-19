---
type: spec
project: prj-job-hunt-2026
created: 2026-05-13
status: research-complete
superseded_by: "[[2026-05-15-agent-fleet-dashboard-design]]"
artifact_target: supporting artifact #3 (closes the cost-economics gap + serves as Agent Ops resume evidence)
ships: 2026-05-29 to 2026-06-08 (per locked design doc)
linked_artifacts:
  - "[[2026-05-06-unified-roadmap]]"
  - "[[vault-synthesizer eval suite]]"
  - "[[knowledge_loop]]"
  - "[[2026-05-15-agent-fleet-dashboard-design]]"
linked_research:
  - "[[2026-05-07-target-role-specs]]"
  - "[[2026-05-14-Agent-Fleet-Observability-Dashboard-ChatGPT]]"
  - "[[2026-05-14-Agent-Fleet-Observability-Dashboard-Gemini-DR]]"
ai-context: "Original build spec + deep-research prompt scaffolding for the Agent Fleet Observability Dashboard. Research returned 2026-05-14 from both Gemini DR and ChatGPT DR. Brainstorming session 2026-05-15 synthesized the two returns + locked all open questions. Locked design lives at [[2026-05-15-agent-fleet-dashboard-design]] — that doc is the implementation-ready source of truth, not this one. This spec retained for historical context + audit trail."
---

# Agent Fleet Observability Dashboard — Build Spec + Research Prompt

> **Status: research-pending.** No code is written until deep research returns with distribution-surface + comparison-study validation. This document IS the research input.

---

## 1. Executive Summary

The Agent Fleet Observability Dashboard is a proposed single-surface read-only visualization of Sean's 8-active-agent fleet (Vault Indexer, Vault Synthesizer, Deep Researcher, Meta-Agent, Daily Driver, Knowledge Lint, Flush, Job Feed) plus telemetry from the synthesizer manifests, Gemini DR spend tracker, Sunday lint reports, eval suite results, and job-feed SQLite DB.

The dashboard turns Sean's existing instrumentation (CSV, JSON, SQLite, markdown reports) into recruiter-readable evidence that he runs a real production fleet with real costs, real failure modes, and real telemetry — not weekend projects.

Distribution-surface decision is the load-bearing open question: static HTML on Vercel vs. Astro page on personal site vs. Cowork artifact vs. GitHub Pages. Each has different recruiter-discovery dynamics and different infrastructure burdens. Deep research must surface the right choice.

The narrative anchor: the dashboard surfaces — visually and unambiguously — the 9-day silent regression that the Substack post 1 ("The Night My Vault Said Nothing") describes. Reader hits the dashboard, sees the drop, sees the recovery, sees the eval-suite catch. The dashboard is the visual hero of Substack post 2 and the resume evidence for the Agent Ops / FDP track.

Expected build time: 2–3 working days post-research. Expected ship: 2026-06-08 to 2026-06-15 depending on distribution-surface choice.

---

## 2. Why This Is Necessary

Six reasons, ordered by load-bearing strength.

**Reason A — The Agent Ops / FDP backup track needs visible operational evidence. (STRONG)**
ChatGPT-Nate-1's primary backup-track recommendation is Agent Ops / Forward Deployed Product / Support Ops AI. The Anthropic FDE Boston listing literally asks for "MCP servers, sub-agents, and agent skills" deliverables, but the *operational* signal is implicit: do you know what it takes to keep agents running in production? Without a dashboard, Sean's claim "I run 8 production agents" rests on the agents themselves being inspectable — recruiters won't clone the repo, won't read the launchd plists, won't grep the CSV log. The dashboard converts that claim from "trust me, look at the repo" to "look at this screen for 30 seconds."

**Reason B — Karpathy's $20B 2026 funding flow says this market is real. (STRONG)**
The Karpathy synthesis explicitly names evals + agent-ops platforms as a $20B 2026 capital-deployment vector. Sean can't compete with Helicone / Braintrust / Langfuse / LangSmith on building one, but he *can* demonstrate fluency by building a one-page static version that uses the same telemetry primitives. The dashboard is the artifact that says "I understand the agent-ops category at the level of someone who would use these tools, not just hear about them."

**Reason C — Closes the cost-economics gap, the single weakest skill. (MEDIUM-STRONG)**
Both Nate-1 docs (Claude + GPT) name cost economics as Sean's one beginner skill on the seven-skills map. The dashboard surfaces real spend across the fleet: Gemini DR per-task + per-month spend (already JSON-instrumented at `vault/health/gemini-spend-{YYYY-MM}.json`), Anthropic API spend (via Daily Driver tracking), local-model implied amortization (electricity + hardware over the 17-day workload). This is fluency demonstrated by lived experience, not by a separately-built calculator.

**Reason D — Pairs with Substack post 2 as visual hero. (MEDIUM-STRONG)**
Substack post 1 (ships Friday 2026-05-22) tells the story of the 9-day silent regression that the eval suite caught. Substack post 2 (Friday 2026-05-29) is the follow-up — "Vault said something again." The dashboard provides the *visual* of the regression-to-recovery arc: synthesizer `concepts_written` flatlined for 9 nights, eval-suite count drops from 7/10 to 1/10, fix lands, both recover. That visual is far more shareable on LinkedIn than the eval-suite repo itself.

**Reason E — Two purposes, one surface (operational efficiency). (MEDIUM)**
Sean already needs a job-hunt tracker view ([[target-companies]] + [[warm-intros]] + [[job_feed]]). The dashboard can absorb that as a second tab — application velocity, target-30 status counts, warm-intro pipeline. Building one surface for two purposes is more credible than building two surfaces. The pattern: "I built one observation surface that serves both my fleet ops and my job hunt; the same primitives generalize" — which is itself the agent-PM thesis.

**Reason F — Recursive validation of the artifact stack. (WEAK-MEDIUM)**
The dashboard surfaces the eval-suite pass count, which catches the regression that the eval-suite was built to catch, in the producer pipeline that the Phase 6 EXPLANATION.md describes, which uses the typed-edges schema that the Phase D EXPLANATION.md describes, all of which can be queried via the second MCP (`vault-knowledge-mcp`). Five flagship artifacts collapse into a single observable surface. The dashboard isn't an addition to the portfolio — it's the demo of the portfolio.

---

## 3. How It Would Work (v0 Best-Guess Architecture)

### 3a. Panels

| Panel | Visualization | Data source | Refresh cadence |
|---|---|---|---|
| **Fleet Health** (top, 8-tile grid) | Per agent: last run timestamp, status (✓/✗/⊘), last cost, last duration | `vault/90_system/agent-logs/agent-run-history.csv` (filtered to last 24h per agent) | Page load |
| **Cost Trends** | Stacked area chart, last 30 days, color per agent | `agent-run-history.csv` aggregated by agent + day | Page load |
| **Model Mix** | Donut chart, local vs cloud %, segmented by family | `agent-run-history.csv` `model_used` column | Page load |
| **Synthesizer Telemetry** | Line chart with two series (concepts_written, connections_written), last 60 nights | `vault/health/synth-manifest-*.json` | Page load |
| **Eval Suite Status** | Single number + sparkline (7/10, last 14 days) | `evals/vault-synthesizer/last-run.md` frontmatter | Page load |
| **Recent Runs Table** | Sortable, last 50 rows | `agent-run-history.csv` tail | Page load |
| **Job Hunt Overlay** (tab 2, optional) | Application velocity sparkline + target-30 status pie + warm-intro pipeline | `target-companies.md` parsing + `vault/.job-feed.db` | Page load |
| **Annotation Layer** | A pinned callout on the Synthesizer Telemetry timeline pointing at the 2026-05-01 → 2026-05-10 regression window with link to the Substack post | Hardcoded | Static |

### 3b. Tech Stack (v0 default — open for research challenge)

- **Output:** Single HTML file (< 50 KB pre-data), no build step
- **Visualization:** Chart.js (allowed by Cowork artifact rules) for trend charts; Grid.js for the runs table; inline SVG for the fleet-health tile grid
- **Data loading:** **Open question for research** — see §6 Q1
- **Distribution surface:** **Open question for research** — see §6 Q2
- **Anonymization:** **Open question for research** — see §6 Q3
- **Theme:** Light mode primary, dark mode toggle, matches `[[sw-ai-pm-portfolio]]` V3 Teal/Amber tokens
- **Typography:** Sora (headings) + Inter (body) + JetBrains Mono (numbers)
- **Accessibility:** WCAG 2.1 AA — see `[[sw-ai-pm-portfolio/DESIGN-SPEC-V4]]` standards Sean already enforces

### 3c. The Narrative Annotation (load-bearing)

The Synthesizer Telemetry panel has a single hardcoded annotation: a pinned marker on the 2026-05-01 to 2026-05-10 window labeled "9-day silent regression — caught by eval suite 2026-05-10." Hovering the marker reveals: "Synthesizer wrote 0 concepts for 9 consecutive nights. The vault-synthesizer eval suite caught it on 2026-05-10. Read the story → [Substack post link]." This annotation is the difference between "a generic agent dashboard" and "an interview-grade artifact telling a specific true story."

### 3d. Empty-State Behavior

If a data source is empty or unavailable, the panel renders a calm explainer ("No synthesizer runs in the last 30 days — this agent runs nightly at 02:30 only when the MBP is awake; see [[knowledge_loop]] for details"). No spinners. No "loading..." that lasts more than 200ms. Every panel is content-or-explanation, never indeterminate.

### 3e. Privacy Surface

If the dashboard is public, what's stripped: actual dollar amounts in Cost Trends (replace with relative % bars), actual agent run IDs that include vault content (replace with run ordinals), the entire Job Hunt Overlay tab (this is locked behind a `?private=1` query param or a separate file). The dashboard must be safe to share with a recruiter cold without leaking job-search status or financial detail.

---

## 4. How This Complements the Existing 7 Flagships + Supporting Artifacts

| Flagship / Supporting | What it is | What the dashboard adds |
|---|---|---|
| `intent-engineering` MCP | Skill-wrapping MCP | None directly; the dashboard doesn't surface MCP usage |
| Phase D typed edges | Knowledge graph infra | Visualizes synthesizer's edge-write count over time |
| Phase 6 knowledge loop | Producer/consumer pipeline | Visualizes the producer side (synthesizer manifest telemetry) |
| Financial-research fleet | Multi-agent retrieval | Shows up as an agent tile + cost contributor (when sanitized version ships) |
| Animation pipeline | 6/11 short film | Independent, not visualized |
| Vault Synthesizer Eval Suite | 10-case binary pass/fail | Shows pass count + sparkline directly |
| Substack-Drafter Agent | Voice-rotation weekly draft | Shows up as an agent tile (when activated post-B7) |
| `vault-knowledge-mcp` (Task 10) | Knowledge-graph MCP | Could surface MCP call telemetry if logged; v0 doesn't depend on this |
| Token Cost Calculator (Task 5 Step 3) | Single-file HTML calculator | Complementary: calculator is forward-looking design tool; dashboard is backward-looking observation |
| 14-agent fleet Loom (Task 5 Step 1) | 5–7 min unedited screen recording | The dashboard IS the visual the Loom narrates from; pairs tightly |

Net effect: the dashboard ties 5 existing artifacts into one viewable surface and is the natural visual companion to the 14-agent fleet Loom + Substack post 2.

---

## 5. Recruiter / Hiring-Manager Resonance Hypothesis

**The 30-second cold-open we believe lands hardest:**

The recruiter opens the URL. They see a fleet grid (8 tiles, mostly green). They see a cost-trend chart (4 colors, last 30 days, total spend ~$X). They see a synthesizer line chart with a visible dip-and-recovery annotated "9-day silent regression — caught by eval suite." They see an eval suite count of "7/10 passing." They scroll to recent runs (50 rows, sortable). Total visible information: ~10 datapoints they can verify against the linked repos.

The story they read in 30 seconds: "this candidate operates a real fleet, has caught and recovered from a real regression, and has the tooling habit to instrument fleet behavior — not just build agents."

**Why we believe this lands at each tier:**

- **Tier 1 (Anthropic FDE, Glean FDP, HubSpot Voice):** FDE customers want partners who already understand operational maturity. The dashboard is the signal that survives the "candidate has nice demos but no production experience" rejection mode.
- **Tier 2 (Klaviyo, Liberate, Manifold Bio):** B2B SaaS PMs increasingly own AI-feature observability. The dashboard demonstrates the candidate knows what observability looks like before they're asked to design it.
- **Tier 3 (Sierra, Decagon):** Agent PMs at the frontier need to design agent telemetry as part of the product. The dashboard demonstrates the candidate has done it.

**What the dashboard refutes specifically:**
- "PM with side projects" → "PM with instrumented production fleet"
- "Hand-wavy about cost economics" → "Track of every agent run with model + cost + duration"
- "Says he's run a fleet" → "Public dashboard recruiter can verify"

---

## 6. Open Questions for Deep Research

Ordered by leverage.

**Q1 — Data loading: build-time static vs. fetch-at-load vs. live-poll?**
v0 spec is ambiguous. Three options. (a) Build-time static: a build script runs nightly, embeds the data as JSON in the HTML, no network calls at load. (b) Fetch-at-load: the HTML fetches a hosted JSON file on page load. (c) Live-poll: the HTML re-fetches every N seconds. Tradeoffs: static is fastest + most portable but requires a build step; fetch is slightly slower but always fresh; live-poll is overkill for daily-cadence data. Research target: what pattern do recruiter-visible AI ops dashboards (Helicone, Braintrust, Langfuse, LangSmith, Vercel AI Observability, OpenTelemetry-for-agents references) use for their *public* demo dashboards? Cite at least 3 implementations.

**Q2 — Distribution surface: where does the dashboard actually live?**
Five candidates. (a) Vercel deploy of a static HTML file under `sw-token-cost-calculator`-style repo at `sw-agent-fleet-dashboard`. (b) Astro page on the personal site (deferred — site not yet deployed). (c) Cowork artifact via `mcp__cowork__create_artifact` (lives in chat, refreshes via MCP `callMcpTool`). (d) GitHub Pages from the Superuser Pack repo. (e) Vercel + Astro hybrid where the personal site embeds the same artifact at `/transactions/agent-fleet/`. Research target: which surface maximizes (i) recruiter-discovery from a LinkedIn post, (ii) ability to ship before personal-site deployment closes, (iii) loom-ability for Substack post 2, (iv) longevity (still loading in 12 months without infra babysitting). Cite at least 3 examples of AI-ops dashboards in the wild and their distribution choices.

**Q3 — Anonymization: what stays, what goes, what's behind a query-param gate?**
v0 spec says strip actual cost dollars, replace with %; strip agent run IDs that contain vault content; gate the Job Hunt Overlay tab. But what if the recruiter resonance is *exactly* the dollar amounts ("$2.40 spent in the last 30 days running 8 agents")? Research target: what do published AI ops dashboards reveal vs hide? Is there a "$0.XX/day fleet operating cost" pattern that lands as positive signal, or does revealing cost numbers come across as small-time?

**Q4 — Comparison study: 5–10 published AI ops dashboards to disassemble.**
Find 5–10 published dashboards in the AI ops / LLM observability / agent telemetry category, accessed in May 2026. Candidates to investigate: Helicone public demo, Braintrust dashboard tour, Langfuse demo, LangSmith trace viewer, Vercel AI SDK observability, OpenTelemetry GenAI dashboards, AgentOps.ai public demos, individual builders' personal observability dashboards on Twitter/LinkedIn. For each: URL, the 3 panels that anchor the dashboard, what they got right, what feels generic / bloated. Identify the 1–2 strongest design patterns to copy and the 1–2 weakest to avoid.

**Q5 — Recruiter eye-test: 30 seconds, three panels.**
Take a hiring manager who has 30 seconds and is mid-coffee. What 3 panels do they MUST see in priority order? What single number anchors the whole dashboard at the top of the page? Research target: heuristics for landing-page hierarchy in AI portfolio surfaces — is there a Nielsen Norman Group or similar UX study on candidate-portfolio scanning behavior? Otherwise, cite 3 personal-portfolio sites from the AI PM / FDE community that have gotten attribution in interview reports.

**Q6 — Eval-suite integration shape: pass-count number, sparkline, full case grid, or all three?**
The eval suite has 10 cases with skip-reasons. The dashboard could surface (a) just the pass count "7/10", (b) the pass count + a 14-day sparkline of pass counts, (c) the full case grid (cases × dates, with green/red/yellow cells), (d) all of the above. Tradeoffs: more visual = more recruiter-engaging, but also more recruiter-confusion if they don't know what the cases mean. Research target: what pattern do public eval dashboards (Braintrust, OpenAI Evals public, Anthropic system-card visualizations) use? Cite at least 2.

**Q7 — Substack-post tie-in: hero visual or sidebar?**
The dashboard pairs with Substack post 2 ("Vault said something again"). Should the dashboard BE the hero visual at the top of the post (single screenshot, then text), or is it a sidebar/footer link? Research target: examine 5 Substack posts that successfully drove portfolio engagement (Aakash Gupta's AI PM newsletters, individual builders' "I built X" posts from April–May 2026). Identify the visual-to-text ratio that correlates with high engagement.

**Q8 — Two-purpose-one-surface: should the job-hunt tab actually exist?**
v0 spec floats a Job Hunt Overlay as tab 2. But mixing fleet ops with job-hunt may dilute the agent-ops message OR may strengthen it as "this candidate instruments everything." Research target: are there published examples of multi-purpose personal dashboards that work? Is there a counter-pattern of single-focus dashboards that work better? Decide.

**Q9 — Karpathy frame naming: what does this dashboard CALL itself?**
v0 spec uses "Agent Fleet Observability Dashboard." Candidates: "Agent Ops Dashboard," "Fleet Telemetry," "LLM Cost Dashboard," "Personal AI Operations Console." Naming sets the recruiter's expectation. Research target: what naming convention does the agent-ops vendor category use? Helicone calls itself ___, Braintrust calls itself ___, etc. Pick a name that triggers the right pattern-match.

**Q10 — Substack-as-a-source-of-truth, alternate Substack-friendly graphic format.**
If the dashboard is the visual hero of Substack post 2, the post will be read on mobile, screenshotted into LinkedIn, and embedded in DMs. Does the v0 desktop-first layout work on mobile? Should there be a "screenshot-optimized" view (single column, fewer panels, bigger numbers)? Research target: examine the mobile rendering of the §6 Q4 candidate dashboards; identify whether dashboard creators ship a mobile/screenshot variant.

---

## 7. Anti-Patterns (Things NOT to Build)

- **Real-time WebSocket / 1-second-poll telemetry.** Daily cadence is fine. Real-time adds infra burden for zero signal — Sean's agents run on cron, not on demand.
- **Login / auth.** No. Public read-only or query-param-gated, that's it.
- **Mocked data labeled as real.** Every number must trace to a verifiable file (CSV/JSON/SQLite/MD). The cold-open recruiter must be able to click "view source data" and see the CSV row.
- **Pretty but unverifiable.** A "$47.20 last 30 days" number must come from `agent-run-history.csv` rows, not hardcoded.
- **More than 7 colors in any chart.** Chart-junk anti-pattern. Stick to teal/amber + 4 neutrals.
- **Auto-rotating carousel / hero image.** Recruiter exits in 30 sec; static layout only.
- **Generic "Look at all these tools I use" tile grid.** This isn't a tech-stack list. Every tile must be a *running* agent with telemetry.
- **The Job Hunt Overlay made publicly visible by default.** Active job-search status is private until employed.
- **A claim the data doesn't back.** If `agent-run-history.csv` shows the meta-agent failed 3 times this week, the dashboard shows that. Don't hide it. Recovered failures are the credibility story.

---

## 8. Success Criteria (Binary, Measurable)

| # | Criterion | How verified |
|---|---|---|
| 1 | Single HTML file < 50 KB pre-data | `wc -c index.html` |
| 2 | Loads + renders in < 2 seconds on cold cache | Chrome DevTools Performance audit |
| 3 | All 8 fleet tiles show real data on Sean's machine, none mocked | Visual + `csvkit` cross-reference against `agent-run-history.csv` |
| 4 | 30-day synthesizer telemetry shows the 9-day regression visibly | Visual + annotation present |
| 5 | Mobile rendering survives a single iPhone screenshot at 375px width | Manual phone test |
| 6 | Recruiter cold-open passes the 30-sec test (informally tested with a non-PM friend) | Self-assessment + 2 outside readers |
| 7 | `EXPLANATION.md` 4Q artifact lands in the repo | File exists, <90-sec recruiter readability |
| 8 | 60-sec Loom recording the main panels | Loom URL exists, plays end-to-end clean |
| 9 | Substack post 2 ships with the dashboard as visual hero (Friday 2026-05-29 or following Friday) | Substack post URL exists |
| 10 | At least 1 attributable recruiter engagement attributed to this artifact | Recorded in [[target-companies]] notes column |
| 11 | Privacy boundary holds: no actual cost dollars visible without query param (or, per Q3 research verdict, dollars visible by design) | Manual inspect of public surface |

---

## 9. Time + Cost Estimate

**Time:** 2–3 working days post-research. Day 1: data-loader implementation (assuming research returns "static build-time" as Q1 verdict) + Chart.js panels. Day 2: Grid.js table + annotation layer + responsive layout + accessibility pass. Day 3: distribution-surface ship (Vercel deploy or Cowork artifact, per Q2 verdict) + README + EXPLANATION + Loom. If research returns a more complex distribution-surface choice (Astro hybrid), add 1 day.

**Cost:** $0 cloud. Vercel free tier covers a static page. No API keys exposed; data is local-machine-only.

**Schedule placement:** earliest start Mon 2026-05-26 (after eval suite Loom + Substack post 1 ship 5/22). Ship target 2026-06-08 to 2026-06-15. Slips do not affect Track-C, animation pipeline (6/11), or `vault-knowledge-mcp` (Task 10). Tier-A protected.

---

## 10. Tier-A Check (Operating Model Compliance)

- **Walk-away $100k base:** N/A — portfolio artifact.
- **5-days-in-office no:** N/A — local work.
- **AI > Tech > Creative PM ordering:** ✅ — pure AI-PM artifact, demonstrates Agent Ops backup track.
- **Agents draft / Sean sends:** ✅ — Sean publishes; agents may draft Substack copy.
- **Track-C protected:** ✅ — `intent-engineering` ships; this is downstream supporting work.
- **Friday 4:30 retro:** ✅ — build fits inside 8:30–5:30 deep-work container.
- **5:30 PM hard stop:** ✅ — 2–3 day build does not require evening overflow.

---

## 11. References to Study (Pre-Research Reading List)

- [[2026-05-06-unified-roadmap]] §"Track-C Tier-A protected" + Task 5 (token cost calculator)
- [[Claude-Karpathys-Sequoia-Ascent-2026-Strategic-Synthesis-for-Sean-Winslow]] §"$20B 2026 funding for eval/agent-ops platforms"
- [[2026-05-07-target-role-specs]] §3 Anthropic FDE + §4 Interview Shape by Role Family
- [[knowledge_loop#EXPLANATION]] — the producer side the dashboard visualizes
- [[concept_edges#EXPLANATION]] — the edge-write data the synthesizer telemetry surfaces
- The eval suite at `evals/vault-synthesizer/` — the pass-count source
- [[sw-ai-pm-portfolio/DESIGN-SPEC-V4]] — token / typography / color reference for visual consistency
- Helicone public demo, Braintrust dashboard tour, Langfuse demo, LangSmith trace viewer (URLs to verify in research)

---

## 12. Research Instructions (Paste-Ready Prompt Scaffold)

The following is a paste-ready prompt for Gemini DR-Max (or a Claude deep-research run). Copy from the line below to the end of this document.

---

```
<role>
You are an AI-ops / LLM-observability analyst with deep coverage of the agent-ops vendor category (Helicone, Braintrust, Langfuse, LangSmith, AgentOps.ai, OpenTelemetry GenAI, Vercel AI Observability) and the personal-portfolio AI dashboard scene (individual builders publishing fleet-observability surfaces on Vercel/GitHub Pages April–May 2026). You read source repos, public demo dashboards, and community discussion on the OpenLLMetry / LangSmith / AgentOps GitHub Discussions + LinkedIn. You speak with the precision of someone whose dashboard-design recommendations have shipped to public-demo state.

Your job is to produce a grounded architecture-and-positioning validation document for an Agent Fleet Observability Dashboard that a 33-year-old AI PM is preparing to ship as a supporting portfolio artifact for his job-hunt. The document feeds (a) the distribution-surface decision before code is written, (b) the panel-priority hierarchy for the 30-second recruiter cold-open, and (c) the comparison-study positioning against published AI ops dashboards.
</role>

<context>
**Candidate profile:**
- 2 years titled PM experience, 4–6 years of agentic-engineering portfolio signal
- Operates an 8-active-agent fleet on macOS launchd (local-first, Mac Mini + MBP, mostly $0 cloud)
- Existing instrumentation: `vault/90_system/agent-logs/agent-run-history.csv` (every run), `vault/health/synth-manifest-*.json` (per-night manifests), `vault/health/gemini-spend-*.json` (cloud cost tracking), `evals/vault-synthesizer/last-run.md` (eval pass count), `vault/.job-feed.db` (SQLite)
- Target backup track: Agent Ops / Forward Deployed Product / Support Ops AI per ChatGPT-Nate-1
- One MCP server already published (`intent-engineering`), shipping a second (`vault-knowledge-mcp`) in early June

**The artifact being designed:**
- Name (working): Agent Fleet Observability Dashboard
- Single HTML file (< 50 KB pre-data), Chart.js + Grid.js + inline SVG
- 8 panels: fleet health tiles, cost trends, model mix, synthesizer telemetry, eval suite status, recent runs, optional job-hunt overlay, annotation layer
- One narrative anchor: visible annotation on the 2026-05-01 → 2026-05-10 regression window the eval suite caught
- Distribution surface candidates: Vercel static, Astro page on personal site, Cowork artifact, GitHub Pages
- Build time budget: 2–3 working days post-research
- Cost target: $0 (static + free tier)

**Why this artifact matters:**
- Closes the cost-economics gap, the single weakest skill on the 7-skills map per both Nate-1 docs
- Provides operational evidence for the Agent Ops / FDP backup track
- Pairs with Substack post 2 ("Vault said something again") as visual hero showing the 9-day silent regression and recovery
- Karpathy frame: $20B 2026 funding flows into eval/agent-ops platforms — Sean demonstrates fluency by building a static one-pager that uses the same primitives

**Non-negotiables:**
- Read-only against local data files — no write surface
- Empty-state honesty: panels render explainers, never spinners-that-never-resolve, never mocked data
- Privacy: actual cost dollars + agent content stripped or gated; safe to share cold with a recruiter
- Build fits inside a 5:30 PM hard-stop daily container
- Mobile-readable: survives a single iPhone screenshot at 375px width
</context>

<task>
Produce a 10-section architecture-and-positioning document covering the questions in <output_format>. Multi-source triangulation: every recommendation must cite at least 2 independent reference dashboards (public URL + last-update-date verifiable, screenshot if possible).

The goal is NOT to summarize agent-ops vendor marketing — Sean has read it. The goal is to surface:
- Which distribution surface (Vercel / Astro / Cowork / GH Pages / hybrid) gives the best recruiter-discovery + longevity + ship-speed combination
- Which 3 panels MUST anchor the 30-second cold-open
- What naming convention triggers the right pattern-match against the vendor category
- The 1–2 things in the v0 spec that, if changed before code is written, would have outsized impact on outcome
</task>

<anti_hallucination_guards>
Non-negotiable. Prior research has fabricated dashboard URLs, vendor product names, and "industry conventions."

1. Every cited dashboard must link to a current, reachable public URL OR an archived URL with the archive date stated. If a dashboard is referenced in a blog post but no public URL is findable, mark as "claimed but unverifiable — recommend skip."
2. Vendor product features (e.g., "Braintrust has a trace explorer") must cite the specific product page URL, accessed on YYYY-MM-DD.
3. "Industry convention" claims must cite at least 3 specific dashboard examples that follow the convention. If you can't find 3, mark as "preliminary pattern."
4. Recruiter attribution claims ("this dashboard got X an interview at Y") must cite a public-source URL (LinkedIn post, Substack, HN comment). Paraphrased rumor is forbidden.
5. Substack engagement claims ("this post got 5,000 reads") must cite Substack's public stats page on the post or the author's own claim with URL.
6. Mobile-rendering claims must reference an actual screenshot or device test, not "industry best practice says."
</anti_hallucination_guards>

<output_format>
Markdown with frontmatter, then ten sections.

## 1. Reference Dashboard Survey (5–10 dashboards)
For each: name, public URL, last-update-date, the 3 panels that anchor the dashboard, "what they got right," "what they got wrong / feels generic." Order by relevance to the candidate's artifact (personal/portfolio-grade dashboards first, vendor-marketing dashboards second).

## 2. Distribution-Surface Verdict (answers Q2)
Vercel vs. Astro vs. Cowork vs. GitHub Pages vs. hybrid. Pick one. Cite recruiter-discovery dynamics, longevity, ship-speed, loom-ability.

## 3. Data-Loading Pattern Verdict (answers Q1)
Static-build-time vs. fetch-at-load vs. live-poll. Pick one. Cite §1 survey findings.

## 4. Anonymization Pattern (answers Q3)
What to strip / hide / show. Pick one. Reveal-cost-numbers-or-not is the load-bearing call.

## 5. The Three Anchor Panels (answers Q5)
What 3 panels MUST be visible above the fold for the 30-sec recruiter cold-open? Priority-rank them and justify with §1 references.

## 6. Naming Verdict (answers Q9)
"Agent Fleet Observability Dashboard" vs alternatives. Pick the name that triggers the right pattern-match.

## 7. Eval-Suite Integration Shape (answers Q6)
Pass-count number vs. sparkline vs. full grid vs. all three. Pick one.

## 8. Substack Hero Format + Mobile Variant (answers Q7 + Q10)
Single-screenshot hero vs. sidebar link. Does the dashboard need a mobile/screenshot variant? Cite the §1 surveys.

## 9. Two-Purpose Surface (answers Q8)
Should the Job Hunt Overlay tab actually exist on the public surface? Decide.

## 10. The Outsized-Impact Recommendation
One specific architectural or positioning change to the v0 spec that, if made before code is written, would meaningfully shift the recruiter-resonance outcome. Justify with reference to §§1, 5, and 8 findings.

## Sources Index
Every URL, blog post, podcast, post, screenshot, and reference cited above. Organized by section. Accessed-on date for each.
</output_format>

<validation>
Before delivering:
1. URL health: every public URL gets opened to verify it loads.
2. Vendor-feature verification: every vendor product feature claim cites a current product page.
3. Recruiter-attribution discipline: every "this got attention" claim has a verifiable URL.
4. Mobile-rendering discipline: any mobile-rendering claim references an actual screenshot or device test.
5. The outsized-impact recommendation must trace to specific findings in §§1, 5, or 8.
6. Word count target: 3,500–5,500 words.
</validation>
```

---

**Status when this research returns:** flip this spec's frontmatter `status` from `research-pending` to `research-complete`. Append the research file path as a new `linked_research` entry. Then update Task 11 in the unified roadmap to reflect the locked distribution surface + ship date.
