/**
 * GA4 Event Tracking for Miami Yacht Collective
 * Tracks: modal_open, call_click, whatsapp_click
 * (with cta_location: modal | sticky | header | footer | widget | card | inline)
 */
(function () {
  'use strict';

  function getPageName() {
    var path = window.location.pathname.replace(/\/$/, '');
    if (!path || path === '') return 'home';
    return path.split('/').pop().replace('.html', '');
  }

  var pageName = getPageName();

  function location_of(el) {
    if (el.classList.contains('modal-btn')) return 'modal';
    if (!el.closest) return 'inline';
    if (el.closest('.myc-sticky-cta')) return 'sticky';
    if (el.closest('.myc-header')) return 'header';
    if (el.closest('.myc-footer')) return 'footer';
    if (el.closest('.myc-widget')) return 'widget';
    if (el.closest('.myc-card')) return 'card';
    return 'inline';
  }

  function send(name, el) {
    if (typeof gtag !== 'function') return;
    gtag('event', name, { page_name: pageName, cta_location: location_of(el), transport_type: 'beacon' });
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

  // [data-modal] links carry the WhatsApp URL as a no-JS fallback but open the modal instead
  document.querySelectorAll('a[href*="wa.me/"]:not([data-modal])').forEach(function (el) {
    el.addEventListener('click', function () { send('whatsapp_click', el); });
  });
})();
