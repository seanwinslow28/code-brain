---
title: "Your prototype graveyard is leaking secrets. The Prototype Classifier + Demotion Audit decide what stays"
source: "https://natesnewsletter.substack.com/p/product-management-cheap-software-governance?r=1z4sm5&utm_campaign=post&utm_medium=web"
author:
  - "[[Nate]]"
published: 2026-05-28
created: 2026-05-29
description: "Watch now | PMs used to ration engineering. Now they have to classify abundance."
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain: [product-management]
ai-context: "Nate Jones argues the PM role is shifting from rationing scarce engineering to classifying an abundance of cheap prototypes, introducing a Prototype Classifier + Demotion Audit to decide which working artifacts become products, internal tools, or deletions."
---
Product management has always been a rationing job. Most ideas would not get built. Engineering time was scarce. Coordination was slow. A roadmap was partly a strategy document and partly a rationing system, and product managers helped decide which customer problems, executive priorities, technical constraints, and market bets deserved the company’s limited ability to make software.

That role is changing, because the cost of a first version has collapsed. The thing entering the product conversation is no longer a request. It is a working artifact. A dashboard. A lightweight app. An agent that already touches a system of record.

The scale this reaches is already documented. Inside Microsoft, employees have built more than 1 million Power Platform citizen-development assets: 18,000-plus environments, 170,000 apps, 50,000 automated flows, 1,200 chatbots. Most companies are nowhere near that, but the shape of the problem is arriving everywhere, and the product function is the part of the org that has to absorb it.

The old model asked, “Should we build this?” The new model starts one step later: somebody already built something. Now the company has to decide whether it should matter. The PM is no longer mainly a coordination role around scarce engineering. It becomes the discipline that classifies software abundance into market value, internal reliance, or deletion. That is a more strategic job, and a more technical one. Get it wrong and the failure is not loud. You do not get an outage on launch day. You get a pile of half-real tools nobody owns, spreading into systems of record before anyone decided they were allowed to.

**Here’s what’s inside:**

- **Why the old roadmap filter broke.** When a first version costs almost nothing, rationing engineering time stops being the job. You get a clear read on what replaces it, and why the shift is more strategic than the prototyping conversation suggests.
- **A four-state ladder for classifying what your team builds.** Personal tool, team beta, supported internal product, customer-facing product, with the specific user-count and risk thresholds that move a tool from one rung to the next.
- **The demotion triggers almost everyone skips.** The exact signals that tell you a tool you still support has stopped earning it, so you stop paying to keep dead software alive.
- **Two prompts you can run this week.** One classifies any employee-built tool into its real production class and names what promotion would take. The other audits a tool you already support and tests whether it should be demoted.

The cost of making software fell. The cost of being wrong about what you depend on did not. Below, here is how the product job changes when production stops being the scarce input, and the two prompts that turn it into something you can run on Monday.

## LINK: Grab the Prompts

Companies almost always know how to promote tools. They rarely know how to demote them. Something useful appears, earns a rung, and keeps it forever, until the supported-tools list becomes a museum of things nobody remembers depending on. These two prompts run in both directions on purpose. The Prototype Classifier takes one tool you can point at and tells you what it is right now, what moving up would take, and the one thing that breaks downstream if it disappears. The Demotion Audit asks the question the up direction never does: is this still worth what we pay to keep it alive? Bring real facts to both. Neither prompt will guess on your behalf, because the whole value is surfacing what you haven’t written down yet.

## The old PM job was built around scarcity

Product rituals make sense when software is expensive.

PRDs, roadmap reviews, planning cycles, launch checklists, prioritization meetings, and intake processes all slow work down before engineering time gets consumed. The friction was the design, not a flaw in it.

When software is expensive, the company needs a filter. You cannot afford every stray idea to become a ticket. You cannot afford every department to clone the product. You cannot afford every half-understood customer request to ship.

The PM helped run that filter.

AI weakens the filter because it changes what people can produce before they reach product and engineering. The top of the funnel used to be words, mockups, spreadsheets, and persuasion. Now it includes working tools, dashboards, automations, agents, and half-real products.

A product leader can no longer wait passively for polished business cases. The useful signal may already be running inside a team. A prototype may reveal hidden demand before the market research does. A local automation may expose a platform gap. A messy agent may show that customers want an outcome the official product does not support.

The PM’s job is to understand that signal, not suppress it.

The company needs broad building because that is where new demand becomes visible. But broad building without judgment becomes sprawl. Useful work stays hidden, risky work spreads without support, and nobody knows which tools the business now depends on.

