---
granola_id: ac0b9d4c-255c-4224-8a60-14c18d99fbf6
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of ios training - transcript.
context: the-block
created: 2026-04-28
source: granola-sync
attendees:
  - mvitebsky@theblock.co
  - erupkus@theblock.co
note: "[[30_domains/product-management/the-block-meetings-granola-notes/iOS Training.md]]"
---

# Transcript for: iOS Training

## Attendees
- Matt Vitebsky (mvitebsky@theblock.co)
- Ed Rupkus (erupkus@theblock.co)

### Sean (2026-04-28T18:31:03.354Z)

2.

### Guest (2026-04-28T18:31:11.476Z)

You see in that list of the GitHub repo.

### Sean (2026-04-28T18:31:14.394Z)

Yes. Secrets, what's needed. And we had access to the Block Pro API key this whole time. I didn't realize.

### Guest (2026-04-28T18:31:38.036Z)

Oh, yeah.

### Sean (2026-04-28T18:31:38.634Z)

I thought it was something that Mike had to give us.

### Guest (2026-04-28T18:31:42.996Z)

Well, I think if you have. The pro subscription, you can generate an API key.

### Sean (2026-04-28T18:31:50.634Z)

Yeah, just so.

### Guest (2026-04-28T18:31:51.876Z)

Like.

### Sean (2026-04-28T18:31:52.874Z)

You could do that, you can get the news, you get data. All right, cool.

### Guest (2026-04-28T18:31:52.916Z)

Right. Yeah.

### Sean (2026-04-28T18:32:00.874Z)

Yeah, when I come, when it comes to the other things. I do not have like a privy. Oh weird.

### Guest (2026-04-28T18:32:14.916Z)

What up, gents?

### Sean (2026-04-28T18:32:16.234Z)

How's it going sir?

### Guest (2026-04-28T18:32:16.676Z)

Hey. Hey. I was ready to build some iOS apps. Web code. I gotta teach you everything. I want to record this. Yeah, we should. Okay, cool. Who is going to be doing most of the work?

### Sean (2026-04-28T18:32:47.514Z)

I mean, I'll take it on.

### Guest (2026-04-28T18:32:50.916Z)

It's probably helpful to for both for both of us to know. But I want someone to drive. Okay, you go ahead, Sean. You're probably more comfortable anyway. All right, before we get started, can you guys actually send me your Apple ID so I can make your admins? Would that be just the email? That. I write under your name? You got. Just give me an email, actually. It'll work. Actually, give me a. I'm gonna send it to your block email just to make it secure.

### Sean (2026-04-28T18:33:49.114Z)

Okay. My black email is not associated with my Apple ID. Does that matter?

### Guest (2026-04-28T18:33:56.036Z)

It doesn't matter. This is just for logging into the App Store connect. Okay, Sean sent you years. Ed sent you years. Let me know when you guys are in. Am I receiving anything?

### Sean (2026-04-28T18:34:25.754Z)

Yeah. Same.

### Guest (2026-04-28T18:34:28.116Z)

Check your spam. To. Rupkus. Europe gets the Blocko. S Winslow at the Blocko. I believe I got your emails right. Yeah. That's correct. I wonder why it's not coming. Why it says no apps for you in all apps for Sean. That's weird. All right, well, we can come back to this, hopefully during the time of the meeting. It'll come back. All right, Sean, you got cloud CLI and Xcode installed. All right. You want to share your screen? Did you accept the GitHub invite? I did.

### Sean (2026-04-28T18:35:53.354Z)

I cloned the repo as well.

### Guest (2026-04-28T18:35:56.036Z)

I already cloned it. Beautiful.

### Sean (2026-04-28T18:35:57.434Z)

Yeah.

### Guest (2026-04-28T18:35:58.836Z)

Many steps ahead. All right.

### Sean (2026-04-28T18:36:01.354Z)

But once I got it, I wanted to play around with it.

### Guest (2026-04-28T18:36:04.036Z)

Okay. Perfect. Can you go to this folder in your finder?

### Sean (2026-04-28T18:36:10.474Z)

On. Can you see my screen? I don't know what the fuck.

### Guest (2026-04-28T18:36:15.956Z)

I can see your anti gravity.

### Sean (2026-04-28T18:36:16.234Z)

Oh, there we go. All right, cool. So what did you say? What did you want me to go to?

### Guest (2026-04-28T18:36:21.156Z)

