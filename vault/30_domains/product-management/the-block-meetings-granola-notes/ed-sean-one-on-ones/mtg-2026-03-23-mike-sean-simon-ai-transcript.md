---
granola_id: 188a6ab8-2563-4bcf-a86a-0d365d337e64
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of mike / sean - simon ai - transcript.
context: the-block
created: 2026-03-23
source: granola-sync
attendees:
  - mprice@theblock.co
  - erupkus@theblock.co
note: "[[30_domains/product-management/the-block-meetings-granola-notes/Mike _ Sean - Simon AI.md]]"
---

# Transcript for: Mike / Sean - Simon AI

## Attendees
- Mike Price (mprice@theblock.co)
- Ed Rupkus (erupkus@theblock.co)

### Sean (2026-03-25T15:02:18.758Z)

I'm gonna ping mic.

### Guest (2026-03-25T15:04:27.862Z)

You bring them.

### Sean (2026-03-25T15:04:32.758Z)

One of the main reasons why I wanted to have this meeting was just to just essentially go over stuff. And solidify our thinking for our meeting with Matt, but this could happen at any time. It's just kind of diving deeper into the. X402 stuff, his self-service API. It kind of like ties in with some our pro plans.

### Guest (2026-03-25T15:04:58.742Z)

Yeah.

### Sean (2026-03-25T15:04:59.238Z)

Just a better understanding.

### Guest (2026-03-25T15:05:03.542Z)

About to hear what he's actually working on already.

### Sean (2026-03-25T15:05:30.358Z)

So if he responds, we'll just do what we did yesterday if he responds, then I'll shoot you a slack. We can hop back on. So we're not just sitting around like a bunch of bunch of jaggaloons.

### Guest (2026-03-25T15:05:46.422Z)

I'm looking at the box you sent me for the Block Pro three. Ideas.

### Sean (2026-03-25T15:05:51.878Z)

Yeah. What do you think?

### Guest (2026-03-25T15:05:53.862Z)

You have nins and keiko and different llama is the partners in here. Instead of the ones diamond.

### Sean (2026-03-25T15:06:03.238Z)

Instead of the.

### Guest (2026-03-25T15:06:03.622Z)

Specified.

### Sean (2026-03-25T15:06:04.278Z)

Way?

### Guest (2026-03-25T15:06:05.302Z)

Instead of the ones Simon specified.

### Sean (2026-03-25T15:06:05.398Z)

Oh. Did he specify?

### Guest (2026-03-25T15:06:10.822Z)

I have it in the slideshow. And then.

### Sean (2026-03-25T15:06:13.078Z)

Oh, okay, cool.

### Guest (2026-03-25T15:06:23.622Z)

This. This is a lot of stuff I don't have. I don't have time to read all of it.

### Sean (2026-03-25T15:06:27.798Z)

Yeah, it was just something. It was something that I was putting together just so I had a better understanding and could actually. Talk to mad about it instead of just saying the idea and not really backing it up. And I figured if you wanted to check it out. Could.

### Guest (2026-03-25T15:06:47.622Z)

It's just a lot of stuff. It's, like, hard to get it. It's hard to admit it. It's an excuse. It's like any of this is.

### Sean (2026-03-25T15:06:57.878Z)

Yeah, it wasn't something that was going to send to Matt or anything like that. It was more.

### Guest (2026-03-25T15:07:05.702Z)

What he thinks. And if he wants to. He probably will have will pick an idea and want us to. Like. Write sort of like a prd, I guess, or something like that. And then, you know, these would come in handy for sure.

### Sean (2026-03-25T15:07:21.398Z)

Okay, cool.

### Guest (2026-03-25T15:07:24.182Z)

My man, I'll catch you on the next meeting.

### Sean (2026-03-25T15:07:26.998Z)

Sounds good, man. Talk to you later.

### Guest (2026-03-25T15:16:36.578Z)

I don't remember exactly what the hell that is, but anything that we throw on the webia. Yes. We can easily expand that. I think. Yeah, that was one of our ideas because I think talking to clients, talking to revenue, one of the main things was querying data. So like for this to really take off, we would have to have data in it, like the data dashboard and phone and potentially funding, et cetera, et cetera. Yeah. That's all I was asking. Yeah. Funding would be a different beast. But I think we could easily do it. I mean, funding, it's that it's backend is in Python. So I think that would be wouldn't be. Yeah, we wouldn't necessarily need to do the like full because we have. Like. I don't know if I'm gonna get lost in the data pipelines here, but we already have like funding dashboard charts that we post on data dashboard, which makes me think that we like have the pipeline set up that those that data gets basically translated into data dashboard. Like bucket essentially. So like the summarized data, like how many monthly deals, how many monthly capital, how much capital raise in a month. That's like not raw data that we collect on Django, but just to summarize portion already system data dashboard. So like if we include the dashboard, I feel like that would be. Like sufficient enough. I mean, yeah. Yeah, that makes sense. Yeah.

