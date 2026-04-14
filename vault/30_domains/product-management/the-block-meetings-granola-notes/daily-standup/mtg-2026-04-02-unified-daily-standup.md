---
granola_id: dc43a0b7-b5bf-4256-b744-8a4cb4ff6d56
granola_type: note
type: meeting
domain:
  - product-management
status: active
ai-context: Daily standup covering unified daily standup.
context: the-block
created: 2026-04-02
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
  - bvadimovich@theblock.co
  - ysmagulov@theblock.co
  - akryvanosau@theblock.co
  - sho@theblock.co
  - koliva@theblock.co
  - ramuald.vishneuski@ventionteams.com
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Unified Daily Standup-transcript.md]]"
---

### Twitter / X API & Authentication Issues

- Campus Twitter account has no subscription; main account downgraded to basic plan (only 2 apps allowed)
	- Previously had ~$100/month pro subscription used for one integration + crypto IQ auth
	- Pro plan now costs ~$4,500/month — not viable
- Nikita flagged: crypto IQ app may need to be abandoned to free up the second app slot for campus sign-in
	- Proposal: hide crypto IQ pages on frontend + update Twitter app redirects to campus flow
	- No concrete crypto IQ roadmap exists; decision deferred (“cross that bridge when we get to it”)
- Alternative path: set up pay-as-you-go on the campus account for authentication
	- Estimated cost: ~$200/month additional (comparable to current spend)
- Twitter accounts primarily managed by Davis and team; Caesar and Nikita have access but won’t change plans unilaterally

### Sponsored Courses & Payment Flow

- iOS auth integration on campus likely deploying today (Mike)
- Payment flow update (Nikita + Rama) targeting today; Vicky needs to submit tax info first
- Certificate link for Rise 360 course completion: certs are generated async on backend — no static link available
	- Resolution: David should redirect to a static completion page instead; URL to be confirmed with Nikita

### Standup Updates

- Alex: Twitter identification work blocked on redirect issue; reached out to Nikita for help; reviewing Maria’s requests in the meantime
- Anna: Election hub ticket comments done; Twitter sharing ticket nearly complete (only preview remaining, Maria helping)
- Badan: Fix for invalid URL on prices/ETF/stock pages — working solution, needs more testing before review
- Caesar: Investigating overpayment on RDS (Postgres version related); also scoping Terraform Cloud replication with DynamoDB, Atlantis, and GitHub Actions
- Maria: Fixes for money tracker and reports card page; prices table change column issue fixed; dynamic slugs ticket marked “won’t fix” (effort not worth the result)
- Marina: Sticky banner bug reproduced and fixed; also fixing Brave browser issue; summing up election page events
- Mike: iOS auth, payment updates, minor Simon AI fixes (MCP-related)
- Nikita/Mhulis: Sponsor courses access provisioning; layout still being finalized
- Rama: Payment flow work with Nikita; release today or tomorrow
- Brian: Minor ticket triage; flagged site under load (Caesar’s report) — potential outage risk
- Kristoff: Thesis deadline this week; LMS task targeting Friday

### Action Items

- Nikita
	- Investigate Twitter subscription status and share findings in group DM/channel
	- Check pay-as-you-go option on campus Twitter account for authentication
	- Confirm static completion page URL for David’s Rise 360 course redirect
- Sean
	- Tell David to build a static completion page (not use certificate link)
	- Share updated Poly Market course with Ed and others for review
	- Check in with Matt on crypto IQ forward strategy
- Maria
	- Add J4 event tracking for “Stand with Crypto” clicks (all interactions/redirects)
- Brian
	- Investigate site-under-load report from Caesar
- Badan
	- Finish testing invalid URL fix; send to Brian for review when ready
- Caesar
	- Continue Terraform Cloud / DynamoDB / Atlantis scoping
	- Share Twitter subscription findings in group DM

Chat with meeting transcript: https://notes.granola.ai/t/31399c22-346d-49fd-89a7-67b72ba52e18