The product function has to hold both ideas at the same time: let more people build, and decide what the business will rely on.

## The supply curve moved

The public software ecosystem shows the direction of travel. GitHub’s 2025 Octoverse counted 630 million total projects and 4.3 million AI-specific projects. Most of those projects will never matter to anyone beyond the person who made them. That is what abundance looks like.

The world is producing more software-shaped work than product organizations were built to evaluate.

The same pattern is already inside companies. The Microsoft number from the open is worth sitting with for a second: 1 million citizen-development assets, documented as far back as 2023, governed through inventory, telemetry, permission review, environment controls, and data policy. The age of the figure is what should bother you. The problem was already this big before the current wave of AI building tools arrived, which means most companies are now racing to catch up to a curve that bent years ago.

Microsoft did not present this as a reason to stop employees from building. It used governance as the way to let employees build while protecting the company. That is the posture product leaders need. Broad building is good. Ungoverned reliance is not.

The security data shows what happens when posture is missing. GitGuardian’s 2026 State of Secrets Sprawl report says AI-service secrets exposed on public GitHub reached 1,275,105 in 2025, up 81 percent year over year. Faster creation means more credentials, more local workflows, more integrations, and more places for access to leak.

Product leaders inherit that problem when useful tools spread before anyone decides what class of thing they are.

So a useful prototype is only the start of the evaluation. What data does it touch, what systems can it write to, what happens when it fails, who owns it, how is it checked, and what is the company promising once other people start depending on it? These are product questions now, not engineering ones.

## PMs need more market judgment, not less

It is easy to hear all of this as an internal tooling problem. That would make the role too small.

Cheap software makes PMs more responsible for market judgment, not less.

When building is expensive, weak product thinking can hide behind execution constraints. A team can spend months building one thing and blame the cost of production for why it could not test more. When first versions get cheap, that excuse weakens.

The question becomes sharper: why are we building this at all?

The PM has to understand the market well enough to aim production.

Which customer problem is worth solving? Which workflow is close enough to money, retention, trust, or habit that it matters? Which competitor feature is noise? Which customer request is a symptom of a deeper problem? Which internal prototype reveals real demand, and which one is just a local convenience?

Those are product judgment calls, and most PMs were never trained to make them.

AI also makes the role more fluid. The line between product, design, engineering, data, research, and operations gets blurrier when a small team can move from customer insight to working prototype quickly. The PM has to move across that boundary without pretending the boundary disappeared.

They need enough technical fluency to understand what the system can do and enough market clarity to decide what the system should do. The PM becomes less of a translator between business and engineering and more of an accountable thinker about what should exist in a market where production is no longer the scarce input.

## The prototype commons needs stewardship

The prototype commons is the informal space where new tools appear before the company has classified them: scripts, dashboards, agents, automations, and half-real products built because employees can finally solve problems that never made it onto a roadmap.

That space is valuable. It reveals hidden demand, missing platform primitives, customer pain, and internal workflows that the official product process has not understood yet.

But a commons still needs stewardship.

If nobody owns it, useful work stays invisible and risky work spreads without the right support. If product shows up only to say no, employees will hide useful tools until something breaks. The right posture is open discovery: show us what you made, what problem it solves, who uses it, what data it touches, and what you learned.

Run a weekly prototype review. Keep it small. Product, platform or engineering, security or risk when data is involved, design or research when user experience matters, and the artifact owner.

Do not call it a steering committee. The name matters because the posture matters. A steering committee sounds like permission. A prototype review sounds like discovery.

The intake form should fit on one page.

What problem does this solve? Who uses it today, and how often? What systems, data, credentials, or customer surfaces does it touch? What happens if it gives a wrong answer, fails, or disappears? Who owns it today, and who is the backup? What evidence shows it is useful? What should happen next: stay personal, move to team beta, become supported internally, or enter product discovery?

Each review has three possible outcomes.

Leave it where it is, with maybe one small safety fix. Promote it one step. Or harvest the learning and retire it.

That last option matters. The goal is not to put every prototype on a roadmap. The goal is to learn from abundance without becoming dependent on everything abundance produces.

## The production-class ladder

Once a company accepts that more people will build, it needs a way to decide what each thing is.

The first version of a thing and the supported version of a thing are not the same object.

That sentence is the reason for a production-class ladder.

The first state is the personal tool. One person uses it. It can be scrappy. It can change every weekend. It should stay away from sensitive data unless the company has clear rules for local handling. The goal is learning and personal leverage.

The second state is the team beta. A small group uses it regularly. It solves a real problem, but it is not yet a formal internal product. It needs a named owner, a backup owner, a short description, a list of systems it touches, and a failure plan. If it touches credentials, customer data, money, compliance, or production infrastructure, it needs review before it spreads.

