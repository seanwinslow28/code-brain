---
granola_id: 9c0e7aa4-40ad-45aa-a548-c5a0c2068e20
title: "Unified Daily Standup"
type: note
created: 2026-04-09T13:59:24.160Z
updated: 2026-04-09T14:36:47.403Z
attendees: 
  - bmendoza@theblock.co
  - mprice@theblock.co
  - npivcevic@theblock.co
  - mvitebsky@theblock.co
  - erupkus@theblock.co
  - mhulis@theblock.co
  - cdaumur@theblock.co
  - vention-team
  - cpaz@theblock.co
  - abenitez@theblock.co
  - norobenko@theblock.co
  - mzhynko@theblock.co
  - mlozuk@theblock.co
  - kbaspinar@theblock.co
  - bvadimovich@theblock.co
  - ysmagulov@theblock.co
  - akryvanosau@theblock.co
  - sho@theblock.co
  - koliva@theblock.co
  - ramuald.vishneuski@ventionteams.com
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Unified Daily Standup-transcript.md]]"
domain: [product-management]
---
### Team Updates & Progress

- Alex (Akryvanosau)
	- Prebit ticket deployed to testing, missing component caused rollback
	- Twitter notification main functionality complete, refactoring remaining
	- Profile update pages: removing “go back” button due to complex navigation logic
		- Forces users through required verification steps (email, data consent, name fields)
		- Logout button sufficient for navigation
	- Certification flow call scheduled for tomorrow
- Ana (out/traveling)
	- Tickets 4634 and 3277 ready for deployment, teams notified
	- Comments added to report cards and election hubs landing page
- Bodan (Bvadimovich)
	- Bug fixes: misconfigured destinations awaiting deploy
	- Large number display issue on converter pages resolved
	- Terms of service effective dates ticket received design feedback
	- Regional data loading issue discovered
		- Converter page cryptocurrency/fiat selection missing for non-US users
		- Works with US VPN, fails without VPN (Croatia tested)
		- Potentially affects other site areas
- Brian (Mendoza)
	- Google bot optimization for data dashboard nearing completion
	- Identified SSR performance issue: loading all chart data upfront in large JSON files
	- Treasury analysis completed
- Caesar (Cpaz)
	- Infrastructure migration progress: Atlantis nearly functional
	- AWS permissions fixes needed for testing
	- Terraform execution improvements planned to reduce box count by 50%

### Development & Content Work

- Koliva
	- Google Core Update impact analysis ongoing
	- Evergreen pages stable, news articles showing decrease
		- May correlate with reduced market interest due to global events (Iran focus)
	- Full assessment expected in 7-10 days
- Kristoff (Kbaspinar)
	- Charts task progress, may need Nicola sync tomorrow
	- Academic commitment: final state exams second week of June
		- Reduced availability in May for exam preparation
		- Will maintain meeting attendance but limited work capacity
- Maria (Mhulis)
	- Election pages fixes completed
	- iOS banners implementation across site
	- Newsletter popup replacement for daily newsletters modal
- Mlozuk
	- Election market targeting fixes finalized
	- Ad targeting for safety keywords in progress
- Mike (Price)
	- iOS app updates: terms of service, privacy flags, marketing flags
	- User creation process overhaul required
	- Selectable sponsor field for WordPress integration
		- Initial WordPress implementation, potential GAM migration later

### Authentication & Course Integration

- Nikita (Npivcevic)
	- Backend/frontend integration started for sponsor courses
	- Authentication and success flow coordination with Alex
	- Twitter authentication verification scheduled for tomorrow
	- Profile back button removal confirmed
- Norobenko
	- Sponsor course integration work with Nikita
	- Authentication side adjustments for Alex
	- David’s course example received, spreadsheet import process pending
- Nicola (Koliva)
	- Singular Live investigation for new Block show
	- Platform usability challenges: confusing interface, poor documentation
	- Dynamic content setup still problematic
	- Troubleshooting session with Sean planned
- Ramuald (Vishneuski)
	- Payment flow and AQA project continuation
	- Campus bugs identified and being addressed

### Post-Meeting Discussion: WordPress Automation

- Claude MCP WordPress integration proposal
	- Goal: automate ETF page creation and updates
	- Security concerns raised by Mike
	- Alternative approaches discussed:
	- Decision: test browser automation first, evaluate MCP if needed

Chat with meeting transcript: https://notes.granola.ai/t/0b396aa8-1bf2-41d3-b20c-8d7eb95581e5
