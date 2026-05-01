---
granola_id: 3ddc48dd-600b-49d7-90a9-c9ba6b7a4e3b
granola_type: transcript
type: meeting
domain:
  - product-management
status: active
ai-context: Full transcript of unified daily standup - transcript.
context: the-block
created: 2026-04-29
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
  - kbaspinar@theblock.co
  - bvadimovich@theblock.co
  - ysmagulov@theblock.co
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
- Koray Baspinar (kbaspinar@theblock.co)
- Bogdan Vadimovich (bvadimovich@theblock.co)
- Yermek Smagulov (ysmagulov@theblock.co)
- Serena Ho (sho@theblock.co)
- K. Oliva (koliva@theblock.co)
- Ramuald Vishneuski (ramuald.vishneuski@ventionteams.com)

### Guest (2026-04-29T14:01:08.805Z)

Latest crypto news works because this is not based on ACS. This works fine. And it can kind of have unlimited pages. But everything else that is based on ACS cannot have more than 10,000 results or 1000 pages. So I wanted like to clarify. So it is like kind of expected that if you insert, for example, like if you insert like, I know article that like was created yesterday, you inserted like in a search, you will see it like in a search. But if you like insert like a very old article, like for example some kind of you won't see it. At least I tried like with like five different articles and they just do not appear on search. So it's kind of okay. It's like expected right or it's not. I think it's so that's how it works. Okay. I think this is. Like something that is also like I think we struggled with this like for a long time and I think like kind of those. Like kind of. Some words mess up with the logic of search. And yeah, I'm not sure. Okay. Now I now I get it. We're okay with the limit for 10,000 results because back then did some. Fixes for categories pages, but that also affected like this search page. And that's all for now. By in the future it may affect some other collections like authors or when authors get more than 10,000 pages and stuff. So everything we have this collection you have this limit. Yeah, I don't like it. But. I'm not sure like what what can be done. Like for now it's anyway better than like having like broken UI. I mean and like kind of broken user experience. It's better to have like at least like shown 1000 pages then well show 3000 and 2000 of them do not work. But yeah like it's still not perfect I guess. Yeah absolutely. Let's limit it 1000 like let's hide the broken pages. Yeah but like how to how to actually fix it. I don't know. I don't know. Let's ask Amazon to change their policy. This like yeah maybe maybe a good thing to do would be to replace ACS with something that is not deprecated because yeah ACS is deprecated by Amazon so we can use it only because we were using it before it got deprecated but they closed it for new users and they are kind of forcing everyone to use elasticsearch. Which is a different service for searching. Is it more powerful? I don't know. Never used it. Anyone else knows like kind of comparison between cloud search and elasticsearch. So tell us. We should definitely add that or like that. Let's investigate. More beneficial. We don't have enough time to solve our tech and imagine like how much time we have to take that. Gotta pay up the debt. Kind of if you think about it. The more pages appears like on the website the more website lives the bigger like you know. Number of pages that are essentially not being shown. So like at some point oh yeah we are showing 5% let's go I mean that's probably exaggeration but you get it. Ready to jump into daily.

### Sean (2026-04-29T14:06:06.910Z)

Yeah, you guys good?

### Guest (2026-04-29T14:06:10.405Z)

Yeah.

### Sean (2026-04-29T14:06:10.990Z)

All right. So we. So I apologize for the background noise. Some guys just sawing away all goddamn morning. But, yeah. So we'll start with Anna.

### Guest (2026-04-29T14:06:27.285Z)

So each test in the databug that Kristoff just created production and that is looking good. So this is bug that various mentioning on the thread so we can form in the thread. And well sorry this was the one that we're overlaps the menus and whatever. Yes correct thank you. Yes you so I will continue with the wallet connection book I'm seeing some errors in there so I'm checking that and also for the sponsored course. That's amazing.

### Sean (2026-04-29T14:07:16.110Z)

Awesome. Thank you, Anna. Well done.

### Guest (2026-04-29T14:07:22.325Z)

