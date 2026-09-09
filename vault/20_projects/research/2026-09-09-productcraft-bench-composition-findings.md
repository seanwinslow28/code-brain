---
title: "Productcraft bench composition — research findings (pass 1, L4 gate)"
date: 2026-09-09
project: productcraft
status: ratified-2026-09-09
tags: [research, productcraft, bench-composition, product-org]
cost: $0 (last30days local lanes + web research; no Gemini DR API spend; the optional subscription Deep Research run was judged unnecessary — four web sweeps returned 97 primary sources)
models: "last30days sweep: Sonnet 5 · SVPG, Reforge/Lenny, curricula, analytics-role sweeps: Opus 5 (analytics-role relaunched once after a stall) · synthesis, seventh-seat ruling, audit cycle: Fable 5.1"
---

# Productcraft bench composition — findings brief

**Gate:** L4 — the six-seat bench is a baseline hypothesis; this pass confirms, adds, or cuts seats before build, and rules on the seventh Insights & Analytics seat. It also proposes the audit cycle.

**Method ($0):** three `last30days` passes (social lanes returned near-zero relevant signal — a negative finding recorded below) plus four primary-source web sweeps: SVPG's essays and the three Cagan tables of contents (21 sources), Reforge's competency and specialization pages plus Lenny's surveys (26), fifteen PM curricula with published module lists (27), and how real product orgs staff analytics (23). Raw sweep files are session-local; this brief holds the findings and citations.

## Headline recommendation

**Keep all six seats. Add the seventh — Insights & Analytics — but as the studio's evidence seat, shaped like Systemcraft's Evals & Evidence Architect: it designs metrics and grades evidence, co-signs the Discovery Lead's evidence and audits the Growth seat's experiments, and never makes a product decision.** Adopt two boundary adjustments (positioning stays with the Strategist; OKR outcomes are co-signed by the Strategist, the roadmap belongs to Delivery). Run the seven seats as a sequential pipeline with two closed audit cycles.

## Findings

### 1. The frameworks divide the work on a different axis than the bench — and that is already settled

SVPG divides product work by **risk owned inside one cross-functional team** (value and viability to the PM, usability to design, feasibility to the tech lead), not by activity: "A typical cross-functional product team requires three specific and very distinct skill sets" (svpg.com/product-model-competencies). Reforge's twelve competencies vary by **seniority**, not by seat (ravi-mehta.com/product-manager-skills). Lenny's canonical job description is three verbs — shape, ship, synchronize — not six roles (lennysnewsletter.com/p/what-is-product-management).

That mismatch is structural and applies to every seat equally. The bench is not an org chart with seven headcount; it is one PM's toolset, split into artifact-owning stages so each stage can be grounded in its own canon and audited by a different one. The L4 lock already made that choice. So the test for each seat is not "would Cagan staff it" but the Systemcraft test: **is it a distinct knowledge domain, with its own artifact, its own canon, and its own audit duty?** (the diversity-delays-saturation finding in the Systemcraft bench brief).

### 2. Seat by seat

