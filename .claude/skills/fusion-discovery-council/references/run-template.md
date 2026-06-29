# Run template — fusion-discovery-council single-session flow (agent-driven BACKFILL)

Copy the fenced block into a **Claude Code session opened in `code-brain`**, fill the
`<PLACEHOLDERS>`, and run. This is the canonical standard run as of the 2026-06-28 agent-layer
pivot: the council CLI is the paid part; **BACKFILL is done by the agent** with its own
`WebSearch`/`WebFetch` on the Anthropic subscription ($0), which vets relevance natively. The old
`--supplement` (in-CLI Exa/Brave) path is opt-in/headless only — leave it off here.

Set the tier per topic (`quick` $0.50 / `standard` $1.50 / `deep` $4.00). Use `--lens substack`
for post angles (writes a sibling brief) or `--lens pm` for opportunity cards. One topic per RUN
block — add or remove blocks as needed.

---

```
TASK: Run fusion-discovery-council on the topic(s) below, then agent-backfill each ledger's
blind-spot map with your own web tools and verify the result. One paid CLI run per topic; the
backfill is $0 (your subscription).

READ FIRST:
- .claude/skills/fusion-discovery-council/SKILL.md — the skill contract. Pay attention to §0
  (paths), §3 (flags — --supplement is OFF by default and stays off here), §4 + §4.1 (the exact
  CLI invocation AND the single-session agent-driven flow), §5 (cost discipline + the $10/day cap),
  §6 (the verification gate — relevance is yours to judge, verbatim-ness is the backstop's),
  §7 (NEVER git add/commit the vault).

STEP 1 — RUN THE COUNCIL CLI (paid). One at a time, from the CLI working dir. Capture each printed
"Verified ideas: N · dropped: M · $X.XX" line and keep a running daily total. If any run prints
"Budget rejected", STOP, report what completed, and do NOT pass --force or raise tiers — resume
tomorrow (the $10/day cap is checked against ACTUAL spend; it's the real guardrail).

  cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council

RUN 1 — <SHORT LABEL>:
  uv run python -m council.discovery \
    "<TOPIC — a specific audience + their pain, in plain words>" \
    --lens <pm|substack> --tier <quick|standard|deep> \
    --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/research/<YYYY-MM-DD>-<topic-slug>-<lens>-idea-ledger.md

  # (deep tier pauses for an interactive cost confirm; add --yes ONLY if Sean pre-authorized it)
  # (add more RUN blocks for more topics)

STEP 2 — AGENT BACKFILL (the dogfood; $0). For EACH ledger written above:
  a. Open it and read the "## Blind-spot / Whitespace Map" section.
  b. For each gap bullet, WebSearch the SOLUTION/EVIDENCE side of the gap (what would fill it —
     not a complaint query), WebFetch the most promising results, and pull a VERBATIM quote that
     genuinely addresses the gap. YOU are the relevance filter: keep a quote only if it actually
     speaks to the gap, not just shares keywords.
  c. Append a "## Web Supplement (gap-fill)" section to the ledger. Lead with this caveat line:
       > Gap-fill **LEADS** from a solution-side web search of the blind-spot map — verbatim quotes
       > at real URLs, relevance agent-vetted; NOT FUSE-consensus claims. Treat as leads.
     Then one "### <gap>" subsection per gap, each finding on its own line:
       - "<verbatim quote>" — <URL>
     A gap you cannot honestly fill is:
       - still open — not filled
     NEVER fabricate or paraphrase a quote into looking sourced — that breaks the §6 gate.

STEP 3 — VERIFY (the backstop). For EACH ledger, prove every quote is verbatim at its URL:
  cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && \
    uv run python -m council.discovery.verify_supplement <LEDGER ABSOLUTE PATH>
  Exit 0 = clean. Exit 1 = at least one quote isn't verbatim — DEMOTE each flagged item to
  "still open — not filled" and re-run until exit 0.

=== REPORT BACK (one compact table) ===
Columns: Topic | Verified ideas | Dropped | Cost | Gaps filled/total | verify_supplement (clean?)
         | Highest-signal pain point (1 line) | Sharpest blind-spot line (next-topic fuel)
Then: total spend vs the $10/day cap.

=== DO NOT ===
- git add / git commit anything under vault/ — Obsidian-Git owns vault commits (CLAUDE.md rule 8).
  Just write the ledgers (+ briefs) and stop.
- pass --supplement (the agent IS the backfill here), --force, or retry a budget-rejected run.
- run image generation or any unrelated work.
```

---

## After it finishes

You'll have one ledger per topic (+ a brief each for `--lens substack`), each with an
agent-backfilled, backstop-verified `## Web Supplement (gap-fill)` section. From there: fold the
strongest verified pain into wherever this topic's work lives (e.g. a project command center or the
PM opportunity backlog).
