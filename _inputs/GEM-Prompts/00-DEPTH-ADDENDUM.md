# Depth & Format Addendum

Append this section to any of the 11 extraction prompts when pasting into the GEM. It overrides the GEM's default compression behavior to produce skills with enough substance to be operationally useful.

---

## ADDENDUM — Paste this after the "PROMPT END" line of any extraction prompt

---

## Output Depth Requirements

Your default compression is too aggressive for these skills. Claude Code needs enough context to IMPLEMENT patterns correctly, not just know they exist. Follow these depth rules:

### Minimum Content Per Skill

- **SKILL.md body**: 80-200 lines minimum per skill. Under 80 lines means you've compressed too far.
- **Code examples**: Every pattern mentioned MUST include a complete, working TypeScript/React code block — not just a method name or one-liner description. "Use text.split(' ').map()" is NOT enough. Show the full component with imports, props interface, useCurrentFrame(), and the JSX return.
- **Reference files**: Generate a `references/` file for any skill that has lookup tables, parameter guides, or pattern libraries exceeding 50 lines. Do NOT try to cram everything into SKILL.md.

### What "Complete Code Example" Means

BAD (too compressed):
```
* **Word Stagger**: Use text.split(' ').map() to wrap words in <Sequence> components.
```

GOOD (operationally useful):
```tsx
// Word-by-word stagger reveal
interface WordStaggerProps {
  text: string;
  startFrame?: number;
  staggerFrames?: number;
}

export const WordStagger: React.FC<WordStaggerProps> = ({
  text,
  startFrame = 0,
  staggerFrames = 3,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: 'flex', gap: 8 }}>
      {text.split(' ').map((word, i) => {
        const delay = startFrame + i * staggerFrames;
        const opacity = spring({ frame: frame - delay, fps, config: { damping: 30 } });
        const y = interpolate(opacity, [0, 1], [20, 0]);
        return (
          <span key={i} style={{ opacity, transform: `translateY(${y}px)` }}>
            {word}
          </span>
        );
      })}
    </div>
  );
};
```

### Reference File Requirements

For each skill, evaluate whether it needs a reference file. Create one when:
- The skill has a lookup table (spring parameters, platform specs, easing functions) — put it in `references/`
- The skill has more than 3 code patterns — put the pattern library in `references/patterns.md`
- The skill has configuration templates — put them in `references/`

Example structure for a skill with reference files:
```
remotion-typography/
  SKILL.md                          (80-150 lines: workflow + 2-3 inline examples)
  references/
    text-patterns.md                (all text animation component code)
    motion-vocabulary.md            (spring parameter table + easing reference)
```

In SKILL.md, reference these files:
```markdown
For the complete library of text animation components, see `references/text-patterns.md`.
For spring parameter combinations by motion style, see `references/motion-vocabulary.md`.
```

### Mandatory SKILL.md Structure

Every SKILL.md MUST follow this exact section order. Do NOT skip sections or invent new ones.

```markdown
---
name: skill-name-in-kebab-case
description: One sentence describing what this does AND when Claude should auto-load it. Embed trigger phrases naturally.
---

# Skill Title

## Purpose

One paragraph: what this skill does and why it exists. Imperative form.

## When to Use

Bullet list of specific situations when Claude should activate this skill:
- Situation 1
- Situation 2
- Situation 3

## Examples

Show 2-3 realistic user/Claude dialog exchanges demonstrating the skill in action:

**Example 1: [Scenario name]**
```
User: "[realistic user prompt]"
Claude: [Uses skill-name] [What Claude does — show actual output patterns, not just descriptions]
```

**Example 2: [Scenario name]**
```
User: "[realistic user prompt]"
Claude: [Uses skill-name] [What Claude does]
```

## [Domain Content Sections]

The core patterns, code examples, decision trees, lookup tables, and reference material.
This is the bulk of the skill (60-150 lines). Organize by task, not by concept.
Every pattern mentioned MUST include a complete, working code example.

## Success Criteria

Bullet checklist of what makes this skill's output successful:
- [ ] Criterion 1 (testable, yes/no)
- [ ] Criterion 2

## Copy/Paste Ready

Show explicit invocation phrases users can type:
```
"[Natural language trigger 1]"
"[Natural language trigger 2]"
"[Natural language trigger 3]"
```
```

