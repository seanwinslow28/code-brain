---
granola_id: c0f86a63-ff50-4e0b-96c7-70a9d5f7d838
title: "Sponsored Course Implementation Kick-off - Transcript"
type: transcript
created: 2026-03-16T13:12:55.058Z
updated: 2026-03-16T14:48:42.823Z
attendees: 
  - akryvanosau@theblock.co
  - erupkus@theblock.co
  - mhulis@theblock.co
  - rvishneuski@theblock.co
  - norobenko@theblock.co
  - bmendoza@theblock.co
note: "[[30_domains/product-management/the-block-meetings-granola-notes/Sponsored Course Implementation Kick-off.md]]"
---

# Transcript for: Sponsored Course Implementation Kick-off

### Guest (2026-03-16T14:00:39.631Z)

Yes, Sean.

### You (2026-03-16T14:00:40.732Z)

'Sup, guys?

### Guest (2026-03-16T14:00:45.571Z)

It's about I guess so.

### You (2026-03-16T14:01:17.762Z)

Ramon, you bold board already?

### Guest (2026-03-16T14:01:21.451Z)

Hello. Sorry?

### You (2026-03-16T14:01:23.802Z)

Said you're bored already? Just

### Guest (2026-03-16T14:01:28.781Z)

What what do you mean?

### You (2026-03-16T14:01:31.202Z)

I was just joking, saying you you went online and immediately you were like this. Are you at work?

### Guest (2026-03-16T14:01:37.461Z)

You know,

### You (2026-03-16T14:01:38.132Z)

Bear. Understand.

### Guest (2026-03-16T14:01:40.471Z)

little bit exhausted. Long day.

### You (2026-03-16T14:01:42.902Z)

Yeah.

### Guest (2026-03-16T14:01:43.521Z)

Yeah. I don't think Brian will join. You know if Mhida? Will will be here? Let's give him a second. I I just ping him just in case. Thanks. Okay. We should probably just turn it over and just fill them in. Oh. And we could Hey, Nick. Sorry. Some login issues happened. Don't worry. No worries. Right. So probably there's no need in going over the message anymore. Main thing is that pausing on the 201 individuals and gonna go ahead and implement the sponsored course support for campusand.co Yeah. So we just scheduled the call to go over any specific questions and concerns. That would come with doing it right now. We have all these epics assigned. I don't know if you had a chance to or these tickets assigned. I don't know if you had a chance to look through the epic. But, Nikita, you mentioned that you had a you had a question in the message this morning. Yeah. Exactly. As I've already started preparing the back end up for this course of courses. Or would be public access? Courses. And I'm I'm a bit not clear in terms of how exactly we should handle the works with the expiry of the access. Because we did not have the support for that before. We did not plan that for the upsells. So if you the subscription is expired, it means that you just cannot sign in. Yeah. Ideally ideally, it would mean that you can sign in it just the yeah. Go ahead. I mean, like, you yeah. I I understand that it should be, like, you can sign in, but everything should be blocked. Or there should be a payable or something. That you should see instead of the interface. Or the functionality. But we we don't have it. Right now. Yeah. For for enterprises, I mean, it's highly likely that people would not log in after their, you know, after their subscription expires or they they discontinue the the enterprise support. So we don't have it now. For sponsored courses. Okay. That's the thing we can do a fast follow on. What's not you you know, let that be a blocker. Those users do want to Experian sponsor course, they can create an individual account that's not under enterprise Right? It would be just under a different organization. Yeah. So we will issue the access to the active team organizations. Mhmm. And all their users plus the old people who has an active individual subscription plus all new people. Either you will add them manually through the admin panel to the Teamwork. Or it will be the individuals. Who will go and sign in from the call through the axe. So the matter but it was just a question of how we should transition to the sponsored courses from the data perspective only. Yeah. That's a good that's a good call out. What you just said makes sense and yeah. For the enterprises, if we don't have the upsells and we don't have the capability for them to sign in, it might just have to be a follow-up afterwards.

### You (2026-03-16T14:07:04.752Z)

