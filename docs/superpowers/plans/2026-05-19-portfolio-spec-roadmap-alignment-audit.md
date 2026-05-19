# Portfolio Spec ↔ Unified Roadmap Alignment Audit

> **For agentic workers:** This is a **scoping audit**, not a TDD plan — no test code, no commits. Findings are organized by severity. Each carries a concrete action with file:line references. Resolve every CRITICAL item before opening the Phase 2 build session in [`~/Code-Brain/sw-ai-pm-portfolio/`](../../../../../sw-ai-pm-portfolio/). Use checkbox (`- [ ]`) syntax on action items as you close them.

**Goal:** Confirm the [sw-ai-pm-portfolio specs](../../../../../sw-ai-pm-portfolio/docs/specs/) (8 surface specs + 1 blueprint + 1 master plan) are coherent with what the [unified roadmap](../../../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md) is shipping into them — surfacing every contradiction, schema mismatch, missing upstream artifact, and untouched open decision **before** Sean opens the Phase 2 build session.

**Architecture under audit:** The redesigned portfolio replaces the V3-bridge `sw-portfolio` at the same apex (`seanwinslow.com`). The roadmap ships **content** (EXPLANATION.md files, manifesto, scorecard, control-architecture doc) into the portfolio's four content collections (`work` / `transactions` / `architecture` / `essays`) via canonical-source build-time fetches. The portfolio's job is to be the **frame** around the body of work the roadmap is filling in.

