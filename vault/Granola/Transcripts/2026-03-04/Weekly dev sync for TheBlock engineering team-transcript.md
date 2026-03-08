---
granola_id: 55227379-efb9-49c8-89c6-cef26ffb3921
title: "Weekly dev sync for TheBlock engineering team - Transcript"
type: transcript
created: 2026-03-04T14:55:02.338Z
updated: 2026-03-04T15:23:16.632Z
attendees: []
note: "[[2026-03-04#Weekly dev sync for TheBlock engineering team]]"
---

# Transcript for: Weekly dev sync for TheBlock engineering team

### Guest (2026-03-04T14:59:37.614Z)

I use Firefox, and it won't let me share my screen. So I had the open Chrome and use it. And then I someone had to approve me. So yeah. K. Get it. But I'm not logged in to Chrome because I don't because I have to open two f eight, and my phone is in my room. So yeah. For a long morning. Alright, Maria. I just pushed up doesn't matter. Same code. It's just the cleaner. So this is Oops. Cool. We should be good. Let me know if it doesn't work. Sorry. Stop. I'm stopping this this share. But, yeah, let me know, Maria.

### You (2026-03-04T15:00:45.044Z)

You guys all good? Alright.

### Guest (2026-03-04T15:00:51.824Z)

Yes.

### You (2026-03-04T15:00:51.864Z)

Sweet. How's everything going with the dev sync?

### Guest (2026-03-04T15:01:06.304Z)

Great. We had a small hiccup. The prices deployed, but we're fixing it right now.

### You (2026-03-04T15:01:10.954Z)

Awesome. Great. Thank you. Alright. We'll get started. So Alex is here. So Alex,

### Guest (2026-03-04T15:01:21.234Z)

So today, I saw that the images does not load for the Compass marketing page for Teams, only on the the box with my branch. I was looking to that. Found out that the one of the environment variables is not correct. But after fixing it, it didn't help much. So currently, we can do otherwise fixes. And then besides that, I've been working on the banner for data charts. And that's it.

### You (2026-03-04T15:01:53.874Z)

Cool. Thank you. Which of the campus, images were loading on the enterprise page? The, like, the thumbnails? Okay.

### Guest (2026-03-04T15:02:05.494Z)

Yeah. For courses. Have, like, a section learning task and currently two sections. And, yeah, preview images. Does not load.

### You (2026-03-04T15:02:16.904Z)

Gotcha.

### Guest (2026-03-04T15:02:17.264Z)

No. It don't load.

### You (2026-03-04T15:02:19.154Z)

Okay. Alright. Yeah. Keep us posted, please. Thank you.

### Guest (2026-03-04T15:02:23.204Z)

Oh, it was still in production and on the dev branch. It only affects my dev branch.

### You (2026-03-04T15:02:28.004Z)

It's on the it's on the what? The effects?

### Guest (2026-03-04T15:02:32.884Z)

Doesn't affect production and development bridge, but on the, like, my changes.

### You (2026-03-04T15:02:37.734Z)

Gotcha. Understood. Alright. Thank you,

### Guest (2026-03-04T15:02:40.944Z)

Alex, how Alex, how far away are you with data dashboard? Better? Well, currently working on the animation for mobile to switch them smoothly on mobile device. But beside that, it didn't take much long to finish it. Okay. So it Thank you.

### You (2026-03-04T15:03:06.354Z)

Thanks, Alex. Anna.

### Guest (2026-03-04T15:03:09.864Z)

