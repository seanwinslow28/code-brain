---
granola_id: c9ec03bb-c9b3-4878-a6de-243936db3d06
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of unified daily standup - transcript.
context: the-block
created: 2026-03-12
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

### Guest (2026-03-12T14:00:51.713Z)

All right. Look at you tagging in the you said it was pretty serious and important. Incorrect. Two pages. Yeah. They return 200 instead of 404. But a lot of them. But the sheet that you link in it, like in that ticket. It talks about no titles. On them. But the issue is different. Just Ahrefs saw it like this. It shows an empty page. It should be 404. Right, nicola? Sorry. What was that? This. You know, like this Ahrefs issue. Latest. Some pages, like empty pages, shows 2, 200. It should be like, 400. Four. Ah, saw it like Missing Title and meta description, but the issue is way bigger than that. False positive. Okay?

### Sean (2026-03-12T14:02:04.033Z)

All good.

### Guest (2026-03-12T14:02:06.433Z)

Yeah. I'll sign to Nicola. Investigate.

### Sean (2026-03-12T14:02:09.553Z)

Cool. All right. Kicking it off. The one and only. Alex, what do we got?

### Guest (2026-03-12T14:02:18.753Z)

Hello. So I finalized the visual part of the marketing page for individuals. So I need to connect with Nikitas to understand where we are with the checkout flow, to proceed with it. And that's it.

### Sean (2026-03-12T14:02:33.473Z)

Perfect. Thank you. Anna.

### Guest (2026-03-12T14:02:40.913Z)

Hello. So from my side, I will continue testing. The advertise for homepage. Only the part that is missing is looking at GAM reports from yesterday's interactions. And I also will we we continue with frequent schematic. And the learn articles fixes prior work done. I need to connect with him due to some comments on the on those tickets. And also for the prices. Migration. Big ticket for all the book fixes. The only thing left is that at tech. But I believe there is no Active right now. So I'm connecting with your mic to see how it tests these on staging. And that is all for myself.

### Sean (2026-03-12T14:03:38.513Z)

Perfect. Thank you, anna.

### Guest (2026-03-12T14:03:40.033Z)

Yeah, if, if, if you want to, like. Test it on prod too. Like, if you want to just assign a token real quick. Like, we launched it. We launched prices with a quick ad. Those pages don't get like that many views, so we want to know really would even notice it. I think it's fine. Like, if it's. If. If it's easier to do it. I mean, I guess up staging ads too, you can do it pretty easily, but. Yeah, just in case. You're not sure that the test environment would portray the full picture. Okay, thank you. We'll let you know. I joined at the right time. Sorry. Also, Anna, if it's. If that's annoying, I can just push up a little change that I was doing. There's like a validation to the Google domain. Takes, like, 30 seconds to remove. I can remove that and we can force it. It's pretty easy. But, I mean, you probably also want to test the actual GAN flow itself, so let me know if you want me to turn that on. Yes, I'll let you know. I'm asking German right now, so maybe he can. Hear. Help, provide something for just thinking on that side.

### Sean (2026-03-12T14:04:55.633Z)

Cool. Thank you, anna. Bodan.

### Guest (2026-03-12T14:05:00.673Z)

Yes. So I started working on the ticket for embedded chart and I think I already might have like a solution, but I need to like to fully implement it and test it out. If it's fine, I will send PR to Data Brian or I mean, yeah. Whoever, and I will deploy the ticket for this update collection, blah, blah, blah, right after this meeting. So something like this? And. And that includes the embed page views as well. Or did you guys split that with Brian? What? One of the requirements in that ticket for embedded data chart functionality is not counting page views anymore. Just let's take a look at the ticket and let me know if you have any questions. The second bullet. Okay. Okay. Yeah, but I think it's okay, but I will check it. Okay?

### Sean (2026-03-12T14:06:11.713Z)

Sweet. Thank you, b.

### Guest (2026-03-12T14:06:12.433Z)

Thanks. I think. Sorry, like, just for some context, I think for some time we had like a subdomain embed dot the block co just because of this reason. So. It separates events. By host. Right? And I think we removed that quite some time ago. And so, yeah, it's. Maybe we need to bring it back. Because, like, I think we still want to count, like, page views on, on embeds, like, especially, like, from third party websites. Yeah, I think. Well, we. Yeah, I don't know when we remove them, but. Domain. But we. We didn't have any page views on GA4. And at least not that I was aware of. Maybe. Maybe I had a different subdomain, but. Brian, feel free to chime in. It seemed like we could just. Not count them when they're, like, embedded on that CO pages, is that correct? Yeah, that's fine. That's possible. Let's sync DMS if there are any more questions. Or better solution is available. Okay?

