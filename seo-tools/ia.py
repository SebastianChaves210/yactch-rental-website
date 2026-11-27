# -*- coding: utf-8 -*-
"""Information architecture registry for miamiyachtcollective.com (2026-10-28).

Single source of truth for:
  * the URL map (old flat .html file -> final clean URL + file on disk)
  * the fleet (name, length, price, photos, occasions, similar yachts)
  * site-wide facts used by the shared header/footer (phone, address, socials)
  * the per-page WhatsApp prefill text
  * link rewriting helpers (old hrefs -> final URLs, relative assets -> root-absolute)

Everything here is owner-confirmed fact or existing site copy. Nothing is invented;
anything unknown is left out and listed in OWNER-TODO.md.
"""
import json, re
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).parent
REPO = HERE.parent
SITE = "https://miamiyachtcollective.com"

# ---------------------------------------------------------------- business facts
PHONE_DISPLAY = "(787) 664-5040"
TEL = "tel:+17876645040"
WA_NUMBER = "17876645040"
EMAIL = "sebastian@mcaiconsulting.com"   # TODO(owner): a branded @miamiyachtcollective.com address is recommended
ADDRESS_LINE = "668 NW N River Dr"
ADDRESS_CITY = "Miami, FL 33136"
MAPS_URL = "https://maps.app.goo.gl/7bYMugMBFHaZruoW8"
INSTAGRAM = "https://www.instagram.com/miamiyachtcollective/"
LOGO = "/images/main-boat-logo-420.webp"
LOGO_PNG = "/images/main-boat-logo-transparent.png"
YEAR = "2026"

def wa_url(msg):
    return f"https://wa.me/{WA_NUMBER}?text={quote(msg, safe='')}"

