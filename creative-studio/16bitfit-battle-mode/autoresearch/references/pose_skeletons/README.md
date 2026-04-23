# Phase 1 Pose Skeletons — SF2 Ryu Walk Cycle

Source: SF2 Ryu walk cycle from Spriters Resource (Super Street Fighter II Turbo / CPS2 sheet).

These 4 OpenPose skeletons are **frozen** inputs to the Phase 1 autoresearch scorer — they
are part of what every experiment is measured against. Never swap or modify mid-run.

## Target Files

```
references/pose_skeletons/
├── ryu_walk_contact.png    # Frame 1 — heel strike, legs spread wide
├── ryu_walk_down.png       # Frame 2 — lowest point, weight absorb
├── ryu_walk_passing.png    # Frame 3 — legs together, one vertical
└── ryu_walk_up.png         # Frame 4 — highest point, push-off
```

Each file: PNG, 512×512 (or whatever your ControlNet model expects), transparent or black
background, OpenPose skeleton overlay only (colored bone segments on dark background —
the standard OpenPose control image format).

## Extraction Steps (do these on the Alienware, where ComfyUI lives)

### Step 1 — Download the reference sheet
Grab Ryu's walk cycle from The Spriters Resource:
https://www.spriters-resource.com/arcade/ssf2t/sheet/240/

The walk cycle is the 4–6 frame row near the top-center labeled "Walking". Each frame is
roughly 48×80 at the original resolution.

### Step 2 — Extract and upscale the 4 keyframes
Open the sheet in any pixel editor (Aseprite, Photoshop, or GIMP). Identify the 4 walk
cycle poses that map to contact / down / passing / up:

- **Contact:** Front leg straight, heel planted. Back leg extended behind.
- **Down:** Lower body dips, weight transferred forward. Both knees slightly bent.
- **Passing:** Legs together, rear leg vertical under body.
- **Up:** Character at highest point, push-off foot extended back, front knee raising.

Crop each frame to an isolated 48×80 PNG. Nearest-neighbor upscale each to 512×512
(or your ControlNet model's expected size). Save these temporarily as
`ryu_walk_{contact,down,passing,up}_source.png` — these are reference inputs for the
preprocessor, NOT the final skeleton PNGs.

### Step 3 — Run DWPose preprocessor in ComfyUI
DWPose is more accurate than vanilla OpenPose for low-resolution characters — important
given Ryu's original 48×80 size.

Load workflow `tools/extract_poses.json` (build this as a 4-node graph):
```
Load Image (source frame) → DWPose Preprocessor → Save Image (skeleton PNG)
```

Run the workflow for each of the 4 upscaled frames. Save outputs to:
`autoresearch/references/pose_skeletons/ryu_walk_{contact,down,passing,up}.png`.

### Step 4 — Sanity check
Open each skeleton PNG. You should see colored bone segments (standard OpenPose format)
showing clearly different leg positions across the 4 frames. If two skeletons look
identical, the preprocessor mis-fired — redo that frame, possibly at a larger upscale
(1024×1024) for more detail.

Critical: **contact and passing must look visibly different** — distinct leg separation vs
legs-together. If they don't, ControlNet can't enforce the distinction downstream and
Phase 1's core hypothesis is compromised.

### Step 5 — Hand-correct if needed (acceptable, not cheating)
If DWPose misses a limb (common on low-res pixel art), you can manually tweak the skeleton
in any image editor — the control image just needs to be readable by ControlNet, it
doesn't have to come from automated extraction. This is standard practice in the ComfyUI
community. Document any manual edits in `edits.md` in this folder so the research is
reproducible.

## Licensing Note

SF2 sprites are Capcom IP. These skeletons are derivatives used solely as ControlNet
conditioning inputs for research purposes — we're not shipping Ryu's likeness, we're
using his pose as a pose reference (same as using a real photo of a walking person).
The generated output is styled as Sean, not Ryu. Keep this reference folder in `.gitignore`
if publishing the repo publicly.