| Seat | Ruling | Evidence for | Evidence against | Adjustment |
|---|---|---|---|---|
| **Product Strategist** | **Confirm** | Own module in 11 of 15 curricula; Reforge's "Product Strategy" competency group (Business Outcome Ownership, Vision & Roadmapping, Strategic Impact); SVPG makes vision and strategy the product leader's core duty | SVPG places *positioning* in product marketing, not product management (svpg.com/product-management-vs-product-marketing) | Positioning stays here: Dunford's method treats POV and positioning as one craft; Growth owns *distributing* it |
| **Discovery Lead** | **Confirm** | Own module in 10 of 15; SVPG: "the product manager's primary responsibility is discovery"; Torres's continuous-discovery canon is distinct and SVPG-recommended | No framework has a standalone discovery *role* — Reforge splits it across Core PM and Innovation PM; SVPG makes it a whole-team activity | None. Its evidence section gets a dual-touch co-sign from the Insights seat (finding 3) |
| **Growth & Distribution Architect** | **Confirm** | Cleanest one-to-one in any framework: Reforge Growth PM ("sign up/registration, onboarding, conversion/monetization, pricing, referrals, retention"); Lenny's growth-team roster; own module in 8 of 15 | SVPG has no growth role anywhere — zero of 482 essay slugs; nearest concept is "product optimization techniques," a PM skill | Boundary with Business: Growth owns monetization *loops* and conversion; Business owns pricing *design* (finding 2, Business row) |
| **Business & Economics Modeler** | **Confirm, flagged tool-poor** | SVPG: viability is half the PM's risk ownership, and "the economics of your product" is non-delegable knowledge; every university program longer than two days gives it its own unit (CMU, Stanford, Kellogg, eCornell 360) | Weakest framework support: no role in SVPG or Reforge (pricing sits in Growth PM at Reforge, P&L in Lenny's GM model); only 7 of 15 curricula; **only 4 installed pm-* skills route here, with no unit-economics or business-case tool** (pass 3) | Keep. It is Systemcraft's Ops & Economics analogue. Its templates (unit-economics model, business case) must be authored, not borrowed |
| **Delivery & Execution Lead** | **Confirm** | Own module in 11 of 15; Reforge's "Product Execution" group is the early-career critical path; SVPG endorses a separate Delivery Manager role | SVPG scopes that role to impediments and production support only, rejects roadmaps as the thing the product model replaces, and has "stopped recommending" OKRs in most companies; two curricula file OKRs under strategy-translation, not delivery | OKR *outcomes* are drafted by the Strategist and owned jointly; Delivery owns the outcome roadmap, stories, plans, release notes, retros. Delivery never sets a goal the Strategist has not signed |
| **Product Leadership & Org Designer** | **Confirm** | Closest SVPG match of the six: product leaders own coaching, vision, strategy, and "a carefully crafted team topology"; EMPOWERED's whole structure is this seat decomposed; present in every leader-tier curriculum (Product School PLC gives it 4 of 12 modules) | Reforge treats leadership as *breadth across work types*, not a peer seat; absent from every foundations-tier curriculum; **thinnest free canon of any seat, nothing purpose-built** (pass 2) | Keep, with the hard artifact contracts L3 locked. This is a book-carried lane (Grove, Bryar & Carr, Cagan) the way Systemcraft's Interaction & Trust lane is free-canon-carried |

**Not added, with why:** Reforge's *Platform PM* (trust, payments, data infrastructure, ML, build-vs-buy) routes to Systemcraft by L2. Reforge's *Innovation PM* (0→1, PMF expansion) is the Strategist and Discovery Lead working together, not a seat. *Design/UX* (own module in 7 of 15) belongs to the future Designcraft team named in L10. *Technical/AI fluency* (7 of 15) is Systemcraft's whole mandate.

### 3. The seventh seat: Insights & Analytics — ruling and reasoning

**The question:** is analytics a distinct knowledge domain with its own artifact, canon, and audit duty, or a lane Discovery and Growth can share?

**Evidence it is distinct:**
- It is the **single most-isolated area in formal PM education**: its own named module in 12 of 15 curricula, more often than strategy (11) or discovery (10). Five of eCornell 360's fourteen core courses are data courses.
- It has a **distinct book canon that never appears on growth reading lists** — Kohavi, Tang & Xu; Rodrigues; Georgiev; Hubbard — and the overlap with growth is exactly two titles, *Lean Analytics* and *The Lean Startup* (pass 2). The overlap with discovery is nil.
- Real orgs staff it as a named function: GitLab runs Product Analyst as a **peer job family to PM** and names one person "Technical DRI for the Product Key Performance Indicators" (handbook.gitlab.com/job-families/product/product-analyst); Spotify and UserTesting merge quant and qual under one "Insights" line; Figma keeps them split and pays for synthesis with scheduled ritual. The one prevalence number found, 45.1% of companies with a dedicated product-analytics team (Product-Led Alliance 2025, n undisclosed, likely biased upward), says it is common but not universal.
- On growth teams specifically, the analyst is a **separate seat from the Growth PM** on Lenny's roster (lennysnewsletter.com/p/how-to-hire-your-first-growth-team).
- **Twelve installed pm-* skills route to it** (SQL, cohorts, A/B analysis, dashboards, sentiment) — a skill with no owning seat is a skill nobody routes to (pass 3).
- Even Cagan's endorsed Product Ops model **is** an insights function: "Quantitative Insights / Qualitative Insights / Tools" sitting "at the same level as Product Management and Product Design" (svpg.com/product-ops-overview).

