---
type: operating-model
artifact: operating-model
domain: [creative-studio]
status: confirmed
last_interviewed: 2026-04-21
created: 2026-04-18
review-date: null
ai-context: "Synthesized operating model for creative-studio. One-file summary to load at the start of any creative-domain work. Active focus: 2D animation pipeline (sw-portfolio-animation-pipeline) targeting a portfolio short before June 11. 16BitFit is paused. Solo practice. Vault-as-SSoT is the active infrastructure build."
---

# Operating Model — Creative Studio

## TL;DR
Solo creative practice. Active focus is the 2D animation pipeline (`sw-portfolio-animation-pipeline`) — target a portfolio short before June 11 travel — with 16BitFit paused until the pipeline is dialed in. Weekday afternoons are research mode, weekends are implementation, and every nailed-down workflow gets packed into a Skill. Claude is the only collaborator; creative taste stays with Sean (90/10 delegation split). The biggest active build target isn't a creative output — it's turning the Obsidian vault into a real agentic SSoT so the fleet actually works in this domain.

## Identity in This Domain
Sean as creative — 2D animator in training, filmmaker, pixel artist, writer, founder of the paused 16BitFit project. Career-transition arc from PM to animation producer is present but not gated on anything yet; no festival submissions until the pipeline clears his quality bar. Creation is solo by design — past collaborations produced frustration + creative differences, and AI amplified the preference for solo work. Storytelling skews comedic, aesthetic target is "made by a 2D animation studio" (classic Disney / 90s Nick / Cartoon Network, or modern Wacom/iPad hand-drawn).

## Operating Rhythm Summary
Block work runs until ~3 PM; creative-studio picks up in the afternoon/evening in **research mode** (AI tool scouting, 2D animation principles, moodboards, agentic-workflow reading). Weekends are **implementation mode** — the week's research gets applied. Render-waiting time is for context-switching to other projects, errands, or more research — not overnight batching (the 150-garbage-output autoresearch incident is the policy). No calendar-enforced sacred block; the only rule is "do something creative every day." Seasonally: Boston winter yields more indoor hours; summer shifts reliance to agent autonomy. Creative communications run on `sean.winslow28@gmail.com`, never `swinslow@theblock.co`.

## Decision Pattern Summary
Default prioritization is **highest dopamine / most fun**, with protective pivoting when a project starts to feel stale (respect the 16BitFit-V3 "grinding past enjoyment" signal). Inspiration beats plans — a new tool or workflow can pull the whole day into an unplanned thread, and that's fine. Auto-yes: tools that solve character consistency, weekend implementation sprints, **the latest/greatest image-gen models regardless of LoRA availability** (Nano Banana 2 / GPT Image 1.5 disproved the "needs a specialized LoRA" assumption). Auto-no: festivals right now, xformers on the 5080, overnight batches on unproven workflows, old LoRA/SDXL sprite-sheet workflows. Agents carry 90% (brainstorming, research, concept generation, Skill scaffolding, style-locked image gen); Sean owns voice/story/final-frame judgment. Tiebreakers: burned-out → sleep on it; direction-unsure → prototype multiple, then lock the winner into a Skill. "Done" for finals = "I'd show this publicly without caveats" + the step-back test makes me smile.

## Dependency Map Summary
**Solo practice — Claude is the only collaborator dependency.** Hard-dependency tools: Claude Code + skills, Adobe Creative Suite, Procreate (iPad). Heavy-use staples: ComfyUI, Remotion, Adobe MCP, Obsidian vault, Pencil (.pen), autoresearch, NotebookLM, Google AI Studio, Gemini + Perplexity Deep Research, Google Antigravity IDE (replaces Cursor). Model staples: Nano Banana 2 + Pro (image), Seedance 2.0 (video). **Three-machine topology is not a single point of failure** — Mac Mini (primary + 6 SDK agents), MBP (travel + intermittent Qwen3-14B), Alienware (RTX 5080 — the beast for ComfyUI and heavy renders). Any machine can carry the others' load, just slower. No single SSoT for creative work today — the Vault is the planned target. Nobody else depends on Sean's creative output on a cadence; no external deadlines beyond the self-imposed June 11 portfolio-short target. Current self-blocker queue: finishing the three-domain operating-model interviews.

