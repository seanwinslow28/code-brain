---
granola_id: fc99f844-7059-4b04-a723-b7e0ff3749a1
title: "Unified Daily Standup"
type: note
created: 2026-03-31T14:00:33.606Z
updated: 2026-03-31T18:33:21.098Z
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
domain: [product-management]
---
### Team Updates & Progress

- Alex: Fixed jobs bugs but found more issues than resolved
	- Taking pull requests from Maria
	- Backend ready for sponsored courses (higher priority than jobs)
- Anna: Finished advertiser fix testing, ready for deployment
	- Starting reports card work today
- Bvadimovich: Profile image inconsistency fix deploying after meeting
	- TF pages misconfigured links approved by Brian, creating dev box
	- RCP images ready for testing
	- Working on indices growth/decrease design changes
- Brian: Deployed analytics, LMS text, newsletter fixes yesterday
	- Working on pre-bid issues and cookie consent bug
	- Happy belated birthday - celebrated Monday night at bar

### Infrastructure & Security

- Caesar: Completed security policy review with team
	- Terraform Cloud billing starts tomorrow - removing unused workspaces
	- Tracking resources to reduce invoice costs
- Cpaz: Working on geo tickets, approved Christoph’s LMS text file
	- Conducting Ahrefs reaudit to verify fixes from last week

### Development & Features

- Christoph: Finished edge script, waiting for deployment when colleague returns
	- Starting LMS text work for SEO/AI optimization
	- Improving ChatGPT findability
- Maria: Fixed reports and post cart pages per Ed’s requests
	- Adding new elections widget to homepage
- Marina: Finalized Polymarket and elections page integration
	- Working on article recirculation block adjustments
	- Needs new task assignment after completion

### Payment & Authentication Systems

- Mike: iOS auth integration nearly complete for The Block
	- Notifications API tweaks for preference saving
	- Campus LMS preference integration
	- Coordinating tax release with Vicki
	- Payment flow prerequisites with Nikita
	- Simon AI updates for MCP and 880 integration
- Nikita Ghoulis: Payment setup shipped to Ramuald for testing
	- Twitter authentication backend ready for Alex’s frontend work
	- Design consolidation needed for sponsored courses
		- Multiple implementation approaches causing confusion
		- UI design appears unfinished with conflicting directions
		- Need final consolidated version ASAP
- Nikita: Payment integration deployed to dev box for testing
	- Tax integration ready for production deployment
	- Sponsored courses authentication, wallet saving, profile updates complete
	- Verification email enforcement questions:
		- Mandatory for new users regardless of Twitter/email signup
		- Optional vs required scenarios need clarification
	- Polymarket code generation clarified: They provide codes/URLs, not generated internally

### Testing & Quality Assurance

- Ramuald: Crypto jobs nearly finished with remaining frontend/backend bugs
	- Nikola handling backend fixes next week
	- Starting payment flow testing
- Ed: Investigating Brave browser data pages error reported by Christoph
	- Conducting pro product interviews and salvage assessment
	- Preparing documentation for new CEO arrival (1 month)

### Action Items

- Sean: Finalize sponsored courses designs with Claudine today
- Sean: Send updated payment flow warning copy to Nikita
- Sean: Complete Zapier integration this week
- Mike: Send API key to Sean for integration testing
- Team: Check machines for axios security vulnerability (details in dev channel)

Chat with meeting transcript: https://notes.granola.ai/t/92816da9-e3d5-451a-bd4c-02c8ec47e515
