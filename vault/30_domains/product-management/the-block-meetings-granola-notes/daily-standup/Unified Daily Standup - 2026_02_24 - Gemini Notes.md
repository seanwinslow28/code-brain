# 📝 Notes

Feb 24, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivčević](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Panasenko](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [Krystof Oliva](mailto:koliva@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMjRUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.y7izhsssf2gh) 

### Summary

**Technical Fixes and Design Review**  
Multiple tickets are progressing, including fixes for the VQA marketing page, anti-bot verification issues, and initial testing for the Poly Market widget. The team is also resolving several access tickets and technical issues related to user deletion operations.

**API Migrations and New Projects**  
Key development projects include migrating from the Metricool API to the Pro Social API for social media data and investigating an in-house Terraform solution to avoid cloud costs. Work is advancing on optimizing learn article metadata for LLMs, beginning the report card module development, and preparing the new Pro API project for integration.

**Multicourses Release and Prioritization**  
The multicourses release is nearing completion, with the team focused on resolving final QA issues and planning the timeline for future functionality like payments and individual workflow. The team decided that payment integration and sponsored courses are currently higher priorities than fixing the current demo organization access

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

## NEEDS FURTHER DISCUSSION

* **Proprietary Terraform Implementation Exploration** An exploration into creating a proprietary Terraform implementation is being conducted instead of continuing with Terraform Cloud due to impending costs.

## ALIGNED

* **Poly Market Trending Events Display** Top trending Poly Market events must be automatically fetched every X hours for display on the homepage.

* **Multi-Language Project Communication Flow** Edvinas and Matt must be kept informed regarding big blockers or new decisions related to the multi-language project.

* **US Election Category Creation** The US election category must be created for articles on WordPress.

* **Demo Organization Access Deprioritization** Fixing or adjusting the demo organization access feature is deprioritized in favor of payment and sponsored course work, relying temporarily on trial subscriptions for demo access.

*More details:*

* **Initial Check-in and Technical Updates**: Aliaksandr Kryvanosau created a PR for the VQA ticket concerning the campus marketing page and is working on the last fix for providing anti-bot verification on the subscribe email, currently encountering issues with testing it on the newsletter. Sean Winslow noted that they would bring up Aliaksandr Kryvanosau's comment about the design with Serena later that day ([00:01:25](#00:01:25)).

* **Poly Market Widget and Migration Status**: Ana Benitez reported that testing for the poly market widget tickets is looking good, as Marina has fixed all the issues, and the ticket was sent to BQA for design review. Ana Benitez will also continue with the data dashboard migration and is working on several access tickets with Brian Mendoza ([00:02:35](#00:02:35)).

* **Ticket Completion and Exam Results**: Bohdan Panasenko completed several small tickets, including adds for the price converter, with a couple more ready for testing ([00:02:35](#00:02:35)). A ticket concerning an error during a user deletion operation is awaiting deploy, although another issue with user deletion was found that may require a new ticket. Bohdan Panasenko also shared that they achieved a perfect score of five on a recent exam ([00:03:47](#00:03:47)).

* **Access Tickets and Poly Market Configuration**: Brian Mendoza is working on advancing access tickets and improving several PRs for the data dashboard, and they will also look into a comment regarding the poly market WordPress material ([00:03:47](#00:03:47)). Edvinas Rupkus confirmed that the current system is set up to automatically fetch the top trending Poly Market events—which are the markets that are most being bet on or predicted—to display on the homepage. This automatic fetching occurs every 24 or 48 hours, although Brian Mendoza noted that events can be manually switched out in WordPress if necessary ([00:05:02](#00:05:02)).

* **Social Platform API Migration and Terraform Plans**: Cesar Paz is continuing work on the J redirect project and has started a new task to replace the Metricool API with the Pro Social API to gather data for Instagram, Facebook, and TikTok, following the discontinuation of Metricool ([00:06:08](#00:06:08)). Additionally, Cesar Paz is tasked with exploring the option of creating an in-house Terraform solution rather than using Terraform Cloud, which is expected to start incurring costs in April ([00:07:26](#00:07:26)).

* **Anthropic's Claude Agent SDK Investigation**: Cesar Paz has not yet looked into the Claude agent SDK but created a new Confluence page outlining how to use Claude via the command-line interface, which is more cost-effective than using an API key ([00:08:35](#00:08:35)). They explained that this approach allows connecting a repository to Claude for context-specific questions and functionality requests. Krystof Oliva offered to collaborate on this topic, as they have experience with Claude and other LLM agents from their school projects ([00:09:33](#00:09:33)).

* **Learn Article Metadata and Multilanguage Project**: Koray Baspinar is currently optimizing the learn articles metadata to be more LLM-friendly, checking crow stats, and addressing href issues. They are also discussing the path forward for the multilanguage project with Nikola Pivčević, and Edvinas Rupkus requested to be kept in the loop regarding any major decisions or blockers ([00:10:45](#00:10:45)).

* **Broken Links and AI/ML Background**: Krystof Oliva confirmed they are wearing pants, completed their first dev box ticket for broken external links, and the fix is ready for testing ([00:12:09](#00:12:09)). They also learned about the Google open framework AMP and switched to working on the ticket to remove big images from the codebase. Krystof Oliva further detailed their AI specialization in computer science, including a project where they use LLM models to analyze data from ICU ventilator systems for doctors ([00:13:14](#00:13:14)).

* **Scheduling a Meeting with Mike Price**: Krystof Oliva and Mike Price discussed finding time to meet one-on-one, with Mike Price proposing they schedule some time for tomorrow since they would be available earlier. Mike Price confirmed that they would be taking their kids to the skating rink later today ([00:15:27](#00:15:27)).

* **Report Card Module and Hero Section Category**: Maryia Zhynko began working on the report cards module, having completed the visualization part and moving on to implementing API fetching ([00:15:27](#00:15:27)). Maryia Zhynko also inquired if the "US election" category had been added to the hero section for articles on WordPress. Edvinas Rupkus confirmed that they would talk to Adam about creating the category and acknowledged that the poly market team had been diligent with feedback, leading to minor design changes in Figma that would be updated in the ticket ([00:16:32](#00:16:32)).

* **Data Dashboard Fixes and Poly Market Work**: Marina Lozuk fixed an issue with the data dashboard, making it ready for testing, and made adjustments for the poly market as reported by Ana Benitez. Marina Lozuk has now started the task for the poly market and the election page. Edvinas Rupkus confirmed with Maryia Zhynko that any requirement not present in the current Figma file, which is actively being kept up to date, should be disregarded ([00:18:00](#00:18:00)).

* **API Development and Testing**: Mike Price reported that the new Pro API project is mostly ready and that they are wrapping up Simon AI for Jordan Leech's integration. Mike Price got the AI summaries API for the backend pushed out late last week, but testing the iOS app digest did not go well this morning, so they are currently working on a fix ([00:19:30](#00:19:30)).

* **Multicourses Release Status and Future Plans**: Mikita Hulis and their team are actively resolving remaining QA issues for the multicourses release, with most items resolved, deployed, and retested. The current tasks focus on final suggestions and adjustments, working closely with Roma and Claudine. Once the current release is finalized, the team plans to provide a timeline for future functionality, including wrapping up payments and the individual workflow ([00:20:54](#00:20:54)).

* **Credential Migration and Sponsored Course Planning**: Nikita Orobenko finalized the migration for cleaning up issued credentials and is waiting for Roma to ready the dev box for testing and production deployment. For the next step—sponsored courses—Nikita Orobenko anticipates the need for design adjustments to the marketing page and dashboard, including the ability for users to create a profile without payment ([00:22:22](#00:22:22)). Edvinas Rupkus confirmed that Claudine is working on the designs, and they will have a sync meeting to review and refine the requirements ([00:23:48](#00:23:48)).

* **Demo Organization Access and Priority**: Nikita Orobenko and Roma discussed that spending time fixing or adjusting the current demo organization access might not be worthwhile, as the entire concept may need to be redefined due to changes like the introduction of subscriptions. Currently, payment integration and sponsored courses are higher priorities, and demo access can be temporarily managed using trial subscriptions ([00:26:00](#00:26:00)). Edvinas Rupkus agreed with this assessment and committed to ensuring the discussion is raised with stakeholders like Matt during the next campus refinement to determine the long-term strategy for demo access ([00:27:29](#00:27:29)).

* **Video Content and Site Translation Investigation**: Nikola Pivčević wrapped up video content work for the elections hub, and the WordPress part is ready for Maryia Zhynko to start on the front end ([00:28:30](#00:28:30)). They also started investigating translating the site into Spanish and bought a popular WordPress translation plug-in that offers automated translation tools, potentially using DPL or Google Translate ([00:29:41](#00:29:41)). Nikola Pivčević noted that the plug-in translates data, but manual translation might be required for front-end labels and other terms ([00:31:16](#00:31:16)).

* **Ongoing QA and Testing**: Ramuald Vishneuski is working with both Mikitas to resolve all remaining issues and find new ones for the multicourses release. They also need to go through many test scenarios and are currently fixing automated tests ([00:34:02](#00:34:02)).

* **Deployment Status and Cleanup**: Edvinas Rupkus confirmed they have been addressing individual issues with developers and noted that moving away from NX is the biggest priority ([00:34:02](#00:34:02)). They also confirmed that they would keep the election coverage requirement tickets updated. Bohdan Panasenko inquired about deployment status, and Mike Price confirmed that deployments are back up and running, although a shift to a more resilient system is planned for a later time ([00:35:32](#00:35:32)).

### Suggested next steps

- [ ] Edvinas Rupkus will talk to Adam to create the US election category for the articles on WordPress, look into the ticket regarding the updated at date in the hero section, and update the poly market ticket today.

- [ ] Brian Mendoza will look at the poly market WordPress comment and check the code for the poly market events to see what the ticket says and if there is a bug to fix.

- [ ] Koray Baspinar will keep Edvinas Rupkus and/or Matt in the loop with any big blockers or new decisions regarding the multi-language project.

- [ ] Edvinas Rupkus will schedule a refining call to address any necessary adjustments regarding the sponsored courses.

- [ ] Sean Winslow will make sure that the group does not forget about addressing the demo access with Matt during the next refinement call.

- [ ] Nikola Pivčević will link the Confluence document outlining how the translation plug-in works in the background inside the ticket.

- [ ] Mike Price and Krystof Oliva will carve out some time tomorrow to meet up.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=rQIvHf2XCBUUu0COzSFLDxIWOAIIigIgABgBCA&detailid=standard)*

# 📖 Transcript

Feb 24, 2026

## Unified Daily Standup \- Transcript

### 00:00:00

   
**Edvinas Rupkus:** Everyone.  
**Sean Winslow:** What's up, guys?  
**Krystof Oliva:** Yes.  
**Sean Winslow:** Cora, what are you talking about? Your background.  
**Mike Price:** So  
**Sean Winslow:** Drew Boomer to change that.  
**Koray Baspinar:** Yeah, yeah, yeah, yeah,  
**Mike Price:** happy.  
**Koray Baspinar:** man. I cannot change it.  
**Sean Winslow:** Okay.  
**Mike Price:** I swear Google released an update or something where they used to like bring me in the call. My camera would never be on automatically. And the last few times my camera would just automatically be on. And poor Corey was on the line when I decided to join the when we had our 101 and he got to see me on my boxers. So,  
**Koray Baspinar:** No, it is.  
**Mike Price:** so embarrassed and I'm so h I'm so happy I decided to get dressed.  
**Koray Baspinar:** No, it is at all.  
**Mike Price:** So, I'm happy for all of y'all.  
**Sean Winslow:** That's the work from home life.  
**Krystof Oliva:** You guys are wearing pants. Uh, I don't  
**Mike Price:** I Yeah, I at least decided to put pants on at this point.  
   
 

### 00:01:25 {#00:01:25}

   
**Mike Price:** So, yeah. Yeah. Yeah.  
**Sean Winslow:** Yeah, Kristoff,  
**Krystof Oliva:** I  
**Sean Winslow:** I noticed that the camera's very close to your face. I wonder why. Oh, there are pens. All right, we'll get started.  
**Krystof Oliva:** usually working from cafes.  
**Sean Winslow:** Yeah, Ben's good. All right, Alex, follow that up. What you got?  
**Aliaksandr Kryvanosau:** I I got some pencil as  
**Mike Price:** That's great.  
**Sean Winslow:** Yeah, everyone.  
**Aliaksandr Kryvanosau:** well.  
**Sean Winslow:** Everyone just state whether or not you're wearing pants.  
**Mike Price:** I'm wearing pants now.  
**Aliaksandr Kryvanosau:** Uh okay. So I created a PR for the VQA ticket about campus marketing page and then I was finalizing jobs and currently I'm working on the last fix about providing antibot verification on the subscribe email. Currently having some issues with testing it on the newsletter to see how it works. So working through  
**Sean Winslow:** Cool.  
**Aliaksandr Kryvanosau:** it.  
**Sean Winslow:** Thank you. Yeah, I saw your comment about the design. Uh, we're meeting with design later today, so I'll bring it up to Serena.  
   
 

### 00:02:35 {#00:02:35}

   
**Aliaksandr Kryvanosau:** Okay, sounds good.  
**Sean Winslow:** Thank you, Anna.  
**Ana Benitez:** Um hello. So yesterday I was testing putting market widget tickets. Um as I mentioned, Marina has fixed like all the issues and it's looking good. So I just sent the message on BQA for design. Um and well I will continue with migration uh for data dashboard and braces. Um also there's some tickets for access I've been working with Brian. So I'll continue with those thoughts and that's all I  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** Thank you so much for letting us uh letting the  
**Ana Benitez:** say.  
**Edvinas Rupkus:** poly market tickets skip to the queue.  
**Ana Benitez:** Of  
**Edvinas Rupkus:** We got to show it to them.  
**Ana Benitez:** course  
**Sean Winslow:** Thank you, Anna. Well done. Welcome  
**Bohdan Panasenko:** Yes.  
**Sean Winslow:** back.  
**Bohdan Panasenko:** Uh hello. Um so did uh some like relatively small tickets adds for price converter. Uh a couple of more tickets are ready for testing.  
**Krystof Oliva:** It's  
**Bohdan Panasenko:** The ticket for error when a user deletion operation is  
   
 

### 00:03:47 {#00:03:47}

   
**Sean Winslow:** Cool.  
**Bohdan Panasenko:** performed. It's a waiting deploy actually. But we found another issue with the user deletion. But that's probably already another ticket. And uh yeah, a couple of more tickets for like uh on on that server. And yeah, that's pretty much it for what I've done so far.  
**Sean Winslow:** Thank you both. How'd the uh how' the exam go?  
**Bohdan Panasenko:** Yeah.  
**Sean Winslow:** Did you get the results  
**Bohdan Panasenko:** Yeah, I got uh five.  
**Sean Winslow:** back?  
**Bohdan Panasenko:** So, it's fine. So, it's good.  
**Sean Winslow:** Nice.  
**Krystof Oliva:** the best actually. It's the perfect score.  
**Bohdan Panasenko:** Yeah, it's great.  
**Sean Winslow:** It's fun. Thank you, Bon. And congratulations, Brian.  
**Brian Mendoza:** Cool. I was working on moving along the access tickets and improving some PRs for uh data dashboard and I will just continue working on that. I think there's a comment for the poly market WordPress stuff.  
**Sean Winslow:** Perfect.  
**Brian Mendoza:** I'll take a look at that as well. Yeah.  
**Sean Winslow:** Thank  
   
 

### 00:05:02 {#00:05:02}

   
**Edvinas Rupkus:** Uh yeah,  
**Sean Winslow:** you.  
**Edvinas Rupkus:** I guess I guess while we're on it, uh is Marine on a call? Okay, perfect. Uh we basically have set we initially thought that we're going to like manage it manually and that's why Brian you set up that uh WordPress like interface to manage all those poly market events. But now I think like the direction came from there and to just like show trending markets uh on the homepage at least and basically like what's what's most being bet on or what's mostly being you know predicted. That's basically what should show up on our homepage. Is that is that what we currently have on the dev  
**Brian Mendoza:** Yes.  
**Edvinas Rupkus:** box?  
**Brian Mendoza:** Uh the way it works is it's fully automatic. Um I think the question I was referring to was like it was like the quantity of events are being fetched,  
**Edvinas Rupkus:** Yeah.  
**Brian Mendoza:** but the way it works is automatically every 24 hours or 48, we can change that to whatever we want we want it to be. Every x amount of hours, we automatically fetch the top trending events.  
   
 

### 00:06:08 {#00:06:08}

   
**Brian Mendoza:** And if we want to change it for whatever reason, like if it's like a weird thing politically or something that we want to take off, we can go into WordPress and switch it out.  
**Edvinas Rupkus:** Yeah,  
**Brian Mendoza:** But it's all  
**Edvinas Rupkus:** understood.  
**Brian Mendoza:** automatic.  
**Edvinas Rupkus:** Okay,  
**Ana Benitez:** So it by showing like how many events we want  
**Edvinas Rupkus:** perfect.  
**Ana Benitez:** to uh to populate because right now we support up to 10 on WordPress right but on the debox I believe there are five or I don't know Brian how this chrome job works  
**Brian Mendoza:** Yeah, it's been a minute since I saw this um like the code for it. I will open it up,  
**Sean Winslow:** Awesome.  
**Brian Mendoza:** but yeah, we'll see. We'll look at what the ticket says and what it's doing. And if it's a bug, we'll fix it. I don't remember off the top what it should be.  
**Ana Benitez:** Okay, thanks.  
**Sean Winslow:** Thank you, Brian.  
**Cesar Paz:** Uh hi.  
**Sean Winslow:** Caesar  
**Cesar Paz:** Well um I keep working in the J redirect some pro and and and I I've started a new task to change because we finally off metricool and we are we were getting data from metricool to jungle um for Instagram, Facebook and Tik Tok.  
   
 

### 00:07:26 {#00:07:26}

   
**Cesar Paz:** So I need to do the same for the new platform we are using now which is pro social. So yeah I need to change the API from metric to pro social in order to get the same data. And in addition I've created a new task. Um Mike told me that maybe we need to uh create our own terraform instead of using terraform cloud. Uh, terapfor clown is going to start to cost money from April probably. So, I'm going to explore this option and I'm going to start this one probably now uh or as soon as possible. Um, yeah, I think that's all.  
**Edvinas Rupkus:** Just quick comment. This is not related to work.  
**Cesar Paz:** Yeah.  
**Edvinas Rupkus:** Uh is there anything different with your mic today as opposed to other days you're sometimes I is I have hard time hear like I can understand you but I have a hard time hearing you but specifically because of the  
**Cesar Paz:** H  
**Edvinas Rupkus:** mic but is something this like whatever you're doing today that's great.  
**Cesar Paz:** sorry.  
   
 

### 00:08:35 {#00:08:35}

   
**Edvinas Rupkus:** So I have very you sound very clear right now. So that's a different mic or different I don't know whatever just you know  
**Cesar Paz:** Sorry. Sorry. Probably.  
**Edvinas Rupkus:** it's all fine I mean I can understand it's just easier to  
**Cesar Paz:** Okay. Okay. Sorry. Uh should I should I repeat? Uh no.  
**Edvinas Rupkus:** No, no, no. You you're you were perfectly clear today.  
**Cesar Paz:** Okay.  
**Edvinas Rupkus:** I'm saying like whatever you doing today,  
**Cesar Paz:** Okay.  
**Edvinas Rupkus:** continue doing that because that's that's  
**Cesar Paz:** Okay. Okay. Okay. Okay.  
**Sean Winslow:** Yeah.  
**Cesar Paz:** Perfect.  
**Sean Winslow:** And and Caesar, quick question. Have you uh been able to look into the clawed agent SDK at all?  
**Cesar Paz:** Uh not yet. But I I added a new confluence page uh which is published in dev uh in the dev channel. Uh it basically to uh start how we can use cloud um through the cloud cle the command uh line uh because in this way it's uh much cheaper than use an ap key.  
   
 

### 00:09:33 {#00:09:33}

   
**Sean Winslow:** Oh.  
**Cesar Paz:** So yeah in this way we can connect a repository um and give all the context to um yeah to cloud to cloud uh ask question about the repository uh okay please give me this functionality based on this uh code or something like this. So I created the conference page is there if you need access to clo uh maybe probably we need to uh share the keeper credential with you and in addition probably the first time when you sing in cloud you need uh for me or for Mike probably uh to redirect an email that we receive from cloud in order to sing in by using an a URL  
**Sean Winslow:** Okay, cool. Yeah.  
**Krystof Oliva:** May maybe maybe Caesar if if I can I can help you out with that or like learn from you maybe because I I used  
**Cesar Paz:** Yeah.  
**Krystof Oliva:** to clo and cloud by and the agent and I mean I studied the LMS like in school. So maybe I can give you some insight on or maybe you can give me some insight and we can work it out  
   
 

### 00:10:45 {#00:10:45}

   
**Cesar Paz:** Okay.  
**Sean Winslow:** Yes.  
**Cesar Paz:** Yeah,  
**Krystof Oliva:** together.  
**Cesar Paz:** of course. Uh if you want to you can create new confluence page for for all the team because if you have more context that's fine.  
**Krystof Oliva:** I don't know if I have all the context to share like I I shared some basic in the in the Slack channel uh recently but but yeah I mean I I use the not just cloud but all the  
**Cesar Paz:** Okay.  
**Krystof Oliva:** APIs of the agents for my like side project for my thesis in school. So maybe I can tell you how I use it myself.  
**Cesar Paz:** Okay.  
**Sean Winslow:** Nice.  
**Cesar Paz:** Okay. Of course. Yeah,  
**Sean Winslow:** Cool.  
**Cesar Paz:** thank you.  
**Sean Winslow:** Thank you. Yeah. And thank you, Kristoff. Corey.  
**Koray Baspinar:** Hello. Uh I am right now working on uh I'm playing with uh learn articles metadata. Uh I am trying to make it more LLM uh friendly and see how they perform after I change it. And also I am creating I'm checking checking crow stats as well and working on href issues and also uh Nicolola had some uh comments about our multil- language project.  
   
 

### 00:12:09 {#00:12:09}

   
**Koray Baspinar:** So uh we are discussing uh how we move forward uh about multil- language project. So yeah, that's all.  
**Sean Winslow:** Cool. Thank you,  
**Edvinas Rupkus:** Can can you keep me and or Matt in the loop with like if you have any,  
**Sean Winslow:** Corey.  
**Edvinas Rupkus:** you know,  
**Koray Baspinar:** Yeah.  
**Edvinas Rupkus:** big blockers or new decisions that come in because Matt's interesting  
**Koray Baspinar:** Yeah. Yeah.  
**Edvinas Rupkus:** too  
**Koray Baspinar:** Nicola had some comments and I also replied him. He has some concerns and uh I replied him about his  
**Edvinas Rupkus:** in the in the ticket.  
**Koray Baspinar:** concerns. Uh no we just discussed in uh we we just we don't have something concrete right now  
**Edvinas Rupkus:** Is it Got  
**Koray Baspinar:** but once we have I think yeah we will we will present it.  
**Edvinas Rupkus:** it.  
**Koray Baspinar:** Yeah.  
**Sean Winslow:** Perfect. Thank you,  
**Edvinas Rupkus:** Sweet.  
**Sean Winslow:** Corey  
**Krystof Oliva:** Hi guys. Uh, so I'm wearing pants and on Friday I had one-on-one with Nicola.  
**Sean Winslow:** Kristoff.  
**Krystof Oliva:** Uh, we talked about like the first week in the blog.  
   
 

### 00:13:14 {#00:13:14}

   
**Krystof Oliva:** Uh, and also we created my first dead box. Like I finished the ticket. So we made it ready for testing. That's the broken external links one. And yeah, so now now that's prepared for testing. Then I learned about the AM the Google open framework because Nola like gave me an interview.  
**Sean Winslow:** Awesome.  
**Krystof Oliva:** So I want to learn more about it. uh and how to kind of make um the SEO better and yeah then I switch on to working on the remove big images from codebase ticket which I'm working on now and yeah right before the call I had a short call within and that's it for me.  
**Sean Winslow:** Thank you. And yeah, you you studied that uh what is it? AI coding is your uh like that's what  
**Krystof Oliva:** Well,  
**Sean Winslow:** you're  
**Krystof Oliva:** I I yeah I mean I I'm studying CS like the computer science in the Czech technical university in Prague but like my specialization we have specialization so some people do games some people do just software engineering and I do AI so we do like AI projects and one of the projects which I'm working on now is like for the last kind of nine months and I will work on it for the next six months is uh it's a bit complicated but basically Basically, it's like um ICU ventilator system and I use AI to analyze their data from the  
   
 

### 00:14:31

   
**Krystof Oliva:** ventilators like people which are really sick. Uh so I analyze the data using different LM models and then I just give the results to the doctors. So I'm kind of using these uh agents and LLMs and different uh API keys for that. So I can help with that basically.  
**Sean Winslow:** cool, man. Yeah, I'll definitely pick your brain.  
**Krystof Oliva:** Plus I'm a VI coder so I use it for coding as well.  
**Sean Winslow:** I am very nice. Yeah, same. I dabble, so I' I'd definitely be I'll be asking you some questions in the future. Thank you,  
**Krystof Oliva:** I feel like maybe Mike I don't know if you saw the message on the slide but we we talked about the call about  
**Sean Winslow:** Chris.  
**Krystof Oliva:** it if you if you know the time about  
**Sean Winslow:** Say that again.  
**Krystof Oliva:** Is is my contact call?  
**Sean Winslow:** Muted.  
**Krystof Oliva:** Is my call or not?  
**Mike Price:** on the call. Sorry about that. I was talking to my kid. What's uh yeah, we're supposed to get up.  
   
 

### 00:15:27 {#00:15:27}

   
**Krystof Oliva:** Ah.  
**Mike Price:** Um I today I'm taking my kids to the skating rink. Um but I will be available in the next few hours oneonone with Nicola um after this. Um but yeah, I'll be working on a few things. Um so yeah, did you want to meet up afterwards? How how how are you on today?  
**Krystof Oliva:** Uh yeah, maybe in the evening like from 9 I can do or tomorrow or Wednesday. I'm working like mostly during the week so I can I can do it also tomorrow or Thursday.  
**Mike Price:** Okay. All right. We'll carve some time.  
**Krystof Oliva:** Okay.  
**Mike Price:** Let's carve some time for tomorrow and we'll um I'll be on a bit earlier and we can we can do that.  
**Krystof Oliva:** Okay. Thank you. Thank you.  
**Mike Price:** All right. Cool. Yeah.  
**Sean Winslow:** Sweet. Thank you, Mike. Thank you, Kristoff. Maria  
**Maryia Zhynko:** Today I started working on report cards uh module. Uh the visualization part is already done and I'm going to start with uh implementing API fetching.  
   
 

### 00:16:32 {#00:16:32}

   
**Maryia Zhynko:** Also I have a question regarding hero section. Did uh someone already add new uh US election category or do I need to do I need to do it myself?  
**Sean Winslow:** Did Someone.  
**Edvinas Rupkus:** Oh, for the articles on WordPress, you mean? Yeah,  
**Maryia Zhynko:** Yes.  
**Edvinas Rupkus:** we're going to have to add it. Yeah, I mean there's there's no articles specifically written for it yet, but we'll Yeah, we probably should do it so at least start building a library of those of those categories. So I I'll I'll talk to Adam and tell him to create it. Uh good call out. I don't know if you saw the Figma file. There were slight changes to like nothing crazy. It's just poly market has been like super super like diligent and picky with their with their feedback. So there are small things that Serena changed on Friday. Um, and I'll try to make sure that the ticket is updated today to like reflect everything as clearly as as possible.  
**Maryia Zhynko:** Yeah, I've seen Figma and also one more question uh in the ticket it says that there should be updated at uh date uh after the uh this uh details about the page with uh enter navigation.  
   
 

### 00:18:00 {#00:18:00}

   
**Maryia Zhynko:** Um but on Figma there is no uh such a field.  
**Edvinas Rupkus:** Uh, is this in the main the main one that's on your in progress right now? Okay,  
**Maryia Zhynko:** Yes.  
**Edvinas Rupkus:** I'll take a look in that for  
**Sean Winslow:** This one right here.  
**Edvinas Rupkus:** sure.  
**Maryia Zhynko:** Yes.  
**Sean Winslow:** Okay. All right. Thank you, Maria. Marina.  
**Marina Lozuk:** Hello guys. Uh, as for me, I fixed the issue for the data dashboard. So, it's ready for for testing and also tweaked some uh some stuff for the poly market which Anna reported and just embarked on the task for poly market and the election page. That's it.  
**Edvinas Rupkus:** I assume uh Brian, Marina, Maria, you guys synced and and figured out a way to DVD up the work to like attack it from all sides.  
**Brian Mendoza:** Yep.  
**Edvinas Rupkus:** Sweet. Yeah, I just took a look at it. Um, Maria, there's I think it's just uh you know, you can you can disregard that little piece of of uh requirement. I think it's just like specifically instructing you to utilize the similar HTML elements for time and and whenever it's applicable.  
   
 

### 00:19:30 {#00:19:30}

   
**Edvinas Rupkus:** So nothing to worry about there. Design is up to date. Design if if you don't see stuff on design that's not then it's probably not uh not required.  
**Maryia Zhynko:** Okay.  
**Edvinas Rupkus:** We're keeping the Figma file like very much uh from going stale.  
**Sean Winslow:** Cool. Thank you, Marina. Mike  
**Mike Price:** um was getting the pro API up and running. Uh the new pro API project, it's mostly ready. Um wrapping up Simon AI now for Jordan Leech, so you can do integration with it. Um our digest um testing out the iOS app. The digest seems to I I got it the AI summaries pushed out API for the back end for it out last I think. early late last week. Uh testing didn't go so well this morning. Um the simulations did, but the actual um test didn't work right. So, I'm working I'm currently looking into fixing that and seeing if we can get that working. Um yeah, that's pretty much that's the top of the list.  
   
 

### 00:20:54 {#00:20:54}

   
**Mike Price:** I'm running through a few things, but that's that's top of the list right now.  
**Sean Winslow:** Nice. All right. Cool. Thank you, Mike Nikita.  
**Mikita Hulis:** Yep. So, some good news. We are both me and you all are working on uh resolving the uh still ongoing QA session for the multicourses release. At this point, most of the things not only are resolved but also deployed and retested and but stuff is still uh coming from the sessions. Now uh it is more so suggestions slash adjustments for the final version of the release. So we are working on those closely with Roma as well as Claudine who has her input uh into the how things should look and or function. Uh so wrapping wrapping this up. Hopefully the the stream of of those uh adjustments will soon end and afterwards we are planning to um provide a plan slash uh timeline for the future uh functionality such as like finishing wrapping up uh payments uh the individual workflow etc etc but need need a few days I would say to uh to finalize the current release, so to speak.  
   
 

### 00:22:22 {#00:22:22}

   
**Sean Winslow:** Perfect.  
**Mikita Hulis:** And that's about it.  
**Sean Winslow:** Thank you. And yeah, I'm sure you saw the campus tracker. You could just just make notes in there and then I can like completely update it for you guys just to, you know, just so we can view it and catch up to speed and everything like that. But yeah, thank you Nikita O.  
**Nikita Orobenko:** Um, yep. Pretty much the same thing. Uh, finalized the migration uh for cleaning up the creds uh the issued creds mess. uh we that during the release uh Roma will ping me out uh once the dev box will be ready to apply it and test it out and once it will be done we will push it to the prod and we'll apply it as well and talking about the sponsored course courses since it will be basically the next step for the campus uh I assume we'll need some design adjustments to handle uh like the marketing page thing. Um I suppose a little adjustment to the dashboard uh in terms of how we actually should present them to the user plus the possibility to create a profile without paying anything.  
   
 

### 00:23:48 {#00:23:48}

   
**Nikita Orobenko:** We will need to have it as well. I mean like we can reuse a lot of elements we already have but we'll need to think about how that should work. Actually I don't think there will be like technical limitations on the back end  
**Edvinas Rupkus:** Okay. Yeah, I should click  
**Nikita Orobenko:** to support any of those uh things.  
**Edvinas Rupkus:** one.  
**Nikita Orobenko:** I would call them adjustments. Uh but anyway, we still need to handle the design adjustments plus do the work on side as  
**Edvinas Rupkus:** Yeah. Yeah, Claudine is working on design. She's she's going to do uh like it's going to be like sort of like a cousin of crypto  
**Nikita Orobenko:** well.  
**Edvinas Rupkus:** IQ authorization like something something like that basically. But yeah, she's working on designs for that and then we have a sync today. So hopefully we'll review that and I'll definitely let her know that like you know we want we'll need a dashboard adjusted to to completely um take care of that you know requirement and and then  
**Nikita Orobenko:** I mean it sounds like yeah it's more about just using the same cards  
   
 

### 00:24:50

   
**Edvinas Rupkus:** also  
**Nikita Orobenko:** but instead of you know like maybe the blue course or something like that just the different namings for the  
**Edvinas Rupkus:** Yeah.  
**Nikita Orobenko:** buttons like access course or you know something like  
**Edvinas Rupkus:** Yep. Yeah. Yeah. We the the tickets that uh Sean right wrote for Claudine in terms of  
**Nikita Orobenko:** That's  
**Edvinas Rupkus:** sponsored courses were pretty thorough and like uh all-encompassing. So hopefully we can review that today with the sign and then we'll schedule a refining call to uh address any you know adjustments that you speak Good, good to hear that there's no like  
**Nikita Orobenko:** okay. Sounds good.  
**Edvinas Rupkus:** major blockers though that would prevent us from getting this  
**Nikita Orobenko:** I mean I don't think there will be any because uh  
**Edvinas Rupkus:** done.  
**Nikita Orobenko:** like it just the free course that should be available without any purchase. I'm more a bit concerned about the profile creation uh just because we don't have that thing uh in the way we want it to be. That's kind of the only thing.  
   
 

### 00:26:00 {#00:26:00}

   
**Nikita Orobenko:** And talking about the demo uh organizations, we talked a bit about that thing with Roma. Right now, it doesn't seems like uh that spending the time on fixing or adjusting the demo access may worth it because ideally we should redefine what is actually the demo access is like how it actually should be working. We never touched it since the original implementation which was done by Brian like a long time ago and a lot of things that already changed since that like the subscriptions came in like a lot of different things and right now I mean like on our side uh it seems like we just kind of  
**Edvinas Rupkus:** Yeah.  
**Nikita Orobenko:** um suddenly forget about it until the next time uh we will have uh a time for it because right now the seems like the payment stuff and the sponsor courses has a higher priority basically. And in terms of the demo access,  
**Edvinas Rupkus:** Correct.  
**Nikita Orobenko:** we still can treat them just using the trial subscriptions. It will grant the full access to the course. Not that uh adjusted one as it was originally in demo ors but still uh kind of the access only for a specific period of the  
   
 

### 00:27:29 {#00:27:29}

   
**Edvinas Rupkus:** Gotcha. Yeah.  
**Nikita Orobenko:** time.  
**Edvinas Rupkus:** uh your assessment is correct and we'll make sure to not forget about this for like the next refinement when we have Matt and somebody else uh from the stakeholders team who can kind of tell us on the on the broader strategy and if like we need that anymore because like we we also removed the demo request uh you know CTA like intake form basically because I feel like we're just slowly moving away from that. It's just all going to be like handholding if anything. So yeah, your assessment is correct and we'll definitely if we need to address it again, I'm sure that stakeholders will  
**Nikita Orobenko:** Yeah,  
**Edvinas Rupkus:** communicate.  
**Nikita Orobenko:** I mean like it it can be a great product feature. So the team organization just can create their own profile or issue  
**Edvinas Rupkus:** Yeah.  
**Nikita Orobenko:** the demo access automatically. they don't need even to connect with us. Uh and boom, they have the access like the demo access, no payments provided, nothing or you know like we can  
   
 

### 00:28:30 {#00:28:30}

   
**Edvinas Rupkus:** Mhm.  
**Nikita Orobenko:** uh I mean like we can adjust it somehow if we need to but it can be a great product feature but I don't think it worth the time right now.  
**Edvinas Rupkus:** Yep. Uh Sean, can we just make sure that we don't forget about this? Like never thought next time we speak to Matt about campus and just it's a thing on our on our in our minds in our back pocket.  
**Sean Winslow:** Yeah, I got you. Thank you, Nikita.  
**Nikola Pivčević:** Uh yeah hello everyone.  
**Sean Winslow:** Nicola.  
**Nikola Pivčević:** So uh on Friday I wrapped up this video content. So it's kind of uh Maria so whenever like you are ready uh to kind of start working on video content on elections hub. Uh so the WordPress part is ready and for the front end I have like a big chunk of it. uh kind of didn't want to like go into too much details of the design but uh I kind of built a wrapper around the existing max player uh component that was you that is used in uh in campus.  
   
 

### 00:29:41 {#00:29:41}

   
**Nikola Pivčević:** Uh so yeah like I think uh yeah whenever you will be ready to work on that. Um, right. And so from yesterday started investigating the uh translating the site into Spanish. So yesterday we bought um kind of the most popular WordPress plug-in for site translations and uh it's kind of like annoyingly it doesn't have a free trial. So we kind of had to bite it immediately. But it's like looking very promising. I think like it's it's very detailed and um uh also has um uh automated translation tools. So it kind of as soon as you publish an article you if you like kind of have like those settings uh it automatically translates and publishes the the article in in a different language which is I guess like the path that we want to take.  
**Edvinas Rupkus:** What what is it? What is it using? Like is it using LLMs or I don't know.  
**Nikola Pivčević:** It's using Yeah, it's using some like they have their own like kind of system for translations but they can they also offer like uh you can um like if you don't want to use their like system you can use DPL I think and then there is like Google translate and uh yeah I don't know like I guess like some other tools yeah that I kind of have they have integrations Good.  
   
 

### 00:31:16 {#00:31:16}

   
**Krystof Oliva:** I feel like also I feel like also some stuff uh like the articles  
**Nikola Pivčević:** Um,  
**Krystof Oliva:** will be I think translated with LM or some stuff but then some things we need to do in right like this manual adding of the translation of the terms isn't  
**Nikola Pivčević:** So,  
**Krystof Oliva:** correct  
**Nikola Pivčević:** so this this plug-in like translates everything uh from the data perspective, right? Like kind of article data, right? Like the data and then yeah,  
**Krystof Oliva:** Yeah.  
**Nikola Pivčević:** like on the front end, we need like some some other um like for the labels for the like kind  
**Krystof Oliva:** Yeah. Yeah.  
**Nikola Pivčević:** of that we  
**Krystof Oliva:** Yeah. I know. Nico, if if you need to help with that.  
**Nikola Pivčević:** have.  
**Krystof Oliva:** Uh like it's kind of manual boring work. So I can do that. It's like internal. Perfect.  
**Nikola Pivčević:** Yeah, I'm kind of I'm currently Yeah.  
**Krystof Oliva:** I I did Yeah,  
**Nikola Pivčević:** Uh, thanks. Yeah.  
**Krystof Oliva:** I did access but if you if you need I can do some of the  
   
 

### 00:32:04

   
**Nikola Pivčević:** Uh, so yeah, I'm currently still like in the phase of investigating.  
**Krystof Oliva:** translations.  
**Nikola Pivčević:** So, uh, no big commitments like I'm just like figuring out like the the the best path forward and like estimate the work and so I'm not doing like I didn't start like with the real integration yet. Um and uh yeah a lot of like questions are like as I'm like investigating like a lot of like details questions arise and um not yeah not trivial task but uh I would say very exciting and I think like with huge potential benefits  
**Krystof Oliva:** Yeah, if if you need to help with the like last part when you have it done, just let me know. Like we did the same thing like not in WordPress but like a TypeScript and JavaScript in Access and I basically did like the translation to Japanese, Chinese, Spanish. It's like boring work but I can do it.  
**Nikola Pivčević:** Yeah. Uh yeah, again I'm hoping like you know um LLMs will help us with like with that work as well. Yeah. And um yeah,  
   
 

### 00:33:09

   
**Sean Winslow:** Yeah,  
**Nikola Pivčević:** that's uh yeah, that's most  
**Sean Winslow:** sweet. Thank you. It's It's called Spike. That's the plug-in name.  
**Edvinas Rupkus:** No, that that's what we use the term that we use to spike it. I don't actually like I use a word, but I don't really know like what it actually means if there's a technical, you know, engineering term for it or explanation for why it's called spike,  
**Sean Winslow:** Got  
**Edvinas Rupkus:** but it's basically just an investigation into a feature or an upgrade or something like that. Yeah.  
**Sean Winslow:** right. Understood. Yeah, I I'll look into that. Uh I'm  
**Nikola Pivčević:** Yeah.  
**Edvinas Rupkus:** Hey,  
**Sean Winslow:** curious.  
**Nikola Pivčević:** And  
**Edvinas Rupkus:** all I know about spikes is like volleyball spikes. spike is how it's would seem like it's like you press a button to to deploy something with a spike,  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** but I  
**Krystof Oliva:** I don't know the bl  
**Nikola Pivčević:** Uh I started like I I started maybe I can link it in inside the ticket.  
   
 

### 00:34:02 {#00:34:02}

   
**Edvinas Rupkus:** regardless  
**Nikola Pivčević:** I started like confluence document like outlining all the like details how this works in the background and like yeah I didn't Yeah,  
**Sean Winslow:** Okay.  
**Nikola Pivčević:** I didn't uh put it I'll put it in. Yeah.  
**Sean Winslow:** Yeah, please do.  
**Nikola Pivčević:** So yeah.  
**Sean Winslow:** Thank you,  
**Edvinas Rupkus:** There's  
**Sean Winslow:** Nicola.  
**Ramuald Vishneuski:** Uh hello uh so mainly I'm working with both Nikita's resolving all issues  
**Sean Winslow:** Promo.  
**Ramuald Vishneuski:** that left and trying to find uh new uh still have to um go through uh many test scenarios and uh also fixing my out test and that's all.  
**Sean Winslow:** Perfect. Yeah, thank you. I' I've been keeping track of all the edits. I very much appreciate it. Thank you, Roma. Ed, got anything?  
**Edvinas Rupkus:** Uh, no. I've been addressing stuff individually with debs. Nothing really want to get the get over with w\*\*\*\*. Um, I know they were being very diligent with it, but it's it's time to say goodbye to NX,  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** too.  
   
 

### 00:35:32 {#00:35:32}

   
**Edvinas Rupkus:** And yeah, that's basically the biggest thing on top of my mind. But yeah, other than that, I'll I'll take care of the election coverage requirement changes any if and if they come our way. So, those tickets are up to date with the latest info.  
**Sean Winslow:** And yeah, my updates. I'm back on the Zap year stuff. So, I've been digging into that, making sure that I'm doing it I'm doing the proper workflow uh so I don't keep on running into issues. And that's basically that's pretty much my updates. So, if anybody has anything that they need help with, just let me know. And yeah, does anybody have anything that they want to talk about before we head out? All right,  
**Bohdan Panasenko:** Uh just one thing uh it's still we still cannot deploy things or we can  
**Sean Winslow:** cool.  
**Bohdan Panasenko:** already uh that's from from that message from Mike.  
**Mike Price:** Yeah, we can.  
**Bohdan Panasenko:** Okay.  
**Mike Price:** They came back up. Uh, we're good. Yeah, we're all good. Uh, we will be shifting soon uh to something more resilient. Oh, on paper more resilient, but that's for a later time. So, we're all good. Business is usable.  
**Bohdan Panasenko:** Okay.  
   
 

### Transcription ended after 00:37:20

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*