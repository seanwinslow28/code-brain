---
type: operating-model
artifact: operating-model
domain: [life-systems]
status: confirmed
last_interviewed: 2026-04-22
created: 2026-04-18
review-date: null
ai-context: "Synthesized one-file operating model for personal systems. Cross-references HEARTBEAT, USER, SOUL, schedule-recommendations. Loaded by agents at the start of any life-systems work. The north star: build financial cushion + multiple income streams via agent leverage."
---

# Operating Model — Life Systems

## TL;DR

Life-systems is Sean's solo domain centered on **personal financial advisory + research**, with daily habits as a motivation layer and a quick-capture inbox as the third leg. The true collaborator is Claude + the agent fleet; loved ones are context, not partners. The north star is finance — building a cushion and multiple income streams for Sean, his girlfriend, his family, and his friends — and every automation in this domain is in service of freeing Sean's hours for that work.

## Identity in This Domain

Sean as a person — not as a PM, not as a creative — building toward financial security and multi-stream income through agent leverage. Lives in Boston (post-NYC move), wakes 05:15–05:30, gyms ~6 days/week, partner relationship, only child, parents (~70) likely future dependents, no current dependents. Day-job W-2 income at The Block (since November 2025); freelance is rare. First-time-budgeter on the personal-finance side. RPG / gamification is the explicit aesthetic preference for the [life-systems-hub](../../../../../life-systems-hub/) UI build-out — "Linear's data density meets Diablo's character screen."

## Operating Rhythm Summary

Weekday: wake 05:15–05:30 → sacred first hour 05:30–06:30 (coffee + breakfast prep + green juice + vitamins + AI-news YouTube / podcast / creative) → walk to gym 06:50 → workout 07:00–08:00 → home + breakfast → workday 08:45 start → deep work 09:00–14:00 (life-systems is displaced) → decompress 14:00–15:00 (no computer) → comms/exec 15:00–17:15 → evening with girlfriend 17:15–21:00 (relaxed learning/creative woven in) → bed 21:00–22:00. Weekend: no gym, recovery + quality time + personal creative + agentic projects. Monthly money cycle is fixed (rent 1st, Chase statement 4th, Chase due 7th, Chase statement closes 10th, Bilt due 12th); finance check lives on the **15th** (statements posted + payday landed). No quarterly tax. Boston winter holds the gym streak (10-min walk pushes through almost any weather); Eco-mode heating keeps the bill steady. See [HEARTBEAT.md](HEARTBEAT.md).

## Decision Pattern Summary

Priority ranking when life-systems items compete: **research dive on a money-making idea > financial deadline > habit streak**. Money-leak only cuts the queue in a true emergency. Money-making research surfaces are **capture-and-defer** by default (with a single carve-out: a genuine breakthrough during research interrupts, except mid-Block-meeting). Auto-yes: Bilt redemptions, subscription kills, habit logs, capture-to-vault, small APR/cash-back wins, **always hear an agent's well-researched brief in full**. Auto-no: new subscriptions w/o cooldown, same-day financial commitments, late-night past 21:00, sacred-first-hour violations, investing without a research pass, **and any scolding/guilt-tripping copy from agents about missed habits or tasks**. Tiebreakers: cheaper alternative w/ great reviews → capture-and-revisit → sleep on it. "Done" lives in the vault and (eventually) renders in the life-systems-hub UI. See [USER.md](USER.md).

## Dependency Map Summary

No human collaborators in the operational sense — solo domain. Loved ones (girlfriend, parents, cousins, friends) influence rhythm via pivots, not execution. **Claude + Anthropic = true collaborator.** Load-bearing non-AI tools: Obsidian, Apple Notes, Chase app, Bilt app, Apple Health/Workouts, personal Gmail, sparse personal Calendar. Load-bearing models today: local `gemma4` + `phi4-mini` on Mac Mini for finance categorization (personal data stays local); NotebookLM + NotebookLM MCP for research organization. Inbound: The Block's API key (crypto data). Target build: Perplexity API + Gemini Deep Research MCP + Coinbase agentkit + open-source deep-research models. Three-machine topology has minimal coupling — Mac Mini is the agent hub but pivotable; iPhone + Apple Watch are the only hard dependency (fitness logging only). Single sources of truth (target state): aggregated CSV/Excel for finance, Apple Fitness for fitness (MCP gap), Obsidian for tasks/notes, `vault/00_inbox/` → `vault/40_knowledge/concepts/` → topic sub-folders for research. Pile-ups: investment/savings decisions (biggest) + learning-thread hopping (structural, not disciplinary). See [SOUL.md](SOUL.md) Part A.

## Institutional Context Summary

Sacred cows: sacred first hour, 21:00 bed, no scolding ever, personal data stays local, gym block, Obsidian-canonical, every-dollar-counts (small income streams compound), and capture-and-defer (with the breakthrough carve-out). Tone: calm, factual, zen. The #1 anti-pattern to avoid is fitness-app-style nagging ("you should walk / meditate / drink water"). Disagreement framing: always "here's an alternative to consider," never confident "you're wrong." Past landmines: going too big too fast on agent fleets (build one at a time, validated tools, observed behavior, then move on); Rocket Money dropped to build a personal version; budget caps set too tight on early agents → immediate failures (raise the cap, don't retry harder); learning-class hopping (frame plans as modular/project-based, do not lecture). Week-one tacit knowledge: every win counts, learn together, never angry at mistakes, research → understand → test → execute, celebrate then push, enjoy the process, ask questions, open to collaboration. See [SOUL.md](SOUL.md) Part B for the full Tier-A/B/C "things Claude has learned about Sean" register.

## Active Leverage Points

