'use strict';
/**
 * POST /api/deal-signup
 * Stores a flash-deal SMS signup as a private JSON object in the Vercel Blob store
 * `myc-deal-signups` (BLOB_READ_WRITE_TOKEN is set on the project).
 *
 * Vercel Node.js serverless function (CommonJS). Never echoes or logs the phone number.
 *
 * Rate limit: best effort, in memory per IP (5 requests / 10 minutes). The Map lives in
 * one function instance, so it resets on cold start and is not shared across instances or
 * regions. Good enough to slow down a naive script, not a security boundary.
 */

const crypto = require('crypto');

const MAX_BODY = 4096;
const RATE_LIMIT = 5;
const RATE_WINDOW_MS = 10 * 60 * 1000;
const MIN_ELAPSED_MS = 1500;
const IP_SALT = process.env.DEAL_SIGNUP_IP_SALT || 'myc-deal-signups-2026-11-salt-v1';

const ALLOWED_ORIGINS = [
  /^https:\/\/miamiyachtcollective\.com$/,
  /^https:\/\/www\.miamiyachtcollective\.com$/,
  /^https:\/\/yactch-rental-website(-[a-z0-9-]+)?\.vercel\.app$/,
  /^http:\/\/localhost(:\d+)?$/,
  /^http:\/\/127\.0\.0\.1(:\d+)?$/,
];

// Injectable for tests: deps.put defaults to @vercel/blob's put() on first use.
const deps = { put: null };
function getPut() {
  if (!deps.put) deps.put = require('@vercel/blob').put;
  return deps.put;
}

const hits = new Map(); // ip -> [timestamps]
function rateLimited(ip) {
  const now = Date.now();
  const arr = (hits.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  if (arr.length >= RATE_LIMIT) { hits.set(ip, arr); return true; }
  arr.push(now);
  hits.set(ip, arr);
  if (hits.size > 5000) {
    for (const [k, v] of hits) if (!v.length || now - v[v.length - 1] >= RATE_WINDOW_MS) hits.delete(k);
  }
  return false;
}

function send(res, status, body, extraHeaders) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  if (extraHeaders) for (const k of Object.keys(extraHeaders)) res.setHeader(k, extraHeaders[k]);
  res.end(JSON.stringify(body));
}

function header(req, name) {
  const v = req.headers && req.headers[name];
  return Array.isArray(v) ? v[0] : (v || '');
}

function clientIp(req) {
  const xff = header(req, 'x-forwarded-for');
  const first = xff.split(',')[0].trim();
  return first || header(req, 'x-real-ip') || (req.socket && req.socket.remoteAddress) || 'unknown';
}

function readBody(req) {
  // Vercel's Node helper may have parsed the JSON body already.
  if (req.body !== undefined && req.body !== null) {
    if (typeof req.body === 'string') {
      if (Buffer.byteLength(req.body) > MAX_BODY) return Promise.reject(Object.assign(new Error('too large'), { code: 413 }));
      return Promise.resolve(req.body);
    }
    if (Buffer.isBuffer(req.body)) {
      if (req.body.length > MAX_BODY) return Promise.reject(Object.assign(new Error('too large'), { code: 413 }));
      return Promise.resolve(req.body.toString('utf8'));
    }
    if (typeof req.body === 'object') return Promise.resolve(req.body);
  }
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    let done = false;
    const fail = (code) => { if (done) return; done = true; reject(Object.assign(new Error('body'), { code })); };
    req.on('data', (c) => {
      size += c.length;
      if (size > MAX_BODY) { fail(413); if (typeof req.destroy === 'function') req.destroy(); return; }
      chunks.push(c);
    });
    req.on('end', () => { if (!done) { done = true; resolve(Buffer.concat(chunks).toString('utf8')); } });
    req.on('error', () => fail(400));
  });
}

function clip(v, n) {
  return typeof v === 'string' ? v.slice(0, n) : '';
}

