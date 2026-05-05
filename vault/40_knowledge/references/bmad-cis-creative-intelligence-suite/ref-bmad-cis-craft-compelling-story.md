---
title: "Craft a Compelling Story"
source: "https://cis-docs.bmad-method.org/how-to/storytelling/"
author:
published:
created: 2026-05-04
description: "Use the storytelling workflow to create narratives that persuade and inspire"
tags:
  - "source/web-clip"
  - "bmad-cis"
type: "reference"
status: processed
domain: [creative-studio]
ai-context: "How-to guide for the CIS `storytelling` workflow — narrative crafting via proven story frameworks for product/brand stories, pitch decks, user stories, change communication, and marketing content."
---
Use the `storytelling` workflow to craft compelling narratives using proven story frameworks, emotional psychology, and platform-specific adaptation.

## When to Use This

- Creating product or brand narratives
- Writing pitch decks or investor presentations
- Developing user stories or case studies
- Communicating change or vision
- Crafting marketing content or campaigns

## When to Skip This

- Purely technical documentation
- Simple factual reporting without narrative need
- Extremely short formats (headlines, taglines)

## Steps

### 1\. Load Sophia

Start a fresh chat and load the Storyteller:

```plaintext
/cis-storytelling
```

### 2\. Define Your Story Purpose

Sophia will ask about your story. Be clear about intent:

**Good story purposes:**

- “Persuade investors that our market opportunity is massive”
- “Inspire employees to embrace a new direction”
- “Help users understand how our product changes their life”
- “Explain a complex technical concept in relatable terms”

**Less effective:**

- “Write about our product” (no clear purpose)
- “Tell our company story” (too vague)

### 3\. Understand Your Audience

Sophia explores who you’re speaking with:

| Audience Question | Why It Matters |
| --- | --- |
| **Who are they?** | Shapes language, tone, references |
| **What do they believe now?** | Identifies gap to bridge |
| **What do you want them to feel?** | Emotional journey design |
| **What should they do?** | Call to action clarity |

### 4\. Choose Your Framework

Sophia selects from 25 story frameworks:

| Framework | Best For |
| --- | --- |
| **Hero’s Journey** | Transformation, overcoming obstacles |
| **StoryBrand** | Customer-centric marketing |
| **Three-Act Structure** | Classic narrative arcs |
| **Before-After-Bridge** | Simple problem-solution stories |
| **The Pixar Pitch** | Emotional, character-driven narratives |
| **Inverted Pyramid** | News-style, impact-first |

### 5\. Craft Your Narrative

Sophia guides you through:

| Story Element | What You’ll Create |
| --- | --- |
| **Hook** | Opening that grabs attention |
| **Characters** | Relatable protagonists and antagonists |
| **Conflict** | The problem or tension |
| **Journey** | The path through struggle |
| **Resolution** | The satisfying outcome |
| **Transformation** | How the world changed |

### 6\. Adapt to Platform

Sophia tailors the story for where it will live:

- **Pitch deck** — Concise, slide-by-slide narrative
- **Blog post** — Scannable, with narrative arc
- **Video script** — Visual storytelling with dialogue
- **Social media** — Micro-narratives for feed format
- **Email** — Personal, direct storytelling

## What You Get

Output saved to `_bmad-output/story-{date}.md`:

| Section | Contents |
| --- | --- |
| **Story Framework** | Which structure was used and why |
| **Audience Profile** | Who the story is for |
| **Emotional Arc** | The journey you want them to feel |
| **Complete Narrative** | Full story with vivid details |
| **Character Development** | Voice, motivation, transformation |
| **Platform Adaptation** | Formatted for your chosen medium |
| **Impact Plan** | How to measure effectiveness |

## Example

```text
You: /cis-storytelling
Sophia: 📖 Greetings, traveler. What tale shall we weave?
You: We need to tell our product story for a pitch deck.
     Our app helps people manage anxiety.
Sophia: Ah, a noble quest. Tell me—who suffers from
       this anxiety, and how does your solution become
       the hero they've been waiting for?
You: [Explains user struggle and solution]
Sophia: [Selects Hero's Journey framework]
       Let us craft your protagonist—someone whose
       anxiety keeps them from living fully.
       [Develops character and emotional stakes]
       [Creates narrative arc with tension and release]
       [Adapts story for pitch deck format—slide by slide]
```

## Tips

## Next Steps

After storytelling:

- Use **presentation design** (coming soon) to create visual decks
- Apply **innovation strategy** (`/cis-innovation-strategy`) to strengthen business narrative
- Use **brainstorming** (`/cis-brainstorm`) to generate story variations

## Providing Context

For best results, provide brand or product context via the `--data` flag:

```bash
workflow cis-storytelling --data /path/to/brand-guidelines.md
```

Sophia will use this context to maintain brand voice and consistency.

---
*Clipped from [bmad-method.org](https://cis-docs.bmad-method.org/how-to/storytelling/) on 2026-05-04T06:21:31-04:00*
