**Layer 4 — Institutional Knowledge → SOUL.md Part B**

This is the tacit/tribal layer — the stuff not in Confluence. If any of these are easier to answer by pointing me at specific Granola transcripts, say the word and I'll grep for context.  
**1\. Internal vocabulary.** Block-specific acronyms, project codenames, product nicknames, jargon. My running list from Layers 1–3: .Co (theblock.co), Campus, Pro (The Block Pro paid tier), Pro Research / Pro News / Pro Data / Pro Deals / Pro API, Launchpad, Sponsored Courses, Election Hub, Report Cards, The Starting Block, Voting Block Index, Knowledge Token Taxonomy, Prerequisite Schema, ToGroom, NeedsDesign, /llms.txt. What else do people drop into Slack that a new teammate would have to look up? Any nicknames for people, teams, or rooms?

1) I would  include the Block iOS app. That will be officially released on the app store soon. Writing tickets for the app will probably be a part of my day to day down the line. I would also add Marketing Site Update, Stripe Integration, Twitter/X Auth, and Crypto IQ. I would also add x402 protocol in there. It’s not implemented yet, but I’ll be pushing for that in the future. I have a bunch of deep research documents within this file path: /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/\_inputs/x402 Deep Research – No need to dig through all of those docs. Just know that they exist. We can add them into the vault somewhere, if needed. Outside of that and everything you just said, you’d find more info by looking through Jira/Atlassian via MCP  or the Granola transcripts. There’s a lot to parse through, so no need to go crazy over it. You got most of it down. 

**2\. Sacred cows.** Decisions or conventions every proposal has to respect — "we don't touch X," "everything has to route through Y," "Matt/Ed will always push back on Z." Specific examples: is there an unspoken rule about not breaking The Block Pro subscriber experience? A style rule for how P\&E updates are worded? A ceiling on roadmap-ambition pitches pre-CEO?

2) When creating presentation Slides, we always have to use the simple template within Figma. Here’s a link to the 2026 Product Roadmap Ed and I are currently working on: [https://www.figma.com/slides/V7KnGbiTK0yiCY4SKYj4dv/Product-Roadmap-2026-Draft?node-id=0-20\&t=qhRmjsD9GVOglaTV-0](https://www.figma.com/slides/V7KnGbiTK0yiCY4SKYj4dv/Product-Roadmap-2026-Draft?node-id=0-20&t=qhRmjsD9GVOglaTV-0) – You’ll also find the Jira ticket writing best practices/guides within the jira-automation skill. – When presenting something you worked on, you should always follow the presentation rules of: Context \--\> problem \--\> solution – Also, when creating a PRD or presentation, we should ALWAYS keep the user journey in mind when it comes to creating new products/pages on the blocks site. We don’t want the user to be overwhelmed with clunky steps and then give up trying to get to the end point. – For Roadmap ambition, it really depends. For this current roadmap, Ed and I started off with different levels of ambition. Matt ended up telling us that those are interesting, but way out of scope. We just want to show the new CEO that we have a good product that already makes money, but how can we revamp it based on the current markets to make it better. There could be other situations where tossing out big ideas during a blue sky phase works well because it could inspire other ideas and we can cherry pick/scale down. 

**3\. Unwritten communication rules.** Channels where you DM vs. post in public. When to @channel vs. @here vs. tag Ed vs. tag the CPO. When to Slack vs. email vs. Jira comment vs. Confluence. What's the "no meetings before X" or "don't DM David after Y" kind of thing? Response-time expectations — is Ed a "respond within an hour" guy, or async-ok?

3) I mostly use Slack for communication. We never email unless it involves someone outside of the company, but that’s rare for me to be involved (for now). When it comes to Jira/Figma/Confluence comments, we mainly do that when we want to have a paper trail of what was said in case we ever have to go back to those tickets/designs. I usually answer Ed’s DM’s (D09RWHRC9HC) as quick as possible, depending on what I’m doing. He’s in Portland, OR on West Coast time, so he sometimes Slacks me while I’m making lunch or something. Outside of that, I answer him ASAP. Being that everyone is all over the country, we just send slack messages whenever and don’t expect a quick response unless the person is in your time zone. For the P\&E Bi-Weekly Update, I post in the \#ask-product-management channel (C02N3UFMTEC). Here’s the post from the P\&E Bi-weekly Update this past Friday April 17th, 2026:   
   @here

Latest bi-weekly update is here. Here's what shipped in the past 2 weeks:

