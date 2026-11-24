# -*- coding: utf-8 -*-
"""Build the generated pages of the 2026-10 information architecture.

    python3 seo-tools/build_site.py            # writes every generated page
    python3 seo-tools/build_site.py yachts faq  # only some groups

Groups: yachts (9 detail pages), fleet (/yachts hub), destinations, events, faq, addons, legal, book, 404.
Content comes from seo-tools/fleet_content.json (copy extracted from the previous yacht pages) and
seo-tools/ia.py. Facts are owner-confirmed only; unknowns are <!-- TODO(owner) --> comments.
"""
import html as H
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ia
from ia import (FLEET, FLEET_BY_OLD, PAGES, SITE, REPO, TEL, PHONE_DISPLAY, wa_for, wa_url, url_of, abs_url, price_str,
                section_crumb, rewrite_links, og_card)
import chrome
from chrome import (esc, shell, jsonld, org_jsonld, breadcrumb_jsonld, breadcrumb_html, cards, card, cta_band, ICON_WA, ICON_PHONE)

CONTENT = json.loads((Path(__file__).parent / "fleet_content.json").read_text(encoding="utf-8"))
ONLY = set(sys.argv[1:])
DOCK = "668 NW N River Dr, Miami River"
DOCK_LONG = "668 NW N River Dr on the Miami River, about 10 minutes from Brickell and 15 minutes from Miami Beach"


def want(group):
    return not ONLY or group in ONLY


def write(old, doc):
    path = REPO / PAGES[old]["file"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rewrite_links(doc), encoding="utf-8")
    print("wrote", PAGES[old]["file"])


def check_lengths(title, desc):
    t = H.unescape(title)
    assert len(t) <= 60, f"title too long ({len(t)}): {t}"
    assert len(desc) <= 155, f"description too long ({len(desc)}): {desc}"


def thumb(src):
    """800px WebP copy next to the original (CLAUDE.md convention). Created on demand with Pillow."""
    p = Path(src)
    if p.name.endswith("-800.webp"):
        return src, None
    out = p.with_name(p.stem + "-800.webp")
    full = REPO / out
    if not full.exists():
        from PIL import Image
        with Image.open(REPO / src) as im:
            im = im.convert("RGB")
            if im.width > 800:
                im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
            im.save(full, "WEBP", quality=80, method=6)
    return str(out).replace("\\", "/"), None


def dims(src):
    from PIL import Image
    with Image.open(REPO / src) as im:
        return im.size


def faq_block(faq, heading="Frequently asked questions"):
    items = "\n".join(f'<div class="myc-faq-item">\n<h3>{esc(q)}</h3>\n<p>{a}</p>\n</div>' for q, a in faq)
    return f'<h2>{heading}</h2>\n{items}'


def faq_jsonld(faq):
    return jsonld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": H.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": H.unescape(re.sub(r"<[^>]+>", "", a))}} for q, a in faq]})


def itemlist_jsonld(name, items):
    return jsonld({"@context": "https://schema.org", "@type": "ItemList", "name": name, "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": H.unescape(n), "url": u} for i, (n, u) in enumerate(items)]})


