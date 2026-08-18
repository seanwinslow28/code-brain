# The block library

Where blocks live, and how the three operations work. SKILL.md names the operations and carries the
routing rules and the two stop conditions that fire mid-run. This file has the mechanics: the file
layout, `list`'s output, and everything about `refine`.

The interview itself doesn't change. The dig rule, the per-field "Accept when:" tests, the four
stages, and both Emit gates all mean here exactly what they mean in SKILL.md. Refine reuses them; it
doesn't get its own softer versions.

---

## Where blocks live

`taste-blocks/` at the root of whatever project Wince was invoked from. One file per block, named
`<slug>.md`, where the slug is the block's name lowercased with spaces turned into hyphens. "Sunday
Pencil" is `taste-blocks/sunday-pencil.md`.

No hidden directory, no dotfile, no database. The user has to be able to find these, open them in
any editor, and copy one out without running anything.

**The file layout.** The current version is the first fenced block in the file. Everything below it
is provenance and history:

````
```
# TASTE BLOCK — Sunday Pencil
version: 2 · 2026-08-17
... the ten fields and NEVER DO ...
```

Thin fields, next pass: COLOR / LIGHT

## Previous versions

```
# TASTE BLOCK — Sunday Pencil
version: 1 · 2026-07-02
... the ten fields and NEVER DO as they stood then ...
```

Thin fields, next pass: THE HAND, COLOR / LIGHT
````

(Displayed with four backticks above so the inner fences survive. **Real files use three.**)

Four rules hold this together:

- **The file opens with the fence. Nothing above it, ever.** No title, no preamble, no frontmatter.
- **The first fence in the file is the current block, always.** Those two rules together are the
  whole lookup: read to the first ```` ``` ````, and what follows is current. Copy it, paste it into
  any model, done.
- **The thin-fields line sits outside the fence**, immediately under it, exactly as SKILL.md's Emit
  step 4 says. It's a note to the next pass, not something an image model should read.
- **Superseded versions go under `## Previous versions`, newest first, each with its own fence and
  its own thin-fields line.** Kept verbatim. Nothing is edited in place, nothing is deleted. The
  heading doesn't exist in a file at version 1; the first refine creates it along with the first
  entry under it.

**Rolling back is a manual copy, and that's deliberate.** The user scrolls down, copies the older
fence, and pastes it wherever they were going to use it. If they want it back as the current
version, they move it to the top of the file themselves; the layout is plain markdown and it's meant
to be hand-edited.

Reverting is not a fourth operation and must not be dressed up as a refine. A refine that only
restores old text spends no generations and produces no decisions, so it can't clear either gate,
and a gate-skipping path that emits a block nobody tested is the exact hole both gates exist to
close. What *is* a real refine is "go back to how it was, because X." That's an answer with a
reason, and it goes through the stages like any other.

**Why one file and not one file per version.** A directory holding `sunday-pencil.md`,
`sunday-pencil-v1.md`, and `sunday-pencil-v2.md` makes `list` guess which is current, and guessing
about which of the user's taste blocks is live is the one thing this layer exists to prevent.
History doesn't clutter the pasteable body either, because the pasteable thing was always the fence
and never the file.

Don't lean on git for this. Wince gets invoked from projects that aren't repos, and by people who
won't reach for a reflog to recover a paragraph.

---

## new

The four-stage run in SKILL.md, unchanged, plus the write. Everything about how the interview goes
is there.

Two things this operation owns:

1. **Write the file.** After Emit's acceptance tests and thin-fields line, write `taste-blocks/<slug>.md` with the
   block as the first and only fence, and the thin-fields line under it if there is one. Create
   `taste-blocks/` if it doesn't exist. Tell the user the path.
2. **Never overwrite.** If `taste-blocks/<slug>.md` already exists, stop before writing and handle
   it per the routing rules in SKILL.md. A name collision is a question for the user, never a
   silent replacement.

If either Emit gate fails, no file is written at all. A failed `new` leaves the directory exactly as
it found it.

**Exit:** the block is written at version 1 and the path is stated, or both gates are reported and
nothing is written.

---

## list

Read `taste-blocks/`, print one line per block, stop. This operation generates nothing, asks
nothing, and writes nothing. It never falls through into an interview.

One line per block, in this shape:

```
<slug>               v<n>  <first sentence of that block's CORE THESIS, verbatim>
<slug>               v<n>  <first sentence of that block's CORE THESIS, verbatim>
```

Placeholders on purpose. Don't fill this example in with the calibration answers from
[block-schema.md](block-schema.md); that file bans quoting them at users, and a sample list is still
a place a user reads them.

- **The slug**, so the user knows what to type at `refine`.
- **The version**, from the current fence's version line.
- **The first sentence of CORE THESIS, verbatim.** Never a paraphrase and never a summary. A
  paraphrase of a taste block is a different taste block, and this line is how the user recognizes
  which of their styles they're looking at. If CORE THESIS is one long sentence, print it long.

Alphabetical by slug. The user is scanning for a name they half remember, so a stable order across
sessions beats a most-recent order that moves things around under them.

**When there's nothing to list.** If `taste-blocks/` doesn't exist or holds no `.md` files, say so
and say what `new` would do. Don't create an empty directory to have something to report.

**When a file doesn't parse.** Check two things: the file opens with a fence, and that fence's first
line starts with `# TASTE BLOCK — `. If either fails, print the filename and say it doesn't parse.
Don't skip it silently, and don't go hunting for a later fence that looks better; the first-fence
rule is the whole lookup and a file that breaks it is a file to report, not to guess at. A block the
user can't see is a block they'll rebuild from scratch.

**Exit:** the lines are printed, or the empty or missing directory is reported.

---

## refine

### What refine actually runs

Four stages: **Diff, Fork, Push, Negate.** The stage it drops is Widen, and that's the only one.

Widen exists to kill dead directions before spending anything. A block that exists has already
killed them, which is what it is. Diff takes Widen's slot: same zero generations, same job of
deciding what's worth spending on, done against a block instead of against a spread.

Negate stays, and it isn't optional. It costs nothing, it owns **NEVER DO**, and the schema calls
that list the spine of the whole block. A refine that can't sharpen the ban list can't fix the field
this skill leans hardest on, which would leave the user re-running `new` every time a ban needed
adding. It also owns **5. NARRATIVE STANCE**, which only gets touched if it's on the target list.

So refine can reach any of the ten fields plus NEVER DO, **REGISTER included**. What limits it isn't
which stages run. It's the target list.

### The target list

The target list is the set of fields this refine is allowed to change. It's built once, in Diff,
from two sources:

1. **Every field the user names as changed.**
2. **Every field on the loaded version's thin-fields line.**

Everything not on the list carries forward verbatim into version 2. Not re-asked, not re-worded, not
"confirmed." Carried.

**The thin-fields line is refine's default agenda, and it's the strongest reason refine exists.**
Gate 2 lets a block ship with up to four thin fields, so a passing block can carry four surface
answers. The thin-fields line is a to-do list written by the run that ran out of budget before it
could finish. SKILL.md's degradation order already promises this: MEDIUM / SUBSTRATE, THE HAND, and
COLOR / LIGHT are told to go thin first specifically because "a refinement pass can recover [them]
from a single image later." Refine is that pass, and this is it cashing the promise.

So a refine where the user says nothing has changed is still a real refine. The thin fields are the
run. A refine with nothing changed *and* no thin fields is the no-op below.

### The second-style count, and where it gets checked

SKILL.md's refine-never-rewrites rule needs a number. Here it is, and here is why it's checked in
Diff rather than at the end.

**Count only the fields the user named as changed. Thin-field recoveries don't count.** Recovering a
thin field is the most ordinary thing a refine does, and counting those would trip the stop on a
block with four thin fields and two real changes, which is the single most typical refine there is.
A thin field going from surface to sharp isn't a different style. It's the same style, finally
written down.

Two thresholds, both computable the moment the target list exists:

- **Six or more of the ten fields named as changed.**
- **CORE THESIS and THE ONE MOVE both named as changed**, whatever the count. That's the sharpest
  signal, because those two are what Gate 2 hard-fails on and they're what the block *is*.

A third only becomes countable later: **more bans retracted than added**, checked at Negate as a
late backstop. Retractions are the quietest signal, because each one looks reasonable on its own.

**Check the first two at Diff exit, before a single generation is spent.** The target list is built
in Diff and it's sitting right there; a stop that only fires at Negate fires after the generations,
the exchanges, and the user's patience are already gone, which is the opposite of what a stop is
for.

