---
granola_id: 6c7c25c5-725f-4dcf-9966-4fdebb903769
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of unified daily standup - transcript.
context: the-block
created: 2026-04-23
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

### Guest (2026-04-23T14:01:06.586Z)

Arts on ETF pages. And it is not hard coded so I can I'll show you on the messages like where we can set this for WordPress. But do we have it? Like charts we have for each of the categories? Yeah. I was going to say that was a blocker or it was blocked by. The one of those tickets that I wrote for Nikola for to enable any chart selection because I think we just had like in the initial setup we just had BTC eth and xrp charts only. And maybe salana too. I don't know. So that's that's why I had that ticket written. And I just can't remember now if we ever shipped that. I think we did right, Nikola. He's not here. With migration. Yeah. Yeah. So. Yeah if it's possible to change them, I'll just go in and change them. And like if that feature is shit. So technically it would solve everything right on. Yeah. Like essentially the only issues as are with XRP and like all other like LTC, Dodge and other. Yeah. Because they had the default or like. The parent ETF ones. Yeah. Okay, I will take a gander. I think it's on. Is it on pages or is it in ETF categories? ETF categories. Yeah, I'll respond to that message and like to show you. Lovely. Thanks. Oh, perfect. Yeah, it's possible to do it. Yeah. Nice. Awesome.

### Sean (2026-04-23T14:03:12.559Z)

Sweet. All set.

### Guest (2026-04-23T14:03:14.746Z)

Yeah.

### Sean (2026-04-23T14:03:14.799Z)

Cool. All right how's it going everybody? We will start with Anna.

### Guest (2026-04-23T14:03:24.746Z)

Hello. I finished testing a lecture. Everything looks good. So we're really for the government. And well finished testing a small pieces for tokens and articles and dot pro charts. They both work by Kristoff. And well now I will start with brand safety keyword ticket dimension.

### Sean (2026-04-23T14:03:45.679Z)

Nice.

### Guest (2026-04-23T14:03:45.706Z)

And that's all.

### Sean (2026-04-23T14:03:47.999Z)

Thank you Anna.

### Guest (2026-04-23T14:03:55.066Z)

Hello there. So the ticket for Price indicators on this pages, it is ready. Nikola proved it. And I will create dev box probably not like on this week because we still have as far as understand like we have this like limitation of dev box. So I will like create it. Later next week. The ticket for AI generated metadata. I forgot to send it for review to Nikola, but it is ready. So I will send it like right now. And yeah, essentially it is ready. And yeah, hopefully it's more or less okay. And I guess I will start finalizing the ticket. That was like left from Maria for like change the list of tokens. And yeah, that's pretty much it.

### Sean (2026-04-23T14:04:52.959Z)

Nice man thank you oh. Thank you Bodan.

### Guest (2026-04-23T14:04:57.866Z)

That sounds good. Let's do that. Hi. Well, I advanced to the immigration. Finally, I could standardize more or less how I can migrate every workspace. I did immigration only for one. I'm doing the same immigration for another one. Yeah, I found with some problems. Because we have stage and brought and I need to parameterize both environment in the same workspace in the atlantis. So this is complex. But I believe it's don't. So I'm standardized the way to do this for the rest of, okay, the other workspace. So keep working on this. That's all. From my side.

### Sean (2026-04-23T14:06:01.119Z)

Okay thank you Caesar.

### Guest (2026-04-23T14:06:03.146Z)

Thank you. I am working on ratings pages. Organic plan and also working on my competitor analysis for the Niv section and I will also check ads. Metadata AI integration. Plan in the sheet. So that's all.

### Sean (2026-04-23T14:06:38.879Z)

Thank you very much. Kristoff.

### Guest (2026-04-23T14:06:45.546Z)

