---
granola_id: 9c0e7aa4-40ad-45aa-a548-c5a0c2068e20
title: "Unified Daily Standup - Transcript"
type: transcript
created: 2026-04-09T13:59:24.160Z
updated: 2026-04-09T14:36:47.403Z
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

### You (2026-04-09T14:00:53.792Z)

Hey everybody. Kristoff. Greetings Ed. M. Onth I say this. At risk. We. Do. Have an agend. A for today. That's going. Through a couple. Of open it. Ems. Welcome. To some sort of. Criteria for methods. Here. A little. Bit. Some agent planning. Or. Mobile. Questions. All right we'll go ahead and get started. We got about 14. So we'll go ahead and go with Alex.

### Guest (2026-04-09T14:02:12.429Z)

So first of all regarding the prebit ticket after approval on the box, I deployed it to further testing and for now there is a missing thing. So I had to undeploy the fix there and now it's still again progress. Then the Twitter notification. I finalized the main part there and now the remaining work is refactoring. Also I had the call with Nikita square regarding the go back button on the profile update pages. So now there is like complex logic. There between. Page navigation due to some old middlewares and we agreed to remove the gold back button because we need to force users to visit certain pages depending on mission fields such as if the email is not verified or if there is no agreement on the data consent or missing first or last name. So the user has logout button. And it's enough in our opinion. So if you don't have any objections there we just remove the go back button. From profile update pages.

### You (2026-04-09T14:03:22.912Z)

Yeah, I personally don't have any objections Ed, do you? Go?

### Guest (2026-04-09T14:03:33.629Z)

I don't have any questions. Tomorrow we plan to have a call regarding the certification flow to see if everything in place. And if yes then it will be ready for review.

### You (2026-04-09T14:03:45.152Z)

Perfect thank you Alex. Ana is out. She gave us some updates. 46 34 is ready for deployment and she informed Marina. 3277 is ready for deployment and informed Badan. And then she made some comments on report cards full page ticket. Made some comments on election hubs landing page. And that's it from her today. So she's currently in the air or will be in about an hour. So. Thank you Anna. Well done.

### Guest (2026-04-09T14:04:38.349Z)

Yes, so as you said the ticket for like a bug for like misconfigured destinations is waiting for deploy. Also finalize the ticket for like large number being cut off bug on converter pages. Also got this ticket for effective dates in terms of service. Just literally a few seconds ago received a little comment from Ed that I just showed like slightly change design. But overall it's fine. And that's pretty much it in terms of what I've done. There is like one thing that I would like to bring up. I assume something related to what like Caesar and Nicola perhaps were discussing. So the thing is I found like an issue relatively odd one. That only if you're not on VPN or like AG in my case I'm in Croatia. Some data is missing on the site. To be precise, for example on converser pages in that module you can like choose cryptocurrency or a fiat currency. And it was just missing. There was nothing. And then Brian told me like I'll try to try on like American VPN because for him it was completely fine. And that American VPN it works. Perfectly. But then I turn off BN again and again like it's empty. And I assume it's something like that probably very recent and something like regional. And also it might be like on some similar issue on different places throughout the site. So yeah, that's kind of what I wanted to bring up. Because I'm not really sure what caused it but yeah.

### You (2026-04-09T14:06:41.392Z)

Cool yeah thank you for the heads up go ahead.

### Guest (2026-04-09T14:06:42.109Z)

Okay. Tell me through luck what this is like exactly the issue and in what URL you are experimenting this and I can check. Okay, I will send it. In some group channel. I'm interested as well. Okay, I'll create like a DM. You can put it in dev. Ice looking into it too. I think she could comment too when she's when she has access to her computer.

### You (2026-04-09T14:07:20.032Z)

Perfect thank you everybody thank you Bodan. Brian.

### Guest (2026-04-09T14:07:28.509Z)

I am wrapping up this Google bot to make a by page for all on data dashboard thing. I look at treasuries as well. But I figured out why it was so big on the data dashboard we are loading all the chart data up front on SSR. Like the big JSON files as well, which is not great. So yeah. That'll be another 10 bucks by today or tomorrow.

