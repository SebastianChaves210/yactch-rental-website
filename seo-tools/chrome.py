# -*- coding: utf-8 -*-
"""Shared page chrome: skip link, header (dropdowns + mobile menu), footer, sticky bar,
booking modal, fleet cards and the document shell used by generated pages.

Every function returns an HTML string with final (clean) URLs and root-absolute assets.
"""
import html as H
import json
from ia import (FLEET, PAGES, EXPERIENCES, DESTINATIONS, EVENTS, GUIDES, SITE, TEL, PHONE_DISPLAY, EMAIL,
                ADDRESS_LINE, ADDRESS_CITY, MAPS_URL, INSTAGRAM, LOGO, YEAR, wa_for, wa_url, url_of, lang_target,
                price_str, section_crumb)

# ---------------------------------------------------------------- labels per language
T = {
    "en": dict(boats="Boat rentals", skip="Skip to content", home="Home", yachts="Yachts", experiences="Experiences", destinations="Destinations",
               prices="Prices", guides="Guides", about="About", contact="Contact", book="Book a Yacht", call="Call",
               call_full=f"Call {PHONE_DISPLAY}", whatsapp="WhatsApp", menu_open="Open menu", menu_close="Close menu",
               all_fleet="View the full fleet", all_exp="All experiences", all_dest="All destinations", from_="from",
               per="/ 4 hours", main_nav="Main", lang_nav="Language", mobile_nav="Mobile",
               footer_h="Let’s plan your private voyage now",
               footer_p="Call or WhatsApp with your date and group size. Captain and crew included, from $1,000 for 4 hours.",
               tagline="Private yacht charters in Miami with captain and crew included. One dock on the Miami River, nine yachts from 25 to 90 feet, booked direct.",
               fleet="Fleet", exp_dest="Experiences &amp; Destinations", company="Company", all_yachts="All yachts &amp; prices",
               events="Miami events", gallery="Gallery", faq="FAQ", addons="Add-ons", book_short="Book a yacht",
               privacy="Privacy", terms="Terms", cancel="Cancellation Policy", book_now="Book now", view="View yacht",
               breadcrumb="Breadcrumb", dock="Departs 668 NW N River Dr, Miami River"),
    "es": dict(boats="Alquiler de lanchas", skip="Saltar al contenido", home="Inicio", yachts="Yates", experiences="Experiencias", destinations="Destinos",
               prices="Precios", guides="Guías", about="Nosotros", contact="Contacto", book="Reservar un yate", call="Llamar",
               call_full=f"Llamar al {PHONE_DISPLAY}", whatsapp="WhatsApp", menu_open="Abrir menú", menu_close="Cerrar menú",
               all_fleet="Ver toda la flota", all_exp="Todas las experiencias", all_dest="Todos los destinos", from_="desde",
               per="/ 4 horas", main_nav="Principal", lang_nav="Idioma", mobile_nav="Menú",
               footer_h="Planifiquemos su paseo privado",
               footer_p="Llame o escriba por WhatsApp con su fecha y cuántos son. Capitán y tripulación incluidos, desde $1,000 por 4 horas.",
               tagline="Alquiler de yates privados en Miami con capitán y tripulación incluidos. Un muelle en el río Miami, nueve yates de 25 a 90 pies, reserva directa.",
               fleet="Flota", exp_dest="Experiencias y destinos", company="Empresa", all_yachts="Todos los yates y precios",
               events="Eventos en Miami", gallery="Galería", faq="Preguntas frecuentes", addons="Extras", book_short="Reservar",
               privacy="Privacidad", terms="Términos", cancel="Política de cancelación", book_now="Reservar", view="Ver yate",
               breadcrumb="Ruta de navegación", dock="Sale de 668 NW N River Dr, río Miami"),
    "pt-BR": dict(boats="Aluguel de lanchas", skip="Pular para o conteúdo", home="Início", yachts="Iates", experiences="Experiências", destinations="Destinos",
               prices="Preços", guides="Guias", about="Sobre", contact="Contato", book="Reservar um iate", call="Ligar",
               call_full=f"Ligar para {PHONE_DISPLAY}", whatsapp="WhatsApp", menu_open="Abrir menu", menu_close="Fechar menu",
               all_fleet="Ver toda a frota", all_exp="Todas as experiências", all_dest="Todos os destinos", from_="a partir de",
               per="/ 4 horas", main_nav="Principal", lang_nav="Idioma", mobile_nav="Menu",
               footer_h="Vamos planejar o seu passeio privativo",
               footer_p="Ligue ou mande WhatsApp com a data e o número de pessoas. Capitão e tripulação inclusos, a partir de $1,000 por 4 horas.",
               tagline="Aluguel de iates privativos em Miami com capitão e tripulação inclusos. Um píer no Miami River, nove iates de 25 a 90 pés, reserva direta.",
               fleet="Frota", exp_dest="Experiências e destinos", company="Empresa", all_yachts="Todos os iates e preços",
               events="Eventos em Miami", gallery="Galeria", faq="Perguntas frequentes", addons="Extras", book_short="Reservar",
               privacy="Privacidade", terms="Termos", cancel="Política de cancelamento", book_now="Reservar", view="Ver iate",
               breadcrumb="Navegação", dock="Sai de 668 NW N River Dr, Miami River"),
}

