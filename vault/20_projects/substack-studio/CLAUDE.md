# CLAUDE.md — Pencil & Prompt (substack-studio)

The operating manual for any session working in this folder. Rules here are standing law. The strategy they enforce lives in the spec.

## 0. Read first, every time

**[SOUL.md](SOUL.md) before any work, it is the masthead.** "Have the agent think like me; build the partner, then the system, then the art." Then [POSITIONING-AND-EDITORIAL-SPEC.md](POSITIONING-AND-EDITORIAL-SPEC.md) for the strategic detail (the one reader, the white space, the voice, the value model, the formats, the relaunch plan). If anything here disagrees with SOUL.md, SOUL.md wins; the spec wins over this file. Do not re-litigate locked decisions (the name, the reader, the arc); pick up the active task.

**The arc is partner first, system as destination (re-anchored 2026-06-29).** The first posts build a creative partner (brainstorm + interview the agent into your taste); the **system framework** (spec it, test it, version it, gate it) is the destination they earn, not the front door. [`2026-06-28-pivot-prompts-to-systems.md`](2026-06-28-pivot-prompts-to-systems.md) is now read as **evidence** (its insight that isolated techniques are commodity is true and feeds the destination), not as the masthead. Do not lead with the framework, and do not default back to "hand out a prompt / teach a technique." Lead with the partner and the demo.

## 1. The voice chain is mandatory

Every post, the manifesto, and the About page run through the chain, in this order. No skipping a stage, no reordering.

`substack-value-engine` → `storytelling-architecture` → `writing-voice-modes` (Sean Mode) → `writing-critique` → `writing-humanity-pass`

- **No em dashes.** Ever. The humanity pass enforces it; do not let any in upstream.
- **Dive-bar grit stays.** That is the humor and the style, non-negotiable.
- **Anti-hype always.** The fastest way to lose a skeptic is to sound like an AI hype-bro.
- **The ask lands sideways.** The reader promise is the headline; "look what I built" repels the artist.

(Image generation and the voice-modes skill run on the Mac, not inside Cowork; the sandbox is firewalled off the image APIs.)

## 2. Positioning guardrails (from the 2026-06-22 discovery run)

These are the traps the research surfaced. Hold the line:

- **Empathetic-believer stance.** "I know exactly why you bounced. You quit one step early. Here is the step." Never scold, never preach.
- **Never lead with the abstract premise.** "Soulless output" and "you won't be replaced" are already-claimed angles (Nate Jones owns both). Lead with a concrete demo, every time. The demonstration is the moat, not the thesis statement.
- **One craft lane per post.** Demo in one discipline. Do not sprawl.
- **Do not lump the failure modes.** A technical glitch, an off-brand tone, and philosophical soullessness are three different problems with three different fixes. Each is its own post. Conflating them is the gap the whole field falls into; we don't.
- **The whitespace question is the method:** "Does feeding the model your references and taste kill the AI look?" Nobody is answering it. Answering it, by showing it, is what Pencil & Prompt is for.
- **Lead with the partner and the demo; the system is the destination (re-anchored 2026-06-29).** "Differentiate, never duplicate" has teeth: the isolated technique/prompt lane is saturated and commodity, so a post whose only takeaway is a free-elsewhere prompt is value-gate-blocked (it already blocked the old flagship how-to). But the answer is not to lead with the framework. Lead with building the partner (brainstorm + interview the agent into your taste) and the live demo; the system (spec/test/version/gate) is where the arc *leads*, earned over the partner posts. The moat is the taste-transfer method, not the architecture diagram.

## 3. The value gate (hard block)

Before a post is worth writing, `substack-value-engine` must clear two slots:

- **Itch:** the problem must be *genuinely Sean's*, not a pain borrowed off a forum. The discovery brief pre-fills candidate Itches from real evidence; verify each one is actually his before building on it.
- **Solution:** must be a *real artifact* — an actual run, an eval, a before/after, a number, a captured transformation. Never hand-waving, never "here's how you could." If there is no real artifact, the gate blocks and the angle waits until Sean has done the work.

The capture of the real work is the post. Write from the build, not after it.

## 4. Demo in Sean's lane; teach a method that travels; ship both tiers

Demonstrate in animation, writing, or visual design, where Sean has provable taste. Then strip the lesson of its craft so a musician or copywriter can run it on theirs. The demo is specific; the method is universal. **Tools ship in two tiers, every time (revised 2026-06-29):** a copy-paste kit so anyone can start in the tool they already have, AND the symlinkable `.claude` skill for the reader ready to level up. Teach the why and how of the technical layer; do not wall the reader off from it. The non-coder is the on-ramp, not the ceiling. (Masthead rationale: SOUL.md §3-4.)

