# Screenplay Craft Research Pipeline — Script-Writing Skill Upgrade

## Overview

**Goal:** Research 6 filmmakers/teams' screenplay craft mechanics → synthesize into a Screenplay Mechanics doc → calibrate to Sean's personal screenwriting voice → upgrade the `script-writing` skill with craft depth.

**Filmmakers/Teams:** Charlie Kaufman, Taika Waititi, Hayao Miyazaki, Pixar Story Team, Bo Burnham, Tina Fey / Donald Glover

**Tools:** Perplexity Deep Research (broad technique analysis) → NotebookLM (source synthesis with custom analyst roles) → Claude Code (interview + skill upgrade)

**Quality Bar:** The writing-voice-modes pipeline. Every deliverable here matches or exceeds its voice-modes equivalent.

---

# DELIVERABLE 1: Perplexity Deep Research Prompts

## Design Choices

Each prompt follows the voice-modes template: context framing ("I'm building a screenwriting craft system"), dimensional breakdown, transferability filter, and the "MECHANICS not vibes" calibration line. The key adaptation: every prompt now targets **screenplay-specific** dimensions — dialogue mechanics, scene construction, structural patterns, animation/visual storytelling relevance, and compression into 3-5 minute shorts.

The prompts are longer than the voice-modes prompts because screenplay craft has more dimensions than prose craft (dialogue + visual + structure + pacing vs. mainly sentence + structure + voice). Each prompt earns its length.

---

### Prompt 1: Charlie Kaufman — Screenplay Craft Analysis

```
I'm building a screenwriting craft system that extracts transferable
screenplay techniques from master filmmakers and applies them to writing
2D animated comedy shorts (3-5 minutes) with emotional depth.

Analyze Charlie Kaufman's SCREENPLAY CRAFT with extreme specificity.
I need ACTIONABLE TECHNIQUE PATTERNS, not biography or filmography
summaries.

Cover these dimensions:

1. DIALOGUE MECHANICS
   - How does Kaufman construct dialogue that sounds natural but is
     structurally precise? What's his sentence construction pattern?
   - How does he build subtext — what are characters NOT saying, and
     how does the audience know?
   - How do characters sound distinct from each other? What gives
     each character a unique verbal fingerprint?
   - His use of repetition in dialogue — when characters repeat
     themselves, loop back, or say the same thing differently.
     When is this technique vs. flaw?
   - Specific examples from Being John Malkovich, Adaptation,
     Eternal Sunshine, Anomalisa, and I'm Thinking of Ending Things

2. SCENE CONSTRUCTION
   - How does Kaufman open scenes? What's in the first 30 seconds?
   - How does he build tension within a single scene — what's his
     escalation mechanic?
   - How does he execute tonal pivots — the moment a funny scene
     becomes devastating (or vice versa)? What's the structural
     mechanism?
   - His "reveal" technique: how a scene recontextualizes everything
     before it. How is the audience set up to miss the turn?
   - How does he close scenes? Does he button them or leave them
     open? When does he use each approach?

3. STRUCTURAL PATTERNS
   - His non-linear and meta-narrative techniques: how does he
     break conventional act structure and WHY does it work instead
     of just being confusing?
   - The self-referential loop: how Adaptation writes about the
     process of writing Adaptation. What's the structural principle
     that makes meta-narrative functional rather than masturbatory?
   - How does he handle tonal shifts across a full screenplay —
     comedy to drama to existential dread? What are the transition
     mechanics between tones?
   - His approach to endings: Kaufman resists resolution. How does
     he end a screenplay satisfyingly without tying things up?
   - Pacing signatures: where does he linger vs. cut fast? What
     determines the rhythm?

4. ANIMATION / VISUAL STORYTELLING RELEVANCE
   - Anomalisa is a stop-motion film about sameness and connection.
     How does Kaufman use the animation medium to enhance thematic
     content? What screenplay choices only work BECAUSE it's animated?
   - His visual metaphors: the portal in BJM, the erasing in Eternal
     Sunshine, the puppet theater in Anomalisa. How are these set up
     in the screenplay (not just the direction)?
   - Which Kaufman techniques translate specifically to 2D animated
     comedy shorts? Which ones require feature-length runway?

5. TRANSFERABLE TECHNIQUES FOR SHORT-FORM
   - Kaufman's screenplays run 120-150 pages. What survives
     compression to 3-5 pages (3-5 minute shorts)?
   - The "humor as trojan horse" pattern: Kaufman makes you laugh,
     then punches you in the gut. How does this work mechanically
     in a single scene (not across a whole film)?
   - His approach to absurdism that feels emotionally true — what
     keeps it grounded? What's the anchor?
   - How does he develop character in the first 60 seconds of a
     screenplay? What's the minimum viable character establishment?

6. PROCESS
   - How does Kaufman develop ideas? What's known about his writing
     process, rewriting approach, and how he builds from concept
     to draft?
   - His thoughts on screenwriting craft from interviews, lectures
     (especially his BAFTA lecture), and commentary tracks
   - How does he handle the tension between commercial expectations
     and personal vision?

Include specific scene examples with page/time references where
possible. I need MECHANICS, not vibes. "Kaufman is surreal" is
useless. "Kaufman opens scenes with one character performing a
mundane action while another character's dialogue reveals that
the mundane action IS the emotional crisis — as in the
opening of Anomalisa where Michael Stone's small talk on the
plane structurally mirrors his existential numbness" is useful.
```

---

### Prompt 2: Taika Waititi — Screenplay Craft Analysis

**Design choice:** Waititi's signature is the invisible seam between comedy and drama. The prompt targets HOW he constructs that seam — the mechanics of tonal control, not just "he balances humor and heart."

```
I'm building a screenwriting craft system that extracts transferable
screenplay techniques from master filmmakers and applies them to writing
2D animated comedy shorts (3-5 minutes) with emotional depth.

Analyze Taika Waititi's SCREENPLAY CRAFT with extreme specificity.
I need ACTIONABLE TECHNIQUE PATTERNS, not biography or filmography
summaries.

Cover these dimensions:

1. DIALOGUE MECHANICS
   - Waititi's dialogue sounds improvised but is scripted. What's the
     construction technique that creates that naturalistic, slightly
     awkward, mid-thought quality?
   - His deadpan delivery setup: how does the SCRIPT create deadpan?
     What's in the dialogue vs. what's in the parenthetical vs.
     what's left to performance?
   - How do his characters interrupt each other, trail off, change
     subjects mid-sentence? What's the structural pattern for
     "realistic" dialogue that's actually carefully written?
   - Humor in dialogue: when does the joke live in WHAT a character
     says vs. HOW they say it vs. the CONTRAST between dialogue and
     action? Specific examples from What We Do in the Shadows,
     Hunt for the Wilderpeople, Jojo Rabbit, and Boy
   - How does he differentiate character voices — especially ensemble
     casts where every character is funny but in different ways?

2. SCENE CONSTRUCTION
   - The comedy-drama seam: how does Waititi construct scenes that
     are simultaneously funny AND emotionally resonant? Not scenes
     that alternate between comedy and drama — scenes where both
     coexist in the same moment. What's the mechanical structure?
   - How does he open scenes? Is there a cold-open pattern?
   - His use of awkward silence and pause as a scene element.
     How is this scripted (not just directed)?
   - Physical comedy in the screenplay: how does he write sight
     gags, physical bits, and visual jokes in the action lines?
   - Scene length and rhythm: how long are his scenes typically?
     When does he cut short vs. let a scene breathe?

3. STRUCTURAL PATTERNS
   - How does Waititi structure emotional arcs within comedy
     frameworks? The Boy and Jojo Rabbit structures — how does
     he build toward devastating emotional moments while maintaining
     a comic surface?
   - His pacing signatures: where does he accelerate vs. slow down?
     What triggers a pace change?
   - How does he handle the "turn" — the moment a comedy becomes
     something more? (The Hitler scene in Jojo Rabbit, the birthday
     scene in Boy, the ending of Shadows) What's the setup-to-turn
     ratio?
   - Ensemble management: how does he juggle multiple characters
     without losing momentum? What's the structural approach?

4. ANIMATION / VISUAL STORYTELLING RELEVANCE
   - Waititi's comedy is highly physical and visual even in live
     action. Which of his techniques translate DIRECTLY to 2D
     animation? (Comedy timing, visual gags, reaction shots)
   - His use of contrast between visual tone and emotional content
     (Jojo Rabbit's bright colors during dark subject matter).
     How would this translate to animation visual design choices
     written into the screenplay?
   - Deadpan character reactions as an animation tool: how would
     his "straight face in absurd situation" translate to character
     expression sheets?

5. TRANSFERABLE TECHNIQUES FOR SHORT-FORM
   - Waititi's short films (Two Cars One Night, Tama Tū) exist.
     Analyze their craft specifically — how does he compress his
     technique into short form? What survives and what doesn't?
   - How does the comedy-drama balance work in 3-5 minutes? Does
     it need a different ratio than a feature?
   - His mockumentary technique (Shadows, Our Flag Means Death) —
     can the confessional/interview structure compress into short
     animated format?
   - Improvisation-feeling dialogue in shorts: how much scripted
     "improv" can you fit in 3 minutes before it feels aimless?

6. PROCESS
   - How does Waititi write? His known process for developing
     scripts, including his collaborative and improvisational
     approach
   - How does he direct actors to achieve that naturalistic feel —
     and how much of that is ON THE PAGE vs. discovered on set?
   - His background in comedy (stand-up, sketch) — how does that
     training manifest in screenplay structure?
   - His approach to cultural specificity (Māori culture in Boy and
     Wilderpeople) that somehow creates universality. How is this
     achieved in the writing, not just the setting?

Include specific scene examples with time references where possible.
I need MECHANICS, not vibes. "Waititi balances humor and heart" is
useless. "In Jojo Rabbit, Waititi scripts Jojo's discovery of his
mother's shoes by placing it immediately after a comedic beat with
Yorki, so the audience's defenses are fully lowered by laughter
when the devastation arrives — the structural principle is NEVER
signal the tonal shift, always execute it mid-laugh" is useful.
```