Go to the project folder in your finder. Okay. Run a terminal there so you can run cloud. At the very root of it.

### Sean (2026-04-28T18:36:38.474Z)

Oh, you want the terminal up? Not anti-gravity.

### Guest (2026-04-28T18:36:42.116Z)

Yeah, just right click on the block app iOS folder, and then you can run a terminal there. All the way at the bottom. New terminal folder. All right, start clot up. Beautiful. I actually just uploaded some new files, some new docs for claude so you can start over. Or you can start where I left off. Can you ask it to pull the latest from git? You may have to.

### Sean (2026-04-28T18:37:25.594Z)

Docks or.

### Guest (2026-04-28T18:37:27.076Z)

Just the latest push or the latest merge from github. They'll probably ask you to log into github. Okay, you actually have the latest.

### Sean (2026-04-28T18:37:51.834Z)

I was gonna say I did it. Like 20 minutes ago.

### Guest (2026-04-28T18:37:54.996Z)

Okay. Perfect. All right. In there you are gonna have. A. What. Is it called? Can you ask it to read the handoff MD? So you don't have the latest? One second. I might have not.

### Sean (2026-04-28T18:38:37.674Z)

I was gonna say, when did you do it?

### Guest (2026-04-28T18:38:40.436Z)

Like 10 minutes ago. And now my cloud's down. Amazing. Okay. It's back up.

### Sean (2026-04-28T18:38:56.554Z)

You don't use any IDEs. You always use the terminal.

### Guest (2026-04-28T18:39:00.596Z)

Xcode is an ID.

### Sean (2026-04-28T18:39:02.394Z)

Okay.

### Guest (2026-04-28T18:39:10.676Z)

Sorry. I'm gonna ask you to pull it again in a second.

### Sean (2026-04-28T18:39:14.234Z)

Sure.

### Guest (2026-04-28T18:39:19.476Z)

ID stand for development environment. What is I. Is it internal or something?

### Sean (2026-04-28T18:39:31.834Z)

No,

### Guest (2026-04-28T18:39:34.116Z)

Interactive?

### Sean (2026-04-28T18:39:37.354Z)

I forget.

### Guest (2026-04-28T18:39:39.636Z)

That's interactive.

### Sean (2026-04-28T18:39:45.754Z)

Integrated, integrated development.

### Guest (2026-04-28T18:39:56.036Z)

Sorry. It's making me log into github. One second. What the hell? Don't tell me I'm in the wrong GitHub. Sorry. Should have done all this before the call. We're doing a live.

### Sean (2026-04-28T18:40:43.674Z)

Doing it live folks.

### Guest (2026-04-28T18:40:47.156Z)

Why is this? I have no access to the repository. You've been. You've been tossed already? So it seems like. I don't know if Mike could do that to me. I. Might not allow it in here.

### Sean (2026-04-28T18:41:29.914Z)

Do you need the Block's password and everything like that? The login credentials? For their GitHub.

### Guest (2026-04-28T18:41:36.356Z)

No, because I'm an admin. It's telling me that I got rejected.

### Sean (2026-04-28T18:41:41.754Z)

Oh boy. Got Mike on the horn.

### Guest (2026-04-28T18:41:46.676Z)

Yeah, for. Real.

### Sean (2026-04-28T18:41:48.954Z)

Up and I got the. Developer, Apple developer email.

### Guest (2026-04-28T18:41:54.516Z)

I got it. All right, make that account while I. Do this. Did we get your Z? Let me check real quick. Yep. Okay. Yeah, sign up right now.

### Sean (2026-04-28T18:43:11.114Z)

As yours taken a while to load Ed.

### Guest (2026-04-28T18:43:13.716Z)

Yeah.

### Sean (2026-04-28T18:43:14.554Z)

Same.

### Guest (2026-04-28T18:43:40.756Z)

Loading for you guys? No, it's just stuck in the. Loading Loop.

### Sean (2026-04-28T18:43:47.194Z)

What is that supposed to give us admin access to?

### Guest (2026-04-28T18:43:50.596Z)

Store connect where you actually upload the app. Well, that is on Apple. Are you guys on the VPN?

### Sean (2026-04-28T18:44:00.634Z)

No.

### Guest (2026-04-28T18:44:02.516Z)

I turned it off because I was having issues with the. Yeah, let me start it. Should. Should we be on the piano? No, sometimes Apple gets weird on vpns.

