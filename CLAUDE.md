# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Miami Yacht Collective** — A static yacht rental lead-generation website for Miami.
- **Domain**: `https://miamiyachtcollective.com`
- **Goal**: Convert visitors into booking leads via Call or WhatsApp. No backend, no forms, no payment processing.
- **Origin**: Migrated from a Webflow "YachtLux" template. Domain registered 2026-03-04.
- **Deploy**: Vercel project `yactch-rental-website` builds from `main` of `github.com/SebastianChaves210/yactch-rental-website` (local remote `deploy`). Work on `design-overhaul`, then `git push deploy design-overhaul:main`. The `origin` remote is stale.
- **Stack**: Pure HTML/CSS/JS — no build tools, no frameworks. The `package.json` and `app/` directory contain an unused Next.js setup; the live site is the root HTML files served statically.

## Dev Server

```bash
python3 seo-tools/devserver.py        # http://localhost:8000 — behaves like Vercel (cleanUrls, trailingSlash:false, vercel.json redirects, 404.html)
```

`python3 -m http.server` no longer works for this site: pages are served at clean URLs (`/yachts/48-isabella` → `yachts/48-isabella.html`) and the old URLs rely on `vercel.json` redirects. Acceptance checks: `python3 seo_validate.py --base http://localhost:8000` and `python3 -I seo-tools/check_ui.py`.

## Architecture

### Two Layers (only the static layer is live)

1. **Static HTML** — The actual production site. Pages live at the root (`index.html`, `about.html`, `prices.html`, `book.html`, `faq.html`…) and in section folders (`yachts/`, `experiences/`, `destinations/`, `events/`, `guides/`, each with an `index.html` hub). `vercel.json` has `cleanUrls: true` + `trailingSlash: false`, so `yachts/48-isabella.html` is served at `/yachts/48-isabella` and every asset path is root-absolute (`/css/…`, `/photos/…`). Each page still carries the booking modal inline; the header, footer and sticky bar are rendered by `seo-tools/chrome.py`.
2. **Next.js app (`app/`, `public/`)** — A dormant experiment. Untracked, not deployed. Ignore unless explicitly asked.

### Asset Locations

Production serves the committed root-level directories. The untracked `public/` copy is not live.

- `css/` — Webflow stylesheets plus `myc-theme.css`, the override layer loaded last on every page
- `js/` — `webflow.js` (Webflow runtime), `tracking.js` (GA4 event tracking)
- `images/` — Template images (backgrounds, icons) in `.avif`/`.svg`. Template stock; no longer shown on the homepage, About or Gallery (replaced 2026-10-04)
- `photos/site/` — Fleet photos cropped to the exact pixel size of the template slots they replaced (homepage about/marquee/testimonial/overview images, About images, and `hero-bay.webp` behind the About and Gallery heroes via `myc-theme.css`)
- `photos/<boat>/` — Real fleet photos. Each photo used on a card or landing page also has a `<name>-800.webp` copy (800px wide); `index.html`, `yacht.html`, the guides and the landing pages point at those, the boat detail galleries use the full-size originals
- `videos/` — Hero and section background videos. Not present in the local working tree by default (`git checkout -- videos/<file>` to restore one)
- `vercel.json` — security headers, 7-day cache for `photos/`, `images/`, `videos/`, `cleanUrls`/`trailingSlash` and 124 `statusCode: 301` redirects (every old `.html` URL and old slug → its final URL, no chains). It is **generated** by `python3 seo-tools/ia_migrate.py --write` from the `PAGES` map in `seo-tools/ia.py`; add a page there, never by hand

### Performance rules

- New photos: resize before committing (Pillow is installed; max 1920px for originals) and generate the `-800.webp` copy for any card or content use.
- Images on `index.html` and `yacht.html` carry `width`/`height` attributes and rely on `:where(img[width][height]) { height: auto; }` in `myc-theme.css`. Do not long-cache `css/` or `js/`: stale CSS with new HTML stretches those images.
- The homepage hero video is injected by an inline script only at 768px and wider. Phones get `videos/Yacht-poster-00001.webp` (the `.jpg` original is kept in git).
- Google Fonts load non-blocking on every page (`rel="preload" as="style"` + `onload` swap, with a `<noscript>` fallback). Keep that pattern on new pages.
- The header logo is `images/main-boat-logo-420.webp` (420px, 20 KB); the 512px PNG stays for schema and is the source art for the icons and share cards.
- Local checks: `python3 -m http.server` plus a browser will serve cached CSS. Force a reload before trusting a layout check.

### Information architecture (2026-10-28)

