---
type: operating-model
artifact: SOUL
domain: [job-hunt-2026]
status: confirmed
last_interviewed: 2026-05-05
created: 2026-05-04
ai-context: "People, tools, and tacit knowledge for the 8-week post-Block job hunt. Consumed by sprint-health, pr-digest, process-inbox, and all agents as context layer. Tier-A truths surface in flush.py + knowledge_lint Tier 2 for soul-tier-a-conflict detection."
---

# SOUL — Job Hunt 2026

## Part A — Dependencies (Layer 3)

### Critical-Path Collaborators

| Person | What I go to them for | Blocker if unavailable |
|---|---|---|
| **Mary** (girlfriend) | Connections, referrals, partner-level decision support, told day-of (2026-05-04) | Loss of fastest warm-intro channel + decision sounding-board |
| **Matt Vitebsky** (ex-Block CPO, high-school friend) | Personal contact; "anywhere" referral offered; handled directly outside the formal tracker | Loss of strongest "anywhere" personal referral and a peer who knows Sean's PM craft from the inside |
| **Larry Cermak** (ex-Block President) | Primary professional reference; "anywhere" referral offered. Telegram `@lawmaster10`, `cermak.vavrinec@gmail.com` | Reference activation stalls; any role that asks for refs in week 1 of an interview loop is blocked |

