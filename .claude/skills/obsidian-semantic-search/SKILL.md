---
name: obsidian-semantic-search
description: Semantic search and embeddings setup for Obsidian vaults. Configure local vector databases, embedding models, and hybrid search pipelines. Use when setting up semantic search, configuring embeddings, building a RAG pipeline, finding related notes by meaning, or choosing between local and cloud embedding options.
---

# Semantic Search and Embeddings

## Purpose

Set up and operate semantic search in an Obsidian vault. Configure embedding models, vector databases, and hybrid search pipelines that find notes by meaning rather than exact keywords. Prioritize local, privacy-preserving solutions.

## When to Use

- Setting up semantic search for the first time
- Choosing between local and cloud embedding options
- Building a custom RAG pipeline with sqlite-vec
- Finding notes related by concept rather than keyword
- Optimizing embedding update strategies for growing vaults

## Examples

**Example 1: Beginner semantic search**
```
User: "Set up semantic search in my vault"
Claude: [Uses obsidian-semantic-search] Recommends Smart Connections
plugin as zero-config starting point. Walks through install, model
selection (BGE-micro-v2 for local), and first semantic query.
```

**Example 2: Custom RAG pipeline**
```
User: "Build a local RAG pipeline for my vault"
Claude: [Uses obsidian-semantic-search] Sets up Ollama with
nomic-embed-text, creates sqlite-vec database, indexes vault notes
with chunking, and implements semantic search function.
```

## Setup Phases

### Phase 1: Zero-Config Plugin (Recommended Start)

Install Smart Connections from Obsidian Community Plugins.

1. Settings > Smart Connections > Smart Environment
2. Select Embedding Model: `BGE-micro-v2` or `nomic-embed-text` (runs locally via transformers.js)
3. Embeddings store in hidden `.smart-env` folder as JSON
4. Open the "Connections" pane to see related notes instantly

Privacy: all data stays on-device. No API keys required.

### Phase 2: MCP Integration for Claude Access

Connect Smart Connections embeddings to Claude via MCP:

```json
{
  "mcpServers": {
    "obsidian-smart": {
      "command": "python",
      "args": ["/path/to/smart-connections-mcp/server.py"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/Users/username/Documents/MyVault"
      }
    }
  }
}
```

Reuses existing Smart Connections embeddings. No double-indexing cost.

### Phase 3: Custom Local RAG Pipeline

For full control, build a pipeline with sqlite-vec and Ollama.

Prerequisites:
- Ollama running locally (`ollama serve`) with `nomic-embed-text` model
- Python with `sqlite-vec` and `ollama` packages

```python
import sqlite3
import struct
import ollama
import os

# Configuration
DB_NAME = "obsidian_vec.db"
EMBEDDING_MODEL = "nomic-embed-text"
DIMENSION = 768  # nomic-embed-text output dimension

def serialize_f32(vector: list[float]) -> bytes:
    """Serialize float vector to bytes for sqlite-vec."""
    return struct.pack(f"{len(vector)}f", *vector)

def setup_db() -> sqlite3.Connection:
    """Initialize SQLite with vector support."""
    conn = sqlite3.connect(DB_NAME)
    conn.enable_load_extension(True)
    # Load sqlite-vec extension
    conn.execute(f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_notes USING vec0(
            path TEXT,
            content TEXT,
            embedding FLOAT[{DIMENSION}]
        )
    """)
    return conn

def embed_and_index(conn: sqlite3.Connection, vault_path: str) -> None:
    """Read MD files, generate embeddings, store in DB."""
    for root, _, files in os.walk(vault_path):
        for file in files:
            if not file.endswith(".md"):
                continue
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # Header-based chunking (better than fixed-size)
            chunks = content.split("\n## ")
            for chunk in chunks:
                if not chunk.strip():
                    continue
                response = ollama.embeddings(
                    model=EMBEDDING_MODEL, prompt=chunk
                )
                conn.execute(
                    "INSERT INTO vec_notes(path, content, embedding) "
                    "VALUES (?, ?, ?)",
                    [path, chunk, serialize_f32(response["embedding"])]
                )
    conn.commit()

def semantic_search(
    conn: sqlite3.Connection, query: str, top_k: int = 5
) -> list:
    """Query the vector database for similar content."""
    query_vec = ollama.embeddings(
        model=EMBEDDING_MODEL, prompt=query
    )["embedding"]
    cursor = conn.execute(
        """
        SELECT rowid, distance, path, content
        FROM vec_notes
        WHERE embedding MATCH ?
        AND k = ?
        ORDER BY distance
        """,
        [serialize_f32(query_vec), top_k]
    )
    return cursor.fetchall()
```