# ---------------------------------------------------------------- fleet
# Order: longest first (the order the fleet is listed everywhere on the site).
FLEET = [
    dict(old="deep-blue", slug="90-deep-blue", name="90' Deep Blue with Jacuzzi", short="Deep Blue", length=90, price=4999,
         type="Motor yacht", crew=2, card=("photos/deep-blue-90/deepblue-1-800.webp", 800, 533), feature="Jacuzzi on board",
         blurb="The headline yacht: 90 feet, an onboard Jacuzzi, captain and crew.",
         occasions=["corporate-yacht-charter-miami", "yacht-party-miami", "bachelorette-yacht-party-miami", "new-years-eve-yacht-miami"],
         similar=["aicon", "azimut-lchaim", "anvera"],
         cabins="Master cabin, twin-bed guest cabins and bathrooms below deck",
         amenities=["Jacuzzi on deck", "Teak aft deck with a full-width sofa", "Flybridge", "Main salon with two cream sofas",
                    "Formal dining table", "Galley with a stone-topped island and full-size refrigerator",
                    "Helm with twin captain's chairs", "Master cabin with a double bed", "Twin-bed guest cabins", "Bathrooms below deck"],
         stop="Anchor off Star Island or in the bay and the Jacuzzi becomes the party."),
    dict(old="aicon", slug="75-aicon", name="75' Aicon", short="Aicon", length=75, price=3000,
         type="Motor yacht", crew=2, card=("photos/aicon-75/aicon75-01-800.webp", 800, 441), feature=None,
         blurb="A 75 foot flybridge yacht with a teak salon and two cabins below deck.",
         occasions=["corporate-yacht-charter-miami", "wedding-yacht-charter-miami", "yacht-party-miami", "art-basel-yacht-charter-miami"],
         similar=["deep-blue", "azimut-lchaim", "anvera"],
         cabins="Master cabin with a double bed and a twin cabin below deck",
         amenities=["Flybridge lounge with orange cushions", "Salon with white sofas and a TV", "Helm on the flybridge under a shade top",
                    "Teak floors and wood detailing through the salon", "Dining table beside the helm seats", "Galley with wood cabinets",
                    "Master cabin with a double bed", "Twin cabin with two single beds", "Teak swim platform at the stern"],
         stop="Drop anchor in the bay and step into the water from the teak swim platform at the stern."),
    dict(old="azimut-lchaim", slug="65-azimut-lchaim", name="65' Azimut L'chaim", short="L'chaim", length=65, price=3000,
         type="Motor yacht", crew=1, card=("photos/azimut-lchaim-65/1-800.webp", 800, 450), feature="Three decks",
         blurb="A full-size Italian motor yacht built for celebrations.",
         occasions=["birthday-yacht-party-miami", "yacht-party-miami", "bachelorette-yacht-party-miami", "corporate-yacht-charter-miami"],
         similar=["aicon", "anvera", "azimut"],
         cabins="Master cabin, VIP cabin, twin cabin and bathrooms with showers",
         amenities=["Flybridge with its own helm, a lounge with a table and a sunpad under the bimini", "Aft deck with a teak dining table in the shade",
                    "Wide bow sunpad", "Salon finished in tan leather and cherry wood", "Galley", "Master cabin", "VIP cabin", "Twin cabin",
                    "Bathrooms with showers", "Inflatable slide and water toys (available at an additional cost)"],
         stop="Anchor and swim; the inflatable slide and water toys can be added to the charter."),
    dict(old="anvera", slug="62-anvera", name="62' Anvera", short="Anvera", length=62, price=1700,
         type="Sport yacht", crew=1, card=("photos/anvera-62/anveras-8.jpg1-800.webp", 800, 600), feature="Fold-down terraces",
         blurb="The sport yacht of the fleet: low, sleek and fast.",
         occasions=["private-sunset-cruise-miami", "yacht-photoshoot-miami", "proposal-yacht-charter-miami", "miami-grand-prix-yacht-charter"],
         similar=["azimut-lchaim", "azimut", "isabella"],
         cabins=None,
         amenities=["One long open walkaround deck", "Three wide sun loungers at the stern", "Terraces that fold down to water level",
                    "Dining table and bench seating in the shade of the hardtop", "Speakers built into the seating", "Bow sunpad",
                    "Bright white cabin lounge below deck with a wraparound lounge and a sofa"],
         stop="Fold the terraces down at anchor and the deck opens out over the water."),
    dict(old="azimut", slug="55-azimut", name="55' Azimut", short="55' Azimut", length=55, price=1600,
         type="Motor yacht", crew=1, card=("photos/legacy/azimut-800.webp", 800, 552), feature=None,
         blurb="Italian lines at a mid-size price.",
         occasions=["bachelorette-yacht-party-miami", "birthday-yacht-party-miami", "private-sunset-cruise-miami", "star-island-boat-tour-miami"],
         similar=["anvera", "isabella", "azimut-lchaim"],
         cabins=None,
         amenities=["Flybridge shaded by a hardtop", "Aft deck with steps down to a full-width swim platform", "Clear bow deck forward"],
         stop="Anchor in the bay and use the full-width swim platform to get in."),
    dict(old="isabella", slug="48-isabella", name="48' Isabella with Jet Ski", short="Isabella", length=48, price=1499,
         type="Motor yacht", crew=1, card=("photos/isabella-48/4-800.webp", 800, 480), feature="Jet ski included",
         blurb="The yacht that comes with a jet ski included in the charter.",
         occasions=["birthday-yacht-party-miami", "bachelor-party-yacht-miami", "bachelorette-yacht-party-miami", "sandbar-yacht-charter-miami"],
         similar=["maxum", "azimut", "anvera"],
         cabins="One cabin with a double bed and a bathroom",
         amenities=["Jet ski included in the charter", "Flybridge with wraparound seating and the helm under a bimini", "Aft deck with bench seating at water level",
                    "Bow sunpad", "Salon with two sofas and a TV", "Galley", "Cabin with a double bed", "Bathroom"],
         stop="Drop anchor and take turns on the jet ski while the rest of the group holds the deck."),
    dict(old="maxum", slug="46-maxum", name="46' Maxum", short="Maxum", length=46, price=1500,
         type="Motor yacht", crew=1, card=("photos/legacy/maxum-800.webp", 800, 552), feature=None,
         blurb="An open-deck motor yacht made for a group day on Biscayne Bay.",
         occasions=["birthday-yacht-party-miami", "private-sunset-cruise-miami", "family-yacht-charter-miami", "yacht-party-miami"],
         similar=["isabella", "azimut", "axopar-brabus"],
         cabins=None,
         amenities=["Flybridge with the helm and seating under a bimini", "Long bow deck with a sunpad", "Railed side decks"],
         stop="Anchor at the sandbar and spend the middle of the day in the water."),
    dict(old="axopar-brabus", slug="28-axopar-brabus", name="28' Axopar Brabus Edition", short="Axopar Brabus", length=28, price=1200,
         type="Sport boat", crew=1, card=("photos/axopar-brabus-28/1-800.webp", 800, 599), feature="Brabus edition",
         blurb="A fast, sharp-handling day boat finished by Brabus.",
         occasions=["sandbar-yacht-charter-miami", "proposal-yacht-charter-miami", "yacht-photoshoot-miami", "star-island-boat-tour-miami"],
         similar=["yamaha-255xd", "maxum", "isabella"],
         cabins=None,
         amenities=["Walkaround sport boat: bow to stern along either side", "Helm under a T-top", "Rows of diamond-stitched navy seats",
                    "Open aft deck for sun and water access", "Twin outboards: one of the fastest rides in the fleet"],
         stop="Get to the sandbar before everyone else; the open aft deck is the way in and out of the water."),
    dict(old="yamaha-255xd", slug="25-yamaha-255xd", name="25' Yamaha 255XD", short="Yamaha 255XD", length=25, price=1000,
         type="Jet boat", crew=1, card=("photos/yamaha-255xd-25/61eaa632-1da8-48db-9a3f-736a6d2333a0.jpg", 800, 600), feature="Jet boat",
         blurb="The smallest, quickest boat in the fleet, built for speed, spray and sandbar time.",
         occasions=["sandbar-yacht-charter-miami", "bachelor-party-yacht-miami", "family-yacht-charter-miami", "spring-break-yacht-miami"],
         similar=["axopar-brabus", "maxum", "isabella"],
         cabins=None,
         amenities=["Bow seating", "Helm and cockpit seating", "Jet propulsion: shallow-water agility for spots the big yachts pass by"],
         stop="Jet propulsion means your captain can tuck into shallow sandbar spots the big yachts pass by."),
]
FLEET_BY_OLD = {b["old"]: b for b in FLEET}
FLEET_BY_SLUG = {b["slug"]: b for b in FLEET}

