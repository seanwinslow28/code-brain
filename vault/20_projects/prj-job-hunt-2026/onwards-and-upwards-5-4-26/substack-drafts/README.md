# Substack — Raising Claude (command center)

Single source of truth for the series. **One series: Raising Claude, 7 posts + a bonus.**
Spine = the opportunity report (`vault/30_domains/creative-studio/substack-research/2026-06-09-opportunity-report-creative-agentic.md`, Part 4).
Engine = `creative-studio/docs/tool-shipping-playbook.md` (every post pairs a pain point with a tool you ship).

Cadence: **2–3×/week (Mon/Thu)**. Honest constraint: cadence is gated by **tool-build time**, not
writing time — 3 of the 7 posts ship with a tool that isn't built yet.

---

## 📅 THE QUEUE — what do I post next?

| When | Post | Folder | Status | Ships with | Blocker |
|---|---|---|---|---|---|
| **Jun 5** ✓ | 1 · You Can't Prompt Taste Into a Machine | `01-cant-prompt-taste/` | **published** | Cheese Gauntlet kit ✓ | — |
| **Thu Jun 11** | 2 · I Built a Machine to Sound Like You | `02-machine-to-sound-like-you/` | voice-pass | VoicePrint ✓ | run voice chain + hero image |
| **Mon Jun 15** | 6 · Stop Building Agents | `06-stop-building-agents/` | drafting | Agent-or-Automation Advisor ⚒ | **build Advisor (a weekend)** + hook pivot |
| **Thu Jun 18** | *bonus* · The Night My Vault Said Nothing | `_ideas/` | idea | evals/vault-synthesizer ✓ | voice chain only (tool-free buffer) |
| **Mon Jun 22** | 3 · Correct Was Never Defined | `03-correct-was-never-defined/` | idea | intent-engineering MCP ✓ / Intent Card ⚒ | draft (MCP already shipped) |
| **Thu Jun 25** | 4 · The Eval Tools Are Built for the Wrong People | `04-eval-tools-wrong-people/` | idea | On-Brand Gate ⚒ | **build On-Brand Gate** |
| **Mon Jun 29** | 5 · Your Content Tripled, Engagement Dropped 40% | `05-content-tripled/` | idea | On-Brand Gate (anti-slop) ⚒ | same gate as Post 4 |
| **Thu Jul 2** | 7 · The Judgment Layer (capstone) | `07-the-judgment-layer/` | ready | the whole stack ✓ | cadence-gate: never before 1+2 |

**Swap rule:** if a tool isn't ready by its post's date, pull the next **tool-free** post forward
(the bonus evals post, or Post 3 — both ship with already-shipped assets). Never ship a post
without its tool; that breaks the whole model. The bonus exists to absorb a slipped build.

**This week's real work:** Post 2 voice chain + hero image (by Thu) → build the Advisor over the
weekend so Post 6 holds Jun 15.

---

## Status legend

`idea` → `drafting` → `voice-pass` (chain not yet run) → `ready` → `scheduled` → `published`

Every post **must** clear the voice chain before publish: **writing-voice-modes → writing-critique → writing-humanity-pass**.
Voice rules: dive-bar grit dialed by context · no em dashes · layoff suppressed · ≤2 pop-culture refs from the real reference universe · the ask lands sideways.

Tool icons: ✓ shipped · ⚒ to-build.

---

## The 7 posts (the spine)

