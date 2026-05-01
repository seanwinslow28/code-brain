---
granola_id: 41bba522-9201-4d22-995e-eb34f02d2106
title: "Data (Pro Future) discussion - Transcript"
type: transcript
created: 2026-03-30T14:00:25.219Z
updated: 2026-03-30T14:33:27.458Z
attendees: 
  - erupkus@theblock.co
  - scousaert@theblock.co
note: "[[30_domains/product-management/the-block-meetings-granola-notes/Data (Pro Future) discussion.md]]"
domain: [product-management]
---

# Transcript for: Data (Pro Future) discussion

### Guest (2026-03-30T14:00:32.677Z)

Option. How we doing?

### You (2026-03-30T14:00:36.746Z)

Doing all right? Had some sort of stomach bug yesterday, so it was basically a non-existent Sunday, but feeling better today. Yeah. It was very irritating, but I'm feeling better.

### Guest (2026-03-30T14:00:50.997Z)

Oh, man.

### You (2026-03-30T14:00:51.946Z)

So.

### Guest (2026-03-30T14:00:52.597Z)

That's all that matters.

### You (2026-03-30T14:00:53.546Z)

Yeah.

### Guest (2026-03-30T14:00:53.957Z)

Love it when it's. When it's the weekends, they get ruined. Right?

### You (2026-03-30T14:00:57.466Z)

Exactly. Yeah, I had, like, I was like, oh man, finally a weekend where I have it to myself, I'm able to get shit done. And Saturday I got a decent amount done. But then yesterday, just literally just slept pretty much all day.

### Guest (2026-03-30T14:01:15.077Z)

This looks man.

### You (2026-03-30T14:01:16.346Z)

But I'm excited that you planned this meeting with Simon. I figured I was like after Friday where we were a bit lost. I was like, I think we need to. Talk to other people, see what they have in mind.

### Guest (2026-03-30T14:01:31.397Z)

Yeah, exactly. The whole Stephen also to also pick his brain about research a little bit. See what, because he. He usually has a lot of ideas, but he never gets asked the questions, so I thought I. Thought I'd do it.

### You (2026-03-30T14:01:46.586Z)

Nice.

### Guest (2026-03-30T14:01:48.437Z)

So, yeah, we'll just see what, like, is there anything? Hey, Simon.

### You (2026-03-30T14:01:55.386Z)

Going Simon.

### Guest (2026-03-30T14:01:55.397Z)

Hey, man. How are you? I am doing great. Yeah, it's been a while, but I've. I've been great for you. Not too bad. Have you met Sean yet? No, I haven't. No. Nice to meet you, Sean.

### You (2026-03-30T14:02:10.106Z)

Nice to meet you as well, Simon.

### Guest (2026-03-30T14:02:10.357Z)

