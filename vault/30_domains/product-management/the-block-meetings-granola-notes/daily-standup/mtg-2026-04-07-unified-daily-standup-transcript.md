---
granola_id: 84313aac-6e54-44b4-8822-deb5fc5861e0
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of unified daily standup - transcript.
context: the-block
created: 2026-04-07
source: granola-sync
attendees:
  - bmendoza@theblock.co
  - mprice@theblock.co
  - npivcevic@theblock.co
  - mvitebsky@theblock.co
  - erupkus@theblock.co
  - mhulis@theblock.co
  - cdaumur@theblock.co
  - vention-team
  - cpaz@theblock.co
  - abenitez@theblock.co
  - norobenko@theblock.co
  - mzhynko@theblock.co
  - mlozuk@theblock.co
  - kbaspinar@theblock.co
  - bvadimovich@theblock.co
  - ysmagulov@theblock.co
  - akryvanosau@theblock.co
  - sho@theblock.co
  - koliva@theblock.co
  - ramuald.vishneuski@ventionteams.com
note: "[[30_domains/product-management/the-block-meetings-granola-notes/Unified Daily Standup.md]]"
---

# Transcript for: Unified Daily Standup

## Attendees
- Ben Mendoza (bmendoza@theblock.co)
- Mike Price (mprice@theblock.co)
- Nikita Pivcevic (npivcevic@theblock.co)
- Matt Vitebsky (mvitebsky@theblock.co)
- Ed Rupkus (erupkus@theblock.co)
- Maria Hulis (mhulis@theblock.co)
- Claudine Daumur (cdaumur@theblock.co)
- Cesar Paz (cpaz@theblock.co)
- Anna Benitez (abenitez@theblock.co)
- Nika Orobenko (norobenko@theblock.co)
- Marina Zhynko (mzhynko@theblock.co)
- Marina Lozuk (mlozuk@theblock.co)
- Koray Baspinar (kbaspinar@theblock.co)
- Bogdan Vadimovich (bvadimovich@theblock.co)
- Yermek Smagulov (ysmagulov@theblock.co)
- Akira Kryvanosau (akryvanosau@theblock.co)
- Serena Ho (sho@theblock.co)
- K. Oliva (koliva@theblock.co)
- Ramuald Vishneuski (ramuald.vishneuski@ventionteams.com)

### Guest (2026-04-07T14:01:17.554Z)

Sean.

### Sean (2026-04-07T14:01:18.103Z)

How's it going everybody?

### Guest (2026-04-07T14:01:53.634Z)

How's everyone doing? She said nice vacation. Yeah we had on Mondays either holiday. Lucky you. Know is there in us. No Friday is a bank Friday is a bank holiday like the markets are not open but yeah at least at the Block it hasn't been ever used. And I took a PTO I guess.

### Sean (2026-04-07T14:02:32.263Z)

Yeah,

### Guest (2026-04-07T14:02:32.994Z)

Well, I mean.

### Sean (2026-04-07T14:02:34.103Z)

There is Easter, but it's on Sunday. So we already have the day. Off.

### Guest (2026-04-07T14:02:39.874Z)

Okay guys on Monday so I thought there's I didn't I'm pretty sure that people take their perspective time off like if it's a holiday in Czech Republic then it's a holiday for you I think that's how okay okay thank you. I guess I had it in the in the Block calendar that's like Easter holiday but probably that's because locally it.

### Sean (2026-04-07T14:03:07.543Z)

Yeah.

### Guest (2026-04-07T14:03:10.514Z)

S just one of those where it's like. It's like a Friday afternoon to sort of work day you know barely anyone's at the office everybody's wearing jeans like that sort of day.

### Sean (2026-04-07T14:03:27.223Z)

Or in our case not wearing pants at all.

### Guest (2026-04-07T14:03:31.314Z)

Well speak for yourself Sean.

### Sean (2026-04-07T14:03:34.583Z)

All right, on that note, let's get right into it. Start with Alex.

### Guest (2026-04-07T14:03:39.794Z)

Hello. For me I've been working on the tweezer identification integration like.

### Sean (2026-04-07T14:03:46.743Z)

Ander.

### Guest (2026-04-07T14:03:46.754Z)

The last video I said that I had a block ratio which was successfully resolved after I call with nikita oh then I prepared all file update pages with wallet and data consent parts and then I had another call with nikita to understand the logic and guards on which I had to put there to prevent. Not to prevent to have like a proper flow there. And then continue working on it.

### Sean (2026-04-07T14:04:14.663Z)

