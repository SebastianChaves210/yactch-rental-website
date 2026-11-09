#!/usr/bin/env node
/**
 * Private retrieval tool for flash-deal SMS signups (not deployed; tools/ is in .vercelignore).
 *
 * Usage (from the repo root so @vercel/blob resolves from node_modules):
 *   vercel env pull .env.blob --environment=production
 *   node --env-file=.env.blob tools/deal-signups/list-signups.mjs > signups.csv
 *   node --env-file=.env.blob tools/deal-signups/list-signups.mjs --delete deal-signups/2026-11/<file>.json
 *
 * Reads BLOB_READ_WRITE_TOKEN from the environment. Prints CSV to stdout, progress to stderr.
 */
import { list, get, del } from '@vercel/blob';

const PREFIX = 'deal-signups/';
const COLUMNS = ['createdAt', 'phone', 'page', 'utm_source', 'utm_campaign', 'country', 'pathname'];

if (!process.env.BLOB_READ_WRITE_TOKEN) {
  console.error('BLOB_READ_WRITE_TOKEN is not set. Run: vercel env pull .env.blob --environment=production');
  process.exit(1);
}

const args = process.argv.slice(2);
const delIdx = args.indexOf('--delete');
if (delIdx !== -1) {
  const target = args[delIdx + 1];
  if (!target || !target.startsWith(PREFIX)) {
    console.error('Usage: --delete <pathname starting with ' + PREFIX + '>');
    process.exit(1);
  }
  await del(target);
  console.error('Deleted ' + target);
  process.exit(0);
}

function csv(v) {
  const s = v === undefined || v === null ? '' : String(v);
  return /[",\r\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

async function readJson(pathname) {
  const result = await get(pathname, { access: 'private', useCache: false });
  if (!result || !result.stream) return null;
  const text = await new Response(result.stream).text();
  try { return JSON.parse(text); } catch (e) { return { parseError: true, raw: text.slice(0, 200) }; }
}

const blobs = [];
let cursor;
do {
  const page = await list({ prefix: PREFIX, cursor, limit: 1000 });
  blobs.push(...page.blobs);
  cursor = page.hasMore ? page.cursor : undefined;
} while (cursor);
console.error('Found ' + blobs.length + ' signup record(s)');

process.stdout.write(COLUMNS.join(',') + '\n');
const BATCH = 8;
for (let i = 0; i < blobs.length; i += BATCH) {
  const slice = blobs.slice(i, i + BATCH);
  const rows = await Promise.all(slice.map(async (b) => {
    const r = await readJson(b.pathname);
    if (!r) return null;
    return [
      r.createdAt || b.uploadedAt,
      r.phone,
      r.page,
      r.utm && r.utm.source,
      r.utm && r.utm.campaign,
      r.country,
      b.pathname,
    ].map(csv).join(',');
  }));
  for (const row of rows) if (row) process.stdout.write(row + '\n');
}
