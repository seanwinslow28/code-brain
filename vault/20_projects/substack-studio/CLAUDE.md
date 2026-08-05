# CLAUDE.md — Pencil & Prompt (substack-studio)

The operating manual for any session working in this folder. Rules here are standing law. The strategy they enforce lives in the spec.

## 0. Read first, every time

**[SOUL.md](SOUL.md) before any work, it is the masthead.** "The models got good, now everything they make is the same; push the agent past the median and publish what actually happened." Then [POSITIONING-AND-EDITORIAL-SPEC.md](POSITIONING-AND-EDITORIAL-SPEC.md) for the strategic detail (the reader, the verified white space, the six territories, the voice, the value model, the relaunch plan), and [SERIES-COMMAND-CENTER.md](SERIES-COMMAND-CENTER.md) for the running order. If anything here disagrees with SOUL.md, SOUL.md wins; the spec wins over this file. Do not re-litigate locked decisions (the name, the subtitle, the two series, the protocol-before-Rung-1 order); pick up the active task. Decisions and verbatim reasons live in the partner-session sidecar (locks L1-L7); the session order lives in [REVAMP-2026-08-05-SESSION-MAP.md](REVAMP-2026-08-05-SESSION-MAP.md).

**The unit of work is the Expedition (refocused 2026-08-04).** A Building the Ladder rung = one real job, the median shown (~20-run census), ONE named divergence mechanism run against it, the contrast captured, the mechanism shipped both tiers into the library with an honest verdict (beat / tied / lost, public retractions per the Graveyard policy). Raising Agents episodes are the sibling series (funny true fleet stories with a navigation lesson). The territory set (d1-d6) is a LOOSE lock: build sessions may surface reshapes, and reshapes route back to a partner-session reconvene, never silently. The taste-transfer era (partner-then-system arc, Take Two, Back to Basics) is retired; its material is quarry in [_archive/](_archive/).

## 1. The voice chain is mandatory

Every post, the manifesto, and the About page run through the chain, in this order. No skipping a stage, no reordering.

`substack-value-engine` → `storytelling-architecture` → `writing-voice-modes` (Sean Mode) → `writing-critique` → `writing-humanity-pass`

- **No em dashes.** Ever. The humanity pass enforces it; do not let any in upstream.
- **Dive-bar grit stays.** That is the humor and the style, non-negotiable.
- **Anti-hype always.** The fastest way to lose a skeptic is to sound like an AI hype-bro.
- **The ask lands sideways.** The reader promise is the headline; "look what I built" repels the reader.

(Image generation and the voice-modes skill run on the Mac, not inside Cowork; the sandbox is firewalled off the image APIs.)

## 2. Positioning guardrails (from the 2026-08-05 research round)

These are the traps three independent research passes surfaced. Hold the line:

- **The mechanism is the commodity; the verdict is the product.** Free equivalents cover the mechanism in five of six territories and publish an evaluation in zero. A post whose deliverable is a technique competes with GitHub; a post whose deliverable is a tested verdict on a technique competes with nobody. Every rung ends in a verdict; no verdict, not done.
- **State the library claim precisely, always:** "no prompt or technique library publishes per-entry tested verdicts against a published measurement protocol." Broad versions ("nobody tests", "nobody admits failures") are falsifiable: Nate Jones already publishes one-off tested verdicts with honest failures. The differentiator is CUMULATION (per-entry, versioned, retractable, against a published protocol), not testing posture.
- **Never lean the masthead on the "stickiness" number.** The persistence effect (d = 0.414) rests on 2 studies with a null moderator test. It is an open question or a future rung, never masthead support. The defensible task-type framing: convergence is strongest on constrained, real-work ideation (d = 0.70) and negligible on free-form play (d = 0.12).
- **Banned figures:** the $2.51B market size and the 10-30x diversity claim (both trace to vendor SEO). The 91%/82% heterogeneous-debate figure is Hegazy 2024 (arXiv 2410.12853) and must always carry its 2024-era-models vintage.
- **Cite only from the tier-audited syntheses**, never raw DR grounding URLs. Every published figure resolves to its primary source first; `agents-sdk/scripts/audit_dr_citations.py` is the standing pre-citation step. The contaminated T3 (Input Axis) discovery ledger is not citable; the reframed ~$1.50 re-run gates any d4 pain claim.
- **Territory rules with teeth:** a d3 draft whose takeaway is "add constraints" gets killed. d1 Cartography is the instrument inside posts, never a standalone beat (Wikipedia owns the free field guide; visual-tell claims are currently unevidenced). The folklore rung (temperature, "think outside the box") sells on protocol and scale, not surprise (a free Medium experiment already published the n=20 version).
- **Never lead with the abstract premise.** "AI makes everything samey" is a universal observation and a claimed angle. Lead with the captured experiment, every time. The capture is the moat, not the thesis statement.
- **One job per rung.** One real job, one named mechanism. Do not sprawl.
- **Empathetic stance, re-pointed.** The reader's skepticism about AI advice is correct; most of it is folklore and some of that is now measured. Never scold, never preach, never hype. And never ship the industry default this publication exists against: "here's a prompt, I never reported back."

## 3. The value gate (hard block)

Before a post is worth writing, `substack-value-engine` must clear two slots:

- **Itch:** the problem must be *genuinely Sean's*, not a pain borrowed off a forum. The discovery brief pre-fills candidate Itches from real evidence; verify each one is actually his before building on it.
- **Solution:** must be a *real artifact* — an actual run, an eval, a before/after, a number, a captured transformation. Never hand-waving, never "here's how you could." If there is no real artifact, the gate blocks and the angle waits until Sean has done the work.

The capture of the real work is the post. Write from the build, not after it.

## 4. Demo in Sean's lane; teach a method that travels; ship both tiers

Run the Expedition on real jobs from Sean's own lanes (animation, writing, visual design, the fleet itself), where the median and the escape are both provable. Then strip the mechanism of its craft so a musician or copywriter can run it on theirs. The demo is specific; the mechanism is universal. **Mechanisms ship in two tiers, every time (rule survives the refocus):** a copy-paste kit so anyone can start in the tool they already have, AND the symlinkable `.claude` skill for the reader ready to level up. Teach the why and how of the technical layer; do not wall the reader off from it. The non-coder is the on-ramp, not the ceiling. (Masthead rationale: SOUL.md §4; catalog: [SKILL-PACKAGING-PLAN.md](SKILL-PACKAGING-PLAN.md).)

## 5. Privacy and repo rules

This folder rides **code-brain's public repo.** Treat everything tracked here as published.

- **Never** write personal, employer, prior-role, job-hunt, financial, medical, or contact data into a tracked file. See code-brain CLAUDE.md **Rule #9**.
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
