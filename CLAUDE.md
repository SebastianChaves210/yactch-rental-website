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
python3 -m http.server 8000
# Open http://localhost:8000
```

## Architecture

### Two Layers (only the static layer is live)

1. **Static HTML (root)** — The actual production site. Each page is a standalone `.html` file with inline CSS for the booking modal, loading the root-level `css/` and `js/` directories.
2. **Next.js app (`app/`, `public/`)** — A dormant experiment. Untracked, not deployed. Ignore unless explicitly asked.

### Asset Locations

Production serves the committed root-level directories. The untracked `public/` copy is not live.

- `css/` — Webflow stylesheets plus `myc-theme.css`, the override layer loaded last on every page
- `js/` — `webflow.js` (Webflow runtime), `tracking.js` (GA4 event tracking)
- `images/` — Template images (backgrounds, icons) in `.avif`/`.svg`. Template stock; no longer shown on the homepage, About or Gallery (replaced 2026-10-04)
- `photos/site/` — Fleet photos cropped to the exact pixel size of the template slots they replaced (homepage about/marquee/testimonial/overview images, About images, and `hero-bay.webp` behind the About and Gallery heroes via `myc-theme.css`)
- `photos/<boat>/` — Real fleet photos. Each photo used on a card or landing page also has a `<name>-800.webp` copy (800px wide); `index.html`, `yacht.html`, the guides and the landing pages point at those, the boat detail galleries use the full-size originals
- `videos/` — Hero and section background videos. Not present in the local working tree by default (`git checkout -- videos/<file>` to restore one)
- `vercel.json` — security headers, 7-day cache for `photos/`, `images/`, `videos/`, and permanent redirects. Every new page needs an extensionless redirect here

### Performance rules

- New photos: resize before committing (Pillow is installed; max 1920px for originals) and generate the `-800.webp` copy for any card or content use.
- Images on `index.html` and `yacht.html` carry `width`/`height` attributes and rely on `:where(img[width][height]) { height: auto; }` in `myc-theme.css`. Do not long-cache `css/` or `js/`: stale CSS with new HTML stretches those images.
- The homepage hero video is injected by an inline script only at 768px and wider. Phones get `videos/Yacht-poster-00001.jpg`.
- Local checks: `python3 -m http.server` plus a browser will serve cached CSS. Force a reload before trusting a layout check.

### Key Pattern: Booking Modal

Every page must include the booking modal markup and JS inline. It's not in an external file — it's copy-pasted into each HTML page's `<head>` (styles) and `<body>` (markup + script).

- CTA buttons use `data-modal` attribute to trigger the modal
- Modal offers: Call (787) 664-5040 or WhatsApp (wa.me/17876645040)
- `js/tracking.js` tracks `modal_open`, `call_click`, `whatsapp_click` via GA4

### SEO Validation

`seo-reference.json` and `seo_validate.py` predate the July 2026 SEO pass and are stale. Do not validate against them without regenerating the reference first. See `SEO-NOTES.md` for the running log of SEO work.

## Pages

| Page | File | Notes |
|------|------|-------|
| Homepage | `index.html` | Hero video (poster only on phones), fleet grid, FAQ, CTA. The H1 holds a `.myc-h1-kicker` span plus the headline |
| Yacht detail pages | `isabella.html`, `maxum.html`, `ferretti.html`, `azimut.html`, `azimut-lchaim.html`, `deep-blue.html`, `anvera.html`, `axopar-brabus.html`, `yamaha-255xd.html` | 9 boats. Photo galleries, spec rows, an "On board" section written from the photos, FAQ, booking CTAs. The 90' Acgua Alberti was removed 2026-10-04 at the owner's request (its page showed Deep Blue's photos); its URLs redirect to `deep-blue.html` and its Stripe links are deactivated. The fleet count is written as "9" or "nine" across the site, and the top price is $4,999 |
| Gallery | `gallery.html` | Fleet photos (template stock replaced 2026-10-04) |
| About | `about.html` | Company info |
| Services | `services.html` | Experiences hub: one card per occasion page, plus links to the guides |
| Contact | `contact.html` | Contact info |
| Booking | `booking.html` | Booking page |
| Fleet listing | `yacht.html` | Indexable fleet page (de-noindexed 2026-07-08) |
| SEO landing pages | `yacht-party-miami.html`, `birthday-yacht-party-miami.html`, `bachelorette-yacht-party-miami.html`, `private-sunset-cruise-miami.html`, `miami-yacht-rental-prices.html`, `corporate-yacht-charter-miami.html`, `sandbar-yacht-charter-miami.html` | Intent pages targeting party/sunset/price searches. Keep facts in sync with llms.txt |
| Search landing pages (2026-10-04) | `boat-rental-miami.html`, `party-boat-rental-miami.html`, `bachelor-party-yacht-miami.html`, `proposal-yacht-charter-miami.html`, `yacht-rental-miami-beach.html`, `yacht-rental-brickell.html`, `alquiler-de-yates-miami.html` (Spanish, `lang="es"`, menu, footer and modal translated by hand in that file) | Same template and fact rules as the occasion pages. Location pages describe the Miami River dock only — never claim pickup elsewhere. Prices repeat here: update on a reprice |
| Guides | `guides.html` (hub), `boating-license-miami-boat-rental.html`, `what-to-bring-yacht-charter-miami.html`, `miami-sandbar-guide.html`, `best-time-yacht-charter-miami.html` | Informational articles (Article + FAQPage schema), generated from the sandbar page template 2026-10-04. Same fact rules as the rest of the site |
| Error pages | `401.html`, `404.html` | Error states |
| Blog | Removed 2026-08-10 | Old `/blog` URLs redirect to the guides in `vercel.json` |

## Do NOT

- Add npm, webpack, or any build step
- Rename any HTML files
- Change any `<title>`, `<meta description>`, heading text (`h1`/`h2`/`h3`), image `alt` text, image `src` paths, or internal link `href` values without explicit instruction (2026-07-08: titles/metas/schema were deliberately optimized in an owner-requested SEO pass — see SEO-NOTES.md before "fixing" them back)
- Break the booking modal flow (Call + WhatsApp must remain on every page)
- Replace existing `.avif` or image references with different paths
- Modify `sitemap.xml` without keeping it in sync with the real page set (new pages must be added)
- State unverified amenities or policies in copy (BYOB, fuel, catering, towels, gratuity, cancellation, pickup anywhere but the dock, trips to Haulover) — owner-confirmed facts are: captain and crew included, Miami River departure at 668 NW N River Dr, per-yacht prices, 24/7 call/WhatsApp booking, and service in Spanish and English (confirmed 2026-10-04)
- Invent boat specs (make, model, year, cabins, engines) — the owner has not supplied them; "On board" copy describes only what the photos show
- Let a `<title>` run past 60 characters (trimmed sitewide 2026-10-04)
- State a NUMERIC guest / passenger capacity anywhere (2026-07-09: owner had ALL "up to 13 guests"/"Max 13"/guest-count copy, the "Guests" table column, capacity fact tiles, "Max Guests" schema, and the guest-count FAQ removed sitewide — do not reintroduce numeric headcount in copy, schema, tables, or alt text. 2026-08-10: the sanctioned replacement is the "Guests: Based on your needs" spec row now on all 10 yacht pages — keep that line, never swap a number back in)
- `git add -A` — the working tree carries intentional uncommitted deletions (assets moved to untracked `public/` for a dormant Next.js experiment); stage files explicitly
- Add payment forms, login, or backend functionality

## Repricing checklist

Prices appear in: the boat detail pages (copy, schema and, since 2026-10-04, the `<title>`), `index.html`, `yacht.html`, `miami-yacht-rental-prices.html`, every occasion and search landing page (tables and FAQ), the guides that quote "from $1,000", `services.html`, `contact.html`, `about.html` and `llms.txt`. Grep for the old figure before calling a reprice done.

## Image Path Gotcha

Production runs on case-sensitive Linux. File names must be lowercase and URL-safe. Past bugs were caused by case mismatches between HTML `src` attributes and actual filenames on disk (macOS is case-insensitive, Linux is not).

## Social

- Instagram: `https://www.instagram.com/miamiyachtcollective/`
