---
type: design-spec
project: prj-job-hunt-2026
created: 2026-05-09
agent_target: agents-sdk
status: approved
ai-context: "Job-feed agent v1 design spec. Phased approach (Phase 1 = free local sources, hybrid scoring, daily roll-up). Phase 2 (paid sources, referral-orbit scoring, notifications) deferred until coverage gaps observed."
---

# Job Feed Agent — v1 Design Spec

## Goal

Automate daily discovery of PM/APM/Technical PM/AI PM roles that fit Sean's
Tier-A constraints (post-Block, 2026-05 job hunt). Surface scored hits in the
vault each morning so Sean can triage and apply manually.

The agent does **not** auto-apply, does **not** notify externally, and does
**not** introduce cloud LLM cost. It is a discovery and triage aid, not an
autonomous applicant.

## Non-Goals (v1)

- Auto-applying to roles
- LinkedIn / Wellfound / Indeed scraping (ToS violation + IP-ban risk)
- SerpAPI or other paid feed gateways (deferred to Phase 2)
- Referral-orbit scoring (Matt/Larry connection signal — Phase 2)
- Desktop notifications (Phase 2 hook designed in)
- Workday / custom-careers-page scraping (fragile; Phase 2 if needed)
- Per-role markdown files (chose daily roll-up; revisit if roll-up gets unwieldy)
- Cross-conversation memory or long-term role history beyond raw SQLite

## Phased Strategy

**Phase 1 (this spec):** Ship free, all-local v1 in 1–2 implementation sessions.
Run for ~2 weeks. Identify coverage gaps from real triage data.

**Phase 2 (deferred, separate spec):** Add SerpAPI for Google-Jobs / LinkedIn-via-search
coverage if v1 misses material role classes. Add referral-orbit scoring axis
(static seed list of Matt/Larry-connected companies, separate fit dimension).
Add desktop notification hook if morning brief surfacing proves insufficient.

## Tier-A Constraints (Hard Filters)

Lifted verbatim from Sean's existing `2026-05-08-prompt-crypto-pm-referral-targets.md`:

- Walk-away salary: **$100k base** (rules-filter uses $90k as soft buffer to
  give benefit of the doubt; LLM scorer evaluates final fit)
- Office: **≤3 days RTO** (prefers 0–2; remote ideal)
- Geography: **US-remote OR Boston-metro**
  (Boston, Cambridge, Somerville, Waltham, Newton, Brookline, reasonable
  commute zone)
- Time zone: must accommodate **Eastern Time**

## Eligible Role Bands

- Associate Product Manager (APM) — primary fit
- Product Manager / PM I / PM II — primary fit
- Senior APM — fit
- Senior PM — STRETCH (LLM judges based on YOE floor in JD)
- Principal PM — STRETCH (some companies use as IC track; LLM judges)
- Director / Head of Product / VP / Group PM / Sr Director / CPO — EXCLUDE

## Architecture

### File layout (new files)

```
agents-sdk/
├── agents/
│   └── job_feed.py                    # main agent entrypoint
├── lib/
│   └── job_sources.py                 # feed + ATS adapter library
├── schedules/
│   └── com.sean.job-feed.plist        # launchd schedule
└── tests/
    └── test_job_sources.py            # adapter unit tests with fixtures

agents-sdk/scripts/
└── update_status.py                   # CLI helper to mutate posting status

vault/
├── .job-feed.db                       # SQLite (standalone, not folded into .vault-index.db)
└── 20_projects/prj-job-hunt-2026/
    ├── job-feed/
    │   ├── watchlist.yaml             # company list (user-editable)
    │   └── YYYY-MM-DD.md              # daily roll-ups
    └── job-feed-archive/              # placeholder for future archival

vault/health/
└── job-feed-manifest-{date}.json      # per-run health manifest
```

### Touched files (minor edits)

