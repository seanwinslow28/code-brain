---
title: "Tier-1 rights audit — Wiley and Cambridge titles"
date: 2026-09-10
project: productcraft
status: complete
tags: [research, productcraft, ebooks, rights, drm, licensing]
---

# Tier-1 rights audit: Wiley and Cambridge titles

**Scope:** Current U.S. lawful acquisition and licensing routes for private agent ingestion of *Testing Business Ideas*, *Trustworthy Online Controlled Experiments*, *Monetizing Innovation*, and *EMPOWERED*. No purchase or outreach was performed.

**Accessed:** 2026-09-10 (America/New_York). Store availability and platform terms can change; re-verify immediately before purchase or licensing.

## Executive summary

None of these four titles is presently a verified, turnkey source for private agent ingestion. The strongest lawful routes are:

- **Cambridge:** lawful Cambridge Core access plus the noncommercial text-and-data-mining (TDM) rights in the Core terms. This can support local indexing, but the title is not currently sold digitally on the U.S. Core page and Core does not authorize automated harvesting.
- **Wiley:** request written permission and a deliverable file from Wiley. Wiley-direct e-books are read through Wiley Reader or VitalSource and are not supplied as downloadable PDF/EPUB files. Wiley also states that public or free availability does not itself authorize AI use.
- **Amazon:** all four Kindle listings exist, but Amazon does not expose the title-level DRM/download flag on the public product pages. Under Amazon's 2026 policy, only a verified purchaser can see whether that purchased Kindle edition is eligible for EPUB/PDF download in **Manage Your Content and Devices**. A purchase test would answer the file-format question, not the separate copyright/licensing question.

| Title | Outcome | Why |
|---|---|---|
| *Testing Business Ideas* | **outreach-needed** | Wiley hosts an unencrypted 368-page PDF labelled “Excerpt 1,” apparently containing the complete book, but Wiley expressly says public/free availability does not imply authorization for AI development, training, or implementation. Written scope confirmation is needed before agent ingestion. |
| *Trustworthy Online Controlled Experiments* | **outreach-needed** | Cambridge's terms contain a useful noncommercial TDM permission for lawfully accessed content, but the U.S. title page currently says the digital edition is unavailable. Confirm access and delivery with Cambridge or an institution before building the corpus. |
| *Monetizing Innovation* | **outreach-needed** | Wiley-direct access is app-bound; the public Wiley PDF is only a 12-page excerpt. No full, licensed export was found. |
| *EMPOWERED* | **outreach-needed** | Wiley-direct access is app-bound; the public Wiley PDF is only a 7-page excerpt. No full, licensed export was found. |

`outreach-needed` means there is a plausible lawful route, but written permission, entitlement, or content delivery must be resolved before ingestion. No purchase or contact was made.

## Platform findings that apply across titles

### Amazon Kindle after the January 2026 change

