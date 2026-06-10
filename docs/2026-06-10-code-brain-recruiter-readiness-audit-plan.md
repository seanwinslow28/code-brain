# Code-Brain Recruiter-Readiness: Audit + Phased Cleanup Plan

**Date:** 2026-06-10 · **Repo:** github.com/seanwinslow28/code-brain (PUBLIC, ~6,024 tracked files, 1.29 GiB packfile)
**On approval, first action:** write this doc to `docs/2026-06-10-code-brain-recruiter-readiness-audit-plan.md` (plan mode blocked writing it there directly) and **make the repo private** via `gh repo edit --visibility private` — the PII below is live on the public internet right now.

## Context

The repo is about to be shown to recruiters. Two problems: (1) job-hunt material and prompts/plans are scattered across 5+ locations; (2) genuinely private material (interview answers, SOUL/USER/HEARTBEAT, warm intros, finance/health data, **309 employer-confidential meeting transcripts**) is tracked and in git history. Decisions already made by Sean: history scrub via `git filter-repo` + force-push; private content stays on disk, gitignored; gated phase-by-phase execution. Decisions made during planning (AskUserQuestion, 2026-06-10): daily notes scrubbed private; knowledge graph stays public with a prune list; repo goes **private now** + GitHub Support ticket post-scrub to purge server-side unreachable objects; job-hunt home stays **in place** at `vault/20_projects/prj-job-hunt-2026/` (gitignored) to avoid breaking 5 runtime paths.

---

## PHASE 0 — Audit Report (discovery complete, read-only)

### 0.1 Privacy inventory (tracked = in working tree index; all tracked files are also in history)

