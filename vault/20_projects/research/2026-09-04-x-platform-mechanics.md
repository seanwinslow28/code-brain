---
title: "X platform mechanics: what is actually true about how a post is distributed"
date: 2026-09-04
status: complete
type: research
tags: [research, x-platform, content-machine, medium-contract, algorithm]
supersedes_research: "#170 (X medium contract, wave 1)"
corrects: ".claude/skills/content-machine/contracts/expressive/x.md"
source_tiers:
  tier_a:
    - "https://github.com/xai-org/x-algorithm — current For You feed source (Apache-2.0, pushed 2026-09-04); cloned and read at commit 9b0dc31"
    - "https://github.com/twitter/the-algorithm — prior dump (AGPL-3.0, pushed 2025-09-08); cloned and read"
    - "https://github.com/twitter/the-algorithm-ml — heavy-ranker training code (pushed 2024-07-10)"
    - "https://help.x.com/en/using-x/how-to-post"
    - "https://help.x.com/en/using-x/types-of-posts"
    - "https://docs.x.com/resources/fundamentals/counting-characters"
    - "https://x.com/elonmusk/status/2082273378749268440 — platform owner statement, 2026-07-28"
    - "https://arxiv.org/abs/2410.17390 — Galeazzi, Paudel, Conti, De Cristofaro, Stringhini; NDSS 2026"
    - "https://arxiv.org/abs/2411.01852 — Ye, Luceri, Ferrara; ACM FAccT 2025"
    - "Direct measurement of the x.com web client DOM and stylesheet, 2026-09-04 (this session)"
  tier_b:
    - "https://www.techmeme.com/241125/p22 — Mediaite, 2024-11-25, Musk on 'lazy linking'"
    - "https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/ — trade press, reporting the July 2026 exchange"
  tier_c_used_for_claims: none
  retrieved_but_unverified:
    - "Bandy & Diakopoulos 2021, Social Media + Society, doi 10.1177/20563051211041648 — publisher returned 403; numbers NOT cited here"
    - "Axios 2023-10-03 on Musk and links — 403; the 2023 quote is NOT cited here"
---

# X platform mechanics

Facts about the machine, from primary sources. Every claim below carries a tier.
Where nobody outside X knows, it says so.

---

## 0. The single most important finding: the algorithm dump you were reading is the wrong one

**Tier A.** There are now two open-sourced X algorithm repositories, and the one everybody
cites is the retired one.

| Repo | License | Created | Last push | Language | Status |
|---|---|---|---|---|---|
| `twitter/the-algorithm` | AGPL-3.0 | 2023-03-27 | **2025-09-08** | Scala/Java | superseded |
| `twitter/the-algorithm-ml` | AGPL-3.0 | 2023-03-27 | 2024-07-10 | Python | superseded |
| `xai-org/x-algorithm` | **Apache-2.0** | **2026-01-19** | **2026-09-04** | **Rust** | **current** |

Verified via the GitHub API (`gh api repos/<name>`) on 2026-09-04. Both were cloned and read.

Three things follow, and they matter more than any individual number:

1. **The 2023 dump is not merely stale — it describes a different system.** The old stack
   ranked with a Scala `home-mixer` calling a TensorFlow "heavy ranker." The current stack ranks
   with **Phoenix**, a transformer that reads the viewer's recent action sequence, written in Rust.
   The candidate sources changed too: the old repo's `search-index` (Earlybird) supplied "~50% of
   posts"; the current one names `thunder/` (in-network), `phoenix/` retrieval and `simclusters/`
   (out-of-network).

2. **The famous 2023 engagement weights were never production values, and the file everyone
   quotes is empty.** In `twitter/the-algorithm` at its final state,
   `home-mixer/server/src/main/scala/com/twitter/home_mixer/param/HomeGlobalParams.scala`
   defines `object ModelWeights` with **every single default set to `0.0`** — `FavParam`,
   `ReplyParam`, `RetweetParam`, `TweetDetailDwellParam`, all of them. Real values came from a
   runtime feature-switch system that was never published. Any post citing "reply = 13.5" or
   "reply = 27" from that repo is quoting a training-config YAML in `the-algorithm-ml`, not a
   production parameter.

