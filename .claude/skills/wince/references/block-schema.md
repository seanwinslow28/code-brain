# The taste block schema

The block is the deliverable. Everything else in this skill exists to fill it in.

---

## PASS CRITERION

Every implementer of this schema has to satisfy this, and it is the only test that matters:

> A stranger who has never heard of Wince can paste a filled block into a fresh ChatGPT or
> Claude window with a one-line scene request and get back something in their style.
> No JSON, no tool-specific syntax, no reference to Wince anywhere in the block body.

The body of the block is plain readable English that a person could have typed themselves. If a
filled block only works when this skill is in the room, the block failed and the schema is being
used wrong.

---

## The template

Emit exactly this shape. The header line and the section headers are verbatim; the answers are the
user's own words, dug down to the decision level.

```
# TASTE BLOCK — <name>
version: <n> · <date>

## INTENT
1. CORE THESIS       what the thing should feel like before it announces itself
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
```

**`<name>`** names the style, not the person. One block per style, because taste is not one
setting. **`version`** starts at 1 and bumps on refinement, so re-running sharpens a block instead
of overwriting it.

**Why two altitudes.** INTENT says what the thing should mean and is medium-agnostic; it would
survive being handed to a writer or a composer untouched. EXECUTION says how the marks get made and
is visual-only. Neither half is sufficient. INTENT cannot say "leave the construction lines
visible." EXECUTION cannot say why any of it matters, which is what lets a model extend the block
to a scene nobody described. NEVER DO sits under both because negation is the one part that stays
stable across altitudes.

**The test for which half a field belongs to** is whether it survives into prose and music
unchanged. That is why REGISTER is upstairs: broad comedy versus naturalism is a live decision for
a writer, and cartoonish versus sincere is one for a composer. Nothing about it is specific to
marks on a surface.

---

## The two hard rules

**1. EMOTIONAL MODE must name what it favors things OVER.** "Quiet and patient" is half an answer.
"Quiet tension over spectacle, patience over instant payoff" is a usable one, because it tells the
model what to sacrifice. Without the sacrifice clause the model keeps both, and keeping both means
defaulting to spectacle, since spectacle is what its average looks like.

**2. Every NEVER DO item carries its why, and the why is the negative of a value the keeps
demonstrated.** A ban without a reason is a preference; a ban with one is a rule the model can
extend to cases nobody listed. "No glossy 3D" bans glossy 3D. "No glossy 3D, because a flawless
surface means the process was hidden or never happened" bans glossy 3D and also bans the
airbrushed thing and the smooth gradient thing that were never on the list.

This rule is deliberately stricter than what a person writing alone at a keyboard produces.
Hand-written blocks routinely skip the whys, because the writer already knows them and never has to
say them out loud. Extracting them is exactly what the interview is for, and it is one of the
reasons an interviewed block beats a hand-written one.

---

## The worked field

Every field entry below follows this pattern. Read this one first.

> **9. THE FINISH** — how finished it should look, and how finished it must NOT look.
>
> *Strong:* "Unfinished on purpose. Construction lines stay in, the searching marks stay in, the
> paper grain stays visible. It should look like it was caught mid-decision, not delivered."
> *Weak:* "Hand-drawn style." That names a category, not a boundary, and the model will resolve the
> ambiguity toward its own average every time.
> *Also strong, opposite direction:* "Immaculate. No visible tooling, no grain, no brushwork. Any
> evidence of process is a defect."
>
> The field is doing its job when a stranger reading the answer could reject a candidate image
> with it.

That last line is the test for all ten. If an answer cannot reject anything, it is a compliment,
not a field.

---

## INTENT

### 1. CORE THESIS
What the thing should feel like before it announces itself.

*Strong:* "The held breath before emergence. Something meaningful is forming, but it has not
announced itself yet."
*Weak:* "Beautiful, emotional, striking." Every image ever made claims all three, so the model
reads it as no instruction at all and falls back to its house style.
*Also strong, opposite direction:* "A Saturday morning cartoon that got out of hand. Everything is
too big, too loud, and delighted with itself."

The field is doing its job when a stranger, handed two competent images and nothing else, could
pick which one is closer to the block.

