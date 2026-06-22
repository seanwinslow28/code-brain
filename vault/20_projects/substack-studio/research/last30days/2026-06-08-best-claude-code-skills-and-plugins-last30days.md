---
title: "Best Claude Code Skills & Plugins — Last 30 Days"
type: research
status: complete
domain: [creative-studio, claude-mastery]
tags: [claude-code, skills, plugins, last30days, research, tooling]
created: 2026-06-08
last-updated: 2026-06-08
date-range: 2026-05-09 to 2026-06-08
sources: [reddit, x, youtube, hackernews, web]
coverage: "5/5 core sources (Reddit, X, YouTube, HN, Web)"
tool: "/last30days v3.0 deep mode"
ai-context: "Synthesized last30days deep-research report on the best Claude Code skills/plugins as of 2026-06-08. RECOMMENDATIONS-type query. X required a vendored-dependency hotfix (see Methodology)."
---

# Best Claude Code Skills & Plugins — What the Community Says (Last 30 Days)

> Deep research across **13 Reddit threads, 19 X posts, 9 YouTube videos (8 full transcripts), 56 Hacker News stories, and 10 web pages**, 2026-05-09 → 2026-06-08. Query type: RECOMMENDATIONS.

## Quick verdict

For a dev-tooling topic, the ranking signal lives on **Reddit + YouTube + HN**; X and web add install data and color. The consensus across every source: **skills are the #1 lever**, but the highest-value move is **getting context out of your head into the skill** — not collecting more plugins. The breakout tool of the month is **Grill Me** (Matt Pocock), and the loudest efficiency theme is **"CLIs beat MCPs"** on token cost.

---

## 🏆 Ranked recommendations

### Tier 1 — Most-installed / consensus picks

| Tool | Signal | Use case | Sources |
|---|---|---|---|
| **Skills + `skill-creator`** (official) | Ranked #1 Claude Code feature overall | Turn a repeated prompt into a reusable recipe; `skill-creator` drafts → tests → packages new skills from plain English | Nate Herk, Tristen O'Brien, AI LABS (YT); r/claudeskills |
| **Frontend Design** (official) | **829,316 installs** — most-installed plugin | Anti-generic UI generation | Composio, Build to Launch (web); Chase AI |
| **Superpowers** | **752,120 installs** — #2 | Structured multi-skill harness (brainstorm → plan → TDD → verify) | web (Composio); HN daily-driver thread |
| **Context7** | **348,660 installs** | Injects up-to-date, version-specific library docs to cut hallucinations | Composio, Firecrawl, TurboDocx (web) |
| **feature-dev** (official) | **89,000 installs** — top workflow plugin | 7-phase brief → working code (requirements → explore → architect → implement → test → review → docs) | Composio, Build to Launch (web) |

### Tier 2 — Breakout / high-signal this month

