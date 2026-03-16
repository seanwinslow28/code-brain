---
granola_id: 1183da1a-a24d-43cf-b4e4-160b487ab4d2
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of test adop - transcript.
context: the-block
created: 2026-03-16
source: granola-sync
attendees:
  - kvallecillo@theblock.co
  - ldanowski@theblock.co
  - erupkus@theblock.co
note: "[[30_domains/product-management/the-block-meetings-granola-notes/Test AdOp.md]]"
---

# Transcript for: Test AdOp

## Attendees
- Karla Vallecillo (kvallecillo@theblock.co)
- Lil Danowski (ldanowski@theblock.co)
- Ed Rupkus (erupkus@theblock.co)

### Guest (2026-03-16T17:31:14.394Z)

Hello.

### Sean (2026-03-16T17:31:15.895Z)

What's up, Carla? How are doing?

### Guest (2026-03-16T17:31:19.074Z)

Good. How are you? Sorry. I'm working on stuff. Hi, Chloe. Let me try to get some stuff done while you guys hop on.

### Sean (2026-03-16T17:31:26.945Z)

Yeah. You're good. Yeah. I'm not sure about Ed at he asked me to invite him, but they're dealing with something else right now, like, having people log in to pro and campus. So he's a

### Guest (2026-03-16T17:31:42.844Z)

No worries. I don't think

### Sean (2026-03-16T17:31:47.315Z)

Yeah.

### Guest (2026-03-16T17:31:48.434Z)

it was mostly Lil. K.

### Sean (2026-03-16T17:31:50.695Z)

Hey.

### Guest (2026-03-16T17:31:51.104Z)

Hey, Lil.

### Sean (2026-03-16T17:31:51.695Z)

Okay.

### Guest (2026-03-16T17:31:52.714Z)

Sorry. I'm late. We just did that. Wanna break anything. In Salesforce. And then you have to deal with it. What about breaking? So, basically, Sean has gotten way further in the process of building our ad op system thing. I don't even know what to call it. What did we decide to call it?

### Sean (2026-03-16T17:32:18.215Z)

Yeah. I would call that the Zapier ad ops automation.

### Guest (2026-03-16T17:32:20.284Z)

Yeah. Yeah. Yeah. We just, wanted to create a couple of I guess, fake deals and close win them just to make sure that everything is set up properly. So we Yeah. Wanted to loop you in first. Yes. Of course. So let me everything on my test account, which is where we created the last one, I can delete everything later. So just give you this record. In short. Do you need it with specific products, I'm assuming? Like, did you do it We wanted to try one with a pro like, a a pro closed one just to make sure that it's not creating a record for that one. And then one with just one product offering and then a third with multiple products in one deal. Okay. You is the trigger based off of opportunity record type? So your goal is only trigger this on a sponsorship

### Sean (2026-03-16T17:33:24.315Z)

Yes.

### Guest (2026-03-16T17:33:25.574Z)

record type.

### Sean (2026-03-16T17:33:28.025Z)

So it's the opportunity

### Guest (2026-03-16T17:33:28.134Z)

Okay.

### Sean (2026-03-16T17:33:30.555Z)

and the oh, it's a field field stage. Stage field rather. Sorry.

### Guest (2026-03-16T17:33:34.644Z)

Okay. But the but it's opportunity

### Sean (2026-03-16T17:33:36.925Z)

Correct.

### Guest (2026-03-16T17:33:38.804Z)

type is your first filter for entering the flow? Okay. So ideally, we should test membership and renewal because we have three records types in Salesforce, membership renewal and sponsorships. Assuming your logic is, like, record type equals sponsorships, it should be fine, but we would need to test the other two. Okay. Let's just go to my record. And you you guys, like, are welcome to play around with this as long as you show me whatever

### Sean (2026-03-16T17:34:10.185Z)

Okay.

### Guest (2026-03-16T17:34:10.234Z)

opportunity you created afterwards, we don't, like, have to do it. Live, but I will be able to bypass all of the requirements. And they're like, times 10 of the sponsorship opportunities. So let me just do one for you. I can, like, add all of those exemptions for you too.

### Sean (2026-03-16T17:34:38.385Z)

Yeah. I was gonna say, I remember when I was making when I was working with this last time, there was a lot of, like, random blockers, like, all the fields that have to be

