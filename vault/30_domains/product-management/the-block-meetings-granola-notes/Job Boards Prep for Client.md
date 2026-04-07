---
granola_id: 62406868-bbdb-4876-a8f2-b5e9a6e24f21
title: "Job Boards Prep for Client"
type: note
created: 2026-04-07T14:34:51.573Z
updated: 2026-04-07T14:53:55.653Z
attendees: 
  - akryvanosau@theblock.co
  - bmendoza@theblock.co
  - erupkus@theblock.co
  - npivcevic@theblock.co
  - rvishneuski@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Job Boards Prep for Client-transcript.md]]"
---
### Luxo Integration Overview

- Block Hunters client wants job board integration with Luxo ATS system
- Pioneer Jobs is competitor using this implementation model
- Luxo distributes job applications across multiple job boards
	- Centralizes applications from satellite job listing sites
	- Block Hunters posts once, automatically syncs to partner sites
- Contract with Block Hunters (BHB group), not directly with Luxo

### Technical Implementation Questions

- Application storage requirements unclear
	- Need to confirm if storing applications in own database is mandatory
	- Could be for observability/source tracking vs affiliate-style tracking
	- May be overkill if Luxo provides conversion analytics
- Two implementation approaches:
- Need sandbox environment and API documentation to test

### Data Mapping Challenges

- Company entity conflicts potential issue
	- Risk of duplicate companies in database (e.g., existing “Allium” vs new “Allium”)
	- May need separate company table for job listings vs existing CMS companies
- Job filtering and mapping requirements
	- Need sample job data to test position/location mapping
	- Multiple companies posting through single integration

### Frontend Changes Required

- Dual job listing types needed
	- Manual jobs (current external links)
	- Luxo-powered jobs (iframe application process)
- Apply button behavior differs between types
- Source labeling required for all applications

### Next Steps

- Get Luxo API access and documentation
- Obtain sandbox environment for testing
- Clarify application storage requirements with Block Hunters
- Review sample job data for mapping assessment
- Timeline: Initially estimated 1-2 weeks + QA, pending unknowns
- Note: QA handoff timing consideration (current QA resource transitioning)

Chat with meeting transcript: https://notes.granola.ai/t/53aebf01-1877-47af-8364-4cb2edfdb8da
