# Public Vault Fixture (synthetic)

A **fully synthetic** miniature vault used as a portable test bed for tools that operate over a vault layout — most immediately the forthcoming `vault-knowledge-mcp` smoke tests.

## What this is

- **10 concept notes** under [`concepts/`](concepts/), each with frontmatter (`slug`, `title`, `related` wikilinks) and short prose carrying inline `[[wikilinks]]`.
- **15 typed edges** in [`edges.json`](edges.json), spanning **all six** `concept_edges` relation types so the fixture exercises the full schema:

  | relation | count |
  |---|---|
  | `supports` | 4 |
  | `depends_on` | 3 |
  | `related_to` | 4 |
  | `evolved_into` | 1 |
  | `supersedes` | 1 |
  | `contradicts` | 2 |
  | **total** | **15** |

## Why it's synthetic and off-thesis

The topic is **espresso brewing methods** — deliberately chosen to have **zero overlap** with the author's professional work, so there is no risk of leaking private vault content into a public repo. This is the design intent, not an accident: a future contributor should **never** fold real notes into this directory. Keep it synthetic. If you need a bigger fixture, extend it with more espresso (or another off-thesis topic), never with real vault material.

## How to load it

The fixture mirrors a stripped-down `vault/40_knowledge/concepts/` shape (no `20_projects/`, no `health/`, no `90_system/`). To use it as a throwaway test vault:

```bash
cp -r examples/public_vault_fixture/ /tmp/test_vault
# point a vault-aware tool at the copy, e.g. once vault-knowledge-mcp ships:
#   AGENT_VAULT_PATH=/tmp/test_vault python3 -m vault_knowledge_mcp ...
```

`edges.json` is the canonical edge list (it matches the `concept_edges` columns: `from_slug`, `to_slug`, `relation`, `confidence`). A loader can build a SQLite index from it directly, or derive edges from the `related` frontmatter + inline wikilinks for a graph-construction smoke test.

## Smoke tests this fixture should support (once `vault-knowledge-mcp` ships)

- **Schema coverage** — every one of the six relation types is present, so a loader that drops any relation fails loudly.
- **Graph traversal** — e.g. "what supports `espresso-extraction`?" returns `pump-pressure`, `tamping`, `water-chemistry`.
- **Contradiction retrieval** — e.g. "what contradicts `pump-pressure`?" returns `water-chemistry`, exercising the verb most knowledge tools can't represent.
- **Wikilink ↔ edge consistency** — every `from_slug`/`to_slug` in `edges.json` resolves to a note file in `concepts/`.
