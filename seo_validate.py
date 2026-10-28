#!/usr/bin/env python3
"""Acceptance checks for miamiyachtcollective.com (rewritten 2026-10-28 for the clean-URL IA).

    python3 seo_validate.py              # file-system checks + crawl
    python3 seo_validate.py --base http://localhost:8000   # also verify sitemap URLs and old-URL redirects over HTTP

Checks every served page (root + yachts/ experiences/ destinations/ events/ guides/; pay/, utility/ and the
redirected Webflow template artifacts are excluded):
  1 H1 · unique <title> <= 60 · unique meta description <= 155 · self canonical · OG + Twitter tags · lang
  JSON-LD parses, BreadcrumbList on every page but home · every <img> has alt text (decorative: alt="" + role="presentation")
  every internal link uses the final URL (no .html, no trailing slash, no redirect-only path) and opens in the same tab
  no skipped heading levels · tel: only the business number · no competitor names
  crawl from /: no broken internal links, no orphan pages (every sitemap URL is linked from a hub and from the nav/footer directly or via its hub)
  sitemap: only final 200 URLs, no noindex pages, hreflang alternates symmetric
Exit status 1 when anything fails.
"""
import json, os, re, sys, html
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
SITE = "https://miamiyachtcollective.com"
EXCLUDE_DIRS = {"pay", "utility", "node_modules", "app", "public", "seo-audit-output", "seo-tools", "scripts", "screenshots", ".next", ".playwright-mcp", "current-site"}
EXCLUDE_FILES = {"logo-preview.html", "search.html", "401.html"}
HUBS = {"/", "/yachts", "/experiences", "/destinations", "/events", "/guides", "/prices", "/faq"}
ALLOWED_TEL = {"tel:+17876645040", "tel:7876645040"}
COMPETITORS = ["royal"]
BASE = None
if "--base" in sys.argv:
    BASE = sys.argv[sys.argv.index("--base") + 1].rstrip("/")

failures = []
warnings = []


def fail(page, msg):
    failures.append(f"{page}: {msg}")


def warn(page, msg):
    warnings.append(f"{page}: {msg}")


def served_pages():
    out = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in EXCLUDE_DIRS or rel.name.startswith("detail_") or rel.name in EXCLUDE_FILES or len(rel.parts) > 2:
            continue
        out.append(rel.as_posix())
    return sorted(out)


def url_for_file(f):
    if f == "index.html":
        return "/"
    if f.endswith("/index.html"):
        return "/" + f[:-11]
    return "/" + f[:-5]


def file_for_url(u):
    """Resolve a clean URL to a file the way Vercel would (no redirects)."""
    path = urlsplit(u).path
    if path == "/":
        return "index.html"
    if path.endswith("/") or path.endswith(".html"):
        return None  # would redirect (trailingSlash:false / cleanUrls)
    rel = path.lstrip("/")
    if (ROOT / (rel + ".html")).is_file():
        return rel + ".html"
    if (ROOT / rel / "index.html").is_file():
        return rel + "/index.html"
    if (ROOT / rel).is_file():
        return rel  # asset
    return None


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self.desc = None; self.canonical = None; self.lang = None; self.robots = ""
        self.og = {}; self.tw = {}; self.hreflang = []
        self.h = []  # (level, text)
        self.imgs = []; self.links = []  # (href, target, in_chrome)
        self.ld = []
        self._tag = None; self._buf = ""; self._ld = False
        self._chrome = 0; self._depth = []
        self.tels = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("header", "footer") and "myc-" in (a.get("class") or ""):
            self._chrome += 1; self._depth.append(tag)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._tag = "title"; self._buf = ""
        elif tag == "meta":
            n = (a.get("name") or "").lower(); p = (a.get("property") or "").lower()
            if n == "description": self.desc = a.get("content", "")
            if n == "robots": self.robots = a.get("content", "")
            if p.startswith("og:"): self.og[p] = a.get("content", "")
            if n.startswith("twitter:"): self.tw[n] = a.get("content", "")
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel == "canonical": self.canonical = a.get("href")
            if rel == "alternate" and a.get("hreflang"): self.hreflang.append((a["hreflang"], a.get("href")))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._tag = tag; self._buf = ""
        elif tag == "img":
            self.imgs.append((a.get("src", ""), a.get("alt"), a.get("role")))
        elif tag == "a":
            href = a.get("href")
            if href:
                self.links.append((href, a.get("target"), self._chrome > 0))
                if href.startswith("tel:"): self.tels.add(href)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True; self._buf = ""

    def handle_endtag(self, tag):
        if tag in ("header", "footer") and self._depth and self._depth[-1] == tag:
            self._depth.pop(); self._chrome -= 1
        if tag == "title" and self._tag == "title":
            self.title = re.sub(r"\s+", " ", self._buf).strip(); self._tag = None
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._tag == tag:
            self.h.append((int(tag[1]), re.sub(r"\s+", " ", self._buf).strip())); self._tag = None
        elif tag == "script" and self._ld:
            self.ld.append(self._buf); self._ld = False

    def handle_data(self, data):
        if self._tag or self._ld:
            self._buf += data