Amazon's KDP help page says that, effective 20 January 2026, verified purchasers may download EPUB and PDF files only for books whose publisher has chosen DRM-free distribution. Books with DRM remain unavailable for EPUB/PDF download. For pre-9 December 2025 DRM-free titles, the publisher must affirmatively reconfirm the setting before downloads are enabled. Borrowers are excluded. The public storefront does not provide a dependable title-level flag for this setting; the conclusive check is the purchaser's **Manage Your Content and Devices** page after purchase. ([Amazon KDP DRM options](https://kdp.amazon.com/en_US/help/topic/GDDXGH9VR22ACM8U), accessed 2026-09-10.)

Accordingly, “Kindle edition available” is not evidence of a standalone file. Even a successful EPUB/PDF download would establish technical possession only; it would not by itself grant permission to create a shared corpus, train a model, or upload the work to a third-party AI service.

### Wiley Reader and VitalSource

Wiley's own e-book specification says purchased e-books are viewed in Wiley Reader or VitalSource, depending on the title, and explicitly states: **“E-Books are not available as a downloadable PDF or ePub.”** Offline use means downloading into the relevant reader app, not exporting an unrestricted source file. Wiley also describes one simultaneous online session and reader-device limits. ([Wiley e-books](https://www.wiley.com/en-us/shop/wiley-ebooks/), accessed 2026-09-10.)

Wiley's AI principles reserve AI-related rights, require authorization before Wiley content is used for AI development, training, or implementation, and say that public/free-to-read availability does not create implied permission. ([Wiley AI principles](https://www.wiley.com/en-us/about-us/ai/principles), accessed 2026-09-10.)

Wiley does offer an institutional TDM route for academic subscribers' noncommercial research through its API and a click-through TDM agreement; corporate subscribers are told to work through their account manager. Wiley prohibits crawling, and directs users without a subscription or needing another format to `TDM@wiley.com`. The public program is framed around subscribed **Wiley Online Library** content. Exact-title searches did not establish that these three trade books are included, so the institutional TDM program must not be assumed to cover them. ([Wiley TDM service](https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining), accessed 2026-09-10.)

For an individual or small team, Wiley's general route is RightsLink on the title page; where RightsLink does not cover the use, submit a request to Wiley Permissions. Wiley lists `permissions@wiley.com`, and its general-permissions page says noncommercial requests may sometimes be granted without a fee. ([Wiley general permissions](https://www.wiley.com/en-us/solutions-partnerships/permissions/general-queries/); [Wiley author permissions help](https://authors.wiley.com/help/license-signing-and-permissions.html), accessed 2026-09-10.)

### Cambridge Core

Cambridge Core's terms permit a user with lawful access to access, download, store, and print content for research, teaching, and private study. The TDM clause additionally permits downloading, extracting, storing, and indexing lawfully accessed content for a **noncommercial** purpose, and loading/integrating it for analysis. Local copies must be deleted when the project ends. The same terms prohibit unauthorized-user access, circumvention, and excessive downloading; Cambridge identifies more than 500 PDFs per hour as excessive. ([Cambridge Core terms of use](https://www.cambridge.org/core/legal-notices/terms), last updated March 2025; accessed 2026-09-10.)

Cambridge's TDM guidance says no extra licence is required for qualifying noncommercial TDM where the user already has lawful access, but bots and automated downloading are not allowed. It invites requests for programmatic access, large-scale work, or particular formats—including full-text XML—at `openresearch@cambridge.org`. This is the best route for confirming whether a private agent workflow is within scope, especially if any third-party hosted service would receive the files. ([Cambridge TDM guidance](https://www.cambridge.org/core/services/open-research-policies/text-and-data-mining), accessed 2026-09-10.)

## Title audits

### 1. *Testing Business Ideas: A Field Guide for Rapid Experimentation*

**Outcome: outreach-needed**

- **Amazon:** The Kindle edition is sold by John Wiley & Sons at [Amazon ASIN B07ZZM9FDT](https://www.amazon.com/dp/B07ZZM9FDT) and identifies e-text ISBN 9781119551423. The public page inspected while signed out did not disclose DRM status or EPUB/PDF download eligibility. Under Amazon's policy, that is only conclusively knowable after purchase in Manage Your Content and Devices.
- **Publisher-direct:** The [Wiley title page](https://www.wiley.com/en-us/Testing+Business+Ideas%3A+A+Field+Guide+for+Rapid+Experimentation-p-9781119551423) routes the e-book through Wiley's reader ecosystem. [VitalSource's edition](https://www.vitalsource.com/products/testing-business-ideas-david-j-bland-alexander-v9781119551423) is fixed-layout with a lifetime licence and offline access in Bookshelf; neither description establishes an exportable PDF/EPUB.
- **Exceptional public PDF finding:** Wiley's own catalogue server exposes [`9781119551447.excerpt.pdf`](https://catalogimages.wiley.com/images/db/pdf/9781119551447.excerpt.pdf). Direct inspection on 2026-09-10 found a 368-page, 32.1 MB, unencrypted PDF whose text runs through the book's index, so it appears materially complete despite the filename/label “Excerpt 1.” Its copyright page reserves reproduction and retrieval-system rights and points users to Wiley/CCC for permission. Because Wiley's AI principles reject implied AI permission from public availability, the file is **technically ingestible but not verified as licensed for this agent use**.
- **Institutional/TDM:** Wiley's general subscriber TDM route may be relevant, but this trade title was not verified as Wiley Online Library subscribed content. Do not crawl the catalogue PDF or treat the WOL TDM agreement as automatically covering it.
- **Permissions route:** Use RightsLink from the Wiley title page or `permissions@wiley.com`; copy `TDM@wiley.com` if requesting a machine-readable delivery format or TDM-specific terms.
- **Best lawful next action:** Send Wiley the exact PDF URL and request written confirmation that one named individual/small team may store and index it in a secure, local/private retrieval system for internal decision support, with no model training, redistribution, or third-party file access. Ask Wiley to specify retention, user-count, output-quotation, and hosted-model limits. Do not purchase the Wiley e-book expecting a portable file.

### 2. *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*

**Outcome: outreach-needed**

- **Amazon:** The Cambridge eTextbook is listed at [Amazon ASIN B0845Y3DJV](https://www.amazon.com/dp/B0845Y3DJV), ISBN 9781108590099. The public page did not expose DRM or EPUB/PDF download eligibility. Only a post-purchase Manage Your Content check can settle Amazon's file-download flag.
- **Publisher-direct:** The [Cambridge Core book page](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59) lists DOI 10.1017/9781108653985 and chapter-level content, but the U.S. page showed the digital edition as **Unavailable** on 2026-09-10. Cambridge explains that purchased Core books are read online and downloaded as **chapter-level PDFs**; it does not send a single full-book PDF. ([Cambridge Core e-commerce explanation](https://www.cambridge.org/core/blog/2023/05/31/expansion-and-improvement-of-cambridge-core-ecommerce-service/); [individual access help](https://corehelp.cambridge.org/hc/en-gb/articles/17013970242962-How-can-I-access-content-as-an-individual?article=17013970242962), accessed 2026-09-10.)
- **Institutional/TDM:** If a library or employer already provides lawful Core access, the Core terms' noncommercial TDM clause is the most concrete route found: chapter PDFs may be manually downloaded, stored, and indexed for the qualifying project. Mere institutional access does not authorize automated/systematic harvesting, sharing the files with unauthorized users, commercial use, or keeping the corpus indefinitely. Cambridge may supply XML or other formats on request.
- **Permissions route:** Write `openresearch@cambridge.org` for TDM, delivery-format, and hosted-agent questions. The Core terms list `directcs@cambridge.org` for questions about the terms.
- **Best lawful next action:** First check whether the user already has institutional Core access to this DOI. If yes, ask Cambridge to confirm that the planned private agent/RAG environment is noncommercial and within the terms—especially whether any hosted AI provider counts as an unauthorized third party—and request full-text XML or an approved bulk-delivery method. If no access exists, ask Cambridge how an individual/small team can lawfully acquire the digital title now that direct sale shows unavailable. Do not infer systematic-download permission merely from visible chapter buttons.

### 3. *Monetizing Innovation: How Smart Companies Design the Product Around the Price*

**Outcome: outreach-needed**

- **Amazon:** The Wiley Kindle edition is at [Amazon ASIN B01F4DYY1I](https://www.amazon.com/dp/B01F4DYY1I), ISBN 9781119240884. The public listing did not reveal DRM or standalone-download eligibility; only a post-purchase Manage Your Content check can do so.
- **Publisher-direct:** The [Wiley title page](https://www.wiley.com/en-us/Monetizing+Innovation%3A+How+Smart+Companies+Design+the+Product+Around+the+Price-p-9781119240860) is subject to Wiley's app-bound e-book policy. The [VitalSource edition](https://www.vitalsource.com/products/monetizing-innovation-how-smart-companies-design-madhavan-ramanujam-georg-v9781119240884) is reflowable, licensed for lifetime use, and available offline in Bookshelf; this is not evidence of an exported file. Wiley's official [`9781119240860.excerpt.pdf`](https://catalogimages.wiley.com/images/db/pdf/9781119240860.excerpt.pdf) is an unencrypted 12-page excerpt, not a full-book source.
- **Institutional/TDM:** The general Wiley subscriber TDM route exists, but this title was not verified as included WOL content. The 12-page excerpt can be used as a limited public reference subject to its copyright notice; it cannot substitute for the full work.
- **Permissions route:** RightsLink on the title page, then `permissions@wiley.com`; include `TDM@wiley.com` for format/API questions.
- **Best lawful next action:** Ask Wiley for a small-team licence covering secure local retrieval/indexing, no training or redistribution, and for an authorized PDF/XML/EPUB delivery. A Kindle purchase test is optional only if the team first decides that Amazon's export status is worth testing; it would not eliminate the need to resolve agent-use rights.

### 4. *EMPOWERED: Ordinary People, Extraordinary Products*

**Outcome: outreach-needed**

- **Amazon:** The Wiley Kindle edition is at [Amazon ASIN B08LPKRD5L](https://www.amazon.com/dp/B08LPKRD5L), ISBN 9781119691327. The public listing did not reveal DRM or EPUB/PDF download eligibility; only a post-purchase Manage Your Content check can settle it.
- **Publisher-direct:** The [Wiley title page](https://www.wiley.com/en-us/Empowered%3A+Ordinary+People%2C+Extraordinary+Products-p-9781119691327) is governed by Wiley's app-bound e-book policy. The [VitalSource edition](https://www.vitalsource.com/products/empowered-marty-cagan-v9781119691327) is reflowable, lifetime-licensed, and available offline in Bookshelf, not documented as an exportable source file. Wiley's official [`9781119691297.excerpt.pdf`](https://catalogimages.wiley.com/images/db/pdf/9781119691297.excerpt.pdf) is an unencrypted 7-page Chapter 1 excerpt only.
- **Institutional/TDM:** As above, Wiley's WOL TDM pathway cannot be presumed to include this trade book. The public excerpt is useful for only very narrow grounding.
- **Permissions route:** RightsLink on the title page, then `permissions@wiley.com`; include `TDM@wiley.com` for a requested machine-readable delivery.
- **Best lawful next action:** Ask Wiley for a written small-team permission and an authorized file, defining secure local indexing, named users, no training, no redistribution, third-party-hosting limits, retention, and allowed output quotation. Do not purchase Wiley/VitalSource access expecting a portable source file.

## Recommended outreach specification

For each publisher, describe the proposed use narrowly and concretely:

1. One individual or a named small team.
2. Secure, private retrieval/indexing for internal decision support.
3. No foundation-model training or fine-tuning.
4. No public distribution, resale, or substitute reading product.
5. Whether processing is wholly local or uses a named hosted model/API, including its retention settings.
6. Requested source format (PDF, EPUB, or XML), permitted retention period, user count, and allowed quotation in agent outputs.

Written approval should identify both the **use right** and the **delivery format**. A reader-app licence, a downloadable file, or a noncommercial TDM clause answers only part of that question.

## Source register

All sources below were accessed 2026-09-10 unless another date is stated:

- [Amazon KDP — Digital Rights Management](https://kdp.amazon.com/en_US/help/topic/GDDXGH9VR22ACM8U)
- [Wiley e-books](https://www.wiley.com/en-us/shop/wiley-ebooks/)
- [Wiley AI principles](https://www.wiley.com/en-us/about-us/ai/principles)
- [Wiley Online Library — Text and data mining](https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining)
- [Wiley general permissions](https://www.wiley.com/en-us/solutions-partnerships/permissions/general-queries/)
- [Wiley author permissions help](https://authors.wiley.com/help/license-signing-and-permissions.html)
- [Cambridge Core terms of use](https://www.cambridge.org/core/legal-notices/terms) (terms last updated March 2025)
- [Cambridge text and data mining guidance](https://www.cambridge.org/core/services/open-research-policies/text-and-data-mining)
- [Cambridge Core e-commerce explanation](https://www.cambridge.org/core/blog/2023/05/31/expansion-and-improvement-of-cambridge-core-ecommerce-service/)
- [Cambridge Core individual access help](https://corehelp.cambridge.org/hc/en-gb/articles/17013970242962-How-can-I-access-content-as-an-individual?article=17013970242962)
- Per-title Amazon, publisher, VitalSource, and publisher-hosted PDF URLs are linked in the title sections above.