**SEVERITY: CRITICAL — employer-confidential (The Block)**
| Path | Tracked | In history | Contents |
|---|---|---|---|
| `vault/30_domains/product-management/the-block-meetings-granola-notes/` | **309 files** | yes | Full Granola meeting transcripts from The Block — *not named in the mission brief; worst single exposure* |
| `vault/30_domains/product-management/media-team-ideas/` | 8 files | yes | Internal Block plans + a 1:1 meeting transcript |
| `the-block/` | 0 (untracked since PR #64) | **yes** (added in v3.15.0 commit `8d930d3`, removed `adfb1a2`) | Entire archived employer domain — history-only exposure |
| `_inputs/Interview-Answers-April-2026/the-block-domain/` (incl. 6.2MB `Sponsored-Courses-PRD.pdf`) | yes | yes | Block PRDs + interview source answers |
| `vault/30_domains/product-management/the-block-resume-info/` | no | **no — never committed** ✓ | verify again from clean clone in Phase 6 |

**SEVERITY: HIGH — personal PII / job-hunt**
| Path | Tracked | Contents |
|---|---|---|
| `vault/20_projects/prj-job-hunt-2026/` | 210 | warm-intros, per-company interview strategy for six named target companies, TMAY scripts, story banks, mock logs, 46MB phone recording `.mov` |
| `vault/05_atlas/operating-models/` | 17 | SOUL/USER/HEARTBEAT/operating-model/schedule-recs for 3 domains |
| `vault/10_timeline/daily/` | 102 | daily notes: job-hunt timeline ("day 37"), mood, schedule |
| `_inputs/Interview-Answers-April-2026/` | (in 115 `_inputs` files) | Layer 1–5 interview source answers |
| `_archive/Interview Responses/` | 6 | Block + **finance + workout** interview responses |
| `_archive/Sean-Winslow-Profiles-For-Context/` | 4 | personal-context profiles v1.x |
| `vault/Sean-Winslow-Full-Personal-Context-v2.0.md` + root `personal-context-v2-interview-prompt.md` | 2 | full personal context |
| `docs/Claude Code Personal Finance Info/` | 9 | finance docs |
| `.claude/skills/personal-finance/SKILL.md` | 1 | **gross/net income ($100K, [redacted]/mo), account limits (Chase $27K, Bilt $6K), spending patterns** — found by sweep, not in brief |
| `.claude/skills/writing-voice-modes/references/voice-samples.md` | 1 | raw autobiographical stories (lines ~87–150) — found by sweep |
| `vault/20_projects/prj-boston-move/` | 4 | move checklist, personal travel doc — found by sweep |
| `vault/20_projects/prj-personal-finance/` | 2 | personal finance project notes — found by sweep |

**REVIEW (content pass in Phase 1 sign-off / Phase 4):**
- `vault/knowledge/` (615 files) — public per decision; **prune list** of job-hunt-derived concepts (e.g. `ai-pm-landscape-for-boston-remote-hiring.md`, career-track/agent-ops-fdp concepts) to be enumerated and approved before Phase 5.
- `vault/40_knowledge/people/` (32 auto-stubs) — public researchers; verify zero contact emails.
- `vault/00_inbox/tickets.md` — keep; one redaction pass (job-hunt bullets).
- `vault/90_system/fleet-memory/` (3 tracked files) — content check.
- `docs/superpowers/plans/2026-05-09-the-block-resume-info-audit-and-conversion.md` — job-hunt adjacent.
- `_inputs/Podcast-AdOps-Calendar-Sync-Workflow/`, `_inputs/x402 Deep Research/` — Block-adjacent; review.

**CONFIRMED CLEAN:** `.env` **never committed** (empty `git log --all -- .env '**/.env'`) ✓ · `.remember/` untracked ✓ · `settings.local.json` ignored ✓ · `the-block-resume-info` never committed ✓ · council-spend JSONs ignored ✓

### 0.2 Bloat inventory (history blobs, largest first)
- `vault/.vault-index.db` — **19 historical commits × 13–18MB ≈ ~280MB of pack**; ignored now, history-only. Largest single win.
- `vault/20_projects/prj-job-hunt-2026/assets/...iPhone-recording-1.mov` — 46MB (covered by job-hunt scrub).
- Root `16bitfit-battle-mode/` — **full duplicate tree** (autoresearch/docs/lora-output/lora-training/pixel-quantizer), 43 tracked files incl. 38MB PSD + 6MB PNGs. The `.gitignore` rule only covers `creative-studio/16bitfit-battle-mode/lora-output/`. Dedupe + scrub.
- `_archive/Grok-Deep-Research/*.pdf` — 13.6MB + 7.1MB, history-only (no longer tracked).
- `.claude/skills/last30days/assets/` — 14MB vendored demo media (jpeg/mp3/png). Recommend trim (replace with README pointer to upstream skill).
- 3 tracked `node_modules` files (vendored bird-search) — untrack.
- `agents-sdk/models/kokoro/CHECKSUMS.txt` — fine, keep (text, not a binary).
- `.git` contains ~30 garbage `tmp_obj_*` files — filter-repo's repack cleans these.

### 0.3 Prompts/plans scatter map
- **Root (5):** `agent-wiring-plan-prompt.md`, `autoresearch-skill-optimizer-prompt.md`, `claude-code-restructure-prompt.md`, `personal-context-v2-interview-prompt.md` (PRIVATE), `SKILLS-AUDIT-v2.md`.
- **docs/ top level:** `vault-knowledge-mcp-build-kickoff-prompt.md` + cluttered top level (9 loose dirs/files incl. system-card pairs — fine but front-door tidy candidates).
- **docs/superpowers/{plans,prompts}/ (18):** existing skill-session convention — keep in place.
- **_inputs/ (4 safe prompts):** Agent-Prompts, GEM-Prompts, Prompts/* — technical, safe, relocatable.
- **Project-local (stay put):** `agents-sdk/docs/plans/` (good convention, mirror it), `creative-studio/16bitfit-battle-mode/prompts-and-summaries/`, `.claude/skills/last30days/docs/plans/` (55, skill-local).
- **Private (move with job-hunt content):** 49 continuation/handoff/plan files inside `prj-job-hunt-2026/`.

### 0.4 Reference-dependency map (what a move would break)
**Hard runtime deps — all avoided by gitignore-in-place strategy (no path changes):**
- `agents-sdk/config.toml` L14/491–492/526 — job_feed watchlist + roll_up_dir, substack-drafter output_dir → `prj-job-hunt-2026/...`
- `agents-sdk/agents/job_feed.py` (writes roll-up), `agents/daily_driver.py:107` (reads feed), `scripts/mock_interview_loop.py:65` (writes mock logs)
- `agents-sdk/lib/artifact_loader.py:20,29` + `config.toml:256` — hardcoded `05_atlas/operating-models/{domain}/{kind}.md`
- `agents-sdk/agents/knowledge_lint.py` — `_BROKEN_LINK_EXCLUDE_DIRS = {"the-block-meetings-granola-notes"}` (folder stays on disk → exclusion stays valid)
- Skills reading job-hunt paths (prose-level): daily-driver, time-management, work-operating-model, llm-council SKILL.md — unaffected.
**Files that DO move (root prompts → docs/) have zero runtime references** — only CHANGELOG mentions (historical, leave as-is).

### 0.5 What recruiters currently see
A stranger browsing today gets: an impressive agent-fleet architecture **and** your salary, bank account limits, full interview strategy for 6 named companies (including Anthropic), mock-interview self-grades, warm-intro contacts, 309 confidential transcripts from your previous employer, daily mood logs, and your personal life story — most of it one `git log` away even where untracked. The architecture story is real but buried under `_inputs/`, `_archive/`, 5 loose root prompt files, and a cluttered `docs/` top level.

---

## PHASE 1 — Target structure & policy design (for approval)

### 1.1 Consolidated private layer (stays on disk, gitignored, scrubbed from history)
**Job-hunt home: `vault/20_projects/prj-job-hunt-2026/` — in place, whole folder gitignored.** Strays consolidate INTO it via **plain `mv` (never `git mv`)** so private content never touches new commits:
```
vault/20_projects/prj-job-hunt-2026/
├── (existing: job-feed/, interview-prep/, warm-intros.md, onwards-and-upwards-5-4-26/, …)
└── source-material/                      ← NEW, consolidated strays
    ├── interview-answers-april-2026/     ← from _inputs/Interview-Answers-April-2026/
    ├── interview-responses-archive/      ← from _archive/Interview Responses/
    ├── personal-context/                 ← v2.0 from vault/, v1.x profiles from _archive/, root interview-prompt
    └── finance-info/                     ← from docs/Claude Code Personal Finance Info/
```
Other private content **gitignored in place** (runtime deps / Obsidian structure): `vault/05_atlas/operating-models/`, `vault/10_timeline/daily/`, `vault/20_projects/prj-boston-move/`, `vault/20_projects/prj-personal-finance/`, granola-notes + media-team-ideas folders, `voice-samples.md`.
**Sanitize-in-place (stays public as a portfolio demo):** `.claude/skills/personal-finance/SKILL.md` — replace the real financial profile (lines ~21–80) with placeholder values; real profile moves to a gitignored `references/financial-profile.md`. History copy scrubbed via blob replacement or path-rename trick (see 1.4 note).

### 1.2 Prompts & plans taxonomy (public reorg, `git mv`)
- **`docs/prompts/`** (NEW) ← root `agent-wiring-plan-prompt.md`, `autoresearch-skill-optimizer-prompt.md`, `claude-code-restructure-prompt.md`, `docs/vault-knowledge-mcp-build-kickoff-prompt.md`, `_inputs/{Agent-Prompts,GEM-Prompts,Prompts}/*` (subfolders preserved). Naming: `YYYY-MM-DD-slug-prompt.md` where dateable.
- **`docs/plans/`** (NEW) ← `SKILLS-AUDIT-v2.md` (renamed `2026-04-XX-skills-audit-v2.md`) + future cross-cutting plans. Mirrors `agents-sdk/docs/plans/`.
- **Stay put:** `agents-sdk/docs/plans/`, `docs/superpowers/{plans,prompts}/`, project-local prompt dirs.
- Remainder of `_inputs/` and `_archive/` reviewed at gate; goal: **both dirs gone from the public tree** (content moved to private home, `docs/prompts/`, or domain folders).

### 1.3 New `.gitignore` additions (appended as one commented block)
```gitignore
# ════ PRIVATE LAYER — personal/job-hunt material lives on disk, never on GitHub ════
# Job-hunt command center (job_feed/daily_driver/mock_interview_loop write here at runtime)
vault/20_projects/prj-job-hunt-2026/
vault/20_projects/prj-boston-move/
vault/20_projects/prj-personal-finance/
# Operating-model artifacts (SOUL/USER/HEARTBEAT — artifact_loader.py reads at runtime)
vault/05_atlas/operating-models/
# Daily notes (personal timeline; Obsidian-Git respects this and stops syncing them)
vault/10_timeline/daily/
# Personal source material & voice calibration
vault/Sean-Winslow-Full-Personal-Context-v2.0.md
.claude/skills/writing-voice-modes/references/voice-samples.md
.claude/skills/personal-finance/references/financial-profile.md
# Employer-confidential (The Block) — archived reference, local-only
vault/30_domains/product-management/the-block-meetings-granola-notes/
vault/30_domains/product-management/media-team-ideas/
# ════ BLOAT GUARDS ════
16bitfit-battle-mode/          # root duplicate of creative-studio/16bitfit-battle-mode — deduped Phase 4
.claude/skills/last30days/assets/
```
(`_inputs/` + `_archive/` need no rules if emptied; add `_inputs/` `_archive/` rules anyway as regression guards.)

### 1.4 History-scrub manifest (`git filter-repo --invert-paths`)
**PRIVATE-PII paths** (current + historical locations):
```
vault/20_projects/prj-job-hunt-2026/        vault/20_projects/prj-boston-move/
vault/20_projects/prj-personal-finance/     vault/05_atlas/operating-models/
vault/10_timeline/daily/                    the-block/
vault/30_domains/product-management/the-block-meetings-granola-notes/
vault/30_domains/product-management/media-team-ideas/
vault/30_domains/product-management/the-block-resume-info/   (defense-in-depth; believed never committed)
_inputs/Interview-Answers-April-2026/       _archive/Interview Responses/
_archive/Sean-Winslow-Profiles-For-Context/ docs/Claude Code Personal Finance Info/
vault/Sean-Winslow-Full-Personal-Context-v2.0.md
personal-context-v2-interview-prompt.md
.claude/skills/writing-voice-modes/references/voice-samples.md
.claude/skills/personal-finance/SKILL.md    (historical blob only; sanitized version re-added in same rewrite via Phase 3 commit ordering — sanitize FIRST in Phase 3, scrub only pre-sanitize blobs by path+blob-id, or simplest: scrub path entirely and re-add sanitized file in a fresh commit post-rewrite)
+ approved vault/knowledge/ prune list (enumerated at this gate)
+ any review-bucket items confirmed at this gate (x402, Podcast-AdOps, resume-info-audit plan doc)
```
**BLOAT paths:** `vault/.vault-index.db` · `16bitfit-battle-mode/` (root, after dedupe) · `_archive/Grok-Deep-Research/` · `.claude/skills/last30days/assets/` · `**/node_modules/` (3 files)
**KEEP:** everything else — `.claude/` skills/agents/hooks, `agents-sdk/`, `creative-studio/`, `life-systems/`, `vault/knowledge/` (minus prune list), `vault/40_knowledge/`, `docs/`, `evals/`, `tools/`, `scripts/`.
**Expected effect:** ~700 fewer tracked files (~6,024 → ~5,300), packfile shrinks from 1.29 GiB by roughly 400–500MB (index.db ~280MB + media + dupes).

### 1.5 Reference-update map (all changes needed; runtime deps untouched by design)
| Change | Files to update |
|---|---|
| Root prompts → `docs/prompts/` | none (no inbound refs); CHANGELOG mentions left as history |
| `_inputs` safe prompts → `docs/prompts/` | none found |
| personal-finance SKILL.md sanitize | the skill itself + new gitignored `references/financial-profile.md`; skill prose updated to "reads local profile from references/" |
| voice-samples.md gitignore | `writing-voice-modes/SKILL.md` note that reference file is local-only |
| CLAUDE.md | structure tree (`docs/prompts/`, `docs/plans/`, `_inputs`/`_archive` removal), new **privacy-layer rule** (list of gitignored-private dirs; agents must never `git add` them), note on root-16bitfit removal |
| README.md | front-door rewrite (1.6) |
| CHANGELOG.md | entries at Phases 3, 4, 6 |
| `scripts/validate.py` | no changes needed (doesn't check moved paths) — must stay green after each phase |

### 1.6 Recruiter front door
- **README rewrite:** lead with the system — architecture diagram, agent-fleet table (13 agents, cost-engineering story: $0 local routing, budget caps, circuit breakers), knowledge loop (flush → synthesizer → critic → lint), skills/hooks counts, governance demo, evals, system card. Add a deliberate **"Privacy boundary"** section: *"Personal operating data (job-search ops, daily notes, operating models) runs through this same system but lives in a gitignored private layer"* — turns the scrub into evidence of judgment.
- **docs/ top-level tidy:** loose system-card/explanation pairs stay (they're showcase); prompts/plans absorbed per 1.2.
- **Recruiter's-first-5-minutes walkthrough** delivered in Phase 6.

---

## Phase summary & gates (one screen)

| Phase | Actions | Gate (Sean approves before next) |
|---|---|---|
| **0–1 (this doc)** | Audit + design (done, read-only) | ✅ **GATE: approve structure, .gitignore, scrub manifest, knowledge prune list** |
| **2 Safety** | `gh repo edit --visibility private` (or confirm done manually) · `git clone --mirror` → `~/code-brain-backup-2026-06-10.git` · annotated tag `pre-recruiter-cleanup-backup` on HEAD · verify mirror (`git -C backup fsck` + ref count) · **Sean pauses Obsidian-Git on ALL machines (Mac Mini, MBP)** + confirm no launchd agent will commit during the window | GATE: backup verified + Obsidian-Git paused everywhere |
| **3 Public reorg** | `git mv` root prompts → `docs/prompts|plans/` · sanitize personal-finance SKILL.md · sanitize tickets.md pass · CLAUDE.md/CHANGELOG updates · `python3 scripts/validate.py` green · logical commits | GATE: review moves + green validation |
| **4 Untrack + consolidate** | install new .gitignore · `git rm -r --cached` all private+bloat paths · plain-`mv` strays into `prj-job-hunt-2026/source-material/` · dedupe root `16bitfit-battle-mode/` (diff vs creative-studio copy first; move uniques, delete dupes) · commit · verify `git status` clean + private files still on disk | GATE: review untracked set |
| **5 History scrub** ⚠️ | `git filter-repo --invert-paths` w/ approved manifest · show before/after (file count, `git log --all -- <private paths>` empty, pack size delta) · **GATE A: approve rewrite results** · re-add origin · `git push --force-with-lease` (+ all branches/tags) · **GATE B: second explicit confirmation before push** · then: reset/re-clone ALL other machine clones (MBP, Mac Mini) **before** they next push · GitHub Support ticket to purge unreachable objects · re-enable Obsidian-Git (local == remote post-push; verify one manual Obsidian-Git sync) | Two explicit gates as listed |
| **6 Verification** | fresh clone to temp dir · prove: zero private files, `git log --all` empty for every manifest path, secret scan (gitleaks if available, else targeted `git log -p` greps for $, account, salary, sk-, ghp_) · `scripts/validate.py` + `cd agents-sdk && pytest` green · live-fire smoke: one daily-driver `--dry-run` · "recruiter's first 5 minutes" walkthrough · final CHANGELOG entry · tickets for deferred polish · **then flip repo public** | Final sign-off → repo public |

### Risks & open flags (thinking-partner notes)
1. **Stale machine clones are the #1 re-exposure vector** — MBP has previously pushed from a stale checkout (PR #52 incident). Any push from an un-reset clone resurrects the old history. Phase 5 treats this as a blocking step, not a footnote.
2. **GitHub residue** — force-push leaves old commits SHA-fetchable until GitHub gc's; handled via private-now + Support ticket (your chosen path). Anything already scraped while public is unrecoverable — assume warm-intro names/comp data may have been crawled; nothing to do but scrub fast.
3. **Obsidian-Git after the rewrite** — local repo is rewritten in place by filter-repo, so local==remote after push; Obsidian-Git should resume cleanly. If it ever did a background fetch mid-window, its merge would conflict — hence pause-everywhere in Phase 2.
4. **Daily notes lose GitHub backup** once gitignored. Mitigation options (ticket): Time Machine already covers disk; or a separate private repo later.
5. **`tickets.md` and `vault/knowledge/` keep leaking job-hunt context over time** (flush/synthesizer write there nightly). Deferred ticket: add a privacy-aware filter to synthesizer/flush prompts, or accept and periodically prune.
6. **filter-repo availability**: verify `git filter-repo --version` in Phase 2; install via `brew install git-filter-repo` if missing.

## Verification (acceptance test, Phase 6)
From a fresh `git clone` of the rewritten repo: (a) `git ls-files | grep -iE 'job-hunt|interview|granola|operating-models|personal-context|finance info'` → empty; (b) for every manifest path, `git log --all --oneline -- <path>` → empty; (c) secret scan clean; (d) `python3 scripts/validate.py` green; (e) `cd agents-sdk && PYTHONPATH=. pytest tests/ -v` green; (f) daily-driver dry-run resolves all paths.
