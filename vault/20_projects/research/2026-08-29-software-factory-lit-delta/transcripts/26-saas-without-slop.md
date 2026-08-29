# How to Build SaaS With AI Without Making Slop

Source: https://youtu.be/0ajxdUNacQE?si=tBP58_-YRcEv_ID1 — NotebookLM-indexed fulltext, dumped 2026-08-29. Transcript text is auto-generated; names/products may be mis-transcribed.

I've built several SaaS products with AI in just 
[music] one week. And the biggest misconception I  
see is that you can simply open an AI code editor, 
type a prompt, and get a finished product. But  
that's not how I do it. I've been getting a lot 
of questions about how I actually built websites  
and SaaS products with AI. So, in this video, I'm 
going to show you SaaS products I recently built  
and walk you through my actual workflow from the 
initial idea and design to coding and setting up  
the back end, emails, refining the UX UI, and all 
the iterations in between. I will [music] show  
you where AI does the work, where I take 
over, and how I turn AI generated sloppy  
prototype into something I can [music] actually 
ship and sell. And by the end of this video,  
you should have a much better idea of how to take 
control of AI before AI takes control of you. Hi,  
my name is Sergei and welcome to my channel. 
Here I talk about design AI vibe coding tools  
and workflows. [music] So if you want to 
learn more, be sure to subscribe to my channel  
if you haven't already and like the video if you 
like it. And now let's get started. Recently I  
partnered with Mobbin. So thank you Mobin so much 
for sponsoring this video. First of all, I'm using  
Claude to validate my idea. This is a preparation 
part which is super important. And this is where I  
create my master prompt that I use to build 
the product later on. And uh it's important  
to understand it's going to be an MVP. It's 
minimal valuable product. It's going to have the  
basic functionality to start from. So we need this 
like core idea and core project to work on and to  
build it later and to update it later. So I talk 
to my cloud validate the idea. I explain what I  
want uh like what's going to be my first features. 
Uh very important is to understand if I'm going to  
be using any APIs this moment and what I need in 
terms of the back end and how the back end will  
be set up. Here I get the information that I'll be 
using the IMDb API. By the end of this dialogue,  
I get this file over here. And this is my master 
prompt basically with information about what  
are we going to build and how it's going to 
be built. Next, what I need to do, I need to  
create a project folder. Uh doesn't matter where 
you use claw code or use cursor. So, I have my  
folder open over here. So, currently I'm building 
this movies calculator website. And here I got  
my um project information uh document. So this 
was the the document that I got from the clog.  
Next I go to my agent and I tell the agent to 
examine this file and to create an implementation  
plan. So basically I'm using a plan mode and this 
is what I'm getting. I'm getting this plan of how  
the project will be implemented. Then I switch to 
agent and I choose the agent. So whatever you want  
to use Cursor is now part of the space x. So I you 
can use grock uh the latest version or uh or you  
can use composer 2.5. It's really cheap and in 
terms of comparing to for example other models  
it works I guess mostly like opus. So very very 
cool model and really fast and cheap of course.  
After the first implement, I get the first concept 
and it looks something like this. So I have it in  
Figma. These are like screenshots and this is what 
I got. So basically I got a really generic design  
as you can see over here. Then what I did I needed 
to do some iterations on the design. What I got  
was actually this website. So as you can see it 
looks much more interesting. Uh of course I have  
the dark and light version. I have my calculator 
working. So the core idea is to count how many  
hours or how many movies can you watch during the 
certain period of time. Uh and here I can watch  
182 movies over the next 6 months if I watch only 
one hour per day. Right? So this was like again  
the core idea of the website and also I had things 
like uh different SEO pages for different for  
example TV series or for example for different 
franches uh like Harry Potter or Marvel comics.  
I did some updates for the design. As you can see 
I added some blur effect and actually it takes the  
color from the covers and uses it to create uh 
this background blur. And here you can see like  
how many hours you need to watch each movie. But 
I wanted to take it even further and this was my  
idea. I wanted to create a watch list because 
I collect the movies in my reminders app or in  
my notes app or notion everywhere basically. H I 
just love to watch movies and then I kind of like  
check them off, delete the movies that I watch or 
something like that. So, I wanted to have like a  
catalog or the way to keep track of the movies I 
watched. And I thought it would be really cool to  
see how much time I spent watching movies and how 
much more time I need to watch all of my movies  
uh in the future. So, I decided to build a profile 
section on this website and to have uh a profile  
page and a watch list. So, let me show you on 
the real website. So this is the actual website  
and here as you can see I have this pretty 
cool menu and [snorts] this is the watch list  
and to have all of these things working like 
uh to keep the information about my profile  
and to keep track of the movies that I have 
watched. I also have the achievements here  
uh to see how many movies I watched to have the 
profile. I have this uh handle for each account.  
But here's the thing. I needed to understand how 
to create this user profile flow with all the  
screens and settings and all of those things. So 
if you're not sure how to do that, the best thing  
is to go to Mobin. And this is what I did. I've 
been using Mobin for so many years. And Mobbin is  
a huge library of real apps and real website, not 
just like some concepts from Pinterest. These are  
real working apps as you can see them over here. 
They they update their database and bring new apps  
in really fast. So for example, you can see here 
a grogbo it was just released a couple weeks ago.  
Uh and here you can see like different 
categories. You can see different screens  
and even UI elements. And most importantly you 
can see flows. And in my case I wanted to see the  
login flows and understand how they work. And 
here I can pick the iOS or the web. I can look  
at different projects and different companies, 
different apps, how they handle this workflow of  
actually logging in and even you can see even has 
this superb base that I just showed you right now.  
Even framer, all of those things. Of course, you 
can look at them by yourself and uh get inspired  
and then prompt your agent uh how you want this 
process to be or you can even copy these images  
and these flows into Figma. What you want to do, 
you want to connect Mobbin to your AI agent. And  
for that, go to your Mobin profile over here. 
Click on the image and then click on MCP.  
And on this page, you will see the instructions 
how to connect Mobbin to the particular AI agent  
for example like Claude Code or Cursor etc. And 
as you can see, I have connected Mobin to claude  
and cursor. For claude, you just need to paste 
in this command into your terminal and run it  
and it will connect. And for cursor, you can do 
this manually by adding this custom MCP setting.  
But you don't need to do this actually if you're 
using cursor because recently Mobin got their  
official plugin to cursor marketplace. And in 
fact, this is the only design plug-in out there  
right now. So let me show you how it works. You 
go to cursor, you go to cursor settings over here,  
and then on the left you need to find customize. 
Click on customize. And here is the input like  
search bar for the marketplace. Of course, you can 
click browse marketplace and find different things  
here that you can connect, but we're interested 
in mobin. So, I just search for mobin. Here it is.  
And I need to click add to cursor. So, I click add 
to cursor. Now, I need to pick I want to add it to  
the whole account or just to my project. 
So, I will add it to the whole account.  
And I will just click add. And that's it. So, it's 
ready. I have it set up over here. As you can see,  
it is connected and now I can use it inside of my 
cursor. The only thing that I missed here is that  
I didn't log into my mobile account because 
I already did it before. For you, if you're  
doing this for the first time, probably you will 
need to authorize your mob account inside cursor,  
but it will take you like 1 second to do. After 
that, what you want to do, you want to create this  
little prompt. For example, use mobin MCP to 
analyze best practices of logging in flows in,  
for example, lifestyle apps and profile settings. 
I need some easy and simple flow using email magic  
link. Create step-by-step full description 
to use in my app. And this is what you do.  
You just paste it here. Go to, for example, ask 
mode. Just paste it here. and it will run through  
hundreds of real life apps and find out the best 
flow that can be used for your project. All right,  
so cursor just finished the job and as you 
can see it pulled up all the information.  
It created this graph of how it can be done uh 
with all the structure the information here what  
we need to have the email how it's going to work. 
Uh then we have the checkout inbox. Step two,  
all of those things over here. It's written down 
the profile. It also uses you see the the links  
to the real apps that you can click on and go and 
check out how it looks in like how the UI looks  
in their product. So this is super cool. Also the 
error and edge cases. So everything is ready. You  
just need to implement it to your app. And this is 
what actually I did. And most importantly, if you  
use my special Mobbin link from the description 
below, so just go to mobbin.com/chyrkov, that's  
c h y r k o v and get your 20% off discount on the 
pro plan. And thanks Mobbin again for sponsoring  
this video. And now back to my profile and this 
is what I actually did. So I have the sign in. Uh  
now I have the settings and as you can see in 
settings, see I can even change the colors.  
These things are saved inside of my super 
basease. I have the social links for my profile  
and basically my profile looks something like 
this and then I can sign out again sign in  
and this how the process looks. So let's sign 
in. So I use my email I will get the magic link  
to my inbox and this is email from my product and 
here's the button that I need to click and now  
I'm signed in to my project. As you can see colors 
changed because I had a different color set in my  
profile. And of course I can use a dark mode. And 
for that I need to use superbase. Supabase works  
super easy. What you need to go you need to do you 
need to go to superbase.com and just click start  
project and in your project you need to connect it 
to your code agent. For example, it's going to be  
again cursor or cloud code. It's super easy. Let 
me show you how to do that. So you go to connect  
and here you need to pick your client. For 
example, mine is cursor. And here you can see  
there is a little prompt. window. Uh, I can copy 
the prompt and send it to the agent or I can set  
it up myself. I figured out that it's easier for 
me and faster to set it up myself. So, I just copy  
this configuration file. I go back to cursor. 
I go to settings. The same you can do in code.  
Just go to settings and go to connections. There 
here I need to pick MCPs and add new MCP server.  
So, I just need to copy the code uh from this 
window over here and that's it. And then I need  
to authorize it. After that my cursor project 
as you can see is over here it is authorized.  
Um it is connected to my database. And now what 
I can do I can now create the profile section  
have the login log out keep all my movies set up. 
And actually anyone you can uh connect to this  
website and create an account for yourself totally 
free. You can sign up and I invite you to do that  
right now. And I just wanted to take this moment 
to remind you that if you want to learn more about  
Claude design or AI design workflows, be sure 
to check out the links in the description below  
to my one-to-one sessions and subscribe to my 
newsletter. And now, as you can see, we have  
another very important step is the part where we 
get the email and email is being sent by a special  
provider. And as you can see, I'm using loops 
for sending out all the transactional email. Of  
course, you can use Loops or you can use recent. 
It doesn't really matter. But in any case, you  
need to have an account here. You can use a free 
plan. Uh it totally enough for a small project.  
And after you have your email client set up, you 
need to tell the agent inside of your Cursor or  
Claude Code to connect your Supabase to this email 
client and of course to run it on your website. It  
will create a very important file which is called 
env file where you will have all of your secret  
data stored. And here as you can see I have links 
for Loops transactional email. So there's several  
links that several keys that you need to import 
from your actual um account. This will be synced  
with your superbase and this way uh when user 
logs in to your website. So basically uh superbase  
will get the email and it will tell the uh email 
client to send the link to the user. User uses the  
link uh this is a magic link. So it has a special 
code inside. So it follows the link gets to the  
website and uh sort of like superbase sees that 
and lets the user in. And the next thing what you  
want to do of course in your SaaS part you want to 
add monetization. And for the monetization, what  
you need to do, you need to connect it to Stripe 
or some other service provider, for example,  
like Lemon Squeezy or Polar. In my case, for this 
project, I'm using Lemon Squeezy because it was  
much easier for me to set it up. So, the next 
step will be is to go to Lemon Squeezy and set up  
an account there. Uh, Lemon Squeezy works better 
because uh, in some countries uh, you don't have  
the option to set up stripe, but Lemon Squeezy 
allows you to do that from, I guess, most of  
the countries out there. So, it's really easy to 
set it up. You set up Lemon Squeezy and you need  
to create a product there for your monthly plan 
and for your yearly plan. So, only two products.  
After that uh you will get an API key or just 
your like secret key and your product key which  
you will add into your env file. So basically 
here I have the Lemon Squeezy setup and here's my  
uh store ID and this these are my links uh 
to my um products. So this is my monthly  
and yearly uh products and that's it. So basically 
you tell the agent that you need to set up Lemon  
Squeezy and will do the trick and after that you 
need to run it in the test mode just to see if it  
works. So then you just switch off the test mode 
and your website is running. Just let me show you.  
I will go to my superb base right now and I'll go 
to profiles and as you can see these are all the  
people that are active on the website right now 
who are registered on my movies calculator. So  
um there let me check I think there are about 
like oh 66 well minus the test user so it's about  
60 people right now who are registered on movies 
calculator. So after you have set up your database  
with a transactional emails and connected uh 
stripe or lemon squeezy doesn't really matter for  
payment gateway uh let me show you how it looks uh 
from the user's point of view u what it has inside  
of his profile. So basically in um the profile we 
show him a pro badge that's very important that he  
has a subscription. Uh then in the menu we have 
the billing. Uh we can also go to settings and  
see the billing over here. And when user clicks 
on the billing we open the lemon squeezy page or  
the stripes page. So this is the best way to 
do this because you don't need to save all the  
financial data on your site. Basically all the 
financial data is saved on Lemon Squeezy or  
Stripe. So this is very important for compliance. 
So as you can see it even has its own domain over  
here. So it's in the Lemon Squeezy domain or in 
stripe again it doesn't really matter or polar.  
Uh and here you can see the subscription. You can 
see the billing information and the payments. Um  
also if the user has an active 
um debit card or a credit card  
that he uses for the payment method uh you 
will see it over here. So from this page user  
can manage actually the subscription. Uh user can 
cancel a subscription or pause it or renew it if  
he needs to. There are two very important files 
that you need to have in your project as well.  
One of them is the change log MD file. This is the 
place where agent should save all the updates that  
it does to your project. As you can see, it 
saves it shows the date and what actually was  
added or changed. This is very important because 
you can always go and check uh what was done and  
sort of like see the process of the history 
of the changes uh that were done to your  
project. And another important file is design 
system MD file. In the design system MD file,  
you save all the information about your design for 
example and your like design tokens like colors,  
typography, uh all of the for example scaling 
tokens and shapes and all of those things. This  
is very important to have because agent is looking 
at this file and your designs look consistent  
and you're not getting like different for 
example buttons, different uh sizes for I don't  
know spacings, gaps and all of those things. So 
basically uh this file is the source of truth for  
all of your designs. And when you do the updates 
to design, when you want to play around with the  
UI, you always say that you need to up, you tell 
the agent to update the design system uh to save  
all of those things. Uh this is how I got it from 
the generic design that I got at the first place  
to something more interesting and something more 
human uh made. After everything is set up on your  
local host, of course, you need to launch it on 
your server. And for that, I will use Versal.  
And I recommend everyone to use Versal because 
it's super easy to set up. You can connect cursor  
directly to Versal. But I prefer to use GitHub. So 
for that I uh connect my cursor to GitHub account.  
So all of my changes and all of my updates are 
written and saved on my GitHub cloud. So every  
time I do a major update, I push it to GitHub. So 
when you're on Vercel, you just need to link your  
GitHub account uh to Vercel and just link it to 
a project particular project and it will set it  
up. So Vercel works super great with all the 
web apps because uh this is a web app. It runs  
on Next.js. Uh and here is the dashboard how it 
looks. And now very important thing that uh some  
people forget to do is to go to environment 
variables. And here you need to add all of your  
secret data. For example, like um lemon squeezy 
data, your loops data, stripe data if you use it  
or Supabase secret keys, all of those things. 
And API keys of course you need to add all of  
them here on Vercel. So these are the ones that 
you had here on your local host and your env
redeploy your project. So this is important 
because if you don't add these files over here  
your project will not work. After that you can 
connect your domain. So super easy again you  
can buy domain from versal here. Uh if you use a 
pro plan um you will get a free domain. So I have  
my domain already set up. So it is connected to 
my project as you can see. Uh and it is running  
live. So check it out. You're welcome to log 
in and to subscribe to this feature. I hope  
you like it and I hope you will uh have fun with 
it with uh creating your uh movies watch lists.  
Thank you so much for watching this video. 
I hope now you have a better and clear  
picture of how to set up your first or maybe 
[music] not the first SaaS product using AI,  
how to build it from scratch. So if you like 
the video, please give it a thumbs [music] up  
and subscribe to my channel if you haven't 
already and I'll see you in the next one. Bye-bye.
