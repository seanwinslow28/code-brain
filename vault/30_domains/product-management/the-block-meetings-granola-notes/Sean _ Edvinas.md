---
granola_id: 677e8d9c-b579-4972-ad70-917d5f3e51e0
title: "Sean / Edvinas"
type: note
created: 2026-04-08T16:12:53.204Z
updated: 2026-04-08T16:56:48.425Z
attendees: 
  - erupkus@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Sean _ Edvinas-transcript.md]]"
domain: [product-management]
---
### AI ETF Analysis Tool Demo

- Demonstrated Claude-based ETF research skill for Morgan Stanley Bitcoin Trust (MSBT)
	- Tool pulls comprehensive ETF data from ticker input
	- Screenshot analysis when links blocked
	- Found ticker error in social media (MSBT vs correct MBST)
	- Successfully retrieved trading view data and basic info
- Updated skill with SEO optimization requirements
	- Added meta title and description length thresholds
	- Real-time skill modification and download capability
- API limitations identified
	- Track Insight data requires specific integration
	- Eaton Vance subsidiary pages difficult for AI to locate automatically
	- Solution: whitelist specific websites for priority checking

### Automation Workflow Planning

- Goal: Slack-initiated ETF processing pipeline
- WordPress integration available via Claude connector
	- Requires VPN access and authorization setup
	- Recommend limited permissions (ETF pages only)
	- Mike consultation needed for security review
- Jira integration demonstrated
	- Biweekly update automation using JQL queries
	- Ticket creation with epic linking
	- Read/write permissions configurable

### Next Steps

- Schedule Mike discussion on WordPress integration security
	- Tomorrow or next standup
	- Focus on limited ETF page access only
- Continue skill development during quieter periods
	- Prioritize ad ops automation scripts
	- Expand connector integrations as needed

Chat with meeting transcript: https://notes.granola.ai/t/0bf9049c-cd2f-4915-acba-c2609d3988b0
