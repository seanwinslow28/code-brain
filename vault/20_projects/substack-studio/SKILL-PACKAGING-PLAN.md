# Skill-Packaging Plan (rewritten 2026-08-05)
## The divergence-mechanism library behind Pencil & Prompt

**Derives from** [SOUL.md](SOUL.md) §2/§6 (the verdict is the product; the library is the lead magnet) and the sidecar locks L6/L7. **Rewritten for the divergence refocus:** the organizing machinery below (Pocock taxonomy, both-tiers rule, hardening checklist) survived the pivot intact; the product catalog swaps from taste-transfer skills to divergence mechanisms, and the library model answers the old §6.1 open decision. The taste-transfer catalog is preserved in [_archive/superseded-docs/](_archive/superseded-docs/) history and in git.

**Aspirational model, unchanged:** Matt Pocock's skills repo (small, composable, model-agnostic, organized by failure mode, shipped one-command, the newsletter's lead magnet). **The delta that makes ours a product and not a clone:** every entry carries a **tested verdict against a published measurement protocol**. The largest skill marketplace indexes 23,600+ entries with install counts and zero test results; verdicts are the shelf's missing column, verified absent in four categories (prompt libraries, enterprise eval tooling, practitioner newsletters, agent-skill marketplaces).

---

## 1. The organizing principle (Pocock taxonomy, both tiers, plus the verdict)

**Axis 1, who invokes it** (unchanged): user-invoked orchestrators (you type them; they run a session with you) vs model-invoked discipline (the agent reaches for them when the task fits). A user-invoked skill may call model-invoked skills, never another user-invoked one.

**Axis 2, the delivery tier** (unchanged): every mechanism ships copy-paste (runnable in a plain chat window today) AND as the symlinkable `.claude` skill.

**Axis 3, NEW and load-bearing: the verdict.** Every library entry carries:

- `version:` the entry is versioned; changes are diffs, not silent edits.
- `verdict: beat | tied | lost` against the median baseline, scored per the published measurement protocol (built at S5, before Rung 1).
- `receipts:` the captured run(s) behind the verdict.
- `retraction:` losers stay published with a public retraction notice (Graveyard policy). "Steelman, Then Shoot" re-runs can revise a verdict either direction.

**The non-commodity test, updated.** Old form: "if someone with the same tools tried to clone this tomorrow, what would they lack?" The answer changed. It is no longer the taste-transfer method; it is **the verdict and the cumulative record**. A competitor can clone any mechanism in an afternoon (five of six territories already have free equivalents, often well-engineered). What they cannot clone is a published protocol plus a versioned history of tested verdicts, because that is bought with time and honesty, not engineering.

**Anti-folklore rule:** no entry ships advice the round classified as folklore (temperature tuning, "think outside the box" directives) except as a tested negative result with its verdict attached.

---

## 2. The mechanism catalog (the working set)

Entry #0 is the protocol itself. Territories per the spec §5; the library builds in this order.

| # | Mechanism (working name) | Territory | What it does | Built from | Ships at |
|---|---|---|---|---|---|
| 0 | **The Scoreboard** (measurement protocol) | all | The versioned protocol: what an entry is, the baseline (the ~20-run median census), the metric with stated limits, blind judging where feasible, the retraction rule. Not a mechanism; the thing that makes every other entry credible. | Finding 8 constraints (lexical metrics insufficient; naive embedding-cosine conflates novelty with incoherence; quality-restriction flips findings). Stress-tested before publish (grilling / pre-mortem + one llm-council pass). | S5 |
| 1 | **The Opponent With a Stake** | d5 | An adversary that has something to lose (a scoreboard, a budget it defends, an instance paid to kill the idea), run heterogeneously across vendors, plus the **theater-detection test**: did the disagreement change the output, or just perform? | Sean's running `llm-council` / `fusion-discovery-council` infrastructure (the heterogeneous variant the evidence favors; the free shelf ships homogeneous persona prompts, unmeasured). | S6 (Rung 1) |
| 2 | **The Morphological Grid** | d2 | Morphological analysis ported to LLM ideation: decompose the job into parameters, force the combinatorial sweep, harvest the cells no median run visits. | The round's sleeper (+18.5% diversity, d ≈ 1.03, Nature Communications, confirmed verbatim). Needs no fleet: travels to a reader with one chat window. | Rung 2 candidate |
| 3 | **The Default Probe** | d1 | The instrument, packaged: run the reader's own brief ~20x, cluster, name the attractor basin. Ships inside every rung as the baseline and standalone as the reader's pre-work check. | The d1 demotion (instrument, not beat): Wikipedia owns the general field guide; the census of *your* brief is the part nobody ships. | With Rung 1 |
| 4 | **Ported Protocols** (the Stolen Methods line) | d2 | One offline discipline's protocol per entry (murder board, cognitive interview, desk crit, jazz comping...), stated faithfully, run against a real job, with the **translation-failure report** as a required section. Roughly half will fail; that is the interesting half and it is Graveyard fuel. | The tips-vs-protocols split (structured protocols measurably beat tips, arXiv 2602.20408). Condition from the competitive check: without the failure report it collapses into the unmeasured Scaman shape. | Recurring rungs |
| 5 | **Constraint Packs** | d3 | Bindable real-world imports (a named person who will read it, a budget that runs out mid-draft, the Honda Civic rule) + the customs-violation report format. | Story engine only; no demand claim (killed on a perfect-precision run). Ships as texture with rungs, never as a demand-driven rung of its own. Standing kill rule: "add constraints" takeaway = dead draft. | Opportunistic |
| 6 | **The Data-Hole Probe** | d4 | A practitioner-facing procedure for catching the model confidently inventing where the reader's data runs out; forces work from supplied material. | The CLEAR half of d4 (fabrication probing exists only as engineer-facing eval tooling). Gate: the reframed ~$1.50 discovery re-run before citing pain evidence. | When a data-hole draft starts |
| 7 | **The Collaborator-Aging Kit** | d6 | The sourdough setup, packaged: memory schema (five streams), the 15-minute weekly feeding ritual, the ISO log, the blind aged-vs-fresh comparison protocol, engineered amnesia as an option. | The private dark start (running since 2026-08-05) + the archived CREATIVE-PARTNER-MEMORY-SPEC research (durable core + deltas + reconcile; portability as the wedge). The 25x sycophancy-amplification result (Writer/ICLR 2026) is the named risk it instruments. | When the arc goes public (first blind comparison) |

