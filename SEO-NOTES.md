# SEO Work Notes — Miami Yacht Collective

Running log so future sessions build on this instead of repeating it. One lesson per entry, summary first.

---

## 2026-10-04 session (Claude, traffic audit and three rounds of fixes — all live)

### Diagnosis: the site is healthy; the domain is new and has no footprint
Domain registered 2026-03-04. Vercel Web Analytics showed 53 to 177 unique visitors a month from June to September, with Google sending only 16 to 25 of them. Brand searches return only our own pages: no TripAdvisor, Yelp or third-party reviews. URLs churned for months (11 pages deleted 12 days after launch, occasion pages re-created under new names in July, blog removed in August). On-site work helps, but reviews, listings and links are the larger lever. No Search Console data was available to me; ask the owner for exports before diagnosing rankings.

### Shipped
- **c6667a8 / a28be9c:** photos recompressed in place (709 MB to 55 MB), `vercel.json` tracked with security headers and redirects for dead URLs, boat pages expanded with unique copy and FAQ, corporate and sandbar pages added.
- **49c890b (speed, guides, boat pages, titles):** 800px WebP card photos on `index.html` and `yacht.html` (23 MB to 4.8 MB), lazy-loading and image dimensions, hero video recompressed and skipped on phones, 7-day media cache. Guides hub plus four guides. "On board" sections and per-photo alt text on boat pages. Every title at 60 characters or fewer. Boat H1s carry a search term. Homepage testimonials and counter digits demoted from `h2` to `div`. Gallery stock images replaced with fleet photos.
- **7e74523 (+ Spanish follow-up):** seven landing pages: boat rental, party boat, bachelor party, proposal and anniversary, Miami Beach, Brickell, and a Spanish page.

### Lessons
- **Titles are now short on purpose.** This reverses the July note that 77 to 91 character titles were deliberate. Keep them at 60 or fewer.
- **Superseded:** the July note "any new content must say max 13 guests" is void. Numeric guest counts are forbidden (see CLAUDE.md).
- **`boat-rental-miami.html` exists despite the July finding that the head term is marketplace-walled.** It was built at the owner's request to cover the long tail ("with captain", small-boat prices). Do not expect it to rank for the head term.
- **No Haulover sales page.** The owner has not confirmed charters go there. The sandbar guide describes Haulover without offering it.
- **Location pages are not pickup pages.** Miami Beach and Brickell pages describe travel to the Miami River dock only.
- **`party-boat-rental-miami.html` overlaps `yacht-party-miami.html`.** It is aimed at smaller boats and the "private, not ticketed" angle, and the two link to each other. Watch Search Console for the two competing on the same queries.
- **Acgua Alberti's page shows Deep Blue's photos.** Its gallery srcs are `photos/deep-blue-90/*`; only `photos/legacy/acgua-alberti.avif` is its own. No "On board" section was written for it.
- **Template stock images on the homepage, About and Gallery were replaced the same day** with fleet photos cropped into `photos/site/`. Still stock: the three background videos on `about.html` (their sections are hidden by the theme) and the `View-Yacht-Showcase` text badge.
- **New pages are generated from `sandbar-yacht-charter-miami.html`** by replacing the head tags, the three JSON-LD blocks and everything between `<section class="myc-hero">` and the footer. The Spanish page's menu and footer were then translated by hand in the file, so regenerating it would lose them.
- **Correction to my own audit:** homepage testimonials are named, not anonymous, and boat-page main copy was about 45% shared before this work, not 50%.

