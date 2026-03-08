---
granola_id: 61ab6263-960a-4e4d-a2db-e8c79ffb5407
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of case queue - transcript.
context: the-block
created: 2026-02-26
source: granola-sync
attendees:
  - kvallecillo@theblock.co
  - ldanowski@theblock.co
note: "[[mtg-2026-02-26-case-queue]]"
---

# Transcript for: Case Queue

## Attendees
- Karla Vallecillo (kvallecillo@theblock.co)
- Lil Danowski (ldanowski@theblock.co)

### Sean (2026-02-26T19:31:07.336Z)

Hey. What's up?

### Guest (2026-02-26T19:31:07.435Z)

Hello. Nothing much. What's going on?

### Sean (2026-02-26T19:31:12.096Z)

Nothing. Joining today's meeting to learn a little bit more about Salesforce.

### Guest (2026-02-26T19:31:16.665Z)

No.

### Sean (2026-02-26T19:31:18.626Z)

Think I'm gonna be taking over the campus situation over there, I guess.

### Guest (2026-02-26T19:31:25.015Z)

I don't even know what that means, but best of luck to you. Also, I was hoping to bother you because I'm trying to create a bot using Zapier so that it can track all of, so I'm subscribed to a bunch of newsletters from our competitors. And I've been manually tracking who's sponsoring their, newsletters. So I'm trying to create a bot to do that for me so I don't have to continue to, like, track it and it'll just update my spreadsheet. But I don't know. Instructions didn't mean to

### Sean (2026-02-26T19:32:05.156Z)

No. Trust me. I know exactly what you mean. There are so many things. Like, I I I'm running through, like, the ones that you know, I already said I'm trying to create, but the they keep on breaking. So I'm trying to get, like, really detailed and figure out the different more techy steps that you can incorporate into Zapier. So that they don't, like, run into any issues. Because a lot of the issues happen when it's, like, trying to communicate with other apps. I'll be in supposed to be you know, good at, but

### Guest (2026-02-26T19:32:35.705Z)

I thought that was the whole point. Hi, Lil. Hi. I'm sorry. I was, on with Vicky, and we are nerds and lost track of time in a spreadsheet. No problem. We're literally talking about spreadsheets too.

### Sean (2026-02-26T19:32:44.776Z)

Yeah.

### Guest (2026-02-26T19:32:47.725Z)

Great. Okay. Let me, like, change brain gears immensely and open different tabs. I have the case queue up if you want me to just share my screen. Yeah. I wanna I have that up. I just wanted to pull up my, like, how to. Which would have been wonderful if someone directed me towards it. Are you kidding me, Carla? Really? You You said this to me? I swear all I remember is Jeff and Cam being like, okay. Just look through just look through the cases that come up. Okay. This is an opportunity to reset. Wonderful. Okay. So let's back way back up just because Sean is brand brand new to the process. Okay. Anytime somebody emails support@Theblock.co, we have an automation in Salesforce that creates a case. Like a totally different different object in Salesforce. It tries to recognize who the person is sent the case. And if there's an existing leader contact in Salesforce, it'll be like, Lil at Theblock is having trouble, and it'll affiliate that support case with either my person record or my company record. But a lot of times, they're, like, super random email addresses that aren't in our database, and it'll just create like, using a blank person record. So we have a real time I should not pull up my Slack Give me two seconds. Real time alert of all of the cases as they come in in the Salesforce alerts channel. And this is just, like, it's just what it is. Anytime somebody sends an email there, it's a notification of what the subject line is. It gives you a link directly to that case in Salesforce. And we've had a ton of different ways of handling support cases in the past. Just based on, like, what the majority of the topics were. Okay. So from here, some there could be a decision to, like, use this as a real time alert and manage things instantly. You could also come to the case queue in Salesforce and just, like, look at the full list. You're not dealing with them in a real time way. And the idea here is that there should never be any cases in the queue. They should all be assigned out to people, and then different people should be working on them, and they should be closed out after we're done addressing their problem or you know, whatever the case may be. So this list view is all current open cases. We have a ton that are from, like, September. What I notice every once in a while is I'll go in here and the list is, like, a 100 long. And all of them the majority of them are, like, not sales related. So this is all to say that at one point, Cam was managing the entire thing because the majority of the cases were, like, pro customers reaching out about their account or a login issue or, like, it was generally more sales y. And now that we've moved away from surfacing that email to any pro customers within the portal, it's become largely more a lot of spam. But a lot a lot of also just general, like, CloudFare issues and, like, people not being able to sign in to theblock.co or, like, just issues that are outside of what we felt like Cam should be using his time to address. So at some point in the last couple of months, I don't remember when, we told Cam he can step totally off of this. And Carla would triage if it was sales related. So if somebody's reaching out and she sees the, you know, subject line that's like, I want to publish a press release, We're like, go ahead and grab that as if it's an inbound lead, and you can you know, grab the case and assign it out to the team as as needed. Mike offered to jump in on anything that was, like, tech support ish. And then he was gonna kind of route between I'm gonna also ask you this. Does he like to go by Ram? I've heard people call him

