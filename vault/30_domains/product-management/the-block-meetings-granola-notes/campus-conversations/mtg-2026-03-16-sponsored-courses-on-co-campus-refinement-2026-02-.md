---
type: meeting
domain:
  - product-management
status: active
ai-context: Campus team sync on sponsored courses on .co_campus refinement - 2026_02_26 06_13 pst - notes by gemini.
context: the-block
created: 2026-03-16
source: granola-manual
---

# 📝 Notes

Feb 26, 2026

## Sponsored Courses on .Co/Campus Refinement

Invited [Matt Vitebsky](mailto:mvitebsky@theblock.co) [Brian Mendoza](mailto:bmendoza@theblock.co) [Edvinas Rupkus](mailto:erupkus@theblock.co) [Mikita Hulis](mailto:mhulis@theblock.co) [Mike Price](mailto:mprice@theblock.co) [Nikita Orobenko](mailto:norobenko@theblock.co) [Sean Winslow](mailto:swinslow@theblock.co) [Claudine Daumur](mailto:cdaumur@theblock.co) [Ramuald Vishneuski](mailto:rvishneuski@theblock.co)

Attachments [Sponsored Courses on .Co/Campus Refinement](https://www.google.com/calendar/event?eid=MGxtNnUxczdkbmZyYWVjNmozcGtyYTdicW8gZXJ1cGt1c0B0aGVibG9jay5jbw) 

Meeting records [Transcript](?tab=t.ewshxhe1e2ne) 

### Summary

**Sponsored Course Design Details**  
The team reviewed the design mockups for the sponsored course user flow, including new blog.co touchpoints and a dedicated course preview landing page, confirming the navigation flow within the existing platform structure.

**Authentication and Wallet Connection Flow**  
The logging process will use an overlay on blog.co with X authentication and an optional step for providing a wallet address to receive rewards, though authentication bridging between blog.co and campus requires further discussion.

**Campus Integration and Course Format**  
It was decided that authenticated users should land on the Campus dashboard to access sponsored courses, which will utilize a standardized, short course format, potentially switching to the Rise 360 structure

### Details

**Decisions**

*Rate these decisions:* [Helpful](https://bit.ly/4j0NRI9) or [Not Helpful](https://bit.ly/4p4GaCr)

## NEEDS FURTHER DISCUSSION

* **Unified authentication implementation timeline** Implementing a unified authentication experience that bridges the user state and profile creation between the block.co domain and Campus needs further discussion between Product and Engineering.

* **Sponsored course layout standardization** The layout and template design for individual sponsored courses must be standardized and short, potentially utilizing the Rise 360 format, pending technical assessment of the implementation differences.

## ALIGNED

* **Course access pill label** The course access pill text label should be changed from “sponsored” to “unlock” in the designs.

* **Course preview page navigation** The course preview page will not include a back button, maintaining consistency with existing learn article pages.

* **Profile creation vs. wallet priority** Profile creation should be prioritized for the MVP, and the optional wallet address collection and certificate functionality should be de-emphasized or deprioritized.

* **Logged-in sponsored course destination** Logged-in users who access sponsored courses must land on the Campus dashboard/hub, which requires a new design state to prominently display sponsored courses, electives, and learning paths.

* **Free sign-up option implementation** A “Skip for now” CTA must be added to the subscription selection page to enable users to complete a free sign-up flow and access the Campus dashboard without purchasing a paid subscription.

* **Full sponsored course collection access** Users who sign up for sponsored courses must be granted access to the entire collection of available sponsored courses, regardless of which individual course they started the flow with.

* **Login flow UI design standard** The profile creation and full login process UI must be designed to align with the Campus product UI, as the process will be hosted on the Campus side.

*More details:*

* **Sponsored Courses Initiative Overview**: The initiative focuses on advertising and hosting free sponsored courses on campus, with the goal of funneling people into the campus ecosystem through advertising on .go. This strategy serves as a two-way asset, functioning as a revenue generator displayed on .go while also organically pushing users toward campus and providing opportunities to upsell larger courses ([00:00:00](#00:00:00)). The project requires collaboration between code devs and campus devs ([00:02:27](#00:02:27)).

* **Design for Sponsored Course Touchpoints**: Claudine Daumur presented new touchpoints for accessing sponsored courses via blog.co, including a simple card on the homepage and a similar module within article pages. It was noted that the label "sponsored" might be changed to "unlock" on the card ([00:02:27](#00:02:27)) ([00:05:18](#00:05:18)). New elements on the learn page include a large hero card to highlight important campus courses and new pills on cards, such as a "campus" pill to distinguish courses and a "sponsored" pill (potentially "unlock") ([00:03:48](#00:03:48)).

* **Course Preview Page and User Flow**: A new, separate course preview landing page was designed with light and dark modes, featuring a video, cards, and various Calls to Action (CTAs) ([00:05:18](#00:05:18)). Claudine Daumur showcased an interactive prototype with simple hover states and video animation upon scrolling. A recirculation module at the end of the page might not be necessary for the Minimum Viable Product (MVP) if there is only one sponsored course initially ([00:06:48](#00:06:48)).

* **Discussion on Navigation and Back Button**: Ramuald Vishneuski inquired about the back button functionality on the new course preview page, noting that on article pages there are options to choose other articles ([00:08:05](#00:08:05)). Claudine Daumur and Sean Winslow clarified that a back button is not needed because users remain within the blog and still have the navigation bar ([00:09:26](#00:09:26)).

* **Logging Flow and Profile Creation**: Claudine Daumur presented the logging flow, which starts on the course preview page and uses an overlay, meaning the user stays within blog.co. The flow involves signing in with X (Twitter) for authentication, accepting shared information, and an optional step to add a wallet address ([00:10:26](#00:10:26)). There was a discussion about adding extra steps to edit profile information gathered from the Twitter account ([00:12:15](#00:12:15)).

* **Wallet Connection and Certificates on-Chain**: Mike Price questioned whether connecting a wallet would be more optimal than pasting an address and if the reason for providing the wallet address was clear (to receive sponsored rewards) ([00:12:15](#00:12:15)). Matt Vitebsky suggested that the current design, which makes the wallet address optional and requires pasting the address, is low-risk for users and likely less work for the team. Edvinas Rupkus emphasized that the main goal is free profile creation and not getting "hung up" on the specific details of adding a wallet, certificates, and the associated scope increase ([00:13:35](#00:13:35)).

* **Clarification on Certificates and Rewards**: Nikita Orobenko questioned the specifics of issuing certificates "on chain". Matt Vitebsky clarified that this is "copy language" and the main objective is collecting wallet addresses from users who complete the course to send to the Product Manager (PM) for reward distribution. Nikita Orobenko confirmed that collecting and storing wallet addresses in the database is acceptable for distributing rewards ([00:13:35](#00:13:35)) ([00:16:07](#00:16:07)).

* **Discussion on Unified User Authentication and Profile**: Mike Price raised the point that the current implementation begins to feel like a turning point where user state should be linked to blog.co, suggesting a unified experience ([00:17:04](#00:17:04)). Mike Price and Brian Mendoza argued that since the authorization cookie is on the same domain, they could start unifying the experience by running profiles on blog.co instead of campus ([00:18:14](#00:18:14)). Matt Vitebsky requested that Mike Price and Edvinas Rupkus take this conversation offline to sync up on the authorization bridging ([00:19:15](#00:19:15)).

* **Campus Integration and Post-Authentication Landing Page**: Following successful authentication, the user is granted access to the free version of the multicourse page on campus and will arrive at the sponsored course landing page housed within campus ([00:20:16](#00:20:16)). Nikita Orobenko and Mikita Hulis pointed out that, currently, logged-in users are locked out of non-authorized UI, and it would be tricky to reimplement public pages for them. They suggested that instead of navigating directly into the course, the user should be directed to the dashboard, which is the main hub for purchased courses and previews ([00:21:41](#00:21:41)).

* **Dashboard Design for Sponsored Courses**: Mikita Hulis and Nikita Orobenko agreed that sponsored courses should be available on the campus dashboard, potentially in a new section or mixed with other courses, to maximize visibility ([00:22:56](#00:22:56)). The need for a dedicated design state for the dashboard, including electives, learning paths, and sponsored courses, was identified ([00:24:39](#00:24:39)). Sean Winslow mentioned that this concept was addressed in original tickets and a prototype would be shared with the team ([00:27:48](#00:27:48)).

* **Campus Sign-up Flow and "Skip for Now" Option**: Edvinas Rupkus discussed the marketing page flow, which presents users with three access cards, and the need for a "Skip for now" Call to Action (CTA). This CTA would allow users to complete the free login experience, land on the dashboard, and organically discover the sponsored courses within campus ([00:28:47](#00:28:47)). Nikita Orobenko confirmed the technical feasibility, provided the design perspective for the new sign-up functionality on campus is established, which should create an account and grant access to the whole collection of sponsored courses ([00:30:08](#00:30:08)).

* **Sponsored Course Layout and Format**: Edvinas Rupkus confirmed that a specific, standardized template would be used for sponsored courses, as they are intended to be short (consumable within 10 minutes) unlike the longer 101 or 201 courses ([00:32:38](#00:32:38)). Sean Winslow noted that David suggested pivoting to the Rise 360 format, which is a lighter format involving a simple quiz. Nikita Orobenko expressed interest in understanding the difference between Rise 360 and the existing 101/201 implementations to assess the necessary adjustment time ([00:33:54](#00:33:54)).

* **Summary of Next Steps**: Edvinas Rupkus summarized that Product and Engineering need to look into and discuss the authentication bridging decisions between .go and campus. The team owes designs for the dashboard and individual sponsored courses. Claudine Daumur requested a ticket for the sponsored courses within the campus product, and stated they would adjust the login process designs to look more like the campus product UI since it will live on campus ([00:35:15](#00:35:15)). Sean Winslow committed to discussing Rise 360 with David to clarify the differences ([00:36:33](#00:36:33)).

### Suggested next steps

- [ ] Claudine Daumur will change the design from 'sponsored' to 'unlock' in the designs.

- [ ] Claudine Daumur will change the design of the login process to look like the campus product UI instead of blog.co UI.

- [ ] Sean Winslow will send the prototype he made for the sponsored courses on campus to Mikita Hulis and Nikita Orobenko.

- [ ] Sean Winslow will talk to David about the Rise 360 format, understand the differences, and see if further discussion is needed.

- [ ] Edvinas Rupkus will set up time for himself and Mike Price to discuss problems and topics related to the go off.

*You should review Gemini's notes to make sure they're accurate. [Get tips and learn how Gemini takes notes](https://support.google.com/meet/answer/14754931)*

*Please provide feedback about using Gemini to take notes in a [short survey.](https://google.qualtrics.com/jfe/form/SV_9vK3UZEaIQKKE7A?confid=nlP4Q4DZSWcbmCxZeTNaDxIPOAIIigIgABgBCA&detailid=standard)*

# 📖 Transcript

Feb 26, 2026

## Sponsored Courses on .Co/Campus Refinement \- Transcript

### 00:00:00 {#00:00:00}

   
**Sean Winslow:** What's up,  
**Edvinas Rupkus:** Hey,  
**Sean Winslow:** bro?  
**Edvinas Rupkus:** hey, Nikita. Do you know if the other Nikita is going to join?  
**Nikita Orobenko:** I suppose so. Well, let me just in  
**Edvinas Rupkus:** Okay. Okay. Let's give it another few sec. Also invited Brian and Mike. Brian said he would show up.  
**Sean Winslow:** Brian's  
**Edvinas Rupkus:** Oh, Brian's here. Hello sir.  
**Sean Winslow:** here.  
**Brian Mendoza:** What's  
**Edvinas Rupkus:** Sorry. Okay. I think I don't know if Mike's going to show up, but I think we have everybody in. So, we can get started and start talking about sponsored courses on.go/campus. So, this initiative is basically twofold. um we'll start basically advertising and hosting free courses on campus uh and they will live in the campus ecosystem. However, we'll want to try and funnel people into campus and sort of like advertise them on that. Go. So, it will work two way as a revenue generating asset uh that's displayed on that. But also at the same time it should indirectly uh push people towards campus and explore it even more organically with opportunities to upsell for for bigger courses as well.  
   
 

### 00:02:27 {#00:02:27}

   
**Edvinas Rupkus:** So we definitely need that code devs and campus devs collaborating on this one. Uh but Claudine if you don't mind sharing some of your Figma we can take a look at the the sketches that we have so far. We can start at the beginning. Yeah. I don't combo about code.  
**Claudine Daumur:** Um, so yeah, the goal here is to add more uh to add new touch points uh through uh through the blog.co to be able to access uh the the new sponsored courses. So I designed a bunch of new modules. Uh the first one is on the homepage. It's this one. So, it's a simple uh card uh in the in the left trail. Uh here is the the dark um uh mode right here. And I just noticed your comment uh regarding unlock rather that than sponsored. So, I'm totally fine with that. Um, I don't know if it's a recent comment or not, but uh yeah, I can I can change that in my uh in my designs.  
   
 

### 00:03:48 {#00:03:48}

   
**Claudine Daumur:** And then um if we click on this card, we will go then to the course preview page that I'm going to show you um a bit later. First I will show you uh inside the article page we have another model module that is pretty similar to what we have on the homepage. Um same elements uh the layout is the only thing that is changing. So it's within the article and we have the same on dark mode and then we have um a bunch of new things on the learn page. So um it's this version. Uh so first um we have a big hero card to highlight the most um important maybe not the most recent but yeah the most important um um compus courses. Um so at the top of the page we have also a new section um dedicated to Compus to the to the new courses and then we have a bunch of new pills on the card. So we have a compus pier so that way we can highlight what is a course. Um, and if we don't have the compus peel, it will be just like a regular learn article.  
   
 

### 00:05:18 {#00:05:18}

   
**Claudine Daumur:** And then we have another sponsored peel. So maybe it will be unlock instead of sponsored. And uh there is also a tiny change regarding the layout of the the former card that we have here. So currently uh in production it look like that. So we have the beginner peel or uh you know the level peel. So beginner, intermediate or advanced. Um and they are all at the bottom of the cards. So now uh they will be um just under the the sunail. Uh so that way uh all the different pills are at the same uh place uh within the the cards and then we have uh the course preview page. So for that one so it will be like a totally new page. We have dark mode and light mode. And it's a simple landing page uh with a bunch of CTA. We will have um a video right here, some cards, and yeah, that's it. Um so I can show you uh an interactive prototype. I'm I've made a tiny uh animations.  
   
 

### 00:06:48 {#00:06:48}

   
**Claudine Daumur:** So we have one right here. um on the little um little pill right here. Uh we have a simple um over state and then when we start scrolling uh the video will get a little bit bigger. We have also a simple animation right here. Um it's a tiny detail. If we don't have time for that, it's okay. And then we have um a little animation on the on the current and and yeah, that's it. And also this section at the end, I'm not sure we will need that for the MVP because uh it's like a recirculation module. But if we only have one um one sponsored course or one uh comput course at first, uh it doesn't make sense to have this session. Uh but when once we have um multiple courses uh it would be nice to to have this kind of section at the end of the of the landing page. And then uh we have the login flow.  
**Edvinas Rupkus:** So, should we pause? Should we pause now before we get into campus and then just Yeah,  
   
 

### 00:08:05 {#00:08:05}

   
**Claudine Daumur:** Okay.  
**Edvinas Rupkus:** let's let's Are there any questions, concerns with the what you've seen on that  
**Brian Mendoza:** This part looks fine to me. Nothing crazy.  
**Edvinas Rupkus:** go?  
**Nikita Orobenko:** Yeah, the same thing on my end. No problems on a bit more extra API to retrieve the information uh and make it dynamic.  
**Edvinas Rupkus:** Cool. Yeah. So, basically if you want to Oh,  
**Mikita Hulis:** And they'll start I mean,  
**Edvinas Rupkus:** sorry. Go ahead, Nikita.  
**Mikita Hulis:** no, no, no. Everything's fine.  
**Edvinas Rupkus:** Cool. Yeah. So, if you want to take the course and interact with that CTA, we're basically going to go into this flow now. Okay. Hey, Roma. Roma has a question.  
**Ramuald Vishneuski:** Um yeah uh sorry uh where is back button? How to return to learn articles from here?  
**Claudine Daumur:** Sorry, what? Where is the  
**Ramuald Vishneuski:** Uh back button. So we we opening this page from learn uh  
**Claudine Daumur:** Yeah,  
**Ramuald Vishneuski:** your page.  
**Claudine Daumur:** we don't the back button because um you know it's like the it's like when we click on the on the learn um wait when we click on uh the regular learn article page we go to to a to an article page.  
   
 

### 00:09:26 {#00:09:26}

   
**Claudine Daumur:** So I'm not sure currently we have a back button.  
**Sean Winslow:** Yeah, there there are no back buttons.  
**Claudine Daumur:** Uh  
**Ramuald Vishneuski:** Okay.  
**Sean Winslow:** It's it's just you click on a on a new uh like you click on data pages or you click on home or something  
**Ramuald Vishneuski:** Mhm. Oh,  
**Sean Winslow:** like that.  
**Claudine Daumur:** yeah.  
**Ramuald Vishneuski:** okay.  
**Claudine Daumur:** Yeah.  
**Ramuald Vishneuski:** Okay.  
**Claudine Daumur:** Because we are still within the we are still within the block. So we still have the the navbar and everything.  
**Ramuald Vishneuski:** Yeah,  
**Claudine Daumur:** So yeah, for that we don't need a back button.  
**Ramuald Vishneuski:** that's okay. I I just had that concern because on article pages or learn articles, we have other uh articles that you can choose. So So yeah,  
**Claudine Daumur:** Ah yeah next to yeah.  
**Ramuald Vishneuski:** but that's okay. Just little concern.  
**Claudine Daumur:** Okay. Um so maybe I can show you the logging flow. Um we are still uh actually with the logging flow we are still within um the blog.co if I'm not mistaken.  
   
 

### 00:10:26 {#00:10:26}

   
**Claudine Daumur:** uh because we we see the the the course preview page behind uh the overlay. So um this is the first flow uh which is pretty straightforward. Um so we sign with X. So if I click continue with X then I will have you know the the little the the the X window for you know um authentification and then uh I will uh go back to this uh to this uh screen uh to um accept a bunch of different thing that I will be sharing you know with withco If I click on on I accept, I will have optional step which is to basically add my uh my wallet my wallet address. So I can skip it or I can enter an a wallet address and then save my wallet. uh this is an error state and uh this is like a active uh input state and uh once I'm done I will be uh arriving on the actual compus product um and this is the light mode version right here and um a few days ago uh when I when I shared that with um the team Uh we've discussed the possibility maybe to uh edit the information that we get from the Twitter account.  
   
 

### 00:12:15 {#00:12:15}

   
**Claudine Daumur:** So maybe we can have a bunch of extra steps uh within that flow to um edit our profile info. So this is what I've been working on today. Um it's not perfect but uh there are a bunch of thing that not exactly sure that that I wanted to discuss with you. So um I logged in with Yeah. Mike you have a  
**Mike Price:** I had two questions.  
**Claudine Daumur:** question.  
**Mike Price:** Uh, one about the wallet address. Um, is it like um would it be more optimal to actually just use a connection like we did with access where someone could just like if they have a wallet like Phantom or something connected and is it evident to the user why they're giving their wallet address? like why am I giving my wallet address to receive sponsor rewards?  
**Edvinas Rupkus:** Yeah, the second the answer to the second  
**Mike Price:** Okay. Okay. I didn't see that text there. All right. So, the second question is obvious. Um, would it be more optimal to do a connection or is it just better to use the I guess y'all probably thought this out and is better to paste it?  
   
 

### 00:13:35 {#00:13:35}

   
**Matt Vitebsky:** Yeah. Yeah. I think it's like people are pretty weary connecting their wallets. So, this is just like a no risk option for them and it's optional. I think it'll be less work on our end.  
**Mike Price:** Gotcha. Okay. All right. That's  
**Edvinas Rupkus:** Go ahead and make it  
**Claudine Daumur:** Yeah.  
**Edvinas Rupkus:** a  
**Nikita Orobenko:** Uh I'm a bit curious what does it actually means like the certificates onchain.  
**Edvinas Rupkus:** th this this whole adding your wallet thing is sort of like optional like this would  
**Mike Price:** Innocent.  
**Edvinas Rupkus:** increase the scope I feel like quite a bit. Um, maybe it would be a lot easier to return to, you know, editing your wallet information or your profile information in that like user account model that we've been discussing directly on campus as opposed to within the uh profile creation flow. So I would not like get hung up on the on the specific part of like adding your wallet and certificates and etc cuz that that's not like a huge of emphasis for us.  
   
 

### 00:14:43

   
**Edvinas Rupkus:** I think the bigger emphasis for us is the profile creation in a free way. So basically to you know have it a a onetoone uh profile being created when you sign up and buy a course as opposed to when you u discover you know campus organically through learn through that go or through the marketing page and then you can just sign up and create a profile for free with Twitter or or any other fashion.  
**Nikita Orobenko:** Yeah, I mean uh there is a difference if we don't want to do the sign in uh using the preview to connect your wallet and actually create an account. uh as I remember the previous being used for that uh or can be used for that. Uh in that case it means we just store the the wallet address somewhere uh in the database if they will want to add it. So we cannot perform the authorization through the wallet connect mechanism. But uh that's one thing but I'm still curious uh I mean like the sponsor rewards is fine. uh we will collect the wallet addresses and we can redistribute the uh rewards using those wallets address.  
   
 

### 00:16:07 {#00:16:07}

   
**Nikita Orobenko:** But how we actually are planning to issue the certificates on chain that's the most uh  
**Mike Price:** You'd have to an NFT.  
**Nikita Orobenko:** um  
**Mike Price:** You'd have to take the image and then meant to NFT. And then wouldn't they have to accept that as a transaction though? It would you would have to  
**Matt Vitebsky:** Yeah, let's get caught up on this is just like copy language.  
**Mike Price:** Hey.  
**Matt Vitebsky:** I think the the main use case is just giving them the reward from  
**Nikita Orobenko:** Okay. Yeah.  
**Matt Vitebsky:** PM.  
**Nikita Orobenko:** I mean like I'm I'm just a bit curious uh regarding uh the language because the the recent experience is  
**Mike Price:** It's out. It's out of scope.  
**Nikita Orobenko:** telling yeah it's better to clarify it early as much as  
**Edvinas Rupkus:** Yes.  
**Matt Vitebsky:** Yeah,  
**Nikita Orobenko:** possible.  
**Matt Vitebsky:** the really like the thing that I care about is getting the wallet address if they completed the course, being able to send all the wallets that completed the course to PM.  
**Nikita Orobenko:** Okay. I mean like uh I don't see any problem to collect those wallet addresses just and store them somewhere in the database.  
   
 

### 00:17:04 {#00:17:04}

   
**Nikita Orobenko:** Uh they still can be used to distribute the rewards or something. Uh I mean if we don't if we're not planning uh to do the authorization through the wallets using the preview for example. Yeah,  
**Mike Price:** One question I had about the um the off like it seems like we're  
**Nikita Orobenko:** Mike.  
**Mike Price:** extending user authentication and then kind of making the bridge. This really starts to feel like the turning point where we want to link like the actual user state to the block.co. Um I just feel like going back and forth between like at here it looks like we're on the block.co collecting information, but then we went to the profile page and now they're on campus. Is it kind of like the bridge where we want to start actually doing the authorization and keep and making it unifi? Because it's not like it would be harder to do it one way or the other, you know, like if we actually wanted to make this one unified experience on one site, then we could start doing authorization right here on the block code.  
   
 

### 00:18:14 {#00:18:14}

   
**Matt Vitebsky:** If you're saying it's not harder one way or another, then yeah, the answer would be yes.  
**Mike Price:** like the actual cookie is still on the same domain like when they log in. So yeah, no would actually be if we can actually make it more unified and do the profile and everything here guys like what are your what is your opinion? Do should we like start to do this? Cuz like from what I'm seeing, we already have authorization on between campus and this do and this repo. They're both in the same codebase. The cookies on the same domain. We literally could just run profiles and everything and keep them on a unified experience right here on the block code.  
**Brian Mendoza:** Makes sense to me.  
**Mike Price:** Tell me. All right. All right. So I  
**Edvinas Rupkus:** But we wouldn't would we would we show on if you're on that go that you like you're  
**Mike Price:** mean  
**Edvinas Rupkus:** in a logged in state that's not that's not in scope right it's just like in on the back end you'd be sort of  
   
 

### 00:19:15 {#00:19:15}

   
**Mike Price:** no like that's exactly like we're talking about bringing the profile and the logged in state to the block code rather than jumping them between two different sites.  
**Edvinas Rupkus:** I just feel like you would need like your profile screens and all that for that code as  
**Mike Price:** But no, you're building the profile screen on the black co instead of uh  
**Edvinas Rupkus:** well.  
**Mike Price:** campus. We have to build it anyway.  
**Edvinas Rupkus:** Yeah.  
**Matt Vitebsky:** Let's let's take this one offline and keep going. Um Mike, me and Ed can sync on this.  
**Mike Price:** All  
**Edvinas Rupkus:** Yeah. Yeah. That's that we def you're definitely right, Mike.  
**Mike Price:** right.  
**Edvinas Rupkus:** Like we're we are getting closer to that state and the eventual goal is to have these profiles be sort of bridged, you know, so you don't have a million profiles with the block ecosystem.  
**Mike Price:** Well, if we're like saying,  
**Edvinas Rupkus:** Uh but  
**Mike Price:** if we're going to build it, then we can build it. If the eventual idea is to have this linked on the block code, then this seems like the right time because we're doing the bridging  
   
 

### 00:20:16 {#00:20:16}

   
**Edvinas Rupkus:** Okay,  
**Mike Price:** already anyway. And then we could literally just not duplicate work and go straight at it.  
**Edvinas Rupkus:** makes sense. Yeah, we'll uh we'll take a that we can discuss that. But uh assuming you know you go through a successful authentication um essentially this grants you access to the free version of the multicourse page on on campus and and if you had pressed take course initially and then went through the off you'd arrive at the campus housed uh sponsored course landing page where you'll be able to take that course. Do we do you have a screen for that, Claudium?  
**Claudine Daumur:** Um uh actually no no uh no not yet. No no  
**Edvinas Rupkus:** Okay. Yeah.  
**Claudine Daumur:** no.  
**Edvinas Rupkus:** But I mean essentially it looks you know relatively similar to what uh the learn page is just on the campus the main campus front end and you just interact with the course and just you know go through the  
**Claudine Daumur:** There you go.  
**Edvinas Rupkus:** regular um course steps. Go ahead Nikita.  
   
 

### 00:21:41 {#00:21:41}

   
**Nikita Orobenko:** So it means that we're introducing the different layouts for the sponsored courses that should be visible inside of the campus because right now the only layout we have is the standard one. You take the entrance test and you go then through the course. You see the stats, the subjects, all those kind of things. Uh the public pages, they're generally unavailable once you signed in. Is it is it is it do you remember? I may be mistaken there. But uh so if you're signing in then you will be navigated either to the start page of that course or we can navigate you to the dashboard where you will see your sponsored course uh like it's happening right now because the dashboard page is basically like the the current homepage for everybody. Once you will purchase something you are the new page is your uh the dashboard with all the courses uh to which you have the access to or you don't and you can be upselled uh or access them and then you  
**Mikita Hulis:** That's a great point actually.  
   
 

### 00:22:56 {#00:22:56}

   
**Nikita Orobenko:** can  
**Mikita Hulis:** I mean because we are like after the user is logged in and they've purchased something they are as of now locked out out of the non uh nonauthorized uh UI. basically they cannot see uh the main pages but and to reimplement it would be somewhat  
**Sean Winslow:** meaning  
**Mikita Hulis:** tricky uh just because of the amount of existing redirects and their them being intertwined. So since we already have the dashboard as the main hub for uh all of your purchased courses and we have the functionality of previews there as well. Uh wouldn't it make more sense to have the have those courses which we want to promote be available there as well?  
**Sean Winslow:** meaning the sponsored courses at the bottom of the uh campus hub you're talking  
**Mikita Hulis:** Uh well probably not at the bottom because we like if we want to  
**Sean Winslow:** about.  
**Mikita Hulis:** push them then locating them at the bottom of the dashboard would be uh someone getting like getting eyes off of them. But well somewhere on the somewhere on the dashboard uh page as the part of uh maybe uh your purchased courses at the top and right after the uh promotional material those uh like uh paid for courses uh sponsored courses and afterwards like the ones to not start it maybe.  
   
 

### 00:24:39 {#00:24:39}

   
**Sean Winslow:** Mhm.  
**Mikita Hulis:** So maybe um like the ones uh you've already started at the top then promotional ones and then not yet started once because ultimately as a product we've like if a user already has purchased a course then we did our job and the purchase was made like going through it is uh in interest of users themselves.  
**Edvinas Rupkus:** Yeah, I think I kind of I'm kind of following you.  
**Sean Winslow:** Gotcha.  
**Edvinas Rupkus:** What we essentially need a design uh state for the for that dashboard where we have electives or we have the learning paths and sponsor courses as well.  
**Mikita Hulis:** What I'm trying to to say is that once the user has already purchased the course like we do not want to obstruct  
**Edvinas Rupkus:** So,  
**Mikita Hulis:** the user from accessing the course but we also have our own agenda to upsell them and sell them on the more courses specifically especially sponsored ones.  
**Edvinas Rupkus:** Mhm.  
**Mikita Hulis:** So we need to find a proper place for those uh to not be lost uh to the eyes of the client.  
**Edvinas Rupkus:** Yeah. So you're saying instead of like opening it full screen your video like directly into the into the interface for the course you want to just upsell and show like everything that we have all the all the whole dashboard with electives with learning paths with  
   
 

### 00:26:17

   
**Nikita Orobenko:** Yeah, kind of.  
**Edvinas Rupkus:** everything.  
**Nikita Orobenko:** Or we can create the separate section like uh right now we do have like in progress and all courses and we can maybe create like the sponsor courses uh being somewhere on the top for example. um cuz that that part inside of the campus that will be the second  
**Sean Winslow:** Yep.  
**Nikita Orobenko:** uh access point for those uh sponsor courses cuz you I suppose we're planning the regular the other users being having an access and a possibility to access them not only for the people who came in uh from the call side.  
**Mikita Hulis:** Yeah,  
**Nikita Orobenko:** So this  
**Mikita Hulis:** maybe a maybe a separate logged in page when the user can browse through them would be nice.  
**Nikita Orobenko:** use  
**Mikita Hulis:** So the first goal is to uh probably avoid um changing the functionality of uh pages like of the like not logged in pages not being able to be shown to already logged in users. So another way to circumvent it and to not really shove new courses uh in the person's throat would be to have a separate page with a separate navigation uh which would still direct users uh well sort of as a like a shopping page of like by the way here are the cores you can purchase without logging out.  
   
 

### 00:27:48 {#00:27:48}

   
**Sean Winslow:** I I know what you're talking about. Yeah, this was you're getting into more detail, which I appreciate it and it's necessary, but it it was addressed in the uh original tickets and we're like I I made a prototype. I'll send it to you like a while ago when I first started uh building the PRD that you'll see at the bottom that's kind of like it's essentially what you're describing. So, it's just kind of bare bones, but it is like something similar to that. So, I'll send it your way so you can get a take a look. But I'll take uh everything that you're saying right now and I'll get deeper into the actual tickets themselves so we can actually establish this and especially all the backend stuff that you guys are way more familiar with. We'll be able to make those connections a little bit better.  
**Mikita Hulis:** Thank you sir.  
**Edvinas Rupkus:** Another thing that we also have to be aware of is that like the the whole marketing flow uh marketing page flow where you you're pressed to sign up and you're you will be presented.  
   
 

### 00:28:47 {#00:28:47}

   
**Edvinas Rupkus:** We're not there yet, but like it's already designed that we're going to start working on this. But you will be faced with these three cards where whether it's 101, 2011 or or uh all access, we're going to need a CTA for uh like skip for now basically. So if a person just like wants to just go through the login flow uh for them to arrive on that said dashboard and just go through this free basically login experience and and land on on campus so that they can explore and see like just just stumble upon the uh sponsored courses within campus. Yeah, exactly there. I feel like something that's like very not obvious. Uh that's just, you know, skip for now right underneath and you continue signing up for campus. Does that sound logical, doable?  
**Nikita Orobenko:** I mean yeah uh it it all depends on uh how exactly we want to enlarge uh the sign in possibilities on the canvas end. So if it will be the sign in with uh like the same thing uh we're planning to have on the co side no problems there.  
   
 

### 00:30:08 {#00:30:08}

   
**Nikita Orobenko:** We already had it for the crypto key before. Uh the only thing I'm probably just want to see how it should look like uh from the design perspective because right now the only thing you can do on the campus and you can just sign in and there are two things either we will create you an account on the flight if your organization is already on boarded or go away. Uh so in this case uh we might want to handle that option that if you will either try to sign in we still will create UN accounts even if your uh organization are not on boarded or something else. So kind of the sign up functionality basically because the users  
**Edvinas Rupkus:** Yeah, I think that's the right  
**Nikita Orobenko:** may go through that way as well not only through the marketing CDA on the campus marketing  
**Edvinas Rupkus:** approach.  
**Nikita Orobenko:** page but also through the regular sign up and we still need to create an account uh and give the subscription with basically an access to the sponsor courses which are available at the moment.  
   
 

### 00:31:24

   
**Nikita Orobenko:** uh no payment required not attached to this tribe. So we will utilize the local subscriptions functionality we already have and then boom you have the access to those sponsor courses inside of the campus once your sign up will be completed.  
**Edvinas Rupkus:** Okay. Yeah.  
**Nikita Orobenko:** The same thing if you are going through the call. I'm not sure we should give you the access only to the course uh where you started the flow. We might still want to give you the access to the whole collection of the sponsor courses because I believe at some point of a time there might be more than just one sports courses at the moment.  
**Edvinas Rupkus:** Yeah.  
**Sean Winslow:** Yeah, that's the idea.  
**Nikita Orobenko:** Okay, perfect.  
**Edvinas Rupkus:** Okay. So, it seems like Okay,  
**Nikita Orobenko:** And uh and still one little  
**Edvinas Rupkus:** go ahead.  
**Nikita Orobenko:** thing I would planning to have a little different design uh for the sponsor courses uh main page once you will open the course uh you know like take the entrance test see the subject or we're still planning to use the already existing layout.  
   
 

### 00:32:38 {#00:32:38}

   
**Edvinas Rupkus:** No, we're definitely going to have a design for that. I'm pretty sure a little  
**Nikita Orobenko:** Uh we're planning to Yeah. I I mean like will it be just the version two for all sponsor  
**Edvinas Rupkus:** bit  
**Nikita Orobenko:** courses or we are planning to make that layout a bit dynamic uh for each different sponsor courses?  
**Edvinas Rupkus:** I I think it it's basically should be a standardized uh template for short because this is this is not a like a long course just like 2011 or or 101\. It's I think it's like within 10 minutes should be should be consumed within 10 minutes. So all the like sponsored courses I believe electives as well but I could be mistaken uh should follow like a a shorter template that's not like as what's the right word like as broad as and and like all comp all-encompassing basically. It's it's almost like a video or just access to this uh you know articulate interactivity where you just go through the specific things that we have pointed out and and you're done and it's all done. So  
   
 

### 00:33:54 {#00:33:54}

   
**Nikita Orobenko:** Okay,  
**Sean Winslow:** Yeah,  
**Edvinas Rupkus:** yeah.  
**Sean Winslow:** I was gonna say,  
**Nikita Orobenko:** I will I  
**Sean Winslow:** have you spoken to uh David recently,  
**Nikita Orobenko:** will not  
**Sean Winslow:** Nikita? Okay.  
**Nikita Orobenko:** yet.  
**Sean Winslow:** Yeah. Well, so so he suggested that we pivot to uh using the rise format and rise 360\. So I started looking into that. I started adding it to the tickets and it's essentially like you I'll I'll send you the example that he sent me. It it give you just like a like a simple p like similar to what we already have now, but it's just very it's it's lighter. There's not it's not as heavy as going to like the CMI5 and the LMS. It's just like a simple like a few question uh quiz and it looks it looks very similar to what we have  
**Nikita Orobenko:** Um, that's interesting.  
**Sean Winslow:** now.  
**Nikita Orobenko:** Uh we definitely need to talk about it because I'm I'm I'm happy that we're discovering it uh when we do have a time for that. Uh but I'm not even sure what what's the actual difference cuz if it's the same uh kind of implementation as we already have for 2011 I'm totally fine for that.  
   
 

### 00:35:15 {#00:35:15}

   
**Nikita Orobenko:** Uh if it's not it's something completely different from what we had with 101 or 2011 then we will need to schedule up some time to uh adjust the the existing implementation for running those subjects.  
**Sean Winslow:** Okay. Yeah, I'll send you uh I'll send you what I have on the actual tickets and the example he gave me and then I'll tell I'll ask him what the differences are and then if we can we can all sync up, he can explain uh exactly what the differences are.  
**Nikita Orobenko:** Mhm. Okay. Yeah, that will be perfect.  
**Sean Winslow:** Cool.  
**Edvinas Rupkus:** Okay. So, so to summarize uh we as product and engineering need to look into discuss the uh O sort of decisions in terms of go and campus and when do we want to bridge that and want to do it um now basically with this project then we'll also owe you the uh designs for the dashboard and the actual individual uh sponsored course and then um yeah  
**Claudine Daumur:** Can you make a ticket for that?  
**Edvinas Rupkus:** absolutely.  
   
 

### 00:36:33 {#00:36:33}

   
**Claudine Daumur:** Yeah.  
**Edvinas Rupkus:** Uh and then am I missing anything else,  
**Sean Winslow:** Uh,  
**Edvinas Rupkus:** Sean?  
**Sean Winslow:** I'll David about the Rise 360 and understand what the differences are and if we actually have to dig in deeper. And that was really about it. CL, what what did you say you wanted to make a ticket for?  
**Claudine Daumur:** for the for the sponsored courses uh but within the confus product and uh I just wanted to clarify  
**Sean Winslow:** Okay. Yes.  
**Claudine Daumur:** something um regarding the profile creation. So now it's my understanding that um not only the profile creation actually but the whole um the whole um login process. Uh so now I feel like it shouldn't look like uh blog.co co um UI but uh it should be like uh like the compus product UI because it would happen uh on compus side right all those  
**Edvinas Rupkus:** Yeah, it will live.  
**Claudine Daumur:** uh okay okay so yeah I will I will change  
**Edvinas Rupkus:** It will live on campus. Yes.  
**Claudine Daumur:** that  
**Nikita Orobenko:** I mean but if we do the bridging so you will be able  
**Claudine Daumur:** Yeah.  
**Nikita Orobenko:** to authenticate if uh with the campus account on the call side and the vice versa with the uh co account on the campus side. Uh it may be funny but we can call just the block ID and uh it may just look a bit different because you will create one account for both uh things at one time kind of but it depends on the bridging itself and how exactly we're planning it to  
**Claudine Daumur:** Okay.  
**Edvinas Rupkus:** Any  
**Nikita Orobenko:** do.  
**Sean Winslow:** Okay.  
**Claudine Daumur:** Okay.  
**Edvinas Rupkus:** other comments or concerns? I'll set up some time, Mike, for us to discuss the any problems or uh you know things we need to chat about the the go off.  
**Mike Price:** Cool.  
   
 

### Transcription ended after 00:39:12

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*