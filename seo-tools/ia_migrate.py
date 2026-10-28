# -*- coding: utf-8 -*-
"""Migrate the flat Webflow-era pages to the 2026-10 information architecture.

    python3 seo-tools/ia_migrate.py            # dry run: report what would change
    python3 seo-tools/ia_migrate.py --write    # move pages, swap chrome, rewrite links, write vercel.json/robots/llms

Idempotent: a page that has already been migrated (new chrome present) is only re-linked.
Pages that are rebuilt from scratch (yacht pages, hubs, legal, FAQ, 404, book) are produced by
build_site.py; this script only removes their legacy source files once the new file exists.
"""
import json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ia
from ia import PAGES, FLEET, SITE, REPO, rewrite_links, wa_for, og_card
import chrome

WRITE = "--write" in sys.argv
TODAY = "2026-10-28"

# pages that build_site.py rebuilds entirely (legacy file is removed, not transformed)
REBUILT = {"yacht", "booking", "404"} | {b["old"] for b in FLEET}
# generated pages with no legacy source
NEW = {k for k, p in PAGES.items() if p["new"]}
# legacy files left untouched (template artifacts, redirected away)
LEAVE = {"401", "search", "logo-preview"}

HEADER_RE = re.compile(r'\s*<div data-animation="default" class="header-section w-nav".*?</div>\s*</div>\s*</div>\s*</div>\s*(?=<div class="main-wrapper">)', re.S)
FOOTER_RE = re.compile(r'<section[^>]*class="footer-section">.*?</section>\s*', re.S)
STICKY_RE = re.compile(r'<div class="myc-sticky-cta"[^>]*>.*?</div>\s*', re.S)
MODAL_RE = re.compile(r'<div class="modal-backdrop" id="modalBackdrop".*?</script>\s*', re.S)
CURSOR_RE = re.compile(r'\s*<section class="cursor-secition">.*?</section>', re.S)
WEBFLOW_RE = re.compile(r'\s*<script src="https://d3e54v103j8qbb\.cloudfront\.net/js/jquery[^>]*></script>\s*<script src="/?js/webflow\.js" type="text/javascript"></script>', re.S)
TRACK_RE = re.compile(r'<script src="/?js/tracking\.js"></script>')
NEW_HEADER_RE = re.compile(r'<a class="myc-skip".*?</header>', re.S)
NEW_FOOTER_RE = re.compile(r'<footer class="myc-footer".*?</footer>', re.S)


def sh(*cmd):
    return subprocess.run(cmd, cwd=REPO, check=True, capture_output=True, text=True).stdout


def git_mv(src, dst):
    Path(REPO / dst).parent.mkdir(parents=True, exist_ok=True)
    sh("git", "mv", "-f", src, dst)


def lang_of(s):
    m = re.search(r'<html[^>]*lang="([^"]+)"', s)
    return m.group(1) if m else "en"


def needs_webflow(s):
    """Keep jQuery/webflow.js only where Webflow interactions or components are used."""
    return bool(re.search(r'opacity:0|w-slider|w-tabs|w-dropdown|w-lightbox|w-background-video|w-form', s))


def strip_hub_crumb(s, old):
    """Pages that moved from Experiences to Destinations/Events get a new breadcrumb + BreadcrumbList."""
    p = PAGES[old]
    if p["section"] not in ("destinations", "events"):
        return s
    trail = ia.section_crumb(old)
    hub_label, hub_url = trail[1]
    s = re.sub(r'(<div class="myc-breadcrumb">.*?)<a href="/experiences">Experiences</a>', lambda m: m.group(1) + f'<a href="{hub_url}">{hub_label}</a>', s, count=1, flags=re.S)
    s = s.replace('"name": "Experiences",\n   "item": "https://miamiyachtcollective.com/experiences"', f'"name": "{hub_label}",\n   "item": "{SITE}{hub_url}"')
    return s


