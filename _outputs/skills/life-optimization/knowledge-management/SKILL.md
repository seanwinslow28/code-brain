---
name: knowledge-management
description: Personal Knowledge Management (PKM) and Second Brain assistant. Organizes notes, synthesizes research from multiple sources, and links related concepts. Use this skill when the user asks to "organize my nodes", "synthesize", "connect these ideas", or "update my knowledge base".
---

# Knowledge Management (Second Brain)

## Purpose

Acts as a "Digital Librarian" that structures, synthesizes, and retrieves information. It transforms a folder of loose text files into a cohesive "Second Brain" by enforcing metadata standards, identifying semantic links, and compressing context for long-term memory.

## When to Use

- **Synthesis:** When you have 5 different sources and want one summary ("Combine these 3 articles into a note").
- **Organization:** When your `/Inbox` is full of random thoughts.
- **Connection:** When you ask "Have I written about this before?"
- **Memory:** When closing a session and you want to save the context (`/compress`).

## Examples

**Example 1: Synthesis (The Research Digest)**
```
User: "Read the 4 PDF papers in /research and summarize the key findings on 'Agentic Memory'."
Claude: [Uses knowledge-management] I'll process the sources.
Generating synthesis note: `Agentic_Memory_Synthesis.md`...

**Core Themes Identified:**
1. **Episodic vs. Semantic:** All 4 papers distinguish between event logs (episodic) and fact retrieval (semantic).
2. **Retrieval Triggers:** Paper A and C propose vector-based retrieval.

**Consensus Matrix:**
| Feature | Paper A | Paper B | Paper C |
| :--- | :--- | :--- | :--- |
| Vector DB | ✅ | ❌ | ✅ |
| Graph | ❌ | ✅ | ❌ |
```

**Example 2: Context Compression**
```
User: "I'm done for today. Compress this session."
Claude: [Uses knowledge-management] Summarizing session...
Updating `project_log.md`:
- **Decisions:** Chose Python over Node for the scraper.
- **Open Loops:** The regex for 'Transport' is flaky.
- **Files Modified:** `scraper.py`, `CLAUDE.md`.
Context saved. Ready to `/resume` next time.
```

## Knowledge Workflow

### 1. The Atomic Note Pattern

When creating notes, ALWAYS use this frontmatter to ensure they are "surfaceable" later.

```markdown
---
type: concept | meeting | project | journal
date: YYYY-MM-DD
tags: [tag1, tag2]
status: draft | permanent
---

# Title
[Content]
```

### 2. Synthesis Protocol

When asked to "synthesize" or "summarize" multiple files, do not just concatenate summaries.
Use this structure:
1.  **Salient Keywords:** What terms appear in all sources?
2.  **Consensus Points:** Where do the sources agree?
3.  **Divergence:** Where do they disagree?
4.  **Actionable Takeaways:** What can I DO with this info?

### 3. Context Compression (`/compress`)

At the end of a long session, run this logic to save the state to the file system.

**Compression Logic:**
1.  **Read** the current conversation history (what we just did).
2.  **Extract** key decisions, new terms defined, and open questions.
3.  **Append** to `session_log.md` or `daily_notes/[Date].md`.

### 4. Lazy Prompting (Context Library)

Do not ask the user for context we already have.
*   "If the user asks about **Fitness**, read `contexts/health_profile.md`."
*   "If the user asks about **Work**, read `contexts/work_projects.md`."

## Success Criteria

- [ ] New notes always include YAML frontmatter.
- [ ] Synthesis outputs identify both consensus and divergence.
- [ ] Session compression captures open loops (unfinished tasks).
- [ ] Cross-linking suggestions are specific (referencing actual filenames).

## Copy/Paste Ready

```
"Synthesize these documents into a single note."
"Compress this session and save the context."
"Organize my inbox files."
"Link this new concept to my existing notes."
```
