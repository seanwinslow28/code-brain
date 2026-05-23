---
type: handoff-prompt
project: prj-job-hunt-2026
created: 2026-05-23
ai-context: |
  Kickoff prompt for a fresh Claude Code session. Builds a new universal-purpose
  Skill at .claude/skills/openai-image-gen/ that mirrors the existing
  .claude/skills/gemini-image-gen/ skill but targets OpenAI's latest image model.
  Born 2026-05-23 after Sean validated that OpenAI's image generator outperformed
  Nano Banana 2 on the Steadman-gonzo aesthetic for his substack post headers.
  The new skill becomes the canonical image-gen pipeline going forward; the
  existing gemini-image-gen stays available as a fallback / comparison surface.
related:
  - "[[.claude/skills/gemini-image-gen/SKILL]]"
  - "[[.claude/skills/skill-system-mastery/SKILL]]"
  - "[[docs/substack-image-generation-design-2026-05-23]]"
---

# Kickoff prompt — Build the `openai-image-gen` Skill

> **How to use:** copy the entire `BEGIN PROMPT` → `END PROMPT` block below into a fresh Claude Code session in this repo. The session will research, build, test, and document the skill. Estimated session length: 60–90 minutes. Estimated API cost: $0.20–0.50 (a few real test generations).

---

## BEGIN PROMPT

You are building a new universal-purpose Claude Code Skill at `.claude/skills/openai-image-gen/` that wraps OpenAI's latest image-generation API. The skill mirrors the existing `.claude/skills/gemini-image-gen/` skill in structure, CLI surface, and the integration with the `image-generator-prompt-science` 7-Layer Prompt Framework — but targets OpenAI instead of Google Gemini. Build it using the `skill-system-mastery` skill (load it before writing any skill files; it enforces the YAML frontmatter contract and triggering-description best practices).

**Why this skill exists:** Sean tested manually against ChatGPT's image generator and OpenAI's outputs landed better than Nano Banana 2 for his use case (Substack post headers in Ralph Steadman gonzo aesthetic with style-reference image attached). The new skill makes that workflow scriptable + repeatable + agent-callable. Substack post headers are the primary use case but the skill must be universal — usable for photorealism, illustration, product shots, infographics, headshots, anything that isn't pixel art (pixel art already has its own skill).

### Step 1 — Required reading (do this first, in this order)

1. **`.claude/skills/skill-system-mastery/SKILL.md`** — load this skill first so you build the new skill correctly. Pay attention to the description-field contract: descriptions must include trigger phrases users will actually type ("generate an image", "create a picture", "make a portrait", "render", etc.).

2. **`.claude/skills/gemini-image-gen/SKILL.md`** — the structural template you are mirroring. The new openai-image-gen skill follows this exact shape: top-level `SKILL.md` + `references/` subdirectory + `scripts/generate_image.py` CLI.

3. **`.claude/skills/gemini-image-gen/references/nano-banana-2-capabilities.md`** — the model-specific reference doc you are mirroring. Your equivalent will be `references/openai-image-capabilities.md` covering OpenAI's latest model.

4. **`.claude/skills/gemini-image-gen/scripts/generate_image.py`** — the script you are mirroring. Same flags: positional `prompt`, `--output / -o`, `--aspect-ratio` (or whatever the OpenAI equivalent is — research this), `--reference / -r`, `--env-file`, `--model`. Same UX: load env from `.env`, generate, save to disk, print confirmation.

5. **`.claude/skills/image-generator-prompt-science/SKILL.md`** (if it exists) — the 7-Layer Framework that both image-gen skills delegate to. Don't duplicate it; reference it.

6. **`docs/substack-image-generation-design-2026-05-23.md`** — Sean's design doc for the substack-image-gen pipeline. The new skill is the engine that replaces NB2 in this pipeline. After build, the design doc's "Workflow → Invocation" section will need a one-line addition pointing at the new script path; this is part of your doc-update work in Step 5.

