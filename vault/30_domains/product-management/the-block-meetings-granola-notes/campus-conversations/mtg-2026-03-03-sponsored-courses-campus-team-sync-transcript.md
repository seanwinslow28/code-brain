---
granola_id: 0456b9cc-e958-40d5-ba07-856a4ac64a12
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of sponsored courses - campus team sync - transcript.
context: the-block
created: 2026-03-03
source: granola-sync
attendees:
  - ddebreczeni@theblock.co
  - erupkus@theblock.co
  - mhulis@theblock.co
  - norobenko@theblock.co
  - cdaumur@theblock.co
note: "[[mtg-2026-03-03-sponsored-courses-campus-team-sync]]"
---

# Transcript for: Sponsored Courses - Campus Team Sync

## Attendees
- David Debreczeni (ddebreczeni@theblock.co)
- Ed Rupkus (erupkus@theblock.co)
- Maria Hulis (mhulis@theblock.co)
- Nika Orobenko (norobenko@theblock.co)
- Claudine Daumur (cdaumur@theblock.co)

### Sean (2026-03-03T15:45:12.324Z)

Everyone.

### Guest (2026-03-03T15:45:14.214Z)

Hi.

### Sean (2026-03-03T15:45:34.594Z)

So we're just waiting on Nikita and Claudine.

### Guest (2026-03-03T15:45:41.864Z)

Yep. Basically, what we wanted to do is make sure that we're all on the same page as in preparation for sponsored courses. Just to chat about, like, what does a sponsored course experience look like? On on campus? Like, what's what's viable and what's not viable? And yeah, how does, like, Rise three sixty play into all of that. So just know, just just a design. Product and engineering is all on the same page in terms of that because either, you know, we would love to have upsells as much as possible given that a sponsored course is free to take. So you could have people who are not paying any subscriptions taking these courses, And if and if it'll be possible to, like, showcase the upsell opportunities as well for the paid for courses. So just wanted to chat with the team what the whole experience looks like.

### Sean (2026-03-03T15:46:45.054Z)

Yeah. David did

### Guest (2026-03-03T15:46:49.634Z)

So yeah,

### Sean (2026-03-03T15:46:50.894Z)

go ahead.

### Guest (2026-03-03T15:46:51.294Z)

Yeah. In terms of differences between between the rise and storyline, Storyline produces the same format as you've seen with the two zero one. Which is a slide based, more like classical long form learning experience. Arise, on the other hand, is more like a one pager web website where you're as you're going down the new content just loads in. So instead of having individual slides, you're essentially your logged in to mostly one screen, and then you're progressing. Dialogues progress as as you progress. The main the only shortcoming is with the voiceovers that rise Although it does support voice overs, it very clunky. It inserts a little player into each and every block. Of text. So instead of playing continuously like, the user would need to play them one by one, which is just breaks the ball experience. So we generally do not use voice overs with the RISE courses. But they are responsive. While storyline courses are not. So it's easy to complete the course even when you're phone. But I I wouldn't advise that it's 39. So, yeah, that's the main main difference is I think I've shared or I can still

### Sean (2026-03-03T15:48:33.324Z)

Yeah. I'll share

### Guest (2026-03-03T15:48:34.204Z)

can still share it. But there's

### Sean (2026-03-03T15:48:40.404Z)

This right here, David?

### Guest (2026-03-03T15:48:42.614Z)

Yep. That one. So, yeah, that's how it looks like. And just so just so that catch up everybody on what we're speaking about. So, basically, we wanted to just be on the same page, all design product and engineering. Of the sponsored courses and, like, what that might look like on on campus. So, yeah, we're just chatting about the specific I don't know if that's the right word. Format or infra for her for the course. The sponsor course specifically. For those, like, short shorter form courses that could live on campus. So could this could this my question for me is, could this be a pop up window in on the campus dashboard? Or no? The course the course itself is that what you're asking? The course itself I mean, it is HTML based. It can play when whatever window we we started in. So it's still basically utilize the same concepts as the two zero one. Like, we get the source files like, the compile bundles, and then we just launch them inside of the frame. Right. So there are no difference between the the storyline and the rise. From that side.

### Sean (2026-03-03T15:50:12.294Z)