### You (2026-04-09T14:07:51.472Z)

3. Thank you Brian. Caesar.

### Guest (2026-04-09T14:08:00.829Z)

Keep working in the immigration. Right now. Atlantis is almost working. I'm testing through a bull request. It's working. I need to fix the permissions from AWS. But it's working. And when I finish this test, I'm going to apply this new way to execute terraform to our boxes in order to eliminate the problem to reduce the number of the boxes to half because of the recent updates from terraform. So keep working on this. That's all from my side.

### You (2026-04-09T14:08:48.032Z)

Perfect thank you Caesar.

### Guest (2026-04-09T14:08:49.949Z)

Thank you. I'm working on my geotechnical and also checking the data both from Bing and Google search console about the impacts of Google corrupt date. But from my earliest assumptions. I can say that corrupt, they didn't. Hit hard us because I see that the data on our evergreen pages are stable. Mostly news there is decrease in news articles which might be related to also market interest at the same time. Because since one month. Is more occupied with Iran. And global kind of issues. So that might be it. But we will see the overall picture I think in one week or 10 days. That's it from my side. Thank you.

### You (2026-04-09T14:10:12.432Z)

Nice thank you. Next we'll go with Kristoff.

### Guest (2026-04-09T14:10:20.189Z)

Guys from my side. I'm still working on the task with the charts. I guess I had some role there. Maybe I will need to sync up with Nicole about it. Maybe, Nicola, if you can tomorrow, I'll try to work it on myself. But yeah, just maybe you can help me out with that. Then on through the daily edge, we're going to sync up. Because I have the final state exams at the beginning of June. I already know like the dates the second week of June. So I decided like I need to focus on that in May. So now I can still like continue working normal as we agreed. But then in May, I'll probably have to prepare for that. I will still be able kind of maybe to join some meetings and stay in the loop. But I guess I won't be able to work as I'm working on. So that's something that we need to schedule at. So we have a call after the daily and yeah, that's it from me.

### You (2026-04-09T14:10:52.912Z)

At all. Gotcha all right cool yeah thank you for the heads up. Here. Maria.

### Guest (2026-04-09T14:11:25.069Z)

Hello. Today I did some fixes for elections pages that are posted. Also continued working on adding iOS banners across the site. I have replaced access module at the top of the page and finishing with pop up. That will replace newsletters, daily newsletters. Model.

### You (2026-04-09T14:11:57.232Z)

Perfect thank you oh geez. Thank you Maria.

### Guest (2026-04-09T14:12:05.709Z)

I finalize fixes for the election bully market stuff and proceed working on the adding, targeting for the ads regarding safety keywords. So I'm still working on it. That's it.

### You (2026-04-09T14:12:23.792Z)

Great thank you. Mike.

### Guest (2026-04-09T14:12:31.069Z)

Adding terms of service and privacy flags and marketing flags to the iOS app as well as the API for supporting it. That also kind of involves a little bit of an overhaul to how we create users. So it's probably a significant update. But I'll have it today. And then one more thing to support the app where we go live and that's a selectable sponsor.

### You (2026-04-09T14:13:02.592Z)

Special.

### Guest (2026-04-09T14:13:02.749Z)

Field basically that will support in WordPress will add the sponsor logo and link and all that stuff.

### You (2026-04-09T14:13:02.752Z)

Ly just giving. Support. For condition.

### Guest (2026-04-09T14:13:10.349Z)

And then allow us to push it. I was thinking we could use that. Or maybe we can use gam. I don't know. We're already doing a game integration. But yeah, I think I was just kind of thinking in the old way of doing things instead of setting up sponsors. I don't know if we like doing sponsors in gam yet.

### You (2026-04-09T14:13:31.472Z)

Yeah, it's a good question I guess we can. We could talk to your mech about that because I don't know what would it be a pain to do both like if you already have game integrated.

### Guest (2026-04-09T14:13:43.069Z)

No, no, it would be a pain.

### You (2026-04-09T14:13:43.792Z)

Yeah okay.

### Guest (2026-04-09T14:13:47.069Z)

