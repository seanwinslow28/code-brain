---
granola_id: 6ef614de-3fa4-4b12-9d80-bb2e1262f57b
title: "The Starting Block (New .co daily show) Data reqs - Transcript"
type: transcript
created: 2026-03-27T14:03:08.389Z
updated: 2026-03-27T14:29:25.099Z
attendees: 
  - bmendoza@theblock.co
  - erupkus@theblock.co
  - mprice@theblock.co
  - npivcevic@theblock.co
note: "[[30_domains/product-management/the-block-meetings-granola-notes/The Starting Block (New .co daily show) Data reqs.md]]"
domain: [product-management]
---

# Transcript for: The Starting Block (New .co daily show) Data reqs

### Guest (2026-03-27T14:03:10.012Z)

Overlays. So why we gather here is to basically discover how we can, what's the easiest path of setting it up with the specific, you know, data points that would anticipate having at hand. So I can share my screen. We could, I don't know, go through the, some of the few. Api settings that they have. Like, you know, like limits. And stuff. So we could just. Like, go through the. The basics of what this specific subscription. Gives us. So. Right now we have. The professional subscription. Which is this. 20, 000 API calls, 100 megs of data. That doesn't really tell me much. Because I don't know, like, what, what, what I guess we probably should start at what data we want to serve there. So. The main things that they have talked about. Where, like, if you can imagine a live stream with a ticker where the price is prices of specific assets are flowing. So that would be like, you know, our prices. From coin gecko or maybe even almax. At least for simplicity sake, let's keep it at prices. So, like, connecting our coin gecko data. To Showcase prices. Another one would be. To. Pull our headlines, basically, like all specific story that they, you know, if they want to talk about it, they put, you know, the headline or, or whatever else is available, author or something like that. And then data dashboard charts. So that's like one of the more important things. They would want. To surface, you know, like maybe have an overlay of a chart inside of the app. Or inside of the live stream and talk about it, basically. So. I'm not really sure where to. Start chatting about this. We, we have access to the. To this, to this dashboard. And basically where is the. Extra manager? Yeah. So you can create data streams here. And this is what it has. Like you, I guess this is like private token, public token. And you can. This is sort of like the. We're working with here. They always expose the private token. It's cool. It always annoys me, like, copy it now or you lose it forever. Okay. So what data are we sending from here? In the, the first things that they have pointed out where the. Like our headline, like, so basically our, our news API, I would assume. Because they would want to pull our. Our headlines, you know, like when the producer of the Daily show would want to set up specific stories that they're going to talk about. So, like, they want to pull in a few headlines. Right. So that's, that's one. Data dashboard charts. And not all charged just like some. Yeah. I don't know what, like, what's the.

### You (2026-03-27T14:07:23.650Z)

I'm guessing I would have to do with whatever they're talking about. At the time because what they're hoping to establish is a live, like they're doing a live stream, so they're hoping to get live data.

### Guest (2026-03-27T14:07:28.732Z)

Yeah.

### You (2026-03-27T14:07:35.010Z)

Just kind of immediately whenever they're talking about it. So a producer would be there able to essentially query the sapi and immediately get whatever they're talking about.

### Guest (2026-03-27T14:07:45.372Z)

That means you have to send everything over.

### You (2026-03-27T14:07:48.930Z)

Yeah, I guess we would have to see what their schedule is like to see exactly because I know they have an episode schedule.

### Guest (2026-03-27T14:07:57.692Z)

Like they can plan it, but, like, doing it live wouldn't be like, well, you need to talk to our API directly. You don't want to.

### You (2026-03-27T14:07:59.890Z)

Yeah.

### Guest (2026-03-27T14:08:05.612Z)

