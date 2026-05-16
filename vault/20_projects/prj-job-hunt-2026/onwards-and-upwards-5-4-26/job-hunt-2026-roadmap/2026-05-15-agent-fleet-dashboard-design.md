---
type: design
project: prj-job-hunt-2026
created: 2026-05-15
status: design-complete
supersedes: "[[2026-05-13-agent-fleet-dashboard-spec]]"
linked_artifacts:
  - "[[2026-05-13-agent-fleet-dashboard-spec]]"
  - "[[2026-05-14-Agent-Fleet-Observability-Dashboard-ChatGPT]]"
  - "[[2026-05-14-Agent-Fleet-Observability-Dashboard-Gemini-DR]]"
  - "[[2026-05-06-unified-roadmap]]"
ai-context: "Locked design for the Agent Fleet Observability Dashboard. Synthesizes the 2026-05-13 build-spec + research-prompt with the two deep-research returns from Gemini DR and ChatGPT DR, plus a brainstorming session with Sean on 2026-05-15. Two render modes (public at fleet.seanwinslow.com + private at file://), one build pipeline, full visual + interaction spec. Implementation-ready for writing-plans skill. v2 kanban write-back deferred."
ships: 2026-05-26 to 2026-06-08 (3 working days post-design)
---

# Agent Fleet Observability Dashboard — Locked Design

> Successor to [[2026-05-13-agent-fleet-dashboard-spec]]. Synthesizes both DR returns plus the 2026-05-15 brainstorming session decisions. Implementation-ready.

---

## 1. Decision Summary

| Topic | Locked Decision |
|---|---|
| Use mode | Two render modes, two URLs — public + private from one build pipeline |
| Public surface | `fleet.seanwinslow.com` via Vercel + Cloudflare CNAME (DNS-only) |
| Private surface | `file:///Users/seanwinslow/Sites/agent-fleet-private/index.html` |
| Cost framing | Architectural — show $ in context of governance decisions ("99.2% local-only" leads, dollars follow as evidence) |
| Visual personality | Dark hybrid (Vercel deployment-log mood + full legibility). Sora / Inter / JetBrains Mono |
| Public layout | Top bar · Regression hero · KPI row · Agent grid · below-fold detail |
| Private layout | Fleet Operator — alerts pinned · agent grid featured · job hunt below fold |
| Mascot | Asterisk Spark — 8-pt spinning sparkle, amber-to-purple gradient arms, dark core, blinking eyes. Pure HTML/CSS, ~40 lines |
| Microcopy voice | Subtle Sean voice in empty states |
| Footer copy | "Built by Sean Winslow. 8 agents on macOS launchd, 99% local-first inference. View source · last build [TS]" |
| Kanban v1 | Read-only at `/kanban`, ships with v1 |
| Kanban v2 | Interactive with agent write-back — deferred (own portfolio artifact post-v1-validation) |
| Data loading | Static build-time snapshot (no live polling) |
| Build trigger | local cron on Mac Mini at 06:00 ET daily |
| Cost | $0 cloud · $12/yr domain (already owned) |

---

## 2. System Architecture

### 2a. Two render modes, one build pipeline

Both renders read the same raw data at build time and emit two independent HTML files. The public render anonymizes / strips job-hunt content; the private render keeps everything.

```
                                ┌─────────────────────────┐
                                │ build.py @ 06:00 ET     │
                                │   (Mac Mini cron)       │
                                └────────────┬────────────┘
                                             │
              ┌──────────────────────────────┼──────────────────────────────┐
              │                              │                              │
   READ raw data sources              AGGREGATE telemetry          RENDER two passes
   (CSV, JSON, SQLite, MD)           (KPIs, sparklines, regression  (public-safe + full)
              │                       window, model mix, kanban       │
              │                       column membership)               │
              │                                                ┌───────┴───────┐
              ▼                                                ▼               ▼
                                                          public/         ~/Sites/
                                                          (committed)     agent-fleet-
                                                          → git push      private/
                                                          → Vercel        (gitignored)
                                                          fleet.seanwinslow.com
```

### 2b. Data sources (all local files)

| Source | Path | Used for |
|---|---|---|
| Agent run history | `vault/90_system/agent-logs/agent-run-history.csv` | Every panel — runs, costs, durations, models |
| Synthesizer manifest | `vault/health/synth-manifest-{date}.json` | Regression hero · concepts/connections/edges sparkline |
| Gemini DR spend | `vault/health/gemini-spend-{YYYY-MM}.json` | Cloud cost · monthly governor headroom |
| LLM Council spend | `vault/health/council-spend-{YYYY-MM}-{DD}.json` | Council monthly running total |
| Job feed manifest | `vault/health/job-feed-manifest-{date}.json` | Daily job-feed roll-up (private only) |
| Knowledge lint reports | `vault/health/*-lint-report.md` | Lint findings → kanban tickets |
| Eval suite last-run | `evals/vault-synthesizer/last-run.md` | Eval pass count + case grid |
| Job feed database | `vault/.job-feed.db` (SQLite) | Target-30 funnel · warm-intro pipeline (private only) |
| Research queue | `vault/00_inbox/research-queue.md` | Kanban Backlog/ToDo items |
| Manual tickets | `vault/00_inbox/tickets.md` (new file Sean maintains) | Kanban manual entries |