3. **The current repo is the opposite: its defaults are stated to be production values.** From
   `xai-org/x-algorithm` README, "Experiments and Configuration": *"we run cron scripts that set
   the defaults in this repository's code to be the primary production values, for example in
   `home-mixer/params/param.rs`."* The same section commits to publishing experiments running at
   ≥10% of traffic, and `docs/BIDIRECTIONAL_BOOST_CHANGE.md` shows a dated diff of a real July 2026
   rollout. **This is the first time X's published numbers have been claimed to be live numbers.**

**Tier A, negative finding.** The `twitter/the-algorithm` README still links its explanation to
`blog.x.com/engineering/en_us/topics/open-source/2023/twitter-recommendation-algorithm`. That URL
is **dead** — it 403s to curl and, in a real browser, redirects to a blog.x.com "Looks like this
page doesn't exist" page. The canonical 2023 explainer no longer exists at its canonical address.

---

## 1. The fold

### What X documents: nothing

**Tier A.** X's help pages state the composition limits and are **completely silent on
truncation**. `help.x.com/en/using-x/how-to-post` gives 280 characters standard, up to 25,000 for
X Premium longer posts, up to 4 photos / 1 GIF / 1 video. `help.x.com/en/using-x/types-of-posts`
repeats the 280/25,000 split and adds one length-dependent rule that is *not* about the fold but is
worth knowing:

> "If you mention an account in the first 280 characters of your post they will be notified. If you
> mention an account after the first 280 characters of your post, currently they will not be
> notified."

Neither page — nor `docs.x.com` — contains the string "Show more" or any statement of where a post
truncates. **The fold is undocumented by X.** That is a real finding, not a gap in the search.

### What it actually is: rendered lines, not characters

**Tier A, direct measurement (this session, 2026-09-04, x.com web client, logged out,
Chrome 148, 1280px viewport).**

The fold is implemented as CSS `-webkit-line-clamp`. It is a **line count applied to a rendered
box**, so it is a function of column width, font size and where words happen to wrap — not of
character count. Measured on a live post body:

```
-webkit-line-clamp: 5
font-size:   15px
line-height: 20px      →  clamped box = 100px tall
overflow:    hidden
class:       font-chirp max-w-full whitespace-pre-wrap break-words text-text line-clamp-5
```

That instance was a **quoted post body inside a quote-post card**, which carried a "Show more"
affordance at exactly 289 characters of text.

Fetching X's shipped stylesheet (`abs.twimg.com/x-web/x-web/assets/styles-B3qqg1Vj.css`, 334 KB)
and grepping every `-webkit-line-clamp` declaration gives the client's complete truncation
vocabulary:

```
.line-clamp-1   .line-clamp-2   .line-clamp-3
.line-clamp-4   .line-clamp-5   .line-clamp-10
.min-[450px]:line-clamp-1   .min-[450px]:line-clamp-2   .narrow:line-clamp-1
```

**Every fold X ships is one of {1, 2, 3, 4, 5, 10} rendered lines.** The responsive variants
(`min-[450px]:`, `narrow:`) prove the clamp changes with viewport — so the fold genuinely differs
between web and mobile widths, and the honest answer to "is it characters, lines, or height" is
**lines, evaluated after layout**.

### What I could not measure, stated plainly

- I could not observe the clamp applied to a **top-level long post in a For You timeline**, because
  that surface requires a login. `line-clamp-10` exists in the shipped stylesheet and is the only
  clamp large enough to be a long-post fold, which is *consistent with* a 10-line top-level fold —
  **but I did not observe it applied, and I am not asserting it.**
- On the **logged-out permalink page**, a ~4,000-character long-form post
  (`x.com/ItsKieranDrew/status/1716071958050123854`) rendered **in full with no "Show more" at
  all**. The fold is a timeline-surface behaviour, not a property of the post.
- **Nobody outside X publishes the top-level fold value.** Every "the fold is at 280 characters"
  claim traceable through search came from social-media-marketing blogs (Tier C) and none cited a
  source.