def check_page(f, raw, seen_titles, seen_descs):
    url = url_for_file(f)
    p = Page(); p.feed(raw)
    is_404 = f == "404.html"
    noindex = "noindex" in p.robots
    # title / description
    if not p.title: fail(f, "missing <title>")
    elif len(p.title) > 60: fail(f, f"title {len(p.title)} chars > 60: {p.title}")
    if p.title in seen_titles: fail(f, f"duplicate title (also {seen_titles[p.title]})")
    seen_titles.setdefault(p.title, f)
    if p.desc is None or not p.desc.strip(): fail(f, "missing meta description")
    else:
        if len(p.desc) > 155: fail(f, f"description {len(p.desc)} chars > 155")
        if p.desc in seen_descs: fail(f, f"duplicate description (also {seen_descs[p.desc]})")
        seen_descs.setdefault(p.desc, f)
    # h1
    h1s = [t for l, t in p.h if l == 1]
    if len(h1s) != 1: fail(f, f"{len(h1s)} H1s: {h1s[:3]}")
    # heading order (no skipped levels)
    prev = 0
    for lvl, txt in p.h:
        if prev and lvl > prev + 1:
            fail(f, f"heading skips from h{prev} to h{lvl} ('{txt[:40]}')"); break
        prev = lvl
    # canonical / og / twitter / lang
    if not is_404:
        if p.canonical != SITE + url: fail(f, f"canonical {p.canonical!r} != {SITE + url}")
        for k in ("og:title", "og:description", "og:url", "og:image", "og:type"):
            if not p.og.get(k): fail(f, f"missing {k}")
        if p.og.get("og:url") and p.og["og:url"] != SITE + url: fail(f, f"og:url {p.og['og:url']} != {SITE + url}")
        if p.og.get("og:image") and not p.og["og:image"].startswith("https://"): fail(f, "og:image not absolute")
        if p.og.get("og:image"):
            img = p.og["og:image"].replace(SITE + "/", "")
            if not (ROOT / img).is_file(): fail(f, f"og:image file missing: {img}")
        for k in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
            if not p.tw.get(k): fail(f, f"missing {k}")
    if not p.lang: fail(f, "missing <html lang>")
    # JSON-LD
    types = []
    for blk in p.ld:
        try:
            d = json.loads(blk)
        except Exception as e:
            fail(f, f"invalid JSON-LD: {e}"); continue
        for node in (d.get("@graph", [d]) if isinstance(d, dict) else d):
            types.append(node.get("@type"))
    if not is_404 and url != "/" and "BreadcrumbList" not in types: fail(f, "no BreadcrumbList JSON-LD")
    if not p.ld and not is_404: fail(f, "no JSON-LD at all")
    for blk in p.ld:
        for m in re.finditer(r'https://miamiyachtcollective\.com/[^"\s]*', blk):
            u = m.group(0)
            if u.endswith(".html") or re.search(r"/(index)?\.html", u):
                fail(f, f"JSON-LD still references an old URL: {u}")
    # images
    for src, alt, role in p.imgs:
        if alt is None: fail(f, f"<img> without alt: {src}")
        elif alt.strip() == "" and role != "presentation": fail(f, f"decorative <img> without role=presentation: {src}")
        if src.startswith(("css/", "js/", "images/", "photos/", "videos/")): fail(f, f"relative asset path: {src}")
        if src.startswith("/") and not (ROOT / src.lstrip("/")).is_file() and not src.startswith("/videos/"): fail(f, f"image file missing: {src}")
    # links
    internal = []
    for href, target, in_chrome in p.links:
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        sp = urlsplit(href)
        if sp.scheme or href.startswith("//"):
            if sp.netloc and sp.netloc.endswith("miamiyachtcollective.com"):
                fail(f, f"absolute self link should be relative: {href}")
            continue  # external
        if target == "_blank": fail(f, f"internal link opens a new tab: {href}")
        if not href.startswith("/"): fail(f, f"relative internal link (should be root-absolute): {href}"); continue
        if sp.path.endswith(".html"): fail(f, f"link to .html (non-final URL): {href}")
        elif sp.path != "/" and sp.path.endswith("/"): fail(f, f"link with trailing slash: {href}")
        elif file_for_url(href) is None and not sp.path.startswith("/_vercel"): fail(f, f"broken internal link: {href}")
        internal.append((sp.path, in_chrome))
    # tel
    for t in p.tels:
        if t not in ALLOWED_TEL: fail(f, f"unexpected phone number: {t}")
    for c in COMPETITORS:
        if re.search(r"\b" + c + r"\b", raw, re.I): fail(f, f"competitor name '{c}' present")
    return dict(url=url, noindex=noindex, is_404=is_404, links=internal, title=p.title, hreflang=p.hreflang)


