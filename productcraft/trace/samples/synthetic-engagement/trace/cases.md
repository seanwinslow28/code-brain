---
engagement: pc-eng-000-callboard
written: 2026-09-20
status: proposed
---

# What happened in this review

A made-up studio planned a casting tool for community theatre, and this page is the record of that planning
being checked. Two moments are worth reading closely. Early on, a check stopped the strategy over a sentence
that was never written down. Later, a check found a real hole and pointed at the wrong document as its cause.
Everything here is invented for the kit's tests: no seat wrote it, no theatre exists, and nobody was interviewed.

## Case: A check stops the strategy over something nobody wrote down

pass: pass-02
finding: 1
assist: worked
question: What was the gate actually objecting to?
options:
  - key: a
    label: The plan picked the wrong problem to solve
  - key: b
    label: The plan leaned on a belief it never stated or tested
  - key: c
    label: The plan had too many actions for its budget
sources:
  - path: audits/gate-1-r1.md
    sha256: faf32a8a08ef8407981ee1df9e8f842ac296a0e11a9df3aa45e3f40e31797d25
    excerpt: "GP-1 rests on an unstated assumption that directors control the rehearsal calendar."
    label: Finding 1 · the gate's first round
  - path: artifacts/strategy-pov.md
    sha256: 4cbcb041c5463d7ac95d0ea8dac43b7ed20f8aed0aecb74540ce8045c478805d
    excerpt: "A1 — directors control the rehearsal calendar (testable in the pilot)."
    label: What the repaired strategy says now

### Story

The studio wanted to end the scramble that eats two rehearsal weeks a season, so its first document promised
that the tool would own the rehearsal calendar and hand directors slots to accept. That promise only works if
directors are the people who decide when rehearsals happen.

Nothing in the document said so. The check read the promise, asked what had to be true for it to work, and
found a belief holding up the whole plan with nothing behind it — no interview, no register entry, no way to
be proved wrong. The reviewer graded that as serious enough to stop the document, and left two smaller notes
about wording alone.

The repair did not argue. It wrote the belief down as something to test in the pilot, split the promise into
the case where a venue shares its calendar and the case where it does not, and dropped an action that no
longer had a reason. The second round of the same check passed.

### Hint

Read the promise and ask what would have to be true about the people involved for it to work at all.

### Reveal

The objection was to an unstated, untested belief, not to the choice of problem. The gate's own words are in
the excerpt: the guiding policy rested on an assumption that directors control the calendar, and the document
never said it. That is why the repair is one line in an assumption register rather than a new strategy. Note
what you are judging here: the gate did a good job on a document that was not yet good. Those are two separate
verdicts, and only the first one is yours on this run.

### Your turn

In your own words: what would have made this a note rather than a stop?

### Terms

- guiding policy: the one approach a strategy commits to, out of the ones it could have chosen.
- assumption register: the list of things a plan needs to be true, written so each one can be tested.

### Diagram

- A promise in the plan
- ? Is what it depends on written down
- no: A stop, until someone writes it down and says how to test it
- yes: A note at most, and the test goes in the register

## Case: A check finds a hole and names the document it is standing in

pass: pass-13
finding: none
assist: independent
question: Where does the fix for this belong?
options:
  - key: a
    label: In the growth document, which set the target
  - key: b
    label: In the metrics plan one stage earlier, which has no metric to measure it with
  - key: c
    label: Nowhere yet — there is not enough evidence to say
sources:
  - path: audits/audit-growth.md
    sha256: 88b977d4935a36b6cd8d75e60dc34b2e49d2392ad4a53c4134f449a9022beeb5
    excerpt: "Stake: can every loop target be measured by the plan? No: L1 has a target and no metric, because the plan has no acquisition metric."
    label: The audit of the growth document
  - path: artifacts/metrics-evidence-plan.md
    sha256: 4c3e6cad5cbaec5f4243359b81028b7caba71f939274694cd767c8762424f530
    excerpt: "OC-3 is bounced to the Strategist as unmeasurable by this plan"
    label: The metrics plan, one stage earlier

### Story

The growth document promises a loop: a director invites the cast, and cast members become next season's
directors. It puts a number on it — thirty invites per production — which is the kind of target someone is
supposed to read off a dashboard later.

The check that follows asks one question of every loop: can the plan actually measure this? Read the two
excerpts and answer before you read on. The metrics plan written one stage earlier lists four metrics, and
none of them counts anyone arriving.

### Reveal

The auditor was right that the target cannot be read, and the reviewer of this run recorded the failure one
stage upstream: the metrics plan has no acquisition metric, so the growth seat could not have measured its
loop no matter how it wrote the target. Fixing the growth document alone would leave the hole exactly where
it is. This is the most useful line on the page when it happens — it says the work to redo is somewhere other
than the pass you are reading.

### Your turn

Write the sentence you would put in the critique, naming the evidence and the consequence.

### Terms

- loop: a way the product brings the next user in through the last one.
- first failing stage: the point in the train where the problem entered, which can be earlier than the run you are reading.