Working on the charts failed to load, but I had some problems involving the charts like on the local. I don't know why. Maybe Nicola if we can have a chat about it after a daily. And then in the meantime, I started working on the chart being blocked by the pro ban. Ner. Since I couldn't resolve the issue with. The charts unloading. So I took it from Ana. And also a quick question. Kristoff, when you were working on the ETFs, ETF pills and the crypto bills and articles. The zero percent thing. Was that always there? Like, was that just from the implementation? Oh, this I didn't work on. I didn't work on these. Yeah, I think it was Brian. I did it. I was asking. Okay. But I checked, I checked this ticket like the to do one and it's not like it's still showing zero. We probably just didn't connect. Probably just didn't connect the like API. Value for 24 hour price change to that specific component. So if you don't get to it, Brian will take care of it. When he comes back. Okay, so I shouldn't worry about it now about this. Yeah, worry about your current and progress task. I just wanted to ask like in case you had. Yeah, I don't know. I just, I just looked at it and it seems not the result, but I didn't have the time to. Get. Just a little thing on whether Brian come back. Tomorrow. Ah, tomorrow. Okay, nice. Yeah, I know. I miss a mom calendar days. 20 hours.

### Sean (2026-04-23T14:08:39.279Z)

I was gonna say tomorrow about like five more hours and 20 more minutes.

### Guest (2026-04-23T14:08:48.746Z)

More like 24 hours. Looking to scouting.

### Sean (2026-04-23T14:08:51.759Z)

Well. 24 hours plus to five hours plus the 20 minutes. Thank you Kristoff. Mike.

### Guest (2026-04-23T14:09:06.986Z)

And not here.

### Sean (2026-04-23T14:09:07.599Z)

Said okay. Nikita ghoulis.

### Guest (2026-04-23T14:09:16.266Z)

Yep. So we're supposed to be with the need is he might have mentioned yesterday also. Sorry, by the way, from dropping from the sink, there was an urgent hole here at vention. So, yeah, working closely with Nikki on the new UI and it's combination with the backend with like adjustments for potentially missing crypto wallets, et cetera, et cetera. Entirely focused on that and that's all.

### Sean (2026-04-23T14:09:42.799Z)

Cool thank you Nikita. Oh.

### Guest (2026-04-23T14:09:50.106Z)

Touch with Rama regarding the issues he found. So fixing them, deploying and seeing. What's what will be the next that he will found. So I think that's mostly it for now.

### Sean (2026-04-23T14:10:08.959Z)

Cool. Yeah one thing I wanted to bring up now that we're getting the new CEO. I don't know if you guys saw in the campus channel that cam tines wrote that the campus certificate for coursework completion still has Larry as CEO on it. So I'll write up a tick just so we can get that squared away and fixed for future implementation.

### Guest (2026-04-23T14:10:34.026Z)

Hopefully we'll need to change that anymore.

### Sean (2026-04-23T14:10:34.319Z)

Just. Yeah.

### Guest (2026-04-23T14:10:40.746Z)

Go ahead.

### Sean (2026-04-23T14:10:41.199Z)

What's up Roma?

### Guest (2026-04-23T14:10:41.546Z)

Rama. Okay, so also we have Kaleb, JC in course. Description. As SEO. Maybe we should change that as well.

### Sean (2026-04-23T14:10:57.839Z)

Yes yeah I'll write that down.

### Guest (2026-04-23T14:11:02.266Z)

Is that one on one. Or which one on one? Yeah. Because he's still the, he's, oh, he's this. Oh, okay, Yeah, he's the voice over there. So technically we need to remove him. It's just the title. I don't know what the hell we should call him. Probably just first name, last name. That's it. Oh, Lord. Okay.

### Sean (2026-04-23T14:11:31.279Z)

Yeah Joel just say he's the voice actor.

### Guest (2026-04-23T14:11:32.426Z)

Yeah. Produced by or whatever, tequila Jesse.

### Sean (2026-04-23T14:11:38.959Z)

Yeah.

### Guest (2026-04-23T14:11:41.546Z)

Not the Block CEO. Caitlin Jason. Yeah, I want to make sure we let's create a ticket for that too. Sean.

### Sean (2026-04-23T14:11:46.639Z)

Yeah. You got. It. Thank you Nikita thank you Rama for pointing that out. Michaela.

### Guest (2026-04-23T14:11:56.426Z)

I was just wondering. So should we make like the CEO name editable in some WordPress or somewhere. No, that's a, that's a bad omen. We don't, we're not preparing for that.

### Sean (2026-04-23T14:12:08.879Z)

Do it do it do a drop down.

### Guest (2026-04-23T14:12:12.106Z)