function validPhone(phone) {
  if (typeof phone !== 'string' || !/^\+[1-9]\d{7,14}$/.test(phone)) return false;
  if (phone.startsWith('+1')) return /^\+1[2-9]\d{2}[2-9]\d{6}$/.test(phone);
  return true;
}

function decodeCity(v) {
  try { return decodeURIComponent(v).slice(0, 100); } catch (e) { return clip(v, 100); }
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return send(res, 405, { ok: false, error: 'method_not_allowed' }, { Allow: 'POST' });
  }
  const ctype = header(req, 'content-type').toLowerCase();
  if (ctype.indexOf('application/json') !== 0) {
    return send(res, 415, { ok: false, error: 'unsupported_media_type' });
  }
  const origin = header(req, 'origin');
  if (origin && !ALLOWED_ORIGINS.some((re) => re.test(origin))) {
    return send(res, 403, { ok: false, error: 'forbidden' });
  }
  const len = parseInt(header(req, 'content-length'), 10);
  if (len > MAX_BODY) return send(res, 413, { ok: false, error: 'payload_too_large' });

  const ip = clientIp(req);
  if (rateLimited(ip)) return send(res, 429, { ok: false, error: 'rate_limited' }, { 'Retry-After': '600' });

  let data;
  try {
    const raw = await readBody(req);
    data = typeof raw === 'string' ? JSON.parse(raw) : raw;
  } catch (e) {
    return send(res, e && e.code === 413 ? 413 : 400, { ok: false, error: 'bad_request' });
  }
  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return send(res, 400, { ok: false, error: 'bad_request' });
  }

  // Bots: honeypot filled or submitted faster than a human could. Pretend success, store nothing.
  const elapsed = typeof data.elapsedMs === 'number' && isFinite(data.elapsedMs) ? data.elapsedMs : 0;
  if ((typeof data.company === 'string' && data.company.trim() !== '') || elapsed < MIN_ELAPSED_MS) {
    return send(res, 200, { ok: true });
  }

  if (!validPhone(data.phone)) return send(res, 400, { ok: false, error: 'invalid_phone' });
  if (data.consent !== true) return send(res, 400, { ok: false, error: 'consent_required' });

  const utmIn = data.utm && typeof data.utm === 'object' && !Array.isArray(data.utm) ? data.utm : {};
  const utm = {};
  for (const k of ['source', 'medium', 'campaign', 'content', 'term']) {
    if (typeof utmIn[k] === 'string' && utmIn[k]) utm[k] = utmIn[k].slice(0, 100);
  }

  const createdAt = new Date();
  const iso = createdAt.toISOString();
  const record = {
    phone: data.phone,
    consent: true,
    consentText: clip(data.consentText, 600),
    consentVersion: clip(data.consentVersion, 40),
    createdAt: iso,
    page: clip(data.page, 500),
    referrer: clip(data.referrer, 500),
    utm,
    landingPage: clip(data.landingPage, 500),
    userAgent: clip(header(req, 'user-agent'), 300),
    country: clip(header(req, 'x-vercel-ip-country'), 8),
    city: decodeCity(header(req, 'x-vercel-ip-city')),
    ipHash: crypto.createHash('sha256').update(ip + IP_SALT).digest('hex').slice(0, 16),
  };

  const month = iso.slice(0, 7);
  const pathname = 'deal-signups/' + month + '/' + iso.replace(/:/g, '-') + '-' + crypto.randomUUID() + '.json';

  try {
    await getPut()(pathname, JSON.stringify(record), {
      access: 'private',
      addRandomSuffix: false,
      contentType: 'application/json',
    });
  } catch (e) {
    console.error('deal-signup: blob put failed', e && e.name, e && e.message ? String(e.message).slice(0, 200) : '');
    return send(res, 500, { ok: false, error: 'storage_failed' });
  }

  return send(res, 200, { ok: true });
};

module.exports._deps = deps;
module.exports._resetRateLimit = () => hits.clear();