def transform(old, s):
    """Apply the new chrome + final URLs to a legacy page. Returns the new document."""
    lang = lang_of(s)
    yacht = ia.FLEET_BY_OLD.get(old)
    already = 'class="myc-header"' in s
    s = rewrite_links(s)
    # --- head: canonical, og:url, share card
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{ia.abs_url(old)}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{ia.abs_url(old)}">', s, count=1)
    if old in ia.DESCRIPTIONS:
        d = ia.DESCRIPTIONS[old].replace("&", "&amp;").replace('"', "&quot;")
        s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{d}">', s, count=1)
        s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{d}">', s, count=1)
        s = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{d}">', s, count=1)
    # --- chrome
    if not already:
        assert HEADER_RE.search(s), f"{old}: header not found"
        s = HEADER_RE.sub("\n    " + chrome.header(old, lang) + "\n    ", s, count=1)
        # main wrapper -> <main>
        assert '<div class="main-wrapper">' in s, f"{old}: main-wrapper missing"
        s = s.replace('<div class="main-wrapper">', '<main id="main" class="main-wrapper">', 1)
        m = FOOTER_RE.search(s)
        assert m, f"{old}: footer not found"
        before = s[:m.start()]
        close = before.rfind("</div>")
        before = before[:close] + "</main>" + before[close + 6:]
        s = before + chrome.footer(old, lang) + "\n  " + s[m.end():]
        s = STICKY_RE.sub(chrome.sticky(old, lang, yacht) + "\n", s, count=1)
        s = MODAL_RE.sub(chrome.modal(old, lang) + "\n", s, count=1)
        if not needs_webflow(s):
            s = WEBFLOW_RE.sub("", s)
            s = CURSOR_RE.sub("", s)
        s = TRACK_RE.sub('<script src="/js/tracking.js"></script>\n<script defer src="/js/myc-site.js"></script>', s, count=1)
    else:
        # already migrated: refresh the shared chrome so header/footer edits propagate
        s = NEW_HEADER_RE.sub(lambda m: chrome.header(old, lang), s, count=1)
        s = NEW_FOOTER_RE.sub(lambda m: chrome.footer(old, lang), s, count=1)
        s = STICKY_RE.sub(chrome.sticky(old, lang, yacht) + "\n", s, count=1)
        s = MODAL_RE.sub(chrome.modal(old, lang) + "\n", s, count=1)
    # --- decorative images: alt="" needs role="presentation"
    s = re.sub(r'<img(?![^>]*role=)([^>]*?)alt=""', r'<img\1alt="" role="presentation"', s)
    # --- modal triggers never point at "#": give them the WhatsApp URL as the no-JS fallback
    wa = wa_for(old)
    s = re.sub(r'<a([^>]*?)href="#"([^>]*?)data-modal', lambda m: f'<a{m.group(1)}href="{wa}"{m.group(2)}data-modal', s)
    s = re.sub(r'<a([^>]*?)data-modal([^>]*?)href="#"', lambda m: f'<a{m.group(1)}data-modal{m.group(2)}href="{wa}"', s)
    # --- site-wide Organization (+ LocalBusiness unless the page already defines it, + WebSite on the home page)
    if "/#organization" not in s:
        defines_business = '"streetAddress"' in s
        s = s.replace("</head>", chrome.org_jsonld(include_business=not defines_business, website=(old == "index")) + "\n</head>", 1)
    s = strip_hub_crumb(s, old)
    if old != "index" and '"BreadcrumbList"' not in s:
        s = s.replace("</head>", chrome.breadcrumb_jsonld(ia.section_crumb(old)) + "\n</head>", 1)
    if old in PATCHES:
        s = PATCHES[old](s)
    if PAGES[old]["section"] in ("experiences", "destinations", "events") or old in ("boat-rental-miami",):
        s = patch_landing(old, s)
    if PAGES[old]["section"] == "guides" and old != "guides":
        s = patch_guide(old, s)
    return s


# ---------------------------------------------------------------- page-specific patches (idempotent)
STEPS_HTML = """<div class="myc-steps">
  <div class="myc-step"><div class="num">Step 1</div><h3>Call or WhatsApp</h3><p>Tell us your date, group size and the occasion. We answer 24/7 and check live availability while you&rsquo;re on the line.</p></div>
  <div class="myc-step"><div class="num">Step 2</div><h3>We match the yacht</h3><p>We recommend the right boat from our 9-vessel fleet for your group and budget &mdash; no platforms, no broker markup.</p></div>
  <div class="myc-step"><div class="num">Step 3</div><h3>Step aboard</h3><p>Meet us at our Miami River dock &mdash; about 10 minutes from Brickell and 15 from Miami Beach &mdash; and your captain takes it from there.</p></div>
</div>"""