Hello. So, yeah, regarding Alex comments, apparently, is a workaround for that marketing page issue. So I'll continue to see if the images are correct. So this is a ticket that came from the query. And then I'll so I'll continue with polymarket widget tickets. With my now just fixed. And we'll continue to look at Wolfgang's comments on the issue for work for it author editing. Because, apparently, for some users, it works. And for others, it behaves weird. So yeah. That's all from my side. Will you I don't know if you saw the comment that I that was that we found sort of yesterday after stand up was, like, a little bug that we found with the widgets for product market. Because when you are on that box and switch from dark mode to light mode, it seems like JavaScript broke or something. I don't know if this is something you're able to test to see if that's So I tried to replicate but I couldn't. I will continue while testing these other fixes as well. And let you know. Okay. Brian, were you gonna add something? Was gonna say the same thing. I gave it, like, thirty minutes, forty minutes last night trying to break it. Something else broke the JavaScript on your page. I couldn't reproduce it, and it was not the light mode, dark mode. But I've seen that before. It must be, like, some weird edge case or weird chain of events that makes it break, but the symptom is, like, and the thing we're looking for is the JavaScript breaks. And when you click the swiper, like, the text overlaps over each other. Something it's really weird. It's it's kinda hard to break. I don't know what happened, but it we I I couldn't get it consistently. Maybe you can find the case. But something breaks the JavaScript on the page sometimes. By clicking by clicking on things. So I'm also trying to reproduce locally on the bugs, but I failed. So it seems to be working, so it's hard to reproduce. Okay. Yeah. Can you take a look on it? If you see something, keep us posted. But if not, you know, don't kill yourself. Yeah. Is it going to be a showstopper for for the release of now? Okay. I don't think so. No. I I I probably just, like, have Anna take a look at, like, all the changes that you've made. And if everything looks good, then we can proceed. Okay. Well, we shouldn't we shouldn't we shouldn't deploy. Sorry. We haven't gotten the go ahead yet, but, like, we can prepare it basically for deploy. Okay.

### You (2026-03-04T15:06:07.034Z)

Alright. Cool. Thank you, guys. Hold on.

### Guest (2026-03-04T15:06:14.084Z)

Yes. Hi there. There is one more ticket prepared for ready for testing. I'll send the dev box to Anna. A bit later. And regarding I read a comment from Anna for that displaying the username tickets. And, that's not a problem. I would like to chat with her after the meeting because there's lots of things happening weirdly. Yeah. So that's pretty much it. We're working mostly on that and trying to figure out what's going on.

### You (2026-03-04T15:06:52.884Z)

Okay. Alright. Thank you, Bodan. Brian?

### Guest (2026-03-04T15:07:00.064Z)

Cool. Moving some tickets around and helping with the deploys today. Hopefully, we can get Polymark out as well.

### You (2026-03-04T15:07:05.304Z)

Nice. Great. Thank you, Brian. Caesar.

### Guest (2026-03-04T15:07:15.224Z)

Hi. I'm sorry. Yesterday, it was I'm sorry. Well, on Monday and Friday, I was working in the in several staffs, social media in Django because we changed medical or social. Finally, I was taking it from social. We can't use it. Because we need to upgrade this at least on ground. So I talked with Mike in order to create a new subscription metric tool and work at any of that. I'm getting more and more resources on video, so I I was working on this too. In a show on Friday, I created the full request for the. I have a comment from Nicholas to do a small fix. In that for weakness. I'm trying to do it today. In addition, I have a task from Vicky. In order to upload several invoices to Wiggly. On different services. I'm working on that right now too. Yeah. Starting a small pictures from different people.

### You (2026-03-04T15:08:35.004Z)

Cool. Thank you, Cesar.

### Guest (2026-03-04T15:08:35.384Z)

Yeah. That's fine. Thank you.

### You (2026-03-04T15:08:39.674Z)

Yeah. Don't apologize for taking a holiday. I hope you enjoyed it.

### Guest (2026-03-04T15:08:41.884Z)

Yeah. Yeah. But probably, I have to not try. Earlier. It was done. Suddenly when yeah. The the

### You (2026-03-04T15:08:51.764Z)

Gotcha.

### Guest (2026-03-04T15:08:53.164Z)

was. Yeah.

### You (2026-03-04T15:08:53.414Z)

No worries.

### Guest (2026-03-04T15:08:54.444Z)

Sure. Thank you.

### You (2026-03-04T15:08:56.294Z)

Thank you. Corey.

### Guest (2026-03-04T15:09:00.264Z)

