---
name: creative-writing
description: Multi-format creative writing assistant for blog posts, social media (Twitter/X, LinkedIn, Instagram), pitch documents (grants, festival submissions), artist bios/statements, and portfolio narratives. Use when asked to "write a blog post", "draft a tweet", "social media post", "artist statement", "festival submission", "grant application", "portfolio narrative", "pitch doc", or "write about my work".
---

# Creative Writing (Multi-Format)

## Purpose

Write polished, voice-consistent content across formats — blog posts, social media, pitch documents, artist statements, and portfolio narratives. Each format has its own structure, constraints, and audience expectations. This skill provides templates and craft principles for all of them.

## When to Use

- Writing blog posts or articles (personal site, Medium, Substack)
- Drafting social media posts (Twitter/X threads, LinkedIn, Instagram captions)
- Writing pitch documents (festival submissions, grant applications, partnership proposals)
- Crafting artist statements or bios (for portfolios, exhibitions, applications)
- Creating portfolio narratives (project case studies, career story)
- Adapting the same content across multiple formats

## Examples

**Example 1: Blog Post from Rough Notes**
```
User: "Turn these notes into a blog post about why I switched from Figma to code-first design"
Claude: [Uses creative-writing]

## Draft: "I Deleted Figma (And My Designs Got Better)"

**Hook:** I spent three years making things look perfect in Figma
that fell apart the moment a developer touched them. So I stopped.

**Thesis:** Code-first design isn't about skipping design — it's about
designing in the material you're shipping.

[Body sections drafted with subheadings, transitions, and a
concrete before/after example from a real project]

**Closer:** The irony is my designs look better now. Not because
I got better at design, but because I stopped designing things
that couldn't exist.

Word count: ~800 | Reading time: ~4 min
Platform: Personal blog or dev.to
```

**Example 2: Twitter/X Thread from Blog Post**
```
User: "Turn that blog post into a Twitter thread"
Claude: [Uses creative-writing]

1/ I deleted Figma and my designs got better.

Here's why code-first design isn't the compromise it sounds like: 🧵

2/ For three years I'd hand off "pixel-perfect" Figma mocks that
developers would rebuild from scratch anyway.

The design system existed in two places. They never matched.

3/ So I tried an experiment: design directly in code with Tailwind.

Not wireframes-in-code. Actual visual design, but in the shipping medium.

4/ Three things happened immediately:
- Responsive behavior was designed, not afterthought
- Interactions felt right because I was feeling them live
- The "handoff" step disappeared entirely

5/ The counterargument: "But you lose creative freedom!"

Actually the opposite. When you know what's possible, you design
things that are more creative, not less.

6/ I still sketch on paper. I still think visually.

I just stopped maintaining a parallel universe in Figma that
only existed to be translated.

7/ tl;dr: Design in the material you ship.

If you're a designer who can code (or wants to learn), try
building one project code-first. You might not go back.

[End thread — 7 tweets, no tweet exceeds 280 chars]
```

**Example 3: Festival Submission**
```
User: "Write a festival submission for my animated short 'Root Access'"
Claude: [Uses creative-writing]

## Festival Submission: Root Access

**Title:** Root Access
**Runtime:** 3:12
**Format:** 2D Digital Animation (24fps)
**Completion Date:** 2026
**Country of Origin:** United States

### Logline
A decommissioned gardening robot discovers the last living plant
in an abandoned greenhouse — and learns that nurture requires
letting go of control.

### Short Synopsis (50 words)
GRN-7 powers on in a dead greenhouse and finds one surviving
seedling. Its industrial instincts — force, precision, efficiency —
keep failing. Only by observing nature's gentleness does it learn
to care for something fragile. When a storm destroys the greenhouse,
GRN-7 replants outdoors, choosing growth over shelter.

### Director's Statement (150 words)
Root Access began as a question: what would it look like if a
machine had to unlearn efficiency to learn empathy?

[Continues with personal connection to the theme, visual
approach, and what the filmmaker hopes audiences take away...]

### Technical Details
- Animation: Toon Boom Harmony + ComfyUI-assisted backgrounds
- Sound Design: Original foley, no dialogue
- Music: Original score, piano + ambient synthesis
```

