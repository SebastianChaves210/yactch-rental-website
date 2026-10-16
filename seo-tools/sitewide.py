# -*- coding: utf-8 -*-
"""Sitewide changes for the Oct 2026 tourist-SEO branch. Idempotent: safe to re-run."""
import json, re, sys
from pathlib import Path
from urllib.parse import quote
sys.path.insert(0, str(Path(__file__).parent))
from pages_spec import PAGES, BOATS

REPO = Path(sys.argv[1])
SITE = "https://miamiyachtcollective.com/"
NEW = [p["slug"] for p in PAGES]
LANG = {p["slug"]: p["lang"] for p in PAGES}
LANG["alquiler-de-yates-miami"] = "es"

def rd(n): return (REPO / n).read_text(encoding="utf-8")
def wr(n, s): (REPO / n).write_text(s, encoding="utf-8")
def lang_of(n): return LANG.get(n[:-5], "en")

ALL = sorted(p.name for p in REPO.glob("*.html") if p.name != "logo-preview.html")
INDEXABLE = [l.split(SITE)[1] or "index.html" for l in re.findall(r"<loc>([^<]+)</loc>", rd("sitemap.xml"))]
INDEXABLE += [s + ".html" for s in NEW if s + ".html" not in INDEXABLE]

# ------------------------------------------------------------------ 1. fonts: non-blocking
FONT_RE = re.compile(r'<link href="(https://fonts\.googleapis\.com/css2\?[^"]+)" rel="stylesheet">')
def fix_fonts(s):
    m = FONT_RE.search(s)
    if not m: return s
    u = m.group(1)
    return s.replace(m.group(0), f'<link rel="preload" as="style" href="{u}" onload="this.onload=null;this.rel=\'stylesheet\'">\n  <noscript><link href="{u}" rel="stylesheet"></noscript>')

# ------------------------------------------------------------------ 2. sticky mobile CTA
STICKY = {
    "en": ("Call", "WhatsApp", "Book now"),
    "es": ("Llamar", "WhatsApp", "Reservar"),
    "pt-BR": ("Ligar", "WhatsApp", "Reservar"),
}
def add_sticky(s, lang):
    if 'class="myc-sticky-cta"' in s or 'class="modal-backdrop"' not in s: return s
    c, w, lab = STICKY[lang]
    bar = f'''<div class="myc-sticky-cta" aria-label="{lab}">
  <a href="tel:7876645040" class="myc-sticky-call">{c}</a>
  <a href="https://wa.me/17876645040" target="_blank" rel="noopener" class="myc-sticky-wa">{w}</a>
</div>
'''
    return s.replace('<div class="modal-backdrop"', bar + '<div class="modal-backdrop"', 1)

# ------------------------------------------------------------------ 3. WhatsApp prefill
DEFAULT_WA = "Hi! I'd like to book a private yacht in Miami. My date:"
WA = {
    "index": DEFAULT_WA, "booking": DEFAULT_WA, "contact": DEFAULT_WA, "about": DEFAULT_WA, "gallery": DEFAULT_WA,
    "guides": DEFAULT_WA, "404": DEFAULT_WA, "401": DEFAULT_WA,
    "yacht": "Hi! I'd like to book one of your yachts. My date:",
    "services": "Hi! I'd like to plan a yacht experience in Miami. My date:",
    "yacht-party-miami": "Hi! I'd like to book a private yacht party in Miami. My date and group size:",
    "birthday-yacht-party-miami": "Hi! I'm planning a birthday yacht party in Miami. My date and group size:",
    "bachelorette-yacht-party-miami": "Hi! I'm planning a bachelorette yacht party in Miami. My date and group size:",
    "bachelor-party-yacht-miami": "Hi! I'm planning a bachelor party yacht charter in Miami. My date and group size:",
    "private-sunset-cruise-miami": "Hi! I'd like to book a private sunset cruise in Miami. My date:",
    "miami-yacht-rental-prices": "Hi! I saw your prices page and I'd like a quote. My date:",
    "corporate-yacht-charter-miami": "Hi! I'd like to plan a corporate yacht charter in Miami. Date and group size:",
    "sandbar-yacht-charter-miami": "Hi! I'd like to book a sandbar yacht charter in Miami. My date:",
    "boat-rental-miami": "Hi! I'd like to rent a boat with captain in Miami. My date:",
    "party-boat-rental-miami": "Hi! I'd like to rent a party boat in Miami. My date and group size:",
    "proposal-yacht-charter-miami": "Hi! I'm planning a proposal or anniversary cruise in Miami. My date:",
    "yacht-rental-miami-beach": "Hi! I'm staying in Miami Beach and I'd like to rent a yacht. My date:",
    "yacht-rental-brickell": "Hi! I'm in Brickell/Downtown and I'd like to rent a yacht. My date:",
    "alquiler-de-yates-miami": "¡Hola! Quiero reservar un yate privado en Miami. Mi fecha:",
    "boating-license-miami-boat-rental": DEFAULT_WA, "what-to-bring-yacht-charter-miami": DEFAULT_WA,
    "miami-sandbar-guide": DEFAULT_WA, "best-time-yacht-charter-miami": DEFAULT_WA,
}
for b, (name, _) in BOATS.items():
    WA[b] = f"Hi! I'm interested in the {name}. My date:"
