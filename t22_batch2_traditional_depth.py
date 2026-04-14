"""
T22 Batch 2: Traditional region depth — second products for 7 single-product traditional regions
Targets: Cameroon Matango (75), Fiji Yaqona (69), Morocco (183),
         Nigeria Palm Wine (74), Samoa Ava (71), Turkey (184), Hawaii Awa (70)
"""
import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(WRITE_DSN)
conn.autocommit = True
cur = conn.cursor()

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS producer: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country,
           production_philosophy, philosophy_description,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Producer [{pid}]: {name}")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS product: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, subcategory, producer_id, region_id, origin_country,
           description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, subcategory, producer_id, region_id, origin_country,
          description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Product [{pid}]: {name}")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence,
           meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T22 BATCH 2: TRADITIONAL REGION DEPTH (7 REGIONS) ===\n")

# ── CAMEROON — MATANGO (75) — Yaoundé Matango Producers ──
print("── CAMEROON — MATANGO — Yaoundé Producers ──")
pid = P(
    name="Yaoundé Traditional Matango Collective",
    producer_type="kombucha_brewery",
    region_id=75,
    country="Cameroon",
    production_philosophy="Forest kiosk tradition — Cameroon's fermented palm wine culture in the centre-south",
    philosophy_description=(
        "The Yaoundé Traditional Matango Collective represents the network of small-scale "
        "matango producers serving the kiosk culture around Cameroon's capital region and the "
        "Centre and South provinces. Matango is the generic Cameroonian term for fermented "
        "palm wine, produced from the sap of various palm species — primarily the raffia palm "
        "and oil palm — tapped daily and fermented naturally by indigenous yeasts. The Collective "
        "organises traditional producers around sustainable tapping practices, hygiene standards, "
        "and fair pricing, while preserving the spontaneous fermentation character that gives "
        "authentic Cameroonian matango its complex, yeasty profile."
    ),
    reputation_narrative=(
        "Cameroonian matango represents an ancient African fermented beverage tradition shared "
        "across the forest zone of Central and West Africa, with Cameroon's Centre-South region "
        "particularly noted for its active matango kiosk culture and diverse palm species."
    ),
    price_positioning="entry",
    authority_tier=2
)
prod = PROD(
    name="Cameroonian Matango — Oil Palm Fresh-Tapped Emu",
    category="traditional_cultural",
    producer_id=pid,
    region_id=75,
    origin_country="Cameroon",
    subcategory="Matango",
    description=(
        "Fresh-tapped oil palm wine (matango) from the Centre-South region of Cameroon, "
        "produced daily from the fermented sap of the Elaeis guineensis (African oil palm) "
        "tree. Unlike raffia palm matango (used for the Bafoussam variety), oil palm matango "
        "is lighter in colour and more delicate in flavour, with a frothy, mildly alcoholic "
        "character similar to freshly fermented apple juice. The sap is collected at dawn "
        "by skilled palm tappers who make incisions in the palm flower stalk, allowing the "
        "sap to ferment spontaneously in collection gourds. At its freshest, matango is "
        "subtly sweet and effervescent; by afternoon, it has developed noticeable acidity "
        "and alcoholic strength."
    ),
    price_tier="entry"
)
PAIR(prod,
     "Ndolé (Cameroonian bitterleaf stew with groundnuts and smoked fish)",
     "complement", "classic", "main",
     "Matango's light sweetness and fermented freshness balance ndolé's bitter-rich complexity")
PAIR(prod,
     "Soya (grilled spiced beef skewers) with suya pepper and sliced onion",
     "cleanse", "established", "casual",
     "Effervescent palm wine refreshes the palate between spiced soya bites")

