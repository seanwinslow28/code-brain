---
title: "Wince — the taste interview skill (design spec)"
type: spec
status: approved
created: 2026-08-10
domain: [substack-studio, creative-studio]
tags: [pencil-and-prompt, wince, taste-block, divergence-mechanism, skill-design]
ai-context: "Design for the skill Rung 0 promises. Brainstormed with Sean 2026-08-10 via superpowers:brainstorming, five locked decisions plus the name. Ships as divergence mechanism #1 for the Pencil & Prompt library. Post that depends on it: vault/20_projects/substack-studio/rung-0-taste-experiment/post.md."
---

# Wince

**The one job.** It shows you things, reads which ones you wince at, and writes the block that makes the machine draw like you.

**The pain it is organized by.** You can't describe what you want, so you argue with the model one adjective at a time and land on the average. Documented, with receipts: [the Rung 0 capture](../../../vault/20_projects/substack-studio/rung-0-taste-experiment/capture/prompts.md), six generations, five rounds of plain language before the thing Sean actually wanted showed up.

**Differentiation, one sentence.** Pocock's `grill-me` and every prompt-improver interrogate you about a spec you already have. Wince puts something in front of you and reads your reaction, because taste is the one input nobody can state before they see it.

**Invocation.** User-invoked, `/wince`. Never model-invoked; nobody wants an unprompted interview about their feelings.

---

## 1. Locked decisions

| # | Decision | Reason |
|---|---|---|
| 1 | **Visual v1, engine built to extend.** One medium-agnostic interview engine, shipping with the visual block schema only. | The visual schema is the only one with a proof behind it. Prose and music are new templates later, not a rewrite. |
| 2 | **Show, then ask.** | An ask-only interview requests a spec for taste the user hasn't met. That is the exact error the post documents. |
| 3 | **Words to narrow, images at the forks.** | Sean's constraint, verbatim: "I'd rather not do this all day." The skill has to beat five rounds, not reproduce them. |
| 4 | **A library of named blocks, one per style.** | Taste isn't one setting. Sean ran the interview more than once and wants blocks per style. |
| 5 | **Three deliberately unalike example blocks, shown only after the user's own is emitted.** | Shipping Sean's block as *the* example would pull every reader toward amber accents and construction lines, which is the convergence problem wearing his face. Ordering defuses the anchor; a label would not. |
| 6 | **Name: Wince.** | One syllable, involuntary, and it points at the mechanic that does the real work. The ban list is a list of things that made him wince. |

---

## 2. The load-bearing mechanic: dig to the decision

This is what separates a working block from a mood board, and it comes straight out of Sean's own June taste doc.

Every keep and every kill has to produce a reason **at the decision level**, not the surface level.

> **Surface:** "I love the texture and the grain."
> **Decision:** "I want the process to stay visible. The sketch marks aren't mistakes, they're evidence of thought. It's visual proof that art takes time."

The second one is portable. It tells a machine what to do in a situation Sean never described. The first one does not.

Same on the negative side. Every ban carries its why, and the why is the negative of a value the keeps demonstrated:

> **Never do:** polished, surface-perfect rendering that erases the hand.
> **Why:** everything I love keeps the fingerprints in. A flawless surface means the process was hidden or never happened.

**Rule for the interview:** it never accepts a bare preference. When the user says "I like that one," it asks what decision the maker made, and it keeps asking until the answer would still be useful applied to a different subject. One level down, every time. That is the grill-me DNA, pointed at the thing grill-me can't reach.

---

## 3. The four stages

Target: under ten minutes, three or four generations total. Sean's run took six and most of an afternoon; anything that doesn't beat that has no reason to exist.

