# Zapier MCP Tool Recommendations for Claude Code & Claude Desktop
**Date:** February 15, 2026 | **Context:** Sean Winslow's PM work at The Block + personal projects

---

## How Zapier MCP Works (Quick Reference)

**What it is:** Zapier acts as a bridge between Claude (Code or Desktop) and 8,000+ apps. You pick specific actions ("tools") within each app, and Claude can execute them via natural language.

**Cost model:** Each successful MCP tool call = **2 Zapier tasks** from your plan's quota. Failed calls don't count. This is important for budget planning.

| Plan | Tasks/month | Monthly cost | Cost per MCP call |
|------|-------------|-------------|-------------------|
| Free | 100 | $0 | ~$0 (50 MCP calls max) |
| Professional | 750 | $19.99/mo (annual) | ~$0.053 per call |
| Team | 2,000 | $69/mo (annual) | ~$0.069 per call |

**Key constraint:** Since you're using The Block's Zapier, check what plan they're on and whether your MCP usage draws from a shared task pool. If it's Enterprise, MCP may need to be explicitly enabled by an admin.

**Setup:** You're already on the MCP tools page, so you know the drill. Each tool you add becomes available to Claude as a callable function.

---

## Your Current Setup (What I See)

**12 apps connected, ~175 tools total:**

| App | Tools | Primary Use |
|-----|-------|-------------|
| Google Analytics 4 | 6 | **THE GA4 WORKAROUND** — Run Report is the key tool |
| Google AI Studio (Gemini) | 9 | AI generation from within Claude |
| Google Docs | 14 | Document creation/editing |
| Confluence Cloud | 3 | Wiki/documentation |
| Jira Software Cloud | 22 | Ticket management |
| Gmail | 12 | Email automation |
| Salesforce | 9 | CRM/pipeline data |
| Google Sheets | 28 | Data storage/reporting |
| Zapier Tables | 11 | Structured data |
| Google Calendar | 13 | Scheduling |
| Slack | 27 | Team communication |
| Google Drive | 21 | File management |

---

## The GA4 Breakthrough

This is likely the workaround you've been looking for. Here's why:

**"Run Report for a Property"** lets you pull GA4 reports via Zapier's authenticated connection — meaning Claude can request analytics data without you needing Google Cloud admin access. Zapier handles the authentication through the connection you (or your team) already set up.

**What you can likely do now:**
- Ask Claude to pull page views, sessions, user counts for TheBlock.co or Campus
- Get conversion data and event tracking metrics
- Run custom dimension/metric reports
- Pull traffic source breakdowns

**What to test first:**
1. In Claude Desktop or Code, ask: *"Use the GA4 Run Report tool to get the last 7 days of page views for [your GA4 property]"*
2. If it works, you just bypassed the Google Cloud admin blocker entirely
3. The "API Request (Beta)" tool is your escape hatch — it lets you make raw HTTP requests with GA4's authentication, which means you can access any GA4 API endpoint Zapier hasn't built a specific tool for

**Important caveat:** This uses Zapier's authenticated connection to GA4. If The Block's GA4 is connected to Zapier at the org level, you should have access. If it requires individual Google Cloud credentials, you may need someone with admin access to connect it once in Zapier. But once connected, Claude can query it freely.

**Also add Looker if available:**
Zapier has Looker tools including "Run a Selected Look" and "Execute a SQL Query." If The Block uses Looker (not just Looker Studio), adding these tools would let Claude pull dashboard data directly. Looker tools available through Zapier:
- Run a selected Look
- Execute a SQL query
- Create a render task (export dashboard to image/PDF)
- Find a user
- Add/create users

---

## Recommended Tools to ADD — For PM Work at The Block

### Tier 1: Add Now (High impact, directly supports daily work)

| App | Key Tools to Add | Why |
|-----|-----------------|-----|
| **Looker** | Run a Selected Look, Execute SQL Query | Completes the analytics workaround alongside GA4. Pull dashboard data into Claude for analysis. |
| **WordPress** | Create Post, Update Post, Find Post, Get Post, Upload Media | You work with WordPress for The Block's site. Let Claude draft and push content, update ETF pages, manage posts. Pairs with your existing ETF page creator skill. |
| **Figma** | Get File, Get Comments, Get Images | Pull design specs and assets into Claude for PRD writing, design review, or prototype scaffolding. Connects to your design team workflow. |
| **GitHub** | Create Issue, Create Pull Request, Search Repos, Get File Contents, Create/Update File | Code review, PR management, and file operations directly from Claude. Essential for dev team coordination. |

### Tier 2: Add Soon (Workflow optimization)

| App | Key Tools to Add | Why |
|-----|-----------------|-----|
| **Notion** | Create Page, Update Page, Find Database Item, Add Block to Page | If you or anyone at The Block uses Notion. Also useful for personal knowledge management alongside Obsidian. |
| **Google Ads** | Create Report | If The Block runs Google Ads, pulling campaign data into Claude for RevOps/AdOps analysis. |
| **Airtable** | Create/Find/Update Records | Flexible database for tracking anything — ETFs, content pipeline, project status. Could replace some Zapier Tables usage. |
| **Netlify** | Create Deploy, List Sites | Automate deployment of your prototype projects directly from Claude. |

---

## Recommended Tools to ADD — For Personal Projects

### Personal Finance Tracker (Rocket Money Replacement)

| App | Key Tools to Add | Why |
|-----|-----------------|-----|
| **Plaid** (if available via Zapier) | Get Transactions, Get Accounts | Bank account data without building your own Plaid integration. Check if Zapier supports it. |
| **Google Sheets** | ✅ Already connected | This is your immediate finance tracking backend. Claude can write/read spending data here until you build the custom app. |
| **Zapier Tables** | ✅ Already connected | Alternative structured storage for categorized expenses, subscription tracking. |