**Broader network (not critical-path; opportunistic):**
- The 9 P&E peers from the 5/4 huddle — Nikita Orobenko, Mike Price, Jordan Leech (media + AI), Koray Baspinar, Claudine Daumur, Bohdan Panasenko, Edvinas Rupkus, Nikita Gulis, Nikola Pivcevic, Josh Gragg. Source of file: `vault/20_projects/prj-job-hunt-2026/The-Block-Contacts-After-Layoff.md`.
- Warm-network 20 (broader; not yet fully inventoried — partial in the README's outreach log).

### Load-Bearing Tools

**Direct hunt operations:**
- **Claude Code / Claude Agent SDK** — primary work environment
- **Obsidian + the vault** — knowledge / pipeline / artifacts
- **Obsidian web clipper** — feeds project-discovery flow
- **LinkedIn** — search + Open to Work + DMs
- **Wellfound** — secondary job board
- **Gmail** (`sean.winslow28@gmail.com`) — sole inbox
- **Google Calendar** — scheduling
- **GitHub** — MCP shipping + portfolio surface
- **Substack** — public writing + build-in-public
- **Telegram** — Larry channel + parts of the warm-network
- **Codex app** — supplementary work

**Build / IDE:**
- **Google Anti-Gravity** — main IDE
- **Pi Coding Agent** (pi.dev) — agentic workflows on Ollama + LM Studio (low-cost compute path)
- **Figma + Claude Design** — design surface (portfolio + UI work)

**Learning surface:**
- **YouTube** + **NotebookLM** — daily learning + study notebooks

### Load-Bearing External APIs / Models

| Service | Role | Outage risk |
|---|---|---|
| Anthropic (Claude API + Claude Code) | Primary thinking / coding partner | High — but local Ollama + Pi Agent provide a degraded fallback |
| Gemini Deep Research / DR Max | Comprehensive paid research with citations | Medium — LDR + SearXNG is the local fallback |
| Local Ollama (Qwen3-14B on MBP, gemma4:e4b on Mac Mini) | Local inference for vault synth, lint, flush, deep_researcher | Medium — Anthropic/Gemini cloud is the fallback |
| LDR + SearXNG (Mac Mini) | Local research stack | Medium — Gemini DR is the cloud fallback |
| OpenAI | Cross-model experimentation | Low — substitutable |
| Perplexity | Search synthesis | Low |
| ElevenLabs | Voice / audio for portfolio + creative work | Low for the hunt itself |
| ComfyUI | Image generation pipeline | Low for the hunt itself |
| NotebookLM | Study + research synthesis | Low |
| Pi Coding Agent | Cheap agentic execution | Medium for build velocity |
| Web scrapers (various) | Job-board + AI-trend signal | Medium |
| Google Suite | Calendar / Gmail / Drive / Docs | High — same blast radius as Gmail |

**No single outage would immediately halt building.** The redundancy across cloud + local + agent stacks is intentional and a strength of the setup.

### Three-Machine Topology

- **Mac Mini — primary build station.** Most building happens here. Down for >24h = real productivity loss; daily-driver, deep_researcher, vault_indexer, and the Ollama localhost stack all live here. Tolerable for ≤1 day; backed up by the MacBook Pro for short outages.
- **MacBook Pro — travel + couch + cross-over.** Handles Mac Mini work *and* high-powered open-source model testing (it's high-spec, so it doubles as Alienware-style test rig). Acts as hot backup for both Mac Mini and Alienware roles. Down for >2 days = noticeable for travel days, but tolerable.
- **Alienware (Windows) — open-source model testing + creative work.** Lowest blast radius for the hunt. Tolerable if down for days; only blocks creative experiments and OSS testing that the MBP can't cover.

### Single Source of Truth

- **Primary:** `vault/20_projects/prj-job-hunt-2026/README.md` — the live tracker. If anything disagrees with reality, the README wins.
- **Secondary (planned):** `vault/20_projects/prj-job-hunt-2026/CLAUDE.md` — to be added; will scope project-specific Claude behavior. README remains the always-loaded canonical doc.
- **Tertiary:** `vault/05_atlas/operating-models/job-hunt-2026/` (this artifact bundle).

### Who Depends On Me

| Person / channel | Cadence | What they need |
|---|---|---|
| Mary | Continuous | Honest day-by-day signal on the search; partner-level transparency |
| Substack readers / public network | Weekly (build-in-public cadence, once started) | Useful posts on AI / building / hunting |
| The Friday retro itself | Weekly | A real review, not theater |

### Self-Blocking Decisions

_(Decisions only Sean can make that tend to pile up.)_

- **Target list:** which 30 companies go on the list
- **Substack voice:** what the writing voice sounds like before the first post ships
- **YouTube:** whether to create a channel at all
- **Build-in-public format:** cadence (weekly?), surface (Substack vs LinkedIn vs both), tone
- **Next thing to build:** post-MCP-v0, what's the second portfolio artifact
- **Track-C MCP cold-start chain:** name → repo → README → plan of action (the four steps that unblock the differentiator artifact)

---

## Part B — Institutional Knowledge (Layer 4)

### Internal Vocabulary

| Term | Meaning |
|---|---|
| **Track A** | Runway — severance, UI, COBRA/ACA, finances. Done in week 1, then maintained. |
| **Track B** | Pipeline — positioning artifacts, target list, applications, interviews. The job-hunt machine. |
| **Track C** | Differentiator — one MCP server (intent-engineering) shipped public + one written artifact. Non-negotiable, even in offer week. |
| **Onwards-and-Upwards plan** | The 5/4 master doc at `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md`. |
| **The 5/4 huddle** | The post-layoff Block call where the 9 P&E peers shared contact info. Source for `The-Block-Contacts-After-Layoff.md`. |
| **Walk-away** | The $100k/yr salary floor. Below = auto-no. |
| **Warm-20** | The 20-person warm-network outreach list (partial, in the README outreach log). |
| **Karpathy single-top-rec** | The thesis that one shipped MCP server is the highest-leverage portable career artifact. Source for Track-C scope. |
| **AI PM / Tech PM / Creative PM** | Archetype shorthand for the role priority order (AI > Tech > Creative). |
| **Block-themed skills** | The 11 skills audited and sanitized in place during the 5/4 migration — preserved as transferable PM patterns rather than archived. |
| **Sacred first hour** | The 8:30–9:30 AM learning block. No email, no apps, no work — articles / YouTube / podcasts only. |

### Sacred Cows

- **Friday retro doesn't get skipped** — even in slow weeks, even in interview-loop weeks.
- **Mary gets honest signal, never a polished version.**
- **Agents don't message humans on Sean's behalf.** Drafts are fine; sending is Sean's.
- **Track-C MCP is non-negotiable** — protected even in offer week.
- **Walk-away salary = $100,000 base.** Below is auto-no.
- **5-days-in-office = non-negotiable no.**
- **Remote is preferred but not absolute.** Two override conditions: a role at **Anthropic** specifically, or any role with **$250k+/yr base** anywhere — Sean would relocate for either.

### Unwritten Communication Rules

**Reply latency norms:**
- Recruiters: within 24h.
- Warm-network: within 48h.
- Cold-recruiter spam: never.

**Channel-of-choice:**
- **Substack** = long-form / essay / build-in-public deep dives.
- **Twitter / X** = short-form sharing, quick takes, signal.
- **LinkedIn** = amplify what's already on Substack + Twitter (not the original surface).

**Tone defaults:**
- **Story-driven Sean Mode** is the baseline. See [`.claude/skills/writing-voice-modes/SKILL.md`](../../.claude/skills/writing-voice-modes/SKILL.md) — Sedaris-tuned: self-deprecating humor, hyper-specific details, mundane-accumulation that pivots to a real point. No corporate veneer.
- For Slack / DMs / professional replies: dial Sean Mode to ~60% (warmer + dryer, still recognizably Sean).

**Anti-patterns:**
- Never use the LinkedIn one-click "Easy Apply" button — applications go through the company-direct path with a tailored resume.
- Never send a generic "just checking in" follow-up. If you're following up, lead with new value or a specific question.
- Always lead with kind + thankful + genuine curiosity about the company / their work. Not flattery — actual interest.

### Ask X About Y

| Person | Topic |
|---|---|
| Larry Cermak | References, "anywhere" referrals, Block context |
| Matt Vitebsky | AI PM career framing, Block context, personal-network warm intros |
| Mary | Decision support, energy check, "who do I know at X?" |
| Jordan Leech | Media + AI angle |
| Nate B Jones | AI news + AI tool-usage recommendations |
| Matt Wolfe | AI news + AI tool-usage recommendations |

### Past Landmines

_(Patterns from prior hunts — actively defend against these.)_

- **Applied to too many roles too soon → burned out by week 4.** Pace the application volume; the 5/week cap exists for this reason.
- **All eggs in one basket → outsized letdown when it falls through.** Always have ≥3 active loops before any one role becomes "the role."
- **Skipped company research before the interview** → showed up under-prepped. Mandatory pre-interview research block per loop.
- **Failed to fully understand the role / responsibilities before interviewing.** Read the JD twice and write a 1-pager on what the role actually is *before* accepting the screen.
- **Forgot the post-interview thank-you.** Send within 24h via email + LinkedIn message. Non-negotiable.

### Week-One Tacit Knowledge

_(What a sharp friend shadowing the hunt would need to know on day one but isn't in the README.)_

- **Sean works best in the morning** — schedule the hardest cognitive work (Track-C, interview prep, deep writing) before lunch, not after.
- **The mid-day 1–2 hour break is mandatory** — it's not a slack window, it's how Sean handles a long day mentally and stays human. Don't try to compress it.
- **Sean loves to learn and will take on any task no matter how out-of-realm.** Push him toward "you've never done this — learn and ship" tasks; he'll take the bait.
- **Peak focus is the 8:30 AM learning hour and the 9:30 AM–1 PM block.** That's where the day's leverage lives.

### Things Collaborators Have Learned About Sean

- More energized by **building** than by **selling**.
- Works best in the morning at peak focus.
- The break matters — let him have it.
- Loves to learn; willing to take on any task however difficult or out-of-realm.
- Works hard at everything he does.
- Genuinely funny + enjoyable to be around — that's a real asset in interviews and warm-network calls, not a soft skill to apologize for.

### Tier-A Truths (high-priority — the agent fleet must not contradict)

1. **Walk-away salary = $100,000/yr base.** Below = auto-no, no exceptions.
2. **5-days-in-office = non-negotiable no.**
3. **Agents do not message humans on Sean's behalf.** Drafts only.
4. **Track-C MCP (intent-engineering) is the differentiator — protected, even in offer weeks.**
5. **Friday retro is the only mandatory ritual.**

**Tier-A relocation-exception clauses** (so the fleet doesn't flag false conflicts):
- Remote-preferred is overridden by **a role at Anthropic specifically.**
- Remote-preferred is overridden by **any role with $250k+/yr base.**