| Stage | What happens | Generations | Source in Sean's run |
|---|---|---|---|
| **Widen** | Named directions in words. Fast keep/kill across a spread deliberately far apart. Kills dead ends before spending anything. | 0 | The early rounds where he could only say "not that" |
| **Fork** | Two or three real generations at the surviving fork, where the choice is genuinely visual. Pick one, dig to the decision. | 2-3 | Image 3 into image 4, where discovery actually happened |
| **Push** | Deliberately overshoots. Goes too far on purpose so the user can pull it back. Finds the ceiling. | 1 (may reuse Fork) | "Ugly is fine. Go too far and I'll pull you back." The round that produced the gargoyle |
| **Negate** | Builds the never-do list out of everything killed, with the why under each. No new generations. | 0 | His ten-item Ban On Sight list, the sharpest artifact in the folder |

Then **Emit**.

**Why Push is not optional.** It is the only stage that finds something the user didn't know to ask for. Cutting it turns Wince back into an interview about a spec.

---

## 4. The block schema: two altitudes, one spine

**Revised 2026-08-10** after Sean supplied a second real block of his own. The two he has written independently sit at different altitudes, and the schema follows that seam rather than inventing one.

| | [Execution block](../../../vault/20_projects/substack-studio/rung-0-taste-experiment/capture/prompts.md) (produced image 6) | [Intent block](../../../vault/20_projects/substack-studio/rung-0-taste-experiment/capture/taste-blocks/sean-intent-layer.md) (written during the first tests) |
|---|---|---|
| Altitude | how the marks get made | what the image should mean |
| Fields | medium, the hand, color rule, the finish, register, the one move | core thesis, emotional mode, composition, narrative strategy, material, color/light, character |
| Portable to prose or music? | no | **yes, almost entirely** |
| Can it say "leave the construction lines visible"? | yes | no |
| Can it say why any of it matters? | no | yes |

Neither is sufficient. Their NEVER DO lists overlap almost completely, which is the tell that negation is the stable spine under both.

**So the block has two parts and a shared spine:**

```
# TASTE BLOCK — <name>
version: <n> · <date>

## INTENT            (medium-agnostic; survives into prose, music, anything)
1. CORE THESIS       what the thing should feel like before it announces itself
2. EMOTIONAL MODE    what it favors, and what it favors it OVER
3. REGISTER          how stylized, relative to reality
4. STRUCTURE         the focal discipline; what gets room, what gets cut
5. NARRATIVE STANCE  how the meaning reaches the audience

## EXECUTION         (medium-specific; visual is the only v1 template)
6. MEDIUM / SUBSTRATE   what it's made of and made on
7. THE HAND             how the marks get made
8. COLOR / LIGHT        the palette discipline, stated as a constraint
9. THE FINISH           how finished it should look, and how finished it must NOT look
10. THE ONE MOVE        the single decision that carries the meaning

## NEVER DO          (the spine; each item carries its why)
```

**REGISTER added 2026-08-10, during Task 2 verification.** The first draft of this schema mapped six execution-block fields into five slots and silently dropped REGISTER, which is a real field in Sean's real block ("wildly exaggerated, absurd cartoon caricature. Never realistic, never photographic"). It sits in INTENT rather than EXECUTION because "how stylized, relative to reality" survives into prose and music unchanged, which is the test this section uses for the split. It is a separate axis from EMOTIONAL MODE: Sean's own taste is quiet and patient AND wildly exaggerated at once.

**This resolves the extend-later problem for free.** INTENT is already medium-agnostic, as Sean's own intent block proves. Adding prose or music in v2 means writing a new EXECUTION template and nothing else. Decision 1 gets easier, not harder.

**It also puts §2 into the artifact.** The dig-to-the-decision rule is not just interview behavior now. INTENT is where those answers land, so a block that skips it is visibly incomplete rather than quietly shallow.

**Portability requirement:** the block must survive being pasted into a chat window by a person who has never heard of this skill. No JSON, no tool-specific syntax, no references to Wince itself.

---

## 5. The library

Named blocks on a shelf. `version` bumps on refinement, so re-running sharpens a block instead of overwriting it.

- **Skill tier:** writes to a blocks folder. Can list what exists, start a new one, or refine an existing one.
- **Copy-paste tier:** prints the block and tells the reader to keep it wherever they keep notes. This is why the block must stay plain readable text.

---

## 6. Both tiers (CLAUDE.md §4, hard rule)

