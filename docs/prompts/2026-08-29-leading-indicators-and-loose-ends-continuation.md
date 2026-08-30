# Agentic-Web Sprint — Leading-Indicators Research + Loose-Ends Continuation

Continuation prompt from the 2026-08-29 evening session (historical-patterns funnel +
Odlyzko check). Run in a fresh session. Everything here is **product-agnostic** and
$0-preferred; evidence discipline carries over (tag every number
[independent]/[vendor]/[derived]; cite what you read; absence of data is a finding).

## Context to load first

- Verdict being extended: [vault/20_projects/research/2026-08-29-agentic-rails-odlyzko-check.md](../../vault/20_projects/research/2026-08-29-agentic-rails-odlyzko-check.md)
  (+ its `2026-08-29-agentic-rails-odlyzko-check/` evidence pair).
- Council pre-mortem that motivated it: [vault/20_projects/research/2026-08-29-tech-revolution-patterns-council-premortem.md](../../vault/20_projects/research/2026-08-29-tech-revolution-patterns-council-premortem.md)
  — note the standing rule: the historical work is a **filter on what not to build,
  not a territory warrant**.
- Build-in-public candidate (wayfinder input, do not publish in this session):
  [vault/20_projects/research/2026-08-29-tech-revolution-patterns/build-in-public-candidate-odlyzko-check.md](../../vault/20_projects/research/2026-08-29-tech-revolution-patterns/build-in-public-candidate-odlyzko-check.md)

## Task 1 — Leading-indicators deep pass (the main event)

The verdict names six indicators whose crossing would reopen the rails-timing question.
For EACH, research and document:

1. **The authoritative series**: who publishes it, at what cadence, at what URL/venue,
   and whether it's [independent] or [vendor]. Where tonight's number was
   search-snippet tier, re-verify against a primary source.
2. **Baseline as of 2026-08-29** (from the verdict, re-checked):
   - ACP/Instant-Checkout GMV disclosure: **none in 11 months** (the disclosure event
     itself is the signal).
   - Agentic-GMV line item in any GAAP filing: **none**.
   - x402 organic settlement: ~$10–15M/mo organic of ~$24M nominal; daily settlement
     −93% YTD (Helios Analytics via CryptoPotato; Artemis/Chainalysis for organic
     share). Threshold: sustained >$100M/mo organic.
   - HUMAN Security checkout-touch share of live agentic traffic: 2.3–2.6%
     (Apr–Jul 2026 monthly series). Threshold: >10%.
   - AI-referred share of e-commerce sessions: <0.2–1% [derived]. Threshold: ~2–3%.
     (Adobe publishes growth %, not share — find whether anyone publishes the share
     directly, or document that the share must stay derived.)
   - TollBit / Cloudflare Pay-Per-Use payout disclosure: **none**. (Also track
     Cloudflare's pay-per-answer successor — 2 AI buyers at launch.)
3. **A checking recipe**: the exact $0 steps (URL + what to look for) that a future
   session — or a scheduled agent — can run to re-read each indicator in <10 minutes.
4. **Two indicators the verdict may have missed**: propose candidates with rationale
   (e.g., Stripe/Shopify earnings-call language shifts; HUMAN's series being
   discontinued would itself be a signal; a second Etsy-class integration exit or a
   contradicting success). Sean ratifies additions.

**Deliverable:** `vault/20_projects/research/2026-09-XX-agentic-rails-leading-indicators-tracker.md`
— one section per indicator (series, baseline, threshold, recipe, last-checked date),
designed to be re-run and appended to on a cadence.

**Cadence recommendation, not automation:** close with a recommendation (e.g., monthly
manual re-check at ~30 min, or a candidate fleet-agent design) but **do not wire any
scheduled agent** — automation is a Sean decision per the standing agent-downsizing
rule (8 disabled agents stay disabled; new schedules need explicit approval).

## Task 2 — Tie up the named loose ends

From the 2026-08-29 lit-review ticket (mark it DONE in
[vault/00_inbox/tickets.md](../../vault/00_inbox/tickets.md) when finished):

- **(a) Yegge's "Revenge of the Junior Developer"** — the Sourcegraph original 403s on
  server-side fetch. Use an interactive browser session (Browser pane `navigate`, or
  claude-in-chrome if the pane is also blocked) to read
  `https://sourcegraph.com/blog/revenge-of-the-junior-developer`, extract his
  per-developer token-cost figures verbatim, and append a cited addendum to
  [vault/20_projects/research/2026-08-29-software-factory-lit-delta/sweep-practitioners.md](../../vault/20_projects/research/2026-08-29-software-factory-lit-delta/sweep-practitioners.md)
  (§11). If the browser also fails, record the failure and stop — his numbers stay
  uncited, and any doc that wants them must say so.
- **(b) Two unread exe.dev posts** — "How Antithesis Turned exe into a Sandbox for
  Agentic Software Tests" and "OAuth for Agents" (blog.exe.dev). Read both, append a
  classified entry each (practitioner vs vendor, quotes <25 words, adopt/beware) to
  [sweep-companies.md](../../vault/20_projects/research/2026-08-29-software-factory-lit-delta/sweep-companies.md).
- **(c) notebooklm 52MB tooling lesson** — make it durable in two places:
  1. Add a short "Known limitation on large notebooks" note to code-brain's own
     reference layer (a `claude-mastery/` note or the vault knowledge corpus — NOT the
     `~/.claude/skills/notebooklm/` skill file, which `notebooklm skill install`
     overwrites): `chat.ask` hard-fails with `RPCResponseTooLargeError` at a 52,428,800-byte
     client cap on the 57-source notebook regardless of `-s` scoping; per-source
     `source fulltext` is the reliable path; scoped asks worked at ≤8 sources only when
     the selected sources were small.
  2. **Draft** (do not post) an upstream issue for `teng-lin/notebooklm-py` with the
     repro (CLI version from `notebooklm --version`, error JSON, source count/sizes) and
     leave it at `docs/prompts/drafts/` or in the session summary for Sean's explicit
     approval before anything is posted publicly.
- **(d) No action:** Arize hands-on remains Sean's own optional track. The Sept-1
  sitting ticket (runs A + B, rubric scoring, wave-2 drafts) stands unchanged — do not
  touch its scope from this session.

## Constraints

- $0 spend (WebSearch/WebFetch/browser + subscriptions). No Gemini DR, no council, no
  discovery runs from this prompt.
- No build, no scheduled agents, no publishing. Drafts and trackers only.
- Commit vault/docs work per repo convention; MacBook Pro sessions commit vault/
  themselves (standing memory).
- Wrap-up per CLAUDE.md rule 8: ticket anything surfaced-but-unfinished before ending.