David Mead is he able to like, you're able to export CMI five and with the x API similar to what we did for the campus courses. Right?

### Guest (2026-03-03T15:50:21.914Z)

Yeah. Yeah. It it uses the same output format. So in this case, it's basically there will be no need in terms of adjusting how the player will look like because we can use the same one that we already have. The only thing is which we already discussed a little since it will be a sponsored courses, we might wanna style their the homepage of the course a bit differently. Just because it's a sponsored courses. But that's a different thing. Since it will be a regular course, no problems on showing that course on the dashboard. You know, at the top of the page, for example, in our special section for the sponsored courses, asking the user kinda, you know, try it out or something like that. So what happens in your ideal state what happens when you get taken from that call? You log in. You have a profile, etcetera, etcetera, and you're boom, you're in campus. You're ready to take the sponsored course. What do you see on your screen? Do you see this? Is it just like a a full screen and then you have a top bar menu and that's and that's it? Or, like, No. So firstly, you will see the dashboards. With the course. With the with all available courses, you can purchase, or you can access for free we're talking about the sponsored courses. If you will click, like, the access or start or something, it will take you to the course page like it's doing right now, we might probably want to add an entrance test for this course, or we may skip it so you can just start learning through the course. On a course page. And once you will click start, it will launch the subject At the top of the page, you will see the nav panel you know, like the my compass, sign out, under it, you will see a different navigation bar. And then there will be a big iframe which will contain the course materials. Like the navigation through the course, between the elements the contents, the materials, everything. The same way how we're doing it right now with the two zero one. The only difference is if it will be just one subject, okay, we just need to plan Will there be a quiz after this subject because it will be a short course comparing to the two zero one. How we wanna style the course page Will there be an entrance test? If there will be no entrance test, then we need to adjust the logic on the front end and and the back end as well to support it. Because in many places, we rely that the the tests is in place. And in order to start learning the course, you need to complete the test. So I'm not concerned in terms of I I already got what I needed to to get from the content wise perspective. How it will be launched, I only care about how to launch the content. Only thing the and the other important thing is we need to decide how it will look like the course page there will will there be an entrances or there will be no entrances. How exactly we wanna show them up on the dashboard page, and those other things. I would say. But correct me if I'm wrong. I worry if I'm missing something here.

### Sean (2026-03-03T15:54:37.934Z)

So, yeah, there there's not gonna be an entrance test or anything like that. The whole idea is to have the user click on it through dot co and then within dot co, you're going to have the, the opportunity to sign in through x and, like, get authenticated through that. And that's what we were discussing earlier, like, with the with Mike through the, like, the API and authentication and everything like that. So is gonna be handling that, and then from dot co, it's gonna go straight into the My Campus Hub, which is right here. And then the whole the whole idea is that it's going to essentially make an account for you through your Twitter account And then eventually, as time goes on, like, an actual, like, regular account with dot co and campus, And then you're gonna have the my courses hub, and then you're going to be able to select the, for example, polymarket course. And then you're just gonna go right into the RISE course itself. Which, David, it's only gonna be, like, what, five questions? David? Did is that

### Guest (2026-03-03T15:55:47.164Z)

Yes. Five Well, you said five questions, five five lessons. Oh,

### Sean (2026-03-03T15:55:58.164Z)

Yeah. The yeah. What what what did we with, the research team that they narrowed it down to?

### Guest (2026-03-03T15:56:02.374Z)

yes.

### Sean (2026-03-03T15:56:03.784Z)

Okay.

### Guest (2026-03-03T15:56:04.304Z)

Yes. Yes. Yes. Yes. Five topics.

### Sean (2026-03-03T15:56:09.164Z)

So, yeah, that's it's really not as it's it's not as detailed as the campus one. The whole idea is just to have users like, log in through Twitter, and then so Polymarket is able to access They they have access to those the user's Twitter accounts.

### Guest (2026-03-03T15:56:27.754Z)