### Guest (2026-03-16T17:34:48.684Z)

Yeah.

### Sean (2026-03-16T17:34:49.635Z)

filled out specifically.

### Guest (2026-03-16T17:34:51.064Z)

Yeah. The pro side is way crazier than the sponsorship side. But okay. Cool. Let me add a product. Should I sell our first campus LMS?

### Sean (2026-03-16T17:35:19.485Z)

You're good.

### Guest (2026-03-16T17:35:21.904Z)

If we're gonna if we're gonna go for it, let's make it No. Should I do, like, a two million dollar campus deal right before we're

### Sean (2026-03-16T17:35:28.955Z)

I'm gonna tell you, just bump it up. They were just throwing us money.

### Guest (2026-03-16T17:35:31.704Z)

oh my god. Okay. Let's just do something random. One hundred. You're ready for me to market one right now just to make sure it doesn't pick it up. Right?

### Sean (2026-03-16T17:36:02.935Z)

Correct. Yeah. Right right now right now, this app is off. So it's not gonna get triggered or anything like that. I would just have to refresh the page, and this should show up

### Guest (2026-03-16T17:36:11.664Z)

Oh, if your Zap is off, I don't think if the trigger is the stage moving into close one, you refreshing it is not gonna trigger the the zap. Like, I'll have to keep it in

### Sean (2026-03-16T17:36:24.785Z)

Well, that's that's more so for the actual test

### Guest (2026-03-16T17:36:26.584Z)

well,

### Sean (2026-03-16T17:36:29.125Z)

itself because when I refresh it, then it shows the actual like, it'll show the latest the latest Salesforce ad ops Like, what like, the the the latest record on Salesforce. Sorry. Hold on.

### Guest (2026-03-16T17:36:46.074Z)

I don't know if I'm following. So

### Sean (2026-03-16T17:36:46.735Z)

Yeah.

### Guest (2026-03-16T17:36:48.134Z)

it's okay for me to close to win this, and then you're just you'll be able to test whether it triggers it even though the zap's off.

### Sean (2026-03-16T17:36:53.805Z)

Yes. Correct. Because it it like, when I when I refresh the page, then it shows the latest closed won opportunities in the act in the actual zap itself. Like, it'll say,

### Guest (2026-03-16T17:37:05.234Z)

Okay. Okay.

### Sean (2026-03-16T17:37:07.235Z)

just, like, kind of, like, shows, like, oh, this one happened on 03/16 and blah blah blah. And then it'll

### Guest (2026-03-16T17:37:11.874Z)

Okay. But it'll so it'll show you this, and it'll say whether it was gonna

### Sean (2026-03-16T17:37:12.455Z)

show you all the fields that Correct.

### Guest (2026-03-16T17:37:16.814Z)

the flow or not. So you don't

### Sean (2026-03-16T17:37:18.145Z)

Yep.

### Guest (2026-03-16T17:37:18.374Z)

Great. And, Lou, when do you pull when do you pull numbers? Just so that or do you have to go in and delete these? I'll I I'm the one who does. Like, I'll remember if there's, like, a random Okay. Okay. Every day is my answer right now, Carla. But I just know we're keeping a close eye right now. So Yes. Correct. But I I will remember to take all this stuff out. Oh, and, Sean, I have those one pagers What would be the best way to include those Did we decide whether we can include it in the form or

### Sean (2026-03-16T17:37:57.225Z)

So yeah. Yeah. Can you set you said a bunch of different PDFs for each client or each form that you would want? Product? Alright. So yeah. So

### Guest (2026-03-16T17:38:07.084Z)

for each product. Yeah.

### Sean (2026-03-16T17:38:11.015Z)

them over to me, and then I'll figure out whether or not it should be within a step or if it just gets incorporated into the actual email that's sent out.

### Guest (2026-03-16T17:38:18.524Z)

Mhmm. K.

### Sean (2026-03-16T17:38:19.095Z)

So yeah. That over to me, and then I'll I'll let you know.

### Guest (2026-03-16T17:38:22.624Z)

Okay.

### Sean (2026-03-16T17:38:22.795Z)

But, yeah, it's just it's just a PDF for each product. Right? Like, that's

### Guest (2026-03-16T17:38:25.544Z)

Yes.

