"""Sitewide <head> polish: one icon set, web manifest, theme-color and the
branded link-preview cards from make_og.py (og:image + size + alt, og:locale).

Idempotent. Run from the site root: python3 seo-tools/head_polish.py
"""
import html
import re
import subprocess
import sys

sys.path.insert(0, "seo-tools")
from make_og import PAGES  # noqa: E402

SITE = "https://miamiyachtcollective.com"
SKIP = ("utility/", "detail_", "logo-preview.html")
OG_FALLBACK = {"401": "404", "search": "404"}
LOCALE = {"es": "es_US", "pt-BR": "pt_BR"}

ICON_RE = re.compile(r'[ \t]*<link\b[^>]*\brel="(?:shortcut icon|icon|apple-touch-icon|manifest)"[^>]*>\n?', re.I)
THEME_RE = re.compile(r'[ \t]*<meta\b[^>]*\bname="theme-color"[^>]*>\n?', re.I)
OGIMG_EXTRA_RE = re.compile(r'[ \t]*<meta\b[^>]*\b(?:property|name)="(?:og:image:(?:width|height|alt|type)|twitter:image:alt)"[^>]*>\n?', re.I)


def icon_block(prefix, indent):
    lines = [
        f'<link rel="icon" href="{prefix}favicon.ico" sizes="48x48">',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32x32.png">',
        f'<link rel="icon" type="image/png" sizes="16x16" href="{prefix}favicon-16x16.png">',
        f'<link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">',
        f'<link rel="manifest" href="{prefix}site.webmanifest">',
        '<meta name="theme-color" content="#081524">',
    ]
    return "".join(indent + l + "\n" for l in lines)


def set_meta(s, key, value):
    """Replace the content of an og:/twitter: meta tag, either attribute order."""
    pat = re.compile(r'(<meta\b[^>]*\b(?:property|name)="' + re.escape(key) + r'"[^>]*>)', re.I)
    m = pat.search(s)
    if not m:
        return s, False
    tag = re.sub(r'content="[^"]*"', f'content="{value}"', m.group(1))
    return s[: m.start()] + tag + s[m.end():], True


def process(f):
    s = open(f, encoding="utf-8").read()
    head_end = s.index("</head>")
    head, rest = s[:head_end], s[head_end:]
    prefix = "../" if "/" in f else ""
    m = ICON_RE.search(head)
    indent = re.match(r"[ \t]*", head[m.start():]).group(0) if m else "  "
    pos = m.start() if m else head.rfind("\n", 0, len(head)) + 1
    head = head[:pos] + "\x00" + head[pos:]
    head = ICON_RE.sub("", head)
    head = THEME_RE.sub("", head)
    head = head.replace("\x00", icon_block(prefix, indent))

    slug = f[:-5]
    if not f.startswith("pay/"):
        card = OG_FALLBACK.get(slug, slug)
        if card in PAGES:
            url = f"{SITE}/photos/og/{card}.jpg"
            head, ok1 = set_meta(head, "og:image", url)
            head, ok2 = set_meta(head, "twitter:image", url)
            if not ok1:
                print("  no og:image tag in", f)
            head = OGIMG_EXTRA_RE.sub("", head)
            _, kicker, title, _ = PAGES[card]
            alt = html.escape(f"{title.replace(chr(0xa0), ' ')} — Miami Yacht Collective", quote=True)
            extra = (f'{indent}<meta property="og:image:width" content="1200">\n'
                     f'{indent}<meta property="og:image:height" content="630">\n'
                     f'{indent}<meta property="og:image:alt" content="{alt}">\n'
                     f'{indent}<meta name="twitter:image:alt" content="{alt}">\n')
            og = re.search(r'[^\n]*<meta\b[^>]*\bproperty="og:image"[^>]*>\n', head)
            head = head[: og.end()] + extra + head[og.end():]
        else:
            print("  no card for", f)
        # og:locale
        if 'property="og:locale"' not in head:
            lang = re.search(r'<html[^>]*\blang="([^"]+)"', s).group(1)
            loc = LOCALE.get(lang, "en_US")
            og = re.search(r'[^\n]*<meta\b[^>]*\bproperty="og:site_name"[^>]*>\n', head) or re.search(r'[^\n]*<meta\b[^>]*\bproperty="og:title"[^>]*>\n', head)
            if og:
                head = head[: og.end()] + f'{indent}<meta property="og:locale" content="{loc}">\n' + head[og.end():]
    out = head + rest
    if out != s:
        open(f, "w", encoding="utf-8").write(out)
        return True
    return False


files = [f for f in subprocess.check_output(["git", "ls-files", "*.html"]).decode().split() if not f.startswith(SKIP)]
changed = [f for f in files if process(f)]
print(f"{len(changed)} of {len(files)} pages updated")