WA.update(json.loads((Path(__file__).parent / "wa_new_pages.json").read_text(encoding="utf-8")))
WA_RE = re.compile(r'href="https://wa\.me/17876645040(?:\?text=[^"]*)?"')
def prefill(s, slug):
    msg = WA.get(slug, DEFAULT_WA)
    return WA_RE.sub(f'href="https://wa.me/17876645040?text={quote(msg, safe="")}"', s)

# ------------------------------------------------------------------ 4. hreflang
CLUSTERS = [
    {"en": "", "es": "alquiler-de-yates-miami.html", "pt-BR": "aluguel-de-iate-em-miami.html"},
    {"en": "yacht-party-miami.html", "es": "fiesta-en-yate-miami.html"},
]
def add_hreflang(s, name):
    if 'rel="alternate" hreflang=' in s: return s
    key = "" if name == "index.html" else name
    for c in CLUSTERS:
        if key in c.values():
            tags = "".join(f'\n  <link rel="alternate" hreflang="{l}" href="{SITE}{u}">' for l, u in c.items())
            tags += f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}{c["en"]}">'
            return re.sub(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + tags, s, count=1)
    return s

# ------------------------------------------------------------------ 5. related-experiences block on existing pages
RELATED = {
    "yacht-party-miami": [("party-boat-rental-miami.html", "Party boat rental"), ("birthday-yacht-party-miami.html", "Birthday parties"), ("spring-break-yacht-miami.html", "Spring break yachts"), ("new-years-eve-yacht-miami.html", "New Year's Eve")],
    "birthday-yacht-party-miami": [("quinceanera-yacht-party-miami.html", "Quinceañera yacht parties"), ("yacht-party-miami.html", "Yacht parties"), ("family-yacht-charter-miami.html", "Family charters"), ("sandbar-yacht-charter-miami.html", "Sandbar charter")],
    "bachelorette-yacht-party-miami": [("bachelor-party-yacht-miami.html", "Bachelor parties"), ("spring-break-yacht-miami.html", "Spring break yachts"), ("isabella.html", "48' Isabella with jet ski"), ("yacht-party-miami.html", "Yacht parties")],
    "bachelor-party-yacht-miami": [("bachelorette-yacht-party-miami.html", "Bachelorette parties"), ("spring-break-yacht-miami.html", "Spring break yachts"), ("party-boat-rental-miami.html", "Party boat rental"), ("isabella.html", "48' Isabella with jet ski")],
    "private-sunset-cruise-miami": [("proposal-yacht-charter-miami.html", "Proposals and anniversaries"), ("star-island-boat-tour-miami.html", "Star Island boat tour"), ("new-years-eve-yacht-miami.html", "New Year's Eve"), ("wedding-yacht-charter-miami.html", "Weddings on board")],
    "miami-yacht-rental-prices": [("boat-rental-miami.html", "Boat rental with captain"), ("yacht.html", "Our fleet"), ("star-island-boat-tour-miami.html", "Star Island boat tour"), ("south-beach-yacht-rental.html", "South Beach yacht rental")],
    "corporate-yacht-charter-miami": [("art-basel-yacht-charter-miami.html", "Art Basel week"), ("miami-grand-prix-yacht-charter.html", "Grand Prix weekend"), ("deep-blue.html", "90' Deep Blue with jacuzzi"), ("yacht-photoshoot-miami.html", "Photo and video shoots")],
    "sandbar-yacht-charter-miami": [("miami-sandbar-guide.html", "Miami sandbar guide"), ("family-yacht-charter-miami.html", "Family charters"), ("star-island-boat-tour-miami.html", "Star Island boat tour"), ("spring-break-yacht-miami.html", "Spring break yachts")],
    "boat-rental-miami": [("party-boat-rental-miami.html", "Party boat rental"), ("family-yacht-charter-miami.html", "Family charters"), ("yamaha-255xd.html", "25' Yamaha 255XD"), ("axopar-brabus.html", "28' Axopar Brabus")],
    "party-boat-rental-miami": [("yacht-party-miami.html", "Yacht parties"), ("spring-break-yacht-miami.html", "Spring break yachts"), ("bachelor-party-yacht-miami.html", "Bachelor parties"), ("sandbar-yacht-charter-miami.html", "Sandbar charter")],
    "proposal-yacht-charter-miami": [("wedding-yacht-charter-miami.html", "Weddings on board"), ("private-sunset-cruise-miami.html", "Private sunset cruise"), ("yacht-photoshoot-miami.html", "Photo and video shoots"), ("star-island-boat-tour-miami.html", "Star Island boat tour")],
    "yacht-rental-miami-beach": [("south-beach-yacht-rental.html", "South Beach yacht rental"), ("star-island-boat-tour-miami.html", "Star Island boat tour"), ("yacht-rental-brickell.html", "Brickell and Downtown"), ("private-sunset-cruise-miami.html", "Private sunset cruise")],
    "yacht-rental-brickell": [("yacht-charter-before-cruise-miami.html", "Before or after your cruise"), ("yacht-rental-miami-beach.html", "Miami Beach yacht rental"), ("star-island-boat-tour-miami.html", "Star Island boat tour"), ("corporate-yacht-charter-miami.html", "Corporate charters")],
    "alquiler-de-yates-miami": [("fiesta-en-yate-miami.html", "Fiestas en yate"), ("quinceanera-yacht-party-miami.html", "Quinceañeras en yate"), ("aluguel-de-iate-em-miami.html", "Em português"), ("miami-yacht-rental-prices.html", "Precios (English)")],
    "boating-license-miami-boat-rental": [("boat-rental-miami.html", "Boat rental with captain"), ("family-yacht-charter-miami.html", "Family charters"), ("yacht-charter-before-cruise-miami.html", "Before or after your cruise"), ("miami-yacht-rental-prices.html", "Rental prices")],
    "what-to-bring-yacht-charter-miami": [("family-yacht-charter-miami.html", "Family charters"), ("sandbar-yacht-charter-miami.html", "Sandbar charter"), ("yacht-photoshoot-miami.html", "Photo and video shoots"), ("best-time-yacht-charter-miami.html", "Best time to charter")],
    "miami-sandbar-guide": [("sandbar-yacht-charter-miami.html", "Sandbar charter"), ("family-yacht-charter-miami.html", "Family charters"), ("star-island-boat-tour-miami.html", "Star Island boat tour"), ("spring-break-yacht-miami.html", "Spring break yachts")],
    "best-time-yacht-charter-miami": [("private-sunset-cruise-miami.html", "Private sunset cruise"), ("art-basel-yacht-charter-miami.html", "Art Basel week"), ("spring-break-yacht-miami.html", "Spring break and Music Week"), ("new-years-eve-yacht-miami.html", "New Year's Eve")],
}
def add_related(s, slug):
    if slug not in RELATED or 'class="myc-related"' in s: return s
    h = {"es": "Más experiencias"}.get(lang_of(slug + ".html"), "Related experiences")
    block = f'<div class="myc-related"><h2>{h}</h2><ul>' + "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in RELATED[slug]) + "</ul></div>\n\n"
    assert s.count('<div class="myc-cta-band">') == 1, slug
    return s.replace('<div class="myc-cta-band">', block + '<div class="myc-cta-band">', 1)