### Sean (2026-04-28T18:44:27.594Z)

Try incognito?

### Guest (2026-04-28T18:44:45.316Z)

Is it different? You don't know? That is unfortunate. Okay. Let's see what we can do without it. Can you go back to. The folder?

### Sean (2026-04-28T18:45:07.594Z)

Which folder?

### Guest (2026-04-28T18:45:08.596Z)

Like the finder folder. All right. Double click on that bottom file. Dot Xcode project. Okay. Beautiful. This is Xcode. I just fetches all the things in the nav bar. This is how you test the app locally.

### Sean (2026-04-28T18:45:57.674Z)

You did the back end with. Everything's Firebase?

### Guest (2026-04-28T18:46:03.796Z)

No, the back end's connect guitar back end. Firebase is for analytics. What's one signal? That is the push notifications. I'm about to do something very insecure.

### Sean (2026-04-28T18:46:26.154Z)

Until we roll.

### Guest (2026-04-28T18:46:29.556Z)

I'm most excited. I just don't give a anymore. All right. That's the secrets file with all of our keys. Download that.

### Sean (2026-04-28T18:46:50.874Z)

It downloaded.

### Guest (2026-04-28T18:46:54.596Z)

Okay. Throw that into the root directory. Beautiful. All right. Your app should work perfectly. Then. You should, like, it's going to ask you to do that. You should log into GitHub. Just click always allow. It's going to ask you, like, six times. It's really annoying. Like, you have to put your password in. I don't know why it does this. But it's not just my computer. I always allow you a couple more times. Yep.

### Sean (2026-04-28T18:47:30.554Z)

Yeah I've done this before. I thought like. Felt like I was on acid at the amount of times that I had to do it. I was just like.

### Guest (2026-04-28T18:47:40.676Z)

I thought my computer was bugged, but I'm glad to see that it's everyone's computer and Xcode. I always allow, always allow. There you go. All right. Now let's go back to Xcode. Still grabbing stuff.

### Sean (2026-04-28T18:47:57.594Z)

How big.

### Guest (2026-04-28T18:48:00.676Z)

So what you've done is basically. Set up, Sean, to have the. Whole. Like. Context of all the code on his local. Exactly. And you need that to push new updates to Apple store connect. Like, it's just coming from. Not that I'm super knowledgeable in that, but applesauce connect stores it as a compiled app. So it basically takes all this. And makes it into, like, one single app where, like, if someone outside of the company downloaded, they can't see everything that goes into it. Interesting. I'll walk you through how to, like, actually compile it and send it to Apple store. Edish might as well do this, too. So you have it on yours.

### Sean (2026-04-28T18:49:03.274Z)

Yeah, so was everything. Was I know what everyone's waiting for the iOS app store like we're like waiting on that to be pushed and everything like that. So. What we're doing now like is essentially. I don't know like what are we doing with the Apple store? If it's not already on there?

### Guest (2026-04-28T18:49:30.196Z)

Well, you'll need admin access to make any updates to it in the future. And you'll need it locally if you want to make any updates to the app itself. So basically, the test flight is in there, the one that we all have. But if you want to make any changes to it, you have to do it here in cloud and Xcode. And or in anti gravity doesn't really matter. And then push that back up to the app store. So I didn't. Clone it. I just downloaded it from GitHub, right? Just to. Unzip it and then do the same thing. New terminal in folder. Click on the X project. Got a star cloud first right after opening the terminal. Yeah. Okay. Your app is done. All right, Sean, hit command shift K. That refreshes. Context. Yep. Clean it. And then click that play button at the top. So this is going to run it in a local simulator for you.

### Sean (2026-04-28T18:51:13.834Z)

Simulator. Up?

### Guest (2026-04-28T18:51:15.556Z)

So basically the process is if you make a change with cloud or anti-gravity whatever it is. You always clean the environment because that deletes, like, any old code. And then you click that play button again. So that's going to load whatever changes you made into the simulator. So fresh canvas. Exactly. It's like clearing the cache on a website. I'm fetching the. Packages. It'll take a while, as you saw with chance. Yep. Oh, well, that's cool. Ed, now you can pretend like you have an iPhone.

### Sean (2026-04-28T18:52:00.794Z)

I was gonna say yeah Ed what are you using your PC or are you using the.

### Guest (2026-04-28T18:52:05.796Z)

I have a Mac. Yeah, Matt was able to get me to switch to Mac device, at least for the laptop.

