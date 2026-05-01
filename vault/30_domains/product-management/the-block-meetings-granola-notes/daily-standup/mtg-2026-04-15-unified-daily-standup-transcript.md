---
granola_id: 9494d0e7-8e43-4b23-b41e-c464e751551c
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of unified daily standup - transcript.
context: the-block
created: 2026-04-15
source: granola-sync
attendees:
  - bmendoza@theblock.co
  - mprice@theblock.co
  - npivcevic@theblock.co
  - mvitebsky@theblock.co
  - erupkus@theblock.co
  - mhulis@theblock.co
  - cdaumur@theblock.co
  - vention-team
  - cpaz@theblock.co
  - abenitez@theblock.co
  - norobenko@theblock.co
  - mzhynko@theblock.co
  - mlozuk@theblock.co
  - kbaspinar@theblock.co
  - bvadimovich@theblock.co
  - ysmagulov@theblock.co
  - akryvanosau@theblock.co
  - sho@theblock.co
  - koliva@theblock.co
  - ramuald.vishneuski@ventionteams.com
note: "[[30_domains/product-management/the-block-meetings-granola-notes/Unified Daily Standup.md]]"
---

# Transcript for: Unified Daily Standup

## Attendees
- Ben Mendoza (bmendoza@theblock.co)
- Mike Price (mprice@theblock.co)
- Nikita Pivcevic (npivcevic@theblock.co)
- Matt Vitebsky (mvitebsky@theblock.co)
- Ed Rupkus (erupkus@theblock.co)
- Maria Hulis (mhulis@theblock.co)
- Claudine Daumur (cdaumur@theblock.co)
- Cesar Paz (cpaz@theblock.co)
- Anna Benitez (abenitez@theblock.co)
- Nika Orobenko (norobenko@theblock.co)
- Marina Zhynko (mzhynko@theblock.co)
- Marina Lozuk (mlozuk@theblock.co)
- Koray Baspinar (kbaspinar@theblock.co)
- Bogdan Vadimovich (bvadimovich@theblock.co)
- Yermek Smagulov (ysmagulov@theblock.co)
- Akira Kryvanosau (akryvanosau@theblock.co)
- Serena Ho (sho@theblock.co)
- K. Oliva (koliva@theblock.co)
- Ramuald Vishneuski (ramuald.vishneuski@ventionteams.com)

### Sean (2026-04-15T14:02:32.887Z)

At the Nikitas with the merged audio, I dig it. All right. Go ahead and get started. Go ahead and start with Alex.

### Guest (2026-04-15T14:02:44.429Z)

Hello. Well, I've been finalizing the swiper for the homepage view. There is some weird bug with the odd amount of tiles. It works correctly, but with even amount of tiles, it doesn't work. Visually. So currently looking to that.

### Sean (2026-04-15T14:03:04.567Z)

Okay. All right. What did you say the automotive tells.

### Guest (2026-04-15T14:03:12.669Z)

Well, on the homepage, on the desktop, we display four jobs on tablet three and on mobile one. So for odd numbers, the. Networks correctly, but on the desktop view, the swiper doesn't look good for some reason.

### Sean (2026-04-15T14:03:27.527Z)

Okay. Okay. Gotcha. Understood.

### Guest (2026-04-15T14:03:28.509Z)

So we're back.

### Sean (2026-04-15T14:03:30.487Z)

Okay. All right. Yeah. Thank you. Keep us posted. Anna.

### Guest (2026-04-15T14:03:36.189Z)

I want. Maria. I want everybody to, like, just. At least elect somebody. To pick up your work. If you haven't already, just so that if you're not done, you can continue and get it shipped. Okay. I think I should maybe send all my tickets to Sean already, and then they can redirect it to other devs.

### Sean (2026-04-15T14:04:06.327Z)

That's what I was going to say. Thank you, Alex.

### Guest (2026-04-15T14:04:10.589Z)

Okay. We'll do.

### Sean (2026-04-15T14:04:12.167Z)

Cool. Yeah. And just feel free to just keep me posted on your whole life. You know?

### Guest (2026-04-15T14:04:19.149Z)

