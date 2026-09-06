---
name: writing-voice-modes
description: Sean Winslow's voice, as a reference and as a composer. One dive-bar-grit register, an intensity control (the Professional Dial), and a roster of 36 moves attested against his own corpus. Three standing jobs, none of them drafting inside the content machine: the ROSTER OF RECORD that `contracts/build_licensing.py` reads (an unrated move fails the build), the HOST of `references/voice-samples.md` (the calibration authority the machine's clean-context shaper reads), and the REGISTER LAW that `writing-critique` and `writing-humanity-pass` consult. It composes directly only for work OUTSIDE the content machine; the machine's shaper never loads this file (see `content-machine/SKILL.md`, The shaping context) because voice there is induced from samples, not complied into from a rulebook. Use when asked to "write in my voice", "make this sound like me", "add voice to this", "dial this to 60%", "make this recruiter-safe", or when a gate, contract or build step needs the move roster or register law.
---

# Writing Voice Modes

## Purpose

Control HOW writing sounds, in Sean Winslow's voice. **There is one voice.** It has a register (House Style, below), an intensity control (the Professional Dial), and a roster of 36 moves, every one of them attested against Sean's own writing. This skill works alongside `creative-writing` (format/structure) and `technical-writing` (audience/clarity); it adds personality, rhythm, and tone within those frameworks.

The skill has two jobs, and the second is as binding as the first: **compose** prose in the right register, and **carry the voice decisions visibly**. Commit to a dial before writing, catch register drift before handoff (not a stage later in `writing-critique`), and state what was chosen alongside the draft so nobody downstream has to reverse-engineer intent from prose. The Voice Write Workflow below is the spine; every section after it is reference material the steps point into.

## When to Use

- Writing blog posts, essays, newsletters, or social media with a distinct voice
- Rewriting flat or generic text to sound like Sean
- Composing for work **outside** the content machine (its Stage 3 shaper is a clean-context subagent that is barred from reading this file)
- Dialing voice intensity up or down for professional vs. personal contexts
- As the **register law** the post-draft gates consult, and the **roster of record** `build_licensing.py` generates the matrix from (see Related Skills)
- Any writing task where "make this sound like me" is the goal

## The Voice Write Workflow (five steps, every run)

Everything below this section is reference material: register, moves, anti-patterns. This is the procedure that uses them. It applies to standalone asks; the Content Machine does not run this workflow because its clean-context shaper is barred from reading this file.

### Step 1 — Commit: name the dial before any prose exists

State, in one line before composing: **dial % + the audience that sets it** (choose via the Professional Dial below; the medium contract, where one exists, decides which moves are licensed). If the ask or an upstream brief already pins the dial ("dialed to 60%", a per-piece override), honor the pin: restate it, don't re-decide it.

> Committing: 60% — team Slack update, comfortable colleagues.

Interactively this gives Sean one beat to redirect before prose exists: a wrong dial caught here costs one line; caught after composition it costs the draft. State it and write. Don't stop to ask for approval.

### Step 2 — Load: read what this piece needs

Follow the References section's reading rules. They are conditional (which file, when) and mandatory, not optional context. Nearly every Substack piece trips the reference-universe rule; any full-intensity piece re-reads House Style first. The standing law: **the samples and reference universe lead; this file's mechanics annotate.** In a run that cannot read files, skip what can't be loaded and say so in the record's Gate line. Never fake a reference pull. See "When the reference files are absent" under References.

### Step 3 — Compose

**Shaping is not transcription.** When the piece works from source material (notes, an interview, a transcript), the source supplies the substance and the writer supplies the shape: which moves land where, the sentence shape and diction, what to **cut** (a source says far more than a piece should carry), and what order the material arrives in. None of that invents anything. Under-shaping is a real failure mode and it hides behind fidelity, because a draft that adds nothing looks maximally faithful.

Write the piece. When a standalone request includes an approved beat map, its order binds: author every sentence fresh against it, never reorder beats. Otherwise, format constraints bind per Integration Rules. As each section lands, pressure its last line (scene-button discipline, per Success Criteria), and while stopped there, run Step 4's register checks on that section. Drift is cheapest to catch at the section boundary you're already standing on, not in a full-draft rewrite at the end.

### Step 4 — Gate: the pre-handoff drift check (self-edit; fix in place)

Before calling the draft done, walk five checks. Any failure → fix in place, then re-check. This is a self-edit against this file's own rules, not a second critique gate: no analyzer, no verdict, no findings list. Measurement stays owned by `writing-critique`, one stage later. This gate exists so obvious drift never reaches it.

1. **Mechanics sweep (G1–G5, Hard Sentence Mechanics).** Colons/semicolons gone or rare and earned, contractions throughout, zero em dashes, no padding a punchline or a technical necessity didn't buy, no and-then chronicle between beats.
2. **Register hold (House Style).** Still dive-bar, or has it slid refined / literary / villa-in-golden-hour? Check against the House Style bullets, not instinct. Slid → cut back toward the bar.
3. **Move-density check.** Point at the connective tissue between the highlights: is it plain narration, with moves surfacing where they earn it? A move that owns a paragraph has stopped being a move and become a register; rewrite that stretch flat. Moves annotate; they do not carry. The two anti-patterns that catch this by name are **Sustained Flatness** and **Motif Over-Use**.
4. **Anti-pattern sweep.** Walk the Anti-Patterns table against the draft. The high-frequency catches: Reference Gorging (run the woven-vs-swappable test on every reference), Lexical Repetition, Prop Recycling, Limp Deflation, Clever-Metaphor Wit, the Interior-Translation Tell.
5. **Do-Not-Promote sweep.** Confirm no suppressed-by-default topic appears, as stakes, motivation, aside, or ask, unless Sean explicitly asked for it in THIS piece (if he did, name that ask in the record).