Yes, I'm gonna roll WordPress initially and then we can circle back before I'm gonna use cam or something. Cool.

### You (2026-04-09T14:13:54.432Z)

Cool thank you Mike.

### Guest (2026-04-09T14:14:02.749Z)

So we are started. We have started the integration process between backend and front end for the. Sponsor course to support. And as Alex has already mentioned, we've had a huddle between ourselves about like joining basically three pieces of developed software in all the authentication flow, the sharing success flow and the. And the back and for the both of those have a pretty nice idea of how it should roll. Tomorrow was again Alex had mentioned. We'll have.

### You (2026-04-09T14:14:39.072Z)

Swarm. The catalog.

### Guest (2026-04-09T14:14:39.469Z)

One more thing verifying that the implemented. Update to the Twitter authentication are good to go and yeah, continue to integrate in integrating the. Two. The back button if you was already mentioned, we're dropping it. So yeah, that's pretty much it. One thing though to Brian actually we'd like to discuss, like for a few minutes a thing regarding the redirect to to the course. So if you don't mind, could you join us? In huddle after the daily? Thank you. That's all. Right. Not a big one on my ends. Working on the multiple things regarding the sponsor courses. Started at the same process with Nick for the integration parts as well as adjusting some things for Alex on the authentication side. I think that's pretty much it for now. Also had a convol with David's. He sent an example of the course. We'll take a look at it a bit later. Do we still have to finish up the spreadsheets? Process to import the course?

### You (2026-04-09T14:16:22.832Z)

To. Complete my gotcha he sent you the the final like approved version like after like.

### Guest (2026-04-09T14:16:29.949Z)

Kinda? Yeah, we just need to see how the rise course emits the custom API X API calls we need to track the lesson and events. We will be able to track the course progress. And actually issue.

### You (2026-04-09T14:16:56.112Z)

Gotcha all right cool. Thank you Nikita. Michaela.

### Guest (2026-04-09T14:17:08.429Z)

Went depressed like unmute and instead of like launched an app. Yes sir. So yeah today spent investigating singular live for the new show start on block that we'll be doing can say I can't say that this app has like a nice user experience. It's so confusing. Like I still like I spent the whole day like trying to like click around and still have no clue what's going on. Yeah. So you know when was the last time like you had to lead the user manual to understand like how when to use an app like yeah not that friendly. So I still I kind of I was able to figure out like some of the stuff like how the load the chart that we were talking about and yes how to create some like elements there, but I still struggled to figure out like how to like have dynamic content based on data. Looking into that right now.

### You (2026-04-09T14:18:24.032Z)

Did you check out they have like a few standard YouTube videos just about like an overview but did you look at all the live streams and stuff because I saw yeah nothing nothing was helping. Not really.

### Guest (2026-04-09T14:18:38.749Z)

It's vague you know like you have to look a 15 minute video and it doesn't answer your question and then you're like why did I look at this?

### You (2026-04-09T14:18:39.792Z)

Yeah. Yeah.

### Guest (2026-04-09T14:18:46.989Z)

Yeah most of most of the videos are like in terms of setting up like the designs and stuff rather than setting it up with at least the ones that I looked at. It's like demos to what this platform can do rather than like. And then like it says like look at the tab on the left that says data there is no such tab, you know like, why did I even ask him? Yeah I can show you I can show you where the yeah, we can we can like troubleshoot together if you'd like maybe maybe like using it like you know we can you know use it together and share knowledge because like yeah.

### You (2026-04-09T14:19:23.872Z)

I think that's the move. Cool yeah I will happily do that for you because I've been very curious about it myself. So I'll let you know whatever I find out.

### Guest (2026-04-09T14:19:37.469Z)

Maybe we can have like a short meeting tomorrow and like share like what we. So like I don't know if maybe have you gone to the like API endpoint screen? So I did look at it but that's not the main so I'm trying to figure out like so there is like a data object that I should be able to like kind of set like even manually and then like this like automatic tablets the layouts but and then like the API just kind of updates this main data repository. And like that's part two but the first part of like kind of setting up this kind of data store which kind of controls the layout. I'm still.

