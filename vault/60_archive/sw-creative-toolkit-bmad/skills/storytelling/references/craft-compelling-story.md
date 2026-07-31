# Storytelling — Quick Reference

Read this file once for the storytelling mindset, the audience-first principle, and the move-on criteria for each phase.

---

## The Mindset

> **Find the authentic story before styling the surface.**
>
> **Make the abstract concrete through vivid sensory detail.**
>
> **Powerful narratives leverage timeless human truths.**

A story isn't decoration on a message — it's how a message becomes memorable, transferable, and felt. A clean structure with no soul produces text. A felt story with no structure produces a memory.

The nine phases progress through three movements:

```
Anchor (1–3) → Compose (4–6) → Land & Persist (7–9)
```

---

## Phase 1 — Sidecar Memory Load

**Goal:** Pick up where prior storytelling sessions left off.

**Why it matters:** Sophia keeps a sidecar of audience profiles, framework preferences, and voice signatures from prior sessions. Loading them prevents re-litigating decisions the user has already made.

**What you produce:** Loaded prior preferences (or "no prior preferences" on first run).

**Practical note:** Sidecar reads from `${CLAUDE_PLUGIN_DATA}/storyteller-sidecar.md`. If the file doesn't exist or doesn't load, continue without it — this is an enrichment, not a gate.

---

## Phase 2 — Purpose, Audience, Subject

**Goal:** Establish the three anchors every story rests on.

**Why it matters:** Stories without explicit purpose drift toward "tell me about your product" — which produces nothing memorable. Stories without explicit audience generalize until they don't move anyone. Stories without subject specificity stay abstract.

**What you produce:**
- **Purpose** — single-sentence intent (persuade, inspire, explain, mobilize, connect)
- **Audience** — named, specific, with their current beliefs and emotional state
- **Subject** — what the story is *about*, in concrete terms

