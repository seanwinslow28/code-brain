---
title: "One person's best AI session vanishes the second they close the tab. Grab the 3 prompts that make it your team's."
source: "https://natesnewsletter.substack.com/p/public-ai-work-team-learning"
author:
  - "[[Nate]]"
published: 2026-05-25
created: 2026-05-26
description: "Watch now | The AI work your company cannot see is the AI work your company cannot learn from."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [claude-mastery, product-management]
ai-context: "Nate Jones' 3-prompt kit for turning private AI work public (Shopify River pattern, 5,938 employees in one month) — convert a messy session into a teachable post, draw the safe-to-share boundary for sensitive work, and let senior people model judgment in the open without it feeling staged."
---
5,938 Shopify employees worked alongside the same AI agent in a single month, all of it in public. When those numbers surfaced this spring, everyone fixated on the scale. The scale is not the interesting part.

Almost no other company works this way, and most of them have the opposite problem. Their people are using AI constantly, asking ChatGPT to rewrite emails, using Claude to reason through customer issues, running coding agents against repos, quietly building small workflows that save hours. And almost none of it is visible to anyone else.

A good prompt disappears into one person’s chat history. A clever correction stays inside one employee’s browser tab. The workflow your best operator nailed last month gets rebuilt from scratch by a new hire who never knew it existed. A senior person figures out how to load context, challenge the model, and review what comes back, and the junior across the team never gets to watch how any of that judgment works.

The result: individuals get smarter, the company does not.

That is the missing layer in most AI adoption plans. Companies are buying tools, writing acceptable-use policies, measuring logins, running the occasional training session. None of it touches the actual problem, which is that your best AI work is invisible to everyone who could learn from it. So every quarter, the same lessons get rediscovered from nothing. You are paying tuition on the same lesson over and over, across hundreds of people, and the bill never stops arriving.

Shopify’s answer is not surveillance. It is not scraping everyone’s chat history and calling it knowledge management. It is something smaller and far more useful: a deliberate way to make non-sensitive AI work visible enough that the people around it can actually learn. The agent that produced those numbers runs only in public. That single design choice is the whole game, and any team can copy it.

**Here’s what’s inside:**

- **What Shopify actually built.** Not the AI mandate everyone argued about, but the design choice underneath River, the agent that runs in public and turns one engineer’s judgment into the whole team’s.
- **Why a prompt library will not save you.** The most valuable part of AI work is the part a prompt library cannot hold, and what you have to make visible instead.
- **Where to draw the line.** A workflow-by-workflow boundary for regulated and sensitive work, so you capture the learning without exposing anything that should stay private.
- **The room, the rules, and the one constraint that makes it work.** A setup any team can run in ninety minutes, the metrics that actually signal learning, and the single binding rule that bends a team toward sharing instead of hoarding.
- **How to bring this into your org.** A three-part prompt kit: one that turns a messy AI session into a post your team can learn from, one that draws the line between what’s safe to share and what stays private, and one that helps your senior people model real work in public without it feeling staged.

Private AI work helps the person at the keyboard. Public AI work helps the company learn. That difference is small today and decisive in a year.

## LINK: Grab the prompts

These three prompts exist because the hardest part of public AI work is not deciding to do it. It is the first concrete move. Most teams stall at the same three places. A useful session happens and nobody can turn it into something teachable, so it evaporates. Somebody wants to share but freezes because they cannot tell what is safe to put in a public channel. And the senior people whose judgment is most worth watching have no low-friction way to work in the open without it feeling like a performance. Each prompt clears one of those blocks, and they run clean on first paste in ChatGPT, Claude, or Gemini.

## The Shopify example is not about a memo

This is where the Shopify story gets more interesting than the mandate discourse.

The public argument around Tobi Lütke’s AI memo has mostly been about whether AI should be mandatory, whether companies are using AI as cover for headcount discipline, and whether AI-first management is inspiring or threatening. I have already written about that elsewhere. The memo was a filter. It changed what kind of person would thrive at Shopify and what kind of person would want to work there.

But the fresher lesson is River.