### Sean (2026-03-16T17:38:26.245Z)

okay. Cool.

### Guest (2026-03-16T17:38:33.164Z)

I think I have to make two more. I don't have one for the article button. And there was one other one that I saw. But I will get those over to you today.

### Sean (2026-03-16T17:38:45.645Z)

Thank you.

### Guest (2026-03-16T17:38:47.134Z)

No. Thank you. You're making my life so much easier.

### Sean (2026-03-16T17:38:50.935Z)

Yes. It's very interesting. This time around, I really dug deep into what Zapier is capable of, and I just found out so much more. Like, hopefully, to lessen any sort of break breakages within the actual workflow itself. Because, like, a lot of it is done through, like, the products at Zapier like sells essentially, or, like, they implemented in their own workflows.

### Guest (2026-03-16T17:39:16.164Z)

I'm trying to create one myself for my news like, the newsletters that come into my inbox. But I'm still working on it. It's not the most friendly thing.

### Sean (2026-03-16T17:39:32.855Z)

What where does it go? How does it work, or how is it supposed to work?

### Guest (2026-03-16T17:39:36.444Z)

Basically, it looks through my emails and checks for specific newsletters coming in, and then it's tracking the sponsors for each newsletter and then recording it in a Google Doc. So instead of me having to manually do it, hopefully, it can just track them for me.

### Sean (2026-03-16T17:39:54.775Z)

Mhmm.

### Guest (2026-03-16T17:39:56.884Z)

Is it, like, an AI component of a Zap? No. It's just yes. Yes. Yes. Because it it uses, like, ChatGPT or something. Yeah. Interesting. Never giving anything access to my to randomly go through. Like No. It only you have to provide whatever email you wanted to

### Sean (2026-03-16T17:40:17.665Z)

Like,

### Guest (2026-03-16T17:40:19.084Z)

look for, scrape for. Yeah.

### Sean (2026-03-16T17:40:20.835Z)

so you edit the filter, like, only only

### Guest (2026-03-16T17:40:21.144Z)

Yeah. Yeah. Yeah.

### Sean (2026-03-16T17:40:23.665Z)

get triggered

### Guest (2026-03-16T17:40:25.394Z)

I would be weary too. No. I've, like, heard of people literally who work for Gem like, for these companies, and they're testing out the bots, and they've, like, deleted their entire email or, like, gotten into their Google Drive and, like, surfaced all of the company records on blah blah blah. Like, there's harsh Don't scare me like that.

### Sean (2026-03-16T17:40:46.515Z)

No. I think I I I heard the story

### Guest (2026-03-16T17:40:47.624Z)

I'm here thinking.

### Sean (2026-03-16T17:40:49.675Z)

ClaudeBot. Is that what you're talking about? Or now

### Guest (2026-03-16T17:40:53.424Z)

Potential. Yes.

### Sean (2026-03-16T17:40:54.775Z)

Yeah.

### Guest (2026-03-16T17:40:55.094Z)

Potentially. Yeah. I just I know. Everything's overworked in my opinion. Just, like, do it.

### Sean (2026-03-16T17:41:02.845Z)

Yeah.

### Guest (2026-03-16T17:41:05.354Z)

I'm I'm so old and old school. Like, just do the do the work.

### Sean (2026-03-16T17:41:08.515Z)

Yeah. I was gonna say, well, people are are like, finding they're spending more time trying to make that a thing instead of actually doing the work that they're trying to get that thing to do.

### Guest (2026-03-16T17:41:19.704Z)

Well, yeah, because if you don't learn how to do it the right way first, if you just add automation on top of it, then it's gonna be shitty automation. So it's like,

### Sean (2026-03-16T17:41:25.385Z)

Yeah.

### Guest (2026-03-16T17:41:27.534Z)

I'm such a my my kid call me a boomer, and I'm like, I am not a boomer. But I am definitely not a fan of all of these. New things. As Carla knows, our team can't even, like, keep their close date on five opportunities up to date. So, like, why add automation on top of it? Alright. I just did oh my god. Okay. Membership and renewal. Not that you say. Okay. I'll give you the records. Okay. And then we want a sponsorship record. With one product and a sponsorship record with multiple. Yes.

### Sean (2026-03-16T17:42:51.335Z)

