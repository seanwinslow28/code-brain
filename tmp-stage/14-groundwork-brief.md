# groundwork — source brief

> The second project Sean started after the Crunchbase panel. This brief exists so it can be described accurately. Drawn from the repo's README, CONTEXT.md, and CLAUDE.md as of late July 2026.

---

## What it is, in one sentence

An open-source, harness-agnostic Company OS. You point a coding agent at the repo and it interviews your company about the work each function actually does, what should get more human time, what should get automated away, and under what rules, then generates the operating system from that map.

Its own tagline: "The groundwork your company runs on."

The output is folder-per-function ontologies, skills with named owners, a compiled constitution, and organizational memory that learns under governance instead of rewriting itself.

## Status

Charting is complete. All 19 design decisions are resolved and recorded. Build is underway. Capabilities get described publicly only as they become real, which is itself a stated discipline in the README.

---

## The one idea that makes it different

Two other projects work the same territory and both shipped parts of this shape first, which the README says plainly rather than obscuring.

**Sylph** shipped the self-improving company-brain-as-a-git-repo shape in May 2026. After you approve a skill's output, Sylph rewrites its own rules to match your edits, automatically and unreviewed. **groundwork's contrast is what happens to that rewrite:** the rule change itself becomes a typed proposal a human approves before it lands.

**clawcompany** ships four-layer compressed memory at roughly 400 tokens per mission, which is real context-budget engineering. The difference there is a category rather than a feature count: clawcompany is a runtime you adopt, its own app and server, while groundwork is files any agent already reads.

**So the lane groundwork owns is governance.** Typed rules, named owners, appeals, and a validator. Neither active competitor ships it.

---

## The concepts worth knowing by name

These are the parts that make the governance real rather than aspirational.

**The Describability Gate.** An eight-part precondition an activity must pass before a skill is generated for it: inputs, output, standard, source of truth, exception path, error cost, owner, and review gate. All eight must be *answered*. A truthful "none" counts as an answer. "N/A" does not. **There is no waiver mechanism.**

**Generator refusal.** The generator never invents an owner, a forbidden action, or a death condition. It drafts only what it can observe. Those three fields come solely from a human's interview answers.

**Death conditions.** Every skill's Owner's Card carries a pause condition and a retirement condition, always human-answered. The repo's line: "some agents should die" only means something if a human named the trigger.

**Blast-radius routing.** A proposed change auto-applies exactly when a bad version's worst case is bounded, meaning a body-only edit to a read-only or reversible-write skill. Anything touching a description, governance metadata, an Owner's Card, a higher-risk skill, or a rule escalates to human review. Auto-applied changes land in an append-only governance changelog.

**Machinery-follows enforcement.** The validator errors exactly when a field is about to back, or already backs, a running agent. It warns on incomplete thinking about activities you have chosen to act on. It stays silent on untouched worksheets. Strictness follows consequence, not completeness.

**Depth doctrine.** "Depth is earned by acting, not by planning to act." The interview steers a first run to three to five activities rather than a full inventory.

**The pull promise.** Pulling the engine forward never breaks old content merely for being old. A new requirement warns. A check that catches something always invalid keeps its severity, because the content was genuinely broken all along.

---

## Why this belongs in a Crunchbase conversation

**It is the structural answer to the pain Nick named.** Nick said "AI is moving faster than I can, by the time I finish the automation it's outdated." A pile of thirty prompts in Make.com has no owner, no review gate, no retirement condition, and no record of why a rule exists. That is why it rots. groundwork is a bet that the durable unit is not the automation, it is the governed description of the work the automation does.

**It is the same instinct as the calibration thread, applied to an org instead of a model.** Do not let the machine assert what it has not earned. Make the claim carry its evidence, its owner, and its review path. A prediction with no track record and an agent with no named owner fail the same way.

**It is an internal-platforms artifact.** The role Sean is interviewing for covers internal platforms. groundwork is what he thinks internal platforms should look like when agents are doing the work: files any agent can read, rules a human approves, and a validator that gets strict exactly where consequences are real.

---

## The honesty note that should survive any retelling

The README credits its prior art at length and by name, including work it competes with, and states plainly which ideas it did not invent. That posture is part of the project, not decoration on it.