### You (2026-04-09T14:20:18.512Z)

This.

### Guest (2026-04-09T14:20:29.069Z)

Like still fingering it up.

### You (2026-04-09T14:20:32.192Z)

Other. Perception. Good yeah thank you Nichola. We'll definitely set something up soon.

### Guest (2026-04-09T14:20:46.109Z)

Hello so I continue with payment flow and my AQA project and I found some bugs on campus. And that's what I'm doing now. That's all.

### You (2026-04-09T14:21:04.032Z)

Gotcha thank you Rama. Do you have anything that you want to bring up?

### Guest (2026-04-09T14:21:11.149Z)

Nothing to add if anything else people up over and slack.

### You (2026-04-09T14:21:16.272Z)

So. Cool yeah and updates on my end. Michael I don't know if you have time for after the meeting but we're hoping to just talk to you about some claude stuff I told you last week that we were trying to do some PM work utilizing Caude and the claw different cloud skills so or if not after this meeting just at some point whenever you're free.

### Guest (2026-04-09T14:21:41.949Z)

Okay yeah that sounds fine.

### You (2026-04-09T14:21:44.672Z)

So after the stand up you're good to stay for a little bit.

### Guest (2026-04-09T14:21:47.709Z)

Yeah yeah we can do that.

### You (2026-04-09T14:21:49.232Z)

Sweet. And outside of that same tasks just chip it away. So does anybody else have anything that they want to discuss before we head out. All right sweet. Well everybody enjoy the rest of your evenings the rest of your days have a good weekend if I don't see you tomorrow. And yeah I'll talk to you Tuesday. Thanks team.

### Guest (2026-04-09T14:22:18.669Z)

Thank you. S bounce.

### You (2026-04-09T14:22:32.592Z)

I think so. Yeah so I guess we'll prep real quick the the main thing that we want to discuss was like the WordPress.

### Guest (2026-04-09T14:22:47.309Z)

Yeah just saying like if we could. From his perspective give access connect WordPress. To club max. And just like. Seeing if there's any red flags that he sees that. You know. Because we need an admin. To do it I guess right. So just getting his take on like how we should approach that we want it just to get grant access to the ETF page for example.

### You (2026-04-09T14:23:24.112Z)

Okay. Yeah. I'm gonna ping him. All right. Whenever whenever he pings us we can just make a new meeting or something. All right cool.

### Guest (2026-04-09T14:25:01.149Z)

Yeah. See. What's up? Yeah so we were. Trying to see I talked to Matt about this and ran it by him first. But I'm gonna see if there's any. Very mundane and easy. VM tasks such as like adding ETFs to our WordPress page that could be automated through the use of cloud. So his Matt was like why would you not connect it to WordPress why would you not give the mcp access to our WordPress and specifically like let's say the page so we wanted to we wanted to I wanted to run it by you first to see like what's your take on that you claude MCP access to our WordPress? Yeah no that's a bad.

### You (2026-04-09T14:26:24.752Z)

Okay.

### Guest (2026-04-09T14:26:26.269Z)

Idea that's that's what I that's what I told Sean first but then I ran by Matt and he's like why not know. YOLO yeah basically. No way dude no no no no. No.

### You (2026-04-09T14:26:42.832Z)

Good yeah.

### Guest (2026-04-09T14:26:44.429Z)

No.

### You (2026-04-09T14:26:46.032Z)

Glad we ran a bayou.

### Guest (2026-04-09T14:26:49.309Z)

That's a bad idea like all right so MCP access if it's read only okay fine if we're gonna say all right we give it we set up MCP we set up an MCP server for wordpress and you can read data. I don't see a problem with that at all. But we also have salmon AI. Right like we already have an MCP server that has all the WordPress content so we don't you wouldn't need it for content necessarily.

### You (2026-04-09T14:27:19.712Z)

So.

### Guest (2026-04-09T14:27:21.389Z)