Sean is. Our Sean is our APM. He started with us in the fall. Basically, you know, him and I are managing. Go on campus. And Simon is. Our. Is our Simon AI. The person who's Simon has been named after. So probably the title speaks for Excel. For itself. But, yeah, Simon, I I scheduled this call to fix your brain a little bit. About data, specifically in the pro context. Because as, you know, as I texted you a couple weeks ago, we're thinking about pro and thinking about all these different Avenues. That we should take with, you know, the offerings that we used to have or might have. Depending on the CEO, the new CO that will join and, like, you know, we have to basically prepare for them specific plans that they could potentially embark on. So that's sort of the context and why we're doing what we're doing. So obviously, like, the whole data Consortium thing is very ambitious and, like, a huge project. But it's maybe too broad or too, like dream state. We're thinking about. Potentially if we were to revive, bro, the platform itself. What is basically. Our strategy and what we want to do. So Sean and I have a bunch of ideas and, like, the guesses about what. You know, has gone wrong or what is missing from the current pro offering. So I just wanted to include you and, like, ask if your brain, basically on what are your thoughts about what might, might have gone wrong or what it is currently missing that could Elevate the tools to the next level. Okay. Okay. Is that an open question that I should answer now, or should I just, like, think along with you guys? You can. You, if you have any thoughts, you know, specifically around. What Pro was when we were selling it and, like, why do you think. Obviously, like, bull market and bear markets affect the demand? But, like, why do you think it's. It's not that, not done as, as well as it could have. Right. I think one of the main perspectives, you don't have to speak for riches, you know, if you don't want to. Right, right. I would say the searchability, I think that's the right word for charts. And that means the underlying data sets that we offer is pretty. Bad. And there are so many charts and you have to scroll through all the pages and actually, like, until you actually know what we have to offer, I think you have to spend a considerable amount of time into the, into the data dashboard, which is obviously not great if you. Want, if you want to onboard new clients, for example. Another one is, for example, all of the markets charts, we all, we have all of these aggregations that underlying we have this data set of, like, hourly level data on for every market. And people are, they just can't know. There's no way to know for them as well. So there's a lot of data that we had that we are not offering through the charts as well. I think those two are, are pretty important. There's some data that's, like, not even visible on, on any of our front end. I mean, the first chart that you're seeing on the data dashboard is spot market monthly volume. So that is USD volume per exchange, but aggregated over the whole month. While underlying we have for all these exchanges, we have all the markets available on these exchanges on an hourly level. So we know this data way more granular, granular than, than the stuff that we're showing. And, and where is that data coming from? Is that like our proprietary collection or like, is it, is it license through somebody? Like, how does it, how do you guys collect that? Yeah. So markets data specifically, we collected by going through all of the exchange apis. So that is what I would say. Yes, it is proprietary. Nice. So it's something value to tell. Like we wouldn't have a problem like marketing. To any other. Remind me, remind me of the, of the makeup of, like, the data that we can sell and, like, sort of use for profit and data that we can. Yeah. So there's three buckets. One is markets data. Like, like we just discussed. It's, it's us collecting data with an API. This is kind of like we always consider it to be owned, but it's not really our data as well. It's, it's actually from the exchange, but we feel safe enough to sell it as our own. We have collected it for analytics purposes or something. Then there is all the on chain stuff that we do in house that is actually propriety, I guess, because we write the scripts to parse the data from raw data into ready for analytics data. And then there's everything else, which means it comes from a third party that is, for example, defi llama, this coin gecko, that is data that we just cannot sell. That, that will be illegal. And since everything is nowadays so multi-chain we notice that it's easier to get data from these third parties as opposed to getting it ourselves. Because if you need to parse an ethereum and solana and arbitrum and polygon and BNB chain, it's. It's starting to get impossible, especially for a team of two. So that's where we always make a balance between if we can do it in-house preferably, yes, because we can sell it. And we also have much more control about the data. But if it's too much effort, we just have to take it from some, somewhere else. Gotcha. And. Another one we were chatting about data consortiums. You mentioned that, like, you know, partnering with a few. Different data providers would get paint a much, like, complete picture of the full data, crypto data environment. So with the stuff that we have. Currently in house that, like, basically we can sell. What do you think? Like, what's the percentage of it? Is it 50? Is it 30? Like, where are we at with the stuff that we have? My estimate is always 60, 65. Since we own basically everything in markets, ETFs. Treasuries. And then it's starting to get, like, more balanced, like stable coins and then the on-chain metrics and then defi. Defy. We don't own a lot of it nowadays. Again, especially because of the multi-chain stuff. But the most popular categories, which are always have always been like market treasuries and stable coins, we pretty much own 60, 70% of it. So. Gotcha. If, if there was, if there was, like, let's say. One area where we were. Like, either. We would acquire rights to the data or some sort of, like, partnership, like, you know, to bring that data in-house what would, what would it be specifically? In your, who would your target. Provider or specific area of sector of crypto data that you'd just like to, you know, looking? I'm looking at the list that I sent you earlier. It's, it's a llama coingecko, and they all are pretty much necessary. Coin gecko is purely necessary for the prices. Anything that we want to do that has to do something with market cap or prices, it's going gecko. Like, we all also use it for the prices product. If I llama is coded for everything defi and then there's token terminal, which has basically everything else except for rwa stuff, which is then kind of like this super niche. Bucket, which only rwa dot xyz does well. But with these four, we, we can cover pretty much anything, especially, I mean, that combined with the stuff that we already own and it's pretty easy to maintain. We have everything. Gotcha. The reason, and that's one thing I'd like to add, the reason why we have so many third party providers today is because we want to do everything for free. Like, and then you have to kind of, like, take into account API usage and then some other sources who are free. I mean, we, if we could take anything from token terminal, like half of the charts that we do not own will go to token terminal. But we're, we don't want to pay for it. So we, I need to find, like, five or six other companies who have the same data, but for free. Yeah. Yeah, it's definitely tough to dedicate resources to, to a initiative that doesn't really, like, that doesn't yield immediate, you know, payment or subscriptions or whatever. Exactly. I've seen this in the last five years. I mean, it's, it's basically always the thought, like, okay, we can spend the money, I guess. But until this day, it's not have, it never has been very clear how data specifically will get a return on that investment. It's just part of the overall package advertising machine, I guess. So it's hard to kind of. Like, convince larry or anyone else to, well, give me 20k year and I can buy some stuff. Right. It's interesting because the current. Pro, like Pro still, like, generates almost, almost a million dollars per year. And all these clients that engage with us and still, like, subscribe, basically, they're, they do it not entirely because of what majority reason is because of data. So they, they are still finding value in it. So it's interesting to, like, You know, as we're going through this exercise, we're trying to look at, like, okay, like, why, why are you still here? Like, this project has been sunset for 18 months. There's no support, no nothing, but they're still, you know, Fine. The reason, I guess, to spend money and utilize it. So it seems like there's something still there. We just maybe didn't have the right approach or we didn't polish it enough to. Yeah. To offer. There's also this kind of, like, Pareto principle where, like, 80 of our decline requests is about, I don't know, 20 and probably even less percent of the charts. It's always about stable coins, market data. And then since treasuries have come along, treasuries, that's basically it. Like, nobody, nobody goes to us for defi data, or it happens sometimes, but it's very infrequent. Yeah. It's also, it appears that a lot of stradfi companies, like, I guess from the conversations that people have had with the CEOs, the new potential CEOs, the focus and the consensus amongst all of them is like unanimous. That event will have, like, another wave of institutions, especially like trad five people spinning up crypto teams again, and they're interested in the, like, adoption of crypto. So, like, payments, stable coins, rwa tokenization, like all those things are going to be very relevant as well. So, like, if we could build. Some sort of coverage with data for that, like, that would set us up in a very good spot. Obviously, in addition of other things that we would able to provide. That makes sense. That makes sense. It's also probably not an accident that this particular data is the hardest to get, like doing or the waste of right. We've, I've tried it. Like in house. It's a nightmare. It's a nightmare from a maintenance perspective. There is no standardization at all. There's technology on these weird chains, but, like, have billions in dollars and, and think. But there is no integration tools at all. So you have to build everything from scratch. It's crazy. So it's way too expensive. If we need to hire people to do this in-house it would be. Probably cost, like half a million dollars a year, which is way too much. Yeah. So rwa.xyz it that they basically wanted the providers that, that do that. Yeah. The only one that do it well. And how. Like, I haven't done any research into them, but are they. Like, are they licensing their data? Are they like, I don't know. Like, how does, how did that work? So we actually use them right now because we have, like, this partnership. It's basically me talking to this guy and basically asking him, like, hey, can we use the data for free, please? And he's like, yeah, yeah. If you send me the numbers on the traffic and I'm like, yeah, yeah, no problem. I'll send you the numbers. But never sent the numbers. So it's kind of sketchy, but at least we, we are using them. Like, they have an API. We are integrated. So, yeah, it's once you have, like, a proper deal, it should be super easy to get the data from them. Okay. It's definitely helpful to know that we at least have, like. Person contact, you know, that we could reach out to. For sure. They would love to, by the way. And also, like, for example, coinbase reached out to us for rwa data. And I'm telling, like, hey, I cannot solve this to you, but please go to rwa. And then he's super thankful as well. So we actually have, like, a decent relationship because of that. Nice. Okay. Anything. As you mentioned, obviously searchability, discoverability. Any other things that come to your, to your mind that's like, you know, if we, if we were to redo, like, what would be your favorite things that we, the product team would focus on? Yeah, go ahead. I was gonna say one of the things that we had talked about and we were just, like, mocking in designs. Was this. Like, data or chart creation tool. I don't know how much. Like, value there is in it. But it could be one way of approaching that, that sort of problem of, like, not, not being able to display. A million charts that represent the same data set, like, from very different angles. So having a data creation tool where you, like, sort of pick your own series, pick your own sort of variables that you want to, they want to see. That could be one, but I just, like, I just, I'm just, I guess, you know, guesstimating. I'm not sure if there's any value in that. Was actually the, the exact thing that I was about to say as well. We have, there was one thing we haven't really covered, and it's just like we're doing the whole product, like, make people, let people make their own charts. We have thought about this in a previous iteration. Maybe after five years, I'm getting too cynical, I don't think I will make money. Like, if, if that's going, if that needs to be the different, differentiator, I don't think that's going to work. There have been other tools. I don't know. I don't think that's. That's going to solve anything. It's, it's nice to have, but if I'm not sure if it's going to make or break things, I don't know. That I appreciate that. I think, I think they definitely, I followed myself up with, with, like, I'm just estimating I'm, you know, shot at shooting in a dark, basically. But. I think when, when mats were joined, we had the same kind of, like, reasoning because, mat, I think in his previous job had some experience with this kind of stuff. And the conclusion was we need to do some, some market analysis, like with our clients actually want this. We have no idea. So it's, it's a, it's like, let's try and, and see what it, but it's, it's not super easy to create and do it while I think. So it would be pretty expensive to not even be sure that it's something people want. Okay. Sean, anything. That has come to your mind?