### Sean (2026-03-12T14:07:44.113Z)

Yeah. So, Brian, just so happens you're next. What you got?

### Guest (2026-03-12T14:07:48.513Z)

Cool. Amazing. Moved a bunch of tickets to testing, meaning the learn issues that popped up. And I was trying to debug the poly market thing. I couldn't get it. But then Marina sent me a helpful message overnight. So maybe there's a way to reproduce that there. So I'll be looking at that today. I'm seeing other tickets. Alone through qa. Is that for the. For the filtering for the. So I shouldn't. I shouldn't text them yet. So I woke up and she said that she found that she saw six on the homepage. And it might be related to the. I guess the automated clearing or the updating. Gotcha. Yeah. In the whole day I was kind of watching it, but I was forced in the refresh every now and then, but I was out of sync, so maybe don't text them yet. Maybe I can reproduce if I'm just waiting around. We'll see. I'll keep you updated. Sweet. Thank you.

### Sean (2026-03-12T14:08:49.153Z)

Thank you, brian. Caesar.

### Guest (2026-03-12T14:08:53.713Z)

Hello again. I'm not doing anything of this war. I keep doing bug fix or. Some. Yeah. I have songs. Some people do several things. But I. I keep stuck in the same task yesterday. I did all my best. I'm doing all my best to. To solve the problem with the research path in the developed role in the box. I did. I did a comparison. Between the barium and variables between pro and dev. I added new web bars. In addition, I modified some values. Here. We have in order to do test in the database. Yeah, I had to activate some project. I don't know. Research. Failing. So I keep working on that. Well, I have to. I have to check the deployment of the legacy VCO because it failed two days ago. So I need to check this. Find the reason why it's for you. That's all.

### Sean (2026-03-12T14:10:36.513Z)

Sweet. Thank you, cser.

### Guest (2026-03-12T14:10:38.993Z)

Thank you.

### Sean (2026-03-12T14:10:41.393Z)

Corey.

### Guest (2026-03-12T14:10:44.513Z)

Hello. I'm working on price page FAQs and I started to feel the heat. Resource team, I think, is going to follow up after me. And also I am working on geo optimization. For each non news page types I started to create tasks accordingly. Some of them I will do it by myself, some will need developer help as well like schema markups et cetera. In terms of content improvements, I start to do it myself first. I started with Learn Pages now and I will go to Data and other Pages as well because GEO is becoming more and more important. So we don't, we won't fall behind for that change. So yeah, it is, it is a must. I also discuss with team and other parts as well. So yeah, these are the testes I am working on right now.

### Sean (2026-03-12T14:11:55.153Z)

Cool, man. Thank.

### Guest (2026-03-12T14:11:55.793Z)

Awesome. And for the. For the I think you pages, you're adding FAQ questions, and then you're waiting for the research team to, like, check them. I am just adding the questions there, following the answers. I got it. Okay. And then. I don't know if. I don't know if you were on yesterday, but we were talking about it. About the specific question for how often price pages are. Price page. Information is updated on that individual page. And, like, ours are, I think, are just static. Like, we don't. We don't have a refreshing number on the individual page.

### Sean (2026-03-12T14:12:40.673Z)

You.

### Guest (2026-03-12T14:12:44.513Z)

I don't know if you're going to, you know, for the future FAQs that you create. Probably just better to skip that question because it's not, you know, I don't think it's anything just to brag about that. Our private pages are static. Okay? Thanks. Just. Just. Just wanted to ask. So how. How many FAQs or price pages did we already add? Like, up to 10. Eight right now. Yeah. Okay? So, yeah, I just wanted to ask. So Anna found, like, she was testing the schema markup for FAQs, and she noticed that we are kind of adding some, like, rich HTML. And I think it's not really intentional. It's probably like a side effect of copy pasting from somewhere else. And so. Just as a note, if we can when pasting paste as normal text, you know, like when you right click. So instead of just like pasting regularly, right click paste as text. So so that like, we remove the unnecessary markup from it. Because I think, like, not sure, like Corey, if, if that has like, negative impact on on schema markup. But, like, yeah, we don't want to. I think, like, we have, like, span and then style 400 pixels, something. I don't know. Yeah. Yeah, I can go through and make sure that. Okay?

### Sean (2026-03-12T14:14:31.233Z)

All right, sweet. Thank you, Corey. How are you feeling, by the way?

### Guest (2026-03-12T14:14:35.953Z)

Good. Good. Thank you.

### Sean (2026-03-12T14:14:36.833Z)

Good. Is not here. Maria.

### Guest (2026-03-12T14:14:51.313Z)

