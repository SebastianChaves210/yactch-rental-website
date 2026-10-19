# -*- coding: utf-8 -*-
"""Content spec for the Oct 2026 tourist landing pages. Facts: owner-confirmed only."""

SITE = "https://miamiyachtcollective.com/"

BOATS = {
    "deep-blue":     ("90' Deep Blue with Jacuzzi", "$4,999 / 4 hours"),
    "ferretti":      ("75' Ferretti", "$3,000 / 4 hours"),
    "azimut-lchaim": ("65' Azimut L'chaim", "$3,000 / 4 hours"),
    "anvera":        ("62' Anvera", "$1,700 / 4 hours"),
    "azimut":        ("55' Azimut", "$1,600 / 4 hours"),
    "isabella":      ("48' Isabella with Jet Ski", "$1,499 / 4 hours"),
    "maxum":         ("46' Maxum", "$1,000 / 4 hours"),
    "axopar-brabus": ("28' Axopar Brabus", "$1,200 / 4 hours"),
    "yamaha-255xd":  ("25' Yamaha 255XD", "$1,000 / 4 hours"),
}
BOATS_ES = {
    "deep-blue":     ("Deep Blue de 90' con jacuzzi", "$4,999 / 4 horas"),
    "ferretti":      ("Ferretti de 75'", "$3,000 / 4 horas"),
    "azimut-lchaim": ("Azimut L'chaim de 65'", "$3,000 / 4 horas"),
    "anvera":        ("Anvera de 62'", "$1,700 / 4 horas"),
    "azimut":        ("Azimut de 55'", "$1,600 / 4 horas"),
    "isabella":      ("Isabella de 48' con jet ski", "$1,499 / 4 horas"),
    "maxum":         ("Maxum de 46'", "$1,000 / 4 horas"),
    "axopar-brabus": ("Axopar Brabus de 28'", "$1,200 / 4 horas"),
    "yamaha-255xd":  ("Yamaha 255XD de 25'", "$1,000 / 4 horas"),
}
BOATS_PT = {
    "deep-blue":     ("Deep Blue de 90 pés com jacuzzi", "$4,999 / 4 horas"),
    "ferretti":      ("Ferretti de 75 pés", "$3,000 / 4 horas"),
    "azimut-lchaim": ("Azimut L'chaim de 65 pés", "$3,000 / 4 horas"),
    "anvera":        ("Anvera de 62 pés", "$1,700 / 4 horas"),
    "azimut":        ("Azimut de 55 pés", "$1,600 / 4 horas"),
    "isabella":      ("Isabella de 48 pés com jet ski", "$1,499 / 4 horas"),
    "maxum":         ("Maxum de 46 pés", "$1,000 / 4 horas"),
    "axopar-brabus": ("Axopar Brabus de 28 pés", "$1,200 / 4 horas"),
    "yamaha-255xd":  ("Yamaha 255XD de 25 pés", "$1,000 / 4 horas"),
}

# ---- photo catalog (existing -800 webp copies) ----
P = {
    "isabella_aerial": ("photos/isabella-48/4-800.webp", "Aerial view of the Isabella 48-foot yacht on Biscayne Bay"),
    "isabella_jetski": ("photos/isabella-48/1-800.webp", "Isabella 48 yacht with its jet ski in Miami"),
    "isabella_bow": ("photos/isabella-48/8-800.webp", "Bow sunpad of the Isabella 48 facing the Miami skyline"),
    "isabella_fly": ("photos/isabella-48/13-800.webp", "Shaded flybridge seating on the Isabella 48 with Miami skyline views"),
    "isabella_aft": ("photos/isabella-48/18-800.webp", "Aft deck seating on the Isabella 48 yacht"),
    "isabella_anchored": ("photos/isabella-48/7-800.webp", "Isabella 48 anchored on Biscayne Bay with downtown Miami behind"),
    "lchaim_fisher": ("photos/azimut-lchaim-65/4-800.webp", "Azimut L'chaim cruising past Fisher Island"),
    "lchaim_bow": ("photos/azimut-lchaim-65/2-800.webp", "Guests on the bow of the Azimut L'chaim off Fisher Island"),
    "lchaim_crew": ("photos/azimut-lchaim-65/32-800.webp", "Crew serving drinks to guests on the Azimut L'chaim"),
    "lchaim_aft": ("photos/azimut-lchaim-65/60_AZI_WEB-6-800.webp", "Aft deck table with the Brickell skyline behind the Azimut L'chaim"),
    "lchaim_dining": ("photos/azimut-lchaim-65/60_AZI_WEB-8-800.webp", "Aft deck dining area of the Azimut L'chaim in downtown Miami"),
    "lchaim_sunpad": ("photos/azimut-lchaim-65/60_AZI_WEB-13-800.webp", "Bow sunpad of the Azimut L'chaim facing downtown Miami"),
    "lchaim_swim": ("photos/azimut-lchaim-65/62_Azimut_Priceless_WEB-57-800.webp", "Guests on the swim platform of the Azimut L'chaim"),
    "lchaim_fly": ("photos/azimut-lchaim-65/60_AZI_WEB-16-800.webp", "Flybridge seating and table on the Azimut L'chaim"),
    "lchaim_run": ("photos/azimut-lchaim-65/1-800.webp", "65-foot Azimut L'chaim cruising off Miami"),
    "deepblue_aft": ("photos/deep-blue-90/deepblue-1-800.webp", "Aft deck of the 90-foot Deep Blue yacht"),
    "deepblue_2": ("photos/deep-blue-90/deepblue-2-800.webp", "90-foot Deep Blue superyacht in Miami"),
    "deepblue_10": ("photos/deep-blue-90/deepblue-10-800.webp", "Deck of the 90-foot Deep Blue yacht with Jacuzzi"),
    "deepblue_16": ("photos/deep-blue-90/deepblue-16-800.webp", "Interior salon of the Deep Blue 90 yacht"),
    "ferretti_bay": ("photos/ferretti-75/img-20240905-wa0032-800.webp", "Ferretti 75 yacht cruising Biscayne Bay in Miami"),
    "ferretti_fly": ("photos/ferretti-75/img-20240905-wa0034-800.webp", "Flybridge lounge with round table on the Ferretti 75 yacht"),
    "ferretti_table": ("photos/ferretti-75/img-20250613-wa0054-800.webp", "Champagne and appetizers on the Ferretti 75 aft deck table"),
    "anvera_skyline": ("photos/anvera-62/anveras-9-800.webp", "Aerial view of the 62-foot Anvera with the Miami skyline behind"),
    "anvera_brickell": ("photos/anvera-62/anveras-41-800.webp", "Anvera 62 running through downtown Miami near Brickell"),
    "anvera_loungers": ("photos/anvera-62/anveras-12-800.webp", "Aft sun loungers on the 62-foot Anvera yacht"),
    "axopar_speed": ("photos/axopar-brabus-28/photo-feb-17-2026-3-18-28-pm-1-800.webp", "Axopar 28 Brabus running at speed off Miami"),
    "axopar_bay": ("photos/axopar-brabus-28/1-800.webp", "28-foot Axopar Brabus Edition sport boat on Biscayne Bay"),
    "axopar_seats": ("photos/axopar-brabus-28/photo-feb-17-2026-3-18-28-pm-5-800.webp", "Rear bench seating on the Axopar 28 Brabus boat"),
    "yamaha_helm": ("photos/yamaha-255xd-25/easyfowey-9-800.webp", "Helm and cockpit of the Yamaha 255XD on Biscayne Bay"),
    "yamaha_4": ("photos/yamaha-255xd-25/easyfowey-4-800.webp", "25-foot Yamaha 255XD jet boat in Miami"),
    "maxum": ("photos/legacy/maxum-800.webp", "46-foot Maxum flybridge yacht"),
}

STEPS_EN = """<div class="myc-steps">
  <div class="myc-step"><div class="num">Step 1</div><h3>Call or WhatsApp</h3><p>Tell us your date, group size and the occasion. We answer 24/7 and check live availability while you&rsquo;re on the line.</p></div>
  <div class="myc-step"><div class="num">Step 2</div><h3>We match the yacht</h3><p>We recommend the right boat from our 9-vessel fleet for your group and budget &mdash; no platforms, no broker markup.</p></div>
  <div class="myc-step"><div class="num">Step 3</div><h3>Step aboard</h3><p>Meet us at our Miami River dock &mdash; about 10 minutes from Brickell and 15 from Miami Beach &mdash; and your captain takes it from there.</p></div>
</div>"""
STEPS_ES = """<div class="myc-steps">
  <div class="myc-step"><div class="num">Paso 1</div><h3>Llame o escriba por WhatsApp</h3><p>Díganos la fecha, cuántos son y la ocasión. Atendemos 24/7 en español y revisamos la disponibilidad real mientras hablamos.</p></div>
  <div class="myc-step"><div class="num">Paso 2</div><h3>Elegimos el yate</h3><p>Le recomendamos el barco ideal de nuestra flota de 9 embarcaciones según su grupo y presupuesto &mdash; sin plataformas ni comisiones de intermediarios.</p></div>
  <div class="myc-step"><div class="num">Paso 3</div><h3>Suba a bordo</h3><p>Nos vemos en nuestro muelle del río Miami &mdash; a unos 10 minutos de Brickell y 15 de Miami Beach &mdash; y su capitán se encarga del resto.</p></div>
</div>"""
STEPS_PT = """<div class="myc-steps">
  <div class="myc-step"><div class="num">Passo 1</div><h3>Ligue ou mande WhatsApp</h3><p>Diga a data, quantas pessoas e a ocasião. Atendemos 24 horas, em inglês e espanhol, e conferimos a disponibilidade na hora.</p></div>
  <div class="myc-step"><div class="num">Passo 2</div><h3>Escolhemos o iate</h3><p>Indicamos o barco certo da nossa frota de 9 embarcações para o seu grupo e orçamento &mdash; sem plataformas nem comissão de intermediários.</p></div>
  <div class="myc-step"><div class="num">Passo 3</div><h3>Embarque</h3><p>Encontro no nosso píer no Miami River &mdash; cerca de 10 minutos de Brickell e 15 de Miami Beach &mdash; e o capitão cuida do resto.</p></div>
</div>"""