### Structural Rules

1. **Follow the section order exactly**: Frontmatter → Purpose → When to Use → Examples → Domain Content → Success Criteria → Copy/Paste Ready
2. **Examples are mandatory** — 2-3 user/Claude dialog pairs showing realistic usage. This is how Claude learns the skill's interaction pattern.
3. **Copy/Paste Ready is mandatory** — 3-5 natural language phrases a user would actually type
4. **Domain content is the bulk** — this is where code examples, decision trees, and patterns live (60-150 lines)
5. **No sections beyond what's listed** — no "Design Notes", "Packaging Notes", "Reference Links for You", "How to Install". Those go in YOUR response to me, not in the SKILL.md.

### Format Rules (Non-Negotiable)

1. **YAML frontmatter is mandatory** — every SKILL.md starts with `---\nname:\ndescription:\n---`
2. **description field must include trigger phrases** — this is the ONLY field Claude reads for auto-loading. Embed them naturally: "React Native debugging assistant. Diagnoses build failures, red screens, and performance issues systematically." NOT a list of keywords.
3. **Imperative form only** — "Use spring() for natural motion" not "This skill uses spring()"
4. **No human-facing sections** — no "Design Notes for This Skill", no "Reference Links for Your .md File", no packaging instructions inside the skill. These go in YOUR response to me, not in the SKILL.md content.
5. **No Google search wrapper URLs** — use direct URLs or, better, reference the MCP server: "Query the remotion-docs MCP server for current API syntax"
6. **No emoji in SKILL.md body** — skills are consumed by AI, not displayed to humans. No emoji in headings, no emoji in bullet points, no emoji in reference file names. Zero emoji.
7. **TypeScript only** — all code uses strict TypeScript with proper interfaces, not loose JavaScript
8. **Clean markdown** — no escaped characters (`\---`, `\#\#`, `\*\*`). Output raw markdown that can be saved directly as a .md file.
9. **Skill directory name must match the `name` field** — `remotion-typography/SKILL.md` has `name: remotion-typography`

### Compression Override

For these skills, adjust your compression rules:
- **DO compress**: Conceptual explanations Claude already knows (what React is, what TypeScript is, what animation means)
- **DO NOT compress**: Specific parameter values, component code, configuration snippets, lookup tables, and domain-specific patterns (these are WHY the skill exists)
- **The test**: After compression, could Claude implement the pattern from ONLY what's in the skill, without guessing? If not, you compressed too far.

### Output Checklist (Run Before Presenting)

For EACH skill, verify:
- [ ] SKILL.md has YAML frontmatter with `name` and `description` (description includes trigger phrases naturally embedded)
- [ ] SKILL.md follows the mandatory section order: Purpose → When to Use → Examples → Domain Content → Success Criteria → Copy/Paste Ready
- [ ] Examples section has 2-3 user/Claude dialog exchanges
- [ ] Copy/Paste Ready section has 3-5 natural language trigger phrases
- [ ] SKILL.md body is 80-200+ lines (not under 80)
- [ ] Every mentioned pattern has a complete, working code example (with imports)
- [ ] Reference files exist for lookup tables and pattern libraries exceeding 50 lines
- [ ] SKILL.md references its reference files with "when to read" guidance
- [ ] All code is TypeScript with proper interfaces
- [ ] No human-facing sections (Design Notes, Packaging Notes, Reference Links for You)
- [ ] Imperative form throughout
- [ ] Zero emoji anywhere in skill content (headings, body, reference files)
- [ ] Clean markdown — no escaped characters, ready to save as .md
- [ ] Skill directory name matches the `name` field in frontmatter

---

## END ADDENDUM