### 2c. Privacy boundary (structural)

The privacy boundary is enforced by **separate output files in separate destinations**, not by policy or feature flags:

1. **Public render-pass never reads** `vault/.job-feed.db` — the data source is skipped entirely. Even an accidental field reference returns empty.
2. **Public render-pass strips log excerpts** containing vault path references, prompt content, or completion text.
3. **Output paths are physically separated**: public goes to repo root + `git push`; private goes to `~/Sites/agent-fleet-private/` which is gitignored at the home-directory level.
4. **The kanban Job Feed lane only emits on private** — the public kanban renders 4 columns of ticket types, not 5.
5. **No cross-link**: the public `/fleet` and `/kanban` never reference the private surface.

### 2d. Distribution

**Public** — Vercel project `agent-fleet-observability`. Custom domain `fleet.seanwinslow.com` configured via Cloudflare CNAME (DNS-only / gray cloud — Vercel handles SSL on its edge). Auto-deploys on every push to the repo's `main` branch.

**Private** — `file://` URL opened directly in Chrome on Sean's Mac. Bookmark it. Not exposed to the network.

**Repo** — new dedicated repo: `github.com/seanwinslow28/agent-fleet-observability` (public). Generated HTML is committed to the repo (yes, daily auto-commits — accepted v1 trade-off, can be squashed periodically).

---

## 3. Public Artifact (`fleet.seanwinslow.com`)

### 3a. Routes

| Path | Page | Notes |
|---|---|---|
| `/` or `/fleet` | Observability dashboard | Default landing |
| `/kanban` | Read-only ticket board | 4 visible columns (Job Feed lane hidden on public) |

`/archive` is **v2** — Done column on `/kanban` is bounded by the "last 7 days" rule for v1, which keeps it tight without needing a separate route. See Section 11.

### 3b. Top bar (every page)

- Asterisk Spark mascot (32px, top-left) — animates: spin + blink
- Wordmark: **Agent Fleet Observability** in Sora 600
- Subtitle: `fleet.seanwinslow.com` in JetBrains Mono 11px, color `#6e7681`
- Status pill: `● 8/8 HEALTHY` (green) — color-shifts to amber/red based on actual snapshot state
- Snapshot timestamp: `2026-05-15 06:00 ET` in JetBrains Mono
- Nav links: `/fleet` · `/kanban` · `/archive` (current page indicated by `border + bg`)

### 3c. `/fleet` above the fold

1. **Hero — Regression Timeline**
   - Full-width panel inside the `priv-wrap` dark container
   - Eyebrow: `VAULT SYNTHESIZER · CONCEPTS WRITTEN PER NIGHT · 60 DAYS` in mono 10px
   - Headline: *"For **nine consecutive nights**, the synthesizer wrote zero concepts. The eval suite caught it on day ten."* — Sora 14px, with the bolded phrase in amber `#f0b429`
   - Chart: inline SVG line chart, 60-day x-axis
     - Healthy segment: green `#3fb950`, 2px stroke
     - Regression segment: red `#f85149`, 2px stroke — drops to y=0 for the 9-night window
     - Recovery segment: teal `#18b894`, 2px stroke — climbs back post-fix
     - Subtle area fills under healthy + recovery in 15% opacity
   - Annotations:
     - Red dashed vertical band covering the regression window (May 1–10) with red `#f85149` borders
     - Red "9-DAY SILENT REGRESSION" callout above the band's left edge
     - Green "EVAL CAUGHT · MAY 10" marker at the catch point
   - X-axis labels: 5 dates in mono 10px, evenly spaced

2. **KPI row (4 cards)**
   | Card | Label | Value | Sub |
   |---|---|---|---|
   | 1 | Eval Pass · last night | `7 / 10` (green) | 14-day sparkline `▁▁▃▃▆▇▇▇▇▆▇▇▇` |
   | 2 | Fleet Spend · 30 days | `$8.40` | `99.2% local · 240 runs` |
   | 3 | Local-only Share | `99.2%` (green) | `7 of 8 agents · $0/run` |
   | 4 | Spend Governors | `$50/mo` (amber) | `$7 task · $20 daily breaker` |

