# 📝 Notes

Jan 27, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivcevic](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Vadimovich](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAxMjdUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.1kexkkuhj0vp) 

### Summary

Aliaksandr Kryvanosau prioritized the enterprise marketing page, partially failed a Salesforce test due to external issues, and agreed with Edvinas Rupkus to schedule another test and check with Decision Foundry to test the remaining forms by the February 12th Marquetto deprecation deadline. Ana Benitez is testing data dashboard and FAQ fixes, found an article spacing bug that Edvinas suggested was ticket 4426 under Brian Mendoza, and determined the issue was separate from the newsletters/prices ticket. Bohdan Vadimovich deployed the price converter migration, updated a display name ticket, received clarification from Cesar Paz on WordPress monoblocks deployment, and is working with Nikola Pivcevic on a user deletion error due to a lack of approval for the current solution. Brian Mendoza finished multiple tickets, moved them to testing, and will start poly market WordPress work, while Cesar Paz created Confluence pages for red boxes and LWS cost reduction (expected to save $\\$5,000-\\$7,000$ monthly), deployed a new Graph dashboard, and added Docker image update functionality. Koray Baspinar is compiling a list of unnecessary categories and tags to improve SEO, collaborating with Matt on category/tag pages, and confirmed Brian is working on the "mention us in Google thing." Maryia Zhynko finished fixes for stock and ETF pages, is adding a 'buy button,' and Marina Lozuk is addressing data dashboard issues, improving chart embedding, and asked Edvinas Rupkus to check with Matt regarding the priority of a real-time chart download feature. Mikita Hulis and Nikita Orobenko reported a major shift in priorities due to a miscommunication about a new course format, requiring them to drop other tasks like payment setup to implement extended CMI5 or X API support for the course's interactive format within two weeks, with the goal of releasing the update on the 13th, postponing upsells and sales components. Nikola Pivcevic fixed Chroma-reported issues related to jobs, enabled adding charts to stock pages, prepared a fix for AMP pages, and started a report for broken external links, while Ramuald Vishneuski continues work on crypto jobs but will prioritize multicourse testing. Sean Winslow is working on campus voiceovers and tickets for release, has a meeting with design, and is working on the job board; Edvinas Rupkus confirmed the poly market contract signing is causing a shift in many development priorities.

### Details

* **Marketing Page Development and Adjustments** Aliaksandr Kryvanosau's main priority was the marketing page for individuals until the focus switched to the enterprise marketing page, reusing some of the individual page work ([00:00:00](#00:00:00)). Aliaksandr mentioned that testing with Salesforce was partially unsuccessful because they had Salesforce issues preventing them from fetching the form, but noted a small bug where an error message does not stop the loader, which is a small issue that can be fixed ([00:01:50](#00:01:50)). The plan is to schedule another Salesforce test session, and Edvinas Rupkus and Aliaksandr agreed to check with Decision Foundry to ensure time is set aside to test the rest of the forms that were not tested yet, with a hard deadline to deprecate Marquetto by February 12th ([00:26:13](#00:26:13)).

