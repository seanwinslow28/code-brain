# Phase 3: Interview + Writing Exercises — Session Guide

## Setup

Start a Claude Code session in your `claude-code-superuser-pack` repo.
Open with this single prompt that loads context and kicks off the interview:

---

## The Prompt (paste this to start the session)

```
Read these 3 files:
1. vault/40_knowledge/references/ref-voice-mechanics-research.md
2. .claude/skills/creative-writing/SKILL.md
3. .claude/skills/technical-writing/SKILL.md

You're about to help me build a `writing-voice-modes` skill. The ref doc
contains technique profiles for 4 authors (Kerouac, Thompson, Vonnegut,
Sedaris) distilled from deep research. The two SKILL.md files are the
existing format skills that voice modes will work alongside.

We're doing this in two phases:

PHASE A — Interview (calibration)
Ask me questions ONE AT A TIME to understand my personal writing
preferences and how they map to the 4 voice mode profiles. Don't
ask all questions at once. Wait for my answer before asking the next.
Keep it to 8-10 questions total. You're calibrating, not exploring.

PHASE B — Writing Exercises (testing)
After the interview, we'll do hands-on writing in each mode so I can
feel which techniques resonate vs. which feel forced. I'll tell you
when I'm ready to move to Phase B.

Start Phase A now. Ask your first question.
```

---

## What to Expect in Phase A (Interview)

Claude Code should ask questions in roughly this arc:

**Questions 1-3: Your natural voice**
- How do you naturally write when no one's editing you? (Slack messages,
  quick notes, journal entries) — short and punchy? Long and flowing?
- When you re-read something you wrote that you're proud of, what made
  it work?
- Do you gravitate toward humor, directness, storytelling, or analysis
  when writing about something you care about?

**Questions 4-6: Author resonance**
- Which of the 4 authors' techniques excited you most during the research?
  Which felt like "oh, I already do a version of that"?
- Are there techniques from any author that you admire but wouldn't use
  in your own writing? What feels wrong about them for you?
- When you imagine writing a blog post about your ComfyUI workflow or
  your Claude Code setup, which author's ENERGY feels right? (Not their
  exact style — their energy.)

**Questions 7-8: Practical constraints**
- What are you actually going to write with these voice modes? Blog posts?
  Twitter threads? Newsletter? Portfolio narratives? Technical docs? All?
- Is there an audience you're writing FOR? (Other PMs? Creative technologists?
  General tech audience? Personal expression?)

**Your job during the interview:**
- Be honest, not aspirational. Don't say "I want to write like Thompson"
  if your natural voice is closer to Sedaris. The skill works best when
  it amplifies your actual tendencies, not replaces them.
- Give concrete examples when you can. "I tend to write long sentences
  with lots of dashes" is more useful than "I like flowing prose."
- It's fine to say "I don't know" — that's what the writing exercises
  are for.

---

## Transition to Phase B

When the interview feels complete (8-10 questions), say:

```
Good, I'm ready for Phase B. Let's do the writing exercises.
```

---

## What to Expect in Phase B (Writing Exercises)

### Exercise 1: Four-Mode Test (the core exercise)

Claude Code should ask you for a topic you'd actually write about. If it
doesn't, offer one. Good topics:

- "The first time I got Claude Code to do something that genuinely
  surprised me"
- "Why I'm building a Game Boy fitness RPG in 2026"
- "What I learned switching from 12 years of freelancing to a PM role"
- "The absurdity of managing 15 AI subscriptions"

Claude Code writes the OPENING PARAGRAPH (3-5 sentences) of that topic
in each of the 4 modes:

1. Beat Flow (Kerouac techniques)
2. Gonzo Technical (Thompson techniques)
3. Minimalist Absurdist (Vonnegut techniques)
4. Domestic Observer (Sedaris techniques)

**Your job:** Read all 4 and react honestly:
- Which one made you think "yes, that sounds like me but better"?
- Which one felt forced or like cosplay?
- Which specific LINES or PHRASES from any mode landed?
- Which mode surprised you (liked it more or less than expected)?

### Exercise 2: The Hybrid Draft

Based on your reactions, Claude Code writes a 5th version that blends
the techniques you responded to. This is the starting point for your
personal voice mode.

**Your job:** React to this one more carefully:
- What works? What's still off?
- Does it sound like you or like an AI doing an impression?
- What would you change if you were editing this yourself?

### Exercise 3: Mode Switching (optional, if time/energy allows)

Take the same topic and ask Claude Code to write:
- A Twitter thread in your preferred mode
- A technical doc intro in a mode you wouldn't expect
  (e.g., Vonnegut mode for API documentation)

This tests whether the modes hold up across formats, not just blog posts.

---

## What Comes Out of Phase 3

By the end of this session, you should have:

1. **Interview notes** — Claude Code's understanding of your natural voice
   and preferences (it retains this in the session context)
2. **4 mode samples** — Concrete examples of each mode applied to your topic
3. **Your reactions** — Which modes/techniques resonated and which didn't
4. **A hybrid draft** — The starting point for your personal voice
5. **Enough signal to build the skill** — Phase 4 can happen in the same
   session or a follow-up

---

## Moving to Phase 4 (Skill Creation)

If you have energy left in the same session, say:

```
Based on the interview and writing exercises, let's build the
writing-voice-modes SKILL.md now. Use the ref doc for technique
details, my interview answers for calibration, and the exercise
outputs as example material. Put it at .claude/skills/writing-voice-modes/SKILL.md
```

If you'd rather do it in a fresh session, save the session transcript
(Claude Code's /save command or copy the key outputs) and bring it into
the next session as context.

---

## Time Estimate

| Phase | Time |
|-------|------|
| Setup + context loading | 2 min |
| Interview (8-10 questions) | 15-20 min |
| Exercise 1: Four-mode test | 10-15 min (reading + reacting) |
| Exercise 2: Hybrid draft | 5-10 min |
| Exercise 3: Mode switching (optional) | 10 min |
| Phase 4: Skill creation (if same session) | 20-30 min |
| **Total** | **~60-90 min** |
