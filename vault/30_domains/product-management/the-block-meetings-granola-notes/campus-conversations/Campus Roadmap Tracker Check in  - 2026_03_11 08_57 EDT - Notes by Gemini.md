# 📝 Notes

Mar 11, 2026

## Campus Roadmap Tracker Check in 

Invited [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Ramuald Vishneuski](mailto:rvishneuski@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co)

Attachments [Campus Roadmap Tracker Check in ](https://www.google.com/calendar/event?eid=MzRuM2xqYmJrcTR0ZDV1cGUwMWc5MjJvbGYgc3dpbnNsb3dAdGhlYmxvY2suY28) 

Meeting records [Transcript](?tab=t.mfpfw56se4u) 

### Summary

Alignment meeting focused on ongoing QA adjustments, bug prioritization, and estimated release timelines with progress reporting clarification.

**Address Ongoing QA Challenges**  
Continuous Quality Assurance adjustments and bugs from a previous implementation are a major challenge, requiring developers to switch constantly between new work and old fixes. The team decided that future releases must allocate dedicated time for both development and a formal QA process.

**Prioritizing Email Field Addition**  
A key decision was made to set the email field addition to the hiring feature tables as a double high priority for the next big release to enhance user experience. The team agreed only to implement this small part, not the entire larger update tied to ticket 405340\.

**Individual Access Release Timeline**  
The target release window for the individual access and payment flow is mid to late April, based on an estimated 3 weeks of development and 1.5 to 2 weeks of QA time. Back-end account management is 70% to 80% complete, while the front-end checkout flow is roughly 65% done.

### Details

* **Participant Wellness and Meeting Objective**: The meeting began with a check-in on Nikita Orobenko's recovery from surgery, noting that they are nearly two months post-operation and progressing well with the rehabilitation process ([00:00:00](#00:00:00)). Sean Winslow then stated that the primary objective of the meeting was to align everyone on current progress, identify any blockers, and determine development priorities, aiming to document this information for all team members ([00:01:39](#00:01:39)).

* **Current Blockers and QA Process**: Mikita Hulis highlighted that a major ongoing challenge is the continuous list of quality assurance (QA) adjustments and bugs stemming from the previous implementation, requiring them to constantly switch between new development and old fixes. They suggested that the current state signifies a need to allocate adequate time for both development and a dedicated QA process for future releases ([00:02:45](#00:02:45)).

* **Bug Prioritization and Definition**: The team discussed the nature of the remaining bugs, noting that there are currently no critical, unpostponable bugs, though a prior ticket (4064) contained approximately 50 adjustments ([00:04:30](#00:04:30)). Mikita Hulis suggested that many of these issues are not true bugs but rather changes stemming from evolving requirements due to a rushed process during the previous release. Edvinas Rupkus advised the team to specifically ping them if there is confusion about prioritizing a bug over a future implementation ([00:05:49](#00:05:49)).

* **Multicourse Status and Bug Tracking**: Ramuald Vishneuski confirmed that there are no critical bugs concerning multicourses, noting that the most significant issue, involving certificates, was recently resolved ([00:07:11](#00:07:11)). They indicated that minor to medium issues remain on the front and back end, some of which are ready for deployment, while others will be addressed later, and they will create separate tickets for them. Ramuald Vishneuski also shared a link with Sean Winslow to the main list of all existing campus bugs ([00:08:19](#00:08:19)).

* **Prioritizing Email Field Addition**: Ramuald Vishneuski proposed prioritizing the addition of an email field to the tables on the "my team" and "my candidates" pages, a feature that was previously initiated but never finished ([00:09:55](#00:09:55)). They view this as a crucial enhancement to significantly improve the user experience for the hiring feature ([00:14:25](#00:14:25)). Nikita Orobenko indicated that adding just the email field is feasible, though the back-end side of the overall feature requires significant work and might be easier to rebuild from scratch ([00:11:39](#00:11:39)).

* **Email Field Implementation and Ticket Identification**: Ramuald Vishneuski confirmed that the plan is only to implement the small part of adding the email field, not the entire "my team" and "my candidates" update ([00:14:25](#00:14:25)). The relevant ticket for the larger update was identified as 405340 ([00:12:58](#00:12:58)). Edvinas Rupkus requested that this item be marked as a double high priority for the next big release ([00:14:25](#00:14:25)).

* **Progress on Next Big Release Components**: The next major release focuses on individual access and payment flows, with the course already live ([00:14:25](#00:14:25)). Nikita Orobenko reported that back-end account management is estimated to be 70% to 80% complete, after which they will proceed with upsells and other payment-related tasks, which may require adjustments to existing revived functionality ([00:15:44](#00:15:44)). On the front-end side, Mikita Hulis estimates the individual checkout flow is roughly 65% done, while the user management feature is at 0% but does not constitute a huge amount of work ([00:18:12](#00:18:12)).

* **Design Updates and Completion Estimates**: Claudine Daumur confirmed the completion of the login flow design and the tablet and mobile versions. Their remaining work involves the completion state at the end of the course, and they estimate having about one week of work left on campus ([00:19:44](#00:19:44)). Claudine Daumur also notified the team that they would be out of the office the following week and planned to finalize all work before then ([00:21:20](#00:21:20)).

* **Timeline for Individual Access and Payment Flow Release**: The team discussed the deadline for the individual access release, confirming there are no strict external deadlines, but there is an outstanding commitment to Poly Market for a sponsored course following the individual release ([00:22:53](#00:22:53)). Mikita Hulis proposed a proper timeline of about three weeks of pure development time followed by one and a half to two weeks of QA time, totaling five weeks ([00:25:16](#00:25:16)). This timeline suggests a target release window of mid to late April ([00:26:41](#00:26:41)).

* **Mitigating Risks and Setting Priorities**: Nikita Orobenko highlighted the risk that the sponsored course commitment could interfere with the established deadline for the payment flow, which is a higher current priority ([00:30:18](#00:30:18)). In case of necessary changes, they stated that the original purchase flow should be prioritized, the upgrades are optional, and the basic parts of the sponsored course (like the new dashboard section) could be implemented, potentially cutting off the upsells functionality ([00:32:52](#00:32:52)). Edvinas Rupkus committed to keeping the team informed about any deadlines or changes from the sponsor ([00:34:36](#00:34:36)).

* **Importance of Content for Testing**: Nikita Orobenko stressed that the availability of content is a critical factor and a potential blocker for testing, as having the content is necessary to test the dashboard and other parts of the system fully ([00:35:51](#00:35:51)). Sean Winslow confirmed that they would speak with David to ensure the course content is ready soon ([00:36:59](#00:36:59)).

* **Handling Bugs in Existing Courses**: Ramuald Vishneuski inquired about the process for addressing bugs in the existing course "Digital Essentials 2001," which contains several small issues ([00:36:59](#00:36:59)). Sean Winslow advised that Ramuald Vishneuski should create a ticket for the issues, which they will then forward to David, who is responsible for the course content ([00:38:39](#00:38:39)). The team also confirmed that when a course file is updated, it involves deleting the old file and uploading a new one to the S3 bucket, which takes about five to ten minutes, but this action does not affect the users' progress ([00:39:54](#00:39:54)).

* **Finalizing Progress Reporting for Management**: Mikita Hulis reviewed the meeting notes and requested several adjustments to ensure accurate reporting to higher-ups, including separating "user account management" into its own item with a 45% total progress assigned to both Nikita Orobenko and themself ([00:42:40](#00:42:40)). They also suggested clarifying that the mid to late April deadline is a "common denominator" for the conjunction of the self-service flow, account management, and upgrades, not for a single feature ([00:44:25](#00:44:25)). Sean Winslow acknowledged the importance of these adjustments for cleaning up the reporting ([00:45:40](#00:45:40)).

### Suggested next steps

- [ ] \[Ramuald Vishneuski\] Create Tickets: Create separate tickets for existing minor/medium multi-course issues. Plan to fix these issues during general bug fixing stage.

- [ ] \[Ramuald Vishneuski\] Create Bug Tickets: Create individual tickets for bugs listed in comments of the multi-course main ticket. Move the main ticket to the done section.

- [ ] \[Ramuald Vishneuski\] Review Bug List: Review the main list of campus bugs. Determine which issues require fixing during the new payment flow development.

- [ ] \[Ramuald Vishneuski\] Prioritize Feature: Mark the upgrade ticket 405340 for adding the email field to My Team and My Candidates pages as double high priority.

- [ ] \[Sean Winslow\] Assign Design Tickets: Assign the recently created design tickets for the account management flow to Nikita Orobenko and Mikita Hulis.

- [ ] \[Claudine Daumur\] Share Login Design: Share the finalized login flow design with Sean Winslow and Edvinas Rupkus.

- [ ] \[Claudine Daumur\] Finalize Design: Finish working on the completion state design at the end of the course.

- [ ] \[Edvinas Rupkus\] Update Deadlines: Keep the team posted immediately upon learning new information regarding Poly Market delivery deadlines.

- [ ] \[Sean Winslow\] Confirm Content Status: Speak with David tomorrow to confirm the content status for the sponsored course. Update the team immediately afterwards.

- [ ] \[Ramuald Vishneuski\] Report Course Bugs: Create a ticket documenting the buggy behavior found in the Digital Essentials 2001 course. Forward the ticket information to Sean Winslow for review by David.

- [ ] \[Sean Winslow\] Update Tracking Notes: Separate User Account Management from Self-Service Flow in the shared notes. Assign the task to both Nikitas and set the overall progress to 45%.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=kWbVQ5okf0Yd08Hc6burDxITOAIIigIgABgBCA&detailid=standard)*

# 📖 Transcript

Mar 11, 2026

## Campus Roadmap Tracker Check in  \- Transcript

### 00:00:00 {#00:00:00}

   
**Edvinas Rupkus:** Good morning. Morning.  
**Nikita Orobenko:** Hey guys,  
**Sean Winslow:** And again,  
**Nikita Orobenko:** how's it going?  
**Sean Winslow:** I'm doing well, man. H I keep on forgetting. How How's your arm doing?  
**Nikita Orobenko:** Uh, kind of perfectly fine already.  
**Sean Winslow:** Yeah.  
**Nikita Orobenko:** I mean like it's it's already like two months post up  
**Sean Winslow:** Yeah.  
**Nikita Orobenko:** so everything is quite good already.  
**Sean Winslow:** Cool. Good.  
**Mikita Hulis:** Hey. Hey  
**Sean Winslow:** Is that Nikita?  
**Edvinas Rupkus:** It's it's it's already been two months since your since your  
**Mikita Hulis:** guys.  
**Edvinas Rupkus:** surgery.  
**Nikita Orobenko:** Yeah. Yeah. Like already like close to two months I I suppose.  
**Edvinas Rupkus:** Jeez,  
**Nikita Orobenko:** So I mean like the most just the rehabilitation  
**Edvinas Rupkus:** I was actually fine.  
**Nikita Orobenko:** process in the gym. So that's the most important one.  
**Sean Winslow:** Did you get any fun drugs for it? Did you get any fun drugs for  
**Nikita Orobenko:** H uh no  
**Sean Winslow:** it?  
**Nikita Orobenko:** like I mean like in in the post Soviet countries we don't they don't use the opioids like barely unless you are in the in the hospice care like paleative care so you just won't get them.  
   
 

### 00:01:39 {#00:01:39}

   
**Nikita Orobenko:** Uh, but there are like the the the pain meds that are being sold without the prescriptions, but they're still quite good. But I just used them like maybe for two days or three after the the the operation, so it was not that bad.  
**Sean Winslow:** Yeah, just pretty much help you sleep,  
**Nikita Orobenko:** Hopefully.  
**Sean Winslow:** get through the night. I think that's what I would do.  
**Ramuald Vishneuski:** Hello.  
**Nikita Orobenko:** Yeah.  
**Sean Winslow:** All right, so it looks like we have the whole crew here. Uh so basically we just wanted to get an idea get everyone together to get an idea of where everyone's at. I know we've been uh doing the daily stands up and daily standups and I've been taking notes uh what you guys have been updating us on. But I just want to get everything sort of written down just so we're like everyone's aligned, everyone who has access to this and then try to find out if we have any blockers or like what's a like and what we'll discuss what a priority is like you know what percentage of completion we're at.  
   
 

### 00:02:45 {#00:02:45}

   
**Sean Winslow:** So So yeah. So Ed, do you have anything to add you want to discuss?  
**Edvinas Rupkus:** Uh no, no. Yeah. And if there are specific questions, so something that's unclear, uh we can maybe spend a few minutes like quickly not refining it, but just talking about like what's expected, what's what should be included in the, you know, for future releases. Uh and go ahead  
**Mikita Hulis:** as well as as for the bloggers the unending list of QA adjustments to previous implementation I would say because I'm I myself am sort of getting tired of like giving an update each day of like Hey, by the way, I I'm planning to do this stuff, but I've received another pack of uh wonders from Roma. And so I do that and then I plan to return to like the imp like it's sort of jumping back and forth uh with the bugs from the previous uh release or adjustments at this point, I should say. Uh and yeah and jumping back to the to the payment implementation which is sort of a pain but I I think this signifies actually that well on the previous release we were constrained by the sponsorships and like the do's eye situation but in general this signifies that we should give like proper time for development and proper time for the QA process as well which is Yeah, it's I'm sort of sounding like a like a broken record.  
   
 

### 00:04:30 {#00:04:30}

   
**Mikita Hulis:** Like we we do stuff quick and we can do stuff quick, but after all there is like mainly two well now three of us, but uh Alex is working on the on the marketing sites situation. Uh yeah, there is just like 24 hours in the day less. We are not working 24 hours. Let me tell you that. Every chance.  
**Edvinas Rupkus:** So, how many how many like critical bugs uh are there? Or is it like a whack-a-ole? You fix one bug, another one appears.  
**Mikita Hulis:** you each day I can give you like an answer that like none and then tomorrow I receive with like a couple and then I fix those and or me and Nikia fix those and then there is again none and yeah sort of back and forth at this point already like none nothing critical is there so far everything can be postponed. But if you look at the 4064 ticket, there was like 50\. There's a list of like 50 and like a billion comments of like, oh, by the way, this should work in this sort of manner because I do suppose that uh a lot of those a lot of those are not actually bugs.  
   
 

### 00:05:49 {#00:05:49}

   
**Mikita Hulis:** They they stem from the changing uh requirements. And this is no slide to neither you or Sean, but uh yeah, everybody was in a rush again. And so the the specification changed along the way. We fly we've flown through it like we are past the release. Everything is nice. Everything is great. But if like all of those all of those twists and turns have their have their price meaning that a lot of a lot of changes were required in like during and after the and after the release. But at this point I do hope like fingers crossed that yeah everything is resolved fine.  
**Nikita Orobenko:** We're just hoping Roma will be satisfied at one point of time  
**Mikita Hulis:** That's  
**Nikita Orobenko:** and better to happen sooner than  
**Edvinas Rupkus:** Yeah.  
**Mikita Hulis:** He's never satisfied.  
**Nikita Orobenko:** Later.  
**Mikita Hulis:** That's a  
**Edvinas Rupkus:** Well, definitely definitely ping us if you're like at the point like, "Okay, we don't know if this is something that should be prioritized over if a specific bug is supposed to be prioritized over you know the future implementation because I understand definitely I hear you that we need to reserve time for QA but like I've seen Roma's attention to  
   
 

### 00:07:11 {#00:07:11}

   
**Mikita Hulis:** Yes.  
**Edvinas Rupkus:** detail and it like if a pixel is not in  
**Mikita Hulis:** Oh, believe me, we are giving him we are giving him push back on like each step of the way.  
**Edvinas Rupkus:** place yeah  
**Mikita Hulis:** Please, please believe us. Roma can testify to that. We are already like pri prioritizing on like this can be done afterwards.  
**Edvinas Rupkus:** Yeah.  
**Mikita Hulis:** this can be done by somebody else or later on or like this is not this is totally  
**Edvinas Rupkus:** Yeah.  
**Mikita Hulis:** is being done but uh it is still true that up until yesterday I would say there were uh some constant there was some constant amount of uh like critical stuff I would say not to like maybe not always to the functionality itself but rather to the way that the user perceives it  
**Edvinas Rupkus:** Okay,  
**Mikita Hulis:** which is I'd say even more important cuz we want to sell the ship.  
**Edvinas Rupkus:** go ahead.  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** One more.  
**Ramuald Vishneuski:** Uh so right now u regarding multicourses we don't have critical bugs. Uh the most critical issue was uh issue with certificates that we fixed  
   
 

### 00:08:19 {#00:08:19}

   
**Sean Winslow:** Yeah.  
**Ramuald Vishneuski:** uh uh yesterday and today finally and that's done. Uh we have still a few u minor medium issues uh on front and uh back. Uh some of them uh waits to be deployed already. Uh they are on de branch and uh some of them will migrate uh to future. I will create separate uh tickets for them and we will uh fix it um uh during uh uh our general bug fixing. Uh Sean, I I've sent you a link uh that's uh that's a link uh uh to all campus bugs that's  
**Sean Winslow:** Oh,  
**Ramuald Vishneuski:** exists in tickets in general. It's our main list of bugs.  
**Sean Winslow:** okay. Gotcha. All right.  
**Ramuald Vishneuski:** Yeah.  
**Sean Winslow:** Thank  
**Ramuald Vishneuski:** uh a few a few of the bugs exists in u  
**Sean Winslow:** you.  
**Ramuald Vishneuski:** uh in some tickets uh like for example multour uh I've commented all my bugs there but uh let's say I will create tickets for them and those comments uh uh that that ticket main ticket will go to done section.  
   
 

### 00:09:55 {#00:09:55}

   
**Ramuald Vishneuski:** Yeah. Um but uh that's I will do that a little bit later. Um yeah. So um uh during next uh stage  
**Sean Winslow:** Okay.  
**Ramuald Vishneuski:** uh with uh new payment flow uh I will um uh take a look which bugs from this list should be fixed uh as well during that next step. Um one one issue I want to fix uh that is not related to payment flow. Um as you remember uh like half a year ago we started uh our um uh we started implementation of uh updates for my team and my candidates page. Uh that effort was started by Martin. Uh and we haven't finished that yet. Um I want uh uh somehow uh finish that not uh it's not like I want to do everything from that. I have only one important thing I want to do. It's to add email field to all tables. That's all. Uh everything else uh can wait but that that is very important uh feature. So it's a question to both Nikitas.  
   
 

### 00:11:39 {#00:11:39}

   
**Ramuald Vishneuski:** Um could we do that uh during next u uh iteration with payment flows?  
**Nikita Orobenko:** I mean, if it's just about the email field, I don't see any big problems.  
**Ramuald Vishneuski:** Yes.  
**Nikita Orobenko:** Uh, but we still have like the leftovers. They are more I suppose they're a bit more in the better shape on the front end side regarding all those all those changes, but they're much in the worse shape on the back. So it's just easier to redo from the scratch what was Martin building because it was never finalized. Uh and Nikita can correct me but on the front end side it's more about just uh fix some of the outstanding things instead of just rewriting from the scratch completely.  
**Mikita Hulis:** sort of. Yeah, to be honest, like at this point, I cannot fully recall  
**Ramuald Vishneuski:** Nice.  
**Edvinas Rupkus:** Do we have that ticket still for that that he was working on?  
**Ramuald Vishneuski:** Nice.  
**Edvinas Rupkus:** Who like is it assigned to  
**Ramuald Vishneuski:** Yeah. To to to Nikita or Nikita somewhere in in Jira.  
**Edvinas Rupkus:** somebody?  
   
 

### 00:12:58 {#00:12:58}

   
**Ramuald Vishneuski:** Uh could we go to Kang? I saw that last time there.  
**Sean Winslow:** Which um which ticket was  
**Ramuald Vishneuski:** Um let's see.  
**Sean Winslow:** it?  
**Ramuald Vishneuski:** Um, it's hard to recall how it was called. Um, upgrade. Upgrade word upgrade.  
**Edvinas Rupkus:** I think it's wasn't it enhancements.  
**Ramuald Vishneuski:** Oh yeah. Enhancement.  
**Sean Winslow:** This  
**Ramuald Vishneuski:** Uh-uh. Nope. Nope. Nope.  
**Edvinas Rupkus:** Oh,  
**Sean Winslow:** one.  
**Ramuald Vishneuski:** Nope.  
**Edvinas Rupkus:** here I found it. 40 53 40\.  
**Nikita Orobenko:** 4158\. I  
**Edvinas Rupkus:** No, no, 40\. Oh, did you see this?  
**Nikita Orobenko:** suppose  
**Edvinas Rupkus:** A different one here. I'll I'll drop a link. This is This is definitely the one that uh was assigned to my team. At least one of them. There were a couple tickets maybe.  
**Ramuald Vishneuski:** Yes, this one. That's right.  
**Edvinas Rupkus:** Yeah.  
**Ramuald Vishneuski:** Uh so yeah,  
**Edvinas Rupkus:** Sweet.  
**Ramuald Vishneuski:** we can just do like little part of that. Uh just add the email fields.  
   
 

### 00:14:25 {#00:14:25}

   
**Ramuald Vishneuski:** That's all. Uh and actually it will it should improve um user experience significantly regarding uh hiring feature. uh like uh maybe it will attract uh more users to this feature again. Uh so that's why I want to to do that right  
**Edvinas Rupkus:** Okay,  
**Ramuald Vishneuski:** now.  
**Edvinas Rupkus:** please please mark this as double high priority so that we we don't forget about it.  
**Sean Winslow:** Great.  
**Ramuald Vishneuski:** Yeah,  
**Edvinas Rupkus:** Not that it's going to change anything.  
**Ramuald Vishneuski:** I will I will not forget about this one.  
**Edvinas Rupkus:** Yeah.  
**Ramuald Vishneuski:** I remember of that all the time for the last half  
**Edvinas Rupkus:** Okay.  
**Ramuald Vishneuski:** year.  
**Edvinas Rupkus:** Uh okay. So this is definitely one of the things uh you know the next big release but then speaking about the rest of stuff obviously like having said all that what we said up until now um looking forward to the next big release specifically individual access and 2011 uh ability to purchase it with uh purchasing flows. I know that Alex is starting to work on the individual marketing course, but how about the rest of the stuff?  
   
 

### 00:15:44 {#00:15:44}

   
**Edvinas Rupkus:** Obviously, like the course is live, so that that part is good. But now we just need to connect all the wires.  
**Nikita Orobenko:** I mean on the back end side uh we could say that the account management is close to be like maybe 80 or like 70% done. Uh I still have like a few things to finish up uh on it. then I will gracefully will move forward to the the upsells uh and the rest of the stuff related to the payments because even I even though I revived the things we already did before some of those things will need to be adjusted to support the upsells. uh and maybe it will be missing something because the goal was just to remove everything and roll back the functionality to the state it was before. Uh we even started uh the new payment flow just not to break the existing pro setup. Um so yeah there is  
**Edvinas Rupkus:** When you Yeah.  
**Nikita Orobenko:** only to be chunks  
**Edvinas Rupkus:** When you say user management, are you talking about like within campus user management like the Is this the one that  
   
 

### 00:17:14

   
**Nikita Orobenko:** Yeah, the accountment, the team management,  
**Edvinas Rupkus:** designed?  
**Nikita Orobenko:** uh all that functionality inside of the popup  
**Edvinas Rupkus:** Gotcha.  
**Nikita Orobenko:** window.  
**Edvinas Rupkus:** Any questions on that one?  
**Mikita Hulis:** Wonderful.  
**Edvinas Rupkus:** Like what's supposed to be included, what's not supposed to be included? Like I know that we refined it before,  
**Sean Winslow:** Cool.  
**Nikita Orobenko:** Not not at the moment,  
**Edvinas Rupkus:** but  
**Nikita Orobenko:** but if I will do have anything, I will go straight to you guys.  
**Sean Winslow:** Yeah,  
**Edvinas Rupkus:** Okay.  
**Sean Winslow:** I I created the tickets for uh for this design. So, um I will I did it yesterday. So I'll assign it to you uh to both Nikita's just so you have an idea and then I'll make some upgrades based on  
**Edvinas Rupkus:** Yeah, there's probably there's probably like a sub should be subtask one for back end,  
**Sean Winslow:** well  
**Edvinas Rupkus:** one for front end for I'm not sure like how much along are we in either of those aspects. If you if you had to give a percentage on the stuff like the specific stuff that we see on the screen,  
   
 

### 00:18:12 {#00:18:12}

   
**Sean Winslow:** Okay.  
**Edvinas Rupkus:** obviously we're you know address  
**Mikita Hulis:** So front wise I would say the payment setup not the one on the screen but the  
**Edvinas Rupkus:** Yeah.  
**Mikita Hulis:** individual checkout flow is well I'd say roughly 65% done as it will actually like close to what it was uh before the before the switch uh to the like adjustments for the release. And this is what I'm focused like hopefully entirely focused from now on. Um this is like 65% done. As for upgrades, the feature itself front end wise is uh less complicated. So I'd say most of the UI is done and uh only the redirects are uh remaining which I guess sub like it's like 50% but the the general scope of upgrades on the front end is sort of small and as for the uh user management it's at 0%. uh nothing like user management wise uh is done yet on the front end. It's not like huge uh amount of work but uh the UI itself like the model you see on the screen uh is uh quite complex in its interaction with the back end on of which uh it's like almost done.  
   
 

### 00:19:44 {#00:19:44}

   
**Mikita Hulis:** So I'm finishing up the I will finish up the payment setup and we'll move on to the to the user management for user settings. This one is the larger monops.  
**Sean Winslow:** This one's a what?  
**Mikita Hulis:** larger than the other remaining features I would say.  
**Sean Winslow:** Gotcha. Okay. All right. And then um Claudine I've actually So is there anything uh that you have questions about I mean leading up to this also about sponsored courses or anything like  
**Nikita Orobenko:** Yeah.  
**Sean Winslow:** that?  
**Claudine Daumur:** Um, no, I don't really have more questions.  
**Nikita Orobenko:** Okay.  
**Claudine Daumur:** Um, I finished working on the login flow this morning. Um, I will share the design with uh with you Shen and Ed. Um, now uh what is left for me to do is the completion state. So at the end of the course and that's it.  
**Sean Winslow:** Okay.  
**Claudine Daumur:** Um I finished working on the tablet and mobile versions. So yeah I would say that I have about uh one week left of work on on campus.  
   
 

### 00:21:20 {#00:21:20}

   
**Claudine Daumur:** Um but yeah just for your information I will be um out of office next week. So I will try to finish everything  
**Sean Winslow:** Okay.  
**Claudine Daumur:** um before the end of the week. It will depend on uh how things goes. Um again, if there are any uh you know changing requirements or stuff like that, uh it may take one day or or two to to to finish the the work. But yeah, it's just yeah, just the the completion state and um and I will also share my uh my new login flow uh just to make sure that we are all aligned.  
**Sean Winslow:** Great. Thank you. And you guys, I I know we we had a meeting um we had a meeting kind of going over the actual O and the user flow and everything like that. Um well, I I haven't been able to talk to Mike. wasn't in yesterday, but were you guys uh like good with well I guess I don't know Ed what would the Nikita have to worry about like the actual transition between doco and campus is that something or is that a mic thing?  
   
 

### 00:22:53 {#00:22:53}

   
**Edvinas Rupkus:** for unifying login across campus and co.  
**Sean Winslow:** Yeah.  
**Edvinas Rupkus:** Yeah, I mean we're still quite far away from from that. But he's I think he's doing the ground work basically or at least you know one of the things  
**Sean Winslow:** Okay.  
**Edvinas Rupkus:** that's that's on his mind. But yeah, we definitely once the designs are finished, we should have another refinement session and talk about you know the strategy forward.  
**Sean Winslow:** Okay.  
**Edvinas Rupkus:** Um I guess last thing would be if you know just to chat if like Matt ask asks us where we at with individuals in terms of deadlines, what I would like to get ahead and just set real expectations this time. Um, what are you guys thinking  
**Mikita Hulis:** A question first is uh is there some sort of  
**Edvinas Rupkus:** about?  
**Mikita Hulis:** uh concrete like deadline from the sponsors or something again of the sorts as with the previous release?  
**Edvinas Rupkus:** I mean for from from our sponsors or from our like partnerships, we owe Poly Market a sponsored uh course which was going to happen which  
   
 

### 00:24:13

   
**Mikita Hulis:** Yeah.  
**Edvinas Rupkus:** is we're going to which we're going to work on afterwards uh after individuals  
**Mikita Hulis:** Okay.  
**Edvinas Rupkus:** release. So, in terms of deadline, I haven't like there there hasn't been anything that's like we have to have this in by, you know, May 1st or anything like that. Not that I've heard. Uh it's just every time we meet, we just sort of like update them on what's on what what we're working on. U we have like a lot of other things that we're working on on them as well. So, it's not like we're just ignoring them. So, um I definitely can try and figure out if there's a specific date for the sponsored courses,  
**Mikita Hulis:** Come on.  
**Edvinas Rupkus:** but for the individual access, I mean, we just need to, you know, it's always like ASAP. But I don't have like like like like with the 2011 release like I don't have that sort of you know, Almax says this date or  
**Mikita Hulis:** Got it. Got it.  
**Edvinas Rupkus:** else.  
**Mikita Hulis:** like just uh I was asking more so for clarification cuz like not to like overstep  
   
 

### 00:25:16 {#00:25:16}

   
**Edvinas Rupkus:** Yeah.  
**Mikita Hulis:** and like uh prolong the s\*\*\* but to like truly set a comfortable deadline or like comfortable expectations for you of like how we see the development like Miko of course and Roma chime in but my idea  
**Edvinas Rupkus:** Yeah.  
**Mikita Hulis:** of it is that for for a proper release this time of I would say uh the individual checkout, the current the currently designed like the current setup of the account management uh and uh the account management the uh this setup and the upgrades. I'd say it's like three or so weeks of pure development time before going to QA and then I do suppose like one and a half or two weeks of QA because as we've learned with the previous one this does take time and like if we don't want to do it post like there there is no difference uh like doing it pre or post  
**Edvinas Rupkus:** Yeah.  
**Mikita Hulis:** release only one would be that like some of the stuff would be would be broken. That's that's a given. So like five five or so weeks total I would say.  
   
 

### 00:26:41 {#00:26:41}

   
**Edvinas Rupkus:** So we are right now uh middle of second week of March. Uh one, two, three. So like mid April basically mid to end April.  
**Mikita Hulis:** somewhere along these lines. And guys, of course, uh chime in if you think this is  
**Edvinas Rupkus:** Yeah.  
**Mikita Hulis:** reasonable.  
**Nikita Orobenko:** No, I do agree. especially on the QA part this time  
**Edvinas Rupkus:** Okay.  
**Nikita Orobenko:** because  
**Mikita Hulis:** nothing horrendously broken but there were like a lot a lot of like  
**Nikita Orobenko:** fix  
**Mikita Hulis:** small but important things which is by the way like that's I do say it's something to be proud of nothing was horrendously broken among like the among the releases that we had like the postrelease process was prolonged but not painful I would say so I guess that's that's something to be a problem for  
**Nikita Orobenko:** Yeah,  
**Mikita Hulis:** everybody.  
**Nikita Orobenko:** but I still will prefer fixing the bugs with not my ass being on fire to be honest,  
**Sean Winslow:** Shoot.  
**Nikita Orobenko:** but more calmer pace because when you do realize that's just  
**Mikita Hulis:** True.  
   
 

### 00:27:59

   
**Nikita Orobenko:** suddenly something is not working pretty much everywhere like the cues are not working on the prod the keys are not working on the dav box uh the data here is the one thing the data here is the different thing uh the service are not generated uh we missing that part of functionality the admin panel broke here here and there uh the ros fires  
**Mikita Hulis:** I forgot this was there was one painful day though. Yeah. Yeah. Yeah. True. There was a day when we were busting our ass till 2 till till 2:00 p.m. I should say, not P.M.  
**Nikita Orobenko:** So yeah, if we can get that time will be perfect.  
**Mikita Hulis:** Does this make sense to  
**Edvinas Rupkus:** Okay.  
**Mikita Hulis:** you?  
**Edvinas Rupkus:** Say it again. Uh Nikita.  
**Mikita Hulis:** Does this make sense to you? Does this sound fair and  
**Edvinas Rupkus:** Yeah. No,  
**Mikita Hulis:** reasonable?  
**Edvinas Rupkus:** I mean I mean I I understand there's uh I don't have any like push  
**Sean Winslow:** It's  
**Edvinas Rupkus:** back or anything like that.  
   
 

### 00:29:07

   
**Edvinas Rupkus:** Um, I do want to just, you know, I'm I'm a completionist, so I'd love to get everything sort of have a clean slate and then we can not move on from from campus courses and learning paths, but just like leave them in a good state where we would at least give them a chance to succeed and be sold.  
**Mikita Hulis:** Yeah, cuz like excuse my French, but like like both me and Nikita do not want to look like a whiny b\*\*\*\*\*\* and always talk about like, oh, there was not enough time for this or like there should have been like more time for that. But this has been the truth for like I guess my whole stay at the blog.  
**Edvinas Rupkus:** Yeah.  
**Mikita Hulis:** It sort of like goes in iteration of like oh there is some calm work and then bam something huge happens and your ass is on fire your ass off and then you're tired and then another calm period etc etc. So thank you guys for your understanding. Like it's not the most comfortable thing to uh to live through but uh mama raising no  
   
 

### 00:30:18 {#00:30:18}

   
**Edvinas Rupkus:** Well, well,  
**Mikita Hulis:** so  
**Edvinas Rupkus:** it it would be ideal if we had like a full road map, you know, but we're just sort of living living by the day.  
**Mikita Hulis:** Yeah, building the car while we're riding it always the case.  
**Edvinas Rupkus:** Yes,  
**Mikita Hulis:** It feels like we're all adjusted to it at this point,  
**Sean Winslow:** What's  
**Edvinas Rupkus:** exactly.  
**Mikita Hulis:** but you're you can never fully adjust to it by  
**Sean Winslow:** going to say something new every  
**Mikita Hulis:** noting.  
**Sean Winslow:** time?  
**Mikita Hulis:** She fully agrees. I guess it's  
**Edvinas Rupkus:** Anything else, Sean, that you want to get for this from this uh  
**Sean Winslow:** Nikita O raise his hand real  
**Nikita Orobenko:** Uh yeah,  
**Sean Winslow:** quick.  
**Nikita Orobenko:** I I do feel the risks that may come because we owe the sponsor course that somebody may affect our deadlines because of that uh saying like we we need to get that course up before this day specific one. So in that case we will need to rearrange the plans. Uh to be honest yeah the sponsor courses  
   
 

### 00:31:26

   
**Mikita Hulis:** will become one become two at this point. Yeah.  
**Nikita Orobenko:** are not the biggest one comparing to the upsells to the new payment flow and whatever. So we're starting with the original payment flow. The upsells are the second great priority in the current implementation. Uh so in case if the changes in the plans will arrive from the poly market saying like we need to get the sponsor course as soon as possible. So we will just left uh the upgrades the upsells uh not finished and we will just move forward to the sponsor courses because for the sponsor courses it just what like the new section thing uh like in the minimum implementation right the new section thing on the on the dashboard and just the possibility to launch the course a bit different navigation and generate the SS or something like that. So we even can uh remove the parts of the share it off between the coal and the campus because if it won't be finished up that time uh it's probably not to include to the release.  
   
 

### 00:32:52 {#00:32:52}

   
**Nikita Orobenko:** I'm just trying to visualize what if something will go wrong because it may happen and we won't be able to stop it. So just for everybody to understand that we will need to cut something but uh at least right now we're making the priorities uh based on their true weight in terms of the original purchase flow is a definitely should be included. The upgrades are more optional thing because we can finish them just a bit later. uh and the basics part for the sponsor courses uh also can be done not that except for the share it off uh and the new signin flow I mean technically the signin flow uh we can enrich the campus signin with the x without too much problems because we already had that thing for the crypto IQ here and it's still working. We're still creating the profiles. Uh if you will use it, uh nothing has changed. Maybe the the f\*\*\*\*\*\* Twitter API has changed thanks to the but except I don't suppose nothing else has changed since that. So kind of the minimum the better, but just so everybody will understand the possible risks because I'm feeling that something may not go right this time as well.  
   
 

### 00:34:36 {#00:34:36}

   
**Nikita Orobenko:** As always, I just don't remember any of the situation when everything went just went great without any problems without any changes in the plans. So we will just be aware that something may just change and we will be ready to handle those things uh no matter  
**Edvinas Rupkus:** Yeah, I'll definitely try and keep you posted as soon as I learn anything  
**Nikita Orobenko:** what.  
**Edvinas Rupkus:** like you know more from bond market side in terms of deliver this you know deadlines and for delivery but yeah they're they're definitely the like very picky so you never know what's going to what they're going to say so we should definitely be prepared for like a scoped down version if we need to deliver that as the course itself like the course itself that that we're going to like the sponsored course that we owe to poly market uh about prediction markets that one's already like in review and I think it's with David and and giving his uh review to to the researcher so that's kind of ahead of schedule you know um so but on that part yeah we won't have a blocker  
   
 

### 00:35:51 {#00:35:51}

   
**Nikita Orobenko:** which is great because the content uh is actually the most problematic blocker in terms of testing. Unless we will have the contents uh we're basically stopping the testing of that part as well. That was the most problematic part for the 2011 because uh the dashboard itself is okay nice looking thing but in the reality unless you will have the second course it's barely usable and you don't see anything uh you can just you you just cannot test anything useful with it unless you have the second course and the second course is only available once the content is finalized and we only got the content the the very last minute last time.  
**Sean Winslow:** Yeah.  
**Nikita Orobenko:** So the sooner we will get the content that it will be  
**Sean Winslow:** Yeah. I'm going to speak with David tomorrow. I know I remember the last time I spoke to him,  
**Nikita Orobenko:** better.  
**Sean Winslow:** he said he has everything and everything's pretty much ready because they were able to condense uh all the content that they had from like their pre like Yeah, it doesn't really matter, but we should be good on that end.  
   
 

### 00:36:59 {#00:36:59}

   
**Sean Winslow:** And then I'll double check and confirm with David tomorrow and then I'll I'll you guys posted.  
**Nikita Orobenko:** Okay.  
**Sean Winslow:** But Roma, what you got?  
**Ramuald Vishneuski:** Uh I have a question regarding this uh new sponsored course. So uh uh David will be uh casing it uh again right?  
**Sean Winslow:** Sorry. Say that again.  
**Ramuald Vishneuski:** So David will create this course by himself. Um uh I guess that you noticed uh in  
**Sean Winslow:** Yes.  
**Ramuald Vishneuski:** uh uh digital essentials essentials uh uh 2001 that we have some um uh like buggy behavior. Um I saw that we have VQA nodes I guess from clouding. Yeah. uh that's uh uh there are uh many of kind of small bugs there.  
**Sean Winslow:** Yeah.  
**Ramuald Vishneuski:** Uh so okay uh if if I want to report uh those bugs and I want to get some fixes for it, what should we do? Uh of course u I guess I should create a separate ticket to David. Uh but will he fix that or not? Maybe should we discuss those bugs uh with all of you before before we uh decide what to fix or what is our flow here?  
   
 

### 00:38:39 {#00:38:39}

   
**Sean Winslow:** So I would I would think because yeah, he doesn't really access um Jira as often, but I speak to David on a on a weekly basis. So he cuz when uh Claudine pointed these out, I spoke with David about it and he said, "Okay,  
**Ramuald Vishneuski:** Mhm.  
**Sean Winslow:** I'll take care of these or most of these have been taken care of." So if you write a ticket or if you just, you know, preferably, yeah, just write a ticket and then I'll flag flag it to David so he is aware and then I'll just forward him all the information whatever you give me.  
**Ramuald Vishneuski:** Okay. Okay. Nice. And uh also we should fix uh current 2001 u course uh some buttons and uh how step after step goes uh in in that course. Uh so yeah uh but okay when fix is done we have this new file for for cars. Yeah u what should we do with this new file? Just uh uh remove from uh S3 bucket and upload a new one. Uh Nikita.  
   
 

### 00:39:54 {#00:39:54}

   
**Mikita Hulis:** That's exactly how it works.  
**Ramuald Vishneuski:** Okay. Okay.  
**Nikita Orobenko:** Exactly.  
**Ramuald Vishneuski:** Um  
**Nikita Orobenko:** David is passing me the new source files. I'm just re-uploading them. Uh the only problem is that there is no good mechanism for reuploading them. um right now without the glitch uh cuz if you are in the process of taking the course uh at one moment I need to delete the existing source files and then upload the new one so it's taking the time like around maybe five or 10 minutes so there is no graceful mechanism to prevent the problems for the users Even if there will be a way to upload the new source files just to a different folder name, change the namings in the database which will be much faster comparing to 10 minutes upload time uh of the away time for the user. Uh it still will produce the glitch.  
**Ramuald Vishneuski:** I guess it's not so uh so critical. Yeah. Uh if we choose right timing and so on. Um but the most important thing here uh to stay with users progress.  
   
 

### 00:41:23

   
**Ramuald Vishneuski:** It should not be this progress should not be uh deleted after this switch.  
**Nikita Orobenko:** It's not deleted. It's just the files in the S3. It's has nothing with the  
**Ramuald Vishneuski:** Okay.  
**Nikita Orobenko:** progresses  
**Ramuald Vishneuski:** Okay. That's nice.  
**Nikita Orobenko:** unless we're changing the the indentificators of the subjects or the lessons. Uh we have no problems with the progresses. Only in case if we will change them on the flight then it will produce the problems. But in those cases uh I will start smelling everybody  
**Ramuald Vishneuski:** This is a it's a LMS part.  
**Nikita Orobenko:** will.  
**Ramuald Vishneuski:** So we will not change that  
**Nikita Orobenko:** Yeah.  
**Ramuald Vishneuski:** definitely.  
**Nikita Orobenko:** Uh unless suddenly it will change by itself somehow. But in this case uh believe me there will  
**Ramuald Vishneuski:** Of  
**Nikita Orobenko:** be uh this scream that you will hear uh right from the  
**Ramuald Vishneuski:** course.  
**Nikita Orobenko:** Armenia.  
**Ramuald Vishneuski:** Of course. Okay, we will we will try to do everything on the box first. Of course. I guess everything should be fine if we uh choose right approach.  
   
 

### 00:42:40 {#00:42:40}

   
**Ramuald Vishneuski:** Okay,  
**Sean Winslow:** Great.  
**Ramuald Vishneuski:** that's all for me what I wanted to hear. Thank you.  
**Sean Winslow:** Awesome. Thank you. Uh Nikita  
**Mikita Hulis:** Uh yeah, I have a pretty important adjustments I would say if you would uh kindly scroll to the point  
**Sean Winslow:** something.  
**Mikita Hulis:** one the the overarching thing one. I've read through it carefully and I don't think that right now it actually reflects what we've discussed and like percentages and or assignments etc etc. So first of all uh between point 8 and 9 could you create a separate one uh and move parts of the 0.9 to it meaning like meaning user account management it should be a separate one uh and well let let's go through it by one by one so uh let's separate user account management from 0.9 and assign it uh a separate row assign both and me both and nik both and both Nikita and me uh there and set progress to like about I would say 45% because for account management Nikita is mostly done while there is nothing on the front end side and we are both working on it and not Serena at this point so uh that's that's one Or you can just assign both of us there and uh and set it to 45% as a total progress.  
   
 

### 00:44:25 {#00:44:25}

   
**Mikita Hulis:** Yep. And  
**Sean Winslow:** All right. Yeah.  
**Mikita Hulis:** should should be good to go.  
**Sean Winslow:** Okay.  
**Mikita Hulis:** Nikita is mostly finished. which is also a misleading line cuz who the hell knows which one. Uh yep. Uh this would be the one. Uh then self-service flow is uh correct I would say but it should also include the O there because for all of those features those are both front end and back end. So this is this is also true and uh mid late April should be sort of a common uh common denominator between the two to showcase that like this is not the only feature like this single feature would not take mid to late April. It's the conjunction of both uh of both of them because like because what I'm thinking is that you you guys and Sean would present like our proposed uh proposed deadlines and timings uh to to higherups and I think this should make sense.  
**Nikita Orobenko:** And I suppose we should include the marketing side to the deadline as  
   
 

### 00:45:40 {#00:45:40}

   
**Mikita Hulis:** Uh yep.  
**Nikita Orobenko:** well.  
**Mikita Hulis:** If only there was a way to unify the column and I don't think there is because it's pretty excell Yeah,  
**Sean Winslow:** Okay.  
**Mikita Hulis:** this should this should make sense. I think it's understandable that all of those would be released at the same time. So um well yeah it it actually would be better suited as like the part of the blue column but I I I I think you'll be perfectly able to uh convey  
**Sean Winslow:** Yeah. Clean it up.  
**Mikita Hulis:** it.  
**Sean Winslow:** But yeah, no, that's I mean that's perfect. I'm glad we got to that point. Um,  
**Mikita Hulis:** Sorry I'm a sucker for order.  
**Sean Winslow:** no, dude. I appreciate it. This is this is perfect. This is exactly why we had this meeting. And I also I wanted to just extend uh what the discussions were at the retro and the and uh stand up yesterday because obviously there was a lot to talk about and we weren't able to talk throughout the whole thing.  
   
 

### 00:46:57

   
**Sean Winslow:** But yeah, so um I'm glad I'm very glad we had this. This is very very much uh now I'm caught up to speed. Exactly. And yeah, do you guys have anything else that you want to discuss before we head out?  
**Mikita Hulis:** One more thing since we are so in sync and in touch now and and everything is handled for today. How about uh me and Roma will skip uh today's daily to enjoy some of the sun while it's still out.  
**Sean Winslow:** I was gonna say that works for me. Yeah,  
**Edvinas Rupkus:** Yeah,  
**Sean Winslow:** this was this was your st.  
**Edvinas Rupkus:** we definitely this was definitely a very long stand update.  
**Mikita Hulis:** True.  
**Sean Winslow:** Yeah.  
**Mikita Hulis:** A personalized one nonetheless. Sorry, I'm already like my time doesn't work.  
**Sean Winslow:** No, it's understandable. Yeah. Uh, thank you guys. I very much appreciate it. And yeah, enjoy the rest of your evenings.  
**Mikita Hulis:** Yeah. And then back for the for some even evening work. Wonderful. Thank you guys.  
   
 

### Transcription ended after 00:48:26

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*