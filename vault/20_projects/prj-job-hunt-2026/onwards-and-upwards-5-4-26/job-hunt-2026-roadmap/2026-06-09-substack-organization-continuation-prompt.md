---
type: continuation-prompt
project: prj-job-hunt-2026
for: a fresh Claude Cowork session
created: 2026-06-09
purpose: "Organize the scattered substack-drafts folder into a clear series/posting system, build a daily posting queue, and map images + plugins/skills/MCPs to each post."
---

# Continuation Prompt — Organize the Substack engine (series, queue, images, tools)

Paste everything below the line into a new Cowork session. It is self-contained.

---

## Who you are and what we're doing

You are my thinking partner and editor for my Substack. Be honest, challenge me, don't
just execute. Brief and direct, no trailing summaries. Use **AskUserQuestion before any
multi-step work** and at every real decision point. Work in the code-brain repo:
`/Users/seanwinslow/Code-Brain/code-brain/`.

**The problem:** I'm supposed to post to Substack every day, but my drafts folder is a
mess. Duplicate variants of the same story, one-off stories tangled up with my flagship
series, multiple image versions with no "which is final," process junk mixed in, and no
posting order anywhere. I open the folder and freeze.

**What I need from this session, in priority order:**
1. **A folder + naming system** so I always know which story belongs to which series, what
   its status is, and what posts next. This is the most important outcome.
2. **A daily posting queue / calendar** — tell me what to post first, second, third, with
   dates, so "what do I post today?" is a one-glance answer.
3. **An image plan per post** — which image is the hero, which are superseded, what's still
   missing, and how to generate the missing ones.
4. **A tool map per post** — which plugin/skill/MCP ships alongside each post (the whole
   point of my series is each post hands the reader a tool).
5. Then, with the system in place, help me **keep strategizing and drafting** the next posts.

## How to behave (hard rules)

- **Any drafting or editing of post copy MUST go through my voice chain:**
  `writing-voice-modes` → `writing-critique` → `writing-humanity-pass` (the skills live in
  `.claude/skills/`). My voice: dive-bar grit dialed by context, **no em dashes**, the
  **layoff is suppressed** (never use it as backstory/stakes), reference governor (~1-2
  pop-culture refs max, only from my real reference universe), the ask lands sideways.
- **The drafts live inside the Obsidian vault.** You may reorganize files with plain `mv`
  (the Obsidian-Git plugin auto-commits). **Never run `git add`/`git commit` against the
  vault yourself** — that's a hard repo rule.
- **Propose the structure and get my approval before mass-moving files.** Show me the plan;
  let me say go. Then move.
- Capture any deferred work as one-line bullets under `## Todo` in
  `vault/00_inbox/tickets.md`.
- Daily posting is aggressive — be honest with me about cadence vs. quality, don't just
  cheerlead.

## Read these first (in order)

1. **The strategy + series plan (most important):**
   `vault/30_domains/creative-studio/substack-research/2026-06-09-opportunity-report-creative-agentic.md`
   — Part 4 is the 7-post series plan; the positioning brief is Part 3. This is the spine
   the whole folder should organize around.
2. **The engine/playbook:**
   `creative-studio/docs/tool-shipping-playbook.md` — every post pairs a pain point with a
   tool I ship; this explains why.
3. **The flagship that's live + its companion:**
   `…/substack-drafts/2026-06-05-raising-claude-post1.md` (Post 1) and
   `…/substack-drafts/raising-claude-cheese-gauntlet-kit-PUBLIC.md` (its tool/companion).
4. **The drafted Post 2:** `…/substack-drafts/2026-06-08-raising-claude-voiceprint-build.md`
   (the VoicePrint build narrative — already in my voice, marked DRAFT pending the chain).
5. **The six research reports** (only if you want the source pain-point quotes), all in
   `vault/30_domains/creative-studio/substack-research/`.
