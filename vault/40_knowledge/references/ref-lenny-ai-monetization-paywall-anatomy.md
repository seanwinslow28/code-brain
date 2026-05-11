---
title: "Why SaaS freemium playbooks don’t work in AI, and what to do instead"
source: "https://www.lennysnewsletter.com/p/why-saas-freemium-playbooks-dont"
author:
  - "[[Lenny Rachitsky]]"
published: 2026-05-05
created: 2026-05-11
description: "How to build an AI monetization strategy that actually works"
tags:
  - "source/web-clip"
  - "lennys-newsletter"
  - "ai-monetization"
  - "job-hunt-2026"
type: reference
status: processed
domain: [product-management]
ai-context: "Lenny's Newsletter guest post by Vikas Kansal (Google AI product lead) — the anatomy of a modern AI paywall, why SaaS freemium gating fails on AI compute economics, and Google AI's framework for usage caps + tier gating."
---
*👋 Hey there, I’m Lenny. Each week, I answer reader questions about building product, driving growth, and accelerating your career. For more: [Lenny’s Podcast](https://www.lennysnewsletter.com/podcast) | [Lennybot](https://www.lennybot.com/) | [How I AI](https://www.youtube.com/@howiaipodcast) | My favorite [AI/PM courses](https://maven.com/lenny), [public speaking course](https://ultraspeaking.com/lennyslist?via=lenny), and [interview prep copilot](https://www.benerez.com/copilot/lenny)*

*P.S. Get a full free year of Google AI, Cursor, Lovable, Notion, Manus, Replit, Gamma, n8n, Canva, ElevenLabs, Factory, Wispr Flow, Fin, Supabase, Bolt, Linear, PostHog, Framer, Railway, Granola, Warp, Gumloop, Magic Patterns, Mobbin, Stripe Atlas, and ChatPRD, by becoming [an Insider subscriber](https://www.lennysnewsletter.com/subscribe?plan=founding). [Yes, this is for real](https://www.lennysproductpass.com/).*

---

Today’s guest author, [Vikas Kansal](https://x.com/vikaskansalHQ), leads product for [Google AI](https://one.google.com/intl/en/about/google-ai-plans/), arguably the most successful consumer subscription bundle in history, with Gemini 3.1, Nano Banana, NotebookLM, Veo3, and terabytes (!) of cloud storage. Vikas has been on the front lines of figuring out how to successfully monetize AI products, balancing compute costs with sustainable growth, and in today’s in-depth guest post, he shares all the lessons he and his team have learned about paywalling AI.

Let’s get into it.

---

![](https://substackcdn.com/image/fetch/$s_!jX4T!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8dbe470a-3caf-43dd-ab76-118d515e409f_1456x970.png)

You’ve just launched an incredible AI product. Growth is exploding, and users are completely hooked on the “magic” of your free tier. Then your bills arrive. In traditional SaaS, serving an extra free user costs essentially zero. In AI, every time a free user hits “Enter,” your GPUs fire, and your cash burns. AI products need to figure out monetization quickly, or compute costs will bankrupt your company.

Most product teams still reach for the traditional SaaS freemium playbook when designing their AI freemium strategy: give away the basics, and gate the best features. But as growth expert (and four-time Lenny’s Podcast guest) [Elena Verna](https://www.elenaverna.com/p/why-ai-doesnt-mean-the-end-of-freemium) rightly points out, when building an AI product, you have to give away a massive amount of “magic” for users to get to the aha moment. They need to actually experience the model writing a perfect email or generating that perfect image before deciding to use a product even a second time. In today’s increasingly noisy market, the time to value (TTV) must be instantaneous if you hope to keep people’s attention.

But this creates a paradox: what happens when that free magical experience becomes so good (and expensive in compute) that it cannibalizes your premium tier?

While launching Google’s [AI subscriptions](https://one.google.com/about/google-ai-plans/), we slammed right into this wall. The free tier was so good that for most tasks, it was outperforming humans. For free! It could write flawless Python, draft perfect marketing copy, and summarize long email threads instantly. We realized we were competing against ourselves, while also trying to create a sustainable business as demand for AI compute exponentially increases over time. Users rightly asked themselves, “Why should I pay $20 a month when the free version is already smarter than I am?”

The traditional SaaS playbook would suggest that we should’ve paygated some of our best features, like the [viral](https://www.reddit.com/r/singularity/comments/1fiyrz5/googles_notebooklm_new_podcast_function_has_the/) NotebookLM podcast generator, Nano Banana images, or Gemini Deep Research. In the past, Slack successfully gated message history and Figma gated team libraries. But if we had paygated the ability to talk it out live with Gemini or Deep Research, users would never have experienced the magic needed to build a daily habit and worked up a desire to try the tools again. Plus, this may not have actually addressed the biggest sources of compute costs. The reality of AI products forced us to completely rebuild the anatomy of a paywall for AI subscriptions. Here is the framework we developed.

## The anatomy of a modern AI paywall

![](https://substackcdn.com/image/fetch/$s_!DSRt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6feef582-dd90-4a58-8819-44d3bbd6a175_1532x862.png)

Generated with Nano Banana Pro, a benefit of the Google AI subscription bundle 👀

The modern AI paywall should be constructed with both sides of the equation in mind: what users expect and what actually costs the company money in compute. This means moving beyond a traditional SaaS freemium model to multiple dynamic, usage-based, and outcome-driven tiers. If you are building an AI paywall, shift your upgrade triggers to these three pillars that align customer utility with costs to the company:

## Pillar 1: Gate usage intensity

When we first added a paywall to Google’s AI features, our instinct was the traditional SaaS “premium” play: a single $20 **Gemini Advanced** tier, where users pay to access the smartest model. But we quickly hit two problems. First, as I mentioned above, the free tier was already so capable that many users felt it was already “smarter than them.” So they saw no reason to upgrade. But the second was more surprising: the power users who *did* upgrade were consuming such immense amounts of compute that the unit economics for the company were terrifying. We realized the real value proposition wasn’t just the quality of the model/answer, but the volume of work a user could pump through the system. And we’d have to price that access accordingly if the business model was going to work.

So we redesigned our offering into **Plus, Pro, and Ultra** tiers. Each bucket maps to a specific level of usage intensity, offering higher usage and larger context windows (up to 1 million tokens) as you move up. This provides users with predictable, prepaid pricing tiers and avoids the pay-per-use AWS-style bill shock that consumers hate. You get a taste of most features in every tier, and the Pro tier may be sufficient for a casual experimenter, while power users would opt for the Ultra tier. This approach aligned our unit economics and subscriber distribution to create a financially sustainable business model. We found that gating usage intensity was a more powerful monetization lever than gating model intelligence.

**As another example, [Midjourney](https://www.midjourney.com/)** does this well. They use a “Fast Mode” vs. “Relax Mode” system. Fast Mode provides instant GPU access for quick results using limited monthly hours—which are priced accordingly. Once Fast Hours are exhausted, users on Standard plans or higher can switch to unlimited Relax Mode, which operates in a queue based on demand. Users are paying for priority access to their GPUs to generate more, faster images and not necessarily for better images. And the company can keep their unit economics tight.

## Pillar 2: Gate outcomes

While Pillar 1 monetizes raw compute and volume, Pillar 2 monetizes productivity. The free tier may give a user the right answer, but it requires manual effort—copying, pasting, prompting, and formatting. To get users to upgrade, you must put a paywall in front of features that collapse multi-step tasks into a single click. “Pro” users are highly sensitive to friction, and they will justify the subscription cost simply based on the hours of work it eliminates from their life.

Our original value proposition for **Gemini Advanced** was built entirely around providing the “best and fastest answer” a frontier model could produce. Since then, LLMs made a major transition from passive text generators to autonomous **AI agents** that can reason, plan, use tools, and retain memory to complete complex tasks. We embraced this shift by making **Chrome [auto browse](https://support.google.com/chrome/answer/16821166?hl=en)** exclusively for our higher tiers. Chrome’s auto browse (powered by Gemini) is an AI agent feature that autonomously navigates websites, fills out forms, compares products, adds items to carts, and manages tasks like booking appointments within the browser. We framed the paywall around the employee labor saved, by letting the agent navigate the web and execute actions on behalf of the user to complete actual work. We stopped selling “answers” and started selling “hours.”

Intercom’s [Fin AI agent](https://fin.ai/pricing) is the gold standard in outcome-based AI pricing. It charges $0.99 per resolution. It’s free to let the AI try to answer, but you only pay when the user confirms their problem was actually solved. [Sierra](https://sierra.ai/) also does this well.

## Pillar 3: Gate the heaviest compute modalities

When we were brainstorming the go-to-market for **Genie 3** —our real-time interactive “world model”—we knew the compute costs would be staggering. During internal dogfooding, we joked that the TPUs were melting on every prompt. We realized that offering this to every free user wasn’t just a bad business move but was physically impossible. There simply weren’t enough TPUs to serve this model at the 100K+ QPS required for hundreds of millions of DAUs. However, we also found that consumers intrinsically understand that these heavy modalities are a premium service. They don’t expect a cinematic, photorealistic 3D world to be free in the same way they expect a 500-word email to be.

So we made Genie 3 available exclusively to our highest-tier members. By elevating this frontier world model into a premium tier, we turned a massive compute liability into a powerful incentive for users to move to the top of our pricing ladder. This also enabled us to showcase the state-of-the-art model without running into capacity constraints.

My advice is to use your most expensive, compute-heavy modalities as the ultimate upgrade trigger for your highest subscription tier. Make text and basic image generation universally accessible to drive top-of-funnel growth, but set a hard paywall the moment a user wants to render a cinematic video, run a real-time simulation, or enter a persistent 3D environment.

## Craft your monetization ecosystem

Well-crafted and value-aligned tiers can capture the user’s experimental budget, but they won’t keep it. AI subscriptions have relatively higher churn compared with traditional SaaS simply because the core usage habits are still being formed. To access that lifetime user value, you have to design an ecosystem surrounding the tiers to contain and expand your customer base. Below is how you optimize conversion, retention, and cost to serve to ensure that you’re building an ecosystem that lasts.

## Nail your conversion catalysts

Deciding *what* value to put in which tier is only half the battle. You also need to master *when* and *how* to prompt the upsell that actually drives revenue. To push a highly engaged free user over the tipping point, you need specific conversion catalysts—behavioral triggers, contextual UX nudges, and strategic packaging that transform a frustrating roadblock into a frictionless, no-brainer upgrade. Showing the upgrade prompt is more an art than a science. Driving meaningful conversions ultimately comes down to surfacing the right contextual nudge to the right user at the exact moment of high intent. With Google AI subscriptions, we’ve found a few approaches that really work:

#### The multi-turn metric

A user who prompts, receives an output, and then uses follow-up prompts to refine that exact output five or more times in a single session. This signals that they are doing “real work” and likely have a high willingness to pay at this exact moment.

![](https://substackcdn.com/image/fetch/$s_!sjvr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F239961e2-6ff7-45f4-b792-922fe1c8967c_1456x1421.png)

#### The cross-platform trigger

A user who accesses your product on both desktop web and their mobile device within a 48-hour window has officially integrated the tool into their daily life. That is the exact moment to trigger a contextual upsell.

#### The “continue this chat” nudge

We use Gemini “chat sharing” as not only a user acquisition growth loop but also an effective upgrade trigger. When a recipient clicks a shared link to a Gemini conversation, they are given the option to “Continue this chat.” If the chat requires a Pro-tier model or a 1M-token context window, the recipient hits a “soft paywall” that demonstrates the value of the premium tier immediately through a real-world use case.

![](https://substackcdn.com/image/fetch/$s_!0IHa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff32d16c1-a049-471e-8c6e-10d2af8fa120_1456x1149.png)

## Package for stickiness

Designing the perfect upgrade trigger will get you the initial conversion, but the real battle is retention. Right now, industry-wide churn rates for AI subscriptions are notoriously high because users buy the magic on day one but fail to build a daily habit by day 30. AI usage is naturally episodic: a user might write 10 reports in October but zero in November, so they cancel. The fight for month two is real.

To ensure long-term lifetime value (LTV), you must bundle AI with existing, stickier utilities. At Google, bundling our AI subscriptions with Google One cloud storage was the masterstroke. Users rarely cancel their cloud storage, because the pain of losing their photos or emails is too high. That means that Google One subscribers make it to month two of their AI usage almost automatically. The habit is built, and the rest is history.

If you are an independent startup, bundle your AI with sticky workflow assets: saved prompt libraries, team collaboration workspaces, or proprietary data integrations. **Cursor** is a perfect example of how to use this approach well. They built a significant moat by embedding the AI directly into the IDE and indexing the developer’s local codebase. This ensured that if a user decided to churn, they would actively tear down their own customized setup, which is expensive to rebuild.

## Route prompts intelligently

You cannot afford to serve your biggest, most expensive frontier model to every free user for every prompt. As we know, saying “please” and “thank you” to our beloved LLMs is [costing](https://community.openai.com/t/using-please-and-thank-you-in-a-prompt/1235094) millions of dollars in compute. Build a lightweight classifier at the input layer using **semantic routing**: If a free user asks, *“What is the capital of France?”* it is instantly routed to a hyper-cheap, lightning-fast micro-model (e.g. Gemini 3.1 Flash-Lite or an open source 8B parameter model). If they input a complex logic puzzle, it routes to a heavier reasoning model with token metering. The user gets instant magic, and you protect your gross margins invisibly.

You can also use Amazon Bedrock’s Intelligent Prompt Routing, which provides a cloud-native endpoint to efficiently route requests between different foundational models within the same model family. It can dynamically predict the response quality of each model for each request and then route the request to the model with the best response quality. This helps to optimize for both response quality and cost.

## Beware monetization anti-patterns

Even with a perfectly calibrated paywall and a thriving ecosystem, the transition from legacy SaaS to agentic AI is littered with margin traps. These monetization anti-patterns are the common structural mistakes companies make when they prioritize short-term conversion over long-term sustainability. If you aren’t actively designing around these pitfalls, your most engaged power users will quickly become the ones who bankrupt you.

## Don’t break user trust

AI usage naturally spikes around specific time-bound projects or final exams, and users will inevitably need to pause their subscriptions when the work concludes. If you force them through a labyrinth of retention menus or hidden buttons to stop their billing, you run the risk of turning a temporary break into a permanent exit. Instead, design for the natural ebb and flow of AI usage. Offer a frictionless, one-click “pause” or an easy downgrade that preserves their custom instructions and saved prompt libraries. If you make it painless to leave, you preserve the relationship with the chance that they reactivate when their next heavy workload hits.

## Don’t forget to future-proof your tiers

The frontier model you are paying a premium to serve today will likely become cheaper, faster, and commoditized in just a few months. If you lock your tier boundaries in stone, you will quickly find yourself on the wrong side of the unit economics equation. You would be bleeding margins because compute costs unexpectedly spiked and end up [giving away](https://www.forbes.com/sites/annatong/2026/03/05/cursor-goes-to-war-for-ai-coding-dominance/) $5,000 of compute for a $200 subscription, or bleeding users because a competitor is now offering your “premium” capabilities for free. To future-proof your monetization strategy, you must build flexibility directly into your paywall. Constantly audit your unit costs, be prepared to shift previously premium features down to the free tier as compute inevitably gets cheaper, and always ensure you have room at the top of your pricing ladder to monetize the next massive breakthrough in AI capability.

## There’s a cost to peak-agnostic pricing

Even public utility companies know that you cannot be charging users the exact same rate at 2 p.m. on a Tuesday as you do at 2 a.m. on a Sunday. And AI infrastructure in particular is fundamentally constrained by peak concurrency. During the weekday B2B rush, your GPUs are redlining, and you might even be paying surge pricing to your cloud provider to maintain uptime. On weekends, those same servers are sitting completely idle, burning depreciation costs. If you charge a flat rate 24/7, you accidentally incentivize users to run heavy, non-urgent tasks right when your compute is most expensive. Introduce mechanics like “usage multipliers” or compute “happy hours” where their credits go twice as far. This smooths out your server load, delights cost-conscious users, and transforms idle weekend GPU time into pure profit.

## Build sustainability in the messy middle

It is important to remember that this is only year three of what will likely be a 10-year transformational shift around AI. We are squarely in the “messy middle” of the technology and the business of gen AI. Right now, users are actively pouring experimental dollars into the market, eager to test, adopt, and play with the latest AI tools. But just as users are navigating this messy middle, so are we as product and monetization leaders. Our challenge right now isn’t just capturing those experimental dollars; it’s experimenting in real time to figure out how to translate them into sustainable unit economics and the right long-term product offerings. These experimental budgets won’t last forever.

As a business, your focus must be on building long-term stickiness, embedding your product into daily workflows, and building an impenetrable moat around user retention before the novelty fades. The way forward is to start aligning user expectations with actual unit costs now—and continue evolving your offering as those shift with the market and the technology. Creating dynamic, value- and cost-aligned subscription tiers is the first big step toward that future.

I can’t wait to see the incredible AI products you build and, more importantly, the sustainable businesses you build around them.

*Thanks, Vikas! For more, follow Vikas on [X](https://x.com/vikaskansalHQ) and [LinkedIn](https://www.linkedin.com/in/vikasrkansal/).*

*Have a fulfilling and productive week 🙏*

---

**If you’re finding this newsletter valuable, share it with a friend, and consider subscribing if you haven’t already. There are [group discounts](https://www.lennysnewsletter.com/subscribe?group=true), [gift options](https://www.lennysnewsletter.com/subscribe?gift=true), and [referral bonuses](https://www.lennysnewsletter.com/leaderboard) available.**

Sincerely,

Lenny 👋

---
*Clipped from [lennysnewsletter.com](https://www.lennysnewsletter.com/p/why-saas-freemium-playbooks-dont) on 2026-05-11T13:22:25-04:00*