Perfect. Thank you, Alex. Anna.

### Guest (2026-04-07T14:04:22.274Z)

So I'm working on testing the added events for election hub. For da for and also the fixes for home page coverage and Twitter sharing preview. Also on election hub Serena is working on the Viteoi so I'm waiting for her if she has any feedback and I'll share it with you in case of it that's all for the other tickets not an election hub I'll continue with recirculation tickets. Marina worked on.

### Sean (2026-04-07T14:05:00.823Z)

Perfect. Thank you, Anna.

### Guest (2026-04-07T14:05:02.034Z)

Okay awesome. Is how close do you think we are with the election coverage? I know that you said Sabrina is doing VQA but it's probably not much left there. Yeah probably not much hopefully we're getting closer I'm just in these last fixes Marina and Maria work done. Great. Yes hello there so the ticket for invalid URLs throughout the like price stock and ETF pages it is ready. I think Brian approved it. So I will create a dev box once like other tickets are tested so that like Caesar asked not to create too many dev boxes and the tickets for. Like that FAQ section that is like expanded by default. Is read essentially there just appear like one little thing that I kind of didn't think about so I'll quickly fix it and then I will send it to review as well. That's pretty much it.

### Sean (2026-04-07T14:06:19.143Z)

Perfect. Thank you, Bad. An. Brian.

### Guest (2026-04-07T14:06:26.594Z)

But I spent most of the weekend like debugging this out not an outage but this really really slows degradation we had last week on Tuesday and Thursday. I've made some I'm going to document whatever I found on confluence and I made some small changes that might fix it. It's not some consistent thing. It was the first to slow downs we've had in like a year. Or like at least a very, very long time. But still Caesar noticed some numbers are way too high. Yeah, I'll document everything and go back to work and tickets. Yeah, that's it.

### Sean (2026-04-07T14:07:01.863Z)

Thank you, man. Caesar.

### Guest (2026-04-07T14:07:10.594Z)

Hi, just today I'm working in the immigration from terraform cloud to our self hosted. Basically I created a new repository to create the history bucket to say for terraform state by workspace. I created a dynamo DB table in order to lock the Terraform meter form apply in order to not create conflicts. Yeah, I'm testing this for the boxes. I have to add a new ACS task for atlantis in order to simulate terraform cloud with atlantis in GitHub. So I'm working on this. I'm investigating because this is new for me. So yeah my time now is fully dedicated to this task. I've created a new one to renew certificates in Azure. Yeah, because I received several emails for renewing them. And that's all.

### Sean (2026-04-07T14:08:25.703Z)

Cool. Thank you, Caesar.

### Guest (2026-04-07T14:08:28.434Z)

Thank you. I'm mainly working on data right now checking the impacts from Google core updates. And also working on Google search console Ahrefs at the same time. To report some issues that affecting the page performance. And also working, we'll be working on my monthly report. And also I started at FAQ price pages. That's all.

### Sean (2026-04-07T14:09:08.903Z)

Cool. Thank you, Corey. When did the Google core update happen?

### Guest (2026-04-07T14:09:14.274Z)

Right. Last week started to spend 10 days. So yeah, I think this week is going to finish.

### Sean (2026-04-07T14:09:16.343Z)

Okay.

### Guest (2026-04-07T14:09:20.434Z)

Towards the end of this week.

### Sean (2026-04-07T14:09:22.503Z)

Got. Cha. Thank you. Kristoff.

### Guest (2026-04-07T14:09:30.514Z)

So I finished the file. So once tested, we can be found by AI over you and I'm working on the charts like they failed to load when. The dashboard series that I empty. Like it's a small buck kind of but I'm working on now. And then I do like some learning. There was an obstacle which Mike sent me and I had a meeting with Nikita. I just let it for me.

### Sean (2026-04-07T14:10:04.263Z)

Thank you, Kristoff. Maria.

### Guest (2026-04-07T14:10:12.994Z)

I did a fix for Twitter preview card. There was some issue with display incorrect image. And also I started working on adding iOS app banner to the site.

### Sean (2026-04-07T14:10:29.463Z)

Cool. Thank you, Maria.

### Guest (2026-04-07T14:10:34.914Z)

Hello for me I expanded the Google analytic for the charts and the election page for the poly market also fixed minor bug for the pre browser. And currently working on the adding targeting for the ads. So which are we created. So that's it. Quick question on the election coverage. That's probably for Maria. Do we have just a reminder please do we have events set up for stained with crypto reports cards? Yes, I did set up it. How like what kind of level is it just the ones that navigate to their site or like let's say. You know how many Twitter. Going to say Twitter account navigate into their website also added. Events to track share on Twitter. Interaction. The ones that like we press on the individual profiles like the oh yeah I guess you can mention that already. Okay. All right. Thank you.

