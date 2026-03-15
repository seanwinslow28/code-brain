# 📝 Notes

Feb 3, 2026

## Unified Daily Standup

Invited [Brian Mendoza](mailto:bmendoza@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikola Pivcevic](mailto:npivcevic@theblock.co) [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [vention-team](mailto:vention-team@theblock.co) [Cesar Paz](mailto:cpaz@theblock.co) [Ana Benitez](mailto:abenitez@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Maryia Zhynko](mailto:mzhynko@theblock.co) [Marina Lozuk](mailto:mlozuk@theblock.co) [Koray Baspinar](mailto:kbaspinar@theblock.co) [Bohdan Vadimovich](mailto:bvadimovich@theblock.co) [Yermek Smagulov](mailto:ysmagulov@theblock.co) [Aliaksandr Kryvanosau](mailto:akryvanosau@theblock.co) [Serena Ho](mailto:sho@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [ramuald.vishneuski@ventionteams.com](mailto:ramuald.vishneuski@ventionteams.com) ~~[Josh Gragg](mailto:jgragg@theblock.co)~~

Attachments [Unified Daily Standup](https://www.google.com/calendar/event?eid=M3V1anRvazFuaXV1MzNjaW9ldXBhaWpnbnFfMjAyNjAyMDNUMTUwMDAwWiBlcnVwa3VzQHRoZWJsb2NrLmNv) 

Meeting records [Transcript](?tab=t.mr89ji2cmiua) 

### Summary

**Marketing and Marquetto Updates**  
Work related to the enterprise marketing page and all Marquetto-related tasks are moving into the testing phase, indicating progress in content delivery systems.

**API and Integration Progress**  
Multiple integrations and core platform enhancements are progressing, including user deletion error handling, new Pro API development with authentication, and the CMI5 XAPI multicourse implementation reaching a functional state.

**Multicourse Testing Dependencies**  
Company-wide testing for the multicourse is currently blocked by a required spreadsheet and ID hardcoding, necessitating accelerated syncing with an external party, though overall progress is better than a week ago.

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

NEEDS FURTHER DISCUSSION

**Create New Repository For Jordan Stack**

Temporary solution implemented for Jordan's NAN stuff; future plan is creating new repository for configuration and code to deploy stack in LWS infrastructure.

ALIGNED

**Create New PMP Page Ticket**

New issue detected after fix evaluation for PMP page; Ana will create new ticket for this different issue and close current ticket.

**Acquire Course Overview Videos**

Missing course overview video and subject overview videos needed for new interactive course; Sean will talk to David and Josh about video creation.

*More details:*

* **Enterprise Marketing and Marquetto** Aliaksandr Kryvanosau is finalizing the combo ticket for the enterprise marketing page, specifically working on the carousel animation after completing the scroll stack animation. Sean Winslow noted that all Marquetto-related work is currently in testing and appears locked in, with no further developer side input needed. Mikita Hulis confirmed that the outstanding item to hide Marquetto forms from the front end, due to the collaboration ending, has been completed and deployed ([00:00:00](#00:00:00)) ([00:13:02](#00:13:02)).

* **Page Fixes and Migrations** Ana Benitez is testing stock pages, particularly ETFs, and will begin work on new tickets for token pages. They are also planning to complete the migration of the team members and events pages. Ana Benitez reported that the PMP page fixes worked according to a Google search evaluation, but a new issue has arisen, which Nikola Pivcevic agreed is a different issue, and a new ticket will be created for it ([00:00:00](#00:00:00)).

* **User Deletion and Article Logic** Bohdan Vadimovich finished a ticket concerning error handling during user deletion, which is ready for testing. They also started working on a ticket about article logic related to updating the author page, a topic previously discussed with Ed and Nikola Pivcevic ([00:02:02](#00:02:02)).

* **Poly Market and LMAX Integrations** Brian Mendoza spent time working on the Poly Market integration and finished the LMAX navigator page, which can be moved to testing. Brian Mendoza noted a potential conflict regarding the homepage display, where Matt might want to use the latest trending markets, which would be the opposite of what was just built, and plans to seek clarification on the desired approach ([00:03:09](#00:03:09)). Marina Lozuk is also working on the Poly Market project, having created the necessary UI components and is trying to determine how to find the most relevant market event data for articles. Marina Lozuk indicated that they will need more information, possibly adding a list of questions to the ticket, due to ambiguities in the Figma data ([00:09:00](#00:09:00)).

* **Airflow, Clover, and Rippling Integrations** Cesar Paz completed a task to establish communication between Airflow and Redis in the production environment, despite them residing in different AWS accounts and VNCs ([00:04:00](#00:04:00)). They also created new security rules on Clover related to rate limiting from different IPs to reduce transferred gigabytes from various websockets. Cesar Paz is currently working on two urgent tasks to change the credit card information in various services to reflect the new card associated with Rippling, and is reviewing new Salesforce emails for possible changes ([00:05:04](#00:05:04)).

* **Salesforce and Campus Multicourses** Ramuald Vishneuski tested Elmax and is continuing with the Salesforce migration, noting some issues related to how records are kept in Salesforce and the responses received. Ramuald Vishneuski and Lil are expected to discuss these Salesforce issues, which can be reviewed in a ticket from Aliaksandr. Ramuald Vishneuski will also continue work on the campus multicourses ([00:21:58](#00:21:58)).

* **Category, Tag, and Learn Pages** Koray Baspinar is working on category and tag pages, as well as Learn pages, focusing on creating a topic selection feature for evergreen articles. Koray Baspinar conducted an audit last week showing a decrease in errors and warnings on hrefs, which they attributed to the team's efforts, and plans to continue working on them ([00:06:24](#00:06:24)).

* **Podcast Page and ETF/Stock Fixes** Maryia Zhynko completed the Eden Force podcast to podcast page, which is ready for testing. Maryia Zhynko also implemented a few fixes for ETFs and stock pages. Sean Winslow mentioned they would discuss the Election Hub with the design team to see if they are ready to move forward with the tickets that have already been written up ([00:07:50](#00:07:50)).

* **iOS App and Pro API Updates** Mike Price is working on the iOS application, focusing on integrating authentication using Privy and developing the associated strategy. Mike Price also coordinated with Matt to implement a quick notification system using Firebase for provisioning. They are developing a new version of the pro API, which is a precursor to a self-service API, and is focused on building backwards compatibility to ensure existing pro API token holders can access it. Mike Price is collaborating with Matt and leadership on the pricing structure and strategy for the self-service model to correctly configure Stripe ([00:10:08](#00:10:08)).

* **CMI5 XAPI Multicourse Progress** Mikita Hulis reported significant progress on the CMI5 XAPI multicourse situation, which now allows importing interactive courses, storing them, providing access, and generating player links, functioning beyond a proof of concept. Mikita Hulis is currently concentrating on the layer of interaction between the player's inbaked methods and the back end, specifically ensuring support for older course versions like the 101, alongside the new version ([00:11:29](#00:11:29)).

* **Multicourse Testing and Checkpoint Dependencies** Nikita Orobenko reported great progress, with most functionality resolved ([00:13:02](#00:13:02)). Nikita Orobenko highlighted that company-wide testing is dependent on the course being imported, which requires David to finish a spreadsheet that is dependent on a person picking questions for the test who is on PTO until Friday. The completion of checkpoints work is blocked until the course is imported and new IDs are generated, which David needs to hardcode into the XAPI course ([00:14:17](#00:14:17)). Nikita Orobenko emphasized the need for acceleration and regular syncing with David to resolve questions quickly, acknowledging the limited timeline but stating their position is better than a week ago ([00:16:14](#00:16:14)).

* **Course Video and Thumbnail Requirements** Nikita Orobenko informed Sean Winslow that course overview videos are missing—a short public marketing video and overview videos for each subject—because the new interactive course focuses on audio. Nikita Orobenko pointed David towards Josh as a potential resource for video creation and noted the continued need for image thumbnails ([00:17:20](#00:17:20)). Sean Winslow agreed to follow up with David regarding the videos and Josh's involvement ([00:18:33](#00:18:33)).

* **Recent Deployments and Future Work** Nikola Pivcevic reported the deployment of several smaller tickets, including the AMP issue and rich text editor on FAQs, and the WordPress portion of the new rating page prediction markets ([00:18:33](#00:18:33)). Nikola Pivcevic has a ticket for broken external links ready for testing and, in collaboration with Maria, a dev box ready for testing white papers. The Elmax navigator page is scheduled for deployment today, and Nikola Pivcevic plans to begin work on video for WordPress ([00:20:04](#00:20:04)). Nikola Pivcevic also confirmed that a hardcoded fix for adding Apple podcast links was implemented and is ready for deployment soon ([00:21:13](#00:21:13)).

* **Voiceovers and Workflow Updates** Sean Winslow stated they finished their portion of the campus voiceovers and will meet with David to discuss moving forward, including helping with a few more tasks. Sean Winslow also mentioned working on Zapier workflows for the podcast and RevOps crews, similar to the NAN work Caesar Paz was handling ([00:16:14](#00:16:14)) ([00:23:22](#00:23:22)).

### Suggested next steps

- [ ] Koray Baspinar will keep working on the errors and warnings on hrefs and work on their monthly report this week.  
- [ ] Ana Benitez will create a new ticket for the new issue with PMP page fixes and close the current one.  
- [ ] Brian Mendoza will figure out how to test the LMAX navigator page, make a quick PR to look at the data, and update Sean Winslow in the ticket regarding Matt's request for trending markets on the homepage.  
- [ ] Cesar Paz will check all the Salesforce emails.  
- [ ] Marina Lozuk will add a list of questions regarding the poly market data displayed in Figma to the ticket or send them to Sean Winslow.  
- [ ] Mike Price will work with Matt and leadership on the pricing structure and strategy for self-service, and ensure GAN works correctly on the iOS app after the updates.  
- [ ] Sean Winslow will get the course overview video and the image thumbnail to Nikita Orobenko as soon as possible.  
- [ ] Nikola Pivcevic will start working on the video for WordPress.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=0u0SPh7Z3SAbvKYPGHRcDxIUOAIIigIgABgBCA&detailid=standard)*

# 📖 Transcript

Feb 3, 2026

## Unified Daily Standup \- Transcript

### 00:00:00 {#00:00:00}

   
**Aliaksandr Kryvanosau:** can mute it.  
**Mike Price:** I did it myself.  
**Aliaksandr Kryvanosau:** Nice. You can side hustle as a you know hair cutter.  
**Mike Price:** I thought about it once or twice.  
**Aliaksandr Kryvanosau:** You also miss the channel.  
**Sean Winslow:** Jeez. All right, we'll get started. Alex, start with you.  
**Aliaksandr Kryvanosau:** Okay. So for me the combo ticket about uh marketing page for enterprise I was able to finalize the scroll stack animation and now I'm finalizing the carousel one and after that it will be ready for review.  
**Sean Winslow:** Awesome.  
**Aliaksandr Kryvanosau:** That's it on my  
**Sean Winslow:** Yeah, I see all the Marquetto stuff is in test.  
**Aliaksandr Kryvanosau:** end.  
**Sean Winslow:** Um, yeah, Liil Liil was asking if there was anything else on the developer side, but it looks like everything's pretty pretty much locked in. It's just waiting for the end of testing.  
**Aliaksandr Kryvanosau:** Yep. Correct.  
**Sean Winslow:** Cool. Awesome. Thank you, Anna.  
**Ana Benitez:** Um hello so I am testing a stock pages ETF and Maria shar some new tickets for token pages so I will start on those um and also planning to finish team members and events page migration um and that's all uh another thing uh Nicola I was taking the PMP page fixes that were made.  
   
 

### 00:02:02 {#00:02:02}

   
**Ana Benitez:** I ran like a um fix uh evaluation on Google search and it says it it is the fix worked but there's a new issue. So if you're okay I can create another ticket for that and close this  
**Nikola Pivcevic:** it. Yeah, I was looking at it and like yeah,  
**Ana Benitez:** one.  
**Nikola Pivcevic:** I saw like there is like some other but like yeah weird issues come up and like we need to Yeah, let's let's create a new ticket. Yeah, it's a different issue as you said.  
**Ana Benitez:** Yeah. Okay. Thank you.  
**Nikola Pivcevic:** Yeah, sure. Thank you.  
**Ana Benitez:** Uh that's all.  
**Sean Winslow:** All right, cool. Thank you, Anna. All done.  
**Bohdan Vadimovich:** Yes. Hello there. So I finished working on that ticket for uh when there is error when deletion of user uh it's ready for testing and uh I started working on the ticket that Ed and Nicola were discussing about u article logic when updating the author page and yeah that's pretty much it.  
**Sean Winslow:** Awesome.  
   
 

### 00:03:09 {#00:03:09}

   
**Sean Winslow:** Thank you. Any any more exams coming up?  
**Bohdan Vadimovich:** Uh yeah, in two weeks.  
**Sean Winslow:** Two weeks. All right. Thank you, Bodon. Brian  
**Brian Mendoza:** Cool. I spent most of the past few days working on the Poly Market thing and the last yesterday was the LMAX uh navigator page. Um I think we can put that in testing. I'll figure out how we can test that. I'll make a quick PR for some like just to look at the data, I guess. And I think Matt might want to change it. There was another conversation where he was like, we need to use the latest trending markets or whatever from the past few days. So, I'm going to see what we're actually want to do on the homepage here, but I'll keep you updated in the  
**Sean Winslow:** Cool. Thank you. Yeah, I've been I've been following along.  
**Brian Mendoza:** ticket.  
**Sean Winslow:** I've been trying to track exactly what he said. Do you have you been talking to him separately?  
   
 

### 00:04:00 {#00:04:00}

   
**Sean Winslow:** Do you understand what he's asking  
**Brian Mendoza:** No, it's that other ticket that that's that's signed to Marina.  
**Sean Winslow:** for?  
**Brian Mendoza:** Um, I got a notification for that and he was like and it it was just like, yeah, the homepage will be using the latest trending or uh markets. So, that's all I know. I just got a notification yesterday and I was like, wait, that that's like the exact opposite of what we just built. So, I will see what he wants, what he  
**Sean Winslow:** Okay. Yeah, because I know he's he's in communication with Poly Market,  
**Brian Mendoza:** wants.  
**Sean Winslow:** so I'm sure they're just tossing things his way and he's just like, "All right, we'll we'll try to figure it out." So, thank you. I appreciate it, Brian. Caesar.  
**Cesar Paz:** Hi. Uh well uh today I finished uh a task which is now in the down column. Uh basically I created the communication between airflow um um radius in the pro environment both was in in different AWS account in different VCs.  
   
 

### 00:05:04 {#00:05:04}

   
**Cesar Paz:** So I I I I had to work on this. Uh in addition uh today in the morning I was uh creating new uh security rules on Clover about the rate limit uh from different IPs uh basically to reduce the gigabytes uh to process or to transfer from our uh web from different websockets we have. Um and now I'm working on um in two task um to change the great card in different services because we are using a new great card uh associated with rippling. Uh this task is in the urgent uh yeah in the urgent part is the first one the the second one sorry and I'm checking new cell force emails too because uh maybe I have to implement some change I don't know where but maybe I have to to check all these cell force  
**Sean Winslow:** Awesome.  
**Cesar Paz:** emails we have a lot so working on this right now and that's  
**Sean Winslow:** Thank you. Yeah. Did you finish up the stuff with Jordan? All the NAN  
**Cesar Paz:** Yeah. Yeah.  
   
 

### 00:06:24 {#00:06:24}

   
**Sean Winslow:** stuff.  
**Cesar Paz:** Uh we have a temporary solution right now. Uh right now um but probably in the future we should uh create a new repository with all uh the configuration and all the code he has. um because maybe in the future we want to deploy all this stack in our infrastructure in LWS. But by now we have a temporary solution. It's fine. It's working fine. Um yeah, he's happy. I think uh that's all.  
**Sean Winslow:** Thank you, Caesar.  
**Cesar Paz:** Thank you.  
**Sean Winslow:** Corey.  
**Koray Baspinar:** Hello. Uh I I'm working on u category and tag pages uh and also working on learn pages as well. Uh creating uh some kind of topic selection uh for those evergreen articles and also I did an audit last week and looks like our errors and warnings are decreasing uh on hrefs which is great. Thanks Nicolola and Brian also as well everyone let's say and I will also keep working on them. Uh and next thing is I will be working on my monthly report this week.  
   
 

### 00:07:50 {#00:07:50}

   
**Koray Baspinar:** Yeah that's all.  
**Sean Winslow:** Perfect. Yeah. How'd the move  
**Koray Baspinar:** Uh I didn't lose my mental so it  
**Sean Winslow:** go?  
**Koray Baspinar:** is good.  
**Sean Winslow:** Good. All right. Yeah. Step in the right direction. All right. Thank you, Corey. Maria.  
**Maryia Zhynko:** I finished with uh Eden force podcast to podcast page. It's uh ready for testing actually. Uh also did a few fixes for ETFs and stock pages. And that's it.  
**Sean Winslow:** This is ready for testing. Okay.  
**Maryia Zhynko:** Yes.  
**Sean Winslow:** Yeah. Thank you, Maria. I I'll look into So, I have a meeting with design uh about well, just our weekly sync, so I should find out more information about the the election hub and so I already have a bunch of tickets written up. It's just a matter of seeing what they had to tinker with a few things. So, I'll talk to them and see if we're good to start moving forward and then I'll let you know if I have some extra stuff for you.  
   
 

### 00:09:00 {#00:09:00}

   
**Maryia Zhynko:** Okay, thank you.  
**Sean Winslow:** Thank you,  
**Marina Lozuk:** Hello, I've been working on the poly market.  
**Sean Winslow:** Marina.  
**Marina Lozuk:** I've already created all necessary component for the UI and currently working on the trying to figure figure it out how to find the most relevant uh like market event for articles. So, it's quite tricky. So, working on it.  
**Sean Winslow:** Okay, cool. Thank you. Yeah. And are all the like whatever docs that Matt was sending and adding to the tickets, are they helpful or do you need more information, more context?  
**Marina Lozuk:** I believe that I will need more information even because of Figma there are some data which is displayed and not really obvious what should be shown there. So probably I will add the list of questions regarding that.  
**Sean Winslow:** Okay,  
**Marina Lozuk:** Yep.  
**Sean Winslow:** cool. Thank you. Yeah, just either uh send them to me or write him down on the ticket and then Matt probably see it so  
**Marina Lozuk:** Okay.  
**Sean Winslow:** he'll he might have more information because he's the one kind of leading that ship.  
   
 

### 00:10:08 {#00:10:08}

   
**Sean Winslow:** But thank you, Mike.  
**Mike Price:** Uh currently working on the iOS app. Um working on integrating off um with Privy and building that strategy out and uh coordinated with Matt building out notifications of a quick little notification system with Firebase uh to help them provision that. Um and working on a new version of our pro API which will be a precursor to full self-service API. um want to get out back I started working on some backwards compatibility so that folks with existing pros API tokens can access it. Um main reason being we have some clients out there who need some functionality that current API does not give and rather than build on that rather just kind of ship the API version API portion of the project um sooner than later so they can have access to that and kind of benefit from it. Um but yeah, be working with Matt and um leadership on pricing structure and strategy for self-service um so we can set up Stripe correctly with the product structure and all that. So what I'm hands off  
**Sean Winslow:** Nice.  
   
 

### 00:11:29 {#00:11:29}

   
**Sean Winslow:** Yeah. And uh Yur said you guys met you were meeting on Monday, so everything's  
**Mike Price:** Yeah, to talk about GAM and I gotta run that.  
**Sean Winslow:** good.  
**Mike Price:** Yes, I gotta run. He did some updates. So, I gotta run make sure GAN works right on that. Forgot about that bit.  
**Sean Winslow:** Okay.  
**Mike Price:** Yeah.  
**Sean Winslow:** All right. Nice. Thanks, Mike. Nikita  
**Mikita Hulis:** Yep. Uh well, we have I would say huge progress in the CMI5 uh XAPI multicourse uh situation meaning that we can now import those interactive courses, store them, provide access to them, generate links to them from which we are able to generate a player for those and we have I would say more than a proof of concept that it will work. uh and right now working on uh the layer of interactivity between not interactivity but interaction between the player and its inbaked methods uh and our own back end. Uh personally I'm focused right now on the uh on the support for the older versions of courses basically for our 101 so that it can be it can still work with the older version of UI without the disembedding and interactivity in the video format while uh keeping the new version possible as well.  
   
 

### 00:13:02 {#00:13:02}

   
**Mikita Hulis:** Uh otherwise uh yeah great state progress uh we have I would say a an action item for I don't know the editor maybe it's not the editorial team but basically for the for the guys who are preparing the course some action would be required from them but more on that from Nikita wouldn't steal the spotlight there from him and also took care of one of the outstanding items for emergence section actually which Ed has asked me quite a while ago hiding the Marquetto the stuff from Marquetto since our collaboration uh is ending and that's all from  
**Sean Winslow:** Cool. Yeah. Yeah. Ed mentioned that to me too. You said it's completed.  
**Mikita Hulis:** Yeah,  
**Sean Winslow:** It's good.  
**Mikita Hulis:** it's deployed. No more Marquetto forms on the on the front end.  
**Sean Winslow:** Beautiful. Thank you,  
**Nikita Orobenko:** Yep.  
**Sean Winslow:** Nikita.  
**Nikita Orobenko:** Um so the progress is a great uh one. Um we were able to resolve most of the functionality at least to understand how it should be done and done it actually.  
   
 

### 00:14:17 {#00:14:17}

   
**Nikita Orobenko:** Uh the thing is that we as far as I know we are planning to start the companywide testing but we do need to understand that we will be able to do it only once the course will be imported. The course will be imported once the David will finish the spreadsheet. the David will be able to finish the spreadsheet once the person who's responsible for picking the questions for the test will pick them but that person as far as I know uh is on the PDO till Friday this week. Um, so I do suppose we need a little bit of the acceleration here. Uh, if if it's possible because the sooner we will get it, the sooner we will finalize our own things on the development side because we are not able to finish the checkpoints uh work until the course will be imported. The David will get our own ids which he will put into the X API course. Then he will make a new export. Then we will upload the new export to the S3. then we will be able to make uh the checkpoints uh thing working because right now the goal is that once you're finishing the subject you should be redirected to the checkpoint uh quiz page after each of the subjects uh to our own interface and David need to hard basically kind of hardcode the links but we only will get the proper links once we will import the course and once we will get our own IDs for each subjects,  
   
 

### 00:16:14 {#00:16:14}

   
**Nikita Orobenko:** lessons, the checkpoints, whatever. We are on a daily sync with David in terms of uh filling out the spreadsheet. So whenever I have any questions to him or he has any, we are resolving them as soon as possible. But if it's possible to keep your guys uh eyes on it, that will be better cuz uh we're doing our best. Uh cuz we do have a bit limited timeline. But we are not in the same uh bad place as we were the week ago to be honest. So that's a good news.  
**Sean Winslow:** Cool. Yeah, I'm actually meeting with him after this meeting to discuss some updates. I finished all of my end of the campus uh voiceovers. So, he said he's going to start pushing them through, but we're just going to touch touch base. So, I'll bring that up to him and then yeah, I'll let you know if anything else come but you're meeting daily. So, but yeah.  
**Nikita Orobenko:** Yeah,  
**Sean Winslow:** Uh,  
**Nikita Orobenko:** whenever it Yeah.  
   
 

### 00:17:20 {#00:17:20}

   
**Sean Winslow:** cool. Yeah, I'm I'm keeping an eye on it. So,  
**Nikita Orobenko:** The only other thing uh we do need to have the course overview  
**Sean Winslow:** thanks  
**Nikita Orobenko:** video uh like it should be a short video that similar to what we have right now which we can uh put to the public marketing page that will should be able inside of the uh should be available inside of the campus plus we should have the overview video for each subject. Uh and we don't have those videos because the current the the new course is everything about uh is everything about everything but not the videos because it's an interactive course with a uh audio uh layer uh on top of it. So I pointed David to the Josh. I suppose the Josh may be the best uh person right now uh to handle the video creations or something. At least maybe Josh can navigate, but just for you to know that we don't have any videos and we need again uh the image uh thumbnail for it. So, a lot of different small things but still important  
   
 

### 00:18:33 {#00:18:33}

   
**Sean Winslow:** All right, you got it. I'll get that to you as soon as possible.  
**Nikita Orobenko:** things.  
**Sean Winslow:** I'm going to talk to him, see what the deal is, see if he's spoken to Josh, and I'll once that's over, I'll update you.  
**Nikita Orobenko:** Yeah. Again, if if you will have if you will need anything from us, just don't hesitate and ping because again, uh we are at the same boat here.  
**Sean Winslow:** Okay, cool. Yeah, I'll I'll see what I can do. Thank you, Nikita.  
**Nikita Orobenko:** Yep, no problem.  
**Sean Winslow:** Appreciate it. All right,  
**Nikola Pivcevic:** Uh yeah, hello everyone.  
**Sean Winslow:** Nicola.  
**Nikola Pivcevic:** I just wanted to comment like how Nikita sometimes adds D before someone's first name and so he will say like D Josh and like makes it sound like oh it's not any Josh it's the Josh you  
**Sean Winslow:** Be  
**Nikola Pivcevic:** know it's um it's  
**Nikita Orobenko:** But in case of the Josh,  
**Nikola Pivcevic:** amazing.  
**Nikita Orobenko:** it's basically like the the Josh  
**Nikola Pivcevic:** Um all right so for me uh a bunch of like smaller tickets some I deployed so the AMP issue was deployed the rich text editor on FAQs was deployed uh the new rating page prediction markets yeah this was also deployed I mean like the WordPress part they need to build it right and then uh so yeah I have this broken external links uh wrapped up I have it um Uh Brian reviewed it and I have it uh ready in testing.  
   
 

### 00:20:04 {#00:20:04}

   
**Nikola Pivcevic:** I have a D box for it. Uh and uh can you scroll up a bit? Sorry. Yeah. Uh all right. The white papers. Uh yeah, in collaboration with Maria, we have a dev box ready for testing. Uh and yeah, this one is Yeah, I think I put this one last week to for ready for testing. this charts any charts on ETF stock pages. Okay. And uh yeah, finally I guess we are deploying Elmax navigator page today which is um amazing.  
**Sean Winslow:** Good  
**Nikola Pivcevic:** Yeah.  
**Sean Winslow:** news.  
**Nikola Pivcevic:** And uh yeah this enable FAQ schema output in WordPress. Uh Maria also picked this one and uh so it's just on a dev box just for testing but it's basically it was done. We just kind of um we removed uh we deleted like three lines that kind of were skipping this code from executing. Okay. And uh yeah, and I think I'm kind of finally ready to kind of look into video for WordPress.  
   
 

### 00:21:13 {#00:21:13}

   
**Nikola Pivcevic:** Yeah, I'll I'll start working on that.  
**Sean Winslow:** Nice.  
**Nikola Pivcevic:** Yeah,  
**Sean Winslow:** Cool.  
**Nikola Pivcevic:** that's all.  
**Sean Winslow:** Thank you.  
**Nikola Pivcevic:** Yeah.  
**Sean Winslow:** Yeah, I actually have a question. Jordan reached out to me yesterday about finding how to upload like Spotify links to the uh podcast page. Did it reach out to you?  
**Nikola Pivcevic:** I Yeah, he did. I created a ticket for myself and yeah, I just need uh to ask someone for a review, I guess. Brian, uh yeah, I have it ready. Yeah, I'll probably like we can deploy today or tomorrow.  
**Sean Winslow:** Okay, cool. Yeah,  
**Nikola Pivcevic:** It's hardcoded.  
**Sean Winslow:** I'll I'll look inside.  
**Nikola Pivcevic:** Yeah. Yeah, it's hardcoded.  
**Sean Winslow:** Oh,  
**Nikola Pivcevic:** So there is no like option to change it.  
**Sean Winslow:** it is. Gotcha. Yeah, because I I was looking for it.  
**Nikola Pivcevic:** Yeah.  
**Sean Winslow:** I was like I found I found all the links for the like separate podcast, but I couldn't find the other thing, and it was it was bugging me.  
   
 

### 00:21:58 {#00:21:58}

   
**Sean Winslow:** So, Right. But it's hardcoded, so I'm not going  
**Nikola Pivcevic:** Yeah, it's uh yeah,  
**Sean Winslow:** crazy.  
**Nikola Pivcevic:** this add Apple podcast link to layer one. Yeah, I just created a ticket so I don't  
**Sean Winslow:** Okay,  
**Nikola Pivcevic:** forget.  
**Sean Winslow:** perfect. Awesome. Thank you, Nicola.  
**Nikola Pivcevic:** Right. Thank you, Sean.  
**Sean Winslow:** Romano.  
**Ramuald Vishneuski:** Hello team. Um so I've tested Elmax quickly. Uh now I continue with um Salesforce migration. Uh we have some little issues but those are related to Salesforce itself not to work we've done. So uh perhaps we should discuss that with Lil I suppose. Yeah. And um uh we'll continue with uh campus uh multicourses. Um yeah, that's all  
**Sean Winslow:** Okay. So, what what were you saying about the sales for the what was the issue or it's it's not an  
**Ramuald Vishneuski:** uh those issues uh how we keeping our  
**Sean Winslow:** issue.  
**Ramuald Vishneuski:** records in uh Salesforce and uh uh what uh responses we get from Salesforce.  
   
 

### 00:23:22 {#00:23:22}

   
**Ramuald Vishneuski:** Uh so um uh you you can uh uh check those uh issues in u uh ticket from Alexander. Yeah. Uh that one.  
**Sean Winslow:** Got awesome.  
**Ramuald Vishneuski:** Thank you Alexander.  
**Sean Winslow:** Okay, thank you.  
**Ramuald Vishneuski:** Yeah.  
**Sean Winslow:** Perfect. Cool. Yeah, I'll let I'll look into that and then I'll let her know cuz she's trying to stay completely updated on everything. All right. I appreciate her, Ro. And I don't think Yarmick is in here, right? Nope. All right. So, yeah. So, the main updates for me are finishing up I pretty much finished up the voiceover stuff. So, and I'll be meeting with David just discuss how we're moving forward. I should be helping him out with a few more things. So, I'll let you guys know how that goes. And the other things are like Zapier Zapier workflows. Just trying to figure stuff out like similar to the NAN stuff uh that Caesar was working on. I was doing stuff for the podcast uh crew and the RevOps crew. And those are the updates from me. But does anybody else have anything they need to discuss? All right. So, enjoy the rest of your evenings, guys, your mornings, and I'll talk to you tomorrow.  
   
 

### Transcription ended after 00:25:11

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*