Like, pull everything at once. So you're saying maybe they plan everything in advance. Like, we're going to talk about this, this, and then they can go to WordPress and curate everything they're going to talk about. Right. Exactly. Okay. So there's like a flag or something in where Pressa says singular and then it sends it to singular. We synchronize it. We keep minimal data overhead. But, you know, they have that data there and then they're working out of singular with the data that they. Curated. Right. Or am I off? Do we have maybe like some. Like design work of how this should look? I think, I think I, this would kind of give us, because, like, for example, yeah, the Michael, what you're suggesting, like, for example, for if, if we're talking about articles and they handpick a few articles, I mean, they can cop if they are hand picking, they can copy paste this into singular or whatever. Right? Like kind of if, if it's like handpicked, if it's like a list of latest articles. Yeah, it makes sense, like to, to feed it because, yeah, you kind of, you press the button and you have it everything in singular. Copy and paste Jason or something. If they were to do that. But, yeah, I see what you're saying. Let me pull up this. There's some brief sketches that they have. Let me open that up real quick. And regards working, I think, like regarding token data. Yeah. Makes sense, like, to keep it live regarding charts. I'm not sure how are they going to visualize those charts because it's not just data, right? It's also visual, visual part. And maybe singular supports embeddings. So we can kind of embed a chart for the live stream. I don't know. So this is the, just like the schedule of giving show. But this is what it kind of looks like. So I guess that's the live stream. Right. And this is what they're taking inspiration from. You have headlines. So I guess technically you could just. Like. Copy that headlines. Not sure. Maybe it would be easier if you could select a few. Articles and be like automatically pulling. Because the, the singular app is basically a place where there's a design, somebody who's designed these black, you know, overlays. Combined, fills it in with specific data. So data. Right. So. And then it creates an overlay that you can just play on your video. And, and it's all just like one output. Basically. Gotcha. And that's just like going to change the different things as they're talking. Right. Like potentially. Yeah. Like if they have more than three things, they more than three headlines that they would like to talk to, you know, cover. They can just press this button and basically the next, you know, pop in. So kind of like a new show where, like, different things are showing up. Yeah. Yeah. And then there's your chart. So we need to send an image unless they can somehow render or embed. Then we need to send, like, an image of the chart over. Yeah, I was going to say getting, getting high charts on an overlay would be crazy because there's no point in rendering that when nobody's in a hover over and look at tool tips. So. No, no, no. Yeah. That little box is like a html enabled thing. And it can take an embedding, then that'd be cool. But other than that, yeah, we're going to send them an image.

### You (2026-03-27T14:12:04.450Z)

No, I think. I think that's what it is. It's. It takes HTML, CSS compositions and layers them over our video output in real time.

### Guest (2026-03-27T14:12:14.252Z)

Okay. We could link the embed, maybe, but I don't think rendering high charts natively is a good idea. No, no, that's not, that's not going to work. Yeah. So we send them the embedding and then they see that. And then, I mean, that could definitely. Okay, so I guess the other question is, like, how are they going? Is it, we were talking about bringing headlines back. Is this part of that? Like, are we going to bring back headlines for real? No, I, I don't, I don't think that's like the pro headlines they were thinking about. This is just basically. Like. The headlines of specific stories that, okay, are currently on. So handpicked. Yeah. It probably would be happening. So they, they have this. Like. I wish it was more like first in this platform singular. But the, like, if we go to. One of the. Best compositions, this is basically where you create stuff. It's very powerful. You can get. Wait, oh, I gotta share this.

### You (2026-03-27T14:13:27.410Z)

Have you guys ever messed with, like, after effects or anything like that? Any, like, motion graphic stuff?

### Guest (2026-03-27T14:13:34.812Z)

And I think the closest I have is obs. And that's. Yeah.

### You (2026-03-27T14:13:40.130Z)

Because, yeah, that's. I was going through some of the tutorials, and that's what it kind of reminds me of. Like, the whole idea is just after effects meets live graphics.

### Guest (2026-03-27T14:13:49.372Z)

Okay. Yeah. So, like, you create a specific, like, specific assets, I guess, and you connect them with data nodes. So I think in my head how I'm understanding is you have, like, a prices data node. So you'd have, you design a top bottom Banner that sort of, like, rotates. That would be one of them. Then you have, like, these charts. Like, maybe this is basically like a chart image overlay. And that one also, you know, glue go in and out. And then. Yeah, like something like a headline. Box. Where. You would connect data nodes to specific, like, stories that were handpicked. But again, like, it's hard to, like, visualize it how it would. What the workflow would look like without. Having an actual data to, like, play with. Gotcha. I would assume, like, we would essentially just. Like. Put, like, send all of our, of the articles. That, you know, basically, like. The real time news API. Entails. Like, am I thinking about it right way? I for the. If we, they have data sources, right? I'm sure that the data source can be managed here somewhere. Right. And it's kind of, you can populate it manually. I'm not saying, like, yeah, we cannot make the automation, but, like, if they are going in WordPress and or, like, not even in WordPress, they're probably going to our latest news. And they kind of handpicked, like, oh, I want to talk about this story. You know, just copy paste it there instead of, like, having to, oh, I find it now found the story. Now I have to go to WordPress, click flag, press update. Now, oh, they didn't sync in singular. And now I can use it in singular, right? Like, kind of feels like we are adding, like, seven steps instead of, like, you know, just, you know, copy pasting. You want to talk about. I don't know, just like kind of maybe I'm not understanding the, the whole flow, right, of, like, how they want to manage this specific page in WordPress, and they have access to some content. Like fields can, we have one ACI field for, like, posts, one for a data dashboard. Maybe the slug to load the PNG from. And just, like, maybe just one wordpress page with different ACFs and different queries. For the separate things that they want. Like poly market. I think that's a fair example of it. Yeah. So you basically have, for each shell, you'd have a different post. And you'd be able to schedule, like, handpicked headlines and pick the charts that you. Want to. Have ready. Right. Yeah. Try to be maybe, I'm pretty sure we have to look at how we handle the thumbnail structure, but I'm pretty sure it's like sludge or something. We'll figure it out. That might be a little tricky about it's doable. And then everything else. I mean, we could even just add everything from WordPress, which would be a benefit to that. Like maybe if they want to add election stuff, we could structure things there just from that same page. So, yeah, we're, we're, like, in a very much like the beginning stages of this whole thing and what this meeting together because, like, we just have to talk about at the same time so they can. Design can be informed what's possible so they can be informed what's possible to, you know, to pull in. So with this is definitely varies so much. You know, it's, it's, it's just forming the, the whole idea. Makeup of the show. Yeah. So that, that seems. It seems very doable. And one, one other thing that they, a small thing that they had mentioned was. Having. These, again, design components. You know how, like, when you're interviewing somebody, like a guest, you'd have their name and their, like, title. Below them. Like, that would appear on the sort of like, like in, in the news. I guess that could just be like another field in that same, that same post. They have, like, these people names entitled. Ready? In WordPress. You could just type in. Like. But my text. Does that make sense? I think, like, yeah, kind of what Brian suggested, like, if we have a dedicated page to each episode, right? Like, we can have, like, additional fields where, like, you can pick articles, you can pick charts, you can have, like, text that you want to, like, prepare in advance or something like this.

