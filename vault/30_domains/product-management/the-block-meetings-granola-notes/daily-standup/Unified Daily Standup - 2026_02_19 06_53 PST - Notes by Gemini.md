# 📝 Notes

Feb 19, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivčević](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Panasenko](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [Krystof Oliva](mailto:koliva@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMTlUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.rrx60kgzknn7) 

### Summary

**Technical Setup and Fixes**  
Multiple engineers reported completing various technical tasks, including fixing Campus LRS issues, working on metadata issues, and migrating color palettes on charts, with a notable shift to using Orbstack as a more reliable Docker alternative.

**Campus Release Timeline Clarification**  
The team discussed the timeline for the second major Campus release, which includes Stripe integration and profile management, agreeing to create a tracker sheet to provide specific dates for remaining tasks.

**Simon AI Demonstration and Future**  
The Simon AI chatbot, which uses RAG and a vector database of internal data, was demonstrated, leading to a discussion about its potential value in providing up-to-date news and exploring options like using open-source LLMs to reduce costs

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

## NEEDS FURTHER DISCUSSION

* **Orbstack Default Setup Recommendation** New onboarders should use Orbstack setup immediately. Orbstack performs better and provides more reliable operation than Docker Desktop for Mac OS users.

* **Campus Second Major Release Timeline** Timeline for Campus second major release needs establishment, covering Stripe integration and individual 201 access. Sean provides tracker sheet to Matt for specific date and deadline information.

## ALIGNED

* **Krystof Access 201 Course** Krystof takes time next week to complete 201 campus course. Ramuald provides guidance regarding block email login access.

* **Sean Matt Edvinas Groom Backlog** Sean, Matt, and Edvinas will schedule call to sift through backlog and groom old, irrelevant tickets. This process addresses growing ticket stack and ensures priority items visibility.

*More details:*

* **Initial Greetings and Office Location Discussion**: Sean Winslow thanked Aliaksandr Kryvanosau, and they briefly discussed Aliaksandr Kryvanosau being in an office to sign documents. Aliaksandr Kryvanosau clarified that they work through an outsourced company, and the office is that company's location ([00:00:00](#00:00:00)).

* **Branding and Update Priorities**: Nikola Pivčević noted that the Venshin cards had not been updated and still displayed cardart, which Mikita Hulis confirmed was technically correct since it is a subbranch of the company. Mikita Hulis requested to deliver their update first due to feeling unwell, a request that Sean Winslow granted ([00:01:09](#00:01:09)).

* **Mikita Hulis's Technical Recovery and Task Update**: Mikita Hulis reported spending the majority of their day recovering their setup after Docker Desktop malfunctioned, leading them to switch to Orbstack ([00:01:09](#00:01:09)). They are now part of the "happy family of Orbstack users" and continuing to apply fixes related to various campus redirects discussed with Claudine and Roma. Mikita Hulis plans to deploy those fixes tomorrow and indicated their overall impact for the rest of the day would be minimal due to feeling unwell, but they would remain in touch due to the fresh release ([00:02:20](#00:02:20)).

* **Discussion and Endorsement of Orbstack**: Sean Winslow inquired if Orbstack was a replacement for Docker, to which Mikita Hulis explained it is a faster and more reliable wrapper around the core Docker engine, especially for Mac OS ([00:03:30](#00:03:30)). Krystof Oliva and Mike Price also endorsed Orbstack, with Krystof Oliva suggesting that it should be the default for onboarding due to the stability issues they experienced with Docker ([00:04:37](#00:04:37)). Mikita Hulis then logged off to rest ([00:05:26](#00:05:26)).

* **Aliaksandr Kryvanosau's Task Update**: Aliaksandr Kryvanosau reported completing a new ticket from Ed regarding changing the successful message on the advertise form, which is now in code review. They also implemented the reach-out model for jobs, including the disclaimer, and are currently working on a metadata issue, while noting they had to revert some local setup changes on the monorepository to get it working correctly ([00:05:26](#00:05:26)).

* **Ana Benitez's Migration and Testing Updates**: Ana Benitez shared that only one fix remains for the color palettes on the charts regarding the attachment migration, which they discussed with Marina, moving the ticket back into progress. They finished testing fixes from Bam and the press release eyebrow feature, which are ready for deployment, and they will now focus on the migration tickets related to notifications that Ryan worked on ([00:05:26](#00:05:26)).

* **Cesar Paz's Collaboration and New Task**: Cesar Paz mentioned assisting Mikita Hulis in the morning with a bug fix in the deployment release of campus LRS. They are also starting a low-priority task of checking through old pull requests in mono from approximately six months ago, specifically related to job redirects ([00:06:36](#00:06:36)).

* **Krystof Oliva's Thesis Defense and Development Tasks**: Krystof Oliva was off the previous day to test their thesis with the doctors and today finished the link removal task, which is now ready for testing after the final review from Nicola. They started working on an image refactoring task to remove large images from the codebase and plan to finish the banner task, which is currently on hold, by Tuesday. Krystof Oliva also inquired about taking the 201 course for Upscale LMS after the campus release ([00:07:46](#00:07:46)).

* **Course Access and Bug Reporting for Krystof Oliva**: Mike Price confirmed that the campus 201 course is available for Krystof Oliva to proceed with. After Krystof Oliva confirmed passing the 101 course, Ramuald Vishneuski clarified that their existing Upscale LMS account may not work, but they can log in using their block email to be added automatically for access ([00:10:36](#00:10:36)). Edvinas Rupkus requested that Krystof Oliva report any bugs they find while taking the course, as it is still being tested ([00:11:33](#00:11:33)).

* **Maryia Zhynko's Elections Hub Progress**: Maryia Zhynko provided a brief update, noting that the money tracker section of the elections hub landing page is complete, and they are now starting work on the report cards section ([00:11:33](#00:11:33)).

* **Marina Lozuk's Data Dashboard and API Status**: Marina Lozuk reported being almost done with supporting different themes for the data dashboard iframes and is preparing to move the task to testing. They will then pick up the issue that Ana Benitez reported yesterday ([00:12:38](#00:12:38)).

* **Mike Price's API and Infrastructure Updates**: Mike Price reported that the Simon AI API is mostly done, and the Pro API is nearly complete, with a few remaining tasks. They performed a substantial refactor on the iOS app to prepare it for release and integrated Depot.dev into the build system, resulting in faster builds, including for the Canvas LMS ([00:12:38](#00:12:38)). Mike Price also confirmed they have an open pull request for treasuries ([00:14:06](#00:14:06)).

* **Simon AI API Development and Access Discussion**: Mike Price explained that the standalone Simon AI API was built to leverage the technology for Jordan Leech's automations, which took about a week to develop ([00:14:06](#00:14:06)). Sean Winslow was curious about Simon AI and Nikola Pivčević offered to stay after the meeting to show them how to access it through the block pro account ([00:15:12](#00:15:12)).

* **Nikita Orobenko's Campus LRS Fixes and Credit Migration**: Nikita Orobenko reported working on fixing an issue where data was not stored in the product instance of the campus LRS, but confirmed that progress saving was unaffected, and thanked Cesar Paz for help resolving the main problem. They are also preparing a migration to normalize the amount of assigned credits, which were slightly over-assigned during deployments ([00:15:58](#00:15:58)).

* **Timeline Discussion for Campus Second Major Release**: Nikita Orobenko requested clarification on the expected timeline for the second major part of the campus release, specifically regarding the Stripe integration, profile management, and access to 201 for individuals, seeking to align expectations and avoid issues ([00:15:58](#00:15:58)). Sean Winslow committed to finishing and sharing a campus tracker sheet with Matt today to discuss specifics, noting there are no known financial constraints after the enterprise release ([00:18:02](#00:18:02)).

* **Next Steps for Campus Timeline and Priorities**: Edvinas Rupkus agreed with the plan to create a sheet of remaining tasks for Matt to provide specific dates, noting that the individual release priority follows the enterprise version and should look professional ([00:19:13](#00:19:13)). Nikita Orobenko agreed to sync on the engineering side with Roma to estimate the time required for the Stripe integration and other fixes. Sean Winslow confirmed they will share the finished tracker sheet with the group after Matt's review ([00:20:23](#00:20:23)).

* **Nikola Pivčević's Video Component and Backlog Grooming**: Nikola Pivčević is primarily focused on wrapping up the videos component on the front end and has been involved in ticket grooming ([00:20:23](#00:20:23)). They noted the extensive backlog, with over 500 tickets, much of which is old, and Edvinas Rupkus acknowledged this is a task for themself and Matt to address ([00:21:39](#00:21:39)). Nikola Pivčević added that they initiated the grooming process to ensure Krystof Oliva and Bogdan had sufficient work ([00:23:24](#00:23:24)).

* **Discussion on Ticket Backlog History**: Edvinas Rupkus noted the backlog contains old tickets, many of which are no longer relevant due to changing requirements, and that they will set up a call with Sean Winslow and Matt to sift through them ([00:21:39](#00:21:39)). Sean Winslow and Nikola Pivčević mused over the history within the old tickets, mentioning former team members and the early days of the company ([00:23:24](#00:23:24)).

* **Ramuald Vishneuski's Testing and Bug Fixes**: Ramuald Vishneuski continues to test campus, noting a fixed post-release issue where some users lacked access to the old course because it was not assigned to the upskill LMS organization. They are continuing to work on items related to credits and outstanding bugs ([00:25:54](#00:25:54)).

* **Post-Campus Priority Setting**: Edvinas Rupkus reiterated that after campus testing is complete, the next priority is ensuring migration tickets are finished, followed by the poly market widgets that Marina Lozuk is developing ([00:25:54](#00:25:54)). Sean Winslow confirmed the bug tracker sheet will be completed within the hour and that they will follow up with Matt regarding the timeline ([00:27:44](#00:27:44)).

* **Demonstration and Discussion of Simon AI**: Nikola Pivčević confirmed they had the authority to restore Sean Winslow's Pro access if needed, but upon checking, confirmed Sean Winslow had access to all products ([00:27:44](#00:27:44)). Nikola Pivčević proceeded to demonstrate Simon AI, explaining it as a chatbot trained on the block's data, which uses a Retrieval-Augmented Generation (RAG) implementation by storing content in a vector database ([00:30:34](#00:30:34)). When a question is asked, Simon AI retrieves relevant articles from the vector database and feeds that context into a large language model (LLM) to generate an answer based on the provided content, along with linked sources ([00:33:12](#00:33:12)).

* **Simon AI Maintenance and Future Considerations**: Nikola Pivčević confirmed that a pipeline is in place to update the vector database whenever an article is published or updated ([00:37:20](#00:37:20)). They noted that people were initially excited about the product, but its usage was limited because it was not exposed to a wider audience due to the cost and potential abuse of running LLM queries ([00:39:31](#00:39:31)). Sean Winslow suggested considering an open-source LLM trained on the block's data to make the service more accessible and affordable. Nikola Pivčević noted a drawback is that up-to-date information is critical in the news business, and pre-trained LLMs would lack the latest data; furthermore, modern LLMs can search the internet, leading to mixed results when compared with Simon AI's performance ([00:40:23](#00:40:23)).

* **Simon AI Evaluation and Potential Improvements**: Nikola Pivčević confirmed that an internal evaluation showed Simon AI provided the same or better results than ChatGPT in 70% of cases upon its release. Sean Winslow expressed interest in diving deeper into this area, mentioning tools like Google Labs for side-by-side evaluation ([00:42:50](#00:42:50)). They discussed leveraging current approaches, such as LLM "skills" to improve efficiency and reduce token waste, concluding that Simon AI's biggest value is its ability to search for recent news ([00:38:34](#00:38:34)) ([00:44:01](#00:44:01)).

### Suggested next steps

- [ ] Mikita Hulis will deploy the fixes discussed with Claudine and Roma regarding various redirects in campus tomorrow morning.

- [ ] Krystof Oliva will wrap up the link removal task in a meeting tomorrow and aim to finish the image re task and the banner task by Tuesday.

- [ ] Sean Winslow will create and finish the campus tracker sheet today detailing what is left for the campus project, send it to Matt for review, and then share it in the group chat.

- [ ] Edvinas Rupkus will reply to emails and comments on all Figmas and tickets later today.

- [ ] Krystof Oliva will log in to the upscale LMS using the company email to access the course and report any bugs found while testing.

- [ ] Sean Winslow will talk to Matt to get an update on the timeline for the second major part release of the campus.

- [ ] Nikita Orobenko will coordinate on the engineering side regarding the remaining work for the Stripe integration to provide an estimate.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=9s4s5bjREzroLt-p4n6FDxIWOAIIigIgABgBCA&detailid=standard)*

# 📖 Transcript

Feb 19, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Mike Price:** All right.  
**Sean Winslow:** Thank you. Something new every morning. Thank you, Alex. You got me my back every single time.  
**Aliaksandr Kryvanosau:** Yeah, because I'm the first one to talk.  
**Sean Winslow:** Were you Are you in an office right  
**Aliaksandr Kryvanosau:** Yep.  
**Sean Winslow:** now?  
**Aliaksandr Kryvanosau:** I needed to sign some dogs, so I decided to stay here and work here as well.  
**Sean Winslow:** Nice. Keeping it official.  
**Aliaksandr Kryvanosau:** Yep. I even have my bench to open doors.  
**Sean Winslow:** Oh my god.  
**Krystof Oliva:** Wait,  
**Sean Winslow:** Kristoff,  
**Krystof Oliva:** there are office.  
**Sean Winslow:** how you doing?  
**Krystof Oliva:** Yeah. Hi, there are offices. I thought it's only  
**Aliaksandr Kryvanosau:** Well, I'm not working directly to block.  
**Krystof Oliva:** remote.  
**Aliaksandr Kryvanosau:** I'm working through another um outsource company. So, this is the outsource company's  
**Krystof Oliva:** Okay,  
**Aliaksandr Kryvanosau:** office.  
**Krystof Oliva:** now it makes sense because like I was thinking they have the minus two hours compared to me, but it should be Yeah, whatever.  
**Nikola Pivčević:** Also, I noticed that they didn't update the cards to Venshin.  
   
 

### 00:01:09 {#00:01:09}

   
**Nikola Pivčević:** Instead, it's still cardart.  
**Mikita Hulis:** Well, strictly speaking, it still is.  
**Sean Winslow:** Hey.  
**Nikola Pivčević:** Is it? Oh, like the companies still didn't the  
**Mikita Hulis:** It's a it's it's it's a subbranch of the company of which we are a part of. So both are true.  
**Nikola Pivčević:** Okay. Okay.  
**Mikita Hulis:** which is by the way uh Sean if you don't mind when we switch to updates could I give  
**Sean Winslow:** That's  
**Mikita Hulis:** mine first because I do feel quite unwell  
**Sean Winslow:** okay. Yeah, you got it. Yeah. So, we'll get started. Uh, yeah. That's Nikita.  
**Mikita Hulis:** What a surprise. Yeah. So, my update will be sweet and short. Uh spent majority of my day recovering my setup because uh Docker desk Docker Desktop wonderfully went haywire on me today, which uh yeah, got me mad. I've tried to reset the whole thing a few times and applied various fixes. It did not fix the issue. So, uh, Brian and Nicole can welcome me and Mike can welcome me into a happy family of Forbac users.  
   
 

### 00:02:20 {#00:02:20}

   
**Mikita Hulis:** Yeah, you're right.  
**Aliaksandr Kryvanosau:** Welcome to the club.  
**Mikita Hulis:** You got it. Yes, I switched to Orbstack, recovered recovered the recovered the stack and uh with that in place, I'm continuing to apply those fixes discussed yesterday with Claudine and Roma regarding various redirects in campus would have been deployed today, but with the with the dockers thingy uh could not uh make it in time. So, I'll uh likely deploy those uh tomorrow, probably first thing. And yeah, that's uh that's about it. Yeah. And uh this sort of got me derailed. Uh so I feel quite s\*\*\* to be honest, but hopefully nothing major. Hopefully I'll be back I'll be back in full force tomorrow.  
**Sean Winslow:** Yeah.  
**Mikita Hulis:** And yeah,  
**Sean Winslow:** And all right,  
**Mikita Hulis:** that's about  
**Sean Winslow:** man. Yeah. Sorry to hear that you're not feeling well, but yeah, if if you want, feel free to log off, get some rest, and then yeah, we could focus on the other stuff tomorrow.  
**Mikita Hulis:** I'll be at least in touch especially since the release is so fresh.  
   
 

### 00:03:30 {#00:03:30}

   
**Sean Winslow:** Gotcha.  
**Mikita Hulis:** So do not feel like completely logging off but yeah the impact for the  
**Sean Winslow:** Okay.  
**Mikita Hulis:** rest of the day would probably be minimal.  
**Sean Winslow:** Got All right. Yeah. take take care of yourself because that's your health is more important at this point. So also quick question uh is Orbstack is that a replacement for Docker or is that a completely different  
**Mikita Hulis:** It's it's another wrapper around Docker basically.  
**Mike Price:** truck and replacing  
**Sean Winslow:** thing?  
**Krystof Oliva:** Yeah.  
**Mikita Hulis:** So you have your core Docker engine which does what Docker does, meaning containerizing stuff, but to launch it on anything other than Linux, you need some sort of wrapper, basically a container around Docker with its containers. And the two major uh uh solutions for that are either Docker Desktop for both like Windows and uh Mac OS as well as Orbstack which it seems like should be a default now. Yeah, I've been using it for a few hours now and yeah, it's so much f\*\*\*\*\*\* better.  
**Krystof Oliva:** Yeah, it's it's like faster and more reliable.  
   
 

### 00:04:37 {#00:04:37}

   
**Mike Price:** Test it.  
**Krystof Oliva:** Like I also switched since I joined like I use Docker before and it's like for Mac it just works better. I don't know. I mean it it like just runs the containers in the same but I feel like it's it it's better like I also had some problems with Docker when I joined and this solved it just like switching to her stick. So maybe if like someone is on boarding they should use or stack right away because I couldn't run it on Docker for some reason and it worked in the previous company like I used to work with Docker.  
**Mikita Hulis:** Yeah, I sort of feel bad about like trying to recover my setup in Docker Desktop before and I was I gave up and I should have g I should have given up much much earlier. It feels  
**Sean Winslow:** You were trying to hold on to what you already knew. I get  
**Mikita Hulis:** Well, it's it's sort of plug and play like there is nothing it's not like there's  
**Sean Winslow:** that.  
**Mikita Hulis:** anything new to learn.  
   
 

### 00:05:26 {#00:05:26}

   
**Mikita Hulis:** It's there is still like Docker is the underlying thing. There's not much to learn.  
**Sean Winslow:** Yeah. All right. Well, yeah, I'm definitely going to look into that because I've I've explored Docker as well and I've had my issues so I just kind of dealt with them. So, yeah. Thank you. Feel better, Alex.  
**Aliaksandr Kryvanosau:** Hello again. Okay. So for me,  
**Sean Winslow:** Hey.  
**Aliaksandr Kryvanosau:** I got a new ticket from ad about changing successful message on the advertise form. Uh change it and now it's in code review. Then I implemented the um reach out model for jobs at the disclaimer and I'm working on the metadata issue and also I had some issues with the local setup as well on the mon repository but uh I wasn't able to resolve them. So, I had to just u uh uh what the word for this? Get some old changes back. And now it's working correctly without latest changes. So it's fine.  
**Sean Winslow:** All right, cool.  
   
 

### 00:06:36 {#00:06:36}

   
**Sean Winslow:** Yeah. Uh, keep us updated. I know Ed uh Ed said he has a doctor's appointment. I don't know if he's in. So, yeah, he's going to be out for this standup. So, if anybody has anything they want me to pass over to him, just let me know.  
**Edvinas Rupkus:** I'm here. I'm just I'm in the car.  
**Aliaksandr Kryvanosau:** Okay.  
**Edvinas Rupkus:** I'm I'm here.  
**Sean Winslow:** No.  
**Edvinas Rupkus:** I just I'm driving.  
**Sean Winslow:** Okay, cool. All right. Thank you, Alex.  
**Ana Benitez:** Um hello. Well, regarding that attachment migration, uh there is one fix left for the color palettes on the charts and I already discussed that with Marina. So, uh that ticket is back in progress for one comment. And I also finished testing some of Bam pixes and the press release eyebrow he worked on. These tickets are looking good. So they're in a wedding deployed and for now I will continue with um tickets for migration that Ryan work on regarding the notifications. And that's all from my side.  
   
 

### 00:07:46 {#00:07:46}

   
**Sean Winslow:** Perfect. Thank you, Anna.  
**Ana Benitez:** Thank you.  
**Sean Winslow:** Is Bodon in today? No,  
**Ana Benitez:** I think he's out.  
**Krystof Oliva:** He has the exit in today,  
**Sean Winslow:** he's out.  
**Krystof Oliva:** I think.  
**Sean Winslow:** Gotcha. I thought he had the exam yesterday. Well, probably recovering from the exam and partying right after. So, we'll skip Bodon. I didn't get any updates, but yeah, it sounds like everything is up to speed. Uh Brian Caesar,  
**Cesar Paz:** Hi. Well, uh today in the morning I was helping to Nikita to  
**Sean Winslow:** wait.  
**Cesar Paz:** um fix a book uh we had in the dep in the release of campus ls. Uh and in addition I'm starting a new task uh a low priority task probably um I'm checking some pull requests from since 6 months ago more or less in mono. Uh so yeah I'm working on this right now in the jaw redirect. It's below because I don't see. Yeah,  
**Sean Winslow:** Okay,  
**Cesar Paz:** it's there exactly.  
   
 

### 00:09:12

   
**Cesar Paz:** And that's all.  
**Sean Winslow:** cool. Thank you, Caesar.  
**Cesar Paz:** Thank you.  
**Sean Winslow:** All right, we'll go with Corey. Just kidding. Go with  
**Krystof Oliva:** Okay. Hello guys. So yesterday I was off.  
**Sean Winslow:** Kristoff.  
**Krystof Oliva:** I had uh test my thesis with the doctors. But today I finished the link removal task like I got the last review from Nicola and we decided that tomorrow we'll kind of wrap it up in a meeting and yeah but it should be done now ready for testing and then I started working on the image re task. There are some images quite large which are in the codebase and we have to get rid of them. Um, and also I have um I'm in the middle of doing the banner task, but I kind of uh put it on hold for a while because I I I started working on the image thing. But yeah, these two I will kind of finish uh I hopefully until Tuesday. Uh so yeah, I think that's it for me and also I want to ask uh so when the campus one is out, can I like take some time next week and do the course like to get my knowledge?  
   
 

### 00:10:36 {#00:10:36}

   
**Mike Price:** It's out. Go ahead.  
**Sean Winslow:** Did Did you take uh 101 yet?  
**Krystof Oliva:** Yeah. Yeah. I I passed the 101 and I want to do the  
**Sean Winslow:** Yeah,  
**Krystof Oliva:** 2011\.  
**Sean Winslow:** I mean you should you should be able to uh if you if you log into your into my campus, it should pop up right  
**Krystof Oliva:** Okay,  
**Sean Winslow:** below.  
**Ramuald Vishneuski:** No, I saw that you have account in individual or so.  
**Krystof Oliva:** perfect.  
**Ramuald Vishneuski:** So you bought access to upscale LMS uh half year ago, right?  
**Krystof Oliva:** Yeah. Yeah.  
**Ramuald Vishneuski:** uh and from uh that account you can't uh do that but we can  
**Sean Winslow:** Cool,  
**Ramuald Vishneuski:** um create a new one for you inside the block or and you will be able to do  
**Mike Price:** I say,  
**Ramuald Vishneuski:** that.  
**Mike Price:** can he just log in with his block email?  
**Krystof Oliva:** Okay,  
**Ramuald Vishneuski:** Uh yeah you you can just log in in uh uh using your uh uh the blog uh email.  
**Krystof Oliva:** company address.  
**Ramuald Vishneuski:** Yeah. And you will be added automatically there.  
   
 

### 00:11:33 {#00:11:33}

   
**Krystof Oliva:** Okay, perfect. Yes,  
**Ramuald Vishneuski:** So yeah.  
**Krystof Oliva:** I'll do that probably next week. And yeah, I think I think that's it for me.  
**Sean Winslow:** man. Thank you. Yeah. Let us know what you think.  
**Edvinas Rupkus:** report also report any bugs if there are if you find any first off because we're still you know obviously like testing it and making sure that it's all working correctly.  
**Sean Winslow:** Did  
**Edvinas Rupkus:** So like keep us keep us in the loop if there's anything that doesn't seem  
**Sean Winslow:** you get that, Kristoff?  
**Krystof Oliva:** No, I didn't catch it at all. Sorry.  
**Sean Winslow:** He he said if you uh if you see any bugs or or anything like  
**Krystof Oliva:** Yeah, of course.  
**Sean Winslow:** that,  
**Krystof Oliva:** Yeah,  
**Sean Winslow:** just let us know.  
**Krystof Oliva:** I did the same in the in the block app and I sent it to the same Right.  
**Sean Winslow:** Perfect. Thank you, Maria.  
**Maryia Zhynko:** Yep. Today I continued working on uh elections uh hop landing page. The money tracker section is done starting with uh report cards section.  
   
 

### 00:12:38 {#00:12:38}

   
**Sean Winslow:** Cool. Perfect. Thank you, Marina.  
**Marina Lozuk:** Hello. As for me, I'm almost done with the task of supporting different themes for the iframes for the data dashboard. I'm about to move it to testing and pick up the issue which Anna reported me yesterday. That's  
**Sean Winslow:** Cool. Thank you.  
**Marina Lozuk:** it.  
**Sean Winslow:** Yeah, there there have no there haven't been any other API questions with the poly market stuff. You've been good with  
**Marina Lozuk:** Yeah, I think so.  
**Sean Winslow:** that.  
**Marina Lozuk:** Just need to test it and maybe someone will find something.  
**Sean Winslow:** Thank you, Marina. Mike.  
**Mike Price:** Um, Simon AI API is mostly done. Pro API is almost done. Uh, just a few things in the works. Um, I've been working on iOS app. Um, did a pretty large refactor just getting it in shape ready for the  
**Sean Winslow:** Awesome.  
**Mike Price:** release, notifications, such. Um also did some work finally integrated with depot.dev for our build system. So have faster builds now like five minute the block pro builds and so on.  
   
 

### 00:14:06 {#00:14:06}

   
**Mike Price:** I'm doing canvas LMS as well. So it should have better faster builds caching so forth. So here and there doesn't support. Also, I have a PR for treasuries uh that needs to go out soon.  
**Sean Winslow:** Thank  
**Mike Price:** So, I have a PR up for that.  
**Sean Winslow:** Is is Simon AI supposed to go into the app?  
**Mike Price:** Um no, um Jordan Leech was doing some automations um and he reached out and wanted to leverage Simon AI for it. So, I built a quick standalone API for it. We were talking about doing that anyway, so I just took it on real quick.  
**Sean Winslow:** Oh,  
**Mike Price:** Real quick, me.  
**Sean Winslow:** nice.  
**Mike Price:** It took me a week to build it out, but yeah, it's mostly  
**Sean Winslow:** Cool,  
**Mike Price:** done.  
**Sean Winslow:** man. Thank you. Yeah, I'd be curious. I'd like to learn more about Simon AI when everyone has time.  
**Mike Price:** But if you tinker around with stuff, you can take a look at the API once I get it out.  
   
 

### 00:15:12 {#00:15:12}

   
**Sean Winslow:** Sweet.  
**Mike Price:** It's uh mess around with it streaming everything.  
**Sean Winslow:** Oh, yeah. Awesome. Thank you,  
**Nikola Pivčević:** Do you have access to Simon like through through the block that  
**Mike Price:** Yeah,  
**Nikola Pivčević:** pro?  
**Mike Price:** you can access it now if you have access to the black  
**Sean Winslow:** Oh, all right. I  
**Mike Price:** pro.  
**Sean Winslow:** should  
**Nikola Pivčević:** We can stay after the meeting if you want like Yeah. Just to see like do you have a pro account? Did you ever log in into the blog that  
**Sean Winslow:** I did I remember I did when I first started working here, but then it said it was um like after the new year it it like I didn't have it anymore, but I think it got renewed. So, I think it got renewed automatically. So, I just had to double  
**Nikola Pivčević:** Yeah, like yeah,  
**Sean Winslow:** check.  
**Nikola Pivčević:** we can maybe stay like after after the meeting if you don't have anything. We can see like have  
**Sean Winslow:** Cool. Yeah, I would love that.  
   
 

### 00:15:58 {#00:15:58}

   
**Sean Winslow:** Thank you, Nikita. O.  
**Nikita Orobenko:** Yep.  
**Sean Winslow:** Yes.  
**Nikita Orobenko:** Um we were working on um fixing a little the product instance of the campus LRS. Uh I mean the only thing we did lost is just the data was not stored in it but uh it was it did it should not affected the progress saving because the progress saving is happening before the statements will be sent out to the LRS because they are being proxited through the campus instance. Uh but yeah, thanks to the Caesar, we figure out uh what was the main problem there. Uh also was working on preparing the migration for um aligning uh the credits because during the deployments uh we're a bit assigned we assigned a bit more than we needed. Uh so now we should just normalize uh the amount of credits. Um and that's it so far. Uh the major question I do have on the plate uh what what are our expectations regarding the second major part release of the campus uh in terms of the timeline uh regarding the stripe integration because as we talked with Roma we suppose that there will be intermediate releases with some bug fixes and the stuff we will find not regarding uh the stripe thing and then there will be a separate major release with the stripe integration with the access to 2011 for the individuals clients uh the new uh profile management things and so on and so on in terms of the things that we planned.  
   
 

### 00:18:02 {#00:18:02}

   
**Nikita Orobenko:** So is there any specific time constraints that we should be aware about? Uh are they tied to some consequences in the financial uh financial area like the last one we had? Uh or it don't. uh so just want to make sure that everyone will be aligned with the expectations with the timelines beforehands so we won't repeat the same thing uh again and we will broke the sanssara uh circle Oh.  
**Sean Winslow:** So yeah, so I'm putting together a campus tracker after the 2011 release and it should be done. It'll be done today. So I'm gonna I'm going to bring that to Matt and then we'll discuss unless Ed did he because I don't  
**Nikita Orobenko:** Mhm.  
**Sean Winslow:** think there's anything financial a after this fact after the enterprise uh release. So I think we're good on that front, but I I haven't received any sort of timeline just yet. So, I could talk to Matt and see what the deal is, but Ed, did he mention anything about a timeline to you?  
**Edvinas Rupkus:** No, I don't have a specific date.  
   
 

### 00:19:13 {#00:19:13}

   
**Edvinas Rupkus:** The year plan sounds okay uh with you know create a sheet and then go into him for specifics but obviously like our marketing pages are very different right now for individuals and marketing and the enterprise version. So we have to try and uh obviously like do it his answer will be ASAP.  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** Uh obviously we don't want to we don't want to create any critical bugs or anything like that. So, uh, yeah, I think, uh, Sean, you please do the the sheet of of like what's left over and what sort of stage we're in with each of those specific details and then Matt can provide you like if there's a specific uh date or deadline, but I mean there's no there's no like client that's waiting for individual release, you know, it's it's all enterprise. That's that's very important. Uh so but but again we want our product to look you know and feel professional uh and polish. So, I hope that provides a little bit more  
**Sean Winslow:** Did you get that,  
**Nikita Orobenko:** Yeah.  
**Sean Winslow:** Nikita?  
   
 

### 00:20:23 {#00:20:23}

   
**Nikita Orobenko:** Um I think we'll need to sink on the engineering side of that questions regarding what's we have left specifically for the stripe integration. Let the Roma have the proper time for testing. Uh we obviously didn't have before the 2011 release. Uh so we will figure out what what else we need to fix. and how much time that will take. So combine them all together and then I I suppose we will have kind of a proper uh estimate or at least from the engineering perspective.  
**Sean Winslow:** Cool. Yeah, once once I finish the tracker sheet, uh I'll send it to Matt just to review and then I'll put it in uh that group chat that we've been using just so you guys can have something to to visualize the updates.  
**Nikita Orobenko:** Okay. Yeah, that will be perfect.  
**Sean Winslow:** Cool. Thank you, Nicola.  
**Nikola Pivčević:** Uh yeah hello everyone. So uh mostly um wrapping up the videos uh so the videos component on the front end and yeah did uh some more ticket grooming.  
   
 

### 00:21:39 {#00:21:39}

   
**Nikola Pivčević:** Uh there is a lot of stuff in the backlog but like yeah I I guess like I'll stop here and like yeah we'll we'll we'll groom as needed. Right. There's like I guess like more than 500 tickets in the backlog. Yeah. Okay.  
**Sean Winslow:** That's a lot of  
**Edvinas Rupkus:** Yeah,  
**Nikola Pivčević:** It's  
**Edvinas Rupkus:** it's honestly it's Yeah,  
**Mike Price:** do the Jason  
**Edvinas Rupkus:** it's honestly Matt and my Yeah,  
**Sean Winslow:** grooming.  
**Edvinas Rupkus:** it's it's a lot of old stuff and it's honestly on Matt and my plate to go through  
**Mike Price:** stuff.  
**Edvinas Rupkus:** them. We should probably set up a call Sean Matt and I and like just run through them cuz uh back in the day that's what we used to do on Malcolm and I. We would spend like hours sifting through those tickets that are that are old. They're no longer relevant. But uh thank you Nicola for for looking through a few of them or not a few of them a lot of them and providing some color and closing a few of them.  
   
 

### 00:22:34

   
**Edvinas Rupkus:** But yeah, we we we'll have to like just make sure to stay on top of it because the  
**Nikola Pivčević:** Yeah, let me know. Yeah,  
**Edvinas Rupkus:** the stack continues to grow.  
**Nikola Pivčević:** like every every every ticket has its own story, right? Like uh it's and it's not easy like kind of to decide at at the moment like oh what to do with this  
**Sean Winslow:** Mhm.  
**Nikola Pivčević:** one, right? Like we first need to see like oh is it implemented? Is it fixed? Like bring like you know so it's not like yeah it's it takes time. It takes like, oh, we need to ask other people. And then like, yeah, it's kind of an ongoing process, right?  
**Edvinas Rupkus:** Yeah,  
**Nikola Pivčević:** It's  
**Edvinas Rupkus:** requirements also change like midway through integrations and those features are no longer needed and those tickets just get left behind. So yeah, we'll we'll get it sorted.  
**Nikola Pivčević:** Yeah. But I think like kind of the the the reason why I started doing this is like now fix like both Kristoff and Bogdan have enough work now.  
   
 

### 00:23:24 {#00:23:24}

   
**Nikola Pivčević:** So I think like yeah it's no longer like uh such an important uh uh it's not like burning thing to do and yeah like uh I'm still waiting for for a few replies on some tickets and I added a few uh comments on the Figma file for the elections hub. So when you have like a moment like yeah just uh if you can take a look at it.  
**Edvinas Rupkus:** Yeah, I'll check it out today.  
**Nikola Pivčević:** Yeah. Thank Thanks.  
**Sean Winslow:** Awesome. Thank you. Yeah, I'm I'm excited to dig through. I like how you described it. Every every ticket has a story. I'm just going to go through the history of of the block just by sifting through the tickets, the the highs and lows.  
**Nikola Pivčević:** Yeah, Mike and I yesterday like we stumbled upon open PR that was made by Joel and Yeah, like it's so old like Yeah, I guess like most of the people here don't know who Joel is, but so that's how old it is, right?  
**Sean Winslow:** Yeah, I do notice yesterday when I was looking to the uh like for tickets for the bug tracker, I was just looking at all of campus stuff and yeah, there was a bunch of names that I've not not seen before.  
   
 

### 00:24:33

   
**Sean Winslow:** So, I was like, "Oh, that's interesting." The legend.  
**Nikola Pivčević:** Yeah, it's an amazing  
**Mike Price:** I spoke to like about a month ago.  
**Sean Winslow:** Yeah.  
**Mike Price:** He he hit me up.  
**Sean Winslow:** Was  
**Mike Price:** It's good to hear from He was  
**Sean Winslow:** he was he uh uh product or was he a  
**Mike Price:** DevOps.  
**Sean Winslow:** developer?  
**Mike Price:** He was our main DevOps guy. He did a lot of our infrastructure that still in production  
**Sean Winslow:** Gotcha.  
**Mike Price:** today.  
**Sean Winslow:** Wow. s\*\*\*.  
**Nikola Pivčević:** And he was the I guess like the second engineer to join join the block, right? It was first I guess uh uh Jake  
**Mike Price:** Jake who doesn't he the CTO and found co-founder of the  
**Nikola Pivčević:** and Yeah. Joel like installed WordPress,  
**Mike Price:** block and then yeah Joel made it  
**Nikola Pivčević:** right? Like Joel Yeah. Like installed like the first thing like Yeah.  
**Sean Winslow:** It's  
**Mike Price:** work we were on Paththeon days we were using Lando for development  
**Sean Winslow:** like it's like watching a movie and then you just start watching the prequel and you're just like, "Oh my god, this is how it came to be." Thank you,  
   
 

### 00:25:54 {#00:25:54}

   
**Mike Price:** Yeah. Yeah.  
**Sean Winslow:** Nicola. Speaking of legend, Romalt, what you got?  
**Ramuald Vishneuski:** Uh hello everybody. Uh we continue testing uh campus. Um we had one issue um after uh release uh that uh we didn't assign course to uh upskill LMS organization. So uh some users uh didn't have access to uh old course. Now it's fixed. Um yeah uh and we just continue doing uh uh stuff uh with cadets right now and all the bugs.  
**Sean Winslow:** Okay, thank you. Yeah,  
**Ramuald Vishneuski:** Yep.  
**Sean Winslow:** I've been keeping tabs on everything that you've been making edits to, so I appreciate  
**Ramuald Vishneuski:** Yeah.  
**Sean Winslow:** that. All right. Uh, Ed, is there anything that you want to discuss for a doctor  
**Edvinas Rupkus:** No,  
**Sean Winslow:** appointment?  
**Edvinas Rupkus:** I just No, I wrote a I wrote a Yeah, I'll have a late start today. So, I'll reply to emails and comments on all sigmas and and tickets uh later today. But uh the comment I don't know if it's sent in the chat was that after obviously like campus we're testing it and and uh after that we want to make sure that the migration tickets are done which are I think we're getting close to it but just a step of priority right after that the poly market widgets that Marina is working is like the next thing in in line in terms of priority.  
   
 

### 00:27:44 {#00:27:44}

   
**Edvinas Rupkus:** So, just wanted to uh reiterate  
**Sean Winslow:** Cool. All right. Yeah. And when it comes to updates on my end, that bug tracker should be done within the next hour. So, uh, I'll get that out to the campus folk. And that's really about it on my end. I had to talk to Matt, see what the timeline is about, and I'll let you guys know about that. And yeah, is there anything else that anybody wants to discuss before we head out? All right, everybody. Enjoy your Friday. Enjoy your weekend. Uh, I'll see you guys next Tuesday. And you're welcome.  
**Krystof Oliva:** See you guys.  
**Nikola Pivčević:** Sean, if you want to stay for the  
**Sean Winslow:** I was going to say, yeah. Later,  
**Nikola Pivčević:** Hi.  
**Sean Winslow:** guys. So, my last email that I got was the pro account was ending, but let's see if I can access it.  
**Nikola Pivčević:** I think I'm an admin in pro and even if like you lost your access I can like bring your access back.  
   
 

### 00:29:24

   
**Nikola Pivčević:** Oh yeah, I have the power,  
**Sean Winslow:** again.  
**Nikola Pivčević:** you know. So yeah. like Yeah, let me know like  
**Sean Winslow:** See,  
**Nikola Pivčević:** if  
**Sean Winslow:** let me see if because I I just have to find my password. I have it somewhere. All right. Yeah, I'm going to have I'm going to have to find this. But I tell you what, if if you could just uh grant me access and then if you just want to actually Would you mind? we could just go on yours and you could just walk me through like just how to access it and then I'll be able to play with it myself just so we're not sitting here while I'm fidgeting with my  
**Nikola Pivčević:** I think you should I think you should have  
**Sean Winslow:** stuff  
**Nikola Pivčević:** access products.  
**Sean Winslow:** sign on.  
**Nikola Pivčević:** See you have everything. Yeah.  
**Sean Winslow:** Oh, it's through. Okay.  
**Nikola Pivčević:** So I think you should have everything but I can I can share like how how it looks.  
   
 

### 00:30:34 {#00:30:34}

   
**Nikola Pivčević:** Okay. So yeah see like kind of you this is like kind of the list of products that you have like access to. So it's like you have everything. So I think it's that's that's  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** enough. Okay. Uh so Simon, so you go here and then open like this like uh chat, right? So the idea here like you know uh man, I didn't work for on this like for a long time.  
**Sean Winslow:** Mhm.  
**Nikola Pivčević:** But yeah, I was kind of like actively working on this back in the days when this was like still a thing. And uh uh so the idea of like this whole like connect project like like it's a kind of um project within pro and the idea was that you can connect with researchers and uh like other pe members of the block team and uh maybe like the idea was like maybe even like have like forums for like the blog pro members. to discuss with within themselves, right? Like kind of topics, right?  
   
 

### 00:31:44

   
**Nikola Pivčević:** Like kind of like a connect like a way to connect with other like folks and  
**Sean Winslow:** Mhm. I  
**Nikola Pivčević:** and within that platform.  
**Sean Winslow:** guess  
**Nikola Pivčević:** So we built Simon AI which is like kind of uh so so uh yeah just a way to uh yeah I can maybe like show you how it how it behaves. But let's let's let's ask a question and maybe let's ask a question about like a recent article. I want to see like if it still works.  
**Sean Winslow:** if  
**Nikola Pivčević:** Okay. So,  
**Sean Winslow:** it's  
**Nikola Pivčević:** uh let's see. Soil.  
**Sean Winslow:** so is it supposed to be like a chatbot that's trained all on the block's data like everything that the block collects  
**Nikola Pivčević:** Um. Yeah. So, so yeah, let me ask a question about something of from a recent article and see like uh does it like uh uh uh which which which yield protocol was launched by soil, right? Let's see. I'm currently not able to answer that question.  
   
 

### 00:33:12 {#00:33:12}

   
**Nikola Pivčević:** Oh, thank you so much for Yeah. So, let's maybe uh try something else. Um uh yeah smart yeah coin base uh what let's see like uh what is more see if it works. Okay. So that did like answer uh Moro launches Moro Prime. Is it this Morpho? Oh, so it kind of linked to the price page. It linked to Morph for lunches. Moro Prime I guess cryptolanding cryptoland more for CO. Yeah. And the outlook. Yeah. I guess like it's so kind of the how how how it should work, right?  
**Sean Winslow:** Mhm.  
**Nikola Pivčević:** Uh so every article that we publish we uh store in a so-called vector database and I don't know have you heard about this like rag rag implementation. Yeah rag. So so this yeah that's it.  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** So we are storing all our content in a rag like a vector database and then uh so whenever you ask a question to Simon. So it will first uh try to pick up the most important keywords from your query right like from whatever you asked.  
   
 

### 00:34:52

   
**Nikola Pivčević:** Then try using like this vector database. try to fetch uh I think like 10 or 20 articles uh from this vector database that might provide um answer the answer to your question and then we feed an NLM with all this um data right all those articles and with the original question that you asked right so let's say I ask this question right so what is morpho so we will extract again using LLM's um like the keywords most important keywords like morpho. Then we will f look through the uh to find articles that have potentially this answer this question and then when we get all those like uh articles you know make a big query to an LLM I think we're using chip and it's uh we kind of feed it like giving the users question what is morpho and the context when the list of all the  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** articles that we fetched from this vector database please answer please answer the questions right and and so the answer is like that the LLM provides is based  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** on the context that it was provided from our content right and then  
   
 

### 00:36:15

   
**Sean Winslow:** Okay.  
**Nikola Pivčević:** we link we also put links to um kind of sources that it used to give the answer Right?  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** And those sources not necessarily mean that it really uh the answer was answered from this using this source but it's was something that was provided as context to the LLM when it was giving the answer right so it we don't know like whether the really the information that is provided here is found in this article right so but it's something that was given to the LLM when they were generating this answer Nice.  
**Sean Winslow:** All right, cool. Yeah. Yeah.  
**Nikola Pivčević:** Yeah,  
**Sean Winslow:** No, I'm very familiar with all that stuff. I that's stuff that I've been very obsessed with as of late.  
**Nikola Pivčević:** that's  
**Sean Winslow:** So, I've been learning all about it. And yeah, I find that And do like how does it get updated if you haven't worked on it in a while? Is there someone keeping track of it or does it do the articles go straight into the vector database like right  
   
 

### 00:37:20 {#00:37:20}

   
**Nikola Pivčević:** yeah. So, yeah,  
**Sean Winslow:** at Oh,  
**Nikola Pivčević:** we built that pipeline and it's still working that pipeline, right?  
**Sean Winslow:** nice.  
**Nikola Pivčević:** So,  
**Sean Winslow:** Okay.  
**Nikola Pivčević:** so every time we publish or update an article, we update the vector database like with the new content and um but we we didn't like going to make any updates to how Simon works in general, right? Like we didn't man like I don't remember last time I sent a message to Simon.  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** Yeah.  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** Glad it worked at least.  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** So, yeah. Uh I I'm not sure like whether like there are like now like better like um like like  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** ways to do this, but I think this one is like pretty good, right? Like kind of we you don't want to like fit too much context to the LLM like this kind of like rag. I think like for this use case it's still good. I don't know like maybe if you're if you're reading about it maybe there are like new approaches to how to uh how to make like this is like a kind of I think like the best use case is like a help center like a chatbot where you kind of have like a knowledge base of like how to solve issues and then the chatbot like looks through the when you ask a question it looks through like through the knowledge base of like article how how to solve certain issues and then it  
   
 

### 00:38:34 {#00:38:34}

   
**Nikola Pivčević:** gives an answer to you Right. And I think like this is um uh still kind of the the best way to do it to do this kind of system. I don't  
**Sean Winslow:** Yeah, you're not wrong. That definitely is.  
**Nikola Pivčević:** know.  
**Sean Winslow:** And you don't want to overload it with context because then it just like starts hallucinating and giving you like random things that it could have pulled from. But there there are ways now.  
**Nikola Pivčević:** Damn.  
**Sean Winslow:** I don't know. So I would have to like take a look at it. It's more so just to stop wasting tokens where it's if you're using chat GBT there's like have you heard of skills like like clawed skills or agent skills.  
**Nikola Pivčević:** Oh yeah.  
**Sean Winslow:** So that's just a way for the LLM to like essentially take take the  
**Nikola Pivčević:** Yeah.  
**Sean Winslow:** keywords and not search like the full thing. It's just like picking and choosing. And so yeah, so that might be one way to update it. Outside of that, rag is still pretty popular, especially with a huge database.  
   
 

### 00:39:31 {#00:39:31}

   
**Sean Winslow:** So, I would like to dig in this some more.  
**Nikola Pivčević:** Yeah.  
**Sean Winslow:** I don't know, like at a future date, like when we're not as busy. But yeah,  
**Nikola Pivčević:** Yeah.  
**Sean Winslow:** I  
**Nikola Pivčević:** This is pretty cool. People were very excited about this product and then like it felt short because  
**Sean Winslow:** very  
**Nikola Pivčević:** uh we didn't have like enough users in pro, right?  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** So it didn't see like that much usage because we didn't expose it, right? Like I think like if this was like put on co I think like it would be like a really useful tool right but the problem is like yeah uh we cannot put it on code because yeah like running l  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** queries it's not cheap so kind of and you could spam  
**Sean Winslow:** Yeah. Exactly.  
**Nikola Pivčević:** it right a lot and people could abuse it. So, so yeah, we need to find some other way. But yeah, I think like it's pretty valuable, but yeah, we need to find a way to kind of bring it to a larger audience.  
   
 

### 00:40:23 {#00:40:23}

   
**Nikola Pivčević:** Yeah,  
**Sean Winslow:** Yeah,  
**Nikola Pivčević:** I don't know.  
**Sean Winslow:** I think yeah, bringing it to a larger audience. I think it's also what would be interesting is just using an open-source LLM that we train on our own data like but that would be a very timeconuming process but open source models are getting like ve pretty big and very uh  
**Nikola Pivčević:** Yeah.  
**Sean Winslow:** like very useful like people are  
**Nikola Pivčević:** Yeah. But yeah, I think like with with our kind of business model, we are in like the news business and like up-to-date information is the most important, right? And and the idea of of rag is like the day the context is immediately there,  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** right? So like when you need to train the LLM, then it like that takes time and then it you don't have the latest data, right? like you always always kind of behind. Uh and I think like another uh problem with uh with Simon is uh you know the new stories that we create are public data right it's not right that data that we own right like oh there is you cannot find this information anywhere else except you know here and um so LLMs now can search the internet right and  
   
 

### 00:41:31

   
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** then um the quality of results that you get from Simon AI  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** are not drastically better than what you get from like just quing chipd for example right because like they know this stuff right like they'll google it in the  
**Sean Winslow:** Yep.  
**Nikola Pivčević:** backgrounds in the background like take the first five results they get from Google and u and take it in as the context right so uh yeah so kind of like yeah that I think like this is also like kind  
**Sean Winslow:** Yeah. Cool.  
**Nikola Pivčević:** of something to to think about like I think we also did this exercise uh and uh like people were asked like oh query something and then rate the uh how do you say like the score like the answer that Simon provided versus like a regular like chpt query and um uh mixed results right like so it's not always like Simon like sometimes provides poorer results than uh than like just straight up asking chip.  
**Sean Winslow:** You you did an an evaluation between Chad GBT and  
**Nikola Pivčević:** Yeah.  
   
 

### 00:42:50 {#00:42:50}

   
**Nikola Pivčević:** Yeah. Yeah.  
**Sean Winslow:** Simon.  
**Nikola Pivčević:** I think like there was like when we released this like uh people like internal internally were doing this test and I'm sure like there is like this like spreadsheet where people like were adding their comments about like um the results and like yeah like positively like in I don't know like kind of how we marketed it is in um 70% of cases Simon AI provided the same or better results than CHP which sounds like like pretty good but on the other hand like oh in 30% of the cases J GPT gave a better answer right so it's yeah  
**Sean Winslow:** Yeah. Huh. All right. Yeah. I definitely if if if this gets resurfaced, I would love to dive in a little bit more because I I I also just recently found um Google Google has a product within Google Labs that you essentially do the evaluation side by side. It's just it gives you a visual um like test score and like if you just provide the API keys and ask specific questions, it's just kind of an interface for you to actually work with that stuff.  
   
 

### 00:44:01 {#00:44:01}

   
**Nikola Pivčević:** Yeah. All  
**Sean Winslow:** But yeah, I and I think yeah,  
**Nikola Pivčević:** right.  
**Sean Winslow:** there there are definitely ways to because like not all LLMs are up to date either. Like there are things that I would find out about and then start typing it in and it's like I don't know what that is.  
**Nikola Pivčević:** Yeah.  
**Sean Winslow:** Can you give me more information about that?  
**Nikola Pivčević:** Yeah. Yeah.  
**Sean Winslow:** So if you incorporate like our data and then our articles that are like constantly updating like if there's a way to just feed the feed that into the vector database like constantly like I think this could be something a bit more interesting and cheaper if we decide to just like pivot to an open source model and that is trained on our data and then yeah I think it's something I I would have to think about but and we can like talk about it in the future because I think it for sure You're not you're not wrong. It's something that would benefit like a lot of people just visiting the site and not just pro users.  
**Nikola Pivčević:** I think it's uh like it does better uh when searching for really recent news, right? And I think like this is probably like the biggest value.  
**Sean Winslow:** Yeah.  
**Nikola Pivčević:** I don't know in my mind but because like yeah we when you ask Simon it immediately has in context the most recent articles which is like pretty nice  
**Sean Winslow:** Yeah,  
**Nikola Pivčević:** right um yeah  
**Sean Winslow:** cool.  
**Nikola Pivčević:** uh does that man like if you have like if you're not I'm not able to access pro whatever like yeah let me know like we can we can figure it  
**Sean Winslow:** I will. Yeah, thank you. I I should definitely be able to access it. I saw um I have to do the authenticator app on Microsoft, so I was just essentially live, but I the email, so I should be good. Awesome. Thank you very much,  
   
 

### Transcription ended after 00:45:58

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*