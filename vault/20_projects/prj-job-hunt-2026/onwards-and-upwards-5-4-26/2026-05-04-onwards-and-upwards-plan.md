# Onwards and Upwards — Job Hunt + Build Plan

> **For Sean:** This is a plan, not a sentence. Steps use checkbox (`- [ ]`) syntax. Work it phase by phase. The first 24 hours are about protecting downside; the next 30 days are about positioning; everything after is about compounding. Mark items done as you go — small wins are the antidote to spiral.

> **Status update (2026-05-05):** Operating-model interview completed for `job-hunt-2026` (CHANGELOG v3.26.2). All 5 artifacts at `vault/05_atlas/operating-models/job-hunt-2026/` at `status: confirmed`. Tier-A truths locked: walk-away $100k, 5-days-in-office = no, agents draft / Sean sends, Track-C protected, Friday retro non-negotiable. Relocation overrides: Anthropic OR $250k+/yr. **Phase rhythm refinement from interview** — the day is now framed as one fluid 8:30–5:30 container with parallel activities (not block-scheduled per phase day-of-week), with a sacred 8:30–9:30 AM learning hour and a mandatory 1–2 PM break. The phase arc (Phase 1–8 below) still holds; only the intra-day shape changed. **Open work items the bundle surfaced are tracked in [[2026-05-04-migration-completion-handoff#Operating-model interview completed (2026-05-05)|the migration-completion handoff doc]].** Phase 4 (MCP server) is the time-sensitive one — interview surfaced the cold-start chain (name → repo → README → plan) as the top self-blocking decision; target ship date 2026-05-25 means kickoff this week.

> **Priority shift (2026-05-07):**
> - Claude Code-assisted work going forward is portfolio projects, portfolio website creation, and build-in-public strategy. Resume + LinkedIn are Sean-owned, off the Claude track.
> - The unified roadmap at [`2026-05-06-unified-roadmap.md`](job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md) is the operative plan. Its Tasks 0–7 + the "This Week's 5 Decisions" block supersede the master plan's Phase 2 / Phase 4 ordering.
> - Track-C (MCP server v0 ship 2026-05-25 — `intent-engineering`) remains Tier-A protected per the operating-model. The portfolio website (`/transactions/` route, Astro 5 + React islands per unified roadmap Decision 2) and build-in-public cadence (one Substack post per Friday + LinkedIn syndication per unified roadmap Task 6 §C / §D) join Track-C as the protected work.
> - All other Tier-A protections from the operating-model still hold.

**Goal:** Convert the May 4, 2026 layoff at The Block into a deliberately-shaped 8–14 week sprint that lands a new role (AI PM, Technical PM, or Creative PM) — Boston metro or remote — while shipping the portable career artifacts that the Karpathy synthesis identified as the highest-compounding moves.

**Architecture:** Three concurrent tracks running off one shared rhythm.
- **Track A — Runway:** Severance, unemployment, health insurance, finances. Non-negotiable. Done in week 1, then maintained.
- **Track B — Pipeline:** Applications, interviews, target list, network outreach. The job-hunt machine.
- **Track C — Differentiator:** MCP server (`intent-engineering` v0, ship 2026-05-25) + portfolio website (`/transactions/` route) + build-in-public artifacts (Substack + LinkedIn syndication + GitHub `EXPLANATION.md` files). The work that survives every market scenario.

Tracks A and B run hot in weeks 1–2; Track C ramps in week 2 and runs to week 6. Daily rhythm (Phase 7) is the connective tissue.

**Stack:**
- **Tracking:** This file (canonical plan), `vault/20_projects/prj-job-hunt-2026/` (ongoing tracking notes), daily notes (`vault/10_timeline/daily/`)
- **Comms:** Gmail (sean.winslow28@gmail.com), LinkedIn, Telegram (Alex's reference), personal X
- **Build:** TypeScript MCP SDK (`@modelcontextprotocol/sdk`), Node 22, Anthropic SDK, GitHub for hosting
- **Publishing:** Substack OR portfolio site (decide in Phase 5; don't decide today)

---

## Open Threads (carry forward — do not let these slip)

Both items closed 2026-05-07. Kept here for historical traceability; Friday-retro check no longer required.

- [x] **Counter-signed severance PDF from Leanne.** ✅ Closed 2026-05-07 — fully executed PDF received from Block.
- [x] **Block-named skills scrub before any public Superuser Pack push.** ✅ Closed 2026-05-07 — the three CIIA-protected skills (`the-block-jira-ticket-writer`, `etf-page-creator`, `biweekly-jira-update`) have been handled per the Phase 4 plan. Phase 3 Task 3.3 (public announcement) and Phase 4 Task 4.3 Step 9 (publish MCP server / pin Superuser Pack on profile) are no longer gated by this item.

---

## Phase 0: Today + Tomorrow (May 4–5, 2026) — Protect Downside, Decompress

### Task 0.1: Cut the panic loop

**Files:**
- Create: `vault/10_timeline/daily/2026-05-04.md` (likely already exists — append a layoff section)
- Create: `vault/20_projects/prj-job-hunt-2026/README.md`

- [x] **Step 1: Write the day down.** Append a short section to today's daily note titled "Layoff — what happened, how I feel, what I did about it." Five bullets max. This is for you in 6 weeks when the lens flips from "this is awful" to "this is when I pivoted." Stop after five bullets — no spiraling on paper.

- [x] **Step 2: Set up the project hub.** Create `vault/20_projects/prj-job-hunt-2026/README.md` with three sections: `## Pipeline` (companies + status), `## Artifacts` (resume v, LinkedIn v, MCP server v, essay v), `## Weekly Retro` (one line per week). This is the dashboard.

- [x] **Step 3: Tell three people who matter, no more, today.** Maryalice (already), one close friend, one professional ally outside The Block. Not your parents yet unless you want to. Not LinkedIn — that's a Phase 3 decision after positioning is set. Public announcement is a strategic move; don't make it an emotional one.

- [x] **Step 4: Stop work at a reasonable hour. Eat. Sleep.** No grand strategy tonight. Tomorrow morning is when the plan starts. Tonight is for being a person.

### Task 0.2: Lock the calendar

**Files:**
- Modify: Google Calendar (both `sean.winslow28@gmail.com` and `swinslow@theblock.co` — although Block calendar access may be revoked at any moment)

- [x] **Step 1: Export the Block calendar today.** While you still have access. File → Export from Google Calendar settings, save the .ics. You'll lose access soon and there are reference contacts and meeting context buried in there.

- [x] **Step 2: Block your calendar 8:30 AM–12:30 PM Mon–Fri for the next 4 weeks.** Title: "Job Hunt — Deep Work." This is your new morning shift. Afternoons stay flexible for interviews, errands, life.

- [x] **Step 3: Block 4:30–5:30 PM Fri** as "Weekly Retro" — non-negotiable check-in with yourself.

---

## Phase 1: Stabilize the Runway (Week 1, May 4–11) — Track A

### Task 1.1: Severance agreement decision ✅ COMPLETED 2026-05-05

> **STATUS:** Signed and sent to Leanne Li (VP People Operations) on 2026-05-05. Claude review (5-flag analysis: CIIA, ADEA exposure, NY forum-selection, laptop reset deadline, FLSA representation) substituted for the paid attorney review given the 2026-05-07 signing deadline. Tenure recalibrated post-CIIA review: ~6 months service (start 11/10/2025), so one-month severance ($8,333.33) is fair, not lowball. CIIA Section 5 1-year non-solicit is the only meaningful post-termination obligation; no post-termination non-compete (MA-compliant). Three Block-named skills (`the-block-jira-ticket-writer`, `etf-page-creator`, `biweekly-jira-update`) flagged for scrub before any public Superuser Pack push — see Phase 4 / public-launch checklist.

**Files:**
- Severance agreement (text): `vault/50_sources/finance/the-block-severance-docs/severance-agreement-doc.md`
- CIIA (was bundled with offer letter): `vault/50_sources/finance/The Block Day 1 Information/The_Block_Offer_Letter.pdf` (pages 4–13)
- Counter-signed PDF (pending): `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/severance-agreement-signed.pdf`

- [x] **Step 1: Wait for the email.** Received from Leanne ahead of EOD 2026-05-05.

- [x] **Step 2: Read the entire agreement once before noting anything.** Done 2026-05-05 — full review with Claude. Flags raised: 3-day signing window (vs. ADEA's 21/45-day requirement if 40+); Section 17 governs disputes in NY courts despite MA-governing-law; Section 8 laptop factory-reset deadline; Section 4(d) FLSA representation; Section 15 reaffirms the CIIA. CIIA itself: Section 5 1-year non-solicit (employees + customers + potential customers), Section 2.4 self-developed-IP carve-out applies for general-purpose work, Exhibit A was left blank at hire (small vulnerability for any pre-existing inventions).

- [x] **Step 3: Legal review.** Substituted Claude's structured 5-flag review for paid attorney review given the 48-hour signing window and short-tenure context. Reasonable compromise; flagged that for any future severance with bigger $ at stake or longer tenure, a paid MA attorney review is the right move regardless of timeline pressure.

- [x] **Step 4: Decide and sign by the deadline.** Signed and sent to Leanne 2026-05-05.

- [x] **Step 5: Save fully counter-signed copy.** ✅ Received 2026-05-07; counter-signed PDF saved.

### Task 1.2: Health insurance — COBRA decision and ACA marketplace

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/health-insurance-comparison.md`

- [ ] **Step 1: Get the COBRA election notice.** It must arrive within 14 days by federal law. Block's HR will send. It tells you the monthly cost (approximately $700–1,200/mo individual, $1,800–2,500/mo family — varies wildly by plan).

- [ ] **Step 2: Pull current Block plan benefits summary** so you can compare apples to apples. Should be in your existing benefits portal or last open enrollment doc.

- [ ] **Step 3: Open a comparison file with three columns: COBRA continuation / ACA Marketplace silver plan / ACA Marketplace bronze plan.** Compare: monthly premium, deductible, OOP max, prescription coverage (esp. anything you currently take), in-network providers (esp. anyone you see regularly).

- [ ] **Step 4: Open MA Health Connector (mahealthconnector.org).** Layoffs trigger a Special Enrollment Period — you have **60 days from your last day** to enroll without penalty. Get a real quote. Often a Connector silver plan is dramatically cheaper than COBRA and the network is fine for most metro Boston needs.

- [ ] **Step 5: Decide before May 18.** Default: ACA Marketplace silver plan unless COBRA is the only way to keep a critical specialist. Save the decision rationale in the file.

### Task 1.3: Unemployment insurance

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/unemployment-claim.md`

- [x] **Step 1: File the day after your last day (May 5).** MA Department of Unemployment Assistance: mass.gov/unemployment. Online filing takes ~30 minutes.

- [ ] **Step 2: Have ready:** SSN, driver's license, Block's full legal name + address (find on a recent paystub), employment dates, gross earnings per quarter for the last 4 quarters, reason for separation = "Lack of work / layoff."

- [ ] **Step 3: Note the weekly certification day.** You'll need to certify weekly — usually a 5-minute form. Set a recurring reminder for that day, every week, until you accept an offer.

- [ ] **Step 4: Severance interaction.** In Massachusetts, severance is generally treated as wages allocated to the period it covers, which can delay UI benefits. Report the severance accurately when filing — DUA will figure out the offset. Don't try to game this; lying to DUA is fraud.

- [ ] **Step 5: Save the claim number and the determination letter when it arrives.**

### Task 1.4: Finances — runway math

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/runway-math.md`

- [ ] **Step 1: Compute gross runway.** Liquid savings + severance net + expected weekly UI × 26 weeks. Don't include investment accounts you aren't willing to touch.

- [ ] **Step 2: Compute monthly burn at three levels:**
  - **Lean** (cut subscriptions, no eating out, no travel): figure on the conservative side
  - **Normal** (current spend minus Block-adjacent costs)
  - **Aspirational** (normal + budgeted job-hunt expenses: lawyer, professional photos, a few meals with contacts)

- [ ] **Step 3: Compute runway in months at each level.** That's your decision compass. If lean runway is < 4 months, the urgency dial is at 9. If lean runway is > 9 months, you can be more selective on roles.

- [ ] **Step 4: Identify the three biggest discretionary cuts.** Not all subscriptions — the **three** that move the needle. Cancel them today. The personal-finance skill in life-systems can help if you want to delegate. Don't death-by-a-thousand-cuts; pick the three.

- [ ] **Step 5: One-time expenses to budget for:** lawyer (~$300), professional headshots if LinkedIn photo is dated (~$200), domain registration if you don't have a personal one (~$15/yr), one travel/hotel for an in-person interview (~$500). Earmark $1,500 total in the runway math.

### Task 1.5: Block offboarding logistics

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/block-offboarding-checklist.md`

- [ ] **Step 1: Personal data extraction (do today, access disappears fast):**
  - Personal contacts in Slack DMs → export thread or save names/emails to a file
  - LinkedIn-saved colleagues from Block → no action needed, you keep those
  - Google Drive personal files → download anything personal NOW
  - Calendar events with personal-network people → already exported in Task 0.2
  - Browser bookmarks if you used a Block-managed browser → export

- [x] **Step 2: Equipment return.** Wait for HR's instructions; don't ship anything until you have a return label and confirmation. Document model + serial of laptop, monitor, peripherals before you return them.

- [x] **Step 3: Final paystub + W-2 expectations.** Confirm address on file is correct so the W-2 mails to you in January. Confirm last paycheck timing.

- [ ] **Step 4: 401(k) — open Fidelity Rollover IRA THIS WEEK; complete direct rollover when distribution form arrives.** Current state (NetBenefits, 2026-05-04): $1,398.70 in **THE BLOCK 401K PLAN** (account 401(k):6851X), administered by Fidelity under the Justworks PEO wrap plan. Action plan:
    - **Sub-step A — TODAY/TOMORROW: Open a Fidelity Rollover IRA online** (10 min at fidelity.com → Open Account → Rollover IRA). Free; no funding needed. This is the empty destination bucket.
    - **Sub-step B — THIS WEEK: Add beneficiaries to the 401(k)** while you still have NetBenefits access (the first notification on the dashboard). 2 minutes; prevents probate hassle.
    - **Sub-step C — Confirm vesting status before distribution.** Pull `Justworks_Wrap_Plan_SPD.pdf` (in `vault/50_sources/finance/The Block Day 1 Information/TheBlock-Fidelity 401k set up/2025-financial-and-tax-docs/The-Block-Tax-Docs/`) or check the "Vested Balance" line in NetBenefits. At 6 months tenure, you're likely 0% vested in any employer match if there's a graded/cliff vesting schedule. Your own elective contributions are always 100% yours; expect the actual rollover amount to be ≤ $1,398.70.
    - **Sub-step D — When Fidelity sends the Distribution Election Notice (30–90 days post-separation), elect "Direct Rollover to IRA"** and provide the new Rollover IRA account number. Critical phrase = "direct rollover" or "trustee-to-trustee transfer." **Never accept a check made out to you** — that triggers 20% mandatory withholding even if you intend to roll within 60 days.
    - **Why NOT leave it in the plan:** Per SECURE 2.0 (effective 2024), balances under $7,000 trigger mandatory force-out for separated participants. <$1,000 = force-cash; $1,000–$7,000 = auto-roll to whichever IRA provider the plan has on contract (usually a small custodian with mediocre fees). Pre-empt with your own Fidelity Rollover IRA.
    - **Why NOT cash out:** Math on $1,398.70 cashed at age <59½ = 20% federal withholding (-$280) + 10% early withdrawal penalty (-$140) + ordinary income tax in 2026 (~22% bracket with severance + UI ≈ -$300). Net ≈ $680 from $1,398. ~50% effective hit. Don't.
    - **One related ask for Leanne:** confirm in writing that no equity grants (RSUs, options, ESPP) exist beyond the 401(k) — Section 2(c) of the severance releases all claims for "stock awards, stock options," so anything not surfaced before the Effective Date is gone.

- [ ] **Step 5: Reference letter from Larry.** Send him a Telegram message **this week**, friendly and short, saying thank you and asking if he's still up for being a reference. He volunteered — take him up on it. Sample: "Larry — really appreciated the way you handled today. Wanted to take you up on the reference offer. Happy to send a one-pager on what I'm looking for whenever you have a sec. Thanks."

---

## Phase 2: Position Yourself (Week 1–2, May 5–18) — Track B

### Task 2.1: Decide your three target archetypes (sharpen the funnel)

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/target-archetypes.md`

- [ ] **Step 1: Write a one-paragraph pitch for each archetype.** Three paragraphs total. Each pitch is what you'd say to a recruiter who asked "what kind of role are you looking for?"
  - **AI PM** — angle: agentic engineering practitioner who ships. Anchor evidence: Superuser Pack, MCP server (forthcoming), 14 SDK agents.
  - **Technical PM** — angle: PM who reads + writes code, ships specs that engineers respect. Anchor: PRDs at The Block, intent-engineering skill, working knowledge of TS/Python/Claude SDK.
  - **Creative PM** — angle: 12 years illustration/animation + PM at a media company + agentic creative pipeline. Anchor: animation pipeline, design-team agents, writing-voice-modes.

- [ ] **Step 2: Rank them.** Karpathy's framework + your stated goals + the current market suggest: **AI PM > Technical PM > Creative PM.** AI PM has the most listings; Creative PM has the longest cycles; Technical PM is the safety net. You don't have to fully pick — but if you have one resume bullet to lead with, pick the archetype that bullet serves.

- [ ] **Step 3: Acceptance criteria — three "yes" filters and three "no" filters.** Examples:
  - YES: PM-track role, $X minimum, remote OR Boston metro hybrid, AI/agent/data product surface area
  - NO: pure project management role, individual contributor IC dev role (unless title is Tech Lead PM), <$X, financial services with no AI angle, anti-remote in non-Boston

- [ ] **Step 4: Salary anchor.** Compute three numbers: walk-away (you won't take less), target (your real ask), reach (top of the range you'd quote with confidence). Use levels.fyi + Glassdoor for AI PM / Technical PM in Boston metro and remote. Write them down. You'll need them in 4 weeks.

### Task 2.2: Resume rewrite — one master + three tailored 🟡 V1 master + 3 variants drafted 2026-05-07

> **🟢 Sean-owned · off the Claude Code track (2026-05-07).** Resume work is Sean's lane. Future iterations happen on Sean's own time without Claude in the loop. The methodology callout below stays as a reference for any future iteration.

> **STATUS (2026-05-07):** Master resume rewritten V1→V3 + 3 tailored variants (AI PM, Tech PM, Creative PM) drafted in one ~90-min session. Variants are reorder + Summary swap of the master with no new content invented (per Step 5). **Pending on Sean's side:** read each aloud (Step 7), cut what sounds robotic, decide whether NYL bullets need modernization for 2026-target recruiters, decide whether the HelloPM cert listing is still active.
>
> **Actual files (supersede the planned paths in the Files block below):**
> - Master: [`../assets/Sean_Winslow_Resume.md`](../assets/Sean_Winslow_Resume.md)
> - AI PM variant: [`../assets/Sean_Winslow_Resume_AI_PM.md`](../assets/Sean_Winslow_Resume_AI_PM.md)
> - Tech PM variant: [`../assets/Sean_Winslow_Resume_Tech_PM.md`](../assets/Sean_Winslow_Resume_Tech_PM.md)
> - Creative PM variant: [`../assets/Sean_Winslow_Resume_Creative_PM.md`](../assets/Sean_Winslow_Resume_Creative_PM.md)
>
> **Methodology — how the V1 was sourced:** Sean self-dumped a 14-bullet workstream summary at [`the-block-resume-additions-2026.md`](../../../30_domains/product-management/the-block-resume-info/the-block-resume-additions-2026.md), with each bullet pointing at its evidence artifact inline. Six evidence files were read in parallel to ground the bullets in measured outcomes + JD competency coverage:
>
> 1. [`P&E-Q2-OKRs.md`](../../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/P&E-Q2-OKRs.md) — Q2 OKR backbone (Objs 1–5 with KRs); the role's actual quantifiable goals.
> 2. [`Bi-Weekly-Update-May-1-2026.md`](../../../30_domains/product-management/the-block-resume-info/The%20Block%20-%20Bi-Weekly%20Update/Bi-Weekly-Update-May-1-2026.md) — most recent shipped-work catalogue, pre-written.
> 3. [`Bi-Weekly-Update-April-17-2026.md`](../../../30_domains/product-management/the-block-resume-info/The%20Block%20-%20Bi-Weekly%20Update/Bi-Weekly-Update-April-17-2026.md) — mid-tenure shipped work.
> 4. [`P&E-Department-2.0-Execution-Plan.md`](../../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/P&E-Department-2.0-Execution-Plan.md) — strategic leadership evidence (the 10-week Confluence overhaul Sean authored).
> 5. [`TASKS.md`](../../../30_domains/product-management/the-block-resume-info/SeanxEd-Q2-OKRs-Roadmap-2026/TASKS.md) — line-item evidence + Project CTO scope context.
> 6. [`The-Block-Job-Description.md`](../../../30_domains/product-management/the-block-resume-info/The-Block-Job-Description.md) — JD competencies for cross-checking bullet coverage.
>
> Selected Projects section was sourced directly from repo files (`CHANGELOG.md`, `CLAUDE.md`, the unified roadmap) — no CIIA gate since those are Sean's own open-source artifacts.
>
> **Forward pointer — `the-block-resume-info/` folder:** [`vault/30_domains/product-management/the-block-resume-info/`](../../../30_domains/product-management/the-block-resume-info/) contains a substantial unprocessed archive beyond the 6 files used in this V1 pass. Material likely useful for future resume iterations, portfolio breakdowns, talk-track stories, and the unified roadmap's Tasks 4–5:
>
> - **Polymarket Sponsored Courses PRD evolution** — 4+ versioned `.docx` files in [`The Block - PRD/`](../../../30_domains/product-management/the-block-resume-info/The%20Block%20-%20PRD/) (Sponsored Courses PRD Confluence v1 / v2 / v3, Campus_Sponsored_MicroCourses_PRD_v3, Matt-aligned variant), plus the user-flow diagram, Ed's annotated PDF notes, the Sponsored Courses Sales One-Pager, the user-flow JPEG, and the Slack-conversation export with Ed about PRD reassessment. Flagship-quality material for a future portfolio breakdown.
> - **x402 / agentic-wallet research** — 4 PDFs in [`The Block-x402-Research/`](../../../30_domains/product-management/the-block-resume-info/The%20Block-x402-Research/) (Strategy, Implementation Guide, Competitive Landscape, Agentic Economy framing). The Block Leadership-Experience X402 / A2A / Pro MCP bullet is grounded in these. Strong Phase 6 interview-prep fuel and a clean Karpathy-aligned "agent economy" portfolio piece.
> - **AdOps automation walkthrough** — [`AdOps-Automation-Walkthrough.docx`](../../../30_domains/product-management/the-block-resume-info/AdOps-Automation-Walkthrough.docx). Concrete Zapier RevOps automation evidence; could let the Zapier line in Work Experience bullet 1 become a deeper portfolio piece.
> - **Granola meeting transcripts** — 40+ files in [`vault/30_domains/product-management/the-block-meetings-granola-notes/`](../../../30_domains/product-management/the-block-meetings-granola-notes/). Includes the Larry Cermak final meeting, the Matt × Ed × Sean meeting, weekly Sean × Ed 1:1s, Brand / Media / Design Weekly Syncs, Project CTO Design Check-ins, Pro Future research / data discussions, App Store rejection thread, Confluence Cleanup syncs, and the Sean × Ed Pro Workshop. Story-bank fuel for master plan Task 2.5 (8 STAR stories).
> - **JD competency breakdowns** — 13 files in [`The Block Job Description Breakdowns - ChatGPT/`](../../../30_domains/product-management/the-block-resume-info/The%20Block%20Job%20Description%20Breakdowns%20-%20ChatGPT/), one per JD line. Useful as a coverage cross-check on tailored variants and as direct cover-letter input.
> - **Design assets + diagrams** — PNG / JPEG mockups, sponsored-courses user-flow visuals, Mermaid diagrams (`.md`), Block PRD visual, recess example image, GA4 screenshot.
> - **Additional bi-weekly updates** — beyond the 2 read in this pass, others may exist in [`The Block - Bi-Weekly Update/`](../../../30_domains/product-management/the-block-resume-info/The%20Block%20-%20Bi-Weekly%20Update/).
> - **Block + Campus overviews** — [`TheBlock-And-Campus-Overviews.md`](../../../30_domains/product-management/the-block-resume-info/TheBlock-And-Campus-Overviews.md). Useful for talk-track context and "company you worked at" framing on cover letters.
>
> **Recommended follow-up — deep audit + markdown conversion (~90 min, not yet scheduled):** Schedule a one-shot audit pass on this folder that (1) inventories every file with a one-line description + which downstream artifact (resume variant, portfolio breakdown, story-bank entry, x402 essay, talk track) it can feed; (2) converts the high-value `.docx` files (Polymarket PRD versions, AdOps walkthrough, Sponsored Courses One-Pager) to markdown so Claude Code agents can read them directly without `pandoc` overhead — none of these are vault-indexed today because most files lack YAML frontmatter and many are non-text formats; (3) adds YAML frontmatter to every markdown file in the folder for the nightly vault-indexer; (4) flags any file containing Block-protected IP per CIIA §2.3 that needs sanitization before any public surfacing — particularly anything with proprietary client lists, internal Pro revenue figures, unannounced partnership names, or financial projections from the Pro 2.0 deck. Best run before the Phase 5 Week-3 application surge or before any portfolio piece starts referencing these artifacts. Daily-note breadcrumb for this V1 session: [`vault/10_timeline/daily/2026-05-07.md`](../../../10_timeline/daily/2026-05-07.md) Claude Code Sessions block.

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/resume-master-2026-05.md`
- Create: `vault/20_projects/prj-job-hunt-2026/resume-ai-pm.md`
- Create: `vault/20_projects/prj-job-hunt-2026/resume-tech-pm.md`
- Create: `vault/20_projects/prj-job-hunt-2026/resume-creative-pm.md`

- [ ] **Step 1: Pull your existing resume.** Most likely in Google Drive or a previous version on your portfolio site. If it's >12 months old, treat it as raw material, not a base.

- [ ] **Step 2: Rebuild the master resume in Markdown.** Sections: Header (name, Boston, email, phone, LinkedIn, GitHub, portfolio site) → Summary (2 lines max) → Experience (reverse chrono, ≤5 bullets per role, each bullet starts with a verb and ends with a metric or named artifact) → Selected Projects (3, with link/repo) → Skills (no skill list of doom — group as "Product / Technical / Creative") → Education.

- [ ] **Step 3: Write each Block bullet to the Karpathy frame.** Example rewrites — these are templates, fill in real numbers:
  - "Owned the Block Pro research surface area roadmap; shipped X features over 18 months, increasing institutional retention by Y%."
  - "Authored the agent-native research interface intent spec, reframing Block Pro as a multi-consumer product (human UI + agent MCP). Adopted by engineering as the foundation for the v2 platform."
  - "Built and operated a 14-agent autonomous research fleet (Claude Agent SDK) that runs on a $0/month local-first stack and produces daily morning briefings."

- [ ] **Step 4: Write the "Selected Projects" section.** Three projects:
  - **Claude Code Superuser Pack** — link to GitHub. One line: "117 skills, 13 hooks, 14 autonomous agents. Open-source agentic engineering toolkit."
  - **Agentic Financial-Research Fleet** — describe carefully (no personal numbers). One line: "Multi-agent research system over a verifiable financial domain; design exemplar of Karpathy-style sensors+actuators on a fine-tuned local stack."
  - **Animation Pipeline (16BitFit + portfolio shorts)** — link to portfolio. One line: "Agent-orchestrated 2D animation pipeline; humans own creative ceiling, agents own technical floor."

- [ ] **Step 5: Tailor three variants** by re-ordering the bullets and switching the Summary line. Don't lie; just emphasize.

- [ ] **Step 6: Convert master to PDF.** Use a clean template — your portfolio site might have one, or use Resumake, or LaTeX if you're feeling fancy. Two pages max; one page if you can do it without strain.

- [ ] **Step 7: Read out loud.** Anything that sounds like it was written by a robot, rewrite. Anything you can't defend in an interview, cut.

### Task 2.3: LinkedIn refresh

> **🟢 Sean-owned · off the Claude Code track (2026-05-07).** LinkedIn refresh is Sean's lane. Future iterations happen on Sean's own time without Claude in the loop.

**Files:**
- (No file — directly on LinkedIn)
- Save before/after screenshots to `vault/20_projects/prj-job-hunt-2026/linkedin-snapshots/`

- [ ] **Step 1: Update headline.** Not "Open to Work" yet — that's a Phase 3 toggle after positioning is locked. Headline lead: pick one archetype and lead with it. Example: "AI Product Manager · Agentic Engineering Practitioner · Ex-The Block (Crypto Data, Pro Research)"

- [ ] **Step 2: Rewrite the About section.** Three short paragraphs.
  - P1: who you are, one career sentence, your superpower
  - P2: what you've shipped (Block + Superuser Pack + animation pipeline) — concrete artifacts
  - P3: what you're looking for, what you bring, end with a friendly "let's talk" line

- [ ] **Step 3: Update current role.** Change The Block end date to May 2026. Add a one-line description of the layoff context if you want to control the narrative ("Role eliminated as part of company-wide restructuring under new CEO; not performance-related"). Optional — many people leave it ambiguous, both work.

- [ ] **Step 4: Add the Superuser Pack** as a "Featured" project with a link to the public GitHub repo.

- [ ] **Step 5: Update photo** if your current one is >2 years old or doesn't match the archetype you're selling. Boston has plenty of professional headshot studios; spend the $200 in week 2.

- [ ] **Step 6: Don't toggle "Open to Work" yet.** Wait until Phase 3 launch (when resume + first MCP server are public). Toggling early without artifacts attracts low-quality recruiter spam and signals desperation.

### Task 2.4: GitHub README pass — the "this is who I am" surface

**Files:**
- Modify: `~/Code-Brain/claude-code-superuser-pack/README.md` (verify it's link-worthy for a hiring manager)
- Create or modify: GitHub profile README at `github.com/<yourusername>/<yourusername>/README.md`

- [ ] **Step 1: Read your Superuser Pack README as a hiring manager would.** Does the first paragraph make them want to look at the second? If not, rewrite the first paragraph. Lead with what it IS and what it DEMONSTRATES, not what it CONTAINS.

- [ ] **Step 2: Add a "Why this exists" section near the top.** One paragraph framing this as your applied agentic-engineering practice, not just a config dump. Karpathy's framing language is your friend here.

- [ ] **Step 3: Pin the repo on your GitHub profile.** Plus the new MCP server repo when it ships. Plus your animation portfolio repo if public.

- [ ] **Step 4: Profile README.** A short bio. Three pinned links: portfolio, Superuser Pack, MCP server (forthcoming). One line under "Currently:" — your AI/Tech/Creative PM pitch in 12 words.

### Task 2.5: Talk track + story bank — what you say in every conversation for the next 8 weeks

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/talk-track.md`
- Create: `vault/20_projects/prj-job-hunt-2026/story-bank.md`

- [ ] **Step 1: Write the 30-second pitch.** "I'm Sean Winslow, a PM with 12 years of design + animation background and the last 2 at The Block where I owned X. I'm focused now on the AI PM space — I've spent the last year building an open-source agentic engineering toolkit and I want to bring that practitioner perspective to a product team. Looking for [archetype], Boston metro or remote." Memorize it. Practice it twice.

- [ ] **Step 2: Write the layoff line.** One sentence, neutral. "The Block did a P&E reorg under their new CEO and reduced headcount across the team — I was part of that group. Not performance-related; cost-cutting. Alex Lebedyev is happy to be a reference." Short. Don't badmouth. Don't over-explain.

- [ ] **Step 3: Write the "why are you a fit" line for each archetype.** Three sentences each. Memorize the first one for AI PM (your top archetype) cold; have the others on a card.

- [ ] **Step 4: Build the story bank.** Eight stories, each fitting the STAR pattern (Situation, Task, Action, Result), 90 seconds each. Suggested set:
  - Block Pro revamp — your flagship (PM craft + influence)
  - ETF page creator skill / project — agentic engineering applied to a real Block need
  - Working with Ed and stakeholders — collaboration + judgment
  - A time you killed your darling — taste + product judgment
  - The 16BitFit pause — recognizing when to stop, strategic patience
  - Superuser Pack architecture — systems thinking
  - A failure with a Block roadmap item — honesty + what you learned
  - Animation portfolio piece — creative range

- [ ] **Step 5: Practice 3 stories out loud once.** Don't memorize verbatim — internalize the beats. Out loud is non-negotiable; reading silently doesn't catch the awkward parts.

---

## Phase 3: Network Activation (Week 1–2, May 5–18) — Track B

### Task 3.1: Reference roster

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/references.md`

- [ ] **Step 1: List 5 references.** Mix of: 1 Block leadership (Alex), 1 Block peer, 1 cross-functional Block partner (eng or design), 1 from prior role, 1 from creative/portfolio side. For each: name, current role, email/Telegram/whatever they use, a 2-line note on what they'll vouch for.

- [ ] **Step 2: Prep each one.** Send a short message — same template — asking if they're game and what's the best contact. Always follow up with a one-pager (Task 3.2) so they have ammunition.

- [ ] **Step 3: Prep the one-pager.** A single page for references: your archetypes, three projects, three accomplishments to highlight, and the kind of role you're looking for. Saves them having to write their own framing.

### Task 3.2: Warm-network outreach — the strategic 20

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/warm-20.md` (table of 20 people)

- [ ] **Step 1: List 20 specific people you'd contact this month.** Not 50 — twenty. Quality > volume. Mix:
  - 5 former colleagues at companies you'd like to work at
  - 5 PM peers in your broader network (not Block)
  - 3 people in AI/agentic-engineering specifically (researchers, founders, devrels)
  - 3 hiring managers or VPs in Boston metro you've crossed paths with
  - 2 recruiters who've reached out in the past 12 months and you respected
  - 2 wildcards (someone you've always meant to talk to)

- [ ] **Step 2: Tier them.** Tier 1 = warmest, contact this week. Tier 2 = reach out in week 2. Tier 3 = week 3+, with a real artifact in hand.

- [ ] **Step 3: Draft one message template, three variants.** Length: 4–5 sentences. Pattern:
  - 1 sentence: hey, here's my situation, brief.
  - 1 sentence: here's what I'm looking for (specific archetype + geography).
  - 1 sentence: here's the artifact / portfolio link / project.
  - 1 sentence: here's what I'd love from you (not "any leads??" — be specific: "any context on your team's hiring priorities?" or "would you be up for a 15-min call?").
  - 1 sentence: low-pressure exit ("totally fine if it's a no — appreciate you either way").

- [ ] **Step 4: Send Tier 1 (8–10 messages) by end of week 1.** Don't do them all at once; spread over 3 days so responses come in waves.

- [ ] **Step 5: Track responses.** Add to the warm-20 table: status (sent / replied / call scheduled / dead) + date.

### Task 3.3: Public announcement decision

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/public-announcement.md`

- [ ] **Step 1: Decide whether and when to post publicly.** Two reasonable strategies:
  - **A: Quiet first 2 weeks**, position privately, then public announcement when LinkedIn + resume + first MCP server are all live. (This is the recommended default.)
  - **B: Announce now**, leverage the natural sympathy + algorithm boost, accept that some early engagement will hit before you're polished.

- [ ] **Step 2: If A: schedule the post for ~May 18 or later.** Set a calendar reminder.

- [ ] **Step 3: Draft the post regardless.** Five short paragraphs. Pattern:
  - 1: factual layoff announcement, no spin.
  - 2: what you valued about The Block (one specific thing — the Pro team, Alex's leadership, the Campus mission, etc.).
  - 3: what you're looking for, archetype + geography + one specific differentiator.
  - 4: what you've been building (link Superuser Pack + first MCP server).
  - 5: how to help — be specific. "If you know of openings in [archetypes] at companies in [list of 5 ideal companies], please connect me."

- [ ] **Step 4: Post when ready.** LinkedIn primary; consider X if your network there is healthy.

---

## Phase 4: Differentiator — Ship Your First MCP Server (Weeks 2–4) — Track C

> **Active Claude-collaboration zone (2026-05-07).** Per the priority shift at the top of this file, Phase 4 is the protected zone for Claude-Code-assisted work. Active deliverables: (a) the `intent-engineering` MCP server v0 ship on 2026-05-25 (unified roadmap Task 3); (b) the portfolio website `/transactions/` route work (unified roadmap Decision 2 — Astro 5 + React islands); (c) the unified roadmap's flagship-artifact lineup — Phase D + Phase 6 `EXPLANATION.md` files (unified roadmap Task 2), the sanitized financial-research fleet 4Q artifact (unified roadmap Task 4), the 14-agent fleet Loom + token-cost calculator (unified roadmap Task 5), and the animation pipeline portfolio short shipping June 11. The unified roadmap holds execution detail; Tasks 4.1–4.4 below remain the deeper specification for the MCP server.

> Karpathy's single-top-recommendation, restated: "Convert your highest-leverage skills to MCP servers, open-source them, and use that ecosystem as your career's portable artifact." This is the move that survives every market scenario.

### Task 4.1: Pick the first MCP server

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/mcp-server-pick.md`

- [ ] **Step 1: Score the five candidates from the synthesis** on (a) effort to build, (b) demonstrability for hiring managers, (c) reusability outside your own life. The five candidates:
  - `granola-meeting-notes-processor` — clearly reusable, low effort
  - `intent-engineering` — your differentiated IP, medium effort, highly demonstrable
  - `the-block-jira-ticket-writer` — sanitize to "PM-ticket-writer-with-style-guide," medium effort
  - `etf-page-creator` — sanitize to "structured-content-publisher," medium effort, less demonstrable
  - `writing-voice-modes` — calibrated, runs anywhere, medium effort

- [ ] **Step 2: Pick one.** Recommendation: **`intent-engineering` MCP server.** It's your most differentiated piece of IP, it directly demonstrates AI-PM thinking, and the demo is "agent reads your spec and tells you what's missing" — visceral and easy to show on a screenshare. Granola is more obviously useful but less personal IP.

- [ ] **Step 3: Define the v0 scope in one paragraph.** What tools does it expose? (e.g., `analyze_intent_spec`, `generate_intent_spec_template`, `audit_existing_spec`.) What resources? (e.g., a small library of canonical intent specs.) Keep it tight. v0 ships before v1.

- [ ] **Step 4: Acceptance criteria for v0:**
  - Runs locally via stdio transport
  - Demoable from Claude Desktop with one config-file change
  - README has a 30-second "what it does" + 5-minute "set it up yourself" + a 3-line example transcript
  - Repository is public, MIT licensed, with sensible commit history

### Task 4.2: Spike — get any MCP server running locally

**Files:**
- Create new repo: `~/Code/sw-mcp-intent-engineering/` (or wherever your code lives)
- Create: `package.json`, `tsconfig.json`, `src/index.ts`

- [ ] **Step 1: Read the spec.** Use the `claude-api` skill or fetch the MCP TS SDK docs via context7. This is plumbing — don't freeform it.

- [ ] **Step 2: Scaffold a minimal MCP server.** Pin Node 22+, TypeScript 5+, `@modelcontextprotocol/sdk`. One tool that returns "hello from intent-engineering." Get this running in Claude Desktop before you write any business logic. Don't skip this step — wiring is half the work, not the last 5%.

- [ ] **Step 3: Verify it loads in Claude Desktop.** Update `claude_desktop_config.json`, restart, see your tool listed. Run it. See "hello." Commit.

### Task 4.3: Implement v0 of the actual server

**Files:**
- Create: `src/tools/analyze_intent_spec.ts`, `src/tools/generate_template.ts`, `src/tools/audit_spec.ts`
- Create: `src/resources/canonical-specs/*` (3–5 sample specs)
- Create: `tests/` with at least one integration test

- [ ] **Step 1: Port the intent-engineering skill prompt** into a structured tool. The skill content becomes your tool description + system prompt. Keep the IP — don't water down the framework, just make it callable.

- [ ] **Step 2: Implement `analyze_intent_spec(spec_text)`** — takes a string, returns structured assessment (autonomy level, anti-patterns flagged, missing fields, suggested rewrites).

- [ ] **Step 3: Implement `generate_template(role, autonomy_level)`** — returns a markdown intent-spec template scoped to the use case.

- [ ] **Step 4: Implement `audit_existing_spec(file_path)`** — reads an existing spec from the user's filesystem, runs the analyzer, returns a diff-style report.

- [ ] **Step 5: Write 3–5 canonical specs as resources.** Drawn from your existing skill examples. Sanitize anything Block-specific.

- [ ] **Step 6: One integration test per tool.** Run via `vitest`. Each test: invoke the tool with a fixture input, assert structural properties of the output.

- [ ] **Step 7: README.** Sections: What this is (1 paragraph) → Why MCP (1 paragraph + Karpathy reference) → Quickstart (5 commands) → Tools reference (auto-generated or manual) → Examples (3 transcripts) → Roadmap (be honest about what's not done) → License.

- [ ] **Step 8: Demo video.** 90-second Loom or asciinema recording. Show: setup, three tool invocations, the value moment. This is the artifact you'll send to hiring managers.

- [ ] **Step 9: Publish.** Push to GitHub public. Pin on profile. Add to LinkedIn featured. Add to Superuser Pack README as "MCP server adjacent to this skill."

- [ ] **Step 10: Announce.** A focused tweet/LinkedIn post linking the repo and a one-line value prop. Tag relevant accounts (Anthropic, MCP folks, Karpathy if it's not too tryhard). Don't overdo announcements — one is enough; the repo is the product.

### Task 4.4: Track usage and iterate

**Files:**
- Modify: `README.md` of the MCP server repo, `vault/20_projects/prj-job-hunt-2026/mcp-feedback.md`

- [ ] **Step 1: Ask 3 specific people to try it.** Two PMs in your network + one engineer. Send the demo video + setup steps. Ask for honest reaction.

- [ ] **Step 2: Log feedback.** Each piece of feedback is a row in a table: who, what, action you took (or didn't, with reason).

- [ ] **Step 3: Ship v0.1 or v0.2** if anything actionable comes back. Don't get stuck polishing — every iteration is a star on the repo and a touchpoint with the person who gave feedback.

---

## Phase 5: Application Pipeline (Weeks 2+, ongoing) — Track B

### Task 5.1: Target company list — the strategic 30

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/target-companies.md`

- [ ] **Step 1: List 30 companies.** Tiers:
  - **Tier 1 (10): "yes please"** — companies you'd be genuinely excited to join. Mix of AI-native (Anthropic, OpenAI, Cursor, Cognition, Anysphere, Replit), AI-adjacent media/data (Bloomberg, Reuters, Politico, Stripe), Boston-local (HubSpot, Klaviyo, Wayfair, Toast).
  - **Tier 2 (15): "would consider"** — solid, just less of a perfect fit
  - **Tier 3 (5): "safety net"** — places where the role is good even if the company isn't your dream.

- [ ] **Step 2: For each Tier 1 company, identify ≥1 inside contact.** LinkedIn first connection or 2nd-degree warm intro. Note them. This determines which you actually apply to first.

- [ ] **Step 3: Track openings.** Use a single source of truth — the spreadsheet/markdown table. Columns: Company, Role, Source, Date Posted, Date Applied, Status, Inside Contact, Next Action, Notes.

### Task 5.2: Application cadence — the rhythm

**Files:**
- Update weekly: `vault/20_projects/prj-job-hunt-2026/applications.md` (the master table)

- [ ] **Step 1: Set the cadence.** 5 quality applications per week. Not 25. Quality means: tailored resume, personalized cover note, ≥1 paragraph that proves you read the JD, ideally an inside-contact ping concurrent with the application.

- [ ] **Step 2: Tuesday and Thursday mornings (8:30–10:30 AM)** are application slots. Block on calendar. Write the deep work on those days; submit by Friday EOD.

- [ ] **Step 3: Cover note template.** Three short paragraphs.
  - P1: why this specific company / role / team caught your attention (proof you read it).
  - P2: what you bring — link to one concrete artifact (MCP server repo / Superuser Pack / animation piece — pick the one that fits).
  - P3: short, friendly close.

- [ ] **Step 4: Inside-contact message.** Sent same day as the application. Pattern: "Hey [name] — applying for [role] at [company]. Wanted to flag it in case there's any context worth me knowing or anyone on the team you'd suggest I connect with. Either way, no pressure — appreciate you."

- [ ] **Step 5: Recruiter triage.** Inbound recruiters from "Open to Work" toggle (once on) — apply this filter:
  - Title in your archetype list? Continue.
  - Salary range mentioned ≥ walk-away? Continue.
  - Remote OR Boston metro? Continue.
  - Otherwise: polite "not the right fit, here's what I'm looking for" + thank them.
  - Continue list: 30-min screening call. If it advances, log in the application table.

### Task 5.3: Pipeline health check — weekly

**Files:**
- Modify weekly: `vault/20_projects/prj-job-hunt-2026/applications.md`

- [ ] **Step 1: Friday 4:30 PM retro** (already on calendar from Phase 0). Review the table. Three numbers:
  - Applications submitted this week (target: 5)
  - Active conversations this week (target: 3+)
  - Interviews scheduled or completed this week (early: 0–1, mid-search: 2–4)

- [ ] **Step 2: One-line entry to `prj-job-hunt-2026/README.md` "Weekly Retro" section.** What worked, what stuck, one thing to change next week.

- [ ] **Step 3: At week 4, evaluate the funnel.** If 20 quality applications in and <3 phone screens, the resume + positioning need a rewrite, not more applications. If lots of phone screens but no advancement, story bank needs work. If lots of late-stage rejections, target archetype may be misaligned.

---

## Phase 6: Interview Readiness (Weeks 3+, as interviews land) — Track B

### Task 6.1: Interview prep system

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/interviews/<company>-<role>.md` per interview loop

- [ ] **Step 1: One file per interview loop.** Top section: company research notes (mission, recent news, product launches, team structure, glassdoor signals). Middle: per-round prep (interviewer name, role, format). Bottom: questions you'll ask them (memorized — never go in without 5 ready).

- [ ] **Step 2: Standard prep block.**
  - Company: 30 minutes of reading their last 3 product launches, last 6 months of blog posts, their PM JD if available
  - Interviewer: LinkedIn — what's their background, what might they care about
  - Format: clarify with recruiter — case study? technical deep-dive? portfolio walkthrough?
  - Stories: pick 3 from the bank that fit this loop's emphasis

- [ ] **Step 3: Practice the technical / portfolio walkthrough on your own.** Out loud, with a screen recording, once. Watch it back. Painful and necessary.

### Task 6.2: PM case study reps

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/case-study-reps/`

- [ ] **Step 1: Practice 5 PM case studies before the first real one.** Examples:
  - "Design Bloomberg Terminal but for an AI agent consumer."
  - "Walk me through how you'd 0→1 a personal AI assistant for crypto research."
  - "Your model error rate is up 15% this week. What do you do?"
  - "How would you build a Karpathy-style intent spec for [product X]?"
  - "Tell me about a product you wish existed."

- [ ] **Step 2: Record one case study answer end-to-end.** Watch yourself. Cringe. Improve.

- [ ] **Step 3: Mock interview with one trusted PM friend.** Real conditions. Real feedback. Worth its weight in gold.

### Task 6.3: Salary negotiation prep

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/target-archetypes.md` (your three numbers from Task 2.1)

- [ ] **Step 1: Read one negotiation post.** Patrick McKenzie's "Salary Negotiation: Make More Money, Be More Valued" is canonical. 1 hour of reading saves you tens of thousands.

- [ ] **Step 2: Practice the "what are you looking for?" answer.** Don't volunteer a number first. "I'm focusing on the role fit and team at this stage; happy to align on comp once we both think there's a match." If pushed: "Based on my research for [archetype] roles in [geo], I'm targeting [target number]. Open to discussing the full package." Memorize it.

- [ ] **Step 3: Decision matrix for offers.** Fields: base, equity (with assumptions stated), bonus target, sign-on, location/remote terms, level/title, manager quality (qualitative), product mission alignment, runway concerns. When the first offer lands, fill it in. Don't try to think about it from scratch under pressure.

---

## Phase 7: Daily + Weekly Rhythm — Sustainability

> The biggest risk is not the job market. It's burnout from grinding 10 hours/day for 6 weeks and then being too cooked to interview well in week 7. Pace.

### Task 7.1: Daily structure

**Files:**
- Existing: `vault/10_timeline/daily/YYYY-MM-DD.md` (your daily-driver agent already creates these)

- [ ] **Step 1: Morning shift, 8:30 AM–12:30 PM.** Job hunt deep work. One of three blocks per day:
  - Mon/Wed: Track A (logistics) + Track B (positioning)
  - Tue/Thu: Track B (applications)
  - Fri: Track C (MCP server / portfolio work) + retro

- [ ] **Step 2: Afternoon, 1:30–4:30 PM.** Flexible. Track C work, network calls, life admin, exercise, errands. NOT more job hunt — variety preserves energy.

- [ ] **Step 3: Evening hard stop, 5:30 PM.** This is hard. The point of the layoff is not "now I work 12 hours alone in the apartment." Pick a hard cutoff, stick to it.

- [ ] **Step 4: Weekend rule:** one half-day of optional work, otherwise off. Use weekends to refill.

### Task 7.2: Weekly retrospective (Friday 4:30 PM)

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/README.md` "Weekly Retro" section

- [ ] **Step 1: Numbers** — applications submitted, active conversations, interviews this week. Three integers.

- [ ] **Step 2: One thing that worked.** Repeat next week.

- [ ] **Step 3: One thing that didn't.** Change next week.

- [ ] **Step 4: One non-job-hunt win.** Animation pipeline progress, a workout streak, a meal cooked, a visit with Maryalice. Counterbalance is essential.

- [ ] **Step 5: One sentence for next week's headline goal.** Write it tonight; wake up Monday already aimed.

### Task 7.3: Mental health bumpers

**Files:**
- (No file — these are routines, not deliverables)

- [ ] **Step 1: Move every day.** Walk, gym, climb, whatever. Non-negotiable. Your existing `health-habits` skill can help if you want it gamified.

- [ ] **Step 2: One social interaction per day** that isn't job-hunt related. Coffee with a friend, call your mom, gym banter — counts.

- [ ] **Step 3: Therapy or coach if you have one.** If you don't and the spiral gets bad, BetterHelp or Talkspace are reasonable bridges. The Block had an EAP — check if it extends through severance period.

- [ ] **Step 4: Recognize the milestones that aren't offers.** First MCP server shipped. First public LinkedIn post. First inbound recruiter. First on-site. Each one is a real signal, not just a step toward "the real win."

---

## Phase 8: Acceptance + Off-ramps (Week 6+, when offers land)

### Task 8.1: Offer evaluation

**Files:**
- Create: `vault/20_projects/prj-job-hunt-2026/offers/<company>-offer.md`

- [ ] **Step 1: Use the matrix from Task 6.3.** Fill it in immediately when the offer lands. Don't make decisions in your head.

- [ ] **Step 2: Always negotiate.** Even if the first number is at your target. Polite, factual. "I'm excited about the role. The total comp is in the right range; I was hoping to land closer to [X], based on [reason — competing offer, market data for this archetype, sign-on flexibility]. Is there room?"

- [ ] **Step 3: Ask for 1 week to decide.** Standard ask, standard accept.

- [ ] **Step 4: Talk to the team again.** Manager, future peers, ideally a skip-level. Pre-decision. Companies that say no to this are red-flagging themselves.

### Task 8.2: Wind-down of the search

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/README.md`

- [ ] **Step 1: When you sign:** withdraw open applications gracefully. Send a thank-you to every recruiter who got you to phone screen. Decline every active loop with a personal note. Maintain the network.

- [ ] **Step 2: Write a public win post.** Brief, gracious. Tag the people who helped. The next person in your situation will see this; that's worth doing well.

- [ ] **Step 3: Close out the project.** Move `prj-job-hunt-2026/` from `20_projects/` to `40_archive/` once you're 30 days into the new role and confident it's settled.

- [ ] **Step 4: One-month retro on the job hunt itself.** What would you do differently? Save it — you'll be glad to have it the next time, in 3 or 5 or 10 years.

---

## Self-Review

**Spec coverage:** All four user-stated goals are addressed.
- Turn the news into motivation → Phase 0 + Phase 7 (rhythm)
- Generate artifacts to land a PM role → Phase 2 + Phase 4
- Targets AI / Tech / Creative PM, Boston or remote → Phase 2 archetype work + Phase 5 target list
- "I can't be as picky" → Phase 5 has Tier 1 / 2 / 3 explicitly + safety-net layer

**Placeholder scan:** A few placeholders remain by design — your specific salary numbers, your specific 30 companies, your specific 20 contacts. These can't be filled in for you. Every other step has concrete content.

**Type consistency:** Track A / B / C labels are used consistently. Phase numbers are sequential. File paths follow your existing vault structure. Timeline references are anchored to May 4, 2026 = day 1.

**Worth flagging where I made judgment calls:**
- Recommended **signing the severance** (Task 1.1.4) and **ACA over COBRA** (Task 1.2.5) as defaults — these are the right calls for ~85% of people in your situation but you should still verify with your specific facts.
- Recommended **`intent-engineering` as your first MCP server** (Task 4.1) over the alternatives — it's the most differentiated; happy to argue this if you want a different pick.
- Recommended **AI PM > Tech PM > Creative PM** ranking (Task 2.1.2) — this is calibrated to current market + your stated open-mindedness; reverse it if your gut says creative is still the heart-thing.
- Built in a **hard 5:30 PM stop** (Task 7.1.3). You will want to ignore this. Don't.

---

## Execution Handoff

Plan complete and saved to `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md`.

Most of this plan is human work — phone calls, decisions, conversations, judgment. It is not code that a subagent can crank through. **The exception is Phase 4 (the MCP server)** — that is genuinely subagent-friendly work and I'd be happy to dispatch fresh subagents per task with review between them when you're ready to start it.

Two natural starting points right now:

1. **Tonight (Phase 0 only).** Cut the panic loop, set up tracking, tell the three people. Stop. Sleep. Begin Phase 1 tomorrow. Strongly recommended for a Monday-evening-after-getting-laid-off start.

2. **Tomorrow morning (Phase 1, Task 1.1 + 1.3 first).** Severance review prep + unemployment claim are the two highest-EV moves. Both can be done in 90 minutes total.

Tell me when you want to start Phase 4 — that's where I can directly help with code via subagents. For Phases 0–3, the most useful thing I can do is be a sounding board: when you're drafting your LinkedIn paragraph or the warm-20 message template, paste it back and I'll give honest feedback.

You're going to land somewhere good. Onwards.
