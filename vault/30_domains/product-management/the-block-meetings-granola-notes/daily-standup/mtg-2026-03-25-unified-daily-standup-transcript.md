---
granola_id: e282c683-f334-426e-935f-12793ccc4478
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of unified daily standup - transcript.
context: the-block
created: 2026-03-25
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

### Guest (2026-03-25T14:01:08.597Z)

Hey guys.

### Sean (2026-03-25T14:01:11.050Z)

How's it going everybody?

### Guest (2026-03-25T14:01:15.637Z)

Good.

### Sean (2026-03-25T14:01:52.250Z)

Brian is out today. I'm going to go ahead and get started. We'll start with Alex.

### Guest (2026-03-25T14:02:11.317Z)

Hello. So I did a code review for one of my US tickets. Then I've been working on the job aggregated view ticket because Ramo went violent and created like plenty of test cases there. So now I need to take a look at those. There are more than 30 now. And that's it.

### Sean (2026-03-25T14:02:30.970Z)

30 test cases. Oh geez. For the heads up. Anna.

### Guest (2026-03-25T14:02:42.757Z)

Hello. So I will continue with the newsletter expiration part. That seems to be working, but I'm saying to see like all the other edge cases. Also, we'll continue with key races tickets for the lecture hub. And as for updates, I finished testing Kristoff's buck for updating articles on hero section and waiting for him. That's a very great. And also the SEO tickets that both have worked on is ready. And Alex tickets for come prepper heat pack. Looks good. So those three are ready for deployment.

### Sean (2026-03-25T14:03:25.130Z)

Perfect. Thank you, Anna. From Alex. Bad. An.

### Guest (2026-03-25T14:03:35.397Z)

Yes. Hello there. So we. Got, let's say one issue with that ticket for embedded data chart. But we fixed it. Me and Brian, we kind of found a way how to properly test it. There was an issue that. It's, it was practically impossible to test like duplicated Google analytics events. Neither on local nor on dev instance. But we kind of found a way and we fixed our also. We made a fix and now it's from production. And yeah, that was the main thing I was doing yesterday. And yeah, also the ticket for RCTP is kind of ready for testing. But I left a comment for Anna because it's also a little bit tricky. That's pretty much it.

### Sean (2026-03-25T14:04:33.770Z)

Perfect. Thank you, Bad. An. Caesar.

### Guest (2026-03-25T14:04:44.037Z)

Hello. While I keep working in the same than yesterday migrating workflows from github to workflow. Yesterday I had some problems with airflow. I broke airflow during three, four hours. And finally I achieved two fix. In addition, I deployed yesterday. The J redirect from the lockdown Pro. So it's deployed in prod.

### Sean (2026-03-25T14:05:20.410Z)

Perfect. Thank you, Caesar.

### Guest (2026-03-25T14:05:23.797Z)

Ucing. Hello. I started another crawl on a strips and screening frog to create a list of broken external links for Nikola and Kristoff. And also I work with cocoa for geo package for the clients. And also she mentioned me other selling options for like data dashboard pages and learn pages. We also discussed about other selling options for PR posts. And also working on geo improvements for campus and pro and finally spam update announced yesterday by Google. And I am checking the impacts so far so good. But it will take a couple of days. To roll out and I will be taking the results. That's all.

### Sean (2026-03-25T14:06:27.130Z)

Thank you, Corey.

### Guest (2026-03-25T14:06:30.917Z)

Corey, do you have an idea of how many. Assets do we need for Price's FAQ page just like we do for the time being? Like, I don't know if you want to wait and do 201 ones like a few months from now or should we do like one now. And then I don't know assumption tomorrow at. Okay. So thank you. Everyone. I have been working on the script for it to upload a few Akwe and I will also deploy the ticket which Anna just reviewed with the hero catch upload. So I'll deploy that and continue working on the script.

### Sean (2026-03-25T14:07:20.650Z)

Perfect. Thank you. Bria.

### Guest (2026-03-25T14:07:33.637Z)

Today I finished with a report cards page sending the ticket to review. Right now I'm working on some of the suggestions that Alex left to my previous PR about X sharing functionality and tomorrow I'm going to start working on Price.

### Sean (2026-03-25T14:07:51.530Z)

R.

### Guest (2026-03-25T14:07:58.197Z)

Search improvement. It's lower.

### Sean (2026-03-25T14:08:06.490Z)

You got caught up here. Okay, gotcha. Price pages. Okay. Cool. Thank you, Maria.

### Guest (2026-03-25T14:08:26.277Z)

