#!/usr/bin/env python3
"""Local dev server that behaves like Vercel for this static site.

Honours vercel.json: redirects (statusCode / permanent), cleanUrls, trailingSlash,
directory index files and the custom 404 page. Run from the repo root:

    python3 seo-tools/devserver.py            # http://localhost:8000
    python3 seo-tools/devserver.py 3000

Vercel's own order is: redirects -> cleanUrls/trailingSlash normalisation -> filesystem -> 404.
"""
import json, mimetypes, os, re, sys, urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
CLEAN = CFG.get("cleanUrls", False)
TRAILING = CFG.get("trailingSlash", None)
mimetypes.add_type("image/avif", ".avif")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("application/manifest+json", ".webmanifest")


def compile_source(src):
    """Translate Vercel's path-to-regexp subset into a Python regex."""
    out = "^"
    i = 0
    while i < len(src):
        c = src[i]
        if c == ":":
            m = re.match(r":([A-Za-z0-9_]+)(\([^)]*\))?([*+?])?", src[i:])
            name, inner, mod = m.group(1), m.group(2), m.group(3)
            pat = inner[1:-1] if inner else "[^/]+"
            if mod == "*":
                out += f"(?P<{name}>(?:{pat})(?:/(?:{pat}))*)?" if inner else f"(?P<{name}>.*)"
                # ':path*' also matches the empty remainder (with or without the slash before it)
                out = out.replace(f"/(?P<{name}>.*)", f"(?:/(?P<{name}>.*))?") if not inner else out
            elif mod == "+":
                out += f"(?P<{name}>.+)"
            elif mod == "?":
                out += f"(?P<{name}>{pat})?"
            else:
                out += f"(?P<{name}>{pat})"
            i += m.end()
            continue
        if c in ".":
            out += re.escape(c)
        elif c == "(" and src.startswith("(.*)", i):
            out += "(.*)"; i += 4; continue
        else:
            out += c
        i += 1
    return re.compile(out + "$")


REDIRECTS = []
for r in CFG.get("redirects", []):
    code = r.get("statusCode") or (308 if r.get("permanent", True) else 307)
    REDIRECTS.append((compile_source(r["source"]), r["destination"], code))


def apply_redirects(path):
    for rx, dest, code in REDIRECTS:
        m = rx.match(path)
        if m:
            d = dest
            for k, v in m.groupdict().items():
                d = d.replace(f":{k}*", v or "").replace(f":{k}", v or "")
            return d, code
    return None, None


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.command, fmt % args))

    def redirect(self, location, code):
        self.send_response(code)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_HEAD(self):
        self.do_GET(head=True)

    def do_GET(self, head=False):
        parsed = urllib.parse.urlsplit(self.path)
        path = urllib.parse.unquote(parsed.path)
        qs = ("?" + parsed.query) if parsed.query else ""
        # 1. vercel.json redirects
        dest, code = apply_redirects(path)
        if dest:
            return self.redirect(dest + qs, code)
        # 2. cleanUrls: /foo.html -> /foo  (index.html -> /)
        if CLEAN and path.endswith(".html"):
            new = path[:-5]
            if new.endswith("/index"):
                new = new[:-5] or "/"
            return self.redirect((new or "/") + qs, 308)
        # 3. trailingSlash: false -> strip
        if TRAILING is False and path != "/" and path.endswith("/"):
            return self.redirect(path.rstrip("/") + qs, 308)
        # 4. filesystem
        fs = ROOT / path.lstrip("/")
        candidates = []
        if path == "/" or fs.is_dir():
            candidates.append(fs / "index.html")
        elif fs.is_file():
            candidates.append(fs)
        if CLEAN and not fs.suffix:
            candidates.append(ROOT / (path.lstrip("/") + ".html"))
        for c in candidates:
            if c.is_file():
                return self.send_file(c, 200, head)
        # 5. 404
        return self.send_file(ROOT / "404.html", 404, head)

    def send_file(self, file, status, head=False):
        data = file.read_bytes()
        ctype = mimetypes.guess_type(str(file))[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/json", "application/manifest+json"):
            ctype += "; charset=utf-8"
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head:
            self.wfile.write(data)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Serving {ROOT} on http://localhost:{port}  (cleanUrls={CLEAN}, trailingSlash={TRAILING}, {len(REDIRECTS)} redirects)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
