# Migration Report — substack-studio

**Date:** 2026-06-22
**What:** Consolidated the "Raising Claude" Substack work into this tracked (public) folder inside
code-brain, so it backs up to GitHub and syncs across machines. **Copy + privacy transformation**
(originals copied, never moved). README/CLAUDE.md left as stubs for a later brainstorm.

> **Note on this report:** it is itself a tracked public file, so it describes the sensitive
> material **abstractly** — it never reproduces the literal terms, names, or quotes that were
> scrubbed/excluded. "Do-Not-Promote framing" is the umbrella term for the suppressed personal
> topic (per the series' own voice rule and code-brain Rule #10).

**Result:** 83 files staged as tracked (71 content files + 12 skill symlinks). `_private/` is
gitignored and empty of content. The privacy gate (Do-Not-Promote term / prior-employer name /
named individuals / compensation terms / family names) returns **zero hits** across all tracked
files.

---

## Sources (copied from)

| Source path | Status at source |
|---|---|
| `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/` | **gitignored** (private) — the core win: now backed up + synced |
| `vault/30_domains/creative-studio/` (4 last30days reports) + `substack-research/` (8 files) | already tracked/public |
| `vault/20_projects/research/` (addictive-storytelling, 2d-animation ledger, 3 discovery JSONs) | already tracked/public |
| `creative-studio/docs/tool-shipping-playbook.md` | already tracked/public |
| `docs/substack-image-generation-design-2026-05-23.md` → `playbook/image-house-style.md` | already tracked/public |

**Originals untouched** — verified no git modifications to any tracked source file (copy-not-move;
the gitignored drafts source was read-only).

---

## What was COPIED (public)

- **Posts 01–07** (folders, with `images/`, `hero-prompt.txt`, kits, `_seed.md`, build-spec/research).
- **Bonus** → `bonus-the-night-my-vault-said-nothing/` (`the-night-…md` renamed to `post.md`).
- **SERIES-COMMAND-CENTER.md** (the drafts `README.md`, renamed so it doesn't collide with the stub).
- **CONTINUATION × 3** + **NEXT-POST-KICKOFF.md** (editorial seed).
- **_assets/** (headshot + style-anchor prompts).
- **research/** — `opportunity-report-creative-agentic.md` (spine) + `deep-dives/` (5) + `last30days/` (6) + `discovery/` (2 ledgers + `discovery-sessions/` 3 JSONs).
- **playbook/** — `tool-shipping-playbook.md` + `image-house-style.md`.
- **.claude/skills/** — 12 relative symlinks (no copies; see §Skills).

## What was SCRUBBED before tracking (privacy transformation)

All edits applied to the **public copy only**; the un-scrubbed originals remain in the gitignored
source. Hard rule enforced: the Do-Not-Promote term, the prior-employer name, any named individual,
compensation terms, and family names appear in **no** tracked file.

**Body prose (creative-touch — review/revert wording if desired):**
| File | What changed |
|---|---|
| `07-the-judgment-layer/post.md` | the Do-Not-Promote clause in the "evals papers" sentence → "…with something to prove," |
| `bonus-…/post.md` | the Do-Not-Promote clause in the "fleet of fourteen" sentence → "…back when the time horizon for…" |
| `research/discovery/2026-06-02-…addictive-storytelling…md` (L106 example) | the Do-Not-Promote clause in the illustrative quote → "…which I rebuilt once I had the time" |

**Frontmatter / process-note mentions** — mechanical replacement of the Do-Not-Promote term with
"Do-Not-Promote framing" in: `01/post.md` (voice_chain_notes), `01/LAUNCH.md`, `02/post.md` (×3),
`03/post.md`, `SERIES-COMMAND-CENTER.md` (voice rules), `CONTINUATION-2026-06-10` (×4),
`CONTINUATION-2026-06-17-substack-posts` (×1), `NEXT-POST-KICKOFF.md` (×1).

**Stale-path repoints** (also removed the literal job-hunt-project string from tracked files):
- Full drafts-dir path → `vault/20_projects/substack-studio/` in the 3 CONTINUATION docs, KICKOFF, and `01/LAUNCH.md` (incl. the image-gen command paths).
- `build_spec:` in `06/post.md` and two spec refs in `SERIES-COMMAND-CENTER.md` → the locally-present `06-stop-building-agents/2026-06-17-agent-or-automation-advisor-build-spec.md`.
- `project:` job-hunt-project tag → `project: substack-studio` in 3 frontmatter blocks.

## What was EXCLUDED (stayed only in the gitignored source)

- **`_archive/`** — retired cuts carrying the Do-Not-Promote topic in full body prose + dup-guard variants.
- **`_experiments/`** — beatmaps, voice-calibration, and especially
  `council-sessions/2026-05-14-post-1-council-session.md`, which contains **hard PII**: named former
  colleagues/managers, employment-departure specifics, home address, a family member, compensation /
  runway details, and a medical aside.
- macOS `.DS_Store` files (junk).

Rationale (signed off): copy-not-move already preserves these in the source; a `_private/` copy would
be local-only too, so copying them in would only duplicate the PII into a second location.

---

## Skills (mechanism: relative symlinks)

`.claude/skills/<name>` → `../../../../../.claude/skills/<name>` for all 12: **writing chain**
(writing-voice-modes, writing-critique, storytelling-architecture, writing-humanity-pass,
substack-value-engine, creative-writing), **image** (openai-image-gen, gemini-image-gen),
**research engine-backed** (last30days, llm-council, fusion-discovery-council, gemini-deep-research).

- Verified: all 12 resolve to a `SKILL.md`; git stages them as **12 symlink objects** and does
  **not** traverse into them — so `writing-voice-modes/{references,drafts}/` (the gitignored personal
  voice data) is **never** staged. Confirmed 0 skill-internal files in git's add list.
- Engine-backed skills keep working unchanged — their SKILL.md hardcodes **absolute** paths to
  `tools/llm-council/`, `agents-sdk/scripts/gemini_dr.py`, `.env`, and `vault/health/` spend files,
  which resolve identically from this nested location.
- Fallback if a session launched here doesn't pick up the symlinks: code-brain's root
  `.claude/skills/` auto-loads anyway (this folder is nested inside the repo). Recommend confirming
  skill load from a session opened in this folder.

---

## Open items for Sean

1. **Residual mild "hiring-signal / job-hunt" framing in research files** (NOT scrubbed): the two
   `research/last30days/2026-06-09-ai-*` reports and the discovery question frame the work as hiring
   signal. These were **classified PUBLIC-SAFE in the approved plan**, are **already public** in
   their source location, and are professional-positioning (not PII), so they were left verbatim
   rather than altering research you marked public. Do a final pass if you want them neutralized too.
   (One dangling roadmap path ref to a non-copied build-spec also remains in a research file.)
2. **⚠️ Pre-existing leak at the source** (not introduced here): the original
   `vault/20_projects/research/2026-06-02-topic-28-…md:106` still contains the un-scrubbed
   illustrative Do-Not-Promote quote in the **tracked** repo today (the substack-studio copy was
   scrubbed). Recommend a source-side scrub. (Ticket logged.)
3. **Missing skills (not fabricated):** `image-generator-prompt-science` is not in code-brain (lives
   in portfolio repos; the image-gen skills reference it as an optional delegate and work without
   it); `substack-aeo-geo-optimizer` does not exist anywhere. Canonicalizing either is out of scope.
4. **Headshot:** `_assets/references/sean-headshot.jpg` is tracked (public). It's already public on
   Substack; pull it if you'd rather not have your photo in the repo.

## Path-coupling risks (no runtime change made)

- **`substack_drafter.py:529` + `config.toml:556`** still write to the **old gitignored source**
  drafts path. The fleet is unaffected, but new drafts land in the source, **not here** — so
  `substack-studio` is a curated **snapshot**, not the live drafting target. **Do not repoint
  `output_dir`** until a scrub-gate exists (raw drafter output can carry un-suppressed Do-Not-Promote
  framing that would leak into the public path). (Ticket logged.)
- Docs/comments only (no runtime impact): `vault_synthesizer.py` comments, `retrieval_diversity.py`
  docstring, `test_judge_*` fixtures, `openai-image-gen/SKILL.md:140`, `time-management/SKILL.md:10`,
  `daily-driver/SKILL.md:106`. Reconcile only if the source path is ever retired.

## Verification performed

- Privacy gate grep (Do-Not-Promote term / prior-employer name / named individuals / compensation
  terms / family names) over exactly the files git will track → **0 hits**.
- `_private/` ignored (`.gitignore`), 0 `_private` entries in `git status`.
- 12 skill symlinks resolve; 0 skill-internal files in git's add list.
- Originals at all tracked source paths show no git modifications.