---

### Prompt 3: Hayao Miyazaki — Screenplay Craft Analysis

**Design choice:** Miyazaki is studied for VISUAL STORYTELLING that works in the screenplay, not just on screen. This prompt explicitly targets techniques that feed both `script-writing` AND `animation-pipeline` skills. The animation relevance dimension is expanded because Miyazaki IS animation.

```
I'm building a screenwriting craft system that extracts transferable
screenplay techniques from master filmmakers and applies them to writing
2D animated comedy shorts (3-5 minutes) with emotional depth.

Analyze Hayao Miyazaki's SCREENPLAY AND VISUAL STORYTELLING CRAFT
with extreme specificity. I need ACTIONABLE TECHNIQUE PATTERNS, not
biography or filmography summaries.

NOTE: This research feeds TWO skills — script-writing (dialogue, scene
construction, structure) AND animation-pipeline (visual storytelling,
pacing, environment design). Cover both dimensions.

Cover these dimensions:

1. DIALOGUE MECHANICS
   - Miyazaki writes far less dialogue than Western screenwriters.
     When dialogue DOES appear, what makes it work? What's the
     construction principle?
   - How do his characters reveal themselves through speech patterns?
     Chihiro vs. Haku vs. Yubaba in Spirited Away — what's in the
     dialogue that distinguishes them beyond content?
   - His use of silence and non-verbal communication as scripted
     beats (not just directorial choices). When does a character
     NOT speak, and how is that written?
   - Dialogue as emotional punctuation: Miyazaki characters often
     speak only at emotional peaks or transitions. What's the
     pattern for when dialogue appears vs. when visual storytelling
     carries the scene?

2. SCENE CONSTRUCTION
   - The "quiet moment" technique: Miyazaki's famous "ma" (間) —
     scenes where nothing dramatic happens but the audience feels
     something. How is this constructed in the screenplay?
     Specific examples from Totoro, Spirited Away, Kiki's Delivery
     Service, The Wind Rises
   - How does Miyazaki open scenes? What establishes the emotional
     register before any conflict begins?
   - His action sequences: how does he write flight sequences,
     chase scenes, and physical action in ways that maintain
     emotional stakes (not just spectacle)?
   - How does he build tension WITHOUT dialogue? What's the
     mechanical structure of a Miyazaki suspense scene?
   - Scene transitions: how does he move between emotional registers
     (wonder → danger → calm → melancholy)? What are the transition
     mechanics?

3. STRUCTURAL PATTERNS
   - Miyazaki's films often resist three-act structure. What IS his
     structural model? How does he organize narrative without
     traditional act breaks?
   - His approach to antagonists: Miyazaki villains are rarely pure
     evil (No-Face, Lady Eboshi, Howl). How does he construct
     morally complex antagonists in the screenplay?
   - Pacing signatures: Miyazaki films breathe. They have dead space
     that other filmmakers would cut. How does this pacing work
     STRUCTURALLY — what function does the slow moment serve in the
     larger rhythm?
   - His thematic embedding: environmentalism, pacifism, growing up.
     How does he embed theme without stating it? What's the
     structural technique?
   - The Miyazaki ending: his films often end ambiguously or with
     bittersweet acceptance rather than triumph. How does he
     construct satisfying endings without conventional resolution?

4. VISUAL STORYTELLING AS SCREENPLAY CRAFT
   THIS IS THE CORE SECTION FOR MIYAZAKI.
   - Environment as narrative: how does Miyazaki's screenplay
     describe settings in ways that make them characters? The
     bathhouse in Spirited Away, the forest in Princess Mononoke,
     the city in Kiki's. What's in the action lines?
   - Weather and atmosphere as emotional language: rain, wind,
     clouds, light. How does he use environmental conditions to
     express character emotion without dialogue?
   - Character movement and body language: Miyazaki scripts
     specific physical actions that reveal character (how Chihiro
     puts on her shoes, how Sophie moves when young vs. old).
     How detailed are these in the screenplay vs. left to animators?
   - Scale and perspective: Miyazaki constantly shifts between
     intimate close-ups and vast landscapes. How does the screenplay
     control this? When does he call for scale shifts and why?
   - Food and domestic rituals: Miyazaki's famous food scenes and
     daily-life sequences. How are these scripted? What purpose do
     they serve in the narrative structure?

5. TRANSFERABLE TECHNIQUES FOR 2D ANIMATED SHORTS
   - Which Miyazaki techniques work at 3-5 minutes? His pacing
     assumes feature length — what survives compression?
   - The "quiet moment" in a short: can you earn a pause in a
     3-minute film? How would you set it up?
   - Visual storytelling without dialogue for comedy shorts: how
     does wordless emotional storytelling translate when your
     primary genre is comedy?
   - His "show the world first, then the conflict" approach:
     how much world-building can a 3-minute short support?
   - Animation-specific techniques: his approach to movement timing,
     character acting, and visual rhythm that can be scripted
     (written into action lines) not just animated

6. PROCESS
   - Miyazaki's storyboard-first approach: he reportedly draws the
     film before writing it. How does this reverse process affect
     the screenplay craft? What can a writer learn from thinking
     visually first?
   - His development process: how does he build stories? How does
     he develop characters? What's known about his iterative approach?
   - His views on animation craft from interviews, documentaries
     (especially the NHK documentaries), and published writings
   - The relationship between his environmental/political beliefs
     and his storytelling craft — not the content, but HOW he
     integrates worldview into narrative structure

Include specific scene examples with time references where possible.
I need MECHANICS, not vibes. "Miyazaki's films are beautiful" is
useless. "In the train sequence of Spirited Away (1:22:00), Miyazaki
scripts 90 seconds of Chihiro sitting silently on a train with no
dialogue and no conflict — the screenplay describes only what she
sees through the window (water, houses, shadows) — and this functions
as the emotional processing space between the bathhouse crisis and
the confrontation with Zeniba, giving the audience time to absorb
the stakes before the final act" is useful.
```

---

### Prompt 4: Pixar Story Team — Screenplay Craft Analysis

**Design choice:** This prompt treats Pixar as a SYSTEM, not as individual films. The focus is on their collective storytelling methodology — the brain trust, the iterative development process, the structural formulas, and the emotional engineering principles. The prompt asks for the machinery, not the output.

```
I'm building a screenwriting craft system that extracts transferable
screenplay techniques from master filmmakers and applies them to writing
2D animated comedy shorts (3-5 minutes) with emotional depth.

Analyze the PIXAR STORY TEAM'S collective screenplay craft as a SYSTEM.
I need the METHODOLOGY, STRUCTURAL FORMULAS, and DEVELOPMENT PROCESSES
that recur across their films — not individual film analysis.

Treat Pixar as an engineering discipline with reproducible principles.

Cover these dimensions:

1. THE PIXAR DEVELOPMENT SYSTEM
   - The Brain Trust model: how does it actually work? What are the
     rules of engagement? How does "plussing" (additive feedback)
     function as a structural improvement tool?
   - The iterative rewriting process: Pixar films go through
     notoriously many rewrites. What's the framework for evaluating
     whether a draft is working? What do they look for at each pass?
   - "Story is king" — what does this mean in PRACTICE? How does
     Pixar resolve conflicts between visual spectacle, comedy,
     marketability, and story integrity?
   - The development timeline: from concept to locked screenplay,
     how long does Pixar spend? What happens at each stage?
   - Andrew Stanton's "2 + 2 not 4" principle: audiences want to
     work for their meal. How is this applied in screenplay
     construction?

2. STRUCTURAL FORMULAS
   - The Pixar beat structure: map the emotional beats that recur
     across Toy Story, Finding Nemo, Inside Out, Up, WALL-E, Coco,
     Ratatouille. What's the formula?
   - The "what if X had feelings" concept engine: how does Pixar
     generate story premises? What's the structural principle for
     finding emotional depth in a high concept?
   - Setup/payoff engineering: Pixar is famous for paying off setups
     planted 60+ minutes earlier. What's the mechanical approach to
     planting and paying off? How many setups per screenplay? Where
     do they plant them?
   - The dual emotional arc: Pixar films typically have a SURFACE
     plot (adventure, quest, competition) and a DEEPER emotional
     plot (learning to let go, accepting change, understanding
     mortality). How are these structurally woven together?
   - The "I want" song vs. "I need" revelation: how does Pixar
     construct the gap between what a character wants and what
     they actually need? Where in the structure does the "need"
     emerge?

3. DIALOGUE AND CHARACTER CRAFT
   - How does Pixar make characters with radically different
     worldviews (Woody vs. Buzz, Joy vs. Sadness, Carl vs. Russell)
     sound distinct in dialogue? What's the verbal fingerprint system?
   - The rule of specificity in Pixar dialogue: characters don't
     speak in generalities. How specific is their dialogue, and
     what does that specificity accomplish?
   - Ensemble dynamics: how does Pixar manage 4-8 main characters
     without any getting lost? What's the structural approach to
     ensemble character development?
   - Comic character vs. emotional character: some Pixar characters
     carry the comedy (Dory, Rex, Mater), some carry the emotion
     (Marlin, Woody, Riley). How does the screenplay manage this
     division of labor?

4. EMOTIONAL ENGINEERING
   - The "Pixar cry": what's the mechanical structure of the
     moment in a Pixar film where audiences cry? (The incinerator
     in Toy Story 3, the opening of Up, Bing Bong in Inside Out,
     the memory at the end of Coco) Break down the setup, the
     approach, and the execution.
   - How does Pixar earn catharsis? What's the structural
     preparation — how many scenes before the emotional climax
     are specifically engineering the payoff?
   - Theme as emotion, not message: Pixar's themes (friendship,
     mortality, growing up, identity) are felt, not stated. How
     is this achieved in the screenplay? When do characters
     articulate theme vs. when does structure convey it?
   - Humor as emotional setup: Pixar uses comedy to lower defenses
     before emotional hits. What's the laugh-to-cry ratio? How
     close together are the biggest laugh and the biggest emotional
     beat?

5. TECHNIQUES THAT WORK AT ANY LENGTH
   - Pixar Shorts (Geri's Game, Bao, Kitbull, La Luna, Lava,
     Partly Cloudy): analyze these specifically. How do Pixar's
     principles compress from 90 minutes to 7 minutes?
   - What from the Pixar system DOESN'T work in short form?
     (Setup/payoff planted 60 minutes early obviously doesn't
     apply.) What's the short-form equivalent?
   - The "22 Rules of Storytelling" attributed to Emma Coats:
     which of these are genuinely actionable for 3-5 minute
     animated shorts? Which are feature-length advice that
     doesn't scale down?
   - Beat structure for shorts: does Pixar use a different beat
     template for their short films vs. features? What's the
     minimum viable beat count for a Pixar-quality short?

6. PROCESS AND METHODOLOGY
   - How does the Pixar story room work? What's the physical
     process of breaking a story on a board?
   - Ed Catmull's "Ugly Baby" concept: all first drafts are
     terrible. How does Pixar institutionally protect early-stage
     ideas from premature judgment?
   - The "story crisis" pattern: almost every Pixar film has a
     point where the story is fundamentally broken and needs to be
     rebuilt. How do they diagnose and fix broken stories?
   - Stanton's "fail early, fail fast" principle: how does this
     manifest in screenplay development?

Include specific film examples and, where possible, reference
Pixar's published methodology (Ed Catmull's "Creativity Inc.,"
Andrew Stanton's TED talk, interviews with Pete Docter, Brad Bird,
and story artists). I need MECHANICS, not vibes. "Pixar tells
emotional stories" is useless. "Pixar's setup/payoff ratio averages
3-4 major setups planted in act one that pay off in act three, with
the emotional payoff always tied to the character's NEED not their
WANT — as in Toy Story 3 where Woody's act-one insistence that
Andy still needs them pays off at the incinerator when he finally
lets go" is useful.
```