# ------------------------------------------------------------------ 6. footer links (all pages)
FOOT = {
    "en": dict(anchor='class="footer-nav-link">Rental Prices</a>', links=[("star-island-boat-tour-miami.html", "Star Island Tours"), ("wedding-yacht-charter-miami.html", "Weddings"), ("family-yacht-charter-miami.html", "Family Charters"), ("services.html#events", "Miami Events")],
               lang_anchor='<a href="alquiler-de-yates-miami.html" lang="es" hreflang="es" class="footer-nav-link">Español</a>', lang_add='<a href="aluguel-de-iate-em-miami.html" lang="pt-BR" hreflang="pt-BR" class="footer-nav-link">Português</a>'),
    "es": dict(anchor='class="footer-nav-link">Precios</a>', links=[("star-island-boat-tour-miami.html", "Tour por Star Island"), ("wedding-yacht-charter-miami.html", "Bodas"), ("family-yacht-charter-miami.html", "Familias"), ("fiesta-en-yate-miami.html", "Fiestas en yate (ES)")],
               lang_anchor='<a href="index.html" lang="en" hreflang="en" class="footer-nav-link">English</a>', lang_add='<a href="aluguel-de-iate-em-miami.html" lang="pt-BR" hreflang="pt-BR" class="footer-nav-link">Português</a>'),
    "pt-BR": dict(anchor='class="footer-nav-link">Preços</a>', links=[("star-island-boat-tour-miami.html", "Tour por Star Island"), ("wedding-yacht-charter-miami.html", "Casamentos"), ("family-yacht-charter-miami.html", "Famílias"), ("services.html#events", "Eventos em Miami")],
                  lang_anchor=None, lang_add=None),
}
def add_footer(s, lang):
    f = FOOT[lang]
    if 'star-island-boat-tour-miami.html" class="footer-nav-link"' not in s:
        i = s.find(f["anchor"])
        if i != -1:
            line_start = s.rfind("\n", 0, i) + 1
            indent = s[line_start:i][: len(s[line_start:i]) - len(s[line_start:i].lstrip())]
            ins = "".join(f'{indent}<a href="{u}" class="footer-nav-link">{t}</a>\n' for u, t in f["links"])
            s = s[:line_start] + ins + s[line_start:]
    if f["lang_anchor"] and f["lang_anchor"] in s and 'hreflang="pt-BR" class="footer-nav-link"' not in s:
        i = s.find(f["lang_anchor"]); line_start = s.rfind("\n", 0, i) + 1
        indent = s[line_start:i]
        s = s.replace(f["lang_anchor"], f["lang_anchor"] + "\n" + indent + f["lang_add"], 1)
    return s

