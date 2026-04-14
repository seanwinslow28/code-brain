---
granola_id: 58185dc4-3183-46dd-acbf-fc30292a8988
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Meeting about singular.live discussion/refinement.
context: the-block
created: 2026-04-08
source: granola-sync
attendees:
  - bmendoza@theblock.co
  - erupkus@theblock.co
  - npivcevic@theblock.co
  - jleech@theblock.co
  - jgragg@theblock.co
  - zwang@theblock.co
  - gjenkinson@theblock.co
  - dquinton@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Singular.live discussion_refinement-transcript.md]]"
---

### Project Overview & Status

- Singular.live discussion/refinement for new live show “Starting Block”
- Team alignment needed across design, engineering, and operations
- Launch timeline pushed to May (originally April)
	- Allows time to secure title sponsor
	- Better coordination with sponsorship deals

### Design & Animation Progress

- Josh spent 30 minutes in Singular composer exploring lower third animations
- Zwang created skewing animation effects for overlays
- Singular’s WYSIWYG more intuitive than straight HTML/CSS coding
- Next: Josh rebuilding lower third animation in Singular today
	- Will determine dynamic text update capabilities
	- Test workflow integration with Jordan’s live operations

### Data Integration Requirements

- Price ticker needs live data feeds
	- Current: Coin Gecko API (1-minute updates, API limits)
	- Preferred: LMAX API (every second updates, better for live ticker)
- Chart integration options explored:
	- Nicola to test if Singular supports embedded web views for chart interactivity
- WordPress backend for show content management
	- New post type for each show
	- Data nodes push to Singular composer
	- Guest names, headlines, images, charts selection

### Sponsorship Strategy & Revenue

- LMAX ticker sponsorship opportunity identified
	- Jeff confirmed 40% of LMAX traffic comes from The Block
	- Current homepage deal: $800k annually
	- Proposed ticker sponsorship: $100-200k for 6 months
	- Jeff reaching out to Gena next week
- Title sponsor model (3-month deals):
	- Naming rights: “Starting Block powered by [Sponsor]”
	- Permanent brand placement throughout show
	- Watermarked logos on all clip content
- Individual segment sponsorship potential:
- Estimated reach: 3-5k views per show, 100k monthly views minimum

### Technical Implementation Plan

- Three teams need coordination: design, engineering, operations
- Key technical questions to resolve:
	- Singular’s live data ingestion capabilities
	- Interactive chart rendering possibilities
	- Dynamic sponsor logo switching per segment
- WordPress integration for content management
- 20-minute pre-show setup target for Jordan

### Next Steps

- Josh: Complete lower third animation in Singular today, discuss workflow with Jordan this afternoon
- Nicola: Investigate Singular’s web view and live data capabilities
- Ed: Schedule weekly Wednesday meetings (Friday next week due to Paris Blockchain Week)
- Jeff: Send LMAX ticker sponsorship proposal to Gena
- Josh: Clean up mockup and send to Jeff for sponsor discussions
- Jordan/Gareth: Capture time-lapse footage in Paris for promotional materials
	- 5-minute busy intersection shoot
	- Gareth as steady presence amid fast-paced background motion

Chat with meeting transcript: https://notes.granola.ai/t/b5ed4aae-c9e9-4247-beeb-827bb839ccd8
