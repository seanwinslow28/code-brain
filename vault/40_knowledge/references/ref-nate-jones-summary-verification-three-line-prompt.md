---
type: reference
domain: [claude-mastery]
status: draft
ai-context: "Nate Jones' three-line verification prompt: makes the model re-check its own long-document summary against the source and flag low-confidence spots before you trust it."
created: 2026-05-21
---

If you’ve ever asked AI to summarize the transcript of a messy meeting or a long document and the summary sounded confident but missed the thing you cared about most, this one’s for you.

Summarization is the most common AI move I see in the wild, and the easiest place for hallucinations to slip through unnoticed, because the longer the source, the less likely anyone is to go back and check.

Monday’s piece was about catching those after they show up in an answer. The prompt I want to show today is what I run before that, to make the model check its summary against the source before I trust it. It makes the model do a second pass on its own work, with the source material sitting right there, and it flags the places the model isn’t sure about.

It’s three lines long. Here it is:

`[YOUR ANALYSIS REQUEST]`

`After providing your initial analysis, complete these verification steps:`

`1. List three specific ways your analysis could be incomplete, misleading, or incorrect`

`2. For each potential issue, cite specific evidence from [DOCUMENT/DATA] that either confirms or refutes the concern`

`3. Provide a revised analysis that incorporates verified concerns and acknowledges remaining uncertainties`

The first bracketed bit is where your question goes. The second is where you point the model at a document or data you’ve pasted in. If there isn’t one to point at, change it to your initial answer and the model will check its own work against itself.

What changes when you add this block is the job the model is doing. The first time through, it’s trying to give you an answer. The second time, with the verification steps nudging it, it’s trying to catch where its own answer might be wrong.

The cost is that the second pass takes longer and the revised answer comes back more cautious than the original. So I save it for the questions that earn it: legal documents I’m summarizing before I act on them, medical or insurance reads where the details change what I decide, financial breakdowns I’m about to repeat to someone, research summaries going to a boss or a client.

## **The pigeon test**

I pulled up a paper that claims pigeons can differentiate between the paintings of Monet and Picasso. The paper has a clean, headline-friendly finding and a much messier underlying story, which makes it a useful thing to test the prompt on. Hand the same paper to the same model with two different prompts, and you’ll notice the output gives you two different versions of “the truth.”

The first prompt is the one most people would type without thinking: _Summarise the key findings of this document._

The second is the same request with three lines bolted onto the end:

_Pull out the three most interesting findings with numbers and setup. After your initial analysis, list three specific ways your analysis could be incomplete, misleading, or wrong. For each one, cite evidence from the paper that confirms or refutes the concern. Then provide a revised analysis._

The model still hands you the confident summary at the top, but the self-check pulls things out into the open that the first pass left buried. It admits the sample was eight pigeons with substantial individual variation, which is a real thing to say about a study and not a thing the original summary mentioned.

It notes that the generalization was weaker than the headline implied, because the birds responded more strongly to images they had already seen in training than to new ones, and the paper itself flags this in a place you’d miss if you were skimming. It raises the possibility that what looks like “concept learning” might be the pigeons reacting to combinations of low-level visual features — brush stroke density, color variance, that sort of thing — which is a less romantic finding than birds-grok-Monet but a more defensible one.

|   |   |   |
|---|---|---|
||[![](https://ci3.googleusercontent.com/meips/ADKq_NbO1TWI1Fe1lWnc7O6gdsrkuAvqJ8Y1y342jMocKinXXTMXZIiQl23_J2ikrYMzOroRYnbSx8bi9V06SpBXJ48z0lQW4NejWYu5naBQLm6CDn52i5Jx88EPKbp8faTiFTY6wyXaA4E6M3tTamEQoFzLINeC55M18eZY8FSqRYtZPY1J-Hpbai2aRcVzZpkASej-9Ldtdqxp155SDKgPsJRa4JURQeK-xIEAGBAkQwOVdEL5CVKpvefbuh1xRPucByhs11lv6WNy3cuDj8c2hfZHH7aBUEjA55IEU4yLuvcVFICL5XGcpz8_GMJvtOb4CZqxHJ0=s0-d-e1-ft#https://substackcdn.com/image/fetch/$s_!TALl!,w_1100,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb08e43b1-7748-4abb-a693-a10faa716f04_1446x318.png)](https://substack.com/redirect/fc45d30a-ae98-4fdb-a707-38c5a09fa11f?j=eyJ1IjoiMXl1b21tIn0.aG4yU6FuXGvN-q-2o5knL2EChKsjMX-SMuvyUWnuDdE)||

Here’s the conclusion of the prompt *with* the three sentences added

|   |   |   |
|---|---|---|
||[![](https://ci3.googleusercontent.com/meips/ADKq_Nbf8Gww28Y2HoEzmnlQjSht2vwOoujk1yOxyltKMn1FHSL_NCh124lLbM8sHLPuDwQ_Y_E2gi9UHSnhSEiOa6el_7KqpvdKjGRvhGqUjgd0w_7BuJLV83wq0VvSn9jEy2CjBBMEOzuYZeTyyF2H9xzx8agru6kvpnk9PjtUcyf3Oni27p6hrbrGTkLcPXwKUiME7UR-eGmTq238haTaczwawg7lke8LrvtsmYeI4NscoDSdq9mzb0jSlxnSZxp-6JVAyQ3spu85-uOEIs9k0yXE8zOsAad-ygt2AwnZ2xgIfotbCb7c9BtZD6BGhrghQRIVpIc=s0-d-e1-ft#https://substackcdn.com/image/fetch/$s_!z4lT!,w_1100,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02c9656b-985d-40fe-b534-8568d9906c01_1518x740.png)](https://substack.com/redirect/3d8c1989-c434-4ca7-8e40-c77d8c3da5e9?j=eyJ1IjoiMXl1b21tIn0.aG4yU6FuXGvN-q-2o5knL2EChKsjMX-SMuvyUWnuDdE)||

## **If you take one thing from this**

The trick isn’t a smarter model, it’s giving the model a second job. The first pass is built to sound right. The second pass, if you ask for it, is built to find where the first pass might not be. That’s most of the difference between an answer you can repeat and an answer you can’t.

## **Up next this week**

Friday’s piece is the longer walkthrough of two settings in your AI tool that can change how often it makes things up.