---
type: operating-model
artifact: SOUL
domain: [the-block]
status: draft
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
| **New CEO (TBA)** | Incoming CEO, starts 2026-05-01 (name not yet known — update this row on announcement) | Roadmap direction, Block Pro revamp approval (post-start) | Roadmap/strategic choices will increasingly route through them |
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
| Larry (Interim CEO / President) + incoming CEO | Ongoing; new CEO takes the handoff 2026-05-01 | Roadmap clarity, Block Pro direction |
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
_To be filled by interview (Layer 4)._

### Sacred Cows
_To be filled by interview (Layer 4)._

### Unwritten Communication Rules
_To be filled by interview (Layer 4)._

### Ask X About Y
_To be filled by interview (Layer 4)._

### Past Landmines
_To be filled by interview (Layer 4)._

### Week-One Tacit Knowledge
_To be filled by interview (Layer 4)._

### Things Collaborators Have Learned About Sean
_To be filled by interview (Layer 4)._