### Sean (2026-04-28T18:52:06.154Z)

Mac.

### Guest (2026-04-28T18:52:12.516Z)

And have you looked back? No, I'm not. No. All right, look at this. You have the app. So go ahead. And sign up or do let. Maybe later. Doesn't really matter. You have to still fill out. You have to agree with the terms. All right. Do you see an Xcode? Go back to Xcode. You see that console down there? Yeah. Perfect. So this is all the logs. This is like if you're gonna go into dev tools on. On a website and view the console. So basically, if you're trying to do something with cloud and it's not working the way you want it, ask it to add logs. And then just basically copy paste, you know, this stuff into cloud so it knows, like, what's. What's going wrong. Sometimes these are like thousands and thousands of lines and it'll eat a ton of context. So, like, I would click the garbage can. On the bottom right. And then let's go back to the app. Let's say, like, something's broken on data. Let's go into the data page. Let's click on one of these charts. Say the chart doesn't load. You would go back to Xcode and basically just copy like that more recent piece into cloud and be like, this is what the logs are showing me.

### Sean (2026-04-28T18:53:38.154Z)

Gotcha?

### Guest (2026-04-28T18:53:42.196Z)

Okay, let me see if my shit's done. It's still not done.

### Sean (2026-04-28T18:53:47.514Z)

What are you are you still trying to log into GitHub?

### Guest (2026-04-28T18:53:50.436Z)

No, I've logged in. I'm pushing a branch to main, but it's running through mike's tests right now.

### Sean (2026-04-28T18:53:56.874Z)

Got. Cha?

### Guest (2026-04-28T18:53:59.796Z)

Okay, so you have the app. Do you know how to push an app to. The store?

### Sean (2026-04-28T18:54:09.514Z)

No I've never done that before.

### Guest (2026-04-28T18:54:12.116Z)

All right. Let's have some fun. Ask claude to update the version number of the app or update the build. Rather, let's do for now.

### Sean (2026-04-28T18:54:22.154Z)

Update the build.

### Guest (2026-04-28T18:54:23.476Z)

So. Yeah, so new feet. So basically, the way that app, the App Store works is you have a version number, and for each version number, you can have any amount of builds. So basically, if we're, like, launching a new feature, you update the version number. And then every, like, attempt at, you know, testing it, sending it to QA or sending it to the company, whatever. You upload the bill to, like, the first one would be build one, something goes wrong. It's still the same feature we're working on. Then you update it to build two, and that's how the Apple store. Kind of identifies it. So let's do update the build. You don't have to do it within next code. Let's do it.

### Sean (2026-04-28T18:55:03.914Z)

Oh no.

### Guest (2026-04-28T18:55:15.716Z)

Oh, no, it's not doing what I want it to do. Click X out of this. Or stop it.

### Sean (2026-04-28T18:55:21.674Z)

Stop it.

### Guest (2026-04-28T18:55:22.916Z)

Yeah. Tell it to update the build number. Of the app. Well, all of that. To change. One to two.

### Sean (2026-04-28T18:56:08.954Z)

Making big moves man.

### Guest (2026-04-28T18:56:19.236Z)

Are you able to log into apple?

### Sean (2026-04-28T18:56:24.954Z)

It's still loading.

### Guest (2026-04-28T18:56:33.556Z)

That is. If you try to open it safari. No, it doesn't seem to work any better. What the. Come on, apple. I'm gonna try to resend you guys the invites. Okay. Boat should have new invites now. All right, so you bumped the version. That's great. So we're at 2.3 build number two now. So the app store will see this as a unique build. So you'll be able to play with it in test flight. The only issue is you need to log into apple to actually be able to upload test. Ball problem. Yeah, but for now, let's try to make a change to the app. Let's go back to the app. What's a small change we can make right now that we can notice but won't up the experience. At a different category for learn articles. What do you mean by that? I don't know. Filter. You have the three different. If you scroll the top. You have the three different ones there. What do you want? The new filter to be? Just some take things. Are you. Are you saying, like, we shouldn't. We shouldn't do anything that's like would appear like a bug. I mean, we could always undo it, but let's make, like, an actual feature enhancement because beginner intermediate advanced from the API. Gotcha. Let's do. Let's just change that text at the top. Yeah. So take a screenshot of this. There's a screenshot button. Yep. Pull that into claude. This is why I like working with the CLI. It's much easier to pull things in.