# dropdown / footer labels for the occasion and destination pages
EXP_LABELS = {
    "en": {"birthday-yacht-party-miami": "Birthday", "bachelorette-yacht-party-miami": "Bachelorette", "bachelor-party-yacht-miami": "Bachelor",
           "proposal-yacht-charter-miami": "Proposal", "corporate-yacht-charter-miami": "Corporate", "wedding-yacht-charter-miami": "Wedding",
           "private-sunset-cruise-miami": "Sunset Cruise", "yacht-party-miami": "Yacht Party"},
    "es": {"birthday-yacht-party-miami": "Cumpleaños", "bachelorette-yacht-party-miami": "Despedida de soltera", "bachelor-party-yacht-miami": "Despedida de soltero",
           "proposal-yacht-charter-miami": "Pedida de mano", "corporate-yacht-charter-miami": "Empresas", "wedding-yacht-charter-miami": "Bodas",
           "private-sunset-cruise-miami": "Paseo al atardecer", "yacht-party-miami": "Fiesta en yate"},
    "pt-BR": {"birthday-yacht-party-miami": "Aniversário", "bachelorette-yacht-party-miami": "Despedida de solteira", "bachelor-party-yacht-miami": "Despedida de solteiro",
           "proposal-yacht-charter-miami": "Pedido de casamento", "corporate-yacht-charter-miami": "Corporativo", "wedding-yacht-charter-miami": "Casamento",
           "private-sunset-cruise-miami": "Pôr do sol", "yacht-party-miami": "Festa em iate"},
}
DEST_LABELS = {
    "en": {"sandbar-yacht-charter-miami": "Sandbar", "star-island-boat-tour-miami": "Star Island", "yacht-rental-miami-beach": "Miami Beach",
           "south-beach-yacht-rental": "South Beach", "yacht-rental-brickell": "Brickell"},
    "es": {"sandbar-yacht-charter-miami": "Sandbar", "star-island-boat-tour-miami": "Star Island", "yacht-rental-miami-beach": "Miami Beach",
           "south-beach-yacht-rental": "South Beach", "yacht-rental-brickell": "Brickell"},
    "pt-BR": {"sandbar-yacht-charter-miami": "Sandbar", "star-island-boat-tour-miami": "Star Island", "yacht-rental-miami-beach": "Miami Beach",
           "south-beach-yacht-rental": "South Beach", "yacht-rental-brickell": "Brickell"},
}
# the Spanish page yacht-party-miami has a true translation; everything else in ES/PT menus links to the English page
EXP_TARGET = {"es": {"yacht-party-miami": "fiesta-en-yate-miami"}}
# yacht names in the ES / PT menus
NAMES = {
    "es": {"deep-blue": "Deep Blue de 90' con jacuzzi", "ferretti": "Ferretti de 75'", "azimut-lchaim": "Azimut L'chaim de 65'", "anvera": "Anvera de 62'",
           "azimut": "Azimut de 55'", "isabella": "Isabella de 48' con jet ski", "maxum": "Maxum de 46'", "axopar-brabus": "Axopar Brabus de 28'", "yamaha-255xd": "Yamaha 255XD de 25'"},
    "pt-BR": {"deep-blue": "Deep Blue de 90 pés com jacuzzi", "ferretti": "Ferretti de 75 pés", "azimut-lchaim": "Azimut L'chaim de 65 pés", "anvera": "Anvera de 62 pés",
           "azimut": "Azimut de 55 pés", "isabella": "Isabella de 48 pés com jet ski", "maxum": "Maxum de 46 pés", "axopar-brabus": "Axopar Brabus de 28 pés", "yamaha-255xd": "Yamaha 255XD de 25 pés"},
}