Hello. I'm working on my monthly reports. And, also, I I open several tasks on SEO board. I didn't assign them yet. But maybe anyone volunteer can check. And take them. And, also, LLM TXT feature for campus one thing I'm working on, and I will open ticket to create one for the website. I think is good to try that. And, yeah, that's all.

### You (2026-03-04T15:09:36.314Z)

Cool. Yeah. I'd be interested in checking that out, seeing seeing what it actually entails.

### Guest (2026-03-04T15:09:43.444Z)

Try those tickets under the SEO app? Yeah. Yep. Alright. Cool. Check them out. Thanks.

### You (2026-03-04T15:09:50.774Z)

This one right here.

### Guest (2026-03-04T15:09:51.094Z)

Thank you. No. This is this is stuff assigned to him. It's probably unassigned to him.

### You (2026-03-04T15:09:54.974Z)

Okay.

### Guest (2026-03-04T15:09:58.524Z)

It's under the epic.

### You (2026-03-04T15:09:58.584Z)

Good. Understood. Christophe.

### Guest (2026-03-04T15:10:04.064Z)

Hi, guys. So yesterday, I got the access from Caesar. But it's too late, so I couldn't do it or remove big images. Code base one. But, yeah, I started working on the on the one with with the home page section. And, also, Anna texted me about testing my link removal tickets, so I I answered her. And, also, I think there are some things we need to discuss, so maybe I'll have a call with her later. And that's it for me.

### You (2026-03-04T15:10:31.564Z)

Cool. Thank you. Anna, you're busy. Thank you, Christophe.

### Guest (2026-03-04T15:10:36.484Z)

Sorry, Anna. Yes.

### You (2026-03-04T15:10:42.924Z)

Maria.

### Guest (2026-03-04T15:10:45.294Z)

Today, I continued working on adding our share of functionality share to Twitter functionality. Also did some fixes as brand requested on other election stuff and left a comment in Figma so that if you could check it, so it would be nice. Now checking the fix for prices.

### You (2026-03-04T15:11:14.064Z)

Cool. You left a comment, on the you're talking about the election coverage?

### Guest (2026-03-04T15:11:18.614Z)

It's on Sigma.

### You (2026-03-04T15:11:19.764Z)

Okay.

### Guest (2026-03-04T15:11:21.024Z)

Yeah. So I'll take it. I or some comment rather. I replied, let's see Serena's input. That's it. It's a good good call out, Maria. We missed that part. Missed missed redesigning that part. It's just always something.

### You (2026-03-04T15:11:42.094Z)

Cool. Thank you, Maria. Marina,

### Guest (2026-03-04T15:11:44.654Z)

Hello, guys. I'm still on the polymarket stuff. Today, I finalized all the comments that Polymarket team has given for us. So also to investigate the issue with the GS that switching themes, but I was not able to to do neither on my local machine nor on the dock box. So probably there are, as Brian said, some tricky steps. To to reproduce that. And apart from that, I'm also added targeting for Gum on individual prices page as we are going to release it So it's the only thing which is left as my side regarding gum stuff. So and my plan is to proceed with the polymarket form election stuff. That's it. So And do you while market fit in the card? That little CTA? Like, I've like, I I come up with a fix. Of it. So, like, like, you know, just make them smaller and adding three dots as we discussed yesterday. So if there is no need for putting everything just part of this will be shown. But it will be hard to reproduce, but, anyway, there there would be some edge cases. When it will be useful. Yeah. It looks really good. I like this. There's some might might be some dimension or some resolutions. That might not fit, but this I think this is Some sometimes the the time, like, time step information can be too long. Instance, one days, one like, like, one hour and forty minutes, something like that. It's gonna be too long. To fit it. So, like, another, like, trade off might be not like, printing, like, depicting everything like ours and just using first letters. So it also will shrink this content, but I I'm not sure. So let's see what they say. If if anything, can introduce it anytime. And maybe my question would be regarding deployment Are we planning it or we are waiting I was actually just gonna speak on that. We're holding off. I I don't know if Matt said anything to you, but they haven't paid us yet. So, yeah, we wanna hold off until they pay us. I don't think would be Yeah. I saw the conversation yesterday in the channel They basically said that like, the invoice is coming. So like, Jeff was asking about the state of the deployment. Like, are we preparing to do it or not? Like, it's it's basically it's it's most likely gonna be tomorrow. That's what I would say. But if I have to bet money. Yeah. Okay. It's in the mail. Classic. Yeah. Okay. Thank you, Marina.