def hero(old, h1, lede, facts, cta_label="Check availability", lang="en", kicker=None):
    trail = section_crumb(old)
    f = "\n".join(f'<div class="myc-fact"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in facts)
    k = f'<span class="myc-kicker" style="color:var(--myc-gold)">{kicker}</span>' if kicker else ""
    return f'''<section class="myc-hero">
        <div class="w-layout-blockcontainer container-default w-container">
          {breadcrumb_html(trail, lang)}
          {k}<h1>{h1}</h1>
          <p class="myc-lede">{lede}</p>
          <div class="myc-facts">
{f}
          </div>
          <div style="margin:26px 0 10px;"><a href="{wa_for(old)}" class="yacht-details-button w-button" data-modal>{cta_label}</a></div>
        </div>
      </section>'''


# =============================================================================== yacht pages
def yacht_page(b):
    old = b["old"]
    c = CONTENT[old]
    name = b["name"]
    short = b["short"]
    price = price_str(b)
    wa = wa_for(old)
    trail = section_crumb(old)
    gallery = c["gallery"]
    n = len(gallery)
    # Lede: the boat's own blurb plus what is on board (from FLEET amenities). The old fleet_content "summary"
    # was the same "Experience luxury aboard … perfect for unforgettable Miami charters" sentence on every page.
    blurb = b["blurb"] if b["blurb"].endswith(".") else b["blurb"] + "."
    first_two = [a[0].lower() + a[1:] for a in b["amenities"][:2]]
    lede = f"{blurb} On board: {' and '.join(first_two)}."
    if old == "yamaha-255xd":
        lede = "The smallest, quickest boat in the fleet: a 25-foot jet boat built for speed, spray and sandbar time, with your captain included."

    # --- gallery: first 5 photos in the grid (800px copies), every photo in the lightbox
    grid = []
    for i, g in enumerate(gallery[:5]):
        t, _ = thumb(g["src"])
        tw, th = dims(t)
        grid.append(f'<a href="/{g["src"]}" data-full data-alt="{esc(g["alt"])}"><img src="/{t}" width="{tw}" height="{th}" alt="{esc(g["alt"])}" loading="{"eager" if i == 0 else "lazy"}"{" fetchpriority=\"high\"" if i == 0 else ""} decoding="async"></a>')
    rest = "\n".join(f'<li><a href="/{g["src"]}" data-full data-alt="{esc(g["alt"])}">{esc(g["alt"])}</a></li>' for g in gallery[5:])
    more_btn = f'<button type="button" class="myc-gal-more" data-lightbox-open>View all {n} photos</button>' if n > 1 else ""
    gal_html = f'''<section class="myc-ygallery" aria-label="Photo gallery">
        <div class="myc-wrap">
          <div class="myc-gal{" is-single" if n == 1 else ""}" data-lightbox data-lightbox-label="{esc(name)} photos">
{chr(10).join(grid)}
            {more_btn}
          </div>
          {"<ul class=\"myc-gal-rest\" hidden>" + rest + "</ul>" if rest else ""}
        </div>
      </section>'''

    # --- stats
    crew_txt = "Captain + 2 crew" if b["crew"] == 2 else "Captain + 1 crew"
    stats = [("Length", f"{b['length']} ft"), ("Guests", "Based on your needs"), ("From", f"{price} <span style=\"font-size:.8em;color:var(--myc-mist)\">/ 4 h</span>"),
             ("Crew", f"{crew_txt} included"), ("Departs", "Miami River dock")]
    stats_html = "\n".join(f'<li><span class="k">{k}</span><span class="v">{v}</span></li>' for k, v in stats)
    # TODO(owner): maximum guest count per yacht is not published; the "Guests" stat stays "Based on your needs" until supplied

    # --- intro copy (existing) + occasions + extras
    intro = c["intro_html"]
    onboard = c.get("onboard_html") or ""
    amen = "\n".join(f"<li>{esc(a)}</li>" for a in b["amenities"])
    included = [
        "The whole yacht, private to your group — no tickets, no strangers",
        "Licensed captain",
        f"{'Two' if b['crew'] == 2 else 'One'} professional crew",
        "4 hours on the water, departing the Miami River dock",
        "Children's life jackets on board",
        "Booking and service in English and Spanish",
    ]
    if old == "isabella":
        included.insert(1, "Jet ski included in the charter")
    if old == "deep-blue":
        included.insert(1, "Onboard Jacuzzi")
    inc_html = "\n".join(f"<li>{esc(i)}</li>" for i in included)
    extra_note = ""
    if old == "azimut-lchaim":
        extra_note = " The inflatable slide and water toys shown in the gallery are available at an additional cost."

    # --- specs
    specs = [("Length", f"{b['length']} ft"), ("Type", b["type"]), ("Guests", "Based on your needs"),
             ("Crew", f"Licensed captain + {b['crew']} crew")]
    if b.get("cabins"):
        specs.append(("Cabins", b["cabins"]))
    specs += [("Departure", f'<a href="{ia.MAPS_URL}" target="_blank" rel="noopener">{DOCK}</a>'), ("Minimum charter", "4 hours"),
              ("Booking", f'<a href="{TEL}">{PHONE_DISPLAY}</a> or WhatsApp, 24/7')]
    specs_html = "\n".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in specs)

    # --- itinerary
    stop = b["stop"]
    if old in ("yamaha-255xd", "axopar-brabus"):
        cruise = "Run the bay at speed past Star Island and Fisher Island — the ride itself is half the point on this boat."
    else:
        cruise = "Loop Star Island, Palm and Hibiscus Islands and run down past Fisher Island with the skyline behind you."
    itinerary = [
        ("0:00", "Board on the Miami River", f"Meet your captain and crew at {DOCK_LONG}. Welcome aboard, a short safety briefing, music on."),
        ("0:15", "Down the river into the bay", "Under the bridges and past the Brickell towers into Biscayne Bay. The skyline opens up behind you."),
        ("1:00", "The islands loop", cruise),
        ("1:45", "Anchor and swim", stop + " Nixon's Sandbar off Key Biscayne is the classic stop; your captain picks the spot for the day's wind and tide."),
        ("3:15", "The slow ride home", "Back along the skyline with the city lighting up. Book the late slot and this leg is your sunset cruise."),
        ("4:00", "Back at the dock", "Four hours on the water, door to door from the Miami River."),
    ]
    it_html = "\n".join(f'<li><span class="t">{t}</span><strong>{h}</strong><p>{p}</p></li>' for t, h, p in itinerary)

    # --- occasions
    occ = "\n".join(f'<li><a href="{url_of(s)}">{esc(PAGES[s]["label"])}</a></li>' for s in b["occasions"])

    # --- similar
    sim = cards(b["similar"], heading="h3")

    # --- schema
    faq = c["faq"]
    service = {
        "@context": "https://schema.org", "@type": "Service", "@id": abs_url(old) + "#service",
        "name": c["service_name"], "serviceType": "Private yacht charter", "description": c["service_desc"], "url": abs_url(old),
        "image": [SITE + "/" + g["src"] for g in gallery[:6]],
        "provider": {"@type": "LocalBusiness", "@id": SITE + "/#business"},
        "areaServed": [{"@type": "City", "name": "Miami"}, {"@type": "City", "name": "Miami Beach"}, {"@type": "Place", "name": "Biscayne Bay"}],
        "availableChannel": {"@type": "ServiceChannel", "servicePhone": {"@type": "ContactPoint", "telephone": "+1-787-664-5040", "contactType": "reservations"}, "serviceUrl": abs_url(old)},
        "offers": {"@type": "Offer", "name": f"4-hour {name} charter", "price": str(b["price"]), "priceCurrency": "USD",
                   "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(b["price"]), "priceCurrency": "USD", "unitText": "4 hours",
                                          "referenceQuantity": {"@type": "QuantitativeValue", "value": 4, "unitCode": "HUR"}},
                   "availability": "https://schema.org/InStock", "url": abs_url(old), "seller": {"@id": SITE + "/#business"}},
        "additionalProperty": [{"@type": "PropertyValue", "name": "Length", "value": f"{b['length']} feet"},
                               {"@type": "PropertyValue", "name": "Yacht type", "value": b["type"]},
                               {"@type": "PropertyValue", "name": "Crew", "value": f"Licensed captain + {b['crew']} crew"},
                               {"@type": "PropertyValue", "name": "Departure", "value": "668 NW N River Dr, Miami, FL 33136"}],
    }
    # the first gallery photo is the page's hero image: preload it so it is not queued behind the CSS
    first_thumb, _ = thumb(gallery[0]["src"])
    preload = f'<link rel="preload" as="image" href="/{first_thumb}" fetchpriority="high">'
    head_extra = "\n".join([preload, jsonld(service), breadcrumb_jsonld(trail), faq_jsonld(faq), org_jsonld()])

    wa_tpl = f"Hi! I'd like to book the {name} on {{date}} for {{guests}} guests, {{duration}}. Is it available?"
    wa_tpl2 = f"Hi! I'm {{name}}. I'd like to book the {name} on {{date}} for {{guests}} guests. Email: {{email}}. Phone: {{phone}}. {{message}}"
    body = f'''
      <section class="myc-yhero">
        <div class="myc-wrap">
          {breadcrumb_html(trail)}
          <h1>{c["h1"]}</h1>
          <p class="myc-lede">{esc(lede)}</p>
          <ul class="myc-stats">
{stats_html}
          </ul>
          <div class="myc-btn-row">
            <a class="myc-btn myc-btn-gold" href="{wa}" target="_blank" rel="noopener">{ICON_WA}Book on WhatsApp</a>
            <a class="myc-btn myc-btn-ghost" href="{TEL}">{ICON_PHONE}Call {PHONE_DISPLAY}</a>
          </div>
        </div>
      </section>
      {gal_html}
      <div class="myc-wrap myc-ybody">
        <div class="myc-ymain">
          <section id="overview">
            <h2>{esc(c["intro_title"])}</h2>
{intro}
          </section>
          <section id="pricing">
            <h2>Pricing</h2>
            <div class="myc-tiers is-single">
              <div class="myc-tier is-main"><span class="d">4 hours</span><span class="p">{price}</span><span class="n">Private charter, captain and crew included</span></div>
            </div>
            <p class="myc-tier-more">Longer charters available, ask for a quote.</p>
            <!-- TODO(owner): only the 4-hour rate exists today; add 6-hour / 8-hour tiers here once the rates are confirmed -->
            <h3>What the price includes</h3>
            <ul class="myc-check">
{inc_html}
            </ul>
            <p class="myc-note">The rate is the same on every date of the year, including holidays and event weeks.{extra_note} Confirm the all-in total for your date when you book.</p>
            <!-- TODO(owner): list what is not included (fuel, gratuity, dockage, water toys) once confirmed -->
          </section>
          <section id="specifications">
            <h2>Specifications</h2>
            <dl class="myc-specs">
{specs_html}
            </dl>
            <!-- TODO(owner): builder, model, year, cabins and heads for the {esc(name)} are not published yet; add them here when supplied -->
          </section>
          <section id="on-board">
            <h2>{esc(c.get("onboard_title") or f"On board the {short}")}</h2>
{onboard}
            <h3>Amenities and water toys</h3>
            <ul class="myc-check">
{amen}
            </ul>
          </section>
          <section id="itinerary">
            <h2>A sample 4-hour charter on the {esc(short)}</h2>
            <p>Every charter is private, so this is a starting point rather than a schedule. Tell your captain what matters most — the swim stop, the skyline, the sunset — and the day bends around it.</p>
            <ol class="myc-timeline">
{it_html}
            </ol>
          </section>
          <section id="occasions">
            <h2>Popular occasions on the {esc(short)}</h2>
            <ul class="myc-chips">
{occ}
              <li><a href="{url_of("services")}">All experiences <span aria-hidden="true">&rarr;</span></a></li>
            </ul>
          </section>
          <section id="faq">
            {faq_block(faq)}
          </section>
        </div>
        <aside class="myc-yaside" aria-label="Book the {esc(name)}">
          <div class="myc-widget">
            <div class="myc-widget-head"><span class="price">{price}</span><span class="per">/ 4 hours</span></div>
            <p class="inc">Licensed captain and crew included &middot; departs the Miami River</p>
            <form data-wa-form data-wa-template="{esc(wa_tpl)}">
              <label for="w-date">Date</label>
              <input type="date" id="w-date" name="date" required data-min-today>
              <div class="myc-grid2">
                <div><label for="w-guests">Guests</label><input type="number" id="w-guests" name="guests" min="1" inputmode="numeric" placeholder="8" required></div>
                <div><label for="w-duration">Duration</label>
                  <select id="w-duration" name="duration">
                    <option value="4 hours">4 hours — {price}</option>
                    <option value="longer than 4 hours (please quote)">Longer charter — ask for a quote</option>
                  </select>
                </div>
              </div>
              <input type="hidden" name="yacht" value="{esc(name)}">
              <button type="submit" class="myc-btn myc-btn-wa">{ICON_WA}Book on WhatsApp</button>
            </form>
            <a class="myc-btn myc-btn-ink" href="{TEL}">{ICON_PHONE}Call {PHONE_DISPLAY}</a>
            <p class="myc-widget-note">We answer 24/7 and confirm most charters in under 10 minutes. No platform fees, no broker markup.</p>
            <!-- TODO(owner): the maximum guest count for the {esc(name)} is not published, so the guests field is not capped -->
            <details class="myc-fallback">
              <summary>Prefer to send your details?</summary>
              <!-- TODO(owner): there is no form handler on this site; this form composes a WhatsApp message until one is connected -->
              <form data-wa-form data-wa-template="{esc(wa_tpl2)}">
                <label for="f-name">Name</label><input type="text" id="f-name" name="name" autocomplete="name" required>
                <label for="f-email">Email</label><input type="email" id="f-email" name="email" autocomplete="email" required>
                <label for="f-phone">Phone</label><input type="tel" id="f-phone" name="phone" autocomplete="tel" required>
                <div class="myc-grid2">
                  <div><label for="f-date">Date</label><input type="date" id="f-date" name="date" required data-min-today></div>
                  <div><label for="f-guests">Guests</label><input type="number" id="f-guests" name="guests" min="1" required></div>
                </div>
                <label for="f-message">Message</label><textarea id="f-message" name="message" rows="3" placeholder="Occasion, start time, anything we should know"></textarea>
                <label class="myc-hp" for="f-company">Leave this field empty<input type="text" id="f-company" name="company" tabindex="-1" autocomplete="off"></label>
                <button type="submit" class="myc-btn myc-btn-ink">Send via WhatsApp</button>
              </form>
            </details>
          </div>
        </aside>
      </div>
      <section class="myc-section myc-section-ivory" id="similar">
        <div class="myc-wrap">
          <div class="myc-section-head">
            <h2>Similar yachts</h2>
            <a class="myc-link" href="{url_of("yacht")}">See the full fleet <span aria-hidden="true">&rarr;</span></a>
          </div>
          {sim}
        </div>
      </section>
      <section class="myc-section">
        <div class="myc-wrap">
          {cta_band(f"Check the {esc(short)}&rsquo;s availability", f"One call or WhatsApp message &mdash; captain and crew included, from {price} for 4 hours.", old)}
        </div>
      </section>
'''
    doc = shell(old, title=c["title"], desc=ia.DESCRIPTIONS.get(old, c["desc"]), body=body, head_extra=head_extra, yacht=b, og_alt=f"{name} — Miami Yacht Collective")
    write(old, doc)


