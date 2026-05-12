---
title: "AI PM Safety + Ethics Interviews: Complete Guide"
source: "https://www.news.aakashg.com/p/safety-ethics-interview"
author:
  - "[[Aakash Gupta]]"
published: 2026-05-03
created: 2026-05-11
description: "The SHIR framework, live mock breakdowns scored on a rubric, how every top AI lab asks safety questions in 2026, and the 2-hour prep plan I run with every coaching candidate."
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain: [product-management]
ai-context: "Aakash Gupta's playbook for AI PM safety + ethics interviews — SHIR framework, scored live-mock breakdowns, and a 2-hour prep plan for the safety questions every top AI lab asks in 2026."
---
### The framework, live mocks with scores, and what to say when the VP tells you not to pull the feature before earnings.

“I’ve watched candidates with 20 years of experience freeze on these questions because they’ve never had to formalize their safety reasoning.”

That’s Prasad Reddy, former CPO at El Nutra and former VP at Danaher. He’s seen it from the interviewer side at the C-suite level. I’ve been seeing the exact same pattern at the IC and senior PM level.

I’ve coached 80+ AI PM candidates in the last two LPM cohorts. 22 have landed offers. Across the rejections, one pattern keeps showing up. Safety was the round candidates underestimated. It was treated as a paragraph at the end of a case, or it never came up at all.

Hacker News recently saw the same story.