### You (2026-03-30T14:19:25.466Z)

You asked pretty much all the questions that I was going to ask, but I guess one of the last things that I would ask would be do you see a value in having like a central hub or would you think that it would be preferable to keep pro to put pro as like a headless CLI? Like you're essentially just getting the data from API.

### Guest (2026-03-30T14:19:47.877Z)

That's a good question. Which probably has the same answer. Like, I don't, I, I don't think our clients are super technical. Like, if, if you're going to try to sell them data with the CLI, I think 90 will be like, what's a CLI? So I'm not sure. I, I would think it would be amazing because I'm, I'm a programmer. But, like, if the clients themselves are non-technical people. I don't think that would be valuable. But again, I'm way out of touch with most of our clients, so I have no idea if how these people profiles look. I also probably would want to ask about Simon AI, too, because that.

### You (2026-03-30T14:20:27.946Z)

Yeah, that's fair.

### Guest (2026-03-30T14:20:33.157Z)

Like. Obviously we spent a lot of time, you spent a lot of effort on it. But there's ways to make it better. And in the current iteration, it's probably, it's definitely not something that we could, like, advertise. It's just not powerful enough. That's not have enough data. Do you think that, that has a, some sort of potential. Not to be the soul, not to be the sole, like, value add, but, like, an additional tool? Like, is it something that we should even look at?