**Evidence against a seat, and how the design answers it:**
- SVPG: data knowledge "is not something that can be delegated," and insights teams "are there to help product teams and product leaders to make informed decisions, not to make those decisions for them." Reforge never names analytics a PM specialization; it is an embedded competency plus a partner data team. → **The seat produces measurements, never decisions.** That is exactly Systemcraft's Evals rule: measurements are Evals', thresholds are Ops'. The Insights seat designs the metrics and grades the evidence; the Strategist, Growth, and Business seats decide on it; Sean decides above them.
- Systemcraft's bench brief: five seats is the top of the sensible range; every seat past that buys mostly coordination tax. → **Seven is a real cost and this brief says so.** Mitigation: the Insights seat runs as a co-sign-and-audit seat more than a drafting stage (again the Evals pattern), so it does not add a full stage to the train; the pipeline stays sequential with full-artifact handoff; and the seat closes the one gap the shared-lane design leaves open (next point).
- The shared-lane alternative (Discovery qualitative, Growth quantitative) has a **self-grading hole**: the Growth seat would design its experiments and read its own results. Systemcraft's rule — the seat who designs a test never grades it — has no owner without this seat. Torres's own practice confirms the need from the discovery side: she invented a strength-of-evidence model to grade the *inputs* to an opportunity tree, and found roughly eight story-based interview sets in 500 uploads (pass 4). Grading evidence is its own craft.

