#!/usr/bin/env python3
"""terminal4_batch18_tea_refs_links.py — refs and tech_links for Taiwan oolong (279-287) and Indian tea (288-298)"""
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
        "name": "Taiwan High Mountain Oolong — Gaoshan Altitude, Harvest Season, and the Oriental Beauty Distinction",
        "category": "tea_knowledge",
        "origin": "Taiwan",
        "description": (
            "Taiwan's Gaoshan (high mountain) oolongs are produced at elevations of 1,000-2,500m in the Central Mountain Range. "
            "The key appellations: Alishan (1,200-1,800m, Chiayi County) — approachable, sweet, dairy-like; "
            "Lishan (1,800-2,200m, Taichung) — more complex, orchid and honey notes; "
            "Dayuling (2,200-2,500m, Taichung) — the most prized, extremely limited, exceptionally sweet and floral. "
            "Oxidation levels: Gaoshan oolongs are lightly oxidised (15-25%), producing jade green leaves with a complex floral-sweet character. "
            "Harvest seasons matter significantly: spring (April-May) produces the most prized first flush; winter (October-November) produces a sweeter, "
            "lower-yield second harvest. Summer harvests are lighter in quality. "
            "Oriental Beauty (Dong Fang Mei Ren or Bai Hao Oolong) is a unique heavily oxidised (60-70%) Taiwanese oolong from Hsinchu and Miaoli. "
            "Its distinctive character comes from the tea jassid leafhopper insect biting young leaves, triggering a terpene response that creates "
            "the famous muscatel, honey and wild flower aromatics. It cannot be replicated with insecticides. "
            "Dong Ding oolong (from Nantou, medium elevation 600-1,000m) is Taiwan's most traditional style: medium oxidation with two processing options — "
            "traditional charcoal roasting (baked, nutty, complex) or modern light roasting (fresher, greener). "
            "Baozhong (Pouchong) is the least oxidised Taiwanese oolong (8-15%), from Wenshan in New Taipei City — almost green in character. "
            "Brewing: traditional Gongfu method (Yixing clay pot or gaiwan, 90-95C water, 6-8g per 100ml, 30-45s first infusion, extending each subsequent steep). "
            "Each tea yields 5-10+ infusions, each revealing new dimensions."
        ),
        "authority_tier": 1,
        "source_text": "Tea Research and Extension Station Taiwan 2024; Floating Leaves Tea Education; World Tea Expo 2024",
    },
    {
        "name": "Darjeeling — The Champagne of Teas: Flush Seasons, Muscatel Character, and Estate Hierarchy",
        "category": "tea_knowledge",
        "origin": "India — Darjeeling, West Bengal",
        "description": (
            "Darjeeling tea is produced in the foothills of the Himalayas in West Bengal at elevations of 600-2,000m. "
            "The Darjeeling GI (Geographical Indication) designation applies only to teas grown in 87 notified tea gardens in the district. "
            "Flush seasons define the character of Darjeeling tea: "
            "First Flush (March-April): Bright, light, green-fresh, floral; the most eagerly anticipated and highest-priced; Makaibari and Glenburn "
            "are estate benchmarks for biodynamic first flush. "
            "Second Flush (May-June): The iconic muscatel character (a grape-like, dry Muscat aromatic) develops due to tea jassid insect interaction "
            "with mature leaves; Castleton Muscatel is the most celebrated second flush. "
            "Monsoon/Rain Flush (July-September): Lower quality, primarily for blending. "
            "Autumn Flush (October-November): Fuller-bodied, more oxidised, copper-coloured liquor; rounder, less muscatel; Jungpana Autumn Flush is a reference estate. "
            "Estate hierarchy: Makaibari (biodynamic, certified organic, highest altitude in district at 2,000m+), Castleton, Glenburn, Jungpana, "
            "Badamtam, and Margaret's Hope are among the most celebrated estates. "
            "The Darjeeling TGFOP (Tippy Golden Flowery Orange Pekoe) grade indicates the proportion of tip/bud content. "
            "Brewing: 85-90C water (never boiling for first flush); 3g per 200ml; 2-3 minutes; no milk for quality Darjeeling (milk masks muscatel). "
            "White tea: Darjeeling silver tips (Jungpana) are the most delicate expression from the district."
        ),
        "authority_tier": 1,
        "source_text": "Tea Board of India 2024; Darjeeling Tea Association; World Tea Encyclopedia 2024",
    },
    {
        "name": "Assam and Nilgiri — India's Bold Orthodox and Frost Tea Traditions",
        "category": "tea_knowledge",
        "origin": "India — Assam and Nilgiri",
        "description": (
            "Assam: Located in northeast India, Assam is the world's largest tea-growing region by area. "
            "Camellia sinensis var. assamica produces the characteristic malty, robust, full-bodied liquor suited to milk service. "
            "Two production styles: CTC (cut-tear-curl) for commercial blends; Orthodox for specialty whole-leaf. "
            "Halmari Gold is among the highest-scored Assam estates for orthodox first flush — its bright, malty character with golden tips is the reference "
            "for quality Assam. Second flush Assam develops deeper malt and a fuller body. Assam is the base for most Irish and English breakfast blends. "
            "Nilgiri: Located in the Blue Mountains of Tamil Nadu and Kerala at 1,000-2,500m. Nilgiri is known for its clean, bright, floral style — "
            "distinctly different from Assam's malt. A unique feature is frost tea: during the cool winter months (December-January), frost on the leaves "
            "concentrates sugars and creates the Nilgiri frost tea's distinctive winter-harvest character. "
            "Kairbetta Estate Nilgiri Frost (Tippy) is the benchmark frost tea — its combination of high tippy content and cold-harvest concentration "
            "creates exceptional brightness and floral intensity unusual for Indian black tea. "
            "Both Assam and Nilgiri Orthodox benefit from water just off boil (95-99C), 3-4 minutes, with or without milk. "
            "Service context: Assam is appropriate for power breakfast service, brunch, and British-style afternoon tea. Nilgiri's brightness suits "
            "lighter afternoon pairings."
        ),
        "authority_tier": 2,
        "source_text": "Tea Board of India 2024; Halmari Estate; Nilgiri Tea Producers Association; World Tea Review 2024",
    },
]

