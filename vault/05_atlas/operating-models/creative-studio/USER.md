---
type: operating-model
artifact: USER
domain: [creative-studio]
status: draft
last_interviewed: 2026-04-20
created: 2026-04-18
review-date: null
ai-context: "Sean's recurring decisions and prioritization patterns for creative work. Default mode is excitement-driven with a 90/10 delegation ratio (agents do the bulk, Sean owns voice and final polish). Consumed by daily-driver, process-inbox, sprint-health."
---

# USER — Creative Studio

## Decisions Made 3+ Times Weekly
- **Where/how to apply autoresearch.** Current uses: improving ComfyUI workflows, sharpening prompts and Skills. Open question: what else can autoresearch unlock for creative pipelines? Brainstorm candidate down the line.
- **Is this skill-worthy?** When something's nailed down or I see Claude can carry it across projects, pack it into a Skill so multiple skills can chain into a full pipeline (the "ultimate creative studio" target).
- **Which Nano Banana 2 concept/style wins this scene?** For the active portfolio short, picking a visual direction from a batch of concept renders at `sw-portfolio-animation-pipeline/runs/act2-exploration/concepts`. This "post-moodboard storyboard" step is becoming a pipeline staple.
- **Is this render good enough, or re-queue?** — ongoing frame-by-frame quality call.

## Real Prioritization Criteria
_(Messy is fine.)_
- **Highest dopamine / most fun** is the default winner when multiple threads compete.
- **Inspiration beats everything.** A new tool or workflow (e.g., Seedream 2.0 walk-cycle test) can pull me straight into a project that was otherwise cold.
- **Protective pivoting:** if a project is going stale, pivot to another creative thread. Prevents the "sick of it, rush-to-finish" failure mode that's burned me before.
- **Close-the-gap rule:** when something's close to done, prioritize finishing it.
- **June 11 deadline** for portfolio short is the one hard timeline — doesn't always win day-to-day, but tightens as the date nears.

## Auto-Yes
- Any tool/workflow that might solve character consistency for 2D animation.
- Workflow tutorials from trusted creators.
- Saturday/Sunday implementation sprints.
- **Testing the latest/greatest image-gen models regardless of LoRA availability.** Nano Banana 2 and GPT Image 1.5 proved closed-source generalists beat outdated specialist workflows. Z-Image, ERNIE, and similar get tested on their own merits — no "no pixel LoRA, therefore skip."

## Auto-No
- Festival submissions right now — not until 2D animation pipeline output clears my quality bar.
- Workflows that require xformers / non-SDPA on the RTX 5080.
- Overnight batch runs on unproven workflows (cf. the 150-garbage-output autoresearch burn).
- **Old ComfyUI LoRA / SDXL sprite-sheet workflows** — hours of LoRA/SDXL iteration that only ever produced subpar outputs. We've moved past that era; don't re-enter the tar pit.
- _Not auto-no:_ Wan 2.5. Cheaper than Seedance 2.0 / Kling / Veo 3.1, worth testing. Just don't run multi-hour experiments without a proven workflow.

## Daily Investment Heuristic
- **Default at 3 PM:** whatever I'm most excited about right now.
- **Sometimes:** whatever unblocks weekend implementation (synthesize-then-implement pattern — how `16bitfit-battle-mode` began after the Boston move).
- **Low energy / burnout:** watch YouTube, read articles, browse GitHub repos for useful things for future projects. Don't force building.
- **High energy:** build.

## Agent Delegation
**Already trusted to agents:**
- Brainstorming + concept exploration.
- Information gathering and research synthesis.
- Organization / vault work.
- Concept generation and variant prototyping.
- Scaffolding Skills and workflows.
- Style-locked image generation once a Skill encodes the style (e.g., `gemini-pencil-animation-image-gen`).

**Never delegated:**
- Final frame judgment.
- Story / script decisions.
- Creative taste and the final-10% polish pass.
- Which tool/model to adopt into the core pipeline.

**Target ratio:** agents carry ~90%, Sean owns establishing voice/goals/vision/concepts/storylines up front and the final 10% polish at the end.

## Tiebreakers When Unsure
- **Burned out / low-signal:** sleep on it, revisit tomorrow.
- **Direction unsure:** prototype multiple concepts or variants. Step back and see which one actually feels right.
- **When a direction wins:** lock it into a Skill so Claude can reproduce that style on demand (pattern: image of inspiration → prompt iteration in Nano Banana 2 → Skill).

## Definition of "Done" in This Domain
- **For a final creative output (render, short, etc.):** "I'd show this publicly without caveats." Measured by the step-back test — does it feel cohesive, does it make me smile? Self-criticism is always present (there's always a flaw, a better joke, a better story choice), but when it works as a whole, it ships and I move on to the next.
- **For a pipeline/workflow/Skill:** softer bar — works reliably enough to be reused across projects without re-explaining. Pipelines are "done for now"; finals are "done."
