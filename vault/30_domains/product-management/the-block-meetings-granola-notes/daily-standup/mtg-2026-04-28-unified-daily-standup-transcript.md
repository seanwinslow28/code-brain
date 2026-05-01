---
granola_id: 7d6bc8c8-c192-4145-bb93-02239046e296
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of unified daily standup - transcript.
context: the-block
created: 2026-04-28
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

### Guest (2026-04-28T14:37:25.180Z)

All right. Love hearing that. So SEO bugs. I saw. Corey tagged me on some. Some of them. One, one. I think, like, it was like. High priority one. And I asked Bogdan to take a look at it. It's like some broken link on. Yeah, but it's like it's there. I don't think any of those. Kind of get some context for a few of these and then I can, like, order them. So, yeah. These. Okay, what else is here? Finish. Yeah, I think crypto jobs. It's copper ones. I would say. And. Yeah, so I'm trying to get it running on a dev box. See that it's kind of working there. Like, maybe, like, if I see some minor issue and then, like, it's ready for review testing and. Yeah, so it's. I think it's very close. Starting block. And then. Then we can investigate after that. The gecko. Yeah. Support. SEO box sort of can just, like, be, you know, whenever we have time. Unless there's a. Major one. Election bug. Election Hub. It would be nice to actually, like, prepare that one. And make sure it actually works as intended. Right. Or is it supposed to. Leave it here? Almax page updates. I have not heard back from them after yesterday's call. They probably were, like, themselves like, oh, we didn't think about that. So let me just quickly see if I have. A. No, I don't have. Message from them. Though. Let's just sort of look again. Restart. Her back and forth with them. And whenever they have something, we'll just slot it in. It's those changes will be relatively small. Right, Nicola, for the filtering. Yeah. Without Max, you never know exactly. So, yeah, like. If it's just to expand the table. That's. That's the easiest way, I guess. Yeah. But I don't know, like, if we. If we add, like, three more rows. Yeah. Like. But, like, in three months, the lad, two more. So how. How big this table is going to get? I added. Yeah, I don't know. I'm just gonna wait for that. I I offer them all the options. And then let's see what they want. Okay. I see your bugs on Max page updates. Beverage shoes, and I I'm not familiar, so I fixed that one today. That's one. That's. It's fine. Like, yeah, century not working. Nuxt four. I think it's like we should have it. I think, like, someone opened the PR recently. What was it? Something about central career or marina. Yeah, kind of annoying, but I did merge that PR that I completely forgot about that we had, like, WordPress delivering so many errors to Sentry, and then it kind of spent all our, like, reporting quota, and then it stopped reporting. And I think, like, it's should be now, like, start reporting again in three days. With the first of the new months. So, yeah, hoping. We get that. Going, it's. Yeah, we're kind of flying blind. Yeah. Now with the issues like that, I don't know who is. Who was saying Roma that we have, like, issues on call, like, yeah, we don't know. Like, it's hard to track. Yeah. Okay. Translations shelved for now. Until we have further. Knowledge. I did test it with Caesar and Anna. And they read it as, like, nine out of ten. It was pretty good. They said that they look those translations. Looks like people wrote it. There were a few words that, like, exactly what Alex was talking about. Like. Like wallet, for example, translation. Or specific words. They're crypto words and just like the bot is. Doesn't have the context. Yeah, well, I'll have to check, like, how. How this would work because it's not that we. Are sending this to an llm. We are sending this to this plugins service, and I'm not sure, like, what options. For, like. Inputs on how to translate. I'm not sure. Okay. Sho, for now, until further notice, and this is also more late. Decisions. But it'll be. A hefty one. Okay, so Brian will help out with. The access, and then we'll write a ticket to fully deprecate it going forward. Oh, you, Nicholas, finishing up the crypto jobs. Then starting block is sort of like after a meeting tomorrow. No. Yeah, tomorrow. We can see where we're at. And then, like, if we have any. They're planning to start this show, like, soon, right? Exactly. Yeah. So it probably would be good to investigate and spike. In spite to coin gecko. Sorry. Somebody said something.

### Sean (2026-04-28T14:43:32.297Z)

I think like second weekend in May. Well I was saying the second week in May because I know they kept on pushing. It because of all the conferences and stuff.

### Guest (2026-04-28T14:43:43.420Z)

Yeah. Yeah. So, I mean, as always, like, stuff gets delayed, but, yeah, we definitely should buy. It's going to be fine. I mean, like, we have the prototypes ready. It's like if we are going to raise almax, we'll be able to do it. Right. So it's not a big deal, but, like, to do it right. If we want to use coingecko and, like. Like, have enough time to kind of QA everything. Yeah. So we should, like, focus on it. Gotcha. Yeah. So it seems like you're prepared for tomorrow's call, Michaela. Like you get handed everything for Josh. To need it to. So we're good there. And then, yeah, after that, like, obviously the election, we probably have to get it on that and, like, make sure it's production ready. And then after that, all, like. The one-off things that probably put this. Like. How does that look? I can take SEO and election Hub. Is it hard to spin up elections up locally or. No, it's just a payload you said, right? Yeah, I can take. I can take those bugs. Yeah. Let me know if. There is also one. One more. I think it's not listed here. It's so. But I think who reported it, I don't know, in. In dev or somewhere. It's like that. When you press. Yeah. Maybe you press search. Click. Now. Yeah. See, like, there is slight. Ly annoying. Yeah.

### Sean (2026-04-28T14:45:51.657Z)

I was just looking at that.

