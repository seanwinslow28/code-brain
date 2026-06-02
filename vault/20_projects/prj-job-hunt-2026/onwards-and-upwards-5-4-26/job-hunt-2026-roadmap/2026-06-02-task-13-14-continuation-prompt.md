---
type: continuation-prompt
for: "Tasks 13 + 14 (Phase A stragglers — Access-vs-Meaning Manifesto close-out + Authority/Recovery/Audit build)"
created: 2026-06-02
paste_into: fresh Claude Cowork session
---

# Kickoff prompt — paste everything below the line into a fresh Cowork session

---

We're finishing the two remaining Phase A stragglers from my AI PM job-hunt roadmap: **Task 13 (Access-vs-Meaning Manifesto)** and **Task 14 (Authority / Recovery / Audit Reframe)**. Same working style as always: use a task list; **research/verify first, then build**; explain the WHY and the tradeoffs as you go so I can defend the choices in interviews; and **STOP at any real fork** to let me choose. Tier-A discipline: **agents draft, I send**. Do **not** auto-commit — Obsidian-Git owns `vault/` auto-commit; the `code-brain` repo (non-vault: `docs/`, `agents-sdk/`, `tools/`) and the `sw-ai-pm-portfolio` repo are mine to commit by hand. Be concise and direct.

## FIRST — re-read state, don't trust this prompt blindly

This prompt was written by a prior session and the roadmap moves fast. Verify before doing anything:

1. **Task specs** — `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`. Read the **Task 13** block (search "Task 13 — Access-vs-Meaning") and the **Task 14** block (search "Task 14 — Authority / Recovery / Audit"). Each has the full step list, locked architecture, and verification gate. Also read **Task 7 — STOP-DOING** (it forbids the "Agent OS" framing — load-bearing for Task 14) and skim the **Task 12 (Judge Layer)** status (Task 14 cross-links its `JUDGE_UNAVAILABLE` ledger entry).
2. **Completion log** — `unified-roadmap-completion-log.md` (same dir). Read the Task 13 entries (`2026-05-21` Steps 2-3, `2026-05-22` Steps 4-6) and the recent ship history so you know what's already shipped.
3. **Open host items** — `vault/00_inbox/tickets.md`.
4. **Task 13 prep doc** — `2026-05-20-task-13-step-1-manifesto-outline.md` (same dir).

Then give me a **3-line state-of-play** and **confirm the plan for each task before building**.

## IMPORTANT — Task 13 is mostly DONE; verify before doing redundant work

Per the roadmap status (2026-05-22), Task 13's **draft-lock gate already PASSED**. These shipped and exist on disk — confirm them, don't recreate them:
- `docs/MEANING_OVER_ACCESS.md` (the ~1,500-word manifesto, 5 sections + inline Mermaid quadrant chart)
- `docs/diagrams/access-meaning-spectrum.{mmd,svg}` (the spectrum chart source + render)
- `docs/MEANING_OVER_ACCESS_EXPLANATION.md` (the 4Q artifact)
- `sw-ai-pm-portfolio/src/content/essays/meaning-over-access.mdx` (the live `/essays/` page) + the `/essays/` IA
- `vault/.../substack-drafts/2026-06-19-meaning-over-access-substack-cross.md` (the cross-post, held for publish day)