Okay. Yeah. Alex, feel free to sign all the job tickets to me because I'm currently working on this. So.

### Sean (2026-04-15T14:04:29.687Z)

Awesome. Thank you, Michael. A. Anna.

### Guest (2026-04-15T14:04:38.749Z)

I closed a lot of tickets for election hubs yesterday. There is just one doubt for the landing page. And also there was a ticket worked on or priced signals. I added some comments in there. And the ticket you mentioned, Alex, for previous is looking good. I added a comment for Yarmik to look at. And, yeah, we'll be waiting on that part. About the ticket for adding the llm is file for that code that is really to deploy and I will continue with the data tickets framework. And that's all from my. City.

### Sean (2026-04-15T14:05:29.047Z)

Anna.

### Guest (2026-04-15T14:05:30.749Z)

Thank you. Yes. Hello there. So essentially the ticket that Anna mentioned about indicators. I already have a fix. I just send it to Nikola for, like, kind of just make sure that it's fine. And what is once he, like, approves it, I will, like, I'll let Anna know. Also, there was, like, a ticket. It's a bit somewhere below for, like, bug. Yeah. Category pages pagination issues. Turn out. Well, it's not really a bug. I mean, relatively it's AWS limitation that it, like, limits to 10, 000. Yeah. Essentially, we cannot have, like, with our current implementation, which is like 10, 10 articles per page, we simply cannot have more than 909. Working pages. And this is like. Yeah, like cloud search limitation. And sucks a bit. But we guess we, I kind of agreed on why one way of solving it. Yeah. Also got, like, a few comments on some other tickets, like, for example, for invalid URL. And. Yeah, that's, that's pretty much it. I will quickly fix that. And, yeah, that's it. Oh, nico just texted me that he approved it. So I will update the dev box and. Yeah.

### Sean (2026-04-15T14:07:25.687Z)

Perfect. All right, cool.

### Guest (2026-04-15T14:07:27.629Z)

Yeah, that's, that's pretty much it.

### Sean (2026-04-15T14:07:29.847Z)

That's it. Okay. Thank you, Bod. Han. Brian.

### Guest (2026-04-15T14:07:36.989Z)

Cool. I was working with a consultant, Alex, on the pre bid stuff and some of these weird ad issues. I think I got it mostly figured out. I will put Santa box before I leave because it should be tested. We basically had, like, European rules applying to everything. So European privacy laws applying to Americans and a bunch of other things. And it was, like, confusing pre bid. It's. It's a lot. It's like a rabbit hole, but hopefully the dump box works well. And what else? And I was also looking at the data dashboard dev box as well, making sure that's good. And I will try to coordinate with the people leaving today to see what tickets I should pick up when I'm back. And. Yeah.

### Sean (2026-04-15T14:08:22.407Z)

Perfect. Thank you, Brian. And enjoy your vacation. Or you're going on vacation for the week. Nice.

### Guest (2026-04-15T14:08:30.109Z)

Just a week. End.

### Sean (2026-04-15T14:08:31.127Z)

Hell yeah. Enjoy, dude.

### Guest (2026-04-15T14:08:33.389Z)

Thanks.

### Sean (2026-04-15T14:08:35.687Z)

Caesar.

### Guest (2026-04-15T14:08:40.189Z)

Well, last week on Friday, I finished the first step for, for atlantis. Now it's working fine. I did some test. I executed until Atlantis plan and Atlanta supply in one repo. Yeah. It's acting as terraform cloud. So I have to do something similar for red boxes as the second step. In addition this morning, because yesterday I'm only I was on, I was off. Basically, I was taking message, solving some issues and, and trying to, to do all things that people need. So keep working on that right now. When I finish all these things, I'm going to, to continue with my task. And. Yeah, and that's all.

### Sean (2026-04-15T14:09:36.647Z)

Perfect. Thank you, Caesar.

### Guest (2026-04-15T14:09:38.509Z)

Thank you. I started to prepare a post core update report. I'm checking the data. I'm planning to present tomorrow. And also the yesterday's tasks are still same price page, FAQs, learn page content improvements, data pages, meta title changes. And also additionally, I started to prepare a plan to increase organic traffic of ratings pages to improve content or any technical. I will review it, audit it and prepare a plan for that as well. Yeah, that's it.