### Guest (2026-04-28T14:45:54.620Z)

Yeah. Also, I've noticed this this morning. The very last data point is. Like. That's not. That's not what. Body market says. Interesting. Like. Like, obviously theirs is like, oh, no, actually, this is poly market. Oh, wow. What happened? That's interesting. Something broke on there and. Yeah. Okay. There's something. Well, at least it's not us. Gotta read the news.

### Sean (2026-04-28T14:46:31.097Z)

Just super popular.

### Guest (2026-04-28T14:46:37.100Z)

Interesting. Way. But, yeah. Okay. And, yeah, this week is Christoph's last week.

### Sean (2026-04-28T14:46:47.177Z)

Oh shit.

### Guest (2026-04-28T14:46:49.260Z)

Yeah, he's, like, preparing for his state exam. Is it last week? Like last week? He's not gonna come back or last week just for time being. I think, like, he's hoping to come back. So that's. I know, like, from his side, but, like, I'm not sure, like, from our side. What's. What's going to happen? Yeah, he did. He did tell me that he basically was sort of telling me without telling me that he would like to stay at the Block, but I. I told him to chat with Mike and, you know, Nichola. Have you had any conversations about him? Michael? He's cool to come back whenever he's ready. I mean. It's helpful. You know? Yeah, we enjoyed working with him. I pair programmed with him a few times, so. Yep. As long as he's. Whenever he's ready. And everybody else is cool with it. They're good. All righty. Brian, what's. What's their name? Is your name him yet? No.

### Sean (2026-04-28T14:47:51.737Z)

The cat the cat I'm guessing?

### Guest (2026-04-28T14:47:53.180Z)

Oh, peanut. Seen that. Yeah. With a little peanut. What's your dog's name? Snoopy.

### Sean (2026-04-28T14:48:03.977Z)

Oh man I'm noticing a trend here Brian.

### Guest (2026-04-28T14:48:04.380Z)

And. Peel up. Yeah, there we go. Love it. Okay. I will try to, like, assign tickets and provide context as much as possible with just being us in case. You need more context, Brian. Yeah. Ideally, just take us through the election Hub stuff because I think reading through slack threads would be very confusing. Since you guys have the context. Maybe you can just make a. Even just like a link to the message that's enough. I'll figure it out. Everything else I can figure it. Out. Oh, you mean like you want to do it right now or. Or. Yeah, because I'll literally forget because there's other stuff to do, too. So, like, I like it right now. It's easy, right? I can think about it, but a couple hours from now. Oh, what was that thing? Like, should. And what the issue with, like, Brian said, like, you deployed yesterday, the pre-bid stuff. And I know, like, Alex suggested, like, and even. Yeah, like. It's a lot. We're really just gluing apis and talking to ad providers. Right now, the issue is that the ad providers, year Mac was trying to work with don't support European laws. So we have to update one trust and our config to go around that. But the biggest change we did was we needed to add Cloudflare headers, send them the prebid. Because the. The root issue was that we were using gdpr in every single country when we shouldn't be. So we had to do that and pass, like, state headers because cloudford knows what state you're in, apparently. So send that around. And that was the main thing we did. And the issue right now with your mech is the ad providers we wanted to use are not gdpr friendly. So we have to add a few more and, like, add a lot of if conditions in the code. Like, if you're in this state, in this country using this provider, you can use it. We'll load it for you. So a lot of just, like, gluing things together and debugging live. I feel like it'll never end. Yeah. Hopefully, like, I think, like, Alex. From what I understood, like, was kind of annoyed by this, like, kind of that, like, we're like. Site, you know, monetized by ads, and our ads are not, like, working as expected. They're working now. But, yeah, apparently not even that, he was annoyed when we were on our call. He said we could be sued for, like, multiple millions of dollars by the way it was set up. Because we were not respecting privacy laws at all. But no one noticed, so we're good now. People have tried to sue us for less. Yeah, that's crazy. Okay. Is this. Is this pretty good thing, like, all solved now, or is it still as of now? It's way better than before. We have pre-bid work in the u. S. But we're Mech is trying to figure out the European side. But we got, we got them on the us earlier, so we're good. We have no ads on europe. I think we'll survive. I think that's what it is right now, actually. I think it's just blank. Or the in-house ads or something. But I was holding off. I told you, I'm not going to send the message to Jeffrey until. He thinks we're good. So there's another update coming out later. Maybe we'll send a message later. Who knows? Alrighty. This group. So I think, like everyone here is aware that Matt is leaving. And do want to throw a party for him, like a farewell party on Friday or something. Just have a beer, maybe. I think that would be great. Well, usually, like, organizes. Them. Is. It. I don't. I've never been to one of those. Just whoever we, we just set it up. Ability is and. Yeah. With Joel the sad hour. What was with Joel? The sad hour. Of the side hour. Yeah. Yeah. Yeah. Just. I can. Yeah, I can try. Like, I'll chat with him if this is something he's interested in opening it up to him. But, yeah, I also invite him to the sad hour. Yeah. And probably, like, not too late. Yeah, for sure. Yeah. Yeah. 6 30 a.m. I'll take the gray hunt to New York if we have to.

### Sean (2026-04-28T14:52:54.777Z)

Oh yeah.

### Guest (2026-04-28T14:52:57.420Z)

Okay. Alrighty. Well. I can't wait for the all hands in half an hour. Good luck. DJ. So many. Guys. See you. See you.

### Sean (2026-04-28T14:53:18.217Z)

Guys.

