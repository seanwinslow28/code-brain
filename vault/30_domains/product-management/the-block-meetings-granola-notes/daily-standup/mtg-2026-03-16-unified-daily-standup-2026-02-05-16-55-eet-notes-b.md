---
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup - 2026_02_05 16_55 eet - notes by gemini.
context: the-block
created: 2026-03-16
source: granola-manual
---

# 📝 Notes

Feb 5, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivcevic](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Vadimovich](mailto:bvadimovich@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~ ~~[Yermek Smagulov](mailto:ysmagulov@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMDVUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.r4kuwbcxb6x5) 

### Summary

**Content and Pricing Migration Status**  
Updates were provided on the marketing page endpoint requirements and ongoing price migration, while the new podcast deployment is paused pending final quality assurance sign-off from the design team.

**System QA and Service Updates**  
System maintenance tasks are nearing completion, including finishing checks on Salesforce emails and completing credit card service updates, though some support contact is still required. QA was finalized for several existing pages and the Poly Market task, while front-end work on Poly Market UI continues.

**Missing Content Blocks Course Release**  
The course template is mostly finalized, but the entire course import and release are at significant risk due to critical content—specifically test questions—missing from the research team. A decision was made to escalate the content issue immediately to Matt to ensure the research team meets the necessary deadlines.

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

NEEDS FURTHER DISCUSSION

**Poly Market data retrieval improvement**

Improve method retrieving data from Poly Market, potentially improving search mechanism. Marina Lozuk check relevance on dev box, comment on tickets.

ALIGNED

**WordPress image integration process**

Aliaksandr Kryvanosau try production WordPress instance access images; Brian Mendoza upload images, provide URLs if production access fails.

**Wallets keys ticket deployment**

Wait for Jerick return deploy wallets key tickets.

**Task updates communication standard**

Cesar Paz keep Sean Winslow in loop regarding all updates requested by Lil.

**Individual marketing page release**

Individual marketing page newest version omission possible for 16th release, not priority compared to teams version.

**Research team question completion**

Sean Winslow talk to Matt ensure research team double down providing missing course questions before deadline, critical for course import.

**White papers podcast deployment**

Hold off deploying White Papers podcast, wait for design team QA approval.

*More details:*

* **Multicourse and Marketing Page Updates** Aliaksandr Kryvanosau reported that they were able to get the model for the marketing page but require a new endpoint from compass to view the video, which Nikita Orobenko is preparing. Aliaksandr Kryvanosau is also working on a PR comment from Brian Mendoza regarding getting images from WordPress, which currently presents a local issue ([00:00:00](#00:00:00)). Brian Mendoza suggested that Aliaksandr Kryvanosau try logging into WordPress in production or that they could upload the images if issues persist ([00:02:30](#00:02:30)).

* **Price Migration and Podcast Status** Ana Benitez is continuing with prices migration, addressing comments on the FAQ section and moving through other sections and pages. For the new podcast, Ana Benitez confirmed that everything looks good but is waiting for Serena from design to complete the QA process for the landing page. Sean Winslow acknowledged the update, confirming that the team is waiting for the design's "good to go" ([00:03:19](#00:03:19)).

* **Contributor Field Logic and QA** Bohdan Vadimovich stated that the ticket for the new contributors field logic is almost ready, requiring only proper testing ([00:03:19](#00:03:19)). Brian Mendoza reported finishing QA for the events and some other pages, which they might deploy later today, and completed the Poly Market task. Ana Benitez inquired about deploying wallets key on tickets and if they should wait for Jerick, which Brian Mendoza confirmed, expecting Jerick's return on Monday ([00:04:38](#00:04:38)).

* **Credit Card Services and Salesforce Emails** Cesar Paz completed almost all services to update credit card information and ripping but needs to contact the support team for some services because direct changes through the interface are not possible. Cesar Paz also finished all checks on Salesforce emails, a task requested by Liil, and is aiming to complete this work soon to start new tasks next week ([00:05:32](#00:05:32)). Sean Winslow asked Cesar Paz to keep them in the loop on those tasks for Lil ([00:06:46](#00:06:46)).

* **Monthly Report and All Hands Presentation** Koray Baspinar focused on their monthly report and presentation for the all hands meeting. Sean Winslow congratulated them on presenting during the all hands ([00:06:46](#00:06:46)).

* **FAQ Issues and Poly Market UI** Maryia Zhynko is working on fixing issues within the FAQ section on the individual price page. Sean Winslow mentioned writing tickets for the election hub and confirmed that Maryia Zhynko will have more work once final design iterations are confirmed. Marina Lozuk is still busy with Poly Market UI, working on the table widget using a flag provided by Brian Mendoza and implementing mobile fixes for the progress bar on the single market widget ([00:07:55](#00:07:55)).

* **ECMI 5 Player and Course Template Finalization** Mikita Hulis is polishing the ECMI 5 player and adjacent setup, ironing out final quirks with the combination of old and new setups, and ensuring the original URL structure is preserved ([00:09:09](#00:09:09)). Nikita Orobenko stated that the course template is mostly finalized but is missing questions for tests and checkpoints, which were expected from Gabe today as the latest deadline. Nikita Orobenko emphasized that the missing questions are blocking the course import and pose a risk to the release ([00:10:28](#00:10:28)) ([00:14:20](#00:14:20)).

* **Marketing Pages Endpoints and Release Planning** Nikita Orobenko confirmed working on endpoints for Aliaksandr Kryvanosau for the marketing pages. The team discussed the release plan for the individual marketing page newest version, with Mikita Hulis confirming it is not a priority for the 16th release, a statement Sean Winslow attributed to Matt. Nikita Orobenko also synced with Dave on redirects and events adjustments for lesson start and end to enable proper progress syncing ([00:11:58](#00:11:58)).

* **Addressing the Missing Questions and Research Team Communication** Sean Winslow expressed concern about the missing questions from Gabe and planned to reach out to Matt to encourage the research team to double down on providing the necessary content, noting that David spoke with Stephen, who only commented on minor details like font placement instead of the questions themselves. Nikita Orobenko stressed the need for the research team to meet the deadline, especially since the team adjusted to a quick gear switch three weeks before the release ([00:13:07](#00:13:07)) ([00:15:33](#00:15:33)).

* **Fixes and External Links Cleanup** Nikola Pivcevic deployed a small fix for an app related to the Layer 1 link and prepared another small fix for AMP that is ready for review ([00:15:33](#00:15:33)). They are also looking into cleaning up existing broken external links as part of phase two, with the notifier currently in QA. Nikola Pivcevic shared the video plugin name with Sean Winslow, who plans to research it and coordinate with the media team ([00:16:43](#00:16:43)).

* **Podcast Deployment Status** Ana Benitez and Nikola Pivcevic discussed the deployment of the white papers podcast, confirming they will hold off until design gives the official approval to avoid unexpected issues during deployment. Sean Winslow agreed to wait for the design sign-off ([00:17:58](#00:17:58)).

* **Campus Work and Research Team's Python Script** Ramuald Vishneuski is working on campus ([00:19:01](#00:19:01)). Sean Winslow shared that they are trying to help David with graph animations and asked if anyone knew what kind of Python script the research team uses, but Brian Mendoza indicated a lack of knowledge regarding the research team's processes . Sean Winslow plans to experiment with something over the weekend to help David .

### Suggested next steps

- [ ] Brian Mendoza will upload the images for Aliaksandr Kryvanosau and provide all the URLs if Aliaksandr Kryvanosau is unable to log into WordPress in production.  
- [ ] Brian Mendoza will wait for Jerick on Monday or whenever he is back before deploying the wallets key on tickets.  
- [ ] Cesar Paz will keep Sean Winslow posted on the tasks related to updating the credit card for services.  
- [ ] Sean Winslow will talk to Matt to see if the group can get research to double down on providing the questions for the courses.  
- [ ] Sean Winslow will update the group once the information about the tickets is obtained.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=5JKobzGkZsfQC9jCe5MADxIWOAIIigIgABgDCA&detailid=standard)*

# 📖 Transcript

Feb 5, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Maryia Zhynko:** Hello.  
**Nikita Orobenko:** Anyways,  
**Sean Winslow:** What's up, kid? Give people another minute. All right, we can get started. We will start with who else? We'll start with Alex.  
**Aliaksandr Kryvanosau:** Nothing new. Well, same old same old for me. Multicourses and marketing page. I was able to get the model but to see the video I need a new endpoint from compass. So already connected with Nikita O on that matter and this end point will be ready soon. Then I got a comment in PR for this ticket from Brian. So I investigated to get images from the WordPress. So I tried to do this but my local stuff with WordPress doesn't work. So I've been trying to resolve it  
**Sean Winslow:** So,  
**Aliaksandr Kryvanosau:** mainly.  
**Sean Winslow:** so you have to get images from WordPress but it's not something locally is not working. You said what's  
**Aliaksandr Kryvanosau:** Yep. Correctly.  
**Sean Winslow:** up  
**Brian Mendoza:** I would upload them in production. Um, you should have access.  
   
 

### 00:02:30 {#00:02:30}

   
**Brian Mendoza:** If not, I can upload them for you, but yeah, I do think we want to try to use them hosted in our uh stack like on production. So, if you're having issues on local, try to Have you ever uh are you able to log into WordPress in production?  
**Aliaksandr Kryvanosau:** But  
**Brian Mendoza:** Have you tried that before?  
**Aliaksandr Kryvanosau:** uh I'm not sure about production but I am able to login on the  
**Brian Mendoza:** Cool. Try it on the VPN with that link I linked in the PR,  
**Aliaksandr Kryvanosau:** debox.  
**Brian Mendoza:** the WP.theblock.co. If it doesn't work, I'll I'll update them for you and give you all the URLs.  
**Sean Winslow:** Cool.  
**Brian Mendoza:** But yeah, let me know if it doesn't work for you, though.  
**Aliaksandr Kryvanosau:** Okay. But I still would like to play around with it locally to see how it works.  
**Brian Mendoza:** Cool. Sounds good.  
**Aliaksandr Kryvanosau:** Thanks.  
**Sean Winslow:** Nice. Yeah, let let us know if you run into any more issues. I'll try to help too if possible. But thank you,  
   
 

### 00:03:19 {#00:03:19}

   
**Aliaksandr Kryvanosau:** Thanks.  
**Sean Winslow:** Alex. You're welcome, Anna.  
**Ana Benitez:** Um hello I am still on prices migration so there were some comments on frequently asked questions and I'll continue through all the other sections and pages um and also for the new podcast um I think everything looks good uh we're just waiting for design to come back on the landing page uh but so far it's looking good That's hope for  
**Sean Winslow:** Cool. You said you're waiting for design. Did you reached out to design or there's something that's still not completed on design  
**Ana Benitez:** Uh I reached out uh to Serena to complete the QA.  
**Sean Winslow:** stud?  
**Ana Benitez:** So she's just going to give the uh good to go I  
**Sean Winslow:** Gotcha.  
**Ana Benitez:** guess.  
**Sean Winslow:** Cool. Thank you, Anna.  
**Ana Benitez:** Thank  
**Sean Winslow:** Well done.  
**Bohdan Vadimovich:** Yes. Uh hello there. So the ticket for that uh new field contri contributors uh logic uh is um uh almost ready. I just need to test it out properly and uh yeah so something like this.  
   
 

### 00:04:38 {#00:04:38}

   
**Sean Winslow:** Cool. All right. Nice. Yeah. Thank you,  
**Brian Mendoza:** Cool. Um, and I finished QAing the events and some other pages,  
**Sean Winslow:** Brian.  
**Brian Mendoza:** so I might try to deploy them later today. And I also finished the Poly Market thing. Um, I believe it's fine, Marina. Uh, if there's any issues, let me know. And then I'm going to work on some of the other stuff and move around. Oh  
**Sean Winslow:** Cool.  
**Ana Benitez:** Um, regarding that, Brian,  
**Brian Mendoza:** yeah.  
**Ana Benitez:** um, there's also these wallets, key on tickets that are ready, but should we wait for Jerick on that or  
**Brian Mendoza:** Yes, probably.  
**Ana Benitez:** what?  
**Brian Mendoza:** Good. Good call. Yeah, I was going to probably do that.  
**Ana Benitez:** Okay.  
**Brian Mendoza:** I'll wait for your M on Monday or whenever he's back.  
**Ana Benitez:** Thank you.  
**Sean Winslow:** Yeah, I think it's on Monday.  
**Brian Mendoza:** Um,  
**Sean Winslow:** And I didn't see Did Matt uh reply to your last message?  
**Brian Mendoza:** no.  
   
 

### 00:05:32 {#00:05:32}

   
**Sean Winslow:** Was it separate?  
**Brian Mendoza:** But I'm pretty sure I'll It's like a oneliner just to change it if he does want to change it. I'll just change it from like 48 hours to like a minute or something. So, we'll see.  
**Sean Winslow:** Okay, sounds good. Thank you, Brian. Caesar.  
**Cesar Paz:** Hi. Uh again, not much about me. Um yesterday I completed almost all the services uh uh in order to update the credit card uh and rippling but I need to talk with the support team of some of these services because it's not possible to change directly uh in the interface. Um, I finished two or at least I believe I finished uh all checks in all about the all force Salforce emails because Liil told me to check all these emails to to check if we need to change something in our configuration. Uh yeah, keep working in this task. Uh now I'm going to I hope finishing this one today or tomorrow and start next week with new task. Uh that's  
   
 

### 00:06:46 {#00:06:46}

   
**Sean Winslow:** Cool. Awesome. Thank you. Yeah,  
**Cesar Paz:** all.  
**Sean Winslow:** keep me posted uh on those tasks because I know Lil is asking for a lot of updates. I'm sure you could just talk to us uh directly, but I would just like to be in the loop if possible.  
**Cesar Paz:** Okay. Of course.  
**Sean Winslow:** Cool. Thank  
**Cesar Paz:** Thank you.  
**Sean Winslow:** you, uh Corey.  
**Koray Baspinar:** Uh hello uh I today I must be worked on my uh monthly report and presentation for the all hands. Uh that's it. Sure.  
**Sean Winslow:** Oh, you presented during the all hands.  
**Koray Baspinar:** Yeah.  
**Sean Winslow:** Wow, look at that.  
**Koray Baspinar:** Really excited.  
**Sean Winslow:** Very exciting. All right. So, yeah. So,  
**Koray Baspinar:** Yeah.  
**Sean Winslow:** yeah, focus on that. That's very important. Thank you for all the updates.  
**Koray Baspinar:** Yeah. Thanks,  
**Sean Winslow:** I appreciate it, Maria.  
**Maryia Zhynko:** Today we're working on fixing some issues with FAQ section on individual price page.  
**Sean Winslow:** Cool.  
   
 

### 00:07:55 {#00:07:55}

   
**Sean Winslow:** Yeah, thank you. Yeah, I appreciate anybody. I'm I'm writing up the tickets for the election hub. Uh I'm just waiting on the final design iterations. I I believe they're done, but I'm just confirming with Serena now. And then we'll have I'll have more stuff for you, uh Maria. But I appreciate everybody, you know, or just like you're you taking on other work or the delegation of work.  
**Maryia Zhynko:** Yep. Okay.  
**Sean Winslow:** Thank you, Marina.  
**Marina Lozuk:** Hello. Uh, I'm still busy with the poly market UI stuff. Today I worked on the table widget and the implementing using flag that Brian provided me with yesterday and also I worked on the like progress bar for single market widget. So work it on the mobile fixes. So probably that's it.  
**Sean Winslow:** Cool. Yeah. And everything uh looks good. Any more questions on your end about the tickets  
**Marina Lozuk:** No question.  
**Sean Winslow:** or  
**Marina Lozuk:** Maybe the the only one is regarding the like the way I I retrieve data from the poly market, right?  
   
 

### 00:09:09 {#00:09:09}

   
**Marina Lozuk:** I've also added the task, but it will be easier to check it as soon as I create the dev box to to see whether it's like uh relevant ones or not relevant. And maybe we need to improve the way of we doing it like the way we search it. Maybe it's only currently it's only one concern which I  
**Sean Winslow:** Okay,  
**Marina Lozuk:** have.  
**Sean Winslow:** cool. Yeah, if if you have any questions, yeah, just keep on commenting on the tickets.  
**Marina Lozuk:** Yep.  
**Sean Winslow:** Thank you. Mike here. No, Nikita Gulis.  
**Mikita Hulis:** Uh, yep. Update pretty much the same for me as yesterday. Uh, polishing the polishing the ECMI 5 player and adjacent setup. Uh, ironing out the last quirks with the combination of the old and the new setup, hiding all of the things in like exclusive things for one or the  
**Sean Winslow:** Cool.  
**Mikita Hulis:** other. Basically, for example, so that navigation is not being displayed uh for the interactive player while it's still being uh there for the regular version, etc., etc. There are quite a few of those.  
   
 

### 00:10:28 {#00:10:28}

   
**Mikita Hulis:** The main goal here is to preserve our original URL structure so that the new player is just integrated into it without uh like messing up the current setup. keeping trying to keep as much uh default stuff as possible. And that's about it.  
**Sean Winslow:** Yeah, I sp I spoke with David this morning. Did uh did you guys have a meeting today?  
**Nikita Orobenko:** We did.  
**Sean Winslow:** You did.  
**Nikita Orobenko:** Yeah.  
**Sean Winslow:** So, yeah. So, on that note, let's go to Nikita O.  
**Nikita Orobenko:** Uh yeah. So mostly the the template for the course is kind of finalized except we're still missing the questions uh for the tests and for the checkpoints. Uh, as it was said before, today is kind of the latest day for the Gabe to to pick them up. Uh, I know that the Gabe is in PDO and traveling and it's a bit problematic to pick those questions on the train, but I hope that tomorrow they will be there. uh otherwise we starting to have uh a little risks I would say cuz uh the rest of the things are either finished or not that important cuz those things are definitely blocking us from importing the course and making it work.  
   
 

### 00:11:58 {#00:11:58}

   
**Nikita Orobenko:** I mean we can do some tricks but we still f\*\*\*\*\*\* need that course anyway. So uh those tricks are not that won't be that helpful uh to be honest and yeah working on a few uh end points uh for Alex for the marketing pages. Um the quick question are we planning to release the individual uh marketing page newest version along with the teams version or just the team one uh for the 16th release?  
**Mikita Hulis:** I think it was mentioned on the call that it is not a priority and can be omitted for the 16\.  
**Nikita Orobenko:** Okay.  
**Sean Winslow:** Yeah. Yeah. That's that's what Matt said.  
**Nikita Orobenko:** Okay.  
**Sean Winslow:** He said he he was talking about Poly Market would only care about the team ones.  
**Nikita Orobenko:** Mhm.  
**Sean Winslow:** So  
**Nikita Orobenko:** Okay. Um and yeah uh we sync with uh Dave uh also on the redirects after finishing up the core the subject. So since the template is kind of already finished, we were able to prepare the links for him. So he will set up the redirects uh after the subjects will be completed.  
   
 

### 00:13:07 {#00:13:07}

   
**Nikita Orobenko:** Plus he's working on adjusting a little the events that the uh will be sent uh on the lesson start and the lesson end. So we will be able finally uh sync uh the progress properly because that's also an important thing for us. Uh, and I think that's kind of it for now on my  
**Sean Winslow:** Okay, cool.  
**Nikita Orobenko:** ends.  
**Sean Winslow:** Yeah, I wish I wish there was some way I could, you know, work on Gabe stuff, but I don't I don't really know exactly what is required of him. So, but I'm working on some of the some of the other details like um getting icons and some of the animation stuff. So,  
**Nikita Orobenko:** No,  
**Sean Winslow:** but  
**Nikita Orobenko:** I I I mean like the the whole thing about the game I suppose is that once the companywide testing will be started and if somebody from the research team will see that the questions are not correctly picked uh it will start it will quickly start smelling uh a bit not good uh and everybody will start writing down their grandma's wishes in terms of what we need to fix and what we need to adjust.  
   
 

### 00:14:20 {#00:14:20}

   
**Nikita Orobenko:** Uh a beautiful phrase I heard first time in my life from Dave today uh about wishes. Uh but it it will be like that to be honest. So they are responsible for the question.  
**Sean Winslow:** Yeah.  
**Nikita Orobenko:** So let them be responsible but also we still have the deadline and their responsibility doesn't change anything.  
**Sean Winslow:** Yeah, agreed. And I I would think that they know the, you know, like how serious this is, but we'll we'll see.  
**Nikita Orobenko:** Let us maybe remind quickly how this is important and if at first it's  
**Sean Winslow:** Yeah.  
**Nikita Orobenko:** important uh how much it  
**Sean Winslow:** Yeah, exactly. I think I I'll probably reach out to Matt to like,  
**Nikita Orobenko:** costs.  
**Sean Winslow:** you know, get them on top of everything. Uh because yeah, I don't know if I'm sure David has as well, so I I don't want to keep on proddding, but if if like research apparently David did speak with Stephen about like some of the some of the courses and Stephen wasn't really pointing out the questions themselves, so he was like, "All right, I guess that's that means it's good." He was just pointing out some of the the font placement or something like  
   
 

### 00:15:33 {#00:15:33}

   
**Sean Winslow:** that. So, yeah, we'll see. But yeah, I'll I'll talk to Matt to see if we can get research to double down.  
**Nikita Orobenko:** Yeah, cuz I I mean like in the in this situation uh if we were able to quickly switch gears uh just 3 weeks before the f\*\*\*\*\*\* release. So, I do really want to see and expect the same thing from the other side cuz we are on the same boat this  
**Sean Winslow:** Agree.  
**Nikita Orobenko:** time.  
**Sean Winslow:** I very much agree, Nikita. Yeah, I'll let you know what Matt says.  
**Nikita Orobenko:** Okay. Yeah. Thank you so much.  
**Sean Winslow:** You're welcome. Thank you, Nicola.  
**Nikola Pivcevic:** Uh yeah hello everyone. So uh today deployed like a small fix for uh for uh what was it app for the lay layer one like um link and also prepared a small small another fix for AMP which is ready for review. Uh Brian, I just tagged you recently and uh yeah, so I'm kind of waiting. So didn't know exactly how to proceed on the video thing.  
   
 

### 00:16:43 {#00:16:43}

   
**Nikola Pivcevic:** So I guess like Sean, we are still waiting on like direction. Uh so in the meantime, I was looking at um uh broken external links. So the this notifier is in in QA but like this other thing that we need to clean up existing broken links, right? This is just like this is like part phase two of this cleanup.  
**Sean Winslow:** All right. What What's the name of that video link by the way? the plugin rather  
**Nikola Pivcevic:** It's um just a second  
**Sean Winslow:** because part part of the uh part of the tickets that I'm writing it does incorporate the aspect of like bringing in the media. So if if I just know what this plugin does, I can start doing my own research and then bring it up to uh the media team seeing exactly what they have in mind for exports and stuff like that and I'll be able to combine those and then  
**Nikola Pivcevic:** there.  
**Sean Winslow:** yeah and then we can eventually meet to actually discuss everything in detail.  
**Nikola Pivcevic:** Yes. So, I just shared it here like I don't know if you saw it in in  
   
 

### 00:17:58 {#00:17:58}

   
**Sean Winslow:** Got it.  
**Nikola Pivcevic:** the  
**Sean Winslow:** Awesome. So yeah, so I I'll keep you posted on that,  
**Nikola Pivcevic:** Okay. And sorry,  
**Sean Winslow:** Nicola.  
**Nikola Pivcevic:** wanted to ask like I see the white papers podcast is ready for deployment. Do we deploy like what's the  
**Sean Winslow:** Uh I think Anna, weren't you saying that we have to wait for um  
**Ana Benitez:** So, yeah.  
**Sean Winslow:** design  
**Ana Benitez:** Yeah, it's almost ready. Nicola, um, do we want to release this as soon as it's  
**Nikola Pivcevic:** I don't know. Same same for  
**Ana Benitez:** ready?  
**Nikola Pivcevic:** me.  
**Sean Winslow:** Yeah, I I think we'll we'll hold off. We'll wait for design to actually give us the okay and but I think I mean it's it seems like something that's been done multiple times before, especially with layer 1\. So, it seems like it's just another day, but we'll see. I I want to double check to make sure that we're all good. I I don't want to start deploying things and then we suddenly have something else that was supposed to be done, but Okay.  
   
 

### 00:19:01 {#00:19:01}

   
**Nikola Pivcevic:** Yeah. Yeah.  
**Sean Winslow:** Yeah.  
**Nikola Pivcevic:** I just want to ask like what's the status? I'm I'm in no hurry to deploy this.  
**Sean Winslow:** Okay,  
**Nikola Pivcevic:** Okay.  
**Sean Winslow:** cool. All right. Thank you, Nicola. And yeah, I'll get back to you on the details of those tickets.  
**Nikola Pivcevic:** Sounds good. Thank you.  
**Sean Winslow:** You're welcome. Rald.  
**Ramuald Vishneuski:** Hello. Um, I'm working on campus right now and that's  
**Sean Winslow:** All right.  
**Ramuald Vishneuski:** all.  
**Sean Winslow:** Short and sweet. Dig it. Campus overall. Uh yeah. All right. So, um updates on my end. I pretty much spoke about it uh throughout, but it's helping out David. And oh, actually, I had a question. Does anybody know uh what kind of Python script the research team uses for to like create the animations like the like the graph animations? Has anybody ever come across any of those? No.  
**Brian Mendoza:** I think in general we have no idea what they do or how they do things. Black  
**Sean Winslow:** I think if we establish anything during this meeting,  
**Brian Mendoza:** box.  
**Sean Winslow:** it's very much we are in in a bubble and they are or they're in a bubble and we're outside it. So, but yeah,  
**Brian Mendoza:** Yeah.  
**Sean Winslow:** I'm I'm just going to start messing around uh to help David out to see because what what he was getting wasn't very good. So, I'm going to see if I can mess around with something this weekend. But yeah, those are my updates and yeah, a nice a nice quick one, but I'll see everyone at the all hands and give Corey a nice congratulations. We'll be seeing him at the all hands as well. Good luck, Corey.  
**Koray Baspinar:** Thanks guys.  
**Sean Winslow:** All right, so yeah, so I'll see everyone there and I'll update everyone once I get the information about all the tickets and everything like that. So I appreciate it, guys.  
   
 

### Transcription ended after 00:21:04

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*