And do the client's images go like, do you put them within Salesforce or I'm sorry. Never mind. Take that back. Don't listen to me. That's all through the form process. That I was setting up. But what what was the original

### Guest (2026-03-16T17:43:05.854Z)

They just send them to me through

### Sean (2026-03-16T17:43:06.805Z)

way of doing that?

### Guest (2026-03-16T17:43:09.924Z)

email or through Telegram. You have this triggered on every single product? Type or on specific products?

### Sean (2026-03-16T17:43:20.535Z)

Just on whatever, is marked as closed one, it'll go through, and then it'll filter out whether or not it says sponsored post or basically the whole, list of things that Carla gave me, like sponsored post, display ads, or display posts,

### Guest (2026-03-16T17:43:36.524Z)

Newsletters.

### Sean (2026-03-16T17:43:38.765Z)

newsletters,

### Guest (2026-03-16T17:43:40.234Z)

So that's are you reading based on, like, the actual name of the product or is it, like, a contains formula where you're saying look through all of the products, and if it contains the word newsletter,

### Sean (2026-03-16T17:43:52.875Z)

Correct. Yeah. If whatever gets, marked as closed one, then it'll go through the filters, And if it has, like, it's basically stopping it if it has anything outside of the specific words that Carla sent to me. Meaning, like, say if it like, for example, if it didn't have newsletter or like, for if it's if it said podcast, the crypto beat, it wouldn't go through.

### Guest (2026-03-16T17:44:19.514Z)

Right.

### Sean (2026-03-16T17:44:20.225Z)

It would just, like, stop. Stop the zap.

### Guest (2026-03-16T17:44:21.534Z)

Okay. Asking this also because we're about to rename all of the products. So I just wanna make sure whatever, like, naming convention changes we make still work with whatever formula you created.

### Sean (2026-03-16T17:44:33.025Z)

So send me you send me, the renames

### Guest (2026-03-16T17:44:36.644Z)

Okay.

### Sean (2026-03-16T17:44:39.615Z)

could still work.

### Guest (2026-03-16T17:44:40.074Z)

Okay.

### Sean (2026-03-16T17:44:41.265Z)

But, yeah, that to me whenever you

### Guest (2026-03-16T17:44:42.894Z)

Okay. Nothing like I mean, we're just, like, removing the block dot

### Sean (2026-03-16T17:44:44.545Z)

please.

### Guest (2026-03-16T17:44:47.504Z)

co from a lot of these and then like, the word newsletter will still be in the news products and, like, some of the display ad stuff isn't changing significantly, but I'll change you what the new ones are. So we're gonna do one newsletter. Okay. That's three. As far as no one has commented on how much money you're bringing in. I should've made it $500,000. And then and then we will hit our goals. Sponsorship product. One. I'm just putting these all in chat so you have, like, the records. Okay. And now you want one with something that would trigger and something that wouldn't. So, like, a sponsored post and a podcast.

### Sean (2026-03-16T17:45:55.295Z)

Yep.

### Guest (2026-03-16T17:45:56.174Z)

Oh, which would be?

### Sean (2026-03-16T17:45:57.855Z)

If you don't mind.

### Guest (2026-03-16T17:45:58.124Z)

Think about that one. But I was just thinking multiple products because there's an email that comes afterwards, and I wanted to know if that email when that email is triggered, if it'll have both products on there or however many products are in the deal or if it just will send multiple emails. Let me say multiple K. We do have a Salesforce sandbox that, like, theoretically, we should be doing this in, but

### Sean (2026-03-16T17:46:51.365Z)

Uh-huh.

### Guest (2026-03-16T17:46:51.724Z)

it's fine. I've become a lot less don't don't mess things up now that I don't have an admin for, like, however many years in a row.

### Sean (2026-03-16T17:47:06.775Z)

So, yeah, let's just see what happens.

### Guest (2026-03-16T17:47:07.704Z)

I mean, this I know is not gonna break anything. But And that you can delete it. Yes. Okay. Let's do display ads, a newsletter, and do you have a bit doing, like, research on mocks also? We didn't include those. Okay. Usually, those assets there is no assets because the conversation is directly with Steven. And it's, like, already scoped out in the contract. So it should is will that count as one of my products that it's not pulling? So, like, this will be the bundle test where it has a newsletter, but it okay. Had to beat Gina for today. She already put in two.

