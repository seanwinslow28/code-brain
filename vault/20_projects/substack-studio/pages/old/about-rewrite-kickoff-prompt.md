# PROMPT — paste into a fresh Cowork session to write the Pencil & Prompt "About" page

Copy everything below the divider.

---

You're collaborating with **Sean Winslow** on his Substack, **Pencil & Prompt** ("Teach the machine your taste, one creative job at a time"). This session's job: **write a great, UNIQUE About page that stands on its own as a personal piece.** Be a real thinking partner, brainstorm one question at a time before writing, generate options, and pressure-test every idea against "why is this Sean, not a template?" Be concise and direct; Sean is a creative technologist (animation, writing, character design) who builds with an agent fleet and wants the why and the how.

## Skills to use (in this order)
1. **`superpowers:brainstorming`** — run the collaboration. Ask ONE question at a time, scope the About's shape with Sean, and get his approval on a short skeleton BEFORE drafting. (That skill's hard rule: no draft until he approves a design.)
2. Then the **voice chain, in order, to write it:** `voiceprint:substack-value-engine` → `voiceprint:storytelling-architecture` → `anthropic-skills:writing-voice-modes` (Sean Mode) → `voiceprint:writing-critique` → `voiceprint:writing-humanity-pass`. (If `anthropic-skills:writing-voice-modes` isn't invocable, read it from disk at `.claude/skills/writing-voice-modes/SKILL.md`.)
3. Optional while scoping: `sw-creative-toolkit:storytelling` for narrative-shape options (Before-After-Bridge, etc.).

## Read first
- Positioning source of truth: `vault/20_projects/substack-studio/POSITIONING-AND-EDITORIAL-SPEC.md`
- The sibling **Start Here** page — READ IT TO DIFFERENTIATE FROM, do not borrow its lines or structure: `vault/20_projects/substack-studio/pages/start-here.md`
- The two About drafts that missed (read so you don't repeat them): `vault/20_projects/substack-studio/pages/about.md` and `vault/20_projects/substack-studio/pages/about-council-version-short.md`
- Voice: `.claude/skills/writing-voice-modes/SKILL.md` (Sean Mode + the House Style grit register + the signature-moves table) and its calibration anchor `.claude/skills/writing-voice-modes/references/voice-samples.md` (read the newest section, the "Start Here PRIME ANCHOR").

## The locked opening (the About MUST start with this, verbatim — it's Sean's own)
> I was a husky youth with an appetite for stupidity. I'd plant myself three feet from a static TV with an extra large bowl of Cinnamon Toast Crunch and mainline whatever the networks were pushing. Saturday mornings were a sacrament. My parents' living room was the church. Years went by and I used that same appetite to teach myself animation, write multiple screenplays, and piece together a few short films.

That paragraph is the through-line: the **same appetite** is what makes AI a natural next chapter, not a non-sequitur. Build everything after it so AI enters as the continuation of that appetite.

## The job
- **Short:** ~250-350 words, the Substack-standard About length (see examples). First person.
- **A standalone PERSONAL piece, distinct from Start Here.** About = who Sean is and the journey (the husky TV kid → self-taught animation, screenplays, short films → AI shows up → he points the same appetite at teaching the machine his taste and builds anima → who that makes him). **Start Here already carries the manifesto, the full thesis argument, and the three-format list. So About must NOT re-argue the thesis or re-list the formats the way Start Here does.** A one-line gesture at "what I do here" is fine; the About's job is the PERSON, not the pitch.
- **Fold AI in naturally, in order.** The exact failure to avoid (it's why the last draft was rejected): a paragraph ended on "a fleet of AI agents," then the next abruptly reset to "Then AI showed up and everyone lost it," a chronology whiplash, because the fleet IS the AI. Introduce AI once, in sequence, as the next thing the appetite chased.
- **anima** gets a light, sideways mention (he built it; the human owns the timing/casting/taste, the agents propose and don't decide), never its full story.
- **Credibility shown sideways, never claimed.** The films, Break Time, the screenplays, anima, the fleet are proof he did the work, never a resume line or an "I'm an expert."

## Real facts you may use (invent nothing beyond these)
- Self-taught animator and filmmaker; first animated comedy short is **Break Time**.
- Wrote **eleven screenplays** in his twenties.
- Built **anima**, a 2D-animation pipeline where the human owns timing, casting, and taste, and the agents do the cheap parallel work and propose, never decide.
- Links: YouTube **youtube.com/@seanpwinslow** (real channel tagline, usable: "I like getting creative with AI and making silly cartoons"), GitHub **github.com/seanwinslow28**, site **seanwinslow.com**. Flagship link is a placeholder: **[Take Two #1]**.
- Do NOT invent Break Time's plot, or any personal backstory beyond the locked opening. No sympathy backstory, no job-hunt ask.

## Voice rules
No em dashes, ever. Dive-bar grit (bodily, blue-collar, profane when it earns it). Anti-hype (never sound like an AI hype-bro). References woven as diction are good and Sean's natural density runs hot; avoid only the "that reminds me of the time… cut to [bit]" gorging cadence. The closer must be the strongest line and must never ask the reader for anything.

## Examples to aim for (short, personal, voice-forward — fetch them, or Sean can paste them as markdown)
- `https://hannahstulberg.substack.com/about` — clean: name + credibility sideways, POV stated as a belief, "that's what this is about," a sign-off that echoes the publication name.
- `https://liantomato.substack.com/about` — the most PERSONAL and voice-forward model: raw, funny, self-deprecating, casual "what you'll get" bullets, a darkly funny sign-off. This is the tonal North Star for how personal Sean can go.
- `https://lifeinthemachine.substack.com/about` — same lane (animation + AI + the human side): credits as credibility → the threat → the mission → "let's figure this out together."

## Method
1. `superpowers:brainstorming`: scope the shape with Sean one question at a time — how personal/funny to go (à la Lian), whether to include any "what you'll find" gesture or keep it pure bio, and the sign-off. Build a short skeleton around the locked opening. Get his approval.
2. Run the voice chain to draft it.
3. Present the draft and iterate (Sean often rewrites by hand — fold his edits back into `voice-samples.md` as a calibration anchor).
4. On his approval, save the final to `vault/20_projects/substack-studio/pages/about.md` (prior drafts are preserved in git history and `pages/_council/`).

Start by reading the context and the locked opening, then open the brainstorm with your first question.