And and then there's the whole thing about security well I guess we could like build the off system around it. Because we block everything that's outside of course as of yesterday we block everything outside of vpn. What are you using it for what's the use case what's the MCP doing just adding records basically so like instead of. Not not adding a new spouse it's adding a record for an Es so it's creating you know adds new and filling out details that it found and pressing save if that's the same draft yeah. It saves a draft and then it updates it yeah basically ideal world of paying you know some slack saying hey you know this is.

### You (2026-04-09T14:28:08.432Z)

Urce.

### Guest (2026-04-09T14:28:10.029Z)

Saying.

### You (2026-04-09T14:28:11.232Z)

Again.

### Guest (2026-04-09T14:28:12.829Z)

You know proved this and say and save the draft in WordPress. You're gonna use AI to do it like AI is gonna go and look up the details and create the ETF automatically.

### You (2026-04-09T14:28:23.952Z)

I already set up a skill that was pretty much doing the the research aspect and then I would just fill it in manually and so we just figured we'd take it a like one more level up but it's you know if it's too like that was one of the things that I was thinking of too like one thing that I never wanted to connect claude to was the WordPress just because it has access to so many things but I think I think if we limit it and just you know add all the guardrail.

### Guest (2026-04-09T14:28:30.989Z)

Yeah. I think if we. Build we could build that probably like we could society like all right here's the MCP is the ETF MCP for wordpress and then you get an API key and then you hook it up to claud and then it can. Write in it only allowed to like that MCP only allows you to create drafts. And there you can go and approve it. Seems like that seems like a lot of work for the you know cost savings or the effort savings here so that's the only like what were you guys thinking as far as what you would do for alternative alternative like the main point is going in everywhere and looking at all the different sources so we already we already can utilize the skill to pull all that info so this would just be like another you know step forward but that it's easy to just have a lot of work for you and then you just put it in yourself I'm saying like well you guys have a club Max subscription you get co work so you could literally log into wordpress and then tell it to do it and it will use your browser you can use browser use and fill all the stuff in for you. If you want to go that route like if you just want to like automate that there's a here's your skill you did a research go to wordpress fill it in it'll fill it in for you maybe I miss I didn't connect didn't describe it right when I first was describing this idea that's that's what that's what we had I think oh.

### You (2026-04-09T14:30:27.952Z)

Have you do you have do you have success using claude when you have your VPN on? Because every time I try to use it with a VPN on it. It just like doesn't connect like it just has issues connecting to anything.

### Guest (2026-04-09T14:30:38.909Z)

I never had an issue with the VPN though.

### You (2026-04-09T14:30:41.632Z)

Okay yeah I'd be down to test that out because like in the past whenever the VPN is on claude doesn't work. Or like when I've tried to use like claude in chrome just like testing it out it just doesn't it's like blocked.

### Guest (2026-04-09T14:30:57.309Z)

I I've actually. I always use cod. E like let's see. Working on it. No it doesn't it doesn't have a problem I just did it now I connected to the VPN and it's fine like unless it's an issue like connecting with the browser.

### You (2026-04-09T14:31:20.592Z)

Yeah all right yeah I'll run some tests because yeah that that's what I've been using for my own personal work is CLUD and co-work just going to town.

### Guest (2026-04-09T14:31:29.709Z)

Using our dedicated VPN server.

### You (2026-04-09T14:31:30.592Z)

So. So I'm using yeah yeah but I'm talking about like I have my own personal clodge and that's what I would use for just like day to day work but I haven't I haven't set up the.

### Guest (2026-04-09T14:31:33.549Z)

Right. Yeah.

### You (2026-04-09T14:31:45.232Z)

I've been set up the Blocks clawed yet I have to do like a. I have to split it up between like. Claud Block and claude personal on for cloud code so once I do that then I'll be able to start messing around.

### Guest (2026-04-09T14:32:04.589Z)

I mean it wouldn't be too hard to make the MCP server really want to go that route but like if you're already doing automation if you're already doing automation with cowork then what's the gap like what's the what's the real gap here because you're achieving the same result just a different way.

### You (2026-04-09T14:32:24.432Z)