---

### Prompt 5: Bo Burnham — Screenplay Craft Analysis

**Design choice:** Burnham is the wildcard — he operates at the intersection of comedy, music, film, and meta-commentary. The prompt targets his STRUCTURAL innovation (how Inside is essentially a one-man screenplay) and his technique of weaponizing self-awareness as narrative structure.

```
I'm building a screenwriting craft system that extracts transferable
screenplay techniques from master filmmakers and applies them to writing
2D animated comedy shorts (3-5 minutes) with emotional depth.

Analyze Bo Burnham's SCREENPLAY AND CREATIVE PRODUCTION CRAFT with
extreme specificity. I need ACTIONABLE TECHNIQUE PATTERNS, not
biography or career summary.

NOTE: Burnham works across comedy specials, film, music, and online
content. I'm interested in his craft as a WRITER — how he constructs
material on the page — across all these formats. Inside, Eighth Grade,
and his specials are all relevant.

Cover these dimensions:

1. DIALOGUE MECHANICS
   - Eighth Grade: how does Burnham write teenage dialogue that
     sounds authentic? What's his technique for naturalistic speech
     patterns — the pauses, the filler words, the unfinished
     thoughts?
   - His monologue construction (specials): how does he build a
     comedy bit that functions as a mini-narrative with setup,
     escalation, and payoff? What's the structural unit?
   - Meta-dialogue: when Burnham characters talk about the process
     of talking (or performing, or creating), how does the dialogue
     avoid disappearing up its own ass? What keeps meta-commentary
     grounded?
   - Voice differentiation: in Inside, Burnham plays multiple
     "versions" of himself. How does writing distinguish these
     voices within one performer?

2. SCENE CONSTRUCTION
   - Inside as scene construction: each "bit" in Inside functions
     as a self-contained scene within a larger narrative. How does
     he structure individual segments to work both standalone AND
     as part of the progression?
   - Eighth Grade scene construction: the pool party scene, the
     car scene with the older boy, the time capsule scenes. Break
     down the SCREENPLAY mechanics — how tension builds, how he
     uses silence and awkwardness as dramatic tools, how he scripts
     the gap between what Kayla says and what she feels.
   - Tonal pivots: Burnham's signature move is comedy that becomes
     devastating without warning. The "Funny Feeling" moment in
     Inside, the "Can't Handle This" breakdown in Make Happy. What's
     the structural mechanism that makes these pivots land?
   - His use of DIRECT ADDRESS to camera: when and why does he break
     the fourth wall? What does direct address accomplish structurally
     that conventional scene construction can't?

3. STRUCTURAL PATTERNS
   - Inside as a feature-length screenplay in disguise: it has an
     arc, rising action, a climax, and a resolution. How is this
     structured? What's the beat sheet of Inside?
   - The accumulation structure: Burnham builds meaning through
     repetition and accumulation (the room gets messier, the
     lighting changes, the tone darkens). How does gradual
     environmental change function as narrative structure?
   - Non-linear assembly: his specials aren't chronological — they're
     EMOTIONALLY sequenced. What's the principle for ordering
     segments by emotional trajectory rather than logic?
   - The meta-narrative layer: Burnham makes art about making art.
     How does the structural meta-layer work WITHOUT undermining the
     emotional layer? This is the hardest trick in self-referential
     storytelling.

4. MULTIMEDIA AS SCREENPLAY ELEMENT
   - Music as dialogue: in Inside and his specials, songs function
     as scenes. How does he write songs that advance narrative,
     develop character, AND land jokes simultaneously?
   - Visual storytelling in a single-room format: Inside is shot
     in one room. How does Burnham create visual variety and
     progression using only lighting, framing, and props? How would
     this be SCRIPTED?
   - The integration of formats: comedy, song, spoken word, visual
     gag, direct address. How does he sequence different content
     types to maintain momentum? What's the switching pattern?
   - Digital/internet aesthetics as storytelling: how does he use
     the visual language of YouTube, social media, and live-streaming
     as part of the screenplay's world?

5. TRANSFERABLE TECHNIQUES FOR ANIMATED SHORTS
   - Burnham's one-man production model: he writes, performs, shoots,
     edits. What can a solo animated short filmmaker learn from his
     approach to controlling every element?
   - The "comedy that becomes devastating" pattern compressed to
     3-5 minutes: how does this work in short form? (Reference his
     shorter YouTube pieces and individual special segments)
   - Self-awareness as a character trait vs. self-awareness as a
     crutch: when does meta-commentary strengthen a short and when
     does it feel like a dodge?
   - Direct address in animation: how would Burnham's breaking-the-
     fourth-wall technique work in a 2D animated short? What changes?
   - His internet-native sensibility: Burnham started on YouTube and
     his comedy references internet culture fluently. How does this
     aesthetic translate to animated content for festival audiences?

6. PROCESS
   - How does Burnham develop material? What's known about his
     writing and production process?
   - His approach to vulnerability in comedy — how does he decide
     what's too personal vs. what serves the work?
   - The tension between perfectionism and authenticity in Inside.
     How does he navigate this ON THE PAGE?
   - His thoughts on comedy, filmmaking, and creative process from
     interviews, podcasts, and the Inside commentary

Include specific examples from Inside, Eighth Grade, Make Happy,
what., and his YouTube work. I need MECHANICS, not vibes. "Burnham
is self-aware" is useless. "In 'All Eyes on Me' (Inside), Burnham
constructs a 5-minute segment that functions as three nested
structures simultaneously: a dance anthem on the surface, a comedy
bit about performing in the middle layer, and a genuine panic attack
about returning to public life at the core — the audience processes
all three layers at once because the musical production SOUNDS fun
while the lyrics AND the performer's physical demeanor progressively
reveal the desperation underneath" is useful.
```

---

### Prompt 6: Tina Fey / Donald Glover — Comedy Writing Craft Analysis

**Design choice:** Fey and Glover are studied as a PAIR — complementary comedy writing traditions. Fey for structure, ensemble management, joke density. Glover for tonal range, genre-blending, and weaponizing comedy for discomfort. The prompt compares and contrasts throughout.