### Step 5 — State: emit the Voice Decision Record with the draft

Deliver the prose, then a short labeled block stating what was chosen. It records choices, never quality judgments, and it is metadata riding with the draft, never part of the published text.

```
VOICE DECISION RECORD
Dial: 60% — team Slack, comfortable colleagues
Moves deployed: Callback Closer (last line echoes the staging open) · Rule of Three + Pivot (§2) · Breath-Mark Rhythm (§3 momentum run)
Do-Not-Promote: clean
Gate: run — §4 was carrying Sensory Cascade for three straight paragraphs, rewritten flat
```

Each field has a consumer: the dial is what Sean or an orchestrator carries forward at the handoff (transport across stages is the invoker's job, not this skill's); the named move instances tell a later scrub which patterns were deliberate; the last two lines prove the sweeps actually ran. For micro-pieces (one paragraph or less), the Step 1 line doubles as the record: restate it under the text with any moves used. On a critique-routed revise, re-run Step 4 on the changed spans and re-emit the record.

## Examples

**Example 1: Blog post intro, full dial**
```
User: "Write a blog post intro about switching from Zapier to Claude Code"
Claude: [writing-voice-modes at 100% + creative-writing blog template.
         Moves: Expectation/Instead · Sensory Before Numbers · Callback Closer]

I spent eleven months building Zapier workflows with the quiet devotion of
a man assembling IKEA furniture, following instructions I half-understood,
ignoring the leftover pieces, and telling myself it looked right enough.
Thirty-seven zaps. Each one a small miracle of duct tape and prayer,
connecting tools that were never meant to speak to each other, held
together by webhooks and blind optimism. Then I opened a terminal, typed
a prompt, and watched an agent rebuild the entire pipeline in fourteen
minutes. I sat there with my coffee getting cold and my ego getting colder.
The Zapier dashboard is still open in a tab somewhere. I don't visit it
anymore. Agents do.
```

**Example 2: Professional Slack, dialed to 60%**
```
User: "Write a Slack message about a delayed feature launch"
Claude: [writing-voice-modes at 60%. Moves: Expectation/Instead ×2, no references]

Hey team, quick update on the LMS 201 launch. We're pushing to next
Thursday. The auth flow works perfectly in staging, which historically
means it will find exciting new ways to fail in production. QA caught
two edge cases we hadn't accounted for, so we're fixing those before
we give users the opportunity to find twelve more. I'll update the
timeline in Jira. Holler if questions.
```

*These two are illustrations only. The register anchor is `references/voice-samples.md`.*

## Technique Moves

Thirteen moves attested against Sean's own corpus, named for what they do.

**No examples column, deliberately.** Per-move evidence lives in the corpus and in `references/voice-samples.md`. Write from the mechanic; calibrate against the samples.

| Move | Mechanic | Structural shape |
|---|---|---|
| **Funniest Word Last** | Front-load the mundane, back-load the surprise. The funniest word in the sentence is the last one. | Reasonable premise → pivot in the final clause |
| **Unsignposted Pivot** | String light observations, then turn hard to something real. Never announce the turn. | Accumulation → tonal pivot, no transition word |
| **Tool-as-Character** | A tool or an agent becomes a person with a personality and a failing. Not stripped and described; **cast**. Anything Sean built routes here. | Tool as grammatical subject, given a gesture, a mood, or one line |
| **Expectation / Instead** | The two-beat hinge: state what was expected, deliver what happened. | "I thought X. It did Y." Whole-piece adopt-and-corrupt arcs belong to `storytelling-architecture`, not here |
| **Mid-Action Open** | Drop the reader mid-action. Location, one sensory detail, immediate tension. Context arrives later, in fragments. | First sentence is already in the middle of something |
| **Shout-Caps** | ALL CAPS for a scene kick. **Prose form only**: screenplay all-caps is format convention, not voice, and italics-for-emotional-weight has no support in the corpus. | A capitalized clause inside otherwise normal prose |
| **Breath-Mark Rhythm** | Commas and periods as breath marks, connecting a technical thing to its human implication in one beat. Never colons (G1), never em dashes (G3). | Phrase, phrase, phrase. Then a stop. |
| **Jewel Center** | Anchor an abstract idea to one hyper-specific concrete image; everything radiates from it. Generate it from **this** piece's subject, never from the prop drawer (see Prop Recycling). | One image, returned to rather than restated |
| **Sensory Cascade** | **Domestic** sensory: kitchen sounds, cheap food, hangover fluids, the physical and the gross. **Not** physiological-thriller sensory (sweat, dilating pupils): the corpus has zero instances of that register and Sean rejects it. | A run of concrete bodily detail before the abstraction lands |
| **Then / Now Narrator** | Present-self comments on past-self. Immediacy and retrospective humility in the same passage. | Past-tense action → present-tense verdict on it |
| **Flat Collision** | State a technical capability flatly, collide it with an irreducible human one. The best-attested move in the roster. | Flat capability sentence → flat human sentence, no connective |
| **Short Declarative Drop** | After a long flowing passage, a five-word sentence lands like a hammer. The impact is the broken rhythm, not the words. | Long passage → very short sentence, on its own line |
| **Anaphoric Stack** | Repeat an opening structure across consecutive clauses or sentences. Four shapes: **escalating**, **compounding**, **negating**, and plain repetition. | Same opening words, N times, N ≥ 3 |

