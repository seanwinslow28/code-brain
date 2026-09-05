# Medium contract: X (Expressive lane)

Wave 1 ([#166](https://github.com/seanwinslow28/code-brain/issues/166)).

**Lens: [Observer](../../interview/observer.md) — on the standalone route only. The reactive route
runs no lens and no interview** (see `## How a post is sourced`,
[#249](https://github.com/seanwinslow28/code-brain/issues/249)). Corrected 2026-09-04 on the wave-1 run
([#232](https://github.com/seanwinslow28/code-brain/issues/232)); it was **Skeptic**, ruled in
[#226](https://github.com/seanwinslow28/code-brain/issues/226) on the reasoning that room 1 means one
landed claim with no arc to soften it. The run proved the pairing incoherent. Skeptic worked exactly
as designed — a narrow claim, a sample, a retraction condition — and the post came out as evidence.
Sean's verdict: *"That looks more like a Resume bullet point than a funny observational tweet."*

The tell was in this file the whole time: **all thirteen moves below are comic**, and an evidence
transcript makes none of them reachable. The lens was pulling against its own roster. It also reached
past the sentences — because Skeptic needs measured evidence, it filtered which of his week's
material was even eligible to become a post.

A room-1 post is one landed *thing*. #226 read that as a claim; it is more often a **noticing**.
Skeptic remains right for a post that genuinely argues something, and naming a second lens for that
case is a ruling by Sean, not a line in this file.

**Status: corrected by the #232 run, re-routed by the #249 ruling.** The run produced no shipped post
— it was stopped at the gates when the shape came out wrong, which is what a first run is for. The
contract has been corrected; X has still never shipped a post. The sourcing routes below are **ruled
and unbuilt**: the plumbing is [#250](https://github.com/seanwinslow28/code-brain/issues/250), and
until it lands X cannot run at all.

## How a post is sourced — X runs no interview

Ruled 2026-09-04 ([#249](https://github.com/seanwinslow28/code-brain/issues/249)). X was the first
medium to reach stage 2 and find nothing there to excavate. An interview exists to draw out material
only the author has; a reactive post's material is **someone else's post, already on the screen**,
and the interviewer knows no less about it than he does. Sean's ruling: *"Asking multiple questions
for an X post that would span between 5 to 50 words is over the top."* The reactive median is six
words ([#247](https://github.com/seanwinslow28/code-brain/issues/247)).

X therefore has **two routes, neither of them an interview.** The machine drafts on both.

### Route 1 — autonomous (the default)

The machine searches Sean's own logged-in X, picks stimuli, builds a stimulus block, drafts cold, and
hands back a deck of candidate posts. **No input from him at all.** This is the route the machine
exists for — posts getting out while he is busy with something else — and it is the only
configuration that ever tests the shaper on the thing it is meant to do. A reactive post's take *is*
the post, so a machine handed the take is arranging six of his words, which is not a service.

Authenticated access is solved and already installed: `last30days` reads the `auth_token` / `ct0`
session cookies out of the local browser (`scripts/lib/vendor/bird-search/lib/cookies.js`, via
`@steipete/sweet-cookie`) and calls X's GraphQL `SearchTimeline`. No password is stored. #247's "no
unauthenticated path" finding is true and irrelevant — the path is authenticated. Three standing
caveats: the cookies rotate and a run re-reads them, the endpoint is internal and can break without
notice, and the session lives on whichever machine he is logged into, which is the MacBook Pro.

**Manual paste is not a route.** A flow where Sean finds the post himself and hands it over was
considered and rejected by him: if he is already looking at the tweet he already has the line, so the
machinery buys nothing and costs steps.

### Route 2 — brainstorm

When he has a seed and wants it pushed somewhere he had not thought of. **Divergence first**, many
candidate lines, back and forth until one lands — never one output, never an interview. The model is
`anima/.claude/skills/brainstorm-front-door` (micro-expand always on, alternate premises before any
question is asked, every lock carrying his verbatim reason).

This is L8-legal by the 2026-09-02 amendment: a persona that generates **candidates he rules on** is
the rule's own sentence; only a persona that produces a *score* is banned.

### The stimulus block

Route 1's stage-2 artifact, replacing the transcript. Git-ignored, beside the transcripts.

```
STIMULUS BLOCK — <slug> — <date>
Source: <permalink>
Author: <@handle>
Post: <verbatim text, fetched through publish.x.com/oembed>
Media: <what any attached image or video shows>
Surface: reply | quote-post
```

**It carries nothing from Sean.** If the draft turns out to need a fact about his week, that goes on
the ASK LIST and comes back as a one-line answer stored as a separate mini-transcript — never folded
into the block. The two files have **opposite polarity** and must never be merged; see `## Gates`.

**The blind line, optional.** When he has time, he writes his own version of a post *without reading
the machine's*, and whichever one he posts is the scoreboard. Sentence-survival percentages are
meaningless at six words; whose line shipped is a clean binary that accumulates weekly. Same blind
design that made [#221](https://github.com/seanwinslow28/code-brain/issues/221) trustworthy. When he
skips it the machine still ships a draft — that is the machine doing its job.

## Governing documents, in precedence order

1. [`LANE.md`](LANE.md) — Expressive-lane law (the first-screen test, the reply-hook memo).
2. [`../move-licensing.md`](../move-licensing.md) — the shared matrix.
3. This contract.

## Licensed moves: thirteen, all of them sentence-sized

Budget heat 3, room 1. X keeps the full register and gives up all the space:

**Funniest Word Last** · **Shout-Caps** · **Rule of Three + Emotional Pivot** ·
**Pop Culture Anchoring** · **Blunt-Literal Description** · **Reader-Dismissal** ·
**Equation / Formula Defamiliarizer** · **Borrowed Canon Line** · **Faux-Ignorance Aside** ·
**Affectionate-Insult Epithet** · **Fumbled Idiom** · **Zeugma Paint** · **Character-Intro Verdict**

Two things follow, and both are worth stating plainly.

**X is the only Expressive medium that keeps heat 3.** The bodily, profane, insulting register is
licensed here in full. Nothing about the medium asks him to behave.

**X gets no whole-piece moves, so a post has no arc.** Everything that needs a beat or more is banned
by room: no Mid-Action Open, no Callback Closer, no Self-Deprecation as Structure, no Inverted
Refrain, no Sincerity Punished by the World, no Comic Under-Reaction. A post is one landed sentence,
not a small essay. **The move that would have carried the ending is not available**, which is the
real constraint of the medium and the reason most people's posts read as amputated blog paragraphs.

**Equation / Formula Defamiliarizer is licensed here and almost nowhere else** — its restriction is
short-form, and this is short-form ([#175](https://github.com/seanwinslow28/code-brain/issues/175)).
X is its home.

**Screenwriting Cut-To is banned**, ruled against the axes: a single post has no room to establish
the stated intent before turning on it, so the notation ends up doing work the setup should have done
([#162](https://github.com/seanwinslow28/code-brain/issues/162)).

## Threads, and the honest limit

A thread is the obvious way to buy room, and **this contract cannot grant it.** The matrix is a
shared reference that contracts may narrow and never widen; lifting X to room 2 would license a
dozen beat-sized moves across every piece of machinery that reads the matrix. If threads should
unlock those moves, that is a **budget change on the matrix, ruled by Sean**, not a line in this file.

Until then: a thread is a sequence of posts each obeying room 1. That is a real constraint and it is
probably the right one — a thread whose beats only work in sequence is a blog post that has been
chopped up, which is the anti-pattern below.

## First screen

The surface the [lane's first-screen test](LANE.md#the-first-screen-test) runs against:

- **The post itself**, up to the "Show more" fold. In a thread, the first post — nobody expands post
  one to decide whether to read post two.
- The attached image is part of the first screen, not decoration
  ([#170](https://github.com/seanwinslow28/code-brain/issues/170)).

**What the fold actually is** (corrected 2026-09-04,
[#247](https://github.com/seanwinslow28/code-brain/issues/247)). It is a CSS `-webkit-line-clamp`:
**rendered lines, counted after layout** — not characters, not height. Every clamp X ships is one of
{1, 2, 3, 4, 5, 10} lines, and the stylesheet carries responsive variants keyed to viewport width, so
**the fold genuinely differs between a phone and a desktop**. X documents it nowhere; that is a
finding, not a gap in the searching.

Three consequences, and the third is the one that changes how the test is run:

1. **Do not write to a number.** The top-level timeline value is not observable without a login. The
   only clamp large enough to be a long-post fold is `line-clamp-10`, which is *consistent with* ten
   lines and was never seen applied. Every "the fold is at 280 characters" claim traceable through
   search came from marketing blogs citing nothing.
2. **Lines, not characters, means the same post folds differently at different widths.** A post that
   clears the fold on a desktop can be cut on a phone by nothing but a narrower column.
3. **The fold is a timeline behaviour, not a property of the post.** On a logged-out permalink a
   ~4,000-character post rendered in full with no "Show more" at all. So the first-screen test is a
   test of how the post arrives *in a feed*, and reading your own permalink will not run it.

**Reply surface: yes.** Replies and quote-posts. The
[reply-hook memo](LANE.md#the-reply-hook-memo-advisory-never-a-gate) ships with every post — it is
about *inbound* replies to this piece, and is untouched by everything below.

**Reply and quote-post are not the same surface** (established 2026-09-04,
[#247](https://github.com/seanwinslow28/code-brain/issues/247), read off the current ranking code
`xai-org/x-algorithm`; `twitter/the-algorithm` is superseded and its published weights are all
zeroed defaults, so the "reply = 13.5" figures in circulation quote a training file, not production).

A **reply** is filtered out of the feed of anyone who does not already follow the author, **with no
exemption for who was replied to** — the retired Scala stack had exactly that exemption and it is
gone. It also takes the 0.75× out-of-network discount *even in-network*, and the +15.0 mutual-follow
boost on replies applies to originals only.

A **quote-post** carries no `in_reply_to_tweet_id`. The filter never sees it, the discount never
applies, and it is ranked as an original. Both are weighted 5.0; a like is 0.5.

So the same sentence, aimed at the same post, travels or does not travel depending on which button
made it.

## Format

- One post carries one thing. If it carries two, it is two posts, and probably one of them is better.
- Length is bounded by the fold, not the character limit — and the two are independent quantities,
  not a strict and a loose version of one bound. The character limit is 280 **weighted** characters
  (Latin text weighs 1, CJK and emoji weigh 2), every URL counts as a flat 23 however long it really
  is, and attached media costs 0. See `## First screen` for what the fold is; it is measured in
  rendered lines and it is the one that binds first.
- No hashtags. No engagement questions. No "🧵" as a promise the thread does not keep.
- **Quote-post when the line should travel; reply when you actually want the conversation.** This is
  the one format rule that is about the button rather than the words, and it exists because the
  asymmetry above is large and invisible. It is not a rule to always quote-post: a reply is a remark
  *to* a person, a quote-post is a remark *about* them in front of an audience, and at heat 3 that
  distinction has teeth. An Affectionate-Insult Epithet lands as banter in a reply and can land as
  a pile-on when broadcast. Pick the surface for what the line is doing, then know what it costs.
- **The craft survives the switch.** A quote-post still displays the post it answers, so the
  stimulus-as-setup mechanic is intact: the thing being answered is doing the work a standalone post
  would have to spend words building. Nothing about the joke changes.
- **Links do not currently suppress reach.** Corrected 2026-09-04 against the current ranking code
  ([#247](https://github.com/seanwinslow28/code-brain/issues/247)); this line previously asserted
  that they did. The claim was **true history stated in the present tense**: NDSS 2026 measured
  4–8× lower normalised visibility for link posts on 2022–24 data, and Musk confirmed the practice
  in November 2024. It stopped being true since. The live ranking path
  (`xai-org/x-algorithm`, the current repo — `twitter/the-algorithm` is superseded and its published
  weights are all zeroed defaults) carries **no link penalty anywhere**, and its only link term is
  `OpenLinkWeight = +0.2`, positive.

  This is a fact about the platform, and platform facts rot. Re-check it before leaning on it; the
  research note records how, and the method is cheap.

  The writing rule it was attached to survives on its own merits and is unchanged: **where a post
  exists to carry a link, that is a cut of an artifact, and the cut still has to stand on its own
  as a post.** A post that is only a delivery vehicle for a URL was never worth posting, whatever
  the algorithm does with it.

## Negative specimens — what this must never look like

- **The chopped blog post.** A thread whose posts are paragraphs, where post 3 makes no sense without
  post 2. The room-1 rule exists to stop exactly this.
- **Engagement bait.** "Unpopular opinion:", "Nobody talks about this", "Here's what nobody tells
  you about agents 🧵". A hook that promises a secret and delivers a summary.
- **The listicle thread.** "7 lessons from building an agent fleet." Depth on one thing beats a
  survey of seven, here as everywhere.
- **The lecture.** A prescription to an audience of builders from one run of one experiment. This is
  `writing-critique`'s **false authority** tell, and X is where it is cheapest to commit and most
  expensive to be caught.
- **The recycled line.** X is the medium most likely to reach for a line that already worked
  somewhere else. The one-artifact rule applies: `gates/coined_lines.py`.

## Gates, in order

**Post-draft and advisory as of 2026-08-31** (the rules-off re-scope: nothing below is a drafting-time constraint any more). Order: **origin (inverted, below) → do-not-promote + coined-lines sweep → humanity scrub → critique (false authority only)**.

**At six words a gate's cost is not runtime, it is a false finding.** Every gate here runs in
milliseconds and prints nothing most of the time; the only expensive thing in the loop is Sean's
attention. That is what the chain was trimmed against
([#249](https://github.com/seanwinslow28/code-brain/issues/249)).

### The origin gate inverts on X

A cold draft has no transcript, and **the stimulus block must never be indexed in place of one.** The
gate clears any draft atom it finds in the indexed region; point it at the stimulus and it would
clear every phrase lifted from the person being answered — turning the gate from a leak-catcher into
a leak-licenser. That is [#166](https://github.com/seanwinslow28/code-brain/issues/166)'s *borrow
structure, never strings*, and a reactive post is where the risk is highest because the source text
is right there.

So the block is a **forbidden-strings source, not a permitted-vocabulary source**, and the gate's
question changes from *did these words come from Sean* to *did these words come from the person he is
answering, and is he claiming something about himself he never said*. Three rules:

1. **No claim about his week.** A cold reactive post asserts nothing about his fleet, his numbers, his
   month. Not "untraced" — out of scope for the form. Roughly checkable as first person plus a number,
   date, or proper noun.
2. **When the post genuinely needs one, ASK LIST.** One question, one line back, stored as a mini
   transcript — which *is* indexed normally, and the claim is then traced. Deleting the beat is the
   more expensive mistake ([#164](https://github.com/seanwinslow28/code-brain/issues/164)).
3. **No lifted phrasing from the stimulus.** `gates/coined_lines.py` pointed at the block's post text;
   its 80% token-overlap threshold already draws the right line — shared vocabulary passes, a lifted
   run does not.

The reading pass for recombination still runs. Expressive lane advises and never blocks.

### The rest of the chain

- **Do-not-promote + coined-lines** — X needs these *most*. Its own negative specimens name the
  recycled line as the medium's signature temptation, and a heat-3 six-word post is exactly where a
  suppressed topic slips out. Coined-lines does two jobs here: the one-artifact rule and the stimulus
  overlap above.
- **Humanity scrub** — runs, expected silent. Most of its thirty tells are essay-scale.
- **Critique — false authority / operator credibility only.** Structure and hiring signal mean nothing
  at six words. False authority means a great deal: *the lecture* is this contract's named failure,
  cheapest to commit here and most expensive to be caught at.
- **The analyzer does not run on X.** Both its bands are built from essays and X has no series in
  either, so it cannot produce a meaningful reading of a six-word post — and the #232 run showed it
  firing `[FLAG: monotonous, CV < 0.45]` on a 51-word draft, the exact case its own docs promise to
  suppress for insufficient length. It returns when X has shipped enough posts to build a band. (The
  underlying length-guard bug in `references/analyze.py` still bites short drafts in other mediums and
  stays on the #232 defect list.)

## Delivery

A ship packet: the post or the thread, the image if there is one, the reply-hook memo, and any open
items. The machine never posts.

## What this contract does not own

Whether the thing is worth saying (`substack-value-engine`), the sentences
(`writing-voice-modes`), or the decision to post (Sean).
