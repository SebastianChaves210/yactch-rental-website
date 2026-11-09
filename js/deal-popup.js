/**
 * Miami Yacht Collective, flash deals phone signup popup (campaign 2026-11-08 to 2026-11-10).
 * Loaded by js/myc-site.js on every page except /pay and the error pages.
 * No dependencies. Talks only to /api/deal-signup. Never logs or tracks the phone number.
 */
(function () {
  'use strict';
  var END = new Date('2026-11-10T23:30:00-05:00');
  if (Date.now() >= END.getTime()) return;
  if (window.__mycDealPopup) return;
  window.__mycDealPopup = true;

  var KEY = 'myc_deal_popup_v1';
  var TOUCH_KEY = 'myc_first_touch_v1';
  var CONSENT_VERSION = '2026-11-08-v1';
  var API = '/api/deal-signup';
  var SHOW_DELAY = 1500;
  var RETRY_DELAY = 6000;

  var COPY = {
    eyebrow: 'Flash deals',
    title: "Don't miss our flash deals",
    body: 'Put your number in and be the first to know when we drop flash deals on yacht charters. The best rates in Miami.',
    label: 'Mobile number',
    codeLabel: 'Country code',
    button: 'Notify me',
    sending: 'Sending…',
    skip: 'No thanks',
    consent: 'I agree to receive recurring marketing texts from Miami Yacht Collective at this number. Consent is not a condition of purchase. Msg and data rates may apply. Reply STOP to opt out.',
    successTitle: "You're on the list.",
    successBody: "We'll text you when the next flash deal drops.",
    close: 'Close',
    errPhone: 'Please enter a valid mobile number.',
    errConsent: 'Please tick the box to agree to receive texts.',
    errRate: 'Too many attempts. Please try again in a few minutes.',
    errGeneric: 'Something went wrong. Please try again.'
  };

  var CODES = [
    ['1', 'US +1', '(305) 555 0123'],
    ['1', 'Canada +1', '(416) 555 0123'],
    ['1', 'Puerto Rico +1', '(787) 555 0123'],
    ['1', 'Dominican Republic +1', '(809) 555 0123'],
    ['55', 'Brazil +55', '11 91234 5678'],
    ['52', 'Mexico +52', '55 1234 5678'],
    ['57', 'Colombia +57', '301 234 5678'],
    ['54', 'Argentina +54', '9 11 1234 5678'],
    ['58', 'Venezuela +58', '412 123 4567'],
    ['56', 'Chile +56', '9 1234 5678'],
    ['51', 'Peru +51', '912 345 678'],
    ['593', 'Ecuador +593', '99 123 4567'],
    ['34', 'Spain +34', '612 34 56 78'],
    ['44', 'UK +44', '7700 900123'],
    ['33', 'France +33', '6 12 34 56 78'],
    ['39', 'Italy +39', '312 345 6789'],
    ['49', 'Germany +49', '1512 3456789'],
    ['972', 'Israel +972', '50 123 4567'],
    ['other', 'Other', '+44 7700 900123']
  ];

  /* ---------------- storage (Instagram in-app browser may throw) ---------------- */
  function lsGet(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* ignore */ } }
  function ssGet(k) { try { return window.sessionStorage.getItem(k); } catch (e) { return null; } }
  function ssSet(k, v) { try { window.sessionStorage.setItem(k, v); } catch (e) { /* ignore */ } }

  /* ---------------- first touch: landing page + UTM, kept for the session ---------------- */
  function parseUtm(search) {
    var out = {}, keys = ['source', 'medium', 'campaign', 'content', 'term'];
    var q = (search || '').replace(/^\?/, '').split('&');
    for (var i = 0; i < q.length; i++) {
      var kv = q[i].split('=');
      var k = decodeURIComponent((kv[0] || '').replace(/\+/g, ' '));
      if (k.indexOf('utm_') !== 0) continue;
      var name = k.slice(4);
      if (keys.indexOf(name) === -1) continue;
      try { out[name] = decodeURIComponent((kv.slice(1).join('=') || '').replace(/\+/g, ' ')).slice(0, 100); } catch (e) { /* skip bad encoding */ }
    }
    return out;
  }
  var touch = null;
  try { touch = JSON.parse(ssGet(TOUCH_KEY) || 'null'); } catch (e) { touch = null; }
  if (!touch || typeof touch !== 'object') {
    touch = { landingPage: location.href.slice(0, 500), utm: parseUtm(location.search) };
    ssSet(TOUCH_KEY, JSON.stringify(touch));
  }

  var state = lsGet(KEY);
  if (state === 'dismissed' || state === 'signed') return;

  /* ---------------- helpers ---------------- */
  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (!Object.prototype.hasOwnProperty.call(attrs, k)) continue;
      if (k === 'text') n.textContent = attrs[k];
      else if (k === 'html') n.innerHTML = attrs[k];
      else n.setAttribute(k, attrs[k]);
    }
    if (children) for (var i = 0; i < children.length; i++) if (children[i]) n.appendChild(children[i]);
    return n;
  }
  function track(name, params) {
    try { if (typeof window.gtag === 'function') window.gtag('event', name, params || {}); } catch (e) { /* ignore */ }
  }
  function countdownText() {
    var ms = END.getTime() - Date.now();
    if (ms <= 0) return '';
    var mins = Math.floor(ms / 60000);
    var days = Math.floor(mins / 1440);
    var hours = Math.floor((mins % 1440) / 60);
    var m = mins % 60;
    if (days >= 1) return 'Signup closes in ' + days + 'd ' + hours + 'h';
    if (hours >= 1) return 'Signup closes in ' + hours + 'h ' + (m < 10 ? '0' + m : m) + 'm';
    if (mins >= 1) return 'Signup closes in ' + mins + 'm';
    return 'Signup closes in under a minute';
  }

  /* Normalise to E.164. Returns null when invalid. */
  function nanpOk(d) {
    return d.length === 10 && /^[2-9]\d{2}[2-9]\d{6}$/.test(d);
  }
  function normalizePhone(code, raw) {
    var s = String(raw || '').trim();
    var digits;
    if (s.charAt(0) === '+') {
      digits = s.slice(1).replace(/\D/g, '');
      if (digits.charAt(0) === '1') return nanpOk(digits.slice(1)) ? '+' + digits : null;
      return /^[1-9]\d{7,14}$/.test(digits) ? '+' + digits : null;
    }
    if (code === 'other') return null;
    digits = s.replace(/\D/g, '');
    if (code === '1') {
      if (digits.length === 11 && digits.charAt(0) === '1') digits = digits.slice(1);
      return nanpOk(digits) ? '+1' + digits : null;
    }
    digits = digits.replace(/^0+/, '');
    var full = code + digits;
    return /^[1-9]\d{7,14}$/.test(full) ? '+' + full : null;
  }

  /* ---------------- styles ---------------- */
  var CSS = '' +
    '.myc-deal-backdrop{position:fixed;inset:0;z-index:10050;display:flex;align-items:flex-end;justify-content:center;background:rgba(8,21,36,.64);opacity:0;transition:opacity .25s ease}' +
    '.myc-deal-backdrop.is-open{opacity:1}' +
    '.myc-deal-card{position:relative;box-sizing:border-box;width:100%;max-width:440px;max-height:calc(100vh - 12px);max-height:calc(100dvh - 12px);overflow-y:auto;-webkit-overflow-scrolling:touch;background:var(--myc-paper,#fdfcf9);color:var(--myc-ink,#0c1f35);border-top:2px solid var(--myc-gold,#c2a15f);border-radius:14px 14px 0 0;padding:24px 20px calc(16px + env(safe-area-inset-bottom));box-shadow:0 -24px 60px -24px rgba(5,13,24,.7);font-family:var(--myc-sans,"Inter Tight",system-ui,sans-serif);transform:translateY(28px);transition:transform .3s ease}' +
    '.myc-deal-backdrop.is-open .myc-deal-card{transform:none}' +
    '.myc-deal-card *{box-sizing:border-box}' +
    '.myc-deal-close{position:absolute;top:8px;right:8px;width:44px;height:44px;display:grid;place-items:center;padding:0;background:none;border:0;border-radius:50%;color:var(--myc-slate,#55677c);cursor:pointer}' +
    '.myc-deal-close:hover{color:var(--myc-ink,#0c1f35);background:rgba(12,31,53,.05)}' +
    '.myc-deal-close svg{width:18px;height:18px}' +
    '.myc-deal-eyebrow{margin:0 0 8px;font:600 .6875rem/1.4 var(--myc-sans,system-ui,sans-serif);letter-spacing:.2em;text-transform:uppercase;color:var(--myc-gold-text,#8a6d33)}' +
    '.myc-deal-title{margin:0 0 10px;padding-right:40px;font:600 1.75rem/1.15 var(--myc-serif,"Cormorant Garamond",Georgia,serif);color:var(--myc-ink,#0c1f35);outline:none}' +
    '.myc-deal-body{margin:0 0 8px;font-size:.9375rem;line-height:1.55;color:#3b4a5c}' +
    '.myc-deal-timer{margin:0 0 16px;font:500 .75rem/1.4 var(--myc-sans,system-ui,sans-serif);letter-spacing:.08em;text-transform:uppercase;color:var(--myc-gold-text,#8a6d33)}' +
    '.myc-deal-label{display:block;margin:0 0 6px;font:600 .6875rem/1.2 var(--myc-sans,system-ui,sans-serif);letter-spacing:.16em;text-transform:uppercase;color:var(--myc-gold-text,#8a6d33)}' +
    '.myc-deal-row{display:flex;gap:8px}' +
    '.myc-deal-select,.myc-deal-input{height:48px;margin:0;border:1px solid var(--myc-hairline,#e2dccb);border-radius:3px;background:#fff;color:var(--myc-ink,#0c1f35);font:400 1rem/1.2 var(--myc-sans,system-ui,sans-serif);padding:0 12px;-webkit-appearance:none;appearance:none}' +
    '.myc-deal-select{flex:0 0 auto;width:7.5em;padding-right:26px;background:#fff url("data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 12 12\'><path d=\'M2 4l4 4 4-4\' fill=\'none\' stroke=\'%230c1f35\' stroke-width=\'1.6\' stroke-linecap=\'round\' stroke-linejoin=\'round\'/></svg>") right 10px center/10px no-repeat;text-overflow:ellipsis;white-space:nowrap;overflow:hidden}' +
    '.myc-deal-input{flex:1 1 auto;min-width:0}' +
    '.myc-deal-input::placeholder{color:#9aa6b2}' +
    '.myc-deal-select:focus,.myc-deal-input:focus{border-color:var(--myc-gold-deep,#a5833f);outline:2px solid var(--myc-gold,#c2a15f);outline-offset:1px}' +
    '.myc-deal-consent{display:flex;gap:10px;align-items:flex-start;margin:12px 0 0;cursor:pointer}' +
    '.myc-deal-consent input{flex:none;width:20px;height:20px;margin:1px 0 0;accent-color:var(--myc-gold-deep,#a5833f);cursor:pointer}' +
    '.myc-deal-consent span{font-size:.75rem;line-height:1.45;color:var(--myc-slate,#55677c)}' +
    '.myc-deal-error{margin:10px 0 0;font-size:.875rem;line-height:1.4;color:#9b2c2c}' +
    '.myc-deal-error:empty{display:none}' +
    '.myc-deal-btn{display:flex;width:100%;height:50px;align-items:center;justify-content:center;margin:14px 0 0;border:0;border-radius:3px;background:var(--myc-ink,#0c1f35);color:#fff;font:600 .8125rem/1 var(--myc-sans,system-ui,sans-serif);letter-spacing:.15em;text-transform:uppercase;cursor:pointer;transition:background-color .3s ease}' +
    '.myc-deal-btn:hover{background:var(--myc-gold-deep,#a5833f)}' +
    '.myc-deal-btn:focus-visible,.myc-deal-skip:focus-visible,.myc-deal-close:focus-visible{outline:2px solid var(--myc-gold,#c2a15f);outline-offset:2px}' +
    '.myc-deal-btn[disabled]{opacity:.65;cursor:default}' +
    '.myc-deal-skip{display:block;width:100%;min-height:44px;margin:2px 0 0;padding:12px;background:none;border:0;color:var(--myc-slate,#55677c);font:500 .8125rem/1.2 var(--myc-sans,system-ui,sans-serif);text-decoration:underline;text-underline-offset:3px;cursor:pointer}' +
    '.myc-deal-skip:hover{color:var(--myc-ink,#0c1f35)}' +
    '.myc-deal-hp{position:absolute!important;left:-9999px!important;top:0;width:1px;height:1px;opacity:0;pointer-events:none}' +
    '.myc-deal-success .myc-deal-title{margin-top:6px}' +
    '.myc-deal-success .myc-deal-body{margin-bottom:18px}' +
    'html.myc-deal-lock,html.myc-deal-lock body{overflow:hidden!important}' +
    '@media (min-width:768px){.myc-deal-backdrop{align-items:center;padding:24px}.myc-deal-card{border-radius:6px;border-top-width:3px;padding:36px 36px 28px;max-height:calc(100vh - 48px);box-shadow:0 30px 80px -30px rgba(5,13,24,.75)}.myc-deal-title{font-size:2rem}.myc-deal-close{top:10px;right:10px}}' +
    '@media (max-height:620px) and (max-width:767px){.myc-deal-card{padding-top:18px}.myc-deal-title{font-size:1.5rem;margin-bottom:6px}.myc-deal-body{font-size:.875rem}.myc-deal-timer{margin-bottom:12px}}' +
    '@media (prefers-reduced-motion:reduce){.myc-deal-backdrop,.myc-deal-card,.myc-deal-btn{transition:none}}';

  /* ---------------- build ---------------- */
  var shownAt = 0, lastFocus = null, timer = null, backdrop = null, card = null;

  function closeIcon() {
    var s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('aria-hidden', 'true'); s.setAttribute('focusable', 'false');
    var p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    p.setAttribute('d', 'M6 6l12 12M18 6L6 18'); p.setAttribute('fill', 'none'); p.setAttribute('stroke', 'currentColor'); p.setAttribute('stroke-width', '1.8'); p.setAttribute('stroke-linecap', 'round');
    s.appendChild(p);
    return s;
  }

  function build() {
    var style = el('style', { id: 'myc-deal-style' }); style.textContent = CSS;
    document.head.appendChild(style);

    var select = el('select', { 'class': 'myc-deal-select', 'aria-label': COPY.codeLabel, name: 'cc', autocomplete: 'tel-country-code' });
    for (var i = 0; i < CODES.length; i++) select.appendChild(el('option', { value: CODES[i][0], text: CODES[i][1] }));
    select.selectedIndex = 0;
    var input = el('input', { 'class': 'myc-deal-input', id: 'myc-deal-phone', type: 'tel', name: 'phone', autocomplete: 'tel-national', inputmode: 'tel', placeholder: CODES[0][2], 'aria-describedby': 'myc-deal-error', required: '' });
    select.addEventListener('change', function () {
      var opt = CODES[select.selectedIndex];
      input.placeholder = opt ? opt[2] : '';
      if (opt && opt[0] === 'other' && !input.value) input.value = '+';
      input.focus();
    });

    var consentBox = el('input', { type: 'checkbox', id: 'myc-deal-consent', name: 'consent' });
    var consent = el('label', { 'class': 'myc-deal-consent', 'for': 'myc-deal-consent' }, [consentBox, el('span', { text: COPY.consent })]);
    var honeypot = el('input', { 'class': 'myc-deal-hp', type: 'text', name: 'company', tabindex: '-1', autocomplete: 'off', 'aria-hidden': 'true' });
    var error = el('p', { 'class': 'myc-deal-error', id: 'myc-deal-error', 'aria-live': 'polite', role: 'status' });
    var btn = el('button', { 'class': 'myc-deal-btn', type: 'submit', text: COPY.button });
    var skip = el('button', { 'class': 'myc-deal-skip', type: 'button', text: COPY.skip });

    var form = el('form', { 'class': 'myc-deal-form', novalidate: '' }, [
      el('label', { 'class': 'myc-deal-label', 'for': 'myc-deal-phone', text: COPY.label }),
      el('div', { 'class': 'myc-deal-row' }, [select, input]),
      consent, honeypot, error, btn, skip
    ]);

    var title = el('h2', { 'class': 'myc-deal-title', id: 'myc-deal-title', tabindex: '-1', text: COPY.title });
    var body = el('p', { 'class': 'myc-deal-body', text: COPY.body });
    var countdown = el('p', { 'class': 'myc-deal-timer', text: countdownText() });
    var closeBtn = el('button', { 'class': 'myc-deal-close', type: 'button', 'aria-label': COPY.close }, [closeIcon()]);

    card = el('div', { 'class': 'myc-deal-card', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'myc-deal-title' }, [
      closeBtn, el('p', { 'class': 'myc-deal-eyebrow', text: COPY.eyebrow }), title, body, countdown, form
    ]);
    backdrop = el('div', { 'class': 'myc-deal-backdrop' }, [card]);

    closeBtn.addEventListener('click', function () { dismiss(); });
    skip.addEventListener('click', function () { dismiss(); });
    backdrop.addEventListener('mousedown', function (e) { if (e.target === backdrop) backdrop.__down = true; });
    backdrop.addEventListener('click', function (e) {
      if (e.target === backdrop && backdrop.__down) dismiss();
      backdrop.__down = false;
    });
    backdrop.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' || e.key === 'Esc') { e.preventDefault(); dismiss(); return; }
      if (e.key !== 'Tab') return;
      var focusables = card.querySelectorAll('button:not([disabled]),input:not([tabindex="-1"]),select,[tabindex="0"]');
      if (!focusables.length) return;
      var first = focusables[0], last = focusables[focusables.length - 1];
      if (e.shiftKey && (document.activeElement === first || document.activeElement === title)) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      error.textContent = '';
      var phone = normalizePhone(select.value, input.value);
      if (!phone) { error.textContent = COPY.errPhone; input.focus(); return; }
      if (!consentBox.checked) { error.textContent = COPY.errConsent; consentBox.focus(); return; }
      if (typeof window.fetch !== 'function') { error.textContent = COPY.errGeneric; return; }
      btn.disabled = true; btn.textContent = COPY.sending;
      var payload = {
        phone: phone,
        consent: true,
        consentText: COPY.consent,
        consentVersion: CONSENT_VERSION,
        page: location.href.slice(0, 500),
        referrer: (document.referrer || '').slice(0, 500),
        utm: touch.utm || {},
        landingPage: touch.landingPage || '',
        company: honeypot.value,
        elapsedMs: Date.now() - shownAt
      };
      window.fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload), credentials: 'same-origin' })
        .then(function (r) { return r.json().then(function (j) { return { status: r.status, ok: r.ok && j && j.ok === true }; }, function () { return { status: r.status, ok: false }; }); })
        .then(function (r) {
          if (r.ok) { success(); return; }
          error.textContent = r.status === 429 ? COPY.errRate : COPY.errGeneric;
          btn.disabled = false; btn.textContent = COPY.button;
        })
        .catch(function () {
          error.textContent = COPY.errGeneric;
          btn.disabled = false; btn.textContent = COPY.button;
        });
    });

    function success() {
      lsSet(KEY, 'signed');
      track('deal_signup', { page_path: location.pathname });
      card.classList.add('myc-deal-success');
      title.textContent = COPY.successTitle;
      body.textContent = COPY.successBody;
      countdown.parentNode.removeChild(countdown);
      var done = el('button', { 'class': 'myc-deal-btn', type: 'button', text: COPY.close });
      done.addEventListener('click', function () { close(); });
      card.replaceChild(done, form);
      done.focus();
    }

    document.body.appendChild(backdrop);
    timer = window.setInterval(function () {
      if (Date.now() >= END.getTime()) { close(); return; }
      if (countdown.parentNode) countdown.textContent = countdownText();
    }, 60000);
  }

  function dismiss() { lsSet(KEY, 'dismissed'); close(); }

  function close() {
    if (!backdrop) return;
    if (timer) { window.clearInterval(timer); timer = null; }
    document.documentElement.classList.remove('myc-deal-lock');
    var node = backdrop; backdrop = null;
    node.classList.remove('is-open');
    var remove = function () { if (node.parentNode) node.parentNode.removeChild(node); };
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) remove(); else window.setTimeout(remove, 260);
    if (lastFocus && typeof lastFocus.focus === 'function') { try { lastFocus.focus({ preventScroll: true }); } catch (e) { lastFocus.focus(); } }
  }

  function blocked() {
    return !!document.querySelector('.modal-backdrop.active') || document.documentElement.classList.contains('myc-menu-open');
  }

  function show(retry) {
    if (Date.now() >= END.getTime()) return;
    if (lsGet(KEY) === 'dismissed' || lsGet(KEY) === 'signed') return;
    if (blocked()) { if (retry) window.setTimeout(function () { show(false); }, RETRY_DELAY); return; }
    lastFocus = document.activeElement;
    build();
    document.documentElement.classList.add('myc-deal-lock');
    shownAt = Date.now();
    /* next frame so the transition runs */
    window.requestAnimationFrame(function () {
      if (!backdrop) return;
      backdrop.classList.add('is-open');
      var t = document.getElementById('myc-deal-title');
      if (t) { try { t.focus({ preventScroll: true }); } catch (e) { t.focus(); } }
    });
    track('deal_popup_view');
  }

  if (document.readyState === 'complete') window.setTimeout(function () { show(true); }, SHOW_DELAY);
  else window.addEventListener('load', function () { window.setTimeout(function () { show(true); }, SHOW_DELAY); });
})();
