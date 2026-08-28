# sw-creative-toolkit

> **ARCHIVED 2026-07-30** (Sean-ratified, creative-harness wayfinder T27c). Preserved as a
> reference quarry, not installed as live skills. The plugin registration
> (`~/.claude/plugins/sw-creative-toolkit`, a broken symlink to a deleted BMAD folder) was
> removed the same day. The technique catalogs under `skills/*/references/` are the
> absorbable value for future skill work. Sean's ruling: "I don't want them completely
> deleted, but in an archive folder is perfect for them."

Six creative-strategy workflow skills for product managers, distilled from BMad CIS into pure Anthropic-format Cowork skills. Voice-flavored facilitation; clean, neutral output artifacts.

## What's in here

| Skill | Use when you want to... | Voice |
|---|---|---|
| `design-thinking` | Run a 5-phase human-centered design workshop — Empathize, Define, Ideate, Prototype, Test | Maya — jazz-musician facilitator |
| `problem-solving` | Diagnose root causes systematically with Five Whys, Fishbone, TRIZ, Theory of Constraints, Systems Thinking | Dr. Quinn — Sherlock-meets-scientist |
| `innovation-strategy` | Map a market, find unmet jobs, design a business model, evaluate disruption opportunities | Victor — chess grandmaster |
| `presentation` | Design slides, pitch decks, video explainers, conference talks, infographics, visual metaphors, concept visuals | Caravaggio — creative director |
| `storytelling` | Craft launch narratives, customer stories, change stories, pitch arcs, brand stories — across short / medium / extended formats | Sophia — bardic warmth |
| `brainstorm` | Run a *technique-driven* ideation session (SCAMPER, Six Thinking Hats, Crazy 8s, etc.) targeting 100+ ideas | Carson — improv coach |

Each skill installs as `sw-creative-toolkit:<skill-name>` in Cowork.

## Voice handling

Every skill has a thin **voice** line at the top of its body. The voice applies to **facilitation only** — questions, transitions, encouragement.

Output artifacts (POVs, HMW questions, decision matrices, slide outlines, narratives, idea lists) stay **clean, neutral, and on-brand for your product**. No jazz metaphors in your business model canvas. No improv-coach asides in your top picks list.

Each skill defines three prose registers explicitly:

1. **Facilitation prose** — voice applies
2. **Artifact prose** — clean, what you'll copy and use
3. **Rationale prose** — plain explanatory, neither voice nor museum-label

If you want a clean / neutral / "no persona" mode, say so once at the start of any session and the voice drops immediately.

## Sister skill — when NOT to use `brainstorm`

The Anthropic `superpowers:brainstorming` skill claims primacy for unstructured intent discovery before code or features. Use it for:
- "Let's brainstorm" with no defined topic
- Exploring requirements before building

Use `sw-creative-toolkit:brainstorm` for:
- Technique-driven idea volume on a *defined* topic ("100 ideas about X using SCAMPER")
- Named-technique invocation ("let's run six thinking hats")

If you say bare "let's brainstorm," `superpowers:brainstorming` will (and should) win the trigger. Use named techniques to invoke this skill.

## Output

All skills render output **inline as the response**. No file writes — except `storytelling`, which optionally persists a sidecar memory at `${CLAUDE_PLUGIN_DATA}/storyteller-sidecar.md` so Sophia remembers your audience profiles, framework preferences, and voice signatures across sessions.

If the persistent data directory isn't writable in your runtime, the storytelling skill renders the sidecar update inline as a code block instead — it tells you so you know.

## Installation

### Cowork (production)

```bash
cd path/to/sw-creative-toolkit
zip -r ../sw-creative-toolkit.zip . -x "*.DS_Store"
```

In Cowork: **Browse plugins → Upload custom plugin → select the zip**.

### Local Claude Code (dev / testing)

```bash
ln -s /absolute/path/to/sw-creative-toolkit ~/.claude/plugins/sw-creative-toolkit
```

Or pass via flag at session start. Each skill auto-loads from natural prompts that include trigger phrases listed in its description.

## Plugin structure

```
sw-creative-toolkit/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── design-thinking/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── problem-solving/
│   ├── innovation-strategy/
│   ├── presentation/
│   ├── storytelling/
│   └── brainstorm/
└── README.md
```

Each skill follows progressive-disclosure architecture: SKILL.md is the workflow contract, `references/` holds the deep method libraries that load on demand.

## Authorial intent

The personas are flavor. The methodologies are the asset. If you want clean output without facilitation flavor, say "neutral mode" at the start of any session. Every skill respects it.
