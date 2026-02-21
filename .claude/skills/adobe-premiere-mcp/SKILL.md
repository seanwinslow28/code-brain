---
name: adobe-premiere-mcp
description: Adobe Premiere Pro video editing and timeline automation via adb-mcp. Use when editing video in Premiere, assembling timelines, adding transitions, exporting sequences, mixing audio, color grading, managing bins, cutting footage, or working with the Premiere MCP server.
---

# Adobe Premiere Pro MCP

## Purpose

Execute video editing operations in Premiere Pro through the adb-mcp server's UXP plugin. Combine programmatic timeline control with editorial intelligence (pacing, rhythm, continuity) to assemble, refine, and export video content.

## When to Use

- Editing video or assembling timelines in Premiere via MCP
- Importing and organizing media into bin structures
- Trimming clips, adding transitions, or adjusting timing
- Exporting sequences for delivery (festival, social, web)
- Applying basic effects (blur, B&W, opacity)
- Reviewing edits and critiquing pacing or continuity
- Building automated rough cuts from asset folders

## Examples

**Example 1: Automated rough cut from sprites**
```
User: "Import these 24 animation frames and assemble a rough cut at 24fps"
Claude: [Uses adobe-premiere-mcp]
  1. create_project → create bins ("01_Raw_Frames", "02_Sequences")
  2. import_media(file_paths) → move_project_items_to_bin("01_Raw_Frames")
  3. create_sequence_from_media with ordered frame list
  4. get_sequence_frame_image at 0s and 0.5s to verify assembly
  "Rough cut assembled. 24 frames on timeline at 24fps. Want me to adjust hold times?"
```

**Example 2: Export for multiple platforms**
```
User: "Export this edit for TikTok and YouTube"
Claude: [Uses adobe-premiere-mcp]
  1. save_project — checkpoint before export
  2. export_sequence with TikTok preset (.epr): H.264, 9:16, 1080x1920
  3. export_sequence with YouTube preset (.epr): H.264, 16:9, 1920x1080
  Note: "I need the .epr preset file paths. Do you have them, or should I use defaults?"
```

**Example 3: Critiquing an edit**
```
User: "Review my timeline — does the pacing work?"
Claude: [Uses adobe-premiere-mcp]
  1. get_sequence_frame_image at key moments (0s, 3s, 7s, 12s)
  2. Applies Murch's Rule of Six:
     - Emotion: "The cut at 7s lands on an awkward expression — trim 2 frames earlier"
     - Rhythm: "Shots 3-5 are metrically identical (2s each) — vary shot 4 to 3s for rhythmic interest"
     - Eye Trace: "Subject jumps from left to right frame between shots 2-3 — add a 6-frame dissolve"
```

## Premiere Pro Fundamentals

### Document Object Model

- **Application (`app`)** → root entry point
- **Project (`app.project`)** → the active `.prproj` file containing all assets
- **Project Item** → assets in the Project Panel (Clips, Bins, Sequences)
- **Sequence** → the timeline where editing occurs, containing Tracks
- **Track** → horizontal layers: Video `V1, V2...` / Audio `A1, A2...`
- **Track Item (Clip Instance)** → a specific instance of a Project Item placed on a Track

### Critical Concepts

- **Ticks**: Premiere's internal time unit. Many MCP tools require time in ticks, not seconds. Standard: ~254,016,000,000 ticks per second.
- **Preset (.epr)**: Required file for exporting. The MCP **cannot** define encoding settings (bitrate, codec) dynamically — it must reference an `.epr` file path.
- **Index-based operations**: The MCP cannot "select" clips visually. All operations target items by track index and item index.

### Plugin Architecture

Premiere uses a **UXP plugin** via adb-mcp. The API is **more limited than Photoshop** — many features require manual intervention.

```
Claude Code ↔ MCP Server (Python, stdio) ↔ Proxy Server (Node.js, WebSocket) ↔ UXP Plugin ↔ Premiere Pro
```

Load app-specific guidance at session start with `config://get_instructions`.

### What MCP Can vs Cannot Do

| Can Automate | Requires Manual Work |
|-------------|---------------------|
| Create projects, import media, organize bins | Merge Clips / Multi-Camera sequences |
| Build sequences, add clips to timeline | Complex Lumetri Color grading |
| Trim clip in/out points, ripple delete | Audio ducking, Essential Sound panel |
| Add basic effects (blur, B&W, opacity) | Keyframing effects beyond basic properties |
| Add transitions (dissolves, wipes) | Source Monitor preview |
| Export via .epr presets | Dynamic encoding settings (must use presets) |
| Add markers for review notes | Warp Stabilizer, advanced effects |
| Get frame screenshots for visual review | Multicam editing |

For the complete MCP command reference, see `references/premiere-mcp-commands.md`.

## Editorial Intelligence

### Walter Murch's Rule of Six (Decision Hierarchy)

When reviewing or suggesting edits, prioritize in this order:

1. **Emotion (51%)** — Does the cut capture the right feeling? Check expressions at cut points.
2. **Story (23%)** — Does the shot advance the narrative?
3. **Rhythm (10%)** — Check shot duration patterns. Vary between metric (equal) and rhythmic (variable) montage.
4. **Eye Trace (7%)** — Where is the subject in Frame A vs Frame B? Mismatched positions need a transition.
5. **2D Plane (5%)** — Respect the 180-degree rule.
6. **3D Space (4%)** — Maintain spatial continuity.

### Editing Grammar

| Technique | When to Use | How to Execute |
|-----------|-------------|---------------|
| **Hard Cut** | Emphasis, energy, matching action | Default — no transition needed |
| **J-Cut** | Audio leads video (anticipation) | Extend audio in-point before video in-point |
| **L-Cut** | Audio trails video (continuity) | Extend audio out-point past video out-point |
| **Dissolve** | Time passage, emotional shift | `append_video_transition("Cross Dissolve")` |
| **Match Cut** | Visual or thematic continuity | Cut on matching geometry/motion between shots |

### Pacing Guidelines

- **3-5 second rule**: Average shot length for engaging content
- **Metric montage**: Equal shot durations — creates mechanical tension
- **Rhythmic montage**: Variable durations matched to content — creates organic flow
- **Readability floor**: Any cut shorter than 3 frames is invisible to viewers

## Workflow Patterns

### Pattern A: Automated Rough Cut
1. `create_project` → `create_bin_in_active_project` ("01_Footage", "02_Sequences")
2. `import_media` → `move_project_items_to_bin`
3. `create_sequence_from_media` with ordered asset list
4. Adjust timing with `set_clip_start_end_times` (in ticks)
5. Verify with `get_sequence_frame_image` at key moments

### Pattern B: Audio Sync (Manual Handoff)
1. Create and organize bins via MCP
2. **MANUAL STEP**: "Please select the video and audio clips, right-click, and choose 'Create Multi-Camera Source Sequence' using Audio Waveform sync."
3. After manual sync: use `set_clip_disabled` to manage track layers

### Pattern C: Platform Export
1. `save_project` — always save before export
2. Determine preset: Festival (ProRes 422 HQ), YouTube (H.264 16:9), TikTok (H.264 9:16)
3. `export_sequence(sequence_id, output_path, preset_path)` using the `.epr` file

## Execution Protocol

### Small-Batch Pattern
1. Execute **2-3 operations**
2. **Pause** — call `get_sequence_frame_image` at key timecodes to verify
3. **Continue** only after verification
4. `save_project` before batch imports, destructive ops, or exports

### Guardrails

| Rule | Action |
|------|--------|
| Ripple Delete default | Default `ripple_delete=False` (Lift). Only ripple on explicit request — prevents audio desync. |
| Overwrite protection | `add_media_to_sequence` defaults to `overwrite=True`. Check track first, prefer adding to a new track. |
| Save before risk | `save_project` before batch operations, ripple deletes, or exports |
| Naming conventions | Bins: numbered prefixes (`01_Footage`). Sequences: append version (`_v01`). Exports: `[Date]_[Project]_[Codec].mp4` |

### Export Standards Quick Reference

| Target | Codec | Resolution | Bitrate | Notes |
|--------|-------|------------|---------|-------|
| Festival (DCP) | ProRes 422 HQ | Project native | N/A | PCM audio, 24fps |
| YouTube | H.264 High | 1920x1080 | 10-20 Mbps VBR 2-pass | Maximum Render Quality |
| TikTok/Reels | H.264 High | 1080x1920 (9:16) | 8-12 Mbps | Keep text out of bottom 15% |
| General web | H.264 High | 1920x1080 | 8-15 Mbps VBR 2-pass | sRGB color space |

### Error Handling

- **Export timeout**: Heavy exports may timeout the MCP request but continue in Premiere. Advise user to check Media Encoder.
- **Missing preset**: If `.epr` not found, instruct user to export once manually from Media Encoder to create the preset.
- **Sandbox permission denied**: User must grant folder access via UXP Developer Tool.
- **Limited effects**: Only basic effects (Blur, B&W) available via MCP. For Lumetri, instruct manual application.

For shared guardrails and cross-app patterns, see `adobe-cross-app-workflows`. For planning and critique, see `creative-director`.

## Success Criteria

- [ ] Loaded Premiere MCP guidance via `config://get_instructions` at session start
- [ ] Executed in small batches (2-3 ops → get_sequence_frame_image → continue)
- [ ] Clearly communicated what MCP can automate vs what requires manual work
- [ ] Used Lift (not Ripple Delete) by default unless explicitly requested
- [ ] Saved project before all high-risk operations
- [ ] Applied editorial grammar when reviewing or suggesting edits
- [ ] Referenced .epr preset paths for all export operations

## Copy/Paste Ready

```
"Import these clips and assemble a rough cut"
"Export this sequence for TikTok and YouTube"
"Review my edit and critique the pacing"
"Organize my project bins and import media"
"Add transitions between these shots"
```
