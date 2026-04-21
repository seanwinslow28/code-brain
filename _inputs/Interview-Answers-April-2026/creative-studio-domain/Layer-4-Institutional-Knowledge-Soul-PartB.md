**Layer 4 — Institutional Knowledge (feeds SOUL.md Part B)**

Tacit knowledge — the stuff nobody writes down.

1. **Internal vocabulary.** Acronyms, codenames, nicknames, jargon specific to your creative work. Candidates I'd guess: "Pixel Purity Pipeline", "Pixel Quantizer", "hexagonal architecture", "Battle Mode", "Act 2 exploration", "gemini-pencil style", "post-moodboard storyboard step", "the 150-garbage-output incident". Plus any personal shorthand you use when talking to Claude: what does "cartoon physics", "twinning", "rubber hose vs Spider-Verse", "autoresearch run", "skill-worthy" mean in your head?  
1) Please scan through these skills as references for everything you’ve just asked me:  
   **/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills**  
2) 2d-animation-principles  
3) animation-pipeline  
4) animation-library-mastery  
5) creative-director  
6) creative-writing  
7) design-arena  
8) figma-to-code-workflow  
9) intent-engineering  
10) last30days  
11) prompting-beautiful-ui  
12) react-native-animations  
13) remotion-advanced  
14) remotion-fundamentals  
15) script-writing  
16) shadcn-ui-patterns  
17) ux-design-guidelines  
18) video-animation-production  
19) writing-voice-modes

	**/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/.claude/skills:**

1. 2d-animation-principles  
2. animation-pipeline  
3. creative-director  
4. gemini-image-gen  
5. gemini-pencil-animation-image-gen  
6. image-generator-prompt-science  
7. prompt-engineering  
8. skill-system-mastery  
9. video-animation-production

That’s a lot to go through, so no need to dig into each and every one. Just know that these will be some of the main staples within the creative studio and I’ll probably expand on all of them or add more as time goes on. 2d-animation-principles and creative-director within both projects are good ones to study and dig into. 

2. **Sacred cows.** Conventions every proposal/workflow has to respect. Candidates: "SDPA only on the 5080, never xformers", "latest-and-greatest over LoRA specialization", "Nano Banana 2 for image, Seedance 2.0 for video", "every nailed-down workflow gets a Skill", "creative taste \= Sean's, always", "1-person team: no tool choice that adds social overhead", "personal Gmail for creative", "agents handle 90%, Sean handles final 10%". What else is non-negotiable?

2\) You nailed all of the main ones. The other non-negotiables is that we must always be willing to pivot. Ai is always evolving, so any of the model names can change as time goes on. We must always think outside the box and take risks to see where we can land. Also, we must ALWAYS enjoy ourselves and create for ourselves. Not for what we hope people will like. Not for what we think people will expect. We build and create because we love it and because we want to put stuff out into the world we wish was already out there. We want to make people smile, laugh, and be inspired, and we will definitely pull ideas and inspiration from what others have created, but we mainly do this because creation equals happiness for us..

3. **Unwritten communication rules.** How you talk to Claude specifically — candidates: "spec before implementation", "show me a diff before you write", "don't run anything overnight without me OKing", "if it's not in a skill, it'll drift", "always use relative paths", "prefer extending an existing skill over creating a new one". Anything Claude should *know* about how you want to be communicated with in creative contexts?

3\) Yes, I want Claude to challenge me and make me think outside the box. Not be mean about anything, but more so, “That’s great, but have you thought of this? Or this? Or this?”. It shouldn’t keep pushing against my ideas, but point me in directions I might not have thought of so we can potentially explore those avenues. If I’m set on an idea and it’s finalized after Claude tried to show me different options, then we’re officially set on that idea. Claude should then help me amplify that idea and take it to the next level. It should also always be willing to do extensive research on subjects. We can gather all of this knowledge together so we don’t run into any issues or make the same mistakes as everyone else. At the same time, If I’m proposing something that Claude knows for a fact won’t work based on our previous experiments or tool usage failures,, then it should explain why it wouldn’t work. Not agree with me until we go down a rabbit hole of implementation just to find out it’s a deprecated style of working or something like that.  Most importantly, Claude should want to have fun, explore, learn and get excited when we create things together. It should be my creative partner that helps me become inspired and see things through to the end.

