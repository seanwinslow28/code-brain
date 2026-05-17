#!/usr/bin/env python3
"""Vault Embedding Indexer Agent — semantic search index for vault notes.

Runs on Mac Mini (192.168.68.200), 100% local via nomic-embed-text.
Indexes all vault markdown notes into a SQLite vector store.
Incremental: only re-indexes files that changed since last run.

Usage:
    python3 agents/vault_indexer.py
    python3 agents/vault_indexer.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sqlite3
import struct
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.logging_setup import record_run, setup_logger

AGENT_NAME = "vault-indexer"

# Safety limits — $0.00 budget (100% local, no API cost)
MAX_TURNS = 20
MAX_BUDGET_USD = 0.00

# Embedding config
OLLAMA_HOST = "192.168.68.200"
OLLAMA_PORT = 11434
EMBEDDING_MODEL = "nomic-embed-text"
CHUNK_SIZE = 500  # tokens (~2000 chars)
CHUNK_OVERLAP = 50  # tokens (~200 chars)
CHARS_PER_TOKEN = 4  # rough approximation

# D.2.a hash-state: vault-relative file path → {hash: sha256, indexed_at: iso}
INDEXER_STATE_FILENAME = ".indexer-state.json"


def get_db_path(vault_root: Path) -> Path:
    """Return path to the SQLite vector store."""
    return vault_root / ".vault-index.db"


def init_db(db_path: Path) -> sqlite3.Connection:
    """Initialize the SQLite database with the embedding schema."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            embedding BLOB,
            file_mtime REAL NOT NULL,
            indexed_at TEXT NOT NULL,
            UNIQUE(file_path, chunk_index)
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_file_path
        ON chunks(file_path)
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS index_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    # Phase D (v3.20.0, 2026-05-01) — typed reasoning edges. Side-effect
    # write target for vault_synthesizer; queryable read target for
    # knowledge_lint Tier 2 contradiction detection.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS concept_edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_slug TEXT NOT NULL,
            to_slug TEXT NOT NULL,
            relation TEXT NOT NULL CHECK (relation IN (
                'supports','contradicts','evolved_into','supersedes','depends_on','related_to'
            )),
            confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
            valid_until TEXT,
            classifier_version TEXT,
            source_synth_run TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(from_slug, to_slug, relation),
            CHECK (from_slug != to_slug)
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_concept_edges_relation
        ON concept_edges(relation)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_concept_edges_from
        ON concept_edges(from_slug, relation)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_concept_edges_current
        ON concept_edges(from_slug, to_slug)
        WHERE valid_until IS NULL
    """)
    conn.commit()
    return conn


def get_indexed_mtimes(conn: sqlite3.Connection) -> dict[str, float]:
    """Get the last-indexed mtime for each file."""
    cursor = conn.execute(
        "SELECT DISTINCT file_path, MAX(file_mtime) FROM chunks GROUP BY file_path"
    )
    return {row[0]: row[1] for row in cursor.fetchall()}


def discover_vault_files(vault_root: Path) -> list[Path]:
    """Find all markdown files in the vault, excluding system dirs.

    Phase 6 D.2.a: `daily/` is excluded from the embed index — daily logs
    feed synthesis, not search. Concept/connection articles under
    `knowledge/` ARE indexed (they are synthesis output, so a late-night
    synthesizer can retrieve yesterday's concepts for tonight's run).
    """
    exclude_dirs = {
        ".obsidian",
        ".trash",
        ".vault-index.db",
        "90_system",
        "node_modules",
        "daily",       # D.2.a — Phase 6 SOT line 482
    }
    files = []
    for md_file in vault_root.rglob("*.md"):
        parts = md_file.relative_to(vault_root).parts
        if any(part in exclude_dirs or part.startswith(".") for part in parts):
            continue
        files.append(md_file)
    return sorted(files)


# ─── D.2.a hash-state tracking ──────────────────────────────────────────

def compute_file_hash(path: Path, chunk: int = 65536) -> str:
    """SHA-256 hex digest of a file's contents."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def read_indexer_state(state_path: Path) -> dict[str, dict[str, str]]:
    """Load the indexer-state JSON. Missing/corrupt → empty dict."""
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return {}