Yeah. I'll I'll I'll write up a ticket just so that we remember for our future. But it would it require anything special or specific, or it would just be time? That's that's the only thing right now.

### Guest (2026-03-16T14:07:18.231Z)

Time designs. Understanding on how exactly that should be working, What do we mean on the, you know, like, no working interface, the payroll saying that you should renew your subscription. There is no way to renew it through the Stripe. You should go to our support then they will sell you the new license, you know, So the flow right now is a bit complicated. And I probably don't think we should either think about including that to the sponsored courses.

### You (2026-03-16T14:07:53.702Z)

Okay.

### Guest (2026-03-16T14:07:55.101Z)

Yeah. K. Talking about the flow in general. Sean and I were discussing on Friday to, like, try and spot specific blockers. Obviously, right now with the with the, dual one access individuals being paused that creates a few complications and hopefully not too many. With the marketing page, obviously, we'll we'll probably not gonna release it we can't if we don't have the payment flows. So instead of the design marketing page that we have for individuals, The only thing that we probably we probably would need is update to the headshots because that was one of the things that that's still know, Caleb is still on top of that. On top of that page. And that's also the login We we most likely will need to like, create the one of the authorization with x will have to be supported on that one as well because right now, it just takes you to the buy now course. Or the organic for the organic sort of users to come across campus. The dot code to campus funnel would work as design for a sponsored course, which is have the x authorization creating those profiles for them. And then, yeah, just like as we discussed for enterprise users, if they have the act they have the active, subscription, the multi course dashboard, would show the sponsored course they're logged in. But if they're if they're ex enter enterprise contract has expired, They no longer can log in. What else are we not thinking about this? So the the thing is right now, we provision the access through the subscriptions. Right? So it means that once you're creating an account, we should provision you the subscription to get you if you don't if you didn't purchase anything. You just a new user, you sign in through the x, we create you an account, and we should give you subscription to the sponsored products. For some period of time we can limit it We have an option not to limit it. It depends. By default, if we're talking about the onetime purchase, just the yearly subscription. So it will give you the access for one year. If we can if we want to decrease that period of time specifically for the sponsored courses, that will be fine as well. But we just yeah. We just need to understand, like, for what period of time we will give the access to the sponsored courses if the person doesn't have anything else. Can it be indefinite? Or you need some specific point? We we we can we can see that the it's indefinite, you know, problems.

### You (2026-03-16T14:11:40.672Z)

Yeah. I I would think indefinite because again, going back to what we were talking about the enterprise or this is just supposed to be for everyone to access. Like, it

### Guest (2026-03-16T14:11:50.621Z)

Yeah.

### You (2026-03-16T14:11:51.912Z)

the the whole idea is to have Polymarket get more subscribers and users as well.

### Guest (2026-03-16T14:11:58.361Z)

Well, it would depend, like, in, you know, in a year. If we do it for a year, then we have to if we if we continue the partnership, then

### You (2026-03-16T14:12:02.702Z)

Oh, yeah.

### Guest (2026-03-16T14:12:06.201Z)

we'll have to stay on. So whether it's a year, whether it's indefinite, either would probably work. But feel like it's just if if we can if we can see you know, the different levels of access for, like, on the back end, like, you know, people who sign in through the free fun funnel, they get unlimited access to all the, like, free stuff. That's, I think, is a smart solution. As long as we can see that and then sort of act accordingly, in the forward events whether we have elect electives, free other free sponsored courses. I think it'd be easier to just not convoluted and, like, bring ourselves in a corner in the future. So just let's let's go with the indefinite access Okay. Gotcha. Talking about the marketing page. Do you guys did you guys pick with Mike during over the weekend? Anel. I didn't speak with Mike. In front of you,

### You (2026-03-16T14:13:22.792Z)

No.

### Guest (2026-03-16T14:13:26.331Z)

Why why was he bringing something up?

### You (2026-03-16T14:13:26.922Z)

Why? What's up?

### Guest (2026-03-16T14:13:33.851Z)