Okay. And just to confirm, so there will be one course, for example, which will consist from one subject and this subject will have five lessons. Yes. Yeah. Okay. And then we will need to and this understand, will there be any post subject quiz or something. Okay. I can check I I can check with the research team what the, like, I highly doubt there would be any like, prerequisites or any test prior afterwards maybe if they wanna, like, give out some sort of rewards because they they were talking about the fact of, like, giving, like, a bonus. Because we were speaking about the certificates, So Mhmm. We somehow I mean, like, it's not a required one. But we'll in that case, we will need to adjust the logic. A little because the certs are being built on the test submissions for the entry entrance test or a a different attempts. So how we will qualify them, we will like, should they get the certificate, or shouldn't they you know, Yeah. A little bit smarter on that side. Right. David, you can't skip. Right? You have to, like, watch or, like, read everything. Right? You can't just, like, click through the whole thing. Like, it it had you have to basically, like, Yeah. It depends on the setting, but yeah, normally, we set it to that you need to go lesson by lesson. Right. You sort of likely are locked into it. Sort of, like, kinda like how a lot of those, harassment trainings are and stuff like that, like, all those training that you're you're forced to watch a the video and, like, forced to consume the content. So my my my like, guess is if we could grant a certificate for a user if we have confirmation that they have finished all the course, like, they finished the whole lesson. All the lessons and the whole course. Yes. Yes. We can we can base it on that. I think the research team is preparing a couple of quiz so we can tie it to that. I think that's Alright. Least test on the on the knowledge. And that I mean, that's that's even easier, I think, than for the champions team as well. Yeah. Yeah. But there is a difference between the regular test and the quizzes. The quizzes are not using any anti cheat measures. The quizzes are dumb. Basically, it's just 10 questions. You have as many repeats, retries for each questions as you want. Yeah. Just until you will answer correctly. So we need to understand that there is a difference. Yeah. Definitely. There is a difference, and I think there's an inherent difference between the, like, nature of the scores compared to the two one zero one and two zero one. Like, this is supposedly, like, more informational and, like, promotional rather than like, texting your knowledge. Do you know, like, certifying and then showing it off to other people? It's it's I don't think we need test measures here, and people can take the scores or take the tests. As many times as they want. Well, I'm upset myself. Not as many times as they want. It's just, like, if you fail the if you fail the quiz first time, you can, like, retake it for example. And just to make sure you get the bonus or, like, the promotional sponsored prize or whatever it is. So you are right that giving a quiz giving the certification based on the quiz and not on the full, you know, guarded test is different, and I think that's that plays into our content that we're trying to showcase here anyway. Okay. I mean, again, we we we can adapt the search generation based on the course completion instead of just based on the test submissions. I don't think it will be a big problem. As long as we can track based on the events we're receiving, that the course is completed, we're totally fine. Okay. Cool. Sean, let's let's double check all those details. Like, with research and somebody who's sort of leading this know, this whole integration with Polymarket. That that's the expectation. You know? Like, what is what is gonna be the price? Do we actually I'm gonna have quiz questions. And just get get all those details straightened out. Claudia, my question to you would be, that does that make sense to you? Like, if because that was probably one, like, a design state of what it all looks like. Once you're on campus taking a sponsored course. Does that do you have an idea like, was this is it clear enough? To mark something up? So basically, we don't need a dedicated for the course. Once I click on start start the course, on the let's say on the the marketing landing page, Let me check my designs because I'm really conscious. So once I'm on the the dashboard, I'm looking at the dashboard. I can start to sponsored course. I click on the CTA to start the sponsored course, I will directly go to the course to the storyline flow. I won't have a dedicated page for that course like we have for for the digital assets. It would be ideal if we could pull that off. But we're within campus. Right now, you're showing that code, but we'll we'll be within campus. So, like, you you go through the through the login flow and then you show up I think the multicourse dashboard page is the best thing in the file to showcase that.

### Sean (2026-03-03T16:03:00.364Z)

The multi

### Guest (2026-03-03T16:03:00.764Z)

So if you go if you go yeah. I don't know which one it is. It's the third one. The course catalog. Yeah. Yeah. So if you zoom in here, like, we have the list of all the courses that we support. I think there should be a us list for electives or whatever. Zero one. I used to be you zoom in Maybe not anymore. I it was from one of our former One down. Yeah. Yeah. Maybe it's on a different page. Do go to screens before. Yeah. The screens before September 25. Yeah. There is something out of scope v one So we had something a charge for the private course. And a card for the sponsored course. Yeah. This that's what the individual thing looks like. Can you show us the whole dashboard? As required, it's continue. Like, a lot of that stuff is still sort of, like, too early for us, but, like, it's just basically, then you have all courses, and then everything should be another eyebrow for, like, elective slash sponsored courses. Yeah. Yeah.

