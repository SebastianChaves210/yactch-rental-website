# Flash deal signups (private)

Phone signups from the sitewide flash deals popup (`js/deal-popup.js`) are posted to
`api/deal-signup.js`, which writes one JSON object per signup to the **private** Vercel Blob
store `myc-deal-signups` under `deal-signups/<YYYY-MM>/<timestamp>-<uuid>.json`.

Each record: `phone` (E.164), `consent`, `consentText`, `consentVersion`, `createdAt`, `page`,
`referrer`, `utm`, `landingPage`, `userAgent`, `country`, `city`, `ipHash` (salted, truncated;
the raw IP is never stored). The phone number is never echoed in responses, logs or analytics.

This folder is listed in `.vercelignore` and is never deployed.

## Export to CSV

Run from the repo root (needs `node_modules/@vercel/blob`, installed by `npm install`):

```bash
vercel env pull .env.blob --environment=production
node --env-file=.env.blob tools/deal-signups/list-signups.mjs > signups.csv
```

Columns: `createdAt, phone, page, utm_source, utm_campaign, country, pathname`.
`.csv` files are git-ignored. Delete `.env.blob` when done; it holds the read/write token.

## Delete one record (for example a test entry)

```bash
node --env-file=.env.blob tools/deal-signups/list-signups.mjs --delete deal-signups/2026-11/<file>.json
```

## Notes

- The API rate limit (5 requests per IP per 10 minutes) is in memory per function instance.
- The popup stops loading at `2026-11-10 23:30 America/New_York` (hard coded in both
  `js/myc-site.js` and `js/deal-popup.js`). The API stays live; remove `api/deal-signup.js`
  after the campaign if it is no longer needed.