### Sean (2026-04-15T14:10:28.887Z)

Nice. Thank you. Thank you, Corey. Kristoff.

### Guest (2026-04-15T14:10:37.309Z)

I guess I've been working on a couple of things with all over the place. There's one thing I need to talk about is the ad stocks asset per sticket. Like, I put it in the review because I'm not sure if it's done or if there needs to be some change about it. Like, I think Nicole put a question mark to it. And I'm not sure if it's, if it's all right like this, or we should change, change the wording. That's, that's the main thing that's on my mind. And then I have some things to polish up at github, but nicola told me to, to do a up order. But it's, it's, if you scroll down. There is the comment. Yeah, in the comments section, like down. Yeah. Like. Nicole texted it is already done, but, I mean, maybe we can change the wording from tokens, ETF stocks to assets mentioned this article. I don't know if should be assets or if we can keep it at tokens ETFs stocks. Yeah. Asset would make sense. Okay, so I'll just change the warning and that's it. Yeah. All right. Okay. So, so we already have the logic in there where Adam needs to get in the parentheses. It would show on the, like, already access in the comment section, but I just refreshed my memory. You. Okay? Does it, does it show up in the body paragraph? Brian, do you work on this? Right. I think if you scroll down, I think, like, I have a screenshot of, like, it working. In the comment section. Yeah. See, like up in scroll up. See, like this is like the test of, like. So. Oh, yeah, yeah. So. And, yeah, Ed mentions, like, it's still, like, shows the pill in article as well as at the bottom of the article. Nice. Yeah. So let's just change it to assets and then we can close the ticket. Okay. Okay. Thanks, Kristo. Yeah. I guess so. Yeah.

### Sean (2026-04-15T14:12:49.047Z)

Okay. Yeah, let us know if you have any more questions. Maria.

### Guest (2026-04-15T14:13:06.829Z)

Press from my side. I did fix for board car cards filters. On reports cards page and fixed comments from Alex to PR. About iOS app partners. That's it.

### Sean (2026-04-15T14:13:26.567Z)

Thank you, Maria.

### Guest (2026-04-15T14:13:33.549Z)

Hello, Ms. Famiya today. I finally ask quiz brand safety program. And brand review with it. So that's it.

### Sean (2026-04-15T14:13:45.927Z)

Thank you. Mike.

### Guest (2026-04-15T14:13:54.349Z)

Yesterday shipped a huge PR for the iOS off. And that part of the integration. Today. I've had quite a bit of work from Matt to merge in that a lot of updates for the iOS app to Virginia with the off portion. I've been working with. So I'm merging that in and getting that all. Settled, and then we'll test that out. It's kind of the last major push before we go live with the app. So, yeah, just getting that all together and making sure it all works right. Main focus today.

### Sean (2026-04-15T14:14:32.807Z)

Nice. Thank you, Michael. How was the leadership meeting yesterday?

### Guest (2026-04-15T14:14:37.389Z)

Oh, it was good. That was good. It was informative. And, you know, people did pretty well in their OKRs.

### Sean (2026-04-15T14:14:38.887Z)

Yeah.

### Guest (2026-04-15T14:14:44.589Z)

And Steve. I think I mentioned it in the retro with steve joining us, start of May. Yeah. Skin, we're all skin ready for that. And we'll have our official OKR meeting tomorrow. We go over everything.

### Sean (2026-04-15T14:15:03.207Z)

Awesome. Thank you, Mike. The Kira kulis.

### Guest (2026-04-15T14:15:10.749Z)

Short and sweet update working together with nickel. I announced last quirks. The whole flow, what looks like it's working. Been able to go through tests, etc, etc. Just minor fixes here and there, mainly for redirect since the course, since the new course only has like one subject and there are like more. Edge cases here and there. Otherwise working further to support the release. And that's all.

### Sean (2026-04-15T14:15:42.247Z)

Thank you. Yeah, have you guys. Like, everything's been good with David? Has he been. Answering?

### Guest (2026-04-15T14:15:55.949Z)

Yeah, we actually think would give it a lot. So I'm on the last steps of making that course work locally.

