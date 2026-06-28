# Claude Code Run Prompt — 6 Pencil & Prompt discovery runs

Copy everything in the fenced block below into a **Claude Code session opened in `code-brain`** (the council needs `OPENROUTER_API_KEY` from the repo-root `.env` and the canonical CLI; it cannot run inside Cowork). Run it on the Mac.

Slate locked 2026-06-27: hybrid lanes + themes, segment reframed to the AI-curious-but-burned maker (not anti-AI forums). D and E run **deep**; the other four run **standard**. Three runs/day across two days to respect the hard $10/day cap.

---

```
You are running the `fusion-discovery-council` skill to mine fresh, real-URL creative-maker
pain for the Pencil & Prompt Substack. Read the skill first:
.claude/skills/fusion-discovery-council/SKILL.md

GOAL: six --lens substack discovery runs, each a DISTINCT pain cluster, reframed toward
creatives who WANT AI to work for them and got burned (NOT anti-AI / r/BetterOffline doomers).
This deliberately covers ground the existing 2026-06-22 "soulless AI creative output" run did not.

RULES (non-negotiable):
- Run from the CLI working dir: /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council
- --lens substack on every run (writes a ranked idea-ledger + a sibling value-engine brief).
- Output every ledger into: vault/20_projects/substack-studio/research/discovery/
  (NOT the skill's default vault/20_projects/research/ — match the existing substack runs).
- Respect budget. The CLI enforces $10/day on ACTUAL spend. If any run is rejected on budget
  (exit code 2), STOP for the day, report what completed + the running daily total, and tell me
  to resume the remaining runs tomorrow. Do NOT use --force. Do NOT raise any cap.
- Deep runs (D, E): pass --yes (deep tier is pre-authorized for these two; the daily cap still
  applies and will still stop you if needed).
- NEVER git add / git commit the vault. The Obsidian-Git plugin owns vault commits.

Set DATE once at the top of each day's batch:
  DATE=$(date +%F)

=== DAY 1 (run these three, in order) ===

# A · VISUAL / CHARACTER  (standard, segment illustrator) — feeds Take Two #1
uv run python -m council.discovery \
  "illustrators and character artists trying to get AI image generators to match their own drawing style and keep a character consistent across images" \
  --lens substack --tier standard --segment illustrator \
  --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/${DATE}-visual-ai-match-style-character-consistency-substack-idea-ledger.md

# B · WRITING / VOICE  (standard, segment writer) — feeds Take Two #2
uv run python -m council.discovery \
  "writers and authors trying to get AI to write in their own voice instead of generic AI prose" \
  --lens substack --tier standard --segment writer \
  --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/${DATE}-writing-ai-voice-not-generic-prose-substack-idea-ledger.md

# D · LOSING YOUR STYLE TO THE AI AVERAGE  (DEEP, segment creative) — the whitespace thesis
uv run python -m council.discovery \
  "creatives who feel AI flattens their distinctive personal style into a generic average even after feeding it references and examples" \
  --lens substack --tier deep --segment creative --yes \
  --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/${DATE}-losing-your-style-to-ai-average-substack-idea-ledger.md

=== DAY 2 (run these three, in order) ===

# E · SERIES / BRAND CONSISTENCY  (DEEP, segment designer)
uv run python -m council.discovery \
  "designers and creators struggling to keep a character, style, or brand consistent across many AI-generated outputs" \
  --lens substack --tier deep --segment designer --yes \
  --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/${DATE}-series-brand-consistency-ai-substack-idea-ledger.md

# C · ANIMATION / MOTION  (standard, segment animator)
uv run python -m council.discovery \
  "animators using AI video generators getting lifeless motion, wrong timing, and characters that drift between shots" \
  --lens substack --tier standard --segment animator \
  --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/${DATE}-animation-ai-video-motion-timing-drift-substack-idea-ledger.md

# F · AI AS A CREATIVE PARTNER UPSTREAM  (standard, segment creative)
uv run python -m council.discovery \
  "creatives who only use AI for finished output and cannot make it work as a brainstorming, ideation, or storyboarding partner" \
  --lens substack --tier standard --segment creative \
  --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/research/discovery/${DATE}-ai-as-creative-partner-upstream-substack-idea-ledger.md

=== AFTER EACH DAY, REPORT BACK ===
For every run that completed, give me:
  1. The ledger path.
  2. Verified ideas count + dropped/unverified count + the run's actual $ cost.
  3. The running DAILY total $ (so we see the cap headroom).
  4. The full "Blind-spot / Whitespace Map" section pasted verbatim (this is what I use to
     aim the follow-up web search, so do not summarize it).
Then tell me whether the daily cap stopped anything and what remains.
```

---

## What I (Cowork) do once the ledgers land

The vault is mounted here, so after each batch finishes I read the new ledgers directly. Phase 2 is the **web-search "no stone unturned" pass**: I take each run's blind-spot map and run targeted searches to (a) fill the gaps the council flagged and (b) surface fresh first-person maker pain its collectors did not reach. That gets written up as a supplement, then folded with all six ledgers into the ranked Take Two / Fix My Mess / Notes backlog and the discovery-angle map in `SERIES-COMMAND-CENTER.md`.

## The slate at a glance

| Run | Lane / theme | Tier | Segment | Feeds |
|---|---|---|---|---|
| A | Visual / character — match my style, keep a character consistent | standard | illustrator | Take Two #1 |
| B | Writing / voice — write in my voice, not generic AI prose | standard | writer | Take Two #2 |
| C | Animation / motion — lifeless motion, wrong timing, drift | standard | animator | Take Two (motion lane) |
| D | Losing your style to the AI average (the whitespace thesis) | **deep** | creative | manifesto + spine |
| E | Series / brand consistency across many outputs | **deep** | designer | Fix My Mess + design/brand |
| F | AI as a partner upstream (brainstorm / ideate / storyboard) | standard | creative | fresh thesis lane |
