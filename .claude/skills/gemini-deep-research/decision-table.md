# Gemini Deep Research — Decision Table & Worked Examples

Standalone routing reference for the `gemini-deep-research` skill. The skill body (`SKILL.md`) cites this file for the full decision logic, worked examples, and cost-cap escape paths.

---

## Routing Decision Table

| Question shape | Tool | Cost | Wall time |
|---|---|---|---|
| "What's hot on Reddit / X / TikTok about X this week?" | `last30days` | $0 (or SC API) | 2–8 min |
| "What are the practical differences between A and B?" with general web coverage | `deep-research-queue` (LDR) | $0 | 5–12 min overnight |
| "Recent (post-2025), authoritative, ≥10 sources, citation quality matters" | **`gemini-deep-research` DR tier** | $1–3 | 5–20 min |
| "Cross-service matrix / due-diligence / comprehensive landscape" | **`gemini-deep-research` DR Max tier** | $3–7 | 20–60 min |

### Routing signal cheat-sheet

Use this to break ties when the question shape is ambiguous:

| Signal | Route to |
|---|---|
| Contains "Reddit", "Twitter", "X", "TikTok", "what are people saying", "trending" | `last30days` |
| Contains "queue", "research this later", "overnight is fine", "can wait" | `deep-research-queue` |
| Contains "citation", "authoritative", "post-2025", "recent sources", "need it now" | `gemini-deep-research` DR tier |
| Contains "matrix", "comprehensive", "due diligence", "landscape", "every service" | `gemini-deep-research` DR Max tier |
| Price sensitivity explicit ("$0", "free", "local") | `deep-research-queue` first |

---

## Worked Example 1 — Routes to `last30days`

**Question:** "What's the Reddit conversation about Claude Code skills look like this week?"

**Classification reasoning:**
- Explicit platform signal: "Reddit conversation"
- Time signal: "this week" — recency matters, but for social sentiment not authoritative citations
- Output shape: trends, engagement, what people are saying — not a research report with citations
- Cost justification: $0 via `last30days` covers this perfectly; Gemini DR would return authoritative web articles about Claude Code, not Reddit thread sentiment

**Route:** `last30days`

**Invocation:**
```
/last30days Claude Code skills
```

**Expected output shape:** Trend brief with engagement metrics — top Reddit threads, X posts, HN discussions. Includes upvote counts, comment summaries, and cross-platform signals. ~2–8 min, $0 (or SC API cost for Reddit comments/TikTok).

**Expected cost:** $0 (or negligible ScrapeCreators API cost if Reddit comments enabled)

---

## Worked Example 2 — Routes to `deep-research-queue`

**Question:** "What are the practical differences between Ollama Modelfile and ComfyUI custom nodes?"

**Classification reasoning:**
- General technical comparison — well-covered by public web documentation and community resources
- No recency requirement — this is stable tooling, not post-2025 breaking changes
- Output shape: synthesis with citations — exactly what LDR + Qwen3-14B delivers
- This exact question was already completed: `vault/20_projects/research/2026-05-03-what-are-the-practical-differences-between-ollama-modelfile.md`
- Cost: $0 overnight vs $1–3 now with Gemini DR — LDR is the right call

**Route:** `deep-research-queue`

**Action:** Check `vault/00_inbox/research-queue.md` for duplicates first. If not already queued or completed, append `- [ ] What are the practical differences between Ollama Modelfile and ComfyUI custom nodes?` under `## Pending`.

**Expected output shape:** 800–1500 word synthesis report with ≥3 citations at `vault/20_projects/research/{YYYY-MM-DD}-{slug}.md`. Digest injected into next morning's daily note under `<!-- research-digest -->`.

**Expected cost:** $0 (Ollama + SearXNG + LDR, all local on Mac Mini)

**Wall time:** Queued tonight → available ~03:00 tomorrow

---

## Worked Example 3 — Routes to `gemini-deep-research` DR Max

**Question:** "Comprehensive auth-mode and key-generation matrix for Slack, Google Calendar, Gmail, Jira, GitHub, and Linear — covering OAuth flows, service account options, API key scoping, and MCP integration patterns."

**Classification reasoning:**
- Multi-service matrix: 6 services × 4 auth dimensions = 24 cells minimum
- Authoritative docs required: auth modes change; post-2025 accuracy matters (Slack's new MCP auth, GitHub fine-grained tokens, etc.)
- Citation quality critical: this feeds architectural decisions in the superuser-pack
- LDR + Qwen3-14B would struggle with ≥20 sources and structured matrix output
- DR tier could handle it but may miss depth on cross-service comparison
- DR Max is the right call: comprehensive landscape + structured matrix output

**Route:** `gemini-deep-research` DR Max tier

**Mandatory confirmation prompt to show Sean:**
```
Run Deep Research Max for ~$5 (range $3–7, ~30 min)?
Month-to-date Gemini spend: $X of $20 cap.
Options:
- "Yes, run DR Max" — proceed
- "Run standard DR instead ($1–3, 5–20 min)" — downgrade to DR tier
- "Queue to local deep-research-queue ($0, overnight)" — defer to LDR
- "Cancel" — stop
```

**Expected output shape:** Structured matrix report with per-service auth modes, OAuth flow diagrams (or descriptions), key-generation steps, MCP integration notes, and ≥20 citations from official API docs. Lands at `vault/20_projects/research/{date}-auth-matrix-slack-calendar-gmail-jira-github-linear.md`.

**Expected cost:** $3–7 (DR Max tier)

**Wall time:** 20–60 min

---

## Cost-Cap Escape Paths

When `gemini_dr.py` refuses a call because a cap is hit, here are the options in priority order:

### (a) Raise the cap in config.toml

Edit `agents-sdk/config.toml` under `[gemini.budget]`:

```toml
[gemini.budget]
monthly_cap_usd = 30    # raise from default $20
daily_cap_usd = 15      # raise from default $10
```

Then re-invoke. Use this when the research is high-priority and the cap is genuinely too conservative.

### (b) Queue to `deep-research-queue` for $0 local synthesis

Add the question to `vault/00_inbox/research-queue.md` via the `deep-research-queue` skill. The LDR agent runs tonight at 02:45 on Mac Mini. Output will be shallower (≥3 sources vs ≥20 for DR Max) but at $0.

Good fit when: question can wait overnight, general web coverage is sufficient, citation count doesn't need to be high.

### (c) Wait until next month

The monthly cap resets at the first of each calendar month. The spend ledger is at:
```
vault/health/gemini-spend-{YYYY-MM}.json
```

Read the ledger to confirm the reset date and current spend:
```bash
ls vault/health/gemini-spend-*.json
cat vault/health/gemini-spend-$(date +%Y-%m).json
```

### Which to choose

| Situation | Recommended escape |
|---|---|
| Research is time-sensitive (needed today) | (a) raise cap |
| Research can wait until tomorrow morning | (b) queue to deep-research-queue |
| Daily cap hit but monthly cap has headroom | (a) raise daily cap or wait until tomorrow |
| Monthly cap hit with >5 days left in month | (a) raise monthly cap OR (c) wait |
| Monthly cap hit with ≤3 days left in month | (c) wait for reset |
| Question is general enough for LDR | (b) queue regardless of cap status |