ICON_CHEVRON = '<svg class="myc-chev" width="12" height="12" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_PHONE = '<svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor" aria-hidden="true" focusable="false"><path d="M17.51 13.21l-2.51-2.51c-.9-.9-2.42-.54-2.78.63-.27.8-1.17 1.25-1.97 1.07-1.8-.45-4.22-2.78-4.66-4.66-.27-.81.27-1.7 1.07-1.97 1.17-.36 1.53-1.88.63-2.78l-2.51-2.51c-.72-.63-1.8-.63-2.42 0L.81 2.18c-1.7 1.79.18 6.55 4.4 10.76 4.21 4.21 8.97 6.19 10.76 4.4l1.7-1.7c.63-.72.63-1.79 0-2.42z"/></svg>'
ICON_WA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6.1-.1.3-.4.5-.5.1-.2.2-.3.3-.5.1-.2 0-.4-.1-.6-.1-.2-.7-1.7-1-2.3-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4s-1.1 1-1.1 2.5 1.1 2.9 1.3 3.1c.2.2 2.2 3.3 5.3 4.6 2.5 1 3 .8 3.6.8.6 0 1.8-.7 2-1.5.3-.7.3-1.4.2-1.5-.1-.1-.3-.2-.6-.3zM12 2C6.5 2 2 6.5 2 12c0 1.7.4 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3.1 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2z"/></svg>'
ICON_IG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'


def esc(s):
    return H.escape(s, quote=True)


def _exp_href(slug, lang):
    return url_of(EXP_TARGET.get(lang, {}).get(slug, slug))


def _yacht_items(lang, mobile=False):
    t = T[lang]
    out = []
    for b in FLEET:
        name = NAMES.get(lang, {}).get(b["old"], b["name"])
        out.append(f'<li><a href="{url_of(b["old"])}"><span class="myc-menu-name">{esc(name)}</span>'
                   f'<span class="myc-menu-meta">{t["from_"]} {price_str(b)}</span></a></li>')
    return "\n".join(out)


def _exp_items(lang):
    return "\n".join(f'<li><a href="{_exp_href(s, lang)}">{esc(l)}</a></li>' for s, l in EXP_LABELS[lang].items())


def _dest_items(lang):
    return "\n".join(f'<li><a href="{url_of(s)}">{esc(l)}</a></li>' for s, l in DEST_LABELS[lang].items())


def _lang_switch(old, lang, cls="myc-lang"):
    t = T[lang]
    parts = []
    for code, label in (("en", "EN"), ("es", "ES"), ("pt-BR", "PT")):
        target = lang_target(old, code)
        cur = ' aria-current="true"' if code == lang else ""
        parts.append(f'<a href="{url_of(target)}" lang="{code}" hreflang="{code}"{cur}>{label}</a>')
    sep = '<span class="myc-lang-sep" aria-hidden="true">·</span>'
    return f'<nav class="{cls}" aria-label="{t["lang_nav"]}">{sep.join(parts)}</nav>'


