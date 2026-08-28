# Kickoff — eng-002: from knowledge loop to workforce (Systemcraft engagement 2)

Paste everything below the line into a fresh session.

---

Two steps, in order. Step 1 gathers the vision input; step 2 runs the engagement.

**Step 1 — watch the source.** Invoke `/watch` on https://youtu.be/EzQAgnjTq2k?si=o4GhGTtfyVnrGOaZ (Greg Isenberg with Allie K. Miller). I want a working extraction of her "workforce" agent-team concept: how she structures the team, what makes her agents *proactive* rather than reactive, how they map to her goals, how they self-improve, and every concrete golden nugget worth stealing. Capture the extraction as notes the engagement can cite (a file under `vault/20_projects/research/`, dated, `fetched:`-stamped). If /watch cannot process the video, say so plainly and fall back to transcript retrieval — never summarize a video you couldn't actually read.

**Step 2 — engage the studio.** Invoke `/systemcraft`. This is **eng-002**, and I want it typed at Open as what it really is: a **redesign** of my agents-sdk fleet — not a patch pass on the old one. Full train if the type calls for it; the skill routes.

**The brief, in my words:** the current fleet is stale and mostly valueless to me. Outside the vault critic, it spends its nights keeping itself clean — and eng-001 proved it doesn't even do that reliably. It burns huge context to hand me stale job-hunt info. I haven't materially updated it in a couple of months, which in AI terms means it's lightyears behind. I want to redesign it into a **proactive workforce team**: agents mapped to my actual goals (job hunt, Systemcraft, content/creative work, life systems), that bring me things before I ask, that measure their own usefulness, and that self-improve — informed by what Allie K. Miller describes and by what eng-001 measured.

**Binding inputs the engagement must pull (all local):**
- The eng-001 ledger — `systemcraft/ledger/index.md` for the two-hop read, then the entries. Non-negotiable anchors: **d01** (no standing success definition), **d02** (the activity-over-value metric), **d03** (consumption is the gate — near-zero measured use), **d40–d42** (detection-without-delivery, no runbook, attention as the real cost), and the Ops value test (only the indexer cleanly survives; the synthesizer would not).
- The Design Strategist's audit artifact (`systemcraft/ledger/engagements/eng-001-fleet-knowledge-loop-audit/artifacts/audit-design-strategy.md`) — its **six drafted evaluable success criteria** are the PRD section's starting material, not a blank page.
- The Step-1 extraction of Allie K. Miller's workforce model.
- The fleet's current reality: agent inventory + incident history in `CLAUDE.md`; live state readable over read-only SSH (`ssh -o BatchMode=yes seanwinslow@seans-mac-mini.local`).

**Standing constraints (unchanged):** I'm a PM, not a dev — plain language, one question at a time, a recommendation with every question. Public repo — corpus/ledger/private layers never reach git. The 8 agents disabled in April stay disabled unless the redesign explicitly re-justifies one on the record. Draft-then-ratify before any commit; push is my call. Fresh evidence beats stale memory — if the design needs current agent-fleet patterns beyond the video, `/last30days` and the research lanes are available and cheap.

**Also on the table, the engagement decides where they land:** the four small eng-001 P0 fixes still pending (alert delivery via the existing Pushover path, the crying-wolf one-liner, the index-truncation bug, the daily-driver note assertion). Fold them into the redesign or ship them first as a stabilization step — but decide explicitly, don't let them float.

**What done looks like:** a ratified PRD for the workforce fleet with evaluable success criteria co-signed at framing (the dual-touch), the full artifact chain behind it if the routing calls for it, gates passed, ledger entries accreting as eng-002 — and me knowing exactly what gets built first and why A over B, every step.
