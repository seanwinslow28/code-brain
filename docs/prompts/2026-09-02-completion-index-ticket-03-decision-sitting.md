# Completion Index — ticket-03 decision sitting (continuation prompt, 2026-09-02)

Paste the block below into a fresh Claude Code session opened in `/Users/seanwinslow/Code-Brain/code-brain`. It holds the four-decision sitting that map ticket 03 owes, using `/grilling`, one question at a time, recommendation first.

```text
/grilling

This is the ticket-03 decision sitting for the completion index (my company, founded 2026-09-01). The design chain is done: Systemcraft engagement eng-004 closed administratively on 2026-09-02 with Gate 2 at DESIGN PASS WITH ACCEPTANCES (signed) and its reconciliation round complete. Four decisions were routed to me and nobody else may make them. Hold the sitting one decision at a time, recommendation first, two or three mutually exclusive choices, the consequence of no answer stated. Do not re-litigate the founding locks L11–L13 or anything the gates already resolved; extend only.

Read first, in this order (all local; the ledger and sidecar are private — never quote them into tracked files or issues):
1. The ticket itself: ~/Code-Brain/completion-index/docs/wayfinder/03-category-panel-framing-and-the-s1-date.md, and the map parent 01-map.md (Notes, Decisions-so-far, Fog).
2. eng-004 Close records: systemcraft/ledger/engagements/eng-004-completion-index-harness-design/close-digest.md (incl. the reconciliation addendum), d12-coord (the frozen P0-EQ denominator), d13-coord and d14-coord.
3. The PRD as ratified: artifacts/prd-completion-index.md — §Category and site panel, §Success definition, §Sean rulings, criteria S1/S4/S6/S11 — and artifacts/prd-appendix-category-panel-options.md (the 12 over-complete candidates, 3 consent-tier candidates). d15 (auto parts recommended, not selected) and d28 (agents compared over anonymized fixtures; named per-site surfaces only with consent).
4. The robots pre-check: COORDINATOR-FINDING-robots-sweep.md + artifacts/robots-sweep-2026-09-01-raw.txt (with its correction marker) — 6 of 9 readable candidates disallow /cart for every agent, 2 answer 403 (bot-hostile), RockAuto blocks ClaudeBot outright.
5. The ops model: artifacts/ops-model-runbook.md — §Proposed superseding S1 date (2027-07-31, recomputed on the 12–18-week build load; break cases 08-17 / 09-17), §Calendar, §Sean attention admission (10.92–11.59 h/month, max rolling week 7.42 h), §Cash (base $155, reservation $180), and d69c (≥38 candidates must enter the first governed sweep at the measured 8/12 yield to retain 25 eligible fixtures). Also d69f (PUBLICATION_DROUGHT) and the Gate-2 round-2 finding that cycle 1 is designed to publish no aggregate (artifacts/red-team-gate2-round2-findings.md, the "consent tier as the v0.1 emission" decision).
6. vault/00_inbox/tickets.md — the two eng-004 tickets (decisions; D+14 record due 2026-09-16).

The four decisions, in this order:
1. Category and panel. Standing recommendation: automotive parts; PC components is the fallback. The appendix's 12 candidates are a paper list from model knowledge; d69c says at least 38 must enter the sweep. Before asking me, expand the candidate list to ≥38 real automotive-parts sites with size/platform diversity (national chains, catalog-first sellers, performance and vehicle specialists, regional/independent sellers), using web search for discovery only. You may run the read-only pre-check on new candidates — one honest GET /robots.txt per domain via ~/Code-Brain/completion-index/scripts/robots_sweep.py — and nothing else touches any site. Then ask me to lock the category and approve the provisional list that goes to ticket 08's full eligibility sweep.
2. Framing. PRD r2–r3 adopted the gate's steel-man: v0.1 compares agent stacks over anonymized site fixtures; no named per-site page or badge without the owner's consent (L11's badge is deferred, not deleted). Recommendation: ratify. Ask me to ratify or reverse, with the consequence that a reversal reopens Gate 1.
3. The S1 date. I already ruled that 2027-03-01 is superseded via L12's own SUPERSEDES mechanism by an Ops-priced date. Ops' reconciled value is 2027-07-31. Recommendation: set it. Ask me to set 2027-07-31, set a different date with a reason, or decline (which leaves S1 at a date the design says it cannot meet). Record my answer as the R-M6 disposition for the D+14 record.
4. The v0.1 emission. Cycle 1 is designed to publish no aggregate (floors, permission, and S1 series rules), so Report #1 is a method-and-controlled-checkout release with the drought counter visible. Recommendation: say so on the site and make that the finish line (map ticket 21 is already reworded). Ask me to confirm or to hold Report #1 until an aggregate exists.

Also record, without asking twice: the R-M1 disposition (judge-quality gates frozen in the ops model — recommend `shipped` on paper) for the D+14 record.

Outputs when the sitting ends (draft, then I ratify each write):
- The ticket's Resolution record in ~/Code-Brain/completion-index/docs/wayfinder/03-…md: the four rulings, dated, with my reason for each, and the approved provisional candidate list (commit the company repo locally; do not create the GitHub repo or push unless I say so in this session).
- A dated `## Sean rulings` addition to the PRD (a record action, not seat substance) and one new coordinator ledger entry d15-coord in the eng-004 folder with the four rulings and the R-M1/R-M6 dispositions; append one index line per the coordinator-only index rule; commit the private ledger repo (systemcraft/ledger is its own git repo — commit only the eng-004 folder and index.md).
- If I set the S1 date: append a dated `[L14] SUPERSEDES [L12] (date only)` line with my verbatim why under LOCKED DECISIONS in ~/.creative-harness/partner-sessions/2026-08-29-agentic-web-startup.md — append-only, never edit an existing lock.
- Update the two eng-004 tickets in vault/00_inbox/tickets.md (decisions answered; D+14 record now needs only the outside-use event).
- Update the standing memory note completion-index-build-state.md.

Rules: I am a PM, not a dev — plain language, define any studio term at first use. Never state an unmeasured number as measured. Public repo: nothing from the ledger or sidecar lands in a tracked file. Verify `git status --porcelain systemcraft/` is empty before you stop. Close with a short recap that stands on its own.
```
