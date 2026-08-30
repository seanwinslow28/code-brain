# DRAFT — upstream issue for `teng-lin/notebooklm-py` (DO NOT POST without Sean's explicit approval)

Drafted 2026-08-29. Repro re-run and confirmed live the same evening. When approved,
post to https://github.com/teng-lin/notebooklm-py/issues. Sanity-check before posting:
(1) `notebooklm --version` still matches; (2) search existing issues for
"RPCResponseTooLargeError" to avoid a duplicate; (3) strip nothing — the trivial-ask
nuance is the useful part of the report.

---

**Title:** `chat.ask` fails with RPCResponseTooLargeError (52,428,800-byte client cap) on large notebooks — but only for substantive questions

**Body:**

## Summary

On a 57-source notebook, `notebooklm ask` hard-fails when the underlying `chat.ask`
RPC response exceeds the client's 50 MiB read cap. The answer is never received. The
failure depends on the *question*, not just the notebook: a trivial ask succeeds on the
same notebook, while a cross-source synthesis ask fails.

## Environment

- NotebookLM CLI, version **0.7.3** (`notebooklm --version`)
- macOS (Apple Silicon), Python CLI installed at `~/.local/bin/notebooklm`
- Notebook: 57 sources (mix of YouTube transcripts, markdown docs, web articles)

## Repro (2026-08-29)

Same notebook, same session, two consecutive asks:

```console
$ notebooklm ask "In one sentence, what is this notebook about?"
Answer:
This notebook is a comprehensive collection of video transcripts, ...   # succeeds

$ notebooklm ask "Across all sources, compare how Uber, Stripe, Shopify, and Ramp place evaluation gates in their agent pipelines, with citations."
21:42:32 WARNING [notebooklm.middleware.tracing] [req=2169445d] rpc failed: chat.ask (RPCResponseTooLargeError)
Error: RPC response exceeded 52428800 bytes (read 52443017 bytes before aborting)
```

## Additional observations (earlier session, same notebook, same CLI version)

- `-s` source scoping did **not** avoid the failure on this notebook for substantive
  questions; scoped asks only succeeded at ≤8 sources, and only when the selected
  sources were themselves small.
- Per-source `notebooklm source fulltext` works reliably at any notebook size and is
  the workaround we use.

## Expected

Either (a) the large RPC response is streamed/chunked so the answer survives, or
(b) the client fails fast with a message that names the actual constraint ("this
question's grounding payload exceeds the 50 MiB response cap — try scoping with -s or
reduce sources") rather than a raw byte-count error after a long wait.

## Guess at mechanism (unverified)

The RPC response appears to scale with the grounding/citation payload for the material
the question touches, not with the answer text — which is why notebook size alone
doesn't predict the failure and a large notebook looks healthy until the first real
cross-source question. If the cap is a tunable client constant, exposing it (env var or
flag) might be a cheap mitigation; if the payload is mostly grounding data the CLI
discards anyway, aborting the read early or filtering fields server-side would be
better.

Happy to provide verbose logs (`-vv`) or run diagnostics on the same notebook.
