---
name: wince
description: Interview someone's visual taste out of them by showing options and reading their reactions, then emit a reusable taste block they can paste into any image model. Use when asked to "figure out my style", "build my taste block", "what's my aesthetic", "the model won't draw like me", "make it look like mine", "run the taste interview". Also owns the block library, so use it for "what taste blocks do I have", "list my blocks", "refine <name>", "update my taste block", "my style has changed since I made this". If someone is stuck arguing an image toward what they want one adjective at a time, offer it, do not start the interview unasked. USER-INVOKED — do not invoke from another skill. Not for generating final art (use the image-gen skills); not for prose voice (use writing-voice-modes); not for fixing a single prompt or a drifted generation (use prompt-how-much).
---

# Wince

It shows you things, reads which ones you wince at, and writes the block that makes the machine draw like you.

## The one rule that makes this work

Every keep and every kill has to produce a reason **at the decision level**, not the surface level.

> **Surface:** "I love the texture and the grain."
> **Decision:** "I want the process to stay visible. The sketch marks aren't mistakes, they're evidence of thought. It's visual proof that art takes time."

The second one is portable. It tells a machine what to do in a situation the user never described. The first one does not.

Same on the negative side. Every ban carries its why, and the why is the negative of a value the keeps demonstrated:

> **Never do:** polished, surface-perfect rendering that erases the hand.
> **Why:** everything I love keeps the fingerprints in. A flawless surface means the process was hidden or never happened.

Never accept a bare preference. When someone says "I like that one," ask what decision the maker made. Keep going one level down until the answer would still be useful applied to a different subject. Two follow-ups is usually enough; four is an interrogation and people quit. If the third try still lands on surface, record the surface answer, mark it thin, and move on. A thin field is honest. A fabricated one is not.

### The test, run on every answer before you record it

Take the answer and apply it to a subject the user never mentioned. A dog at a bus stop, a kitchen at 2am, anything far from what's on screen. Now imagine two competent images of that subject. If the answer lets you reject one of them, it's a decision. Record it. If it only lets you add something to both, it's surface. Ask again.

Pick the pair the answer would have the hardest time telling apart, not the easiest. Two images that both already do the thing the answer names is the honest test. An answer that can only beat a foil nobody would have made hasn't chosen anything.

### Counting the tries

The user's first answer about a field is try 1 for that field. Every follow-up you ask about that field produces its next try. You get at most two follow-ups, so try 3 is the last. The count runs per field and resets when you move on. If an answer lands on a different field than the one you're digging, credit it there as that field's try 1 and leave the current field's count where it was. If the user dodges twice without landing on any field, that counts as your two follow-ups spent.

### How to ask the follow-up

Point at their own words and ask what choice the maker made to get that. "What is the grain doing for you that a clean surface wouldn't?" beats "can you say more?" Say back what you heard in their words before you ask again, so it reads as interest rather than doubt. Ask about the decision, not about their feelings. "Not about their feelings" means don't ask how it made them feel; asking what it reminds them of, or what would ruin it, is fair game and usually faster. Never hand them an answer to pick from, for the reason given in the examples guard in [references/block-schema.md](references/block-schema.md).

### Marking a field thin

Record the user's own words as the answer, with no marker inside the block. Track the thin fields outside the block body, after the closing NEVER DO section, as `Thin fields, next pass: <field names>`. The block itself has to survive being pasted into an image model, and a parenthetical that model doesn't understand is a parenthetical it will try to draw.

Never list a field the user did dig, and never fill a thin field with a plausible answer of your own.

### Where this rule stops

This rule governs the conversation. The schema's per-field "Accept when:" tests judge the finished answer, and they are stricter. When one of them fails, check why. If the decision is in what the user said and only the phrasing is loose, tighten the phrasing and move on. If it fails because information the user never gave is missing, that is not a wording job. Go back and ask, and it spends a try like any other. Never close that gap yourself.


## Three operations

Wince runs one of three things, and which one it is gets settled before the interview starts.

| Operation | Runs when | What it does | Exit when |
|---|---|---|---|
| **new** | the user asks to build one, and the name they give has no file yet | The full four-stage run below. | The block is written to `taste-blocks/<slug>.md` at version 1 and the path is stated, or a gate failure is reported and no file is written. |
| **list** | the user asks what blocks they have | Reads `taste-blocks/` and prints one line per block: slug, version, and the first sentence of its CORE THESIS verbatim. | The lines are printed, or the empty or missing directory is reported. Generates nothing, asks nothing, writes nothing. |
| **refine `<name>`** | the user asks to change one they already have, and the name has a file | Loads the block, runs it as a picture, digs only what changed and what was thin, bumps the version, keeps the old one in the file. | The next version is written above the old one and the path is stated, or a no-op is reported and nothing is written, or a gate failure is reported and the existing version is left standing as current. |