### Sean (2026-04-28T18:59:29.194Z)

Yeah do you have to do. Command.

### Guest (2026-04-28T18:59:35.876Z)

No, no. Don't pull it into the project folder.

### Sean (2026-04-28T18:59:36.074Z)

Or.

### Guest (2026-04-28T18:59:38.356Z)

Just pull it straight into claude. Whichever claw you want it. You can just drop screenshots.

### Sean (2026-04-28T18:59:43.274Z)

Okay I see what you're saying.

### Guest (2026-04-28T18:59:43.636Z)

At the. Concept. So tell it. On the learn page. Can we rewrite the H1? And then whatever you guys want to change it to momentarily?

### Sean (2026-04-28T19:00:07.274Z)

What is it right now?

### Guest (2026-04-28T19:00:10.676Z)

If you read it. There? On the app. If you go to the app itself. Go to the. App. So let's learn about all things Bitcoin, ethereum, defiant. Yeah. Put xrp after ethereum.

### Sean (2026-04-28T19:00:29.994Z)

We rewrite the h1 to.

### Guest (2026-04-28T19:00:32.276Z)

Include. After mentioned ethereum. So, like. So. Like. Different. And, like, groundbreaking where you don't need to be as. Like. Prescriptive with commands is you could. You would always have to be, like, super correct. And, like, trying to. Tell it what it needs to do. And now it's like, just. You could just tell it words, and it's, like, understands what you're trying. Very natural language. Now. This looks so bizarre to. Not that I learn. Previously. But.

### Sean (2026-04-28T19:01:17.274Z)

Yeah no it doesn't take much it kind of just figures it out like you could be as vague. As hell and it'll just be like it'll try to figure it out.

### Guest (2026-04-28T19:01:25.716Z)

It's not. Were you using the company? Credits or your own or your web coding list? I just expense the credits. Like, how much did it cost to, like, build the whole thing? $400. Wow.

### Sean (2026-04-28T19:01:46.314Z)

Use the API the whole time.

### Guest (2026-04-28T19:01:49.156Z)

Yep.

### Sean (2026-04-28T19:01:49.914Z)

Oh. I also. Just realized I forgot. To cop. Y the. Rest of the team on them. I replied to. So I. M sure.

### Guest (2026-04-28T19:02:01.796Z)

That is the right way to do it. But for now, let's just do hard code. So it even tells you when you're being stupid. Wow.

### Sean (2026-04-28T19:02:38.154Z)

You can. Take it out.

### Guest (2026-04-28T19:02:39.236Z)

The little. Thinking words spelunking. Pontificating.

### Sean (2026-04-28T19:02:45.754Z)

There's something called tweak cc that you can like edit all this so you can make it whatever the hell you want. Pontificating. Blubbering.

### Guest (2026-04-28T19:03:04.276Z)

Everybody's. Everybody's creating value somehow there.

### Sean (2026-04-28T19:03:13.834Z)

Excited to. Dive into this. I know we.

### Guest (2026-04-28T19:03:15.316Z)

What is it doing now? It's.

### Sean (2026-04-28T19:03:17.594Z)

January. But. If it's been a lot. Going on.

### Guest (2026-04-28T19:03:19.556Z)

Like the app can. It'll, like, try to run the app in its environment to make sure that there's no errors. Like clock code is doing it itself. Before.

### Sean (2026-04-28T19:03:35.594Z)

With. A.

### Guest (2026-04-28T19:03:37.316Z)

We try it and it fails for whatever reason.

### Sean (2026-04-28T19:03:39.994Z)

One. Thing. About.

### Guest (2026-04-28T19:03:41.716Z)

Wow.

### Sean (2026-04-28T19:03:43.114Z)

Just.

### Guest (2026-04-28T19:03:43.316Z)

So. So you could even. You could cloud code could not see, like, any errors or whatever, but then you do Xcode. You're trying to push it to the. To the thing, to Apple.

### Sean (2026-04-28T19:03:43.434Z)

Trying to.

### Guest (2026-04-28T19:03:54.436Z)

Store, whatever. And it's. And it could be erroneous. Yeah, it happens. I wouldn't say it's, like, often, but I'd say, like, probably 10 to 15% of the time, it'll miss something, but it's better than usually cash more than it misses.

### Sean (2026-04-28T19:04:10.794Z)

Have you tried the new codex Matt like with five five.

### Guest (2026-04-28T19:04:15.236Z)