## Hybrid Search Pattern

Pure semantic search can miss specific terminology. Combine keyword (BM25) and vector search for best results.

| Query Type | Strategy | Weight |
| :--- | :--- | :--- |
| Specific terms ("JWT auth error") | Keyword-heavy | 70% keyword, 30% vector |
| Conceptual ("notes about productivity") | Vector-heavy | 30% keyword, 70% vector |
| Exploratory ("related to this note") | Vector-only | 100% vector |

Implementation: run keyword grep first for candidate notes, then re-rank by vector similarity.

## Chunking Strategies

| Strategy | When to Use | Implementation |
| :--- | :--- | :--- |
| Header-based | Well-structured notes | Split on `#` / `##` markers |
| Sentence with overlap | Dense prose notes | 300 tokens, 80 token overlap |
| Whole-note | Atomic notes (<500 words) | Embed entire note as one vector |

Header-based chunking preserves semantic groups and works best with Obsidian's heading structure.

## Local Embedding Model Comparison

| Model | Dimensions | Size | Best For |
| :--- | :--- | :--- | :--- |
| `nomic-embed-text` | 768 | ~275MB | Best quality/size tradeoff |
| `BGE-micro-v2` | 384 | ~24MB | Fast, low resource |
| `BGE-M3` | 1024 | ~570MB | Multilingual support |
| `mxbai-embed-large` | 1024 | ~670MB | Highest quality local |

Recommend `nomic-embed-text` for most users. Beats OpenAI `text-embedding-ada-002` on several benchmarks while running fully local.

## Cloud vs Local Tradeoffs

| Factor | Local (Ollama / sqlite-vec) | Cloud (OpenAI / Pinecone) |
| :--- | :--- | :--- |
| Privacy | High: data never leaves device | Low: notes sent to API |
| Cost | Free (uses CPU/RAM) | Paid per token |
| Setup | Complex: requires CLI/Python | Easy: API key plug-and-play |
| Scale | Good for <50k notes | Massive: billions of vectors |
| Latency | Fast: zero network latency | Variable: API dependent |

Recommend local for personal vaults. Cloud only for team/enterprise scale.

## Embedding Update Strategies

As the vault grows, avoid re-indexing everything on every change.

1. **Hash-based incremental sync**: Hash each note (MD5). Only re-embed notes where hash changed
2. **Idle processing**: Wait for 60 seconds of user inactivity before processing the modified files queue
3. **Startup indexing**: Scan for new/modified files only at Obsidian launch
4. **Separate vector store**: Keep `.smart-env` or `vec_notes.db` outside of iCloud/Git sync to prevent binary file conflicts

## Success Criteria

- [ ] Semantic search returns conceptually related notes (not just keyword matches)
- [ ] Embedding model runs locally without API keys
- [ ] Vector index updates incrementally (not full re-index)
- [ ] Search results include file path and content snippet
- [ ] Privacy requirement met (no data leaves device)

## Copy/Paste Ready

```
"Set up semantic search in my Obsidian vault"
"Find notes related to this concept"
"Build a local RAG pipeline with sqlite-vec"
"Which embedding model should I use?"
"Compare local vs cloud embeddings for my vault"
```
