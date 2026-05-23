---
title: "Stop telling AI to “make it better.” Tell it what to leave out."
source: "https://nateszerotoai.substack.com/p/stop-telling-ai-to-make-it-better"
author:
  - "[[Nate]]"
published: 2026-05-10
created: 2026-05-23
description: "Most people prompt AI by piling on instructions. The pros do the opposite: they subtract. Here's the one-line shift that fixes vague AI output."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [claude-mastery]
ai-context: "Nate Jones' prompting flip: stop asking for 'warmer/more personal/better' — name what's wrong with the current draft instead. Negative constraints move the answer; positive nudges produce beige."
---
A friend was writing an end-of-year thank-you note to her son’s third-grade teacher last month and asked ChatGPT for help. The first draft came back fast. It was sweet, structured, and it could have been about anyone’s kid with any teacher. So, she tried again. “Make it warmer.” “Make it more personal.” “Make it less generic.” Each draft inched toward a version of the same bland thing.

She wasn’t doing anything wrong. She was using the only lever most of us use, and the lever isn’t the one that meaningfully moves the answer.

*There’s a small prompting shift that fixes this. Here’s the move, and two examples of it working.*

## Why telling AI to “make it better” keeps producing the same bland answer

When we don’t like an AI answer, the instinct is to ask for a better version. Warmer, more personal, more creative, less corporate. We point at the response we got and try to nudge it toward something we’d prefer.

The problem is that AI hears “warmer” and reaches for the average idea of warmth. It hears “more personal” and reaches for the average idea of personal. Whatever it has been trained on, the most popular and inoffensive version of that thing is what comes back.

What is worse, this turns into a loop. You ask for warmer. AI gives you a warmer beige. You ask for “more personal, less stiff.” AI gives you a slightly different shade of beige. The loop feels like AI isn’t listening, but it is doing exactly what you asked.

![](https://substackcdn.com/image/fetch/$s_!sgmi!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e814c36-9bfe-4fae-bbd1-9e5d6ccd8572_1100x938.jpeg)

## You can’t describe the perfect AI answer, but you can name what’s wrong with this one

Here is the conceptual flip.

The perfect thank-you note to a third-grade teacher is hard to describe before you’ve seen one. The perfect cover letter, the perfect apology email, the perfect explanation of fractions to an eight-year-old — all of these are harder to describe than they are to recognize. You’d know the right one if you saw it, you just can’t sketch it from scratch.

The bad version, on the other hand, is easy. You can name three things wrong with it in fifteen seconds.

That is the lever most of us walk past. What to rule out is easier to see than what to aim at. The bland note opened with “I wanted to take a moment.” It used the words “shape” and “inspire.” It ended with a generic line about appreciation. You don’t have to describe what good looks like to know that none of those lines belong in a note about your actual kid and his actual teacher.

There’s a clue about this hidden in how companies develop AI tools. When you look at the prompts that run serious AI products — the kind that power customer support tools or coding assistants — a good percentage of the instructions are about what NOT to do.

## Let’s see this in action

Here’s a bland first draft of a thank-you note.

![Bland thank-you note draft](https://substackcdn.com/image/fetch/$s_!9vr0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed13c4c0-13a4-422f-b297-a5016ffb1a60_1100x694.jpeg)

Bland thank-you note draft

Now the same task, with three patterns ruled out and one specific moment to land on.

![Better thank-you note draft, with don’t-instructions](https://substackcdn.com/image/fetch/$s_!ev4R!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7373310f-5301-41cd-8a81-2e56dbc1df17_1100x827.jpeg)

Better thank-you note draft, with don’t-instructions

The shift in the second draft isn’t because the model suddenly got more creative. It’s because the canvas got smaller. Three patterns ruled out is three fewer places the answer can land in beige.

Take a LinkedIn post about lessons from a failed project. Same idea, different surface. The first draft is always the same structure: philosophical opener, bulleted lessons, hashtags.

![Bland LinkedIn post draft](https://substackcdn.com/image/fetch/$s_!Dw1s!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb599aed5-d5cf-4ae4-a75d-f22cf239c691_1100x798.jpeg)

Bland LinkedIn post draft

Now the same prompt with the patterns named and ruled out.

![Better LinkedIn post draft, with don’t-instructions](https://substackcdn.com/image/fetch/$s_!Z4Hr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2be1cc15-bdee-4888-ac25-1d523d653c5f_1100x913.jpeg)

Better LinkedIn post draft, with don’t-instructions

## Try this

Pull up the last AI answer you didn’t love. The cover letter that sounded like every other cover letter, the thank-you note that sounded like a Hallmark card, the email reply that was too formal for the situation.

Write down one or two specific things you didn’t like. Not “it was bland” — that doesn’t help anyone. Name the actual pattern. *“Opened with ‘I am writing to express.’” “Used the word ‘leverage’ twice.” “Ended with ‘looking forward to hearing from you.’”*

Now run the prompt again with those instructions added: *“Don’t open with ‘I am writing to express.’ Don’t use the word ‘leverage.’ Don’t end with ‘looking forward to hearing from you.’”*

Read the new version against the one you didn’t love. The difference is usually bigger than you’d expect from three small instructions.

## Want to go further

Once you start spotting AI’s tics, you’ll notice a handful that show up over and over — the same kinds of openers, the same kinds of fillers, the same predictable closing sentences. The patterns are predictable enough that most regular AI users end up keeping a small clipboard of standing instructions for them, pasted at the end of almost every request. **On Wednesday, I’ll walk through seven of those lines — the ones I reach for most. For today, the muscle to build is just noticing.**

## What we learned

AI defaults to the average version of whatever you ask for, because the canvas is too big and “good” is too abstract a target to aim at. Naming what you don’t want is faster, easier, and steers the answer harder than asking for a better version. Once you start spotting the tics — the openers, the phrases, the formal closings — you will keep noticing them, and the answers will start to feel like yours.

---
*Clipped from [substack.com](https://nateszerotoai.substack.com/p/stop-telling-ai-to-make-it-better) on 2026-05-23T14:32:11-04:00*