- `agents-sdk/config.toml` — add `[job_feed]` section
- `agents-sdk/schedules/install_schedules.sh` — register/unregister the new plist
- `agents-sdk/agents/daily_driver.py` — morning mode reads today's job-feed roll-up
  if present and appends a small summary block to the brief
- `CLAUDE.md` — agent table update (active fleet 7 → 8); architecture comment;
  hooks/agents counts if applicable
- `CHANGELOG.md` — version bump entry under Added
- `README.md` — counts and tables

### Untouched files (intentionally)

- `vault_indexer.py`, `vault_synthesizer.py`, `flush.py`, `meta_agent.py`,
  `knowledge_lint.py`, `process_inbox.py`, `deep_researcher.py`,
  `gemini_researcher.py`, `pr_digest.py`, `preserve_session.py`,
  `spending_analysis.py`, `sprint_health.py`
- `.vault-index.db` schema — job-feed has its own standalone DB
- All existing skills under `.claude/skills/`
- All existing subagents under `.claude/agents/`

## Data Sources

### Aggregator feeds (4)

| Source | Endpoint | Cadence | Notes |
|---|---|---|---|
| RemoteOK | `https://remoteok.com/api` | Live | Public JSON, broad remote tech, well-tagged |
| HN "Who's Hiring" | `https://hn.algolia.com/api/v1/search?tags=story&query=Ask+HN+Who+is+hiring` | Live | Filter to current month's thread; parse comments |
| web3.career | `https://web3.career/api/v1?token=<keychain>` | Live | Free tier with token; crypto vertical |
| WeWorkRemotely | `https://weworkremotely.com/categories/remote-product-jobs.rss` | Live | Public RSS, generalist remote |

Each adapter implements a uniform interface in `lib/job_sources.py`:

```python
class FeedAdapter(Protocol):
    name: str
    async def fetch(self, since: datetime | None) -> list[Posting]: ...
```

### Watchlist (~40 companies, user-editable)

Stored in `vault/20_projects/prj-job-hunt-2026/job-feed/watchlist.yaml`. The agent
reads it on every run; no code change to add/remove companies.

```yaml
ai_native:
  - anthropic, openai, huggingface, cohere, mistral, perplexity
  - glean, sierra, scale, replicate, together-ai
  - cursor, replit, lovable, modal, pinecone, langchain, vercel, supabase

ai_creative_crossover:
  - elevenlabs, suno, pika, krea, tome, gamma, heygen, synthesia
  - runway, descript

creative_design:
  - figma, canva, linear, notion, webflow, framer, spline

creator_economy:
  - beehiiv, fourthwall

boston_metro:
  - hubspot, draftkings, toast, klaviyo, datarobot
  - hopper, circle

crypto_warm_network:
  - messari, coinbase, kraken
```

ATS auto-detection at runtime: agent attempts Greenhouse, Lever, then Ashby endpoints
in order. First non-404 wins. Companies with no match get dropped from the run with
a one-line warning logged to the run manifest.

ATS endpoints used:
- Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true`
- Lever: `https://api.lever.co/v0/postings/<slug>?mode=json`
- Ashby: `https://api.ashbyhq.com/posting-api/job-board/<slug>?includeCompensation=true`

## Pipeline

```
fetch → dedupe → rules-filter → LLM scoring → persist → render roll-up
```

### 1. Fetch

All 4 feed adapters + ~40 ATS pollers run in parallel via `asyncio.gather()`.
Politeness:
- 1 req/sec per host (asyncio semaphore keyed on hostname)
- 10-sec timeout per HTTP request
- Honor `Retry-After` headers
- User-Agent: `SeanWinslow-JobFeed/1.0 (personal job-hunt agent)`
- Exponential backoff on 429 / 5xx (max 3 retries)

Yields a unified `Posting` dataclass:

```python
@dataclass
class Posting:
    source: str            # 'remoteok', 'hn', 'greenhouse:anthropic', ...
    source_role_id: str
    url: str
    company: str
    title: str
    location: str | None
    salary_disclosed: str | None
    posted_at: datetime | None
    description: str       # raw, normalized to Markdown via markdownify
```