## Institutional Context Summary
Project vocabulary comes from `sw-portfolio-animation-pipeline`: **Pencil Test (PT)**, A-2 Anchor, HF01–05 / SF01–05 / CC01–08 audit codes, Retry Ladder, Phase A-E, the "Seedance finds the motion, NB2 protects the aesthetic" philosophy, and the project's Engine Truth ("if it plays smoothly at 12fps and the character is recognizably Sean on cream paper, it ships"). Canonical reference skills: `2d-animation-principles`, `animation-pipeline`, `creative-director`, `gemini-pencil-animation-image-gen`, `image-generator-prompt-science`, `script-writing`, `writing-voice-modes`, `autoresearch`. Communication rules: **challenge Sean with alternatives, stop challenging once he commits, call out known-broken approaches, always do extensive research, be a creative partner not just an executor**. Oracle sources Sean actually trusts: Nate B. Jones (agentic AI), Matt Wolfe (creative AI news), AI Search (ComfyUI + OSS), Alex Grigg (2D animation), The Dive Club (UI/UX), Karpathy's autoresearch, Richard Williams' *Animator's Survival Kit*. Pinned landmines: stale ComfyUI workflow proposals, the 150-garbage-output autoresearch incident, xformers on 5080, old LoRA/SDXL sprite-sheet rabbit holes. Sacred cows added beyond the obvious: **always be willing to pivot, create for ourselves, enjoyment is non-negotiable, take risks**.

## Active Leverage Points
- **Pack nailed-down workflows into Skills.** Pattern already works (`gemini-pencil-animation-image-gen`). Chaining Skills is how Sean scales the "ultimate creative studio."
- **Test the latest/greatest generalist models on merit** instead of waiting for specialized LoRAs. Signal for what's worth testing: open-source models being directly compared to Nano Banana 2 / GPT Image 1.5 / Seedance 2.0.
- **Post-moodboard concept batch step** as a pipeline staple — generate a batch of Nano Banana 2 concepts, pick the visual direction, lock the winner into a Skill.
- **Claude Research Skill** — consolidate Perplexity API + Google MCP + NotebookLM MCP + Gemini Deep Research into one Claude-native research surface. Kills the #1 context-switch cost.
- **Obsidian vault as the agentic SSoT** — the extra-hour north star. Once agents can properly navigate, connect notes, and add to them, the whole creative studio unlocks asynchronously.
- **Weekly `last30days` run** to catch new tools without manual scouting.

## Known Bottlenecks
- **The agent fleet doesn't function in creative-studio today.** No MCP connections, no reliable machine-to-machine reach, bugs when they connect at all. Biggest build target.
- **Research-app ↔ research-app context switching** — currently the single most expensive friction.
- **Three-machine repo sync** — can't keep everything in parity without leaving all three on, and Obsidian Git on vault-only is still unresolved.
- **MCP re-auth every session** — a recurring time sink.
- **Adobe MCP setup cost** — high enough that Sean has deferred testing it.
- **Creative Skills split across two repos** (`claude-code-superuser-pack` and `sw-portfolio-animation-pipeline`) with no sync signal.
- **Vault synthesizer intermittent** — succeeds only when MBP is awake (Qwen3-14B dependency).
- **Handoff-prompt friction** — long threads require manual handoff drafting; no automated detection.
- **Alienware ICMP-blocked** — HTTP checks only, ping fails. Already in auto-memory.

## Cross-Domain Bleed
- **Into The Block:** rare — creative and Block are kept separate; the only regular bleed is Block-downtime flowing into creative time. Personal Gmail for creative is the dividing line.
- **Into Life Systems:** energy budget bleed — creative is high-dopamine and can eat into sleep or health routines; the career-transition arc to animation producer is technically Life Systems scoped but creative outputs are the currency that will eventually fund it.
- **From Life Systems into creative:** the June 11 travel deadline is a Life Systems fact driving the portfolio-short timeline. The Boston move / seasonal shift changes hours-available.

## Current Open Questions
- How should autoresearch be applied to creative work beyond ComfyUI workflow optimization and prompt/Skill improvement? (Raised in Layer 2.)
- When does the reusable 2D animation pipeline get extracted out of `sw-portfolio-animation-pipeline` into its own project? (Raised in Layer 3.)
- Can Obsidian run on the Alienware given the mac-only plugin errors previously encountered? If Vault is SSoT for all three machines, this needs solving. (Raised in Layer 5.)
- Does Phase 6 (`phase6-SUPER-PLAN-2026-04-17.md`) already deliver any of the Karpathy `llm-wiki` / `claude-memory-compiler` agentic vault navigation, or is it still to-build? (Raised in Layer 5.)
- How do we make MCP authorization persistent across sessions? (Raised in Layer 5.)
- How does the agent fleet actually reach Mac Mini / MBP / Alienware on-demand without requiring all three to be always-on? (Raised in Layer 5.)
- When does 16BitFit simplification start, and what's the scope? (Raised in Layer 1 — "we can circle back to that later.")

## Related Artifacts
- HEARTBEAT: [[HEARTBEAT]]
- USER: [[USER]]
- SOUL: [[SOUL]]
- Schedule rules: [[schedule-recommendations]]
- Active project (2D animation pipeline / Pencil Test): [[prj-animation-pipeline]]
- Paused project (16BitFit): [[prj-16bitfit]]
- Load-bearing workflow reference: [[ref-ai-animation-nb2-seedance-workflow]]
- Creative-studio MOC: [[moc-creative-studio]]
- Tier-0 identity: [[Sean-Winslow-Full-Personal-Context-v1.1|Full Personal Context]]