Where small effort produces disproportionate output:

1. **Agent research fleet (highest leverage).** Multi-agent setup spanning Perplexity API, Gemini Deep Research MCP, NotebookLM MCP, The Block's crypto API, GitHub/Reddit/YouTube/blog scraping → consolidated research briefs with summary + recommended action + path to execution. Unblocks the biggest pile-up (investment/savings decisions) by collapsing "research from scratch" into "read the brief, pull the trigger."
2. **Monthly 15th finance check, fully automated.** Pulls all statements, categorizes via local models, writes a structured vault note. Sean reviews async.
3. **Quick-capture routing.** Anything dropped to `vault/00_inbox/` (webclipper, random thought, Apple Notes promote) → indexed to `vault/40_knowledge/concepts/` with YAML → mature topics promoted into their own sub-folder. Removes the "where does this belong?" friction.
4. **Single-reminder cadences over recurring nags.** FantasyPros: one nudge end-of-January, none in August. Habit logs: morning surfacing, never push-notification reminders.
5. **Build-don't-buy multiplier.** Every personal app/agent saves money + teaches a skill + becomes a portfolio piece (career-transition aligned).

## Known Bottlenecks

What limits Sean's throughput in this domain:

1. **Autonomous agents lack MCP tools + API keys (CRITICAL, top fix).** `[DEFERRED] Slack MCP unavailable in headless mode` and `[DEFERRED] Calendar MCP unavailable in headless mode` are landing in the daily note. Either the headless SDK gains MCP, or autonomous agents gain alternate auth.
2. **No real-time finance read.** Until something Rocket-Money-style is wired, finance check stays monthly. Agents can't proactively flag anomalies between statement closes.
3. **Investment/savings decisions pile up.** Sean self-blocks here — solved by agent research briefs landing in the right format.
4. **Boston medical/dental/barber search.** Self-blocking because "it'll eat my whole day." Agents can shortlist + prep scheduling; Sean books.
5. **Junk mail in personal Gmail** persists despite past audits. Inbox sweep is recurring chore.
6. **Two-Google + inbound third Claude-Code-via-Block account** is going to compound context-switch cost. Needs a session-start "which account am I in" routine.
7. **Vault tree lags skill targets** — `vault/02_Areas/Finance|Health|Productivity` don't exist despite skills writing there.
8. **Sparse life-systems memory** in `memory/` — mostly Alienware infra. Need entries for no-scolding rule, 15th-monthly cadence, capture-and-defer, weekend-gym hard rule, FantasyPros end-of-January reminder.
9. **Stale time-bounded rules** in skill frontmatter (4:45 AM legacy wake; "Apartment Cleanup through March 20, 2026"). Tech debt.

## Cross-Domain Bleed

What spills between life-systems and other domains:

- **Life-systems → the-block.** Sleep, gym, sacred first hour, and decompress block all directly govern the energy Sean brings to Block work. A blown habit week shows up as flat focus during 09:00–14:00 deep work. Boston medical/dental search displaces deep-work hours when not delegated.
- **the-block → life-systems.** Block API key (inbound) becomes a life-systems crypto-research input. Block-issued Claude Code account (inbound) adds dual-auth complexity to life-systems agents. Rippling pay stubs (work) feed life-systems finance sheet. Block compliance windows (e.g., crypto trading restrictions for employees) intersect with personal investing decisions — agent should check this rule before recommending crypto moves.
- **Life-systems → creative-studio.** Time leftover from automated life-admin is a candidate input for creative work (16BitFit, Remotion, animation portfolio, festival pipeline). Agentic-workflow learnings cross-pollinate.
- **creative-studio → life-systems.** ComfyUI / open-source generation tooling overlaps with life-systems-hub UI ambitions. Animation-producer career arc lives in creative-studio but the "build cushion / multiple income streams" framing in life-systems is what makes the career-transition runway financially safe.

## Current Open Questions

Things Sean himself flagged as "I should figure this out":

1. **Free + paid API + MCP audit.** Catalog the research firepower options (crypto, stocks, prediction markets, finance data sources) so Claude has the right tools.
2. **Agentkit spend ceiling per agent.** Where's the line between "small autonomous move" and "final spend decision"? Resolved per-agent based on observed usage; defaults err toward breathing room.
3. **Real-time finance read.** What's the path to a Rocket-Money-style live view of Chase + Bilt without reintroducing a paid subscription Sean churned away from?
4. **Apple Fitness MCP / CLI bridge.** Doesn't exist today; needs to be built or sourced.
5. **Apple Notes ↔ Obsidian MCP / community plugin.** So quick-captures don't strand in Apple Notes.
6. **Vault → life-systems-hub UI linkage.** React + Vite + Tailwind v4 dashboard that renders the vault as a "save file."
7. **Subscription re-audit.** Sean flagged the 2026-02-27 audit as due for refresh.
8. **Open-source deep-research models** — which one(s) earn a slot in the research fleet alongside Perplexity + Gemini Deep Research?

## Related Artifacts

- HEARTBEAT (Layer 1 — operating rhythms): [[HEARTBEAT]]
- USER (Layer 2 — recurring decisions): [[USER]]
- SOUL (Layers 3+4 — dependencies + institutional knowledge): [[SOUL]]
- Schedule rules (Layer 5 — friction-derived recommendations): [[schedule-recommendations]]
- Tier-0 identity: [[Sean-Winslow-Full-Personal-Context-v2.0|Full Personal Context]]
- Domain CLAUDE.md: [life-systems/CLAUDE.md](../../../../life-systems/CLAUDE.md)
- Sister-domain operating models: [the-block](../the-block/), [creative-studio](../creative-studio/)