### Sean (2026-02-26T19:37:10.416Z)

Oh, really?

### Guest (2026-02-26T19:37:11.465Z)

and I'm like, I don't I don't wanna just say that if it's not true.

### Sean (2026-02-26T19:37:12.586Z)

Yeah. I mean, that would be the first time that that I've never heard that before. Usually, it's rumble. Who who's called them Ram?

### Guest (2026-02-26T19:37:19.645Z)

Like, price?

### Sean (2026-02-26T19:37:20.826Z)

No. No. Rommel.

### Guest (2026-02-26T19:37:23.125Z)

No. Ramald. And I and I usually say his full name, but then I, like, trying to think of who said Ram a couple times, and I was like, oh, that's, like, a fun nickname, but also

### Sean (2026-02-26T19:37:31.986Z)

Yep.

### Guest (2026-02-26T19:37:32.815Z)

anyway, he got looped into it once Mike was basically like, oh, I will triage. And we're like, you probably don't, like, have time for so much of this stuff, and it was getting assigned out anyway to somebody on his team. So I think now Matt has voluntold you, Sean, to handle all campus, you know, inquiries. And we also just removed a lot of people from Salesforce. So it's kinda like, I don't even think Mike Price has a license anymore. So we just have to reestablish the responsibilities of what person is gonna handle what topic based on who still actually has a Salesforce license.

### Sean (2026-02-26T19:38:12.026Z)

Okay.

### Guest (2026-02-26T19:38:13.925Z)

This

### Sean (2026-02-26T19:38:14.326Z)

Understood.

### Guest (2026-02-26T19:38:15.665Z)

has been the most enlightening conversation I've had in a long time, Lil, because I was told to do this, first of all, all open cases was not where I was told to go. They were like, just go to the case queue one that actually says case queue, and those are the ones that you need to close out. So those are the ones that I've been paying attention to. I haven't gone into all at all. So I'm like, my name is on there. And it says open. And yeah. So Okay. So now yeah. No. Anything Salesforce, just make sure I'm in the conversation. The reason I will tell you the reason somebody thought this Case queue literally means that it's owned by the queue still and has not been assigned out to a person yet. So it's like a new where somebody hasn't looked at this and been like, this is Sean's. This is Carla's. So the idea of a queue is that there's never anything here because they're getting farced out. Okay. From here, if you go to the all open cases list, you can see who they were assigned out to and what the status is. So I can see that I gave this to Mike, and it's still, you know, sitting here, basically. And so there's a couple here. The same four that we just saw in the case queue are still owned by that queue owner, but neither here nor there. Okay. So I think twofold of what we need to do. One is just make a call as a team that we're gonna close out, like, everything that's super sale and old because at this point, unless it's really important, Yeah. These are so old that unless the person has, like, like, if they haven't reraised their hand, then

### Sean (2026-02-26T19:39:54.066Z)

Mhmm.

### Guest (2026-02-26T19:39:56.385Z)