Yep. So apart from continuous work on UI 4 sponsored courses, we together with finished the payment setup with the. With the older design and the new functionality. So then Sean, if you don't mind, we would like to stay on the call maybe for like no more than 10 minutes. We want to show you whether or not it's sufficient. Should be and also we have one idea on improvement regarding the 100% discount. So wanted to run it by you. Whether or not it's worth implementing. It's. It's a tiny thing. It's more so the. Ux thing. And that's about it.

### Sean (2026-03-25T14:09:18.010Z)

Thank you. Yeah, I'll stick around. Nikita. O.

### Guest (2026-03-25T14:09:28.917Z)

The same update on my end. But yeah, regarding the 100% promoles, it's more about like the idea to overcome this tribe limitations. And possible risks of spending the time where we don't need to spend it. But yeah, it's mostly done to be passing on testing. So just want to figure out like the last few questions before passing it to testing and switching back to the sponsor courses.

### Sean (2026-03-25T14:10:05.850Z)

Connell gotcha.

### Guest (2026-03-25T14:10:06.997Z)

And yeah, the code thing is just insanity comparing to the codex and the chat GPT models. I'm not sure why I exactly did not even try to before. But now. It's much better.

### Sean (2026-03-25T14:10:30.090Z)

So you were using codecs before and then you just switched to Claude 4.6.

### Guest (2026-03-25T14:10:35.717Z)

Yeah. What if you plug in thanks to Nick recommendations? But yeah, it's just an insanity.

### Sean (2026-03-25T14:10:44.810Z)

Perfect. Cool. Yeah. Glad to hear that. Thank you, Nikita. Michaela.

### Guest (2026-03-25T14:10:53.317Z)

Hello everyone. So. Yeah, still working on translations. So wrapped up like most of it including the language switcher like in the top navigation and now working on setting up the dev box for it. Currently working on making sure that we can install the WordPress plugin through composer, which unfortunately is not supported by the plugin itself, but like a third party like open source tool that some someone provided. So we are working on that. So. So we kind of follow the same pattern like we have for all other plugins. Yeah, that's about it.

### Sean (2026-03-25T14:11:44.730Z)

Thank you, Nichola. Rama.

### Guest (2026-03-25T14:11:50.437Z)

Hello people. So I can see working on crypto jobs. Almost done. There. And so we will wait for. Pixel from Alexander. And we'll test once again. And that will be all for crypto jobs. And working with my other test.

### Sean (2026-03-25T14:12:19.690Z)

Nice. Perfect. Thank you very much, Ram. A. Ed, you got anything?

### Guest (2026-03-25T14:12:31.397Z)

No, nothing else to add.

### Sean (2026-03-25T14:12:34.730Z)

Okay. Yeah, same with me. Just pretty working on the same stuff that I was working on yesterday. So just continuing. That train. And yeah, that's really about it. Does anybody have anything that they want to discuss before we head out?

### Guest (2026-03-25T14:12:54.597Z)

Actually, Nichola. Should we meet this Friday to talk translations or not? Ready? Yeah, let's do it. Yeah, let's do. It. Let's set up something. Some of my meeting or something. I'll put it down. Yeah, thanks.

### Sean (2026-03-25T14:13:16.810Z)

All right, cool. Yeah. So I'll be staying with Nikita's at as well. I'm sure. And yeah, for the rest of you, don't want to stay and hang. Have a good rest of your evenings, rest your mornings. I'll talk to you tomorrow. Thank you guys.

### Guest (2026-03-25T14:13:34.357Z)

Thank you. Bye.

### Sean (2026-03-25T14:13:43.210Z)

Want to share your screen?

### Guest (2026-03-25T14:13:45.637Z)

You could also. See my screen. Guys.

### Sean (2026-03-25T14:14:07.850Z)

Yeah, yeah.

### Guest (2026-03-25T14:14:08.997Z)