I've been. I've been doing some smaller projects on it. It's definitely very good. But I have, like, all my history. And context and clawed. Okay.

### Sean (2026-04-28T19:04:26.634Z)

They came out with a plugin that you can add to claude so it's like if you have your chat GPT login you could just still use everything through cloud. Yeah seven to. You.

### Guest (2026-04-28T19:04:42.036Z)

Hello, Wars. Everyone. Okay, so it just made the change. It's a talk me through how. What's our next steps to test it?

### Sean (2026-04-28T19:04:52.794Z)

I'd already made the change. So right now it's running so am I gonna have to clear the cache again?

### Guest (2026-04-28T19:05:00.916Z)

You're always gonna have to clear the cache. You don't have to stop running. Just do command. Okay, it'll stop it automatically.

### Sean (2026-04-28T19:05:02.714Z)

Yeah.

### Guest (2026-04-28T19:05:07.316Z)

You don't do. Don't ask next time. Studio don't ask. All right, so close the app for you. Clean succeeded. And now run it again.

### Sean (2026-04-28T19:05:15.434Z)

So command B when you do the.

### Guest (2026-04-28T19:05:17.956Z)

Command V to run it. Yeah.

### Sean (2026-04-28T19:05:22.234Z)

Particip. Ant.

### Guest (2026-04-28T19:05:34.116Z)

And if you ever want to test, like, a fresh install, so, like, say your testing features that are premium versus. Not premium, you would just literally delete the app from the simulator. So if you would right click on the app in the simulator and delete it. And then do again. Sorry. Can you repeat that again? If you want to do what? What do you do that for? So if you ever need a test, like, different states, like, say logged in versus, like, new account versus want to go through, like, the login flow again. All you have to do is delete the app from the simulator and then just click run it again. Pizza is a new download. Exactly. Okay, let's go to learn. Let's see if our change took place. Wow. All right, now I would tell cloud to undo that and just read from WordPress, but that was just an example of how it works. Yeah. So that's actually a pretty good segue, like what if you do something and it's like, ah, I made it worse than it was before. What's. You just go back and say, undo this previous change. Or. Yeah.

### Sean (2026-04-28T19:06:43.834Z)

Yeah yep. You ever use the rewind the rewind. Function in cloud. I've never tried that before.

### Guest (2026-04-28T19:07:00.276Z)

And just tell it to read from WordPress again.

### Sean (2026-04-28T19:07:04.874Z)

Except. Ion. And after this.

### Guest (2026-04-28T19:07:14.676Z)

I try to log into your apple again.

### Sean (2026-04-28T19:07:17.674Z)

Yeah. Ben. Stud. Io court. Check. S.

### Guest (2026-04-28T19:07:37.316Z)

I'm liking it.

### Sean (2026-04-28T19:07:37.594Z)

Out. Different. Teams. Different locations.

### Guest (2026-04-28T19:07:40.996Z)

Different email. Maybe. Try to create a developer account. And then let me resend it if it's.

### Sean (2026-04-28T19:07:56.714Z)

So. There are three. Bases.

### Guest (2026-04-28T19:07:58.116Z)

Married yellow in the background.

### Sean (2026-04-28T19:07:58.874Z)

Of. Catalog. The first. One was that.

### Guest (2026-04-28T19:08:04.676Z)

Really loud in the background.

### Sean (2026-04-28T19:08:06.314Z)

Oh sorry. I think she's in a meeting. I. Always have.

### Guest (2026-04-28T19:08:17.556Z)

Oh, well, I just signed it with my personal email, like with the Apple ID. No.

### Sean (2026-04-28T19:08:25.674Z)

But this.

### Guest (2026-04-28T19:08:25.956Z)

Should I try to do the. The Block email?

### Sean (2026-04-28T19:08:26.314Z)

Will be.

### Guest (2026-04-28T19:08:28.916Z)

Instead a new account with the block email?

### Sean (2026-04-28T19:08:30.794Z)

Nourished. And stronger. Too. Much of the. Cliff. Ribs or. Burn themselves. Out. There. So.

### Guest (2026-04-28T19:08:47.796Z)

God, this is so. Like.

### Sean (2026-04-28T19:08:57.354Z)

I. Ve been.

### Guest (2026-04-28T19:09:03.476Z)

How would this work then? If I have a different. I have no idea how this stuff, like, works on the back end with apple.

### Sean (2026-04-28T19:09:07.514Z)

