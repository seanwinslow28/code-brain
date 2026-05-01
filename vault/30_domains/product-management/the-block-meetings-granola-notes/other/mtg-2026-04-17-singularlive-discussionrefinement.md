---
granola_id: 7f82d8be-72f7-4cb9-a4cd-82be9f0a807f
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Meeting about singular.live discussion/refinement.
context: the-block
created: 2026-04-17
source: granola-sync
attendees:
  - dquinton@theblock.co
  - gjenkinson@theblock.co
  - bmendoza@theblock.co
  - erupkus@theblock.co
  - npivcevic@theblock.co
  - jleech@theblock.co
  - jgragg@theblock.co
  - zwang@theblock.co
  - jcarusi@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Singular.live discussion_refinement-transcript.md]]"
---

### Singular.live Control App Demo

- Sean demonstrated complete control interface for live broadcast
	- Created playlists for intro, Block briefing, market pulse, hot seat, Block original segments
	- Logic layers automatically switch between elements (same color = mutually exclusive)
	- Lower thirds, headlines, price ticker all controllable via interface
- 25+ hours invested learning software architecture
	- Composition environment for asset creation
	- Control app for live broadcast management
	- Requires refresh when updating compositions

### Price Ticker Implementation

- Two approaches under consideration:
- Decision: Explore native implementation first, fallback to HTML if needed
- Top 5-10 tokens by market cap (excluding stablecoins)

### Dynamic Content Management

- Guest information system established:
	- Control nodes for guest name, title, company
	- Manual updates before each show
	- Multiple guest profiles can be pre-prepared
- Article integration working:
	- Title, author, image fields
	- Copy/paste from website feed
	- Instant updates to broadcast overlay
- Interactive charts functional:
	- TradingView-style charts with live interaction
	- Jordan must interact via OBS during broadcast
	- Pre-show coordination needed for chart discussions

### Production Workflow

- Jordan requires dual monitor setup:
	- OBS on primary screen
	- Singular control app on secondary
- Pre-show preparation process:
- Daily 10-15 minute sync call recommended between Gareth and Jordan

### Next Steps

- Sean & Nicola: Implement native ticker with live data feed
- Sean: Add remaining design elements (segment titles, sponsor logos)
- Gareth: Discuss sponsorship requirements with Jeff for ticker integration
- Josh, Jamie, Davis, Jordan: Marketing plan meeting early next week
- Team: Soft launch target May 4th, 2026
- All: Weekly Wednesday refinement meetings continue

Chat with meeting transcript: https://notes.granola.ai/t/8378f151-a63f-4cf4-b0a9-2e619044867a
