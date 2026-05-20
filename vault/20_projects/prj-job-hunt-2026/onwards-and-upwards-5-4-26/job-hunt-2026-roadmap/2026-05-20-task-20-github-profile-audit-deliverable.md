---
type: deliverable
project: prj-job-hunt-2026
task: Task 20 (A11) — GitHub Profile Audit
created: 2026-05-20
ships_by: 2026-05-22
audience: Sean (executes the changes) + future interview-prep reference
ai-context: |
  Single-source deliverable for Task 20 of the unified roadmap. Contains the bio rewrite,
  pinned-6 ordering, 4-section README inserts for each pinned repo, strategic-fork picks,
  cross-link checklist, and a 10-second-incognito-test verification gate. Drafted from
  ground truth: live github.com/seanwinslow28 scrape + roadmap context. Sean reviews,
  edits, and pushes the changes — agents draft / Sean sends boundary preserved.
related:
  - "[[2026-05-06-unified-roadmap]]"
  - "[[operating-model]]"
---

# Task 20 — GitHub Profile Audit Deliverable

> Single deliverable Sean drives the 6 steps from. Each section is paste-and-ship.

## 0. The diagnosis (so you can talk to this in interviews)

The recruiter funnel that Task 20 is designed against:
- ~30 seconds on github.com/seanwinslow28 before a recruiter opens the resume
- They scan: (a) bio, (b) pinned repos top-left to bottom-right, (c) contribution graph density, (d) whether forks are strategic or noise
- Decision rule recruiters use: *"Does this person ship things that matter, or are they a learner?"*

Your live state as of 2026-05-20 was failing this rule on every signal. Bio said "AI enthusiast looking to learn." Pinned repos were mostly forks + pre-2026 work. None of the 2026 shipped artifacts (MCP server on the registry, fleet dashboard, code-brain v4.0) appeared. **This audit moves you from "learner" to "operator" by changing what those 30 seconds see — not by adding new work, just by surfacing what already exists.**

## 1. Bio (Step 1 of Task 20)

**Recommendation: Variant A** (132 chars, under the 160 GH limit):

```
AI PM building MCP servers + an agent fleet that ships my work. New artifacts most Fridays. Boston-metro. seanwinslow.com/transactions
```

**Why this and not the others** (carry this rationale into interviews — it shows how you think about positioning):
- "AI PM" leads with the role keyword recruiters filter on, not a self-description ("enthusiast")
- "building MCP servers + an agent fleet" names two concrete deliverables; the second is the un-fakeable flex because most candidates describe agents, you operate one
- "ships my work" is the load-bearing claim — converts "I use AI" → "AI is in my production loop"
- "most Fridays" is honest cadence without overclaiming "weekly"
- "Boston-metro" gates location-filtered ATS searches
- "seanwinslow.com/transactions" routes the recruiter to the canonical ledger of shipped artifacts

**Where to put it:** github.com/seanwinslow28 → Edit profile → Bio. Save.