7. **`CLAUDE.md`** (repo root) — read the "Non-Negotiable Rules" + the "Mandatory doc updates" rule at the bottom of "When Modifying" (you MUST update CHANGELOG.md, CLAUDE.md, README.md when shipping a new Skill).

### Step 2 — Research mission (DO NOT skip; do not trust training data alone)

OpenAI's image API has moved rapidly. Sean believes the current model is "Image 2" but isn't sure of the exact name. **Verify the current state via `WebFetch` against `docs.openai.com` and `platform.openai.com/docs` before writing the capabilities doc.** Specifically research:

1. **Current canonical model name** as of 2026. Candidates to verify: `gpt-image-1`, `gpt-image-1-mini`, `gpt-image-1.5`, `gpt-image-2`, or some other latest name. Confirm via the OpenAI docs the model ID string the API actually accepts. Note: as of January 2026 training data, `gpt-image-1` was the GA model (released April 2025) with `gpt-image-1-mini` cheaper variant (Oct 2025). Newer versions may have shipped — verify.

2. **API endpoint + request shape**: `POST /v1/images/generations` (the basic case) — verify the request schema, response schema, and what authentication header to use. Confirm the SDK pattern (`openai` Python package, current major version).

3. **Reference / style-transfer image support**: critical — Sean's primary use case is passing a Ralph Steadman reference image and getting style-matched output. OpenAI's image API historically supports this via the `images/edits` endpoint or via multi-modal input. Confirm:
   - Which endpoint supports reference-image style transfer
   - File-size limits, supported formats (PNG, JPEG, WebP)
   - Whether multiple references can be passed in one call
   - Whether style-transfer works via the standard model or a different model variant

4. **Supported sizes / aspect ratios**: confirm exact pixel dimensions supported (1024×1024, 1024×1536, 1536×1024, 1792×1024, etc.) and which the latest model actually accepts. Substack header target is 16:9 (1456×816 native or upscaled from a 16:9 generation) — verify the closest supported size.

5. **Quality / detail tiers**: gpt-image-1 historically had `low` / `medium` / `high` quality tiers with different pricing. Confirm current options and their cost-per-image.

6. **Prompt rewriting behavior**: OpenAI's image models have historically auto-rewritten user prompts before generation, which can degrade fidelity. Research whether the latest model still does this and whether there's a flag to disable it (e.g., `style: natural` vs `style: vivid` on DALL-E 3; some current models support a `prompt_revision` or similar control). If the rewriting is unavoidable, document the workaround patterns (e.g., explicit "Use this prompt exactly:" preamble).