we're probably not gonna address it. I did do that with a bunch of, like, spam cases, but there were some that looked more legit that I left. So those are the ones that are still in people's names. But, again, like, Carla, like, if you've gotten, like, these two, and it's from September. Somebody asking for a sponsored post. Like, you can reach back out if you want to, but it's probably Yeah. Okay. So my proposed flow to handle this is instead of one person owning the entire queue and the assignment, is that everybody is just given a topic area, and everyone is monitoring the Slack channel.

### Sean (2026-02-26T19:40:42.126Z)

Okay.

### Guest (2026-02-26T19:40:44.875Z)

Okay. So it's not the volume is not crazy. If it was, like, a 100 a day, the would not be my suggestion. If it's one three a week, I think we can all handle this. Pretend this one just came in. You look at the topic. You're like, Carla, this is obviously not sales. You don't need to touch You just totally ignore it. Okay. Sean, you look at this and you're like, this is not campus. I can totally ignore this. Ramald is going to look at this and be like, this is mine, and I'm gonna need to give him this I should record this. I'll kinda, like, redo the the how to to make sure he knows this as well. But what he should do so what you guys should do as well, if there's a topic that you want to grab, you can click directly into the case from the Slack message. So pretend we're opening this one. And then you put it in your name. So very first step, take it out of the case queue ownership and put it in your name so that we all as a group know somebody saw this, and they are going to action it.

### Sean (2026-02-26T19:41:46.066Z)

Cool.

### Guest (2026-02-26T19:41:47.235Z)

Step two is reply to the person. Right? So read their email, You can Slack on the side if you need to figure out the issue. And you can email the person back from directly in the case. The issue that I have found here is that our support email really frequently lands in people's spam boxes. So tons of replies from here, people think they don't get, and then I'll see, like, three more support cases come in in the following week being like nobody's gotten back to me. And I checked and we did, but nobody, like, added their own personal email address.

### Sean (2026-02-26T19:42:22.896Z)

Mhmm.

### Guest (2026-02-26T19:42:24.005Z)

To bump up the security or whatever. And it's just that support email that's getting blocked by people's inboxes. So if you want to, you can, like, copy yourself in on the reply And that way, you're taking the conversation out of the case queue, basically, and into your own inbox, and you're replying from there. And that just ensures that the person's gonna actually see the email.

### Sean (2026-02-26T19:42:47.056Z)

Cool. Yep.

### Guest (2026-02-26T19:42:49.675Z)

So pretend that I wrote the email, blah blah blah, click send. The next thing is to change the status. Kinda like an opportunity, Carla. Like, you're just pushing things along as you get down further in the sales process. To the appropriate status. So we're either waiting on them, they're waiting on us, or it's closed out. If you solve their problem and you close it out, there's a resolution reason And just it don't care too much about this. If we had, like, a support team and we were tracking this in more detail, I would care. But the issue fixed is fine. If it's spam, it's spam. Don't go too crazy, like, figuring out the right value here. So most important is, like, put it in your name, reply to the person, change the status, and then close it out.

### Sean (2026-02-26T19:43:38.086Z)

Cool.

### Guest (2026-02-26T19:43:38.705Z)

And that's really it. Okay. K. Let me look at my how to and see if that is what I said really quick. Okay. Real time email. Slack. We see some little and they haven't been answered to, so, like, say, for example, the two from today, Mhmm. The embed code not working, should we put it in in the correct person's name? And if so, who who's the correct person Like, in this example Yeah. So that's where I wanna, in reestablishing who owns what, you are gonna be sales and sales only. If somebody's asking for a sponsored post or, like, that data thing that somebody asked for, like, downloaded They asked the other day. Sean will be campus, and maybe Ramon will be literally everything else.

### Sean (2026-02-26T19:44:34.186Z)

Mhmm.

### Guest (2026-02-26T19:44:34.565Z)

Just like general tech support type stuff. What he should have done here like, what he did is just reply to the Slack And he's like, I'm looking into this. And what he should have done is put the case in his name, replied to the person to say, we're looking into this. Like, right now, that's