def price_str(b):
    return "${:,}".format(b["price"])

# ---------------------------------------------------------------- page registry
# key = old file name without .html. url = final clean URL. file = path on disk.
# section = hub it belongs to (for breadcrumbs, dropdowns, hub listings).
PAGES = {}

def _add(old, url, section, lang="en", crumb=None, label=None, group=None, new=False):
    file = "index.html" if url == "/" else url.lstrip("/") + ".html"
    PAGES[old] = dict(old=old, url=url, file=file, section=section, lang=lang,
                      crumb=crumb or label, label=label or crumb, group=group, new=new)

_add("index", "/", "home", label="Home")
# hubs
_add("yacht", "/yachts", "yachts", label="Yachts", crumb="Yachts")
PAGES["yacht"]["file"] = "yachts/index.html"
_add("services", "/experiences", "experiences", label="Experiences")
PAGES["services"]["file"] = "experiences/index.html"
_add("destinations", "/destinations", "destinations", label="Destinations", new=True)
PAGES["destinations"]["file"] = "destinations/index.html"
_add("events", "/events", "events", label="Miami Events", new=True)
PAGES["events"]["file"] = "events/index.html"
_add("guides", "/guides", "guides", label="Guides")
PAGES["guides"]["file"] = "guides/index.html"
_add("add-ons", "/add-ons", "root", label="Add-ons", new=True)
_add("faq", "/faq", "root", label="FAQ", new=True)
# yachts
for b in FLEET:
    _add(b["old"], "/yachts/" + b["slug"], "yachts", crumb=b["name"], label=b["name"])
