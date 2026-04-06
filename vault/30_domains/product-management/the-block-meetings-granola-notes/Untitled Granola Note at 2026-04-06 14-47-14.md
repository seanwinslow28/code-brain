---
granola_id: a38ce3a4-41e0-4fce-a751-f5169f687033
title: "Untitled Granola Note at 2026-04-06 14-47-14"
type: note
created: 2026-04-06T18:47:14.287Z
updated: 2026-04-06T19:19:15.432Z
attendees: []
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Untitled Granola Note at 2026-04-06 14-47-14-transcript.md]]"
---
### GA4 Funnel Investigation — Core Problem

- Funnel steps (session start → page view not on homepage) returning no results
- Root cause: The Block uses virtual page views (SPA architecture), not standard GA4 page view events
	- Standard page_view event exists in GA4 but may reflect only initial load or hard refreshes
	- virtual_page_view fires on in-app navigation via GTM data layer — this is what tracks article clicks
	- virtual_page_view not currently selectable as an option in the GA4 funnel UI

### What Was Confirmed

- Session IDs are sticky across navigation (homepage → article → article = same session ID)
	- Session ID does change when tab is left and returned to — likely time/focus-based, not per-navigation
- Page views and session IDs are being captured correctly in the network tab
- GTM data layer fires: GTM history change, lmax impression, virtual_page_view on article click
- GA4 funnel likely not broken — data exists, but the wrong event type is being queried
- page_location parameter works in standard event queries (session starts with exact match .co returns data)
- Funnel goal: understand homepage user journeys — which content buckets (news, prices, etc.) users navigate to after landing

### Next Steps

- Brian
	- Explore wiring up virtual_page_view in GA4 so it appears as a selectable funnel option (not retroactive)
	- Investigate funnel filter settings — possible include/exclude domain logic may need to be reversed
- Sean
	- Continue experimenting with GA4 funnel configuration
	- Try page_location parameter in funnel step 2 as an alternative to page_view event
	- Consider whether Looker dashboard already has this data in a more usable form

Chat with meeting transcript: https://notes.granola.ai/t/ba8a6eb7-590e-475b-80bd-922043ef3ef9
