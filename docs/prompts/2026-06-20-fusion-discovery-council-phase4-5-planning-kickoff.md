# Kickoff Prompt — Plan fusion-discovery-council Phases 4 & 5 (writing-plans)

Paste the fenced block below into a fresh Claude Code session at the repo root (`/Users/seanwinslow/Code-Brain/code-brain`). Its job is to **write the next two implementation plans** (not execute them).

---

```
fusion-discovery-council is a live, working, MERGED PM-lens discovery skill (PR #86, squash-merged to
main). Phases 1–3 shipped: a 4-stage pipeline (GATHER → FUSE → VERIFY → FRAME) that mines fresh
real-URL evidence, fuses it through an OpenRouter Fusion panel, drops anything not traceable to a
fetched source, and frames survivors as a ranked PM idea ledger. 93 tests green, live-confirmed
($0.36 ledger). Your job THIS session is to write the next TWO implementation plans — Phase 4 and
Phase 5 — using the writing-plans skill. DO NOT write feature code. Your deliverable is two plan docs.

═══ STEP 0 — SYNC + BRANCH ═══
The work is merged to main (squash-merge, so the old feat/fusion-discovery-council branch is collapsed
— do NOT reuse it). Run: `git checkout main && git pull`, then `git checkout -b feat/fusion-discovery-council-phase4-5-plans`.

═══ STEP 1 — READ ALL CONTEXT (in this order) ═══
Design + prior work (the format + grounding style to replicate exactly):
- Spec: docs/superpowers/specs/2026-06-20-fusion-discovery-council-design.md
  (§4 the --lens flag, §5 stage definitions INCLUDING the substack lens, §6 the coverage matrix = the
   extended-collectors menu, §9 output conventions)
- Prior plans (mirror their header/global-constraints/file-structure/bite-sized-TDD format):
  docs/superpowers/plans/2026-06-20-fusion-discovery-council.md  (Phase 1)
  docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase2.md
  docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase3.md

SOURCE OF TRUTH for what carries forward — the three field reports (read all, lean on Phase 3 §7):
- tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase1-field-report.md
- tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase2-field-report.md
- tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase3-field-report.md
  → §7 is the actionable backlog: 7a open tickets, 7b deferred code nits, 7c PHASE 4 SCOPE,
    7d PHASE 5 SCOPE, 7e Phase-1 minors, 7f live-run observations (incl. re-check tier $ caps).
- Verified API/model facts: tools/llm-council/council/discovery/FUSION_SCHEMA.md
- Open tickets: vault/00_inbox/tickets.md (Fusion=RESOLVED; last30 INCLUDE_SOURCES=OPEN/external;
  GATHER-stage spend invariant=NEW/LOW)

═══ STEP 2 — GROUND IN THE CURRENT CODE (re-read every file before you reference it; your plans'
"Modify" steps must match the real, current line-by-line state) ═══
- Subpackage: tools/llm-council/council/discovery/{evidence,tiers,fusion,verify,frame,render,pipeline,__main__}.py
  and gather/{__init__,last30,sonar,web}.py
- Reused spine (do NOT duplicate): tools/llm-council/council/{budget,cli,client}.py
- Test patterns + fixtures: tools/llm-council/tests/discovery/* and tools/llm-council/tests/conftest.py
- The skill surface: .claude/skills/fusion-discovery-council/SKILL.md
- FOR PHASE 5 (substack handoff): read .claude/skills/substack-value-engine/SKILL.md so frame_substack
  emits a brief that skill actually consumes; note the chain it feeds (storytelling-architecture →
  writing-voice-modes → writing-humanity-pass → writing-critique).
- FOR any new last30 sources: ~/.claude/plugins/marketplaces/last30days-skill/scripts/lib/schema.py
  (the report.to_dict() shape).

═══ STEP 3 — WRITE TWO SEPARATE PLANS via the superpowers:writing-plans skill ═══
(The spec is large — decompose per the skill's scope check: one plan per phase.)

PHASE 4 — Extended collectors + fetch hardening
  File: docs/superpowers/plans/<today>-fusion-discovery-council-phase4.md
  Scope (spec §6 + Phase-3 §7c):
   • New tier-gated collectors, each following the gather/web.py search+fetch injection-seam pattern,
     slotted into gather_evidence() and gated via a TierConfig flag:
       – Review sites (G2/Capterra/Trustpilot/App Store/Play/Product Hunt) WITH competitor-weakness
         mining (harvest 1★/2★ reviews = "where competitors fail").
       – GitHub Issues + Canny/feature-request boards + public roadmaps (explicit upvoted unmet needs).
       – Demand/intent: Google People-Also-Ask + autocomplete question harvest.
       – Q&A: Stack Overflow/Exchange + Quora.
       – Trend velocity: Google Trends / Exploding Topics.
   • _simple_fetch SSRF / redirect allow-list (web.py) — do it HERE; the new collectors widen the
     fetch surface (Phase-3 §7c).
   • Quote-verbatim hardening: WebFetch Sonar citations to anchor verbatim text per URL (Phase-1 minor 6).
   • Fold the deferred §7b nits touching these files: _first_json_object scan-forward robustness
     (fusion.py); last30 timeout → module constant (last30.py).
   • COST-INTEGRITY RULE (§7a, explicit): if ANY new collector makes a paid call, thread its incurred
     cost into a typed gather-stage failure the same way FusionError.cost → DiscoveryFailed.cost_usd does,
     so a gather failure never silently records $0.
  Open design decisions to RESOLVE — surface to Sean via AskUserQuestion where genuinely forked, else
  default to the spec's stated principle ("lean, web-search + fetch, NO new paid scraper deps; Apify
  deferred"):
   • Which collectors ship in Phase 4 vs defer further.
   • Per source: free official API (GitHub Issues API, Stack Exchange API) vs site-targeted Brave/Exa
     search+fetch vs paid (Apify) — spec §3 default is web-search+fetch, no Apify.
   • Which tier (quick/standard/deep) gets which collector.
   • Re-check the per-run + daily/monthly $ caps — more collectors + any paid calls push cost up
     (Phase-3 §7f). Propose updated caps if needed.

PHASE 5 — substack lens + segment qualifier
  File: docs/superpowers/plans/<today>-fusion-discovery-council-phase5.md
  Scope (spec §4/§5 + Phase-3 §7d):
   • frame_substack(): verified pain points → post angles + hooks + value-promise, packaged as a
     handoff brief consumable by the substack-value-engine skill (match its input — you read its SKILL.md).
   • Wire --lens substack through __main__.py + a render variant for the brief.
   • --segment qualifier (e.g. developer | creative | pm) that reshapes the gather queries toward a
     target audience — the Phase-1 run #2 insight (generic "creatives" returned developer pain).
   • Output path for the brief per spec §9; ensure it lands where the writing chain expects it.

For BOTH plans, every task is bite-sized TDD with COMPLETE code grounded in the real files (no
placeholders), and each plan starts with the standard header + a Global Constraints block copying the
verified constraints below.

═══ STEP 4 — SELF-REVIEW each plan (coverage vs spec + field reports; placeholder scan; type
consistency), fix inline, then commit each plan to the branch. ═══

═══ STEP 5 — DO NOT EXECUTE. After both plans are committed, offer the execution path
(subagent-driven, fresh session per phase) and produce a Phase-4 execution kickoff prompt in the same
shape as docs/prompts/2026-06-20-fusion-discovery-council-phase3-execution.md. Recommend Phase 4 before
Phase 5, but note Phase 5 can ship independently on today's 2–3 live sources. ═══

═══ GLOBAL CONSTRAINTS / GOTCHAS (carry verbatim into both plans) ═══
- Test command: `uv run --extra dev python -m pytest -v` from tools/llm-council/ — plain `uv run pytest`
  does NOT work (pytest is in the `dev` extra). Baseline after merge: 93 passed, 1 skipped.
- Python floor >=3.10. Co-located subpackage; reuse council client.py + budget.py; NO second HTTP
  client or spend file.
- Fabrication gate (verify.py) is SACRED — never weaken; every pain point traces to a real-URL quote.
- The skill never `git add`s vault/ (CLAUDE.md rule 8 — Obsidian-Git owns vault commits).
- Verified model IDs: `~google/gemini-pro-latest` (tilde = floating alias), `mistralai/mistral-medium-3-5`
  (hyphen). The bare `google/gemini-pro-latest` and dotted `mistralai/mistral-medium-3.5` 400. Others
  valid: anthropic/claude-opus-4.7, openai/gpt-5.5, x-ai/grok-4.3, deepseek/deepseek-v4-pro, Sonar variants.
- Caps (re-evaluate if Phase 4 adds paid calls): per-run quick $0.50 / standard $1.50 / deep $4.00;
  discovery daily $10 / monthly $50, tagged tool="discovery", isolated from council's $7/$40.
- Cost-integrity theme: never bill a provider and record $0.
- New skill/agent/script → update CHANGELOG.md + CLAUDE.md + README count tables (repo "When Modifying").
- last30 live yield is still blocked by the upstream INCLUDE_SOURCES=null crash (external config; the
  collector degrades safely to []). Note it; don't re-litigate. GATHER currently = Sonar + Brave web live.

DELIVERABLE THIS SESSION: two committed plan docs (Phase 4, Phase 5) + a Phase-4 execution kickoff
prompt. No feature code.
```

---

## Notes for Sean (not part of the paste)
- The next session **plans only** — it writes Phase 4 + Phase 5 as two separate plan docs (mirroring the Phase 1–3 format), then hands you an execution kickoff prompt for Phase 4. Same brainstorm-is-done → writing-plans → subagent-driven rhythm you've used all along.
- It will likely ask you a couple of focused scoping questions on Phase 4 (which extended collectors ship first; free APIs vs search+fetch vs paid Apify; tier placement; whether caps need bumping) — those are genuine forks worth your call.
- Optional before Phase 4 execution: the 30-second `INCLUDE_SOURCES=reddit,hackernews` env fix unblocks last30 as a 3rd live source.
- This prompt file lives at `docs/prompts/2026-06-20-fusion-discovery-council-phase4-5-planning-kickoff.md` for reference.