# experiences (occasion pages) — keyword slugs kept, nested under /experiences
EXPERIENCES = [
    ("birthday-yacht-party-miami", "Birthday Parties", "celebrations"),
    ("bachelorette-yacht-party-miami", "Bachelorette Parties", "celebrations"),
    ("bachelor-party-yacht-miami", "Bachelor Parties", "celebrations"),
    ("quinceanera-yacht-party-miami", "Quinceañeras", "celebrations"),
    ("yacht-party-miami", "Private Yacht Parties", "celebrations"),
    ("party-boat-rental-miami", "Party Boat Rentals", "celebrations"),
    ("proposal-yacht-charter-miami", "Proposals & Anniversaries", "romance"),
    ("wedding-yacht-charter-miami", "Weddings on Board", "romance"),
    ("private-sunset-cruise-miami", "Private Sunset Cruises", "romance"),
    ("corporate-yacht-charter-miami", "Corporate Charters", "groups"),
    ("family-yacht-charter-miami", "Family Charters", "groups"),
    ("yacht-photoshoot-miami", "Photo & Video Shoots", "days"),
    ("yacht-charter-before-cruise-miami", "Before or After Your Cruise", "days"),
]
for slug, label, group in EXPERIENCES:
    _add(slug, "/experiences/" + slug, "experiences", label=label, group=group)
# destinations
DESTINATIONS = [
    ("sandbar-yacht-charter-miami", "Sandbar Charters", "Sandbar"),
    ("star-island-boat-tour-miami", "Star Island Boat Tours", "Star Island"),
    ("yacht-rental-miami-beach", "Miami Beach", "Miami Beach"),
    ("south-beach-yacht-rental", "South Beach", "South Beach"),
    ("yacht-rental-brickell", "Brickell & Downtown", "Brickell"),
]
for slug, label, short in DESTINATIONS:
    _add(slug, "/destinations/" + slug, "destinations", label=label, crumb=label)
    PAGES[slug]["short"] = short
# events
EVENTS = [
    ("art-basel-yacht-charter-miami", "Art Basel Week"),
    ("new-years-eve-yacht-miami", "New Year's Eve"),
    ("spring-break-yacht-miami", "Spring Break & Music Week"),
    ("miami-grand-prix-yacht-charter", "Grand Prix Weekend"),
]
for slug, label in EVENTS:
    _add(slug, "/events/" + slug, "events", label=label)
# guides
GUIDES = [
    ("boating-license-miami-boat-rental", "Do You Need a License to Rent a Boat in Miami?"),
    ("what-to-bring-yacht-charter-miami", "What to Bring on a Yacht Charter"),
    ("miami-sandbar-guide", "The Miami Sandbar Guide"),
    ("best-time-yacht-charter-miami", "The Best Time for a Yacht Charter in Miami"),
]
for slug, label in GUIDES:
    _add(slug, "/guides/" + slug, "guides", label=label)
# root pages
_add("miami-yacht-rental-prices", "/prices", "root", label="Prices")
_add("boat-rental-miami", "/boat-rental-miami", "root", label="Boat Rentals")
_add("gallery", "/gallery", "root", label="Gallery")
_add("about", "/about", "root", label="About")
_add("contact", "/contact", "root", label="Contact")
_add("booking", "/book", "root", label="Book")
_add("alquiler-de-yates-miami", "/alquiler-de-yates-miami", "root", lang="es", label="Alquiler de yates en Miami")
_add("fiesta-en-yate-miami", "/fiesta-en-yate-miami", "root", lang="es", label="Fiesta en yate en Miami")
_add("aluguel-de-iate-em-miami", "/aluguel-de-iate-em-miami", "root", lang="pt-BR", label="Aluguel de iate em Miami")
_add("privacy-policy", "/privacy-policy", "legal", label="Privacy Policy", new=True)
_add("terms", "/terms", "legal", label="Terms of Service", new=True)
_add("cancellation-policy", "/cancellation-policy", "legal", label="Cancellation Policy", new=True)
_add("404", "/404", "error", label="Not found")
PAGES["404"]["file"] = "404.html"

# pages that are noindex until the owner approves them (excluded from the sitemap)
NOINDEX = {"privacy-policy", "terms", "cancellation-policy", "add-ons", "404"}

