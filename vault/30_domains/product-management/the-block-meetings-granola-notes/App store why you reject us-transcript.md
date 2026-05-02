---
granola_id: 2c98c9af-ee2a-4f89-8a35-bf49e791116c
title: "App store why you reject us - Transcript"
type: transcript
created: 2026-04-30T15:29:15.667Z
updated: 2026-04-30T17:34:31.823Z
attendees: 
  - mvitebsky@theblock.co
  - erupkus@theblock.co
note: "[[30_domains/product-management/the-block-meetings-granola-notes/App store why you reject us.md]]"
---

# Transcript for: App store why you reject us

### You (2026-04-30T15:30:27.463Z)

How to do?

### Guest (2026-04-30T15:30:27.756Z)

Sean. What up boys?

### You (2026-04-30T15:31:04.823Z)

That? Mane?

### Guest (2026-04-30T15:31:07.436Z)

Sean you in yet?

### You (2026-04-30T15:31:08.983Z)

Not yet. I'm waiting for it.

### Guest (2026-04-30T15:31:10.716Z)

Jesus.

### You (2026-04-30T15:31:11.703Z)

I'm waiting for it to because I kept on doing it so many times. I honestly think I was being rate limited, so I was waiting 24 hours until I tried to Google voice phone number again.

### Guest (2026-04-30T15:31:24.636Z)

Alrighty. Ed what are you working on? Trying to basically force merge it because it was still waiting for a unit test I don't know we did an update since yesterday. All right copy ghlogin ghauth login. Open a new terminal.

### You (2026-04-30T15:31:58.823Z)

We have the Block's GitHub login information.

### Guest (2026-04-30T15:32:04.076Z)

Yeah it's your personal accounts I made you admins on the repo.

### You (2026-04-30T15:32:06.983Z)

Oh nice. Okay. New, there you go. And do Claude.

### Guest (2026-04-30T15:32:31.436Z)

No don't do cloud here give me.

### You (2026-04-30T15:32:32.663Z)

Oh no.

### Guest (2026-04-30T15:32:33.996Z)

One second now we don't want cloud here. Give me a second I log into github I want to make sure you're an admin. Do you think we should record this call just in case. It wouldn't hurt? Okay. All right type that ghauth login into the new terminal. Enter yep. Https. Yes why. I log in with the web browser. In the code. Yeah I gave you a code there on this terminal. Oh thanks. I have to confirm access and it's another six digit X field. I have to type in the same thing again no this is not the same thing. My passport but in my password.

### You (2026-04-30T15:35:29.223Z)

Do you have the mobile app?

### Guest (2026-04-30T15:35:35.996Z)

I don't think so no but I think it was I just had it saved in my passwords I think it was some sort of like token or whatever attached to my profile. Like a like a pen I guess so I think I'm in right yep. So now tell your authenticated. Yeah cool let's go to apple connect. Let's see what they got right what they got wrong. All right go to app review in the left hand menu. All right. So they have a few things we need to fix. Okay the support URL provide an app store connect is a dead URL I just put that in without actually checking it so we need like an actual contact URL. Looking for one. Thing we should note it down for a future or we need to like find it right now. If we don't have a contact email we just have to make one in WordPress. And just put it live and then you can update I'll show you what updated if you don't want it to be like contact. We have info at the Block. Currently put. I don't trust that now. We need it needs to be a website it needs to be a URL. Go ahead and click. It again oh yes. So basically for 1.5 we just need to make a website that's like a support website where they can you can literally just have a website that has like an email contact here for support. With they need to see something. Okay so the next one is about the pop-up that says ask give permissions app to track Sean you've seen that a million times. The app does have it I got cute with it where I only had it pop up on the second session so the second time you open the app clearly apple does not like that so this is a fun one for claude to do. I would literally just copy this entire guideline 2.1 in and be like we set it up to fire on the second session can we change that to fire on the initial session? Obviously we should wait until. Yeah. Okay 2.5.4. Basically there I have put permissions to have background music they couldn't find where in the app we have background music. So for this one we just need to reply with. How they can get to like the podcast and then listen to app and then. Switch the app off and the podcast will play in the background so you just have to give them like a clear direction on how to test this. Oh interesting.

### You (2026-04-30T15:39:38.903Z)

So you would just forward them like you would show them the path to get to the podcast essentially.

### Guest (2026-04-30T15:39:45.036Z)

