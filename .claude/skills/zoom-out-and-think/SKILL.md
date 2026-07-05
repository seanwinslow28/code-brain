---
name: zoom-out-and-think
description: System-level root-cause oracle for a codebase or subsystem stuck in repeated band-aid patches. Reads the whole subsystem, researches current best practice for the domain, names the root cause instead of the symptom, and emits an intent-carrying spec for a lesser model to implement. Use when the same class of bug keeps recurring.
---

# Zoom Out and Think

## Purpose

Diagnose a codebase or subsystem that keeps producing the same class of bug no
matter how many times it gets patched. Never start from the latest failing
line — ground in what's actually recurring and what's already been tried, then
read the whole subsystem's state, control flow, and orchestration before
naming anything. Research the current best practice for the specific domain so
the diagnosis is grounded in more than intuition, then name the single
system-level root cause and refuse to let a band-aid pass as a fix. Close by
emitting an intent-carrying spec that hands the real ask, the root cause, and
the change to a lesser model — carrying enough motivational intent and
critical detail that it implements the fix without drifting back into the
same patch pattern. This skill diagnoses and specs; it does not implement the
fix itself.

## Provenance

Assembled from systematic-debugging + plan-and-think + intended-vs-implemented.

## When to Use

- A bug or failure class keeps recurring after two or more patch attempts, and
  nobody can state in one sentence why it actually happens.
- A subsystem has accumulated enough point-fixes that the fixes themselves are
  now part of the problem — contradictory null checks, redundant retries,
  patches that only relocate the failure instead of removing it.
- Before agreeing to "just one more patch" on a system that has already
  absorbed several for the same underlying complaint.
- Producing a root-cause diagnosis and an intent-carrying spec for a cheaper or
  weaker model (e.g. Opus) to implement, where the reasoning behind the fix has
  to survive the handoff intact.
- Not for a first-time bug with no patch history — use `systematic-debugging`
  directly for that. This skill is for the entrenched, already-patched case,
  where the fix has to zoom out past the file that's currently on fire.

## Step 1: Ground First (Hard Gate)

<HARD-GATE>
Do not read the subsystem, do not map control flow, and do not open Step 2
until (a), (b), and (c) below have real answers. "I can already see what's
recurring" or "the fix is obviously X" is exactly the shortcut this gate
exists to block — a diagnosis built on an assumed pattern is a diagnosis of a
bug that doesn't exist. This applies even when the recurring bug looks small,
looks like it has an obvious one-line fix, or has "clearly" been diagnosed
correctly before.
</HARD-GATE>

Ask these three, in order, and wait for real answers before touching any code
or file:

(a) **What keeps recurring** — the specific class of failure, stated precisely
    enough that a different person could recognize the next occurrence. Not
    "it's broken sometimes" — the exact symptom, the exact trigger condition,
    and how many times it has already come back.
(b) **What's been tried** — every patch or workaround already attempted,
    including partial fixes, "it seemed to help for a while," and anything
    abandoned because it didn't fully work. A root-cause hunt that ignores the
    patch history will just re-propose a patch someone already tried.
(c) **What "coherent/correct" looks like end-to-end** — the target state for
    the whole subsystem, not just "this one call stops throwing." If nobody
    can describe the correct end-to-end behavior, that gap is itself a clue.

Do not diagnose, map, research, or propose anything until (a)-(c) are
answered. If the request already answers some of these in passing, restate
your understanding of each back and get explicit confirmation — do not
silently infer the rest just to save a round-trip.

## Step 2: Read the Whole System

Map how the subsystem actually works before touching any single bug instance —
this is the "zoom out": the recurring failure is a symptom of the system's
actual shape, not of the specific file where it last surfaced.

1. **State** — where does the relevant state live, who owns it, and what else
   reads or mutates it? A recurring bug is often state that two components
   both think they own.
2. **Control flow** — trace the real call graph or request/execution lifecycle
   for this subsystem end-to-end, not just the function where the error
   surfaces.
3. **Orchestration** — identify which component actually *decides* (owns the
   policy, the retry logic, the scheduling) versus which components merely
   *execute* what they're told. Recurring bugs cluster exactly where "who
   decides this" is unclear or split across two places.
4. **Compare intent vs. reality** — run the `intended-vs-implemented` move:
   read the subsystem's documented intent (README, design doc, comments,
   original spec, CLAUDE.md entry) and compare it against what the code
   actually does right now. The gap between documented intent and live
   behavior is one of the most common places a recurring bug hides — it means
   nobody has re-verified the assumption since the doc was written.

Do this for the whole subsystem before opening Step 3. A root cause found by
reading only the failing function is still a guess, not a diagnosis.

## Step 3: Research Current Best Practice

