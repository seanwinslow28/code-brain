---
name: wince
description: Interview someone's visual taste out of them by showing options and reading their reactions, then emit a reusable taste block they can paste into any image model. Use when asked to "figure out my style", "build my taste block", "what's my aesthetic", "the model won't draw like me", "make it look like mine", "run the taste interview". If someone is stuck arguing an image toward what they want one adjective at a time, offer it, do not start the interview unasked. USER-INVOKED — do not invoke from another skill. Not for generating final art (use the image-gen skills); not for prose voice (use writing-voice-modes); not for fixing a single prompt or a drifted generation (use prompt-how-much).
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

## The four stages

Four stages, then Emit. A full run finishes in under ten minutes and spends three or four
generations. Widen and Negate spend zero. Fork spends two or three. Push spends exactly one.

| Stage | Job | Generations | Exit when |
|---|---|---|---|
| **Widen** | Five named directions in words, deliberately far apart. Kill the dead ends before spending anything. | 0 | At least three of the five are dead **and** both fields Widen owns are recorded or marked thin. |
| **Fork** | Generate the survivors against the user's real subject. Pick one, then dig. | 2-3 | One direction is chosen with a decision-level reason **and** all four fields Fork owns are recorded or marked thin. |
| **Push** | Overshoot the winner on purpose so the user pulls it back. | 1 | The user has named a ceiling, liked or not, **and** all three fields Push owns are recorded or marked thin. |
| **Negate** | Walk back through every kill and ask why it was wrong. | 0 | Five to ten banned items, each with its why, **and** the field Negate owns is recorded or marked thin. |

Rough clock: two minutes on Widen, four on Fork, two on Push, two on Negate. If you're past minute
seven and Negate hasn't started, stop digging, take first answers, and mark them thin. Negate is the
one stage you can't shorten, because it's the only one that produces the spine.

### Which stage owns which field

Every field in [references/block-schema.md](references/block-schema.md) has exactly one owner. A
stage does not exit until each field it owns has an answer in the user's own words or is marked thin
per the rule above. Nothing gets filled in later from memory, and nothing gets filled in by you.

| Field | Owner | Why that stage can actually answer it |
|---|---|---|
| 3. REGISTER | Widen | The spread crosses register on purpose, so a kill is a position on the scale. |
| 2. EMOTIONAL MODE | Widen | A kill is a sacrifice. The direction they gave up is the OVER clause, which is the half people can't state cold. |
| 1. CORE THESIS | Fork | The decision-level reason for the pick, dug per the rule, is what the thing should feel like before it announces itself. |
| 6. MEDIUM / SUBSTRATE | Fork | Same subject, different directions. Substrate is the first thing that visibly differs. |
| 7. THE HAND | Fork | You can point at the marks in a specific image and ask what made them. |
| 8. COLOR / LIGHT | Fork | Counts and bans come from looking. Nobody says "exactly one accent" from memory. |
| 4. STRUCTURE | Push | The overshoot is the only image the user has to triage, and STRUCTURE is the field that has to name what gets cut. |
| 9. THE FINISH | Push | The ceiling the user names is a finish boundary. That's what Push is for. |
| 10. THE ONE MOVE | Push | When everything else goes wrong at once, the thing they still protect is the one move. |
| 5. NARRATIVE STANCE | Negate | The whys pile up into forbidden routes to meaning. Ask for the positive route while the negatives are on the table. |
| NEVER DO | Negate | Bans come from real kills, and by Negate every kill in the run is on record. |

---

### Widen — 0 generations

Before anything else, ask one line: what are you going to be making pictures of? You need it for
Fork. If they don't have one, pick a subject, say you're picking it, and keep it fixed. The subject
is a control variable, not a taste answer, so choosing it for them costs nothing.

Then say roughly this:

> I'm going to name five directions. They're deliberately far apart and most of them are wrong.
> Tell me which ones are out. Don't be polite about it.

Name five. One line each, no images. Each line names its **medium**, its **finish**, and its
**register**. The spread has to cross all three, not run five flavors of one look. The check is
mechanical: no two of the five may match on more than one of those three axes. If two do, one of
them is filler and you have four directions, not five.

Ask why each kill is a kill, and dig it per the rule above. Kills are cheaper to explain than keeps
and they carry more, so this is where the interview is fast.

Record **3. REGISTER** and **2. EMOTIONAL MODE** before you leave. For EMOTIONAL MODE, say back what
they gave up: "so you're giving up X to get Y" is the OVER clause, in their words, and it's usually
one question.

If fewer than three die, the spread was too narrow. Replace the near-duplicate survivors with
sharper opposites, once, and ask which of these is closest to something they'd never make. If all
five die, ask what all five got wrong, then offer three new ones built out of that answer. One
reoffer either way, then take the top two survivors and move.

