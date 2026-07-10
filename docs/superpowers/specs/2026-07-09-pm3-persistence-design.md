# PM3 — Persistent Pain-Taxonomy Store (Design Spec, NOT BUILT)

**Date:** 2026-07-09
**Status:** Execute-ready pending the **7/21 PM3 t1 verdict** (GO → build from this spec; KILL/rescope → this spec cost $0 beyond the clustering test). **Do not build before that verdict.**
**Campaign:** fusion-discovery-council Phase 2, Item 4b.
**Grounding:** every matching decision below is measured, not assumed — see the 4a validation note
[`vault/20_projects/research/2026-07-09-pm3-4a-pain-key-clustering-validation.md`](../../vault/20_projects/research/2026-07-09-pm3-4a-pain-key-clustering-validation.md).

## Problem

Discovery runs are point-in-time: each run re-surfaces pains with no memory of prior runs, so
"is this pain growing?" is unanswerable. PM3 persists verified pains across runs so a re-run can
emit **accelerating / cooling / newly emerged** — the taxonomy-movement layer the D3 dashboard
already reserves a slot for. Prerequisite now satisfied: D3 Slice A made the session store
reliable (persist-by-default), so run history actually accumulates.

## What 4a measured (binding constraints on this design)

Tested on the two same-topic 2026-06-21 runs (3×12 verified pains, 36 cross-run pairs, human-judged):

| Matcher | Precision | Recall | Verdict |
|---|---|---|---|
| Canonical-title / token-Jaccard @ E3's 0.5 threshold | 0 claims | 0% | FAIL — cross-run phrasing drift sits at 0.06–0.17, far under the within-run dedup threshold |
| NLI cross-encoder (E1's, bidirectional, any threshold) | 0% | 0% | FAIL — principled: paraphrase duplicates entail in neither direction; specific→generic entails spuriously |
| Local LLM judge alone (qwen3.6-35b, temp 0) | 25% | 100% | FAIL — over-merges thematically-adjacent pains |
| **Candidate-gen (exact-URL ∪ lexical top-1) → LLM confirm** | **100%** | **100%** | **PASS** (n=1 true pair — read as "no measured failure", not a validated rate) |

Structural finding (8-for-8 on the sample): the stages fail in **complementary** ways — every LLM
false positive lies outside every cheap candidate set, and the judge rejects every false candidate
the cheap signals over-propose. Measured hazard: a lexical *band* candidate generator (e.g. ≥0.15)
admits the B1↔B7 pair the judge wrongly merges — **candidate gen must stay exact-URL ∪ top-1, never
band-based.**

Consequences:
1. **There is no stable pain-key.** No canonical title, no text hash, no embedding cluster id as
   primary key. Pains get an opaque autoincrement id; identity is established per-ingest by the
   two-stage matcher.
2. **RELATED is a first-class outcome**, stored as a typed link (concept_edges-shaped), never a merge.
3. Granularity mismatches (one broad pain ↔ several fine-grained ones) are real: matching must be
   one-to-many capable, each candidate judged independently.
4. Embedding-based candidate generation is an **untested upgrade path** — noted, not designed in.

## Storage

**SQLite at `vault/.discovery-pains.db`** — next to `vault/.vault-index.db` per the master plan,
but its **own file**: `vault-index.db` is owned by vault_indexer (different producer, different
lock discipline); sharing one file couples unrelated write paths. Pure-stdlib `sqlite3`, WAL mode,
same posture as `concept_edges.py` (kebab-case pragmatism, no ORM).

### Schema

```sql
CREATE TABLE pains (
    id            INTEGER PRIMARY KEY,
    display_title TEXT NOT NULL,          -- most recent observation's title (display only, NOT identity)
    first_seen    TEXT NOT NULL,          -- ISO date of first observation
    last_seen     TEXT NOT NULL,
    topic         TEXT NOT NULL,          -- gather topic of first observation
    segment       TEXT NOT NULL DEFAULT ''
);

CREATE TABLE observations (               -- one row per (pain, run) sighting
    id            INTEGER PRIMARY KEY,
    pain_id       INTEGER NOT NULL REFERENCES pains(id),
    session_id    TEXT NOT NULL,          -- session JSON id (D3's store is the provenance spine)
    observed_on   TEXT NOT NULL,          -- ISO date from session id
    topic         TEXT NOT NULL, tier TEXT NOT NULL, segment TEXT NOT NULL DEFAULT '',
    title         TEXT NOT NULL,          -- this run's phrasing (full text history preserved)
    summary       TEXT NOT NULL,
    intensity     INTEGER NOT NULL DEFAULT 0,     -- CandidatePainPoint.intensity (1-5)
    recency       TEXT NOT NULL DEFAULT '',       -- CandidatePainPoint.recency
    velocity_raw  REAL,                           -- E4 per-card slope when velocity_mode != off
    quote_count   INTEGER NOT NULL DEFAULT 0,
    UNIQUE(pain_id, session_id)
);

CREATE TABLE evidence (                   -- EvidenceRecord fields, serializer-compatible
    id            INTEGER PRIMARY KEY,
    observation_id INTEGER NOT NULL REFERENCES observations(id),
    source_type   TEXT NOT NULL, source_name TEXT NOT NULL,
    url           TEXT NOT NULL, date TEXT NOT NULL DEFAULT '',
    quote         TEXT NOT NULL, engagement INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX evidence_url ON evidence(url);        -- exact-URL candidate generation

CREATE TABLE pain_links (                 -- concept_edges-shaped typed relations
    src_pain_id   INTEGER NOT NULL REFERENCES pains(id),
    dst_pain_id   INTEGER NOT NULL REFERENCES pains(id),
    relation      TEXT NOT NULL CHECK (relation IN ('related_to','broader_than')),  -- broader_than = 4a's granularity mismatch
    session_id    TEXT NOT NULL,          -- run that asserted the link
    PRIMARY KEY (src_pain_id, dst_pain_id, relation)
);

CREATE TABLE match_audit (                -- every judge decision is auditable + replayable
    id            INTEGER PRIMARY KEY,
    session_id    TEXT NOT NULL,
    incoming_title TEXT NOT NULL,
    candidate_pain_id INTEGER NOT NULL,
    candidate_source TEXT NOT NULL,       -- 'url' | 'lexical-top1'
    lexical_score REAL NOT NULL,
    verdict       TEXT NOT NULL CHECK (verdict IN ('SAME','RELATED','DIFFERENT')),
    judge_model   TEXT NOT NULL,
    reason        TEXT NOT NULL DEFAULT ''
);
```

**Serializer reuse:** ingest consumes the in-memory objects the pipeline already has
(`VerifiedPainPoint.point` = `CandidatePainPoint(title, summary, quotes, urls, consensus,
intensity, recency, segment)`); the `evidence` table mirrors `EvidenceRecord` field-for-field so
`EvidenceBundle.to_dict()/from_dict()` round-trips rows without translation. No new serialization
format is invented.

## Ingest (where PM3 hooks the pipeline)

A post-frame step on `run_discovery`'s **success path only** (after the session write; pm lens
only), behind an opt-in flag (`DISCOVERY_PAIN_STORE=1` initially — flip to default-on after a
soak, mirroring the sessions_dir rollout). Session JSONs deliberately do NOT carry per-card pains
(D3's call); the store ingests from the live objects, with `session_id` linking each observation
back to the D3 session store. Store failures must never fail the run (the `_write_session`
posture: warn to stderr, run and spend records survive).

Per incoming verified pain:
1. **Candidate generation** (cheap, no LLM): pains sharing ≥1 exact evidence URL
   (`evidence_url` index) ∪ the lexical top-1 by E3's `pain_similarity` (reused as-is from
   `dedup.py`) over same-topic pains. **Never a similarity band** (measured B1↔B7 hazard).
