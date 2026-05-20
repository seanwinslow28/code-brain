---
name: gemini-deep-research
description: Invoke Google's Gemini Deep Research or Deep Research Max APIs for paid, comprehensive research with web grounding, citations, and optional charts. Use when Sean asks for "deep research", "gemini research", "deep research max", "comprehensive analysis with citations", "due diligence on X", or surfaces a question that needs ≥20 sources cross-referenced, recent (post-2025) authoritative content, or a structured matrix that the local LDR + Qwen3-14B path can't produce reliably. Skip for simple lookups (answer in-session), social-media trend questions (use last30days), or questions answerable by the local deep-research-queue at $0/run. Always prompts for cost confirmation before invoking Deep Research Max ($3-7/task).
allowed-tools: Bash, Read, Edit, AskUserQuestion
---

# Gemini Deep Research

Paid, web-grounded research via Google's Gemini Deep Research and Deep Research Max APIs. Use this skill when citation quality, recency (post-2025), and comprehensive cross-referencing matter more than cost. For $0 alternatives, see the alternatives table below.

See [`decision-table.md`](decision-table.md) for the full routing reference with worked examples and cost-cap escape paths.

---

## 1. When to Use This Skill vs. the Alternatives

| Question shape | Tool | Cost | Wall time |
|---|---|---|---|
| "What's hot on Reddit / X / TikTok about X this week?" | `last30days` | $0 (or SC API) | 2–8 min |
| "What are the practical differences between A and B?" with general web coverage | `deep-research-queue` (LDR) | $0 | 5–12 min overnight |
| "Recent (post-2025), authoritative, ≥10 sources, citation quality matters" | **`gemini-deep-research` DR tier** | $1–3 | 5–20 min |
| "Cross-service matrix / due-diligence / comprehensive landscape" | **`gemini-deep-research` DR Max tier** | $3–7 | 20–60 min |

**Quick routing heuristic:**
- Social-media conversation, trends, Reddit/X → `last30days`
- General synthesis at $0, can wait overnight → `deep-research-queue`
- Authoritative citations, recent web coverage, need it now → DR tier
- Multi-service matrix, due-diligence depth, 60-min window OK → DR Max tier

---

## 2. Tier Picker

Once the question maps to this skill, select the tier before invoking:

### DR tier (default)
- **Predicted cost:** ~$2 (range $1–3)
- **Wall time:** 5–20 min
- **Auto-proceed:** Yes, if `[gemini.budget].monthly_cap_usd` headroom > $5 remaining for the month.
- **Confirmation:** Not required for DR tier — proceed directly to invocation.

### DR Max tier
- **Predicted cost:** ~$5 (range $3–7)
- **Wall time:** 20–60 min
- **Confirmation:** MANDATORY `AskUserQuestion` before every DR Max call. Show:
  - Predicted cost + range
  - Estimated wall time
  - Month-to-date Gemini spend (read from `vault/health/gemini-spend-{YYYY-MM}.json`)

**DR Max confirmation prompt template:**

```
Run Deep Research Max for ~$5 (range $3–7, ~30 min)?
Month-to-date Gemini spend: $X of $20 cap.
Options:
- "Yes, run DR Max" — proceed
- "Run standard DR instead ($1–3, 5–20 min)" — downgrade to DR tier
- "Queue to local deep-research-queue ($0, overnight)" — defer to LDR
- "Cancel" — stop
```

Read the ledger before showing this prompt:
```bash
cat vault/health/gemini-spend-$(date +%Y-%m).json 2>/dev/null || echo '{"month_usd": 0}'
```

---

## 3. How to Invoke

After tier selection (and DR Max confirmation if required), invoke the helper:

```bash
# DR tier
agents-sdk/.venv/bin/python3 agents-sdk/scripts/gemini_dr.py \
  --query "<refined question>" \
  --tier dr \
  --no-confirm

# DR Max tier (--no-confirm is REQUIRED — the skill's AskUserQuestion IS the confirmation)
agents-sdk/.venv/bin/python3 agents-sdk/scripts/gemini_dr.py \
  --query "<refined question>" \
  --tier max \
  --no-confirm
```