### You (2026-03-04T15:14:55.684Z)

How much do you wanna bet? That they're gonna pay us?

### Guest (2026-03-04T15:14:59.654Z)

Oh, can we can we open up a small little prediction market on Polymarket to say? No. No.

### You (2026-03-04T15:15:10.524Z)

Alright. Thank you, Marina. Mike.

### Guest (2026-03-04T15:15:13.794Z)

Finding AI Pro API, those are not next up. I didn't get to those yesterday, but I got iOS digest. Shipped today with the notifications update. Campus authentication, wanna ship that soon. It's close. I just need to get it in testing. Testing, that one is a little bit more trickier because it it has a lot of moving parts and need to get it up on, like, a dev box somewhere. So I'm a work on getting the dev box up for it so we can test it out. I'll have to, like, ship a test build that points to those.

### You (2026-03-04T15:15:50.394Z)

Nice.

### Guest (2026-03-04T15:15:50.704Z)

But, yeah, then I'm hitting Summit AI and Pro API. So

### You (2026-03-04T15:15:57.354Z)

Come in. Thank you, Mike. Nikita.

### Guest (2026-03-04T15:16:05.194Z)

If you've well, I'm continuing to work I've started to continue to work on on the payment setup, resurrected every everything that I had prior. And continue to work on that and also got a few tickets from Rob for few tickets from Roma today. But a few small adjustments, we should also go into this release. I'm done with those. Those are already deployed to dev as well. So, yeah, we'll continue to work on the on the payment setup, and that's all.

### You (2026-03-04T15:16:41.094Z)

Perfect. Thank you, Nikita. Nikita. Oh,

### Guest (2026-03-04T15:16:45.954Z)

Yep. Similar thing on my end. Started revising and rewiring whatever we had for the payments for the new payment flow for the Stripe. Was working on a few bugs on the campus back end. Got probably the most beautiful project overview from Nicola. So he shout out to Nicolas because it was just, like, sitting in the theater and watching the most beautiful storytelling you may. Imagine, to be honest. And, yeah, we will continue our dive through the WordPress later, but the first part was a brilliant one already. And, yeah, that's it. We also deployed a little migration to the prods and fixed the credits for the individuals. So now all of the credits are fixed both for the individuals and the team organizations. So that's

### You (2026-03-04T15:18:01.634Z)

Awesome.

### Guest (2026-03-04T15:18:02.844Z)

that's it on my end.

### You (2026-03-04T15:18:06.314Z)

Thank you. Nikola,

### Guest (2026-03-04T15:18:11.124Z)

Yeah. Translations. Yeah. Still we'll meet with Ed after the stand up to go through, like, the current progress and review some questions that with Corey as well. Yeah. That's that's it.

### You (2026-03-04T15:18:33.554Z)

Cool. How are you enjoying Cloud Code? Did you get used to it yet?

### Guest (2026-03-04T15:18:35.834Z)

They're pretty nice. Yeah. So

### You (2026-03-04T15:18:36.404Z)

Yeah.

### Guest (2026-03-04T15:18:39.364Z)

looking at to the left right now, so I'm using Claude. Okay.

### You (2026-03-04T15:18:42.264Z)

Gotta keep tabs.

### Guest (2026-03-04T15:18:46.014Z)

Thank you.

### You (2026-03-04T15:18:47.174Z)

Cool. Thank you, Nikola. Rommel.

### Guest (2026-03-04T15:18:50.124Z)

Awesome. Yeah. So I'm working mostly on campus. We we've done we've case mitigation with. It is done. Now he's fixing bugs and Nicky Tagulis both of them And also started crypto jobs. Again. So yeah. That's what I'm doing now. Yeah. I saw I saw a little comment on on think on the dev sync I think Nicola maybe left it in terms of job boards if there's a deadline or something. Mhmm. There's no the answer there's no strict deadline. It's just wanna just be ready, basically, to launch at a moment's notice. Jeff is working on securing clients and, like, you know, basically, like, third parties who could who would be our clients and list their jobs on the database. So that's in progress and close to being done, but I'm I'm supposed to get a notice on that. Yes.

