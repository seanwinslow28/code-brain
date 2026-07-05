---
type: discovery-synthesis
post: take-two-01-teach-the-model-your-hand
created: 2026-06-28
status: decision-pending
purpose: "Fresh user-pain discovery (5 streams, mid-2026, dated + cited) → the true pain point, what NOT to build, and the recommended post-that-ships-a-tool."
target_output: "Both: a post that ships a tool (Sean's call, 2026-06-28)"
related:
  - "matrix-results-scored.md"
  - "likeness-lock-style-logic-research-and-scaffold.md"
---

# True pain + opportunity map

## TL;DR

The hypothesis held, strongly and from five independent angles. **The true, current, loudest pain is fidelity-under-control: there is no controllable, repeatable dial for how much of you survives a transformation.** You get a binary cliff (faithful-but-flat, or stylish-but-a-stranger), the field's actual "fix" is shouting DO NOT CHANGE FACE in caps, and every extra edit compounds the drift.

Recommended play, given you chose "a post that ships a tool":
- **The post:** "Teach the model your hand," re-aimed around the dial. Likeness is free now; *control* is the craft. Your 12-style gallery is the demo of finding the dial per style.
- **The tool (v1):** an **Identity-Lock + Drift-Catcher** skill, the productized version of anima's critic-gate + Character Bible. It is the one opportunity that sits in real whitespace AND is your unfair advantage. The post literally narrates the tool doing the thing you just did by hand.

## The evidence convergence (5 streams, one pain)

Every stream, run mid-2026 with dated sources, pointed at the same core.

1. **Identity-vs-stylization complaints.** The loudest, most cross-platform, most recent gripe: "the edited face wasn't mine, it was a weird cousin I never met." The fix circulating is identity-lock prompting in ALL CAPS, which is itself proof no real control exists. The denoising literature states the tradeoff outright: low strength = no style, high strength = a different person, and a paper confirms high denoising destroys the high-frequency detail identity rides on. Midjourney's own docs admit stylize and likeness "compete for influence." (PerfectCorp, 2026-03-05; Stable Diffusion Art + arXiv Diffusion Prism, 2025-01; Midjourney Omni docs.)

2. **Wish-this-existed.** Cross-cutting thesis from the unmet-needs scan: the loudest repeated want is "keep it believably mine/this, exactly, every time, at a quality that survives a close look." Identity drift + consistency + personal-style reliability + texture realism are facets of one missing thing: a dependable, reusable identity-and-style lock. (Storyflow 2026; Perfect Corp 2026-03-05.)

3. **Believable world/era insertion (the Forrest Gump effect).** Base capability is commoditizing fast (Nano Banana Pro, Flux Kontext, Sora/Veo). The ownable gap is the judgment layer: identity-lock across an iterative composite (drift), era-correctness (anachronism is a reasoning gap nobody gates: AI Rome had 4-wheel chariots and a 1911 monument), and translating "make it look real" into actual key/fill/shadow-direction/grain prompts. (futurepedia, 2025-12-30; France24, 2025-12-16.)