def patch_index(s):
    if 'href="/destinations"' not in s:
        s = s.replace('<h2>Explore the Fleet &amp; Experiences</h2>',
                      '<h2>Explore the Fleet &amp; Experiences</h2>\n          <p>Choose by place on the <a href="/destinations">destinations</a> pages &mdash; the sandbar, Star Island, Miami Beach, South Beach and Brickell &mdash; or by date on the <a href="/events">Miami event weeks</a> pages. Questions first? The <a href="/faq">FAQ</a> answers the ones we hear most, and <a href="/book">booking</a> takes one message.</p>', 1)
    if "TODO(owner): reviews" not in s:
        s = s.replace('<section class="testimonial-section">', '<!-- TODO(owner): reviews — the testimonials below predate this rebuild; confirm they are real guests, or replace with Google reviews / a Google Business Profile link. Never fabricate reviews or ratings. -->\n      <section class="testimonial-section">', 1)
    return s


def patch_services(s):
    if 'class="myc-cards"' not in s:
        s = s.replace('<h2>Sandbar &amp; Stiltsville day trips</h2>',
                      '<h2>Choose by destination</h2>\n<p>Prefer to pick the place first? The <a href="/destinations">destinations</a> pages cover the <a href="/destinations/sandbar-yacht-charter-miami">sandbar</a>, <a href="/destinations/star-island-boat-tour-miami">Star Island</a>, and the easiest way to the dock from <a href="/destinations/yacht-rental-miami-beach">Miami Beach</a>, <a href="/destinations/south-beach-yacht-rental">South Beach</a> and <a href="/destinations/yacht-rental-brickell">Brickell</a>.</p>\n\n<h2>The yachts groups book most</h2>\n' + chrome.cards(["isabella", "azimut-lchaim", "deep-blue", "maxum"]) + '\n<p style="margin-top:16px">Compare all nine on the <a href="/yachts">fleet page</a> or the <a href="/prices">price guide</a>.</p>\n\n<h2>Sandbar &amp; Stiltsville day trips</h2>', 1)
    s = s.replace('<h2 id="events">Miami events on a yacht</h2>\n<p>The big weeks on the Miami calendar are the best weeks to be on the water, and we charge the same prices every week of the year. Each page below has the dates and how a 4-hour charter fits around them.</p>',
                  '<h2 id="events">Miami events on a yacht</h2>\n<p>The big weeks on the Miami calendar are the best weeks to be on the water, and we charge the same prices every week of the year. Each page below has the dates and how a 4-hour charter fits around them &mdash; or see <a href="/events">all event weeks</a>.</p>', 1)
    return s