**When the user says "yes, it's a second style."** Don't discard the run. Say what happens next:

- **At Diff exit**, nothing has been spent. The loaded block stays untouched at its current version,
  and what the user just described becomes a `new` run. Nothing is lost.
- **At Negate**, the run has already produced a fork render, an overshoot, kills, and dug answers,
  which is most of a block. The loaded block still stays untouched at its current version, and this
  run's material becomes the new block rather than being thrown away. It needs whatever the refine
  never asked for: **3. REGISTER** at minimum, since refine drops Widen. Ask Widen's field question,
  not Widen's spread; the spread exists to kill directions and this run already has a winner. Then
  fill any other field the target list never covered, and Emit it under a new name to a new file.

Either way the sentence to say is the same. They now have two blocks, and neither one ate the other.

### Diff (0 generations)

Read the file. Say back three things and no more: the name and current version, CORE THESIS in the
user's own words, and the thin-fields line if there is one. Don't recite all ten fields at them;
they wrote it, and a wall of their own text is a wall they'll skim.

Read the loaded block's MEDIUM / SUBSTRATE to yourself while you're in there. It tells you which
column of Fork's question table this person needs, which a first run gets free from Widen and a
refine has no other source for. Don't ask them what medium they work in. It's written down.

**Ask for the subject in the same breath, as a change question.** Fork's generation renders the
block against a subject and the block has no subject in it, by construction: it's style-only, and
the subject question lives in Widen, which refine doesn't run. Nobody else is going to ask, so
without this the load-bearing generation has no prompt.

> Last time we ran this on a figure at a bus stop. Same thing, or are you drawing something else
> now?

If the loaded file doesn't record what the subject was, ask it plain: what are you making pictures
of now. Either way, **the subject never fills a field.** SKILL.md's rule that it's a control
variable and not a taste answer holds here exactly as it does in Widen. What a *changed* subject
does is change how you read the miss at Fork, because a block tuned on one subject and applied to a
different one can miss for reasons that aren't the block's fault. That's the third cause in Fork's
fault separation below, and this is where you find out it's in play.

Then ask both questions in one message:

> Here's what we had. What's changed since, and what on this list still doesn't sound like you?

Build the target list from the answers, say it back, and don't spend a generation until they've seen
it. A refine that quietly decides for itself which fields are in play is a rewrite wearing a version
number.

**Users name changes, not fields.** "The results feel more decisive than they used to" is a claim
about **9. THE FINISH** and the user will never say so. Route it yourself, using the same mapping
SKILL.md uses during the interview, then say the routing back and let them confirm before it goes on
the list: "decisive is pulling against 'caught mid-decision' in your finish. Is that on the table
too?" Route it silently and you've picked which of their fields to rewrite. Don't route it at all
and the change has nowhere to land, so it turns up at Push as a surprise with no budget behind it.

**Exit:** the subject for Fork is settled, the target list exists, is non-empty, has been said back
to the user, and has been checked against the two second-style thresholds above.

### Fork (1-2 generations)

**Generate the block as it stands.** Paste the loaded version's fence in as the prompt, against the
subject settled in Diff, and show them what comes back. That image is the fork's first half, and
it's doing something a first run's Fork can't: it's a test of the block itself rather than of a
direction.

Then one question, and it carries the whole refine:

> This is your block, run as written. Where does it miss now?

**That's a verdict question and the agreeable user won't answer it.** SKILL.md is emphatic that this
user is the common case, not an edge case, and every first-run stage carries an ordering move for
them. Refine's Fork has one image, so there's nothing to rank and nothing to choose between. The
move that still works is a forced single-item ranking, which asks for a priority instead of a
complaint:

> If you could only fix one thing in this before you'd actually use it, what is it?

Nobody has to reject anything to answer that, and it yields the same thing a miss does. Reach for it
the moment the first answer is "yeah, that's pretty good."

**Then separate the fault, before you change anything.** A miss has three causes and only one of
them is refine material:

1. **The block didn't say it.** Refine material. This is the only one that spends a field.
2. **The model didn't do what the block already says.** Not refine material. The block is fine and
   the generation drifted, which is `prompt-how-much`'s job per this skill's own frontmatter
   boundary. Say which one it is and hand it off; don't rewrite a field that was already correct.