### You (2026-03-04T15:20:05.004Z)

Alright. Cool. Ed got anything? Have you been bringing it up?

### Guest (2026-03-04T15:20:12.044Z)

No. I don't think so. No. Okay. Yeah. Most of the stuff has been just

### You (2026-03-04T15:20:12.444Z)

Cool.

### Guest (2026-03-04T15:20:16.144Z)

communicated Mhmm. Figma files and channels with feedback. Also, huge shout out to

### You (2026-03-04T15:20:21.644Z)

Gotcha.

### Guest (2026-03-04T15:20:25.514Z)

for the pushes for to next four. Lastly, data pages have been tremendous success. Don't know if everybody saw the Ask product management channel, but our data pages at least the initial impact is, like, three x to traffic. So

### You (2026-03-04T15:20:43.394Z)

It's wild.

### Guest (2026-03-04T15:20:44.764Z)

it's, like, incredible And I cannot cannot wait for prices to And now I'm, like, wishful thinking, and then I'm thinking about prices already. But

### You (2026-03-04T15:20:55.034Z)

Don't get greedy, Ed.

### Guest (2026-03-04T15:20:55.414Z)

we'll see. Yeah. I know. I know. I gotta stay grounded.

### You (2026-03-04T15:21:03.544Z)

Alright. Cool. Yeah. And I'm finishing up the Zapier stuff today. So I'm just gonna keep on testing that and making sure. So that's my focus for today. And then, yeah, ETFs and ticket stuff. And then, little out of me on the campus, pretty much organizer. I'm just, like, taking care of, like, all the tickets for that. So and Salesforce. So I'm just taking a look at that. So those are all my updates. Does anybody have anything else that they wanna talk about?

### Guest (2026-03-04T15:21:38.614Z)

Maybe maybe I have one question.

### You (2026-03-04T15:21:40.364Z)

Alright.

### Guest (2026-03-04T15:21:43.194Z)

How often is the crypto AMA? Like, the

### You (2026-03-04T15:21:47.294Z)

It's usually every

### Guest (2026-03-04T15:21:48.374Z)

I think it's supposed to be

### You (2026-03-04T15:21:49.864Z)

yeah, every every two weeks.

### Guest (2026-03-04T15:21:52.774Z)

Okay.

### You (2026-03-04T15:21:53.614Z)

Or every other week?

### Guest (2026-03-04T15:21:54.554Z)

Yeah. Although I think it's every other week. I think it was canceled the other week. Yeah. I think last week, I think it was canceled. And this week was supposed to be the missing missing week one. So I think we'll have a three week break. Since the last one. But, yeah, next week, it's scheduled.

### You (2026-03-04T15:22:14.704Z)

Yeah. And I don't know if you guys saw, but,

### Guest (2026-03-04T15:22:14.954Z)

Alright. Thank you.

### You (2026-03-04T15:22:19.374Z)

Larry posted his book on GitHub. So it's free. I'm checking it out. So if anyone's interested, do you remember what, was that in general?

### Guest (2026-03-04T15:22:30.064Z)

You can find on his student profile. It's a viral post.

### You (2026-03-04T15:22:31.944Z)

Cool.

### Guest (2026-03-04T15:22:36.764Z)

But probably general as well. And also, Christophe, did you still have any issues with the email or with your calendar? Yeah. I mean, I still don't see the meetings there, but I just joined the same link. Okay. Just I know we gotta figure out. Just DM me if I forget to, like, circle back. Alright. No worries. No worries, man.

### You (2026-03-04T15:23:00.784Z)

Alright. Cool. Thank you, guys. Enjoy the rest of your evenings, and I'll talk to you tomorrow.

### Guest (2026-03-04T15:23:07.434Z)

Thanks to you guys.