**Fail modes:**
- Vague purpose ("tell our story" — that's a topic, not a purpose)
- Generic audience ("everyone" — that's no audience)
- Abstract subject ("our values" — what specific manifestation of values?)

**Move on when:** Purpose, audience, subject each pass the "could a stranger paraphrase it back?" test.

---

## Phase 3 — Audience Profile & Emotional Arc

**Goal:** Map the audience precisely; design the emotional journey you want them to take.

**Why it matters:** Audience belief at the start ≠ audience belief at the end. The arc between them is the story. Naming the arc makes it intentional.

**What you produce:**
- Audience profile (demographics, beliefs, pains, prior knowledge, biases, decision power)
- Emotional starting state ("skeptical," "exhausted," "curious-but-cautious")
- Emotional ending state ("convinced," "energized," "implicated")
- Emotional arc — the named beats between start and end

**Fail modes:**
- Skipping prior beliefs ("they think we're a vendor; the story has to flip that to partner")
- Designing for the audience you wish you had vs. the one you've got
- Emotional arc that's all up or all down — flat affect is just as bad as no story

**Move on when:** You can name the audience's starting emotion, ending emotion, and at least one inflection point in between.

---

## Phase 4 — Framework Selection

**Goal:** Choose the structural skeleton that fits the purpose.

**Why it matters:** Every framework has a job. Hero's Journey is for transformation. Pixar Spine is for tight, emotional brevity. StoryBrand is for customer-as-hero marketing. Wrong framework = wrong shape.

**What you produce:** Chosen framework with one-line rationale; alternatives considered.

**Fail modes:**
- Defaulting to Hero's Journey for everything (it's not always the answer; Pixar Spine often beats it for short-form)
- Picking a framework before knowing the purpose
- Stacking frameworks ("Hero's Journey but also Three-Act and BAB") — pick one structural skeleton

**Move on when:** The framework fits the purpose so cleanly that the next phase (drafting) feels obvious.

---

## Phase 5 — Character & Voice

**Goal:** Define the protagonist and the narrator's voice.

**Why it matters:** Audiences track *characters*, not concepts. Voice is the signature that makes the story feel made-by-someone, not generated.

**What you produce:**
- Protagonist (who the story is about; can be a customer, a founder, an idea-as-character)
- Antagonist or obstacle (what stands in the way)
- Stakes (what wins or loses)
- Narrator voice (first / third person; tone register; sentence rhythm)

**Voice register choices:**
- Formal / curatorial / authoritative
- Conversational / warm
- Comedic / observational (Sedaris-tuned)
- Lyrical / sensory
- Plainspoken / direct

**Fail modes:**
- Protagonist who's actually a feature list ("our product")
- No real obstacle (low stakes = low engagement)
- Narrator voice that drifts mid-piece — tonal inconsistency kills credibility

**Move on when:** You can describe the protagonist, obstacle, stakes, and voice in five sentences.

---

## Phase 6 — Generate Full Narrative

**Goal:** Draft the complete story with sensory detail and felt beats.

**Why it matters:** Drafting *is* discovery. Outlines feel complete; drafts reveal what's actually missing.

**What you produce:** A complete narrative draft following the chosen framework, with vivid sensory detail and emotional beats placed deliberately.

**Sensory detail principles:**
- Concrete > abstract ("the warm coffee" > "the experience")
- Specific > general ("the 3 AM Slack ping" > "the late-night message")
- Sensory > intellectual (sight, sound, touch, smell, taste)
- One vivid detail beats five generic ones

**Fail modes:**
- All-tell, no-show — explaining what the audience should feel rather than letting them feel it
- Sensory clichés ("the cold steel of determination") — fresh detail, not stock imagery
- Forgetting the audience while writing — you're writing *for them*, not for yourself

**Move on when:** The draft has a beginning that hooks, a middle that builds, and an ending that lands.

---

## Phase 7 — Sensory Detail & Emotional Beats Pass

**Goal:** A second pass to deepen the sensory and emotional layers.

**Why it matters:** First drafts usually have skeletons. Second drafts have skin and weight.

**What you produce:** Revised narrative with strengthened sensory anchors and intentional emotional pacing.

**The pass:**
- Find the abstract sentences. Replace with concrete ones.
- Find the moments where emotion *should* land. Slow them down.
- Find moments that drag. Cut or compress.
- Read aloud. Anything that feels written-not-spoken gets revised toward speech rhythm.

**Move on when:** A reader could mark the emotional peaks of the piece and they'd match the ones you intended.

---

## Phase 8 — Platform Adaptation

**Goal:** Adapt the narrative for where it will live — without losing its soul.

**Why it matters:** The same story performs differently as a 60s social post vs. an 800-word essay vs. a pitch deck. Each medium has its own physics.

**Common adaptations:**

| Platform | Adaptation |
|---|---|
| Pitch deck | Compress into slide-by-slide narrative; one beat per slide; visuals carry equal weight |
| Blog post | Add scannable structure (headers, pull quotes) without breaking arc |
| Video script | Add visual cues, pacing markers, hook every 15–30s |
| Social post | Compress to one beat; pick the *one* moment that earns the share |
| Email | Personal voice; subject line as the hook |
| Stage talk | Strip text; speaker notes carry detail; slides become poster art |

**What you produce:** One or more platform-adapted versions, each preserving the core arc.

**Fail modes:**
- Adapting the words but not the *rhythm* of the medium (writing prose for a stage talk)
- Stripping so much that the soul is gone (a 60-character version of a 1,500-word piece can't carry the original's depth — pick a different beat)

**Move on when:** Each platform version stands alone *and* recognizably belongs to the same story.

---

## Phase 9 — Impact Plan & Sidecar Update

**Goal:** Define how impact will be measured and persist learnings for next time.

**Why it matters:** Stories without measurement are wishes. Sessions without persistence are starts-from-zero.

**What you produce:**
- Impact plan — how the story's effect will be measured (engagement, conversion, recall, qualitative response)
- Sidecar update — write back to `${CLAUDE_PLUGIN_DATA}/storyteller-sidecar.md` with what to remember next time:
  - Audience profiles confirmed or refined
  - Framework preferences (which worked, which didn't)
  - Voice signatures (the user's preferred register)
  - Anti-patterns the user has rejected

**Move on when:** The user has a clear measurement plan AND the sidecar carries learnings forward.

---

## When This Workflow Fits — and When It Doesn't

**Fits:**
- Brand or product narratives
- Pitch decks and investor presentations
- User stories, case studies, customer journeys
- Change communication, vision narratives
- Marketing campaigns and content
- Founder / leadership storytelling

**Doesn't fit:**
- Pure technical documentation
- Factual reporting without narrative need
- Extremely short formats (headlines, taglines — those are micro-craft, not story)
- Visual-only artifacts — use `sw-creative-toolkit:presentation` for those

If you're not sure whether a piece needs storytelling, ask: *"Does the audience need to feel something specific to act?"* If yes, use this. If no, plain prose is faster.
