---
title: "Executive Briefing: Point an agent at your calendar and your repo, and it will show you the rules your company is actually running. Here are the 15 I wrote for mine."
source: "https://natesnewsletter.substack.com/p/ai-native-company-rules?r=1z4sm5&utm_campaign=post&utm_medium=web"
author:
  - "[[Nate]]"
published: 2026-07-11
created: 2026-07-14
description: "Watch now | The fifteen rules I wrote for my own company, the five questions that turn one resented ritual into a rule that can run, and the ladder that decides how hard that rule is allowed to bite."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [claude-mastery, life-systems]
ai-context: "Nate's framework for writing an AI-native company's operating rules explicitly — separating values, rules, runtime checks, and human appeals so agents (not just people) can enforce them."
---
Your company already has commandments that nobody voted on or consciously decided to enforce.

They live in the recurring meeting nobody questions, the roadmap template everybody fills out, the approval chain nobody can explain, the person everybody checks with before acting, and the sentence “that is just how we do it here.”

Most were never written down, because scarcity wrote them for you. Engineering time was expensive, so a document rationed it. Context moved slowly, so a meeting carried it. Mistakes were costly and hard to catch, so an approval chain sat in front of them. Nobody had to argue for those rules. The conditions argued for them.

AI is dissolving a lot of that scarcity. It has not dissolved the judgment underneath it.

That leaves an operator holding a set of rules written by conditions that no longer hold, with no obvious way to sort the ones still doing work from the ones running on inertia. And there is a second problem sitting behind the first. The rules you decide to keep now have to be legible to something that is not a person. Agents act on written context. A rule that lives only in the head of your longest-tenured director does not exist, as far as your stack is concerned.

Earlier this year I wrote fifteen commandments for my own organization because I needed to make those choices explicit. They are short, deliberately severe rules about speed, product, engineering, meetings, documentation, teamwork, design, and customer experience. The style is half joke and half constraint. “Thou shalt not” is hard to mistake for a suggestion.

I am not asking you to adopt mine. Copying somebody else’s constitution is how you end up with a document that enforces nothing. What follows is the machinery for writing your own.

**Here’s what’s inside:**

- **Separate the four objects most companies blur together.** A value, a rule, a runtime check, and a human appeal do different work and deserve different owners. Confuse them and your culture document enforces nothing.
- **Watch a prohibition collapse without its replacement.** Killing roadmaps only works because two other commandments absorb the job the roadmap was doing. Copy the ban by itself and you have deleted what used to coordinate your company.
- **Read all fifteen, plus the two piles AI leaves behind.** The work nobody can review fast enough, and the work nobody remembers to delete.
- **Run the five-question worksheet on the rule everybody in your organization resents.** Name the behavior, find the scarcity that created it, decide whether that scarcity still exists, and write something a person can tell you broke.
- **Climb the enforcement ladder from value to instruction to reminder to hard block to human-owned decision.** Five rungs, the evidence each one demands, and the reason there is no rung six.
- **Watch one commandment run as software.** A calendar check, a Slack challenge, a deadline, and a human appeal, built so the machine asks the question and a person keeps the judgment.
- **Take the worksheet, the two prompts, and the meeting tool with you.** The companion guide runs the whole method on one of your rules, by hand or with an agent pointed at your calendar, docs, and repo. The Meeting Challenger is the one I already built.

Take one rule. Any rule. The one that makes people sigh in your all-hands. By the end of this you should be able to rewrite it, decide what enforces it, and know who gets to overrule it.

## \[LINK: Executive Circle MCP Server\]

