# Premiere Pro MCP Command Reference

Read this when you need exact parameter details for a specific Premiere MCP tool call. The main SKILL.md provides the overview and editorial intelligence; this file has the complete command list.

## Important: Time in Ticks

Many Premiere MCP commands use **ticks** (not seconds) for time values. Premiere's internal tick rate is approximately 254,016,000,000 ticks per second. The exact rate may vary — use `get_project_info` to determine the timebase.

## Project Management

### create_project
- `directory_path` (string): Folder for the .prproj file
- `project_name` (string): Name of the project
Creates a new Premiere Pro project.

### open_project
- `file_path` (string): Path to existing .prproj
Opens an existing project.

### save_project
Saves the current project. **Call before every high-risk operation.**

### save_project_as
- `file_path` (string): New save location
Saves a copy of the project to a new path.

### get_project_info
Returns active project name, path, ID, items structure, and timebase.
Use as pre-flight check and to understand project state.

## Asset Organization

### import_media
- `file_paths` (array of strings): Paths to video/audio/image files
Ingests raw media into the project panel.

### create_bin_in_active_project
- `bin_name` (string): Name for the new bin
Creates an organizational folder. Use numbered prefixes: `01_Footage`, `02_Sequences`, `03_Renders`.

### move_project_items_to_bin
- `item_names` (array of strings): Names of items to move
- `bin_name` (string): Target bin name
Sorts assets into bins after import.

## Sequence Construction

### create_sequence_from_media
- `item_names` (array of strings): Ordered list of media items
- `sequence_name` (string): Name for the new sequence
Quick assembly — creates a stringout from the listed items in order.

### set_active_sequence
- `sequence_id` (string): Sequence identifier
Focuses a specific timeline for subsequent operations.

### add_media_to_sequence
- `sequence_id` (string): Target sequence
- `item_name` (string): Media item to add
- `video_track_index` (int): Target video track (0-based)
- `audio_track_index` (int): Target audio track (0-based)
- `insertion_time_ticks` (int): Position on timeline **in ticks**
- `overwrite` (bool): Whether to overwrite existing content (default: True)
**Warning**: Defaults to overwrite. Check track contents first or use a new track index.

### remove_item_from_sequence
- `sequence_id` (string): Target sequence
- `track_index` (int): Track number
- `track_item_index` (int): Item position on track
- `track_type` (string): "video" or "audio"
- `ripple_delete` (bool): Close the gap after removal
**Default to False (Lift)** unless user explicitly requests ripple delete. Ripple can desync audio.

### close_gaps_on_sequence
- `sequence_id` (string): Target sequence
- `track_index` (int): Track to close gaps on
- `track_type` (string): "video" or "audio"
Automated ripple delete for all gaps on a track.

## Clip Manipulation

### set_clip_start_end_times
- `sequence_id` (string): Target sequence
- `track_index` (int): Track number
- `track_item_index` (int): Item position
- `start_time_ticks` (int): New in-point **in ticks**
- `end_time_ticks` (int): New out-point **in ticks**
- `track_type` (string): "video" or "audio"
Trims or extends clips. Use for pacing adjustments.

### set_clip_disabled
- `sequence_id` (string): Target sequence
- `track_index` (int): Track number
- `track_item_index` (int): Item position
- `disabled` (bool): True to mute/hide
Mutes audio or hides video clips without removing them.

### set_video_clip_properties
- `sequence_id` (string): Target sequence
- `track_index` (int): Track number
- `track_item_index` (int): Item position
- `opacity` (float): 0-100
- `blend_mode` (string): Blend mode name
Basic compositing adjustments.

### append_video_transition
- `sequence_id` (string): Target sequence
- `track_index` (int): Track number
- `track_item_index` (int): Item position
- `transition_name` (string): e.g., "Cross Dissolve", "Dip to Black"
- `duration` (float): Duration in seconds
- `clip_alignment` (string): Where to place transition relative to cut point

## Effects

### add_black_and_white_effect
Applies black and white effect to a clip.

### add_gaussian_blur_effect
Applies gaussian blur with configurable amount.

### add_motion_blur_effect
Applies motion blur effect.

**Note**: These are the only effects available via MCP. For Lumetri Color, Warp Stabilizer, or other complex effects, instruct the user to apply manually.

## Review & Export

### get_sequence_frame_image
- `sequence_id` (string): Target sequence
- `seconds` (float): Timecode position in seconds
Returns a JPEG at the specified timecode. This is how Claude "sees" the edit.
Use at multiple timecodes to review pacing and composition.

### add_marker_to_sequence
- `sequence_id` (string): Target sequence
- `marker_name` (string): Label
- `start_time_ticks` (int): Position **in ticks**
- `duration_ticks` (int): Duration **in ticks**
- `comments` (string): Notes
- `marker_type` (string): Color/type category
Use for logging critique notes and review feedback on the timeline.

### export_frame
- `sequence_id` (string): Target sequence
- `seconds` (float): Timecode
- `output_path` (string): File save location
Exports a single still frame to disk.

### export_sequence
- `sequence_id` (string): Target sequence
- `output_path` (string): Output file path
- `preset_path` (string): Path to .epr export preset file
**Requires a preset file.** Cannot set codec/bitrate dynamically.
May timeout on long sequences but export continues in Premiere background.

## Audio

### set_audio_track_mute
- `sequence_id` (string): Target sequence
- `track_index` (int): Audio track number
- `muted` (bool): True to mute
Mutes an entire audio track.

## Known Limitations

- No Multicam or Merge Clips via MCP
- No Source Monitor control
- No selection state — all operations are index-based
- No dynamic encoding settings — must use .epr presets
- No Lumetri Color or complex effect parameter control
- Sandbox restrictions may block file access
- Long exports may timeout the MCP connection (export still continues)