Yeah basically just give them exact instructions in text. Here's how you attest this portion. How do we like is this is there a reply or something how do we communicate oh this one? Yeah. Okay that's the background noise what's this? So we need a way to delete accounts this is another one for claude this will be super easy for clot to do. Yeah somewhere in the profiles it gets just going. And nuke it. Do we need to. Like. Show them what we did like obviously with this one with the testing background noise that makes sense with all the other things like how prescriptive do they have to be in the reply. I would just say like guideline 5.1.1 fixed here's out of test. Makes sense. Okay and then they have some questions. So I would answer for now like number one. We are not offering any paid content subscriptions or features in the app that may change in the future. Two again we are not offering any paid features subscriptions or anything in the app that may change in the future. Three same answer. Same answer. Five no users cannot purchase physical goods. Trying to get that money yeah so this is what I would do is like fix those two things with claude. Upload the new build. Submit the new build. But then remember to reply to this. Before so we submit the bill would you mean to apple for review or no. Yeah so fix those which happens first. Fix everything with claude. Yeah. You guys test it make sure that the delete works you have the privy login now so you can literally go and privy and create an account. Through the app delete the account make sure it's deleted in privy. Make sure that asks to track thing pops up on the first session so that's kind of Ed when I was saying on the simulator you want to delete the app so you get that first session again perfect example of. Like when you'll need to use that to test so for this make sure it pops up on the first session. I would always like make sure it like pops up like when you are done with onboarding like you don't want to bombard people with like the things before they actually like get into the app so you can time when that triggers or have it like when you land on home screen. And then archive it. Submit a new build for release for public release and then reply to this email. Hey, just submitted the build. Here's the testing instructions for each thing. Here's the answers to the questions. Thank you very much. Try to fix one of these things? Seems easy enough. What's happening right now here? It's saying that it's. Doing it. Yeah, but you can you can send in a new thing to do. So let's let's test one of these things out. All right we wanted to do the. URL. That's the tracking. Yeah. Delete in the tracking so whichever one you want to tackle. Let's do the leash and. This one. Right. Yep. Copy that. And put that in and then type. Apple is requesting that we utilize account deletion for authenticated accounts. Can you help me create a deletion path through pip privy? I would make sure just specifically authenticated. You can't do that. You have to use your keyboard.

### You (2026-04-30T15:44:29.783Z)

I had a question about. I noticed like all the, there was like 24 branches in there. How have you guys been working with this? Have you guys been working. Like through branches and not pushing to main like, I don't know, or are those just like old. Deprecated branches? Okay.

### Guest (2026-04-30T15:44:47.836Z)

Yeah. I think main is the latest they're all.

### You (2026-04-30T15:44:50.343Z)

Okay.

### Guest (2026-04-30T15:44:53.036Z)

I'm not very good with GitHub.

### You (2026-04-30T15:44:56.343Z)

Yeah, honestly, this is all new to me. I've just been like playing around, like just hopping from my PC to my Mac. So I've been using PRs and stuff like that. So it's good practice.

### Guest (2026-04-30T15:44:56.556Z)

So.

### You (2026-04-30T15:45:07.943Z)

But I also, yeah, it's kind of confusing.

### Guest (2026-04-30T15:45:11.436Z)

Yeah. I'm not good at it at all. Mike actually gave me instructions on how to tell claw to do it properly.

### You (2026-04-30T15:45:20.183Z)

Yeah, I kind of want to make a slash command just so that. It does everything automatically just so it like does the fast forwarding and rewind, whatever the fuck.

### Guest (2026-04-30T15:45:35.836Z)

Edie you're actually doing like a major feature here. Dev ed.

### You (2026-04-30T15:45:45.143Z)

And Matt, can you send me what Mike sent you about the GitHub? Like how to do it properly?

### Guest (2026-04-30T15:45:51.436Z)

Yeah.

### You (2026-04-30T15:45:51.463Z)

If you still have it.

### Guest (2026-04-30T15:45:51.916Z)

I have to find.

### You (2026-04-30T15:45:54.023Z)

Yeah, if not, no worries.

### Guest (2026-04-30T15:45:54.476Z)

Let me pull it up. Found it.

### You (2026-04-30T15:46:05.543Z)

Thank you.

### Guest (2026-04-30T15:46:25.036Z)

Says why I do dangerously skip permissions. I literally tell claude like hey I'm going out for dinner. I'll be back in three hours get as much done as possible. And if you have permissions, it can't do anything.

### You (2026-04-30T15:46:39.463Z)

