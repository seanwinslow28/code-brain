# Degraded paths

What to do when the pictures don't arrive. Read this the moment a generation is refused, comes back
tamer than you asked for, or fails outright, and read it before the interview starts if the session
can't generate images at all.

The interview mechanics stay in SKILL.md: the stage budget, the degradation order, and both Emit
gates. This file only covers what changes when the images stop cooperating.

---

## When the model refuses

Push is the stage most likely to be refused, because "make it ugly, go too far" is exactly the shape
safety filters catch. Measured 2026-08-09 on GPT Image 2: enhancement language aimed at an image
containing a child was refused 3 of 3 times and again after a reword, while a plain compositional
edit on the same image passed. With a described likeness of a real person in the chain, the model
refused to make the subject prettier (3 of 3) and refused to make them uglier (2 of 2), while "strip
the room out" and "make it look hand drawn" passed untouched. The face is fenced. Everything around
it is not.

So: on a refusal, say so out loud, then re-aim the push once at composition, palette, or finish
rather than the figure. If that is also refused, skip Push, tell the user the block will be thinner
for it, and continue. Do not reword a request until it slips past a filter. That is not a
workaround, it is evasion, and the block you would get is not worth it.

[Read "skip Push" against **What "skip Push" means** below before acting on it. It means skip the
picture, never the questions.]

**Three different failures, and only one of them is a refusal.**

- **A refusal** is the model declining on content. It costs an attempt.
- **A sanitized return** is the model complying partway. The picture arrives, nothing was declined,
  and the thing you asked for quietly didn't happen. Under safety pressure this is more common than
  outright refusal. It costs an attempt, because it is a refusal wearing a picture.
- **A transport failure** is a rate limit, a timeout, a quota, a dropped connection. It isn't a
  filter and a retry isn't evasion, so it costs nothing. Retry it plainly. If retrying stops working
  you've lost generation for the run rather than lost an argument with it, which is the mid-run case
  in the next section.

**Check the Push image before you show it.** You named the axis you were overshooting along before
you generated, so compare what came back against Fork's winner on that axis. If it came back tamer
than the winner, or the same, it didn't overshoot, and a pullback measured against it measures
nothing. Treat it as a refusal: say what happened, spend attempt 2 on the re-aim, and don't put the
tame one on screen as if it were the push. If the axis did move but something else got sanitized (a
face blurred, a likeness swapped), the overshoot is real and usable, so show it and say what
changed, or the user reacts to the swap instead of to the push.

This is the failure most likely to get past you, because a refusal announces itself and a sanitized
Push is a perfectly nice picture. Push exists to find the thing the user didn't know to ask for, and
a perfectly nice picture has never once found that.

**The cap, stated so it can't be argued with.** Two attempts per generation, ever. Attempt 1 is the
ask you meant to make. Attempt 2 is one re-aim that changes the *target*, to composition, palette,
finish, ground, or crop, and leaves the figure alone. There is no attempt 3. A reword is not a new
attempt, it's the same attempt in a different coat, and the measured reword failed anyway. Each
image you intend to make gets its own two: Fork's two get two each, Push's one gets two. Entering a
new stage does not restore attempts on an image already refused twice.

**What "skip Push" means, and what it must never mean.** It means skip Push's picture. It does not
mean skip Push. Push owns **4. STRUCTURE**, **9. THE FINISH**, and **10. THE ONE MOVE**, and Gate 2
in SKILL.md hard-fails when THE ONE MOVE is thin, so a stage actually skipped is a run that
cannot ship, and telling the user "the block will be thinner for it" would be a lie by a wide
margin. Run Push against Fork's winner in words instead. That image is on screen, the user already
picked it, and Push already carries a verbal fallback for the case where the picture fails to
produce a ceiling. Aim it at all three fields, not only the finish: what would you cut out of this,
and what would you still protect if everything else went wrong. Expect **9. THE FINISH** to go thin,
because a ceiling imagined is weaker than a ceiling the user flinched at. Expect the other two to
hold. If THE ONE MOVE won't come out in words either, the run fails at Emit, and it should.

A refused Push doesn't put the no-pictures gate in play. Fork already spent two, and that gate only
fires at zero. It does change what the block can honestly claim, though, because THE FINISH was
never tested against a picture. Put that on the version line the way the next section describes:
`version: 1 · 2026-08-17 (Push was refused; THE FINISH untested)`.

**When Fork's image is the one refused, do not run the fork on what's left.** Fork's own rule is
that a fork with one image in it isn't a fork, and an asymmetric fork is worse than a lone image:
whichever direction got drawn wins for being the visible one, and the reason the user hands you is
about rendering rather than about direction. That reason is **1. CORE THESIS**, which Emit
hard-fails on, so the contamination lands on the field you can least afford to lose.

Make the missing half a different way instead. Generate a single-dimension variant of the image that
did pass, and fork against that. This is not the spare third generation and the ban on spending one
for tidiness doesn't apply, because a refused half means Fork's second image never arrived and this
is that second image taking another route. Two pictures delivered either way, and four is still not
available. The variant is a new image, so it gets its own two attempts.