Before naming a root cause, web-search the modern best practice for this
specific domain and pattern — not generic advice, the current consensus for
this exact kind of system (e.g. "idempotent retry design for scheduled
launchd agents," not "how to fix bugs").

1. Identify the precise domain/pattern the recurring failure belongs to.
2. Run real web searches against that domain/pattern; favor recent,
   authoritative sources (official docs, post-mortems, widely-cited
   engineering writeups) over the first generic result.
3. Ground the diagnosis in what's found: the root cause named in Step 4 must
   cite the specific source(s) that informed it, by name or URL, inline in
   the diagnosis — not as a bibliography tacked on at the end.
4. If truly no external pattern applies (fully bespoke logic, no comparable
   prior art exists anywhere), say so explicitly rather than silently skipping
   this step.

## Step 4: Name the Root Cause, Refuse the Symptom

State the single system-level cause in one sentence — not a list of
contributing factors, not "several things are going on here."

1. Trace every symptom gathered in Steps 1-3 back to the one point in the
   system where they converge. If they don't converge on one point, the
   investigation isn't done — go back to Step 2, not forward to a fix.
2. Before writing the diagnosis down, check it against these red flags. If the
   fix on the table matches any of them, it is a band-aid — say so explicitly
   in the output, name it as a band-aid, and keep looking for the level above
   it:
   - The fix only changes behavior at the exact call site where the bug last
     surfaced.
   - The fix is "add a retry / add a timeout / add a null check" with no
     account of why that retry, timeout, or null case exists in the first
     place.
   - The fix would need to be repeated at every other call site that shares
     the same recurring pattern.
   - The fix requires a person to remember to do it again next time, rather
     than making the recurrence structurally impossible.
3. The named root cause must explain every instance from Step 1(a) and every
   failed patch from Step 1(b). If it doesn't explain why the previous patches
   didn't hold, it isn't the root cause yet — keep tracing.

## Step 5: Output — Intent-Carrying Spec

Emit one artifact: a spec that carries the real ask, the root cause, and the
change — structured so a lesser model (e.g. Opus) can implement it without
losing the reasoning and drifting back to the same patch pattern at the first
edge case it hits. Use `intent-engineering`'s scaffolding for this, not a bare
instruction diff — the whole reason this step exists is that the implementing
model will not have run Steps 1-4 itself.

At minimum, structure the spec with:

- **The real ask** — what the human actually wants fixed, restated from the
  grounding answers in Step 1, never invented.
- **The root cause** — the single system-level cause named in Step 4, plus the
  best-practice source(s) from Step 3 that ground it.
- **The change** — the fix at the level that removes the whole class of
  recurrence, with enough motivational intent and critical detail (edge
  cases, what "done" looks like, what would still count as a band-aid) that a
  weaker model implementing it can make the same call correctly on an edge
  case the spec didn't spell out.
- **What NOT to change** — the parts of the system Steps 1-4 confirmed are
  already correct, so the implementing model doesn't "fix" them out of
  over-eagerness.

If the fix is large enough to justify it, invoke `intent-engineering` directly
for its full 9-section template. For a small, contained fix, the four elements
above are the floor — never skip straight to a bare instruction list.

## Example

```
User: "This same null-pointer crash in checkout keeps coming back — we've
patched it four times already."
Claude: [Uses zoom-out-and-think] Before I look at any code, three questions:

(a) What keeps recurring — same exact NPE at the same line each time, or does
    it move around the checkout service?
(b) What's been tried — what did each of the four patches actually change?
(c) What would "coherent/correct" look like end-to-end for payment state?

User: (a) Same NPE, but it moves to a different field accessor each time.
(b) Each patch added a null check right before the crash line. (c) An order's
payment state should never be read before the payment webhook has resolved it.

Claude: [Maps state/control-flow/orchestration end-to-end; runs
intended-vs-implemented — the design doc says payment state is "set once,
read-only after," but the code actually lets three different handlers write
it out of order] [Web-searches current best practice for idempotent,
webhook-driven state machines; cites the source]

## Root Cause
Payment state has no single owner — the webhook handler, the poll-fallback,
and the manual-retry path all write it, so any reader can observe a
partially-written state and NPE on whichever field that path hasn't set yet.
The four prior patches each null-checked one more field — not a fix, a
band-aid: it will recur at the next field this pattern touches.

## Intent-Carrying Spec
**Real ask:** stop the checkout NPE from recurring, permanently — not patch
one more field.
**Root cause:** three uncoordinated writers to shared payment state, no single
state-machine owner (cites [source]).
**Change:** collapse all payment-state writes behind one state-machine
transition function; reads block until a transition completes instead of
racing it. [+ edge cases, what still counts as a band-aid]
**What NOT to change:** webhook signature verification — confirmed correct
and unrelated to this recurrence.
```

## Success Criteria

- [ ] All three grounding questions (a)-(c) were asked and answered before any
      system-mapping began
- [ ] The whole subsystem's state, control flow, and orchestration were
      mapped — not just the file containing the latest bug instance
- [ ] An `intended-vs-implemented` comparison was run: documented/intended
      behavior vs. live behavior, with the gap named explicitly
- [ ] Current best practice for the specific domain/pattern was web-searched
      and cited by source inline in the diagnosis
- [ ] A single system-level root cause is named in one sentence, not a list of
      symptoms
- [ ] Any patch-shaped fix that surfaced during diagnosis was explicitly
      flagged as a band-aid and rejected, or the reasoning for accepting it
      anyway was stated
- [ ] Output is an intent-carrying spec (real ask + root cause + change +
      what NOT to change), not a raw instruction diff — sufficient for a
      lesser model to implement without drift

## Copy/Paste Ready

```
"Zoom out and think about why this keeps breaking"
"We keep patching this — find the real root cause"
"Stop symptom-patching X, tell me what's actually wrong"
"Root-cause this and give me a spec Opus can implement"
"Same bug again — zoom out before proposing another fix"
```