# language equivalents (true translations only)
TRANSLATIONS = {
    "index": {"en": "index", "es": "alquiler-de-yates-miami", "pt-BR": "aluguel-de-iate-em-miami"},
    "yacht-party-miami": {"en": "yacht-party-miami", "es": "fiesta-en-yate-miami"},
}
LANG_HOME = {"en": "index", "es": "alquiler-de-yates-miami", "pt-BR": "aluguel-de-iate-em-miami"}

def url_of(old):
    return PAGES[old]["url"]

def abs_url(old):
    return SITE + PAGES[old]["url"]

def lang_target(old, lang):
    """Where the language switcher points from page `old` for language `lang`."""
    for cluster in TRANSLATIONS.values():
        if old in cluster.values():
            return cluster.get(lang, LANG_HOME[lang])
    return LANG_HOME[lang]

# ---------------------------------------------------------------- WhatsApp prefill per page (existing messages kept)
DEFAULT_WA = "Hi! I'd like to book a private yacht in Miami. My date:"
WA = {
    "index": DEFAULT_WA, "booking": DEFAULT_WA, "contact": DEFAULT_WA, "about": DEFAULT_WA, "gallery": DEFAULT_WA,
    "guides": DEFAULT_WA, "404": DEFAULT_WA, "faq": DEFAULT_WA,
    "add-ons": "Hi! I'd like to add something to a yacht charter in Miami. My date and what I have in mind:",
    "privacy-policy": DEFAULT_WA, "terms": DEFAULT_WA, "cancellation-policy": DEFAULT_WA,
    "yacht": "Hi! I'd like to book one of your yachts. My date:",
    "services": "Hi! I'd like to plan a yacht experience in Miami. My date:",
    "destinations": "Hi! I'd like to plan a yacht day in Miami. My date and where I'd like to go:",
    "events": "Hi! I'd like to book a yacht for an event week in Miami. My date:",
    "yacht-party-miami": "Hi! I'd like to book a private yacht party in Miami. My date and group size:",
    "birthday-yacht-party-miami": "Hi! I'm planning a birthday yacht party in Miami. My date and group size:",
    "bachelorette-yacht-party-miami": "Hi! I'm planning a bachelorette yacht party in Miami. My date and group size:",
    "bachelor-party-yacht-miami": "Hi! I'm planning a bachelor party yacht charter in Miami. My date and group size:",
    "private-sunset-cruise-miami": "Hi! I'd like to book a private sunset cruise in Miami. My date:",
    "miami-yacht-rental-prices": "Hi! I saw your prices page and I'd like a quote. My date:",
    "corporate-yacht-charter-miami": "Hi! I'd like to plan a corporate yacht charter in Miami. Date and group size:",
    "sandbar-yacht-charter-miami": "Hi! I'd like to book a sandbar yacht charter in Miami. My date:",
    "boat-rental-miami": "Hi! I'd like to rent a boat with captain in Miami. My date:",
    "party-boat-rental-miami": "Hi! I'd like to rent a party boat in Miami. My date and group size:",
    "proposal-yacht-charter-miami": "Hi! I'm planning a proposal or anniversary cruise in Miami. My date:",
    "yacht-rental-miami-beach": "Hi! I'm staying in Miami Beach and I'd like to rent a yacht. My date:",
    "yacht-rental-brickell": "Hi! I'm in Brickell/Downtown and I'd like to rent a yacht. My date:",
    "alquiler-de-yates-miami": "¡Hola! Quiero reservar un yate privado en Miami. Mi fecha:",
    "boating-license-miami-boat-rental": DEFAULT_WA, "what-to-bring-yacht-charter-miami": DEFAULT_WA,
    "miami-sandbar-guide": DEFAULT_WA, "best-time-yacht-charter-miami": DEFAULT_WA,
}
for b in FLEET:
    WA[b["old"]] = f"Hi! I'm interested in the {b['name']}. My date:"
WA.update(json.loads((HERE / "wa_new_pages.json").read_text(encoding="utf-8")))

def wa_for(old):
    return wa_url(WA.get(old, DEFAULT_WA))


