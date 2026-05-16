---
name: Agent Fleet Dashboard — Kanban v2 deferred
description: Read-only kanban ships in v1 dashboard; interactive kanban with agent write-back deferred to v2 as its own portfolio artifact
type: project
originSessionId: df31e2c4-dfab-4c15-ac6d-c806d59c5dec
---
Read-only kanban ships in v1 of the Agent Fleet Observability Dashboard (May 2026). Interactive kanban — drag-to-reassign, agents read/write a `tickets.json` source of truth, live status mutation — is deferred to v2. Decision locked 2026-05-15 during brainstorming session.

**Why:**
- v1 budget is 2–3 working days; full interactive would be 1–2 weeks (requires agent runtime changes to know about a task queue)
- Validate the surface first — confirm recruiters / hiring managers respond to the kanban frame before investing in the agent-write-back plumbing
- v2 is more valuable as its own portfolio artifact ("I built Linear-for-AI-agents") than as a v1 feature; could anchor Substack post 3 or 4
- Scope discipline keeps v1 shippable

**v1 surface (in scope):**
- Read-only board at `fleet.seanwinslow.com/kanban` and private equivalent
- 5 columns: Backlog · ToDo · InProgress · Testing · Done
- Tickets composed from existing data: research-queue.md, knowledge_lint findings, eval failures, job-feed (private only), manual `tickets.md`
- Tickets move as agents run (CSV log + manifest reads determine column membership)
- Live-pulsing dot for tickets actually running at snapshot time

**v2 scope (deferred):**
- `tickets.json` (or SQLite table) as source of truth
- Agent runtime gains queue-awareness — picks up assigned tickets, writes status updates back
- Drag-to-reassign UI in the browser
- Possibly websocket or short-poll for near-real-time updates (or just hourly snapshot bumps)
- Dispatch logic: which agents are eligible for which ticket types
- Failure handling: timeouts, retries, ticket reassignment on cap-hit

**How to apply:**
- When Sean returns to dashboard work post-v1-ship, v2 is the next-up project on the roadmap
- Treat as its own portfolio artifact, not a v1.1 patch
- Substack-worthy build narrative: "I gave my AI agents a sprint board and they ship like a team"
- Don't start v2 work until v1 has 1+ real recruiter engagement attributed to it (or 4+ weeks live, whichever comes first) — the validation gate matters