**Also update on the same edit screen:**
- Pronouns (if you want) — leave or set
- Company: leave blank (don't put a past employer; that's a positioning loss)
- Location: change "New York, NY" → "Boston, MA" (or wherever you'd take the next role; the bio repeats it but recruiters filter on the structured field)
- Website: `https://seanwinslow.com` (the apex, not /transactions — the apex is the brand surface; the bio carries the deep-link)
- Social links: keep LinkedIn `in/sean-winslow-204390a5`. Consider dropping Instagram from the GH profile — it pulls toward "creative kid" not "AI PM operator."

---

## 2. Pinned-6 ordering (Step 2 of Task 20)

Pin in this order — GitHub renders left→right, top→bottom:

| Position | Repo | One-line scan signal | Why this slot |
|---|---|---|---|
| 1 | sw-mcp-intent-engineering | "MCP server on the registry" | The Karpathy-named #1 portable career artifact for 2026. Goes first. |
| 2 | agent-fleet-observability | "Live dashboard at fleet.seanwinslow.com" | Proves you build observability, not just agents. Visible deploy. |
| 3 | code-brain | "118 skills, 17 SDK agents, agentic engineering toolkit" | The Karpathy "what does one of these look like in the wild" anchor. |
| 4 | sw-ai-pm-portfolio | "Design-spec-first portfolio build" | Transparency play — PM thinking made legible in repo form. |
| 5 | Pocket_PM_Claude | "AI PM tool from before the wave" | Shows lineage; you've been building AI PM tools, not jumping on a trend. |
| 6 | 16BitFit-V3 | "Mobile fitness game (BMAD method)" | Creative range — supports the AI PM > Tech PM > Creative PM positioning. |

**How to actually pin them:**
1. Visit each repo in the order above
2. From the repo's main page, click the "..." next to "Customize your pins" on your profile
3. Or simpler: profile → Customize your pins → select all 6 → save

**Unpinning the current set:** `anthropic_courses` (fork — recruiters discount forks), `mcp-server-langfuse` (fork), `Operator-grade-browser-agent-portfolio` (older Python project, gets superseded by agent-fleet-observability). Keep them public, just don't pin.

---

## 3. README inserts (Step 3 of Task 20 — the meat)

For each pinned repo, paste this 4-section block at the top of the README (after the H1 and intro paragraph, before any installation instructions). Each block runs ~200 words. The "What I Learned" answer is the one you should be ready to verbalize in 30 seconds in an interview — that's the unfakeable part.

### Repo 1 of 6 — `sw-mcp-intent-engineering`

```markdown
## Why this exists

### Problem
Engineering teams treat AI agents like reliable coworkers, but agents fail silently when given underspecified intent. The cost is shipped features that solve the wrong problem — and the failure mode is invisible until production. PMs feel this pain twice: once writing the spec, and again when an agent confidently delivers something off-target. There's no shared protocol for "audit this spec before an agent runs on it."

### Solution
A Model Context Protocol server that exposes three tools any MCP-aware client (Claude Desktop, Cursor, etc.) can call: `analyze_intent_spec` audits a spec against a 25-item rubric, `generate_template` scaffolds new specs by kind, `audit_existing_spec` retrofits older docs. Published to npm as `@swins/intent-engineering-mcp` and to the official MCP registry as `com.seanwinslow/intent-engineering` via DNS-verified namespace.

### Tradeoffs and Decisions
- **TypeScript over Python**: the MCP TS SDK has the deepest client coverage (Claude Desktop, Cursor) — at the cost of locking out the Python-native data science crowd.
- **stdio transport over HTTP**: zero-infra v0, but couples the server to a process-bound client. v1 will add SSE for cloud agents.
- **DNS-verified namespace (`com.seanwinslow/*`) over GitHub-handle namespace**: locks the brand surface to a domain I control; required a separate Ed25519 keypair + apex TXT record, which is more upfront friction than `mcp-publisher login github`.

### What I Learned
The MCP protocol is essentially a contract for "I am a tool an LLM can call without me writing a wrapper." Once that landed, the server became a thin protocol adapter over an existing skill — and the OPTIONAL-fields pattern I'd developed on a separate knowledge-graph project translated directly. The most non-obvious win: the server scored 23/25 with zero anti-patterns when audited by its own tool. **A tool that successfully eats its own dog food earns more credibility in 30 seconds of demo than 30 minutes of documentation.**
```

### Repo 2 of 6 — `agent-fleet-observability`

```markdown
## Why this exists

### Problem
Operators of multi-agent fleets face a credibility wall when talking to non-technical stakeholders: "trust me, I have an agent fleet running" doesn't survive the question "show me." Cloning a private monorepo isn't an answer. The fix has to be *a screen recruiters and execs can look at for 30 seconds and walk away believing.*

### Solution
A static observability dashboard at fleet.seanwinslow.com showing the autonomous agent fleet's last-night telemetry: agent run statuses, cost trends, model mix, the synthesizer's 60-night accuracy line with the 2026-05-01 → 2026-05-10 silent regression explicitly annotated, eval case grid, recent runs table, kanban board with live-pulse on currently-running tickets. Two render passes share 90% of logic: public (anonymized) is the URL anyone sees; private (named entities visible) is deployed behind an auth boundary.

### Tradeoffs and Decisions
- **Inline SVG for every chart over Chart.js / Grid.js**: page weight stays under 50KB, deterministic build output, charts survive screenshots, no CDN race on cold cache. Cost: SVG helpers are hand-rolled — `line_chart`, `sparkline`, `donut`, `stacked_area` in `lib/svg_charts.py`. Acceptable because the chart vocabulary is small and stable.
- **Combined `lib/render.py` over separate public/private files**: DRY beats the original two-file split because both passes only differ by one `anonymize.public_pass()` call before render.
- **Filesystem reads over a database**: the underlying telemetry is already JSON/CSV/SQLite on disk; adding a backend would have meant duplicating state for zero new capability.

### What I Learned
**Observability is a recruiting tool, not just an engineering tool.** I built this because I needed it for my own fleet's debugging — and discovered that the same view, anonymized, was the single most effective "show me" answer to a recruiter or hiring manager. The architectural choices that made the page fast (inline SVG, no JS) also made it screenshot-able, which made it shareable. **When the user is a recruiter, page weight is a recruiting metric.**
```

### Repo 3 of 6 — `code-brain`

```markdown
## Why this exists

### Problem
"AI-augmented engineering" is everywhere as a buzzword but almost never as a working artifact. Most engineers' AI integration is "I open Claude and ask it things." Karpathy's argument is that the durable form of this looks more like an operating system — a personal toolkit of skills, agents, and a knowledge graph, all auto-loaded into the workflow. The gap: nobody had published one in the open.

### Solution
A personal agentic-engineering toolkit and second brain: 118 Claude Code skills, 13 subagents, 14 hooks, 17 autonomous Claude Agent SDK agents (8 running on launchd by default), 3 primary domain workspaces, an Obsidian vault with PARA structure + nightly knowledge synthesizer, and a local verbatim TTS pipeline (Kokoro-82M ONNX) that turns vault docs into MP3s for $0/run. Every component is in active use; every scheduled agent has a launchd schedule.

### Tradeoffs and Decisions
- **Monorepo over many small repos**: keeps the agent fleet, skills, and vault co-evolving without sync hell. Cost: harder to extract individual components for others to install. Mitigation: an installer (`scripts/install.sh`) exports subsets to other projects.
- **Local models (Qwen3-14B, Kokoro-82M) for high-frequency loops + cloud Sonnet/Opus for high-stakes calls**: optimizes cost per agent run by routing — Qwen handles the nightly vault synthesis at $0; Sonnet drafts only when local can't ground. Cost: routing logic + a HybridRouter abstraction adds complexity.
- **launchd over GitHub Actions for scheduling**: agents run on hardware I own + observe directly; no opaque CI environment to debug. Cost: doesn't scale to a team; that's fine — this is a personal OS.

### What I Learned
**The queue file is the entire UX.** I started by building rich CLI interfaces for each agent and discovered they all converged on the same shape: "read this markdown queue, do work, write output back into the vault." Once I stopped fighting that shape and made every agent treat a queue file as the interface, the fleet became composable — agents started consuming each other's outputs without either side knowing about the other. **The lesson generalizes: the right interface for an autonomous agent is rarely an API; it's a file the agent and the next agent both read.**
```

### Repo 4 of 6 — `sw-ai-pm-portfolio`

```markdown
## Why this exists

### Problem
Most PM portfolios fall into one of two template traps: the design-system viewer (color swatches + type samples + component cards — a designer's tool, not a portfolio) or the luxury-minimal PM site (minimal serif + abstract gradients + "VISION MEETS VELOCITY"). Both communicate "I followed a template." Neither communicates "I have judgment." For an AI PM specifically, the failure mode is worse — recruiters can't tell the candidates apart because the artifacts are interchangeable.

### Solution
A portfolio rebuild that anchors to three non-fungible loads: (1) a hand-drawn pencil-test character that's mine, (2) a calibrated comedic voice (Sedaris-tuned, encoded as a writing-voice-modes skill), (3) a "daily-dated layer" that surfaces real autonomous agent-fleet activity onto the page, dated to the morning it was written. Stack: Astro 5 + Tailwind 4, two fonts only (Newsreader + JetBrains Mono), one splash color per section. Currently in design-spec-first phase: 12 locked specs under `docs/specs/`, build starting Phase 0→Phase 2.

### Tradeoffs and Decisions
- **Specs-first build over jump-to-Astro**: prior two attempts (V3 + V4) drifted into template-land because the design philosophy wasn't locked before code started. V5 locks the voice, character, and "daily-dated layer" first. Cost: looks docs-only to recruiters who don't read deep.
- **Astro over Next.js**: islands architecture suits a content-heavy portfolio with minimal interactivity; ships less JavaScript; faster cold loads. Cost: smaller ecosystem of recipes for unusual layouts.
- **Two fonts, hard limit**: Newsreader (editorial/serif) + JetBrains Mono (terminal/wire-service). No Inter, no Sora, no third-font flex. Discipline forces the design to lean on rhythm and color, not type variety.

### What I Learned
**The template trap is a failure of locking decisions early enough.** Both prior attempts had good specs that I let drift mid-build. V5's discipline — every spec gets a `*-spec-v1.md` lock file, every change goes in `CHANGELOG.md`, the master plan stays strategic and specs stay tactical — is what's making the difference. The lesson is a PM lesson disguised as a design lesson: **the rate at which you let a spec re-open is the rate at which the build drifts.**
```

### Repo 5 of 6 — `Pocket_PM_Claude`

```markdown
## Why this exists

### Problem
Founders, ICs, and PMs all routinely hit the same wall: "I have an idea but I don't know how to break it down into a real product spec." The naive answer is "ask Claude" — but that produces a blob, not a structured PM artifact. What's actually needed is a tool that takes an underspecified idea and outputs PM-shaped documents: problem statement, target user, MVP scope, success criteria.

### Solution
A web app that takes a one-paragraph idea and breaks it down through a PM's lens — outputting problem framing, user segments, MVP scope, and a phased roadmap. Built with Claude (the inference layer), Cursor (the build environment), and Railway (deploy). Single-page UX; no signup; designed to be the lowest-friction way to get from "I have a thought" to "I have a structured doc to share."

### Tradeoffs and Decisions
- **Single-page web app over a CLI or VS Code extension**: maximum reach (anyone with a browser), zero install friction. Cost: no version history, no shareable canonical URLs per breakdown.
- **Railway over Vercel for deploy**: simpler env-var handling for the Anthropic API key at the time. Vercel would be the choice today.
- **No persistence layer**: every breakdown is stateless. Pro: zero account/DB burden. Con: can't return to a past breakdown.

### What I Learned
**Structure is the product, not the inference.** Claude can write PM artifacts well if you give it the right scaffolding; the real product was the prompts and the shape of the output, not the underlying model. This is the same lesson the MCP server work would later make explicit: **when LLMs are abundant, the IP is in the contract you hand them, not the model you call.**
```

### Repo 6 of 6 — `16BitFit-V3`

```markdown
## Why this exists

### Problem
Fitness apps mostly fall into two buckets: gamified-but-shallow (streaks + badges over a thin habit-tracker) or simulation-heavy-but-joyless (numeric workout logs). Neither sustains long-term engagement for people who'd actually enjoy the *game* if it were good enough to play on its own. There's room for a real game that happens to be how you log workouts.

### Solution
A mobile fitness game built with the BMAD method (Business, Marketing, Architecture, Development) as the planning framework. The game loop turns workout sessions into in-world progression: each logged workout fuels a 16-bit battle-mode character through a structured RPG arc. Built on TypeScript, designed mobile-first.

### Tradeoffs and Decisions
- **Game-first over tracker-first**: the win condition is "would this game be fun to play even if it weren't a fitness app?" Risk: shipping a half-game-half-tracker that's neither.
- **BMAD method over straight Agile**: forces the work to plan business + marketing alongside architecture and dev, instead of letting marketing become a last-mile afterthought. Cost: BMAD's heavier planning surface is overkill for a solo build.
- **16-bit visual style over photoreal or modern flat**: pixel art has a built-in nostalgia premium AND a forgiving production pipeline — solo art-direction-able. Cost: not every audience reads pixel-art as "serious."

### What I Learned
**The PM discipline shows up most clearly when you're your only PM.** I built 16BitFit-V3 partly to test whether I could hold the line on scope when there was no stakeholder forcing it — and the answer was "only with explicit rituals." The BMAD method's quarterly business + marketing planning sessions turned out to be the load-bearing discipline; without them the build would have drifted into pure engineering joy. **Translatable lesson: solo PM work needs the same forcing functions as team PM work — they just have to be self-imposed and ritualized.**
```

> **Sean: review each repo's insert before pasting.** I drafted from the roadmap context + GH descriptions; I don't have direct access to the actual code in repos 5 + 6. If anything misrepresents the work, fix the specifics before commit. The structure (Problem/Solution/Tradeoffs/Learned) is the load-bearing part — content can be edited freely.

---

## 4. Contribution-shape diagnosis (Step 4 of Task 20)

The risk the roadmap flags: your vault auto-commits 2-3x per day (`vault: auto-commit YYYY-MM-DD HH:MM:SS`). That pattern dominates the green-square graph and recruiters discount it as "automated noise, not real work."

**Diagnostic check (Sean runs in 60 seconds):**
1. Visit github.com/seanwinslow28 (logged out / incognito)
2. Look at the contribution graph for the last 4 weeks
3. Click through to a recent commit. Is the top of the list `vault: auto-commit ...` or substantive commits?

**Likely state right now (from my read of the code-brain git log):** of the last ~20 commits, ~14 are `vault: auto-commit`. That's ~70% noise to a recruiter scanning.

**Mitigation (Step 4 fix):**
- **Don't try to stop the auto-commits** — they're load-bearing for the vault sync owner rule (CLAUDE.md non-negotiable #8)
- **Do mirror substantive commits to the relevant standalone repos** so the *pinned repos* show real work cadence even when the monorepo is noisy

Specific candidates to mirror (recent substantive work from code-brain):
- `82d5e2b — v3.38.0: vault synthesizer Tier-1.5 + morning schedule swap` → mirror the synthesizer-only diff to a standalone if/when N1 Task 37 ships
- `67c6ba6 — post-rename cleanup: LaunchDaemon-safe installer + vault doc sweep` → already in code-brain, no mirror needed but visible in code-brain pinned repo
- The agent-fleet-observability and intent-engineering MCP repos already have clean substantive history (no vault auto-commits) — their pinned status will lift the perceived contribution shape on its own

**Bottom line:** pinning the 4 substantive 2026 repos (intent-engineering, fleet-observability, code-brain, sw-ai-pm-portfolio) is itself the contribution-shape fix. The auto-commit noise is in a single repo that will appear as #3 in the pinned set, but the surrounding 5 repos read as substantive work, so the overall scan signal flips.

---

## 5. Strategic forks/contributions (Step 5 of Task 20)

**Roadmap target:** 3 forks/contributions that anchor your contribution graph to the AI ecosystem.

**Recommended 3** (with rationale for each — carry into interviews):

| # | Fork target | Why this one | Action (15 min total) |
|---|---|---|---|
| 1 | `modelcontextprotocol/typescript-sdk` | You shipped an MCP server. Forking + starring the SDK you used signals "I work in this ecosystem." Optional micro-PR: a typo fix or doc improvement you noticed shipping intent-engineering. | Fork + star. If you noticed any rough edges shipping, open an issue describing it. |
| 2 | `anthropics/anthropic-sdk-typescript` | Anthropic FDE is your wildcard Week-2 application. Forking the SDK = "I use this in production." | Fork + star. |
| 3 | `anthropics/courses` (the *real* one, not your existing fork) | You already have a fork — unpin it (it's currently pinned at slot 1) but keep the fork visible. Helps you remain in the GH Anthropic ecosystem graph. | Already forked. Optional: do one course exercise + push the notebook to the fork. |

**Alternative 3rd-pick** (if any of your target-30 companies is on GH with a forkable repo): pick one. E.g., `linear/linear-sdk` if Linear is on your list. Demonstrates "I'm building toward this company specifically."

---

## 6. Cross-link checklist (Step 6 of Task 20)

Five clicks, five places to update. Do all of them in a single ~10-minute session so they ship together.

- [ ] **GitHub profile → Website field**: set to `https://seanwinslow.com`
- [ ] **LinkedIn → About section**: append the line "Code at github.com/seanwinslow28 — pinned repos are the live work."
- [ ] **LinkedIn → Featured section**: add github.com/seanwinslow28 as a featured link with a custom thumbnail (screenshot of the pinned-6 grid)
- [ ] **Substack profile**: add github.com/seanwinslow28 as the linked website
- [ ] **seanwinslow.com (when live)**: footer link to github.com/seanwinslow28

---

## 7. Verification gate — the 10-second incognito test

The roadmap's binary success criterion for Task 20:

> *Open github.com/seanwinslow28 in incognito. Within 10 seconds, a reader should be able to say "this person builds MCP servers and ships evals" — not "AI enthusiast."*

**Run this test yourself once everything above is shipped.** Specifically:
1. Open a fresh incognito window
2. Navigate to github.com/seanwinslow28
3. Set a 10-second timer
4. Read top to bottom: bio → pinned 6 → any visible work cadence
5. Verbalize what you'd say if asked "who is this person?" right now
6. **Pass criterion:** your sentence contains "MCP," "agent fleet," and/or "ships [something]"
7. **Fail criterion:** your sentence contains "enthusiast," "learner," or you say something generic like "AI guy"

If you fail, iterate the bio first — it's the cheapest fix.

---

## 8. Execution sequence — what order to do this in (60-90 min total)

1. **5 min:** Update bio + location + website field on GH profile (Section 1)
2. **3 min:** Re-pin the 6 repos in the order specified (Section 2)
3. **30-45 min:** Paste the 4-section README inserts into each of the 6 repos. Commit each with a clean message like `docs: add Why-this-exists section per task-20 audit`. (Section 3)
4. **5 min:** Fork the 3 strategic targets (Section 5)
5. **10 min:** Cross-links — GH profile Website field, LinkedIn About, Substack profile (Section 6)
6. **2 min:** Run the 10-second incognito test (Section 7)

**Total Sean-time: ~60-90 minutes. Ships Task 20 by Friday 5/22 with 1 day of buffer.**

---

## 9. Interview talking points (carry these forward)

The "why" behind each decision so you can explain choices during interviews:

1. **"Why MCP servers as your primary 2026 portfolio piece?"** — Karpathy's argument: the durable artifact of the agent era is the protocol surface, not the model. MCP is the protocol agents read; shipping one to the official registry is the highest-leverage signal you can put on a 2026 PM resume.

2. **"What's the lesson from the dogfood result on intent-engineering?"** — A tool that scores well when audited by its own rubric earns instant credibility. More general lesson: build tools whose internal quality you'd be embarrassed for the tool itself to surface.

3. **"Why a 4-section README structure?"** — Recruiters scan 4 things in 30 seconds: what is it, how does it work, what choices did you make, what did you learn. The structure mirrors that scan path.

4. **"Why did the bio matter so much?"** — Bio is the only persistent text recruiters read every visit. "AI enthusiast" is the single highest-frequency anti-pattern in PM/eng job-hunt advice from 2024-2026. Removing it is a single edit that compounds across every recruiter visit.

5. **"Why mirror substantive commits, not stop the auto-commits?"** — The auto-commits serve a real engineering purpose (vault git ownership). Surface area matters more than purity — pinning the 4 standalone 2026 repos flips the perceived contribution shape without breaking the underlying system.

---

*End of deliverable. Task 20 verification gate is Section 7. When you pass, mark Task 20 closed in the unified roadmap. The next task on the imminent list is Task 13 (Access-vs-Meaning Manifesto, draft-lock Fri 5/23).*
