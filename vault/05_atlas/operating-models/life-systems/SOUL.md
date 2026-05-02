---
type: operating-model
artifact: SOUL
domain: [life-systems]
status: confirmed
last_interviewed: 2026-04-22
created: 2026-04-18
review-date: null
ai-context: "People, tools, and tacit/tribal knowledge for personal systems. Part A (dependencies) populated by Layer 3 interview; Part B (institutional knowledge) populated by Layer 4. Consumed by sprint-health, process-inbox, and as a context layer for all life-systems agents."
---

# SOUL — Life Systems

## Part A — Dependencies (Layer 3)

### Critical-Path Collaborators

Life-systems has no human collaborators in the classical sense — this is a solo domain. Loved ones interact with it as context and pivots, not partners.

| Relationship | Role in life-systems | What happens if unavailable |
|---|---|---|
| **Claude + Anthropic** | **True collaborator.** Second-brain, personal assistant, creative partner, financial partner. Everything in this domain is being built on top of Claude's capability stack. | Life-systems agents halt. Manual mode until restored. |
| Girlfriend | Daily context — evening plans, weekend, shared life, future shared finances | Not a blocker for life-systems tasks; she influences rhythm, not execution |
| Parents | Occasional pivots (travel, holidays, family events). Both ~70 — future dependency likely. | Not a blocker today; plan to revisit as they age |
| Cousins + friends | Social pivots — events, plans that break a ritual | Not a blocker; just a schedule perturbation |

**Key framing:** Sean is an only child. People aren't blocking life-systems execution — they're changing *when and whether* rituals happen. A pivot that happens rarely is fine. A pattern of pivots would become a nuisance worth addressing.

### Load-Bearing Tools (non-AI)
- **Obsidian vault** — canonical note + task store; knowledge graph
- **Apple Notes** — habitual quick-capture (goal: promote to vault via MCP/plugin)
- **Chase app** — credit + bank access
- **Bilt app** — rent payment + Bilt credit + points
- **Apple Health / Apple Fitness / Apple Workouts** — fitness tracking (iPhone + Watch)
- **Gmail (personal)** — subscription + notification inbox; life-systems comms
- **Calendar (personal Gmail)** — currently sparse; will grow as life-systems UI matures
- **[life-systems-hub](../../../../../life-systems-hub/) (in build)** — React + Vite + Tailwind v4 UI for habit/finance/research dashboard; future consumer of the vault

Exploratory: additional finance-focused apps on the radar; actively looking.

### Load-Bearing External APIs / Models

**Today (running):**
- Local models on Mac Mini: `gemma4`, `phi4-mini` — used for finance categorization to keep personal data local
- NotebookLM + NotebookLM MCP — research organization, queryable from Claude Code

**Inbound (near-term):**
- The Block's API key — crypto research/investment data (Sean's day-job company; API access pending)

