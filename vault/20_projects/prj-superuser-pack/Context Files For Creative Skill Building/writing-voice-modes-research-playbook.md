# Writing Voice Modes — Research Playbook

## Overview

**Goal:** Research 4 authors' writing techniques → synthesize into a Voice Mechanics doc → build a `writing-voice-modes` skill that integrates with existing creative-writing and technical-writing skills.

**Authors:** Jack Kerouac, Hunter S. Thompson, Kurt Vonnegut, David Sedaris

**Tools:** Perplexity Deep Research (broad technique analysis) → NotebookLM (source synthesis) → Claude Code (interview + skill creation)

---

## Phase 1A: Perplexity Deep Research (Run First)

Perplexity excels at synthesizing across many sources quickly. Use it to generate the initial technique profiles that you'll then deepen with primary sources in NotebookLM.

### Prompt 1: Jack Kerouac — Technique Analysis

```
I'm building a writing voice system that applies literary techniques to modern
technical and creative content (blog posts, social media, technical docs).

Analyze Jack Kerouac's writing craft with extreme specificity. I need
ACTIONABLE TECHNIQUE PATTERNS, not biographical summary.

Cover these dimensions:

1. SENTENCE MECHANICS
   - Average sentence length and variation patterns
   - How he uses punctuation (especially dashes, commas, "and")
   - His rhythm patterns — where does he accelerate and decelerate?
   - Specific examples of his "spontaneous prose" technique in practice

2. STRUCTURAL PATTERNS
   - How does he open pieces? What's his first-paragraph signature?
   - How does he transition between scenes or ideas?
   - How does he build momentum across a longer piece?
   - What role does repetition play in his structure?

3. VOICE AND POV
   - First person vs third person usage patterns
   - How does he handle interiority (thoughts, feelings)?
   - His relationship to the reader — does he address them? Ignore them?
   - How personal/confessional does he get and what's the technique?

4. SPECIFIC TRANSFERABLE TECHNIQUES
   - What techniques from Kerouac could be applied to writing about
     technology, AI, or creative workflows without feeling like parody?
   - How would "spontaneous prose" translate to blog writing?
   - What's the difference between Kerouac's stream-of-consciousness
     and just rambling?

5. KEY WORKS TO STUDY
   - Which specific passages (cite the book and chapter/section) best
     demonstrate each technique?
   - Any interviews or essays where Kerouac explains his own process?

Include direct examples from his work where possible. I want to understand
the MECHANICS, not just the vibes.
```

### Prompt 2: Hunter S. Thompson — Technique Analysis

```
I'm building a writing voice system that applies literary techniques to modern
technical and creative content (blog posts, social media, technical docs).

Analyze Hunter S. Thompson's "Gonzo journalism" craft with extreme specificity.
I need ACTIONABLE TECHNIQUE PATTERNS, not biographical summary.

Cover these dimensions:

1. SENTENCE MECHANICS
   - His sentence length variation — when does he go long vs. short?
   - How does he use profanity and exaggeration as rhetorical tools
     (not just shock value)?
   - His use of ALL CAPS, italics, ellipses — when and why?
   - How does his dialogue attribution work?

2. STRUCTURAL PATTERNS
   - The "Gonzo" structure: how does he weave personal narrative
     into reporting/analysis?
   - How does he handle cold opens? (He often starts mid-action)
   - His escalation pattern — how does chaos build across a piece?
   - How does he handle factual information within the wild narrative?
   - When/how does he break the fourth wall?

3. VOICE AND STANCE
   - How does he position himself as simultaneously participant AND
     observer AND critic?
   - His humor mechanics — what makes Thompson funny vs. just unhinged?
   - How does he earn the reader's trust despite obvious exaggeration?
   - The interplay between rage and precision in his prose

4. SPECIFIC TRANSFERABLE TECHNIQUES
   - How would "Gonzo" translate to writing about AI tools, coding
     workflows, or productivity software?
   - What's the line between "Gonzo tech writing" and just being
     unprofessional?
   - Which Thompson techniques work in SHORT form (social media,
     blog posts) vs. requiring long form?

5. KEY WORKS TO STUDY
   - Which specific passages best demonstrate each technique?
   - His letters and correspondence — any craft insights there?
   - The difference between early Thompson (Hell's Angels) and
     peak Gonzo (Fear and Loathing) in terms of technique evolution

Include direct examples from his work where possible.
```

### Prompt 3: Kurt Vonnegut — Technique Analysis

