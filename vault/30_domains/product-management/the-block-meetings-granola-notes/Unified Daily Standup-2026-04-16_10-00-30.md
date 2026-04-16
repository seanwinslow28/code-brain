---
granola_id: eb455913-fa92-4bb2-90b8-8382a8378ddd
title: "Unified Daily Standup"
type: note
created: 2026-04-16T14:00:30.454Z
updated: 2026-04-16T14:35:53.502Z
attendees: 
  - bmendoza@theblock.co
  - mprice@theblock.co
  - npivcevic@theblock.co
  - mvitebsky@theblock.co
  - erupkus@theblock.co
  - mhulis@theblock.co
  - cdaumur@theblock.co
  - vention-team
  - cpaz@theblock.co
  - abenitez@theblock.co
  - norobenko@theblock.co
  - mzhynko@theblock.co
  - mlozuk@theblock.co
  - kbaspinar@theblock.co
  - bvadimovich@theblock.co
  - ysmagulov@theblock.co
  - akryvanosau@theblock.co
  - sho@theblock.co
  - koliva@theblock.co
  - ramuald.vishneuski@ventionteams.com
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Unified Daily Standup-transcript.md]]"
---
## Private Notes

Message Claudine about wallet integration design - just another field 

## Enhanced Notes

### Development Updates & Bug Fixes

- Anna deployed fix for pages exceeding 2MB, testing data dashboards
- Stand with Crypto API returning 404 errors, blocking report cards
	- Anna to reach out to Stand with Crypto team
- Bodan completed Learn About Crypto stocks copy update (one-line change, ready to merge)
	- Fixed review items from Nikola for invalid URL and indices pages tickets
	- Working on article widget positioning across different page layouts
- Caesar progressing on migration using Atlantis instead of Terraform Cloud
- Kristoff completed LLMs txt file (ready for deploy), wording changes, timezone task updates
- Mike merging iOS changes from Matt, resolving merge conflicts to ship ASAP

### Product & Infrastructure Decisions

- Indices pages deprioritized, eventual shutdown planned
	- Price indicator changes to merge across all repos regardless of indices timeline
- Sponsored courses wallet integration approach finalized:
	- Optional wallet collection on account creation
	- Reward page to include wallet field if missing
	- CSV export to Pilot Market for reward processing
	- Message Claudine about wallet integration design - just another field
- Mobile support for campus confirmed 80% ready
	- Roma noted desktop-only testing historically, will expand if needed
- Stand with Crypto API caching layer needed when service returns
	- Nikola to implement to avoid direct dependency on external API

### Action Items

- Anna: Contact Stand with Crypto about API issues
- Bodan: Merge crypto stocks copy update, continue article widget fixes
- Kristoff: Address Nikola’s review suggestions, deploy LLMs file
- Nikola: Set up caching layer for Stand with Crypto API when available
- Bodan: Take over token homepage list ticket from Maria
- Roma: Continue auto-test optimization, discuss crypto jobs approach with Nikola

Chat with meeting transcript: https://notes.granola.ai/t/08b3d267-4bce-4cda-a93a-59ac5c34aa3e