### Sean (2026-03-03T16:04:34.584Z)

What's up, Nikita?

### Guest (2026-03-03T16:04:36.774Z)

I actually finding the idea that there won't be any dedicated page for the course is a good idea because I even didn't think about that because we can navigate straight from the dashboard to the place where the person will be going through the course. Mhmm. So there will be a page where you will see your results because there won't be any results because there are no entrance Right? Because there will be just one subject we don't even need to show that page to the user. So the dashboard straight to the course back, and there were there will be no intermediate state. Mhmm. That would be the ideal scenario. But it is that is that possible? I mean, yeah. It it it's even less work for us, I suppose. Mhmm. Still some work, but anyway, no no problem. Like, no pain in the ass on terms of designing the specific page for a specific sponsored course. Except for the marketing parts. Yeah. On the public pages. But it's inevitable at this moment. Yeah. In terms of the custom categories, there were no problems. On we already added the possibility to add different type of pills to any course you want. You can style them, like, pick the color, everything from the admin panel side. Already. And we can add the custom category like the sponsored course. It maybe won't be visible to the user or there will be some magic in the admin panel, but we can sort them and pick the sponsored courses to a separate box. Like, the old courses box, and maybe at the top of all courses, you will see, like, the sponsored courses instead of for the required courses. As we have. Yeah. Yeah. Own designs. Yeah. I think I I will update my design because, yeah, it's from a long time ago now. So I will make a new a new version of this page.

### Sean (2026-03-03T16:07:02.704Z)

Perfect.

### Guest (2026-03-03T16:07:02.784Z)

Yeah. If you could if you could slide it, then to the sponsored course, Sigma, that would be great. And then we can sort of go from there, and those would have a then we can meet again maybe in the finance just to make sure that it's all tracking and we have all the bases covered.

### Sean (2026-03-03T16:07:20.344Z)

Yeah. Claudine, you want me to write down any of the details and a ticket for you? Yeah.

### Guest (2026-03-03T16:07:25.064Z)

Yeah. Please. Yes? I I have a a a another question regarding the yeah, regarding the completion state so at the end of the course, I finished the course. I I would like to a CTA to to get my my certificate and maybe another CTA to to add my certificate on LinkedIn or something like that. Maybe and maybe another city to share my my my certificate or share some some designs on on my Twitter account. Saying that I finished the course. So I'm just wondering, if this completion state or completion page will be under under story lane. Will it be under outside of the story lane flow? So maybe I need that case, I need to to make some designs regarding that. I think it will be outside of the storyline flow because they need to take the take the final test first. Okay. Yep. The same thing. Okay. Yeah. And, Sean, let's confirm what, like, what is the user journey afterwards because

### Sean (2026-03-03T16:08:51.324Z)

Yeah.

### Guest (2026-03-03T16:08:54.944Z)

Polymarket is giving a bonus or not. You know, like, $50 free per making predictions. So we probably want a CTA to, like, you know, directing people to the Polymarket. So go ahead. Now you know anything about Polymarket. Now go ahead

### Sean (2026-03-03T16:09:08.764Z)

Go ahead.

### Guest (2026-03-03T16:09:10.804Z)

start play placing predictions.

### Sean (2026-03-03T16:09:11.164Z)

Yeah.

### Guest (2026-03-03T16:09:12.534Z)

Just getting that whole thing, you know, from product perspective, I mean, that user journey straightened out. We have it in a ticket for quality, and then she get has those checkpoints. But in my view, yeah, you just you finished you finished the whole lesson then you have a prompt to take the final quiz or whatever it is. And then once you pass that quiz, whatever the threshold is, it'll decide on. You get these, like, you know, congratulations. There's a for certifications. Added to LinkedIn. Go to Polymarket. Sort of something like that. Okay.

### Sean (2026-03-03T16:09:52.684Z)

Nikita, did you have another question?

### Guest (2026-03-03T16:09:55.844Z)

