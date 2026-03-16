---
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup - 2026_02_26 06_55 pst - notes by gemini.
context: the-block
created: 2026-03-16
source: granola-manual
---

# 📝 Notes

Feb 26, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivčević](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Bohdan Panasenko](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~ ~~[Koray Baspinar](mailto:kbaspinar@theblock.co)~~ ~~[Krystof Oliva](mailto:koliva@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMjZUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.cxt5j56ycjl5) 

### Summary

**Poly Market Widget Prioritization**  
The team prioritized 19 Poly Market widget tickets, focusing on moving higher-priority items through the bottleneck. Engineers confirmed they are not aiming for a direct copy of Poly Market's UX but must resolve current ordering logic issues to ensure functionality.

**Individual Development Progress Updates**  
Multiple team members reported progress on key areas, including finishing ETF price migration, resolving display name update bugs, and nearing completion of year redirects using Redis. Other updates included fixing frontend bugs for the multi-course release and addressing unused events being emitted on every page.

**AI Tooling and Cost Investigation**  
Mike Price detailed the functionality of Simon AI, an internal tool augmenting ChatGPT with a vector database of WordPress articles to enhance crypto knowledge. The team agreed to investigate open-source models like Quen Coder 3.5 as potential cost-saving alternatives for the AI tool stack

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

## NEEDS FURTHER DISCUSSION

* **Poly Market Widget Sorting Logic** The correct Poly Market widget ordering logic requires external investigation by Edvinas, as current sorting attempts fail to accurately represent the market order 30% of the time.

* **Simon AI Open Source AI Investigation** Investigation into using open-source AI models, such as Quen Coder 3.5, for the Simon AI backend is needed to explore cost-saving opportunities.

*More details:*

* **Poly Market Widget Prioritization**: The team has 19 tickets related to Poly Market widgets and is prioritizing their release, with the higher priority items being focused on getting through the bottleneck ([00:00:00](#00:00:00)). Edvinas Rupkus noted they will review Marina's comments regarding the ordering logic, as they do not aim for a one-to-one copy of Poly Market's UX but need to ensure widgets do not appear broken due to ordering issues ([00:09:26](#00:09:26)).

* **Individual Development Updates (Aliaksandr Kryvanosau)**: Aliaksandr Kryvanosau has been working on redesigning the reach-out model and investigating a scrolling issue on the individual job page, which they have successfully reproduced locally and hope to finish soon. The issue was discovered to be content-related, and they are making good progress on a fix ([00:00:00](#00:00:00)).

* **Individual Development Updates (Ana Benitez)**: Ana Benitez reported that the migration for prices on ETF pages is ready, and they are working through comments on prices and stock pages with Maria, checking if the remaining issues are deployment-related or actual bugs. Addressing these issues will be their priority for the day ([00:01:45](#00:01:45)).

* **Individual Development Updates (Bohdan Panasenko)**: Bohdan Panasenko returned to address a bug related to updating a user's display name, where a previously implemented solution was not accepted, requiring them to rework a prior solution to make it functional ([00:01:45](#00:01:45)). Bohdan Panasenko is currently working on making the previous solution work ([00:03:00](#00:03:00)).

* **Individual Development Updates (Brian Mendoza)**: Brian Mendoza deployed the access-related work and plans to address a comment about it not working, suspecting the user might be on a Nux 2 page or have a conflicting tab open. They will also work on some analytics issues identified by Ed, where six to eight extra, unused events are being emitted on every page due to the migration to GAM, which may be contributing to the big query bill limit ([00:03:00](#00:03:00)).

* **Individual Development Updates (Cesar Paz)**: Cesar Paz is close to finishing the year redirects by implementing a new key in Redis to ensure redirection occurs through Redis and HAProxy rather than directly through WordPress. They are conducting final tests and anticipate creating a pull request today, and they also created a new task to automate sending PDF invoices to Google Drive based on a request from Matt and Vicki ([00:04:09](#00:04:09)).

* **Individual Development Updates (Krystof Oliva)**: Krystof Oliva is setting up their Claude code in preparation for a meeting with Mike, aiming to switch from or improve their use of Cursor to utilize the capabilities of the new coding technology more efficiently. They have been practicing basic commands, looking into a repository Mike provided, and hope to soon have "five agents running" while coding for the blog ([00:05:36](#00:05:36)).

* **Individual Development Updates (Maryia Zhynko)**: Maryia Zhynko completed a few fixes for the prices and stock pages mentioned by Anna and is continuing to work on report cards ([00:07:36](#00:07:36)).

* **Individual Development Updates (Marina Lozuk)**: Marina Lozuk is proceeding with the Poly Market work, focusing on ordering the market for specific events and implementing those blocks on the election page. They tried various ways to sort the markets but found no logic that would consistently reproduce the exact behavior seen on Poly Market, noting that even Poly Market displays different orders for the same widget across different locations ([00:07:36](#00:07:36)).

* **Poly Market Sorting Logic Investigation**: Marina Lozuk found that using a \`group item threshold\` property seemed to satisfy the ordering for about 70% of events but resulted in a different order for the remaining 30% ([00:09:26](#00:09:26)). Edvinas Rupkus agreed to investigate the sorting problem further, noting that when trying to sort by outcome, they encountered "bizarre ordering" where low-percentage markets would jump to the top, suggesting Poly Market is using additional logic ([00:10:40](#00:10:40)).

* **Individual Development Updates (Mike Price)**: Mike Price released an update for the iOS app and successfully implemented AI summaries in the digest after several iterations. They also collaborated with Matt on the data engine charting, connecting it to the Black-Co API for testing by the research team. Mike Price is working on connecting the iOS app to Campus for authorization and finalizing internal hookups for the Simon AI API for Jordan and their team's automation workflows ([00:11:57](#00:11:57)).

* **Simon AI Description and Use Case**: Mike Price explained that Simon AI is an internal tool augmenting ChatGPT with a vector database RAG system, where WordPress articles are vectorized and stored in Weaviate. This system ties the vector database to ChatGPT, running embeddings to provide a custom-baked flavor of OpenAI, essentially feeding the model articles to enhance its knowledge of the crypto space ([00:13:14](#00:13:14)).

* **Cost-Saving Alternatives for AI**: Sean Winslow raised the idea of potentially using open-source models like Quen Coder 3.5 to save on costs associated with Simon AI, as new, free models are frequently being released that might be capable alternatives. Sean Winslow committed to looking into the open-source options and sending links to Mike Price ([00:14:12](#00:14:12)).

* **Individual Development Updates (Mikita Hulis)**: Mikita Hulis reported that all frontend points from Roma are closed, with deployment to development expected today or tomorrow ([00:14:12](#00:14:12)). They are addressing backend issues with Roma and are nearing the end of QA for the multi-course release. Two adjustment tickets will likely be addressed early next week before proceeding with planning and implementing the payment flow ([00:15:22](#00:15:22)).

* **Individual Development Updates (Nikita Orobenko and Ramuald Vishneuski)**: Nikita Orobenko and Ramuald Vishneuski are primarily focused on fixing Campus bugs related to the multi-course release ([00:15:22](#00:15:22)). Ramuald Vishneuski is continuing to find frontend bugs for Nikita Hulis to address ([00:16:51](#00:16:51)).

* **Individual Development Updates (Nicola)**: Nicola skipped the stand-up but is working on site translation and has started writing proof of concept code for WordPress translation. They were also assisting Edvinas Rupkus with LMAX code and API issues ([00:16:51](#00:16:51)).

* **Final Commitments and Next Steps (Sean Winslow)**: Sean Winslow will send the rise-related materials to Nikita Hulis immediately following the meeting and will send links regarding open-source AI alternatives to Mike Price . Sean Winslow is also planning to work on the design ticket that they had overlooked .

### Suggested next steps

- [ ] Cesar Paz will finalize checks and hopefully create the pull request today for the yours redirects.

- [ ] Mike Price will finish hooking up the last bit of internals for S Simon API by tomorrow for Jordan and his team to integrate into their automation workflows.

- [ ] Brian Mendoza will figure out the issue with the deployed access stuff not working, work on the analytics items Ed found, and get the in-article items into testing.

- [ ] Cesar Paz will create a new task to automatically send invoices by PDF from Gmail to Google Drive using a Google script.

- [ ] Edvinas Rupkus will read Marina Lozuk's comment about the Poly Market ordering issue and try to synthesize the problem to communicate to them.

- [ ] Sean Winslow will look into open-source LLM options like Quen Coder to potentially save on cost for Simon AI and send links to Mike Price.

- [ ] Mikita Hulis will get the rise stuff from Sean Winslow right after this meeting.

- [ ] Sean Winslow will work on the design ticket that was overlooked.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=ieqaACCAolQvIRYSiWPtDxIWOAIIigIgABgDCA&detailid=standard)*

# 📖 Transcript

Feb 26, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Sean Winslow:** Okay. Yeah, makes  
**Edvinas Rupkus:** So yeah,  
**Sean Winslow:** sense.  
**Edvinas Rupkus:** to answer your question, Kristoff, um there's like 19 tickets in there already. We want to make sure that the Poly Market widgets uh go out relatively soon. Uh but yeah, after that, it's just basically prioritization. So the higher the priority, the more emphasis we put on getting that stuff out through the bottleneck.  
**Krystof Oliva:** Okay, thank you. Thank you.  
**Sean Winslow:** Cool. Yeah. So, uh, so yeah. So, for Anna and Roma, I'll just uncclick everybody. You're right. Usually, their boards are This is literally their whole board. So,  
**Edvinas Rupkus:** Yeah, exactly.  
**Sean Winslow:** all right, cool. Yeah, we'll start with Alex.  
**Aliaksandr Kryvanosau:** Hello. So for me uh jobs as usual I've been working on the redesign for reach out model and then I've been looking into the issue with uh scrolling to section on individuals u p job jobs page. Uh so far I was only been able to reproduce it on devbox but then before the meeting I was able to notice that it is content related issue and I'm able to reproduce it locally.  
   
 

### 00:01:45 {#00:01:45}

   
**Aliaksandr Kryvanosau:** So it's in good progress and I hope to finish it soon. That's it.  
**Sean Winslow:** Perfect. Thank you, Alex. Anna.  
**Ana Benitez:** Um hello. So regarding migration for prices, uh ETF pages are ready. Uh and prices and stock pages, uh I still have some comments I shared with Maria and uh well, we're making sure if that is a deposs issue or an actual issue. Uh so we'll keep you posted on that part. Yes. So we that will be the priority for today and that's all.  
**Sean Winslow:** Perfect. Thank you. Ready for your flight? No issues.  
**Ana Benitez:** Yeah. No. Thank you.  
**Sean Winslow:** Thank you, Anna. Well done.  
**Bohdan Panasenko:** Hello there. Uh so yeah, I kind of as I said I had to come back to the ticket for uh bug when updating user display name. I made a solution. Uh Nicola didn't like it and he said we should make a previous solution like make it work and it's a little bit pain in the ass but I'm working on it.  
   
 

### 00:03:00 {#00:03:00}

   
**Bohdan Panasenko:** I'm trying. Yeah.  
**Sean Winslow:** I appreciate that. Yeah. Yeah. Thank Thank you, Bon Brian.  
**Brian Mendoza:** Uh yesterday I deployed the access stuff. I see a comment about it not working. I'm like almost certain he is on a Nux 2 page or just has some weird tab open in a separate window. We'll figure that out.  
**Sean Winslow:** Uh,  
**Brian Mendoza:** But other than that, I'm going to work on some analytics stuff that Ed found yesterday and get this in article stuff in testing.  
**Sean Winslow:** what was the analytic  
**Brian Mendoza:** Uh we have so when we migrated to GAM um we forgot we didn't forget we just  
**Sean Winslow:** stuff?  
**Brian Mendoza:** decided not to unwire the events that get emitted from the ads. So we have a like for every page there's like six to eight extra events that we're not using and I think that's why we're hitting our big query bill or whatever or a limit because every single navigation has six to eight events that we're not using because we're just using the gamma events the native ones.  
   
 

### 00:04:09 {#00:04:09}

   
**Sean Winslow:** Gotcha. Okay, sweet. Thank you, Brian.  
**Cesar Paz:** Uh hi. Well,  
**Sean Winslow:** Caesar  
**Cesar Paz:** I almost finished the yours redirects. Uh basically, I created a new uh key in radius. Now, yeah, I'm doing some test in a box to check if the redirection is done uh through radius and ha proxy instead of WordPress directly. Uh I believe it's done but I I I'm doing some more checks and I hope um doing the pull request today. I'm going to send this pull request to my because there are several chains. Um in addition I've created a new task to send invoices to Google Drive automatically. Um this is a request from Matt and Vicki. Uh it's basically to yeah to to filter uh our Gmail account to get the invoices to send and use a Google script in order to send these invoices uh by PDF to Google Drive. So this is the the functionality and yeah that's all solving  
**Sean Winslow:** Cool.  
**Cesar Paz:** a small fixes small book and that's all.  
   
 

### 00:05:36 {#00:05:36}

   
**Sean Winslow:** All right. Thank you,  
**Cesar Paz:** Thank you.  
**Sean Winslow:** Caesar. Corey. All right.  
**Edvinas Rupkus:** My core is out today, I  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** think.  
**Sean Winslow:** Kristoff.  
**Krystof Oliva:** So hi everyone. I have pants today as well. Uh I have been working on setting up my cloth code. So I have a meeting tomorrow with Mike uh regarding that. Uh so I need to prepare for it. Uh I've been using the cursor for now and he wants me to switch or kind of improve it in this in this case. So so I've been doing a bit of like this work kind of to prepare for the harder task and be able to do them more efficiently with AI and and it's it's going good so far. like I have learned the basic commands and he sent me a repo. I think he also sent it to like the general chat um that I will look to and kind of try to use the superpowers of quote and then tomorrow I have the meeting with him.  
   
 

### 00:06:40

   
**Sean Winslow:** Yeah.  
**Krystof Oliva:** So probably soon I will have five agents running while I'm in my class, you know, and coding for the blog. So that's it.  
**Sean Winslow:** Hell  
**Krystof Oliva:** Yeah. And then like once I do it,  
**Sean Winslow:** yeah.  
**Krystof Oliva:** I finally will finish the the task which I wanted to finish. But I just focus on this because Mike made the time for me tomorrow. So I wanted to like prepare for it.  
**Sean Winslow:** No, I get it. When I first started like learning about this stuff, I couldn't help but just like try to dive in deeper and try to figure out what else it's capable of. So, I I  
**Krystof Oliva:** Yeah,  
**Sean Winslow:** understand.  
**Krystof Oliva:** I think us as like informatives were quite lazy in this sense. So we try to automate everything, you know. So  
**Sean Winslow:** Yeah. Well,  
**Krystof Oliva:** yeah.  
**Sean Winslow:** it's it's trying to, you know, simplify your workload, but also it's just fascinating that this is even possible. So, you're like, "All right, well, let's see what else it can do." Thank you,  
   
 

### 00:07:36 {#00:07:36}

   
**Krystof Oliva:** Yeah. Yeah.  
**Sean Winslow:** Kristoff.  
**Maryia Zhynko:** Yep.  
**Sean Winslow:** Maria.  
**Maryia Zhynko:** Today I did a couple of uh fixes for prices and stock pages that Anna mentioned and continued working on report cards.  
**Sean Winslow:** Awesome. Cool. Thank you, Maria. Marina  
**Marina Lozuk:** Hello. As for me, I proceed working on the poly market stuff and mostly on the ordering the market for specific event that we discussed with the yesterday and also looked at at the um election page and implementation of those blocks as well. That's it.  
**Edvinas Rupkus:** Did you have any success in the I saw you make the comment for it was a long comment.  
**Marina Lozuk:** Uh yes uh I  
**Edvinas Rupkus:** I haven't  
**Marina Lozuk:** tried different ways so I believe that now I'm waiting for your input what is  
**Edvinas Rupkus:** mar  
**Marina Lozuk:** the most appropriate way of doing that because none of them will reproduce like same behavior as we have on the poly market because I compared like on different events sometimes will like fit what we have on the poly market sometimes it doesn't fit and I couldn't find the logic uh like 100% which will 100% work and to capital for one of the market which is shared with something with iron like war or something like that uh uh on the poly market I found three places of using these uh widget right and the order was different even on the poly market on every single widget.  
   
 

### 00:09:26 {#00:09:26}

   
**Marina Lozuk:** So that's why I don't know exactly the right way of sorting. So I uh believe that uh there is a um there is a parameter uh let me have a look how it's called group item threshold and this u this property may be the most applicable and when I use it like uh the maybe 70% of events would u would satisfy what we have and the poly market stuff, right? But anyway, 30% would have different anyway different  
**Edvinas Rupkus:** Okay.  
**Marina Lozuk:** order.  
**Edvinas Rupkus:** Uh, thanks for looking into it. I'll I'll read through your comment and I'll try to synthesize the problem and communicate to them if there is a problem.  
**Marina Lozuk:** Yeah. Yeah.  
**Edvinas Rupkus:** We don't need we don't want to like copy one to one the the UX from poly market. But we just wanted to make sure that it it's it makes sense for their but yeah if if 30% of the time we have like 0.0% 0% markets or outcomes showing up on those widgets, then it sort of like loses the point. It's like it almost looks like the the widget itself is broken.  
   
 

### 00:10:40 {#00:10:40}

   
**Edvinas Rupkus:** So, uh yeah, I'll take a look and yeah,  
**Marina Lozuk:** uh and uh one thing to mention so when I try to sort them by the  
**Edvinas Rupkus:** I'll  
**Marina Lozuk:** outcome right there is like yes percentage from highest to the lowest  
**Edvinas Rupkus:** Mhm.  
**Marina Lozuk:** for some widget I got some bizarre ordering for instance I've got some market which on the poly on the poly market at the very end but they will go to the very top because they kind of reproduce 50% you know and there are like the the question would be persona A persona B persona C instead of like uh the name of other people. So in poly market we would have kind of real people right but with lower percentage of outcome at the top but when I try to order them by this outcome these kind of odd stuff will go up which I would never find in poly market like I need to scroll a lot to read Um  
**Edvinas Rupkus:** Yeah, they must be doing something else on their site. Um, additionally,  
**Marina Lozuk:** yeah.  
**Edvinas Rupkus:** okay, we'll investigate.  
   
 

### 00:11:57 {#00:11:57}

   
**Edvinas Rupkus:** Thanks, Marina.  
**Sean Winslow:** Thank you, Marina. Mike.  
**Mike Price:** Uh did some work on the iOS app. Did another release. Um got the AI summaries in the digest actually finally working with a few iterations. Uh so check out the latest iOS approve. Um and then I did uh did some work with Matt on the uh data engine charting adding hooking it up to the DP the the black co API for charting. Uh, so allow the research team test that out, see how it looks, and then, uh, I've been working on the rest of the pro API functionality and getting the iOS app  
**Sean Winslow:** Nice.  
**Mike Price:** hooked up to campus for authorization uh, for the last, uh, last major feature for iOS app. So, um that and then um getting the last bit of internals for S Simon API hooked up uh for Jordan and his team to uh integrate into their automation workflows. So, I should have that by tomorrow. So, that's it.  
**Sean Winslow:** Thank you, Mike.  
**Mike Price:** Thank you,  
**Sean Winslow:** Yeah,  
   
 

### 00:13:14 {#00:13:14}

   
**Mike Price:** Mike.  
**Sean Winslow:** I was talking to Jordan about why he wanted Simon AI in the first place,  
**Mike Price:** Yeah.  
**Sean Winslow:** and it's a pretty interesting use case. So,  
**Mike Price:** Yeah. Yeah, that's pretty cool.  
**Sean Winslow:** yeah, thank you,  
**Krystof Oliva:** What? What does this sound?  
**Mike Price:** Yeah,  
**Sean Winslow:** Mike.  
**Krystof Oliva:** Let me  
**Mike Price:** it's our own internal it's uh we just augmented uh chat GPT with a vector  
**Krystof Oliva:** ask.  
**Mike Price:** database uh rack system. uh you you know you know what rag is of course. So yeah, we have a vector DB and Weev8. All of our WordPress articles get vectorized and and sent over to Weev8 and then we can uh basically just we just tie the two together and then uh run run run the embeddings against the vector DV and send it over to Chat GBT and then come back with our own uh kind of custom baked uh flavor of open AI.  
**Krystof Oliva:** Yeah. Yeah. So it's basically like we feed the GGPDFR steroids analytics articles and then it knows more about the crypto space,  
   
 

### 00:14:12 {#00:14:12}

   
**Mike Price:** Exactly.  
**Krystof Oliva:** right?  
**Mike Price:** Exactly.  
**Krystof Oliva:** We did the similar thing  
**Mike Price:** Yeah.  
**Sean Winslow:** Yeah. To save on cost,  
**Mike Price:** Nice.  
**Sean Winslow:** have you guys uh thought well I know pro hasn't well Simon AI hasn't really been used as much but to save on cost have you guys thought about using like open source like Quen Coder like the new one 3.5 I think it is.  
**Mike Price:** Uh maybe I don't know. No, we haven't considered it, but open to possibilities of  
**Sean Winslow:** Yeah, I I I'll look into that because every day I hear something new is coming out that's like blowing everything out  
**Mike Price:** course.  
**Sean Winslow:** the water and if it's free and we have the data space for it or the uh Yeah, I I'll look into it.  
**Mike Price:** Cool. Thanks. Yeah,  
**Sean Winslow:** Yeah.  
**Mike Price:** send me some links.  
**Sean Winslow:** Nice, Nikita.  
**Mikita Hulis:** Yes sir. So some good news uh I'd say uh front end wise all apart of one points uh from Roma are closed and either today or tomorrow would be deployed to deployed to dev.  
   
 

### 00:15:22 {#00:15:22}

   
**Mikita Hulis:** I think there was only one uh tiny leftover otherwise it seems as though uh most of it is covered. uh some things from the back end also required my attention so we'll address them uh together with uh oh uh I want to help him out to uh close out a few points left over there um yeah otherwise we have approaching the the end of uh QA4 for the multicourses release of course there are uh two uh adjustments tickets which I've mentioned yesterday which we'd also like to address uh likely likely on like Monday, Tuesday, something like this. Uh yeah and otherwise uh we would be able to proceed to uh planning and continuing implementing uh  
**Sean Winslow:** Awesome.  
**Mikita Hulis:** the payment flow and later on of course uh the things discussed on the prior meeting as well. Uh, and I think that's about it.  
**Sean Winslow:** Thank you, Nikita. Yeah, I'll get over the Yeah, like we discussed, I'll get the rise stuff over to you as like right after this meeting. So,  
**Mikita Hulis:** Lovely.  
**Sean Winslow:** Nikita O.  
   
 

### 00:16:51 {#00:16:51}

   
**Nikita Orobenko:** barely have anything to add uh thanks to the detailed explanation of the uh previous speaker. Uh yeah, so we're working mostly on the campus bugs uh related to the multicourse release. Uh I think that that's mostly it for now.  
**Sean Winslow:** Yeah. No, that's good. Yeah. Knock those bad boys out. I very much appreciate it, Nicola.  
**Edvinas Rupkus:** Nicole is skipping stand up today. Uh he told me that he is uh one second. He is working on the site translation and started writing some proof of concept code for WordPress in terms of that. But he was also helping me with the uh LMAX code and API issues that they were having.  
**Sean Winslow:** Sweet. Thank you, Nicola and Ed Roma.  
**Ramuald Vishneuski:** Uh hello team. So uh we continue working on campus trying to find more uh front bugs because Nikita uh should fix uh uh he he is  
**Sean Winslow:** Cool.  
**Ramuald Vishneuski:** uh near the end for so want to find some for him. Um, and that's most  
**Sean Winslow:** Thank you, Roma. Ed,  
**Edvinas Rupkus:** No,  
**Sean Winslow:** anything.  
**Edvinas Rupkus:** nothing specific. Uh, reply to Marina today about P market. That's not to mind to get those widgets out.  
**Sean Winslow:** Cool. Yeah. And on my end, still Zapier, but after today's meeting's going to get the rise stuff over to Nikita and Nikita and I will Mike, I'll send you some links of what I find about some of the open source stuff. And I believe that's it. unless I'm missing something. And I'm going to work on the the design um ticket that yeah was overlooked on my end. So, I apologize about that. But yeah, that's it. Anybody else have anything that they want to discuss? All right, enjoy your Fridays and your weekends everybody. I'll talk to you guys later.  
**Ana Benitez:** Thank you. Bye.  
   
 

### Transcription ended after 00:19:55

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*