# =============================================================================== /yachts hub
def fleet_hub():
    old = "yacht"
    title = "Yachts &amp; Boats for Rent in Miami | Fleet of 9, 25–90 ft"
    desc = ia.DESCRIPTIONS["yacht"]
    check_lengths(title, desc)
    trail = section_crumb(old)
    faq = [
        ("How much does it cost to rent a yacht in Miami?", "Our private charters start at $1,000 for 4 hours on the 25' Yamaha 255XD, and the 46' Maxum is $1,500. Mid-size 55–62 ft yachts run $1,600–$1,700 for 4 hours, 65–75 ft yachts are $3,000, and the 90-foot Deep Blue with Jacuzzi is $4,999 for 4 hours — captain and crew always included. See the <a href=\"/prices\">full price guide</a>."),
        ("What's included in the price?", "Every charter includes the yacht, a licensed captain and professional crew. You never drive the boat yourself, and nobody in your group needs a boating license."),
        ("Which yacht is right for my group?", "Small, fast groups take the 25' Yamaha 255XD or the 28' Axopar Brabus. Birthdays and bachelorettes usually land on the 46' Maxum, the 48' Isabella with Jet Ski or the 55' Azimut. Milestone celebrations and client days go to the 62' Anvera, the 65' Azimut L'chaim and the 75' Ferretti, and once-only events to the 90' Deep Blue. Tell us the occasion and we'll match the boat."),
        ("Where do charters depart from?", f"From our dock at {DOCK_LONG}. From there you cruise down the river into Biscayne Bay."),
    ]
    table_rows = "\n".join(
        f'<tr><td><a href="{url_of(b["old"])}">{esc(b["name"])}</a></td><td>{b["length"]} ft</td><td>{b["type"]}</td><td>{price_str(b)} / 4 h</td><td>{esc(b["blurb"])}</td></tr>'
        for b in FLEET)
    body = f'''
      {hero(old, "Yachts &amp; Boats for Rent in Miami", "Nine private yachts and boats from 25 to 90 feet, every one with a licensed captain and crew included. Filter by size, budget or feature, compare them side by side, then book by phone or WhatsApp.",
            [("Fleet", "9 yachts, 25&rsquo;&ndash;90&rsquo;"), ("From", "$1,000 / 4 hrs"), ("Included", "Captain &amp; crew"), ("Departs", "Miami River")], "Ask which yacht fits")}
      <section class="myc-section myc-on-light">
        <div class="myc-wrap">
          <div class="myc-filters" aria-label="Filter the fleet">
            <fieldset>
              <legend>Size</legend>
              <button type="button" class="myc-filter" data-group="size" data-value="all" aria-pressed="true">All sizes</button>
              <button type="button" class="myc-filter" data-group="size" data-value="small" aria-pressed="false">Day boats under 40&rsquo;</button>
              <button type="button" class="myc-filter" data-group="size" data-value="mid" aria-pressed="false">Yachts 40&rsquo;&ndash;69&rsquo;</button>
              <button type="button" class="myc-filter" data-group="size" data-value="large" aria-pressed="false">Superyachts 70&rsquo;+</button>
            </fieldset>
            <fieldset>
              <legend>Budget for 4 hours</legend>
              <button type="button" class="myc-filter" data-group="budget" data-value="all" aria-pressed="true">Any budget</button>
              <button type="button" class="myc-filter" data-group="budget" data-value="b1" aria-pressed="false">Under $1,500</button>
              <button type="button" class="myc-filter" data-group="budget" data-value="b2" aria-pressed="false">$1,500&ndash;$3,000</button>
              <button type="button" class="myc-filter" data-group="budget" data-value="b3" aria-pressed="false">$3,000+</button>
            </fieldset>
            <fieldset>
              <legend>Feature</legend>
              <button type="button" class="myc-filter" data-group="feature" data-value="all" aria-pressed="true">Any</button>
              <button type="button" class="myc-filter" data-group="feature" data-value="jet ski" aria-pressed="false">Jet ski included</button>
              <button type="button" class="myc-filter" data-group="feature" data-value="jacuzzi" aria-pressed="false">Jacuzzi</button>
            </fieldset>
            <!-- TODO(owner): a "guests" filter is ready to add once a maximum guest count per yacht is supplied -->
            <p class="myc-filter-status" data-filter-status aria-live="polite">Showing all 9 yachts</p>
          </div>
          <div data-filter-grid>
            {cards([b["old"] for b in FLEET], heading="h2")}
            <p class="myc-filter-empty" data-filter-empty hidden>No yacht matches every filter. <button type="button" class="myc-link" data-filter-reset style="background:none;border:0;cursor:pointer;font:inherit">Clear the filters</button> or <a href="{TEL}">call {PHONE_DISPLAY}</a> and we will match the boat to your group.</p>
          </div>
        </div>
      </section>
      <section class="myc-section myc-section-ivory">
        <div class="myc-wrap">
          <h2>The fleet at a glance</h2>
          <div class="myc-table-wrap" style="overflow-x:auto"><table class="myc-table" style="width:100%;border-collapse:collapse;font-size:15px">
<thead><tr><th style="text-align:left;padding:14px 16px;color:#fff">Yacht</th><th style="text-align:left;padding:14px 16px;color:#fff">Length</th><th style="text-align:left;padding:14px 16px;color:#fff">Type</th><th style="text-align:left;padding:14px 16px;color:#fff">From</th><th style="text-align:left;padding:14px 16px;color:#fff">Best for</th></tr></thead>
<tbody>
{table_rows}
</tbody></table></div>
          <p style="margin-top:14px;color:var(--myc-slate)">Every rate is for a 4-hour private charter with captain and crew. Compare them on the <a class="myc-link" href="/prices">price guide</a>.</p>
        </div>
      </section>
      <section class="myc-section">
        <div class="myc-wrap myc-prose">
          <h2>How to choose</h2>
          <p><strong>Fast and small.</strong> The <a href="/yachts/25-yamaha-255xd">25' Yamaha 255XD</a> and the <a href="/yachts/28-axopar-brabus">28' Axopar Brabus Edition</a> are day boats for couples and small groups who want speed, spray and shallow sandbar spots the big yachts pass by.</p>
          <p><strong>The classic yacht day.</strong> The <a href="/yachts/46-maxum">46' Maxum</a> is a $1,500 open-deck yacht for groups, the <a href="/yachts/48-isabella">48' Isabella</a> brings a jet ski along, and the <a href="/yachts/55-azimut">55' Azimut</a> and <a href="/yachts/62-anvera">62' Anvera</a> add Italian lines and a sportier ride. These are the boats most birthdays, bachelorettes and sunset cruises book.</p>
          <p><strong>When the occasion matters.</strong> The <a href="/yachts/65-azimut-lchaim">65' Azimut L'chaim</a> and the <a href="/yachts/75-ferretti">75' Ferretti</a> give a group three decks and real yacht presence at $3,000. The <a href="/yachts/90-deep-blue">90' Deep Blue with Jacuzzi</a> is the headline boat for corporate events, big birthdays and once-only celebrations.</p>
          <p>Not sure? Tell us the date, the group and the occasion on <a href="{wa_for(old)}" target="_blank" rel="noopener">WhatsApp</a> or by phone and we'll recommend the boat. Browse by occasion on the <a href="/experiences">experiences</a> pages or by where you want to go on the <a href="/destinations">destinations</a> pages.</p>
          {faq_block(faq)}
          {cta_band("Not sure which yacht? Ask us.", "Call or WhatsApp with your date and group size &mdash; we check live availability and match the boat to the occasion, 24/7.", old)}
        </div>
      </section>
'''
    head_extra = "\n".join([itemlist_jsonld("Miami Yacht Collective Fleet", [(b["name"], abs_url(b["old"])) for b in FLEET]), breadcrumb_jsonld(trail), faq_jsonld(faq), org_jsonld()])
    write(old, shell(old, title=title, desc=desc, body=body, head_extra=head_extra, og_alt="Nine private yachts, 25 to 90 feet — Miami Yacht Collective"))