I think we just need to run some tests just to make sure that it works. Because I was also looking into splitting up like the only thing that I can use personally when splitting up a claude Block and claud personal is claud code like you're not able to have two separate desktop apps or co-work apps. So it would like it would mean that I would have to like log in and log out to switch it up so but if that if that's the case.

### Guest (2026-04-09T14:32:49.549Z)

Oh you have like a purse so you have like your personal cloud account and you have like your block cloud account.

### You (2026-04-09T14:32:54.752Z)

Yeah.

### Guest (2026-04-09T14:32:56.109Z)

Okay. Gotcha.

### You (2026-04-09T14:32:59.792Z)

I already looked up how to split it up but when I looked up how to use like the desktop app it doesn't allow you to switch unless you like completely log out. Yeah I'll keep on messing around.

### Guest (2026-04-09T14:33:12.349Z)

Okay like if you're using cloud code you can you can install the playwright skill.

### You (2026-04-09T14:33:17.792Z)

Yeah.

### Guest (2026-04-09T14:33:19.869Z)

And use the playwright and then you can tell it to basically write a playwright script that says go to this block go to rvp go to our thing go to our site our etf do the research and then these are the fields and that's more precise as well so probably be even out there because it'll know all the fields beforehand.

### You (2026-04-09T14:33:40.192Z)

Yeah.

### Guest (2026-04-09T14:33:41.149Z)

And it'll be fast so it's almost like a semi automation but using AI.

### You (2026-04-09T14:33:45.312Z)

Yeah.

### Guest (2026-04-09T14:33:46.109Z)

You could probably even extend that you could extend your current skill to use the playwright skill and then like a one time effort of going into finding all the field names and button names and then say all right now run playwright and do all these things and then it's all in one shot and it can do that headless too like so all you got is connect to the VPN log in go to the ATF and then like there's I guess a million ways to do it but you know if you guys want to do the MCP for it. It'll probably take like a day to build and test out. If that's really if it's really worth it. Now be.

### You (2026-04-09T14:34:25.872Z)

I think tested it out with cloud code would probably be the easiest route just we just have to make sure that it's secure and that there's all the guard rails are in place and then like I'll test it out on like my own personal thing. Yeah. And so yeah. But yeah the MCP we were just thinking oh I was thinking that mainly because you like you have the connectors in claude and it's like one of the options so I wasn't sure if you've ever used that before.

### Guest (2026-04-09T14:34:56.269Z)

Never built the MCP for WordPress for our WordPress installed before. So that wouldn't that would involve like going to word press and extending like building new endpoints and then exposing like MCP protocol endpoint there and then allowing and then making like a tool for. For ETF creation and verification, which I don't know yet I'm sure php has some libraries out there for building mcps. I'd be happy to take it on honestly I got a bazillion projects and what's the bazillion plus one? I don't care like I'll build it out if y'all really want it.

### You (2026-04-09T14:35:34.992Z)

All right I think. I think we'll run some tests and then we'll get back to you because yeah I don't want to keep on adding to your project list but if if it if you don't mind and we end up like needing it. But yeah we'll keep we'll keep you posted we we mostly just wanted to run it by you and get your thoughts on it in the first place.

### Guest (2026-04-09T14:35:54.269Z)

I mean I think it's safe as long as we build it out right like it's probably even more dangerous to do the automation than to write like a very fine tuned MCP that just says, hey, you can only do this thing and it's really, you know, carefully done the NCP has no like escalated access so. But if you do like a playwright script it could accidentally go and create a post or something.

### You (2026-04-09T14:35:57.632Z)

Yeah. Yeah.

### Guest (2026-04-09T14:36:19.869Z)

You know. So.

### You (2026-04-09T14:36:24.192Z)

All right.

### Guest (2026-04-09T14:36:24.349Z)

Yeah.

### You (2026-04-09T14:36:25.392Z)

All right cool man yeah we'll keep you posted whether or not we're going to move forward with it. But yeah we'll let you know we appreciate it dude.

### Guest (2026-04-09T14:36:36.509Z)

I'll set up a draft PRL let me know if you want to test it out.

### You (2026-04-09T14:36:38.992Z)

Hell. Yeah all right you're the man thank you. Later.

