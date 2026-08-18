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

Three rules hold this together:

- **The first fence in the file is the current block, always.** That's the whole lookup. Copy the
  first fence, paste it into any model, done.
- **The thin-fields line sits outside the fence**, immediately under it, exactly as SKILL.md's Emit
  step 4 says. It's a note to the next pass, not something an image model should read.
- **Superseded versions go under `## Previous versions`, newest first, each with its own fence and
  its own thin-fields line.** They're kept verbatim. Nothing is edited in place, and nothing is
  deleted.

That's what "keep the old one" means operationally, and it's the whole rollback story: the user
scrolls down, copies the older fence, and pastes it. If they want it back as current, that's a
refine that says "go back to how it was," which is a real answer with a real reason behind it.

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

1. **Write the file.** After Emit's four numbered steps, write `taste-blocks/<slug>.md` with the
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
sunday-pencil        v2   The held breath before emergence.
loud-saturday        v1   A Saturday morning cartoon that got out of hand.
```

- **The slug**, so the user knows what to type at `refine`.
- **The version**, from the current fence's version line.
- **The first sentence of CORE THESIS, verbatim.** Never a paraphrase and never a summary. A
  paraphrase of a taste block is a different taste block, and this line is how the user recognizes
  which of their styles they're looking at. If CORE THESIS is one long sentence, print it long.

Alphabetical by slug. The user is scanning for a name they half remember, so a stable order across
sessions beats a most-recent order that moves things around under them.

**When there's nothing to list.** If `taste-blocks/` doesn't exist or holds no `.md` files, say so
and say what `new` would do. Don't create an empty directory to have something to report.

**When a file doesn't parse.** If a file's first fence isn't a block, print its filename and say it
doesn't parse. Don't skip it silently. A block the user can't see is a block they'll rebuild from
scratch.

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
2. **Every field on version 1's thin-fields line.**

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

### Diff (0 generations)

Read the file. Say back three things and no more: the name and current version, CORE THESIS in the
user's own words, and the thin-fields line if there is one. Don't recite all ten fields at them;
they wrote it, and a wall of their own text is a wall they'll skim.

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

**Exit:** the target list exists, is non-empty, and the user has seen it.

### Fork (1-2 generations)

**Generate the block as it stands.** Paste version 1's fence in as the prompt, against the user's
current subject, and show them what comes back. That image is the fork's first half, and it's doing
something a first run's Fork can't: it's a test of the block itself rather than of a direction.

Then one question, and it carries the whole refine:

> This is your block, run as written. Where does it miss now?

The miss is the material. Everything downstream comes off it.

**Spend a second generation only when the user names an axis and words won't settle it.** Then make
a single-dimension variant along that axis and fork the two the ordinary way, same subject, same
framing. Never a third. A refine that needs three pictures to find out what changed is a `new` run
that hasn't admitted it yet.

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
real signal, not a normal edit. Record it, and count it toward the second-style stop in SKILL.md.

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
| Diff | 0 | 3 |
| Fork | 1-2 | 7 |
| Push | 1 | 4 |
| Negate | 0 | 4 |

**At exchange 15 with Negate unstarted, stop digging and start Negate.** Same rule as the first run,
scaled to a shorter one: the three stages above it add to 14, so 15 means you've already overrun and
the ban list is what's about to get eaten.

The dig rule and its per-field cap apply unchanged: two follow-ups per field, try 3 is the last.
**Refine gets six follow-ups total across its whole target list**, the same shape as Fork's six in a
first run, and for the same reason. Spend them on the fields the user named as changed first, then
on the thin ones. A refine that spends twelve questions re-litigating a block the user already has
is the interrogation the dig rule exists to prevent, and here they can walk away and still own a
working block.

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

**Gate 2 runs on the whole of version 2, inherited fields counted, and it cannot fail on inheritance
alone.** Version 1 passed it, so version 1 held at most four thin fields with CORE THESIS and THE
ONE MOVE dug and five or more bans. Refine never un-digs a field it doesn't touch, and a field it
does touch either gets dug or stays where it was. The thin count can only hold or fall.

So Gate 2 fails a refine in exactly one way: **the refine subtracts.** A retracted answer with
nothing put in its place, or bans dropped under five. If the user pulls CORE THESIS or THE ONE MOVE
and doesn't replace it, that's the hard fail, and it's usually the second-style stop announcing
itself late.

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
- **Version 1 was words-only and this refine had pictures.** The fields the refine touched are
  tested now. The ones it carried are still untested, and the line has to name which.
  `version: 2 · 2026-08-17 (refined with generated references; REGISTER and NARRATIVE STANCE carried
  untested from a words-only version 1)`

Plain prose on all three, per the rule in [block-schema.md](block-schema.md). Never a config token.

### The thin-fields line in version 2

**Recomputed from scratch. Never inherited.** Walk all ten fields:

- Dug to decision level in this refine: off the line.
- On the list, worked, still surface: stays on the line.
- Not on the target list and thin in version 1: stays on the line, because nothing happened to it.
- Never asked in either run: stays on the line.

If nothing is thin, the line is absent entirely. Never write it empty.

Version 1's own thin-fields line stays exactly as it was, under version 1's fence in the history. It
describes that version and it's still true of it.

### The no-op

If the user names nothing changed and version 1 has no thin fields, there's nothing for the refine
to do. Don't bump the version. Say the block still stands, and offer `new` in case what they're
actually holding is a second style.

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
