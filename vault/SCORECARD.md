---
artifact: vault-scorecard
created: 2026-05-29
last_telemetry: 2026-05-29
ai-context: "Nate Jones's 5-test scoreboard for agent infrastructure, scored across four knowledge systems with Sean's vault telemetry verbatim. Companion long-form essay at docs/VAULT_AS_AGENT_INFRASTRUCTURE.md. Telemetry regenerable via scripts/generate_schema.py."
---

# Vault Scorecard

> Five tests. Four knowledge systems. Three passes, two failures. The failures are the latest blueprints.

Most people treat Obsidian as a place to put things they swear they'll reread and never do. I was most people. Now I treat my vault as agent infrastructure — the substrate a fleet of agents reads, writes, and argues with while I sleep. Nate Jones published five structural tests for what actually counts as agent infrastructure in 2026: durable, named, ownable, permissioned, auditable. This scores my vault against them, next to Notion, default Obsidian, and Linear. Every number below is pulled live from `vault/.vault-index.db`, regenerable with `scripts/generate_schema.py`.

## (a) Persistent State

**Diagnostic:** Does the system survive a process crash, machine restart, or session boundary with state intact?

**Sean's vault:** Pass, above Linear — Three independent persistence substrates: (1) markdown files on disk (every concept, every connection, every note), (2) SQLite `concept_edges` table with 632 typed edges and 15,582 indexed chunks (`vault/.vault-index.db`), (3) JSONL session-end flush dumps via `flush.py`. Survives crash, restart, session boundary, machine swap. Code: [agents-sdk/agents/knowledge_loop/EXPLANATION.md](../agents-sdk/agents/knowledge_loop/EXPLANATION.md).

## (b) Defined Verbs

**Diagnostic:** Are the legal operations on the system explicitly named, ideally enforced?

**Sean's vault:** Pass, above Linear — Six relation verbs enforced at the database level via a `CHECK (relation IN (...))` constraint: `supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`. No rogue verbs admitted. Verb distribution as of 2026-05-29: `depends_on: 215 · related_to: 199 · supports: 160 · contradicts: 38 · evolved_into: 13 · supersedes: 7`. Code: [agents-sdk/lib/concept_edges/EXPLANATION.md](../agents-sdk/lib/concept_edges/EXPLANATION.md).

## (c) Ownership

**Diagnostic:** Who owns each record, and is that ownership machine-readable?

**Sean's vault:** Partial — Files on disk, git history (committer identity), and a frontmatter `author` field where present. **No per-record assignee/watcher model.** This is the first of the two honest losses to Linear.

> **HONEST NOTE — Linear wins here.** Its assignee, creator, and watchers model is semantic and queryable in ways a folder of files will never be, and I'm not going to dress that up. Naming the gap is the whole reason `vault-knowledge-mcp` exists — it ships ownership as a typed edge (`created_by`, concept → person), the first real step onto the axis where Linear currently beats me.

## (d) Permissions

**Diagnostic:** Can the system grant or deny access per-record, per-role?

**Sean's vault:** Partial — Filesystem-level only (POSIX read/write, git remotes). No per-record RBAC. **The second honest loss to Linear.**

> **HONEST NOTE — Linear wins here too.** RBAC, team scopes, project access — Linear was built multi-tenant, the vault was built single-player, and on permissions that difference is decisive. But the closer is already on disk, not on a someday list: the Judge Layer — a control-plane interceptor between an agent's intent (`ActionProposal`) and its action, gated by declarative policy, every decision written to an append-only ledger. It turns "the agent wrote a thing" into "the agent proposed a thing, and the control plane checked it against a policy before it took effect." I won't pretend that's full RBAC yet. It's the primitive underneath it. The rest is rollout — across the fleet, then per-agent policy into per-record scopes.

## (e) Queryable Audit History

**Diagnostic:** Can a third party reconstruct what changed, when, and why, without the human's narration?

**Sean's vault:** Pass, above Linear — Three independent audit substrates:
- **`git log`** — semantic commit messages, the v3.X.X versioning, every vault auto-commit dated
- **`concept_edges` SQLite** — every edge tagged with `source_synth_run`, `created_at`, `classifier_version`, and where deprecated, `valid_until`. 8 edges currently bear `valid_until` timestamps — real-time graph curation, not a write-once log.
- **`vault/health/*-manifest-*.json`** — per-run synthesizer manifests with `concepts_written`, `clusters_sampled`, `rejected_reasons{}`, `skipped_thin_source`, `model_used`
- **`vault/.../daily-log.md`** — session-end flush dumps with `trigger:` tags

A third party can answer "what changed on 2026-05-12 around the LDR contradiction?" by querying `WHERE created_at > '2026-05-12' AND relation = 'contradicts'`. The graph answers itself — it returns `('local-deep-research-ldr', 'gemini-deep-research', 'contradicts', confidence=0.8, created_at='2026-05-12T16:52:36')`, the actual edge the synthesizer wrote the day that pattern landed.

## Closing scoreboard

| | Persistent State | Defined Verbs | Ownership | Permissions | Audit |
|---|---|---|---|---|---|
| Notion | ❌ | ❌ | ✅ | ✅ | ⚠️ |
| default Obsidian | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |
| Linear | ✅ | ✅ | ✅✅ | ✅✅ | ✅ |
| Sean's vault | ✅✅ | ✅✅ | ⚠️ | ⚠️ | ✅✅ |

Three passes, two failures. One closer is already built — the Judge Layer, in rollout now against the permissions gap. The other, `vault-knowledge-mcp`, is next up against ownership. The failures aren't shortcomings to apologize for. They're the blueprints I'm building from.
