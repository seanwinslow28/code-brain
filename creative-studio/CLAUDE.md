# CLAUDE.md — Creative Studio (Domain: Creative Work)

Domain context for Sean's creative work — 16BitFit Battle Mode, Remotion video production, pixel art, animation pipeline, creative writing, Adobe MCP workflows. For ecosystem-wide rules, see root [CLAUDE.md](../CLAUDE.md).

## Scope of This Domain

**In:** 16BitFit Battle Mode (game + sprite pipeline + autoresearch + LoRA), Remotion programmatic video, pixel art, animation production (with eye toward animated short films), creative writing across formats, Adobe app pipelines (Photoshop, Premiere, After Effects, Illustrator), design system work, ComfyUI workflows, AI creative tooling.

**Out:** Personal finance/health/learning, job-hunt logistics. Those route to [life-systems/CLAUDE.md](../life-systems/CLAUDE.md) or `vault/20_projects/prj-job-hunt-2026/`. The-block templates are archived (see [the-block/CLAUDE.md](../the-block/CLAUDE.md) for reference patterns from the prior role).

## Operating Model

The five-artifact bundle for this domain (populated by the [`work-operating-model`](../.claude/skills/work-operating-model/SKILL.md) skill):

- Heartbeat (rhythms): [vault/05_atlas/operating-models/creative-studio/HEARTBEAT.md](../vault/05_atlas/operating-models/creative-studio/HEARTBEAT.md)
- User profile (decisions): [vault/05_atlas/operating-models/creative-studio/USER.md](../vault/05_atlas/operating-models/creative-studio/USER.md)
- Soul (people / tools / tribal): [vault/05_atlas/operating-models/creative-studio/SOUL.md](../vault/05_atlas/operating-models/creative-studio/SOUL.md)
- Synthesized model: [vault/05_atlas/operating-models/creative-studio/operating-model.md](../vault/05_atlas/operating-models/creative-studio/operating-model.md)
- Schedule rules: [vault/05_atlas/operating-models/creative-studio/schedule-recommendations.md](../vault/05_atlas/operating-models/creative-studio/schedule-recommendations.md)

If those files still show `status: awaiting-interview`, run: `Run the work-operating-model interview for creative-studio`.

## Workspace Layout

- `16bitfit-battle-mode/` — the 16BitFit project (sprite pipeline, agent fleet, autoresearch, LoRA training). Has its own [CLAUDE.md](16bitfit-battle-mode/CLAUDE.md) and `SOURCE-OF-TRUTH.md`. **Moved here from repo root in v3.15.0.**
- `design-team/` — design system reference, brand guidelines, support files for the read-only design-team review agents. **Moved here from repo root in v3.15.0.** The agents themselves live at canonical [.claude/agents/](../.claude/agents/).
- `finance/` — creative-studio business finance (separate from personal finance, which lives in `life-systems/`)
- `scripts/` — automation scripts specific to creative production
- `templates/` — reusable production templates

## Project-Specific Handoff: 16BitFit

When working on 16BitFit specifically, **load [16bitfit-battle-mode/CLAUDE.md](16bitfit-battle-mode/CLAUDE.md) and [16bitfit-battle-mode/SOURCE-OF-TRUTH.md](16bitfit-battle-mode/SOURCE-OF-TRUTH.md) instead of relying solely on this general creative-studio context.** The 16BitFit project has its own non-negotiables (Gemini image models, RTX 5080 SDPA-only, hexagonal architecture, Illustrious XL v0.1 LoRA base, etc.) that override generic creative defaults.

## Primary Skills for This Domain

