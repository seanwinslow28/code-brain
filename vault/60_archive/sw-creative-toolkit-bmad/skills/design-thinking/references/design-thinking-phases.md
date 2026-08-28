# Design Thinking Phases — Quick Reference

Read this file when you need a fast refresher on what each phase produces, what makes it succeed or fail, and when to loop back versus push forward.

---

## The Five Phases

```
Empathize → Define → Ideate → Prototype → Test → (back to any earlier phase)
```

The arrows are the *common* path. The actual process is non-linear: testing often reveals empathy gaps, ideation often reveals weak framing. Loop back without apology.

---

## Phase 1 — Empathize

**Goal:** Understand the people you're designing for.

**Why it matters:** Without empathy, solutions solve the wrong problems.

**What you produce:** Raw observations, interview notes, journey maps, empathy maps. *Not* solutions yet.

**Common methods:** User interviews, observation/shadowing, empathy mapping, journey mapping, diary studies. (See `references/design-methods.md`.)

**Fail modes to watch for:**
- Stopping at what users *say*; missing what they *do*.
- Synthesizing too early — collapsing 30 raw insights into 3 themes before patterns emerge.
- Designing for an imagined "average user" instead of specific people.

**Move on when:** You can articulate user pain in their own words and you keep hearing the same things.

---

## Phase 2 — Define

**Goal:** Frame a user-centered problem statement.

**Why it matters:** A bad problem definition guarantees a bad solution. A good one inspires ideation without prescribing it.

**What you produce:**
- Point of View (POV): `[User type] needs [need] because [insight].`
- How Might We (HMW) questions reframing the problem as opportunities.
- Affinity-clustered insight themes.

**Example POV:** *"Busy parents need a way to feel connected to their children's education because current communication is scattered and time-consuming."*

**Fail modes:**
- POV that's actually a solution in disguise.
- HMW too narrow ("How might we add a notification?") or too broad ("How might we improve the world?"). Aim for *just* abstract enough to leave solution space open.
- Skipping POV/HMW and jumping straight from research to ideas.

**Move on when:** You have one POV that anchors the work and 3–5 HMW questions that feel productive to brainstorm against.

---

## Phase 3 — Ideate

**Goal:** Generate a wide range of solutions. Diverge before converging.

**Why it matters:** First-instinct solutions are usually obvious. Quantity unlocks better quality.

**What you produce:** 30–100+ raw ideas, then a clustered shortlist of 2–3 to prototype.

**Common methods:** Brainstorming, Crazy 8s, SCAMPER, provotype sketching, analogous inspiration. (See `references/design-methods.md`.)

**Fail modes:**
- Converging in the same session you diverge — kills wild ideas before they get heard.
- One person dominating the room. Use silent generation (Brainwriting, Crazy 8s) to fight this.
- Stopping at 10 ideas. The good ones usually live past 30.

**Anti-bias note:** When generating ideas, deliberately shift creative domain every 10 ideas — different industry, different metaphor, different scale. LLMs and humans alike cluster semantically without prompting.

**Move on when:** You have 2–3 concepts that excite the team, address the POV, and feel feasible enough to prototype.

---

## Phase 4 — Prototype

**Goal:** Make ideas tangible enough to test.

**Why it matters:** Discussion goes in circles; a rough artifact gets reactions. Fidelity is the enemy of speed at this stage.

**What you produce:** Paper sketches, click-through wireframes, role-play scripts, Wizard-of-Oz simulations, physical mockups. Whatever's just-real-enough to provoke real reactions.

**Common methods:** Paper prototyping, role-playing, Wizard of Oz, storyboarding, physical mockups.

**Fail modes:**
- Polishing too early. Pixel-perfect screens kill honest feedback ("It looks finished — I don't want to be rude…").
- Building before learning. Engineering the prototype defeats the purpose.
- Testing the wrong thing. Define *what you're trying to learn* before deciding fidelity.

**Move on when:** A user can walk through the experience and react to it without you explaining it.

---

## Phase 5 — Test

**Goal:** Validate with real users. Negative results are valuable — they save you from building the wrong thing.

**Why it matters:** Internal consensus is not validation. You're testing assumptions, not asking for approval.

**What you produce:** Observed behavior, captured feedback, validated/invalidated assumptions, prioritized iteration list.

**Common methods:** Usability testing, Feedback Capture Grid, A/B testing, Assumption Testing, Iterate and Refine.

**Fail modes:**
- Testing with the team or friends instead of representative users.
- Asking "Do you like it?" instead of giving them a task and watching what they actually do.
- Treating critique as an attack on the prototype rather than data.

**Sample size rule of thumb:** 5–7 users per round catches ~80% of usability issues. More users without iteration is wasted budget.

**Move on when:** You can clearly state what's validated, what's invalidated, what to change, and what to keep.

---

## Non-Linear Loops

Testing rarely sends you cleanly forward. Common loop-backs:

| What you find in Test… | Loop back to… |
|---|---|
| Users have a different pain than you assumed | Empathize |
| The HMW was framed wrong; even good ideas miss the real problem | Define |
| Concept resonates but execution falls flat | Prototype |
| You can't tell if it's working without more data | Test (next round, refined) |

Loop without shame. The whole point of low-fidelity prototyping is that loops are cheap.

---

## When Design Thinking Fits — and When It Doesn't

**Fits:**
- New product or feature where user experience matters
- Reimagining an existing experience
- Cross-functional initiative needing shared empathy
- Innovation opportunity where you suspect unmet needs

**Doesn't fit:**
- Pure technical or backend problems with no user touchpoint
- Compliance/regulatory work with fixed requirements
- Timeframes that don't allow user validation (you'll just be guessing in expensive packaging)

If you're not sure whether to use design thinking, ask: *"Could the wrong understanding of the user produce the wrong solution here?"* If yes, use it.
