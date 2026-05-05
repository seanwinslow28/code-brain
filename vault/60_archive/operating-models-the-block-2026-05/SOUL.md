---
type: operating-model
artifact: SOUL
domain: [the-block]
status: confirmed
last_interviewed: 2026-04-19
created: 2026-04-18
review-date: null
ai-context: "People, tools, and tacit/tribal knowledge for The Block. Populated by the work-operating-model skill. Consumed by sprint-health, pr-digest, process-inbox, and as a context layer by all agents."
---

# SOUL — The Block

## Part A — Dependencies (Layer 3)

### Critical-Path Collaborators
| Person | Role | What I go to them for | Blocker if unavailable |
|---|---|---|---|
| **Ed Rupkus** | Product Manager (my manager) | Priority signal, P&E wording review, career guidance, tiebreaker on non-Campus calls | Most decisions I stall on; daily overlap |
| **Matt Vitebsky** | VP P&E / CPO | P&E update sign-off, exec-level escalation | Bi-weekly P&E post cannot ship without his nod |
| **Larry Cermak** | President of The Block; **Interim CEO** until the new CEO is announced (announcement expected 2026-05-01) | Exec-level roadmap signal in the interim period | Top-of-org strategic alignment until the new CEO lands |
| **Steve W. Chung** | Incoming CEO, starts 2026-05-01. Tech + media + global-scale executive. Most recently at Azuki (anime-NFT / web3, LA); prior: Co-CEO CJ ENM America & Chief Global Officer of CJ ENM; Chief Growth Officer at FOX Corporation (launched LiveNOW and FOX SOUL FAST channels); founder of OTT platform Frankly (reverse-IPO). Stanford MBA, Harvard AB. | Roadmap direction, Block Pro revamp approval (post-start), strategic CEO sign-off on everything downstream | All top-of-org strategic choices route through him from 2026-05-01 onward |
| **Mike Price** | Lead Developer / Lead Software Engineer | The Block's API access (pending), deepest tech-architecture calls | API access is the current gated item — deliberately not pushing |
| **Josh Gragg** | Director of Design | Design-team direction, design-system questions, escalation on design disagreements | Design approvals that the individual designers can't green-light |
| **Claudine Daumur** | Product Designer | Design handoffs, Figma-level clarification on tickets I wrote | Specific design-Q resolutions |
| **Serena Ho** | Product Designer | Same as above | Specific design-Q resolutions |
| **Nikita Orobenko** | Engineering — Campus-focused | Campus-feature tech clarifications | Campus dev blockers |
| **Nikita Gulis** | Engineering — Campus-focused | Same | Campus dev blockers |
| **Nikola Pivcevic** | Senior Software Engineer | Harder .Co engineering questions | Ticket-level tech clarifications |
| **Brian Mendoza** | Senior Software Engineer | Same | Ticket-level tech clarifications |
| **Cesar Paz** | DevOps | Jira/Slack integration, staging envs, infra questions | Environment/infra unblocks |
| **Koray Baspinar** | SEO Consultant (eng/dev adjacent) | SEO sync, GEO/SEO implementation on Learn + Data pages | SEO-feature direction |
| **Ramuald Vishneuski** / **Ana Benitez** | QA / AQA | Test coverage, release verification | Release-readiness sign-off |
| **Bohdan Panasenko** | Engineering — Intern | Junior dev support | Low |
| **Krystof Oliva** | Engineering — Intern (AI-focused) | AI-adjacent experimentation, potential collaborator on Block-side AI | Low today, rising |
| **David** | Sr. Mgr, Course Design & Compliance (Campus / Sponsored Courses) | All Campus compliance + Sponsored Courses context | Campus decisions that need compliance context; occasionally hard to reach |
| **Lil Danowski** | Sr. Director RevOps | RevOps favors (Claude/Zapier/AI tool help) | Low-priority — never blocks me |
| **Karla Vallecillo** | AdOps / Sponsorship Campaign Manager | AdOps favors | Low-priority |
| **Jeffrey Milligan** | SVP Sales | Sales-side context for Sponsored Courses + API revenue ideas | Occasional |
| **Steven Zheng** | Head of Research | ETF research feed via `#research-etf`; future product signal | Indirect — his team posts the signal, not him |

