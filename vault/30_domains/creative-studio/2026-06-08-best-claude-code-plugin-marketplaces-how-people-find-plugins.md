---
title: "Best Claude Code Plugin Marketplaces & How People Find Plugins — Last 30 Days"
type: research
status: complete
domain: [creative-studio, claude-mastery]
tags: [claude-code, plugins, marketplaces, discovery, last30days, research, tooling]
created: 2026-06-08
last-updated: 2026-06-08
date-range: 2026-05-10 to 2026-06-09
sources: [reddit, x, youtube, hackernews, web]
coverage: "5/5 core sources (Reddit, X, YouTube, HN, Web) + official docs/directory grounding"
tool: "/last30days v3.0"
ai-context: "Synthesized last30days research on the best Claude Code plugin MARKETPLACES and how developers DISCOVER plugins, as of 2026-06-08. RECOMMENDATIONS-type query. Community-signal pass (Reddit/X/YT/HN) supplemented with official Anthropic docs + directory fetches for the discovery mechanics and install-count grounding."
---

# Best Claude Code Plugin Marketplaces & How People Find Plugins (Last 30 Days)

> Research across **4 Reddit threads, 3 X posts, 3 YouTube videos (3 full transcripts), 3 Hacker News stories, and ~12 web pages**, 2026-05-10 → 2026-06-09, supplemented with the official Claude Code plugin docs and the two largest public directories. Query type: RECOMMENDATIONS.

## Quick verdict

There are **two marketplaces that matter and a layer of directories on top of them**. The thing people install from is the **official `claude-plugins-official` marketplace** (auto-loaded, curated by Anthropic) and its sibling **`claude-plugins-community`** (third-party plugins that passed automated safety screening). The thing people *browse* to decide what to install is a **third-party directory** — overwhelmingly **claudemarketplaces.com** (250K+ monthly visitors) or **aitmpl.com** — plus **"awesome" GitHub lists** and **Vercel's skills.sh / find-skills** directory. Discovery is still mostly social: a YouTuber's "9 plugins" video or a Reddit thread sends you to a specific install command, not to a search box. The ecosystem is huge and noisy — directories now claim **9,900+ plugins / 20,300+ skills / 2,500+ marketplaces** — so **curation and install-count are the trust signals people actually use.**

---

## The marketplace landscape (ranked by what people actually use)

### Tier 1 — The two marketplaces you install *from*

| Marketplace | What it is | How you add it | Trust model |
|---|---|---|---|
| **`claude-plugins-official`** | Anthropic-managed, auto-available the moment you start Claude Code. ~100+ plugins: LSP/code-intelligence, official integrations (GitHub, Linear, Figma, Vercel, Supabase, Slack, Sentry…), dev workflows (commit-commands, pr-review-toolkit), security-guidance. | Built in. `/plugin install <name>@claude-plugins-official` | Curated by Anthropic; "inclusion is at Anthropic's discretion" |
| **`claude-plugins-community`** | Third-party plugins that passed Anthropic's automated validation + safety screening; each pinned to a commit SHA. | `/plugin marketplace add anthropics/claude-plugins-community` → `/plugin install <name>@claude-community` | Automated review, not hand-curated |

The official one is the default and the safest. Per the in-product video breakdown, **"It's the app store for Claude Code run by Anthropic itself… `official/plugins` is built by Anthropic, `external` is third-party stuff that passed review. Honestly, the curation is what I like most — it means less garbage to dig through."** — per *BuggedIn* on YouTube. That repo is moving fast: **24K stars, but 668 open issues against only 9 open PRs** — *"people want plugins way faster than they can be merged."*

### Tier 2 — The directories you *browse* to decide

These don't host the install runtime; they aggregate everything and rank it so you can find signal in a 9,000-plugin haystack.