# =============================================================================== tiles for hubs
TILE_IMG = {
    "sandbar-yacht-charter-miami": ("photos/yamaha-255xd-25/easyfowey-9-800.webp", "Boat anchored at a Miami sandbar on a private charter"),
    "star-island-boat-tour-miami": ("photos/azimut-lchaim-65/4-800.webp", "Azimut L'chaim cruising past Fisher Island"),
    "yacht-rental-miami-beach": ("photos/azimut-lchaim-65/60_AZI_WEB-13-800.webp", "Bow sunpad of the Azimut L'chaim facing downtown Miami"),
    "south-beach-yacht-rental": ("photos/isabella-48/4-800.webp", "Aerial view of the Isabella 48-foot yacht on Biscayne Bay"),
    "yacht-rental-brickell": ("photos/anvera-62/anveras-41-800.webp", "Anvera 62 running through downtown Miami near Brickell"),
    "art-basel-yacht-charter-miami": ("photos/deep-blue-90/deepblue-1-800.webp", "Aft deck of the 90-foot Deep Blue yacht"),
    "new-years-eve-yacht-miami": ("photos/azimut-lchaim-65/32-800.webp", "Crew serving drinks to guests on the Azimut L'chaim"),
    "spring-break-yacht-miami": ("photos/isabella-48/1-800.webp", "Isabella 48 yacht with its jet ski in Miami"),
    "miami-grand-prix-yacht-charter": ("photos/anvera-62/anveras-9-800.webp", "Aerial view of the 62-foot Anvera with the Miami skyline behind"),
}


def tile(slug, kicker, title, text):
    src, alt = TILE_IMG[slug]
    w, h = dims(src)
    return f'''<a class="myc-tile" href="{url_of(slug)}">
  <img src="/{src}" width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async">
  <div class="myc-tile-body"><p class="myc-tile-kicker">{kicker}</p><h3>{title}</h3><p>{text}</p><span class="myc-more">Explore <span aria-hidden="true">&rarr;</span></span></div>
</a>'''


# =============================================================================== /destinations hub
def destinations_hub():
    old = "destinations"
    title = "Yacht Charter Destinations in Miami | Miami Yacht Collective"
    desc = "Sandbar days, Star Island, Miami Beach, South Beach and Brickell: where a private 4-hour yacht charter from the Miami River goes, crew included."
    check_lengths(title, desc)
    trail = section_crumb(old)
    tiles = "\n".join([
        tile("sandbar-yacht-charter-miami", "Swim stop", "Sandbar charters", "Anchor in waist-deep turquoise water at Nixon&rsquo;s Sandbar off Key Biscayne, or push on to the stilt houses of Stiltsville."),
        tile("star-island-boat-tour-miami", "Sightseeing", "Star Island boat tours", "The celebrity homes of Star, Palm and Hibiscus Islands from your own yacht, not a tour boat with a microphone."),
        tile("yacht-rental-miami-beach", "Staying in", "Miami Beach", "Fifteen minutes from the beach to the dock, then straight out past the Venetian Islands and the skyline."),
        tile("south-beach-yacht-rental", "Staying in", "South Beach", "Fisher Island and Government Cut sit right off the causeway. The islands are the first thing you see."),
        tile("yacht-rental-brickell", "Staying in", "Brickell &amp; Downtown", "Ten minutes from the towers to the river. The charter starts in the middle of the city and leaves it behind."),
    ])
    faq = [
        ("Where do charters depart from?", f"From our dock at {DOCK_LONG}, with easy parking and no marina crowds. Every charter starts on the river and heads into Biscayne Bay."),
        ("Where can the yacht take us in four hours?", "Classic routes cover Biscayne Bay, the Star Island and Fisher Island mansions, swim stops at Nixon's Sandbar, day trips to Stiltsville and sunset skyline cruises. Your captain shapes the route around your group."),
        ("Can you take us to Stiltsville?", "Yes. Stiltsville sits on the flats at the edge of Biscayne Bay inside Biscayne National Park. Tell us when you book and we'll plan a charter long enough to include it."),
        ("Can you pick us up in Miami Beach or Brickell?", "Every charter boards at our Miami River dock, which is about 10 minutes from Brickell and 15 from Miami Beach. The location pages explain the easiest way to reach it from each neighborhood."),
    ]
    body = f'''
      {hero(old, "Where a Miami Yacht Charter Can Take You", "Every charter leaves one dock on the Miami River and reaches the whole bay in four hours: the celebrity islands, the sandbar, the skyline and the open water past Fisher Island. Pick the place and we&rsquo;ll match the boat.",
            [("Departure", "Miami River dock"), ("Reach", "Biscayne Bay to Stiltsville"), ("From", "$1,000 / 4 hrs"), ("Booking", "Call or WhatsApp, 24/7")], "Plan the route")}
      <section class="myc-section myc-on-light">
        <div class="myc-wrap">
          <div class="myc-section-head"><h2>Destinations</h2><p>Each page covers the route, the best boats for it and what the day looks like hour by hour.</p></div>
          <div class="myc-tiles">
{tiles}
          </div>
        </div>
      </section>
      <section class="myc-section myc-section-ivory">
        <div class="myc-wrap myc-prose">
          <h2>The route, from the dock out</h2>
          <ol class="myc-timeline">
            <li><span class="t">Start</span><strong>The Miami River</strong><p>Board at {DOCK_LONG}. The first ten minutes run under the bridges and past the Brickell towers.</p></li>
            <li><span class="t">Bay</span><strong>Biscayne Bay and the skyline</strong><p>The river opens into the bay with downtown Miami and Brickell behind you &mdash; the view every photo of Miami is trying to get.</p></li>
            <li><span class="t">Islands</span><strong>Star, Palm, Hibiscus and the Venetian Islands</strong><p>Waterfront estates behind guarded gates, best seen exactly the way we see them: from the water, at a slow pace.</p></li>
            <li><span class="t">Cut</span><strong>Fisher Island and Government Cut</strong><p>The private island at the mouth of the shipping channel, reachable only by boat or ferry, with South Beach across the water.</p></li>
            <li><span class="t">Swim</span><strong>Nixon&rsquo;s Sandbar</strong><p>A shallow stretch off Key Biscayne where you stand in the water beside the boat. The stop on almost every party and birthday charter we run.</p></li>
            <li><span class="t">Far end</span><strong>Stiltsville</strong><p>Wooden houses standing on the flats at the edge of the bay inside Biscayne National Park, with the skyline on the horizon behind you.</p></li>
          </ol>
          <p>Comparing the swim spots? The <a href="/guides/miami-sandbar-guide">Miami sandbar guide</a> covers Nixon&rsquo;s, Haulover and Stiltsville side by side, and <a href="/guides/best-time-yacht-charter-miami">the best time to charter</a> covers seasons, sunset times and weekday versus weekend.</p>
        </div>
      </section>
      <section class="myc-section">
        <div class="myc-wrap">
          <div class="myc-section-head"><h2>Boats that make the most of the bay</h2><a class="myc-link" href="/yachts">See the full fleet <span aria-hidden="true">&rarr;</span></a></div>
          {cards(["isabella", "axopar-brabus", "azimut-lchaim", "yamaha-255xd"])}
        </div>
      </section>
      <section class="myc-section myc-section-ivory">
        <div class="myc-wrap myc-prose">
          {faq_block(faq)}
          <p>Planning a celebration around the route? Start with <a href="/experiences/birthday-yacht-party-miami">birthday yacht parties</a> or <a href="/experiences/private-sunset-cruise-miami">private sunset cruises</a>, or see <a href="/experiences">all experiences</a>.</p>
          {cta_band("Tell us where you want to go", "Call or WhatsApp with your date and group size &mdash; we&rsquo;ll match the yacht and the route, 24/7.", old)}
        </div>
      </section>
'''
    head_extra = "\n".join([itemlist_jsonld("Miami yacht charter destinations", [(PAGES[s]["label"], abs_url(s)) for s, _, _ in ia.DESTINATIONS]), breadcrumb_jsonld(trail), faq_jsonld(faq), org_jsonld()])
    write(old, shell(old, title=title, desc=desc, body=body, head_extra=head_extra))