River is Shopify’s internal AI coding agent. A [ZenML case summary](https://www.zenml.io/llmops-database/building-a-public-ai-agent-workspace-for-organizational-learning) of Tobi Lütke’s public post says River works in public Slack channels rather than private one-on-one workspaces. The reported numbers are striking: in one 30-day period, 5,938 Shopify employees engaged with River across 4,450 Slack channels; in one week, River opened 1,870 pull requests in Shopify’s main monorepo, roughly one in eight merged pull requests.

The specific numbers are useful, but they are not the point.

The point is the design choice. Shopify did not only ask, “How can an agent help one employee do work?” It asked, “How can the agent’s work become visible enough that the organization learns?”

A different question entirely.

If a senior engineer works with River in a public channel, other engineers can see how she scopes the task, what context she gives the agent, where the agent gets stuck. They watch the human correct it. They watch what gets accepted and what gets rejected. A new hire can scroll through prior interactions before making their own request. A support engineer can watch a backend engineer construct the right query and reuse the pattern later.

Apprenticeship.

For most of human history, people learned skilled work by being near skilled workers. You watched how the senior person framed the problem, what they noticed, what they ignored. You learned the craft from the process as much as from the finished product.

AI is quietly breaking that model because so much AI work happens in private windows.

The junior employee does not see how the senior person prompts. The new manager never watches the experienced operator verify an answer. The correction that made the workflow reusable stays invisible. Everyone is alone with the model, which means everyone has to rediscover the same lessons.

Call it the apprenticeship gap.

[Anthropic’s published case study on how its own teams use Claude Code](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code) is a softer version of the same lesson, because it makes the work pattern visible instead of celebrating the output alone. The useful part is what the case study names: the workflows. Data teams using Claude Code to navigate pipelines and update documentation, finance teams describing data workflows in plain text, product engineers using it to find the right files in unfamiliar codebases. That kind of public description lets another team copy the habit, not admire the result.

The public-sector analogue is less flashy but useful. The UK Department for Work and Pensions’ [evaluation of its Copilot trial](https://www.gov.uk/government/publications/an-evaluation-of-dwps-microsoft-copilot-365-trial/an-evaluation-of-dwps-microsoft-365-copilot-trial) (published January 2026) covered 3,549 staff and found that peer demonstrations, acceptable-use guidelines, and informal sharing shaped adoption more than formal training. The design differs from River, but the lesson travels outside Big Tech: adoption improves when people can see how competent colleagues actually use the tool, not when the organization buys licenses.

## Why AI prompt libraries are not enough

A prompt library is a start, but not enough.

A prompt library captures the static instruction. It usually misses the work. It misses the messy context that made the prompt useful. It misses the revisions. It misses the judgment. It misses the moment when the model produced something plausible and the human said, “No, that is wrong for our customer,” or “No, that violates our tone,” or “No, that analysis skipped the important constraint.” When people watch me work with a model, what surprises them is [how often I say no](https://natesnewsletter.substack.com/p/your-comprehension-is-worth-more), and how fast. The speed comes from having been wrong before, and none of it is visible to anyone who was not in the room.

The most valuable part of AI work is rarely the prompt. It is the habit around it.

Manufacturing learned this the expensive way. There is a generation of machinists nearing retirement who can feel quality in a piece of steel through their fingertips, and who cannot fully say how. Companies like John Deere have spent real money trying to capture that knowledge before it walks out the door, and the people doing the capturing will tell you how hard it is to get right. You can approximate the felt sense of a master machinist. You cannot transcribe it. This is Polanyi’s paradox, the old observation that we know more than we can tell, and it is why some of the most stubborn bottlenecks in a supply chain still trace back to one person with a skill that lives in their hands. There is one person who knows how to paint the racing stripes on a Rolls Royce. The senior operator’s judgment about when to trust a model and when to override it is the same kind of knowledge. It resists being written down, which is why a static instruction captures so little of it.

Good AI work includes knowing what to ask, what context to load, what standard to apply, what output to distrust, what to verify manually, and when to stop iterating. A clean prompt pasted into Notion does not capture that. It is learned by watching the work unfold.

Public AI work needs to make four parts of the work visible: the task the person was trying to get done, the context they gave the model, the interaction pattern they used to prompt and correct it, and the review standard they applied before trusting the output.

If you only share the final answer, the team learns almost nothing. If you share the process, the team starts to build shared taste.

And shared taste is one of the real bottlenecks in AI adoption.

## This is not surveillance

The obvious objection is privacy, and it is a serious objection.

Most employees should not assume their private AI chats will become public. Companies should not quietly ingest everyone’s ChatGPT history and tell themselves they are building a learning system. That will create fear, not learning. It will push good work further underground. It will also create real legal, security, and HR problems.

The right model is intentional public work, declared and bounded.

Teams should create declared spaces where non-sensitive AI work can happen in the open. A product team might have an AI workbench channel. A sales team might have a sanitized customer-research workflow channel. A finance team might have a read-only analysis-pattern channel. An engineering team might have public agent channels for certain classes of non-sensitive tasks.

The boundary matters. Employees need to know what belongs there and what does not.

A safe public AI work system does not ask people to expose everything. It asks people to share the parts of the work that help others learn and that can be shared without creating risk.

That means the company needs rules.

Customer PII stays private. HR stays private. Legal strategy stays private. Compensation stays private. Sensitive financials stay private. Confidential product plans stay private. Personal coaching and interpersonal conflict stay private. If the learning value can be preserved through a sanitized example, sanitize it.

A regulated team should draw the boundary by workflow, not by enthusiasm. A hospital IT group can share non-PHI workflows such as scheduling cleanup, policy search, radiology operations planning, or claims-process documentation while keeping clinical decision support, patient records, and treatment reasoning fully private. A bank can make reusable research, controls testing, and internal-document workflows visible while keeping customer data, suspicious-activity details, and trading strategy out of the channel. The lesson is not “make regulated work public.” It is “create a safe public surface for the parts of AI work that can teach without exposing protected information.”

The competitive-intelligence objection deserves the same treatment. Public internal channels are not public to the internet. They sit inside the same confidentiality, access-control, and departure-policy regime as code, customer playbooks, internal docs, and product plans. If a workflow is too sensitive to be written down anywhere, keep it private. But ordinary internal AI work is not more leak-risky than any other internal operating practice because it involves a model.

The labor-relations objection is real too, but hiding senior AI work often makes it worse. Visibility can show that AI is not replacing senior judgment; it is changing where that judgment gets applied.

The goal is to make useful work teachable.

The difference between apprenticeship infrastructure and productivity theater lives in that goal.

## What leaders should make public

The most important public AI work should come from senior people.

This is uncomfortable, but necessary.

In most companies, senior people have the most valuable judgment and the least visible process. They write the final memo. They make the decision. They edit the strategy deck. They approve the customer plan. But the actual thinking often happens offstage.

With AI, that offstage thinking becomes even more hidden. A senior leader may use an agent to pressure-test a plan, rewrite a board update, compare scenarios, or identify risks. If that all happens privately, the organization never learns how a strong operator uses AI.

A company that wants to build AI fluency should ask senior people to run some non-sensitive work in public.

Not performative demos. Real work. A leader might ask an agent to critique a launch plan in a team channel. A senior engineer might use an agent to investigate a low-risk bug and narrate the review. A sales leader might show how they turn account notes into a call-prep brief, with customer-sensitive details removed. A product leader might show how they ask AI to find weak assumptions in a roadmap narrative.

People do not copy the exact prompt. They see judgment in action, and that is what they carry forward.

They see how senior people frame ambiguity, how much context is enough, how often the first answer is wrong. They watch good operators push back. They learn that using AI well is active supervision, not passive consumption.

Most AI training misses this.

Training tells people what the tool can do. Public senior workflows show people how capable people actually use it.

## How to set up a public AI channel

A practical system does not need to be complicated.

Start with one declared channel per team. Make the purpose explicit: this is for non-sensitive AI work that others can learn from, including reusable workflows, useful failures, prompt revisions, review examples, and playbooks. It is not a dumping ground for every chat transcript and it is not a surveillance feed.

Then pin three examples from senior people in the first week: one research workflow, one drafting or review workflow, and one failure that produced a better review rule. As patterns repeat, turn them into short playbooks with a use case, inputs, prompt or context pattern, output standard, review step, risk level, owner, and last-updated date. Once a week, spend 30 minutes on what saved time, what failed, and what should travel to another team.

This is where the company starts getting smarter.

The piece that makes this work is a constraint, and it is worth being honest about how binding it feels. At Shopify, you cannot work with River in a direct message. The agent only operates in public channels. Direct messages are the most popular thing in Slack and arguably the worst thing for team learning, because they take the most useful exchanges and seal them off one conversation at a time. Forcing the agent into the open is a deliberate friction. Some people will find it annoying, and that annoyance is doing the work. A constraint that individuals find mildly inconvenient is often the thing that bends a whole team toward shared learning, and the leaders worth watching are the ones auditing their own environment for where a small, intentional constraint would do the same.

## What to measure in public AI work

Do not measure token volume.

Do not rank people by how many prompts they submit.

Do not celebrate the person who produces the most AI sludge.

The useful metrics are about learning and reuse.

How many reusable workflows did the team create? How many were adopted by another person or team? How many examples were pinned because they changed how people work? How often did a public workflow prevent duplicated effort? How many stale examples were retired? How many failures turned into better review rules?

The best signal is not “AI usage is up.”

The best signal is “the same mistake is happening less often.”

Organizational learning looks like that. The same lesson stops getting relearned from scratch in five different corners of the company.

The principle that holds these together is simple: share artifacts, not surveillance. Senior people model the work in declared channels. Customer, employee, legal, financial, and strategic sensitivity stays out. Failures are training material, not blame material. And the metric is reusable workflows and avoided rework, not token volume.

Anything that does not pass those tests does not need to be in the public channel. These rules are intentionally plain because the problem is not complicated in principle. It is complicated in practice because companies keep collapsing three different things into one bucket.

They confuse visibility with surveillance, adoption with learning, and prompt sharing with apprenticeship.

The Monday-morning version is small. Create the channel, write one pinned message that says what belongs there and what stays private, and have the senior person post one real piece of non-sensitive work: the request, the back-and-forth, the correction, the version accepted, and the review note. Pin two more examples in the first week. By month two, mid-level operators should be posting their own. By month four, the channel should be producing reusable playbooks. Total senior-time investment to start the flywheel: about ninety minutes across the first two weeks.

A company does not become AI-native because every employee has a private conversation with a model. That may make some individuals faster. It may even produce meaningful pockets of value. But it does not automatically make the company smarter.

A company becomes smarter when the lessons travel.

What travels goes beyond the prompt. The correction, the review standard, the failure mode, the reusable workflow, and the senior person’s judgment all become visible enough for the next person to learn from them.

That is the real promise of public AI work. Not mandatory usage, not productivity theater, not another dashboard showing how many people opened a chatbot this week.

The practical question for leaders is direct: what AI work inside your company is making one person better, but leaving everyone else behind?

If that work stays private, the company keeps paying the same tuition.

The promise is apprenticeship at scale.

![](https://substackcdn.com/image/fetch/$s_!X9Ur!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F240553da-409a-4efc-a4fa-3181a5689246_1254x1254.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/public-ai-work-team-learning) on 2026-05-26T17:12:15-04:00*

YOUTUBE TRANSCRIPT
So Shopify's internal coding agent is named River. In one 30-day stretch this spring, 5,938 Shopify employees used River across more than 4,400 Slack channels. In a single week, River opened 1,800 And the numbers are what most people grabbed onto when Toby Lutke, CEO of Shopify, posted about all of this earlier this month.

Underneath those numbers, though, there's a design choice that is actually the story. River doesn't work in private. Every conversation an engineer has with River happens in a public Slack channel. Other engineers can scroll back through the thread, they can see how a senior engineer scoped the task, what context she loaded, where the agent got stuck,

what she rejected, what she kept. That's the part that nobody is copying. Okay, let's get into the deeper meaning here. Most companies have a hidden AI problem and it has nothing to do with tooling. Your employees are using AI all day long. They're asking ChatGPT to rewrite emails. They're using Claude to reason through a tricky customer issue.

They're running coding agents to inspect repos. They're getting Copilot to summarize 40-page docs in two minutes. They're quietly building small workflows that save them hours every single week. and almost all of it is happening in private, in private software, private windows. This is not a conversation about whether it's secure. It's about the fact that it's not shared.

The good prompt disappears into one person's chat history. The clever correction stays inside one employee's The workflow that worked yesterday gets rediscovered next week by the next person who builds the same thing from scratch because nobody told them it existed. That is a real thing. I have talked to Amazonians who will tell me that there are six,

eight, ten different vibe coded tools inside the company for the same problem. So individuals are getting smarter, the company is not, and that is the gap. Most companies have already bought the tools they need, so the problem at this point isn't necessarily tooling per se, it's visibility. I wrote about this same shift on the Substack last month,

about how the comprehension layer is what gets rewarded now, not the output layer. If you want the longer version of why all of this matters at the individual level, that's where you dig in. Now, we're going to keep moving at the team level because that's what this video is about today.

Every quarter, your team rediscovers the same lessons. The workflow your best operator nailed last month is invisible to the new hire. They build it from scratch. For most of human history, the way we learned skilled work was by being near skilled workers. And I don't think that's changed.

You watched how the senior person framed the problem, what they noticed, what they ignored. You picked up the bits that didn't show up in any training manual. You learned the craft from the process as much as from the finished product. Now think about what happens when most of the actual thinking in the AI age happens

in a private window. The junior employee never sees how the senior person instructs their agents. The new manager never watches an experienced operator verify an answer. The correction that made the workflow reusable stays invisible to everyone except the person who wrote it. Everyone is alone with their model,

which means everyone has to rediscover the same lessons from scratch. and I'm calling this the apprenticeship gap and it's getting wider every single quarter because more of your team's actual thinking is happening inside chat windows that nobody can see. One of the best examples I know of how hard it is to get implicit knowledge into digital systems,

into the way we learn and understand, comes from the manufacturing era and specifically from John Deere and from other similar companies that that are used to building complex physical machine tooling. There is a whole generation of American workers who are used to working on complex tooling in manufacturing environments who are nearing retirement, and they're extraordinarily skilled,

and they know things in their fingertips, literally, that they can't speak or express. It goes back to Polanyi's paradox, the work is more than we know. There is an entire effort of what I know PMs who have done this to grab their knowledge and figure out how to turn it into a machine learning algorithm before they retire.

And there's no new people coming up in the manufacturing industry with the same knowledge in their fingertips because there's just fewer and fewer people stepping into factories. And so we need to find ways to digitize it. I think what's really interesting about that is that when you talk to a PM who's done that, and I have,

You hear mostly how hard it is to get it right. There is literally no way to get the full felt experience of someone's ability to turn a particular steel piece of machinery into an algorithm. that you can get close, you can approximate, it's not perfect.

Which is why key bottlenecks in our supply chain actually are driven by a single person with extraordinary ability in their fingertips. And the world is built by people like this. So there's one person who knows how to paint the racing stripes on a Rolls Royce. They're the only ones. There's one person somewhere in Oregon, I think,

who's a machinist, who knows how to test the quality on a particular type of Boeing screw and they're the only ones. And by the way, if you think they're retired and that's the issue with Boeing, that is not the issue with Boeing, that is a much longer conversation. They are not the problem. But that's what I mean.

Like that physical knowledge is hard to speak. It's hard to communicate. And we have the same thing in software. And I think it's really important to learn from our physical engineering counterparts when we think about solving these kinds of software problems. And that's why this video matters. So what does public AI work actually look like?

Because just dumping every chat transcript into a Slack channel is not what I'm suggesting. What you want to make visible is four parts of the work. One, the task. What was the person actually trying to get done? Two, the context. What did they tell the model? What did they paste in? What did they leave out?

Three, the interaction. How did they prompt? What did the first answer look like? How did they push back? What did they ask the model to redo? And four, the review. What did the human accept What did they reject? What did they verify manually and what did they rewrite? And why?

If you only share your final answer, the team learns almost nothing. If you share all of those four parts, the team starts to build a sense of shared taste. And shared taste is one of the tremendous bottlenecks in AI adoption right now. A prompt library doesn't fix this, right?

A prompt library captures static instructions, but it misses all of that messy context. It misses the revisions. It misses the moment when the model produced something that looked plausible and the human said, no, that's wrong for our customer, or no, that violates our tone, or no, that analysis skipped the constraint that actually matters here.

And I do that a lot. In fact, when people look over my shoulder when I'm using AI, one of the things they notice is I say no to the model a lot. And I say no very quickly. And I say no based on a very rapid assessment of the quality of what the model is producing for me.

And that tends to surprise people. And that's why it's so important to share these things. So the most valuable part of AI work is rarely the prompt. It's the surrounding habit. The prompt is the easy part to copy. The habit is what teaches us and helps us to learn.

On the Substack, I broke down all four parts with a worked example for you, right? The task, the context, the interaction pattern, the review standard. So if you want the full version, how this looks in practice, The link's in the description. Okay, the objection that tends to come up first when I describe this is privacy.

And it's a very serious objection, so let's be really honest about it. Your employees should not assume their private AI chats are going to just become company property. Now, I know on paper most people have agreements that say whatever you type into the company AI is the company's. In reality, most people don't act that way.

And if you were to say every one of your AI chats is default public, a lot of people would just stop using AI a lot. Like that's just the reality. And you don't want to push good work underground. So what I'm describing is the opposite of that. I'm describing declared spaces and

And that's the beauty of the Shopify example. Senior people running real work where the team can watch. Toby does this himself with River in a public channel. The point of the channel is to make learning visible full stop. You create declared channels. In Slack, a product team gets an AI workbook bench channel.

A sales team gets a sanitized customer research workflow channel. A finance team gets a read-only analysis pattern channel. The engineering team can have public agent channels for certain classes of non-sensitive tasks. The boundary is the way this works well, right? Your team needs to know exactly what belongs in the public channel and what does not.

Customer data has to stay private. HR has to stay private. Legal strategy has to stay private. So there's things that you have to keep private. But If you can prioritize everything around that and say, can we learn together in a public channel, you can get a tremendous amount of momentum.

You should be able to draw up a workflow where you can say, I can put clinical decision support, I can put anonymized patient records, I can put treatment reasoning into a space that is is public so that we can see the agent operate against it, but not in a way that discloses any PII or violates HIPAA.

And that takes some work and it's not perfectly easy, but the alternative is that you take something like HIPAA that was intended to protect patient privacy in the U.S. and it turns into a constraint on AI learning. and you don't want that. You want to be in a situation where you're thinking creatively about how to be

compliant but how to still expose relevant context that other people can learn from as far as how they interact with AI and reasoning models. So the takeaway here is not make regulated work public in a non-compliant way. I'm not advocating that. The lesson is create a safe public surface for the parts of AI work that can teach

without exposing protected information and lean into that as much as you can. There's a fuller treatment of the regulated industry version on the Substack, what a hospital IT team or a bank can actually put in a public channel without crossing a line. If you're operating in a high regulated environment, I think that one's worth a read.

Okay, here's where this gets uncomfortable for a lot of us watching. The most important public AI work in your company has to come from senior people. In most companies, your senior people have the most valuable judgment and also the least visible process. They will write the final memo, but you don't know how they did it.

They'll make the decision, but they don't tell you why they made that decision. They'll edit the strategy deck. They approve the customer plan. If all of that happens in private, your organization never gets to see how a strong operator actually uses AI. The fix is really clear here.

Ask your senior people to run some non-sensitive work in public and equip them to do so. Make it easy the way River is easy at Shopify. Real work, things that have stakes. A leader asking an agent to critique a launch plan in a team channel.

A senior engineer using an agent to investigate a low-risk bug while narrating the review out loud. A sales leader showing how they turn account notes into a call prep brief with customer-sensitive details stripped out. a product leader asking AI to find weak assumptions in a roadmap narrative. The junior person on the team doesn't copy the prompt anymore.

They actually see the judgment in action. They see how senior people frame ambiguity, how much context is enough, how often the first answer is wrong. They watch a good operator push back. They learn that using AI well is active supervision, not passive consumption. Most AI training doesn't get close to this level of quality.

Because training just tells people what the tool can do, right? public senior workflows show people how capable individuals who are at the top of their craft actually use AI. And by the way, that is exactly what Toby is modeling at Shopify. As the CEO, he also considers himself an individual contributor, and he has

Deliberately putting his work in a public channel, allowing other people to ask questions of his agent, allowing other people to critique his choices in that channel and work with his agent as he works with the agent to shape results. Is it a little bit chaotic? Yes. Is he still the one who's telling the agent what to do?

Also yes. But that open room format for the work he does with his agent allows him to teach and socialize what he wants to drive through the company in a way that nothing else does. So start with one declared channel per team. Steve, write a pinned message at the top that says what the channel is for.

Make sure that it's for reusable workflows and useful failures and for prompt revisions. And make sure that it's a default. One of the ways that River works at Shopify is that you cannot interact with River in a DM. It's not possible. Have those kinds of constraints. And as patterns repeat, and they will repeat,

turn the repeated patterns into playbooks or into skills or into inputs for the next challenge that you're facing. Because you can learn deliberately from the channel. And by the way, yes, you can use AI to brush through that channel and gather those lessons learned.

That's one of the fastest ways to socialize real AI usage that I've ever found. And that means that your company actually starts to get smarter. The whole team starts to get smarter. Junior folks get smarter. Not because everyone has the same prompt, but because the organization now has a way to turn what one person learned into

what the whole team can use. Total senior team investment to get the flywheel started, it's not that long, right? Like you just have to be willing to do it and you have to be willing to comply with, frankly, a constraint that can feel a little bit binding.

You can only interact with this agent in a public channel, right? Well, you got to be willing to do that. And then when you do that, you start to find out that you are effectively multiplying your time and impact in ways you didn't realize. And that's what Toby concluded when he was actually writing out his whole

reflection on apprenticeship and the age of AI. Last thing, what does it matter to measure in this particular environment? We've talked about things like token volume, they have their place. Tasks or workflows, they're definitely useful. But I think we need to shape some useful metrics around learning and reuse. How many reusable workflows

How often did a public workflow prevent duplicated efforts somewhere else? That one's hard to measure, but it's worth trying. How many stale examples got retired? How many failures became better review rules? The best signal sometimes is not AI usage is up. The best signal sometimes is that the mistake is happening less often on our team.

And that's how organizational learning looks. And it's hard to measure, but it's worth trying to because it reflects reality better. So the practical question for the leaders out there isn't whether your team is using AI. Most of them are using it a lot already. The practical question is what AI work inside your company is making one person

better while everybody else falls behind. Because if that work stays The companies that pick The ability to learn from one another are the ones that start to compound organizationally. So if you want to dig into this, if you want to look at what channel rules look like, get a playbook to get started for different industries,

that's on the Substack, deeper dive there. I just want to call out as we close here that the biggest thing that you can take away from this video is actually the power of constraints to drive this collaboration. I think it is undersold how this is getting facilitated at Shopify by the simple

rule that agents never run in DMs and Slack. DMs are so popular in Slack and Slack has been fighting them from a product perspective for a while because they're demonstrably bad for teamwork, but they're very popular with individuals. They allow you to say, I can get a response, I can just ping someone, etc.

By insisting that agents only work in public channels, you are putting a binding constraint in favor of collaboration and learning. And so the larger lesson I'm not talking about Slack per se. The larger lesson is that constraints that are creative and careful shape incentives toward learning. And you should audit your environment and say,

where are we putting intentional constraints that individuals may find frustrating sometimes, but that on the whole promote collective public learning for AI? That is the takeaway I want you to have. Cheers. I'll see you next time.