So **Task 13's only remaining work is the Step 7 close-out** (Step 8 publish is ~6/19 and is OUT OF SCOPE here — I handle Substack/LinkedIn publishing myself):
- Re-validate the role-map JD URLs (200-OK check); the spec warned they rot between draft-lock and publish.
- `python3 scripts/validate.py` → confirm ≤60 warnings / 0 errors.
- Confirm `npm run build` (or the essays validator) still resolves `/essays/meaning-over-access/` in `sw-ai-pm-portfolio`.
- The 2026-05-22 cold-read flagged two voice spots for me to look at (NOT auto-fixed per Tier-A): §2 ¶3 "stop letting the agent guess" and §2 ¶5 "specifically to make this point". **Surface these to me** — I'll decide whether to run `writing-voice-modes` on them.
- Prep (don't run) the commit + tag `gap-fill-2-draft-locked` across `code-brain` + `sw-ai-pm-portfolio`; leave clean git status + suggested commit messages.

If your re-read shows anything beyond this still open on Task 13, flag it.

## Task 14 is the real build — Authority / Recovery / Audit Reframe

**What it is (the why):** Nate B Jones's §3.7 names a control-architecture trinity — Authority, Recovery, Audit — that Forward-Deployed / enterprise AI PM buyers look for. I've already *implemented* all three (cost caps + circuit breakers + keychain-gated keys + Pushover escalation + append-only JSONL ledgers); it's currently framed only as "cost discipline." Task 14 **reframes the existing infrastructure** as the named trinity and adds a tiny runnable demo. It's the **FDE-shaped artifact** — direct match to the Anthropic FDE Boston JD — and closes my one "beginner" gap (cost economics) with a worked example. ~80% of the substance already exists; the work is the naming, the worked example, and a small demo harness.

**Deliverables (per the Task 14 spec — verify exact paths/line numbers against the live files, they may have drifted):**
- `agents-sdk/docs/CONTROL_ARCHITECTURE.md` — the main ~1,500-word artifact: three sections (Authority / Recovery / Audit) mapping 1:1 to Nate §3.7, + a Mermaid sequence diagram (breach → block → ledger write → Pushover ping → rollback), + the worked-example walkthrough. Cite the real implementation: `agents-sdk/config.toml` (per-query/daily/monthly caps; `fallback_disabled=true` on Job Feed), `agents-sdk/lib/keychain.py`, `agents-sdk/lib/pushover.py`, the `vault/health/*-spend-*.json` ledgers, CLAUDE.md hook exit-code semantics + rollback lines, `agents-sdk/lib/concept_edges` provenance.
- `tools/governance-demo/` (new sidecar, sibling to `tools/llm-council/`): `replay_budget_breach.py` (`--fixture {allowed,over_budget,missing_auth}`, `--dry-pushover` flag), the three `fixtures/*.json`, `outputs/sample_ledger.jsonl`, and `test_replay.py`.
- `agents-sdk/config/authority.example.yaml` — sanitized declarative policy example (generic cost numbers, no real caps).
- `agents-sdk/docs/EXPLANATION.md` — the 4Q artifact (feeds the ledger row).
- Ledger row `sw-ai-pm-portfolio/src/content/transactions/control-architecture.mdx` — **note: `.mdx`, not `.md`** (the spec says `.md`, but the live transactions collection uses `.mdx`; schema-match to an existing row like `code-brain-system-card.mdx`, inline-body 4Q). Run `node scripts/validate_content.mjs` after.
- Update `CHANGELOG.md` / `CLAUDE.md` / `README.md` in `code-brain` per the mandatory doc rule.

## Locked decisions for Task 14 (don't re-litigate; confirm and go)

- **NO "Agent OS" / "runtime architecture" framing.** HybridRouter gets **exactly one paragraph** under Authority ("authority over which brain runs which task"), with an explicit deferral linking the Task 7 STOP-DOING entry. This is the load-bearing credibility guardrail — Council Deprioritization 1: framing ~100 lines of routing logic as "Agent OS" invites senior-engineer screen questions (concurrency, distributed caching, thread locking) I can't win at my coding level. Hold this line across the whole build; self-check during the editorial pass.
- Three sections map 1:1 to the trinity; the demo is a **forced over-budget call** exercising all three legs in 60–90s.
- Voice: sober/declarative work-artifact body (it's docs); any personal-voice flourish is mine to add. The LinkedIn post + Loom (Step 6) are **out of scope** — I do those myself.

## Critical environment constraints (so you don't try and fail)

- **The sandbox cannot fire Pushover or read the macOS Keychain.** Build `replay_budget_breach.py` + the fixtures + `test_replay.py` and run `pytest` in-session with Pushover **mocked / `--dry-pushover`**. The verification-gate criterion that it "fires a *real* Pushover notification" and the `--fixture over_budget` live run are **host-side (my machine)** — prepare them and hand me the exact commands. Don't attempt live paging from the sandbox.
- The demo script calls a **stubbed** agent runner (no real Gemini DR / Council spend). Make the fixtures obviously synthetic and note the stub boundary in `tools/governance-demo/README`.
- Writing to `vault/health/` during a demo run is host-side; in-session tests should write to a temp dir or fixture path, not the real ledgers.

## Sequencing

1. **Task 13 close-out first** (it's ~30–45 min: verify shipped state, JD-URL recheck, validate.py, surface the 2 voice flags, prep commit/tag). Quick win, clears the board.
2. **Task 14 build** (the real work: 3-section doc + demo harness + tests + example YAML + 4Q + ledger row). Build it in stages; run pytest as you go.

## Verification gates (build a final task for each)

**Task 13 (draft-lock close-out portion only):** role-map JD URLs 200-OK (or snapshotted with a `last_validated` note if any rot); `validate.py` ≤60 warnings / 0 errors; `/essays/meaning-over-access/` resolves; the 2 voice flags surfaced to me; commit + tag prepared (not pushed).

**Task 14 (per the spec):** `CONTROL_ARCHITECTURE.md` has the 3 named sections + Mermaid sequence diagram + exactly ONE HybridRouter paragraph (not a section); all three fixtures exercise distinct code paths verified by `pytest`; `outputs/sample_ledger.jsonl` has one captured entry per fixture; `authority.example.yaml` + `EXPLANATION.md` land; ledger `.mdx` row validates clean via `node scripts/validate_content.mjs`; CHANGELOG/CLAUDE/README bumps land. (The live `--fixture over_budget` run returning exit code 7 + real Pushover ping, and the Loom/LinkedIn, are host-side and excluded here.)

**Consider offering** the premium LLM-Council stress-test on `CONTROL_ARCHITECTURE.md` after the draft (same play as the Code-Brain System Card + the Discovery PRD) — it's a strong candidate since FDE buyers will read it hard. Offer it; don't auto-run (it runs host-side via Claude Code — the Cowork sandbox blocks `openrouter.ai`).

## When done

Status blockquote in the roadmap for each task (check the step boxes); full narrative in the completion log; host close-outs (commits, Loom, LinkedIn, the host-side Pushover demo, the ~6/19 Substack publish for Task 13) captured in `tickets.md`. Leave clean git status + suggested commit messages for both repos.

## Micro-forks to surface to me (don't decide alone)

- Task 13: whether to run `writing-voice-modes` on the two flagged spots, or leave them.
- Task 14: ledger `surface` value for `control-architecture.mdx` — the spec suggested `"control architecture (docs)"`; confirm against the live `SURFACE_ENUM` in `sw-ai-pm-portfolio/src/content/config.ts` (likely `infra` is the closest valid enum) and ask me which.
- Task 14: whether to run the LLM-Council stress-test before I commit.