### Sean (2026-03-16T17:48:07.555Z)

Oh, yeah. So, also, Carla, that's a good question. So in if someone puts in for for example, the three that, Lil just put in for, if one of them isn't like, the actual sponsored like, what like, pretty much what you had me set up I'm trying to think, yeah, this is a good test because I have no idea whether or not that would actually if

### Guest (2026-03-16T17:48:30.234Z)

Trigger it.

### Sean (2026-03-16T17:48:30.845Z)

them would go through or because it it it always gets triggered. It's just a matter of going through the filters and what goes through like, what the filters allow.

### Guest (2026-03-16T17:48:37.504Z)

Mhmm.

### Sean (2026-03-16T17:48:39.975Z)

So, like, so that's that's where the email question comes in. Like, what is actually getting sent through the email?

### Guest (2026-03-16T17:48:51.064Z)

Okay.

### Sean (2026-03-16T17:48:53.235Z)

Close one.

### Guest (2026-03-16T17:49:07.234Z)

Okay. So then when we want one now with only a product that it would not pick up. That would be the last. That's funny. What? Okay. We'll go grab a snack. Did you do one with multiple products that it would pick up? Like, with all the products that it would pick up? No. Just multiple. I didn't this one was multiple, but we Well, one of them wouldn't. Research. Yeah. So I haven't done one with, like, only a newsletter and a sponsored post. Maybe that would be a good one. There's no chance that it just wouldn't trigger it. Right?

### Sean (2026-03-16T17:49:42.415Z)

That it wouldn't it should

### Guest (2026-03-16T17:49:42.934Z)

Sean? Or is there?

### Sean (2026-03-16T17:49:47.385Z)

like, as long as it's connected as as long as Zapier is connected to Salesforce, it should always get triggered.

### Guest (2026-03-16T17:49:54.204Z)

No. What I'm saying is even if there's let's say it has two products that you've included a form for, but one of them it didn't. Like, the the last one that Ldan just made, there's no chance that because of that, it won't trigger the Zapier. Or is it?

### Sean (2026-03-16T17:50:08.435Z)

Does it say it's it said closed one. Right? So, yeah, it'll always get triggered as long as it says closed one.

### Guest (2026-03-16T17:50:10.024Z)

Oh,

### Sean (2026-03-16T17:50:14.305Z)

It's just a matter of, like, after that, going through the filters, what gets stopped and what doesn't. Like, it does does adding one that isn't part of what we added in the forms If if that's not like, going through the actual filters themselves, like, would that stop? The actual zap from finishing the workflow?

### Guest (2026-03-16T17:50:34.254Z)

Mhmm.

### Sean (2026-03-16T17:50:35.545Z)

So that's definitely something to test.

### Guest (2026-03-16T17:50:38.444Z)

Okay.

### Sean (2026-03-16T17:50:46.755Z)

Because, like, would that happen? Like, say, like, you would get a newsletter a podcast, and okay.

### Guest (2026-03-16T17:50:53.864Z)

Yes. Alright. Here is test five. Sponge and multiple products. And what did we say the last one is? A single product? That is not supposed to be picked up. Did I do the one that should be already? One last item I already did. It felt like you didn't you do a campus one? Well, I did the pro and the and the renewal. So totally different records types, but within a sponsorship records type. We did, like, one line item should pick up multiple products with one thing it wouldn't pick up. Now I just did three products that should pick up all three. Okay. The only thing I haven't done is one product that shouldn't be picked up. Like, research unlock. Yes. Just like a stand alone Let's do that. What party? No. I don't need it. My, we have a tornado warning today, which is super fun, so kids are home. I don't have my phone, buddy. It's in the kitchen. They're making, like, slime and homemade Play Doh, and my kitchen is a disaster.

### Sean (2026-03-16T17:52:28.535Z)

I mean, I think it's harder to me. Homemade slime?

### Guest (2026-03-16T17:52:30.194Z)

It is. It is. It is a party. One product not picked up. I'm just saying. Maybe this will get everybody's attention.

### Sean (2026-03-16T17:52:53.745Z)

Like, oh my

### Guest (2026-03-16T17:52:57.894Z)

And they'll start closing stuff?

### Sean (2026-03-16T17:52:58.195Z)

yeah.

