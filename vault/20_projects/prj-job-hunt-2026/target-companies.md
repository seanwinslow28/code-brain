---
type: tracker
project: prj-job-hunt-2026
created: 2026-05-13
last_updated: 2026-05-13
status: active
linked_research:
  - "[[2026-05-07-target-role-specs]]"
  - "[[2026-05-06-unified-roadmap]]"
linked_artifacts:
  - "[[job_feed]]"
  - "[[warm-intros]]"
ai-context: "Strategic-30 target list per master plan Phase 5 Task 5.1 + roadmap Task 6 §E. Source intelligence: Gemini DR-Max research 2026-05-07. Application tracking schema. Tier 1 = 'yes please' / Tier 2 = 'would consider' / Tier 3 = 'safety net + wildcards'. Status mutations: applied / talking / interview / passed / rejected / offer. Featured Artifact column pulls from DR §5 Portfolio-to-Role Mapping."
---

# Target Companies — Strategic 30

**Goal:** 5 quality applications per week (master plan Phase 5 Task 5.2), Tue + Thu mornings 8:30–10:30 AM. Front-load Tier 1 + Tier 3 wildcards (Anthropic FDE, Sierra, Decagon) because they take longer in pipeline.

**Intelligence source:** [[2026-05-07-target-role-specs]] — Gemini DR-Max, 16 roles fully spec'd with JD URLs, comp ranges, hiring-manager telemetry, portfolio-to-role mapping. Tiers below are reorganized vs. DR's tenure-fit tiering — these use the master plan's "yes please / would consider / safety net" framing weighted by Boston-metro + remote constraint + portfolio match.

**Discovery loop:** [[job_feed]] agent polls 38-company watchlist daily at 8:00–11:00 AM ET. New roles surface in `vault/20_projects/prj-job-hunt-2026/job-feed/<date>.md`. When a feed hit matches a target company below, update the row's `Status` + `Date Applied`.

**Status legend:**

| Status | Meaning |
|---|---|
| `not-applied` | Target identified, not yet applied |
| `applied` | Application submitted |
| `talking` | Recruiter / hiring manager outreach in progress |
| `interview` | In active interview loop |
| `offer` | Offer extended |
| `passed` | Sean declined to apply (location, comp, fit) |
| `rejected` | Company declined |
| `tbd` | Role not currently posted; monitor via job_feed |

---

## Tier 1 — "Yes please" (10)

Apply Weeks 2–3. Mix of remote (Glean, Pair, Cohere) + Boston (HubSpot, Liberate, Manifold, Klaviyo, BCG X) + the Anthropic Boston FDE crown jewel.