# Links: ref_id -> [(product_id, note)]
LINK_CONFIGS = {
    "taiwan_oolong": [
        (279, "Alishan Spring Harvest is the most classic Gaoshan oolong expression — directly illustrates the altitude, spring flush, and light oxidation profile described."),
        (280, "Alishan Winter Harvest demonstrates how winter flush contrasts spring in sweetness and yield — central to the harvest season discussion."),
        (281, "Lishan Wang Family 2,200m is the intermediate ultra-high mountain expression — bridges Alishan and Dayuling in the altitude-quality hierarchy."),
        (282, "Dayuling 2,500m is the apex of Gaoshan oolong — directly illustrates the extreme altitude expression and limited availability discussed."),
        (283, "Oriental Beauty is the unique insect-bitten oolong described in this reference — its Dong Fang Mei Ren character and 60-70% oxidation contrast with Gaoshan styles."),
        (284, "Dong Ding Charcoal-Roasted demonstrates the traditional roasted Dong Ding style described in the medium-elevation Taiwan oolong context."),
        (285, "Dong Ding Modern Light Roasted provides the contrast to charcoal-roasted — the two Dong Ding processing styles discussed in this reference."),
        (286, "Jin Xuan Milk Oolong from Floating Leaves illustrates the cultivar-specific character (Jin Xuan 12) within the Taiwan oolong landscape."),
        (287, "Baozhong Pouchong from Floating Leaves demonstrates the least-oxidised Taiwanese oolong style — the Wenshan appellation counterpart to Gaoshan."),
    ],
    "darjeeling": [
        (288, "Makaibari First Flush Biodynamic is the premier first flush benchmark — directly illustrates the spring flush character and biodynamic estate quality described."),
        (289, "Castleton Second Flush Muscatel is the iconic muscatel reference — its tea jassid-influenced character is the defining example of Darjeeling second flush."),
        (290, "Glenburn Second Flush demonstrates another estate expression of the muscatel season for comparative estate analysis."),
        (291, "Jungpana Autumn Flush illustrates the autumn flush character — fuller-bodied, rounder, less muscatel, directly described in this reference."),
        (292, "Jungpana Silver Tips White Tea demonstrates Darjeeling white tea as the most delicate expression from the district covered here."),
        (298, "Glenburn Darjeeling Oolong demonstrates Darjeeling oolong as an emerging category — the district's extension beyond orthodox black tea."),
    ],
    "assam_nilgiri": [
        (293, "Halmari Gold Assam First Flush Orthodox is the primary quality Assam reference — its malty brightness sets the benchmark for the orthodox Assam style."),
        (294, "Halmari Second Flush demonstrates how Assam second flush develops deeper malt — essential for understanding flush-season variation in Assam."),
        (295, "Harney & Sons Assam Irish Breakfast illustrates the blending use of Assam described in the reference — CTC-based with robust character for milk service."),
        (296, "Kairbetta Nilgiri Frost Tea is the primary frost tea reference — directly illustrates the cold-harvest winter Nilgiri character described."),
        (297, "Harney & Sons Nilgiri Black Tea demonstrates the standard Nilgiri bright, clean style contrasted with Assam's malty robustness."),
    ],
}

def main():
    conn = psycopg2.connect(CONN)

    # Insert refs and capture IDs
    ref_ids = []
    for ref in REFS:
        try:
            with conn.cursor() as cur:
                cur.execute(SQL_REF, ref)
                row = cur.fetchone()
                conn.commit()
                ref_ids.append(row[0])
                print(f"  REF OK id={row[0]} name={row[1][:70]}")
        except Exception as e:
            conn.rollback()
            print(f"  REF FAIL {ref['name'][:50]}: {e}")

    if len(ref_ids) != 3:
        print(f"Expected 3 refs, got {len(ref_ids)}. Aborting links.")
        conn.close()
        return

    taiwan_ref_id, darjeeling_ref_id, assam_ref_id = ref_ids

    # Build and insert links
    all_links = []
    for prod_id, note in LINK_CONFIGS["taiwan_oolong"]:
        all_links.append({"technique_id": taiwan_ref_id, "product_id": prod_id, "relevance_note": note})
    for prod_id, note in LINK_CONFIGS["darjeeling"]:
        all_links.append({"technique_id": darjeeling_ref_id, "product_id": prod_id, "relevance_note": note})
    for prod_id, note in LINK_CONFIGS["assam_nilgiri"]:
        all_links.append({"technique_id": assam_ref_id, "product_id": prod_id, "relevance_note": note})

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