- **Access code:** executive\_circle
- **Link:** [promptkit.natebjones.com/executive/mcp](http://promptkit.natebjones.com/executive/mcp)

A read-only MCP server that gives your AI direct access to my entire published content library. Connect once, and then the archive just shows up inside your normal AI conversations. You ask your AI a question during your actual work, and it pulls from everything I’ve published to answer it.

Setup takes about ninety seconds.

- Register once at **[promptkit.natebjones.com/executive/mcp](http://promptkit.natebjones.com/executive/mcp)**
- Enter your access code (**executive\_circle**) and email, and get a personal connector URL with a unique token.
	- In Claude, you go to Settings → Connectors → Add custom connector, paste the URL, and you’re done.
		- ChatGPT works the same way through Settings → Apps & Connectors.
		- If you use Claude Code, Cursor, or any other MCP-compatible client, the URL works there too.

Your subscription now works inside your AI. Have fun!

## \[LINK: Join the Slack →\]

[The Slack community is live](https://join.slack.com/t/natescommunity/shared_invite/zt-43jji0fbo-mD~LFBAQqxCRFrxOVrPJiA)! It’s where I’ll be sharing things between articles, where you can get help on builds in real time, and where the fastest conversations in this community are already happening. I’ll see you in there!

## \[LINK: Grab the guide + meeting challenger\]

Every failed version of this I have watched started the same way. Somebody wrote the rule down, put it somewhere respectable, and assumed the writing was the enforcement. Six months later the document is still true and nothing has changed.

**[The companion guide](https://promptkit.natebjones.com/20260709_784_guide_substack_v1)** takes one of your rules through the whole method: the ritual, the scarcity, whether that scarcity survived, and the machinery underneath. Run it yourself with a pen, or hand it to an agent with real access. The agent version does not ask you what your rules are, because you would tell it what you wish they were. It reads your calendar, your handbook, your repo, your tracker, and it comes back with the rules your company is running, including every one you have stated somewhere with no check behind it. That last list is usually longer than people expect.

**[The Meeting Challenger](https://promptkit.natebjones.com/20260709_784_promptkit_substack_v1)** is Commandment Seven, already built. It never touches the calendar. It asks, it shows what is missing, and it leaves the decision with you. Point it at your own calendar this week.

## The new scarcity is judgment

Start with what got cheap.

When film cost money, a vacation produced twenty-four pictures, and somebody chose the shot. Digital photography removed that cost, and now most of us have forty thousand images, six versions of the same sunset, and no reliable way to find a child’s birthday. Taking the picture became free. Choosing, organizing, and deleting did not.

AI is doing that to work. Another draft is cheap. Another landing page, research packet, sales sequence, or internal tool is cheap enough that the default answer becomes “why not.”

The company still pays. It pays in review, maintenance, coordination, customer confusion, duplicated systems, and the obligation to remember why any of this exists.

So the shortage moved. The scarce thing now is judgment: what should be built, what should be reviewed, what should be maintained, and what should stop.

That is why my first commandment is the preamble for all the others.

> Thou shalt not slow down engineering. Thou shalt go fast.

Speed here does not mean typing faster or working people until they break. It means shortening the distance between learning something true and changing the product because of it.

Any process can survive that commandment if it names the risk it controls. Security review can. A production migration can. A legal requirement can. An approval chain whose only defense is “this is how requests enter the queue” has a harder time.

Once execution gets cheap, every ritual has to defend itself from zero.

## A written instruction is not enforcement

The most tempting version of this idea is also wrong.

You cannot drop a `constitution.md` at the top of a company folder, tell every agent to read it, and declare the culture solved. I want to spend real time here, because this is the mistake I watch smart operators make first, and it is the one that costs the most before anyone notices.

Instruction files are real, and they work. [OpenAI uses](https://openai.com/index/introducing-codex/) `AGENTS.md` [files](https://openai.com/index/introducing-codex/) to give Codex repository standards, commands, and navigation guidance, and [Claude Code uses](https://code.claude.com/docs/en/memory) `CLAUDE.md` for persistent project and organizational instructions. Both help, because they move context and standards close to the work.

They are still not hard controls.

Anthropic’s documentation makes the distinction explicit. `CLAUDE.md` is context, not guaranteed configuration. If an action must happen at a particular point, Anthropic recommends a hook or another deterministic control. OpenAI’s explanation of the Codex loop shows the same underlying reality. Instructions enter the agent’s context alongside tools, permissions, files, and the user’s request. The file shapes behavior. The surrounding system determines what the agent can do, and what evidence comes back when it does.

[BCG made an adjacent argument in June](https://www.bcg.com/publications/2026/why-ai-agents-need-an-identity-not-just-instructions): agents acting on a company’s behalf will express its culture across customer interactions, so the culture can no longer stay implicit. I agree with the direction. The practical danger is treating “make culture explicit” as one job.

Making culture explicit is four separate jobs. Each one has a different owner.

**A value says what matters.** “Put the customer first.” It may be true and still tell an agent almost nothing. A value is a tiebreaker for humans, and it belongs to whoever sets direction.

**A rule says what behavior is required or forbidden.** “Do not close a support case until the customer has confirmed the answer solved the problem.” The test of a rule is that a person can look at what happened and tell you whether it was followed. Broken or not broken. If two reasonable people can disagree about which one it was, you have written a value and mislabeled it. A rule belongs to whoever runs the function it governs.

**A runtime checks a narrow condition and takes a defined action.** A workflow that blocks ticket closure until customer confirmation exists is a runtime. It does not interpret the rule. It checks one piece of evidence and does one thing. A runtime belongs to whoever owns the system it runs inside, which means someone in engineering or ops. This is the layer companies forget to staff.

**An appeal gives a human the right to explain an exception or reverse the action.** The support lead who can override the block for harassment, fraud, or a customer who has gone dark. Write down the name of the person who can reverse it. A blank there means there is no appeal.

Four objects, four owners. Blur them and you get the standard outcome: a beautifully written values document, a Slack channel where people argue about whether the values were honored, and no system anywhere that can tell you what happened.

The more consequential the action, the more the appeal layer carries.

Take something small. A calendar challenger can run automatically because it is narrow, visible, and reversible. It asks a question. It does not make a private judgment about somebody’s motives, and it does not fire an employee, publish a customer message, move money, or delete production data.

That is the first rule of executable culture. Automate the check before you automate the consequence.

## The commandments only work as a system

The second mistake is treating the list like a buffet.

Most of the prohibitions are safe only because another commandment picks up the useful work the old process was doing. Pull the prohibition away from that support and the company does not get faster. It loses a function.

My product “repeal” is the clearest case. Commandment Three says product does not make roadmaps. Commandment Five says product does not control or direct engineering time. Satisfying lines, if you have spent enough years in software companies. Also irresponsible on their own.

Roadmaps did a job. Engineering capacity was expensive and work moved slowly, so specs, tickets, and quarterly plans kept strategy connected to the people who could build. The process went stale often, and the alternative was rarely instant customer learning. It was confusion.

So the repeal only holds because two other commandments buy the job back. Product is in the terminal daily. Product sits with engineering and jams daily. Product gives up the right to direct scarce engineering time from outside the work, and takes on the obligation to touch the material, bring the customer into the room, and decide as the product becomes real.

The artifacts collapse. The accountabilities do not. A spec, a mock, a prototype, and a working implementation can now show up in the same session, and engineering is still accountable for whether the thing works while product is still accountable for whether anyone cares enough to use it. The daily jam is where those two questions meet.

Commandment Thirteen supplies the shared test: act like all that matters is one profoundly helpful and delightful customer experience. That does part of the coordination job the roadmap used to do. A group can argue forever about a list of possible features. It can reach a harder judgment about whether the thing in front of the customer helps. That question travels. Commandment Twelve widens where it applies, because design is in the code. The payment error, the permission request, the agent escalation, and the recovery path all touch the customer, and most of them never appeared in a Figma file.

Copy “no roadmaps” without the rest and you have not adopted a system. You have deleted the thing that used to coordinate your company.

## Fewer meetings require better writing

> No meeting lasts longer than an hour. If that forces documentation, good.

Everyone remembers the cap. Commandment Eleven is what makes it survivable: documentation is code.

I learned why that matters at Amazon, and not in a way I would recommend reproducing. Fifty-seven. That is how many drafts one six-page narrative went through before anyone was allowed to put it in front of a room. That sounds insane. It mostly was. I have also never found a faster way to discover that an argument I believed was airtight had a hole in the third paragraph.

The drafting was mechanical. Every pass stripped out a word that was hiding something. A weasel word went, and underneath it was a claim I could not support. A rounded number went, and underneath it was a figure nobody had checked, which would have changed the decision if anyone had. By draft fifty-seven the document contained the claim, the evidence, the tradeoff, and the questions still open, because there was nowhere left for any of them to hide.

The culture around this could be cruel. I once sat with a colleague in tears after an L7 spent an hour taking apart their first PRFAQ. I am not defending that. I am separating the writing discipline from the way it was enforced, because the discipline is now load-bearing in a way it was not then.

At Amazon, the document did the deciding, and the audience was a room of people who could push back. Now the document is also read by something that cannot push back. An agent does not squint at a vague escalation path and ask what you meant. It acts. Give it a fuzzy source hierarchy, an ambiguous permission rule, or a definition of done that assumes context nobody wrote down, and the work ships wrong at machine speed.

So the standard is narrow. Write the parts that let work move without being re-explained.

That is what funds the meeting rules. The hour cap creates pressure to preserve the decision, the documentation rule raises the standard of what gets preserved, and the monthly challenge stops the calendar from growing back.

Shopify gave everyone a useful public example in 2023 when it [cleared recurring meetings from employee calendars and urged people to be critical about what went back on](https://www.forbes.com/sites/jenamcgregor/2023/01/03/shopify-is-canceling-all-meetings-with-more-than-two-people-from-workers-calendars-and-urging-few-to-be-added-back/). The reset was bold. The harder part is making the question recur after the announcement fades. A one-time purge makes a point. A recurring check changes the default.

So we built the question into software.

Our system scans the calendar, checks whether each standing meeting has a current justification, and posts a challenge in Slack when one is missing:

> This meeting has no justification on file this month. Per Commandment Seven: reply with a reason to keep it, or it comes off the calendar Friday.

The system does not decide the meeting is foolish, and it does not infer that the owner is wasting anyone’s time. It does the part humans are unreliable at: asking the same question again next month, showing the missing evidence, and giving the owner a chance to answer.

A recurring prompt became a scheduled check with visible evidence, and the appeal stayed human.

The Markdown file supplied the source rule. Nothing else. The calendar check, the Slack message, the deadline, and the appeal path are what made it operational, and skipping them leaves you with a value statement that has a filename.

## Speed needs a human protocol

An organization moving this fast can become unbearable even while the product improves. Five of the commandments exist to prevent that.

Be flexible to deliver value, like water over stone. Assume best intent. Do not bring a complaint without a fix or a proposed fix. Do not build alone. Imitate people who go faster than you, and teach people who go slower.

Best intent is the load-bearing one. Fast organizations communicate in compressed form: shorter messages, unfinished work shown early, direction changed without a diplomatic explanation of why the old direction was reasonable at the time. That compression only works if a short message is not read as contempt. Assuming best intent excuses nothing and removes no accountability. It buys the first interpretation a chance to be ordinary, and when that interpretation turns out to be wrong, the humans still have to deal with it.

The complaint rule does something else. AI has shortened the distance between noticing a problem and making a first repair, so you can usually show the failure, draft the change, or name the owner even when you cannot solve the whole thing. The organization still needs the negative signal. Bring it with a repair attached.

The teaching rule protects a resource that is easy to miss: pace that can spread. If speed is visible but never taught, you get one hero and a queue.

## The full constitution

Here is the current fifteen-rule version. I would not recommend copying it. Read it as a worked example of choices your organization is already making without saying so out loud.

1. **Do not slow down engineering. Go fast.** Shorten the distance between evidence and a better product.
2. **No meeting lasts longer than an hour. If that forces documentation, good.** Use the meeting for what requires people together.
3. **Product does not make roadmaps.** Plan against customer behavior and working software.
4. **Product is in the terminal daily.** Judgment about a material requires contact with the material.
5. **Product does not control or direct engineering time.** Product and engineering build together. Neither becomes the other’s ticket desk.
6. **Product sits with engineering and jams daily.** Presence replaces distant direction.
7. **Kill standing meetings monthly unless they can justify themselves.** Recurring time must keep earning its place.
8. **Be flexible to deliver value, like water over stone.** Do not make the preferred method more important than the useful result.
9. **Assume best intent.** Speed requires a humane first interpretation.
10. **Do not complain without a fix or proposed fix.** Bring the negative signal and a possible repair.
11. **Documentation is code.** Agents and people use written context to act, so ambiguity can ship.
12. **Design is in the code, terminal, SDK, and UI.** The product surface includes every interaction, rather than screens alone.
13. **Act like all that matters is one profoundly helpful and delightful customer experience.** Give the company a shared object it can judge.
14. **Do not build alone. Build with your team.** Cheap individual production does not eliminate collective taste or responsibility.
15. **Imitate people who go faster than you, and teach people who go slower.** Pace is apprenticed, not announced.

The list also exposes two tests I would apply to any AI-heavy organization. Can it review as fast as it builds? Can it delete what cheap creation leaves behind?

The first pile sits outside the reviewer’s door. If build agents produce ten times as many documents, pull requests, campaigns, analyses, and prototypes while review capacity stays flat, the organization did not get ten times more productive. It moved the bottleneck.

Every build agent needs a review path: tests, source links, diffs, screenshots, reconciliations, and a person who owns acceptance. This extends the argument in [Every Agent Needs an Owner](https://natesnewsletter.substack.com/p/ai-agent-ownership). “Done” is not a status the agent awards itself.

The second pile is quieter. Old prototypes, duplicate agents, stale instruction files, dashboards nobody opens, features nobody owns, automations still touching systems long after the original problem disappeared.

A deletion agent should not get broad authority to erase production systems. It can nominate candidates, show usage, name the owner, and ask whether the thing still earns its cost. Recurring check, no deletion authority.

## The worksheet: how to write one rule that can run

Do not begin with a workshop to draft fifteen commandments. Begin with one ritual, artifact, or approval that people perform without asking why. Pick the one everybody resents. Resentment is a signal that a rule has outlived the conditions that made it reasonable, and a repeal people wanted is the cheapest way to prove the method works.

Five questions, in order, thirty minutes. The order is what does the work, and the third one is what stops you from doing something stupid.

**1\. Name the ritual.** Write it flat, with no editorializing and no argument attached.

> “The product team creates a quarterly roadmap.”
> 
> “Leadership holds a recurring Monday status meeting.”
> 
> “Every customer-facing release requires two approvals.”

If you cannot write the behavior in one sentence without complaining about it, you do not understand it yet.

**2\. Name the scarcity it protects.** What limited thing made this rational for the person who introduced it? Time, attention, money, access, trust. The roadmap rationed engineering capacity. The status meeting moved context. The approvals caught legal, safety, brand, or operational risk.

Do not skip this. A ritual that looks obsolete is often still carrying work you have not noticed, and the person who introduced it was not an idiot.

**3\. Ask whether the scarcity is still real, and what job survives if it isn’t.** AI does not repeal everything. Regulation still exists. Production risk still exists. Customers can still be harmed. People still need private conversation, trust, mentoring, and conflict resolution. If the scarcity is intact, keep the control or redesign it, and stop here.

If it has weakened, you are not done, because the ritual was still doing a job. Ask what breaks if you remove it tomorrow. If the roadmap disappeared, how would customer priorities reach engineering? If the meeting disappeared, where would the decision and its context live? If the approvals disappeared, which real failure would stop being caught?

Write the answer down as a job, not a feeling. A prohibition with no replacement is an orphan. It creates chaos, and then the chaos gets blamed on speed.

**4\. Write the rule so a person can tell whether it was broken.** This is the test that separates a rule from a value. Most first drafts fail it.

> Weak: “Keep meetings useful.”
> 
> Stronger: “No standing meeting survives a month without a current owner, purpose, and written reason to continue.”
> 
> Weak: “Document decisions.”
> 
> Stronger: “No project decision is final until the choice, owner, evidence, and next action exist in the project record.”

Read your draft and ask whether two reasonable colleagues could disagree about whether someone violated it. If they could, you wrote a value. Rewrite.

**5\. Decide the machinery.** Five fields, and the rule is not ready until all five have an answer.

**Trigger.** What observable event starts the check. For the meeting rule, the monthly review date arrives.

**Evidence.** What artifact proves compliance. A current justification attached to the calendar record. It exists or it does not, and that binary is the whole standard. If the check requires an agent to infer motive, fairness, taste, or emotional context, it needs a person. Everything else is interpretation, and a runtime has no business interpreting.

**Action.** What happens when the evidence is missing. Start with the lightest thing that restores attention, and never jump from “the check failed” to “the machine makes the consequential decision.”

**Owner.** Who responds, and who decides. Two different names, often.

**Appeal.** Who can overrule the action. Write the name down. A blank there means there is no appeal, and a rule with no appeal will eventually meet a case its author never imagined.

Then give the rule a sunset. Name the date the organization asks whether this rule still deserves to exist, and who runs that review. A constitution that cannot repeal its own laws becomes the same process pile it was written to replace. Commandment Seven applies to Commandment Seven.

## The enforcement ladder: choose the weakest machinery that works

You have a rule, a trigger, evidence, an action, and an owner. Now decide how hard the rule is allowed to bite.

Five rungs, lightest first. Value, instruction, reminder, hard block, human-owned decision. Most organizations that get excited about agents start near the top and work down. Start at the bottom and climb only when the rung below has failed, and name the failure that made you climb. A rule that jumped two rungs because somebody was annoyed is a rule your team will learn to route around.

**Rung one: a value.** A shared reason for acting, with no required behavior attached. It costs nothing to state and it asks everyone to interpret it in context, which means variation. Use it when the group is small, the tradeoff is visible, and people already act consistently without being prompted. “We protect shared attention” is a value. So is “assume best intent,” and that one stays here permanently, because there is nothing at this rung a machine could check without turning the place into somewhere you would hate to work. **What pushes you up:** people agree with the value and still make incompatible choices, or a new hire cannot infer the behavior from it.

**Rung two: an instruction.** A written behavior, expected under stated conditions. It converts the value into something a person can follow, and it costs somebody the work of writing, teaching, and interpreting it, because edge cases arrive the moment it meets real work. “Kill standing meetings monthly unless they justify themselves” is an instruction. Use it when people will comply once the expectation is clear, and when a missed step is visible and recoverable. **What pushes you up:** people support it and forget it anyway, which happens most when the action is infrequent and has no natural cue.

**Rung three: a reminder.** The system notices and tells someone. Nothing is blocked. The evidence is thin by design, usually the presence or absence of an artifact, and the action is a message to a named human who keeps the decision. Documentation prompts, renewal checks, stale-owner notices, the calendar challenger. Use it when the failure is memory rather than disagreement, and most people act after one useful prompt. Most rules should stop right here. A reminder does most of the work of a gate and earns a fraction of the resentment. **What pushes you up:** the reminder gets ignored repeatedly, or compliance cannot be verified, or proceeding without the requirement costs real money.

**Rung four: a hard block.** The system prevents the next step until a specific, observable requirement is satisfied. A release waits for a passing test. A payment waits for the right authorization. Two conditions before you build one: the blocked action has to be reversible or deferrable, and the evidence has to be something the system can verify without interpretation. Blocks interrupt work and create support burden, and a badly designed one turns a legitimate exception into an emergency. Build a gate that blocks on a judgment call and your team will learn to route around it. They always do. **What pushes you up:** the blocked case turns on disputed evidence or a valid exception the system cannot judge.

**Rung five: a human-owned decision.** A named person reviews the evidence, hears the appeal, and owns the outcome. Automation can trigger the review, show what is missing, and record the result. It does not make the judgment. Human decisions are slow and sometimes inconsistent, and the owner needs real authority, a response expectation, and a record of what was decided before. Use it when the stakes or the ambiguity justify judgment and the caseload is survivable.

There is no rung six. That is the part worth sitting with. The ladder does not terminate in automation, it terminates in a person, and if you find yourself reaching past the top for something that decides on its own, you have not found a higher rung. You have found a rule that needs repair: clarify the evidence, narrow the cases that require judgment, delegate the ownership, or push the routine cases back down.

Which gives the whole thing its shape. Some rules live at rung five permanently, and no quality of evidence ever moves them down. If the action ends someone’s employment, moves money, publishes to a customer, deletes production data, or makes a private judgment about a person’s character, an agent does not hold the trigger. It can gather the evidence, show the pattern, name the owner, and ask. A person decides.

In regulated or safety-critical work, the existence of an agent does not reduce human accountability. It makes the chain of responsibility more important, which is why [infrastructure becomes the control layer](https://natesnewsletter.substack.com/p/agent-infrastructure-control-layer). Identity, permissions, logs, limits, review, and shutdown are what decide whether your rule is a suggestion or a dependable part of the system. Everything above that layer is commentary.

## Where this goes wrong

Vague virtue is the easiest failure. “Be innovative,” “move fast,” and “put the customer first” may express real values, and they will not tell an agent or a new employee what to do when speed conflicts with safety, or when one customer’s request conflicts with the product’s long-term health. Translate the value into a decision somebody faces.

The orphan prohibition is the more dangerous one. The company bans roadmaps, meetings, tickets, approvals, or documentation without replacing the coordination, context, risk control, or customer signal those things carried. The old process comes back, because the job never left.

Treating context as enforcement is the failure this whole piece is built around. A sentence in `AGENTS.md` or `CLAUDE.md` can guide behavior. It cannot guarantee an action. A hard requirement needs a real control, and the control needs tests of its own.

A rule with no appeal will eventually meet a case its author never imagined. If nobody can see, challenge, or reverse the action, the system becomes efficient at being wrong.

Then there is constitution bloat. Anthropic recommends keeping `CLAUDE.md` specific, concise, and well structured, because long instruction files reduce adherence. [OpenAI has described the same lesson from agent-first engineering](https://openai.com/index/harness-engineering/): give the agent a map, not a thousand-page manual. Your constitution should hold durable choices. Detailed procedures belong in the workflow, skill, runbook, or policy that applies when needed.

The last failure is trying to automate the part that makes the company human. You can lint whether a document has an owner. You can check whether a test ran. You can challenge a meeting. You cannot lint whether two people trust one another, and you cannot automate the judgment required to tell somebody, “I believe you meant well, but this hurt, and we have to repair it.”

The calendar bot can raise the question every month. Only the people involved can repair the trust when the rule gets broken.

## Start with the rule everybody resents

So go find it. You already know which one it is, because it is the rule that produces the sigh in your all-hands, the one your best people stopped following without telling you, the one nobody can trace to a person who chose it.

Run the five questions on it this week. Half an hour, alone, before you involve anyone else. Ask what scarcity created it, whether that scarcity survived contact with the last two years, and what job would go unclaimed if the rule vanished tomorrow.

If the rule survives that, write it down properly. Give it a trigger, evidence, an owner, and somebody who can overrule it.

If it does not survive, replace the work it was doing, and then repeal it.

And if the check that remains is narrow, visible, reversible, and boring enough, let the software remember to ask.

## Coming up

Tomorrow on [YouTube](https://www.youtube.com/@natebjones) I am talking about why I reach for ChatGPT 5.6 Sol every day even though Fable 5 handles ambiguity better, and why that is not a contradiction. Benchmarks tell you which model is smarter. They do not tell you which one matches how you actually work, which in my case is long, verbal, and stubborn about finishing things. I am also launching a model picker that takes a ramble and hands back a mix.

## Related reading

- [Your team is running agents nobody owns](https://natesnewsletter.substack.com/p/ai-agent-ownership) — the ownership card and the two prompts behind it. This is rung five with a name attached, and the piece that argues “done” is not a status an agent awards itself.
- [Grab the one-minute test that tells you if your task needs a chat, one agent, a team, or nothing at all](https://natesnewsletter.substack.com/p/agent-shaped-work) — the question that comes before the worksheet. Some rituals should not become systems at all, and this is how you tell.
- [Seven questions decide whether your AI agent ships](https://natesnewsletter.substack.com/p/agent-infrastructure-control-layer) — identity, permissions, logs, limits, review, shutdown. The runtime rung, in production, with the vendors who gate it.
- [Six things have to be true before AI changes a workflow](https://natesnewsletter.substack.com/p/enterprise-ai-deployment-layer) — most companies have built two. The orphan-prohibition problem at enterprise scale.

![](https://substackcdn.com/image/fetch/$s_!1fjW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4114ea8-8b1a-433d-980d-4ee8f0c932a2_1390x768.png)

---
*Clipped from [substack.com](https://natesnewsletter.substack.com/p/ai-native-company-rules?r=1z4sm5&utm_campaign=post&utm_medium=web) on 2026-07-14T14:42:07-04:00*
