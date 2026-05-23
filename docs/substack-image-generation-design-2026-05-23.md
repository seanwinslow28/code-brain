---
type: design-doc
artifact: substack-image-generation-pipeline
created: 2026-05-23
status: draft-v1
ai-context: |
  Design for the voice-mode-aware Gonzo image-generation pipeline for Sean's Substack posts.
  Built on Nano Banana 2 (gemini-3.1-flash-image-preview) via the .claude/skills/gemini-image-gen
  skill. Anchored on 4 Ralph Steadman reference images Sean uploaded 2026-05-23 covering the full
  intensity gradient (maximal/painterly/restrained/line-only). Each voice mode pairs with one
  reference image + 6 prompt slots that swap per mode. Hybrid workflow (Option D): in-IDE for
  the next 3-5 posts to validate the prompt library; promote to autonomous substack_drafter
  agent once aesthetic is proven.
related:
  - "[[.claude/skills/gemini-image-gen/SKILL]]"
  - "[[.claude/skills/gemini-image-gen/references/nano-banana-2-capabilities]]"
  - "[[.claude/skills/writing-voice-modes/SKILL]]"
---

# Substack Image Generation Pipeline — Design v1

## What this is

A voice-mode-aware image-generation pipeline that pairs each of Sean's 5 voice modes (Sedaris / Thompson / Kerouac / Vonnegut / Sean Mode) with a dedicated Ralph Steadman reference image and a parameterized 7-Layer NB2 prompt. Output is a 16:9 Substack header image generated via Nano Banana 2 (`gemini-3.1-flash-image-preview`) at ~$0.045-0.067/image and 4-6s/generation.

## Why this approach (Option D — hybrid)

Three options were considered: (A) stay manual in ChatGPT, (B) in-IDE via Claude Code, (C) fully autonomous via `substack_drafter` agent. Picked **D — hybrid: B first, C once validated** because the Gonzo-by-voice-mode mapping needs ~3-5 real generations against real posts before the aesthetic is dialed in. Auto-pipelining unproven creative output risks 10 wrong images on a Thursday-night schedule. Same Tier-1.5-verification logic from the vault synthesizer retrofit: prove the prompt library in-session, promote to agent once predictable.

## Architecture

### Single anchor, varied registers

All output reads as one column-illustrator's hand (Steadman: india-ink + watercolor wash + deliberate splatter). What varies per voice is **ink density**, **palette**, **composition**, and **subject framing**. Same dial; 5 distinct settings.

### Voice mode → aesthetic mapping

| Voice mode | Ink density | Palette | Composition | Reference image |
|---|---|---|---|---|
| **Sedaris** (Domestic Observer) | Light, sketch-like, breathing room | Warm sepia, burnt orange, dusty rose, cream | Domestic interior — kitchen, late-night desk | `ref-3.png` (restrained Walter White portrait) |
| **Thompson** (Gonzo Technical) | HEAVY maximal, drips off the page, manic | Acid neon — coral, electric lemon, cobalt, sulfur | Distorted, fish-eye, things-coming-at-viewer | `ref-1.png` (maximal white-helmet Steadman) |
| **Kerouac** (Beat Flow) | Brush-stroke sweep, calligraphic | Cool jazz blues, cigarette grey, neon-sign red | Horizontal flow, jewel-center anchor + radiating motion | `ref-2.png` (cosmic radial explosion) |
| **Vonnegut** (Minimalist Absurdist) | Minimal — single line + one splatter | Monochrome grayscale + ONE accent color drop | Extreme negative space, object small in frame | `ref-4.png` (pen-line caricature) |
| **Sean Mode** (Hybrid default) | Medium, restrained Steadman, disciplined splatter | Teal `#0D7377` + amber `#B45309` over grayscale ink | Editorial-illustration / New Yorker cover | `ref-1.png` (canonical Steadman anchor) |

Reference images live at `vault/.../substack-drafts/substack-image-generation-references/substack-image-generation-ref-{1,2,3,4}.png` (Sean uploaded 2026-05-23). **One reference per call, not all four.** Multiple refs in one call confuses NB2's style transfer; one ref reinforces the text slots without interpolation muddiness.