### Sean (2026-03-25T15:18:16.231Z)

Yeah, and I was looking into different ways after you gave me the information about.

### Guest (2026-03-25T15:18:16.978Z)

That's cool. Though.

### Sean (2026-03-25T15:18:23.991Z)

You're currently using sonnet 4.5. Right for the actual calling. Because. When I was thinking about the open source LLM stuff like one of the things is either to save money like you could transition over to haiku for specific queries depending on how complicated it is and then just using sonnet 4.6. For a little bit more complicated. But have you looked into like when Alibaba's models like Quinn 3.5 I think it's called. And yeah Quin 3 5 and Quinn 3 2.

### Guest (2026-03-25T15:19:07.778Z)

Yeah, I think I installed it a little while ago.

### Sean (2026-03-25T15:19:09.351Z)

Or.

### Guest (2026-03-25T15:19:10.978Z)

I don't know if I have their latest things. I did it back in February.

### Sean (2026-03-25T15:19:15.031Z)

Okay.

### Guest (2026-03-25T15:19:16.098Z)

Nothing with that. Yeah, it was fine. Like it was good. But it's more, it was more for like experimental. I didn't find it good to be to do like production work yet.

### Sean (2026-03-25T15:19:22.871Z)

Yeah. Gotcha. Okay.

### Guest (2026-03-25T15:19:28.978Z)

Yeah. And then we have a cloud max subscription. Gives us that does cloud max subscription is insane. Like it's two a month. But the way the amount of usage you get out of it is like ridiculous. Like I can, I literally use cloud opus all day.

### Sean (2026-03-25T15:19:37.831Z)

Yeah.

### Guest (2026-03-25T15:19:49.058Z)

And I don't hit my quotas and I'm running like 10 different projects.

### Sean (2026-03-25T15:19:52.951Z)

Yeah.

### Guest (2026-03-25T15:19:54.258Z)

So it's like, so for us, we have a cloud max subscription and you know, we have like four developers on it. And and then this also uses it. So we just have like all this usage that doesn't really. So for us, it's like now we're using it for development. We're using it for. And then this is so the cost of this right now is negligible. If we did need to move to like on premise inference, you know, I heard lama olama, whatever that was pretty decent. But I'm open to suggestions if we want to do some local inference stuff. I've done a number of things before. So we can, we can try it out. I like doing the routing based on complexity takes like. Some inference up front. So like we'd have to. Like figure that out and make it just adds a little layer of complexity on top of it. Like, oh, this is a complex question. Send it off to plot. Or this is not a question. Use the local. You know, so it's like, or you can do it based on the amount of tokens like, oh. Anything below, you know, 50 tokens gets the local LLM. Anything above that gets the remote LLM. But yeah, that's, that's basically it. But right now we're fine. I think this is projected usage wouldn't bother us, you know, for a foreseeable future. And if we ever did, it's a great problem to have because we're also getting paid for it.

### Sean (2026-03-25T15:21:23.911Z)

Yeah exactly.

### Guest (2026-03-25T15:21:27.058Z)

So can you please explain to my ignorant mind? Because I remember in the beginning, Simon, I was using. Openai as the back end, right? Like that's how we're prompting that. We use open AI for the embedding still. There's no way around that. We're locked in to open AI's embeddings, but we use cloud for sonnet. You can use any llm. You just take it. You're just passing the embeddings over to whichever LLM you want to use. So using anthropic for their answers, their answers just have better quality. Like they just have even sonnet is better than what we are using. I think we're using like. I think we're using like the deprecated model. I gotta check that. But yeah, like we're not using GPT. I don't know if we're using GPT5 in production right now. For the Simon that served assignment that's serving up pro. Yeah, that's the legacy Simon. Yeah. So this was technically still be like, like the answers would come from the LLM, which is under our subscription. Yes. We were saying about the usage that we could potentially run into the limits. Yeah. Limit the capture way high. Like what? That's an interesting like business. Model. Like that's weird that they haven't tightened that up yet because like we can, we can use the subscription to build tools. That would use this. Software you provide us. To power basically the product that we are trying to sell. Yeah. And then. It's like, it's like a triple. Dipping. And we're making money off of the subscription. I guess, I guess it makes sense. But I feel like.

### Sean (2026-03-25T15:23:21.671Z)

Well the big the big three are pretty much like unconquerable at this point so they're just like yeah if you want to pay us to try to get paid yourself go for it like you're not going to destroy us in our actual. Like like any actual land of llms like Google Anthropic and open AI. Youe.