# ---------------------------------------------------------------- meta descriptions (<=155 chars, applied sitewide 2026-10-28)
DESCRIPTIONS = {
    "index": 'Private yacht rentals in Miami with captain and crew included. 9 yachts from 25 to 90 ft, from $1,000 for 4 hours, departing the Miami River. Book direct.',
    "yacht": 'The full Miami Yacht Collective fleet: 9 private yachts and boats, 25 to 90 ft, from $1,000 for 4 hours with captain and crew. Compare and book direct.',
    "services": 'Private yacht experiences in Miami: parties, birthdays, bachelorettes, sunset cruises, sandbar days and corporate events. Crew included, from $1,000.',
    "about": 'A small, hand-picked yacht charter fleet departing the Miami River. Direct to the captain, no platforms, no booking fees. Call or WhatsApp to book.',
    "contact": 'Call or WhatsApp (787) 664-5040, open 24/7. Private yacht charters departing the Miami River, 10 minutes from Brickell. Most bookings confirmed in minutes.',
    "booking": 'Book a private yacht in Miami direct: pick the yacht, date and group size and we confirm by WhatsApp or phone, usually in under 10 minutes. Crew included.',
    "deep-blue": 'Charter the 90-foot Deep Blue with Jacuzzi in Miami: the superyacht for parties, corporate events and celebrations. From $4,999 for 4 hours, crew included.',
    "aicon": 'Charter the 75 foot Aicon in Miami: a flybridge lounge, a teak salon and cabins below deck, captain and crew included. From $3,000 for 4 hours.',
    "azimut-lchaim": "Charter the 65-foot Azimut L'chaim in Miami for yacht parties, sunset cruises and private celebrations on Biscayne Bay. From $3,000 for 4 hours with crew.",
    "anvera": 'Charter the 62-foot Anvera in Miami: a sleek, high-performance Italian yacht for day charters, sunset cruises and private events. From $1,700 for 4 hours.',
    "azimut": 'Rent the 55-foot Azimut yacht in Miami. Sleek Italian design and powerful performance, captain and crew included. From $1,600 for 4 hours. Book today.',
    "isabella": 'Rent the 48-foot Isabella in Miami with a jet ski included. Built for birthdays, bachelor and bachelorette days and sunset cruises. From $1,499.',
    "maxum": 'Charter the 46-foot Maxum in Miami: an open-deck motor yacht for groups, captain and crew included. From $1,500 for 4 hours. Call or WhatsApp to book.',
    "axopar-brabus": "Charter the 28' Axopar Brabus Edition in Miami. Premium sport boat, captain and crew included, $1,200 for 4 hours. Book with Miami Yacht Collective.",
    "yamaha-255xd": 'Rent the 25-foot Yamaha 255XD jet boat in Miami: fast, agile, captain included, from $1,000 for 4 hours. Skyline runs, sandbar days and watersports.',
    "yacht-party-miami": 'Rent the whole yacht for your party in Miami, no ticketed crowds. Captain and crew included, from $1,000 for 4 hours on Biscayne Bay. Book by WhatsApp.',
    "party-boat-rental-miami": 'Private party boat rentals in Miami: your group, your music, your own boat with captain and crew. No tickets, no strangers. From $1,000 for 4 hours.',
    "birthday-yacht-party-miami": 'Celebrate your birthday on a private yacht in Miami, captain and crew included, from $1,000 for 4 hours. Skyline cruise, Star Island loop, sandbar swim.',
    "bachelorette-yacht-party-miami": 'The bachelorette boat day in Miami: a private yacht with captain and crew from $1,000 for 4 hours. Star Island cruise, sandbar swim and skyline photos.',
    "bachelor-party-yacht-miami": 'Private bachelor party yacht charters in Miami, captain and crew included: a yacht with a jet ski, fast sport boats and a 90-foot superyacht. From $1,000.',
    "quinceanera-yacht-party-miami": 'Celebrate a quinceañera or sweet sixteen on a private yacht in Miami: the whole boat for the family, crew included, a Spanish-speaking team. From $1,000.',
    "proposal-yacht-charter-miami": 'Propose or celebrate an anniversary on a private yacht in Miami: sunset over the skyline, just you two or the whole family, crew included. From $1,000.',
    "wedding-yacht-charter-miami": 'Get married on a private yacht in Miami. Ceremonies on board are welcome, with the skyline as the backdrop and crew included. From $1,000 for 4 hours.',
    "private-sunset-cruise-miami": 'A private sunset cruise past the Miami skyline, just your group. Captain and crew included, from $1,000 for 4 hours. Date nights, proposals, anniversaries.',
    "corporate-yacht-charter-miami": 'Private corporate yacht charters in Miami for client days, team outings and company celebrations. Captain and crew included, from $1,000 for 4 hours.',
    "family-yacht-charter-miami": "Private family yacht charters in Miami: children welcome, children's life jackets on board, calm Biscayne Bay routes and a sandbar swim. From $1,000.",
    "yacht-photoshoot-miami": 'Rent a private yacht in Miami for a photo shoot, video shoot or content day. Commercial shoots welcome; skyline and open-water backdrops. From $1,000.',
    "yacht-charter-before-cruise-miami": 'Sailing from PortMiami? Spend the day before or after your cruise on a private yacht: board near downtown, cruise Star Island and the skyline, from $1,000.',
    "sandbar-yacht-charter-miami": "Private sandbar boat and yacht charters in Miami. Anchor at Nixon's Sandbar, cruise to Stiltsville and swim in Biscayne Bay, crew included. From $1,000.",
    "star-island-boat-tour-miami": 'A private Star Island boat tour in Miami: the celebrity homes of Star, Palm and Hibiscus Islands from your own yacht, crew included. From $1,000.',
    "yacht-rental-miami-beach": 'Staying in Miami Beach? Private yacht charters board 15 minutes away on the Miami River and cruise Star Island, Fisher Island and the skyline. From $1,000.',
    "south-beach-yacht-rental": 'Staying in South Beach? Private yacht rentals board 15 minutes away on the Miami River and cruise Star Island, Fisher Island and the skyline. From $1,000.',
    "yacht-rental-brickell": 'Private yacht charters 10 minutes from Brickell: board on the Miami River and cruise past the skyline into Biscayne Bay, crew included. From $1,000.',
    "art-basel-yacht-charter-miami": 'Private yacht charters during Art Basel Miami Beach, December 4 to 6, 2026, at the same prices as any other week. Captain and crew included, from $1,000.',
    "new-years-eve-yacht-miami": 'Ring in the new year on a private yacht in Miami: your group only, captain and crew included, the same price as any night, from $1,000 for 4 hours.',
    "spring-break-yacht-miami": 'Private spring break yacht parties in Miami, including Miami Music Week and Ultra weekend, March 22 to 28, 2027. Your own boat with crew, from $1,000.',
    "miami-grand-prix-yacht-charter": 'Private yacht charters for Miami Grand Prix weekend in early May: your own yacht with captain and crew on Biscayne Bay, at regular prices from $1,000.',
    "miami-yacht-rental-prices": 'Real 2026 Miami yacht rental prices: 9 private yachts from $1,000 to $4,999 for 4 hours, captain and crew always included. Compare every boat, get a quote.',
    "boat-rental-miami": 'Rent a boat in Miami with a licensed captain and crew included: jet boats, sport boats and yachts from 25 to 90 feet, from $1,000 for 4 hours.',
    "boating-license-miami-boat-rental": 'Florida has no boating license, but anyone born in 1988 or later needs a Boating Safety Education ID Card to drive. With a captain, guests need nothing.',
    "what-to-bring-yacht-charter-miami": 'The packing list for a Miami yacht charter: what to wear, which sunscreen to use, what shoes work on deck and what to leave at the dock.',
    "miami-sandbar-guide": "Where Miami's sandbars are and how to reach them by boat: Nixon's Sandbar off Key Biscayne, Haulover in the north bay and the stilt houses of Stiltsville.",
    "best-time-yacht-charter-miami": 'When to book a yacht in Miami: dry season versus summer, weekdays versus weekends, how to time a sunset cruise. Month-by-month weather and sell-out dates.',
    "alquiler-de-yates-miami": 'Alquiler de yates privados en Miami con capitán y tripulación incluidos. 9 yates y lanchas de 25 a 90 pies, desde $1,000 por 4 horas. Reserve por WhatsApp.',
    "fiesta-en-yate-miami": 'Fiesta en yate privado en Miami: cumpleaños, despedidas, quinceañeras y celebraciones. El yate completo para su grupo, capitán incluido, desde $1,000.',
    "aluguel-de-iate-em-miami": 'Aluguel de iate e lancha em Miami com capitão e tripulação inclusos. 9 embarcações de 25 a 90 pés, passeios privativos de 4 horas, a partir de $1,000.',
}
for _k, _v in DESCRIPTIONS.items():
    assert len(_v) <= 155, (_k, len(_v))