### 2. EMOTIONAL MODE
What it favors, and what it favors it OVER. See hard rule 1; this is the field that rule exists for.

*Strong:* "Favor still beauty, quiet tension, patience, loneliness, and process over punchline,
chaos, spectacle, or instant payoff."
*Weak:* "Contemplative and moody." No sacrifice named, so nothing gets sacrificed. The model will
add a dramatic sky to the contemplative thing and consider the brief met.
*Also strong, opposite direction:* "Favor absurdity and momentum over dignity and restraint. When
the choice is between funny and tasteful, take funny."

The field is doing its job when it names something genuinely good that the user is willing to give
up. If the OVER list is only made of bad things, nothing was chosen.

### 3. REGISTER
How stylized, relative to reality. The distance between the subject and its depiction.

*Strong:* "Wildly exaggerated, absurd cartoon caricature. Never realistic, never photographic."
*Weak:* "Stylized." A word that covers everything between a police sketch and a Muppet. The model
picks a point on that scale for you, and the point it picks is the middle.
*Also strong, opposite direction:* "Straight naturalism. Correct proportion, correct anatomy,
correct optics. Nothing is heightened, and if a viewer notices a stylistic choice, it has already
failed."

The field is doing its job when it fixes a position on the scale from documentary to cartoon
tightly enough that a nearby position is visibly wrong.

**Register is a separate axis from EMOTIONAL MODE, and answering one does not answer the other.**
The proof is in one person: the same taste can want quiet, patient, and still in one block and
wildly exaggerated in another, because how something feels and how literal it looks are independent
dials. Sober absurdism and frantic naturalism are both real, common, and impossible to specify if
these two fields get collapsed.

### 4. STRUCTURE
The focal discipline. What gets room, what gets cut.

*Strong:* "One focal idea, given room to breathe. Negative space is intentional, never just empty.
A crowded frame is out unless the crowding is itself the subject."
*Weak:* "Good composition, balanced." A compliment applied after the fact, not a rule that decides
anything while the image is being made.
*Also strong, opposite direction:* "Fill it. Every square inch carries something. Empty space is
wasted space, and if the eye gets to rest the joke dies."

The field is doing its job when it tells you what to delete. A structure rule that never removes
anything is decoration.

### 5. NARRATIVE STANCE
How the meaning reaches the audience. This is also where emotion delivery lives: whether feeling
arrives through silhouette and framing or through a face doing the work.

*Strong:* "Internalize the drama. The viewer gets the story through posture, silence, framing,
absence, and atmosphere instead of the big event. Emotion reads first through silhouette, body
language, and scale. Faces can underplay."
*Weak:* "It should tell a story." Universally true of images, so it selects nothing. The useful
part of this field is the route the meaning takes, never the fact that there is meaning.
*Also strong, opposite direction:* "State it. The moment of maximum event, faces at full volume, no
ambiguity anywhere about what just happened."

The field is doing its job when it forbids a legitimate route. Both examples above rule out the
other one.

---

## EXECUTION (visual)

### 6. MEDIUM / SUBSTRATE
What it's made of and made on.

*Strong:* "Warm cream paper, graphite and ink, animator's pencil-test feel, visible paper grain."
*Weak:* "Traditional media." A shelf in an art store, not a material. It leaves the model to pick,
and the model picks the most photographed option.
*Also strong, opposite direction:* "Vector on flat white. No substrate, no ground, no texture. It
was never on anything."

The field is doing its job when a person could go buy the materials.

### 7. THE HAND
How the marks get made.

*Strong:* "Graphite linework, fine cross-hatching for shadow, a faint light-blue construction
underdrawing left visible."
*Weak:* "Loose, sketchy linework." Two adjectives that describe a hundred incompatible hands.
Sketchy how, with what, leaving what behind.
*Also strong, opposite direction:* "No hand at all. Uniform line weight, mechanically even, zero
pressure variation, nothing that betrays a wrist."

The field is doing its job when it names a tool or a specific behavior, not a mood the marks are
in. How far the hand exaggerates its subject is not this field's business; that is REGISTER, and
stating it twice at two altitudes gets it averaged.