**Ruling: add the seat.** Name it *Insights & Analytics*. Artifact: the metrics and evidence plan (north-star and input metrics, instrumentation requirements per SVPG's non-negotiable, evidence-strength grading of discovery inputs, experiment analysis). Dual-touch: it co-signs the Discovery Lead's evidence section before the opportunity tree is handed forward. Audit duty: the Growth seat's experiment designs. Law: it never makes a product decision.

### 4. Audit cycle (proposal)

Pipeline order follows the artifact chain: **1 Strategist → 2 Discovery → 3 Insights → 4 Growth → 5 Business → 6 Delivery → 7 Leadership.** Every audit is a fresh-context invocation that sees artifacts only, never the drafting conversation (Systemcraft rule, ratified 2026-08-22). One auditor per artifact; two closed cycles, mirroring Systemcraft's own 3-cycle plus 2-cycle shape.

| # | Seat | Produces | Audits | Audit stake |
|---|---|---|---|---|
| 1 | Product Strategist | Strategy and POV doc (vision, positioning, strategic bets, OKR outcomes) | Leadership's decision memo | Does the decision follow the strategy, and is why-A-over-B honest? |
| 2 | Discovery Lead | Discovery plan + opportunity solution tree + evidence | Strategist's strategy/POV | Is the POV grounded in customer evidence, or in the founder's wish? |
| 3 | Insights & Analytics | Metrics and evidence plan; co-signs Discovery's evidence (dual-touch) | Growth's growth model and experiments | Designer never grades: are the experiments measurable, powered, and honestly read? |
| 4 | Growth & Distribution Architect | Growth model + GTM plan | Business's business case | Do the unit economics survive the real acquisition channels and retention curve? |
| 5 | Business & Economics Modeler | Business case + pricing/packaging + unit-economics model | Delivery's outcome roadmap | Does the sequencing protect payback and cash, or front-load cost? |
| 6 | Delivery & Execution Lead | Outcome roadmap + OKR translation + stories/plans/release notes/retros | Insights' metrics plan | Is every metric instrumentable and shippable, not vanity? |
| 7 | Product Leadership & Org Designer | Stakeholder map + decision memo + operating-model doc | Discovery's discovery plan | Can this org actually run continuous discovery, and who will resist it? |

Cycles: Strategist → Leadership → Discovery → Strategist (3-cycle); Insights → Growth → Business → Delivery → Insights (4-cycle). Every seat audits exactly one artifact and is audited by exactly one peer.

**The red-team gate stays a protocol, not a seat** (Systemcraft precedent): milestone gates on Codex at strategy sign-off, before the Systemcraft handoff, and at close.

### 5. Negative findings, stated

- The social lanes (Reddit, X, YouTube, last thirty days) returned almost nothing usable for these questions: every pass tripped the engine's relevance floor. These are newsletter- and syllabus-shaped questions. Future passes of this shape should go straight to primary-source sweeps.
- No public survey gives the share of companies with product ops, product analysts, or growth teams by company size. The 45.1% figure stands alone and undisclosed.
- No live "Cagan versus Reforge" competency debate surfaced. The two frameworks differ by construction (risk-owned versus seniority-leveled), not by argument.
- Several primary pages were unreachable this session (Reforge direct fetch, Stanford GSB, HBS catalog, Amazon and Google APM role pages); Reforge was read through a text proxy with canonical URLs cited.

## Evidence strength

- **Strong** (multiple independent primary sources): analytics as an isolated discipline in curricula and org practice; growth as a distinct specialization; leadership as audience-gated; the frameworks' different dividing axes.
- **Moderate**: the self-grading argument for the Insights seat (an inference from Systemcraft's ratified rule plus Torres's practice, not a controlled study); Business seat's role status (thin framework support, strong canon).
- **Weak**: the 45.1% prevalence figure; any "2026 trend" claim from the social lanes.

## Decisions requested (Sean)

1. Ratify the seven-seat roster: the six confirmed, plus Insights & Analytics as the evidence seat that measures and never decides.
2. Ratify the two boundary adjustments: positioning with the Strategist; OKR outcomes co-signed by the Strategist, roadmap owned by Delivery.
3. Ratify the audit cycle in finding 4, with the red-team gate remaining a Codex-run protocol.

## Key sources

svpg.com/product-model-competencies · svpg.com/product-ops-overview · svpg.com/the-product-manager-contribution · svpg.com/the-role-of-analytics · svpg.com/product-management-vs-product-marketing · svpg.com/the-delivery-manager-role · svpg.com/team-objectives-overview · Wiley tables of contents for INSPIRED, EMPOWERED, TRANSFORMED · ravi-mehta.com/product-manager-skills · reforge.com/blog/product-manager-skills · reforge.com/blog/product-specializations · reforge.com/blog/crossing-the-canyon-product-manager-to-product-leader · lennysnewsletter.com/p/what-is-product-management · lennysnewsletter.com/p/how-to-hire-your-first-growth-team · lennysnewsletter.com/p/product-management-career-ladders · Product School PMC/PLC/AIPC module pages · Pragmatic Institute framework PDF · Kellogg AI-Enabled PM certificate (20 modules) · CMU MSPM curriculum · Stanford Online PM program · eCornell PM and PM360 · handbook.gitlab.com/job-families/product/product-analyst · amplitude.com/blog/hire-product-analyst · amplitude.com/blog/webinar-recap-ronny-kohavi · kameleoon.com/blog/what-center-excellence-experimentation · thdpth.com/p/kill-your-data-team-why-product-teams · productledalliance.com/state-of-product-analytics-report-2025 · optimizely.com/insights/blog/data-analysts-vs-product-analysts-vs-pms · Systemcraft bench-composition brief (2026-08-22) for the seat test and audit doctrine.

## Decision record (ratified by Sean, 2026-09-09)

1. **Ratified:** seven-seat roster — the six baseline seats confirmed, plus **Insights & Analytics** as the studio's evidence seat: it designs metrics, grades evidence strength, and reads experiments; it co-signs the Discovery Lead's evidence (dual-touch) and audits the Growth seat's experiments; **it never makes a product decision.**
2. **Ratified:** the two boundary adjustments — positioning stays with the Product Strategist; OKR outcomes are co-signed by the Strategist while Delivery owns the outcome roadmap.
3. **Ratified:** the audit cycle in finding 4 (Strategist → Leadership → Discovery → Strategist; Insights → Growth → Business → Delivery → Insights), every audit fresh-context on artifacts only; the red-team gate remains a Codex-run protocol, not a seat.