Yeah. Have you ever tried the phone? The what is. Like when you're able to put it on your phone? What do they call it? Oh, dispatch.

### Guest (2026-04-30T15:46:49.516Z)

I haven't. I don't really need to be on the move and clotting.

### You (2026-04-30T15:46:53.303Z)

Yeah.

### Guest (2026-04-30T15:46:54.236Z)

Any separation of church and state.

### You (2026-04-30T15:46:56.663Z)

I'm with you. I think the whole purpose of it was to essentially like do what you're doing. Only people don't realize you could do dangerously skip permissions.

### Guest (2026-04-30T15:47:11.276Z)

Doing. Moving in the right direction. Ed are you clear on the first one for the contact page? Yeah we just need to offer a way to then to contact us so in the app somebody would press contact us and that would lead them to the URL. Where they would be able to see an email. Yeah. A little time. Just returning back to our conversation that we had in the slack after our meeting yesterday. I honestly think you should sit down with Mike because he'll give you such a better GitHub explainer than I ever can. That makes sense I just. Was just trying to think if I was thinking about this correctly. And. Like there's nobody else who's like working right like if you know I merge main from my local just directly without creating a branch. Technically everybody else has to op main right to make sure that we're having the same root code. Yeah and then if their local is different you'll they'll have claude kind of merge the two. They'll take your changes local changes. But yeah the only people who are going to be working on this app are you two and mike so just coordinate with Mike. And that specific thing about the passwords or the secrets. That that get that contains all the API keys. Right. Yeah, so typically what you would do is you would host it on the back end and have the app point to it. Or like a website point to it. Which we do have so don't worry about that but locally you have to have them. Got it okay that makes sense.

### You (2026-04-30T15:49:13.703Z)

Yeah and you can set up something called.gitignore. So when you have it local you like whatever's in the dot get ignore that whenever you push to github those. Yeah.

### Guest (2026-04-30T15:49:28.396Z)

Is in the dot get ignore. Got you okay so the thing that you pushed they emerged right before we met yesterday. We have to do something with the secrets. Was that just like some fix or whatever you don't remember.

### You (2026-04-30T15:49:45.863Z)

I do. Because you you had the secrets in the where did you when you downloaded the secrets did you put it right into the. Local folder?

### Guest (2026-04-30T15:49:58.396Z)

Me.

### You (2026-04-30T15:49:58.583Z)

Yeah.

### Guest (2026-04-30T15:50:00.076Z)

Yeah, he did. Oh, but I it should be in the git ignore regardless because he downloaded from GitHub. Let's make sure the secrets aren't in github. Okay. You got three options. Where oh these okay. I don't. Love. Either. On any of these. Options. Let me see what privy offers. All of those seem like a lot of work. Okay this seems a lot more straightforward. So according to privy stocks. You should be able to. Just send this. So I should say previous docs say that we have this. Yeah, you can use the delete function through the API and paste that. Because there is a back end auth on the block side but mike hasn't hooked that up yet so I don't think any of these options would. Really make sense does this sound good? Yeah. There's no getting our file this is secrets xconfig template yeah that's not the real secrets. Yeah and if it was here it would show up right here right. If we had. The secrets file here.

### You (2026-04-30T15:52:54.903Z)

Correct? Yeah if you if you put it into the root yeah.

### Guest (2026-04-30T15:53:00.556Z)

Okay. Security check. Service. All right seems like you need mic I would copy basically. Those two options and then send Mike a message for apps or approval we need an account deletion process which one do you want to go with? Now you're collaborating as a dev. All right. Store this tell to store this to memory and we're going to switch gears. Store this like stored this work stream to memory I'm going to work with my back end dev let's move on to something else. And then let's move on to. The don't track thing. So copy paste the dump track thing. Brother what is happening here? Is not virtual. It'll figure it out. Let's go back to app store. All right. What was the first one. Or the second one. This one app. Of the tracking of the yeah. So you so you can just sort of like start piling tasks one on top of another for it's not like two different cli's that it's that it happens no so like it just said I'll save the workstream memory and surface where the merge stands so when Mike gets back to you just be like resurfacing conversation on delete function and then whatever his reply was and it just finds it like that based on the context. Well I just started to memory. Okay all right well let's start with this one just copy paste it. And then basically yeah add the details of like. We are right now triggering it on second session can we trigger it now on first session once the user finishes onboarding? On the second session or like the second page. We're currently triggering it on the second session what apple wants first session so after user finishes onboarding when they land on the homepage where it's like all the news that's when should trigger. And then copy paste it. Tell it I let you want it to be after user finishes onboarding because otherwise it'll do it like it'll put it first. And then paste it. There's you can't like do paragraph breaks right is there a way no just literally paste it doesn't matter.