### 2. Dedupe

Query SQLite for existing `(source, source_role_id)`. Three states:

| DB state | Action |
|---|---|
| Not in DB | New — proceed to rules-filter |
| In DB, `fit_score IS NOT NULL` | Already scored — skip |
| In DB, `fit_score IS NULL AND rules_passed = 1` | Carryover from prior run — re-queue for scoring |

Retention: `(source, source_role_id)` once scored never re-surfaces (locked
in Q6). The carryover case is for postings persisted on a day MBP stayed asleep —
they get scored on the next run when MBP is reachable.

### 3. Rules-Filter

Drop with zero LLM cost:

| Reason | Rule |
|---|---|
| Too senior (band) | Title regex matches `Director`, `VP`, `Head of`, `Group PM`, `Sr Director`, `EVP`, `CPO` |
| Too senior (YOE) | Description first 500 chars contains `7+ years`, `8+ years`, `10+ years` |
| Geo ineligible | Location explicitly non-US-and-non-remote (e.g., `London-only`, `Berlin`, `EMEA-only`, `Tokyo`, `Toronto-only`) |
| Below salary floor | Disclosed salary range upper bound < $90k |
| Not a PM role | Title doesn't match any of: Product Manager, Associate Product Manager, APM, PM I, PM II, Senior PM, Sr PM, Sr. PM, Principal PM, Product Lead, Product Owner, Technical PM, Lead PM |

Rules persistedly drop ~70-80% of raw fetched postings. Rules-rejected postings
are still persisted to SQLite with `rules_passed=0` and `rules_rejection_reason`
set, so they don't re-process on subsequent runs and Sean can audit if he ever
feels role-classes are missing.

### 4. LLM Scoring (Qwen3-14B on MBP via HybridRouter)

Survivors go to scoring. Routing:

- `task = "job_scoring"`
- `fallback_disabled = true` — explicitly does NOT fall back to cloud Sonnet,
  to preserve $0 cost integrity. If MBP unreachable, scoring fails and
  postings persist with `fit_score=NULL` for re-scoring on the next run.

Prompt produces strict JSON:

```json
{
  "fit_score": 4,
  "role_band": "PM | APM | Sr_PM_stretch | Principal_stretch | Other",
  "rationale": "one-sentence why this lands or doesn't",
  "concerns": ["array of disqualifiers worth flagging"],
  "fit_dimensions": {"role_band_fit": 4, "geo_fit": 5, "industry_fit": 5, "yoe_fit": 3}
}
```

System prompt encodes Tier-A constraints + role bands + scoring rubric +
2-3 few-shot examples covering: clean APM-grade fit, Sr PM stretch with
domain depth, on-paper match that fails geo, ambiguous title.

### 5. Persist

Every fetched posting (rules-passed AND rules-rejected) writes to SQLite. The
full `Posting.description` is truncated to a 500-character `description_excerpt`
before storage — the agent never persists full job descriptions, since the URL
is already on record and full descriptions can be re-fetched if ever needed.
LLM-scored postings additionally render into the daily Markdown roll-up.

### 6. Render Roll-up

Generate (or regenerate) `vault/20_projects/prj-job-hunt-2026/job-feed/<today>.md`.
Format defined below.

## Storage Schema

### SQLite (`vault/.job-feed.db`)

```sql
CREATE TABLE job_postings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_role_id TEXT NOT NULL,
    url TEXT NOT NULL,
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    location TEXT,
    salary_disclosed TEXT,
    posted_at TEXT,
    first_seen_at TEXT NOT NULL,
    description_excerpt TEXT,
    rules_passed INTEGER NOT NULL,
    rules_rejection_reason TEXT,
    fit_score INTEGER,
    role_band TEXT,
    rationale TEXT,
    concerns TEXT,
    fit_dimensions TEXT,
    scored_at TEXT,
    status TEXT DEFAULT 'new',
    UNIQUE(source, source_role_id)
);

CREATE INDEX idx_first_seen ON job_postings(first_seen_at);
CREATE INDEX idx_fit_score ON job_postings(fit_score DESC) WHERE fit_score IS NOT NULL;
CREATE INDEX idx_status ON job_postings(status);
CREATE INDEX idx_unscored ON job_postings(rules_passed, fit_score)
  WHERE rules_passed = 1 AND fit_score IS NULL;
```

