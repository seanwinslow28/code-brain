---
granola_id: 3ba96835-6672-4125-bfb6-5c2cd0cd94b9
title: "Brand, Media, Design Weekly Sync"
type: note
created: 2026-04-08T20:01:33.628Z
updated: 2026-04-08T20:34:43.194Z
attendees: 
  - dquinton@theblock.co
  - ckuhn@theblock.co
  - melshahat@theblock.co
  - jcarusi@theblock.co
  - snotcutt@theblock.co
  - jleech@theblock.co
  - ksparks@theblock.co
  - cdaumur@theblock.co
  - jgragg@theblock.co
  - sho@theblock.co
  - erupkus@theblock.co
  - zwang@theblock.co
  - gjenkinson@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Brand, Media, Design Weekly Sync-transcript.md]]"
---
### Singular Live Broadcasting Software - Lower Thirds Development

- Sean spent hours testing lower third animations in Singular platform
	- Successfully created skewed entry effect matching Zwang’s design concept
	- Major limitation: entire container must be skewed at -45° angle to achieve effect
	- Cannot set custom starting points - animations always begin from composition edges
- Technical constraints discovered:
	- “Fade and translate” function only translates, doesn’t actually fade
	- No keyframe manipulation - only start/end animation points available
	- Custom easing curves appear unavailable despite interface suggestions
- Current prototype (L3 test) ready for Jordan to test in OBS integration
	- Composition size set to 600x200 for lower thirds specifically
	- Need to determine if custom compositions can live within larger broadcast layout
- Next steps require close collaboration 2x weekly between Sean, Jordan, and Zwang

### Election Coverage Video Production Status

- Confusion around video production ownership and current status
	- Ed wrote script, delivered to Jamie (currently out this week)
	- Kelvin mentioned filming completed last week but no one has seen output
	- Jordan confirms he hasn’t been involved in any video creation
- Video editing capabilities limited to Sean or Davis
	- Kelvin cannot edit video content
	- Jordan handles only live broadcast technical setup
- Promotional video intended as Kelvin hype-man style (similar to campus promo)
	- Should show quick product shots of election coverage UI
	- All designs already completed in Figma
- Launch timeline: Next week if video production resolved

### Process Improvements Needed

- Missing intake system for media requests causing projects to fall through cracks
- Current workflow relies on ad-hoc Slack requests vs structured ticketing
- Jordan’s JIRA integration on hold due to Gareth’s new show changing podcast structure
- Media board exists but election video not tracked there
- Meeting time moving to 11:30 AM ET Wednesdays for European team members

### Action Items

- Jordan: Test L3 composition in OBS/Studio environment tomorrow
- Ed: Post election coverage script in social media marketing Slack channel
- Sean: Knowledge transfer with Zwang and Jamie on Singular limitations early next week
- Team: Clarify election video production status and ownership via Slack

Chat with meeting transcript: https://notes.granola.ai/t/a0af2cf0-a6fd-4fdf-8a15-dfaaa0001606