**Blocks live in `taste-blocks/` at the root of whatever project Wince was invoked from**, one file
per block, named `<slug>.md`. No hidden directory, no dotfile. The user has to be able to find these
and copy one out without running anything. The current version is the first fenced block in the
file; superseded versions sit below it under `## Previous versions`, kept verbatim. Full layout in
[references/library.md](references/library.md).

**Never let one operation become another quietly.**

- `refine` on a name with no file is not a `new` run. Say the name doesn't exist, list what does, and
  offer to start one.
- `new` with a name that's already taken is not a `refine`. Say so and ask, per the collision
  handling in the reference. Never overwrite a file.
- A name matching more than one block gets a question, never a guess.
- `refine` with no name at all is the common phrasing and it isn't an operation. Run `list`, ask
  which one, then refine that. If the directory holds exactly one block, still name it back before
  you start, because the user may be thinking of a block they made somewhere else.
- `list` never falls through into an interview.

**Refine is a different stage shape, not the four stages run again**, and it runs both Emit gates on
its own generations. Don't run one out of this file; the mechanics are all in
[references/library.md](references/library.md).

### Refine never rewrites a block from scratch

Taste sharpens; it rarely reverses. Load what exists, ask what has changed since, and edit. A refine
that produces a completely different block means the user has a second style, not a revised one. Say
so and offer to make a new one instead.

**When to say it** is a counted thing, checked at the end of Diff before any generation is spent and
again at Negate as a backstop. The thresholds and the arithmetic are in the reference, because both
are computed off the target list and neither is available here.

Ask it plainly and let the user decide:

> This is turning into a different block rather than a sharper one. Do you want to keep the old one
> as it is and start a second style, or is the old one genuinely wrong now?

Both answers are fine. What's not fine is landing on a second style by accident and losing the first
one to a version bump.

## The four stages

These four are `new`. Refine reuses them per the reference; `list` runs none of them.

Four stages, then Emit. A full run finishes in under ten minutes and spends three or four
generations. Widen and Negate spend zero. Fork spends two or three. Push spends exactly one.

| Stage | Job | Generations | Exit when |
|---|---|---|---|
| **Widen** | Five named directions in words, deliberately far apart. Kill the dead ends before spending anything. | 0 | At least three of the five are dead, and REGISTER has been asked for and dug. |
| **Fork** | Generate the survivors against the user's real subject. Pick one, then dig. | 2-3 \* | One direction is chosen with a decision-level reason, and all five fields Fork owns have been asked for and dug. |
| **Push** | Overshoot the winner on purpose so the user pulls it back. | 1 \* | The user has named a ceiling that passes the test below, and all three fields Push owns have been asked for and dug. |
| **Negate** | Walk back through every kill and ask why it was wrong. | 0 | Five to ten banned items each carrying its why, and NARRATIVE STANCE has been asked for and dug. |

\* These counts assume the session can generate images and that the generations land. A refused or
sanitized generation moves them in both directions: Push can deliver zero, and a sanitized return
burns a generation that never reaches the user. A session with no image capability at all spends
zero throughout and runs a different recipe. All of it is in [references/degraded-paths.md](references/degraded-paths.md).

**What "asked for and dug" guarantees, and what it doesn't.** It guarantees you actually put the
question to the user and followed the rule above before recording anything. It does not guarantee
the answer is any good, because a field marked thin satisfies it too. That is deliberate. Quality
has one floor and it sits at Emit, where both gates run. Don't treat a stage exit as evidence the
block is working.

### The user who likes everything

Most of this section assumes someone who will tell you a thing is bad. Plenty of people won't. In a
taste interview the agreeable user is the common case, not an edge case: you are a stranger showing
them work and asking them to pass judgment on it, and the reflex is to be nice. "Yeah, that one's
good" to all five directions. "That's cool too" to the deliberate overshoot.

Every gate here leaks under that user, so each stage carries a move for it and the moves all work
the same way. **Stop asking for a verdict and ask for an order.** Ranking, choosing between exactly
two, and naming what they'd regret losing are all easy for someone who finds rejection rude, and
they yield the same information a kill does. The stages below mark where to reach for this.

