# Medium contract: X (Expressive lane)

Wave 1 ([#166](https://github.com/seanwinslow28/code-brain/issues/166)).

**Lens: [Observer](../../interview/observer.md).** Corrected 2026-09-04 on the wave-1 run
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

**Status: corrected by the #232 run.** The run produced no shipped post — it was stopped at the gates
when the shape came out wrong, which is what a first run is for. The contract has been corrected;
X has still never shipped a post.

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
[reply-hook memo](LANE.md#the-reply-hook-memo-advisory-never-a-gate) ships with every post.

## Format

- One post carries one thing. If it carries two, it is two posts, and probably one of them is better.
- Length is bounded by the fold, not the character limit — and the two are independent quantities,
  not a strict and a loose version of one bound. The character limit is 280 **weighted** characters
  (Latin text weighs 1, CJK and emoji weigh 2), every URL counts as a flat 23 however long it really
  is, and attached media costs 0. See `## First screen` for what the fold is; it is measured in
  rendered lines and it is the one that binds first.
- No hashtags. No engagement questions. No "🧵" as a promise the thread does not keep.
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

**Post-draft and advisory as of 2026-08-31** (the rules-off re-scope: nothing below is a drafting-time constraint any more). Order: **origin (claims tier) → do-not-promote + coined-lines sweep → humanity scrub → critique / analyzer**.

The origin check runs `gates/origin_check.py` plus the reading pass for recombination. Expressive
lane advises and never blocks. The do-not-promote sweep runs `gates/coined_lines.py` alongside the
suppressed-topic check.

## Delivery

A ship packet: the post or the thread, the image if there is one, the reply-hook memo, and any open
items. The machine never posts.

## What this contract does not own

Whether the thing is worth saying (`substack-value-engine`), the sentences
(`writing-voice-modes`), or the decision to post (Sean).
