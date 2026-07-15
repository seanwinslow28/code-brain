# Context Map

code-brain is a multi-context repo. Per-context `CONTEXT.md` files are created
lazily by `/domain-modeling` when terms actually get resolved — absence is normal,
not an error. Consumer rules live in `docs/agents/domain.md`.

| Context | Root | CONTEXT.md |
|---|---|---|
| Agents SDK (fleet, routing, manifests, launchd schedules) | `agents-sdk/` | `agents-sdk/CONTEXT.md` |
| Creative Studio (Phaser, Remotion, pixel art, design team) | `creative-studio/` | `creative-studio/CONTEXT.md` |
| Life Systems (finance, health, learning, time) | `life-systems/` | `life-systems/CONTEXT.md` |
| LLM Council & Discovery (council, fusion-discovery, budgets) | `tools/llm-council/` | `tools/llm-council/CONTEXT.md` |
| Vault & knowledge loop (PARA, synthesizer, critic, lint) | `vault/` | `vault/CONTEXT.md` |

System-wide ADRs: `docs/adr/`. Context-scoped ADRs: `<context>/docs/adr/`.
