# Claude Code Prompt: Build Adobe MCP Skills from NotebookLM Research

Copy everything below the line into Claude Code.

---

## Context

I've spent 4 weeks building a comprehensive research corpus across 6 NotebookLM notebooks to support a two-stage creative automation system for my Claude Code Superuser Pack. The system has two layers:

1. **Creative Director Skill** (planning + critique) — Interviews me about creative intent, proposes 2-3 creative routes with pros/cons, generates a detailed technical execution plan, and reviews work-in-progress with expert critique feedback tied to design principles.

2. **Adobe App MCP Skills** (execution) — Takes the confirmed plan from the Creative Director, translates it into MCP tool calls via the adb-mcp project (https://github.com/mikechambers/adb-mcp), executes in small batches, verifies results, and loops with me for review.

**The user workflow:** Plan Mode (Creative Director) → confirm route → Execute Mode (app-specific MCP skill) → review cycle → iterate.

The adb-mcp architecture: `Claude Code ↔ MCP Server (Python, stdio) ↔ Proxy Server (Node.js, WebSocket) ↔ Adobe Plugin (UXP for PS/Premiere, CEP for AE/Illustrator) ↔ Adobe App`

## Your Task

Use the `notebooklm-mcp` to access my 6 NotebookLM notebooks, extract the synthesized knowledge from each, and create 6 Claude Code skill files. Each skill must follow the mandatory format defined in my `skill-system-mastery` skill (located at `.claude/skills/skill-system-mastery/SKILL.md` in this repo).

### The 6 Notebooks → 6 Skills

| Notebook Name | Skill to Create | Skill Path |
|---|---|---|
| Creative Direction & Critique Systems | `creative-director` | `.claude/skills/creative-director/SKILL.md` |
| Adobe Photoshop Mastery | `adobe-photoshop-mcp` | `.claude/skills/adobe-photoshop-mcp/SKILL.md` |
| Adobe Premiere Pro Mastery | `adobe-premiere-mcp` | `.claude/skills/adobe-premiere-mcp/SKILL.md` |
| Adobe After Effects Mastery | `adobe-aftereffects-mcp` | `.claude/skills/adobe-aftereffects-mcp/SKILL.md` |
| Adobe Illustrator Mastery | `adobe-illustrator-mcp` | `.claude/skills/adobe-illustrator-mcp/SKILL.md` |
| Adobe MCP Integration Hub | `adobe-cross-app-workflows` | `.claude/skills/adobe-cross-app-workflows/SKILL.md` |

## How to Execute

### Phase 1: Discovery

1. Use the notebooklm-mcp to list all my notebooks. Identify the 6 listed above.
2. For each notebook, list the sources to understand what's available.
3. For each notebook, look for **notes I've saved as sources** — these are the synthesis outputs from my research workflow:
   - **Creative Direction notebook**: Should contain an "Operating Charter," "App Handoff Protocol," and "Critique-to-Action Map"
   - **Each app notebook**: Should contain a "Skill Outline" note (a structured outline for that app's Claude Code skill)
   - **Integration Hub**: Should contain a "Master Plan" synthesis that maps shared patterns across all four app skills
4. These synthesis notes are the highest-priority sources — they're already structured for skill creation. The other sources provide supporting detail.

### Phase 2: Extract & Synthesize

For each notebook, query it to extract the information needed for that skill. Use targeted questions like:

**For the Creative Direction notebook:**
- "What are the critique rubrics and checklists documented in this notebook?"
- "What is the Operating Charter for the AI creative assistant?"
- "What is the App Handoff Protocol template?"
- "What is the Critique-to-Action Map that translates observations to Adobe tool actions?"
- "What creative brief templates exist for different project types?"

**For each Adobe app notebook (PS, Premiere, AE, Illustrator):**
- "What are the core fundamentals of [app] that an AI needs to understand?"
- "What MCP commands are available for [app] and what does each one do?"
- "What are the common workflow patterns documented for [app]?"
- "What are the known limitations and error patterns for the [app] MCP?"
- "What review/critique criteria exist for evaluating [app] output quality?"
- "What guardrails and safety patterns are documented for automated [app] operations?"

**For the Integration Hub notebook:**
- "What is the master plan for the Adobe MCP skill system?"
- "What shared patterns exist across all four app skills?"
- "What cross-app workflows are documented?"
- "What is the recommended skill file structure?"

### Phase 3: Create the Skills

Build each skill following **this exact mandatory section order** (from skill-system-mastery):

```
1. YAML frontmatter (name + description)
2. # Skill Title
3. ## Purpose
4. ## When to Use
5. ## Examples
6. ## [Domain Content] — the bulk, organized by task
7. ## Success Criteria
8. ## Copy/Paste Ready
```

**Critical formatting rules:**
- `name` field must be kebab-case and match the directory name
- `description` must include trigger phrases — the exact verbs and tool names users would type. This is NOT a summary of the workflow. It's WHEN to load the skill.
- Keep SKILL.md under 500 lines. Use `references/` for anything over 50 lines that's conditional (lookup tables, code example libraries, per-app command lists)
- Use imperative form throughout ("Review the composition" not "This skill reviews compositions")
- 2-3 examples showing realistic user/Claude dialog exchanges
- Success Criteria must be testable yes/no checklist items

### Skill-Specific Instructions

#### 1. `creative-director` Skill

This is the PLANNING skill. It does NOT execute MCP commands. It:
- Interviews the user about creative intent (audience, platform, tone, references, constraints, project context like 16BitFit branding vs. standalone)
- Proposes 2-3 distinct creative directions with pros/cons and effort estimates
- Generates a detailed technical execution plan for the chosen direction (step-by-step, which Adobe app handles each step, verification checkpoints)
- Reviews work-in-progress using critique rubrics (composition, hierarchy, color, pacing, timing, typography)
- Translates critique into actionable next steps mapped to specific Adobe tools
- Hands off to the appropriate `adobe-[app]-mcp` skill for execution

Embed the Operating Charter, App Handoff Protocol structure, and Critique-to-Action Map from the notebook directly into the skill content. The critique rubrics should be concrete enough that Claude can run them as checklists, not abstract theory.

If the critique frameworks from the notebook are extensive (50+ lines), put them in `references/critique-rubrics.md` with "when to read" guidance in SKILL.md.

**Description trigger phrases should include:** creative direction, plan project, review work, critique, art direction, creative brief, design review, visual feedback, propose options, plan edits

#### 2. `adobe-photoshop-mcp` Skill

This is an EXECUTION skill for Photoshop via the adb-mcp MCP server. It:
- Takes a confirmed plan from the Creative Director (or direct user requests)
- Translates plan steps into Photoshop MCP tool calls
- Executes in small batches (2-3 operations), then pauses for verification
- Uses `config://get_instructions` to load Photoshop-specific MCP guidance at session start
- Understands PS fundamentals: layers, masks, blending modes, selections, adjustments, smart objects, text, generative AI features
- Knows the available MCP commands and their parameters (from the notebook's source on `uxp/ps/commands/index.js`)
- Follows non-destructive patterns (no flatten/rasterize without explicit approval)
- Can review its own output by requesting a canvas screenshot and evaluating against quality criteria

If the full MCP command reference is extensive, put it in `references/ps-mcp-commands.md`.

**Description trigger phrases should include:** photoshop, edit image, create PSD, layer, mask, sprite sheet, generative fill, batch process, photo editing, image manipulation, PS MCP

#### 3. `adobe-premiere-mcp` Skill

Execution skill for Premiere Pro. Same structure as Photoshop but:
- Understands Premiere's MORE LIMITED MCP capabilities (the plugin API is less mature than PS)
- Clearly distinguishes what MCP can automate vs. what requires manual work
- Covers: timeline editing, transitions, effects, audio, color grading, export settings
- Knows editing grammar: when to use J-cuts, L-cuts, dissolves, hard cuts (from the notebook's editorial pacing sources)
- Handles export presets for different targets (festival submissions, YouTube, social)
- References media-utils-mcp for file analysis capabilities

If command reference is extensive, use `references/premiere-mcp-commands.md`.

**Description trigger phrases should include:** premiere, video editing, timeline, edit video, transitions, export, audio mix, color grade, sequence, cut, Premiere MCP

#### 4. `adobe-aftereffects-mcp` Skill

Execution skill for After Effects. This is the MOST POWERFUL app in the MCP system because:
- AE uses ExtendScript via CEP plugin, which allows running arbitrary scripts
- Claude can programmatically: create compositions, add/animate layers, set keyframes, apply effects, write expressions, manage render queue
- The AE object model (Application → Project → CompItem → Layers → Properties → Keyframes) is the foundation
- Expressions (AE's built-in dynamic scripting) are a key capability for creating dynamic animations
- Directly supports the animation pipeline: AI-generated frames → AE composition → smooth animation → render

This skill should teach Claude the AE object model thoroughly enough to write valid ExtendScript. If ExtendScript patterns/examples exceed 50 lines, put them in `references/ae-extendscript-patterns.md`.

**Description trigger phrases should include:** after effects, motion graphics, animation, composition, keyframes, expressions, ExtendScript, AE MCP, render, MOGRT, compositing

#### 5. `adobe-illustrator-mcp` Skill

Execution skill for Illustrator. Also uses ExtendScript via CEP:
- Understands vector vs. raster distinction
- Covers: paths, shapes, pathfinder, appearance, artboards, symbols, text, styles
- Illustrator DOM: Application → Document → Layers → PathItems/TextFrames/GroupItems
- SVG export optimization for web/game assets
- Character design model sheets for animation style guides

If ExtendScript patterns exceed 50 lines, use `references/ai-extendscript-patterns.md`.

**Description trigger phrases should include:** illustrator, vector, SVG, paths, icon, logo, artboard, illustration, character design, AI MCP, vector asset

#### 6. `adobe-cross-app-workflows` Skill

This is the INTEGRATION skill. It:
- Documents cross-app pipelines (e.g., Illustrator → Photoshop → After Effects → Premiere)
- Contains the MCP architecture reference (how the proxy/plugin system works, troubleshooting connectivity)
- Defines shared guardrails that apply to ALL app skills (naming conventions, checkpoint behavior, destructive action safeguards)
- Handles the Creative Director → execution skill handoff protocol
- Covers common cross-app scenarios: animation pipeline, sprite processing, social media content creation, festival submission workflow
- Acts as the troubleshooting guide when MCP connections fail

**Description trigger phrases should include:** adobe workflow, cross-app, pipeline, MCP troubleshooting, multi-app, handoff, adobe proxy, animation pipeline, asset pipeline

## Quality Checks Before Finishing

After creating all 6 skills, verify:

1. [ ] Each SKILL.md has valid YAML frontmatter with `name` matching directory name
2. [ ] Each `description` contains trigger phrases (NOT workflow summaries)
3. [ ] Mandatory section order is followed exactly in every file
4. [ ] No single SKILL.md exceeds 500 lines — heavy content is in `references/`
5. [ ] Every `references/` file has "when to read" guidance in the parent SKILL.md
6. [ ] The Creative Director skill does NOT contain MCP tool call instructions (that's the execution skills' job)
7. [ ] Each execution skill references `config://get_instructions` for loading app-specific MCP guidance
8. [ ] Each execution skill explicitly states the small-batch execution pattern (execute 2-3 ops → pause → verify → continue)
9. [ ] Cross-references between skills are correct (Creative Director references the 4 app skills by name; app skills reference the Creative Director for planning; all reference cross-app-workflows for shared patterns)
10. [ ] Success Criteria in each skill are testable yes/no items, not vague aspirations

## Important Context About Me

- I'm a beginner coder who understands fundamentals. The skills should explain technical concepts (like ExtendScript, UXP, object models) clearly enough that I can understand them when reviewing the skill files.
- I'm a 2D animator and PM — my use cases are: 16BitFit game sprites, animated short films for festivals, social media content, and automation workflows.
- These skills live in my Superuser Pack under `.claude/skills/` in the Creative Studio domain.
- I already have 89+ skills across 6 domains. These 6 new skills bring Creative Studio from 15 to 21 skills.

## Begin

Start by using notebooklm-mcp to list my notebooks and identify the 6 target notebooks. Then work through them one at a time, extracting the synthesis notes and creating each skill. Create the Creative Director skill first (it's the foundation the others reference), then the 4 app skills, then the cross-app-workflows skill last (it references all the others).