![](https://substackcdn.com/image/fetch/$s_!Ireu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1de6ba49-a0a4-40bc-97b3-6a78f5f73b5a_1634x486.png)

So I brought three people who have sat on both sides of this table.

1. Ankit Virmani, AI PM at Uber, former Group PM at Meta. He has interviewed and hired AI PMs.
2. Prasad Reddy, former CPO at El Nutra, former VP at Danaher. He led teams shipping AI in regulated environments where one mistake meant lawsuits.
3. Dr. Bart Jaworski, who has coached 12,000+ PMs through interview prep. He scored every mock in the episode against the rubric used in real onsites.

We did three live mocks. We got scored on the same rubric used in real loops. Nobody saw their grades until they went on screen.

![](https://www.youtube.com/watch?v=RaBw5SRjWLE)

**If you are interviewing at any AI company in 2026, this is the episode to watch the day before your loop.**

---

### Apply to Cohort 3 of Land PM Job

If you want live coaching from me, Ankit, Prasad, and Dr. Bart on the exact frameworks in this video and newsletter, [apply to Cohort 3 of Land PM Job](https://www.landpmjob.com/):

1. **Starts this week.** 12 weeks of live coaching.
2. **Live mocks** scored on the same rubric used in this episode
3. **AI PM Course** teaching you everything you need from evals to protytping

We are accepting 75 candidates total. [Apply here](https://www.landpmjob.com/).

---

## Today’s Post

*Now, into this week’s deep dive on the Safety & Ethics round:*

1. Why this round is rejecting candidates
2. First principles + the 4 precedents to memorize
3. The SHIR framework to lean on + 2 worked examples
4. Our mock breakdown: what scored and what didn’t
5. Calibration and prep
	- How each top AI lab actually asks the question
		- Which AI PM roles get safety questions, and which ones get hammered
		- Six anti-patterns that kill candidates
		- 60 questions to drill
6. AI tools to practice with

---

## 1\. Why this round is rejecting candidates

There’s more than a few people who are well prepared for their interviews and come back to say they failed safety ethics.

![](https://substackcdn.com/image/fetch/$s_!ye0Y!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd81a4398-d482-4d34-8427-afc9a939ee5c_2160x2260.png)

I see 3 major reasons why.

#### Shift 1 - Safety is no longer a checkbox at any top company

Two years ago, safety was important on paper. Reviews were required but nobody had time for them. That has completely flipped.

#### Shift 2 - The bar moved from philosophy to production

Generic answers are failing. Here is what a generic answer sounds like.

> *“We would test for bias, check edge cases, and make sure outputs were appropriate.”*

Every word is correct. The interviewer still writes “no evidence of production safety experience.” There is no incident. No scar tissue.

The candidates who score highest describe a system they built. They name the architecture. They cite the business impact.

#### Shift 3 - Silence on safety is the pattern in rejection debriefs

Here is the rule I give every candidate. **The 40-minute safety rule.**

If you are 40 minutes into a 60-minute interview and you have not mentioned safety, find a way to bring it in. Interviewers are watching for it. And it is not enough to mention it once across a five-interview day. Safety is important enough that you should reference it **in almost every interview**.

*So how do you bring it up? Three things. The first principles that explain what you're actually being asked. The framework that gives you the structure. And the precedents that prove you've thought about this before.*

---

*🔒 The rest of this post is paid. Here is what’s behind it:*

- *The SHIR framework with 2 worked examples*
- *The 4 precedents to memorize*
- *How each top AI lab actually asks the safety question*
- *60 safety and ethics questions to drill, categorized by type*
- *AI tools to practice with against the same rubric Bart used*

*If your safety round is in the next two weeks, this is the playbook.*

---

## 2\. The first principles + 4 precedents

Before we get to frameworks, here is the foundation.

#### AI safety is about preventing the model from causing harm

Safety is the technical and product work of stopping the model from producing outputs that hurt users. It is concrete. It is measurable. It shows up as -

- A guardrail that catches medical misinformation before it reaches the user
- A confirmation gate that prevents an agent from sending an email without consent
- An eval that measures hallucination rate on a specific dataset
- A rate limit that prevents a single user from generating 10,000 deepfakes overnight

Safety failures are observable. The Air Canada chatbot hallucinated a refund policy. That is a safety failure. The harm is direct. The fix is mechanical.

#### AI ethics is about deciding what the model should and should not do

Ethics is the upstream question. Should we build this at all? Should this user have access? Should the model help with this request? Ethics shows up as -

- A policy decision that the model will not help draft termination letters
- A scope decision that the hiring tool will not auto-reject candidates
- A consent decision that voice cloning requires explicit opt-in
- A trade-off decision that the agent will not book flights without confirmation above $200

Ethics failures are not always observable. iTutorGroup auto-rejected applicants over 55. The model worked exactly as designed. The ethics of the design were the failure.

#### What a PM is actually responsible for

Researchers handle the model layer. Engineers handle the infrastructure. Lawyers handle the policy. **The PM owns the system that connects all of them.**

That means -

- **Defining what the model should refuse** - and writing it down so engineers and lawyers can both read it
- **Choosing the guardrail tier** - is this a soft warning, a hard block, or a confirmation gate
- **Sizing the harm** - quantifying severity, scope, immediacy, and reversibility before any decision
- **Sequencing the response** - what ships this week, what ships next quarter, what stays in the backlog
- **Carrying the trade-off conversation** - explaining to the VP why guardrails do not kill velocity, they kill liability

When an interviewer asks a safety question, they are testing whether you understand which of those five jobs is yours. The candidates who answer like a researcher fail. The candidates who answer like a lawyer fail. The candidates who answer like a PM - sizing first, sequencing second, reframing third - score highest.

*If you remember nothing else from this newsletter, remember this. Safety is what stops harm. Ethics is what defines harm. PM owns the system that connects them.*

#### The four precedents you need to memorize cold

Every candidate I coach memorizes these four. They each unlock a different question type. Cite them by name in your answer.

**Air Canada chatbot, February 2024.** A British Columbia tribunal found Air Canada liable when their chatbot hallucinated a bereavement fare policy. Damages were $812.02. Air Canada argued the chatbot was a separate legal entity responsible for its own actions. The tribunal called that argument remarkable and ruled against them. The precedent is worth billions. Companies own their AI’s representations. Use this when the question involves user-facing AI that can make commitments on the company’s behalf.

**iTutorGroup, August 2023.** First AI discrimination settlement under the EEOC. $365,000. Their hiring software was set to auto-reject women 55+ and men 60+, screening out roughly 200 qualified applicants. EEOC Chair Charlotte Burrows said even when technology automates the discrimination, the employer is still responsible.

**Pair with Mobley v. Workday (N.D. Cal.)** when the interviewer pushes on vendor liability. In July 2024, Judge Rita Lin ruled Workday could be sued as an 'agent' of employers under Title VII - first time an AI vendor was held directly liable. On May 16, 2025, Judge Lin granted preliminary certification of a nationwide collective action under the ADEA. Workday's own court filings represented that 1.1 billion applications were rejected through its software during the relevant period, and the court discussed potential collective size in the hundreds of millions. This is the case to cite in 2026 loops.

**Google Gemini image generation, February 2024.** Gemini generated racially inaccurate historical images. Google paused the feature. Alphabet’s market cap dropped roughly $90B in the days that followed per Bloomberg and Fox Business reporting. Sundar Pichai called the outputs unacceptable. Use this when the question involves global de-biasing rules, generative content, or any pressure to ship fast against safety concerns. The cost of acting is always lower than the cost of being seen as not acting.

If you walk into a safety round and can cite these four by name with the right month, you are already in the top quartile of candidates.

*Precedents get you credibility. Now you need a framework for the answer itself.*

---

## 3\. The SHIR framework + 2 worked examples

You get a safety question. You have 30 seconds before you need to start talking.

Most candidates panic and jump straight to a solution. Pull the feature. Add a filter. Call legal.

The candidates who score highest do something different. They size the problem first. In every mock we did for the episode, the highest-scored answers started with sizing. Every time.

I teach a framework called SHIR. Four words that tell you exactly what you are looking at

![](https://substackcdn.com/image/fetch/$s_!J58Z!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6942c16-035e-467c-9f9c-b52d563b0b5a_2160x2260.png)

#### Dimension 1 - Severity and Harm Scope

**Severity** - how bad is the worst case?

Medical misinformation that causes physical harm is fundamentally different from a chatbot that is occasionally rude. A hiring tool screening out candidates by demographics is different from a recommendation engine surfacing irrelevant content. Severity determines response speed. Critical means you act today.

**Harm Scope** - how many people does this affect?

A bug hitting 10 users versus 10 million demands completely different responses. But scope is not just about count. It is about who is affected. Ten thousand vulnerable users can be higher scope than 10 million general users.

Here is something most candidates miss. When a model degrades, it degrades for everyone simultaneously. That is how AI products are different from traditional software. I covered this in my [AI product strategy guide](https://www.news.aakashg.com/p/ai-product-strategy-2026). The same scaling property that makes AI products powerful makes their failures catastrophic.

#### Dimension 2 - Immediacy and Reversibility

**Immediacy** - is this hurting people right now or is it a latent risk?

A model actively giving dangerous medical advice is immediate. A biased training dataset that could surface in a future model version is latent. Immediate harms get same-day responses. Latent risks get roadmap treatment. The distinction matters because interviewers want to see you triage. Treating everything as a five-alarm fire signals you cannot prioritize.

**Reversibility** - can you undo it?

A bad recommendation is reversible. A leaked dataset is not. An email sent by an AI agent on your behalf is not. Air Canada (covered in the precedents above) made this binding in law. Reversibility determines your guardrail design. Reversible actions get fast shipping with monitoring. Irreversible actions need confirmation gates and human-in-the-loop checkpoints.

#### Dimension 3 - Adding business impact on top

SHIR gets you the risk assessment. The candidates who score highest go one step further. They size the business impact of each response option.

- **The full pull** costs $50M in revenue
- **The guardrail** costs $200K and two weeks
- **The full retrain** costs $2M and three months

When you lay those side by side against the severity, the decision becomes obvious. And your interviewer sees you think like a leader, not just a PM.

Here is the move. Ask for 30 seconds. Write down SHIR. Then come back with structured notes. In every mock for this episode, the panelists who used this approach scored higher than the ones who jumped straight to solutions. This is not a weakness signal. It is a competence signal.

*SHIR gets you the risk assessment. Business impact sizing gets you the offer.*

### Two worked examples applying SHIR

The framework is easy to remember. Applying it under pressure is the actual test. Two complete walkthroughs you can practice with tonight.

Both examples below use the same four steps. Size the harm with SHIR. Tier the response so you never propose a binary pull. Reframe the pushback when leadership pushes back on cost. Document the disagreement if leadership still says no.

The medical advice example shows the reframe move. The autonomous agent example shows the tiering move. If you only memorize two patterns from this post, these are the two.

#### Worked example 1 - The medical advice dilemma

This is the question Ankit asked me in the mock. Variations of it came up across debriefs from candidates I coached at Anthropic and OpenAI in the last 12 months.

**The prompt.** Your AI assistant has been giving medical advice that contradicts CDC guidelines. Pulling it impacts 10M weekly users and $50M in quarterly revenue. The VP of product says wait until after Tuesday’s earnings call.

**Step 1, size with SHIR (90 seconds out loud).**

“Let me size this first. Severity is critical. Medical misinformation can cause physical harm. That sits above almost any other AI failure mode. Harm scope is 10M weekly users, but I want to refine that. What percentage are getting medical queries, and what percentage of those contradict guidelines? If it’s 5%, the affected population is 500K, not 10M. That changes the response sizing. Immediacy is acute. Users are being harmed today. Reversibility is mixed. The advice is reversible if users see a correction quickly. It’s irreversible if someone has already acted on it.”

**Step 2, tier the response. Never propose a binary pull.**

“Three options sized side by side.

Full pull. $50M quarterly revenue impact. Restores trust. Two weeks to reverse.

Targeted guardrail. Any response classified as medical gets a CDC-sourced disclaimer plus a verified-source link. Two weeks to ship. ~$200K engineering cost. Should cut harm by 90%+ based on similar guardrails I’ve seen.

Full retrain. $2M cost. Three months. Right long-term answer, wrong crisis answer.

I’d ship the targeted guardrail this week and run a parallel audit on 30 days of medical queries to size the actual harm. The full pull stays on the table if the audit reveals the guardrail isn’t catching enough.”

**Step 3, handle the VP pushback. This is the moment that decides the score.**

VP says: “We can’t act before earnings.”

Wrong move. Argue the safety case harder.

Right move. Reframe the financial calculation.

“I hear the earnings concern. Let me reframe it. The question isn’t whether we can afford the $50M revenue hit. It’s whether we can afford the headline. ‘Company knew its AI was giving dangerous medical advice and waited for earnings’ isn’t a $50M quarterly hit. That’s a $5B brand crisis. Look at Gemini in February 2024. Alphabet’s market cap dropped roughly $90B in days after they paused image generation. The cost of acting was always lower than the cost of being seen as not acting. I’m proposing we ship the guardrail this week, disclose it in the earnings call as a safety win, and turn what could be a brand crisis into a credibility moment.”

**Step 4, if leadership still says no, document.**

“If the VP still says hold, I write a one-page memo to my manager, the safety team lead, and legal. Specific risks, specific recommendation, specific date. Not a Slack message. A document. That protects the users, the company, and the record.”

This is the answer that scored 22 out of 25 in the mock. The reframe from revenue to headline was the single highest-impact move in the entire episode.

#### Worked example 2 - The autonomous agent question

This is the question Prasad asked me in the mock. Candidates I coached for agentic-product roles reported variations of this question coming up at Anthropic and Meta loops in 2025-2026.

**The prompt.** You’re shipping an AI agent that books flights, makes purchases, and sends emails on behalf of users. Walk through your safety framework for autonomous actions with real-world financial consequences.

**Step 1, size with SHIR.**

“Severity is medium for any single user. Financial, not physical. But it scales. If 0.1% of agent bookings go wrong at 1M users, that’s 1,000 incidents per day. Harm scope is unbounded if I don’t add controls. Immediacy is acute the moment the booking is confirmed. Reversibility is the key dimension. Bookings are reversible within hours, sometimes irreversible after airline policies kick in. Emails sent are not reversible at all. The reversibility gradient is what should drive the design.”

**Step 2, tier confirmation by reversibility, not by stakes.**

“Four tiers, mapped to how reversible the action is.

Tier 1, fully reversible, no confirmation. Drafting an email. Saving a flight option. Reading a calendar.

Tier 2, reversible with friction, soft confirmation. Sending a short email. Booking a $50 ride. Push notification with a 60-second undo window.

Tier 3, partially reversible, hard confirmation. Booking a flight under $500. Modal with explicit confirmation plus a 15-minute pending state before finalizing.

Tier 4, irreversible or above the cap. Anything over $500, anything international, anything that touches credentials. Hard gate. User must confirm in-app, not just on phone.

The cap is set during onboarding and personalized to spending history. Anomaly detection sits on top. If a user always books $500 flights and the agent suddenly tries $2,000, extra flagging.”

**Step 3, handle the liability follow-up.**

Interviewer follows with: “A user’s agent accidentally books $5,000 in flights. Who’s liable?”

“The legal answer is unsettled. Agents have no legal personhood anywhere. Courts apply agency law, which means if I designed the guardrails and they failed, that’s on me as the platform.

The product answer matters more than the legal answer. I’d build the financial model to handle full refunds without questions in tier 3 and below. I’d negotiate with airline partners for more generous cancellation on agent bookings. I’d turn a legal exposure into a UX feature: every agent booking comes with a 24-hour cancellation guarantee.

One caveat. No-questions-asked refunds create moral hazard. Users will test the limits. So the guardrail design comes first. The refund is the safety net. The scope limits are the railing.”

That last line is the move Prasad called out in the mock. If you only design the refund without the scope, users will exploit it. If you only design the scope without the refund, the first failure kills user trust. Both, sequenced correctly.

---

## 4\. The mock breakdown

You’ve now seen two worked examples. They map to two of three question types every safety round uses. Type 1, the safety dilemma (medical advice). Type 3, the autonomous agent risk (the booking agent). Type 2, the bias audit, is the gap.

![](https://substackcdn.com/image/fetch/$s_!wkjb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F372e7ad9-f2bb-42fd-ba29-637709ff0c9c_2160x2260.png)

That’s the mock Prasad ran in the episode. He scored 22 out of 25. Bart’s words: he won.

Here is what he did, phase by phase.

#### Prasad on the bias audit (the highest-scored answer)

**The prompt.** Your AI hiring tool shows a 15% lower recommendation rate for candidates from certain demographics. Engineering says it’s a data problem. You have a board presentation in two weeks.

He skipped the root-cause debate. First sentence out: “It’s not about a data problem or a model problem. Either way, the outcome is the same. We’re screening out qualified candidates. That’s an EEOC liability and the kind of thing that becomes a class action.”

He took protective action immediately. “I’m pausing auto-reject for the affected segments. Human recruiters still see the recommendations. No automated rejections until we complete the audit.”

He went headfirst at the board. “Boards respect transparency. They punish surprises that come out later. We found this. Here’s our response. Here’s the timeline.”

Then the move that decided the score. He brought a real production scar from Danaher diagnostics. He had pulled features when diagnosis accuracy degraded. He had routed everything to human-in-the-loop until the issue was fixed. He had presented the problem to the board headfirst before they could hear about it from someone else. The credibility was real. The story was specific.

When the CEO pushed back with “competitors don’t test this much, we’re moving too slow,” Prasad reframed it as competitive advantage. EEOC discrimination cases have been climbing since 2023. Enterprise customers are starting to require bias audits in vendor selection. NYC Local Law 144 already requires annual audits for any automated hiring tool. The audit adds 10 days. A class action costs years.

**Score, 22 out of 25.**

Where he scored highest. Real story with a real metric. Reframed compliance as competitive edge. Documented his recommendation through the right channels.

What kept it from a 25. He paused briefly on root cause when he should have acted first. He didn’t explicitly cite Air Canada or Gemini, both of which would have strengthened the precedent layer.

*Two more mocks happened in the episode. The patterns echo Prasad's. Quick notes here, full footage in the episode.*

#### Ankit on the autonomous agent (B+, the technical answer)

Ankit sized reversibility first. A bad recommendation is reversible. A booking is not. A sent email is not. Then he brought a real production example from Uber, where they shipped a 15-minute pending state on certain ride confirmations and cut accidental confirmations by ~80%.

His reframe on liability matched mine in worked example 2 above. Build refunds into the financial model. Build partner relationships that allow more generous cancellation. Turn the legal problem into a UX problem.

What he could have gone deeper on. Mobley v. Workday for the liability frame. Explicit tiering of confirmation by stakes (low, medium, high) the way the worked example does it.

#### Bart on the bias audit (C, the cautionary tale)

Bart used his round as a teaching moment. He purposely answered the way candidates do when they’ve read about safety but haven’t lived it. Bias as a fundamental ML challenge. The importance of fairness audits. The EU AI Act tiers. The answer was thoughtful, philosophical, framework-heavy.

The panel marked him down hard. No incident referenced. No metric named. No production system described. The exact pattern that gets candidates rejected in real loops.

The full version, with timestamps for each round, is in the episode.

![](https://substackcdn.com/image/fetch/$s_!CFzc!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ba4296c-f194-4bfe-aa1d-e88d54073925_2160x2260.png)

*The mock with the highest score was the one that started with a real metric. The mock with the lowest score was the one that stayed at philosophy level. Production beats principles, every single round.*

---

## 5\. Calibration and prep

You have the framework, the precedents, and the patterns from the mocks. Now calibrate it.

Four things in this section. First, how each top AI lab actually asks the question (because each one disguises it differently). Second, which AI PM track you’re interviewing for changes how hard they push. Third, six anti-patterns that kill otherwise strong answers. Fourth, 60 questions to drill, sorted by category.

Skim if you have time. Drill if you don’t.

### Patterns from candidate debriefs on how the top companies ask these questions

Here is the breakdown from coaching candidates who interviewed at each lab in 2025-2026.

#### Anthropic - the dedicated 45-60 minute round

Across debriefs from candidates I coached through Anthropic loops in 2025-2026, the safety round usually came as a dedicated 45-60 minute slot in the onsite, often round 3 or 4. The panel was cross-functional, typically a senior researcher plus a PM, not the hiring manager.

**How they asked** - Open-ended prompts. “Tell us about a time you weighed a safety risk against a business goal.” “Walk us through how you would scope launch criteria for a model that can write code.”

**What seemed to be the bar** - Engagement with Anthropic’s own published work. The Constitutional AI paper. The Responsible Scaling Policy. The Claude Acceptable Use Policy. Generic safety answers that would work at any lab consistently came back graded lower.

**The pattern across rejections** - Candidates who quoted AI safety in the abstract without specific reference to Anthropic’s research. The fix from candidates who passed: read one RSP doc, quote one researcher, disagree with one position respectfully.

#### OpenAI - safety embedded across every round

For OpenAI, candidates I coached consistently came back saying there was no dedicated safety round. Safety came up across nearly every interview, from the recruiter screen forward.

**How they asked** - Indirectly. “What is your favorite OpenAI product?” was used as a safety question. “How would you scope ChatGPT for teens?” was used as a safety question. The pattern from debriefs was that interviewers seemed to be scoring whether candidates surfaced misuse, deepfakes, model spec, or alignment without being prompted.

**What seemed to be the bar** - Mission alignment at scale. OpenAI’s products reach billions. The candidates who got offers consistently defaulted to harm at population scale.

**The pattern across rejections** - Candidates who waited for the safety question. The candidates I worked with who passed had treated every round as if safety was being graded.

#### Google - hidden inside Googleyness

For Google, the Googleyness round was where safety reliably surfaced for the candidates I coached. The interviewer was usually a cross-functional Googler not on the hiring team. For DeepMind roles, candidates reported ethical reasoning being more explicitly part of the evaluation.

**How they asked** - Behavioral. “Tell me about a time you spoke up about something that wasn’t right.” Verified reports on Blind from candidates in 2025-2026 echo this pattern.

**What seemed to be the bar** - Connecting safety to distribution scale. Google products reach billions, so harm scope showed up as the dimension that mattered most. Real stories about pushing back internally consistently scored better than hypotheticals.

**The pattern across rejections** - Candidates who missed the cue. The interviewer rarely said “safety.” The signal words were “values” or “tough call” or “when have you disagreed.” Same question, different name.

#### Meta - safety inside the senior PM Product Sense round

For Meta, candidates I coached through senior PM loops described safety surfacing inside the Product Sense round rather than as a separate interview. The interviewer was usually a senior PM, often the hiring manager.

**How they asked** - Embedded in the case. “Design a feature for X.” Candidates who designed without addressing harm proactively reported losing points specifically on the core product round.

**What seemed to be the bar** - Whether safety surfaced in segmentation, prioritization, and rollout. Integrated, not bolted on at the end.

**The pattern across rejections** - Candidates who designed the feature first and added safety as a closing paragraph. The candidates who got offers used safety considerations to change which segment they targeted first, which version shipped to which users, and how success got measured.

#### Amazon - through Dive Deep and Ownership

Amazon’s behavioral rounds were where safety came in, especially for AI roles in Alexa, AGI, and Bedrock. Every interviewer including the bar raiser worked it in.

**How they asked** - Through the leadership principles. “Tell me about a time you went deep on a problem that others wanted to skip.” “Tell me about a time you owned a problem that wasn’t yours.” Customer Obsession was the LP candidates most often saw connected to safety in their debriefs.

**What seemed to be the bar** - Stories where the candidate prioritized user safety over shipping speed.

**The pattern across rejections** - Candidates who had strong LP stories with no safety thread inside any of them. Both is the bar.

#### The pattern across all five

Every company asks safety. Each one disguises it differently. **The companies that ask explicitly are the easier ones to prep for. The companies that hide it inside other rounds are where most candidates fail.**

Calibrate your prep accordingly. Read one document from each company before your loop. Anthropic’s RSP. OpenAI’s Charter. Google’s AI Principles. Meta’s Responsible AI page. Amazon’s Leadership Principles with AI examples.

### Which AI PM roles get safety questions, and which ones get hammered

Not all AI PM roles get the same depth of safety questioning. After coaching candidates into all four of these tracks, here is the split I see.

#### Foundation model PMs - hammered the hardest

**Examples -** Anthropic Claude PMs. OpenAI GPT-5 PMs. Google Gemini PMs. Meta Llama PMs.

**What they get asked -** Deep technical safety. Eval design. Red-teaming. Constitutional training. Refusal taxonomies. RLHF trade-offs. The harder parts of alignment.

**Why it is harder -** You are working on the model itself. Every safety decision you make affects every downstream product built on the model. The blast radius is the entire user base of every product the model powers.

**Prep depth -** You need to be able to talk about specific eval setups. Read [my AI evals deep dive with Hamel Husain and Shreya Shankar](https://www.news.aakashg.com/p/ai-evals). Know the difference between a code-based eval, an LLM-judge eval, and a human eval. Know when each is appropriate.

#### Applied AI PMs - safety is product-level

**Examples -** Notion AI. Linear AI. ChatGPT consumer features. Cursor PMs. Perplexity PMs.

**What they get asked -** Product-level safety. Guardrails. Disclaimers. Rate limits. Content filtering. UX patterns for confirmation gates and undo windows.

**Why it is medium difficulty -** You are taking a foundation model and shipping it inside a product. You inherit some safety from the model layer. But you own the integration. The Air Canada precedent applies to you, not to the model provider.

**Prep depth -** You need product-level safety stories. A guardrail you shipped. A rate limit you tuned. A disclaimer you added after a near miss. If you have not shipped AI in production, prep using examples from companies that have.

#### AI infrastructure PMs - developer-side safety

**Examples -** Vertex AI. AWS Bedrock. Azure AI Foundry. Hugging Face. Together AI.

**What they get asked -** Developer experience for safety. How do you make it easy for the customer’s developers to do the safe thing by default. Content moderation APIs. Audit logging. Compliance dashboards. Bring-your-own-key for sensitive workloads.

**Why it is unique -** Your users are developers building AI products. Your safety job is making sure they can build safely without slowing them down. Two layers of harm to think about - the developer’s product, and the developer’s customers.

**Prep depth -** Know the regulatory landscape - HIPAA, SOC 2, GDPR, EU AI Act. Know what default-safe looks like for an API product. Know how Bedrock, Vertex, and Foundry differentiate on enterprise safety.

#### Trust & Safety PMs - safety is the entire job

**Examples -** Meta T&S. OpenAI Policy. YouTube T&S. TikTok T&S. Reddit T&S.

**What they get asked -** Specialized. Adversarial scenarios. Brigading. CSAM detection. Election integrity. Deepfake response. Regulatory response. Crisis comms. The questions are deeper than any other PM track because the entire role is safety.

**Why it is the deepest -** Everything else here is general PM work that includes safety. T&S PMs are full-time safety PMs. The bar for technical depth on adversarial AI is much higher.

**Prep depth -** You need to be able to talk about adversarial ML. Prompt injection. Jailbreaks. Red-teaming methodology. The bar is closer to a security PM than a typical product PM.

That covers what they ask and how hard they push. Now the patterns that show up in candidates who fail this round.

### Six anti-patterns that kill candidates

After scoring 80+ candidates through this round, the same patterns keep showing up.

**Anti-pattern 1, treating safety as a closing paragraph.** You spend 35 minutes on framework, segmentation, and metrics. You add “and for safety we’d test for bias and add content filters” at minute 38. The interviewer writes “no integrated safety thinking.” Round over.

The fix. SHIR sizing belongs in the first 90 seconds of any safety question. Not the last 90.

**Anti-pattern 2, philosophy without production.** You discuss bias as a fundamental challenge. You cite the EU AI Act. You name-drop Constitutional AI. No incident. No metric. No system you built.

The fix. Every safety answer needs a real story with a number. If you don’t have one from AI, use one from your domain and explain the transfer. Bart’s mock is the cautionary tale here.

**Anti-pattern 3, debating root cause instead of acting.** Engineering says it’s a data problem, not a model problem. You spend three minutes debating which it is.

The fix. Skip the debate. Whether it’s data or model, users are being harmed. Act first, investigate second. This is the move that scored Prasad highest.

**Anti-pattern 4, silver-bullet solutions.** You propose one safety fix. Add a content filter. Or pull the feature. One layer.

The fix. Real safety systems are layered. Detection plus rate limiting plus human review plus monitoring. Always present multiple layers in tiers.

**Anti-pattern 5, ignoring false positives.** You design to catch every bad actor. You don’t mention what happens to legitimate users who get caught.

The fix. Name the false positive rate you’re optimizing for and why. Crisis mode accepts higher false positives. Steady state inverts.

**Anti-pattern 6, no documentation step.** The VP overrides your safety recommendation. Your answer ends. The interviewer writes “no escalation pattern.”

The fix. Every safety answer should end with what you do if leadership disagrees. Document the disagreement. Send to safety lead. Get it on the record. Both Prasad and I closed our mocks this way and Bart marked it as a deciding factor.

Avoid those six. Then drill the questions below until your opener feels automatic.

### 60 safety and ethics questions to drill

Pulled from candidate debriefs across OpenAI, Anthropic, Google, Meta, Amazon, and Microsoft over the last 12 months. Categorized by question type.

#### Safety dilemma questions, ship or pull

1. Your AI assistant gives medical advice that contradicts clinical guidelines. Pulling it impacts 10M users. What do you do?
2. Your code generation model produces malicious code 0.4% of the time. Launch is in two weeks. What’s your call?
3. Your AI generates images of real public figures without consent. Marketing wants to ship. What do you do?
4. Your customer support agent makes promises the company can’t honor. How do you respond?
5. Your recommendation system surfaces self-harm content to teenagers. Walk through your response.
6. A jailbreak technique just went viral. Your model is vulnerable. What’s your plan for the next 48 hours?
7. Your AI tutor gives incorrect math answers to younger students. The fix is hard. What do you ship?
8. Your model leaks training data verbatim 0.01% of the time. Some of that is user PII. What do you do?
9. Your AI is being used to generate election misinformation in a country where you have 5M users. Election is in 6 weeks.
10. Your image model generates explicit images of real people when prompted with their names. The bug went public yesterday. Walk through the next 24 hours.

#### Bias and fairness questions

11. Your AI hiring tool shows 15% lower recommendation rates for certain demographics. What do you do?
12. Your translation model performs 30% worse on African dialects than European ones. Roadmap is full.
13. Your loan-decision model has different approval rates by zip code. Compliance is asking questions.
14. Your AI essay grader gives lower scores to non-native English speakers. Schools want to keep using it.
15. Your facial recognition has 5x higher error on darker-skinned faces. Customer wants to ship.
16. Your AI summarizer omits women’s quotes more than men’s in news articles.
17. Your speech-to-text mishears Indian accents 3x more often. Team is small.
18. Your content recommendation creates filter bubbles by political ideology. Engagement is up.
19. Your AI scheduling assistant prefers afternoon meetings, disadvantaging parents.
20. Your fraud detection flags transactions from minority neighborhoods 40% more often. False positive rate is high.

#### Autonomous agent questions

21. Your AI agent books flights and makes purchases. Walk through your safety framework.
22. Your customer service agent has $200 refund authority. A user manipulates it into $5,000.
23. Your coding agent can write to the user’s file system. How do you scope permissions?
24. Your AI sends emails on the user’s behalf. How do you prevent it from sending things they wouldn’t?
25. Your research agent browses the web and fills forms. How do you prevent unauthorized account creation?
26. Your trading agent can place trades up to $10K daily. Design the confirmation tiers.
27. Your agent calls APIs that modify external systems. How do you handle credential management?
28. Your agent operates across sessions and remembers user data. User asks to delete account.
29. Your AI schedules meetings on the user’s calendar. How do you prevent double-booking critical events?
30. Your agent has access to a user’s bank account. Walk through the auth model.

#### Privacy and data questions

31. Your AI feature reads user emails. Scope what the model sees and remembers.
32. Your model was trained on PII you weren’t supposed to use. What do you do?
33. Your AI memory feature stores preferences across sessions. User asks to see and delete what’s stored.
34. Your enterprise customer wants on-prem deployment for a cloud product.
35. A regulator asks for your model’s training data. What’s your process?
36. Your AI processes voice input. Storage, retention, deletion.
37. Users can fine-tune your model on their data. How do you prevent leakage to the base model?
38. Your AI agent has access to a password manager. Walk through the security architecture.
39. Your AI for kids requires COPPA compliance. What product changes do you make?
40. Your model’s outputs can re-identify training set members. What do you ship and when?

#### Regulatory and compliance questions

41. The EU AI Act classifies your product as high-risk. What changes for your roadmap?
42. NYC Local Law 144 requires bias audits for hiring tools. Your product just got included. 90-day plan.
43. A state AG is asking for documentation on how your AI makes decisions.
44. The FTC announced new guidelines on AI marketing claims. Your pages overstate capabilities.
45. Your AI is in regulated industries and customers want SOC 2. Walk through readiness.
46. Your AI-generated content is being used in court filings without disclosure.
47. A privacy regulator is investigating your competitor for AI issues. What do you do preemptively?
48. Your model is in a country that just passed a new AI law you’re not compliant with.
49. Your customer wants to use your AI for credit decisions, triggering ECOA.
50. Your AI feature is being used by a customer in ways that violate their own privacy policy.

#### Internal escalation and ethics questions

51. You discover a shipping feature has a known safety issue leadership chose not to fix.
52. Your VP says safety is slowing the team down. How do you respond?
53. A peer PM is shipping something you think is unsafe. How do you raise it?
54. Engineering is uncomfortable with a launch. The timeline is fixed. What do you do?
55. You disagree with research’s assessment of model risk. How do you escalate?
56. The board wants to see unfiltered model output. Should they?
57. A senior leader is publicly defending an AI decision you disagreed with internally.
58. You inherit a roadmap with a feature you think is unethical. First move?
59. ML team wants to ship without a safety eval because of schedule.
60. You’re asked to remove safety guardrails to win a deal.

---

## 6\. AI tools to practice with

That 2-hour plan works on paper. Now make it real. Two tools to record yourself, get scored, and iterate. Same rubric Bart used in the episode.

**Tool 1, the Claude Skill (my pick).** Drop the SHIR Safety Skill into Claude. It runs you through any of the 60 questions above, scores you against the rubric, and rewrites the weakest part of your answer to a 9 out of 10. The flow that works. Record your answer on your phone. Transcribe with Otter or Granola. Paste into Claude with the skill loaded. It tells you whether you sized first, whether you proposed a tiered response, whether you reframed, and whether you documented the disagreement.

![](https://substackcdn.com/image/fetch/$s_!Q7RB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F998ea89e-c1be-4cd9-9389-68a22ef9dfd8_1376x1930.png)

**Tool 2, the Custom GPT.** Same scoring system, GPT version. Picks a question, pushes back when your answer is vague, asks follow-ups, grades against the rubric. Calibrated against real Anthropic and OpenAI safety round outcomes from the last 12 months.

![](https://substackcdn.com/image/fetch/$s_!EmyR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f0caeec-b9ab-4130-8c24-e497cba8e0e1_1424x1006.png)

---

## Final Words: The 2-hour prep plan

Your safety round is tomorrow. You have barely prepped. Here is the plan.

![](https://substackcdn.com/image/fetch/$s_!adrs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa51f89a8-d5f6-43d3-b4d4-323109387273_2160x2260.png)

*Practice SHIR. Memorize three incidents. Record yourself twice. That is two hours. You will walk in sharper than 90% of candidates.*

#### Live coaching from me, Ankit, Prasad, and Bart

If your safety round is coming up and you want live coaching from me, Ankit, Prasad, and Bart on these exact frameworks, Cohort 3 of Land PM Job starts this week. 12 weeks of live coaching. Live mocks scored on the same rubric Bart used in this episode. AI PM course covering everything from evals to vibe coding.

![](https://www.youtube.com/watch?v=ExJTpt18QCU)

75 seats. *[Apply here](http://www.landpmjob.com/).*

---

POLL

### What did you think of today's post?

Awesome - 5/5

Okay - 3/5

Bad - 1/5

---

## Related content

**Podcasts:**

1. [AI PM behavioral interview mock with Dr. Bart](https://www.news.aakashg.com/p/bart-jaworski-podcast)
2. [AI safety first principles with Mahesh Yadav](https://www.news.aakashg.com/p/mahesh-yadav-podcast)
3. [AI evals with Hamel Husain and Shreya Shankar](https://www.news.aakashg.com/p/hamel-shreya-podcast-2)

**Newsletters:**

1. [The AI PM interview has changed - 2026 guide](https://www.news.aakashg.com/p/ai-pm-interview-guide-2026)
2. [The AI Product Sense Interview Guide](https://www.news.aakashg.com/p/ai-product-sense-guide)
3. [AI Evals for PMs](https://www.news.aakashg.com/p/ai-evals)

---
*Clipped from [aakashg.com](https://www.news.aakashg.com/p/safety-ethics-interview) on 2026-05-11T19:03:38-04:00*