- **Acgua Alberti removed (same day, owner's decision).** Page deleted, `/acgua-alberti` and `/acgua-alberti.html` redirect to `deep-blue.html`, fleet count changed from 10 to 9 on every page, top price is now $4,999, both Stripe links deactivated and its pay pages removed. If the boat comes back with its own photos, restore it from git history (`git show 3a078a0:acgua-alberti.html`) and reverse those counts.

### Open
- Owner: Google reviews, Business Profile posts, TripAdvisor/Yelp/Bing/Apple listings, local links (see OWNER-TODO.md).
- Owner: real specs per boat, more Maxum and 55' Azimut photos (one each today).
- Resubmit `sitemap.xml` in Search Console (35 URLs now) and export queries and page indexing after 3 to 4 weeks.
- "(2026)" in the prices and license titles needs a January 2027 refresh.

---

## 2026-07-09 session (Claude, design overhaul — branch `design-overhaul`)

### What shipped (commit 1210d8f, NOT yet merged to main)
"Midnight & Champagne" premium theme: new `css/myc-theme.css` override layer loaded after the Webflow CSS on all 25 pages (detail_*.html, 401, logo-preview skipped). Midnight navy / warm ivory / champagne gold, Cormorant Garamond display serif + Inter Tight body. NO changes to titles, metas, headings text, alt text, image srcs, hrefs, schema, or URLs — the 2026-07-08 SEO pass is fully preserved.

### Key mechanics for future sessions
- The theme wins over per-page inline `<style>` blocks via specificity prefixes: `html .modal-*` (head styles), `body .myc-*` / `body .home-faq-*` (body styles), and `!important` only where inline `style=""` attributes had to be beaten (`.yacht-page-header`, `.footer-nap-block`, booking/contact pill CTAs targeted by `a[style*="#25D366"]`).
- Fixed pre-existing bug: white nav links were invisible on light pages (all pages use the base transparent header). Header is now permanent navy glass.
- Font loading: webfont.js + WebFont.load (Lato/Aclonica/Inter Tight) replaced sitewide with one `display=swap` css2 link (Cormorant Garamond + Inter Tight). Any NEW page must copy the new head pattern.
- Booking modal upgraded on all pages: role=dialog, aria-modal, focus trap/restore; open() focuses close btn after a 60ms rAF delay (visibility transition race).
- Local QA: expected console 404s remain /videos/* and /_vercel/insights only. Axopar page has a pre-existing Webflow "improperly configured forms" warning (template artifact).

---

## 2026-07-08 session (Claude, autonomous SEO run)

### Lesson: The live site and the local working tree have diverged — trust git, not the filesystem
The owner (or a Next.js experiment) moved `css/`, `js/`, `images/`, `photos/`, `videos/` into an untracked `public/` dir, leaving ~430 uncommitted deletions in the working tree. The live site still serves the committed root-level dirs. Never `git add -A` in this repo; stage files explicitly. I restored `css/ js/ images/` locally via `git checkout --` for verification only.

### Lesson: Owner standardized all guest capacities to "up to 13 guests" (uncommitted edits, likely USCG 12-passenger + captain rule)
index.html/yacht.html/detail pages all edited to 13. `llms.txt` still said 30/20/15 — fixed this session to match. Any new content must say max 13 guests per charter.

### Lesson: Prior session's audit (2026-05-17) already shipped the critical fixes
sitemap.xml, robots.txt, llms.txt, LocalBusiness+Service+Breadcrumb schema, template brand-name cleanup are all live and verified (curl 200s this session). Don't redo. Remaining gaps found this session:
- No FAQ content or FAQPage schema anywhere
- No Open Graph / Twitter Card tags on any page
- services/contact/booking missing meta descriptions; booking has no H1
- yacht.html (the nav "Yachts" fleet page!) was noindexed + robots-blocked as a "template artifact" but is linked 4x from homepage nav — wasted link equity
- yacht.html + detail_*.html linked to yamaha-255xd.html which 404s (boat photos exist in public/photos/yamaha-255xd-25/ but page was never created; no price/capacity facts available, so card removed rather than page invented)
- No dedicated intent pages for "yacht party miami" / "sunset cruise miami" (the two biggest non-brand intents we can win); party photos exist in public/photos/party/
- priceRange "$$$" instead of numeric; no hasOfferCatalog

### Lesson: Facts for content must come from llms.txt + yacht page schemas
Verified facts usable in copy: fleet 28–90 ft, from $899/4hr (Maxum) to $3,000/4hr (Deep Blue), licensed captain + crew included on every charter, departs 668 NW N River Dr on the Miami River (10 min Brickell / 15 min Miami Beach), 24/7, booking via call/WhatsApp (787) 664-5040, areas: Biscayne Bay, Star Island, Fisher Island, Stiltsville, Nixon's Sandbar. DO NOT invent: fuel policy, BYOB policy, cancellation policy, catering details — owner never confirmed these.

### Party photo filenames contain other businesses' names
public/photos/party/ has files like "best-miami-boat-rentals_-aquarius-boat-rental-...jpg" (scraped from Instagram/Pinterest). When using, copy + rename to neutral SEO names (miami-yacht-party-XX.jpg) and skip photos watermarked/branded by competitors.

### Lesson: Occasion pages are how small operators win Miami yacht SERPs (research-backed)
Fresh SERP research (July 2026, 15 searches): "birthday yacht party miami" and "bachelorette yacht miami" are won exclusively by small local operators with DEDICATED landing pages (feelingyachty, primeluxuryrentals, onkor, vistayachts) — zero marketplaces. "miami yacht rental prices" is won by standalone price-guide pages with real numbers and a year in the title. "sunset cruise miami" head term is Viator/$14-ticket territory — only winnable with the "private" modifier. "boat rental miami" is marketplace-walled; don't chase it. Head term "yacht rental miami" is winnable long-term (miamiyachtingcompany holds #1 as a local operator).

### Shipped this session (2026-07-08)
- 6 NEW pages: yacht-party-miami.html, birthday-yacht-party-miami.html, bachelorette-yacht-party-miami.html, private-sunset-cruise-miami.html, miami-yacht-rental-prices.html (2026 price table, all 10 yachts), yamaha-255xd.html (fixes the 404 fleet card)
- services.html REBUILT: was Webflow template junk ("Donut Ride"/"Banana Ride" cards hotlinking another site's CDN) → now the Experiences hub linking all occasion pages
- yacht.html rehabilitated: removed noindex + robots block, real title/meta/canonical, ItemList schema, H1 "Yachts & Boats for Rent in Miami"
- index.html: title → "Yacht Rental Miami | Private Charters from $899…", new meta, 6-question FAQ section + FAQPage schema, LocalBusiness priceRange "$899 - $3,000" + hasOfferCatalog (10 offers), "Yachtlux Club" artifact reworded
- Site-wide: "Experiences" nav link on all pages, footer "Experiences" column (6 links), full OG/Twitter tags on all 22 indexable pages (9 pages had stale duplicate og:description tags from Webflow — removed)
- contact/booking: meta descriptions + intent titles; booking got an H1 (promoted existing h2); gallery H1 aligned to party intent
- sitemap.xml: +7 URLs, lastmod 2026-07-08; robots.txt: yacht.html unblocked; llms.txt: 10 vessels, capacities fixed to 13, experience pages listed

### Lesson: f-string page generation ate a JS brace — always console-check generated pages
Generated pages had `WebFont.load({...})` missing a closing brace (f-string `{{` escaping), which threw "Unexpected token ')'" on every new page. Caught only via Playwright console. Any future template generation: load the page headless and assert zero console errors (excluding local-only 404s for /_vercel/insights and /videos/*).

### Lesson: verify with a fresh-context agent — it caught what self-review missed
The adversarial verifier found: stale duplicate og:description tags (first-tag-wins for WhatsApp/FB previews — the old one advertised "onboard catering", an unverified amenity), the "Yachtlux Club" template artifact, and an implied-champagne phrase. All fixed. It also confirmed: all 25 JSON-LD blocks parse with no duplicate keys, all prices/capacities consistent across text+schema+llms.txt, all links/sitemap/robots/modals clean.

### Open items / caveats for next session
- seo-reference.json is now STALE (predates this pass) — seo_validate.py comparisons against it will fail; regenerate reference before using
- Party photos (photos/party/) are Pinterest/Instagram-sourced third-party images the owner collected. Copyright + authenticity risk. Owner should replace with real charter photos ASAP; keep filenames/dimensions to avoid touching HTML
- Owner's uncommitted "up to 13 guests" edits on index/yacht/detail pages were included in this commit (consistent, intentional). detail_*.html template pages still carry uncommitted edits — left unstaged (robots-blocked artifacts)
- Titles run 77–91 chars (keyword+price front-loaded, brand suffix truncates in SERPs) — deliberate
- Email in schema/llms.txt is still sebastian@mcaiconsulting.com — action plan item 15 (business-domain email) still open
- Off-site work still owned by Sebastian: GBP services/photos/reviews cadence, Yelp/TripAdvisor listings, Bing Places/Apple Business Connect, 305/786 number
- DONE later same day: Google Search Console property https://miamiyachtcollective.com/ added under sebastian@mcaiconsulting.com (auto-verified via existing DNS record) and sitemap.xml resubmitted 2026-07-08 — GSC read it immediately: Status Success, 22 discovered pages. Check Pages report in ~1-2 weeks for indexing coverage of the 6 new pages.