### You (2026-04-30T15:57:24.583Z)

And if you ever do you could just do shift. Shift enter.

### Guest (2026-04-30T15:57:28.956Z)

Did you send that thing to mike by the way? You want to do that before the context window fills because then you'll lose all this. But give them some details like apple won't accept the app unless we have a delete function.

### You (2026-04-30T15:57:53.703Z)

The. Cell. And also.

### Guest (2026-04-30T15:57:55.356Z)

To your resumes.

### You (2026-04-30T15:57:59.303Z)

Chat. The way that.

### Guest (2026-04-30T15:57:59.836Z)

I already build an app.

### You (2026-04-30T15:58:00.263Z)

You set yourself.

### Guest (2026-04-30T15:58:03.196Z)

You said what was the last thing you said?

### You (2026-04-30T15:58:04.023Z)

Up.

### Guest (2026-04-30T15:58:04.876Z)

I already built my new company an app.

### You (2026-04-30T15:58:07.223Z)

What?

### Guest (2026-04-30T15:58:07.436Z)

You did?

### You (2026-04-30T15:58:07.623Z)

How?

### Guest (2026-04-30T15:58:09.276Z)

Yeah.

### You (2026-04-30T15:58:10.023Z)

For for what though like what is the app?

### Guest (2026-04-30T15:58:12.636Z)

I can show you real estate.

### You (2026-04-30T15:58:13.383Z)

Please.

### Guest (2026-04-30T15:58:16.476Z)

Dude I'm just seeing red everywhere here what's happening oh no this previous that's the previous never mind sorry. My screen. Let me let me move to that I'd like on the main tabs open now.

### You (2026-04-30T15:58:25.863Z)

Yeah. How did you get your screens to the left?

### Guest (2026-04-30T15:58:35.596Z)

It's a setting I don't know which setting it is.

### You (2026-04-30T15:58:38.823Z)

An apple setting? An iMixer okay.

### Guest (2026-04-30T15:58:40.876Z)

Yeah. Apple setting just screenshot my page and ask chat GPT how did he get it to the left.

### You (2026-04-30T15:58:42.823Z)

I like that. You're not you're not wrong. That's what I would do it like I would watch YouTube videos and then people have like a specific thing I'm like I would just screenshot it like what is this?

### Guest (2026-04-30T15:59:05.756Z)

So basically it's an app for real estate agents on the ground to basically do. Intake like property listings so like right now the way that property listings work is very agent to agent there's no standardization so basically adding like a layer standardization. So I'll do my home from childhood.

### You (2026-04-30T15:59:25.703Z)

Morning. My question. Is. I don't. Think so.

### Guest (2026-04-30T15:59:54.796Z)

Pretty straightforward but basically takes like a manual process and just puts it in an app so the data is all standardized. One cool thing you won't see on. The simulator version is I created a lidar feature that lets you create a floor plan and a 3D map of the property that doesn't work on the simulator. That was the fun part.

### You (2026-04-30T16:00:21.863Z)

What did you use the Google Maps 3D simulator or like. Their.

### Guest (2026-04-30T16:00:31.516Z)

14 and up has a lidar sensor. So you literally use the camera and the lidar sensor to create a 3D map. Apple has like software that stitches it together and then it also software that creates a floor plan.

### You (2026-04-30T16:00:44.823Z)

Health.

### Guest (2026-04-30T16:00:46.636Z)

It's pretty fucking cool. Yeah that's this is like nothing sexy. Yeah, so you can take photos like if you're an agent. Like going through the person's home you can be snapping photos. But what is cool is I built end to end communication offers to be able to like negotiate with the buyers here. But they are very hyped on it.

### You (2026-04-30T16:01:28.103Z)

Oh yeah.

### Guest (2026-04-30T16:01:31.516Z)

Well. Connected that to. This front end. So agent. Creates the listing. I'm an investor. I can now see the listing. I didn't submit that one, but I can now see the listing. And then I can talk to the person.

### You (2026-04-30T16:01:57.063Z)

What up though?

### Guest (2026-04-30T16:02:01.196Z)

