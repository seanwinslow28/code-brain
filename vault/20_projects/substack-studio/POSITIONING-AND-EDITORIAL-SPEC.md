# Pencil & Prompt — Positioning & Editorial Spec

**Status:** Rewritten 2026-08-05 for the divergence refocus (sidecar locks L1-L7; three research syntheses). The masthead lives in [SOUL.md](SOUL.md) ("push the agent past the median"); read it first. This doc is the strategic detail beneath it. Where the two disagree, SOUL.md wins. The README and CLAUDE.md derive from this doc; if they ever disagree, this wins until explicitly revised.

**Evidence base for every claim here:** [research/2026-08-05-prior-art-synthesis.md](research/2026-08-05-prior-art-synthesis.md) · [research/2026-08-05-competitive-check-six-territories.md](research/2026-08-05-competitive-check-six-territories.md) · [research/discovery/2026-08-05-territory-pain-validation.md](research/discovery/2026-08-05-territory-pain-validation.md). Cite from these (tier-audited) and never from raw DR grounding URLs.

> Note: this doc contains competitive positioning, not personal data. It is written clean for the public repo.

---

## 1. What this publication is (one paragraph)

A Substack for anyone building or living with AI who has hit the median: the models got good, and now everything they make is the same. Pencil & Prompt runs real experiments that push agents past the average, in public, and publishes the verdicts, including the failures. Each week, one real job: show the answer the model gives everyone, run one named divergence mechanism against it, capture what came out that the median run never would have produced, ship the mechanism in both tiers, and file an honest verdict. Underneath the posts sits the product: a public, versioned mechanism library where every entry carries a tested verdict against a published measurement protocol. Told funny first, useful always, by a creative PM raising a self-built fleet of agents at home, model-agnostic the whole way.

---

## 2. The reader (the one reader)

**Primary: the median-bitten practitioner.** Writers, builders, designers, PMs, daily AI users. They use AI seriously, they have felt the convergence ("the same artificial tone, the same obvious phrasing", "I cannot stress enough how obvious it is"), and they are tips-fatigued: they have read a hundred prompt listicles and rightly suspect most of the advice is folklore. Some of it measurably is (temperature tuning and "think outside the box" directives have negligible effect on semantic diversity). What they cannot get anywhere is evidence about what actually works.

**The guide, not the audience: Sean.** A creative PM who runs a self-built fleet of agents (the council infrastructure, the creative harness, the vault) and lives the incidents he writes about. The apparatus is real and running; the posts are captures from it, not thought experiments.

**Both tiers, brought along (preserved rule):** every artifact ships copy-paste for the reader in a plain chat window AND as a symlinkable `.claude` skill for the reader leveling up. The non-coder is the on-ramp, not the ceiling.

**Niche discipline:** model-agnostic (Claude / Codex / open-source, never exclude on tool), but not promise-agnostic. The promise that excludes is the evidence standard: readers who want vibes and hype have a hundred other newsletters.

---

## 3. The core belief (the soul, short form)

- The models got good, and that is the problem: competent output that converges on the same average, strongest exactly where people do paid, constrained work.
- Escaping the median is a buildable, testable capability, not a vibe. Mechanisms can be run, measured, and given verdicts.
- **The mechanism is the commodity; the verdict is the product.** A post whose deliverable is a technique competes with GitHub. A post whose deliverable is a tested verdict on a technique competes with nobody.
- Honesty is structural, not tonal: published failures, public retractions, and a measurement protocol the reader can audit.

## 4. The wedge / white space (verified 2026-08-05)

Three independent passes (DR prior-art + falsification moves, the six-territory competitive check, six discovery runs) converge on one seam:

- **Enterprise eval rigor is real but private** (CI eval gates, version snapshots, regression tests) and never published as a public library.
- **Public artifacts have no evidence standard.** Prompt marketplaces, skill marketplaces (23,600+ entries, install counts as the only signal), and free adversarial tools all ship mechanisms with zero evaluation. The sharpest specimen writes it in its own README: "this project has not independently benchmarked review quality."
- **Nate Jones (the nearest incumbent) already publishes one-off tested verdicts with honest failures.** So "we test and admit failures" is dead as a novelty claim. What he does not do, and nobody does: **cumulate**. Per-entry, versioned, retractable verdicts against a published protocol.

**The precise claim (use this form only):** no prompt or technique library publishes per-entry tested verdicts against a published measurement protocol. Broad versions ("nobody tests", "nobody admits failures") are falsifiable and will be falsified.

