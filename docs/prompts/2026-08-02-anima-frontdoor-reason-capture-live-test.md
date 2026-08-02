# Continuation — live-test the anima front door's reason capture

*Kickoff prompt for a fresh session. Paste the body below.*

---

Run a real anima brainstorm to live-test the front door's new reason-capture
behavior. This is an **execution ticket, not a design ticket** — the design was
grilled and ratified 2026-08-02 and shipped in
[anima PR #121](https://github.com/seanwinslow28/anima/pull/121). You are
exercising it, not redesigning it.

## 1. No research phase. No re-planning.

Everything you need is on disk. Do **not** run web research, deep research, or
cloud CLIs. Do **not** re-open the design decisions listed in §3 — they were
settled one at a time with Sean and are recorded in
`vault/00_inbox/tickets.md`. If the test surfaces a genuine flaw, that becomes
a **finding to report**, not a decision you make in-session.

You also do not need the private creative-harness lane for this. The work is
entirely in the public anima repo.

## 2. Read first, in this order

1. `vault/00_inbox/tickets.md` — the bullet beginning **"Live-test the anima
   front door's reason capture before T27c generalizes it"**. That is your
   ticket, including the six things to watch.
2. `anima/.claude/skills/brainstorm-front-door/SKILL.md` — Step 0, the
   subsection **"Every lock carries Sean's reason, in his own words."** This is
   the behavior under test.
3. `anima/.claude/skills/brainstorm-front-door/references/session-sidecar-contract.md`
   — the Shape block and the Rules bullet on verbatim reasons.
4. `anima/briefs/2026-07-02-ai-guru-pilot/frontdoor-session.md` — a real
   sidecar from before this change. Read how locks are actually written and how
   `(verbatim)` is already used on the SPARK line. Your output should look like
   this file plus reason sub-lines.

## 3. What was ratified — do not re-litigate

- The orchestrator asks exactly **`Why that one? One line.`** at each lock.
- The answer lands as an indented `- why (verbatim): "…"` sub-line under the
  lock, quoted **exactly**. Never tightened, merged, or completed.
- On a category-grade answer ("liked B better", "felt right"), the orchestrator
  may offer **one** candidate reason as a thinking prompt. **The guess is never
  the recorded text.** Never guess twice.
- A skipped question records **nothing**. A bare agreement with the guess, with
  no words of Sean's own, records **nothing**. No reason is ever inferred,
  guessed into place, or backfilled later.
- `SUPERSEDES` entries take the sub-line too. The entry line's prose "why" is
  the orchestrator's account of what changed; the sub-line is Sean's reason for
  changing it.

## 4. Run the test

Invoke the `brainstorm-front-door` skill and run a genuine session.

**The spark must be real.** Ask Sean for an actual idea he cares about — a
short, a piece, a project. Do **not** invent a test spark and do **not** reuse
ai-guru or GRANDMASTER. The open question is whether the one-guess prompt
genuinely churns *his* thinking, and a synthetic brainstorm cannot answer that.
His stated reason for choosing that design, verbatim: *"I could like an option,
but not really find the reason why. Having the orchestrator make a guess could
help get the brain churning."*

Run the chain as the skill defines it. Do not shortcut stages to reach the
reason-capture behavior faster — cadence under a full-length session is one of
the things being measured.

## 5. Report these six findings

1. **Did it ask every time?** Or did it drift and start skipping the question
   as the session got long? This is the likeliest failure mode.
2. **Did the quote land verbatim?** Check for tightening, merging, or finishing
   Sean's sentence. Any of those is a real defect.
3. **Did a skip record nothing?** Have Sean deliberately wave one off.
4. **Did a bare agreement record nothing?** Have Sean deliberately agree with a
   guess without adding his own words, and confirm the guess did not become the
   quote.
5. **Did `SUPERSEDES` get the question?** If no supersession occurs naturally,
   say so rather than manufacturing one.
6. **How did the cadence feel?** Ask Sean directly whether asking at every lock
   turned the room into an interrogation. The pushback was capped at one guess
   for exactly this reason; if the base question alone is too much, that's the
   finding that matters most.

## 6. Wrap up

- Leave the real `frontdoor-session.md` in place as the specimen.
- Write a short findings note against the six points above.
- Update the ticket bullet in `vault/00_inbox/tickets.md` with the outcome and
  date, and move it to `## Done` if it passed.
- **Any fix is prose in `SKILL.md` and/or `session-sidecar-contract.md` only.**
  The two-file change contract still holds. Anything broader is a new lift Sean
  must approve first.
- Capture any call-outs Sean makes as new ticket bullets under `## Todo` before
  wrapping, per code-brain CLAUDE.md rule 8.

## Context worth knowing

The reason this is worth testing before building anything else: the **creative
partner session skill** ticket generalizes this exact pattern — sidecar,
one-question-at-a-time, recommendation every time, a one-line why at every lock
— into a standalone skill for use beyond anima. Testing the pattern in its
first home is cheaper than discovering the flaw after a second skill has copied
it.