2. **Confirmation**: temperature-0 local LLM judge (`qwen3.6_35b-a3b-32k` on MBP Ollama,
   `localhost:11434` — the 4a-measured configuration), strict `SAME | RELATED | DIFFERENT` with a
   one-line reason. Each candidate judged **independently** (one-to-many by construction).
3. **Outcome**: SAME → append an observation to that pain (update `last_seen`, `display_title`);
   RELATED → new pain + `related_to` link (granularity mismatch → `broader_than`); DIFFERENT / no
   candidates → new pain. Every judgment lands in `match_audit`.
4. **Degraded mode**: Ollama unreachable → ingest as new pains with a `match_audit` row
   (`judge_model='deferred'`), and a catch-up pass re-judges deferred rows on the next run.
   Honest deferral, **no cloud fallback** (fleet cost-safety rule: a local-route miss never
   silently becomes paid API spend).

## Trend emission (the PM3 payoff)

Computed at ingest end for the run's topic, written into (a) the ledger's new "Pain taxonomy
movement" section and (b) the D3 dashboard's reserved PM3 slot (replacing the placeholder):

- **Newly emerged** — pain's first observation is this run.
- **Accelerating** — ≥2 observations AND (intensity strictly rising across the last two
  observations OR `velocity_raw > 0` in the latest observation OR observation frequency rising:
  gap between the last two sightings < the mean prior gap).
- **Cooling** — previously observed on this topic but absent from this run's verified set, OR
  intensity strictly falling across the last two observations.
- Everything else: **steady** (rendered, not hidden — honesty rule).

Label definitions live in one pure function over `observations` rows so the 7/21 t1 data can
recalibrate them without schema change. **Open question the t1 re-run answers (the gate):**
whether cross-run deltas on a 2-week gap are signal or panel noise — that is red-team #5's
objection, and it gates the build, not this spec.

## Testing sketch (for the eventual build)

Hermetic throughout (tmp SQLite; judge behind an injectable seam like E4's `_pytrends_fetch`).
Fixtures replay the 4a corpus: the A2↔B10 true duplicate must merge; the four judge
false-positives (A1-B5, A1-B7, A3-B1, B1-B7) must never reach the judge (candidate-gen guard);
the A1-B12 granularity case must land `broader_than`, not a merge. Degraded-mode ingest, catch-up
re-judge, and trend-label unit tests over synthetic observation histories. Store failure never
fails the run.

## Out of scope

Embedding candidate-gen (upgrade path; test against the same 4a corpus first) · cross-topic
matching (same-topic only until t1 validates the spine) · any UI beyond the ledger section + D3
slot · building ANY of this before the 7/21 t1 GO.
