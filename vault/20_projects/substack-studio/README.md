# Pencil & Prompt

*Push your AI past the average, one tested experiment at a time.*

This folder is the working studio behind the **Pencil & Prompt** Substack: posts, research, the playbook, the image house style, and the writing/image/research skill chain that produces every piece. The publication lives at [@seanpwins](https://substack.com/@seanpwins); this folder is where it gets made.

## The premise

The models got good, and now everything they make is the same. Pencil & Prompt runs real experiments that push agents past the median, in public, and publishes the verdicts, including the failures. Weekly experiment series: **Building the Ladder** (numbered rungs: one real job, the median shown, one named divergence mechanism run against it, honest verdict). Sibling story series: **Raising Agents** (funny true stories of raising a fleet of agents). The product underneath: a public, versioned mechanism library where every entry carries a tested verdict against a published measurement protocol. Model-agnostic; funny first, useful always; anti-hype.

The founding story is a failure report: the publication's previous premise (taste-transfer) died by Sean's own GPT Image 2 test, and the origin-confession flagship tells that story straight.

## The docs (read in this order)

1. **[SOUL.md](SOUL.md)**: the masthead. Wins all disagreements.
2. **[POSITIONING-AND-EDITORIAL-SPEC.md](POSITIONING-AND-EDITORIAL-SPEC.md)**: reader, verified white space, the six territories, voice, value model, relaunch plan.
3. **[SERIES-COMMAND-CENTER.md](SERIES-COMMAND-CENTER.md)**: the live editorial queue and conventions.
4. **[SKILL-PACKAGING-PLAN.md](SKILL-PACKAGING-PLAN.md)**: the mechanism-library catalog and hardening gate.
5. **[CLAUDE.md](CLAUDE.md)**: session law (voice chain, value gate, positioning guardrails, privacy).
6. **[REVAMP-2026-08-05-SESSION-MAP.md](REVAMP-2026-08-05-SESSION-MAP.md)**: the working order for the relaunch (S0-S6).

Decisions with verbatim reasons: the 2026-08-04 partner-session sidecar (local-only, `~/.creative-harness/partner-sessions/`). Evidence: [research/](research/) (the three 2026-08-05 syntheses are the citable base).

## How a post gets made

1. **Pick the rung** from the command center's queue (territory roster feeds it).
2. **Run the value gate** (`substack-value-engine`): the Itch must be genuinely Sean's, the Solution a real captured run. No capture, no post.
3. **Do the experiment for real.** Median census first (~20 runs), then the mechanism. The capture is the substance.
4. **Voice chain, in order:** `substack-value-engine` → `storytelling-architecture` → `writing-voice-modes` (Sean Mode) → `writing-critique` → `writing-humanity-pass`. No em dashes; anti-hype; the ask lands sideways.
5. **Sean hand-rewrites.** Always. His rewrite folds back into voice-samples.
6. **Ship the mechanism both tiers** (copy-paste + `.claude` skill) into the library with its verdict, then publish.

## Repo map

```
SOUL.md                             the masthead (read first)
POSITIONING-AND-EDITORIAL-SPEC.md   strategy source of truth
SERIES-COMMAND-CENTER.md            the editorial queue
SKILL-PACKAGING-PLAN.md             the mechanism-library catalog
CLAUDE.md / README.md               session law / you are here
REVAMP-2026-08-05-SESSION-MAP.md    relaunch working order (S0-S6)
research/                           syntheses, deep-dives, discovery ledgers (the evidence base)
pages/                              Start Here / About drafts (pre-refocus drafts = quarry)
playbook/                           tool-shipping-playbook.md, image-house-style.md
continuation-prompts/               dated session kickoffs + history
_assets/                            references + style anchors
_archive/                           the pre-divergence era: old docs + post folders (quarry, never base)
_private/                           gitignored, local-only sensitive lane
.claude/skills/                     symlinked skills (resolve to code-brain canonical copies)
```

## Current status (2026-08-05)

- **Name:** Pencil & Prompt (kept). **Subtitle:** "Push your AI past the average, one tested experiment at a time." (locked at the S1 naming pass).
- **Phase:** relaunch, working the session map. S0 (sourdough dark start) and S1 (this doc re-anchor) are done; next are S2 (image pass), S3 (pages + profile), S4 (origin confession), S5 (measurement protocol, hard-ordered before Rung 1), S6 (Rung 1).
- **Standing:** Notes run from day zero; sourdough feeds weekly in private; the territory set stays a loose lock until real posts prove the value.