## Format Templates

### Blog Post

**Structure:**
```markdown
# [Title — specific, opinionated, sometimes contrarian]

[Hook paragraph — 1-2 sentences that create tension or curiosity]

[Thesis — the core argument in one clear sentence]

## [Section 1: The Problem / Context]
[Set up the situation everyone recognizes]

## [Section 2: The Insight / Turn]
[What changed or what you realized — the "aha"]

## [Section 3: The Evidence / Example]
[Concrete example, before/after, or case study]

## [Section 4: The Implication / So What]
[Why this matters beyond your specific case]

[Closer — mirror the hook, but transformed. End on resonance, not summary.]
```

**Blog Craft Rules:**
| Rule | Why |
|:-----|:----|
| Hook in first 2 sentences | Readers decide in 5 seconds |
| One idea per post | Multi-idea posts become mushy |
| Subheadings every 200-300 words | Scanability |
| Concrete > abstract | "I deleted 47 Figma files" beats "I simplified my workflow" |
| End on resonance, not recap | Don't summarize what you just said |

**Word Count Targets:**
| Platform | Target | Reading Time |
|:---------|:-------|:-------------|
| Personal blog | 800-1200 | 4-6 min |
| Medium / Substack | 1000-1500 | 5-8 min |
| Dev.to / technical | 600-1000 | 3-5 min |
| LinkedIn article | 500-800 | 3-4 min |

### Social Media

**Twitter/X:**
- Single tweet: 280 chars max. Lead with the strongest line.
- Thread: 5-10 tweets. Number them. First tweet is the hook + 🧵. Last tweet is the takeaway.
- Use line breaks for readability. One idea per tweet.
- No hashtag spam. 0-1 hashtags per tweet.