**Immediate action:** Even before building the custom finance app, you can set up a Google Sheet as a spending tracker and have Claude categorize transactions, flag subscriptions, and generate monthly reports via the tools you already have connected.

### Automation & Workflow Building

| App | Key Tools to Add | Why |
|-----|-----------------|-----|
| **Zapier NLA (Natural Language Actions)** | If available as a tool | Meta-tool that lets Claude trigger any Zapier workflow. Useful for your Zapier→Claude Code migration goal. |
| **Webhooks by Zapier** | Catch Hook, Retrieve Poll | Create custom triggers that any of your projects can fire into. Foundation for the "Claude Code automation UI" you want to build. |
| **Code by Zapier** | Run Python, Run JavaScript | Execute code snippets within Zapier flows. Bridge between Claude Code scripts and Zapier automations. |

### Creative Projects & Side Hustles

| App | Key Tools to Add | Why |
|-----|-----------------|-----|
| **YouTube** | Upload Video, Find Video, Get Video Details | For publishing animated shorts, analyzing competitors, tracking your content. |
| **ElevenLabs** (if available) | Generate Speech | Voice generation for animated shorts directly from Claude. |
| **Dropbox or Google Drive** | ✅ Drive already connected | Store and organize sprite sheets, animation assets, project files. |

### Life Systems & Productivity

| App | Key Tools to Add | Why |
|-----|-----------------|-----|
| **Todoist** or **TickTick** | Create Task, Find Task, Update Task | Personal task management that Claude can read/write. Bridges until Obsidian is fully set up. Free tiers available. |
| **Toggl Track** (if available) | Start Timer, Stop Timer, Get Time Entries | Project time tracking — feeds into the "visualize my progress" goal. Free tier available. |
| **Apple Reminders** (via Zapier) | Create Reminder | Quick capture from Claude to your phone's native reminders. |

---

## Tools to Be Strategic About (Task Budget Awareness)

Since each MCP call costs 2 tasks, be intentional about which tools get heavy use:

**High-frequency tools (will eat tasks fast):**
- Slack (sending messages, reading channels)
- Gmail (sending emails)
- Google Sheets (frequent reads/writes)

**Low-frequency, high-value tools (best ROI per task):**
- GA4 Run Report (one call = rich analytics data)
- Looker Run Look (one call = full dashboard data)
- Jira bulk operations (batch ticket creation)
- Google Docs (document generation)

**Optimization tip:** For repetitive data pulls (like daily analytics), consider building a Zapier Zap that runs on a schedule and dumps GA4 data into a Google Sheet automatically. Then Claude reads the Sheet (1 MCP call) instead of running multiple GA4 reports (multiple MCP calls). This saves tasks significantly.

---

## Complete Recommended Tool List

### Already Connected (Keep All) ✅
1. Google Analytics 4 (6 tools)
2. Google AI Studio / Gemini (9 tools)
3. Google Docs (14 tools)
4. Confluence Cloud (3 tools)
5. Jira Software Cloud (22 tools)
6. Gmail (12 tools)
7. Salesforce (9 tools)
8. Google Sheets (28 tools)
9. Zapier Tables (11 tools)
10. Google Calendar (13 tools)
11. Slack (27 tools)
12. Google Drive (21 tools)

### Add for Work (PM at The Block) 🔵
13. **Looker** — Analytics data pull (the other half of the GA4 workaround)
14. **WordPress** — Content management, ETF page updates
15. **GitHub** — Code/PR management, dev team coordination
16. **Figma** — Design spec extraction for PRDs/prototypes

### Add for Personal Projects 🟢
17. **YouTube** — Video publishing, content analysis
18. **Webhooks by Zapier** — Custom triggers for any project
19. **Code by Zapier** — Run Python/JS in Zapier flows
20. **Todoist** or **TickTick** — Personal task management (free tier)

### Add When Ready 🟡
21. **Notion** — If useful alongside Obsidian
22. **Google Ads** — If The Block runs campaigns
23. **Netlify** — Prototype deployment automation
24. **Toggl Track** — Time tracking across projects
25. **Airtable** — Flexible database for any project

---

## Immediate Next Steps

1. **Test the GA4 workaround NOW** — Ask Claude to run a GA4 report. If it works, you just solved your biggest blocker.
2. **Add WordPress** — You already build ETF pages and work with The Block's site. This is a no-brainer.
3. **Add GitHub** — Dev coordination and code management directly from Claude.
4. **Check your Zapier plan's task limit** — Know your budget before going heavy on MCP calls.
5. **Set up a "GA4 Daily Dump" Zap** — Schedule GA4 → Google Sheets export to reduce ongoing MCP task consumption.

---

## Important Notes

- **Enterprise plans:** Zapier MCP isn't enabled by default on Enterprise accounts. If The Block is on Enterprise, you may need an admin to enable it.
- **Tool visibility:** Each MCP server's tools are only visible to the person who created them, even if the integration is org-wide. Your colleagues won't see your MCP tools.
- **Claude Code vs Claude Desktop:** Both can connect to Zapier MCP. Claude Code uses the SSE transport method. Claude Desktop uses the Integrations UI. Both use the same Zapier endpoint.
- **Task tracking:** Monitor usage at mcp.zapier.com. Every successful tool call = 2 tasks. Plan accordingly.

---

*This document should be stored in the Obsidian vault under a "Tools & Infrastructure" folder once the vault is set up.*