### Sean (2026-04-07T14:11:58.183Z)

Thank you both. Mike.

### Guest (2026-04-07T14:12:06.594Z)

Real updates. I still need to deploy the iOS off. For campus to get that finished. So I plan on finishing that this week really and then I got some few a few Simon. I'm actually talking to Simon about Simon AI. He's got some feedback. He's got some ideas. So I'm about to work with him for a little bit and see what we can do there.

### Sean (2026-04-07T14:12:28.903Z)

Cool. Yeah. Please. I will probably talk to you about that as well. Thank you. Thank you, Mike. Nikita ghoulis.

### Guest (2026-04-07T14:12:44.194Z)

Yep. So I'm pretty much mostly done with the UI for the social sharing and as a result of the sponsored course like an abstraction from the back and it's. Like not yet finished. So in the meanwhile Kip in terms helping will help out both Alex and and you know with either Twitter authentication and or the backend implementation and then it's the integrations tab between the backend and frontend for the. For the sponsored courses. And yep and like a few few minor tweaks here and there for the for the UI itself. And that's all.

### Sean (2026-04-07T14:13:32.983Z)

Thank you very much. Nikita. Oh.

### Guest (2026-04-07T14:13:41.794Z)

We finally release the new implementation for the payments to the prod last week. It went. Kind of okay normal no huge breaks or something so but we discovered that the API versions of the stripe we're using should be largely and heavily upgraded. So the upgrade is already on testing on the dev box. That will allow us to enable accepting the crypto payments. Because the right now version does not just allow it seems like Vitek will be able to enable the unrock integration on the prods already. So there will be one less question. Flying. Under the ground and not resolved. So working on the sponsored courses most of the API I'm moving to be finished a few little things. Did we get any final decision on how we are working with the. Bonuses after completing the course? Like it will be the code? Will it be the link if it will be the link how that link will look like? Plus we do have a button to share the results on Twitter. I just want to remind that we won't be able to share the image itself. Into the twit because it will allow it will require us requesting an additional access to the person's Twitter account, which we probably don't want to do based on the experience from the crypto key. So, but we can prepare the tweet. Which will contain the link publicly available link to the certificate and it will show a large image preview inside of that tweet. Plus we can add some text to it. So I will need a decision here as well and if it's just the link with some kind of text, the text as well also pinged David about the course. We will start wrapping up the spreadsheet to import that course. Not sure about how the progress on the consent is going on.

### Sean (2026-04-07T14:15:56.023Z)

Okay.

### Guest (2026-04-07T14:16:26.354Z)

But I suppose we need to start finishing it up. On the sponsored course. Yeah. The content has been finished. If anything it's just been he's just been playing with like additional stuff for demos. Like all last time I knew was that the content is finished. I mean we had sent it out to public market already to sign off. So we haven't heard anything from them. And to answer your earlier question about the rewards they had to push a call from last week we had all these questions ready for them. So we have a trail of messages, you know asking all these questions. So for now we're going with the codes. Like they provide the codes. That we give out to each of the users. And then if later on they come back and they don't like that. You know it's you know not going to be a ding on us. Because they have the question that we didn't have the requirement. So for now let's go with the with the code implementation and each completion is a new is a code that's coming from a list they provided us. And the Twitter thing is fine. Yeah. Sean and I can work on the actual copy of the tweet. Yeah. Link would work. I missed anything else. Yeah and regarding the course itself just want to make sure that we do have. The course overview image that we're showing on the dashboard. Just to make sure that everything is in place. That thing most likely the course overview video.

### Sean (2026-04-07T14:18:09.943Z)

Okay. Yeah.

### Guest (2026-04-07T14:18:18.434Z)

Like a short video that talks about the course or if we don't need to have it we may skip it. But if we need to have it we need to have a video. For both of those things. Yeah that's like the script that we were talking about with media and the last call and then if you could chase down design in terms of the polymer. I think we would be using the same poly market cover image. For that like has been in the figma designs. But we just have to make sure that we all are on the same page research and design. On the actual cover image. I don't know if that was a placeholder or not so we just need to get confirmation.

### Sean (2026-04-07T14:19:00.743Z)

Okay.

### Guest (2026-04-07T14:19:02.114Z)