# ── FIJI — YAQONA (69) — Taki Mai second expression ──
print("\n── FIJI — YAQONA — Wakaya Kava ──")
pid = P(
    name="Wakaya Perfection Kava — Fiji",
    producer_type="kombucha_brewery",
    region_id=69,
    country="Fiji",
    production_philosophy="Wakaya Island premium kava — Fiji's most exclusive terroir for noble yaqona",
    philosophy_description=(
        "Wakaya Perfection sources kava (yaqona) from the private island of Wakaya in Fiji's "
        "Koro Sea, where a single private resort estate farms noble kava root using traditional "
        "Fijian methods in volcanic island soils free from chemical inputs. Wakaya Island's "
        "isolation and unique volcanic terroir produce kava root of exceptional purity and "
        "potency, with the island's microclimate creating ideal growing conditions for the "
        "slow-maturing noble kava cultivars that produce the most psychoactive and smooth "
        "preparation. The island's kava is hand-selected and sun-dried before preparation, "
        "preserving the kavalactone content that gives yaqona its distinctive effects."
    ),
    reputation_narrative=(
        "Wakaya Perfection represents the premium end of Fijian kava, demonstrating that "
        "terroir matters for yaqona as much as it does for wine — with the island's isolation, "
        "volcanic soils, and careful farming producing an exceptional kava experience."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Wakaya Perfection Fijian Noble Kava — Waka",
    category="traditional_cultural",
    producer_id=pid,
    region_id=69,
    origin_country="Fiji",
    subcategory="Yaqona",
    description=(
        "Noble kava (yaqona) from Wakaya Island in the Koro Sea, Fiji, produced from the "
        "lateral roots (waka) of mature Piper methysticum plants cultivated for 5–7 years "
        "before harvest. Waka root produces the finest kava preparations, with higher "
        "kavalactone content and a smoother, less astringent character than above-ground "
        "stem preparations (lewena). Wakaya Island's volcanic soils and isolation from "
        "chemical agriculture produce an exceptionally pure and potent kava. "
        "Traditional Fijian ceremony involves grinding the root, straining through cloth, "
        "and serving in a communal tanoa bowl, consumed in a social ceremony of respect "
        "and connection."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Kokoda (Fijian raw fish coconut salad) with lime and chilli",
     "complement", "classic", "starter",
     "Yaqona's earthy numbness and mild sedative character create calm anticipation before kokoda")
PAIR(prod,
     "Lovo-cooked taro with coconut cream and freshly caught reef fish",
     "complement", "established", "main",
     "Traditional Fijian feast foods served with yaqona — the cultural context of ceremony and welcome")

# ── MOROCCO (183) — Moroccan Mint Tea (second expression) ──
print("\n── MOROCCO — Hamid's Authentic Moroccan Tea ──")
pid = P(
    name="Hamid's Authentic Moroccan Tea — Medina Marrakech",
    producer_type="tea_garden",
    region_id=183,
    country="Morocco",
    production_philosophy="Marrakech medina tea tradition — the art of Moroccan hospitality in a glass",
    philosophy_description=(
        "Hamid's Authentic Moroccan Tea represents the medina tea house tradition of Marrakech, "
        "where expert tea masters (muallims) have been blending and pouring the perfect atay "
        "for generations. The medina tea tradition emphasises the theatrical pour from height — "
        "aerating the tea to create froth — and the precise balance of gunpowder green tea, "
        "fresh nana mint (spearmint), and generous quantities of rock sugar cane. The tea house "
        "culture of Morocco's imperial cities is a fundamental expression of Moroccan "
        "hospitality (diyafa) and social culture, where declining tea is considered impolite "
        "and accepting it opens conversation and commerce."
    ),
    reputation_narrative=(
        "The Moroccan tea house tradition represents one of the world's great beverage ceremonies, "
        "with the atay culture of the imperial cities (Marrakech, Fez, Meknès, Rabat) refined "
        "over centuries to a form of social art requiring years of practice to master."
    ),
    price_positioning="entry",
    authority_tier=2
)
prod = PROD(
    name="Moroccan Atay with Rose Petals and Orange Blossom",
    category="tea",
    producer_id=pid,
    region_id=183,
    origin_country="Morocco",
    subcategory="Moroccan Mint Tea",
    description=(
        "Moroccan atay (mint tea) prepared in the imperial style with gunpowder green tea, "
        "fresh nana mint, rose petals, and orange blossom water — a festive variation served "
        "for special occasions and honoured guests. The rose petals and orange blossom add "
        "fragrant floral complexity to the classic mint-sugar-green tea base, creating a "
        "more perfumed expression suited to dessert service or celebratory occasions. "
        "Served in small ornate Moroccan tea glasses with a theatrical high pour from a "
        "traditional Moroccan teapot (barrad). The combination of green tea's slight bitterness, "
        "mint's freshness, rose's fragrance, and sugar's sweetness creates a beverage of "
        "extraordinary complexity and cultural depth."
    ),
    price_tier="entry"
)
PAIR(prod,
     "Bastilla au pigeon with cinnamon, almonds, and powdered sugar",
     "complement", "classic", "main",
     "Moroccan feast drink meets Moroccan feast dish — atay's mint freshness lifts bastilla's richness")
PAIR(prod,
     "Moroccan almond pastilla (M'hanncha) with honey and cinnamon",
     "complement", "established", "dessert",
     "Rose-orange atay and almond pastry create the classic Moroccan dessert pairing of great elegance")

# ── NIGERIA — PALM WINE BELT (74) — Igbo Palm Wine ──
print("\n── NIGERIA — PALM WINE — Igbo Raphia Tradition ──")
pid = P(
    name="Igbo Raphia Palm Wine Tappers — Enugu State",
    producer_type="kombucha_brewery",
    region_id=74,
    country="Nigeria",
    production_philosophy="Enugu State raphia tradition — South-Eastern Nigeria's white palm wine culture",
    philosophy_description=(
        "The Igbo Raphia Palm Wine Tappers of Enugu State represent the South-Eastern Nigerian "
        "tradition of raphia palm (Raphia hookeri) wine tapping, which produces a distinctive "
        "white, milky palm wine quite different from the oil palm variety tapped in coastal regions. "
        "Raphia palm wine is traditionally central to Igbo social and ceremonial life — used in "
        "wedding ceremonies, funeral rites, new yam festivals (Iri Ji), and daily social bonding. "
        "The tappers, known as ogidi, maintain family traditions of responsible tapping that "
        "balance harvest with palm health over generations."
    ),
    reputation_narrative=(
        "Igbo palm wine culture represents one of Nigeria's most sophisticated and ceremonially "
        "embedded fermented beverage traditions, with raphia palm wine's distinctive character "
        "— white, mildly sour, highly effervescent — central to South-Eastern cultural identity."
    ),
    price_positioning="entry",
    authority_tier=2
)
prod = PROD(
    name="Enugu State Raphia Palm Wine — White Emu (Fresh)",
    category="traditional_cultural",
    producer_id=pid,
    region_id=74,
    origin_country="Nigeria",
    subcategory="Palm Wine",
    description=(
        "Fresh raphia palm wine (emu) from Enugu State in South-Eastern Nigeria, tapped from "
        "the cut flower stalk of the raphia palm (Raphia hookeri) and collected in traditional "
        "gourds. Raphia palm wine differs significantly from oil palm wine — it is milky-white "
        "in appearance due to suspended yeast, highly effervescent, mildly sweet when very fresh "
        "(morning tapping), and progressively more sour and alcoholic as the day progresses. "
        "By evening, it has developed noticeable sourness and higher alcohol. Traditionally "
        "consumed from shared calabash cups in social settings, ceremonies, and festivals. "
        "Central to Igbo hospitality customs and spiritual ceremonies."
    ),
    price_tier="entry"
)
PAIR(prod,
     "Ofe onugbu (bitter leaf soup) with stockfish, palm oil, and ede (cocoyam)",
     "complement", "classic", "main",
     "Raphia palm wine's effervescent freshness and mild sweetness balance bitter leaf's intensity")
PAIR(prod,
     "Suya (grilled spiced beef) with sliced tomato, onion, and suya pepper",
     "cleanse", "established", "casual",
     "Fresh palm wine's effervescence and mild sweetness cool and refresh between spiced suya bites")

# ── SAMOA — AVA (71) — Samoan Cultural Trust ──
print("\n── SAMOA — AVA — Taumafai Ava Ceremony ──")
pid = P(
    name="Samoa Ava Fono — Traditional Ceremony Council",
    producer_type="kombucha_brewery",
    region_id=71,
    country="Samoa",
    production_philosophy="Samoan ava protocol — the most sacred beverage ceremony in Polynesia",
    philosophy_description=(
        "The Samoa Ava Fono represents the traditional council governance structure through "
        "which ava (kava) ceremonies are conducted in Samoan villages and government institutions. "
        "Unlike casual kava consumption elsewhere in the Pacific, Samoan ava is a highly ritualised "
        "ceremony with strict protocols governing who prepares, serves, and receives ava — always "
        "in order of rank (matai, chiefs). The ceremony opens all important social occasions "
        "including meetings of the fono (village council), state ceremonies, welcoming of chiefs, "
        "and significant family events. The Samoa Ava Fono preserves these protocols as living "
        "constitutional practices."
    ),
    reputation_narrative=(
        "Samoan ava ceremony represents one of the Pacific's most formally elaborate and "
        "socially significant beverage traditions, embedded in the fa'a Samoa (the Samoan way) "
        "and inseparable from questions of political authority and social order."
    ),
    price_positioning="entry",
    authority_tier=2
)
prod = PROD(
    name="Samoan Ava — Taumafai Ceremony Grade Kava",
    category="traditional_cultural",
    producer_id=pid,
    region_id=71,
    origin_country="Samoa",
    subcategory="Ava",
    description=(
        "Taumafai (high-ceremony) grade ava from Samoa, prepared from dried and powdered "
        "roots of Piper methysticum selected for potency and purity. The taumafai grade "
        "represents the finest preparation for formal ceremonies — chiefly investitures, "
        "state occasions, and diplomatic receptions. The root is traditionally ground by "
        "a taufa'alele (specially appointed young women) in a specific ceremonial manner, "
        "then strained through hibiscus bark into a communal tanoa (wooden bowl). The "
        "ceremony includes formal oratory, presentation of the tanoa, and serving in strict "
        "order of rank. The ava itself is earthy, mildly bitter, and numbing, with a calming, "
        "mildly euphoric effect that encourages measured, respectful conversation."
    ),
    price_tier="entry"
)
PAIR(prod,
     "Palusami (taro leaves baked in coconut cream) with breadfruit",
     "complement", "classic", "main",
     "Ava ceremony opens traditional feast — palusami's rich coconut cream follows ava's earthiness")
PAIR(prod,
     "Oka (Samoan raw fish in coconut cream, lime, and chilli)",
     "complement", "established", "starter",
     "Ava's calming prelude followed by Samoa's national dish — the archetypal fa'a Samoa sequence")

# ── TURKEY (184) — Turkish Tea (çay) ──
print("\n── TURKEY — Turkish Çay — Rize Tea Region ──")
pid = P(
    name="Rize Çay — Eastern Black Sea Tea Producers",
    producer_type="tea_garden",
    region_id=184,
    country="Turkey",
    production_philosophy="Rize's Black Sea tea heritage — Turkey's national drink from the eastern mountains",
    philosophy_description=(
        "Turkish çay (tea) is produced almost exclusively in the Rize Province on Turkey's "
        "eastern Black Sea coast, where the region's high rainfall, acidic soils, and mild "
        "climate create ideal conditions for Camellia sinensis cultivation. Turkey is one of "
        "the world's largest tea consumers per capita, and the Rize tradition of double "
        "samovar brewing — a concentrated decoction diluted to personal taste — is one "
        "of the world's most distinctive tea preparation methods. The Rize çay producers "
        "maintain a distinct Ottoman-era tea garden culture that is inseparable from "
        "Turkish social life, commerce, and hospitality."
    ),
    reputation_narrative=(
        "Rize tea is Turkey's national beverage and cultural touchstone, with the Rize Province "
        "producing virtually all of Turkey's domestic tea. The Turkish tea glass (ince belli — "
        "thin-waisted) and double-samovar service are globally recognised symbols of Turkish culture."
    ),
    price_positioning="entry",
    authority_tier=2
)
prod = PROD(
    name="Rize Turkish Çay — Black Sea Estate Orthodox Tea",
    category="tea",
    producer_id=pid,
    region_id=184,
    origin_country="Turkey",
    subcategory="Turkish Black Tea",
    description=(
        "Orthodox black tea from Rize Province on Turkey's eastern Black Sea coast, produced "
        "from Camellia sinensis grown in the region's characteristic terraced mountain gardens "
        "above the Black Sea. Turkish çay is processed as a fully oxidised black tea and "
        "brewed in the traditional double-samovar method: a concentrated decoction in the "
        "upper pot is diluted to taste from the lower pot of hot water, allowing each drinker "
        "to customise strength. Served in the iconic ince belli (thin-waisted) tulip glass "
        "without milk but with sugar cubes on the side. Strong, dark, and slightly tannic, "
        "Turkish çay is served continuously throughout the day in tea houses (çay evleri), "
        "bazaars, and homes as the cornerstone of Turkish hospitality."
    ),
    price_tier="entry"
)
PAIR(prod,
     "Simit (sesame bread ring) with white cheese, olives, and tomato",
     "complement", "classic", "any",
     "The Turkish breakfast cornerstone — çay with simit and white cheese is national daily ritual")
PAIR(prod,
     "Baklava with pistachio, honey, and clotted cream",
     "contrast", "classic", "dessert",
     "Turkish çay's tannin and bitterness cut through baklava's intense honey-nut sweetness")

# ── HAWAII — AWA (70) — Hana Hou Kava ──
print("\n── HAWAII — AWA — Hana Hou Kava ──")
pid = P(
    name="Hana Hou Kava — Maui",
    producer_type="kombucha_brewery",
    region_id=70,
    country="USA",
    production_philosophy="Hawaiian awa revival — traditional Polynesian kava in sacred Hawaiian form",
    philosophy_description=(
        "Hana Hou Kava on the island of Maui represents the contemporary revival of Hawaiian "
        "awa (kava) cultivation and traditional preparation practices. Hawaiian awa is one of "
        "the most potent and historically significant kava cultivars in Polynesia, brought to "
        "the Hawaiian Islands by the original Polynesian voyagers and cultivated for over "
        "1,000 years before significant decline in the colonial period. The revival brings "
        "Hawaiian awa back to traditional kapu (taboo) ceremonial contexts, traditional "
        "cultivation methods, and the Hawaiian concept of awa as a bridge between the physical "
        "and spiritual worlds."
    ),
    reputation_narrative=(
        "The Hawaiian awa revival is both a cultural restoration project and a contribution "
        "to global kava diversity, preserving some of the world's rarest and most potent "
        "kava cultivars while reconnecting Hawaiian communities with their Polynesian heritage."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Hana Hou Hawaiian Awa — Hiwa Cultivar Traditional Preparation",
    category="traditional_cultural",
    producer_id=pid,
    region_id=70,
    origin_country="USA",
    subcategory="Hawaiian Awa",
    description=(
        "Hawaiian awa from the Hiwa (black) cultivar, one of the most historically significant "
        "and potent Hawaiian kava varieties, prepared in the traditional Hawaiian manner using "
        "fresh root ground in water and strained through bark cloth (olonā). The Hiwa cultivar "
        "is among the rarest Hawaiian awa varieties, associated with ceremonial use and "
        "historically reserved for ali'i (chiefs) and kahuna (priests) due to its potency. "
        "The fresh-root preparation method produces a greener, more aromatic and powerful "
        "awa than the dried-root methods used elsewhere in the Pacific. Hana Hou's cultivation "
        "on Maui uses traditional agricultural methods that honour the plant's sacred status "
        "in Hawaiian culture."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Lomi lomi salmon with sweet Maui onion and tomato",
     "complement", "classic", "starter",
     "Hawaiian awa ceremony preceding traditional Hawaiian feast — lomi salmon's freshness follows")
PAIR(prod,
     "Poi (fermented taro paste) with kalua pork from the imu",
     "complement", "established", "main",
     "Traditional Hawaiian lu'au — awa, poi, and kalua pig are the elemental components of feast")

print("\n✅ T22 Batch 2 complete — all traditional regions now have 2+ products.")
print("  Cameroon Matango (75): +1 producer, +1 product, +2 pairings")
print("  Fiji Yaqona (69): +1 producer, +1 product, +2 pairings")
print("  Morocco (183): +1 producer, +1 product (tea), +2 pairings")
print("  Nigeria Palm Wine (74): +1 producer, +1 product, +2 pairings")
print("  Samoa Ava (71): +1 producer, +1 product, +2 pairings")
print("  Turkey (184): +1 producer, +1 product (tea/çay), +2 pairings")
print("  Hawaii Awa (70): +1 producer, +1 product, +2 pairings")

cur.close()
conn.close()