7. **Multi-turn / conversational editing**: does the latest model support iterative editing of a previously-generated image (analogous to Nano Banana 2's conversational editing strength)? If yes, document how (likely via the `images/edits` endpoint with the prior output passed as the base image).

8. **Negative prompting**: how do you tell the OpenAI model what NOT to render? Plain-English negatives in the prompt, or a dedicated parameter?

9. **Rate limits + safety filters**: document the current rate-limit tiers + how the safety filter manifests (which error code / response shape to handle gracefully).

10. **Pricing table**: per-image cost at each size/quality combination, and the input-token pricing if the model bills the prompt separately.

**Research method:** use `WebFetch` to read OpenAI's official docs, the OpenAI cookbook (`github.com/openai/openai-cookbook`), and the OpenAI Python SDK's GitHub readme. Use `WebSearch` if the docs are stale or you need release-note timelines. Do NOT rely on third-party blog posts as primary sources — go to the OpenAI docs themselves.

### Step 3 — Build mission

Mirror the file structure of `.claude/skills/gemini-image-gen/` exactly:

```
.claude/skills/openai-image-gen/
├── SKILL.md
├── references/
│   ├── openai-image-capabilities.md       (mirror of nano-banana-2-capabilities.md)
│   └── universal-prompt-templates.md      (mirror — 10 ready-to-use templates,
│                                           or symlink to the gemini one if templates
│                                           are model-agnostic)
└── scripts/
    └── generate_image.py                  (mirror of gemini's script with the
                                            same CLI surface, OpenAI SDK underneath)
```

**SKILL.md requirements:**
- YAML frontmatter with `name: openai-image-gen` and a `description:` that includes natural-language triggers users will type. The gemini-image-gen description is your template — mirror its trigger word patterns ("generate image", "create image", "make a picture", "render", etc.) so the right skill loads when Sean asks for an image. The skill-system-mastery skill enforces this contract — follow it.
- **Disambiguation from gemini-image-gen**: both skills can generate the same types of images. Add explicit "When to use this vs gemini-image-gen" guidance: openai-image-gen is the default for editorial illustration + style-transfer-via-reference workflows (per Sean's 2026-05-23 validation); gemini-image-gen remains available for high-volume / cost-sensitive batches and conversational-editing-heavy workflows.
- Same section structure as gemini's SKILL.md: Purpose / When to Use / Examples / Core Workflow (5-step pipeline) / Aspect Ratio Selection Guide / Script Usage / Error Handling / Cross-References / Success Criteria / Copy/Paste Ready.

**Script requirements (`scripts/generate_image.py`):**
- Same CLI signature as `gemini-image-gen/scripts/generate_image.py` — keep the surface identical so existing callers and docs can switch by just renaming the script path.
- Required flags: positional `prompt`, `--output / -o`, `--aspect-ratio` (mapped internally to the closest OpenAI-supported size), `--env-file` (defaults to `.env`), `--reference / -r` (path to a style-reference image; if present, route to whichever OpenAI endpoint supports style transfer).
- Optional flags: `--model` (default to the latest OpenAI image model the research confirmed), `--quality` (low/medium/high if supported), `--n` (number of variants if supported).
- Load `OPENAI_API_KEY` from `--env-file` and validate at startup. Fail with a clear error message if missing.
- Print model used, aspect ratio, output path, and prompt preview before generating (mirror gemini script's stdout). Print save confirmation + file size after success.
- Save output as PNG to the specified path. Handle the case where the API returns base64 vs URL (research will clarify which the latest model uses).
- Cleanly handle: missing API key, safety-filter blocks (400/422 responses), rate-limit (429), invalid prompt, network failure. Mirror the gemini script's error-message style.

**Reference doc requirements (`references/openai-image-capabilities.md`):**
- Mirror the structure of `nano-banana-2-capabilities.md`: Model Overview / Capabilities Matrix / Technical Specifications / API Configuration / Prompting Best Practices / Style-Specific Tips / Known Limitations / Cost Optimization.
- Populate with the research from Step 2 — model ID, endpoint, sizes, quality tiers, pricing, reference-image support, rate limits, safety filters, prompt-rewriting behavior, conversational-edit support.
- Include a head-to-head section: "OpenAI [model] vs Nano Banana 2 — when to choose which." This is load-bearing for Sean's workflow because he now has both options and needs a fast decision rule.

**Universal-prompt-templates doc:**
- If the gemini skill's `universal-prompt-templates.md` is model-agnostic (templates that work for both), evaluate whether to symlink or copy. If model-specific (e.g., calls out NB2 quirks), produce an OpenAI-tuned version.

### Step 4 — Test mission (REAL API CALLS — budget ~$0.20)

After the skill is built, validate it against Sean's actual use case. Two test generations:

**Test 1 — Sedaris voice on "The Night My Vault Said Nothing":**
- Use the exact prompt from `docs/substack-image-generation-design-2026-05-23.md` "First test (2026-05-23) — Sedaris v2 LOCKED as canonical" section (it's quoted verbatim in `vault/.../substack-drafts/images/` design context — look at the prompt that produced `2026-05-10-the-night-my-vault-said-nothing-header.png`).
- Reference image: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/substack-image-generation-references/substack-image-generation-ref-3.png` (Walter White Steadman portrait).
- Output: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/images/2026-05-10-the-night-my-vault-said-nothing-header-openai-test.png` (separate filename so it doesn't clobber the canonical gemini-generated image; Sean compares both).

**Test 2 — Sean Mode on "Access Over Meaning" manifesto:**
- Use the exact prompt from the same design doc's Sean Mode section.
- Reference image: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/substack-image-generation-references/substack-image-generation-ref-1.png` (maximal Steadman anchor — the one Sean confirmed works in ChatGPT for both use cases).
- Output: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/images/2026-06-19-meaning-over-access-header-openai-test.png`.

After both generations, view both PNGs with the `Read` tool. Compare to the existing gemini-generated versions in the same folder. Write a short critique in the Step 5 commit message (one paragraph per test) noting what landed better, worse, or differently. This is the validation that the new skill matches Sean's ChatGPT-side experiments.

### Step 5 — Documentation + commit

Mandatory per the repo's `CLAUDE.md` "When Modifying" rule (creating a new skill triggers all three doc updates):

1. **`CHANGELOG.md`** — add a new version entry (probably `4.1.2` if `4.1.1` is the last shipped version; check the current latest). Capture: what the skill does, why it was built (OpenAI image-gen outperformed NB2 on Sean's Steadman-aesthetic Substack workflow on 2026-05-23), the 2 test generations + which lands better, the model name + version researched, the script CLI surface mirrors gemini-image-gen.

2. **`CLAUDE.md`** — bump the skill count (currently 118; new total 119). Update any other counts that change (likely just the skills total).

3. **`README.md`** — bump skill count if the count is surfaced there. Update any "image generation" mentions if applicable.

4. **`docs/substack-image-generation-design-2026-05-23.md`** — under "Workflow → Invocation", add a one-line note that openai-image-gen is now the primary script and gemini-image-gen is the fallback. Don't rewrite the doc; just add the routing line.

5. **Commit** with a message like `feat(skills): openai-image-gen — OpenAI image generation wrapper mirroring gemini-image-gen`. Don't push.

### Step 6 — Definition of done

The session is complete when:

- [ ] `.claude/skills/openai-image-gen/SKILL.md` exists with valid YAML frontmatter (per skill-system-mastery contract) and a description that triggers naturally on user requests like "make an image of X" / "generate a picture of X" / "render X" / "create an illustration of X"
- [ ] `.claude/skills/openai-image-gen/references/openai-image-capabilities.md` exists with researched (not hallucinated) model facts: confirmed model ID, supported sizes, pricing table, reference-image support documented, rate limits documented, head-to-head comparison vs NB2 included
- [ ] `.claude/skills/openai-image-gen/scripts/generate_image.py` exists with the same CLI surface as the gemini version; runs successfully against `OPENAI_API_KEY` from `.env`
- [ ] Test generations 1 and 2 produced real PNG outputs in `vault/.../substack-drafts/images/` with the `-openai-test` suffix
- [ ] Written critique comparing OpenAI output to Gemini output for both tests (in the commit message body or as a small note in the design doc)
- [ ] `python3 scripts/validate.py` runs clean (≤60 warnings / 0 errors) — same threshold as the existing repo baseline
- [ ] CHANGELOG / CLAUDE / README updated per the mandatory doc rule
- [ ] One commit on `main` (or current branch) with the work; do NOT push to remote (Sean reviews before push)

### Anti-patterns — do NOT do these

- **Do NOT skip the research step** and rely on training data for OpenAI's model name + API shape. OpenAI ships fast; the docs are the only source of truth.
- **Do NOT copy gemini-image-gen's text verbatim** into the new skill. Mirror the structure but write fresh content. Identical text confuses the description-based trigger router and creates maintenance burden.
- **Do NOT bypass `skill-system-mastery`.** Load that skill first. It enforces the YAML frontmatter contract that makes the skill discoverable.
- **Do NOT hardcode the OpenAI API key anywhere.** Always load from `.env` via `--env-file`. The `.env` file is already gitignored.
- **Do NOT commit the test PNGs to git if they're large.** Add `*-openai-test.png` to a `.gitignore` rule in the images/ folder if needed, OR commit them deliberately as "what shipped, what didn't" reference (mirror what Sean already did with the v1-superseded.png file). Sean's call — flag this in the commit message and ask if uncertain.
- **Do NOT push to remote.** Local commit only; Sean reviews first.
- **Do NOT take more than ~90 minutes.** If research is dragging past 30 min, ship the skill with the best-known model facts + an explicit "verify next session" note in the capabilities doc, and move on. Perfect is the enemy of shipped.
- **Do NOT add unrelated features** (no batch generation, no caching layer, no parallel generation, no fancy CLI flags beyond what the gemini script has). Mirror the existing surface; expand later if Sean asks.

### Context Sean is NOT bringing to the new session

You will not have:
- The conversation history from this Cowork session
- The 4-Q context about the substack workflow
- Sean's voice-mode-aware Gonzo aesthetic mapping (it's in the design doc — read it)

You WILL have:
- This kickoff prompt verbatim
- Full read/write/bash/edit tool access on the repo
- Network access for WebFetch + WebSearch (use them for the research step)
- The `.env` file with `OPENAI_API_KEY` already set

### One last thing

Sean is mid-job-hunt sprint (post-Block layoff, 8-week sprint through ~2026-07-04). His default mode is "minimize context-switching cost." The new skill must be drop-in usable in his next Substack-post session — meaning if Sean says "generate the header for my next post," the skill must trigger naturally from natural-language description-based skill routing, not require him to remember a special command. The description field on `SKILL.md` is the single most important field for this — invest in it, copy the gemini description's trigger patterns, then test that it actually loads when you mention "generate an image" in a fresh session.

End of mission. Begin with Step 1.

## END PROMPT

---

## Notes for Sean (not part of the prompt above)

**Expected research findings the new session should hit:**
- Model ID: probably `gpt-image-1` or `gpt-image-1.5` (latest as of training cutoff was `gpt-image-1`; there may be newer variants since)
- Endpoint: `/v1/images/generations` for basic, `/v1/images/edits` for reference-image style transfer
- Sizes: typically 1024×1024, 1024×1536, 1536×1024 (and possibly 1792×1024 for 16:9)
- Pricing: roughly $0.04–0.19 per image depending on size and quality tier
- Style-reference workflow: probably via the `images/edits` endpoint with the reference as `image` parameter

**Cost ledger to plan for:**
- Research: $0 (just WebFetch reads)
- Test generation 1 (Sedaris): ~$0.04–0.19
- Test generation 2 (Sean Mode): ~$0.04–0.19
- Total session: ~$0.10–0.40

**Where the new session's commit will land:**
On whatever branch is checked out at session start. If you're on `main` (most likely), the commit lands on main. The session will NOT push — you review locally first.

**Time budget for the new session:** 60–90 min. If it's running long, the prompt's anti-pattern section tells the session to ship with partial research + a "verify next session" note rather than spin on perfection.

**Carry-forward after the new session ships:**
1. Compare the OpenAI test outputs against the Gemini canonical headers
2. If OpenAI wins on both, regenerate the canonical headers via the new skill and update the design doc to route through openai-image-gen as primary
3. If results are mixed, document the routing rule (which voice modes go to which skill) in the design doc

**Roadmap continuation:** after this skill ships, we return to the roadmap per your direction. Next imminent items (from earlier in the session): Substack Post 1 publish (gates Post 3 cadence), Task 19 Step 1+1b (interview_grader profile + rubric, Monday 5/26 test day), Friday retro at 4:30 PM today.