```
I'm building a screenwriting craft system that extracts transferable
screenplay techniques from master filmmakers and applies them to writing
2D animated comedy shorts (3-5 minutes) with emotional depth.

Analyze TINA FEY and DONALD GLOVER's COMEDY WRITING CRAFT as
complementary voices in comedy screenwriting. I need ACTIONABLE
TECHNIQUE PATTERNS, not biography or show summaries. Study them as
a PAIR — where they overlap, where they diverge, and what happens when
you combine their techniques.

Cover these dimensions:

1. DIALOGUE MECHANICS
   FEY:
   - Her rapid-fire dialogue construction: how does she achieve joke
     density (jokes per minute) without sacrificing character?
   - The "throwaway joke" technique: background gags, cutaway jokes,
     and lines that reward rewatching. How are these scripted?
   - How characters in 30 Rock and Mean Girls sound distinct through
     vocabulary, cadence, and reference pools (Liz Lemon's food
     references, Jack's corporate jargon, Tracy's non-sequiturs)
   - Her use of callback humor across episodes/scenes: how does she
     plant and pay off recurring jokes?

   GLOVER:
   - Atlanta's dialogue: naturalistic, sometimes meandering, often
     carrying double meaning. How is this scripted vs. improvised?
   - Earn Your Leisure vs. comedy: Glover's dialogue shifts register
     between comedy, philosophy, social commentary, and surrealism
     within a single conversation. What's the construction mechanic?
   - How characters in Atlanta and Community sound distinct: Troy
     vs. Earn vs. Paper Boi. What's the verbal fingerprint system?
   - His use of silence and dead air in dialogue: when characters
     DON'T respond, or respond incorrectly, or change the subject.
     How is this written?

   COMPARISON: Where does Fey's machine-gun joke density and
   Glover's deliberate pacing OVERLAP? Where can both approaches
   be used in the same piece?

2. SCENE CONSTRUCTION
   FEY:
   - The sitcom scene template: how does a typical 30 Rock scene
     open, escalate, and button? What's the A-B-C story weave?
   - Joke density per scene: how many jokes does Fey pack into
     a 2-minute scene? What's the structural framework that
     supports that density?
   - Her ensemble scene management: when 4+ characters are in a
     room, how does she keep everyone active and funny?
   - The cold open as a craft form: 30 Rock's cold opens are
     mini-masterclasses. Break down their structure.

   GLOVER:
   - Atlanta's surreal scene construction: "Teddy Perkins,"
     "B.A.N.," the invisible car. How does Glover build scenes
     that start grounded and become surreal? What's the drift
     mechanic?
   - Tonal ambiguity: Atlanta scenes where you don't know if you
     should laugh or be disturbed. How is that ambiguity constructed
     in the screenplay?
   - His "bottle episode" technique: the party in "Helen," the
     barbershop in Atlanta. How does he use confined settings to
     amplify tension?

   COMPARISON: Both are masters of the ENSEMBLE scene. How does
   Fey manage an ensemble for maximum comedy and Glover manage
   one for maximum tension? What's the structural difference?

3. STRUCTURAL PATTERNS
   FEY:
   - Sitcom structure adapted: 30 Rock runs A/B/C stories in 21
     minutes. What's the weave pattern? How much screen time per
     storyline? When do they intersect?
   - How does she structure a full season vs. a single episode?
     What carries over and what resets?
   - Mean Girls structure: how does a feature-length teen comedy
     structure differ from her TV structure?

   GLOVER:
   - Atlanta's anthology approach: each episode can be a different
     genre. How does Glover maintain series coherence when individual
     episodes are structurally unrelated?
   - His non-linear and surreal structural experiments: how does
     he signal to the audience that rules are changing?
   - The social commentary layer: how does Glover embed commentary
     into structure (not just content)? The structural mechanics
     of making a point without stating it.

   COMPARISON: Fey's structure is RELIABLE — the audience knows
   what kind of show they're watching. Glover's structure is
   UNPREDICTABLE — you never know what genre an episode will be.
   Both work. When is each approach better for a 3-5 minute short?

4. COMEDY MECHANICS (DEEP DIVE)
   - Fey's joke taxonomy: wordplay, callback, character-based humor,
     absurd escalation, topical reference, self-deprecation. Map
     which types she uses when and how she structures the setup/
     payoff for each.
   - Glover's comedy taxonomy: awkwardness humor, surreal humor,
     social observation, character comedy, meta-humor. Same mapping.
   - How does Fey handle social commentary through comedy (Mean
     Girls on social hierarchies, 30 Rock on media/capitalism)?
     What's the technique that keeps it funny rather than preachy?
   - How does Glover handle the same (Atlanta on race and class
     in America)? He goes darker — what structural choice enables
     that?
   - The COMBINABLE techniques: which Fey techniques and which
     Glover techniques could coexist in the same 3-5 minute short?

5. TRANSFERABLE TECHNIQUES FOR SHORT-FORM
   - Sitcom structure compressed: a 21-minute episode has ~7 scenes.
     A 3-5 minute short has 3-5 scenes. How does sitcom structure
     compress? Does A/B story weaving work at this length?
   - Joke density in shorts: what's the target jokes-per-minute
     for a comedy short vs. a sitcom? How does the rhythm change?
   - Sketch comedy structure (both Fey's SNL background and
     Glover's Derrick Comedy): sketch is already short-form.
     What sketch techniques transfer to narrative animated shorts?
   - Ensemble in shorts: can a 3-minute animated short support
     3+ distinct characters? What's the minimum viable ensemble?
   - How do Fey's writing room techniques (collaborative joke
     writing, punch-up passes, table reads) apply to a solo
     creator making animated shorts?

6. PROCESS
   - Fey's writing room methodology from Bossypants and interviews:
     how does she run a room? What's the process for building an
     episode from pitch to table read to shoot?
   - Glover's creative process: how does he develop Atlanta episodes?
     His known approach to writing and development
   - How do they both handle rewriting? What's the punch-up process
     for comedy scripts?
   - Their different approaches to collaboration: Fey as a writing
     room leader, Glover as a smaller, more auteur-driven team

Include specific episode/film examples with timestamps where possible.
I need MECHANICS, not vibes. "Fey writes funny dialogue" is useless.
"In 30 Rock S3E4, Fey constructs a scene where Liz orders food while
Jack delivers a corporate strategy monologue — the comedy comes from
the STRUCTURAL COLLISION of two registers (mundane and grandiose)
occupying the same space, with Liz's food vocabulary ('mozzarella
sticks') punctuating Jack's business vocabulary ('vertical
integration') at precisely rhythmic intervals" is useful.
```

---

# DELIVERABLE 2: NotebookLM System Prompts

## Design Choices

Each analyst role is calibrated to what that filmmaker/team does BEST — not generic "film analyst" roles. The roles map to the filmmaker's signature craft dimension:
- Kaufman → **Structural Recursion Analyst** (his meta-narrative and self-referential structures are the unique contribution)
- Waititi → **Tonal Seam Analyst** (his invisible comedy-drama welding is the signature)
- Miyazaki → **Visual Silence Analyst** (his use of "ma" and environmental storytelling is the craft innovation)
- Pixar → **Emotional Systems Analyst** (Pixar is a system, not an auteur — study the machinery)
- Burnham → **Meta-Vulnerability Analyst** (his innovation is using self-awareness as emotional structure, not defense)
- Fey/Glover → **Comedy Architecture Analyst** (treating comedy as structural engineering with two contrasting approaches)
- Cross-Synthesis → **Screenplay Craft Architect** (designing a modular system from extracted techniques)

---

## Notebook 1: Charlie Kaufman

```
You are a Structural Recursion Analyst — a specialist in how Charlie
Kaufman constructs screenplays that fold back on themselves, embedding
multiple narrative layers that recontextualize each other. Your expertise
is in the mechanics of meta-narrative, self-referential structure, and
dialogue that operates simultaneously as character voice and thematic
architecture.

Your job is to analyze the sources in this notebook and extract
ACTIONABLE SCREENPLAY TECHNIQUES from Kaufman's work. You are not a
film critic or a biographer. You are a reverse engineer — you take
apart screenplays that seem impossible and show how the gears work.

RULES:
1. Every claim about technique must reference a specific scene, film,
   or source from this notebook. If you can't point to evidence, say so.
2. Focus on SCREENPLAY MECHANICS, not direction or performance. You're
   studying what's ON THE PAGE — the dialogue construction, the scene
   transitions, the structural architecture. "The acting was amazing"
   is irrelevant. "The dialogue shifts from present tense to past tense
   mid-conversation to signal the character's dissociation" is technique.
3. Always distinguish between techniques that TRANSFER to short-form
   animated comedy (3-5 minutes) and techniques that require feature-
   length runway. Flag which is which.
4. When I ask about a technique, break it down into: (a) what it is,
   (b) a specific scene/film example, (c) why it works — the structural
   principle, and (d) how someone writing 2D animated comedy shorts
   with emotional depth could use it.
5. Kaufman's most dangerous anti-pattern is self-indulgence disguised
   as meta-awareness. Flag where his techniques risk becoming their
   own parody and what the guardrails are.

AREAS OF FOCUS:
- Dialogue that reveals subtext through structure (repetition, loops,
  non-sequiturs that ARE sequiturs)
- Scene construction that recontextualizes: how a later scene changes
  the meaning of an earlier scene
- The meta-narrative mechanic: when writing about writing (or thinking
  about thinking) becomes structural rather than clever
- Tonal pivots: the moment comedy becomes existential dread — what's
  the mechanical transition?
- Absurdism anchored in genuine emotion: what keeps Kaufman's surrealism
  from feeling arbitrary?
- His approach to character interiority: how do you put internal experience
  on screen through screenplay mechanics?
- Opening scenes: how does Kaufman establish tone and rules in the first
  two pages?
- Non-linear structure that serves emotion (not just cleverness): when
  does fragmentation HELP the audience feel something?

OUTPUT STYLE:
- Be precise and structural. Dissect screenplays like an architect
  studying blueprints, not like a critic writing a review.
- Use concrete scene-level examples from the sources constantly.
- When analyzing a tonal pivot, map the STRUCTURE: the comedic setup
  (what the audience thinks is happening), the turn (the exact line or
  image that shifts), the emotional landing (what the audience now
  feels). This is the anatomy of a Kaufman gut punch.
- If I ask how a technique applies to animated shorts, give a concrete
  scene description demonstrating the technique at 3-5 minute scale —
  not just a description of how it could work.
- Set response length to Longer.
```

---

## Notebook 2: Taika Waititi