### Guest (2026-03-16T17:52:59.754Z)

Well, actually, sell some stuff. Yeah. Around the block. That will not pick it up. Right?

### Sean (2026-03-16T17:53:12.055Z)

It should not. Yeah.

### Guest (2026-03-16T17:53:12.714Z)

Great. $500,000. That's starting to get people's attention.

### Sean (2026-03-16T17:53:24.745Z)

David's gonna be like, man, I don't even have to release anything yet. Crushing it.

### Guest (2026-03-16T17:53:33.314Z)

Alright. Done. Oh my god. Okay. Cool. Cool. That's all the ones. That I can think of. Once I see the like, I'll think I'll be able to think of something else if you guys see any, like, oddities within what is and isn't triggering the flow. We do have, like, product IDs, which would make it a lot more fail proof than just saying, like, product name contains newsletter. Like, I could literally give you a list of product ID equals this, and then that's one eighteen digit unique identifier that will never change ever. Even if I call this product something totally different a year from now.

### Sean (2026-03-16T17:54:47.475Z)

Yeah. Could would you do that? Do you have that located anywhere, or you would have to do some digging?

### Guest (2026-03-16T17:54:53.914Z)

No. Super easy. I can just pull you product name with, like, a

### Sean (2026-03-16T17:54:54.505Z)

Okay. Oh, perfect. Yeah. That would make things a lot more

### Guest (2026-03-16T17:54:58.134Z)

column for ID. Okay.

### Sean (2026-03-16T17:55:01.745Z)

accurate. Awesome.

### Guest (2026-03-16T17:55:05.964Z)

Cool. What else you need from me? I think that was all. How would that work, Lil, if if we're doing product IDs? How would that work for like, the daily newsletter? Is there a different product ID for when someone buys one versus when someone buys three or six? Or whatever? Oh, no. It's the same product. Your quantity is different. So, like, looking at this product as an example, there's a quantity field on everything. So when I buy, like, Oh, maybe I'm thinking, like, newsletters was a bad example. I'm thinking, like, sponsored posts. I know that there's different products Correct. But there's not gonna be three IDs for a three post bundle. It's one ID for the product that says it's three sponsored posts. Okay. Okay. So here, for example, like, we have a separate line item for a bundle of 10, Mhmm. But that product With the same ID. One ID. There's just a quantity of one on this because it's already a bundle of 10. Got it. Okay. Cool. And then sometimes if they sell, like, seven and it's not one of our existing bundle types, Gina will put it in as one with a quantity of seven. Okay. But you're not triggering, like, or are you seven different somethings if there's a quantity of seven. Like, if somebody bought It would just be one. Okay. But that's interesting, though. Like, if they buy a packet of 10, are you asking to gather you're not, like, gathering all of them upfront because they're probably over the course of a year anyway. Mhmm. Okay. Okay. Yeah. So I'm basically gonna give you a list like this. It just includes name, product ID.

### Sean (2026-03-16T17:57:09.975Z)

Perfect.

### Guest (2026-03-16T17:57:12.794Z)

Cool. Let me know when I can delete those.

### Sean (2026-03-16T17:57:16.705Z)

Yeah. I'm gonna continue working on that and then testing and yeah, if it ends up working out that it's a lot better for using the product ID, then I'll incorporate that as well.

### Guest (2026-03-16T17:57:25.934Z)

Yeah. It's just it's more like

### Sean (2026-03-16T17:57:27.845Z)

But

### Guest (2026-03-16T17:57:29.614Z)

as long as you keep me in the loop and we are, like, telling you what the product name is, if

### Sean (2026-03-16T17:57:30.765Z)

yeah,

### Guest (2026-03-16T17:57:34.284Z)

fine. But I don't like doing things in a way that requires edits on like, multiple.

### Sean (2026-03-16T17:57:42.665Z)

we're good.

### Guest (2026-03-16T17:57:43.024Z)

Makes sense. Yeah.

### Sean (2026-03-16T17:57:44.745Z)

Hello.

### Guest (2026-03-16T17:57:45.604Z)

Right. Cool. Okay. Thanks, Will. No problem. See you guys.

### Sean (2026-03-16T17:57:48.555Z)

Later.

### Guest (2026-03-16T17:57:49.284Z)

Bye. Bye.