`status` values: `new` | `reviewed` | `applied` | `passed`. Mutated via
`update_status.py` CLI helper or directly in SQLite.

### Run manifest (`vault/health/job-feed-manifest-{YYYY-MM-DD}.json`)

```json
{
  "date": "2026-05-09",
  "runs": [
    {
      "fired_at": "2026-05-09T08:00:01-04:00",
      "fetch_total": 287,
      "rules_passed": 42,
      "rules_rejected": 245,
      "llm_scored": 42,
      "llm_failed": 0,
      "mbp_reachable": true,
      "duration_sec": 234,
      "failed_pollers": []
    }
  ]
}
```

Surfaced in the meta-agent fleet-health summary.

## Daily Roll-up Format

Sample `vault/20_projects/prj-job-hunt-2026/job-feed/2026-05-09.md`:

```markdown
---
type: job-feed-daily
project: prj-job-hunt-2026
date: 2026-05-09
total_surfaced: 12
top_fits: 4
medium_fits: 6
weak_fits: 2
unscored: 0
complete: true
ai-context: "Daily job-feed roll-up. Hits sorted by fit_score desc. Status mutations via update_status.py."
---

# Job Feed — 2026-05-09

**12 new fits** from 4 feeds + 40 watchlist polls.
4 strong (≥4) · 6 medium (3) · 2 weak (≤2) · 0 unscored.

## Top Fits (≥ 4/5)

### 1. Hopper — Senior PM, AI & Commerce Foundations · ⭐ 5/5
- **Source:** ashby:hopper · **Location:** Remote (US) · **Posted:** 2026-05-08 · **Comp:** not disclosed
- **Band:** Sr_PM_stretch · **Concerns:** YOE floor 3yr listed (you have 2yr + side portfolio)
- **Rationale:** Boston-HQ AI travel co, remote-OK, AI-PM crossover lands on Block ETF-data + side AI portfolio cleanly.
- **Status:** new
- 🔗 [Apply](https://jobs.ashbyhq.com/hopper/...) · **db_id:** 47

### 2. Anthropic — Product Manager, Claude Code · ⭐ 5/5
- ...

## Medium Fits (3/5)

### 5. Klaviyo — Product Manager, Customer Hub · ⭐ 3/5
- ...

## Weak Fits (≤ 2/5) — included for visibility

### 11. AcmeCo — Senior Product Manager, Logistics · ⭐ 2/5
- ...

## Carried Over from Yesterday — Now Scored

(only present if yesterday's run had unscored postings that today's run resolved)

## Unscored — MBP was asleep

(only present if MBP stayed asleep through the entire 8–11 AM window AND
yesterday's carryover wasn't resolved; effectively a "something is wrong"
banner)

## Triage

```bash
cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 scripts/update_status.py 47 applied
PYTHONPATH=. .venv/bin/python3 scripts/update_status.py 51 passed
```

(Or in an interactive Claude session: `update status 47 to applied`)
```

## Daily-Driver Morning-Brief Integration

`agents-sdk/agents/daily_driver.py` morning mode adds one method:

```python
def _append_job_feed_summary(self, today: str) -> str:
    """Append today's job feed summary to the morning brief, if available."""
    feed_path = self.vault_path / "20_projects/prj-job-hunt-2026/job-feed" / f"{today}.md"
    if not feed_path.exists():
        return ""
    fm = read_frontmatter(feed_path)
    top_3 = parse_top_fits(feed_path, n=3)
    return render_summary_block(fm, top_3, feed_path)
```