### Sean (2026-02-26T19:44:50.716Z)

Yeah.

### Guest (2026-02-26T19:44:52.255Z)

person has no idea that anything's happening. Mhmm. And me as a, you know, manager or whatever looks in here, and I'm like, nothing's happening. So I will remind him to do that, and you guys can do the same. You just grab the case and put it in your name. I don't think your job should be cleaning up after other people's old cases. Like, you're you're in charge of your own cases.

### Sean (2026-02-26T19:45:15.206Z)

Cool. Makes sense.

### Guest (2026-02-26T19:45:17.585Z)

Okay.

### Sean (2026-02-26T19:45:18.706Z)

Can you add me to that Slack channel, the security Thank you. Oh, Slack alerts or Salesforce alerts?

### Guest (2026-02-26T19:45:22.855Z)

Yes. Yeah. I need to change the name of that because it makes no sense. It used to be, like, a consolidated general Salesforce alert. Channel and when Sasha set it up back in the day. Okay. You're added to the channel. For your personal, like, organization of the cases, you could just come back to the all open cases view and just find the ones that are in your name. So, like, that campus one that came in the other day, Sean, I already put in your name. Or you can just look at the my open cases view if you wanna filter that and see only the cases that are open in your name.

### Sean (2026-02-26T19:46:09.196Z)

Okay.

### Guest (2026-02-26T19:46:09.685Z)

However you wanna do it. I doubt that it's gonna be so crazy that you need to, like, parse out between the two because the idea is not to ever let it get this crazy.

### Sean (2026-02-26T19:46:15.536Z)

Okay.

### Guest (2026-02-26T19:46:18.865Z)

Yeah. And, yeah, Carla, I like, I would not what I have seen you doing in the past is, like, assigning the actual case to Cam and and then saying that it was sent to sales. Like, we wanna keep the reps totally out of the case object. And so you can reply to the person and loop Cam into the actual email, but then close your case. Okay. As sent to sales. Okay. Yeah. And that way, it's, like, out of here, and it's just now on cam to reply to the person out of this in his inbox. Okay. Because I don't think the rest of the team other than Cam has any idea what this queue even is because he's the only one who's ever been in, like, a support capacity before. So it would like, if you assign one to Kogo, for example, or, like, Fred, they'd have no idea what this even is. Okay. No. Okay. That's basically it. Yeah.

### Sean (2026-02-26T19:47:22.006Z)

Alright. Well, I just have

### Guest (2026-02-26T19:47:22.885Z)

Yeah.

### Sean (2026-02-26T19:47:24.326Z)

two questions. One, is do I have to use the authenticator every single time I log in? Or is that is there is there a way to bypass that?

### Guest (2026-02-26T19:47:32.725Z)

You should not have to as long as you're like, I don't have to use my authentication for Salesforce. Have you bookmarked this as the custom domain domain? Let me put it in the chat.

### Sean (2026-02-26T19:47:42.956Z)

Yeah. Right.

### Guest (2026-02-26T19:47:47.415Z)

It's like, show me what happens when you well, I guess you already in, so it'll probably bypass it. But it should just let you get in via SSL. And not a multistep.

### Sean (2026-02-26T19:48:03.976Z)

Oh, I see why. Yep. I know why. At the back, every single time I would log in using my

### Guest (2026-02-26T19:48:10.035Z)

No. No. No. Yeah.

### Sean (2026-02-26T19:48:11.656Z)

username and password, but at the bottom, log in with

### Guest (2026-02-26T19:48:14.695Z)

Yeah. Yeah. It's new custom domain. I would just bookmark that

### Sean (2026-02-26T19:48:14.726Z)

okay.

### Guest (2026-02-26T19:48:18.585Z)

link that I put in here, in via that, not salesforce.com, it'll automatically send you to the SSO page.

### Sean (2026-02-26T19:48:24.056Z)

Perfect. Thank you. And the second second thing I wanted to bring up, you deleted that account that I was messing around with. Right? To test?