So this is all just within like losing track what's just your app date greater than what's the actual already product. So I created a web app and iOS app and they talk to each other. Gotcha. Wow. So this is this basically would be like equivalent of red fin or. Yes sort of. This is for off market properties that aren't going to hit those. They have like their own investor network and their own agent network. Gotcha. So you're not coming after. Zillow or the reference. There it is. Communication.

### You (2026-04-30T16:02:56.903Z)

I'm able.

### Guest (2026-04-30T16:02:59.836Z)

That whole thing. Huh coded the app Vibe coded the back end Vive coded the website there's also a whole slew of admins stuff that I've coded.

### You (2026-04-30T16:03:12.183Z)

To the back end you don't use like. Youe're not using like a cloud service or anything like that.

### Guest (2026-04-30T16:03:19.836Z)

Of course there's like a bunch of backend APIs that have to talk to each other to make all of this work as an ecosystem.

### You (2026-04-30T16:03:22.343Z)

Okay. Gotcha.

### Guest (2026-04-30T16:03:27.356Z)

So there's the property I just created. I'm able to review it here. Can improve it. And put it on the dashboard. I can edit it. I can send it back to the agent. There's the photo I uploaded.

### You (2026-04-30T16:03:43.463Z)

Pretty.

### Guest (2026-04-30T16:03:46.476Z)

I can send it back to the notes. So yeah that's what I built for them.

### You (2026-04-30T16:03:52.263Z)

Oh. Yeah.

### Guest (2026-04-30T16:03:54.156Z)

That's awesome. What other. Like inefficiencies are you guys trying to target with like. With this app? Or just like. It's all very sounds like it's very rudimentary so far. Like you know that's why they need a lot of help. From VMs. Yeah they have no tech basically so I'm coming in and giving them tech there. Make money hand over fist. They literally told me they're super profitable despite having the shittiest deck.

### You (2026-04-30T16:04:24.103Z)

Oh my god.

### Guest (2026-04-30T16:04:25.196Z)

So good tech. And maybe we can make maybe more money. And it goes haywire here. Yeah for sure for tomorrow. I think a lot of like non us people have holiday so I'm not sure how many people will show up. But probably nice if you could. Showcase like the stuff you're creating. I don't know if you're comfortable with that. For what showcasing what? Tomorrow for our like standoff meeting. Like showcasing the new stuff. Yeah like I don't know like what you're working on or whatever. I want to show it I'll probably just talk through it. Yeah okay just just so I know like I think it's a holiday for quite a few people. So if people don't show up it's not because they don't love you.

### You (2026-04-30T16:05:25.943Z)

They're just too sad.

### Guest (2026-04-30T16:05:29.756Z)

All right looks like it fixed this. There you go what's the what's the proper way now? So I should just create a branch now. Right now you should test this locally for sure. Why send something to github that then you know someone's gonna have to review and you don't even know if this works yet. So test it local first so I would ask this is a new feature so I would ask it to do a minor version bump of the app then go through Xcode. Clean build it onto your simulator see if you can get a torque on your simulator. And we we instructed with claw to do like 2.3.3 right. And then that that would appear on Xcode. Yeah so I would just say minor version bump build one. So like. I just kind of taking a while to get used to this. Once you get used to this it's like I can have I literally usually have like four separate projects running like two apps two websites that I just have all my windows open it's going back and forth between them how long before your whole wallet is just screens and you have multiple unlike big days I'll have like my second screen kind of like how people have like their like trading charts and shit I'll have it all just clods sort of working on different nice okay all right let's let's let's see how you do an Xcode. Okay bumped both changes are sitting on stage. For the pushes yeah don't push it until you feel confident in your local. Got it. So clean the whole thing right. And then change where it says any iOS device to iPhone 17. And then build right yep. All right I'm gonna go to the bathroom while it builds. Fair.

### You (2026-04-30T16:08:04.103Z)

Now that you're getting. No pun intended a vibe for how all this shit works like what were some of the like. Matt made that thing for the charts like what were some of the ideas that you had. That you would want like as an app or a web app.

### Guest (2026-04-30T16:08:29.116Z)

Oh where's the Block app.

### You (2026-04-30T16:08:32.023Z)

Lic and scroll to the right.

### Guest (2026-04-30T16:08:37.836Z)

Doesn't look like it's ready. There we go it's almost ready yeah. We can chat about that after we're done with this for sure.

### You (2026-04-30T16:08:49.063Z)

Cool.

### Guest (2026-04-30T16:09:04.316Z)