4. **Character consistency.** A commoditized red ocean. Single-face consistency is solved and free; listicles-of-listicles and a first-party feature on every model confirm saturation. Whitespace migrated to the hard edges: long-series + multi-character at scale (an honest "85% ceiling"), wardrobe/prop as a separable lock, consistency that survives editing AND motion, and crucially **expressive/animated** consistency (the leader's named weakness is "dead, rigid, no squash-and-stretch"). That last one is your pencil-test domain. (theneuralpost 2026-01-28; toonystory 2026-04; gensgpt 2026; magichour 2026.)

5. **Workflow toil → skill/plugin.** The recurring loop, verbatim across dev forums: hand-author a locked identity/style description, re-paste it every prompt, re-roll and eyeball for drift, escalate to a per-character LoRA, cull a 40-to-100 batch down to ~5 keepers, hand-assemble comparison grids. Every model update resets the work. The under-served seam is the taste/orchestration loop on top of capable engines; the thinnest-served category is exactly "anchor → batch → catch drift → propose fix." (community.openai.com 2025-04-18 and 2026-06-14; indiehackers 2025-11-18.)

## What NOT to build (the crowded zones)

- **Another single-face consistency wrapper.** Red ocean. Every model ships it; dozens of SaaS wrappers and a mature open-source stack already exist.
- **A raw "historical selfie" generator.** The one-shot consumer trend output (Nano Banana "me in a Renaissance painting") is already good enough to go viral. The model is not the gap.
- **A model-level "dial."** The vendors are racing toward this and gpt-image-2 exposes no seed or fidelity knob anyway. Do not promise a parameter; own the *workflow* that simulates the dial and stays useful as models improve.

## The true pain point (stated)

> Likeness is free now. Control is not. There is no controllable, repeatable way to say "keep 70% me, go 100% woodblock" and get it reliably, again, across a set. You get a cliff, not a dial, and every edit erodes you further.

Your hand-run matrix already proved the consumer half of this: likeness scored 2/2 across all 12 styles, and the whole spread was in whether a deliberate hand survived. The pain is not "it cannot render me." It is "I cannot *control how much of me* survives, repeatably."

## Recommended play: a post that ships a tool

### The post (re-aimed)
"Teach the model your hand," but the lesson is the dial, not the complaint. Spine: I taught it my face, it nailed the likeness instantly (likeness is free), then I pushed 12 styles by hand to find where "me" survives the weirdness, and that manual loop was real toil. Here is the dial, and here is the skill that runs it for you. The gallery (anchor → pushed variations, straight to strange) is the demo; the scored matrix is the proof; the skill is the gift.

### The tool, v1: Identity-Lock + Drift-Catcher
The productized version of what you already built in anima.

- **Input:** 1 to 3 anchor images + a likeness-lock spec (the five identity markers, your sean-anchor block) + a swappable style-logic block + a shot/style list.
- **Process:** assembles the reference bundle, fans out N generations, auto-diffs each output against the anchor on the named identity markers, flags the ones that drifted, and proposes the corrective prompt diff. The "dial" is a target identity-retention level the verify-loop enforces by re-rolling until it passes.
- **Output:** an on-model set + a drift report (pass/fail per frame + the exact fix appended).
- **Packaging:** non-coder-runnable (a skill / GPT / hosted thing), per the tool-shipping-playbook. Never "clone this repo."

### Why this is your unfair advantage
This is a near-direct lift of the anima pattern: the likeness-lock is the Character Bible identity block, the drift-catcher is the T1 rule gate + T2 vision critic that "proposes prompt diffs, not pass/fail," and the dial is the draft-to-pro / retry-ladder discipline. You have a working reference implementation of the exact judgment layer the whole field is missing. Commodity models get better underneath it; the critic layer stays valuable. That is the moat.

## Honest risks / caveats

- **The dial is what the field is racing toward.** Frame it as a workflow that survives model upgrades (the critic layer), not a model feature you invented.
- **gpt-image-2 has no API knobs / no seed.** v1 is prompt-orchestration + a verify loop, not real parameters. Be honest about that in the post; it is also why the toil exists.
- **Scope creep.** World-insertion (era-check + lighting-match) and multi-character-long-series are bigger judgment-layer products. Tempting, but v1 should be the single-subject dial + drift-catcher. The others are the roadmap.
- **The auto-diff needs to actually work.** Identity-similarity scoring across hard style changes is non-trivial (DINOv2/CLIP have known limits, which anima already documented). v1 can lean on a vision-critic read ("is this still him, on these markers") rather than a brittle metric.

## Open decisions (for convergence)

1. **Tool v1 scope:** confirm Identity-Lock + Drift-Catcher as the build, versus the batch-cull keeper-picker or the believable-insertion judgment pipeline.
2. **Post demo anchor:** the style-range museum gallery (recommended, you already have it), world-insertion as a second act, or both.
3. **Next artifact:** a PRD for the tool, or a re-aimed beat skeleton for the post, or both in parallel.

## Sources (strongest dated)

- PerfectCorp, "Stop ChatGPT from changing your face," 2026-03-05: https://www.perfectcorp.com/consumer/blog/generative-AI/chatgpt-face-change
- Apiyi, Nano Banana Pro quality decline, 2026-04: https://help.apiyi.com/en/nano-banana-pro-quality-decline-april-2026-analysis-en.html
- Stable Diffusion Art, denoising strength: https://stable-diffusion-art.com/denoising-strength/ ; arXiv Diffusion Prism, 2025-01: https://arxiv.org/pdf/2501.00944
- Midjourney Omni Reference docs: https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference
- theneuralpost, "character consistency is finally solved," 2026-01-28: https://theneuralpost.com/2026/01/28/nano-banana-vs-the-world-why-character-consistency-is-finally-solved/
- toonystory, best AI for character consistency, 2026-04: https://toonystory.com/blog/best-ai-for-character-consistency-2026
- gensgpt, character consistency guide (85% ceiling), 2026: https://www.gensgpt.com/blog/character-consistency-ai-image-generation-2026-guide
- futurepedia, realistic composites with Nano Banana, 2025-12-30: https://newsletter.futurepedia.io/p/make-realistic-composite-images-with-nano-banana-12-30-2025
- France24, AI reconstructions of ancient Rome full of errors, 2025-12-16: https://www.france24.com/en/technology/20251216-ai-generated-reconstructions-ancient-rome-errors
- OpenAI community, character consistency / style-locking, 2025-04-18: https://community.openai.com/t/need-for-character-consistency-and-style-locking-in-image-generation/1232362
- OpenAI community, gpt-image-1 deprecation breaks visual identity, 2026-06-14: https://community.openai.com/t/gpt-image-1-deprecation-may-break-the-visual-identity-of-my-game-project/1383707
- Indie Hackers, AI product-photo tool (2-3 hrs/shot), 2025-11-18: https://www.indiehackers.com/post/launched-an-ai-product-photo-tool-after-being-frustrated-with-existing-solutions-79483e1625
- magichour, AI video consistency is still broken, 2026: https://magichour.ai/blog/ai-video-consistency-character-face-tools
