---
granola_id: 6ef614de-3fa4-4b12-9d80-bb2e1262f57b
title: "The Starting Block (New .co daily show) Data reqs"
type: note
created: 2026-03-27T14:03:08.389Z
updated: 2026-03-27T14:29:25.099Z
attendees: 
  - bmendoza@theblock.co
  - erupkus@theblock.co
  - mprice@theblock.co
  - npivcevic@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/The Starting Block (New .co daily show) Data reqs-transcript.md]]"
domain: [product-management]
---
### Data Requirements for Singular Integration

- Four main data types needed for live stream overlays:
- Current Singular subscription: Professional tier
	- 20,000 API calls monthly
	- 100MB data limit
	- Supports HTML/CSS compositions and WebSocket connections
- Price ticker implementation options:
	- WebSocket for real-time updates vs polling every few seconds
	- Use LMAX proxy API (500-700 bytes, highly optimized)
	- Concern: LMAX servers down daily 5-5 California time for maintenance
	- Rate calculation: 3,600 calls/hour for per-second updates

### WordPress-Based Content Management

- Dedicated episode pages in WordPress with ACF fields:
	- Article selection for headlines
	- Chart slug references for PNG generation
	- Guest information fields
	- Potential for additional content types (election data, etc.)
- Producer workflow:
	- Handpick stories from latest news
	- Select charts to display
	- Pre-populate guest details
	- Minimum one week advance notice for new content types
- Alternative considered: Google Sheets integration (rejected - sticking with WordPress)

### Next Steps

- Sean to communicate technical feasibility to media team
- Engineering team member to explore Singular platform capabilities
	- Shared credentials available for system testing
- Brian likely point person for WordPress development (pending CTO transition)
- Design team needs to finalize overlay specifications
- No immediate urgency - translations work takes priority
- Npivcevic traveling to Czech Republic next week

Chat with meeting transcript: https://notes.granola.ai/t/7499606a-b981-422f-942c-ee699d538957
