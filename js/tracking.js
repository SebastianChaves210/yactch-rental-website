/**
 * GA4 lead tracking for Miami Yacht Collective.
 * gtag.js (G-TRVB7SJPJY) is loaded in the <head> of every page; this file is loaded sitewide
 * right after the booking modal and before /js/myc-site.js.
 *
 * Events (sent with transport_type: 'beacon' so they survive navigation):
 *   whatsapp_click  any wa.me / api.whatsapp.com link, plus the booking widget and forms that
 *                   compose a WhatsApp message (myc-site.js calls window.mycTrack when it opens WhatsApp)
 *   phone_click     any tel: link
 *   email_click     any mailto: link
 *   modal_open      a [data-modal] trigger opened the Call/WhatsApp booking modal
 *
 * Params on every event:
 *   link_location   header | mobile_menu | sticky_bar | hero | booking_widget | booking_form | modal |
 *                   card | cta_band | footer_cta | footer | faq | related | yacht_page | inline
 *                   (override anywhere with data-track-location="..." on the link or an ancestor)
 *   page_path       location.pathname (clean URL, e.g. /yachts/48-isabella)
 *   link_url        the href (or the composed WhatsApp URL)
 *   link_text       trimmed visible text of the link (max 80 chars)
 *   yacht_name      only when known: <body data-yacht> on yacht pages, the fleet card's data-yacht,
 *                   or the yacht chosen in a booking form
 */
(function () {
  'use strict';

  /* ------------------------------------------------------------------
   * Google Ads conversions (optional) - the ONLY place to configure them.
   * When a Google Ads account exists, set the AW- id and the conversion label
   * for each lead event you want counted, e.g.
   *   var ADS = { id: 'AW-123456789', labels: { whatsapp_click: 'AbCdEfGhIjKlMnOp', phone_click: 'QrStUvWxYz012345', email_click: '' } };
   * Each matching event then also sends gtag('event', 'conversion', { send_to: 'AW-123456789/<label>' }).
   * Leave id empty to send GA4 events only.
   * ------------------------------------------------------------------ */
  var ADS = { id: '', labels: { whatsapp_click: '', phone_click: '', email_click: '' } };

  var LOCATIONS = [
    ['.modal-booking', 'modal'],
    ['.myc-sticky-cta', 'sticky_bar'],
    ['.myc-m-foot', 'mobile_menu'],
    ['.myc-header', 'header'],
    ['.myc-footer-cta', 'footer_cta'],
    ['.myc-footer', 'footer'],
    ['.myc-fallback', 'booking_form'],   // nested inside .myc-widget, so it must come first
    ['.myc-widget', 'booking_widget'],
    ['.myc-card', 'card'],
    ['.myc-hero, .myc-yhero, .myc-contact-hero, .hero-block, .home-hero-section, .about-hero-section, .gallery-hero-section, .services-hero-section', 'hero'],
    ['.myc-cta-band, .contact-cta-stack', 'cta_band'],
    ['.myc-faq-item, .myc-faq-group, .home-faq-section', 'faq'],
    ['.myc-related', 'related']
  ];

  function hasGtag() { return typeof window.gtag === 'function'; }

  function closest(el, sel) {
    return el && el.closest ? el.closest(sel) : null;
  }

  function locationOf(el) {
    var o = closest(el, '[data-track-location]');
    if (o) return o.getAttribute('data-track-location');
    for (var i = 0; i < LOCATIONS.length; i++) {
      if (closest(el, LOCATIONS[i][0])) return LOCATIONS[i][1];
    }
    return document.body.hasAttribute('data-yacht') ? 'yacht_page' : 'inline';
  }

  function yachtOf(el) {
    var y = closest(el, '[data-yacht]');
    return y ? y.getAttribute('data-yacht') : (document.body.getAttribute('data-yacht') || '');
  }

  function textOf(el) {
    var t = (el.textContent || '').replace(/\s+/g, ' ').trim() || el.getAttribute('aria-label') || '';
    return t.length > 80 ? t.slice(0, 80) : t;
  }

  /**
   * Send a lead event. Exposed as window.mycTrack(name, extra, el) so other scripts
   * (the WhatsApp booking forms in myc-site.js) can report with the same params.
   */
  function track(name, extra, el) {
    var params = {
      link_location: (extra && extra.link_location) || locationOf(el),
      page_path: window.location.pathname,
      transport_type: 'beacon'
    };
    if (el && el.href) params.link_url = el.href;
    if (el) params.link_text = textOf(el);
    var yacht = (extra && extra.yacht_name) || yachtOf(el);
    if (yacht) params.yacht_name = yacht;
    if (extra) {
      for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k) && extra[k] != null && extra[k] !== '') params[k] = extra[k];
    }
    if (!hasGtag()) return params;
    window.gtag('event', name, params);
    if (ADS.id && ADS.labels[name]) {
      window.gtag('event', 'conversion', { send_to: ADS.id + '/' + ADS.labels[name], transport_type: 'beacon' });
    }
    return params;
  }
  window.mycTrack = track;

  if (ADS.id && hasGtag()) window.gtag('config', ADS.id);

  function eventFor(a) {
    var href = a.getAttribute('href') || '';
    if (/^tel:/i.test(href)) return 'phone_click';
    if (/^mailto:/i.test(href)) return 'email_click';
    if (/(^|\/\/)(www\.)?(wa\.me|api\.whatsapp\.com|whatsapp\.com)\//i.test(href) || /^whatsapp:/i.test(href)) {
      // [data-modal] links carry the WhatsApp URL only as a no-JS fallback: with JS they open the modal
      // (reported as modal_open) and the modal's own WhatsApp button reports the real whatsapp_click.
      return a.hasAttribute('data-modal') ? 'modal_open' : 'whatsapp_click';
    }
    if (a.hasAttribute('data-modal')) return 'modal_open';
    return null;
  }

  function onClick(e) {
    if (e.type === 'auxclick' && e.button !== 1) return;
    var a = closest(e.target, 'a[href]');
    if (!a) return;
    var name = eventFor(a);
    if (name) track(name, null, a);
  }

  // Capture phase: fires before any handler that might stop propagation.
  document.addEventListener('click', onClick, true);
  document.addEventListener('auxclick', onClick, true);
})();