Do you remember that sometime before we we we had those consultants guys who was helping us to build the Stripe integration. Mhmm. So, Mike, came to me and asked, is there any way we can actually release that part in the old design but the new functionality and then move forward to the sponsored courses. So so how

### You (2026-03-16T14:14:08.892Z)

So he he was asking

### Guest (2026-03-16T14:14:11.461Z)

Stripe integration, basically, with with the link Yeah. The line? On the on the checkout session. So I believe there is a problem not on Mike Mike's end. Our accountants probably just pushing on him. To finalize the tax situation on the prod account because it was not it was not finalized yet. With with even with the release of of multi courses. So we already played around with our old implementation. We obviously need some time to finish it out because there was an outstanding questions with the consultants about the 100% promo codes. And a few other things. But it's kinda it's possible to release it even first as the first thing before the sponsored courses or in condition in conjunction with the sponsored courses. Yeah. So in that case we will be able to release the new marketing page but just for initial purchase. Of the two zero one. No upsells. Just initial purchase flow. So the Alex has already built it. That page already exists. The individuals. It's just the possibility for the new users to purchase the two zero one So sorry. Repeat one one more time. Which one which part would would we not have? The upsells? Yeah. So if we're releasing the new checkout flow, Yeah. It's just the replacement for the current flow. Where the card only is is acceptable. Yeah. So and can you say it again? I say anything. I'm sorry. I was a bit in interrupted. No. You're fine. Okay. So if we're planning to release the new checkout flow for the Stripe, replacing the old and existing one which is accepting only cards. The new one will last. Allow us to accept the even maybe the crypto the other stuffs, whatever. Rates, whatever we will configure. So if we will release it, we can release the new marketing page for and allowing our users to purchase the two zero one from the marketing page. But there won't be a possibility to upgrade inside of the application.

### You (2026-03-16T14:17:19.322Z)

Okay.

### Guest (2026-03-16T14:17:20.041Z)

So existing users will still see like, contact support to upgrades. Mhmm. But the new users will will be able to to purchase and that will be the minimal thing for us because the pay the marketing page already exists. Right? It was already built by Alex. We just did not release it. The checkout flow, yeah, we need some time to finish it up. Like, there is basically, like, three main thing. The checkout restoration mechanism, we need to finalize it. The 100% promo codes we need just to check it because we spend too much time with the consultants. Trying to figure out how we need to handle it. And I just don't remember how exactly we decided to handle it. Because it was a fucking long time ago. Mhmm. And the third moment we just need to make sure that it looks kinda kinda good. In the old design. So there it three main outstanding items on the new checkout flow. I mean, new new checkout flow is just the the thing on the checkout page itself. So would you go directly like, if you press purchase course, would it would it take you directly to the old design of the checkout? Page? Like, you wouldn't see this, would you? You wouldn't see this? No. Not at the moment. Okay. So you will go straight to the form where you need to enter your details and the payment method details. Mhmm. I'm just trying to think of The main problem is that we need a way to at least to have an option for people. Like, if they navigate the campus instead of, like, I don't know. Let's say you're a polymarket and what you're tangentially on one of the teams and they're like, alright. Let's let's see what they're you know, let's let's check our probably markets, people's understanding of prediction markets. So let's say, hey. Let's go to campus. They have it there. So they they come here and they're like, okay, how do I access it? They they try to log in. There's just two courses. Obviously, we're not gonna have Polymarket sponsor course on here, but they there's at least should be, like, a you know, option to authenticate with x this would have been the the path forward. It's sort of like a workaround. You press sign up. This is what and, what shows up, and then you have a skip for now to create a pre free profile, which gets will which would get you through This is probably a super small edge case to it's not like it's not really a blocker because we can live without this. Mean, it's just an idea. Yeah. Yeah. I Or we're we're missing, yeah, we're missing the thing regardless. Like, it's well, this this whether we release updated updated flows or the the marketing page it was still still missing that part. So this is the cube item. That would let us have this path So, I mean, if we have to update, like, if if our finance department is telling Mike that we need to release, you know, update the pay payment flows, the Stripe integration, then we obviously should do it. So and if we and if we can release two zero one together with it, like, not the two zero one marketing page at least, That would definitely be a win. Yeah. So let's see what what from where the wind is coming regarding the checkout flow. Is if it's coming from the finance side then I don't I don't suppose we do have any other option.

