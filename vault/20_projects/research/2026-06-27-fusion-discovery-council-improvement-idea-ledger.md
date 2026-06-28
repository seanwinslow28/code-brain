# Idea Ledger — fusion-discovery-council: harden the engine + map to paid

- **Date:** 2026-06-27
- **Method:** deep-research (5 fan-out angles, cited) → `pm-product-discovery:brainstorm-ideas-existing` (PM / Designer / Engineer trio) → scored ledger + phased roadmap
- **Sharpening passes (2026-06-27):** Opportunity Solution Tree (§8) · success metrics + North Star (§9) · strategy red-team (§10). **Read §10 first if short on time** — it produced a Week-0 set of cheap tests that should run before any Phase-0 build.
- **Ambition (Sean's call):** harden the engine to cover all the bases now **AND** map a concrete path to a product others would pay for
- **Push hardest on:** evidence breadth & quality · output sharpness · workflow & UX
- **Scope read first:** [SKILL.md](../../../.claude/skills/fusion-discovery-council/SKILL.md) · engine at [`tools/llm-council/council/discovery/`](../../../tools/llm-council/council/discovery) · Phase 1–5 field reports in [`council/docs/`](../../../tools/llm-council/council/docs)

---

## 0. The one-paragraph read

The pipeline is already doing the **hard, rare thing** — gather real-URL evidence → multi-vendor fusion → an anti-fabrication gate → ranked idea ledger. Deep research confirms that combination is genuine whitespace: *no commercial competitor fuses multiple LLM vendors, and the leaders (PainOnSocial, BigIdeasDB) cite sources but push verification onto the user ("verify the findings yourself") rather than enforcing a gate.* So the moat is real — but three things keep it from "golden": (1) the **verification is mechanically shallow** (substring match, below 2026 SOTA), (2) the **output is mechanically shallow** (`intensity × corroboration` score, templated opportunity text — the framing throws away the evidence richness the gate worked so hard to earn), and (3) it's a **single-operator artifact** with no longitudinal memory, no run history, and Sean's absolute paths baked in. Fix those and you have a tool that is both best-in-class for your own discovery *and* a credible paid product. This ledger ranks the fixes and sequences them.

---

## 1. What the research changes about the plan

Five cited briefs (full sources in §7). The load-bearing findings:

| Finding | Source signal | Implication for the skill |
|---|---|---|
| **No competitor fuses vendors; none *enforce* a citation gate** — they cite + say "verify yourself." GummySearch (the 140K-user category leader) **shut down Nov 2025** on Reddit-API licensing. | Competitive brief | The wedge is real and the category just lost its leader. Lead with the gate as a **guarantee**, and stay multi-source so you're not Reddit-API-hostage like the dead incumbent. |
| **Substring-matching is below SOTA.** Production grounding = atomic-claim decomposition + **NLI entailment** (does the source *entail* the claim, not *contain a string*). Recipes: ALCE/TRUE, RAGAS faithfulness, FActScore; cheap verifiers: DeBERTa-NLI, **Luna**. | Methods brief | `verify.py`'s `needle in hay` is gameable and brittle (it caused the one inconclusive live spot-check). Upgrade the gate — it's literally the moat. |
| **Multi-vendor panels beat a single strong judge AND are ~7× cheaper (PoLL, Cohere)** — *but only when decorrelated.* #1 failure mode: correlated errors / echo chambers. **Self-preference bias** is real: never let a model family grade its own output. | Methods brief | `standard` tier uses **judge = Opus while Opus is on the panel** — a textbook self-preference setup. Cheap, high-credibility fix. |
| **Velocity = slope of demand, not size.** Demand-intent lives in autocomplete + People-Also-Ask. Standard math: multi-axis pain score (frequency × intensity × reach) with **exponential recency decay** `e^(−λ·age)`, times a velocity multiplier. | Trend brief | Adds the missing "why now." Competitors sell velocity (Exploding Topics $39–249) and demand-intent (AnswerThePublic $9–199) *separately* — fusing them into one gated card is unclaimed. |
| **Actionable opportunity card = who · pain (customer's words) · evidence · SIZE · why-now · proposed bet.** ODI score = `Importance + max(Importance − Satisfaction, 0)`. RICE confidence is the evidence-penalty term. | Output brief | The current card (`opportunity: "Ship a capability that removes X"`, `workaround: "(from evidence — see quotes)"`) is filler. Real framing is the biggest output-sharpness win. |
| **Pay-for reality:** self-serve discovery $19–$99/mo; one-time "report" $29–$149; done-for-you brief $500–$2.5K; creator paid-newsletter $10–$30/mo. The gate doesn't open a *new* pricing axis — it lets you sit at the **top** of the indie band, not the $19 bottom. **Recurring needs a "fresh/dated" justification.** | Monetization brief | Maps cleanly to three buyers. The longitudinal pain-tracking idea (below) is what makes a *subscription* honest rather than a one-time DB sale. |

---

## 2. The brainstorm — 15 ideas across the trio

Generated PM / Designer / Engineer per `brainstorm-ideas-existing`. Each is tagged to a real code path and a research finding so it's actionable, not theoretical.

### Product Manager (business value · strategy · customer impact)

- **PM1 — "Verified, or it doesn't ship" as the product promise.** Make the anti-fabrication gate the *brand*, not an implementation detail. Surface a per-run **fabrication-gate scorecard** (verified N / dropped M / corroborated-across-K-domains). Research: competitors cite but don't enforce — this is the only durable moat on top of converging card-framing.
- **PM2 — Add the "why now" layer (velocity + demand-intent).** Fuse pain evidence with trend slope and autocomplete/PAA demand into a single card. No competitor fuses pain + velocity + intent; they're sold as three separate products.
- **PM3 — Longitudinal pain taxonomy (the recurring-value moat).** Persist verified pains across runs in a small store; track frequency/intensity/recency over time so a re-run says *"this pain is accelerating / cooling / newly emerged."* This is the deferred §13 item — and the **single thing that makes a subscription honest** (fresh/dated = the recurring justification).
- **PM4 — Real opportunity scoring (ODI + RICE-confidence + recency/reach).** Replace `intensity × (1+domains)` with a defensible score a PM can paste into a PRD: importance/underservedness, reach (upvotes/distinct authors), recency decay, corroboration. The PM buyer's exact need is "inputs to a decision I won't be embarrassed by."
- **PM5 — Three output modes for three buyers.** Same engine, three framings: PM opportunity card · indie one-time "deep opportunity report" · creator paid-newsletter card stream. This is the packaging spine for map-to-paid.

### Product Designer (UX · usability · delight)

- **D1 — The actionable opportunity card redesign.** Adopt who · pain-in-their-words · evidence · **size** · **why-now** · **proposed bet (riskiest assumption + cheapest test)**. Directly fixes the filler `opportunity`/`workaround` fields in [`frame.py`](../../../tools/llm-council/council/discovery/frame.py).
- **D2 — Receipts UI (provenance you can see).** Every claim renders its verification status inline: ✓ verified · corroborated across K domains · recency badge · quote+permalink. Make the gate *visible* — trust is a UX surface, and it's the demoable wow for a paid buyer.
- **D3 — Discovery dashboard artifact.** A self-contained HTML view (Sean already ships these via `mcp__cowork__create_artifact` + the agent-fleet-observability pattern) over run history: spend vs caps, verified/dropped trend, pain-taxonomy movement, re-open buttons. Answers the workflow gap + the research-flagged bill-shock anxiety.
- **D4 — Promote the blind-spot/whitespace map to hero output.** It's the signature cross-model artifact and SKILL.md §6 already calls it "often the highest-signal section" — yet it renders last. Lead with it, and attach concrete "sharpen the next run" actions (reframe topic · add `--segment` · raise tier).
- **D5 — Interactive card triage.** Accept / reject / promote each card (today `pipeline.cli patches list` is read-only). Triage decisions feed the taxonomy (PM3) and produce a curated shortlist — the artifact a creator/PM actually acts on.

### Software Engineer (technical possibility · data leverage · scale)

- **E1 — Entailment verification gate v2.** Upgrade [`verify.py`](../../../tools/llm-council/council/discovery/verify.py) from substring to **atomic-claim + NLI entailment** (ALCE/TRUE recipe; cheap DeBERTa-NLI or Luna as the per-claim checker; keep substring as a fast pre-filter). Fixes brittleness *and* is the moat tech. Add separate **citation precision + recall** to the scorecard.
- **E2 — Fix panel self-preference + add a blind, separate adjudicator.** `standard` tier has judge=Opus with Opus on the panel. Make the judge a different family from any panelist, keep it blind to authorship, swap evidence order. PoLL-backed; low effort, high credibility.
- **E3 — MMR dedup + recency decay in scoring.** Near-duplicate collapse (republished articles cluster in embedding space — MMR is built into LangChain/LlamaIndex) + exponential time decay `e^(−λ·age)` and reach weighting in the score. Tunable α; guard against recency over-correction (research caveat).
- **E4 — New signal channels: velocity + demand-intent (as scoring, not gate-evidence).** Google Trends (pytrends/SerpApi) slope + autocomplete/PAA. **Critical nuance:** PAA/autocomplete produce *queries, not URL-anchored quotes*, so they must feed the **score**, not the gate (the skill already correctly excludes them as evidence — add them as a separate channel). Also harden the under-yielding collectors: fan reviews out to N single-`site:` queries (Brave collapses OR'd `site:`), stabilize HN.
- **E5 — Decouple from one machine (the productization spine).** Config-driven paths, env-based output dir, per-user spend namespacing, kill the hardcoded "for Sean" in the brief. Then the deferred **autonomous/queued mode** (overnight topic queue, reusing the fleet's launchd pattern) becomes possible. Required before anyone but Sean can "access" it.
- **E6 — Auto web-supplement (BACKFILL, Stage 5).** After FRAME, turn each blind-spot bullet into a *solution-side* web search (how-tos, comparisons, studies, success cases), URL-anchor every finding, and append a separate **Web Supplement (gap-fill)** section — marking anything it can't fill as "still open." Makes the whitespace map (D4) self-chasing. **Build-ready:** spec'd + TDD-scoped in [`docs/prompts/2026-06-27-fusion-discovery-council-web-supplement-stage-prompt.md`](../../../docs/prompts/2026-06-27-fusion-discovery-council-web-supplement-stage-prompt.md), born from the manual gap-fill pass Sean ran on the 2026-06-27 substack runs. Safe by construction (deterministic extraction can't fabricate); its real failure mode is *relevance*, which E1's entailment upgrade later vets.

---

## 3. Top 5 (the prioritized cut, per the brainstorm skill)

Ranked on strategic alignment (harden + map-to-paid) × impact × feasibility × differentiation.

| # | Idea | Why it was selected | Key assumptions to validate |
|---|---|---|---|
| **1** | **E1 — Entailment verification gate v2** | The gate *is* the moat and it's currently below SOTA + caused the only live spot-check failure. Hardening it is both the #1 quality win and the #1 paid-trust story. | A small NLI model (DeBERTa/Luna) raises recall without nuking precision or blowing latency/cost on a per-claim pass; substring stays as a cheap pre-filter. |
| **2** | **PM4 + D1 — Real opportunity score + card redesign** | Biggest output-sharpness win (Sean's chosen axis); turns gate-verified evidence into PRD-grade cards. Low-moderate effort, no new API spend. | ODI/RICE-style scoring is computable from fields the panel already returns (intensity, segment, corroboration) + cheap derived signals (reach from upvotes, recency from dates). |
| **3** | **PM3 — Longitudinal pain taxonomy** | Converts a one-shot tool into recurring value — the *only* honest basis for a subscription (research: recurring needs "fresh/dated"). Also a genuinely novel signal (pain accelerating) no competitor has. | A stable pain-identity key across runs is achievable (embedding-cluster or canonical-title match) without heavy infra; SQLite next to `.vault-index.db` suffices. |
| **4** | **PM2/E4 — Velocity + demand-intent channel** | Adds "why now"; fuses three signals competitors sell separately. High differentiation, moderate effort. | Free/cheap velocity (pytrends) and PAA sources are reliable enough; keeping them as *score* signals (not gate-evidence) preserves the fabrication guarantee. |
| **5** | **E2 — Fix panel self-preference + blind adjudicator** | Cheap, fast, research-backed quality + credibility fix; removes a textbook bias from the headline "multi-vendor" claim. | A non-panel judge of equal quality exists in the OpenRouter roster at acceptable cost; blinding doesn't degrade clustering. |

> **The bridge to paid** rides on top of these: **D2 (receipts UI)** + **D3 (dashboard)** are the demoable surfaces, and **PM5 + E5** are the packaging + decoupling that make "people pay to access" literally possible.

---

## 4. Full scored ledger (all 15 + harden-hygiene)

Impact 1–5 (customer/quality value) · Effort 1–5 (1 = hours, 5 = multi-day) · **Moat** = deepens the defensible wedge · Tag = which chosen axis it serves.

| ID | Idea | Impact | Effort | Moat | Tag | Tier |
|---|---|:--:|:--:|:--:|---|:--:|
| E1 | Entailment verification gate v2 | 5 | 3 | ★★★ | Evidence | **P0** |
| PM4+D1 | Real opportunity score + card redesign | 5 | 2 | ★★ | Output | **P0** |
| E2 | Fix self-preference + blind adjudicator | 4 | 1 | ★★ | Evidence | **P0** |
| H | Harden hygiene (reviews fan-out, HN, `--segment` escaping, request-shape watch, typed `failure_reason`) | 3 | 1 | ★ | Harden | **P0** |
| PM3 | Longitudinal pain taxonomy | 5 | 4 | ★★★ | Output/Paid | **P1** |
| PM2/E4 | Velocity + demand-intent channel | 4 | 3 | ★★ | Evidence | **P1** |
| D2 | Receipts UI (visible provenance) | 4 | 2 | ★★ | Output | **P1** |
| E3 | MMR dedup + recency/reach decay | 4 | 2 | ★ | Evidence | **P1** |
| E6 | Auto web-supplement (BACKFILL Stage 5) — *build-ready prompt* | 4 | 2 | ★★ | Evidence/Output | **P1** |
| D4 | Whitespace map as hero output | 3 | 1 | ★ | Output | **P1** |
| D3 | Discovery dashboard artifact | 4 | 3 | ★ | Workflow | **P2** |
| D5 | Interactive card triage | 3 | 3 | ★ | Workflow | **P2** |
| PM1 | Fabrication-gate scorecard (brand) | 3 | 1 | ★★ | Paid | **P2** |
| E5 | Decouple from one machine | 4 | 4 | ★ | Paid | **P2** |
| PM5 | Three output modes / packaging | 4 | 3 | ★★ | Paid | **P3** |
| — | Autonomous/queued overnight mode | 3 | 4 | ☆ | Workflow | **P3** |

---

## 5. Phased roadmap (the sequence)

Ordered exactly to Sean's framing: **harden-now → output-sharpen → workflow → map-to-paid.** Each phase has a Definition of Done so it doesn't drift.

### Week 0 — Validate before you build (from the red-team, §10)
Five cheap tests, ranked by impact × cheapness. The first uses data already on disk and **gates the whole effort**:
1. **Audit your own conversion.** Of the verified cards in your existing 6+ ledgers/sessions, how many became a real artifact (commit / post / PRD)? If it's near zero, the bottleneck isn't discovery *quality* — and hardening won't move the North Star. Fix the conversion gap first. ($0, ~1 hr.) **→ DONE 2026-06-28: ~88% generous conversion across 16 runs — REFUTED, proceed. See §11.**
2. **Panel vs single-model** on one topic, same evidence bundle, blind-rate the pain points — does fusion earn its 4–6× cost?
3. **5 buyer conversations** — does "verified, not hallucinated" rank *above* quantity/novelty as a purchase driver? (Tests the paid wedge.)
4. **Re-run one past topic** 2–4 weeks later — does pain movement exceed sampling noise? (Validates PM3 / the subscription thesis.)
5. **Track per-collector yield** (you already emit `gather_status`) — is any single source becoming load-bearing and fragile?

### Phase 0 — Harden (close the honest backlog) · ~1 focused session
The field reports' own §7 list + the two cheap moat fixes. **DoD:** a few consecutive live runs (incl. `deep`) with no FUSE flake, no self-grading judge, every collector yielding.

- **E2** — judge ≠ any panelist family; blind to authorship; swap evidence order.
- **H** — reviews collector fans out to N single-`site:` queries; stabilize HN under `--no-native-web`; `--segment` operator-char strip; add the OpenRouter request-shape live re-verify + surface typed `failure_reason`.
- Confirm `last30` reddit yield holds; one `deep`-tier live run as the SSE-padding worst case.

### Phase 1 — Sharpen the output (the chosen #1 axis) · ~2 sessions
Make the gate deeper and the cards PRD-grade. **DoD:** a run produces cards with size + why-now + proposed-bet, each claim entailment-verified with precision/recall reported.

- **E1** — entailment gate v2 (atomic-claim + NLI; substring as pre-filter; precision/recall on the scorecard).
- **PM4 + D1** — ODI/RICE-style score (importance/underserved · reach · recency-decay · corroboration) + the who/pain/evidence/size/why-now/bet card.
- **E3** — MMR dedup + recency/reach decay (feeds PM4's score).
- **D4** — whitespace map first, with "sharpen the next run" actions.
- **D2** — receipts UI (verification status inline).

### Phase 2 — Evidence breadth + the longitudinal moat · ~2 sessions
Add the signals competitors silo, and the memory that makes re-runs compound. **DoD:** a second run on the same topic reports pain movement over time; cards carry a velocity/why-now signal.

- **PM3** — pain-taxonomy persistence (SQLite next to `.vault-index.db`; stable pain key via embedding-cluster/canonical-title).
- **PM2/E4** — velocity (pytrends) + demand-intent (autocomplete/PAA) as a **scoring channel** (never gate-evidence).
- **D3** — discovery dashboard artifact (run history, spend vs caps, pain trends, re-open).
- **E6** — auto web-supplement / BACKFILL ([build-ready prompt](../../../docs/prompts/2026-06-27-fusion-discovery-council-web-supplement-stage-prompt.md)). **Pull-forward candidate:** it's spec'd and additive, so it can land as early as Phase 1 to feed D1's *why-now / proposed-bet* slot with solution-side evidence. **No hard dependency on E1** (safe by construction — deterministic extraction can't fabricate), but it must call the **shared verification helper E1 will own**, so its relevance vetting upgrades for free when E1 lands. Default-ON → watch the *verified-but-ignored* counter-metric so the supplement doesn't become an unread appendix.

### Phase 3 — Map to paid (decouple + package) · scoped, not started
Only after the engine is best-in-class for *Sean's own* use. **DoD:** a non-Sean user can run it on their own key/paths and get a verified ledger; one packaging picked and priced.

- **E5** — config-driven paths, per-user spend, kill the "for Sean" hardcode.
- **D5** — interactive triage → curated shortlist.
- **PM1 + PM5** — gate scorecard as the brand; pick a packaging (see §6) and ship the first external surface.
- Autonomous/queued mode if daily use materializes.

---

## 6. Map-to-paid — the packaging options (decide later)

Research-anchored; the anti-fabrication gate is what lets you sit at the **top** of each band, not the bottom. Don't pick now — Phase 3 decides.

| Buyer | What they pay for | Packaging | Realistic price | Anchored to |
|---|---|---|---|---|
| Indie founder (entry) | "don't build the wrong thing" — cheap validated, evidence-linked ideas | Subscription, ~5–10 verified cards/mo | **$19–$29/mo** | PainOnSocial $19 floor; gate premium → $29 |
| Indie founder (one-shot) | one verified deep report, no commitment | One-time "deep opportunity report" | **$29–$149** | AI-report ~$2/run → BigIdeasDB $149 lifetime |
| PM / serious individual | decision inputs they won't be embarrassed by | Subscription + export + team-shareable | **$49–$99/mo** | PainOnSocial Pro $49; Exploding Topics $99 |
| Done-for-you | trust + named deliverable | Per-engagement verified brief | **$500–$2,500** one-off | CI briefs $1K–$5K |
| Creator | fresh post-able angles with receipts | Paid newsletter of verified cards | **$10–$30/mo** | Substack high-value niche $20–$50 |

**Recommended lead:** subscription with included verified runs (top of indie band, the gate justifies it), **one-time report as the escape hatch**, paid-newsletter as funnel. **Not** recommended as the core: selling the skill file itself (power-law, small — fine as a $5–$9 PromptBase credibility artifact) or pure usage credits (bill-shock kills solo conversion). The longitudinal taxonomy (PM3) is what makes the *subscription* honest; without it you're selling a one-time DB.

**Portfolio value (the other "paid"):** even if it never charges a dollar, this is a near-perfect AI-PM portfolio piece — a multi-vendor system with a *measurable* anti-hallucination guarantee, scored against named 2026 methods (ALCE, PoLL, ODI). The entailment-gate + precision/recall metric is a recruiter-grade artifact on its own.

---

## 7. Assumptions to validate + risks

- **Gate upgrade pays for itself.** Validate E1 raises citation recall without tanking precision or per-run latency/cost. Cheapest test: run the new NLI gate over an *existing* session JSON's candidates and diff verified/dropped vs. the substring gate. No new spend.
- **Pain-identity is stable enough across runs.** PM3 needs a key that matches "the same pain" run-to-run. Cheapest test: cluster two existing same-topic runs' verified pains; eyeball whether the matches are real before building persistence.
- **Velocity/intent stay out of the gate.** The fabrication guarantee is the whole moat — PAA/autocomplete must never be paraphrased into a sourced claim. Enforce structurally (separate channel), as the skill already does for excluded sources.
- **Data-source fragility is the category's killer.** GummySearch died on Reddit-API licensing. Staying multi-source is the hedge; don't let any one collector become load-bearing.
- **Don't over-engineer verification.** Research warns naive precision is gameable by saying less, and recency weighting can over-correct. Keep α/thresholds tunable and report both precision and recall so regressions are visible.
- **Map-to-paid is downstream of decoupling.** The tool is honestly single-operator today (absolute paths, "for Sean"). No external-pay conversation is real until E5. Keep Phase 3 gated behind Phases 0–2.

---

## 8. Opportunity Solution Tree (sharpening pass — added 2026-06-27)

Anchors every idea to **one** desired outcome → opportunities → solutions → experiments (Teresa Torres). The "customer" here is the discovery-tool *user* (Sean now; PM / founder / creator later).

**Desired outcome (one metric):** lift the share of discovery runs that yield a *trusted, acted-on* opportunity — a card that becomes a build, a post, or a PRD input — toward **≥50%** (baseline TBD; see §9 and the Week-0 audit).

**Opportunities, scored `Importance × (1 − Satisfaction)`, 0–1 (Sean-as-user):**

| Opportunity (user's words) | Imp | Sat | Score | Maps to |
|---|--:|--:|--:|---|
| O3 — "Every run starts from zero — I can't tell if a pain is growing, fading, or new." | .75 | .05 | **.71** | PM3 |
| O2 — "It tells me a pain exists, not whether it's worth acting on or *why now*." | .90 | .25 | **.68** | PM4 · D1 · E4 · E3 |
| O6 — "Only I can run this; I can't hand it to anyone." | .65 | .05 | **.62** | E5 · PM5 (Phase 3) |
| O1 — "I have to re-verify quotes myself, and sometimes they don't hold up." | .95 | .55 | **.43** | E1 · D2 · PM1 |
| O5 — "I can't trust the run at a glance — spend, drops, what's new." | .60 | .30 | **.42** | D3 · PM1 |
| O4 — "I get generic pain, not pain for the segment I care about." | .70 | .45 | **.39** | E4 · `--segment` |

**The non-obvious read:** the *output* gaps (O3, O2) score **higher** than the *gate* gap (O1) — because the gate already works (Sat .55), it just isn't SOTA. So felt value lives in **sharpen + longitudinal (Phase 1–2)**; the gate upgrade (E1) is a **defensibility / paid-credibility** bet, not where you feel the most pain today. This refines the roadmap: *within Phase 1, the card-redesign + scoring (O2) can ship before the entailment gate (E1)* for fastest felt value — even though E1 is the bigger moat.

**Top-3 in-scope, expanded (outcome → opportunity → 3+ solutions → cheapest experiment):**

| Opportunity | Solutions (PM / Designer / Eng) | Cheapest experiment (hypothesis · metric · threshold) |
|---|---|---|
| **O2 — worth acting on / why-now** | PM4 ODI/RICE score · D1 card redesign (who/pain/evidence/size/why-now/bet) · E4 velocity+demand-intent · E3 recency/reach decay | Re-score one existing ledger both ways, show old vs new card to yourself. *Metric:* "which would you act on?" *Threshold:* redesigned chosen ≥4/5. ($0) |
| **O3 — is this pain growing** | PM3 taxonomy persistence (SQLite) · pain-movement badges · D3 trend view · embedding pain-key | Cluster two existing same-topic runs' verified pains. *Metric:* % correct same-pain matches (eyeball). *Threshold:* ≥80% before building persistence. ($0) |
| **O1 — trust the evidence (the moat)** | E1 entailment gate v2 · D2 receipts UI · PM1 gate scorecard · E3 MMR dedup (real, not duplicate, corroboration) | Replay an existing session's candidates through a prototype NLI gate vs substring. *Metric:* Δ verified/dropped + manual correctness on a 20-card sample. *Threshold:* recall ↑, precision ≥ substring, $0 spend. |

O6 (hand it to others) is the highest-scoring *paid-path* branch but stays Phase 3; O4/O5 are supporting.

---

## 9. Success metrics — North Star + dashboard (sharpening pass — added 2026-06-27)

**North Star: _Acted-on verified opportunities per month_** — verified cards that became a build, a post, or a PRD input (trailing 30 days). Chosen because it measures *value delivered*, not vanity (runs generated, cards produced) — a verified pain nobody acts on is worthless. *Formula:* `count(cards where triage = acted ∧ traceable to an artifact) / 30d`. *Source:* triage (D5) + taxonomy (PM3); until those ship, a **manual log**.

**Input metrics (the levers, ~MECE):**

| Input | Definition | Driven by |
|---|---|---|
| Verified-card yield / run | verified cards per run | GATHER breadth × gate |
| Actionability rate | % verified cards carrying size + why-now + proposed-bet | Phase-1 sharpen (PM4/D1) |
| Trust rate | % verified cards accepted at triage with no bad citation found | Phase-1 gate (E1) |
| Why-now coverage | % cards with a velocity/demand signal attached | Phase-2 (E4) |
| Supplement gap-fill rate | % of blind-spots filled (vs left "still open") per run | Phase-2 (E6) |

**Health metrics (must stay stable):**

| Metric | Healthy | Yellow | Red | Freq |
|---|---|---|---|---|
| Citation precision (sampled/NLI) — *the moat metric* | ≥0.95 | 0.90–0.95 | <0.90 | per run + weekly |
| Citation recall (don't over-drop true pains) | ≥0.85 | 0.70–0.85 | <0.70 | weekly |
| Supplement relevance precision (sampled; full vet pending E1 entailment) — *does the gap-fill quote actually address the gap?* | ≥0.80 | 0.65–0.80 | <0.65 | weekly |
| Drop rate | 20–60% | 60–80% or <10% | >80% | per run |
| Cost / run vs tier cap | ≤ cap | 1–1.8× cap | >1.8× cap (observed $2.74 vs $1.50) | per run + daily total |
| FUSE success / collector yield | ~100% / all >0 | one collector 0 | FUSE flake | per run |

**Counter-metrics (guard against Goodhart):** ① **verified-but-never-acted-on rate** — if yield climbs but this does too, you're making trustworthy-but-useless cards; ② **single-source-card share** — if it climbs with yield, corroboration is illusory.

**Metrics tree:**
```
North Star: Acted-on verified opportunities / month
├── Input: verified-card yield/run      → GATHER + gate
├── Input: actionability rate           → card redesign + scoring (Phase 1)
├── Input: trust rate                   → entailment gate (Phase 1)
├── Input: why-now coverage             → velocity/intent channel (Phase 2)
└── Counters: verified-but-ignored · single-source-card share
```

**Honest instrumentation note:** the North Star + inputs 2–4 + counters **can't be auto-measured until D5 (triage) + PM3 (taxonomy) + D3 (dashboard) ship** — until then, log them by hand against your own runs. The **gate-health metrics (precision/recall/drop/cost/FUSE) are measurable now** from the session JSON + spend file, and they're exactly what gates E1's success — so instrument those in Phase 1, the value metrics when their features land. (Pre-launch framework; calibrate baselines after the Week-0 audit.)

---

## 10. Red-team — attack the load-bearing assumptions (sharpening pass — added 2026-06-27)

> Supersedes the flat list in §7 with a ranked, tested version. A fair adversary, not a doubt-manufacturer — what holds up is named plainly in the second block.

### Top kill-assumptions (ranked by impact × likelihood-wrong × cheapness-to-test)

**1. Verified discovery actually converts to acted-on opportunities.** *(the North Star itself)* — ✅ **TESTED 2026-06-28: REFUTED (~88% generous conversion across 16 runs). Proceed. Full findings in §11.**
- **Claim:** a sharper, more-trusted discovery output will produce more builds/posts/decisions.
- **Fails if:** the binding constraint on shipping is *time/execution*, not idea-supply — in which case better discovery doesn't move output at all.
- **Evidence this week:** audit your existing 6+ ledgers/sessions — how many verified cards became a real artifact?
- **Kill criterion:** <~10% historical conversion ⇒ stop; fix the idea→action gap (triage, smaller bets) before hardening the engine.
- **Cheapest test:** the Week-0 #1 audit. Data is already on disk. $0.

**2. "Verified, not hallucinated" is what buyers will pay for.** *(the paid wedge)*
- **Claim:** trust/provenance is the purchase driver, so the gate justifies premium pricing.
- **Fails if:** buyers reveal-prefer *quantity / novelty / freshness*, and "verify yourself" is good enough — the gate's value is invisible until a fabrication burns you (rare, deniable).
- **Evidence this week:** 5 buyer conversations (PM, founder, creator) ranking purchase drivers; or a landing-page A/B on the verification promise.
- **Kill criterion:** verification ranks below quantity/novelty for ≥4/5 ⇒ don't lead with the gate in GTM; reposition.
- **Cheapest test:** 5 convos / a Reddit ask. ~Hours.

**3. The gate is a durable moat, not a one-sprint copy.** *(differentiation)*
- **Claim:** entailment + multi-vendor cross-check + corroboration is harder to copy than a substring check; execution is the moat.
- **Fails if:** an incumbent (PainOnSocial/BigIdeasDB) ships "we cite + verify" first — research flagged them "one engineering sprint" away — and erases the differentiation; today's substring gate is in fact *weaker* than they could build.
- **Evidence this week:** competitor feature-watch; ship E1 + a published precision/recall number you can defend.
- **Kill criterion:** a competitor ships enforced verification before you reach buyers ⇒ moat is execution-speed only; compete on the longitudinal/fusion layer instead.
- **Cheapest test:** quarterly competitor scan + the E1 replay experiment (§8, O1).

**4. Multi-vendor fusion materially beats a single strong model *for this task*.** *(cost structure + the "fusion" brand)*
- **Claim:** decorrelated vendors give blind-spot coverage (the whitespace map) worth the 4–6× spend (PoLL).
- **Fails if:** PoLL is about *judging*, not *idea-generation-from-fixed-evidence* — a single strong model on the same bundle may yield ~equivalent pain points, making the panel mostly waste (the $2.74 overshoot).
- **Evidence this week:** A/B one topic — panel vs single-model on the *same* evidence bundle; blind-rate both.
- **Kill criterion:** blind raters can't distinguish panel from single-model output ⇒ drop to single-model + keep one cross-check pass for the gate only; bank the cost.
- **Cheapest test:** one paired run, blind rate. Small $.

**5. Longitudinal tracking creates real recurring signal.** *(the subscription justification for PM3)*
- **Claim:** "this pain is accelerating/cooling" is a true, recurring signal that makes a subscription honest.
- **Fails if:** on the cadence a user re-runs, pain movement is within sampling noise — "accelerating" is an artifact of which posts got fetched.
- **Evidence this week:** re-run one past topic 2–4 weeks later; compare verified-pain frequency/intensity deltas to run-to-run variance.
- **Kill criterion:** movement indistinguishable from noise ⇒ PM3 is a *memory/dedup* feature, not a trend signal; don't price a subscription on it.
- **Cheapest test:** one re-run of an existing topic. ~1 run's spend.

### What's well-reasoned (don't manufacture doubt)
- **The gate-as-architecture is genuinely rare** — research confirmed *no* competitor enforces verification (they cite + say "verify yourself"). That whitespace is real.
- **Sequencing paid behind quality** (harden → sharpen → workflow → paid) is sound — it refuses to sell a single-operator, coupled tool.
- **The output-sharpness diagnosis is concretely correct** — verified against `frame.py` (templated `opportunity`, `workaround: "(from evidence — see quotes)"`, score = `intensity × (1+domains)`).
- **Keeping velocity/demand-intent out of the gate** is the right call — it preserves the fabrication guarantee (the whole moat).
- **Not leading with selling the skill file** is well-supported (power-law marketplace; fine as a $5–9 credibility artifact, not a revenue line).

### What I couldn't assess (gaps)
- **Actual historical conversion rate** — needs the Week-0 #1 audit (the single most important unknown).
- **Revenue vs portfolio-credibility** — "map to paid" could mean either; it changes everything about Phase 3 scope. (You said paid, but the bar differs hugely between "a real SaaS" and "a recruiter-grade artifact that *could* charge.")
- **Buyer identity** — PM vs founder vs creator are three different products; the OST/metrics assume "Sean-as-user" today.
- **Per-run cost at others' scale** — the $2.74 overshoot is fine for you; unmeasured if strangers run it on a metered key (E5 addresses, untested).

---

## 11. Week-0 conversion audit — findings (2026-06-28)

The cheapest, highest-stakes test from §10 (red-team #1): *do verified discovery runs actually convert to acted-on artifacts, or do they sit unused?* Scope: all three clusters (~16 runs), generous definition (engaged = synthesized / fed an editorial pipeline / used in a real event / a post in active capture), with shipped flagged separately. Read-only, $0 — traced session JSONs + ledgers forward to downstream artifacts.

| Cluster | Runs | Verified pains | Downstream artifact traced | Conversion (generous) |
|---|--:|--:|---|---|
| **Crunchbase** (06-25) | 5 | 32 | `crunchbase-discovery-synthesis.md` → used in the **CPO interview, Fri 6/26** (1-day turnaround; it *changed* the interview thesis) | ✅ acted-on |
| **Substack 06-27 batch** | 6 | ~29 | `2026-06-27-discovery-synthesis-backlog-and-web-supplement.md` → `SERIES-COMMAND-CENTER` **Take Two backlog** + **discovery-angle map** → flagship post `take-two-01` (`discovery_angle:` cites the exact run angles; capture-pending) | ✅ acted-on |
| **Substack 06-22** (soulless-AI) | 1 | 7 | feeds the discovery-angle map (Fix My Mess / Take Two) | ✅ acted-on |
| **Substack 06-02** (mature, ~26d) | 1 | — | informed editorial positioning (MIGRATION-REPORT) | ◐ acted-on (old, diffuse) |
| **2D-animation substack-deep** (06-21) | 1 | 4 | promoted into the substack pipeline (copied in) | ◐ engaged, no post yet |
| **2D-animation pm** (06-21, standard+deep) | 2 | 15 | none traced | ✗ not-yet (no destination) |

**Verdict: red-team kill-assumption #1 is REFUTED.** Generous conversion ≈ **14/16 runs (~88%)** — far above the ~10% kill threshold that would have said "stop hardening, fix conversion first." Discovery is *not* a dead-end here; **it converts fast when pointed at a destination** (the Crunchbase batch converted in a day because it had an interview; the substack batch is mid-pipeline with institutionalized machinery). **So hardening is justified — proceed with the roadmap.**

**Shipped (strict), honestly:** only the Crunchbase synthesis has been *used externally* (the interview). The substack posts are days old and sit in a documented capture pipeline, not yet published — so strict "published-post" conversion is **still unproven** and should be re-checked in ~2 weeks once `take-two-01` + the Take Two backlog ship. The only clear non-converters are the 2 exploratory 2D-animation **pm** runs, which had no live target.

**The real finding — it re-orders the roadmap (this is the payoff).** Every conversion routed through the *same manual middle step*: **consolidate the ledgers → re-rank/re-score by recurrence & severity → run a web pass to fill the blind-spot map.** That hand-done middle is the actual observed friction — so the roadmap items that automate it are the highest-leverage, now **evidence-backed, not hypothesized**:

- **E6 (BACKFILL)** automates the exact web-supplement pass both syntheses did by hand → **confirmed top felt-value priority** (it's literally the manual step you keep repeating).
- **PM4 (real scoring)** — both syntheses re-ranked by recurrence/severity manually → automate it.
- **D4 (whitespace-first)** — the blind-spot map is the most-acted-on section (the whole supplement pass exists to serve it) → lead with it.
- **PM3 (longitudinal/synthesis memory)** — the synthesis doc is a manual per-batch artifact today → persist it.
- **E1 (gate)** stays the **defensibility / paid-credibility** bet (consistent with the §8 OST: it's not where the *felt* friction is). Keep it P0 for the moat, but the **felt-value order is E6 → PM4 → D4 first**.
- **Usage insight:** discovery converts when it has a "so-what" home. The 2 non-converters had none. Point runs at live targets — and the tool could even prompt *"where will this go?"* at FRAME time.

**Caveats:** n=1 (Sean's own usage — the right unit for the North Star at this stage); corpus skews very recent; evidence is documentary (frontmatter `discovery_angle`, synthesis refs, command-center wiring), not published URLs; generous definition. The strict shipped-post rate is the open question — revisit ~2 weeks.

---

## 12. Sources

**Competitive landscape:** GummySearch shutdown + alternatives ([redship.io](https://redship.io/reddit-tool/gummysearch), [bigideasdb.com](https://bigideasdb.com/gummysearch-alternative)) · [PainOnSocial](https://painonsocial.com/) · [Painpoint](https://www.painpoint.space/) · [BigIdeasDB](https://bigideasdb.com/) · [Syften](https://syften.com/) · [F5Bot](https://f5bot.com/) · [Brand24 pricing](https://brand24.com/prices/) · [Mention pricing](https://mention.com/en/pricing/) · [Reddily](https://reddily.io/).
**Trend/demand:** [Exploding Topics pricing](https://tipsonblogging.com/2025/05/exploding-topics-pricing/) · [Glimpse](https://meetglimpse.com/) · [AnswerThePublic pricing](https://answerthepublic.com/en/pricing) · [Google Trends API (2025)](https://developers.google.com/search/blog/2025/07/trends-api) · [Exa pricing](https://exa.ai/pricing) · velocity math [texta.ai](https://www.texta.ai/glossary/trend-velocity), [trendtracker.ai](https://www.trendtracker.ai/blog-posts/whats-rising-whats-fading-how-to-interpret-trend-velocity) · recency decay [landbase.com](https://www.landbase.com/blog/how-to-weight-recency-vs-frequency-vs-intensity-in-email-signal-scoring) · PAA demand-intent [searchengineland.com](https://searchengineland.com/guide/people-also-ask).
**Methods:** LLM-attribution survey [arxiv 2311.03731](https://arxiv.org/html/2311.03731v2) · FActScore [arxiv 2305.14251](https://arxiv.org/pdf/2305.14251) · RAGAS [docs](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) · TruLens RAG-triad [trulens.org](https://www.trulens.org/getting_started/core_concepts/rag_triad/) · Luna [arxiv 2406.00975](https://arxiv.org/html/2406.00975v2) · PoLL [arxiv 2404.18796](https://arxiv.org/html/2404.18796) · multi-agent debate/correlated-errors [arxiv 2510.12697](https://arxiv.org/pdf/2510.12697) · FreshLLMs [arxiv 2310.03214](https://arxiv.org/abs/2310.03214) · MMR [community.fullstackretrieval.com](https://community.fullstackretrieval.com/retrieval-methods/maximum-marginal-relevance).
**Output frameworks:** RICE [Intercom](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) · ODI/Opportunity Algorithm [Strategyn](https://strategyn.com/outcome-driven-innovation/) · Opportunity Solution Trees [Product Talk](https://www.producttalk.org/opportunity-solution-trees/) · JTBD forces [jobstobedone.org](https://jobstobedone.org/radio/unpacking-the-progress-making-forces-diagram/) · opportunity brief [Productfolio](https://productfolio.com/opportunity-brief-template/) · Cagan assessment [Product School](https://productschool.com/blog/product-fundamentals/opportunity-assessment) · Rule of One [eternitymarketing.com](https://eternitymarketing.com/blog/the-single-most-important-rule-in-copywriting) · scratch-your-own-itch [Marc Lou](https://newsletter.marclou.com/p/scratch-your-own-itch).
**Monetization:** [PainOnSocial pricing](https://painonsocial.com/pricing) · [ChatGPT pricing](https://chatgpt.com/pricing/) · [Perplexity Pro/Max](https://www.perplexity.ai/pro) · [BigIdeasDB pricing](https://bigideasdb.com/bigideasdb-pricing) · [Fiverr market-research costs](https://www.fiverr.com/resources/guides/costs/market-researcher) · skills marketplaces [agent37.com](https://www.agent37.com/blog/monetize-claude-code-skills), [PromptBase](https://promptbase.com/sell) · paid newsletters [beehiiv 2026](https://www.beehiiv.com/blog/the-state-of-paid-newsletters-2026).

> Research caveats carried from the briefs: Glimpse paid pricing is demo-gated (approximate); Google Trends API is alpha/no-public-pricing; ODI opportunity-score thresholds (~10/~15) are convention not law; several monetization figures are secondary aggregators — spot-verify before quoting in any customer-facing doc.