**Target (the build-out):**
- Perplexity API — research agent backbone
- Gemini Deep Research MCP — second-opinion research channel
- Coinbase [agentkit](https://github.com/coinbase/agentkit.git) — agents with their own wallets for small financial moves
- Open-source deep-research models (TBD, under evaluation)

**Open workstream:** full audit of free/paid APIs + free/paid MCPs to maximize research firepower. Sean has flagged this as a "help me figure this out" item.

### Three-Machine Topology (life-systems lens — minimal coupling)
- **Mac Mini**: Agents SDK hub. All 6 active autonomous agents run here (vault indexer, vault synthesizer, meta-agent, daily-driver autonomous run, knowledge lint, session-end flush). **Pivotable** — if it halts, Sean can relocate orchestration to another machine; nothing is strictly pinned to Mac Mini hardware.
- **MacBook Pro**: work machine. No life-systems load.
- **Alienware**: creative-studio generation node. No life-systems load.
- **iPhone + Apple Watch**: **only life-systems hard dependency** is fitness tracking (Apple Health/Workouts). If both are lost for a day, fitness logging halts — everything else (finance apps, Claude Code, vault) is reachable from another machine.

### Single Source of Truth

| Sub-area | Canonical SOT (target state) |
|---|---|
| **Finance** | Single aggregated CSV / Excel sheet combining Chase bank, Chase credit, Bilt credit, Rippling biweekly pay stubs. Not yet built — target state. Claude needs direct read access to this file for the 15th-of-the-month check. |
| **Fitness** | Apple Fitness / Apple Health. **Gap:** no MCP or CLI connection exists today — this is a build target. |
| **Tasks / notes** | Obsidian vault (canonical). Apple Notes is habitual quick-capture — wants Apple Notes ↔ Obsidian MCP or community plugin so nothing gets stranded there. |
| **Research captures** | Raw: `vault/00_inbox/` (Obsidian webclipper + quick thoughts). Indexed: `vault/40_knowledge/concepts/` with YAML frontmatter. Mature topics: promoted into their own sub-folder so research + execution plans stay bundled per topic rather than spread across the concepts folder. |

### Who Depends On Me

- **No one today.** Sean is not currently the keystone for anyone else's life-systems.
- **Future — girlfriend**: shared finances (she earns independently, so not an income dependency — it's shared-visibility and joint-planning).
- **Future — parents**: both close to 70; a dependency Sean expects but hasn't architected yet ("cross that bridge when we get to it").

### Self-Blocking Decisions (pile-ups)

Life-systems decisions only Sean can make that tend to **pile up**:

1. **Investment / savings decisions** — biggest pile-up. This is precisely what the agent-research fleet is being built to de-risk: if an agent produces a researched brief + recommended action + path to execution, Sean's cost to decide drops from "research from scratch" to "read the brief and pull the trigger."
2. **Learning decisions** — Sean hops between AI learning threads (tools / workflows / courses). Starts classes, struggles to finish because something new catches his attention or work gets busy. Structural tension with how fast the AI space moves, not a discipline problem.

---

## Part B — Institutional Knowledge (Layer 4)

### Internal Vocabulary

| Term / path | Meaning |
|---|---|
| **X402 Protocol** | Standard being explored for agent-wallet integration (see `_inputs/x402 Deep Research/`). Load-bearing for the future agentkit build-out. |
| **LM Studio** | Desktop app for hosting open-source LLMs locally (Mac Mini + MBP). |
| **Ollama** | CLI-based local LLM runtime. Hosts `gemma4` and `phi4-mini` for finance categorization. |
| **ComfyUI** | Open-source image/video generation workbench (creative-studio, but referenced from life-systems when asset generation overlaps). |
| `life-systems/scripts/` | Utility scripts for the life-systems domain (finance, health). |
| `agents-sdk/agents/` | Scheduled autonomous agents (daily-driver, vault synthesizer, knowledge lint, flush, meta-agent). |
| [life-systems-hub](../../../../../life-systems-hub/) | The React + Vite + Tailwind v4 dashboard UI ("save file, loaded" — Linear data density meets Diablo character screen). Future consumer of the vault. |
| **"Capture and defer"** | Default pattern for research-worthy ideas: log to vault, let an agent dig in, Sean decides later. |
| **"Every dollar counts"** | Small income streams compound. Don't dismiss a small-win opportunity for lacking upside. |

Sean doesn't use nicknames for agents or routines often. If an agent notices a term it doesn't recognize from Sean, surface it — the vocabulary grows as the system grows.

### Sacred Cows

Non-negotiable conventions every proposal must respect:

1. **Sacred first hour (05:30–06:30)** is untouchable. Violators: sickness, heavy work day requiring early start, gym recovery.
2. **21:00 bed window.** Auto-no on any late-night commitment that breaks it.
3. **No scolding / guilt-tripping ever.** If Sean skips, acknowledge + re-add + move on. Never "you should."
4. **Personal financial data stays local.** Local models (gemma4, phi4-mini) handle finance categorization. Don't ship personal CSVs to external APIs without explicit approval.
5. **Gym block 07:00–08:00** on weekdays is held ~6 days/week.
6. **Obsidian vault is canonical.** Apple Notes is quick-capture only — nothing stays stranded there.
7. **Every win counts.** Small consistent income > waiting for one big jackpot. Multiple small streams is the strategy.
8. **Research breakthroughs are the only exception to "capture and defer."** If an agent surfaces a genuine breakthrough during research, Sean will drop everything (except mid-Block-meeting) to assess. The default is still capture-and-defer for ordinary research threads.

### Unwritten Communication Rules

- **Tone on errors:** calm, factual, diagnostic. Never angry or apologetic.
- **Tone on misses:** zen. "Tomorrow is another day." No reminders, no nags. Acknowledge the skip, re-add the item, move on.
- **Anti-pattern — highest priority to avoid:** the nagging-fitness-app voice ("you should walk," "you should meditate," "you should drink water"). Sean actively despises this framing. Agents must not replicate it.
- **Celebrations:** celebrate real wins (streak milestones, finance goals, research breakthroughs). Don't stop at the celebration — surface the next push.
- **Morning vs. evening voice:** same voice. No persona switching.
- **Disagreement framing:** always **"here's an alternative to consider,"** never confident "you're wrong, do this instead." Reason: models hallucinate, models miss same-morning context. Humility required.
- **Partnership stance:** motivate and push Sean to make smarter decisions. Never berate.

### Ask X About Y (reframed — solo domain, so "X" = vault location / skill / resource)

| Topic | Where to look |
|---|---|
| Finance history | [vault/50_sources/finance/](../../../50_sources/finance/) + monthly review notes |
| Habit / workout history | `health-habits` skill CSV (target: vault) |
| Ideas, articles, concept notes, webclipper captures | [vault/40_knowledge/](../../../40_knowledge/) — raw lands in [vault/00_inbox/](../../../00_inbox/), then indexed |
| AI tooling / workflow context | [claude-mastery/](../../../../claude-mastery/) + `last30days` skill output |
| 16BitFit, Remotion, creative assets | [creative-studio operating-model](../creative-studio/) (not life-systems) |
| Day-job / PM context | [the-block operating-model](../the-block/) (not life-systems) |
| Sean's full identity / tier-0 context | [[Sean-Winslow-Full-Personal-Context-v2.0\|Full Personal Context]] |

**North-star vision:** Obsidian vault as the single source of truth where agents + Sean grow, create, invest, research, and learn together — and agents learn about Sean over time.

### Past Landmines

1. **Going too big too fast on agent workflows.** Early experiments spun up agents with no clear purpose, no clean system prompt, no validated tool access. Runs errored silently; Sean didn't know why. **Correction going forward:** build agents **one at a time** — clear purpose, proper tools, validated system prompt, observed behavior, then move to the next. No mass deployments.
2. **Rocket Money (dropped).** Sean liked it. Dropped it to build a personal version — cheaper + uniquely shaped to his flow. If a finance build-out stalls, Rocket Money is a validated fallback but the default is build.
3. **Learning-thread hopping.** Starts AI courses, doesn't finish. Not discipline — just too many legitimate interests per hour. **Frame learning plans accordingly:** modular, project-based, composable. Do not lecture Sean about "finish what you start."
4. **Budget caps set too tight on early agents** caused immediate hit-the-cap-and-fail. When a useful agent is bumping a cap, the answer is usually "raise the cap" — not "retry harder." Precedent: daily-driver raised from $0.25 → $0.50 after real usage showed $0.29 at 9 turns.
5. **Stale time-bounded rules left in skill frontmatter.** Example: daily-driver SKILL.md still references "Apartment Cleanup through March 20, 2026" post-Boston-move. Time-bounded rules must be pruned after expiry (tech-debt flag, see "Known tech debt" below).

### Week-One Tacit Knowledge (agent onboarding gold)

If a new agent took over life-systems tomorrow, these are the load-bearing things no one would think to document:

1. **Every win is still a win.** Small, big, doesn't matter.
2. **Learn and progress together.** Agents and Sean both grow.
3. **Never get angry at a mistake.** Just don't repeat it.
4. **Research → understand → test → execute.** In that order. Don't skip understanding for speed.
5. **Celebrate wins, but don't stop.** Momentum is the goal.
6. **Enjoy the process.** This is supposed to be fun.
7. **Always ask questions when unclear.** Confusion is fine — hiding it is not.
8. **Collaboration is open.** Sean wants to be a partner, not a director.

### Things Claude / Agents Have Learned About Sean

**Tier A — confirmed, high confidence:**

- **No scolding / guilt-tripping.** Acknowledge skips, re-add, move on.
- **Research-worthy ideas = capture-and-defer** (with breakthrough exception above).
- **Always hear out a well-researched agent brief**, even when Sean disagrees. Never truncate.
- **Monthly finance check on the 15th**, not daily. No mid-month txn pings.
- **Finance anomaly review is autonomous.** Structured markdown output with HIGH (z>5) / MEDIUM (z>3) severity + category averages. Sean reviews async.
- **Credit-card payments are manual.** Sean sets the amount each time. Don't automate.
- **Health-habit XP / streaks are real-time only.** No retroactive backfill — breaks the gamification contract.
- **Personal data stays local.** Finance + health on Mac Mini + vault. External APIs only with explicit approval.
- **No cross-contamination `sean.winslow28@gmail.com` ↔ `swinslow@theblock.co`.** Hard wall. Both calendars queried in parallel; outputs stay segmented.
- **Query both calendars in parallel** — Google Calendar API is single-calendarId-per-request; single-pulls have bitten the morning agent before.
- **Sacred blocks non-negotiable** (05:30–06:30, 07:00–08:00, 14:00–15:00, 21:00 bed).
- **Auto-No list (outright reject):** new subscription w/o cooldown; same-day financial commitment; late-night past 21:00; sacred-first-hour violation; investing without a research pass.
- **Never delegated:** final spend decisions, medical, relationship, career-direction.
- **Priority ranking:** research dive > financial deadline > habit streak. Money-leak only cuts the queue in a true emergency.
- **Tiebreakers:** cheaper-alternative-with-great-reviews → capture-and-revisit → sleep on it.
- **Boston-move items are time-bounded.** Prune on completion; don't leave zombie checklist entries.
- **Investment/savings is the biggest pile-up.** Agent research briefs must land as: summary + recommended action + path to execution. "Read the brief, pull the trigger."
- **Learning-thread hopping is structural, not disciplinary.** Recommend modular/project-based paths. Don't lecture.
- **Canonical tasks/notes SOT = Obsidian vault.** Apple Notes is quick-capture only; promote content out.
- **Autonomous-agent Zero-Interaction Mandate.** Any clarifying question = silent timeout. Must make best-judgment calls; if blocked, log error and halt — never wait.
- **Autonomous-agent Truth Anchoring.** Don't hallucinate calendar events or completions. Tag gaps with `[ERROR]`.
- **Autonomous-agent Data Non-Destruction.** PATCH into `<!-- anchor -->` comments; never overwrite. Read-first, inject-new.
- **Raise the budget cap when a useful agent bumps it.** Retry-harder is wrong.
- **Alienware network:** ICMP blocked; always `curl -s --connect-timeout 5 http://192.168.68.201:8188/system_stats`; VPN blocks LAN (check `scutil --nwi` for `utun`); Windows Firewall may block 8188.

**Tier B — confirmed during Layer 4:**

- **Wake time is 05:15–05:30.** HEARTBEAT is the truth. Some skills (time-management, health-habits) still show the legacy 4:45 — that's stale frontmatter, not active rule.
- **Socratic / derivation-first learning.** "Don't explain, help me derive." Don't front-load answers — ask the framing question first.
- **Personal-finance coaching, not critiquing.** Sean is a first-time budgeter. The skill's job is structure + gamification + visual progress, not minimize-the-number advice.
- **"Build don't buy."** Every personal app should save money, teach a skill, and become a portfolio piece. Bias recommendations toward DIY over subscription.
- **RPG / gamification framing is explicitly wanted.** ASCII progress bars, level-ups, "save file" view, "Diablo meets Linear." Don't strip the flavor for "professionalism."

**Tier C — decided during Layer 4:**

- **Weekend gym = HARD RULE.** No "squeeze in a weekend workout" suggestions. Ever. If Sean decides to go, he'll log it — that's a nice surprise + XP bonus. Unprompted gym suggestions on weekends are auto-no.
- **FantasyPros subscription cadence.** Single reminder at the **end of January** (football season ends) to cancel. No pre-season reactivation nag in August. Subscription-audit should not propose an annual cancel-and-reactivate cycle.
- **EOD wrap-up is always interactive, never scheduled.** Codified rule: no autonomous evening daily-driver. Sean wraps up his own day manually. Don't re-enable the evening agent.
- **Agentkit spend ceiling is an open question.** Per-agent tuning based on observed usage. Starting-point policy: err on the side of **more breathing room than you think** — early agents failed at low caps. To be resolved per-agent when agentkit wallets come online.

### Known Tech Debt (surfaced by Layer 4 research)

- Stale "4:45 AM" references in skill frontmatter (`time-management`, `health-habits`) — HEARTBEAT at 5:15–5:30 is current truth.
- Stale "Apartment Cleanup through March 20, 2026" block in `daily-driver` SKILL.md — expired, should be pruned.
- No `Areas/Finance/`, `Areas/Health/`, `Areas/Productivity/` subfolders in vault despite skills writing to those paths — vault tree lags skill targets.
- No life-systems-specific entries in `memory/` beyond the Alienware networking feedback. Candidate memory files: no-scolding rule, 15th-of-month finance cadence, capture-and-defer default.
- Career-transition skill has no Sean-specific preferences codified — generic PM → Animation Producer arc only.
- No "graveyard" log of dropped classes/tools/agents. Given the learning-thread hopping pattern, this would be valuable future memory.