If the moves fail too, the run does not quietly produce a block anyway. It fails at Emit and says
what it couldn't get.

### The budget you can actually count

You have no clock. In a turn-based interview you can't observe wall time between turns, so run the
budget in **exchanges**, where one exchange is one user message plus your reply.

| Stage | Exchanges |
|---|---|
| Widen | 6 |
| Fork | 13 |
| Push | 6 |
| Negate | 8 |

**At exchange 26 with Negate unstarted, stop digging and start Negate.** That number is derived,
not picked: the three stages ahead of Negate sum to 25, so 26 is exactly where Negate should be
opening anyway. Ten minutes is the target and this is how you hit it.

Widen gets six rather than five because the agreeable path is the common path, and it structurally
costs one failed ask plus one reoffer before the forced ranking lands. Budgeting for the rare
cooperative user and calling the normal one an overrun is how a budget starts lying to you.

When you have to degrade, degrade in this order rather than letting everything go thin at once:

1. **Protect CORE THESIS and THE ONE MOVE.** Emit hard-fails if either is thin, so spending your
   last follow-ups anywhere else is spending them on a block that won't ship.
2. **Let MEDIUM / SUBSTRATE, THE HAND, and COLOR / LIGHT go thin first.** They're the three most
   likely to be thin anyway, and they're the three a refinement pass can recover from a single
   image later.

### Which stage owns which field

| Field | Owner | Why that stage can actually answer it |
|---|---|---|
| 3. REGISTER | Widen | The spread crosses register on purpose, so a kill is a position on the scale. |
| 1. CORE THESIS | Fork | The decision-level reason the winner won is what the thing should feel like before it announces itself. |
| 2. EMOTIONAL MODE | Fork | The loser is a direction they liked enough to keep through Widen and then gave up after seeing it. That's a real sacrifice, which is what the OVER clause needs. |
| 6. MEDIUM / SUBSTRATE | Fork | Same subject, different directions. Substrate is the first thing that visibly differs. |
| 7. THE HAND | Fork | You can point at the marks in a specific image and ask what made them. |
| 8. COLOR / LIGHT | Fork | Counts and bans come from looking. Nobody says "exactly one accent" from memory. |
| 4. STRUCTURE | Push | The overshoot is the only image the user has to triage, and STRUCTURE is the field that has to name what gets cut. |
| 9. THE FINISH | Push | The ceiling the user names is a finish boundary. That's what Push is for. |
| 10. THE ONE MOVE | Push | When everything else goes wrong at once, the thing they still protect is the one move. |
| 5. NARRATIVE STANCE | Negate | The whys pile up into forbidden routes to meaning. Ask for the positive route while the negatives are on the table. |
| NEVER DO | Negate | Bans come from real kills, and by Negate every kill in the run is on record. |

Owning a field means that stage is responsible for coming back with it. It doesn't mean the answer
can only arrive there. Under the rule above, an answer that lands on a different field gets credited
to that field wherever it turns up, and the owning stage confirms it rather than asking again from
scratch. What you must never do is fill a field nobody asked about.

One routing note, because it comes up unprompted and early: when a user volunteers what color is
*for* ("the color carries the whole feeling, it never decorates"), that's a claim about how meaning
reaches the viewer. Hold it for **5. NARRATIVE STANCE** two stages later. Only the count and the
bans belong to **8. COLOR / LIGHT**.

---

### Widen (0 generations)

**Before anything else, check that this session can generate images at all.** If it can't, say so
now rather than at Fork, and run the whole interview on the words-only recipe in
[references/degraded-paths.md](references/degraded-paths.md). Announcing it late costs the user four
stages of work on a promise you knew you couldn't keep.

Then ask one line: what are you going to be making pictures of? You need it for
Fork. If they don't have one, pick a subject, say you're picking it, and keep it fixed. The subject
is a control variable, not a taste answer, so choosing it for them costs nothing.

Note what they make them **in**, too. You get this free from the five directions and their
reactions, and Fork can't phrase half its questions without it. Drawing and painting, camera work,
or synthetic. It's not a field and you don't dig it.

Then say roughly this:

> I'm going to name five directions. They're deliberately far apart and most of them are wrong.
> Tell me which ones are out. Don't be polite about it.

