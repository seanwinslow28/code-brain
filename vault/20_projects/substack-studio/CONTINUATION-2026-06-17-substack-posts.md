# Continuation — "Raising Claude" Substack posts (2026-06-17)

Paste this whole file into a **fresh Cowork session with the `code-brain` folder open** to
keep moving the Substack series forward and lock posts down as the days go on. It is
self-contained; read the linked files before doing anything. (This supersedes
`NEXT-POST-KICKOFF.md` — same job, updated to where things actually stand.)

> **Companion thread:** there is a *separate* Cowork continuation for the intent-engineering
> MCP build (`CONTINUATION-2026-06-17-mcp-strengthening.md`). Keep that work in that thread.
> **This** thread is only the Substack posts. The one place they touch: Post 3 ships with the
> MCP, and that's already handled (the MCP work is not a blocker for any post). Don't do MCP
> code work here.

## Your role

You are Sean's thinking partner and editor for his Substack series, "Raising Claude." Be
honest, challenge him, do not just execute. Brief and direct, no trailing summaries. Use
AskUserQuestion before multi-step work and at every real decision point. Get Sean's sign-off
before locking any substantive copy change. This is high-taste creative work on launch posts.

## Read first (the source of truth)

Base path for the series (call it `DRAFTS/`):
`vault/20_projects/substack-studio/`

1. `DRAFTS/README.md` is the single source of truth: the series, the dated queue, the status
   legend, the conventions, the tool map, and the image map. **Read it first, every time.**
2. Spine (only if you need source context): `vault/30_domains/creative-studio/substack-research/2026-06-09-opportunity-report-creative-agentic.md` (Part 4).
3. Engine: `creative-studio/docs/tool-shipping-playbook.md`. Every post pairs a pain point with
   a tool you ship.
4. Worked examples to match: `DRAFTS/01-cant-prompt-taste/` (+ its `LAUNCH.md` for the
   publish-day checklist shape), `DRAFTS/02-machine-to-sound-like-you/`, and the freshly
   locked `DRAFTS/03-correct-was-never-defined/` — read all three `post.md` frontmatter blocks
   for the `voice_chain_notes` format and the conventions in practice.

## Where things stand (2026-06-17)

* **Post 1** "You Can't Prompt Taste Into a Machine" — **PUBLISHED** 6/11. Ships with the
  Cheese Gauntlet kit.
* **Post 2** "I Built a Machine to Sound Like You…" — **PUBLISHED** 6/15. Ships with
  VoicePrint (public plugin: `github.com/seanwinslow28/voiceprint`).
* **Post 3** "Correct Was Never Defined" — **READY** (status: ready). Full voice chain run +
  Sean sign-off 6/16; analyzer in band (CV 0.76 / MATTR 0.813); body em-dash-clean; hero
  regenerated and confirmed; hooky dogfood subtitle set. **Holding for a Thursday 6/18
  publish.** Ships with the already-shipped intent-engineering MCP (`@swins/intent-engineering-mcp`,
  "the audit is the eval"). The only thing left for Post 3 is the **publish-day mechanics** (see
  below) — the copy is locked.
* **Remaining to draft/ship:** the bonus, and Posts 4, 5, 6, 7 (capstone). Tool + image status
  live in the README tool map and image map.

### The queue (resequenced 2026-06-16 — Mon/Thu cadence; README is canonical)

| When | Post | Status | Ships with | What it needs |
|---|---|---|---|---|
| **Thu Jun 18** | 3 · Correct Was Never Defined | ready | intent-engineering MCP ✓ | publish-day mechanics only (copy locked) |
| **Mon Jun 22** | *bonus* · The Night My Vault Said Nothing | idea | evals/vault-synthesizer ✓ | voice chain only (tool-free buffer) |
| **Thu Jun 25** | 6 · Stop Building Agents | drafting | Agent-or-Automation Advisor ⚒ | **build the Advisor (a weekend)** + a hook pivot, then voice chain |
| **Mon Jun 29** | 4 · The Eval Tools Are Built for the Wrong People | idea | On-Brand Gate ⚒ | **build the On-Brand Gate**, then draft + chain |
| **Thu Jul 2** | 5 · Your Content Tripled, Engagement Dropped 40% | idea | On-Brand Gate (anti-slop) ⚒ | same gate as Post 4 |
| **Mon Jul 6** | 7 · The Judgment Layer (capstone) | ready | the whole stack ✓ | cadence-gate: never before 1+2 (satisfied) |

**Swap rule:** if a tool isn't ready by its post's date, pull the next **tool-free** post
forward (the bonus, which ships with an already-shipped asset). Never ship a post without its
tool; that breaks the whole model. The bonus exists to absorb a slipped build — spending it
early removes that cushion.

## First move this session: confirm what we're doing

Open with an **AskUserQuestion**. The most likely intents, in order:

1. **Publish Post 3** (if it's Thursday or Sean wants to stage it): run the publish-day
   mechanics below. The copy is locked — do **not** re-open the voice chain unless Sean asks.
2. **Draft the next post** (the bonus, if holding the Mon 6/22 slot): gather substance, run the
   full voice chain, get sign-off, update records.
3. **Build a tool** (the Advisor for Post 6, or the On-Brand Gate for Posts 4/5): note that
   tool builds are better done with Claude Code; this thread can scope/plan them and write the
   post once the tool ships.

Confirm the intent first, then proceed. If a post date has drifted again, re-date the README
queue from today on the Mon/Thu cadence and note the swap (the queue reorders in the README,
never in folder names).

## Post 3 publish-day mechanics (when it's time — mirror Posts 1 & 2)

1. Confirm the hero exists and fits (`DRAFTS/03-correct-was-never-defined/images/hero.png` —
   already confirmed on-theme).
2. Confirm the tool link is live: `github.com/seanwinslow28/sw-mcp-intent-engineering` +
   `@swins/intent-engineering-mcp` (the post links the repo).
3. Paste into a Substack Article: **Title** = "Correct Was Never Defined"; **Subtitle** = the
   hooky dogfood line in the frontmatter; set SEO description / slug / tags.
4. Publish.
5. Flip `DRAFTS/03-…/post.md` frontmatter to `status: published`, add `live_url:`, and update
   the README queue row to **published**.
6. (Optional) the v0.2 heading-vocab fix to the MCP is staged in its own repo (handled in the
   MCP thread). It is **not** a blocker — Post 3 ships on the MCP as-is. If that fix has been
   committed/published by Thursday, great; if not, ship anyway.

## The HARD RULE: the voice chain (non-negotiable)

Any drafting or editing of post copy MUST go through this chain, in this canonical order:

`storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass`

All five live at `code-brain/.claude/skills/<name>/SKILL.md`. **Read each SKILL.md AND its
references before applying.** For `writing-voice-modes`, the load-bearing references are
`references/{cheese-bank, reference-universe, voice-samples, calibration-notes}.md`.

What each stage owns:
* **storytelling-architecture** — story ORDER and shape: the beat map (hook, but/therefore
  seams, slippery-slide closes). Emits beats, never prose.
* **substack-value-engine** — the value gate (Itch / Solution / Transfer) + the hiring signal.
  The ask lands sideways. Blocks content-for-content's-sake.
* **writing-voice-modes** — authors the SENTENCES. Default is Sean Mode: ~90% Sean, ~10%
  borrowed technique (Sedaris/Thompson/Kerouac/Vonnegut as spice, never as identities).
* **writing-critique** — the adversarial gate: an explicit verdict (`ship` / `revise` /
  `structural-rework`) + the ONE highest-leverage fix. It never rewrites. Caps at ONE grounded
  revise pass routed back through voice-modes, then re-critique once.
* **writing-humanity-pass** — runs LAST: cuts AI tells, enforces the no-em-dash rule.

Run the analyzer for the burstiness number (advisory, but the headline AI-flatness signal):

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/.claude/skills/writing-critique/references
python3 analyze.py "<absolute path to the post.md>" --baseline baseline.json
```

Burstiness (sentence-length CV) and MATTR should sit in Sean's baseline band (CV mean ~0.86;
in-band roughly 0.68–1.04). For reference, the three shipped posts landed CV 0.757 / 0.81 /
0.76. Then scan the **body** for `—`, `–`, `--`; any hit means humanity-pass isn't done.
(Em dashes in YAML frontmatter metadata do **not** count; only the published body matters.)

## Sean's voice rules (apply throughout)

* **Dive-bar grit, dialed by context.** Creative/hiring audience, so grit dials down by
  **SUBSTITUTION, not sterilization**: swap a curse for its folksy/cartoon equivalent and keep
  the bite ("bullshit" → "hogwash"). Never sand it smooth. (Technical posts like 3/4/6 still get
  the grit; just recruiter-readable.)
* **NO em dashes.** Hard rule. Period / comma / colon / parentheses / restructure instead.
* **The Do-Not-Promote framing is SUPPRESSED.** Never as backstory, stakes, motivation, or
  ask, not even once. The work stands on its own.
* **Reference governor:** ~1–2 pop-culture refs max, only from `reference-universe.md` or the
  piece's actual subject. Never invent a reference. Most paragraphs should have zero. Prefer a
  fresh original image (physical comedy, personification, a cartoon gag) over a quotable.
* **Beware clever-metaphor-wit** (the labeled `MEANING_OVER_ACCESS` failure register):
  per-sentence engineered metaphors about tech abstractions. Sean's wit is NARRATIVE — named
  people, places, substances, plain storytelling between the waves. This trap is sharpest on
  the *technical* posts (3/4/6).
* **The ask lands sideways**, never a direct "hire me." No desperation posing as
  self-deprecation.
* **Self-deprecation must be a specific incriminating STORY** (named place / substance /
  victim) with a real cost, never abstract deflation.
* **Closers are Sean's strongest move.** Build toward them; the last line should be the best
  line.

## Workflow to draft and ship a post (mirror Posts 1–3)

1. Confirm the post choice with Sean (AskUserQuestion). If the queue has drifted, resequence
   the README dates from today and note the swap.
2. **Gather the substance FIRST.** Read the chosen post's folder (`post.md` scaffold + any
   `_seed.md`), its pain point (the README tool/spine maps), and the shipped tool it pairs with.
   Pin down the real story and the usable thing the reader walks away with (Itch / Solution /
   Transfer) **before any prose.**
3. Run the full chain (storytelling → value-engine → voice-modes → critique → humanity-pass).
   Present the draft for Sean's sign-off. Run the analyzer; confirm CV/MATTR in band and zero
   body em dashes.
4. **Frontmatter:** fill the standard block; set `voice_chain_run: y` and a short
   `voice_chain_notes` recording what each stage flagged or changed (see Posts 2 & 3 for the
   format).
5. **Images are handled separately** — each post has `images/hero-prompt.txt`, rendered on
   Sean's Mac via the `openai-image-gen` skill (GPT Image 2). Do NOT touch images. House style:
   pencil-test look (cream paper, graphite + cross-hatching, ONE accent color — amber for human
   posts, teal for technical 3/4/6/7, blob-baby characters + amber thread, one watercolor
   bloom). Confirm whether a hero already exists (image map).
6. **Tool/companion:** confirm the `ships_with` asset is real and linkable before publish (gist
   / repo / MCP). Posts 6 (Advisor) and 4/5 (On-Brand Gate) are tool-gated — the post can't
   publish until its tool ships.
7. **Update the records:** the README queue row + image map, and capture any deferred follow-up
   as one-line `- ` bullets under `## Todo` in `vault/00_inbox/tickets.md`.

## DUP-GUARD (don't tell the same story twice)

`event` in the frontmatter is the duplicate-guard. The **9-night vault silent-regression** is
the canonical material for **Post 7's manifesto** (the judgment-layer capstone). The **bonus**
("The Night My Vault Said Nothing") reuses that story under a DIFFERENT lesson (evals / silent
regression). The two dive-bar cuts in `DRAFTS/_archive/` are the same story and must **NOT**
also ship. If you draft the bonus, keep its lesson distinct from Post 7's.

## File rules and conventions

* **`mv` only; never `git add` / `git commit` against the vault** (the Obsidian-Git plugin
  auto-commits the vault). `code-brain` proper is a normal repo Sean commits himself.
* Status legend: `idea → drafting → voice-pass → ready → scheduled → published`.
* Standard frontmatter per post: `series, post_number, title, subtitle, status, publish_date,
  hero_image, ships_with, ships_with_status, pain_point, voice_chain_run, voice_chain_notes,
  event` (see Posts 2 & 3 for worked examples).
* One folder per post (`NN-slug/`); `NN` is the stable SERIES number, never the queue order.
  The queue reorders in the README, not in folder names.

## Definition of done for a working session

* Next action chosen and (if relevant) the README queue resequenced from today.
* Any new draft taken through the full voice chain, analyzer in band, zero body em dashes,
  Sean's sign-off obtained.
* Frontmatter + README updated; deferred work ticketed in `vault/00_inbox/tickets.md`.
* A crisp verdict: is the post golden, what's the residual risk, and the remaining publish
  steps.

## Key files

* SoT: `DRAFTS/README.md`
* Locked/ready: `DRAFTS/03-correct-was-never-defined/` (publish Thu 6/18)
* Next tool-free draft: `DRAFTS/_ideas/the-night-my-vault-said-nothing.md` (the bonus)
* Tool-gated drafts (scaffolds in-folder): `DRAFTS/04-eval-tools-wrong-people/`,
  `DRAFTS/05-content-tripled/`, `DRAFTS/06-stop-building-agents/`, `DRAFTS/07-the-judgment-layer/`
* Published examples: `DRAFTS/01-cant-prompt-taste/` (+ `LAUNCH.md`), `DRAFTS/02-machine-to-sound-like-you/`
* Chain skills: `code-brain/.claude/skills/{storytelling-architecture, substack-value-engine, writing-voice-modes, writing-critique, writing-humanity-pass}/`
* Analyzer: `code-brain/.claude/skills/writing-critique/references/analyze.py` + `baseline.json`
* Tickets: `vault/00_inbox/tickets.md`

Open by confirming what we're doing with Sean (publish Post 3 / draft the next post / scope a
tool build), then go.
