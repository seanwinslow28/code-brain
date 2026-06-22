# Launch pack — Post 1: You Can't Prompt Taste Into a Machine

Everything needed to ship Post 1. Work top to bottom on publish day.

## Status

- **Copy:** ready. Voice chain passed (Do-Not-Promote framing suppressed; gauntlet cheese line swapped; analyzer CV 0.757 / MATTR 0.82, in your baseline; zero em dashes).
- **Tool:** ready. `ships-with-cheese-gauntlet-kit-PUBLIC.md` is the gist source.
- **Image:** prompt ready, render is the one Mac step below (the Cowork sandbox can't reach the Gemini API).

---

## Step 1 — Generate the hero image (pencil-test house style)

New look per the v2 image design (`docs/substack-image-generation-design-2026-05-23.md`): the elegant **pencil-test on cream paper** style from your portfolio, not the grotesque. Concept for Post 1 (LOCKED): the rough, honest guy comes face to face with a glossy motivational-poster impostor of himself in a part-mirror-part-screen — both drawn as goofy cartoon caricatures, and the drawing-style contrast (frazzled rough graphite vs. too-smooth slick) carries the thesis. Amber accent, one watercolor bloom, no desk/blobs/thread, no text. Prompt is saved at `images/hero-prompt.txt`.

**Primary — ChatGPT (made your portfolio anchors, proven for this style):** paste the contents of `images/hero-prompt.txt` into ChatGPT image gen. Iterate conversationally ("warmer bloom," "more construction lines," "calmer thread"). Save the result as `images/hero.png`.

**Scriptable — `openai-image-gen` (GPT Image 2; `--reference` routes to images.edit so it inherits the pencil-test look):**
```bash
cd ~/Code-Brain/code-brain
python3 .claude/skills/openai-image-gen/scripts/generate_image.py \
  "$(cat 'vault/20_projects/substack-studio/01-cant-prompt-taste/images/hero-prompt.txt')" \
  --output "vault/20_projects/substack-studio/01-cant-prompt-taste/images/hero.png" \
  --aspect-ratio 16:9 \
  --quality high \
  --reference ~/Code-Brain/sw-ai-pm-portfolio/reference-images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```
(Needs `OPENAI_API_KEY` in `.env` — it's there.)

If the first render misses, describe a tweak and re-run — don't start from scratch.

---

## Step 2 — Create the gist (the tool)

1. Go to gist.github.com (logged in as seanwinslow28).
2. New gist. Filename: `cheese-gauntlet-prompt-kit.md`.
3. Paste the full contents of `ships-with-cheese-gauntlet-kit-PUBLIC.md`.
4. **Create public gist.** Copy the URL.
5. In `post.md`, replace `https://gist.github.com/REPLACE-WITH-YOUR-GIST-URL` with the real gist URL.

---

## Step 3 — Substack metadata

- **Title:** `You Can't Prompt Taste Into a Machine`
- **Subtitle:** `Raising Claude · Post 1 — why "write like me" prompts hand you a confident stranger`
- **SEO / social description (~155 chars):** `I built a skill to make AI write in my voice. It gave me a confident stranger. Why you can't describe a voice into a machine, and the method that works.`
- **Hero image:** `images/hero.png` (from Step 1).
- **Slug suggestion:** `cant-prompt-taste-into-a-machine` (keeps the primary phrase in the URL).

---

## Step 4 — AEO/GEO report (CITED framework)

```
C — Context clarity:    ⚠️  Strong title + clear thesis; audience (writers/creatives using AI) is implicit.
I — Intent match:       ⚠️  It's a Story; the how-to lives in the kit, not the post (by design).
T — Truth signals:      ⚠️  Experience-based, no cited stats. Fine for a method-story; the measured proof (burstiness) lands in Post 2.
E — Extraction format:  ❌  Pure narrative, no headers/FAQ — intentionally, to protect the cold open.
D — Differentiation:    ✅  "You can't describe a voice, only reject what isn't it" + raising-not-cloning + the Cheese Gauntlet = a named, original method.

AI Citation Readiness: MEDIUM — and that's the right call. Don't genericize the essay.
```

**The strategy:** the narrative stays a narrative. Citability comes from two things that don't touch the body:

1. **The kit IS your extractable asset.** The 3-prompt gist is exactly the structured how-to AI engines cite. Making it public + linked (Steps 2/5) is the AEO win. Most of your citation pull will route through the kit, not the essay.
2. **Metadata carries the searchable question** (Step 3 subtitle/description name the query: "why write-like-me prompts fail").

**Top 3 AI queries this could capture (via the kit + metadata):**

1. "Why don't 'write like me' / humanize prompts work?" → answered by the thesis + the gauntlet method.
2. "How do I get an AI to write in my actual voice?" → answered by the kit's 3 prompts.
3. "What is the Cheese Gauntlet method?" → the named, ownable framework.

**Optional (only if you want it):** a 2-line italic TL;DR under the title — *"The short version: you can't describe your voice to a machine. You can only show it what isn't you, over and over. Here's how."* It feeds AI extraction without harming the cold open since it reads as a deck, not the lede. Your call — the post is strong without it.

**No invented stats.** The post makes no unsourced factual claims to flag (it's a personal method-story). Keep the measurable proof for Post 2 (VoicePrint's burstiness numbers).

---

## Step 5 — Publish sequence

1. ☐ Hero image rendered (Step 1) and reviewed.
2. ☐ Gist created, public, URL copied (Step 2).
3. ☐ Gist URL swapped into `post.md` (replaces the REPLACE-WITH-YOUR-GIST-URL placeholder).
4. ☐ Paste `post.md` body into Substack. Set Title + Subtitle + hero image + SEO description (Step 3).
5. ☐ Publish.
6. ☐ Copy the live Substack post URL.
7. ☐ Swap that URL into the gist (replaces `https://REPLACE-WITH-YOUR-SUBSTACK-POST-URL` in the kit's top line).
8. ☐ Update `post.md` frontmatter: `status: published`, `publish_date: <today>`, drop the launch_blockers.
9. ☐ Update the series README queue row for Post 1 to ✓ published.

Then Post 2 (VoicePrint) is next in the queue — it needs the voice chain + its own hero.
