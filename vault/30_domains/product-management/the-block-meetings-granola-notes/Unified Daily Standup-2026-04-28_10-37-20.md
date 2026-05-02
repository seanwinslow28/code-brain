---
granola_id: 7d6bc8c8-c192-4145-bb93-02239046e296
title: "Unified Daily Standup"
type: note
created: 2026-04-28T14:37:20.906Z
updated: 2026-04-28T14:53:47.809Z
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
### Engineering Updates

- Crypto jobs (CoinGecko integration) nearly ready — Nicola testing on dev box, minor issues only, close to review/testing
- Pre-bid ads deployment done; main fix was adding Cloudflare headers to pass state/country data to pre-bid
	- Root issue: GDPR applied to every country incorrectly
	- Current gap: ad providers for European market aren’t GDPR-compliant — need additional providers + conditional logic per region
	- US pre-bid working; Europe currently serving no ads (or in-house fallback)
	- Compliance risk flagged: previous setup could have exposed The Block to multi-million dollar privacy law violations
- Sentry not reporting — WordPress was flooding the quota; should reset at start of new month (May 1)
- Translations tested with Caesar and Anna — rated ~9/10, reads natural; edge cases around crypto-specific terms (e.g. “wallet”) where the translation plugin lacks context

### Election Hub & SEO Bugs

- Election Hub needs to be production-ready; Brian volunteering to take it on
	- Spinning up locally is straightforward (Payload-based)
	- Nicola to provide Slack thread links for context rather than a full walkthrough
- SEO bugs: Corey flagged a high-priority broken link; Bogdan assigned to investigate
	- Lower-priority SEO bugs to be addressed as bandwidth allows

### Almax Page Updates

- No response from Almax after yesterday’s call — likely still processing options presented
- Changes expected to be relatively small; will slot in when they respond
- Open question: how to handle table scaling if rows keep being added over time — waiting on Almax direction

### Team & Org

- Christoph’s last week (state exam prep) — hopes to return; Michael confirmed he’s welcome back whenever ready
- Matt leaving — farewell party proposed for Friday, ~6:30pm; Nicola to check with Joel about hosting/opening up the venue
- All-hands in 30 minutes from standup

### Next Steps

- Nicola
	- Follow up with Almax on page update options
	- Assign tickets with context for Brian, especially Election Hub
	- Chat with Joel re: Matt’s farewell Friday ~6:30pm
- Brian
	- Pick up Election Hub bugs and SEO bugs
	- Get access sorted (with Sean’s help); ticket to be written to fully deprecate Sho going forward
- Nicola / Michael
	- Discuss Christoph’s return arrangement from The Block’s side
- Team
	- Investigate and spike CoinGecko integration — target window is second week of May (conferences pushing timeline)
	- Hold on translations until further decisions made
	- Send update to Jeffrey on ads once European side is resolved

Chat with meeting transcript: https://notes.granola.ai/t/0eb43087-c775-466c-b961-5620a7085258