### The character-counting rules that *are* documented

**Tier A** — `docs.x.com/resources/fundamentals/counting-characters`:

- Max **280 weighted** characters. Latin text, punctuation and common symbols weigh **1**; CJK,
  emoji and most other Unicode weigh **2** (a `👨‍👩‍👧‍👦` ZWJ sequence still totals 2).
- **All URLs are wrapped in `t.co` and count as exactly 23 characters** regardless of real length.
- **Attached media costs 0 characters.**
- Auto-populated `@mentions` at the start of a reply don't count; manually typed ones do.

**Consequence for the contract:** the image is free in character terms and the link costs a flat
23. Neither of those is the fold, and the two limits are independent.

---

## 2. Link suppression

**Verdict: the contract line is stale, not folklore.** It was well-evidenced for 2022–2024 and is
contradicted for the present by both the current source code and the platform owner. Stating it as
a standing "fact about the platform" is now wrong.

### The current code contains no link penalty at all

**Tier A**, `xai-org/x-algorithm` @ 9b0dc31, read directly.

I grepped the entire `home-mixer/` tree for URL and link handling. Every hit is one of: ad
click-tracking marshalling (`util/urt/ad_marshaller.rs`), a `MALICIOUS_URL` **safety** label
mapping, or `util/url.rs` — which is a 15-line percent-encoding helper and nothing else. There is
**no link feature, no URL filter, and no domain list in the ranking path.**

The only link-related term in the scorer is a **positive weight**:

```rust
param!(OpenLinkWeight, f64, "rust_home_mixer_open_link_weight", 0.2);
```

A predicted link-click *raises* a post's score. The old repo agreed in direction: its Phoenix
prediction head set included `open_link` with its own `home_mixer_model_weight_open_link` param.

**One caveat, stated because it cuts the other way.** The *previous* repo does contain a genuine
URL filter — `OutOfNetworkCompetitorURLFilter.scala`, which hard-removes an out-of-network,
non-repost post whose URLs intersect a `CompetitorURLSeqParam` list. But: the param's definition is
**absent from the published code**, the filter is **not wired into any pipeline** anywhere in that
repo, and it does not exist at all in the current repo. It is evidence that domain-level blocking
was *built*, not evidence that a general link penalty *ran*.

Also Tier A: the old Earlybird **light ranker** did use `has_link_flag`, `has_visible_link_flag`,
`has_news_url_flag` and `link_language` as model features
(`src/python/twitter/deepbird/projects/timelines/configs/recap_earlybird/feature_config.py`). Those
are *inputs to a logistic regression whose learned coefficients were never published* — so their
sign is unknown, and that model's own README says it "was last trained several years ago." It
proves links were *observed*, not that they were *penalised*.

### What the platform owner has said, with dates

**Tier A (primary — read directly on x.com, 2026-09-04).** Musk, 9:13 PM 2026-07-28, replying to
Paul Graham's *"You no longer penalize tweets with links in them?"*:

> "We haven't for over a year"

`x.com/elonmusk/status/2082273378749268440`, 231.4K views. The exchange also involved X head of
product Nikita Bier telling Mark Zuckerberg "you do not need to put the links in replies anymore"
(Tier B, ppc.land).

**Tier B.** Techmeme/Mediaite, 2024-11-25 — the *earlier* position, verbatim from Musk:

> "Just write a description in the main post and put the link in the reply. This just stops lazy
> linking."

So the owner's own account is: penalty on until roughly mid-2025, off since. Note this is a claim
about *outcome* with no accompanying structural announcement; the code merely shows no penalty
today, which is consistent but not independent.

### What independent measurement found — and its date

**Tier A, peer-reviewed.** Galeazzi, Paudel, Conti, De Cristofaro & Stringhini, *"Revealing The
Secret Power: How Algorithms Can Influence Content Visibility on Twitter/X"*, **NDSS 2026**
(arXiv 2410.17390, submitted 2024-10-22). 40M+ tweets, 9M+ users.

Method: a **p-score = view count / author follower count**, so author size is controlled for.
Findings on links:

| Dataset | Period | Median p-score, link to news domain | Median p-score, no link | Ratio |
|---|---|---|---|---|
| Ukraine–Russia | 2022-11-22 → 2023-03-01 | 0.033 | 0.246 | ~8× lower |
| US Elections | 2024, around the election | 0.012 | 0.056 | ~4× lower |

The authors' own caveat, quoted:

> "Although the inaccessibility of the platform's recommendation algorithm prevents us from
> establishing an explicit causal link to algorithmic design, our findings provide reasonable
> evidence in support of this hypothesis."

**Both datasets predate the period in which the penalty is claimed to have been lifted.** This is
strong evidence that links *were* suppressed through 2024. It is not evidence about 2026.

### Numbers I am deliberately not repeating

A trade-press analysis (ppc.land, Tier B outlet / Tier C claim) asserts linked posts get "94 percent
fewer views." It publishes no methodology, no sample, and no primary links. The same article dates
X's algorithm publication to "January 2026 and updated in May," which is only half right — the
repo's own commit history shows a 2026-09-04 push. **Treat the 94% as unverified marketing-grade
arithmetic.** I have not reproduced it and neither has anyone whose method I could read.

Likewise, Bandy & Diakopoulos (2021) is a genuine peer-reviewed source on algorithmic timelines
reducing external-link exposure, but the publisher returned 403 and **I did not read it**, so none
of its numbers appear above.

---

## 3. Replies and quote-posts — the section that matters most

This is where the mechanics are most concrete and most counter-intuitive. Two independent Tier A
sources agree, and they answer the author's actual question.

### Replies are worth 0.75× a standalone post, mechanically

**Tier A**, `xai-org/x-algorithm/home-mixer/params/param.rs` and `scorers/ranking_scorer.rs`:

```rust
param!(OonWeightFactor, f64, "rust_home_mixer_oon_weight_factor", 0.75);
param!(EnableOonRescoreForInNetworkRepliesRetweets, bool, "...", true);
```

The README states this in plain language:

> "**Out-of-Network Discount**: posts from accounts the viewer does not follow are multiplied by a
> factor below 1, **as are replies and reposts from accounts the viewer does follow**."

The repo's own unit test confirms the arithmetic — a reply candidate's final score equals
`original_score × OonWeightFactor`. **A reply is penalised the same 0.75× as content from a total
stranger, even when shown to your own followers.** The prior repo had the identical structure and
the identical default (`scored_tweets_reply_scale_factor = 0.75`, `RescoreReplies` in
`RescoringFactorProvider.scala`), so this has been stable across two generations of the stack.

### Replying to a large account does NOT reach that account's audience

**This is the direct answer, and it is no.**

**Tier A, current code.** `home-mixer/filters/oon_retweet_reply_filter.rs`:

```rust
let is_reply = c.in_reply_to_tweet_id.is_some();
let is_retweet = c.retweeted_tweet_id.is_some();
(c.in_network == Some(false) && (is_retweet || is_reply))
    || (is_reply && c.ancestors.is_empty())
```

Removed as a candidate if: **it is a reply and the viewer does not follow you**, or the reply's
thread ancestors failed to load. There is no exemption keyed to who you replied *to*. The README's
filter table states it as *"Reposts and replies from accounts the viewer does not follow."*

**This is a change from the previous generation, and the change went the wrong way for reply
strategy.** In `twitter/the-algorithm`, `OONReplyFilter.scala` was commented *"This filter removes
recommended replies to not followed users"* and kept an out-of-network reply **when the viewer
followed the account being replied to**. That is exactly the "reply to a big account, reach their
audience" mechanism — and it existed. The current Rust filter has removed that exemption. Under the
2026-09-04 code, an out-of-network reply is dropped before scoring, full stop.

**Tier A, X's own help page** (`help.x.com/en/using-x/types-of-posts`) corroborates the
follow-graph half independently:

> "Anyone following the sender and the recipient of a reply will see it in their Home timeline."
> "You will see replies in your Home timeline if you are following **both** the sender and the
> recipient of the reply, or if we think the reply is relevant to you. Otherwise, you won't see the
> reply unless you visit the sender's profile page."