### You (2026-03-27T14:19:12.530Z)

Is that a pain in the ass to make numerous Pages on WordPress? For, like, just for this? Or is that. Is that just like a basic.

### Guest (2026-03-27T14:19:20.492Z)

I think it's kind of like you kind of create a new episode, and then you add, like, the stuff to that episode.

### You (2026-03-27T14:19:21.410Z)

Blocker? Yeah. Well, I was going to say, because it could also use Google sheets. So if that's easier and. And less work on. No.

### Guest (2026-03-27T14:19:38.732Z)

We've done that. We don't do that. It's probably better to build it in WordPress.

### You (2026-03-27T14:19:40.530Z)

Okay. Gotcha.

### Guest (2026-03-27T14:19:44.732Z)

Yeah. Having, because they might have, I think they should let us know at least if at least a bare minimum a week in advance if they want to add new things. So, like, if we have in WordPress, like, posts, data dashboard chart and, like, interview guest. And then they want to add a new thing, like news of the day or something, they need to tell us. Right? Because we can't just have a text. We can't just add text boxes or we can't have one text box that does it all. We need to, like, label it. So they should have a design, like a thing of all the potential things for all the shows and episodes. So we can have all the possible options. But, yeah, like the types of, the types of data that we want to show. Yeah. One day just like their episodes on Friday and on Tuesday, like, oh, we should have this. And then they don't have it on WordPress. Yeah. Jabs are on vacation. People are super busy with other stuff. Yeah. Yeah. So, so far, it's been four main things that, that at least I've been asked for. One is to have those PNG charts. The, the images of the charts. Two is the headlines. So just like basically being able to pull titles of our stories. Three is the price sticker that's flow along the bottom of the video. And, and fourth was the. Like, text field for, you know, people names that would be guests on the show. And their titles. I guess technically, like, like technically, that thing you could. You could go into this design. And, like, type it in yourself, I would guess, but that would mean have to change the design every single time for every single show. So it's probably easier to do it on WordPress. Yeah, that all sounds perfectly fine. My only question would be. I know this is, like, still super early in design. I'd love or we need to hear about the ticker and how they want it to be because that could be hard, depending on what they want. If they own a websocket ticker that's, like, scrolling. I mean, we could, we could do a poll every few seconds, but we need to see if they want, like, a ticker that's, like, scrolling and, like, updating every few seconds. Versus, like, one ticker that's updated at the start of the show, and that's it. But that could be complex. That could be super easy. But just something, you know, keep in mind. When they start, they do, they do support web sockets. Oh, that's really cool, actually. Yeah. I think, yeah, I'd shared the document. Yeah. Where they say, like, kind of like, yeah, you can, like, the simpler implementation is polling. But if you kind of really need really real time data and I think, like, kind of for, for like they kind of mentioned, oh, for sports or for, like, kind of sub a second, like precision, something like this. So maybe, like, we can go with polling, but, yeah, it's maybe a web sockets. Are sick. And also, just in case this has not come up, but I'm thinking about it and the way. Our, the way our revenue team works, it's very likely this could come up. If we were to put lmax price ticker on here. Would that be a problem? I mean, it's just an API, I guess, too, is the allow us to do it. And be fine. I don't think they're up. Yeah. Five to five or five California time. We're chilling. Sorry. I didn't get that. What is, what does that mean? The servers go down every single day. That's right. Forgot about that. You're the daily maintenance or something. Yeah. Okay. Yeah. Because I think their memory runs out. We don't get from coin gecko live updates every second. Right. So we get, we get, like, every minute. So we need max for, like, really per second updates. And they are not just. What was that? Michael? Oh, go ahead. No, unlock is super optimized. So maybe it's better we use that even just for, like, cache the API response because it's like 500 bytes now or 700 bytes. So in terms of, like, api limits, like, that'd be super nice. We're talking about using our API from lmax directly. Yeah. Proxy that we built. Yeah. Okay. Yeah, it keeps it easy. And I think, like, from, like, all the requirements, you said that I think, like, the ticker is the thing that we should focus on. Feels like that's the only thing that, you know, they cannot do without us, right? Like, kind of the other things. Yeah. You can prepare the names, the articles, the images, right? Like you can kind of prepare this before the show, but, like, the ticker. Have it really live. You can, can have this. Okay. Yeah, I think I. Think I have answers to the questions I had. I think next, next steps are just basically communicating to them. The. Outcome of this and, like, you know, what, what that experience would be like for each of these episodes. And then, yeah, I'll just get. There. Get their thoughts on the ticker. Yeah, I think it would be wise if someone, like from the engineering team would log in into the system and just. Figure things out a bit, like click around, see what's possible. Yeah, we can share. We can share keeper credentials. So no worries there. Any these, these. Okay. My only worry was I wasn't sure, like, if, if we have to worry about the limits. Probably not. Right, even if we fed per second, I'm not sure, like, how, how the, how it works, but, like, if we fetch every second. That's. 60 calls per minute. So it's. 3600 per hour. And it should last for one hour. Right. So I think we're fine. That's a monthly thing. Right? What's the rate limit on that? What's like the time?