Yeah and the that yeah the video we definitely had plans for video because you probably would show that video on socials like on the release and then also on the overview like. Before people start that course. Okay. I know that there's quite a few things that we still have to deliver to you to course all the supplemental materials etc. But if you had to give an estimation once every all that stuff is like covered how we're how are we tracking with sponsored courses overall. Would you say a week more two weeks more. I think we need like. We maybe just need to sync with Alex Nick to see where we're at to get the. Estimation with the same mace not just. My humble opinion on that. Topic. Plus to include the estimation for testing. As well.

### Sean (2026-04-07T14:20:18.823Z)

Cool. Makes sense.

### Guest (2026-04-07T14:20:21.394Z)

We can chat a little bit upon it like my estimation would be that if like if all of the necessary stuff was. There today. Then it wasn't. Like be much of an overshare to have the original deadline of like mid April. Mind you without testing. So for development to be done maybe like. A few days on top of it, not more. But yeah, it's all will depend on like how quick those decisions would be made and how final are those because like strictly speaking from like the like as I've said during the like my portion the sharing part like I did implement all of the variants of like what it could be like with the code, with the link, et cetera, et cetera, et cetera. But those decisions influence the backend implementation. Pilot.

### Sean (2026-04-07T14:21:23.383Z)

Gotcha. Understood.

### Guest (2026-04-07T14:21:24.354Z)

Yeah understood.

### Sean (2026-04-07T14:21:30.743Z)

Okay. All right. Yeah. Thank you, guys. Yeah. Well, pretty much one of the main things that we're waiting on are just, you know, Pilot market giving us answers. But yeah, like I said, go with the code and I will work on getting design up to speed with the video and everything like that. So I appreciate it, guys.

### Guest (2026-04-07T14:21:51.154Z)

Thank you.

### Sean (2026-04-07T14:21:51.863Z)

You're welcome. Michaela, welcome back.

### Guest (2026-04-07T14:21:59.394Z)

Yeah thanks Sean hello everyone. So yesterday fixed the issues reported by Roma on crypto jobs. Updated the dev box I think everything is now. Okay except the requirements changed and reviewed the document for the for implementing this synchronization with loxo, I guess. We have a meeting about it later today as well. And other than that so continued working on the translations. Now experiencing some issues with memory issues with that's like translation plugin and WordPress is running out of memory. And kind of trying now to investigate like is there like a memory leak or is it like really that heavy? I don't know and yeah like working on that not sure exactly. Yeah Brian. Sorry one thing when I was looking at TV code this is I think I sent it in slack. Could I make a big deal about it? There were some very very big like task spikes in ECS for WordPress. I think we hit 75. Not even on the same day that tvco had that issue it was like in that same window. It was insane. And I think there's another smaller spike again like TV call like two spikes one huge enormous one kind of big. I'll try to save the screenshot or find that but maybe it could be related. I didn't look at memory usage for WordPress in that time frame. But I did see a huge 75 test spike in ECS it was crazy weird like WordPress is blocked for external traffic like editorial team spun up 75 tasks. I see I'll see you I'll find that screen sure I'll find that page and send you it and the thing is that how this translation plugin works is like issues. Like asynchronous request and then triggers like some processing and those fail, right? Like you don't see anything. It's just that you know the translation doesn't go through and like it not you don't see anything on the screen it's just the network called fails and it's like out of memory and I don't know like I couldn't figure it out yet. Please do share maybe it's connected I don't know maybe it's yeah and also what I didn't kind of what we I guess like wanted to do we did this in production but not locally so we didn't split payloads and wordpress cache because it fails while loading cash and that's why when it fails when it tries to load WordPress cache like that's the last call that like then triggers out of memory. And so maybe I thought like it was a casting issue and so I kind of moved the wordpress cache to a separate redis database. Locally as well, which I think is nice and we should have done that like a long time ago but yeah. Yeah I have that as well but it's not it's a good thing to do but it didn't fix my issue. Yeah and also so Corey reached out to me and talking about SEO stuff of course and so he pointed out there is like an important ticket that should be done so apparently Google now doesn't like any page larger than two megabytes and kind of if I understood correctly Corey like kind of threatening to deindex those pages. And those influence all our data pages. And so it's kind of a high priority ticket I would say like I didn't start working on it I could potentially but like on the expense of maybe like some other tickets yeah, I just wanted to hire bring it up and like yeah see like if someone wants to have some cycles to take a look at it or should I prioritize this? I don't know like I just just wanted to bring it up. I can look at it because sponsored course is going to pick up again soon now I get those ready for QA but that won't be for whenever that is. So I could take it for a day or two or until that's ready and then maybe hand it off to Bogdan or you or someone whoever has bandwidth if I can't fix it. Yeah yeah I'm not sure I how to fix it I have no clue because like yeah data pages are heavy like and I don't know like I was thinking maybe sacrificing SSR somewhat I don't know how we'll see figure it out I'm not sure like you know Google like loads everything oh do we load the data pages SSR we might dude because I'm not unintentional but we might be doing some heavy loading that we are maybe we are loading the data we are not rendering I'm sure that we are not rendering the chart but maybe we do include the chart data in the payload maybe that maybe I'm guessing that that's probably if it's over two megabytes that has to be what it is nothing nothing can be that big yeah. And also wrote a ticket for lcp for those pages as well. Brian also treasuries also giving the other not just data. Huge payloads. Data definitely is a bigger priority and much more urgent than treasuries but yeah definitely. I wanted to mention so looked at what I was looking at this SEO issues and I saw that we kind of dropped in Google search traffic like about 20 30% in the last few weeks which kind of don't like it yeah Kara was looking into it I was I was monitoring that as well but it appears that from Christ first impressions that it's all it's seen across our competitors as well. Yeah yeah like this core update back to back core updates is hitting really bad especially in these publishers and I checked 10 of our competitors only being crypto is benefiting from these updates there nine is suffering a lot especially coindesk lost two and a half million point traffic looks like in April so yeah we have like when I compare to data it's like 20% decrease in traffic in clicks also impressions dropped a lot but impressions let me give also update about this like Google really have a big fuck up since last April they reported wrong impressions data and they were inflated data not actual data and they just click they are just fixing it now and we might see dropping impressions but it's like. It will be overall everyone will see this drop in impressions so yeah. We'll continue monitoring. But also we need to wait until this core updates finish and a week or 10 days to see the actual picture actually yeah yeah I also take another look at across our content types and it really is just news so it's just all like how much it is being you know pushed into the news and discover and all that it's not like you know data or prices are getting a huge hit other ones are being stable is just news with fewer fewer feet in the door basically. We can also think about like there is one since one month there is global issues and interest is so we can do that direction bigger things right now than crypto news. Okay, let's let's continue Sean.

