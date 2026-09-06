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

**Status: corrected by three runs.** ([#231](https://github.com/seanwinslow28/code-brain/issues/231)'s
vocabulary, which the previous line sat outside of.) #232 ran the chain and was stopped at the gates
when the shape came out wrong, which re-routed the lens and plumbed route 1 via #249 and #250.
[#246](https://github.com/seanwinslow28/code-brain/issues/246) ran the standalone route under
Observer all the way to a hand-rewritten final. The third correction is the first route-1 deck
([#255](https://github.com/seanwinslow28/code-brain/issues/255), amended by
[#258](https://github.com/seanwinslow28/code-brain/issues/258)): eight drafts, four picked, and all
four cuts turned out to be one thing — see `## Stance and aim`. **X has still never shipped a post** — #246's final
is written, gated and rewritten, and waiting on a body of posts rather than on the machine.

Route 1 is built and smoke-tested end to end ([#250](https://github.com/seanwinslow28/code-brain/issues/250),
2026-09-05): `x/stimulus.py` runs the authenticated sweep, fetches verbatim post text through
oEmbed, writes the stimulus block, and both gates read the block in its inverted polarity. What it
searches on and how big a deck is were ruled the same day
([#251](https://github.com/seanwinslow28/code-brain/issues/251)): a **27-account watchlist in three
lanes**, and a deck of **eight ranked stimulus-and-draft pairs**. Both are below. **No post has
run through it yet** — the first is [#246](https://github.com/seanwinslow28/code-brain/issues/246).

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

Authenticated access is solved and already installed: `last30days` vendors an X client
(`scripts/lib/vendor/bird-search/`) that calls X's GraphQL `SearchTimeline`. No password is stored.
#247's "no unauthenticated path" finding is true and irrelevant — the path is authenticated. Three
standing caveats: the cookies rotate and a run re-reads them, the endpoint is internal and can break
without notice, and the session lives on whichever machine he is logged into, which is the MacBook
Pro.

**Where the cookies actually come from, corrected on the #250 build.** The ruling said the client
reads them out of the local browser via `@steipete/sweet-cookie`. Measured on the MacBook Pro
2026-09-05: **all three browser paths fail.** Safari returns `EPERM` on
`Cookies.binarycookies` (the reader has no Full Disk Access), Chrome's reader throws
`Value is too large to be represented as a JavaScript number` on a WebKit cookie timestamp — a
`node:sqlite` integer bug, not a login problem, so it fails whether or not he is signed in — and
Firefox has no profile. What works is the credential file `last30days`' own setup wizard writes,
`~/.config/last30days/.env`, and `x/stimulus.py` resolves in that order (process env → project
`.claude/last30days.env` → global `.env` → browser). One consequence worth writing down: **a
rotated session is fixed in one place on this machine, not two.** If `stimulus.py auth` says the
stored cookies were rejected, re-run the `last30days` setup wizard; nothing in the content machine
holds a second copy.

```bash
python3 .claude/skills/content-machine/x/stimulus.py auth
python3 .claude/skills/content-machine/x/stimulus.py sweep --query "<query>" --count 20
```

#### What it searches on: a watchlist, in three lanes

Ruled on [#251](https://github.com/seanwinslow28/code-brain/issues/251). The sweep reads
`creative-studio/content-machine/watchlist.md` — git-ignored, per-machine, seeded from the 19
accounts in [#247](https://github.com/seanwinslow28/code-brain/issues/247).

Not the follow graph, and **not open keyword search**, which is out on measurement:
`"claude code" -filter:replies min_faves:20` returned 8 of 8 engagement bait or non-English, and the
engagement floor made it *worse* — high engagement on a keyword selects for bait by construction.
That is [#170](https://github.com/seanwinslow28/code-brain/issues/170)'s vendor-SEO finding arriving
on a third engine.

| Lane | Job | Found by |
|---|---|---|
| **A — Experimenters** | stimulus + learning | second ring, **outbound only**: `from:<handle> filter:replies` |
| **B — News / watchers** | learning | artifact search — the thing a watcher posts, never a ranking |
| **C — Reach** | quote-post distribution | accounts Lane A engages with, **admitted by eye** |

**Direction beats volume, measured.** `from:simonw filter:replies` returns real people he answers.
`to:karpathy min_faves:30` returns a crypto shill and a raw ETH address — an engagement floor does
not save it, because reply-spam aimed at a mega-account collects likes by construction. Harvest
outbound. Never inbound.

**Lane C cannot be gated by a number, and the first harvest is why.** The top-scoring candidate on
every available metric — most vouchers, highest recent reach, ahead of every real name — was an
antisemitic edgelord account. Two rules came out of it: **a reply is not an endorsement** (a Lane A
account replying to someone can be an argument or banter with a shitposter, so the second ring
generates candidates and never vouches for them), and **reach selects for outrage, because that is
what reach means**. Harvest mechanically, admit by hand, keep the rejections so the next sweep does
not re-propose them.

The watchlist also serves a second consumer later — the Oracle's news lane, deferred to
[#252](https://github.com/seanwinslow28/code-brain/issues/252) until Oracle graduation, so week 2
measures one changed mechanism rather than two.

#### The deck: eight ranked pairs

```bash
python3 .claude/skills/content-machine/x/stimulus.py watchlist
python3 .claude/skills/content-machine/x/stimulus.py deck --days 3 --size 8
```

`deck` returns the **pool**, not the deck: retrieve wide across all three lanes, narrow to the top
eight downstream. Queries run per lane and cap at two posts per account, because a single OR chain
returns whoever posted most — a 14-handle chain measured 40 posts of which 17 were one voice, and a
deck of eight with three from one account is not a deck.

Then, in order:

1. **Rank the pool, take eight.** Ranking candidates is not the draft-scoring loop L8 bans
   ([#169](https://github.com/seanwinslow28/code-brain/issues/169)). Ranked so he can stop early.
2. **`block` each pick**, which re-fetches verbatim text through oEmbed.
3. **Draft one candidate per stimulus, in an isolated clean-context spawn.** One per block, not
   eight in one context: [#221](https://github.com/seanwinslow28/code-brain/issues/221) measured that
   same-context generation converges, so eight drafted together become variations of the first.
   **One draft per stimulus, deliberately** — several candidates per stimulus is
   [#228](https://github.com/seanwinslow28/code-brain/issues/228), which needs this as its baseline.
4. **Hand back eight ranked pairs**, each draft shown with the post it answers. A reply is
   unreadable without its setup, so the pair is the unit — roughly forty words each.

**Eight is a measurement, not a ruling.** The hit rate is unknown and
[#248](https://github.com/seanwinslow28/code-brain/issues/248) cannot supply it, because that was an
exercise where he wrote on all twelve and rejected none. The size the record sets is the size. The
failure being sized against is not "too long to read" — it is #227's week-1 Oracle deck being denied
in full, and machine work is nearly free while his attention is not.

**Manual paste is not a route.** A flow where Sean finds the post himself and hands it over was
considered and rejected by him: if he is already looking at the tweet he already has the line, so the
machinery buys nothing and costs steps.

### Route 2 — brainstorm

When he has a seed and wants it pushed somewhere he had not thought of. **Divergence first**, many
candidate lines, back and forth until one lands — never one output, never an interview.

**Route 2 is a pointer, not code** — confirmed on the #250 build, which is what that ticket asked
before anything got written. It points at `creative-partner`'s **divergence stage**, and the pointer
had to be corrected: `anima/.claude/skills/brainstorm-front-door` is the *model* the ruling named and
it is **not invocable from here.** It lives in a different repository (`~/Code-Brain/anima`), it
emits a brief bundle for the anima pipeline rather than candidate lines, its own header says *"do not
invoke it from another skill"*, and `creative-partner`'s description already routes anima brief
sessions away from itself and to it. Naming an out-of-repo skill as the route is how a session ends
up trying to call something that is not there.

The in-repo equivalent is ratified and matches the ruling's shape move for move: four isolated
generators wearing different frames plus one critic, frame selection offered and confirmed before
dispatch, and the sentence that makes it L8-legal written into the skill itself — *"machines write
candidates; Sean writes fates."* Its stated cost is ~5 calls per run and the spend is always his
choice, which is the honest reason this is a pointer: route 2 is an interactive session he opens, not
a script the machine runs.

This is L8-legal by the 2026-09-02 amendment: a persona that generates **candidates he rules on** is
the rule's own sentence; only a persona that produces a *score* is banned.

### The stimulus block

Route 1's stage-2 artifact, replacing the transcript. Git-ignored, **beside** the transcripts in a
directory of their own: `creative-studio/content-machine/stimulus/`.

```
STIMULUS BLOCK — <slug> — <date>
Source: <permalink>
Author: <@handle>
Post: <verbatim text, fetched through publish.x.com/oembed>
Media: <what any attached image or video shows>
Surface: reply | quote-post
```

```bash
python3 .claude/skills/content-machine/x/stimulus.py block <status-url> \
    --slug <slug> --surface reply|quote-post [--media "..."]
python3 .claude/skills/content-machine/x/stimulus.py check <block.md>
```

**Its own directory, not a filename convention inside `transcripts/`** (ruled on the #250 build). The
two files have opposite polarity, and the failure mode is a tab-complete: one wrong path argument
turns the origin gate from a leak-catcher into a leak-licenser, silently, with a clean-looking
report. Three independent guards, because one is not enough for a mistake that leaves no trace — a
separate home, the `STIMULUS BLOCK` sentinel on line 1, and a hard refusal (exit 2) in
`origin_check.py` when a file carrying that sentinel is handed over as a transcript.

The sweep's own text is never the record. Every block **re-fetches** through oEmbed before writing
anything down — the same discover-then-verify method that took #247's 79 URLs to 79 clean returns —
and the block records what the channel could not give: oEmbed returns no media (so `Media:` is
supplied by hand or reads `none`), and it truncates long posts at the embed limit, which the block
flags on a `Fetch:` line rather than leaving a `…` to be read as the author's own ellipsis.

**It carries nothing from Sean.** If the draft turns out to need a fact about his week, that goes on
the ASK LIST and comes back as a one-line answer stored as a separate mini-transcript — never folded
into the block. The two files have **opposite polarity** and must never be merged; see `## Gates`.

**What the shaper is handed** (ruled 2026-09-06 on
[#255](https://github.com/seanwinslow28/code-brain/issues/255), the route's first real run). The
block goes into the clean context **verbatim, labelled as the thing being answered**, and with no
prohibition attached. You cannot write a reply to a post you cannot see, so the drafting context
necessarily receives the exact text the gates treat as forbidden — the polarity trap one stage
upstream of where a gate can look. Three shapes were considered and Sean ruled the first: the block
as-is with the gates catching lifts afterwards; the block plus an explicit *"do not reuse its
wording"*; or a paraphrase the shaper could not lift from. The prohibition lost because the
2026-08-31 re-scope empties the shaping context of style rules on measured evidence, and one
re-added rule is how that erosion starts. The paraphrase lost on craft: a reply lands against the
exact rhythm of what it answers, so a reply written to a paraphrase is a reply to a different post.

**The label is form, not style** — the same class as the deliverable bounds the shaper already
gets. It says *this is the post you are replying to*; it never says what to do about it.

**One sentence now rides with it** (added 2026-09-06,
[#258](https://github.com/seanwinslow28/code-brain/issues/258)): *"Write the reply that agrees with,
extends, or answers this post. If the line costs someone something, it costs you."* That is
`## Stance and aim` compressed to a description of the deliverable — what kind of object a reply is —
and it is in the context because **no gate can see where a joke points**. Origin, coined-lines,
humanity and critique are all blind to it; without the sentence the only enforcement point is Sean's
pick step, which is what the first deck's four cuts cost. It is the first addition to the emptied
shaping context since the block label itself, and the whole budget this ruling spends there. See
`SKILL.md`, "The shaping context". **If the next deck does not clear 4 of 8 stance-legal, the
sentence is not the lever** and the route is more paired samples rather than more rules.

**First measurement, same run:** eight drafts, **0 lifted runs, 0 unsourced first-person claims**,
`coined_lines.py` clean against both the stimulus and the ledger on all eight. The unconstrained
context did not lift, which is the evidence this ruling stands on. One run — re-read it after the
next few decks rather than treating it as settled.

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

**X is the only Expressive medium that keeps heat 3, and the reason is the audience, not the
manners.** No recruiter is reading. A joke that would end a cover letter is fine here, and that is
exactly what heat measures — Sean, 2026-09-06: *"I'm not dealing with recruiters, so I don't have to
worry about professional language and being buttoned up."* The bodily and profane register stays
licensed in full.

**Heat is volume. Aim is a separate axis**, ruled 2026-09-06 in `## Stance and aim` below. The
previous version of this line said *nothing about the medium asks him to behave*, which conflated the
two and is now wrong in a specific way: the medium does not ask, and he ruled anyway. The *insulting*
third of the register is aimed from now on, not free. The proof that the axes are independent is his
own: the loudest specimen in the corpus is a benchmark table swapped for his own bodily failings —
heat 3 at full volume, with every ounce of the negative landing on himself.

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

## Stance and aim

Ruled 2026-09-06 on [#258](https://github.com/seanwinslow28/code-brain/issues/258), against the first
route-1 deck ([#255](https://github.com/seanwinslow28/code-brain/issues/255)). Two rules, and they do
different jobs.

**Rule 1 — the reply stands with the post.** It agrees with it, extends it, or answers it. It never
contradicts or undercuts the frame the poster posted in.

**Rule 2 — if a line leans negative, it lands on Sean.** People are never the ones put down. Machines,
tools, companies, releases and trends are fair game; a person is not.

### Why it is stance and not targeting

The ticket opened on the wrong axis and the deck falsified it. The proposed rule was *who pays for
the joke* — a machine is fine, a person is not — and the cut draft answering @steipete aimed squarely
at a machine, while the picked draft answering @geoffreylitt aimed at a machine too. Target does not
separate them. What separates all eight is where the reply **stands**:

| | What the poster was doing | What the draft did | |
|---|---|---|---|
| complaint about slop | complaining | agreed, added an image | **pick** |
| joke about his own agent | joking | extended his joke | **pick** |
| enthusiasm about building | enthusing | agreed, then took the hit himself | **pick** |
| a genuine question | asking | answered it | **pick** |
| proud of a thing he built | proud | called the thing a liar | cut |
| reporting a lab's claim | reporting | dunked the claim | cut |
| pitching an idea | pitching | took the idea as a threat | cut |
| excited about four releases | excited | called them all the same | cut |

Self-deprecation is not the axis either: the self-directed pick agrees *first*, and one of the cuts
is arguably self-directed too. **Agreement is the load-bearing half; the self-directed hit is what
you do once you are standing in the right place.**

Sean's ground for it was reputational rather than craft — his favourite of the eight was the
funniest of the eight. He does not want to put anyone down or make anyone feel stupid, and a reply
reads as hostile when it shows up to disagree with something the poster was happy about, whoever the
joke names.

### Scope

**Rule 1 binds wherever a stimulus exists** — replies and quote-posts, route 1 and any reactive post
however sourced. It is not *excluded* from the standalone route so much as **inapplicable** there: a
standalone post has no post to stand with.

**Rule 2 binds all of X.** It has nothing to do with how the post was sourced.

### Aiming notes on two moves

No move was delicensed. Nothing in the roster caused the four cuts, the two obvious suspects were
never reached in sixteen cold reps ([#248](https://github.com/seanwinslow28/code-brain/issues/248)'s
coverage note), and nothing reads the matrix at runtime anyway
([#222](https://github.com/seanwinslow28/code-brain/issues/222)) — so a ban would have cut moves the
failures did not use and left the failures legal. Two moves get an aiming note instead, because the
reply surface changes their mechanism:

- **Reader-Dismissal** — the move contradicts the reader's assumption. In an essay the reader is a
  stranger; **in a reply the reader is the person being answered**, so the move collides with rule 1
  by construction. It only lands when the objection belongs to a third party — a lurker, not the
  addressee. This is a *form* problem, the same class as "X gets no whole-piece moves," not a heat
  problem.
- **Affectionate-Insult Epithet** — the vocative points anywhere except the person being replied to.
  The construction is fine about a third party and is rule 2 when aimed at the addressee. This
  sharpens the `## Format` note that the same epithet reads as banter in a reply and a pile-on in a
  quote-post.

**Reopen trigger.** A deck failure that a delicensing would have caught and an aiming note did not.
One specimen, not a hunch.

### On watch, not ruled

All four picks were replies and **both quote-posts in the deck were cut**. Both also broke rule 1
independently, so there is no evidence the *surface* did anything, and n=2. Watch it across the next
few decks before anyone writes a rule about the button.

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
- **The causal link has to be structural, because there is no beat to carry it.** Two things placed
  in sequence read as *and then*, and a room-1 post has no arc in which to turn that into *but* or
  *therefore*. So the connection is made inside the sentence — the two things simultaneous, or one
  plainly causing the other — or the reader is left to infer it and does not.

  Earned on the Observer run ([#246](https://github.com/seanwinslow28/code-brain/issues/246)). The
  draft listed a run of physical actions in order and then named the thing they were supposed to add
  up to, leaving the reader to supply the link. Sean's verdict: *"it just feels like there's no
  connection."* His rewrite put the two halves in the **same clause, at the same moment**, and the
  connection stopped needing to be inferred. The piece itself stays in the private brain.

  **This rule is not new and that is the finding.** `storytelling-architecture` mechanic 1 — the
  but/therefore test — already names the dead *and then* seam, and mechanic 6 tests the turn inside a
  beat. Both run on a **beat map**, and a one-sentence post never gets one, so the rule was true and
  structurally unreachable in this medium. It is promoted here rather than duplicated there
  (`SKILL.md`, "A ratified lesson is not automatically a new rule").
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

```bash
python3 .claude/skills/content-machine/gates/origin_check.py <draft.md> \
    --stimulus <block.md> [--transcript <mini-transcript.md>]
python3 .claude/skills/content-machine/gates/coined_lines.py <draft.md> \
    --lane expressive --artifact <slug> --stimulus <block.md>
```

**Two exemptions widen the claim check and neither widens the forbidden set** (built #250). A claim
token that appears in the post is exempt, because the post supplies the subject and a number he is
answering is not a claim about his week — and a lift of that number is caught by rule 3, which is the
check that owns the case. The block's `Author:` handle and `Media:` gloss are exempt for the same
reason: naming the person you are answering is the form, and describing a picture both of them can
see is not an assertion about him. The forbidden-strings source stays the `Post:` field alone.

Origin's own lift check and rule 3 overlap on purpose and measure different things: origin flags a
contiguous run of three content words with the connective tissue collapsed out (a reworded lift),
`coined_lines.py` windows a whole line at 80% (a paraphrased one). Neither alone is the check.

The reading pass for recombination still runs. Expressive lane advises and never blocks.

### The rest of the chain

- **Do-not-promote + coined-lines** — X needs these *most*. Its own negative specimens name the
  recycled line as the medium's signature temptation, and a heat-3 six-word post is exactly where a
  suppressed topic slips out. Coined-lines does two jobs here: the one-artifact rule and the stimulus
  overlap above.

  **The one-artifact half is still unarmed, and the gate now says so out loud.** `coined-lines.md`
  had never existed ([#232](https://github.com/seanwinslow28/code-brain/issues/232)); #250 created it
  with the convention and Sean's unregistered backlog, but a ledger with no `>` lines enforces
  nothing. The gate used to print *"nothing to check against"* and exit 0, which in a GATE RECORD is
  indistinguishable from a clean run; it now prints **UNARMED**. Register at least one line before
  the amortized-ratio run ([#233](https://github.com/seanwinslow28/code-brain/issues/233)) — one
  interview feeding five posts is exactly what manufactures this contract's own *recycled line*.
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
