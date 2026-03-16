---
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup - 2026_02_11 06_55 pst - notes by gemini.
context: the-block
created: 2026-03-16
source: granola-manual
---

# 📝 Notes

Feb 11, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivcevic](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Vadimovich](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [Krystof Oliva](mailto:koliva@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMTFUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.600v3w79crf8) 

### Summary

**New Team Member Welcome**  
The meeting began with the welcome and introduction of a new team member specializing in software engineering and AI. Various individuals provided updates on their respective tasks, including resolving Salesforce issues, testing buy buttons and CTAs, and preparing design updates for testing.

**Migration and Deployment Status**  
Multiple teams provided status reports covering critical deployment and migration tasks, such as finishing QA for access and newsletters and planning the deprecation of old services. A major development was the decision to assign a team member to begin building the skeleton for the upcoming significant election coverage task.

**Campus Release Scope Defined**  
The Campus team held a deep discussion regarding the scope of the highly anticipated 16th release, confirming core functionality like filtering and search, but determining that the Stripe integration and related upsell mechanisms must be hidden initially. The release will only include the two main courses, with post-release focus shifting to payment flows and account management.

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

ALIGNED

**Homepage Takeover Assets Upload**

Upload updated homepage takeover assets to dev box for LMX confirmation, launching on 16th.

**Produce Evergreen Content Topics**

Start producing evergreen content based on agreed-upon topics.

**Maria Assigned Election Coverage**

Maria assigned to begin skeleton building work for election coverage.

**Course Video Overview Delivery**

Sean sends course video overview file directly to Nikita O. for upload.

**Review Course Tickets Scope**

Edvinas and Nikita O. sync after daily meeting to review and edit Roma's course related tickets reflecting scope limitation changes.

**White Papers Podcast Deployment**

White papers podcast deployment prioritized after Alex's higher priority Salesforce PR merged. Deployment targeted today or tomorrow.

**Kristoff Onboarding Check-in**

Edvinas and Kristoff huddle after meeting to address Kristoff questions or concerns.

**Hide Upsell UI Display**

Hide upsell UI display during deployment because Stripe integration postponed.

**2011 Course Included Existing Clients**

2011 course included in existing clients’ current upskill LMS access.

**Team Orgs Upsell Mechanism**

Team organizations replace upsell mechanism with 'Contact Admin' placeholder text.

**Ask David Course Completion Time**

Ask David for time estimation per course module or definition of formula for calculating completion hours for interactive courses.

**Admin Field Completion Time**

Add admin field allowing manual input of course completion time instead of calculation or mapping.

**Set Up Course Chaining**

Set up course chaining mechanism (101 until 2011\) immediately to enforce learning path rules.

**Marketing Page Update Scope**

Only team enterprise marketing page updates for 16th release; individual marketing page remains focused on 101 purchase.

*More details:*

* **Welcome and Introductions**: Krystof Oliva was welcomed as a new team member and introduced to Edvinas Rupkus and Sean Winslow. Krystof Oliva is a computer science student specializing in software engineering and AI, and they were previously a developer on the access protocol team. The team generally meets three times a week for daily updates, and Krystof Oliva is based in Prague ([00:00:00](#00:00:00)) ([00:23:45](#00:23:45)).

* **Aliaksandr Kryvanosau's Updates on Salesforce and Dev Box**: Aliaksandr Kryvanosau detailed work on Salesforce, including resolving an issue that required 40 cherry-picks into a new branch for clean-up and retesting. They also fixed a dev box connection issue caused by a long branch name, which had to be shortened. Aliaksandr Kryvanosau is applying small changes to the Salesforce pro part, such as disabling button states and adding error message links, and they are waiting for Li's go-ahead to merge their pull requests ([00:01:09](#00:01:09)).

* **Ana Benitez's Testing and Fixes**: Ana Benitez finished testing the buy button for ETFs on all price pages and will continue working on required fixes for those pages. Their work also includes a WordPress ticket to enable charts on the same pages. Additionally, they finished testing the Google Call-to-Action (CTA) on articles and are reviewing the latest comments from Sean Winslow and Brian Mendoza ([00:02:13](#00:02:13)).

* **Bohdan Panasenko's Development Updates**: Bohdan Panasenko reported that the ticket for the indices design mismatch is ready for testing. They also addressed a bug related to the same open article in the latest section, noting that there is an ongoing discussion despite already replying to Nicole's requested changes ([00:02:13](#00:02:13)).

* **Brian Mendoza's Migration Work and Asset Coordination**: Brian Mendoza successfully deployed the events and team members pages and is now focused on finishing the Quality Assurance (QA) for access and newsletters as part of the migration. The next step for them is planning the deprecation and removal of the old service. Edvinas Rupkus forwarded updated assets for a homepage takeover scheduled for the 16th and asked Brian Mendoza to upload them to the dev box for LMX confirmation ([00:03:53](#00:03:53)).

* **Cesar Paz's Jira and Invoice Management**: Cesar Paz created a new webhook in Jira for Jordan Mendoza to enable the creation of validators that block certain task movements until requirements are met. Cesar Paz is also working on centralizing invoices for services, which requires forwarding emails to Ripley and gathering all invoices into a single account, noting the difficulty due to the number of services and lack of access to all of them ([00:04:57](#00:04:57)). They are also creating a way to access the Learning Record Store (LRS) for the block test box, and the associated task is almost complete, requiring only a new layer for environment variables ([00:06:25](#00:06:25)).

* **Jira Automation Access and Constraints**: Regarding Jordan Mendoza's automation work through an external tool, Cesar Paz confirmed they are creating the necessary requirements, such as establishing validators, but do not have extensive knowledge of the tool itself. They chose this solution instead of granting Jordan Mendoza admin access to Jira, and they noted that while there is a limit on Jira automations, the current usage is deemed acceptable ([00:07:46](#00:07:46)).

* **Koray Baspinar's Content and Research Focus**: Koray Baspinar is working on evergreen topics, and the team agreed on starting the production of evergreen content. They are also analyzing data for reporting, which will be presented at the sync meeting tomorrow, and are conducting keyword research to create a plan for improvement ([00:07:46](#00:07:46)). Koray Baspinar also updated and reviewed the research conducted previously on the multi-language project, which the team plans to re-initiate. Sean Winslow asked Koray Baspinar to review a specific ticket to ensure alignment with their notes ([00:09:13](#00:09:13)).

* **Maryia Zhynko's Bug Fixes and Election Coverage Assignment**: Maryia Zhynko finished fixing bugs on the prices page and requested a new task. Edvinas Rupkus highlighted an overnight issue on the .co site where logged-in users receive a pop-up to connect their wallet ([00:09:13](#00:09:13)). Brian Mendoza is already working on the access issues and plans to address this bug, but Edvinas Rupkus suggested assigning Maria Zhynko to start building the skeleton for the election coverage, which is a significant task and the tickets should be assigned shortly ([00:10:48](#00:10:48)).

* **Marina's Absence and Pond Market Widget Tracking**: Marina was unable to attend the call, but Edvinas Rupkus provided their update, which includes working on the pond market widget and tracking. Marina also helped with the Salesforce migration, which is scheduled for release today, and double-checked the event tracking ([00:11:54](#00:11:54)). Edvinas Rupkus will look into the confusing pond market widget tracking setup to ensure the correct implementation for handling events that might lack a category attribute on the API, which could lead to undefined categories in the Google Analytics 4 (GA4) data ([00:13:14](#00:13:14)).

* **Multicore Support and Marketing Page Review**: Mikita Hulis announced that the multicore support is finally shipped to QA and the focus is now on addressing any feedback from Roma. They also confirmed that they are reviewing the pull request from Alex for the marketing page ([00:14:23](#00:14:23)).

* **Course Upload and Tracking Progress**: Nikita Orobenko reported that they were able to upload the core content both locally and to the dev box, with one subject (D5 2011\) currently working to send correct statements for user progress tracking ([00:14:23](#00:14:23)). They are waiting for David to provide the other subjects, redirects, and course video overviews, and once Cesar Paz makes the LRS available, the progress tracking should begin functioning. Sean Winslow will begin working on the editing aspect of the video overviews and will send them directly to Nikita Orobenko for upload ([00:15:41](#00:15:41)).

* **Reviewing Roma's Tickets for Limited Scope Release**: Edvinas Rupkus noted that Roma sent tickets for review due to the limited scope of the first Minimum Viable Product (MVP) release, and they need to determine the best way to review the tickets without calling out non-working items. Nikita Orobenko suggested a one-on-one sync after the daily meeting to outline what was actually implemented, what is working, and what is not planned for the 16th release, including work related to Stripe integration ([00:16:58](#00:16:58)).

* **Nikola Pivčević's Deployments and Dependencies**: Nikola Pivčević spent the day working on the WordPress video max integration. They plan to deploy a new ratings page to support Callum's growth team efforts and deploy the white papers podcast today ([00:18:08](#00:18:08)). Nikola Pivčević was considering waiting for Aliaksandr Kryvanosau's Salesforce deployment, which is expected within hours, but agreed with Edvinas Rupkus that the Salesforce pull request has a higher priority and that deploying the white papers today or tomorrow is acceptable ([00:19:22](#00:19:22)).

* **Ramuald Vishneuski's Market Duplication and Salesforce Concerns**: Ramuald Vishneuski (Roma) announced that they finished the market duplication tickets and fixed all related issues on their side, and are now focusing completely on campus ([00:20:15](#00:20:15)). They discussed a remaining minor concern with Edvinas Rupkus regarding Salesforce where using the same email could reveal the old user's name and company in the API response, which Lil confirmed was not a significant concern ([00:21:36](#00:21:36)). The updated Figma file is now approved ([00:22:40](#00:22:40)).

* **New Team Member Background and Next Steps**: Krystof Oliva confirmed their background as a student in software engineering and AI, with one year of experience in the access protocol team, and is located in Prague ([00:22:40](#00:22:40)). Edvinas Rupkus and Sean Winslow will sync with Krystof Oliva immediately following the daily call to huddle and answer any questions they may have ([00:24:39](#00:24:39)).

* **Campus Team Sync \- Scope and Implementation Details**: The campus team remained after the daily meeting to discuss the scope of the 16th release ([00:24:39](#00:24:39)). The team confirmed the left rail is complete and the course section has filtering, search capabilities, and cards for the "continue" and "all courses" sections. Due to postponing the Stripe integration, the possibility for upsells needs to be hidden for individual users, though the UI is currently displayed in one place ([00:25:48](#00:25:48)).

* **Course Visibility and Product Strategy**: The team discussed the visibility of unavailable courses, concluding they should be hidden for individuals but potentially shown for team organizations to allow them to contact their manager about updating access ([00:26:54](#00:26:54)). Matt confirmed that the 2011 course will be included for current clients who already have access to the 101 course. The immediate release on the 16th will hide upsells for everyone and may replace the upsell mechanism with a "contact admin" message for team organizations ([00:28:10](#00:28:10)).

* **Course Details and Completion Time Estimation**: The team established that the chaining mechanism, which prevents starting 2011 until 101 is finished, is already complete and can be used. They are waiting for the new course's thumbnail, and the title and description are done or in progress. The course detail model is complete, showing the title, level, and subject count, though the current estimation of one subject equaling one hour of effort is a guess, and a formula or manually set field for course completion time is needed ([00:29:27](#00:29:27)). Sean Winslow committed to asking David for an estimation of how long each module would take ([00:33:19](#00:33:19)).

* **Campus Release Functionality and Post-Release Focus**: The filter/sort option is done, but the system is not yet fully CMI5 compliant, though it is X API compliant, with the goal to add CMI5 support after the release ([00:34:25](#00:34:25)). The initial focus after the 16th will be on finishing the new payment flow, the improved marketing page for individuals, and account management ([00:35:50](#00:35:50)). The individual marketing page will only allow purchasing the 101 course until the Stripe integration is complete, leading to a small mismatch between individual and enterprise marketing pages ([00:38:41](#00:38:41)).

* **Final Campus Scope and Next Steps**: The release will only include the 101 and 2011 courses, and there will be no mini-courses or enhancements like sponsor course and policy filtering at this time ([00:38:41](#00:38:41)). The campus team will edit the relevant tickets to assist Roma with testing, noting that the main outstanding issues are the payment flows and the upsell mechanism ([00:40:02](#00:40:02)).

### Suggested next steps

- [ ] Ana Benitez will continue working on all the fixes needed on the ETF prices pages and the ticket for WordPress to enable charts on these pages.  
- [ ] Edvinas Rupkus will send updated assets for the homepage takeover to Brian Mendoza for upload to the dev box for the ones sent yesterday.  
- [ ] Koray Baspinar will take a look at ticket one sent by Sean Winslow to ensure it lines up with the notes given.  
- [ ] Edvinas Rupkus will send Maryia Zhynko the election coverage tickets right after the call to start the skeleton building for the election coverage.  
- [ ] Sean Winslow will send the course overviews video to Nikita Orobenko to upload and use.  
- [ ] Sean Winslow will ask David for a mental estimation of how long each module would take to complete or if there is a formula he can use.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=A_WzpXkHO6qPWv5p7xTzDxIWOAIIigIgABgBCA&detailid=standard)*

# 📖 Transcript

Feb 11, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Edvinas Rupkus:** It appears we have a new team member in our  
**Sean Winslow:** Oh, Kristoff. Very nice to meet you.  
**Edvinas Rupkus:** meeting.  
**Krystof Oliva:** Hi everyone.  
**Sean Winslow:** Man, I'm Sean. I'm the associate PM here. And we have Ed,  
**Krystof Oliva:** pressure  
**Sean Winslow:** who is the lead PM or one of the lead PMs. And I will be running this meeting today.  
**Edvinas Rupkus:** Yeah, we usually meet uh three times a week. Kristoff. Is that how you pronounce your name, by the way? Kristoff.  
**Krystof Oliva:** of the spine or crystals.  
**Edvinas Rupkus:** Kristoff. Um, and we meet three times a week to discuss the daily, you know, questions and updates basically of what people have been working with. So, welcome to the team.  
**Sean Winslow:** Amen.  
**Edvinas Rupkus:** Nice to meet you.  
**Krystof Oliva:** Thank you.  
**Sean Winslow:** Nice meeting you. I'll get to you towards the end uh just so you get a feel of the flow and we'll begin right now I believe. Yeah. 10:02. So we'll start with Alex.  
   
 

### 00:01:09 {#00:01:09}

   
**Aliaksandr Kryvanosau:** Hello. So today I did some work on the Salesforce. I did some stupid thing there. I merged um from the and from main into this branch. And it would have been fine if we would merge it into dev, but we had to merge it into main. So I had to clean it up. So I did 40 cherry pigs into a new branch to make it a clipier and Roma had to retest it. So my motive for today, work dumber takes longer.  
**Sean Winslow:** I dig the motto. And uh yeah, you saw my note about um the job boards thing that Serena's working. Okay,  
**Aliaksandr Kryvanosau:** Yeah.  
**Sean Winslow:** cool.  
**Aliaksandr Kryvanosau:** So yeah, then I had some issues with the dev box connected with Caesar on it and it turned out that I created too long branch name. So I had to shorted it uh a bit and after that it worked fine.  
**Sean Winslow:** Beautiful.  
**Aliaksandr Kryvanosau:** And then I applied some small changes to the pro part of the Salesforce dis to the disabled state of the button and added link to the error message.  
   
 

### 00:02:13 {#00:02:13}

   
**Aliaksandr Kryvanosau:** And that's it for me.  
**Sean Winslow:** Thank  
**Edvinas Rupkus:** We're waiting on Li's uh go ahead to get those all those forms out  
**Sean Winslow:** you.  
**Edvinas Rupkus:** today. So, I'll keep you posted.  
**Aliaksandr Kryvanosau:** VPRs already. So, I just need a green flag to merge them.  
**Edvinas Rupkus:** Nice. Very  
**Sean Winslow:** Perfect. Awesome. Thank you, Alex. Anna  
**Ana Benitez:** Uh well uh yesterday I finished testing the buy button on for ETFs uh for all prices pages and I will continue today for all the fixes we need worked on on these pages. Uh and also that ticket for WordPress to enable charts on these pages as well. Um, also I finished testing Google CTA uh on articles and I'm just looking at your last comments C with Brian. Uh, and that's all from my side.  
**Sean Winslow:** Cool. Thank you, Anna.  
**Ana Benitez:** Thank  
**Sean Winslow:** Go a bow down.  
**Bohdan Panasenko:** Yes. Uh hi everyone. So the ticket for uh indices design mismatch is ready for testing. And uh I also did like a ticket at uh the bug u uh for the same open article in the latest but uh Nicole requested some changes but I already replied because there is like some discussion but yeah overall like something like This  
   
 

### 00:03:53 {#00:03:53}

   
**Sean Winslow:** That's it. All right. Cool. Thank you. Banan Brian.  
**Brian Mendoza:** I finished deploying the extra the events and team members pages and all that and it went well. Um, so I'm going to go start porting like finish up the QA for access and newsletters and all this little stuff for the migration and then start planning out how we can um deprecate the old service and get rid of it and finish this thing up.  
**Edvinas Rupkus:** Brian,  
**Sean Winslow:** Sweet.  
**Edvinas Rupkus:** I have uh updated assets for the homepage takeover that we're going to launch on or not launch but uh enable on the 16th. Uh and uh I would like to see we probably would need to send them to LMX to like confirm it. So, can we do like can I send you assets and we upload them to the dev box for the one they sent yesterday?  
**Brian Mendoza:** Yep.  
**Edvinas Rupkus:** All right, I'll I'll forward it to Thanks.  
**Brian Mendoza:** Cool.  
**Sean Winslow:** Sweet. Thanks, Brian.  
**Cesar Paz:** Uh, hi. Well,  
   
 

### 00:04:57 {#00:04:57}

   
**Sean Winslow:** Caesar.  
**Cesar Paz:** uh, today I created a new web book in Jira for 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 10 N 108m for Jordan because yeah,  
**Sean Winslow:** Okay. Nice.  
**Cesar Paz:** he needs to create a new in Jira and he needs to create some validators in order to block some movements in the Jira task. Um yeah it's only possible to move the data task uh after uh some requirements. So uh I had to create this uh in addition well I kept working in the uh invoices for our services because now I need to uh forward all invoices all emails with invoices to Ripley uh the law.co go and I need to gather all these invoices in only one account and it's costing me a lot because we have uh several services. Uh I don't have access to all of them. Uh I need to redirect all of these invoices first to a service account because I I want to centralize all these invoices first in order to move forward to reaping the blood of code.  
   
 

### 00:06:25 {#00:06:25}

   
**Cesar Paz:** Um well solving some issues today. A lot of messages from Jordan and Thiago and different books in the dead boxes, different things to fix. Um yeah, now I'm creating uh the way to access to LRS to our block test box. Uh because Nikita told me this now. And that's all. That's all. This one.  
**Sean Winslow:** That's all.  
**Cesar Paz:** Yeah, that task. Uh it's almost completed. Um I only need to uh create a new layer to define new environment variables in the monobox. But yeah, uh maybe there are I don't know five six points and I need to compute only one. Five of them are completed. Uh it's a bit tough. So keep working on this.  
**Sean Winslow:** Is is there anybody because I was talking to Jordan Jordan yesterday and he was saying that he's trying to do a lot of automation stuff with through NAD and I know is there anybody else that can help him out with that or is are you  
**Cesar Paz:** Yeah.  
**Sean Winslow:** the only one that has access to  
   
 

### 00:07:46 {#00:07:46}

   
**Cesar Paz:** Well,  
**Sean Winslow:** everything?  
**Cesar Paz:** I I don't have much idea about this tool. uh I basically creating the things that uh he need. Uh for example, yesterday uh he needed admin access to Jira but finally I prefer well we prefer not to give admin access to anyone to Jira. So we have to uh do another solution and the solution was basically uh to use this tool because by using this tool we okay uh Jordan could create validators and keep working on that. Um yeah uh we check that um we have a limit in the automations we can do uh J but it's under the rad told me that it's under the rad so it's fine um yeah that's what  
**Sean Winslow:** Okay.  
**Cesar Paz:** that's thank  
**Sean Winslow:** All right. Thank you, Caesar  
**Koray Baspinar:** Uh hello everyone and Christoff welcome to the team and uh I am  
**Sean Winslow:** Corey.  
**Koray Baspinar:** working on uh evergreen topics. I presented them to team today. uh we agreed on some topics and we will start producing evergreen content and also I'm playing with uh working on some data uh also my reporting I will pro uh present it tomorrow uh for our s in our sync and other than that I'm working on a keyword research keyword analysis uh how we can  
   
 

### 00:09:13 {#00:09:13}

   
**Sean Winslow:** Awesome.  
**Koray Baspinar:** improve some keywords and how we can improve some keywords more kind of uh creating a plan for that and also I did a research couple of months ago from about our multil- language uh project. So we want to initiate it again and I uh reviewed it and updated it. Uh that's all from my side. Sure.  
**Sean Winslow:** Thank you, Corey. Yeah, I wrote up uh those tickets after you made um your notes that Matt asked you to make. If you could just if if you don't mind if I just send you ticket one. Uh can you just take a look just to make sure that it lines up with the notes that you that you gave me.  
**Koray Baspinar:** Yep. Of course. Of course.  
**Sean Winslow:** Thank you, Maria.  
**Maryia Zhynko:** Today I finished fixing some bugs on prices page and currently I need a new task.  
**Edvinas Rupkus:** So, uh, the thing that came up overnight was, uh, the second time already that it's happened, it looks like, uh, on.co, where a person is logged in to the site to read news and they get the popup to connect their wallet.  
   
 

### 00:10:48 {#00:10:48}

   
**Edvinas Rupkus:** Does anyone know if it's up their head like if we spike that and and if we know the cause of the issue?  
**Brian Mendoza:** I'm working on access already and I saw that thread. I was going to fix it on the way like as a side quest. Um so we can  
**Edvinas Rupkus:** Gotcha. Okay.  
**Brian Mendoza:** keep  
**Edvinas Rupkus:** I was I was potentially I was potentially thinking of uh giving that to Maria. Otherwise, I think we're basically ready to start like the skeleton building for the election coverage. So, all we need to do is really just to assign the the tickets to Maria and we can get started. the like the hero section  
**Sean Winslow:** Awesome.  
**Edvinas Rupkus:** might change a little like it's supposed to be sort of like modular that we can swap in and out like you know a long form video versus a short so there could be like slight changes but I think there's no reason to not begin the work because there's quite a quite a quite a big one so Maria the the uh election coverage tickets should come your probably right after the  
   
 

### 00:11:54 {#00:11:54}

   
**Maryia Zhynko:** That's great.  
**Edvinas Rupkus:** call.  
**Sean Winslow:** Thank you, Maria. Marina.  
**Edvinas Rupkus:** She's uh she let me know that she's she was not able to make today's call, but her her update was that uh she's been  
**Sean Winslow:** Okay.  
**Edvinas Rupkus:** working on the pause market widget thing and tracking everything. She's left comments there. Uh I replied to her, but I don't know if she's had a chance to review that.  
**Sean Winslow:** I think yeah, she left the  
**Edvinas Rupkus:** And then she's she okay and then she's uh  
**Sean Winslow:** comment.  
**Edvinas Rupkus:** helped with the Salesforce migration and obviously this has been planned to release sometime today. Um and she double checked the event tracking. I believe that's the I believe that's related to the I'll look into the uh pond market widget tracking because it's I think it's quite confusing with like the way pod market has set up their events and tags and and markets there. So have to make sure that we're on the same page but that's from  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** Marina.  
**Sean Winslow:** Is that essentially us trying to sync up our G4 data with  
   
 

### 00:13:14 {#00:13:14}

   
**Edvinas Rupkus:** No, it's basically um making sure that we can send the right  
**Sean Winslow:** theirs?  
**Edvinas Rupkus:** events or like or like figure out a way where sometimes a specific uh event which is like the question if I understood correctly her concern is that some um events which is like will Bitcoin hit $100,000 some of those events like if they're created super fast or something and they're just deployed on the they might not have a category attribute on the API. So like if somebody clicks that on our site, it it might not like it might have an undefined category when you look at the J4 data on our side. So if it's it's related to that and we have to just make sure that we have the right implementation to take care of those instances. But yeah,  
**Sean Winslow:** Okay,  
**Edvinas Rupkus:** I'll I'll take a look at it today what she wrote.  
**Sean Winslow:** cool. Thank you. Thank you. Marina Edm on the call today.  
**Edvinas Rupkus:** I don't think so. I think he  
**Sean Winslow:** Okay.  
   
 

### 00:14:23 {#00:14:23}

   
**Sean Winslow:** Nikita  
**Edvinas Rupkus:** might  
**Sean Winslow:** Gulis.  
**Mikita Hulis:** Yep. Well, some happy news. We are finally shipped to QA for the multicore support. So, as of right now, we are focused on of course supporting uh any and all feedback from Roma.  
**Sean Winslow:** Awesome.  
**Mikita Hulis:** uh graciously assigned us a few tickets to track the progress in this regard and also as of right about this moment uh reviewing the PR from Alex uh for the for the marketing page and that's about  
**Sean Winslow:** Thank you so much, Nikita. Oh, and then yeah, I have some updates for you guys after Nikita gives me his  
**Nikita Orobenko:** Yep. Uh so yeah, we were able finally to upload the course both locally and on to the dev box knowing our limitations regarding the missed contents or a lot of different things. But it's working at least one subject from it. it's working cuz I only have on my hands that the D5 2011 uh which will send the correct statements after each lesson completion so we can properly track the progress of the user on our system as well.  
   
 

### 00:15:41 {#00:15:41}

   
**Nikita Orobenko:** Um so there I'm only waiting once uh the David will pass me the other subjects plus uh including the redirects. He said he's working on um the subject video overviews and I suppose the course video overview plus incorporating some feedback uh from somewhere uh about the course itself. So but it's already not that blocking uh for us at least to start  
**Sean Winslow:** Awesome.  
**Nikita Orobenko:** testing and seeing how the things are look how the things looks like. Um so I think that's it. for now and once the Caesar will be able to make uh the LRS available I suppose the progress tracking will start working as  
**Sean Winslow:** Yeah.  
**Nikita Orobenko:** well.  
**Sean Winslow:** Thank you guys very much for really digging down and like conversing with David on this whole situation. I don't know if you guys spoke to him this morning, but he reached out to me finally and then so I'm going to start working on the actual editing aspect of the um video overviews. So he's just sending me some stuff now. So that should be done hopefully by today.  
   
 

### 00:16:58 {#00:16:58}

   
**Sean Winslow:** So I Yeah. So, and then I know he's going to start focusing on yes getting you the rest of the stuff.  
**Nikita Orobenko:** Mhm.  
**Sean Winslow:** So, thank you again. But and I'll I'll send this I don't know where I'm going to send the course overviews, I guess, to David to give to you guys. So,  
**Nikita Orobenko:** Or if if it will be just a video,  
**Sean Winslow:** thank  
**Nikita Orobenko:** uh you can just send it straight to me. So I will upload them and we'll start using  
**Sean Winslow:** All right, you got it.  
**Edvinas Rupkus:** Uh,  
**Nikita Orobenko:** them.  
**Edvinas Rupkus:** one quick thing, Roma sent a couple tickets that we he wants us to review for like, you know, if if requirements changed basically and requirements have changed, we like limited the scope of this first NDP release quite a bit. So, I'm just thinking in my head like what's the best course of action in terms of reviewing those tickets for him to like, you know, not call out things that don't work.  
**Nikita Orobenko:** Uh I think we we can uh just think after the daily uh just uh like 101 uh because I can just describe to you like what we actually did, what's working and what's not being even planned to be released.  
   
 

### 00:18:08 {#00:18:08}

   
**Nikita Orobenko:** uh on the 16th and what we can  
**Edvinas Rupkus:** Okay, perfect.  
**Nikita Orobenko:** actually release right after the 16th uh if we will get some uh if we will have some time to finish our work on the stripe  
**Edvinas Rupkus:** Gotcha.  
**Nikita Orobenko:** integration.  
**Edvinas Rupkus:** Yeah, let's let's sync.  
**Sean Winslow:** Sweet. Thank you, Nikita. Nicola.  
**Nikola Pivčević:** Uh yeah, hello everyone. Uh so um spent most of my day working on the WordPress uh video max integration. Uh making some progress there. And uh two other things. So I'll have I'll deploy today u a new ratings page. I mean like um support for the new ratings page that what's his name? Uh Callum.  
**Edvinas Rupkus:** Callum. Yeah. Callum growth team.  
**Nikola Pivčević:** And uh yeah, we're going to deploy the white papers podcast today. Uh I'm just like I'm not sure, Alex, did you deploy your uh your stuff already? I was planning like kind of to wait on on you finishing your deployment and then then to deploy the white papers.  
   
 

### 00:19:22 {#00:19:22}

   
**Aliaksandr Kryvanosau:** Are you talking about the Salesforce?  
**Nikola Pivčević:** Yeah.  
**Aliaksandr Kryvanosau:** Uh, no. I'm still waiting for a green flag.  
**Edvinas Rupkus:** Yeah. Yeah.  
**Nikola Pivčević:** Okay.  
**Edvinas Rupkus:** We wait for a little  
**Nikola Pivčević:** Do do we know maybe like the expected time?  
**Edvinas Rupkus:** should it should be like like within  
**Nikola Pivčević:** deploy.  
**Edvinas Rupkus:** hours.  
**Nikola Pivčević:** Okay.  
**Sean Winslow:** And you're waiting to deploy the white papers podcast until that's that's  
**Edvinas Rupkus:** Yeah.  
**Nikola Pivčević:** Yeah, I guess maybe we can deploy now.  
**Sean Winslow:** complete.  
**Edvinas Rupkus:** I think Yeah.  
**Nikola Pivčević:** I don't know like  
**Edvinas Rupkus:** I don't know if there's going to be like a conflict or of any sort like you know with with the repositories but if we need to wait like for tomorrow let's say for the white papers it's totally fine like if you know people have  
**Nikola Pivčević:** Okay. Yeah. Yeah.  
**Edvinas Rupkus:** to  
**Nikola Pivčević:** Let's I guess this um Alexis PR has a  
**Edvinas Rupkus:** Yeah. Yeah. That's definitely u more of a You're right.  
**Nikola Pivčević:** priority.  
   
 

### 00:20:15 {#00:20:15}

   
**Edvinas Rupkus:** Yeah. So today or tomorrow for the white papers nothing's going to uh break. So,  
**Nikola Pivčević:** Okay.  
**Edvinas Rupkus:** it's all good. Thanks,  
**Sean Winslow:** Yeah, sweet.  
**Edvinas Rupkus:** Nico.  
**Sean Winslow:** Thank  
**Ramuald Vishneuski:** Uh hello everybody. So uh I will introduce myself. I am K and uh hello Kristoff. Nice to have you in our uh team. Uh so uh today we finished with uh market duplication tickets. Uh finally u all fixes uh fixed from our side. what we had uh from our site some things from Salesforce but that's on their uh side uh and now uh I'm completely on campus and that's all. Yeah.  
**Sean Winslow:** Perfect. Thank you very much, Rald. Yeah, and the Salesforce stuff, that was pretty much what we were discussing in that meeting last week. It was just whether or not they want to include like emails for the for the clients. Yeah. Cool. Thank you, Roma.  
**Edvinas Rupkus:** Oh, sorry. Real quick.  
   
 

### 00:21:36 {#00:21:36}

   
**Edvinas Rupkus:** Uh, I left a comment there in regards to one of those uh things you mentioned, Roma. I again I hadn't chance to like look at the confluence and or the tickets and all the comments  
**Ramuald Vishneuski:** Yeah.  
**Edvinas Rupkus:** there. Uh, so you mentioned if you use the same email again, you had a concern. What what was exactly the concern? I don't know if that's still a problem or not or like a  
**Ramuald Vishneuski:** Um that's still a concern and uh it's on the uh  
**Edvinas Rupkus:** concern.  
**Ramuald Vishneuski:** Salesforce site. So if you use the same email um so first of all you will get in API response u your old uh uh name uh and you basically can reveal uh who is uh under uh someone email you can uh know someone's  
**Edvinas Rupkus:** Oh,  
**Ramuald Vishneuski:** company that Yeah.  
**Edvinas Rupkus:** yeah. This one. Yeah. Yeah. This this one I chatted with Lil. That one's That one's fine. It looks like the second one. So, the link that Alex just sent.  
   
 

### 00:22:40 {#00:22:40}

   
**Edvinas Rupkus:** Thank you, Alex.  
**Ramuald Vishneuski:** until you can basically rewrite uh those uh um names,  
**Edvinas Rupkus:** Uh  
**Ramuald Vishneuski:** company uh all the data uh and uh screw up everything. Uh no, no one will do that of course but uh the thing is that uh you can do that.  
**Edvinas Rupkus:** Gotcha. Yeah, I chatted with Lil. Um, she did not think that that was a that was a concern.  
**Ramuald Vishneuski:** Yeah. Uh that that's very minor.  
**Edvinas Rupkus:** Yeah.  
**Ramuald Vishneuski:** So everything is fine now.  
**Edvinas Rupkus:** Cool. And I I provided that uh updated Figma file. It looks like that's green now. So that's great. Awesome.  
**Sean Winslow:** Thank you, Ralt. And we'll go with Kristoff. So, how's it going, Kristoff? Uh, if you want to make a brief introduction.  
**Krystof Oliva:** Yeah. So, hi guys.  
**Edvinas Rupkus:** What is it?  
**Krystof Oliva:** I'm Kristoff. I'm a chef student. I'm studying computer science. I'm in my last uh semester of studying software engineering and AI.  
   
 

### 00:23:45 {#00:23:45}

   
**Krystof Oliva:** And I've been previously working in the access protocol team as a developer.  
**Edvinas Rupkus:** Awesome.  
**Krystof Oliva:** I kind of went back and forth between front end and back end. So, I have like one year of experience over there. And yeah, I'm happy to join you guys and I'm looking forward to working with you.  
**Edvinas Rupkus:** Uh, what what time zone are you located in in the  
**Krystof Oliva:** I'm located in Prague.  
**Edvinas Rupkus:** world?  
**Krystof Oliva:** in Prague. So it's the minus 6 hours to New York Central  
**Edvinas Rupkus:** Gotcha. Okay, sweet. Awesome.  
**Sean Winslow:** Nice.  
**Krystof Oliva:** Europe.  
**Sean Winslow:** Very nice to meet you, Kristoff. Welcome to the team.  
**Krystof Oliva:** Makes sense.  
**Sean Winslow:** Ed, sorry, Ed, do you have any u updates?  
**Edvinas Rupkus:** Uh, no. And not anything to call out at this moment that I haven't yet. Uh, Kristoff, do you need to like how how long do you think is going to be a check? I can I can just hit you up and we can huddle uh for any questions or concerns you have.  
   
 

### 00:24:39 {#00:24:39}

   
**Edvinas Rupkus:** So that's the only thing on my mind and then like we'll sync with Nikita on the scope of the release the specific requirements.  
**Sean Winslow:** Yeah. Do you want to stay after this or you  
**Edvinas Rupkus:** Yeah. Yeah. Let's Yeah,  
**Sean Winslow:** gonna  
**Edvinas Rupkus:** let's stick around the campus campus squad and we can we can chat and take notes.  
**Sean Winslow:** Sweet. All right, sounds good. Yeah, my my updates are all on campus side as well. So, it's just getting all the icons and graphics together and then eventually editing all this stuff together. So, those are my main updates and then yeah, so if nobody else does anybody else have anything that they want to share. All right. Uh, I'll see you guys tomorrow. Whoever is staying for campus, I'll see you right now. Have a good evening, guys. Bye.  
**Aliaksandr Kryvanosau:** Uh just a question. Do I need to stay here regarding compass?  
**Edvinas Rupkus:** I don't think so.  
**Sean Winslow:** Yeah, I was going to  
   
 

### 00:25:48 {#00:25:48}

   
**Edvinas Rupkus:** I think yeah if if there's no if marketing marketing site  
**Sean Winslow:** say  
**Edvinas Rupkus:** didn't you know what whatever the ticket was create written I feel like that's what we going to implement. So if there are any notes um just handle it. So no worries.  
**Sean Winslow:** Man, you want me to stop sharing my screen or share something  
**Edvinas Rupkus:** Yeah.  
**Sean Winslow:** specific?  
**Edvinas Rupkus:** Do do you want to go to that? Um let me Yeah.  
**Sean Winslow:** What role model was?  
**Edvinas Rupkus:** I don't you were included in that group DM.  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** Okay. Uh can you pull up the 40? Well, I guess yeah,  
**Sean Winslow:** 40\.  
**Edvinas Rupkus:** I guess Nikita. Oh, you can just like spitball stuff and we can you can just take notes and we can like then go back and edit those tickets for Roma as needed. So, whatever is easier for you. I don't think we should do like line by line here together.  
**Nikita Orobenko:** Uh  
**Edvinas Rupkus:** It's going to be a waste of time.  
   
 

### 00:26:54 {#00:26:54}

   
**Nikita Orobenko:** okay. So basically the the left rail uh is done. Uh at least we made it. Uh and depending on the information that the user will have, it will work. Uh no problems there. uh the course section. Um we do have the filtering, the search possibilities, uh the cards uh for the continue section, for the all courses section. The only limit right now since we're postponing um the stripe integration, uh we need to lock um the possibility for the upsell. So at the right top corner  
**Mikita Hulis:** Yeah, yeah, yeah. I've also just recalled that there is no possibility actually,  
**Nikita Orobenko:** there  
**Mikita Hulis:** but the UI is currently being displayed at least in one place here for the upsell. So, I'll I'll hide and add it to the deployment as  
**Nikita Orobenko:** so and since you won't be able to uh you you will be able to see the unavailable course if you don't have an access to it. Uh the problem is I suppose we need somehow to hide it for now.  
   
 

### 00:28:10 {#00:28:10}

   
**Nikita Orobenko:** We can keep it only for the team organizations. So we definitely want to hide it for the individuals but for the team orgs we can show it at least give them the possibility to to contact their org manager you know to see like oh we see you launched the new course so we want to update to it and have an access to it so how we're going to do it or it's also a question to the product and the business side of the whole thing uh when we're launching the new course should that course become the part of the existing uh upskill LMS product. If yes then all of the organization that has already an access to the upskill LMS they will get the access to that course. If we want to not to give anybody the access to that new course, we should create a separate product and then provision the access uh to that separate product for all of the organizations uh that will need that course.  
**Edvinas Rupkus:** I just hit up Matt for that and he's going to tell me hopefully in two seconds.  
   
 

### 00:29:27 {#00:29:27}

   
**Edvinas Rupkus:** He said yes. So, it's included. So,  
**Nikita Orobenko:** Okay.  
**Edvinas Rupkus:** 2011 will be part of what current clients will have.  
**Nikita Orobenko:** Mhm. So that's perfect. Uh no problems on giving the access to the all existing organizations that have an access to the uh 101 already. So for the 16 release, we're hiding the possibility for the upsells. We're hiding the possibilities uh uh as for everybody especially the individuals because we don't have a stripe integration being ready yet that's obvious for the team orgs if  
**Edvinas Rupkus:** Mhm.  
**Nikita Orobenko:** we will be able we will just keep something like contact or admin uh or something replacing uh the upsell mechanism because oh no, if they have the access to the regular course, they will have the access to a new one.  
**Edvinas Rupkus:** Yeah,  
**Nikita Orobenko:** Uh just yeah,  
**Edvinas Rupkus:** they don't they won't have anything to upsell to or to upgrade to.  
**Nikita Orobenko:** excuse me.  
**Edvinas Rupkus:** Yeah.  
**Nikita Orobenko:** Uh it's already a bit uh evenish here.  
**Edvinas Rupkus:** Yeah.  
**Nikita Orobenko:** Uh okay,  
   
 

### 00:30:43

   
**Edvinas Rupkus:** You good?  
**Nikita Orobenko:** so all courses section it's fine. uh we just if we want we need to have the categories uh for the 2011 and 101 we can add like the level categories we can add uh optional pills we can set up the chaining mechanism so if you did not finish the 101 you won't be able to finish the 2011 that mechanism is already done if we want to start using it it's better to do it from the  
**Edvinas Rupkus:** Mhm. Got you.  
**Nikita Orobenko:** Um the thumbnail image for the new course we are still waiting for it. The course title we do have it the description uh either done or in progress. The course overview is in progress uh regarding the video preparation. Um what else? the course detail model uh it's done um because we do have the title the levels like the amount of subjects uh the only thing is that we count each subject as one hour of effort to complete I'm not sure if it's correct way of doing it  
**Mikita Hulis:** But so far we no other one.  
   
 

### 00:32:10

   
**Mikita Hulis:** It's a sort of guest estimation can be done but we would need  
**Nikita Orobenko:** Mhm.  
**Mikita Hulis:** an understanding of a would this be a formula or would would it be like manually set for like as a sort of like part of the description or some like some other field? Right now those two are just equal always  
**Nikita Orobenko:** like five subjects, five hours to complete the course.  
**Mikita Hulis:** one hour for one subject.  
**Nikita Orobenko:** If previously we at least had it, we had the videos which we can sum up and get the total amount of time you need at least to watch all of them. Right now we don't have any videos because the course is interactive uh as  
**Edvinas Rupkus:** Yeah.  
**Nikita Orobenko:** hell.  
**Edvinas Rupkus:** Can we Sean, can we hit up David and ask him if he's like kind of have a mental  
**Nikita Orobenko:** So  
**Edvinas Rupkus:** uh estimation basically for what what he's created or if there's like a formula that he can uh go by to like if there's you know 100 slides that means 20 hours or something like that.  
   
 

### 00:33:19 {#00:33:19}

   
**Nikita Orobenko:** Mhm.  
**Sean Winslow:** meaning ask him ask him how long each module would take essentially.  
**Edvinas Rupkus:** Yeah.  
**Sean Winslow:** All right. Yeah, I can ask.  
**Edvinas Rupkus:** Yeah.  
**Nikita Orobenko:** and just sum  
**Sean Winslow:** Yeah.  
**Mikita Hulis:** And for the implementation purposes n I do suppose that we can just add an additional field  
**Nikita Orobenko:** up. Yep.  
**Mikita Hulis:** which can be filled admin display not calculate anything but  
**Nikita Orobenko:** To each. Mhm.  
**Mikita Hulis:** rather give the ability to just tell from the admin panel that this is how many hours it will roughly take.  
**Nikita Orobenko:** Okay. Okay.  
**Sean Winslow:** Yeah, I'm in I'm talking to him right now about all the video stuff, so I'll just shoot him a message.  
**Mikita Hulis:** Or as an alternative, we can have a mapping,  
**Nikita Orobenko:** Yeah.  
**Mikita Hulis:** but it would not be always truthful like mapping from like the amount of the amount of subjects towards towards ours, which I do suppose that subjects in general can vary a lot.  
**Nikita Orobenko:** Yeah, because the the size of each subject uh will would arrive from uh case to case.  
   
 

### 00:34:25 {#00:34:25}

   
**Nikita Orobenko:** Um okay. Uh so the embedded intro video is done. Uh the actions button we already discussed. Uh if we will replace to contact the or admin uh or otherwise you won't be able to see it.  
**Mikita Hulis:** Some sort of text instead of the action buttons would probably be good in this case until the absolute is done.  
**Nikita Orobenko:** Yeah. Um uh so the filter sort option is done which was not the big part of the we v1 as we planned but we already did it. um no notifications um no update states the company specific pol courses nothing like that. So basically the minimum thing is kind of done.  
**Edvinas Rupkus:** Mhm.  
**Mikita Hulis:** Front end wise,  
**Sean Winslow:** Okay.  
**Mikita Hulis:** a few of those things are handled as well such as like an ability to have sponsor course cards  
**Nikita Orobenko:** We  
**Mikita Hulis:** etc etc but it is not supported on the back end yet.  
**Edvinas Rupkus:** Nice.  
**Nikita Orobenko:** yeah so in terms of supporting the CMI5 right now it's not like CMI5 compliant fully. It's the X API compliance of course, but the difference and the gap between them is not that giant.  
   
 

### 00:35:50 {#00:35:50}

   
**Nikita Orobenko:** So the goal is to adjust and add the support for CMI5 uh right after the release uh or somewhere uh after that because the goal the ultimate goal uh knowing the 3WE constraint was just to make it work uh to track the progress and sync it back uh to our own system so we won't lose it and it will work. Um there are no uh expert possibilities out of the system. Um yet the bills and the badges are configurable through the CLMS already because we do have the custom categories we can set up uh for each of the course like either the level categories or the custom ones. Um and the payment integration will come as the second part of that release. Uh after the 16th once we will finish uh the management for the profile uh the initial purchase flow and the upsell mechanism inside uh inside of the campus. But you already did see uh the design.  
**Sean Winslow:** I was Yeah, I have the design ticket,  
**Edvinas Rupkus:** Okay.  
**Mikita Hulis:** Yeah,  
**Sean Winslow:** too.  
**Nikita Orobenko:** So,  
   
 

### 00:37:18

   
**Mikita Hulis:** basically the first focus of after 16th would be on finishing the the new payment way which is which was postponed in favor of this release as well as I guess from Alex's side a return to the improved version of marketing for individuals tying those together and also at least a portion of the um payment account management  
**Nikita Orobenko:** Yeah. Um, and regarding the chaining mechanism between the courses, uh, we should set up it right now, I suppose, because I see that they should be launched as the learning paths, right?  
**Edvinas Rupkus:** Yeah. One 10 one until one.  
**Nikita Orobenko:** Like one  
**Edvinas Rupkus:** Yeah.  
**Nikita Orobenko:** Okay. Okay. Yeah, I'll add it. Uh so just to um enforce the rule from the  
**Mikita Hulis:** Yeah,  
**Nikita Orobenko:** beginning.  
**Mikita Hulis:** all of the functionality for it is done both ways. So, it's just a matter of configuration.  
**Nikita Orobenko:** Yep. And for the 16th, I suppose we're not updating the individual's marketing page. We only update the team uh marketing page. So the individual side it you will be able to purchase  
   
 

### 00:38:41 {#00:38:41}

   
**Edvinas Rupkus:** Correct.  
**Nikita Orobenko:** only the 101 uh for now at least uh until we will finish the stripe integration.  
**Edvinas Rupkus:** Yep. Yeah. So it'll be a small mismatch, I guess, between the individuals and and enterprise marketing pages, but the enterprise marketing page doesn't have any payment. You know, it's just all going to be the form, the sales sales force form that Alex has been working on. And then we can do a fast follow like you just mentioned where the Stripe integration can you know tie in with the individual marketing page payment flows sort of as this you know the launching point for those payment flows. So that make sense and  
**Nikita Orobenko:** Yep.  
**Edvinas Rupkus:** all the upsells with it.  
**Sean Winslow:** All right. Was there anything else?  
**Edvinas Rupkus:** I I don't think we're going to have any mini courses as of this point, right?  
**Nikita Orobenko:** Yeah, just 101 and  
**Edvinas Rupkus:** Yeah. Okay. So,  
**Nikita Orobenko:** 2011\.  
**Edvinas Rupkus:** this the enhancement to sort of point for now as well, right? It's not it's not that's not included.  
   
 

### 00:40:02 {#00:40:02}

   
**Sean Winslow:** I don't think so. I haven't heard anything about many courses yet.  
**Edvinas Rupkus:** Okay.  
**Nikita Orobenko:** I mean technically each subject of the 2011 is a separate course but it's still the part of the 2011\.  
**Sean Winslow:** Yeah,  
**Nikita Orobenko:** So  
**Mikita Hulis:** It's more soation detail rather than the actuality.  
**Sean Winslow:** I think the mini Yeah, I think the mini courses is supposed to be like for, you know, future branch branching off like when like what David his ideas about um learning tree and stuff like that. So you can branch off and  
**Edvinas Rupkus:** Yeah. Well,  
**Sean Winslow:** level  
**Edvinas Rupkus:** it's also like the the stuff that we covered in the previous ticket where it's like the sponsor course and the the policy,  
**Sean Winslow:** Oh yeah.  
**Edvinas Rupkus:** you know, like all those other uh additional ones that won't be a learning path that won't be 101, 2011, 301, whatever it may be. But we we we don't have them launching it. That's we don't we don't don't need any filtering for him because we just have the learning path 101 and so on. So this is this also can be skipped in testing I  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** guess.  
**Sean Winslow:** Awesome.  
**Edvinas Rupkus:** Okay.  
**Sean Winslow:** Right.  
**Edvinas Rupkus:** All right. We'll we'll we'll go through it and uh edit the ticket to make to help out Roma.  
**Nikita Orobenko:** Yep.  
**Edvinas Rupkus:** But this seems like just only a few only a few things uh in here primarily being the the payment flows and like the upsell of the whole thing.  
**Nikita Orobenko:** All right.  
**Edvinas Rupkus:** So everything else appears to be uh covered. So excellent work team.  
**Sean Winslow:** Yeah, thank you very much,  
**Edvinas Rupkus:** Look looking forward to the retro next week.  
**Sean Winslow:** guys.  
**Nikita Orobenko:** Um, oh yeah. Oh yeah, we definitely needed it. Uh but yeah, let's try our best regarding the last mile uh problems with the contents with everything cuz I suppose that David has like uh a little uh pain in the ass regarding the the review cycles of the contents and adjusting everything for it.  
**Edvinas Rupkus:** Yep.  
   
 

### Transcription ended after 00:42:45

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*