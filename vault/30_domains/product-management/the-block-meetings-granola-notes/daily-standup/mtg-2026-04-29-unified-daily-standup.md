---
granola_id: 3ddc48dd-600b-49d7-90a9-c9ba6b7a4e3b
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup.
context: the-block
created: 2026-04-29
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
  - kbaspinar@theblock.co
  - bvadimovich@theblock.co
  - ysmagulov@theblock.co
  - sho@theblock.co
  - koliva@theblock.co
  - ramuald.vishneuski@ventionteams.com
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Unified Daily Standup-transcript.md]]"
---

### Search Infrastructure Issues

- ACS (Amazon Cloud Search) has 10,000 result/1,000 page limit affecting all collections except “Latest crypto news”
	- New articles appear in search, very old articles don’t show up
	- Categories pages fixes inadvertently affected search functionality
- Current workaround: Hide broken pages rather than show non-functional pagination
- Long-term solution needed: Replace deprecated ACS with Elasticsearch
	- ACS closed to new users, Amazon pushing migration to Elasticsearch
	- Investigation required on Elasticsearch capabilities vs current system

### Development Updates

- Anna: Fixed databug in production (menu overlap issue), continuing wallet connection work and sponsored course
- Bovadam: Completed Maria sticks for token list, fixed podcast UI issues, AI metadata ticket ready for testing
	- GitHub build jobs failing consistently despite multiple reruns
- Brian: Rebuilding election hub after stack setup, deploying updates for Friday deadline
- Cesar: Migrating 20-30 Terraform workspaces in BigQuery/GCP, writing BI streams
	- Long-running task but capacity for small urgent items

### Team Transitions

- Kristoff: Deployed overlay ticket, taking rest of week off for final exams
	- Will join CEO call next week before departure
- Nikita & Akita: Collaborating on campus bugs from Ramo’s findings
	- Fixed several issues, working through remaining items systematically
	- Emergence deployment failed due to Bizzabo integration issues (conference provider from 2024)

### Authentication & Infrastructure Work

- Nikita: Working on crypto key user authentication adjustments
	- Goal: Allow normal sign-in without data complications
	- Expected completion today, moving to testing phase
- Michaela: Struggling with dev box job issues, Caesar providing assistance
	- Fixed “Next page” display for 15 rows (acknowledged as suboptimal UI)
	- Four new tickers pending coordination for implementation

### Newsletter & Email Issues

- Mike received three welcome emails simultaneously at night
	- Unrelated to current newsletter development work
	- Investigating SendGrid/Launchpad API trigger cause
- Unsubscribe process problematic: Users must unsubscribe from each newsletter individually
	- Different sub-accounts prevent unified unsubscribe interface
	- Reputation scores: Block news 99%, data insights 96%
	- Planning cleanup to reduce bounces and improve scores

Chat with meeting transcript: https://notes.granola.ai/t/044fc0c7-00d9-4e02-8e59-a713265a7eb2
