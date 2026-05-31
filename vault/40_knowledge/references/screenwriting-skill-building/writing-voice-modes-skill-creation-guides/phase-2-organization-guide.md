# Phase 2: Organizing Your Research → One Usable Reference Doc

## Step 1: Store Everything in the Vault (Raw Archive)

Create this folder structure inside your vault:

```
vault/40_knowledge/references/
├── ref-voice-mechanics-research.md          ← THE COMPILED DOC (Step 2)
├── voice-modes-raw/                         ← Raw research archive
│   ├── perplexity-kerouac.md
│   ├── perplexity-thompson.md
│   ├── perplexity-vonnegut.md
│   ├── perplexity-sedaris.md
│   ├── notebooklm-kerouac-synthesis.md
│   ├── notebooklm-thompson-synthesis.md
│   ├── notebooklm-vonnegut-synthesis.md
│   ├── notebooklm-sedaris-synthesis.md
│   └── notebooklm-cross-author-synthesis.md
```

Each raw file gets basic frontmatter:

```yaml
---
type: reference
domain:
  - creative-studio
status: active
context: writing-voice-modes
ai-context: "Raw Perplexity Deep Research output on Jack Kerouac's writing techniques."
created: 2026-03-01
source: perplexity-deep-research
---
```

**Why keep the raw files:** Future reference, and if you upgrade the skill later
(or adapt it for script-writing), you can re-mine these without re-running the research.

---

## Step 2: Compile the Reference Doc (This Is the Actual Phase 2 Work)

This is where YOUR judgment matters — not Gemini's, not NotebookLM's. You're
the editor. The compilation process is:

### What You're Doing

Reading through all 9 documents and pulling out ONLY the techniques that are:
1. **Specific enough to be actionable** — "Vonnegut uses short sentences" = cut.
   "Vonnegut averages 8-12 word sentences, rarely exceeding 20, and deploys
   a single long sentence (30+ words) every 2-3 paragraphs for contrast" = keep.
2. **Transferable to your content** — If a technique only works for novel-length
   fiction, cut it. If it works for blog posts, social media, or tech docs, keep it.
3. **Resonant with you personally** — This is the filter Gemini can't apply.
   When you read a technique and think "oh, I'd actually use that," it goes in.
   When you think "that's cool but not me," it stays in the raw archive.

### How to Actually Do It

**Option A: Manual curation (recommended, ~60-90 min)**

Open each of the 9 docs side by side with a blank ref-voice-mechanics-research.md.
For each author, pull the best material into the compiled doc using this structure:

```markdown
## [Author Name]: The [Mode Name] Mode

### Core Technique (1 sentence)
[The single most important thing this author does differently]

### Sentence Mechanics
- [Only the specific, actionable patterns — with examples]

### Structural Signatures
- [How they open, build, and close — with examples]

### Humor / Emotional Mechanics
- [What creates their distinctive effect — the formula, not the vibe]

### Transferable Techniques (ranked by usefulness)
1. [Technique name]: [What it is] → [How it applies to tech/AI writing]
2. [Technique name]: [What it is] → [How it applies to tech/AI writing]
3. [etc.]

### Anti-Patterns (what makes this mode become parody)
- [Specific warning signs]
```

For each section, you're choosing the BEST version across your Perplexity output
AND your NotebookLM synthesis. Sometimes Perplexity found a better example.
Sometimes NotebookLM's synthesis was sharper. Pick the winner for each point.

**Option B: Claude Code-assisted curation (~30-45 min)**

Upload all 9 raw docs to a Claude Code session (or this chat) and ask:

"Read all 9 documents. For each author, extract ONLY the techniques that are
(a) specific enough to include a concrete example, (b) transferable to blog
posts, social media, or technical writing about AI/technology, and (c) not
redundant with another technique already extracted. Organize using [the
template above]. Flag any places where Perplexity and NotebookLM disagree
so I can make the call."

Then you EDIT the output — add your personal resonance filter, cut anything
that feels generic, and add any techniques you noticed in the raw research
that the compilation missed.

---

## Step 3: What Claude Code Gets During the Interview

During the Phase 3 interview session, Claude Code loads ONLY:

1. `ref-voice-mechanics-research.md` (the compiled doc — this is the primary context)
2. Your existing `creative-writing` SKILL.md (so it knows the current format system)
3. Your existing `technical-writing` SKILL.md (same reason)

That's it. NOT all 9 raw docs. The compiled doc IS the research — it's the
signal extracted from the noise.

---

## Step 4: After the Interview → Skill Creation

The interview output + compiled research feeds into building the
`writing-voice-modes` SKILL.md. The raw archive stays in your vault
for when you circle back to upgrade script-writing and other creative skills.

---

## The Key Insight

Phase 2 is not "organize files into folders." Phase 2 is **editorial curation** —
you're the editor deciding which techniques from 9 documents of research
make the cut for the final reference. The folder structure is just where
things live. The real work is the compilation, and that requires YOUR taste.