| Directory | Scale (as of June 2026) | Curation signal | Why people use it |
|---|---|---|---|
| **claudemarketplaces.com** | 20,300+ skills · 2,500+ marketplaces · 9,900+ MCP servers · 250K+ monthly visitors | Install count + GitHub stars + community votes; "only actively used extensions listed"; updated daily from GitHub | The de-facto "#1 directory"; browse by category (Frontend/Backend/Security/DevOps), command-palette search, trending tab |
| **aitmpl.com** | 340 plugins · 1,367 agent skills | Open-source marketplace + **CCPI** package manager | Curated collections; ships its own installer/package manager |
| **claude.com/plugins** | The official public web directory | Three tiers: *Official Integrations* / *Anthropic Verified* / *Community Plugins*; shows install counts + source links | Official, shows real install numbers, links straight to install |
| **Vercel `skills.sh` / `find-skills`** | find-skills tool has **1.8M+ installs** | Searchable by category, author, install count | "Fastest way to find skills without manually searching GitHub repos" |

### Tier 3 — The "awesome" GitHub lists (curation by hand + by bot)

- **`Chat2AnyLLM/awesome-claude-plugins`** — hand-curated list of marketplaces + plugins.
- **`ComposioHQ/awesome-claude-plugins`** — curated list extending Claude Code with commands/agents/hooks/MCP; surfaces tools like **CCHub** (a Tauri desktop app for managing the whole ecosystem: MCP marketplace, config profiles, skills/plugins browser, workflow templates, security audit).
- **`quemsah/awesome-claude-plugins`** — *automated* collection of plugin adoption metrics scraped across GitHub via n8n workflows (i.e., a data-driven "awesome" list).
- **`awesome-claude-skills`** — ~8.7K stars; the most-cited curated skills list.
- **`anthropics/skills`** — Anthropic's own production-ready skills repo.

---

## How people actually find plugins (the discovery channels)

Discovery is a funnel: **social proof → directory/list → install command.** Almost nobody opens an empty search box cold; they arrive with a name from a video, thread, or list.

1. **In-product `/plugin` Discover tab (the lowest-friction path).** Run `/plugin`, hit the **Discover** tab, and browse all connected marketplaces. The killer feature: plugins relevant to your current repo are **pinned at the top with a "suggested for this directory" label** — context-aware discovery without leaving the terminal. Each plugin's detail pane now shows a **context-cost token estimate**, a **last-updated date**, and a **"Will install" manifest** (commands/agents/skills/hooks/MCP/LSP) so you can vet exactly what it adds before installing.

2. **YouTube "N plugins" listicles (huge top-of-funnel).** The single highest-engagement artifact this month is **Austin Marchese's "9 Claude Code Plugins to Build 10x Faster"** (40.7K views, 1,467 likes). The format *is* the discovery mechanism: each plugin gets a demo + a description-box install link. Named picks: **Caveman** (token-condensing output style), **Firecrawl + Exa** (web-scraping/semantic-search stack), **Compound Engineering** (plan→work→review→compound loop), **Anthropic's official plugins** (skill-creator, frontend-design, security-guidance, legal), **OpenAI's Codex plugin** (multi-model), **buildpartner.ai**, **Morph** (fast-apply / warp-grep), and **Code Burn** (token-spend dashboard).

3. **Third-party directories (the browse-and-rank path).** When people want to *compare*, they go to claudemarketplaces.com or aitmpl.com and sort by install count / stars / votes. This is where the long tail gets found.

4. **Reddit threads + comments (social proof + skepticism).** r/ClaudeCode, r/ClaudeAI, r/claudeskills, r/AIDigitalServices. The top thread — **"9 Claude Code Plugins That Absolutely Changed My Workflow"** (r/AIDigitalServices, 409 pts) — is pure word-of-mouth discovery, and the #1 comment is literally the discovery request: *"Can someone give me the links or instructions on how I can install this?"* Reddit is also where the **garbage-detection** happens (see sentiment below).

5. **"awesome-*" GitHub lists** — the developer-native bookmark layer, increasingly **bot-maintained** (quemsah scrapes adoption metrics; claudemarketplaces pulls from GitHub daily).