Yes hello there so I was working on that Maria sticks for list of tokens and you and like podcast UI issues and I found like a few more problems and I fixed so they are on dev boxes already and also like made a small adjustment to like AI generated metadata ticket and it essentially is also ready for testing. I will create actually I can create dev box right now because build like job is failing constantly I like try to rerun it five times but it's still failing. So yeah unpleasant hopefully it will be also like fixed on its own maybe and yeah that's pretty much it.

### Sean (2026-04-29T14:08:20.830Z)

Thank you. Could you guys discuss that during the dev sync? That is. I feel like GitHub has been having issues lately. No?

### Guest (2026-04-29T14:08:30.885Z)

We've not discussed because I forgot about it but yes it has issues.

### Sean (2026-04-29T14:08:32.750Z)

Okay. Gotcha. Cool. Thank you, bovadam. Brian.

### Guest (2026-04-29T14:08:42.725Z)

I was getting elections or just in general my stack set up again had this update a few things and rebuild images so I will wrap up the election hub updates today as yesterday was spent just setting things up again. And they put up a bunch of other PRS up for testing and review. There's one more pre bit update that I will work on smaller one but we did deploy another set of updates last night hopefully Jeff will be happy by Friday.

### Sean (2026-04-29T14:09:12.270Z)

Yeah. I appreciate that, Brian. Thank you. Caesar.

### Guest (2026-04-29T14:09:21.445Z)

Well apart from some small issues in support I keep working in the mid ratio I immigrated several workspace key working because there are like 20 30 workspace to migrate. Terraform workspace the BigQuery in gcp and now I'm writing the BI stream so there are several workspace a lot of them have changed my hand so I need to update the terrible code working this task is really really complete really long but if some small task appear seen in this war of course I'm going to have time for them because this task is the the main one but I believe I should have time for small task in case of appearing so keep working on this that's from my side.

### Sean (2026-04-29T14:10:32.270Z)

Nice. Thank you, Cesar.

### Guest (2026-04-29T14:10:34.165Z)

Thank you.

### Sean (2026-04-29T14:10:39.470Z)

He's out. Kristoff.

### Guest (2026-04-29T14:10:44.725Z)

Hi guys I'm still six I just came here kind of to say that I deployed the ticket with overlay and then I would be kind of taking it the rest of the week off and then starting to prepare for the final citizens I guess this is a bit of a goodbye. I will join on the call the CEO next week.

### Sean (2026-04-29T14:11:11.950Z)

Come in. Thank you, Kristoff. Yeah, I hope you feel better. And good luck on your finals. And, yeah, definitely please join with the CEO call. Mike. On. Pivot. Akita.

### Guest (2026-04-29T14:11:55.045Z)

So for campus we are working really really closely with Nikita on the bugs which Ramo graciously provided basically dropped for now the distinction between France and back and just taking them on one by one some of them are already fixed and we are continuing to well kick them off one by one. That's the main thing there and they have also another update for Ed regarding the emergence thing. Y which you've asked to adjust yesterday. So strictly speaking it is done but the deployment actually failed and I've noticed it only today and deployment fails. Haven't said this word in a while. Bear with me for a second because they're visible so I'll take another look at it and I'll have the time away from from the bag from remaining bugs and adjustments at campus. But overall it still it seems like it needs another look because the basically the deployment pipeline is broken. Because. Something is wrong with visible once again and we are still using it to fetch. Speakers. Prior months and that would be. It. What a blast from the past. Yeah truly I was like I was looking at it. Like haven't seen this word in a while. Haven't been mad at them in a while as well.

### Sean (2026-04-29T14:13:29.710Z)

What is it called? Indivisible.

### Guest (2026-04-29T14:13:34.085Z)

B I Z Z ABO it was the app we used for provider reuse for our conference in 2024 and Nikita has very intimate knowledge of the ins and outs of visible.

### Sean (2026-04-29T14:13:36.830Z)

Okay. Yeah, I picture. I picture an internal slackabo.

### Guest (2026-04-29T14:14:01.445Z)

