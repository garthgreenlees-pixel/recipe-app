#!/usr/bin/env python3
"""terminal4_batch14_pairings.py — pairings for products 465-472 (traditional/cultural beverages)"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """
INSERT INTO pairing_intelligence
  (beverage_product_id, food_flavour_profile, pairing_type, flavour_logic, meal_context, confidence)
VALUES
  (%(beverage_product_id)s, %(food_flavour_profile)s, %(pairing_type)s, %(flavour_logic)s, %(meal_context)s, %(confidence)s)
"""

PAIRINGS = [
    # 465 — Tanna Noble Kava Borogu (Vanuatu)
    {"beverage_product_id": 465, "food_flavour_profile": "fresh coconut flesh with lime and Vanuatu sea salt", "pairing_type": "complement", "flavour_logic": "Fresh coconut's fat and sweetness complement kava's earthy, slightly bitter profile; the coconut flesh traditional accompaniment cleanses the palate and softens kava's numbing quality.", "meal_context": "any", "confidence": "classic"},
    {"beverage_product_id": 465, "food_flavour_profile": "laplap — Vanuatu taro and banana earth oven pudding with coconut cream", "pairing_type": "bridge", "flavour_logic": "The definitive traditional Vanuatu pairing: laplap's starchy, coconut-sweet flavour bridges kava's earthy bitterness; the earth-oven smoke adds ceremonial resonance.", "meal_context": "celebration", "confidence": "classic"},
    {"beverage_product_id": 465, "food_flavour_profile": "grilled reef fish with island lemon and wild herbs", "pairing_type": "cleanse", "flavour_logic": "Borogu kava's clean earthy bitterness and mild numbing effect cleanse the palate between bites of grilled fish; citrus heightens the beverage's earthy depth.", "meal_context": "main", "confidence": "established"},
    {"beverage_product_id": 465, "food_flavour_profile": "roasted taro chips with smoked coconut dipping sauce", "pairing_type": "complement", "flavour_logic": "Taro's neutral starch and slight sweetness complement kava's earthiness; smoked coconut adds depth that bridges the beverage's complex terroir-like character.", "meal_context": "casual", "confidence": "established"},

    # 466 — Vanuatu Noble Kava Export — Nakamal
    {"beverage_product_id": 466, "food_flavour_profile": "cassava fritters with chilli honey and shaved coconut", "pairing_type": "complement", "flavour_logic": "Export-grade kava's refined earthiness is complemented by cassava's mild starchiness; chilli honey bridges the beverage's mild spice while coconut softens the whole experience.", "meal_context": "aperitif", "confidence": "established"},
    {"beverage_product_id": 466, "food_flavour_profile": "Pacific-spiced pork belly bao with pickled cucumber and sriracha", "pairing_type": "bridge", "flavour_logic": "Noble kava's earthy complexity bridges Pacific pork preparations; the bao's soft sweetness soothes the slight bitterness and pickling acidity keeps the palate engaged.", "meal_context": "casual", "confidence": "suggested"},
    {"beverage_product_id": 466, "food_flavour_profile": "fresh papaya and pineapple with lime zest and tajín", "pairing_type": "cleanse", "flavour_logic": "Kava's mild numbing and earthy profile is cleansed by tropical fruit acidity; the bright flavours refresh the palate and complement the beverage's oceanic island character.", "meal_context": "any", "confidence": "established"},
    {"beverage_product_id": 466, "food_flavour_profile": "dark chocolate truffles with sea salt and toasted coconut", "pairing_type": "complement", "flavour_logic": "Noble kava's earthy bitterness complements dark chocolate's cacao depth; sea salt bridges the beverage's mineral quality and coconut echoes the islands.", "meal_context": "pre_dessert", "confidence": "adventurous"},

    # 467 — Lehua Hawaiian Awa — Mahakea Cultivar
    {"beverage_product_id": 467, "food_flavour_profile": "poke bowl with Hawaiian albacore, soy, sesame, macadamia and nori", "pairing_type": "complement", "flavour_logic": "Mahakea awa's clean, noble character is the traditional Hawaiian beverage companion to fresh raw fish; sesame and nori add umami that bridges the awa's earthy depth.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 467, "food_flavour_profile": "poi (fermented taro paste) with kalua pig and lomi salmon", "pairing_type": "bridge", "flavour_logic": "The iconic luau feast combination: Hawaiian awa's earthy bitterness bridges the sour-umami of poi and the smokiness of kalua pig; a traditional cultural pairing with deep historical roots.", "meal_context": "celebration", "confidence": "classic"},
    {"beverage_product_id": 467, "food_flavour_profile": "macadamia nut crusted mahi-mahi with coconut rice and mango salsa", "pairing_type": "complement", "flavour_logic": "Lehua awa's clean, slightly bitter profile with its earthy finish complements the richness of macadamia-crusted fish; coconut rice softens the awa and mango's acidity refreshes.", "meal_context": "main", "confidence": "established"},
    {"beverage_product_id": 467, "food_flavour_profile": "haupia (coconut milk pudding) with fresh pineapple", "pairing_type": "complement", "flavour_logic": "Traditional Hawaiian coconut milk dessert is a natural companion to awa ceremony; haupia's coolness and sweetness soothes the awa's mild numbing and bitter finish.", "meal_context": "dessert", "confidence": "established"},

    # 468 — Samoan Ava Ceremony Preparation
    {"beverage_product_id": 468, "food_flavour_profile": "palusami (taro leaves baked in coconut cream in umu)", "pairing_type": "complement", "flavour_logic": "The primary ceremonial Samoan food companion to ava: palusami's rich coconut cream and earthy taro complement ava's woody, slightly bitter character; the umu smoke adds ceremony.", "meal_context": "celebration", "confidence": "classic"},
    {"beverage_product_id": 468, "food_flavour_profile": "sapasui (Samoan chop suey with glass noodles, soy and vegetables)", "pairing_type": "bridge", "flavour_logic": "Ava's earthy depth bridges the umami-rich soy and glass noodles of sapasui; the beverage's mild bitterness cuts through the richness of the braised pork in the dish.", "meal_context": "main", "confidence": "established"},
    {"beverage_product_id": 468, "food_flavour_profile": "grilled oka (raw fish marinated in coconut cream and lime)", "pairing_type": "complement", "flavour_logic": "Oka's cool, citrusy coconut marinade complements ava's earthiness; the raw fish's clean sweetness balances the beverage's bitter notes and ceremonial weight.", "meal_context": "starter", "confidence": "established"},
    {"beverage_product_id": 468, "food_flavour_profile": "fresh young coconut water and tropical fruit platter", "pairing_type": "cleanse", "flavour_logic": "Coconut water's natural sweetness and electrolytes cleanse between ava rounds; tropical fruit acidity refreshes and complements the Pacific island terroir of the ava root.", "meal_context": "any", "confidence": "classic"},

    # 469 — Barako Lambanog Triple-Distilled (Philippines)
    {"beverage_product_id": 469, "food_flavour_profile": "lechon kawali (crispy deep-fried pork belly) with liver sauce and vinegar dip", "pairing_type": "complement", "flavour_logic": "The quintessential Filipino pulutan for lambanog: the spirit's clean coconut sweetness and heat complement crispy pork belly; vinegar dip bridges the spirit's acidity.", "meal_context": "casual", "confidence": "classic"},
    {"beverage_product_id": 469, "food_flavour_profile": "kinilaw na tanigue (raw Spanish mackerel in coconut vinegar and ginger)", "pairing_type": "bridge", "flavour_logic": "Lambanog's coconut base bridges naturally to coconut vinegar-cured fish; the spirit's clean spirit character complements the kinilaw's acidity and fresh ginger heat.", "meal_context": "starter", "confidence": "classic"},
    {"beverage_product_id": 469, "food_flavour_profile": "chicharon (pork rind crackling) with spiced vinegar and chopped tomato", "pairing_type": "cleanse", "flavour_logic": "Triple-distilled lambanog's clean heat cleanse the fat of chicharon effectively; vinegar dip bridges the spirit's acidity and the salt heightens the coconut base note.", "meal_context": "aperitif", "confidence": "established"},
    {"beverage_product_id": 469, "food_flavour_profile": "bibingka (coconut rice cake) with salted egg and shaved coconut", "pairing_type": "complement", "flavour_logic": "Lambanog's coconut character finds a direct echo in coconut rice cake; salted egg adds umami and the ritual context of festive food matches the spirit's celebratory heritage.", "meal_context": "any", "confidence": "established"},

    # 470 — Ilocos Region Basi — Traditional Fermented Sugarcane (Philippines)
    {"beverage_product_id": 470, "food_flavour_profile": "bagnet (Ilocano twice-cooked crispy pork) with native vinegar and tomato", "pairing_type": "complement", "flavour_logic": "The defining Ilocano pairing: basi's tannic, slightly sweet fermented character matches bagnet's deep pork richness; native vinegar bridges the wine's acidity.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 470, "food_flavour_profile": "pinakbet Ilocano (bitter melon, squash, eggplant and pork in fermented shrimp paste)", "pairing_type": "bridge", "flavour_logic": "Basi's complex fermented sweetness and tannin bridge bagoong's funk and the vegetables' bitterness; a culturally specific pairing that reflects Ilocano culinary identity.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 470, "food_flavour_profile": "dinakdakan (grilled and chopped pork offal with vinegar, onion and chilli)", "pairing_type": "complement", "flavour_logic": "Basi's fermented character and moderate tannin stand up to the strong flavours of dinakdakan; vinegar bridges the wine's acidity while the offal's richness integrates the tannin.", "meal_context": "casual", "confidence": "established"},
    {"beverage_product_id": 470, "food_flavour_profile": "grilled liempo (pork belly) marinated in calamansi and soy with garlic fried rice", "pairing_type": "complement", "flavour_logic": "Basi's sweet-tart profile complements the caramelised char on calamansi-marinated pork; garlic rice softens the wine's tannin and the soy's umami amplifies its depth.", "meal_context": "main", "confidence": "established"},

    # 471 — Cross-River Raphia Palm Wine (Nigeria)
    {"beverage_product_id": 471, "food_flavour_profile": "Cross River pepper soup with goat meat and uziza leaf", "pairing_type": "complement", "flavour_logic": "Palm wine's light sweetness and gentle ferment acidity complement the aromatic heat of Cross River pepper soup; uziza leaf adds herbal complexity that bridges the wine's yeasty freshness.", "meal_context": "starter", "confidence": "classic"},
    {"beverage_product_id": 471, "food_flavour_profile": "suya spiced beef skewers with onion, tomato and yaji pepper spice", "pairing_type": "bridge", "flavour_logic": "Palm wine's effervescent freshness and gentle acidity bridge the intense spice of suya; the beverage's natural sweetness tempers the peanut-chilli heat.", "meal_context": "casual", "confidence": "classic"},
    {"beverage_product_id": 471, "food_flavour_profile": "grilled tilapia with ata din din (fried pepper sauce) and jollof rice", "pairing_type": "complement", "flavour_logic": "Fresh raphia palm wine's yeasty, slightly sweet character complements grilled fish and the smoky tomato base of jollof; the beverage's natural CO2 cleanses the palm oil.", "meal_context": "main", "confidence": "established"},
    {"beverage_product_id": 471, "food_flavour_profile": "puff-puff (Nigerian fried dough) with hot sauce and groundnut soup", "pairing_type": "complement", "flavour_logic": "Fresh palm wine's mild sweetness and effervescence complement fried dough's oily richness; groundnut soup's complex fat and spice are bridged by the wine's earthy freshness.", "meal_context": "casual", "confidence": "established"},

    # 472 — Bafoussam Matango — Fermented Banana Wine (Cameroon)
    {"beverage_product_id": 472, "food_flavour_profile": "ndolé (Cameroonian bitter leaf stew with groundnuts and crayfish)", "pairing_type": "complement", "flavour_logic": "Matango's banana sweetness and gentle ferment acidity complement ndolé's complex bitter-umami profile; groundnut richness is bridged by the wine's natural sweetness.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 472, "food_flavour_profile": "poulet DG (director general chicken with plantain and vegetables)", "pairing_type": "complement", "flavour_logic": "Bafoussam banana wine's fruity sweetness pairs with the caramelised plantain in poulet DG; the dish's tomato-based richness is refreshed by the wine's gentle acidity.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 472, "food_flavour_profile": "grilled plantain with pepper sauce and smoked catfish", "pairing_type": "bridge", "flavour_logic": "Matango's banana base bridges directly to grilled plantain's caramelised sweetness; smoked catfish adds depth and the pepper sauce's heat is soothed by the wine's fruit.", "meal_context": "casual", "confidence": "established"},
    {"beverage_product_id": 472, "food_flavour_profile": "koki (steamed black-eyed pea pudding wrapped in banana leaf)", "pairing_type": "complement", "flavour_logic": "The banana leaf wrapping and Bafoussam terroir create a poetic pairing; koki's earthy legume depth is complemented by matango's sweet, lightly fermented banana character.", "meal_context": "any", "confidence": "established"},
]

def main():
    conn = psycopg2.connect(CONN)
    inserted = 0
    skipped = 0
    failed = 0
    for p in PAIRINGS:
        try:
            with conn.cursor() as cur:
                cur.execute(SQL, p)
                conn.commit()
                inserted += 1
                print(f"  OK pid={p['beverage_product_id']} ctx={p['meal_context']} food={p['food_flavour_profile'][:55]}")
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            skipped += 1
            print(f"  SKIP pid={p['beverage_product_id']}")
        except Exception as e:
            conn.rollback()
            failed += 1
            print(f"  FAIL pid={p['beverage_product_id']}: {e}")
    conn.close()
    print(f"\nDone: inserted={inserted}, skipped={skipped}, failed={failed}")

if __name__ == "__main__":
    main()
