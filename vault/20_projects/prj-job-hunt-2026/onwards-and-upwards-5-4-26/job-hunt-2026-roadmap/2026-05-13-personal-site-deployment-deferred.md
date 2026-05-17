---
type: deferred-issue
project: prj-job-hunt-2026
created: 2026-05-13
status: superseded-by-gap-fill-3
superseded_on: 2026-05-16
unblocks: seanwinslow.com going live, Substack syndication of EXPLANATION.md files via GitHub raw URLs, LinkedIn "view my portfolio" CTA
roadmap: 2026-05-06-unified-roadmap.md
ai-context: "Superseded 2026-05-16 by Council Gap-Fill 3 (un-defers deployment). The 2026-05-13 deferral was correct for the gallery form of /transactions/; the council reframed the surface as a reverse-chronological ledger of shipped AI artifacts, which stands recruiter-ready today with 5 EXPLANATION.md files already on disk. Canonical deploy record lives at the Task 1 Step 3 expanded scope in 2026-05-06-unified-roadmap.md (ship target Mon 2026-05-19). This doc remains as historical context + retains the original step-by-step deploy mechanics, two of which were updated by the gap-fill: host is now Vercel (consistency with agent-fleet-observability), not Cloudflare Pages; Cloudflare DNS records for Vercel are set to DNS-only / orange-cloud OFF."
---

# Personal Site Deployment — SUPERSEDED 2026-05-16 by Council Gap-Fill 3

