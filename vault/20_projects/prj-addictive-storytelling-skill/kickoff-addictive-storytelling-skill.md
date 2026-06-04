---
type: project
domain: [creative-studio]
status: draft
created: 2026-06-03
ai-context: "Self-contained kickoff prompt to build a new 'Addictive Storytelling + Value' skill layer that sits upstream of [[writing-voice-modes]] and [[writing-humanity-pass]] — owns narrative architecture and reader-value delivery so every Substack post solves a real problem Sean actually had. Build deferred until after the 2026-06-11 skill-freeze (see [[skill-ideas-deferred]])."
---

# Kickoff Prompt — Build the "Addictive Storytelling + Value" Skill Layer

> Paste everything below the line into a fresh Cowork session. It is self-contained: it carries the source thesis, the repo map, and the build contract so the new session starts with full context. Re-attach `substack-writing-tips-1.md` if you still have it (optional — its core thesis is embedded below).

---

## Role & Goal

You are helping Sean Winslow (AI/Tech/Creative PM, mid job-hunt, ships with an autonomous agent fleet) build a new **skill layer for addictive storytelling and reader value**, primarily for his Substack but reusable across his writing. This is NOT an edit to the existing `writing-voice-modes` skill. It is a new, separate skill (possibly a small suite) that sits *upstream* of voice and completes a three-skill chain:

```
NEW: storytelling + value     →  writing-voice-modes  →  writing-humanity-pass
(WHAT story, WHAT value)         (HOW it sounds)          (scrub AI tells, no em dashes)
```

The new skill owns **narrative architecture and value delivery**: the story shape that makes someone keep reading, and the payoff that makes them come back. Voice-modes and humanity-pass already exist and are strong; do not duplicate their jobs. Read both before designing anything (paths below).

**The problem we're solving:** Right now Sean's Substack posts are stories spun from his personal projects *for the sake of having a post*. The target state: tell an interesting, addictive story about a real problem he hit, then hand the reader genuine value at the end — show how he solved it and how they can too. The post someone *wishes existed* when they were stuck on the same thing.

## The Source Thesis (load-bearing — this is the spine of the value model)

From the YouTube transcript that prompted this work (paraphrased, keep it central):

- The #1 metric in writing/creating online is **building a library of things YOU genuinely find valuable** — things that clarified your thinking, improved your craft, made your systems better.
- Where most people fail: they create for the sake of creating, or they create what they *think* someone else wants. Both start from the wrong goal and just "check a box."
- The move: **wake up and ask "what do I selfishly want to learn / build / improve next?"** Solve that for yourself first. The newsletter is just *double-monetizing* work you were already going to do. The internet is very good at finding 10,000 people exactly like you.
- This is also the most *sustainable* path, and consistency is the whole game.

Translate this into a hard rule the skill enforces: **every post must solve a real problem Sean actually had.** The story is the hook; the solution is the gift. No "content for content's sake" passes the gate.

## Repository Map (real paths — verify before acting)

The two existing skills this must integrate with live in Sean's command center repo, `code-brain`:

- `/Users/seanwinslow/Code-Brain/code-brain/.claude/skills/writing-voice-modes/` — SKILL.md, `references/voice-samples.md`, `references/calibration-notes.md`, `evals.yaml`, `evals.sealed.yaml`, `drafts/`. **Read SKILL.md fully.** Note its 5 voice modes, 13 signature moves, the professional dial, and the content-type→mode mapping.
- `/Users/seanwinslow/Code-Brain/code-brain/.claude/skills/writing-humanity-pass/` — SKILL.md, `references/ai-tells.md`, `references/voice-safe-exceptions.md`, `evals.yaml`, `evals.sealed.yaml`. **Read SKILL.md fully.** Note: it runs LAST, enforces the no-em-dash hard rule, and defers to Sean's signature moves.

The downstream consumer: the **Substack-Drafter agent** (`agents-sdk/`, default-disabled, Thursday 18:00 weekly, reads `writing-voice-modes` verbatim, 5-week voice rotation). The new skill should be designed so this agent can eventually load it the same way. Confirm its current behavior in `/Users/seanwinslow/Code-Brain/code-brain/CLAUDE.md` before wiring anything.

Follow the **house skill conventions** you observe in the two existing skills: YAML frontmatter with a trigger-rich `description`, progressive disclosure (lean SKILL.md + `references/` for depth), a `references/` folder, and an `evals.yaml` + `evals.sealed.yaml` pair. Match that structure exactly.

## Operating Constraints (Sean's preferences)

- Be concise and direct; cut words that don't change the point.
- Be a thinking partner, not an executor — pressure-test ideas, surface trade-offs, then commit.
- Sean knows coding fundamentals and is deep into agentic engineering. Don't over-explain basics.
- Use the **task list** (TaskCreate/TaskUpdate) to track the phases below, and **AskUserQuestion** to confirm scope before building.
- Update `code-brain`'s `CHANGELOG.md` and any relevant count tables when you add the skill(s), per that repo's maintenance rules. Run `python3 scripts/validate.py` after.

---

## Phase 1 — Deep Research (use the `deep-research` skill)

Invoke the **`deep-research`** skill and run a fact-checked, multi-source deep dive. Produce a single cited research report saved to `vault/20_projects/research/` in `code-brain` (match the dated-filename convention you see there). Research these five threads, then synthesize across them — do not just list findings, extract the *transferable mechanics*:

1. **Addictive storytelling / engagement architecture.** What actually makes readers keep going and come back: open loops and curiosity gaps, narrative tension, the Zeigarnik effect, "but/therefore" causal chains (vs "and then"), in medias res openings, the promise-progress-payoff contract, micro-cliffhangers in short form. Pull from proven practitioners (e.g., long-running high-retention newsletter writers, story-structure canon) — cite real sources, not vibes.
2. **The story-then-value structure for short-form.** How the best technical/maker newsletters fuse a personal narrative with a concrete, takeaway-rich payoff. Where the "here's how you do it too" lands without killing the story. Formats that convert one-time readers into returning subscribers (the value/retention loop). Tie back explicitly to the source thesis above.
3. **Impressing recruiters / hiring signal through writing.** What hiring managers and recruiters in PM/AI actually read for: evidence of judgment, systems thinking, shipping, and reflection. How to demonstrate competence through story without it reading as a resume or a desperate pitch. (Cross-reference the "Desperation Posing as Self-Deprecation" anti-pattern already in `writing-voice-modes` — the ask belongs sideways, never as a closer.)
4. **Keeping a personal voice while using structure.** How writers apply repeatable story frameworks without sounding formulaic or templated. The failure mode where structure flattens voice. How to keep Sean's calibrated voice (the 5 modes / 13 signature moves) intact when a story scaffold is imposed on top.
5. **Funny without cheesy.** The mechanics of humor that builds trust vs humor that undercuts credibility. Specificity over generic jokes, self-implication, comedic timing in prose, the line between wit and try-hard. Map to Sean's existing humor moves (Hard Cut/Deflation, Rule of Three + pivot, Humor as Trojan Horse).

**Deliverable for Phase 1:** the cited report + a one-page synthesis of the 8–15 most transferable mechanics, each phrased as something a skill could operationalize (a rule, a checklist item, or a structural template). Flag any mechanic that conflicts with an existing voice-mode or humanity-pass rule so we resolve it deliberately.

## Phase 2 — Plan (translate research into a skill design)

Before writing any skill files, produce a short design doc and get Sean's sign-off via **AskUserQuestion**. Decide and propose:

1. **One skill or a small suite?** Likely candidates: a `storytelling-architecture` skill (story shapes, open loops, tension, the narrative spine) and possibly a separate `substack-value-engine` skill (the problem-first value contract, payoff structure, retention loop, recruiter signal). Recommend the cleanest decomposition — bias toward the fewest skills that keep single-responsibility clean. Justify it.
2. **The chain contract.** Define exactly how the new skill(s) hand off to `writing-voice-modes` then `writing-humanity-pass`: what each layer owns, what it must NOT touch, and the invocation order. Add a "Related Skills" + integration section mirroring how the existing two cross-reference each other.
3. **The value gate.** Encode the source thesis as an explicit gate: a post may not proceed unless it names (a) the real problem Sean hit, (b) the actual solution, (c) what the reader can now do. Define how the skill blocks or flags "content for content's sake."
4. **Short-form fit.** Specify how the story scaffold compresses to Substack short-form (hook → tension → turn → payoff → so-can-you) without the long runway that some voice modes assume.
5. **Eval design.** Plan `evals.yaml` cases that test: an addictive open, a satisfying value payoff, voice preserved under structure, funny-not-cheesy, and the recruiter-signal-without-desperation line. Plan the sealed-eval pair the same way the existing skills do.

## Phase 3 — Build

Once the plan is approved:

1. Author the skill(s) under `/Users/seanwinslow/Code-Brain/code-brain/.claude/skills/<skill-name>/` with `SKILL.md` (lean, trigger-rich frontmatter, progressive disclosure), `references/` for the deep mechanics from Phase 1, and `evals.yaml` + `evals.sealed.yaml`.
2. Wire the integration: update the "Related Skills" sections of `writing-voice-modes/SKILL.md` and `writing-humanity-pass/SKILL.md` so the trio cross-references cleanly (the new skill composes the story + value, voice-modes makes it sound like Sean, humanity-pass scrubs).
3. Update `code-brain` `CHANGELOG.md`, any skill-count tables in `CLAUDE.md`/`README.md`, and run `python3 scripts/validate.py`.
4. (Optional, propose it) note how Substack-Drafter would load the new skill in its weekly run.

## Phase 4 — Verify (do not skip)

- Write one **real test post** end-to-end using the full chain on an actual problem Sean solved (pick from his projects: anima pipeline, the vault critic, intent-engineering MCP, the Substack-Drafter itself). Run it through new-skill → voice-modes → humanity-pass.
- Score it against the new `evals.yaml`: addictive open? genuine value payoff? voice intact? funny-not-cheesy? recruiter signal without the desperate ask? zero em dashes?
- Run a critique pass (consider Sean's `llm-council` variance profile for blind-spot coverage) and report whether the post is something a stranger stuck on the same problem would actually bookmark. If not, iterate before declaring done.

---

## Definition of Done

A new skill (or tight suite) that, chained with `writing-voice-modes` and `writing-humanity-pass`, reliably turns one of Sean's real problems into a short Substack post that (1) hooks and holds, (2) sounds like Sean, (3) hands the reader a concrete, usable solution, (4) signals competence to a recruiter without pitching, and (5) makes them want the next one. Plus: cited research report, evals, integration wiring, changelog, and one verified test post proving the whole chain produces "pure gold worth reading."