Out. There. Not. Ifying.

### Guest (2026-04-28T19:09:12.116Z)

If I. If I'm logged into my personal Apple ID on my Mac on your computer, not on the website.

### Sean (2026-04-28T19:09:25.034Z)

The. Topic. To create a new apple. Present. Ing on. The uran I. Participated. In these. Conversations just. To get. These. Stigmatized. Gamma.

### Guest (2026-04-28T19:09:40.276Z)

Still not working.

### Sean (2026-04-28T19:09:41.594Z)

Members. More aware of. The different.

### Guest (2026-04-28T19:09:44.036Z)

I tried the new invite and didn't work. Okay. I mean, we can't really go any further until you guys are in the connect store, unfortunately.

### Sean (2026-04-28T19:09:56.394Z)

Yeah I think we have.

### Guest (2026-04-28T19:09:57.156Z)

Let me see if I can. Let me see if you can. If I can try after creating the.

### Sean (2026-04-28T19:09:57.994Z)

To.

### Guest (2026-04-28T19:10:07.156Z)

Work ID.

### Sean (2026-04-28T19:10:09.914Z)

Bring. These types of things for. Two of these that. Might be. The most. Ident. Ified as. Gas. For everyone. There. Working. Out that. They notice they. Don't have anything. Around. Which. Is our substitute. Program. Or. Care. Table family. I have no idea. Especially. For those that. Was one of the reasons. We'll see. That it's. To be profile. For. Quite little period. S.

### Guest (2026-04-28T19:10:50.196Z)

Yeah. Like, I think. I was trying to set up my Granol with her. New iPhone, and I think I was running into the same issue that you need to have a different phone number for different Apple ID, some like that. Like, so annoying. Oh, is that the step you're failing on? Yeah, it's telling me that I have to. Like, it's like 2fa.

### Sean (2026-04-28T19:11:14.554Z)

We. Do recommend.

### Guest (2026-04-28T19:11:15.476Z)

I'm trying to do the 2fa and it's not letting me do the 2fa with this specific phone number because my. My personal has the same phone number.

### Sean (2026-04-28T19:11:16.314Z)

A. Two part. Of health. Care.

### Guest (2026-04-28T19:11:25.796Z)

You got a Google voice.

### Sean (2026-04-28T19:11:27.994Z)

Prov. Ides a horizontal. And physical support.

### Guest (2026-04-28T19:11:29.716Z)

Google voice. That. I give you a number.

### Sean (2026-04-28T19:11:53.674Z)

Your. Leaders can start. To have a convers. Ation. That we. Have with all of this is. Available. In the event.

### Guest (2026-04-28T19:12:04.756Z)

I have noted that this thing was a thing. It's awesome. That's what I use for all my spam stuff. Here's how to. Well, I had no idea this was a thing. Yeah, it's pretty awesome.

### Sean (2026-04-28T19:12:25.514Z)

They're about having the two of the. Wicked and marriage. To violent.

### Guest (2026-04-28T19:12:28.276Z)

Okay.

### Sean (2026-04-28T19:13:04.554Z)

As. Well. As. The other. Background. Just. Getting. Those.

### Guest (2026-04-28T19:13:11.076Z)

John, you in. Are you still out?

### Sean (2026-04-28T19:13:13.914Z)

I'm still out trying to I just downloaded Google voice so I'm gonna try to make. Another apple ID.

### Guest (2026-04-28T19:13:23.796Z)

Google voice. Also very fun for pranking friends.

### Sean (2026-04-28T19:13:29.674Z)

Classic.

### Guest (2026-04-28T19:13:31.956Z)

Sean, I went to, like, two years ago. I was in actually Portland with Brittany, angel and Casey. And Brittany met some guy at a bar the night before, and I used my Google voice number to start texting. I was the guy. That are going for a while.

### Sean (2026-04-28T19:13:52.234Z)

Oh my god. It's him.

### Guest (2026-04-28T19:13:55.396Z)

That's funny. I was saying. I was saying some crazy.

### Sean (2026-04-28T19:14:03.834Z)

Like just like random dick pics on online that you found just like just like a giant giant hog it's like character.

### Guest (2026-04-28T19:14:11.396Z)

It did send online. Foot out the door. It won't put out the door. It doesn't matter. Strike the record, Gemini.

### Sean (2026-04-28T19:14:27.754Z)

We're gonna put this up on confluence how to build.

