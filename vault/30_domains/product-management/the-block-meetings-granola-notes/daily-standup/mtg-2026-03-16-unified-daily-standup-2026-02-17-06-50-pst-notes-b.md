---
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup - 2026_02_17 06_50 pst - notes by gemini.
context: the-block
created: 2026-03-16
source: granola-manual
---

# 📝 Notes

Feb 17, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivčević](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Panasenko](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [Krystof Oliva](mailto:koliva@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMTdUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.fzaj1tbgud6c) 

### Summary

**Current Release Preparation Status**  
The team confirmed that they are preparing for a major production release anticipated within the next two to three hours, having already pushed a jobs guard update to the dev environment and resolved most major associated issues.

**Development and QA Updates**  
Several team members provided updates on their work, including the completion of the contributor ticket, migration routes review, creation of new backend services, and testing for the prices and data pages. An ongoing issue was noted regarding charts in articles lacking a black background in dark mode.

**Strategic Initiatives and Adjustments**  
Work is progressing on the multilanguage MVP and Video Max integration, though the latter requires further design clarification and strategic planning for video placement. The monthly retro meeting was canceled due to current deadlines and timeline proximity to the next scheduled retro

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

NEEDS FURTHER DISCUSSION

**Video Deployment Strategy Refinement**

Video deployment strategy needs refinement; further discussion with design team scheduled to determine exact timing and placement. Videos potentially deploy as separate effort before elections launch.

ALIGNED

**Service Deprecation Timeline Strategy**

Notification API and websocket tasks must wrap up and head to QA today or tomorrow. Service deprecation consideration begins after migration tasks completion.

**Election Hero Moment Content Type**

Election coverage hero moment must use news article format. Rich media or podcast content format forbidden for this top section.

**Sean Join Brand Media Meetings**

Sean receives authorization to join Wednesday brand media team meetings. Meetings available for observing media strategy discussion.

**Monthly Retro Meeting Canceled**

Monthly retro meeting canceled this month. Cancellation provides more time for team members to focus on current release deadlines.

*More details:*

* **Onboarding, Project Setup, and Job Guard Deployment**: Aliaksandr Kryvanosau assisted Kristoff with onboarding to the core project, including local project setup and an introduction to Figma. They also pushed a jobs guard update to the dev environment to ensure that jobs not added to WordPress would not appear on production following today's release ([00:00:00](#00:00:00)) ([00:09:01](#00:09:01)). Aliaksandr is currently working on the modal for the "reach out" button click and has also completed some minor job fixes ([00:02:11](#00:02:11)).

* **Testing and Quality Assurance Updates**: Ana Benitez completed testing the "contributors ticket welcome work" and confirmed it is ready for deployment. They provided comments on the prices pages and plan to perform regression testing on data pages and sticky footers today. Ana will also assist Roma by starting to test the campus marker on the test page ([00:02:11](#00:02:11)).

* **Contributor Ticket and Existing Issues**: Bohdan Panasenko confirmed that the contributor ticket is ready, and the actual contributor field needs to be deployed to production, followed by the deployment of the related pull requests (PRs), which will likely occur after the meeting. They completed a couple of small tickets ready for review, including an extremely small one for Nicola to review. Bohdan also noted an already known issue where charts inside articles do not have a black background in dark mode; instead, they display a white background ([00:03:23](#00:03:23)).

* **Migration Progress and API Fixes**: Brian Mendoza reviewed the migration routes and confirmed that all content and pages are complete or in QA ([00:04:57](#00:04:57)). The two remaining components for the migration are the notification API and the websocket, which they plan to complete and submit for QA today or tomorrow before considering deprecating the service. Brian also fixed an issue found by Nikita that caused style leakage ([00:06:15](#00:06:15)).

* **Service Creation and Invoice Clarification**: Cesar Paz created services for the Pro API and Simon AI, and today they created a service for Campus LS, while also solving small fixes and checking data team errors related to invoices. They are awaiting answers from Mike and Matt regarding forwarding all invoices to infra.co and are currently fixing an error on the def instance ([00:06:15](#00:06:15)).

* **Multilanguage MVP and Traffic Spike Analysis**: Koray Baspinar is primarily working on the multilanguage Minimum Viable Product (MVP) and closely monitoring a significant and ongoing spike in traffic observed on both Google Discover and Google Search. They noted that the traffic spike, which is currently seeing around two times the normal volume, started in July, attributing the increase to the SEO person who works for the blog ([00:07:52](#00:07:52)).

* **Link Removal Tool and Onboarding Tasks**: Krystof Oliva completed the backend for the link removal tool, optimized it based on comments from Nicola, stress-tested it successfully, and is now awaiting Nicola's review. They received helpful onboarding from Alex regarding the project repository and Figma ([00:09:01](#00:09:01)). Krystof is working on adding a banner to the data page that links to the Pro website, which is not yet complete due to font and image matching issues ([00:10:01](#00:10:01)).

* **Bug Reporting and Thesis Work**: Krystof Oliva tested the block app and found a bug on the prices page where, even after signing in, the system asks the user to sign in again when attempting to ask for coin notifications ([00:10:01](#00:10:01)). They will be unavailable tomorrow afternoon due to thesis work involving user experience testing with doctors at the hospital. Edvinas Rupkus asked Krystof to send them a direct message with the details of the bug, including a screen recording ([00:11:10](#00:11:10)).

* **Price Page and Election Landing Page Work**: Maryia Zhynko has been fixing comments posted by Anna regarding the price page and updating the logic for charts on the stocks page ([00:11:10](#00:11:10)). After the call, they will return to working on the elections landing page. Edvinas Rupkus clarified that the hero section for election coverage will feature a news article, not rich media like a podcast, although rich media will still be present elsewhere on the page ([00:12:16](#00:12:16)).

* **Mobile Fixes and Analytics Implementation**: Marina Lozuk fixed an issue in the recirculation section on mobile devices and finalized the task related to the PolyMarket, which is now ready for review and testing. They added all necessary Google Analytics events, including a new event for the disclaimer on cards that feature a logo below the market. Marina also created new dev boxes for the sticky footer, gum, and data dashboard based on the current main branch, which can be easily released once tested ([00:13:25](#00:13:25)).

* **Release Support and Issue Resolution**: Mikita Hulis is supporting the release by resolving issues found by Roma ([00:13:25](#00:13:25)). All major issues have been resolved, with only one or two minor leftovers remaining that can be handled after the release. They reviewed Brian's ticket for resolving the style leakage and confirmed it should be ready to merge, noting that they will remove the existing "band-aid" fix on campus once Brian's ticket is merged ([00:15:06](#00:15:06)).

* **Video Max Integration and Media Strategy**: Nicola Pivčević has completed the initial setup for the Video Max integration and has left a comment in the Figma file seeking design clarification on video presentation ([00:15:06](#00:15:06)). They suggested that video deployment could potentially be a separate effort preceding the election release, but they need clarity on the go-to-market strategy. Edvinas Rupkus confirmed they would be meeting with the design team today to refine the strategy for video placement, potentially including a media hub that could also incorporate podcasts ([00:16:21](#00:16:21)).

* **Current Release Preparation**: Ramuald Vishneuski confirmed that the team is currently preparing for a release. Nikita and Rebecca are working on updating the core and the development database signal to production, with the release anticipated in two to three hours ([00:17:26](#00:17:26)).

* **LMAX Launch Support and Internal Meetings**: Edvinas Rupkus is focusing on supporting the LMAX launch today, thanking the campus and Quality Assurance teams for their efforts. Sean Winslow plans to focus on Zapier integration after the launch and inquired about joining the Wednesday 4:00 PM Eastern meetings with the brand media team ([00:18:46](#00:18:46)). Edvinas Rupkus indicated that there is no reason Sean cannot join those meetings to observe the discussion of media strategy ([00:18:46](#00:18:46)).

* **Retro Meeting Cancellation**: Edvinas Rupkus announced the cancellation of the retro meeting for this month due to current deadlines, noting that postponing it would place it too close to the next scheduled retro .

### Suggested next steps

- [ ] Brian Mendoza will wrap up the notification API and the websocket and get those in QA today or tomorrow.

- [ ] Sean Winslow will talk to Josh and whoever else on the media team about joining the Wednesday 4:00 Eastern meetings.

- [ ] Cesar Paz will wait for answers from Mike and Matt regarding forwarding all invoices to infra.co.

- [ ] Krystof Oliva will send a direct message to Edvinas Rupkus with the bug or issue that was found in the prices section of the block app.

- [ ] Edvinas Rupkus will jump in the Figma file and point out specifically what was discussed with Matt regarding the hero moment for election coverage.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=9XM71EVQ51H22FVyP7ivDxIWOAIIigIgABgDCA&detailid=standard)*

# 📖 Transcript

Feb 17, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Sean Winslow:** got the crab walk to start off this Tuesday.  
**Edvinas Rupkus:** It's just people trickling into the meeting room.  
**Sean Winslow:** Okay. All right, give people one more second. Yeah, keep on filtering in the uh little animations. That'll pass time. Should I play the cra the actual crab YouTube  
**Edvinas Rupkus:** No,  
**Sean Winslow:** video?  
**Edvinas Rupkus:** please do send the do send a happy Chinese New Year if anybody is observing that. I think that's what Kristoff was alluding to.  
**Sean Winslow:** Do we know uh what year it is? What the year of the the  
**Brian Mendoza:** I think it's the horse. I think so.  
**Sean Winslow:** horse? All right, we'll get started. We'll we'll we'll discuss our Chinese New Year's animals uh right after. I'm curious, Alex.  
**Aliaksandr Kryvanosau:** Hello. So uh I helped Kristoff to on board to the core project to also help him to set up the project locally and introduced to Figma. Then I pushed the jobs guard to the dev. So they are not present if they're if they weren't added to the WordPress.  
   
 

### 00:02:11 {#00:02:11}

   
**Aliaksandr Kryvanosau:** So they won't be appear on production after today's release. And then I did some fixes to the jobs. I'm currently working on the model for when we click on the reach out button. And that's it.  
**Sean Winslow:** Cool. Thank you, Alex. Anna  
**Ana Benitez:** Um hello. So yesterday I finished testing the contributors ticket welcome work done. Uh so that's complete and it's ready to deploy. Uh also added some comments on prices pages and well for today I will uh perform regression testing on data pages and also on sticky footers. Uh this is a de book a new debox that Marina uh worked on. So I'll be looking at that and but first uh I'll start testing campus marker in test uh page uh helping Roma on that site. And that's all for my site.  
**Sean Winslow:** Perfect. Thank you, Anna. And yeah, everything worked out fine yesterday. You you passed the information along to Marina.  
**Ana Benitez:** Uh yes to Maria. Yeah,  
**Sean Winslow:** Okay.  
   
 

### 00:03:23 {#00:03:23}

   
**Sean Winslow:** Well,  
**Ana Benitez:** thank you for that.  
**Sean Winslow:** yeah. Okay. You're welcome. Well  
**Bohdan Panasenko:** Um yes hello there.  
**Sean Winslow:** done.  
**Bohdan Panasenko:** So as Anna said the contributor ticket is ready. Um it's just uh we need like to deploy actually actual contributor field uh on the pro and then deploy the the PRs. So probably we'll do it after the meeting. Um also worked on couple of little tickets. Uh some of them are ready for review. Uh there are two of them I think. So when uh Nicola is when Nicola if you when you have time one of them is like extremely small. So like it's l really like 5 seconds question. Um yes also there is like the ticket that I got from at about Ibro um in press releases essentially it's it's already ready. I just left a little comment like of clarification and u um also I wanted to say like uh so it's not so about my tickets that's it I think uh I just before the um before the meeting I found one one issue maybe it's already known but you know always better to mention than not to mention um in articles if you on dark mode the charts inside articles they like uh they don't have a back they don't have like a black  
   
 

### 00:04:57 {#00:04:57}

   
**Bohdan Panasenko:** background they're like white background is it it's not okay just  
**Edvinas Rupkus:** Yeah, it's known. Yeah. Yeah.  
**Bohdan Panasenko:** wanted and uh yeah I guess that's  
**Edvinas Rupkus:** Good call out though.  
**Bohdan Panasenko:** pretty much it from my side I just wanted also like yeah to let you know that I have an exam tomorrow yeah so probably I won't be able to go to meeting but I will work before the exam and that's pretty Oh my s\*\*\*.  
**Sean Winslow:** Cool, man. Thank you, Baldan. Yeah, you're gonna crush it as per usual. Yeah, thank you for letting us know  
**Bohdan Panasenko:** Thanks.  
**Brian Mendoza:** Sorry,  
**Sean Winslow:** Brian.  
**Brian Mendoza:** I lost my tab. Um, what was I going to say? Okay. Um, I started the Oh, why did my board look funny? Um, that looks  
**Edvinas Rupkus:** The expedite the expedite column is missing.  
**Brian Mendoza:** weird.  
**Edvinas Rupkus:** Go up. Up.  
**Sean Winslow:** There we go.  
**Brian Mendoza:** Boom. Yeah. Um, what's it called? I started I looked took at some of our routes and what's left for the migration and all the content and pages are done or in QA whatever we knew that and I we're missing two things which is the notification API and the websocket which is like it was like half baked uh the first few months but not completed.  
   
 

### 00:06:15 {#00:06:15}

   
**Brian Mendoza:** So, I'm going to wrap those up and get those in QA probably today or tomorrow. And then we can think about deprecating the service once everything is done. And I fixed Nikita's issue with the that he found on Friday that leaked styles everywhere. Um, and yeah, just working through the rest of the stuff that's in QA.  
**Sean Winslow:** Perfect. Thank you, Brian Caesar.  
**Cesar Paz:** Uh hi uh I created the services uh for pro API and Simon AI and in addition today I created to the service for campus ls uh yeah solving a small fixes uh solving well checking some errors in the data team that yesterday I post a message in the dev channel uh about this um about invoices.  
**Sean Winslow:** Cool.  
**Cesar Paz:** I'm uh waiting for the answers from Mike and Matt probably uh because we need to forward all invoices to infra.co. Um yeah, I'm fixing uh the error we had for our def instance uh yesterday. uh on  
**Sean Winslow:** Thank you.  
**Cesar Paz:** that  
**Sean Winslow:** Yeah. Uh you you had a shout out from Nikita O about you helping out with the campus stuff.  
   
 

### 00:07:52 {#00:07:52}

   
**Sean Winslow:** So I appreciate that.  
**Cesar Paz:** waters.  
**Sean Winslow:** Thank you,  
**Cesar Paz:** Thank  
**Sean Winslow:** Caesar Corey.  
**Koray Baspinar:** Hello. Uh I am mainly working on uh our multil language MVP uh and also checking our crazy spike  
**Sean Winslow:** Yeah.  
**Koray Baspinar:** in traffic closely on both on Google discover and Google search. Uh yeah, that's all.  
**Sean Winslow:** Are you referring to what was going on in the tech SEO like how Monday like a huge there's a huge  
**Edvinas Rupkus:** Yeah, it's still ongoing.  
**Sean Winslow:** spike?  
**Koray Baspinar:** Yeah. Yeah.  
**Edvinas Rupkus:** I think we're seeing like two lex traffic right now like  
**Koray Baspinar:** It's It's still same. Yeah. It's crazy.  
**Edvinas Rupkus:** live  
**Koray Baspinar:** Yeah. It's  
**Sean Winslow:** You don't think you don't think has anything to do with the fact that we're searchable now on Google or preferable on  
**Koray Baspinar:** crazy.  
**Sean Winslow:** Google?  
**Koray Baspinar:** It is It is only about uh the SEO person who works for blog.  
**Edvinas Rupkus:** He's not wrong. Ever since he joined, what was it, Car? Was it like June or something?  
   
 

### 00:09:01 {#00:09:01}

   
**Koray Baspinar:** July and the spike  
**Edvinas Rupkus:** July.  
**Koray Baspinar:** started.  
**Edvinas Rupkus:** And we literally just went on a like trajectory straight up. It's so funny.  
**Koray Baspinar:** Exactly.  
**Sean Winslow:** Hell yeah. Thank you.  
**Koray Baspinar:** I want to take all the credit.  
**Sean Winslow:** Oh yeah, it's very much a team effort,  
**Koray Baspinar:** Yeah.  
**Sean Winslow:** but just take take your flowers right now.  
**Koray Baspinar:** Thanks for everyone.  
**Sean Winslow:** Thank you, Corey Kristoff.  
**Krystof Oliva:** Hi guys. So yeah, I worked on the link removal tool the back end on Thursday. I got some comments from Nicola regarding it. So I optimized it and then stress tested and it was a success. So now it's done and I'm waiting for review from Nicola. Uh then on Friday I had a like on boarding call kind of with Alex. It was very helpful because I tried to set up the the local host myself, but I mean there was some confusion with the pro uh repo being the co website and he kind of introduced me to it and also like to the Figma which we use.  
   
 

### 00:10:01 {#00:10:01}

   
**Krystof Oliva:** So it was kind of nice and yeah then I tried to kind of focus on the ticket regarding adding the banner for the data page like um linking to the pro website and and yeah so I did that. I mean it's not ready yet because like the fonts and um the pictures are not matching but yeah I was working on that a bit also on Sunday and then on Monday. Uh and yeah I had a one call with um with Banana and we just talked briefly and then I also talked with um Marina today and she kind of told me like u the front end stuff and the Figma and how to use it properly. So it was also really nice. And then I also u tested the block app and I found like one bug but I don't know where to kind of flag it. Like there's a Google sheet but in the Google sheet there's like general and some other tabs but not for the prices. And the the bug was found in the prices like when you sign in and then uh even though you are signed in it still it still ask you to sign in again when you're trying to ask for the notification regarding like the coins.  
   
 

### 00:11:10 {#00:11:10}

   
**Krystof Oliva:** So I don't know how to how to like that. Um, and I guess I guess that's it for me and I will be gone tomorrow because I have to do some thesis work with the doctors in the hospital. So I'm doing like user experience testing regarding my application. So tomorrow I will probably be working a bit on in the morning but in the afternoon I have like full block of doctors which I have to kind of test.  
**Edvinas Rupkus:** Sounds good.  
**Krystof Oliva:** So So  
**Edvinas Rupkus:** Can Can you please send me the in a DM the the the bug or the issue that you  
**Krystof Oliva:** yeah. Yeah. Yeah.  
**Edvinas Rupkus:** you saw with the All right.  
**Krystof Oliva:** Yeah. Yeah, I I will do a screen recording and say  
**Edvinas Rupkus:** Okay. Sweet. Thanks.  
**Sean Winslow:** Well, thank you Kristoff Maria.  
**Maryia Zhynko:** Today I've been mostly working on fixing the comments that Anna posted for price page uh and also was updating uh the logic for uh charts on stocks page like uh and asked you shown yesterday.  
   
 

### 00:12:16 {#00:12:16}

   
**Maryia Zhynko:** Um and after the call I will get back to working on elections landing page.  
**Sean Winslow:** Perfect. All right. Cool. Thank you, Maria. Marina.  
**Edvinas Rupkus:** Sorry, sorry. Real quick, sorry. Before we move to Marina, Maria, the I'll jump in the Figma file and like I'll point out specifically what I'm talking about, but I talked with Matt on Friday and uh basically the hero moment, the hero moment for election coverage where you have like the a couple of those prediction markets and like later stories and then there's the big story moment. That will be just a a a news article. It won't be like rich media or it won't be like a podcast. So, uh we will still have rich media on the page, but just in that specific top section, it'll be a it'll be a a news story, just so I know. I'll go in there when I have a second and I'll update it.  
**Maryia Zhynko:** Yep. Okay.  
**Edvinas Rupkus:** All right. Sorry. Thank  
   
 

### 00:13:25 {#00:13:25}

   
**Sean Winslow:** Good. Thank you, Maria. Marina  
**Marina Lozuk:** So I fixed the issue for uh for recirculation section on the mobile devices and also finalized task with poly market. So it's ready for review and for testing. As for Google Analytics, I've added all necessary events and even one more for disclaimer. So every every card uh has the logo uh  
**Sean Winslow:** Awesome.  
**Marina Lozuk:** below the the market below the event and for for those click I kind of introduce a new event because we don't have any information about event about market it's just general information so I've just separated it and basically that's it. Uh also I've created all new dev box as I mentioned last week for the for the sticky footer for for gum and for the data dashboard based on our current main branch. So as soon as tested we can easily uh release it. That's it.  
**Sean Winslow:** Thank you very much, Marina. Um, Nikita Gulis, want to give us a couple  
**Mikita Hulis:** Yes sir.  
**Sean Winslow:** updates?  
**Mikita Hulis:** Uh so supporting the supporting the release uh resolving the issues that uh Roma has found at this moment uh all of the major ones uh were resolved.  
   
 

### 00:15:06 {#00:15:06}

   
**Mikita Hulis:** Uh continues working closely with Niko and Roma in case something new uh will arise there. But if you there's like one or two leftovers which are not uh major whatsoever. Uh so be safely done after the release. All of the major ones are handled as of this moment. Uh did review the ticket from Brian. Thank you Brian for resolving the style leakage there. I think it should be good to go whether now or later on. Uh cuz on campus specifically I I I've left the the band-aid to prevent it just for good measure. But uh once Brian's ticket would be merged, I'll uh I'll remove it as uh unnecessary anymore. And yeah,  
**Sean Winslow:** Awesome.  
**Mikita Hulis:** that's about it.  
**Sean Winslow:** Thank you. Uh Nikita O's focusing on campus. Nicola  
**Nikola Pivčević:** Uh yeah, hello everyone. So mostly working on the video max integration. So I have like the initial setup done. Uh I left a comment on the Figma file regarding like some design question about like how videos are present.  
   
 

### 00:16:21 {#00:16:21}

   
**Nikola Pivčević:** I don't know Ed if you I I think I tagged you uh if you can maybe like take a look Serena. Yeah. To figure out like um how the presentation should work, right? And uh um yeah, I don't know like regarding this this like implementation like I guess like we could potentially deploy videos uh before as a separate effort to elections. So yeah, maybe just we need like some time to figure out like how we want to um go to to to market or go to production with this.  
**Edvinas Rupkus:** Yeah, we're going to meet today with design again because we still need to like refine that uh that strategy what it actually means, you know, where where do they all live? So, we've been chatting with the media team and with the design team, but uh we sort of have a concept of a of a plan.  
**Nikola Pivčević:** Yeah. Uh yeah, I mean like videos could be supported everywhere, not just on the elections page, right? And I think we have a bunch of already videos media file that we could  
   
 

### 00:17:26 {#00:17:26}

   
**Edvinas Rupkus:** Exactly. Yeah. So, we need like we're kind of looking into a media hub for something like that where we could like in introduce podcasts in there as well so that they're not just like pushed in the corner. Um, so yeah, progress is underway.  
**Nikola Pivčević:** Yeah. And and I guess like uh there are like links on the elections hub page that link kind of u view more videos or view shorts, right? And like how does that page look like, right? And um yeah, just yeah, we just need kind of more product  
**Edvinas Rupkus:** Yep. Yeah,  
**Nikola Pivčević:** clarification.  
**Edvinas Rupkus:** we'll definitely get you more answers on that.  
**Nikola Pivčević:** All right.  
**Sean Winslow:** Cool.  
**Nikola Pivčević:** Thank you.  
**Sean Winslow:** Nicola promo.  
**Ramuald Vishneuski:** Uh hello everybody again. So we preparing release right now. Um Nikita uh Rebecca tries to um update the course uh and update uh development uh database uh signal to production. Um yep and we expecting release in a few hours I guess in two or three hours.  
   
 

### 00:18:46 {#00:18:46}

   
**Ramuald Vishneuski:** Yep.  
**Sean Winslow:** Perfect. Thank you for a moment. Ed,  
**Edvinas Rupkus:** Um, nothing.  
**Sean Winslow:** any is there any  
**Edvinas Rupkus:** Say it again. No,  
**Sean Winslow:** updates?  
**Edvinas Rupkus:** nothing uh to update the team on that I haven't chatted about yet. Uh, many things in play. Obviously the supporting the LMAX launch today. So huge thanks to the campus team working their butts off and obviously QAM making sure that we are not releasing something critical with critical  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** bugs. Um yeah, all eyes on that today.  
**Sean Winslow:** Yeah, same goes for me. And once that's done, I'll probably focus back on the Zapier stuff, dive back into that world. Uh, and Ed, quick question for you. the Wednesday meeting with the brand media team. Uh would I be able to start joining those? Is that possible? Like the four o'clock well 4:00 Eastern meetings.  
**Edvinas Rupkus:** I usually don't join them uh unless I like have something very specific to discuss. For example, I wanted to discuss the election coverage and them creating shorts or videos for that.  
   
 

### 00:20:09

   
**Edvinas Rupkus:** Uh I started I started getting pulled into those because of the crypto IQ thing and how much  
**Sean Winslow:** No.  
**Edvinas Rupkus:** we collaborated. So like I think like if you want to just join and and observe them uh or like you know just be there in the room with them as they discuss their media strategy. I feel like there's no no need why you or no reason why you can join. But uh I usually don't join them unless I have a question.  
**Sean Winslow:** Okay, cool. Yeah, I'll talk to Josh and whoever else on the media team.  
**Edvinas Rupkus:** Yep.  
**Sean Winslow:** Thank you. All right. Uh, so does anybody else have anything that they want to  
**Edvinas Rupkus:** Oh yeah, one more thing I in case you people haven't seen yet,  
**Sean Winslow:** discuss?  
**Edvinas Rupkus:** I canled retro for this month uh just because of the deadlines and giving people more time to focus on the uh releases and it just didn't make sense to postpone it because then we're going to have another one in like two weeks time. So uh no retro this time unfortunately. No retro until morale improves.  
**Sean Winslow:** All right, guys. So, yeah. So, as I'd said, no retro, but we'll be around if you guys need anything. And yeah, especially uh campus team, please let us know anything that you need. Anything that I can help out with, just yeah, reach out. And everybody else, enjoy the rest of your evenings and I'll see you guys tomorrow.  
   
 

### Transcription ended after 00:22:03

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*