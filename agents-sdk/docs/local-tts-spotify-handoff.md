---
type: handoff-doc
created: 2026-05-15
status: deferred — gated on local TTS pipeline being stable across 10+ runs
---

# Save-to-Spotify Handoff — Sean's Research Briefings

## What this is

A handoff point for a future phase that pipes finished MP3s from
`vault/90_system/audio/` into Spotify's [`save-to-spotify`](https://github.com/spotify/save-to-spotify)
CLI as a private podcast / show titled "Sean's Research Briefings."

## Why deferred

The local TTS pipeline must prove itself on the verbatim guarantee and
chunking quality before adding a publishing leg. Re-open this doc once Sean
has listened end-to-end to at least 10 docs and the chaptering, prosody,
and idempotency feel right.

## Where to start when re-opening

1. **Verify save-to-spotify is the right tool.** As of 2026-05-15, the
   `spotify/save-to-spotify` repo state, license, and Spotify's private-show
   policy need fresh due diligence — none of it is being relied on yet.
   Spotify's "Anchor" / "Spotify for Podcasters" web UI may be a simpler
   route for a personal show than wiring a CLI.
2. **Define the show metadata model.** Each MP3 needs: episode title (from
   the source markdown H1 or filename), description (from the source's
   `description:` frontmatter or first paragraph), publish date (from
   filename prefix or frontmatter `created:`), cover art (probably a single
   static image reused across episodes).
3. **Decide the trigger.** Three options:
    - **a)** Manual `python3 scripts/publish_to_spotify.py --source x.mp3`
    - **b)** Auto-publish on every doc_to_audio run (extend the CLI)
    - **c)** Nightly batch — a new SDK agent that walks
      `vault/90_system/audio/` and publishes anything new
   Recommendation: start with (a). Promote to (c) only after 5+ uneventful
   manual runs.
4. **Authentication.** Spotify's API uses OAuth 2.0. Tokens belong in macOS
   Keychain via `agents-sdk/lib/keychain.py`, never in config.toml.
5. **Rollback.** Deleting a published episode is reversible via Spotify's UI
   — but URLs cached by clients may persist. Build the script to ALWAYS
   publish as DRAFT first; promote-to-live is a separate manual step.

## Handoff interface

The local TTS pipeline already gives you everything you need:

- **MP3 path:** `vault/90_system/audio/<source-stem>.mp3` — predictable from
  the source markdown path.
- **JSON output:** `doc_to_audio.py --json` emits `output_path`,
  `duration_sec`, `voice`, `speed`, `segments_synthesized` — perfect for a
  publisher script to consume via subprocess.
- **Idempotency:** the MP3 mtime tells you whether the source has been
  re-rendered and therefore whether to re-publish.

No changes to `doc_to_audio.py` itself are needed to support this. The
publisher is purely additive.

## Do NOT do in this phase

- Modify `doc_to_audio.py` to include a `--publish` flag (couples the
  layers).
- Add a `[spotify]` block to `config.toml` (premature).
- Pre-install `save-to-spotify` (no idea yet whether it's the right tool).

## When ready

Run a separate `/writing-plans` session with this doc as the spec input.
