---
name: Resume strengthening recommendations 2026-05-09
description: Concrete edit list for vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md and the three tailored variants. Each row cites the source artifact (file + line range) the recommendation is grounded in. Scope: bullets to strengthen with new metrics/specifics, net-new bullets to add, story-bank entries unlocked. Output of the the-block-resume-info audit pass executed 2026-05-09.
type: career-asset
domain: product-management
status: complete
---

# Resume strengthening recommendations — 2026-05-09

> **What this is:** the user-facing payoff of the the-block-resume-info audit. It cross-references every resume-grade artifact discovered in `vault/30_domains/product-management/the-block-resume-info/` against the current master resume at `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md` and tells you exactly what to add or sharpen.
>
> **Decision rule:** every recommendation must cite (a) which current resume bullet it touches (or "NEW") and (b) the source artifact path + line range that grounds the claim. No claim without evidence.
>
> **CIIA gate:** every recommendation has been cross-referenced against [`the-block-resume-info-ciia-scrub-2026-05-09.md`](the-block-resume-info-ciia-scrub-2026-05-09.md). When the source's `ciia_status` is `redact` or `redact-internal-only`, the recommendation is framed in **capability terms** — not specific revenue, named institutional clients, or unshipped financial projections.

## TL;DR

- Audit reviewed **22 source artifacts** across 6 thematic clusters (AdOps automation, Polymarket × Campus PRD evolution, x402 strategy memo, Q2 OKRs / bi-weeklies / Project CTO, Pro 2.0 deck and pre-mortem, Granola transcripts).
- **5 bullets to strengthen** with verified specifics from the source artifacts — Section A.
- **2 net-new bullet candidates** for the master resume — Section B.
- **5 story-bank entries** unlocked for Phase 6 interview prep — Section C.
- **4 portfolio-piece candidates** that need CIIA redaction before public surfacing — Section D + cross-ref [`the-block-resume-info-ciia-scrub-2026-05-09.md`](the-block-resume-info-ciia-scrub-2026-05-09.md).
- **3 candidates considered and rejected** — Section E.
- **Conservative recommendation:** pick top 3 from B+A combined, keep one portfolio piece (D1: Polymarket PRD evolution) for sanitized public surface, ship the resume update in one ~45-min session this week before the Phase 5 application surge.

---

## A. Bullets to strengthen (existing resume bullet → upgrade)

### A1. Resume bullet: "Built and shipped 3 production Claude Skills... and a Zapier RevOps automation pipeline for the AdOps department — automating WordPress ETF page generation, Jira ticket creation, and biweekly stakeholder updates."

- **Source:** [`vault/30_domains/product-management/the-block-resume-info/AdOps-Automation-Walkthrough.md`](../../30_domains/product-management/the-block-resume-info/AdOps-Automation-Walkthrough.md), lines 11–47 (problem framing), 71–137 (Zap 1 architecture), 158–197 (Tables + Zap 2), 275–290 (full component table)
- **Current weakness:** the bullet conflates the Claude Skills work (etf-page-creator, stakeholder-update, jira-automation — three skills Sean shipped) with the Zapier pipeline (a separate, larger orchestration). The actual Zapier pipeline does **not** generate WordPress ETF pages — that's the `etf-page-creator` skill. The bullet under-sells both.
- **Strengthen to (split into two bullets):**
  - Bullet A1a (Skills): *"Shipped 3 production Claude Skills (`etf-page-creator`, `stakeholder-update`, `jira-automation`) automating WordPress ETF page generation, biweekly executive updates, and per-product Jira ticket scaffolding — directly fulfilling the P&E Q2 Objective 5 KR3 ('Ship 1-3 Claude Skills')."*
  - Bullet A1b (AdOps automation): *"Built the AdOps RevOps automation pipeline — 11 Zapier workflows + 10 product-specific intake forms + central Tables database — that turns a Salesforce 'Closed Won' trigger into auto-created parent/child Jira tickets, personalized client intake emails, and routed Slack notifications, eliminating 7 manual handoff steps per deal."*