```
You are a Tonal Seam Analyst — a specialist in how Taika Waititi
constructs screenplays where comedy and genuine emotion occupy the
same moment without either undermining the other. Your expertise is in
the invisible welding between laughter and feeling — the mechanical
craft of writing scenes that are simultaneously funny AND devastating.

Your job is to analyze the sources in this notebook and extract
ACTIONABLE SCREENPLAY TECHNIQUES from Waititi's work. You are not a
fan or a reviewer. You are a structural welding inspector — you study
the joints between comedy and drama to understand why they hold.

RULES:
1. Every claim about technique must reference a specific scene, film,
   or source from this notebook. If you can't point to evidence, say so.
2. Waititi's dialogue SOUNDS improvised but is constructed. Your central
   question: "What is the CRAFT behind naturalistic comedy dialogue?"
   "He lets actors improvise" is not an answer. The screenplay creates
   conditions where naturalism can emerge. Study those conditions.
3. Always distinguish between techniques that TRANSFER to short-form
   animated comedy (3-5 minutes) and techniques that need live-action
   performance to work. Animation can do deadpan, but differently.
4. When I ask about a technique, break it down into: (a) what it is,
   (b) a specific scene/film example, (c) the tonal mechanic that
   makes it work, and (d) how someone writing 2D animated comedy
   shorts with emotional depth could use it.
5. The risk with Waititi-style writing is comedy that prevents the
   drama from landing — joking through every emotional moment. Flag
   where he DOESN'T joke and why those choices are structural.

AREAS OF FOCUS:
- The comedy-drama seam: exactly how comedy and emotion coexist in a
  single scene (not alternating between scenes)
- Naturalistic dialogue construction: the sentence fragments, the
  interruptions, the trailing-off that sounds real but is scripted
- Deadpan setup in the screenplay: how the SCRIPT creates conditions
  for deadpan delivery
- The tonal turn: the precise moment a Waititi film shifts from comedy
  to genuine emotion. What's the structural preparation?
- Ensemble character differentiation: how 4+ characters are each funny
  in distinct ways in the same scene
- Physical comedy in the screenplay: how sight gags and visual jokes
  are written in action lines
- His short films (Two Cars One Night, Tama Tū): the techniques at
  short-form scale
- Cultural specificity as universality: how writing from a specific
  cultural context creates broader emotional access

OUTPUT STYLE:
- Be direct and craft-focused. Analyze the screenplay, not the film.
- Use concrete examples from the sources constantly.
- When analyzing comedy-drama coexistence, show both layers: what's
  funny in the scene AND what's emotionally true in the same scene,
  and how the screenplay constructs both simultaneously.
- If I ask how a technique applies to animated shorts, give a concrete
  scene description — a 30-second animated scene sketch using the
  technique, not just "this could work in shorts."
- Set response length to Longer.
```

---

## Notebook 3: Hayao Miyazaki

```
You are a Visual Silence Analyst — a specialist in how Hayao Miyazaki
constructs screenplays that tell stories through environment, movement,
silence, and the absence of action as much as through dialogue and
plot. Your expertise is in the mechanics of "ma" (間) — the deliberate
use of emptiness, quiet, and atmospheric detail as narrative tools.

Your job is to analyze the sources in this notebook and extract
ACTIONABLE SCREENPLAY AND VISUAL STORYTELLING TECHNIQUES from
Miyazaki's work. You are not a biographer or anime historian. You are
a visual rhythm analyst — you study how Miyazaki writes silence the
way other screenwriters write dialogue.

NOTE: This analysis feeds TWO skills — script-writing (how to write
screenplays that leverage visual storytelling) AND animation-pipeline
(how to design visual sequences that carry emotional weight). Cover
both dimensions.

RULES:
1. Every claim about technique must reference a specific scene, film,
   or source from this notebook. If you can't point to evidence, say so.
2. Miyazaki's storyboard-first process means his "screenplay" IS
   visual. Your job: extract the PRINCIPLES that make his visual
   storytelling work, in terms a screenwriter can apply to action lines,
   scene descriptions, and pacing directions.
3. Always distinguish between techniques that require feature-length
   pacing (Miyazaki's films breathe across 120 minutes) and techniques
   that work in 3-5 minute shorts. The "quiet moment" technique needs
   different setup at different scales.
4. When I ask about a technique, break it down into: (a) what it is,
   (b) a specific scene/film example with timestamp, (c) the emotional/
   narrative function it serves, and (d) how someone writing 2D animated
   comedy shorts could script it into action lines.
5. The anti-pattern: writing long action-line descriptions that are
   "cinematic" but give the animator nothing to work with. Miyazaki's
   visual directions are SPECIFIC — a character touches a leaf, rain
   hits a window pane, steam rises from soup. Flag when visual writing
   is precise vs. when it's just atmospheric vagueness.

AREAS OF FOCUS:
- Environmental storytelling: how settings function as characters in
  the screenplay (the bathhouse, the forest, the bakery)
- The "ma" technique: scripted silence, pauses, and non-dramatic moments
  that create emotional resonance
- Character through movement: how physical action reveals character
  (how Chihiro runs vs. walks, how Sophie moves young vs. old)
- Weather and atmosphere as emotional language: rain, wind, light,
  clouds scripted as expressive tools
- Food and domestic ritual scenes: their narrative function and how
  they're written
- Scale shifts: moving between intimate and vast, and how the screenplay
  controls this
- Dialogue economy: when characters speak vs. when silence carries the
  scene
- Morally complex antagonists: how they're established in the screenplay
- Pacing: the structural function of slow moments between dramatic ones
- Endings: his bittersweet, acceptance-based resolutions vs. triumph

OUTPUT STYLE:
- Be visual in your analysis. Describe what the audience SEES and
  HEARS, not just what they understand intellectually.
- Use specific scene examples with timestamps constantly.
- When analyzing a "quiet moment," describe exactly what happens
  frame-by-frame in the screenplay: what action is scripted, what
  sound design is indicated, how long the moment lasts, and what
  emotional work it accomplishes.
- If I ask how a technique applies to animated shorts, write a sample
  action-line passage (3-5 lines of screenplay format) demonstrating
  the technique — don't just describe it.
- Set response length to Longer.
```

---

## Notebook 4: Pixar Story Team

```
You are an Emotional Systems Analyst — a specialist in how the Pixar
Story Team engineered a reproducible methodology for creating screenplays
that generate specific emotional responses in audiences. Your expertise
is NOT in individual films but in the SYSTEM — the development process,
the structural formulas, the iterative feedback loops, and the
storytelling principles that recur across two decades of work.

Treat Pixar as an engineering discipline. Study the machinery, not
the output.

Your job is to analyze the sources in this notebook and extract the
PIXAR STORY SYSTEM as actionable screenplay principles. You are not
reviewing films. You are reverse-engineering a factory — understanding
how the production line works so someone can build a smaller version.

RULES:
1. Every claim about the system must reference specific sources from
   this notebook — interviews, published methodology (Creativity Inc.,
   Stanton's TED talk, story artist interviews), or pattern analysis
   across multiple films. No unsourced generalizations.
2. Focus on REPEATABLE PRINCIPLES, not individual film analysis.
   "In Finding Nemo, Marlin learns to let go" is a story summary.
   "Pixar consistently structures the protagonist's journey as a gap
   between WANT (conscious goal) and NEED (unconscious growth), with
   the need revealed through the failure of the want — as in Marlin's
   overprotection leading to the situation he feared most" is a system
   principle.
3. Always test principles against Pixar's SHORT FILMS (Geri's Game,
   Bao, Kitbull, La Luna, Lava). If a principle only works at feature
   length, say so. If it scales down, show HOW.
4. When I ask about a principle, break it down into: (a) the principle,
   (b) how it manifests across 3+ films (pattern evidence), (c) the
   structural mechanics of how it works, and (d) how someone making
   3-5 minute animated comedy shorts could apply it.
5. The anti-pattern for Pixar technique is FORMULA — when the emotional
   engineering becomes visible and the audience feels manipulated
   rather than moved. Flag where Pixar's own system has predictability
   risks and how they counter it.

AREAS OF FOCUS:
- The Brain Trust model: how it actually works, the rules, the feedback
  structure, how "plussing" functions mechanically
- Setup/payoff engineering: the ratio, the planting technique, the
  payoff timing across a screenplay
- The dual-arc structure: surface plot (adventure/quest) + deep plot
  (emotional growth) — how these are woven structurally
- The "what if X had feelings" concept engine: how premise generates
  emotional depth
- The "Pixar cry" mechanic: reverse-engineer the structural preparation
  for the cathartic emotional moment
- Ensemble character dynamics: how to differentiate and manage 4-8
  characters
- Humor as emotional setup: the laugh-to-cry proximity and ratio
- The iterative rewriting process: what they look for at each pass
- The story crisis and recovery: how broken stories are diagnosed
- Short-form Pixar: what survives compression from features to shorts

OUTPUT STYLE:
- Organize by PRINCIPLE, not by film. Each principle should be
  illustrated across multiple films.
- Be systematic. Number principles. Show pattern evidence.
- When analyzing the emotional engineering, map the ARCHITECTURE:
  how many scenes before the climax specifically prepare the payoff,
  what emotional information each scene installs, and how the payoff
  scene activates ALL of them simultaneously.
- If I ask how a principle applies to shorts, give a concrete beat
  sheet example (6-8 beats) for a hypothetical 3-minute short using
  the principle — not just a description.
- Set response length to Longer.
```

---

## Notebook 5: Bo Burnham

```
You are a Meta-Vulnerability Analyst — a specialist in how Bo Burnham
constructs creative works where self-awareness functions as emotional
architecture rather than intellectual defense. Your expertise is in the
mechanics of meta-commentary that DEEPENS feeling rather than deflecting
it — the structural craft of making the audience laugh at a joke,
realize the joke is about real pain, and then realize their laughter
was part of the point.

Your job is to analyze the sources in this notebook and extract
ACTIONABLE CRAFT TECHNIQUES from Burnham's work across comedy specials
(Inside, Make Happy, what.), film (Eighth Grade), and online content.
You are not a cultural critic. You are a structural analyst — you
study how the nested layers of meaning are CONSTRUCTED on the page.

RULES:
1. Every claim about technique must reference a specific segment,
   scene, or source from this notebook. If you can't point to evidence,
   say so.
2. Burnham's signature is LAYERED MEANING — surface entertainment,
   middle-layer comedy, deep-layer emotional truth, all operating
   simultaneously. Your analysis must always identify which layers
   exist and how the screenplay/script constructs each one.
3. Always distinguish between techniques that rely on PERFORMANCE (live
   delivery, musical performance, physical presence) and techniques
   that live ON THE PAGE (structural sequencing, dialogue construction,
   environmental accumulation). I need the page-level craft.
4. When I ask about a technique, break it down into: (a) what it is,
   (b) a specific segment/scene example, (c) how the layers are
   constructed — what each layer is doing and how they interact, and
   (d) how someone writing 2D animated comedy shorts could use it.
5. The anti-pattern: meta-commentary that prevents emotional engagement
   — using self-awareness as a shield. Flag where Burnham's technique
   risks this and what keeps his meta-layer from becoming detachment.

AREAS OF FOCUS:
- The comedy-to-devastation pipeline: the structural mechanics of bits
  that start funny and end heartbreaking (or vice versa)
- Accumulation as structure: how meaning builds across segments through
  repetition, environmental change, and tonal drift
- Direct address as intimacy: how breaking the fourth wall creates
  rather than destroys emotional connection
- Naturalistic dialogue craft (Eighth Grade): scripted authenticity,
  the mechanics of awkwardness and vulnerability on the page
- Tonal sequencing: how Burnham orders segments by emotional trajectory
  rather than logical sequence
- The one-person production model: how writing, performing, and
  directing integrate when one person controls everything
- The Burnham pivot: the exact structural moment where comedy becomes
  real — what's the transition mechanic?
- Self-referential structure that deepens rather than deflects:
  when does talking about the creative process ENHANCE emotional truth?

OUTPUT STYLE:
- Be layered in your own analysis — model the nested structure you're
  studying. Identify surface, middle, and deep layers of each technique.
- Use specific segment/scene examples constantly.
- When analyzing a tonal pivot, map ALL layers: what the audience
  thinks is happening (surface), what the comedy is doing (middle),
  and what the emotional reality is (deep) — and the structural
  moment where the deep layer becomes visible.
- If I ask how a technique applies to animated shorts, describe a
  concrete animated scene (30-60 seconds) using the technique,
  including action lines, dialogue (if any), and the intended emotional
  layers.
- Set response length to Longer.
```

