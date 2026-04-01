---
granola_id: defb5e37-f079-4d73-a7b4-f5dcdec369cf
title: "Unified Daily Standup"
type: note
created: 2026-04-01T14:00:04.312Z
updated: 2026-04-01T14:24:24.801Z
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
  - bvadimovich@theblock.co
  - ysmagulov@theblock.co
  - akryvanosau@theblock.co
  - sho@theblock.co
  - koliva@theblock.co
  - ramuald.vishneuski@ventionteams.com
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Unified Daily Standup-transcript.md]]"
---
### Engineering Updates

- Akryvanosau — continuing work on certification integration / sponsored courses response
	- Switched priority to sponsored courses; previous bug fixes (found by Ramuald) still pending
- Abenitez — election web tickets progressing; full page for report cards next
	- Bylines component ticket ready for review; Brave browser testing ongoing
- Bvadimovich — chart fix PR up and approved; creating dev box post-standup
	- Invalid URL bug found to affect more than just price pages
- Brian Mendoza — debugging pre-bid / OneTrust issue; limited tooling makes it slow
	- Pre-bid testing: confirmed dev environment not viable; production was used for prior regression testing
- Mhulis — election hub fixes done; homepage election banner complete
	- Blinking “live” label feasible but requires Serena to update original images; performance impact assessed as minimal
- Mlozuk — working on recirculation block + disappearing ad close button fix
	- Close button disappears on scroll; hard to reproduce — appears tab-timeout related
- Ysmagulov — deploying iOS onboarding portion of Campus LMS today
	- Josh back; assets being gathered for Apple submission

### Sponsored Courses / Campus LMS — Sign-in Flow

- Concern raised: postponing email verification creates UI and backend complexity
	- Certs currently generated once conditions are met (course passed or completed) — postponed verification disrupts this
- Proposal: unify the new sign-in review screen (profile pic, name, email) for both X sign-in and regular email sign-in
	- Email field non-editable for email sign-in; minor copy adjustments needed
	- Sean confirmed this direction makes sense
- Wallet address collection: originally requested by Polymarket to collect wallets via sponsored courses
	- Consensus: skip for now — optional field, low likelihood of genuine submissions, risk of discouraging participation
- New UI (success screen / certificates): confirmed for sponsored courses only, not general rollout
- Designs reviewed mid-standup — confirmed refined and workable; no further consolidation needed

### SEO & Infrastructure

- Ramuald flagged two Cora tickets needing ownership while Michaela is out:
	- “Page size exceeds Google’s 2MB crawl limit” — Sean noted this should be resolved; likely a legacy/migration artifact; assigned to Sean
	- Structured data schema validation error in hreflang
- Traffic sliding over last two weeks of March
	- Slight drop in weekly/monthly users in Google Analytics around March 17th
	- Not clearly Google core update-related (rollout still in progress)
	- No red flags in hreflang data yet; monitoring via Looker dashboard
- Cdaumur — removed all Terraform Cloud workspaces to avoid new costs (cost feature active today)
	- Removed unused Google Admin accounts to reduce spend
	- AWS forecast for this month: $18,000 — $3,000 over prior month
	- New task created: find free/alternative Terraform Cloud solution and migrate

### Action Items

- Sean Winslow
	- Review Figma success-stage screen and confirm design completeness
	- Follow up with Nikita and Akryvanosau on new sign-in UI direction and email verification flow
	- Take ownership of the page-size crawl limit SEO ticket
	- Monitor Looker dashboard for further traffic drop signals
- Bvadimovich
	- Create dev box for positive/negative indicators ticket after standup
- Ysmagulov
	- Deploy iOS onboarding for Campus LMS today; coordinate with Josh on Apple submission assets
- Cdaumur
	- Investigate $3K AWS cost increase
	- Identify and implement free alternative to Terraform Cloud
- Ramuald Vishneuski
	- Continue testing new payment flow; progress auto-test work

Chat with meeting transcript: https://notes.granola.ai/t/03027b25-0332-4663-909c-92ae81328655
