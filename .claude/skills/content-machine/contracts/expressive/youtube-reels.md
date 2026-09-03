# Medium contract: faceless YouTube / Reels scripts (Expressive lane)

Wave 3 ([#172](https://github.com/seanwinslow28/code-brain/issues/172)). The last of the nine.

**Lens: long form — the Substack assignment for the series the video belongs to (Storyteller →
Stakes for a story, Technical Peer → Skeptic for a spine piece). Short form — Stakes → Cold Reader.**
A long video is a post read aloud, so it needs the same transcript the post would need. A sixty-second
cut has room 2 and about 150 spoken words: there is no space to build, so the interview has to arrive
with the consequence already found, and a listener cannot scroll back over an undefined noun.

**Status: unproven.** No channel exists — the only trace of one in the publication is a line in
`SERIES-COMMAND-CENTER.md` reading *add YouTube "if/when real"* — and no video has run through this
contract. Every rule below is reasoned, none is measured. Where this file is silent,
[`LANE.md`](LANE.md) and the publication's own law govern; **do not invent a rule here to fill a
gap.** It hardens on the first real video, the way `substack.md` hardened on the first real post.

## Governing documents, in precedence order

1. The publication's `SOUL.md`, `POSITIONING-AND-EDITORIAL-SPEC.md`, and `CLAUDE.md` — for a Pencil
   & Prompt video, the masthead and house law win, exactly as they do for a post.
2. [`LANE.md`](LANE.md) — Expressive-lane law (the first-screen test, the outside-fact rule, the
   reply-hook memo).
3. [`../move-licensing.md`](../move-licensing.md) — the shared matrix.
4. This contract.

---

## The two forms

The matrix rules **YouTube / Reels as one budget** (heat 3, room 4, twin to Substack) and recorded
that as known coarseness, with the remedy named at the time: *a medium that must differ narrows in
its own contract.* This is that medium, and this is that narrowing.

A sixty-second Reel does not have room 4. It has X's problem — **the move that would carry the
ending is not available** — while a long YouTube piece genuinely is a Substack post read aloud. One
contract, two declared forms:

| Form | Surface | Clock | Room |
|---|---|---|---|
| **Short** | Reels, Shorts, vertical | **≤ 60 seconds** | **2** (narrowed) |
| **Long** | YouTube, horizontal | bounded by padding, not by minutes | 4 (as ruled) |

**The clock is spent at a fixed rate, and that is the whole difference from prose.** Measured
narration runs roughly 150 words per minute, so sixty seconds is about **150 spoken words** — less
than a third of what fits on one screen of a post. Treat 150 wpm as a budgeting estimate only: the
pipeline measures the real duration with `ffprobe` after synthesis, and the measurement wins.

**Three minutes is a routing line, not a rule.** Past roughly three minutes `/faceless-explainer`
hands off to `/general-video`. That is a production fact worth knowing before the interview, because
it decides which pipeline the script is written for.

## Licensed moves

Licensing is not this contract's call; the matrix is. This contract **narrows** it for short form and
inherits it unchanged for long form.

**Long form: 34 licensed, 1 conditional, 1 banned.** The widest roster in the set alongside
Substack.

**Short form: 23 licensed, 1 conditional.** Room 2 drops eleven moves, and it is worth naming them
rather than letting a drafter discover the gap:

- **Whole-piece (room 4), five:** Mid-Action Open · Callback Closer · Self-Deprecation as Structure ·
  Inverted Refrain · Sincerity Punished by the World
- **Runway (room 3), six:** Breath-Mark Rhythm · Jewel Center · Sensory Cascade · Sensory Before
  Numbers · Humor as Trojan Horse · Buried Rotten Beat

What survives into short form: **Funniest Word Last · Unsignposted Pivot · Tool-as-Character ·
Expectation / Instead · Then / Now Narrator · Flat Collision · Short Declarative Drop · Anaphoric
Stack · Hard Cut / Deflation · Rule of Three + Emotional Pivot · Pop Culture Anchoring ·
Hyper-Specific Anecdote · Screenwriting Cut-To · Blunt-Literal Description · Reader-Dismissal ·
Borrowed Canon Line · Faux-Ignorance Aside · Affectionate-Insult Epithet · Comic Under-Reaction ·
Fumbled Idiom · Zeugma Paint · Character-Intro Verdict · Rhetorical Catechism**, plus Shout-Caps
under both conditions below.

**Equation / Formula Defamiliarizer is banned in both forms.** Its restriction is short-form and
[#175](https://github.com/seanwinslow28/code-brain/issues/175) ruled that a spoken script is not
short-form in the sense that matters: the move is read off a page in one glance, and a listener
cannot glance.

**Screenwriting Cut-To is licensed here and this is its only home** — banned on X, conditional on
Substack. And the notation question that
[#162](https://github.com/seanwinslow28/code-brain/issues/162) said would recur, recurs one layer
down: in a script the notation finally has a legitimate place, **the scene boundary in the scene
table**, and it is still banned from the narration line. Nobody says a cut out loud. The turn is
carried by the scene break and the words on either side of it.

**Shout-Caps carries two conditions here, not one.** The matrix condition stands: licensed in
narration the voice performs, banned in scene headings and any production field, because all-caps
there is format convention and not the move. This contract adds the second, from the rule below:
**caps are a note to a performer, not a guarantee.**

---

## The visual track

The new section, and the reason this contract needed one. Every other contract governs an artifact
made of one track. This one governs words that arrive with a picture on top of them.

**The picture has an owner and it is not this contract.** `/faceless-explainer` generates the
narration audio and invents every visual — typography, abstract graphics, diagrams, data-viz. It
captures no websites and no product screenshots by construction. **Art direction is texture:** style
preset, motion, palette, choreography, transitions. Free, downstream, none of our business.

**But a picture can assert a fact, and an assertion is substance.**

> **Any number, date, proper noun, quotation, chart, or reproduction of a real artifact that appears
> on screen is a claim, and it traces to the transcript like any other claim.**

This is the machine's one law reaching the one place it could not previously see. The failure it
stops is specific and it is not hypothetical: a data-viz scene plotting figures nobody measured,
drawn by a model **after** the origin gate has already signed the words off as clean.

**So the script carries on-screen claims, and the pipeline does not invent them.** Every scene in the
deliverable has an `onScreen` field holding, verbatim, any claim-bearing text or figure that appears
in that scene. Empty is a legitimate value and it is the common one. The field exists so
`gates/origin_check.py` can read the visual layer as text, which is the only way a mechanical gate
ever will.

**A chart plots only figures the transcript carries, with the date they were measured.** Same
standard as the portfolio contract's `number`/`date` pair, for the same reason: a figure on screen is
a claim with no author attached and no way for a viewer to check it.

**The picture never renders the words being spoken.** On-screen text that repeats the narration is
kin to the **Doubled Image** anti-pattern ([#158](https://github.com/seanwinslow28/code-brain/issues/158),
run #2) — two channels, one piece of information, and one of them wasted. The picture adds what the
sentence cannot carry, or it stays quiet.

---

## What a spoken script has to survive

Three constraints that no written medium in this set has, and they are what make this the hardest
contract rather than the longest.

**1. A move must survive a flat read.**

The narrator is synthetic and reads everything at the same temperature. On the local $0 path this is
literal: `agents-sdk/lib/markdown_to_speech.py` runs `flatten_emphasis()` before synthesis, and
Kokoro takes one voice at one speed with no emphasis channel. Caps do not shout. Italics do not lean.
A paid engine may perform more, and this contract does not get to choose the engine.

So: **if a move only lands because a voice performed it, the words do the work instead, or the move is
cut.** Comic Under-Reaction, Flat Collision, Faux-Ignorance Aside and Breath-Mark Rhythm all borrow a
reader's inner performance on the page and get nothing here. Emphasis that matters is carried by word
choice and sentence shape. Caps are a note to a performer, not a guarantee — and the failure mode is
not that the move lands badly, it is that **the move silently evaporates and nothing reports it.**

**2. The voice is a narrator, never an impersonation.**

**Cloning Sean's voice is banned in this medium.** The capability is one call away (the ElevenLabs
MCP exposes `create_voice` and `voice_change`), which is exactly why the ban is written down rather
than assumed. A synthetic Sean reading machine-assembled sentences is the machine's original failure
mode moved from the page to the ear, and it is the one version of it a listener has no way to detect.
Undetectable is the property this publication trades against.

**Disclosure lives once, at the channel level** — the about text or the description — and **never
inside a video.** A per-video disclaimer spends the first screen on throat-clearing, and it stages the
machine as an apology, which this series does not do.

**3. The listener cannot re-read.**

Prose lends the reader a second pass and audio does not. A sentence that needs one has failed before
it was spoken. This bounds clause depth, nested qualification, and any construction whose subject
arrives late. It is the honest reason a script is not a post read aloud, and it is the one place the
register legitimately differs from Substack's.

---

## First screen

The surface the [lane's first-screen test](LANE.md#the-first-screen-test) runs against. There are two
and they are not the same screen, because **YouTube and Reels do not decide in the same place**:

- **YouTube: the thumbnail and the title, before a single frame plays.** The click is decided here,
  with no audio and no motion.
- **Reels / Shorts: the first frame and the first ~1.5 seconds of picture and sound.** It autoplays,
  so no thumbnail decision exists at all. The opening *is* the first screen.

**The lane law survives this medium unamended, and the reason is the re-founding.** In prose you open
by moving a sentence up; in video the first shot exists whether you write it or not, since silence on
black is still a first screen. That looks like it breaks *move a beat up, never write one*. It does
not, because after 2026-08-31 **the shot is texture and the beat it depicts is substance**: the
opening image is invented freely like any image, and the beat it lands on is moved, never written.
`LANE.md` is not amended and does not need to be.

**The thumbnail is the one surface not made of sentences**, so the same law is said for pictures:
**the thumbnail depicts a beat the video actually contains.** Not a beat it gestures at, not a beat
it could have had. Clickbait is precisely this rule's failure mode, and it is the only form of
writing-from-nothing that the origin gate structurally cannot see.

**Reply surface: yes.** Comments on both surfaces. The
[reply-hook memo](LANE.md#the-reply-hook-memo-advisory-never-a-gate) ships with every video.

---

## The two entry routes

**Native.** Its own interview, its own transcript, under the standing law. One instruction the other
contracts do not carry: **the interview must reach for what can be shown, not only what can be said.**
A beat with no visible referent is a beat this medium cannot carry, and discovering that at the scene
table is discovering it too late. It goes on the ASK LIST like any other reach the interview missed.

**Cut.** A video made from an existing piece, which is how most of them will start. The rule is
inherited verbatim from the LinkedIn contract
([#171](https://github.com/seanwinslow28/code-brain/issues/171)): **a cut inherits the source
artifact's transcript and may not add a claim the source did not carry**, and it runs
`gates/coined_lines.py` with the **source's** slug, because a cut is the same artifact on a second
surface.

**And one extension this medium forces.** A cut to video adds a whole track the source never had. The
narration is cut *down* from text that already passed the gates, so nothing can launder itself there
— it launders in **the pictures added on top**, which are new content entering after the source's
ledger closed. So: **every on-screen claim in the visual track traces to the source's transcript
too.** Without that clause the cut rule covers the half of this medium that was never at risk.

---

## Format

- **Short form is ≤ 60 seconds. Long form is bounded by padding**, the same test as a post: long
  enough to tell it, then stop. Neither is bounded by a word count; words are how the clock gets
  spent.
- **The deliverable is a scene table, not a screenplay and not the pipeline's JSON** (see Delivery).
- One scene carries one thing. A scene carrying two is two scenes, and one of them is probably better.
- **Numbers are spoken as measured.** Never rounded to sound tidy, never restated in prettier units.
  The real figure is the reason the beat lands.
- **On-screen text never duplicates the narration.**
- Screenplay notation lives in the scene table's structure and never in a narration line.
- No sting, no subscribe bumper, no "if you enjoyed this". A CTA is not a reply hook, and the lane
  already said so.

---

## Negative specimens — what this must never look like

- **The post read aloud.** A Substack piece pasted into a TTS engine with stock graphics behind it.
  The medium has added nothing, and the listener cannot re-read the sentences that were built for a
  reader who could.
- **The explainer voice.** "In this video, we'll explore…" — the generic educational-YouTube register.
  It is the medium's own house style, it is nobody's voice, and it arrives by default unless something
  stops it.
- **The talking chart.** A data-viz scene plotting figures nobody measured, or a real figure with no
  date on it. The most likely fabrication in this medium, and the origin gate only catches it because
  the `onScreen` field exists.
- **The doubled screen.** On-screen text reading back the words being spoken.
- **The funnel scene.** A scene whose job is to sell the next thing. The downstream schema will
  actively invite this (see Delivery); the publication exists against it.
- **The clickbait thumbnail.** A picture promising a beat the video does not contain. Writing from
  nothing, on the one surface the gate cannot read.
- **The performed move that isn't.** Caps, italics, or a beat of silence written as though a voice
  will honour them. On the default path it will not.
- **The chopped essay.** Short form built by cutting a long piece into sixty-second slices, where clip
  three makes no sense without clip two. X's chopped-blog-post failure, in a medium where the viewer
  cannot scroll back.

---

## Gates, in order

Post-draft and advisory, in the machine's current order: **origin (claims tier) → do-not-promote +
coined-lines sweep → humanity scrub → critique / analyzer**. Expressive lane advises and never blocks.

**One thing runs differently here.** The origin check runs over **the narration and the `onScreen`
fields together**, as one text. That is the entire mechanism by which the law reaches the picture:

```bash
python3 .claude/skills/content-machine/gates/origin_check.py <script.md> <transcript.md> --lane expressive
```

For a **cut**, `coined_lines.py` takes the **source's** slug, not the video's:

```bash
python3 .claude/skills/content-machine/gates/coined_lines.py <script.md> \
    --lane expressive --artifact <source-piece-slug>
```

The first-screen test runs post-draft on the assembled script, against **both** first screens. A
failure returns as a reorder, never as new material.

---

## Delivery

A ship packet: the **scene table**, the ORIGIN LEDGER, the ASK LIST, the REPLY-HOOK MEMO, and — for
long form — a **thumbnail brief naming the beat it depicts**. The machine never renders, never
publishes, and never picks a voice.

The scene table is this contract's own, one row per scene:

| Field | What it is |
|---|---|
| `scene` | Number and a short name. |
| `narration` | The spoken words, verbatim. This is the writing. |
| `onScreen` | Any claim-bearing text or figure in this scene, verbatim. Usually empty. |
| `seconds` | Estimated duration. Replaced by the pipeline's measurement. |

**Translating that into `narrator_scripts.json` is a production step, not a writing step, and the
contract is deliberate about not adopting the pipeline's schema.** Its validator
(`scripts/validate-narrator.mjs`) requires a `narrativeIntent.type` per scene from a fixed enum:
`hook`, `pain_point`, `product_intro`, `feature_showcase`, `benefit_highlight`, `social_proof`,
`branding`, `cta`. That is a **sales funnel**, and six of the eight stages are an advertisement.
Writing to that schema would make every scene declare itself a stage of a sale before a word was
written.

**`product_intro`, `feature_showcase`, `benefit_highlight`, `social_proof` and `cta` are banned
values for this publication.** Named explicitly so that nobody fills a required field with `cta`
merely because a validator demanded one.

**The distinction is worth keeping, because it will recur.** The portfolio contract ruled that the
site's executable data contract **wins**, and it was right. This is the same situation with the
opposite answer: **an executable contract wins when it encodes the medium; it loses when it encodes
somebody else's business model.** Ask which one it is before adopting a schema.

---

## What this contract does not own

The art direction, style preset, motion, transitions, background music, or the voice engine
(`/faceless-explainer` and the hyperframes family); story order (`storytelling-architecture`);
whether the video is worth making (`substack-value-engine`); the sentences (`writing-voice-modes`);
or the decision to publish (Sean).