3. **Agent grid (8 tiles, 4-col)**
   - Per tile: status dot (green/amber/red with glow) · full agent name (Sora 12px) · last-run timestamp · last cost
   - Eight tiles: Vault Indexer, Vault Synthesizer, Deep Researcher, Meta Agent, Daily Driver, Knowledge Lint, Flush, Job Feed

### 3d. `/fleet` below the fold

| Panel | Visualization | Source |
|---|---|---|
| 30-day Cost Trend | Stacked area chart, color per agent (public shows %, not $) | `agent-run-history.csv` aggregated by agent + day |
| Model Mix | Donut, segments by family (Qwen3-14B / nomic / gemma4 / Sonnet 4.6 / Gemini DR) | `agent-run-history.csv` `model_used` column |
| Recent Runs | Table, last 50, sortable: agent · status · duration · model · cost ($ shown — consistent with architectural framing) | `agent-run-history.csv` tail 50 |
| Synthesizer Telemetry Deep Dive | Two-series line chart: concepts_written, connections_written, 60 nights | `synth-manifest-*.json` |
| Eval Suite Case Grid | 10 rows (cases) × 14 cols (last 14 days), green/red/yellow cells | `evals/vault-synthesizer/last-run.md` (joined with prior runs) |

### 3e. `/kanban` (read-only v1)

**Columns**: Backlog · ToDo · InProgress · Testing · Done

**Ticket sources** (4 visible on public, 5 on private):

| Source | Color | Public? | Origin |
|---|---|---|---|
| Research | `#c084fc` purple | Yes | `vault/00_inbox/research-queue.md` items |
| Lint | `#f0b429` amber | Yes | Latest `*-lint-report.md` `LintIssue` entries |
| Eval | `#f85149` red | Yes | Failing eval cases from `evals/vault-synthesizer/last-run.md` |
| Manual | `#8b949e` gray | Yes | `vault/00_inbox/tickets.md` (new file Sean maintains) |
| Job Feed | `#58a6ff` blue | **No (private only)** | `vault/.job-feed.db` company records by stage |

**Column membership rules** (computed at build time):

| Column | Rule |
|---|---|
| Backlog | Ticket has no assigned agent (research-queue items without an agent tag, manual tickets without assignment, unfixed lint issues) |
| ToDo | Ticket has assigned agent + the agent has a queued upcoming cron run (or eval case is failing pending fix) |
| InProgress | A row exists in `agent-run-history.csv` for this ticket's agent within the last `run_duration_minutes` window AND the row's `status` is "started" without a corresponding "completed" row. (Live-pulse dot rendered.) |
| Testing | Run completed but downstream verification (eval, lint, Sean review) pending |
| Done | Verified complete within last 7 days; older → `/archive` |

**Live-pulse dot** for InProgress: small green dot with 2s opacity pulse animation (purely visual flourish — snapshot is static, but the animation suggests current-window freshness).

### 3f. Public anonymization rules (enforced in build script)