### You (2026-03-16T14:22:03.202Z)

Mhmm.

### Guest (2026-03-16T14:22:07.771Z)

So the minimum, what what we will do, we will just release the checkout flow We'll keep the the existing marketing page. With some little adjustments. But at least we can change and update the headshots if we need to. Right? And then we will move to the sponsored courses If something else will happen, I mean, like, we can either extend the the amount of work we we need to do, or we can decrease depends on fully depends on what's going on. And from where the wind is going. Yeah. K. And we still have a few things to figure out, but, at least think we can we're at least on the same page So that's good. Any other questions? Oh, not not mean, not a question, but this is the I've already sort of started the preparation for this idea of basically older UI with the new payment flow Like because the payment flow itself logically speaking, is almost done. Or even completely done. I've already described again, the parts of the updated UI, will raise it down. But still left the functionality for the new setup intact. And from what we saw together with the this sort of pre intermediate setup is not, like, minimal, but close to it, I would say. My question, I guess, would be is for, like, reprioritizing the the whole thing. Is there some sort of deadline for the the new prioritized feature, meaning for the sponsored courses. Nice to know, like, what's the the expectation there? I think I think if we got it out mid April, that would be fantastic. Yeah. That's about all right now. There's no specific date again. But when I told Matt that how how we how we discussed that two zero one individual access would be done by, like, mid April or whatever that that date that we were about. He said that he'd rather have sponsored courses by then. So don't know if that's a good good enough answer, but Well, it's because I I I'd say we'll, for sure, have it by this date. Maybe if, like, if everything goes okay even the portion of the self-service checkout would be there. Weird to have them sort of backwards, but if it is well, if it is more important for the longevity of the block and sponsorships, then so be it. Yes. We are on the crossroads now. So yeah, great that we've discussed it beforehand. Funnily enough, like, on our in our previous conversation, I was asking, like, maybe there is some sort of sponsorship. Maybe something should take priority, and lo and behold, it's there. Right. Yeah. It's just, like, this priority shift, like, on these things, like, week to week. Especially with, like, you know, new CEO coming in soon. So it's like, no no guarantees that they don't they won't shift shift again. It's just, like, you know, state of state of things. So I have to scramble and make the list of it. So Whatever the priority is, it will be done if push comes to shove. Like, everybody will just Cool. So that matters. Sense. Yeah. It it will be done. It's just sort of it's it's it's a it's a tiny bit tiring to see, like, the direction shifts. Week to week, like you said. Like, Yeah. As soon as we as soon as we agree on something, the direction changes. At least this didn't change. Yeah. It's it it at least it's always the case, I mean, that the changes are constant. This will never change. I don't know. Oh, the fact of the Yeah. Yeah. The fact that it of of a constant just never changes. Exactly.

### You (2026-03-16T14:27:12.152Z)

Yeah. The only constant is change.

### Guest (2026-03-16T14:27:14.731Z)

Oh my god. Okay. I am meeting by market on Wednesday, from, you know, the the campus slash dot co side for all the things that we have. Contractually agreed with them. So I was gonna fully confirm with them what they want the reward to be. For the like, any person who's finished the sponsored course, like, we currently have a basically, a finished design that that's why I said 99% finished I'm just need to find out which one that is. Elections. I don't understand. It was just here. I just was looking at it.

### You (2026-03-16T14:28:03.452Z)

Who say you wanna

### Guest (2026-03-16T14:28:05.801Z)

Other Right here. So after after you're done with the course, you basically would this is not the one that I'm just okay. Yeah. Don't think we'll finish this, but I was just gonna ask Serena to, like, I get the answer that this is fully a biomarker code, I'll ask Serena to update this and, like, have the biomarker code you know, be the reward essentially. Go ahead, Nikita. I already have too many questions. And just forgive me for that. So that page is it just for the sponsored courses? Or we should reuse the same one for the regular courses if it's applicable? You know, like, the socks