# ---------------------------------------------------------------- link rewriting
OG_RENAMES = {  # old photos/og/<name>.jpg -> new name (keeps every card next to its page basename)
    "yacht": "yachts", "services": "experiences", "miami-yacht-rental-prices": "prices", "booking": "book",
}
for b in FLEET:
    OG_RENAMES[b["old"]] = b["slug"]

def og_card(old):
    return f"{SITE}/photos/og/{OG_RENAMES.get(old, old)}.jpg"

_HREF_RE = re.compile(r'(href|action)="([^"#?]*?)\.html(#[^"]*)?"')
_ABS_RE = re.compile(r'https://miamiyachtcollective\.com/([a-z0-9-]+)\.html(#[a-zA-Z0-9-]*)?')
_ASSET_RE = re.compile(r'(["\'(,])(css|js|images|photos|videos)/')
_ROOT_FILES = ("favicon.ico", "favicon-32x32.png", "favicon-16x16.png", "apple-touch-icon.png", "site.webmanifest", "icon-192.png", "icon-512.png")

def _map_old(name, frag):
    if name == "index":
        return "/"
    if name == "services" and frag == "#events":
        return "/events"
    if name in PAGES:
        return PAGES[name]["url"] + (frag or "")
    return None

def rewrite_links(s):
    """Old relative hrefs, old absolute URLs, relative asset paths and tel: links -> final form."""
    def href(m):
        attr, name, frag = m.group(1), m.group(2), m.group(3) or ""
        if "/" in name or name.startswith("http"):
            return m.group(0)
        new = _map_old(name, frag)
        if new is None:
            return m.group(0)
        if name == "services" and frag == "#events":
            return f'{attr}="{new}"'
        return f'{attr}="{new}"'
    s = _HREF_RE.sub(href, s)
    s = re.sub(r'href="index\.html"', 'href="/"', s)
    def absu(m):
        new = _map_old(m.group(1), m.group(2) or "")
        return (SITE + new) if new else m.group(0)
    s = _ABS_RE.sub(absu, s)
    s = s.replace("https://miamiyachtcollective.com/index.html", SITE + "/")
    s = _ASSET_RE.sub(lambda m: m.group(1) + "/" + m.group(2) + "/", s)
    for f in _ROOT_FILES:
        s = s.replace(f'href="{f}"', f'href="/{f}"')
    s = s.replace("tel:7876645040", "tel:+17876645040")
    # share cards that moved with their page
    for old, new in OG_RENAMES.items():
        s = s.replace(f"/photos/og/{old}.jpg", f"/photos/og/{new}.jpg")
    return s

def section_crumb(old):
    """Breadcrumb trail (list of (label, url)) for a page, hub included."""
    p = PAGES[old]
    trail = [("Home", "/")]
    hub = {"yachts": "yacht", "experiences": "services", "destinations": "destinations", "events": "events", "guides": "guides"}.get(p["section"])
    if hub and hub != old:
        trail.append((PAGES[hub]["label"], PAGES[hub]["url"]))
    if old != "index":
        trail.append((p["crumb"], p["url"]))
    return trail

# ---------------------------------------------------------------- hub children
def children(section):
    return [k for k, p in PAGES.items() if p["section"] == section and p["file"] != f"{section}/index.html"]

if __name__ == "__main__":
    for k, p in PAGES.items():
        print(f"{k:38} -> {p['url']:45} {p['file']}")
