**Phase 4: Current State**

| Skill | Lines | Quality | Problem |
| ----- | ----- | ----- | ----- |
| meeting-prep | 164 | Q:4 | Decent templates but zero Block-specific content |
| sprint-roadmap | 297 | Q:4 | Comprehensive framework, completely generic |
| data-analysis | 286 | Q:4 | Solid technical foundation, no Block context |
| commit-checklist | 60 | Q:3 | Thin stub, generic conventional commits |
| org-definition-of-done | 81 | Q:3 | Thin stub, placeholder criteria |
| team-styleguide | 45 | Q:3 | Thinnest skill in the pack, completely generic |

All 6 need Block-specific rewrites. The last 3 are the Q:3 stubs from the audit.

**Phase 4 Interview: The Block PM Workflows**

I already know: Technical APM, 45/35/20 split, leads daily standup, \~7-8 meetings/week (Tue-Thu), Campus 201 \+ Zapier automations, Jira usage.  
Here's what I need, organized by skill. Answer as much or as little as you want per round — you can drop answers in a doc like before.  
**1\. Meeting Prep**

1. **Daily standup:** How long? Who attends (devs, PM manager, designers, QA)? What's the agenda structure? (Blockers → progress → plans? Round-robin? Something else?)  
   1. It consists of me, my manager Ed (Product Manager), and the developers/engineers on my team. You can find their names and role titles within [team-roles.md](http://team-roles.md)   
   2. They’re scheduled from 10 AM ET to 10:45 ET, but they tend to go quick unless we have a lot to discuss  
   3. It’s a round robin unless someone has things they’d like to discuss like blockers or questions they might have about what they’re working on. I go through everyones names in Jira to filter out they’re personal Jira board. That person says what they’re currently working on, then we move on to the next.   
2. **Sprint planning:** How often? Who facilitates? How long? What gets produced?  
   1. The product team comes up with the PRD or different tasks that pop up. We create all of the design and implementation tickets. Then we’ll assign the design tickets first. Then after that’s complete, we then assign it to a developer who doesn’t have many to-do’s. It’s either that, or the devs will split up their work if someone has a lot on their plate. We also have developers that mainly focus on Campus related work (Nikita Orobenko, Aliaksandr Kryvanosau, and Nikita Gulis) and Developers that focus on the [Block.co](http://Block.co) related work (everyone else).   
3. **Other recurring meetings:** What other meetings do you run or attend regularly? (Retros, 1:1s with manager, cross-team syncs, stakeholder reviews?)  
   1. Our retro’s are once a month. They occur right after a daily stand up.   
   2. I have one on ones with my Manager Ed to go over the bi-weekly update (stakeholder updates from the P\&E department) and anything else we need to discuss  
   3. I have a 1 on 1 with David Debreczeni (Senior Manager Course Design & Compliance) every Thursday at 8am ET to discuss Campus related stuff.  
   4. The product team and design team meet every Tuesday to sync up and make sure we’re on the same page.    
   5. Bi-weekly check ins with the the SEO team and the Google Ad Manager/Rev-ops team

4. **Where do agendas/notes live?** Slack, Confluence, Google Docs, Notion, or somewhere else?  
   1. Mostly in Slack and in Confluence. We also use Google Docs and Google Sheets to share trackers, agendas, and planning sometimes.   
5. **Retro format:** Do you do retros? Format? (Start/Stop/Continue? What went well/could improve?)  
   1. We do them once a month using Retros.work ([https://retros.work/](https://retros.work/)) – It’s mostly a check in to see how everyone’s doing and making sure everyone is in a good headspace.

**2\. Sprint & Roadmap (We’ll skip this for now. My manager takes care of most of this, so I don’t have much to provide for you)**

1. **~~Sprint length:~~** ~~1 week or 2 weeks?~~  
2. **~~Team composition:~~** ~~How many devs? QA? Designers? Other PMs?~~  
3. **~~Story points:~~** ~~Do you use them? If yes, what's a typical sprint velocity range?~~  
4. **~~OKRs:~~** ~~Does The Block use OKRs? Who sets them? Quarterly?~~  
5. **~~Roadmap:~~** ~~Where does the roadmap live? (Jira board, Confluence page, Google Sheet, something else?) Who's the audience?~~  
6. **~~Reporting:~~** ~~How do you report sprint/project progress to leadership? Format?~~

**3\. Data Analysis**

1. **Metrics you track:** What are your key metrics? (Subscriber growth, API usage, Campus enrollment, page views, ad revenue — anything?)  
   1. I’m still fairly new to this, but we mostly track impressions, page views, page clicks, ad revenue, Article Click-Through Rate, Data Page Source Analysis, etc. I’ve added a document called GA4-Tracking.pdf which holds different GA4 analytics my boss asked me to look into a while back.   
2. **Tools access:** What analytics tools can you actually access? (GA4? Looker? Amplitude? Internal dashboards? Or mostly Jira/Google Sheets?)  
   1. I have access to GA4 and Looker, but not Admin access, which limits my ability to give Claude Code an API key. That’s where the Zapier MCP comes in (I can access GA4, but not Looker through Zapier MCP)   
3. **Reports:** What reports do you produce and for whom? Weekly? Monthly? Ad hoc?  
   1. I personally don’t report much just yet. My manager Ed does that. But once Campus 201 is fully live (only the enterprise version is live), then I’m sure I’ll take on those analytics.   
4. **Data sources via Zapier:** What data do you currently pull through Zapier automations?  
   1. Just GA4 for Analytics  
5. **Stakeholder format:** Do stakeholders prefer Slack summaries, Google Docs, slide decks, or something else?  
   1. For the bi-weekly updates, I write it up in Confluence and then post a summary in Slack with the link to the confluence page. 

**4\. Commit Checklist (I don’t handle this stuff. It’s all through the Dev team)**

1. **~~Commit format:~~** ~~Does The Block use conventional commits (feat:, fix:, etc.)? Or a different format?~~  
2. **~~Jira ticket keys:~~** ~~Is it always BLOCK-XXX? Are there other project keys (e.g., CAMPUS-, DATA-)?~~  
3. **~~Branch naming:~~** ~~What's the convention? (e.g., feature/BLOCK-123-description, fix/BLOCK-456-bug)~~  
4. **~~PR process:~~** ~~How many approvals needed? Any required CI checks? Who reviews your PRs?~~  
5. **~~Pre-commit tooling:~~** ~~Any linters, formatters, or hooks the team uses? (ESLint, Prettier, Husky, etc.)~~

**5\. Definition of Done (We can skip this one as well. This is mostly the developers work for the most part)** 

1. **~~Current DoD:~~** ~~Does The Block have an explicit Definition of Done? If so, what are the criteria? If not, what does "done" look like in practice?~~  
2. **~~Jira workflow:~~** ~~What are the column/status names? (e.g., To Do → In Progress → In Review → QA → Done? More? Fewer?)~~  
3. **~~Different DoD by type:~~** ~~Is the DoD different for bugs vs features vs spikes/research?~~  
4. **~~Compliance/security:~~** ~~Any specific security review or compliance requirements before shipping?~~

**6\. Team Styleguide (Another thing that the developers take care of. I know we use Nuxt4 for the front end and Wordpress for the backend. This isn’t really something that I have to worry about just yet)**

1. **~~Tech stack:~~** ~~What's the frontend stack? (React, Next.js, Vue, vanilla JS? TypeScript? Tailwind, CSS modules, styled-components?)~~  
   1. ~~I know we’ve been in the process of migrating over to Nuxt4. That’s all I know about the tech stack.~~  
2. **~~Backend:~~** ~~Node? Python? What framework?~~  
   1. ~~We use Wordpress. That’s all I know~~  
3. **~~Naming/file conventions:~~** ~~Any patterns enforced? (PascalCase components, kebab-case files, barrel exports, etc.)~~  
4. **~~Testing:~~** ~~What testing tools? (Jest, Vitest, Playwright, Cypress?) Any coverage requirements?~~  
5. **~~Linting/formatting:~~** ~~ESLint config? Prettier? Any custom rules?~~  
6. **~~API patterns:~~** ~~REST? GraphQL? How are endpoints structured?~~

**7\.** I’ve added a folder called **Additional Skills and Info To Add To Claude Superuser Pack** – this contains a lot of the context/docs I was referencing throughout these responses. It also contains images of the **Design systems** for [theblock.co](http://theblock.co) and [Campus](https://www.theblock.co/campus) – Those design systems will be necessary for the Prototype Builder I want to create.

8\. You’ll also find 3 premade skills within the folder called **Work \- The Block \- Skills** inside the **Additional Skills and Info To Add To Claude Superuser Pack** folder. Those are the 3 Skills I created when I started getting repetitive tasks: Writing Jira Tickets, Filling out the ETF fields within WordPress, and the Bi-weekly update. – Please extract and incorporate those skills into the already made skills that serve a similar purpose inside of this project. 