And the reply-opener trap, same page:

> "When you post a post beginning with a username, only people who follow both you and the account
> you are mentioning will see the post in their Home timeline."

**So a reactive one-liner on a stranger's post reaches:** the account you replied to (their
notifications), anyone who follows *both* of you, and anyone reading that post's reply thread. It
does **not** enter the For You feed of the big account's followers. The "reply guy" distribution
theory is falsified against the current code.

### The one lever that actually exists: mutual follows

**Tier A**, `ranking_scorer.rs` + `param.rs` + `docs/BIDIRECTIONAL_BOOST_CHANGE.md`:

```rust
param!(ReplyWeight, f64, "rust_home_mixer_reply_weight", 5.0);
param!(BidirectionalFollowReplyWeightBoost, f64, "...", 15.0);

fn bidirectional_boost_eligible(candidate: &PostCandidate) -> bool {
    candidate.in_reply_to_tweet_id.is_none()      // NOT a reply
        && candidate.retweeted_tweet_id.is_none() // NOT a repost
        && candidate.is_mutual_follow_author == Some(true)
}
```

When the author is a **mutual follow** and the post is an **original**, the weight on P(reply)
becomes **5.0 + 15.0 = 20.0** — a 4× multiplier on the single highest-weighted positive engagement
prediction. The dated rollout: A/B test began 2026-07-10 at values {5,10,15,20}; broad launch at 20
on 2026-07-13; reduced to 15 on 2026-07-24 after World Cup feedback.

**A reply candidate is explicitly excluded from this boost.** The mechanism rewards *provoking*
replies on your own original posts among people who follow you back — not *writing* replies.

### Quote-posts are treated as original posts, not replies

**Tier A.** Quote-posts carry no `in_reply_to_tweet_id`, so `OONRetweetReplyFilter` does not touch
them and the reply/repost arm of the out-of-network discount does not apply. The prior repo made
this explicit at the query layer: `TweetKindOption(includeOriginalTweetsAndQuotes = true)`. Quoting
is separately rewarded as an engagement to *predict*:

```rust
param!(QuoteWeight, f64, "rust_home_mixer_quote_weight", 5.0);   // == ReplyWeight
param!(QuotedClickWeight, f64, "...", 0.05);
```

**Practical upshot: a quote-post is distributed like an original post; a reply is distributed like
out-of-network content.** For a writer who reacts to other people's posts, that is the single
highest-leverage mechanical fact in this document. The reactive one-liner keeps its full score if
it is a quote-post and loses 25% plus all out-of-network reach if it is a reply.

---

## 4. The published ranking algorithm, in full

**Tier A**, `xai-org/x-algorithm/home-mixer/params/param.rs`, read 2026-09-04. These are stated by
X to be the primary production values.

### Score formula

```
Final Score = Σ (weight_i × P(action_i))
```

then three adjustments: **author diversity** (decaying multiplier per repeated author, floor 0.25),
**out-of-network discount** (0.75, or 0.5 within a topic request), and a **new-author boost**. A
separate `vm-ranker/` service reorders the result afterwards.

### The weights

| Action | Weight | Note |
|---|---:|---|
| Reply | **5.0** | highest single engagement weight |
| Reply, author is a mutual follow, post is an original | **20.0** | `5.0 + 15.0` boost |
| Quote | **5.0** | equal to reply |
| Share via copy link | **20.0** | highest positive weight in the file |
| Share via DM | 5.0 | |
| Share | 2.0 | |
| Repost | 1.0 | |
| Favorite (like) | **0.5** | a like is worth 1/10th of a reply |
| Follow author | 4.0 | |
| Click (post) | 0.4 | |
| **Open link** | **+0.2** | *positive* |
| Video open | 0.07 | |
| Photo expand | 0.05 | |
| Quoted-post click | 0.05 | |
| Dwell | 0.05 | |
| Continuous dwell time | 0.004 | |
| Post unexplored | 0.02 | in-network only by default |
| Video quality view | 0.0 | currently off |
| Profile click | 0.0 | currently off |
| Not dwelled | −0.02 | |
| Block author | −31.2 | |
| Not interested | −43.2 | |
| Mute author | −58.8 | |
| Report | **−234.0** | |