### You (2026-03-16T14:29:04.752Z)

The

### Guest (2026-03-16T14:29:06.571Z)

the success stated. I'm not sure we can do that. I'm just kinda throwing on the plates If we can, should we spend the time on it, or we just need to do it separately just for the sponsored courses? Like, their own success state. Have to take a look at what it what it looks like currently. You're saying to just reuse what we what we're currently doing for one zero one and two zero one? I mean, right now, I don't think we do have a success state Oh, I'm just not just not sure. I just don't remember. I'm not. I mean, like, I remember we have an option to show the certificate on the home page of the course. In the block. And specific block. That if you get it, you will see it's Yeah. Well, this is How do do we know how the certificates could look like? Because they're share buttons, but is are we reusing the same template that we already have for the regular certs? Yeah. I I don't Or it should be CAT cards, the square format that we use for the CryptoIQ, you know, like, something more cast than me. I don't I I I feel like I even show shown this to you because she has marked it as still, like, work in progress, and she just went on vacation. On Friday. So it still needs to be figured out, like, we don't even know if we're gonna have a share on x or share on LinkedIn. Like, all this stuff is not completely ironed out. What what what we had talked about that one of those requirements call requirement calls that we had for sponsored courses that this would be a pop up screen. Remember how you were saying that might be that might be actually simpler? While you're with on the multi course dashboard. If the the sponsored course would would come up, like, the whole module, like, this thing. Would come up as a as a pop up within your screen iframe. And you would just go through the video, go through the slides, go through all NIS interfaces, but it it's not all interface yet. Sorry. What? I mean, I'm just getting nice interfaces for the inside of the course. Yeah. I don't I don't really know what she took. This is this must have been the

### You (2026-03-16T14:32:14.642Z)

The

### Guest (2026-03-16T14:32:16.491Z)

screenshots that you provided her, Sean. Right?

### You (2026-03-16T14:32:18.192Z)

Yeah. That was the prototype.

### Guest (2026-03-16T14:32:19.801Z)

Yeah. She Anyway we should open the window, either the model or the full screen size to show the success states once you open it up the course. From there, you should be able to get your the promo codes, or something Right? Yeah.

### You (2026-03-16T14:32:50.912Z)

Yeah. That's the idea.

### Guest (2026-03-16T14:32:51.901Z)

I would I would love it if it was if something like this, like the rice the RISE format or whatever the course is called. It just shows up like this. It basically was something, you a menu, and you have all these steps that you have to do here to press on a bunch of cards. Take a bunch of questions, etcetera, etcetera. You press next, next, next, next, next, next, next. You finish everything. And on this window, that's a pop up You no. Before the success pop up, you will see the queries. You will be redirected to take a quiz. And only after the quiz, it's probably will be easier to do just the separate page or something. I mean, we'll we'll figure out that. K. Alright. Do we have that linked Oh, it's just the David's course is just still like a preview format. Right? Like, it's gonna have to be exported, but do we have that link in that epic, Sean?

### You (2026-03-16T14:33:58.542Z)

No. I will.

### Guest (2026-03-16T14:34:00.541Z)

Okay. And

### You (2026-03-16T14:34:01.722Z)

Repost it in the group, I'll do that.

### Guest (2026-03-16T14:34:02.271Z)