Yeah. Okay. So the first thing first. You do remember we had the possibility to provide the promo code before even entering the email address. Right now I needed to disable it because there is a stripe limitation. There are two things. Either we can create the checkout session with the promo code attached. And user have no possibility to adjust them later. So if the user will delete the promo, he won't be able to attach a new one. Or we don't allow the user to enter any promo code before entering the email address and before the session will be created. But then user can play around as many as he wants with the promo codes. So it sounded like it's better for us to disable it before you will enter the email address. And allow you to play fully with them. Once the session will be created. Session is being created once you will enter the email address. I don't see a problem with that. What was the was that just like, I don't know, requirement or some sort of journey that we had designed before to enter the promo code before. Is there like, was there a specific need for it that I'm not sure it was a need for that? We just did it. It was the original design. And since we're doing the new flow based on the old design, I just saw that as the problem, because of the stripe limitations. And I saw like we found it like the most. Good way to overcome. This rep limitations. Yeah, that makes sense. Okay. So then the user entered the email address. The form is loading as well as the possibility to add the promo code. Here. So it will dynamically be added as a button. And then you will just click enter. The same thing. As it was before. So. The normal flow is working fine and I want to talk a bit more about the 100% promo codes. Because as we talked about that before, we probably don't want to collect the payment details from people if they're using the 100% promo code. And stripe actually allows us to do it. The thing is, it's not that obvious for the user. You see if you entered all of your details here, then you go, for example, and enter the promo code for 100% off. The total view is zero dollars. And the pay button right now is attached to the stripe flag which defines can the user complete the session or no. Has the stripe all necessary details to complete the session. And you see there is no payment details entered. Only the billing info, the promo codes and stripe don't require the payment information being entered. But it's not obvious for the user. Right. So we thought what if we will show a little static thing on top of the payment block, the same one we have for the email when you're entering kind of the corporate email and we show you the notification, hey, you probably use the corporate email most likely you need the team product. Just the greenish background thing and the text inside of it. We can reuse the same one. On top of the payment block saying like you may now proceed without attaching the payment method. You can do it later. Blah, blah, blah. So the user will know for sure that the payment method is not required. Because it's indeed not required. The problem is if we try to dynamically show and then show the payment block depending on the promo code state. It has the large risks of becoming a pain in the ass from the implementation perspective. Possible stripe issues. So we thought it might be good to have like the most. Friction way to handle it just to show the static thing. When we need it. To say like, hey, you can complete without providing us any payment details. Because what if the user entered the promo code right now? Or, you know, like went through the whole flow, entered the payment details and only after that he entered the promo code should we remove the payment block with the answer details. But what if the user will then remove the promo code? Should we render the payment block again? So, you know, like a lot of possible edge cases, we probably don't want to handle and spend the time on. So the payment block is always visible. With the possible different payment options. But only the static notification will be dynamically shown and not shown depending on the op promo code applied. Could we grade out if you notice that you have a full promo code attached like, you know, like in this scenario. And it just sort of like. Almost disables the card information section. Most probably no, I mean like we can take a look at that. But all those elements are being rendered by the stripe. So we only create. A workaround around the stripe elements. So strictly speaking, we can place an overlay. On top of it. A separate one from stripe. We can disable click events on this overlay. In this case, and it will overlap with the stripe elements. So we would not pass those clicks through and apply some sort of filter like grayscale, for example, to gray out. Underlying elements which would be stripe. So we are not interfering in this case with stripe themselves. We are sort of placing a cap on it. So yes, it is possible. But if the user partially provided the payment details, the stripe will fail to confirm the session because the validation will fail. And we will need to clear up the data or complete them. Let's see if we can play around this. So the answer would be maybe then get a brought up a valid point. I'm just thinking of the ux. Just to show you how the possible how the notification thing may look like. Let me just do it right now. So you see like the greenish background thing with some kind of text in it. Pretty much the same one, but with the different copies saying like you may now complete without providing us the payment information and that's it. In that case, it will be the only thing we actually need. And the rest will by the stripe. So if you partially entered you either need to clean them up completely or finish them, but it all will be handled by the stripe. So we don't need to play around with the overlays with whatever. We've seen the invocation that you have that like the banking info is not needed or something like what would the notification say? Yeah. So if you applied the 100% promo code, we can just say something like you may now proceed without completing providing the payment methods details. You can you will be able to manage it later on inside of the canvas. Once we'll launch the account management. Thing. Yeah that makes sense. Because earlier what Michael actually did once we had that case and we needed. To start handling those 100% promos. He did the thing to even escape rendering. For all stripe elements. So you just enter the the email, the name. And if you entered the promo here boom you are down. You will see the success screen. Right now. It's kind of. Impossible to do it that early because on the first step we collect only the email. We don't need the name. And then the name and the name is a part of the billing information. It's just the separate stripe elements. We change the way how we show the elements because previously it was a lot of our own code on top of the elements. And right now it's more about like the constructor. With our styles, but the stripe elements themselves. On the new rails. So if you apply the full promo code and then you try to add banking info even if we don't want you to. It will be fine. We will attach them. Yeah, but you won't be charged. Yeah, right. Okay. So it just works. It's just like it's like a UI ux issue where. It's yeah, yeah. So the bottom will be once you. Yeah, that's fine. Yeah, I think bottom line I think is fine. Sean, do you have any like reservations about this?

