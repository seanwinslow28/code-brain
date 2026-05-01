---
granola_id: 44484b57-60c8-4706-b86d-a38b12beb3b9
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup.
context: the-block
created: 2026-04-21
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

- Anna (Frontend)
	- Completed 404 URLs for speeches in Blockdown - ready for deploy
	- Plus/minus signs on pages ready
	- iOS banner apps ticket reassigned from Maria for GA4 events
		- Same consecutive event tracking issue as before
		- Added comment for tracking every event
		- iOS app not releasing this week - no urgency
	- Reviewing Nicola’s election hub fix for semi crypto
- Brian (Backend)
	- Multiple tickets ready for deploy after daily
	- Large numbers cut-off ticket finalized and ready for testing
	- AI generated metadata ticket 95% complete
		- One remaining issue being fixed
- Caesar (DevOps)
	- Box deployment migrated from Terraform Cloud to Atlantis
	- Converting all workspaces (Elasticsearch, Airflow, BigQuery, AWS)
	- Weekly 2-3 hours spent in Cloudflare blocking bots to reduce suspicious traffic
- Corey (Content)
	- Working on learn page content improvements
	- Adding Price page FAQs - planning to finish this week
	- Added comments for pro page design
	- Data pages meta titles in progress - finish by next week
	- Started ratings pages work
	- Planning competitor analysis by segments report
	- 258 meta titles completed manually out of ~1000 total
		- Need automation solution for remaining titles
- Kristoff (Development)
	- Merged timezone ticket and verified on Pro
	- Created dev box for asset building changes
	- Working on free star code cleanup

### Campus Platform Development

- Nikita/Ramo (absent - Belarus holiday)
	- Sponsored course pushed to dev box, testing started
	- Twitter limitations applied (account must be 1+ days old)
	- Current sign-in flow allows access regardless of existing account status
		- Creates account if none exists
		- Misleading copy needs adjustment
	- Upsell flow shows “course not available” message for 101/201 courses
	- Data processing consent and wallet address collection required for all users
	- Admin account needs replacement with individual accounts
	- Weekly sync calls planned to prevent issues falling through cracks

### Elections Hub Deployment

- Nicola
	- Fixed Stand with Crypto API issue
	- Added fallback layer for API failures
	- Local and dev box testing complete
	- Deployment instructions prepared
	- Targeting early next week launch pending promotional video completion
	- Need to select featured article for main page
	- Video section can be hidden until content available
	- Job boards two-step verification implemented
	- Sentry error reporting issues identified - seeking help

### iOS App Final Push

- Mike
	- Completing sponsor features for iOS app
	- Adding WordPress API endpoint
	- Final portal before going live

### Next Steps

- Sean: Send Claudine’s latest address collection design to Nikita
- Team: Volunteer for Sentry error reporting fix
- Corey/Sean: Implement automation for remaining 750+ meta titles
- Nicola: Coordinate with editorial team on video content
- Nikita: Set up individual campus accounts replacing shared admin access

Chat with meeting transcript: https://notes.granola.ai/t/9dee6c9d-5ed9-4d9c-9a64-b252195786fc
