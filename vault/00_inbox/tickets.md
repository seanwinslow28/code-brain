---
type: manual-tickets
description: Hand-curated Manual lane for the Agent Fleet Observability kanban board. One ticket per `-` bullet under the appropriate section. See agent-fleet-observability/docs/manual-tickets-schema.md for the parser rules.
---

# Manual tickets

Sean's hand-curated kanban entries. Parser is `lib.readers.read_manual_tickets`
in the agent-fleet-observability repo. Empty sections are fine; the chip will
show 0 until items land here.

## Todo

- Re-add fleet-memory to daily_driver via cheap read-only inject (drop MCP bridge + context-management beta that doubled cost to $0.97 and tripped the cap 5/29); reuse inject_memories_into_prompt() like vault_synthesizer — assigned: Sean
- Build a $0/run local summarizer (gemma4:e4b / qwen3 on Mac Mini) that curates daily_driver's fleet-memory namespace, so the Opus agent only reads, never writes — assigned: Sean
- Wire SDK fleet agents to surface/read open tickets from tickets.md (mirror the interactive session-start-inject-tickets.sh hook) — GATE: only do this once agents have real tasks beyond vault upkeep (e.g. substack-drafter); the current vault-upkeep loop agents don't need it — assigned: Sean
- Build a $0/run local critic-synthesizer (gemma4:e4b / qwen3 on Mac Mini) that reads the nightly critic-manifest-{date}.json after the 03:30 run, ranks+dedupes vault_critic suggestions, and writes a top-N shortlist to a SEPARATE suggestions lane (NOT the hand-curated Manual Todo) for Sean to review and promote — propose-don't-auto-promote, human-in-the-loop — GATE: only build after ~2 weeks of clean vault_critic nightly runs (recent runs show status=partial / ag_fail=5; don't triage noise) — assigned: Sean
- vault-knowledge-mcp launch comms: record the 90-sec Loom from docs/LOOM-SCRIPT.md (all 3 tools, lead on find_contradictions), drop npm + GitHub links into the LinkedIn first-comment, then post docs/LINKEDIN-DRAFT.md tagging Anthropic — assigned: Sean
- vault-knowledge-mcp: log the first recruiter/hiring-manager engagement attributable to this artifact in target-companies.md (spec §8 criterion 9, the last open success criterion) — assigned: Sean
- Task 19 Step 4 / Gate C: record + grade the 3 first-test answers (TMAY / "walk me through what happened with The Block" / "shipped something hard") via mock_interview_loop.py; drill to 8+/10 ×3 consecutive. Also grades the Task 16 stories + Task 17 TMAY — assigned: Sean
- TMAY per-company file: fill a Why-Here swap for each remaining top-5 target before its interview (4 already filled: Anthropic FDE / Sierra / Decagon / ServiceNow) — assigned: Sean
- Task 12 judge layer Steps 8-9 (Sean-host): run the full pytest suite + validate.py per 2026-05-31-task-12-day-6-handoff.md; record the 90-sec --demo-injection Loom; post the LinkedIn draft tagging Anthropic + FDE-Boston JD; commit + tag judge-layer-v0.1.0 (paste-ready CHANGELOG block in the handoff doc) — assigned: Sean
- Task 12 judge layer: add the /transactions/judge-layer ledger row in sw-ai-pm-portfolio (surface: control-plane) — GATE: Gap-Fill 3 personal-site deploy must land first so the page resolves — assigned: Sean
- Task 25 LDR Grounding-Collapse: create the standalone repo from the 5 staged scratchpad files (mkdir ~/Code-Brain/ldr-grounding-collapse, copy README.md + the-failure.md + the-diagnosis.md + the-fix.md + eval-case.yaml, git init, gh repo create --public, push) — the standalone path isn't a mounted folder so it must be created host-side — assigned: Sean
- Task 25 LDR Grounding-Collapse: run writing-voice-modes on substack-drafts/2026-05-29-ldr-grounding-collapse.md, then publish Substack Post 1 (gates Posts 2-3 + the Task 13 manifesto + the Looms); confirm npm run build in sw-ai-pm-portfolio resolves /transactions/ldr-grounding-collapse/; swap the repo URL placeholder → live in both the Substack draft and the ledger row once pushed — assigned: Sean
- meta-agent monitoring blind spot: it reported "all healthy" through the vault_critic Anti-Gravity 5/5 nightly failures (5/26→6/1) because critic status=partial is treated as tolerable. Add an alert when a CLI's failures == calls (100% failure) OR tokens_total==0 with calls>0, even if overall status is partial — so a fully-dead sub-CLI surfaces. Now that the manifest carries antigravity_last_error/codex_last_error, surface that text in the alert — assigned: Sean
- job-feed ATS watchlist decay: 14 company pollers 404 every run (huggingface, beehiiv, framer, scale, glean, tome, spline, fourthwall, draftkings, circle, together-ai, replicate, canva, datarobot) + mistral ReadTimeout + web3career_token missing from Keychain. Audit/refresh the ATS endpoint URLs (greenhouse/lever board tokens likely renamed) and add the web3.career token, or prune dead entries so the err.log stops filling — assigned: Sean
- Task 23 MCP Security Audit (v0.1.1 already published to npm + registry): run npm run build in sw-ai-pm-portfolio to confirm /transactions/mcp-security-audit/ resolves, then commit the new mcp-security-audit.mdx ledger row; post sw-mcp-intent-engineering/docs/LINKEDIN-DRAFT.md (links in first comment, tag Anthropic) and optionally commit that draft file — assigned: Sean
- vault-critic AG hang — read tomorrow's 03:30 capture: check vault/90_system/agent-logs/ag-timeout-*.log + critic-manifest-2026-06-03.json for 429/RESOURCE_EXHAUSTED/Quota/"Request cancelled." If confirmed (high-confidence hypothesis: gemini-cli #22648 swallows a preview-model 429 at the 00:30-Pacific quota-reset boundary), migrate the nightly off oauth-personal to GEMINI_API_KEY (also forced by oauth-personal-via-gemini-cli EOL 2026-06-18), then REMOVE the temporary VAULT_CRITIC_AG_DEBUG=1 from schedules/com.sean.agent.vault-critic.plist + reload. Context: agents-sdk/CONTINUATION-2026-06-02-vault-critic-antigravity.md Session 3 — assigned: Sean
- daily-driver morning cost cap breach: 2026-06-02 run cost $0.6848 vs $0.60 cap (second breach after 5/29 hit $0.97) yet meta-agent reported "healthy". Either raise the cap deliberately or investigate the overrun; also fold cost>cap into the meta-agent alert blind-spot ticket — assigned: Sean
- test suite hang: tests/test_gemini_dr.py makes a real unmocked network call to the Gemini DR API with no timeout, so `pytest tests/` hangs indefinitely (must run per-file or deselect). Mock the API call or mark it integration/skip-by-default so the full suite completes — assigned: Sean
- Task 24 Discovery PRD (content-complete + council-revised; ledger row validated clean via scripts/validate_content.mjs): run `npm run build` in sw-ai-pm-portfolio to confirm /transactions/discovery-prd-content-workflow/ resolves, then commit the new discovery-prd-content-workflow.mdx (surface: product) by hand; optional LinkedIn teaser on the cross-functional-translation angle — assigned: Sean

## In Progress

## Done

- Task 19 mock-interview rig: one-time `agents-sdk/.venv/bin/pip install faster-whisper` on the Mac (only setup left before the rig produces a grade) — assigned: Sean