### Sean (2026-03-25T14:25:33.850Z)

No reservations. Yeah, because I was just trying to think of how.

### Guest (2026-03-25T14:25:34.117Z)

Maybe we're just.

### Sean (2026-03-25T14:25:37.610Z)

Like, I don't know, I've used Stripe in the past when it comes to logouts. And I'm trying to think if there is an element where it just doesn't. Like the banking info doesn't pop up when you do enter a promo code. But it sounds like, yeah, it's way too much implementation work and it would be too much of a workaround.

### Guest (2026-03-25T14:25:59.877Z)

We will have to return to the previous.

### Sean (2026-03-25T14:26:02.090Z)

Yeah. Exactly. So yeah.

### Guest (2026-03-25T14:26:07.237Z)

Status.

### Sean (2026-03-25T14:26:08.170Z)

In the end. Yeah, I think it'll be fine.

### Guest (2026-03-25T14:26:10.677Z)

That's the notification.

### Sean (2026-03-25T14:26:13.130Z)

Yeah.

### Guest (2026-03-25T14:26:13.317Z)

Okay. If you can write us some copies here that will be perfect. And we'll. Add the rest. Yeah, basically just what we want to tell the user to proceed forward.

### Sean (2026-03-25T14:26:34.250Z)

Cool, you got it.

### Guest (2026-03-25T14:26:36.037Z)

Like the idea not to confuse, not to stop and explain that the payment methods attachment is optional at that moment.

### Sean (2026-03-25T14:26:46.730Z)

All right, cool. And do we have, are we doing the promo code? Is this for previous users that are trying to get access to 201 like that already paid for like, what was the 100% Promo code for?

### Guest (2026-03-25T14:27:05.237Z)

Either one offs right of the one. Off what we want to provide access. People. Like select individuals. Yeah 100%. We don't have that many of them. Right. We don't let people we waive access to. So like. Think I don't know. Potential maybe employees of the block. Let's say. Huge partners like stuff like that. I don't know people don't we don't want to collect info or connect payment from. Yeah so if all of this is probably going to be like more than like HKC if anything. So. It's not have to be ready for this scenario. That's all.

### Sean (2026-03-25T14:27:58.650Z)

Yeah, no, for sure.

### Guest (2026-03-25T14:27:58.677Z)

That's I'm not worried about like whether it's a notification or blackout like it's. Off oh I see it. Was. Oh it was used by Mike. Maybe we didn't have it like in real. At all. But.

### Sean (2026-03-25T14:28:34.410Z)

Well, it could also be the potential of. Someone trying to access 201 down the line like that already purchased the all encompassing package. So. Yeah, that makes sense.

### Guest (2026-03-25T14:28:44.997Z)

Yeah yeah we still need to handle that scenario and the quick thing regarding the emails. Oh no just for the nearest feature right now we basically hard coded the name for the product like campus for individuals but since there will be a division between the 101 between 201 and the all access we most probably need to change the name in here as well as on the email with the receipt. So I went ahead and changed it a little before that we had just like the campus for individuals payment confirmation and the product name here was always campus for individuals. Did it I changed it a little I just modify it like campus for individuals digital assets essentials 101. Like a little tweak and since we did not covered the 100 promo codes before I just changed it that as well to include that the payment method was the promotion code 100% discount makes sense.

### Sean (2026-03-25T14:30:06.170Z)

Yeah, that works.

### Guest (2026-03-25T14:30:07.637Z)

Yeah but. When the tier one will be released for the individuals and with all access and blah blah blah we will might need to update the rest of the email plus what we are showing here on the checkout because right now it's fine. Because it's only just one product for everyone but once there will be more products we definitely need to revisit that little thing again.

### Sean (2026-03-25T14:30:39.290Z)

Okay, yeah, so just tweaking the text after everything's available just to make sure. That everyone. Okay.

### Guest (2026-03-25T14:30:50.117Z)

That thing inside of the products in the receipt thing is fine to go into live even right now. The small change here but if you want me I can just revert it. So it will be campus for individuals until we'll release 201 ML access for every individual. S or we can just keep it and that will be it. Until we're ready for 2021. And we just have the updates. So. What's your question? I mean do you want me to revert that little thing for the product in the payment confirmation or we can keep it? No, this is fine. I think that's basically it on my end so we just need to copy what will do the little thingy on top of the payment form. Payment block and I think that will be it.

### Sean (2026-03-25T14:32:10.650Z)

That works. Thank you.

### Guest (2026-03-25T14:32:17.077Z)

Thank you gents. See bye.

### Sean (2026-03-25T14:32:23.130Z)

Guys.