Name five. One line each, no images. Each line names its **medium**, its **finish**, and its
**register**. The spread has to cross all three, not run five flavors of one look. The check is
mechanical: no two of the five may match on more than one of those three axes. If two do, one of
them is filler and you have four directions, not five.

Ask why each kill is a kill, and dig it per the rule above. Kills are cheaper to explain than keeps
and they carry more, so this is where the interview is fast when it is fast at all.

Record **3. REGISTER** before you leave. That is Widen's only field. Widen used to own EMOTIONAL MODE
as well and no longer does, because reading two independent axes out of one set of kills is how they
get collapsed, and the schema is emphatic that they are independent. If a kill reads as "too much" or
"too loud" rather than "too stylized," that's an emotional-mode signal and it belongs to Fork.
Note it, don't record it.

**When the kills don't come.** If fewer than three die, the spread was too narrow. Replace the
near-duplicate survivors with sharper opposites, once, and ask which of these is closest to
something they'd never make. If all five die, ask what all five got wrong, then offer three new ones
built out of that answer. One reoffer either way.

**When the second round still produces no kills, stop asking for kills and force a ranking:**

> Rank all five, worst first. You don't have to hate any of them, I just need the order.

Ranking is far easier than rejecting for someone who doesn't want to be rude, it costs nothing, and
the bottom three of a ranking are your kill list. Dig them exactly as you would dig a kill: "what
puts that one last?"

Only if the ranking is refused too may Widen exit thin, and when it does, say so out loud:

> Nothing's been ruled out yet, so the block we end up with is going to be vague. I'll keep going,
> but I'm going to push harder on the next few.

A thin Widen still has to hand Fork two directions. Pick the two furthest apart yourself, say you're
picking them and why, and mark **3. REGISTER** thin. Choosing which two get drawn is a control
decision like choosing the subject. Choosing what the user thinks of them is not.

### Fork (2-3 generations)

**Read the EXECUTION preamble in [references/block-schema.md](references/block-schema.md) before you
ask Fork's first question.** That preamble is where MEDIUM / SUBSTRATE and THE HAND get mapped out
of drawing vocabulary and into camera and 3D vocabulary. Fork is the only stage that asks about
either one, so it is the only stage that needs the mapping, and it needs it before it opens its
mouth rather than after a question has already landed wrong.

At most two directions survive Widen, so generate one image per survivor. If only one survived,
generate it and then generate one variant that changes a single dimension of it, because a fork with
one image in it is not a fork. Either way that's two. Same subject every time, same framing every
time, so the delta reads as style and not composition. Say that out loud:

> Same subject, one version per direction. The only thing changing is style, so whatever you
> react to is style.

Spend a third generation only to break a tie the user can't break in words, or to split a winner
they liked in halves. Never a third for tidiness. Four is not available at this stage.

**If either image is refused, times out, or comes back not doing what you asked**, stop and read
[references/degraded-paths.md](references/degraded-paths.md) before your next move. Do not run the
fork on the one image that survived. Never a third attempt on the same image, and a reword is not a
new attempt.

**When they like both**, don't ask again in the same words. Force the binary, which is the easiest
question in the whole interview to answer:

> You only get one. Which one is going in the block?

If they still won't choose, choose for them, say out loud that you're choosing and that it weakens
the block, and mark **1. CORE THESIS** and **2. EMOTIONAL MODE** thin. Push needs a winner to
overshoot, so the run continues. It will not survive the Emit gate, and it shouldn't.

**Fork owns five fields and gets six follow-ups total across all of them**, not two each. The
per-field cap in the rule above still applies as a ceiling, but patience doesn't reset when you
change subject, and twelve questions in one stage is the interrogation that rule exists to prevent.
Spend the six on CORE THESIS and EMOTIONAL MODE first. MEDIUM / SUBSTRATE, THE HAND, and
COLOR / LIGHT absorb the shortfall and go thin.

**Two fields come off the pick, and they come from opposite sides of it.**

- **1. CORE THESIS** comes from the winner. Ask why that one, and dig until the reason would still
  be useful on a subject that was never on screen. Fork may exit with this provisional. Negate
  sharpens it, because a thesis with five bans around it has edges a thesis alone doesn't, and
  forcing it closed inside Fork's clock is how it goes thin for no reason.
