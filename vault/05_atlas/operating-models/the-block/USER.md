---
type: operating-model
artifact: USER
domain: [the-block]
status: draft
last_interviewed: 2026-04-19
created: 2026-04-18
review-date: null
ai-context: "Sean's recurring decisions and prioritization patterns for The Block. Populated by the work-operating-model skill. Consumed by daily-driver, process-inbox, sprint-health."
---

# USER — The Block

## Decisions Made 3+ Times Weekly
- **"Slow or unresponsive?"** — Is a dev / designer / David Campus-side actually blocked on something of mine, or just moving at their pace across time zones? Has escalated to written CYA communication logs twice; expect more.
- **"Escalate or handle?"** — Default: keep Ed in the loop on almost everything. Exception: Campus-side calls I'm confident on → I make the call, tell Ed after (he usually agrees).
- **"Build or buy/Zapier or Claude?"** — Ongoing migration: new automations go to Claude Code / skill-building; Zapier only for in-place workflows, trending down.
- **"Accept this meeting invite?"** — Current default is yes for almost anything, while still new.
- **"Does this Jira ticket need me?"** — Any comment or question on a ticket I wrote is mine to unblock.

## Real Prioritization Criteria
_In my own words, ordered by what actually wins:_
1. **Ed-signal** — whatever Ed surfaced most recently as "focus on this."
2. **Closest to shipping** — bias toward the thing about to go out.
3. **Unblock someone else** — even during a high-priority Ed task, I'll pivot for a beat if a dev/designer is stuck waiting on me.
4. **Deadline pressure** — tight deadline outranks no-deadline.
5. **Leverage R&D** — when there's no clear priority: Claude skills, PM-automation workflows, agent×crypto product research (x402, wallet-agent intersections for future Block product/API revenue).

## Auto-Yes
- Anything Ed (manager) or Matt (CPO) directly asks me to work on.
- Any dev/designer comment or question on a ticket I wrote.
- Every meeting invite — while still new, optimizing for learning + meeting coworkers. Only miss for hard schedule conflicts.
- Overnight Blocker escalation (only thing that breaks the sacred first hour).

## Auto-No / Defer-to-Later
- **RevOps/AdOps favors** — not my jurisdiction; I always get to them, but they're never high-priority. They come to me because I know Claude / Zapier / AI tools.
- **Salesforce Campus user/client emails** — check on occasion; rarely urgent.
- (No reflexive "decline meeting" pattern yet — still new-hire mode.)

## Daily Investment Heuristic
- **Ed-signal + deadline** tasks first, always.
- **Drained but no deadline** → pivot to Prototype-Lab / skill-building to keep the day interesting.
- **Genuinely low energy** → clear Ed/deadline work first, then step away. Recovery path = better sleep + food, not pushing through.

## Agent Delegation
**Aggressive trust posture — willing to delegate most things if guardrails are tight, intent-engineering is clean, and voice/workflows are encoded.**

**Already trusted to agents:**
- Daily Driver — morning Obsidian prep (8:45 AM SDK agent + interactive `daily-driver` skill).
- `jira-automation` — bi-weekly P&E update draft (still has a Slack/Granola reconciliation gap to close).
- `etf-page-creator` — WordPress field prep; I paste to CMS.
- Ticket drafting, PRD drafting, response drafting for Jira/design questions — always with my review pass before it goes out.
- Claude-as-substitute-for-bombarding-Ed on "how would a real PM handle this?" questions (career pivot from 10 yrs of multimedia management).

**Hard never-delegate:**
- **The Block's GitHub** — I don't have access and can't make PRs; agents definitely don't.
- **The Block's WordPress backend** — I have access but refuse agent write access. "If something went seriously wrong, the company goes dark and I'd be out of a job."

**Review gate rule:** Everything an agent drafts gets my eyes before it leaves Claude. Hallucination check is non-negotiable.

## Tiebreakers When Unsure
1. Write both options into Obsidian so I don't lose them.
2. Review after the day's meetings are done.
3. Still stuck?
   - Strategy/priority question → ask Ed.
   - Design question → Slack the designer directly.
   - Dev question → Slack the dev directly.
4. Default tiebreaker: pick the option that unblocks someone else.

## Definition of "Done" in This Domain
- **Jira ticket:** acceptance criteria met, linked to Epic, correct components + labels, per the `jira-automation` quality checklist.
- **Bi-weekly P&E update:** Ed tweaked wording → CPO approved → posted to `#ask-product-management` at 4:00 PM ET. Format: "Done / In-flight / Focus for upcoming months," grouped by product area (`.Co`, `Campus`, `DevOps`, `iOS app`, etc.).
- **ETF page:** all WordPress fields validated + pasted (per `etf-page-creator` skill) + ETF tracker spreadsheet row updated.
- **PRD:** canonical reference = Sponsored-Courses-PRD.pdf. Pattern to extract + encode into `prd-generator` when that skill is next tuned for Block.
- **Workflow/skill:** shipped into `.claude/skills/` with trigger phrases + a tight intent spec + at least one real-world dry-run before I rely on it.

## Career-Context Flag
- I'm transitioning into PM from a decade of multimedia management. I intentionally use Claude Code as a senior-PM stand-in to avoid over-asking Ed. This shapes what I delegate and how hard I push on intent-engineering.