| # | Company | Role | Loc / Policy | Comp | Status | Date Applied | Inside Contact | Featured Artifact | Notes / JD |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Anthropic** | Forward Deployed Engineer | Boston, 1–2 days/wk | $280–320k (NY equiv) | not-applied | — | — | `intent-engineering` MCP server | JD literally asks for "MCP servers, sub-agents, agent skills" — direct match. [Greenhouse](https://job-boards.greenhouse.io/anthropic/jobs/4985877008) |
| 2 | **Glean** | Forward Deployed PM | Remote-US | $170–280k | not-applied | — | — | 14-agent SDK fleet | "0-to-1 product creation" + "shipped AI in production." [Greenhouse](https://job-boards.greenhouse.io/gleanwork/jobs/4651950005) |
| 3 | **Pair Team** | Senior Product Manager | Remote-US | $140–180k est | not-applied | — | — | `intent-engineering` MCP + financial-research fleet (HIPAA parallel) | "Use AI tools to ship prototypes." 4+ yrs PM listed, pitch portfolio velocity. [startup.jobs](https://startup.jobs/senior-product-manager-pair-team-6968549) |
| 4 | **HubSpot** | PM, Voice Intelligence | Boston / Remote | $140–170k est | not-applied | — | — | 14-agent SDK fleet | Boston anchor + remote-flexible. Gap: voice/STT-TTS depth. [BuiltInBoston](https://www.builtinboston.com/job/product-manager-voice-intelligence/8892823) |
| 5 | **Liberate** | Sr. AI Agent PM (FDP) | Boston / SF 2-day | $160–235k | not-applied | — | — | 14-agent SDK fleet (cost governors) | Insurance-vertical agent automation. 4–7 yrs floor; pitch agent architecture. [Greenhouse](https://job-boards.greenhouse.io/liberate/jobs/5200882008) |
| 6 | **Manifold Bio** | AI Product Manager | Boston, MA | $120–150k | not-applied | — | — | Animation pipeline + MCP | Boston biotech AI; foundation models + reasoning agents. Gap: biotech domain. [TheLadders](https://www.theladders.com/job/ai-product-manager-manifold-bio-boston-ma_86793499) |
| 7 | **Klaviyo** | Sr. PM, AI (Customer Agent) | Boston, 3 days/wk | $136–204k | not-applied | — | — | Multi-agent retrieval + synthesis | At edge of 3-day cap. Gap: e-commerce mar-tech. [WelcomeToJungle](https://www.welcometothejungle.com/en/companies/klaviyo/jobs/senior-product-manager-ai-customer-agent_boston_7nsppwmn) |
| 8 | **Cohere** | PM, Agent Harness & Modelling | Remote (EST preferred) | Unstated | not-applied | — | — | 14-agent SDK fleet | Owns agent runtime: tool orchestration, parallel execution, failure recovery — direct fleet match. [Ashby](https://jobs.ashbyhq.com/cohere/1d1b300d-254b-48c4-958f-99c6b907f295) |
| 9 | **BCG X** | (Associate/Sr) AI Product Manager | Boston, MA | $129.6–171k | not-applied | — | — | Phase D typed reasoning edges | Boston anchor, B2B Sales/Service Cloud focus. Gap: Salesforce ecosystem. [BCG Careers](https://careers.bcg.com/global/en/job/56768) |
| 10 | **HubSpot** | Sr. PM I, Flywheel Sales | Boston / Remote | $150–180k est | not-applied | — | — | Phase D synthesizer | Second HubSpot bet — internal GTM AI tooling. [BuiltInBoston](https://www.builtinboston.com/job/senior-product-manager-i-flywheel-sales/7806296) |

---

## Tier 2 — "Would consider" (15)

Apply Weeks 3–5. SF roles included with remote-exception ask; AI-native frontier labs included as portfolio-leverage plays.

| # | Company | Role | Loc / Policy | Comp | Status | Date Applied | Inside Contact | Featured Artifact | Notes / JD |
|---|---|---|---|---|---|---|---|---|---|
| 11 | **Scale AI** | Incubation Product Manager | San Francisco | Unstated | not-applied | — | — | Phase 6 knowledge loop | Moonshots Team. 2–3 yrs experience matches. Remote-exception ask required. [BuiltInSF](https://www.builtinsf.com/job/incubation-product-manager/4010550) |
| 12 | **Robinhood** | PM, Care AI Platform | NYC, 3 days/wk | Unstated | not-applied | — | — | Sanitized agentic financial-research fleet | NYC commute is the friction; AI Care Platform is the fit. [BuiltInNYC](https://www.builtinnyc.com/job/product-manager-customer-care/7137271) |
| 13 | **Glean** | PM, AI Quality | SF Bay, 3–4 days | $160–240k | not-applied | — | — | Phase 6 knowledge loop | LLM eval + inference-provider relationships. Violates 3-day cap; remote-exception ask. [Greenhouse](https://job-boards.greenhouse.io/gleanwork/jobs/4525518005) |
| 14 | **Scale AI** | PM, Agent & RL Environment Data | SF / NY / Seattle | $216–270k | not-applied | — | — | Typed reasoning edges (`concept_edges`) | 6+ yrs floor — severe stretch without warm ref. [Scale Careers](https://scale.com/careers/4609736005) |
| 15 | **OpenAI** | APM / PM I (track) | SF / Remote | $200–280k est | tbd | — | — | `intent-engineering` MCP | Monitor via job_feed; APM track favors portfolio-tenure asymmetry. |
| 16 | **Hugging Face** | PM, AI Tooling / Hub | Remote | Unstated | tbd | — | — | 14-agent SDK fleet | Open-source AI infra; remote-friendly. Monitor via job_feed. |
| 17 | **Perplexity** | Product Manager | SF / Remote | $180–250k est | tbd | — | — | Sanitized financial-research fleet (retrieval) | Search + retrieval-augmented gen. Strong artifact fit. |
| 18 | **Mistral** | Product Manager | Paris / Remote-EU | Unstated | tbd | — | — | `intent-engineering` MCP | EU-leaning; consider only if remote-US fully available. |
| 19 | **Cursor (Anysphere)** | Product Manager | SF | $180–280k est | tbd | — | — | Vibe-coding adjacency | Vibe-coding rep target — applying *to* the tool you'd use in interviews. |
| 20 | **Replit** | Product Manager | Remote | $160–220k est | tbd | — | — | 14-agent SDK fleet | Agent-native IDE; remote-friendly. Monitor via job_feed. |
| 21 | **Modal Labs** | AI Product Manager | NYC / SF | $180–250k est | tbd | — | — | Cost governors + local routing | Serverless GPU infra — agent cost economics match. |
| 22 | **Pinecone** | Product Manager | NYC | $170–230k est | tbd | — | — | Phase D typed reasoning edges | Vector DB; reasoning-edges as a structured-recall artifact. |
| 23 | **LangChain** | Product Manager | SF / Remote | Unstated | tbd | — | — | 14-agent SDK fleet | Agent orchestration framework — fleet is the demo. |
| 24 | **Notion** | PM, AI | SF / NYC | $200–280k est | tbd | — | — | Phase 6 knowledge loop | AI-native knowledge tool; Phase 6 is the parallel. |
| 25 | **ElevenLabs** | Product Manager | NY / London / Remote | Unstated | tbd | — | — | Animation pipeline (creative crossover) | Voice AI; pivot into creative-tech if AI PM track stalls. |

---

## Tier 3 — "Safety net + wildcards" (5)

Apply Weeks 4–6. SF on-site wildcards (Sierra, Decagon) included for asymmetric upside; Larry's crypto network roles for the Domain Specialist fallback per [[2026-05-06-unified-roadmap]] Fork 2.

| # | Company | Role | Loc / Policy | Comp | Status | Date Applied | Inside Contact | Featured Artifact | Notes / JD |
|---|---|---|---|---|---|---|---|---|---|
| 26 | **Sierra** | PM, Agent Development | SF / NY on-site (strict) | $180–390k | not-applied | — | — | Local-model routing + 14-agent fleet | 5–7 yrs floor + on-site mandate. Wildcard only. [Ashby](https://jobs.ashbyhq.com/Sierra/effd7cd2-8a28-4bae-a3b8-40720ba09717) |
| 27 | **Decagon** | Senior Agent Product Manager | SF on-site | $200–285k | not-applied | — | — | Typed reasoning edges | "Founder background" explicitly welcomed. 6+ yrs floor. [Ashby](https://jobs.ashbyhq.com/decagon/dcf9b561-f2fb-422b-88a9-33ce76e96608) |
| 28 | **Coinbase** | PM, Developer Platform | Remote | $180–250k est | not-applied | — | Larry (warm intro available) | `intent-engineering` MCP + Block on-chain context | Larry's network — Domain Specialist fallback. See [[warm-intros]]. |
| 29 | **Messari** | Senior Product Manager | NYC / Remote | $160–220k est | not-applied | — | Larry (direct ref) | Sanitized financial-research fleet | Larry is at Messari. Strongest warm intro of the set. See [[warm-intros]]. |
| 30 | **Linear** | PM, AI / Platform | Remote | $180–250k est | tbd | — | — | Phase D typed reasoning edges | AI-native PM tooling; remote-friendly. Monitor via job_feed. |

---

## Application Cadence

Per master plan Phase 5 Task 5.2:

- **5 quality applications per week** starting Week 3 (2026-05-19)
- Tuesday + Thursday mornings 8:30–10:30 AM are application blocks
- Each app: tailored resume + personalized cover note + ≥1 paragraph proving JD-read + featured artifact link
- Inside-contact ping sent same day as application

**Week-by-week sequence** (from DR §7):

| Week | Slot | Targets |
|---|---|---|
| Week 2 (5/12–5/18) | High-leverage wildcards + T1 anchors | #1 Anthropic FDE, #2 Glean FDP, #3 Pair Team, #5 Liberate |
| Week 3 (5/19–5/25) | Boston ecosystem + technical reaches | #11 Scale Incubation, #4 HubSpot Voice, #7 Klaviyo, #6 Manifold |
| Week 4 (5/26–6/1) | Core PM backfills | #13 Glean AI Quality, #9 BCG X, #8 Cohere |
| Week 5 (6/2–6/8) | SF "Hail Mary" exceptions | #26 Sierra, #27 Decagon, #14 Scale Agent/RL |
| Week 6+ | Larry's network + frontier labs | #28 Coinbase, #29 Messari, #15 OpenAI, #16 HuggingFace |

---

## How This File Stays Alive

1. **Status mutations:** Update the `Status` column when state changes. When you apply, add `Date Applied` (YYYY-MM-DD). When you hear back, note in `Notes / JD` column.
2. **New role surfacing:** When [[job_feed]] surfaces a relevant new role at a target company, update the row to point to the new JD URL. If a *non-listed* company surfaces a strong fit, add a Tier-3 row or replace a `tbd` row.
3. **Weekly retro:** Friday 4:30 PM retro (per operating-model HEARTBEAT) reviews what shipped and adjusts Week N+1 selections from this table.
4. **Inside contacts:** Maintained in [[warm-intros]]. When a contact is added there, cross-reference into the `Inside Contact` column here.

**This file is the canonical tracker.** [[job_feed]] is discovery; this is sequencing. The DR research at [[2026-05-07-target-role-specs]] is the source intelligence — quote it in cover letters where the JD-specific framing matters.
