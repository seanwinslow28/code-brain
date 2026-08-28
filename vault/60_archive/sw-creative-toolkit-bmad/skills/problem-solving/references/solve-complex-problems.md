# Systematic Problem Solving — Quick Reference

Read this file once at the start of a session for the diagnostic mindset, the symptoms-vs-causes distinction, and the move-on criteria for each phase.

---

## The Mindset

> **Symptoms lie. Structure doesn't.**

A problem is a system revealing where it's weakest. The right question beats a fast answer every time. Hunt for the structural cause that produces the symptom — not the symptom itself.

The eight phases progress through three movements:

```
Diagnose (Phases 1–4) → Solve (Phases 5–6) → Implement & Verify (Phases 7–8)
```

Diagnostic discipline up front buys you correctness later. Skipping diagnosis is the most common — and most expensive — failure mode.

---

## Phase 1 — Define & Refine the Problem

**Goal:** Transform a vague complaint into a precise, actionable problem statement.

**Why it matters:** "It's slow" is not a problem statement. "Checkout abandonment hit 40% after the 2026-04-12 release" is. Precision is the gate.

**What you produce:**
- Refined problem statement
- Symptoms vs. impact distinction
- Clear success criteria

**Fail modes:**
- Accepting the first description. The first articulation is almost always too vague or already-a-solution-in-disguise.
- Mixing symptoms with causes ("the database is slow because there's no index" — that's already a hypothesis).
- Skipping success criteria. You can't know if you fixed it if you didn't define what fixed looks like.

**Move on when:** A stranger could read the statement and (a) tell you what's wrong, (b) tell you who's affected, (c) recognize the fix when they see it.

---

## Phase 2 — Diagnose & Bound the Problem

**Goal:** Map where the problem exists and where it doesn't. Boundaries reveal patterns.

**Why it matters:** Most "mystery" problems become obvious when you map their boundaries. Intermittent issues often have a boundary you haven't named.

**What you produce:** Is/Is-Not table; observed patterns; eliminated hypotheses.

**Fail modes:**
- Boundary too coarse ("happens on prod, not on dev" — but *which* prod? *which* requests?).
- Confusing absence-of-evidence with evidence-of-absence ("it's never happened to me" ≠ "it doesn't happen").
- Stopping at the first pattern without looking for a second.

**Move on when:** You can describe the problem's habitat in three sentences.

---

## Phase 3 — Root Cause Analysis

**Goal:** Drill from symptoms to the structural cause that produces them.

**Why it matters:** Symptom fixes return as new symptoms. Structure fixes hold.

**What you produce:** Root cause(s) with traceable causal chain; named contributing factors; system dynamics if relevant.

**Choose a method:**
- **Five Whys** — linear cause chain
- **Fishbone** — multi-factor problems
- **Systems Thinking** — recurring problems with feedback loops

**Fail modes:**
- Stopping at the first plausible answer. Five Whys doesn't say "five whys *or fewer*" — keep drilling until the next "why" stops being productive.
- Treating one root cause as *the* root cause when there are multiple. Real systems have multiple contributing structures.
- Confusing blame with root cause. "Bob didn't test it" is rarely the structural answer; the structural answer is "we don't have a pre-merge test gate."

**Move on when:** A different person, given the symptom, could trace forward to the same root cause using your reasoning.

---

## Phase 4 — Forces & Constraints

**Goal:** Understand what's pushing toward solution, what's pushing against it, and what the limiting bottleneck actually is.

**Why it matters:** Even correct solutions fail if forces are misread. The technical fix is often the easy part; adoption is where solutions die.

**What you produce:** Driving forces, restraining forces, primary constraint, named assumptions.

**Fail modes:**
- Treating real and assumed constraints the same. A budget cap is a real constraint. "We've always done it this way" is an assumed one — and often the cheapest to remove.
- Identifying the wrong bottleneck. Optimize the wrong constraint and the system stays just as slow.

**Move on when:** You know what would have to be true (and what would have to change) for solutions to land.

---

## Phase 5 — Generate Solution Options

**Goal:** Diverge widely. Mix systematic and creative methods. Don't converge yet.

**Why it matters:** First-instinct solutions are usually obvious. Quantity unlocks better quality, same as ideation.

**What you produce:** 10–15+ candidate solutions, mixing incremental and breakthrough approaches.

**Choose methods:**
- **Systematic** (TRIZ, Morphological, Biomimicry) for engineering / optimization
- **Creative** (Lateral Thinking, Assumption Busting, Reverse Brainstorming) when stuck
- Mix at least two

**Fail modes:**
- Converging during divergence. Killing wild ideas in the same breath as proposing them shrinks the solution space.
- Stopping too early. If you have 3 ideas and they're all variations on the obvious solution, keep going.
- Ignoring the "wild" lane. Wild ideas often contain the seed of a real solution that gets refined later.

**Move on when:** You have 10+ candidates and the obvious solution feels challenged by at least one alternative.

---

## Phase 6 — Evaluate & Select

**Goal:** Choose the optimal solution against criteria you've named — not vibes.

**Why it matters:** Without an explicit decision protocol, the loudest voice wins. With one, the analysis wins.

**What you produce:** Defined criteria, evaluated options, recommended solution, named assumptions, remaining concerns.

**Fail modes:**
- Picking criteria after evaluating (retrofitting the answer you already wanted).
- Pretending the recommendation is risk-free. There's always something. Name it.
- Skipping the rationale. "Option B" without "*because*" is half a decision.

**Move on when:** You can articulate why the chosen option beats the runner-up in one sentence.

---

## Phase 7 — Implementation Plan

**Goal:** Convert the selected solution into specific actions with owners, sequence, and resource needs.

**Why it matters:** A solution without an implementation plan is a wish. Most solutions die in the gap between "we should do X" and "Sean owns step 3 by Friday."

**What you produce:** Approach (pilot / phased / big bang), action steps, sequence, dependencies, owners, resource needs, milestones.

**Fail modes:**
- Vague ownership. "The team will handle it" is no owner.
- No sequence. A list of actions without dependencies is a wish list, not a plan.
- No first action. The first concrete step matters more than the rest.

**Move on when:** Tomorrow morning, the first owner knows exactly what to do.

---

## Phase 8 — Monitoring & Validation

**Goal:** Define how you'll know the solution is working — and what triggers a pivot if it isn't.

**Why it matters:** Solutions implemented without monitoring are solutions that quietly fail. The validation plan is the difference between "we shipped a fix" and "we know we shipped a fix that worked."

**What you produce:** Success metrics, validation plan, risk mitigation, named adjustment triggers.

**Fail modes:**
- Vanity metrics. "Page views went up" doesn't mean the problem was solved.
- Late detection. If your metric tells you something's wrong six weeks after it broke, the metric is wrong.
- No plan B. "What's our trigger to abandon and pivot?" is a question every plan needs an answer to.

**Move on when:** You could hand the validation plan to a stranger and they'd know what numbers to watch and what action each trigger demands.

---

## Optional Phase 9 — Capture Lessons

**Goal:** Reflect on the process to improve future problem-solving.

**Why it matters:** A team that solves problems well has usually built a habit of debriefing them well.

**What you produce:** What worked, what to avoid, surprising insights, patterns to remember.

**Fail modes:**
- Treating it as a blame audit. The point is structural learning, not person-targeted feedback.
- Skipping it. The lesson un-named is the lesson un-learned.

---

## When Systematic Problem-Solving Fits — and When It Doesn't

**Fits:**
- Complex, persistent challenges
- Recurring problems despite previous fixes
- Multiple plausible solutions, no clear winner
- Cross-system issues
- High-stakes decisions where rigor matters

**Doesn't fit:**
- Well-understood problems with obvious solutions (just fix it)
- Simple, isolated bugs
- Time-critical situations requiring immediate action (do, then debrief)
- Problems where the cost of analysis exceeds the cost of trial-and-error

If you're not sure whether to use this approach, ask: *"Is this problem expensive enough or recurring enough to deserve diagnosis?"* If yes, use it. If no, just fix it.