### Fork — 2-3 generations

At most two directions survive Widen, so generate one image per survivor. If only one survived,
generate it and then generate one variant that changes a single dimension of it, because a fork with
one image in it is not a fork. Either way that's two. Same subject every time, same framing every
time, so the delta reads as style and not composition. Say that out loud:

> Same subject, one version per direction. The only thing changing is style, so whatever you
> react to is style.

Spend a third generation only to break a tie the user can't break in words, or to split a winner
they liked in halves. Never a third for tidiness. Four is not available at this stage.

Get a pick, then dig it per the rule until the reason would still be useful on a subject that was
never on screen. That reason is **1. CORE THESIS**.

Then work the picture in front of you for the other three. Point at the image, not at categories.
"What is that surface, if you had to go buy it" gets **6. MEDIUM / SUBSTRATE**. "What made those
marks" gets **7. THE HAND**. "How many colors are allowed in here, and which one is never allowed"
gets **8. COLOR / LIGHT**, which needs a number, an "only," or a "never" to be worth recording.

### Push — 1 generation

Push always spends its generation. It may take Fork's winner as the input image and go further from
there, which is what "reuse" means here. It never means skipping the generation.

Overshoot the winning direction along its own most distinguishing axis. More of the thing that made
it win, too much of it, on purpose. Tell the user that's what you're doing before they see it:

> This next one goes too far on purpose. It'll probably be ugly. Tell me where it broke and pull me
> back.

Then read the pullback. Three things come out of it and you ask for each one:

- **9. THE FINISH** — "where exactly did it stop being right?" The ceiling, stated as a boundary.
- **4. STRUCTURE** — "what would you cut out of that?" A structure rule that deletes nothing is
  decoration, so keep asking until something gets deleted.
- **10. THE ONE MOVE** — "in all that mess, what's the one thing still worth keeping?" One move, not
  a list. If they name three, ask which one they'd protect when the three fight.

Push exits on a named ceiling whether or not they liked the result. Liking it is not the point. A
user who says "actually that's better" has still named a ceiling, it's just further out than you
thought, and that's the finding.

**Why Push is not optional.** Push is the only stage that finds something the user did not know to
ask for. Every other stage narrows what they already brought. Cut it and this becomes an interview
about a spec, which is the thing that does not work.

### Negate — 0 generations

No images. Walk back through everything killed in Widen, Fork, and Push, in order, and ask why each
one was wrong. You have the list already: three or more Widen kills, one or two Fork losers, and
whatever broke in the Push image.

> Back to the ones you killed. This one, early on. What was actually wrong with it?

Each answer becomes a NEVER DO item in the user's own rejecting words, with its why attached, and
the why is the negative of a value the keeps demonstrated. Five to ten items. Fewer than five means
you're taking bans at face value and not asking why. More than ten and the list stops generalizing
and starts being a log.

If the kills don't reach five items, don't invent the rest. Restate the negative half of fields
you already recorded: the finish ceiling from Push, the color count from Fork, and the one move all
carry a ban on their far side, and the schema wants those bans written here anyway. Restating a ban
is not redundancy. Inventing one is.

While the forbidden routes to meaning are on the table, ask for the positive one: "so if the face
isn't doing the work, where does the feeling come from?" That answer is **5. NARRATIVE STANCE**.
Ask it, don't derive it. Inverting a ban yourself is filling in a field for them.

A closing principle is welcome as a last line, and it doesn't replace the per-item whys.

---

### Emit

**Gate first.** If image generation was available in this run and Emit is reached with zero
generations spent, the run failed. Say so plainly, name the stage that never happened, and do not
emit a block. A block built from words the user never tested against a picture is a spec, and specs
are what this skill exists to replace.

Otherwise, emit the block exactly per the template in
[references/block-schema.md](references/block-schema.md). Then:

1. **Name it.** Ask the user. The name names the style, not the person, because they'll have more
   than one. If they shrug, offer two names built out of their own words and let them pick.
2. **Stamp `version: 1 · <today's date>`.** Version 1 on a first run. Refinement bumps it.
3. **Run the ten "Accept when:" tests** from the schema against the ten answers before the block
   goes on screen. When one fails, handle it per "Where this rule stops" above: loose phrasing gets
   tightened, missing information gets asked for.
4. **Write the thin-fields line after the closing NEVER DO section, outside the block body**, and
   only if thin fields exist:

   ```
   Thin fields, next pass: CORE THESIS, THE HAND
   ```

   Names only, no marker of any kind inside the block. If nothing is thin, the line is absent
   entirely. Never write it empty, and never list a field the user actually dug.