```
I'm building a writing voice system that applies literary techniques to modern
technical and creative content (blog posts, social media, technical docs).

Analyze Kurt Vonnegut's writing craft with extreme specificity. I need
ACTIONABLE TECHNIQUE PATTERNS, not biographical summary.

Cover these dimensions:

1. SENTENCE MECHANICS
   - His famous short-sentence style — what's the actual average
     length and how does he vary it?
   - How he uses repetition as a structural device ("So it goes,"
     "And so on," "Hi ho")
   - His parenthetical asides — when and why?
   - The rhythm of Vonnegut prose — how does humor emerge from rhythm?

2. STRUCTURAL PATTERNS
   - His chapter/section length (often very short) — why does this work?
   - How he embeds philosophy within narrative without being preachy
   - His use of diagrams, illustrations, and non-text elements
   - The "Vonnegut story shape" — how he structures narrative arcs
   - How he handles time jumps and non-linear narrative

3. VOICE AND TONE
   - The mechanics of "dark humor" in his writing — what's the formula?
   - How does he maintain warmth while being deeply cynical?
   - His direct-address style ("Listen:" etc.)
   - Ironic understatement — when does he deploy it and how?
   - How he makes complex ideas feel simple without being simplistic

4. SPECIFIC TRANSFERABLE TECHNIQUES
   - How would Vonnegut write about AI and machine learning?
   - His ability to explain complex systems simply — technique breakdown
   - Which techniques work for blog posts about technology?
   - How would his dark humor translate to writing about automation,
     job displacement, or the absurdity of productivity culture?
   - "So it goes" as a structural device — what's the general pattern
     you could adapt?

5. KEY WORKS TO STUDY
   - Which passages best demonstrate each technique?
   - His "8 Rules for Writing" — how do they manifest in his own work?
   - His nonfiction essays (Palm Sunday, Wampeters Foma & Granfalloons)
     — different techniques than his fiction?
   - His speeches, especially commencement addresses

Include direct examples from his work where possible.
```

### Prompt 4: David Sedaris — Technique Analysis

```
I'm building a writing voice system that applies literary techniques to modern
technical and creative content (blog posts, social media, technical docs).

Analyze David Sedaris's writing craft with extreme specificity. I need
ACTIONABLE TECHNIQUE PATTERNS, not biographical summary.

Cover these dimensions:

1. SENTENCE MECHANICS
   - His sentence construction — how does he set up and deliver
     humor within a single sentence?
   - Comma usage and pacing — how does punctuation create comic timing?
   - How he handles dialogue (his transcription style is distinctive)
   - The balance between observation and commentary within a paragraph

2. STRUCTURAL PATTERNS
   - His essay structure — how does a typical Sedaris piece open,
     develop, and close?
   - How long are his sections? How does he transition?
   - The "mundane setup → unexpected pivot" pattern — how does he
     build to the turn?
   - How he structures pieces that are funny but also emotionally
     devastating by the end

3. VOICE AND SELF-PRESENTATION
   - The mechanics of self-deprecation as a literary device
   - How he makes himself the fool without losing the reader's respect
   - His observational technique — what details does he notice and
     select for inclusion?
   - How he handles other people in his essays (family, strangers)
     without being cruel
   - The balance between vulnerability and performance

4. HUMOR MECHANICS (Deep Dive)
   - Types of humor he uses: observational, self-deprecating,
     absurdist, deadpan — when does he deploy each?
   - His setup-punchline rhythm — is it predictable or varied?
   - How does he earn emotional depth THROUGH humor rather than
     despite it?
   - The role of specificity in his humor (exact brands, exact
     numbers, exact quotes)

5. SPECIFIC TRANSFERABLE TECHNIQUES
   - How would Sedaris write about his daily routine with AI tools?
   - His technique of finding the universal in the specific — how
     does that apply to tech writing?
   - Which techniques work in short form (social media, newsletters)?
   - How would his observational style translate to writing about
     the absurdity of modern technology and AI relationships?

6. KEY WORKS TO STUDY
   - Which specific essays best demonstrate each technique?
   - His diary entries (Theft by Finding) — different craft than
     polished essays?
   - Audio performances — does hearing him read reveal technique
     that's invisible on the page?
   - His New Yorker pieces vs. book collections — any differences?

Include direct examples from his work where possible.
```

---

## Phase 1B: NotebookLM Notebooks (Build After Perplexity)

Create **one notebook per author**. Feed each notebook with the Perplexity research output PLUS primary sources.

### Sources to Add Per Notebook

**All Authors:**
- The Perplexity Deep Research output (paste as a text source)
- Paris Review interview (if available — Kerouac and Vonnegut have them)
- 2-3 passages YOU personally love from their work (type or paste key excerpts)