def header(old, lang="en"):
    t = T[lang]
    wa = wa_for(old)
    cur = lambda key: ' aria-current="page"' if PAGES[old]["section"] == key or old == key else ""
    menus = [
        ("yachts", t["yachts"], _yacht_items(lang), url_of("yacht"), t["all_fleet"], "myc-menu-yachts"),
        ("experiences", t["experiences"], _exp_items(lang), url_of("services"), t["all_exp"], ""),
        ("destinations", t["destinations"], _dest_items(lang), url_of("destinations"), t["all_dest"], ""),
    ]
    desk = []
    mob = []
    for key, label, items, hub, all_label, extra in menus:
        desk.append(f'''<li class="myc-nav-item myc-has-menu">
          <button type="button" class="myc-nav-link myc-nav-toggle" aria-expanded="false" aria-controls="myc-menu-{key}">{label}{ICON_CHEVRON}</button>
          <div class="myc-menu {extra}" id="myc-menu-{key}">
            <ul class="myc-menu-list">
{items}
            </ul>
            <a class="myc-menu-all" href="{hub}">{all_label} <span aria-hidden="true">&rarr;</span></a>
          </div>
        </li>''')
        mob.append(f'''<li class="myc-m-item">
          <button type="button" class="myc-m-toggle" aria-expanded="false" aria-controls="myc-m-{key}">{label}{ICON_CHEVRON}</button>
          <ul class="myc-m-sub" id="myc-m-{key}" hidden>
{items}
            <li class="myc-m-all"><a href="{hub}">{all_label} <span aria-hidden="true">&rarr;</span></a></li>
          </ul>
        </li>''')
    plain = [("miami-yacht-rental-prices", t["prices"]), ("guides", t["guides"]), ("about", t["about"]), ("contact", t["contact"])]
    for slug, label in plain:
        a = f'<a class="myc-nav-link" href="{url_of(slug)}"{cur(slug) if slug != "guides" else cur("guides")}>{label}</a>'
        desk.append(f'<li class="myc-nav-item">{a}</li>')
        mob.append(f'<li class="myc-m-item"><a class="myc-m-link" href="{url_of(slug)}">{label}</a></li>')
    desk_html = "\n        ".join(desk)
    mob_html = "\n        ".join(mob)
    home_cur = ' aria-current="page"' if old == "index" else ""
    return f'''<a class="myc-skip" href="#main">{t["skip"]}</a>
    <header class="myc-header" id="myc-header">
      <div class="myc-header-inner">
        <a class="myc-logo" href="{url_of(lang_target(old, lang)) if lang != "en" else "/"}"{home_cur} aria-label="Miami Yacht Collective"><img src="{LOGO}" width="420" height="420" alt="Miami Yacht Collective" loading="eager" decoding="async"></a>
        <nav class="myc-nav" aria-label="{t["main_nav"]}">
          <ul class="myc-nav-list">
        {desk_html}
          </ul>
        </nav>
        <div class="myc-header-actions">
          {_lang_switch(old, lang)}
          <a class="myc-call" href="{TEL}" aria-label="{t["call_full"]}" title="{t["call_full"]}">{ICON_PHONE}</a>
          <a class="myc-cta" href="{wa}" target="_blank" rel="noopener">{t["book"]}</a>
          <button type="button" class="myc-burger" aria-expanded="false" aria-controls="myc-mobile" aria-label="{t["menu_open"]}" data-label-open="{t["menu_open"]}" data-label-close="{t["menu_close"]}"><span></span><span></span><span></span></button>
        </div>
      </div>
      <div class="myc-mobile" id="myc-mobile" hidden>
        <nav aria-label="{t["mobile_nav"]}">
          <ul class="myc-m-list">
        {mob_html}
          </ul>
        </nav>
        <div class="myc-m-foot">
          <a class="myc-btn myc-btn-wa" href="{wa}" target="_blank" rel="noopener">{ICON_WA}{t["whatsapp"]}</a>
          <a class="myc-btn myc-btn-ghost" href="{TEL}">{ICON_PHONE}{t["call_full"]}</a>
          {_lang_switch(old, lang, "myc-lang myc-lang-mobile")}
        </div>
      </div>
    </header>'''