| # | Title | Pain (their words) | Ships with | Tool status |
|---|---|---|---|---|
| 1 | You Can't Prompt Taste Into a Machine | "humanize prompts don't work" | Cheese Gauntlet kit | shipped |
| 2 | I Built a Machine to Sound Like You | "it's obvious, we know" / fraud guilt | VoicePrint | shipped |
| 3 | Correct Was Never Defined | "the missing layer is structured intent" | Intent Card / intent-engineering MCP | MCP shipped; Card to build |
| 4 | The Eval Tools Are Built for the Wrong People | "designed for ML engineers" | On-Brand Gate | to build |
| 5 | Your Content Tripled, Engagement Dropped 40% | "AI slop, the arms race is losing" | the anti-slop gate | to build (= Post 4's tool) |
| 6 | Stop Building Agents | "automations, not agents" (1,556 upvotes) | Agent-or-Automation Advisor | to build (cheap; loudest hook) |
| 7 | The Judgment Layer | brand stewardship worth more as output floods | the whole stack; ties to "Access Over Meaning" | shipped |
| — | *bonus:* The Night My Vault Said Nothing | "evals are the new PRDs / silent regression" | evals/vault-synthesizer repo | shipped (tool-free buffer) |

---

## 🖼️ Image map

Hero lives at each post's `images/hero.png`; superseded/test versions sit in `images/_superseded/`.

| Post | Hero | Superseded held | Still needed |
|---|---|---|---|
| 1 | — | — | **GENERATE** (no hero was ever tracked for the live post) |
| 2 | — | — | **GENERATE** (by Thu Jun 11) |
| 3 | `hero.png` ✓ (intent-eng header) | v1 | optional refresh |
| 4 | — | — | **GENERATE** |
| 5 | — | — | **GENERATE** |
| 6 | — | — | **GENERATE** |
| 7 | `hero.png` ✓ (meaning-over-access) | chatgpt, openai-test | — (plus the access-meaning chart embed at publish) |
| bonus | `hero.png` ✓ | v1, chatgpt, openai-test | — |

**Missing heroes: Posts 1, 2, 4, 5, 6.** Generate via `gemini-image-gen` /
`gemini-pencil-animation-image-gen` (the load-bearing hand-drawn character) using the refs in
`_assets/references/`. The repeatable house style: **cheesy caption + grotesquely-detailed image
as overt satire** (from the cheese-bank). Post 2 is the priority (ships Thu).

---

## 🔧 Tool map (ships_with)

| Tool | For post | Status | Notes |
|---|---|---|---|
| Cheese Gauntlet kit | 1 | shipped | `01-…/ships-with-cheese-gauntlet-kit-PUBLIC.md` (published) + `…-kit.md` (source) |
| VoicePrint | 2 | shipped | Cowork plugin; dogfood done (Priya, 0.57 burstiness) |
| intent-engineering MCP | 3 | shipped | `@swins/intent-engineering-mcp` — "the audit is the eval" |
| Intent Card | 3 | **to build** | brief-mode tools `audit_brief`/`scaffold_brief`/`assess_brief_readiness` (report §2A) |
| On-Brand Gate | 4 + 5 | **to build** | generalize writing-critique → pass/fail + violated clauses + slop-risk (report §2B) |
| Agent-or-Automation Advisor | 6 | **to build** | cheapest tool, a weekend; loudest hook (report §1 #3) |
| the whole stack | 7 | shipped | capstone ties everything to "Access Over Meaning" |

**Build order (report §"What to do next"):** Advisor (Post 6) → Intent Card (Post 3) → On-Brand Gate (Posts 4/5).

---

## Folder & naming conventions

```
NN-slug/                    one folder per post; NN = SERIES number (stable, not queue order)
  post.md                   the draft (or scaffold). Carries the standard frontmatter block.
  _seed.md                  salvaged raw material (Post 3 only, so far)
  ships-with-*.md           the tool/companion that ships with the post
  images/hero.png           the final hero
  images/_superseded/       old/test image versions, never deleted, never confused for final
_ideas/        unscheduled posts + future seeds (the bonus evals post lives here)
_archive/      superseded variants + retired cuts (workshop history; do not publish)
_experiments/  process artifacts (council sessions, beatmaps, voice-calibration)
_assets/references/   headshot + image-gen style refs
```

The **queue reorders in this README**, not in folder names — so resequencing never renames a folder.

### Standard frontmatter (every `post.md`)

```yaml
series: raising-claude
post_number: 1            # or "bonus"
title: "..."
status: idea | drafting | voice-pass | ready | scheduled | published
publish_date: 2026-06-05  # or TBD
hero_image: images/hero.png        # or "MISSING — needs generation"
ships_with: cheese-gauntlet-kit
ships_with_status: shipped | to-build
pain_point: "in the audience's own words"
voice_chain_run: y | n
event: voice-calibration  # which real story it draws from (the duplicate-guard)
```

`event` is the **dup-guard**: the 9-night vault regression is the canonical material for Post 7
(manifesto framing). The bonus evals post reuses it under a *different lesson*; the two dive-bar
cuts in `_archive/` are the same story and must **not** also ship.

---

## Reconciliation notes (what changed 2026-06-09)

- One war story (9-night silent regression) was told 3 ways across 5 files → manifesto wins Post 7,
  evals cut survives as the bonus, two dive-bar cuts retired to `_archive/`.
- `the-confident-stranger` = an alt full-intensity cut of the shipped Post 1 → `_archive/`.
- `ldr-grounding-collapse` (was labeled "Post 1") = a distinct event → re-slotted as Post 6 draft.
- `intent-engineering-mcp.md` (empty project stub) → `03-…/_seed.md`, salvaged for its origin paragraph.
- Two empty legacy dirs (`images/ archive/ experiments/ substack-image-generation-references/`)
  couldn't be deleted from this session — they're empty, git won't commit them; delete in Finder when convenient.
