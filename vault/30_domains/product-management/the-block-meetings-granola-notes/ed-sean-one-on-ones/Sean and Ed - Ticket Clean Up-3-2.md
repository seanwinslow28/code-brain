# **Ticket cleanup**

Mon, 02 Mar 26 · erupkus@theblock.co

### **Personal Updates & Moves**

* Sean moving to Boston (Charlestown) March 21st with girlfriend  
  * Long distance relationship, now working from home enables move  
  * Girlfriend from Staten Island, moved to Boston with sister  
* Erupkus moved from NY State to Portland, Oregon in 2024  
  * Lived in NY 2015-2024 (school, work, then NYC)  
  * No plans to return to East Coast  
* Team trend: everyone currently moving (David, Corey also relocating)

### **Campus Landing Hub Implementation Questions**

* Claudine’s comment on implementation ticket needs clarification  
  * Unclear if requesting ticket requirements or actual development work  
  * Sean will ask for clarification on landing hub page requirements  
* Sponsored course flow design unresolved  
  * True it would be course catalog, but what does sponsored course look like \- do you press play and that’s it, do you go through chapters etc  
  * Key question: after clicking course card, is it popup or dedicated page?  
  * Need upsell opportunities before/after course completion  
  * Rise 360 example provided by David shows interactive LMS interface  
* CMI5 exports from LMS systems, not standalone interfaces

### **Ticket Cleanup Progress**

* Reviewed tickets from $17.54 onwards  
* Closed outdated items:  
  * Newsletter improvements (2024) \- low priority, functional but could be prettier  
  * NFT page design \- no longer relevant, NFT market declined  
  * Various spacing/design tweaks already implemented  
* Kept relevant backlog items:  
  * Entity project (company pages connecting all crypto data)  
  * RSS feed story removal capability for editorial mistakes  
  * Overview page with watchlist functionality  
  * QA workflow visualization  
* Draft tickets indicate unfinished bug reports needing investigation

### **Next Steps**

* Schedule call tomorrow 10:30 AM with David and campus devs  
  * Align on sponsored course expectations and capabilities  
  * 30-minute session post-standup  
* Sean continuing Zapier automation work  
  * First zap completed (18 steps), second zap in progress  
  * Multiple paths for ad placement in Jira  
  * Demo ready for next ops meeting  
* Continue ticket cleanup from stopping point (around ticket 2119\)  
* Sean researched X402 issue, will share findings relevant to auth/Stripe integration

---

