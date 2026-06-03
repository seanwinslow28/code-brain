---
type: reference
domain:
  - creative-studio
status: active
context: screenplay-craft-system
ai-context: "Phase 3 session guide for the script-writing skill upgrade. Drives a Claude Code / Cowork interview + writing-exercise session that calibrates the 6-filmmaker mechanics (ref-screenplay-mechanics-research.md) to Sean's screenwriting voice. Output is screenplay-calibration-notes.md, which feeds the Phase 4 SKILL.md build. Downstream consumers: anima's Sam (scriptwriter) and Bea (storyboard) agents."
created: 2026-05-31
source: deliverable-5, voice-modes-pipeline-port
---

# Deliverable 5 — Phase 3 Session Guide
### Script-Writing Skill Upgrade · The Interview + Calibration Session

> **What this is.** A complete, copy-paste-ready protocol for a *fresh* Claude Code / Cowork thread to interview Sean and run him through writing exercises — the same move that made `writing-voice-modes` land. Phase 1 (deep research) and Phase 2 (compile → `ref-screenplay-mechanics-research.md`) are done. This is Phase 3. Its single output is **`screenplay-calibration-notes.md`**, which Phase 4 turns into the upgraded `SKILL.md`.
>
> **Why a separate thread.** Calibration works best when the interviewer is *naive* — it can't pattern-match Sean's answers to what it already "knows" he'll say. Start this in a clean session so the discoveries are real, not confirmed.

---

## 0. Design rationale (read once, then skip)

A few choices worth surfacing before you run it, so you can adjust:

- **The interview leads, the exercises confirm.** In the voice-modes run, the strongest findings (*"Sean's closers are his strongest move," "one strong reference earns it — three is self-indulgence"*) came from watching Sean *rewrite* AI output, not from him describing his taste. So the interview is deliberately short and opinionated (forced A/B/C choices, one at a time), and the exercises are where the real signal lives. Budget your attention accordingly.
- **Every question is anchored to a real Sean script.** Generic "how do you like to open a scene?" produces generic answers. "*New Years Resolutions* opens on a fly crawling on cocktail weenies while two guys argue about burrata — is the grotesque-mundane cold open your default entry gear, or a one-off?" produces a calibration. Each question below cites a specific moment from his shorts so he's reacting to evidence, not theorizing.
- **The 6 modes are framed as *tools to rank against his existing voice*, never as styles to imitate.** The whole point of the prose skill was discovering Vonnegut is "punctuation toolkit only, not a full mode." We want the screenplay equivalent — which filmmaker mechanics are native, which are stretch, which are traps for him specifically.
- **Miyazaki does double duty.** Per the kickoff's anti-patterns, the Miyazaki-flavored exercises (dialogue economy, the Ma beat, haptic visuality) are written so their output also feeds the `animation-pipeline` upgrade. Flag anything Sean says about *visual* storytelling for both skills.
- **The output mirrors `calibration-notes.md` exactly.** Same section shape (Interview Findings → Mode Ranking → Key Discoveries → What Doesn't Work), plus one new table — *Sean's Screenplay Signature Moves* — that is the screenplay-form translation of his prose signatures (the `cut to`, hard cut/deflation, rule-of-three-with-pivot) plus whatever new ones surface. That table is the load-bearing artifact Phase 4 builds the mode descriptions around.

---

## 1. The kickoff prompt (paste this into the new thread)

```
You are my second brain and long-term creative partner. We're running Phase 3
of an upgrade to my `script-writing` skill — the calibration phase.

CONTEXT YOU NEED:
A few months ago we built a `writing-voice-modes` skill by running a 4-phase
pipeline: deep research per author → compile into one reference doc → interview
me + writing exercises to calibrate to MY voice → build the SKILL.md. It worked.
We're now doing the exact same thing for screenwriting, studying 6 filmmakers/
teams for their SCREENPLAY CRAFT (not biography): Charlie Kaufman, Taika Waititi,
Hayao Miyazaki, the Pixar story system, Bo Burnham, and Tina Fey × Donald Glover.

Phases 1 and 2 are DONE. Before we start, read these files in order:
1. vault/40_knowledge/references/screenwriting-skill-building/ref-screenplay-mechanics-research.md
   — the compiled 6-filmmaker mechanics reference (the techniques we're calibrating)
2. .claude/skills/script-writing/SKILL.md
   — the current skill we're upgrading
3. .claude/skills/writing-voice-modes/references/calibration-notes.md
   — what a GOOD Phase 3 output looks like. This is the shape we're producing.
4. .claude/skills/writing-voice-modes/SKILL.md
   — see the "Sean's Signature Moves" table. Several of those (the screenwriting
   cut-to, hard cut/deflation, rule of three + pivot, self-deprecation as
   structure) come straight from my screenwriting instincts. They carry over.

MY BACKGROUND: I've written ~8 shorts — 5 animated 2D comedy shorts that won
best short comedy animation at indie festivals, plus spec scripts (A.P. Bio,
Food Traveler, a Lord of the Flies comedy pilot). My scripts are in the
Seans-Old-Scripts folder alongside the reference doc if you want texture. Two
I'll reference a lot: "I Quit" (ironic V.O. narrator, rule-of-three escalation,
chaotic exit punchline) and "New Years Resolutions" (Father Time as a deadpan
narrator who undercuts everyone — "They broke up on January 9th").

HOW THIS SESSION RUNS:
- First you interview me. Ask the questions ONE AT A TIME. Wait for my answer
  before the next. Don't lecture between questions — react briefly, then move on.
- Then we do writing exercises. You'll draft scene fragments in different
  filmmaker modes; I'll rewrite the ones that feel off. Watch what I change.
- At the end you'll write `screenplay-calibration-notes.md` synthesizing what we
  learned — same structure as the voice-modes calibration-notes.md.

Your job is to DISCOVER my screenwriting voice, not flatter it. If I contradict
myself, push on it. If an exercise reveals something my interview answers didn't,
trust the exercise. Don't imitate the 6 filmmakers — figure out which of their
mechanics are native to me, which are a stretch, and which are traps.

Start by confirming you've read the four files, then give me a one-paragraph
plan for the session and ask Question 1.
```

---

## 2. The interview (Section guide for the interviewing Claude)

> **Instructions to the interviewer:** Ask these **one at a time**. Offer the lettered options but make clear Sean can reject all of them — the options exist to force a *specific* reaction, not to constrain him. After each answer, reflect it back in one sentence and note what it implies, then move on. Do **not** batch them. Aim for 9 core questions; Q10 is the self-ranking capstone. The "Listen for" notes are for you, not to read aloud.

### Q1 — Scene entry gear
*"New Years Resolutions* opens on a fly scraping its legs across cocktail weenies while two guys one-up each other about burrata. *I Quit* opens on a V.O. narrator flatly explaining Gary's life over corporate-jargon babble. When you start a scene, what's your default way in?"
- **A.** A grotesque/mundane *image* the audience reads before anyone speaks
- **B.** An ironic narrator/V.O. frame that's already lying to me
- **C.** A character mid-action, no context, I catch up
- **D.** Direct-to-camera confession (Waititi's Confessional Shortcut)

*Listen for: which is reflex vs. which he reaches for when stuck. The V.O. narrator recurs across his work — is it a core tool or a crutch? (That's Q2.)*

### Q2 — The ironic narrator: tool or crutch?
"You lean on an undercutting narrator a lot — the V.O. in *I Quit*, Father Time in *New Years Resolutions* ('They broke up on January 9th'). Is that a load-bearing device you want the skill to protect, or a habit you'd cut if I pushed you? When does it *earn* its place versus do the work the scene should do visually?"

*Listen for: the Pixar/Miyazaki trap — narration articulating what the image should carry. Find his own line between "the narrator is the joke" (earned) and "the narrator is exposition" (crutch). This becomes an anti-pattern entry.*

### Q3 — On-the-nose vs. oblique dialogue
"Your dialogue swings both ways. Linda says exactly what she means ('I'm tired of lying to our son, Gary'). But Pete and Tim talk *around* everything — a whole panicked aria about $50 truffles that's really about status. When do you want a character to just say it, and when do you want them talking about truffles?"
- **A.** Default oblique; directness is a rare spike
- **B.** Default direct; obliqueness for the comedic characters only
- **C.** Depends on who's the fool in the scene

*Listen for: whether obliqueness is instinct or craft-he-applies. The voice-modes finding was that subtext-through-action is native to him via screenwriting. Confirm or complicate it.*

### Q4 — Verbal fingerprints
"Pixar's rule: if you can swap a line between two characters with no loss, the dialogue failed. When you write two characters, do you *hear* distinct voices on the first pass, or do they start interchangeable and separate in revision? How do you make two people sound incompatible in 3 minutes?"

*Listen for: does he think in worldview-collisions (Buzz/Woody) or does differentiation come from situation/status? Tim-vs-Pete and Gary-vs-Linda are both status duels — flag if that's his actual engine.*

### Q5 — Is the gut punch even wanted?
"The whole skill assumes comedy-with-feelings. But some of your shorts are pure sketch — *New Years Resolutions* is closer to a roast than a tearjerker. Honestly: across your festival shorts, how often were you actually going for the emotional gut punch versus just trying to be funny?"
- **A.** Almost always want the punch (Waititi/Pixar end of the dial)
- **B.** Rarely — comedy's the point, feeling is a bonus (sketch end)
- **C.** Depends on length/format

*Listen for: this sets the skill's center of gravity. If he's more sketch than sentiment, the Fey/Glover and Burnham mechanics matter more than Miyazaki's Comfort Trigger — and we shouldn't over-weight catharsis machinery he won't use.*

### Q6 — The tonal pivot, in screenplay form
"In prose, your signature move is the hard cut / deflation — build an epic register, land mundane in the final clause. What's its *screenplay* equivalent? When you flip a scene from funny to real (or funny to bleak), how do you physically do it on the page?"
- **A.** A hard CUT TO — smash between incompatible tones (Burnham's Violent Juxtaposition)
- **B.** Hold on a face too long, no cut, let it curdle (Waititi's Deadpan Hold)
- **C.** Drop the laugh 75% in and trail into something honest (Waititi's Mid-Laugh Pivot)
- **D.** A beat of dead silence / stillness first, *then* the turn (Miyazaki's Micro-Ma)

*Listen for: which of these he already does without a name for it. The `cut to` is documented as load-bearing across all his formats — confirm it's A, or discover he actually prefers the hold. This is the single most important dialogue/scene finding.*

### Q7 — How endings resolve
"*I Quit* ends cathartic and loud — Gary throws his briefcase at a jury and runs home yelling 'I love my family!' *New Years Resolutions* ends on Father Time deflating everyone. Cathartic resolution or deflationary/ambiguous — which is your instinct? And does your prose 'callback closer' (end on the opening image, transformed) carry into your scripts?"
- **A.** Cathartic, earned, emotional (Pixar/Waititi)
- **B.** Deflationary / ironic / bittersweet (Kaufman/Miyazaki)
- **C.** I want both somehow — the laugh AND the ache

*Listen for: the voice-modes session proved his closers are his strongest, most reliable instinct. Whatever he says here, the exercises will test it (Exercise 4). Note if the callback-closer transfers — it's a candidate signature move for the table.*

### Q8 — Words vs. pictures
"This skill feeds an animation pipeline. Could you write a 2-minute stretch with *no dialogue* and trust the visuals (Miyazaki's dialogue economy), or is your comedy verbal-first — built on rhythm, references, and people talking past each other (Fey's density)? Be honest about where your comfort is."
- **A.** Verbal-first; silence scares me
- **B.** I could go wordless and want to get better at it
- **C.** Mix — wordless setups, verbal payoffs

*Listen for: dual-purpose Miyazaki signal — flag everything here for `animation-pipeline` too. If he's verbal-first (likely, given the scripts), the skill should teach the wordless muscle deliberately, not assume it.*

### Q9 — Ensemble vs. two-hander
"*New Years Resolutions* is a room full of people bouncing off a narrator. *I Quit* is basically one family unit. Do you think in *crowds* — reaction chains, register collisions, someone always cutting in — or in *pairs*, two worldviews dueling? Which generates more for you?"

*Listen for: structural default. Crowd-thinking pulls toward Fey's ensemble management + Glover's drift; pair-thinking pulls toward Pixar's verbal fingerprint + Kaufman's two-handers. The skill's scene templates should match his actual unit of composition.*

### Q10 — The self-ranking capstone
"Last one. Of the six modes — Kaufman (meta/absurd-as-wound), Waititi (deadpan + sincere), Miyazaki (visual/quiet), Pixar (causal/structural), Burnham (tonal violence/self-implication), Fey×Glover (density + drift) — which feels most like *you already*, and which feels most foreign or fake when you try it? Same way you told me Vonnegut was the one you couldn't sustain in prose."

*Listen for: THE mode-ranking seed. In voice-modes this produced "Vonnegut is punctuation toolkit only." Expect a parallel: probably one mode is home base, one or two are stretches, and at least one is a trap (looks like him but isn't). Write the ranking from this + the exercises, not from this alone.*

---

## 3. Transition prompt (interview → exercises)

> Paste/say this to move into the exercises once Q10 is answered:

```
Good — that's the interview. Now we test it.

I'm going to give you scene fragments to write in specific filmmaker modes.
The point isn't for you to nail them — it's for me to rewrite the ones that
feel wrong, so you can see where my actual voice pulls away from the technique.
Write them fast and a little rough. When I rewrite, narrate what you think I
changed and WHY before I confirm — that's how we both learn the calibration.

We'll do four (maybe five). Ready for Exercise 1?
```

---

## 4. The writing exercises

> **Instructions to the interviewer:** Use **one shared premise** across Exercises 1–4 so the comparisons are clean and Exercise 4's callback has something to call back to. Propose a premise that fits Sean's lane (a small, mundane, comedic situation with a buried feeling) and get his nod before starting. Suggested default if he has none: **"A man tries to return an opened item to a store without a receipt."** It's mundane, status-loaded, escalatable, and animatable. After each rewrite, **state your read of what he changed and why, then let him confirm or correct** — the gap between your read and his correction is the calibration.

### Exercise 1 — Same opening, three modes
Write the opening **8–12 lines** of the short three times, properly formatted, same premise each time:
- **(a) Kaufman — the Mundanity Weapon:** treat the absurd/charged situation with bureaucratic seriousness; emotional payload on a separate channel (V.O. or overheard).
- **(b) Miyazaki — Dialogue Economy:** wordless. Open on physical action and haptic detail (the warped door, the weight of the item). No one speaks.
- **(c) Waititi — Confessional Shortcut:** character addresses camera in the first 10 seconds; their self-assessment contradicts what we see.

**Extract:** Which does he rewrite *least* (native)? Which does he fight or abandon (stretch/trap)? Does he silently re-add a V.O. narrator to the wordless one (confirming Q2)? Note his instinct on entry gear vs. what he claimed in Q1.

### Exercise 2 — Dialogue obliqueness + verbal fingerprints
Hand him a deliberately flat, on-the-nose exchange (4 lines) between two characters in the premise — both saying exactly what they feel. Ask him to rewrite it so (1) neither character answers the other directly, and (2) the two are assigned *incompatible registers* (one declarative-absolute, one self-interrupting-conditional — Pixar's verbal fingerprint).

**Extract:** Does oblique come naturally (confirming Q3)? How far does he push subtext-through-action — does he add a contradicting *physical* action (the supply-room move from the current skill's Example 3)? Is his differentiation engine worldview (Pixar) or status (his scripts' actual pattern)?

### Exercise 3 — The tonal pivot
Give him a comedic beat that's landing — say, the return-counter argument peaking. Ask him to execute the comedy→real turn **three ways**: (a) hard `CUT TO` smash (Burnham), (b) hold-on-the-face-no-cut (Waititi Deadpan Hold), (c) dead-silence-beat-then-turn (Miyazaki Micro-Ma). Then ask which one is *his*.

**Extract:** This is the core confirmation of Q6 and of the `cut to` as load-bearing. Watch whether he deflates *downward* (mundane/bleak) or punches *upward* (sincere) — that tells you if he's closer to Burnham's dissonance or Waititi's sincerity. Whichever he picks becomes the screenplay-form entry for "hard cut / deflation" in the signature-moves table.

### Exercise 4 — The closer (the one that matters most)
Write the **final image** two ways: (a) Pixar cathartic — the Want resolved through physical action, no thematic line spoken; (b) Kaufman/Miyazaki ambiguous — a new equilibrium, the question left open. Then challenge him: "Now write a **callback closer** that returns to Exercise 1's opening image with one element transformed."

**Extract:** The voice-modes session found *every* exercise ended with Sean replacing the AI closer with something better — closers are his single most reliable instinct. Expect the same. Whatever he writes here is gold; capture it verbatim as a voice sample. Confirm whether the callback-closer transfers from prose (Q7) — if it does, it's a locked signature move.

### Exercise 5 — *(optional, if energy holds)* — Visual storytelling / animation crossover
Take an emotional beat from the premise and ask him to render it as **pure physical action, no dialogue** — using Metaphor Compression (make the feeling the literal visible object) or Kaufman's Physical Displacement Loop (a mundane object behaves wrongly as the feeling intensifies; the face stays calm).

**Extract:** Dual-purpose — flag everything for `animation-pipeline`. Tests Q8's wordless muscle directly. Note whether he can stay out of the dialogue and trust the image, or whether he taps out and reaches for a line. This is the clearest read on the script↔board boundary that Sam and Bea will live on.

---

## 5. What the session produces — output spec

> **Instructions to the interviewer:** When the exercises are done, synthesize — don't transcribe. Write **`screenplay-calibration-notes.md`** to the skill's references folder, matching the structure of `writing-voice-modes/references/calibration-notes.md`. Then stop and hand to Phase 4. Sections required:

**`screenplay-calibration-notes.md` structure:**

1. **Header** — "Distilled from a [N]-question interview and [N] writing exercises ([date]). Synthesis, not transcript. Use alongside SKILL.md when calibrating screenplay output." Same disclaimer shape as the prose version.
2. **Interview Findings** — one short block per question (Q1–Q10): the answer + what it implies, in Sean's terms. Bold the decisive word (the prose version bolds *"Dry humor is #1"* etc.).
3. **Mode Ranking (Native → Stretch)** — ordered list of the 6 filmmaker modes from home-base to foreign, each with a one-line *why*, plus an explicit "toolkit-only, not a full mode" call on any that are partial (the Vonnegut-equivalent finding).
4. **Key Calibration Discoveries** — the headline insights, each as a bolded claim + 2–3 sentences of evidence from the exercises. This is the highest-value section — aim for the specificity of *"Sean's closers are his strongest move"* and *"one strong reference earns it — three is self-indulgence."* Likely candidates: where his `cut to` lands, whether the ironic narrator is tool or crutch, sketch-vs-sentiment center of gravity, ensemble-vs-pair default, the wordless-muscle gap.
5. **Sean's Screenplay Signature Moves** *(NEW table — the load-bearing artifact for Phase 4)* — columns: **Move | Mechanic | Where it lands on the page | Example (from his scripts or the exercises)**. Seed it with the screenplay-form translations of his prose signatures — the `cut to`, hard cut/deflation, rule-of-three-with-pivot, self-deprecation-as-structure, callback closer, the ironic-undercutting narrator — and add any new ones the session surfaced. This table is what Phase 4 builds the mode descriptions and anti-patterns around.
6. **What Doesn't Work for Sean** — the anti-patterns / traps, screenplay-specific (parallel to the prose doc's list). Pull from the exercises he abandoned and from `ref-screenplay-mechanics-research.md` §8, narrowed to *his* failure modes.

Also capture, verbatim, **2–4 of his best exercise rewrites** as `voice-samples` candidates (especially closers) — Phase 4 will want real screenplay samples the way voice-modes had `voice-samples.md`.

---

## 6. Handoff to Phase 4 (do this at the very end)

> Close the session with:

```
That's Phase 3. You've written screenplay-calibration-notes.md and saved my best
exercise rewrites as voice samples. Phase 4 is a SEPARATE session: take the
current script-writing/SKILL.md and upgrade it into a voice-calibrated skill
shaped like writing-voice-modes — filmmaker-derived modes, my signature-moves
table, a professional/tonal dial, content-type→mode mapping, and anti-patterns.

Before you stop, give me:
1. A one-paragraph summary of the 3 biggest calibration discoveries.
2. The proposed mode ranking (native → stretch).
3. A flag on anything that should ALSO update the animation-pipeline skill
   (the Miyazaki/visual findings).
4. A note for the anima fleet: how Sam (scriptwriter, Opus) should load these
   modes, and where the script↔board boundary with Bea sits based on what
   Exercise 5 revealed.
```

---

### Pipeline position (for orientation)

```
Phase 1  Deep research per filmmaker        ✅ done (6 Perplexity/Gemini reports)
Phase 2  Compile → ref-screenplay-          ✅ done
         mechanics-research.md
Phase 3  THIS GUIDE → interview + exercises  ◀ you are here
         → screenplay-calibration-notes.md
Phase 4  Build upgraded SKILL.md             next session
         (+ references/, voice-samples)
Phase 5  Port into anima: Sam loads modes,   downstream
         Bea consumes script↔board handoff
```
