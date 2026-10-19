"""Builds the favicon / home-screen icon set from the header yacht mark.

Gold mark on midnight navy, so the tab icon matches the header logo and stays
visible on light and dark browser tabs.
Run from the site root: python3 seo-tools/make_icons.py
"""
from PIL import Image, ImageChops, ImageDraw

NAVY = (12, 31, 53)
GOLD = (194, 161, 95)
GOLD_LIGHT = (222, 199, 146)

src = Image.open("images/main-boat-logo-transparent.png").convert("RGBA")
src = src.crop(src.getbbox())
# Keep the logo's own shading: mask = alpha x luminance.
lum = src.convert("L")
mask = ImageChops.multiply(src.split()[3], lum.point(lambda v: min(255, int(v * 1.15))))


def gold_mark(width):
    h = round(src.height * width / src.width)
    m = mask.resize((width, h), Image.LANCZOS)
    # Vertical champagne gradient, lighter on top.
    grad = Image.new("RGB", (width, h))
    d = ImageDraw.Draw(grad)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (width, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(GOLD_LIGHT, GOLD)))
    out = Image.new("RGBA", (width, h), (0, 0, 0, 0))
    out.paste(grad, (0, 0), m)
    return out


def tile(size, mark_ratio, radius_ratio=0.0, pad_y=0.0):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg = Image.new("RGBA", (size, size), NAVY + (255,))
    if radius_ratio:
        r = Image.new("L", (size * 4, size * 4), 0)
        ImageDraw.Draw(r).rounded_rectangle([0, 0, size * 4 - 1, size * 4 - 1], radius=round(size * 4 * radius_ratio), fill=255)
        im.paste(bg, (0, 0), r.resize((size, size), Image.LANCZOS))
    else:
        im = bg
    mk = gold_mark(round(size * mark_ratio))
    im.alpha_composite(mk, ((size - mk.width) // 2, (size - mk.height) // 2 + round(size * pad_y)))
    return im


# Browser tabs: rounded navy tile, mark nearly edge to edge so it reads at 16px.
for s in (16, 32, 48):
    tile(s * 8, 0.92, 0.22).resize((s, s), Image.LANCZOS).save(f"/tmp/fav-{s}.png")
tile(256, 0.92, 0.22).resize((32, 32), Image.LANCZOS).save("favicon-32x32.png")
tile(128, 0.92, 0.22).resize((16, 16), Image.LANCZOS).save("favicon-16x16.png")
ico = tile(384, 0.92, 0.22)
ico.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
# Old Webflow paths still requested by caches / old shares: same art.
tile(256, 0.92, 0.22).resize((32, 32), Image.LANCZOS).save("images/favicon.png")

# iOS home screen: full-bleed square (iOS rounds it), mark ~68% wide.
tile(180, 0.68).convert("RGB").save("apple-touch-icon.png", optimize=True)
tile(256, 0.68).convert("RGB").save("images/webclip.png", optimize=True)
# Android / manifest.
tile(192, 0.68).convert("RGB").save("icon-192.png", optimize=True)
tile(512, 0.68).convert("RGB").save("icon-512.png", optimize=True)
print("icons written")