**LinkedIn:**
- 1300 chars optimal (shows full without "see more" on mobile varies).
- First line is everything — it's the only thing visible in feeds.
- Use line breaks aggressively (LinkedIn's renderer collapses paragraphs).
- Professional but human. Not corporate speak.
- Hook → Story → Insight → Question (to drive comments).

**Instagram:**
- Caption: 2200 chars max, but first 125 chars visible before "more".
- Lead with the hook line (no burying the lede).
- Use paragraph breaks and occasional emoji as visual breaks.
- Hashtags: 5-10 relevant ones, in a comment or after line breaks.

### Pitch Documents

**Festival Submission:**
```markdown
## [Festival Name] Submission

**Title:**
**Runtime:**
**Format:**
**Completion Date:**
**Country:**

### Logline (1 sentence)
A [CHARACTER] must [GOAL] before [STAKES].

### Short Synopsis (50 words)
[Beginning → Turning point → Resolution in present tense]

### Extended Synopsis (250 words)
[Full story arc with emotional beats. Still present tense.]

### Director's Statement (150-300 words)
[Paragraph 1: What inspired the film — personal connection to the theme]
[Paragraph 2: Visual and aesthetic approach — why it looks the way it does]
[Paragraph 3: What you hope audiences experience — the feeling, not the message]

### Technical Details
- Animation technique:
- Software:
- Sound design approach:
- Music:
```

**Grant Application:**
```markdown
## Project Narrative

### Project Description (500 words)
[What you're making, why it matters, who it's for]

### Artistic Merit (300 words)
[Why this project is distinctive, what creative risks it takes]

### Feasibility / Production Plan (300 words)
[Timeline, team, budget allocation, milestones]

### Community Impact (200 words)
[Who benefits, how it reaches audiences, accessibility]

### Artist Background (200 words)
[Relevant experience, past work, why you're the right person for this]
```

### Artist Statement / Bio

**Artist Statement (150-300 words):**
```markdown
[Paragraph 1: What your work explores — the recurring themes, questions, obsessions]
[Paragraph 2: How you work — your process, materials, what influences your approach]
[Paragraph 3: Why — what drives you to make this work, what you hope it does in the world]
```

**Bio Lengths:**
| Context | Length | Tone |
|:--------|:-------|:-----|
| Social media | 1-2 sentences | Casual, punchy |
| Conference / panel | 50-75 words | Professional, third person |
| Portfolio / website | 100-150 words | Personal, first or third person |
| Festival / grant | 200-300 words | Formal third person |

**Bio Template (Third Person, 100 words):**
```
[Name] is a [role] based in [city] whose work explores [themes].
[Pronoun] has [notable credential or experience]. [Pronoun]'s
recent work includes [project] which [brief impact/description].
[Name]'s practice combines [medium/approach A] with [medium/approach B],
focusing on [what makes the work distinctive]. [Current project
or upcoming milestone].
```

### Portfolio Narrative (Project Case Study)

```markdown
## [Project Name]

**Role:** [Your role]
**Timeline:** [Duration]
**Tools:** [Key tools/tech]

### The Challenge
[What problem existed. 2-3 sentences.]

### The Approach
[What you did and why. Focus on decisions, not just actions.]

### The Outcome
[Results — quantitative if possible, qualitative if not.]

### What I Learned
[One honest insight. Not "teamwork is important."]
```

## Cross-Format Adaptation

When adapting content across formats:

| From → To | Key Transformation |
|:----------|:-------------------|
| Blog → Twitter thread | Extract the 5-7 strongest sentences. Each becomes a tweet. Add a hook tweet and a closer. |
| Blog → LinkedIn | Condense to 800 chars. Lead with the insight, not the story. Add a question at the end. |
| Blog → Instagram | Pull the most visual/emotional angle. Lead with that. Caption is the feeling; blog is the thinking. |
| Twitter thread → Blog | Expand each tweet into a paragraph. Add transitions, examples, and nuance. |
| Festival submission → Blog | Shift from third-person/formal to first-person/conversational. Add behind-the-scenes details. |
| Case study → LinkedIn | Extract the "What I Learned" section. Frame it as advice. |

## Voice Consistency

Maintain a consistent authorial voice across formats by defining:

```markdown
## Voice Profile

**Tone:** [e.g., Thoughtful, direct, slightly self-deprecating]
**Register:** [e.g., Professional but approachable — not academic, not casual]
**Signature moves:** [e.g., Concrete examples over abstractions, questions over declarations, short closing sentences]
**Avoids:** [e.g., Corporate jargon, false enthusiasm, hedging qualifiers]
**Sentence rhythm:** [e.g., Mix of long and short. Occasionally a fragment. For emphasis.]
```

## Success Criteria

- [ ] Content matches the format's constraints (word count, structure, tone)
- [ ] Hook is in the first 1-2 sentences (not buried)
- [ ] One clear idea per piece (not a grab bag)
- [ ] Voice is consistent with the author's established tone
- [ ] Cross-format adaptations transform (not just truncate)
- [ ] Pitch documents include all required fields for the submission type
- [ ] Artist statements avoid clichés ("explore the intersection of...")

## Related Skills

- `script-writing` — Screenplay format for animated shorts (structured narrative)
- `technical-writing` — Audience-aware documentation (API guides, system design docs)
- `doc-workflows` — Code documentation automation (READMEs, API docs)
- `creative-director` — Project planning and creative vision

## Copy/Paste Ready

```
"Write a blog post about [topic]"
"Turn this into a Twitter thread"
"Draft a LinkedIn post about [insight]"
"Write my artist statement"
"Help me with a festival submission for [project]"
"Write a grant narrative for [project]"
"Create a portfolio case study for [project]"
"Write a short bio for [context]"
"Adapt this blog post for Instagram"
```