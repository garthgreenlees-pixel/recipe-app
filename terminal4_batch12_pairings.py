#!/usr/bin/env python3
"""terminal4_batch12_pairings.py — pairings for products 435-446 (12 products without pairing_intelligence)"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """
INSERT INTO pairing_intelligence
  (beverage_product_id, food_flavour_profile, pairing_type, flavour_logic, meal_context, confidence)
VALUES
  (%(beverage_product_id)s, %(food_flavour_profile)s, %(pairing_type)s, %(flavour_logic)s, %(meal_context)s, %(confidence)s)
"""

PAIRINGS = [
    # 435 — Bouchard Père et Fils Côte de Nuits-Villages Rouge (Burgundy regional red)
    {"beverage_product_id": 435, "food_flavour_profile": "duck breast with cherry reduction and roasted beetroot", "pairing_type": "complement", "flavour_logic": "Regional Pinot Noir's red-fruit core and earthy undertones mirror the gamey sweetness of duck; cherry sauce echoes the wine's fruit profile.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 435, "food_flavour_profile": "mushroom risotto with truffle oil and parmesan", "pairing_type": "bridge", "flavour_logic": "Côte de Nuits terroir delivers forest-floor and mushroom notes that bridge directly into earthy risotto; parmesan fat softens the wine's tannins.", "meal_context": "main", "confidence": "established"},
    {"beverage_product_id": 435, "food_flavour_profile": "aged comté and charcuterie board with cornichons", "pairing_type": "complement", "flavour_logic": "Nutty aged comté and cured meats match the wine's savoury Burgundian character; bright acidity cuts through charcuterie fat.", "meal_context": "cheese", "confidence": "classic"},
    {"beverage_product_id": 435, "food_flavour_profile": "roasted quail stuffed with foie gras on brioche toast", "pairing_type": "elevate", "flavour_logic": "Village-level Burgundy elevates fine game bird; foie gras richness is balanced by the wine's structural tannins and acidity.", "meal_context": "main", "confidence": "established"},

    # 436 — Drouhin Côte de Beaune-Villages (Burgundy regional white/red)
    {"beverage_product_id": 436, "food_flavour_profile": "roast chicken with tarragon butter and gratin dauphinois", "pairing_type": "complement", "flavour_logic": "Classic Burgundian partnership; Côte de Beaune red Pinot Noir complements the herbal richness of tarragon chicken and creamy potato gratin.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 436, "food_flavour_profile": "veal blanquette with cream and button mushrooms", "pairing_type": "bridge", "flavour_logic": "Pale veal's delicacy pairs beautifully with Côte de Beaune's lighter Pinot Noir; mushroom and cream bridge the wine's fruit and earthy notes.", "meal_context": "main", "confidence": "established"},
    {"beverage_product_id": 436, "food_flavour_profile": "époisses de Bourgogne washed-rind cheese", "pairing_type": "bridge", "flavour_logic": "Epoisses is the classic Burgundian cheese match; the wine's acidity and red fruit cut through the pungent, unctuous paste.", "meal_context": "cheese", "confidence": "classic"},
    {"beverage_product_id": 436, "food_flavour_profile": "pan-fried salmon with beurre blanc and capers", "pairing_type": "contrast", "flavour_logic": "Regional Burgundy can handle richer fish preparations; the wine's acidity contrasts the rich beurre blanc while Pinot's light body doesn't overwhelm salmon.", "meal_context": "fish_course", "confidence": "suggested"},

    # 437 — Château Pichon Comtesse de Lalande (Pauillac 2nd growth)
    {"beverage_product_id": 437, "food_flavour_profile": "rack of lamb with herb crust and Bordelaise sauce", "pairing_type": "complement", "flavour_logic": "Pauillac and lamb is the canonical Bordeaux pairing; the wine's cassis, cedar, and graphite notes complement the herb crust while tannins cut through lamb fat.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 437, "food_flavour_profile": "roast beef tenderloin with bone marrow and truffle jus", "pairing_type": "complement", "flavour_logic": "Second-growth Pauillac's structure and depth stand up to the richness of beef tenderloin; bone marrow softens tannins and truffle adds earthy complexity.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 437, "food_flavour_profile": "aged cheddar and blue cheese selection with walnut bread", "pairing_type": "bridge", "flavour_logic": "Pichon Comtesse's cab-dominated blend handles aged hard cheeses well; blue cheese contrasts the fruit while walnuts echo the wine's savoury notes.", "meal_context": "cheese", "confidence": "established"},
    {"beverage_product_id": 437, "food_flavour_profile": "wild mushroom and thyme tart with black truffle shavings", "pairing_type": "bridge", "flavour_logic": "Earthy truffle and mushroom bridge the wine's secondary forest-floor and tobacco notes; the tart's butter pastry smooths the wine's tannic grip.", "meal_context": "starter", "confidence": "established"},

    # 438 — Château Lynch-Bages (Pauillac 5th growth)
    {"beverage_product_id": 438, "food_flavour_profile": "côte de bœuf with béarnaise sauce and pommes sarladaises", "pairing_type": "complement", "flavour_logic": "Lynch-Bages is celebrated for its approachable Pauillac style that complements rich beef cuts; béarnaise adds herbal brightness that harmonises with the wine's aromatic profile.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 438, "food_flavour_profile": "roast lamb shoulder slow-cooked with garlic and rosemary", "pairing_type": "complement", "flavour_logic": "Slow-roasted lamb's depth of flavour matches Lynch-Bages's concentrated fruit and structured tannins; rosemary echoes the wine's herbal cassis notes.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 438, "food_flavour_profile": "duck confit with green lentils and smoked bacon", "pairing_type": "complement", "flavour_logic": "Duck confit's richness and smokiness align with Lynch-Bages's powerful character; lentils provide earthiness that bridges the wine's secondary flavours.", "meal_context": "main", "confidence": "established"},
    {"beverage_product_id": 438, "food_flavour_profile": "grilled lamb cutlets with chimichurri and charred aubergine", "pairing_type": "elevate", "flavour_logic": "Lynch-Bages's robust structure elevates chargrilled lamb; chimichurri's acidity refreshes the palate while char notes echo the wine's smoke and tobacco finish.", "meal_context": "casual", "confidence": "established"},

    # 439 — E. Guigal Côtes du Rhône Rouge (Southern Rhône entry-level)
    {"beverage_product_id": 439, "food_flavour_profile": "grilled merguez sausages with harissa and flatbread", "pairing_type": "complement", "flavour_logic": "Guigal's peppery Grenache/Syrah blend complements the spiced lamb in merguez; harissa's heat is balanced by the wine's generous fruit.", "meal_context": "casual", "confidence": "classic"},
    {"beverage_product_id": 439, "food_flavour_profile": "pizza with fennel sausage, mozzarella and oregano", "pairing_type": "complement", "flavour_logic": "Rustic Southern Rhône red is a natural pizza partner; fennel sausage echoes the wine's anise and garrigue notes.", "meal_context": "casual", "confidence": "classic"},
    {"beverage_product_id": 439, "food_flavour_profile": "beef daube Provençal with olives and herbes de Provence", "pairing_type": "bridge", "flavour_logic": "Classic Provençal braise with olive and thyme is the natural expression of Côtes du Rhône terroir — the wine bridges seamlessly with its garrigue and red-fruit character.", "meal_context": "main", "confidence": "established"},
    {"beverage_product_id": 439, "food_flavour_profile": "aged manchego and dried apricots on a charcuterie board", "pairing_type": "complement", "flavour_logic": "Manchego's nuttiness and dried fruit complement Guigal CdR's approachable red-fruit style; a versatile, crowd-pleasing combination.", "meal_context": "aperitif", "confidence": "suggested"},

    # 440 — Jean-Louis Chave Hermitage Rouge (Northern Rhône Syrah)
    {"beverage_product_id": 440, "food_flavour_profile": "braised wild boar with black pepper and juniper berry sauce", "pairing_type": "complement", "flavour_logic": "Chave Hermitage's monumental Syrah with its peppery, smoked-meat character is made for robust game; juniper and black pepper amplify the wine's spice profile.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 440, "food_flavour_profile": "aged Colston Bassett Stilton with quince paste", "pairing_type": "contrast", "flavour_logic": "Rich blue cheese contrasts Hermitage's powerful tannins and spice; quince paste bridges the wine's fruit and the cheese's savoury intensity.", "meal_context": "cheese", "confidence": "established"},
    {"beverage_product_id": 440, "food_flavour_profile": "grilled côte de bœuf with smoked bone marrow butter", "pairing_type": "complement", "flavour_logic": "A great Hermitage demands the finest beef; smoked bone marrow amplifies the wine's smoky, meaty secondary notes while its fat integrates the tannins.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 440, "food_flavour_profile": "roasted venison haunch with blackcurrant jus and celeriac purée", "pairing_type": "elevate", "flavour_logic": "Chave Hermitage's complexity and age-worthiness elevate the occasion of venison service; blackcurrant echoes the wine's dark fruit while celeriac earthiness bridges its mineral depth.", "meal_context": "main", "confidence": "established"},

    # 441 — Château Beaucastel CNDP Blanc (Châteauneuf-du-Pape white)
    {"beverage_product_id": 441, "food_flavour_profile": "butter-poached Maine lobster with saffron beurre blanc and fennel", "pairing_type": "elevate", "flavour_logic": "Beaucastel Blanc's rich Roussanne-dominant blend with its honey, beeswax and floral complexity elevates luxury lobster; saffron amplifies the wine's golden intensity.", "meal_context": "fish_course", "confidence": "classic"},
    {"beverage_product_id": 441, "food_flavour_profile": "roast monkfish with white miso butter and leek fondue", "pairing_type": "complement", "flavour_logic": "Beaucastel Blanc's weight and texture complement meaty monkfish; white miso's umami depth bridges the wine's savoury Roussanne character.", "meal_context": "fish_course", "confidence": "established"},
    {"beverage_product_id": 441, "food_flavour_profile": "truffle-stuffed roast chicken with morel cream sauce", "pairing_type": "bridge", "flavour_logic": "One of the great white wine-chicken pairings; CNDP Blanc's opulent body handles the truffle's earthiness while morel cream bridges its honeyed richness.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 441, "food_flavour_profile": "langoustine bisque with tarragon crème fraîche and brioche croutons", "pairing_type": "complement", "flavour_logic": "The wine's richness and weight are matched by bisque's concentrated crustacean sweetness; tarragon's anise note harmonises with the Roussanne's floral character.", "meal_context": "starter", "confidence": "established"},

    # 442 — Henry Marionnet Touraine Sauvignon Blanc (Loire Valley)
    {"beverage_product_id": 442, "food_flavour_profile": "chèvre frais with herb crust and pickled green tomatoes", "pairing_type": "complement", "flavour_logic": "Loire Sauvignon Blanc and fresh goat's cheese is the defining regional pairing; the wine's grassy, citrus notes mirror the cheese's tangy acidity.", "meal_context": "starter", "confidence": "classic"},
    {"beverage_product_id": 442, "food_flavour_profile": "asparagus with hollandaise and poached egg", "pairing_type": "bridge", "flavour_logic": "Touraine's vibrant acidity and herbaceous character bridge classic asparagus; hollandaise's richness is cut by the wine's freshness.", "meal_context": "starter", "confidence": "established"},
    {"beverage_product_id": 442, "food_flavour_profile": "oysters with mignonette and lemon", "pairing_type": "complement", "flavour_logic": "Loire Sauvignon Blanc's mineral, saline edge complements the briny character of oysters; a fresh, textbook pairing for aperitif service.", "meal_context": "aperitif", "confidence": "classic"},
    {"beverage_product_id": 442, "food_flavour_profile": "smoked salmon rillettes with crème fraîche and dill crackers", "pairing_type": "cleanse", "flavour_logic": "The wine's bright acidity and citrus zest cleanse the richness of salmon fat between bites, keeping the palate fresh throughout service.", "meal_context": "amuse", "confidence": "established"},

    # 443 — Gaffel Kölsch (Cologne ale)
    {"beverage_product_id": 443, "food_flavour_profile": "Cologne-style Himmel und Ääd (black pudding with apple sauce and mashed potato)", "pairing_type": "complement", "flavour_logic": "Gaffel Kölsch is the traditional accompaniment to Cologne's civic dish; the beer's delicate malt sweetness and mild hop balance the blood sausage's richness and apple's acidity.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 443, "food_flavour_profile": "Halloumi skewers with lemon, herbs and grilled vegetables", "pairing_type": "cleanse", "flavour_logic": "Kölsch's light, clean carbonation and gentle bitterness cleanse grilled halloumi's saltiness; the beer's delicate palate doesn't overwhelm the vegetables.", "meal_context": "casual", "confidence": "established"},
    {"beverage_product_id": 443, "food_flavour_profile": "schnitzel with potato salad and mustardy vinaigrette", "pairing_type": "complement", "flavour_logic": "Gaffel Kölsch's gentle malt and hop balance complement the breaded pork's mild richness; the beer's carbonation lifts the fried coating.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 443, "food_flavour_profile": "soft pretzels with obatzda beer cheese and radishes", "pairing_type": "complement", "flavour_logic": "Classic German beer snack combination; Kölsch's mild bitterness bridges the creamy beer cheese while complementing the pretzel's salty crust.", "meal_context": "aperitif", "confidence": "classic"},

    # 444 — Uerige Altbier (Düsseldorf copper ale)
    {"beverage_product_id": 444, "food_flavour_profile": "Sauerbraten with red cabbage, ginger snap gravy and potato dumplings", "pairing_type": "complement", "flavour_logic": "Uerige Altbier's firm malt backbone and roasted notes are made for Sauerbraten's tangy-sweet marinade; the beer's bitterness cuts through the sweet-sour gravy.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 444, "food_flavour_profile": "grilled bratwurst with Düsseldorf mustard and sauerkraut", "pairing_type": "complement", "flavour_logic": "The canonical Altbier food pairing in its home city; Uerige's copper malt character and firm hop bitterness complement the fatty sausage and cut through sauerkraut's acidity.", "meal_context": "casual", "confidence": "classic"},
    {"beverage_product_id": 444, "food_flavour_profile": "aged Gouda with smoked almonds and dark rye bread", "pairing_type": "bridge", "flavour_logic": "Altbier's caramel malt and roasted notes bridge perfectly to aged Gouda's butterscotch and nutty character; dark rye echoes the beer's malt complexity.", "meal_context": "cheese", "confidence": "established"},
    {"beverage_product_id": 444, "food_flavour_profile": "venison burger with pickled red onion and smoked bacon on a pretzel bun", "pairing_type": "complement", "flavour_logic": "Altbier's maltiness and moderate bitterness stand up to game meat's richness; smoke and pickle amplify the beer's roasted and bitter notes.", "meal_context": "casual", "confidence": "suggested"},

    # 445 — Lyrarakis Dafni (Cretan white, Dafni grape)
    {"beverage_product_id": 445, "food_flavour_profile": "grilled octopus with lemon, capers and wild rocket", "pairing_type": "complement", "flavour_logic": "Dafni's aromatic herb and floral character mirrors the Mediterranean cuisine of Crete; the wine's acidity and citrus complement char-grilled octopus perfectly.", "meal_context": "starter", "confidence": "classic"},
    {"beverage_product_id": 445, "food_flavour_profile": "dakos (Cretan barley rusk with tomato, feta and olives)", "pairing_type": "bridge", "flavour_logic": "The defining Cretan dish meets its native wine; Dafni's herbal and bay leaf notes bridge the olive oil, tomato and feta combination authentically.", "meal_context": "aperitif", "confidence": "classic"},
    {"beverage_product_id": 445, "food_flavour_profile": "stuffed courgette flowers with ricotta and mint in tomato sauce", "pairing_type": "complement", "flavour_logic": "Dafni's aromatic quality and fresh acidity complement the delicate floral courgette blossom; mint and ricotta align with the wine's herbal freshness.", "meal_context": "starter", "confidence": "established"},
    {"beverage_product_id": 445, "food_flavour_profile": "pan-fried sea bass with olive oil, garlic and cherry tomatoes", "pairing_type": "complement", "flavour_logic": "Simple pan-fried Mediterranean fish with olive oil is the ideal showcase for a native Cretan white; Dafni's herbal complexity and acidity elevate the clean fish flavour.", "meal_context": "main", "confidence": "established"},

    # 446 — Douloufakis Dafnios Red (Cretan red, Kotsifali/Mandilari)
    {"beverage_product_id": 446, "food_flavour_profile": "lamb kleftiko slow-roasted with garlic, lemon and herbs en papillote", "pairing_type": "complement", "flavour_logic": "Dafnios Red's spiced cherry, warm earth and herbal notes are the natural companion to Crete's iconic slow-roasted lamb; the wine's tannins integrate beautifully with the gelatinous meat.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 446, "food_flavour_profile": "stifado (Cretan beef and shallot stew with cinnamon and allspice)", "pairing_type": "bridge", "flavour_logic": "Stifado's warming spice profile bridges Dafnios Red's aromatic red-fruit and spice character; the wine's structure handles the braised beef's depth.", "meal_context": "main", "confidence": "classic"},
    {"beverage_product_id": 446, "food_flavour_profile": "graviera Cretan cheese aged with dried fig and honey", "pairing_type": "complement", "flavour_logic": "Cretan Graviera's mild nuttiness and sweet notes complement Dafnios Red's approachable, fruit-forward style; dried fig bridges the wine's fruit.", "meal_context": "cheese", "confidence": "established"},
    {"beverage_product_id": 446, "food_flavour_profile": "grilled lamb souvlaki with tzatziki, pita and charred onion", "pairing_type": "complement", "flavour_logic": "Dafnios Red's spiced fruit and moderate tannins are built for the char and herb of Greek souvlaki; tzatziki's cooling acidity refreshes the palate.", "meal_context": "casual", "confidence": "established"},
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
                print(f"  OK product={p['beverage_product_id']} ctx={p['meal_context']} food={p['food_flavour_profile'][:50]}")
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            skipped += 1
            print(f"  SKIP (exists) product={p['beverage_product_id']}")
        except Exception as e:
            conn.rollback()
            failed += 1
            print(f"  FAIL product={p['beverage_product_id']}: {e}")
    conn.close()
    print(f"\nDone: inserted={inserted}, skipped={skipped}, failed={failed}")

if __name__ == "__main__":
    main()
