# Discovery Synthesis, Web Supplement, and Ranked Backlog (2026-06-27)

Folds the six 2026-06-27 council runs (visual, writing, animation, losing-your-style, series/brand consistency, partner-upstream) plus the original 2026-06-22 "soulless AI creative output" run into one ranked Take Two / Fix My Mess / Notes backlog, and records the web-search pass that filled the gaps every run's blind-spot map flagged.

- **Council spend, 6 runs:** ~$7.76 total (A $1.21 · B $1.65 · D $1.32 · E $1.26 · C $1.17 · F $1.15), under the $10/day cap. Verification drop counts were low (0-2 per run), so the evidence held up.
- **Source ledgers:** the six `2026-06-27-*-idea-ledger.md` files + their `-brief.md` siblings in this folder.

---

## Part 1 — Web supplement (the "no stone unturned" pass)

Every run mined the *complaint* and almost none mined the *fix*. The recurring blind spots, verbatim across runs, were: no evidence on whether references / LoRA / fine-tuning / calibration actually solve it; no tool/model head-to-head; no current (2026) capability read; no success cases; little quantitative data. Those gaps are not incidental. They are the exact thing Pencil & Prompt exists to answer. So the web pass went after the **solution side, the mechanism, and the proof** rather than more pain.

### 1.1 The mechanism behind all of it (the thesis backbone)

The flattening is not a bug you prompt your way out of. It is what the model is built to do, and naming that is the spine of the whole publication.

- Generative models approximate the probability distribution of their training data and emit the *most likely* sequence, so repeated use converges on the average. This is **mode collapse**: intra-model (repeated samples converge on the same ideas) and inter-model (independently trained models converge on each other).
- A peer-reviewed result makes it concrete: generative AI **enhances individual creativity but reduces the collective diversity** of novel content. Working with AI makes one person's story better and everyone's stories more similar.
- Follow-ups find the homogenizing effect **persists despite prompt and parameter tweaks**, and that when AI is withdrawn, individual creative performance drops while homogeneity keeps climbing.

This is the "you quit one step early" reframe, proven: feeding it references gets you surface cues, then it drifts back to the mean unless you actively, repeatedly steer it off. Teaching it your taste *is* fighting the regression to the mean.