# ------------------------------------------------------------------ 7. logo + poster
LOGO_OLD = 'src="images/main-boat-logo-transparent.png"'
def fix_logo(s):
    # only the header logo img (eager, class header-brand-logo); schema/og keep the PNG
    return re.sub(r'<img ([^>]*?)src="images/main-boat-logo-transparent\.png"([^>]*class="header-brand-logo")',
                  lambda m: "<img " + re.sub(r'width="512" height="512" ', 'width="420" height="420" ', m.group(1)) + 'src="images/main-boat-logo-420.webp"' + m.group(2), s)

# ------------------------------------------------------------------ run
for name in ALL:
    s = rd(name); o = s; slug = name[:-5]; lang = lang_of(name)
    s = fix_fonts(s)
    s = add_sticky(s, lang)
    s = add_hreflang(s, name)
    s = add_related(s, slug)
    s = add_footer(s, lang)
    s = fix_logo(s)
    s = prefill(s, slug)
    if name == "index.html":
        s = s.replace("videos/Yacht-poster-00001.jpg", "videos/Yacht-poster-00001.webp")
    if s != o:
        wr(name, s)
print("pages touched")

# ------------------------------------------------------------------ 8. theme CSS
css = rd("css/myc-theme.css")
if ".myc-sticky-cta" not in css:
    css += """

/* ---- Oct 2026: sticky mobile Call / WhatsApp bar + related-links block ---- */
.myc-sticky-cta { display: none; }
body .myc-related { margin: 34px 0 10px; padding: 22px 24px; border: 1px solid var(--myc-hairline); border-radius: 16px; background: var(--myc-paper); }
body .myc-related h2 { font-size: 22px; margin: 0 0 12px; }
body .myc-related ul { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 10px; }
body .myc-related li { margin: 0; }
body .myc-related a { display: inline-block; padding: 9px 16px; border-radius: 999px; border: 1px solid var(--myc-gold-deep); color: var(--myc-ink); text-decoration: none; font-weight: 600; font-size: 15px; }
body .myc-related a:hover { background: var(--myc-gold); color: var(--myc-ink-deep); }
@media (max-width: 767px) {
  .myc-sticky-cta { position: fixed; left: 0; right: 0; bottom: 0; z-index: 9000; display: flex; gap: 10px; padding: 10px 14px calc(10px + env(safe-area-inset-bottom)); background: rgba(8, 21, 36, 0.96); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); border-top: 1px solid rgba(194, 161, 95, 0.35); }
  .myc-sticky-cta a { flex: 1; text-align: center; padding: 14px 10px; border-radius: 999px; font-family: var(--myc-sans); font-weight: 700; font-size: 16px; letter-spacing: 0.01em; text-decoration: none; }
  .myc-sticky-cta .myc-sticky-call { background: var(--myc-gold); color: var(--myc-ink-deep); }
  .myc-sticky-cta .myc-sticky-wa { background: #25D366; color: #fff; }
  body { padding-bottom: 74px; }
  html .modal-backdrop { z-index: 9999; }
}
"""
    wr("css/myc-theme.css", css)