3. **The sample was unlucky.** One render is one sample. A model that ignores an instruction once
   will often honor it next time, and rewriting the block off a single unlucky draw makes the block
   worse in a way nobody will trace later.

Ask it straight, on whatever they just named:

> Before we change anything: is this the block not saying it, or the model not doing what the block
> already says?

This is [degraded-paths.md](degraded-paths.md)'s contamination hazard in a new place. That file
warns that a lone image gets reasons about *rendering* rather than about *direction*, and that the
contamination lands on CORE THESIS. Refine's Fork is structurally that case, with no control image
to compare against, so the separation has to be asked rather than inferred.

**A miss the user can't name twice is noise.** If they can't say what's wrong on a second look, or
the subject changed in Diff and the miss is plausibly about the new subject rather than the block,
leave the field alone and say why.

**Spend the second generation on a nameable dissatisfaction, not a named axis.** "It should be
looser" is enough; so is "I can't say what, but the first thing I'd fix is the lines." Gating this
on the user naming a clean axis locks the escape hatch behind exactly the answer the agreeable user
doesn't have. Make a single-dimension variant along your best reading of what they said, say out
loud which dimension you moved, and fork the two the ordinary way, same subject, same framing. If
you read it wrong, that's information too, and it's cheaper than another round of words.

Never a third. A refine that needs three pictures to find out what changed is a `new` run that
hasn't admitted it yet.

**When the target list is a single ban and nothing else**, spend the generation anyway. It's the
test that decides whether the ban is needed: if the thing the user wants to forbid shows up in the
render of the current block, the block doesn't already handle it and the ban earns its place. If it
doesn't show up, the ban is noise and the whys already on the list are covering it. That's a real
finding either way, and it's unavailable from conversation.

Refusals, sanitized returns, and transport failures behave exactly as
[degraded-paths.md](degraded-paths.md) says, including the two-attempts-per-image cap.

**Exit:** the current-state render has been seen and reacted to, and every Fork-owned field on the
target list has been asked for and dug.

### Push (1 generation)

SKILL.md's Push, unchanged, aimed at whichever image won refine's fork. Overshoot along the most
distinguishing axis, warn the user first, check the return actually went further before showing it.

One difference in what you're listening for. Version 1 already has a **9. THE FINISH**, so you're
not building a ceiling from nothing, you're finding out whether the ceiling moved. Ask the pullback
question first, then ask it against the record:

> Last time you said it stopped working once the figure wouldn't resolve. Is that still where it
> stops?

**A confirmation does not un-thin a field.** If THE FINISH was thin and the user re-confirms the
same surface answer, it's still surface and it stays on the thin list. Only a decision-level answer
takes a field off, judged by the same test in SKILL.md that would have judged it the first time.
This is the easiest mistake to make in a refine, because agreement feels like progress.

### The incumbent rule

The target list controls which fields *can* change. Nothing yet controls whether a change is an
improvement, and a refine can absolutely replace a sharp answer with a vague one: the user names a
field as changed, it gets its follow-ups, and what comes back is surface. The field was dug before
and it's thin now. Nothing was retracted and the block still got worse.

So: **when a field was dug in the loaded version and the replacement lands surface after its
follow-ups, keep the loaded answer.** Say it plainly, in the room, and don't dress it up:

> What you already have is sharper than what we just got, so I'm keeping it. We can come back to
> this.

Then count the attempt as a retraction toward the second-style backstop at Negate. A user who keeps
trying to replace sharp answers with vague ones is drifting toward a different block, and this is
the quietest place that shows up.

**One exception, and it's the honest one.** If the user says the old answer is now *wrong* rather
than merely better-phrased, don't keep it. Record the retraction with nothing in its place and let
the field go thin. That's a real subtraction, it's the path Gate 2 exists to catch, and papering
over it with a stale answer would emit a block that quietly contradicts its owner. A refine that
fails this way told the truth.

This rule is what makes the thin count in a refine actually monotone rather than merely asserted.
Without it, the gate ruling below is wishful.

**Exit:** the overshoot has been reacted to, and every Push-owned field on the target list has been
asked for and dug.

### Negate (0 generations)

Walk the kills this refine produced: what the current-state render got wrong, what the variant lost,
where the push broke. Each one becomes a new NEVER DO item in the user's own rejecting words with
its why attached, or sharpens an existing item that was pointing at the same thing without saying
why.

