---
granola_id: ffd5e31c-7738-4d7a-96ae-fcb1aa366157
title: "Unified Daily Standup"
type: note
created: 2026-03-10T14:00:27.536Z
updated: 2026-03-10T19:48:24.659Z
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
---
### Team Updates & Progress

- Alex (Akryvanosau): Finalized banner for data charts, created dev box
	- Fixed desktop issue but broke dev box during restart
	- Caesar investigating the issue
	- Started Canvas marketing page for individuals
- Anna (Abenitez): Testing GA4 for newsletters, events working
	- Clarifying cookie expiration mechanics
	- Polymarket changes by Marlene/Brent look good, awaiting client review
	- Completed ads testing on price converter page and global search results
- Brian (Bmendoza): Working on llm.txt and linting for codebase cleanup
	- Removing notifications, cleaning up code with comments
	- Analytics improvements in progress
- Corey (Cpaz): Finished llm.txt (assigned to Brian)
	- Completed monthly report
	- Started monthly audit screening
	- Working on geo strategy

### Infrastructure & Technical Work

- Caesar (Cdaumur): Solving Launchpad dev box issues
	- Homepage working but research/funding/news sections failing
	- Investigating environment variables and closure blocking
	- Migrating GitHub Actions workflows to Airflow
	- AWS costs reduced from $22K to $15K despite adding new services
- Christophe (Cdaumur): Finished image tool, uploaded to core base test
	- Created dev box for Anna
	- Started updating homepage test
	- Discovered GitHub Copilot skills feature for recurring tasks
	- Switching from Cursor to GitHub Copilot

### Major Feature Releases

- Maria (Mhulis): ShareX functionality almost complete
	- Fixing dynamic image for candidate sharing
- Marina (Mlozuk): Polymarket improvements and election page development
	- Adding concerns/questions to tickets
	- Investigated homepage article click issues, found potential fix
- Nikita Gulis (Mhulis): Multi-course support post-release fixes
	- 3-4 fixes from original tickets, separate ones for wordings/redirects
	- Role-based logical adjustments completed
	- Payment setup work resumed after multi-course completion

### Campus Platform Issues

- Nikita O (Norobenko): Payment setup bug fixes ongoing
	- Manual database migration needed to avoid auto-migration
	- Certificate generation issues resolved with Caesar’s help
	- Queue problems on prod fixed
- Ramuald (Ramuald Vishneuski): Canvas box work continues
	- Certificate generation fixed on production
	- Some users missing certificates from earlier attempts
	- Need to decide: show best attempt vs last attempt for certificates

### SEO & Content Improvements

- Nicolas (Npivcevic): Translation work in progress
	- Fixed FAQ schema markup issue after NUX4 migration
	- No longer using WordPress for schema, built on frontend instead
	- Sentry error fixes ready for Mike’s review
	- Added IRA (Investment Retirement Account) to ratings platforms
	- Broken link notifier ready after addressing Anna’s feedback

### Major Accomplishments

- NUX4 Migration: Completed after months of work
	- Team-wide effort with no critical bugs in production
	- Significant achievement for entire development team
- Polymarket Integration: Successfully launched
	- Planned ahead during fall 2025 (September-October)
	- Delivered during election season timing vs typical trend-chasing
- Performance Metrics:
	- SEO traffic increasing steadily
	- Website performance improving
	- Error/warning numbers decreasing

### Action Items

- Sean: Finish campus user change tickets, post today
- Sean: Complete Zapier testing for ad ops project
- Caesar: Share company Copilot credentials with Christophe via Keeper
- Ramuald: Resolve certificate display logic (best vs last attempt)
- Team: Prepare for ad ops demo discussion with fake contract close testing

Chat with meeting transcript: https://notes.granola.ai/d/ffd5e31c-7738-4d7a-96ae-fcb1aa366157