print("css done")

# ------------------------------------------------------------------ 9. tracking.js
wr("js/tracking.js", """/**
 * GA4 Event Tracking for Miami Yacht Collective
 * Tracks: modal_open, call_click, whatsapp_click (with cta_location: modal | sticky | inline)
 */
(function () {
  'use strict';

  function getPageName() {
    var path = window.location.pathname.replace(/\\/$/, '');
    if (!path || path === '') return 'home';
    return path.split('/').pop().replace('.html', '');
  }

  var pageName = getPageName();

  function send(name, el) {
    if (typeof gtag !== 'function') return;
    var loc = 'inline';
    if (el.classList.contains('modal-btn')) loc = 'modal';
    else if (el.closest && el.closest('.myc-sticky-cta')) loc = 'sticky';
    gtag('event', name, { page_name: pageName, cta_location: loc, transport_type: 'beacon' });
  }

  document.querySelectorAll('[data-modal]').forEach(function (el) {
    el.addEventListener('click', function () {
      if (typeof gtag === 'function') {
        gtag('event', 'modal_open', { page_name: pageName, transport_type: 'beacon' });
      }
    });
  });

  document.querySelectorAll('a[href^="tel:"]').forEach(function (el) {
    el.addEventListener('click', function () { send('call_click', el); });
  });

  document.querySelectorAll('a[href*="wa.me/"]').forEach(function (el) {
    el.addEventListener('click', function () { send('whatsapp_click', el); });
  });
})();
""")
print("tracking.js done")

# ------------------------------------------------------------------ 10. sitemap + vercel.json + robots untouched
lastmod = "2026-10-16"
urls = []
for n in INDEXABLE:
    urls.append(SITE if n == "index.html" else SITE + n)
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
alts = {}
for c in CLUSTERS:
    for l, u in c.items():
        alts[u] = c
for u in urls:
    key = u.replace(SITE, "")
    sm += f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
    if key in alts:
        for l, uu in alts[key].items():
            sm += f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{uu}"/>\n'
        sm += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{alts[key]["en"]}"/>\n'
    sm += "  </url>\n"
sm += "</urlset>\n"
wr("sitemap.xml", sm)
print("sitemap", len(urls), "urls")

vj = json.loads(rd("vercel.json"))
have = {r["source"] for r in vj["redirects"]}
for slug in NEW:
    if "/" + slug not in have:
        vj["redirects"].append({"source": "/" + slug, "destination": "/" + slug + ".html", "permanent": True})
wr("vercel.json", json.dumps(vj, indent=2) + "\n")
print("vercel.json redirects", len(vj["redirects"]))
