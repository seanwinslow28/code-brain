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

## Success Criteria

- [ ] Socratic Drills ask at least 2 questions before giving the full answer.
- [ ] Flashcard script successfully parses Basic and Cloze cards.
- [ ] ELI5 explanations always start with an analogy.
- [ ] Study plans link every topic to a tangible building project.

## Copy/Paste Ready

```
"Quiz me on [Topic] until I get it right."
"Convert these notes to Anki cards."
"Explain [Concept] like I'm 5."
"Create a learning path for [Skill]."
```
