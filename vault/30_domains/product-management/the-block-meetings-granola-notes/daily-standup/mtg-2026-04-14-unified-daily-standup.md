---
granola_id: 781275ae-8e14-4d7a-9d1b-12de5b01b94e
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup.
context: the-block
created: 2026-04-14
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

### Team Updates & Progress

- Brian Mendoza: Finalized tickets, deployed category pages pagination fix
	- Set up dev box for sponsored courses
	- Completed 461A ticket: reduced from 6MB to 600KB chart data
	- Pages now load incrementally vs all at once
- Bodan: Fixed multiple tickets in review, awaiting dev box creation for testing
- Anna: Website health improving per Ahrefs audit
	- Working on learn page content improvements and metadata
	- Adding FAQ sections to price pages
	- Completed ~200/700 data pages meta titles/descriptions
- Kristoff: Time zone ticket ready for broad testing
	- Nearly solved charts failing when series JSON missing
	- Final state exam preparation needed in May/June
- Maria: Finished Edinburgh app banners (in review)
	- Updated homepage prices with token rank filtering for top tokens
	- Working on elections landing page fixes
- Marina: Finalized election patient work
	- Adding brand safe keywords with detailed testing commands for QA

### iOS App & Authentication

- iOS app deployed to production with unified auth backend
- Includes consent for privacy, terms of service, marketing
- Ready for App Store submission pending final verification
- No anticipated approval issues due to basic functionality

### Sponsored Courses Development

- Nikita & Alex: Frontend/backend integration mostly complete
- Twitter authentication integrated successfully
- Awaiting finalized course content from David due to tracking changes
	- Switched from Storyline to Rise, breaking lesson progress tracking
	- Found workaround solution, testing locally
- Deployed Stripe version to prod enabling crypto payments
- Mock data version ready for QA while awaiting LMS connection
- Outstanding questions:
	- Reward codes vs links from PolyMarket (no response yet)
	- Video overview still pending from media team
	- Twitter legal pages reference CryptoKey, need review

### Technical Infrastructure

- Roma: New payment flow released with crypto payments
	- Some non-critical issues remain, separate fix effort planned
	- Automation project in parallel development
- Michaela: Investigated Singular Live platform for Starting Block show
	- Mixed feelings on platform UX but functional once configured
	- Price ticker prototype working with Ed
- Luxo integration: API keys received from Block Hunters
	- Full admin access to their job posting data (concerning scope)
	- Straightforward implementation expected

### SEO & Content Performance

- Website health scores improving across audit tools
- Search traffic down 20-30% last month
	- Possible Google Core update impact
	- Market downturn correlation
	- This week showing rebound signs
- Translation project meeting with Alex Lavadov Thursday
	- Coindesk experience on partial translation SEO issues

### Team Changes & Organizational Updates

- Departures: Vention team (Roma, Alex, Maria, Marina, Vishnu) leaving this week
- New CEO: Steve Chung joining May 1st
- Third-party audit: Alex conducting organizational assessment
	- Anonymous feedback collection ongoing
	- Report will provide fresh perspective for new CEO
	- Addressing long-standing inefficiencies
- QA bottleneck: Anna will be sole QA after departures
	- Consider skipping QA for minor one-line changes
	- Direct communication for urgent fixes

### Action Items

- Sean: Hunt down PolyMarket for codes/links decision
- Sean: Review Twitter legal pages screenshots from Nikita
- Brian: Deploy mock data version and share PRs for reference
- Nikita: Finalize course import and test tracking solution
- Michaela: Review Google Sheets templates before Friday Singular Live meeting
- Team: Support Anna as sole QA, consider process adjustments for minor changes

Chat with meeting transcript: https://notes.granola.ai/t/b1896562-e4f5-428c-aea3-f6221a221034
