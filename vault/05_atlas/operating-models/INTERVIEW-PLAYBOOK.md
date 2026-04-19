---
type: reference
domain: [the-block, creative-studio, life-systems]
status: active
created: 2026-04-18
ai-context: "Step-by-step playbook for running the three work-operating-model interviews and committing each result to PR #20 on the v3.15.0-restructure branch. Self-contained — paste-able prompts, no prior conversation context needed."
---

# Interview Playbook — Work Operating Model

This is the operational playbook for populating the 15 placeholder artifacts in this folder. Each interview takes ~45 minutes, runs through 5 layers with checkpoints, and produces 5 markdown artifacts written by the [`work-operating-model`](../../../.claude/skills/work-operating-model/SKILL.md) skill.

## Pre-flight (do once before the first interview)

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git checkout v3.15.0-restructure   # confirm you're on the right branch
git status                          # should be clean except agent-logs
```

Then before each interview:
- Block ~45 minutes
- Kill notifications
- Be honest, not aspirational — the skill captures how you *actually* work, not how you think you should
- Have your calendar handy (Layer 1 asks about recurring meetings)

## Recommended order

1. **the-block** first — day-job tuning has the highest immediate downstream impact (jira-automation, meeting-defender become smarter)
2. **creative-studio** second — three-machine topology and pipeline friction surface here
3. **life-systems** third — pulls in cross-domain context (sleep/gym/sacred-blocks constrain everything else)

You can do all three in one sitting (~2.5 hr) or stretch over several days. Mid-layer breaks are fine — the skill saves after each layer; resume by saying *"resume the {domain} interview at Layer N."*

---

## Interview 1 — The Block (day job)

### Prompt to start

```
Run the work-operating-model interview for the-block.

Read the existing files at vault/05_atlas/operating-models/the-block/ first to confirm they're at status: awaiting-interview (this is a fresh interview, not a delta).

Walk me through all 5 layers — Operating Rhythms, Recurring Decisions, Dependencies, Institutional Knowledge, Friction. After each layer, summarize back what I said in 5-8 bullets, show me the proposed artifact updates, and wait for my explicit "confirm" before writing to disk.

For Layer 1, lean into Block-specific tuning: sprint ceremonies, bi-weekly P&E update cadence, the swinslow@theblock.co vs sean.winslow28@gmail.com email split, crypto market cycles. For Layer 3, the Granola meetings at vault/30_domains/product-management/the-block-meetings-granola-notes/ are the source of truth for internal context. For Layer 5, be sharp on "decisions I delay because they're annoying" — those are prime Jira automation candidates.

After the final layer, do a full read-through of all 5 artifacts and ask me to confirm. Then bump status from "draft" to "confirmed" on each file.
```

### Prompt to commit + push

```
The the-block operating-model interview is complete. Please:

1. Verify all 5 files at vault/05_atlas/operating-models/the-block/ have status: confirmed (or status: draft if I deferred final review)
2. Run a cross-file consistency check per .claude/skills/work-operating-model/artifact-templates.md (people in HEARTBEAT also in SOUL Part A; tools in SOUL Part A also referenced in USER or HEARTBEAT; recommendations in schedule-recommendations traceable to Layer 5 answers)
3. git add vault/05_atlas/operating-models/the-block/
4. git commit -m "interview(the-block): populate 5-layer operating model"
5. git push

Do not stage anything else — just the the-block operating-model folder. Report the commit SHA and confirm push succeeded.
```

---

## Interview 2 — Creative Studio

### Prompt to start

```
Run the work-operating-model interview for creative-studio.

Read the existing files at vault/05_atlas/operating-models/creative-studio/ first. Walk me through all 5 layers with checkpoints after each one (summarize → show diff → wait for "confirm" → write).

Domain-specific tuning to lean into:
- Layer 1: 16BitFit has its own project rhythm (phase milestones, gate checks). Ask about deep-work blocks vs render-waiting time. This domain is mostly personal-Gmail calendar.
- Layer 3: The three-machine topology (Mac Mini orchestrator, MacBook Pro heavy inference, Alienware CUDA) is most load-bearing here. Ask what specifically halts if each machine goes down.
- Layer 3 Q6: I'm pursuing a PM → Animation Producer career transition — ask about festival/application cadences (Annecy, Ottawa, etc.).
- Layer 5: Pipeline orchestration pain points (ComfyUI brittleness, sprite cleanup friction) are prime candidates.

After Layer 5, full read-through and confirm before flipping status to "confirmed."
```

### Prompt to commit + push

```
The creative-studio operating-model interview is complete. Please:

1. Verify all 5 files at vault/05_atlas/operating-models/creative-studio/ have status: confirmed (or draft if deferred)
2. Run cross-file consistency checks
3. git add vault/05_atlas/operating-models/creative-studio/
4. git commit -m "interview(creative-studio): populate 5-layer operating model"
5. git push

Stage only the creative-studio operating-model folder. Report commit SHA and push status.
```

---

## Interview 3 — Life Systems

### Prompt to start

```
Run the work-operating-model interview for life-systems.

Read the existing files at vault/05_atlas/operating-models/life-systems/ first. Walk me through all 5 layers with checkpoints (summarize → diff → "confirm" → write).

Domain-specific tuning:
- Layer 1: My 4:45 AM routine, 45/35/20 work split, gym block, sleep window. Boston move from NYC has specific seasonal friction — capture it.
- Layer 1 Q5: Mostly personal Gmail in this domain; Bilt/Chase financial cycles.
- Layer 2 Q1: Habits and streak tracking — the health-habits skill consumes this.
- Layer 3: Typically just Mac Mini for daily orchestration. Local models (gemma4, phi4-mini) handle finance categorization where possible — personal data stays local.
- Layer 5: Friction in finance-CSV ingestion, habit logging, weekly reviews.

Final read-through, confirm, flip status to "confirmed."
```

### Prompt to commit + push

```
The life-systems operating-model interview is complete. Please:

1. Verify all 5 files at vault/05_atlas/operating-models/life-systems/ have status: confirmed (or draft if deferred)
2. Run cross-file consistency checks
3. git add vault/05_atlas/operating-models/life-systems/
4. git commit -m "interview(life-systems): populate 5-layer operating model"
5. git push

Stage only the life-systems operating-model folder. Report commit SHA and push status.
```

---

## After all 3 interviews — wrap-up prompt

Use this once all three are committed to PR #20:

```
All three operating-model interviews are complete and pushed to PR #20.

Please do the following:

1. Run python3 scripts/validate.py and confirm it still exits 0
2. Run cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/ -q
3. Cross-check that the 15 artifacts (5 files × 3 domains) all have status: confirmed (or draft) and none are still at status: awaiting-interview
4. Look for cross-domain bleed mentioned in any operating-model.md file — if domain X mentions a person/tool/pattern from domain Y, surface it as a bullet so I can verify the cross-references are accurate
5. Update CHANGELOG.md v3.15.0 entry — under "Known follow-ups," strike through "Three-domain interviews not yet run" since it's now done
6. Update PR #20 description: change the "Run 3 operating-model interviews" checkbox to checked, and add the 3 interview commit SHAs
7. Mark PR #20 as Ready for Review (gh pr ready 20)

Report results. Don't merge — wait for Mac Mini cross-machine review pass before merging to main.
```

---

## Edge cases and tips

| Situation | What to do |
|---|---|
| Need to break mid-interview | Skill saves after each layer. Resume with: *"resume the {domain} interview at Layer N"* |
| Want to revise one layer later | *"Update my {domain} operating model — re-run Layer N only"* |
| Cross-references inconsistent | Skill flags this on final read-through. Update the inconsistent file before flipping status to confirmed |
| Don't want to confirm a layer | Skill won't write without your "confirm." Push back, restate, re-summarize until accurate |
| Forgot what a layer covers | See [interview-questions.md](../../../.claude/skills/work-operating-model/interview-questions.md) for the verbatim 5-layer question set |

## What "good" looks like for each artifact

- **HEARTBEAT.md** — someone could glance at it and predict where you'll be Tuesday at 2pm
- **USER.md** — captures the *real* prioritization criteria (messy is fine), not the LinkedIn version
- **SOUL.md** — names actual people; "Sarah from product" beats "the PM I work with"; tribal knowledge a new hire would need on day one
- **operating-model.md** — synthesizes the other four; surfaces leverage points and bottlenecks; cross-references make sense
- **schedule-recommendations.md** — every "Automate" or "Protect" item traces back to a specific Layer 5 answer; nothing invented

If any artifact reads like it could apply to a generic PM / generic creative / generic person, push back and re-do the layer with sharper specifics.

## Honest > aspirational reminder

The downstream agents — `meeting-defender`, `daily-driver`, `sprint-health`, `process-inbox`, `pr-digest` — will trust whatever lands in these files. If you write "I never check email after 6pm" but actually do, meeting-defender will defend a window you don't actually protect, and you'll learn to ignore it.

The operating model is for capturing reality. Aspirations belong somewhere else.