- **URL map and data:** `seo-tools/ia.py` — `PAGES` (old slug → final URL, file, section, language), `FLEET` (length, price, photos, amenities, occasions, similar yachts), `DESCRIPTIONS` (every meta description, ≤155 chars), `WA` (per-page WhatsApp prefill), `rewrite_links()` (old hrefs/assets → final form).
- **Chrome:** `seo-tools/chrome.py` renders the skip link, header (Yachts/Experiences/Destinations dropdowns, Prices, Guides, About, Contact, EN·ES·PT switcher, call icon, "Book a Yacht" → page-specific WhatsApp link), footer (brand/NAP, Fleet, Experiences & Destinations, Company, legal + language + Instagram bottom bar), sticky mobile bar, booking modal, fleet cards and the document shell. ES/PT labels live in its `T` dict. Behaviour is in `js/myc-site.js` (dropdowns with hover/keyboard/touch, full-screen mobile menu, lightbox, WhatsApp booking forms, fleet filters); styles are section 20 of `css/myc-theme.css`, maintained in `seo-tools/ia_block.css` and re-applied by `ia_migrate.py`.
- **Generated pages:** `python3 seo-tools/build_site.py [yachts|fleet|destinations|events|faq|addons|legal|book|404]` rebuilds the 9 yacht pages (copy from `seo-tools/fleet_content.json` + `FLEET`), `/yachts`, `/destinations`, `/events`, `/faq`, `/add-ons`, the three legal drafts, `/book` and `404.html`. Edit the data, not the HTML.
- **Migrated pages:** everything else (home, about, contact, gallery, the landing pages, guides, ES/PT) was transformed in place by `seo-tools/ia_migrate.py`. Re-running `ia_migrate.py --write` is idempotent: it refreshes the header/footer/sticky/modal on every migrated page, re-applies the per-page patches, regenerates `vercel.json`, `robots.txt`, `llms.txt`, `sitemap.xml` and the theme CSS block. Run it after any change to `chrome.py`, `ia.py` or `ia_block.css`, then `build_site.py` for the generated pages.
- **Adding a page:** add it to `PAGES` in `ia.py` (+ `DESCRIPTIONS`, `WA`, a `make_og.py` card keyed by the page basename), build or write it at its final path, run `ia_migrate.py --write`, then `seo_validate.py`.
- **Yacht template facts:** 6h/8h tiers render "Ask for quote", guests stay "Based on your needs", builder/model/cabins are omitted, and the fallback form composes a WhatsApp message — each is an owner TODO (see OWNER-TODO.md). Do not fill them in without the owner.
- `seo-tools/sitewide.py` is retired. `generate_pages.py` writes legacy-format pages from `seo-tools/landing-legacy-template.html` and must be followed by `ia_migrate.py --write`.

### Icons and link previews (2026-10-19)

- **Icons:** gold yacht mark on midnight navy. `seo-tools/make_icons.py` builds `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` and overwrites the old Webflow `images/favicon.png` / `images/webclip.png` with the same art. `site.webmanifest` lists the 192/512 icons
- **Share cards:** every page's `og:image`/`twitter:image` points at a branded 1200x630 card in `photos/og/<page>.jpg` (navy panel, gold kicker, Cormorant headline, facts line, wordmark). Built by `seo-tools/make_og.py` from its `PAGES` map (photo, kicker, headline, facts); fonts are in `seo-tools/fonts/`. Keep cards under ~250 KB (WhatsApp drops larger thumbnails) and landscape (portrait and AVIF previews break). Facts on the cards repeat prices: include `photos/og/` in a reprice
- **Head tags:** `seo-tools/head_polish.py` (idempotent) applies the icon block, manifest, `theme-color`, the card URL, `og:image:width/height/alt`, `twitter:image:alt` and `og:locale` to every page. Cards are keyed by the page **basename** (`yachts/48-isabella.html` → `photos/og/48-isabella.jpg`, `yachts/index.html` → `yachts.jpg`). A new page needs a `PAGES` entry in `make_og.py`, then run `make_og.py <slug>` and `head_polish.py`. The `pay/` pages keep their Stripe crops (`photos/stripe/*-og.jpg`); their head comes from `stripe-payment-links/build-pay-pages.mjs`, which carries the same icon block

### Key Pattern: Booking Modal

Every page must include the booking modal markup and JS inline. It's not in an external file — it's copy-pasted into each HTML page's `<head>` (styles) and `<body>` (markup + script).

- In-page CTA buttons use the `data-modal` attribute to trigger the modal; since 2026-10-28 their `href` is the page's WhatsApp URL (no-JS fallback, never `#`). The header "Book a Yacht" and the booking widgets go straight to WhatsApp; the header call icon uses `tel:+17876645040` (all `tel:` links are now the `+1` form)
- Modal offers: Call (787) 664-5040 or WhatsApp (wa.me/17876645040); the modal markup is rendered by `chrome.modal()` and refreshed by `ia_migrate.py`
- `js/tracking.js` tracks `modal_open`, `call_click`, `whatsapp_click` via GA4 with a `cta_location` param (`modal`, `sticky`, `header`, `footer`, `widget`, `card`, `inline`); `[data-modal]` links are excluded from `whatsapp_click`
- **Sticky mobile bar:** rendered by `chrome.sticky()` on every page (Call + WhatsApp; on yacht pages "from $X · 4h · Book now"), shown only under 768px; labels translated on the Spanish and Portuguese pages
- **Prefilled WhatsApp text:** every `wa.me/17876645040` link carries `?text=` with a page-specific message. The map is `WA` in `seo-tools/ia.py` (+ `seo-tools/wa_new_pages.json`); new pages need an entry