Yeah, exactly. It's like handing out parachutes to all your commercial plane passengers. Like, no, no, no, we're not doing that. All right, so yeah, set up today, dev box for translations and getting ready to deploy election hub pages after stand up. And that's, that's all for me.

### Sean (2026-04-23T14:12:36.239Z)

Nice cool yeah I'm guessing that's the the big the big push after the stand-up.

### Guest (2026-04-23T14:12:43.226Z)

Yeah, like I'm kind of merging a lot of code that I didn't work on, so hopefully everything goes well. Like, yeah, we'll be on standby.

### Sean (2026-04-23T14:12:51.039Z)

Nice. And Ed did you ever get the stuff from Cody because I was trying to get into his dropbox and I was having issues myself. Like the the videos okay.

### Guest (2026-04-23T14:13:01.626Z)

Yeah, we're good. I picked, yeah, three shorts. And I told already whenever nickel deploys, I'll jump in and upload them.

### Sean (2026-04-23T14:13:12.639Z)

Cool. Thank you Nichola.

### Guest (2026-04-23T14:13:16.106Z)

Thank you.

### Sean (2026-04-23T14:13:16.639Z)

Rama.

### Guest (2026-04-23T14:13:19.706Z)

K again. We're working on sponsored cursors right now. And that's all.

### Sean (2026-04-23T14:13:28.239Z)

Perfect.

### Guest (2026-04-23T14:13:28.586Z)

Mostly on campus parts because.co site is pretty easy. To fix something. So more attention to campus. App itself. We're looking good so far. Like. Any, what's the status now? Use your list ever growing. Yes, a lot of bugs. That is the status. Do we have any deadline for this feature or not? Well, we, we had originally talking about the end of month release. But like it's not super strict. I don't think there's any anything dangling over our heads because of that. So we definitely would prefer it to be fixed rather than shipped early with bugs, you know. So that's all I can say for now. Like I said, I'm waiting for the CEO. To come in as well. And but our relationship with that market is really good right now. So we're also launching right now the another landing page for them. So if we have to postpone another week, because I think it's next week, May already. Got time is flying.

### Sean (2026-04-23T14:14:53.279Z)

Yeah.

### Guest (2026-04-23T14:14:54.346Z)

Yeah, end of next week. So yeah, we're probably not going to be able to ship it by end of next week. Probably have to do the following. So that's sort of the timeline. That we should be thinking in our head. Okay. Okay. Yeah. We get to in seven days, like my 30th if we could get to that. That would be amazing. But I'm also realistic. It's hard to say. When we will fix everything. So, but definitely just keep us posted as well. So I have a call scheduled, I think, on Tuesday so we can. Like. Check in. And answer any last questions. Hopefully there won't be any surprises. Yeah, but what is next feature we should implement on campus after that. After that, as far as I can tell, it's 201 individual.

### Sean (2026-04-23T14:16:05.359Z)

Individuals. Yeah.

### Guest (2026-04-23T14:16:10.426Z)

Okay. Okay. Slide feeling that we may do that together. Just feeling. It's a bad feeling. Yeah. Because the idea of poly market cools is to bring more people to see our little course and buy access to 101 and 201. And this part. Should be kind of implemented. Right. True, true. But also. It's.

### Sean (2026-04-23T14:16:50.959Z)

One of the bigger aspects is getting to poly market like trying to get. Trying to get like traffic into poly market just as much as we're trying to get traffic into campus.

### Guest (2026-04-23T14:17:04.346Z)

The way leadership has been thinking about this right now has been that this is the sponsored course. Is how do you say it's like. Bathing the path basically to see if this works. And we are actually able to funnel people from. That go and socials elsewhere. To campus and just to get this like to take those content for free. Then we can sell it to a lot more people, a lot more companies. And that's a lot more like profitable. Because you have guaranteed. You know, upon delivery of the course guarantees revenue. So that's almost. Like for at this moment is more important to. Like make sure the poly market stuff works and obviously like. We have the once we have the till one ready, if we spin up this flywheel and we have like, you know, a lot of, you know, hopefully a lot of traffic on that code moving. Funneling into the campus and getting the sponsored courses because maybe they don't want to pay, you know, whatever X many dollars for individual course. And that becomes sort of like the. Consumption vehicle for individuals. And enterprises is a different story. We do want enterprises. To. Get access. So I hear you that it would logically make sense from a product perspective to have 201 ready for them to be upsold and buy those two one and one on one courses. But let's just ship out the sponsored course and then we'll go from there. Okay. Okay.