# =============================================================================== /events hub
def events_hub():
    old = "events"
    title = "Miami Event Week Yacht Charters | Miami Yacht Collective"
    desc = "Art Basel, New Year's Eve, spring break and Grand Prix weekend: private yacht charters in Miami at the same prices as any other week, crew included."
    check_lengths(title, desc)
    trail = section_crumb(old)
    tiles = "\n".join([
        tile("art-basel-yacht-charter-miami", "December 4&ndash;6, 2026", "Art Basel week", "Client hospitality and sunset escapes fifteen minutes from the Convention Center, on your own yacht."),
        tile("new-years-eve-yacht-miami", "December 31", "New Year&rsquo;s Eve", "Your own yacht instead of a ticketed party boat. No holiday surcharge."),
        tile("spring-break-yacht-miami", "March 2027", "Spring break &amp; Music Week", "Miami Music Week and Ultra weekend with your group&rsquo;s own boat and a sandbar stop."),
        tile("miami-grand-prix-yacht-charter", "Early May", "Grand Prix weekend", "A private 4-hour charter between the sessions, at regular prices."),
    ])
    faq = [
        ("Do prices go up during event weeks?", "No. Our prices are the same every week of the year, including Art Basel, New Year's Eve, spring break, Miami Music Week, Ultra and Grand Prix weekend: from $1,000 for 4 hours with captain and crew included."),
        ("How long is an event-week charter?", "Every charter is 4 hours. You choose whether that window is an afternoon on the bay, a sunset run or a night cruise."),
        ("When should we book for a big week?", "Early. The big weekends are the first dates of the year to fill, and the larger yachts go first. Call or WhatsApp as soon as you have the date and we'll hold the boat."),
    ]
    body = f'''
      {hero(old, "Yacht Charters for Miami&rsquo;s Big Weeks", "The weeks the whole world comes to Miami are the best weeks to be on the water, away from the crowds and the lines. We run the same prices every week of the year. Each page has the dates and how a 4-hour charter fits around them.",
            [("Prices", "Same every week"), ("From", "$1,000 / 4 hrs"), ("Charter", "4 hours, private"), ("Booking", "Call or WhatsApp, 24/7")], "Hold a date")}
      <section class="myc-section myc-on-light">
        <div class="myc-wrap">
          <div class="myc-section-head"><h2>Event weeks</h2><p>Dates need a yearly refresh; the current ones are on each page.</p></div>
          <div class="myc-tiles">
{tiles}
          </div>
        </div>
      </section>
      <section class="myc-section myc-section-ivory">
        <div class="myc-wrap">
          <div class="myc-section-head"><h2>The yachts groups book for event weeks</h2><a class="myc-link" href="/yachts">See the full fleet <span aria-hidden="true">&rarr;</span></a></div>
          {cards(["deep-blue", "ferretti", "azimut-lchaim", "isabella"])}
        </div>
      </section>
      <section class="myc-section">
        <div class="myc-wrap myc-prose">
          {faq_block(faq)}
          <p>Hosting clients? See <a href="/experiences/corporate-yacht-charter-miami">corporate yacht charters</a>. Celebrating? See <a href="/experiences/yacht-party-miami">private yacht parties</a>. And for timing, seasons and sunset hours, read <a href="/guides/best-time-yacht-charter-miami">the best time for a yacht charter in Miami</a>.</p>
          {cta_band("Book the big weekend early", "Call or WhatsApp with your dates &mdash; we check live availability and hold the yacht the same day.", old)}
        </div>
      </section>
'''
    head_extra = "\n".join([itemlist_jsonld("Miami event week yacht charters", [(PAGES[s]["label"], abs_url(s)) for s, _ in ia.EVENTS]), breadcrumb_jsonld(trail), faq_jsonld(faq), org_jsonld()])
    write(old, shell(old, title=title, desc=desc, body=body, head_extra=head_extra))


