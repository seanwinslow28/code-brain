# NotebookLM CLI — known limitation on large notebooks

*Recorded 2026-08-29. Lives here (not in `~/.claude/skills/notebooklm/`) because
`notebooklm skill install` overwrites the skill file on update — this note survives.*

## The 52MB `chat.ask` cap

On large notebooks, `notebooklm ask` (RPC `chat.ask`) can hard-fail with:

```
WARNING [notebooklm.middleware.tracing] [req=...] rpc failed: chat.ask (RPCResponseTooLargeError)
Error: RPC response exceeded 52428800 bytes (read 52443017 bytes before aborting)
```

The 52,428,800-byte (50 MiB) limit is a **client-side** read cap in notebooklm-py, hit
while streaming Google's RPC response — the answer itself is never seen.

**What we know from two sessions against the same 57-source notebook**
(`Startup-Ideas-AI-Agents-S…`, CLI 0.7.3):

- 2026-08-29 (lit-delta session): substantive cross-corpus asks failed with the error
  above **regardless of `-s` source scoping** on the 57-source notebook. Scoped asks
  succeeded at **≤8 sources, and only when the selected sources were small**.
- 2026-08-29 (evening re-verification): a **trivial ask succeeded** on the full
  notebook ("what is this notebook about?"), while a substantive multi-company
  comparison ask failed at 52,443,017 bytes. So the trigger is the size of the RPC
  response payload for that particular question (grounding/citation payload scaling
  with material touched), **not notebook size alone** — which also means a large
  notebook can *appear* to work until the first real question.

## Reliable paths on large notebooks

1. **Per-source `notebooklm source fulltext`** — the reliable extraction path at any
   notebook size; pull transcripts source-by-source and synthesize locally.
2. Scoped asks (`-s`) only for small source subsets (≤8 small sources observed working).
3. Keep working notebooks well under ~50 sources if you want `ask` to be dependable.

Upstream: `teng-lin/notebooklm-py`. Issue draft (not yet posted — Sean approves any
public posting) at
[docs/prompts/drafts/2026-08-29-notebooklm-py-issue-draft-rpc-response-too-large.md](../../docs/prompts/drafts/2026-08-29-notebooklm-py-issue-draft-rpc-response-too-large.md).
