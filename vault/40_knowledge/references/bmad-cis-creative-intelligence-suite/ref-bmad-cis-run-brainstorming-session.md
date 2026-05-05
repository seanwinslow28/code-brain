---
title: "Run a Brainstorming Session"
source: "https://cis-docs.bmad-method.org/how-to/brainstorm/"
author:
published:
created: 2026-05-04
description: "Use the brainstorming workflow to generate diverse ideas with Carson"
tags:
  - "source/web-clip"
  - "bmad-cis"
type: "reference"
status: processed
domain: [creative-studio]
ai-context: "How-to guide for the CIS `brainstorming` workflow — generate diverse ideas with Carson using 36 techniques across 7 categories, with use/skip criteria."
---
Use the `brainstorming` workflow to generate diverse, creative ideas using 36 proven techniques across 7 categories.

## When to Use This

- Starting a new project and need options
- Stuck on a problem and want fresh perspectives
- Exploring solutions before committing to a direction
- Building a pipeline of ideas for future consideration
- Facilitating team ideation sessions

## When to Skip This

- You already have a clear, single solution path
- Time is extremely constrained (under 10 minutes)
- The problem requires analytical rather than creative approaches

## Steps

### 1\. Load Carson

Start a fresh chat and load the Brainstorming Coach:

```plaintext
/cis-brainstorm
```

### 2\. Define Your Topic

Carson will ask what you want to brainstorm about. Provide a clear but open-ended topic:

**Good topics:**

- “Ways to improve user onboarding”
- “New features for a budgeting app”
- “Revenue streams for a content platform”

**Less effective:**

- “Fix the bug in line 42” (too specific)
- “Should I use React or Vue?” (decision-making, not ideation)

### 3\. Choose Your Approach

Carson offers four ways to select brainstorming techniques:

| Mode | Best For | Description |
| --- | --- | --- |
| **User-selected** | You know which technique you want | Browse 36 techniques and pick one |
| **AI-recommended** | You’re unsure what would work best | Carson analyzes your topic and recommends |
| **Random** | Serendipity and surprise | Let fate choose a technique |
| **Progressive** | Comprehensive exploration | Try multiple techniques in sequence |

### 4\. Explore with the Technique

Carson guides you through the chosen technique using “Yes, and…” methodology:

- **Build on ideas** — Don’t judge, add to what’s emerging
- **Go for quantity** — More ideas increase quality odds
- **Embrace wildness** — Crazy ideas often contain gems

### 5\. Capture and Refine

After ideation, Carson helps you:

1. **Cluster similar ideas** — Find themes and patterns
2. **Identify standouts** — Mark ideas worth pursuing
3. **Add practical details** — Make actionable ideas more concrete

## What You Get

Output saved to `_bmad-output/brainstorming-{date}.md`:

| Section | Contents |
| --- | --- |
| **Topic** | Your brainstorming challenge |
| **Technique Used** | Which method was applied |
| **Ideas Generated** | Full list of all ideas |
| **Top Picks** | Carson’s recommendations |
| **Next Steps** | How to move forward |

## Example

```text
You: /cis-brainstorm
Carson: What would you like to brainstorm about?
You: Ways to reduce cart abandonment
Carson: Love it! Let's use Reverse Brainstorming.
       Instead of "how to reduce abandonment," let's ask:
       "How could we MAXIMIZE abandonment?"
You: [Generate reverse ideas]
Carson: Great! Now let's flip these:
       - "Make checkout confusing" → "Simplify to 3 clicks"
       - "Hide shipping costs" → "Show total upfront"
       [Generates actionable solutions from reverse angles]
```

## Tips

## Next Steps

After brainstorming:

- Use **design thinking** (`/cis-design-thinking`) to test ideas with users
- Apply **innovation strategy** (`/cis-innovation-strategy`) to evaluate business potential
- Run **problem-solving** (`/cis-problem-solving`) if you need to diagnose why solutions aren’t working

## Available Techniques

Carson’s 36 techniques span 7 categories:

| Category | Techniques Include |
| --- | --- |
| **Collaborative** | Brainwriting, Round Robin, Six Thinking Hats |
| **Structured** | SCAMPER, Reverse Brainstorming, Morphological Analysis |
| **Creative** | Metaphors, Random Word, Forced Connections |
| **Deep** | Five Whys, Laddering, Assumption Surfacing |
| **Theatrical** | Role Storming, Hero’s Journey, Future Press |
| **Wild** | Worst Possible Idea, Anti-Problems, Exaggeration |
| **Introspective** | Guided Imagery, Incubation, Dream Capture |

---
*Clipped from [bmad-method.org](https://cis-docs.bmad-method.org/how-to/brainstorm/) on 2026-05-04T06:19:52-04:00*