### Sean (2026-04-07T14:30:57.703Z)

Cool. Nichola, are you finished?

### Guest (2026-04-07T14:30:59.794Z)

Yeah that's all thanks Sean.

### Sean (2026-04-07T14:31:00.983Z)

Cool. Thank you. Roma.

### Guest (2026-04-07T14:31:07.074Z)

Hello everybody so now I'm retic payments on Devbox because as Mikita said strap API changed. Also added few more things for crypto jobs for front end so backend part is done but I haven't tested it yet I will I will test it when front end part is done. But I don't know like Alexander will not fix that separately I guess it will go with log integration. So but we will discuss that a little bit later and working on my AQI project almost done.

### Sean (2026-04-07T14:32:04.583Z)

Nice.

### Guest (2026-04-07T14:32:05.714Z)

Moved that to AWS now need to do some estimation. How more effective it is compared to github actions so we'll do that and I guess that's all.

### Sean (2026-04-07T14:32:26.983Z)

Go. Thank you, Ram. A. Ed, anything else that you want to bring up? All right.

### Guest (2026-04-07T14:32:44.834Z)

Right I was gonna say nothing to update the lockslow integration is the top of mine we'll jump to that fit this call.

### Sean (2026-04-07T14:32:55.943Z)

Yeah. And not too many updates on my end, pretty much continuing zapier stuff. They added some more things that they wanted me to add to it. So just keep on building on that. And, yeah, just minor tasks, just getting them done, getting them out of the way. So other than that, does anybody else have anything that they want to discuss before we head out? Oh, what's up, Rama?

### Guest (2026-04-07T14:33:24.914Z)

Who is alex. Believe it. S like a consultant from our portfolio companies or not our portfolio from like all the owners. Companies so I think it's just like. Consultant to help us optimize whatever. Our workflows etc etc. So they're just doing some interviews whatever that's all I know. I'm actually meeting that person myself in a couple hours. So yeah sure thank you just was wondering about him okay thank you.

### Sean (2026-04-07T14:34:10.903Z)

No problem. All right, guys, thank you very much. I'll talk to you tomorrow. Have a good evening.

### Guest (2026-04-07T14:34:19.314Z)

Thank you.

### Sean (2026-04-07T14:34:20.983Z)

Bye, guys.