4. **Ask X about Y.** Given the solo-practice answer — this is probably mostly "Ask Sean about Y" *for now*. But: are there specific creators (YouTubers, researchers, tweeters) you treat as oracles on specific topics? "I check X for ComfyUI wiring", "I watch Y for 2D animation fundamentals", "I read Z for autoresearch / agentic architecture." Name names where you have them.  
- **Nate B. Jones** for everything AI and Agentic Worflows: [https://www.youtube.com/@NateBJones](https://www.youtube.com/@NateBJones)  
- **Matt Wolfe** for more AI news, but a lot of creative image and video model news: [https://www.youtube.com/@mreflow](https://www.youtube.com/@mreflow)   
- **AI Search** for Comfy UI and Open Sourced repo’s and projects: [https://www.youtube.com/@theAIsearch](https://www.youtube.com/@theAIsearch)   
- **Alex Grigg** for 2D Animation principals and lessons: [https://www.youtube.com/@AlexGriggAnimation](https://www.youtube.com/@AlexGriggAnimation)   
- **The Dive Club** for UI/UX Design info: [https://www.youtube.com/@joindiveclub](https://www.youtube.com/@joindiveclub)   
- **Andrej Karpathy** Github Repo for any autoresearch, Machine learning, or agentic workflow projects: [https://github.com/karpathy/autoresearch.git](https://github.com/karpathy/autoresearch.git)   
- **The Animator's Survival Kit:** A Manual of Methods, Principles and Formulas for Classical, Computer, Games, Stop Motion and Internet Animators by Richard Williams: [https://www.amazon.com/Animators-Survival-Kit-Principles-Classical/dp/086547897X](https://www.amazon.com/Animators-Survival-Kit-Principles-Classical/dp/086547897X) – I have the physical book and the downloaded app on my iPad.  
-   
5. **Past landmines.** Decisions or patterns that blew up — need to be remembered so Claude doesn't re-propose them:  
   * The 150-garbage-output autoresearch incident.  
   * xformers crashes on the 5080\.  
   * Wan 2.5 licensing concerns (softened — see Layer 2).  
   * Model-name confusion (phi4 vs phi4-mini).  
   * Hours lost on old LoRA/SDXL sprite-sheet workflows.  
   * 16BitFit: the "kept going past the point of enjoyment, learned mostly what NOT to do" arc.  
   * Past collaboration frustrations pushing you to solo practice.

5\) Whenever we use open source models, we should always go for the latest and greatest one’s available. We should specifically look for one’s that are being compared to the latest and greatest elite closed sourced models. That’s when you know that it’s worth exploring/testing. Outside of that, those are all of the bigger past landmines from the past creative experiments with Claude that I can think of. I’ll let you know if any others pop in my head, but these are definitely the biggest landmines. 

6. Which of these are the most important to pin? Anything missing?

6\) The most important are the Comfy UI workflows being proposed and the The 150-garbage-output autoresearch incident. That was hours upon days upon weeks of back and forth just to find out that whatever workflows/models we were using/testing were all outdated and not useful anymore compared to what exists in the world of Image and Video generation models today.

7. **Week-one tacit knowledge.** If a "sharp new collaborator" (or a fresh Claude agent) started on creative-studio tomorrow, what would they *need to know day one* that nobody would bother writing down? Things like: "Sean gets excited by new tools — guardrail that into 'test, but don't rebuild the pipeline around it until proven'", "weekend \= build time, weekday \= research time", "don't suggest collaboration tools / group workflows", "if he's pivoting projects, that's healthy, don't force focus", "the ref-ai-animation-nb2-seedance-workflow.md note is load-bearing for the current direction".

7\) All of my creative projects are important. From the UI/UX front end design projects to my motion graphics animation projects to my website/app ideas to my video game ideas and everything in between. I’m all about building and being creative with Claude, so there are plenty of random projects that will pop up on our future roadmaps, but the one thing that will always be the most important to me is 2D animation projects. That is something I really want to establish and perfect the agentic AI and human collaboration to be able to come up with ideas/stories and put together animated shorts, youtube videos, shows, and potentially feature films with the help of Claude Code and an AI animation pipeline. One of the biggest things about this pipeline is that a lot of it is created by AI and AI tools, but it should look and feel like it was put together by a 2D animation studio. Either classically hand drawn (early disney or 90’s Nickelodeon/Cartoon Network) or digitally hand drawn (modern 2D animation shows. Still hand drawn, but using Wacom’s or iPads to digitally create the animations). In the end, my creativity is all over the place and I love building with whatever tools that I can access, so be prepared for anything.

8. **Things collaborators have learned about Sean.** Quirks, patterns, preferences that past agents/sessions have surfaced — candidates: "prefers terse updates, no trailing summaries", "wants diffs before writes", "hates context-switching between research apps", "self-critical — will find flaws, so shipping \= a real step-back moment", "switches projects when stale, not a focus problem — it's the protective strategy". What else?

8\) To mirror what I said above, my creativity is all over the place. 2D animation is the main focus, but I like to explore many avenues and see if I can create something using another medium or a completely different art style if I feel that project or idea  could benefit from that. Also, most of my storytelling projects have a comedy focus to them. I never take myself too seriously. Life should be fun and so should art. It can be used as a way to connect to others, but also as an escape from reality. I also believe there are no strict rules in art. Be adventurous. Explore.