Called after the calendar section, before the vault-health section. ~30-40 lines
total including the small parser.

When the file exists and is `complete: true`, the brief renders:

```markdown
## Job Feed (2026-05-09) · 4 strong / 6 medium / 2 weak

- **Hopper** — Senior PM, AI & Commerce · Remote · 5/5 · [→](./job-feed/2026-05-09.md#1-hopper)
- **Anthropic** — PM, Claude Code · Remote · 5/5 · [→](./job-feed/2026-05-09.md#2-anthropic)
- **ElevenLabs** — APM, Music · Remote · 4/5 · [→](./job-feed/2026-05-09.md#3-elevenlabs)

[Full roll-up →](./job-feed/2026-05-09.md)
```

When the file exists but is `complete: false` (MBP still asleep at 8:45 AM):

```markdown
## Job Feed (2026-05-09) · Scoring deferred
MBP was asleep at 8 AM. Agent will retry hourly until 11 AM.
14 postings fetched and rules-filtered; LLM scoring pending.
[Refresh the roll-up after MBP wakes →](./job-feed/2026-05-09.md)
```

When the file doesn't exist (agent didn't run, or exited early): brief silently
omits the section. No spurious "0 fits" line.

## Schedule

`agents-sdk/schedules/com.sean.job-feed.plist`:

```xml
<key>Label</key><string>com.sean.job-feed</string>
<key>ProgramArguments</key>
<array>
  <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3</string>
  <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/job_feed.py</string>
</array>
<key>StartCalendarInterval</key>
<array>
  <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
  <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>30</integer></dict>
  <dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
  <dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>30</integer></dict>
  <dict><key>Hour</key><integer>10</integer><key>Minute</key><integer>0</integer></dict>
  <dict><key>Hour</key><integer>10</integer><key>Minute</key><integer>30</integer></dict>
  <dict><key>Hour</key><integer>11</integer><key>Minute</key><integer>0</integer></dict>
</array>
<key>EnvironmentVariables</key>
<dict>
  <key>PATH</key>
  <string>/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
  <key>PYTHONPATH</key>
  <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk</string>
</dict>
<key>WorkingDirectory</key>
<string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk</string>
<key>StandardOutPath</key>
<string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/logs/job-feed.out.log</string>
<key>StandardErrorPath</key>
<string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/logs/job-feed.err.log</string>
```

The `PATH` env var is the launchd workaround documented in
`agents-sdk/BUGFIX-2026-04-07-launchd-path.md`. Mandatory.

### Per-fire idempotency logic

```
1. Compute today_et = current Eastern Time date.
2. Load today's roll-up frontmatter if it exists.
   IF complete == true: exit 0 silently.  (~50ms total)
3. Determine if fetch is needed: last_fetched_at > 4 hours ago, OR no fetch today.
   IF YES: run fetch + rules-filter + persist (no LLM needed for either).
4. Probe MBP reachability: HTTP HEAD to Ollama on MBP, 2-sec timeout.
   IF NO: write/refresh roll-up with current state (rules-rejected scored;
          rules-passed marked unscored), set complete=false, exit 0.
   IF YES: query SQLite for postings WHERE
          rules_passed=1 AND fit_score IS NULL AND
          (date(first_seen_at) = :today_et OR date(first_seen_at) < :today_et).
          (Note: SQLite syntax — `date()` function, parameterized `:today_et`.)
          Score them. Regenerate roll-up. Set complete=true if all scored.
```

### Outcomes by scenario

| Scenario | Result |
|---|---|
| MBP awake at 8:00 | First fire does everything. Fires 2-7 see `complete=true`, exit 50ms. |
| MBP wakes 8:45 | 8:00 fire writes partial (rules-rejected only). 9:00 fire scores backlog. Morning brief at 8:45 shows "Scoring deferred." Sean refreshes the roll-up after 9:00. |
| MBP wakes 10:30 | 10:30 fire catches it. |
| MBP asleep all morning | All 7 fires no-op on scoring. Roll-up shows postings as unscored. **Tomorrow's run** picks them up via the dedupe carryover logic. Nothing permanently lost. |

