/**
 * Miami Yacht Collective — shared site behaviour (2026-10-28)
 * Header dropdowns (hover + keyboard + touch), full-screen mobile menu,
 * gallery lightbox, WhatsApp booking widget, fleet filters.
 * No dependencies. Loaded with `defer` on every page.
 */
(function () {
  'use strict';
  var html = document.documentElement;
  var WA = 'https://wa.me/17876645040?text=';

  /* ---------------- header ---------------- */
  var header = document.getElementById('myc-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 24); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    var items = Array.prototype.slice.call(header.querySelectorAll('.myc-has-menu'));
    function setOpen(li, open) {
      li.classList.toggle('is-open', open);
      li.querySelector('.myc-nav-toggle').setAttribute('aria-expanded', String(open));
    }
    function closeAll(except) {
      items.forEach(function (li) { if (li !== except) setOpen(li, false); });
    }
    items.forEach(function (li) {
      var btn = li.querySelector('.myc-nav-toggle');
      var menu = li.querySelector('.myc-menu');
      var timer;
      btn.addEventListener('click', function () {
        var open = !li.classList.contains('is-open');
        closeAll(li);
        setOpen(li, open);
      });
      li.addEventListener('pointerenter', function (e) {
        if (e.pointerType !== 'mouse') return;
        clearTimeout(timer);
        closeAll(li);
        setOpen(li, true);
      });
      li.addEventListener('pointerleave', function (e) {
        if (e.pointerType !== 'mouse') return;
        timer = setTimeout(function () { setOpen(li, false); }, 140);
      });
      li.addEventListener('focusout', function (e) {
        if (!li.contains(e.relatedTarget)) setOpen(li, false);
      });
      li.addEventListener('keydown', function (e) {
        var links = Array.prototype.slice.call(menu.querySelectorAll('a'));
        var i = links.indexOf(document.activeElement);
        if (e.key === 'Escape') { e.preventDefault(); setOpen(li, false); btn.focus(); }
        else if (e.key === 'ArrowDown') {
          e.preventDefault();
          if (!li.classList.contains('is-open')) { closeAll(li); setOpen(li, true); }
          (links[i + 1] || links[0]).focus();
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          if (i > 0) links[i - 1].focus(); else btn.focus();
        } else if (e.key === 'Home' && i >= 0) { e.preventDefault(); links[0].focus(); }
        else if (e.key === 'End' && i >= 0) { e.preventDefault(); links[links.length - 1].focus(); }
      });
    });
    document.addEventListener('click', function (e) { if (!header.contains(e.target)) closeAll(); });

    var burger = header.querySelector('.myc-burger');
    var panel = document.getElementById('myc-mobile');
    if (burger && panel) {
      var setMenu = function (open) {
        panel.hidden = !open;
        burger.setAttribute('aria-expanded', String(open));
        burger.setAttribute('aria-label', open ? burger.getAttribute('data-label-close') : burger.getAttribute('data-label-open'));
        html.classList.toggle('myc-menu-open', open);
        if (window.mycLenis) { if (open) window.mycLenis.stop(); else window.mycLenis.start(); }
        if (open) {
          var first = panel.querySelector('button, a');
          if (first) first.focus();
        }
      };
      burger.addEventListener('click', function () { setMenu(panel.hidden); if (!panel.hidden) return; burger.focus(); });
      panel.querySelectorAll('.myc-m-toggle').forEach(function (b) {
        b.addEventListener('click', function () {
          var sub = document.getElementById(b.getAttribute('aria-controls'));
          var open = b.getAttribute('aria-expanded') === 'true';
          b.setAttribute('aria-expanded', String(!open));
          if (sub) sub.hidden = open;
        });
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !panel.hidden) { setMenu(false); burger.focus(); }
        if (e.key === 'Tab' && !panel.hidden) {
          var f = panel.querySelectorAll('a[href], button');
          var first = burger, last = f[f.length - 1];
          if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
          else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
        }
      });
      var mq = window.matchMedia('(min-width: 992px)');
      var onMq = function (m) { if (m.matches && !panel.hidden) setMenu(false); };
      if (mq.addEventListener) mq.addEventListener('change', onMq); else mq.addListener(onMq);
    }
  }

  /* ---------------- lightbox ---------------- */
  var gal = document.querySelector('[data-lightbox]');
  if (gal && window.HTMLDialogElement) {
    var photos = Array.prototype.slice.call(gal.querySelectorAll('a[data-full]')).map(function (a) {
      return { src: a.getAttribute('href'), alt: a.getAttribute('data-alt') || '' };
    });
    var dlg = document.createElement('dialog');
    dlg.className = 'myc-lightbox';
    dlg.setAttribute('aria-label', gal.getAttribute('data-lightbox-label') || 'Photo gallery');
    dlg.innerHTML =
      '<div class="myc-lb-inner">' +
      '<div class="myc-lb-stage"><img class="myc-lb-img" alt=""></div>' +
      '<div class="myc-lb-bar"><p class="myc-lb-cap"></p><p class="myc-lb-count"></p></div>' +
      '<button type="button" class="myc-lb-btn myc-lb-close" aria-label="Close"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M3 3l12 12M15 3L3 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></button>' +
      '<button type="button" class="myc-lb-btn myc-lb-prev" aria-label="Previous photo"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M11 3L5 9l6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
      '<button type="button" class="myc-lb-btn myc-lb-next" aria-label="Next photo"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M7 3l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
      '</div>';
    document.body.appendChild(dlg);
    var img = dlg.querySelector('.myc-lb-img'), cap = dlg.querySelector('.myc-lb-cap'), count = dlg.querySelector('.myc-lb-count');
    var idx = 0, opener = null;
    function show(i) {
      idx = (i + photos.length) % photos.length;
      img.src = photos[idx].src;
      img.alt = photos[idx].alt;
      cap.textContent = photos[idx].alt;
      count.textContent = (idx + 1) + ' / ' + photos.length;
      var pre = new Image(); pre.src = photos[(idx + 1) % photos.length].src;
    }
    function openAt(i, el) {
      opener = el || null;
      show(i);
      dlg.showModal();
      if (window.mycLenis) window.mycLenis.stop();
      dlg.querySelector('.myc-lb-close').focus();
    }
    dlg.addEventListener('close', function () {
      if (window.mycLenis) window.mycLenis.start();
      if (opener && opener.focus) opener.focus();
    });
    dlg.querySelector('.myc-lb-close').addEventListener('click', function () { dlg.close(); });
    dlg.querySelector('.myc-lb-prev').addEventListener('click', function () { show(idx - 1); });
    dlg.querySelector('.myc-lb-next').addEventListener('click', function () { show(idx + 1); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.classList.contains('myc-lb-stage') || e.target.classList.contains('myc-lb-inner')) dlg.close(); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
    });
    var tx = 0;
    dlg.addEventListener('touchstart', function (e) { tx = e.changedTouches[0].clientX; }, { passive: true });
    dlg.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - tx;
      if (Math.abs(dx) > 48) show(dx < 0 ? idx + 1 : idx - 1);
    }, { passive: true });
    gal.querySelectorAll('a[data-full]').forEach(function (a, i) {
      a.addEventListener('click', function (e) { e.preventDefault(); openAt(i, a); });
    });
    var more = document.querySelector('[data-lightbox-open]');
    if (more) more.addEventListener('click', function () { openAt(0, more); });
  }

  /* ---------------- WhatsApp booking forms ---------------- */
  document.querySelectorAll('form[data-wa-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var hp = form.querySelector('.myc-hp input, input.myc-hp');
      if (hp && hp.value) return;
      if (form.reportValidity && !form.reportValidity()) return;
      var msg = form.getAttribute('data-wa-template') || "Hi! I'd like to book a private yacht in Miami.";
      var data = new FormData(form);
      var parts = [];
      msg = msg.replace(/\{(\w+)\}/g, function (_, k) {
        var v = (data.get(k) || '').toString().trim();
        if (k === 'date' && v) {
          var d = new Date(v + 'T12:00:00');
          if (!isNaN(d)) v = d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
        }
        return v;
      });
      msg = msg.replace(/\s{2,}/g, ' ').replace(/\s([.,])/g, '$1').trim();
      var yacht = form.querySelector('[name="yacht"]');
      if (yacht && yacht.value && msg.indexOf(yacht.value) === -1 && !/\{yacht\}/.test(form.getAttribute('data-wa-template') || '')) {
        msg = msg.replace(/^Hi!/, 'Hi! I\'m interested in the ' + yacht.value + '.');
      }
      var url = WA + encodeURIComponent(msg);
      var win = window.open(url, '_blank', 'noopener');
      // GA4 whatsapp_click for forms that compose a WhatsApp message (handler in /js/tracking.js)
      if (window.mycTrack) window.mycTrack('whatsapp_click', {
        link_location: form.closest('.myc-fallback') ? 'booking_form' : 'booking_widget',
        link_url: url,
        yacht_name: yacht && /^\d{2}' /.test(yacht.value) ? yacht.value : undefined  // fleet names only, not "right yacht for my group"
      }, form);
      if (!win) location.href = url;
    });
  });
  var dateInputs = document.querySelectorAll('input[type="date"][data-min-today]');
  if (dateInputs.length) {
    var today = new Date(); var iso = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
    dateInputs.forEach(function (i) { i.min = iso; });
  }

  /* ---------------- fleet filters ---------------- */
  var grid = document.querySelector('[data-filter-grid]');
  if (grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.myc-card'));
    var state = { size: 'all', budget: 'all', feature: 'all' };
    var status = document.querySelector('[data-filter-status]');
    var empty = document.querySelector('[data-filter-empty]');
    function matches(card) {
      var len = +card.getAttribute('data-length'), price = +card.getAttribute('data-price'), feat = card.getAttribute('data-feature') || '';
      var okSize = state.size === 'all' || (state.size === 'small' && len < 40) || (state.size === 'mid' && len >= 40 && len < 70) || (state.size === 'large' && len >= 70);
      var okBudget = state.budget === 'all' || (state.budget === 'b1' && price < 1500) || (state.budget === 'b2' && price >= 1500 && price <= 3000) || (state.budget === 'b3' && price > 3000);
      var okFeat = state.feature === 'all' || feat.indexOf(state.feature) !== -1;
      return okSize && okBudget && okFeat;
    }
    function apply() {
      var shown = 0;
      cards.forEach(function (c) { var m = matches(c); c.hidden = !m; if (m) shown++; });
      if (status) status.textContent = shown === cards.length ? 'Showing all ' + shown + ' yachts' : 'Showing ' + shown + ' of ' + cards.length + ' yachts';
      if (empty) empty.hidden = shown !== 0;
    }
    document.querySelectorAll('.myc-filter').forEach(function (b) {
      b.addEventListener('click', function () {
        var group = b.getAttribute('data-group'), val = b.getAttribute('data-value');
        state[group] = val;
        document.querySelectorAll('.myc-filter[data-group="' + group + '"]').forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        apply();
      });
    });
    var reset = document.querySelector('[data-filter-reset]');
    if (reset) reset.addEventListener('click', function () {
      state = { size: 'all', budget: 'all', feature: 'all' };
      document.querySelectorAll('.myc-filter').forEach(function (o) { o.setAttribute('aria-pressed', String(o.getAttribute('data-value') === 'all')); });
      apply();
    });
    apply();
  }
})();
