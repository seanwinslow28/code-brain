---
granola_id: 1f13b5bb-df6b-4cee-824a-da840fd59859
title: "Google Ad Manager Operations Sync - Transcript"
type: transcript
created: 2026-03-24T15:30:47.230Z
updated: 2026-03-24T15:47:49.347Z
attendees: 
  - kvallecillo@theblock.co
  - vlu@theblock.co
  - erupkus@theblock.co
  - ysmagulov@theblock.co
  - mprice@theblock.co
  - ldanowski@theblock.co
  - rmirzaie@theblock.co
  - jmilligan@theblock.co
  - tim@theblock.co
  - npivcevic@theblock.co
  - mlozuk@theblock.co
note: "[[30_domains/product-management/the-block-meetings-granola-notes/Google Ad Manager Operations Sync.md]]"
---

# Transcript for: Google Ad Manager Operations Sync

### Guest (2026-03-24T15:31:16.482Z)

Greetings. Everyone. Okay, let me check. I think we have everybody. Have the whole core here. So we can get started. I don't really have an agenda for today's call. One of the things that we could check in on is the tests that Sean and I think you met with Lil and Carla to discuss the automation. Progress, basically. So happy to talk about that. I also saw. A call come in on the ask VM channel about. A pixel tracking, the IAS. Yeah, it seems like that one was answered. So awesome. So what was the answer there? Yeah, we can add the tracking. We can do it. Okay. All right. So. On this, we have an RFP came through via dentsu. They're asking for a ton of information. It's a 30k budget. They want. So what I'm going to do, I will send to ed, you and Ymac. What exactly they're looking for to see if we have some of this information handy. It's pretty comprehensive for this 30k. Typically, I wouldn't want to put all this effort into something that's 30k. But this is probably not going to be the last time we receive such a request in terms of what. Some of these big ad agencies need from process and compliance standpoint and a tracking standpoint. So we could do the work now. We'll have it ready for the for any future RFP. So I'll send you through. It's for JPMorgan Chase. So it's worth it from a client standpoint. But we'll see if you guys have questions on this, let me know. The question that I want answered is, can we do it? Meaning based on their technical requirements. Is it something net new that will need to implement? For example, the IAS pixel. Is it something that we've done in the past to just generally get that understanding? Sounds good. Yes. And the rover will take a look. Thanks. Where were we with the. Salesforce automation for closed ones? What's, what are the next steps?

### You (2026-03-24T15:34:18.482Z)

So yeah, so for the most part everything is built out. I just have to finish the testing so far the testing has been going well but Lil I saw that you posted a message in slack and then you deleted it. About you wanted to remove something from Q1 like all the stuff that you made for me.

### Guest (2026-03-24T15:34:35.602Z)

Yeah, because I figured it out.

### You (2026-03-24T15:34:37.522Z)

Okay.

### Guest (2026-03-24T15:34:37.522Z)

I'm just, I just edited it out of all of my reports this week because I was going to ask how long we need to like leave those tests in salesforce. And then I answered my own question.

### You (2026-03-24T15:34:47.762Z)

Gotcha yeah it should be done by the end of this week or the beginning of next but Karla do you have those PDFs that. You were asking me to add to. The automation?

### Guest (2026-03-24T15:34:59.842Z)

Let me share them with you right now.

### You (2026-03-24T15:35:01.762Z)

Sweet thank you. Yeah so for the most part everything's everything's done I just have to run a few more tests. And then hopefully we should be good to go but I'll keep on monitoring it just to make sure that nothing's breaking or nothing is out of whack or some sort edge case through throws something off.

### Guest (2026-03-24T15:35:25.842Z)

That includes both email and Twitter. Or not, but our telegram.

### You (2026-03-24T15:35:30.962Z)

Not telegram no we're going to save that for another time because adding the well now it's becoming a more regular thing but adding like telegram and the bod father it just adds like a whole layer of confusion within zapier itself.

### Guest (2026-03-24T15:35:31.682Z)