## Safety, Costs, Operational Guardrails

### Cost model

| Component | Cost |
|---|---|
| 4 feed adapters | $0 (free public APIs/RSS) |
| ~40 ATS pollers | $0 (Greenhouse/Lever/Ashby public endpoints) |
| Qwen3-14B scoring on MBP | $0 (local) |
| SQLite + Markdown writes | $0 |
| **Total** | **$0/run** |

Defensive cap in config: `max_cost_usd = 0.10`. Tripwire only — should never fire.

### LLM routing — explicit no-fallback

`fallback_disabled = true` for `task = "job_scoring"`. If MBP is unreachable,
scoring fails fast; postings persist with `fit_score=NULL`. Reasons:

1. Cost integrity — Sonnet fallback at ~$0.003/1k tokens × ~50 postings
   would silently exceed the $0.10 cap.
2. Visibility — Sean prefers "scoring deferred" UX over a surprise cloud bill.

### ToS compliance

All v1 sources are explicitly public APIs:

| Source | License/ToS basis |
|---|---|
| RemoteOK API | Public, documented at remoteok.com/api |
| HN Algolia | Public, documented at hn.algolia.com/api |
| web3.career API | Public free tier with token |
| WeWorkRemotely RSS | Public RSS, intended for syndication |
| Greenhouse / Lever / Ashby | Public job-board endpoints, intended for syndication |

Explicitly NOT scraped: LinkedIn, Wellfound, Indeed, Glassdoor, BuiltIn.

### Secrets

- web3.career token: macOS Keychain at `com.sean.agents.web3career_token`
  (mirrors the `com.sean.agents.gemini_api_key` pattern)
- No other secrets in v1

### Disable / kill-switch

Three levels of granularity, all reversible:

1. **One-off skip:** `touch agents-sdk/.disable-job-feed` — agent checks at
   startup, exits 0 if present
2. **Persistent disable:** `enabled = false` in `[job_feed]` config — agent exits
   immediately
3. **Full uninstall:** `launchctl unload ~/Library/LaunchAgents/com.sean.job-feed.plist`,
   then remove plist + DB + folder. ~5 commands total. No surgery on shared infra.

### Privacy

All postings are public listings. SQLite stays local. No outbound data egress
beyond standard HTTP requests to public APIs. User-Agent string contains no
Sean-identifying info.

## Failure Modes

| Failure | Handling |
|---|---|
| Network down | Fetch fails, error logged, no roll-up written, brief omits section |
| MBP asleep | Per the polling logic above; carryover handles it |
| One ATS endpoint 404s | Per-poll try/except, others continue; logged in run manifest |
| Watchlist YAML malformed | Fail at startup, no run, error in stderr log |
| SQLite locked | Standalone DB; no contention with vault_indexer |
| Cost cap hit | Defensive only; halts and logs |
| LLM returns malformed JSON | Try-parse, fall back to a default-low score with rationale "LLM output unparseable", concern flag set so Sean can audit |

## Configuration

`agents-sdk/config.toml` adds:

```toml
[job_feed]
enabled = true
max_cost_usd = 0.10
http_timeout_sec = 10
rate_limit_per_host_per_sec = 1
mbp_probe_timeout_sec = 2
mbp_probe_url = "http://mbp.local:11434/api/tags"  # Ollama on MBP
fetch_skip_if_within_hours = 4
fallback_disabled = true
log_level = "INFO"

[job_feed.paths]
db = "vault/.job-feed.db"
watchlist = "vault/20_projects/prj-job-hunt-2026/job-feed/watchlist.yaml"
roll_up_dir = "vault/20_projects/prj-job-hunt-2026/job-feed"
manifest_dir = "vault/health"
```

## Phase 2 Hooks (designed in, not implemented in v1)

