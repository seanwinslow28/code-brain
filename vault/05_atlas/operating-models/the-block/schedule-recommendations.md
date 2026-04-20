---
type: operating-model
artifact: schedule-recommendations
domain: [the-block]
status: draft
last_interviewed: 2026-04-19
created: 2026-04-18
review-date: null
ai-context: "Friction-derived schedule and automation rules for The Block. Populated by the work-operating-model skill. Consumed by meeting-defender and future calendar agents."
---

# Schedule Recommendations — The Block

## Protect
_When X, then Y. Calendar-level defenses._
- **When** a meeting invite lands between **8:45–9:45 AM ET**, **then** decline or reschedule — first-hour rule (Daily Driver + `daily-driver` skill).
- **When** a meeting invite lands between **2:00–3:00 PM ET**, **then** decline — off-computer decompression is mandatory.
- **When** Tue / Wed / Thu **10:00 AM ET** conflicts with anything, **then** the Daily Standup wins (I lead it).
- **When** post day of the bi-weekly P&E update, **then** hold the 3:00–4:00 PM ET block for final wording + CPO review + 4:00 PM ET `@here` post to `#ask-product-management` (C02N3UFMTEC).
- **When** Ed DMs (`D09RWHRC9HC`), **then** treat as immediate-response regardless of block — soft exception only during active lunch / break.
- **When** an overnight Blocker is escalated by a dev or designer to me + Ed, **then** allow it to break the sacred first hour (only whitelisted exception).

## Automate
_Manual work that should become agent-triggered. Each item traces to a Layer 5 answer._
- **Jira ↔ Slack/Granola reconciliation in the bi-weekly P&E draft** — teach `jira-automation` to cross-check "we shipped X" mentions in Slack / Granola against Jira ticket state before adding to Done / holding in In-flight.
- **Encode Ed's wording-tweak pass** into `jira-automation` output so his edits become the default voice.
- **Slack-triggered ETF pipeline:** when a post lands in `#research-etf` (C09EXM9FYAG), auto-fire `etf-page-creator` pre-research → queue output for Sean's paste pass. Current flow: VPN on → `http://theblock.co/edit` → manual skill invocation.
- **ETF tracker Google Sheet auto-append** after `etf-page-creator` runs successfully.
- **Cross-meeting topic indexer:** an agent walks Granola transcripts, detects recurring topics, and maintains a `topic → transcripts` lookup so Sean doesn't re-read to answer "what did we say about X?"
- **GA4 read access via Google OAuth** in Claude Code — ask Claude for metrics instead of hunting.
- **Meeting-update → ticket backflow:** an agent drafts ticket updates from meeting transcripts, flagging ambiguous parts for Sean rather than guessing.
- **Figma-to-ticket pipeline:** resolve the `.fig` download / personal-account workaround. Target: a Claude workflow that ingests designs without requiring a Block Dev-Mode seat (current manual workaround is deliberate — no Dev seat requested).
- **Colleague-automation migration off Zapier:** build a Claude-Agents-SDK-or-Claude-Code-controlled replacement for the Zapier workflows Sean is asked to build for colleagues. Zapier is unreliable and LLM-hostile.
- **Nano-Banana-2-powered diagram agent** for embedding diagrams in PRDs / Confluence docs.

## Decline or Defer
_Patterns Sean actively defers or should decline._
- **RevOps / AdOps favor requests** (Zapier builds, Karla's GA4 asks, etc.) — defer to low-priority queue; never drop the Ed-signal or shipping work to do them.
- **Salesforce Campus user / client email replies** — batch at a set time; not real-time.
- **Ticket clean-up / grooming passes** — known to get delayed; schedule explicitly rather than wait to "feel like it."
- **Being a silent attendee in meetings** — not yet triggered (still in new-hire "attend everything" mode); re-evaluate this rule at the 6-month mark post-Nov 10 start (i.e., after 2026-05-10).

## 20-Minutes-to-2-Minutes Candidates
_Highest-leverage automation wins from Layer 5 Q1._
1. **Jira ↔ Slack/Granola reconciliation** in the bi-weekly P&E draft.
2. **Cross-meeting transcript topic indexer.**
3. **GA4 via Google OAuth** inside Claude Code.
4. **Figma → ticket pipeline without Dev-Mode seat.**
5. **Colleague-automation migration Zapier → Claude-built workflows.**
6. **Slack-triggered `etf-page-creator`.**
7. **ETF tracker spreadsheet auto-append.**
8. **Meeting-update → ticket backflow.**

## Context-Switch Costs to Minimize
- **Meeting cluster → Slack / ticket writing** — biggest drain. Immediate post-meeting focus required to capture details + citations; Claude silently adds out-of-scope stack assumptions that must be scrubbed. **Mitigation:** batch ticket writing into a dedicated 20-minute block after meeting clusters rather than interleaving with Slack; run a `ticket-scrub` pass that flags stack-assumption drift.
- **Three-machine hopping (Mac Mini / MacBook Pro / Alienware)** — especially mid-Agents-SDK experiment. Displays + unification flaky. **Open ask:** design a cleaner topology / hand-off pattern; revisit with Sean.

## Claude Code / Agent-Fleet Friction Points
_Layer 5 Q7 — these are hooks/agents to fix or build._
- **Daily Driver SDK agent has no MCP access** → Sean re-runs `daily-driver` skill in Claude Code every morning. Give the SDK agent MCP reach.
- **`jira-automation` doesn't reconcile Slack/Granola** "we shipped X" signals against Jira state.
- **`etf-page-creator` still requires manual WordPress paste** — Slack-trigger + ETF tracker auto-append both missing.
- **No `sprint-health` skill yet.**
- **`process-inbox` doesn't know about `#research-etf` (C09EXM9FYAG)** as a first-class signal channel.
- **Agent context windows forget Block-specific conventions mid-session** — need durable injection of SOUL.md + USER.md into long Block sessions.
- **Repeated Slack + Zapier re-authorization loops** — stabilize the auth pattern.
- **Zapier MCP is broader-looking than it is** — real API coverage is limited; don't rely on it for the colleague-automation migration.
- **Figma MCP path requires the `.fig` download workaround** — deliberate (no Dev-Mode seat request) but still friction.
- **Google OAuth for GA4 + Looker read access** — missing.

## The Extra Hour
_If Sean had +1 hour/day in Block work, it goes here. This is the north star for the recommendations above._
1. **Prototype-Lab** — UX flows for devs/designers; a place for Sean's design + animation instincts to feed Block work.
2. **Bulletproof Block-specific Claude skills** — tight enough that Sean's review pass shrinks to a sanity check.
3. **Real collaboration with the Media team** on their pitched ideas (see `vault/30_domains/product-management/media-team-ideas/` — Around-The-Block Globe MVP, Ambassador Program, Global Crypto Adoption Tracker, etc.). Sean's media background is latent leverage for Block revenue.
