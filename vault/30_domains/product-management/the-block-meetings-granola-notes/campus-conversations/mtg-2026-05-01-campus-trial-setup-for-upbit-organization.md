---
granola_id: 91e3b879-ee8d-471c-aea3-0e7de2138eb0
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Campus team sync on campus trial setup for upbit organization.
context: the-block
created: 2026-05-01
source: granola-sync
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Campus trial setup for Upbit organization-transcript.md]]"
---

### Campus Platform Setup Process

- Setting up trial access for potential client (Sean from Upbit exchange)
	- Two options: demo with dummy data vs. trial with real content access
	- Need to clarify with Jeff what type of access client wants
- Current process requires creating organization + subscription to trigger welcome emails
	- Individual org setup doesn’t send proper welcome emails
	- Self-service success email only triggers after Stripe checkout completion

### Technical Implementation Issues

- User deletion requires removing both user record AND identity record
	- Deleting just user record leaves email constraints in database
	- Identity deletion necessary to fully remove email from system
- Welcome email logic only works for individual self-service accounts
	- Organizational accounts don’t trigger same welcome flow
	- Need custom welcome email command for org-based trials

### Client Background

- Upbit exchange showing strong interest in Campus platform
- Jeff currently in Miami/Vegas communicating with client
- Client wants upskilling solution for their organization
- Need official-looking onboarding experience

### Subscription Configuration

- Mark paid out of band prevents trial period setup
- Better to set expiration date, let trial expire, then request payment
- Demo organizations can be upgraded to real accounts later

### Next Steps

- Mike to create welcome email command within 10 minutes
	- Will include delete function for iOS testing
	- Button-click solution for sending welcome emails
- Await Jeff’s clarification on demo vs. trial preference
- Test welcome email process with fake organization first

Chat with meeting transcript: https://notes.granola.ai/t/54278204-8650-401f-a344-8d75d4e0450e
