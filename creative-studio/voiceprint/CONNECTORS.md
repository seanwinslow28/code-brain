# Connectors

## How tool references work

Some plugins reference external tools by category, using `~~category` as a
placeholder for whatever the user connects (e.g. `~~project tracker` → Linear,
Asana, or Jira). Those placeholders get filled in during customization.

## Connectors for this plugin

**VoicePrint needs none.**

VoicePrint operates entirely on text the reader pastes into the conversation and
on plain files in the reader's own workspace. It does not read from or write to
any external service — no chat tool, no project tracker, no cloud storage, no
database. There is nothing to connect and nothing to customize here.

This is deliberate. The product's privacy guarantee ("paste me your old writing,
it stays local") only holds if the plugin has no outbound integrations. Keep it
that way: if a future feature seems to want a connector, prefer a local-file
solution first.

| Category | Placeholder | Used? |
|----------|-------------|-------|
| (none)   | (none)      | VoicePrint is connector-free by design |
