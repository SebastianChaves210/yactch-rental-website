# -*- coding: utf-8 -*-
"""Generate the Oct 2026 landing pages from sandbar-yacht-charter-miami.html."""
import json, re, sys, html as H
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pages_spec import PAGES, BOATS, BOATS_ES, BOATS_PT, P, SITE

REPO = Path(sys.argv[1])
TEMPLATE = (REPO / "sandbar-yacht-charter-miami.html").read_text(encoding="utf-8")

CHROME = {
    "es": [
        ('class="header-nav-link w-nav-link">Home<', 'class="header-nav-link w-nav-link">Inicio<'),
        ('class="header-nav-link w-nav-link">Yachts<', 'class="header-nav-link w-nav-link">Yates<'),
        ('class="header-nav-link w-nav-link">Experiences<', 'class="header-nav-link w-nav-link">Experiencias<'),
        ('class="header-nav-link w-nav-link">About<', 'class="header-nav-link w-nav-link">Nosotros<'),
        ('class="header-nav-link w-nav-link">Contact<', 'class="header-nav-link w-nav-link">Contacto<'),
        ('<div class="secondary-text">Book Now</div>', '<div class="secondary-text">Reservar</div>'),
        ('<h2 class="footer-desp">Let’s plan your private voyage now</h2>', '<h2 class="footer-desp">Planifiquemos su paseo privado</h2>'),
        ('<div class="secondary-text">Request Itinerary</div>', '<div class="secondary-text">Solicitar itinerario</div>'),
        ('<h5 class="footer-nav-title">Main Pages</h5>', '<h5 class="footer-nav-title">Páginas</h5>'),
        ('<h5 class="footer-nav-title">Experiences</h5>', '<h5 class="footer-nav-title">Experiencias</h5>'),
        ('<a href="index.html" class="footer-nav-link">Home</a>', '<a href="index.html" class="footer-nav-link">Inicio</a>'),
        ('<a href="about.html" class="footer-nav-link">About</a>', '<a href="about.html" class="footer-nav-link">Nosotros</a>'),
        ('<a href="services.html" aria-current="page" class="footer-nav-link w--current">Services</a>', '<a href="services.html" class="footer-nav-link">Servicios</a>'),
        ('<a href="booking.html" class="footer-nav-link">Book Now</a>', '<a href="booking.html" class="footer-nav-link">Reservar</a>'),
        ('<a href="guides.html" class="footer-nav-link">Guides</a>', '<a href="guides.html" class="footer-nav-link">Guías</a>'),
        ('<a href="alquiler-de-yates-miami.html" lang="es" hreflang="es" class="footer-nav-link">Español</a>', '<a href="index.html" lang="en" hreflang="en" class="footer-nav-link">English</a>'),
        ('<a href="contact.html" class="footer-nav-link">Contact</a>', '<a href="contact.html" class="footer-nav-link">Contacto</a>'),
        ('class="footer-nav-link">Yacht Parties<', 'class="footer-nav-link">Fiestas en yate<'),
        ('class="footer-nav-link">Birthday Parties<', 'class="footer-nav-link">Cumpleaños<'),
        ('class="footer-nav-link">Bachelorette Parties<', 'class="footer-nav-link">Despedidas de soltera<'),
        ('class="footer-nav-link">Sunset Cruises<', 'class="footer-nav-link">Paseos al atardecer<'),
        ('class="footer-nav-link">Corporate Charters<', 'class="footer-nav-link">Eventos de empresa<'),
        ('class="footer-nav-link">Sandbar Charters<', 'class="footer-nav-link">Días de sandbar<'),
        ('class="footer-nav-link">Boat Rentals<', 'class="footer-nav-link">Alquiler de lanchas<'),
        ('class="footer-nav-link">Bachelor Parties<', 'class="footer-nav-link">Despedidas de soltero<'),
        ('class="footer-nav-link">Proposals<', 'class="footer-nav-link">Propuestas de matrimonio<'),
        ('class="footer-nav-link">Rental Prices<', 'class="footer-nav-link">Precios<'),
        ('class="footer-nav-link">Our Fleet<', 'class="footer-nav-link">Nuestra flota<'),
        ('<div class="modal-heading" id="modalHeading">How Would You Like to Book?</div>', '<div class="modal-heading" id="modalHeading">¿Cómo prefiere reservar?</div>'),
        ("<p class=\"modal-subtext\">We'll confirm your booking right away!</p>", '<p class="modal-subtext">¡Confirmamos su reserva de inmediato!</p>'),
        ('class="modal-btn modal-btn-call">Call us at (787) 664-5040<', 'class="modal-btn modal-btn-call">Llamar al (787) 664-5040<'),
        ('class="modal-btn modal-btn-wa">WhatsApp Direct<', 'class="modal-btn modal-btn-wa">WhatsApp directo<'),
        ('aria-label="Close booking dialog"', 'aria-label="Cerrar"'),
    ],
    "pt-BR": [
        ('class="header-nav-link w-nav-link">Home<', 'class="header-nav-link w-nav-link">Início<'),
        ('class="header-nav-link w-nav-link">Yachts<', 'class="header-nav-link w-nav-link">Iates<'),
        ('class="header-nav-link w-nav-link">Experiences<', 'class="header-nav-link w-nav-link">Experiências<'),
        ('class="header-nav-link w-nav-link">About<', 'class="header-nav-link w-nav-link">Sobre<'),
        ('class="header-nav-link w-nav-link">Contact<', 'class="header-nav-link w-nav-link">Contato<'),
        ('<div class="secondary-text">Book Now</div>', '<div class="secondary-text">Reservar</div>'),
        ('<h2 class="footer-desp">Let’s plan your private voyage now</h2>', '<h2 class="footer-desp">Vamos planejar o seu passeio privativo</h2>'),
        ('<div class="secondary-text">Request Itinerary</div>', '<div class="secondary-text">Pedir roteiro</div>'),
        ('<h5 class="footer-nav-title">Main Pages</h5>', '<h5 class="footer-nav-title">Páginas</h5>'),
        ('<h5 class="footer-nav-title">Experiences</h5>', '<h5 class="footer-nav-title">Experiências</h5>'),
        ('<a href="index.html" class="footer-nav-link">Home</a>', '<a href="index.html" class="footer-nav-link">Início</a>'),
        ('<a href="about.html" class="footer-nav-link">About</a>', '<a href="about.html" class="footer-nav-link">Sobre</a>'),
        ('<a href="services.html" aria-current="page" class="footer-nav-link w--current">Services</a>', '<a href="services.html" class="footer-nav-link">Serviços</a>'),
        ('<a href="booking.html" class="footer-nav-link">Book Now</a>', '<a href="booking.html" class="footer-nav-link">Reservar</a>'),
        ('<a href="guides.html" class="footer-nav-link">Guides</a>', '<a href="guides.html" class="footer-nav-link">Guias</a>'),
        ('<a href="alquiler-de-yates-miami.html" lang="es" hreflang="es" class="footer-nav-link">Español</a>', '<a href="index.html" lang="en" hreflang="en" class="footer-nav-link">English</a>\n                    <a href="alquiler-de-yates-miami.html" lang="es" hreflang="es" class="footer-nav-link">Español</a>'),
        ('<a href="contact.html" class="footer-nav-link">Contact</a>', '<a href="contact.html" class="footer-nav-link">Contato</a>'),
        ('class="footer-nav-link">Yacht Parties<', 'class="footer-nav-link">Festas em iate<'),
        ('class="footer-nav-link">Birthday Parties<', 'class="footer-nav-link">Aniversários<'),
        ('class="footer-nav-link">Bachelorette Parties<', 'class="footer-nav-link">Despedidas de solteira<'),
        ('class="footer-nav-link">Sunset Cruises<', 'class="footer-nav-link">Pôr do sol<'),
        ('class="footer-nav-link">Corporate Charters<', 'class="footer-nav-link">Eventos corporativos<'),
        ('class="footer-nav-link">Sandbar Charters<', 'class="footer-nav-link">Dias de sandbar<'),
        ('class="footer-nav-link">Boat Rentals<', 'class="footer-nav-link">Aluguel de lanchas<'),
        ('class="footer-nav-link">Bachelor Parties<', 'class="footer-nav-link">Despedidas de solteiro<'),
        ('class="footer-nav-link">Proposals<', 'class="footer-nav-link">Pedidos de casamento<'),
        ('class="footer-nav-link">Rental Prices<', 'class="footer-nav-link">Preços<'),
        ('class="footer-nav-link">Our Fleet<', 'class="footer-nav-link">Nossa frota<'),
        ('<div class="modal-heading" id="modalHeading">How Would You Like to Book?</div>', '<div class="modal-heading" id="modalHeading">Como prefere reservar?</div>'),
        ("<p class=\"modal-subtext\">We'll confirm your booking right away!</p>", '<p class="modal-subtext">Confirmamos a sua reserva na hora!</p>'),
        ('class="modal-btn modal-btn-call">Call us at (787) 664-5040<', 'class="modal-btn modal-btn-call">Ligar para (787) 664-5040<'),
        ('class="modal-btn modal-btn-wa">WhatsApp Direct<', 'class="modal-btn modal-btn-wa">WhatsApp direto<'),
        ('aria-label="Close booking dialog"', 'aria-label="Fechar"'),
    ],
}

