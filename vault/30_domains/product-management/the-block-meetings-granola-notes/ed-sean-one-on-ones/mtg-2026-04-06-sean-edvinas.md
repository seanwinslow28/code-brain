---
granola_id: 58a6a9d2-c492-41f8-b298-56963e1b636e
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: "1:1 with Ed covering sean / edvinas."
context: the-block
created: 2026-04-06
source: granola-sync
attendees:
  - erupkus@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Sean _ Edvinas-transcript.md]]"
---

### Zapier Testing

- Added PDF steps; running another round of tests to confirm nothing is broken
- Will share update async as the day progresses
- Prefer to present only when fully complete with no issues

### AI Automation & Priorities

- 12–1pm: meeting to discuss AI implementation (e.g. ETFs use case)
- Matt suggested prioritising WordPress integration over other flows
	- No publish rights needed — run via Slack commands, confirm each action, lands as draft in WordPress
- Job board integration: close to signing a contract with a provider
	- Requires specific API to pull listings and push applications
	- Erupkus working on this for the rest of today

### GA4 / Data Layer Investigation

- Erupkus spent most of Friday trying to build a funnel exploration in GA4 — unresolved
	- 40K homepage sessions recorded, but almost no subsequent page views to other URLs
	- End condition (exclude homepage URLs) still returning homepage — behaviour unexplained
	- Likely cause: undocumented Tag Manager setup from a consultant ~3 years ago; no documentation exists
- Broader data quality concern: GA4 setup is outdated, undocumented, team always “shrugging shoulders” on data
- Plan: loop in Brian to inspect what’s firing under the hood in Tag Manager and GA4

### iOS App Ads

- Placing iOS app ads on the homepage
- Erupkus working with Josh; Josh joining in ~15 minutes
- Goal: ship while the relevant people are available

### Next Steps

- Sean
	- Run full Zapier test suite after this meeting; update Erupkus async
	- Work on the “pro idea” today ahead of a follow-up sync with Erupkus
	- Attend Brian/GA4 investigation call when scheduled
- Erupkus
	- Reschedule AI discussion to Wednesday
	- Finish editing the deck (visual upgrades remaining)
	- Reach out to Brian to schedule GA4/data layer call — include Sean
	- Complete job board API integration today
	- Coordinate with Josh on iOS app homepage ads; loop in Sean once Josh is on

Chat with meeting transcript: https://notes.granola.ai/t/7ba68e7d-7ef4-4cce-ac72-722751559324