### Guest (2026-02-26T19:48:32.225Z)

Yes.

### Sean (2026-02-26T19:48:32.896Z)

So

### Guest (2026-02-26T19:48:33.195Z)

The opportunity, but not the count. I can make another opportunity for you.

### Sean (2026-02-26T19:48:35.026Z)

I okay. Yeah. I could I can make it myself.

### Guest (2026-02-26T19:48:38.595Z)

Okay.

### Sean (2026-02-26T19:48:39.546Z)

But either way, I'm going to be testing again. So I'm hoping I don't need to actually you know, mess around in Salesforce. But if I do, just giving you a heads up, I might you know crush it again mid

### Guest (2026-02-26T19:48:51.055Z)

That's fine.

### Sean (2026-02-26T19:48:53.026Z)

mid March. Who knows?

### Guest (2026-02-26T19:48:53.885Z)

Just make it, like, $4,000,000 instead of a 120 k. Gina's gonna be like, what

### Sean (2026-02-26T19:49:00.226Z)

The next call

### Guest (2026-02-26T19:49:00.775Z)

It was so

### Sean (2026-02-26T19:49:01.526Z)

the next all hands, I'm really trying to

### Guest (2026-02-26T19:49:01.845Z)

I don't know. I know. I don't realize, like, who doesn't know everybody else. And I was like, like, she truly thought that it was just, a bot name. Like, she had no idea who these were. Like, who is this, like, Sean's Winslow selling? It's like, oh my god. Anyway, Okay. Yeah. If you guys have suggestions as you start doing this too, like, we can change the process. I feel like the people who are included on this just are constantly changing. So if we had one owner of it, there'd be a very a very different way to handle it handle it.

### Sean (2026-02-26T19:49:37.066Z)

Yeah. No. It's cool. That works for me.

### Guest (2026-02-26T19:49:38.685Z)

Sweet.

### Sean (2026-02-26T19:49:39.206Z)

I'll be I'll keep tab.

### Guest (2026-02-26T19:49:40.765Z)

Okay. Another thing, sorry, for Sean real quick. Is I'm trying to get rid of all of the different email addresses that live across all of our different websites that, like, nobody's even on the list service anymore, Similar to people emailing support, we have lot of things forwarding to sales@theblock.co. We have, like, sales@theblock.pro and ops@theblock.co and just all these different things for different reasons. And one of them was campus@theblock.co, And I I swear I looped you into an email recently where it was more of a support thing.

### Sean (2026-02-26T19:50:19.586Z)

One that Matt recently replied to.

### Guest (2026-02-26T19:50:20.985Z)

Was it did he just reply to you? Okay. Yeah. Let me see. My oh, yeah.

### Sean (2026-02-26T19:50:27.376Z)

The guy Yeah.

### Guest (2026-02-26T19:50:28.455Z)

Yeah. Yeah. Yeah. Okay. So those should stop because I'm trying to get that email address, like, just removed from the site so that everything comes through support. Because I think it would be more efficient that everything is logged in the same support queue versus us having, these

### Sean (2026-02-26T19:50:44.196Z)

Yeah.

### Guest (2026-02-26T19:50:45.155Z)

stand alone emails for everything. Because as people are, like, coming and going, nobody's cleaning up the members of the listservs. And then things get lost.

### Sean (2026-02-26T19:50:55.016Z)

Yeah. Now that great.

### Guest (2026-02-26T19:50:59.855Z)

Alright. Sweet. I'll tell I'll update that doc and just, like, write the high level ownership. But that's it.

### Sean (2026-02-26T19:51:10.156Z)

Cool. That works for you.

### Guest (2026-02-26T19:51:10.705Z)

Fantastic. Okay. Thank you.

### Sean (2026-02-26T19:51:11.956Z)

Thank you.

### Guest (2026-02-26T19:51:13.555Z)

No problem.

### Sean (2026-02-26T19:51:14.166Z)

Bye, guys.

### Guest (2026-02-26T19:51:14.535Z)

Yep.