### SEO Validation

`python3 seo_validate.py --base http://localhost:8000` (dev server running) is the acceptance suite: one H1, unique title ≤60 and description ≤155, self canonical, OG/Twitter, lang, JSON-LD validity and BreadcrumbList, alt text, final-URL-only internal links, heading order, phone numbers, competitor names, crawl + orphan check, sitemap hygiene, and (with `--base`) every old sitemap URL = 200 or exactly one 301. `python3 -I seo-tools/check_ui.py` covers keyboard/touch behaviour of the header, mobile menu, lightbox and booking widget. `seo-reference.json` is stale and unused. See `SEO-NOTES.md` for the running log.

## Pages

| Page | URL → file | Notes |
|------|------|-------|
| Homepage | `/` → `index.html` | Hero video (poster only on phones), fleet grid, FAQ, CTA. The H1 holds a `.myc-h1-kicker` span plus the headline. Keeps jQuery/webflow.js for its interactions |
| Fleet hub | `/yachts` → `yachts/index.html` | Generated (`build_site.py fleet`): filterable cards (size, budget, feature), at-a-glance table, how to choose, FAQ, ItemList schema |
| Yacht detail pages | `/yachts/90-deep-blue`, `/yachts/75-ferretti`, `/yachts/65-azimut-lchaim`, `/yachts/62-anvera`, `/yachts/55-azimut`, `/yachts/48-isabella`, `/yachts/46-maxum`, `/yachts/28-axopar-brabus`, `/yachts/25-yamaha-255xd` → `yachts/<slug>.html` | 9 boats, generated (`build_site.py yachts`) from `FLEET` + `fleet_content.json`: stat strip, lightbox gallery, pricing tiers, specs `<dl>`, included + amenities (from the photos only), sample itinerary, occasion chips, FAQ, WhatsApp booking widget, similar yachts, sticky price bar. The 90' Acgua Alberti was removed 2026-10-04; its URLs redirect to the Deep Blue. Fleet count "9"/"nine" sitewide, top price $4,999 |
| Experiences hub | `/experiences` → `experiences/index.html` | Migrated `services.html`: one card per occasion page, recommended yachts, destinations + events links, guides, FAQ |
| Experience pages | `/experiences/<slug>` for birthday, bachelorette, bachelor, quinceañera, yacht-party, party-boat-rental, proposal, wedding, private-sunset-cruise, corporate, family, yacht-photoshoot, yacht-charter-before-cruise | Migrated landing pages (keyword slugs kept). Each has a recommended-yachts card block after its boat table and a `.myc-related` block with ≥2 experiences + 1 guide. Prices repeat here: update on a reprice |
| Destinations | `/destinations` (generated hub) + `/destinations/<slug>` for sandbar-yacht-charter-miami, star-island-boat-tour-miami, yacht-rental-miami-beach, south-beach-yacht-rental, yacht-rental-brickell | Location pages describe the Miami River dock only — never claim pickup elsewhere |
| Events | `/events` (generated hub) + `/events/<slug>` for art-basel, new-years-eve, spring-break, miami-grand-prix | Dates in copy, fact tiles and FAQ (Art Basel Dec 4-6 2026; Ultra Mar 26-28 2027 / Music Week Mar 22-28 2027; Grand Prix "early May") need a yearly refresh |
| Guides | `/guides` → `guides/index.html` + `/guides/<slug>` for the four guides | Article + FAQPage schema; each links ≥2 yachts and ≥2 experiences |
| Prices | `/prices` → `prices.html` | Migrated `miami-yacht-rental-prices.html` |
| Boat rentals | `/boat-rental-miami` | Head-term landing page kept at the root |
| Book | `/book` → `book.html` | Generated: yacht/date/guests/duration → WhatsApp, call, how booking works, form fallback |
| FAQ | `/faq` → `faq.html` | Generated hub of the existing FAQ answers, grouped, FAQPage schema |
| Add-ons | `/add-ons` → `add-ons.html` | Generated, `noindex` until the owner confirms the add-on list |
| Legal drafts | `/privacy-policy`, `/terms`, `/cancellation-policy` | Generated templates marked "DRAFT – owner to review", `noindex`, not in the sitemap |
| About, Contact, Gallery | `/about`, `/contact`, `/gallery` | Migrated Webflow pages (keep jQuery/webflow.js). About has a "How booking works" block and a team/story placeholder |
| Spanish / Portuguese | `/alquiler-de-yates-miami`, `/fiesta-en-yate-miami` (es), `/aluguel-de-iate-em-miami` (pt-BR) | Kept at their keyword slugs; chrome rendered in their language; hreflang pairs only where a true translation exists |
| Error pages | `404.html` (generated, links to `/yachts`, `/experiences`, `/contact`), `401.html` (untouched template page) | Share card `photos/og/404.jpg` |
| Template artifacts | `detail_*.html`, `search.html`, `logo-preview.html`, `utility/` | Robots-blocked and 301-redirected in both spellings; left untouched |
| Blog | Removed 2026-08-10 | Old `/blog` URLs redirect to the guides |