L = {
    "en": dict(home="Home", exp="Experiences", check="Check Availability", gal_h=None, tbl=("Yacht", "Starting price", "Best for"), faq="Frequently asked questions", related="Related experiences", call="Call (787) 664-5040", wa="WhatsApp Us"),
    "es": dict(home="Inicio", exp="Experiencias", check="Ver disponibilidad", gal_h=None, tbl=("Yate", "Precio desde", "Ideal para"), faq="Preguntas frecuentes", related="Más experiencias", call="Llamar al (787) 664-5040", wa="Escríbanos por WhatsApp"),
    "pt-BR": dict(home="Início", exp="Experiências", check="Ver disponibilidade", gal_h=None, tbl=("Iate", "Preço a partir de", "Ideal para"), faq="Perguntas frequentes", related="Veja também", call="Ligar para (787) 664-5040", wa="Fale pelo WhatsApp"),
}

from PIL import Image
def dims(rel):
    with Image.open(REPO / rel) as im:
        return im.size

def esc(s):  # attribute-safe
    return s.replace("&", "&amp;").replace('"', "&quot;")

def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=1, ensure_ascii=False) + '\n</script>'

def build(page):
    lang = page["lang"]; l = L[lang]
    boats = {"en": BOATS, "es": BOATS_ES, "pt-BR": BOATS_PT}[lang]
    url = SITE + page["slug"] + ".html"
    og = SITE + page["og"]
    title_txt = H.unescape(page["title"])
    desc = page["desc"]

    # --- head ---
    s = TEMPLATE
    s = s.replace('<html lang="en">', f'<html lang="{lang}">')
    s = re.sub(r"<title>.*?</title>", f"<title>{page['title']}</title>", s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{page["title"]}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(desc)}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s, count=1)
    s = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{og}">', s, count=1)
    s = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{page["title"]}">', s, count=1)
    s = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{esc(desc)}">', s, count=1)
    s = re.sub(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{og}">', s, count=1)
    if lang != "en":
        s = s.replace('<meta property="og:site_name" content="Miami Yacht Collective">', f'<meta property="og:site_name" content="Miami Yacht Collective">\n  <meta property="og:locale" content="{ {"es":"es_US","pt-BR":"pt_BR"}[lang] }">')

    # --- schema ---
    svc_name, svc_desc, price = page["service"]
    service = {"@context": "https://schema.org", "@type": "Service", "@id": url + "#service", "name": svc_name,
               "description": svc_desc, "url": url, "image": og,
               "provider": {"@type": "LocalBusiness", "@id": SITE + "#business"},
               "areaServed": [{"@type": "City", "name": "Miami"}, {"@type": "City", "name": "Miami Beach"}],
               "offers": {"@type": "Offer", "name": svc_name + " — 4-hour private charter", "price": price, "priceCurrency": "USD",
                          "priceSpecification": {"@type": "UnitPriceSpecification", "price": price, "priceCurrency": "USD", "unitText": "4 hours"},
                          "availability": "https://schema.org/InStock", "url": url}}
    if lang != "en":
        service["inLanguage"] = lang
    crumbs = [{"@type": "ListItem", "position": 1, "name": l["home"], "item": SITE}]
    if lang == "en":
        crumbs.append({"@type": "ListItem", "position": 2, "name": "Experiences", "item": SITE + "services.html"})
    crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": H.unescape(page["crumb"]), "item": url})
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]]}
    blocks = re.findall(r'<script type="application/ld\+json">.*?</script>', s, re.S)
    assert len(blocks) == 3, len(blocks)
    s = s.replace(blocks[0], jsonld(service)).replace(blocks[1], jsonld(bc)).replace(blocks[2], jsonld(faq))

    # --- body ---
    if lang == "en":
        crumb_html = f'<a href="index.html">{l["home"]}</a> &nbsp;&rsaquo;&nbsp; <a href="services.html">{l["exp"]}</a> &nbsp;&rsaquo;&nbsp; <span>{page["crumb"]}</span>'
    else:
        crumb_html = f'<a href="index.html">{l["home"]}</a> &nbsp;&rsaquo;&nbsp; <span>{page["crumb"]}</span>'
    facts = "\n".join(f'<div class="myc-fact"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in page["facts"])
    gallery = '<div class="myc-gallery">\n' + "\n".join(
        f'<img src="{P[k][0]}" width="{dims(P[k][0])[0]}" height="{dims(P[k][0])[1]}" loading="lazy" alt="{esc(P[k][1])}">' for k in page["gallery"]) + "\n</div>"
    th = l["tbl"]
    rows = "\n".join(f'<tr><td><a href="{b}.html">{boats[b][0]}</a></td><td>{boats[b][1]}</td><td>{why}</td></tr>' for b, why in page["table"])
    table = f'<div class="myc-table-wrap"><table class="myc-table">\n<thead><tr><th>{th[0]}</th><th>{th[1]}</th><th>{th[2]}</th></tr></thead>\n<tbody>\n{rows}\n</tbody>\n</table></div>'
    body = page["body"].replace("{GALLERY}", gallery).replace("{TABLE}", table)
    faq_html = f'<h2>{l["faq"]}</h2>\n' + "\n".join(f'<div class="myc-faq-item">\n<h3>{q}</h3>\n<p>{a}</p>\n</div>' for q, a in page["faq"])
    related = f'<div class="myc-related"><h2>{l["related"]}</h2><ul>' + "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in page["related"]) + "</ul></div>"
    cta_h, cta_p = page["cta"]
    cta = f'''<div class="myc-cta-band">
  <h2>{cta_h}</h2>
  <p>{cta_p}</p>
  <div class="myc-cta-buttons">
    <a href="tel:7876645040" class="myc-btn-primary">{l["call"]}</a>
    <a href="https://wa.me/17876645040" target="_blank" rel="noopener" class="myc-btn-wa">{l["wa"]}</a>
  </div>
</div>'''
    middle = f'''<section class="myc-hero">
        <div class="w-layout-blockcontainer container-default w-container">
          <div class="myc-breadcrumb">{crumb_html}</div>
          <h1>{page["h1"]}</h1>
          <p class="myc-lede">{page["lede"]}</p>
          <div class="myc-facts">
{facts}
          </div>
          <div style="margin:26px 0 10px;"><a href="#" class="yacht-details-button w-button" data-modal>{l["check"]}</a></div>
        </div>
      </section>
      <section>
        <div class="w-layout-blockcontainer container-default w-container">
          <div class="myc-content">
{body.strip()}

{faq_html}

{related}

{cta}

          </div>
        </div>
      </section>
'''
    start = s.index('<section class="myc-hero">')
    end = s.index('    </div>\n    <section data-w-id="2bf42e04-35fe-8a4c-78a6-1b9d3711c468" class="footer-section">')
    s = s[:start] + middle + s[end:]

    # --- chrome translation ---
    for a, b in CHROME.get(lang, []):
        assert a in s, (page["slug"], a)
        s = s.replace(a, b)
    # the template marks services.html as current in the footer; new pages are not services
    s = s.replace('<a href="services.html" aria-current="page" class="footer-nav-link w--current">Services</a>', '<a href="services.html" class="footer-nav-link">Services</a>')
    return s

wa = {}
for page in PAGES:
    out = REPO / (page["slug"] + ".html")
    out.write_text(build(page), encoding="utf-8")
    wa[page["slug"]] = page["wa"]
    print("wrote", out.name, len(out.read_text(encoding="utf-8")))
(Path(__file__).parent / "wa_new_pages.json").write_text(json.dumps(wa, ensure_ascii=False, indent=1))
