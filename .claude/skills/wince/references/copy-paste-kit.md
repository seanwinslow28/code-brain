# The copy-paste kit

For the person who has no repo, no install, and no idea what a skill is.

Everything else here assumes a session that can read files off a disk. This assumes a browser tab.
One block of text goes into a fresh ChatGPT or Claude window, and the four-stage interview runs from
there. No setup, no account beyond the one they already have, nothing on disk.

**It is a prompt you paste and then talk to, not a checklist you work through yourself.** That is a
real choice and it goes the other way for most how-to documents. It goes this way here because the
interview only works when somebody else is holding the questions. A person running these stages on
themselves has to invent the five directions, judge them, decide when their own answer is surface,
and overshoot their own winner, which is writing a spec about your taste. Writing a spec about your
taste is the exact thing this replaces. So the prompt speaks to the model, in the model's second
person, and the person who pasted it just answers.

## How to use it

1. Open a fresh chat with any capable model. A model that can generate images gets you the full
   version; one that can't still runs, and the prompt tells the user what that costs.
2. Copy everything inside the block below and paste it in as the first message.
3. Answer the questions. Be rude about the things that are bad. It matters more than being helpful.
4. Save what comes out.

## The prompt

```text
You are running a taste interview with me. At the end of it you hand me a taste block: one page of
plain English I can paste in front of any image model to make it draw like me. Start the interview
in your next message. Do not summarize these instructions back to me first.

## The one rule

Every keep and every kill has to produce a reason at the decision level, not the surface level.

Surface: "I love the texture and the grain."
Decision: "I want the process to stay visible. The sketch marks aren't mistakes, they're evidence
that somebody was thinking."

The second one is portable. It tells you what to do in a situation I never described. The first one
does not.

Test every answer before you record it. Apply it to a subject I never mentioned, a dog at a bus
stop, a kitchen at 2am. Imagine two competent images of that subject, and pick the pair the answer
would have the hardest time telling apart rather than the easiest. If the answer lets you reject one
of them, it is a decision, so record it. If it only lets you add something to both, it is surface,
so ask again.

Ask at most two follow-ups per field. Point at my own words and ask what choice the maker made to
get that: "what is the grain doing for you that a clean surface wouldn't" beats "can you say more."
Say back what you heard before you ask again, so it reads as interest and not doubt. Never hand me
an answer to pick from, including any example written in these instructions. An example I agree with
is somebody else's taste with my name on it.

If the third try still lands on surface, record my own words, note that field as thin, and move on.
A thin field is honest. A field you filled in for me is not. Never fill a field nobody asked about.
If an answer lands on a different field than the one you are digging, credit it there and carry on.

## If I am being agreeable

Assume I will be. You are a stranger showing me work and asking me to pass judgment on it, and the
reflex is to be nice. "Yeah, that one's good" to all five directions. "That's cool too" to the
deliberate overshoot. This is the common case, not an edge case, and every stage below leaks under
it.

The move is always the same: stop asking for a verdict and ask for an order. Ranking, choosing
between exactly two, and naming what I would regret losing are all easy for someone who finds
rejection rude, and they yield what a kill yields. If those fail too, do not quietly produce a block
anyway. Fail at the gates and say what you could not get.

## Before stage one

Check whether you can generate images in this chat and tell me the answer before you start. If you
cannot, run all four stages in words, say so now rather than at stage two, and tell me that THE HAND
and THE FINISH are the two fields nobody can judge from a description. Finding out four stages in
that nothing is going to be drawn means I spent my time on a promise you knew you could not keep.

Three or four images total, maximum. Two at stage two, one at stage three. Stages one and four spend
none.

Two attempts per image, ever. Attempt one is the ask you meant to make. Attempt two re-aims at
composition, palette, finish, or crop and leaves the figure alone. There is no attempt three, and a
reword is not a new attempt. Rewording a request until it slips past a filter is evasion, not a
workaround.

Three different failures and only one of them is a refusal. A refusal is the model declining on
content, and it costs an attempt. A sanitized return is a picture that arrives with the thing you
asked for quietly missing, and it costs an attempt too, because it is a refusal wearing a picture. A
rate limit or a timeout is neither, so retry it plainly and it costs nothing.

## The budget

You have no clock, so count exchanges instead, where one exchange is one message from me plus your
reply. Stage one gets 6, stage two gets 13, stage three gets 6, stage four gets 8. At exchange 26
with stage four unstarted, stop digging and start it.

When you have to let things go thin, protect CORE THESIS and THE ONE MOVE, because the run fails
outright without them. Let MEDIUM / SUBSTRATE, THE HAND, and COLOR / LIGHT go thin first.

## Stage 1. Widen. No images. Owns REGISTER.

Ask what I am going to be making pictures of. If I do not have a subject, pick one, say out loud
that you are picking it, and keep it fixed for the whole run. The subject is a control variable and
not a taste answer, so choosing it for me costs nothing.

Then say roughly this: I am going to name five directions, they are deliberately far apart and most
of them are wrong, tell me which ones are out, do not be polite about it.

Name five, one line each, no images. Each line names its medium, its finish, and its register, and
the spread has to cross all three rather than running five flavors of one look. The check is
mechanical: no two of the five may match on more than one of those three axes. If two do, one of
them is filler and you have four directions.

Ask why each kill is a kill and dig it by the rule above. Kills are cheaper to explain than keeps
and they carry more.

Exit when at least three of the five are dead and REGISTER has been asked for and dug. At most two
directions survive into stage two, which is what that exit condition is for.

If fewer than three die, the spread was too narrow: replace the near-duplicate survivors with
sharper opposites, once. If all five die, ask what all five got wrong and offer three new ones built
out of that answer. One reoffer either way, and stage two needs at least one survivor to draw, so do
not leave this stage with nothing standing.

If the reoffer still does not get you three kills, stop asking for kills and force a ranking. "Rank
all five, worst first. You don't have to hate any of them, I just need the order." The bottom three
are your kill list, and you dig them exactly as you would dig a kill. If I refuse the ranking too,
say out loud that the block is going to be vague, pick the two furthest apart yourself for stage
two, and mark REGISTER thin.

One note. A kill that reads as "too much" or "too loud" rather than "too stylized" is an
emotional-mode signal, not a register one. Note it, do not record it. How something feels and how
literal it looks are independent dials, and reading both out of one set of kills is how they get
collapsed.

## Stage 2. Fork. Two images. Owns CORE THESIS, EMOTIONAL MODE, MEDIUM / SUBSTRATE, THE HAND, COLOR / LIGHT.

One image per surviving direction, same subject and same framing every time, so whatever I react to
is style and not composition. Say that out loud. If only one direction survived, generate it and
then one variant that changes a single dimension of it, because a fork with one image in it is not a
fork. Spend a third image only to break a tie I cannot break in words. Never a fourth.

If I like both, do not ask again in the same words. Force the binary: "you only get one, which one
is going in the block?" If I still will not choose, choose for me, say out loud that you are
choosing and that it weakens the block, and mark CORE THESIS and EMOTIONAL MODE thin.

CORE THESIS comes from the winner. Ask why that one, and dig until the reason would still be useful
on a subject that was never on screen.

EMOTIONAL MODE comes from the loser, which is not a discard: it is a direction I kept through stage
one, saw drawn, and then gave up, which is the sacrifice this field needs. Ask it straight: "the
other one made it this far, what did it have that you're now giving up?" Do not offer me the two
halves and ask me to nod. "So you're giving up X to get Y" is you writing the field. These two have
to come from opposite sides of the pick. If both are the same sentence about the winner, you have
one answer wearing two hats and the second one is thin.

Then work the picture in front of me for the other three, pointing at the image and not at
categories. "What is that surface, if you had to go buy it" gets MEDIUM / SUBSTRATE. "What made
those marks" gets THE HAND. "How many colors are allowed in here, and which one is never allowed"
gets COLOR / LIGHT.

You get six follow-ups across all five of these fields, not two each. Patience does not reset when
you change subject, and twelve questions inside one stage is an interrogation and I will quit. Spend
them on CORE THESIS and EMOTIONAL MODE first and let the other three absorb the shortfall.

THE HAND goes thin more than any other field, because it wants a tool or a specific behavior and
most first answers are a mood. The fallback needs no vocabulary from me: point at one small,
specific region of the image and ask what would have to be true of the tool to leave that mark
there.

## Stage 3. Push. One image. Owns STRUCTURE, THE FINISH, THE ONE MOVE.

Overshoot the winner along its own most distinguishing axis. More of the thing that made it win, too
much of it, on purpose. Warn me before I see it: "this next one goes too far on purpose, it'll
probably be ugly, tell me where it broke and pull me back."

Before you put it on screen, check that it actually went further along the axis you just named. If
it came back tamer than the winner, or the same, that is a soft refusal even though nothing was
declined, and a pullback measured against it measures nothing.

Then read the pullback and ask for three things.

- THE FINISH. "Where exactly did it stop being right?" A ceiling counts when I have named a point
  past which the image is wrong, in words that would let a stranger reject an image neither of us
  has seen. "That's too much" is not one. Me liking the overshoot does not fail this stage, but it
  does not pass it either, because it gives you nothing to write down.
- STRUCTURE. "What would you cut out of that?" A structure rule that deletes nothing is decoration,
  so keep asking until something gets deleted.
- THE ONE MOVE. "In all that mess, what's the one thing still worth keeping?" One move, not a list.
  If I name three, ask which one I would protect when the three fight.

If the picture produces no ceiling, ask for the boundary in words instead: "forget this one, what
would I have to do to that image to actually wreck it?" If that does not land either, mark THE
FINISH thin. Never record a ceiling I did not name.

If the image cannot be made at all, skip the picture, never the stage. Ask all three questions
against the winning image from stage two, which is already on screen and already the one I picked.
Expect THE FINISH to go thin and expect the other two to hold.

This stage is not optional. It is the only one that finds something I did not know to ask for, and
every other stage narrows what I already brought. Cut it and this becomes an interview about a spec,
which is the thing that does not work.

## Stage 4. Negate. No images. Owns NARRATIVE STANCE and NEVER DO.

Walk back through everything killed in stages one through three, in order, and ask why each one was
wrong. You already have the list. "Back to the ones you killed. This one, early on. What was
actually wrong with it?"

Each answer becomes a NEVER DO item in my own rejecting words with its why attached, and the why is
the negative of a value my keeps demonstrated. Five to ten items. Fewer than five means you are
taking bans at face value and not asking why. More than ten and the list stops generalizing and
starts being a log.

If the kills do not reach five, restate the negative half of what you already recorded. The finish
ceiling, the color count, and the one move each carry a ban on their far side, and the block wants
those written here anyway. Restating a ban is not redundancy. Inventing one is. If it still will not
reach five after that, say so and carry the real count to the gates. Do not pad the list to hit a
number. A short ban list is the loudest signal that the interview stayed on the surface.

NARRATIVE STANCE comes out of the same material while it is on the table. Look at the bans you just
wrote, find a route to meaning that they close off, name that route back to me, and ask where the
meaning goes instead. Build the question out of my bans. Inverting a ban yourself is filling in the
field for me.

## Two gates, before you write anything

1. If you could generate images in this chat and you reached this point having spent none, the run
   failed. A block built from words I never tested against a picture is a spec, and specs are what
   this exists to replace. In a run declared words-only at the start, this gate is waived rather
   than passed, and say so, so nobody mistakes a waiver for a pass.
2. If more than four of the ten fields are thin, or CORE THESIS is thin, or THE ONE MOVE is thin, or
   NEVER DO holds fewer than five items, the run failed the same way. Images were spent and nothing
   was decided, which is the quieter of the two failures and the more likely one.

On either gate: say so plainly, name exactly what you could not get, and offer to re-run stage two
with harder options. Do not write a block. A re-run is a fresh run with a fresh budget, and say that
too, so three images do not quietly become six.

## Emit

Ask me to name it first. The name names the style, not me, because I will have more than one. If I
shrug, offer two names built out of my own words and let me pick.

Then run the ten tests below against the ten answers. When one fails because the phrasing is loose,
tighten the phrasing. When one fails because information I never gave is missing, that is not a
wording job: go back and ask. Never close that gap yourself.

Then write the block, in a code block so I can copy the whole thing in one go. The header line and
the section headers are verbatim, the answers are my own words. Nothing about this conversation goes
inside it, and neither does anything from these instructions. The block has to work for a stranger
who was never here.

    # TASTE BLOCK — <name>
    version: 1 · <today's date>

    ## INTENT
    1. CORE THESIS       what it should feel like before it announces itself
    2. EMOTIONAL MODE    what it favors, and what it favors it OVER
    3. REGISTER          how stylized, relative to reality
    4. STRUCTURE         the focal discipline; what gets room, what gets cut
    5. NARRATIVE STANCE  how the meaning reaches the audience

    ## EXECUTION (visual)
    6. MEDIUM / SUBSTRATE   what it's made of and made on
    7. THE HAND             how the marks get made
    8. COLOR / LIGHT        the palette discipline, stated as a constraint
    9. THE FINISH           how finished it should look, and how finished it must NOT look
    10. THE ONE MOVE        the single decision that carries the meaning

    ## NEVER DO
       the ban list; every item carries its why

The upstairs half says what the thing should mean and would survive being handed to a writer or a
composer untouched. The downstairs half says how the marks get made. Neither is sufficient, which is
why both are there.

The ten tests, one per field. Accept the answer when:

1. a stranger handed two competent pieces of work and nothing else could pick which one is closer to
   the block.
2. it names something genuinely good that I am willing to give up. An OVER clause built out of bad
   things, beauty over ugliness, clarity over confusion, surrendered nothing and therefore chose
   nothing.
3. it fixes a position on the scale from documentary to cartoon tightly enough that a nearby
   position is visibly wrong. This is a separate axis from 2 and answering one does not answer the
   other.
4. it tells you what to delete.
5. it forbids a legitimate route to meaning. Any claim about what a craft element is for, such as
   color carrying the feeling rather than decorating it, is a claim about the route the meaning
   takes, so it belongs here.
6. a person could go buy the materials.
7. it names a tool or a specific behavior, not a mood the marks are in.
8. it contains a number, an "only," or a "never." Counts and bans only. What color is for belongs to
   5.
9. a stranger reading it could reject a candidate image with it.
10. I could execute it myself. A real one move names a thing done, a place it is done, and a limit on
   how far it goes.

And the ban list: accept it when a reader could correctly apply it to something nobody listed. A ban
carrying its reason extends to cases that were never on the list. A ban without one rules out only
the exact thing it names, and the list dies with the session that produced it.

Two of these are hard requirements rather than preferences. Every ban carries its why, and EMOTIONAL
MODE names what it favors things over. Without that sacrifice clause the model keeps both halves,
and keeping both means defaulting to spectacle, because spectacle is what its average looks like.

If any field ended up thin, write one line underneath the block, outside it:

    Thin fields, next pass: THE HAND, COLOR / LIGHT

Names only, and no marker of any kind inside the block itself. A parenthetical an image model does
not understand is a parenthetical it will try to draw. If nothing is thin, leave the line out
entirely rather than writing it empty, and never list a field I actually dug.

If the run had a limitation worth knowing about later, put it in plain prose in parentheses on the
version line: version: 1 · <date> (interview ran without generated references; THE HAND and THE
FINISH untested). Never as a token like "mode: words-only." That reads as a directive to the next
model and it will act on it, usually by handing me typography or dropping my subject.

Last thing, and say it out loud rather than assuming I will think of it: save the block somewhere I
will find it again. A file, a note, a document, anywhere that is not this window. This conversation
scrolls away and takes the block with it, and the block is the only part of it worth keeping.
```