## Do NOT

- Add npm, webpack, or any build step
- Move or rename a page without updating `PAGES` in `seo-tools/ia.py` and re-running `ia_migrate.py --write` (every old URL must keep a single 301 to a 200; no redirect chains)
- Link to a `.html` URL, a trailing-slash URL or a relative asset path anywhere: internal links use the final clean URL and assets are root-absolute (`seo_validate.py` fails otherwise)
- Change any `<title>`, `<meta description>`, heading text (`h1`/`h2`/`h3`), image `alt` text, image `src` paths, or internal link `href` values without explicit instruction (2026-07-08: titles/metas/schema were deliberately optimized in an owner-requested SEO pass; 2026-10-28: descriptions were shortened to ≤155 chars and live in `DESCRIPTIONS` — see SEO-NOTES.md before "fixing" them back)
- Break the booking modal flow (Call + WhatsApp must remain on every page)
- Replace existing `.avif` or image references with different paths
- Edit `sitemap.xml`, `vercel.json` redirects, `robots.txt` or the header/footer HTML by hand: they are generated by `seo-tools/ia_migrate.py --write` (sitemap = final 200 URLs only, no `noindex` pages, `xhtml:link` hreflang for the en/es/pt-BR clusters)
- State unverified amenities or policies in copy (BYOB, fuel, catering, towels, gratuity, cancellation, pickup anywhere but the dock, trips to Haulover) — owner-confirmed facts are: captain and crew included, Miami River departure at 668 NW N River Dr, per-yacht prices, 24/7 call/WhatsApp booking, and service in Spanish and English (confirmed 2026-10-04). Confirmed 2026-10-16: every charter is 4 hours (no 2- or 3-hour option), prices are identical on holidays and event weeks (NYE, Art Basel, Ultra, F1), nobody on the team speaks Portuguese (the Portuguese page says service is in English and Spanish), commercial photo and video shoots are allowed, children are welcome and children's life jackets are on board, and wedding ceremonies may be held on board. Still unconfirmed: whether the captain narrates the Star Island route (the page says "happy to point things out", not "guided tour")
- Invent boat specs (make, model, year, cabins, engines) — the owner has not supplied them; "On board" copy describes only what the photos show
- Let a `<title>` run past 60 characters (trimmed sitewide 2026-10-04)
- State a NUMERIC guest / passenger capacity anywhere (2026-07-09: owner had ALL "up to 13 guests"/"Max 13"/guest-count copy, the "Guests" table column, capacity fact tiles, "Max Guests" schema, and the guest-count FAQ removed sitewide — do not reintroduce numeric headcount in copy, schema, tables, or alt text. 2026-08-10: the sanctioned replacement is the "Guests: Based on your needs" spec row now on all 10 yacht pages — keep that line, never swap a number back in)
- `git add -A` — the working tree carries intentional uncommitted deletions (assets moved to untracked `public/` for a dormant Next.js experiment); stage files explicitly
- Add payment forms, login, or backend functionality

## Repricing checklist

Prices appear in: `FLEET` in `seo-tools/ia.py` (drives the header dropdown, footer, cards, yacht pages, hubs and `/book`), `seo-tools/fleet_content.json` (yacht copy, FAQ, titles), `DESCRIPTIONS` in `ia.py`, `index.html`, `prices.html`, every experience/destination/event page (tables and FAQ), the guides that quote "from $1,000", `experiences/index.html`, `contact.html`, `about.html`, `faq.html`, `llms.txt`, the share cards (`make_og.py` facts) and `stripe-payment-links/catalog.json`. After editing the data run `build_site.py` and `ia_migrate.py --write`, then grep for the old figure before calling a reprice done.

## Image Path Gotcha

Production runs on case-sensitive Linux. File names must be lowercase and URL-safe. Past bugs were caused by case mismatches between HTML `src` attributes and actual filenames on disk (macOS is case-insensitive, Linux is not).

## Social

- Instagram: `https://www.instagram.com/miamiyachtcollective/`