The third state is the supported internal product. This is software the company depends on. It needs product ownership, engineering or platform partnership, access management, monitoring, documentation, support, auditability, and a change process. The difference is obligation. People now expect the thing to work, and the company has to make sure it does.

The fourth state is the customer-facing product or feature. This is part of the company’s external promise. It needs the usual product standards plus AI-specific evaluation and governance where the surface requires it: model performance, data handling, fallback behavior, user control, support readiness, and policy compliance.

The thresholds will differ by company, but they need to exist. A useful first pass is simple: one primary user for a personal tool, three or more regular users for four weeks for a team beta, ten or more users or meaningful outage cost for a supported internal product, and any external user, revenue, contractual reliance, public documentation, or support commitment for a customer-facing product.

The ladder keeps building fast without pretending every useful thing deserves the same process.

In the old model, PMs decided what entered engineering. In the new model, PMs also decide what gets promoted out of the prototype commons.

## The strongest objection

The strongest counterargument is that the production-class ladder reintroduces the bottleneck the article is trying to escape.

If every employee-built tool has to pass through product review before a team can use it, then the company has rebuilt the old roadmap intake process under a new name. The artifact arrived early, but the organization still forces it to wait in line.

That objection is right if the ladder is default-deny. The point is to make it default-allow at the low-risk end and explicit only when the artifact creates broader obligation. A person should not need product approval to build a personal helper. A team should not need a roadmap slot to try a beta that touches low-risk data and has a named owner. The review does not decide whether employees may build. Its job is to notice when an artifact has started to matter enough that the company owes it a class, an owner, and a support path.

The old intake process controlled what got built. The new promotion process controls what becomes relied upon.

Those jobs are different.

The second objection is that promotion will be political. The artifacts built by the favored team will get support, while better artifacts from less powerful teams get ignored.

That can happen, and the mitigation is the written decision log. A single line is enough: owner, backup, next review date, the condition that would promote it, the condition that would demote it. Every promotion, denial, retirement, or request for more evidence leaves a record of users, usage, risks, systems touched, failure cost, owner, and reasoning. Politics survives that, but it has to argue with what the log says.

## Demotion matters

A ladder needs a way down. Without one, the company keeps paying to support tools it stopped using and forgot it had.

The ladder needs a downward direction.

A team beta should move back to personal tool if usage falls to one person, if the backup owner disappears, or if the original problem stops recurring. The tool may still be useful. The company should just stop pretending a team depends on it.

A supported internal product should move back to team beta if it loses its owner, falls out of the operating rhythm, or no longer justifies support. That demotion needs a notice period and a migration plan because people may have built work around it. The notice does not have to be elaborate: a date by which the thing stops being supported, posted where the people who use it will see it, with a named alternative or a clear statement that there is none.

A customer-facing feature should be sunset when the external promise no longer earns its maintenance cost.

Cheap creation should make product leaders more willing to retire weak things. Without disciplined demotion, the company accumulates product debt faster than it can name it.

This is where the ladder becomes more than a launch framework. It becomes a maintenance discipline. The promotion question is loud. The demotion question is the one almost nobody asks: is what you already support still in the class you put it in?

## The real PM shift

The product conversation has spent a lot of time on how fast AI can move an idea into a prototype. That was useful for a moment. It showed that the cost of first versions had collapsed.

The next question matters more.

What happens after the prototype exists?

Three answers fail. Doing nothing leaves a graveyard of demos. Sending everything to production produces chaos. Locking building to central product and engineering wastes the creative capacity AI just unlocked.

The better answer is a default-allow system for experimentation and a deliberate promotion path for work the business will rely on.

But the larger shift is upstream from the ladder.

Software abundance makes product judgment more important. PMs have to know the market better, understand the technical system more deeply, and form clearer opinions about what should exist. They have to see when a prototype is a local helper, when it reveals a real workflow, when it should become infrastructure, and when it should die.

The binding constraint moves from “can we make it?” to “should this exist, who is it for, what standard does it need to meet, and what are we willing to rely on?”

Engineering used to be the scarce thing. The scarce thing now is judgment. Look at what your team built last quarter. Some of it is already yours to own. The question is whether you know which.