> **STATUS:** Superseded 2026-05-16. Deployment is no longer deferred. Canonical deploy record is the **Task 1 Step 3 expanded scope** in [`2026-05-06-unified-roadmap.md`](2026-05-06-unified-roadmap.md) (ship target **Mon 2026-05-19**). Two deploy choices changed from this doc's original recommendation: (1) **host = Vercel**, not Cloudflare Pages — for consistency with the [`agent-fleet-observability`](../../../../agent-fleet-observability/) deploy already on Vercel; (2) **Cloudflare DNS records set to DNS-only / orange-cloud OFF** for the Vercel apex + www records, so Vercel's edge handles SSL without proxy interference. Steps 1–6 below are retained as historical reference + the residual mechanics still apply (build verification, custom-domain attach, optional repo push). Triggers + acceptance criteria are obsolete (superseded by the Gap-Fill 3 verification gate).
>
> **Original TL;DR (preserved for context):** [sw-portfolio](https://github.com/seanwinslow28/sw-portfolio) is built, pushed to GitHub, and has a working `/transactions/` route. It is **not deployed** to any host. **seanwinslow.com** is owned (Cloudflare + Namecheap) but points at nothing live. Sean deferred deployment 2026-05-13 because the site itself isn't recruiter-ready yet. This doc holds the full fix for when it is.

## Why deferred

Sean's call, 2026-05-13: *"The site isn't ready yet, so I'd like to defer this for when it's ready to ship."*

Deploying a half-finished portfolio to `seanwinslow.com` creates two problems:

1. **Recruiter risk** — if anyone clicks through from LinkedIn or a Substack post during the 8-week sprint, they see in-progress work, not the artifact Sean is being judged against.
2. **Indexing risk** — Google starts crawling the half-finished site. Hard to course-correct first impressions in search results.

Better to ship once, when the design + content + 4Q artifact set are at the bar Sean wants.

## Domain ownership (confirmed 2026-05-13)

- Sean owns **seanwinslow.com** via **Cloudflare** and **Namecheap**
- Likely arrangement (to be confirmed at deploy time): registered at Namecheap, DNS managed via Cloudflare
- No DNS records currently point at any hosted instance of the site

## Current state of the repo (as of 2026-05-13)

| Piece | State |
|---|---|
| Local `~/Code-Brain/sw-portfolio/` ↔ GitHub | ✅ In sync. Remote = [github.com/seanwinslow28/sw-portfolio](https://github.com/seanwinslow28/sw-portfolio). Last commit on `main` = `08731f9` from 2026-05-08. |
| Build stack | ✅ Astro 5 + React 19 islands + Tailwind v4 + GSAP + Lenis. `output: 'static'`, `npm run build` → `dist/`. |
| `/transactions/` route | ✅ Shipped 2026-05-08 (commit `f13a103`). Uses Astro content collections + `TransactionCard.astro` component. Two entries: Phase D + Phase 6. |
| Hosting config in repo | ❌ No `vercel.json`, `netlify.toml`, `wrangler.toml`, `_redirects`, `CNAME`, or `.github/workflows/` |
| `site:` field in [astro.config.mjs](../../../../../sw-portfolio/astro.config.mjs) | ❌ Missing — needed for canonical URLs / sitemap / og:url |
| Custom domain | ❌ `seanwinslow.com` not yet pointed at any host |

## The full fix — execute in this order when ready to ship

### Step 1: Decide host

Sean owns the Cloudflare side of the domain stack already. **Recommended: Cloudflare Pages.** Reasons:
- DNS is already on Cloudflare → zero-config custom domain attach
- Free tier covers a static portfolio comfortably (unlimited bandwidth, 500 builds/month)
- Same dashboard Sean is already in for the domain

Alternatives, in order of fastest path-to-live:
- **Vercel** — best Astro DX, free hobby tier, push-to-deploy on `main`. ~3-min setup. Worth picking if Cloudflare Pages hits a snag with Tailwind v4 + GSAP + Astro 5.
- **Netlify** — equivalent posture to Vercel.
- **GitHub Pages** — free but requires writing a `.github/workflows/deploy.yml` action because Astro needs a build step. Slower setup, more friction.

### Step 2: Set production URL in [astro.config.mjs](../../../../../sw-portfolio/astro.config.mjs)

Add `site: 'https://seanwinslow.com'` to the `defineConfig({...})` block. Tiny change, but Astro needs it before deploy or the sitemap, canonical tags, and og:url all generate wrong:

```diff
 export default defineConfig({
+  site: 'https://seanwinslow.com',
   integrations: [react()],
   vite: { plugins: [tailwindcss()] },
   output: 'static',
   build: { format: 'directory' },
 });
```

Commit with `chore(astro): set production site URL for canonical / sitemap`. Push to `main`.

### Step 3: Verify the build runs clean locally first

```bash
cd ~/Code-Brain/sw-portfolio
npm run build
# Expect: dist/ generated, no errors, content collection routes hydrated
ls dist/transactions/
# Expect: index.html + per-slug subdirs for both transactions content entries
```

If the build fails, fix it before connecting to a host. Common Astro-5-with-content-collections gotchas: missing `src/content/config.ts` (it exists — verified 2026-05-13), Tailwind v4 + Vite plugin order, React 19 peer-dep warnings.

### Step 4: Wire the GitHub repo to Cloudflare Pages

In Cloudflare dashboard:

1. Workers & Pages → Create application → Pages → Connect to Git
2. Pick `seanwinslow28/sw-portfolio`
3. Production branch: `main`
4. Framework preset: **Astro** (auto-detected)
5. Build command: `npm run build`
6. Build output directory: `dist`
7. Environment variables: none needed for static build
8. Deploy

First build runs in ~90 seconds. You get a `sw-portfolio-XXXX.pages.dev` URL. Verify the site loads there, navigate to `/transactions/`, confirm both Phase D and Phase 6 entries render.

### Step 5: Attach `seanwinslow.com` as custom domain

In the Cloudflare Pages project:

1. Custom domains → Set up a custom domain → `seanwinslow.com`
2. (Optional but recommended) Also add `www.seanwinslow.com` with a redirect rule to apex
3. Cloudflare auto-handles DNS if the domain is already on Cloudflare DNS (which it is per Sean's confirmation 2026-05-13)
4. SSL/TLS handshake takes a few minutes, then the site is live at `https://seanwinslow.com`

If Namecheap is acting as registrar but Cloudflare is doing DNS (likely setup), no Namecheap action needed — Cloudflare handles the routing. If DNS is somehow split, point Namecheap nameservers at Cloudflare's first.

### Step 6: Optional — push the superuser-pack EXPLANATION commit if not already pushed

Status as of 2026-05-13: commit `3909881` (Phase D + Phase 6 EXPLANATION.md files) is **pushed** to [github.com/seanwinslow28/CLAUDE-CODE-SUPERUSER-PACK](https://github.com/seanwinslow28/CLAUDE-CODE-SUPERUSER-PACK).

This matters for the **Substack syndication fallback** (unified roadmap Decision 2): if the personal site is delayed past 2026-05-13, GitHub `EXPLANATION.md` files become canonical and Substack posts syndicate from GitHub raw URLs. Today the personal site doesn't link out to those URLs (the transactions content is inlined in the Astro content collection), but the URLs need to exist publicly anyway for the Decision-2 fallback.

If a future session sees this commit hasn't been pushed yet, push it.

## Acceptance criteria for "deployment is done"

- [ ] `https://seanwinslow.com` resolves and serves the portfolio (200 OK, no certificate warnings)
- [ ] `https://seanwinslow.com/transactions/` lists both Phase D + Phase 6 artifacts
- [ ] `https://seanwinslow.com/transactions/phase-d-typed-edges/` renders the full deep-dive page
- [ ] `https://seanwinslow.com/transactions/knowledge-loop-phase-6/` renders the full deep-dive page
- [ ] Sitemap (`/sitemap-index.xml` or `/sitemap.xml`) has correct `seanwinslow.com` URLs (not `localhost:4321`)
- [ ] `https://www.seanwinslow.com` redirects to apex (or vice versa — pick one and be consistent)
- [ ] LinkedIn / Substack profile bio updates to point to `seanwinslow.com` (one-time update, not repo work)
- [ ] First push to `main` after deploy triggers a Cloudflare Pages auto-deploy (verify the loop works)

## Triggers to un-defer

This issue moves from "deferred" to "active" when **any** of these fire:

1. Sean says "the site is ready" / "let's ship it" / "go live with seanwinslow.com"
2. Sean publishes anywhere with a `seanwinslow.com` link (LinkedIn headline, Substack profile, resume) — the site MUST be live before that link goes public
3. Substack post is being prepared that would link to a `seanwinslow.com/transactions/...` URL
4. A recruiter / hiring manager asks for a portfolio URL (anti-pattern — Sean should have shipped before pitching, but if it happens, deploy same-day)

## What NOT to do while deferred

- Do NOT auto-deploy on push (no `.github/workflows/`, no `vercel.json`, no `wrangler.toml` checked in)
- Do NOT add `site: 'https://seanwinslow.com'` to `astro.config.mjs` until ready to deploy (it generates absolute URLs in og:url and canonical, which would 404 if anyone scrapes them before the site is live)
- Do NOT point any DNS records at any host
- Do NOT publish a Substack post or LinkedIn update referencing `seanwinslow.com` until the site is live there

## Related

- [2026-05-06-unified-roadmap.md](2026-05-06-unified-roadmap.md) — parent roadmap, Decision 2 explains the Substack-from-GitHub-raw fallback
- [2026-05-13-claude-code-handoff-task-1-2.md](2026-05-13-claude-code-handoff-task-1-2.md) — the handoff that surfaced this gap during execution
- Local repo: `~/Code-Brain/sw-portfolio/`
- GitHub repo: https://github.com/seanwinslow28/sw-portfolio
- Domain registrar / DNS: Cloudflare + Namecheap (combined; exact arrangement to be confirmed at deploy time)