If the variant is refused too, you can't build a fork out of pictures at all. Run Fork's pick in
words, symmetrically, on the words-only recipe below, both directions described and neither drawn.
The picture that survived isn't a fork half any more, but it's still a real image of the subject, so
keep it for THE HAND's fallback, which is the field that most needs something to point at.

**When the refusals don't stop.** At Widen you may pick the subject yourself, because it's a control
variable and nobody has been told no yet. That stops applying here. Once the model has refused, the
subject is a thing the run is negotiating over, and swapping it out from under the user decides on
their behalf what they're allowed to want a picture of. So you disclose and they choose. Say what
was refused and what passed, then put both options up with their costs:

> The model won't generate this one. Two ways forward. We change what's in the picture and keep the
> stages intact, or we keep the subject and I run the rest in words, which costs you THE HAND and
> THE FINISH. Your call.

Don't name the fence in the same breath as the question. If they ask why one thing passed and
another didn't, answer them, because they asked. Volunteering it hands over the fix and the
diagnosis at once, which is the thing this file bans in three other places.

One swap. It restores no spent attempts, and if the swapped subject is refused too, the answer is
whatever it would have been without the swap.

## When there are no pictures at all

If the session cannot generate images, say so at the start, not at Fork. Run all four stages in
words, mark the emitted block `mode: words-only`, and tell the user which fields are least
trustworthy as a result (THE HAND and THE FINISH, which are the two nobody can judge from a
description).

[`mode: words-only` is the intent, not the literal string. Write it as the version line below.]

**Say it at the start** is the load-bearing half. Someone who agrees to a taste interview and finds
out four stages in that nothing is going to be drawn has spent their time on a promise you knew you
couldn't keep.

**"Mark the emitted block" means the version line, and the mark can't be a style token.** Write it
like this:

```
version: 1 · 2026-08-17 (interview ran without generated references; THE HAND and THE FINISH untested)
```

A literal `mode: words-only` inside the block breaks the rule in **Marking a field thin** in
SKILL.md.
"Mode" is a live style word and "words-only" reads as text only, no imagery, so a multimodal model
can reasonably answer it with typography or by dropping the subject. The parenthetical above is
inert, it's plain English a person could have typed, and the provenance still travels with the block
long after this session is gone.

**The no-pictures gate is waived, and waived out loud.** It's conditioned on image generation having
been available precisely so this mode has somewhere to stand, which means a words-only run passes it
by construction and not by merit. Say that when you announce the mode, so nobody mistakes a waiver
for a pass.

**Then name the two fields to trust least: 7. THE HAND and 9. THE FINISH.** THE HAND's whole
fallback is pointing at a region of a real generated image and asking what tool would leave that
mark, and there's no image to point at. THE FINISH's ceiling comes from watching an overshoot break,
and nothing broke. Neither is judgeable from a description, by them or by you.

**What the stages do here.** Widen is unaffected, because it never spent anything. Fork picks
between two described directions, symmetrically, neither one drawn. Push overshoots the winning
description in words. Negate is not unaffected, which is its own paragraph below. The exchange
budget doesn't change.

**The decisions gate does not relax, and the honest count is three.** Gate 2 in SKILL.md fails a run at more than
four thin fields, or a thin CORE THESIS, or a thin THE ONE MOVE, or fewer than five NEVER DO items.
Words-only starts you three thin, not two: THE HAND and THE FINISH for the reasons just given, and
**8. COLOR / LIGHT**, which Fork owns precisely because counts and bans come from looking and here
there's nothing to look at. One more is permitted, and it's **6. MEDIUM / SUBSTRATE**, the only one
of the four you can still reach in words. Four of ten passes and four is the ceiling. A fifth fails
the run. There's no slack in this mode, so don't budget as though there is.

What does survive is everything the gate hard-fails on, and none of it needed a picture. CORE THESIS
comes off why one direction beat the other, THE ONE MOVE comes off the pullback, NEVER DO comes off
kills. Spend every follow-up you have on those three.

**Negate loses a third of its material and two thirds of its fallback.** Negate works from Widen
kills, Fork losers, and whatever broke in the Push image, and the third source doesn't exist here.
Then when the kills don't reach five, the top-up rule restates the finish ceiling from Push and the
color count from Fork, and both of those are thin by default in this mode, leaving the one move as
the only restatement still standing. So dig the Widen kills harder than you otherwise would: each
kill should yield the ban itself and the generalizing ban underneath it, the second-order one that
also rules out something nobody named. That's where a words-only Negate finds its five.

**When generation dies mid-run.** All of the above reads as a start-of-run condition, and generation
also just stops sometimes, usually at Fork. If at least one image got made, the no-pictures gate is
already satisfied and stays satisfied, because it counts generations spent and not generations
available. Run the remaining stages on this recipe and say partial rather than absent:

```
version: 1 · 2026-08-17 (generation failed partway; THE FINISH untested)
```

Name only the fields the loss actually cost. If Fork's images were made and Push's wasn't, THE HAND
had something to point at and doesn't belong on that line, and the default-thin count above shrinks
with it.

If it comes apart anyway it fails at Emit like any other run. Words-only is a thinner run, not an
excused one.
