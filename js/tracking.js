/**
 * GA4 Event Tracking for Miami Yacht Collective
 * Tracks: modal_open, call_click, whatsapp_click (with cta_location: modal | sticky | inline)
 */
(function () {
  'use strict';

  function getPageName() {
    var path = window.location.pathname.replace(/\/$/, '');
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
