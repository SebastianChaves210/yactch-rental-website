#!/bin/sh
# Ping Bing/IndexNow after a production deploy.
# Usage: scripts/indexnow.sh            -> submits every URL in the live sitemap
#        scripts/indexnow.sh URL [URL]  -> submits only those URLs
KEY=e91e0740976e7f9f45f60b1d49ba39cb
HOST=miamiyachtcollective.com
if [ $# -gt 0 ]; then
  URLS=$(printf '%s\n' "$@")
else
  URLS=$(curl -s "https://$HOST/sitemap.xml" | grep -o '<loc>[^<]*' | sed 's/<loc>//')
fi
BODY=$(printf '%s\n' "$URLS" | python3 -c "
import sys,json
u=[l.strip() for l in sys.stdin if l.strip()]
print(json.dumps({'host':'$HOST','key':'$KEY','keyLocation':'https://$HOST/$KEY.txt','urlList':u}))")
curl -s -o /dev/null -w "IndexNow: %{http_code} (200/202 = accepted)\n" -X POST \
  -H "Content-Type: application/json; charset=utf-8" --data "$BODY" https://api.indexnow.org/indexnow
