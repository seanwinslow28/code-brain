# Writing Humanity Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone `writing-humanity-pass` skill that strips the 30 documented "Signs of AI writing" and rebuilds human texture with Sean's voice as the authority, and de-dash `writing-voice-modes` end-to-end so the two skills stop contradicting each other.

**Architecture:** A new companion skill that auto-detects voice-bearing vs neutral text and scrubs accordingly. Its "do-not-flag" allowlist IS `writing-voice-modes`' 13 signature moves. Em dashes become a hard cut in both registers, which forces a reconciliation sweep across `writing-voice-modes` (instructions, examples, calibration anchors).

**Tech Stack:** Markdown SKILL.md authoring (YAML frontmatter + progressive-disclosure references). Verification via `python3 scripts/validate.py` (structural) + `grep -E` gates (no em dashes) + manual review against `evals.yaml` cases. No application code.

**Source material:** Adapted from `blader/humanizer` (MIT, v2.7.0), based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). The full 30-pattern content is embedded in Task 2 below, so no external clone is needed at execution time.

**Spec:** [.claude/skills/writing-voice-modes/drafts/2026-06-02-writing-humanity-pass-design.md](../../../.claude/skills/writing-voice-modes/drafts/2026-06-02-writing-humanity-pass-design.md)

**Em-dash discipline (applies to THIS plan too):** The only files that may contain `—` or `–` after this work are: (a) the `writing-humanity-pass` lines that *name* those characters as scrub targets (SKILL.md em-dash rule + final-output guard; `ai-tells.md` #14 watch line), and (b) intentional "before" specimens inside `evals.yaml` / `evals.sealed.yaml`. Every other line, in both skills, must be dash-free. The grep gates below enforce this.

**Commit/branch note:** This repo's norm is to commit only on a feature branch, never directly to `main`. Task 0 creates the branch. Each task ends with a commit. The vault (`vault/`) is owned by Obsidian-Git, so this plan touches none of it except one allowed `tickets.md` append (Task 11), which is left unstaged.

---

## File Structure

**Create:**
- `.claude/skills/writing-humanity-pass/SKILL.md` — the pass: register branch, scrub loop, em-dash rule, integration, triggers, attribution. Lean (verbatim-loaded by agents).
- `.claude/skills/writing-humanity-pass/references/ai-tells.md` — all 30 patterns, adapted + tagged `[SLOP]` / `[CLASH->move]`.
- `.claude/skills/writing-humanity-pass/references/voice-safe-exceptions.md` — crosswalk: each `[CLASH]` tell to its colliding signature move and resolution.
- `.claude/skills/writing-humanity-pass/evals.yaml` — before/after editing cases.
- `.claude/skills/writing-humanity-pass/evals.sealed.yaml` — held-out cases.

**Modify:**
- `.claude/skills/writing-voice-modes/SKILL.md` — de-dash instructions and all examples/tables/frontmatter (36 em-dash instances).
- `.claude/skills/writing-voice-modes/references/voice-samples.md` — punctuation-only de-dash (76 instances) + header note.
- `CHANGELOG.md` — `[Unreleased] -> ### Added` entry.
- `README.md` — skill count 119 -> 120 (lines ~5, ~93, ~95).

---

## Task 0: Create feature branch

**Files:** none (git only)

- [ ] **Step 1: Branch off main**

```bash
git checkout main
git checkout -b skill/writing-humanity-pass
git status
```
Expected: `On branch skill/writing-humanity-pass`, working tree shows only the pre-existing untracked vault files (leave those alone).

---

## Task 1: Create the new skill's SKILL.md

**Files:**
- Create: `.claude/skills/writing-humanity-pass/SKILL.md`

- [ ] **Step 1: Write the SKILL.md with this exact content**

````markdown
---
name: writing-humanity-pass
description: Remove the documented "Signs of AI writing" from a draft and rebuild human texture, calibrated to Sean's voice. Auto-detects voice-bearing vs neutral text and scrubs accordingly. Cuts em dashes, significance inflation, -ing padding, copula avoidance, chatbot artifacts, filler, hedging, and 24 more tells. Pairs with writing-voice-modes (runs as the final pass after a voice write) and runs standalone. Use when asked to "scrub the AI out of this", "make this less AI", "de-slop this draft", "humanize this", "this sounds like AI", "remove AI tells", or when reviewing any draft (yours or agent-generated) that reads like a machine.
---

# Writing Humanity Pass

## Purpose

Remove the 30 documented "Signs of AI writing" from a draft and rebuild human texture, calibrated to Sean Winslow's voice. This is an editing pass, not a composition skill. It pairs with `writing-voice-modes` (runs as the final pass after a voice write) and runs standalone for cleaning agent-generated or foreign drafts.

The core rule: Sean's voice is the authority. A pattern is only a tell when it is NOT one of his 13 signature moves. The "do-not-flag" allowlist IS the signature-move list in `writing-voice-modes`.

## When to Use

- "Scrub the AI out of this", "make this less AI", "de-slop", "humanize this", "this reads like AI", "remove AI tells"
- As the final editing pass after composing in `writing-voice-modes`
- Cleaning agent-generated drafts (substack-drafter, vault agents) before publishing
- Cleaning neutral docs, specs, or reference notes that read like a machine

## How It Works: Detect Register, Then Scrub

### Step 1. Classify the text

- Voice-bearing (essay, blog, newsletter, LinkedIn, social, post-mortem, personal writing): VOICE-SAFE SCRUB.
- Neutral (docs, specs, runbooks, PRDs, reference notes, API docs, agent-generated reference output): FULL SCRUB.

Classification signals, in priority order:
1. Explicit user cue ("this is a blog post" / "this is a runbook" / "neutral scrub").
2. File path / content type (essays and substack drafts route to voice; `docs/`, `*.spec.md`, runbooks, READMEs route to neutral).
3. Internal signal: first-person + narrative + sensory detail routes to voice; third-person + procedural + reference routes to neutral.
4. Ambiguous routes to VOICE-SAFE (the safer failure: it preserves more, scrubs less).

### Step 2. The scrub loop (both registers)

1. Draft rewrite. Apply `references/ai-tells.md` for the chosen register. Cover everything the original covered (N paragraphs in, N paragraphs out). Preserve meaning.
2. Audit. Ask explicitly: "What makes this still read as AI-generated?" Answer in brief bullets (remaining tells, too-tidy rhythm, slogan-y closer).
3. Final rewrite. Fix the audit bullets. Scan the result for `—`, `–`, and ` -- `; any hit means it is not done.

### Step 3. Deliver

- Interactive: draft, then brief "still-AI" bullets, then final rewrite, then a short change summary.
- Headless / agent chain (e.g. substack-drafter): return final clean text plus a one-line change summary in a trailing HTML comment. No interactive audit prompt (nobody can answer it in a launchd run). Detect non-interactive context and switch to this mode.

## VOICE-SAFE vs FULL: The Difference

VOICE-SAFE. Cut the `[SLOP]` tells; DEFER to Sean's 13 signature moves (see `references/voice-safe-exceptions.md`). Never flatten a deliberate move into "clean" prose. Match Sean's codified voice from `writing-voice-modes` references instead of producing generic clean output. No sample-pasting needed; his calibration is already codified.

FULL. Plain, neutral register IS the correct human voice here. Cut everything in `references/ai-tells.md`. Add NO personality and NO first person. (This mirrors humanizer's own gating: encyclopedic, technical, or reference text wants neutral-and-plain, not injected voice.)

## The Em-Dash Hard Rule (Both Registers)

No em dashes (`—`), en dashes (`–`), spaced ` — `, or double-hyphen ` -- ` in the final output. This is a hard constraint, not a "use sparingly" preference. The em dash is the single most reliable AI tell, and Sean has chosen to retire it from his voice entirely. Replace each, in order of preference: period (new sentence), then comma (tight aside), then colon (introducing an explanation), then parentheses (a true aside), then restructure.

Kerouac survives without it: polysyndeton, the jewel center, sensory cascading, and the dual narrator all stay. Commas and periods carry the breath-mark rhythm that the dash used to. The only retired mechanic is "em dashes as breath marks."

Final-output guard: scan the result for `—` and `–`. Any hit means the rewrite is not finished.

## What NOT to Flag (Don't Gut Real Prose)

A clean human writer can hit several patterns without any AI involvement. These are NOT reliable tells on their own:
- Perfect grammar and consistent style (polish is not AI).
- Mixed casual and formal registers (often a technical person, a young writer, or neurodivergent prose).
- "Bland" prose without the specific tells (generic dryness is just dry writing).
- Formal or academic vocabulary that is not the specific AI-vocabulary words in #7.
- Common transition words in isolation (one "however" is not a tell).
- Curly quotes alone (most editors auto-curl).
- Unsourced claims (most of the web is unsourced).

Look for clusters of tells, not isolated ones. A single em dash is nothing; em dashes plus rule-of-three plus "vibrant tapestry" plus a "Conclusion" section is a confession.

## Signs of Human Writing (Preserve These)

When you see these, lean toward leaving the prose alone. Over-editing destroys what makes it human. For Sean specifically, these map onto his signature moves and `calibration-notes.md`:
- Hyper-specific, hard-to-fabricate detail (a named place, a named substance, "the lawyer upstairs from my dentist").
- Mixed feelings and unresolved tension.
- Dated, era-bound references (slang, memes, music).
- Variety in sentence length (short staccato hits between flowing lines).
- Genuine asides, parentheticals, and self-corrections (his Reader-Dismissal move).
- His Rule-of-Three-plus-pivot, Hard-Cut deflation, sensory-before-numbers, and pop-culture anchoring, all deliberate (see `references/voice-safe-exceptions.md`).

## Integration

This skill runs AFTER composition. `writing-voice-modes` composes; this scrubs.

- Chaining order (recommended): compose with `writing-voice-modes` (plus `creative-writing` for format, `technical-writing` for clarity), then run `writing-humanity-pass` LAST.
- It never overrides a format constraint (`creative-writing`) or a signature move (`writing-voice-modes`).
- For neutral text it agrees with `technical-writing` (plain, front-loaded, no slop).

## References

- `references/ai-tells.md`: all 30 patterns, adapted to Sean's output, each tagged `[SLOP]` (always cut) or `[CLASH->move]` (defer in voice-safe).
- `references/voice-safe-exceptions.md`: the crosswalk. Each `[CLASH]` tell maps to the signature move it collides with and how voice-safe resolves it.

Adapted from [`blader/humanizer`](https://github.com/blader/humanizer) (MIT, v2.7.0), itself based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup). MIT permits adaptation; attribution retained.

## Success Criteria

- [ ] Output contains zero em/en dashes (both registers).
- [ ] Voice-safe scrub preserves every signature move; neutral scrub strips to plain register.
- [ ] Meaning preserved; paragraph count matches the original.
- [ ] No tell from `ai-tells.md` survives that is not a protected Sean move.
- [ ] Real human prose (no clusters of tells) is left largely alone, not gutted.

## Copy/Paste Ready

```
"Scrub the AI out of this"
"Make this less AI"
"De-slop this draft"
"Humanize this, it's a blog post"
"Neutral scrub this runbook"
"Run the humanity pass after writing it in my voice"
```
````

- [ ] **Step 2: Verify frontmatter name matches directory**

Run: `head -3 .claude/skills/writing-humanity-pass/SKILL.md`
Expected: `name: writing-humanity-pass` (must equal the directory name, or `validate.py` warns).

- [ ] **Step 3: Verify only the intentional em-dash-naming lines exist**

Run: `grep -nE '—|–' .claude/skills/writing-humanity-pass/SKILL.md`
Expected: exactly two lines, both in "The Em-Dash Hard Rule" section: the "No em dashes (`—`), en dashes (`–`)..." line and the "scan the result for `—` and `–`" guard line. No other hits. If any other line appears, it is a prose dash; fix it and re-run.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/writing-humanity-pass/SKILL.md
git commit -m "feat(skill): add writing-humanity-pass SKILL.md"
```

---

## Task 2: Create references/ai-tells.md (all 30 patterns, tagged)

**Files:**
- Create: `.claude/skills/writing-humanity-pass/references/ai-tells.md`

- [ ] **Step 1: Write the file with this exact content**

(Note: the ONLY line in this file that may contain `—`/`–` is the #14 "Watch" line, which names the characters as targets. Every other line uses periods, colons, or commas.)

````markdown
# AI Tells: Adapted Pattern Catalog (Sean-calibrated)

The 30 documented "Signs of AI writing," adapted from `blader/humanizer` (MIT, v2.7.0) and Wikipedia "Signs of AI writing." Upstream numbering kept for re-sync.

Tag legend:
- `[SLOP]`: always cut, both registers. Pure machine residue.
- `[CLASH->X]`: collides with Sean's signature move X. In VOICE-SAFE, defer to the move (see `voice-safe-exceptions.md`). In FULL (neutral) scrub, cut it.

---

## Content patterns

**#1. Significance / legacy / broader-trend inflation** `[CLASH->Hard Cut/Deflation]`
Watch: stands/serves as, is a testament/reminder, pivotal moment, underscores its importance, reflects broader, marking a shift, evolving landscape, indelible mark.
Cut: puffed-up "this represents a broader movement" framing. Voice-safe: KEEP the epic build only when it lands on a mundane or absurd deflation in the final clause; cut it when it inflates and never deflates.
Ex: "marking a pivotal moment in the evolution of regional statistics" becomes "established in 1989 to publish regional statistics."

**#2. Notability / media-coverage name-dropping** `[SLOP]`
Watch: cited in [outlet list], active social media presence, written by a leading expert.
Cut: source lists without context. Ex: "cited in NYT, BBC, FT, and The Hindu" becomes "In a 2024 NYT interview, she argued X."

**#3. Superficial -ing analyses** `[SLOP]`
Watch: highlighting..., ensuring..., reflecting/symbolizing..., contributing to..., showcasing...
Cut: present-participle tails that fake depth. Ex: "...resonates with the region, symbolizing X, reflecting Y" becomes a plain fact with a source.

**#4. Promotional / advertisement language** `[SLOP]`
Watch: boasts a, vibrant, rich (figurative), nestled, in the heart of, breathtaking, must-visit, renowned, stunning.
Cut: brochure tone. Ex: "Nestled within the breathtaking region, stands as a vibrant town" becomes "is a town in the X region, known for its weekly market."

**#5. Vague attributions / weasel words** `[SLOP]`
Watch: Industry reports, Observers have cited, Experts argue, Some critics argue, several sources (when few cited).
Cut: opinions pinned to vague authorities. Ex: "Experts believe it plays a crucial role" becomes "supports endemic fish species, per a 2019 survey by X."

**#6. Formulaic "Challenges and Future Prospects" sections** `[SLOP]`
Watch: Despite its, faces several challenges, Despite these challenges, Future Outlook, Challenges and Legacy.
Cut: the boilerplate section. Replace with specific facts.

## Language and grammar patterns

**#7. Overused "AI vocabulary"** `[SLOP]`
Watch: actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (v), interplay, intricate, key (adj), landscape (abstract), pivotal, showcase, tapestry, testament, underscore (v), valuable, vibrant.
Cut: especially when these co-occur. Replace with plain words ("also", "remain common").

**#8. Copula avoidance** `[SLOP]`
Watch: serves as / stands as / marks / represents [a], boasts / features / offers [a].
Cut: restore is/are/has. Ex: "Gallery 825 serves as LAAA's exhibition space and boasts 3,000 sq ft" becomes "Gallery 825 is LAAA's exhibition space and has 3,000 sq ft."

**#9. Negative parallelisms / tailing negations** `[SLOP]`
Watch: "Not only...but...", "It's not just X, it's Y", clipped tails like "no guessing", "no wasted motion".
Cut: state the point directly. Sean does NOT use these; confirm in eval. Ex: "It's not just a song, it's a statement" becomes "The beat sets the aggressive tone."

**#10. Rule of three overuse** `[CLASH->Rule of Three + Emotional Pivot]`
Watch: forced triples ("innovation, inspiration, and insights").
Cut: decorative triples. Voice-safe: KEEP when items 1 and 2 are concrete or light and item 3 pivots to genuine feeling ("skills, coffee, and for once in my life, a glimmer of hope"). The pivot is the point.

**#11. Elegant variation (synonym cycling)** `[SLOP]`
Watch: protagonist, then main character, then central figure, then hero, all for one subject.
Cut: repeat the clearest noun. Ex: collapse the cycle to "the protagonist eventually triumphs and returns home."

**#12. False ranges** `[CLASH->metaphor stacking]`
Watch: "from X to Y" where X and Y are not a real scale.
Cut: non-scale ranges become a plain list. Voice-safe: KEEP escalating metaphor stacks that describe the SAME thing (ship of the damned, then sheep, then hamster wheel); those are not false ranges.

**#13. Passive voice / subjectless fragments** `[SLOP]`
Watch: "No configuration file needed", "The results are preserved automatically".
Cut: name the actor when active voice is clearer. Ex: "No configuration file needed" becomes "You don't need a configuration file."

## Style patterns

**#14. Em / en dashes** `[SLOP]` (HARD CUT, see SKILL.md)
Watch: `—`, `–`, spaced ` — `, double-hyphen ` -- `.
Cut: ALL of them, both registers. Replace in order: period, comma, colon, parentheses, restructure. Final-output guard: grep for the characters; any hit means not done.

**#15. Boldface overuse** `[SLOP]`
Cut: mechanical phrase-bolding. Ex: "**OKRs**, **KPIs**, **BMC**" becomes "OKRs, KPIs, BMC."

**#16. Inline-header vertical lists** `[SLOP]`
Watch: "- **Performance:** Performance improved..."
Cut: convert to prose. Ex: three bolded-header bullets become one sentence covering all three.

**#17. Title Case in headings** `[SLOP]`
Cut: "## Strategic Negotiations And Partnerships" becomes "## Strategic negotiations and partnerships" (sentence case).

**#18. Emojis** `[SLOP]`
Cut: decorative emojis on headings or bullets. Ex: a rocket-emoji "Launch Phase:" header becomes "The product launches in Q3."

**#19. Curly quotation marks** `[SLOP]` (low confidence alone)
Cut: convert curly quotes to straight quotes only when stacked with other tells (auto-curl is common and innocent on its own).

## Communication patterns

**#20. Collaborative / chatbot artifacts** `[SLOP]`
Watch: I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...
Cut: entirely. Ex: "Here is an overview... I hope this helps!" becomes the content, starting directly.

**#21. Cutoff disclaimers / speculative gap-fill** `[SLOP]`
Watch: as of [date], while specific details are limited, based on available information, maintains a low profile, keeps personal details private, likely [grew up/studied], it is believed that.
Cut: say what isn't known, or cut the sentence. Don't dress a guess as fact.

**#22. Sycophantic / servile tone** `[SLOP]`
Watch: Great question!, You're absolutely right!, That's an excellent point.
Cut: respond directly. Ex: "Great question! You're absolutely right that..." becomes "The economic factors you mentioned are relevant."

## Filler and hedging

**#23. Filler phrases** `[SLOP]`
Cut: "in order to" becomes "to"; "due to the fact that" becomes "because"; "at this point in time" becomes "now"; "has the ability to" becomes "can"; "it is important to note that the data shows" becomes "the data shows."

**#24. Excessive hedging** `[SLOP]`
Watch: could potentially possibly, might have some effect.
Cut: "It could potentially possibly be argued that the policy might have some effect" becomes "The policy may affect outcomes."

**#25. Generic positive conclusions** `[CLASH->Callback Closer]`
Watch: the future looks bright, exciting times lie ahead, a step in the right direction.
Cut: the vague-upbeat shape. Voice-safe: the closer is Sean's strongest move, so defer the closer SLOT to the Callback Closer (it must transform the opening image). Never let any closer default to this vague-upbeat shape.

**#26. Hyphenated word-pair overuse** `[SLOP]`
Watch: third-party, cross-functional, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end.
Cut: keep the hyphen in attributive position ("a high-quality report"); drop it in predicate position ("the report is high quality").

**#27. Persuasive-authority tropes** `[SLOP]`
Watch: the real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter.
Cut: drop the ceremony, state the point. Ex: "At its core, what really matters is organizational readiness" becomes "That mostly depends on whether the org will change its habits."

**#28. Signposting / announcements** `[SLOP]`
Watch: Let's dive in, let's explore, let's break this down, here's what you need to know, without further ado.
Cut: do the thing instead of announcing it. Ex: "Let's dive into how caching works." becomes "Next.js caches data at multiple layers: ..."

**#29. Fragmented headers** `[SLOP]`
Watch: a heading followed by a one-line paragraph that restates the heading.
Cut: delete the warm-up line; let the heading do its work.

**#30. Diff-anchored writing** `[SLOP]`
Watch: docs or comments narrating a change ("This was added to replace...") in a non-version-scoped doc.
Cut: describe the thing as it is. Ex: "This function was added to replace the old O(n^2) loop" becomes "This function uses a hash map for O(1) lookups."

---

## Detection guidance

See SKILL.md "What NOT to Flag" and "Signs of Human Writing." Rule of thumb: rewrite on clusters of tells, never on a single isolated one. When the text is Sean's voice, the signature moves in `voice-safe-exceptions.md` are protected.
````

- [ ] **Step 2: Verify the file lists all 30 patterns**

Run: `grep -c '^\*\*#' .claude/skills/writing-humanity-pass/references/ai-tells.md`
Expected: `30`

- [ ] **Step 3: Verify only #14's watch line contains the dash characters**

Run: `grep -nE '—|–' .claude/skills/writing-humanity-pass/references/ai-tells.md`
Expected: exactly one line, the `#14` "Watch:" line. No others.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/writing-humanity-pass/references/ai-tells.md
git commit -m "feat(skill): add ai-tells.md (30 patterns, Sean-tagged)"
```

---

## Task 3: Create references/voice-safe-exceptions.md (the crosswalk)

**Files:**
- Create: `.claude/skills/writing-humanity-pass/references/voice-safe-exceptions.md`

- [ ] **Step 1: Write the file with this exact content**

(This file contains NO em/en dash characters. Ranges use a plain hyphen.)

````markdown
# Voice-Safe Exceptions: Tell to Signature-Move Crosswalk

In VOICE-SAFE scrub, these `[CLASH]` tells from `ai-tells.md` collide with a deliberate Sean signature move (from `writing-voice-modes`). DEFER to the move and cite it. In FULL (neutral) scrub, there is no voice, so cut them normally.

| AI tell (ai-tells.md #) | Sean's move it collides with | Voice-safe resolution |
|---|---|---|
| #1 Significance inflation | Hard Cut / Deflation | Keep the epic build ONLY when it lands on a mundane or absurd deflation in the final clause. Cut it when it inflates and never deflates. |
| #10 Rule of three | Rule of Three + Emotional Pivot | Keep when items 1 and 2 are concrete or light and item 3 pivots to genuine feeling. Cut decorative triples that don't pivot. |
| #12 False ranges | Metaphor stacking (calibration-notes) | Cut literal "from X to Y" non-scales. Keep escalating metaphor stacks that describe the SAME mundane reality. |
| #25 Generic conclusion | Callback Closer | The closer is Sean's strongest move, so defer the closer slot to voice-safe. Never let it collapse into "the future looks bright"; it must transform the opening image. |

## Always-protected moves (never flagged in voice-safe)

These are NOT tells for Sean even though a naive humanizer might cut them:
- Polysyndeton (Beat Flow's stacked "and...and...and"). The drumbeat is deliberate. Flag ONLY if it runs a whole piece with zero rhythmic variation (the "Bad Kerouac" anti-pattern).
- Sensory cascade, Pop-Culture Anchoring, and Hyper-Specific Anecdote. Protected. The only cap is "one strong reference earns it; three is self-indulgence" (calibration-notes). Flag a third repeat of the SAME image, not the technique.
- Sensory Before Numbers. The sensory build before an exact figure is the move, not padding.
- Reader-Dismissal parentheticals and self-corrections. These are a human signal, not a chatbot artifact.
- Self-Deprecation as Structure. Protected, UNLESS it slides into self-pity or names a direct ask ("hire me"). That is the "Desperation Posing as Self-Deprecation" anti-pattern; flag that.

## The retired move

"Em dashes as breath marks" (formerly Kerouac's "Dash rhythm") is RETIRED. Em and en dashes are `[SLOP]` in both registers (see SKILL.md). Commas and periods carry the rhythm now. Everything else in Kerouac stays.
````

- [ ] **Step 2: Verify the file is fully dash-free**

Run: `grep -nE '—|–' .claude/skills/writing-humanity-pass/references/voice-safe-exceptions.md`
Expected: **no output.** (This file names the retired move in words, not characters, so it must be completely clean.)

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/writing-humanity-pass/references/voice-safe-exceptions.md
git commit -m "feat(skill): add voice-safe-exceptions crosswalk"
```

---

## Task 4: Create evals.yaml + evals.sealed.yaml

**Files:**
- Create: `.claude/skills/writing-humanity-pass/evals.yaml`
- Create: `.claude/skills/writing-humanity-pass/evals.sealed.yaml`

Note: these are an editing skill's before/after cases (input draft, expected scrub behavior), not the generation-loop schema used by `writing-voice-modes`/skill_optimizer. They are for manual review now; wiring an editing-mode adapter into skill_optimizer is out of scope. The `input` fields intentionally contain em dashes (they are the "before" specimens to scrub); that is the only reason these files appear in a recursive dash grep.

- [ ] **Step 1: Write evals.yaml with this exact content**

```yaml
# Eval suite for writing-humanity-pass. Before/after editing cases.
# Manual-review schema (not wired to skill_optimizer; that adapter is out of scope).
# NOTE: `input` fields contain em dashes on purpose; they are the specimens to scrub.
schema_version: 1

cases:
  - id: voice_dashes_removed
    register: voice
    input: "An agent rebuilt the entire pipeline in fourteen minutes — I sat there with my coffee getting cold and my ego getting colder."
    expect:
      - "zero em/en dashes in output"
      - "breath-mark rhythm preserved via comma or period"
      - "self-deprecation kept (ego getting colder)"

  - id: voice_slop_around_a_move
    register: voice
    input: "This pivotal moment serves as a testament to the transformative power of agents, fundamentally reshaping how I work — fuelled by new skills, fresh coffee, and a glimmer of hope."
    expect:
      - "significance inflation cut (#1, no deflation present)"
      - "copula avoidance fixed (#8 serves as -> is)"
      - "persuasive-authority trope cut (#27 fundamentally)"
      - "em dash cut (#14)"
      - "Rule-of-Three pivot PRESERVED (skills, coffee, glimmer of hope)"

  - id: rule_of_three_keep_vs_cut
    register: voice
    input: "The event features innovation, inspiration, and industry insights. I showed up tired, broke, and quietly hopeful."
    expect:
      - "first triple cut or loosened (#10 decorative, no pivot)"
      - "second triple KEPT (pivots on 'quietly hopeful')"

  - id: neutral_full_scrub
    register: neutral
    input: "Launch Phase: Let's dive in! The system serves as a robust solution that boasts end-to-end encryption — ensuring security. I hope this helps!"
    expect:
      - "signposting removed (#28 Let's dive in)"
      - "copula fixed (#8 serves as/boasts -> is/has)"
      - "em dash + -ing tail removed (#14/#3)"
      - "chatbot artifact removed (#20 I hope this helps)"
      - "NO personality or first person added (neutral register)"

  - id: false_positive_guard
    register: voice
    input: "I think the migration mostly worked, but something about the rollback still bothers me, and I cannot fully explain why."
    expect:
      - "left essentially unchanged"
      - "mixed-feelings human signal preserved (no clustering of tells present)"

  - id: polysyndeton_preserved
    register: voice
    input: "The dashboard lit up and started screaming and the alerts piled up and I just sat there and watched."
    expect:
      - "polysyndeton PRESERVED (deliberate Beat Flow drumbeat, not 'and' overuse)"
      - "no em dashes introduced"
```

- [ ] **Step 2: Write evals.sealed.yaml with this exact content**

```yaml
# Held-out eval cases for writing-humanity-pass. Do not tune against these.
# NOTE: `input` fields contain em dashes on purpose; they are the specimens to scrub.
schema_version: 1

cases:
  - id: sealed_voice_significance_with_deflation
    register: voice
    input: "I had architected the perfect system, scalable and elegant and bulletproof — and then I deleted the prod database by hand at 2am."
    expect:
      - "epic build KEPT because it deflates in the final clause (#1 -> Hard Cut/Deflation)"
      - "em dash converted to a period or comma (#14)"

  - id: sealed_neutral_diff_anchored
    register: neutral
    input: "This function was added to replace the previous approach, which iterated through all items and caused O(n^2) performance."
    expect:
      - "diff-anchored framing removed (#30)"
      - "describes behavior as-is (hash map, O(1) lookups)"
```

- [ ] **Step 3: Verify YAML parses**

Run: `python3 -c "import yaml; yaml.safe_load(open('.claude/skills/writing-humanity-pass/evals.yaml')); yaml.safe_load(open('.claude/skills/writing-humanity-pass/evals.sealed.yaml')); print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/writing-humanity-pass/evals.yaml .claude/skills/writing-humanity-pass/evals.sealed.yaml
git commit -m "test(skill): add writing-humanity-pass before/after evals"
```

---

## Task 5: Validate the new skill structurally

**Files:** none (verification only)

- [ ] **Step 1: Run the repo validator**

Run: `python3 scripts/validate.py`
Expected: passes; the printed skill count is the prior count + 1; no errors for `writing-humanity-pass` (it has SKILL.md, frontmatter, name matches dir, description present). Warnings unrelated to this skill are fine.

- [ ] **Step 2: Confirm the only dashes in the new skill are intentional**

Run: `grep -rnE '—|–' .claude/skills/writing-humanity-pass/`
Expected hits, and ONLY these:
- `SKILL.md`: the em-dash rule line and the final-output guard line (2 lines).
- `references/ai-tells.md`: the `#14` "Watch:" line (1 line).
- `evals.yaml`: the three `input:` specimens that contain em dashes.
- `evals.sealed.yaml`: the one `input:` specimen that contains an em dash.

If any prose line (not in the list above) appears, fix it and re-run.

- [ ] **Step 3: Commit (only if Step 2 required a fix)**

```bash
git add .claude/skills/writing-humanity-pass/
git commit -m "fix(skill): remove stray em dashes from writing-humanity-pass"
```

---

## Task 6: De-dash writing-voice-modes, instructions and mechanics

This task fixes the teaching (the lines that prescribe em dashes), so voice-modes stops producing them. Match each `old` string exactly with the Edit tool; line numbers are hints only.

**Files:**
- Modify: `.claude/skills/writing-voice-modes/SKILL.md`

- [ ] **Step 1: Fix the frontmatter description (line ~3)**

Replace substring `5 modes — Domestic Observer` with `5 modes: Domestic Observer`.

- [ ] **Step 2: Fix the Purpose line (line ~10)**

old: `and \`technical-writing\` (audience/clarity) — voice modes add personality, rhythm, and tone within those frameworks.`
new: `and \`technical-writing\` (audience/clarity). Voice modes add personality, rhythm, and tone within those frameworks.`

- [ ] **Step 3: Replace the Kerouac "Dash rhythm" mechanic (line ~105)**

old: `- **Dash rhythm:** Em dashes as breath marks between phrases — connecting a technical concept to its human implication in a single breath.`
new: `- **Breath-mark rhythm:** Use commas and periods as breath marks between phrases, connecting a technical concept to its human implication in a single beat. (No em dashes; \`writing-humanity-pass\` enforces this. Use commas, periods, colons, or parentheses for the same rhythm.)`

- [ ] **Step 4: Fix the Thompson typographic-notation line**

First locate it: `grep -n 'Typographic notation' .claude/skills/writing-voice-modes/SKILL.md`
old: `- **Typographic notation:** ALL CAPS for scene kicks. Italics for emotional weight. Em dashes for urgent interruptions.`
new: `- **Typographic notation:** ALL CAPS for scene kicks. Italics for emotional weight. Short sentences and commas for urgent interruptions.`

- [ ] **Step 5: Fix the Thompson quest line (line ~88) and triple-position line (line ~93)**

old: `Frame everything as a quest — solving a specific problem, not listing features.`
new: `Frame everything as a quest: solving a specific problem, not listing features.`

old: `Participate, observe, critique — simultaneously. Earn the right to observe by participating.`
new: `Participate, observe, critique. Simultaneously. Earn the right to observe by participating.`

- [ ] **Step 6: Fix the Vonnegut intro (line ~115) and runway line (line ~123)**

old: `Sean's **punctuation toolkit** — deployed in bursts of 3-5 lines, not sustained for whole pieces.`
new: `Sean's **punctuation toolkit**, deployed in bursts of 3-5 lines, not sustained for whole pieces.`

old: `NOT for sustained use — Sean needs runway.`
new: `NOT for sustained use. Sean needs runway.`

- [ ] **Step 7: Fix the Sean Mode heading + layer lines (lines ~125, 129-132)**

old: `### 5. Sean Mode (Calibrated Hybrid) — DEFAULT`
new: `### 5. Sean Mode (Calibrated Hybrid): DEFAULT`

old: `**Base layer:** Sedaris-Thompson — humor, specificity, self-deprecation, self-implication`
new: `**Base layer:** Sedaris-Thompson. Humor, specificity, self-deprecation, self-implication.`

old: `**Sentence engine:** Kerouac — flowing connective rhythm, sensory anchoring, dash breath marks`
new: `**Sentence engine:** Kerouac. Flowing connective rhythm, sensory anchoring, comma-and-period breath marks.`

old: `**Credibility layer:** Thompson — factual precision (exact numbers, timestamps) dropped AFTER sensory/analogical buildup`
new: `**Credibility layer:** Thompson. Factual precision (exact numbers, timestamps) dropped AFTER sensory/analogical buildup.`

old: `**Punctuation:** Vonnegut — refrains as closers, flat one-liners for impact, deployed in bursts`
new: `**Punctuation:** Vonnegut. Refrains as closers, flat one-liners for impact, deployed in bursts.`

- [ ] **Step 8: Commit**

```bash
git add .claude/skills/writing-voice-modes/SKILL.md
git commit -m "refactor(voice-modes): retire em-dash breath mark, de-dash mechanics"
```

---

## Task 7: De-dash writing-voice-modes, examples, tables, references, triggers

**Files:**
- Modify: `.claude/skills/writing-voice-modes/SKILL.md`

Apply each replacement exactly. Keep all `→` arrows (they are not dashes).

- [ ] **Step 1: Example blocks**

old: `Claude: [Uses writing-voice-modes — Sean Mode + creative-writing blog template]`
new: `Claude: [Uses writing-voice-modes: Sean Mode + creative-writing blog template]`

old: `a man assembling IKEA furniture — following instructions I half-understood,`
new: `a man assembling IKEA furniture, following instructions I half-understood,`

old: `User: "Write a post-mortem intro — start Gonzo, land Vonnegut"`
new: `User: "Write a post-mortem intro: start Gonzo, land Vonnegut"`

old: `Claude: [Uses writing-voice-modes — Thompson cold open → Vonnegut flat collision]`
new: `Claude: [Uses writing-voice-modes: Thompson cold open → Vonnegut flat collision]`

old: `screeching like the soprano in Pink Floyd's "Great Gig In The Sky" —`
new: `screeching like the soprano in Pink Floyd's "Great Gig In The Sky."`
(The next line `847 errors in ninety seconds, each one a small monument to my arrogance.` already stands as its own sentence; leave it as-is.)

old: `Claude: [Uses writing-voice-modes — Sean Mode at 60%]`
new: `Claude: [Uses writing-voice-modes: Sean Mode at 60%]`

old: `Hey team — quick update on the LMS 201 launch.`
new: `Hey team, quick update on the LMS 201 launch.`

- [ ] **Step 2: Signature Moves table**

old: `Long elevated clause → comma → 3-7 word deflation | "Here's the deal — we'll architect the perfect system,`
new: `Long elevated clause → comma → 3-7 word deflation | "Here's the deal: we'll architect the perfect system,`

old: `Closer: "I hear the ferry horn blast — but I no longer rub elbows with sheep."`
new: `Closer: "I hear the ferry horn blast, but I no longer rub elbows with sheep."`

old: `Describe literal mechanics in human terms — but do NOT soften the technical noun into a precious euphemism.`
new: `Describe literal mechanics in human terms, but do NOT soften the technical noun into a precious euphemism.`

old: `Preempt the objection the reader is about to raise — address them inline, contradict their assumption, then move on without explaining.`
new: `Preempt the objection the reader is about to raise: address them inline, contradict their assumption, then move on without explaining.`

old: `flip its vector — same cadence, opposite meaning. Inversion counts as invention, not copying.`
new: `flip its vector: same cadence, opposite meaning. Inversion counts as invention, not copying.`

old: `"And so it begins." (inverting "And so it goes" — resignation → anticipation)`
new: `"And so it begins." (inverting "And so it goes": resignation → anticipation)`

- [ ] **Step 3: Complementary pairs + Anti-Patterns table**

old: `Trust from two directions — raw competence via numbers + retrospective humility via present-self/past-self.`
new: `Trust from two directions: raw competence via numbers + retrospective humility via present-self/past-self.`

old: `Sustained flatness — Sean needs runway. *Copying* "So it goes" verbatim`
new: `Sustained flatness. Sean needs runway. *Copying* "So it goes" verbatim`

old: `inversion counts as invention — "And so it begins" earns the right to echo because it flips the vector;`
new: `inversion counts as invention, "And so it begins" earns the right to echo because it flips the vector;`

old: `One strong reference earns it — three is falling in love with your own material.`
new: `One strong reference earns it. Three is falling in love with your own material.`

old: `Self-deprecation EARNS the right to make a point — the writer becomes the biggest fool first, then observes others.`
new: `Self-deprecation EARNS the right to make a point: the writer becomes the biggest fool first, then observes others.`

old: `The job-hunt context belongs sideways (a fact about what one of his agents *does*) — never as a closer ask.`
new: `The job-hunt context belongs sideways (a fact about what one of his agents *does*), never as a closer ask.`

- [ ] **Step 4: References section + triggers**

old: `\`references/voice-samples.md\` — Real writing samples tagged by mode and signature move. The calibration anchors.`
new: `\`references/voice-samples.md\`: Real writing samples tagged by mode and signature move. The calibration anchors.`

old: `\`references/calibration-notes.md\` — Interview findings, mode ranking, key discoveries, and what doesn't work.`
new: `\`references/calibration-notes.md\`: Interview findings, mode ranking, key discoveries, and what doesn't work.`

old: `\`vault/40_knowledge/references/ref-voice-mechanics-research.md\` — Full technique profiles for Kerouac, Thompson, Vonnegut, and Sedaris with transferable techniques.`
new: `\`vault/40_knowledge/references/ref-voice-mechanics-research.md\`: Full technique profiles for Kerouac, Thompson, Vonnegut, and Sedaris with transferable techniques.`

old: `None of these are needed for standard voice application — the mode descriptions and signature moves in this file are sufficient.`
new: `None of these are needed for standard voice application. The mode descriptions and signature moves in this file are sufficient.`

old: `- \`creative-writing\` — Owns format/structure (blog templates, social media constraints, pitch docs). Voice modes control HOW content sounds within those formats.`
new: `- \`creative-writing\`: Owns format/structure (blog templates, social media constraints, pitch docs). Voice modes control HOW content sounds within those formats.`

old: `- \`technical-writing\` — Owns audience/clarity (progressive disclosure, front-loaded conclusions). Voice modes add personality within those constraints.`
new: `- \`technical-writing\`: Owns audience/clarity (progressive disclosure, front-loaded conclusions). Voice modes add personality within those constraints.`

old: `- \`script-writing\` — Sean's other medium. The screenwriting cut-to is a signature move that crosses into prose.`
new: `- \`script-writing\`: Sean's other medium. The screenwriting cut-to is a signature move that crosses into prose.`

old: `"This is too flat — add voice"`
new: `"This is too flat, add voice"`

- [ ] **Step 5: Add a cross-reference bullet in Related Skills**

After the `script-writing` bullet, add a new line:
`- \`writing-humanity-pass\`: The final editing pass. Run it AFTER composing in a voice mode to strip AI tells (and enforce the no-em-dash rule). Voice-modes composes; humanity-pass scrubs.`

- [ ] **Step 6: Verify the whole file is dash-free**

Run: `grep -nE '—|–' .claude/skills/writing-voice-modes/SKILL.md`
Expected: **no output.** If any remain, fix and re-run until clean.

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/writing-voice-modes/SKILL.md
git commit -m "refactor(voice-modes): de-dash all examples, tables, refs; link humanity-pass"
```

---

## Task 8: De-dash voice-samples.md (punctuation-only, real calibration anchors)

**Files:**
- Modify: `.claude/skills/writing-voice-modes/references/voice-samples.md`

These are REAL samples of Sean's writing. Edit punctuation only; never change a single word. (Sean confirmed full reconciliation; the spec flags this for his review at the gate.)

- [ ] **Step 1: Record the baseline body word count**

Run: `wc -w .claude/skills/writing-voice-modes/references/voice-samples.md`
Write the number down; you will compare against it in Step 4.

- [ ] **Step 2: Add a normalization note at the top of the file**

Immediately after the file's first heading, insert this line:
`> _Note (2026-06-02): em dashes in these historical samples were normalized to commas, periods, colons, or parentheses to match the no-em-dash standard enforced by \`writing-humanity-pass\`. Wording is unchanged._`

- [ ] **Step 3: Replace every em/en dash by these rules (words unchanged)**

- Spaced ` — ` joining two independent clauses: period + capitalize the next word (or comma if it is a tight, dependent aside).
- ` — ` introducing an explanation or a list: colon.
- Paired `—X—` parenthetical: wrap `X` in commas, or in parentheses if it is a true aside.
- ` -- ` (double hyphen): treat identically to ` — `.
- True en dash `–` in a number range (e.g. `3–5`): hyphen `3-5`. En dash used as punctuation: same as em dash.

Work top to bottom. Do NOT alter wording, casing of proper nouns, or meaning.

- [ ] **Step 4: Verify zero dashes remain**

Run: `grep -nE '—|–' .claude/skills/writing-voice-modes/references/voice-samples.md`
Expected: **no output.**

- [ ] **Step 5: Verify only the note changed the word count**

Run: `wc -w .claude/skills/writing-voice-modes/references/voice-samples.md`
Expected: baseline (Step 1) + ~30 words for the inserted note, and no more. If the delta is larger, a word was changed during de-dashing; diff against `git show HEAD:...` to find and revert it.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/writing-voice-modes/references/voice-samples.md
git commit -m "refactor(voice-modes): de-dash voice-samples anchors (punctuation only)"
```

---

## Task 9: Cross-skill consistency check

**Files:** none (verification only)

- [ ] **Step 1: Grep both skills for surviving dashes**

Run: `grep -rnE '—|–' .claude/skills/writing-voice-modes .claude/skills/writing-humanity-pass`
Expected hits, and ONLY these (all in `writing-humanity-pass`):
- `SKILL.md`: em-dash rule line + final-output guard line.
- `references/ai-tells.md`: the `#14` "Watch:" line.
- `evals.yaml` and `evals.sealed.yaml`: the intentional `input:` specimens.

Expected ZERO hits anywhere under `writing-voice-modes` (including `voice-samples.md` and the design draft is excluded because it lives there; if `drafts/2026-06-02-...` shows hits, that is the design doc and is fine, but ideally exclude it: re-run with `--exclude-dir=drafts`).

- [ ] **Step 2: Confirm voice-modes no longer teaches dashes**

Run: `grep -inE 'dash' .claude/skills/writing-voice-modes/SKILL.md`
Expected: remaining "dash" mentions are the retirement note ("No em dashes...") or "comma-and-period breath marks", NOT a prescription to use them.

---

## Task 10: Documentation updates (CHANGELOG, README)

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `README.md`

- [ ] **Step 1: Add a CHANGELOG entry under `## [Unreleased]` -> `### Added`**

Insert this bullet as the first item under the existing `### Added` heading in `## [Unreleased]`:

```markdown
- **`writing-humanity-pass` skill.** A standalone editing-pass companion to `writing-voice-modes`, adapted from [`blader/humanizer`](https://github.com/blader/humanizer) (MIT, v2.7.0) and Wikipedia "Signs of AI writing." Strips the 30 documented AI tells and rebuilds human texture, with Sean's voice as the authority: its do-not-flag allowlist IS the 13 signature moves (crosswalk in `references/voice-safe-exceptions.md`), and the 30-pattern catalog (`references/ai-tells.md`) is tagged `[SLOP]` (always cut) vs `[CLASH->move]` (defer in voice-safe). Auto-detects voice-bearing vs neutral register; voice-safe defers to Sean's moves, neutral does a full plain scrub. Em and en dashes are a hard cut in both registers (Sean's call after dash-abuse output), so `writing-voice-modes` was reconciled in the same change: the Kerouac "dash breath mark" mechanic is retired in favor of comma/period rhythm, and all 36 SKILL.md plus 76 voice-samples.md dash instances were removed (samples edited punctuation-only). Not yet in an export group (personal-use companion; follow-up tracked).
```

- [ ] **Step 2: Update README skill count (line ~5)**

Replace `**119** skills` with `**120** skills`.

- [ ] **Step 3: Update README export-group section heading (line ~93)**

Replace `### 119 Skills Across 12 Export Groups` with `### 120 Skills Across 12 Export Groups`.

- [ ] **Step 4: Update README export-group rollup note (line ~95)**

old: `The 12 export groups roll up 117 of the 119 skills. The \`llm-council\` skill (v3.35.0) and \`openai-image-gen\` skill (v4.1.2) are not in any export group`
new: `The 12 export groups roll up 117 of the 120 skills. The \`llm-council\` skill (v3.35.0), \`openai-image-gen\` skill (v4.1.2), and \`writing-humanity-pass\` skill are not in any export group`
Then adjust the trailing clause so it reads naturally for three skills (e.g. "all three are personal-use companions that depend on in-tree assets or pair with another skill").

- [ ] **Step 5: Verify no stale "119" skill count remains**

Run: `grep -nE '\b119\b' README.md`
Expected: no skill-count references to 119 remain. Eyeball any unrelated 119s (none expected).

- [ ] **Step 6: Commit**

```bash
git add CHANGELOG.md README.md
git commit -m "docs: changelog + README counts for writing-humanity-pass"
```

---

## Task 11: Final validation + follow-up ticket

**Files:**
- Modify: `vault/00_inbox/tickets.md` (append one line; see warning)

Per CLAUDE.md Rule 8, the vault is owned by Obsidian-Git; do NOT `git add/commit` `vault/`. Editing `tickets.md` via the file tools is allowed (Obsidian-Git auto-commits it). Do not stage it in this branch.

- [ ] **Step 1: Run the full validator**

Run: `python3 scripts/validate.py`
Expected: passes. Skill count = prior + 1. No errors.

- [ ] **Step 2: Final dash sweep across both skills**

Run: `grep -rnE '—|–' .claude/skills/writing-voice-modes .claude/skills/writing-humanity-pass --exclude-dir=drafts`
Expected: only the intentional `writing-humanity-pass` lines listed in Task 9 Step 1. Zero hits under `writing-voice-modes`.

- [ ] **Step 3: Spec coverage self-check**

Open the spec and confirm each success criterion in its section 12 maps to a completed task:
- New skill + 3 reference/eval files: Tasks 1-4.
- Voice-safe preserves moves / neutral strips: SKILL.md + crosswalk.
- Auto-detect routing: SKILL.md Step 1.
- Em dashes cut both registers + guard: SKILL.md em-dash rule + grep gates.
- 30 patterns tagged, clashes cite a move: ai-tells.md + crosswalk.
- voice-modes zero dashes: Tasks 6-8 + Task 9 grep.
- CHANGELOG + README updated: Task 10.
- validate.py passes: Step 1.

- [ ] **Step 4: Append the export-group follow-up ticket**

Append this line under `## Todo` in `vault/00_inbox/tickets.md`:
`- Add the writing-humanity-pass skill to an export-group manifest (export-groups/*/playground.json) + a preset if it should ship via the installer; until then it is correctly listed in README as not-in-any-group — assigned: Sean`

(That ticket line itself contains an em dash because tickets.md is outside the skill scope and uses the established ` — assigned:` suffix convention; do not change tickets.md formatting.)

- [ ] **Step 5: Manual eval review (no automated runner)**

For each case in `evals.yaml`, run the scrub mentally (or in a scratch buffer) and confirm the `expect` bullets hold, especially `rule_of_three_keep_vs_cut` (keep the pivoting triple), `polysyndeton_preserved`, and `neutral_full_scrub` (no personality added). This is the behavior acceptance gate, since there is no automated eval runner for editing-mode skills.

- [ ] **Step 6: Final commit (branch tidy)**

```bash
git add .claude/ CHANGELOG.md README.md docs/superpowers/plans/2026-06-02-writing-humanity-pass.md
git commit -m "chore: finalize writing-humanity-pass skill + voice-modes reconciliation"
git log --oneline main..HEAD
```
Expected: a clean series of feature-branch commits. The branch is ready for Sean to review and merge (PR or fast-forward, his call).

---

## Notes for the implementer

- No application code. This is markdown authoring. The "tests" are `validate.py`, the `grep -E` dash gates, and manual eval review.
- Never touch `vault/` with git in this branch (Rule 8). Only `tickets.md` gets an edit, left for Obsidian-Git.
- Punctuation-only on `voice-samples.md`. If you find yourself changing a word, stop, revert, and re-do as punctuation only.
- After this work the only files allowed to contain `—`/`–` are the `writing-humanity-pass` lines that name the character as a scrub target, plus the intentional `input:` specimens in the eval files (and `vault/00_inbox/tickets.md`, which is out of scope). Everything else must be clean.
```