PAGES = []

# ---------------------------------------------------------------- 1. Star Island
PAGES.append(dict(
    slug="star-island-boat-tour-miami",
    lang="en",
    title="Private Star Island Boat Tour Miami | Celebrity Homes",
    desc="A private Star Island boat tour in Miami: cruise past the celebrity homes of Star, Palm and Hibiscus Islands and the Millionaire's Row waterfront on your own yacht. Captain and crew included, from $1,000 for 4 hours.",
    h1="Private Star Island Boat Tour in Miami",
    crumb="Star Island Boat Tour",
    lede="See the celebrity mansions of Star Island, Palm Island and Hibiscus Island from your own private yacht &mdash; no ticket line, no crowd, no shared deck. Captain and crew included, from $1,000 for 4 hours.",
    facts=[("Starting at", "$1,000 / 4 hrs"), ("Route", "Star Island, Fisher Island &amp; the skyline"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["lchaim_fisher"][0],
    wa="Hi! I'd like to book a private Star Island boat tour in Miami. My date:",
    body=f"""
<h2>The celebrity homes tour, without the tour boat</h2>
<p>Every visitor to Miami hears about Star Island: the gated island of waterfront mansions between downtown and South Beach where the famous have lived for a century. The usual way to see it is a ticketed sightseeing boat with a hundred strangers and a microphone. The better way is a private yacht. Your group, your captain, your pace, and the islands that tour companies sell as Millionaire's Row right off the rail.</p>
<p>Our charters leave from the Miami River, which puts you on Biscayne Bay within minutes. From there the route runs past Star Island, Palm Island and Hibiscus Island, along the Venetian Islands, down past Fisher Island and back along the downtown and Brickell skyline. You can slow down where you want, stop for a swim, and make it a sunset cruise if the timing works.</p>

<h2>What you cruise past</h2>
<ul>
<li><strong>Star Island:</strong> The famous one. A single loop road of waterfront estates behind a guarded gate, best seen exactly the way we see it: from the water.</li>
<li><strong>Palm and Hibiscus Islands:</strong> Star Island's quieter neighbors on the MacArthur Causeway, lined with the same scale of homes.</li>
<li><strong>The Venetian Islands:</strong> A chain of residential islands strung along the Venetian Causeway between Miami and Miami Beach.</li>
<li><strong>Fisher Island:</strong> The private island at the mouth of Government Cut, reachable only by boat or ferry.</li>
<li><strong>The skyline:</strong> Downtown Miami and Brickell from the bay, which is the view every photo of Miami is trying to get.</li>
</ul>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>A private Star Island cruise, hour by hour</h2>
<ul>
<li><strong>Hour 1:</strong> Board on the Miami River and cruise downriver past the Brickell towers into Biscayne Bay.</li>
<li><strong>Hour 2:</strong> Loop Star Island, Palm Island and Hibiscus Island, then run the Venetian Islands with South Beach ahead of you.</li>
<li><strong>Hour 3:</strong> Down past Fisher Island and Government Cut. Drop anchor for a swim if the group wants it.</li>
<li><strong>Hour 4:</strong> The slow ride home along the skyline. Book the late slot and this is your sunset.</li>
</ul>
<p>Want the water stop to be the main event instead? Pair the islands with a <a href="sandbar-yacht-charter-miami.html">sandbar day</a> at Nixon's Sandbar.</p>

<h2>On the water off Star Island</h2>
{{GALLERY}}

<h2>Boats for a Star Island tour</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a> or compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>. Staying on the beach side? See <a href="south-beach-yacht-rental.html">yacht rental from South Beach</a>.</p>
""",
    gallery=["lchaim_fisher", "lchaim_bow", "anvera_brickell", "isabella_bow"],
    table=[("isabella", "Flybridge views and a jet ski at the swim stop"), ("axopar-brabus", "Fast sport boat for a couple or small group"), ("maxum", "Best-value yacht for the islands loop"), ("azimut-lchaim", "Three decks for a group that wants the full cruise"), ("deep-blue", "The 90-foot superyacht with a jacuzzi on deck")],
    faq=[
        ("How much does a private Star Island boat tour cost?", "From $1,000 for 4 hours on the 46' Maxum or the 25' Yamaha 255XD, with a licensed captain and crew included. The 48' Isabella with a jet ski is $1,499 for 4 hours, and the fleet runs up to the 90' Deep Blue at $4,999."),
        ("Can you see the celebrity homes from the boat?", "Yes. The homes on Star, Palm and Hibiscus Islands face the water, so a boat is the only way to see them up close. Your captain runs the loop at a slow pace so you can take it in."),
        ("How long is the tour?", "Every charter is 4 hours. The Star Island loop takes a fraction of that, so the rest of the time is yours: cruise the skyline, swim off the boat, or time the return for sunset."),
        ("Where does the boat leave from?", "Our dock on the Miami River at 668 NW N River Dr, about 10 minutes from Brickell and 15 from Miami Beach. Star Island is a short cruise from the river mouth."),
        ("Is this a guided tour with commentary?", "It is a private charter, not a scripted tour. Your captain knows the bay and the islands and is happy to point things out along the way."),
    ],
    cta=("See Star Island from your own yacht", "Afternoon and sunset slots fill first. Call or WhatsApp and we'll hold the boat for your date today."),
    related=[("private-sunset-cruise-miami.html", "Private sunset cruise"), ("sandbar-yacht-charter-miami.html", "Sandbar charter"), ("yacht-charter-before-cruise-miami.html", "Before or after your cruise"), ("south-beach-yacht-rental.html", "South Beach yacht rental")],
    service=("Private Star Island Boat Tour", "Private yacht charter past the celebrity homes of Star Island, Palm Island, Hibiscus Island and Fisher Island in Miami. Licensed captain and crew included. From $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 2. South Beach
PAGES.append(dict(
    slug="south-beach-yacht-rental",
    lang="en",
    title="South Beach Yacht Rental | Private Charters from $1,000",
    desc="Staying in South Beach? Private yacht and boat rentals board 15 minutes away on the Miami River and cruise Star Island, Fisher Island and the skyline. Captain and crew included, from $1,000 for 4 hours.",
    h1="Yacht Rental for South Beach",
    crumb="South Beach",
    lede="Private yachts and boats for South Beach visitors &mdash; board on the Miami River about 15 minutes from Ocean Drive, cruise past Star Island and Fisher Island, and be back for dinner. Captain and crew included, from $1,000 for 4 hours.",
    facts=[("Starting at", "$1,000 / 4 hrs"), ("From South Beach", "About 15 minutes to the dock"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["isabella_aerial"][0],
    wa="Hi! I'm staying in South Beach and I'd like to rent a yacht. My date:",
    body=f"""
<h2>The boat day from South Beach</h2>
<p>South Beach is where most Miami trips are based, and a yacht is the best half-day you can add to one. Our charters board on the Miami River, about 15 minutes from Ocean Drive by car or rideshare across the MacArthur Causeway. Within minutes of leaving the dock you are on Biscayne Bay with the skyline behind you and the islands ahead.</p>
<p>Every charter is private: your group only, with a licensed captain and crew included in the price. Pick the boat, pick the date, and tell us whether you want a swim stop at the sandbar, a loop of the celebrity islands, or a sunset run along the skyline.</p>

<h2>Getting to the dock from South Beach</h2>
<ul>
<li><strong>Address:</strong> 668 NW N River Dr, Miami, FL 33136, on the Miami River.</li>
<li><strong>From Ocean Drive, Collins Avenue or Lincoln Road:</strong> About 15 minutes by car via the MacArthur Causeway, which runs right past Star Island on the way.</li>
<li><strong>Rideshare:</strong> Straightforward to the address above; we will confirm the exact meeting point when you book.</li>
</ul>
<p>Also staying on the beach? The <a href="yacht-rental-miami-beach.html">Miami Beach page</a> covers Mid-Beach and North Beach, and <a href="yacht-rental-brickell.html">Brickell and Downtown</a> is 10 minutes from the dock.</p>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>Where a South Beach charter goes</h2>
<ul>
<li><strong>Star Island, Palm and Hibiscus Islands:</strong> The celebrity-home islands you drove past on the causeway, seen from the water on a <a href="star-island-boat-tour-miami.html">private Star Island tour</a>.</li>
<li><strong>Fisher Island and Government Cut:</strong> The private island and the shipping channel at the southern tip of South Beach.</li>
<li><strong>Nixon's Sandbar:</strong> Shallow, clear water off Key Biscayne for the swim stop.</li>
<li><strong>The skyline:</strong> Downtown and Brickell from Biscayne Bay, best at sunset.</li>
</ul>

<h2>On the water</h2>
{{GALLERY}}

<h2>Boats popular with South Beach guests</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a> or compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>.</p>
""",
    gallery=["isabella_aerial", "lchaim_fisher", "axopar_speed", "deepblue_aft"],
    table=[("isabella", "Flybridge yacht with a jet ski included"), ("anvera", "Open-deck Italian yacht, loungers at the stern"), ("axopar-brabus", "Sport boat for a couple or small group"), ("azimut-lchaim", "Three decks and a bow sunpad"), ("deep-blue", "The 90-foot superyacht with a jacuzzi")],
    faq=[
        ("Do you pick up in South Beach?", "Charters board at our Miami River dock, about 15 minutes from South Beach by car. We confirm the meeting point with you when you book."),
        ("How much does a yacht rental near South Beach cost?", "From $1,000 for 4 hours with a licensed captain and crew included. The 48' Isabella with Jet Ski is $1,499, the 65' Azimut L'chaim is $3,000 and the 90' Deep Blue with Jacuzzi is $4,999, all for 4 hours."),
        ("Can we do a sunset cruise?", "Yes. Tell us when you book and we schedule the 4 hours so the last hour runs along the skyline at sunset. See the private sunset cruise page for the route."),
        ("Do we need a license or experience?", "No. Every charter comes with a licensed captain and crew."),
    ],
    cta=("Book your South Beach boat day", "Weekend and sunset slots go first. Call or WhatsApp and we'll hold the boat for your date today."),
    related=[("star-island-boat-tour-miami.html", "Star Island boat tour"), ("yacht-rental-miami-beach.html", "Miami Beach yacht rental"), ("private-sunset-cruise-miami.html", "Private sunset cruise"), ("yacht-party-miami.html", "Yacht parties")],
    service=("South Beach Yacht Rental", "Private yacht and boat charters for South Beach visitors, boarding on the Miami River about 15 minutes away. Licensed captain and crew included. From $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 3. Art Basel
PAGES.append(dict(
    slug="art-basel-yacht-charter-miami",
    lang="en",
    title="Art Basel Yacht Charter Miami 2026 | Private from $1,000",
    desc="Private yacht charters during Art Basel Miami Beach, December 4 to 6, 2026. Same prices as any other week: captain and crew included, from $1,000 for 4 hours. Skyline cruises, sunset runs and private parties on Biscayne Bay.",
    h1="Art Basel Yacht Charter in Miami",
    crumb="Art Basel",
    lede="Art Basel Miami Beach runs December 4 to 6, 2026. Get off the convention floor and onto the water: private yachts with captain and crew, at our regular prices, from $1,000 for 4 hours.",
    facts=[("Dates", "Dec 4&ndash;6, 2026 (previews Dec 2&ndash;3)"), ("Starting at", "$1,000 / 4 hrs"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["deepblue_aft"][0],
    wa="Hi! I'd like to book a yacht during Art Basel week in Miami. My date:",
    body=f"""
<h2>Basel week on the water</h2>
<p>For one week in December the whole art world is in Miami Beach, and the best seat in the city is on a boat. A private yacht gives your group a few hours away from the fair crowds, with the skyline, the islands and the sunset as the backdrop. Collectors use it to host clients, galleries use it to entertain, and groups of friends use it to turn an afternoon off into the best day of the trip.</p>
<p>We do not add an event surcharge. Art Basel week is priced like any other week: every charter is 4 hours with a licensed captain and crew included, from $1,000 on the 46' Maxum to $4,999 on the 90' Deep Blue with its jacuzzi.</p>

<h2>Art Basel Miami Beach 2026 dates</h2>
<ul>
<li><strong>VIP preview days:</strong> December 2 and 3, 2026.</li>
<li><strong>Public days:</strong> December 4 to 6, 2026, at the Miami Beach Convention Center.</li>
<li><strong>Our dock:</strong> 668 NW N River Dr on the Miami River, about 15 minutes from the Convention Center by car.</li>
</ul>
<p>Boats book out around the fair, so the earlier you call, the more of the fleet is open on your date.</p>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>Three ways to do Basel on a yacht</h2>
<ul>
<li><strong>Client hospitality:</strong> A <a href="corporate-yacht-charter-miami.html">corporate charter</a> on the 65' Azimut L'chaim, 75' Ferretti or 90' Deep Blue: the aft deck for conversation, the flybridge for the view, and a dock 15 minutes from the fair.</li>
<li><strong>The sunset escape:</strong> A late-afternoon slot so the last hour runs the <a href="private-sunset-cruise-miami.html">skyline at sunset</a> before the night's events.</li>
<li><strong>The daytime reset:</strong> Star Island, Fisher Island and a swim at Nixon's Sandbar on the 48' Isabella or 62' Anvera, back in time for the evening openings.</li>
</ul>

<h2>On the water in December</h2>
{{GALLERY}}

<h2>Yachts for Art Basel week</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a> or compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>.</p>
""",
    gallery=["deepblue_aft", "ferretti_table", "lchaim_aft", "anvera_skyline"],
    table=[("deep-blue", "The superyacht with a jacuzzi for hosting"), ("ferretti", "Flybridge lounge and a dining table on the aft deck"), ("azimut-lchaim", "Three decks for a larger group"), ("anvera", "Sleek open-deck Italian design"), ("isabella", "Flybridge yacht with a jet ski")],
    faq=[
        ("Are prices higher during Art Basel?", "No. Our prices are the same every week of the year: from $1,000 for 4 hours with captain and crew included."),
        ("How far is the dock from the Miami Beach Convention Center?", "About 15 minutes by car. Our dock is at 668 NW N River Dr on the Miami River."),
        ("Can we host clients on board?", "Yes. The 65' Azimut L'chaim, 75' Ferretti and 90' Deep Blue all have an aft deck with a table and a flybridge with a view, and the crew looks after your guests."),
        ("When should we book for Basel week?", "As early as you can. The fair draws a crowd that books boats, and the first weekend of December fills first."),
    ],
    cta=("Lock in your Basel week slot", "December 4 to 6 fills early. Call or WhatsApp and we'll hold the yacht for your date today."),
    related=[("corporate-yacht-charter-miami.html", "Corporate charters"), ("private-sunset-cruise-miami.html", "Private sunset cruise"), ("new-years-eve-yacht-miami.html", "New Year's Eve on a yacht"), ("deep-blue.html", "90' Deep Blue with Jacuzzi")],
    service=("Art Basel Yacht Charter Miami", "Private yacht charters during Art Basel Miami Beach, December 2026. Licensed captain and crew included, regular prices from $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 4. New Year's Eve
PAGES.append(dict(
    slug="new-years-eve-yacht-miami",
    lang="en",
    title="New Year's Eve Yacht Party Miami | Private from $1,000",
    desc="Ring in the new year on a private yacht in Miami. Your group only, captain and crew included, same price as any night: from $1,000 for 4 hours. Skyline and Biscayne Bay on December 31.",
    h1="New Year's Eve Yacht Party in Miami",
    crumb="New Year's Eve",
    lede="Skip the ticketed party boats. Spend December 31 on a private yacht with your own group, a licensed captain and crew, and the Miami skyline lit up around you &mdash; at our regular prices, from $1,000 for 4 hours.",
    facts=[("Date", "December 31, 2026"), ("Starting at", "$1,000 / 4 hrs"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["lchaim_crew"][0],
    wa="Hi! I'd like to book a private yacht for New Year's Eve in Miami. Group size:",
    body=f"""
<h2>Your own boat, your own countdown</h2>
<p>New Year's Eve in Miami means ticketed cruises that sell hundreds of seats and sell out early. A private charter is the opposite: one yacht, your group, your music, and a crew whose only job that night is you. The skyline, the causeway lights and the bay are the same view the big boats sell by the seat, and you get the deck to yourselves.</p>
<p>We charge the same price on December 31 as on any other night: every charter is 4 hours with a licensed captain and crew included, from $1,000 on the 46' Maxum to $4,999 on the 90' Deep Blue with Jacuzzi.</p>

<h2>Two ways to spend the night</h2>
<ul>
<li><strong>The early cruise:</strong> Board in the late afternoon, catch the last sunset of the year over the skyline, and be back at the dock in time for dinner and the city's midnight parties.</li>
<li><strong>The night cruise:</strong> A later slot so the city is lit while you are on the water. Tell us when you book and we schedule the 4 hours around the time that matters to you.</li>
</ul>
<p>Miami's public New Year's fireworks are shot from the downtown waterfront at Bayfront Park and from the Miami Beach oceanfront. If seeing them from the water matters to your plan, say so when you call and we will talk through the timing honestly before you book.</p>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>Why it works</h2>
<ul>
<li><strong>Private:</strong> No shared deck, no strangers in your photos, no line to board.</li>
<li><strong>Crewed:</strong> A licensed captain and crew on every boat, so nobody in your group is the designated skipper.</li>
<li><strong>Flexible:</strong> Pick the boat, the slot and the route. Star Island, Fisher Island and the skyline are all a short cruise from the dock.</li>
<li><strong>Same price:</strong> No holiday surcharge.</li>
</ul>

<h2>Nights on the bay</h2>
{{GALLERY}}

<h2>Yachts for New Year's Eve</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a> or compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>. Planning a full <a href="yacht-party-miami.html">yacht party</a>? That page covers the music, the route and the boats.</p>
""",
    gallery=["lchaim_crew", "deepblue_16", "ferretti_table", "lchaim_dining"],
    table=[("azimut-lchaim", "Three decks and a salon for a group celebration"), ("deep-blue", "Superyacht with a jacuzzi and a full salon"), ("ferretti", "Flybridge lounge and aft deck dining"), ("isabella", "Flybridge yacht for a smaller group"), ("maxum", "Best-value yacht for the night")],
    faq=[
        ("Is there a surcharge for New Year's Eve?", "No. Our prices are the same on December 31 as any other night: from $1,000 for 4 hours with captain and crew included."),
        ("Can we see the fireworks from the boat?", "Miami's public fireworks are launched from Bayfront Park downtown and from the Miami Beach oceanfront at midnight. Whether a charter can be on the water at that time depends on the slot, so tell us your plan when you call and we will be straight with you about what is possible."),
        ("How long is a New Year's Eve charter?", "Every charter is 4 hours. You choose whether that window is the afternoon sunset run or a night cruise."),
        ("When should we book?", "Early. New Year's Eve is one of the first dates of the year to fill, and the bigger yachts go first."),
    ],
    cta=("Book the yacht for December 31", "The last night of the year fills first. Call or WhatsApp and we'll hold the boat for your group today."),
    related=[("yacht-party-miami.html", "Private yacht parties"), ("private-sunset-cruise-miami.html", "Private sunset cruise"), ("art-basel-yacht-charter-miami.html", "Art Basel week"), ("miami-yacht-rental-prices.html", "Rental prices")],
    service=("New Year's Eve Yacht Party Miami", "Private New Year's Eve yacht charters in Miami with licensed captain and crew included. Regular prices, from $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 5. Spring Break / Miami Music Week
PAGES.append(dict(
    slug="spring-break-yacht-miami",
    lang="en",
    title="Spring Break Yacht Party Miami | Ultra &amp; Music Week 2027",
    desc="Private spring break yacht parties in Miami, including Miami Music Week and Ultra weekend, March 22 to 28, 2027. Your own boat with captain and crew, from $1,000 for 4 hours. No ticketed party boat.",
    h1="Spring Break Yacht Party in Miami",
    crumb="Spring Break",
    lede="March in Miami is spring break, Miami Music Week and Ultra all at once. Get your group its own yacht instead of a ticket on a party boat: captain and crew included, from $1,000 for 4 hours.",
    facts=[("Peak dates", "Miami Music Week Mar 22&ndash;28, 2027"), ("Starting at", "$1,000 / 4 hrs"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["isabella_jetski"][0],
    wa="Hi! I'd like to book a spring break yacht party in Miami. My date and group size:",
    body=f"""
<h2>Your spring break boat, not a ticket</h2>
<p>Every March the party boats in Miami sell tickets by the hundred. A private charter is a different day: one yacht, your group, your playlist on the speakers, a swim stop at the sandbar and a licensed captain and crew who handle everything else. You split the cost of the boat across the group rather than paying per head, and nobody you did not invite is on board.</p>
<p>Same price as any other week. Every charter is 4 hours with captain and crew included, from $1,000 on the 46' Maxum or 25' Yamaha 255XD to $4,999 on the 90' Deep Blue.</p>

<h2>The March calendar</h2>
<ul>
<li><strong>Spring break:</strong> College weeks run through March, with the first half the busiest on the water.</li>
<li><strong>Miami Music Week:</strong> March 22 to 28, 2027, the week of pool parties and club nights that surrounds Ultra.</li>
<li><strong>Ultra Music Festival:</strong> March 26 to 28, 2027, at Bayfront Park on the downtown waterfront. A daytime charter before the festival gates open is the classic move.</li>
</ul>
<p>Weekend boats in March book out early. Call as soon as your dates are set.</p>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>A spring break charter, hour by hour</h2>
<ul>
<li><strong>Hour 1:</strong> Board on the Miami River and cruise out past the Brickell skyline into Biscayne Bay.</li>
<li><strong>Hour 2:</strong> Star Island and Fisher Island on the way south.</li>
<li><strong>Hour 3:</strong> Anchor at Nixon's Sandbar. Swim, float, music up. On the Isabella the jet ski comes out here.</li>
<li><strong>Hour 4:</strong> The ride home with the skyline ahead, back at the dock in time for the night.</li>
</ul>

<h2>Spring break on our boats</h2>
{{GALLERY}}

<h2>Boats for a spring break group</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a>, compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>, or see the <a href="party-boat-rental-miami.html">party boat</a> and <a href="yacht-party-miami.html">yacht party</a> pages.</p>
""",
    gallery=["isabella_jetski", "lchaim_swim", "axopar_speed", "anvera_loungers"],
    table=[("isabella", "Jet ski included for the sandbar stop"), ("azimut-lchaim", "Three decks for the biggest group"), ("anvera", "Open deck built for sun and music"), ("maxum", "Best-value yacht for a group on a budget"), ("yamaha-255xd", "Fast jet boat for a small crew")],
    faq=[
        ("How much is a spring break yacht in Miami?", "From $1,000 for 4 hours with captain and crew included, split however your group likes. The 48' Isabella with a jet ski is $1,499 and the 65' Azimut L'chaim is $3,000 for 4 hours."),
        ("Do you raise prices for Ultra or Music Week?", "No. Prices are the same every week of the year."),
        ("Can we bring our own music?", "Yes. Bring your playlist. Every charter is private, so the speakers are yours for the 4 hours."),
        ("Can we swim?", "Yes. Nixon's Sandbar off Key Biscayne is the swim stop on most March charters, and the captain picks the spot for the day's wind and tide."),
        ("Do we need a license?", "No. A licensed captain and crew run every charter."),
    ],
    cta=("Get your group's boat for March", "Spring break weekends go first. Call or WhatsApp and we'll hold the yacht for your date today."),
    related=[("yacht-party-miami.html", "Yacht parties"), ("party-boat-rental-miami.html", "Party boat rental"), ("sandbar-yacht-charter-miami.html", "Sandbar charter"), ("bachelor-party-yacht-miami.html", "Bachelor parties")],
    service=("Spring Break Yacht Party Miami", "Private spring break and Miami Music Week yacht charters in Miami with licensed captain and crew included. From $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 6. Miami Grand Prix
PAGES.append(dict(
    slug="miami-grand-prix-yacht-charter",
    lang="en",
    title="Miami Grand Prix Yacht Charter | F1 Weekend from $1,000",
    desc="Private yacht charters for Formula 1 Miami Grand Prix weekend in early May. Skip the superyacht broker: your own yacht with captain and crew, at regular prices from $1,000 for 4 hours, on Biscayne Bay.",
    h1="Miami Grand Prix Yacht Charter",
    crumb="Miami Grand Prix",
    lede="F1 weekend brings the world to Miami. Before or after the race, give your group the water: a private yacht with captain and crew, regular prices, from $1,000 for 4 hours.",
    facts=[("Race weekend", "Early May 2027"), ("Starting at", "$1,000 / 4 hrs"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["anvera_skyline"][0],
    wa="Hi! I'd like to book a yacht for Miami Grand Prix weekend. My date:",
    body=f"""
<h2>Race weekend, off the track</h2>
<p>The Miami Grand Prix runs at the Miami International Autodrome in Miami Gardens, and the city around it turns into a week of parties, brand events and visitors who have come a long way. Search for a yacht that week and you will find brokers offering superyachts by the week at six figures. We do the day version: a private yacht for 4 hours with a licensed captain and crew, at the same prices as any other weekend.</p>
<p>Our dock is on the Miami River in the middle of the city, 10 minutes from Brickell and 15 from Miami Beach, so a charter fits between the practice sessions, the race and the evening events.</p>

<h2>The race weekend plan</h2>
<ul>
<li><strong>Friday or Saturday afternoon:</strong> A skyline cruise, a loop past Star Island and Fisher Island, and a swim at Nixon's Sandbar before the evening parties.</li>
<li><strong>Sunday morning:</strong> The quiet option before the race. Board early, cruise the bay while the city sleeps in, and be back with time to get to Miami Gardens.</li>
<li><strong>Monday:</strong> The day most visitors have free and nobody plans. Book it before you arrive.</li>
</ul>
<p>The 2027 race is scheduled for early May. Check the official Formula 1 calendar for the exact dates, then call us for the boat.</p>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>For clients and teams</h2>
<p>Hosting during Grand Prix week? The 65' Azimut L'chaim, 75' Ferretti and 90' Deep Blue all have an aft deck with a dining table, a flybridge with the view and a crew to look after your guests. See the <a href="corporate-yacht-charter-miami.html">corporate charter page</a> for how we run client days.</p>

<h2>Fast boats, big boats</h2>
{{GALLERY}}

<h2>Yachts for Grand Prix weekend</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a> or compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>.</p>
""",
    gallery=["anvera_skyline", "axopar_speed", "deepblue_10", "ferretti_bay"],
    table=[("deep-blue", "Superyacht with a jacuzzi for hosting"), ("anvera", "The fastest-looking yacht in the fleet"), ("axopar-brabus", "Brabus-edition sport boat, twin outboards"), ("ferretti", "Flybridge lounge and aft deck dining"), ("azimut-lchaim", "Three decks for a bigger group")],
    faq=[
        ("Do prices go up for Grand Prix weekend?", "No. Our prices are the same every week: from $1,000 for 4 hours with captain and crew included."),
        ("Can we charter by the hour or for a full day?", "Every charter is 4 hours. Book two slots on different days if you want the water twice over the weekend."),
        ("How far is the dock from the circuit?", "The Autodrome is in Miami Gardens, north of the city. Our dock is on the Miami River downtown, so plan a charter for a different part of the day than the race sessions."),
        ("Can we host clients on board?", "Yes. The larger yachts have an aft deck table, a salon and a flybridge, and the crew takes care of your guests."),
    ],
    cta=("Book the boat for race weekend", "F1 week fills early across the city. Call or WhatsApp and we'll hold the yacht for your date today."),
    related=[("corporate-yacht-charter-miami.html", "Corporate charters"), ("star-island-boat-tour-miami.html", "Star Island boat tour"), ("art-basel-yacht-charter-miami.html", "Art Basel week"), ("anvera.html", "62' Anvera")],
    service=("Miami Grand Prix Yacht Charter", "Private yacht charters for Formula 1 Miami Grand Prix weekend with licensed captain and crew included. Regular prices from $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 7. Before or after your cruise
PAGES.append(dict(
    slug="yacht-charter-before-cruise-miami",
    lang="en",
    title="Yacht Charter Before or After Your Cruise | PortMiami",
    desc="Sailing from PortMiami? Spend the day before or after your cruise on a private yacht. Board minutes from downtown, cruise Star Island and the skyline with captain and crew, from $1,000 for 4 hours.",
    h1="A Private Yacht Day Before or After Your Cruise",
    crumb="Before Your Cruise",
    lede="Flying in a day early or staying a day after your cruise? Four hours on a private yacht turns the layover into the best part of the trip. Captain and crew included, from $1,000.",
    facts=[("Starting at", "$1,000 / 4 hrs"), ("Dock", "Miami River, minutes from downtown"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["anvera_brickell"][0],
    wa="Hi! I'm in Miami before/after a cruise and I'd like to book a yacht. My date:",
    body=f"""
<h2>The day the cruise itinerary leaves empty</h2>
<p>Most cruise lines tell you to arrive in Miami the day before you sail, and plenty of ships dock back early on the last morning. That leaves a day in Miami that most people spend in a hotel lobby. A private charter is the better answer: board a yacht a short ride from PortMiami, cruise the skyline and the celebrity islands, swim at the sandbar and be back on land with the whole evening ahead of you.</p>
<p>Every charter is 4 hours with a licensed captain and crew included, from $1,000. You bring the group; we bring the boat and the bay.</p>

<h2>Where the yacht day fits</h2>
<ul>
<li><strong>The day before you sail:</strong> Land in the morning, drop the bags at the hotel, and spend the afternoon on the water. A sunset slot ends the day on the skyline.</li>
<li><strong>Debarkation day:</strong> Ships typically clear passengers in the morning. A late-morning or midday charter uses the hours before an evening flight.</li>
<li><strong>Cruise ship in the photos:</strong> PortMiami sits at the mouth of the Miami River on Government Cut, so the route out of the river passes the port and the ships docked there.</li>
</ul>
<p>Luggage: our dock is a working marina, not a storage facility, so plan to leave bags at your hotel or with the cruise line before you come to the boat.</p>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>Four hours, hour by hour</h2>
<ul>
<li><strong>Hour 1:</strong> Board on the Miami River and cruise downriver past the Brickell skyline toward the port and Biscayne Bay.</li>
<li><strong>Hour 2:</strong> Star Island, Palm Island and Hibiscus Island, then Fisher Island at the mouth of Government Cut.</li>
<li><strong>Hour 3:</strong> Anchor at Nixon's Sandbar for a swim, or keep cruising if the group would rather stay dry.</li>
<li><strong>Hour 4:</strong> Back along the skyline to the dock.</li>
</ul>

<h2>The Miami you see from the water</h2>
{{GALLERY}}

<h2>Boats for a cruise-day charter</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a>, compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>, or read <a href="what-to-bring-yacht-charter-miami.html">what to bring on a charter</a>.</p>
""",
    gallery=["anvera_brickell", "lchaim_fisher", "isabella_anchored", "yamaha_helm"],
    table=[("isabella", "Flybridge yacht with a jet ski for the swim stop"), ("maxum", "Best-value yacht for a family or small group"), ("axopar-brabus", "Fast sport boat for a couple"), ("anvera", "Open-deck Italian yacht with loungers"), ("azimut-lchaim", "Three decks for a bigger group")],
    faq=[
        ("How far is your dock from PortMiami?", "Our dock is at 668 NW N River Dr on the Miami River, in the middle of the city and a short ride from the port and the downtown hotels. We confirm the meeting point when you book."),
        ("Can we fit a charter in before boarding the ship?", "Every charter is 4 hours. Tell us your ship's boarding window when you call and we will tell you honestly whether a morning slot works for your date."),
        ("Can you store our luggage?", "No. Leave bags with your hotel or the cruise line before coming to the dock."),
        ("Do we need any boating experience?", "No. A licensed captain and crew are included on every charter."),
    ],
    cta=("Book the day around your cruise", "Pre-cruise afternoons book up with the ship schedules. Call or WhatsApp and we'll hold the boat for your date today."),
    related=[("star-island-boat-tour-miami.html", "Star Island boat tour"), ("yacht-rental-brickell.html", "Brickell and Downtown"), ("family-yacht-charter-miami.html", "Family charters"), ("sandbar-yacht-charter-miami.html", "Sandbar charter")],
    service=("Pre-Cruise and Post-Cruise Yacht Charter Miami", "Private 4-hour yacht charters for cruise passengers with a day in Miami before or after sailing from PortMiami. Licensed captain and crew included. From $1,000.", "1000"),
))

# ---------------------------------------------------------------- 8. Photoshoot
PAGES.append(dict(
    slug="yacht-photoshoot-miami",
    lang="en",
    title="Yacht Photoshoot Miami | Rent a Yacht for Photo &amp; Video",
    desc="Rent a private yacht in Miami for a photoshoot, video shoot or content day. Commercial shoots welcome. Skyline, Star Island and open-water backdrops, captain and crew included, from $1,000 for 4 hours.",
    h1="Yacht Photoshoot &amp; Video Shoot Rental in Miami",
    crumb="Photoshoots",
    lede="Book a private yacht as your set. Brand shoots, music videos, content days and personal sessions are all welcome, with a captain who positions the boat for the shot. From $1,000 for 4 hours.",
    facts=[("Starting at", "$1,000 / 4 hrs"), ("Shoots", "Commercial photo &amp; video welcome"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["lchaim_sunpad"][0],
    wa="Hi! I'd like to rent a yacht for a photo/video shoot in Miami. My date:",
    body=f"""
<h2>A set that moves</h2>
<p>Miami's best backdrops are on the water: the Brickell skyline at golden hour, the mansions of Star Island, the open bay with nothing behind the subject but blue. A private yacht puts all of them in one 4-hour session, with a licensed captain who holds the boat where the light is and a crew who stays out of frame.</p>
<p>Commercial shoots are welcome. We host brand campaigns, music videos, fashion lookbooks, creator content days, engagement and family sessions, and everything in between. Tell us the shot list when you book and we will recommend the boat that fits it.</p>

<h2>Boats as sets</h2>
<ul>
<li><strong>90' Deep Blue:</strong> A jacuzzi on deck, a cream-and-wood salon, a formal dining table and a master cabin below. The superyacht look.</li>
<li><strong>65' Azimut L'chaim:</strong> Three levels to shoot on: a flybridge with a sunpad, a teak aft deck with a dining table and a wide bow sunpad facing downtown.</li>
<li><strong>62' Anvera:</strong> One long open deck with fold-down terraces at the stern and sun loungers. Clean modern lines for product and fashion.</li>
<li><strong>48' Isabella:</strong> A jet ski included, a flybridge with wraparound seating and a bow sunpad with the skyline behind it.</li>
<li><strong>28' Axopar Brabus:</strong> A navy diamond-stitched sport boat that photographs fast even standing still.</li>
</ul>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>Light and locations</h2>
<ul>
<li><strong>Golden hour:</strong> Book the late slot so the last hour is the skyline at sunset. See the <a href="best-time-yacht-charter-miami.html">best time guide</a> for how the light runs through the year.</li>
<li><strong>Star Island and Fisher Island:</strong> Mansions and palms in the background, a short cruise from the dock.</li>
<li><strong>Open bay and sandbar:</strong> Turquoise water at Nixon's Sandbar for swimwear and in-water shots.</li>
<li><strong>Brickell from the river:</strong> The first minutes out of the dock run straight past the towers.</li>
</ul>

<h2>Frames from our decks</h2>
{{GALLERY}}

<h2>Yachts for a shoot</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a> or compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>.</p>
""",
    gallery=["lchaim_sunpad", "isabella_bow", "anvera_loungers", "deepblue_16"],
    table=[("deep-blue", "Jacuzzi, salon and master cabin: the superyacht look"), ("azimut-lchaim", "Three decks, bow sunpad facing downtown"), ("anvera", "Modern open deck and fold-down terraces"), ("isabella", "Flybridge, bow sunpad and a jet ski"), ("axopar-brabus", "Brabus sport boat for action shots")],
    faq=[
        ("Can we do a commercial photo or video shoot on board?", "Yes. Commercial photo and video shoots are welcome, including brand campaigns, music videos and creator content. Tell us the plan when you book."),
        ("How much does a yacht rental for a photoshoot cost?", "The same as any charter: from $1,000 for 4 hours with captain and crew included, up to $4,999 for the 90' Deep Blue."),
        ("Can the captain position the boat for specific shots?", "Yes. Share the shot list and the captain will hold the boat for the skyline, the islands or open water as the light allows."),
        ("Is 4 hours enough for a shoot?", "Every charter is 4 hours, which covers two or three locations and a golden-hour finish. Book two charters on separate days for a bigger production."),
    ],
    cta=("Book your yacht as a set", "Golden-hour slots go first. Call or WhatsApp with your shoot date and we'll hold the boat today."),
    related=[("private-sunset-cruise-miami.html", "Private sunset cruise"), ("proposal-yacht-charter-miami.html", "Proposals and anniversaries"), ("deep-blue.html", "90' Deep Blue with Jacuzzi"), ("azimut-lchaim.html", "65' Azimut L'chaim")],
    service=("Yacht Photoshoot and Video Shoot Rental Miami", "Private yacht rental in Miami for commercial and personal photo and video shoots. Licensed captain and crew included. From $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 9. Family
PAGES.append(dict(
    slug="family-yacht-charter-miami",
    lang="en",
    title="Family Yacht Charter Miami | Kids Welcome, from $1,000",
    desc="Private family yacht charters in Miami with children welcome and children's life jackets on board. Captain and crew included, calm Biscayne Bay routes, a sandbar swim stop, from $1,000 for 4 hours.",
    h1="Family Yacht Charter in Miami",
    crumb="Family Charters",
    lede="A private boat day the whole family can do: children welcome, children's life jackets on board, a licensed captain and crew, and calm bay water with a swim stop. From $1,000 for 4 hours.",
    facts=[("Starting at", "$1,000 / 4 hrs"), ("Kids", "Welcome, life jackets on board"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["isabella_anchored"][0],
    wa="Hi! I'd like to book a family yacht charter in Miami. Our date and ages of the kids:",
    body=f"""
<h2>The Miami day for the whole family</h2>
<p>A private charter is the family-friendly way to see Miami from the water. There are no crowds and no shared deck, the route stays on the sheltered water of Biscayne Bay, and the day runs at the pace of the youngest person on board. Children are welcome on every boat and we carry children's life jackets, so you do not need to bring your own.</p>
<p>A licensed captain and crew run every charter, which means the adults are guests too. The captain handles the boat and the stops; you handle the sunscreen.</p>

<h2>What a family charter looks like</h2>
<ul>
<li><strong>Calm water:</strong> Biscayne Bay is protected from the open Atlantic by Miami Beach and Key Biscayne, so the ride is smooth.</li>
<li><strong>A swim stop:</strong> Nixon's Sandbar is shallow and clear, the kind of water kids can stand in beside the boat.</li>
<li><strong>Things to see:</strong> The skyline, the mansions of Star Island, the cruise ships at PortMiami and the houses on stilts at Stiltsville on a longer route.</li>
<li><strong>Shade and a place to rest:</strong> The flybridge yachts have shaded seating, and the 48' Isabella, 65' Azimut L'chaim and 90' Deep Blue have a cabin and bathroom below deck.</li>
</ul>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>Timing the day</h2>
<ul>
<li><strong>Morning slots</strong> are calmest on the water and best for younger children.</li>
<li><strong>Afternoon slots</strong> suit teenagers who want the sandbar stop and, on the Isabella, the jet ski.</li>
<li><strong>Late slots</strong> end with the skyline at sunset.</li>
</ul>
<p>Not sure what to pack? The <a href="what-to-bring-yacht-charter-miami.html">what to bring guide</a> covers sunscreen, shoes and the rest.</p>

<h2>Families on our boats</h2>
{{GALLERY}}

<h2>Boats for a family day</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a> or compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>.</p>
""",
    gallery=["isabella_anchored", "isabella_fly", "lchaim_swim", "yamaha_4"],
    table=[("isabella", "Shaded flybridge, cabin below and a jet ski"), ("maxum", "Best-value flybridge yacht"), ("azimut-lchaim", "Three decks, cabins and bathrooms for a big family"), ("yamaha-255xd", "Jet boat for a small family that wants speed"), ("deep-blue", "Salon, cabins and a jacuzzi on deck")],
    faq=[
        ("Are children allowed on the charter?", "Yes. Children are welcome on every boat in the fleet."),
        ("Do you have life jackets for kids?", "Yes. Children's life jackets are on board. Tell us the ages of the children when you book so the crew has the right ones ready."),
        ("Is the water rough?", "Charters run on Biscayne Bay, which is sheltered from the open ocean by Miami Beach and Key Biscayne. The captain picks the route for the day's conditions."),
        ("Is there a bathroom on board?", "The 48' Isabella, 65' Azimut L'chaim, 75' Ferretti and 90' Deep Blue have a bathroom below deck. Ask when you book and we will match the boat to your group."),
        ("How much does a family charter cost?", "From $1,000 for 4 hours with captain and crew included, for the whole boat rather than per person."),
    ],
    cta=("Plan the family's boat day", "Tell us the date and the ages of the kids. Call or WhatsApp and we'll match the boat and hold it today."),
    related=[("sandbar-yacht-charter-miami.html", "Sandbar charter"), ("yacht-charter-before-cruise-miami.html", "Before or after your cruise"), ("birthday-yacht-party-miami.html", "Birthday parties"), ("what-to-bring-yacht-charter-miami.html", "What to bring")],
    service=("Family Yacht Charter Miami", "Private family yacht charters in Miami with children welcome and children's life jackets on board. Licensed captain and crew included. From $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 10. Wedding
PAGES.append(dict(
    slug="wedding-yacht-charter-miami",
    lang="en",
    title="Wedding Yacht Charter Miami | Ceremonies &amp; Receptions",
    desc="Get married on a private yacht in Miami. Ceremonies on board are welcome: the skyline or the open bay as the backdrop, a licensed captain and crew, from $1,000 for 4 hours. Elopements, vow renewals and small weddings.",
    h1="Wedding Yacht Charter in Miami",
    crumb="Weddings",
    lede="Say it on the water. Ceremonies on board are welcome, with the Miami skyline, Star Island or the open bay behind you and a crew to handle everything but the vows. From $1,000 for 4 hours.",
    facts=[("Starting at", "$1,000 / 4 hrs"), ("Ceremonies", "Welcome on board"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["ferretti_table"][0],
    wa="Hi! I'd like to plan a wedding ceremony on a yacht in Miami. Our date:",
    body=f"""
<h2>A wedding with the city as the backdrop</h2>
<p>A yacht wedding in Miami is the small, unforgettable version of the big day: the people who matter most, a deck over Biscayne Bay, and a skyline or sunset instead of a ballroom wall. Ceremonies on board are welcome. Elopements, vow renewals, destination weddings for a small group and the reception cruise after a ceremony on land all work on our boats.</p>
<p>You bring the officiant, the rings and the guests. We bring a private yacht, a licensed captain and crew, and the bay. Every charter is 4 hours, from $1,000 for the whole boat.</p>

<h2>How a yacht wedding runs</h2>
<ul>
<li><strong>Boarding:</strong> Guests meet at our Miami River dock, 10 minutes from Brickell and 15 from Miami Beach. The boat leaves when everyone is aboard.</li>
<li><strong>The ceremony:</strong> On the bow, the aft deck or the flybridge, wherever the couple wants to stand. The captain can hold the boat for a still backdrop or keep cruising slowly.</li>
<li><strong>The celebration:</strong> Cruise the skyline, loop Star Island and Fisher Island, and time the last hour for sunset.</li>
<li><strong>Photos:</strong> Bring your photographer. The boat is the set, and the captain positions it for the shot. See the <a href="yacht-photoshoot-miami.html">photoshoot page</a> for the best light and locations.</li>
</ul>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>Picking the boat</h2>
<ul>
<li><strong>Elopement or vow renewal:</strong> The 48' Isabella or 62' Anvera for a couple and a few witnesses.</li>
<li><strong>Small wedding:</strong> The 65' Azimut L'chaim or 75' Ferretti, with an aft deck table and a flybridge for the ceremony.</li>
<li><strong>The statement:</strong> The 90' Deep Blue, with a jacuzzi on deck, a salon, a formal dining table and cabins below.</li>
</ul>
<p>Just proposing for now? Start with the <a href="proposal-yacht-charter-miami.html">proposal and anniversary page</a>.</p>

<h2>Decks for a ceremony</h2>
{{GALLERY}}

<h2>Yachts for a wedding</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a> or compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>.</p>
""",
    gallery=["ferretti_table", "lchaim_aft", "deepblue_16", "isabella_bow"],
    table=[("deep-blue", "Jacuzzi, salon, dining table and cabins"), ("ferretti", "Flybridge lounge and aft deck dining"), ("azimut-lchaim", "Three decks and a wide bow for the ceremony"), ("anvera", "Open deck for an intimate ceremony"), ("isabella", "Flybridge yacht for an elopement")],
    faq=[
        ("Can we hold the ceremony on the yacht?", "Yes. Ceremonies on board are welcome. You arrange the officiant; we provide the yacht, captain and crew."),
        ("How much does a yacht wedding in Miami cost?", "The boat is priced like any charter: from $1,000 for 4 hours with captain and crew included, up to $4,999 for the 90' Deep Blue."),
        ("How long is the charter?", "Every charter is 4 hours, which is enough for boarding, a ceremony, a skyline cruise and a sunset finish."),
        ("Where does the boat leave from?", "Our dock at 668 NW N River Dr on the Miami River, about 10 minutes from Brickell and 15 from Miami Beach."),
        ("Can we bring a photographer?", "Yes. Photo and video on board are welcome, and the captain will position the boat for the shots you want."),
    ],
    cta=("Set the date on the water", "Sunset slots book months out for weddings. Call or WhatsApp with your date and we'll hold the yacht today."),
    related=[("proposal-yacht-charter-miami.html", "Proposals and anniversaries"), ("yacht-photoshoot-miami.html", "Photoshoots on board"), ("private-sunset-cruise-miami.html", "Private sunset cruise"), ("deep-blue.html", "90' Deep Blue with Jacuzzi")],
    service=("Wedding Yacht Charter Miami", "Private yacht charters for wedding ceremonies, elopements, vow renewals and receptions in Miami. Ceremonies on board welcome. Licensed captain and crew included. From $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 11. Quinceañera
PAGES.append(dict(
    slug="quinceanera-yacht-party-miami",
    lang="en",
    title="Quinceañera Yacht Party Miami | Private from $1,000",
    desc="Celebrate a quinceañera or sweet sixteen on a private yacht in Miami. The whole boat for the family, captain and crew included, a Spanish-speaking team, from $1,000 for 4 hours. Fiesta de quince en yate.",
    h1="Quinceañera Yacht Party in Miami",
    crumb="Quinceañera",
    lede="A quince on the water: the whole yacht for the family, the skyline and the bay for the photos, and a captain and crew who handle the boat. We speak Spanish and English. From $1,000 for 4 hours.",
    facts=[("Starting at", "$1,000 / 4 hrs"), ("Team", "Spanish &amp; English"), ("Booking", "Call or WhatsApp, 24/7")],
    og=P["lchaim_bow"][0],
    wa="Hi! I'd like to plan a quinceañera yacht party in Miami. Our date:",
    body=f"""
<h2>La fiesta de quince, en yate</h2>
<p>Miami families have been celebrating quinceañeras on the water for years, and it is easy to see why: the dress on the bow, the skyline behind the photos, the whole family on one deck and nobody else on board. A private charter gives you the boat for 4 hours with a licensed captain and crew, and a team that plans it with you in Spanish or English.</p>
<p>The same goes for a sweet sixteen or any milestone birthday. From $1,000 for the whole boat, up to the 90' Deep Blue with its jacuzzi at $4,999.</p>

<h2>How the day runs</h2>
<ul>
<li><strong>Boarding and photos:</strong> Family meets at our Miami River dock. The first minutes out run past the Brickell towers, the first photo stop.</li>
<li><strong>The cruise:</strong> Star Island and Fisher Island, then open Biscayne Bay with the skyline across the water.</li>
<li><strong>The party:</strong> Your music on the speakers, cake on the aft deck table and a swim stop at the sandbar if the group wants one.</li>
<li><strong>The sunset:</strong> Book the late slot and the last hour is golden light on the skyline for the final photos.</li>
</ul>
<p>Bringing a photographer or videographer? Photo and video on board are welcome. See the <a href="yacht-photoshoot-miami.html">photoshoot page</a> for the best light.</p>

<h2>How to plan it</h2>
{STEPS_EN}

<h2>Picking the yacht for a quince</h2>
<ul>
<li><strong>65' Azimut L'chaim:</strong> Three decks, an aft deck dining table in the shade and a wide bow sunpad for the dress photos.</li>
<li><strong>75' Ferretti:</strong> A flybridge lounge around a round table and a covered aft deck for the family.</li>
<li><strong>90' Deep Blue:</strong> The superyacht: a jacuzzi on deck, a formal dining table and a salon for the toast.</li>
<li><strong>48' Isabella:</strong> A flybridge with wraparound seating and a jet ski for the cousins.</li>
</ul>

<h2>Celebrations on deck</h2>
{{GALLERY}}

<h2>Yachts for a quinceañera</h2>
{{TABLE}}
<p>Browse the <a href="yacht.html">full 9-yacht fleet</a>, compare every rate on the <a href="miami-yacht-rental-prices.html">price guide</a>, or read the <a href="birthday-yacht-party-miami.html">birthday yacht party page</a>. Prefiere español? Vea <a href="fiesta-en-yate-miami.html">fiestas en yate en Miami</a>.</p>
""",
    gallery=["lchaim_bow", "ferretti_fly", "lchaim_dining", "deepblue_10"],
    table=[("azimut-lchaim", "Three decks and a bow for the photos"), ("ferretti", "Flybridge lounge and covered aft deck"), ("deep-blue", "Jacuzzi, salon and dining table"), ("isabella", "Flybridge yacht with a jet ski"), ("maxum", "Best-value yacht for a smaller family")],
    faq=[
        ("How much does a quinceañera yacht party cost in Miami?", "From $1,000 for 4 hours for the whole boat with captain and crew included. The 65' Azimut L'chaim and 75' Ferretti are $3,000 and the 90' Deep Blue is $4,999 for 4 hours."),
        ("Do you speak Spanish?", "Yes. Our team books and runs charters in Spanish and English. Call or WhatsApp in either language."),
        ("Can we bring a photographer and decorations for the photos?", "Photo and video on board are welcome and the captain positions the boat for the shots. Tell us what you plan to bring when you book and we will confirm what works on the boat you choose."),
        ("Can we play our own music?", "Yes. The charter is private, so the speakers are yours for the 4 hours."),
        ("Are younger cousins and children welcome?", "Yes. Children are welcome and children's life jackets are on board."),
    ],
    cta=("Plan the quince on the water", "Saturday sunset slots go first. Call or WhatsApp, in Spanish or English, and we'll hold the yacht for your date today."),
    related=[("fiesta-en-yate-miami.html", "Fiestas en yate (español)"), ("birthday-yacht-party-miami.html", "Birthday parties"), ("family-yacht-charter-miami.html", "Family charters"), ("yacht-photoshoot-miami.html", "Photoshoots on board")],
    service=("Quinceañera Yacht Party Miami", "Private quinceañera and sweet sixteen yacht parties in Miami with licensed captain and crew included. Spanish-speaking team. From $1,000 for 4 hours.", "1000"),
))

# ---------------------------------------------------------------- 12. Fiesta en yate (ES)
PAGES.append(dict(
    slug="fiesta-en-yate-miami",
    lang="es",
    title="Fiesta en Yate en Miami | Celebraciones desde $1,000",
    desc="Fiesta en yate privado en Miami: cumpleaños, despedidas de soltera y soltero, quinceañeras y celebraciones. El yate completo para su grupo, capitán y tripulación incluidos, atención en español, desde $1,000 por 4 horas.",
    h1="Fiesta en Yate en Miami",
    crumb="Fiesta en yate",
    lede="El yate completo para su grupo: cumpleaños, despedidas de soltera y soltero, quinceañeras o cualquier celebración. Capitán y tripulación incluidos, atención en español, desde $1,000 por 4 horas.",
    facts=[("Desde", "$1,000 / 4 horas"), ("Equipo", "Atención en español"), ("Reservas", "Llamada o WhatsApp, 24/7")],
    og=P["lchaim_crew"][0],
    wa="¡Hola! Quiero organizar una fiesta en yate en Miami. Mi fecha:",
    body=f"""
<h2>Su fiesta, su yate, su gente</h2>
<p>Una fiesta en yate en Miami no tiene que ser un barco con boletos y cien desconocidos. Con nosotros el yate es suyo: su grupo, su música en los altavoces, su ruta por la bahía de Biscayne y un capitán y tripulación con licencia que se ocupan del barco. Usted celebra; nosotros navegamos.</p>
<p>Reservamos y atendemos en español. Todos los paseos son de 4 horas con capitán y tripulación incluidos, desde $1,000 en el Maxum de 46' hasta $4,999 en el Deep Blue de 90' con jacuzzi.</p>

<h2>Celebraciones que organizamos</h2>
<ul>
<li><strong>Cumpleaños:</strong> Pastel en la mesa de popa, el skyline de fondo y una parada para nadar en el sandbar.</li>
<li><strong>Despedidas de soltera y de soltero:</strong> El Isabella de 48' con jet ski incluido es el favorito de los grupos.</li>
<li><strong>Quinceañeras:</strong> El vestido en la proa, la familia en cubierta y la ciudad detrás de las fotos. <a href="quinceanera-yacht-party-miami.html">Más sobre quinceañeras en yate</a>.</li>
<li><strong>Aniversarios y propuestas:</strong> Un paseo al atardecer por el skyline, solo ustedes dos y la tripulación.</li>
<li><strong>Eventos de empresa:</strong> Clientes y equipos en los yates grandes, con mesa en popa y flybridge con vista.</li>
</ul>

<h2>Cómo reservar</h2>
{STEPS_ES}

<h2>Una fiesta en yate, hora por hora</h2>
<ul>
<li><strong>Hora 1:</strong> Embarque en nuestro muelle del río Miami y salida río abajo frente a las torres de Brickell hacia la bahía.</li>
<li><strong>Hora 2:</strong> Star Island, Palm Island y Fisher Island, las islas de las mansiones.</li>
<li><strong>Hora 3:</strong> Ancla en Nixon's Sandbar: agua clara y poco profunda para nadar junto al barco. En el Isabella sale el jet ski.</li>
<li><strong>Hora 4:</strong> Regreso con el skyline de frente. Reserve el turno de la tarde y la última hora es el atardecer.</li>
</ul>

<h2>Fiestas en nuestros yates</h2>
{{GALLERY}}

<h2>Yates para una fiesta</h2>
{{TABLE}}
<p>Vea la <a href="yacht.html">flota completa de 9 yates</a>, compare precios en la <a href="miami-yacht-rental-prices.html">guía de precios</a> o lea sobre el <a href="alquiler-de-yates-miami.html">alquiler de yates en Miami</a> en español.</p>
""",
    gallery=["lchaim_crew", "isabella_jetski", "lchaim_dining", "deepblue_aft"],
    table=[("isabella", "Jet ski incluido para la parada en el sandbar"), ("azimut-lchaim", "Tres cubiertas para el grupo grande"), ("ferretti", "Flybridge con mesa redonda y popa techada"), ("deep-blue", "Jacuzzi en cubierta, salón y comedor"), ("maxum", "El yate de mejor precio para empezar")],
    faq=[
        ("¿Cuánto cuesta una fiesta en yate en Miami?", "Desde $1,000 por 4 horas por el yate completo, con capitán y tripulación incluidos. El Isabella de 48' con jet ski cuesta $1,499, el Azimut L'chaim de 65' $3,000 y el Deep Blue de 90' con jacuzzi $4,999, siempre por 4 horas."),
        ("¿Atienden en español?", "Sí. Reservamos y atendemos en español y en inglés, por llamada o WhatsApp, las 24 horas."),
        ("¿Podemos llevar nuestra música?", "Sí. El paseo es privado, así que los altavoces son suyos durante las 4 horas."),
        ("¿Desde dónde sale el yate?", "Desde nuestro muelle en 668 NW N River Dr, en el río Miami, a unos 10 minutos de Brickell y 15 de Miami Beach."),
        ("¿Necesitamos licencia o experiencia?", "No. Todos los paseos incluyen capitán y tripulación con licencia."),
    ],
    cta=("Reserve la fecha de su fiesta", "Los sábados y los atardeceres se llenan primero. Llame o escriba por WhatsApp y apartamos el yate para su fecha hoy."),
    related=[("alquiler-de-yates-miami.html", "Alquiler de yates en Miami"), ("quinceanera-yacht-party-miami.html", "Quinceañeras en yate"), ("yacht-party-miami.html", "Yacht parties (English)"), ("miami-yacht-rental-prices.html", "Precios")],
    service=("Fiesta en Yate en Miami", "Fiestas privadas en yate en Miami: cumpleaños, despedidas de soltera y soltero, quinceañeras y celebraciones. Capitán y tripulación incluidos, atención en español. Desde $1,000 por 4 horas.", "1000"),
    hreflang_group="party",
))

# ---------------------------------------------------------------- 13. Aluguel de iate (PT-BR)
PAGES.append(dict(
    slug="aluguel-de-iate-em-miami",
    lang="pt-BR",
    title="Aluguel de Iate em Miami desde $1,000 | Capitão Incluso",
    desc="Aluguel de iate e lancha em Miami com capitão e tripulação inclusos. Frota de 9 embarcações de 25 a 90 pés, passeios privativos de 4 horas pela Biscayne Bay, Star Island e o skyline, a partir de $1,000. Atendimento em inglês e espanhol.",
    h1="Aluguel de Iate em Miami",
    crumb="Aluguel de iate",
    lede="Iates e lanchas privativas em Miami com capitão e tripulação inclusos, a partir de $1,000 por 4 horas. Saída do Miami River, a 10 minutos de Brickell e 15 de Miami Beach.",
    facts=[("A partir de", "$1,000 / 4 horas"), ("Frota", "9 embarcações, 25 a 90 pés"), ("Reservas", "Ligação ou WhatsApp, 24 horas")],
    og=P["lchaim_fisher"][0],
    wa="Olá! Quero alugar um iate em Miami. / Hi! I'd like to rent a yacht in Miami. Date:",
    body=f"""
<h2>O passeio de iate em Miami, do jeito certo</h2>
<p>Alugar um iate em Miami é o programa que transforma a viagem: a Biscayne Bay, as mansões de Star Island, o skyline de Brickell e uma parada para nadar na água clara do sandbar, tudo em um passeio privativo de 4 horas. Nenhum passeio é compartilhado: o barco é do seu grupo, com capitão e tripulação licenciados inclusos no preço.</p>
<p>A frota tem 9 embarcações, de uma lancha a jato Yamaha de 25 pés até o Deep Blue de 90 pés com jacuzzi no convés. O preço vai de $1,000 a $4,999 por 4 horas, sem plataforma e sem comissão de intermediário. A equipe atende em inglês e espanhol pelo WhatsApp e por telefone.</p>

<h2>Para onde o passeio vai</h2>
<ul>
<li><strong>Star Island, Palm Island e Hibiscus Island:</strong> As ilhas das mansões de celebridades, vistas da água.</li>
<li><strong>Fisher Island:</strong> A ilha privativa na entrada do canal de Government Cut.</li>
<li><strong>Nixon's Sandbar:</strong> Um banco de areia raso de água transparente em frente a Key Biscayne, a parada para nadar.</li>
<li><strong>Stiltsville:</strong> Casas sobre palafitas no limite da baía, dentro do Biscayne National Park.</li>
<li><strong>O skyline:</strong> Downtown e Brickell vistos da baía, melhor ainda no pôr do sol.</li>
</ul>

<h2>Como reservar</h2>
{STEPS_PT}

<h2>Ocasiões</h2>
<ul>
<li><strong>Aniversários e festas:</strong> O iate inteiro para o grupo, com a sua música nas caixas de som.</li>
<li><strong>Despedidas de solteira e de solteiro:</strong> O Isabella de 48 pés vem com jet ski incluso.</li>
<li><strong>Pôr do sol a dois:</strong> Reserve o horário da tarde e a última hora é o skyline dourado.</li>
<li><strong>Família:</strong> Crianças são bem-vindas e há coletes salva-vidas infantis a bordo.</li>
<li><strong>Antes ou depois do cruzeiro:</strong> O píer fica a poucos minutos do Port of Miami e dos hotéis do centro.</li>
</ul>

<h2>Nossos iates</h2>
{{GALLERY}}

<h2>Preços por embarcação</h2>
{{TABLE}}
<p>Veja a <a href="yacht.html">frota completa</a> e a <a href="miami-yacht-rental-prices.html">tabela de preços</a> (em inglês). Prefere espanhol? Veja <a href="alquiler-de-yates-miami.html">alquiler de yates en Miami</a>.</p>
""",
    gallery=["lchaim_fisher", "isabella_jetski", "deepblue_aft", "anvera_skyline"],
    table=[("deep-blue", "Superiate com jacuzzi no convés"), ("ferretti", "Flybridge com lounge e mesa na popa"), ("azimut-lchaim", "Três conveses para grupos grandes"), ("anvera", "Convés aberto, design italiano"), ("azimut", "Flybridge com teto rígido"), ("isabella", "Flybridge e jet ski incluso"), ("maxum", "O iate de melhor custo-benefício"), ("axopar-brabus", "Lancha esportiva edição Brabus"), ("yamaha-255xd", "Lancha a jato para grupos pequenos")],
    faq=[
        ("Quanto custa alugar um iate em Miami?", "A partir de $1,000 por 4 horas com capitão e tripulação inclusos. O Isabella de 48 pés com jet ski custa $1,499, o Azimut L'chaim de 65 pés $3,000 e o Deep Blue de 90 pés com jacuzzi $4,999, sempre por 4 horas."),
        ("Vocês falam português?", "A equipe atende em inglês e espanhol. Pode escrever no WhatsApp em português que respondemos em inglês ou espanhol."),
        ("Precisa de habilitação náutica?", "Não. Todos os passeios incluem capitão e tripulação licenciados."),
        ("De onde sai o iate?", "Do nosso píer em 668 NW N River Dr, no Miami River, a cerca de 10 minutos de Brickell e 15 de Miami Beach."),
        ("O passeio pode ser de 2 horas?", "Não. Todos os passeios são de 4 horas, o tempo de ver as ilhas, o skyline e ainda parar para nadar."),
    ],
    cta=("Reserve o seu passeio em Miami", "Fins de semana e horários de pôr do sol são os primeiros a acabar. Ligue ou mande WhatsApp e seguramos o iate para a sua data hoje."),
    related=[("alquiler-de-yates-miami.html", "En español"), ("index.html", "In English"), ("star-island-boat-tour-miami.html", "Star Island boat tour"), ("miami-yacht-rental-prices.html", "Preços (English)")],
    service=("Aluguel de Iate em Miami", "Aluguel de iates e lanchas privativas em Miami com capitão e tripulação inclusos. Frota de 9 embarcações. A partir de $1,000 por 4 horas.", "1000"),
    hreflang_group="home",
))