Messaging. Okay. Are there any clients that exclusively communicate through telegram and they don't have like they don't provide emails? For the most part, the communication is on telegram, but a lot of times they'll send us like Google files. I don't think it'll be an issue. Okay. Sweet.

### You (2026-03-24T15:36:05.442Z)

Okay. Yeah I'll test that out more down the line but for now. Just because there are so many different forms like I just don't want to I don't want to break it and confuse it just yet.

### Guest (2026-03-24T15:36:20.402Z)

Yeah, when you think you're in a good spot, let's meet, let's, let's have a meeting and we'll throw it together.

### You (2026-03-24T15:36:25.362Z)

Cool.

### Guest (2026-03-24T15:36:28.482Z)

Any, any, any questions or things to bring up from the game standpoint? No, I'm not stealing my end. Well, then the last thing, I guess. One of the, one of the previous meetings we had talked about the. Impression based contracts. I just wanted to bring that topic again in case we were ready for further conversations. If not, that's fine as well. The duration. Slash impression based. Play ad. S. I think we have any updates. It's like technically we can do it. We just need to. I don't know, test. I think if we have any. Chance to. Investigate it or make a decision or, you know, something along those lines. Can you repeat the question? Just wanted to bring the topic. Up about the impression based contracts for display ads. In case you had, you know, more info to share or we are getting more and more requests for CPA based models every day as opposed to duration. So no update. I know the last we spoke in February. We wanted to have a decision in early March, but I think they're still moving pieces in terms of the team is still selling direct. We still have open inventory. And we are getting really over the last two weeks, we've gotten probably five or six different requests for either agencies or specific clients that are looking for like a $5, $6 CPM. And contract with us based on number of impressions. So for the foreseeable future, we'll continue to do both. Until the market tells us one way or the other. Frankly, I don't. We make too much money selling direct, so I don't necessarily see that going away anytime soon. I don't know if anyone else has. A strong opinion or thought on that. But in, since we do have these unused inventory, we need to find ways to monetize. And I think that's where the impressions based models can come in. Got it. Have we started testing? I know we said last time that I don't know what the final decision was, whether we were going to do a small percentage and start testing. I know we were going to try when okx canceled their three weeks, but then they came back and rescheduled them. So where are we? There? Is the question like, can we do both at the same time or have we done both? Have we tested? No, we were going to test. I think you had to, like, under 5% or something. Did we start that or are we still waiting to start that with kicks to finish? And I have. Turned on programmatic on our loan pages and waiting for me to start the campaigns just to make sure the campaigns work as intended. So you have turned it on or you will turn it on after. I will turn it on after Erik's and I have asked alchimi to turn it on for our learned pages. And as far as I will see just one or two impressions, I will turn it off again. I have turned it on only on learn pages. Why would we not keep it running, Yuramak? Is it just because of okx right now? Because ok is kind of guaranteed campaign and it will be shown always like it will take 100% of our impressions. Yeah, I'm in agreement with you. I mean, we made the decision to not advertise poly market in a specific piece of real estate that was promised to them. And they're just going to have to wait until okx runs their course. So I'm good with that decision for sure. Let me know when we do turn it on. Like do we have any sense of, let's just say we, we turn on programmatic. Flip the switch. Do we have any revenue projections based on site traffic or any potential numbers that we can work with here? Because we would need at least, I don't know, maybe a couple of days of programmatic month to understand the fill rate to understand the CPMs, etc. Okay, so then my next question is there is with alchemy, do we have. A predefined rate. Okay. Any reason that we don't. Was it? Go ahead. I'm sorry. I don't even know. It's like, I don't know about any business conversations with them. So I'm not sure if we had any. Yeah, Jeff, I think just the current idea is, you know, you get multiple. Partners bidding and you sort of. See how high they're each going to outbid each other and kind of find out how much. We're going to get from programmatic if we want to do if like that was kind of, I think the starting point and it's taken us like half a year and we're not even at the point where we can start serving these. But like once we get there and we start getting that information, then if we want to do like a fixed deal with them. Then we can. Cool. You answered that you answered my next question, which was, is it just an element of getting multiple partners in bidding? So it is, it is what you, what you mentioned. They would, in my experience, they're probably open to a fixed rate deal like we could consider if we only have alchemy. We don't have any other partners. We can go back to them and say, hey, we'll give you a reasonable CPA CPM. Probably it's probably going to be under like six bucks. But to start there, they would be the only provider. And then to kind of shift the model once we get some other partners. Another question actually, do we need to bring on the partners who will be part of our programmatic ecosystem. Or is it open to anyone? Need to bring them on? Okay. Okay, cool. Yeah, I mean, in theory, it sort of opened to anyone that wants to work with us. We can get them set up. One element is do we go with Google? Because with Google, we might get scam ads. It's going to be quite a low CPM, but they'll probably fill, I presume, all the inventory just at like, you know, potentially quite low cost. Okay. Yeah, I think so. That's more so the question that I was trying to get at. I didn't articulate it well. So. The Google button, like that to me, like when I think about programmatic, I think of Google. When I think of alchemy, I just think of a partner that has inventory from their clients and they're giving us that inventory at a rate that may or may not be fixed. So do we have the ability to just turn on like the auction for Google at any point? Yes. But it would be up against alchemy and any other like crypto partner. Because the point is you basically say all of them, how much you want to pay, whoever pays the most. We get that. Okay. All right. I also want to, we want to gather that data first. I think before we can then try and do fixed deals. Because, yeah, otherwise you might do the fixed deals at cheaper than you might get from the bidding wars. Yeah, I agree. I agree. And my preference is to bring on trusted partners where we know they have good crypto clients as opposed to the Googles, where you just have less control, it would seem. Just as you mentioned with like the quote unquote scam ads. Tim. Yeah. Plus you will get a lot of non crypto ads, I imagine through Google, which I always find looks a bit not ideal for right now. Totally agree. Yeah. Okay. Yeah, I think we decided not to run Google at first, didn't we? Yep. Yeah. So we're going to start just with the crypto partners. Let's say if none of them are by any of the ads, then we might like switch on Google. But if they just take all the inventory, then we probably wouldn't choose to switch on Google. Tim, if I were to. So I mentioned there's been a lot of inbounds, a lot of one off requests. Can I send some of these partners your way to just chat with them about. Deals similar to alchemy? Okay, we'll chat offline. I just want to make sure you have time. Cool. Okay. So. We'll wait for alchemy to be ready. Let's turn on essentially for us to test our functionality. And then we can communicate then what we want to proceed with. We'll take a look at the RFP. That Jeff will send our way. We'll take a look at what they're asking for. And then we can. Head about, you know, the topic of impression based constructs. Next time we meet or the following times a week. Ed and your Mac, you have the email. Someone brought something to my attention around. Someone was looking a bit deeper into the, I don't know what the right terminology is, but taking a look at the coding for our site. They found that there was code in there, for lack of a better word, from a company called freestar. Freestar is like a big programmatic ad provider. Slash technology provider. Based here in Philly. Have we ever worked with them? And if so, does it ring a bell to anyone? We had an integration a while ago, but we since took it out, like we stopped using them. It shouldn't be there anymore. So it's my understanding, Michael, that it is still there and it's visible. All right, we'll take it out. We're not using them. It's somewhere in our 60 file. At least it was about a week ago. If there's any, is it a matter of just. Snipping that piece of the back end out, you know, no impact to anything? Is it just sitting there as a relic, Mike? Yeah, it's just a relic. There's nothing that depends on it. We could just rip it out. Okay. All right, cool. Yeah, keep me posted on that one. Thanks guys. Awesome. Thanks team. Have a good rest of your day. You too.

### You (2026-03-24T15:47:43.762Z)

Guys.

### Guest (2026-03-24T15:47:43.762Z)

Thanks. Bye everyone.

