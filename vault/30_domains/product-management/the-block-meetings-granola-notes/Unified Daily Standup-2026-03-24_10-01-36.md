---
granola_id: 2634f150-aa2b-4a5f-b38a-ef3f6dce7dda
title: "Unified Daily Standup"
type: note
created: 2026-03-24T14:01:36.563Z
updated: 2026-03-24T14:24:29.724Z
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

- Alex (Akryvanosau): Xantrification for sponsored courses
	- Switched to jobs feature after Rama’s testing feedback
	- Deployed data chart banner ticket
	- Left comments for Sean and Ed to review
- Anna (Abenitez): Charts and SEO work
	- Completed testing charts functionality on articles
	- Finishing SEO optimization ticket
	- Continuing newsletter updates from Brian’s work
	- Working on election pub stickers
- Bodhan (Bvadimovich): Data charts and image fixes
	- Embedded data charts ready for deploy (post-meeting)
	- Fixed RTTP incorrect images issue
	- Identified multiple website locations with same problem
	- Working on corrupted “see all data” buttons on ETF pages

### Infrastructure and Backend Tasks

- Caesar (Cpaz): Migration project ongoing
	- Migrating executions from abstraction to Airflow
	- Completed 5-10 pipelines migration
	- Reduced execution time by 4,000-5,000 minutes in T hub
	- Need to install new libraries for remaining tasks
- Corey: Price page FAQs and geo improvements
	- Working on Price page FAQs
	- Geo task for package selling
	- Geo improvements for campus and pro per Matt’s request
- Kristoff: Link removal and timezone issue
	- Deployed link removal feature
	- ETF build ticket already implemented
	- Timezone inconsistency on .pro site
		- Can’t run locally, needs dev box testing
		- Requires DLCMS setup with proper environment variables
		- Decision: Test directly in production for simple one-line fix

### Product Development

- Maria (Mzhynko): Report cards implementation
	- New assignment for report cards page
	- Filtering and search functionality in progress
	- Everything else completed except filters
- Mike (Michael Price): iOS and admin panels
	- Campus iOS offer deployment after Matt’s QA polish
	- Pro API admin panel for usage statistics
	- Simon AI admin panel for usage tracking
- Nikita Ghulis: Authentication and payments
	- Finished AI implementation of Twitter auth for sponsored courses
	- Forwarding to Nikita O for minor adjustments (caching and structure issues)
	- Working on UI portion of sponsored courses
- Nikita O: Payment system completion
	- Finishing 100% promo codes handling
	- Moving to testing phase after completion
	- Ready to proceed with sponsored courses

### Content and Localization

- Nikita (Npivcevic): Market data updates
	- Received exports from David, pushed to production
	- Updated Ethereum market structure yesterday
	- Awaiting additional exports from David
- Michael A: Translation work
	- Minor adjustments remaining before dev box deployment
	- Homepage and article page ready for review
- Rama: Jobs feature and automation
	- Working with Alexander on crypto jobs completion
	- Ready to publish active jobs (1-2 days to completion)
	- Campus work: multi-courses nearly done, minor bugs remaining
	- Automation project: Moving test execution from GitHub Actions to Amazon services

### Action Items and Cleanup Initiative

- Link Cleanup Strategy (Kristoff, Rama, Corey to discuss post-meeting):
	- 6,000 broken URLs identified from Ahrefs
	- Proposed: Clean 100 URLs daily over 2 months
	- Group similar link types for efficient processing
	- Create ticket for systematic approach
	- Add article author attribution to error tracking
- Sean’s Updates:
	- Working with media team on upcoming live stream (1-2 weeks)
	- Finishing Zapier integration
	- Preparing roadmap presentation materials
	- Personal: Relocated to Boston

Chat with meeting transcript: https://notes.granola.ai/t/a0a99f57-8801-4654-8b12-8a5735053a15