### 8. COLOR / LIGHT
The palette discipline, stated as a constraint. The word constraint is load-bearing. Palettes
stated as vibes get widened; palettes stated as counts and bans get obeyed.

*Strong:* "Monochrome graphite and ink throughout, with exactly ONE restrained warm accent. Never a
second accent color."
*Weak:* "Warm, muted, earthy palette." The model reads this as permission for five warm muted
colors, which is the same as no palette. Nothing here says how many.
*Also strong, opposite direction:* "Full saturation, six colors minimum, all of them fighting. No
neutrals anywhere, no color allowed to recede."

The field is doing its job when it contains a number, an "only," or a "never." State what light is
for as well, but keep the halves in their places: a principle about what color is *for* ("color and
light carry the emotional meaning, they never decorate") is a thesis-level claim that travels to
any medium, so it belongs upstairs; the count and the bans stay here.

### 9. THE FINISH
See the worked field above. It is the pattern for this section and the example is real.

### 10. THE ONE MOVE
The single decision that carries the meaning. One move, not a list. If a block has five one-moves
it has none, because the model has no way to know which one to protect when they conflict.

*Strong:* "One warm amber accent on the single element that holds the feeling, plus one soft amber
watercolor bloom behind the figure that bleeds into the paper. The wash sits BEHIND the linework,
never on top, never splatter."
*Weak:* "Make it feel nostalgic." A goal handed back to the model as if it were an instruction. It
says what should happen to the viewer, not what happens on the page.
*Also strong, opposite direction:* "The subject is always drawn one size too large for its frame
and always slightly cropped by it, so nothing ever quite fits."

The field is doing its job when the user could execute it themselves. A real one-move names a
thing done, a place it is done, and a limit on how far it goes.

---

## NEVER DO

The ban list, and the spine of the whole block. Both real blocks behind this schema had nearly
identical never-do lists while their positive halves described completely different pictures, which
is the tell that this section is doing more work than any single field above it.

Every item carries its why. See hard rule 2.

*Strong item:* "No polished, surface-perfect rendering that erases the hand. Everything I love
keeps the fingerprints in, and a flawless surface means the process was hidden or never happened."
*Weak item:* "No AI look." It names a feeling about the output and gives the model no test it can
run. The model does not know which of its own habits produced the feeling.
*Also strong, opposite direction:* "No visible construction, no stray marks, no texture. Evidence
of effort reads as an unfinished job, and I want it to look like it arrived."

The section is doing its job when a reader could correctly apply it to something nobody listed. If
every item only rules out the exact thing it names, the whys are missing and the list will not
generalize past the session that produced it.

Two more things that make a ban list work:

- **Bans come from real kills.** The strongest items are things the user actually rejected on
  sight, phrased in the words they rejected them with. Invented bans read like taste and behave
  like noise.
- **A closing principle is allowed and useful, but it does not replace per-item whys.** "If an
  element can be removed without changing the idea, it does not belong" is an excellent last line.
  It is not a substitute for saying why gradients are out.

---

## Fields that land in more than one place

Filling this out on real material, a few things reliably show up not knowing where to go. These are
the mappings, so nobody has to rediscover them.

- **Material and texture.** Splits three ways inside EXECUTION. What it is made on goes to MEDIUM /
  SUBSTRATE, how the marks get made goes to THE HAND, and whether the searching marks survive goes
  to THE FINISH. "Preserve evidence of making" is a finish rule wearing a materials coat.
- **Color and light.** Splits across both altitudes. What color is *for* ("it carries the emotional
  meaning, it never decorates") is a claim about meaning, so it sits in INTENT alongside the thesis.
  The operational half (how many colors, which one, what is banned) is EXECUTION 8. Written in one
  place only, it loses either its reason or its teeth.
- **Character and emotion.** The positive half ("emotion reads through silhouette and scale, faces
  can underplay") is NARRATIVE STANCE. The negative half ("do not let characters explain the
  feeling with obvious expressions") is NEVER DO.

Anything that lands in two places gets its positive written once, in the field that would still
need it if the other were deleted, and its negative restated in NEVER DO. Restating a ban is not
redundancy. It is the only part of the block that survives an aggressive summarizer.