### Guest (2026-03-25T15:23:37.858Z)

Yeah, I just worry that like they're not as concerned about making money at this point as they are about earning, getting that market share. Everybody who afford it is trying to buy the market.

### Sean (2026-03-25T15:23:38.711Z)

Re not.

### Guest (2026-03-25T15:23:48.258Z)

Right. I guess yeah, I guess I'm looking a lot more like forward forward looking. Where it's going to come to a point where it's like. Saturation and maturity at some point, whether it's next year or five years or 10 years from now. But yeah, that's I guess my model is an abstraction layer. So if we ever need to switch to model, it's literally like a string change. You can change whatever. It's really, yeah, that you need a key. If you need a key, you need to provide the key. Um, so it's not even like a code change. So it's just like a configuration change.

### Sean (2026-03-25T15:24:11.831Z)

Yeah.

### Guest (2026-03-25T15:24:22.338Z)

So if we ever want to change, we could easily just point back to GPT if we wanted to, you know, it doesn't matter. Nice. Okay. This is so cool. Let's hurts my brain a little bit. I've been trying to step out of my comfort box a little bit. I need to dip my toes in this as well. I've been saying this for like so many weeks. Hopefully this week I can get around to it. Yeah. Yeah, man. Dive in man. That's what I mean. Sitting in prompts all day, man, just like learning. And I like. So sometimes I'm like, oh, yeah, that looks good. Sometimes I'm really just like looking at and I'm reading everything line by line. If I don't understand it, I'll go and reread it again. And then it's like, yeah. And then you just like in it. I was in the zone till like 1am last night. So yeah, so I want to test these. The only thing we need to do. So I have an admin dashboard. It's in the works right now. I want to get the admin dashboard in so we can see usage metrics. So that way and then test that out. And then that way we have visibility on who's using it, where using it and all that stuff. Also in building, still building. I'm building almost like. A pixel tracking. Implementation. I put it in pro API, the pro API. I've shown you all the pro API already. I don't think so. So this is the self serve. This was supposed to be the self serif pro API. This is like the reinvention of the public API that we implemented infro. This is self serve. I'm working with Jeff on pricing. Whatever that will be. Anybody can get started for free. They get some free usage out of it. No, actually, we do have a startup. You do have to pay to get started. I don't know if we did a free trial or not though. But anyway, like, so this is this actually we just implemented like tracking for this. So anybody who uses this for shipping the content with a pick, like with, like, three different encrypted pixels and inside the content so we can like see where they're called, where they're putting this content and track it. And they're also citing us and, you know, not breaking and putting no index, no follow. On their stuff. If not, then so what we do is we get the URL they requested us from and then we scrape that URL to see if they have no index and they'll follow. And if they don't have no index, no follow, then we, then they violate that we cut their access because we don't want them to hurt our SEO. So I plan on doing the same thing with Simon AI. Anybody who gets content from there. We track it. And you cite us, you put no index, no follow, or you get cut off. And then that's it. It's not an automated process yet. We can probably automate it at some point because we, it's all just data driven. So, but yeah. But yeah, that's, that's all right. So this was the self service thing that, you know, I was very passionate about this in leadership. Everybody was like really, okay, do it. So I did it. And then. Yeah, the only thing that's left is I have to like update the logo and stuff. Josh did be QA said look great. You know, it's like, hey, thanks. We have docs, we have refined docs for it. So, you know, this tells what existing pro users existing pro users can use it. That's actually one of the things that helped accelerate this is that someone else wanted new features. And I'm like, well, I'm not going to build new features on the old one. I'm going to build this out. And then give that to you. So existing customers can take their API keys and then just plug it in and then get authenticated and use it. So it's part of their pro so they don't like lose out on this. They get the new API. This is all rust driven as well. So it's really fast and it's really memory efficient, which really excites me because we had a lot of performance issues. The last one, which is no base. So. Yeah. And then we have new documentation for it on everything on how to authenticate. I need to hide this. This is not supposed to be there. I think this is supposed to be there. Yeah. Create a strike stack out for subscription list available payment plans. I mean, if somebody wants to use this and make it make us money, that's fine. But yeah, I should hide that. And then we have, so we have our charts, our news. It shows you all the stuff. Fancy new API docs.

### Sean (2026-03-25T15:28:47.511Z)

How do you plan on testing the x402 like what what would the process be for that?

### Guest (2026-03-25T15:28:47.618Z)

Yeah. I'm going to drive the price down to like 0.0001 cents.

### Sean (2026-03-25T15:28:52.151Z)

Like. Yeah.

### Guest (2026-03-25T15:28:57.058Z)