# =============================================================================== /faq
def faq_page():
    old = "faq"
    title = "Miami Yacht Charter FAQ | Miami Yacht Collective"
    desc = "Answers to the questions we hear most: what a Miami yacht charter costs, what's included, where the boats leave from, licenses, children and how to book."
    check_lengths(title, desc)
    trail = section_crumb(old)
    groups = [
        ("pricing", "Prices and what&rsquo;s included", [
            ("How much does it cost to rent a yacht in Miami?", "Our private charters start at $1,000 for 4 hours on the 25' Yamaha 255XD, and the 46' Maxum is $1,500. Mid-size 55–62 ft yachts run $1,600–$1,700 for 4 hours, 65–75 ft yachts are $3,000, and our 90-foot superyacht is $4,999 for 4 hours — captain and crew always included. See the <a href=\"/prices\">full price guide</a>."),
            ("What's included in the price?", "Every charter includes the yacht, a licensed USCG captain and professional crew. You never drive the boat yourself, and nobody in your group needs a boating license."),
            ("Why do prices differ so much between yachts?", "Size and vessel class drive the rate. A higher price buys more deck space, more luxury and features like the Deep Blue's on-deck Jacuzzi or the Isabella's included jet ski — not more people."),
            ("Are there hidden fees or platform markups?", "You book direct with us by phone or WhatsApp — no marketplace platform fees and no broker markup. Confirm the all-in total for your date when you book."),
            ("Do prices go up on holidays or event weeks?", "No. Our prices are the same on every date of the year, including New Year's Eve, Art Basel, spring break, Miami Music Week, Ultra and Grand Prix weekend."),
            ("Can I book 6 or 8 hours?", "Every listed price is for a 4-hour charter. Longer days are quoted on request — tell us what you have in mind when you call or message. <!-- TODO(owner): publish 6h/8h rates when confirmed -->"),
        ]),
        ("booking", "Booking", [
            ("How do I book?", f"Call or WhatsApp {PHONE_DISPLAY} — we answer 24/7 and most charters are confirmed in under 10 minutes. No web forms, no platform fees, no broker markup."),
            ("How far ahead should we book?", "Call or WhatsApp as soon as you have a date. We check live availability while you're on the line and can hold the yacht the same day. Weekends, sunset slots and event weeks fill first."),
            ("How do I get an exact quote?", f"Call or WhatsApp {PHONE_DISPLAY} with your date, group size and how many hours you want. We quote on the spot, 24/7."),
            ("Do you speak Spanish?", "Yes. We book and run charters in English and Spanish. Nobody on the team speaks Portuguese, but our <a href=\"/aluguel-de-iate-em-miami\" lang=\"pt-BR\">Portuguese page</a> explains how to book in English or Spanish."),
            ("What is your cancellation policy?", "Ask us when you book and we'll confirm the terms for your date in writing. <!-- TODO(owner): link /cancellation-policy here once the draft is approved -->"),
        ]),
        ("day", "The day on the water", [
            ("Where do charters depart from?", f"From our dock at {DOCK_LONG}, with easy parking and no marina crowds."),
            ("Where can the yacht take us?", "Classic routes cover Biscayne Bay, the Star Island and Fisher Island mansions, swim stops at Nixon's Sandbar, day trips to Stiltsville and sunset skyline cruises. Your captain shapes the route around your group. See the <a href=\"/destinations\">destinations</a> pages."),
            ("How long is a charter?", "Every charter is 4 hours, which covers a skyline cruise, the islands loop, a swim stop and a sunset finish if you book the late slot."),
            ("What should I bring and wear?", "Light clothes with a swimsuit underneath, polarized sunglasses and a hat that fits tight. Wear soft-soled shoes to the dock and expect to go barefoot on board. Use lotion sunscreen rather than spray, which makes decks slippery. Full list in <a href=\"/guides/what-to-bring-yacht-charter-miami\">what to bring on a yacht charter</a>."),
            ("Is the water rough?", "Charters run on Biscayne Bay, which is sheltered from the open ocean by Miami Beach and Key Biscayne. The captain picks the route for the day's conditions."),
            ("What happens if the weather turns?", "Your captain makes the call on the day based on the forecast and conditions on the bay. Ask us about rescheduling terms when you book. <!-- TODO(owner): confirm the weather / rescheduling policy -->"),
        ]),
        ("fleet", "The fleet", [
            ("Which yacht is right for my group?", "Small, fast groups take the 25' Yamaha 255XD or the 28' Axopar Brabus. Birthdays and bachelorettes usually land on the 46' Maxum, the 48' Isabella with Jet Ski or the 55' Azimut. Milestone celebrations and client days go to the 62' Anvera, the 65' Azimut L'chaim and the 75' Ferretti, and once-only events to the 90' Deep Blue with Jacuzzi. Browse <a href=\"/yachts\">all nine yachts</a>."),
            ("Is there a bathroom on board?", "The 48' Isabella, 65' Azimut L'chaim, 75' Ferretti and 90' Deep Blue have a bathroom below deck. Ask when you book and we will match the boat to your group."),
            ("Which yacht comes with a jet ski?", "The <a href=\"/yachts/48-isabella\">48' Isabella</a>. The jet ski is included in the $1,499 charter, so half the group can be on the water while the other half holds the deck."),
            ("Which yacht has the Jacuzzi?", "The <a href=\"/yachts/90-deep-blue\">90' Deep Blue</a>, the largest yacht in the fleet, at $4,999 for 4 hours."),
            ("How many guests can each yacht take?", "Tell us your group size when you book and we'll match the right yacht to it. <!-- TODO(owner): publish the maximum guest count per yacht when confirmed -->"),
        ]),
        ("rules", "Licenses, children and rules", [
            ("Do I need a boating license?", "No. When a licensed captain operates the boat, guests need no license, card or boating experience. Every Miami Yacht Collective charter includes a licensed captain and crew. Details in <a href=\"/guides/boating-license-miami-boat-rental\">do you need a license to rent a boat in Miami</a>."),
            ("Are children allowed on the charter?", "Yes. Children are welcome on every boat in the fleet, and children's life jackets are on board. Tell us the ages when you book so the crew has the right ones ready."),
            ("Can we hold a ceremony or a photo shoot on board?", "Yes. Wedding ceremonies, elopements and vow renewals are welcome, and so are commercial photo and video shoots. The captain will position the boat for the shots you want. See <a href=\"/experiences/wedding-yacht-charter-miami\">weddings on board</a> and <a href=\"/experiences/yacht-photoshoot-miami\">photo and video shoots</a>."),
            ("Is this a ticketed party boat?", "No. Every charter is fully private: the whole yacht is yours, with just your group on board. You choose the music, the route and the vibe."),
            ("Can we bring food and drinks on board?", "Ask us when you book and we'll tell you what works on the yacht you've chosen. <!-- TODO(owner): confirm BYOB, catering, ice and cooler policy -->"),
        ]),
    ]
    toc = "\n".join(f'<li><a href="#{k}">{t}</a></li>' for k, t, _ in groups)
    sections = []
    all_faq = []
    for key, heading, qs in groups:
        all_faq += qs
        items = "\n".join(f'<div class="myc-faq-item">\n<h3>{esc(q)}</h3>\n<p>{a}</p>\n</div>' for q, a in qs)
        sections.append(f'<section class="myc-faq-group" id="{key}">\n<h2>{heading}</h2>\n{items}\n</section>')
    body = f'''
      {hero(old, "Frequently Asked Questions", "Everything we get asked before a booking, answered plainly. If your question isn&rsquo;t here, one call or WhatsApp message gets it answered 24/7.",
            [("Charters", "4 hours, private"), ("From", "$1,000 / 4 hrs"), ("Included", "Captain &amp; crew"), ("Departs", "Miami River")], "Ask a question")}
      <section class="myc-section myc-on-light">
        <div class="myc-wrap myc-prose" style="max-width:860px">
          <ul class="myc-toc myc-chips">
{toc}
          </ul>
{chr(10).join(sections)}
          <p>Still deciding? Compare the <a href="/yachts">fleet</a>, read the <a href="/prices">price guide</a> or browse the <a href="/guides">planning guides</a>.</p>
          {cta_band("Ask us anything", "Call or WhatsApp &mdash; a real person answers 24/7 and most charters are confirmed in under 10 minutes.", old)}
        </div>
      </section>
'''
    clean = [(q, re.sub(r"\s*<!--.*?-->", "", a)) for q, a in all_faq]
    head_extra = "\n".join([faq_jsonld(clean), breadcrumb_jsonld(trail), org_jsonld()])
    write(old, shell(old, title=title, desc=desc, body=body, head_extra=head_extra))