Marie is out for. For a few hours, so she'll. She'll be available in a few. Yeah.

### Sean (2026-03-12T14:14:53.473Z)

Okay?

### Guest (2026-03-12T14:14:57.313Z)

She told me she's working on. The election. Coverage, politician tweets.

### Sean (2026-03-12T14:15:08.193Z)

Cool.

### Guest (2026-03-12T14:15:08.913Z)

And then Marina also told me she had this kid daily for personal reasons, and she's working on that same pages by the market implementation.

### Sean (2026-03-12T14:15:19.553Z)

Sweet. And maxo. Nikita.

### Guest (2026-03-12T14:15:29.393Z)

Short and sweet. Working on the payment flow. Mainly today was focusing on the layout around. The Pagan volume itself and readjust it in frame to salvage as much of the previous layout as possible. Office logic, at least. And that's it. And, yeah, happiness. No additional bug ends or adjustments were found for the cell service for the first day in a while. So, yeah, Some cards in the chat. Thank you.

### Sean (2026-03-12T14:16:05.153Z)

Tell. Some hearts in there, some celebratory horns. Thank you, nikita. Makita o.

### Guest (2026-03-12T14:16:17.153Z)

Not too many things on my end. Working on the profile management for the multi courses for the stripe payment part release. Also was in touch with Mike yesterday regarding the new authentication flow. So we're still discussing how it would be better to do that thing. Just one quick question. So, for the sponsored courses. Do we want or don't we? The possibility to sign in using your wallet. Through the privy preview or something like that. So we just want to collect the address or we want to have the possibility to sign in. Through an additional sign in method. If it's super easy implementation that, like, doesn't prolong our, you know, death time. Then I would say, yes, let's support it. The collection page for the. Sean, I don't think we have an answer for how they're going to try to distribute the reward. Right? We haven't. We haven't gotten a response to that.

### Sean (2026-03-12T14:17:37.953Z)

H. Not yet.

### Guest (2026-03-12T14:17:40.113Z)

Yeah. So it's most likely going to be a code that people would like then use after watching the sponsored course as the reward on their respective platform. In this case, on Polymarket, they will use a code that they receive. Potentially if we have, like, wallet information. There would be an opportunity to distribute those rewards directly to, you know, like, to the, to the, like, waitlist those wallets or wait, white list those wallets for specific features. So long rant, but answer to your question is if we can support wallets. Great. If not, if it adds a lot, let's just skip it. And we'll do, like, a follow up later on. No, I mean, like, there were no problem to collect them. We're just discussing in terms of should we support the possibility to sign in using the wallets. Yeah. We still need to collect them during the flow. But it will be just stored somewhere in the database, for example, just as the string, right, as the wallet address. But it's a bit different thing because if you can't sign in through the wallet, it can be used as the separate authentication provider. Yeah, like, I don't know. I don't know if people would be. Scared of the. Of giving their addresses. Like, people are just skittish like that. So if we don't need to collect wallets, I would like, you know, shy away from it. But, like, again, Sean, we should check with Matt Bob market to see, like, what they plan to do. What? The distribution of the reward. Because. First of all, like, if people are. If we're going to educate users with X, I expect very few people to actually provide their wallet addresses because they just don't want to, like, box them. You know, bugs themselves. I think in the designs, that specific wallet collection step was optional. It wasn't a required thing. So, yeah, we just need an answer. Like, this decision has to be informed by an answer of how we're going to distribute these prizes. Yeah. I mean, but for the sign. It doesn't sound like we need to have the possibility to sign in through the wallets.

### Sean (2026-03-12T14:20:17.953Z)

No, it was just kind of like an option. It was before we started talking to Polymarket. So we were thinking that could be the connection to Polymarket. But that could very much change. So once we get a solidified answer from them of how they want to distribute the actual. Code or have a distribute the credits. Then we'll have a clearer answer. On whether or not we should actually involve wallets. But, yeah, sign in won't be necessary.

### Guest (2026-03-12T14:20:49.553Z)

No matter what. Okay, we can have definitive answer right now. I think. Yeah. Right this second. Yeah, we need to check. That's a good question. Though.

### Sean (2026-03-12T14:21:07.713Z)

It is. Yeah, I was talking to Mike about that stuff yesterday, too. And Nikita. I just had a quick question for you. Did you see my message about.

### Guest (2026-03-12T14:21:20.993Z)

Yeah, So, I mean, like, as there are no changes. There is nothing we should be worried about because we already understood that there won't be any entrance test. Right. There might be only one test. At the end, our regular quizzes. But David already know what to do with them.

### Sean (2026-03-12T14:21:47.873Z)

Cool.

### Guest (2026-03-12T14:21:48.593Z)