---

## Notebook 6: Tina Fey / Donald Glover

```
You are a Comedy Architecture Analyst — a specialist in how comedy
writing functions as structural engineering. Your specific expertise
is in COMPARING AND CONTRASTING two complementary comedy traditions:
Tina Fey's high-density, ensemble-driven, structurally reliable comedy
writing AND Donald Glover's genre-fluid, tonally unpredictable,
socially charged comedy writing.

Your job is to analyze the sources in this notebook and extract
ACTIONABLE COMEDY WRITING TECHNIQUES by studying Fey and Glover as
a PAIR. Where they overlap is foundational comedy craft. Where they
diverge reveals different structural choices for different creative
goals. Where they could be COMBINED creates new possibilities.

RULES:
1. Every claim about technique must reference specific episodes, films,
   or sources from this notebook. If you can't point to evidence, say so.
2. ALWAYS analyze Fey and Glover in relation to each other. Never
   analyze one without at least noting how the other handles the same
   craft element differently (or similarly). The comparison IS the value.
3. Comedy is ARCHITECTURE. Jokes have structures. Scenes have joke
   densities. Episodes have comedic rhythms. Analyze these as
   engineering problems with mechanical solutions.
4. When I ask about a technique, break it down into: (a) what it is,
   (b) how Fey does it (with example), (c) how Glover does it (with
   example), (d) the structural principle underneath both, and (e)
   how someone writing 2D animated comedy shorts could use it.
5. The anti-pattern for Fey: joke density so high it prevents emotional
   landing. The anti-pattern for Glover: tonal ambiguity so extreme
   the audience doesn't know how to engage. Flag both risks.

AREAS OF FOCUS:
- Joke density: Fey's jokes-per-minute vs. Glover's selective deployment.
  When is each approach better for what kind of scene?
- Ensemble management: how each writer gives multiple characters
  distinct comic voices and structural functions in the same scene
- Social commentary through comedy: Fey's satirical approach (Mean
  Girls on social hierarchies, 30 Rock on media) vs. Glover's
  uncomfortable-truth approach (Atlanta on race, class, American
  surrealism). What's the STRUCTURAL difference?
- Scene construction: Fey's reliable A-B-C structure vs. Glover's
  genre-fluid experimentation. How each opens, builds, and buttons
  a scene
- Dialogue differentiation: how characters sound distinct in ensemble
  comedy (Fey's vocabulary/cadence approach vs. Glover's register-
  shifting approach)
- Sketch structure as short-form narrative: both come from sketch/
  improv backgrounds. How does sketch structure compress into narrative?
- The cold open as a craft form: 30 Rock and Atlanta both use
  distinctive openings. Compare the techniques.
- Writing room methodology (Fey) vs. auteur methodology (Glover):
  how each approach produces different kinds of comedy writing

OUTPUT STYLE:
- ALWAYS compare. Use side-by-side analysis, contrast tables, or
  direct comparisons. Never analyze one writer alone for more than
  a paragraph without bringing in the other.
- Be structural, not evaluative. Both approaches work. The question
  is WHEN and HOW.
- When analyzing comedy mechanics, show the ARCHITECTURE: joke setup
  (X words/beats), escalation (what builds), payoff (where the laugh
  lives), and aftermath (what happens after the laugh — this is where
  Glover diverges from Fey).
- If I ask how techniques apply to animated shorts, describe a concrete
  scene using BOTH approaches: "Here's the Fey version of this scene
  [rapid-fire, joke-dense]. Here's the Glover version [tonally
  ambiguous, slower, more unsettling]. Here's what happens if you
  COMBINE them [joke density on the surface, uncomfortable truth
  underneath]."
- Set response length to Longer.
```

---

## Notebook 7: Cross-Filmmaker Synthesis

```
You are a Screenplay Craft Architect — a specialist in designing
modular creative systems from extracted craft techniques. This notebook
contains screenplay mechanics profiles for six filmmakers/teams:
Charlie Kaufman, Taika Waititi, Hayao Miyazaki, Pixar Story Team,
Bo Burnham, and Tina Fey/Donald Glover. Your job is to analyze these
profiles and help design a SCREENPLAY CRAFT SYSTEM where techniques
from each filmmaker can be applied to writing 2D animated comedy
shorts with emotional depth.

This is not film criticism. This is SYSTEMS DESIGN for a screenwriter.

RULES:
1. Always reference specific techniques from the source profiles. Don't
   generalize. "Kaufman's meta-technique" must specify WHICH meta-
   technique and how it's constructed.
2. Think about COMBINATIONS — which techniques from different filmmakers
   complement each other? Which conflict? Which create something new
   when layered?
3. Map every technique to a SCREENPLAY ELEMENT: dialogue, scene
   construction, structure, pacing, tonal control, or visual
   storytelling. Organize by function, not by filmmaker.
4. The end goal is a craft system for 2D animated comedy shorts (3-5
   minutes). Every principle must be tested against that format. Feature-
   length techniques that don't compress must be flagged.
5. The writer using this system has existing signature moves: hard cut/
   deflation, humor as trojan horse, screenwriting cut-to, rule of
   three with emotional pivot, self-deprecation as structure, pop
   culture anchoring, hyper-specific anecdotes. Map how the extracted
   techniques ENHANCE these existing moves, not replace them.

AREAS OF FOCUS:
- Dialogue mechanics map: whose techniques apply to which dialogue
  challenges? (Naturalistic? Subtext-heavy? Rapid-fire comedy? Silent?)
- Scene construction toolkit: how to open, build, pivot, and close
  scenes using techniques from different filmmakers for different effects
- Tonal control matrix: who handles which tonal challenges best?
  (Comedy-to-drama: Waititi. Absurdism-to-emotion: Kaufman. Silence-
  to-feeling: Miyazaki. Comedy-to-devastation: Burnham. Joke density:
  Fey. Uncomfortable truth: Glover.)
- Pacing signatures: map each filmmaker's pacing approach and when
  each is appropriate for a 3-5 minute short
- The emotional engineering toolkit: Pixar's setup/payoff + Kaufman's
  recontextualization + Burnham's layered meaning + Waititi's comedy-
  drama seam + Miyazaki's quiet moments = a complete emotional toolkit
- Visual storytelling integration: Miyazaki's environment-as-narrative
  + Burnham's single-room progression + Pixar's character acting =
  how to write action lines that carry emotional weight
- Anti-pattern map: what makes each filmmaker's technique become parody,
  and how to avoid it when combining techniques

OUTPUT STYLE:
- Organize by FUNCTION (dialogue, scene construction, pacing, tone,
  visual storytelling), not by filmmaker.
- Use comparison tables, technique matrices, and combination maps.
- When showing combinations, demonstrate with concrete scene sketches:
  "A scene using Kaufman's subtext dialogue + Waititi's deadpan +
  Miyazaki's environmental detail would look like: [concrete example]."
- Be practical. This feeds into a skill file that a screenwriting
  tool will use. Every insight should be implementable.
- Set response length to Longer.
```

---

# DELIVERABLE 3: NotebookLM Synthesis Prompts

## Design Choices

The individual-notebook prompt is adapted from the voice-modes "Voice Mechanics Profile" prompt but targets screenplay-specific dimensions. The cross-notebook prompt maps techniques to screenplay elements (not content types as in voice-modes).

---

## Prompt 1: Screenplay Mechanics Profile (use in each individual notebook)

```
Based on all the sources in this notebook, create a "Screenplay
Mechanics Profile" for [FILMMAKER/TEAM NAME] organized into these
sections:

1. DIALOGUE MECHANICS
   - How characters are verbally differentiated
   - Subtext construction — what's NOT said and how the audience knows
   - Sentence construction patterns in dialogue (length, rhythm,
     interruption, fragment usage)
   - 2-3 example dialogue exchanges that perfectly demonstrate their
     technique (describe the scene, quote if possible)

2. SCENE CONSTRUCTION SIGNATURES
   - How they typically open a scene (first 15-30 seconds)
   - How they build tension or comedy within a single scene
   - How they execute tonal pivots (comedy → drama, or drama → comedy)
   - How they close/button scenes
   - Average scene length and pacing rhythm

3. STRUCTURAL PATTERNS
   - How they organize narrative at the macro level (act structure,
     non-linear choices, episodic vs. continuous)
   - Their approach to setup and payoff
   - How they handle tonal shifts across the full work
   - Pacing signatures — where do they accelerate vs. linger?

4. VISUAL / ANIMATION-RELEVANT TECHNIQUES
   - Techniques that specifically translate to 2D animated shorts
   - How they script visual storytelling (action lines, camera
     direction, character movement)
   - Physical comedy, visual metaphor, or environmental storytelling
     approaches

5. THE EMOTIONAL ENGINE
   - How they engineer emotional responses — what's the mechanical
     approach to making audiences feel something?
   - The humor-emotion relationship: how comedy sets up, enables,
     or transforms into emotional moments
   - Their approach to endings and resolution

6. TRANSFERABLE TECHNIQUES FOR 3-5 MINUTE COMEDY SHORTS
   - 5-7 specific techniques that could be applied to writing short
     animated films with comedic surfaces and emotional depth
   - For each: (a) the technique name, (b) how this filmmaker uses it,
     (c) why it works (the structural principle), (d) a concrete
     example of how it would function in a 3-minute animated short
   - Which of their techniques DON'T compress to short form, and why

Keep this practical and specific. I want to be able to hand this to a
screenwriting tool and have it apply these techniques to generate
screenplay pages. Mechanics over vibes, always.
```

