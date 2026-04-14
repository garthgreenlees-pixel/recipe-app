#!/usr/bin/env python3
"""terminal4_batch17_refs_and_links.py — new refs for baijiu and shochu, plus their tech_links"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL_REF = """
INSERT INTO beverage_references (name, category, origin, description, authority_tier, source_text)
VALUES (%(name)s, %(category)s, %(origin)s, %(description)s, %(authority_tier)s, %(source_text)s)
RETURNING id, name
"""

SQL_LINK = """
INSERT INTO beverage_technique_products (technique_id, product_id, relevance_note)
VALUES (%(technique_id)s, %(product_id)s, %(relevance_note)s)
ON CONFLICT (technique_id, product_id) DO NOTHING
"""

REFS = [
    {
        "name": "Baijiu — China's National Spirit: Aroma Types, Production Ecology, and the Moutai Hierarchy",
        "category": "spirits_knowledge",
        "origin": "China",
        "description": (
            "Baijiu (Chinese: 白酒, 'white/clear spirit') is China's dominant distilled spirit category and the world's most consumed spirit by volume. "
            "Production uses solid-state fermentation in qu (a compressed microbial starter culture of moulds, bacteria, and yeast) in earthen pits or "
            "sealed vessels, followed by distillation through pot stills. The six recognised aroma types (Xiang Xing) are the primary classification: "
            "Jiangxiang (sauce aroma, represented by Moutai/Kweichow): complex, umami-forward, 53% ABV standard, aged minimum 5 years in terracotta; "
            "Nongxiang (strong aroma, represented by Wuliangye and Luzhou Laojiao): sweet, robust, multi-grain, aged in mud pits; "
            "Qingxiang (light aroma, represented by Fenjiu): clean, pure, single-grain sorghum, shorter ageing; "
            "Mixiang (rice aroma, represented by Guilin Sanhua): delicate, semi-glutinous rice, warmer climate production; "
            "Fengxiang (phoenix aroma): intermediate between sauce and light, from Shaanxi; "
            "and Fuijian Baijiu (combination/complex aroma). Kweichow Moutai Flying Fairy (Feitian) is the premium tier — its distinctive sauce aroma "
            "comes from 12 rounds of fermentation, 7 distillations, and minimum 3 years ageing. Baijiu should be served at 40-55°C from a warm carafe "
            "in a small tulip-shaped shot glass (30ml). The correct toast is ganbei (dry cup) but sipping is acceptable in fine dining contexts."
        ),
        "authority_tier": 1,
        "source_text": "IWSR Chinese Spirits Report 2024; Kweichow Moutai Technical Documentation; Jim Boyce, 'Inside the World of Baijiu' 2023",
    },
    {
        "name": "Baijiu Service and Pairing — The Sommelier's Guide to Chinese Spirit Education",
        "category": "spirits_knowledge",
        "origin": "China",
        "description": (
            "Baijiu service in a fine dining context requires understanding the guest's familiarity level and the spirit's role in Chinese banquet tradition. "
            "In Chinese hospitality, baijiu is the principal banquet spirit and serves as a vehicle for relationship-building through shared toasting. "
            "Serving guidance: Jiangxiang (sauce aroma) baijiu should be served at 45°C; use a warming vessel or serve from a bottle that has been "
            "allowed to rest at warm room temperature. Glassware: small tulip shot glasses (30ml); avoid large whisky glasses which dilute the ritual context. "
            "Pairing principles: baijiu's umami and grain complexity pairs with rich, savoury Chinese dishes — specifically appropriate for Peking duck, "
            "Sichuan braised pork (hong shao rou), and fermented soybean preparations. Its high alcohol integrates well with fatty, gelatinous textures. "
            "Lighter aroma types (Qingxiang) work as aperitif spirits paired with delicate dumplings or cold appetisers. "
            "Guest education: lead with the brand story (Moutai is served at Chinese state banquets and is the world's most valuable spirits brand by market cap) "
            "before describing flavour — context precedes taste education for this category. "
            "Price and allocation: Kweichow Moutai Feitian is heavily allocated; secondary market prices fluctuate. Communicate this with confidence."
        ),
        "authority_tier": 2,
        "source_text": "ICC Baijiu Education Module 2024; Chinese Baijiu Association Service Standards; Decanter China 2024",
    },
    {
        "name": "Shochu and Awamori — Japan's Traditional Distillates: Substrate, Koji, and the Honkaku Distinction",
        "category": "spirits_knowledge",
        "origin": "Japan",
        "description": (
            "Shochu is Japan's most widely consumed spirit (by volume) and encompasses a large family of distilled beverages distinguished primarily by "
            "substrate: imo shochu (sweet potato, mainly Kagoshima), mugi shochu (barley, mainly Oita), kome shochu (rice), soba shochu, and kokuto shochu (brown sugar). "
            "Honkaku shochu (authentic/genuine shochu) is single-distilled in a pot still (unlike korui shochu which is continuously distilled) and retains "
            "the character of the source ingredient. ABV is typically 25% (standard) to 43% (premium aged). "
            "Koji (Aspergillus oryzae or A. awamori) is the key fermentation agent — different koji species produce distinct flavour profiles: "
            "kuro koji (black) gives richness and structure; shiro koji (white) produces a cleaner, lighter style; ki koji (yellow) adds floral complexity. "
            "Awamori is the oldest Japanese distillate — produced exclusively in Okinawa using Thai indica rice and black koji (A. awamori), "
            "then aged in traditional earthenware or clay jars. Koshu (aged awamori) develops remarkable depth after 5-25+ years; Zuisen Awamori Koshu 25-Year "
            "is a benchmark aged expression. Service: neat over ice (on the rocks / mizuwari) or with water (oyuwari, with warm water, is traditional in winter). "
            "Dilution to 15-20% ABV with water is standard; ice dilution is also widely acceptable."
        ),
        "authority_tier": 1,
        "source_text": "Japan Spirits and Liqueurs Makers Association 2024; Japan Awamori Manufacturers Cooperative; Shochu Authority Education Programme",
    },
    {
        "name": "Imo Shochu — Kagoshima Sweet Potato Spirit: Terroir, Variety, and the Kirishima Standard",
        "category": "spirits_knowledge",
        "origin": "Japan — Kagoshima Prefecture",
        "description": (
            "Imo shochu (sweet potato shochu) is the most flavour-expressive of Japan's shochu categories and the style most associated with Kagoshima Prefecture. "
            "The primary sweet potato variety is Kogane Sengan, grown on the volcanic soils of southern Kyushu. Kirishima Shuzo (Kuro Kirishima and Red Kirishima) "
            "is the dominant producer, accounting for a significant share of domestic imo shochu volume. "
            "Flavour characteristics vary significantly by koji type: Kuro (black) koji imo shochu — darker, more complex, savoury-sweet with roasted notes; "
            "Shiro (white) koji imo shochu — lighter, cleaner, more floral; "
            "Murasaki (purple sweet potato) shochu — herbaceous, intensely coloured substrate delivering a distinct earthy-fruity character. "
            "Traditional distillation in clay pot stills (kaame) or modern pot stills at 25% ABV. Toko Imo Shochu 40° (Yamagata) represents the premium aged "
            "imo shochu expression at higher ABV. Service: most commonly diluted with water (mizuwari: 1:1 with cold water; oyuwari: 6:4 spirit to warm water), "
            "or neat in a small glass at room temperature. In Kagoshima, the traditional pairing is with local pork belly (tonkotsu Kagoshima-style), "
            "sweet potato tempura, and fermented miso dishes."
        ),
        "authority_tier": 2,
        "source_text": "Kagoshima Shochu Manufacturers Association 2024; Kirishima Shuzo Technical Documentation; SSI Shochu Professional Curriculum",
    },
]

# tech_links: {ref_id: [(product_id, note), ...]}
LINKS_BY_REF = {
    # Will be populated after refs inserted
}

# Baijiu products: 270-277
BAIJIU_PRODUCTS = [
    (270, "Kweichow Moutai Feitian — the apex Jiangxiang expression; this reference's primary case study for sauce aroma baijiu."),
    (271, "Kweichow Moutai 15-Year demonstrates how extended ageing deepens the Jiangxiang profile described in the baijiu aroma type framework."),
    (272, "Moutai Prince illustrates the accessible tier of the Moutai ecosystem — key for list architecture and guest education."),
    (273, "Wuliangye Classic Nongxiang is the primary Nongxiang case study — five-grain strong aroma baijiu contrasted with Moutai's Jiangxiang."),
    (274, "Luzhou Laojiao 1573 Nongxiang demonstrates the mud-pit fermentation and robust strong aroma style central to this reference."),
    (276, "Fenjiu Blue and White Porcelain 20-Year is the Qingxiang (light aroma) benchmark — single sorghum, clean spirit, contrasted with Nongxiang's complexity."),
    (277, "Guilin Sanhua illustrates the southern Mixiang (rice aroma) category — warm climate rice substrate production described in the aroma type framework."),
]

# Shochu products: 155-170
SHOCHU_PRODUCTS_GENERAL = [
    (155, "Kuro Kirishima Imo Shochu 25° is the black koji imo shochu benchmark — illustrates the richer, darker style produced with kuro koji in Kagoshima."),
    (162, "Iichiko Silhouette Mugi Shochu demonstrates barley shochu — the clean, approachable mugi style contrasted with imo shochu's intensity."),
    (165, "Iichiko Special 43° Mugi Shochu illustrates premium aged barley expression at elevated ABV — the artisan end of the mugi category."),
    (166, "Helios Ryukyu Awamori 25° is the entry-level Okinawan awamori — directly relevant to the awamori regional distinction described."),
    (168, "Zuisen Awamori Koshu 10-Year demonstrates medium-aged awamori complexity — the koshu ageing potential central to this reference."),
    (170, "Kumesen Kusu 25-Year Aged Awamori is the benchmark long-aged awamori expression — illustrates the extreme potential of koshu ageing."),
]

SHOCHU_IMO_PRODUCTS = [
    (155, "Kuro Kirishima Imo Jochu — black koji Kirishima expression; the primary commercial benchmark for Kagoshima imo shochu."),
    (156, "Red Kirishima Imo Jochu — red koji variant from the same producer; demonstrates how koji type transforms the same substrate's flavour."),
    (157, "Toko Imo Shochu 25° from Yamagata demonstrates imo shochu production outside Kagoshima — different terroir, different sweet potato variety."),
    (158, "Toko Premium Aged Imo Shochu 40° is the high-ABV premium aged imo shochu benchmark — directly relevant to the ageing and dilution discussion."),
    (159, "Komasa Sakurajima Imo Shochu uses the Sakurajima region's volcanic ash soil — demonstrates how terroir affects sweet potato character."),
    (160, "Komasa Jozen Imo Shochu demonstrates the lighter shiro koji imo style as contrasted with Kirishima's kuro koji benchmark."),
]

def main():
    conn = psycopg2.connect(CONN)

    # Insert references
    ref_ids = {}
    for ref in REFS:
        try:
            with conn.cursor() as cur:
                cur.execute(SQL_REF, ref)
                row = cur.fetchone()
                conn.commit()
                ref_ids[ref["name"]] = row[0]
                print(f"  REF OK id={row[0]} name={row[1][:70]}")
        except Exception as e:
            conn.rollback()
            print(f"  REF FAIL {ref['name'][:50]}: {e}")

    # Determine IDs
    ref_names = list(ref_ids.keys())
    if len(ref_names) < 4:
        print("Not all refs inserted — check errors above")
        conn.close()
        return

    baijiu_ref_1 = ref_ids[ref_names[0]]  # Baijiu National Spirit
    baijiu_ref_2 = ref_ids[ref_names[1]]  # Baijiu Service/Pairing
    shochu_ref_1 = ref_ids[ref_names[2]]  # Shochu/Awamori general
    shochu_ref_2 = ref_ids[ref_names[3]]  # Imo Shochu specific

    print(f"\nRef IDs: baijiu_1={baijiu_ref_1}, baijiu_2={baijiu_ref_2}, shochu_1={shochu_ref_1}, shochu_2={shochu_ref_2}\n")

    # Build all links
    all_links = []
    for prod_id, note in BAIJIU_PRODUCTS:
        all_links.append({"technique_id": baijiu_ref_1, "product_id": prod_id, "relevance_note": note})
        all_links.append({"technique_id": baijiu_ref_2, "product_id": prod_id, "relevance_note": note})

    for prod_id, note in SHOCHU_PRODUCTS_GENERAL:
        all_links.append({"technique_id": shochu_ref_1, "product_id": prod_id, "relevance_note": note})

    for prod_id, note in SHOCHU_IMO_PRODUCTS:
        all_links.append({"technique_id": shochu_ref_2, "product_id": prod_id, "relevance_note": note})

    inserted = 0
    skipped = 0
    failed = 0
    for lnk in all_links:
        try:
            with conn.cursor() as cur:
                cur.execute(SQL_LINK, lnk)
                conn.commit()
                inserted += 1
                print(f"  LINK OK ref={lnk['technique_id']} prod={lnk['product_id']}")
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            skipped += 1
        except Exception as e:
            conn.rollback()
            failed += 1
            print(f"  LINK FAIL ref={lnk['technique_id']} prod={lnk['product_id']}: {e}")

    conn.close()
    print(f"\nDone: refs={len(ref_ids)}, links_inserted={inserted}, skipped={skipped}, failed={failed}")

if __name__ == "__main__":
    main()