### Prompt template (constant across all modes)

```
Layer 1 (Task): Create an editorial illustration.

Layer 2 (Context): Substack post header for Sean Winslow's personal essay
titled "{POST_TITLE}". The essay's subject is {POST_SUBJECT_ONE_SENTENCE}.
Audience is AI product managers, recruiters, and engineering leaders.

Layer 3 (Style): Ralph Steadman gonzo style. Confident india-ink linework
with watercolor wash splotches and deliberate ink splatter.
{VOICE_INK_DENSITY}. Hand-drawn medium throughout — not digital-flat,
not photorealistic.

Layer 4 (Layout): {VOICE_COMPOSITION}. {VOICE_FRAMING}. Aspect ratio 16:9
for Substack header. Generous breathing room around the central subject.

Layer 5 (Consistency): Single coherent ink-and-watercolor medium. The
splatter and drips are deliberate, controlled, never chaotic. The
watercolor wash sits BEHIND the ink, not on top of it.

Layer 6 (Uniformity): Palette: {VOICE_PALETTE}. Lighting: {VOICE_LIGHTING}.
Mood: {VOICE_MOOD}.

Layer 7 (Output): High detail in the ink work. Not photorealistic. Not
digital illustration. Hand-drawn editorial quality, magazine-cover register.
NO text in the image. NO watermark. NO signature. Negative space is a
feature, not a bug.
```

### Six voice slots (swap per mode)

| Slot | Sedaris | Thompson | Kerouac | Vonnegut | Sean Mode |
|---|---|---|---|---|---|
| `INK_DENSITY` | Lighter density, sketch-like, breathing room | Heavy maximal Steadman — splatter + drips running off the page, manic gesture | Brush-stroke energy — calligraphic sweep rather than splatter | Minimal — single confident line, one strategic splatter, rest negative space | Medium — recognizably Steadman but restrained, disciplined splatter |
| `COMPOSITION` | Domestic interior framing | Distorted perspective, fish-eye, things-coming-at-the-viewer | Long horizontal flow with one anchor object centered | Extreme negative space, object small in frame | Editorial-illustration / New Yorker cover framing |
| `FRAMING` | Technical element placed naturally in domestic scene as if it belongs | First-person POV inside chaos — monitor, dashboard, agent fleet thrashing | The jewel-center object at center, brushwork + motion lines radiating outward | Like a hand-drawn doodle from *Breakfast of Champions* — one isolated object | Scene from actual post rendered literally, slightly off-kilter |
| `PALETTE` | Warm sepia, burnt orange, dusty rose, cream wash | Acid neon — coral red, electric lemon, cobalt blue, sulfur yellow | Cool jazz blues, cigarette grey, neon-sign red (60s NYC nocturne) | Monochrome grayscale with ONE accent color drop | Teal `#0D7377` + amber `#B45309` (portfolio brand) over grayscale ink |
| `LIGHTING` | Soft warm interior — single desk lamp or stove hood | Harsh poker-game light from below, monitor glow, no daylight | Nocturnal — neon signs, wet pavement reflection, single street lamp | Flat even printed-page light, no shadow | Natural daylight from upper left, soft shadows |
| `MOOD` | Cozy, slightly off-kilter, New-Yorker-editorial register | Visceral, chaotic, slightly nauseating — writer mid-quest | Nocturnal momentum, road-trip energy, jazz-club velocity | Deadpan, slightly absurd, devastating in restraint | Confident, slightly off-kilter, authored |

## Workflow

### File layout

```
vault/.../substack-drafts/
├── *.md                              (draft files)
├── images/                           (NEW — generated headers land here)
│   └── <post-slug>-header.png
├── substack-image-generation-references/   (Sean's Steadman anchors)
│   ├── substack-image-generation-ref-{1..4}.png
└── experiments/                      (R&D from 2026-05-22 consolidation)
```

### Frontmatter contract

Every substack-draft .md gets two optional fields:

```yaml
voice_mode: sedaris   # sedaris | thompson | kerouac | vonnegut | sean (default: sean)
header_image: images/<post-slug>-header.png   # populated after generation
```

### Invocation (in-session, Option D Phase B)

Sean: "Generate the header image for `<post-slug>` post."

Claude Code:
1. Read the .md, pull `voice_mode` from frontmatter (or detect from voice tone)
2. Extract `POST_SUBJECT_ONE_SENTENCE` (load-bearing variable; ask Sean if not derivable)
3. Assemble the prompt from template + 6 voice slots
4. Run `python3 .claude/skills/gemini-image-gen/scripts/generate_image.py "<prompt>" --output vault/.../substack-drafts/images/<slug>-header.png --aspect-ratio 16:9 --env-file .env --reference vault/.../substack-image-generation-references/substack-image-generation-ref-<n>.png`
5. Show output; iterate via conversational editing (NB2's strength)
6. Once accepted, write `header_image:` frontmatter back into the .md

### Cost + speed envelope

| Resolution | Cost/image | Time/image | Per-post budget (≈3 iterations) |
|---|---|---|---|
| 0.5K | ~$0.045 | 2-4s | ~$0.14 |
| 1K (default) | ~$0.067 | 4-6s | ~$0.20 |
| 2K | ~$0.10 | 8-15s | ~$0.30 |

**Recommendation:** 1K for first pass + iterations, generate final at 2K only after the composition is locked. Substack auto-resizes; 1K header reads fine on the platform.

## Promotion path (Option D Phase C)

Once 3-5 generations land cleanly and Sean has signed off on the aesthetic:

1. Add `image_gen` step to [`agents-sdk/agents/substack_drafter.py`](agents-sdk/agents/substack_drafter.py) after the text-draft step
2. Agent reads `voice_mode` from frontmatter (or detects from prompt)
3. Agent generates image + writes back to .md frontmatter
4. Agent's existing cost cap absorbs the ~$0.10 marginal cost (currently `max_budget_usd = 0.10` at the agent level — may need bump)
5. Update `[agents.substack_drafter]` config block in `agents-sdk/config.toml`
6. Optional: surface image preview in the daily-driver morning brief (Thursday-after-substack-run)

## Open questions (resolve as we go)

1. **What's the Substack header dimension Substack actually crops to?** Spec says 1456×816 (16:9). NB2 generates 1024×576 at 1K-16:9. Upscaling 1024→1456 via Substack's renderer is fine for editorial illustration (no fine detail loss). If we want native res, generate at 2K (2048×1152) and downscale.
2. **Should I batch-generate variants?** Per NB2 capabilities §8: the "grid trick" (request 4x4 grid at 2K) gets 16 images for ~$0.10. Could be a Phase C optimization for picking-best-of-4 per post.
3. **What about inline images mid-post?** Out of scope for v1 (header only). Add to backlog if Sean wants them.
4. **Voice detection from prose** (when `voice_mode` frontmatter is absent) — for Phase C, the agent could use a small classifier or just ask. Out of scope for in-IDE Phase B (Sean specifies).

## Rollback

- `rm -rf vault/.../substack-drafts/images/` (deletes generated images; references untouched)
- `git revert <commit>` on this design doc
- No code changes yet (Phase B is in-session script invocation only); nothing to revert in agents-sdk

## First test (2026-05-23) — Sedaris v2 LOCKED as canonical

**v1 result:** generic *Bon Appétit*-style watercolor magazine illustration. Steadman aesthetic barely present. Root cause: over-correcting for "Sedaris = restrained" via the phrase "deliberate, controlled, never chaotic" + Ref 3 (the most restrained anchor of the 4) created a dual-restraint signal that pushed past Steadman into "tasteful." Preserved at `images/2026-05-10-the-night-my-vault-said-nothing-header-v1-superseded.png`.

**v2 result:** authored Steadman-quiet, kitchen-table-discovery-at-11pm. Notebook handwriting renders specific failure modes (`concept_null_v3`, `data_void_log`, `report_zero`) — model picked up the post's actual story from `POST_SUBJECT_ONE_SENTENCE`. Visible artistic urgency, wonky perspective (table askew, lamp cord curves), deliberate Steadman ink splatter in deeper umber. Saved as canonical at `images/2026-05-10-the-night-my-vault-said-nothing-header.png`.

**Key word-choice learning:** the model hears "lighter density" as "make it gentle," but hears "Steadman dialed down to a quiet domestic register" as "same artist, quiet mode." Word choice on the style anchor matters more than density adjectives. Sedaris voice slots updated below to reflect this.

### Sedaris voice slots — v2-validated (LOCKED)

| Slot | Sedaris (v2-validated) |
|---|---|
| `INK_DENSITY` | In the unmistakable style of Ralph Steadman, dialed down to a quiet domestic register: gestural india-ink linework with visible pen-pressure variation, calligraphic flicks, and a few deliberate ink splatters and drips. Hand-drawn at speed by an artist who knows what they are doing — NOT slowly rendered, NOT smooth, NOT polished magazine-illustration. Visible artistic urgency. |
| `COMPOSITION` | Domestic interior framing — kitchen or late-night desk, viewed at a low three-quarter angle. The table edge slightly askew, the lamp cord curves where it should hang straight, the laptop screen tilts a few degrees off-square. |
| `FRAMING` | Technical element placed naturally in the domestic scene as if it belongs. Specific objects + handwritten text on visible surfaces (notebook, sticky notes, etc.) that directly visualize the post's actual content. The pen lines on any handwriting should look like real urgent handwriting, not lettering. |
| `PALETTE` | Warm sepia, burnt orange, dusty rose, and cream wash, with two or three small deliberate ink splatters in deeper umber and one tiny pop of muted teal as a subtle portfolio bridge. |
| `LIGHTING` | Soft warm interior light from a single screen or lamp source and one overhead pendant casting a small circle of light. |
| `MOOD` | Cozy but slightly off-kilter, like a New Yorker editorial illustration drawn by Ralph Steadman if Steadman were having a good night. The viewer should feel the late hour and the quiet shock of discovery in the same frame. |

### Sean Mode voice slots — INITIAL (test pending on manifesto)

| Slot | Sean Mode (initial draft) |
|---|---|
| `INK_DENSITY` | Medium-intensity Steadman — recognizably gonzo but restrained, disciplined splatter. Gestural india-ink linework with visible pen-pressure variation. Hand-drawn at speed with visible artistic urgency. NOT smooth vector, NOT digital flat, NOT polished magazine-illustration. |
| `COMPOSITION` | Editorial-illustration / New Yorker cover framing, slightly off-kilter. |
| `FRAMING` | Scene from the actual post rendered literally with deliberate visual quirks. Wonky perspective — geometric elements drawn by hand, not by ruler, so lines curve slightly and intersect imperfectly. |
| `PALETTE` | Confident grayscale ink linework over off-white paper, with strict accent use of teal (#0D7377) and amber (#B45309) — the portfolio brand palette. Accent colors used sparingly to emphasize specific subject elements that carry the argument. |
| `LIGHTING` | Natural daylight from upper left, soft cast shadows suggesting the subject sits on a desk. |
| `MOOD` | Confident, slightly off-kilter, authored. Editorial-cover register — the kind of illustration that would land on the front of a Wired or New Yorker tech feature. |

### Special-case prompt rules

- **Chart / diagram subjects:** override the universal "NO text in the image" rule to allow brief hand-painted axis labels or essential chart text. The "no text" constraint is for editorial titles/captions, not for in-scene functional text (labels on a chart, handwriting on a notebook).
- **Reference image selection:** always pass exactly ONE reference per call, picked by voice mode per the table above. Multi-reference calls cause style soup.
- **Word choice on style anchor:** "In the unmistakable style of Ralph Steadman, dialed down to a [register-appropriate descriptor]" outperforms density adjectives ("lighter," "heavier"). Frame each voice as "same artist, [register] mode" rather than "more/less of X."
