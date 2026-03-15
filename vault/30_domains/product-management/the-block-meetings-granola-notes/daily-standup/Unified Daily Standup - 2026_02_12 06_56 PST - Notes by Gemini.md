# 📝 Notes

Feb 12, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivcevic](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Vadimovich](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [Krystof Oliva](mailto:koliva@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMTJUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.twrgwem90iqv) 

### Summary

**Salesforce Merge and Bug Fixes**  
A critical merge for Salesforce changes initially failed deployment but was successfully resolved by adjusting the required commit message to trigger the deploy process. Technical team members addressed several bugs and fixes, including issues with article display and top navigation bar leaks.

**Prioritizing Researcher Features and QA**  
The team prioritized adding research reports and articles to researcher author pages due to researcher urgency, ensuring the feature would be completed soon. Work progressed on dev box configurations, UI fixes, multiquest release QA support, and an investigation into multilanguage competitors.

**Release Date Change and Final Preparations**  
The due date for the upcoming major release was officially shifted from February 16th to February 17th due to the President's Day holiday. Work continued on preparing video assets, fixing an unexpected style linkage issue between Typical and Campus, and finalizing iOS app updates to use the internal API.

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

NEEDS FURTHER DISCUSSION

**Cesar OKRs Start Plan**

Cesar must start work on OKRs tasks including AWS/GCP cost improvement and creating AI agents via Cloud; detailed discussion needed on AI agent implementation.

**Future Credit System Concept**

Full credit assigning concept needs further discussion after current release; topics include per-course credit limits and expiration handling.

ALIGNED

**Ticket 4436 Feature Prioritization**

Researchers require ability add research reports and articles to author pages; Anna prioritize ticket 4436 deployment this week or next week.

**Rework Branches Based Main**

Sticky banner and data dashboard branches must be reworked; branches must be based on main branch, not dev.

**David Finish Subject Assets**

David required to export four extra subjects and set up redirects after subjects to quizzes; necessary for testing navigation flow.

**Investigate Style Leakage Root Cause**

Mikita found style leakage issue from Typical to Campus; Brian must investigate and identify root cause immediately.

**Release White Papers Podcast**

White papers podcast release scheduled; deploy immediately after standup since Alex finished required work.

**Campus Course Credit Assignment**

Immediate campus course credit assignment decided: current users assigned two additional credits, new users assigned four credits.

**Report Image Ratio Issue**

Potential recirculation component image ratio issue reported; issue information must be dropped in Engineering QA channel.

**Kristoff Pro Data Messaging**

Pro data awareness messaging implemented on data pages (near H1 and under charts); Kristoff assigned task for implementation.

*More details:*

* **Salesforce Merge and Deployment**: Aliaksandr Kryvanosau successfully merged the Salesforce changes, noting that the merge for the "pro part" went smoothly, but the code deployment failed initially ([00:00:00](#00:00:00)). Cesar Paz assisted, and it was discovered that the commit message needed to begin with "merge pull request" to trigger the deploy, which was resolved by Cesar Paz making a proper commit to move the process to code. Aliaksandr Kryvanosau also corrected an error where they merged \`def main\` while attempting to push Salesforce changes into \`dev\`, which was reverted before reaching production ([00:02:27](#00:02:27)).

* **Marketing Page Cleanup and Design Review**: Aliaksandr Kryvanosau is currently cleaning up the marketing ticket related to teams to merge it into \`dev\`, which will allow it to be tested with other campus tickets ([00:02:27](#00:02:27)). Sean Winslow confirmed that Aliaksandr Kryvanosau approved the Serena design for the modal ([00:03:39](#00:03:39)).

* **Testing, Migration, and Bug Fixes**: Ana Benitez reported that they were testing stock and price pages and will continue with ETF pages migration. Ryan fixed bugs reported the previous night, specifically issues with leaks on the top navigation bar and opening articles in a new tab; these tickets are ready, and Ana Benitez will ask Ryan about deploying them today ([00:03:39](#00:03:39)).

* **Article Display Fixes**: Bohdan Panasenko confirmed that the ticket addressing the issue of the same article being displayed in the latest crypto news section is fixed and ready for testing. They also fixed a related issue where the last sponsored article did not contain the last "like" from the sponsored section, noting that the core of the issue seemed to have changed during the NX migration ([00:04:50](#00:04:50)).

* **Researcher Feature Priority**: Edvinas Rupkus requested that ticket 4436, regarding the ability to add research reports and articles to researcher author pages, be pulled in for completion, ideally this week or next week, as researchers are anxious about the feature. Ana Benitez agreed to prioritize this work ([00:06:03](#00:06:03)).

* **Dev Box Tasks and Nominal User Email Forwarding**: Cesar Paz finished the task concerning MVARS for the dev boxes and believes the second task for the dev boxes is also complete, requiring them to speak with Mike to confirm the deployment of a stack with every dev box deployment. They also worked on forwarding emails from nominal users for certain services to \`freeblood.co\` for invoicing, identifying the nominal users by service and sending this information to Matt and Mike for their decision ([00:07:18](#00:07:18)).

* **Future Goals and AI Agents**: Cesar Paz is planning to start new tasks focused on their OKRs, including improving costs in AWS or GCP and initiating the creation of AI agents using Cloud, and Sean Winslow expressed interest in discussing this research further ([00:08:42](#00:08:42)). Sean Winslow mentioned that there is a Cloud Agents SDK that could make the process fairly easy ([00:09:55](#00:09:55)).

* **Multilanguage Investigation and Presentation**: Koray Baspinar worked on a multilanguage investigation, checking competitors, and aiming to create a minimum viable product for the following week. They also finished their presentation scheduled for today ([00:09:55](#00:09:55)).

* **Onboarding and First Task Completion**: Kryštof Oliva had a call with Nicola for an introduction to the repository and WordPress and was assigned their first task: removing links. Kryštof Oliva has completed the main feature for this task and is now working on the remaining polishing and related tasks ([00:11:00](#00:11:00)).

* **UI Fixes and LinkedIn Page Implementation**: Maryia Zhynko completed minor user interface fixes for the stock and prices page. They have begun implementing the elections LinkedIn page, starting with basic markup and the hero component ([00:11:52](#00:11:52)).

* **Google Analytics and Branch Preparation**: Marina Lozuk spent time examining information about Google Analytics and methods for tracking multiple tags for the same event. They also started creating new branches for the sticky banners and the data dashboard, as the previous branches, which were based on \`dev\`, need to be replaced with new ones based on \`main\` ([00:13:14](#00:13:14)).

* **QA Support and Review**: Mikita Hulis is focused on supporting the quality assurance process for the multi-quest release, applying crucial adjustments and waiting for new ones, as well as providing another review of the marketing page based on Aliaksandr Kryvanosau's adjustments ([00:14:27](#00:14:27)).

* **iOS App Updates and API Deployment**: Mike Price worked on iOS app updates, including switching to displaying prices from the company's own API instead of directly from Coin Gecko's native system. They are finishing up notifications, polishing the app, and preparing it for internal testing after merging BQA live fixes. Mike Price also has a pull request out for updating treasuries and creating companies from Slack webhooks and is preparing a new API for deployment today ([00:16:10](#00:16:10)).

* **Simon AI API Testing**: Mike Price mentioned they are currently testing a standalone API for the Simon AI system and plan to deploy it in the next day or so ([00:16:10](#00:16:10)).

* **Asset Status and Release Date Change**: Nikita Orobenko reported that most issues are currently minor and they are adjusting fixes with Nick, but they are waiting for updates on assets from David ([00:18:18](#00:18:18)). Sean Winslow confirmed that they are also waiting for David to send the video assets today and is currently working on the thumbnails. Edvinas Rupkus shared the news that the release due date has been moved from February 16th to February 17th due to the President's Day holiday, providing an extra day ([00:19:27](#00:19:27)).

* **Remaining Assets Needed for Release**: Nikita Orobenko needs David to export four extra subjects and set up redirects from the subject end to the quizzes to test navigation, as they can currently only test one subject ([00:20:25](#00:20:25)).

* **Style Linkage Investigation**: Mikita Hulis found a style linkage issue today, seemingly new, between Typical and Campus, which they temporarily circumvented from the Campus site. They have notified Brian Mendoza for investigation, noting that it should not hinder the release, but they cannot identify the root cause of the leakage ([00:21:41](#00:21:41)).

* **Deployment of Small Fixes and Style Leakage Concern**: Brian Mendoza plans to deploy two small fixes today: opening articles in a new tab and another small fix from Slack concerning a price URL issue. They also expressed concern over the unexpected style linkage issue reported by Mikita Hulis, which seems to have appeared randomly from a feature released two months ago, and they will look into it today ([00:22:42](#00:22:42)).

* **Video Integration and White Paper Release**: Nikola Pivčević spent time onboarding Kryštof Oliva and preparing their first task. They are making good progress on video integration, noting that the WordPress part is almost complete, and they are now creating a proof-of-concept component on the front end by reusing an existing Campus video component. Nikola Pivčević also confirmed that they will focus on releasing the white papers podcast after the stand-up meeting, since Aliaksandr Kryvanosau finished their work ([00:24:38](#00:24:38)).

* **Campus Visuals and Credit System Discussion**: Ramuald Vishneuski is working on minor visual tasks for the Campus backend. They discussed the credit system with Nikas, agreeing to assign two additional credits for all users for the one course currently available, with new users receiving four credits. Ramuald Vishneuski noted that a more comprehensive discussion regarding the credit assignment concept, including credit expiration and test cases, needs to happen after the current release ([00:25:48](#00:25:48)).

* **Recirculation Component Issue and Pro Data Awareness Ticket**: Edvinas Rupkus identified a potential issue with the recirculation component where image ratios appear inconsistent and will post the details in the engineering quality assurance channel for Mike Price to review. Edvinas Rupkus will also write a small ticket for "pro data awareness," which involves adding a message next to the H1 on data pages and beneath charts to surface the availability of pro data services ([00:28:13](#00:28:13)). Kryštof Oliva was suggested as a candidate to handle the "pro data awareness" ticket ([00:28:13](#00:28:13)).

### Suggested next steps

- [ ] Ana Benitez will ask Ryan if the fixed bugs on the top n bar and for opening articles on a new tab can be deployed today.  
- [ ] Cesar Paz will start new tasks to complete or start his OKRs, including improving the cost in AWS/GCP and starting to create AI agents using Cloud, and will keep Sean Winslow posted about the AI agents creation.  
- [ ] Brian Mendoza will investigate the style linkage that Nikita Orobenko found, which seems to stem from a later feature.  
- [ ] Nikola Pivčević will focus on releasing the white papers podcast after stand up.  
- [ ] Edvinas Rupkus will send the potential issue with the recirculation component and image ratio to the engineering QA channel and write a small ticket for pro data awareness.  
- [ ] Kryštof Oliva will take on the ticket for pro data awareness, adding a message next to the H1 and underneath the chart on individual charts for data pages.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=HWG-NFhG_wid512ahudsDxIWOAIIigIgABgBCA&detailid=standard)*

# 📖 Transcript

Feb 12, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Koray Baspinar:** Hey  
**Bohdan Panasenko:** Hi.  
**Edvinas Rupkus:** Everyone.  
**Kryštof Oliva:** Yes.  
**Sean Winslow:** How's it going, Kristoff? Kristoff, have you been have you been set up uh on Jira yet on Confluence?  
**Kryštof Oliva:** Yeah. Yeah. I'm Christoph. You missed an F. But there there I am the fifth or  
**Sean Winslow:** Oh, say gotcha.  
**Kryštof Oliva:** sixth.  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** Can we change that? Is that Can you change that or do we have Caesar? Uh, go ahead and change it. Your name is incorrect. Did Did you try to change it, Kristoff?  
**Kryštof Oliva:** No, I didn't.  
**Cesar Paz:** Uh,  
**Edvinas Rupkus:** I think I think a little too.  
**Cesar Paz:** should I have  
**Edvinas Rupkus:** Yeah.  
**Sean Winslow:** Yeah, I think I'm sure you can go into your uh profile settings, but yeah, we'll figure that out. It's not important right now. We'll get to that later. For now, we will start with  
**Aliaksandr Kryvanosau:** Hello.  
**Sean Winslow:** Alex.  
**Aliaksandr Kryvanosau:** So today in the morning I got a green flag to merge the Salesforce.  
   
 

### 00:02:27 {#00:02:27}

   
**Aliaksandr Kryvanosau:** It went smoothly for the pro part but didn't so well for the code. So I had to reach to Caesar to know why it's didn't deploy. Turn out that the to trigger the deploy the commit message must start with um merge pull request and because my pull request contained only cherrypics it had a different me message I think. So uh Caesar had to m a proper commit to trigger deploy and now it's on code. So Salesforce has reached both sides which is great.  
**Sean Winslow:** Awesome.  
**Aliaksandr Kryvanosau:** Yes. So then I wanted to push this uh Salesforce changes into dev because they are required for the marketing page and I messed up a little bit and measured the def main but luckily the message was wrong. So it didn't reach production. So I reverted it and now everything is fine.  
**Sean Winslow:** Awesome.  
**Aliaksandr Kryvanosau:** And currently I'm cleaning up the marketing uh ticket about teams to merge it into dev so it can be tested alongside with other compass tickets. And that's  
**Sean Winslow:** All right.  
   
 

### 00:03:39 {#00:03:39}

   
**Sean Winslow:** Thank Thank you,  
**Aliaksandr Kryvanosau:** it.  
**Sean Winslow:** Alex. And yeah, I'm pretty sure I saw you gave a thumbs up to the uh Serena design for the modal.  
**Aliaksandr Kryvanosau:** Yeah,  
**Sean Winslow:** Cool.  
**Aliaksandr Kryvanosau:** it look good.  
**Sean Winslow:** Sweet. Thank you, Anna.  
**Ana Benitez:** Um hello team. So I was testing stock and price pages yesterday. Today I'll continue with ETF pages migration and um also last night uh Ryan worked on fixing some of the bugs that were reported about the leaks on the top n bar and also for opening articles on a new tab. Uh so those tickets were uh are ready and I'll ask Ryan if we can deploy it as well today. And that's all for me.  
**Sean Winslow:** Okay, cool. Thank you, Anna. Is there anything that we can help you out with or they're You said the tickets already completed. You're all good on that front.  
**Ana Benitez:** Uh, yes. For the bucks.  
**Sean Winslow:** Okay.  
**Ana Benitez:** The bucks are Yeah.  
**Sean Winslow:** Okay. Cool.  
   
 

### 00:04:50 {#00:04:50}

   
**Sean Winslow:** Thank you, Anna. Well done.  
**Bohdan Panasenko:** Yes. So the ticket that I mentioned yesterday that um uh the same article displayed in latest crypto news is fixed. It's ready for testing. Uh I fixed uh similar ticket that u the last sponsor article does not contain the last like from the sp in the sponsor section the sponsored article. Actually the core of the issue I think was changed uh throughout the next migration because if before as it says in ticket it says like there is no sponsored article now actually we haven't brought that uh it is the same article it is shown but doesn't matter anyway it's fixed and I send it to review to Nicola  
**Sean Winslow:** Perfect. Okay, cool.  
**Bohdan Panasenko:** Yeah. Yeah.  
**Sean Winslow:** Yeah, thank you for checking that out.  
**Bohdan Panasenko:** So I I guess during  
**Sean Winslow:** This one you're talking about, right?  
**Bohdan Panasenko:** NX migration kind of it was the issue was changed but it still kind of exists.  
**Sean Winslow:** Okay.  
**Bohdan Panasenko:** But yeah, it's ready. So I  
   
 

### 00:06:03 {#00:06:03}

   
**Sean Winslow:** Ready. All right. Thank  
**Edvinas Rupkus:** for that uh 44 36 if if you can go back to Oakland.  
**Sean Winslow:** you.  
**Edvinas Rupkus:** Uh researchers are antsy about that feature. I I don't know if you're like obviously we have very important campus and other uh deliverables. So like that definitely don't need to intrude on that. But if we can pull this one in uh Anna like I don't know either this week or next week that'd be great.  
**Ana Benitez:** Yeah.  
**Edvinas Rupkus:** just one one specific one they've been asking about.  
**Ana Benitez:** Okay. Yes.  
**Edvinas Rupkus:** Thank you.  
**Sean Winslow:** Ed, is that what uh Adam brought up yesterday in Slack?  
**Edvinas Rupkus:** Um I I forget what he brought up but yeah it was it's about  
**Sean Winslow:** The  
**Edvinas Rupkus:** the ability to change the ability to add research reports and research articles to our researchers like author pages.  
**Sean Winslow:** Yeah, gotcha. Yep. Cool. Thank you. Banan Brian.  
**Ana Benitez:** I think B is not here,  
**Sean Winslow:** Yeah.  
**Ana Benitez:** but he he worked on a lot of tickets yesterday and  
   
 

### 00:07:18 {#00:07:18}

   
**Sean Winslow:** Yeah, I so cool.  
**Edvinas Rupkus:** Yeah, he shipped quite a few things aside, too.  
**Sean Winslow:** So, yeah. So, we'll give him a break. Welldeserved break. Next we'll go to  
**Cesar Paz:** Uh hi. Well, um I finished the task about the MVARS for the dead  
**Sean Winslow:** Caesar.  
**Cesar Paz:** box. Uh and in addition, I have to talk with Mike because I believe uh the second task for the dead boxes is done. Uh after doing my change during this uh during the last week, the last weeks. uh so I have to to talk with him because I believe that we are deploying uh a stack every time we deploy the box. Um so it should be done and in addition yesterday I finished uh one part in the uh okay we need to uh forward all invoices to freeblood.co code. Um, this is a problem because uh some of these services uh are managed only by nominal users. So I need to forward emails from these nominal users. I have to identify what are which are these nominal users by service.  
   
 

### 00:08:42 {#00:08:42}

   
**Cesar Paz:** So I I did I did exactly this yesterday. Uh I sent this information to Matt and Mike. So probably after uh their decision I have to keep working on this because this is not done yet and probably now I don't have uh urgent task finally. So uh my idea is to uh start new task uh to complete or to start my OKRs. uh for example I I would like to keep improving the cost uh in AWS or GCP or in other services and I would like to start to create some AI agents by using cloud. I'm not sure if it's possible to do this but I would like to start the creation of agents uh by using cloud. Uh so I'm going to start with this probably and that's all.  
**Sean Winslow:** Nice. Yeah, please keep me posted on that. I would love to talk to you. We could have a one-on-one or whoever wants to join because that is something that I'm very interested in as well. So, we can discuss. I've been doing research on that myself.  
   
 

### 00:09:55 {#00:09:55}

   
**Sean Winslow:** So, I can give you some tips and vice versa hopefully.  
**Cesar Paz:** Yeah. Okay, that's fine. Uh, I have to investigate first because I've never used cloud for creating a  
**Sean Winslow:** Sweet.  
**Cesar Paz:** agents. But yeah, of course, I'm going to talk with you.  
**Sean Winslow:** Yeah, they they have a a clawed agents SDK and it makes it fairly easy and everything kind of  
**Cesar Paz:** Okay.  
**Sean Winslow:** just like does all the work itself at this point. So yeah,  
**Cesar Paz:** Mhm.  
**Sean Winslow:** but yeah, we'll work something out.  
**Cesar Paz:** Okay.  
**Sean Winslow:** Cool.  
**Cesar Paz:** Good.  
**Sean Winslow:** Thank  
**Cesar Paz:** Thank you.  
**Sean Winslow:** you. Next, Corey.  
**Koray Baspinar:** Hello. Uh, today I mainly worked on multil- language investigation. Uh, I I I'm checking our competitors and also uh trying  
**Sean Winslow:** Cool,  
**Koray Baspinar:** to create some MVP for next week and also other than that I finished my presentation for today. Uh, that's all.  
**Sean Winslow:** man. Looking forward to it.  
**Koray Baspinar:** Thanks man.  
**Sean Winslow:** You're welcome, Kristoff.  
   
 

### 00:11:00 {#00:11:00}

   
**Sean Winslow:** Thank you,  
**Kryštof Oliva:** Hi guys. So today in the morning I had a call with Nicolola and he kind of introduced me to the repo and to the  
**Sean Winslow:** Corey.  
**Kryštof Oliva:** WordPress and he introduced me to the first task about removing the links. So I was working on that and I get the main feature done but yeah there's a lot of polishing a lot of other stuff to do about it as well. So I will work on it.  
**Sean Winslow:** Sweet. Thank you very much. How's uh how are the first few days going? Still doing the onboarding stuff,  
**Kryštof Oliva:** Um yeah, I guess the on boarding thing um is done now.  
**Sean Winslow:** right?  
**Kryštof Oliva:** So So yeah, I mean I I kind of tried it was all right.  
**Sean Winslow:** Getting your hands dirty  
**Kryštof Oliva:** It took a bit of time to kind of uh get some services and to get all access,  
**Sean Winslow:** now.  
**Kryštof Oliva:** but now I hopefully I have everything I need at least for now.  
**Sean Winslow:** Cool, man.  
   
 

### 00:11:52 {#00:11:52}

   
**Sean Winslow:** Thank you very much, Kristoff  
**Maryia Zhynko:** Today I did some uh minor fixes for stock and prices page uh UI  
**Sean Winslow:** Maria.  
**Maryia Zhynko:** issues and I'm starting uh with implementation of this elections LinkedIn page. I started with uh some basic markup and the hero component.  
**Sean Winslow:** Cool. Thank you, Marina. Uh Ed, I saw you were making some changes. Are they 100% complete? Meaning like that like do we have to keep on editing or for the  
**Edvinas Rupkus:** Uh it's just yeah yesterday I just like  
**Sean Winslow:** uh  
**Edvinas Rupkus:** basically edited the last few uh just minor things essentially and I and I just like did some formatting as well. Um yeah, not nothing nothing crazy changed.  
**Sean Winslow:** Okay.  
**Edvinas Rupkus:** Uh there's one thing like I mentioned before like the the main hero uh big the the big sort of hero component where it's the right now in the Figma it's the long form video like a podcast uh is reserved  
**Sean Winslow:** Yeah. Yeah.  
**Edvinas Rupkus:** for that.  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** I think that might change either to a short or or maybe even to a story but I don't think that's you know very major changes anyway.  
   
 

### 00:13:14 {#00:13:14}

   
**Edvinas Rupkus:** So like I I added that little call out in  
**Sean Winslow:** Cool. All right. Thank you, Maria. Marina.  
**Marina Lozuk:** Hello guys. Today I've been scrutinizing information about Google Analytics and how to track many tags for the same events. So uh and also I started creating new branches for the sticky banners and for that data dashboard as previous one were created bas based on dev but they need to be like replaced with the new ones based on main. So that's it.  
**Sean Winslow:** Cool. Thank you. Yeah. Have you been talking with Yurmeck to like has he been helping you out with the sticky footer  
**Marina Lozuk:** I believe that sticky footer is ready.  
**Sean Winslow:** stuff?  
**Marina Lozuk:** I just need to prepare a new uh a new branch for that and like to to to check it double check that everything works as expected.  
**Sean Winslow:** Okay.  
**Edvinas Rupkus:** Yeah, I think we we're going to wait for the rest of the migration to be finished, right?  
**Marina Lozuk:** Yeah,  
**Edvinas Rupkus:** For  
**Marina Lozuk:** but anyway this work must be done as we can't merge  
   
 

### 00:14:27 {#00:14:27}

   
**Edvinas Rupkus:** Okay.  
**Marina Lozuk:** it to dev and dev to main as there are some changes which should shouldn't be released. So I just need to rework what I've done a little  
**Edvinas Rupkus:** Yeah,  
**Marina Lozuk:** bit.  
**Sean Winslow:** Okay,  
**Edvinas Rupkus:** sounds  
**Sean Winslow:** cool. Thank you, Marina. Mike, what's up? What do you got? Just kidding. I said Nikita,  
**Edvinas Rupkus:** Okay.  
**Sean Winslow:** what do you got?  
**Edvinas Rupkus:** No, Mike's here, but we can't hear  
**Mikita Hulis:** Should we give it a  
**Sean Winslow:** Oh,  
**Edvinas Rupkus:** Mike.  
**Sean Winslow:** you  
**Edvinas Rupkus:** Yeah, he says it's speaking,  
**Mikita Hulis:** sec?  
**Edvinas Rupkus:** but his mic must be not connected on his end. Yeah, I see you, Mike. You're toggling on and off.  
**Sean Winslow:** All  
**Edvinas Rupkus:** We can come back to Mike.  
**Mikita Hulis:** Well,  
**Sean Winslow:** right.  
**Mikita Hulis:** uh I'm focused right now on supporting uh the QA process. aroma. He already got a few uh few adjustments for the for the multi-quest release as of this moment. Um all of them uh all the crucial ones at least are already applied and waiting to be deployed in a few and yeah awaiting the awaiting the new ones and also uh also done the one more review of the marketing marketing page from Alex uh because he he's adjusted it to the changes I requested yesterday.  
   
 

### 00:16:10 {#00:16:10}

   
**Mikita Hulis:** Uh, yep.  
**Mike Price:** Can y'all hear me?  
**Mikita Hulis:** Yep.  
**Edvinas Rupkus:** Yep.  
**Sean Winslow:** Yep.  
**Mike Price:** All right. Uh mainly iOS app updates. So, I was working on uh hooking up our our prices and switching from Coin Gecko's native. So, we're hooking we're displaying prices from our own API now. Um finishing up our notifications. Um just polishing it. We got a bunch of BQA Josh live BQA. So, merge that in. Getting it ready for internal testing. Um, I have a PR out for uh treasuries for updating uh treasury uh creating companies from the Slack uh hook web hooks that we created. So, we're going to merge that in in a bit. And then um I have a a new API to deploy which I'm going to try to get out today uh just for that's something that I've been working with Cam on and getting some actual users on it. Um, and then one more thing, uh, Simon AI, there was a, um, we have we have a standalone API for it that I'm currently testing.  
   
 

### 00:17:23

   
**Mike Price:** I want to get it out there probably the next day or so.  
**Edvinas Rupkus:** Mike, sorry. Excuse my ignorance. When you say we're going to use our own API to for prices, what do you actually  
**Mike Price:** So, Coin Gecko,  
**Edvinas Rupkus:** mean?  
**Mike Price:** we use Coin Gecko for our prices, but like we have a whole system that batches it and serves up the requests basically. Um, the initial app iteration was just using a standard API key, which would not suffice for actual deployment. So, we've t taken that, flipped it on its head, and now we're talking to our TV code API to grab all the prices for for just like you see on the price pages. We have that on the app. So,  
**Edvinas Rupkus:** Gotcha.  
**Mike Price:** I'm grabbing all the prices with via our own API. Um,  
**Edvinas Rupkus:** Gotcha. So, it's still gonna it's still going to originate from Coin Gecko,  
**Mike Price:** yeah.  
**Edvinas Rupkus:** but it's just going to be talking to prices instead of Coin Gecko directly.  
**Mike Price:** Yeah.  
   
 

### 00:18:18 {#00:18:18}

   
**Mike Price:** Yeah, exactly.  
**Edvinas Rupkus:** All right. All right. Cool.  
**Sean Winslow:** Cool. Thanks, Mike. And and Simon Simon AI, that's our own that's the block's own AI system,  
**Edvinas Rupkus:** Yeah, that's that that predates you,  
**Sean Winslow:** right?  
**Mike Price:** Yeah.  
**Edvinas Rupkus:** Sean.  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** It was I could I could tell you all about it on our 101\.  
**Mike Price:** Yeah.  
**Sean Winslow:** Okay. Yeah, please. Wait. Thanks,  
**Mike Price:** Yeah.  
**Sean Winslow:** Mike. Nikita. Oh.  
**Nikita Orobenko:** Um not too much updates on my ends. Uh currently uh spiraling in a silent panic mode uh because everything seems to be kind of fine but not no  
**Sean Winslow:** Oh,  
**Nikita Orobenko:** major things on Roma and uh right now it's mostly minor things.  
**Sean Winslow:** okay.  
**Nikita Orobenko:** So we're adjusting and fixing with Nick but uh the the the due date is coming uh for all of us. So uh the only question is like how is there any updates on the assets uh the subjects I didn't heard anything from David today  
   
 

### 00:19:27 {#00:19:27}

   
**Sean Winslow:** Yeah, same. Uh, so yeah,  
**Nikita Orobenko:** uh  
**Sean Winslow:** I haven't heard from like we were supposed to have an 8 am meeting and he didn't show up and then he gave me some updates via Slack a few minutes later saying that he was he was busy working on the modules and that he's going to send me the um the video assets today. So, I'm still waiting on them, but once he sends them to me, I'm going to knock them out and then I'll send them to you guys. And I'm working on the thumbnails now.  
**Nikita Orobenko:** Mhm. Okay.  
**Edvinas Rupkus:** And then I don't know if I don't know if the rest of the team caught that, but it's going to be February 17th, not 16th. So because of the holiday, so we'll get an extra. Yeah,  
**Nikita Orobenko:** You know how to bring the good news  
**Edvinas Rupkus:** that's  
**Mikita Hulis:** It's actually really great.  
**Nikita Orobenko:** ad  
**Edvinas Rupkus:** Yeah, sorry. Should have should have been a bigger, you know, suspense, but yeah. Anyway,  
   
 

### 00:20:25 {#00:20:25}

   
**Sean Winslow:** Oh.  
**Edvinas Rupkus:** President's Day coming in clutch.  
**Sean Winslow:** Yeah. Uh, also, Nikita,  
**Nikita Orobenko:** Okay.  
**Sean Winslow:** are there any other assets aside from the um intro videos and the thumbnails that you need?  
**Nikita Orobenko:** Uh I mean like not really. Uh the the the other major thing I'm waiting and the only David can help me with that. Uh but I suppose he will do it just right after he will finish adjusting uh the subjects uh content after the review he got. Uh I only need the exports of those uh four extra subjects and we need to he also need to set up the redirects uh after the subject end to our quizzes. So we will test out how the navigation will work in this case. So because right now we only can test only one  
**Sean Winslow:** Okay.  
**Nikita Orobenko:** subject.  
**Sean Winslow:** All right. Cool. Yeah. Let let me know if uh David reaches out to you. Uh I'll keep you posted if he gets back to me and hope hopefully I'll have the asset side done on my end by today.  
   
 

### 00:21:41 {#00:21:41}

   
**Sean Winslow:** But yeah,  
**Nikita Orobenko:** Okay.  
**Sean Winslow:** we got an extra day. Woo.  
**Nikita Orobenko:** That's perfect.  
**Mikita Hulis:** Before we move on,  
**Sean Winslow:** Yeah.  
**Mikita Hulis:** I actually forgot a one more portion of my update if you don't mind.  
**Sean Winslow:** Go for it.  
**Mikita Hulis:** Uh I found a linkage of styles today. There seems to be a new one from uh from Typical to Campus. Not to worry. It seems like I' I've found at least a band-aid to circumvent it from campus's site, but still it like it warrants to be investigated. I've notified Brian about it since it seems to stem from one of the later features on which he worked on. So he's already notified and uh it should be it should be handled. Uh should not hinder the release since the leakage from campus's  
**Sean Winslow:** Okay.  
**Mikita Hulis:** site looks to be easily avoidable. But I I I can't figure out the root cause though like why is it  
**Sean Winslow:** You you can or you can't. You said  
**Mikita Hulis:** cannot.  
   
 

### 00:22:42 {#00:22:42}

   
**Mikita Hulis:** No, I can't. I can't.  
**Sean Winslow:** Okay.  
**Mikita Hulis:** I found a band-aid, but like how it how it leaks, I I don't don't yet know.  
**Sean Winslow:** Okay.  
**Mikita Hulis:** And by the way,  
**Sean Winslow:** Gotcha.  
**Mikita Hulis:** huge thanks to Brian too for responding on such a short notice.  
**Sean Winslow:** Thank you, Brian. Yeah, Brian. I noticed you're on now, so we'll just pivot to you real quick.  
**Brian Mendoza:** Yeah, my bad for joining a bit late.  
**Sean Winslow:** Oh, good.  
**Brian Mendoza:** Cool. Um, I cranked out a bunch of stuff last night. Um, I'm going to try to deploy these two small fixes today. It's the open articles in new tab. And there's another one that isn't showing up on Jira,  
**Sean Winslow:** All  
**Brian Mendoza:** but it was um, another small one that was from Slack. I think it was the price URL thing. And then I got a bunch of things in QA and patched up for review access page and all that. And I'm going to look at Nikita's comment today because that's really scary because that leaked for no reason.  
   
 

### 00:23:34

   
**Brian Mendoza:** Not for no reason. Obviously, there's a reason, but it it like that feature came out like two months ago. So, it's like why is it randomly leaking now? So,  
**Sean Winslow:** right.  
**Brian Mendoza:** something to look at.  
**Mikita Hulis:** Yeah,  
**Sean Winslow:** Yeah.  
**Mikita Hulis:** it seems that Lish had started just about now because on dev on the box for Roma it is not visible as if it is not there like at all. Not that it is like taking no effect but that it's not there.  
**Brian Mendoza:** Strange.  
**Mikita Hulis:** Maybe some sort of like code separation during the build actually prevents it. It's uh I'm not quite  
**Brian Mendoza:** Sounds really fun.  
**Sean Winslow:** I appreciate it, Brian. Yeah. Uh, please keep us posted on that. I'm kind of curious as to if if you find the the the reason behind it, Nicola.  
**Nikola Pivčević:** Uh yeah, hello everyone. So uh today uh spend as Kristoff said uh some time with him uh to on board him and uh prepare him for his first task.  
   
 

### 00:24:38 {#00:24:38}

   
**Nikola Pivčević:** Uh other than that working on the video integration and um think I'm kind of uh have good progress on the WordPress part. I think it's like almost done. I'm working now on the front end part just to kind of um kind of prepare like a proof of concept component on the front end to verify that videos in fact work. And um yeah, I'm reusing like I found like um already built component for campus for videos. So I'm reusing that that component. Um didn't find any reason not to so far. Okay. And um other than that uh yeah I guess like we can now release  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** the white uh the white papers podcast now that u Alex finished. Yeah. Okay. Yeah. So we're going to focus on that after stand up.  
**Sean Winslow:** Perfect. And yeah. Uh do you do you want me to discuss anything about the tickets uh that I wrote any further with you or it's just okay?  
**Nikola Pivčević:** So, uh, I'm good so  
   
 

### 00:25:48 {#00:25:48}

   
**Sean Winslow:** Yeah,  
**Nikola Pivčević:** far.  
**Sean Winslow:** just keep me posted on that because like I said, I just kind of looked at the documentation. It was kind of going back and forth. So,  
**Nikola Pivčević:** Yeah. Oh,  
**Sean Winslow:** thank you Nicola  
**Nikola Pivčević:** thank you, sir.  
**Sean Winslow:** Romalt.  
**Ramuald Vishneuski:** uh health team. So I'm working on campus uh for now only some pretty minor um visual stuff for back end uh uh we discussed with Nikas how we will treat uh um credits. So we agree that we will assign uh two um additional cadets for all users for now because we just uh we're adding only one course for now and new users will get four credits but later we we should discuss um uh the whole concept of uh credit assigning. Uh so should we assign u like uh four credits and user can spend them for for one course or like uh two credits per course and what should we do when it access expires and so so on. So there are a lot of test cases we should discuss and uh decide something.  
   
 

### 00:27:12

   
**Ramuald Vishneuski:** Yeah but that's will be after this release. Um and yeah, just continue working on on campus. That's  
**Sean Winslow:** Okay,  
**Ramuald Vishneuski:** all.  
**Sean Winslow:** cool. Yeah. And um yeah, we'll figure that out because I I did notice that for the campus 101, you did have like this whole credit system. I guess it wasn't really discussed for 2011 that much as of yet.  
**Ramuald Vishneuski:** Uh, sorry. What you  
**Sean Winslow:** I you were talking about the the credit system that campus 101 has,  
**Ramuald Vishneuski:** mean?  
**Sean Winslow:** but it's not set up for 2011\. like there was no there was nothing in the requirements for 2011 when it came to the credit system.  
**Ramuald Vishneuski:** Uh, I don't remember that. I saw  
**Sean Winslow:** Okay. All right. Yes,  
**Ramuald Vishneuski:** that.  
**Sean Winslow:** it's not a big deal. We could discuss further after after the  
**Ramuald Vishneuski:** Okay.  
**Sean Winslow:** fact.  
**Ramuald Vishneuski:** Okay. And that's all from my set.  
**Sean Winslow:** Cool.  
**Ramuald Vishneuski:** Thank you.  
**Sean Winslow:** Thank you, Roma.  
   
 

### 00:28:13 {#00:28:13}

   
**Sean Winslow:** And thank you for keeping us updated.  
**Ramuald Vishneuski:** Of course.  
**Sean Winslow:** Is your mic here? All right, Ed. What you got going  
**Edvinas Rupkus:** Uh just one thing in regards to ratings.  
**Sean Winslow:** on?  
**Edvinas Rupkus:** It appears that there's there could be like an issue with the com with the recirculation component. Uh I'll send it who should I send it over to? Should I just put it in the engineering QA channel? It looks like the one of the images is like even though they are the same ratio, they don't appear as the same ratio, but might be just a small thing.  
**Mike Price:** Yeah, drop it in the QA channel.  
**Edvinas Rupkus:** Say it again,  
**Mike Price:** Yeah,  
**Edvinas Rupkus:** Mike.  
**Mike Price:** it's just drop in engineering QA channel from  
**Edvinas Rupkus:** All right, cool.  
**Mike Price:** there.  
**Edvinas Rupkus:** Uh, and then I have a small ticket that they that I will write for uh pro data awareness. So, basically for our data pages, we're going to have like a little message right above right next to the H1. And then on individual charts as well like sort of underneath the the chart where all the CTAs are uh to further surface the fact that we sell pro data like you know we have data API and all that stuff all the services uh is relatively straightforward nothing crazy there so is there anybody who has bandwidth for that or would like to grab  
**Mike Price:** Maybe Kristoff could take that off as well since he's kind of getting started relatively low lift.  
**Edvinas Rupkus:** Yeah, we can can definitely sign it to him. Awesome. That's it for me. If I have more stuff, I'll I'll ping you guys. But  
**Sean Winslow:** Cool. Yeah. And on my end, uh,  
**Edvinas Rupkus:** thanks  
**Sean Winslow:** just finishing up the campus stuff. I pretty much explained everything earlier. So, yeah, not not much to update as of now. So, hopefully I have some updates this afternoon. But, anybody else have anything that they want to discuss? All right.  
**Cesar Paz:** Thank  
   
 

### Transcription ended after 00:30:59

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*