---
granola_id: 192dc0b1-aa01-4607-a354-2672822201d9
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: "1:1 with Ed covering ios training deus."
context: the-block
created: 2026-04-29
source: granola-sync
attendees:
  - mvitebsky@theblock.co
  - erupkus@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/iOS training deus-transcript.md]]"
---

### iOS App Development Setup

- Ed successfully set up Xcode development environment
	- Downloaded iOS 17 simulator (8GB)
	- Configured Apple developer account authentication
	- Resolved initial build failures with secrets file
- First successful app build and simulator testing
	- App launched on iPhone 17 simulator
	- Tested dark/light mode toggle
	- Confirmed search functionality works across news/token/data APIs
- Development workflow established
	- Clean build: Command+Shift+K
	- Archive for App Store: Product → Archive
	- Simulator controls: rotate, restart, app switcher

### App Store Submission Process

- Removed iPad support to resolve submission blocker
	- Updated code via Claude to remove iPad dependencies
	- Build number updated to 2.3.22
- Successfully submitted app for Apple review
	- Expected review time: 72+ hours for full App Store release
	- 48 hours for TestFlight external testing
	- Manual release selected for first version
- App Store Connect configuration completed
	- Promotional text and description added
	- Keywords configured
	- No sign-up required setting confirmed

### TestFlight Testing Setup

- Internal vs external testing structure explained
	- Internal: Invite-only, immediate access after upload
	- External: Link-based (100 user limit), requires Apple review
- Current internal testers: Sean, Matthew, Edvinas
- External testing link ready for broader company rollout
- Ed needs iPhone for proper testing
	- Push notifications can’t be tested on simulator
	- Larry approval needed for $600 device purchase

### Technical Infrastructure

- Authentication via Privy
	- Both Sean and Ed added as admins
	- Currently on dev plan (500 user limit)
	- Need to upgrade to production plan before launch
- Analytics and monitoring
	- GA tracking configured for iOS property
	- Mike manages push notification data
- Search functionality
	- Queries multiple APIs simultaneously (news, token, CoinGecko, data)
	- Cost concerns only at 50k+ users
	- Caching strategy available if needed

### Next Steps

- Sean: Retry Apple ID setup daily until successful
- Ed: Test app on wife’s iPhone until company device approved
- Team: Create step-by-step documentation from meeting recordings
- Revenue team: Secure sponsor for launch (logo upload to WordPress)
- Mike: Push marketing page live when sponsor confirmed
- Privy: Upgrade to production plan before launch

Chat with meeting transcript: https://notes.granola.ai/t/eab63992-1d1c-4c26-aa09-67dcb7d38df2