Then one pass over the existing list:

> Any of these you'd take back?

**Bans are additive by default.** Taste sharpens, and the ban list is the part that sharpens most
reliably, because every kill in every run adds to it and almost nothing subtracts. A retraction is a
real signal, not a normal edit. Record it, and count it toward the retraction backstop: **more bans
retracted than added trips SKILL.md's refine-never-rewrites rule**, per the thresholds above.
Incumbent-rule saves count here too.

**5. NARRATIVE STANCE** comes off the same material, but only if it's on the target list. Build the
question out of this refine's bans, never out of an example from the schema.

**The floor still holds at five items.** Since refine only adds by default this rarely bites, but a
run of retractions can drop the list under five, and that fails Gate 2 exactly as it would on a
first run.

**Exit:** every kill this refine produced has been asked about, the existing list has been offered
back once, and NEVER DO holds at least five items.

### The budget

| Stage | Generations | Exchanges |
|---|---|---|
| Diff | 0 | 5 |
| Fork | 1-2 | 7 |
| Push | 1 | 4 |
| Negate | 0 | 4 |

**At exchange 17 with Negate unstarted, stop digging and start Negate.** Same rule as the first run,
scaled: the three stages above it add to 16, so 17 means you've already overrun and the ban list is
what's about to get eaten.

Diff gets five and not three because of what it has to fit: the say-back plus the subject question
plus both diff questions (1), then one exchange per unnamed-field claim to route it and get the
routing confirmed, then the target list said back (1). A single-change answer eats three of those on
its own.

**The dig rule and its per-field cap apply unchanged: two follow-ups per field, try 3 is the last.
Eight for the whole refine.** Not six. Six was wrong, and it was wrong in the direction that breaks
the promise refine exists to keep: in a first run Fork's six cover five fields inside one stage,
while Widen, Push, and Negate each dig on top of that with no stage total at all. Capping a whole
refine at six would give an ordinary six-field list one follow-up each, which is below what the dig
rule assumes, on exactly the fields (THE HAND, COLOR / LIGHT) the degradation order let go thin
*because* a refinement pass could recover them.

**A target list over four fields gets split across two refines.** Take the user-named changes first
and leave the thin-field recoveries for the next pass, saying so out loud. Four fields at two
follow-ups each is eight, so the cap and the split agree rather than fighting: inside a split list
nothing is rationed, and the user gets two sharp passes instead of one thin one. They own a working
block the whole time, so stopping between them costs nothing.

### The gates in a refine

**Both gates run. Neither one is softer here.**

**Gate 1 counts what this refine spent, and version 1's generations don't carry.** A refine done
entirely in conversation is spec editing, and specs are the thing this skill exists to replace. The
picture is what makes a refine sharpen instead of drift: without it, the user is describing a
remembered image and you're both arguing about a block neither of you has seen run.

If the session can generate and the refine reached Emit having spent zero by choice, that's a Gate 1
failure. If it spent zero because attempts were exhausted or the session can't generate at all, run
[degraded-paths.md](degraded-paths.md)'s words-only recipe, waive the gate out loud, and mark it on
version 2's version line. Refusal and absence aren't the same thing as not bothering.

**One thing to say before a words-only refine starts.** THE HAND, THE FINISH, and COLOR / LIGHT
can't be un-thinned without a picture, for the reasons degraded-paths gives. Those three are also
the most common contents of a thin-fields line. If they're what this refine came for, say so up
front and offer to come back when generation works, rather than spending the user's afternoon on the
three fields nobody can judge from a description.

**Gate 2 runs on the whole new version, inherited fields counted. Run it. Don't reason about whether
it can fail.**

It's tempting to argue that a refine can't fail Gate 2, on the grounds that the loaded version
passed it and refine only touches the target list. That argument is false and it fails three ways:

- **A dug field can come back thinner.** The user names a field as changed, it gets its follow-ups,
  and the answer lands surface. Dug before, thin now, and nothing was retracted. A block sitting at
  the four-thin ceiling fails outright on that alone. This is what the incumbent rule above exists
  to prevent, and the rule is the reason the thin count actually holds or falls rather than merely
  being said to.
- **The ban list can shrink without a retraction.** Merging two items into one sharper item is good
  editing and it's a net loss of one. A six-item list merged twice is four, and four fails.
