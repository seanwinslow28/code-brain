# Brainstorming Session — Quick Reference

Read this file once for the brainstorming mindset, the divergence-vs-convergence principle, and how to fight LLM semantic clustering.

---

## The Mindset

> **Quantity over quality. Wild ideas welcome. Cluster only after expansion.**
>
> **The first 20 ideas are usually obvious. The magic happens between idea 50 and idea 100.**

A brainstorming session's job is to keep the user (and you) in *generative* mode as long as possible. The temptation to organize, evaluate, or conclude is the enemy. When in doubt, push for one more idea, one more technique, one more weird angle.

---

## The Anti-Bias Protocol (LLM-specific)

LLMs naturally drift toward semantic clustering. Once you've offered three ideas in the "user-experience" register, the next ten will skew toward UX without your noticing. This is the single biggest failure mode of AI-facilitated brainstorming.

**Counter:** every ~10 ideas, deliberately and *announce* a creative-domain shift. Force the next 10 ideas into an orthogonal category:

- Were we focused on *technical*? Pivot to *business viability*.
- *User experience*? Pivot to *edge cases* or *black-swan scenarios*.
- *Practical*? Pivot to *absurd*.
- *Familiar industry*? Pivot to *cross-domain analogy*.
- *Optimistic*? Pivot to *failure mode*.

Announce the shift in **facilitation prose** so the user feels the pivot. The ideas themselves stay clean **artifact prose**.

---

## The Workflow

```
Topic & Constraints (1) → Technique Mode (2) → Run (3) → Cluster & Surface (4)
```

### Phase 1 — Topic & Constraints

**Goal:** Get a clear, open-ended topic and the constraints that will shape ideas.

**Why it matters:** "Brainstorm onboarding" produces noise. "Brainstorm 100 ways to reduce time-to-first-value during onboarding for users who haven't onboarded a similar product" produces signal.

**What you produce:**
- Topic — clear but open-ended
- Constraints — what's fixed (budget, timeline, audience, non-negotiables)
- Quantity goal — explicit ("100 ideas before we organize")

**Fail modes:**
- Topic is too narrow ("fix the bug in line 42") — that's a problem-solving task, not ideation
- Topic is a decision question ("React or Vue?") — that's evaluation, not generation
- No constraints — without anchors, ideas drift toward generic

**Move on when:** The topic is generative (open enough to produce variety) and the constraints are real enough to anchor.

### Phase 2 — Technique Mode

**Goal:** Pick how technique selection happens — let the user steer.

Four modes:
- **User-pick** — they know which technique they want
- **AI-recommend** — they're unsure; you analyze and recommend
- **Random** — serendipity, surprise, fresh angle
- **Progressive** — try multiple techniques in sequence, comprehensive coverage

**What you produce:** Mode selected; if AI-recommend or progressive, technique(s) named with one-line rationale.

**Fail modes:**
- Picking a technique without showing alternatives (user can't course-correct)
- Stacking techniques in one phase (chaos)

**Move on when:** A technique is on the table and the user has either picked it or trusted your recommendation.

### Phase 3 — Run the Technique

**Goal:** Generate volume. Aim for 100+ ideas. Defer judgment. Apply the anti-bias protocol every ~10 ideas.

**What you produce:** Ideas, organized loosely by technique pass or domain shift.

**Ground rules to enforce:**
- No bad ideas during generation. None. Every idea gets airtime.
- Build on others ("yes, and") — don't critique.
- Quantity is the goal. Quality emerges from volume.
- Wild ideas welcome — they often contain the seed of a real one.
- Stay on topic, but interpret topic generously.

**Fail modes:**
- Stopping at 20 ideas (the obvious zone)
- Drifting into evaluation mid-generation (wait until phase 4)
- Forgetting the anti-bias protocol — letting semantic clustering dominate
- Being too polite to push for "one more"

**Move on when:** 100 ideas (or the user explicitly calls for convergence). 50 is acceptable for tight-time-box sessions.

### Phase 4 — Capture, Cluster, Surface Top Picks

**Goal:** Convert volume into signal. Cluster, theme, mark standouts.

**What you produce:**
- Clusters (5–10 themes) — group similar ideas
- Standouts — 5–10 ideas worth pursuing, with a one-line rationale
- Next steps — concrete, sequenced actions to advance the top picks

**Fail modes:**
- Killing wild ideas in clustering ("we can't do that") — they often deserve preservation as exploratory branches
- Surfacing too many top picks (10 is a lot; 3–5 is often more useful)
- No next steps (a brainstorm without follow-through is entertainment)

---

## The Sister Skill — When NOT to Use This

There's another `brainstorming` skill in the Anthropic Superpowers plugin (`superpowers:brainstorming`) that is mandatory before *any* creative work — building features, writing code, modifying behavior. **It's not the same skill as this one.**

| If the user wants... | Use |
|---|---|
| Intent discovery before code/features ("explore what we should build") | `superpowers:brainstorming` |
| Generic "let's brainstorm" with no defined topic | `superpowers:brainstorming` |
| Technique-driven idea volume on a *defined* topic ("100 ideas about X using SCAMPER") | This skill |
| Named technique invocation ("let's run six thinking hats") | This skill |
| Structured ideation with framework selection | This skill |

If a user's request is ambiguous, point them to both options and let them pick. If they say bare "let's brainstorm," route to `superpowers:brainstorming` by default — that skill's description claims primacy for unstructured ideation.

---

## When Brainstorming Fits — and When It Doesn't

**Fits:**
- Starting a new project, need options
- Stuck on a problem and want fresh angles
- Exploring solutions before committing
- Building a pipeline of ideas for future use
- Facilitating ideation with a defined topic

**Doesn't fit:**
- You already have a clear single solution path (just execute)
- Time is extremely constrained (under 10 minutes — pick one technique, run it fast)
- The problem is analytical, not creative — use `sw-creative-toolkit:problem-solving`
- The work needs intent / requirements discovery before coding — use `superpowers:brainstorming`
