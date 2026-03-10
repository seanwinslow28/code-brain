---
granola_id: 2b489ca7-d894-40a0-9026-d0642c215fbc
title: "Unified Daily Standup"
type: note
created: 2026-03-05T12:59:01.779Z
updated: 2026-03-05T15:36:55.911Z
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

Claudine asked to have the 3 cards she posted in prod:

[https://theblockcrypto.atlassian.net/browse/PRO-4064?focusedCommentId=70338](https://theblockcrypto.atlassian.net/browse/PRO-4064?focusedCommentId=70338)

Work on the implementation ticket based on Claudine's reference. 

Koray not attending. Here are his updates:

I am working on my monthly reporting

Llm.txt project

Learn metadata updates

Sean Winslow  [3:57 PM]

What have you done in the past when it comes to people emailing about Campus bugs? Just writing a ticket and assigning to Ramuald or screenshotting/tossing it into the campus channel?

Matt Vitebsky  [4:02 PM]

try to resolve first - ie if they just need credits or something fix in the backend. Otherwise create a ticket and drop in the engineering qa chan

Sean Winslow  [4:05 PM]

I don't think I have access to Campus' backend. Unless it's all set up on WP?

## Enhanced Notes

### Development Progress & Bug Fixes

- Alex: Finalized data chart banner, working on Salesforce migration tool (dot pro to dot core)
	- Migration tool step form ready today/tomorrow
- Anna: Completed price migration checks, pretty market breaches working
	- Regression testing on sticky footer complete - ready for release
	- Continuing with GA4 newsletters and GAM key values tickets
- Bvadim: Fixed duplicate user terms issue blocking migration process
	- Found 16 users with duplicated terms (including Ramuald Vishneuski)
	- Created script to identify and fix invalid URLs
	- Solution addresses both duplicate terms and URL issues
- Brian: Debugging prices migration, updated with Anna’s comments
	- Planning analytics work with Ed and notification deployment
- Cesar: Completed UX pull request changes, testing in progress
	- Checking Salesforce domain for new compliance requirements
	- Migrating workflows from abstraction repo to Airflow (hitting monthly execution limits)
- Christophe: Finalizing Brooklyn tickets with Anna
	- Removing images from codebase, moving to WordPress S3 library
	- Next: main page article refreshing
- Marina: Working on polymarket election page integration
	- Sticky footer ready for release (approved by Sean)
	- Maintaining design consistency across polymarket widgets
- Nikita: Resurrected payment support changes rolled back in previous release
	- Working on checkout page for new payment flow
- Akira: Payment setup revival, syncing with Roma on dev box queue issues
	- Assisting with release preparation
- Nikola: Finished menu translations and front-end loading
	- Pausing translations to address notification ticket comments
	- Investigating WordPress Sentry issues flagged by Mike
- Ramuald: Preparing campus release with multiple fixes
	- Planning deployment today or tomorrow morning
- Maria: Updating election page report cards per Serena’s design changes
	- Continuing Twitter social sharing functionality

### Analytics & Content Issues

- Ed identified sponsored learn article display problems
	- Articles missing sponsored pills despite correct category tagging
	- Revenue team questioning Parsley vs GA4 page view discrepancies (216 vs 164)
	- Chart embedding creating double page view counting bug
	- Assigned tickets to investigate chart performance metrics
- Claudine requested 3 cards for production deployment
	- Reference: https://theblockcrypto.atlassian.net/browse/PRO-4064?focusedCommentId=70338
	- Team to work on implementation ticket based on her specifications

### Campus Support Transition

- Sean taking over campus Salesforce support from Matt
	- User Andre reporting credit issues (claims 11 credits reduced to 0)
	- Ramuald found user actually had 4 credits, system showing correct amount
	- Someone issued additional credits yesterday at 6PM server time
- Campus backend access setup
	- Brian providing CLMS login credentials to Sean
	- Ramuald to demonstrate user management and credit allocation
	- Recommendation: use incognito mode to avoid login conflicts
	- Test environment access to be provided for safe experimentation

Chat with meeting transcript: https://notes.granola.ai/t/299db135-80c0-475c-862a-9971baabc215
