---
granola_id: 2bc57671-1c65-4a3c-8dd6-68a7d5b66cd8
title: "Project CTO Design Check-ins"
type: note
created: 2026-04-20T14:01:23.550Z
updated: 2026-04-20T15:01:27.813Z
attendees: 
  - mvitebsky@theblock.co
  - erupkus@theblock.co
  - cdaumur@theblock.co
  - jgragg@theblock.co
  - sho@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Project CTO Design Check-ins-transcript.md]]"
---
### Homepage Redesign Progress Review

- Serena presented extensive desktop and mobile iterations
	- Multiple hero section variations with news prioritization
	- Modular approach allowing flexible content placement
	- Strong revenue integration: 4+ ad modules (OKX, sponsored posts, press releases, Pro unlock)
- Claudine’s work halted due to campus obligations, out today
	- More abbreviated content sampling approach
	- Stylistic concerns: rounded corners feel “AI-generated”
	- Modular newsletter signup with different types

### Navigation and Content Strategy Decisions

- Jump navigation concerns
	- Competes with primary nav (News/Data/Research/Prices duplicated)
	- Solution: rename sections (e.g., “Today’s Markets” vs “Prices”)
	- Alternative: eliminate jump nav, bring abbreviated sections above fold
- Latest vs Trending toggle discussion
	- Potential content overlap issues
	- Proposed logic to prevent duplicates between sections
	- “Most Read Today” numbering system preferred over repeated labels
- Content hierarchy priorities

### Technical Implementation Considerations

- Chart library replacement needed
	- Current HighCharts framework 5-6 years old, needs updating
	- Matt successfully used native Swift charts in app
	- Exploring ShadCN library for Block-style charts
- YouTube embed strategy
	- Autoplay may hurt YouTube algorithm/view counts
	- Need research on best practices for embedded players
- Responsive design approach
	- Expand to 4 columns on wider screens (1800px+)
	- Contract to preserve hero + ad on smaller screens (1024px)

### Design Philosophy and User Testing

- “Apple Store vs Walmart” approach
	- Coindesk feels cluttered like Walmart
	- Aim for intentional spacing around content like Apple Store
	- Balance premium feel with news organization content volume
- User testing priorities
	- A/B test component positioning (sponsored vs most read)
	- Test hero module click-through rates (wide vs narrow stories)
	- Jump nav usage patterns need validation
- Reference sites for inspiration
	- Wealthsimple Magazine for modern, airy design
	- 3D scroll effects and parallax implementation

### Next Steps

- Serena: Create version with abbreviated sections above fold
	- Eliminate jump nav requirement
	- Integrate latest/trending toggle
	- Develop condensed market/research modules
- Josh: Explore chart library alternatives, investigate data feed access
- Team: Continue visual research on competitor news sites
- Matt: Dedicate focused time to design exploration this week

Chat with meeting transcript: https://notes.granola.ai/t/010b0e3a-182d-4a8b-9442-862b9f3e46b2