def write_indexer_state(state_path: Path, state: dict[str, dict[str, str]]) -> None:
    """Write indexer-state JSON atomically."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = state_path.with_suffix(state_path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(state_path)


def detect_changed_files(
    vault_root: Path,
    prior_state: dict[str, dict[str, str]],
) -> tuple[list[Path], dict[str, dict[str, str]]]:
    """Walk the vault, return (changed_files, new_state).

    A file is "changed" iff its SHA-256 differs from `prior_state[rel]["hash"]`,
    OR the file is not in `prior_state`. Deleted files are removed from the
    returned state. Previously unchanged files retain their prior `indexed_at`.

    `changed_files` is a list of absolute Paths; `new_state` keys are
    POSIX-style vault-relative paths.
    """
    now_iso = datetime.now().isoformat(timespec="seconds")
    new_state: dict[str, dict[str, str]] = {}
    changed: list[Path] = []

    for fp in discover_vault_files(vault_root):
        rel = fp.relative_to(vault_root).as_posix()
        h = compute_file_hash(fp)
        prior = prior_state.get(rel)
        if prior and prior.get("hash") == h:
            # unchanged — keep old indexed_at
            new_state[rel] = prior
        else:
            new_state[rel] = {"hash": h, "indexed_at": now_iso}
            changed.append(fp)

    return changed, new_state


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks of approximately chunk_size tokens."""
    char_chunk = chunk_size * CHARS_PER_TOKEN
    char_overlap = overlap * CHARS_PER_TOKEN

    if len(text) <= char_chunk:
        return [text] if text.strip() else []

    chunks = []
    start = 0
    while start < len(text):
        end = start + char_chunk

        # Try to break at a paragraph or sentence boundary
        if end < len(text):
            # Look for paragraph break
            para_break = text.rfind("\n\n", start + char_chunk // 2, end)
            if para_break > start:
                end = para_break + 2
            else:
                # Look for sentence break
                for sep in [". ", ".\n", "! ", "? "]:
                    sent_break = text.rfind(sep, start + char_chunk // 2, end)
                    if sent_break > start:
                        end = sent_break + len(sep)
                        break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - char_overlap
        if start >= len(text):
            break

    return chunks


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter from markdown."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].strip()
    return text


async def get_embedding(text: str, host: str = OLLAMA_HOST, port: int = OLLAMA_PORT) -> list[float]:
    """Get embedding vector from Ollama nomic-embed-text on Mac Mini."""
    import httpx

    url = f"http://{host}:{port}/api/embed"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json={
            "model": EMBEDDING_MODEL,
            "input": text,
        })
        resp.raise_for_status()
        data = resp.json()
        # Ollama returns {"embeddings": [[...]]} for /api/embed
        embeddings = data.get("embeddings", [])
        if embeddings:
            return embeddings[0]
        raise RuntimeError(f"No embedding returned from {EMBEDDING_MODEL}")


def embedding_to_blob(embedding: list[float]) -> bytes:
    """Pack a float list into a compact binary blob."""
    return struct.pack(f"{len(embedding)}f", *embedding)


def blob_to_embedding(blob: bytes) -> list[float]:
    """Unpack a binary blob back to a float list."""
    n = len(blob) // 4
    return list(struct.unpack(f"{n}f", blob))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


async def search(
    query_text: str,
    db_path: Path,
    top_k: int = 5,
    *,
    include_embeddings: bool = False,
) -> list[dict[str, Any]]:
    """Search the vault index for semantically similar chunks.

    Args:
        query_text: The search query.
        db_path: Path to the SQLite database.
        top_k: Number of results to return.
        include_embeddings: When True, each result dict includes the
            stored embedding under key ``embedding`` (list[float]).
            Enables downstream cluster-and-sample retrieval (Tier 2
            retrofit, 2026-05-16) — the synthesizer needs vectors to
            cluster the pool with HDBSCAN. Off by default to keep
            payloads small for callers that only consume text.

    Returns:
        List of dicts with ``file_path``, ``chunk_text``, ``similarity``,
        and (when ``include_embeddings=True``) ``embedding``.
    """
    query_embedding = await get_embedding(query_text)

    conn = sqlite3.connect(str(db_path))
    cursor = conn.execute("SELECT file_path, chunk_text, embedding FROM chunks WHERE embedding IS NOT NULL")

    results = []
    for row in cursor.fetchall():
        file_path, chunk_text_val, blob = row
        if blob:
            stored_embedding = blob_to_embedding(blob)
            sim = cosine_similarity(query_embedding, stored_embedding)
            record: dict[str, Any] = {
                "file_path": file_path,
                "chunk_text": chunk_text_val[:200],
                "similarity": sim,
            }
            if include_embeddings:
                record["embedding"] = stored_embedding
            results.append(record)

    conn.close()
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


async def index_vault(
    vault_root: Path,
    logger: Any,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Run the full indexing pipeline.

    Returns:
        Summary dict with counts of files processed, chunks created, etc.
    """
    db_path = get_db_path(vault_root)
    conn = init_db(db_path)

    # Discover files
    all_files = discover_vault_files(vault_root)
    indexed_mtimes = get_indexed_mtimes(conn)

    # Find files that need (re)indexing
    files_to_index = []
    for f in all_files:
        rel_path = str(f.relative_to(vault_root))
        current_mtime = f.stat().st_mtime
        last_mtime = indexed_mtimes.get(rel_path, 0)
        if current_mtime > last_mtime:
            files_to_index.append((f, rel_path, current_mtime))

    # Find deleted files to remove from index
    current_rel_paths = {str(f.relative_to(vault_root)) for f in all_files}
    deleted_paths = set(indexed_mtimes.keys()) - current_rel_paths

    summary = {
        "total_vault_files": len(all_files),
        "files_needing_index": len(files_to_index),
        "files_already_indexed": len(all_files) - len(files_to_index),
        "files_deleted": len(deleted_paths),
        "chunks_created": 0,
        "embeddings_generated": 0,
        "errors": [],
    }

    logger.info(
        f"Discovered {len(all_files)} vault files, "
        f"{len(files_to_index)} need indexing, "
        f"{len(deleted_paths)} deleted"
    )

    if dry_run:
        logger.info("DRY RUN — would index these files:")
        for f, rel_path, mtime in files_to_index[:20]:
            logger.info(f"  {rel_path} (mtime: {datetime.fromtimestamp(mtime).isoformat()})")
        if len(files_to_index) > 20:
            logger.info(f"  ... and {len(files_to_index) - 20} more")
        conn.close()
        return summary

    # Remove deleted files from index
    for del_path in deleted_paths:
        conn.execute("DELETE FROM chunks WHERE file_path = ?", (del_path,))
        logger.info(f"Removed deleted file from index: {del_path}")
    conn.commit()

    # Index new/modified files
    now = datetime.now().isoformat()
    for file_path, rel_path, mtime in files_to_index:
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
            text = strip_frontmatter(text)

            if not text.strip():
                continue

            # Remove old chunks for this file
            conn.execute("DELETE FROM chunks WHERE file_path = ?", (rel_path,))

            # Chunk and embed
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                try:
                    embedding = await get_embedding(chunk)
                    blob = embedding_to_blob(embedding)
                    summary["embeddings_generated"] += 1
                except Exception as e:
                    logger.warning(f"Embedding failed for {rel_path} chunk {i}: {e}")
                    blob = None

                conn.execute(
                    """INSERT OR REPLACE INTO chunks
                       (file_path, chunk_index, chunk_text, embedding, file_mtime, indexed_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (rel_path, i, chunk, blob, mtime, now),
                )
                summary["chunks_created"] += 1

            conn.commit()
            logger.info(f"Indexed {rel_path}: {len(chunks)} chunks")

        except Exception as e:
            logger.error(f"Failed to index {rel_path}: {e}")
            summary["errors"].append({"file": rel_path, "error": str(e)})

    # Update metadata
    conn.execute(
        "INSERT OR REPLACE INTO index_meta (key, value) VALUES (?, ?)",
        ("last_run", now),
    )
    conn.execute(
        "INSERT OR REPLACE INTO index_meta (key, value) VALUES (?, ?)",
        ("total_chunks", str(summary["chunks_created"])),
    )
    conn.commit()
    conn.close()

    return summary


async def run(dry_run: bool = False) -> None:
    """Run the vault embedding indexer."""
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir, config.log_level)

    agent_cfg = config.agent_config("vault_indexer")
    if not agent_cfg.enabled:
        logger.warning("Vault indexer agent is disabled in config.toml")
        return

    logger.info("Starting vault embedding indexer")
    start_time = time.monotonic()

    try:
        summary = await index_vault(
            vault_root=config.vault_root,
            logger=logger,
            dry_run=dry_run,
        )

        elapsed_ms = int((time.monotonic() - start_time) * 1000)

        if dry_run:
            print("=== DRY RUN — Vault Embedding Indexer ===")
            print(f"\nVault root: {config.vault_root}")
            print(f"DB path: {get_db_path(config.vault_root)}")
            print(f"Embedding model: {EMBEDDING_MODEL} on {OLLAMA_HOST}:{OLLAMA_PORT}")
            print(f"Chunk size: ~{CHUNK_SIZE} tokens, overlap: ~{CHUNK_OVERLAP} tokens")
            print(f"\nTotal vault files: {summary['total_vault_files']}")
            print(f"Files needing indexing: {summary['files_needing_index']}")
            print(f"Files already indexed: {summary['files_already_indexed']}")
            print(f"Files deleted from index: {summary['files_deleted']}")
            print(f"\n--- Routing ---")
            print(f"Target machine: Mac Mini (192.168.68.200)")
            print(f"Target model: nomic-embed-text via Ollama")
            print(f"Cost: $0.00 (100% local)")
            print(f"Schedule: nightly 02:00 via launchd")
            print("\n=== END DRY RUN ===")
            return

        logger.info(
            f"Indexing complete: {summary['chunks_created']} chunks, "
            f"{summary['embeddings_generated']} embeddings, "
            f"{len(summary['errors'])} errors, {elapsed_ms}ms"
        )

        record_run(
            log_dir=config.log_dir,
            agent_name=AGENT_NAME,
            mode=None,
            status="success" if not summary["errors"] else "partial",
            cost_usd=0.00,
            duration_ms=elapsed_ms,
            turns=None,
            notes=(
                f"chunks={summary['chunks_created']}, "
                f"embeddings={summary['embeddings_generated']}, "
                f"errors={len(summary['errors'])}"
            ),
        )

    except Exception as e:
        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        logger.error(f"Vault indexer failed: {e}")
        record_run(
            log_dir=config.log_dir,
            agent_name=AGENT_NAME,
            mode=None,
            status="error",
            cost_usd=0.00,
            duration_ms=elapsed_ms,
            turns=None,
            notes=str(e)[:200],
        )
        raise


def main():
    parser = argparse.ArgumentParser(description="Vault Embedding Indexer Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Discover files and show what would be indexed, without calling Ollama",
    )
    args = parser.parse_args()

    asyncio.run(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