- **The loaded version may never have passed.** These are plain markdown files in the user's project
  and this reference tells them to hand-edit. Nothing guarantees what's on disk came out of a run
  that cleared the gate.

So the honest statement is short. **Gate 2 fails a refine when the refine loses ground**, by any of:
a field that came back thinner and wasn't caught by the incumbent rule, a retraction with nothing
put in its place, or a ban list under five however it got there. And it fails a refine when the
loaded block was already failing and the refine didn't fix it, which is worth catching rather than
inheriting.

A hard fail on CORE THESIS or THE ONE MOVE is almost always the second-style stop announcing itself
late, so check the thresholds before you report the gate.

**A failed refine is cheap, and say so.** On a first run, a failed gate means no block. On a refine,
version 1 is untouched on disk and stays current. Tell the user that in the same breath as the
failure, because the thing they're afraid of is having broken something that worked.

### The version line

**The parenthetical describes the run that made that version, never the one before it.** Never carry
version 1's parenthetical into version 2. It's a claim about a run that isn't this one, and leaving
it there is the block lying about its own provenance.

Three cases:

- **Both runs had pictures.** No parenthetical, unless this refine hit a degraded path of its own.
  `version: 2 · 2026-08-17`
- **This refine ran words-only.** Say so, and name what it couldn't test.
  `version: 2 · 2026-08-17 (refined without generated references; THE HAND and THE FINISH untested
  in this pass)`
- **The loaded version was words-only and this refine had pictures.** Carry forward only what the
  old limitation still costs. Words-only makes exactly three fields untrustworthy (THE HAND, THE
  FINISH, and COLOR / LIGHT, per [degraded-paths.md](degraded-paths.md)), so subtract whichever of
  those this refine tested and name what's left.
  `version: 2 · 2026-08-17 (refined with generated references; THE FINISH still untested)`

  **If the refine tested all three, the parenthetical goes away entirely.** Don't list carried
  INTENT fields as untested. Words-only never made them untrustworthy; a thesis doesn't need a
  picture, and a line claiming otherwise is the block being pessimistic about itself for no reason.

Plain prose on all three, per the rule in [block-schema.md](block-schema.md). Never a config token.

### The thin-fields line in version 2

**Recomputed from scratch. Never inherited.** Walk all ten fields:

- Dug to decision level in this refine: off the line.
- Was thin before, worked in this refine, still surface: stays on the line.
- **Was dug before, worked in this refine, replacement landed surface: off the line**, because the
  incumbent rule kept the sharp answer and the field is still dug. The line describes the block, not
  the attempt.
- Was dug before and the user retracted it as wrong with nothing to replace it: on the line, and
  check Gate 2, because that's a real subtraction.
- Not on the target list and thin in the loaded version: stays on the line, nothing happened to it.
- Never asked in either run: stays on the line.

If nothing is thin, the line is absent entirely. Never write it empty.

The loaded version's own thin-fields line stays exactly as it was, under its fence in the history. It
describes that version and it's still true of it.

### The no-op

If the user names nothing changed and the loaded version has no thin fields, there's nothing for
the refine to do. Don't bump the version. Say the block still stands, and offer `new` in case what
they're actually holding is a second style.

Writing a version 2 identical to version 1 is version noise, and a few rounds of it makes the
history unreadable, which is the one job the history has.

### Exit

Version 2 written above version 1 in the same file and the path stated, or a no-op reported with
nothing written, or a gate failure reported with version 1 left standing as current.

---

## When operations collide

The routing rules are in SKILL.md because they fire at invocation, before this file gets opened.
Two details that belong here:

**Fuzzy names.** If what the user typed matches more than one slug as a prefix or substring, print
the matches and ask which. Never pick the closest. Two of someone's styles can be a hyphen apart,
and refining the wrong one buries the right one's history under a version bump.

**A `new` run whose name collides at Emit.** The user names the block at Emit step 1, after the
whole interview is done, so a collision can surface at the very end. Don't overwrite and don't
silently rename. Say the name is taken, show the existing block's thesis line, and ask: is this the
same style, in which case what just ran should have been a refine, or a different one that needs a
different name. If it was the same style, don't discard the interview. Fold what just came out of it
into the existing block as a refine, which is what the run turned out to be.