## 5. Privacy and repo rules

This folder rides **code-brain's public repo.** Treat everything tracked here as published.

- **Never** write personal, employer, prior-role, job-hunt, financial, medical, or contact data into a tracked file. See code-brain CLAUDE.md **Rule #10**.
- Anything sensitive goes in the gitignored **[_private/](_private/)** lane and stays there. Never move it up without a privacy pass; never weaken the `.gitignore` rule that covers it.
- **Never `git add` / `git commit` the vault.** The Obsidian-Git plugin owns vault auto-commit (code-brain CLAUDE.md Rule #8).
- Competitive/white-space analysis is fine in public (it is not personal data). The line is personal and employer material.

## 6. Skills map

| Step | Skill |
|------|-------|
| Mine real reader pain into ranked angles | `fusion-discovery-council` (costed; `--lens substack`), `last30days` (fresh complaints) |
| Value gate (start the chain) | `substack-value-engine` |
| Shape the narrative | `storytelling-architecture` |
| Voice it (Sean Mode) | `writing-voice-modes` |
| Red-team the draft | `writing-critique` |
| Final scrub (kills em dashes + AI tells) | `writing-humanity-pass` |
| High-variance critique (optional) | `llm-council` |
| Hero image (pencil-test house style, on the Mac) | `openai-image-gen` (primary), `gemini-image-gen` |

The chain skills are symlinked under `.claude/skills/` and resolve to code-brain's canonical copies. Naming is done; do not re-run `pm-marketing-growth:product-name`.

## 7. Brainstorm method

When scoping anything (the editorial queue, the manifesto angle, sequencing), use `superpowers:brainstorming` and ask one question at a time. That is how this project was built, and it is working. Generate breadth before converging; pressure-test every idea against *"why is this Sean, not a template?"*

## 8. The writing workflow (proven on Start Here + About, 2026-06-27)

The reliable loop for any Pencil & Prompt piece, page or post. Use it by default.

**Stage 0 — Deep-research pre-flight (never skip; added 2026-06-27).** No post gets slapped together. Before brainstorming the shape, run five checks (scaled to the post) so the piece earns the reader's time:

1. **Pain / demand** — is the itch real and genuinely Sean's? Use the `fusion-discovery-council` ledgers + the discovery synthesis; mine fresh pain if the lane is uncovered.
2. **Competitive read** — how is this already covered, and where is the gap? Search the **Executive Circle MCP** (Nate Jones's archive) + the web for the closest comparable, and name what we do that they don't. Differentiate, never duplicate. (Nate owns "taste" + "you won't be replaced" + commercial-image *precision*/JSON; we own the soulless→soul demo for a *personal* style. Lead with the demo.)
3. **Craft accuracy** — is our how-to current and actually correct? Tools/models move monthly; verify the technique by web search so we never teach a stale or wrong move.
4. **PM lens** — run at least **jobs-to-be-done** ("what is the reader hiring this post to do?") + a quick **red-team / pre-mortem** ("what makes this feel slapped together or fail?"). Reach for other PM skills (`pm-execution:red-team-prd`, `pm-product-strategy:value-proposition`, `pm-product-discovery`, `honest-thinking-partner`) when a post needs more angles.
5. **Value gate** — only proceed when the Itch is real and the Solution is a real captured artifact (§3). The capture is the post.

Capture the pre-flight findings (with sources) at the top of the piece's working doc, so the draft is built on them. Then the writing loop:

1. **Brainstorm the shape first** (`superpowers:brainstorming`): one question at a time, lock a short skeleton (structure, length, tone dial, the opening line, the closer) BEFORE drafting. No draft until Sean approves the shape.
2. **Run the voice chain** to write it: `substack-value-engine` → `storytelling-architecture` → `writing-voice-modes` (Sean Mode) → `writing-critique` → `writing-humanity-pass`.
3. **Sean hand-rewrites.** The chain draft is a strong starting point, never the ship. Sean's edits are the real voice (on Start Here and About, his rewrites were the decisive lift).
4. **Fold Sean's rewrite back into** `.claude/skills/writing-voice-modes/references/voice-samples.md` as a calibration anchor, so the next piece starts closer to his voice.
5. **Mechanical proofread only** on the final (apostrophes, escapes, em dashes); prose untouched.

Optional, for a high-variance take: the **LLM Council** can write parallel blind versions and a chairman synthesizes (premium profile), then the synthesis runs through the same chain. Keep council and superseded drafts in `pages/_council/` + git history; never clobber the canonical file.
