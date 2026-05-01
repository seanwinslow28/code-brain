---
granola_id: a73c58af-1980-446c-90ed-347285e5e081
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Campus team sync on campus sync.
context: the-block
created: 2026-04-28
source: granola-sync
attendees:
  - ddebreczeni@theblock.co
  - mvitebsky@theblock.co
  - erupkus@theblock.co
  - mhulis@theblock.co
  - mprice@theblock.co
  - norobenko@theblock.co
  - rvishneuski@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Campus Sync-transcript.md]]"
---

### Sponsored Courses — Login & Identity Blockers

- Core issue: users who registered via Crypto IQ can’t log into regular campus
	- Root cause: missing multi-auth sign-in flow (front end only; backend largely done)
	- Secondary issue: users previously invited as interviewees or KOLs can’t reuse that email if signing in via Twitter
- Proposed near-term fix (Nikita’s plan): filter out Crypto IQ and guest-role users during normal campus sign-in
	- If a user has no normal account outside Crypto IQ/guest roles, auto-issue them a standard user
	- Avoids needing to build multi-profile auth now
	- Doesn’t fully close the problem — multi-auth still needed long-term
- Crypto IQ user records: likely to be wiped entirely
	- Leadership unlikely to care about preserving Crypto IQ history
	- Wiping eliminates the Crypto IQ identity conflict entirely
	- Sean to confirm with leadership before proceeding
- Multi-profile auth: still required eventually, but not blocking near-term launch
	- Estimated ~1 week to build if needed
	- Risk of releasing two features simultaneously flagged as concern

### Twitter Account Guard & QA Requirements

- Same Twitter guard logic from Crypto IQ will apply to sponsored courses
	- Requirements: 90-day-old account, 50+ followers, 30+ tweets, no private profiles
	- Private profile filtering may be dropped — less relevant since card-sharing tracking isn’t active
	- Bot protection considered sufficient via existing criteria
- Whitelisting logic already architected — can reuse for manual profile additions

### Enterprise Bugs (201 Tickets)

- Ddebreczeni resolved all bugs flagged by Roma
	- All three courses updated on prod
	- Dev box exports may need separate update — Roma primarily tests on dev

### Wallet Collection Export

- Admin panel now supports CSV exports of: wallets, emails, Twitter handles
- Wallet editing/adding feature going to Roma for testing today

### Next Steps

- Sean
	- Check with leadership on wiping Crypto IQ user records
	- Monitor Nikita’s login fix progress; pivot to multi-auth if needed
- Norobenko (Nikita)
	- Implement sign-in filter to unblock Crypto IQ and KOL/interviewee users
	- Add manual profile whitelisting at backend for Twitter guard
	- Send wallet/editing feature to Roma for testing after this call
	- Fix query progress tracking and certificate generation bugs
- Ddebreczeni
	- Send dev box exports to Roma so all environments are in sync
- Rvishneuski (Roma)
	- Re-test enterprise (201) bugs after dev box is updated
	- Test sponsored courses after that

Chat with meeting transcript: https://notes.granola.ai/t/e0e99237-9d93-4de1-b9b1-e0136fc4acb1
