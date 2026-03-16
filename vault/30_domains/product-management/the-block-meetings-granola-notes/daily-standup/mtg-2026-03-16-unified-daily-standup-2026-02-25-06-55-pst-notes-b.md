---
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup - 2026_02_25 06_55 pst - notes by gemini.
context: the-block
created: 2026-03-16
source: granola-manual
---

# 📝 Notes

Feb 25, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivčević](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Panasenko](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~ ~~[Krystof Oliva](mailto:koliva@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMjVUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.gfp6pu8n5yxq) 

### Summary

**Dashboard and Access Deployment Ready**  
Several major tasks, including the data dashboard and access migrations, were finalized and scheduled for deployment following the stand-up meeting. Other technical updates included implementing antibot verification for job subscribe and finishing final adjustments for the multi-course release.

**Cloud Search Data Inconsistencies**  
Significant time was spent debugging a local build issue related to the block pro container, compounded by problems with non-functioning URLs in the application. The team determined that recently imported data and potential lags in the Cloud Search indexing process were likely contributing to the observed inconsistencies.

**Local Build Failure Resolved**  
A major local build failure was traced back to an outdated local repository that resulted from a silently failed pull command, which was quickly resolved. However, debugging efforts for a separate, persistent service issue involving the Redis death loop concluded for the day without a final fix

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

## ALIGNED

* **Local Build Error Debugging Assistance** Maria will receive assistance from Brian and Nikola immediately following the standup to debug her local build error.

* **LMAX Color Update Deployment Process** The LMAX update regarding the green color change will be deployed immediately without requiring a prior review.

* **Learn Page Component Style Update** The iOS version components (iPhone app slider/style) must be incorporated onto the desktop version of the learn page update for Claudine's ticket.

* **Local Reddis Fix Procedure** To fix the local Reddis issue causing the 404 error, the data dump file located at data/Reddis/dump.rdb must be deleted, and data re-imported using make import-data.

* **Cloud Search token re-indexing process** The process for fixing the staging Cloud Search issue involves first running \`import data\` and then executing WordPress commands to clear existing token data from Cloud Search and re-upsert all local data.

* **Local repo reinitialization attempt** Local build issues will be debugged further by Maryia attempting to reinitialize the repository; if unsuccessful, debugging will continue tomorrow morning.

*More details:*

* **Meeting Commencement and Initial Exchange**: The meeting began with informal greetings and a brief discussion about the unofficial "Wednesday frog" rule, which participants Ramuald Vishneuski and Aliaksandr Kryvanosau clarified means "no crabs" on Wednesdays. Sean Winslow noted that Koray Baspinar had changed their meeting background, and Koray Baspinar indicated that they had chosen the current background because they could not figure out how to change the default "white heaven background" ([00:00:00](#00:00:00)).

* **Aliaksandr Kryvanosau's Technical Update**: Aliaksandr Kryvanosau reported that they implemented antibot verification, similar to the newsletter page, for the job subscribe feature, but they still need to determine how to test this new implementation. They also noted that the loading states they had requested from Serena appeared to be completed, as they had already seen comments and implementation details in Figma ([00:01:43](#00:01:43)).

* **Ana Benitez's Migration and Deployment Update**: Ana Benitez is finalizing migration tickets, specifically confirming that the data dashboard and access migrations are complete and ready for deployment today. They mentioned coordinating the deployments with Marina and will subsequently continue working on notification migration tickets ([00:02:56](#00:02:56)). Ana Benitez also alerted the team that they will be unavailable the following day starting at 2:00 p.m. EST due to a flight reschedule, which was part of ongoing flight issues in Mexico ([00:16:07](#00:16:07)).

* **Bohdan Panasenko's Error Resolution and Ticket Finalization**: Bohdan Panasenko confirmed that several tickets are ready for testing, including the one for the error that occurred when deleting a user. They noted that while that specific ticket for the user deletion error is deployed, a new error has emerged that will require a new ticket. Additionally, they are working to finalize a previously ready ticket concerning the updating of display names because a new issue appeared in the solution ([00:02:56](#00:02:56)).

* **Brian Mendoza's Deployment and Poly Market Focus**: Brian Mendoza reported that the Access testing was completed the previous day and they plan to deploy it after Marina deploys the data dashboard. They committed to completing the newsletter signups and investigating any remaining tasks for the Poly Market feature ([00:04:26](#00:04:26)). Brian Mendoza later offered to stay after the meeting to help Maryia Zhynko with an error they encountered ([00:07:30](#00:07:30)).

* **Koray Baspinar's SEO and Content Strategy Update**: Koray Baspinar is focused on performing a keyword gap and competitor analysis to track performance in keyword visibility compared to competitors. They are also developing new evergreen topics for presentation to the team and are finalizing work on "hs," starting a new crawl, and analyzing website crawl data and metadata changes for learning articles ([00:05:45](#00:05:45)).

* **Krystof Oliva's Codebase Cleanup**: Krystof Oliva is continuing work on the ticket to remove large images from the codebase but indicated they had limited time for this task recently. They plan to continue this work and provide a more substantial update on their progress the following day ([00:05:45](#00:05:45)).

* **Maryia Zhynko's Integration and Local Build Issue**: Maryia Zhynko began integrating the script API into the election hub landing page, but encountered a local build error related to the block pro repository ([00:05:45](#00:05:45)). They requested assistance from the team, as Marina also appeared to be experiencing the same issue on their GitHub branch ([00:07:30](#00:07:30)).

* **Marina Lozuk's Poly Market and Deployment Schedule**: Marina Lozuk has been working on Poly Market tasks, primarily fixing issues and making adjustments based on designer feedback. They also started work on the new Poly Market page and planned to release the data dashboard following the stand-up meeting ([00:07:30](#00:07:30)).

* **Mikita Hulis's Multi-Course Release and Legacy Tickets**: Mikita Hulis is finishing the final adjustments for the multi-course release. They also reviewed two older tickets (3620 and 3511), which are related to general course functionality and require both front-end and back-end work. Mikita Hulis and Nikita Orobenko have started collaborating on these two tickets and anticipate completing them by the end of the week ([00:08:56](#00:08:56)).

* **Nikita Orobenko's Campus Backend Migration**: Nikita Orobenko confirmed they finished preparations for the credits normalization migration and will initiate the release for the campus backend. The migration for individual organizations will be applied later as a separate task, and they confirmed they are not currently running into any blockers ([00:10:24](#00:10:24)).

* **Nikola Pivčević's WordPress and LMAX Updates**: Nikola Pivčević is continuing work on WordPress translations and looking into the LMAX update. They confirmed an easy fix for the color update by changing the color to a mint green used on price pages. However, they are having trouble locating new perpetual values in both the development and production APIs, which they suggested should display automatically if added to the API ([00:11:41](#00:11:41)).

* **Ramuald Vishneuski's Campus Work and Audit Test Review**: Ramuald Vishneuski is continuing work on campus tasks, which now includes the migration with Nikita Orobenko, and they will review the fixes made by Nikita Orobenko. Ramuald Vishneuski also expressed concern about a previous audit test score and is actively working on their audit test ([00:13:43](#00:13:43)).

* **Sean Winslow's Task Confirmation and Follow-up**: Sean Winslow is continuing work on Zapier matters. They confirmed with Edvinas Rupkus that they need to incorporate the mobile styling from the iPhone learn app, specifically the slider component, into the ticket for Claudine ([00:14:47](#00:14:47)).

* **Post-Meeting Debugging of Maryia Zhynko's Local Build**: Following the stand-up, Brian Mendoza and Nikola Pivčević worked with Maryia Zhynko to debug their local build error, which showed that the \`block pro\` container was not accessible and that the packages failed to install ([00:17:08](#00:17:08)) ([00:19:49](#00:19:49)). Initial attempts to pull the image and restart services were not immediately successful ([00:18:25](#00:18:25)) ([00:34:01](#00:34:01)). The group determined that the underlying issue was likely that the Redis service was infinitely failing because Maryia Zhynko's ARM machine was using the Valkyrie image instead of the normal Redis image, which resulted in a 404 error because of missing data ([00:44:19](#00:44:19)). They also identified a separate issue with missing data on a dev box price page, which Brian Mendoza suspected was due to recent data changes made by Caesar ([00:55:13](#00:55:13)) ([00:57:58](#00:57:58)).

* **Production Data Testing and URL Issue Investigation**: Maryia Zhynko inquired about testing with production data outside of the production environment, which led to a discussion about getting a production data dump for use in a development box. Nikola Pivčević confirmed that the imported data is nearly current, as it is from the previous night. brian (let me in) reported an issue where URLs within the application were not real, missing an ID in the middle, and determined this was likely a data issue ([00:59:08](#00:59:08)).

* **URL and Cloud Search Analysis**: The team investigated whether the broken URLs were a data issue or potentially related to Cloud Search. brian (let me in) observed that the URL appeared strange generally, and Nikola Pivčević suggested that Cloud Search might be the source of the difference ([01:00:04](#01:00:04)). An attempt to query by ID failed, and Nikola Pivčević noted an issue with a field added recently, suggesting it was not yet indexed ([01:00:04](#01:00:04)).

* **Cloud Search Processing and Potential Deployment**: Nikola Pivčević and brian (let me in) noted that the Cloud Search issue might be temporary while a recently added field finishes processing. brian (let me in) suggested that if the QA process finished, they were open to pushing the code to main the following morning and flipping the ALB, with the caveat that they would immediately flip it back if the broken URL issue persisted ([01:03:29](#01:03:29)). brian (let me in) also confirmed they ran the \`import data\` command the previous night and would run it again ([01:06:21](#01:06:21)).

* **Cloud Search Data Clearance Strategy**: Nikola Pivčević proposed using WordPress commands to clear Cloud Search data for a specific post type, such as tokens, and then re-upserting all data from the dev instance to ensure Cloud Search matched the dev environment. brian (let me in) recalled having a command set for this process, which was previously used for team members ([01:06:21](#01:06:21)). The consensus was to run \`import data\` first, and then follow up with the commands to clear and re-assert the data ([01:08:03](#01:08:03)).

* **Local Build and Yarn Lock Issues**: Maryia Zhynko's local build finished, but Mike Price joined the conversation to discuss related build failures, which were identified as having issues with the \`yarn lock\` and the build process not working ([01:10:10](#01:10:10)). Maryia Zhynko reported that the build failed locally at line 33 in the block pro app Docker file after resolving a conflict and pulling the latest changes. Mike Price noted that the latest CI/CD build had succeeded 37 minutes prior, but mentioned they were upgrading the Node version from 20 to 24, which involved updating the yarn lock ([01:12:18](#01:12:18)).

* **Diagnosing the Build Failure Root Cause**: The team confirmed that Maryia Zhynko had not pulled Caesar's latest changes, which were merged a few hours prior, suggesting their local repository was outdated ([01:14:46](#01:14:46)). After reviewing the error, which involved an "incompatible missing features" spa specifier in a New Relic package, Mike Price traced it to a specific commit that contained the fix and suggested Maryia Zhynko's local code was outdated ([01:16:45](#01:16:45)). The issue was resolved when Maryia Zhynko performed a \`git pull\` in the \`apps/block-pro\` directory, indicating the previous pull had failed silently ([01:19:59](#01:19:59)).

* **Build Optimization and Infrastructure**: Mike Price noted that the current builds were faster due to using Depot, which provided cache optimizations by adjusting the positioning of build arguments to the bottom of the files to prevent cache busting ([01:27:15](#01:27:15)). They explained that this change, along with S3 cache and the persistence of build environments in Depot, resulted in three-minute builds using a 32-core runner, with Rust builds completing in approximately eight seconds ([01:28:16](#01:28:16)).

* **Redis and Dev Box Debugging**: With the build issue resolved, the team returned to debugging the Reddis issue, which involved a "death loop" that started after deleting the dump and running \`import data\` ([01:29:14](#01:29:14)). They confirmed that Reddis was healthy and responsive via the command-line interface, but the block pro application was still showing a 404 error and not appearing in the system ([01:40:11](#01:40:11)). Maryia Zhynko attempted to match files from a Slack message and restart services, but the issue persisted ([01:41:54](#01:41:54)).

* **Conclusion of Debugging Session**: brian (let me in) noted that the service issue seemed related to traffic or the block pro service not being correctly tied in. Maryia Zhynko offered to reinitialize their repository, which was accepted, as brian (let me in) had a conflicting meeting. Nikola Pivčević suggested continuing the debugging session the following morning if Maryia Zhynko was unable to resolve the issue ([01:48:39](#01:48:39)).

### Suggested next steps

- [ ] Sean Winslow will get back to Ramuald Vishneuski soon regarding the test scores and percentages.

- [ ] Aliaksandr Kryvanosau will look into how to test the antibot verification for the subscribe on the jobs page.

- [ ] Ana Benitez will continue with notification tickets on migration.

- [ ] Koray Baspinar will present new type of evergreen topics to the team.

- [ ] Edvinas Rupkus will ask about the new values for perpetuals in the LMAX update.

- [ ] Nikola Pivčević will deploy the LMAX update with the green color change.

- [ ] Sean Winslow will make an update to incorporate the mobile aspect of the iPhone app learn page into the ticket for Claudine.

- [ ] Marina Lozuk will release the data dashboard after the stand up, and Brian Mendoza will deploy Axis after Marina deploys data dashboard, then Brian Mendoza will work on the newsletter signups and check for anything else to do on the Poly Market stuff.

- [ ] Maryia Zhynko will run `make halt` to kill everything.

- [ ] Maryia Zhynko will try reinitializing the repo to fix the breaking issue.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=nPtIcA9dGTX60R23oGzQDxIWOAIIigIgABgBCA&detailid=standard)*

# 📖 Transcript

Feb 25, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Ramuald Vishneuski:** um time ago. Yeah.  
**Aliaksandr Kryvanosau:** Okay, let's sync after the golden  
**Ramuald Vishneuski:** No. Okay.  
**Sean Winslow:** What's up  
**Ramuald Vishneuski:** Cool.  
**Sean Winslow:** everybody?  
**Ana Benitez:** Hello.  
**Sean Winslow:** Little frog and crab start start this  
**Aliaksandr Kryvanosau:** No, no, it it's Wednesday.  
**Sean Winslow:** Wednesday.  
**Aliaksandr Kryvanosau:** No craps.  
**Ramuald Vishneuski:** So what what day we should uh use caps?  
**Aliaksandr Kryvanosau:** on any day but not on Wednesdays.  
**Ramuald Vishneuski:** Okay.  
**Sean Winslow:** Where are you getting these rules from? Or is this a personal  
**Aliaksandr Kryvanosau:** It's a memorable like it's Wednesday,  
**Sean Winslow:** rule?  
**Aliaksandr Kryvanosau:** my dudes. Have you seen this?  
**Sean Winslow:** I have not like I I think I saw it on Instagram. Is that where is that where you saw it?  
**Aliaksandr Kryvanosau:** Oh, it was so long ago, so I don't recall.  
**Sean Winslow:** Yeah. Wednesdays are for frogs for sure.  
**Aliaksandr Kryvanosau:** Thanks.  
**Sean Winslow:** Oh yeah, Cory, no more heavenly background.  
**Koray Baspinar:** I still couldn't figure out how to change that background. So I choose this today. Whenever I open, I see this white heaven background.  
   
 

### 00:01:43 {#00:01:43}

   
**Sean Winslow:** I think you should just switch it up every single time. Just surprise us. Start getting start getting custom focus don't focus  
**Koray Baspinar:** Okay.  
**Sean Winslow:** so much on SEO work. Focus on how you can change your background and the Google  
**Koray Baspinar:** Okay,  
**Sean Winslow:** meets.  
**Koray Baspinar:** we'll do that if traffic drops.  
**Sean Winslow:** All right, everyone. Good. Think we'll get started. Alex.  
**Aliaksandr Kryvanosau:** Okay, so today I looked into how the antibot verification works on the newsletter paper newsletter page and implemented the same thing for the subscribe on the jobs  
**Sean Winslow:** Cool.  
**Aliaksandr Kryvanosau:** but I don't know how to test it yet. So currently looking into that and that's it.  
**Sean Winslow:** Yeah, I don't know if Serena made a comment or if she reached out to you, but when I was with her on the design sync yesterday, she said she was working on the loading um states that you were asking for. So, they should be done fairly soon.  
**Aliaksandr Kryvanosau:** Well, I think they're already done because I already saw some comments and the implementation in the  
   
 

### 00:02:56 {#00:02:56}

   
**Sean Winslow:** Oh,  
**Aliaksandr Kryvanosau:** Figma.  
**Sean Winslow:** awesome. Perfect. Thank you, Anna.  
**Ana Benitez:** Um hello so um I am wrapping all migration tickets. So yesterday data dashboard and access um are done. So we can deploy that today. I already talked with Marina about that and yep we'll be on on ending on those deployments and I will continue with notification tickets on on migration and that's all from my side.  
**Sean Winslow:** Perfect. Thank you,  
**Ana Benitez:** Thank you.  
**Sean Winslow:** Anna. Ronald, what you got going on?  
**Ramuald Vishneuski:** just exploring some features of of Google Meet.  
**Sean Winslow:** I like the look. I like I like the new look. Uh, bow down. What you  
**Bohdan Panasenko:** Yes. So couple of more tickets are ready for testing.  
**Sean Winslow:** got?  
**Bohdan Panasenko:** Um the ticket for error uh when user is being deleted uh is deployed. Well, there is now another error but that's already another ticket. And um there turned out to be some issue with that old ticket for updating display name.  
   
 

### 00:04:26 {#00:04:26}

   
**Bohdan Panasenko:** I don't know how it's occurred, but yeah, I'm working on that.  
**Edvinas Rupkus:** Yeah, the person wanted to change their like back to their legal name essentially. So that's the original origin of it if that's what your question is about them.  
**Bohdan Panasenko:** Yeah. Yeah. No. So, the thing this this this ticket was ready for testing, but then I don't know. I'm pretty sure there was no So, like there there appeared like an one issue with this uh solution and I'm pretty sure it wasn't like this before or either I was blind which is also possible. But yeah, like right now I'm just trying to fix like to finalize this ticket, let's say.  
**Sean Winslow:** Awesome. Thank you, Bon Brian.  
**Brian Mendoza:** Cool. Um, Axis finished testing yesterday, so I'm going to deploy it after Marina deploys data dashboard. And then I'm going to try to crank out the newsletter signups and see if there's anything else to do on the Poly Market stuff. And that's it.  
**Sean Winslow:** Nice. Thank you. Cool.  
   
 

### 00:05:45 {#00:05:45}

   
**Sean Winslow:** Thank you, Brian. Caesar zoom that in. All right, we'll go with Corey.  
**Koray Baspinar:** Hello. Um, I'm working on keyword gap and competitor analysis. There is now ongoing update and I want to see how they perform and we are performing in terms of keyword visibility and how our competitors are uh doing right now and also I'm working on new type of evergreen topics.  
**Sean Winslow:** Perfect.  
**Koray Baspinar:** I will present them to uh team h also finish working on hs and start another crawl and also working on uh our website crawl analysis and learn article metadata changes. That's it.  
**Sean Winslow:** Thank you,  
**Krystof Oliva:** Hi guys,  
**Sean Winslow:** Kristoff.  
**Krystof Oliva:** I have a short update. So I've been working on the remove big images from codebase, but I didn't have so much time. So I'll keep on working on that and hopefully have more updates tomorrow.  
**Sean Winslow:** All right, cool. Thank you, Kristoff Maria. Yeah.  
**Maryia Zhynko:** Uh in the morning I started working with u integration of uh stand with script API to the election uh hub landing page.  
   
 

### 00:07:30 {#00:07:30}

   
**Maryia Zhynko:** But a few hours ago I encountered an error with uh my local builds uh with the block pro report. Also seems that Marina has the same issue with her branch on GitHub. So I would appreciate if someone could help me with that.  
**Sean Winslow:** Uh, is anyone available to help Maria  
**Brian Mendoza:** Yeah,  
**Nikola Pivčević:** We can stay.  
**Brian Mendoza:** stay active.  
**Sean Winslow:** out?  
**Brian Mendoza:** We can see  
**Nikola Pivčević:** Yeah, let's stay after you.  
**Sean Winslow:** Cool. Thank you guys. And thank you, Maria. Marina.  
**Marina Lozuk:** Hello guys. As for me, I've been working on the poly market stuff, mostly fixing and making some tweaks based on the designer commands. So, and also a little bit worked on the poly market again poly market stuff but for the new page. That's it. And after the stand up, I'm going to release the data dashboard.  
**Sean Winslow:** Perfect. Awesome. Thank you, Marina. Nikon. Oh, all right. Go with Nikita Gulis.  
**Mikita Hulis:** Uh yep.  
   
 

### 00:08:56 {#00:08:56}

   
**Mikita Hulis:** Uh continue to work on uh last uh remaining adjustments for the multicourse release as well as uh Rome actually forwarded me two tickets uh a bit older ones but would be nice to have those. Those are after all related to the uh to the course functionality not multicourse but in general both uh both course and multicourse those being 3620 and 3511\. Today I've looked through them. I've recognized that those are older ones and probably leftovers from uh uh Anton M actually. So uh investigated them a bit. Uh it turns out that um previous solution did not work cuz uh it requires both work on front end and back end. Uh so I came to Nikita O uh and we've started to look at them uh together. Uh some progress there but probably will uh finish those two in conjunction with Nig uh tomorrow or Friday. And that's about it. Wrapping up the multi-course ones as well as addressing those two uh those two tickets should be uh should be not much remaining on this front. And that's it.  
   
 

### 00:10:24 {#00:10:24}

   
**Sean Winslow:** Sweet. Thank you, Nikita. Nikita.  
**Nikita Orobenko:** Um pretty much the same as above.  
**Sean Winslow:** Oh,  
**Nikita Orobenko:** Uh but yeah, we finished preparation for the credits normalization migration. Uh we'll be initiating the release for the campus back ends and then we will apply it. Uh the migration for the individuals uh orgs will come um later uh as the separate one. I think that's probably it. And that's  
**Sean Winslow:** That's it. Cool.  
**Nikita Orobenko:** it.  
**Sean Winslow:** Yeah, that you guys haven't been running into issues, right? No blockers or anything.  
**Nikita Orobenko:** Uh no, not not at the moment.  
**Sean Winslow:** Okay. Yeah.  
**Nikita Orobenko:** And waiting for tomorrow's call uh on the uh next step on the campus side.  
**Sean Winslow:** Cool. Yeah. Yeah. We were disc we were having a conversation with Claudine and we definitely need to just make sure that you guys are in sync so she's not doing anything that isn't necessary or vice versa. So cool.  
**Nikita Orobenko:** Yep. Perfect.  
   
 

### 00:11:41 {#00:11:41}

   
**Nikita Orobenko:** Thank you.  
**Nikola Pivčević:** Uh yeah,  
**Sean Winslow:** Nicola  
**Nikola Pivčević:** hello everyone. Uh so yeah, continue working on um the translations for WordPress and also was looking add into the LMAX update. Uh so I updated the color. So that's an easy fix for the and the other ask was for perpetuals like they apparently added new values but I don't see them in the API. And I also tried like the dev and the production API and it's not there.  
**Edvinas Rupkus:** Okay.  
**Nikola Pivčević:** And I think like if they just add it should automatically be displayed. Um I don't know.  
**Edvinas Rupkus:** Gotcha.  
**Nikola Pivčević:** Yeah.  
**Edvinas Rupkus:** I'll I'll ask them.  
**Nikola Pivčević:** Yeah. And I'm preparing. So I don't know. Do they want to like do they want to take a look before we deploy or just deploy? Like it's just the green color change.  
**Edvinas Rupkus:** And let's not no let's not dive in that rabbit hole again. We'll just do changes as they ask.  
**Nikola Pivčević:** Uh no,  
**Edvinas Rupkus:** We don't want to waste your time again for like  
   
 

### 00:12:50

   
**Nikola Pivčević:** I mean like um  
**Edvinas Rupkus:** colors like for for to to see what the colors look like on the dead box.  
**Nikola Pivčević:** yeah.  
**Edvinas Rupkus:** No, that's that's that's fine.  
**Nikola Pivčević:** Okay, let's just so I'll just deploy it. Okay. And yeah, and the color is like the green color like there was weren't specific about which one. So, I took the same color as we use on our price pages and it's like kind of mint green,  
**Edvinas Rupkus:** Yeah,  
**Nikola Pivčević:** whatever.  
**Edvinas Rupkus:** perfect.  
**Nikola Pivčević:** Okay.  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** Thank you.  
**Nikola Pivčević:** Yeah, no problem.  
**Edvinas Rupkus:** I'll have some about the where actually those perpetuals  
**Nikola Pivčević:** If they just add it like Yeah,  
**Edvinas Rupkus:** are.  
**Nikola Pivčević:** if they add it add it to the their API, it should automatically be on our website, right? Shouldn't be shouldn't even require any change from us.  
**Edvinas Rupkus:** Gotcha. Okay.  
**Nikola Pivčević:** Okay. Yeah, that's all.  
**Sean Winslow:** Thank you, Nicola. Yeah, I was a little disappointed when I saw Elmax on here.  
   
 

### 00:13:43 {#00:13:43}

   
**Sean Winslow:** I was just like, "Oh, Jesus Christ." The saga continues.  
**Nikola Pivčević:** It's small thing.  
**Sean Winslow:** All right,  
**Nikola Pivčević:** Not a big  
**Sean Winslow:** cool. Romalt.  
**Ramuald Vishneuski:** Uh hello everybody. Uh so we continue working on campus. Uh now uh we will do migration uh with Nikita and uh uh I will uh take a look at those fixes that Nikita has made um and working on my audit test. That's all.  
**Sean Winslow:** Cool. Thank you, Roma. Yeah, I saw your uh your message. Uh I was going to talk to Ed about that specific like when it comes to the like the actual test scores and everything like that, the percentages.  
**Ramuald Vishneuski:** Mhm.  
**Sean Winslow:** So,  
**Ramuald Vishneuski:** Yeah,  
**Sean Winslow:** I'll get back  
**Ramuald Vishneuski:** I'm pretty sure that uh that score was uh different before. Uh so that's that's why I I have this concern.  
**Sean Winslow:** Okay, cool. Yeah, I'll get back to you soon.  
**Ramuald Vishneuski:** Thank you.  
**Sean Winslow:** Thank you, Roma. Ed, any  
**Edvinas Rupkus:** No,  
   
 

### 00:14:47 {#00:14:47}

   
**Sean Winslow:** updates?  
**Edvinas Rupkus:** just looking through uh providing comments and to Figma files and tickets. Nothing for me. What should I  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** do?  
**Sean Winslow:** Uh yeah, and for me, I'm continuing with the Zapier stuff, but Ed, I actually wanted to ask you real quick. Um yesterday during the design meeting, Josh said to incorporate like the um the mobile aspect like that we have on the the iPhone app, like the learn page into the ticket for Claudine. I just wanted to confirm if that was correct. Do you remember that?  
**Edvinas Rupkus:** I think he meant the uh the iPhone app slider or component like style onto the learn update basically. So that that it sort of works the same way like the mobile version of the learn page desktop.  
**Sean Winslow:** No,  
**Edvinas Rupkus:** Oh my god, this is not coming.  
**Sean Winslow:** I I do that.  
**Edvinas Rupkus:** But yeah, that's what he meant. To make the mobile desktop version with the with the iOS version components one to  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** one.  
   
 

### 00:16:07 {#00:16:07}

   
**Sean Winslow:** Understood. Cool. Yeah, I'll make that update, too. And yeah, that's it on my end. Um, I know people are going to be staying afterwards to help Maria out, but does anybody have anything else they want to bring up?  
**Ana Benitez:** Um, I would like to let you know tomorrow I have a flight at 2:00 p.m. EST. So during the time I'm uh on the airplane, I won't be available. Uh, yeah, just as as a heads up and sorry for the short notice. Uh, it's just because it's flights have been a mess in the country lately. So I was rescheduled and all. Thank  
**Sean Winslow:** Yes, the the snow has really screwed up everyone's lives this past weekend and it snowed again here today.  
**Nikola Pivčević:** Is it because of snow or because of like the assassination of the gang?  
**Sean Winslow:** So,  
**Nikola Pivčević:** Like what was what is it?  
**Ana Benitez:** as uh in my here in Mexico  
**Sean Winslow:** big bowl.  
**Ana Benitez:** is because of all the issues a little bit.  
   
 

### 00:17:08 {#00:17:08}

   
**Edvinas Rupkus:** A little little different little different little different  
**Ana Benitez:** Yes.  
**Edvinas Rupkus:** snow.  
**Ana Benitez:** More like fires. Yeah.  
**Edvinas Rupkus:** Yes.  
**Ana Benitez:** It's so sad.  
**Edvinas Rupkus:** Stay  
**Ana Benitez:** Yeah. area.  
**Krystof Oliva:** ever.  
**Sean Winslow:** Yes, please. Yeah. All right. Yeah. And thank you for letting us know everybody else. Good. All right. Sweet. I'll talk to everyone tomorrow. Enjoy the rest. Later, guys.  
**Brian Mendoza:** Hello.  
**Nikola Pivčević:** Hello.  
**Maryia Zhynko:** Hello.  
**Brian Mendoza:** Want to show your screen?  
**Maryia Zhynko:** Let me just share my  
**Brian Mendoza:** Let's see what's  
**Maryia Zhynko:** screen.  
**Brian Mendoza:** up.  
**Maryia Zhynko:** Okay. Do you see it?  
**Brian Mendoza:** Yes. Whoa. Where are the build  
**Maryia Zhynko:** Yes.  
**Brian Mendoza:** files?  
**Maryia Zhynko:** Um I'm currently on main branch on mono and on main branch on the block pro repo and uh it always fails. Uh somewhere here on the line 33  
**Brian Mendoza:** Oh, wow.  
**Maryia Zhynko:** Three.  
**Brian Mendoza:** I That's a new one.  
   
 

### 00:18:25 {#00:18:25}

   
**Brian Mendoza:** Let's see. All right. Cool. Uh, this is with Mike's changes, right? Let me try. Let me I was running it right now. Let me see. Have you run the new uh mono Nicola?  
**Nikola Pivčević:** Nope.  
**Brian Mendoza:** Let me see. I bet it's broken. So, don't update main then. Probably most  
**Maryia Zhynko:** But also I pulled uh yesterday morning or  
**Brian Mendoza:** likely.  
**Maryia Zhynko:** or the days after the days before uh yesterday uh in the evening and uh it was building fine and it just happened  
**Brian Mendoza:** Okay.  
**Maryia Zhynko:** today.  
**Brian Mendoza:** So, what does this say? This says, okay, what the f\*\*\*? Um, is that comment in So, that's a code comment. Okay. The layer is invalidated. Did you make that comment or was that in the Docker file on line 32?  
**Maryia Zhynko:** Uh, it was on this  
**Brian Mendoza:** Okay.  
**Maryia Zhynko:** file.  
**Brian Mendoza:** Interesting. Oh, I see it.  
**Nikola Pivčević:** Uh yeah,  
**Brian Mendoza:** Yeah, just a separate line of  
   
 

### 00:19:49 {#00:19:49}

   
**Nikola Pivčević:** instead of building, have you tried maybe like pulling the latest  
**Brian Mendoza:** sentence.  
**Nikola Pivčević:** image?  
**Maryia Zhynko:** Just by make a  
**Nikola Pivčević:** Make pull. Yeah. So, so make pull and then uh pull.  
**Maryia Zhynko:** pen.  
**Nikola Pivčević:** So make pull and then is s equals the block pro and maybe try running this like yeah can't that unauthorized What  
**Maryia Zhynko:** Um, this maybe because I just uh reinstalled  
**Brian Mendoza:** Oh,  
**Maryia Zhynko:** Docker.  
**Brian Mendoza:** here you try my command. It's fine. Uh, let me find one for you. Locker, unless it's on Slack. Actually, it doesn't matter here. It's a f\*\*\*\*\*\* GitHub token, but it's only four packages. Try pasting this in your terminal. Check um meet chat. That should work. This is only read. So even if it leaks, nothing bad happens. I think hopefully it's Google Google chat. Try it now. But then this would probably still break if you need to rebuild packages locally, right?  
**Maryia Zhynko:** Mhm.  
   
 

### 00:21:16

   
**Brian Mendoza:** Most likely. Cool. Let me see if I can repro  
**Nikola Pivčević:** So,  
**Brian Mendoza:** this  
**Nikola Pivčević:** So I did re recently this like like pulled the image and then like just uh reinstalled the packages and it worked.  
**Brian Mendoza:** like right now. Right now.  
**Nikola Pivčević:** I don't know like yesterday I think  
**Brian Mendoza:** Okay, I see one. Mine actually just failed but for completely this isn't even the same error log.  
**Nikola Pivčević:** I  
**Brian Mendoza:** So something about this package giving me a 401\. Let me see if I can find  
**Nikola Pivčević:** was getting like this open AI package or whatever what was it like do we introduce like some open  
**Brian Mendoza:** it.  
**Nikola Pivčević:** AI package in the blog  
**Brian Mendoza:** Lot of dependencies. I think this bundle is like six. The image is like six earbutts, huh? It's huge. Campus quiz question answer. Yeah, mine failed, but this is this is not the same error. Yeah, mine fails. Interesting. We should probably have to message Mike unless we can figure this out on the call.  
   
 

### 00:22:44

   
**Brian Mendoza:** Um,  
**Nikola Pivčević:** What failed for you, Brian?  
**Brian Mendoza:** similar thing, something with the yarn lock. It's It's uh the yarn lock or the custom yarn install command, but it's the same exact lines that Maria has. How do they not have Oh, they have markdown. Yay. I sent this. It's And these are the lines Maria had, right? You just said the comment show up in your error messages. So, it's something with yarn and caching, which doesn't sound great. Yep. Same lines. I wonder I bet I wouldn't be surprised if he had to configure something in his local docker maybe or I don't know maybe there's a step he forgot to let us know about but your build works fine Nicola so I'm not sure let me see if there's a mono update in the past  
**Nikola Pivčević:** I didn't Yeah, I didn't update the mono.  
**Brian Mendoza:** like  
**Nikola Pivčević:** I think like Mike pushed some updates last week. I don't think I have those.  
**Brian Mendoza:** it was on Sunday it was on the weekend yeah he was messaging me over the weekend and I was like, "Um, that's that's Yeah, go for it,  
   
 

### 00:23:50

   
**Nikola Pivčević:** Yeah.  
**Brian Mendoza:** bro. Let's see. Trying to find anything that mentions yarn, but Oh, I know. Let me see. What path is this in, Maria? I don't have the tab open. It's the Block Pro Docker file app. Okay, thank  
**Maryia Zhynko:** Yes.  
**Brian Mendoza:** you. Oh, there's a commit called fix attempt from 3 hours ago.  
**Maryia Zhynko:** Okay.  
**Brian Mendoza:** I think uh  
**Maryia Zhynko:** Do I need to append  
**Brian Mendoza:** um I bet you can just check out this branch.  
**Maryia Zhynko:** it?  
**Brian Mendoza:** This um Let me see what Caesar's been up to. Uhhuh. Oh, yeah. Caesar's uh definitely trying stuff here. Check this out. I'm pretty sure this will work. I think we're debugging in main, which is fine, but you should have sent a message maybe.  
**Maryia Zhynko:** This  
**Brian Mendoza:** Yeah. So, get check out that. And I bet that I wouldn't be surprised if that works on  
**Maryia Zhynko:** coming  
**Brian Mendoza:** mono. Yeah.  
   
 

### 00:25:48

   
**Brian Mendoza:** f\*\*\* that. Don't, man. Don't even What even is that? Unless you're working on that, then stop s\*\*\*. Yeah.  
**Maryia Zhynko:** might be because I'm in a bit different um OS.  
**Brian Mendoza:** Gotcha.  
**Maryia Zhynko:** check out.  
**Brian Mendoza:** You got a new computer.  
**Maryia Zhynko:** Uh, no, I'm just working from the laptop, not from the usual Mac Mini.  
**Brian Mendoza:** Gotcha. Gotcha. Gotcha.  
**Maryia Zhynko:** Okay.  
**Brian Mendoza:** I miss Linux sometimes. Is that mint?  
**Maryia Zhynko:** Yes, it is.  
**Brian Mendoza:** Yeah, I would spend too much time fiddling with it and then waste like a week just doing nothing. So, I just stay on Mac.  
**Maryia Zhynko:** I also prefer Mac, but you cannot add RAM to MacBook.  
**Brian Mendoza:** Yeah. Well, you can if you spend like 3,000 bucks,  
**Maryia Zhynko:** It's not that easy as installing it for any other  
**Brian Mendoza:** but  
**Maryia Zhynko:** laptop.  
**Brian Mendoza:** Yeah, if this works, I'll let Caesar know that whatever he's doing is breaking things. Or maybe he was trying to fix a bug from this commit.  
   
 

### 00:27:41

   
**Brian Mendoza:** So, we'll see. I think it worked. No, your packages are installing.  
**Maryia Zhynko:** Yes, it seems like it's  
**Brian Mendoza:** That's where mine failed. I didn't get past this. So, I didn't get past the install. We'll see  
**Maryia Zhynko:** working.  
**Brian Mendoza:** though. No way.  
**Maryia Zhynko:** Oh, wait.  
**Brian Mendoza:** Okay, I bet it's just all this stuff that Mike added.  
**Maryia Zhynko:** Okay.  
**Brian Mendoza:** Um, try this. This is the original commit from the summer. This is what we're we've probably all running on. I'll let them know. I bet Caesar's trying to fix Mike's build then is what's going on. f\*\*\*. Damn. So, it's not So, it's not these changes at all, but I have the same exact message. So, what the f\*\*\*? Could you scroll up a little bit more? Maybe there's something more above there. Um, so it says cache is not writable. SLT temp. Oh, your node version. Interesting.  
   
 

### 00:33:03

   
**Brian Mendoza:** Let me see. And I bet that's why I have the same issue.  
**Nikola Pivčević:** Uh I saw this error and yeah I kind of was able to fix it by pulling the image not building it right and so I kind of pulled the image but maybe now the image is different right when it does do we kind of create a new image I guess we have now a new  
**Brian Mendoza:** Okay.  
**Nikola Pivčević:** image than the one that so when you pull now you pulled the latest latest image and now it's different is I know  
**Brian Mendoza:** I'm not sure. So you're saying when we pull you're saying the image might have changed from the time you pulled it to  
**Nikola Pivčević:** maybe I don't know like may Yeah.  
**Brian Mendoza:** no.  
**Nikola Pivčević:** Did you try the sorry I didn't see like when when did were you able to pull the image? Yeah.  
**Maryia Zhynko:** Yes,  
**Nikola Pivčević:** This thing were you able Okay.  
**Maryia Zhynko:** it succeeded.  
**Nikola Pivčević:** And and can you then like uh yeah try to run this image?  
**Brian Mendoza:** Make sure you check out main.  
   
 

### 00:34:01 {#00:34:01}

   
**Maryia Zhynko:** Make  
**Brian Mendoza:** Oh, sorry. So I'll try to run at you.  
**Nikola Pivčević:** They also don't have traffic.  
**Brian Mendoza:** And you're the block pro is on the latest main, right?  
**Maryia Zhynko:** It's on that commit  
**Brian Mendoza:** Uh pro I mean not mono  
**Maryia Zhynko:** pro. Yes, it's on latest name.  
**Brian Mendoza:** cuz he sent a message about making sure that's updated.  
**Nikola Pivčević:** And yeah, can you can you take a look at logs and see like if uh what's going on inside the container? So monologues. Yeah,  
**Maryia Zhynko:** like  
**Nikola Pivčević:** it's okay. It's running. Yeah. Can you try to open it now again? Maybe like we tried opening it. What? Is this maybe a like routing issue like traffic issue or something like that? Like seems it's running right  
**Maryia Zhynko:** Yes,  
**Nikola Pivčević:** but  
**Brian Mendoza:** Try the homepage, not podcasts. Maybe the traffic file on your local isn't up to date. Oh, what? Never mind. Oh,  
   
 

### 00:37:01

   
**Maryia Zhynko:** I tried podcast because uh  
**Brian Mendoza:** is your mono still on that weird branch or the weird commit from the summer? Yeah, go back to main just because we confirmed that it's none of the updates to  
**Maryia Zhynko:** yes.  
**Brian Mendoza:** mono. And then you I think restarting it will just bring in the traffic changes. You don't need to do anything crazy. So make restart the block. Pro  
**Nikola Pivčević:** Awesome.  
**Brian Mendoza:** Did it work or no? The f\*\*\*? Um, is it HTTP? Just thought I can check the URL. Maybe it f\*\*\*\*\* up. Yes, it looks Wait, type in http slash. You never know. Sometimes it does um s and it breaks things for me. Nope. H Why is it doing this? What the f\*\*\*? Traffic. When something breaks locally, everything breaks. Try this.  
**Maryia Zhynko:** This  
**Brian Mendoza:** Let's see what this looks like for you. Yep.  
**Maryia Zhynko:** one  
**Brian Mendoza:** Go to your dashboard.  
   
 

### 00:40:10

   
**Brian Mendoza:** Top left.  
**Maryia Zhynko:** left. Uh  
**Brian Mendoza:** Yeah. Uh routers  
**Maryia Zhynko:** dashboard  
**Brian Mendoza:** explore. Interesting. It's not running, but we are. We see it running. Uh, go back to services. Maybe it's in services. Yeah. Yeah, it's not showing up. Let me see what mine looks like. Let me run things. Oh, my s\*\*\*'s broken. Nic, what does yours look like? My local is broken now.  
**Nikola Pivčević:** Look, it  
**Brian Mendoza:** It's localhost 8080\.  
**Nikola Pivčević:** looks  
**Brian Mendoza:** I know. I'm pretty sure I've seen this. It does have the Black Pro and it's running, I think, but I just want to double check. So, this is just if we if yours has it and Maria's doesn't, that's just telling us that it's not working or the image isn't being set up on traffic properly on Maria's setup.  
**Nikola Pivčević:** Uh so I have a bunch of yeah rules here. Let me share.  
**Brian Mendoza:** Yeah. Okay.  
   
 

### 00:41:26

   
**Brian Mendoza:** So, that's what it should look like. Um, so TP is not showing up. And yeah, so that's it. I bet it's something with traffic, I guess. But you're running everything on main solution.  
**Nikola Pivčević:** Did you make changes like maybe to uh the Docker Compose file in mono?  
**Maryia Zhynko:** Nope.  
**Brian Mendoza:** Is traffic running? Type in a make PS. Well, yeah, obviously it's never mind. Sorry. It's running because you see the dashboard.  
**Maryia Zhynko:** Look.  
**Brian Mendoza:** Um, start showing  
**Nikola Pivčević:** because like yeah the configuration of traffic is kind of done through it's traffic is uh reading the uh configuration from the containers. So kind of maybe we should restart traffic but like traffic yeah like kind of the nice thing about traffic is it kind of out updates and like you change the settings  
**Maryia Zhynko:** Let's  
**Nikola Pivčević:** and then it's immediately I don't know I never had the issues with traffic.  
**Brian Mendoza:** Um, is your configuration file good? Let's open it. It's in apps. It's in mono Dockercompose or something like that.  
   
 

### 00:42:59

   
**Brian Mendoza:** It's Yeah. Yeah. Docker and then the block.pro.  
**Maryia Zhynko:** compose.  
**Brian Mendoza:** It's going to be the dev one. You ran append, right? Or you ran up when you ran it.  
**Nikola Pivčević:** I think I think he she ran a pend.  
**Maryia Zhynko:** This  
**Brian Mendoza:** Okay. So,  
**Nikola Pivčević:** Yeah.  
**Brian Mendoza:** it's going to be the LP pro-dev.  
**Nikola Pivčević:** So, it's not Yeah.  
**Brian Mendoza:** ML  
**Nikola Pivčević:** Not that one, but uh the block prodev.  
**Brian Mendoza:** that guy. Yep. Oh,  
**Maryia Zhynko:** Okay.  
**Brian Mendoza:** what does mine look  
**Nikola Pivčević:** Oh,  
**Brian Mendoza:** like?  
**Nikola Pivčević:** like is this like should be like uh commented out? Yeah, that's weird.  
**Brian Mendoza:** Oh, mine is the same. Mine is the same. And then what's the block code that look like? It just seems right now like the rules for the block pro aren't applying and that's why she's not seeing the service.  
**Nikola Pivčević:** Oh. It's not. Sorry.  
**Brian Mendoza:** Um.  
**Nikola Pivčević:** The the traffic labels are uh in the blog pro yl not here.  
   
 

### 00:44:19 {#00:44:19}

   
**Brian Mendoza:** Oh,  
**Nikola Pivčević:** Yeah.  
**Brian Mendoza:** it still uses that file.  
**Nikola Pivčević:** Can you open? Yeah. Yeah. Can you open this  
**Brian Mendoza:** Interesting.  
**Nikola Pivčević:** one?  
**Brian Mendoza:** Scroll down. They're there.  
**Nikola Pivčević:** Oh, but this is like very different from like I have like three rules and not like 18 rules. What is this?  
**Brian Mendoza:** The actual file is hold on. It should be fine. Try slashcampus maybe. Well, no. I feel like it's just not working in general. Type in make PS in your console. What does that show us?  
**Maryia Zhynko:** Make  
**Brian Mendoza:** The Black Pro is running traffic. Yeah, that's all you need.  
**Nikola Pivčević:** Like why are there like campus rules?  
**Brian Mendoza:** Wait. Oh, I ran into this.  
**Nikola Pivčević:** What?  
**Brian Mendoza:** Yeah, it's Reddus. It's this f\*\*\*\*\*\* Reddus thing that they said was fine. Um, your Reddus is infinitely dying. Are you on ARM 64 or on AMD or whatever?  
**Maryia Zhynko:** 64\.  
   
 

### 00:45:47

   
**Brian Mendoza:** So, this is an ARM machine. Okay.  
**Maryia Zhynko:** Yes.  
**Brian Mendoza:** you need  
**Nikola Pivčević:** Yeah,  
**Brian Mendoza:** to  
**Nikola Pivčević:** I think delete just delete that file. Is it like that? I think the Is that  
**Brian Mendoza:** I honestly could never fix it.  
**Nikola Pivčević:** it?  
**Brian Mendoza:** I just switched the image to normal Reddus instead of Valky cuz I tried everything that was being suggested and it never worked. So yeah,  
**Nikola Pivčević:** I guess this is not I guess like this is a separate issue like Yeah.  
**Brian Mendoza:** this is not this is not related to your thing at all. Let's  
**Nikola Pivčević:** And this sorry the thing that I shared is my my configuration for the blog pro YML file. I don't know like it's I just have you see under labels I have like three three lines of code and and you have like 20  
**Maryia Zhynko:** Okay. Shall we try this  
**Brian Mendoza:** This will most likely fix it.  
**Maryia Zhynko:** one?  
**Brian Mendoza:** Um, we see the issue in your make PS. It's that Reddus is dying forever.  
   
 

### 00:46:43

   
**Brian Mendoza:** And that's why you have a 404 because it's there's no data. like nothing's showing up because Reddus is not working. So let's open your docker compose arm 64  
**Maryia Zhynko:** Compose  
**Brian Mendoza:** docker/compose 64 sorry and then just replace those with Yep.  
**Maryia Zhynko:** and  
**Brian Mendoza:** I would just yeah restart the whole thing at this point.  
**Maryia Zhynko:** restart.  
**Brian Mendoza:** You can just do reddus but you know just a clean slate. So make down and make append the block pro. It's going to pull the different reddus image. You got to you got it to work on your arm machine. Nicola, I deleted the file or whatever and I looked at the config. I  
**Nikola Pivčević:** uh works for Valkyrie works for me.  
**Brian Mendoza:** didn't  
**Nikola Pivčević:** I think like I just deleted uh so from the data folder I think like can you open the data folder Maria?  
**Maryia Zhynko:** Take  
**Nikola Pivčević:** Yeah. and then Reddis and then yeah this dump I just just deleted it because maybe you don't have to do it right now but like that's how I think like how Caesar helped me like fix my Valky issue because like the dump wasn't compatible something I guess  
   
 

### 00:48:14

   
**Brian Mendoza:** Yeah, checks out. I'll try it again probably later today cuz my should have broken now.  
**Nikola Pivčević:** Yeah.  
**Brian Mendoza:** So, the poll worked for you. And then if this works, we still don't have a working rebuild for you, but at least you're work you're up locally. And then I messaged Mike. Um, and Caesar is literally working on this, I think. So, we can see what they say tomorrow since you're taking off.  
**Maryia Zhynko:** Okay.  
**Brian Mendoza:** Let's check your logs. Is the container fully up yet? Yeah, it's barely spinning up. Let's see. Now we're timing out. So, yeah, looks like we're having some Reddus issues locally, but at least it's not build issues. Why is this happening? Uh, in the other terminal tab, if you make PS is Reddit running now or did it hang up again? Oh, it's still using val key. What the f\*\*\*? Are you Is this Is this ARM?  
**Maryia Zhynko:** Um, you should be  
**Brian Mendoza:** the f\*\*\*.  
   
 

### 00:49:51

   
**Brian Mendoza:** Um, you go to base.yml. Is that what the other one would be on the left side in the compose files in your file tree? Maybe just search in reddus.yml. So go to that directory and compose compose.l  
**Maryia Zhynko:** Great.  
**Brian Mendoza:** ML or you could try deleting the data f the data file but let's just try this because I think will she have to repole her data or will it regenerate it Nicola  
**Nikola Pivčević:** uh she'll have to pull it but that's kind of easy like so kind of like just import data from uh so the same command it's just that like this is like a dump that it's created from radius and that's not compatible but like kind of the export function is compatible I don't know like kind of  
**Brian Mendoza:** Cool. So, we can try to you can try to change Reddit with that YML, Maria, or you can delete the data folder and run a dump. So  
**Nikola Pivčević:** Yeah. Another just the dump. Yeah, just the  
**Brian Mendoza:** you're  
**Nikola Pivčević:** dump.  
   
 

### 00:51:08

   
**Brian Mendoza:** goodbye.  
**Maryia Zhynko:** Okay. And restart  
**Brian Mendoza:** Restart and import data. I  
**Maryia Zhynko:** again.  
**Brian Mendoza:** think  
**Nikola Pivčević:** And I think you need to run uh WordPress to be able to import data,  
**Maryia Zhynko:** Can you  
**Nikola Pivčević:** I guess.  
**Maryia Zhynko:** make print?  
**Brian Mendoza:** Nothing ever works. What's wrong here? Um, is it the lowerase version again? Try the all lower  
**Nikola Pivčević:** What?  
**Brian Mendoza:** case. What? Huh? Uh, capital W lowerase P.  
**Maryia Zhynko:** Okay.  
**Brian Mendoza:** Bro,  
**Maryia Zhynko:** So,  
**Brian Mendoza:** what?  
**Nikola Pivčević:** You  
**Brian Mendoza:** Try running import data. Just see if it works. Uh,  
**Nikola Pivčević:** know,  
**Brian Mendoza:** make import dash data. That's fine. Damn, bro. Nothing is working right now.  
**Nikola Pivčević:** what what I didn't even know like there is like a a make command in part  
**Brian Mendoza:** Oh,  
**Nikola Pivčević:** data.  
**Brian Mendoza:** you run it inside the  
**Nikola Pivčević:** Yeah. Yeah.  
**Brian Mendoza:** CLI.  
**Maryia Zhynko:** I don't mind.  
**brian (let me in):** Hello.  
   
 

### 00:55:13 {#00:55:13}

   
**Nikola Pivčević:** And then in the brackets,  
**Maryia Zhynko:** Hello.  
**Nikola Pivčević:** let me in.  
**brian (let me in):** Bro, nothing works when you want it to. It's so annoying. Okay, I think I'm think we're good. Uh, you see my screen, right?  
**Maryia Zhynko:** Yes.  
**brian (let me in):** Hello. Okay. All right. So, what's going on with this dot box? Hold on. Can we close this up? All right. Is this that one? Look at the What am I doing? This should be here. This should be here. All right. So, you're saying that's probably because there's no IDs, right, in the uh price payloads or whatever. price individual. Oh, right. Okay. So, this yellow's broken. And then, do you happen to have the IDs of any of these, Maria?  
   
 

### 00:56:46

   
**Maryia Zhynko:** U might have ideas but it's not coming to  
**brian (let me in):** Would  
**Maryia Zhynko:** front end some reason.  
**brian (let me in):** it be the same one as production? Let's see. Okay, same ID. So the ID exists then cuz the URL loads in SSR, right?  
**Maryia Zhynko:** Yeah,  
**brian (let me in):** Or no.  
**Maryia Zhynko:** it's not coming to the front and to the  
**brian (let me in):** Okay. So when we fetch this,  
**Maryia Zhynko:** table.  
**brian (let me in):** the ID is not getting pulled in there. And there were no code changes whatsoever and it just stopped  
**Maryia Zhynko:** Yeah, it was uh like conflict resolution and uh then all the data in the table  
**brian (let me in):** working.  
**Maryia Zhynko:** disappeared.  
**brian (let me in):** What's interesting is that like we were talking about, none of these changes look like they would break that. Like you just merged two completely unrelated files. Um, I asked Caesar for his timeline of things because I know he was messing with the dead boxes a lot and I actually had a simil not a similar issue but I had some missing data in another one and it might be related.  
   
 

### 00:57:58 {#00:57:58}

   
**brian (let me in):** Maybe I asked them for a date of changes and specifically if he changed anything in the last week. Um cuz yeah, if you're saying that these worked like at this point, like they shouldn't have broken and it's probably something with the data cuz I'm pretty sure resets it over the weekend as well when we change things. So yeah, and I was telling Anna um cuz all these changes in your ticket are fine. Like she can debug this as is. So worst case we can roll this out because this is all cumulative. These are these are just API routes and pages. Um we can try this in prod and then if it's not working we just flip it off in the ALB and then we figure it out. But I'm pretty sure it's a devbox data issue or something weird like that because your transformer fixed the issue and you're saying this was the one thing that was working since you opened the step box up and Caesar's been making a lot of data changes and just a lot of stuff here.  
   
 

### 00:59:08 {#00:59:08}

   
**brian (let me in):** So, I'm going to lean towards that. Um,  
**Maryia Zhynko:** Is there a way to test somehow it with production data but not in production?  
**brian (let me in):** we could maybe get a dump from production. I'm sure we've done that before, right, Nicola? Just getting a dump and putting it in a dev box or no?  
**Nikola Pivčević:** uh the date all the data should be like imported when you run import  
**brian (let me in):** Oh, let me run that.  
**Nikola Pivčević:** data it's uh it's not live data but it's like  
**brian (let me in):** I guess we can  
**Nikola Pivčević:** from last night I think right so it's it's pretty pretty close  
**brian (let me in):** Nothing ever f\*\*\*\*\*\* works, huh? Data.  
**Nikola Pivčević:** what's the what's the issue exactly sorry like I didn't uh didn't catch  
**brian (let me in):** It's very annoying. Um, so everything's fine except these URLs in the like if you click it, it's not a real URL.  
**Nikola Pivčević:** token Bitcoin  
**Maryia Zhynko:** Yes,  
**Nikola Pivčević:** USD.  
   
 

### 01:00:04 {#01:00:04}

   
**brian (let me in):** Yeah.  
**Maryia Zhynko:** it's missing ID in the middle.  
**Nikola Pivčević:** Yeah, but but you think that's a data issue?  
**brian (let me in):** Yes, because I think that Maria said it was working for a while, right? And there were very few changes being done  
**Maryia Zhynko:** Yes, was working and I was testing it.  
**brian (let me in):** here.  
**Maryia Zhynko:** Uh then um I needed to resolve a conflict and after that uh pull uh it stopped uh showing data in the table.  
**brian (let me in):** Yeah, looks like the URL is weird in general. Let me see the production one. How's your build, by the way, Maria? Or your import?  
**Maryia Zhynko:** It's still pulling 96%  
**brian (let me in):** Cool. Yeah, it got stuck there for a while. Okay. So, yeah, Nicola, it looks like it's a URL because this is  
**Nikola Pivčević:** Yeah,  
**brian (let me in):** production.  
**Nikola Pivčević:** but where why would that be uh any different? So it could be cloud search  
   
 

### 01:01:09

   
**brian (let me in):** Could it be cloud search?  
**Nikola Pivčević:** maybe.  
**brian (let me in):** Let's see. There's a way to query by ID, right?  
**Nikola Pivčević:** Yeah.  
**brian (let me in):** Oh, wait. Don't worry. Let me f\*\*\*\*\*\* Oh, no. 2FA.  
**Nikola Pivčević:** Um,  
**brian (let me in):** Oh, wait. Why is there no 2FA? That's concerning. I'm not going to complain, though. I forgot it was structured query, right? And then just this.  
**Nikola Pivčević:** what do Think like normal  
**brian (let me in):** Nope. How was I? I was just asking  
**Nikola Pivčević:** like like not structure but simple. Yeah. And then try to invalid field name. Oh, f\*\*\*\*\*\* hell. Oh, did I mess it up? How How could I mess it up?  
**brian (let me in):** I know what to  
**Nikola Pivčević:** Sorry.  
**brian (let me in):** do.  
**Nikola Pivčević:** Like uh I just This length uh issue is the field that I added like an hour ago.  
   
 

### 01:02:09

   
**brian (let me in):** Oh,  
**Nikola Pivčević:** Like could it  
**brian (let me in):** wait. No.  
**Nikola Pivčević:** be what is  
**brian (let me in):** Um, is there any way I could do that or is it like until you fix  
**Nikola Pivčević:** what is it like? Oh the name lung in facet lung parameter like what parameter?  
**brian (let me in):** It looks like there's an extra character here. Maybe semicolon amperand \#39 a dot. Oh, what the f\*\*\*? Apostrophe. I don't know. Dang it. Can I query cloud switch from the CLI? It would probably be the same thing.  
**Nikola Pivčević:** But why is it so? Sorry. Um,  
**brian (let me in):** No worries.  
**Nikola Pivčević:** I'm still I'm still like uh like what's what's the wrong with this field processing long? Yeah, I don't see what should be the issue here. Like, yeah, the issue is it's not it's not uh indexed yet, but that does shouldn't mean that oh, this the whole thing fails.  
   
 

### 01:03:29 {#01:03:29}

   
**Nikola Pivčević:** Let's see. Run test search.  
**brian (let me in):** What if I omit it?  
**Nikola Pivčević:** in facet.  
**brian (let me in):** Maybe because it's processing. Maybe that's all it is. Who  
**Nikola Pivčević:** Yeah. Yeah. Weird that like I we cannot like perform a test search here and it's  
**brian (let me in):** knows?  
**Nikola Pivčević:** failed. But I don't know like nothing feels off with this like field specifically. I don't know. It's just that I just recently added and restarted the indexing.  
**brian (let me in):** Well, we can I can debug this when it's um when the field finishes finishes processing, Maria, maybe. Um yeah, it might be cloud search messing up the URLs maybe on this table. But yeah, that's the last thing. And like I said, um if this finishes QA, I'm personally not against pushing this tomorrow when you're online in the morning, uh to main flipping on the ALB, the URLs are broken. All right, flip it right back and then we'll see.  
   
 

### 01:06:21 {#01:06:21}

   
**brian (let me in):** But I do lean toward data issue or staging cloud search issue because we've had a few of those the dead boxes. Um in terms of getting a dump from production make import data does do that and I did run it last night actually. Let me run it again. What? How we got rid of it? Yeah. Okay. I will keep an eye on the cloud search over the next few hours or day.  
**Nikola Pivčević:** Uh what we can do is like there are like commands in WordPress that kind of clear uh cloud search data for a specific post type. So we could potentially like clear everything from cloud search uh for um tokens and then uh reabsert all the data to cloud search from that dev instance. So it's kind of you know cloud search exactly matches uh that dev instance and not like want to do we  
**brian (let me in):** I did that with team members.  
**Nikola Pivčević:** want  
   
 

### 01:08:03 {#01:08:03}

   
**brian (let me in):** So we should be I have a command set somewhere for that.  
**Nikola Pivčević:** Um, I don't remember exactly. Let me find it as  
**brian (let me in):** I got somewhere. Why did my history know?  
**Nikola Pivčević:** well.  
**brian (let me in):** It's where is Isn't there a WordPress CLI, right? from what I remember or something.  
**Nikola Pivčević:** Yeah. Um, yeah, I found it.  
**brian (let me in):** Nice.  
**Nikola Pivčević:** It's pretty old but it's uh yeah we so yeah we should run this uh from yeah from inside the the WordPress container  
**brian (let me in):** So, should I run import data yet or no? Or just run it for now? Run.  
**Nikola Pivčević:** running for data first. Yeah. So that's kind of uh because this those commands will like first command will delete everything  
**brian (let me in):** Uh,  
**Nikola Pivčević:** from ACS for that type and then it will the next one will kind of read the local data and upsert to  
   
 

### 01:10:10 {#01:10:10}

   
**brian (let me in):** I'll run that when this when this is done then because that's going to take like 20 minutes. Cool.  
**Nikola Pivčević:** Yeah.  
**brian (let me in):** Thank you. That might actually work. Oh, what the f\*\*\*? Make a local finish. Maria, nice.  
**Maryia Zhynko:** Yes.  
**brian (let me in):** Does it work now? Uh  
**Nikola Pivčević:** Uh Mike is is calling you. You should  
**brian (let me in):** Yeah,  
**Nikola Pivčević:** probably  
**brian (let me in):** I'm going to tell them right now. You invite people. It was about um the build. I'm pretty sure if it's something bad, he'll probably tell me right now. What was I gonna say? Um what was I gonna do? What was I doing? I forgot what I was doing. God damn. Oh, I'm going to paste this in our  
   
 

### 01:11:33

   
**Nikola Pivčević:** Yeah, that's like um multitasking and then like forgetting what what was I doing  
**brian (let me in):** chat.  
**Nikola Pivčević:** before.  
**Mike Price:** What's up, guys?  
**brian (let me in):** Hello, Mike.  
**Mike Price:** What's going  
**brian (let me in):** Did we figure it out,  
**Mike Price:** on?  
**brian (let me in):** Maria? We're I think we're on the tail end of it. It was uh Red is failing the whole time, so we're good.  
**Mike Price:** Reddis,  
**brian (let me in):** Well, the the rebuild isn't working, I think, still.  
**Mike Price:** the repo's not working. What do you mean?  
**brian (let me in):** But yes,  
**Mike Price:** Uh, for the block for block pro.  
**brian (let me in):** and we're on the latest maintenance,  
**Mike Price:** Oh,  
**brian (let me in):** I believe.  
**Mike Price:** I I we deployed the last few deploys succeeded.  
**brian (let me in):** So,  
**Mike Price:** I built locally. What happened?  
**brian (let me in):** uh, we're having some yarn lock issues.  
**Mike Price:** You upgraded um you pulled the latest. All right. So, if are you building  
   
 

### 01:12:18 {#01:12:18}

   
**brian (let me in):** Yes, Maria,  
**Mike Price:** locally?  
**Maryia Zhynko:** Yes.  
**brian (let me in):** can you take over while I work on the dev box for a little  
**Maryia Zhynko:** Yes.  
**brian (let me in):** bit?  
**Maryia Zhynko:** Uh was building locally. I'm on the latest mono and also on the latest main in uh the block.pro Pro and it fails on the line 33 in U Docker Docker files zlo pro app file.  
**Mike Price:** if I do. The last PR that built successfully was 37 minutes ago. Pro 4029 UI. So this fix pro 4092 UI was the last successful build in the CI/CD. Um where is it? So it's not building for you locally. It's not It is building in the CI/CD though as of 37 37 minutes ago. You said you have the latest mono, correct?  
**Maryia Zhynko:** Yes, but I  
**Mike Price:** So I think the biggest issue is that um we had we the one thing I was wondering I  
**Maryia Zhynko:** can  
**Mike Price:** was worried about and I wanted I I thought I made an announcement in dev was that we are upgrading the node version.  
   
 

### 01:13:41

   
**Mike Price:** Um it was from like version 20 to 24 and that involve uh the yarn lock being updated. Um so yeah so is the dev box failing? Like what what exactly is failing? I'm sorry.  
**Maryia Zhynko:** Uh it was failing on the line 33 in uh the block docker file the block pro app for me locally.  
**Mike Price:** Is that for you locally or in the dev box like for you locally? Okay. Um,  
**Maryia Zhynko:** Wait.  
**Mike Price:** you did a full build. You ran uh make build all that. So, it's failing on the docker during the yarn install. Okay.  
**Maryia Zhynko:** Yes.  
**Mike Price:** You pulled Caesar just merged some things. um for Daniel's thing. Uh when did you because he just merged that in. He merged that in. When did he merge that in? He merged this in a few hours  
**Maryia Zhynko:** Um  
**Nikola Pivčević:** A few hours ago, I  
**Mike Price:** ago. When When was the last time you pulled? Did you pull after his changes or before?  
   
 

### 01:14:46 {#01:14:46}

   
**Maryia Zhynko:** uh before  
**Mike Price:** You pulled before. So, you don't have his latest changes in.  
**Maryia Zhynko:** not the one that Caesar pushed 37 minutes ago.  
**Mike Price:** So, I'm looking at his last push to Maine and it was four hours ago. Yeah. So, he pushed he his last push to main was four hours ago. you pulled when a you said a few hours  
**Maryia Zhynko:** Um,  
**Mike Price:** ago.  
**Maryia Zhynko:** no. Before I I  
**Mike Price:** All right,  
**Maryia Zhynko:** think.  
**Mike Price:** let's look at your Docker. Are you sharing your screen? Let me share your screen because I want to see if you have his changes or not because I  
**Maryia Zhynko:** Nope.  
**Mike Price:** know that it was building like we've been deploying for like the last few days. Um he just pushed things. So yeah.  
**Maryia Zhynko:** I've just pulled uh  
**Mike Price:** All right. So, can you go to Mono in the repo?  
**Maryia Zhynko:** few  
**Mike Price:** Um, like go to the repo your CLI. We're going to reset to just before this change and see if you can build.  
   
 

### 01:15:51

   
**brian (let me in):** We did try that  
**Mike Price:** Um,  
**Maryia Zhynko:** Thank you.  
**brian (let me in):** earlier.  
**Mike Price:** you reset to B00ED6.  
**brian (let me in):** Yes, I think it's actually in the meat chat. Let me see. Oh, no. I opened the new browser. Maria, open the meat chat. Check if the one that we tried was B00. Whatever should be up there.  
**Mike Price:** Yeah,  
**brian (let me in):** Yep. This one, Mike. Bends in EF6.  
**Mike Price:** B 0 is that that be the last successful build.  
**brian (let me in):** Yep. Tried it 50 minutes ago.  
**Mike Price:** Tried it 50 minutes ago and it didn't work. And it also didn't work with the latest things that he did as well. What's What's the error? What's the What is the error message exactly?  
**brian (let me in):** It is I guess we'll see it right now, but it's something like it fails on the yarn lock or the yarn mount path in that 32 33 step.  
   
 

### 01:16:45 {#01:16:45}

   
**brian (let me in):** Uh we'll see it right now, I guess.  
**Mike Price:** You have the the yarn lock file is in the in the black pro repo.  
**brian (let me in):** Uh check your unlike  
**Maryia Zhynko:** which it looks like it's going to  
**brian (let me in):** file.  
**Maryia Zhynko:** build.  
**Mike Price:** All right. Yeah, I fixed it. What was the fix?  
**brian (let me in):** What did you do?  
**Maryia Zhynko:** All all this. Oh  
**brian (let me in):** Oh  
**Mike Price:** No. What does it say?  
**brian (let me in):** no.  
**Maryia Zhynko:** no.  
**Mike Price:** Oh, what's there? Yeah, at the bottom it says  
**brian (let me in):** New relic.  
**Mike Price:** What? Building environment build fail. Ncompatible missing features spa specifier and new relic package. That feels very familiar actually. um that I think I actually get that same issue and that was a fix that came from let me go to the why is my internet creeping um the blockpro so the fix that brought that in and your last deploy your last deploy did pass in the CI/CD D but looking back it was prefix and positive indices I fix a my summaries m open a pi key.  
   
 

### 01:18:46

   
**Mike Price:** Yeah it was this commit that fixed it. Um so I am going to pass this commit over in the chat. Make sure I just want to make sure that your local code has this. All right, just a sanity check. So, click on that. That looks like you have outdated code locally somehow. So, can you check your new your plugins New Relic client client locally and see if you have that? Yeah, I guess you got to search for it.  
**brian (let me in):** soft.  
**Mike Price:** Yeah,  
**brian (let me in):** Oh yeah,  
**Mike Price:** see it has.  
**brian (let me in):** the  
**Mike Price:** So,  
**brian (let me in):** spa.  
**Mike Price:** is this is your Delot Pro repo updated with the latest main? I know it's a stupid question, but that's what's in production and that's why it's the production is building. You're not building locally though. Do you have this or was it maybe perhaps the merge didn't go right if you merged in and there were changes and there was a conflict.  
   
 

### 01:19:59 {#01:19:59}

   
**Maryia Zhynko:** I don't know. I pulled maybe in an hour or two  
**Mike Price:** All right. Just just entertain me. Um cuz your your local doesn't match what's in Maine.  
**Maryia Zhynko:** ago.  
**Mike Price:** Okay. Pull.  
**brian (let me in):** So you're not on a  
**Mike Price:** What does it say? All right.  
**brian (let me in):** branch.  
**Mike Price:** Get What branch are you on?  
**Maryia Zhynko:** Come to  
**Mike Price:** All right.  
**Maryia Zhynko:** me.  
**Mike Price:** Cool.  
**brian (let me in):** Oh  
**Mike Price:** Wait.  
**brian (let me in):** no. Uh, it didn't pull. It didn't pull. Yeah, cancel that.  
**Mike Price:** Stop. It's not going to pass. It didn't pull.  
**brian (let me in):** Control C. That it looks like your main didn't pull earlier, Maria.  
**Mike Price:** Yeah.  
**brian (let me in):** It looks like it failed like silently. So, go to your apps to block out Pro and then pull. So, CD apps block pro and then pull.  
   
 

### 01:20:59

   
**Mike Price:** Yeah. Get pull.  
**brian (let me in):** And then I think it's all going to work now. Let's see.  
**Mike Price:** All right, now you're good. Now try to build it.  
**brian (let me in):** Snoopy.  
**Mike Price:** I'm wondering I'm wondering about Caesar's changes. It says yes to redirect not with red is in the dev box.  
**brian (let me in):** Okay, good start. Is that as far as we've gotten, Ria, or no? Or did I fail after this last time?  
**Maryia Zhynko:** It's going further.  
**brian (let me in):** Okay.  
**Mike Price:** Yeah, it didn't get to this part last  
**brian (let me in):** So,  
**Mike Price:** time.  
**brian (let me in):** it looks like when you pulled main last time, it like failed or whatever and it just didn't spit anything  
**Mike Price:** Yeah.  
**brian (let me in):** out or it got lost in the terminal. But, let's see.  
**Mike Price:** Yeah.  
**brian (let me in):** I'll stick around, but it looks like this probably going to work. These builds are fast, Mike.  
   
 

### 01:27:15 {#01:27:15}

   
**brian (let me in):** Holy s\*\*\*.  
**Mike Price:** loving it. Depot, man. Depot was the game changer. And then on top of that, we got cache optimizations on the images. We were building the images and there was just no caching at all because of the way we were building them before. um we were putting the build arguments up front at the top and that was always cache busting all the layers below it. So we put the build arguments at the bottom because we would take the build arguments and put and assign them as environment variables which would cause the change. So we put them at the bottom and now everything will get cached if there's no changes.  
**brian (let me in):** That makes so much sense.  
**Mike Price:** Um yeah,  
**brian (let me in):** Like that's probably a twoline change, right? Just  
**Mike Price:** it was a two line change that made a huge difference.  
**brian (let me in):** change  
**Mike Price:** But then we added um S3 cache and stuff for the um like we had not S3 cache for node node specifically, but the build environments persist in depot.  
   
 

### 01:28:16 {#01:28:16}

   
**Mike Price:** Um you it's a pain to ever do that in GitHub. You can do it in GitHub actions, but it's a huge pain. Um but depot um it they give you that by default. So we can cache everything and the yarn installs will be much quicker. Um so that gives us our threeminute builds and we're on like 32 a 32 worker runner on depot. So or a 32 core runner. So the Rust builds blow my mind. Those things build in like eight seconds sometimes.  
**brian (let me in):** Yeah, that's insane.  
**Mike Price:** Like are you kidding?  
**brian (let me in):** Like I was telling that's people's biggest complaint. Like, oh my god, it takes a year to compile. But no, it takes eight seconds,  
**Mike Price:** Eight seconds, man. Are you kidding me?  
**brian (let me in):** bro.  
**Mike Price:** Got I gotta brag to Joel about that when I say like, "Guess how guess what my build times are these days." Oh man.  
**brian (let me in):** We're good.  
   
 

### 01:29:14 {#01:29:14}

   
**brian (let me in):** Maria, we're at least on this. looking to figure out the reddest stuff.  
**Mike Price:** Yeah, we're good. We should What's up with Reddus? What's wrong with Reddus?  
**brian (let me in):** Um, it's that Valkyrie thing I ran into, but we got stuck on the build and we didn't try after she fixed it.  
**Mike Price:** Okay,  
**brian (let me in):** Reddus was like in a death loop and we ran import data after deleting the dump, so it should work probably.  
**Mike Price:** gotcha.  
**brian (let me in):** We'll see.  
**Mike Price:** All right, cool. All right. Yeah, that's exporting layers. We're good. Sorry for the um the the the turbulence.  
**brian (let me in):** Oh, we should have checked main. No worries.  
**Mike Price:** It's  
**brian (let me in):** In our defense, we didn't see any errors when we pulled it. So, for sure.  
**Nikola Pivčević:** Bye. Bye.  
**Maryia Zhynko:** All right.  
**brian (let me in):** Can you guys hear that? My neighbors are fighting.  
   
 

### 01:30:12

   
**brian (let me in):** I'm hoping you guys can't hear that. Okay, good.  
**Maryia Zhynko:** No.  
**brian (let me in):** I don't know. Some people stay in relationships and shouldn't stay in, you know? They just be fighting all day.  
**Maryia Zhynko:** Oh,  
**brian (let me in):** But  
**Maryia Zhynko:** I have uh two neighbors who have who fight almost  
**brian (let me in):** yeah,  
**Maryia Zhynko:** every day.  
**brian (let me in):** me too. It's really annoying when I'm debugging something and I'm already annoyed and then they start. I'm like, "God, f\*\*\*\*\*\* damn it, bro.  
**Maryia Zhynko:** Sometimes I wish they scream louder so I would hear why they  
**brian (let me in):** Is it ever interesting or is it always like drama?  
**Maryia Zhynko:** argue.  
**brian (let me in):** Yeah. I don't think I've ever heard an actual valid argument from these guys. It's always some b\*\*\*\*\*\*\*. It's funny.  
**Maryia Zhynko:** Yesterday it built faster. No,  
**brian (let me in):** You're not running anything, are you?  
   
 

### 01:31:35

   
**brian (let me in):** Any services?  
**Maryia Zhynko:** no, I shouldn't.  
**brian (let me in):** At least I made it to this step. Hopefully, it's done soon. Damn, it's still Damn. Maybe hopefully it works. That's taking a minute. That takes like a few seconds for me. That last step.  
**Maryia Zhynko:** Yeah, this is where it turned. Yesterday it was incredibly  
**brian (let me in):** It's getting concerning.  
**Maryia Zhynko:** fast.  
**brian (let me in):** Hopefully, it's fine. Maybe it's making new layers for your because you on a fresh computer and stuff. There you go. Wait, what? I've never seen that.  
**Maryia Zhynko:** Yeah, me too.  
**brian (let me in):** What the f\*\*\* is going on? Yeah, maybe he's just making a bunch of new stuff. Who knows?  
**Maryia Zhynko:** Okay, it's  
**brian (let me in):** Nice.  
**Maryia Zhynko:** done.  
**brian (let me in):** Let's see if it works.  
   
 

### 01:36:44

   
**Nikola Pivčević:** Yeah, maybe try uh removing everything from are you running or stack or or docker?  
**Maryia Zhynko:** Docker.  
**Nikola Pivčević:** Yeah, maybe like if you can open Docker desktop and stop everything from there.  
**Maryia Zhynko:** I don't have Docker desktop.  
**brian (let me in):** Make halt usually kills everything.  
**Nikola Pivčević:** Oh  
**brian (let me in):** Sorry, I was tabbed that. I was helping Marina. Uh, make halt. What? We Are we just trying to kill everything right now or what?  
**Nikola Pivčević:** yeah.  
**brian (let me in):** Okay.  
**Maryia Zhynko:** Yes.  
**brian (let me in):** Yeah.  
**Nikola Pivčević:** Yeah.  
**Maryia Zhynko:** Make what?  
**brian (let me in):** Uh, space. H A L T A L T.  
**Maryia Zhynko:** H  
**brian (let me in):** That's like a kill switch. Sorry, I was tab that. Oh, what the f\*\*\*? Um, orphaned container. What the f\*\*\* is this, man? Um, docker rmi id r  
**Maryia Zhynko:** Okay.  
**brian (let me in):** and then try pasting that ID in  
   
 

### 01:37:47

   
**Maryia Zhynko:** Um,  
**brian (let me in):** bruh. Um, Docker RM just without the I. Try again. It looks like it worked. Nope. Oh my god. Same thing. Dockerrm.container. I'm sorry you're having so many issues, Maria.  
**Maryia Zhynko:** This is insane.  
**brian (let me in):** It's never fun. It's always Okay, hopefully hopefully this is good. It always adds up, man. This turned into a s\*\*\* storm. I think data dashboard deploy is going good, though. Sorry, I was I'm going to go back to that. Let me know. Let me know if there's another error.  
**Maryia Zhynko:** I hope  
**brian (let me in):** Yeah, hopefully not.  
**Maryia Zhynko:** no.  
**brian (let me in):** Okay. data dashboard is alive. We're good. Okay. Oh, I see a bug, but we'll figure that out later.  
   
 

### 01:40:11 {#01:40:11}

   
**brian (let me in):** I see. What we got here? Valky is still blowing up. Could you run make logs reddis or s equals reddis or whatever. Oh. Oh, that works. Cool. I didn't know that worked. Um. Oh, no, that won't work. Yeah. So, uh, break those logs. Uh, make logs SQL reddus. So, it's working. Why is it in a death loop? Go all the way up. I think it's that config issue.  
**Maryia Zhynko:** Create  
**brian (let me in):** Hold on. Can you run make reddis cli make space  
**Maryia Zhynko:** this sha.  
**brian (let me in):** reddus-  
**Maryia Zhynko:** Okay.  
**brian (let me in):** cli that's up um why are you 404ing? Let me get a payload. Let me see if that works.  
   
 

### 01:41:54 {#01:41:54}

   
**brian (let me in):** Let me see what is the payload for this API TV code home. Try getting payload colon. So type type in get space payload colon uh tbcco-ash  
**Maryia Zhynko:** Okay. Call  
**brian (let me in):** homepage.  
**Maryia Zhynko:** H.  
**brian (let me in):** Yeah. So reddus is fine. Um reddis are uh break out of that. So break uh control C that and then make PS.  
**Maryia Zhynko:** Okay.  
**brian (let me in):** So we're healthy. And then the logs in the block pro. What do they say? Are they fine? Cuz you still had a 404, right? Yeah. What the f\*\*\*? Um refresh it. I don't know. Try the homepage instead of podcasts. Same thing. Um, thinking thinking local host 8080 is your Reddus is your the black pro showing up?  
   
 

### 01:43:21

   
**brian (let me in):** Refresh that. Yeah. So,  
**Maryia Zhynko:** first.  
**brian (let me in):** it looks like the block pro is still not showing up here and that's the root issue. Um, and your tra your compos files are the same as ours. We got a mono. I sent you a message on Slack. Could you paste that all in your the blocktop proy? Maybe that'll fix it. Maybe it won't. I'm just trying to match up files now.  
**Maryia Zhynko:** The block pro  
**brian (let me in):** that YML that file we were in earlier. Yep. So, and then make restart the Yeah. Now that I'm remembering you, you run that command. But if that doesn't work, I'm realizing Mike mentioned something about this Nvar and that might break. We'll see right now. And this was also on Friday or when the weekend was doing s\*\*\*.  
   
 

### 01:45:20

   
**brian (let me in):** But Nicola is fine on this end. So we'll see if this works. Yeah, this was in his Slack message. So, if this doesn't work, then we'll try this as well. We'll see. Let's try it up. Is it all the way up? It must be. Yeah, that's all the way up. All right. Um, let's try this new environ. Let me see where even is this TV code. Hold on. Hold on. Check something out. Um I guess in your where even is this? I'm trying to find where he put this file that he sent the Slack message. Um I think app host was renamed or something. Let's try this. Uh, what would I do here?  
   
 

### 01:48:39 {#01:48:39}

   
**brian (let me in):** Try this in your um docker/compose.n um apparently he renamed this as well. I sent him meat chat. Sorry, I'm just sending random s\*\*\* now. Boom. And then inside docker/compose end. Yeah, that one. Yep. And then you have it already. Oh, what the f\*\*\* is that what it is? Just out of curiosity. So you have that already and I didn't. So maybe that's probably why it's broken. Um, try the block code.lohost. local host on your browser. Oh s\*\*\*, I have a meeting in 10 minutes. Let's try to figure this out. Um, try that code.lohost instead of pro. Interesting. Why the f\*\*\* is this breaking? Um,  
**Maryia Zhynko:** Maybe I will try to reinitialize the repo and hopefully it will  
**brian (let me in):** you could try that.  
**Maryia Zhynko:** work.  
**brian (let me in):** Yeah.  
**Maryia Zhynko:** I'm not going to steal more of your time. You spent a lot time with me trying to debug this. Thank  
**brian (let me in):** That's fine. Um, I have a meeting in 10 minutes,  
**Maryia Zhynko:** you.  
**brian (let me in):** so I probably won't be able to help you cuz that takes a minute, right? Like reinitializing everything. Um, I think we left off. It's something with traffic or the service. Something's up here with the uh is this not being tied  
**Nikola Pivčević:** Yeah,  
**brian (let me in):** in?  
**Nikola Pivčević:** maybe we can continue tomorrow morning if you don't figure it out like until  
**Maryia Zhynko:** Okay,  
**Nikola Pivčević:** then.  
**Maryia Zhynko:** I hope it will work. It worked yesterday on this computer and uh today's morning but after build it after build started failing it stopped working.  
   
 

### Transcription ended after 01:51:39

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*