### Sean (2026-04-23T14:18:53.679Z)

Cool thank you Rama. Do you want to add anything.

### Guest (2026-04-23T14:19:01.626Z)

Yeah, I was just going to say because the spot, that's definitely not the last sponsor course that we'll implement. So this already talks about, you know, I think there's. Three agreements talks with other companies too, so we just need to make sure that this works and it's like. We can show something for the clients. Other than that, yeah, no, just the top of mind is the election coverage. So. I'll be on standby and coordinating with. Socials and our partners. So Polymarket and stand with crypto. Have agreed to amplify it. So hopefully. I was a little bit of Ruckus on socials. That's mainly it. Yeah. I have the question if stand with crypto answer you about the bridge beam return and error. I mean, it's working with the fix Michela. Just wondering why you said if it's for the API. Yes. I think it should be fixed, right, Nichola, and you have the sort of like fallback implemented in case it doesn't work anymore. Yeah. It's just that what I don't have implemented is there is no, if it does like stop working their API, we don't have like any notification. We're kind of falling without notifying us like, oh, standard crypto is down and we're kind of serving this not up to date version. Yeah, that will be a bigger concern with V2 rather than right now. Right now, like it's just a list of those politicians. It will be important for us to have that. Flag once week two in the whole formula. Calculation is in place. But I think right now if it's working, even if it's like, you know, for the next month if it's outdated by a month, I don't think the world will collapse. So yeah. Okay, let's just let's just assume that, you know, their API works. Because that data is not changing that fast. You know. Also hopefully it works when we deploy because like the initial cache like needs to, you know, pick it up. Yeah. Good question. Though. Thank you.

### Sean (2026-04-23T14:21:38.159Z)

Thank you Ana and one thing I just wanted to ask before we head out Rama and campus team nicholas nikita sorry do you need anything from David. Do you need anything from his end because he was updating me with a bunch of games but if he has like a bunch of bugs that need to be worked on then we should be focusing on that.

### Guest (2026-04-23T14:22:03.866Z)

We still need to update 201. To the list of bugs I've created. Some time ago.

### Sean (2026-04-23T14:22:16.079Z)

Yeah.

### Guest (2026-04-23T14:22:19.146Z)

And I guess that's all from my side.

### Sean (2026-04-23T14:22:21.439Z)

Okay.

### Guest (2026-04-23T14:22:22.186Z)

Yeah, I need those fixes.

### Sean (2026-04-23T14:22:25.439Z)

Nikita's anything on your end?

### Guest (2026-04-23T14:22:29.146Z)

I don't think so. As of right now.

### Sean (2026-04-23T14:22:32.639Z)

Okay.

### Guest (2026-04-23T14:22:38.026Z)

For the course.

### Sean (2026-04-23T14:22:42.799Z)

They just finished up the election hub video right Ed.

### Guest (2026-04-23T14:22:47.146Z)

So we're probably going to have just a placeholder. Picture in the, in the beginning. That's why. Okay. Sort of prediction. Well, we'll try to do like a fast follow on that.

### Sean (2026-04-23T14:23:08.079Z)

So for right now we'll just use the the poly market PNG that we have and then hopefully we're able to get them on it soon. Thank you.

### Guest (2026-04-23T14:23:17.386Z)

And I haven't done testing new poly market course. So maybe I will need something.

### Sean (2026-04-23T14:23:25.279Z)

Okay.

### Guest (2026-04-23T14:23:25.866Z)

So that's what I can say. Let's send it to one stock to him that Rama has logged.

### Sean (2026-04-23T14:23:27.679Z)

Yeah yeah yeah.

### Guest (2026-04-23T14:23:33.306Z)

Sean. And then from we sent it to him already some time ago.

### Sean (2026-04-23T14:23:38.319Z)

I'm gonna I'm gonna remind him I'm gonna poke him yeah. Cool thank you. Is there anything else that people want to discuss before we head out start enjoying the weekend. All right. Sweet thank you very much everybody. Enjoy the rest of your evenings I'll talk to you next week. There it goes.