| Field | Public render |
|---|---|
| Exact dollar amounts | **Shown** ($8.40, $50/mo, etc.) — they tell the architectural story |
| Per-task cost per agent run | Shown (`$0.32`) — same reason |
| Job Feed tickets | **Stripped** — entire data source skipped on public pass |
| Target-30 company names | Never read on public pass |
| Application-velocity sparkline | Private only |
| Warm-intro pipeline | Private only |
| Log excerpts | Stripped (would require sanitization that's unreliable; skip entirely) |
| Vault path references inside ticket titles | Replaced with `vault/[...]` redacted form |
| Eval case names | Shown (they're public test-case identifiers) |
| Agent names | Shown |
| Run timestamps | Shown |

### 3g. Footer (every page)

> **Built by Sean Winslow.** 8 agents on macOS launchd, 99% local-first inference. [View source](https://github.com/seanwinslow28/agent-fleet-observability) · last build {TIMESTAMP}

---

## 4. Private Artifact (`file://`)

### 4a. Routes (same as public)

`/fleet` · `/kanban` · `/archive` — identical paths, different render passes.

### 4b. Top bar additions (private)

- **`PRIVATE`** badge next to wordmark — purple bg `#2d1f3a` / fg `#c084fc`, mono 10px
- Multiple status pills:
  - `● FLEET 7/8` (green) — current fleet health
  - `HUNT · 29 ACTIVE` (info blue) — job hunt pipeline state
  - `2 ALERTS` (amber) — only renders when alerts > 0
  - `MBP AWAKE` / `MBP ASLEEP` (amber/gray) — gates synth health interpretation
- Same snapshot timestamp

### 4c. `/fleet` above the fold (Fleet Operator layout)

1. **Alerts banner** — only renders when there are any. Pinned at the top above the agent grid.
   - Title in amber `#f0b429`: `⚠ 2 things need your attention`
   - Right-side subtitle: `overnight · last 12h` in mono 10px
   - Each alert row: colored dot (amber/red) + sentence + right-aligned timestamp
   - Alert types surfaced:
     - Agent run hit per-task cap (amber)
     - Eval pass count dropped vs prior 14-day average (red)
     - Monthly governor headroom < 30% remaining (amber)
     - MBP-not-awake gating overnight synth (amber)
     - Sunday lint Tier-A SOUL conflict found (red)
     - Multiple consecutive failed runs for any agent (red)

2. **Agent grid** (8 tiles, featured) — same 4-col layout, **with per-tile detail expanded**:
   - Tile lines include: status dot · agent name · last-run · last cost
   - **Per-tile second line:** ticket count or metric specific to agent (e.g., Synthesizer: "+24 concepts"; Researcher: "1 of 2 (cap hit)"; Job Feed: "14 new")

3. **KPI row (4 cards, private variant)**
   | Card | Label | Value (example) | Sub |
   |---|---|---|---|
   | 1 | Eval Pass | `7 / 10` | 14-day sparkline |
   | 2 | Fleet $ · 30d | `$8.40` | `99.2% local` |
   | 3 | Monthly Headroom | `$18 / $50` (amber) | `Gemini DR · 64% · 16d left` |
   | 4 | Runs · 24h | `31` | `30 ok · 1 capped` |

### 4d. `/fleet` below the fold (private additions on top of public panels)

| Panel | Source |
|---|---|
| Job Hunt — Target-30 funnel | `vault/.job-feed.db` companies by stage |
| Job Hunt — Applications this week | `vault/.job-feed.db` joined with `agent-run-history.csv` |
| Job Hunt — Next Actions | Hand-curated upcoming-action list from `vault/.job-feed.db` `next_action` field |
| Job Hunt — Warm-Intro Pipeline | `vault/.job-feed.db` warm-intro records |
| Job Hunt — Tier-A Guardrail Check | Operating-model artifact compliance: walk-away criteria + 5:30 hard-stop + Track-C protection. Static checks based on yesterday's daily log + calendar |
| Cloud Spend Governance — Gemini DR | `vault/health/gemini-spend-{YYYY-MM}.json` running total with horizontal headroom bar against $50 cap |
| Cloud Spend Governance — LLM Council | `vault/health/council-spend-*.json` aggregated, headroom bar against $40 cap |
| Recent Failures | Last 5 cap-hits or errored runs from `agent-run-history.csv` with sanitized log excerpt |

The public below-fold panels (cost trend, model mix, recent runs, synth telemetry, eval case grid) also render here with full $ values and unredacted detail.

### 4e. `/kanban` (private — 5 lanes)

Same as public, plus:
- Job Feed lane chip visible in filter bar (`● Job Feed 5 [private]`)
- Job Feed tickets render in their natural columns (e.g., "Anthropic FDE · phone screen scheduled" in Testing)
- Manual tickets unredacted

### 4f. Private footer

Same as public: *Built by Sean Winslow. 8 agents on macOS launchd, 99% local-first inference. View source · last build {TS}.*

(The footer copy doesn't need a private-mode variant — the privacy is in the data above it, not the footer itself.)

---

## 5. Visual Design System

### 5a. Personality D — Dark hybrid

Vercel-deployment-log dark palette with full legibility, mono numbers, status-everywhere mood. Locked in the brainstorming session as the working visual reference.

### 5b. Palette

| Token | Hex | Use |
|---|---|---|
| `bg-primary` | `#0a0d12` | Page background |
| `bg-panel` | `#11151c` | Panel surfaces |
| `bg-recessed` | `#0d1219` | Below-fold cards, kanban columns |
| `border-subtle` | `#1a2230` | Panel borders, dividers |
| `text-primary` | `#e6edf3` | Body text |
| `text-secondary` | `#8b949e` | Sub-text |
| `text-tertiary` | `#6e7681` | Labels, timestamps |
| `accent-green` | `#3fb950` | Healthy, OK, success — Vercel-green tier |
| `accent-teal` | `#18b894` | sw-portfolio teal — used for synthesizer recovery line and emphasis |
| `accent-amber` | `#f0b429` | Warnings, regression callout, mascot arms |
| `accent-purple` | `#c084fc` | Research tickets, private badge, mascot arms (gradient target) |
| `accent-red` | `#f85149` | Errors, regression band, failure alerts |
| `accent-blue` | `#58a6ff` | Job feed, info pills, hunt status |

### 5c. Typography stack

```
Headings:  'Sora', 'SF Pro', system-ui, sans-serif
Body:      'Inter', -apple-system, sans-serif
Numerals:  'JetBrains Mono', 'SF Mono', Monaco, monospace
```

Loaded from Google Fonts with `display=swap`. Fallbacks rendered first; webfonts swap in when loaded. Acceptable FOUT for an instrumented dashboard.

### 5d. Mascot — Asterisk Spark

Pure HTML + CSS, ~40 lines. Sits at 32px in production (top-left of every page next to wordmark). Animates with two simultaneous loops: continuous 12s rotation on the arms layer, and a 5.5s blink on the eyes (rapid scaleY to 0.08 then back to 1).

**Structure:**

```html
<div class="spark">
  <div class="arms">
    <div class="arm arm-v"></div>
    <div class="arm arm-h"></div>
    <div class="arm arm-d1"></div>
    <div class="arm arm-d2"></div>
  </div>
  <div class="core">
    <div class="eye eye-l"></div>
    <div class="eye eye-r"></div>
  </div>
</div>
```

**CSS** (reference — production version may tune sizing):

```css
@keyframes m-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes m-blink {
  0%, 88%, 100% { transform: scaleY(1); }
  91%, 95% { transform: scaleY(0.08); }
}
.spark { width: 32px; height: 32px; position: relative; display: flex; align-items: center; justify-content: center; }
.spark .arms { position: absolute; width: 100%; height: 100%; animation: m-spin 12s linear infinite; }
.spark .arm { position: absolute; background: linear-gradient(180deg, #f0b429 0%, #c084fc 100%); border-radius: 1px; }
.spark .arm-v { width: 2px; height: 100%; left: 50%; transform: translateX(-50%); }
.spark .arm-h { width: 100%; height: 2px; top: 50%; transform: translateY(-50%); }
.spark .arm-d1 { width: 2px; height: 90%; left: 50%; top: 5%; transform: translateX(-50%) rotate(45deg); opacity: 0.6; }
.spark .arm-d2 { width: 2px; height: 90%; left: 50%; top: 5%; transform: translateX(-50%) rotate(-45deg); opacity: 0.6; }
.spark .core { width: 14px; height: 14px; background: #0a0d12; border-radius: 50%; position: relative; z-index: 2; border: 1px solid #f0b429; box-shadow: 0 0 16px #f0b42966; }
.spark .eye { position: absolute; width: 1.8px; height: 2.2px; background: #f0b429; border-radius: 0.5px; top: 4px; animation: m-blink 5.5s infinite; transform-origin: center; }
.spark .eye-l { left: 3px; }
.spark .eye-r { right: 3px; }
```

Reduced-motion: when `prefers-reduced-motion: reduce` is set, the spin and blink animations are paused (mascot becomes a static sigil).

### 5e. Microcopy voice

Empty states use plain-language descriptions of what happened, not generic "No data" messaging.

| Default | Sean voice |
|---|---|
| "No synthesizer runs in last 30 days" | "Synth napped 9 nights this month. MBP was asleep." |
| "Eval suite: 0 cases passed" | "Eval suite went quiet. Worth investigating." |
| "No job feed activity" | "Job feed paused. Watchlist hasn't fired today." |
| "No alerts" | "Nothing on fire. Carry on." |
| "0 tickets in Backlog" | "Backlog empty. The fleet is caught up." |

Hover tooltips on the regression band use the narrative voice: *"Synthesizer wrote zero concepts for 9 consecutive nights. The vault-synthesizer eval suite caught it on day ten. Read the story →"*

### 5f. Footer (locked copy)

> *Built by Sean Winslow. 8 agents on macOS launchd, 99% local-first inference. [View source](https://github.com/seanwinslow28/agent-fleet-observability) · last build {TIMESTAMP}*

No "Saturday morning cartoons" line — that phrase lives exclusively on Sean's personal portfolio hero to preserve its impact.

---

## 6. Build Pipeline

### 6a. Repo layout

```
agent-fleet-observability/
├── build.py                     # entry point
├── Makefile                     # `make build` runs build.py
├── vercel.json                  # if needed — default config works for static
├── lib/
│   ├── readers.py               # CSV / JSON / SQLite / Markdown loaders
│   ├── aggregations.py          # compute KPIs, sparklines, regression window
│   ├── kanban.py                # ticket aggregation + column-membership rules
│   ├── public_render.py         # render public/index.html + kanban.html
│   ├── private_render.py        # render private/index.html + kanban.html
│   └── anonymize.py             # public-pass stripping rules
├── templates/                   # Jinja2 templates
│   ├── base.html                # top bar + mascot + footer shared
│   ├── fleet.html               # /fleet page
│   ├── kanban.html              # /kanban page
│   └── partials/                # hero, kpi-row, agent-grid, etc.
├── assets/
│   ├── styles.css               # full stylesheet (~10 KB)
│   └── charts.js                # tiny client-side layer for Chart.js init
├── index.html                   # GENERATED (public/fleet) — committed
├── kanban.html                  # GENERATED — committed
├── data.json                    # GENERATED — committed (sidecar for /kanban filter)
├── README.md
└── .gitignore                   # blocks /tmp, .env, raw-data-cache, etc.
```

Generated `index.html`, `kanban.html`, `data.json` ARE committed (yes, every cron run creates a commit — accepted v1 trade-off, squash periodically). Vercel auto-deploys on push.

### 6b. `build.py` pseudocode

```python
#!/usr/bin/env python3
"""Agent Fleet Observability Dashboard — build script.
   Runs on Mac Mini cron at 06:00 ET daily.
   Reads vault data, emits public/index.html (committed) + private file.
"""

VAULT = Path.home() / "Code-Brain/claude-code-superuser-pack/vault"
PRIVATE_OUT = Path.home() / "Sites/agent-fleet-private"
REPO = Path(__file__).parent

def main():
    data = {
        "agent_runs": readers.read_run_history(VAULT / "90_system/agent-logs/agent-run-history.csv"),
        "synth_manifests": readers.read_synth_manifests(VAULT / "health"),
        "gemini_spend": readers.read_gemini_spend(VAULT / "health"),
        "council_spend": readers.read_council_spend(VAULT / "health"),
        "lint_reports": readers.read_lint_reports(VAULT / "health"),
        "eval_last_run": readers.read_eval_last_run(VAULT.parent / "evals/vault-synthesizer/last-run.md"),
        "job_feed_db": readers.read_job_feed_db(VAULT / ".job-feed.db"),
        "job_feed_manifests": readers.read_job_feed_manifests(VAULT / "health"),
        "research_queue": readers.read_research_queue(VAULT / "00_inbox/research-queue.md"),
        "manual_tickets": readers.read_manual_tickets(VAULT / "00_inbox/tickets.md"),
    }

    agg = aggregations.compute_all(data)
    kanban_tickets = kanban.compose_tickets(data, agg)

    # Public pass — strip job-hunt + log excerpts
    public_data = anonymize.public_pass(agg, kanban_tickets)
    public_render.render_fleet(public_data, REPO / "index.html")
    public_render.render_kanban(public_data, REPO / "kanban.html")
    public_render.render_data_sidecar(public_data, REPO / "data.json")

    # Private pass — keep everything
    PRIVATE_OUT.mkdir(parents=True, exist_ok=True)
    private_render.render_fleet(agg, kanban_tickets, PRIVATE_OUT / "index.html")
    private_render.render_kanban(agg, kanban_tickets, PRIVATE_OUT / "kanban.html")
    private_render.render_data_sidecar(agg, kanban_tickets, PRIVATE_OUT / "data.json")

    # Diff-and-commit public artifacts only if changed
    if has_changes(REPO):
        subprocess.run(["git", "-C", REPO, "add", "index.html", "kanban.html", "data.json"], check=True)
        subprocess.run(["git", "-C", REPO, "commit", "-m", f"snapshot {timestamp()}"], check=True)
        subprocess.run(["git", "-C", REPO, "push"], check=True)

if __name__ == "__main__":
    main()
```

### 6c. Schedule

Launchd plist at `~/Library/LaunchAgents/com.sean.agent-fleet-dashboard.plist`:

```xml
<!-- StartCalendarInterval: every day at 06:00 -->
<key>StartCalendarInterval</key>
<dict>
  <key>Hour</key>
  <integer>6</integer>
  <key>Minute</key>
  <integer>0</integer>
</dict>
```

Hand-managed for v1 (don't auto-install via `install_schedules.sh` until the build proves stable for a week). EnvironmentVariables include `PATH` with `/usr/local/bin` and `/opt/homebrew/bin` per the launchd requirement documented in CLAUDE.md.

### 6d. Build performance budget

- **Cron-fire to public-live**: < 60 seconds total
  - Build: < 10 sec (Python + Jinja, all-local I/O)
  - Git commit + push: < 5 sec
  - Vercel build + deploy: < 30 sec (static — no framework build)
- **Page weight budget** (public/index.html): < 50 KB pre-data, < 200 KB with data
- **Cold-cache TTFB** (Vercel edge): < 200ms continental US

### 6e. Failure handling

| Failure | Behavior |
|---|---|
| Vault path inaccessible (Mac Mini not awake, etc.) | Build aborts with clear log entry; previous snapshot stays live; no commit |
| Single data source missing | Skip that panel with Sean-voice empty state ("Synth napped — MBP was asleep") |
| Git push fails (no network) | Log + retry on next cron; previous snapshot stays live |
| Generated HTML > 200 KB | Build emits warning but proceeds (soft budget) |
| Vercel deploy fails | Sean gets email from Vercel; previous deploy stays live |

---

## 7. Kanban v1 spec (read-only)

### 7a. Columns

`Backlog · ToDo · InProgress · Testing · Done`

### 7b. Filter chips (top of board)

Five chips, one per ticket source. Each chip clickable (client-side filter via `data.json` sidecar — toggles which tickets render). Counter shown next to each.

### 7c. Ticket card schema

```typescript
type Ticket = {
  id: string;                    // stable hash of source + title
  title: string;                 // user-facing
  source: 'research' | 'lint' | 'eval' | 'manual' | 'feed';
  assigned_agent: string | null; // 'deep_researcher' | 'synthesizer' | etc. | 'Sean' | null
  column: 'backlog' | 'todo' | 'in_progress' | 'testing' | 'done';
  is_running: boolean;           // for InProgress: render live-pulse dot
  created_at: ISO8601;
  moved_at: ISO8601;             // when it landed in current column
  link?: string;                 // optional — to vault file or external URL
  details?: string;              // optional — short text for hover/expand
};
```

### 7d. v2 deferred — interactive write-back

See `vault/.../memory/project_agent_fleet_dashboard_kanban_v2.md` for the deferred-work notes. v2 scope summarized:

- `tickets.json` (or SQLite table) as canonical source of truth
- Agent runtime gains queue-awareness — picks up assigned tickets, writes status back
- Drag-to-reassign UI
- Real-time updates via short-poll or websocket
- Dispatch logic + failure handling

Validation gate before starting v2: 1+ recruiter engagement attributed to v1 OR 4+ weeks live (whichever first).

---

## 8. Mobile + responsive

### 8a. Breakpoints

- **Desktop primary**: ≥ 1024px (target render width)
- **Tablet**: 768–1023px (4-col grids collapse to 2-col)
- **Mobile**: < 768px (everything stacks to single column)
- **Screenshot/mobile floor**: 375px (iPhone) — single-column, every panel survives

### 8b. Mobile-specific rules

- KPI cards: 4-up → 2×2 → 1-up
- Agent grid: 4-up → 2-up at 768px → 1-up at 480px (compact tile variant)
- Hero regression chart: maintains viewBox proportions; SVG scales fluidly
- Kanban: 5-col board → horizontal-scroll on tablet → stacked accordion on mobile
- Top bar: nav links wrap below wordmark on < 480px

### 8c. Mascot mobile sizing

The 32px mascot stays 32px on mobile (already at minimum legible scale). On screenshots / posters, scales up to 48px alongside larger wordmark.

---

## 9. Success Criteria

Updated from the v1 spec's Section 8 with locked decisions.

| # | Criterion | How verified |
|---|---|---|
| 1 | Single HTML file < 50 KB pre-data (each route) | `wc -c index.html` and `wc -c kanban.html` |
| 2 | Loads + renders in < 2 sec on cold cache | Chrome DevTools Performance audit |
| 3 | All 8 fleet tiles show real data from `agent-run-history.csv` | Visual + `csvkit` cross-reference |
| 4 | 30-day synthesizer telemetry shows the May 1–10 regression visibly with annotation | Visual + annotation present |
| 5 | Mobile rendering survives a single iPhone screenshot at 375px width | Manual phone test |
| 6 | Recruiter cold-open passes the 30-sec test (informally tested with a non-PM friend) | Self-assessment + 2 outside readers |
| 7 | `README.md` 4Q artifact lands in the repo | File exists, < 90-sec recruiter readability |
| 8 | 60-sec Loom recording walks through main panels + the kanban | Loom URL exists, plays end-to-end |
| 9 | Substack post 2 ships with the dashboard screenshot as visual hero | Substack post URL exists |
| 10 | At least 1 attributable recruiter engagement attributed to this artifact | Recorded in `[[target-companies]]` notes column |
| 11 | Privacy boundary holds: no job-hunt data on public, ever | Manual inspect of public surface + grep generated HTML |
| 12 | Asterisk Spark mascot renders + animates correctly on Chrome / Safari / Firefox | Manual cross-browser check |
| 13 | Build script completes in < 60 sec cron-fire-to-live | Time `make build && git push` |
| 14 | Kanban v1 read-only board renders with at least 1 ticket per source type | Visual smoke test on first build |
| 15 | `prefers-reduced-motion` disables mascot spin + blink | Manual check via OS setting |

---

## 10. Anti-patterns (preserved from v1 spec)

- ❌ Real-time WebSocket / 1-second-poll telemetry — daily cadence is enough
- ❌ Login / auth on public — public read-only or `file://` private, that's it
- ❌ Mocked data labeled as real — every number traces to a verifiable source file
- ❌ More than 7 colors in any chart — chart-junk anti-pattern
- ❌ Auto-rotating carousel / hero image — static layout only
- ❌ Generic "Look at all these tools I use" tile grid — every tile must be a *running* agent
- ❌ Job-hunt overlay made publicly visible by default — never, structurally enforced
- ❌ A claim the data doesn't back — recovered failures are the credibility story
- ❌ Nested-session-span / agent-trajectory waterfall (Gemini DR's "outsized impact" rec) — **explicitly rejected.** Sean's agents are independent cron jobs, not nested traces; the visualization is a category mismatch for this system. Each agent run is atomic. Reference: Gemini DR Section 10.
- ❌ Cloudflare orange-cloud proxy in front of Vercel — DNS-only (gray cloud); Vercel handles SSL

---

## 11. v2 / Future Work (deferred)

| Item | Scope | Trigger |
|---|---|---|
| Interactive kanban with agent write-back | `tickets.json` source of truth, drag-to-reassign UI, agents read+write status, live updates | 1+ recruiter engagement attributed to v1 OR 4+ weeks live |
| Per-skill / per-MCP telemetry | Surface which skills + MCPs are most-used in the agent runs | Post-v2 kanban |
| Cost forecasting | Project monthly spend based on current burn rate | Post-v2 kanban |
| Substack post 2 hero variant | Dedicated 375px screenshot-optimized render mode | When Substack post 2 ships |
| Custom domain SSL renewal automation | Currently manual via Vercel — could be automated | If a renewal ever fails |
| Public archive page beyond 7 days | Browseable history of completed tickets | If `/archive` Done column gets unwieldy |
| Knowledge graph deep-dive panel | Concept count, top clusters, recently modified — pulls from `concept_edges` SQL table | Post-v1 once schema is settled |

---

## 12. References

- Original spec: [[2026-05-13-agent-fleet-dashboard-spec]] (now superseded; status update flipped to `research-complete` in 2026-05-15 commit)
- ChatGPT DR: [[2026-05-14-Agent-Fleet-Observability-Dashboard-ChatGPT]]
- Gemini DR: [[2026-05-14-Agent-Fleet-Observability-Dashboard-Gemini-DR]]
- Roadmap: [[2026-05-06-unified-roadmap]] (Task 11 in roadmap needs to be updated post-design with locked ship date + distribution surface)
- sw-portfolio design tokens: `[[sw-portfolio/DESIGN-SPEC-V4]]` (deferred — informs token choices; tokens here are stand-alone for v1)
- v2 kanban deferred-work memory: `project_agent_fleet_dashboard_kanban_v2.md`

---

## 13. Schedule + Cost

**Time:** 4 working days post-design (kanban v1 added ~1 day to the original 2–3-day estimate from the v1 spec).
- Day 1: build pipeline scaffolding · data readers · aggregations · top-bar + agent grid + KPI row · mascot CSS
- Day 2: regression hero chart · below-fold panels (cost trend, model mix, recent runs, synth telemetry, eval case grid) · public/private split rendering · anonymization layer
- Day 3: kanban v1 page · ticket composers per source · column-membership rules · filter chips · live-pulse for InProgress
- Day 4: mobile responsive pass (375px floor) · Vercel deploy + Cloudflare CNAME · launchd plist + cron · README + Loom recording

Optional Day 5 buffer for: cross-browser polish (Safari WebKit quirks), copy edits, recruiter-friendly README, or unexpected data-source edge cases.

**Cost:** $0 cloud (Vercel free + Cloudflare free; domain already owned). $0 LLM (build is local Python, no inference calls).

**Schedule placement:** earliest start 2026-05-26 (after eval suite Loom + Substack post 1 ship 2026-05-22). Ship target **2026-05-29 to 2026-06-08**.

Slips do not affect Track-C, animation pipeline (6/11), or `vault-knowledge-mcp` (Task 10). Tier-A protected.

---

## 14. Tier-A Compliance Check (operating model)

- **Walk-away $100k base:** N/A — portfolio artifact, not a paid role
- **5-days-in-office no:** N/A — local work
- **AI > Tech > Creative PM ordering:** ✅ — pure AI-PM artifact, demonstrates Agent Ops backup track
- **Agents draft / Sean sends:** ✅ — Sean publishes; agents can draft Substack copy
- **Track-C protected:** ✅ — `intent-engineering` and `vault-knowledge-mcp` ship independently; this is downstream supporting work
- **Friday 4:30 retro:** ✅ — build fits inside 8:30–5:30 deep-work container
- **5:30 PM hard stop:** ✅ — 3-day build does not require evening overflow

---

**Status:** design-complete. Next step: invoke `writing-plans` skill to produce a step-by-step implementation plan from this design.