# =============================================================================== /add-ons
def addons_page():
    old = "add-ons"
    title = "Yacht Charter Add-Ons in Miami | Miami Yacht Collective"
    desc = "What comes with every Miami Yacht Collective charter, which yachts have a jet ski or Jacuzzi built in, and how to ask for extras for your day."
    check_lengths(title, desc)
    trail = section_crumb(old)
    body = f'''
      {hero(old, "Add-Ons and Extras", "Every charter already comes with the yacht, a licensed captain and crew and four hours on the water. This page covers what is built into specific yachts and how to ask for anything else.",
            [("Included", "Captain &amp; crew"), ("Charter", "4 hours, private"), ("Extras", "On request"), ("Booking", "Call or WhatsApp, 24/7")], "Ask about an extra")}
      <section class="myc-section myc-on-light">
        <div class="myc-wrap myc-prose" style="max-width:860px">
          <h2>Included on every charter</h2>
          <ul class="myc-check">
            <li>The whole yacht, private to your group</li>
            <li>Licensed captain and professional crew</li>
            <li>4 hours on the water from the Miami River dock</li>
            <li>Children&rsquo;s life jackets on board</li>
            <li>Service in English and Spanish</li>
            <li>The same price on every date of the year</li>
          </ul>
          <h2>Built into specific yachts</h2>
          <ul>
            <li><a href="/yachts/48-isabella">48' Isabella with Jet Ski</a> &mdash; a jet ski comes with the charter at no extra cost.</li>
            <li><a href="/yachts/90-deep-blue">90' Deep Blue with Jacuzzi</a> &mdash; the only yacht in the fleet with a Jacuzzi on deck.</li>
            <li><a href="/yachts/65-azimut-lchaim">65' Azimut L'chaim</a> &mdash; an inflatable slide and water toys are available at an additional cost.</li>
          </ul>
          <h2>Have something specific in mind?</h2>
          <p>Decorations for a birthday, a photographer for a proposal, a longer day, a particular start time &mdash; tell us what you&rsquo;re planning when you call or message and we&rsquo;ll tell you what we can arrange on the yacht you&rsquo;ve chosen and what it costs. We would rather answer honestly than list things on a page.</p>
          <!-- TODO(owner): confirm which add-ons MYC actually offers (catering, decorations, photographer, DJ/sound, water toys, extra hours, towels, ice)
               and their prices. Sub-pages are created only for confirmed services. This page is noindex until then. -->
          <p>Occasion first? Browse <a href="/experiences">all experiences</a>; boat first? Compare the <a href="/yachts">fleet</a> and the <a href="/prices">prices</a>.</p>
          {cta_band("Tell us what you have in mind", "Call or WhatsApp with your date, group size and the extras you&rsquo;re thinking about &mdash; we answer 24/7.", old)}
        </div>
      </section>
'''
    head_extra = "\n".join([breadcrumb_jsonld(trail), org_jsonld()])
    write(old, shell(old, title=title, desc=desc, body=body, head_extra=head_extra, noindex=True))


# =============================================================================== legal drafts
DRAFT = '<p class="myc-draft"><strong>DRAFT &ndash; owner to review.</strong> This page is a template written on 2026-10-28 and is not yet published to search engines. Bracketed items need the owner&rsquo;s confirmation before it goes live.</p>'


def legal_page(old, title, h1, desc, sections):
    check_lengths(title, desc)
    trail = section_crumb(old)
    sec = "\n".join(f"<h2>{h}</h2>\n{b}" for h, b in sections)
    body = f'''
      <section class="myc-yhero">
        <div class="myc-wrap">
          {breadcrumb_html(trail)}
          <h1>{h1}</h1>
          <p class="myc-lede">Miami Yacht Collective &middot; {ia.ADDRESS_LINE}, {ia.ADDRESS_CITY} &middot; <a href="{TEL}" style="color:#fdfcf9">{PHONE_DISPLAY}</a></p>
        </div>
      </section>
      <section class="myc-section myc-on-light">
        <div class="myc-wrap myc-prose myc-legal">
          {DRAFT}
          <p><em>Last updated: 2026-10-28 (draft)</em></p>
{sec}
          <h2>Contact</h2>
          <p>Questions about this policy: call or WhatsApp <a href="{TEL}">{PHONE_DISPLAY}</a> or email <a href="mailto:{ia.EMAIL}">{ia.EMAIL}</a>. <!-- TODO(owner): replace with a branded @miamiyachtcollective.com address --></p>
        </div>
      </section>
'''
    head_extra = "\n".join([breadcrumb_jsonld(trail), org_jsonld()])
    write(old, shell(old, title=title, desc=desc, body=body, head_extra=head_extra, noindex=True))


def legal_pages():
    legal_page("privacy-policy", "Privacy Policy | Miami Yacht Collective", "Privacy Policy",
               "How Miami Yacht Collective handles the information you share when you call, message or browse the site. Draft pending owner review.", [
        ("Who we are", "<p>Miami Yacht Collective arranges private yacht charters departing from 668 NW N River Dr, Miami, FL 33136. This policy explains what information we collect when you use miamiyachtcollective.com or contact us, and how we use it.</p>"),
        ("What we collect", "<ul><li><strong>Contact details you give us.</strong> When you call, WhatsApp or email us you share your name, phone number and the details of the charter you want (date, group size, occasion). We use them to answer you and to arrange the charter.</li><li><strong>Site analytics.</strong> The site uses Google Analytics 4 and Vercel Web Analytics to understand which pages are visited and which buttons are tapped (for example, a tap on the WhatsApp button). This data is aggregated and does not identify you by name.</li><li><strong>Payments.</strong> The site itself takes no payments. If we send you a payment link, it is processed by Stripe under Stripe&rsquo;s own privacy policy; we never see your full card number.</li></ul><!-- TODO(owner): confirm there is no other tracking (Meta pixel, call tracking, CRM) -->"),
        ("Cookies", "<p>Analytics cookies are set by Google Analytics and Vercel Web Analytics. The site sets no advertising cookies of its own. You can block cookies in your browser settings without affecting your ability to call or message us.</p><!-- TODO(owner): if Google Ads conversion tracking is added, list it here -->"),
        ("How we use your information", "<ul><li>To answer your enquiry and arrange, confirm and run your charter.</li><li>To contact you about your booking (changes, weather, meeting point).</li><li>To improve the website and our service.</li></ul><p>We do not sell your information. We share it only with the people needed to run your charter (for example, the captain of the yacht you booked) and with the service providers above.</p>"),
        ("How long we keep it", "<p>Booking details are kept for as long as needed to run the charter and meet our legal and accounting obligations, then deleted. [TODO(owner): confirm the retention period.]</p>"),
        ("Your rights", "<p>You can ask us what information we hold about you, ask us to correct it or ask us to delete it by contacting us at the details below. If you are in the EU, UK or a US state with privacy legislation, you may have additional rights under that law.</p>"),
        ("Third-party links", "<p>The site links to WhatsApp, Instagram and Google Maps. Those services have their own privacy policies.</p>"),
    ])
    legal_page("terms", "Terms of Service | Miami Yacht Collective", "Terms of Service",
               "Terms for a private yacht charter with Miami Yacht Collective: booking, payment, conduct on board, weather and liability. Draft pending owner review.", [
        ("The charter", "<p>Miami Yacht Collective arranges private, captained yacht charters departing from 668 NW N River Dr, Miami, FL 33136. Every charter includes the yacht, a licensed captain and crew for a 4-hour period unless a different duration is agreed in writing. The published price is for the whole yacht, not per person.</p>"),
        ("Booking and confirmation", "<p>Bookings are made by phone or WhatsApp. A charter is confirmed when we have confirmed the date, yacht and price in writing (WhatsApp message or email) and any agreed deposit has been received. [TODO(owner): confirm the deposit amount and when the balance is due.]</p>"),
        ("Payment", "<p>Payment is made by the method we agree with you, which may include a Stripe payment link. [TODO(owner): list accepted payment methods and whether gratuity, fuel or dockage are included or extra.]</p>"),
        ("Cancellations and changes", "<p>Our <a href=\"/cancellation-policy\">cancellation policy</a> sets out the terms for cancelling or moving a charter.</p>"),
        ("The captain&rsquo;s authority", "<p>The captain is responsible for the safety of everyone on board and has the final say on the route, the anchorage, swimming and the sea state. The captain may shorten, change or end a charter if conditions or the conduct of guests make it unsafe to continue.</p>"),
        ("Guests and conduct", "<p>The guest who books is responsible for their group. Guests follow the crew&rsquo;s safety instructions, wear life jackets when asked, and treat the yacht with care. Damage caused by a guest beyond normal wear is charged to the booking guest. Illegal substances are not permitted on board. [TODO(owner): confirm the alcohol policy and the minimum age, if any.]</p>"),
        ("Weather", "<p>If the captain decides the weather makes a charter unsafe, we will offer another date or, where that is not possible, a refund of amounts paid for that charter. Rain alone does not cancel a charter. [TODO(owner): confirm.]</p>"),
        ("Liability", "<p>To the extent permitted by Florida law, Miami Yacht Collective&rsquo;s liability for any claim arising from a charter is limited to the amount paid for that charter. Nothing in these terms limits liability that cannot be limited by law. Guests join a charter at their own risk with respect to swimming and water activities.</p>"),
        ("Governing law", "<p>These terms are governed by the laws of the State of Florida.</p>"),
    ])
    legal_page("cancellation-policy", "Cancellation Policy | Miami Yacht Collective", "Cancellation Policy",
               "How cancellations, date changes and weather are handled for a private yacht charter booked with Miami Yacht Collective. Draft pending owner review.", [
        ("Cancelling a charter", "<ul><li>Cancelled more than [TODO(owner): N] days before the charter: [TODO(owner): full refund / deposit refunded].</li><li>Cancelled between [N] and [M] days before: [TODO(owner): deposit retained].</li><li>Cancelled less than [M] days before, or no-show: [TODO(owner): full amount due].</li></ul><!-- TODO(owner): replace with the real tiers; the GetMyBoat listings use 1% refund within 5 days, which may or may not be the direct-booking policy -->"),
        ("Changing the date", "<p>Tell us as early as you can. If the yacht is available on the new date, we move the booking at no charge [TODO(owner): confirm]. If it is not, the cancellation terms above apply.</p>"),
        ("Weather", "<p>If the captain decides the weather makes a charter unsafe, we offer another date or a refund of amounts paid for that charter. Rain alone does not cancel a charter; the decision is made on the day based on wind, sea state and lightning. [TODO(owner): confirm.]</p>"),
        ("Late arrival", "<p>Charters start at the booked time. If your group arrives late, the charter still ends at the scheduled time. [TODO(owner): confirm the grace period, if any.]</p>"),
        ("How to cancel", f"<p>Call or WhatsApp {PHONE_DISPLAY}. We confirm every cancellation or change in writing.</p>"),
    ])


