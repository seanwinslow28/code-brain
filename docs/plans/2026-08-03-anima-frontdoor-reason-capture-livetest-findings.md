# anima front-door reason-capture — live-test findings (2026-08-02 → 08-03)

The first real session run against the reason-capture behavior shipped in
[anima PR #121](https://github.com/seanwinslow28/anima/pull/121). Test vehicle:
a genuine spark Sean cares about — the portfolio About-Me short ("How to Solve
a Problem") — run through the full front-door chain to an emitted, validated
brief bundle. Specimen sidecar:
`anima/briefs/2026-08-02-about-me-short/frontdoor-session.md` (18 locks, L1–L18).
Verdict up front: **the behavior passed its live test**, with two design gaps
worth a prose amendment (findings 1b and 2b) and three paths that never
triggered naturally and remain untested (findings 3, 4, 5).

## The six findings

**1. Did it ask every time? PASS, with a design-gap discovery (1b).**
No drift: every lock after the SPARK carries a captured reason — 17 of 17
through an 11-turn session, including the final locks (L15–L18), where drift
was predicted to appear. The base question was asked explicitly at L2, L3, L4,
L5, L6, L7, L8, L10, and L18.
**(1b) The volunteered-reason case is unspecified.** At eight locks (L9, L11,
L12, L13, L14, L15, L16, L17) Sean gave the reason *with* the decision,
unprompted. The skill text doesn't address this; re-asking "Why that one?"
after he just said why would have been interrogation theater. The orchestrator
chose: record the volunteered words verbatim, flag in-chat that the given line
was being taken as the reason (offering amendment). That choice worked, but it
is an improvisation, not a rule. **Candidate prose fix (needs Sean's
approval, two-file contract):** one line under the four rules — a reason
volunteered with the decision satisfies the ask; record it verbatim, don't
re-ask.

**2. Did the quote land verbatim? PASS, with a boundary note (2b).**
Spot-checkable: typos and idiosyncrasies were preserved exactly ("than that's
a successful animated film", "Tartakofsky", "they only have some much time",
"hahaha I love all of these"). No tightening, merging, or sentence-finishing
found in any of the 17 sub-lines.
**(2b) Excerpt-selection is a judgment the contract doesn't name.** When a
reason arrives embedded in a longer message (decision + reason + new ideas in
one paragraph), the orchestrator must choose *which contiguous sentences* are
"the reason." Selection was always contiguous and unedited here, but the
contract is silent on it. Worth one sentence in the contract if it ever
misfires; report-only for now.

**3. Did a skip record nothing? UNTESTED.** Sean never waved a question off —
every ask got a substantive answer. The skip path did not run. (The plan
called for deliberately waving one off; the session's momentum was real and
Sean engaged every question. Honest report over manufactured test.)

**4. Did a bare agreement record nothing? UNTESTED — and notably, the
one-guess mechanism never triggered at all.** Sean never gave a
category-grade answer ("liked B better", "felt right") in 18 locks; every
reason was substantive on the first ask. The design's motivating scenario —
"I could like an option, but not really find the reason why" — did not occur.
The guess path, the bare-agreement-records-nothing path, and the
never-guess-twice cap are all still design-only. First occurrence in a future
session should be watched for.

**5. Did SUPERSEDES get the question? UNTESTED — no supersession occurred.**
The one reversal-shaped moment (retiring the raised-arm hero pose for its
salute read-risk) amended a *proposal*, not a locked decision, so no
SUPERSEDES entry was warranted. Reported rather than manufactured, per the
ticket's instruction.

**6. How did the cadence feel? PASS — emphatically, in Sean's own words:**
"This session has been pretty damn great and the sidecar questions haven't
bothered me at all. It's really made me think deeper about WHY I want those
choices and even made me think of other routes to go. Definitely want that
moving forward."
Beyond not-annoying, the mechanism **generated story**: Sean's L4 reason ("It's
more of a comment on me and my use of AI… I always need to take a step back")
was autobiographical in a way the premise wasn't yet — surfacing it flipped
the protagonist from steady-conductor to caught-in-the-chaos, which the
stress-test reviewer later independently praised as the concept's honesty. The
why-question didn't just record a reason; it changed the film. That is the
strongest possible validation of the design hypothesis ("get the brain
churning").

## Disposition

- The behavior ships as-is; no in-session skill edits were made (per the
  execution ticket: flaws are findings, not in-session decisions).
- One candidate prose amendment for Sean to approve (finding 1b), one
  watch-item (2b), three paths to observe in future sessions (3, 4, 5) —
  tracked as a ticket in `vault/00_inbox/tickets.md`.
- The T27c creative-partner-skill generalization can proceed against this
  evidence: the pattern held under a full-length real session, and the
  volunteered-reason rule should be written into the generalized skill from
  day one.