**Rung subjects come from the quarry:** the archived creative jobs (the comics world, the self-portrait brief, the voice work) are the real jobs mechanisms run against. The demo lane stays Sean's; the mechanism travels.

---

## 3. What each entry must do to be MINE

1. **The verdict is load-bearing, not decorative.** An entry ships with its captured run and its beat/tied/lost. No verdict, no ship. This is both the mechanic and the marketing, the way VoicePrint's "samples beat rules" was.
2. **Heterogeneity where the evidence demands it.** Adversarial and panel mechanisms default to cross-vendor (the homogeneous variant measurably underperforms: consensus collapse). Cite Hegazy 2024 with its vintage attached.
3. **Named failure modes instrumented, not just acknowledged.** Theater-detection for opposition; fabrication probes for data holes; sycophancy amplification for memory. The free shelf acknowledges; we measure.
4. **Model-agnostic.** Works in Claude, ChatGPT, or wherever. No lock-in. The library's portability is a selling point the vendor-locked memory/brand-voice tools cannot match.

---

## 4. The hardening checklist (the "make it MINE" gate)

Every entry clears this before it ships (Pocock + tool-shipping-playbook, plus the verdict axis):

- [ ] **Small and composable.** One job, named in a sentence.
- [ ] **Organized by pain, not feature.** Answers a failure mode the reader feels.
- [ ] **Model-agnostic.** No lock-in.
- [ ] **Both tiers.** Copy-paste kit AND the symlinkable skill.
- [ ] **User vs model-invoked, declared.**
- [ ] **Verdict attached.** Scored against the published protocol, receipts included, version stamped.
- [ ] **A proof built in.** The before/after or the number is IN the entry, not just the post about it.
- [ ] **Dogfood a stranger.** Run it as a persona who is not Sean; zero-leakage + distinctness check.
- [ ] **Differentiation named.** One sentence: what someone with the same tools would lack. (Post-refocus, the answer should almost always include "the tested verdict.")

---

## 5. Build priority

1. **The Scoreboard** (entry #0). Everything else is bounded by it. S5, stress-tested before publish.
2. **The Opponent With a Stake + the Default Probe** (Rung 1 needs both: the probe is its baseline).
3. **The Morphological Grid** (Rung 2 candidate; cheapest high-evidence mechanism; travels without a fleet).
4. **Ported Protocols** as the recurring spine line, one port per entry.
5. **The Data-Hole Probe and Constraint Packs** opportunistically, per their gates.
6. **The Collaborator-Aging Kit** when the sourdough arc goes public with receipts.

---

## 6. Open decisions for Sean

1. **Where the library lives.** ~~Which product is the lead magnet~~ ANSWERED 2026-08-05: the library-as-product model is locked (L6/L7); the library is the lead magnet and the Substack is its changelog. Still open: the home. Pocock ships via `npx skills@latest add` / skills.sh; our options are a public Pencil & Prompt mechanisms repo (Pocock-style, research-favored), claude.ai-native skills, or a plugin. **Decided at S5** alongside the protocol, since the entry format and the home constrain each other.
2. **Names.** "The Scoreboard," "The Opponent With a Stake," "The Morphological Grid," "The Default Probe," "Constraint Packs," "The Data-Hole Probe," "The Collaborator-Aging Kit" are working names. Naming pass when the first three entries are real.
3. **Whether the library gets its own name** (from the sidecar's open question) or ships as "the Pencil & Prompt library." Decide at S5 with the home.
4. **Versioning cadence for verdict re-runs** (the old Scheduled Decay idea, demoted to policy): quarterly re-runs were the machine hypothesis; confirm cadence once entries exist.