* **Testing and Bug Fixing for Data and Articles** Ana Benitez is testing fixes for data dashboard migration and frequently asked questions ([00:01:50](#00:01:50)). Ana inquired about a ticket for a bug regarding spacing between images and text on articles, which Edvinas suggested was ticket 4426 under Brian. Nikola Pivcevic suggested that a new fig caption feature for the Yahoo RSS feed might be the cause of a small front-end issue related to image captions. Ana concluded that the spacing issue seemed separate from the newsletters/prices ticket and would create a new issue for it ([00:02:56](#00:02:56)).

* **Deployment and Technical Clarifications** Bohdan Vadimovich reported that the price converter migration was deployed, and a ticket for updating the display name is ready. Bohdan sought clarification from Cesar Paz regarding the monoblocks deployment option for WordPress dev instances, which Cesar explained involves choosing the monobox and the service to deploy WordPress, with deployment of progus being automatic ([00:04:11](#00:04:11)). Cesar noted that while the deployment is complete, there is a current problem accessing the box through the VPN, which Cesar is working on fixing. Bohdan is also working on a user deletion error that requires discussion with Nikola Pivcevic due to Nikola’s lack of approval for the current solution ([00:05:41](#00:05:41)).

* **Completed Tasks and Future Work** Brian Mendoza finished and moved a number of tickets to testing and plans to start the poly market WordPress work as well as preparing for election coverage video and WordPress content. Cesar Paz created a Confluence page explaining red boxes, deployed a new Graph dashboard without custom criteria, and added functionality to update the Docker image in the box ([00:06:57](#00:06:57)). Cesar also created a Confluence page about LWS cost and performed measures to reduce it, expecting a potential reduction of $5,000 to $7,000 in February. Brian mentioned having deployed the LX thing, expecting it to save another one or two thousand a month, which Cesar confirmed by noting a significant reduction in transfer size from one terabyte per day to maybe 200 or 300 GB ([00:08:19](#00:08:19)).

* **SEO and Content Improvement** Koray Baspinar is working on learn topics and the learn plan, while also checking category and tag pages with Matt because they contain many irrelevant tags and categories that might hurt SEO. Koray is compiling a list of unnecessary categories and tags. Koray confirmed that Brian is working on the "mention us in Google thing" ([00:09:32](#00:09:32)).

* **Stock Pages and Chart Functionality** Maryia Zhynko finished fixes for stock and ETF pages and is now working on adding a 'buy button' to aggregate stock, ETF, and token pages. Marina Lozuk is working on issues for the data dashboard page and improving the embedding of charts into articles to support different themes like dark or light. Marina raised a question about the priority of implementing a feature for downloading charts in real-time, noting that the current back-end solution presents implementation issues, and Edvinas Rupkus agreed to check with Matt on the priority of this feature ([00:10:41](#00:10:41)).

* **Poly Market Widget Prioritization** Edvinas Rupkus mentioned that the poly market contract was signed, making poly market widgets a top priority ([00:12:15](#00:12:15)) ([00:26:13](#00:26:13)). Marina Lozuk asked if they should defer the chart theme task to pick up poly market work. Brian Mendoza advised Marina to finish their current tasks first, as Brian is focusing on the WordPress implementation of poly market which requires troubleshooting and is not in a rush ([00:13:31](#00:13:31)).

* **Multicourse Support and Immediate Shifting of Priorities** Mikita Hulis and Nikita Orobenko reported a major shift in priorities due to a miscommunication about the new course format, which is incompatible with the current back end ([00:14:23](#00:14:23)). They are dropping other tasks, including payment setup, to implement extended CMI5 or X API support for the new course's interactive format. Nikita Orobenko emphasized the tight deadline, describing the situation as "Hunger Games" or "crypto IQ 2.0," with less than two weeks to implement the changes and avoid serious consequences ([00:15:34](#00:15:34)).

* **Plan and Implementation for Multicourse Support** Nikita Orobenko aims to formalize a high-level plan today and then move to back-end and front-end implementation. The issue is that the course will be interactive, requiring them to drop all current controlling logic for course navigation, as the course itself will handle this ([00:17:04](#00:17:04)). Mikita Hulis clarified that the issue stems from earlier miscommunication regarding timelines and requirements, and the focus must now be on implementing the necessary changes quickly ([00:18:30](#00:18:30)). The goal for the next two weeks is to finalize the plan today/tomorrow, start applying it, turn it over to QA before the 13th, and release it on the 13th to be ready by the 16th, postponing upsells and sales components ([00:19:35](#00:19:35)).

* **Additional Development Updates** Nikola Pivcevic fixed all Chroma-reported issues related to jobs and finished enabling the adding of charts to stock pages, though there is one dev box issue to resolve. Nikola also prepared a fix for an AMP pages issue and needs to sync up with Brian Mendoza on the solution. Nikola also started working on a report for broken external links, initially by sending notifications of possible broken links detected in recent articles to Slack ([00:21:07](#00:21:07)). Sean Winslow confirmed that any updates from Elmax would be forwarded to them from Edvinas Rupkus ([00:22:24](#00:22:24)).

* **Crypto Jobs and Release Strategy** Ramuald Vishneuski continues work on crypto jobs but will prioritize multicourse testing once it is on dev ([00:22:24](#00:22:24)). Ramuald noted that crypto jobs will be released alongside multicourses but will be hidden, as they do not want to waste time on cherry-picking and releasing untested changes. Edvinas Rupkus confirmed that as long as the crypto jobs don't show up on the front end, Matt is fine with the release strategy ([00:23:49](#00:23:49)).

* **General Updates and Priorities** Sean Winslow is working on campus voiceovers and tickets for release today or tomorrow, and also has an upcoming meeting with design ([00:23:49](#00:23:49)). Sean is also working on the job board, trying to find other companies to involve ([00:25:05](#00:25:05)). Edvinas Rupkus confirmed that the poly market contract signing means a shift in many development priorities ([00:26:13](#00:26:13)).

### Suggested next steps

- [ ] Sean Winslow will work on creating tickets related to the poly market stuff today.  
- [ ] Ana Benitez will create another ticket for the spacing issue between images and text on articles, as she thinks it is a separate issue.  
- [ ] Cesar Paz will try to fix the problem with the VPN and contact support through email if necessary.  
- [ ] Edvinas Rupkus will check with Matt regarding the priority of the issue about downloading charts for Marina Lozuk.  
- [ ] Sean Winslow will stay on top of decision foundry scheduling to make sure they carve some time out to test the rest of the forms that were not tested yet.  
- [ ] Edvinas Rupkus will write a ticket after the meeting for the error handling related to Salesforce forms.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=sT4rHYK6zTIQO-bHHxGtDxIUOAIIigIgABgDCA&detailid=standard)*

# 📖 Transcript

Jan 27, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Edvinas Rupkus:** Good reading sin.  
**Sean Winslow:** Sorry. Thank you, Alex, for the heads up. Ed, you can't help yourself. Even on vacation, you still got to attempt a daily standup.  
**Edvinas Rupkus:** Oh, I mean they miss you guys too  
**Sean Winslow:** Fair. Can't stop. Won't stop. All right. 10:01 13 people. All right. Yeah. So, let's begin. We'll start with  
**Aliaksandr Kryvanosau:** Hello.  
**Sean Winslow:** Alex.  
**Aliaksandr Kryvanosau:** So my main priority was the marketing page for individuals until yesterday call which switched to the enterprise marketing page. Beside that I did some some small adjustments to the jobs to the Salesforce and that's pretty much it. I was able to reuse some of the individual page work on the enterprise one. So the progress so far is okay. Okay. So, we should meet the deadlines.  
**Edvinas Rupkus:** Nice. How did the How did the test go with uh with Salesforce yesterday?  
**Aliaksandr Kryvanosau:** That's  
**Sean Winslow:** Perfect.  
**Edvinas Rupkus:** Did you did you test  
   
 

### 00:01:50 {#00:01:50}

   
**Aliaksandr Kryvanosau:** uh well there but they weren't able  
**Edvinas Rupkus:** it?  
**Aliaksandr Kryvanosau:** to test the compass one because they had the Salesforce issues on their side. We won't able to fetch the  
**Edvinas Rupkus:** Okay.  
**Aliaksandr Kryvanosau:** form.  
**Edvinas Rupkus:** Okay. Gotcha. All right.  
**Sean Winslow:** Yeah, I I think they're going to try to schedule another uh session, but I asked Lil to send me the recording just in case. All right, cool. I was going to ask Alex if you got anything out of that. It seemed like it was kind of just rolling along and I I wasn't really sure what we had to do with it.  
**Aliaksandr Kryvanosau:** Well, basically just watching how our like design implementation works and I noticed like a small bug with this error. The message doesn't stop the loader. So, we can fix it,  
**Sean Winslow:** Yeah,  
**Aliaksandr Kryvanosau:** but it's a pretty small issue.  
**Sean Winslow:** perfect. Thank you, Alex. Anna  
**Ana Benitez:** Um hello I am testing um fixes for data dashboard migration and frequently asked questions.  
   
 

### 00:02:56 {#00:02:56}

   
**Ana Benitez:** Um that's all uh also it while we have you here I wanted to ask you which ticket it is uh regarding the bug of spacing between images and and the text on articles.  
**Edvinas Rupkus:** Yeah, if you unhighlight Amma uh it should be under Brian. It's like it's like a text. Uh yeah, the first one in test.  
**Ana Benitez:** in testing.  
**Edvinas Rupkus:** The first one in test 44 26 that one.  
**Ana Benitez:** Oh, okay.  
**Edvinas Rupkus:** I believe I believe that's what they were referring to.  
**Ana Benitez:** No, I think this is like for the newsletters and in and prices. uh indices on on in articles and they're referring to a spacing between the the images and the the caption for the im.  
**Edvinas Rupkus:** caption.  
**Ana Benitez:** Yeah, the caption  
**Edvinas Rupkus:** Isn't that a new one?  
**Ana Benitez:** for  
**Edvinas Rupkus:** Do Do we always have the captions shown there? Cuz Cuz I know that Nicola just released like something for captions, right? Some sort of fig caption like thing for from the Yahoo RSS  
**Nikola Pivcevic:** Yeah. Yeah.  
   
 

### 00:04:11 {#00:04:11}

   
**Edvinas Rupkus:** stuff.  
**Nikola Pivcevic:** Could be like the cause of of the Yeah. the small uh issue. Yeah. On the front end.  
**Ana Benitez:** Okay. Okay. I'll take a look. I think it's a separate issue at so I'll create another.  
**Edvinas Rupkus:** Okay. Okay. Sweet.  
**Ana Benitez:** Thank you.  
**Edvinas Rupkus:** Thank you.  
**Sean Winslow:** Thank you. Well done.  
**Bohdan Vadimovich:** Uh yes hello there. So the uh price converter migration uh was uh finally deployed. Um also the ticket for uh updating display name. Um it's ready. Uh the only thing I wanted to clarify probably with Caesar uh for WordPress dev instances what option do we use for monoblocks uh uh deployment?  
**Cesar Paz:** Uh well I explained this to Nicola. Um basically we need to choose uh the monox and the service to deploy WordPress and that's all because automatically if you choose the monobox it's going to be deployed deploy progus. So now it's deployed. So now I'm working in the in in our VPN because we are having a problem.  
   
 

### 00:05:41 {#00:05:41}

   
**Cesar Paz:** So you can't access to that box right now. It's deployed. Um but we can't access to the VPN.  
**Bohdan Vadimovich:** Okay. So, sure. So, yes. So, the answer EK and uh so yeah, this this ticket is uh sorry, did I miss some kind of question from Caesar? probably I I just heard him here very Oh,  
**Cesar Paz:** No, no.  
**Bohdan Vadimovich:** okay. Sorry, it's just my internet is lagging right now. Uh and uh the next thing I'm also working on um deletion of a user error. Um but I guess this thing we need to discuss a little bit with Nicola because he didn't like my solution and yeah, we are going to uh deal with it. And that's pretty much it.  
**Sean Winslow:** Cool. Thank you. Well done. Yeah. And if you have any more questions, if your if your internet's lagging, just let us know, please.  
**Bohdan Vadimovich:** Um, no I think it's fine. I just I had like yesterday installed like new router and I think it's one or two days issue.  
   
 

### 00:06:57 {#00:06:57}

   
**Sean Winslow:** Okay, thank you. Bod Brian  
**Brian Mendoza:** Well, uh, I finished a lot of tickets, put them in testing. Uh, and I'm probably going to start the poly market WordPress stuff again and start thinking about all that, uh, uh, election covered stuff, video stuff, and WordPress stuff while these get tested and wrapped up.  
**Edvinas Rupkus:** Yeah, we definitely owe you tickets for that, but we'll eventually put them on your board.  
**Brian Mendoza:** No worries. I'm going to start the poly market thing anyway, so there's no rush on that.  
**Sean Winslow:** Okay, cool. Yeah, I I'll work on that today. Thank you, Brian.  
**Cesar Paz:** Hi.  
**Sean Winslow:** Caesar.  
**Cesar Paz:** Uh well uh I've created uh the conference page related to our red boxes to explain how our red boxes work. I created yesterday uh a new gram dashboard without the custom criteria. Um well in addition I added the functionality in the box to update the docker image. Um in addition I created a new conference page about the LWS cost. I did all the measures to reduce the cost.  
   
 

### 00:08:19 {#00:08:19}

   
**Cesar Paz:** So um I suppose well I expect uh this reduction in February. So I don't know exactly how much but maybe five six 7,000 less. Um, yeah, and that's all. Now, I'm trying to fix the problem with the VPN. Uh, probably I have to contact with them through the support email because I'm not sure how I can. Uh, sorry. And that's all. That's all.  
**Sean Winslow:** Okay. All right. Cool. Thank you, Caesar.  
**Cesar Paz:** Thank you.  
**Sean Winslow:** What's up,  
**Brian Mendoza:** Oh,  
**Sean Winslow:** Brian?  
**Brian Mendoza:** Caesar. Uh, I deployed the LX thing last night. That should be another thousand or two that we save a  
**Cesar Paz:** H yeah. Yeah. I checked it this morning.  
**Brian Mendoza:** month.  
**Sean Winslow:** All  
**Cesar Paz:** Um and I could say that uh yeah the the size the the transfer size is much less now. Instead of one terabyte by day it's maybe two or 300  
**Brian Mendoza:** Cool.  
**Cesar Paz:** GB. So that's fine.  
   
 

### 00:09:32 {#00:09:32}

   
**Cesar Paz:** It's cool.  
**Brian Mendoza:** Is it  
**Cesar Paz:** Perfect.  
**Sean Winslow:** right. Thank you, Cesar. Thank you, Brian, for mentioning that, Corey.  
**Koray Baspinar:** Hello. Uh I'm working on learn topics and uh learn plan. Uh and also uh I am checking our category and tag pages uh with Matt because uh there are some uh irrelevant a lot of irrelevant tags and uh categories uh not aligned with our website. I think it might hurt our SEO. So I am uh creating a list of uh unnecessary categories and tags and I'm working on that as well. Uh that's it. Yep.  
**Sean Winslow:** Perfect. Thank you, Corey. Did were you able to look at the um what we were discussing last week during your presentation uh what Ed mentioned the like mention us in Google thing? Did you see anything on that?  
**Koray Baspinar:** Yeah. Yeah. Yeah. Uh Brian is working on it.  
**Sean Winslow:** Oh, cool.  
**Koray Baspinar:** Yep.  
**Edvinas Rupkus:** Yeah,  
**Sean Winslow:** Perfect.  
**Koray Baspinar:** Yeah.  
   
 

### 00:10:41 {#00:10:41}

   
**Edvinas Rupkus:** I think it's like uh in test right now already,  
**Koray Baspinar:** Yeah. Yeah.  
**Edvinas Rupkus:** right?  
**Sean Winslow:** Nice. Hell yeah. All right. Thank you, Corey.  
**Maryia Zhynko:** Yep,  
**Sean Winslow:** Maria.  
**Maryia Zhynko:** I finished with uh fixes for stock and ETF pages and now I'm working on adding uh buy button to aggregate stocks, ETFs and uh token pages.  
**Sean Winslow:** Beautiful. Cool. Thank you, Maria. Marina.  
**Marina Lozuk:** Hello, I've been working on the issues for data dashboard page. Also, I pick up a tax task for improvements uh embedding charts into articles to support different team like dark or light one. Uh and also yesterday I looked at the issue or like maybe also improvements regarding downloading charts and I have a question whether we are going to tackle this issue or not and do we need to work on it because currently all those chat are generated on the back end site like vone or something like that and uh what was mentioned that they expect to be able to download chat in the real time like they will update uh um like uh filters and they'd like to get this chat.  
   
 

### 00:12:15 {#00:12:15}

   
**Edvinas Rupkus:** Yeah. Like what's visible basically on their screen instead of just  
**Marina Lozuk:** Yeah. what this yes I  
**Edvinas Rupkus:** the the  
**Marina Lozuk:** uh I've taken a quick look into that trying to implement it via like HTML to canvas something like that and there are some issues like it it wasn't like easy to make it up running and running and I'm just wondering whether I need to proceed working on that or we won't be fixing it. What shall I  
**Edvinas Rupkus:** Yep. Yeah. I can I can check with Matt.  
**Marina Lozuk:** do?  
**Edvinas Rupkus:** Do you think do you see a path forward or you still have to like investigate and and sort of like find a solution?  
**Marina Lozuk:** I need to I need to investigate as Nicola mentioned that we  
**Edvinas Rupkus:** Yeah.  
**Marina Lozuk:** can look at the like high chart expert functionality like get CSV something like that but I need to investigate whether it works because uh the solution which I had in my mind didn't play out well  
**Edvinas Rupkus:** Gotcha.  
**Marina Lozuk:** So,  
**Edvinas Rupkus:** I will uh I will ask Matt and where where that falls and in our like company priorities uh because the poly market the contract just got signed.  
   
 

### 00:13:31 {#00:13:31}

   
**Edvinas Rupkus:** So, we'll definitely want to start working on the poly market widgets,  
**Marina Lozuk:** Yeah,  
**Edvinas Rupkus:** but I'll I'll shoot them at Chilma text and I'll let you know if we should  
**Marina Lozuk:** it's yeah and uh like my second question do I need to like defer the task with improving supporting  
**Edvinas Rupkus:** uh  
**Marina Lozuk:** different theme for embedded chat and pick up poly market as Brian has already started working on that or I just need to finalize my task and then pick up poly market stuff based on the priorities.  
**Edvinas Rupkus:** Yeah. Uh, Brian, what part specifically are you starting to work on right  
**Brian Mendoza:** I don't worry about it, Marina, because I'm just like picking it up because I have nothing else to work on.  
**Edvinas Rupkus:** now?  
**Brian Mendoza:** Um, I'm just working on the WordPress implementation which had like they had like a hard step I had to figure out anyway. So, it's not like I'm going to move really fast and get it done today. Might take a day or two of QA and testing. So, finish your tasks.  
   
 

### 00:14:23 {#00:14:23}

   
**Brian Mendoza:** I'm not in a rush. Um, I can find other stuff to work on as well.  
**Marina Lozuk:** Okay, then probably I will finalize what I have on my plate and then we'll switch to poly market. But waiting uh for the response regarding expert, right? Like saving images because it can it can be time consuming I  
**Edvinas Rupkus:** Yep. Gotcha.  
**Marina Lozuk:** guess.  
**Edvinas Rupkus:** Yeah, I'll let you know for sure. And uh uh sounds  
**Marina Lozuk:** Yep,  
**Edvinas Rupkus:** good.  
**Marina Lozuk:** that's it.  
**Sean Winslow:** Cool. All right. Perfect. All right. Thank you, Marina. Nikita  
**Mikita Hulis:** Yep. So,  
**Sean Winslow:** Gulles.  
**Mikita Hulis:** similar to Alex's update, there was a quite a bit quite a bit of a shift uh in response to yesterday's call on the state of the uh multicourse support. uh due to some well pretty insane level of comm miscommunication uh it turned out to be that uh the format for the for the new course is not the one that is supported by our back end currently.  
   
 

### 00:15:34 {#00:15:34}

   
**Mikita Hulis:** So um yeah, we'll basically both me and Nikita drop everything uh uh well everything including the payment setup to jump ahead and uh do the extended version uh of the CMI5 support or X API uh to to support this sort of format and this sort of interactivity uh for the for the newly upcoming Of course, uh we have a pretty good idea uh of how we're going to achieve that. They will tell you more about it, but yeah, the next couple of weeks will be all about it. Uh rolling this one out and that's it.  
**Sean Winslow:** Okay, thank you. Yeah. Uh, you guys had the meeting with David.  
**Mikita Hulis:** Uh yeah, with David and later on with uh Matt and Mike and David also. Yep.  
**Sean Winslow:** Okay. Thank you, Nikita. Nikita O.  
**Nikita Orobenko:** Um, I would rather say no comments. Uh, it's uh kind of let the hunger games begin the  
**Mikita Hulis:** It's crypto IQ 2.0.  
**Nikita Orobenko:** crypto.  
**Mikita Hulis:** Let's everybody get get burned out.  
**Nikita Orobenko:** Yeah, I zero.  
   
 

### 00:17:04 {#00:17:04}

   
**Nikita Orobenko:** Uh, exactly except that for the crypto we had month and right now we have uh a bit less uh a bit more than just two weeks but we don't have any other options uh because otherwise uh if we won't be able to ship it uh according to the deadlines uh there will be consequences and they they're quite bad I would say. So um we're working on it. Uh the initial plan is already in my head. Uh the goal is to formalize at least the high level plan uh of the implementation and the adjustments later today and then we will switch to the actual implementations uh both the back end and the front end because uh the problem we did not understood that the course will be interactive and basically we we just need to drop uh everything that we do have on our side in terms of the controlling how you're going through the course switching between the lessons, the navigation, all that kind of things. That all of those will be handled by the the course itself.  
**Mikita Hulis:** Well, to be fair, like I would rephrase it from we we did not understand it to requirements were defined long ago and it was uh something different.  
   
 

### 00:18:30 {#00:18:30}

   
**Mikita Hulis:** It seems like in this in this case the person who was preparing the courses and we we were operating under the different different timeline s different uh requirements assumptions as well. So there was a certain level of miscommunication earlier down the line  
**Nikita Orobenko:** Yeah.  
**Mikita Hulis:** but now there is definitely no time to point fingers. We just need to to do this because we have no choice.  
**Nikita Orobenko:** Exactly. That was the thing I wanted to repeat myself from the retrospective uh from the crypto IQ 1.0. Not the time to point fingers. I don't care about it. Uh we have a deadline and we need to do the things and we need to ship it. So that's it.  
**Sean Winslow:** Okay. All right. Yeah, I appreciate that. Yeah, I'm I'm diving into a bunch of campus stuff myself. So, but let me know if there's anything I could do to help and try to communicate with other  
**Nikita Orobenko:** I don't think that anything will change at that moment uh already because we  
   
 

### 00:19:35 {#00:19:35}

   
**Sean Winslow:** people.  
**Nikita Orobenko:** don't have a time to change anything. Uh the only thing we're just postponing uh the the upsells uh the sales part uh because we  
**Mikita Hulis:** everything a part of the core multicourse functionality to support 2011 for the  
**Nikita Orobenko:** just  
**Mikita Hulis:** LMAX. That's the whole agenda for the next two weeks. The plan is to finalize the idea and the plan today slash tomorrow morning and start uh start applying it. Uh then sometime before 13th, a few days before 13th, uh we will uh turn it out to the QA and the release would probably be on well the last Friday before 16th which would be well 13\. Yeah. And it should be released then to be ready on 16th which is which is  
**Sean Winslow:** Okay. All right. Thank you for all those updates. I was very curious if there was any follow-ups to yesterday. So, I appreciate that, guys. Nicola  
**Nikola Pivcevic:** Uh yeah, hello everyone. Uh so um um jobs so fixed all the issues that Chroma uh reported.  
   
 

### 00:21:07 {#00:21:07}

   
**Nikola Pivcevic:** Uh we'll see if he comes up with new stuff. Uh and um finished. Yeah, sorry. If you scroll up, uh finished the uh enabling this adding any chart stock pages. Uh there is one issue with the dev box. So I need to fix that before moving to ready for testing. Um uh yeah and uh prepared like a small fix which I don't know I need to like talk to Brian a bit like we have this AMP issue with AMP pages so prepared the fix for it. will uh but Brian also like kind of worked on it a bit and like yeah we need to I guess u uh work together and sync up on on on the solution and um yeah uh looked today into the report for broken external broken links and uh yeah kind of just the first part where we send a notification of a possible broken link detected. it u for just recent articles in Slack. Uh and uh that's  
**Sean Winslow:** Cool. Thank you, Nicola.  
**Nikola Pivcevic:** it.  
   
 

### 00:22:24 {#00:22:24}

   
**Sean Winslow:** And yeah, um I'm sure you and Ed have talked about it, but if any updates come from Elmax, Ed's just going to forward it straight to me and then I'll talk to you about it.  
**Nikola Pivcevic:** Okay, I'm good.  
**Sean Winslow:** Right,  
**Edvinas Rupkus:** Yep.  
**Sean Winslow:** Ronald?  
**Ramuald Vishneuski:** Uh hello team. Uh so I continue my work with crypto jobs. Uh but I will uh skip that right now because um uh now we have different priorities and uh I'm waiting when um multicourses will be on dev and I will start u uh testing it immediately. Uh it's not ready completely. So as Nikita's above Nikita said uh but uh uh these apart uh for me to test. So I I will uh start now and uh uh we'll wait uh uh for the update from there. Um and yeah, that's mostly all.  
**Sean Winslow:** Okay, thank you, Roma. Yeah, I know there's a lot of lot of changes in shifts right now, so I appreciate everyone's tenacity and able to everyone able to move and shift.  
   
 

### 00:23:49 {#00:23:49}

   
**Sean Winslow:** So,  
**Ramuald Vishneuski:** And um by the way um seems like we will uh release crypto jobs v um multouruses but it will be hidden because uh everything is on devbox and uh like we don't want to waste time on cherry picking and making some um uh releases that were untested. That's why we will release everything  
**Edvinas Rupkus:** Y sounds good.  
**Ramuald Vishneuski:** here.  
**Edvinas Rupkus:** I I checked with Matt and he said as long as it doesn't show up on the front end, he doesn't care. Like, you know,  
**Ramuald Vishneuski:** Yep.  
**Edvinas Rupkus:** if if the back end doesn't have any jobs and doesn't show up on the front end, he doesn't care.  
**Sean Winslow:** Awesome.  
**Ramuald Vishneuski:** Yeah.  
**Sean Winslow:** Thank you, Roman. And uh Yer Yermeck uh pinged me. He said he's going to be skipping this one, but he didn't have any updates. Um updates on my end. I am also working on the campus stuff with David, trying to get the voiceovers done. I'll be focusing on the tickets to get those out today or tomorrow morning.  
   
 

### 00:25:05 {#00:25:05}

   
**Sean Winslow:** And yeah, and then I have a meeting with design to look into other things that I'll update you guys on tomorrow or later this week. And that's it on my end. And I'm also doing some job board stuff for eventually what will become the back end. Trying to find other other companies that we should involve on the actual job boards. So Ed, anything on your end?  
**Edvinas Rupkus:** Nothing specific. Uh I replied to a bunch of questions on Jira yesterday. Let me know if it was like for job boards and for um I forget if some few other uh initiatives too. Let me know if if what I what I replied with made sense. Uh I think Serena provided some VQA for the job boards. Alex, I think you I don't know. Let me know if you didn't see that the directive that she proposed. That sounded pretty good to me for the  
**Aliaksandr Kryvanosau:** Sorry, where?  
**Edvinas Rupkus:** titles like the spaces the how many lines for each of Yeah.  
   
 

### 00:26:13 {#00:26:13}

   
**Aliaksandr Kryvanosau:** Okay.  
**Edvinas Rupkus:** Okay, sweet. Yeah, nothing specific for my end. If anything, I'll just uh I'll ping ping you guys. But yeah, basically the gist is that poly market contract got signed. So a lot of these things will shift into dev now. Um so that's basically top of mind.  
**Sean Winslow:** All right, perfect. Thank you, Ed. Uh, does anybody else have things that they want to bring up? Any comments, questions, concerns?  
**Aliaksandr Kryvanosau:** Yes, I just recall uh add a question to you about the Salesforce.  
**Sean Winslow:** We got  
**Aliaksandr Kryvanosau:** Um when are we planning to test them ourselves and release them?  
**Edvinas Rupkus:** uh whenever like the testing is complete like if they you know patched up all the different kind of inconsistencies with the data flows. Uh we definitely are we have a sort of like a hard deadline to deprecate Marquetto  
**Aliaksandr Kryvanosau:** No.  
**Edvinas Rupkus:** by February 12th. So, we sort of should be done by then.  
**Aliaksandr Kryvanosau:** So, we're just waiting on their side  
**Edvinas Rupkus:** Uh, yeah, we yeah,  
   
 

### 00:27:29

   
**Aliaksandr Kryvanosau:** testing.  
**Edvinas Rupkus:** we need to like but hopefully this week we can we're able to test the last campus form and I think I still owe you the ticket to like handle the error states for all the forms, right? because we want to unify that and after that I  
**Aliaksandr Kryvanosau:** Yeah.  
**Edvinas Rupkus:** think there's nothing else preventing us from shipping it we can just you know prep it for a waiting deploy  
**Aliaksandr Kryvanosau:** And we're going to test it ourselves to see that we didn't have new as much matches with the design.  
**Edvinas Rupkus:** yeah I think we definitely should uh spin it through this QA cycle if we have the capacity bandwidth uh we can you know do VQA as well but I I don't I don't think it's needed I think as long as especially those other three forms that don't get as much traction uh as long as they're function they're functioning and they're they're sending data to Salesforce and we get rid of Marquetto that's all that matters. So yeah, Sean, let's let's stay on top of um decision foundry scheduling to make sure that we carve some time out to test the rest of the forms that weren't tested  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** yet.  
**Sean Winslow:** Yeah, I'm on that Slack channel. So, and I I was just talking to Lil this morning, so I'll make sure on top of  
**Edvinas Rupkus:** Sweet. Yep. Yeah, I'll I'll defin I'll write a ticket uh after this for the like error handling.  
**Sean Winslow:** it.  
**Edvinas Rupkus:** Alex  
**Aliaksandr Kryvanosau:** Okay, thanks. That's great to know the plan.  
**Sean Winslow:** Cool. Thank you, Alex. Thank you, Ed. Anybody else?  
   
 

### Transcription ended after 00:29:54

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*