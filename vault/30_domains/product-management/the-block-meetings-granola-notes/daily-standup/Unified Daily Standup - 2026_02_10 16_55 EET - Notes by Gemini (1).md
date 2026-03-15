# 📝 Notes

Feb 10, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivcevic](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Bohdan Vadimovich](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [Krystof Oliva](mailto:koliva@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~ ~~[Koray Baspinar](mailto:kbaspinar@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMTBUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.hdkabfmaf9ip) 

### Summary

**Technical Dependencies Resolved**  
The team successfully addressed several technical dependencies, confirming that dynamic deployment templates are now functioning, SSH is working, and the BigQuery hitting limits issue appears to be resolved.

**Key Projects Are Advancing**  
Development on key projects, including poly market, multicourses, and app push notifications, is advancing, although the multicourses remain blocked by missing finalized course assets like overview videos.

**RSS Feed Causing SEO Issues**  
A critical SEO issue was identified where the RSS feed, even when delayed and linking back to the original source, allows Yahoo Finance to outrank the primary articles in search results, necessitating the complete discontinuation of the feed.

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

NEEDS FURTHER DISCUSSION

**Election Hub Content Tagging Method**

Group needs decision on mechanism for tagging Election Hub content, debating between a new category, subcategory under Policy, or specific checkbox. Edvinas will discuss implementation with Adam.

ALIGNED

**Maria Election Coverage Front End Work**

Maria assigned front-end work for election coverage. Brian assists Maria as migration finishes.

**Multicourses CMI5 QA Push**

Multicourses and CMI5 integration push to QA scheduled for tomorrow. Minimum viable assets utilized to unblock QA process.

**Nikitas Ask David For Course Assets**

Nikitas will ask David tomorrow for finalized design assets, including thumbnails and overview videos, needed to assemble courses.

**Nikola Clear Existing Broken Links**

Nikola will implement approach aligned with Corey for clearing existing broken SEO links.

**Yahoo RSS Feed Policy**

RSS feed stopped completely because Yahoo Finance ranked higher for proprietary news articles, kicking company out of Google search rankings.

**Poly Market Widget VPN Access**

Poly Market widget testing requires capability without VPN access, similar to Elmax setup. Poly Market provides an IP address for firewall access.

**Maria Starts Election Coverage Tickets**

Maria starts work on front-end election coverage tickets immediately. Brian and Marina provide support as Max 4 migration tasks conclude.

*More details:*

* **Aliaksandr Kryvanosau's Updates**: Aliaksandr finalized the enterprise compass marketing page, which is currently in code review, and addressed two fixes for the compass certificate page support email links. They also implemented minor fixes for jobs and are working on a ticket from testing regarding the Salesforce form on the campus page. Sean Winslow noted that there is no design for the relevant modal yet and will ask Serena to quickly create one ([00:00:00](#00:00:00)).

* **Ana Benitez's Updates**: Ana worked on testing the stock and exchange-traded fund (ETF) pages, providing feedback, and will continue testing buy buttons on G4 pages today with assistance from Yermek Smagulov. Regarding the fourth white paper podcast, Serena confirmed that everything is ready, and Edvinas Rupkus and Sean Winslow confirmed that the team is ready for deployment ([00:01:16](#00:01:16)).

* **Bohdan Vadimovich's Updates**: Bohdan completed work on the new contributor feature, which is ready for testing, and fixed a small visual design issue that has been sent for review and was recently approved ([00:02:22](#00:02:22)).

* **Brian Mendoza's Updates**: Brian spent yesterday deploying most items in the awaiting deploy status, delaying the sorted sets and events page due to an unexpected issue on the dev box. They are currently deploying the sorted sets and events page during normal hours as a precaution and plan to follow up on in-progress tasks, noting that a large pull request for poly market work needs to be reviewed and tested, possibly requiring a new API endpoint for QA ([00:02:22](#00:02:22)).

* **Cesar Paz's Updates**: Cesar deployed changes to the box part, which resulted in dynamic templates for deploying new services, like Campus or TCB3, and confirmed that SSH is now working. They are currently working on dynamically enabling environment variables in the boxes and need to forward emails with invoices to a specific address ([00:03:35](#00:03:35)). Cesar confirmed that the BigQuery hitting limits issue appears to be resolved, as they only exceeded the limit for two days, and the situation is now normalized ([00:05:06](#00:05:06)).

* **Maryia Zhynko's Updates and Future Assignments**: Maryia has been working on fixing issues on the stock, ETF, and prices pages, as well as fixing bugs found on the "Advertise With Us" page following the migration. Edvinas Rupkus suggested that Maryia would be suitable to handle the front-end side of election coverage, an idea that Brian Mendoza and Mike Price supported ([00:06:16](#00:06:16)). Brian offered to assist Maryia, as they are close to completing the migration, planning to finish deprecating legacy services and APIs soon ([00:07:33](#00:07:33)).

* **Marina Lozuk's Updates**: Marina is nearly finished with the poly market work, having deployed the changes to the dev box for testing. The only remaining task is the Google Analytics tracking, and they have added a few questions regarding this to the ticket. Sean Winslow confirmed they would respond to the questions immediately after the standup ([00:08:18](#00:08:18)).

* **Mike Price's Updates and Q2 OKRs**: Mike is focused on pushing app notifications, having worked on push notifications for the iOS app last week, and is working with Matt to release a test build, starting with leadership and then moving to a company-wide test within the next week. They are also building a standalone Simon AI app for potential integration and are working on a redo of the public API to make it more performant and self-service, planning to complete this last item within the next two weeks as it is one of their Quarterly Objectives and Key Results (OKRs) ([00:09:18](#00:09:18)).

* **Mikita Hulis and Nikita Orobenko's Collaboration on Multicourses**: Mikita Hulis and Nikita Orobenko worked with David and Nikita to find a way to send out the multicourses and the CMI5 integration to QA while waiting for the finalized course questions. They confirmed that all functionality appears to be ready and anticipate sending it to QA tomorrow if the verification steps for the interim solution go well, but they are still waiting for finalized assets like overview videos and thumbnails, which they can update later ([00:10:39](#00:10:39)).

* **Course Assets and Dependency on David**: Sean Winslow confirmed that for Campus 101, they plan to use simple interior and exterior thumbnails and a video with two slides and voice-over, but they require the necessary assets from David via the Learning Management System (LMS). Nikita Orobenko agreed that they need the overview video for the whole course to allow users without access to decide if the course is relevant to them ([00:14:48](#00:14:48)). Sean will follow up with David regarding these assets and asked Nikita Orobenko to also discuss it with David during their meeting ([00:15:54](#00:15:54)).

* **SEO and Video Implementation**: Nikola Pivcevic worked on and deployed several smaller SEO-related tasks and aligned with Corey on a safe approach for clearing up existing broken links. Nikola also received the tickets for videos on the website and will need to meet after the standup to clarify a few questions, particularly regarding the specification details provided on the ticket that came from documentation ([00:16:48](#00:16:48)). Edvinas noted that Nikola's return coincided with the resolution of the Elmax issues ([00:17:59](#00:17:59)).

* **RSS Feed Issue with Yahoo Finance**: Nikola Pivcevic confirmed that they stopped the RSS feed completely because delaying the news feed by 30 minutes to allow the article to be published on their website first did not prevent Yahoo Finance from outranking their own articles in Google search results ([00:17:59](#00:17:59)). Nikola expressed surprise that Yahoo Finance, even when linking back to their original story, still ranked higher, causing the original article to be kicked out of Google search results ([00:19:03](#00:19:03)).

* **Romuald Vishneuski's Updates and Marketo Deprecation**: Romuald is working on Campus, has minor issues with the Marketo deprecation task that require retesting, and is waiting for the full course on the dev environment for testing. Romuald also requires assistance in addressing redundant courses in the CMS/Pro database ([00:20:08](#00:20:08)). The Marketo deprecation is nearing completion, with only minor UI issues remaining, and Romuald confirmed they will be ready before the deadline, potentially for deployment tomorrow or Thursday ([00:21:39](#00:21:39)).

* **Poly Market Widget Testing Environment**: Edvinas Rupkus noted Matt's request to set up a testing environment for the poly market widgets similar to the Elmax setup, allowing the Poly Market team to test without needing VPN access. Mike Price suggested that the best way to unblock the Poly Market team would be if they could provide an IP address to allow them access ([00:22:54](#00:22:54)).

* **Election Coverage Discussion and Tagging**: The team transitioned to discussing the election coverage project, specifically how to tag or categorize content for the new Elections Hub page ([00:25:22](#00:25:22)). Nikola Pivcevic asked how authors should tag an article to ensure it appears on the new Elections Hub page, questioning if it should be a new category, a tag, a checkbox, or a label ([00:28:00](#00:28:00)). Edvinas suggested that a checkbox, such as "include on the election page," would be preferable to avoid introducing another category or relying on authors to consistently use a tag ([00:29:10](#00:29:10)).

* **Methodology for Videos and the Elections Hub**: Nikola asked if the same methodology used for articles would also apply to videos, ensuring they are added to the Elections Hub page. Edvinas agreed that a method, perhaps a subcategory under "policy," would be established, and they will discuss this with Adam ([00:29:10](#00:29:10)). Edvinas noted that videos are currently only planned for the Elections Hub page, though future Core Template Optimization (CTO) work may integrate them onto other pages ([00:30:21](#00:30:21)).

* **Data Sources for Election Coverage**: The team discussed where data, such as report cards, would be pulled from for the election coverage. Edvinas confirmed that there would be an exclusive API feed for the ST Crypto portion, though Mike Price noted no new updates have been received since the initial call with Stamber Crypto and Coinbase developers ([00:33:49](#00:33:49)).

* **Assigning Front-End Election Coverage Work**: Edvinas suggested that Marina could assist Maria with the broad front-end work for election coverage after Marina completes the poly market widget implementation ([00:35:08](#00:35:08)). Brian supported this idea and noted that Maria is wrapping up their current stock and prices work, making them ready to start on the election coverage ([00:35:08](#00:35:08)).

* **SEO and Technical Tags for Election Hub**: Sean mentioned that he sent the first election coverage ticket to Matt, who provided a full comment, now displayed in the ticket, regarding the best SEO approach and technical tags to use for the Election Hub landing page ([00:36:24](#00:36:24)).

### Suggested next steps

- [ ] Sean Winslow will read through all of Ana Benitez's comments today.  
- [ ] Sean Winslow will talk to Serena for the modal design, and then get back to Aliaksandr Kryvanosau.  
- [ ] Brian Mendoza will get the poly market PR reviewed and find a way to test it by making an API endpoint or something for QA.  
- [ ] Edvinas Rupkus will keep an eye out for BigQuery hitting limits.  
- [ ] Sean Winslow will reach out to David again regarding the assets from the LMS system for the videos.  
- [ ] Ramuald Vishneuski will reach out to Edvinas Rupkus later for help with figuring out what to do with some redundant courses on pro in CMS to keep the database clean.  
- [ ] Edvinas Rupkus will ask Poly Market for an IP address to allow them to test out the widgets without VPN access and follow up on updates from Stamber Crypto regarding the exclusive API feed for the election hub's report cards.  
- [ ] Cesar Paz will forward all emails with invoices to reply.  
- [ ] Edvinas Rupkus will chat with Adam about the preferable way to tag group content for the elections hub, possibly a subcategory under policy.  
- [ ] Mikita Hulis and Nikita Orobenko will talk to David tomorrow about the needed design assets for the multi-courses and CMI5 integration.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=gciK_OL5BTRxH1iRqMtMDxIWOAIIigIgABgBCA&detailid=standard)*

# 📖 Transcript

Feb 10, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Sean Winslow:** Yo, how's it going everybody? How's  
**Edvinas Rupkus:** Sean  
**Sean Winslow:** everyone?  
**Edvinas Rupkus:** long.  
**Sean Winslow:** Long. Yeah, Ed, how was your  
**Edvinas Rupkus:** Yeah, it was good.  
**Sean Winslow:** vacation?  
**Edvinas Rupkus:** It was very cold in Europe and froze my ass off, but I had a lot of fun. So, ready ready to get back to it.  
**Sean Winslow:** Nice. All right, we will start with Alex.  
**Aliaksandr Kryvanosau:** Hello. So I was able to finalize the compass marketing page for enterprises. Now it's in code review. Then I provided two fixes for compass certificate page support email links. Then did a bit uh fixes for jobs and got a ticket back from testing uh about Salesforce form on campus page and currently working on it.  
**Sean Winslow:** Perfect. Thank you. And I saw your comment. Uh I'm going to talk to Serena.  
**Cesar Paz:** Thank  
**Sean Winslow:** There isn't a design for that modal yet. So I'm going to talk to Serena to see if she can spin something up real quick and then I'll get back to you.  
   
 

### 00:01:16 {#00:01:16}

   
**Aliaksandr Kryvanosau:** Sounds good.  
**Sean Winslow:** Cool. Thank you, Alex. Anna.  
**Ana Benitez:** Um hello. So yesterday I work on testing a stock and ETF pages. Added some comments in there. Also I today uh I will continue testing the buy buttons on G for these pages. Uh Jeremic is helping me with that. And um uh also Serena confirmed that uh regarding the fourth white paper podcast everything is okay. So I wanted to ask from product perspective are we ready to deploy  
**Edvinas Rupkus:** Yeah, I think so.  
**Ana Benitez:** that?  
**Edvinas Rupkus:** I think it's uh unless John heard anything else. I think there's already one in there uh that's released.  
**Sean Winslow:** No.  
**Edvinas Rupkus:** So, we're ready to start populating those.  
**Ana Benitez:** Okay, thank you. And that's all for my side.  
**Sean Winslow:** Cool. Thank you, Anna. Yeah, I saw I saw a bunch of comments.  
**Ana Benitez:** Yeah,  
**Sean Winslow:** I didn't get to read through them all just yet,  
**Ana Benitez:** thank you.  
**Sean Winslow:** but I'll get to them today.  
   
 

### 00:02:22 {#00:02:22}

   
**Sean Winslow:** Right. Well done.  
**Bohdan Vadimovich:** Um, hi there. So, I uh finished working on that uh new contribu contributor thing. Um, it's ready for testing and also I fixed like a small u um visual design if you could say issue. I sent it to review and I think it was just approved. Um, so yeah, that's pretty much it.  
**Sean Winslow:** Cool. All right. Thank you, Bon Brian.  
**Brian Mendoza:** I was deploying most of the things in awaiting deploy yesterday. Um, I had to wait for the sorted sets and events page and all that one because I found this weird thing on the dev box that scared me. But I'm deploying it right now and during a normal hour in case something does go wrong with plan B and C in place. So, um, deploying that now and I'll probably go back to whatever's in progress and figure figuring out something to work  
**Sean Winslow:** Nice.  
**Brian Mendoza:** on.  
**Sean Winslow:** Sweet. Yeah. And all the poly market stuff uh you were working with Matt like everything is taken care of like pretty  
   
 

### 00:03:35 {#00:03:35}

   
**Brian Mendoza:** Yes, I'm gonna get that PR reviewed. It's a big one.  
**Sean Winslow:** much.  
**Brian Mendoza:** And then find a way to test it. Um, make like an API endpoint or something for QA.  
**Sean Winslow:** Thank you, Brian. Caesar, what you got?  
**Cesar Paz:** Hi. Uh well uh I did today a deployment of some change in the box part and now we have uh dynamic templates for deploying for deploying new services. For example, in order to deploy campus, we need specific services or to deploy TCB3, we need another one. So it's dynamic. uh SSH is working now. So we basically to copy the command SSH we can see in the column SSH common and that's all. Um and I have working now sorry I'm working now in um the possibility to the environment variables in the boxes uh dynamic tool. Uh in addition I need to um forward all emails with invoices to reply. Uh so yeah this task is now in the origin tab.  
**Sean Winslow:** Okay.  
**Cesar Paz:** Um so working on that right now.  
   
 

### 00:05:06 {#00:05:06}

   
**Sean Winslow:** Yeah. Does that have to do uh with the comment that we got yesterday?  
**Cesar Paz:** Uh, no. I don't think so.  
**Sean Winslow:** You're not sure. Okay.  
**Cesar Paz:** No.  
**Edvinas Rupkus:** Caesar, sorry if I missed that if you already addressed this.  
**Sean Winslow:** Was  
**Cesar Paz:** Yeah.  
**Edvinas Rupkus:** I think I got an email uh from BigQuery hitting limits again. Is there have there been any news on  
**Cesar Paz:** Yeah.  
**Edvinas Rupkus:** that?  
**Cesar Paz:** Uh, let me check because I received yesterday.  
**Edvinas Rupkus:** It might have been the same email.  
**Cesar Paz:** I believe it's so it's solved I think because uh if yeah if we exceed the limit for seven days in a row we have a problem but we only exceeded two days and now it's normalized  
**Edvinas Rupkus:** Mhm.  
**Cesar Paz:** again so yeah now it's working fine again I didn't receive any email yesterday I received on Saturday I think and on Sunday So yes.  
**Edvinas Rupkus:** Gotcha.  
**Cesar Paz:** Yeah,  
**Edvinas Rupkus:** Okay.  
**Cesar Paz:** I believe it's normalized now.  
**Edvinas Rupkus:** Okay, let's just keep an eye out for that for sure.  
   
 

### 00:06:16 {#00:06:16}

   
**Cesar Paz:** Okay. Yeah.  
**Edvinas Rupkus:** But thanks thanks for the update.  
**Cesar Paz:** Thank  
**Sean Winslow:** Yeah, thank you,  
**Cesar Paz:** you.  
**Sean Winslow:** Caesar. And yeah, I was referring to something that Leanne sent yesterday, but yeah, it definitely doesn't have to do with you. So, thank you very much.  
**Cesar Paz:** No,  
**Sean Winslow:** Yeah,  
**Cesar Paz:** thank you.  
**Sean Winslow:** you're welcome, Corey. Corey,  
**Edvinas Rupkus:** I think he's uh missing the because he has like an appointment to go to today. So if you let me  
**Sean Winslow:** gotcha. Cool.  
**Edvinas Rupkus:** know  
**Sean Winslow:** Maria  
**Maryia Zhynko:** I've been working on uh making some fixes for stock ETFs and prices page and also was uh fixing bugs from found on advertise with us uh from migration.  
**Edvinas Rupkus:** um Matt Mike I sent you a text in regards to Maria's future tickets. Uh, I don't know. I don't know if you had a chance to look at it or think about it. Uh, whoa, something went wrong there. Uh,  
**Sean Winslow:** Oh,  
**Edvinas Rupkus:** I'm thinking that Maria potentially could be good for to think like the front end side of election coverage.  
   
 

### 00:07:33 {#00:07:33}

   
**Edvinas Rupkus:** Does anybody have any other any other ideas? This Marina is  
**Mike Price:** I Yeah,  
**Edvinas Rupkus:** uh  
**Mike Price:** let me Oh, Frank, you were going to say something.  
**Brian Mendoza:** I think it's fine. Yeah, I don't see an issue with that. Um I I'm also looking for bigger stuff to work on as well.  
**Edvinas Rupkus:** Okay, cool.  
**Brian Mendoza:** So, we're probably in the pairing up on things or splitting the work. But  
**Mike Price:** Yeah, Brian.  
**Brian Mendoza:** yeah,  
**Edvinas Rupkus:** Yeah.  
**Mike Price:** I heard they could kind of run that.  
**Brian Mendoza:** I'll like assist Maria because I'm now that we're like on the last two pages for the migration,  
**Edvinas Rupkus:** Okay.  
**Brian Mendoza:** I'm going to probably work on uh figuring out the last few legacy services, APIs or whatever. to deprecate the thing all the way and then I'm just completely free. So, Maria can start and then I'll help her out if she needs it in the next few  
**Edvinas Rupkus:** I see. Yeah, if you guys would like, we can stay stick around after the stand up and just like quickly look at the epic that Sean put together  
   
 

### 00:08:18 {#00:08:18}

   
**Brian Mendoza:** weeks.  
**Edvinas Rupkus:** and just dish out because I think Nicola also is looking for the back end work for that as well. So,  
**Brian Mendoza:** Cool.  
**Edvinas Rupkus:** all right.  
**Brian Mendoza:** Sounds great.  
**Edvinas Rupkus:** Sweet.  
**Sean Winslow:** All right. Yeah, sorry about that, guys. I think my Jira is bugging out right now, but we should be able to power through hopefully. Uh, yeah. Thank you, Maria. Marina.  
**Marina Lozuk:** Hello guys. Uh I'm almost almost done with the poly market stuff. I've already deployed to the dev box. So it's available for tasting. The only thing which is left it's uh Google Analytics tracking. There are few questions and I've added them to the ticket. That's  
**Sean Winslow:** Cool. Thank you, Marina. Yeah,  
**Marina Lozuk:** it.  
**Sean Winslow:** I saw your question and I was just about to answer it and then the standup started. So, I'll get back to you right after this.  
**Marina Lozuk:** Okay. Thank  
**Sean Winslow:** Thank you,  
   
 

### 00:09:18 {#00:09:18}

   
**Marina Lozuk:** you.  
**Sean Winslow:** Mike.  
**Mike Price:** uh pushing the app notifications. Uh last week worked mainly on notifications for push notifications for the iOS app. Um we're working working with Matt to get a uh test build out both for leadership. We started with a test flight for with leadership team. We're going to do a companywide uh test in the next week or so. Uh so everybody can check out the iOS app. Uh other than that, I'm working on a standalone Simon uh Simon AI app to integrate both later when if we want to put it on.co, but there's a need on another side. There's some somebody's doing Jordan Leachch is doing an integration with uh doing some integrations. He's really kind of vi coding a lot of stuff for um the media side of things. So, I'm standing that up real quick. And then, uh, the public API last on the list. We get that out. Um, just a redo of it and that's more performant, self-service. So, that was only OKRs for this quarter.  
   
 

### 00:10:39 {#00:10:39}

   
**Mike Price:** So, I'm going to get that done and wrapped up in the next two weeks. I I think um at least get it out. We'll have legacy support for the existing pro customers.  
**Marina Lozuk:** Dang  
**Mike Price:** Some of them need to use it. So, yeah. That's really  
**Marina Lozuk:** it.  
**Sean Winslow:** Great. All right. Thank you, Mike. Yeah,  
**Mike Price:** it.  
**Sean Winslow:** I was just getting Jordan was just asking me about a bunch of Jurro questions, so I assume it has something to do with that. So, I might reach out to you if if  
**Mike Price:** Okay, cool.  
**Sean Winslow:** necessary.  
**Mike Price:** Let me know what he says.  
**Sean Winslow:** Nikita Gulis.  
**Mikita Hulis:** Yep. So, in collaboration with David and Nikita, we found a sort of middle ground way of uh uh sending out the what we already have uh for the multicourses and the CMI5 integration in uh into QA while we are  
**Sean Winslow:** Cool.  
**Mikita Hulis:** still waiting for the finalized versions of uh questions for the course. Um on our end um it looks like all of the functionality itself is ready and with the with a few steps left to verify the middle ground if all goes well we would be able to uh send it off to QA tomorrow.  
   
 

### 00:12:03

   
**Mikita Hulis:** Uh otherwise we are waiting on the finalized versions of questions etc etc. Um, so yeah, fingers crossed that's everything will go well.  
**Sean Winslow:** Thank Well, so what what were the questions that you were sent? They were they weren't finalized. They were just a handful of questions that he picked.  
**Nikita Orobenko:** the the questions are fine by themselves. Uh we rework them a little with David today because they utilize a little bit different formats uh from what we expected. Um we still need a few little thing other things from the David side. uh the exported sources for all other subjects except for the one I have on my hands. Uh they still will be changing on the flight because the course is not finalized yet as far as I know. But it won't be a problem because we can just reupload the source files uh on our storage and boom uh the course is updated. Uh so I'm just testing it out locally to see what is the minimum possible uh things we need to push it to the QA.  
   
 

### 00:13:23

   
**Nikita Orobenko:** So while we're still are waiting for the design assets to be completed uh like the thumbnails, the overview videos uh etc etc there's still some minimum uh possible thing that we can push to the testing at least to unblock the Roma uh and finish out uh the rest of the things on the flight just not to waste uh the time because it's not a good game uh where at least the game we cannot  
**Edvinas Rupkus:** Yeah.  
**Nikita Orobenko:** win.  
**Edvinas Rupkus:** Uh, is there is there any way either Sean or I could help with the question formatting? I know like I'm familiar with the  
**Nikita Orobenko:** Uh no, the questions are fine already.  
**Edvinas Rupkus:** previous  
**Nikita Orobenko:** Uh so we finally got them after everything. Uh and  
**Mikita Hulis:** It's I was like the the phrasing was a bit off. Yeah, it's more so the finalized version of the course itself and with this questions with everything  
**Sean Winslow:** Oh.  
**Mikita Hulis:** else baked in as of right now with like some  
**Edvinas Rupkus:** Okay.  
**Mikita Hulis:** level of on the-fly changes the goal is to push it to QA as soon as possible and the finalized version should be there at the time of the release itself unless some sort of mishap happens and it is incompatible but it should be compatible.  
   
 

### 00:14:48 {#00:14:48}

   
**Edvinas Rupkus:** Understood.  
**Nikita Orobenko:** So yeah, as of right now, it's more like a question to David.  
**Edvinas Rupkus:** Thanks.  
**Nikita Orobenko:** uh what does he left uh to finish? Maybe he's dependence from somebody from the research team. Maybe he needs help uh finishing with finishing out the course. Uh but on our tax side uh we got basically I hope uh most of the needed things. So I will give you an update a bit later today if tomorrow uh morning uh our morning release uh will be possible to the dev  
**Edvinas Rupkus:** Nice.  
**Nikita Orobenko:** box.  
**Sean Winslow:** Cool. Thank you, Nikita. And yet, are you guys meeting with David tomorrow uh morning or afternoon?  
**Nikita Orobenko:** I suppose yes. Like every  
**Sean Winslow:** Yeah. Okay. Yeah. Because I I meet with him on Thursdays and I was discussing the designs with him.  
**Nikita Orobenko:** day  
**Sean Winslow:** Um because we're just going to go with a simple like for campus 101, the thumbnails were just Oh, yeah. I I went over this with you guys last week.  
   
 

### 00:15:54 {#00:15:54}

   
**Sean Winslow:** I think it it's just seems to be interior and exterior thumbnails and then the actual video is just two slides with some voice over. So, we were going to go with that, but I need David to send me the assets from the LMS system in order to put  
**Nikita Orobenko:** Yeah. Plus,  
**Sean Winslow:** together.  
**Nikita Orobenko:** we do need the overview for the whole course. So,  
**Sean Winslow:** Yeah.  
**Nikita Orobenko:** the people without the access to the course will be able to play it out that video and see like do they really need that course uh or no.  
**Sean Winslow:** Yeah. So, I'm gonna reach out to David again. I don't want to keep on bugging him uh because I keep on messaging him asking about stuff because we're going back and forth trying to figure out what we actually need. But yeah, if you guys can just bring that up to him and then I'll be able to get the assets from him and then put the videos together. So, you guys can hope I know I know that's not extremely important, but for the finalized version it is.  
   
 

### 00:16:48 {#00:16:48}

   
**Sean Winslow:** So, But I'll message him again.  
**Nikita Orobenko:** Yep.  
**Sean Winslow:** But yeah, if you could just talk to him tomorrow, that'd be great.  
**Nikita Orobenko:** Yep. We'll do.  
**Sean Winslow:** Thank you.  
**Nikita Orobenko:** And thank you. I'm I'm not sure what who exactly should I be thanking for, but thank you for pushing the thing with the research team. I'm sorry for my meltdown yesterday, but it seems like it was a necessary thing at that moment  
**Sean Winslow:** No, no,  
**Edvinas Rupkus:** No,  
**Nikita Orobenko:** already.  
**Sean Winslow:** no.  
**Edvinas Rupkus:** no,  
**Sean Winslow:** I I'm sorry.  
**Edvinas Rupkus:** that's that's the right approach.  
**Sean Winslow:** Yeah, I'm sorry that it got to that point. Like I we were trying to we were trying our best and then they just weren't really responsive.  
**Edvinas Rupkus:** Yeah.  
**Sean Winslow:** So, we had to get leadership involved. So, I appreciate you reaching out. Cool. Thank you, Nikita Nicola.  
**Nikola Pivcevic:** Uh yeah, hello everyone. Uh so worked and deployed a bunch of like uh smaller SEO stuff and uh I met with Corey today and we were like we aligned on the like kind of safe approach on clearing up those uh existing broken links.  
   
 

### 00:17:59 {#00:17:59}

   
**Nikola Pivcevic:** And I'm going to uh like work on that approach uh a little bit more like shouldn't be too difficult. And uh yeah, and I read that the got finally the tickets for the videos uh on co and uh I went through them and I maybe I have like a few questions. Maybe we can stay uh after standup and like yeah maybe like go through those questions and uh uh but yeah going to start working on that as  
**Sean Winslow:** Cool.  
**Nikola Pivcevic:** well.  
**Sean Winslow:** Yeah, I I just put those together. I still have to I'm I'm talking with Jordan now. I'm going to meet with them and we're going to try to figure out what exactly the specs are that they would need. The stuff on the tickets were just mainly from the um documentation that uh the plug-in provided. So, it's kind of just, you know, a bunch of stuff like from the documentation. So, we can narrow it down and then yeah, we'll stay after this and try to figure stuff out for you.  
**Edvinas Rupkus:** Nicola, it looks like I was the actual problem in the Elmax saga.  
   
 

### 00:19:03 {#00:19:03}

   
**Edvinas Rupkus:** As soon as I went away, everything got deployed.  
**Nikola Pivcevic:** Yeah.  
**Edvinas Rupkus:** All the blockers were removed. So glad to see that's already  
**Nikola Pivcevic:** Yeah. Yeah.  
**Edvinas Rupkus:** out.  
**Nikola Pivcevic:** It's I'm so happy that that we got Yeah.  
**Edvinas Rupkus:** On to better things.  
**Nikola Pivcevic:** Hopefully we get paid. Did we get paid? I don't know.  
**Edvinas Rupkus:** that too. Yeah, we should.  
**Sean Winslow:** Thank you, Nicola. Oh, and everything was good with the RSS feed yesterday. Was there any updates?  
**Edvinas Rupkus:** Well, it killed the thing.  
**Nikola Pivcevic:** Yeah,  
**Sean Winslow:** Yahoo.  
**Nikola Pivcevic:** we stopped it. We and uh yeah,  
**Sean Winslow:** Okay.  
**Nikola Pivcevic:** unfortunately, which is still like something that I don't quite understand fully like uh we delayed the the RSS feed to u add news only 30 minutes after the news is published on our website, right? And then after uh the Yahoo Finance pulled the news, they would rank higher than our own and we would get kicked out of Google for that news article, right?  
   
 

### 00:20:08 {#00:20:08}

   
**Nikola Pivcevic:** So you would type in the exact article title and Yahoo would show up, we wouldn't show up anymore. Like you know this how much bigger the authority of Yahoo Finance is that like even though like it's our story, it's links back to us. It's uh we it's first appeared on our website still they take over which is crazy crazy in my opinion. Yeah.  
**Sean Winslow:** Yeah,  
**Nikola Pivcevic:** So we stopped Yeah.  
**Sean Winslow:** that's okay.  
**Nikola Pivcevic:** We we stopped the feed completely.  
**Sean Winslow:** Yeah, that's pretty devious. f\*\*\*\*\*\* Yahoo.  
**Nikola Pivcevic:** Yeah.  
**Edvinas Rupkus:** Maybe Google Google algorithms work in mysterious  
**Sean Winslow:** All right. Yeah.  
**Edvinas Rupkus:** ways.  
**Sean Winslow:** Thank you, Nicola. Remote.  
**Ramuald Vishneuski:** Uh hello team. Uh so now I'm working u uh on campus and uh um have uh little uh more issues for um areta duplication um uh task. Uh so have to retest some things. Um and yeah waiting for for the full uh course to be on on the dev uh to test it and um later I will uh need uh your help uh with uh figuring out um what to do with some redundant courses on uh pro in CMS.  
   
 

### 00:21:39 {#00:21:39}

   
**Ramuald Vishneuski:** we uh have some redundant courses uh by mistake. I suppose uh I want to remove them you know in order to to keep our uh database uh clean. So I will reach out to you uh with that later.  
**Edvinas Rupkus:** Okay, Aroma, real quick. Uh,  
**Sean Winslow:** Perfect.  
**Edvinas Rupkus:** you said you have a few little things left for the Marquetto deprecation. Is everything else basically just like in QA right now? All the four forms.  
**Ramuald Vishneuski:** Um we almost done. Uh nothing critical there. Uh only some minor things with uh UI uh mostly nothing  
**Edvinas Rupkus:** Gotcha. Okay.  
**Ramuald Vishneuski:** else.  
**Edvinas Rupkus:** We're looking ready to deploy either tomorrow or or uh what or Thursday. I don't know what day it is.  
**Ramuald Vishneuski:** Wednesday. Okay. I don't know either.  
**Edvinas Rupkus:** Yeah.  
**Ramuald Vishneuski:** Uh yeah,  
**Edvinas Rupkus:** Yeah.  
**Ramuald Vishneuski:** we will be ready uh before deadline.  
**Edvinas Rupkus:** All right.  
**Ramuald Vishneuski:** Yeah,  
**Edvinas Rupkus:** Sweet.  
**Ramuald Vishneuski:** definitely.  
**Edvinas Rupkus:** Awesome.  
**Sean Winslow:** Yeah,  
**Edvinas Rupkus:** Thanks,  
   
 

### 00:22:54 {#00:22:54}

   
**Sean Winslow:** thank you Rom and Yermick. I saw you don't have any updates, correct?  
**Yermek Smagulov:** Yeah, absolutely. I just came in effect if anyone has any questions.  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** Yeah,  
**Sean Winslow:** Just popping  
**Edvinas Rupkus:** we'll discuss we'll discuss stuff today on the call. Um, should be a pretty juicy one probably.  
**Sean Winslow:** All right. So, Ed, updates on your  
**Edvinas Rupkus:** Uh,  
**Sean Winslow:** end.  
**Edvinas Rupkus:** yeah. So, the white papers podcast, I just received a go ahead. So we can definitely push it to production. And then also Matt flag to me that for the poly market widgets that Marina is working on uh it would be nice to have a similar situation with the dev box like we did with Elmax to have the possibility for for Poly Market to uh test it out without the VPN access. So I don't know see if Caesar or like Nicola could help out Marina with that setup. Uh just just a heads up because they will definitely want them to  
**Mike Price:** If they have a IP address that they can give us,  
   
 

### 00:24:00

   
**Edvinas Rupkus:** take.  
**Mike Price:** we can allow this to Yeah,  
**Edvinas Rupkus:** Okay. Would that be easier?  
**Mike Price:** that' be the best way to unblock them to allow them  
**Edvinas Rupkus:** Sweet.  
**Mike Price:** in.  
**Edvinas Rupkus:** All right. I'll ask for that. Okay. Uh, and then yeah,  
**Sean Winslow:** All  
**Edvinas Rupkus:** the rest of the stuff was um tied to campus mostly, but you already seems to be covering that, Sean. Uh, I've trying to work through all the emails in my inbox and try to like respond to any questions that are left unanswered. Is there anything like, you know, that people are waiting on right now that are blocked with? Anybody can just is waiting on my input. Great. Awesome. Yeah, just getting back into this swing of things and uh we'll I guess we can stick around for to discuss poly market uh or not poly market election coverage tickets.  
**Sean Winslow:** right. Yeah. Uh so we'll stick around. Uh updates on my end. Um pretty much just working on the campus stuff and I'm getting Oh, I figured out those scripts uh to generate the animations.  
   
 

### 00:25:22 {#00:25:22}

   
**Sean Winslow:** So I'm going to hopefully start implementing that after the MVP. We don't have time to mess around with that. So, I'm just getting a bunch of icons together and then hopefully the assets that we were just discussing earlier and doing some work for Jordan and Carla on the GR side. So, that's it on my end. So, if does anybody else have anything that they want to discuss before we move towards the election coverage? All right, for those that want to stick around, stick around. For those that want to just do anything else but this, I'll see you guys  
**Edvinas Rupkus:** Good. It's probably Maria, Marina,  
**Sean Winslow:** tomorrow.  
**Edvinas Rupkus:** Brian, Nicola, Mike most importantly.  
**Sean Winslow:** All right, team.  
**Edvinas Rupkus:** Thanks,  
**Sean Winslow:** Do you guys want Yeah.  
**Edvinas Rupkus:** guys.  
**Ana Benitez:** Thank you.  
**Sean Winslow:** Ed, would you mind pulling up yours? Uh,  
**Edvinas Rupkus:** Yeah,  
**Sean Winslow:** because my Yeah,  
**Edvinas Rupkus:** I have it. No  
**Sean Winslow:** I don't know what's going on with my  
**Edvinas Rupkus:** worries.  
**Sean Winslow:** Jira.  
   
 

### 00:26:46

   
**Edvinas Rupkus:** Hello.  
**Brian Mendoza:** What's  
**Edvinas Rupkus:** It literally It literally was just working. Yeah, I'm having So, J must be having issues then.  
**Brian Mendoza:** Check their status page. What's going on over there?  
**Sean Winslow:** Yeah,  
**Edvinas Rupkus:** Uh, okay. Okay. So, our board works, but specific tickets.  
**Sean Winslow:** I have uh the tickets in the Gmail.  
**Edvinas Rupkus:** Oh, there we go.  
**Sean Winslow:** in my You got  
**Edvinas Rupkus:** There we go. Yeah. Okay. Uh, so I guess let's start with Nicola.  
**Sean Winslow:** it.  
**Edvinas Rupkus:** the the few questions that you had. Which one is it? The  
**Nikola Pivcevic:** Uh yeah.  
**Edvinas Rupkus:** 712\.  
**Nikola Pivcevic:** Uh I can uh yeah I'm just sharing my screen. So So yeah my question is yeah my question is um regarding like kind of how we  
**Edvinas Rupkus:** Okay.  
**Nikola Pivcevic:** are going to tag group or like whatever like content for the elections hub. So so I'm guessing not all stories will be under the elections hub right. So is the elections hub like a category, a tag or like a completely new thing?  
   
 

### 00:28:00 {#00:28:00}

   
**Nikola Pivcevic:** Like how do we like in integrated in the current  
**Edvinas Rupkus:** Yeah,  
**Nikola Pivcevic:** like system of like categorization and labeling, right?  
**Sean Winslow:** So if you look at the first ticket, like this is going to be a totally new page. So let me pull up the  
**Edvinas Rupkus:** but I think his question is how do we pull those like election related stories into onto  
**Nikola Pivcevic:** Yeah.  
**Sean Winslow:** ticket.  
**Nikola Pivcevic:** So, so  
**Edvinas Rupkus:** this page because we have like we have policy and law categories but like some of it could be  
**Nikola Pivcevic:** when  
**Edvinas Rupkus:** like about like unrelated to elections you  
**Sean Winslow:** Okay.  
**Nikola Pivcevic:** Yeah. So, how when when uh when an author uh publishes an article, how will they tag an article so that it appears here, right? Like what is the kind of checkbox?  
**Edvinas Rupkus:** That's a great question.  
**Nikola Pivcevic:** Is it a c is it new category?  
**Edvinas Rupkus:** I haven't  
**Nikola Pivcevic:** Is it like a a new checkbox? Is it kind of label like like exclusive or featured that we have or is it like a category that will be added to the like current taxonomy or or something completely different, right?  
   
 

### 00:29:10 {#00:29:10}

   
**Nikola Pivcevic:** Like or like for reports we have like a completely separate like kind of section of the of the when inputting the uh the article like we make a completely separate box for  
**Edvinas Rupkus:** Yeah.  
**Nikola Pivcevic:** that.  
**Edvinas Rupkus:** Yeah. Nishan, I can meet and look through the ticket. I haven't like fully read through it uh yet, but my initial thought is that it would probably have to be I don't I don't want to complicate WordPress even more, but probably would be some sort of like box, you know, like include on the election page because I don't want to introduce another category. You could do a tag but then again like we will be at the mercy of the authors remembering to put the tag on. So um it's a good question. Yeah, we can we can go back and discuss what's the right  
**Nikola Pivcevic:** Yeah. And I'm thinking, yeah, whatever wherever that is for for stories,  
**Edvinas Rupkus:** way.  
**Nikola Pivcevic:** the same applies for videos, right? So when we create a video, we will use the same like methodology of adding this video to to this page, right?  
   
 

### 00:30:21 {#00:30:21}

   
**Nikola Pivcevic:** Same checkbox, same whatever, right?  
**Edvinas Rupkus:** Yeah, I think some something like a subcategory under policy maybe would be good, but we can I can chat with Adam, see what what would be preferable from their perspective.  
**Nikola Pivcevic:** Yeah, maybe we can create a new like subcategory something like  
**Edvinas Rupkus:** Yeah. Yeah.  
**Nikola Pivcevic:** that.  
**Edvinas Rupkus:** Yeah. I'll load it  
**Nikola Pivcevic:** Um,  
**Edvinas Rupkus:** down.  
**Nikola Pivcevic:** yeah, that's that's that's mainly and I guess like for now videos will appear only on this page.  
**Edvinas Rupkus:** I think so. Yeah, we haven't we haven't had any like the CTO the uh core template optimization with that. We are attempting to reshape the templates and like incorporate more of the rich media onto the current legacy not legacy but like the current broad pages. So yeah, I think the answer to your question is for now it's just going to be on this page but then probably a fast follow regular articles and homepage other pages as well.  
**Nikola Pivcevic:** Okay. Yeah. So it's just like kind of like I think like I understand like everything about like individual videos just um yeah how how are we going to show like aggregate views of videos right like how how do we decide which goes here and maybe like oh do we show videos on the homepage so or what how do we select which videos are on the homepage or is it just all the latest or is it right like kind of how do we kind of decide which videos appear where?  
   
 

### 00:32:04

   
**Nikola Pivcevic:** Yeah, that's that's I  
**Edvinas Rupkus:** Yeah. Yeah.  
**Nikola Pivcevic:** think  
**Edvinas Rupkus:** The easiest path would be to have like a media uh like media category like you know how you have specific category on that the whole collection uh page. So it that would probably make more sense. But again, Josh has ideas for this that we haven't even we haven't designed to the design uh stage yet. So yeah, that's something definitely that we're going to talk about in the whole CTO CTO conversation. Uh yeah,  
**Nikola Pivcevic:** What's the CEO conversation?  
**Edvinas Rupkus:** the the C that's what Matt calls it. It's uh core template optimization. So like instead of the bright like whole redesign, we'll do like a slimmer version of that and taking a look at specifically homepage homepage article template and data page if we have the bandwidth uh to to optimize it and like you know improve performance etc etc improve circulation objects. So, and include a lot of the rich media stuff where it's appropriate. So if that's a blocker, we can definitely like escalate it and like maybe Josh or somebody from design team can contri can contribute like a collection page where all the media um all the videos live and then the specific ones would be tagged, you know, with like the same subcategory or whatever is the method that we decide on and then that those get pulled into the election coverage landing page.  
   
 

### 00:33:49 {#00:33:49}

   
**Edvinas Rupkus:** But we'll definitely discuss that today on the design  
**Nikola Pivcevic:** Okay.  
**Edvinas Rupkus:** sync.  
**Nikola Pivcevic:** And I think yeah this data will be pulled from somewhere right like we don't need the WordPress for this right I guess for this like report cards if I remember correctly.  
**Edvinas Rupkus:** Yeah, we'll have a exclusive API feed for  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** this ST crypto.  
**Sean Winslow:** from Um,  
**Edvinas Rupkus:** Mike, have we have we had have we received anything from it?  
**Sean Winslow:** What?  
**Edvinas Rupkus:** I haven't like fully read through my inbox. Do do you have anything since the initial call that we had with Stamber Crypto and the Coinbase Coinbase devs?  
**Mike Price:** No new updates since then. Um,  
**Edvinas Rupkus:** Cool.  
**Mike Price:** yeah, haven't heard from  
**Edvinas Rupkus:** I can follow up.  
**Nikola Pivcevic:** Yeah, like there is plenty of work on videos for now,  
**Mike Price:** that.  
**Nikola Pivcevic:** but yeah.  
**Edvinas Rupkus:** Yeah. Yeah. Additionally, I think the poly market stuff would be uh like Marina, I think, is well equipped. I don't know. Tell me if I'm wrong, but I think that since since she's working on the widget implementation for Poly Markets and those events, I think that would be like once she's done with that, she could potentially help out Marina or help out Maria with the broad front end work.  
   
 

### 00:35:08 {#00:35:08}

   
**Edvinas Rupkus:** But I don't know, tell me if if I'm wrong. I was thinking about assigning that stuff to to Marina um like to try and DVD up the work as much as possible if if possible. Would that sound  
**Brian Mendoza:** I like that idea.  
**Nikola Pivcevic:** Yeah,  
**Edvinas Rupkus:** good?  
**Nikola Pivcevic:** I just like uh like uh want to make sure like and I know I'm not like Brian you said like you we're almost done but like I guess like you know migrating finishing the migration to to Max 4 is I think like something that we should you know prioritize. Um yeah like it came up recently to me like oh this is still on the old page right so it's still not migrated and so kind of like you know finally like getting this like um over the finish line it's I think really important for us yeah so I think like if there are like other tickets to be worked on on the migration like maybe you know Marina can can help with that effort I don't know like yeah just a suggestion  
**Brian Mendoza:** Yeah, I think at the moment it's after I deploy this code today, it's just price pages like those that unit and data dashboard and then I'm going to deprecate like an API endpoint, double check the websockets are good and we're good.  
   
 

### 00:36:24 {#00:36:24}

   
**Brian Mendoza:** So, we're getting there. Um, so yeah, I think Maria is good to start because Maria's work she's wrapping up the I saw the Jira ticket. Correct me if I'm wrong, Maria, but it looks like you guys are almost done. I saw a lot of green on the QA comments for stocks and prices. So, I think you you guys are both finishing up and then I think Maria is good to start this and then me and Marina can pick up after or not pick up, you know, help out where we can.  
**Edvinas Rupkus:** Does that sound right? QA and Maria.  
**Ana Benitez:** Uh  
**Edvinas Rupkus:** Sweet.  
**Ana Benitez:** yes.  
**Edvinas Rupkus:** Okay. I'm excited to assign something new to Maria as well. She's probably all knocked forward out, so better things to come. Okay, any other questions in regards to election coverage? I know that there's quite a few tickets on the epic, but u I'll read I'll read through as well all the tickets. Thanks Sean for the diligent work and splitting up into many different uh user stories and we'll go from there.  
   
 

### 00:37:37

   
**Edvinas Rupkus:** We'll start chipping away at it.  
**Sean Winslow:** And yeah, uh, Nicola, one last thing. If you look at ticket one, uh, because I sent this out to Matt and then he got Corey involved, but I don't necessarily know the tagging within WordPress with that that you guys normally use. So, he he gave like a full comment on what would be best for SEO. So, I displayed that in the first ticket. So if you read through that there are some there are some tags that I wrote in there based on what he was discussing. So, but to get election hub landing page.  
**Edvinas Rupkus:** Which one is this? Okay. Yeah, we can take a look at I don't see a  
**Sean Winslow:** No,  
**Nikola Pivcevic:** Okay. Yeah.  
**Sean Winslow:** the Yeah,  
**Edvinas Rupkus:** comment.  
**Nikola Pivcevic:** Look at him.  
**Sean Winslow:** cool. Thank you. Uh the the comment was in I was sharing before I posted anything or brought it to the board. I just did the Google doc  
**Edvinas Rupkus:** Oh, gotcha. Gotcha. Gotcha. Okay, makes sense.  
**Sean Winslow:** that  
**Edvinas Rupkus:** Okay, sounds good.  
**Sean Winslow:** All right, guys. Does anybody else have any more questions?  
   
 

### Transcription ended after 00:39:13

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*