And then do it that way.

### Sean (2026-03-25T15:28:58.551Z)

Gotcha and what are you supposed to see like it would it be like a blocker or would it just it would just charge you like whatever.

### Guest (2026-03-25T15:29:03.538Z)

So. The agent is going to make a request. This API is going to say f you export 402. And then the AI knows at that point that it needs to pay. It has the header of what token to pay and all that stuff, and then it makes a payment. And then I get my response. For that.

### Sean (2026-03-25T15:29:20.551Z)

Gotcha.

### Guest (2026-03-25T15:29:20.818Z)

So that's full. That's like almost full agent to agent. But like you do that with MCP.

### Sean (2026-03-25T15:29:23.911Z)

Yeah.

### Guest (2026-03-25T15:29:26.498Z)

You can do that with. I don't know if you can do that with mcp. But you could probably do it with MCP, but you can definitely do it with agent.

### Sean (2026-03-25T15:29:33.991Z)

I think you can yeah.

### Guest (2026-03-25T15:29:35.618Z)

S like the best use case for it where it's like fully automated. Your agent has a wallet or has access to a wallet. And then you get the payment. If they make the request via their mcp, they get it comes back, x world two, they pay, they have a quota. It would also be good to, I don't know if we have the endpoint for it to know what their current usage is. Cause I think that's the right thing to do. Yeah. So they can actually track how much usage they have left while they're going.

### Sean (2026-03-25T15:30:05.191Z)

So that was reminding me the open open wallet.

### Guest (2026-03-25T15:30:05.618Z)

What's this?

### Sean (2026-03-25T15:30:09.031Z)

Did you see that? Okay so that's pretty much what you're describing.

### Guest (2026-03-25T15:30:12.978Z)

Yeah, exactly.

### Sean (2026-03-25T15:30:14.151Z)

Yeah okay.

### Guest (2026-03-25T15:30:15.058Z)

This is. Yeah.

### Sean (2026-03-25T15:30:17.591Z)

Awesome hell yeah all right yeah I would love to help you test this out. Yeah I would love to play around with this.

### Guest (2026-03-25T15:30:23.698Z)

Well. If you have an agent with a wallet and you want to point to it, then, you know, getting an API key is super simple. You just put an email address in and give you an API key. And then yeah, just hook your agent up to it. Via mcp. And then yeah, we test it out, see if. But yeah, I'll have to like adjust the prices on it real quick.

### Sean (2026-03-25T15:30:46.071Z)

Okay yeah I'll let you know when I.

### Guest (2026-03-25T15:30:46.338Z)

So you're not. Super exciting. Okay, well, so we'll have a chat with Matt about the future of bro. So this is.

### Sean (2026-03-25T15:31:02.631Z)

This is very much. What we were thinking so I'm glad we spoke to you about this because we were just saying this is pretty much like I mean this is what. The future is so we should really lean into it and you already got us you already got the ball rolling.

### Guest (2026-03-25T15:31:19.698Z)

I mean, this seems like it's a no-brainer to be honest. It's like this. If you don't have this, you already like, what are you doing? Why would you not have this?

### Sean (2026-03-25T15:31:21.751Z)

Yeah. Yeah.

### Guest (2026-03-25T15:31:28.658Z)

You're a blockchain company, right? And you're paying, we're doing stuff like this all the time. We're into it. Why not? You know, we're, we're building for the future. We're super early still. Like, like in the tiny, tiny, tiny corner of this window of like adopters and usage. So yeah, it's, but we will have it.

### Sean (2026-03-25T15:31:49.111Z)

But you see little things you see little things like popping up here and there like it's just like up up like oh here's another here's another person that's like starting to implement it or here's here's somebody that's talking about it a little bit more so it's better to get on now.

### Guest (2026-03-25T15:32:01.698Z)

Yeah. Exactly. I need to fix these icons. I'll have, I'll ship the dashboard soon, but you can start playing with it today. Yeah, just get an API key and then yeah, you're off. That. And if you want to play with the pro API as well, let's let me know about that because I can click you a free API key. You could just use that whenever you want.

### Sean (2026-03-25T15:32:22.551Z)

Sweet yeah yeah I'll hit you probably this afternoon.

### Guest (2026-03-25T15:32:28.338Z)

All right.

### Sean (2026-03-25T15:32:28.471Z)

Thank you Mike.

### Guest (2026-03-25T15:32:30.178Z)

Absolutely.

### Sean (2026-03-25T15:32:30.791Z)

I appreciate it brother. I'll talk to you later.

### Guest (2026-03-25T15:32:33.298Z)

Thanks so much, Mike. Yeah, for sure.

### Sean (2026-03-25T15:32:35.271Z)

Bye guys.

