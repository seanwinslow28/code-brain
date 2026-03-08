---
granola_id: 0456b9cc-e958-40d5-ba07-856a4ac64a12
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Campus team sync on sponsored courses - campus team sync.
context: the-block
created: 2026-03-03
source: granola-sync
attendees:
  - ddebreczeni@theblock.co
  - erupkus@theblock.co
  - mhulis@theblock.co
  - norobenko@theblock.co
  - cdaumur@theblock.co
---

# Sponsored Courses - Campus Team Sync

### The problem

- Need to align design, product and engineering teams on sponsored courses implementation for Campus platform
- Sponsored courses will be free to users, requiring effective upselling strategies to paid content
- Integration with Polymarket requires seamless authentication and reward distribution system
- Current system relies on entrance tests for course progression and certification, but sponsored courses won’t have entrance requirements

### Themes discussion

- Technical format considerations between Rise 360 and Storyline
	- Rise 360 creates responsive, single-page web experience but has poor voiceover support
	- Storyline produces slide-based format with better voiceover but isn’t responsive
	- Both export CMI5 and xAPI compatible with existing Campus infrastructure
- Authentication and user flow design
	- Users will authenticate through Twitter/X via theblock.co
	- Direct integration into My Campus Hub without intermediate course pages
	- Account creation through social login transitioning to regular theblock.co accounts
- Course structure and completion tracking
	- Sponsored courses will have 5 lessons/topics per course
	- No entrance tests required, adapting existing logic that depends on test completion
	- Certificate generation based on course completion rather than test submissions

### Specific ideas

- Dashboard integration approach
	- Add sponsored courses section at top of course catalog
	- Use existing pill/category system to distinguish sponsored content
	- Implement direct navigation from dashboard to course content, bypassing dedicated course pages
- Completion and reward system
	- Generate completion certificates based on finishing all lessons
	- Include final quiz with unlimited retries (no anti-cheat measures needed)
	- Promo code distribution system for Polymarket rewards
		- Option 1: Polymarket provides pre-generated codes
		- Option 2: Campus generates codes and shares with Polymarket
- Post-completion user journey
	- Congratulations page with certificate download
	- LinkedIn sharing functionality for certificates
	- Twitter sharing capabilities
	- CTA directing users to Polymarket with bonus credits
	- Upselling opportunities for paid Campus courses with potential discounts

### Future directions

- Research team coordination needed
	- Confirm final course structure and quiz requirements with research team
	- Get Polymarket sign-off on content by end of week
	- Clarify reward distribution mechanics and bonus amounts
- Design requirements for Claudine
	- Create updated dashboard mockups showing sponsored course placement
	- Design completion/success state pages outside of storyline flow
	- Include social sharing and upselling CTAs in completion flow
- Technical implementation priorities
	- Adapt course completion logic to work without entrance tests
	- Implement promo code generation and tracking system
	- Configure custom course categories in admin panel
	- Set up direct course launching from dashboard

Chat with meeting transcript: https://notes.granola.ai/t/53369a58-5eb6-43ca-a50d-e380704a6df7