### You (2026-03-27T14:26:31.890Z)

I think. Yeah, I think they want to do it, like, what, three days a week?

### Guest (2026-03-27T14:26:32.252Z)

Calls? Yeah, that's maybe five days.

### You (2026-03-27T14:26:38.210Z)

Five.

### Guest (2026-03-27T14:26:39.692Z)

Yeah, that should be fine. Yeah, 3600. That's. Yeah, 100 megabytes isn't that much. But. We're not sending that much data anyway. So even, like, our Price data is, like, super slim. So the ticker might chew through that, do the math maybe, but we'll be, we'll figure something out. Alrighty. Okay, I'll share. I don't, I don't know who, who would be the, the person, the point person from the dev team here. Would it be Michaela? I don't know. But it looks like WordPress stuff here. Mostly. I don't know. Unless Brian, you want to take this? I wasn't going to be doing the. What's it called? CTO thing soon? For the website. That's right. Yeah, that's right. That's right. Yeah, we'll probably get into this. And, yeah, there's no urgency here. So, like, I think we can just sort of. Yeah. Like, I can get more requirements and then we can spike a little bit, but, yeah, I need to finish translations first. Yeah. Yeah, for sure. I think the designs are still not even ready for. These. But this thing show. So I'm off. Next week. Yeah, that's fine. Do you have anything? Fun? Yeah, I'm going to Czech Republic. Nice. Meeting with Larry. Yeah. I'm not that familiar. Is Larry still in the Bahamas? I don't know. I was thinking of meeting Christoph. Kristoff is from Prague. But I'm not. I kind of. I was thinking of going to Prague, but change plan. So I'm just going to burn, which is like two hour drive from Prague. So maybe I go there, maybe I'm not. We'll see. That I'm going with my whole family. So. Yeah. If I was going alone, like, no problem, like, to go to Prague, but.

### You (2026-03-27T14:28:51.890Z)

Packing.

### Guest (2026-03-27T14:28:55.052Z)

We'll enjoy it. Enjoy the Czech Republic spring for you guys. My wife had, like, a work thing there, so we kind of just decided to go. I want to go.

### You (2026-03-27T14:29:04.690Z)

Vacation. Out of it. Nice.

### Guest (2026-03-27T14:29:06.092Z)

Yeah. Alrighty. I'll give you posted. I'll probably start writing tickets eventually for this. But, yeah, I'll see what the media team says. Thanks so much, guys.

### You (2026-03-27T14:29:18.370Z)

Thank you, guys.

### Guest (2026-03-27T14:29:19.452Z)

Thank you. Thank you.