### You (2026-03-30T14:21:04.186Z)

Another nice to have.

### Guest (2026-03-30T14:21:06.277Z)

Yeah. The current version is, is shitty, but, which is normal, I guess, like it's built two years ago, which is a huge amount of time in AI models getting better, technology is getting better and more efficient. I told this to Mike as well. The main problem today is that we put everything into the system, everything, which means there is a lot of conflicting information. So it's garbage and garbage out. You can throw the smartest model at it. It will not be able to figure out because we have like 10,000 articles on bitcoin price, for example. If you ask about bitcoin price evolution, it will have no idea. We have so many articles and so many stuff that it will not know. That's something that we can improve on for sure. We need to be smart about it. I have no idea how to do it now, but we can think about that. And everything else, I think will solve itself with better intelligence of the models. Everything that comes after the context. If you know, if, if that makes sense. And, and from a business perspective, if, if it actually has value. No. Yeah. No, I like to like the frankness.

### You (2026-03-30T14:22:29.706Z)

Does it currently just pull.

### Guest (2026-03-30T14:22:30.437Z)

I'm not sure.

### You (2026-03-30T14:22:31.866Z)

It just pulls from like, like how far back does it go? Like how far back does the vector database go that it's pulling from? Like years and years?

### Guest (2026-03-30T14:22:40.197Z)