All right so you didn't get a fresh load so hit the home button. The home button the up top. Delete the app so long press it. No long pressed app noob apple user. Now press play again clean and play. So it's supposed to show. The tracking right. Yes.

### You (2026-04-30T16:10:06.743Z)

Similar. Back. Ground. And. That was like.

### Guest (2026-04-30T16:10:14.316Z)

This little shift that happens okay Josh designed.

### You (2026-04-30T16:10:14.583Z)

Two years ago. So. I always hit a. Theater. In five months. Tomorrow.

### Guest (2026-04-30T16:10:23.436Z)

Do I need to sign up no we're not really right regardless. Okay boom. Dev. Is that what it looks like on your on your guys's end too yeah every app has this.

### You (2026-04-30T16:10:39.783Z)

Which is. That.

### Guest (2026-04-30T16:10:45.436Z)

It's called a system prompt you can't change how it looks.

### You (2026-04-30T16:10:47.463Z)

Year. Too. Hard. To. Be.

### Guest (2026-04-30T16:10:50.716Z)

Okay. Bada bing bada boom sir.

### You (2026-04-30T16:10:52.183Z)

Said.

### Guest (2026-04-30T16:10:53.996Z)

Now you can. All right so you fixed one of the two I have to wait for Mike to help you with the second one create the contact page fill out the questions and we're good to go.

### You (2026-04-30T16:11:06.103Z)

Like.

### Guest (2026-04-30T16:11:07.436Z)

All right I gotta run.

### You (2026-04-30T16:11:10.423Z)

Later brother.

### Guest (2026-04-30T16:11:25.916Z)

Yeah definitely to meet Mike to. Like. Get a best practices. Feel on GitHub.

### You (2026-04-30T16:11:36.823Z)

I was gonna say getting a github 101 would be ideal especially because like. Like I feel like I know most of what the devs are talking about but then it's just like when it comes to enterprise when it comes to just. Working with a lot of developers it's just over my head so I would really want to know what it's like.

### Guest (2026-04-30T16:11:56.396Z)

Yeah. I think that this should be like a contact us here. What do we load on this oh you actually load this. Below this looks like the full page downloads. Like iframe of the web page.

### You (2026-04-30T16:12:33.223Z)

Oh yeah.

### Guest (2026-04-30T16:12:33.436Z)

I don't know.

### You (2026-04-30T16:12:40.823Z)

Like because directly direct directly from WordPress.

### Guest (2026-04-30T16:12:41.516Z)

Okay. To answer your question. Like for ETFs for example it'd be nice or like. Let's say we call that app. Not app it would be a URL right you put in your. In your I think it's called an app technically right like because it's like. I don't know I don't know the terminology the vernacular that it's supposed to be used but you get a URL just like it has for the data dashboard for the data charts right put in the URL. This thing drops down. Loads and you have three different options let's say like ideally we have one for prices one for. For like for tokens one for ETFs and one for crypto stocks. And we have like a predetermined set of like fields that need to be. Filled out with. For each of them. And then. You have a query. It's like which you know what what token needs to be added or what like asset needs to be added so we put in the asset. And it whatever is able to. Fill out without. The actual. Like API, you know like for some of them you need an API access to pull information. So we could skip that. Show a flag that you need to have. Access to the API like whatever whatever go to go to confluence page you know to find that all that info but then the rest of the stuff is filled out. That's. The that's the vision that I see for like an automation tool. Where I don't need to like. Go to coin gecko and get the token address for a specific chain like all that stuff is just so. Like I don't know like that would mean that would need to connect this app to our cloud essentially right because it would have to the answers are. Being generated by claude because we're telling it to find the answers. Right. How does this.

### You (2026-04-30T16:15:12.023Z)

But that that is doable. It's just.

### Guest (2026-04-30T16:15:15.996Z)

Right.

### You (2026-04-30T16:15:17.303Z)

Yeah honestly we can we can map this out and get that done we would just have to get all the API the necessary API keys. And it would be able to do because it's not like we're trying to sell that it's for us to use like.

### Guest (2026-04-30T16:15:30.476Z)

But we don't have we don't have apis with our subscription because apis and cowork are separate two separate things. So we don't have apis with cloud.

### You (2026-04-30T16:15:42.103Z)

No but.

### Guest (2026-04-30T16:15:42.236Z)

Like if you want to.

### You (2026-04-30T16:15:43.783Z)

But you can give Claude the apis that. You're that you need like the like give Claude the API keys like for these like coin gecko and whatever else and you just store it in the secrets yeah then you could just because unless you're trying to give it company wide it sounds like it would just be for you and I to use.

