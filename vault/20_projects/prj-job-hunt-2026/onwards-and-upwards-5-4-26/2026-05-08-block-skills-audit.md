---
type: audit
project: prj-job-hunt-2026
task: roadmap-task-0-step-1
created: 2026-05-06
target-completion: 2026-05-08
ai-context: "Line-by-line audit of Block-named/Block-contaminated skills in .claude/skills/. Output feeds Task 0 Step 2 (rewrite) + Step 3 (zero-hit grep verification). CIIA Section 2.3 compliance gate before any public Superuser Pack push."
---

# Block Skills Audit — Roadmap Task 0 Step 1

> Source: [unified roadmap](job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md) §Task 0. Each line marked **(T)** transferable or **(B)** Block-specific. (B) lines must be sanitized in Step 2 before the Step 3 grep returns zero hits.

## Baseline (2026-05-06 grep — corrected)

**Command (corrected, path-only filter):** `grep -rni "theblock\|the-block\|track insight\|@theblock\|swinslow@theblock" .claude/skills/ | grep -v ".git/"`

**Result:** 30 hits across 7 files. (Initial grep used `grep -v "the-block/"` which over-filtered — it dropped lines whose *content* references the-block paths from non-archive files. The corrected grep above keeps everything in `.claude/skills/`.)

| File | Hits | Scope |
|---|---|---|
| `.claude/skills/work-operating-model/SKILL.md` | 15 | `the-block` as selectable-archived domain in 4-domain list + Block-era tuning notes — parameterize per Plan A |
| `.claude/skills/etf-page-creator/SKILL.md` | 5 | Block-branded SEO templates + Track Insight references — full sanitize |
| `.claude/skills/api-product-management/SKILL.md` | 5 | `developer.theblock.co` + `@theblock/data-sdk` examples — full sanitize |
| `.claude/skills/jira-automation/SKILL.md` | 2 | Line 293 dead path to `the-block/product-management/templates/prd-to-launch.md` + line 304 `Campus vs theblock.co vs both` example — sanitize |
| `.claude/skills/work-operating-model/interview-questions.md` | 1 | `swinslow@theblock.co` archive note — parameterize |
| `.claude/skills/work-operating-model/artifact-templates.md` | 1 | `swinslow@theblock.co` example — parameterize |
| `.claude/skills/daily-driver/SKILL.md` | 1 | `swinslow@theblock.co` calendar archive line — parameterize |

**`stakeholder-update/SKILL.md` is fully clean** — the `biweekly-jira-update` merge happened cleanly with all Block strings already removed.

## Roadmap deviation surfaced by baseline (corrected 2026-05-06)

The roadmap Task 0 names 3 skills (`the-block-jira-ticket-writer`, `etf-page-creator`, `biweekly-jira-update`). Reality after Sean's clarification + grep:

- **`etf-page-creator`** — live in `.claude/skills/`. Confirmed contamination. **In scope.**
- **`the-block-jira-ticket-writer`** — was MERGED INTO `jira-automation/` when Sean first built the Superuser Pack. Folder at `docs/Additional Skills To Add To Claude Superuser/...` is the pre-merge source, not a duplicate live skill. The merge mostly sanitized it; 2 Block leaks remain in `jira-automation/SKILL.md`. **In scope via `jira-automation`.**
- **`biweekly-jira-update`** — was MERGED INTO `stakeholder-update/`. Merge happened cleanly; zero Block strings remain. **No work needed.**
- **`api-product-management`** — NOT in roadmap Task 0 list. Live in `.claude/skills/`. Contains `developer.theblock.co` + `@theblock/data-sdk` SDK examples. **In scope; surfaced as new sanitization target.**
- **`work-operating-model` (3 files)** + **`daily-driver`** — `the-block` is a selectable-archived domain in the 4-domain operating-model system. **In scope per Plan A — parameterize.**

## Decision (locked 2026-05-06): Plan A — full clean, all 30 → 0