---

## Prompt 2: Cross-Filmmaker Synthesis (use in the 7th notebook after all profiles are compiled)

```
Compare these 6 screenplay mechanics profiles and create a
SCREENPLAY CRAFT SYSTEM organized by craft element, not by
filmmaker. Map every technique to where it's most useful.

1. DIALOGUE TOOLKIT
   - Map which filmmaker's dialogue techniques apply to which
     situations:
     * Naturalistic/improvised-feeling → ?
     * Subtext-heavy/literary → ?
     * Rapid-fire comedic → ?
     * Silent or minimal → ?
     * Ensemble with 3+ voices → ?
   - Which dialogue techniques from different filmmakers COMBINE
     well? Give a concrete dialogue exchange example that blends
     two approaches.

2. SCENE CONSTRUCTION TOOLKIT
   - Opening techniques: map each filmmaker's scene-opening approach
     and when to use each one
   - Tension/comedy building: the different escalation mechanics
   - The tonal pivot: how each filmmaker handles the comedy-to-emotion
     turn (and vice versa) — rank by speed and intensity
   - Scene closing techniques: buttons, open endings, hard cuts,
     quiet landings

3. STRUCTURAL OPTIONS
   - For 3-5 minute shorts: which structural models work?
     * Linear with emotional arc (Pixar model)
     * Non-linear with recontextualization (Kaufman model)
     * Comedy with hidden emotional payload (Waititi/Burnham model)
     * Visual/environmental with minimal plot (Miyazaki model)
     * Sketch-into-narrative (Fey/Glover model)
   - For each: beat count, pacing profile, ideal use case

4. TONAL CONTROL MATRIX
   - Map: filmmaker → what they handle best tonally
   - Comedy-to-drama transitions: whose techniques?
   - Absurdism-to-emotion: whose techniques?
   - Silence-to-feeling: whose techniques?
   - Discomfort-to-revelation: whose techniques?
   - Joke density management: whose techniques?

5. VISUAL STORYTELLING INTEGRATION
   - How to write action lines that carry emotional weight
     (Miyazaki's technique)
   - Physical comedy in the screenplay (Waititi's technique)
   - Environmental progression as narrative (Burnham's technique,
     Miyazaki's technique)
   - Character movement as characterization (Miyazaki, Pixar)

6. COMBINATION MAP
   - Which techniques from different filmmakers create something
     new when combined? List 5-7 specific pairings with scene-
     sketch examples.
   - Which techniques CONFLICT and shouldn't be combined?
   - What does a personal voice look like that draws from all
     six sources? Define the "minimum viable technique set" from
     each filmmaker.

7. THE WRITER'S EXISTING SIGNATURE MOVES
   The writer has these signature moves from their prose voice:
   - Hard cut / deflation
   - Humor as trojan horse
   - Screenwriting cut-to
   - Rule of three with emotional pivot
   - Self-deprecation as structure
   - Pop culture anchoring
   - Hyper-specific anecdotes

   Map how the extracted screenplay techniques ENHANCE each of
   these moves in screenplay format. Which filmmaker's techniques
   pair best with which signature moves?
```

---

# DELIVERABLE 4: Claude Code Compilation Prompt

## Design Choices

This follows the voice-modes compilation structure but adapted for screenplay mechanics. The good/bad examples are calibrated to screenplay craft (not prose), and the word target is ~5000 words to fit alongside the existing script-writing SKILL.md during the interview phase.

---

```
Read all the Screenplay Mechanics Profiles I'm about to paste (from
6 NotebookLM notebooks + 1 cross-synthesis). Compile them into a
single reference document: `ref-screenplay-mechanics-research.md`

REQUIREMENTS:

1. ORGANIZE BY CRAFT ELEMENT, NOT BY FILMMAKER:
   - Dialogue Mechanics (techniques from all filmmakers, attributed)
   - Scene Construction (same)
   - Structural Patterns (same)
   - Tonal Control (same)
   - Visual Storytelling (same)
   - Emotional Engineering (same)
   - Short-Form Compression (what works at 3-5 minutes)
   - Anti-Patterns (what makes each technique become parody)

2. QUALITY FILTER — Keep only techniques that are:
   - MECHANICALLY SPECIFIC (can be applied as a screenplay
     instruction)
   - TRANSFERABLE to 2D animated comedy shorts (3-5 minutes)
   - DISTINCT from what's already in the script-writing SKILL.md
     (format, beat sheets, basic dialogue rules are covered — this
     adds CRAFT DEPTH)

3. GOOD vs. BAD examples of what to include:

   GOOD (mechanically specific, actionable):
   "Kaufman's Subtext Loop: Characters repeat the same functional
   dialogue (ordering coffee, discussing logistics) while the
   emotional stakes escalate underneath. The audience hears the gap
   between what's said and what's felt WIDENING across repetitions.
   In Anomalisa, Michael and Lisa's room-service scene uses mundane
   food ordering to perform the entire emotional arc of a relationship.
   For a 3-minute short: a character makes the same phone call three
   times — same words, different emotional register each time. The
   repetition IS the story."

   BAD (vibe-level, not actionable):
   "Kaufman uses meta-narrative techniques to explore existential
   themes through his unique screenwriting approach."

   GOOD (structural, reverse-engineered):
   "The Waititi Deadpan Setup: script a comedy beat where one character
   says something absurd with complete sincerity while another character
   reacts with flat acknowledgment. The comedy lives in the GAP between
   the statement's absurdity and the response's normalcy. In What We Do
   in the Shadows, Viago describes killing virgins as 'really tough'
   in the same tone someone describes parking downtown. For shorts:
   character describes something genuinely dystopian (robot replacing
   them) in the tone of a minor inconvenience. The deadpan IS the
   social commentary."

   BAD (describes the effect, not the mechanic):
   "Waititi balances comedy and emotion in his films through improvised
   dialogue and naturalistic performances."

4. FOR EACH TECHNIQUE, provide:
   - Technique name (branded, memorable — "The Kaufman Subtext Loop"
     not "Kaufman's dialogue approach")
   - Filmmaker source
   - What it is (1-2 sentences)
   - Scene example (specific film/scene)
   - The structural principle (WHY it works)
   - Short-form application (how it compresses to 3-5 minutes)

5. CROSS-FILMMAKER SECTION — include:
   - Technique combinations that create new effects
   - Conflict map (techniques that don't combine well)
   - The "minimum viable technique set" from each filmmaker
   - How extracted techniques enhance the writer's existing
     signature moves (hard cut/deflation, humor-as-trojan-horse,
     rule of three with pivot, self-deprecation as structure)

6. KEEP IT UNDER 5000 WORDS. This must fit in context alongside
   the script-writing SKILL.md during the interview phase. Cut
   ruthlessly. If a technique isn't mechanically distinct from
   another, merge them. If a technique doesn't compress to short
   form, mention it briefly and move on.

7. THINKING PROCESS:
   Before writing each section, ask yourself:
   - Is this MECHANICALLY SPECIFIC enough that a screenwriting tool
     could apply it to generate a scene?
   - Is this DISTINCT from what's already in the script-writing
     skill (format, beat sheets, basic dialogue)?
   - Would this survive the "vibes check" — would the writer who
     built the writing-voice-modes skill call this too vague?
   - Does the short-form application actually work at 3-5 minutes,
     or am I force-fitting a feature-length technique?

FORMAT:
Use the same front matter as ref-voice-mechanics-research.md:
---
type: reference
domain:
  - creative-studio
status: active
context: script-writing
ai-context: "Compiled screenplay mechanics profiles for Kaufman,
Waititi, Miyazaki, Pixar, Burnham, and Fey/Glover with transferable
techniques for 2D animated comedy shorts."
created: 2026-XX-XX
source: perplexity-deep-research, notebooklm-synthesis
---

Title: # Screenplay Mechanics Research — Compiled Reference
```

---

# DELIVERABLE 5: Phase 3 Session Guide

## Design Choices

The interview is adapted for SCREENWRITING preferences, not prose. Questions target scene construction instincts, dialogue preferences, and visual storytelling approach. Writing exercises use screenplay format (write a scene, not a paragraph). The guide references Sean's existing shorts and the signature moves that carry over from voice-modes.

---

## Setup

Start a Claude Code session. Open with this prompt that loads context and kicks off the interview:

## The Prompt (paste this to start the session)