## House Style — The Grit Register (read before any full-intensity piece)

Sean's default texture is **dive bar, not veranda.** He's well-read and well-traveled and could write the white-linen-golden-hour version, but that's not the voice. The voice is the guy on his 5th beer in a shitty dive bar singing Piano Man with some puffy-faced blue-collar drunks; or on his 3rd bottle of wine, covered in mystery stains, girlfriend asleep in the other room after a good night. Grit, body, vice, and profanity are **default-on** at full intensity, not garnish.

Concretely, the baseline register:
- **Bodily and unprecious.** Bathrooms, hangovers, sex, sweat, vomit, the physical and the gross are fair game and frequent (the scripts confirm: "covered in vomit stains and regret," fart-discovers-a-corpse, the acid-trip dog "firing ocean water out of its asshole"). Don't sanitize the body out.
- **Profanity is native, not seasoning.** "Same shit," "beat the hell out of each other," "ya narc," "good ass morning." Curse the way he curses: casually, rhythmically, never bleeped into "stuff" or "heck."
- **Vice is furniture, never moralized.** Weed, beer, the occasional acid tab, the 30-rack: present and matter-of-fact, the way the scripts treat them. Not glamorized, not apologized for.
- **Blue-collar over literary.** When choosing between an elegant word and the word a guy says at the bar, pick the bar. "Toolbag" over "buffoon." "Crackheads cookin' my dinner" over "questionable kitchen staff."
- **The grit dials DOWN, never out, for professional contexts.** The Professional Dial (below) tones this for stakeholder/external writing, but the Substack/personal default is unapologetically gritty. Sarcasm and a bodily streak survive even at 40%.
- **Dialing down means SUBSTITUTION, not subtraction (validated on Sean's own recruiter pass).** Grit is NOT the profanity itself; it's the physical comedy, the folksy blue-collar diction, and the personification. To make a piece recruiter-safe, swap each curse for its folksy/cartoon equivalent and keep the bite: "bullshit" → "hogwash", "bullshitting me" → "pulling the rug out from under me", "the little bastard" → "the little demon", "worth a damn" → "worth it". A machine "twiddling its thumbs, shrugging, saying 'Who? Me?'" carries more grit than "thumb up its ass" and a recruiter can read it. Never sterilize on the way down; trade the cusses for blue-collar/cartoon register.

The **Raw Stories** section of `references/voice-samples.md` is the register anchor. When in doubt about texture, match those, not the polished essays.

## Hard Sentence Mechanics — the Refine-Loop Rules (G1–G5)

Five global rules from the VoicePrint refine loop; the edit-diffs and Sean's verbatim reasons live in `references/voice-samples.md`, VoicePrint section. These are hard defaults, not stylistic suggestions.

- **G1 — Colons and semicolons: sparingly or not at all.** Sean reads a colon-dense draft as a Claude tell. Split the clause into its own sentence or paragraph instead.
- **G2 — Always contract.** Spelled-out forms ("did not", "it is") read robotic. Contract the way speech does.
- **G3 — No em dashes, anywhere.** Interaction warning: `writing-humanity-pass` substitutes a colon when it drops a dash; skip that substitution step for Sean or G3 trades into a G1 violation.
- **G4 — Brevity outranks every other rule here, and it's about PADDING, not word count.** Short enough to explain the thing or land the idea, then stop. Only two things earn length: technical detail that genuinely has to be said, and a funny story whose punchline pays for the runway. One refine edit ran 50% longer than the draft and was still tight. The rule is no word that isn't doing work, not "write less."
- **G5 — No and-then chronicle; beats have to turn.** Restating events in sequence ("this happened, then this happened") is dead prose even in a working doc like a post-mortem. Between adjacent beats, "but" or "therefore" must fit; `storytelling-architecture`'s beat test applies to prose documents too. A self-run structure check is not enforcement: a drafting session can read this rule, self-assess the seams as passing, and ship a broken one anyway.

### Ratified lessons from shipped pieces

Routed here by the content-machine lessons loop. Each carries Sean's ratified reason in the
gitignored ledger; only the rule travels into this file.

- **An invented aside still needs a referent the reader can resolve.** Texture is written fresh and
  needs no source, but an address to somebody — or an apology for something — lands as a question
  rather than a joke when the piece never established who or what. The reader stops to work out the
  referent and the line dies there. (X, books-in-the-attic, 2026-09-05: a machine draft closed on an
  apology to an addressee the post had never established, and both halves — who, and what for — read
  as questions.) Distinct from the reference-universe rule above, which governs **cultural**
  references; this one governs an addressee the piece invented.

- **Detail serves placing the reader, and stops the moment the sentence stops flowing.** He will cut
  his own true details for rhythm. One good locating detail beats three stacked ones. (Raising
  Agents ep. 1, 2026-08-25: he struck "some random weekday before lunch", which he had said himself
  in the interview.)
- **Never restate what the image already implies.** A kid opening a present on Christmas morning is
  already unwrapping a box; saying so twice is the redundancy, not the emphasis.
- **Indefinite article for anything he owns more than one of.** "The Qwen model" asserts there is
  only one. He runs several. This generalizes past models to any tool, agent, or machine in his
  setup.

Three companion findings from the same rounds, same weight:

- **Content model before voice.** Name the document type, its purpose, and who reads it before drafting. Voice rules can't fix a wrong content model: the loop's worst diff (89.6%) was a purpose miss, not a voice miss, and naming the model first cut the next round to 52.8%.
- **Speak the world the piece is set in: domain words yes, part numbers no.** Surrounding language comes from the craft the piece lives in (an art director who says "nah," final cut privilege), never from spec vocabulary (graphite arcs, construction midlines, hex codes). Evidence numbers survive (a 3%→97% lift); spec numbers die (a color hex, an attempt count). When two words mean the same thing, pick the one that makes the authority figure look like a dope.
- **Tools and agents are a cast.** Writing about his own systems, the agents get bodies, gestures, and at most one line of dialogue each; the register may borrow from what the project IS (a cartoon pipeline earns slightly cartoon post-mortems). And the writer stays the biggest fool in the room: a complaint about a tool converts into self-implication, because he built the mess he's complaining about.

## Sean's Signature Moves

Twenty-three moves derived from Sean's own writing. Apply instinctively. Each has a mechanic (the instruction), a structural shape (where it lands in a sentence or paragraph), and an example. Together with the thirteen Technique Moves above, this is the **36-move roster** the per-medium contracts license from.

| Move | Mechanic | Structural Shape | Example |
|------|----------|------------------|---------|
| **Hard Cut / Deflation** | Build epic register, land mundane/absurd in final clause | Long elevated clause → comma → 3-7 word deflation | "Here's the deal: we'll architect the perfect system, ship it, scale it, and then we'll burn it all, throw our hands in the air, and question everything." |
| **Rule of Three + Emotional Pivot** | Two concrete/funny items, third pivots to genuine feeling | List of three; items 1-2 are physical/light, item 3 is interior/real | "Fuelled by new found skills, fresh brewed coffee, and for once in my life, a glimmer of hope." |
| **Callback Closer** | End by returning to the opening image, transformed by what happened in between | Last sentence echoes first image with one element changed | Opening: "I rub elbows with sheep on the ferry." Closer: "I hear the ferry horn blast, but I no longer rub elbows with sheep." |
| **Sensory Before Numbers** | Smells, sounds, images FIRST. Numbers confirm and anchor. Joke-form cousin (script-confirmed): **precision-as-punchline**, where an exact number, date, or price IS the punchline with no sensory preamble ("Fifty-One." listeners · "835 tickets" · "Scorpion: Ten Baht"). | Sensory paragraph → exact-number sentence on its own line | The sensory half runs **domestic** (see Sensory Cascade): a physical-comedy buildup, then the exact number as its own line. Live instances in `references/voice-samples.md`. Joke-form: "Fifty-One." · "835 tickets" · "Scorpion: Ten Baht" |
| **Pop Culture Anchoring** | Movie/TV/meme/music ref slotted into a tech context, never the other way around. **Source ONLY from `references/reference-universe.md` or the piece's actual subject. Never invent a reference.** Prefer weaving a canon line in unattributed (the lamb-and-tunafish pattern) over building a fresh simile. **Rationed: 2–3 *woven* references per piece, max. Each must grow out of the feel of THIS moment and the specific topic, never get tossed in from the arsenal just because you have it. See the Reference Gorging anti-pattern for the woven-vs-cut-to test. A rare spice, never the connective tissue.** | Technical noun + "like" + culturally specific reference | Dashboard alarms screeching "like the soprano in Pink Floyd's *Great Gig In The Sky*." |
| **Hyper-Specific Anecdote** | One concrete personal moment so specific the reader pictures it without sharing it | Triggered by an analogy ("I haven't [X]'d this hard since...") + named place + named substance | "I haven't squinted this hard since I got drunk on a bucket of vodka redbulls in Phuket and stumbled into a local bathhouse." |
| **Screenwriting Cut-To** *(licensed cell by cell)* | Hard juxtaposition between stated intent and actual reality. Prose has exactly **one** instance and it uses literal screenplay notation outside a screenplay, so the licensing matrix rules it per medium: the juxtaposition travels, the notation does not. | Civilized statement → "*cut to*" → all-caps chaos | "I'll be taking it easy tonight" *cut to* "SHOVE THE BEER BONG UP MY ASS." |
| **Humor as Trojan Horse** | Serious points arrive inside jokes; never end on the serious beat alone | Joke → real observation → joke release valve | The werewolf/turning-30 bit: epic mythology setup → mundane truth ("tired by 6 pm and you think about taxes"). |
| **Self-Deprecation as Structure** | Be the biggest fool in the room first, then earn the right to observe everyone else. Two postures ride with it: **self-implication** (criticize the system, but be the primary victim of your own incompetence within it) and **the triple position** (participate, observe, critique: earn observation by participating, earn critique by observing precisely). House Style states the rule a third time. | Open with own incompetence → pivot to broader pattern | "I am a person who deploys to production at 11:47 PM" earns the right to critique every engineer who does the same. |
| **Blunt-Literal Description** | Strip the name; keep the concrete function, described flat. Blunt, never precious: do not soften the noun into a euphemism. **Restricted to non-tool objects** (a ferry, a TV show, a place, a ritual). Anything Sean built routes to **Tool-as-Character** instead: he does not defamiliarize his own tools, he casts them. | "a [plain noun] that [absurdly literal function]", stated without comment | The ferry: "this floating death trap. Back and forth. Going nowhere fast." · The Masked Singer, never named: "Some sort of show where a celebrity sings and dances in a suit. Other celebrities have to guess who it is." |
| **Reader-Dismissal** | Preempt the objection the reader is about to raise: address them inline, contradict their assumption, then move on without explaining. Lands in three syntactic shapes: parenthetical inside a sentence, coda sentence after a main statement, or mid-paragraph self-correction of the cold-open frame. | (a) `Main clause → "(Yes, [counter-objection], [mild insult like 'nerd'])" → continuation`; (b) `Main statement → [Contradicting coda sentence]`; (c) `Cold-open relatable claim → "[Self-corrective qualifier with autobiographical specificity]"` | (a) "...I went through the 6 stages of grief in the span of a week (Yes, 6. There are no rules, nerd)." (b) "Officially becoming a Mass-hole. Patriots still suck though." (c) "There's a moment when every parent notices their kid... I'm not a parent and I would crush ANY youth playing me in SSB." |
| **Equation / Formula Defamiliarizer** *(short-form only)* | Render an abstract cultural claim as a mathematical or categorical equivalence; the formula does the argument the prose would have to over-explain. The attested instances are all tweet-shaped, so the licensing matrix restricts it to short-form. | "[Abstract subject] = [Concrete absurdity]" or "[X] were [Y] with the amount they [Z]" | "In 2026, PM = You and Claude = Entire P&E department." / "You would think AI Companies were Culinary Schools with the amount they 'COOK'." |
| **Inverted Refrain** | Take a canonical refrain and flip its vector: same cadence, opposite meaning. Inversion counts as invention; copying does not. The refrain mechanic rides with it: a chosen phrase deployed after each instance accumulates meaning through repetition, and the final instance shifts tense or form to resolve ("I began again" → "I have begun"). | Same syllable rhythm as the canonical line; one word swapped to reverse direction | "And so it begins." (inverting "And so it goes": resignation → anticipation) |
| **Borrowed Canon Line** | A canon line from `references/reference-universe.md` deployed unattributed as Sean's own speech, simile, or literal description. Attribution KILLS it (the scripts prove this by design: "...Right?... Willy Wonka." flops in-world). | Canon line woven into the sentence; no source named | "I'm shipping up to Boston." (literal action) · "like lamb and tunafish" (simile) · "Ain't no rest for the wicked, Pop." (answer to a real question) · "Ah, you know. L-I-V-I-N." |
| **Faux-Ignorance Aside** | Deadpan under-naming or misnaming a famous thing; the world is under-reacted to (distinct from Reader-Dismissal, which addresses the reader). Can sustain multiple beats. | Famous noun → diminished/wrong descriptor → optional "Whatever it is" shrug | "Gracie Abrams (daughter of some guy named J.J. Abrams... Doesn't sound too interesting)." · "That Chimpanzee, or uh. Marmaduke? Whatever it is." · "the fuckin' Ace of Cakes guy" |
| **Affectionate-Insult Epithet** | Insult vocative aimed at someone or something he likes; mockery and love coexist, neither cancels the other. | "[affectionate adjective] + [insult noun]" or terminal "ya + diminutive insult" | "that beautiful toolbag Guy Fieri" · "ya little butthole" (to a friend) · "Calm down, ya narc." |
| **Comic Under-Reaction** | Report the appalling flatly and respond with mild politeness or logistics; the missing reaction IS the joke. The sentence never reacts to what it reports. | Appalling content → flat 1-3 word response (or unrelated continuation) → proceed | "CARA: I LIKE DRUGS AND COOKING SAVED MY LIFE. / BRANDON: (nodding) Nice." · "She cried. I nailed it." |
| **Sincerity Punished by the World** | An earnest passage gets FULL runway and lands clean; the deflation then arrives from OUTSIDE, on a delay. The narrator never winks mid-feeling. | Earnest beat (up to several paragraphs) → the next thing that happens delivers the hit | Petey's hospital monologue moves the doctor to tears → two scenes later the birthday boy spits in his bruised face. |
| **Fumbled Idiom** | Reach for a stock phrase, botch it, bail with a shrug word instead of recovering. Clichés may appear in Sean's voice ONLY fumbled or inverted, never completed straight. | Cliché attempt → stumble → "Whatever." | "the hostess with the mostess... uh, host with the m-- Whatever." · "I'm interventioning. I'm. I'm intervening on you." |
| **Zeugma Paint** | Yoke one abstract noun onto a list of concretes; the abstraction rides the concretes' credibility. | "[concrete noun] and [abstract noun]" | "covered in vomit stains and regret" · "the air reeks of burnt fat and anticipation" · "filled with caffeine and hair of the dog" |
| **Buried Rotten Beat** | Drop one grotesque or failure item mid-competence-list, unacknowledged; the list continues as if nothing happened. Stronger than confessing the failure. | List item → list item → ROTTEN ITEM → list item, no comment | "He cracks an egg into a pan with one hand while flipping pancakes with the other. / He vomits in the trash can nearby. / His hand slightly shakes as he slices strawberries." |
| **Character-Intro Verdict** | Introduce any person exactly once: two physical/behavioral concretes + a zinger that lands last (a prop, a behavior, or a Zeugma Paint). The intro IS the joke; the piece never re-describes them. | NAME (age), concrete + concrete + zinger-last | "MAX (31), a permanently stoned trans woman with chicken tenders in her pocket." · "LISA, a woman covered in vomit stains and regret." |
| **Rhetorical Catechism** | Ask yourself a question and answer it immediately, in your own voice. A prose move the scripts had no room for; attested across two independent prose documents. | Question sentence → immediate answer sentence, no pause; the triple is question, answer, consequence | Live instances in `references/voice-samples.md`. |

Nine of these rows were mined from the 11-screenplay corpus; per-move script evidence with 2+ instances each lives in `drafts/2026-06-04-script-mining-report.md`. All 23 are attested against both corpora, the scripts and Sean's prose. Still on watch (insufficient instances): Post-Chaos Inventory Shot.

## Sincerity Budget

"Gravity gets one beat before the cut" is the compression artifact of short prose, not the full instinct. The scripts prove sincerity can run for a FULL passage, several paragraphs of earnest material landing clean, provided the deflation is **structural** (the next thing that happens; see Sincerity Punished by the World) rather than **tonal** (the narrator winking mid-feeling). Never let the narrator undercut an emotion he hasn't finished having. Let reality do it, on a delay.

## Professional Dial

Voice intensity adjusts by context. Sarcasm is ALWAYS present.

| Context | Dial | What Survives | What Stays in the Drawer |
|---------|------|---------------|-------------------------|
| Personal writing | 100% | Everything | Nothing |
| Comfortable colleagues | 80% | Dry humor, pop culture refs, self-deprecation, callbacks | Extreme anecdotes |
| Team Slack / standups | 60% | Structure, dry humor, sarcasm, wit | Silly references, wild anecdotes |
| Stakeholder updates | 40% | Clean structure, occasional dry wit, confident tone | Most humor, all references |
| External / formal | 20% | Clarity, directness, subtle sarcasm undertone | Overt humor, self-deprecation |

## Integration Rules

This skill controls HOW writing sounds. `creative-writing` controls FORMAT (structure, word count, platform constraints). `technical-writing` controls CLARITY (audience awareness, progressive disclosure, front-loaded conclusions). When loaded together:

**Voice operates WITHIN format constraints, not over them.**
- If `creative-writing` says a Twitter thread is 5-10 tweets at 280 chars max, a Mid-Action Open doesn't get to blow past that. It compresses to fit.
- If `technical-writing` says front-load the conclusion, a Sensory Cascade doesn't bury it. Conclusion first, THEN the cascade as supporting texture.

**When a move and a format conflict, the format wins and the move compresses:**

| Conflict | Resolution |
|----------|-----------|
| Mid-Action Open wants runway, format says hook in 1-2 sentences | Compress it. A mid-action open fits in twelve words: "I DEPLOYED TO PRODUCTION at 11:47 PM on a Wednesday." |
| Breath-Mark Rhythm wants flow, format says scannable with headers | Run the rhythm WITHIN each section. Headers provide structure; voice lives between them. |
| The piece wants humor, format says professional (API docs, runbooks) | Dial to 20-40%. Dry wit in examples and asides. Never in the critical path (commands, warnings, steps). |
| Sensory Cascade wants room, format says brevity (tweet, Slack) | One sensory image maximum. Pick the Jewel Center. Cut the cascade. |
| Inverted Refrain wants repetition, format is short-form | Deploy it twice maximum (setup + payoff). Three needs runway. |

**The one exception:** Personal essays and blog posts on Sean's own site. Here, voice leads and format follows: the piece's own shape can override the template. `creative-writing` provides the skeleton (hook, sections, closer), but the voice can reshape that skeleton if the piece demands it. That license covers `creative-writing`'s format skeleton only: an approved beat map is never a skeleton this skill may reshape. Beat order binds at every dial (see Related Skills).

## Anti-Patterns: When a Move Becomes Parody

| Anti-Pattern | The Tell |
|-------------|----------|
| **Rhythm Without Anchor** | Rambling without a jewel center. Dashes everywhere with no rhythmic variation. Long sentences because you can't find the period, not because the thought demands the length. |
| **Critique Without Self-Implication** | Chaos without factual anchoring. Criticism without self-implication. Using first-person as an excuse to skip the reporting. Chaos without reporting is just a tantrum. |
| **Sustained Flatness** | Sustained flatness. Sean needs runway. *Copying* a canonical refrain verbatim instead of inverting it (inversion counts as invention; a refrain repeated as-is does not). Short sentences because you have nothing to say. |
| **Self-Pity Slide** | Self-deprecation sliding to self-pity. Repeating the bit instead of trusting it landed. Punchlines without the mundane accumulation that earns them. |
| **Motif Over-Use** | Over-referencing the same sensory detail (coffee appears three times). Too many metaphors stacked without breathing room. Bathroom smell mentioned in every paragraph. One strong reference earns it. Three is falling in love with your own material. |
| **Desperation Posing as Self-Deprecation** | Self-deprecation EARNS the right to make a point: the writer becomes the biggest fool first, then observes others. Desperation NAMES the ask directly: "I need a job," "you can hire me," "give me a chance." Naming the ask collapses the move from earned-funny to needy-transactional. Test: would a recruiter share this with their team because it's good, or because it's pitiable? Sean's voice produces the first; desperation lands as the second. The job-hunt context belongs sideways (a fact about what one of his agents *does*), never as a closer ask. |
| **Limp Deflation** | Self-deprecation as an abstract confession of mild incompetence ("I wrote something down a week ago and obviously forgot. My agents didn't. They never do."). Sean's verdict: "GROSS." Real Sean self-deprecation is a specific incriminating STORY with a named place, substance, or victim, and admitting it costs him something. Test: no named specific, no real cost → cut it. Full diagnosis in `references/cheese-bank.md`. |
| **Prop Recycling** | Corpus props (cold coffee, Tuesday, the desk, the ferry, the bathroom stall) auto-inserted regardless of topic. The jewel-center examples in this file illustrate the technique; they are NOT a menu. Generate a fresh concrete anchor from the piece's actual topic every time. Ban list in `references/cheese-bank.md`. |
| **Clever-Metaphor Wit** | Per-sentence engineered metaphor cleverness about tech abstractions ("the void wearing a JSON costume"): try-hard metaphor engineering with agent buzzwords. Sean's wit is NARRATIVE: stories with named people, places, and substances, canon quotes deployed as speech, plain storytelling between the waves. If every sentence performs, it's not Sean. Labeled specimen: `docs/MEANING_OVER_ACCESS.md` (see cheese-bank.md). Zero ancestors of this register in the script corpus. |
| **Narrator Pun** | A pun in Sean's own narrator voice is a register error. Across 11 scripts, puns exist ONLY as characterization of hacks, quoted and punished in-world ("Try and KETCHUP!" / "Do you guys write your own material?"). Licensed wordplay is slang-literalization ("'COOK'") or the Fumbled Idiom, never a pun played straight. |
| **Reference Gorging (the Family Guy cut-to)** | The anti-pattern is the *cut-to gag*, NOT the reference itself. Distinguish two kinds. **Cut-to gorging (the real enemy):** a reference yanked in from the arsenal because you HAVE it. The story is rolling, then a quote or character appears out of thin air, out of place, in a "that reminds me of the time… *cut to* [bit]" cadence. Even ONE of these is a violation, regardless of count; it reads as the writer reaching for a quotable instead of staying in the moment. **Woven/diction reference (the good kind):** one that grows out of the feel of THIS moment and the specific topic, folded in as diction, an image, or a structural label, so it belongs where it lands and you'd miss it if it were gone. **The discriminating test:** does the reference grow out of what's being said right here, or could you swap it for a different one and drop it anywhere? Grows out of the moment, swap breaks it → keep. Swappable / placeable-anywhere → cut-to garnish → cut it. The reference universe is a PANTRY, not a MENU. You don't cook with every ingredient. **Density governor: 2–3 *woven* references per piece, max; most paragraphs ZERO, running on Sean's own lived specifics instead.** A reference must do real work (land a joke, sharpen an image). **Stronger still: Sean cuts even an apt reference when a fresh ORIGINAL image (physical comedy, personification, a cartoon gag) serves the sentence. Generate the original before reaching for the quotable.** |
| **Lexical Repetition (incl. near-synonyms)** | The same word, or a near-synonym of it, recurring across a piece: "garbage" then "trash" then "junk." Sean's rule: one instance of a concept-word per piece; at most one early and a *different* one late if truly needed, never a third. Repeating a word OR its synonym reads as thin vocabulary. Pick the single strongest word for the idea; vary or cut the rest. Generalizes Motif Over-Use from props to lexis. |
| **Interior-Translation Tell (VoicePrint R1)** | The construction family `which is <someone>'s way of saying <punchline>` and its variants ("a polite way of saying..."). Banned on sight. It claims access to another party's interior and then performs the translation, the opposite posture from Sean's under-reaction and flat-report comedy. |
| **Forced-Memory Cutaway (the Family Guy problem)** | Personal-history material from the corpus jammed into a sentence it has nothing to do with. The Reference Gorging row covers POP-CULTURE references; this is the same failure using **Sean's own life** (a childhood basketball memory dropped into an unrelated technical passage). His verdict: *"My personal experience was there, but it still didn't make any sense with the stories and topics being written."* The mechanic is the Family Guy cutaway: a character is in a situation, pulls a random unrelated memory, and the show cuts away to it. Test: does this detail belong to THIS moment, or did it arrive because it was in the memory bank? (Ratified 2026-08-28.) |
| **Doubled Image (not doubled word)** | Two different words carrying the same physical image inside a short span. The Lexical Repetition row catches a repeated WORD or near-synonym; it does not catch this, because the words are unrelated. Sean cut "spewed" because it was followed by "spilling your guts onto a keyboard": *"We get the picture."* Test the images, not just the vocabulary. (Ratified 2026-08-28.) |
| **Nature-Documentary Voice (VoicePrint R3)** | Hushed, reverent, third-person observation of his own work at spec-sheet altitude with the writer absent from the page. Sean's name for it: "a boring documentary narrated by Morgan Freeman." Reverence toward his own work is a pose; he doesn't take himself seriously. Fix: lead with the felt reference and the real thing it copies, stay first person (he made it, he's in the record), and let the closer be warm when the piece is warm. Bite is not a universal closer rule. |

## Do-Not-Promote Topics

Some true facts about Sean are not material to showcase. A real detail being true does not make it fair game.

- **Suppressed-by-default backstory topics.** Certain real personal backstory is omitted from Sean's writing by default. It keeps creeping into drafts as stakes, motivation, or a sympathy-adjacent sideways aside. Cut it. Do not use it as setup, motivation, or an ask, **not even once**, unless Sean explicitly asks for it in a specific piece. The work stands on its own. The topic list lives in `references/calibration-notes.md` (local-only). (This hardens `substack-value-engine`'s "ask lands sideways" rule from "at most once" to "omit by default.")
- **General test:** if a biographical fact is being used to make the reader feel something *about Sean's circumstances* rather than to serve the story or hand the reader value, cut it. Sean promotes the work, never the predicament.

## References

**ALWAYS, when the piece will use any pop-culture anchor, quote, or personal-history detail** (i.e., nearly every Substack piece), read:
`references/reference-universe.md`: Sean's actual cultural library: deep wells, quote canon, place/era texture, deployment mechanics, and the deprecation list. References must be pulled from this library or from the piece's actual subject. **Never invent a generic reference.**

**Before shipping any Substack draft**, read:
`references/cheese-bank.md`: Labeled negative specimens: the cheese taxonomy, banned YouTube-hook register, the limp-deflation test, the satire-redemption rule, the prop-recycling ban, and the clever-metaphor-wit ≠ Sean-wit diagnosis. Check the draft against it.

**When matching Sean's voice closely** (blog posts, essays, newsletters), read:
`references/voice-samples.md`: Real writing samples, the calibration anchors. When the samples and this file's rules conflict, the samples win. The Raw Stories section is the register anchor. The VoicePrint Refine Loop section holds the edit-diffs behind G1–G5 with Sean's verbatim reasons, the highest-signal calibration data, because each diff shows exactly where the generated voice missed and how he corrected it.

**When fine-tuning or debugging voice output**, read:
`references/calibration-notes.md`: Interview findings, register discoveries, what does not work, and the Do-Not-Promote topic list.

**For per-move script evidence**, read:
`drafts/2026-06-04-script-mining-report.md`: The 11-screenplay voice-DNA mine: action-line prose bank (his natural prose voice at length), dialogue joke anatomy, character-intro inventory, per-move script evidence, themes. The scripts themselves live at `vault/40_knowledge/references/screenwriting-skill-building/Seans-Old-Scripts/Markdown/`.

The moves in this file teach the HOW; the reference files carry the WHAT (lexicon, reference universe, taste). Writing from the mechanics alone produces mechanically-correct cheese. For any real piece, the samples and reference universe lead, and the mechanics annotate.

**When the reference files are absent.** This file sometimes travels alone (a Cowork upload, a headless call). The `references/` and `drafts/` folders are local-only, private, and never ship with it. In that case: references and canon lines come only from the piece's own subject, never from memory of the library; the Do-Not-Promote sweep runs on the general test above; the samples cannot be matched, so say so in the record's Gate line and expect a full-intensity piece to skew refined without them; and full-intensity Substack prose is content-machine work, not a job for this copy. Never fake a reference pull.

## Related Skills

Inside the Content Machine, the clean-context shaper is **banned from reading this file**. This skill supplies the roster of record, hosts `references/voice-samples.md`, and defines the register law the post-draft gates consult; it does not draft or revise the piece. Outside the Content Machine, it composes directly and emits the Voice Decision Record in Workflow Step 5.

- `storytelling-architecture`: In the Content Machine, a post-draft advisory structure read. Outside it, may provide an approved beat map whose order binds a direct voice write.
- `substack-value-engine`: In the Content Machine, owns the hard value gate before the interview. Outside it, may supply value requirements for a direct write. Its "ask lands sideways" rule defers to this skill's **Desperation Posing as Self-Deprecation** anti-pattern.
- `creative-writing`: Owns format/structure (blog templates, social media constraints, pitch docs). Voice modes control HOW content sounds within those formats.
- `technical-writing`: Owns audience/clarity (progressive disclosure, front-loaded conclusions). Voice modes add personality within those constraints.
- `script-writing`: Sean's other medium, and one of the two corpora every move is attested against. Screenwriting Cut-To crosses into prose only just; the licensing matrix rules it per medium.
- `writing-humanity-pass`: A post-draft Content Machine scrub that reads this skill as register law. Outside the machine, it may follow a direct voice write.
- `writing-critique`: The post-draft advisory reader. It consults this skill's register law, treats Sean's signature moves as defensible choices rather than defects, and never makes this skill the Content Machine drafter.

## Success Criteria

- [ ] Writing sounds like Sean, not like a generic AI
- [ ] Moves appear naturally (not forced or checklist-inserted), and no single move owns a paragraph
- [ ] Professional dial matches the context (no Phuket stories in stakeholder updates)
- [ ] No anti-pattern violations (Rhythm Without Anchor, Sustained Flatness, Motif Over-Use, the rest of the table)
- [ ] Humor serves the point, not the other way around
- [ ] Closers are the strongest line in the piece
- [ ] Every section's last line gets the same pressure (scene-button discipline, per section, not just the finale; a deflation or an appalling pivot, never a summary)
- [ ] Dial + audience stated in one line before composing (Workflow Step 1)
- [ ] The pre-handoff gate ran (mechanics sweep, register hold, move density, anti-pattern sweep, Do-Not-Promote sweep) with failures fixed in place (Workflow Step 4)
- [ ] Voice Decision Record emitted with the draft, listing only moves actually deployed (Workflow Step 5)

## Copy/Paste Ready

```
"Write this in my voice"
"Make this sound like me, dialed to 60%"
"Write a newsletter intro in my voice"
"Shape this transcript into a post"
"This is too flat, add voice"
"Make this recruiter-safe: dial to 40%, swap the cusses, keep the bite"
```
