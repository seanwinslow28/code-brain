---
type: meeting
domain:
  - product-management
status: active
ai-context: Campus team sync on sponsored courses - api twitter auth meeting.
context: the-block
created: 2026-03-02
source: granola-manual
---

# **SUMMARY NOTES**

# **.Co \> Campus Auth**

Mon, 02 Mar 26 · mvitebsky@theblock.co, bmendoza@theblock.co, erupkus@theblock.co, mprice@theblock.co

### **Authentication System Unification**

* Backend infrastructure ready for .co and campus login integration  
  * CryptoIQ authentication already implemented  
  * iOS app authentication tie-in deploying soon  
  * User state reflection between platforms established  
* Shared component approach for profile creation  
  * Same codebase supports both .co and campus  
  * Component reusability for future .co authentication rollout

### **Sponsored Courses Implementation**

* Authentication flow through campus after .co CTA  
  * Users don’t return to .co once they hit sponsored course CTA  
  * No .co login button in navigation yet \- only in sponsored courses flow  
* Polymarket prize validation requirements  
  * Need X account verification to prevent multi-account abuse  
  * Same validation logic as CryptoIQ implementation  
  * Email and wallet support planned for future

### **Design Strategy Decisions**

* Limited .co authentication exposure initially  
  * Only sponsored courses flow gets authentication  
  * No general .co profiles or login value proposition ready  
  * Substantial design effort required for broader .co authentication  
* Backend prepared for future .co authentication expansion  
  * One opportunity to get users to authenticate on .co generally  
  * Current sponsored courses insufficient as sole authentication driver

### **Next Steps**

* Design discussion with campus dev team and David tomorrow  
  * Upsell opportunities for sponsored course completers  
  * Path from sponsored courses to 101, 201, certification programs

---

Chat with meeting transcript: [https://notes.granola.ai/t/4187266a-fc3a-46f3-8265-894e663d00b3-00best9l](https://notes.granola.ai/t/4187266a-fc3a-46f3-8265-894e663d00b3-00best9l)

---

**FULL TRANSCRIPT**

I think, well, What's up? Let's see if Mike joins.  
We're able to do any of the work for the headshot update, Brian? I have it in the PR for the analytics branch. So they'll probably all go out together. Excellent. Cool that we have everybody. What's up, Mike? What's up? So I put this call our schedules to just continue that convo from the, refinement call that we were talking about, the authorization on that co and campus.  
We just wanted us to have a little space and time to to, like, clearly discuss time maybe talk about requirements and, like, you know, what we need to have on that go and what does it actually look like.  
Because it seems like, Mike, you're of the opinion that is a great opportunity for us to actually take some strides in getting that started.  
Yeah.  
Yeah. I've already started some of the legwork for getting, second party authentication in place, and we've already done things with CryptoIQ, which kinda gives us the, you know, kind of the runway to make that happen, between the two.  
So we can easily reflect the user state on dot co now that we have that, and we're we're gonna have this other authentication tie in with the iOS app.  
So and I actually do we actually will deploy that soon. So yeah, just wanted to put it out there that, you know, we can start making some of those. It makes sense. Like, if it makes sense now, to do some of that, it wouldn't be, like, a huge lift to get that in place and don't actually have to, like, patch things together and send them to a different site for different things.  
It whatever it takes to make it feel more unified, from from the user side.  
We can take those steps. It's not it's not a big it doesn't seem like a tall ask, and we're right at the the line where we can really do that.  
So it doesn't make sense then to like, let's say, from the sponsored courses perspective, to redirect people to, like, sign in to their free profile profile with, like, Twitter or whatever.  
If it probably would make sense to just have them log in on that code then, you if we don't have that state where we can support logins. Right? Matt, what are what are your thoughts on that? They do that. We'll take design work. But yeah. Yeah. My thoughts are, like, from a back end perspective, let's go towards, like, the unification path where we do have co logins that are you know, talk to campus logins, talk to Block logins. I think, exposing more than just the sponsored course login on co will require some substantial design efforts.  
I don't think we're set up to have, like, profiles or explain the value of any kind of authentication on co outs of just sponsored courses. Like, I wouldn't want to actually ex this on, like, dot co itself other than in the sponsored courses flow.  
For now.  
Got it. So no, like, login button in the nav or anything yet? Just kinda allow them to go through the off on sponsored courses.  
Yeah. Because, like, what what is a lot like, I feel like we're gonna have, like, one shot to, like, actually get people to authenticate on code generally, not for this particular project.  
Like, if we just have this as the only incentive like, driver for people to authenticate, don't think we're gonna actually succeed in that merit.  
But in terms of, like, how you set up the system, like, if this could be a way where if we wanted to spend design and resources on building out authentication on co, we already have, like, the back end that's supports it. Like, that would be huge.  
Yeah.  
I think that's, like, the main thing. Brian, you were gonna say something? No.  
Sorry.  
Oh, okay.  
Yeah. So, yeah, it does we are at the point where, really, we just need to design for it.  
We can the all the back end things are pretty much there. So whenever we wanna take that step, we can. But I just noticed that, like, we were doing a profile on campus, I was like, but they're coming from Co. I didn't know if it made more sense to put the profile on Co since their their main flow was from from Co.  
I don't know.  
Either either or kind of if we have to do that work anyway, And if we're gonna do that work, we want to make you know, and it felt more unified to do it on code, we could.  
I mean, it's all in Mean, it's all in the same code base and everything. So I think any if anything, we could just make it so that that component is shared if we wanted to show them either co or campus.  
It'll be as simple as using the component and making it look like it needs to own whatever whichever side it is.  
Yeah. I think I I like that path, Mike.  
Share components, then we could utilize it later on on co.  
K.  
Cool.  
So from the flow go ahead.  
No. I was just gonna I was just gonna, like, circle back to, like, the sponsored course flow and what means for, like, the interim.  
Is that like, does it make sense to have Twitter as I I know that we have that as an option.  
Yeah. From the IQ.  
And it's like convenient.  
But if we're gonna have this sort of forward looking take on this, would it make sense to just, like, basically introduce free profile creation for campus and sponsored course access is, like, that's how you get access is you create a free profile and then maybe maybe I misunderstood. Maybe that's what you exactly mean is that that that exact flow will be replicated on that goal as well.

So, like got me. Should we support emails and maybe wallets in the future? For sponsored courses? Yes. For this particular use case, they wanna make sure that you know, me, Matt, I'm not creating 10 emails and then getting a 100 free credits on Polymarket.  
Yeah.  
So we want that same validation that we had with CryptoIQ. Exactly. Yeah.  
Okay.  
Makes sense.  
That flow for for sponsored courses, once they, like, hit the CTA, or whatever from code, they're gonna just be on campus for the rest of the time.  
Is that the they're not going back and forth. They don't have a reason to go back to Coe once they hit the CTA from Coe.  
Data.  
08:03  
Yeah. I think so. I think it's just a formal yeah.  
To to Canvas.  
Okay. Matt, Matt, do we wanna this is probably gonna be another conversation, like, tomorrow that we're have with campus dev and maybe David.  
Of, like, do we wanna have like, design in a way where we have upsell opportunities for those people, like, to for them to finish the sponsored course and then, like, see, okay. There's one zero one. There's still one. There's all these other elected Yeah. I think that'll be great for sure.  
Get certified.  
Yeah. Oh, discuss that. K.  
Okay.  
Cool. That's definitely more clear in my head.  
Thanks, team.  
Yeah. Absolutely. Ten minutes.  
Very good.  
Love it.  
Bye.  
Thanks, guys. See you.  
Thanks.  
Resume  
English

   