### Guest (2026-04-28T19:14:37.716Z)

Try on your phones, I suppose. Last effort to try to make this account. I don't know what the going on.

### Sean (2026-04-28T19:14:41.034Z)

A. Teacher.

### Guest (2026-04-28T19:14:43.236Z)

But it's a prerequisite to do anything else.

### Sean (2026-04-28T19:14:51.034Z)

Who makes. This release. Whatever. House. Just to make. Sure that there. S anything. Too.

### Guest (2026-04-28T19:15:00.196Z)

Well, I can't do it.

### Sean (2026-04-28T19:15:00.474Z)

For.

### Guest (2026-04-28T19:15:01.156Z)

Right? I guess I could do just interface.

### Sean (2026-04-28T19:15:02.074Z)

What. They. Re. In towards.

### Guest (2026-04-28T19:15:04.036Z)

Yeah, all you have to do is sign up on the website, so you should be able to do it.

### Sean (2026-04-28T19:15:04.714Z)

My. Work. On one. On-one. For. Team. Mates or. New fees. To prepare that. Kind of really. Exclusive platform. Yet. We do. Have those. Workshop.

### Guest (2026-04-28T19:15:19.476Z)

Apple.

### Sean (2026-04-28T19:15:20.794Z)

Numbers.

### Guest (2026-04-28T19:15:20.836Z)

App Store connect. S.

### Sean (2026-04-28T19:15:38.714Z)

And. But. In terms of. Next steps. I. Didn't want. To. Call. It. One. Step. One. I. Know we mentioned. Those two guys. Who. Made it courses. I just be curious. To see. What you're. Distributed to connect. To me. If. There was anything that I. Could. Share.

### Guest (2026-04-28T19:17:06.996Z)

So sends me. A verification to my work email. I try to put that verification number into the. Verified email address. Press continue. And it says verification codes can be sent to this phone number. Some sort of glitch. Like, I'm not even doing anything with the phone number. Lovely. Sean. You have the same issues.

### Sean (2026-04-28T19:17:35.994Z)

Yeah I think it's it's something that I have to like play around with try to figure out. Can we.

### Guest (2026-04-28T19:17:42.036Z)

All right. Why don't I schedule another, like, 45 minutes for tomorrow? And hopefully by that time you guys are both into apple.

### Sean (2026-04-28T19:17:47.994Z)

That works?

### Guest (2026-04-28T19:17:49.556Z)

Before we do that, is there any other questions about kind of what we looked at today?

### Sean (2026-04-28T19:17:58.314Z)

I'm personally good.

### Guest (2026-04-28T19:18:05.396Z)

It's like. Kind of. Everything for you. Just gotta sort of. Not let it go anywhere, I guess. Yeah. In the app's in good shape. It's, like, ready to go. Yeah.

### Sean (2026-04-28T19:18:18.634Z)

I. Think.

### Guest (2026-04-28T19:18:19.876Z)

All right, I'll put another hour on for tomorrow. I guess. Try, try, try again to get into apple. Let me know if I should resend the invites again.

### Sean (2026-04-28T19:18:32.794Z)

I. Prefer to see. Yeah send it send it one more time and can you also try to send it to. I'll send my Gmail see if that works.

### Guest (2026-04-28T19:18:42.356Z)

We probably don't wanna. Yeah, we probably don't want personal emails on the company account.

### Sean (2026-04-28T19:18:44.954Z)

No.

### Guest (2026-04-28T19:18:50.276Z)

I mean,

### Sean (2026-04-28T19:18:50.554Z)

Alright yeah.

### Guest (2026-04-28T19:18:54.276Z)

We will have. To. Account got locked.

### Sean (2026-04-28T19:19:00.154Z)

So far so good you might want to make it Thursday man.

### Guest (2026-04-28T19:19:07.316Z)

All right. Tell me by, like, I don't know, noon tomorrow if you guys still can't get into apple, and then we'll just do your personals.

### Sean (2026-04-28T19:19:14.234Z)

Okay. Cool.

### Guest (2026-04-28T19:19:16.596Z)

I don't really care about the security.

### Sean (2026-04-28T19:19:20.234Z)

I was gonna say we got. Yeah we got everything in slack.

### Guest (2026-04-28T19:19:28.196Z)

I'll schedule some time for tomorrow. I'll see you boys later. Thanks.

### Sean (2026-04-28T19:19:31.834Z)

Edmond. Bye.