**Kerouac Notebook — Additional Sources:**
- "Essentials of Spontaneous Prose" (short essay, widely available online)
- "Belief & Technique for Modern Prose" (his 30-point list)
- Excerpts from *On the Road* (opening pages + the "mad ones" passage)
- Excerpts from *The Dharma Bums* (more controlled than On the Road — useful contrast)
- Any literary criticism that breaks down his sentence rhythm patterns

**Thompson Notebook — Additional Sources:**
- "The Kentucky Derby Is Decadent and Depraved" (the birth of Gonzo — essential)
- Opening of *Fear and Loathing in Las Vegas* (the most analyzed Gonzo passage)
- His letters (collected in *The Proud Highway* and *Fear and Loathing in America*)
- Any craft analysis of Gonzo journalism as a technique vs. a lifestyle
- His ESPN columns (late-career, shorter form — useful for blog-length adaptation)

**Vonnegut Notebook — Additional Sources:**
- "Here Is a Lesson in Creative Writing" (from *A Man Without a Country*)
- His "8 Rules for Writing" (widely cited — find the original context)
- Opening pages of *Slaughterhouse-Five* and *Cat's Cradle*
- His shape-of-stories lecture (there are video transcripts)
- *Palm Sunday* essays (his nonfiction voice, distinct from fiction)
- Commencement speeches (his most direct-to-audience voice)

**Sedaris Notebook — Additional Sources:**
- "SantaLand Diaries" (the piece that launched his career — study the structure)
- "Now We Are Five" or "Ashes" (pieces that start funny and become emotionally deep)
- Excerpts from *Theft by Finding* (diary voice vs. polished essay voice)
- Interviews where he discusses his revision process (he road-tests material live)
- "The Learning Curve" or another teaching-themed essay (closest to "explaining things" mode)

### NotebookLM Synthesis Prompts

After loading sources into each notebook, use these prompts to generate synthesis:

**For Each Author (adapt the name):**

```
Based on all the sources in this notebook, create a "Voice Mechanics Profile"
for [AUTHOR NAME] organized into these sections:

1. SENTENCE-LEVEL PATTERNS
   - Typical sentence length range
   - Punctuation signatures
   - Rhythm patterns (when they speed up vs. slow down)
   - 3 example sentences that perfectly demonstrate their style

2. STRUCTURAL SIGNATURES
   - How they typically open a piece
   - How they build through the middle
   - How they close/land
   - Average section/paragraph length

3. HUMOR MECHANICS (if applicable)
   - Primary humor type (observational, absurdist, dark irony, self-deprecating)
   - Setup-to-payoff rhythm
   - What makes the humor work (specificity? understatement? escalation?)

4. VOICE MARKERS
   - 5 phrases or constructions that are unmistakably this author
   - POV preferences and reader relationship
   - What they NEVER do (anti-patterns)

5. TRANSFERABLE TECHNIQUES FOR TECH/AI WRITING
   - 3-5 specific techniques that could apply to blog posts about
     technology, AI tools, creative workflows, or productivity
   - For each: the technique name, how the author uses it, and how
     it would translate to tech content
   - Example: "What would this author's opening paragraph look like
     if they were writing about using Claude Code for the first time?"

Keep this practical and specific. I want to be able to hand this to a
writing tool and have it produce content in this author's mode.
```

**Cross-Notebook Comparison (do this after all 4 are built):**

Create a 5th notebook that contains the 4 Voice Mechanics Profiles, then prompt:

```
Compare these 4 voice mechanics profiles and identify:

1. COMPLEMENTARY TECHNIQUES — where do these authors' strengths
   cover different needs? (e.g., Vonnegut for explaining complex ideas,
   Thompson for making mundane things exciting)

2. CONFLICTING TECHNIQUES — where do their approaches directly
   contradict? (e.g., sentence length preferences)

3. HYBRID OPPORTUNITIES — which combinations of techniques from
   different authors create something new?

4. MAPPING TO CONTENT TYPES
   - Blog posts: which author's techniques fit best? Which 2 combine well?
   - Social media: which techniques work in short form?
   - Technical documentation: which techniques add personality without
     sacrificing clarity?
   - Personal essays: which techniques create emotional depth?
   - Festival/pitch writing: which techniques create authority and voice?

5. THE WRITER'S PERSONAL VOICE
   - If someone wanted to develop their OWN voice by borrowing from
     all 4, what would the "core kit" of techniques be?
   - What's the minimum set of techniques from each author that
     captures their essence without becoming parody?
```

---

## Phase 2: Voice Mechanics Document

After Perplexity research + NotebookLM synthesis, compile everything into a single reference doc.

**Filename:** `voice-mechanics-research.md`
**Location:** Save to your vault at `vault/40_knowledge/references/ref-voice-mechanics-research.md`

