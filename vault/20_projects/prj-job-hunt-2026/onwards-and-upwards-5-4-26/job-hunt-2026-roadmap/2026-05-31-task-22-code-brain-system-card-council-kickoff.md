---
type: kickoff-prompt
parent: 2026-05-06-unified-roadmap.md
task: Task 22 — DR3 Code-Brain System Card
project: prj-job-hunt-2026
created: 2026-05-31
target: Claude Code (interactive, on Sean's Mac)
ai-context: "Paste-ready Claude Code kickoff for Task 22. Builds docs/CODE_BRAIN_SYSTEM_CARD.md with a premium LLM Council stress-test pass. Points at every grounding file, the sibling-artifact pattern, the transactions schema, and the exact council CLI invocation + caps."
---

# Claude Code Kickoff — Build the Code-Brain System Card (Task 22) with the Premium LLM Council

Paste everything below the line into a fresh Claude Code session running from `/Users/seanwinslow/Code-Brain/code-brain`.

---

## Who I am and what we're building

I'm Sean Winslow — an AI Product Manager job-hunting (post-layoff, 8-week sprint). **Code-Brain** is my personal command center: an Obsidian vault plus an autonomous agent fleet built on the Claude Agent SDK. This task ships the **Code-Brain System Card** — a regulatory-accountability artifact that maps my *real, running* fleet to two frameworks enterprise AI-PM hiring managers care about: **SR-11-7** (Fed model-risk management) tiering, and **EU AI Act** technical documentation (Annex IV, Article 50 transparency, Article 61 post-market monitoring).

The credibility move — same one that made the Enterprise Data Readiness Matrix land — is that I'm not reciting a compliance framework abstractly. I'm applying it to a system I actually operate, and **naming the honest gaps**. A PM who's done the work, not a candidate who memorized acronyms.

This must read as a masterpiece: precise, sober, defensible line-by-line, and honest about where Code-Brain is *not* compliant. It is a **portfolio piece, not a regulated production system** — frame it as such (no overclaiming conformance).

**Output files:**
- `docs/CODE_BRAIN_SYSTEM_CARD.md` (1,500–2,500 words)
- `~/Code-Brain/sw-ai-pm-portfolio/src/content/transactions/code-brain-system-card.mdx` (the portfolio ledger row)
- `docs/CODE_BRAIN_SYSTEM_CARD_EXPLANATION.md` (4Q, optional but recommended — mirrors the Vault Scorecard pattern)

> Note: this artifact was renamed from "Superuser System Card" on 2026-05-31 (the project is now Code-Brain). The roadmap Task 22 block is already updated; the dated research docs keep the old name as historical record — don't rename those.

---

## STEP 0 — Read these first (do not draft a word until you've read them)

**The spec (authoritative):**
- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md` — find `### Task 22 — DR3 Code-Brain System Card` (~line 1331). The 7 steps + verification gate are the contract.
- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/unified-roadmap-completion-log.md` — for how sibling artifacts (Task 21, Task 15) shipped.

**The grounding research (this is where the SR-11-7 / EU AI Act substance lives — do NOT invent regulatory detail, cite from here):**
- `vault/20_projects/research/2026-05-18-enterprise-ai-pm-skill-gaps.md` — DR-Max Q2. SR-11-7 model-risk tiering, EU AI Act conformity, the named reference templates (Google Model Cards, Anthropic System Cards, EU Declaration of Conformity), and the original "System Card" artifact recommendation. **Primary source.**
- `vault/20_projects/research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md` — the Anthropic system-card pattern + eval methodology, with real URLs.
- `vault/20_projects/research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md` — system-card references, RSP domains, eval-as-required-human-review. Use for the validation-evidence section.

**The fleet inventory (the substance you'll be tiering — this is the source of truth for what's actually running):**
- `CLAUDE.md` (repo root) — the **authoritative current agent inventory**. Use the `agents-sdk/` "Agent inventory" table + the "Connected MCPs", "Connected External Research APIs", and "Architecture decisions" tables. The roadmap Step 1 lists ~11–12 components (vault_indexer, vault_synthesizer, deep_researcher, meta_agent, daily_driver, knowledge_lint, flush, gemini_researcher, intent-engineering MCP, LLM Council, Substack-Drafter, Judge Layer). **Reconcile against CLAUDE.md and map whatever is actually live** — if the count drifts from the Step-1 list (e.g. Vault Critic, Job Feed, Skill Optimizer also exist), map them too and note the reconciliation.
- `agents-sdk/config.toml` — cost caps, routing, the `[judge_layer]` table, the per-agent kill-switches. This is your evidence for the "controls already in place" + "cost economics" claims.
- `agents-sdk/lib/judge/EXPLANATION.md` + `agents-sdk/lib/judge/` — the Judge Layer (control plane, shipped 2026-05-31). This is the strongest single component for the "human-override path / post-market monitoring" columns — the JSONL ledger at `vault/health/judge_log/` IS a monitoring stream.
- `evals/vault-synthesizer/` — `README.md`, `cases.yaml`, `failure-modes.md`, `last-run.md`. This is your **validation evidence** for the synthesizer (Step 2). Note honestly which agents have an eval suite and which don't.
- `agents-sdk/docs/agents-sdk.md` — fleet architecture, launchd schedules, the headless-SDK-can't-reach-MCP limitation (a real trust-boundary fact).

**The pattern to mirror (study these — your card should feel like a sibling, not a new genre):**
- `~/Code-Brain/enterprise-data-readiness-matrix/` — `README.md`, `matrix.md`, `worked-example-fortune-500-content-co.md`, `EXPLANATION.md`. Task 21, shipped 2026-05-29. The "five dimensions reverse-engineered from my own fleet + a floor rule + a dated remediation plan + honestly-named gaps" structure is the template. Your card's equivalent of the floor rule: **materiality tier is set by the highest-risk action surface, not the average.**
- `vault/SCORECARD.md` + `docs/VAULT_AS_AGENT_INFRASTRUCTURE.md` — Task 15. The "real telemetry as the unfakeable backbone" + "HONEST NOTE where a competitor beats me" move. Steal the honesty calibration.

**Templates + schema (for the EXPLANATION + the ledger row):**
- `vault/40_knowledge/templates/EXPLANATION-template.md` — the 4Q comprehension scaffold.
- `~/Code-Brain/sw-ai-pm-portfolio/src/content/config.ts` — the `transactions` collection Zod schema (the frontmatter contract your `.mdx` ledger row must satisfy).
- `~/Code-Brain/sw-ai-pm-portfolio/src/content/transactions/enterprise-data-readiness-matrix.mdx` — the exact sibling ledger row to copy the frontmatter shape from (Task 21 used `surface: infra`; use the same surface unless the schema says otherwise).

**Voice (for the final pass):**
- `.claude/skills/writing-voice-modes/SKILL.md` — the card is "pure strategic writing": mostly **sober/declarative** (this is a compliance document), with a short Sean-voiced intro and close, exactly like the Vault Scorecard. Do NOT write the whole thing in comedic Sean Mode — the genre is a system card.

---

## STEP 1–6 — Draft the card (you, grounded; NOT the council)

The council models do not know my fleet internals — if they draft the mappings they will hallucinate. **You draft the fact-grounded card** from the files above. Follow the roadmap's 7 steps:

1. **Tier every live component to SR-11-7 (low/med/high materiality) with a one-line rationale.** Materiality = blast radius of a wrong action. Judge Layer's wrapped surface, Substack-Drafter (writes under my byline), Daily Driver (touches calendar/email context) rank higher; read-only indexers rank low.
2. **Validation evidence per component.** Link `evals/vault-synthesizer/` for the synthesizer; for each other agent, state plainly whether an eval exists, and which failure modes are documented in CLAUDE.md. Mark which have published post-mortems (e.g. the LDR grounding-collapse).
3. **Map trust boundaries to EU AI Act Article 50 (transparency) + Article 61 (post-market monitoring):** per public-facing component — does it self-identify as AI? what's logged for monitoring (the `vault/health/*` JSONL ledgers, the judge_log, the fleet dashboard)? what's the human-override path (the Tier-A "agents draft / I send" gate)?
4. **Annex IV-style technical documentation already in place:** training data = none (all production models are API or local-inference, no training); testing = eval suite + production logs; evaluation processes = documented in CLAUDE.md. State what exists.
5. **Honest gaps — this is the credibility core.** No formal post-market-monitoring report cadence; no Annex IV-conformant template; no Article 13 user instructions. Name each plainly. (Mirror the Vault Scorecard's HONEST NOTE calibration.)
6. **Reference templates, cited by URL:** Google Model Cards, the Anthropic Claude system cards, OpenAI system cards, EU Declaration of Conformity — pull the real URLs from the two eval-fluency research docs. Frame the card explicitly as a portfolio piece modeled on these, not a regulated filing.

Target 1,500–2,500 words. Use a tier table (component × SR-11-7 tier × rationale × eval evidence × override path) as the spine — tables survive screenshots and read fast, the same reason the Data Readiness Matrix uses one.

Save the v1 draft to `docs/CODE_BRAIN_SYSTEM_CARD.md`.

---

## STEP 6.5 — Stress-test the draft with the PREMIUM LLM Council

Now convene the council to find what I can't see. Read the skill first: `.claude/skills/llm-council/SKILL.md` (§2.4 PRD/spec stress-test is the closest template). This is a **premium-profile** run (4 frontier models cross-ranking + chairman synthesis) — appropriate because different vendors have different blind spots on regulatory framing.

**Cost discipline:** premium is ~$0.29–1.00/run; caps are $1.00/query, $7/day, $40/month, enforced by the CLI pre-flight. If it refuses on budget, surface the error verbatim and ask me before `--force`.

1. Write the critique prompt to `/tmp/llm-council/code-brain-system-card-stress-<timestamp>.md`:

   ```
   Stress-test the following AI "system card." It maps a personal AI agent fleet to
   SR-11-7 model-risk tiers and EU AI Act technical-documentation requirements. The
   author is an AI Product Manager using it as a portfolio piece to prove regulatory-
   accountability fluency to enterprise hiring managers (fintech, regulated SaaS).

   Each council member should independently surface:
   1. SR-11-7 mappings that are wrong, hand-wavy, or that a model-risk officer would
      reject — name the specific component and the corrected tier + reasoning.
   2. EU AI Act claims that misstate the regulation (Annex IV / Article 50 / Article 61)
      — quote the line and correct it.
   3. The single weakest "honest gap" framing — where the card either over-confesses
      (undersells the work) or under-confesses (claims more compliance than it shows).
   4. Anything that reads as a candidate performing rigor rather than demonstrating it.
   5. The one change that would most increase a hiring manager's trust.

   Quote specific lines/sections. Be ruthless — the author wants the strongest critique,
   not validation. This is a portfolio artifact, not a regulated filing; critique it as
   the strongest version of that.

   === SYSTEM CARD DRAFT ===

   [paste the full docs/CODE_BRAIN_SYSTEM_CARD.md draft here]
   ```

2. Run it (`mkdir -p` the parent of the output first):

   ```bash
   cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council \
       --profile premium \
       --prompt-file /tmp/llm-council/code-brain-system-card-stress-<ts>.md \
       --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-31-task-22-system-card-council-stress.md \
       --tag spec-stress-code-brain-system-card
   ```

3. Read the chairman synthesis + the four named drafts from the output file. Report back to me: the convergent corrections (fix these), the divergent ones (my call), and the single highest-trust change the chairman names.

---

## STEP 6.7 — Revise per the council

Apply the convergent, factually-correct fixes to `docs/CODE_BRAIN_SYSTEM_CARD.md`. For divergent calls, list them for me and recommend — don't silently pick. Never accept a council "fix" that asserts a fleet fact you can't verify in the source files (the council can be wrong about my internals — you have the files, it doesn't).

---

## STEP 7 — Ship

1. **Voice pass** — run the card through `writing-voice-modes`: sober/declarative body, short Sean-voiced intro + close. Strip emoji from prose (tables can keep tier marks). Match the Vault Scorecard register.
2. **4Q EXPLANATION** — write `docs/CODE_BRAIN_SYSTEM_CARD_EXPLANATION.md` per the template. <90-second cold read.
3. **Ledger row** — create `~/Code-Brain/sw-ai-pm-portfolio/src/content/transactions/code-brain-system-card.mdx` matching the `transactions` Zod schema in `config.ts` (copy the shape from `enterprise-data-readiness-matrix.mdx`). Then `cd ~/Code-Brain/sw-ai-pm-portfolio && npm run build` and confirm `/transactions/code-brain-system-card/` resolves.
4. **Validate** — `cd ~/Code-Brain && python3 scripts/validate.py` → PASSED / 0 errors.
5. **CHANGELOG** — add an entry to `CHANGELOG.md` (new doc + portfolio row).

---

## Guardrails (do not skip)

- **Honesty is the artifact.** The named gaps are what make it credible. Do not let the voice pass or the council soften them into nothing.
- **Don't auto-commit.** Obsidian-Git owns `vault/` auto-commit; `docs/` and the portfolio repo are mine to commit by hand. Stage nothing, push nothing — leave a clean `git status` and tell me the suggested commit message.
- **Tier-A:** this is canonical AI-PM > Tech-PM content; agents draft, I send; honor the council cost caps; don't fabricate regulatory text — cite from the research docs.
- **Reconcile the inventory** against the live CLAUDE.md and tell me if the component count differs from the roadmap's Step-1 list.

## Definition of done

`docs/CODE_BRAIN_SYSTEM_CARD.md` is 1,500–2,500 words; every live fleet component mapped to an SR-11-7 tier with validation evidence + override path; EU AI Act Article 50/61 + Annex IV coverage accurate; all gaps honestly named; reference templates cited by real URL; premium council stress-test run + its corrections applied; voice pass done; 4Q EXPLANATION written; the `code-brain-system-card.mdx` ledger row builds clean; `validate.py` PASSED; CHANGELOG updated; nothing committed; suggested commit message provided.