Sean's call: clean every `the-block` string in `.claude/skills/` to zero, not just the IP-adjacent ones. Reasoning: legal layer (CIIA Section 2.3) only protects Block IP, but the readability layer matters more for the public Superuser Pack push. Every `the-block` string in a generic-looking skill creates recruiter-friction ("did he actually scrub it, or just the obvious parts?"). Zero is the only count that doesn't generate that question.

**Trade-off accepted:** `work-operating-model` will lose `the-block` as a literal selectable slug; replaced with `archived-employer` (or equivalent placeholder). Bundle still lives at `vault/40_archive/operating-models-the-block-2026-05/`, so historical interviews can still be re-run by mapping `archived-employer` → that path. Functional capability preserved; literal string removed.

## Skill 1 — `etf-page-creator/SKILL.md` line-by-line

Path: [.claude/skills/etf-page-creator/SKILL.md](../../../../.claude/skills/etf-page-creator/SKILL.md)

| Line(s) | Mark | Content / Note |
|---|---|---|
| 1–2 | **(T)** | Frontmatter `name: etf-page-creator` — generic; could rename to `structured-content-publisher` per roadmap line 183 but "etf-page-creator" itself is not Block-branded |
| 3 | **(B)** | `description:` references "Track Insight IDs" specifically — sanitize to "external data IDs" or parameterize |
| 6 | **(T)** | `# ETF Page Creator` heading — generic |
| 8 | **(T)** | "Create properly formatted WordPress ETF pages for a publishing platform" — already parameterized to "a publishing platform" (good) |
| 10–24 | **(T)** | Workflow Overview + Mode determination — generic CMS publishing pattern |
| 26–47 | **(T)** | Required Fields (Title, Symbol, Type, Status) — generic ETF schema, not Block-specific |
| 38 | **(T)** | TwelveData API hint — third-party data source, transferable |
| 50–54 | **(B)** | "Track Insight ID" + cloud.datasets.sh URL pattern — Track Insight is Block's specific data vendor. **Sanitize to "External Data ID" + parameterized URL pattern.** |
| 56–60 | **(T)** | TradingView Symbol — third-party, transferable |
| 62–77 | **(T)** | Issuer / Fee / URL / Custodian — generic ETF metadata |
| 79–90 | **(T)** | Categories list — generic crypto-ETF categories, not Block IP |
| 92–101 | **(T)** | Main Content (3-paragraph structure) — generic editorial pattern |
| 103–109 | **(B)** | "**The Block's Standard Format**: `[ETF Name] ([Symbol]) [Status] & Key Details \| The Block`" + 3 examples ending in `\| The Block`. **Replace with `{publisher_name}` placeholder and a parameterized format.** |
| 111–113 | **(T)** | Slug generation — generic |
| 115–125 | **(B)** | "**The Block's Standard Format**:" again, plus 4 example meta descriptions all ending in `... See [status keyword], details.` formatted to Block voice. **Same fix: `{publisher_name}` + parameterized format string.** |
| 127–135 | **(T)** mostly | Validate & Enrich step — generic. **EXCEPT line 135: "Financial news (The Block, CoinDesk, Bloomberg)" — drop "The Block" or replace with `{publisher_news_source}`.** |
| 137–203 | **(T)** | Format Output checklist — generic copy-paste structure |
| 196 | **(B)** | `[ETF Name] ([Symbol]) [Live Status/Status] & Key Details \| The Block` — same parameterization fix as 103–109 |
| 205–225 | **(T)** | Tips, validation reminders, references — generic |

**Net assessment for `etf-page-creator`:** Skill is ~85% transferable already. Block contamination is concentrated in 3 places: (a) Track Insight ID field (lines 50–54), (b) SEO Title format (lines 103–109 + 196), (c) Meta Description format (lines 115–125). All three fix with 2 placeholders: `{external_data_provider_id_field}` and `{publisher_name}`. ~30 minutes of focused edits in Step 2.