### Guest (2026-04-30T16:16:04.716Z)

Yeah just like I'm always so scared of like. Doing this shit and then like we running out of credits. You know it's like the time gecko for example yeah, but like how would it pull the information that's. I don't know like trading your chart how would you like the URL how would it pull that?

### You (2026-04-30T16:16:30.983Z)

Web search. Or you can give it.

### Guest (2026-04-30T16:16:33.756Z)

Right but how but how how would how would that info show up on. Or you need an API from like the cloud all right so generate the answer for you. Because. All my all my sort of like. Ideas that I've had. With automations require like actual I think in co-work if you build a skill that probably is a lot more doable because cohort directly just like searches it for you like it wouldn't when it works within your local when you have an app that's a URL that's like. Youe know accessible by anyone who has the link or you know has the VPN on kind of like how Matt has it then you need. That then it just uses the API from the. From the cloud account that's how it fetches the answer. And we and the API for cloud is not is not included in the. Subscription that we have I was I was surprised actually to see that.

### You (2026-04-30T16:17:37.383Z)

Yeah because when you do the subscription and like the APIs are like. Like the whole point of the subscription is yeah exactly.

### Guest (2026-04-30T16:17:45.196Z)

Add-ons.

### You (2026-04-30T16:17:47.143Z)

Because like when you do the APIs like strictly like it can rack up so that's why they were just like all right yeah 200 bucks in for. Like this amount of time you do get a lot more with it but it's just.

### Guest (2026-04-30T16:17:59.276Z)

Yeah.

### You (2026-04-30T16:17:59.383Z)

Yeah. When you combine it with everybody at it could definitely rack up but again it's not like. It's not like you'd be using this every single day. And it would just be you trying to use it.

### Guest (2026-04-30T16:18:18.636Z)

I just I don't I have no idea what like we haven't even discussed like club API things. So if anything probably for us for our purposes. What you had showed me with like the skill that probably is. Like. Good enough. You know if it's not your eye who's doing these updates. Would have to the person would just have to like set up clock for them get authenticated with our company account and they just download the skill and upload the skill and then they are able to do the same thing. So if anything it's just perfecting that skill. We I guess then then to rephrase myself instead of it being an app we just have three different skills whether whether it's co-work or whether it's.

### You (2026-04-30T16:19:08.023Z)

Yeah.

### Guest (2026-04-30T16:19:11.916Z)

With with co-work probably would make sense that if you we went for the full WordPress. Like. Authorization but let's not do that let's just. Let's not go crazy especially with like so many things changing like a big mistake like that couldn't just be. Horrible for all of us involved so I just erring.

### You (2026-04-30T16:19:37.863Z)

There is. There is something I do want to test I'm not going to test it with Block stuff. But like codex and cloud code have computer use now so it's similar to like web like like browser use or clotting chrome but computer use it literally just takes over your computer and has its own mouse and it's able to click and point and like so one of the things one of the possibilities would be to. Like copy and paste the WordPress shit that it like finds. So I'm going to test on my own stuff and see how well it works and then if it does work and it's only going to get better as time goes on. But that could be part of the automation right now it's obviously not necessary but I'm just I'm just curious.

### Guest (2026-04-30T16:20:24.316Z)

Yeah yeah definitely do those it's beneficial to just stay on top of it.

### You (2026-04-30T16:20:28.903Z)

Yeah.

### Guest (2026-04-30T16:20:29.356Z)

But I think for now like our automation for our automation projects like skills. Are good enough.

### You (2026-04-30T16:20:38.183Z)

Yeah. For sure. And and the way to like make those skills better is by like if you want to make multiple instead of instead of just trying to combine one huge skill it's like you can have them react to the other so it's like run the skill and then at the bottom of that skill it's like after that like go to this skill and then it'll start it'll like read that exact so it'll be like a chain reaction.

### Guest (2026-04-30T16:21:01.916Z)

Pained yeah gotcha.

### You (2026-04-30T16:21:03.143Z)

Yeah.

### Guest (2026-04-30T16:21:05.996Z)

Okay. Yeah. It's not a huge priority for us cuz like. There's not that many things that are being added so it's like not. I would say like documentation probably for us is most pressing. Like keep running into it more and more now. Okay. I don't think I'll let's just I should probably do. A branch here.

### You (2026-04-30T16:21:41.863Z)

So it's done.