I think it. Yeah, yeah. 2020. I think.

### You (2026-03-30T14:22:43.066Z)

Oh shit. All right.

### Guest (2026-03-30T14:22:44.597Z)

The beginning. So there's a lot too much information, actually. I think that's more the problem. There's too much information in this, in this system. But I actually do think it could be valuable over just a generalized models, because if you ask it any crypto question today, it will give you a good answer. We, you don't need to block Simon AI to, to do that. Where it could be helpful is if you actually want, for example, link data to it. What is the actual price evolution? Of bitcoin and percentages, and then it goes to our backend, looks at the prices that we have and then calculates the percentages difference and so on. And that's pretty unique, right? That's just not somewhere around on the Internet or maybe that example in particular is. But you know what I mean? But any general crypto question that is solved, there is no need for a product from us to do that. What if Simon was just Theta? What if it didn't have any. Like, it's basically like a, the tool is within the data dashboard and it's, you can. Query the data with it. So that it can, like, if you ask it, I guess. You know, what are the monthly volumes on binance? Dating to 2025? Is this something more. No, no, it's, it's more valuable, but not more usable. Because I can imagine people asking about what is options volume, and then they're like, okay, it's, it's 20 billion dollars. And then they're like, okay, but what is an option? Actually? And, and then suddenly it, it will start to, like, I don't know. I only have the data. So you need to take well or deeply about how this integrates with within, like a broader product, which is not linked to the block or something. Needs definitely more thinking. I have no idea. The data is a valuable part, but then it, it gets kind of weird with the user perspective, user experience. And it's also these days general alums are just, are so much better at answering all these questions. So I just don't think. Like, you really would have to spend a lot of time and a lot of resources on perfecting the LLM model. Our own one for it to have an advantage over, like, people, other people's, you know, the general LLMs, basically. And this is why I think it is pretty valuable today because we have all the, we have done all the technical work, the integrations to actually get the data. While an LLM will not write, or usually it will not write a script to get data from binance for a certain market. And then today it's, it's not doing that. It will be probably at some point. But the hard work we have done, and then if you give it all the data to the LLM, it will give you proper answer. But this is the first part that's valuable. And that's why I think hooking up our data. Into Simon AI or whatever you call it, is today still. Probably valuable. Okay. That's worth looking into them at least. Yeah. Well, yeah, yeah. Okay. Definitely have our work cut out for us, bro. But we have to just approach you and see what they're focused on. My personal opinion is that, like. A lot of our. Engagements with, with companies are super Niche. Like all these companies like Fidelity, MasterCard, etc. Etc. They have very, like, specific. Questions and needs that they need answered. And it's like, sure, it's nice to have, like, the general markets data or whatever, but they need, like, very specific stuff and they need specific questions answered and, like, basically, basically it's Consulting. Almost. And the, the thing that people continuously say is that we had no idea the Block can offer that. Like, we had no idea you guys could pull specific data. We didn't have no idea how the expertise on, like, tokenization or stable coins or whatever. And, like, to me, it seems like that is. The, the opportunity is to. Somehow. Communicate that we do offer that. And, like, obviously it's harder to scale that sort of business where it's, like, very much Hands-On and, you know, it's not just. Like getting the data and then just. Selling it, you know, or for apis or whatever. So it's, it's a lot more work and resources intensive. But if we want to go that route and be that sort of fill in that void that's missing and crypto, I feel like that could be. An area because we, right now we just don't spend any sort of, any communications in terms of telling people what we can do, like all the specific case studies we've done, all those, you know, the clients we've helped before. There's no, no track of that. So. Yeah, we'll continue working with the other insights were definitely helpful. I get it. I get the tension between product. I mean, the block to me, I mean, again, after a few years, you kind of like get a hang of it. Like, it's, it's a consulting company, right? The only way we make money as Consulting right now or like 80, 90, I guess, and advertising, of course. But obviously everyone who has, like, this multi-year horizon wants to make some sort of a business a SaaS product. Like, it's a product that sells itself and it's scalable and it's $20 a month and it's. And I, obviously, that's the way to go if you succeed, but it's, it's not going to be easy. With the current setup. Cool.