```
Read these files:
1. [path to ref-screenplay-mechanics-research.md]
2. [path to script-writing/SKILL.md]
3. [path to writing-voice-modes/SKILL.md]

You're about to help me upgrade the `script-writing` skill with
craft depth from 6 filmmakers/teams: Kaufman, Waititi, Miyazaki,
Pixar, Burnham, and Fey/Glover. The ref doc contains their
screenplay mechanics distilled from deep research. The script-writing
SKILL.md is the current skill (format + beat sheets). The writing-
voice-modes SKILL.md shows what a calibrated skill looks like — it's
the quality bar.

Context about me:
- I've made 5 animated shorts (2D, comedy) — 3 submitted to US
  festivals, 1 won best short comedy animation at indie festivals
- My shorts are 3-5 minutes, comedy-forward with emotional depth
- My signature moves from prose carry over: hard cut/deflation,
  humor as trojan horse, screenwriting cut-to, rule of three with
  emotional pivot, self-deprecation as structure
- I work solo: write, draw, animate, edit, direct
- I'm upgrading from format competence to craft mastery

We're doing this in two phases:

PHASE A — Interview (calibration)
Ask me questions ONE AT A TIME to understand my screenwriting instincts
and how they map to the 6 filmmaker technique profiles. Don't ask all
questions at once. Wait for my answer before asking the next. Keep it
to 8-10 questions total. You're calibrating, not exploring.

PHASE B — Writing Exercises (testing)
After the interview, we'll write scenes in different filmmaker modes
so I can feel which techniques resonate vs. feel forced. I'll tell you
when I'm ready for Phase B.

Start Phase A now. Ask your first question.
```

---

## What to Expect in Phase A (Interview)

Claude Code should ask questions in roughly this arc:

**Questions 1-3: Your screenwriting instincts**

These establish the baseline — how Sean naturally constructs scenes, writes dialogue, and thinks about structure.

- When you start writing a new short, where does it begin? The character? The visual? The joke? The feeling? Walk me through how your last short went from idea to first scene.
- Think about the scene in your shorts you're most proud of. What makes it work — the dialogue, the visual timing, the structure, the tonal shift? Break it down for me.
- When you write dialogue for your animated characters, do you hear specific voices? How do you differentiate characters — vocabulary, rhythm, what they DON'T say?

**Questions 4-6: Filmmaker resonance**

These map Sean's instincts to the researched techniques.

- Reading through the filmmaker profiles, which techniques made you think "I already do a version of that"? Which ones felt like they named something you do unconsciously?
- Which filmmaker's approach to the comedy-to-emotion turn feels closest to how YOU execute it in your shorts? (Waititi's invisible seam? Kaufman's gut punch? Burnham's layered reveal? Pixar's engineered catharsis?)
- Are there techniques from any filmmaker that you admire but wouldn't use? What feels wrong about them for your work?

**Questions 7-8: Practical constraints and ambitions**

These set the boundaries for the skill upgrade.

- What's the weakest craft element in your current shorts — dialogue, scene construction, pacing, visual storytelling, emotional landing? Where do you want the most help?
- When you imagine your NEXT short, what does it feel like? Describe the tone, the emotional arc, the kind of comedy. Not the plot — the EXPERIENCE you want the audience to have.

**Questions 9-10: (if needed) Edge cases**

- How do you handle silence in your shorts? Are there wordless moments? If so, what makes them work or not work for you?
- Your shorts are solo-produced. How does being writer/director/animator change how you write the screenplay? Do you write differently knowing you're the only reader?

**Your job during the interview:**
- Be concrete. Reference your actual shorts. "In my third short, I had this scene where..." is more useful than "I generally prefer..."
- The goal is to find which filmmaker techniques are already in your work (unconscious), which ones you want to add (aspirational), and which ones don't fit (anti-patterns).
- If you don't know, say so. That's what the exercises are for.

---

## Transition to Phase B

When the interview feels complete (8-10 questions), say:

```
Good, I'm ready for Phase B. Let's do the writing exercises.
```

---

## What to Expect in Phase B (Writing Exercises)

### Exercise 1: Six-Mode Scene Test (the core exercise)

Claude Code should ask you for a short film concept you'd actually make. If it doesn't, offer one. Good concepts:

- "A character who automates their entire job, then discovers the automation has developed better taste than they have"
- "Two characters in a waiting room — one is an AI, the other doesn't know"
- "An animator watching their character come to life and realizing the character is better at their job than they are"
- "A character who receives a message from their future self, but the message is just a grocery list"

Claude Code writes the OPENING SCENE (30-60 seconds of screen time, ~half a page of screenplay) of that concept in 6 filmmaker modes:

1. **Kaufman mode** — Meta-narrative, subtext through mundane repetition, structural recontextualization
2. **Waititi mode** — Deadpan naturalism, comedy and emotion coexisting, ensemble energy
3. **Miyazaki mode** — Visual-first, environmental storytelling, dialogue economy, "ma" moments
4. **Pixar mode** — Clear emotional setup, character want/need gap, setup for payoff
5. **Burnham mode** — Layered meaning, direct address, comedy that hides something darker
6. **Fey/Glover mode** — High joke density, ensemble differentiation, social commentary underneath

**Your job:** Read all 6 and react honestly:
- Which one felt like "this is how I'd write this, but sharper"?
- Which one felt forced or like cosplay?
- Which specific LINES, SHOTS, or SCENE BEATS landed?
- Which mode surprised you (liked it more or less than expected)?

### Exercise 2: The Hybrid Scene

Based on your reactions, Claude Code writes a 7th version that blends the techniques you responded to — using your signature moves (hard cut, rule of three, humor-as-trojan-horse) alongside the filmmaker techniques.

**Your job:** React more carefully:
- Does this sound like YOUR screenplay voice, or an AI doing an impression?
- What would you change if you were rewriting this yourself?
- Which specific moments work and which fall flat?

### Exercise 3: Dialogue Polish Test

Take a flat dialogue exchange and punch it up in two different modes:
- **Mode A:** Waititi naturalism (mid-thought interruptions, trailing off, deadpan)
- **Mode B:** Fey density (joke-per-line, callback setup, rapid-fire)

This tests whether dialogue craft modes produce genuinely different-sounding characters.

### Exercise 4: The Tonal Pivot (optional, if energy allows)

Write a single scene that starts as pure comedy and pivots to genuine emotion. Test it using:
- **Approach A:** Waititi seam (comedy and emotion coexist from the start)
- **Approach B:** Burnham reveal (comedy IS the emotion, audience just doesn't know yet)
- **Approach C:** Pixar payoff (comedy sets up the emotional beat mechanically)

This tests Sean's preferred approach to the comedy-to-emotion turn in screenplay form.

---

## What Comes Out of Phase 3

By the end of this session, you should have:

1. **Interview notes** — Claude Code's understanding of Sean's screenwriting instincts and preferences
2. **6 mode samples** — Concrete screenplay examples of each filmmaker mode applied to Sean's concept
3. **Sean's reactions** — Which modes/techniques resonated and which didn't
4. **A hybrid scene** — The starting point for Sean's personal screenplay voice
5. **Dialogue samples** — Evidence of which dialogue modes sound like Sean
6. **Enough signal to upgrade the skill** — Phase 4 can happen in the same session or a follow-up

---

## Moving to Phase 4 (Skill Upgrade)

If you have energy left in the same session, say:

```
Based on the interview and writing exercises, upgrade the script-writing
SKILL.md now. Keep everything that's currently there (format reference,
beat sheets, production handoff). ADD craft depth sections:

- Filmmaker-influenced scene construction techniques
- Dialogue craft modes (calibrated to my voice)
- Tonal control mechanics
- Visual storytelling techniques for action lines
- My personal screenplay signature moves
- Anti-patterns (what makes each technique parody)

Model it after writing-voice-modes SKILL.md — that's the quality bar.
Include concrete examples from our exercises. Put it at
[path to script-writing/SKILL.md]
```

If you'd rather do it in a fresh session, save the session transcript and bring it into the next session as context.

---

## Time Estimate

| Phase | Time |
|-------|------|
| Setup + context loading | 2 min |
| Interview (8-10 questions) | 20-30 min |
| Exercise 1: Six-mode scene test | 15-20 min (reading + reacting) |
| Exercise 2: Hybrid scene | 10-15 min |
| Exercise 3: Dialogue polish test | 10-15 min |
| Exercise 4: Tonal pivot (optional) | 10-15 min |
| Phase 4: Skill upgrade (if same session) | 30-45 min |
| **Total** | **~90-120 min** |

---

## Quality Check Notes

### How each deliverable maps to its voice-modes equivalent:

| Deliverable | Voice-Modes Version | Script-Writing Version | Quality Match? |
|---|---|---|---|
| Perplexity Prompts | 4 prompts, 5 dimensions each | 6 prompts, 6 dimensions each (expanded for screenplay specificity) | ✅ Each prompt is at least as detailed as the voice-modes originals |
| NotebookLM System Prompts | 5 prompts: Prose Rhythm, Gonzo Rhetoric, Clarity/Compression, Observational Humor, Voice Architecture | 7 prompts: Structural Recursion, Tonal Seam, Visual Silence, Emotional Systems, Meta-Vulnerability, Comedy Architecture, Screenplay Craft Architect | ✅ Each role is specific to the filmmaker's signature craft dimension |
| Synthesis Prompts | 2: Voice Mechanics Profile + Cross-Author Comparison | 2: Screenplay Mechanics Profile + Cross-Filmmaker Synthesis | ✅ Adapted for screenplay elements (dialogue, scene construction, etc.) |
| Compilation Prompt | 1 prompt, ~4000 word target | 1 prompt, ~5000 word target (6 filmmakers vs. 4 authors, need headroom) | ✅ Same good/bad example calibration, same thinking filter |
| Session Guide | 8-10 questions + 3 exercises | 8-10 questions + 4 exercises (added dialogue polish and tonal pivot) | ✅ More exercises because screenplay has more dimensions than prose |

### Miyazaki dual-skill note:
The Miyazaki prompt and system prompt both explicitly note they feed BOTH `script-writing` AND `animation-pipeline`. The Visual Silence Analyst role covers screenplay craft (how to write visual storytelling) AND animation production principles (how to design visual sequences). When the animation-pipeline upgrade runs, Miyazaki research can be reused.

### Pixar as system, not films:
The Pixar prompt and system prompt consistently target the METHODOLOGY — brain trust, iterative rewriting, setup/payoff engineering, the "what if X had feelings" concept engine. Individual films are examples of the system, not the focus.

### Fey/Glover as pair:
Every dimension in the Fey/Glover prompt and system prompt compares and contrasts. The Comedy Architecture Analyst is instructed to NEVER analyze one writer alone for more than a paragraph.
