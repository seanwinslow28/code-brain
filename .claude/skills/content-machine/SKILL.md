---
name: content-machine
description: Interview-first writing orchestrator. Runs a piece from topic to shipped draft through five stages - topic, interview, shape, gates, ship - under one law, that the piece's substance (every fact, number, name, place, and event) comes only from the interview transcript, while texture is the writer's job. Use when writing anything for publication in the author's own voice, and when asked to "run the content machine", "interview me about", "write this the interview-first way", or "draft from my transcript". Not for neutral technical docs, code, or anything the author has no first-person stake in.
---

# Content Machine

The machine does not write from a topic. It interviews the author, then shapes what he actually
said. Everything below exists to keep that constraint enforced.

Background and the public/private split: [`creative-studio/content-machine/README.md`](../../../creative-studio/content-machine/README.md).
Build map: [GitHub #158](https://github.com/seanwinslow28/code-brain/issues/158).

## Runtime-impact rulings

A **runtime-impact ruling** is a ratified decision that adds, removes, changes, or moves behavior
in the live machine. It is not complete when only its ticket, map, or reference record is correct;
it is complete when every operating file that loads or enforces the behavior agrees with it.

Every runtime-impact ruling therefore has two minimum checks: a human impact inventory that names
the live consumers and verifies each required update, plus a mechanical retirement check whenever
the ruling makes an existing instruction, term, or route invalid. The mechanical check is a floor:
it can find retired vocabulary, but it cannot prove that a rule runs at the right stage.

**Scope:** the Content Machine operating surface — this skill, Content Oracle, and every skill or
file the machine directly loads or invokes. Unrelated skills elsewhere in `.claude/skills/` are
outside this check until evidence justifies widening it.

Mechanical retirement rules live in one canonical registry at
`runtime-retirements.toml` beside this file. Each record names the retirement's source decision,
scan scope, forbidden patterns, and any intentional historical mentions. Content Oracle and other
consumers are targets of this registry; they do not maintain copies of it.

The two checks run before a runtime-impact ruling is resolved: the human inventory first, then the
registry scan. Either may keep the ruling open. Knowledge Lint reruns the same mechanical scan on
Sunday as a drift backstop; it reports findings and never edits operating files automatically.

### Resolution protocol

The session making the ruling owns its propagation. Before resolving it, add this block to the
resolution comment:

```text
RUNTIME IMPACT
Ruling: <one sentence>
Operating files checked:
- <path> — updated | no change needed: <reason>
Retirement registry: <entry id added or "no retirement">
Mechanical check: clean
```

If the ruling retires an instruction, term, or route, add its entry to
`runtime-retirements.toml` before running:

```bash
python3 .claude/skills/content-machine/check_runtime_retirements.py --repo-root .
```

Every match must either be removed or declared as a narrow, reasoned historical allowance in the
registry. A broad directory exclusion is not an allowance. A missing scan target is an error, not
a clean result.

## The law

**The transcript is the only permitted source of substance. Texture is the writer's job.**

*(Re-scoped 2026-08-31 by Sean's ratification of the rules-off experiment: the Arm B
configuration scored 86% hand-rewrite survival with zero fabricated claims against the old
machine's best of 64%. Evidence and design:
[`vault/20_projects/research/2026-08-31-content-machine-rules-off-research.md`](../../../vault/20_projects/research/2026-08-31-content-machine-rules-off-research.md)
and the run-#4 ledger entries. The previous all-words form of the law is preserved in git
history; do not reintroduce it.)*

A model asked to write about a topic fills the gaps with the average of its training data —
locking **substance** to the transcript removes that failure. But a machine forbidden to write
texture can only hand back an organized brain dump; the author's own rewrites proved the best
material (images, dramatization, jokes) arrives at the writing, not the interview.

| | |
|---|---|
| **Substance — transcript-locked** | Every fact, number, name, place, event, and claim about what happened. If a fact the piece needs is missing from the transcript, leave it out or put it on the ASK LIST — never invent it. |
| **Texture — the writer's job** | Images, jokes, metaphors, comparisons, framing, the hook, the closer. Written fresh, no transcript source needed. Texture must stay consistent with what he said happened and sound like the corpus. |
| **The test** | For a claim: name the transcript line it came from; can't → cut or ask. For texture: does it contradict anything he said, and would the corpus plausibly say it that way? |

Two riders, both his: **in-band instructions bind** (his CORRECTIONS and in/out calls inside the
transcript are instructions), and **echo is not fidelity** (when new framing collides with his
spoken wording, re-say the line rather than bolting onto it — L4-06).

Professional-lane documents (resume, cover letter, questionnaire) run the **facts-only** form of the
law: every claim traces to the transcript, phrasing may be conventional. Nobody wants a resume
written in dive-bar register.

## The shaping context (standing as of 2026-08-31)

Stage 3 runs in a **clean context** — a fresh subagent that reads exactly this and nothing else:

1. The interview transcript (the story)
2. `creative-studio/content-machine/corpus/01–06` (his verbatim words)
3. `.claude/skills/writing-voice-modes/references/voice-samples.md` (the calibration authority)
4. `creative-studio/content-machine/reference-universe.md` (his cultural library)
5. `creative-studio/content-machine/do-not-promote.md` (hard constraint, not style)
6. Any prior hand-rewrite of the **same** piece, when one exists (his proven beats outrank
   fresh texture on the same beat — the run-#4 confound, L4-01)

The shaper gets the law's one substance rule, stated positively, the sentence "there are no
style rules to follow," and **the medium's deliverable form only** — the format bounds from the
contract's delivery spec (a title and length for an essay; the typed fields and word caps for a
portfolio write-up), never its register notes, roster, or move guidance. Form is task, not style. **Banned from the shaping context:** this file, `writing-voice-modes/SKILL.md`,
the anti-pattern table, the licensing matrix, the medium contracts, the gate chain, and the
lessons ledger. Voice is induced from the samples, not complied into. Rationale: instruction-count
compliance collapse plus three measured runs — see the research note. Ratified lessons reach the
shaper only when Sean routes one into the corpus or samples, or when a lesson's rider is short
enough to live in the law itself (L4-06 above).

**No autonomous revision loops.** The machine writes candidates; the author ratifies. There is no
score-until-good cycle, no persona panel, no numeric quality mean. A gate may route exactly one
grounded revise request; the author decides everything else.

**L8 binds judges, not generators** (ruled 2026-09-02). The rejected machine is one thing: personas
that *score* output and iterate to a numeric mean. Frames, lenses or personas used to **generate
candidates the author then rules on** are the sentence above, not a violation of it — that is
`creative-partner`'s divergence stage, which Sean ratified, and it never writes a fate, a lock or a
verdict. The test is whether the persona produces a *score* or a *candidate*. A candidate is legal at
any count; a score is banned at any count.

## Stages

| # | Stage | Owner | Status |
|---|---|---|---|
| 0 | **Oracle** — proposes what's worth writing: experiments he could run (frame stage + news lane) and done things from his own week (sweep), scored once into two decks | [`content-oracle`](../content-oracle/SKILL.md) | live, on probation (on-demand only until 2026-10-04); rebuilt after week 1 failed (#227, #238, #239) |
| 1 | **Topic + value gate** — one piece, one lane, one medium, named before anything else; the publication's value gate clears here as a **hard block**, never post-draft | this skill + `substack-value-engine` | live |
| 2 | **Interview** — one lens, one question at a time, read-back at the close. **X's reactive route runs no interview**: its stage 2 is a stimulus block written by `x/stimulus.py` ([#249](https://github.com/seanwinslow28/code-brain/issues/249), built [#250](https://github.com/seanwinslow28/code-brain/issues/250)) | `interview/`, `x/` | live, seven lenses |
| 3 | **Shape** — clean-context draft (see The shaping context) | fresh subagent, this skill orchestrates | live, re-scoped 2026-08-31 |
| 4 | **Gates** — post-draft, advisory: origin (claims tier), do-not-promote + coined-lines sweep, humanity scrub, critique + the analyzer **dashboard** (no metric flags since #219) | `gates/` + chain skills as reference | live, all post-draft as of 2026-08-31 |
| 5 | **Ship** — the author hand-rewrites (mandatory), a mechanical proofread runs on his final, he publishes | the author + one proofread pass | live, proofread added 2026-08-31 |
| 6 | **Lessons** — his corrections become rules, with his consent | `lessons/` + `ledger/` | live |

Stage 0 is skippable by design: a hand-picked topic is a legitimate input. Stage 6 is not skippable
once built, because a machine that never learns from his rewrites makes the same mistake weekly.

## Handoffs

Each stage emits one labeled block and consumes the one before it. The blocks are metadata; none of
them is ever part of the published text.

### Stage 1 → TOPIC CARD

```
TOPIC CARD
Piece: <one line, the thing itself>
Lane: Expressive | Professional
Medium: <which contract governs>
Why now: <what makes this worth the author's hour>
Constraints: <editorial law that binds this piece; series, order, house rules>
```

### Stage 2 → TRANSCRIPT

**Expressive lane:** stored under `creative-studio/content-machine/transcripts/` (git-ignored — it
is verbatim author).

**Professional lane:** stored beside its application, under
`vault/20_projects/prj-job-hunt-2026/applications/<date>-<company>-<role>/` (git-ignored by the
whole-directory rule on the job-hunt home). Ruled in
[#230](https://github.com/seanwinslow28/code-brain/issues/230) before the lane's first run. A
Professional transcript is facts about a named employer, not voice material — it belongs with the
letter, the ORIGIN LEDGER and the ASK LIST it produced, and it is not corpus input the way an
Expressive transcript is.

Either way, never pasted into a tracked file, an issue, or a commit message.

```
TRANSCRIPT — <slug> — <date>
Lens: <which interviewer lens>
Duration: <real elapsed time>

Q1: <question asked>
A1: <answer, verbatim, uncorrected>
...

READ-BACK
<the interviewer's summary of the story back to the author>
CORRECTIONS
<what he changed, verbatim>
```

Verbatim means verbatim. Do not tidy his grammar, complete his sentences, or drop his false starts:
the false starts are where the voice lives, and a tidied transcript quietly re-introduces the
gap-fill the law exists to prevent.

### Stage 3 → DRAFT + ORIGIN LEDGER

The draft ships with two attachments. The Voice Decision Record is `writing-voice-modes`' own
(mode, dial, moves deployed, sweeps run). The Origin Ledger is this machine's:

```
ORIGIN LEDGER
Traced: <count> vivid phrases, each to a transcript line
Untraced: <every phrase that entered the draft from somewhere other than the transcript>
  - "<phrase>" — <where it came from, and why it was kept or cut>
ASK LIST: <untraced phrases the draft is better with. One question each, for him to answer.>
  - "<phrase>" — <what the beat is doing, and the question that would get him to say it>
Verdict: clean | <n> leaks
```

Untraced does not mean "delete silently". It means show the author, so he can say the line himself
or strike it.

**The ASK LIST exists because deleting is the more expensive mistake.** On the first real run the
gate cut a flat under-reaction after a bad output ("Cool. Thanks.") for having no transcript source.
Sean put the beat back on rewrite, in his own words, better. The beat was right; only the invented
wording was wrong. A gate that silently cuts loses material the interview simply failed to reach.
So: anything the draft is genuinely better with goes on the ASK LIST as a question, not into a
diff as a deletion.

## The origin gate

**Post-draft advisory as of 2026-08-31, by Sean's ruling.** The gate is now the law's *sole
enforcement point*: the shaper composes without carrying the law as a composition-time constraint,
and the gate runs after the draft exists, producing the Origin Ledger and ASK LIST as a
traceability record. Expressive lane stays advisory (as it always was); Professional lane still
blocks on untraced claims. What changed is that the drafting context no longer holds the rule —
the research behind the move (instruction-count collapse, field practice, the craft add/never-add
boundary) is in
[`vault/20_projects/research/2026-08-31-content-machine-rules-off-research.md`](../../../vault/20_projects/research/2026-08-31-content-machine-rules-off-research.md).
The law's scope was re-ruled the same day, on the experiment's result: **claims tier only**.
Texture flags from the mechanical layer are informational; only untraced claims (numbers, dates,
names, events) are findings.

Two layers, because the law has two halves and only one of them is mechanical.

**Layer 1, mechanical** (`gates/origin_check.py`, stdlib, no model, $0):

```bash
python3 .claude/skills/content-machine/gates/origin_check.py <draft.md> <transcript.md> --lane expressive
```

It reports every atom in the draft with no counterpart in the transcript, ranked by how hard the
law is on that kind of atom. Numbers, dates, and proper nouns are **claims** (the law names them
explicitly). Everything else is an **image** at most. Connective tissue is exempt by construction,
via a stoplist, because the law already permits it.

**Layer 2, reading.** The mechanical layer cannot tell an invention from a legitimate connective
phrase, and it is blind to the whole class below. Whoever shapes the draft reads the flags, writes
the ORIGIN LEDGER, and puts anything worth keeping on the ASK LIST.

**The gate inverts where there is no transcript** (X's reactive route,
[#249](https://github.com/seanwinslow28/code-brain/issues/249), built
[#250](https://github.com/seanwinslow28/code-brain/issues/250)). A stimulus block is **never** passed
in a transcript's place: the gate clears whatever it finds in the indexed region, so pointing it at
someone else's post would license every phrase lifted from it. The block is scanned as a
**forbidden-strings** source instead, and the question becomes *is this untraceable and about him*
rather than *is this traced*.

```bash
python3 .claude/skills/content-machine/gates/origin_check.py <draft.md> \
    --stimulus <block.md> [--transcript <mini-transcript.md>]
```

**A block handed over as a transcript is refused (exit 2), not warned about.** The mistake is one
wrong path argument, it leaves no trace in the output, and the report it produces looks fine — so
the gate detects the `STIMULUS BLOCK` sentinel on line 1 and stops. The fixture pins why: index the
post text as an answer and a run lifted straight out of it comes back clean. Full rules in
`contracts/expressive/x.md`.

### What layer 1 can and cannot see

Measured against the first real run, whose leaks are pinned in `gates/test_origin_check.py`:

- **7 of 10** real inventions caught, **0** false positives on Sean's own material.
- **Blind to recombination.** All three misses were built entirely from words he did say, put
  together in a way he never did: "it had no table to get anything from" (a pun on his phrase),
  "the research, the ideas, the notes" (his word, wrong speaker), "the actual thinking". A token
  check cannot see these and never will. **Layer 2 owns recombination.** When reading, the question
  is not "is this word his" but "did he put these words in this order."
- It also caught a leak the hand-check missed: the draft had expanded his "WOL" into "wake-on-LAN",
  a word he never said.

Re-run the fixture after any change to the checker: `python3 gates/test_origin_check.py`.

### Lane behavior

| Lane | On an untraced claim | Why |
|---|---|---|
| **Expressive** | Advises. Never blocks, never rewrites. | L8. Sean ratifies; a made-up joke costs a rewrite. |
| **Professional** | **Blocks delivery** (exit 1) while any claim is untraced. | A fabricated number on a resume is a different class of harm. The block is on the document, not on his judgment: he clears it by confirming the fact or striking it. |

The gate reports. It does not revise, does not score, and does not loop.

### The one-artifact rule for coined lines

**A coined line lives in exactly one artifact and is never recycled across mediums.** Reusing the
good line is the most tempting thing the machine can do, because it already worked once. It is also
what turns a body of work into a bag of catchphrases.

Recorded in `coined-lines.md` in the private brain, git-ignored, in the same shape as the corpus so
there is one convention to remember: a `## ` heading names the artifact, every `>` line beneath it is
a coined line that artifact spent.

```bash
python3 .claude/skills/content-machine/gates/coined_lines.py <draft.md> \
    --lane expressive --artifact <this-piece-slug> [--stimulus <block.md>]
```

Stdlib, $0, no model. It catches exact reuse and the more likely case, a line lightly reworded:
below 80% token overlap a shared phrase is just shared vocabulary. `--artifact` exempts the piece's
own lines, so a draft can be re-checked as it evolves. `--stimulus` adds X's second input — the post
being answered, at the same threshold, looking sideways instead of backwards (#250). Lane behaviour
matches the origin gate: Expressive advises, Professional exits 1.

**The ledger was missing until 2026-09-05, so this gate had never once armed**
([#232](https://github.com/seanwinslow28/code-brain/issues/232), created on #250). It now exists
with the convention and Sean's unregistered backlog, and an empty ledger prints **UNARMED** rather
than "nothing to check against" — the old wording exited 0 and read, in a GATE RECORD, exactly like
a clean run. The loader also ignores fenced blocks, so the file's own worked example cannot arm the
gate with a line nobody wrote.

It runs inside the **do-not-promote sweep** rather than as a gate of its own. Both ask the same
question at the same moment: is there something in this draft that is true, and good, and still
should not be here.

### Stage 4 → GATE RECORD

One line per gate: which ran, verdict, what changed. A gate that could not run says so.

### Stage 5 → SHIP PACKET

Final text, images, frontmatter, and the open items the author has to settle himself. On an
Expressive medium with a reply surface, the **REPLY-HOOK MEMO** rides along: three lines of advice
about what would draw a reply, binding on nothing (`contracts/expressive/LANE.md`).

## Running a piece

1. Name the topic and emit the TOPIC CARD. If the medium has no contract yet, say so and write the
   piece against the lane's general rules rather than inventing a contract mid-run.
2. The **orchestrator** (not the shaper) reads the medium contract in
   `contracts/<lane>/<medium>.md` and the lane law (`contracts/<lane>/LANE.md`) for what the piece
   has to deliver — length, structural labels, the first-screen test, the reply-hook memo. Those
   requirements inform the TOPIC CARD, the interview's reach, and the post-draft check. **They are
   never loaded into the shaping context** (2026-08-31): the licensing matrix and per-move rules
   are retired from drafting entirely. The lane's **first-screen test** stays an interview
   instruction: if no beat in the transcript can carry the first screen, the interview did not
   reach far enough.
3. Interview with one lens. One question at a time. Never answer for him, never offer him a menu of
   answers to pick from, never write his line and ask him to approve it. A lens that answers its own
   questions has broken the machine as thoroughly as a draft written from nothing.
4. Shape in the clean context (see The shaping context): spawn a fresh subagent with the listed
   files, the substance rule, and nothing else. Then run the post-draft gates and hand him the
   draft with the records attached.

   **There is no gate runner, and the chain is the contract's, not this file's.** No script
   orchestrates stage 4 for any medium — the orchestrator runs each gate itself, in the order the
   medium contract states, and a contract may **trim** the chain. X drops the analyzer entirely and
   scopes critique to false authority (#249); its origin and coined-lines calls take `--stimulus`.
   The chain listed in the stage table is the default, not a floor. Whatever ran goes in the GATE
   RECORD, including what did not and why — a gate that could not run says so.
5. He rewrites by hand — mandatory, not remedial: three of four runs put his best new material
   (images, dramatization, jokes) into existence at the rewrite (L3-05, L4-02). That rewrite is
   corpus and lesson both.
6. **Mechanical proofread on his final, prose untouched** (added 2026-08-31 at his request).
   Typos, doubled words, spacing, apostrophes/escapes, punctuation only — flag each fix, change no
   phrasing, no word choice, no rhythm. His eye skips his own typos ("self depreciating" survived
   two of his finals); the pass exists to catch those, never to edit him.
7. **Register the final in the rewrite band** (added 2026-09-01, #219). One line in `SERIES` in
   `.claude/skills/writing-critique/references/build_rewrite_band.py`, under the piece's series,
   then rerun it. That band is the analyzer dashboard's second column — his rewrites, as opposed
   to his prose written outside the machine — and "recomputes on every ship" is this step. It is
   maintenance, not a ruling. The corpus band never takes a hand-rewrite; promoting prose into the
   corpus or `voice-samples.md` is a separate act and the only one that changes what gets written.

## The lessons loop

The machine learns only from what he actually changed, and only with his reason attached.

**1. Diff** (`lessons/diff_pieces.py`, stdlib, $0):

```bash
python3 .claude/skills/content-machine/lessons/diff_pieces.py <handoff.md> <final.md>
```

Sentence-aligned, not word-aligned, because a lesson is about a beat rather than a token. A reworded
sentence arrives as one change to ratify instead of six insertions and four deletions. Block-quote
markers and smart quotes are normalized away so formatting never registers as an edit he made.

**2. Propose.** The machine reads the change list and writes one candidate lesson per change into
`ledger/lessons.md` with `Status: pending`. A pending candidate has changed nothing.

**3. Ratify.** He supplies the two things the machine may not infer: **his reason, verbatim**, and a
**scope tag** (permanent rule vs one-off exception). No lesson enters any file without both.

**4. Route.** A ratified permanent lesson goes to exactly one home:

| Lesson is about | Home |
|---|---|
| How he writes | the voice guide |
| How a story is built | `storytelling-architecture` |
| How this medium works | `contracts/<lane>/<medium>.md` |
| Something never to say again | `cheese-bank/cheese-bank.md` |

The structure home was added on the first ratification (2026-08-25), when three of nine lessons
turned out to be about beat order and none of the original three homes fit. A but/therefore rule
filed in the voice guide is filed where nobody will look for it.

**A ratified lesson is not automatically a new rule.** On that same run, the lesson Sean cared most
about turned out to already exist in two skills, and the draft had broken it anyway. The honest
routing was to promote the existing rule and record that a self-run gate had missed it, not to add
a duplicate. Check whether the rule already exists before writing one.

Write the ledger entry first, then make the edit, then record the amended file back in the entry.
Ledger-first means a failed edit still leaves a record of what he ratified.

**One count rides on this route.** The move-licensing matrix is advisory in all nine mediums and
nothing enforces it ([#222](https://github.com/seanwinslow28/code-brain/issues/222)). It earns the
enforcement question back on **two ratified permanent lessons routed to a medium contract whose
reason is that a move was wrong for the room** — one is noise, two is a pattern. When the second
lands, file a fresh ticket; do not arm anything before it.

**Rejected candidates stay in the ledger.** A rejection is the more useful of the two records: it
stops the machine proposing the same wrong lesson next week. Deleting rejections means re-learning
them forever.

**Run it on Professional-lane documents too.** His edits to a resume carry the same signal, under
the facts-only form of the law.

## The private brain

Read-only inputs, all git-ignored, all local:

| Path | Read it when |
|---|---|
| `creative-studio/content-machine/corpus/` | Calibrating any claim about how the author writes |
| `creative-studio/content-machine/reference-universe.md` | The piece will use a pop-culture anchor or a personal-history detail. References come from here or from the piece's actual subject. Never invented. |
| `creative-studio/content-machine/cheese-bank/` | Before shipping any Expressive draft |
| `creative-studio/content-machine/coined-lines.md` | Every piece, at the final sweep. The one-artifact rule: a coined line lives in exactly one artifact and is never recycled. |
| `creative-studio/content-machine/do-not-promote.md` | Every piece, at the final sweep |
| `creative-studio/content-machine/transcripts/` | The interview record for **Expressive** pieces, and later corpus. Professional-lane transcripts live with their application under `vault/20_projects/prj-job-hunt-2026/applications/` instead (#230). |
| `creative-studio/content-machine/stimulus/` | X's stage-2 blocks (#250). **Opposite polarity to a transcript** — forbidden strings, never permitted vocabulary — which is why it is a separate directory and why the origin gate refuses a file carrying the `STIMULUS BLOCK` sentinel. Never merge the two. |
| `creative-studio/content-machine/watchlist.md` | The accounts X's route-1 sweep reads, in three lanes (#251). Per-machine: a fresh clone and the Mac Mini have none, and `x/stimulus.py` refuses to sweep nothing rather than reporting clean. Lane C is admitted **by eye, never by metric** — the first harvest ranked an antisemitic account top on every number available. |
| `creative-studio/content-machine/ledger/` | Ratified lessons |
| `creative-studio/content-machine/ideas-bank.md` | Every Oracle run, **before** scoring — a thin spike from three weeks ago may have an ending now |

Nothing from these paths is ever quoted into a tracked file, a GitHub issue, or a commit message.
The repo is public.

## Related skills

- `writing-voice-modes` — **no longer Stage 3 drafting context** (2026-08-31): the shaper induces
  voice from `references/voice-samples.md`, which that skill remains custodian of. The skill itself
  stays live for standalone voice asks (dial work, recruiter-safe swaps) outside the machine.
- `storytelling-architecture` — beat map. Owns story order.
- `substack-value-engine` — the value gate. Owns whether the piece is worth a reader's time.
- `writing-critique` — adversarial gate. Never rewrites; routes one grounded revise.
- `writing-humanity-pass` — final scrub. Owns the AI-tell sweep and the no-em-dash rule.
- `content-oracle` — Stage 0. Three supplies (sweep, news lane, frame stage), one scoring pass, two
  decks: worth a piece this week, worth posting. A card names an experiment he could run, or a done
  thing with an artifact behind it; it never asserts he did something he did not.
- `grilling` — when the author wants the *plan* stress-tested rather than the story drawn out.