### You (2026-03-30T14:28:55.706Z)

Yeah.

### Guest (2026-03-30T14:28:55.957Z)

Yeah. I agree. Thanks. Sorry. That was a bad note to Android. Sorry, I mean, it is what it is, right? That's the reality. It's all these, all these other providers are dying, you know, like Block works data is or black horse, you know, shutting off their editorial and the sari's laying off people. So it's, it's hard everywhere. It's not like we're just the ones that are, of course, struggling to, to put out something and just embarrass even harder. So, yeah, we'll continue to kind of. Wrestle with this. And I think. We'll put together a pretty max proposal for the new CEO coming in. So we'll see, we'll see what they. Focus on. Okay. Can I, can I end with one more question? How do you guys from the product team look at all of these leadership changes? In general? Yeah. Like, how does it feel for you guys? Because I can imagine it changes a lot for you. But, like, omayan, for example, whether Larry or anyone else basically is in the seat.

### You (2026-03-30T14:30:04.666Z)

This. Color trying to get. My fellow to it.

### Guest (2026-03-30T14:30:09.317Z)

It's, it's pretty much the same workflow.

### You (2026-03-30T14:30:10.986Z)

Same.

### Guest (2026-03-30T14:30:12.757Z)

Because research is still kind of like its own small unit, I feel. Yeah. Yeah. Like data is data. Like, we, every CEO is going to say, like, we need more data. We want to have it, you know, complete. So, yeah, for us, it's definitely been hard to.

### You (2026-03-30T14:30:29.066Z)

Difference. In. What.

### Guest (2026-03-30T14:30:30.677Z)

Like, because with every change, with every sort of change of plans. Like, it almost happens, like, every six months or every year. So, like, and you, I'll tell you essentially start over every, every time there's a change. So, like.

### You (2026-03-30T14:30:44.026Z)

S here.

### Guest (2026-03-30T14:30:45.637Z)

We had this whole plan with, like, with Caleb and we seemed like we were sort of hitting the stride. But then. All of a sudden. Thou got, you know, thrown out into the, into the trash bin, and then we have to start over. And, you know, what's, what's, what's going to be the future of a campus? Who knows? Like, and it's. Yeah, it's just, it's just hard because there's no, like, we're always operating at such a short time Horizon. Yeah. It's hard to build something that's, like, very long term because you just can't, you can't focus on it. We have people coming and going every half a year, essentially. Like, losing those and hiring them slowly for specific initiatives. So it's just. Yeah, it's, it's a, it's a lot of, like, tug and pull, and it's. It's definitely difficult, but, like. I don't know. Seems like we, like, the Block from, from market share standpoint has not been, like, it's basically at an all-time high, essentially. Like, in terms of clicks, in terms of traffic, in terms of, which is weird, right? It feels weird. Like, we're internally, it feels like we're doing something wrong. But then on the outside, it's, it's like we're booming. Exactly. So it, it's, it's definitely hard to. Maybe it's just that, like, competition is dying a lot faster than, than just, like, survival of the fittest almost. Sometimes it's, you know, all you need is just one super clever, clever idea. And, like, you, you know, enter the world stage. So that's what we're, that's what we're aiming for, just to think of the golden nugget and what, you know, what, what that would be. Yeah. So, yeah, the CEO changes are definitely. Not. I would love to have, like, a full two-year plan that we could, that we could work towards and we can actually, like, you know, get resources and not be rushed to meet deadlines every, every single month. Yeah, that makes sense. Well, I appreciate the work you guys do, obviously. So thank you for, for doing that and taking the time to talk to me as well about whatever you guys want to do. Yes. Appreciate your insight. Simon. Of course.

### You (2026-03-30T14:33:13.946Z)

Yeah, man. It was very nice meeting you. Thank you.

### Guest (2026-03-30T14:33:17.077Z)

Likewise, Sean, nice to meet you. All right. Have a good one, Simon. I'll talk to you.

### You (2026-03-30T14:33:22.426Z)

Guys.

### Guest (2026-03-30T14:33:23.877Z)

Cheers. Bye.

### You (2026-03-30T14:33:24.186Z)

Bye.