- **Caveat:** verify "11 workflows" with Sean (the doc says Zap 1 + 10 Zap 2 instances = 11 total). Also verify "7 manual handoff steps" — the doc's "Problem This Solves" section enumerates 8 steps (1-8) and says the automation "eliminates steps 2 through 8" = 7 steps. That math is confirmed. The Q2 OKR KR3 linkage in A1a is verifiable from [`SeanxEd-Q2-OKRs-Roadmap-2026/P&E-Q2-OKRs.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/P&E-Q2-OKRs.md), line 56.
- **CIIA status of source:** `redact` (the source is labeled "AdOps team (internal)" — but the automation work is Sean's own IP under §2.4, only the audience header needs scrubbing for portfolio use; resume bullet is clean).

---

### A2. Resume bullet: "Drafted the PRD and shipped the Polymarket × Campus Sponsored Courses integration end-to-end — The Block's first sponsored-microcourse B2B revenue vertical, including X/Twitter auth flow and full user-flow QA."

- **Source:** [`The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md`](../../30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md), lines 54–62 (objective + 1.1M pageview audience), lines 165–172 (7-week milestones), lines 182–235 (5-component build); [`The Block - PRD/Sponsored_Courses_Sales_OnePager.md`](../../30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_Sales_OnePager.md), lines 21–40 (audience scale), 42–53 (4-step delivery flow); [`The Block - Bi-Weekly Update/Bi-Weekly-Update-May-1-2026.md`](../../30_domains/product-management/the-block-resume-info/The Block - Bi-Weekly Update/Bi-Weekly-Update-May-1-2026.md), line 24 (in-flight as of last bi-weekly)
- **Current weakness:** "B2B revenue vertical" is vague; "X/Twitter auth flow" is one component out of five; "full user-flow QA" undersells the architecture work. Doesn't surface the discovery-gap framing or the scalability template ("repeatable sponsor onboarding playbook") that ties to OKR Obj 1 KR4.
- **Strengthen to:** *"Authored the PRD (v1→v3) and shipped The Block's first sponsored-microcourse B2B revenue vertical (Polymarket × Campus) — a 5-component build (homepage module, Learn page hub, in-article recirculation, embedded course player, sponsor data layer) addressing the discovery gap between 1.1M monthly article pageviews and Campus education content. Delivered the sales one-pager template that productized the partnership for repeatable revenue-team sale."*
- **Caveat:** "first sponsored-microcourse B2B revenue vertical" is Sean's framing — verifiable as the first such vertical at The Block, but reword if a recruiter pushes on "first." The "1.1M monthly pageviews" and "5-component build" are directly grounded in v3.
- **CIIA status of source:** `redact` (PRD v1/v2/v3 contain pre-launch lead-export specs and pre-launch sponsor financial framing — the strengthened bullet stays in capability terms; never reference the pre-launch contract status from Bi-Weekly May 1 line 24 publicly).

---

### A3. Resume bullet (Leadership): "Performed competitive research, stakeholder interviews, A/B-session analysis, and built the demo-ready prototype for the Pro 2.0 platform proposal delivered to the incoming CEO."

- **Source:** [`SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Block-Pro-Audit-and-Gap-Analysis.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Block-Pro-Audit-and-Gap-Analysis.md), lines 16–100 (full product audit, 7 sections); [`Pro-Search-Pre-Mortem.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Pro-Search-Pre-Mortem.md), lines 21–80 (11 tigers + 4 paper tigers + 6 elephants); CLAUDE.md in that folder confirms 9-competitor analysis (Blockworks, Dune, Messari, RWA.xyz, Bloomberg, Nansen, Kaito, S&P Capital IQ Pro, Delphi Digital) + 3 internal stakeholder interviews (Cameron Tynes/Sales, Steven Zheng/Research, Simon Cousaert/Head of Data) + 3 pitch iteration rounds
- **Current weakness:** "stakeholder interviews" doesn't specify count or function. "A/B-session analysis" is vague. "Demo-ready prototype" undersells — the actual contribution arc was: full product audit → 9-competitor matrix → 3 internal stakeholder interviews → data gap analysis prioritized for institutional ICP → 3 rounds of pitch iteration → pre-mortem. **Heavy CIIA caution: do not name client institutions or revenue figures.**
- **Strengthen to:** *"Co-authored the Block Pro 2.0 product audit + competitive analysis (9 enterprise data/research platforms benchmarked) and conducted 3 internal stakeholder interviews (sales, research, head of data) to scope the pitch deck delivered to the incoming CEO — including a structured pre-mortem (11 risks across launch-blocking, fast-follow, and track tiers) that surfaced the engineering-capacity and renewal-cliff dependencies before the proposal landed."*
- **Caveat:** the pre-mortem methodology framing (Tigers / Paper Tigers / Elephants) is unusually rigorous for a PM artifact and worth keeping. Avoid naming the 9 competitors specifically in the resume; "9 enterprise data/research platforms" is verifiable and CIIA-safe. Drop "demo-ready prototype" if you can't point to a working URL — the audit doc shows the prototype was iteration round 3 in flight when the layoff hit, not a shipped artifact.
- **CIIA status of source:** `redact-internal-only` for both anchor docs. Strengthened bullet contains zero proprietary client names, zero ARR/churn figures, and zero unshipped product names (Simon AI Living Dashboard, Pro Search) — clean for public surface.

---

### A4. Resume bullet: "Authored the 10-week P&E Department 2.0 execution plan, consolidating 7 competing team-doc hubs and 25+ orphaned meeting-note pages into a per-product Confluence structure with a centralized Templates Library."

- **Source:** [`SeanxEd-Q2-OKRs-Roadmap-2026/P&E-Department-2.0-Execution-Plan.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/P&E-Department-2.0-Execution-Plan.md), lines 28–43 (audit findings: "At least 7 competing 'team docs' hubs", "~25 of the 50 most-recently-modified pages are biweekly Developer Sync meeting notes", "5+ overlapping onboarding pages", "~20 scattered 'Product requirements - X' pages"), lines 50–102 (proposed structure with 8 top-level containers), lines 113–127 (Phase 0–8 ten-week rollout)
- **Current weakness:** the existing bullet is **already verified accurate** ("at least 7 hubs" → confirmed exactly; "~25 of 50 pages" → confirmed; 10-week timeline → Phase 0 Apr 27 → Phase 8 Jul 1 confirmed). What's missing: the operating-system framing and the OKR Obj 5 linkage that elevates this from "doc cleanup" to "operational maturity proof for the new CEO."
- **Strengthen to:** *"Authored the 10-week P&E Department 2.0 execution plan (Apr 27 → Jul 1, 2026) consolidating 7 competing team-doc hubs, ~25 orphaned Developer Sync pages, and 5+ overlapping onboarding pages into a per-product Confluence architecture with a centralized Templates Library — framed as operational-maturity proof for the incoming CEO and direct delivery against P&E Q2 OKR Objective 5 (Operational Excellence & AI-Assisted Efficiency)."*
- **Caveat:** the bullet is long. If trimming, the OKR linkage is the single most differentiating addition (it ties this bullet to a concrete planning system, not just a one-off project). The "Apr 27 → Jul 1" date range is internal to the plan; consider hedging to "10-week execution plan" if recruiter doesn't need dates.
- **CIIA status of source:** `unreviewed` (no `redact` flag — the doc has internal Confluence references but no client names or revenue figures). Safe for public surface.

---

### A5. Resume bullet (Leadership): "Mapped the integration of the X402 protocol, A2A (agent-to-agent), and The Block Pro MCP into a unified agentic-wallet transaction strategy, positioning Block Pro for the agent economy under the incoming CEO."

- **Source:** [`The Block-x402-Research/x402 Strategy The Block.md`](../../30_domains/product-management/the-block-resume-info/The Block-x402-Research/x402 Strategy The Block.md), lines 14–34 (executive summary with 6-monetization-vector framing), 36–106 (Section 1: Data Dashboard Monetization with tiered pricing model), 108–186 (Section 2: News + Data API Micropayments with hybrid subscription/pay-per-request model), 187–236 (Section 3: AI Agent Data Feeds — the agentic economy play); [`x402 Implementation Guide.md`](../../30_domains/product-management/the-block-resume-info/The Block-x402-Research/x402 Implementation Guide.md), lines 11–28 (executive summary), 30–100 (server-side integration + facilitator services)
- **Current weakness:** "Mapped the integration" is passive; "unified agentic-wallet transaction strategy" reads as buzzword. The actual contribution: a 6-monetization-vector strategy memo connecting x402 (Coinbase's HTTP-payment protocol) to specific Block product surfaces (dashboards, APIs, AI agent feeds, GMCI index, Campus, content crawling) — plus an implementation guide covering server SDK choice, Cloudflare compatibility, wallet/settlement, and risk. That's a real architectural strategy doc, not a deck.
- **Strengthen to:** *"Authored the x402 / A2A / Block Pro MCP integration strategy memo — mapping 6 monetization vectors (per-chart dashboard micropayments, API pay-per-request, AI agent data feeds, index access, education micropayments, content-crawl revenue) to Coinbase's HTTP-native payment protocol — positioning Block Pro as default data infrastructure for the emerging agent economy."*
- **Caveat:** "default data infrastructure for the emerging agent economy" is aspirational framing. Drop or hedge if a recruiter pushes on it. The "6 monetization vectors" is directly grounded in the strategy doc's executive summary. The strategy was scoped but **not shipped** under Sean — the layoff intervened — so phrase as "authored / proposed," never "launched."
- **CIIA status of source:** Strategy doc is `redact` (the Block-specific framing is internal positioning); Implementation Guide is `clean` (technical guide for "a digital media and data company" — generic). The strengthened bullet uses only public protocol concepts and avoids the unshipped Block-specific revenue projections from `Revenue Scenarios.md` (which is `redact-internal-only`).

---

## B. Net-new bullets to add (under which section)

### B1. NEW bullet (Work Experience → The Block, suggested position: insert as bullet 4 after the Polymarket bullet)

- **Source:** [`SeanxEd-Q2-OKRs-Roadmap-2026/Project-CTO/Project-CTO-Visual-Audit-List.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/Project-CTO/Project-CTO-Visual-Audit-List.md), lines 17–106 (8 categories × 5–10 sites each, ~50 sites total, each with "what to look for" guidance), lines 110–116 (audit methodology: "3 things in 2 minutes" structured capture)
- **Proposed text:** *"Built the Project CTO competitive visual audit framework — a curated 50+ site benchmark across 8 categories (crypto-native, premium news, financial/data, modular newsletter formats, editorial-design, bento layouts, crypto data, wildcards) with a 'one to steal / one to never do / mobile-vs-desktop' structured capture methodology — feeding the .co homepage redesign blue-sky exploration with Josh, Serena, and Claudine."*
- **Why it works:** demonstrates competitive-research craft beyond the Pro 2.0 bullet, ties Sean to design-collaboration (Josh, Serena, Claudine — the design team Sean built rapport with), shows structured methodology that hiring managers can verify maps to PM craft. Fills a gap on the current resume — there's no bullet showing Sean's competitive-research-as-input-to-design work.
- **CIIA risk:** `unreviewed` source. Names the redesign codename (Project CTO = Core Template Optimization) which is internal but not client-facing or revenue-tied. **Recommendation:** drop "Project CTO" from the bullet text and just call it ".co homepage redesign" for public surface — the codename adds no recruiter value and adds CIIA exposure.
- **Cleaned text:** *"Built the .co homepage redesign competitive visual audit — 50+ site benchmark across 8 categories (crypto-native, premium news, financial/data, modular newsletter formats, editorial design, bento layouts, crypto data, wildcards) with a structured 'one to steal / one to never do' capture methodology — feeding blue-sky design exploration with the design team."*

---

### B2. NEW bullet (Leadership Experience → The Block, suggested position: bullet 5)

- **Source:** [`Pro-Search-Pre-Mortem.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Pro-Search-Pre-Mortem.md), lines 21–80 (11 tigers across 3 tiers + 4 paper tigers + 6 elephants); folder CLAUDE.md confirms this was authored solo by Sean before the next deck review with Ed
- **Proposed text:** *"Drove pre-mortem rigor on the Pro 2.0 pitch — surfacing 11 launch-blocking, fast-follow, and track-tier risks (engineering-capacity dependencies, renewal-cliff timing, paper-tiger versus real risks, organizational elephants) before the proposal landed — preventing a credibility-killing post-launch ARR collapse scenario."*
- **Why it works:** pre-mortems are a senior PM signal — most PMs don't run them. The Tigers/Paper Tigers/Elephants taxonomy is sophisticated and demonstrates strategic thinking. Hiring managers reading "pre-mortem" will mentally upgrade Sean's craft level.
- **CIIA risk:** `redact` on source. The proposed text avoids naming the specific risks (Fidelity renewal, Venshin departure, Cameron client demos), the specific dollar figures ($76K, $323K), and the specific clients. **Verified clean.**
- **Caveat:** if a recruiter asks for a specific pre-mortem example in interview, Sean has the original doc to walk through (use C5 in Section C below for the story-bank entry). Resume should stay at the methodology-claim level.

---

## C. Story-bank entries unlocked (Phase 6 interview prep — master plan Task 2.5)

### C1. Story: "The MattxEdxSean Pro 2.0 narrowing moment" (March 25, 2026)

- **Source:** [`the-block-meetings-granola-notes/MattxEdxSean Meeting.md`](../../30_domains/product-management/the-block-meetings-granola-notes/MattxEdxSean Meeting.md), lines 13–60 (full meeting summary)
- **Beats:** S=The Block had 3 strategic directions for Pro (Data Consortium, White-Label Simon AI, .co Premium) under exploration. T=Matt Vitebsky (interim CPO) needed Sean and Ed to converge on one direction with a deck for the incoming CEO. A=Presented the 3 options + market opportunity (institutional re-engagement, payments/tokenization/RWAs); accepted Matt's narrowing to "improve Pro as a platform"; reframed deck around 4-beat structure (Opportunity → Hypothesis → What to Build → How to Get There). R=Single deck direction locked, Matt's framework adopted, Sean and Ed split slide ownership for Figma deck.
- **Use for:** master plan Task 2.5 story 1 ("Block Pro revamp — your flagship"); demonstrates ability to take strategic ambiguity from leadership and convert it into deliverable scope.

### C2. Story: "The post-Matt Sean × Ed Pro Workshop pivot" (March 27, 2026)

- **Source:** [`the-block-meetings-granola-notes/Sean x Ed Pro Workshop.md`](../../30_domains/product-management/the-block-meetings-granola-notes/Sean x Ed Pro Workshop.md), lines 13–47
- **Beats:** S=Two days after Matt's narrowing, Sean and Ed had to translate "improve Pro as platform" into a real product idea. T=Avoid undifferentiated "dashboard refresh" framing; find a defensible value proposition. A=Workshopped 3 approaches; rejected API aggregation (data licensing concerns + users could build cheaper); identified TradFi-into-crypto institutional ICP as the defensible angle; aligned on payments + tokenized equities + RWA focus areas; agreed Sean would drive competitive analysis (Blockworks, Dune, Messari) and Ed would draft Control Room concept. R=Clear division of labor — Ed owns container UI, Sean owns the substance inside it; Sean took on competitive research as the analytical foundation.
- **Use for:** "tell me about a time you had ambiguous direction and had to bring structure" — interview pattern.

### C3. Story: "The Pro 2.0 pitch iteration arc — 3 rounds with Ed" (March 26 → April 9, 2026)

- **Source:** [`Pro-revamp-3-25-26-updated/CLAUDE.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/) (the rejected-approaches section); [`Pro-Search-Pre-Mortem.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Pro-Search-Pre-Mortem.md) (round 3 artifacts)
- **Beats:** S=Pitch needed for new CEO (May 1 start). T=Sean had to design ONE coherent product idea inside Block Pro that complemented Ed's Control Room without duplicating it. A=Round 1 ("Living Dashboard") rejected — overlapped with Ed's Control Room, too many nice-to-haves; Round 2 ("Institutional Data Moat" — 3 stitched products) rejected — too broad, didn't connect; Round 3 ("Pro Search" — narrow data-discovery product with provenance) in progress when layoff hit. R=Lesson — Ed's "ONE focused idea, not multiple" was the right north star; the iteration arc itself is proof of receiving feedback well and shipping a tighter spec each round.
- **Use for:** "tell me about feedback that changed your work" or "describe a time you had to iterate on a strategic deliverable" — interview patterns.

### C4. Story: "The AdOps automation cutover — 8 manual steps to 1"

- **Source:** [`AdOps-Automation-Walkthrough.md`](../../30_domains/product-management/the-block-resume-info/AdOps-Automation-Walkthrough.md), lines 27–47 (before-state); 49–197 (after-state architecture)
- **Beats:** S=AdOps team workflow after Salesforce deal close was 8 manual steps with creative assets scattered across email/Slack DMs/Drive links. T=Eliminate manual handoff between deal close and campaign-asset readiness without rebuilding existing tools. A=Designed two-Zap orchestration (Zap 1: Salesforce trigger → Jira tickets + Gmail intake + Slack notify; Zap 2: form submission → Jira update + status transition + Slack notify) with Zapier Tables as the central source of truth, 10 product-specific intake forms, and a duplicate-protection lock. R=AdOps team's day-to-day went from 7 manual steps to "watch Slack, act on 2 notification types"; team can now scale deal volume without scaling headcount.
- **Use for:** "tell me about a time you automated a workflow" — strong concrete example with measurable scope reduction.

### C5. Story: "The Block final conversation — handling the layoff" (May 4, 2026)

- **Source:** [`Larry_Cermak_Final_Meeting.md`](../../30_domains/product-management/the-block-meetings-granola-notes/Larry_Cermak_Final_Meeting.md) (frontmatter title: "Alex/Sean sync"; the recorded layoff-delivery conversation), lines 11–42
- **Beats:** S=Cost-cutting layoff under new CEO Steve Chung's leadership; Sean impacted along with multiple others; not performance-related. T=Receive the news, manage the immediate logistics (severance terms, separation agreement deadline), preserve the professional relationships for references and re-employment. A=Engaged with the conversation, accepted reference-letter offer (Alex Lebedyev offered to recommend for future roles + interview support, shared personal contact info), preserved network ties. R=One month severance (signing required); reference letter from Alex on offer; clear re-employment support pathway.
- **Use for:** "tell me about a time you faced a setback" — handle with care; lead with the next chapter (the job-hunt sprint, the open-source work, the portfolio short) rather than dwelling on the layoff itself. Use this story selectively — only when the recruiter explicitly asks "why did you leave The Block?"

---

## D. Portfolio-piece candidates (Phase 4 / unified roadmap Tasks 4–5)

### D1. Portfolio piece: "Polymarket × Campus Sponsored Courses — full PRD evolution v1 → v3"

- **Source:** [`The Block - PRD/Sponsored_Courses_PRD_Confluence.md`](../../30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_PRD_Confluence.md) (v1), [`Sponsored_Courses_PRD_Confluence_v2.md`](../../30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_PRD_Confluence_v2.md) (v2), [`Sponsored_Courses_PRD_Confluence_v3.md`](../../30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md) (v3 final), [`Sponsored_Courses_Sales_OnePager.md`](../../30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_Sales_OnePager.md) (sales artifact)
- **Why it works:** v1→v3 evolution is uncommonly clean evidence of PM craft — recruiters can see Sean adding components (Component 1: Homepage Module appeared in v3 only), refining metrics (1.2M → 1.1M pageviews after Sept-Dec 2025 GA4 pull), and adding sales-team enablement (one-pager template) over iterations. The pairing with the sales one-pager shows revenue-team productization, not just engineering execution.
- **CIIA gating:** `redact` per scrub list — must redact the pre-launch Polymarket lead-export integration spec, the "100+ leads (Month 1)" pilot target, the X/Twitter auth lead-capture flow specifics, and the sponsor data export tech detail before public surfacing. The post-launch general framing ("first sponsored-microcourse B2B revenue vertical") is clean per the Polymarket carve-out in the scrub list.
- **Best fit:** unified roadmap Task 4 (sanitized portfolio piece) or Phase 4 EXPLANATION.md. Suggested format: a markdown side-by-side showing Component 1 (Homepage Module) added in v3 + Component 5 (Sponsor Data & Sales Enablement) refinement across v1→v2→v3, with redaction notes inline. Estimated 60–90 min sanitization effort.

### D2. Portfolio piece: "AdOps Automation Walkthrough — full architecture document"

- **Source:** [`AdOps-Automation-Walkthrough.md`](../../30_domains/product-management/the-block-resume-info/AdOps-Automation-Walkthrough.md), full file (312 lines)
- **Why it works:** the doc is exceptionally well-written for a non-technical audience — every architecture decision has a "why this not that" explanation in italics (lines 87, 110, 164–170). It's the closest thing in the audit to a finished portfolio piece. Demonstrates technical-writing craft + systems-design thinking.
- **CIIA gating:** `redact` per scrub list — only requires removing the "Audience: AdOps team (internal)" header on line 13 and the "Sean Winslow (swinslow@theblock.co)" escalation contact on line 301. Otherwise clean.
- **Best fit:** unified roadmap Task 4. Lowest CIIA-redaction effort (15 min). Highest immediate portfolio value. **Recommended as the first portfolio piece to sanitize.**

### D3. Portfolio piece: "Project CTO Visual Audit Framework"

- **Source:** [`SeanxEd-Q2-OKRs-Roadmap-2026/Project-CTO/Project-CTO-Visual-Audit-List.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/Project-CTO/Project-CTO-Visual-Audit-List.md), full file
- **Why it works:** clean, structured, recruiter-readable. Shows competitive-research methodology + design collaboration. The "How to Run the Audit" methodology (lines 110–116) is portable and demonstrates Sean's ability to give designers concrete patterns instead of abstract direction.
- **CIIA gating:** `unreviewed` per scrub list — no flagged content. Drop "Project CTO" codename and rename to "homepage redesign visual audit" for public surface (codename adds no value).
- **Best fit:** unified roadmap Task 4 — secondary portfolio piece, complements D2 (architecture craft) with a competitive-research artifact. Estimated 30 min sanitization.

### D4. Portfolio piece: "P&E Department 2.0 Execution Plan"

- **Source:** [`P&E-Department-2.0-Execution-Plan.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/P&E-Department-2.0-Execution-Plan.md), full file (184 lines)
- **Why it works:** demonstrates operational thinking — the Section 9 "How this reads as proof of leadership" is a meta-frame that hiring managers will recognize as senior-PM thinking. The phased rollout (Phase 0–8) with explicit owners + dependencies + risks is execution-document craft.
- **CIIA gating:** `unreviewed` per scrub list — no flagged content. Section 7 "Decision points for Ed (Monday Apr 27)" names the new CEO (Steve Chung) and Mike (engineering lead) — consider redacting names for public surface, replace with "incoming CEO" and "engineering lead."
- **Best fit:** unified roadmap Task 5 (pickier portfolio surface). Estimated 45 min sanitization.

---

## E. Considered and rejected

### E1. Rejected: iOS Training docs

- **Source:** `SeanxEd-Q2-OKRs-Roadmap-2026/iOS-Training-2026/*.md`
- **Why considered:** training docs Sean produced for fellow PMs (referenced in the OKR doc).
- **Why rejected:** internal training, narrowly scoped to TestFlight workflow, not externally legible. Already covered in Leadership-Experience bullet 2 ("Onboarded fellow Product Managers on Claude Code...").

### E2. Rejected: x402 Implementation Guide as portfolio piece

- **Source:** [`The Block-x402-Research/x402 Implementation Guide.md`](../../30_domains/product-management/the-block-resume-info/The Block-x402-Research/x402 Implementation Guide.md)
- **Why considered:** technically detailed external research output, well-written, clean CIIA status.
- **Why rejected:** the doc is generic to "a digital media and data company" — strips most Block-specific context. As a public artifact it reads as research summarization rather than original PM work. Sean's actual contribution (mapping x402 to 6 Block-specific monetization vectors) lives in the `redact`-flagged Strategy doc, which can't be surfaced cleanly. Use the strengthened resume bullet (A5) instead of a portfolio piece for the x402 work.

### E3. Rejected: Pro 2.0 audit / gap analysis as portfolio piece

- **Source:** [`Block-Pro-Audit-and-Gap-Analysis.md`](../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Block-Pro-Audit-and-Gap-Analysis.md)
- **Why considered:** demonstrates the most sophisticated PM craft in the audit — full product audit + competitive matrix + 13.8K-deal funding database analysis.
- **Why rejected:** `redact-internal-only` per scrub list — the doc is built around proprietary client revenue figures ($693K renewal ARR / $442K churn ARR / $173K downsell / 21% churn / specific $/year enterprise positioning). Sanitizing the doc enough for public surface would gut the substance. Keep for personal reference + interview talking points (story C3) only. **Use story-bank C3 + resume bullet A3 instead.**

---

## How to use this document

1. **Tonight or this weekend:** open the master resume at `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md` alongside this file. Apply A1a + A1b (split the Skills/AdOps bullet), A4 (Confluence strengthen), and B1 (NEW visual audit bullet) — that's the highest-leverage 30-min revision.
2. **Before the next interview:** rehearse stories C1, C3, and C4 — the three strongest narratives. C5 (the layoff) only when explicitly asked.
3. **Phase 4 / unified roadmap Tasks 4–5:** start with D2 (AdOps Walkthrough — 15-min sanitization, highest portfolio yield). Add D3 second (visual audit) if you need design-craft evidence. D1 (Polymarket PRD evolution) is the most impressive but the most CIIA-effortful — save for a final polish session.
4. **Cross-reference [`the-block-resume-info-ciia-scrub-2026-05-09.md`](the-block-resume-info-ciia-scrub-2026-05-09.md) before any public surfacing.** Every recommendation in this file has been pre-checked against the scrub list, but the redaction work is yours to do in the source files.
