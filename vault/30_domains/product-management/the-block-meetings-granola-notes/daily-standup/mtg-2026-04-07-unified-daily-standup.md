---
granola_id: 84313aac-6e54-44b4-8822-deb5fc5861e0
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup.
context: the-block
created: 2026-04-07
source: granola-sync
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

### Development Progress Updates

- Election Hub Coverage
	- Anna testing added events, fixes for home page coverage and Twitter sharing preview
	- Sabrina doing VQA - getting close to completion
	- Marina and Maria working on final fixes
- Infrastructure & Performance Issues
	- Brian debugging slow degradation from last Tuesday/Thursday
		- First slowdowns in over a year
		- Caesar noticed high numbers
		- Documentation and small fixes implemented
	- Caesar migrating from Terraform Cloud to self-hosted
		- Created new repository for history bucket
		- DynamoDB table for locking
		- Testing Atlantis for GitHub integration
		- Certificate renewals needed in Azure
- SEO & Traffic Concerns
	- 20-30% drop in Google search traffic over recent weeks
		- Affecting competitors too (CoinDesk lost 2.5M traffic in April)
		- Only BeInCrypto benefiting from core updates
	- Critical issue: Google threatening to deindex pages >2MB
		- Affects all data pages
		- High priority ticket needs assignment
	- Google reporting wrong impressions data since April (being fixed)

### Sponsored Courses Development

- Backend Progress (Nikita O.)
	- Social sharing UI mostly complete
	- Backend abstraction in progress
	- Payments implementation released to prod successfully
	- Stripe API versions need major upgrade for crypto payments
	- Unrock integration ready for prod deployment
- Outstanding Decisions Needed
	- Rewards system: Going with codes (from provided list) per completion
		- Poly Market pushed call, questions ready
	- Twitter sharing: Link with preview (not direct image sharing)
	- Course overview video script needed
	- Cover image confirmation from design team
- Timeline Estimate
	- Development could meet mid-April deadline if decisions made quickly
	- Few days additional for final implementation
	- Testing time not included in estimate

### Technical Issues & Fixes

- WordPress Translation Problems (Michaela)
	- Memory issues with translation plugin
	- 75 task spike in ECS during same window as other issues
	- Moved WordPress cache to separate Redis database
	- Asynchronous requests failing silently
- Completed Work
	- Invalid URLs fix ready (Bad An)
	- FAQ section expansion fix in progress
	- Twitter preview card image fix (Maria)
	- iOS app banner implementation started
	- Google Analytics expansion for charts and election pages (Marina)
	- Crypto jobs fixes completed (Roma)

### Action Items

- Sean and team: Work on Twitter copy for course sharing
- Design team: Provide course overview video and cover image confirmation
- Brian: Document performance issues on Confluence
- Michaela/Brian: Investigate 2MB page size issue for Google compliance
- Roma: Complete AQI project AWS migration and effectiveness comparison

Chat with meeting transcript: https://notes.granola.ai/t/350784ce-db79-49f9-9cad-c63d7f87e611