6. **Manual `/plugin marketplace add` from a repo you were told about** — `owner/repo`, any git URL (GitLab/Bitbucket/self-hosted), local path, or remote `marketplace.json`. This is how niche/team marketplaces spread: someone shares a repo, you add it, its plugins show up in Discover alongside the official ones. Teams automate this via `extraKnownMarketplaces` in `.claude/settings.json` so collaborators get prompted to install on repo-trust.

---

## What's most installed (the install-count leaderboard)

From Anthropic's public directory (claude.com/plugins), early June 2026 — install counts *are* the discovery signal people cite:

| Plugin | Installs | What it does |
|---|---|---|
| **Frontend Design** | ~867K | Polished UI code that avoids generic AI aesthetics |
| **Superpowers** | ~787K | Skill/workflow framework (the big community-origin breakout) |
| **Code Review** | ~360K | Automated PR/code review |
| **Context7** | ~359K | Live, version-accurate library docs into context |
| **Skill Creator** | ~297K | Streamlines building your own skills |

(For comparison, Vercel's **find-skills** discovery tool itself reports **1.8M+ installs** — the directory tooling is now more installed than any single plugin.)

---

## Community sentiment & friction (the honest part)

- **Curation is the #1 stated value, because volume has become a problem.** With 9,000+ plugins, "less garbage to dig through" is the recurring praise for the official marketplace. The flip side: directories exist *because* the official catalog can't keep up (668 open issues / 9 PRs).
- **Skepticism about prompt-wrapper bloat is loud on HN.** The top Show HN this window — *adamsreview: better multi-agent PR reviews* (85 pts, 55 comments) — drew the month's sharpest line: **"I pay Claude, to use Claude, to write instructions for Claude, to review code from Claude."** Another: *"Holy vibe coding Batman, this looks like a repository with just a bazillion prompts of which there are already a million."* Translation: people are wary that many "plugins" are thin prompt collections.
- **Security is a first-class discovery filter.** The official docs warn plugins "can execute arbitrary code on your machine with your user privileges — only install from sources you trust." The Claude-for-Legal-2.0 walkthrough (Liam Barnes, 10.5K views) turns this into a **6-point vetting checklist** for any non-native connector: data residency, credential storage, audit trail, supply-chain/code review, scope minimization, liability allocation. *"You wouldn't install a Word plugin or Chrome extension from a complete stranger without any reviews — the same rule applies here."*
- **"Maintainer matters" is becoming a selection heuristic.** Per Austin Marchese: *"The maintainer of a plugin matters. Because these are Anthropic-developed, you can expect they'll be maintained… I bias toward tools where people are paid to keep them working."* This is why people start at the official marketplace and only venture to community directories for gaps.
- **Marketplaces-of-marketplaces are emerging.** Anthropic's **Legal Builder Hub** is literally *"the plugin that installs other plugins… the app store for legal skills"* — a vertical marketplace nested inside the platform. Expect more domain-specific hubs.

---

## Key patterns from the research

1. **Two-marketplace core, directory-layer discovery.** You install from `claude-plugins-official` / `claude-plugins-community`; you *find* via claudemarketplaces.com, aitmpl.com, awesome-lists, and skills.sh. — per official docs + claudemarketplaces.com
2. **Discovery is social-first, search-second.** A YouTube listicle or Reddit thread → a named plugin → a copy-paste install command. The directories serve the *compare* step, not the *awareness* step. — per Austin Marchese (YouTube) + r/AIDigitalServices
3. **Install-count is the trust currency.** Both the official directory and every third-party directory rank by installs/stars/votes; users quote install numbers as proof. — per claude.com/plugins + claudemarketplaces.com
4. **Curation > volume.** The ecosystem's growth (9,900+ plugins) created the need for the directory layer; "less garbage" is the stated reason people prefer curated sources. — per BuggedIn (YouTube)
5. **Security vetting is now part of discovery.** Trust tier (Official > Verified > Community), maintainer reputation, and the arbitrary-code warning shape *which* plugins people will even consider. — per official docs + Liam Barnes (YouTube)
6. **The plugin format is dead-simple, which is why there are so many.** *"A plugin is just a folder with some files — plugin.json, commands, skills, MCP. No build step, no node_modules. The whole system is JSON plus markdown."* Low barrier → flood → directories. — per BuggedIn (YouTube)

---

## Bottom line / recommendations

- **Start at the official marketplace** (`/plugin` → Discover). It's auto-loaded, curated, shows context-cost + "will install" manifests, and pins repo-relevant plugins. For most people this is enough.
- **Use claudemarketplaces.com as your browse/compare directory** when you want the long tail — sort by install count and recency. aitmpl.com and the awesome-lists are good secondary sweeps.
- **Treat YouTube listicles and Reddit threads as the awareness layer**, but verify each pick against install count + maintainer before installing.
- **Apply the security filter every time**: trust tier → maintainer → read the "Will install" manifest → only then install. Plugins run arbitrary code.
- **For Code-Brain specifically:** the discovery funnel mirrors what already exists here — the installer/export-groups model is essentially a private marketplace. The transferable lesson is the **trust-signal stack** (curation + install-count + maintainer + manifest preview), which is exactly the metadata worth surfacing in any internal skill/plugin catalog.

---

## Stats

```
✅ All agents reported back!
├─ 🟠 Reddit: 4 threads │ 458 upvotes │ 70 comments
├─ 🔵 X: 3 posts │ 88 likes │ 5 reposts
├─ 🔴 YouTube: 3 videos │ 60,271 views │ 3 with full transcripts
├─ 🟡 HN: 3 stories │ 94 points │ 57 comments
└─ 🌐 Web: ~12 pages — Claude Code Docs, claude.com/plugins, claudemarketplaces.com, aitmpl.com, Composio, Firecrawl, Bito, Build to Launch, GitHub (awesome-claude-plugins ×3), systemprompt.io
   🗣️ Top voices: Austin Marchese (YouTube, 1.5K likes), r/AIDigitalServices (409 pts), hn/adamthegoalie (85 pts) │ BuggedIn (YouTube)
```

## Methodology

- **Tool:** `/last30days` v3.0 (Reddit w/ comments, X, YouTube, HN, TikTok, Instagram, Polymarket) → community-signal pass.
- **Window:** 2026-05-10 → 2026-06-09 (last 30 days).
- **Query type:** RECOMMENDATIONS (named marketplaces/directories + discovery behavior).
- **Supplementation:** Because "marketplaces / how people find plugins" is partly a *mechanics* question, the social pass was grounded with the official Claude Code docs (`/discover-plugins`, in-product `/plugin` flow), the official directory (claude.com/plugins, install counts), and direct fetches of claudemarketplaces.com. Social sources supplied awareness/sentiment; official sources supplied the install mechanics and numbers.
- **Caveat:** Install counts and directory totals are point-in-time (early June 2026) and move fast; the official catalog had 668 open issues vs 9 PRs at capture, so listings churn.

## Sources

- [Discover and install prebuilt plugins through marketplaces — Claude Code Docs](https://code.claude.com/docs/en/discover-plugins)
- [Plugins for Claude Code and Cowork — Anthropic (official directory)](https://claude.com/plugins)
- [anthropics/claude-plugins-official — GitHub](https://github.com/anthropics/claude-plugins-official)
- [Claude Code Plugins | Skills, MCP Servers & Marketplace Directory — claudemarketplaces.com](https://claudemarketplaces.com/)
- [Plugin Marketplaces — claudemarketplaces.com](https://claudemarketplaces.com/marketplaces)
- [Claude Code Plugins & Marketplaces — aitmpl.com](https://www.aitmpl.com/plugins/)
- [Best Claude Code Plugins in 2026: Official, MCP, LSP, Design, Workflow — Composio](https://composio.dev/content/top-claude-code-plugins)
- [Top 11 Claude Code Plugins to Try in 2026 — Firecrawl](https://www.firecrawl.dev/blog/best-claude-code-plugins)
- [Best Claude Code Skills to Try in 2026 — Firecrawl](https://www.firecrawl.dev/blog/best-claude-code-skills)
- [Best Claude Code Plugins (2026): 11 Tested, 4 Worth Keeping — Build to Launch](https://buildtolaunch.substack.com/p/best-claude-code-plugins-tested-review)
- [Best Claude Code plugins in 2026 (Top 12 reviewed) — Bito](https://bito.ai/ai-tools/claude-code-plugins/)
- [Claude Code Plugin Marketplace Guide (2026) — Agensi](https://www.agensi.io/learn/claude-code-plugin-marketplace-guide)
- [Chat2AnyLLM/awesome-claude-plugins — GitHub](https://github.com/Chat2AnyLLM/awesome-claude-plugins)
- [ComposioHQ/awesome-claude-plugins — GitHub](https://github.com/ComposioHQ/awesome-claude-plugins)
- [quemsah/awesome-claude-plugins — GitHub](https://github.com/quemsah/awesome-claude-plugins)
- [9 Claude Code Plugins to Build 10x Faster — Austin Marchese (YouTube)](https://www.youtube.com/watch?v=sBF3UumkL4Y)
- [Claude-plugins-official explained in 3 minutes — BuggedIn (YouTube)](https://www.youtube.com/watch?v=uLAvaDXN_k0)
- [Everything in Claude for Legal 2.0: 12 Plugins and 22 Connectors — Liam Barnes (YouTube)](https://www.youtube.com/watch?v=_p1skxxkHuQ)
- [9 Claude Code Plugins That Absolutely Changed My Workflow — r/AIDigitalServices](https://www.reddit.com/r/AIDigitalServices/comments/1tjol8h/9_claude_code_plugins_that_absolutely_changed_my/)
- [Claude Night Market: 23 Claude Code plugins — r/claudeskills](https://www.reddit.com/r/claudeskills/comments/1tgrh6h/claude_night_market_23_claude_code_plugins_for/)
- [Show HN: adamsreview – better multi-agent PR reviews for Claude Code](https://news.ycombinator.com/item?id=48090276)


USER: I'm building a Claude Code plugin that helps someone build their own
personal "writing voice" skill. From the research you just pulled — not
from what I'm telling you — what are the loudest unmet complaints, the
exact words people use, and any gap nobody's filling? Be blunt; tell me
what works against me too.

Straight read, grounded only in what the research actually surfaced. First the honest caveat, because it works against you: that pull was about marketplaces and discovery, not about writing tools. So there is almost no direct "I wish I had a personal-voice skill" complaint in the data. What there is, is strong adjacent signal — anti-slop sentiment, a generic-output complaint, and one competitor architecture that's doing your exact mechanic for a different vertical. I'll separate verbatim from inferred so you can tell which is which.

The loudest unmet complaint: generic, sloppy, fluffy output
This is the only voice-relevant pain that shows up repeatedly and emotionally in the data.

"I realized how much time I was wasting reading AI slop" and the model "adds a bunch of additional fluff" — Austin Marchese, explaining why he installed Caveman (the #1 plugin in a 40.7K-view video).
"I'm just done with the AI slop content." — same video, his "anti-slop agreement" with viewers. He frames human-vs-robot output as an identity, not a feature.
"when I get AI advice, it feels a little bit generic" — his pitch for buildpartner.ai, whose whole reason to exist is de-generic-ifying output by pinning it to a specific voice/expert.
That's three independent "generic/sloppy/fluffy" hits in one video. The market emotion you're selling into is real and loud. But note what those tools actually do: they compress (Caveman) or swap in an expert persona (buildpartner). Neither makes output sound like the specific human using it. That's the seam.

The exact words people use
Lift these verbatim — they're the vocabulary your landing page and skill description should mirror:

"AI slop", "fluff", "generic" (the problem)
"taste profile" — @sanketnadhani: "Tuned to YOUR taste profile (capital, categories, channels, excludes)."
"your firm's voice" / "cold start interview" / "preference file" — Liam Barnes describing Claude for Legal 2.0 (more on this below; it matters a lot)
"ceremony" — HN on a prompt-wrapper plugin: "a fair bit of ceremony for what it does."
"bazillion prompts of which there are already a million" — HN, same thread.
The two words I'd build around are "taste" and "voice." They're already in the community's mouth, and neither is owned by a writing tool yet.

The gap nobody's filling
Here's the real find, and it's the strongest thing in the data for you:

The interview → preference-file → "voice" architecture already exists and is shipping — but only for organizations, never for an individual writer. Liam Barnes describes Claude for Legal 2.0 doing literally your mechanic:

"You type something like cold start interview, and Claude asks you about your practice... takes 10 to 15 minutes... Claude takes the answers, writes them into a preference file... Every skill in the plugin reads that file before it does anything else. Your firm's voice, your firm's checklist, your firm's rules."

And @sanketnadhani does the same shape (interview → "taste profile") for investing signals. Anthropic does it for legal. Nobody in this dataset does interview → preference file → a portable, reusable artifact that captures one person's writing voice. That's the white space. The pattern is proven enough that a $1,500/hr-adjacent vertical ships it, and unclaimed enough that no one's pointed it at personal prose.

Secondary gap: the marketing-voice attempts (R16 "I'm terrible at marketing so I built a thing," R11 "I let Claude Code run my Instagram + TikTok marketing") treat voice as automation output, not as a reusable skill you own and carry between projects. The artifact-you-keep framing is open.

What works against you (the blunt part)
Skill Creator already exists, is Anthropic-built, and has ~297K installs. Your plugin's mechanic — "help someone build their own skill" — is squarely in its lane. The data even hands you the death sentence, verbatim, from the same video: "if you're just one Anthropic-released plugin away from being absolutely cooked, maybe rethink what you're building." Translation: "build-a-skill" is not your moat. "Writing voice" is the only thing keeping you out of skill-creator's shadow. Lead with voice or you're roadkill.

HN's prompt-wrapper allergy is exactly your shape. "I pay Claude, to use Claude, to write instructions for Claude" and "a bazillion prompts of which there are already a million" (85 pts, 55 comments). An interview that emits a markdown file is what this crowd reflexively mocks as "ceremony." If your demo can't show output that's unmistakably more you than baseline Claude in one screen, the skeptics are right and you're noise.

Discovery will bury you. "4200+ claude skills exist — you're not using a single one" (@moneyfet1sh) and a top thread's #1 comment is just "Can someone give me the links or instructions on how I can install this?" (409-pt thread). 9,000+ plugins, ranked by install count and stars you don't have yet. A new solo plugin has zero trust signal in a market where curation and install-count are the only trust signals.

"Maintainer matters" cuts against a solo project. The stated heuristic in the research: "I bias toward tools where people are paid to keep them working." A one-person personal-voice plugin is the opposite of that signal.

The "change how Claude writes" slot is already occupied by Caveman and the official explanatory/learning output styles. You're not entering an empty category; you're arguing you do it personally where they do it generically.

The one-line strategic read
The emotion (anti-slop, anti-generic) is real and loud; the mechanic (interview → preference file → "voice") is proven by legal and finance but unclaimed for personal writing. Your entire defensibility is the word "voice," not the word "skill" — because skill-creator owns "skill," and HN will call the interview "ceremony" unless the before/after output makes the case in five seconds. Build the demo around a side-by-side where the output is recognizably one specific human, or the data says you lose.

One caution on me: this is squeezed from a marketplace-discovery pull, so the voice-specific complaints are adjacent inference, not a chorus of people asking for your exact product. If you want the real verdict, the honest next move is a /last30days run aimed straight at the pain — something like "AI writing sounds generic / how to make Claude write in my voice" — which would replace my inference with actual demand signal. Want me to run that?