**X's own anti-misreading warning, quoted from the code comments** — this is the correction to the
most-repeated claim about this file:

> "Each weight multiplies the *predicted* probability of that action (P(favorite), P(repost), …) or
> a continuous value e.g. watch time — the weights do not multiply raw engagement counts. One common
> misinterpretation is that you can read these weight ratios as count equivalences, e.g. the
> incorrect statement that 'one report cancels 468 likes' — this is incorrect."

The comment also states that report is weighted heavily because "the baseline probability of a
Report is more than 1000x lower than a Like," and that brigading has limited effect because
predictions are personalised and **"For an account to count in the algorithm's recommendation
system, it must take place on a post served in Home Timeline. Directly navigating to a post (i.e.,
coordinating via groupchat) has no ranking impact."**

### Dwell time: yes, and it is cheap

Dwell is a first-class prediction head — `dwell`, `dwell time`, `click dwell time`, `active
seconds`, plus a negative `not dwelled`. But at 0.05 and 0.004, **dwell weights are two orders of
magnitude below reply and quote.** The old stack had a coarser version (`PredictedTweetDetailDwell`
at 15s, `PredictedProfileDwelled` at 20s). Anyone telling you X optimises primarily for time-on-post
is reading a 2023 press narrative, not the 2026 parameter file.

### Media

Media is present but **weak**: photo expand 0.05, video open 0.07, video quality view 0.0
(disabled), quoted-post video quality view 0.0. There is **no media boost multiplier** in the
scorer. There *is* a media-adjacent diversity penalty — the prior repo carried
`ImpressedMediaClusterBasedListwiseRescoringProvider` and
`ImpressedImageClusterBasedListwiseRescoringProvider`, which discount posts whose media resembles
media you were just shown. **Nothing in either repo rewards attaching an image.**

### Post length

**Tier A, negative finding.** I grepped both repositories for text-length, character-count and
word-count features in the ranking path. **There is no post-length feature in the current scorer at
all.** The only length gate found anywhere is in the *previous* repo's **push-notification** service
(`pushservice/.../PushFeatureSwitchParams.scala`), which defines out-of-network quality thresholds
bounded at 70 characters / 18 words, with all defaults set to `0.0` — a notifications filter, not a
timeline one, and unpublished in its live form. **Length does not affect For You ranking in any
published code.**

### Filters, in the order they run

Pre-scoring: duplicates → hydration failures → **older than 48 hours** → the viewer's own posts →
**out-of-network reposts and replies** → NSFW SimClusters → repeated reposts → subscriber-only →
already seen (×2) → already served → muted keywords → blocked/muted authors → video exclusion →
topic → new-user minimum engagement → inventory holdout.

Post-selection: visibility filtering (`ALLOW` / `INTERSTITIAL` / `DROP`) → ancestor/quote/repost
cascade drop → conversation dedup.

**The 48-hour age filter is worth naming**: no post older than two days is a For You candidate.

### What X admits is withheld

Quoted from the README: Grox LLM prompts (`.j2` files) and "some botmaker rules" are not published.
Everything else material to visibility is claimed to be in the repo, backed by an "Under the Hood"
per-account label transparency tool.

---

## 5. Verdicts on the three standing contract claims

| Contract claim | Verdict |
|---|---|
| **The fold is the first-screen bound** | **Verified in mechanism, falsified in framing.** The fold is real and is a CSS `-webkit-line-clamp` — *rendered lines after layout*, from a shipped set of {1,2,3,4,5,10}, responsive to viewport. It is **not** a character count, and X documents it nowhere. The specific top-level value is **unverifiable without a login**; do not assert a number. |
| **The attached image is part of the first screen** | **Verified as a composition fact, unsupported as a distribution claim.** Media renders inline and costs **0 characters** (Tier A, docs.x.com), so it is free real estate on the reading surface. But nothing in either repo rewards attaching an image: photo expand 0.05, video open 0.07, video quality view 0.0, and no media multiplier. Keep the line; strip any implication that images buy reach. |
| **Links suppress reach** | **Falsified as a statement about the platform today.** No link penalty exists anywhere in the current ranking code; the only link term is `OpenLinkWeight = +0.2`, positive. Musk stated on 2026-07-28 that X has not penalised links "for over a year." It was **not folklore historically** — NDSS 2026 measured 4–8× lower normalised visibility for link posts in 2022–2024 data, and Musk confirmed the practice in 2024 — but the contract states a 2024 fact in the present tense. Rewrite or delete. |