![](https://substackcdn.com/image/fetch/$s_!4266!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d9990e4-359b-4c04-9bc8-8bbc4a2e124e_1024x1024.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/product-management-cheap-software-governance?r=1z4sm5&utm_campaign=post&utm_medium=web) on 2026-05-29T14:48:14-04:00*

YOUTUBE TRANSCRIPT
So I'm really excited about this one because I feel like as a PM for a very long time, I have something to say about product management and what is happening now. And so much of what I see in training courses is around the idea that PMs are becoming prototypers. PMs are using Lovable. PMs are using Claude Code.

PMs are using codecs to prototype. That's fine. I don't think that is the heart of where product is going. I think that's just table stakes at this point. And so I want to have a deeper conversation with my fellow PMs about What is happening in our discipline and how we need to change and evolve in the age

of AI because I think the prototyping advice is oversold and we need to be very deliberate about what we're doing because it comes back to the same idea that I've been kind of really with the idea that AI makes generation easier so it moves the bottleneck and we

need to be very intentional about how we leverage human expertise from there to make sure that we are effective with our intelligence, our scarce human If you're wondering what AI looks like at a big company, Microsoft has a story for you. They have built more than one million power platform assets inside the company.

Power platform is what they call their sort of AI tool, right? That includes more than 18,000 different robot environments or agent environments, 170,000 power apps, 50,000 power automate flows, and 1,200 chatbots. The obvious story here is that low code and AI are letting more people build software, right?

The real story is that product management is moving from rationing scarce engineering to classifying and strategizing with software abundance. That matters because the thing arriving in the product conversation is no longer just a request in most cases. It's often a working artifact. It's a dashboard, a workflow, a lightweight app, a local automation, a customer-facing prototype,

maybe an agent that already touches the system of record. So the old product question was, should I even build this? The new product question often starts a step later. Somebody already built something. Now the company has to decide whether it should matter and sense make out of it.

This is the PM shift that I want to talk about today. It is becoming the discipline that classifies software abundance into market value, internal tooling that's useful, or that decides to delete it. And that's a much more strategic job. It's also a much more technical job. Best PMs in the next few years will not be ticket brokers.

They will be people who understand markets and users and workflows and technical systems and data and evals and permissioning and cost and reliability and trust well enough to decide where software abundance ought to be pointed. There is not much room left for the non-technical PM. I don't mean every PM has to become a full-time engineer.

I mean AI products are technical systems and the technical aspects of AI are profoundly determinative of their overall behavior. So we need to understand them well to work with them. Product decisions now involve model behavior and agent loops and data access and workflow boundaries and retrieval and evaluation and latency and cost and permissions and failure modes.

A PM who cannot reason about those things is missing the product. At the same time, AI does not empty human value out of the product work. It actually just shifts the bottleneck. When software production gets cheaper, the scarce thing is not the first version, the first prototype. The scarce thing is great judgment about what ought to exist,

what ought to be deleted, who the product is for, the standard it needs to meet, and what the company is willing to bet on. So the old PM job was really built around scarcity. Product rituals make sense when software is expensive, so PRDs and roadmap reviews and planning cycles and launch checklists, prioritization meetings,

all of that is built around slow work so that engineering time is consumed deliberately. That was the whole point. When software is expensive, the company needs a filter, the PM is the filter. You can't afford every stray idea, you can't afford every department cloning the product, and the PM had to run the filter.

AI kind of destroys that filter because because it changes what people can produce before they ever reach product and engineering. And so the top of the funnel used to be words and it used to be mockups and spreadsheets and persuasion, but now it's got working tools and dashboards and automations and agents and half real

A product leader can no longer wait passively for polished business cases in that world. The useful signal may already be running inside a team along with a lot of noise that isn't useful. So what you need to do in that world is not to shut it down.

I hear a lot of PMed instincts to say, well, our job now is to prototype and nobody else's. No, everybody's job is to prototype. The local automation may expose the platform gap. A messy agent may show that customers want an outcome the official product doesn't support. and maybe the customer service rep built that, not the PM.

So you need to understand where the good ideas in your org are coming from in the form of artifacts and prototypes. The company needs broad building because that is where new demand becomes visible. But broad building with The product function has to hold both ideas at the same time.

Let more people build and decide carefully what the business will rely on. The world is producing more software-shaped work than product organizations were ever built to evaluate. The same pattern is happening inside companies, right? Microsoft's internal power platform ecosystem is a great example here. More than a million citizen development assets inside one company with governance

built around inventory and telemetry and permission review and environment controls and data policy. Microsoft didn't share all of this as a reason to stop employees from building. Instead, it presented governance as a way to let employees build while protecting the company. GitGuardian's 2026 State of Secrets sprawl report says AI service secrets exposed

on public GitHub reached 1.2 million in 2025. It's up farther now, and it was up 81% year over year in 2025. It's going to climb another 80 or 100% this year, I bet you. Faster creation means those mistakes. It means more credentials, more local workflows, more integrations, and more places for access to leak.

Product leaders inherit that problem when useful tools spread before anyone decides what class of thing they are. The question is not only whether a prototype seems useful, the question is what data does it touch? What systems does it write to? Who owns it? Those are now product questions, not just engineering questions,

and they require more of our technical market judgment, not less. It's so easy to hear all of this as an internal tooling problem, but that would make the role too small. Cheap software makes PMs more responsible for market judgment, and that includes judgment from the market around all of our tooling inside and outside the business.

But now first versions are really cheap, and so the question for us becomes really sharp. Why are we building this at all? The PM has to understand the market well enough to aim production successfully. Which customer problem is really worth solving here? Which workflow is close enough to money and retention and trust

so that it's forming a really good habit with customers. Which competitor feature is just noise? Which customer request is a symptom of a much deeper issue? Which internal prototype reveals real demand and which one is just local convenience for one team? That's not product management. That is product judgment.

So what does the new job look like in practice? Let's start with the prototype commons. The prototype commons is the informal space where new tools appear before the company has classified them, where scripts and dashboards and agents and automations and half-real products built because employees can finally solve problems that never made it onto a

roadmap all sprout up together. That space is messy, but it's really valuable. It reveals hidden demand and missing platform primitives and customer pain and internal workflows that the official product process has not yet understood. But a common still needs stewardship. If nobody owns it, useful work stays invisible and risky work spreads without the right support.

If a product shows up only to say no, employees will start hiding useful tools until something breaks. So within that context, I think the better posture for PMs A production class ladder has a few rungs that help you make sense of this messy prototype commons and apply your PM judgment in ways that encourage innovation

rather than discourage it. So let's start with personal tools. A personal tool is for one person, right? It can be scrappy. It should stay away from sensitive data unless the company has rules for local handling. And it's something that you don't have to have a lot of other standards around. Go up a level.

A team beta is used by a small group. It will need an owner. It will need a backup owner. It should have a short description. It should talk about the systems it touches, why it benefits the team, and there should be a failure plan.

Go up another level, a supported internal product is software the company does depend on. It does need product ownership. It needs platform partnership. It needs access management and monitoring. It needs documentation and support and auditability and a change process. It's much more serious. A customer-facing product or a feature is part of the company's external process.

This is the fourth rung on the ladder. It needs the usual product standards plus AI-specific evals and governance where the surface requires it. And the important point is that these are very, very different classes and we shouldn't mix them up. The first version of a thing and the supported version of a thing don't have to be

the same, right? In the old model, PMs decided what entered engineering and that is what became supported and that's what became official software. In the new model, PMs also decide what gets promoted out of the prototype commons. And demotion matters just as much as promotion here, right?

A ladder that only moves upward is going to become a junk drawer. Everything eventually gets to production or gets to some kind of support level, and it's just a pile of old obligations that nobody wants to own. So you need to think about what kinds of customer promises you want to make in production,

what kinds of customer promises you want to make internally, and where you want to leave the rest to be intentionally demoted or left at the personal software level. And that is a real PM shift, because if you don't do that, the company will pay support costs on dead software faster than it can name it.

That is the new tech debt. And so the product conversation has spent a lot of time on how fast AI can move an idea to a prototype. And I hear that over and over again from PMs. That was useful. It showed us that the cost of first versions have collapsed and we get to play a

part in that as PMs. I think the next question matters more. What happens after the prototype exists? If the answer is we don't know, we don't have a plan, the company gets a graveyard of demos. If the answer is everything goes to production, the company gets chaos. If the answer is only central product in engineering may build,

the company wastes a ton of creative capacity that AI just unlocked. The better answer is a default allow system for experimentation and a very, very intentional promotion path governed by product for work the business will rely on. And so that's the decision rule I recommend. If you're a PM, stop asking only whether your team can build faster.

Ask what class of software you're looking at. Is it a personal tool? Is it a team beta? Is it a supported internal product? Is it a customer facing promise? Then ask the harder question. Should this exist? Who is it for? What standard does it need to meet? And what are we willing to rely on?

That's the new product job. In the meantime, keep your head up as a PM. This is an incredibly exciting time to be in product. For so long, we've had to say we can't build everything. Now we finally get to play the other side of the game board. We get to say we can build everything.

What should we build? And I love that we get the challenge of exercising our judgment. So be the PM that is post-prototype. Figure out how to use your judgment to build a true production class ladder to help your organization channel its creative energy to build what matters for customers. I'll see you next time. Cheers.