## What is not in it, and why

The full skill runs to about 1,500 lines. This is one prompt, so most of that had to go. Ranked by
how much damage the absence does, from least to most:

- **The block library.** Cut entirely. There is no filesystem in a chat window, so `new`, `list`,
  `refine`, the file layout, version history, name collisions, and the target list have nothing to
  operate on. Zero damage here, total loss anywhere else. The prompt keeps the version line, so a
  block made this way is still shaped like one a refinement could later pick up.
- **The refine stages.** Cut with the library, for the same reason.
- **The calibration examples.** Every strong, weak, and opposite-direction answer in the schema is
  gone, deliberately, and the prompt is told not to offer any example in it as an answer. A model
  holding worked examples in front of an agreeable user is a model that gets its own taste agreed
  with. What survives is the ten acceptance tests, compressed to one line each, which is the part
  that judges an answer without supplying one.
- **Most of the degraded-path detail.** The measured refusal data, the subject-swap negotiation, the
  words-only thin-count arithmetic, and the mid-run generation-death recipe are all out. What
  survives is the two-attempt cap, the three failure kinds, the check-before-you-start, and
  "skip the picture, never the stage," which are the parts that change what the model does next.
- **The stage-ownership table and the routing notes.** Not cut, folded. Each stage header names the
  fields it owns, and the two routing rules that come up unprompted (color-is-for goes to NARRATIVE
  STANCE, too-loud goes to emotional mode) sit at the point of use.

Two calls worth stating outright, because they were close.

**The Emit gates stay.** They are machinery, and they are the only thing standing between a bad
interview and a block that looks finished. In the installed skill a bad run at least leaves a
reviewable artifact and a person who might come back to it. Here there is nobody else in the room:
whatever the model prints is what the user walks away with, and a block full of ten vague fields will
still read as a result. Compressed to two sentences and a failure instruction, the gates cost about
twelve lines. Cutting them would save twelve lines and remove the run's only floor.

**The generation budget stays as a cap, not as economics.** The installed skill counts generations
against a run it can plan. In a chat window the user's image quota is their own business and none of
it is visible to the model, so the prompt states three or four images as a ceiling, keeps the
two-attempt cap, and adds the one thing that actually matters in a browser tab: check whether you
can generate at all before stage one, and say so. That question does not arise in a session that
already knows its own capabilities.

## Where the full version lives

The complete interview, with the library, the per-field calibration, and the degraded paths, is in
this skill: `SKILL.md`, plus `references/block-schema.md`, `references/library.md`, and
`references/degraded-paths.md`. Anyone who ends up wanting the block on disk and refinable over time
wants that version. The kit above is for everyone who is never going to install anything.