| Skill | Purpose |
|---|---|
| `creative-director` | Interview, propose 2-3 routes, plan Adobe execution, critique work-in-progress |
| `animation-pipeline` | End-to-end 2D animation production with AI-assisted generation (ComfyUI, RIFE/FILM, QA gates) |
| `2d-animation-principles` | Physics, timing, production rules for animation |
| `script-writing` | Screenplay format for animated shorts |
| `pixel-art-retro-style` | 4-color Game Boy palette, 8x8 grid alignment, dithering rules |
| `phaser-game-patterns` | Phaser 3 for the 160x144 fitness RPG |
| `comfyui-workflows` | Workflow JSON design, node wiring, custom nodes, batch generation |
| `sprite-asset-pipeline` | Pixel Purity Pipeline — clean sprites, pack atlases, enforce naming |
| `ai-creative-tools` | Orchestrate ComfyUI / ElevenLabs / Hugging Face creative pipelines |
| `video-animation-production` | FFmpeg / ImageMagick automation |
| `creative-writing` | Multi-format (blog, social, pitch, bio) |
| `writing-voice-modes` | 5 calibrated voice modes including "Sean Mode" |
| `remotion-fundamentals` | Project setup, useCurrentFrame, spring, interpolate, sequences |
| `remotion-typography` | Text and typography animation in Remotion |
| `remotion-data-viz` | Animated charts (bar / line / donut / counter) for crypto data viz |
| `remotion-transitions` | Multi-scene composition with @remotion/transitions |
| `remotion-advanced` | Audio-reactive video, 3D, AI-generated media integration, Lottie |
| `remotion-social-output` | Platform formats (Reels, Shorts, TikTok, X, LinkedIn) |
| `remotion-troubleshooting` | delayRender debugging, performance optimization |
| `remotion-claude-config` | CLAUDE.md template for new Remotion projects |
| `adobe-photoshop-mcp` | Photoshop automation via adb-mcp |
| `adobe-premiere-mcp` | Premiere Pro timeline + export automation |
| `adobe-aftereffects-mcp` | After Effects compositions, expressions, MOGRTs |
| `adobe-illustrator-mcp` | Vector / SVG / icon / logo automation |
| `adobe-cross-app-workflows` | Cross-app pipeline orchestration + MCP architecture |
| `design-arena` | Competitive UI/UX design exploration via Pencil.dev + agent teams |
| `figma-to-code-workflow` | Figma → code via MCP servers |
| `prompting-beautiful-ui` | Awwwards-level UI prompting |
| `tailwind-advanced-patterns` | Premium gradient / glassmorphism / animation Tailwind |
| `shadcn-ui-patterns` | shadcn/ui patterns when scaffolding UI |
| `micro-interaction-patterns` | Polish patterns for hover / loading / form / scroll |
| `visual-polish-checklist` | Systematic visual QA |
| `animation-library-mastery` | Selection between Motion / React Spring / GSAP / CSS |
| `react-native-animations` | Reanimated 3 + Gesture Handler 2 patterns |
| `career-transition` | PM-to-animation-producer career arc work |

## Primary Agents for This Domain

The **design-team quintet** (all read-only — they audit, you fix):

- `ui-reviewer` — layout, spacing, color, typography, hierarchy
- `accessibility-checker` — WCAG 2.1 AA, contrast, keyboard nav, ARIA
- `design-system-enforcer` — token compliance, naming, component patterns
- `visual-polish-auditor` — animations, loading/empty/error states, micro-interactions
- `animation-director` — animation asset and shot-packet QA, applies animation-pipeline gates

Also:
- `creative-director` — scoped strategy + critique (also a skill; agent form delegates the workflow)
- `game-design-advisor` — game mechanics and creative direction for game projects

## Active MCPs Used Here

- **Adobe MCP proxies** (Photoshop, Premiere, After Effects, Illustrator) via adb-mcp
- **Figma** (`claude.ai Figma`) — design imports
- **Hugging Face** (`claude.ai Hugging Face`) — model + dataset + space search
- **Pencil** — design generation in `.pen` files
- **NotebookLM** (`notebooklm-mcp`) — research synthesis for creative briefs
- **Obsidian Vault** — design notes, creative project tracking

## Non-Negotiable Rules Specific to This Domain

1. **Design-team agents are read-only** (`disallowedTools: Edit, Write, Bash`). They audit, Sean fixes. Don't modify their tool permissions.
2. **Pixel-art rules are strict.** Game Boy 4-color palette, 8x8 grid alignment, no anti-aliasing on sprites. Use `pixel-art-retro-style` skill.
3. **For 16BitFit work:** load [16bitfit-battle-mode/CLAUDE.md](16bitfit-battle-mode/CLAUDE.md) for the 8 project-specific non-negotiables (Gemini models, RTX 5080 constraints, SDK names, Keychain, hexagonal architecture, LoRA base model, Phi-4).
4. **Don't generate without a brief.** Use `creative-director` to scope before invoking generation skills. Generic outputs waste compute.
5. **Sprites and animation frames go through QA gates.** Don't ship unprocessed AI output — pipe through `sprite-asset-pipeline` (sprites) or `animation-pipeline` QA gates (animation frames).

## Related Vault Paths

- MOC: [vault/05_atlas/moc-creative-studio.md](../vault/05_atlas/moc-creative-studio.md)
- Active project: [vault/20_projects/prj-animation-pipeline](../vault/20_projects/prj-animation-pipeline)

## When Modifying This Domain

- Update [CHANGELOG.md](../CHANGELOG.md) for any new creative-specific skill, agent, hook, or workflow
- For 16BitFit-specific changes, also update [16bitfit-battle-mode/SOURCE-OF-TRUTH.md](16bitfit-battle-mode/SOURCE-OF-TRUTH.md)
- Update [vault/05_atlas/operating-models/creative-studio/](../vault/05_atlas/operating-models/creative-studio/) artifacts when creative cadence / dependencies / friction shifts