**Consequences:**
1. The measurement protocol is the differentiation, not a chore before it. It publishes before Rung 1 (hard order; map S5).
2. The credible comparison class is eval infrastructure, not prompt packs. Borrow its vocabulary: regression, gate, verdict, retraction.
3. Nate encroaches on angle, not artifact: his tactical artifacts are paywalled, and the genuinely free equivalents (GitHub repos, Wikipedia's Signs-of-AI-writing, SEO content) are uniformly unevaluated.

## 5. The six territories (working set, LOOSE lock L6/L7)

Adopted with evidence-side fates applied (f2). Any territory may be reshaped at draft time; reshapes route to a partner-session reconvene.

| # | Territory | Role | Fate + the rule that rides with it |
|---|---|---|---|
| d5 | Manufactured Opposition | **Rung #1 mechanism source** | Strongest keep: pain precision 1.00, three defensible gaps (stakes, theater-detection, heterogeneity). The free shelf ships persona prompts, all homogeneous, none measured; heterogeneous panels are the best-evidenced mechanism and Sean already runs the infrastructure. Theater-detection is a named check: did the disagreement change the output, or just perform? |
| d2 | Stolen Methods | **Spine mechanism source** | Keep with the claim inverted: forum pain says prompt *tips* fail; the literature says structured *protocols* measurably win (CoT + personas outperforming humans on idea diversity, arXiv 2602.20408). The tips-vs-protocols gap IS the thesis. Condition: every port ships a translation-failure report, or it collapses into Zoe Scaman's unmeasured shape. |
| d1 | Cartography of the Default | **Instrument, not a beat** | Two independent demotions (critic structural + competitive: Wikipedia's field guide cannot be out-catalogued by one person). The premise "nobody has mapped the tells" is false; what nobody has is accuracy data, and detectors "frequently flag even minimally polished text as AI-generated" (APT-Eval). The instrument: the ~20-run median census inside every rung. Evidence is writing-only; visual-tell claims are currently unevidenced. |
| d3 | Import Duty | **Story engine only** | Demand claim killed on a perfect-precision run (zero first-person constraint-failure evidence). Survives as the comedic story engine: smuggled real-world constraints, customs-violation reports. Hard rule: a draft whose takeaway is "add constraints" gets killed. No library rung on Import Duty demand. |
| d4 | The Input Axis | **Deep lane, reshaped to the data-hole probe** | Corpus half is the most saturated shelf checked and the closest relative of the dead premise; it must not lead. The data-hole probe (what the model confidently invents where no data exists, practitioner-facing) is CLEAR. Gate: the contaminated T3 ledger is not citable; a reframed ~$1.50 discovery re-run fires before any pain-evidence claim. |
| d6 | Sourdough | **Serialized arc, dark-started** | Strongest evidence in the round (precision/recall 1.00/1.00; "memory amplifies sycophantic behavior... up to 25x higher sycophancy rates", Writer/ICLR 2026). The surviving white space is narrower than the old claim: benchmarks exist; a personal, longitudinal, published aged-vs-fresh record does not. Feeding started 2026-08-05, privately; the series goes public only when the first week-N blind comparison exists, debuting with receipts. |

**Unpredicted pains logged for future angles:** fragility of centralized memory state; dependence ("a fresh session feels broken"); being falsely accused of AI as its own pain; reliability (not constraint-blindness) as what breaks deadlines; the privacy cost of feeding a personal corpus to a hosted model (the first objection a professional reader will raise, absent from all six panels).

## 6. Voice & stance

**Stance:** the experimenter who publishes verdicts. Empathetic to the median-bitten reader (their experience is real and their skepticism is correct), carrying a builder's authority inside the captures, with the irreverent edge that refuses to oversell. **Dive-bar grit stays.** Funny first, useful always: the L1 bar is a post that opens with a story that makes a person laugh, then delivers value they come back for.

**Mechanics (unchanged):** the mandatory chain, `substack-value-engine` → `storytelling-architecture` → `writing-voice-modes` (Sean Mode) → `writing-critique` → `writing-humanity-pass`. No em dashes; the ask lands sideways; anti-hype always; Sean hand-rewrites every chain draft.

**Anti-pattern:** sounding like an AI hype-bro, or like a growth-hacker who ships the prompt and never reports back. The second is now the sharper danger, because it is the industry default this publication defines itself against.

## 7. The value model

- **The Expedition is the value gate made flesh.** Median shown (Itch), mechanism run and captured (Solution), mechanism shipped both tiers with its verdict (Transfer). The capture is the post; write from the build, not after it.
- **The verdict is the product.** Every shipped mechanism enters the library versioned, with beat / tied / lost, receipts, and the retraction rule. An entry without a verdict does not ship.
- **Both tiers, every time.** Copy-paste kit AND the symlinkable skill.
- **Published failures are trust currency.** A mechanism that loses to the median in public buys more credibility than three wins.
- **Sean's growth is texture, never the pitch.** The reader promise is the headline; "look what I built" repels the reader.

## 8. The recurring formats

Detail and running order live in [SERIES-COMMAND-CENTER.md](SERIES-COMMAND-CENTER.md). The set: **Building the Ladder** (weekly Expedition rungs, numbered), **Raising Agents** (sibling story series), **Unlock Hunts** (occasional tentpoles), and **the Graveyard** (standing verdict policy, not a format). Take Two and Back to Basics are retired as structures: Take Two's before/after muscle lives on as the median-vs-escaped contrast inside every rung; Back to Basics' tool-onboarding DNA folds into rungs that need a tool.

## 9. Cadence & structure

- **Rhythm:** one rung weekly-ish, cadence gated by capture quality, never by a forced calendar. Raising Agents episodes interleave as the change-up. Unlock Hunts land when a real unlock exists.
- **Notes run from day zero** as the reach layer (first candidates already listed in the session map).
- **Subtitle = value prop** (locked research rule, upheld in the 2026-08-05 naming pass).
- **The launch bundle:** Start Here + About + the origin confession (Rung 0), live together; then the protocol post (S5) before Rung 1 (S6). Hard order.

## 10. Naming (locked)

- **Publication: Pencil & Prompt** (locked 2026-06-22, kept at the 2026-08-04 refocus, L4). The name never said "images" or "Claude"; the premise died, the name did not. A third rename would be the circling the refocus exists to end.
- **Subtitle: "Push your AI past the average, one tested experiment at a time."** Locked 2026-08-05 (S1 naming pass, Sean's pick). Reason: it states the reader's transformation plainly (the locked subtitle rule), keeps the old subtitle's cadence for continuity through the refocus, carries the thesis in "past the average", and plants the verdict promise in "tested" without jargon. Runner-up ("Real experiments that push AI past the average. Verdicts published, failures included.") was publication-facing rather than reader-facing; its verdict language goes to Start Here and About.
- **Series names:** Building the Ladder (the Expedition spine; Sean's own recurring phrase on the highest-attachment surface, L5) and Raising Agents (L2). "Building the ladder as I climb it" is the About frame and ritual sign-off.
- **Back pocket:** Saturday Morning Machine, reserved as a future series name for nostalgic childhood-coded creative content. Retired bench unchanged from the 2026-06-22 pass.

## 11. The relaunch plan

Same publication (`@seanpwins`), re-pointed; not a new account. Working order lives in [REVAMP-2026-08-05-SESSION-MAP.md](REVAMP-2026-08-05-SESSION-MAP.md):

1. ~~S1: this doc re-anchor + subtitle~~ (done 2026-08-05).
2. **S2:** theme and image pass (does the pencil-test look survive; the mascots become the Raising Agents cast).
3. **S3:** pages + profile cleanup (new subtitle and bio, curate restacks, unpublish the 3 old posts to drafts, custom homepage, launch-lean nav: Home · Start Here · Building the Ladder · About · GitHub · Portfolio).
4. **S4:** the origin confession (Rung 0, launch flagship): Sean preached taste-transfer, one GPT Image 2 test disproved his own newsletter, and the real problem underneath is the median.
5. **S5:** the measurement protocol (the artifact + the post). Hard-ordered before Rung 1; also decides where the library lives.
6. **S6:** Rung 1, Manufactured Opposition: does arguing actually help, scored against the protocol, theater-detection named.

## 12. What the research validated (2026-08-05 round)

- The library bet survives with the claim narrowed to cumulation (Move B: eleven clean NOs, one incumbent doing one-off rigor).
- Heterogeneous panels are the best-evidenced divergence mechanism; homogeneous debate hits consensus collapse. Cite Hegazy 2024 (arXiv 2410.12853) WITH its vintage: a 2024 result on 2024-era models, never presented as current.
- Morphological analysis is the sleeper rung-#2 candidate (+18.5% diversity, d ≈ 1.03, Nature Communications, confirmed verbatim): it travels to readers with one chat window.
- Temperature tuning and "think outside the box" are folklore (negligible semantic-diversity effect). Partial encroachment exists (a free 2026-03 Medium experiment reached the same conclusion at n=20), so the rung sells on protocol and scale, not surprise.
- Metric choice flips findings (preference-tuned models look more diverse until quality-restricted). The protocol must state its metric and its limits, honestly, at solo scale.
- Query shape drives source quality (research-shaped 88% academic vs market-shaped 65% marketing): every published figure resolves to a primary source first, and the tier-audit (`agents-sdk/scripts/audit_dr_citations.py`) is a standing pre-citation step.

## 13. Open questions

1. **Where the library lives** (public repo vs claude.ai skills vs plugin): decided at S5. Research favors the Pocock-style public repo as lead magnet.
2. **Monetization:** free spine + premium tier remains the research-suggested shape; parked until the launch bundle is live.
3. **Stickiness as a rung:** "the field has two studies on whether homogenization persists; here is a third" is a strong future Expedition. Not masthead material (see SOUL §1).
4. **Rung numbering vs Substack UI** (from L5's open question): settle at S3 when the section pages are built.
