# Your To-Do List — Miami Yacht Collective

## Information architecture rebuild (2026-10-28) — placeholders that need you

The site was restructured on branch `ia-overhaul-2026-10` (not pushed, not live). Every item below is a `<!-- TODO(owner) -->` placeholder in the code or a decision only you can make. Nothing was invented: where a fact was missing, the page says "ask us" and this list has the gap.

### Decisions
- [ ] **Are the 55' Azimut and the 46' Maxum still in the fleet?** Both pages are live at `/yachts/55-azimut` and `/yachts/46-maxum` with one photo each. Say the word and they come out of the fleet, the menus, the schema and the sitemap in one run.
- [ ] **Approve the three legal drafts** at `/privacy-policy`, `/terms` and `/cancellation-policy`. They are marked "DRAFT – owner to review", are `noindex`, and are not in the sitemap. The bracketed items need your real terms: deposit amount and when the balance is due, accepted payment methods, the cancellation tiers (days and percentages), the weather/rescheduling rule, late-arrival grace period, alcohol policy and minimum age, data retention period, and any other tracking tools you use. Once approved I remove `noindex` and add them to the sitemap.
- [ ] **Which add-ons do you actually offer?** `/add-ons` lists only what is confirmed (jet ski on the Isabella, Jacuzzi on the Deep Blue, L'chaim slide and water toys at extra cost). Candidates to confirm with prices: catering, decorations, photographer, DJ or sound, extra hours, towels and ice. Sub-pages are created only for confirmed services; the page is `noindex` until then.
- [ ] **Branded email address.** The footer, the schema, the legal drafts and `llms.txt` still cite `sebastian@mcaiconsulting.com`. A `@miamiyachtcollective.com` address (for example `book@`) is recommended; give me the address and it changes everywhere in one run.
- [ ] **Reviews.** No reviews page or ratings were created because there is no verified source. Send real guest reviews or your Google Business Profile URL and `/reviews`, a reviews block on the homepage and yacht pages, and the footer link go in. The four homepage testimonials (Ariana Del Toro, Jake Holloway, Sofia Castaneda, Ethan Calloway) predate this work: confirm they are real guests or they should come down.

### Facts missing from the yacht pages (every yacht shows "ask us" until supplied)
- [ ] **6-hour and 8-hour rates** per yacht. Since 2026-11-04 the pricing block shows only the 4-hour price plus "Longer charters available, ask for a quote"; the booking widgets offer "Longer charter — ask for a quote". Send the 6h/8h figures and the tiers go back in.
- [ ] **What is not included**: fuel, gratuity, dockage, water toys. The pages only say the 4-hour rate is the same on every date.
- [ ] **Builder, model, year, cabins and heads** per yacht for the Specifications list (only what the photos show is published; the Isabella, L'chaim and Deep Blue cabin lines come from the existing "On board" copy).
- [ ] **Maximum guests per yacht.** The stat strip says "Based on your needs", the booking widget's guest field is uncapped and the fleet filter has no "guests" option until you supply the numbers (CLAUDE.md still forbids numeric capacities).
- [ ] **A real form handler.** The "Prefer to send your details?" forms on the yacht pages and `/book` compose a WhatsApp message because the site has no backend. If you want email leads, pick a handler (Formspree, a Vercel function, your CRM) and I wire it in.

### Copy you should read once (pre-existing, flagged — not changed)
- [ ] **Homepage "Why book with Miami Yacht Collective" cards** list Air conditioning, Bathroom, Free wifi, Entertainment, Sauna and Bar & lounges. These are template claims, not confirmed amenities ("Sauna" especially). Say which to keep and the rest come out.
- [ ] **Contact page card "On the day"** ends with "Tell us if you'd like catering or extras" — catering is not a confirmed service.
- [ ] **About page** — a team/story section is reserved as a placeholder. Send names, roles, years on the water and a crew photo and it goes in; nothing is published until then.
- [ ] **Social profiles.** Only Instagram is linked. Send Facebook, TikTok, YouTube or Google Business Profile URLs if they exist.

### When you approve the branch and it goes live
- [ ] Resubmit `sitemap.xml` in Google Search Console and Bing Webmaster Tools (51 URLs now, all clean URLs). Run `scripts/indexnow.sh` once.
- [ ] Update the website link on Google Business Profile, Instagram and any marketplace listing if it points at a page other than the homepage (old links keep working through a single 301, but new links should go to the final URL).
- [ ] Share previews refresh on their own; a link shared before the change may show the old card until WhatsApp/iMessage re-fetch it.

Things only you can do, ordered by how much they move traffic and bookings. Updated 2026-10-04 after the traffic audit (see SEO-NOTES.md for what was done on the site).

The site itself is in good shape. What holds traffic back now is that the domain is seven months old and almost nothing outside the site mentions it. The first three items fix that and matter more than any further page edits.

## This week

- [ ] **Preview the October 16 branch before it goes live** (`seo-tourist-2026-10`). 13 new pages, a sticky Call/WhatsApp bar on phones, and prefilled WhatsApp messages. Check a few pages on your phone and tap WhatsApp: the message that opens tells you which page the lead came from.
- [ ] **Export Search Console data** (how-to in the Oct 16 notes in SEO-NOTES.md): Performance report, last 3 months, Export > CSV, and the Pages report under Indexing.
- [ ] **Confirm one thing for the Star Island page:** does the captain point out the celebrity homes as you pass? The page currently says "happy to point things out". If you want "guided commentary", say so.

- [ ] **Ask past guests for Google reviews.** Send each recent guest your Google review link on WhatsApp. Aim for 5 in the next 2 to 3 weeks, then one every week or two.
- [ ] **Update your Google Business Profile.** Add each experience as a service with its page link, and post real charter photos about twice a week.
- [ ] **Finish the marketplace listings.** GetMyBoat is under review and the Sailo drafts need their Insurance section. Details are in `marketplace-listings/STATUS.md`.
- [ ] **Read the new pages once.** They are new copy published in your name: the four guides at `/guides.html`, and the seven landing pages (boat rental, party boat, bachelor party, proposal, Miami Beach, Brickell, and the Spanish page at `/alquiler-de-yates-miami.html`).
- [ ] **Resubmit the sitemap in Search Console** once the branch is live. It will have 48 pages.

## This month

- [ ] **Send more photos of the Maxum and the 55' Azimut.** Each page has only one.
- [ ] **Send real specs for each boat**: make, model, year, cabins, bathrooms and anything notable on board. Boat pages describe only what the photos show until then.
- [ ] **Create TripAdvisor, Yelp, Bing Places and Apple Business Connect listings** with the exact same name, address and phone: Miami Yacht Collective / 668 NW N River Dr / (787) 664-5040.
- [ ] **Get a few local links.** Miami event planners, wedding and bachelorette blogs, hotel concierge pages and the marina. Five to ten would be a large change for a domain this new.
- [ ] **Confirm what is included**: BYOB, fuel, ice, speakers, towels, catering, gratuity, cancellation and late-arrival policy. The site avoids all of these because they were never confirmed. Adding them to the pages and FAQs is a quick follow-up.
- [ ] **Do you run charters to Haulover Sandbar?** If yes, a Haulover page is worth building. Today the sandbar guide only describes it.
- [ ] **Replace the party photos with your own.** The images in `photos/party/` came from Pinterest and Instagram.
- [ ] **Set up a business-domain email** such as book@miamiyachtcollective.com. The site and AI assistants currently cite sebastian@mcaiconsulting.com.

## In 3 to 4 weeks

- [ ] **Export Search Console data**: Performance (queries and pages) and Indexing (pages). It shows which of the new pages Google picked up and which searches to push next.

## Later

- [ ] **Get a 305 or 786 number** as a secondary line on listings. Keep the 787.
- [ ] **Submit to data aggregators** (Data Axle, Foursquare).
- [ ] **Every January:** refresh "(2026)" in the prices and license page titles and re-check rates. Also refresh the event dates on the Art Basel, spring break / Ultra and Grand Prix pages (they are written into the copy, the fact tiles and the FAQ).
- [ ] **Launch the Google Ads campaign** built in `google-ads/` when ready. It is paused and has not been test-imported.

## Housekeeping

- [ ] **Decide the fate of the Next.js experiment** (`app/`, `public/`, the `package.json` changes). Until then, never `git add -A` in this repo.