def footer(old, lang="en"):
    t = T[lang]
    wa = wa_for(old)
    fleet = "\n".join(f'<li><a href="{url_of(b["old"])}">{esc(NAMES.get(lang, {}).get(b["old"], b["name"]))}</a></li>' for b in FLEET)
    exp = "\n".join(f'<li><a href="{_exp_href(s, lang)}">{esc(l)}</a></li>' for s, l in EXP_LABELS[lang].items())
    dest = "\n".join(f'<li><a href="{url_of(s)}">{esc(l)}</a></li>' for s, l in DEST_LABELS[lang].items())
    langs = []
    for code, label in (("en", "English"), ("es", "Español"), ("pt-BR", "Português")):
        langs.append(f'<li><a href="{url_of(lang_target(old, code))}" lang="{code}" hreflang="{code}"{" aria-current=\"true\"" if code == lang else ""}>{label}</a></li>')
    return f'''<footer class="myc-footer" id="myc-footer">
      <div class="myc-footer-cta">
        <div class="myc-wrap myc-footer-cta-inner">
          <h2>{t["footer_h"]}</h2>
          <p>{t["footer_p"]}</p>
          <div class="myc-btn-row">
            <a class="myc-btn myc-btn-wa" href="{wa}" target="_blank" rel="noopener">{ICON_WA}{t["whatsapp"]}</a>
            <a class="myc-btn myc-btn-ghost" href="{TEL}">{ICON_PHONE}{t["call_full"]}</a>
          </div>
        </div>
      </div>
      <div class="myc-wrap myc-footer-grid">
        <div class="myc-footer-brand">
          <a href="{url_of(lang_target(old, lang)) if lang != "en" else "/"}" class="myc-footer-logo" aria-label="Miami Yacht Collective"><img src="{LOGO}" width="420" height="420" alt="Miami Yacht Collective" loading="lazy" decoding="async"></a>
          <p class="myc-footer-tagline">{t["tagline"]}</p>
          <address class="myc-footer-address">
            <a href="{MAPS_URL}" target="_blank" rel="noopener">{ADDRESS_LINE}<br>{ADDRESS_CITY}</a>
            <a href="{TEL}">{PHONE_DISPLAY}</a>
            <a href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
            <!-- TODO(owner): a branded @miamiyachtcollective.com address is recommended over the current one -->
          </address>
        </div>
        <nav class="myc-footer-col" aria-labelledby="myc-f-fleet">
          <h2 id="myc-f-fleet">{t["fleet"]}</h2>
          <ul>
{fleet}
            <li><a href="{url_of("yacht")}" class="myc-footer-more">{t["all_yachts"]} <span aria-hidden="true">&rarr;</span></a></li>
          </ul>
        </nav>
        <nav class="myc-footer-col" aria-labelledby="myc-f-exp">
          <h2 id="myc-f-exp">{t["exp_dest"]}</h2>
          <ul>
{exp}
{dest}
            <li><a href="{url_of("boat-rental-miami")}">{t["boats"]}</a></li>
            <li><a href="{url_of("events")}">{t["events"]}</a></li>
            <li><a href="{url_of("miami-yacht-rental-prices")}">{t["prices"]}</a></li>
            <li><a href="{url_of("guides")}">{t["guides"]}</a></li>
          </ul>
        </nav>
        <nav class="myc-footer-col" aria-labelledby="myc-f-co">
          <h2 id="myc-f-co">{t["company"]}</h2>
          <ul>
            <li><a href="{url_of("about")}">{t["about"]}</a></li>
            <li><a href="{url_of("gallery")}">{t["gallery"]}</a></li>
            <li><a href="{url_of("faq")}">{t["faq"]}</a></li>
            <li><a href="{url_of("add-ons")}">{t["addons"]}</a></li>
            <!-- TODO(owner): Reviews page link goes here once real reviews or a Google Business Profile URL are supplied -->
            <li><a href="{url_of("contact")}">{t["contact"]}</a></li>
            <li><a href="{url_of("booking")}">{t["book_short"]}</a></li>
          </ul>
        </nav>
      </div>
      <div class="myc-wrap myc-footer-bottom">
        <p class="myc-footer-copy">&copy; {YEAR} Miami Yacht Collective</p>
        <ul class="myc-footer-legal">
          <li><a href="{url_of("privacy-policy")}">{t["privacy"]}</a></li>
          <li><a href="{url_of("terms")}">{t["terms"]}</a></li>
          <li><a href="{url_of("cancellation-policy")}">{t["cancel"]}</a></li>
        </ul>
        <ul class="myc-footer-langs">
{chr(10).join(langs)}
        </ul>
        <ul class="myc-footer-social">
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{ICON_IG}</a></li>
          <!-- TODO(owner): add Facebook / TikTok / YouTube / Google Business Profile links here once confirmed -->
        </ul>
      </div>
      <p class="myc-footer-watermark" aria-hidden="true">Collective</p>
    </footer>'''


def sticky(old, lang="en", yacht=None):
    t = T[lang]
    wa = wa_for(old)
    if yacht:
        return f'''<div class="myc-sticky-cta myc-sticky-yacht" aria-label="{t["book_now"]}">
  <div class="myc-sticky-info"><span class="myc-sticky-price">{t["from_"]} {price_str(yacht)}</span><span class="myc-sticky-sub">4h &middot; captain &amp; crew</span></div>
  <a href="{TEL}" class="myc-sticky-call" aria-label="{t["call_full"]}">{ICON_PHONE}<span>{t["call"]}</span></a>
  <a href="{wa}" target="_blank" rel="noopener" class="myc-sticky-wa">{ICON_WA}<span>{t["book_now"]}</span></a>
</div>'''
    return f'''<div class="myc-sticky-cta" aria-label="{t["book_now"]}">
  <a href="{TEL}" class="myc-sticky-call">{ICON_PHONE}<span>{t["call"]}</span></a>
  <a href="{wa}" target="_blank" rel="noopener" class="myc-sticky-wa">{ICON_WA}<span>{t["whatsapp"]}</span></a>
</div>'''