This is yeah if it's giving you more issues just like forget about it yeah I've noticed it but did no action so far once I have the time I look into it of course just something on my radar for a bit later.

### Sean (2026-04-29T14:14:16.670Z)

Thank you, Nikita. Nikita. Oh.

### Guest (2026-04-29T14:14:23.125Z)

The large portion of the fixes based on the rules findings across the sponsor course right now I'm working on the authentication adjustments we discussed yesterday. To allow crypto a key user to sign in normally without the pain in the ass for us them without touching the data. And having more. Painful problems in the future. I would call it like that I think that's it most likely we'll finish with the authentication today and we'll pass it to testing as well.

### Sean (2026-04-29T14:15:14.910Z)

Sweet. Awesome. Thank you, Nikita. Michaela.

### Guest (2026-04-29T14:15:22.245Z)

Yeah so struggled today and still had didn't fix the dev box for job jobs asked Caesar to help out and sorry Caesar for taking a lot of your time. But still yeah they're still issues so yeah we'll try trying to figure it out. And yeah while I was waiting for Caesar to check some things out I did fix add I have a pull request for. What's L Max or the next page for the 15 rows and it looks bad in my opinion but like yeah from experience we don't say anything yeah yeah the approach is like yeah let's just roll with it so if you say it's done and let's move on yeah create the dev box for it and yeah hopefully like the issue that with the dev box that we have is with. The campus elements so I think yeah this this the box should should work fine and I think I can. They want to introduce like the four new. Tickers but they're not currently in dev or in prod so I'm not sure like. When they will like do it I don't know like so we need. Coordinated with them yeah we need to kind of coordinate but like in the meantime I'll put the put it on that box and I added those like four tickers also like in the right like the yeah.

### Sean (2026-04-29T14:17:10.670Z)

Cool.

### Guest (2026-04-29T14:17:11.045Z)

Alrighty.

### Sean (2026-04-29T14:17:12.590Z)

Thank you, Nicola.

### Guest (2026-04-29T14:17:14.805Z)

Thanks.

### Sean (2026-04-29T14:17:15.230Z)

Rama.

### Guest (2026-04-29T14:17:17.525Z)

Hello I continue with sponsored courses and that's all.

### Sean (2026-04-29T14:17:23.950Z)

All right, short and sweet. Digarama. Ed, you got anything that you want to add?

### Guest (2026-04-29T14:17:37.125Z)

Nothing particularly when we work on many different things and. Like gonna ensure the transition from that is as smooth as possible. Obviously we'll meet next week with the CEO as a team. And have a lot of work to do to prepare you know roadmap and etc. So mostly like. Working on those those things during months ahead how we're gonna where we're gonna attack. So that's basically on my radar.

### Sean (2026-04-29T14:18:12.910Z)

Cool. Yeah. Same here. And just trying to log into a new apple ID. Since yesterday. But.

### Guest (2026-04-29T14:18:24.405Z)

Teaching us how to vibe code for the iOS app is like he's handed over the like app essentially. So he's spinning us up on iOS app development. Hopefully we'll have time to take a look at that.

### Sean (2026-04-29T14:18:44.670Z)

Just add it to the list. But Mike, are you back? Or.

### Guest (2026-04-29T14:18:51.045Z)

Yeah I'm back what's up?

### Sean (2026-04-29T14:18:53.870Z)

Anything you want to update us on?

### Guest (2026-04-29T14:18:58.005Z)

I didn't get to testing the iOS app yesterday with the sponsor thing I think I'll get to it today so yeah I'll wrap that up. And then yeah. Just working on OKRs really getting okay out of it. So.

### Sean (2026-04-29T14:19:16.990Z)

Cool.

### Guest (2026-04-29T14:19:17.205Z)

