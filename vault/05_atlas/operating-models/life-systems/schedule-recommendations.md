---
type: operating-model
artifact: schedule-recommendations
domain: [life-systems]
status: confirmed
last_interviewed: 2026-04-22
created: 2026-04-18
review-date: null
ai-context: "Friction-derived schedule and automation rules for personal systems. Consumed by meeting-defender and future calendar/automation agents. North star: make Sean more financially secure via agent leverage."
---

# Schedule Recommendations — Life Systems

## The Extra Hour — North Star

**If Sean had +1 hour every weekday in life-systems, it goes to finance — learning about it and putting the learnings into action.**

Why this matters (Sean's framing, preserved):

> Life is chaotic and careers are fragile. Things can be going well at work, but we could be bought out and laid off in the blink of an eye. I need to know that if anything like that ever happened, or if there was a medical emergency, or anything else that would have me financially struggling, that I have a cushion and other avenues of income so that I can put food on the table. I don't want me, my girlfriend, my family, or my friends to ever struggle. I want to be the person that they can come to if they're ever in trouble.

**Implications for every automation below:**
- Every minute saved from habit logging, inbox triage, or admin must be reinvestable in finance (research, decision execution, capital deployment).
- Habits/workouts are the **motivation layer**, not the goal. They support the financial work, not compete with it.
- Scope of care is **self + girlfriend + family + friends** — agent recommendations should respect that Sean is trying to build a cushion for multiple people, not just himself.
- Sean cannot do this alone. Claude + agent fleet must take on tasks Sean can't get to.

---

## Protect

Calendar-level and interaction-level defenses. Rules take the form *When X, then Y*.

- **When** any proposal would violate the **sacred first hour (05:30–06:30)**, **then** reject outright. Exceptions: sickness, extraordinary work day, gym injury recovery.
- **When** any proposal would violate the **gym block (weekday 07:00–08:00)**, **then** reject unless Sean explicitly overrides.
- **When** any proposal would violate the **decompress block (14:00–15:00)**, **then** reject — this is a protected no-computer slot.
- **When** any proposal would cross the **21:00 bed window**, **then** auto-no.
- **When** proposing weekend activity, **then** never suggest "squeeze in a weekend workout." Weekend gym is a hard no-suggestion rule. Sean decides. If he goes, he logs it — agents celebrate the surprise with bonus XP, not a reminder.
- **When** surfacing a financial anomaly, **then** output as a structured markdown table (HIGH z>5 / MEDIUM z>3 + category averages). Never ask Sean to review in the moment — he reviews async.
- **When** agents surface research, **then** preserve the full brief. Never truncate — Sean wants the complete read even when he disagrees with the headline.
- **When** communicating tone, **then** calm / factual / zen. Never nag. Never scold. Never "you should."
- **When** disagreeing with Sean, **then** phrase as "here's an alternative to consider." Never confident "you're wrong, do this instead."
- **When** working with personal financial or health data, **then** route through local models (`gemma4`, `phi4-mini` on Mac Mini). Never ship to cloud without explicit approval.
- **When** a calendar pull is needed, **then** query `sean.winslow28@gmail.com` only. The prior `swinslow@theblock.co` work calendar was archived 2026-05 with the Block layoff. Do not query it.

## Automate

Manual work that should become agent-triggered. Ordered roughly by leverage.

- **Monthly finance check (15th).** Agent pulls Chase bank + Chase credit + Bilt credit + Rippling pay stub data, categorizes via local models, writes a structured vault note. Sean reviews async.
- **Deep-research synthesis** (the single biggest time sink). Agent fleet spans GitHub, YouTube, Reddit, Twitter, blogs, articles, Perplexity API, Gemini Deep Research MCP, NotebookLM MCP, and The Block's crypto API. Produces: research summary + recommended action + path-to-execution. Delivers into a per-topic sub-folder under `vault/40_knowledge/`. Breakthrough findings interrupt (notify Sean); ordinary findings accrue quietly for the 15th-of-month review or the weekly driver.
- **Habit logging assist.** Workout / vitamins / green juice surfaced in the `/daily-driver` morning note. Real-time only — no retroactive backfill.
- **Quick-capture routing.** Obsidian webclipper + Apple Notes → `vault/00_inbox/` → indexed to `vault/40_knowledge/concepts/` with YAML frontmatter → mature topics promoted into their own sub-folder.
- **Subscription scanning / flagging.** Ongoing. Recommendations land in USER-flavored tiebreaker form (cheaper alternative with great reviews vs. capture-and-revisit vs. kill). Sean makes the call.
- **FantasyPros seasonal reminder.** Single nudge at **end of January** to cancel for off-season. No pre-August reactivation nag. No annual cancel-and-reactivate loop.
- **Inbox hygiene.** Deep audit of `sean.winslow28@gmail.com` backlog. Unsubscribe loops, junk categorization, legitimate-but-noisy sender sorting.
- **Desktop + Apple Notes sweep.** One-time (or periodic) audit of scattered content on desktops + Apple Notes → promotable items into vault.
- **Pay stub capture.** Biweekly Rippling pay stub → vault finance sheet.
- **Bilt rewards check.** Periodic scan for available redemptions → surface as auto-yes candidates.

## Decline or Defer

Patterns that Sean should say no to or push, recognized automatically when possible.

- **New recurring subscriptions without a cooldown.** Auto-no.
- **Same-day financial commitments.** Auto-no — reroute to "capture to Obsidian and revisit."
- **Investing without a research pass.** Auto-no.
- **Fitness-app-style nagging notifications ("you should walk / meditate / drink water").** Do not replicate this tone anywhere in the agent fleet — Sean has named this as the #1 communication anti-pattern.
- **Autonomous evening daily-driver / EOD wrap-up.** Declined permanently. EOD is interactive only. Don't re-enable.
- **Weekend gym nudges.** Declined. See Protect list.
- **Scolding / guilt-tripping copy.** Declined in all forms.

## 20-Minutes-to-2-Minutes Candidates

High-leverage automation targets, ordered by annoyance × frequency.

1. **Chase + Bilt CSV pull + categorization** (monthly, 30+ min today).
2. **Raw inbox note → structured concept note with YAML + correct folder** (every capture, 10-15 min today).
3. **Deep-research synthesis across GitHub / YouTube / Reddit / Twitter / blogs → single consolidated brief** (hours today → ideally agent-produced overnight).
4. **Weekly "things I learned this week" assembly** (part of `/daily-driver` weekly review, currently not extended to life-systems).
5. **Manual habit log entry when Sean forgets to tap the Watch** (should nudge via morning note, never via push-notification nag).
6. **Finding the right vault folder for a new capture** — agent inferrer should pick the folder + propose tags, Sean confirms.
7. **Subscription cancel follow-through** (identify → draft cancel flow → Sean executes).
8. **Boston medical / dental / barber search** — agent can do the option research + shortlist + scheduling prep; Sean picks + books. Removes the "this will eat my whole day" blocker.

## Context-Switch Costs to Minimize

- **Work → personal finance** during a workday crack. Batch personal finance into the 15th-of-the-month check; do not scatter across the workday.
- **Creative / learning flow → life-admin task** (pay a bill, respond to a subscription email). Batch into the 15:00–17:15 comms/exec window or weekend.
- **Deep research thread → everyday habit logging.** Habit logging stays asynchronous; no interruption of research.
- **iPhone apps (Chase / Bilt / Apple Health) → vault.** Target: MCP/CLI bridges so data flows into the vault without hand-shuffling.
- **Research-thread organization in the vault.** Target: topic sub-folder auto-creation so a mature research thread has a home by default, not by Sean's grooming.
- **Two-calendar / two-Google-account life** (personal Gmail + Block) — and a **third Claude Code account via The Block** is inbound for PM tasks. Context-switch cost will grow. Needs a session-start routine that makes "which account am I in right now" obvious + a MCP/agent story that handles segmented-auth gracefully.

## Claude Code / Agent-Fleet Friction Points

Specific fleet issues to fix or build. Tied to the observation that autonomous agents in headless mode can't access MCP — so MCP-dependent content is missing from Sean's daily note.

- **CRITICAL — autonomous agents lack MCP tools and API keys.** Seen in the daily note:
  - `[DEFERRED] Slack MCP unavailable in headless mode — backfill in interactive session.`
  - `[DEFERRED] Calendar MCP unavailable in headless mode — backfill in interactive session.`
  Sean has flagged this as needing to change **ASAP**. Either the headless SDK gains MCP access, or the autonomous agents gain an alternate auth path for Slack / Calendar / Gmail / Atlassian. This is the top agent-fleet friction point for life-systems today.
- **Budget caps set too tight on early agents** caused immediate hit-cap-and-fail. Precedent: daily-driver bumped from $0.25 → $0.50 after real usage showed $0.29 at 9 turns. Default: **err on the side of breathing room** — especially for new agents whose real usage is unknown.
- **One-agent-at-a-time build discipline.** Do not mass-deploy agents without validated system prompts, verified tools, and observed behavior. This came from burning cycles on under-specified agents that errored silently.
- **Stale time-bounded rules.** Example: `daily-driver` SKILL.md still references "Apartment Cleanup through March 20, 2026" post-move. Time-bounded rules must be pruned after expiry.
- **Stale wake-time references.** Skills (`time-management`, `health-habits`) still show 4:45 AM. HEARTBEAT at 05:15–05:30 is current truth. Flag as frontmatter tech debt.
- **Vault `Areas/` subfolders** (Finance, Health, Productivity) don't exist despite skills writing to those paths. Vault tree lags skill targets — either create the folders or point the skills elsewhere.
- **Life-systems memory is sparse** — only the Alienware networking feedback is present in `memory/`. Candidate new memory files: no-scolding rule, 15th-of-month finance cadence, capture-and-defer default, weekend-gym hard rule, FantasyPros end-of-January reminder.
- **Target build — API/MCP audit.** Catalog free + paid APIs + free + paid MCPs that would maximize Claude's research firepower (crypto, stocks, prediction markets, personal finance). Sean has flagged this as a collaborative workstream.
- **Target build — life-systems-hub ↔ vault linkage.** The React + Vite + Tailwind v4 UI at [life-systems-hub](../../../../../life-systems-hub/) needs vault wiring so all habit/finance/research data renders in a "save file" dashboard view.
- **Target build — Apple Notes ↔ Obsidian MCP or community plugin** so quick-captures don't strand in Apple Notes.
- **Target build — Apple Fitness ↔ Claude MCP or CLI bridge** so fitness data flows into the vault without manual export.
- **Target build — agentkit wallets with spend ceilings.** Open question: per-agent dollar cap for autonomous financial moves. Resolved per-agent based on observed usage, with breathing-room defaults. Sean and Claude to refine together as agentkit comes online.
