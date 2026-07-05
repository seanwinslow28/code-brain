# Pencil & Prompt

*Teach the machine your taste, one creative job at a time.*

This repo is the working studio behind the **Pencil & Prompt** Substack: posts, research, the playbook, the image house style, and the writing/image/research skill chain that produces every piece. The publication lives at [@seanpwins](https://substack.com/@seanpwins); this folder is where it gets made.

## The promise

For the creative who tried AI, got soulless output from a prompt or two, and walked away sure it has no taste. Pencil & Prompt changes their mind by *showing*, not preaching: take a real creative job from soulless to genuinely good, live, and teach the method that got it there. The thesis under every post is that AI is not here to replace the artist. It is a wildly talented intern with no taste yet, and the job is to teach it yours until it makes work that is recognizably you, on demand.

Full positioning, voice, value model, and the relaunch plan live in **[POSITIONING-AND-EDITORIAL-SPEC.md](POSITIONING-AND-EDITORIAL-SPEC.md)**. That doc is the source of truth. This README is orientation.

## The arc (re-anchored 2026-06-29): partner, then system, then art

The masthead is **have the agent think like me**. You build a creative partner by brainstorming and interviewing the agent into your taste, *then* build the system on top of it, *then* make the art that is yours. The first posts are the partner on-ramp; the **system framework** (spec it, test it, version it, gate it) is the destination they earn, not the front door. An earlier framing (2026-06-28) led with the framework and drifted the masthead onto the architecture; it was re-anchored here. The pivot's insight survives and feeds the destination: isolated techniques are commodity, and the deeper craft is treating creative AI as a system. Masthead: [`SOUL.md`](SOUL.md). History: [`2026-06-28-pivot-prompts-to-systems.md`](2026-06-28-pivot-prompts-to-systems.md) (evidence) plus [`CONTINUATION-2026-06-29-refocus-partner-then-system.md`](CONTINUATION-2026-06-29-refocus-partner-then-system.md) (refocus).

## The reader and the white space

- **The one reader:** the blocked, skeptical artist. A non-coding creative (illustrator, writer, animator, musician, designer) who is AI-curious but burned, and a little ashamed of using it. Sean is the guide and the character, not the audience.
- **The white space Sean owns:** maker's soul (real craft demos) + skeptic's-eye-level empathy + a *teachable* taste-transfer method + a tool that kills the grind + dive-bar anti-hype voice. None of the three closest comparables (Don Giannatti curates, Gabe Michael masters, Nate Jones analyzes) stand here.

## The formats

1. **The Spine** (teaching demos): one creative job, the partner taking it soulless to yours move by move, ending in the transferable method + both-tier artifacts. The signature. Follows one creative project across media (comics, animation, music & voice, editing).
2. **Back to Basics** (working: "Tim the Tool Man"): the tool-onboarding series, NEW 2026-06-29. Introduce a technical partner (skills/`.claude`, then Pi, Hermes, Higgsfield, ComfyUI), why it is a superpower and how it works, wired to the taste-transfer method. The bridge that brings non-coders into the technical.
3. **Tool drop**: "I built you a thing," shipped in both tiers (copy-paste + symlinkable skill). Periodic, tentpole, the premium line.
4. **Fix My Mess**: flagged for re-evaluation under the refocus (may fold into the System arc's public Gate).

Full format set + the first-arc lineup: [`SOUL.md`](SOUL.md) §5-6.

## How a post gets made

1. **Pull an angle** from `research/discovery/` (the idea ledger + value-engine brief), or take a reader submission for Fix My Mess.
2. **Run the value gate** (`substack-value-engine`): the Itch must be genuinely Sean's, and the Solution must be a real artifact, not hand-waving. If it is not, the gate blocks and the angle goes back.
3. **Do the work for real.** Sean runs the soulless-to-art transformation in his own craft lane (animation, writing, visual). That captured run *is* the substance of the post.
4. **Voice chain, in order:** `substack-value-engine` → `storytelling-architecture` → `writing-voice-modes` (Sean Mode) → `writing-critique` → `writing-humanity-pass`. No em dashes; anti-hype; the ask lands sideways.
5. **Hero image** in the pencil-test house style via `openai-image-gen` (see `playbook/image-house-style.md`). Image generation runs on the Mac, not in Cowork.
6. **Publish** to @seanpwins on the format's clock.

## Repo map

```
POSITIONING-AND-EDITORIAL-SPEC.md   the source of truth (read first)
README.md / CLAUDE.md               the heart docs (you are here / the agent rules)
01-…/ … 07-…/  bonus-…/             post folders (post.md + images/), the founding arc
playbook/                           tool-shipping-playbook.md, image-house-style.md
research/
  discovery/                        idea ledgers + value-engine briefs (post angles, sourced pain)
  deep-dives/                       deeper cited research
  last30days/                       fresh real-complaint scans
_assets/                            references/ + style-anchors/ (image house-style inputs)
_private/                           gitignored, local-only lane for anything sensitive
.claude/skills/                     symlinked voice/image/research skills (resolve to code-brain)
CONTINUATION-*.md / *-KICKOFF.md / MIGRATION-REPORT.md   session logs + history
SERIES-COMMAND-CENTER.md            the editorial queue (stale "Raising Claude", being rebuilt)
```

## Current status

- **Name:** locked. Pencil & Prompt, subtitle *"Teach the machine your taste, one creative job at a time."*
- **Phase:** relaunch. Same account (@seanpwins), rebranded from the old "Raising Claude" framing.
- **Front door, next up:** the About page and an origin/manifesto post as the new #1. Then recast posts 1 and 2 as early spine entries; rework or shelve post 3.
- **Profile:** bio still reads the old PM line and needs the empathetic-believer rewrite; restacks are mostly on-thesis (curate, do not nuke). The 3 live posts get reverted to drafts and recast.
- **Editorial queue:** currently in `SERIES-COMMAND-CENTER.md`, which is the stale "Raising Claude" spine and is being rebuilt against the discovery angles. Until then, the spec §10 relaunch plan is the running order.