def main():
    pages = served_pages()
    info = {}
    seen_titles, seen_descs = {}, {}
    for f in pages:
        raw = (ROOT / f).read_text(encoding="utf-8")
        info[f] = check_page(f, raw, seen_titles, seen_descs)
    # ---- sitemap
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    sm_urls = [l.replace(SITE, "") or "/" for l in locs]
    by_url = {i["url"]: f for f, i in info.items()}
    for u in sm_urls:
        if u not in by_url: fail("sitemap.xml", f"{u} is not a served page")
        elif info[by_url[u]]["noindex"]: fail("sitemap.xml", f"{u} is noindex")
        elif u.endswith(".html") or (u != "/" and u.endswith("/")): fail("sitemap.xml", f"non-final URL {u}")
    for f, i in info.items():
        if not i["noindex"] and not i["is_404"] and i["url"] not in sm_urls:
            fail("sitemap.xml", f"indexable page missing from sitemap: {i['url']}")
    # hreflang symmetry
    hl = {i["url"]: {code: href.replace(SITE, "") or "/" for code, href in i["hreflang"]} for i in info.values() if i["hreflang"]}
    for u, alts in hl.items():
        for code, target in alts.items():
            if code != "x-default" and target in hl and u not in hl[target].values():
                fail(by_url[u], f"hreflang {code} -> {target} is not reciprocated")
    # ---- crawl + orphans
    graph = {i["url"]: set(path for path, _ in i["links"]) for i in info.values()}
    chrome_links = set()
    for i in info.values():
        chrome_links |= {path for path, in_chrome in i["links"] if in_chrome}
    reach = {"/"}; stack = ["/"]
    while stack:
        u = stack.pop()
        for v in graph.get(u, ()):
            v = v if v in graph else None
            if v and v not in reach:
                reach.add(v); stack.append(v)
    for u in sm_urls:
        if u not in reach: fail("crawl", f"{u} not reachable from /")
        hub_in = [h for h in HUBS if h != u and u in graph.get(h, ())]
        if not hub_in: fail("orphans", f"{u} is not linked from any hub")
        hub_of = "/" + u.strip("/").split("/")[0] if "/" in u.strip("/") else None
        if u not in chrome_links and not (hub_of and hub_of in chrome_links):
            fail("orphans", f"{u} is not linked from the nav/footer (directly or via its hub)")
    # ---- HTTP checks
    if BASE:
        import urllib.request
        def head(u):
            req = urllib.request.Request(BASE + u, method="HEAD")
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, *a, **k): return None
            op = urllib.request.build_opener(NoRedirect)
            try:
                r = op.open(req, timeout=10); return r.status, r.headers.get("Location")
            except urllib.error.HTTPError as e:
                return e.code, e.headers.get("Location")
        for u in sm_urls:
            code, loc = head(u)
            if code != 200: fail("http", f"{u} -> {code} {loc or ''}")
        old = (ROOT / "seo-tools/sitemap-before-ia-2026-10-28.xml").read_text(encoding="utf-8")
        olds = [l.replace(SITE, "") or "/" for l in re.findall(r"<loc>([^<]+)</loc>", old)]
        for u in olds:
            code, loc = head(u)
            if code == 200: continue
            if code != 301: fail("redirects", f"{u} -> {code} (expected 200 or one 301)"); continue
            c2, l2 = head(urlsplit(loc).path)
            if c2 != 200: fail("redirects", f"{u} -> 301 {loc} -> {c2} {l2 or ''} (chain or dead end)")
    # ---- report
    print(f"checked {len(pages)} pages, {len(sm_urls)} sitemap URLs")
    for w in warnings: print("WARN", w)
    if failures:
        print(f"\n{len(failures)} FAILURES")
        for x in failures: print(" -", x)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
