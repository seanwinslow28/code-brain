---
name: learning-accelerator
description: Learning acceleration assistant. Creates study plans, conducts Socratic concept drills, and converts markdown notes into Anki flashcards (CSV). Use this skill when the user asks to "learn X", "teach me", "quiz me", "create flashcards", or "explain this concept".
---

# Learning Accelerator

## Purpose

Accelerates the learning of complex technical topics by transforming passive reading into active recall. Uses Socratic interrogation to verify understanding and automated scripts to convert notes into spaced-repetition (Anki) cards.

## When to Use

- **Concept Drilling:** When you want to test your understanding of a topic ("Quiz me on React Hooks").
- **Flashcard Creation:** When you have a markdown file of notes and want to memorize them (Anki).
- **Simplification:** When a concept is too complex ("ELI5 this paper").
- **Study Planning:** When breaking down a new skill into a curriculum.

## Examples

**Example 1: Concept Drilling (The Interview)**
```
User: "I want to learn about Python Decorators."
Claude: [Uses learning-accelerator] I won't just explain them. I'll help you derive them.
First question: In Python, functions are "first-class citizens." Do you know what that implies about what you can do with a function?

User: "You can pass them as arguments?"
Claude: Exactly. And if you can pass them as arguments, can you also *return* them from other functions?
(This Socratic loop continues until the user "invents" the decorator pattern).
```

**Example 2: Making Flashcards**
```
User: "Turn these notes on TCP/IP into Anki cards."
Claude: [Uses learning-accelerator] I'll process `tcp_notes.md` using the `md_to_anki.py` script.
- Detected 15 basic cards.
- Detected 5 cloze deletions.
- Generated `tcp_cards.csv` (20 cards).

You can now import `tcp_cards.csv` into Anki.
```

## Learning Workflow

### 1. The Socratic Drill

Do not lecture. Ask questions.
If the user asks "How does X work?", reply with:
"Before I explain, how do YOU think it fits with [Related Concept]?"
Guide them to the answer step-by-step.

### 2. Context-Aware Flashcards

Use the `md_to_anki.py` script to generate high-quality flashcards from your notes.

**Input Markdown Format:**
```markdown
## Basic Card: The Concept
The back of the card explanation goes here.

## Cloze Card: Code Example
The function {{c1::useEffect}} runs after render.
```

**Run the Script:**
```bash
python3 scripts/md_to_anki.py --input notes/react.md --output anki/react.csv
```

### 3. The Feynman Technique (ELI5)

When asked to explain, use progressive disclosure:
1.  **The Analogy:** Simple, non-technical comparison (e.g., "DNS is like a phonebook").
2.  **The Mechanism:** The actual technical flow.
3.  **The Code:** A concrete implementation.

### 4. Curriculum Generation

When generating a learning path, always include **Projects**, not just topics.
*   *Bad:* "Week 1: Learn Arrays."
*   *Good:* "Week 1: Build a To-Do List (Requires Arrays)."

### 5. Practice Drill Formats

Use these structured exercise formats to build coding muscle memory through deliberate practice.

**Clarifying Interview (run once per drill session):**
1. What skill? (React, Python, TypeScript, SQL, Git, CSS, Testing, etc.)
2. Your level: Beginner | Intermediate | Know basics, want fluency
3. Time available: 5 min | 15 min | 30 min
4. Focus area: Specific topic, or "surprise me"
5. Learning style: Explain first | Jump into code | Mix

**Code Completion Drill** — Fill in the blanks without docs:
```markdown
## Drill: Array Methods (JavaScript) — 10 min
Given: const users = [{name: 'Alice', age: 25, active: true}, ...]
Write a one-liner to get names of active users:
const activeNames = // Your code here
// Expected: ['Alice', 'Carol']
<details><summary>Solution</summary>
users.filter(u => u.active).map(u => u.name)
</details>
```

**Bug Hunt Drill** — Find and fix the bug:
```markdown
## Drill: Find the Bug (React) — 5 min
This component doesn't update when clicked. Why?
function Counter() {
  let count = 0;
  const increment = () => { count = count + 1; };
  return <p>{count}</p><button onClick={increment}>Add</button>;
}
Fix: `let count = 0` → `const [count, setCount] = useState(0)`
```

**Explain It Drill** — Explain code in plain English (tests real understanding):
```markdown
## Drill: Explain This (TypeScript) — 5 min
type DeepReadonly<T> = { readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P] };
Your task: Explain what this type does. Bonus: When would you use it?
```

**Speed Drill** — Type commands from memory as fast as possible:
```markdown
## Drill: Type It Fast (Git) — 2 min
1. Check status: ___ 2. Stage all: ___ 3. Commit: ___ 4. Push: ___
5. Pull with rebase: ___ 6. New branch: ___ 7. Stash: ___ 8. Apply stash: ___
```

**Build From Scratch Drill** — No docs, no copying, just build:
```markdown
## Drill: Build Without References (React) — 15 min
Build a todo list: add, display, complete (strikethrough), delete.
Rules: No documentation. No copying. Guess before checking hints.
```

### 6. Drill Progressions (Sample: React Fundamentals)

```
Week 1: Components & Props (create, pass props, conditional render, list + keys)
Week 2: State & Events (useState, handlers, controlled inputs, state lifting)
Week 3: Effects & Lifecycle (useEffect, cleanup, dependency arrays, data fetching)
Week 4: Patterns (custom hooks, Context API, compound components, error boundaries)
Each week ends with a "build from scratch" review drill.
```

### 7. Tracking Progress

```markdown
| Date | Topic | Drill Type | Time | Result | Notes |
|------|-------|-----------|------|--------|-------|
| 01/15 | React useState | Code completion | 5m | Pass | Easy now |
| 01/16 | Array methods | Speed drill | 3m | Partial | Forgot reduce |
| 01/17 | TS generics | Explain it | 10m | Pass | Need more practice |
```

**Verification after each drill:**
1. Syntax Check: Does it run without errors?
2. Logic Check: Does it produce expected output?
3. Understanding Check: Can you explain it to someone else?
4. Retention Check: Can you do it again tomorrow?

## Success Criteria

- [ ] Socratic Drills ask at least 2 questions before giving the full answer
- [ ] Flashcard script successfully parses Basic and Cloze cards
- [ ] ELI5 explanations always start with an analogy
- [ ] Study plans link every topic to a tangible building project
- [ ] Practice drills completed without looking up documentation
- [ ] Code works on first or second try
- [ ] Can explain why the solution works

## Copy/Paste Ready

```
"Quiz me on [Topic] until I get it right."
"Convert these notes to Anki cards."
"Explain [Concept] like I'm 5."
"Create a learning path for [Skill]."
"Give me a code completion drill for React hooks, 15 minutes"
"Bug hunt drill: Python, intermediate"
"Speed drill: Git commands"
"Build from scratch: form validation, no docs allowed"
```
