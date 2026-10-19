"""Builds the 1200x630 link-preview cards (iMessage, WhatsApp, social) for every page.

Photo on the right, midnight-navy fade on the left with a gold kicker, the
headline in Cormorant Garamond, a facts line and the wordmark.
Output: photos/og/<page>.jpg. Run from the site root: python3 seo-tools/make_og.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1200, 630
NAVY = (8, 21, 36)
GOLD = (194, 161, 95)
IVORY = (245, 242, 234)
FONTS = os.path.join(os.path.dirname(__file__), "fonts")


def font(name, size, weight):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    f.set_variation_by_name(weight)
    return f


SERIF = lambda s: font("CormorantGaramond.ttf", s, "SemiBold")
SANS = lambda s, w="Medium": font("InterTight.ttf", s, w)

A = "photos/azimut-lchaim-65/"
PHOTOS = {
    "hero": ("videos/Yacht-poster-00001.jpg", 0.5),
    "lchaim-run": (A + "1.jpg", 0.6),
    "lchaim-fisher": (A + "4.jpg", 0.6),
    "lchaim-party": (A + "62_Azimut_Priceless_WEB-57.jpg", 0.55),
    "lchaim-drinks": (A + "32.jpg", 0.6),
    "lchaim-bow": (A + "60_AZI_WEB-13.jpg", 0.5),
    "lchaim-guests": (A + "2.jpg", 0.6),
    "deepblue-salon": ("photos/deep-blue-90/deepblue-12.jpg", 0.5),
    "deepblue-deck": ("photos/deep-blue-90/deepblue-1.jpg", 0.5),
    "ferretti": ("photos/ferretti-75/img-20250613-wa0058.jpg", 0.55),
    "ferretti-palms": ("photos/ferretti-75/img-20250613-wa0066.jpg", 0.6),
    "isabella": ("photos/isabella-48/7.jpeg", 0.6),
    "isabella-air": ("photos/isabella-48/4.jpeg", 0.6),
    "anvera": ("photos/anvera-62/anveras-1.jpg", 0.55),
    "anvera-city": ("photos/anvera-62/anveras-41.jpg", 0.55),
    "anvera-lounge": ("photos/anvera-62/anveras-12.jpg", 0.6),
    "azimut": ("photos/legacy/azimut.avif", 0.6),
    "maxum": ("photos/legacy/maxum.avif", 0.6),
    "axopar": ("photos/axopar-brabus-28/1.jpg", 0.6),
    "yamaha": ("photos/yamaha-255xd-25/easyfowey-13.jpg", 0.6),
    "yamaha-tower": ("photos/yamaha-255xd-25/easyfowey-3.jpg", 0.6),
}

# page -> (photo, kicker, headline, facts)
STD = "Captain & crew included  ·  Miami River dock"
PAGES = {
    "index": ("hero", "Private yacht rental · Miami", "Miami nights start on a yacht", "9 yachts, 25–90 ft  ·  From $1,000 / 4 hours"),
    "yacht": ("lchaim-run", "The fleet", "Nine private yachts, 25 to 90 feet", "From $1,000 / 4 hours  ·  Captain & crew included"),
    "about": ("lchaim-fisher", "About us", "A small, hand-picked Miami fleet", STD),
    "contact": ("hero", "Book direct", "Let’s plan your voyage", "Call or WhatsApp (787) 664-5040  ·  24/7"),
    "booking": ("lchaim-run", "Book direct", "Book your Miami yacht in minutes", "Call or WhatsApp (787) 664-5040  ·  24/7"),
    "services": ("lchaim-party", "Experiences", "Every Miami celebration, on the water", "From $1,000 / 4 hours  ·  " + STD),
    "gallery": ("lchaim-guests", "Gallery", "Life on board, Miami style", "9 yachts  ·  From $1,000 / 4 hours"),
    "guides": ("lchaim-bow", "Guides", "Miami yacht charter guides", "Planning tips from the Miami River dock"),
    "404": ("hero", "Miami Yacht Collective", "Private yacht rentals in Miami", "From $1,000 / 4 hours  ·  " + STD),
    # boats
    "deep-blue": ("deepblue-salon", "90 ft · With jacuzzi", "90' Deep Blue", "From $4,999 / 4 hours  ·  " + STD),
    "ferretti": ("ferretti", "75 ft · Luxury yacht", "75' Ferretti", "From $3,000 / 4 hours  ·  " + STD),
    "azimut-lchaim": ("lchaim-run", "65 ft · Luxury yacht", "65' Azimut L’chaim", "From $3,000 / 4 hours  ·  " + STD),
    "anvera": ("anvera", "62 ft · Luxury yacht", "62' Anvera", "From $1,700 / 4 hours  ·  " + STD),
    "azimut": ("azimut", "55 ft · Motor yacht", "55' Azimut", "From $1,600 / 4 hours  ·  " + STD),
    "isabella": ("isabella", "48 ft · Jet ski included", "48' Isabella with Jet\u00a0Ski", "From $1,499 / 4 hours  ·  " + STD),
    "maxum": ("maxum", "46 ft · Motor yacht", "46' Maxum", "From $1,000 / 4 hours  ·  " + STD),
    "axopar-brabus": ("axopar", "28 ft · Brabus Edition", "28' Axopar Brabus", "From $1,200 / 4 hours  ·  " + STD),
    "yamaha-255xd": ("yamaha", "25 ft · Jet boat", "25' Yamaha 255XD", "From $1,000 / 4 hours  ·  " + STD),
    # occasions
    "yacht-party-miami": ("lchaim-party", "Yacht parties", "Your own yacht. Your own party.", "From $1,000 / 4 hours  ·  " + STD),
    "party-boat-rental-miami": ("lchaim-party", "Party boat rental", "Party boats in Miami", "From $1,000 / 4 hours  ·  " + STD),
    "birthday-yacht-party-miami": ("lchaim-drinks", "Birthdays", "Birthday yacht party in Miami", "From $1,000 / 4 hours  ·  " + STD),
    "bachelorette-yacht-party-miami": ("lchaim-guests", "Bachelorettes", "Bachelorette yacht party in Miami", "From $1,000 / 4 hours  ·  " + STD),
    "bachelor-party-yacht-miami": ("isabella-air", "Bachelor parties", "Bachelor party yacht in Miami", "From $1,000 / 4 hours  ·  " + STD),
    "private-sunset-cruise-miami": ("hero", "Sunset cruises", "Private sunset cruise in Miami", "From $1,000 / 4 hours  ·  " + STD),
    "corporate-yacht-charter-miami": ("deepblue-salon", "Corporate charters", "Corporate yacht charter in Miami", "Up to 90 ft  ·  " + STD),
    "sandbar-yacht-charter-miami": ("yamaha-tower", "Sandbar charters", "Miami sandbar yacht charter", "From $1,000 / 4 hours  ·  " + STD),
    "proposal-yacht-charter-miami": ("ferretti-palms", "Proposals & anniversaries", "Say it on the water", "From $1,000 / 4 hours  ·  " + STD),
    "wedding-yacht-charter-miami": ("ferretti", "Weddings", "Wedding yacht charter in Miami", "Up to 90 ft  ·  " + STD),
    "family-yacht-charter-miami": ("isabella", "Families", "Family yacht charter in Miami", "From $1,000 / 4 hours  ·  " + STD),
    "quinceanera-yacht-party-miami": ("lchaim-guests", "Quinceañeras", "Quinceañera yacht party in Miami", "From $1,000 / 4 hours  ·  " + STD),
    "spring-break-yacht-miami": ("isabella-air", "Spring break", "Spring break on a private yacht", "From $1,000 / 4 hours  ·  " + STD),
    "new-years-eve-yacht-miami": ("hero", "New Year’s Eve", "Ring in the new year on the bay", "Private yachts  ·  " + STD),
    "art-basel-yacht-charter-miami": ("deepblue-deck", "Art Basel week", "Art Basel yacht charter", "Private yachts  ·  " + STD),
    "miami-grand-prix-yacht-charter": ("anvera", "Grand Prix weekend", "Miami Grand Prix yacht charter", "Private yachts  ·  " + STD),
    "yacht-charter-before-cruise-miami": ("anvera-city", "Before or after your cruise", "A private yacht day in Miami", "From $1,000 / 4 hours  ·  " + STD),
    "yacht-photoshoot-miami": ("lchaim-bow", "Photo & video shoots", "Yacht photoshoot rental in Miami", "From $1,000 / 4 hours  ·  " + STD),
    "star-island-boat-tour-miami": ("lchaim-fisher", "Star Island", "Private Star Island boat tour", "From $1,000 / 4 hours  ·  " + STD),
    # locations / search
    "boat-rental-miami": ("axopar", "Boat rental", "Boat rental in Miami with captain", "From $1,000 / 4 hours  ·  " + STD),
    "south-beach-yacht-rental": ("isabella-air", "South Beach", "Yacht rental for South Beach", "From $1,000 / 4 hours  ·  " + STD),
    "yacht-rental-miami-beach": ("lchaim-fisher", "Miami Beach", "Yacht rental for Miami Beach", "From $1,000 / 4 hours  ·  " + STD),
    "yacht-rental-brickell": ("anvera-city", "Brickell & Downtown", "Yacht rental near Brickell", "From $1,000 / 4 hours  ·  " + STD),
    "miami-yacht-rental-prices": ("deepblue-deck", "2026 prices", "What a Miami yacht rental costs", "$1,000 to $4,999 / 4 hours  ·  Captain & crew included"),
    # languages
    "alquiler-de-yates-miami": ("lchaim-run", "Alquiler de yates · Miami", "Alquiler de yates en Miami", "Desde $1,000 / 4 horas  ·  Capitán y tripulación incluidos"),
    "fiesta-en-yate-miami": ("lchaim-drinks", "Fiestas en yate", "Fiesta en yate en Miami", "Desde $1,000 / 4 horas  ·  Capitán y tripulación incluidos"),
    "aluguel-de-iate-em-miami": ("lchaim-fisher", "Aluguel de iate · Miami", "Aluguel de iate em Miami", "A partir de $1,000 / 4 horas  ·  Capitão e tripulação incluídos"),
    # guides
    "boating-license-miami-boat-rental": ("axopar", "Guide", "Do you need a license to rent a boat?", "Short answer: not with a captain"),
    "what-to-bring-yacht-charter-miami": ("isabella", "Guide", "What to bring on a Miami yacht charter", "Miami Yacht Collective guides"),
    "miami-sandbar-guide": ("yamaha-tower", "Guide", "The Miami sandbar guide", "Nixon’s, Haulover and Stiltsville"),
    "best-time-yacht-charter-miami": ("lchaim-bow", "Guide", "The best time for a Miami yacht charter", "Miami Yacht Collective guides"),
}


PW = 700  # photo width on the right; the navy panel fills the rest


def cover(path, focus_x):
    im = Image.open(path).convert("RGB")
    s = max(PW / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - PW) * focus_x)
    y = (im.height - H) // 2
    return im.crop((x, y, x + PW, y + H))


def compose(photo):
    # Navy panel on the left, photo on the right, blended over a 220px soft edge.
    im = Image.new("RGB", (W, H), NAVY)
    m = Image.new("L", (PW, H), 255)
    px = m.load()
    for x in range(220):
        t = x / 220
        v = round(255 * t * t * (3 - 2 * t))
        for y in range(H):
            px[x, y] = v
    im.paste(photo, (W - PW, 0), m)
    return im


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


MARK = None


def mark(height):
    global MARK
    if MARK is None:
        src = Image.open("images/main-boat-logo-transparent.png").convert("RGBA")
        MARK = src.crop(src.getbbox())
    m = MARK.resize((round(MARK.width * height / MARK.height), height), Image.LANCZOS)
    gold = Image.new("RGBA", m.size, GOLD + (0,))
    gold.putalpha(m.split()[3])
    return gold


def card(slug, photo, kicker, title, facts):
    title = title.replace("'", "\u2019")
    path, fx = PHOTOS[photo]
    im = compose(cover(path, fx))
    d = ImageDraw.Draw(im)
    L, max_w = 72, 470
    # Headline: largest size that fits in 3 lines.
    for size in (72, 66, 60, 54, 50):
        hf = SERIF(size)
        lines = wrap(d, title, hf, max_w)
        if len(lines) <= 3:
            break
    lh = round(size * 1.08)
    ff = SANS(21, "Regular")
    flines = wrap(d, facts.replace("  ·  ", "\u00a0· "), ff, max_w)
    block = 30 + 26 + len(lines) * lh + 22 + len(flines) * 30
    y = (H - block) // 2 - 18
    kf = SANS(19, "SemiBold")
    d.line([(L, y + 10), (L + 44, y + 10)], fill=GOLD, width=2)
    d.text((L + 60, y), kicker.upper(), font=kf, fill=GOLD, spacing=0)
    y += 30 + 26
    for ln in lines:
        d.text((L - 2, y), ln, font=hf, fill=IVORY)
        y += lh
    y += 22
    for ln in flines:
        d.text((L, y), ln.replace("\u00a0", " "), font=ff, fill=(214, 220, 228))
        y += 30
    # Wordmark, bottom left.
    mk = mark(30)
    im.paste(mk, (L, H - 72), mk)
    d.text((L + mk.width + 16, H - 66), "MIAMI YACHT COLLECTIVE", font=SANS(17, "SemiBold"), fill=IVORY)
    os.makedirs("photos/og", exist_ok=True)
    out = f"photos/og/{slug}.jpg"
    im.save(out, quality=84, optimize=True, progressive=True)
    return out


if __name__ == "__main__":
    import sys
    only = set(sys.argv[1:])
    for slug, spec in PAGES.items():
        if only and slug not in only:
            continue
        out = card(slug, *spec)
        print(f"{os.path.getsize(out)//1024:4d} KB  {out}")
