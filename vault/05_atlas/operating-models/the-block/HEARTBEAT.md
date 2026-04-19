---
type: operating-model
artifact: HEARTBEAT
domain: [the-block]
status: draft
last_interviewed: 2026-04-19
created: 2026-04-18
review-date: null
ai-context: "Operating rhythms for Sean's day job at The Block (crypto/ETF company). Populated by the work-operating-model skill. Consumed by meeting-defender and daily-driver."
---

# HEARTBEAT — The Block

## Daily Rhythm
- **Wake / first hour:** 5:15–5:30 AM wake (post-Boston move). Gym opens 7:00 — leave 6:50, home 8:15–8:30. Breakfast, start work 8:45–9:00.
- **Sacred first hour (8:45–9:45):** Daily Driver SDK agent fires at 8:45 AM and drafts the Obsidian day note. I then run the `daily-driver` skill in Claude Code to pull Gmail, Slack, Granola transcripts, Google Calendar, and yesterday's Obsidian notes into a prioritized view. Mixed with AI news + light crypto reading.
- **Deep-work block:** 9:00 AM – 2:00 PM. PRD writing, Prototype-Lab iteration, skill building, deeper Jira work.
- **Lunch:** 11:30 AM – 12:30 PM, often paired with AI/YouTube learning (tools, workflows).
- **Hard decompression:** 2:00 – 3:00 PM. Off-computer. Walk or couch. No meetings here by default.
- **Execution + inbox sweep:** 3:00 – 5:15 PM. Finish in-flight work, Slack catch-up, plan tomorrow from Obsidian (check off done, add new).
- **EOD wind-down:** ~5:15 PM.

## Weekly Cadence
| Day | Calendar | Off-calendar rituals |
|---|---|---|
| Mon | 10:00 Website-redesign Product/Design sync (temporary) | Plan the week from Obsidian |
| Tue | 09:30 Campus team sync (starts 2026-04-28) · **10:00 Daily Standup (I lead)** · 13:00 Product/Design weekly | — |
| Wed | 09:30 Brand/Media/Product sync · **10:00 Daily Standup (I lead)** · 10:45 Media team / daily-show sync | — |
| Thu | **10:00 Daily Standup (I lead)** | — |
| Fri | — (lighter day) | Weekly Slack + Obsidian sweep |
| Sat | — | — |
| Sun | — | — |

Also recurring (day varies): weekly 1:1 with Ed; bi-weekly 1:1 with David (Campus/Sponsored Courses); bi-weekly RevOps/AdOps/GAM; bi-weekly SEO sync.

## Bi-Weekly Rituals
- **P&E update (every 2 weeks):**
  1. Run Claude Cowork + `jira-automation` skill against the "biweekly updates" Desktop folder of priors.
  2. Pull last 14 days of Jira: Done / In-flight (hold steady unless explicit Done) / Upcoming.
  3. Reconcile against Slack + Granola ("we shipped that" mentions) — **known gap, skill doesn't do this well yet**.
  4. Ed reviews/tweaks wording.
  5. CPO skims, usually approves.
  6. Post to `#ask-product-management` (C02N3UFMTEC) at **4:00 PM ET** on post day.

## Event-Driven (off-calendar)
- **ETF pipeline:** monitor `#research-etf` (C09EXM9FYAG) for researcher posts → run `etf-page-creator` skill → manually paste WordPress fields → update the ETF tracker spreadsheet. No compliance or market-open gating.

## Monthly / Quarterly
- **New CEO starts 2026-05-01.** Ed + Sean prepping a roadmap; The Block Pro revamp is the flagship pitch (biggest revenue line, not worked on in years).
- **OKRs:** Not owned yet (new-hire exemption from Nov 10 start). Expected Q2 or Q3 2026. Logged in Rippling (currently messy, pending CEO direction).

## Seasonal Shifts
- None felt yet — too new at The Block to have gone through a full crypto cycle, ETF launch wave, or conference season. Week-to-week rhythm has been stable. Revisit after 6 months.

## Sacred Blocks
- **First-hour rule (8:45–9:45):** Daily Driver agent + `daily-driver` skill only. Breaks **only** for an overnight Blocker escalated by a dev/designer to me + Ed.
- **2:00–3:00 PM decompression:** Off-computer. Do not book here.
- **Daily Standup 10:00 AM Tue/Wed/Thu:** I lead — non-negotiable.

## Email Split (this domain)
- `swinslow@theblock.co` — 100% of Block work. Meetings, Slack notifs, Jira, Confluence, Rippling.
- `sean.winslow28@gmail.com` — Zero Block work. Separation is clean.
- **Rule for calendar agents:** always query BOTH addresses, but expect Block events on `swinslow@theblock.co`.

## Open Questions Noted During Layer 1
- Get MCP access into the Daily Driver SDK agent so the morning hand-off into Claude Code isn't required.
- Make `jira-automation` bi-weekly flow reconcile Slack/Granola "shipped" signals against Jira state.
- Automate the "tweak wording" pass Ed does so it lands in the skill output.