Kinda. It it's more like an idea. What if the poll market will just share the list of the kind of the promo codes? Which we will give to the user once the test is completed and then they will be able to use the this specific promo to create a profile on a pull and market or something. I believe the pull market already have some kind of the promo code already handled somewhere. So it's just a pregenerated list for example, and we'll just pick one assigned to the user once the quiz is completed. The user may revisit it later and still see that this code. So it won't be showed just only once. You know, like, at the first that will be even easier for us because if we will just say, okay. Good. Good guy. Just go to the pool market. And grab what? Like, how exactly they will get their wellness or whatever. Right? Yeah. That that's that's exactly what I mean for and, of course, to straighten out that post post course flow. What it means to complete it and what it means to get the reward for doing so. Or we will generate our own codes and we will get we will give them to the poll market I mean, like, it doesn't matter. Honestly. We it's just an idea. Right now.

### Sean (2026-03-03T16:11:40.634Z)

No.

### Guest (2026-03-03T16:11:41.824Z)

Well, definitely keep it in mind then. List it in the requirements.

### Sean (2026-03-03T16:11:49.524Z)

Yeah. I I like that idea. And we'll definitely because when we first originally started talking about this, it kinda just, like, stopped at the user just taking the course. But now that we're actually working with Polymarket, we can get a little bit further. And figure out exactly how it is we give them the credits and how we them over to Polymarket. So that's exactly also why we wanted to have this meeting just so that we're all up to date and up to speed on this process. Does any oh, David, I wanted to ask. Where have you gotten with research? Have they reached out to you about anything? Since last Monday?

### Guest (2026-03-03T16:12:29.944Z)

Yes. Yes. They actually they handed over a slide deck

### Sean (2026-03-03T16:12:33.274Z)

Cool.

### Guest (2026-03-03T16:12:34.414Z)

and and the script. I checked in with Matt, and he said that we can have fully market sign off on it. But let's let's wait until the end of this week because there are some other unclear details that there is discussion about.

### Sean (2026-03-03T16:12:51.554Z)

Okay.

### Guest (2026-03-03T16:12:52.824Z)

That's how much I know.

### Sean (2026-03-03T16:12:57.164Z)

Awesome. Alright. So before we head out, does anybody else have anything they wanna talk about? While we got this whole crew together?

### Guest (2026-03-03T16:13:03.834Z)

Yeah. Little thing.

### Sean (2026-03-03T16:13:05.374Z)

What's up?

### Guest (2026-03-03T16:13:08.684Z)

I mean, like, this success state after you will finish the course, we I think we should also care not only about moving the user back to the Palo market, but also we can include the upsell part of our own call. Courses. Mhmm. I mean, like, it's it was the main idea, the at the end of the day. To get them from the block call to the Canvas. Take the pre course, and probably purchase our own one.

### Sean (2026-03-03T16:13:31.624Z)

Mhmm.

### Guest (2026-03-03T16:13:40.964Z)

So we can promote the upsell there as well. Maybe with the discounts,

### Sean (2026-03-03T16:13:47.214Z)

Yep.

### Guest (2026-03-03T16:13:50.354Z)

like that, or something because we already talked about that because in some cases, the upsells may be a little discounted, and we can just generate the promo on the fly then basically create the session with the already applied promo for example. If we need to. So

### Sean (2026-03-03T16:14:12.534Z)

Okay. Cool. Yeah. I mean, I do that is that was a part of the original plan. We were kinda looking at this hub to see exactly what it would look like and where the one on one and two zero one would appear their actual hub. So and the promo code, that's that's also a good point. And and would be a nice way to draw them in. So, yeah, we'll discuss and try to figure that out and write all the requirements up as well. So Claudine, any more questions?

### Guest (2026-03-03T16:14:44.264Z)

No. I think it's all good on my side for now.

### Sean (2026-03-03T16:14:48.844Z)

Cool.

### Guest (2026-03-03T16:14:49.304Z)

Awesome.

### Sean (2026-03-03T16:14:50.644Z)

Alright. Thank you, guys. Yeah. Enjoy the rest of your evenings, your nights, I'll see you guys later.

### Guest (2026-03-03T16:14:59.694Z)

You. Good, everyone. Thanks, everyone. Bye bye.

### Sean (2026-03-03T16:15:00.044Z)

Okay.

### Guest (2026-03-03T16:15:03.054Z)

Bye.

