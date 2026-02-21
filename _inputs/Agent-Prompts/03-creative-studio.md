# Creative Studio — Agent Extraction Prompt

Use this prompt with the **Agent Extraction Kickoff** after connecting to the **"Claude Code - Creative Projects"** and **"Claude Code - Remotion Mastery"** NotebookLM notebooks.

---

## PROMPT START — Process this domain with the Kickoff Prompt

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I build creative side projects: a Game Boy-style fitness RPG called 16BitFit (Phaser 3 + React Native), and video content using Remotion. My aesthetic is retro pixel art with strict 4-color Game Boy palette constraints. I also produce social media video content for work.

I'm upgrading one thin agent and creating one new agent for the Creative Studio domain. These agents provide **structured creative review and direction** — the 15 creative-studio skills handle implementation knowledge.

## What's in These Notebooks

**Notebook 1: "Claude Code - Creative Projects"** (63 sources)
Game development with Phaser 3, sprite pipelines, pixel art constraints, fitness RPG design patterns, mobile game UX, AI creative tools. Sources include game design principles, Phaser tutorials, and pixel art guides.

**Notebook 2: "Claude Code - Remotion Mastery"** (504 sources)
Remotion video production: composition patterns, animation timing, transitions, typography, data visualization, social media formats, brand configuration. The richest notebook with extensive source coverage.

## Your Task

Extract behavioral knowledge from these notebooks and generate **2 agents** for the Creative Studio domain: 1 upgrade and 1 new.

## Target Agents

### 1. UPGRADE: game-design-advisor
**Priority**: High
**Current state**: 37 lines, generic 7-item capability list, no design review framework, no output template
**Current file**: `.claude/agents/game-design-advisor.md` (READ THIS FIRST)
**Type**: Advisory agent (read-only for code review, can run game previews)
**disallowedTools**: Edit, Write

**What to extract from notebooks**:
- Game design review dimensions:
  - **Core Loop Engagement**: Is the play → reward → progress cycle satisfying? How many seconds to first reward? Is the loop self-reinforcing?
  - **Progression System**: XP curves, unlock pacing, power scaling, meaningful choices vs stat inflation
  - **Difficulty Curve**: Learning curve for new players, difficulty ramp, fail state design (punishing vs forgiving)
  - **Player Feedback**: Visual/audio feedback for actions, juice/feel, screen shake, particle effects
  - **Session Design**: Session length appropriate for mobile? Clean pause/resume? Progress saved on interrupt?
- Fitness RPG-specific patterns: exercise-to-reward mapping, real-world effort → in-game progress, motivation mechanics, habit formation through gameplay, gamification of health data
- 16BitFit-specific constraints: 160x144 resolution, 4-color Game Boy palette, 8x8 tile grid, retro RPG conventions (top-down, tile-based movement, dialog boxes)
- Mobile-specific concerns: touch input accuracy, battery/performance impact, session interruption handling, offline capability

**Output format requirements**:
- Design Review with per-dimension assessment
- Score per dimension (1-10)
- Specific findings with severity (Critical/Important/Minor)
- Recommendations prioritized by player impact
- 16BitFit-specific notes where applicable

**Trigger phrases**: "review this game design", "is this mechanic fun", "game design feedback", "16BitFit", "fitness game", "game loop", "player experience"

**Must preserve from current thin agent**: Game design guidance, mobile optimization, player engagement, game mechanics balancing

### 2. NEW: video-director
**Priority**: High
**Type**: Advisory agent (read-only review and planning)
**disallowedTools**: Edit, Write

**What to extract from notebooks**:
- Video composition review dimensions:
  - **Timing & Pacing**: Scene duration appropriate? Entry/stay/exit choreography? Breathing room between transitions? Frame-accurate timing?
  - **Visual Hierarchy**: Primary information prominent? Eye flow guided correctly? Text readable at speed? Visual weight balanced?
  - **Motion Quality**: Spring configs natural? Easing appropriate for content type? No jarring motion? Consistent motion language throughout?
  - **Brand Consistency**: Colors match brand palette? Typography follows brand guidelines? Tone appropriate for platform and audience?
  - **Platform Optimization**: Aspect ratio correct for target platform? Duration within platform norms? Safe zones respected? Text minimum size for mobile viewing?
- Scene structure advisory: entry animation → content hold → exit animation, transition selection by content relationship (cut vs dissolve vs wipe), multi-scene flow and pacing
- The Block brand alignment: Primary #1A1A2E, Accent #E94560, Background #0F3460, Text #FFFFFF, professional/authoritative tone
- Platform-specific specs:

| Platform | Aspect Ratio | Max Duration | Min Text Size |
|----------|-------------|-------------|---------------|
| Instagram Reel | 9:16 | 90s | 24px |
| Twitter/X | 16:9 | 140s | 20px |
| LinkedIn | 16:9 or 1:1 | 10min | 18px |
| YouTube Short | 9:16 | 60s | 24px |

**Output format requirements**:
- Scene-by-scene review (scene name, duration, assessment per dimension)
- Overall composition score (1-10)
- Brand compliance status (Compliant / Minor deviations / Major deviations)
- Platform readiness checklist (format, duration, text size, safe zones)
- Specific recommendations with frame references where possible

**Trigger phrases**: "review this video", "is the pacing right", "Remotion composition review", "video for Instagram", "brand check on this video", "video direction", "scene timing"

## Extraction Guidance

- The game-design-advisor needs EVALUATION CRITERIA, not game development knowledge (that's in the skills). Focus on what makes a game mechanic good or bad, not how to implement it.
- The video-director should be able to review a Remotion composition's code and assess the creative choices — timing, pacing, visual hierarchy — without modifying it.
- Include The Block brand specs in the video-director since Sean produces work content.
- Both agents should use severity levels (Critical/Important/Minor) for their findings.
- The Remotion Mastery notebook (504 sources) is the richest — query it thoroughly for video direction patterns.

## Cross-Domain Notes

- game-design-advisor pairs with `phaser-game-patterns`, `pixel-art-retro-style`, `sprite-pipeline` skills
- video-director pairs with `remotion-fundamentals`, `remotion-transitions`, `remotion-typography`, `remotion-social-output` skills
- video-director uses brand specs from `design-system-claude-md` skill
- Both complement the design-team review agents (which focus on UI code, not creative content)

## Quality Bar

Each generated agent should:
- Be 100-150 lines (Rich tier)
- Have concrete evaluation dimensions with specific criteria (not "check if it looks good")
- Include platform-specific guidance where relevant
- Include a complete output format template with severity levels
- Reference real skills and agents from the pack

---

## PROMPT END