### Guest (2026-04-30T16:21:42.316Z)

And just continue working. Yeah it finished the tracking like obviously we tested it and it works. So that part of it's done but now we need the on tact. Contact page. I'm actually surprised that we don't have a contact us page. Let go.

### You (2026-04-30T16:22:05.463Z)

Yeah, I would just ask Mike well because I see you sent it in there. So you can you can create a branch but you could also just like wait until.

### Guest (2026-04-30T16:22:19.356Z)

And just keep it all in local.

### You (2026-04-30T16:22:21.303Z)

For now yeah until he responds because you don't want to create a like you don't want to keep on creating branches just to merge. For the same for the same apple problem that you have on your computer like once mike responds and you'll be able to get an answer unless you respond saying that I'm just going to take care of this on my end. So I would just hold off until you get a response from him. But if you feel antsy then you can just go for it.

### Guest (2026-04-30T16:22:49.116Z)

Yeah how is stuff usually works. Like. Technically if you. Look to protect this sort of like file you know security if. My system were to just crash obviously everything that's in local what they. Write so I wonder how. They again that's we probably just need to sit down like and talk about this stuff.

### You (2026-04-30T16:23:15.783Z)

So one of the things if you if you have git. If you have git installed which you do because you're using github then you can just commit. Yeah we'll look into it but there's there's two different things there's like commit and then push to github like push commits to github because like the whole point of git is just for it to track like any of the changes so like that usually happens almost automat.

### Guest (2026-04-30T16:23:42.076Z)

Oh because yeah because I could do it to my own right I could do you could push it to my own thing not not the org.

### You (2026-04-30T16:23:43.063Z)

Ically. Yeah.

### Guest (2026-04-30T16:23:51.116Z)

Gotcha. Got you got you got you okay.

### You (2026-04-30T16:23:55.383Z)

Because like it kind of like it'll track it like you you could say push to github or commit to github like yep let's make sure we're doing the right one and then you'll see like a string of numbers it's like okay this was pushed to git or committed to git and then that's its own like your computer can crash and then you can start it back up and that that string of numbers will still exist like it'll still like it's like almost like it's memory. And yeah another another best practice is do you have like a hard drive running like at all times that like kind of. Does like backups for you?

### Guest (2026-04-30T16:24:39.356Z)

Like an external hard drive you mean.

### You (2026-04-30T16:24:42.263Z)

Yeah.

### Guest (2026-04-30T16:24:52.636Z)

I don't have that well I actually do have that but I don't have it connected. Okay so what do you think I should do now should I just like leave it as is and just like hot leave this work in the background I don't know what the is to it here what it's like stuck on here maybe it takes a while. The initial urge. It's been it's been like it's been on that for the whole like. The whole time we're working.

### You (2026-04-30T16:25:28.823Z)

I think it's just waiting for you it's waiting for your approval. Commit push these changes.

### Guest (2026-04-30T16:25:39.196Z)

That's that's in regards to the actual build that we just did. But.

### You (2026-04-30T16:26:23.303Z)

Like when whenever you do have questions. You can just. Ask it like have a conversation yeah just. Yeah what do you mean by that how data is this message like what. Like the github message that Matt sent.

### Guest (2026-04-30T16:27:02.796Z)

Yeah it's entered at the beginning of a call.

### You (2026-04-30T16:27:05.303Z)

Yeah that's just that was the best practices thing that he said to give to Claude yeah.

### Guest (2026-04-30T16:27:56.316Z)

These things here okay. Just do option one. Now we're like building on top of it to like getting confused like how much how you like. You're not gonna merge any stuff that you just did.

### You (2026-04-30T16:28:37.223Z)

Another thing to do is like what would you recommend like I made the changes.

### Guest (2026-04-30T16:29:22.636Z)

Oh no meeting with Matt R101. Okay I'll. Be post on all the sentence but then yeah. We'll have you had any success on the transcript or no.

### You (2026-04-30T16:29:37.863Z)

Yeah I have everything I'm putting everything together and making it. Legible because like right now it's kind of all over the place.

### Guest (2026-04-30T16:29:47.036Z)

Yeah let's talk about it on our one-on-one later.

### You (2026-04-30T16:29:47.063Z)

But. Sweet.

### Guest (2026-04-30T16:29:51.596Z)

I seem a bit.

### You (2026-04-30T16:29:52.023Z)

Oh good. Man. Good. So I got the. One on. That. One. Taking. The chicken out. This. Grandpa. To. Bang back.