6. **The voice skills** in `.claude/skills/`: `writing-voice-modes` (+ its references),
   `writing-critique`, `writing-humanity-pass`, `storytelling-architecture`,
   `substack-value-engine`. Also `substack-aeo-geo-optimizer` (make posts citable by AI
   search) and the image skills below.

(The `substack-drafts` folder path in full is:
`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/`.)

## Context you need up front

**The niche / position (from the opportunity report):** *I build the judgment layer for AI
agents — intent, proof, and control — for the people who aren't backend engineers
(creatives, marketers, designers, small studios).* Every post names a pain point in the
audience's own words and hands them a gate or a lens (not another generator).

**The 7-post series plan (the spine to organize around):**

| # | Working title | Pain it answers | Ships with | Status |
|---|---|---|---|---|
| 1 | You Can't Prompt Taste Into a Machine | "humanize prompts don't work" | the Cheese Gauntlet kit | shipped |
| 2 | I Built a Machine to Sound Like You | "it's obvious, we know" / fraud guilt | **VoicePrint** | drafted (needs voice chain) |
| 3 | Correct Was Never Defined | "the missing layer is structured intent" | Intent Card / **intent-engineering MCP** | to draft |
| 4 | The Eval Tools Are Built for the Wrong People | "designed for ML engineers" | On-Brand Gate | to draft |
| 5 | Your Content Tripled, Engagement Dropped 40% | "AI slop, the arms race is losing" | the anti-slop gate | to draft |
| 6 | Stop Building Agents | "automations, not agents" (1,556 upvotes) | Agent-or-Automation Advisor | to draft (loudest hook) |
| 7 | The Judgment Layer | brand stewardship worth more as output floods | the whole stack; ties to "Access Over Meaning" | capstone |

**My shipped assets (what posts can ship with):** `intent-engineering` MCP
(`@swins/intent-engineering-mcp`, "the audit *is* the eval"), `vault-knowledge` MCP (typed
reasoning edges), the writing chain, **VoicePrint** (just built — Cowork plugin), the
design-team agents, Code-Brain.

**Image skills available:** `gemini-image-gen` (general/photo/illustration),
`gemini-pencil-animation-image-gen` (my hand-drawn pencil-test character — the load-bearing
brand character), `image-generator-prompt-science` (prompt craft). My invented image format
(from the cheese-bank): **a cheesy caption paired with a grotesquely-detailed image** as
overt satire — that's a repeatable post-image style. Image-gen reference assets already sit
in `…/substack-drafts/substack-image-generation-references/` (my headshot + style refs).

## The current mess (what you're cleaning up)

Everything is loose in `substack-drafts/`. Real inventory as of 2026-06-09:

- **Flagship series, scattered in root:** `2026-06-05-raising-claude-post1.md`,
  `2026-06-08-raising-claude-voiceprint-build.md`, `raising-claude-cheese-gauntlet-kit-PUBLIC.md`
  (+ a non-PUBLIC `-kit.md` duplicate), `2026-06-05-the-confident-stranger.md` (read it —
  likely a VoicePrint/voice story).
- **The "Access / Meaning" thread, scattered + duplicated:**
  `2026-06-19-meaning-over-access-substack-cross.md` (cross-post, publish target 6/19),
  `2026-06-07-access-vs-meaning-dive-bar.md` **and** `…-v2-Seans-edits.md` (two variants),
  `2026-05-10-the-night-my-vault-said-nothing.md` **and** `…-kerouac-variant.md` (two
  variants of the silent-regression story), `intent-engineering-mcp.md` (1K stub, status
  active) + a fuller `experiments/voice-calibration/2026-05-14-intent-engineering-mcp.md`.
- **One-off / agentic war stories with no home:** `2026-05-29-ldr-grounding-collapse.md`
  (could feed new Post 6 "Stop Building Agents" or a "ghost debugging" post).