**Notes:**
- `--no-confirm` is REQUIRED for DR Max. The helper refuses DR Max without it; the skill's `AskUserQuestion` above provides the human confirmation gate.
- For DR tier, `--no-confirm` is optional but encouraged for consistency.
- **Refine the question** before passing it to `--query`. Apply the same specificity rules as `deep-research-queue`: specific, falsifiable, time-scoped where relevant, citation-friendly.
- Run from the repo root (`/Users/seanwinslow/Code-Brain/code-brain/`).

The helper handles: Gemini API polling, ledger update, vault landing, daily-note digest injection.

---

## 4. What Happens After

The helper writes the report to:
```
vault/20_projects/research/{YYYY-MM-DD}-{slug}.md
```

Report frontmatter includes:
```yaml
source: gemini-deep-research        # or gemini-deep-research-max for DR Max
tier: dr                            # or max
cost_usd: 2.14                      # actual cost from Gemini API response
```

The helper also injects a one-line digest under `<!-- research-digest -->` in today's daily note, matching the same injection point used by the `deep_researcher` agent.

After the run completes, surface the report path and estimated cost to Sean.

---

## 5. Cost-Cap Behavior

The helper enforces two caps from `agents-sdk/config.toml` under `[gemini.budget]`:
- `monthly_cap_usd` (default: $20) — cumulative spend this calendar month
- `daily_cap_usd` (default: $10) — spend so far today

**If either cap is hit, the helper REFUSES the call and exits non-zero.** When this happens:

1. Surface the refusal message from the helper's stderr.
2. Offer alternatives:
   - Queue to `deep-research-queue` (LDR, $0, overnight): "I can add this to the local research queue instead — it'll run tonight at 02:45 at $0."
   - Raise the cap: "Or ask me to raise `[gemini.budget].monthly_cap_usd` in `agents-sdk/config.toml`."
   - Wait: "Or we wait until next month's cap resets."

Read the current ledger to show Sean how much headroom remains before even attempting the call:
```bash
Read vault/health/gemini-spend-$(date +%Y-%m).json
```

---

## 6. Refusal Cases

This skill MUST decline (return without invoking the helper) when:

| Condition | Response |
|---|---|
| Single-fact lookup (one answer, no synthesis needed) | "That's a single-fact lookup — I can answer in-session or use WebSearch directly. Gemini DR would be overkill. Want me to just answer it?" |
| Social-media trends, Reddit/X conversation, "what are people saying about X" | "This is a social-trend question — `last30days` is the right tool. It covers Reddit, X, YouTube with engagement data. Want me to run that instead?" |
| Cost cap hit and user declines to raise it | Queue to `deep-research-queue` or stop, per user choice. |
| User declines DR Max confirmation | "Got it — no DR Max run. Want me to use standard DR (~$2) or queue to the local research queue ($0) instead?" |
| Question is answerable by the local LDR + Qwen3-14B path | "The local deep-research-queue can likely handle this at $0 overnight. Want me to queue it instead of spending $1-3 on Gemini DR?" |

---

## 7. Allowed Tools Rationale

- `Bash` — invoke `gemini_dr.py`, read the spend ledger, check today's date.
- `Read` — inspect `vault/health/gemini-spend-{YYYY-MM}.json` (ledger) and `vault/00_inbox/research-queue.md` (to check for duplicates or to compare scope).
- `Edit` — append to `vault/00_inbox/gemini-research-queue.md` if Sean asks to queue a DR question for later rather than run now (same `- [ ] {question}` format as `deep-research-queue`, but in the Gemini-specific queue file).
- `AskUserQuestion` — DR Max cost confirmation gate. Required before every DR Max invocation.

---

## 8. Related

- `deep-research-queue` — sibling skill for $0 local LDR queue (Qwen3-14B on Mac Mini, overnight).
- `last30days` — sibling skill for social-trend and Reddit/X/YouTube research.
- `agents-sdk/scripts/gemini_dr.py` — the actual runner (handles Gemini API, polling, ledger, vault landing).
- `vault/health/gemini-spend-{YYYY-MM}.json` — month-keyed spend ledger. Read before every DR Max confirmation prompt.
- `decision-table.md` — standalone routing reference with worked examples and cost-cap escape paths.