### Structure

```markdown
---
type: reference
domain:
  - creative-studio
status: active
ai-context: "Writing voice mechanics profiles for Kerouac, Thompson, Vonnegut, and Sedaris with transferable techniques for tech/creative content."
created: 2026-XX-XX
---

# Voice Mechanics Research

## Kerouac: The Beat Flow Mode
[Compiled from Perplexity + NotebookLM]

### Sentence Mechanics
### Structural Signatures
### Transferable Techniques
### Anti-Patterns (what to avoid so it doesn't become parody)

## Thompson: The Gonzo Mode
[Same structure]

## Vonnegut: The Minimalist Absurdist Mode
[Same structure]

## Sedaris: The Domestic Observer Mode
[Same structure]

## Cross-Author Analysis
### Complementary Techniques
### Hybrid Combinations
### Content Type Mapping
```

---

## Phase 3: Claude Code Interview + Writing Session

With the Voice Mechanics doc loaded, start a Claude Code session:

### Interview Prompts

```
Load vault/40_knowledge/references/ref-voice-mechanics-research.md

I want to develop my personal writing voice by borrowing techniques
from 4 authors. Before we build the skill, interview me:

1. Which passages from each author resonate most with how I naturally
   think and write?
2. When I write casually (Slack messages, quick notes), which of these
   authors' patterns show up unconsciously?
3. What topics do I want to write about, and which voice modes
   feel right for which topics?
4. Are there techniques from any of these authors that feel wrong
   for my voice — things I admire but wouldn't use?
```

### Writing Exercises

```
Now let's test. Take this topic: [pick a real blog post idea you have]

Draft the opening paragraph in each of the 4 voice modes:
- Beat Flow (Kerouac techniques)
- Gonzo Technical (Thompson techniques)
- Minimalist Absurdist (Vonnegut techniques)
- Domestic Observer (Sedaris techniques)

Then draft a 5th version that combines the techniques that felt
most natural from each. That hybrid is the starting point for my voice.
```

---

## Phase 4: Build the Skill

### Option A: Extend Existing Skills

Add a "Voice Modes" section to both `creative-writing` and `technical-writing` SKILL.md files. Each mode would include:

- Mode name and description
- 3-5 key techniques (from the research)
- Example opening paragraph
- When to use this mode (content type mapping)
- Anti-patterns (what makes it parody vs. authentic)

**Pro:** No new skill to maintain. Voice modes are contextual options within existing workflows.
**Con:** Makes both skills longer. Voice modes might get lost in the larger skill.

### Option B: Standalone `writing-voice-modes` Skill

A dedicated skill that creative-writing and technical-writing can reference.

**Pro:** Clean separation. Can be loaded independently. Easy to iterate on.
**Con:** One more skill to maintain (you're at 106 already).

### Recommendation: Option B (Standalone)

Your existing writing skills handle *format* (blog post structure, tweet constraints, API doc templates). The voice modes skill handles *how it sounds*. These are orthogonal concerns — a blog post can be Gonzo Technical OR Minimalist Absurdist, and the format rules still apply.

The skill would be invoked alongside the format skill:
```
"Write a blog post about my ComfyUI workflow — use the Gonzo Technical voice mode"
→ creative-writing (format) + writing-voice-modes (voice)
```

---

## Estimated Timeline

| Phase | Time | Output |
|-------|------|--------|
| 1A: Perplexity Research | ~2 hours (4 prompts, review output) | 4 technique analysis docs |
| 1B: NotebookLM Notebooks | ~3 hours (source gathering + synthesis) | 4 voice profiles + 1 cross-analysis |
| 2: Voice Mechanics Doc | ~1 hour (compile + edit) | ref-voice-mechanics-research.md |
| 3: Interview + Writing | ~1-2 hours (Claude Code session) | Personal voice calibration |
| 4: Skill Creation | ~1-2 hours (Claude Code session) | writing-voice-modes SKILL.md |
| **Total** | **~8-10 hours across 2-3 sessions** | **Production-ready skill** |

---

## Notes

- **Don't rush Phase 1.** The quality of the final skill depends entirely on how specific and actionable the technique research is. "Kerouac writes long sentences" is useless. "Kerouac averages 40-60 word sentences connected by dashes and 'and,' with a rhythm that accelerates through a list of concrete images before landing on an emotional beat" is useful.

- **The interview matters.** Without Phase 3, you get a generic "write like famous authors" tool. With it, you get a tool calibrated to YOUR voice that borrows selectively.

- **Start with one voice mode.** When you build the skill, pick the mode you're most excited to use and get it right first. Then add the others. Shipping one great mode beats shipping four mediocre ones.
