---
type: operating-model
artifact: USER
domain: [life-systems]
status: draft
last_interviewed: 2026-04-21
created: 2026-04-18
review-date: null
ai-context: "Sean's recurring decisions and prioritization patterns for personal systems. Life-systems is centered on personal financial advisory + research; habits and quick-capture are supporting layers. Consumed by daily-driver, process-inbox."
---

# USER — Life Systems

## Decisions Made 3+ Times Weekly
- Did I work out today? Was it logged?
- Did I take vitamins / drink green juice?
- Is this transaction worth keeping or is it a subscription to kill?
- What goes on today's task list vs. gets deferred to later in the week?
- Was a research-worthy idea surfaced (web / email / conversation)? → capture to vault.
- Should I dig into a captured idea myself today or hand it to a research agent?

(Note: this domain's *center of gravity* is finance + research, not habits. Habits are the steady drumbeat that keeps focus and motivation; finance and research are where the leverage lives.)

## Real Prioritization Criteria
**Ranking when life-systems items compete:**
1. Research dive on a money-making idea (highest)
2. Financial deadline (statement close, payment due)
3. Habit streak / log

Money-leak only jumps the queue if it's a true emergency (rare — should be near-zero in normal operation).

Money-making research surfaces are **capture-and-defer**, not drop-everything. The captured idea is the unit of work; agents do the heavy lifting in the background.

## Auto-Yes
- Bilt reward redemption when one is available
- Cancel a flagged subscription
- Log the workout / vitamins / green juice
- Capture a research seed to Obsidian
- Small cash-back / APR optimization
- **Always hear an agent out on an idea or plan when it has done extensive research** — even if I disagree, the briefing happens

## Auto-No
- New recurring subscription without a cooldown period
- Any financial commitment the same day it's pitched
- Late-night commitment that breaks the 21:00 bed window
- Anything that violates the sacred first hour
- Investing in something without a research pass first
- **Claude scolding / guilt-tripping about missed habits or tasks.** If I skip the gym or skip a habit log, acknowledge it, re-add it to the list, move on. No "you should be getting this done" framing. Ever.

## Daily Investment Heuristic
- **Habit log** → surfaced in `/daily-driver` morning note every day
- **Finance check** → **monthly, on the 15th** (all statements posted + payday landed). Until a Rocket-Money-style real-time read on Chase + Bilt is wired up, daily finance logging would defeat the point of agents
- **Research dive** → triggered by (a) a new raw idea note dropped into the vault, or (b) Sean asking the `last30days` skill to scan for fresh opportunities

## Agent Delegation

**Already trusted (today):**
- Transaction categorization via local models (gemma4, phi4-mini — personal data stays local)
- Habit-log assist
- Subscription scanning / flagging
- Research summarization
- Quick-capture filing into the vault

**Middle ground (drafts, Sean decides):**
- Research reports + recommended actions
- Subscription kill/keep recommendations
- Money-making idea evaluation + path-to-execution plans

**Future state (agentkit-enabled):**
- Agents with their own wallets executing small financial moves based on accumulated vault knowledge and research (Coinbase [agentkit](https://github.com/coinbase/agentkit.git))
- Multi-agent research fleet: Perplexity API agent + Gemini Deep Research MCP agent + open-source deep-research models, coordinated to produce reports + execution plans
- Agents that compound — their context, history, and judgment improve over time
- Anchoring skills for the build-out: [intent-engineering](../../../../.claude/skills/intent-engineering/), [last30days](../../../../.claude/skills/last30days/); new skills welcome

**Never delegated:**
- Final spend decisions
- Medical decisions
- Anything about the relationship
- Career-direction calls

## Tiebreakers When Unsure
1. Default to the **cheaper alternative with great reviews**
2. If still unsure → **capture to Obsidian and revisit** (don't pull the trigger)
3. Sleep on it before any non-trivial commitment

## Definition of "Done" in This Domain

**All "done" states live in the vault** in their respective locations.

| Ritual | Done means |
|---|---|
| Workout | Logged via health-habits skill into the vault |
| Habit streak | Tracked via health-habits skill (CSV + streak calc) |
| Monthly finance check (15th) | All txns categorized for the prior month, statement closed, vault note written |
| Research dive | Vault note exists with: research summary + recommended action + path to execution |
| Weekly learned-log | Running note in vault, tagged captures retrievable by future agents |

**Future consumer:** [life-systems-hub](../../../../../life-systems-hub/) React UI (dark, RPG-flavored shadcn dashboard — "Linear's data density meets Diablo's character screen"). Goal: vault → hub linkage so all the above renders as a "save file" view.