we'll we'll probably need to get those questions sorted too if there is any, like, there's any quick quiz pre or post, like, all those questions have to be in one place. Accessible on the ticket as well. Yeah. I will I will reach out. I think I think Josh had a accident over the weekend, so he's he hurt himself biking So he's out. Claudine is also out. Yeah. He's okay. Not I think maybe just a concussion or something. So we basically just have Serena now this week. So I'll ping her about this and maybe we can especially after Wednesday, we can have this post completion Well, completely finalized. Sorry about this. This is not a deal. For for initiative that we're embarking on. It's not I mean, like, that's kinda fine. We're still have a bit of the time. The question is, do do we understand that the quiz is just, like, the simple questions that you can retake to as many as you want. And we just need to decide what will be the amount of those questions Talking about post, please? Yeah. Yeah. The quiz that you will take after this the the course finish. Yeah. It it yeah. It will be you can take as many as many time as you want. I think it's five. Yeah. But, Sean, we have to double check what they what they have written down. Okay. What is your guys' design? Yeah. I think it's it's gonna be something like that. It's, like, five questions or so or I don't think it should be, a full test because that's defeats the purpose of of this whole thing. And it's just basically, like, you know, when you read an article or something and then ask you a few questions about it to make sure that you actually read it It's basically that sort of thing. Mhmm. And then you can take it over and over again. Anything else I'm not thinking of? Nothing you can build the implementation. Just one last thing to discuss and maybe questions, like, it felt weird, to be honest. Oh, after after your message on Friday when you said that Matt is frustrated with the lack of progress, what's what happened what we felt frustrated about was the lack of like, I guess, not the lack of the the the the constant switch in direction. Because it's not like we cannot move fast, but we need to have a goal to quickly move forward to. And for the past weeks, it felt like the direction was constantly changing. And so well, I don't know. I wasn't there when you had your conversation, but I was like, we were sort of felt like at blame and, oh, why the fuck did guys not finish this this whole thing? In the meanwhile, we're struggling with the release and additional changes there and later on, like, fixes, adjustments, etcetera, etcetera. It's like jumping here back and forth, like constant context switch, etcetera, etcetera. So if you don't mind, like, sort of rounding those corners and, like, forward into leadership that's doing we are perfectly capable and perfectly willing to do the next big prioritized thing as fast as possible. But but let it be, like, one thing for once, like, without like, jumping back and forth. And I know that you cannot guarantee it but the sort of drive at least in this direction. Because it, like, it honestly felt weird to be blamed And, again, I don't know if there was, like, a huge No. I don't know if there's if there was blaming. I don't know if it's a blame game. I think it's just, like, if anything, it's just more like, in a in a time of uncertainty, it's just, like, many things are happening. CEO gets replaced. All these plans that you had, are shifting, and it's just like, frustration adds on frustration. So it's just like that more than anything. And, like, it affects everybody. It affects Matt affects his job, affects his performance, and just trickles down to everybody. So it's like, I mean, that's where leadership comes in. Right? Like, if you need a leader at the very top who could, like, clear set clear goals and then everybody else can follow and behind them. But now it's just just sort of rural scrambling. So Oh, yeah. That's those. I think and I think yeah. And I think that's, like, part part of that's coming through. Through Matt as well. Like, the fact that we're campus is not doing well and and you know, these requirements and these expectations are shifting, and then we can deliver on these expectations. And then there's more frustration on that because of the fact that we can't deliver it. So it's just like the downward spiral. You know? So the sooner we can just, like, start on a clean slate, the better. And I hope that when the CEO comes, we can finally land on somewhere where we can at least feel like that's constant of change is broken. Well, those frustrations are I I mean, when I when I was on the call with him, I I mean, I definitely did my best in representing you guys and saying that, like, I mean, it's like I said before, we didn't have a PM for the longest time. And the requirements were, like, not fully fleshed out. And then our CEO gets replaced and then, you know, just, like, lack of stability. So yeah, it's, it's tough. I understand. Definitely not nice to to hear that, but It's okay. He he just doesn't care. He he, like, doesn't really about the two zero one. He he, I think, personally, doesn't really think think that two zero one individuals would sell. So it wasn't like, oh, fuck this. Like, we're not doing this. It was just more like, let's just pivot because our private market partnership is a lot more important and we don't have a strict deadline with them, but they are, every call we talk about, they just wanna hear progress. And I think if we had continued this, you know, continue on this path of, like, you know, we work on the multi course access for individuals, etcetera, etcetera. Then we'd have quite a few meetings with them where we wouldn't have any progress in sponsored courses, basically. So I think that's essentially the where where it all is stemming from. But we'll we'll get we'll get this out. Get it. Like, I I I can see by your face that you're frosty in yourself, and it's, like, like, Yeah. Like, not bitching, man. Like, it's okay. It's not the it's not the first audio. Like, give us a clear goal. It will be done. Let's break the cycle. Let's fill optimistic about it. Let's do everything in our power to circumvent it. It's just, like, I I was asking more so that, like, we're on the same page and they, like, direction is clear and the intentions everybody else are also clear. Like, that's that's why I'm moving to the moving to the single goal. Because, like, it's, like, even by your face, like, I can see that you are also frustrated. Yeah. I As Yeah. Wish in everybody else, I do presume. Yep. Yep. We'll just you know, we're doing the best we can. So that's that's all I can expect and promise. So Yes, sir. Likewise. Well, nothing else from me. Let's let's get it. Sweet. K. Ethanol's together. Questions? We'll have to meet again and definitely check-in on this. Because I don't feel like this is this is far from fully fleshed out. But we'll just build the plane as we fly it as we usually do.

