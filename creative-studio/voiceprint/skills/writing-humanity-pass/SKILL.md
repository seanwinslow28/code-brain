---
name: writing-humanity-pass
description: >
  Remove the documented "Signs of AI writing" from a draft and rebuild human texture,
  calibrated to YOUR voice. Auto-detects voice-bearing vs neutral text and scrubs
  accordingly. Cuts significance inflation, -ing padding, copula avoidance, chatbot
  artifacts, filler, hedging, and ~25 more tells. Pairs with your generated voice
  skill (runs as the final pass after a voice write) and runs standalone. Use when
  asked to "scrub the AI out of this", "make this less AI", "de-slop this draft",
  "humanize this", "this sounds like AI", or "remove AI tells".
version: 0.1.0
---

# Writing Humanity Pass

## Purpose

Remove the documented "Signs of AI writing" from a draft and rebuild human texture,
calibrated to the writer's own voice. This is an editing pass, not a composition
skill. It pairs with the writer's generated voice skill (runs as the final pass after
a voice write) and runs standalone for cleaning agent-generated or foreign drafts.

The core rule: **the writer's voice is the authority. A pattern is only a tell when it
is NOT one of their signature moves.** The "do-not-flag" allowlist IS the
signature-move table in the writer's own voice skill (`my-voice/SKILL.md`).

## How It Works: Detect Register, Then Scrub

### Step 1. Classify the text
- Voice-bearing (essay, blog, newsletter, social, personal writing): VOICE-SAFE SCRUB.
- Neutral (docs, specs, runbooks, reference notes): FULL SCRUB.

Ambiguous routes to VOICE-SAFE (the safer failure: preserves more, scrubs less).

### Step 2. The scrub loop (both registers)
1. Draft rewrite. Apply `references/ai-tells.md` for the chosen register. Cover
   everything the original covered (N paragraphs in, N paragraphs out). Preserve meaning.
2. Audit. Ask explicitly: "What makes this still read as AI-generated?" Answer in
   brief bullets.
3. Final rewrite. Fix the audit bullets.

### Step 3. Deliver
- Interactive: draft → brief "still-AI" bullets → final rewrite → short change summary.
- Headless / agent chain: return final clean text plus a one-line change summary in a
  trailing HTML comment. No interactive audit prompt.

## VOICE-SAFE vs FULL: The Difference

VOICE-SAFE. Cut the `[SLOP]` tells; DEFER to the writer's signature moves (see
`references/voice-safe-exceptions.md` for how to read a tell that collides with a
deliberate move). Never flatten a deliberate move into "clean" prose. Match the
writer's codified voice from their voice skill's references instead of producing
generic clean output.

FULL. Plain, neutral register IS the correct human voice here. Cut everything in
`references/ai-tells.md`. Add NO personality and NO first person.

## Punctuation preference (NOT a fixed rule)

Some writers retire the em dash entirely; others use it as a breath mark. **Read the
writer's preference** from their workspace (`voiceprint/_work/pile-state.json` →
`preferences.em_dashes`):

- `"drop"` → treat em/en dashes (`—`, `–`), spaced ` — `, and double-hyphen ` -- ` as
  a hard cut in both registers. Replace each, in order: period, comma, colon,
  parentheses, restructure. Final-output guard: scan for `—`/`–`; any hit means not done.
- `"keep"` (default) → leave the writer's dashes alone. Do not impose one writer's
  punctuation taste on another. The em dash is a common AI tell, so still flag a
  *cluster* of dashes alongside other tells — but a writer who keeps dashes keeps them.

VoicePrint never assumes this preference; it is elicited. The rest of the scrub is
unaffected by the setting.

## What NOT to Flag (Don't Gut Real Prose)

A clean human writer can hit several patterns without any AI involvement. NOT reliable
tells on their own: perfect grammar, mixed registers, "bland" prose without specific
tells, formal vocabulary, a single transition word, curly quotes alone, unsourced
claims. Look for **clusters** of tells, not isolated ones.

## Signs of Human Writing (Preserve These)

Lean toward leaving these alone — over-editing destroys what makes prose human, and
for this writer they map onto their signature moves: hyper-specific hard-to-fabricate
detail (a named place, a named person); mixed feelings and unresolved tension; dated,
era-bound references; variety in sentence length; genuine asides and self-corrections;
and any move documented in their voice skill's signature-move table.

## Integration

This skill runs LAST in the chain:

```
storytelling-architecture → substack-value-engine → [your voice skill] → writing-critique → writing-humanity-pass
   (beat SHAPE)               (value GATE)            (every SENTENCE)      (RED-TEAM)        (scrub, LAST)
```

It never overrides a format constraint, a signature move (the voice skill), or a story
beat (`storytelling-architecture`). For neutral text it agrees with plain technical
writing (front-loaded, no slop).

## References

- `references/ai-tells.md`: the ~30 patterns, each tagged `[SLOP]` (always cut) or
  `[CLASH]` (defer in voice-safe to the writer's move). Includes the evidence-quality
  stratification that wires the measurable signals (burstiness, MATTR) to the
  `writing-critique` analyzer.
- `references/voice-safe-exceptions.md`: how to resolve a tell that collides with one
  of the writer's signature moves.

Adapted from [`blader/humanizer`](https://github.com/blader/humanizer) (MIT, v2.7.0),
based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
MIT permits adaptation; attribution retained.

## Success Criteria

- [ ] Punctuation preference honored (drop vs keep), never assumed.
- [ ] Voice-safe scrub preserves every signature move; neutral scrub strips to plain.
- [ ] Meaning preserved; paragraph count matches the original.
- [ ] No tell from `ai-tells.md` survives that is not a protected signature move.
- [ ] Real human prose (no clusters of tells) is left largely alone, not gutted.