---

## 6. Practical mechanics for a writer of reactive one-liners

Ordered by leverage, each traceable to a Tier A line above.

1. **A quote-post is an original post; a reply is out-of-network content.** Same sentence, same
   target, ~0.75× versus 1.0× score, and the reply is additionally *deleted* from the feed of
   anyone who does not already follow you.
2. **Replying to a large account no longer borrows its audience.** The exemption that made this work
   (`OONReplyFilter`, keep-if-viewer-follows-the-replied-to-account) existed in the 2025 Scala stack
   and is **gone** from the 2026 Rust stack.
3. **Reply and quote are the top-weighted engagements at 5.0 each** — ten times a like (0.5), five
   times a repost (1.0). Writing something people answer or quote is mechanically the goal.
4. **Share-via-copy-link is weighted 20.0**, the highest positive weight in the file. The single
   most valuable reader behaviour is copying your post's link and pasting it elsewhere.
5. **Mutual follows are the only structural boost.** Original posts from mutuals get P(reply)
   weighted at 20.0 instead of 5.0. Replies are explicitly excluded.
6. **Nothing rewards length, and nothing punishes it.** The fold is a *reading* constraint, not a
   ranking one.
7. **48 hours is the whole shelf life.**

---

## 7. Where nobody outside X knows

Stated explicitly, because negative findings were part of the brief.

- **The exact top-level fold value on any client.** Undocumented by X; observable only behind a
  login; `line-clamp-10` is the only candidate in the shipped CSS and I did not see it applied.
- **Whether the published parameter defaults are genuinely live.** X *asserts* the cron-sync; there
  is no external way to verify it, and the previous repo's equivalent file was entirely zeroed.
- **The Phoenix model's learned behaviour.** Weights are published; what the transformer has learned
  to predict from a viewer's action sequence is not inspectable. A link penalty that lives in
  *learned* rather than *coded* behaviour would be invisible in this repo — which is precisely the
  gap the NDSS authors flag, and the reason Musk's "we haven't for over a year" is a claim about
  outcome rather than a verifiable structural fact.
- **Grox prompts and some botmaker rules**, which X states outright are withheld.
- **The old Earlybird light ranker's learned coefficients**, so the sign of its `has_link_flag`
  feature is unknown and always was.

---

## Reproduction

```bash
git clone --depth 1 https://github.com/xai-org/x-algorithm.git      # commit 9b0dc31
git clone --depth 1 https://github.com/twitter/the-algorithm.git    # commit c54bec0d4
gh api repos/xai-org/x-algorithm --jq '{created_at,pushed_at,license:.license.spdx_id}'
```

Fold measurement: load any x.com profile in a browser, then in the console —

```js
[...document.querySelectorAll('*')]
  .filter(e => getComputedStyle(e).webkitLineClamp !== 'none')
  .map(e => getComputedStyle(e).webkitLineClamp)
```

---

## Tier distribution

| Tier | Sources used for claims | Share |
|---|---:|---:|
| **A** — X source repos, X help/dev docs, platform-owner primary post, peer-reviewed measurement, direct instrument measurement | 10 | **83%** |
| **B** — technical/trade journalism reporting the above | 2 | 17% |
| **C** — marketing blogs, agency content, vendor "we analysed N tweets" posts | **0** | **0%** |

Two Tier A sources were located but returned 403 and are **not cited for any number**
(Bandy & Diakopoulos 2021; Axios 2023-10-03). Two Tier C numbers encountered during search —
"94% fewer views" and "30–50% reach reduction visible in the code" — were checked against the
source code and are **contradicted by it**; they appear here only as refuted claims.