| Tool | Use case | Sources |
|---|---|---|
| **Grill Me / Grill with Docs** (Matt Pocock) | "Plan mode on steroids" — relentlessly interviews you to extract context *before* building; checkpoints answers to docs. **Grill Me Codex** variant adds up-to-5-round Codex adversarial review of the plan | Nate Herk ("The Skill That 10x'd My Claude Code Projects"), Chase AI (#2/#3) |
| **Firecrawl** (MCP/CLI) | Scrapes 99% of sites incl. JS-rendered; clean markdown; far less token burn than native web fetch (1,000 free pages/mo) | Tech With Tim, Ben AI |
| **Composio** | "Best first plugin" — token-efficient on-demand tool routing across 200+ apps (Gmail, Linear, Figma, GitHub, Sentry) instead of loading every tool into context | Tech With Tim (YT); Composio/TurboDocx (web) |
| **Behavioral CLAUDE.md** (Karpathy / Forrest Chang) | Four guardrails in one file — think-before-coding, simplicity-first, surgical changes, goal-driven execution (~144k–170k GitHub stars) | Chase AI (#6), web |
| **Graphify** | AST-only knowledge-graph "map" of a repo (deterministic, auto-rebuild-on-commit hook) → Claude answers codebase questions with fewer tokens than grep; can emit an Obsidian vault | Chase AI (#1), Jack Roberts |
| **Impeccable** | 23-command frontend-design skill set; live-select page elements to refine/animate — "defeating the AI slop monster" | Chase AI (#7), Ben AI |
| **/code-review** (official, free) | Anthropic marketplace, no plan gate | web; Anthropic marketplace |

### Tier 3 — Notable mentions (1–2 sources)

- **Google Workspace CLI** — full Gmail/Sheets/Docs/Calendar **read+write** (beats the read-only MCP) and more token-efficient — *Nate Herk, Ben AI*
- **Higgs Field CLI/MCP** — one-stop image/video gen (Nano Banana, Seedance, GPT Image 2) inside Claude — *Chase AI, Ben AI*
- **Printing Press** — 50+ prebuilt CLIs + builds a CLI from any MCP/API — *Ben AI*
- **Caveman** — token-compression skill (~18–40% off CLAUDE.md/skills) — *Ben AI*
- **Codex plugin** (official OpenAI) — second-opinion adversarial review; free tier exists — *Chase AI (#4)*
- **Claude Obsidian** — auto-organizes a Karpathy-style vault; hot-cache at session end — *Chase AI (#5)*
- **Notebook LM Pi** — hooks Claude Code to NotebookLM (batch downloads, slide decks) — *Chase AI (#9)*
- **n8n MCP** — best-in-class no-code automation bridge — *Chase AI (#10)*
- **Playwright CLI** — Python-script browser automation, faster/cheaper than native browser use — *Ben AI*
- **Vercel CLI** — HTML → live URL in ~10s — *Ben AI*
- **Claude video plugin** — downloads + screenshots video for true visual context (not just transcript) — *Ben AI*
- **ViProspecting / Unipile** — lead-gen + WhatsApp/LinkedIn outreach — *Ben AI*
- **GStack** (Gary Tan / YC) — 23-skill founder bundle (office-hours / plan / CEO-review / QA) — *Tech With Tim (#1)*
- **VibeSec** — pre-deploy security audit skill — *Tech With Tim*
- **Lathe** — turns Claude Code/Cursor/Codex into a hands-on tutorial builder, lessons stored locally — *@jqueryscript (X)*
- **skills-for-humanity** — 171 structured reasoning skills — *HN14*
- **adamsreview** — multi-agent PR reviews — *HN10*
- **Rayline** — routes subagents to on-device / cheaper models — *HN30*
- **Academic Research Skills** — *HN11*
- **/slides skill** — build + publish presentations — *r/ClaudeAI (R27)*

---

## Key patterns

1. **Skills win, but extraction > collection.** The breakout tools (Grill Me, skill-creator) exist to pull context *out of your head* into the skill; "brain dump for 5 minutes" never produces a good skill — *per Nate Herk*.
2. **"CLIs > MCPs" is the loudest efficiency theme.** CLIs don't reload context every session; creators are rebuilding MCP tools as CLIs (Google Workspace, Printing Press, Firecrawl) — *per Ben AI*.
3. **Anthropic's own "how we use skills" post drove the month.** Highest-signal content is the **gotchas section**; one job per skill (9 categories); **write the description for the model, not humans**; progressive disclosure via the file system; **don't railroad Claude** — *per Brock Mesarich & AI LABS*.
4. **Adversarial second-opinion loops are trending.** Codex-reviews-Claude shows up everywhere (Grill Me Codex, official Codex plugin, adamsreview) — *per Chase AI / HN*.
5. **Security caveat, repeated.** Studies cited that >⅓ of public skills have flaws / some are malicious — vet third-party skills, prefer official + self-built — *per Tristen O'Brien*.
6. **Don't install everything.** Pick one, learn it, build with it, then add the next — *per web + Tristen O'Brien*.
7. **The harness matters more than the model** (large codebases): five harness pieces = CLAUDE.md (keep ~300 lines, per-subdir in monorepos) + hooks + skills + plugins + LSP/MCP/subagents — *per AI LABS*.

## What X adds (taste over typing)

X is mostly **Claude-Code-vs-Codex discourse**, not a "best skills" ranking:
- "The job is less typing code and more knowing what to ask, review, and ship" — *@subramanya* (reinforces pattern #1)
- New in **v2.1.163**: a native **`/plugin list` command with filters** — third-party marketplaces matter a bit less over time — *@jqueryscript*
- "12 Agentic settings that double your output" (config angle, not plugins) — *@aigoldrushh*
- Voice-control startup routines (Leo) — *@daifreenft*
- "Model monogamist vs philanderer" loyalty debate — *@theHankTaylor*
- **Meta/on-brand:** `mvanhorn/last30days-skill` (the tool that produced this report) is **trending #1 on GitHub's AI trending list today** (+3,558 stars, 34,314 total) — *@sizplay_*

---

## Stats

```
✅ Agents reported back!
├─ 🟠 Reddit: 13 threads │ ~1,941 upvotes │ ~494 comments
├─ 🔵 X: 19 posts │ ~30 likes │ low-engagement builder chatter (CC-vs-Codex, taste-over-typing)
├─ 🔴 YouTube: 9 videos │ ~307K views │ 8 with transcripts
├─ 🟡 HN: 56 stories │ ~2,988 pts (top threads) │ ~1,751 comments
├─ 🌐 Web: 10 pages — Composio, Firecrawl, TurboDocx, Build to Launch, DEV
└─ 🗣️ Top voices: r/ClaudeCode, r/claudeskills │ Nate Herk, Tech With Tim, Chase AI (YT) │ @jqueryscript, @subramanya (X)
```

Marketplace scale (web, June 2026): **101 plugins** in the official marketplace (33 Anthropic-built + 68 partner — GitHub, Playwright, Supabase, Figma, Vercel, Linear, Sentry, Stripe, Firebase); **9,000+ plugins** across all platforms (ClaudePluginHub, Claude-Plugins.dev, Anthropic Marketplace).

---

## Source appendix

### Reddit (13 threads)
- r/ClaudeCode (768⬆/115💬) — Hooks vs Skills vs Plugins vs SKILL.md vs CLAUDE.md vs agents.md — https://www.reddit.com/r/ClaudeCode/comments/1tmq9kz/
- r/AIDigitalServices (409/40) — 9 Claude Code Plugins That Absolutely Changed My Workflow — https://www.reddit.com/r/AIDigitalServices/comments/1tjol8h/
- r/claudeskills (221/18) — Skill that generates a better CLAUDE.md (scans repo + 6 questions) — https://www.reddit.com/r/claudeskills/comments/1tg28ns/
- r/claudeskills (179/7) — A Claude skill that actually teaches (real pedagogy research) — https://www.reddit.com/r/claudeskills/comments/1tty5tz/
- r/ClaudeCode (160/48) [also HN] — Claude Code dynamic workflows is insane! — https://www.reddit.com/r/ClaudeCode/comments/1ts0wuh/
- r/claudeskills (49/14) — How do you find and share Claude Skills? Is there a registry yet? — https://www.reddit.com/r/claudeskills/comments/1tniqym/
- r/ClaudeCode (30/159) — What's a small useful thing you built with Claude Code? — https://www.reddit.com/r/ClaudeCode/comments/1tmnb5n/
- r/claudeskills (33/41) — Skill to stop Claude from building generic AI-slop websites — https://www.reddit.com/r/claudeskills/comments/1tu4v6s/
- r/claudeskills (38/3) — Skill that generates a personal Claude Code cheat sheet — https://www.reddit.com/r/claudeskills/comments/1tjc2ug/
- r/ClaudeAI (24/7) — Went down the Claude Code add-ons rabbit hole — https://www.reddit.com/r/ClaudeAI/comments/1tphvo8/
- r/ClaudeAI (14/10) — 20 Claude Skills for Marketing, Launch and Sales — https://www.reddit.com/r/ClaudeAI/comments/1tbaesy/
- r/ClaudeAI (9/12) — The /slides skill makes presentations genuinely easy — https://www.reddit.com/r/ClaudeAI/comments/1tqvey9/
- r/ClaudeCode (7/20) — What are your best HARNESS/PLUGINS/SKILLS/MCPS? — https://www.reddit.com/r/ClaudeCode/comments/1t81u5w/

### YouTube (9 videos)
- Nate Herk — The Skill That 10x'd My Claude Code Projects (88.6K) — https://www.youtube.com/watch?v=c0kaKxM2pHg
- Nate Herk — I Tested Every Claude Code Feature, These 12 Are the Best (74K) — https://www.youtube.com/watch?v=vfWTyEreOEc
- Tristen O'Brien — Claude Skills Explained Simply (36.7K) — https://www.youtube.com/watch?v=O6tQ6V_P8a0
- Tech With Tim — I Tried 100+ Claude Code Skills. These 6 Are The Best. (30.6K) — https://www.youtube.com/watch?v=ZSvcxjNZdxk
- Brock Mesarich — Anthropic Just Dropped Their Claude Skills Secrets (23K) — https://www.youtube.com/watch?v=VhhVoUXEGeo
- AI LABS — Anthropic Just Revealed The Best Claude Code Setup (18.6K) — https://www.youtube.com/watch?v=lGalJmyI78w
- Chase AI — The Top 10 Claude Code Plugins to 10x Your Next Project (14.6K) — https://www.youtube.com/watch?v=IShdbDP4Jgg
- Ben AI — 12 Claude Plugins, Skills & MCP's I Can't Live Without (13.8K) — https://www.youtube.com/watch?v=je95KXv1QlA
- Jack Roberts — Claude Code + Graphify = Insane Agentic OS (7K) — https://www.youtube.com/watch?v=Owv503rTqYY

### Hacker News (top of 56)
- (528/274) Using Claude Code: The unreasonable effectiveness of HTML — https://news.ycombinator.com/item?id=48071940
- (493/466) Microsoft starts canceling Claude Code licenses — https://news.ycombinator.com/item?id=48238896
- (451/254) Claude Code as a Daily Driver: Claude.md, Skills, Subagents, Plugins, MCPs — https://news.ycombinator.com/item?id=48289950
- (326/65) Claude Code – Everything you can configure that the docs don't tell you — https://news.ycombinator.com/item?id=48318174
- (253/50) A Claude Code and Codex Skill for Deliberate Skill Development — https://news.ycombinator.com/item?id=48130679
- (248/160) How Claude Code works in large codebases — https://news.ycombinator.com/item?id=48144494
- (200/135) Dynamic Workflows in Claude Code — https://news.ycombinator.com/item?id=48311705
- (116/79) Claude Code and Codex can have real-time conversation via Git — https://news.ycombinator.com/item?id=48345837
- (104/77) Show HN: Boxes.dev — run Claude Code and Codex in the cloud — https://news.ycombinator.com/item?id=48399358
- (85/55) Show HN: adamsreview — better multi-agent PR reviews — https://news.ycombinator.com/item?id=48090276
- (82/25) Academic Research Skills for Claude Code — https://news.ycombinator.com/item?id=48083919
- (55/90) Why Ctrl+V won't paste images in Claude Code on WSL, with a fix — https://news.ycombinator.com/item?id=48267432
- (28/7) Show HN: skills-for-humanity — 171 structured reasoning skills — https://news.ycombinator.com/item?id=48275571
- (10/6) Show HN: Lessons from running Claude Code swarms at scale — https://news.ycombinator.com/item?id=48407998
- (9/8) Show HN: Rayline routes Claude Code subagents to on-device/cheaper models — https://news.ycombinator.com/item?id=48448372

### Web
- Composio — Best Claude Code Plugins in 2026 (Official, MCP, LSP, Design, Workflow) — https://composio.dev/content/top-claude-code-plugins
- Firecrawl — Top 11 Claude Code Plugins / Best Claude Code Skills (2026) — https://www.firecrawl.dev/blog/best-claude-code-plugins
- TurboDocx — Best Claude Code Plugins, Skills & MCP Servers (2026) — https://www.turbodocx.com/blog/best-claude-code-skills-plugins-mcp-servers
- Build to Launch — Best Claude Code Plugins (2026): 11 Tested, 4 Worth Keeping — https://buildtolaunch.substack.com/p/best-claude-code-plugins-tested-review
- claudemarketplaces.com — Plugins/Skills/MCP marketplace directory — https://claudemarketplaces.com/

---

## Methodology / provenance

- Generated by `/last30days` v3.0 (deep mode) on 2026-06-08, save-dir `~/Documents/Last30Days/`.
- **X required a hotfix.** The vendored bird-search client's `@steipete/sweet-cookie` dependency shipped without its `dist/` folder, so every X search crashed with `ERR_MODULE_NOT_FOUND` regardless of login (and `FROM_BROWSER=auto` failed silently for the same reason). Fixed 2026-06-08 by dropping `dist/` from `npm pack @steipete/sweet-cookie@0.1.0` into the vendored package; X then returned 19 posts. Tracking + upstream-report follow-ups logged in [[tickets]] (`vault/00_inbox/tickets.md`).
- Citations favor people over publications; web cited only where Reddit/X/YT/HN didn't cover a fact.

USER: I'm building a Claude Code plugin that helps someone build their own
personal "writing voice" skill. From the research you just pulled — not
from what I'm telling you — what are the loudest unmet complaints, the
exact words people use, and any gap nobody's filling? Be blunt; tell me
what works against me too.

Pulled the complaint language straight from the raw transcripts and threads. Here's the blunt read — grounded only in the skills-and-plugins research, quotes verbatim.

The loudest unmet complaints (what people actually say)
1. "The extraction" — getting your brain into the system. This is the single most-repeated pain in the whole pull, and it's your exact problem space. Nate Herk says it plainly:

"the real challenge is still the extraction, getting everything from your head into the AI system so that your skills can use it"

…and names the failure mode everyone recognizes:

"I'm just going to brain dump into clawed code for 5 minutes and it will be good enough — it's not ever good enough"

People know brain-dumping fails. They don't have a method. That's the wedge — but see "what works against you," because someone's already in this lane.

2. Sameness / homogenization fear. The "why" behind voice, stated literally:

"everyone's going to be using the same prompts and getting the same output because the model is fundamentally the same for everybody"

Cure named in the same breath: "you give it your taste, your voice, your decisions, and that's how you get outputs that actually sound like you."

3. "AI slop" — the enemy word. This is the most emotionally charged, most-repeated phrase in the data, and it's the word to build around:

"defeating the AI slop monster" (Chase AI / Impeccable)
"a skill to stop Claude Code from building generic AI-slop websites" (r/claudeskills)
"I'm just done with the AI slop content" (creator on buildpartner.ai)
"how much time I was wasting reading AI slop"

4. Genericness they can feel but can't fix.

"I get AI advice, it feels a little bit generic. But this is a way to pinpoint it"

The exact lexicon (steal it for triggers + positioning)
AI slop · sound like you / sound like an AI generated this · talk like you · your taste, your voice · the extraction / everything from your head · brain dump … never good enough · same prompts, same output · feels generic · branded voice · humanizer. If your trigger phrases and marketing don't contain "AI slop" and "sound like you," you're speaking a different language than your buyers.

The gap nobody's filling
The research shows three pieces that exist separately and have never been combined:

Interview-extraction exists — Grill Me — but it's aimed at project/process context, not writing. Its output is a "knowledge doc" for building software.
Voice-emission exists — Branded Voice ("talk like you") and Humanizer ("so it doesn't sound like an AI") — but these are pre-built and generic. They strip robot-tells; they don't reconstruct your idiolect from your samples.
Nobody ships: interview the writer → analyze their actual writing samples → emit a reusable personal-voice SKILL.md. The seam between "extract from a human" and "emit a personal voice artifact" is empty. That's the real opening.
Secondary gap: discovery + trust. "How do you find and share Claude Skills? Is there a proper registry yet?" plus ">⅓ of public skills have security flaws / some are malicious." A plugin that ingests someone's personal writing walks straight into that trust wall.

What works against you — bluntly
Prior art is named and loved. Tristen O'Brien on Branded Voice: "teaches Claude how to talk like you and not sound like an AI. I use it, trust me, it's awesome." You are not entering empty space; you're displacing a tool people already evangelize.

Grill Me already owns the interview mechanic — and it's the breakout skill of the month, explicitly framed as capturing "your taste, your voice … outputs that sound like you." If your pitch is "interview → voice skill," the first reaction will be "that's just Grill Me + Branded Voice." Your defensibility cannot be the interview. It has to be the writing-specific parts they don't do.

Market fatigue is explicit. Chase AI: "there's so much noise out there that most of us have stopped listening entirely." You're launching plugin N+1 into a crowd that's tuned out.

The technical crowd demands evals, and will say so. HN, on a skill-builder skill: "No benchmarks and evals present, how do you know it produces better result than /create-skill? Naive testing doesn't provide any confidence." A voice plugin with no measurable "this output moved toward me and away from baseline" gets dismissed on sight.

"It's just a prompt" deflation. Nate: "a skill can just be a prompt you don't want to say every time." HN: "I pay Claude, to use Claude, to write instructions for Claude." Voice reconstruction is trivially easy to wave off as a fancy prompt unless you show otherwise.

Your buyer isn't who you think. Every voice/slop complaint in this dataset comes from creator/marketer/agency channels (Nate Herk, Tristen, Ben AI) and Reddit — not the core dev crowd. On X and HN, the loud power-users are arguing CC-vs-Codex and large-codebase harnesses; zero writing-voice demand surfaced there ("voice" on X meant speech control, not prose). Position for operators/creators. If you pitch this to HN engineers, you'll get objection #4 and a shrug.

The context-window wall will hit your core mechanic. The one proven failure mode for long interviews, from Nate: "as the context window starts to fill up I started to get worried that it was going to misremember some of my answers from earlier." Your interview is a long session. Solve checkpoint-to-disk or the product breaks in exactly the scenario it depends on. (Note: Grill Me already solved this — another reason it's the bar.)

The sharpest read
Demand is real, but the word is "AI slop," and most people mean generic content/websites, not "my personal idiolect." Two things make you defensible against Grill Me + Branded Voice, and the research hands you both:

Work from the user's actual writing samples (analysis), not just Q&A — that's the thing none of the emission tools do.
Ship an eval that proves the output moved toward them and away from baseline AI — because "naive testing doesn't provide any confidence" is the literal objection waiting for you.
Without the eval, you're a nicer Branded Voice. With sample-analysis + a real eval, you're the thing nobody in this pull shipped.

One honest flag: there are two more on-target raw files sitting in ~/Documents/Last30Days/ from later runs I did not pull — best-ai-tools-to-write-in-your-own-voice and plugin-marketplaces-and-how-people-find-plugins. The first is dead center on your topic. Want me to mine that one properly? It'll likely sharpen the "exact words" and competitor list well past what the skills-and-plugins pull can give you.