- **Duplicate/variant noise to reconcile or archive:** the `-kerouac-variant`,
  `-beatmap` files (`the-confident-stranger-beatmap`, the archived post1 beatmap),
  `-v2-Seans-edits`, the `archive/` folder, and `experiments/` (council-sessions +
  voice-calibration — these are process artifacts, not posts).
- **Images, unmapped:** `images/` holds headers with `-superseded`, `-chatgpt`,
  `-openai-test` variants for several posts — no clear "this is the final hero for post X."
  Plus the `substack-image-generation-references/` folder.

**The six problems to solve:** (1) series vs one-offs are mixed; (2) duplicate variants of
the same story; (3) no posting order; (4) images aren't tied to posts or marked
final-vs-superseded; (5) no tool-per-post map; (6) process artifacts mixed with publishable
drafts.

## Your task (deliverables)

**A. Audit + classify every draft.** Read each `.md`, and produce a table: file → which
series/story → status → is it a duplicate/variant/superseded → which post-slot it maps to
(or "idea, unscheduled"). Reconcile the variants (pick the canonical, archive the rest).

**B. Design the folder + naming system** (propose, get my approval via AskUserQuestion,
then move with `mv`). The system must make all six problems impossible to recreate. A strong
default to refine with me: **per-post folders inside per-series folders**, each post folder
holding the draft + its images + a standard frontmatter block, plus a top-level `README.md`
index and an `_ideas/`, `_archive/`, `_assets/`, `_experiments/` split. Make
"which image and tool go with this post" answerable by *looking in the post's own folder*.

**C. Standardize frontmatter** so every post self-declares its place. Propose a schema like:
`series / post_number / title / status (idea|drafting|voice-pass|ready|scheduled|published) /
publish_date / hero_image / ships_with (the plugin/skill/MCP) / pain_point / voice_chain_run
(y/n)`. Backfill it across the existing drafts.

**D. Build the posting queue / calendar.** An ordered, dated list (in the README index) that
answers "what do I post today?" at a glance — sequenced from the 7-post series plan, with the
existing drafts slotted in and the one-off stories placed where they fit. Be honest about
daily cadence: recommend a realistic order and flag which posts are ready vs. need drafting +
a voice-chain pass. (Note: Post 6 "Stop Building Agents" has the loudest hook and cheapest
tool — consider pulling it early.)

**E. Map images per post.** For each post: name the final hero image, mark the superseded
ones, list any in-post images, and flag what still needs generating — then offer to generate
the missing ones with the image skills + the references folder, including my
cheesy-caption-plus-grotesque-image satire format where it fits.

**F. Map tools per post.** Make the `ships_with` field real: which plugin/skill/MCP
accompanies each post (VoicePrint → Post 2; intent-engineering MCP → Post 3; the
Agent-or-Automation Advisor → Post 6; etc.), and note which tools still need building (cross-
reference the opportunity report's build-order list).

## Decisions to get from me (use AskUserQuestion)

- **Folder taxonomy:** per-post folders (everything-for-a-post-together) vs. flat files +
  strong frontmatter + an index. (Recommend per-post folders.)
- **Is "Access Over Meaning" its own series, or folded into Raising Claude?** (Several drafts
  belong to it.)
- **Posting cadence reality:** true daily, or a sustainable 2-3×/week with a daily-looking
  queue? What's the start date?
- **Move now vs. propose-first:** confirm before I mass-move files.

## Definition of done

- A `substack-drafts/README.md` that is the single source of truth: the series list, the
  dated posting queue, the status legend, and the naming/frontmatter conventions.
- Every existing draft classified, variants reconciled, process artifacts and superseded
  images archived, and each live post in a folder with its draft + final image + `ships_with`
  tool.
- I can open the folder and, in ten seconds, know exactly what to post next and what image +
  tool go with it.
- Deferred work (posts still to draft, images still to generate, tools still to build) is in
  `tickets.md`.

Start by reading the opportunity report and the current `substack-drafts/` folder, then come
back to me with the audit table and your proposed structure before moving anything.