Sources: [Generative AI enhances individual creativity but reduces collective diversity (Science Advances)](https://www.science.org/doi/10.1126/sciadv.adn5290) · [Homogenization Effects of LLMs on Creative Ideation (C&C 2024)](https://dl.acm.org/doi/10.1145/3635636.3656204) · [Homogenizing effect of LLMs on creative diversity (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S294988212500091X) · [Could we see the collapse of generative AI? (Inria)](https://www.inria.fr/en/collapse-ia-generatives) · [AI-induced cultural stagnation (The Conversation)](https://theconversation.com/ai-induced-cultural-stagnation-is-no-longer-speculation-its-already-happening-272488)

### 1.2 Visual: the moves that actually hold a character/style (runs A + E)

The council said "no evidence reference/LoRA approaches solve it." The web says they partly do, and names the moves:

- **Identity anchoring beats prompting.** Midjourney V7's Character Reference / Omni Reference locks identity from images; the working recipe is 3-5 refs from different angles (front, three-quarter, full-body), Omni strength ~300-500 with `--cw 100`, and dropping the ref into the Style tab too to pin lighting/mood. Nano Banana Pro is repeatedly cited as the cheaper character-consistency winner (minimal face drift across scenes).
- **A LoRA can preserve real style, but only if trained on visual *logic*, not surface motifs.** The distinction practitioners draw: a good style LoRA preserves "the artist's visual decisions when facing subjects the artist never painted," not "classical clothing / exotic interiors" symbols. This is exactly your image-house-style rubric framed as training data: the constants (medium, construction lines, one accent, absurd caricature) are the *logic*, the scene is the variable.

Sources: [Midjourney consistent characters guide 2026 (PromptsEra)](https://promptsera.com/midjourney-consistent-characters/) · [Midjourney debuts consistent-character feature (VentureBeat)](https://venturebeat.com/ai/midjourney-debuts-feature-for-generating-consistent-characters-across-multiple-gen-ai-images) · [7 tools tested on 140 images (ToonyStory)](https://toonystory.com/blog/best-ai-for-character-consistency-2026) · [Consistent character generator guide (Apatero)](https://www.apatero.com/blog/ai-consistent-character-generator-multiple-images-2026) · [LoRA training: when to train vs reference (zsky)](https://zsky.ai/blog/lora-training-guide) · [How I train artist LoRAs: visual logic not style filters (Mariano, Medium)](https://medium.com/@Mariano_S/how-i-train-artist-loras-not-style-filters-but-visual-logic-5bb9449a0701) · [AC-LoRA: personalized artistic style (arXiv)](https://arxiv.org/abs/2504.02231)

### 1.3 Writing: voice calibration that works (run B) — and it is literally your VoicePrint method

The council flagged "no head-to-head, no longitudinal proof calibration sustains voice." The web converges hard on one method, which is the method you already built:

- **Feed examples, do not describe.** Voice profiles built from 3-5 of your best samples (1,500-3,000 words) reverse-engineer tone, vocabulary, sentence structure, and beat the hand-written "be witty and warm" description every time.
- **Extract a measurable Style Block + a negative list** (8-12 items) of words/moves you never use. Output as enforceable rules: sentence-length range, vocabulary patterns, structure habits.

That is `voiceprint-mine` + the cheese-bank negative list, validated by the wider field. Take Two #2 can demonstrate it against your own voice samples as the captured artifact.

Sources: [How to calibrate voice (Writer Help Center)](https://support.writer.com/article/250-how-to-calibrate-voice-for-your-content) · [Voice Pattern Prompts (Prompts Daily)](https://promptsdaily.substack.com/p/voice-patterns-prompts-how-i-get-ai-to) · [Train AI to write like you with custom instructions (Medium)](https://medium.com/@christianaistudio/your-ai-doesnt-know-your-voice-yet-here-s-how-to-fix-that-permanently-b17604ffebae) · [15 style corrections (WriteBros)](https://writebros.ai/resources/how-to-adjust-ai-writing-style-to-sound-natural)

### 1.4 Animation: the moves that fix drift and timing (run C) — anima's thesis, confirmed

The council flagged "no evidence any technique works at production quality." The web names the working pattern, and it is exactly anima's "the human owns timing, casting, keyframes":

- **Keyframe it, don't text-prompt it.** Move from text-to-video to first-frame / last-frame keyframing so the human defines the poses and the model only interpolates. Kling's "Bind Subject" / element reference plus 3+ multi-angle character images resolves the majority of face-drift complaints; Seedance 2.0 / Dreamina expose the same start-end workflow.
- **Drift's root cause is named:** each frame is a memoryless probabilistic sample with no persistent 3D model, so it "wanders away from the original design." Same root cause as the still-image consistency problem (run E #1: "no memory of a defined visual identity").

Sources: [Solving character inconsistency in Kling 3.0 (Atlas Cloud)](https://www.atlascloud.ai/blog/guides/solving-character-inconsistency-a-guide-to-kling-3.0-image-to-video-mode) · [Drift in AI video, explained (Kling)](https://kling.ai/blog/fix-ai-video-drift-consistency-guide) · [Kling O1 first-frame-to-last-frame (fal)](https://fal.ai/models/fal-ai/kling-video/o1/image-to-video) · [Start/end frame animation for creators (Dreamina)](https://dreamina.capcut.com/ai-video/ai-video-motion-for-creators)

### 1.5 The partner workflow + success cases (run F)

The council flagged "absence of evidence from users who successfully use AI as a brainstorming partner." The web has them, and the pattern matches your "talented intern" stance:

- **AI as an adversarial teammate, used upstream.** The working structure: ideate yourself first (avoid premature cognitive closure), then diverge/converge (Double Diamond), and make the model *ask you questions back* before it answers. The value is productive friction and volume in the divergent phase, with human judgment owning convergence.
- Co-creation studies report custom-GPT co-ideation measurably lifts designer creativity when framed this way (partner, not vending machine).

Sources: [From pattern-matcher to creative partner (Yuji Isobe, Medium)](https://medium.com/@yujiisobe/ai-can-supercharge-divergent-thinking-modern-ai-like-chatgpt-can-generate-a-high-volume-of-ideas-b37e24c380cc) · [Human-AI co-creation across design experience (Frontiers)](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1672735/full) · [Enhancing designer creativity through human-AI co-ideation (Cambridge, AI EDAM)](https://www.cambridge.org/core/journals/ai-edam/article/enhancing-designer-creativity-through-humanai-coideation-a-cocreation-framework-for-design-ideation-with-custom-gpt/BCC2CBE43EECE6F0D937BBC0D2F44868)

### 1.6 The one quantitative number worth quoting carefully

"Only 2% of AI output is ready to use without edits" (run F, angle 3) is a vendor LinkedIn stat, single-source, treat as illustrative not load-bearing. The credible quantitative spine is the academic homogenization work in 1.1, not the 98%-rework figure. (Same discipline the original run's blind-spot map asked for re: the "60-80% income drop" stat: cite the peer-reviewed diversity studies, flag the marketing stats as marketing stats.)

---

## Part 2 — The ranked backlog

Each Take Two now pairs a real, sourced **pain** (the soulless before) with a real, sourced **fix** (the move to demonstrate) and a **transfer** (the recipe). That pairing is the value gate cleared in advance. Ranked by flagship value and readiness.

### Take Two spine (ranked)

| # | Take Two | Lane | Pain (before) | Move to demonstrate (after) | Captured artifact | Runs |
|---|---|---|---|---|---|---|
| 1 | **Teach the model your hand** (flagship) | visual | Personal style collapses to the generic average; can't enforce a drawing style (A#4, A#2) | Anchor identity + name the rubric as visual *logic*, correct drift by drift | The mascot-creation run (publication's own face) | A, E, orig |
| 2 | **Write in your own voice** | writing | Blandification; "doesn't sound like me"; model substitutes its defaults (B#1, B#2, B#5) | Feed 3-5 samples → extract a Style Block + negative list (VoicePrint) | A voice-chain run on your own samples | B |
| 3 | **Keep a character alive across a whole series** | visual | No memory of a defined identity; consistency degrades as a series progresses (E#1, A#3, A#5) | Reference anchoring + style-lock across many outputs (Character Bible) | An anima Character Bible bake | E, A |
| 4 | **Make AI motion feel alive** | animation | Lifeless/linear motion, wrong timing, characters drift between shots (C#1, C#2, C#3) | Human owns timing: keyframe / first-last-frame, bind subject | An anima Seedance pass | C |
| 5 | **Use the intern upstream, not just at the end** | process | Generic, repetitive ideation you can't build on (F#1) | AI as adversarial partner: ideate-first, diverge/converge, make it ask you questions | A real brainstorm transcript (this project) | F |

### The thesis post / manifesto fuel (not a Take Two)

**"Fighting the regression to the mean."** The losing-your-style run (D, all 5 angles) + the mode-collapse mechanism (1.1) is the intellectual backbone, not a craft demo. It belongs in Start Here's whitespace claim and as recurring Notes, not as its own how-to post (no single craft job to demo). Lead with the demo, let this be the *why* underneath it. Maps to D#1 (references don't stop the revert-to-average) and D#3 (felt as a threat to authorship).

### Fix My Mess fuel (reader-fix format)

- **Brand systems not enforced** (E#3): hex codes, type, grid drift between mockups. Submit a botched on-brand asset, fix it live.
- **Clients reject AI prototypes as amateurish** (orig Angle 1): the "let a toddler design their app" cold open.
- **Content policy kills a campaign mid-stream** (E#5): brand-name prompt refusals.

### Notes seeds (reach/variety, from day zero)

- The quotables: "3 legs at some point of the video" (C#4), "she woke up and walked to the kitchen to make coffee" (B#1), "AI churns out decent images, but the moment you enforce a coherent stylization it falls apart into mushy averages" (A#4).
- The reframe, one Note at a time: mode collapse explained plainly = "you quit one step early."
- The false-positive anxiety cluster (B#3 accused of AI, A#6 hand work looks AI): real, relatable, good for engagement; a possible Fronkenschteen angle (defend a human artist accused of AI).

### Deliberately skipped (off-thesis / off-voice)

- Economic doom (orig Angle 6; income-drop): off-voice, no demo.
- "AI fundamentally can't feel / lacks a soul" (F#2): the doomer frame; we believe the opposite. Use only as a foil, never as a claim.

---

## Part 3 — Expanded discovery-angle map (all 7 runs → formats)

| Run (2026) | Tier | Top angles | Feeds |
|---|---|---|---|
| Soulless AI creative output (orig, 06-22) | standard | soulless / same-y / correction burden | spine thesis + Fix My Mess (Angle 1) |
| A · Visual / character (06-27) | standard | style can't be enforced; character consistency breaks | **Take Two #1** + #3 |
| B · Writing / voice (06-27) | standard | blandification; doesn't sound like me | **Take Two #2** |
| C · Animation / motion (06-27) | standard | lifeless motion, wrong timing, drift | **Take Two #4** |
| D · Losing your style (06-27) | deep | references don't stop revert-to-average | **manifesto / Start Here whitespace + Notes** |
| E · Series/brand consistency (06-27) | deep | no memory of identity; brand systems not enforced | **Take Two #3** + Fix My Mess |
| F · Partner upstream (06-27) | standard | generic ideation can't support narratives | **Take Two #5** (fresh thesis lane) |

**Net new vs the original run:** the original gave thesis-level pain ("AI is soulless"). These six give subject-level pain *paired with the fix*, across five demoable lanes, reframed toward makers who want it to work. That is the difference between "a take" and "a Take Two."