### Media Team (learn-from, non-blocking)
| Person | Role | My relationship |
|---|---|---|
| Gareth Jenkinson | Head of Multimedia | Learn what they're producing; offer future help |
| Jordan Leech | Video/podcast producer | Same |
| Davis Quinton | Video/podcast producer | Same |

I attend the Wed 10:45 AM sync to learn and look for ways to bring Block revenue through media output.

### Load-Bearing Tools
**Hard collapse (can't work a day without):**
- Jira, Confluence, Slack, Google Calendar, Gmail, Obsidian, Claude Code.

**Soft collapse (a day is manageable, a week breaks workflow):**
- Claude Cowork, Claude Design (new), Anti-Gravity IDE, Granola, Figma, WordPress (manual only — never agent), ETF tracker Google Sheet, Campus CLMS backend, Google Sheets/Docs/Drive, Rippling.

**Periodic / occasional:**
- Salesforce (Campus user emails), GA4, GAM, Twitter (news/signal), Perplexity Deep Research, Gemini Deep Research, Nano Banana Pro / Nano Banana 2 (diagrams + mockups).

### Load-Bearing External APIs / Models
**Data APIs:**
- TwelveData (ETF pricing)
- TradingView (charts)
- SEC.gov (filings)
- CoinGecko, RWA.xyz (site data — I don't touch much directly)
- The Block's own API (access pending from Mike Price — not pushing yet)

**AI models:**
- **Primary:** Claude (Anthropic). Most PM leverage runs through here.
- **Secondary:** Perplexity, Gemini.
- **Growing:** Ollama — phi4-mini and Qwen3-14B for local agentic workflows.
- **Failure mode:** Anthropic outage is the hardest single-point-of-failure in my day.

### Three-Machine Topology (Block-side)
- **Mac Mini (primary):** All three domains + SDK agents + Prototype-Lab. If this is down, ~80% of Block work halts; tolerable for a few hours, not a full day.
- **MacBook Pro (couch / travel / meetings):** Camera + 48GB unified memory. Used for meetings, travel, and occasional creative work. Block-specific halt: meeting attendance and on-the-go Slack/Jira triage. Tolerable for a day.
- **Alienware:** No Block work yet. Might touch Block work via Nvidia NemoClaw experimentation in the future. Today: Creative Studio only.

### Single Source of Truth
**Canonical (company-wide):**
- **Slack** — async communication of record.
- **Jira** — ticket state and sprint truth.
- **Confluence** — P&E updates + long-form docs.
- **Granola transcripts** — meeting record (my personal overlay; company sometimes uses Google Meet transcripts, not reliably).

**Runner-up canonical (G-Suite fabric):**
- Google Calendar, Google Drive, Google Sheets, Google Docs.

**Sean's personal processing layer (NOT a company source):**
- Obsidian — this is where I think, not where The Block stores truth.

**Known gap (flagged in Layer 1):** Slack / Granola often record "we shipped X" before Jira catches up. `jira-automation` skill doesn't reconcile these yet — this is the concrete automation ask.

### Who Depends On Me
| Person / team | Cadence | What they need |
|---|---|---|
| Ed | Daily overlap + weekly 1:1 | My visibility into ticket state, P&E draft, Campus status |
| Devs (Mike, Nikola, Brian, Nikita O., Nikita G., Bohdan, Krystof, Cesar) | Tue/Wed/Thu 10 AM standup + async Slack | Ticket clarifications, acceptance decisions, unblocks on my tickets |
| Designers (Josh, Claudine, Serena) | Standup + ad-hoc | Design ticket clarifications, review approvals |
| QA (Ramuald, Ana) | Per-release | Acceptance criteria clarity |
| David | Bi-weekly + ad-hoc | Campus + Sponsored Courses PM coverage |
| Matt / CPO | Bi-weekly | P&E update for sign-off |
| Larry Cermak (President / interim CEO) | Through 2026-04-30 | Exec-level roadmap signal in the interim window |
| Steve W. Chung (incoming CEO) | Ongoing from 2026-05-01 | Roadmap clarity, Block Pro direction, approval gate for Ed + Sean's pitches |
| Media team (Gareth, Jordan, Davis) | Weekly (Wed 10:45 AM) | Future-facing support, idea sparring |
| RevOps / AdOps (Lil, Karla) | Bi-weekly + ad-hoc | Claude/Zapier/AI-tool help, Salesforce Campus user email handling |

No one currently pings me multiple times a day.

### Self-Blocking Decisions
_Only I can close these out:_
- "Is this blocker real?" triage — when a dev says they're stuck.
- Ticket writing (both Design and Implementation stories).
- Design-review approval on tickets I own.
- Dev/design question response on my tickets.
- Campus / Sponsored Courses judgment calls (the ones I don't escalate to Ed).
- Salesforce Campus user/client email replies.
- GA4 analytics lookups for the team.
- P&E update wording (before Ed's pass).
- General admin work.

(Current volume: manageable — still ramping, responsibilities expanding slowly.)

---

## Part B — Institutional Knowledge (Layer 4)

### Internal Vocabulary
| Term | Meaning |
|---|---|
| `.Co` | theblock.co (the free public site) |
| `Campus` | The Block's LMS / education platform |
| `Pro` | The Block Pro (paid subscription tier — biggest revenue line) |
| `Pro Research` / `Pro News` / `Pro Data` / `Pro Deals` / `Pro API` | Sub-products inside Pro |
| `Launchpad` | Launchpad product |
| `Sponsored Courses` | Campus monetization stream |
| `Block iOS app` | Native app launching to App Store soon — expect ticket load |
| `Marketing Site Update` | Current marketing-site rework |
| `Stripe Integration` | Campus individuals payment flow (tax-compliance revamp) |
| `Twitter/X Auth` | Twitter/X OAuth work |
| `Crypto IQ` | Product codename |
| `Election Hub` / `Voting Block Index` | Election-coverage landing + data product (v1 live, v2 in planning) |
| `Report Cards` | `.Co` social-sharing feature |
| `The Starting Block` | Product with Singular.live data feed |
| `Knowledge Token Taxonomy` / `Prerequisite Schema` | Campus curriculum-graph work |
| `ToGroom` | Jira label — ticket needs product grooming |
| `NeedsDesign` | Jira label — story needs design before implementation |
| `/llms.txt` | Machine-readable site index (shipped for Campus) |
| `x402 protocol` | Agent-payments protocol — Sean actively championing for future Block integration; research archive in `_inputs/x402 Deep Research/` |
| `#research-etf` | Slack channel (C09EXM9FYAG) where the ETF pipeline starts |

(Further terms are best surfaced live from Jira / Granola when they appear — don't try to enumerate exhaustively.)

### Sacred Cows
- **Always use the simple Figma slides template** for presentations. Canonical live example: [Product Roadmap 2026 Draft](https://www.figma.com/slides/V7KnGbiTK0yiCY4SKYj4dv/Product-Roadmap-2026-Draft?node-id=0-20&t=qhRmjsD9GVOglaTV-0).
- **Presentation structure is always `Context → Problem → Solution`.**
- **Jira tickets follow the `jira-automation` skill's templates + quality checklist.** Don't invent new formats.
- **User journey first** on any new product / page pitch. Clunky multi-step flows that risk user drop-off get pushed back.
- **Roadmap ambition (pre-new-CEO):** Matt's signal — pitch a revamp of a product that already makes money (The Block Pro), tuned to current market. Keep moonshots for explicit blue-sky / ideation phases; otherwise scale ideas to what's fundable and shippable.
- **Never give agent write access to WordPress or GitHub** (see USER.md).

### Unwritten Communication Rules
- **Slack is default**; email is rare (external parties only; Sean rarely involved today).
- **Paper-trail comments** go on Jira, Figma, or Confluence — decisions you might have to re-litigate belong in writing against the artifact.
- **Ed DM (`D09RWHRC9HC`) → respond ASAP.** He's Portland, OR (Pacific). Only soft exception is mid-activity overlap (lunch, etc.). Otherwise immediate.
- **No universal response-time expectation across the distributed team.** Send when you think of it; don't expect fast replies unless the person is in your timezone.
- **`@here` is reserved for the bi-weekly P&E update post** in `#ask-product-management` (C02N3UFMTEC). Don't `@here` casually. Example format (2026-04-17 post): short `@here` + Confluence link + 4–6 bullet headline list of shipped items.

### Ask X About Y
| Topic | Go-to person(s) |
|---|---|
| The Block's internal data API | Mike Price (access pending) |
| Campus compliance / Sponsored Courses | David |
| SEO on Learn / Data pages | Koray Baspinar |
| DevOps / staging envs / Jira-Slack plumbing | Cesar Paz |
| Design system / Figma design questions | Josh Gragg (director) + Claudine Daumur + Serena Ho |
| ETF research signal | Steven Zheng's team via `#research-etf` (C09EXM9FYAG) |
| AI-adjacent experimentation / fellow AI obsessive | Krystof Oliva (intern) + Jordan Leech (media + AI) |
| AdOps / RevOps tooling help | Lil Danowski + Karla Vallecillo |
| Media / video production | Gareth Jenkinson, Jordan Leech, Davis Quinton |
| Go-to dev bench (tickets, architecture, clarifications) | Mike Price, Brian Mendoza, Ramuald Vishneuski, Nikola Pivcevic |
| P&E wording preferences | Ed Rupkus |
| Universal fallback ("I don't know, but Ed will know who does") | Ed Rupkus |

### Past Landmines
- **David ↔ devs alignment — 2 incidents** where Campus-side misalignment caused rushed execution and downstream mistakes. Both of Sean's CYA communication logs trace back to this pattern.
- **Remediation in-flight:** new **weekly Campus team sync (Tue 09:30 ET, starting 2026-04-28)** with Sean, Ed, David, and Campus-focused devs.

### Week-One Tacit Knowledge
For a sharp new PM joining Ed's team:
- **Take notes aggressively** — use Granola, Gemini meeting transcripts, or both.
- **Read the relevant Confluence best-practices docs** early.
- **Don't hesitate to ask Ed or Sean questions** — async Slack is fine.
- **Take initiative on projects** without waiting for explicit assignment; surface in the next meeting.
- **Subscribe to these 10 Slack channels on day one:**
  - `#ask-product-management` (C02N3UFMTEC)
  - `#dev` (C07DNU1MQBZ)
  - `#deployment-approval` (C0590T88MUM)
  - `#product-design-team` (C04EU3840M8)
  - `#research-etf` (C09EXM9FYAG)
  - `#social-media-marketing` (C09L89LQAT0)
  - `#tech-seo` (C029B19JPQ8)
  - `#tech-support` (C0259QCR34G)
  - `#general` (CR5D2HQ13)
  - `#ped-team` (C02PHB06BS6)

### Things Collaborators Have Learned About Sean
**Known / visible to the team:**
- Sean is the AI / Anthropic tools person. Uses Claude for ticket writing and research. Go to him for anything AI / agentic / Claude-adjacent.
- Sean responds quickly regardless of "break" windows — stepping away just moves the conversation to phone.

**Not known (deliberately):**
- That Sean uses **Granola** for his meeting notes layer.
- That Sean drafts Slack messages and comments in **Claude** before editing and sending.

**Personal north star:**
- Ed is Sean's aspirational model for PM work ethic — reliable, omnipresent on Slack, across every Block project.
- Sean's long-term target: "hard-working PM like Ed + my own creative / technical edge."