**Copy-paste.** One prompt, pasted into any chat window that can generate images. Runs all four stages and prints the block. No install, no account, no repo.

**Skill.** Symlinkable `.claude` skill. Same interview, plus the library operations and file persistence.

**Model-agnostic.** No API calls, no vendor lock-in, no named model anywhere in the instructions.

---

## 7. Failure paths, designed not discovered

**Content-filter refusal at Push.** Established this morning across two runs and documented in the capture file: enhancement language aimed at an image containing a child blocked 3/3 and again on a reword; with a described likeness in the chain the model refused to make the subject prettier (3/3) *and* uglier (2/2). Push is the stage most likely to trip this, because "make it ugly, go too far" is exactly the shape that gets refused.

Wince must recognize a refusal, say plainly what happened, and route around it once by pushing on something other than a person (composition, palette, finish). It must not silently loop or reword until it slips past a safety filter. **One re-aim, then move on and say so.**

**No image generation available.** Degrades to words-only across all four stages and says so up front, rather than pretending the Fork stage happened.

**User has nothing prepared.** This is the default case and the design assumes it. Widen requires nothing from the user but reactions.

---

## 8. Hardening checklist (SKILL-PACKAGING-PLAN §4)

- [x] **Small and composable.** One job, one sentence.
- [x] **Organized by pain, not feature.** Named above, with a captured receipt.
- [x] **Model-agnostic.** No lock-in.
- [x] **Both tiers.** Copy-paste kit and the symlinkable skill.
- [x] **User vs model-invoked, declared.** User-invoked only.
- [ ] **Verdict attached.** **Ships unscored.** The measurement protocol lands at S5, before the first scored rung. Stated plainly rather than faked.
- [ ] **A proof built in.** Sean's run ships inside the skill as the worked example (image 1 against image 6), not only in the post about it.
- [ ] **Dogfood a stranger.** Run the finished interview as a persona who is not Sean, e.g. someone who makes lo-fi music videos or writes ad copy. Check zero leakage of Sean's taste into their block, and that the two blocks are meaningfully different. **This is a build-completion gate, not a nice-to-have.**
- [x] **Differentiation named.** Above.

---

## 9. Out of scope for v1

- Non-visual mediums. The engine is built for them; the schemas come later.
- Scoring and verdicts. S5 protocol.
- Generating the reader's final art. The block is the deliverable; what they make with it is theirs.
- Auto-detecting taste from a portfolio or an image dump. Different mechanism, possibly a later rung.

---

## 10. Open items

1. **The two non-Sean example blocks come out of the dogfood gate, not a fabrication session.** ~~They need building separately.~~ Resolved 2026-08-10: §8 already requires running the finished interview as a persona who is not Sean. Those runs *produce* real blocks, authored by the skill under the conditions a reader will actually face. Hand-writing fake examples would be weaker evidence and more work. Two stranger personas from different lanes, two example blocks, one gate satisfied. Sean's own two blocks (intent + execution) are the third, and they double as the built-in proof required by §8.
2. **Home not decided.** Where the library lives (public repo vs claude.ai skills vs plugin) is an S5 decision per SKILL-PACKAGING-PLAN §6. Wince ships into `.claude/skills/` meanwhile.
3. **Not in the mechanism catalog.** SKILL-PACKAGING-PLAN §2 was rewritten away from taste-transfer during the refocus. Adding Wince rides the standing masthead-reconcile ticket, not a silent edit.
4. **Post dependency.** Rung 0 claims this skill exists. It publishes after Wince ships, and after the grill-me timeline contradiction in the post is resolved.

---

## 11. Next steps

1. Sean reviews this spec.
2. Implementation plan via `superpowers:writing-plans`.
3. Build `.claude/skills/wince/`, both tiers.
4. Dogfood as a stranger. Gate, not a formality.
5. Repo hygiene per code-brain CLAUDE.md: CHANGELOG entry, count tables in CLAUDE.md and README.md, `export-groups/*/playground.json` manifests, `python3 scripts/validate.py`.
6. Resolve the Rung 0 timeline, then publish the launch bundle.