MODAL_TEXT = {
    "en": ("How Would You Like to Book?", "We'll confirm your booking right away!", f"Call us at {PHONE_DISPLAY}", "WhatsApp Direct", "Close booking dialog"),
    "es": ("¿Cómo prefiere reservar?", "¡Confirmamos su reserva de inmediato!", f"Llamar al {PHONE_DISPLAY}", "WhatsApp directo", "Cerrar"),
    "pt-BR": ("Como prefere reservar?", "Confirmamos a sua reserva na hora!", f"Ligar para {PHONE_DISPLAY}", "WhatsApp direto", "Fechar"),
}


def modal(old, lang="en"):
    h, sub, call, wa_label, close = MODAL_TEXT[lang]
    return f'''<div class="modal-backdrop" id="modalBackdrop" role="dialog" aria-modal="true" aria-labelledby="modalHeading">
  <div class="modal-booking">
    <button class="modal-close" id="modalClose" aria-label="{close}">&times;</button>
    <div class="modal-heading" id="modalHeading">{h}</div>
    <p class="modal-subtext">{sub}</p>
    <div class="modal-buttons">
      <a href="{TEL}" class="modal-btn modal-btn-call">{call}</a>
      <a href="{wa_for(old)}" target="_blank" rel="noopener" class="modal-btn modal-btn-wa">{wa_label}</a>
    </div>
  </div>
</div>

<script>
(function() {{
  var backdrop = document.getElementById('modalBackdrop');
  var modalClose = document.getElementById('modalClose');
  if (!backdrop || !modalClose) return;
  var lastTrigger = null;

  function openModal(e) {{
    e.preventDefault();
    lastTrigger = e.currentTarget;
    backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
    if (window.mycLenis) window.mycLenis.stop();
    requestAnimationFrame(function() {{ setTimeout(function() {{ modalClose.focus(); }}, 60); }});
  }}

  function closeModal() {{
    if (!backdrop.classList.contains('active')) return;
    backdrop.classList.remove('active');
    document.body.style.overflow = '';
    if (window.mycLenis) window.mycLenis.start();
    if (lastTrigger && typeof lastTrigger.focus === 'function') lastTrigger.focus();
    lastTrigger = null;
  }}

  document.querySelectorAll('[data-modal]').forEach(function(btn) {{
    btn.addEventListener('click', openModal);
  }});

  modalClose.addEventListener('click', closeModal);

  backdrop.addEventListener('click', function(e) {{
    if (e.target === backdrop) closeModal();
  }});

  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') {{ closeModal(); return; }}
    if (e.key === 'Tab' && backdrop.classList.contains('active')) {{
      var focusables = backdrop.querySelectorAll('a[href], button');
      if (!focusables.length) return;
      var first = focusables[0], last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) {{ e.preventDefault(); last.focus(); }}
      else if (!e.shiftKey && document.activeElement === last) {{ e.preventDefault(); first.focus(); }}
    }}
  }});
}})();
</script>'''


MODAL_CSS = '''<style>
  .modal-backdrop { position: fixed; inset: 0; z-index: 9999; background: rgba(0, 0, 0, 0.6); display: flex; align-items: center; justify-content: center; opacity: 0; visibility: hidden; transition: opacity 0.2s ease, visibility 0.2s ease; }
  .modal-backdrop.active { opacity: 1; visibility: visible; }
  .modal-booking { background: #fff; border-radius: 20px; max-width: 480px; width: 90%; padding: 48px 40px; position: relative; transform: scale(0.95); transition: transform 0.2s ease; }
  .modal-backdrop.active .modal-booking { transform: scale(1); }
  .modal-close { position: absolute; top: 18px; right: 20px; background: none; border: none; font-size: 24px; color: #555; cursor: pointer; line-height: 1; padding: 4px; transition: color 0.2s ease; }
  .modal-close:hover { color: #000; }
  .modal-heading { font-weight: 800; font-size: 30px; color: #111; text-align: center; margin-bottom: 8px; }
  .modal-subtext { font-size: 16px; color: #666; text-align: center; margin-bottom: 36px; }
  .modal-buttons { display: flex; flex-direction: column; gap: 14px; }
  .modal-btn { display: block; width: 100%; padding: 20px; border: none; border-radius: 999px; font-weight: 700; font-size: 16px; letter-spacing: 0.3px; text-align: center; text-decoration: none; cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease; }
  .modal-btn:hover { transform: translateY(-1px); }
  .modal-btn-call { background: #0d1b4b; color: #fff; }
  .modal-btn-wa { background: #25D366; color: #fff; }
</style>'''