def patch_guides_hub(s):
    if '"@type": "ItemList"' not in s:
        items = [(PAGES[g]["label"], ia.abs_url(g)) for g, _ in ia.GUIDES]
        s = s.replace("</head>", chrome.jsonld({"@context": "https://schema.org", "@type": "ItemList", "name": "Miami yacht charter guides",
                                               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": u} for i, (n, u) in enumerate(items)]}) + "\n</head>", 1)
    return s


def patch_about(s):
    if "How booking works" not in s:
        block = ('      <section class="myc-section myc-on-light" id="how-booking-works">\n        <div class="myc-wrap myc-prose" style="max-width:980px">\n'
                 '          <h2>How booking works</h2>\n          ' + STEPS_HTML + '\n'
                 '          <p>Every charter is 4 hours with a licensed captain and crew, the prices are the same on every date of the year, and we book in English and Spanish. See the <a href="/faq">FAQ</a> for the rest.</p>\n'
                 '          <!-- TODO(owner): team and story section — names, roles, years on the water, a photo of the crew. Nothing is published here until supplied. -->\n'
                 '        </div>\n      </section>\n')
        s = s.replace('      <section class="about-feature-photo-section"', block + '      <section class="about-feature-photo-section"', 1)
    return s


def _retag(s, old_tag, cls, new_tag):
    """<h4 class="cls" ...>text</h4> -> <new_tag class="cls" ...>text</new_tag> (same class, so the CSS look is unchanged)."""
    return re.sub(r'<%s(\s[^>]*class="%s[^"]*"[^>]*)>(.*?)</%s>' % (old_tag, cls, old_tag), r'<%s\1>\2</%s>' % (new_tag, new_tag), s, flags=re.S)


def _demote_hidden(s, section_class):
    """Headings inside a hidden legacy section become <p> so they no longer break the outline."""
    m = re.search(r'<section[^>]*class="%s"[^>]*hidden.*?</section>\s*</section>|<section[^>]*class="%s"[^>]*hidden.*?</section>' % (section_class, section_class), s, re.S)
    if not m:
        return s
    blk = re.sub(r'<h[1-6](\s|>)', r'<p\1', m.group(0))
    blk = re.sub(r'</h[1-6]>', '</p>', blk)
    return s[:m.start()] + blk + s[m.end():]


def patch_index_headings(s):
    s = _retag(s, "h3", "home-about-title", "h2")
    s = _retag(s, "h4", "home-fleet-title", "div")
    s = _retag(s, "h4", "home-benefits-card-title", "h3")
    s = _retag(s, "h4", "testimonial-subtitle", "h3")
    s = _retag(s, "h5", "testimonial-author-name", "p")
    s = _retag(s, "h5", "overview-text", "p")
    return patch_index(s)


def patch_about_headings(s):
    s = _demote_hidden(s, "about-legacy-content")
    s = _demote_hidden(s, "about-wrapper-section")
    return patch_about(s)


def patch_contact(s):
    s = _demote_hidden(s, "contact-details-section-legacy")
    s = re.sub(r'<h5(\s[^>]*)?>(Easy to reach|When you book|On the day)</h5>', lambda m: f'<h3{m.group(1) or ""}>{m.group(2)}</h3>', s)  # inline styles keep the look
    return s


PATCHES = {"index": patch_index_headings, "services": patch_services, "guides": patch_guides_hub, "about": patch_about_headings, "contact": patch_contact}

GUIDE_FOR = {"destinations": "miami-sandbar-guide", "events": "best-time-yacht-charter-miami", "celebrations": "what-to-bring-yacht-charter-miami",
             "romance": "best-time-yacht-charter-miami", "groups": "what-to-bring-yacht-charter-miami", "days": "boating-license-miami-boat-rental"}
GUIDE_LABEL = {"miami-sandbar-guide": "The Miami sandbar guide", "best-time-yacht-charter-miami": "Best time for a Miami yacht charter",
               "what-to-bring-yacht-charter-miami": "What to bring on a yacht charter", "boating-license-miami-boat-rental": "Do you need a boating license?"}
EXP_DEFAULT = ["private-sunset-cruise-miami", "yacht-party-miami", "birthday-yacht-party-miami", "sandbar-yacht-charter-miami"]
EXP_LABEL = {"private-sunset-cruise-miami": "Private sunset cruise", "yacht-party-miami": "Yacht parties", "birthday-yacht-party-miami": "Birthday yacht parties",
             "sandbar-yacht-charter-miami": "Sandbar charter"}
RELATED_RE = re.compile(r'(<div class="myc-related"><h2>[^<]*</h2><ul>)(.*?)(</ul></div>)', re.S)


def _related_links(block):
    return re.findall(r'href="([^"]+)"', block)


def patch_landing(old, s):
    p = PAGES[old]
    if p["lang"] != "en":
        return s
    # recommended yachts: cards for the first three boats of the page's own table
    if 'class="myc-cards"' not in s:
        m = re.search(r'<div class="myc-table-wrap"><table class="myc-table">.*?</table></div>', s, re.S)
        if m:
            slugs = re.findall(r'href="/yachts/([a-z0-9-]+)"', m.group(0))
            olds = [ia.FLEET_BY_SLUG[x]["old"] for x in slugs if x in ia.FLEET_BY_SLUG][:3]
            if olds:
                s = s[:m.end()] + "\n" + chrome.cards(olds) + s[m.end():]
    # related block: >= 2 experiences + 1 guide
    m = RELATED_RE.search(s)
    if m:
        links = _related_links(m.group(2))
        exp = [l for l in links if l.startswith("/experiences/") or l.startswith("/destinations/")]
        guides = [l for l in links if l.startswith("/guides/")]
        add = ""
        need = 2 - len(exp)
        for e in EXP_DEFAULT:
            if need <= 0:
                break
            u = ia.url_of(e)
            if u in links or e == old:
                continue
            add += f'<li><a href="{u}">{EXP_LABEL[e]}</a></li>'
            need -= 1
        if not guides:
            g = GUIDE_FOR.get(p["section"] if p["section"] != "experiences" else (p["group"] or "days"), "what-to-bring-yacht-charter-miami")
            add += f'<li><a href="{ia.url_of(g)}">{GUIDE_LABEL[g]}</a></li>'
        if add:
            s = s[:m.start(3)] + add + s[m.start(3):]
    return s


def patch_guide(old, s):
    """Every guide links to at least 2 yachts and 2 experiences with descriptive anchors."""
    m = RELATED_RE.search(s)
    if not m:
        return s
    links = _related_links(m.group(2))
    body_links = re.findall(r'href="(/yachts/[a-z0-9-]+|/experiences/[a-z0-9-]+|/destinations/[a-z0-9-]+)"', s)
    yachts = {l for l in body_links if l.startswith("/yachts/")}
    exps = {l for l in body_links if not l.startswith("/yachts/")}
    add = ""
    for b in ("isabella", "deep-blue", "maxum"):
        if len(yachts) >= 2:
            break
        u = ia.url_of(b)
        if u not in yachts:
            add += f'<li><a href="{u}">The {ia.FLEET_BY_OLD[b]["name"]}</a></li>'
            yachts.add(u)
    for e in EXP_DEFAULT:
        if len(exps) >= 2:
            break
        u = ia.url_of(e)
        if u not in exps:
            add += f'<li><a href="{u}">{EXP_LABEL[e]}</a></li>'
            exps.add(u)
    if add:
        s = s[:m.start(3)] + add + s[m.start(3):]
    return s


def write_vercel():
    vj = json.loads((REPO / "vercel.json").read_text(encoding="utf-8"))
    r = []
    def add(src, dst, code=301):
        r.append({"source": src, "destination": dst, "statusCode": code})
    # Webflow template artifacts (both spellings) and legacy aliases
    add("/utility/:path*", "/")
    add("/detail_:name(category|guest|length|locations|price|services|type|yacht).html", "/yachts")
    add("/detail_:name(category|guest|length|locations|price|services|type|yacht)", "/yachts")
    add("/logo-preview.html", "/"); add("/logo-preview", "/")
    add("/yacht-details.html", "/yachts"); add("/yacht-details", "/yachts")
    add("/index.html", "/")
    legacy = {
        "/bachelorette-yacht-miami": "bachelorette-yacht-party-miami", "/yacht-parties-miami": "yacht-party-miami",
        "/corporate-yacht-miami": "corporate-yacht-charter-miami", "/boat-tours-miami": "sandbar-yacht-charter-miami",
        "/yacht-catering-miami": "services", "/blog": "guides", "/detail_blog": "guides",
        "/blog/how-much-does-yacht-rental-miami-cost": "miami-yacht-rental-prices", "/blog/how-to-plan-a-yacht-party-miami": "yacht-party-miami",
        "/blog/miami-bachelorette-yacht-party": "bachelorette-yacht-party-miami", "/blog/best-places-to-anchor-biscayne-bay": "miami-sandbar-guide",
        "/blog/miami-yacht-charter-vs-boat-rental": "yacht", "/acgua-alberti": "deep-blue",
    }
    for src, tgt in legacy.items():
        add(src + ".html", PAGES[tgt]["url"]); add(src, PAGES[tgt]["url"])
    add("/pay/acgua-alberti.html", "/pay/deep-blue"); add("/pay/acgua-alberti-deposit-1000.html", "/pay/deep-blue-deposit-1000")
    # every page: old .html and old extensionless slug -> final URL
    for old, p in PAGES.items():
        if p["new"] or old in ("index", "404"):
            continue
        add(f"/{old}.html", p["url"])
        if p["url"] != f"/{old}":
            add(f"/{old}", p["url"])
    add("/es", PAGES["alquiler-de-yates-miami"]["url"]); add("/pt", PAGES["aluguel-de-iate-em-miami"]["url"])
    vj["cleanUrls"] = True
    vj["trailingSlash"] = False
    vj["redirects"] = r
    return json.dumps(vj, indent=2, ensure_ascii=False) + "\n"


def write_robots():
    return """User-agent: *
Allow: /

# Block Webflow template artifacts that should not be indexed
Disallow: /search.html
Disallow: /search
Disallow: /detail_category.html
Disallow: /detail_guest.html
Disallow: /detail_length.html
Disallow: /detail_locations.html
Disallow: /detail_price.html
Disallow: /detail_services.html
Disallow: /detail_type.html
Disallow: /detail_yacht.html
Disallow: /detail_
Disallow: /utility/
Disallow: /401.html
Disallow: /401
Disallow: /logo-preview.html
Disallow: /logo-preview

# Private customer payment pages (sent 1:1, never indexed)
Disallow: /pay/

# AI crawlers (allowed for citation/discoverability; same exclusions as above)
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: PerplexityBot
User-agent: ClaudeBot
User-agent: Google-Extended
Allow: /

# Block Webflow template artifacts that should not be indexed
Disallow: /search.html
Disallow: /search
Disallow: /detail_category.html
Disallow: /detail_guest.html
Disallow: /detail_length.html
Disallow: /detail_locations.html
Disallow: /detail_price.html
Disallow: /detail_services.html
Disallow: /detail_type.html
Disallow: /detail_yacht.html
Disallow: /detail_
Disallow: /utility/
Disallow: /401.html
Disallow: /401
Disallow: /logo-preview.html
Disallow: /logo-preview

# Private customer payment pages (sent 1:1, never indexed)
Disallow: /pay/

Sitemap: https://miamiyachtcollective.com/sitemap.xml
"""


def write_sitemap():
    """Final 200 URLs only; noindex drafts excluded; hreflang alternates where a translation exists."""
    clusters = [{k: ia.abs_url(v) for k, v in c.items()} for c in ia.TRANSLATIONS.values()]
    alts = {}
    for c in clusters:
        for u in c.values():
            alts[u] = c
    order = ["index", "yacht"] + [b["old"] for b in FLEET] + ["services"] + [s for s, _, _ in ia.EXPERIENCES] + ["boat-rental-miami"] + \
            ["destinations"] + [s for s, _, _ in ia.DESTINATIONS] + ["events"] + [s for s, _ in ia.EVENTS] + \
            ["miami-yacht-rental-prices", "guides"] + [s for s, _ in ia.GUIDES] + ["faq", "gallery", "about", "contact", "booking",
            "alquiler-de-yates-miami", "fiesta-en-yate-miami", "aluguel-de-iate-em-miami"]
    seen = set()
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for old in order:
        if old in ia.NOINDEX or old in seen:
            continue
        seen.add(old)
        u = ia.abs_url(old)
        out.append(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>")
        if u in alts:
            for code, uu in alts[u].items():
                out.append(f'    <xhtml:link rel="alternate" hreflang="{code}" href="{uu}"/>')
            out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{alts[u]["en"]}"/>')
        out.append("  </url>")
    out.append("</urlset>\n")
    missing = [k for k in PAGES if k not in seen and k not in ia.NOINDEX]
    assert not missing, f"sitemap missing {missing}"
    return "\n".join(out)


def write_llms():
    s = (REPO / "llms.txt").read_text(encoding="utf-8")
    s = rewrite_links(s)
    s = s.replace("- Fleet listing: https://miamiyachtcollective.com/yachts",
                  "- Fleet listing (filter by size and budget): https://miamiyachtcollective.com/yachts")
    if "/destinations" not in s:
        s = s.replace("### Guides", "### Hubs\n\n- Destinations (sandbar, Star Island, Miami Beach, South Beach, Brickell): https://miamiyachtcollective.com/destinations\n- Miami event weeks (Art Basel, New Year's Eve, spring break, Grand Prix): https://miamiyachtcollective.com/events\n- Frequently asked questions: https://miamiyachtcollective.com/faq\n\n### Guides")
    return s


def main():
    report = []
    # 1. legacy pages -> transformed at their new path
    for old, p in PAGES.items():
        if old in NEW or old in REBUILT or old in LEAVE:
            continue
        src = REPO / f"{old}.html"
        dst = REPO / p["file"]
        if src.exists():
            s = src.read_text(encoding="utf-8")
            new = transform(old, s)
            report.append(f"migrate  {old}.html -> {p['file']}")
            if WRITE:
                if str(src) != str(dst):
                    git_mv(f"{old}.html", p["file"])
                dst.write_text(new, encoding="utf-8")
        elif dst.exists():
            s = dst.read_text(encoding="utf-8")
            new = transform(old, s)
            if new != s:
                report.append(f"re-link  {p['file']}")
                if WRITE:
                    dst.write_text(new, encoding="utf-8")
        else:
            report.append(f"MISSING  {old}")
    # 2. share cards follow their page
    for old, new in ia.OG_RENAMES.items():
        a, b = REPO / f"photos/og/{old}.jpg", REPO / f"photos/og/{new}.jpg"
        if a.exists() and not b.exists():
            report.append(f"og       {old}.jpg -> {new}.jpg")
            if WRITE:
                git_mv(f"photos/og/{old}.jpg", f"photos/og/{new}.jpg")
    # 3. legacy sources of rebuilt pages are removed once build_site.py has produced the new file
    for old in REBUILT:
        src = REPO / f"{old}.html"
        dst = REPO / PAGES[old]["file"]
        if src.exists() and dst.exists() and src.resolve() != dst.resolve():
            report.append(f"remove   {old}.html (rebuilt as {PAGES[old]['file']})")
            if WRITE:
                sh("git", "rm", "-q", f"{old}.html")
    # 4. config + text files
    if WRITE:
        (REPO / "vercel.json").write_text(write_vercel(), encoding="utf-8")
        (REPO / "robots.txt").write_text(write_robots(), encoding="utf-8")
        (REPO / "llms.txt").write_text(write_llms(), encoding="utf-8")
        if all((REPO / PAGES[k]["file"]).exists() for k in PAGES if k not in ia.NOINDEX):
            (REPO / "sitemap.xml").write_text(write_sitemap(), encoding="utf-8")
            report.append("sitemap  written")
        else:
            report.append("sitemap  skipped (run build_site.py first, then re-run)")
        # theme CSS block
        css_path = REPO / "css/myc-theme.css"
        css = css_path.read_text(encoding="utf-8")
        block = (Path(__file__).parent / "ia_block.css").read_text(encoding="utf-8")
        # conservative minify: drop comments and collapse whitespace (the readable source stays in ia_block.css)
        block = re.sub(r"/\*.*?\*/", "", block, flags=re.S)
        block = re.sub(r"\s+", " ", block).strip()
        block = re.sub(r"\s*([{};,>])\s*", r"\1", block)
        block = "/* Source: seo-tools/ia_block.css (minified on apply by ia_migrate.py) */\n" + block
        start, end = "/* === IA 2026-10-28 START === */", "/* === IA 2026-10-28 END === */"
        if start in css:
            css = css[:css.index(start)] + start + "\n" + block + "\n" + end + css[css.index(end) + len(end):]
        else:
            css = css.rstrip() + "\n\n" + start + "\n" + block + "\n" + end + "\n"
        css_path.write_text(css, encoding="utf-8")
        report.append("css      theme block applied")
        pages_css = (Path(__file__).parent / "ia_pages.css").read_text(encoding="utf-8")
        pages_min = re.sub(r"/\*.*?\*/", "", pages_css, flags=re.S)
        pages_min = re.sub(r"\s+", " ", pages_min).strip()
        pages_min = re.sub(r"\s*([{};,>])\s*", r"\1", pages_min)
        (REPO / "css/myc-pages.css").write_text("/* Source: seo-tools/ia_pages.css (minified on apply by ia_migrate.py) */\n" + pages_min + "\n", encoding="utf-8")
        report.append("css      myc-pages.css written")
    print("\n".join(report))
    print(f"{'WROTE' if WRITE else 'DRY RUN'}: {len(report)} actions")


if __name__ == "__main__":
    main()
