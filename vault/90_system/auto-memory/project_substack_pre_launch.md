---
name: Substack pre-launch — corpus actively growing
description: Sean has no published Substack yet. Voice corpus in voice-samples.md is being actively built via AI-draft → Sean-rewrite cycles. Goal is "give Claude a topic, don't edit the output." Sean wants more iteration, especially on Substack format.
type: project
originSessionId: f17ffb8f-8a62-445b-9540-7646aa2cec13
---
Sean's Substack does not exist yet. He's building the `writing-voice-modes` skill via real corpus iteration before going live. Content focus = AI news, AI tools, AI + creativity, technical AI, PM, AI PM.

**Why:** Sean wants the AI-generated voice to be reliable from day one of public writing. The autoresearch optimization run (2026-05-10, design at `docs/superpowers/specs/2026-05-09-writing-voice-modes-autoresearch-design.md`) hit a corpus-thinness ceiling — see `project_autoresearch_candidate_evaluation.md`. Sean explicitly redirected to corpus-building: "the best way to truly make it better." Pure AI-draft → Sean-rewrite cycles in interactive sessions, then promote validated patterns into SKILL.md.

**Status as of 2026-05-14 (most recent corpus session):**

- Voice corpus expanded substantially. Three new exercise rounds appended to `.claude/skills/writing-voice-modes/references/voice-samples.md` (Rounds 2, 3, 4 — total ~12 new annotated samples spanning Twitter / Substack openers / Substack closers / one full 250-word intro).
- **3 new signature moves promoted from corpus → SKILL.md table** (`## Sean's Signature Moves`):
  - **Reader-Dismissal** (3 syntactic shapes: parenthetical, coda sentence, mid-paragraph self-correction)
  - **Equation / Formula Defamiliarizer** (cultural claim rendered as math/categorical equivalence)
  - **Inverted Refrain** (canonical refrain with cadence preserved but vector flipped — "And so it begins" inverting "So it goes")
- **2 new anti-pattern / mechanic refinements added 2026-05-14:**
  - New row in `## Anti-Patterns` table: **"Desperation Posing as Self-Deprecation"** (naming the ask in prose collapses the move from earned-funny to needy-transactional). Added after a draft I generated landed wrong — Sean: "feels more like desperation than self deprecation."
  - Refined `Domestic Defamiliarizer` mechanic with a "blunt, not precious" guardrail. Added after a draft I generated called Sean's agents "small computer programs" — Sean: "sounds weird. I wouldn't say that."
- **Format-vs-voice insight confirmed.** Sean drafts voice-first as single-paragraph blocks with em-dashes (`—` and `--`) as soft breaks. Format pass converts them to actual paragraphs. **When Claude generates output for Sean, pre-apply paragraph breaks** — don't mimic the draft-naïve single-block format.
- **`--` (double-hyphen) is Sean's deliberate em-dash substitute.** Visual preference. Preserve as drafted; treat as `—` for any density-feature extraction.
- **LinkedIn is not a separate voice mode.** Covered by Sean Mode at 60% dial. Cross-posts derive from Substack drafts dialed down.
- **Two provisional moves to watch for promotion** (1 instance each, not yet ready for SKILL.md): Rhetorical Catechism ("Shocked? Yes. Impressed? You bet. Proud? Definitely.") and Lyric-as-Literal ("I'm shipping up to Boston" deployed as literal action, not analogy).

**Working test loop (validated 2026-05-14):**
1. Sean picks a topic (or chooses from 2-3 starter prompts I offer)
2. Claude generates ~250-word Substack intro using updated `writing-voice-modes` skill in Sean Mode, with paragraph breaks pre-applied
3. Sean does K/T/R evaluation — Keep verbatim / Tweak / Rewrite-or-kill — per line, OR direct prose feedback ("this feels desperate")
4. Iterate until Sean validates ("this lands"), then append to `voice-samples.md` as a new corpus tier (AI-drafted, Sean-validated)
5. Patterns from corrections get promoted into SKILL.md — new signature moves, anti-patterns, or mechanic refinements

**Pending artifact** (awaiting Sean's validation in next session):
A 236-word Substack intro on "Why I'm publishing my agent fleet metrics in public" (the dashboard from `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-agent-fleet-dashboard-spec.md`). First version had two failure modes Sean flagged. Revised version cut both. Sean's last response: "This definitely better" — but no explicit K/T/R, so the corpus append is paused. Pick up by asking whether the revised version lands or needs another iteration.

**How to apply (when Sean returns to writing iteration):**
- Default cadence: similar AI-draft → rewrite rounds, focused on Substack format. Sean wants "more iteration, especially on Substack posts."
- Resume by asking either (a) "want to validate the agent-fleet draft from last session, or pick a fresh topic?" or (b) offer 3 topic starters spanning Sean's content lanes (AI tools, AI + creativity, PM/AI PM).
- DO NOT assume Sean has prior Substack posts to pull from. Test prompts should bias toward his actual content lanes; avoid random topics outside what he'd publish.
- The corpus IS the calibration anchor — read `voice-samples.md` (esp. Rounds 2-4) before drafting in Sean's voice.