FONTS = "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter+Tight:wght@300;400;500;600;700&display=swap"


def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=1, ensure_ascii=False) + '\n</script>'


def org_jsonld(include_business=True, website=False):
    """Site-wide Organization (+ LocalBusiness unless the page already defines it, + WebSite on the home page)."""
    graph = [
            {"@type": "Organization", "@id": SITE + "/#organization", "name": "Miami Yacht Collective", "url": SITE + "/",
             "logo": SITE + "/images/main-boat-logo-transparent.png", "telephone": "+1-787-664-5040", "email": EMAIL,
             "sameAs": [INSTAGRAM, MAPS_URL],
             "contactPoint": {"@type": "ContactPoint", "telephone": "+1-787-664-5040", "contactType": "reservations",
                              "availableLanguage": ["English", "Spanish"], "areaServed": "US"}},
            {"@type": "LocalBusiness", "@id": SITE + "/#business", "name": "Miami Yacht Collective", "url": SITE + "/",
             "image": SITE + "/images/main-boat-logo-transparent.png", "telephone": "+1-787-664-5040", "email": EMAIL,
             "priceRange": "$1,000 - $4,999", "parentOrganization": {"@id": SITE + "/#organization"},
             "address": {"@type": "PostalAddress", "streetAddress": ADDRESS_LINE, "addressLocality": "Miami", "addressRegion": "FL",
                         "postalCode": "33136", "addressCountry": "US"},
             "geo": {"@type": "GeoCoordinates", "latitude": 25.7802006, "longitude": -80.2090659},
             "sameAs": [INSTAGRAM, MAPS_URL],
             "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                           "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                           "opens": "00:00", "closes": "23:59"}},
        ]
    if not include_business:
        graph = graph[:1]
    if website:
        graph.append({"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Miami Yacht Collective",
                      "inLanguage": ["en", "es", "pt-BR"], "publisher": {"@id": SITE + "/#organization"}})
    return jsonld({"@context": "https://schema.org", "@graph": graph})


def breadcrumb_jsonld(trail):
    return jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList",
                   "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": H.unescape(n), "item": SITE + u} for i, (n, u) in enumerate(trail)]})


def breadcrumb_html(trail, lang="en"):
    t = T[lang]
    items = []
    for i, (name, url) in enumerate(trail):
        last = i == len(trail) - 1
        if last:
            items.append(f'<li aria-current="page">{name}</li>')
        else:
            items.append(f'<li><a href="{url}">{name}</a></li>')
    return f'<nav class="myc-crumbs" aria-label="{t["breadcrumb"]}"><ol>{"".join(items)}</ol></nav>'


def card(b, lang="en", heading="h3", show_blurb=True):
    t = T[lang]
    src, w, h = b["card"]
    meta = f'{b["length"]} ft &middot; {b["type"]}' + (f' &middot; {b["feature"]}' if b.get("feature") else "")
    name = NAMES.get(lang, {}).get(b["old"], b["name"])
    blurb = f'<p class="myc-card-blurb">{esc(b["blurb"])}</p>' if show_blurb and lang == "en" else ""
    return f'''<article class="myc-card" data-length="{b["length"]}" data-price="{b["price"]}" data-feature="{esc((b.get("feature") or "").lower())}">
  <a class="myc-card-media" href="{url_of(b["old"])}" tabindex="-1" aria-hidden="true"><img src="/{src}" width="{w}" height="{h}" alt="{esc(name)}" loading="lazy" decoding="async"></a>
  <div class="myc-card-body">
    <{heading} class="myc-card-title"><a href="{url_of(b["old"])}">{esc(name)}</a></{heading}>
    <p class="myc-card-meta">{meta}</p>
    <p class="myc-card-price"><span>{t["from_"]}</span> {price_str(b)} <span>{t["per"]}</span></p>
    {blurb}
    <div class="myc-card-actions"><a class="myc-link" href="{url_of(b["old"])}">{t["view"]} <span aria-hidden="true">&rarr;</span></a><a class="myc-btn myc-btn-sm" href="{wa_url("Hi! I'm interested in the " + b["name"] + ". My date:")}" target="_blank" rel="noopener">{t["book_now"]}</a></div>
  </div>
</article>'''


