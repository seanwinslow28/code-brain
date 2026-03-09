# Writing Voice Modes — Integration Rules + Skill Upgrade Plan

---

## PART 1: Integration Rules (Add to SKILL.md)

Insert this section after "Content Type → Mode Mapping" and before "Complementary Technique Pairs":

```markdown
## Integration Rules

This skill controls HOW writing sounds. `creative-writing` controls FORMAT (structure, word count, platform constraints). `technical-writing` controls CLARITY (audience awareness, progressive disclosure, front-loaded conclusions). When loaded together:

**Voice modes operate WITHIN format constraints, not over them.**
- If `creative-writing` says a Twitter thread is 5-10 tweets at 280 chars max, Gonzo mode doesn't get to blow past that. It adapts its cold open and escalation loop to fit the constraint.
- If `technical-writing` says front-load the conclusion, Beat Flow mode doesn't bury it under a sensory cascade. It delivers the conclusion first, THEN runs the cascade as supporting texture.

**When modes and formats conflict, resolve by content type:**

| Conflict | Resolution |
|----------|-----------|
| Mode wants a long cold open, format says hook in 1-2 sentences | Compress the cold open into 1-2 sentences. Gonzo can cold-open in 12 words: "I DEPLOYED TO PRODUCTION at 11:47 PM on a Wednesday." |
| Mode wants flowing rhythm, format says scannable with headers | Use the mode's rhythm WITHIN each section. Headers provide structure; voice lives between them. |
| Mode wants humor, format says professional (API docs, runbooks) | Dial to 20-40%. Dry wit in examples and asides. Never in the critical path (commands, warnings, steps). |
| Mode wants sensory detail, format says brevity (tweet, Slack) | One sensory image maximum. Pick the jewel center. Cut the cascade. |
| Mode wants a refrain, format is short-form | Deploy the refrain twice maximum (setup + payoff). Three needs runway. |

**The one exception:** Personal essays and blog posts on Sean's own site. Here, voice modes lead and format follows. The mode shapes the structure. `creative-writing` provides the skeleton (hook, sections, closer), but the mode can reshape that skeleton if the piece demands it.
```

---

## PART 2: Script-Writing Skill Upgrade Plan

### Why Script-Writing Benefits Most

Sean's screenwriting background is *load-bearing* in his voice — the cut-to, hard juxtaposition, scene kicks, and comedic timing all come from screenwriting instincts. The current `script-writing` skill covers industry-standard format and beat sheets, but it doesn't have the same depth of CRAFT mechanics that writing-voice-modes now has. The upgrade would add:

- Dialogue craft mechanics from studied masters (not just "write natural dialogue")
- Scene construction techniques (how to build tension, land a joke, execute a pivot)
- Animation-specific storytelling patterns (Sean's shorts are 2D comedy)
- Personal style calibration (Sean's screenplay voice vs. generic screenplay format)

### Research Approach (Same Pipeline)

**Authors/Filmmakers to Study:**

| Master | Why | What to Extract |
|--------|-----|-----------------|
| **Charlie Kaufman** | Meta-narrative, self-referential humor, emotional gut punches disguised as absurdism. Closest to Sean's "humor as trojan horse." | Dialogue that sounds natural but is structurally precise. Scene transitions that recontextualize everything before them. |
| **Taika Waititi** | Comedy-drama balance in visual storytelling. Deadpan delivery + genuine emotion. Successfully does what Sean wants to do: funny AND meaningful. | How jokes live inside dramatic scenes without undermining them. Improvisation-feeling dialogue that's actually scripted. Tonal control. |
| **Hayao Miyazaki** | Sean already has Studio Ghibli as a reference point (it literally appears in his origin story). Master of visual storytelling, pacing, and quiet emotional moments in animation. | Scene construction without dialogue. Pacing in animation (when to slow down). How environment tells story. |
| **Greta Gerwig** | Naturalistic dialogue, ensemble character work, personal storytelling at scale. Her writing process (extensive rewriting, emotional authenticity) mirrors Sean's iterative approach. | How personal experience becomes universal narrative. Dialogue rhythm — overlapping, incomplete, emotionally loaded. |
| **Bo Burnham** | One-person creative production, meta-commentary on the creative process itself, comedy that becomes devastating. His work bridges standup, film, music, and writing. | Structure of comedy specials as narrative (Inside is essentially a one-man animated short in live action). How self-awareness becomes a storytelling tool, not just a defense mechanism. |

**Alternative/Additional Candidates:**
- **Wes Anderson** — Visual comedy, symmetry, deadpan. Useful for Sean's animation style direction.
- **Tina Fey / Donald Glover** — Comedy writing rooms, sitcom structure, rapid-fire dialogue.
- **Pixar Story Team** (as a collective) — Beat structure, emotional arcs, the "Pixar rules of storytelling."

### Pipeline

1. **Perplexity Deep Research** — 4-5 prompts (one per filmmaker), focused on SCREENPLAY CRAFT not biography
2. **NotebookLM** — 4-5 notebooks with custom analyst roles (Dialogue Analyst, Scene Construction Analyst, etc.)
3. **Cross-synthesis** — One notebook combining all profiles
4. **Compile** → `ref-screenplay-mechanics-research.md`
5. **Claude Code interview** — Calibrate to Sean's screenplay instincts (his 5 shorts, his cut-to signature, his comedy timing)
6. **Writing exercises** — Write the same scene in different filmmaker modes
7. **Skill upgrade** — Rebuild `script-writing` SKILL.md with mode-aware craft mechanics

### What Changes in script-writing

| Current | Upgraded |
|---------|----------|
| Industry-standard format reference | Kept (format is format) |
| Generic beat sheet (6-8 beats) | **Filmmaker-influenced beat patterns** (Kaufman's non-linear, Waititi's comedy-drama weave, Miyazaki's quiet pacing) |
| Basic dialogue rules | **Dialogue craft modes** extracted from master research |
| Production handoff tables | Kept + enhanced with animation-specific notes |
| No personal calibration | **Sean's screenplay voice profile** (cut-to, hard juxtaposition, humor-as-trojan-horse in scene form) |

---

## PART 3: Other Skills That Benefit From This Approach

The "study masters → extract mechanics → calibrate to Sean" pipeline works for any skill where CRAFT QUALITY matters more than FORMAT COMPLIANCE. Here's the full audit:

### High-Value Candidates (Clear ROI)

| Skill | Masters to Study | What It Adds |
|-------|-----------------|--------------|
| **script-writing** | Kaufman, Waititi, Miyazaki, Gerwig, Burnham | Dialogue craft, scene construction, personal screenplay voice |
| **creative-writing** | Already done (Kerouac, Thompson, Vonnegut, Sedaris feed into this via voice-modes pairing) | Could add FORMAT-specific masters: newsletter writers (Craig Mod, Robin Sloan), essayists (Roxane Gay, Ta-Nehisi Coates) |
| **creative-director** | Saul Bass (visual identity), Paula Scher (bold typography), Hayao Miyazaki (visual storytelling), Dieter Rams (functional design) | Design critique vocabulary, visual direction principles calibrated to Sean's "tech-filled art museum" aesthetic |
| **animation-pipeline** | Richard Williams (animation principles), Glen Keane (character animation), Masaaki Yuasa (experimental 2D), Don Hertzfeldt (indie animation + festival strategy) | Frame-level craft decisions, movement vocabulary, style-specific pipeline adjustments |

### Medium-Value Candidates (Worth Doing Eventually)

| Skill | Masters to Study | What It Adds |
|-------|-----------------|--------------|
| **prd-generator** | Shreyas Doshi (product thinking), Lenny Rachitsky (PM communication), Julie Zhuo (design-informed PM) | PRD writing that's persuasive, not just complete. How great PMs frame problems. |
| **technical-writing** | Stripe docs team (developer experience), Fly.io blog (technical + personality), Julia Evans (zines as technical communication) | Technical writing that people actually enjoy reading. How to add personality without sacrificing precision. |
| **stakeholder-update** | Amazon 6-pager format (narrative structure), Basecamp's Shape Up (pitch format), military briefing structure (BLUF) | Stakeholder comms that are compelling, not just informative. |

### Low-Value / Skip

| Skill | Why Skip |
|-------|----------|
| `config-settings`, `mcp-architecture`, `supabase-backend` | Pure technical reference — craft quality doesn't apply. Format compliance is what matters. |
| `jira-automation`, `zapier-mcp-automation` | Tool operation skills. No "voice" dimension. |
| `health-habits`, `personal-finance` | Data-driven skills. Craft research wouldn't improve the output. |
| `vault-read-write`, `vault-architecture` | Infrastructure skills. The vault doesn't need personality. |

### Recommended Sequence

Based on impact to Sean's career trajectory and project pipeline:

1. **script-writing** — Directly feeds animation pipeline → festival submissions → creative industry transition. Highest career ROI.
2. **animation-pipeline** — Pairs with script-writing upgrade. Together they cover the full creative production workflow.
3. **creative-director** — Visual direction principles feed into portfolio site design, 16BitFit art direction, and animation style development.
4. **creative-writing** (format masters) — Add newsletter/essay format masters to complement the existing voice modes. Lower urgency since voice-modes already handles the "sound" dimension.
5. **technical-writing** (personality masters) — Nice-to-have for portfolio blog posts and docs. Not urgent.
