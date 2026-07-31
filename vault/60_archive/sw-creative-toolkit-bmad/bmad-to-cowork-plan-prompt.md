# Prompt: BMAD CIS → Claude Cowork Plugin/Skill Conversion Plan

> **How to use:** Paste the contents of the `<prompt>` block below into a Claude Code session in **plan mode** (Shift+Tab to toggle). Claude Code will read the referenced files, do the external research, and return a plan of action — without writing any code yet.

---

<prompt>

<role>
You are a senior prompt engineer and Claude plugin architect. You specialize in (1) extracting reusable cognitive techniques from agent-based frameworks and (2) translating them into Anthropic-native primitives — Claude Skills (SKILL.md) and Claude Cowork plugins (skills + commands + MCPs bundled together). You write plans that an implementer can execute without ambiguity.
</role>

<goal>
Produce an actionable conversion plan that turns the BMAD Creative Intelligence Suite (CIS) agents into a coherent set of Claude Skills (and optionally one Cowork plugin that bundles them) — preserving the *techniques* the agents use, not their personas. The user is a Product Manager who wants these available in future Cowork sessions for product management and creative work. Personas are nice-to-have flavor; the **methodologies, frameworks, prompts, and step-by-step workflows are the asset.**

Do NOT write any plugin code, SKILL.md files, or manifests in this pass. Plan only. Implementation will happen in a follow-up session.
</goal>

<inputs_to_analyze>
Read every file under these three roots, in this order:

1. **Example BMAD skill (already partially converted)** — study the structure carefully, this is the closest existing pattern to mimic:
   - `/Users/seanwinslow/Code-Brain/BMAD/.agent/skills/bmad-cis-agent-brainstorming-coach/SKILL.md`
   - `/Users/seanwinslow/Code-Brain/BMAD/.agent/skills/bmad-cis-agent-brainstorming-coach/customize.toml`

2. **CIS reference library** — the source-of-truth for techniques, frameworks, workflows, and the agent roster:
   - `/Users/seanwinslow/Code-Brain/BMAD/_bmad/cis/bmad-cis-creative-intelligence-suite/ref-bmad-cis-agents.md` (start here — gives the agent inventory)
   - `ref-bmad-cis-brainstorming-techniques.md`
   - `ref-bmad-cis-innovation-frameworks.md`
   - `ref-bmad-cis-design-thinking-phases.md`
   - `ref-bmad-cis-apply-design-thinking.md`
   - `ref-bmad-cis-craft-compelling-story.md`
   - `ref-bmad-cis-develop-innovation-strategy.md`
   - `ref-bmad-cis-run-brainstorming-session.md`
   - `ref-bmad-cis-solve-complex-problems.md`
   - `ref-bmad-cis-workflows.md`
   - `ref-bmad-cis-how-to-guides.md`
   - `ref-bmad-cis-getting-started.md`
   - `ref-bmad-cis-understanding-creative-intelligence.md`
   - `ref-bmad-cis-welcome.md`
   - `ref-bmad-cis-configuration.md`

3. **Cowork plugin/skill reference docs** — the platform constraints:
   - `/Users/seanwinslow/Code-Brain/BMAD/_bmad/cis/docs/ref-claude-cowork-manage-org-plugins.md`
   - `/Users/seanwinslow/Code-Brain/BMAD/_bmad/cis/docs/ref-claude-cowork-use-plugins.md`
   - Any screenshots in `/Users/seanwinslow/Code-Brain/BMAD/_bmad/cis/docs/` if they appear relevant
</inputs_to_analyze>

<external_research>
After reading the local files, do web research to fill gaps. Search and read the official sources — do not rely solely on training data:

1. **Anthropic Skills documentation** — what makes a SKILL.md auto-load reliably, YAML frontmatter rules, progressive disclosure, the `references/` and `assets/` pattern, and how skills are discovered. Look for `docs.claude.com` pages on Agent Skills and the `anthropics/skills` GitHub repo.
2. **Claude Cowork plugin format** — manifest structure, how plugins bundle skills + commands + MCPs, `.plugin` packaging, install/distribution flow.
3. **Skill quality patterns** — the `skill-system-mastery` skill's guidance on trigger phrases, description-as-router, and avoiding skill-collision; review the existing PM/design skills already on the user's machine (listed in available_skills) for naming conventions and scope sizing.
4. **Trade-offs: many small skills vs. one fat plugin** — when does each make sense for a solo PM user?

Cite sources inline (URLs) for any claim that depends on external docs.
</external_research>

<thinking_instructions>
Before drafting the plan, think through these in order. Output your reasoning under a `<thinking>` section so I can audit it:

1. **Agent inventory.** From `ref-bmad-cis-agents.md`, list every CIS agent. For each, name the techniques/frameworks they own (not their persona).
2. **Technique deduplication.** Many agents likely share underlying techniques (e.g., SCAMPER might appear in multiple workflows). Build a deduped technique list — this is the real candidate skill set.
3. **Skill granularity decision.** For each technique, decide: does it deserve its own skill, or is it a `references/` file inside a parent skill? Default to **one skill per discrete user-invokable workflow**, with shared technique catalogs as reference files. Justify the cut.
4. **Trigger-phrase mapping.** For each candidate skill, draft 3–5 natural-language triggers a PM would actually say. Flag any collisions with the user's existing skills (`pm-product-discovery:brainstorm`, `pm-execution:create-prd`, `design:critique`, etc.) — propose how to differentiate or whether to skip building it.
5. **Plugin packaging.** Decide whether to ship as: (a) a single `bmad-cis` Cowork plugin bundling all skills + a few commands, (b) a marketplace-style folder of standalone skills, or (c) a hybrid. Recommend one with reasoning grounded in the Cowork plugin docs.
6. **Persona handling.** The user explicitly said personas are optional flavor. Decide where (if anywhere) persona language adds value vs. where it's noise — e.g., it might belong in command preambles but not in skill descriptions.
</thinking_instructions>

<deliverable>
Output a single Markdown plan with these sections, in this order:

1. **Executive Summary** (≤150 words) — what you're proposing, why this shape, and the rough size of the deliverable.
2. **CIS Agent → Technique Map** — table: agent name | techniques owned | proposed skill name | keep persona Y/N.
3. **Proposed Skill Inventory** — for each skill: name, one-line description, trigger phrases, sketch of the SKILL.md outline (sections only, no body), what `references/` files it pulls from the CIS docs, and any collisions/overlaps with existing installed skills.
4. **Packaging Recommendation** — plugin vs. loose skills vs. hybrid. Explain. Include the directory tree of the proposed output.
5. **Build Sequence** — ordered, dependency-aware checklist of skills to build first → last. Mark which are "spike to validate the pattern" vs. "fast-follow."
6. **Open Questions for Sean** — anything you couldn't decide without a human, posed as a short numbered list.
7. **Sources** — every URL you fetched during external research.

Constraints on the output:
- Be specific. "Convert the brainstorming agent" is useless; "Skill `cis-brainstorming-session` triggers on 'run a brainstorm', '[idea] brainstorm session', references `brainstorming-techniques.md` and `run-brainstorming-session.md`" is useful.
- No code. No SKILL.md drafts. No YAML. This is a plan, not an implementation.
- No filler. Each bullet earns its place.
- If a CIS agent is redundant with an installed skill the user already has, say "skip — covered by X" rather than building a duplicate.
</deliverable>

<validation>
Before finalizing, self-check:
- [ ] Did I actually read every file listed in `<inputs_to_analyze>`, or did I skim and infer? Re-read anything I skimmed.
- [ ] Does every proposed skill have a clear, non-overlapping trigger surface vs. the user's existing installed skills?
- [ ] Did I cite sources for every external-research claim?
- [ ] Is the build sequence actually ordered by dependency, or just listed?
- [ ] Would Sean be able to hand this plan to a fresh Claude Code session and have it implement skill #1 without asking clarifying questions? If not, tighten.

If any check fails, revise before responding.
</validation>

</prompt>