Because he just need to add the redirect after the last lesson to that quiz.

### Sean (2026-03-12T14:21:59.313Z)

All right, perfect. Thank you.

### Guest (2026-03-12T14:22:04.193Z)

No problem.

### Sean (2026-03-12T14:22:04.993Z)

Cool. All right. Thank you, nikita.

### Guest (2026-03-12T14:22:10.113Z)

Sean. Yeah, sean, let's not forget to ask matt.

### Sean (2026-03-12T14:22:13.953Z)

Yeah.

### Guest (2026-03-12T14:22:14.113Z)

Can you make sure to chase that answer? Please.

### Sean (2026-03-12T14:22:21.393Z)

Nicola.

### Guest (2026-03-12T14:22:23.473Z)

Yeah. Kings scroll down. Sorry, but so I think this I'm going to deploy after standup the fixes for the broken external links notifier. So this will now send to the correct channel. And thank you Caesar for setting up the environment variables. And also, yeah, I have that. I'll also I'm also adding the cloudflare. Header to kind of bypass Cloudflare issues that we had. And yeah, regarding the FAQ schema for price pages. So is that okay? So are we going to clean up the data so I don't have to kind of, you know, clean it up programmatically? Like, is that okay? So I guess, I think then I like that was the only issue that you found regarding this ticket? Rom, I said. Yeah. Okay, so I think, like, then it's ready to deploy, and then we'll fix the data. Okay? Okay. Okay. Okay, cool. And. Yeah, that's it. And translations.

### Sean (2026-03-12T14:23:42.273Z)

Co. Ol? All right. Thank you, nicola. Ramuald is at a doctor's appointment. So, Ed, do you have anything? You've been asking questions, so I think you're good.

### Guest (2026-03-12T14:24:01.793Z)

Yeah. No, I think. I think it's all good. He's. He's been heavily testing the campus experience. But now. The intest column looks healthy. Nothing specific to rung up right now.

### Sean (2026-03-12T14:24:19.633Z)

Nice. Yeah. And I spoke with David this morning. He said they're ahead of schedule when it comes to the sponsored course stuff, so that's good. And one thing that I wanted to bring up to the team is that Matt asked us to onboard a couple people to the campus website. So. I've never done that before. So would it be possible that if anybody can help walk me through the back end or how it actually work on the actual onboarding process?

### Guest (2026-03-12T14:24:54.433Z)

For pro and for campus.

### Sean (2026-03-12T14:24:57.073Z)

For pro2.

### Guest (2026-03-12T14:24:58.833Z)

You mean the. The management part, like the admin panel? Yeah, we basically create. It's our, I think, two final CDL candidates. So we just want them to have access to campus and pro, basically. I mean, probably the Roma will be the best person here, but I can do that as well. I mean, like, it all depends on what is our goals. Because the admin panel, especially on the prod, is the tricky thing, and it doesn't work. Everywhere and always. We're aware about those things, but it depends on what is our goal here. I mean, just to show how the data may look like. Or something. Right. Yeah, like to give access.

### Sean (2026-03-12T14:25:55.153Z)

Yeah. Forget.

### Guest (2026-03-12T14:26:00.113Z)

Okay? I mean, the login is shared. But we can issue them their own accounts. I'm just not sure how. They will work. Because mostly we just use only one account to sign in into the admin panel.

### Sean (2026-03-12T14:26:19.953Z)

Oh, yeah, they're not getting access to the admin panel. The whole idea is just to give them one month subscription to both pro and campus. So they're essentially just going to be checking it out like a user would.

### Guest (2026-03-12T14:26:32.833Z)

Oh. Okay, Then we can create the. The organization for just those two people. Give that work a trial. Subscription with the access to the products for one month. And boom. It's done.

### Sean (2026-03-12T14:26:53.073Z)

All right, cool. Ed, you have to create the organization. It's not one of the drop down ones.

### Guest (2026-03-12T14:26:59.953Z)

I, I have not created a private organization or like any user and clms or pro. So I, I am the worst at this, at this. You can just ping me and Roma in common chats and we'll solve it. No problems.

### Sean (2026-03-12T14:27:17.793Z)

Perfect. Thank you. All right. So. That was really it on my end. Does anyone else have anything they wanted to discuss? All right. Sweet. Everybody. Enjoy your Fridays and your weekends. I'll talk to you later. And Nikita, I will message you with some help. I appreciate it.

### Guest (2026-03-12T14:27:49.233Z)

Thanks, team. Thank you.

### Sean (2026-03-12T14:27:49.873Z)

All right. Guys later.

### Guest (2026-03-12T14:27:51.153Z)

Bye, team.

