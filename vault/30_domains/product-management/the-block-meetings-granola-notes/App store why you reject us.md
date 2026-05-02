---
granola_id: 2c98c9af-ee2a-4f89-8a35-bf49e791116c
title: "App store why you reject us"
type: note
created: 2026-04-30T15:29:15.667Z
updated: 2026-04-30T17:34:31.823Z
attendees: 
  - mvitebsky@theblock.co
  - erupkus@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/App store why you reject us-transcript.md]]"
---
### App Store Rejection Issues

- Apple rejected app submission with 4 main issues requiring fixes:
	- Support URL is dead link - needs actual contact webpage
	- Tracking permission popup only shows on second session - Apple requires first session
	- Background music permission unclear - need testing instructions for reviewers
	- Missing account deletion functionality for authenticated users
- Additional questions from Apple about paid features/subscriptions
	- All answered “no” - not offering any paid content currently

### Technical Fixes in Progress

- Tracking permission popup
	- Currently triggers on second session via rate limiting workaround
	- Modified to trigger on first session after onboarding completion
	- Successfully tested on simulator - system prompt now appears correctly
- Account deletion feature
	- Requires backend integration with Mike’s help
	- Privy offers delete function through API
	- Two implementation options identified, awaiting Mike’s decision
- Contact page creation needed for support URL

### Development Workflow Discussion

- GitHub branch management concerns
	- 24 branches exist in repo - mostly deprecated
	- Main branch is current, coordination needed between Ed, Sean, and Mike
	- Need proper Git practices training from Mike
- Security considerations
	- Secrets file properly in .gitignore
	- Local development vs GitHub push protocols
	- Version bumping and testing procedures established

### Next Steps

- Ed: Wait for Mike’s response on account deletion implementation approach
- Ed: Create contact page once deletion feature resolved
- Ed: Schedule GitHub best practices session with Mike
- Team: Submit new build to Apple with fixes and testing instructions
- Team: Reply to Apple review with feature explanations and Q&A responses

Chat with meeting transcript: https://notes.granola.ai/t/b1ed77ef-d332-4824-9967-87ed6e11f494