Chat with meeting transcript: [https://notes.granola.ai/t/ec3a3162-6752-4256-8991-2c2889143c17-00best9l](https://notes.granola.ai/t/ec3a3162-6752-4256-8991-2c2889143c17-00best9l)

FULL TRANSCRIPT

Meeting Title: Ticket cleanup  
Date: Mar 2  
Meeting participants: Erupkus

Transcript:  
   
Them: Hey. Hey.    
Me: Yo. How's it going, dude?    
Them: Monday.    
Me: Monday,    
Them: How are you?    
Me: I'm good. Yeah. I feel I feel good. Like the past few weekends, have just been know, going out. This weekend, I stayed in, so I feel normal.    
Them: Very nice. Very nice.    
Me: Yeah.    
Them: Is guys no longer covered by snow?    
Me: So today is actually kinda cold, so the snow's sorta sticking But for the most part, it's been getting like, this past Saturday, it was nice out. So it's slowly melting away, and I'm very excited about it.    
Them: Wait. It's so bizarre to, like, like, I I don't I lived in New York state for so many years and February and March was always, like, full of snow. But here, like, I it was fixed it was six degree weather. I was I was sweating with my, like, Patagonia fleece. I'm like, oh my god. I think about it that there's actually, like, places in the country where there's    
Me: Yeah.    
Them: people showing snow today. Just so hard to think about that. Like, I I'd still don't get used to it.    
Me: When did you live in New York State?    
Them: I've lived well, I went to school there. Upstate New York, and then I worked for a couple of years after I graduated. Actually moved in 2024\. Yeah. To West Coast. We were I would jump I was from 2015, basically, up until 2024\. I was, somewhere in New York State. Upstate New York, then New York City, and then New York State again.    
Me: Okay. And you moved with with your now wife?    
Them: My wife. Yeah. Yeah. We moved to Oregon, and now we're in Portland.    
Me: Nice.    
Them: Yeah. Not planning on calling back. To be honest.    
Me: I I do not blame you. I'm actually I mean, I'm staying on the on the East Coast, but I'm moving to Boston in on March 21\.    
Them: Oh, shoot.    
Me: With my girl. Yeah.    
Them: You're like a like a long term move?    
Me: Yeah. Yeah. Because well, I mean, I'm sure we'll be bouncing around, but my I was doing long distance with my girlfriend. And be because I was working in Manhattan, I couldn't really like, we had to stick with that. But now I'm working from home, she has, like, a nice    
Them: Mhmm.    
Me: a nice sized apartment. So I was like, yeah. We'll just move in together.    
Them: That's right. There we go. Like, big moves.    
Me: Yeah.    
Them: Where in Boston does she live?    
Me: Charlestown? You're familiar? It's, like, right above, like, boss main Boston City. Yeah.    
Them: That's what I live on my skirt. Oh, gotcha. Gotcha.    
Me: It's like it's similar to, like, a suburb type area. It has, like, a bunch of townhouses.    
Them: Gotcha. Yeah. My sister-in-law lived in Boston. She just moved out of Boston. She was Beacon Hill.    
Me: Okay.    
Them: She was, like, right down like, right in the heart of it. So I, like, visited a couple times. But none I don't know nothing that well.    
Me: Yeah. But I've I've yeah. I've been to Beacon Hill as well. So    
Them: Nice. Yeah. It's pretty it's pretty cool there. Very Boston vibes.    
Me: Oh, yeah.    
Them: Doesn't just don't pick up the accent, man.    
Me: Oh, I I it'll be hard not to just because I'll be making all the time.    
Them: Is she from often originally?    
Me: You    
Them: Okay. Okay.    
Me: no. So she's from Staten Island where I'm from. But she moved up there And then we just, like, started talking again like, last year. Through, like, Instagram, and then we just turned into, like, a a long distance thing. And her sister lives up there, so she moved up there because of that. Yeah.    
Them: Gotcha. Cool. Well, good luck with your move.    
Me: Thank you.    
Them: Those are never fun.    
Me: I was gonna say, yeah, talking to you and then talking to David. And Corey, like, everyone's in the middle of a move. I was like, this is a trend.    
Them: Yeah. It's people are always on the move these days. All now, especially with, like, in the remote working, you can get more freedom. You know?    
Me: Yeah.    
Them: It's not no longer, like, job related, like, you get a new job, you will But now it's deciding where you wanna live.    
Me: Exactly. It's it's a beautiful thing. My parents when I told my parents that I have work from home job, they were just like, how does that how does that work? Like, what does that even mean?    
Them: Getting ready. Yeah. Must be so weird to for them. Okay. So tickets. I missed    
Me: Yeah. Did you see, Claudine's comment on on the implementation ticket for, like, that Rommel was working on before he started working on the one today. She was asking about the three cards. Hold on. Let me find it. Okay.    
Them: Send it to me. I didn't get the comment. Oh, the comment for for yeah. Well, the thing underneath the    
Me: Okay. Yeah.    
Them: cards? Yeah. I    
Me: I did. Okay.    
Them: yeah. Yeah. So I replied that. Yeah. We definitely don't want people to incentivize to just create a free free profile and then, like, inspect the courses and then not like, proceed not to not to pay. You know? So it's like that's always the tactic that I've seen is, like,    
Me: So    
Them: if there is a free profile for something, I that's when you can bypass the bypass the the payment. It's like as small as possible.    
Me: Yeah. I was talking about I I I know what you're talking about. She DM'd us. She also messaged on an actual ticket on I just have to find oh, it's, like, lost in the shuffle. Hold on. Why don't you get rid of it? Oh, no. Here we go. So because it's kinda tying into the landing hub for campus. Or for the my campus page. So I wasn't sure if this was an Us thing. Like, we have to write it on the ticket or she was asking for implementation to    
Them: Oh, this is    
Me: actually create it.    
Them: Oh, this is a different thing. Than what I was than what I was talking about.    
Me: No. I I do know about it. It was what she sent us in    
Them: Yeah.    
Me: the group.    
Them: Yeah. Yeah. Okay. Three charge. What is she asking for? I don't get it.    
Me: That's that's why I was a little confused. I thought she was like, I wasn't sure if this was asking to put that information on a ticket. Like, the landing hub page, information, like what it actually looks like, like describe the requirements, or if she's asking like, the the developers to actually start working on this. So I I'll I'll ask her.    
Them: And just say, you asking them to, like, edit the edit the the implementation right now, like, the prod, like, what's on campus, or what are you asking?    
Me: Yeah.    
Them: Because it seem it seems like it's sort of due to a or something like that. Yeah. Because right now, I don't think we have, like, we don't we don't we don't we don't have a more like, it's just a few cards. It's not like    
Me: Yeah.    
Them: like, in her in her design, it's, like, multiple cards can fit in and now it's just like one card. Yeah. Let me know what she says.    
Me: Okay. And yeah. Well, so since we're on the subject, the landing hub after the after going through the sponsored courses,    
Them: Mhmm.    
Me: I I saw your, response. It was, like, it would be course catalog, but what does a sponsored course look like? Do you press play, and that's it? Do you go through the chapters, etcetera, etcetera? So you're talking about, like, after they go Okay. So it's like they I think yeah, We didn't we didn't we didn't go that far. We just pretty much stopped at the like, at the My My Campus landing hub.    
Them: Yeah.    
Me: So you're saying when you click on the actual card itself,    
Them: Well, let's say    
Me: does it look like?    
Them: Well, I feel like yeah. Like, if if you're on that view where it's, like, the all of the the multi multi course page, basically, the line page where all different courses are, the learning paths, one zero one, two zero one, and the electives and sponsored courses. If you interact with one of them, what what happens? Are we going is it, like, a pop up where it's just like inside of that Like, it's it's just a pop up on the multi course    
Me: Mhmm.    
Them: landing page, or do you get taken to a specific course? That    
Me: Yeah. I get    
Them: you know, Like, I I think part part of that answer is like, could be answered with David's input meaning, like, what what are we actually gonna build? Like, because, technically, we want it to be well, ideally, it would be at least in my view, in a state where it's, like, either after or before you finish it. You're exposed to the, like, upsells to the to the locked courses. And if you, like, get taken to a specific landing page for just for that course, there's nothing there's no upsell opportunities at all. You're just, like, you're just on some some some other web page and you're just, you know, finish playing a video or go through the course and that's it. But, like, figuring out, like, what it what does it look like? What are we    
Me: Mhmm.    
Them: planning to do? I don't know if probably should schedule a call with David and researchers and just, like, get all aligned on, like, what what they're actually creating.    
Me: Okay.    
Them: Than what we envision that course being, you know,    
Me: Yeah.    
Them: like, because that's something that they will need to you know, design as well. I mean, even and also if if you even have the freedom to do so.    
Me: Yeah. Yeah. I'm gonna send you something that David sent me. It's like, it's the Rise three sixty    
Them: Mhmm. Yeah.    
Me: like, hub, whatever.    
Them: Mhmm.    
Me: He said example. So I think this is probably what it would be. But, yeah, we should definitely talk to David just to double check because I think I I would assume that it would just send you right to like, if you're trying to take the course, then it would just send you right to the actual course page. InRISE. Because it has, that he made one early in that campus style. But you also have the preview So I guess that would be the modal.    
Them: Yeah. So I don't think there's a reason I don't think there's a reason why that star course thing couldn't be like, the star course CTA    
Me: Mhmm.    
Them: Sorry. Once you click on start course, you you enter this, like,    
Me: Yeah.    
Them: you know, this, like, interactive thing. There's no reason this thing be a pop up. And like, after you press, like, okay. Start course on on Polymarket, you know, sponsored course,    
Me: Mhmm.    
Them: So I think that this is it's probably doable. Unless this is specific. I I just don't know, like, the the back end of this. Like, I don't know what Rise is and, like, how it functions. Is this a specific location, or is this just, a prototype    
Me: No. It's a spit so the rise    
Them: This is    
Me: Rise three sixty, it seems to be like, similar to what the hippocampus. It's like the LMS. It's, like, all through the LMS system. So, however, they connected that it should also be the same deal. Because I was looking into it when I brought it up to the Nikitas. They were like, oh, I hope it doesn't like, I hope it's not different from what we're already doing. But like, c m I five stuff. But the c m I five is just an export from something like an LMS or Rise three sixty. It's not an actual, like, interface or anything like that. Which I was confused about. I just learned last week.    
Them: Okay. It seems like we definitely need to, get a get on a call    
Me: Yeah.    
Them: with David and the campus devs. So that we can just, like, align on what we can expect for these electives and these short courses. And then we need to double check with the researchers that this like, if it'll create enough content for stuff like this. Just looking like this is this is just basically, like, the okay. Layer one to layer two. Okay. Yeah. Let's let me check the schedule. Yeah. Let's schedule a call tomorrow after stand up.    
Me: Cool.    
Them: So let's just do ten point five. And let's is David still on at that point? Or is he off by that point?    
Me: The daily yeah. It's usually    
Them: No, David.    
Me: The daily? Yeah. It's usually done by then. Oh, he should be yeah, he should be on.    
Them: Alright. Cool. Yeah. It can be, like, thirty minutes. I'm probably not not gonna take it that long, but just wanted to    
Me: No.    
Them: start about this so we fully are on the same page.    
Me: Yeah.    
Them: Cool. Okay. Any other questions in terms of that?    
Me: No. That was that was the thing that I was thinking about ever since we had that meeting.    
Them: Yeah. And then    
Me: And, obviously, we're gonna have to cover the other aspect of it.    
Them: yeah. What    
Me: In the next meeting. So    
Them: yeah. I want to write the design tickets for the clothing and then also those implementation stuff. But, I mean, we still have a little bit of like, a little bit of time for for the implementation because there's they still haven't    
Me: Mhmm.    
Them: finished the the outflows. Is that all figured out? Like, the all those tickets, is that all clear now?    
Me: With Roma,    
Them: Yeah.    
Me: Yeah. It it seems like it. Yeah. He he hasn't asked me any more questions.    
Them: Okay. Well, yeah, let's make sure we're checking with people on the payment flows tomorrow. Stand up.    
Me: Okay.    
Them: Cool. Okay. Let's jump into the Well, we we were at $17.54, I think. Check. Yeah. Did we look at this one already or no?    
Me: No. I don't remember that one.    
Them: That's chess. Newsletters improvement on that goal. So old.    
Me: What is that from? Oh, twenty twenty four. Do you think they improved?    
Them: Yeah. Give me the whole thing. Oh,    
Me: Does any    
Them: Are they changed the way it looks, but I don't know if    
Me: Well, that podcast has not even been on the homepage anymore. Right?    
Them: It is, but it's, like, it's a it's a yeah. The nav bar looks different, but it's here now. So you could still you could You can still oh, not podcast. Newsletters. You could still do it and, like, they're talking about these specific, like, instances where you're subscribed to one email with not or one newsletter with the other one, and it's like, how do we handle it with the messaging and marketing contractor. Black logo. I don't think we've ever got through this. Let's not close it. It's probably something we should do when cleaned up.    
Me: So when it comes to something like that, if it comes to an old ticket that hasn't been really completed, how do you, revise it? How do you revisit it? Just by commenting on it?    
Them: Well, this whole concept of cleanup is, like, to get rid of the tickets that are no longer no longer, like, needed or they just, like, cluttering the the board?    
Me: Yeah.    
Them: This one is, like, still relevant, but, like, it's super low priority because it's like, newsletters work. You know? It's just like a the pretty up the experience and make it more smooth. So you just it just stays in the in the backlog, basically, until somebody like, for example, is like, hey. I need more work.    
Me: No.    
Them: I need more work. Just so that    
Me: Okay.    
Them: you look through the list of stuff that's still outstanding and    
Me: Gotcha. Alright.    
Them: maybe if you could pick it up, you know? Folks in adding Folks can add in features issues.    
Me: Yeah. It's good to know because when you were gone, Marina like, asked me a couple times. She was like, yeah. I'm finishing up this thing. Do you have anything else? So I was like,    
Them: Yeah. Yeah. Yeah. I Yeah. Ideally, our team is, like, has a full stack of tickets that can be just picked up and was was great descriptions, but a lot of them don't have great requirements.    
Me: Yeah. It seems like it's    
Them: Unfortunately.    
Me: just a reminder type of deal. It's just like, oh, something that I saw. While you're doing this, if some of them don't have good requirements, if you just, tag my name in there, I can improve them. Whenever I have free time.    
Them: I just don't know, like, if we need to. Like, I just yeah. Potentially, just would rather not waste your time on stuff like this. It's like only when we need to find something to do when there's, like, you know, in a period of like, other than those moments when somebody's, like, raising their hand that they need a ticket, it's like, then you can just go in and just, like, quickly make sure that you know, it's clear enough and then just assign it to them. Rather than just going through this whole list and, like, meeting requirements, and then that stuff never even gets you know, picked up. So it's, like, kind of a waste of your efforts. K. This is looks this looks like automation. Yeah. And this is we're almost done. That's we're gonna touch that. That's the ticket for his automated tests, basically, that he runs. Don't we have to oh, so I'm talking about reported it. I was like, do we still have a ticket attached to him? Or assigned to him?    
Me: Oh, can you go back    
Them: Launchpad.    
Me: Yeah. Can you go back to Jira?    
Them: Oh, shoot.    
Me: On the presentation? Yeah.    
Them: Sorry.    
Me: It's okay.    
Them: I feel it. Do finish this. They'd do it. I saw a lot of this stuff. Dev instances, and they were changing Only axis for near. Yeah. I wouldn't know if this was analyzed. What is this? Oh, NFT page. For design. And this was basically related to let me share my screen real quick. When this when this whole thing was being designed, like, we initially just had tokens. It was just, like, one table. Then we added ETFs and stocks. And we also wanted to add NFTs because at that point, NFTs were irrelevant.    
Me: Yeah.    
Them: And it was sort of did, a gradual look at Yep. ETS first and stocks. And by the time we were, like, we're gonna get to NFTs, they sort of like, lost relevance and    
Me: Yeah. It's    
Them: went downhill. So this never even got picked up. So I can I can close this whole    
Me: It's unfortunate NFTs were    
Them: Very much?    
Me: the thing that got me interested in crypto in the first place that I started, like, I was like, oh, I draw. I can make money off of that.    
Them: Yeah.    
Me: And then literally, like, a month two later, it was just gone. I was like, oh,    
Them: Same Seemed too good to be true. It was. It's, like, a super small We can definitely check this one. Reduce Reduce the space between yeah. Emily was very, very she was our design member before you, and she was very busy like that. The specific things. She's talking about this gap. And I think this is already this is already taken care of. Yeah. It looks a lot different back then.    
Me: by by 1.92 pixels is that what you was asking? Oh oh, no. That was the percentage. Okay.    
Them: Yeah. Yeah. Yeah. No. I was probably, like, 50 pixels. That's definitely More. Yeah. This is the stuff they wanna just, like, get rid of. You know? It's like    
Me: Yeah.    
Them: no. Related entity. Oh, jeez.    
Me: What was that?    
Them: Our entity project. Really wish I had the time for it. Yeah. But this probably is a better Wow. What an epic I think I wrote a PRD for this, though. Wonder if this was one of my first purities that I wrote. Essentially, we wanted I I kinda still want it actually. The create company pages. And it's basically, like, mapping everything, the we have data on in crypto. So, like, if you think about company pages, all the companies that operate in crypto, all the funds, all the blockchains, all the, like, basically, founders and, you know, all of that basically being interconnected and it all stemmed from the funding database because when we were collecting all of funding, deals, had to collect, like, who the founder is, who the investors were, who's like, what is the company, their website, their socials, all that stuff. Like, we had a lot of data collected over the years. And we're like, this stuff needs to live on that goal, like, because you know, anybody's Should have is you should have a Coinbase dedicated company page and then you have company or Coinbase News, have Coinbase. Coinbase is price the stock price that we have from the, you know, from the stocks page. Then you'd have, like, maybe their investment deals that the ARM has, like, all that stuff. Basically. And it all and then it would all sort of like, our whole page structure would be centered around companies. Because, like, right now, it's just, like, we have a tag you know, if there if there if there's a tag for Coinbase. And that's it. Like, you just gonna read news about it. But, like, there's nothing if you there's nothing connecting prices to you know, the the company stock. Point based. To actual news about it. Yeah. If you if you find yourself here somehow, you probably could read some news or find some data that's related to Coinbase.    
Me: No.    
Them: Yeah. There you go. Yeah. But, like, like, this type this basically should be a Coinbase page. Like, it should be just a a full company page, not just the prices page, and it would have, like, all this sort of you know, information. So this that's what the this whole entity I was    
Me: That epic.    
Them: four, but I mean, it's not even now we're gonna have the tickets written for that. So I doubt it was ever it's ever gonna be picked up, but I'll just leave it just so that we don't forget about it. That it's it was some an idea at some point. James, yeah, add price change for one hour and payload. And we We don't really work on the indices anymore. One, What is our impressions? I feel like that's been done. Maybe not. Where is oh, we're here.    
Me: What was the request? Was the request to add an hour?    
Them: One hour price change, value or percentage. In the API. So I feel like they did it because there's a one hour thing here.    
Me: Yeah.    
Them: Yeah. I see the price change. So fresh Yeah. Price change is different. But I feel like if it would if it didn't have the price, we wouldn't be able to calculate the the price change. Whereas one by seven day, one month here today. And I have one hour in here? But that's fine. I'll just close it. We have like, everything works. It's just this ticket is no longer needed, and nobody cares about a JMCI anymore. Let's do well, what else is outstanding here, actually. Yeah. You mind doing this? This was a year ago. Trying to find the specific instance to select thread.    
Me: Did it actually go    
Them: Well, he he left a link there. Let's    
Me: through Slack? Yeah.    
Them: slide. He said one year Seems that change seems that changes displays wrong number. Yeah. I don't no one ever visited these pages and no partnership is over. So We're not gonna waste time on this.    
Me: Draft was a company.    
Them: No. Yeah. I think this is like, an unfinished bug ticket. That's how Roma writes some of those bugs So, like, if it has draft, that means it's, like, missing either requirements or still needs investigation or something like that. Adjust RSS to remove stories from the feed by removing tags. Oh, I remember this recently. Yeah. Yeah. This is basically, like it's quite a tricky situation. Our RSS feed like, we release a story, right, we we distribute a lot of our stories through RSS feeds. So, like, let's say, trading view, the app with charts, they have news as well. So they would list our news article and our headline on their, like, interface through the RSS feed. But then if, like, our editorial makes a mistake on that article, like, they reported something they shouldn't have reported or, like, they make a, like, a brutal mistake. If they edit it, on our side, that RSS feed article that's listed already is not gonna get edited. So it's like, how to, like, basically handle those you know, mistakes, and we want the output changed. So it's, like, only really applicable when there's, like, a major mistake made and and needs    
Me: Yeah.    
Them: some sort of intervention. So it's like that's it's definitely relevant. And we wanna be able to, like, remove a story, you know, from all of our RSS feeds. But    
Me: Yeah. I'll definitely keep that. I I never even heard that.    
Them: Yeah. Well, I mean, it's a good thing that we don't hear about it, but because it means we didn't have to make any rural mistakes. So we had to like, somebody fact check this. But I'll also remove this with the backlog because I definitely would love to get this sorted. So just so we have our bases covered. We have a plan in place. Overview page, this is gonna be all NFTs. Oh, no. That's so yeah. So another part of that ETF stocks, NFTs, that whole prices, you know, initiative. I also was planning on an overview page. Actually, the design of it looked pretty sick. Let me pull it up. Just to share it. Because I wanted for it to be a full hub. For prices. Where is the latest I think this is good enough. Oh, no. This is not ours. This is an inspiration. Is it this? Yeah. I think it's basically like this. Maybe maybe we had an updated version, but this was basically, you know, the grid lines.    
Me: Mhmm.    
Them: This was the overview, basically, design where, like, you would select your watch list. So you'd go to all the, like, tokens, ETFs, stocks, etcetera, etcetera, and you'd favorite your your tokens, and then they would all show up here. And then you'd have all the views related to them.    
Me: Oh, wow.    
Them: Up here right below them. Yeah. So was, like, a initiative to try and sort of retain more users by, like, incentivizing them to have the watches. I've I've wanted to have a watch list for so long on our site where we just I think it's quite tricky to do the to do the caching and, like, you need profiles. So once we have auth we have authorization and profiles, that probably will be easier to accomplish, but still not sure when or if we're ever gonna be able to get to this. So for that reason, I'm not gonna close this ticket.    
Me: Would definitely keep it in the back of our minds.    
Them: Yeah.    
Me: It was good. It's similar    
Them: Let let    
Me: I mean, Matt's Matt's app, you're kinda personalizing    
Them: me Right.    
Me: like, Theblock.    
Them: True. So it's like, maybe it's just gonna be become that and that that's the main thing. You know? We don't we don't worry about. But this I'm just closing the NFT stuff with that. Definitely, definitely won't do. NFT's the next all fixed, and if this is not to do this. Watch list. We'll get to that. Okay. We were at over the page, and I these are closed, those ones closed. Okay. Visual representation of apps quality current state. What? I have no idea what this is. It's a QA process.    
Me: What what are you looking at?    
Them: Why am I here in my personal k. Visual representation. Workflow is broken. Okay. Bug priority wait. Did I share my screen?    
Me: It went back down.    
Them: I could get you. This ticket is referring to current state of that code and pro apps. In order the whole team to know what issues we have. See if you would just join us and find a workaround or not workaround, but like a framework for bug severity. I'll leave it because it's QA's ticket. So they are still thinking about it, maybe. Maybe it's worth it for them to keep it there. What time do we have? Okay. A couple more minutes. A lot of circulation. After second paragraph. And this one's not that not that, old, and it's a science marina. Can remove backlog from this? Because learn is gonna probably need to, like, add in the whole a whole sort of    
Me: Revamp. Yeah.    
Them: yeah. But I'll send my ticket still. Right. Or about Right. Our bot is currently working on this. Yep. You can leave this one. Price page. Oh, that's our zed or or intern PM intern, I think, was a year and a half ago, Good day.    
Me: Name is Ed. Yeah.    
Them: Yeah. Young Young Jones. What's his name? Oh, you went by zed? We had zed in that. It's pretty fun. Oh, I think this is actually taken care of. With Maria's work. Adding a column with buy button for ETFs. Yeah. Yeah. It should should include all that. This ticket is incredible.    
Me: It really got down to the weeds.    
Them: Mhmm. Spanning CMS booking status. Yeah. Not happening. This is for a pro. Funding dashboard, and I think we there was a request from one of the clients to see if a project has a token or not. But we actually so I think it's actually already made because we we add tokens. Like like, basically, to to signify if specific company that's just, like, raised, you know, a seed deal if they have a token or not, at least. And we already we already surfaced that stuff. So if we ever bring funding to that call, we'll    
Me: Mhmm.    
Them: we'll reevaluate that. K. Let me check. I think we have a call at nine. Yeah. For the campus off.    
Me: Yeah.    
Them: Alright. Cool. Let me just mark let me mark this as a stopping point for us, and we can actually can    
Me: Sweet.    
Them: continue We wear here, I think. There's very few tickets left, I think, because a lot of the stuff we    
Me: Yeah.    
Them: becoming a lot more recent and relevant. So twenty one nineteen.    
Me: Yeah. I also, I did a bunch of research on that x four zero two thing. So I could send you some stuff. If you wanna look into it. The pro    
Them: Sure.    
Me: yeah.    
Them: Yes. I'm assuming.    
Me: Yeah. Because that it's actually kinda relevant to what we're about to do with, like, the auth stuff. So    
Them: Yeah.    
Me: and, like, the Stripe connection. So it would make sense, but probably not for a little while. We have to we have lot of other shit on our plate. So    
Them: Right. How's the automation going? Have you looked at that all?    
Me: Yeah. I'm on I'm working on the second Zap and it's kinda like it's getting very tech because I every single time I was working with these something would break, something would not match up.    
Them: Mhmm.    
Me: So I really I really dug deep and tried to figure out like, how Zapier actually works. Like, better. And they have a bunch of steps that they created that it's like, Zapier tables, Zapier webhooks, Zapier SQL calls. So I've been including those. And the first app, it's like 18 steps, but it works. So and it's actually pretty legit. So    
Them: Okay.    
Me: now I'm on on the second one where it should send out like, after Zap one, it sends out the, specific    
Them: Mhmm.    
Me: edge, like well, the specific form rather. To that client. And now Zap two, it should it's building out multiple multiple different paths, for the actual ad itself, like where it would land in Jira.    
Them: Okay.    
Me: So, yeah, that should be done. I should have something by we we meet next week, right, with the with that ops?    
Them: Yeah. Yeah. I think it's not this week, actually.    
Me: Drop ops? Yeah. So I'll definitely have something to show then. Should be finished, hopefully.    
Them: Yeah. Don't feel like it has to be in, like, the super polished state, like, to cover all different scenarios and all different contingencies. It's like as long as we have one specific example, then we could sort of, like, at least get get their minds around. The whole process, and it's good enough. And then we'll know, we can kind of all, like, okay. We need prepare for x, y, and z scenario and, like, you know, then    
Me: Yeah.    
Them: Twitter versus email, like, all that stuff can be follow ups.    
Me: Yeah. And if you ever think of something, like, especially with Google Analytics? If you ever think of something that would be like, would make life easier for you, if it was, like, if you say, if you had, like, a specific type of, something that you wanted to follow within Google Analytics, like, just have it straight sent straight to your sheet, just let me know because it's a pretty easy setup. We have Google Analytics connected to Zapier.    
Them: Okay.    
Me: So if you ever, like, similar to the projects we were working on, like, earlier I don't know, maybe December or something like that before    
Them: Like, basically,    
Me: like, we decide    
Them: sending some triggers or whatever to    
Me: yeah.    
Them: directly to Sheets.    
Me: Just so you have it, like, in your inbox instead of, like, trying to search for everything.    
Them: Okay.    
Me: I'm getting used to    
Them: Yeah. Keep in mind.    
Me: it. Yeah.    
Them: Cool. Yes. That's true. It's definitely very powerful. We use a lot in other channels. Cool. K. Let's take a little ten minute break, and I'll see you soon.    
Me: Sounds good, man.    
Them: Peace.    
Me: Later.   