- **SerpAPI / Google Jobs adapter** — drops into `lib/job_sources.py` next to
  the others; no schema changes
- **Referral-orbit scoring** — extends LLM prompt with a `referral_orbit`
  dimension in `fit_dimensions` JSON; static seed list in
  `vault/20_projects/prj-job-hunt-2026/referral-orbit.yaml`
- **Desktop notification** — helper using `terminal-notifier`, gated by
  `notify_desktop = true` in config
- **More watchlist companies** — edit YAML; no code change
- **Cross-day analytics** — SQLite already supports queries like "postings still
  open after 14 days," "fit-score distribution by source," etc.

## Testing Strategy

### Unit tests (pytest, no network)

- `test_job_sources.py`:
  - Each adapter tested with fixture HTML/JSON in `tests/fixtures/`
  - Edge cases: empty feed, malformed posting, timezone handling, salary parsing
- `test_rules_filter.py`:
  - Title regex matching (positive + negative cases per band)
  - YOE-floor detection
  - Geo eligibility
  - Salary floor
- `test_dedupe_logic.py`:
  - Three states: not in DB, scored, unscored carryover
  - SQLite UNIQUE constraint enforcement
- `test_roll_up_renderer.py`:
  - Rendered Markdown matches snapshot
  - Frontmatter counts correct

### Integration tests

- `test_job_feed_e2e.py` (mocked HTTP):
  - Full pipeline with VCR-recorded HTTP fixtures
  - Idempotent re-run produces no duplicate writes
  - Carryover logic resolves yesterday's unscored

### Live smoke test

- `--dry-run` flag: fetch + rules + persist to a temp DB, print scoring queue
  count, do not call MBP, do not write roll-up
- Run manually before enabling launchd schedule

## Open Items / Known Uncertainties

1. **ATS slug accuracy.** Watchlist company slugs (e.g., `anthropic`,
   `huggingface`) are best-guess. Implementation phase will validate each
   against the live endpoints; failures get dropped with a one-line warning.
   Expect 20–30% slug churn in week 1; should stabilize by week 2.

2. **Description normalization.** ATS feeds return mixed Markdown / HTML / raw
   text. `markdownify` handles most; edge cases (Lever specifically uses some
   custom formatting) may produce ugly excerpts. Won't block scoring.

3. **HN "Who's Hiring" parsing.** Forum-comment extraction is heuristic;
   expect ~70-80% precision. Acceptable for a discovery feed.

4. **Watchlist size growth.** v1 starts at ~40 companies. If this grows past
   ~80, fetch phase parallelism may need an explicit semaphore cap to avoid
   triggering anti-DDoS heuristics on shared ATS hosts. Not a v1 concern.

## Mandatory Doc Updates (per CLAUDE.md)

When this spec is implemented, the implementer MUST update:

- `CHANGELOG.md` — entry under the version's Added section
- `CLAUDE.md` — agent table (active fleet 7 → 8); architecture comment if needed
- `README.md` — agent counts and any affected tables

These are project conventions; the implementation plan will track them as
explicit tasks.

## Acceptance Criteria

v1 is complete when:

1. `pytest agents-sdk/tests/ -v` passes (existing 241 tests + new tests for
   adapters, rules, dedupe, renderer)
2. `python3 scripts/validate.py` passes (validates skill/agent/hook structure)
3. `agents-sdk/agents/job_feed.py --dry-run` runs end-to-end against live
   feeds without errors
4. Live `agents-sdk/agents/job_feed.py` produces a daily roll-up file in the
   expected location with valid frontmatter and ≥1 scored posting
5. `daily_driver.py --mode morning --dry-run` shows the job-feed summary block
   when the roll-up exists
6. `launchctl load` of the new plist succeeds; `launchctl list | grep job-feed`
   shows it registered
7. Disable path verified: `touch .disable-job-feed` causes immediate exit 0
8. Documentation updated: CLAUDE.md, CHANGELOG.md, README.md
