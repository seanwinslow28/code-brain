**Layer 2 — Recurring Decisions (fresh)**

**Q1.** What decisions do you make **3+ times a week** in this domain? I'm thinking: did I work out today / log the habit? Is this transaction worth keeping or is it a subscription to kill? What goes on today's task list vs. gets deferred? Which supplements/meds today? What should I cook vs. order? — tell me which of those are real, which are automatic, and what I'm missing.

1) These are correct: Did I work out today / log the habit? Is this transaction worth keeping or is it a subscription to kill? What goes on today's task list vs. gets deferred? – The main things I want to track with this domain are my personal finances. The daily habits are important and they keep me motivated to get them done and remind me to take breaks or focus on a specific task, but this domain will be a big financial advisor and researcher. Between savings and doing research on finding additional ways to make money. Whether that’s through stocks, crypto, side freelance projects, etc. It should also include “things that I learned this week” so I can log all of the new tools, workflows, news that I might want to reference in the future. It would be nice to just drop things into my obsidian vault whenever I come by them on the web or that someone sent me and be able to look at it later and have my agents reference it in future conversations. An example would be this note that I added to Obsidian when I had a quick idea on how to make money with agents: /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/40\_knowledge/concepts/[idea-autoresearch-agentic-polymarket-crypto.md](http://idea-autoresearch-agentic-polymarket-crypto.md) – I haven’t been able to dive into this, but it could potentially be something that a research agent with a Perplexity API key did extensive research on already and I could just wake up to a report on the idea and a plan of execution.

**Life-systems \= primarily personal financial advisor \+ researcher. Secondary \= daily habit motivation/focus reminders. Tertiary \= weekly "things I learned" log \+ quick-capture inbox → agent-referenceable context.**  
That's a meaningful reframe. Original framing treated finance/health/learning/tasks as peers. You're saying finance is the backbone and the rest supports it. I'll carry that through the rest of Layer 2\.  
**Adjusted focus for Q2–Q7** (to reflect finance-first framing — no need to re-answer Q1):

**Q2. Prioritization criteria.** When life-systems items compete, what wins? Specifically:

* Financial deadline (payment due, statement close) vs. habit streak vs. research dive — what's the real ranking? \- **ANSWER:** **Research dive would win this**  
* Does "money leak" (active subscription bleeding, suboptimal credit routing) always jump the queue? \- **ANSWER: Only if there’s some sort of emergency, but this should never be the case, so I’m not worried about this.**  
* When a money-making research thread (polymarket idea, stock, freelance) surfaces — is that a "capture and defer" or "drop what I'm doing"? \- **ANSWER: It’s a capture and defer \- I want it to be logged and acknowledged. It will be something that I want to dig into myself, but I may be busy with other tasks, so it would be ideal to have a research agent or multiple research agents to do deep dives into. They should research how it could be done, provide ideas of implementation, and the best path to financial success with those ideas through specific paths of execution. It should be brought up in future /daily-driver Obsidian notes saying that an agent started doing the research or finished research and constructed a plan of execution. I would provide a Perplexity API key, we could have another agent with access to the Gemini Deep Research MCP, and we can see which open sourced models are great at deep research and planning. All of those agents can work together and help me figure out a way to potentially make money through investments/side projects/polymarket bets/crypto/stocks etc. I want to really dig into how we can get this done correctly through the intent engineering skill: /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/intent-engineering and the last30days skill: /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/last30days – Other skills can and should be created to make this a rock solid agentic financial pipeline. We could also utilize the Agent Kit repo so I can give my agents some wallets: [https://github.com/coinbase/agentkit.git](https://github.com/coinbase/agentkit.git)** 

**Q3. Auto-yes / Auto-no** in life-systems (finance lens front, habits secondary):

* Auto-yes examples to react to: Bilt reward redemption, cancel a flagged subscription, log the workout, take vitamins, capture a research seed to Obsidian, small cash-back/APR optimization  
* Auto-no examples: new recurring subscription without cooldown, any financial commitment the same day it's pitched, late-night commitment that breaks 21:00 bed, anything that violates sacred first hour, investing in something without a research pass first  
* **ANSWER: All of those are accurate. I would also include in the Auto-yes column that I would always hear an agent out on it’s idea or plan on something it did extensive research on. Another auto-no would be to have Claude scold me or point out that tasks or habits might not have been completed the day before. I need breaks sometimes, so when I don’t go to the gym or execute tasks, I don’t want Claude to point out that I missed it and tell me I should be getting it done. It should acknowledge that I skipped some things and just put it back on the list for me to try again.**

**Q4. Daily investment heuristic** — finance-first framing:

* On a given weekday, when does "do a finance check" happen vs. "dive into a research thread" vs. "just log habits and move on"?  
* Is there a weekday/mood/energy rule? (e.g., "Mondays I review the week's money flow", "low-energy days \= logging only, no research")

**Q4 ANSWER: I would like the 15th of every month to be a finance check. I say the 15th because all of my statements will be available by then and I would have just gotten paid as well. Unless we find a way to have Claude view my chase and bilt accounts in real time (similar to rocket money), then we wouldn’t see any changes with my finances unless I manually log the changes every day, which would defeat the purpose of agents. The habit log should be shown in the daily-driver agent or daily-driver SKILL each morning. The dive into research threads should occur whenever a new raw note containing a potential idea is put into the vault. – The research will occur whenever I stumble upon something I find that could potentially make me money, so I want to do a deep dive, or if I ask Claude to use the last30days skill to see if anything has popped up recently that could be of use and something we should do a deep dive into.** 

**Q5. Agent delegation — this is the big one for the finance-advisor framing.** What do you **already trust** an agent with, and what will you **never delegate**?

* Already: transaction categorization (local models), habit log assist, subscription scanning, research summarization, quick-capture filing?  
* Never: final spend decisions, actually executing a trade or payment, committing to a freelance engagement, medical?  
* What about the **middle ground** — "agent drafts a research report and a recommended action, but I decide"? Where is that line?

**Q5 ANSWER:** **To start, I will keep it as the “Already” (transaction categorization (local models), habit log assist, subscription scanning, research summarization, quick-capture filing) and “middle ground” (agent drafts a research report and a recommended action, but I decide) tasks you mentioned. As time goes on, I would like to give the agents their own wallets (through agentkit) to make these financial decisions based on all of the research on the markets or specific topics and all of the knowledge/data we build within the vault. The agents should constantly learn and grow as time goes on.**

**Q6. Tiebreaker** when unsure (finance-weighted):

* Default to cheaper/save? Sleep on it? Ask girlfriend? Default "no, not now"? Default "capture to Obsidian and revisit"?

**Q6 ANSWER: We should default to finding cheaper alternatives depending on what the situation is. When it comes to me searching for something new in my apartment or a new clothing item or anything like that, we should first check to see if there is a cheaper option that would get the job done and has great reviews. If we’re REALLY unsure and want t dig deeper before pulling the trigger on anything, we should capture to obsidian and revisit.** 

**Q7. Definition of "done"** — expanded to match the reframe:

* Workout "done" \= logged where?  
* Habit streak "done" \= tracked in what?  
* **Finance review "done"** \= txns categorized / budget reconciled / written note in vault / debt paydown target updated — which of these?  
* **Research dive "done"** \= a vault note captured / a report output / a decision recorded / an action taken?  
* **Weekly learned-log "done"** \= what form — a running note, tagged captures, something else?

**Q7 ANSWER: All of this should be tracked within the vault in their respective locations. I’m in the process of building a UI for my life-systems-hub that you can view here: /Users/seanwinslow/Code-Brain/life-systems-hub/[CLAUDE.md](http://CLAUDE.md) – The goal is to link my vault to this hub down the line so I have a nice UI to log all of this information.** 