### Sean (2026-04-15T14:15:59.447Z)

Go?

### Guest (2026-04-15T14:16:08.029Z)

Figuring out some stuff with the reward page. But the course is working, the progress tracking is finally working. The course was imported, so the spreadsheet is mostly finalized, at least for the dev box. But only the slightest adjust will need it for the Pratt airport. So going through the whole flow and testing out locally before passing through the QA. Just to make sure that everything is working. And just in case, David made such a freaking cool mini game at the end of the course. It's just something that we never saw before. So that will be just as ripping. Part of the whole course. Well, that's cool and well put up. When do you think we'll have it on QA? I just wanted to know. He wanted to get an eye, an eye on it real quick. I think. Probably tomorrow or something like that. Give me a note. Okay. Send a link to Matt so we can see it. I also, we also told poly market that they need to answer us by Friday or else the release will get delayed. So if you don't get an answer by. You know, today, tomorrow. We will have more time to shift this. So which will be a perfect news. I suppose. Yep. They're slammed to the, to themselves as well. So. Be posted.

### Sean (2026-04-15T14:18:03.687Z)

Nice. Thank you, Nikita. Also, how did you just describe David's mini game?

### Guest (2026-04-15T14:18:11.149Z)

Ass ripping.

### Sean (2026-04-15T14:18:12.007Z)

I thought so.

### Guest (2026-04-15T14:18:14.989Z)

It's, it was inspired by the papers, please. So it has, like, the cool audio effects, like the animations. Like, it's a game that we can just cut from the campus and just sell it out.

### Sean (2026-04-15T14:18:19.447Z)

Yeah.

### Guest (2026-04-15T14:18:32.109Z)

I think.

### Sean (2026-04-15T14:18:33.287Z)

You're not wrong. I was playing it. And it's very fun.

### Guest (2026-04-15T14:18:35.469Z)

I mean, like, we have the stripe integration ready, so not sure what I was waiting for. We just need the slide design adjustments for them in the game or either the campus. But, I mean, like, I was not able to pass it because I asked him, like, how can I skip it? Because I'm too. I'm too bad as a Trader. I just lost all of all of the money it gave me. But did you take the course, though? Did you take the sponsor course? I took the course as a developer, so I just clicked it through. Did not take the course. Exactly. Yeah. Technically, I think it's supposed to test your understanding of the content because I took it. And I took me three tries, but I did it, and I was like, okay, okay. Yeah, but the minigame is optional because you, you may take as many tries as you want, but the, the final part is always the, the checkpoint. Yeah. Well, the, the game is very much tied to the actual course. So that's like, that's why it fits, I think. Well, and it's challenging enough for sure. Yep.

### Sean (2026-04-15T14:19:47.047Z)

Thank you, Nikita. Nichola.

### Guest (2026-04-15T14:19:53.389Z)

Hello, everyone. So today I spent a lot of time reviewing various PRS, spent time with also bogdan to line on the ticket for the AI integration for meta descriptions, and then we realized that chat GPT API doesn't work. And, yeah, I need to try that out with hopefully, like, fixed it. We tried a fix, actually, during darn thing, but I need to retry it. It didn't work immediately. So maybe take some time. Also, yeah, I need to still agreed with that to export all the charts for Corey. And then, yeah, we'll kind of help, help him. Deliver those updates for the Matta meta changes. And. Yeah. And also, like, Ed asked me to investigate, I guess, before Friday, the update for to see if singulars, like, had there was, like, a video that showcased how to export data from Google spreadsheets. So I'll need to take a look at that as well. And, yeah, kind of focusing on logs of integration. Yeah, that's, that's number one on my priority list. Now. Yeah. Just so you know, Josh might reach out to because today we had a media call, and he's, like, working in singular, basically. You know, the whole day. So I told him about the sort of issues with, like, spacing and the ticker, because I think ticker is going to be, like, the biggest problem for us. If it can call it a problem. And he might reach out to you to, like, actually so you can describe the. The. Ideas or the sounds good things you're running into with that. Yeah. It's nice to have, like, again, meetings with Josh. Like, we, I used to see him, like, all the time. And now, like, for the last, like, six months or a year, like, I see him so rarely. Yeah, he has. He has let his chickens do a lot of the work, and he was more managing, but now he's back into the weeds, I think, Too. That's. I don't know. Is that good or bad? I don't. Sure. I think. I think he wants to. I think he wants to provide designs and, like, do actual explorations. So there's the work you have to do and the work you. And the work that. What? Mike, I said, there's the work that you have to do, and there's work that you enjoy. Getting in the weeds. And doing that stuff. I know that's his, his passion.