### You (2026-03-16T14:43:28.652Z)

'Sup, Roma?

### Guest (2026-03-16T14:43:31.491Z)

Roma, go ahead. I have and, Krishna. So as you remember, I had the intention to implement to add email fields in in my team and my candidates pages. Could could we include that somehow But that's a question to both Nikita's Come on. Roman? Yeah. Roman? With all due respect, let's let's at least postpone this exactly. Like, keep it in mind. Let's postpone it. Like, as you can see clearly by the situation, we cannot promise anything because last week, we had one plan. Now we have another. Let's hope that this one will stay But for now, let's focus on the main goal, which would be this exact thing. Which is the the sponsored courses. Yes. Yes. Yes. What is the what is the severity? Like, of the email chain? Like, what is it just nice to have? Or No. I don't think so. It's nice to have I think it must be because so from from my perspective, it's very hard to to use hiring feature in general. If you don't see for which email you're sending. Invitation. You when you add sending invitation, you adding some name but that's name you should keep track of those names. Because you don't know who is who. In the end. Well, we can be we can be frank that nobody probably is using this application as a stand alone hiring system just yet. It's just not powerful yet. So I would I would guarantee 100% that people it's actually are actually hiring candidates and they use our system that they have an external system of sorts where they have all their, like, applicant pools because like, the applications that people get, like, the actual resumes and CVs and whatever, the it doesn't it doesn't come through Canvas. So those records have to exist elsewhere. And they somehow have to be uploaded to campus in the first place that, like, John Doe has johndoe@gmail.com. So I think it's not a, like, critical feature. I think I agree that it's definitely a a huge improvement, but we can yeah. Let's let's let's have it together with the two zero one stuff afterwards, as a follow-up. I think I think if if it was a make or break feature clients have already revolted about that. Yeah. But it just felt It's it's inconvenience. Yeah. It's it's inconvenient for sure. I know I know that, Nikki, the done, some progress there. If it takes, like, twenty minutes to do? Let's do that now. If not, yes, we can postpone that. Definitely. Yeah. That's that's more I thought for both Nikitas. If you will see that's it can work, like, it's very easy to implement. Let's let's think about that. Guys. Okay? Oh my If if it really takes twenty minutes, then it will be done. It probably won't. But the whole idea is even regarding this particular feature, but any sort of feature for the foreseeable future. What that was trying to say is that unless we have users who want to use Canvas and who want to use those features, nobody gives a shit about those conveniences. And once we have those, this will be at the forefront because there would be somebody to give a shit. Excuse my French. So for now, let's try to select one branch functionality, focus on it, and hopefully that this one will bring us more clients. That's what we should focus on. Rather than diverge. Excuse me if I'm too rude, but, like, No. This would be like, whole idea is to have a single focus. Okay. Okay. If that's like, better for for development Yeah. Okay. Let's do that. Alrighty. K. Thank you, gents. On onward and upward.

### You (2026-03-16T14:48:28.622Z)

Ed's new motto. I I love it. Alright. Thank you, guys. Really

### Guest (2026-03-16T14:48:34.531Z)

Have a good a good rest of your day. Thank you, guys. Thank you, guys. See you. Bye. Bye bye.