**Reading order if executing in a fresh session:**
1. [`sw-ai-pm-portfolio/docs/specs/BLUEPRINT-COMPLETE.md`](../../../../../sw-ai-pm-portfolio/docs/specs/BLUEPRINT-COMPLETE.md) §5 punch list
2. This audit (you're here)
3. [`PORTFOLIO-MASTER-PLAN.md`](../../../../../sw-ai-pm-portfolio/docs/specs/PORTFOLIO-MASTER-PLAN.md) §10 open decisions
4. The 8 surface specs in numbered order

---

## TL;DR — punchline before the body

**The good news:** Slug naming, IA shape, and Tier-A discipline are aligned end-to-end. Every roadmap artifact the portfolio renders (Tasks 10/12/13/14/15) has a home: matching slugs, matching cross-link contracts, matching ship dates. The 4-collection graph (`work` + `transactions` + `architecture` + `essays`) is the right shape for what the roadmap is shipping.

**The bad news (2 critical items, both pre-existing in the blueprint's punch list):**
1. The locked transactions schema's `surface` enum is **5 strict values** (`fleet`/`pipeline`/`product`/`writing`/`infra`), but the roadmap authors use **free-text strings** ("MCP server", "eval harness", "control-plane interceptor", "manifesto / thesis", "architecture writeup"). Either widen the enum or write a definitive remap table before the migration script runs. **Recommended:** keep the enum, ship a remap table.
2. Hero spec §14 + Task 1 Step 3.4 both link the Intent Engineering MCP tile to `/transactions/intent-engineering-mcp/`, but the projects spec + case-study spec + master plan §7 lock it to `/work/intent-engineering-mcp/`. Sean adjudicates; both routes resolve at scale (one is a ledger row, one is a case study), but the **tile** has to point at one of them.

**The pending work (3 important items):**
3. The PENDING ADDITIVE — add `relatedArchitecture` to the transactions schema (already flagged in blueprint §5 item #1).
4. Six PMP §10 open decisions still carry recommended defaults that haven't been confirmed.
5. Six drafted specs still need lock confirmation (case-study, about, transactions, architecture, essays, site-chrome).

**The roadmap dependencies (4 minor items):**
6. Five upstream `EXPLANATION.md` files referenced by frontmatter `explanationUrl` don't exist upstream yet (animation-pipeline, superuser-pack, the-block, 16bitfit + the manifesto/architecture sources). Without them, `scripts/fetch_canonical_sources.mjs` fails the build.
7. One date drift: roadmap Task 13 heading says draft-lock 2026-05-23; body says 2026-05-22. Confirm and fix one of them.
8. Hero `/api/dateline.json` `ledger_row` pattern + projects `/api/next-piece.json` need the Daily Driver extension before Phase 2 ships (BLUEPRINT §3.6).
9. The five Daily Driver write endpoints share **no MCP access** (superuser-pack CLAUDE.md). Live install counts (`shipped-stats-intent-engineering-mcp.json`) come from npm/GitHub public HTTPS APIs only.

---

## File map — what this audit references

**Spec layer** (under [`~/Code-Brain/sw-ai-pm-portfolio/docs/specs/`](../../../../../sw-ai-pm-portfolio/docs/specs/)):
- `BLUEPRINT-COMPLETE.md` (synthesis)
- `PORTFOLIO-MASTER-PLAN.md` (strategic)
- `hero-spec-v1.md` (LOCKED 2026-05-13, animation-reconciled 2026-05-16)
- `projects-section-spec-v1.md` (LOCKED 2026-05-13, A-3 status amended 2026-05-17)
- `case-study-spec-v1.md` (DRAFTED 2026-05-17)
- `about-spec-v1.md` (DRAFTED + lead-line repositioned 2026-05-18)
- `transactions-spec-v1.md` (DRAFTED 2026-05-17)
- `architecture-spec-v1.md` (DRAFTED 2026-05-17)
- `essays-spec-v1.md` (DRAFTED 2026-05-17)
- `site-chrome-spec-v1.md` (DRAFTED 2026-05-17)
- `texture-and-artifacts-spec-v1.md` (not reviewed in this audit — foundations only)

**Roadmap layer:**
- [`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`](../../../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md) (canonical)

**Canonical EXPLANATION.md sources (referenced by spec frontmatter):**
- [`vault/40_knowledge/templates/EXPLANATION-template.md`](../../../vault/40_knowledge/templates/EXPLANATION-template.md) — the 4Q schema all collections validate against
- [`agents-sdk/lib/concept_edges/EXPLANATION.md`](../../../agents-sdk/lib/concept_edges/EXPLANATION.md) — Phase D (committed)
- [`agents-sdk/agents/knowledge_loop/EXPLANATION.md`](../../../agents-sdk/agents/knowledge_loop/EXPLANATION.md) — Phase 6 (committed)
- [`evals/vault-synthesizer/EXPLANATION.md`](../../../evals/vault-synthesizer/EXPLANATION.md) — eval suite (committed)
- [`~/Code-Brain/sw-mcp-intent-engineering/docs/EXPLANATION.md`](../../../../../sw-mcp-intent-engineering/docs/EXPLANATION.md) — Intent Engineering MCP (committed in sibling repo)
- `docs/MEANING_OVER_ACCESS.md` + `docs/MEANING_OVER_ACCESS_EXPLANATION.md` — manifesto (NOT YET AUTHORED — Task 13 ships 2026-05-22 draft-lock)
- `docs/VAULT_AS_AGENT_INFRASTRUCTURE.md` + `docs/VAULT_AS_AGENT_INFRASTRUCTURE_EXPLANATION.md` — scorecard (NOT YET AUTHORED — Task 15 ships 2026-06-03)
- `agents-sdk/docs/CONTROL_ARCHITECTURE.md` + `agents-sdk/docs/EXPLANATION.md` — control architecture (NOT YET AUTHORED — Task 14 ships 2026-06-10)
- `agents-sdk/lib/judge/EXPLANATION.md` — judge layer (NOT YET AUTHORED — Task 12 ships 2026-06-04)
- `gate-b-drafts/EXPLANATION.md` — substack-drafter (committed)

---

## CRITICAL findings (resolve before opening the Phase 2 build session)

### C-1: `surface` enum mismatch between locked spec and roadmap authoring vocabulary

**Where it lives:**
- Spec contract: [`transactions-spec-v1.md` §3.2](../../../../../sw-ai-pm-portfolio/docs/specs/transactions-spec-v1.md#L142-L156) declares `surface: z.enum(['fleet', 'pipeline', 'product', 'writing', 'infra'])` — strict, 5 values, validator fails the build on a 6th.
- Roadmap authoring (current V3 bridge):
  - Task 1 Step 3.1 (line 255): *"`surface` values: `\"MCP server\"` / `\"eval harness\"` / `\"SDK agent\"`"* — three free-text strings, none in the spec enum.
- Roadmap authoring (future task ledger rows):
  - Task 12 (line 867): `surface: "control-plane interceptor"`
  - Task 13 (line 959): `surface: "manifesto / thesis"`
  - Task 15 (line 1135): `surface: "architecture writeup"`
- V3 bridge schema (Task 1 Step 3, line 245): `surface: string` (free text, required, no enum).

**Why this matters:** The redesign's migration script (`migrate_v3_transactions.mjs`, transactions §11.1) maps V3 `beat` → new `surface`, but **it doesn't yet have a mapping table for the free-text strings being authored RIGHT NOW into the V3 bridge** (shipping Mon 5/19). Every future ledger row authored against the roadmap's vocabulary will fail the spec validator unless one of: (a) the enum is widened, (b) an explicit remap is added to the migration script, (c) Sean rewrites each `surface` value at MDX-author time.

**Recommended action — keep the enum, ship the remap table:**

The enum is the right shape (PMP §3.3 surface differentiation, mobile filter UI, 5-value visual continuity with status). Widening it dilutes the IA. Instead, lock a **canonical mapping table** in `transactions-spec-v1.md` §12.3 alongside the existing `beat → surface` table:

| Free-text input (V3 bridge + roadmap authoring) | Canonical `surface` enum value |
|---|---|
| `MCP server` (Task 1 intent-engineering-mcp; future Task 10 vault-knowledge-mcp) | `product` |
| `eval harness` (Task 8 vault-synthesizer-eval-suite) | `fleet` |
| `SDK agent` (Task 9 substack-drafter) | `fleet` |
| `control-plane interceptor` (Task 12 judge-layer) | `fleet` |
| `manifesto / thesis` (Task 13 meaning-over-access ledger row) | `writing` |
| `architecture writeup` (Task 14 control-architecture; Task 15 vault-scorecard) | `infra` |
| `agentic-engineering` (V3 `beat`, Phase D + Phase 6) | `fleet` |
| `creative-pipeline` (V3 `beat`, animation work) | `pipeline` |
| `cushion-economics` (V3 `beat`, vault-as-cushion thesis) | **manual per row** — `product` OR `infra` per the existing §12.3 note |

**- [ ] Action C-1.1:** Add the table above to `transactions-spec-v1.md` §12.3 immediately after the existing 3-row `beat → surface` mapping. Heading: "Free-text → canonical surface remap (forward-looking)."

**- [ ] Action C-1.2:** Update `scripts/migrate_v3_transactions.mjs` (when authored — currently spec-only) to consume the table verbatim. The interactive prompt at migration time should default-suggest the canonical value but let Sean override per row.

**- [ ] Action C-1.3:** Add the table to the build session hand-off prompt at `transactions-spec-v1.md` Appendix C — so the build session knows the mapping is real-data, not example data.

---

### C-2: Intent Engineering MCP tile/ledger destination contradicts across surfaces

**Where it lives:**
- Hero spec §14 (line 325): *"MCP server interactive embed (E2) — separate page (`/transactions/intent-engineering-mcp`), not in the hero."*
- Roadmap Task 1 Step 3.4 (line 261): the 6th home-page card on the **V3 bridge** links to `/transactions/intent-engineering-mcp/` — *"it's an AI ledger artifact, ledger-resident."*
- Projects spec §3 (line 68): A-3 tile maps to `/work/intent-engineering-mcp` (kebab-case slug per §3 routing).
- Case-study spec §13.3 (per blueprint §5 item #2): canonical at `/work/intent-engineering-mcp/`.
- PMP §7 + §11 references: `/work/intent-engineering-mcp` (case-study route).
- Blueprint §5 already flagged this as the only inter-spec contradiction in the punch list.

**Why this matters:** At hard cutover (PMP §10 Decision 9 default), the redesign replaces the V3 bridge. The redesign's projects grid is the home-page entry point for Intent Engineering MCP. If the tile points at `/transactions/intent-engineering-mcp/`, the case-study page at `/work/intent-engineering-mcp/` becomes orphaned (no inbound link from the projects section). If the tile points at `/work/intent-engineering-mcp/`, the V3 bridge's `/transactions/intent-engineering-mcp/` route still resolves (slug preserved through migration) — but Sean has to commit to **both surfaces existing simultaneously**, cross-linked.

The blueprint's own §3.1 ("4-collection content graph") already endorses this: *"One artifact can appear on multiple surfaces simultaneously with the same slug."* The 5 case-study tiles are curated narrative deep-dives; `/transactions/` is exhaustive ledger. Both surfaces feed off the same MDX content collections.

**Recommended action — both surfaces exist; tile points at `/work/`:**

- The redesign's A-3 tile in the projects grid points at `/work/intent-engineering-mcp/`. This is the canonical "narrative deep-dive" route.
- A separate ledger row at `/transactions/intent-engineering-mcp/` also exists (migrated from V3 if it's there 5/19 EOD, or new-authored in the redesign content collection). Surface: `product` per C-1's remap.
- The case-study page's frontmatter declares `relatedLedgerRow: intent-engineering-mcp`; the ledger row declares `relatedCaseStudy: intent-engineering-mcp`. The cross-link script auto-renders both reverse-links.
- Hero spec §14's reference to `/transactions/intent-engineering-mcp` is patched as a 2026-05-19 changelog entry on the locked hero spec — body stays untouched (the §14 line is out-of-scope content describing where the MCP embed lives, not where the tile links).

**- [ ] Action C-2.1:** Add a 2026-05-19 changelog entry to `hero-spec-v1.md` §1.1 noting the MCP embed location updated from `/transactions/intent-engineering-mcp` → `/work/intent-engineering-mcp` to match the projects-spec routing contract.

**- [ ] Action C-2.2:** Confirm in the build session that BOTH surfaces are populated at crossover — the migration script preserves the existing `/transactions/intent-engineering-mcp.md` MDX (V3-bridge inherited) AND a new `/work/intent-engineering-mcp.mdx` (curated case-study) gets authored. They share the slug; they don't compete.

**- [ ] Action C-2.3:** Verify the cross-link graph (`derive_crosslinks.mjs`) handles same-slug-different-collection correctly — the build script needs to disambiguate "ledger row named `intent-engineering-mcp`" from "case study named `intent-engineering-mcp`" in the JSON output. (Slug + collection together = unique key.)

---

## IMPORTANT findings (resolve before locking the 6 drafted specs)

### I-1: The PENDING ADDITIVE — `relatedArchitecture` field on transactions schema

**Where it lives:**
- Architecture spec §14.1 (lines 619-631): declares the required additive verbatim — `relatedArchitecture: z.union([z.string(), z.array(z.string())]).optional()` on the transactions schema. No removals, no renames.
- Blueprint §5 item #1: flagged as the **pending additive that must fold in before build session #1**.
- Transactions spec §3.2: locked spec without the field; cross-link declaration goes one-way (architecture → ledger via `relatedLedgerRow`); reverse direction (ledger → architecture) needs this additive to declare bidirectionally.

**Why this matters:** The 4-surface cross-link graph (BLUEPRINT §3.1) only closes if both directions can declare the edge. Without this additive, ledger rows that want to cite their architecture writeup can only declare it via `derive_crosslinks.mjs` reverse-inference — which works at build but means Sean can't author the relationship from the ledger row's MDX directly.

**Recommended action — apply now, before locks land:**

**- [ ] Action I-1.1:** Edit [`transactions-spec-v1.md` §3.2](../../../../../sw-ai-pm-portfolio/docs/specs/transactions-spec-v1.md) (the Zod schema block) — add the field inside the `Cross-links` section, immediately after `previousVersion`:
```ts
relatedArchitecture: z.union([z.string(), z.array(z.string())]).optional(),  // slug or array; bidirectional via derive_crosslinks.mjs
```

**- [ ] Action I-1.2:** Add a 2026-05-19 entry to `transactions-spec-v1.md` §1.1 (Changelog): *"Additive: `relatedArchitecture: string | string[]` optional field added to schema per architecture-spec §14.1. Bidirectional reverse-link via `derive_crosslinks.mjs`. Pure additive; no behavioral change to existing MDX rows that lack the field."*

**- [ ] Action I-1.3:** Verify Appendix B (frontmatter shape, lines 762-810) includes `relatedArchitecture: null` in the Cross-links block so the example shape stays canonical.

---

### I-2: Six PMP §10 open decisions still carry unconfirmed recommended defaults

**Where it lives:** PMP §10 (lines 374-385) + Blueprint §4.9 (lines 199-209).

| # | Decision | Recommended default | Action |
|---|---|---|---|
| 3 | Dark mode in V1? | Light-only home hero, manual footer toggle for sub-pages | **Confirm or switch** |
| 4 | The Block case study framing | Frame the work, not the exit; Larry Cermak as primary reference; ARCHIVED status locked | **Confirm; Block content review must happen before /work/the-block/ ships** |
| 5 | 16BitFit case study | PAUSED locked; case study leans on the pipeline, not finished game | **Confirm there's enough shippable artifact material** — if no, drop A-5 to A-4 + reduce grid to 5 cells (case-study spec §13.5 OPEN-3) |
| 7 | Global nav shape | All 5 surfaces as siblings (`work` / `transactions` / `architecture` / `essays` / `about`) | **Confirm; switch only if cluttered after live build** |
| 8 | A-3 tile media | 90-sec Loom poster (terminal + Claude Desktop loading) | **Confirm; pick at tile-build time based on 400×500px legibility** |
| 9 | Crossover sequencing | Hard cutover when redesign V1 DoD-green | **Confirm; switch only if hot recruiter loop forces progressive launch** |

**- [ ] Action I-2.1:** Sean adjudicates all 6 in one pass. Likely just "confirm" for all of them per the recommended defaults — only #4 (Block content review) needs material work before the case study can be authored, and that's case-study-spec scope, not portfolio-foundations scope.

**- [ ] Action I-2.2:** Add a 2026-05-19 entry to PMP §10 marking each row's status (resolved + linked to where the resolution landed) — keeps the open-decisions surface honest.

---

### I-3: Six drafted specs still need lock confirmation

**Where it lives:** Blueprint §2 spec map (lines 19-30) — these 6 are still `DRAFTED 2026-05-17`.

- `case-study-spec-v1.md` — has 3 open questions, all with recommended defaults (Blueprint §4.3)
- `about-spec-v1.md` — has 6 open questions, all with recommended defaults (Blueprint §4.4)
- `transactions-spec-v1.md` — has 5 open questions, all with recommended defaults (Blueprint §4.5)
- `architecture-spec-v1.md` — has 5 open questions, all with recommended defaults (Blueprint §4.6)
- `essays-spec-v1.md` — has 5 open questions, all with recommended defaults (Blueprint §4.7)
- `site-chrome-spec-v1.md` — has 5 open questions, all with recommended defaults (Blueprint §4.8)

**Why this matters:** Phase 2 (Hero + Projects) doesn't depend on these locks — Hero and Projects are already locked. But Phase 3 (case-study + about + transactions + architecture + essays + site chrome) cannot begin until the specs lock. If Sean starts building Phase 2 now and the locks land in parallel, Phase 3 begins cleanly.

**Recommended action — defer lock confirmation to the spec-lock pass; Phase 2 doesn't gate on it:**

**- [ ] Action I-3.1:** Open a separate spec-lock session sometime in the next 3 days (5/19–5/21). Walk each spec's open-questions section. Confirm or switch each default per the spec's own `switch-only-if` condition. Add a `2026-05-19` (or relevant date) lock entry to each spec's §1.1 changelog.

**- [ ] Action I-3.2:** Update Blueprint §2's spec map to flip each row from `DRAFTED` → `LOCKED` after the lock pass.

**- [ ] Action I-3.3:** Phase 2 build can proceed in parallel — Hero (`hero-spec-v1.md`) + Projects (`projects-section-spec-v1.md`) are already locked. Don't block on the other 6.

---

## ROADMAP-DEPENDENCY findings (must close before relevant build phase)

### R-1: Five upstream `EXPLANATION.md` files don't exist yet

**Where it lives:** Blueprint §5 punch list items 14-15 + the case-study spec §13.1-§13.5 + architecture spec Appendix B + essays spec Appendix B.

**The full inventory (cross-referenced against `git ls-files`):**

| Upstream file | Required by | Status | Roadmap task |
|---|---|---|---|
| `agents-sdk/lib/concept_edges/EXPLANATION.md` | Phase D ledger row + superuser-pack case study | ✅ COMMITTED 2026-05-12 | Task 2 |
| `agents-sdk/agents/knowledge_loop/EXPLANATION.md` | Phase 6 ledger row | ✅ COMMITTED 2026-05-12 | Task 2 |
| `evals/vault-synthesizer/EXPLANATION.md` | Eval suite ledger row | ✅ COMMITTED 2026-05-12 | Task 8 |
| `~/Code-Brain/sw-mcp-intent-engineering/docs/EXPLANATION.md` | Intent Engineering MCP case study + ledger row | ✅ COMMITTED 2026-05-12 | Task 3 |
| `gate-b-drafts/EXPLANATION.md` (substack-drafter) | Substack-Drafter ledger row | ✅ COMMITTED 2026-05-12 | Task 9 |
| `agents-sdk/lib/judge/EXPLANATION.md` | Judge Layer ledger row | ⏳ NOT YET — Task 12 ship 2026-06-04 | Task 12 |
| `docs/MEANING_OVER_ACCESS.md` + `docs/MEANING_OVER_ACCESS_EXPLANATION.md` | Manifesto essay + ledger row | ⏳ NOT YET — Task 13 draft-lock 2026-05-22 | Task 13 |
| `agents-sdk/docs/CONTROL_ARCHITECTURE.md` + `agents-sdk/docs/EXPLANATION.md` | Control Architecture writeup + ledger row | ⏳ NOT YET — Task 14 ship 2026-06-10 | Task 14 |
| `vault/SCORECARD.md` + `docs/VAULT_AS_AGENT_INFRASTRUCTURE.md` + `docs/VAULT_AS_AGENT_INFRASTRUCTURE_EXPLANATION.md` | Vault Scorecard architecture writeup + ledger row | ⏳ NOT YET — Task 15 ship 2026-06-03 | Task 15 |
| `<animation-pipeline-repo>/EXPLANATION.md` | 2D Animation Pipeline case study (A-1) | ⏳ NOT YET — case-study spec §13.1 OPEN-1 | Task 5 / animation 6/11 |
| `claude-code-superuser-pack/EXPLANATION.md` | Superuser Pack case study (A-2) | ⏳ NOT YET — case-study spec §13.2 | (informal — no roadmap task assigned) |
| `<the-block-templates>/EXPLANATION.md` | The Block case study (A-4) | ⏳ NOT YET — case-study spec §13.4 + PMP §10 Decision 4 | (depends on Block content review) |
| `<16bitfit-repo>/EXPLANATION.md` | 16BitFit case study (A-5) | ⏳ NOT YET — case-study spec §13.5 + PMP §10 Decision 5 | (paused; case study leans on pipeline) |

**Why this matters:** `scripts/fetch_canonical_sources.mjs` (essays §11.1 unified version) **fails the build** if any `explanationUrl`, `essaySourceUrl`, or `sourceUrl` HEAD-check 404s. The redesign cannot build for production until every referenced upstream file exists at the URL declared in its MDX frontmatter.

**Recommended action — phase the upstream authoring to match the build phases:**

The redesign's Phase 2 (Hero + Projects) doesn't fetch any canonical sources — it's purely chrome. So Phase 2 can build TODAY.

The redesign's Phase 3 (case studies + about + transactions + architecture + essays) builds against the canonical fetcher. Phase 3 cannot ship until at least:
- The 5 already-committed `EXPLANATION.md` files (for the V3 bridge migration's pre-existing rows) — ✅ ready
- The case studies have either canonical EXPLANATION.md (preferred) OR inline-body 4Q (V3-fallback, case-study spec §9.2 Option B)
- The architecture + essays surfaces have their canonical sources (or those surfaces don't ship in the first wave)

**- [ ] Action R-1.1:** For the 4 case study upstream files that don't yet exist (superuser-pack, animation-pipeline, the-block, 16bitfit) — case-study spec §9.2 Option B already allows inline-body 4Q for v1. Author the 4Q content directly in MDX frontmatter `four_q:` mirror initially; co-located `EXPLANATION.md` follows when the work earns one. This unblocks Phase 3 case-study builds **without** waiting on upstream authoring.

**- [ ] Action R-1.2:** For Task 13 (manifesto) — the architecture surface ships **after** Task 15 (Vault Scorecard, 6/3) and Task 14 (Control Architecture, 6/10). Order the Phase 3 surface-build sequence in the build session:
1. Case studies (5 MDX, inline-body 4Q where needed) — can start any time post-Phase-2
2. About + transactions + site-chrome — depend on V3-bridge migration; run migration script first
3. Architecture — waits for Task 15 ship (6/3) to populate Vault Scorecard
4. Essays — waits for Task 13 draft-lock (5/22) + Task 14 ship (6/10) for the manifesto's plotted artifacts

**- [ ] Action R-1.3:** Add a `KNOWN-UPSTREAM-PENDING.md` file at the portfolio repo root listing the 8 pending upstream `EXPLANATION.md` files + their ship dates. The build script reads this file and **warns** (not errors) when a referenced URL is in this list, with the ship date. Other URLs still hard-fail.

---

### R-2: V3 bridge ships Mon 5/19 with a looser schema than the redesign

**Where it lives:**
- V3 bridge schema (roadmap Task 1 Step 3.1, line 245): `surface: string` (free text), `shipped: required ISO`, `repoUrl: optional`, `explanationUrl: optional`. No `valueProp`, no `methods[]`, no `limitations[]`.
- Redesign schema (transactions §3.2): `surface: enum (5 values)`, `shipped: strict ISO`, `valueProp: required ≤280 chars`, `methods[]: min 1`, `limitations[]: min 1`, `status: enum`.

**Why this matters:** The redesign re-architects the V3 schema — it doesn't inherit verbatim (transactions §3.1). The migration script (§11.1, §12) handles this at crossover via interactive Sean-confirms-each-row. But during the **interim period** (V3 bridge live from Mon 5/19 → redesign cutover, target TBD), every new artifact Sean ships writes against the V3 schema, NOT the redesign schema. When the migration finally runs, those interim rows need re-authoring of `valueProp`, `methods[]`, and `limitations[]`.

**The interim is bounded but real:** Tasks 12, 13, 14, 15 all ship into the V3 bridge ledger before the redesign cuts over. That's potentially **4-6 new rows authored against the looser schema** before migration.

**Recommended action — author defensively now, migrate-friendly later:**

**- [ ] Action R-2.1:** When authoring Tasks 12/13/14/15 ledger rows on the V3 bridge (Mon 5/19 → cutover), **include the future-schema fields anyway**, even though the V3 bridge schema doesn't require them. Specifically: `valueProp` as a single sentence ≤280 chars (the V3 bridge's existing `description` field can carry it), `methods` as a structured array (the V3 bridge can ignore it during render), `limitations` as a bulleted list in the MDX body that the migration script can promote to frontmatter at crossover.

**- [ ] Action R-2.2:** Update the V3 bridge's `src/content/config.ts` schema to **accept** (but not require) `valueProp`, `methods`, `limitations` fields — passthrough. This lets Sean write redesign-shape MDX into the V3 bridge today, and the migration script becomes mostly a `beat → surface` mapping + ISO date strict cast.

**- [ ] Action R-2.3:** The migration script `migrate_v3_transactions.mjs` (transactions §11.1) is currently spec-only. When authored, its interactive prompt should detect already-present `valueProp` / `methods` / `limitations` fields and skip the "Sean reviews each row" step for them.

---

### R-3: Daily Driver agent extension required before Phase 2 ships

**Where it lives:**
- Hero spec §8 (line 202): `/api/dateline.json` — the **existing** Daily Driver write step (per superuser-pack v3.16.0 morning-mode preamble).
- Projects spec §4 (line 135): `/api/next-piece.json` — NEW; reads earliest-upcoming-ship-date from the roadmap's anchor list.
- About spec §8.1 (per BLUEPRINT §3.6): `/api/about-pulse.json` — NEW; LAST 24H strip.
- Case-study spec §15 (per BLUEPRINT §3.6): `/api/shipped-stats-<slug>.json` per SHIPPED page — NEW; live install counts via npm/GitHub public HTTPS (no MCP).
- Hero spec §8 again: `ledger_row` rotation pattern — NEW (compared to the existing 4 patterns: `fleet_pulse`, `ship_log`, `reading_log`, `now_line`); reads `src/content/transactions/*.md` filesystem to render.

**Why this matters:** Phase 2 DoD (hero spec §15 item 1) requires the dateline reads from a real `dateline.json` written by the Daily Driver overnight — NOT a hardcoded string. The build session hand-off prompt (Appendix B) says "hardcode the dateline JSON for now (`fleet_pulse` pattern, today's date, current vault indexer numbers)" — so the hardcode is acceptable for the **build session** but not for **DoD**.

The Daily Driver lives in [`agents-sdk/agents/daily_driver.py`](../../../agents-sdk/agents/daily_driver.py). Extending it to write 4 new endpoints is **the most coupled action between the roadmap layer and the portfolio layer.** It's a separate work item from anything in the unified roadmap currently.

**Recommended action — scope a Daily Driver extension ticket, gate Phase 4 DoD on it:**

**- [ ] Action R-3.1:** Open a new file `docs/superpowers/plans/2026-05-19-daily-driver-portfolio-endpoints.md` (separate from this audit) scoping the 4 new endpoint writers + the `ledger_row` pattern. Single-agent, single-file, ~200-300 lines of Python. Fits comfortably inside one Cowork session.

**- [ ] Action R-3.2:** Phase 2 builds against hardcoded `dateline.json` (per hero spec Appendix B). Phase 4 DoD requires the Daily Driver extension to be live (writes the file each morning at 08:45). Sequence Daily Driver extension between Phase 3 ship and Phase 4 launch.

**- [ ] Action R-3.3:** Hero spec §15 DoD item 1 stays unchanged. The build session that closes Phase 4 verifies the dateline reads from a real file ≤24h old.

---

## MINOR findings (resolve at the spec-lock pass; non-blocking for Phase 2)

### M-1: Date drift in roadmap Task 13

**Where it lives:** Roadmap line 901 heading: *"Task 13 — Access-vs-Meaning Manifesto + Spectrum Map (Council Gap-Fill 2; NEW 2026-05-17 — **draft-lock 2026-05-23**, publish ~2026-06-19)"*. Body of Task 13 (e.g., line 959) consistently references **2026-05-22** as draft-lock. PMP §6 and Blueprint also reference 2026-05-22.

**Recommended action:**

**- [ ] Action M-1.1:** Fix the roadmap heading at line 901 — change `draft-lock 2026-05-23` → `draft-lock 2026-05-22` to match the body's authoritative date. Or, if Sean's intent is actually 5/23, update PMP §6 + Blueprint §2's references too. **Recommended:** body wins — fix the heading.

---

### M-2: PMP §0.5 references "2026-05-06-unified-roadmap copy.md" (with " copy" suffix)

**Where it lives:** PMP §0.5 (line 32) + PMP §11 (line 401) — both reference `2026-05-06-unified-roadmap copy.md` (with literal "copy" in the filename). The canonical roadmap path is `2026-05-06-unified-roadmap.md` (no copy suffix).

**Why this matters:** Both link targets 404 in the rendered PMP — the file with " copy" doesn't exist in the vault.

**Recommended action:**

**- [ ] Action M-2.1:** Replace both link targets in PMP with `2026-05-06-unified-roadmap.md` (no " copy" suffix). It's a stale link from an earlier draft of the master plan.

---

### M-3: The portfolio repo path in build session hand-off prompts uses `/BMAD/`

**Where it lives:** Multiple Appendix C hand-off prompts (hero, projects, transactions, architecture, essays specs) say *"Open a Claude Code session at `/Users/seanwinslow/Code-Brain/BMAD/sw-ai-pm-portfolio/`."* The actual repo path is `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio/` (no `BMAD/` prefix per the symlinks + the user's earlier context).

**Recommended action:**

**- [ ] Action M-3.1:** When closing the spec-lock pass, do a `grep -l "Code-Brain/BMAD/sw-ai-pm-portfolio" docs/specs/*.md` and replace with `Code-Brain/sw-ai-pm-portfolio`. Affects ~8 hand-off prompts. Pure string replacement; no behavioral change.

---

### M-4: Texture-and-artifacts spec not reviewed in this audit

**Where it lives:** [`sw-ai-pm-portfolio/docs/specs/texture-and-artifacts-spec-v1.md`](../../../../../sw-ai-pm-portfolio/docs/specs/texture-and-artifacts-spec-v1.md) (770 lines, modified 5/19).

**Why this matters:** The texture-and-artifacts spec is a **foundations** spec — covering paper texture, registration marks, torn-paper edges, pencil annotations. It doesn't interface with the roadmap directly (no upstream canonical sources, no schema). But it's referenced by every other spec for visual primitives, and it was recently modified (per git status).

**Recommended action:**

**- [ ] Action M-4.1:** Sean reviews texture-and-artifacts spec separately as part of the spec-lock pass (Action I-3.1). It's a foundations spec; if it locks alone, the build can rely on the visual primitives.

---

## What's strongly aligned (no action needed — record for confidence)

These are the wins. Listed so the spec-lock pass doesn't accidentally drift them.

### A-1: Slug naming aligned end-to-end

Every artifact has one canonical kebab-case slug used identically in the roadmap MDX paths, the spec frontmatter examples, the cross-link target references, and the URL routing:

- `intent-engineering-mcp` (Tasks 1+3 / projects A-3 / case-study spec §13.3)
- `phase-d-typed-edges` (Task 2 / V3 ledger / `previousVersion` examples)
- `knowledge-loop-phase-6` (Task 2 / V3 ledger)
- `vault-synthesizer-eval-suite` (Task 8 / ledger)
- `substack-drafter` (Task 9 / ledger)
- `vault-knowledge-mcp` (Task 10 / `/architecture/` second occupant)
- `judge-layer` (Task 12 / ledger)
- `meaning-over-access` (Task 13 / `/essays/` first occupant + paired ledger row)
- `control-architecture` (Task 14 / paired `/architecture/` writeup + ledger row)
- `vault-scorecard` (Task 15 / `/architecture/` first occupant + paired ledger row)
- `animation-pipeline`, `superuser-pack`, `the-block`, `16bitfit` (case-study A-1, A-2, A-4, A-5)

### A-2: IA shape aligned (4 surfaces + `/about/`)

Roadmap Task 13 line 910 + Task 15 + Task 14 all assume four content-collection surfaces alongside `/about/`:
- `/work/` (5 curated case-study tiles — projects-spec)
- `/transactions/` (exhaustive ledger — transactions-spec)
- `/architecture/` (3-5 architectural arguments — architecture-spec)
- `/essays/` (thesis-shaped writing — essays-spec)

PMP §10 Decision 7 default + site-chrome spec §2.1 + Blueprint §3.1 all confirm this. Same as the roadmap.

### A-3: Task 11 fleet dashboard wired correctly

Roadmap Task 11 DEPLOYED 2026-05-18 at [fleet.seanwinslow.com](https://fleet.seanwinslow.com). Hero spec §14 + site-chrome spec §7 both correctly **link out** instead of embedding (the original Cloudflare-Worker-reads-CSV plan was descoped).

### A-4: STOP-DOING items honored across specs

Roadmap Task 7 + Council Deprioritization 1 + 2:
- **HybridRouter NOT framed as "Agent OS" / "runtime architecture"** — PMP §3.4 enforces this; essays §5 explicit STOP-DOING block; only one paragraph inside the Control Architecture writeup's Authority section earns the public surface.
- **No optimization toward TalentBoard** — Gap-Fill 3 amendment shipped the ledger standalone; no TalentBoard dependency anywhere in the specs.

### A-5: Task 11 → Task 12 / Task 14 telemetry handshake

Roadmap Task 11 §Compounding payoff (line 810): "Becomes the telemetry consumer for Task 12 (Judge Layer judge-outcome distribution + judge-availability panels) and Task 14 (Authority/Recovery/Audit control-plane dashboard upgrade)." The portfolio specs don't depend on this handshake directly — the portfolio only links out to the dashboard at `fleet.seanwinslow.com`. Clean separation.

### A-6: Tier-A discipline preserved across specs

Every spec's "what's NOT in the schema" section, every Definition-of-Done block, every voice-register table honors:
- Walk-away $100k (not a portfolio concern)
- AI PM > Tech PM > Creative PM (positioning encoded in every voice register choice)
- Agents draft / Sean sends (Daily Driver writes JSON endpoints from filesystem only — no MCP; Sean owns every LinkedIn, Substack, and tile-tagline word)
- Track-C protected (intent-engineering MCP shipped 5/12, redesign doesn't gate on it)
- 5:30 PM hard stop (no schedule-driven build pressure in the spec text)

---

## Execution sequence — what to do in what order

Based on every finding above, the recommended sequence between today (2026-05-19) and the Phase 2 build session:

### Now (next ≤2 hours) — author-time fixes to the locked spec layer

1. **- [ ] C-1**: Add the free-text → canonical surface remap table to `transactions-spec-v1.md` §12.3
2. **- [ ] C-2.1**: Add the 2026-05-19 hero spec changelog entry patching the MCP embed URL note
3. **- [ ] I-1.1**: Apply the `relatedArchitecture` additive to `transactions-spec-v1.md` §3.2 + changelog entry
4. **- [ ] M-1**: Fix the roadmap Task 13 heading date (5/23 → 5/22)
5. **- [ ] M-2**: Fix the PMP §0.5 + §11 stale `unified-roadmap copy.md` link targets
6. **- [ ] M-3**: Replace `Code-Brain/BMAD/` with `Code-Brain/` in all 8 spec hand-off prompts

### Today / tomorrow (within 24h) — open decision pass

7. **- [ ] I-2**: Walk PMP §10 open decisions #3, #4, #5, #7, #8, #9 in one pass; confirm or switch each.
8. **- [ ] I-3**: Walk the 6 drafted specs' open-questions sections; confirm or switch each default; flip each spec from `DRAFTED` → `LOCKED` in §1.1.
9. **- [ ] M-4**: Lock texture-and-artifacts spec at the same time.

### Tuesday / Wednesday (2026-05-20 / 5/21) — pre-build infrastructure

10. **- [ ] R-1.3**: Author `KNOWN-UPSTREAM-PENDING.md` at the portfolio repo root.
11. **- [ ] R-2.2**: Widen the V3 bridge `src/content/config.ts` schema to accept (not require) the redesign-shape fields. Defensive author-now-migrate-friendly-later move.
12. **- [ ] R-3.1**: Scope the Daily Driver extension in `docs/superpowers/plans/2026-05-19-daily-driver-portfolio-endpoints.md` (separate plan; doesn't gate Phase 2).

### Wednesday onward — Phase 2 build session unblocked

The Hero + Projects build (PMP §9 Phase 2) can start as soon as items 1-6 land. The remaining items (7-12) work in parallel without blocking the Phase 2 session — Hero and Projects don't depend on the unlocked specs, the V3 schema widening, or the Daily Driver extension.

---

## Self-Review

**Spec coverage:** Every roadmap task that ships content into the portfolio (1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15) is mapped against a spec surface and a finding (or A-N alignment record). Every spec with open questions is mapped against a finding. Every PMP §10 open decision is mapped against a finding. ✓

**Placeholder scan:** Each recommended action has a concrete file:section reference + the literal change to make (verbatim copy-paste-able). No "fix this later" / "TBD" / "Sean adjudicates" without a specific recommended-default + switch-only-if condition. ✓

**Type consistency:** "V3 bridge" = `~/Code-Brain/sw-ai-pm-portfolio/` (post-2026-05-08 scaffold) shipping Mon 2026-05-19 to seanwinslow.com via Vercel. "Redesign" = same repo, post-build-session-1 state. Same domain, same Vercel project, different schema + surfaces. No collision. ✓

**Tier-A check:** Audit recommendations don't push anything below the operating-model truths. Hardest case: PMP §10 Decision 4 (Block case study framing) — handled via spec OPEN-3 deferral to "frame-the-work, not the exit" content draft, not portfolio infrastructure. ✓

**What this audit does NOT do:**
- Review the texture-and-artifacts spec (foundations, decoupled from roadmap)
- Review the about-spec body content (out of scope — biographical, not roadmap-coupled)
- Review the case-study-spec body for The Block / 16BitFit framing (Block content review is a separate work item per PMP §10 Decision 4)
- Propose any net-new specs or roadmap tasks (audit-only; no expansion)

---

## Execution Handoff

This audit is the input to two next-session decisions:

**Option 1 — Author-time fix pass (recommended; ~2 hours):** Sean opens the 6 author-time fixes (CRITICAL + IMPORTANT items I-1, M-1, M-2, M-3) in one Cowork session. Likely 30-60 min total. Spec layer is then internally coherent.

**Option 2 — Lock-pass session (recommended next; ~2-4 hours):** Sean walks every open question across PMP §10 + the 6 drafted specs' §17/§19. Confirms or switches each. Closes the spec-lock state in one pass. The portfolio is then build-ready.

After both passes close, the Phase 2 build session (Hero + Projects per their respective Appendix B/C hand-off prompts) opens unblocked.

---

*Drafted 2026-05-19. Pre-build alignment audit for [`~/Code-Brain/sw-ai-pm-portfolio/`](../../../../../sw-ai-pm-portfolio/) against [`unified-roadmap.md`](../../../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md). Reviewed by Sean Winslow before Phase 2 build kickoff.*