# =============================================================================== /book
def book_page():
    old = "booking"
    title = "Book a Yacht in Miami | Call or WhatsApp 24/7"
    desc = ia.DESCRIPTIONS["booking"]
    check_lengths(title, desc)
    trail = section_crumb(old)
    opts = "\n".join(f'<option value="{esc(b["name"])}">{esc(b["name"])} — {price_str(b)} / 4 h</option>' for b in FLEET)
    tpl = "Hi! I'm {name}. I'd like to book the {yacht} on {date} for {guests} guests. You can reach me at {contact}. Is it available?"
    body = f'''
      <section class="myc-yhero">
        <div class="myc-wrap">
          {breadcrumb_html(trail)}
          <h1>Book your escape</h1>
          <p class="myc-lede">Booking is direct. No portals, no third-party fees. Tell us the yacht, the date and the group and we confirm by WhatsApp or phone &mdash; most charters in under 10 minutes.</p>
          <ul class="myc-stats">
            <li><span class="k">Lines open</span><span class="v">24 hours, 7 days</span></li>
            <li><span class="k">From</span><span class="v">$1,000 / 4 h</span></li>
            <li><span class="k">Included</span><span class="v">Captain &amp; crew</span></li>
            <li><span class="k">Departs</span><span class="v">Miami River dock</span></li>
          </ul>
        </div>
      </section>
      <div class="myc-wrap myc-ybody">
        <div class="myc-ymain">
          <section id="how">
            <h2>How booking works</h2>
            <div class="myc-steps">
              <div class="myc-step"><div class="num">Step 1</div><h3>Call or WhatsApp</h3><p>Tell us your date, group size and the occasion. We answer 24/7 and check live availability while you&rsquo;re on the line.</p></div>
              <div class="myc-step"><div class="num">Step 2</div><h3>We match the yacht</h3><p>We recommend the right boat from our 9-vessel fleet for your group and budget &mdash; no platforms, no broker markup.</p></div>
              <div class="myc-step"><div class="num">Step 3</div><h3>Step aboard</h3><p>Meet us at our Miami River dock &mdash; about 10 minutes from Brickell and 15 from Miami Beach &mdash; and your captain takes it from there.</p></div>
            </div>
          </section>
          <section id="fleet">
            <h2>Pick a yacht</h2>
            <p>Every rate is for a 4-hour private charter with captain and crew. Not sure which one? Send the date and group size and we&rsquo;ll recommend the boat.</p>
            {cards(["isabella", "deep-blue", "azimut-lchaim"])}
            <p style="margin-top:18px"><a class="myc-link" href="/yachts">Compare all nine yachts <span aria-hidden="true">&rarr;</span></a> &nbsp;&middot;&nbsp; <a class="myc-link" href="/prices">See every price</a></p>
          </section>
          {chrome.reviews_block()}
          <section id="faq">
            {faq_block([
                ("How fast do you confirm?", "Most charters are confirmed in under 10 minutes by phone or WhatsApp. We check availability live, match the yacht to your group and hold the date before the call ends."),
                ("Do I pay on the website?", "No. The site takes no payments. Once the charter is confirmed we send you the payment details directly. <!-- TODO(owner): confirm deposit amount and accepted payment methods -->"),
                ("Can I book for someone else?", "Yes. Give us the name and phone number of the person who will be on board so the crew can reach them on the day."),
            ])}
          </section>
        </div>
        <aside class="myc-yaside" aria-label="Booking request">
          <div class="myc-widget">
            <div class="myc-widget-head"><span class="price" style="font-size:1.5rem">Request a date</span></div>
            <p class="inc">We get your details by email and WhatsApp opens with the message ready to send</p>
            {chrome.lead_form(old, prefix="b", page="Book", template=tpl, yacht_options=opts)}
            <a class="myc-btn myc-btn-ink" href="{TEL}">{ICON_PHONE}Call {PHONE_DISPLAY}</a>
            <p class="myc-widget-note">Lines open 24 hours, 7 days a week. English and Spanish.</p>
          </div>
        </aside>
      </div>
'''
    head_extra = "\n".join([breadcrumb_jsonld(trail), org_jsonld()])
    write(old, shell(old, title=title, desc=desc, body=body, head_extra=head_extra))


# =============================================================================== 404
def not_found_page():
    old = "404"
    title = "Not Found | Miami Yacht Collective"
    desc = "That page has sailed. Find the fleet, the experiences or a way to reach Miami Yacht Collective."
    body = f'''
      <section class="myc-404 myc-on-light">
        <div class="myc-wrap">
          <p class="num" aria-hidden="true">404</p>
          <h1>This page has sailed</h1>
          <p>The page you&rsquo;re looking for doesn&rsquo;t exist or has moved. The fleet, the experiences and a real person on the phone are all one click away.</p>
          <div class="myc-btn-row">
            <a class="myc-btn myc-btn-ink" href="/">Back to home</a>
            <a class="myc-btn myc-btn-gold" href="/yachts">Browse the fleet</a>
            <a class="myc-btn myc-btn-gold" href="/experiences">Experiences</a>
            <a class="myc-btn myc-btn-ink" href="/contact">Contact</a>
          </div>
        </div>
      </section>
'''
    doc = shell(old, title=title, desc=desc, body=body, head_extra=org_jsonld(), noindex=True, og_alt="Miami Yacht Collective")
    doc = doc.replace('<link rel="canonical" href="https://miamiyachtcollective.com/404">\n', "")
    write(old, doc)


if __name__ == "__main__":
    if want("yachts"):
        for b in FLEET:
            yacht_page(b)
    if want("fleet"):
        fleet_hub()
    if want("destinations"):
        destinations_hub()
    if want("events"):
        events_hub()
    if want("faq"):
        faq_page()
    if want("addons"):
        addons_page()
    if want("legal"):
        legal_pages()
    if want("book"):
        book_page()
    if want("404"):
        not_found_page()