- **2. EMOTIONAL MODE** comes from the loser. The loser is not a discard, it's a thing they kept
  through Widen, saw drawn, and then gave up. That's the sacrifice the OVER clause needs. Ask it
  straight:

  > The other one made it this far. What did it have that you're now giving up?

  Do not offer them the two halves and ask them to nod. "So you're giving up X to get Y" is you
  writing the field. If the answer names how literal it looks rather than what it favors, that's
  REGISTER again and it's already recorded, so ask again.

  **Check before recording:** these two must come from different sides of the pick. If both are the
  same sentence about the winner, you have one answer wearing two hats, and the second one is thin.

**Then work the picture in front of you** for the other three. Point at the image, not at
categories.

**Ask in the medium the person actually works in.** The question underneath is identical in all
three columns below; only the noun changes. Ask a video editor what made the marks and you get "what
marks, it's a camera," and you've spent an exchange teaching them your vocabulary instead of
learning theirs.

| Field | Drawing and painting | Camera work | Synthetic (3D, motion, vector) |
|---|---|---|---|
| **6. MEDIUM / SUBSTRATE** | "What is that surface, if you had to go buy it?" | "What was it shot on, and what has it been through since?" | "What's rendering this, and what gives it away as rendered?" |
| **7. THE HAND** | "What made those marks?" | "What did the camera do that a better camera wouldn't?" | "What did you have to do to those surfaces to stop them looking like the default?" |
| **8. COLOR / LIGHT** | "How many colors are allowed in here, and which one is never allowed?" | "How many sources are lighting this, and what is never allowed to be lit?" | "How many colors in the palette, and which one is never allowed?" For 3D, count the rig instead. |

COLOR / LIGHT is the one that misfires quietly rather than loudly. Asked about colors, a camera
person answers "however many are in the shot, I don't pick colors, I point at stuff," which is a
sane answer to the wrong question. The rule underneath is **count the thing this person actually
chooses**. A painter chooses pigments. A photographer chooses lights, and the shadow rule tends to
arrive with the count in the same breath. Whichever you count, the field still needs a number, an
"only," or a "never" to be worth recording.

If none of the three columns fit, and plenty of media don't, don't jam them into one. Build the
question the way the preamble does: name the thing they physically control, then ask what they do
with it and what they refuse to do with it.

**THE HAND goes thin more than any other field**, because its test demands a tool or a specific
behavior and most people's first three answers are a mood. "Loose" and "sketchy" are the schema's
weak example word for word. The fallback needs no vocabulary from them, and it has to stay clear of
medium words too: point at one region of the generated image, small and specific, and ask what had
to happen for *that bit* to come out like that. They can answer that without knowing what any of it
is called, and without owning a pencil.

### Push (1 generation)

Push always spends its generation. It may take Fork's winner as the input image and go further from
there, which is what "reuse" means here. It never means skipping the generation, and the one case
where Push spends zero is below, once the image is back.

Overshoot the winning direction along its own most distinguishing axis. More of the thing that made
it win, too much of it, on purpose. Tell the user that's what you're doing before they see it:

> This next one goes too far on purpose. It'll probably be ugly. Tell me where it broke and pull me
> back.

**Push is the stage most likely to be refused, and refusal is not the only way it fails.** Before the
image goes on screen, check it actually went further along the axis you just named. If it came back
tamer than Fork's winner, or the same, that's a soft refusal even though nothing was declined, and a
pullback measured against it measures nothing. On a refusal, a soft refusal, or a failure to arrive,
stop and read [references/degraded-paths.md](references/degraded-paths.md) before your next move.
Never a third attempt on the same image, and a reword is not a new attempt.

Then read the pullback. Three things come out of it and you ask for each one:

- **9. THE FINISH.** "Where exactly did it stop being right?" The ceiling, stated as a boundary.
- **4. STRUCTURE.** "What would you cut out of that?" A structure rule that deletes nothing is
  decoration, so keep asking until something gets deleted.
- **10. THE ONE MOVE.** "In all that mess, what's the one thing still worth keeping?" One move, not
  a list. If they name three, ask which one they'd protect when the three fight.

**What counts as a ceiling.** A ceiling counts when the user has named a point past which the image
is wrong, in words that would let a stranger reject an image neither of you has seen. "That's too
much" is not one. "It stopped working once the figure wouldn't resolve" is. Liking the overshoot
doesn't fail Push, but it doesn't pass it either, because "actually that's better" gives you nothing
to write into THE FINISH.

Push has one generation and doesn't get a second, so when the picture doesn't produce a ceiling, ask
for the boundary in words instead:

> Forget this one. What would I have to do to that image to actually wreck it?

If that doesn't land either, mark **9. THE FINISH** thin and move. Do not record a ceiling the user
didn't name.

**Why Push is not optional.** Push is the only stage that finds something the user did not know to
ask for. Every other stage narrows what they already brought. Cut it and this becomes an interview
about a spec, which is the thing that does not work.

### Negate (0 generations)

No images. Walk back through everything killed in Widen, Fork, and Push, in order, and ask why each
one was wrong. You have the list already: three or more Widen kills or the bottom of the ranking,
one or two Fork losers, and whatever broke in the Push image.

> Back to the ones you killed. This one, early on. What was actually wrong with it?

Each answer becomes a NEVER DO item in the user's own rejecting words, with its why attached, and
the why is the negative of a value the keeps demonstrated. Five to ten items. Fewer than five means
you're taking bans at face value and not asking why. More than ten and the list stops generalizing
and starts being a log.

**If the kills don't reach five, don't invent the rest.** Restate the negative half of fields you
already recorded: the finish ceiling from Push, the color count from Fork, and the one move all
carry a ban on their far side, and the schema wants those bans written here anyway. Restating a ban
is not redundancy. Inventing one is.

**If it still won't reach five after that, Negate has failed and you say so.** Do not pad the list
to hit a number. Report the count you actually got, carry it to Emit, and let the gate there fail
the run. A short ban list is the single loudest signal that the interview stayed on the surface,
which is exactly what the gate is for.

**5. NARRATIVE STANCE** comes out of the same material while it's on the table. Look at the bans you
just wrote, find a route to meaning that they close off, name that route back to the user, and ask
where the meaning goes instead. Build the question out of this run's bans, never out of an example
from the schema file, or you'll be handing them somebody else's taste to agree with. Ask it, don't
derive it. Inverting a ban yourself is filling in a field for them.

A closing principle is welcome as a last line, and it doesn't replace the per-item whys.

---

### Emit

Two gates run before anything is emitted. They fail the same way and for the same reason.

**Gate 1, no pictures.** If image generation was available in this run and Emit is reached with zero
generations spent, the run failed. A block built from words the user never tested against a picture
is a spec, and specs are what this skill exists to replace. In a declared words-only run this gate is
waived rather than passed, and the block says so on its version line. If this run generated nothing,
or generated less than it meant to, read
[references/degraded-paths.md](references/degraded-paths.md) before you fail it or emit it.

**Gate 2, no decisions.** If more than four of the ten fields are thin, or if CORE THESIS or THE ONE
MOVE is thin, or if NEVER DO holds fewer than five items, the run failed the same way a
zero-generation run failed. Three generations were spent and nothing was decided, which is the more
likely of the two failures and the quieter one.

On either gate: say so plainly, name exactly what you could not get, and offer to re-run Fork with
harder options. Do not emit a block. A re-run is a fresh run with a fresh budget, and say that too,
so three generations don't quietly become six.

Otherwise, emit the block exactly per the template in
[references/block-schema.md](references/block-schema.md). Then:

1. **Name it.** Ask the user. The name names the style, not the person, because they'll have more
   than one. If they shrug, offer two names built out of their own words and let them pick. If the
   name is already taken in `taste-blocks/`, don't overwrite and don't rename it yourself; handle it
   per the collision rules in [references/library.md](references/library.md). **A refine skips this
   step.** The block is already named, the slug is the filename, and renaming at Emit orphans the
   file the user just refined.
2. **Stamp `version: 1 · <today's date>`.** Version 1 on a first run. Refinement bumps it.
3. **Run the ten "Accept when:" tests** from the schema against the ten answers before the block
   goes on screen. When one fails, handle it per "Where this rule stops" above: loose phrasing gets
   tightened, missing information gets asked for.
4. **Write the thin-fields line after the closing NEVER DO section, outside the block body**, and
   only if thin fields exist:

   ```
   Thin fields, next pass: THE HAND, COLOR / LIGHT
   ```

   Names only, no marker of any kind inside the block. If nothing is thin, the line is absent
   entirely. Never write it empty, and never list a field the user actually dug.
5. **Write it to `taste-blocks/<slug>.md`** and tell the user the path, so the block outlives the
   window it was made in and `refine` has something to load. Create `taste-blocks/` if it isn't
   there. On a refine, the new version goes in above the old one rather than replacing the file, per
   [references/library.md](references/library.md).