[https://theblockcrypto.atlassian.net/wiki/spaces/\~804285383/pages/276955171/Product\+Engineering+End+of+week+status+update](https://theblockcrypto.atlassian.net/wiki/spaces/~804285383/pages/276955171/Product+Engineering+End+of+week+status+update)

* **.Co** \- Ratings pages recirculation adjustments live  
* **.Co \-** GA4 session tracking improvements  
* **DevOps \-** AWS/Terraform cost optimization & deprecated account cleanup  
* **.Co & Campus** \- Visual bugs, UX improvements, SEO fixes

That’s the only time I do an @here for anything unless I’m told otherwise. 

**4\. Ask X about Y — resident experts (5–10).** I'll seed this from your roster and the team-roles doc, but you know who *actually* answers on specific topics faster than the org chart would suggest:

* The Block's internal data API → Mike Price  
* Campus compliance → David  
* SEO on Learn / Data pages → Koray  
* DevOps / staging / Jira-Slack plumbing → Cesar  
* Design system → Josh (director) / Claudine / Serena  
* ETF research signal → Steven Zheng's team (via \#research-etf)  
* AI-adjacent experimentation → Krystof Oliva (intern, AI-leaning) and Jordan Leech (fellow AI obsessive)  
* AdOps / RevOps tooling → Lil Danowski / Karla Vallecillo  
* Media / video production → Gareth Jenkinson, Jordan Leech, Davis Quinton   
* P\&E wording preferences → Ed Rupkus  
* Strategic direction (interim) → Larry Cermak Which ones are wrong? Who else should be on this list?

4) All of those are accurate. I added some more details to what you listed, but  I would take Larry off the list. I’m rarely in communication with him – I would also add Brian Mendoza, Ramuald Vishneuski, and Nikola Pivcevice as the go-to developers for most of the dev related questions I have, along with Mike Price. I go to Ed for almost everything. He can always point me in the right direction if he doesn’t know the answer. 

**5\. Past landmines.** Decisions that got reversed, patterns that failed, things that "we tried once and won't do again." You mentioned: CYA communication logs (twice) — what triggered them and who were they about (without naming names if sensitive)? Anything about The Block Pro that "we're not doing again"? Any scope-creep patterns on Campus or Sponsored Courses?

5) The main thing is communication issues with David. There have been 2 big situations where he wasn’t on the same page with the devs, and that led to a lot of rushing and mistakes down the line. We’re trying to resolve that with the weekly Campus team meetings. 

**6\. Week-one tacit knowledge.** If a sharp new PM joined Ed's team tomorrow, what would they need to know in week one that nobody would bother writing down? Think: the quirk of how a meeting actually runs vs. the invite, which Slack channel is "where real decisions happen" vs. "where announcements go," which part of Jira is fiction vs. load-bearing, who to sit next to in in-person events, which internal tool has a gotcha.

6) I would tell them to take as many notes as possible (or use granola or gemini meeting transcripts), read through the relevant confluence docs to brush up on the best practices, don’t be afraid to raise your hand and ask Ed and myself questions, take on tasks/projects without asking and then bring it up in the next meeting, and to pay attention to these slack channels:  
   1) **Ask-product-management (C02N3UFMTEC)**  
   2) **Dev (C07DNU1MQBZ)**  
   3) **Deployment-approval (C0590T88MUM)**  
   4) **Product-design-team (C04EU3840M8)**  
   5) **Research0etf (C09EXM9FYAG)**  
   6) **Social-media-marketing (C09L89LQAT0)**  
   7) **Tech-seo (C029B19JPQ8)**  
   8) **Tech-support (C0259QCR34G)**  
   9) **General (CR5D2HQ13)**  
   10) **Ped-team (C02PHB06BS6)**

**7\. Things collaborators have learned about you.** How do Ed / Matt / David / the devs adjust their behavior based on *your* working style? E.g., "Sean replies to Slack inside his 3–5 PM sweep, not throughout the day" or "Sean won't commit to a P\&E wording change until he's checked Granola" or "Sean always drafts in Claude first, then edits." What's the Sean-handling manual that's started to form?

7) They know I love to use Anthropic models/workflows and that I’m interested in AI tools/building things, so they go to me for technical help in that realm. They don’t know that I use Granola or that I use Claude to help me draft messages/comments. They know I use it for ticket writing and research, but that’s about it. They know I answer quickly, no matter what. That window where I try to take breaks doesn’t mean I stop responding. I just step away from my computer, but I’ll respond on my phone. Ed is a big inspiration and a great product manager who is extremely reliable and is all over Slack and any projects that the Block is working on. I aspire to be a hard working PM like him, but with my own creative/technical prowess to help me in my specific path to greatness. 