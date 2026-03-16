---
granola_id: 1872b406-750f-458b-a11b-f4e835e8486e
title: "Ramuald - Campus Bug Fix"
type: note
created: 2026-03-16T16:35:03.028Z
updated: 2026-03-16T16:39:39.191Z
attendees: []
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Ramuald - Campus Bug Fix-transcript.md]]"
---
### Campus Bug Issue

- Bug appears when users added through CMS vs. regular UI flow
	- Sean created account through different mechanism (UI)
	- Bug only surfaces with CMS-added users
	- Backend logic differences between the two flows

### Current Access Setup

- Theblock team has enterprise account access
- Sean accessed campus through usual flow, bypassing CMS
	- This is why bug wasn’t visible initially
- Bug stems from 2.0.1 release (Winslow’s Cross)

### Proposed Solutions

- Add admin to organization in CMS
	- Admin won’t see test and course content
- Add Matt as admin, others as students
	- Students won’t see each other
	- Can view organization average scores only
- Alternative: Fix current individual CMS implementation

### Next Steps

- Ramuald to test one approach and report back in 10 minutes
- Potential release today if fix works
- May need Nikita’s involvement for workarounds

Chat with meeting transcript: https://notes.granola.ai/t/78001d17-a966-4284-9fb7-3d70f07afff9