def cards(boat_olds, lang="en", heading="h3", show_blurb=True):
    from ia import FLEET_BY_OLD
    return '<div class="myc-cards">\n' + "\n".join(card(FLEET_BY_OLD[o], lang, heading, show_blurb) for o in boat_olds) + "\n</div>"


def cta_band(h, p, old, lang="en", call_label=None, wa_label=None):
    t = T[lang]
    return f'''<div class="myc-cta-band">
  <h2>{h}</h2>
  <p>{p}</p>
  <div class="myc-cta-buttons">
    <a href="{TEL}" class="myc-btn-primary">{call_label or t["call_full"]}</a>
    <a href="{wa_for(old)}" target="_blank" rel="noopener" class="myc-btn-wa">{wa_label or ("WhatsApp Us" if lang == "en" else t["whatsapp"])}</a>
  </div>
</div>'''


def shell(old, *, title, desc, body, lang="en", og_image=None, head_extra="", noindex=False, body_class="", yacht=None,
          hreflang=None, webflow=False, og_alt=None):
    """Full document for a generated page. `body` is the content inside <main>."""
    from ia import og_card, abs_url
    url = abs_url(old)
    og = og_image or og_card(old)
    t = T[lang]
    locale = {"en": "en_US", "es": "es_US", "pt-BR": "pt_BR"}[lang]
    robots = '\n  <meta name="robots" content="noindex, follow">' if noindex else ""
    hl = ""
    if hreflang:
        hl = "".join(f'\n  <link rel="alternate" hreflang="{code}" href="{abs_url(slug)}">' for code, slug in hreflang)
    alt = og_alt or f"{H.unescape(title).split('|')[0].strip()} — Miami Yacht Collective"
    wf = ""
    if webflow:
        wf = '\n  <script src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=69ae24c3024e541e58b603ce" type="text/javascript" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>\n  <script src="/js/webflow.js" type="text/javascript"></script>'
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-TRVB7SJPJY"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-TRVB7SJPJY');
  </script>
  <title>{title}</title>
  <meta name="description" content="{esc(desc)}">{robots}
  <link rel="canonical" href="{url}">{hl}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{esc(alt)}">
  <meta name="twitter:image:alt" content="{esc(alt)}">
  <meta property="og:site_name" content="Miami Yacht Collective">
  <meta property="og:locale" content="{locale}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{og}">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <link href="/css/normalize.css" rel="stylesheet" type="text/css">
  <link href="/css/webflow.css" rel="stylesheet" type="text/css">
  <link href="/css/miami-yacht-collective.webflow.css" rel="stylesheet" type="text/css">
  <link href="/css/myc-theme.css" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link href="https://fonts.gstatic.com" rel="preconnect" crossorigin="anonymous">
  <link rel="preload" as="style" href="{FONTS}" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link href="{FONTS}" rel="stylesheet"></noscript>
  <script type="text/javascript">!function(o,c){{var n=c.documentElement,t=" w-mod-";n.className+=t+"js",("ontouchstart"in o||o.DocumentTouch&&c instanceof DocumentTouch)&&(n.className+=t+"touch")}}(window,document);</script>
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#081524">

{MODAL_CSS}
  <script defer src="/_vercel/insights/script.js"></script>
{head_extra}
</head>
<body class="{body_class}">
  <div class="page-wrapper">
    <div class="global-scripts w-embed w-script">
      <style>
  html, body {{
    height: auto !important;
    overflow: visible !important;
  }}
</style>
      <script defer src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>
      <script>
  document.addEventListener("DOMContentLoaded", function () {{
    if (!window.Lenis) return;
    const lenis = window.mycLenis = new Lenis({{
      duration: 1.2,
      easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smooth: true,
    }});
    function raf(time) {{
      lenis.raf(time);
      requestAnimationFrame(raf);
    }}
    requestAnimationFrame(raf);
  }});
</script>
    </div>
    {header(old, lang)}
    <main id="main" class="main-wrapper">
{body}
    </main>
    {footer(old, lang)}
  </div>{wf}

{sticky(old, lang, yacht)}
{modal(old, lang)}
<script src="/js/tracking.js"></script>
<script defer src="/js/myc-site.js"></script>
</body>
</html>
'''