Yeah. Brian do we ever sort out the newsletter? It was just sort of triggered as a. Yeah I will try to get to the bottom of that not sure if it was a one-off I doubt it was a one off or mic let's see what happens try to figure it out I for one didn't get any like I think I'm subscribed to both my personal and my work email like pro and regular. So. I didn't get any emails. If that. Makes us feel any better yeah mate I mean maybe it was the one I'm gonna take a look anyway we'll see maybe someone accidentally sent me. A welcome email it was like the welcome email for all three newsletters at the same time right at the same time yeah yeah that's weird that's weirdly triggered or something that's not related that's not related to what was working on with newsletters. Unlikely I don't know like the I don't know what the errors were that in. That those bugs. With like a like a set like a backend thing like send grid then launchpad API something triggered Michael to get three welcomes at the same second. Just weird. Oh you know what I know what it was oh shoot I gotta go guys I'll be right back I know what it was I'll slack y put in them thank you. Oh he's out he disappeared yeah is it because like you sign up to three different newsletters at the same time and then you get like welcome email from each sign up. Neighbor he said yeah he didn't have anything open is the weird fart like he was just chilling at night. So I guess we'll know. One thing that which is kind of annoying. Probably we should fix it I don't know with sand grid or I don't know but so when I when I sign up to four newsletters let's say I sign up for three different newsletters and then I want to. Unsubscribe from those like I cannot there is no like a single place where I can unsubscribe from all the news the Block newsletters. Instead, I need to find every individual type of newsletter and click unsubscribe there. Oh and so so kind of like I got a let's say the daily I unsubscribe and then tomorrow I get the funding and I'm like what like I wanted to unsubscribe and then I have subscribed from that and then like the day after I get I don't know what's the data insights. I'm like what come on is that is that the is that how it's supposed to work? I thought it was. Isn't there a different. Yeah there was like. Rama. Yeah I've tested that a long time ago and as I remember the trick how to do that so you just need to subscribe again. But only for some newsletters. That you really want. About like me getting those emails I'm concerned about like people getting annoyed that they are not able to unsubscribe or at least the perceived like how people are perceiving this unsubscribe that it doesn't work or that it's like oh I need to unsubscribe like multiple times to actually stop receiving emails from the block. But the sangrid does have like like when you click on the unsubscribe like you you should get a list of like all the newsletters and then you can just uncheck all of those. But I think like maybe we switched to different sub accounts for each different newsletter. And then they are treated as different accounts so they they're not shown on the same like UI when you click unsubscribe. I think like that might be something only one of them is on a different sub account the data and insights the other three are on the same. Maybe something to look into. Yeah. I personally like I would I would pause on that because I feel like. I guess technically it could if you wanted to just keep one and not cancel all of them and you would have to resubscribe like resubscribe on the page itself. Like what was for whatever you want. But I don't know. So I get a lot of times like if I get like some you know emails that I don't want I unsubscribe and I continue getting them from the same domain so it's just like. Maybe it's not as big of an issue as it actually is. That that's something I noticed yeah. And I did notice reputation score like dropped to like 80% 85% or something like this. When I when I logged in which one. The main one Block data for the black news. Or maybe like that's. But it's. Why would our reputation for like non primary email like this although when Brian and I were looking at it it was 99 for the news and then yeah maybe like I saw like for a different sub account yeah don't scare me like that Nicola. Took a look right now what it is. But your callouts?

### Sean (2026-04-29T14:25:24.910Z)

Nice. Does anybody have anything else that they want to discuss before we head out? All right, cool.

### Guest (2026-04-29T14:25:34.565Z)

Let me just quickly check in two seconds right now.

### Sean (2026-04-29T14:25:34.750Z)

I'll see. You.

### Guest (2026-04-29T14:25:37.925Z)

Yeah Block news is 99. And. Then. The data one is. 96 yeah so hopefully after we clean it up with Brian and then next week out goes out. Back up after we get fewer bounces. Sorry for the scare yeah.

### Sean (2026-04-29T14:26:07.950Z)

Cool. Everything good? Ed? All right, sweet. Then I will see everyone tomorrow. Have a good one, team.

### Guest (2026-04-29T14:26:18.085Z)

See guys see you babe see you by.

### Sean (2026-04-29T14:26:18.990Z)

See you Thursday.