**Step 2 rename decision:** Roadmap suggests `etf-page-creator → structured-content-publisher`. Keep `etf-page-creator` since the skill is ETF-specific in mechanics (multi-cat dropdown, ticker format, status workflow); the *Block-ness* is what gets stripped, not the ETF-ness. Document this deviation.

## Skill 2 — `the-block-jira-ticket-writer` (out of scope, documented)

Lives only at `docs/Additional Skills To Add To Claude Superuser/Work - The Block - Skills/the-block-jira-ticket-writer/`. Never landed in `.claude/skills/`. **Action:** none for Step 2; the public-tree gate is already satisfied. If Sean wants the generic `pm-ticket-writer-with-style-guide` skill imported and sanitized, that's a separate Phase-2 task.

## Skill 3 — `biweekly-jira-update` (out of scope, documented)

Lives only at `docs/Additional Skills To Add To Claude Superuser/Work - The Block - Skills/biweekly-jira-update/`. Same as Skill 2. **Action:** none for Step 2.

## Bonus skill — `api-product-management/SKILL.md` (surfaced by audit)

Hits at lines 80, 90, 95, 97, 313 reference `developer.theblock.co`, `@theblock/data-sdk`, `TheBlockClient`, `theblock-data` MCP server name. This is live API example code in a generic skill. **Recommendation:** parameterize the running example to a placeholder vendor (e.g., `@example-data-co/data-sdk`, `developer.example-data-co`) rather than dropping the example — the skill needs concrete code to be useful. ~20 minutes in Step 2.

## Step 2 plan — locked Plan A (full clean, ~90 min next session)

1. **`etf-page-creator/SKILL.md` (5 hits, ~30 min).** 2 placeholders (`{external_data_provider}`, `{publisher_name}`). Edit lines 3, 50–54, 103–109, 115–125, 135, 196. Detailed line table earlier in this audit.
2. **`api-product-management/SKILL.md` (5 hits, ~20 min).** Replace `theblock`-prefixed identifiers with a neutral example vendor (e.g., `@example-data-co/data-sdk`, `developer.example-data-co`) across lines 80, 90, 95, 97, 313. Keep concrete example code — only the vendor identifier changes.
3. **`jira-automation/SKILL.md` (2 hits, ~5 min).** Line 293: drop the `the-block/product-management/templates/prd-to-launch.md` reference (the path is in archive; replace with a generic "see your team's PRD-to-launch template" note). Line 304: `Campus vs theblock.co vs both` → `{primary_component} vs {secondary_component} vs both`.
4. **`work-operating-model/SKILL.md` + `interview-questions.md` + `artifact-templates.md` (17 hits, ~25 min).** Replace literal `the-block` slug with `archived-employer` (or equivalent placeholder) across the 4-domain selectable list, layer-tuning notes, and email-archive examples. Update bundle path reference to use the placeholder slug. Bundle physical location at `vault/40_archive/operating-models-the-block-2026-05/` stays unchanged; only the in-skill slug shifts.
5. **`daily-driver/SKILL.md` (1 hit, ~2 min).** Line 96: `swinslow@theblock.co` → parameterized prior-employer reference.
6. **Run Step 3 grep:** `grep -rni "theblock\|the-block\|track insight\|@theblock\|swinslow@theblock" .claude/skills/ | grep -v ".git/"` — expected hits: **zero**.
7. **Run `python3 scripts/validate.py`** — expected 0 errors.
8. **Commit per roadmap Task 0 Step 5** with message: `chore(skills): full Block-string scrub across .claude/skills/ (CIIA §2.3 compliance + public-push readiness)`.

## Out of scope for Step 2

- `docs/Additional Skills To Add To Claude Superuser/Work - The Block - Skills/` source folders — these are pre-merge archives, not part of the public-push surface. Leave alone.
- `the-block/` archive folder at repo root — explicitly excluded from the grep gate per roadmap Task 0 Step 3.
- Repo-wide grep beyond `.claude/skills/` (CHANGELOG, vault notes, project READMEs reference the-block legitimately as employment history). Out of scope per the roadmap's narrow Task 0 framing.