### Sean (2026-04-15T14:22:58.007Z)

I was going to say, did you invite him? Is he going to the meeting on Friday? Josh.

### Guest (2026-04-15T14:23:07.949Z)

Oh, yeah. No, we're all meeting. Yeah, it's just he's on it now, so he, like, would love the context before he spins today and tomorrow on singular bench.

### Sean (2026-04-15T14:23:08.807Z)

Okay.

### Guest (2026-04-15T14:23:17.309Z)

So.

### Sean (2026-04-15T14:23:21.847Z)

Thank you, Nicola.

### Guest (2026-04-15T14:23:33.469Z)

I, I've done with payments. Payments flow with crypto. With Apple and Google pay. So everything is fine except some issues that are locked in tickets and past everything what is left to honor. So she will handle everything. And I guess that's all.

### Sean (2026-04-15T14:24:05.927Z)

Got. Cha. Thank you very much, Ram. A. Ed, you have anything else? You want to toss in?

### Guest (2026-04-15T14:24:14.669Z)

Yeah. Just the engineering Channel. Clock that we just had during the standup. I think the pro banner on daily charts introduced a small error. On, like, resizing of resolutions, I think. So if somebody could grab that because Larry was aware of this bug, that'd be very much appreciated. Not sure if, like, not sure who has the capacity now because there's a million stuff to take a look at. But let me know. We could investigate.

### Sean (2026-04-15T14:24:58.327Z)

And as for me, finishing up some of the stuff that I was working on yesterday. And yeah, whatever work that needs to be passed on, if you guys can't pass it to another engineer, just feel free to reach out to Ed and I. And then we'll distribute it. As best as we can and try to take a look at it ourselves. And that's the biggest updates on my end. Does anybody else have anything that they want to discuss before they head out? All right guys.

### Guest (2026-04-15T14:25:32.669Z)

Well, I'd like to say thank you for all your kind words. It's been a pleasure working with you. And I hope that it's not a firewall, but just a good buy and see you later. It's the same from side, my side. Thank you for this work that was a great adventure. And I wish you all the best. Roma, you've been with us for years and years, and we've been through a lot since the days of early days of pro. Just can't thank you enough for all the work that you've put through us. And I remember our first meeting talking about starting auto tests. You know, now we have. An evolved full suite on across all of our products. So just want to thank you and thank everybody for everything you've done for us. And spend great working with you. But, yeah, Rama, it's not, you know, I'll get back to you as soon as I hear from the new CEO, but, yeah, it's just. You know how these things go. Well, soon they'll miss you before we know it, and then we'll be asking for help come back. But, yeah, until I wish all the best and definitely hope you get some new projects. Thank you very much. Yeah. Thank you very much, guys. I've been able to work on always, almost with everyone of you. So it was a great pleasure. And I still remember all those videos which Brian recorded for me. Just enroll in this project. It was amazing. So every morning I would see, like, new video, new task. So. It was really easy to enroll in this project. So thank you. I also want to say thank you for all of your hard work. It was a pleasure for me to work with all of. You. Thank you. We'll always think of you, Maria, when we visit crisis pages and all the, all the pages on that go. Because has a little bit of, a little bit of you and all. The hell you had to endure. But, yeah, thanks again, everybody. And may our paths cross again. Best of luck.

### Sean (2026-04-15T14:28:16.087Z)

Thank you very much team. Very much appreciate everything you guys have done for us, for the short amount of time I've been here. You guys have made it a lot easier. So thank you guys and I hope we do see each other again.

### Guest (2026-04-15T14:28:29.709Z)

See. You.

### Sean (2026-04-15T14:28:30.247Z)

Bye guys.

