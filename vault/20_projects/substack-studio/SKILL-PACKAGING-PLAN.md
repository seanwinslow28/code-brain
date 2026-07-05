# Skill-Packaging Plan (2026-06-29)
## The creative-skill set behind Pencil & Prompt

**Derives from** [SOUL.md](SOUL.md) §4-5 (both tiers; the formats) and the [tool-shipping-playbook](playbook/tool-shipping-playbook.md). **Aspirational model:** Matt Pocock's skills repo (small, composable, model-agnostic, organized by failure mode, "make them your own," shipped one-command, used as the newsletter's lead magnet). The good news from the asset audit: most of this already exists in Anima and just needs hardening, universalizing, and differentiating. We are not inventing a library from scratch.

---

## 1. The organizing principle (Pocock taxonomy, both tiers)

Two axes, borrowed from Pocock and adapted to creative work.

**Axis 1, who invokes it.**
- **User-invoked (orchestrators).** You type them. They run a session *with* you: interview, brainstorm, route, critique. These carry the partnership. (Pocock's `grill-me`, `to-prd`.)
- **Model-invoked (discipline).** The agent reaches for them automatically when the task fits. They hold reusable craft: a prompt framework, a critique rubric, animation physics. (Pocock's `tdd`, `domain-modeling`.)
- The rule Pocock enforces and we adopt: a user-invoked skill may call model-invoked skills, never another user-invoked one.

**Axis 2, the delivery tier (the both-tiers rule from SOUL §3-4).**
- **Copy-paste tier.** The skill's core as a paste-able prompt or kit for plain Claude/ChatGPT, no install. Every post ships this.
- **Skill tier.** The `.claude` skill, symlinkable, Pocock-style. Every post also ships this, for the reader leveling up. (For the Higgsfield wrappers, the skill tier is a CLI skill that needs install + auth, so its copy-paste tier is the structured prompt recipe pasted into Higgsfield's web UI.)

**The non-commodity test, applied to every skill** (from the tool-shipping-playbook): *if someone with the same tools tried to clone this tomorrow, what would they lack?* The answer is always the same two things, and they are the moat: the **taste-transfer method**, and **Sean's fleet** as the live worked example. We research the market, never the method.

---

## 2. The skill map

### User-invoked orchestrators (the partnership)

| Skill (working name) | What it does | Hardened from / NEW | Ships in | What makes it MINE (the research) |
|---|---|---|---|---|
| **The Partner** *(grill-me-for-creatives)* | Brainstorms with you, then interviews your taste out of you (what you like, what you reject, the rules of your hand) and hands it to the agent as reusable context. The flagship. | HARDEN: `creative-director` (interview, propose 2-3 routes, critique) + `sw-creative-toolkit:brainstorm` + VoicePrint's interview/gauntlet/mine pattern. Universalize off the Pencil Test pipeline to any craft. | Post 1 | grill-me is engineer-only; VoicePrint is writing-only and it is Sean's. Nobody ships a creative-taste interview. The moat is the elicitation method (B research: a self-authored edge map works where reassurance backfires). |
| **Steal Like an Artist** | Drop a mix of references + a description; it emits a unique prompt geared to *that* mix, not a generic style label. | NEW, built on `image-generator-prompt-science` (the 7-layer framework, narrative over keywords) + the reference-bundle pattern. | Post 3 | Nobody packages "describe + drop refs to a bespoke prompt for that mix." (A + true-pain research: references do not stop revert-to-average; the open gap is the orchestration/taste layer, not the model.) |
| **Per-medium Partners** (comics, animation, music & voice, editing) | The Partner re-geared per medium: a comics partner that builds world + characters + dialogue; an animation partner; an audio partner; an edit partner. Follows one project across the cascade. | HARDEN + re-gear: The Partner + `sw-creative-toolkit:storytelling`/`design-thinking` + the medium skills (anima `2d-animation-principles`, `animation-pipeline`; `writing-voice-modes` for dialogue). | Post 4 (comics) then the cascade | The cascade (one world, built across media) is a unique serialization. The medium craft is Sean's (anima). Per-medium "AI looks generic/dead" is the verified pain. |
| **Back to Basics tool wrappers** | Onboard a technical partner (skills/`.claude`, then Higgsfield, ComfyUI, Pi, Hermes, the next thing): why it is a superpower, how it works, wired to taste-transfer. | HARDEN: `higgsfield-generate` / `-soul-id` / `-product-photoshoot` / `-marketplace-cards`, `comfyui-workflows`. Mostly built already. | Back to Basics series (Post 2 onward) | Plenty teach these tools. The spin is "this tool, wired to your taste and your Soul and the Partner," never a bare tutorial. |
| **The Edge Spec** *(the bridge)* | Interview + gauntlet that maps your defensible creative edge into a one-page spec you feed the Partner. | HARDEN: VoicePrint, generalized from writing-voice to whole-creative-self. | Bridge post (Partner into System) | Direction B research: the sameness fear is the #1 verified worry, and no runnable personalized creative-edge diagnostic exists. The spec is also the first draft of the System arc's intent spec. |

### Model-invoked discipline (the reusable craft)

| Skill (working name) | What it holds | Hardened from / NEW | Used by |
|---|---|---|---|
| **The Taste Rubric** | The "does this survive revision / is it on-spec / is it still you" critique, per medium. Anima's HF/SF reason codes translated to plain-language defect names. | HARDEN: `creative-director` critique rubrics + the Taste Rubric template already drafted in [`take-two-01-…/capture-plan-and-beats.md`](take-two-01-teach-the-model-your-hand/capture-plan-and-beats.md) Part C. | The Partner, every demo |
| **Prompt Science** | The 7-layer prompt framework (task declaration, narrative over keywords, reference handling). | KEEP: `image-generator-prompt-science` (already general). | Steal Like an Artist, all image work |
| **Animation Principles** | Timing, spacing, arcs, the physics of motion that reads alive. | KEEP: anima `2d-animation-principles`. | The animation cascade |
| **Identity / Soul Lock** | Keep it recognizably you / this across a transformation. | HARDEN: `higgsfield-soul-id` + anima Character Bible identity patterns. | The cascade, any "make it yours" |
| **Voice Discipline** | Your written/dialogue voice, named and enforceable. | KEEP: `writing-voice-modes` (Sean Mode + the author techniques). | Comics dialogue, any writing lane |
| **PM-for-creatives** | Treat your creative project like a product: a brief that is a checkable spec, a pre-mortem on the idea, a JTBD on the piece. | RE-GEAR: `pm-execution:write-prd` (to creative brief), `pm-execution:strategy-red-team` (to creative pre-mortem), `pm-product-discovery:brainstorm`. | The Partner; the seam into the System arc |

---

## 3. The new skills to author (and what each must do to be MINE)

1. **The Partner** (highest priority, Post 1 needs it). A two-move session: *brainstorm* (diverge on the idea, the agent pushes back, it does not just agree) then *interview* (pull the taste markers out: keep/kill reactions, the references, the rules, the negative list). Output: a reusable `taste-context` block the reader pastes into any future prompt, plus the `.claude` skill version. The load-bearing principle (must be in the skill, not just the pitch): *the agent earns your taste by being interviewed, not by being told once.*

2. **Steal Like an Artist** (Post 3). Input: a pile of references + a freeform description. Process: the 7-layer framework + reference analysis, emitting one bespoke prompt tuned to that specific mix. The MINE clause: it names *why* it chose each move (so the reader learns the logic), and it is honest that the result is a story of corrections, not a one-shot.

3. **The per-medium Partners** (Post 4 + cascade). Start with **comics**: world, then characters, then dialogue (one post or split into the cascade's first beats). Each re-gears The Partner with that medium's discipline skill. The cascade is the spine: comics to animation to music and voice to editing, one project the whole way.

4. **The Edge Spec kit** (the bridge). VoicePrint generalized: a fast gauntlet (keep/kill, taste by negation, kills the Barnum risk) + a short self-interview, fused into a one-page Edge Spec. It surfaces a blind spot, not a compliment (B research). Hands off to the System arc as the first draft of the intent spec.

5. **Back to Basics #1, "skills 101"** (Post 2). Not a tool wrapper but the onboarding: what a skill is, how `.claude` works, why a technical partner gives you superpowers, demoed by making Post 1's Partner skill actually runnable for the reader. The bridge that earns the right to teach the heavier tools.

---

## 4. The hardening checklist (the "make it MINE" gate)

Every skill clears this before it ships, drawn from Pocock + the tool-shipping-playbook:

- [ ] **Small and composable.** One job, named in a sentence. If you cannot name the friction it kills, it is a feature dump.
- [ ] **Organized by pain, not feature.** The skill answers a failure mode the reader feels (Pocock's structure).
- [ ] **Model-agnostic.** Works in Claude, ChatGPT, or wherever. No lock-in.
- [ ] **Both tiers.** Copy-paste kit AND the symlinkable skill.
- [ ] **User vs model-invoked, declared.** Orchestrator or discipline. Orchestrators may call discipline skills, never each other.
- [ ] **The moat is load-bearing in the build, not just the pitch.** The taste-transfer principle is what the skill *does*, the way VoicePrint's "samples beat rules" is both the mechanic and the marketing.
- [ ] **A proof built in.** A before/after, a number, a watchable convergence. Answers "how do you know it works" for the technical reader.
- [ ] **Dogfood a stranger.** Run it as a persona who is not Sean; a zero-leakage check (none of Sean ends up in their output) and a distinctness check (reads as one specific person, not a template).
- [ ] **Differentiation named.** One sentence: what someone with the same tools would lack.

---

## 5. Build priority

1. **The Partner** (copy-paste + skill). Post 1 is blocked on it. Hardens fastest from `creative-director` + VoicePrint.
2. **Back to Basics #1 / skills-101** (Post 2). Light; mostly explanation + packaging the Partner for install.
3. **Steal Like an Artist** (Post 3). New build on `image-generator-prompt-science`.
4. **The comics Partner + Taste Rubric** (Post 4). Re-gear + the rubric that already exists in draft.
5. **The cascade Partners** (animation, music & voice, editing) and the **Back to Basics wrappers** (Higgsfield, ComfyUI, Pi) interleave from there. Mostly hardening already-built Anima skills.
6. **The Edge Spec kit** (the bridge into the System arc).

---

## 6. Open decisions for Sean

1. **Where the skill tier lives.** Pocock ships via `npx skills@latest add` / skills.sh. Options for us: a Pencil & Prompt skills repo (Pocock-style, the lead magnet), Claude.ai-native skills, or a Cowork/Claude Code plugin. The copy-paste tier is settled; the skill tier's home is open.
2. **Names.** "The Partner," "Steal Like an Artist," "Back to Basics," "The Edge Spec" are working. A `pm-marketing-growth:product-name` pass when the set is firm.
3. **How much of the higgsfield-* wrappers to expose publicly.** They are mature and Sean's; deciding which become public Back to Basics installments vs stay internal.
4. **The PM-for-creatives discipline** is the natural seam into the System arc (treat your art like a product). Confirm it rides the partner arc as texture, or waits for the System arc.
