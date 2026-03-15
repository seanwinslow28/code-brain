# 📝 Notes

Feb 18, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivčević](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Panasenko](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~ ~~[Krystof Oliva](mailto:koliva@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMThUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.clpnqce2tckl) 

### Summary

**Team Updates and Releases**  
Multiple team members provided updates on completed tasks, including support for marketing page releases, data dashboard migration fixes, deployment dashboard updates, and backend notifications implementation.

**Ongoing Technical Projects**  
Key ongoing initiatives include clearing the backlog, addressing multi-language MVP issues, fine-tuning iOS notifications, and working on various API refactors and front-end SEO assignments.

**Elections Hub Video Strategy**  
The team agreed that video integration for the elections hub should support both long-form and short-term video content, with a decision to surface videos directly on the election page as the initial MVP approach before developing a dedicated media hub

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

## ALIGNED

* **Deprecate Old Service Timeline** Old service deprecation timeline defined. Deprecation requires completion of prices, data dashboard migrations. Team will flip switch once migrations finished.

* **Video Support Integration Scope** Video support integration requires broad scope. Support includes long-form and short-term videos.

* **Election Coverage Video Display MVP** Election coverage videos will surface directly on election page as Minimum Viable Product. Older videos replaced by newer ones without 'See More' Call-to-Action link.

*More details:*

* **Team Updates: Aliaksandr Kryvanosau**: Aliaksandr assisted with the front-end release and subsequently worked on the reach out model for jobs ([00:00:00](#00:00:00)). They reported that everything went smoothly on their end regarding the previous day's activities ([00:01:59](#00:01:59)).

* **Team Updates: Ana Benitez**: Ana helped with the marketing page release and is continuing the data dashboard migration for the 'Agri review,' which is progressing well. They plan to finish the individual page and continue working on the prices page after receiving fixes from Maria, noting that the data migration is very close to completion and they plan to finish it today ([00:01:59](#00:01:59)).

* **Team Updates: Brian Mendoza and Project Status**: Brian completed the notifications endpoint and made necessary fixes, planning to put it on a dev box for review. The public websocket is functioning correctly, suggesting the team is close to deprecating the old service after the prices and data updates are finished ([00:03:09](#00:03:09)). Brian also investigated the issue of extra impressions on the sticky footer, confirming that their end shows no doubled impressions, but they will continue to look if the issue persists ([00:04:17](#00:04:17)).

* **Team Updates: Cesar Paz**: Cesar is developing the capability to update mono in the dev box via a button in the deployment dashboard, which they anticipate deploying today. They also deployed campus CLRS yesterday and have an assignment to apply something in Terraform, after which they may begin work on agents if no more urgent tasks arise ([00:05:18](#00:05:18)).

* **Team Updates: Koray Baspinar**: Koray is primarily focused on the multi-language Minimum Viable Product (MVP) and clearing up lingering `href` errors from the last audit. They plan to re-crawl the website using Hrefs and Screaming Frog, and also need to address several questions sent by Nicola ([00:06:52](#00:06:52)).

* **Team Updates: Kristoff and SEO Tasks**: Edvinas provided an update for Kristoff, who is out, stating that Kristoff received a Pull Request (PR) review from Nicola and will work on it the following day ([00:06:52](#00:06:52)). Kristoff has been assigned several backend SEO tasks in addition to the front-end data dashboard banner ([00:08:07](#00:08:07)).

* **Team Updates: Maryia Zhynko and Marina Lozuk**: Maryia completed fixes for stock pages and continued work on the elections hub LinkedIn page. Marina picked up a task related to the data dashboard issue where it does not support black theme and is working on allowing the theme to change in the iFrame when the side theme is changed ([00:08:07](#00:08:07)).

* **Team Updates: Mike Price**: Mike has been fine-tuning notifications for the iOS app and working with the team on the deploy ([00:08:07](#00:08:07)). They also have two APIs pending release—one for Simon AI and a refactor of the ProPublic API—which are close to completion. Mike confirmed that feedback for the testing app, including screenshots, should be added to a feedback spreadsheet or sent directly ([00:09:54](#00:09:54)).

* **Team Updates: Mikita Hulis and Release Support**: Mikita spent the previous day supporting the release by addressing various bugs and making adjustments for deployment for both the front end and back end ([00:09:54](#00:09:54)). Today, their focus is on leftover items that require feedback from Claudine, such as design and business decisions regarding redirects. Mikita reported that a core issue yesterday was DevOps related, and Nicola asked to skip the standup to log off early due to staying late during the release ([00:10:58](#00:10:58)).

* **Team Updates: Nikola Pivčević and Backlog Refinement**: Nikola spent time clearing up numerous tickets in the backlog, removing those that were done, duplicated, or fixed during the migration ([00:12:21](#00:12:21)). They assigned work to Bogdan and Kristoff, reviewed their PRs, and continued work on video content. They noted that the current design for video content appears to only surface shorts, suggesting that the team may want to consider supporting long-form videos for the elections hub ([00:13:21](#00:13:21)).

* **Discussion on Video Content Strategy**: Edvinas agreed that the video support integration should broadly accommodate long-form and short-term videos, stating that they need to see what the team can produce for the election period ([00:13:21](#00:13:21)). The media/design team confirmed that, as an MVP, they could surface videos on the election page without a "see more videos" Call to Action (CTA), though Edvinas and Nikola noted this would prevent users from revisiting older videos ([00:15:06](#00:15:06)). Edvinas proposed that surfacing the videos on the election page is the simplest approach for the initial election coverage, prior to developing a full media hub ([00:16:13](#00:16:13)).

* **Video Storage and Technical Details**: Sean inquired about storage limits, and Nikola clarified that videos use a separate service called Max, while images are stored on AWS S3, meaning there is no practical limit to storage ([00:17:24](#00:17:24)).

* **Team Updates: Ramuald Vishneuski**: Ramuald is continuing to work on fixes for Campus on both the front end and back end. They noted that the release the previous day was successful ([00:17:24](#00:17:24)).

* **Team Updates: Edvinas Rupkus and Sean Winslow**: Edvinas is providing requirements, unblocking people, and overseeing various initiatives ([00:17:24](#00:17:24)). Sean reported that Bogdan completed urgent bug fixes for price converter pages, deployed a ticket for new contributor logic, and worked on a ticket for the eyebrow on press release, all of which are ready for testing or review. Sean has also been tasked with creating a Campus tracker to continue the work from the February 17th tracker, and noted that the next logical steps for Campus involve the individual marketing page, payment flows, and account management tools ([00:18:48](#00:18:48)).

### Suggested next steps

- [ ] Brian Mendoza will put the cranked out notifications endpoint thingy on a dev box for review, and probably put up a PR to put pre-bid on the sticky footer.

- [ ] Brian Mendoza will message Mike Price with some details about deprecating the old service after the price and data migration.

- [ ] Koray Baspinar will recrawl the website through Hrefs and Screaming Frog, and try to answer some questions asked by Nikola Pivčević from yesterday.

- [ ] Sean Winslow will put together a campus tracker, continuing on what was started with the February 17th tracker, by digging through tickets to see what might need updating.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=tKkbDaErGWKfWtl31HcCDxIWOAIIigIgABgDCA&detailid=standard)*

# 📖 Transcript

Feb 18, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Edvinas Rupkus:** Hi  
**Sean Winslow:** s\*\*\*.  
**Ana Benitez:** Hello.  
**Sean Winslow:** s\*\*\*.  
**Aliaksandr Kryvanosau:** at your zoom is so fancy like your web camera.  
**Edvinas Rupkus:** Oh, my camera love hate  
**Aliaksandr Kryvanosau:** Yeah.  
**Edvinas Rupkus:** relationship. My My room is prettiest.  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** It's like a guest room, so I don't like when it's the full wide view of it of the whole thing, but I hate how it follows  
**Sean Winslow:** You know,  
**Edvinas Rupkus:** me.  
**Sean Winslow:** you can turn that off. You know that, right?  
**Edvinas Rupkus:** I know, but then it shows like 180 what's around me.  
**Sean Winslow:** Oh, gotcha.  
**Brian Mendoza:** What are you hiding, Ed?  
**Edvinas Rupkus:** The regs mining  
**Sean Winslow:** All right, we'll get started. Alex,  
**Aliaksandr Kryvanosau:** You're not sharing. I think you're not sharing your screen,  
**Sean Winslow:** what?  
**Aliaksandr Kryvanosau:** I  
**Sean Winslow:** Oh s\*\*\*. Sorry.  
**Aliaksandr Kryvanosau:** think.  
**Sean Winslow:** Let's get started. Alex  
**Aliaksandr Kryvanosau:** All right. Uh so yesterday I helped a bit with the front end release and then worked on the reach out model for jobs and that's mainly  
   
 

### 00:01:59 {#00:01:59}

   
**Sean Winslow:** Cool.  
**Aliaksandr Kryvanosau:** it  
**Sean Winslow:** Yeah. And everything, how you feeling about yesterday? Everything go okay on your end? Did you  
**Aliaksandr Kryvanosau:** on mind. Yes,  
**Sean Winslow:** get  
**Aliaksandr Kryvanosau:** but there are more about about it on Gita's site.  
**Sean Winslow:** Okay. All right. Cool. Thank you, Alex. Anna.  
**Ana Benitez:** Um hello well like Alex mentioned I help with marketing page uh release yesterday after that I continue with um data dashboard migration so for the agri review everything's looking good and I will continue with individual page uh hopefully uh get that finished today and I also will continue with prices page after Maria made some uh fixes. And that's all for me.  
**Sean Winslow:** Perfect. Thank you.  
**Edvinas Rupkus:** Do we are we are we close with those? How close are we with the prices and the data?  
**Ana Benitez:** Well,  
**Edvinas Rupkus:** I know that we've a lot  
**Ana Benitez:** for data, I yeah, for data, I think uh it's really close.  
**Edvinas Rupkus:** of  
**Ana Benitez:** I I plan to finish today.  
   
 

### 00:03:09 {#00:03:09}

   
**Ana Benitez:** Uh and for prices,  
**Sean Winslow:** Cool.  
**Ana Benitez:** uh there are still some pending issues, but uh I see Maria has that on review already. So, pretty close for prices, but still something fixes to be checked.  
**Sean Winslow:** Thank you. Bodon has his exam. So, everyone toss in a little celebratory. There you go. Beat me to it. So, yeah. So, I'm sure he's going to come back, crush it, start running this whole team. But for now, we'll go to Brian.  
**Brian Mendoza:** Cool. Um, only update is I cranked out the notifications uh, endpoint thingy. Just had to make some fixes. I'm going to put it on a dev box for review. And the public websocket is working as expected. So, I think after price and data, we can flip the switch. Um, I'll probably message Mike with some details, but we're pretty much good to go in terms of like deprecating the old service. I'm sure there might be some headaches, but you know, everything's done.  
   
 

### 00:04:17 {#00:04:17}

   
**Brian Mendoza:** So, getting very close.  
**Sean Winslow:** Nice.  
**Brian Mendoza:** And I looked at the thing you sent me at I sent you a Slack message about extra impressions on the sticky footer. Um, nothing on our end shows that. Everything's single, not doubled, but we can keep looking if it continues to be an issue.  
**Edvinas Rupkus:** Yeah, I mean at this point that's why I'm asking about the the data and prices migration because I just want to  
**Brian Mendoza:** Okay.  
**Edvinas Rupkus:** be over with it. Um it make it doesn't really make sense how we can have like  
**Brian Mendoza:** Cool.  
**Edvinas Rupkus:** half page views but double the sticky foot impress impressions. Yeah, I don't know. But that I feel like I don't have the bandwidth to like really dig into it when we're so close to being done with  
**Brian Mendoza:** Oh, speaking of Maria,  
**Edvinas Rupkus:** that.  
**Brian Mendoza:** I'll probably put a PR up for something to put pre- bid on the sticky footer. But yeah, I think We can those. Yeah. Sorry, I'm just rambling.  
   
 

### 00:05:18 {#00:05:18}

   
**Edvinas Rupkus:** Yeah, no worries.  
**Sean Winslow:** Awesome.  
**Edvinas Rupkus:** I'll let you know if there's more like need for investigation, but I'm good for now.  
**Brian Mendoza:** Cool.  
**Sean Winslow:** Thank you, Brian. Caesar  
**Cesar Paz:** Uh hi. Well um I'm working now uh in the possibility to update uh mono in the dev box uh through a button in our deployment dashboard. Uh I'm going to deploy it uh probably today. Um well in addition uh yesterday I yeah I deployed in the morning campus clrs. Um let me think because I did more things yesterday. Um well I'm going to say that's all. Um yeah because I don't remember.  
**Sean Winslow:** Good.  
**Cesar Paz:** Sorry.  
**Sean Winslow:** It's okay. Yeah.  
**Cesar Paz:** Um yeah and probably now when I finish this one yeah I have to uh apply something in terraform that might send me now um if I don't have more urgent task to do well I'm going to start with the a aents if it's possible if it's not I I'll do other task if it's necessary and yeah that's  
   
 

### 00:06:52 {#00:06:52}

   
**Sean Winslow:** Cool. Yeah, I was going to ask you about that,  
**Cesar Paz:** Oh,  
**Sean Winslow:** but it sounds like you have your plate full, but I'll I'll send you some stuff that I that I find on it if you find it useful.  
**Cesar Paz:** okay.  
**Sean Winslow:** Cool.  
**Cesar Paz:** Thank you.  
**Sean Winslow:** You're welcome, Daggy. Caesar Corey.  
**Koray Baspinar:** Hello. Uh I am mainly working on multil- language MVP and also uh trying to clear a few uh hrefs errors uh left in the uh last audit and I will recroll uh the website through Hrefs and Screaming Frog and also try to answer uh some questions that asked uh by Nicola from yesterday. Since yesterday, he sent me a bunch of emails. So, yeah, I will also work on that. That's it.  
**Sean Winslow:** Sweet, man. Thank you. Kristoff is also out, I believe. So,  
**Edvinas Rupkus:** Yeah. Yeah.  
**Sean Winslow:** Maria  
**Edvinas Rupkus:** I have a an update from Kristoff. Nothing crazy, but he told me that he's got a review or a PR review from Nicola.  
   
 

### 00:08:07 {#00:08:07}

   
**Edvinas Rupkus:** He'll work on that tomorrow. And then yeah, Nicola and I sort of have been assigning him a few things. So the for in addition to the front end data dashboard  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** banner, so he has a few of the backend SEO tasks. Thank you, Nicola, for looking through a bunch of those tickets. That's from Kristoff.  
**Sean Winslow:** Thank you, Kristoff. Maria  
**Maryia Zhynko:** Yep. Today I did some fixes for stock pages and continued working on elections hub LinkedIn page.  
**Sean Winslow:** Very cool. Thank you, Maria. Marina  
**Marina Lozuk:** Hello. Today I I pick up the task regarding data dashboard uh issue that it doesn't support black theme. So I'm working on it to allow changing the theme in the I frame by changing the theme on the side. That's it.  
**Sean Winslow:** Cool. Thank you, Mike.  
**Mike Price:** Uh few things mainly getting notifications for the iOS app fine tuned uh was working with the team on the deploy yesterday getting things ready for that and then I have two APIs that we're playing for Simon AI and um refactor of the pro the propublic API.  
   
 

### 00:09:54 {#00:09:54}

   
**Mike Price:** So, both of those pending release, they're close, but just trying to get the last little bits over the line. So, that's it.  
**Sean Winslow:** Cool. Thank you. Yeah, when it comes to uh so I've been playing around with the app and I saw that it said for the testing purposes you could just take a screenshot and then send it to you. Is that within the actual test flight app itself or is that do I just send it to you via Slack? I haven't found anything. I was just curious.  
**Mike Price:** I think we had a spreadsheet. Um,  
**Sean Winslow:** Okay.  
**Mike Price:** yeah, if you have a feedback spreadsheet, put it there. But fine to reach out directly if you have screenshots and details, stuff like that. It's always helpful.  
**Sean Winslow:** Sweet. Oh, you got it. Thank you, Mike. Nikita Gulis.  
**Mikita Hulis:** Yep. Yep. So, of course, yesterday was all about supporting the release like various uh various bugs and adjustments for deployment for both front end and back end.  
   
 

### 00:10:58 {#00:10:58}

   
**Mikita Hulis:** So, yeah, me Roma uh Alex and Mike were all about it yesterday. Uh yeah, it seems like it went good. Stayed stayed a bit late, but yeah, it did went well after all. Uh, yep. Today I'm focused on the leftovers or the thing which needed feedback from Claudine. For example, various like design/ business uh decisions for when this particular where this particular redirect should go etc etc like where where we redirected after the test etc etc. Um there are a few of those. So, working on those today and uh I think we'll deploy them probably tomorrow. Um, yep. And Alex has said that there is more more from Nikita, but he he asked that he'll actually skip this one and uh log off a bit earlier today because he was the last hero standing yesterday because uh all of the all of last issues were on the back main on in the in the admin panel. uh which in the end we've uh figured out was due to the it was DevOps uh related basically.  
   
 

### 00:12:21 {#00:12:21}

   
**Mikita Hulis:** Um so yeah more from him tomorrow I guess.  
**Sean Winslow:** All right. Yeah, that works. Yeah, thank you again. Um, yeah, that was I was looking at the time when we were getting all those messages and it was about, you know, 5:00 p.m. our time. I was like, Jesus Christ, that's different level for you guys. Very much appreciate it all of  
**Mikita Hulis:** I for sure logged off like today.  
**Sean Winslow:** you.  
**Mikita Hulis:** Nig has stayed up until like 4 a.m. I think or something like this.  
**Sean Winslow:** All right. See, I don't know why he just didn't pull an allnighter and just, you know, come to the stand up. He's slacking.  
**Mikita Hulis:** Yeah, let's call  
**Sean Winslow:** Call him right now. Thank you, Nikita. Nicola.  
**Nikola Pivčević:** Uh yeah, hello everyone. So uh yeah, I've been uh uh mostly like looking through uh like clearing up a bunch of tickets uh from the backlog and trying to uh remove the tickets that were a lot of text tickets were like done,  
   
 

### 00:13:21 {#00:13:21}

   
**Sean Winslow:** updated.  
**Nikola Pivčević:** duplicated uh fixed during the migration. Uh and uh yeah, so did that. sorry for sending like I guess like a bunch of emails to a whole bunch of people uh like notifications. Yeah. Uh and um yeah, found some work for both Bogdan and Kristoff and uh yeah, reviewed some of their PRs and work and uh yeah uh continued working a bit on the video content. Uh just uh yeah, I saw that Serena like now has like a third iteration of the design which now is like more cleaner and like um yeah, I I did notice that we are now only surfacing shorts which I don't know like just just just pointing it out that like um yeah regarding the video content uh maybe we will have also long form videos on the elections. have fake  
**Edvinas Rupkus:** Yeah. Yeah.  
**Nikola Pivčević:** Adam.  
**Edvinas Rupkus:** I would say we should uh approach the this task like the video support integration with like more more broader like with to support long form videos, short-term videos, etc., etc. Uh but yeah, the election we we'll see like what the what the team is able to produce for the election period, but we would like to have you know the ability to upload videos even after elections are over you know uh and also I've been chatting  
   
 

### 00:15:06 {#00:15:06}

   
**Edvinas Rupkus:** with media/design team on the actual question that you had Nicola about like okay where do we store the videos like where they live and obviously we have to like see see more videos or see more media CTA there in the design. They said if we lose that and we just we just surface like as an MVP basically for election coverage, we just have the videos with no like CTA to go see more videos. Would it be possible to for them to just live on the election page? I I feel like from what what I understand I I probably should have a a place a home somewhere, but I don't know what  
**Nikola Pivčević:** like it's not necessary but that mean that would mean that like uh if you want to revisit a video  
**Edvinas Rupkus:** what  
**Nikola Pivčević:** that was like three videos ago there is no place where you can see that video right I  
**Edvinas Rupkus:** correct.  
**Nikola Pivčević:** kind of yeah I we can do it but I'm just like just wanted to  
**Edvinas Rupkus:** Yeah.  
**Nikola Pivčević:** to confirm like what's the direction that we want to  
   
 

### 00:16:13 {#00:16:13}

   
**Edvinas Rupkus:** Yeah. Uh ideally after like the keep keep talking about the CTO the core template optimization after that exercise that we'll go through product and design we'll definitely want to have a media hub where we have podcasts and we have you know short-term long-term videos that's sort of like a centralized place where you can explore all media and videos that the block produces. But before we get there, we'll have election coverage uh live. So, I think like as a sort of like try to trial it out and see how how well those those videos are accepted and how much are they watched. Uh I guess the the shortest uh path of resistance is or whatever cleanest path what whatever the saying is is to just just surface those videos there and then if they uh you know get replaced by newer ones they they get replaced and that's it.  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** Does that sound good?  
**Nikola Pivčević:** Yeah. Yeah. Sounds good. Yeah.  
**Edvinas Rupkus:** All right.  
**Nikola Pivčević:** Sounds  
**Edvinas Rupkus:** Sweet.  
**Sean Winslow:** Does WordPress have a limit on storage?  
   
 

### 00:17:24 {#00:17:24}

   
**Sean Winslow:** Like I know we have a bunch of photos stored in there, but I don't know about videos is usually linked through  
**Edvinas Rupkus:** That's our is that our  
**Sean Winslow:** YouTube.  
**Edvinas Rupkus:** AWS  
**Nikola Pivčević:** So videos we are using a separate service called Max for videos and for images it's uh AWS it's S3 right? So it's no limit.  
**Sean Winslow:** Oh,  
**Nikola Pivčević:** Yeah.  
**Sean Winslow:** okay. Gotcha. The limit does not exist, but yeah. All right. Sounds good. Thank you,  
**Nikola Pivčević:** And thank you.  
**Sean Winslow:** Nicola. Romo  
**Ramuald Vishneuski:** Uh hello uh everybody. Uh so uh we're still working on some fixes for campus uh on front end side on back end um and yesterday release was uh pifer um and I guess that's all.  
**Sean Winslow:** All right, cool. Thank you, Roma. Ed, any  
**Edvinas Rupkus:** No,  
**Sean Winslow:** updates?  
**Edvinas Rupkus:** just uh seeing through a bunch of these a bunch of these initiatives and try to provide requirements uh wherever possible unblock people. Thank you for all your help and diligence.  
   
 

### 00:18:48 {#00:18:48}

   
**Sean Winslow:** Is that directed towards me or to the team?  
**Edvinas Rupkus:** Everybody, you as in the  
**Sean Winslow:** Okay, I'll speak for everybody. You're welcome, Ed.  
**Edvinas Rupkus:** team.  
**Sean Winslow:** Uh but I forgot to mention uh when I passed over Bon, but he mentioned he he worked on urgent bugs for price converter pages where all pairs were not loaded, deployed and verified. He deployed a ticket for new contributor logic. Left a comment for Ed regarding it. Did you see that,  
**Edvinas Rupkus:** Yeah. Yeah. Yeah.  
**Sean Winslow:** Ed?  
**Edvinas Rupkus:** I'm talking to researchers to test it  
**Sean Winslow:** And he worked on a ticket for eyebrow on press release.  
**Edvinas Rupkus:** out.  
**Sean Winslow:** It's ready for testing. and a couple more less important tickets that are ready for testing, ready for review. So, that was Bodon and an update for me. Um, I was asked to put together a campus tracker, pretty much continuing on what we started with the February 17th tracker. So, I'll be digging through tickets to see any anything that might need updating.  
   
 

### 00:19:49

   
**Sean Winslow:** But Romalt and Nicola, I might reach out to you if you guys notice anything so I could just add it to the list so we can keep track and keep everyone uh keep everyone updated on  
**Edvinas Rupkus:** Yeah, it's mainly it's mainly the individual piece.  
**Sean Winslow:** everything.  
**Edvinas Rupkus:** So like the thing first things that come to mind is the payment flows. Uh well I guess we'll start at the beginning the individual marketing page that's already assigned to Alex. Then it'll be the payment flows that you know kind of originate from that marketing page and hooking it all up so they can have buy access to 101, buy access to 2011 or buy all access.  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** And then also with that we'll have the the things within well when you're already in campus uh your account management tools where that will pop up that we've that we've talked about and like we try to scope it down. So that will also be part of it. Ho how much of it we release in the very next release that's another disc discussion but like this is this is the stuff that's you know the next step after this obviously after we fix any bugs anything that's not working with the 2011 and yesterday's release but those are the next sort of logical next steps for campus  
**Sean Winslow:** All right. Yeah. So, those are my updates. Uh, thank you, Ed. Um, I'm going to get started on that today. And, yeah, does anybody else have anything that they want to talk about?  
**Edvinas Rupkus:** just uh just hit me up if you have any questions. I can help you point into the the right places for those stuff because a lot of that stuff is already ticketed  
**Sean Winslow:** Okay, perfect.  
**Edvinas Rupkus:** out.  
**Sean Winslow:** Thank you everybody else. Good.  
**Edvinas Rupkus:** Yes, sir. Thanks,  
**Sean Winslow:** All right. Yeah,  
**Edvinas Rupkus:** Dean.  
**Sean Winslow:** thank you everyone and huge shout out for campus yesterday. Campus team, everyone who participated. Honestly, the whole team definitely had their hand in it.  
   
 

### Transcription ended after 00:22:16

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*