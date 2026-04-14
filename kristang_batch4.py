#!/usr/bin/env python3
"""Kristang PCT-9 — Batch 4: Pork & Meat (10 entries)"""
import psycopg2, psycopg2.extras, re, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

entries = [
    {
        "name": "Feng: Kristang spiced pork and offal stew",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Feng is the most distinctly Kristang pork preparation — a dark, intensely spiced stew of pork belly, liver, heart, and sometimes kidney braised with black and white pepper, cloves, cinnamon, star anise, mustard seeds, and a generous quantity of white vinegar. "
            "The dish is named from the Portuguese 'frango' lineage (poultry, though feng is always pork in Malacca) — its structure is a direct descendant of the Portuguese tradition of spiced, vinegar-braised meats (vindalho, cozido) adapted to the pork-and-offal tradition of the Kristang kitchen.\n\n"
            "The spice profile of feng is the most European-facing in the Kristang culinary canon — the aromatic platform is black pepper, cloves, cinnamon, and star anise rather than galangal and lemongrass. "
            "The Southeast Asian elements are present — belacan in the base paste, fresh chili for heat — but they play a secondary role. "
            "The dominant flavour architecture is European-Portuguese: peppery, clove-sweet, cinnamon-warm, unified by vinegar acidity. "
            "This makes feng a valuable entry point for understanding the Kristang synthesis — the dish clearly reads as 'spiced Portuguese stew' to a European palate, while the belacan undercurrent and fresh chili heat are unmistakably Southeast Asian.\n\n"
            "Offal inclusion is the traditional marker — the pig's liver, in particular, adds an organ richness and textural variety that belly alone cannot provide. "
            "Modern Kristang cooks sometimes omit the offal for non-offal-eating guests, but the traditional version is whole-animal and festive. "
            "Feng is the traditional Chinese New Year dish for the Kristang community — eaten on New Year's Day and kept warm in the pot for days."
        ),
        "key_principles": (
            "Vinegar is added mid-braise, not at the end — it integrates into the sauce and loses its sharpness, contributing roundness. "
            "Offal is added later than the pork belly — it cooks faster and must not be overcooked. "
            "The spice platform is European (pepper, cloves, cinnamon, star anise), not Malay aromatic. "
            "Braise low and slow — pork belly collagen requires time; liver added only in the last 15-20 minutes."
        ),
        "common_mistakes": (
            "Adding vinegar at the end — it tastes sharp and aggressive rather than round and integrated. "
            "Adding liver at the start — it overcooks to a crumbly, dry texture that ruins the dish. "
            "Insufficient pepper — feng without generous black and white pepper is not feng. "
            "Short cooking time — pork belly not yet tender and collagen not dissolved."
        ),
        "pro_tips": (
            "The traditional feng uses head meat as well as belly and offal — the gelatinous head meat gives the sauce a sticky, unctuous quality. "
            "White vinegar is correct for feng; apple cider vinegar changes the flavour profile significantly. "
            "Feng improves dramatically over 24 hours — make it the day before service. "
            "The star anise and cinnamon quantity must be controlled: too much produces a medicinal quality. 1 star anise and half a cinnamon stick per 500g of meat is the correct proportion."
        ),
        "trigger_keywords": json.dumps(["feng", "Kristang pork stew", "Kristang feng", "Malacca pork stew", "Eurasian pork offal", "feng Malacca", "vinegar pork stew Kristang"]),
        "authority_tier": 1,
        "lives_or_dies": "The vinegar timing and the offal timing — two separate critical moments in the same dish. The vinegar must go in mid-braise to integrate properly. The liver must go in last to avoid overcooking. Both must be monitored and timed independently. A feng where the vinegar was added late tastes harsh; one where the liver was added early has crumbly, overcooked organ meat.",
        "flavour_context": "Peppery, clove-sweet, cinnamon-warm, vinegar-rounded — the most European-tasting Kristang dish, but with the depth and richness of a Southeast Asian long braise. The offal adds an organ-iron dimension beneath the spiced pork sweetness. Complex, dark, festive."
    },
    {
        "name": "Babi assam: Kristang pork in tamarind sauce",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Babi assam — pork in tamarind — is the everyday Kristang pork dish that shows the Southeast Asian face of the cuisine more clearly than feng. "
            "Fatty pork belly or pork ribs are braised in a tamarind-heavy sauce with shallots, galangal, lemongrass, fresh chili, and palm sugar — the rempah base is lighter than kari debal and the dominant flavour is the sweet-sour-savoury balance of the tamarind-palm sugar-belacan triangle.\n\n"
            "The pork cut is critical: pork belly with the skin on is the correct choice for babi assam — the rendered fat enriches the sauce, the skin adds gelatin and a silky texture, and the three layers (skin, fat, meat) provide textural variety. "
            "Pork ribs are the second choice. Lean pork shoulder produces a drier dish that lacks the characteristic richness.\n\n"
            "Cooking process: the rempah is fried in lard, pork is added and lightly browned in the paste, then tamarind liquid (medium-concentration), water, and a piece of tamarind skin (asam keping) are added for extended sourness during the braise. "
            "The dish simmers with the lid on for 30-40 minutes, then uncovered for a further 15-20 minutes to reduce the sauce to a thick, glossy, clinging consistency. "
            "The pork should be fall-tender at the bone but the skin should retain a slight chew — the textural contrast between soft meat, tender fat, and slightly resistant skin is integral to the dish."
        ),
        "key_principles": (
            "Pork belly with skin — the fat, gelatin, and skin texture are essential. "
            "Tamarind is the primary seasoning, not a finishing accent — use generously and taste. "
            "Reduce uncovered in the final stage — the clinging, glossy sauce is the finish. "
            "Palm sugar to balance the tamarind — essential for the sweet-sour dynamic."
        ),
        "common_mistakes": (
            "Lean pork cuts — dry, flavourless dish without the fat enrichment. "
            "Removing the skin — the gelatin is the textural foundation of the sauce. "
            "Insufficient tamarind — the dish becomes a generic curry rather than specifically babi assam. "
            "Not reducing the sauce — watery babi assam lacks the concentrated sweet-sour intensity."
        ),
        "pro_tips": (
            "Asam keping (dried tamarind skins/slices) added to the braising liquid provides a slow-release sourness distinct from the front-loaded sourness of tamarind paste. "
            "Score the pork skin before cooking — allows the fat to render more completely and the sauce to penetrate. "
            "Babi assam and white rice is one of the great pairings in Southeast Asian home cooking — the rice absorbs the tamarind sauce and every grain is flavoured. "
            "Adding 2-3 tomatoes to the braise adds a fruity sourness that complements the tamarind and reduces the overall salt requirement."
        ),
        "trigger_keywords": json.dumps(["babi assam", "pork tamarind Malacca", "Kristang tamarind pork", "asam pork", "babi assam kristang", "Malacca pork dish", "sweet sour pork Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "The sauce reduction. A babi assam with thin, watery sauce tastes of all the right ingredients but has none of the concentrated sweet-sour intensity that makes the dish extraordinary. Reduce until the sauce clings to the pork — each piece should be coated in a glossy, dark, slightly thick layer that doesn't run off onto the plate.",
        "flavour_context": "Sweet-sour-savoury — the tamarind-palm sugar-belacan triangle in its most direct expression. The pork fat carries all three flavours through the sauce and extends their richness. The residual chili heat is gentle and lingering rather than sharp."
    },
    {
        "name": "Kristang pork belly crisping: kulit babi technique",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Kulit babi — pork crackling — is a Kristang technique of producing shatteringly crispy pork skin that serves both as a cooking by-product (from lard rendering) and as a standalone dish or garnish. "
            "The technique reflects the Portuguese heritage of whole-animal cookery and the Catholic Kristang freedom from pork prohibitions — crackling is served at festivals, eaten as a snack during cooking, and used to garnish rice and vegetable dishes.\n\n"
            "Preparation for crackling: pork skin (belly skin removed from the belly layer) is boiled for 30-40 minutes until soft and translucent, then removed, dried thoroughly, and scored with a sharp knife in a crosshatch pattern. "
            "The dried, scored skin is placed on a rack and air-dried in the refrigerator overnight — the surface must be completely dry before frying. "
            "Frying: the dried skin is added to cold lard or oil, then the heat is raised. "
            "The skin expands as it heats and the water trapped in the tissue escapes as steam — this expansion is what creates the bubbly, blistered texture. "
            "The correct temperature for full expansion and crispness is 180-190°C.\n\n"
            "The Kristang variation: after the basic crispy crackling is achieved, some preparations baste the hot crackling with a mixture of palm sugar, garlic, and dried chili before returning it to the oven for 5 minutes — producing a spiced, sweet-glazed crackling (a variant that echoes the Portuguese tradition of honey-glazed pork)."
        ),
        "key_principles": (
            "Completely dry before frying — residual moisture causes violent oil splatter and prevents proper expansion. "
            "Start in cold oil/lard and raise heat — this allows even expansion rather than immediate surface sealing. "
            "Score the skin — crosshatch scoring ensures even expansion and prevents curling. "
            "Air-dry overnight in the refrigerator — surface desiccation is essential."
        ),
        "common_mistakes": (
            "Frying without drying — violent splatter, uneven expansion, steamed rather than crisped skin. "
            "Hot oil immediately — the surface seals before the interior can expand. "
            "Not boiling first — raw skin does not expand properly during frying. "
            "Skipping the scoring — unscored skin curls and bubbles unevenly."
        ),
        "pro_tips": (
            "Rub the dry skin with rice vinegar and a light salt coat before air-drying — the vinegar draws out additional surface moisture and produces a crispier final product. "
            "The pork skin from belly streaks is the best for crackling — the thin fat layer under the skin renders cleanly. "
            "Spiced Kristang crackling (with palm sugar glaze) served as a pre-meal snack is a distinctive Kristang hospitality tradition — the sweetness of the glaze with the savoury crackling is excellent. "
            "Professional kitchen tip: expanded pork crackling can be stored in an airtight container at room temperature for 2-3 days and re-crisped for 3-4 minutes in a 200°C oven before service."
        ),
        "trigger_keywords": json.dumps(["kulit babi", "pork crackling Kristang", "Kristang pork skin", "Malacca crackling", "pork skin frying", "crispy pork Kristang", "Portuguese pork crackling"]),
        "authority_tier": 1,
        "lives_or_dies": "The dryness of the skin before frying. Skin that is even slightly moist will not expand to full crackling — it will shrink, harden, and produce a chewy rather than shatteringly crisp product. Touch the skin before it goes in the oil: it must feel papery dry, almost like dried noodle skin.",
        "flavour_context": "Intensely savoury pork fat, rendered and crisped — the purest expression of the Maillard reaction applied to pork skin. Plain crackling is salty and neutral; the Kristang spiced-glaze variation adds sweet, chili, and garlic to the crispy base, creating a complex single-bite experience."
    },
    {
        "name": "Kristang pork ribs with cincalok: flavour pairing technique",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The pairing of pork with cincalok is a distinctly Kristang flavour combination — the sweet richness of pork fat and the intensely fermented-saline character of cincalok (fermented baby shrimp) create a contrast pairing of unusual depth. "
            "The technique is used in two ways: cincalok as a table condiment alongside grilled or braised pork, and cincalok incorporated directly into the braising liquid or marinade.\n\n"
            "Cincalok as marinade component: a tablespoon of cincalok, loosened with calamansi juice and mixed with shallots and garlic, is used as a marinade base for pork spare ribs. "
            "The salt and fermented shrimp compounds in the cincalok penetrate the meat during marination (minimum 4 hours, overnight preferred) and produce a deeply savoury, umami-rich flavour foundation. "
            "The marinated ribs are then grilled over charcoal or roasted in an oven — the cincalok caramelises on the surface of the ribs, producing a dark, intensely flavoured crust.\n\n"
            "Cincalok as table condiment alongside pork: a small bowl of fresh cincalok condiment (cincalok + shallots + calamansi + fresh chili) is placed alongside roasted or braised pork. "
            "The diner takes a small amount with each mouthful of pork — the fermented-acid condiment cuts through the fat and adds complexity. "
            "This tableside pairing is one of the characteristic Kristang dining experiences — simple, precise, and requiring no explanation once tasted."
        ),
        "key_principles": (
            "Minimum 4-hour marinade, overnight preferred — the cincalok compounds need time to penetrate. "
            "Calamansi juice in the marinade activates and brightens the cincalok's fermented notes. "
            "Caramelisation of the cincalok surface is the goal — it adds sweetness and depth to the fermented base. "
            "As a condiment: tiny quantities only — a teaspoon alongside, not piled on."
        ),
        "common_mistakes": (
            "Short marination time — cincalok flavour on the surface only, not through the meat. "
            "Too much cincalok in the marinade — the fermented intensity overwhelms rather than enhances. "
            "Not caramelising the surface during grilling — misses the Maillard development of the fermented compounds. "
            "Serving without calamansi — the acid is essential to activate and balance the fermented saltiness."
        ),
        "pro_tips": (
            "Cincalok marinade works equally well on chicken — the resulting grilled chicken is deeply savoury and aromatic. "
            "The cincalok surface caramelisation on grilled ribs produces a crust that resembles Korean doenjang-marinated pork — the same principle of fermented-umami compounds Maillard-reacted at high heat. "
            "For service, the fresh cincalok condiment should be made no more than 30 minutes before service — the calamansi juice changes character over time. "
            "A cross-cultural professional note: the Kristang pork-cincalok pairing is functionally identical to the Italian pork-anchovy pairing (saltimbocca, bagna càuda with pork) — fermented salt-preserved seafood as a contrasting pairing with pork fat."
        ),
        "trigger_keywords": json.dumps(["pork cincalok", "Kristang pork fermented shrimp", "cincalok marinade pork", "pork ribs Malacca", "Kristang pork technique", "cincalok pork pairing", "fermented shrimp pork"]),
        "authority_tier": 1,
        "lives_or_dies": "The caramelisation during grilling. Cincalok on pork that has not been properly grilled — where the surface has merely heated through without caramelising — tastes intensely fishy-salty rather than deep and complex. The Maillard reaction on the fermented shrimp compounds transforms the flavour from raw-fermented to caramelised-savoury.",
        "flavour_context": "Pork-sweet, fat-rich, then the sharp contrast of fermented-salty-sour cincalok — a pairing of opposites that creates unusual complexity. The contrast works because each element is assertive enough to be clearly identifiable while the combination produces something neither could achieve alone."
    },
    {
        "name": "Kristang roast pork: baboy assado Portuguese technique",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Baboy assado — roast pork in the Kristang Creole language — is the Portuguese roasting tradition preserved in the Kristang kitchen, adapted to a tropical climate (charcoal and wood-fired rather than oven-roasted in the original preparations) and spiced with the local aromatic vocabulary. "
            "The dish is distinct from Chinese-style char siu or Cantonese roast pork — the Kristang version uses a vinegar-garlic-pepper marinade (the vinha d'alhos signature) rather than the soy-honey-five-spice platform of Chinese roast pork.\n\n"
            "Preparation: pork loin or shoulder is scored deeply on all sides and rubbed with a paste of white vinegar, garlic, black pepper, coarse salt, and small amounts of cumin and coriander. "
            "The meat is marinated overnight, then roasted slowly (low and slow, 160°C for 2-3 hours depending on size) with basting every 30 minutes using the pan drippings and additional vinegar. "
            "The finished roast is rested for 20 minutes before slicing. "
            "The carving reveals a deeply coloured, spiced crust over juicy, aromatic meat — the vinegar has tenderised the exterior and the garlic and pepper have penetrated through the scored channels.\n\n"
            "The scored channels are the technique's critical feature — without deep scoring, the vinegar-garlic marinade stays on the surface rather than penetrating. "
            "Professional scores go 2cm deep and are spaced 2-3cm apart across all surfaces. "
            "The result is a roast that is fully flavoured throughout rather than merely crusted on the outside — a hallmark of the Portuguese roasting tradition."
        ),
        "key_principles": (
            "Deep scoring (2cm) on all surfaces — marinade penetration is the point of the technique. "
            "Overnight marinade — surface-only marination produces a crust but no interior flavour. "
            "Low and slow roasting (160°C) — preserves moisture while developing the crust. "
            "Baste every 30 minutes — the rendered fat and vinegar combination builds the crust gradually."
        ),
        "common_mistakes": (
            "Shallow scoring — marinade stays on the surface. "
            "Short marination — garlic and pepper on the exterior only. "
            "High roasting temperature — dry, tough exterior before the interior is cooked. "
            "No resting — cutting immediately loses the juices accumulated during resting."
        ),
        "pro_tips": (
            "The vinha d'alhos marinade is the same preparation used for vindaloo — the word 'vindaloo' derives from 'vinho d'alhos' (wine and garlic), demonstrating the Portuguese-Goa-Kristang shared culinary ancestry. "
            "Adding lemongrass to the marinade (finely minced) produces a Kristang-specific variation with the Portuguese base and Malay aromatic layer. "
            "The pan drippings from baboy assado — vinegar, rendered fat, garlic caramelised — are an exceptional basting sauce and should never be discarded. "
            "Serve with Kristang achar — the pickle's sharp acidity is the classic counterpart to the roast's richness."
        ),
        "trigger_keywords": json.dumps(["baboy assado", "Kristang roast pork", "Portuguese roast pork Malacca", "vinha d alhos pork", "Eurasian roast pork", "Malacca roast pork", "Kristang Christmas pork"]),
        "authority_tier": 1,
        "lives_or_dies": "The scoring depth and marinade time together. A beautifully scored pork loin marinated for 2 hours produces the same result as an unscored one — a flavoured crust over bland interior. Overnight marinade with deep scoring produces a completely different experience: every slice is aromatic from inside to outside.",
        "flavour_context": "Garlic-vinegar-pepper crust over sweet, juicy pork — the Portuguese roasting tradition in its most direct form. The vinegar's acid both tenderises and adds a brightness that prevents the richness from being heavy. The spiced crust adds aromatic complexity; the interior sweetness of the pork carries the flavour."
    },
    {
        "name": "Kristang pork meatball: bidara technique",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Bidara are the Kristang pork meatballs — a preparation that shows the Portuguese influence through the form (minced meat formed into balls and cooked in sauce, a technique found across the Portuguese culinary tradition as 'almôndegas') while using the Kristang spice vocabulary in both the meatball mixture and the cooking sauce. "
            "Bidara are served in a tomato-based or coconut milk-based sauce — the tomato version is more European-facing; the coconut milk version more Malay-facing.\n\n"
            "Meatball mixture: minced pork shoulder (not too lean — a 70/30 lean-to-fat ratio is ideal) is combined with finely minced garlic, shallots, fresh coriander leaf, a small amount of soy sauce, white pepper, salt, and a binding agent (breadcrumbs soaked in coconut milk). "
            "The mixture is worked by hand until it holds together — unlike Italian meatballs, Kristang bidara are not enriched with egg, which produces a denser, more resilient texture suitable for the longer sauce cooking. "
            "They are formed to golf-ball size (approximately 30-35g each).\n\n"
            "The cooking sauce is made from fried sambal berlado (chili paste) combined with either diced tomatoes and chicken stock (the European version) or coconut milk and tamarind (the Malay version). "
            "The raw meatballs are added to the simmering sauce and cooked for 15-18 minutes — they must not be pre-fried, as frying before saucing is not traditional and produces a drier result."
        ),
        "key_principles": (
            "70/30 pork (lean/fat) — leaner pork produces dry, crumbly meatballs. "
            "No egg in the mixture — Kristang bidara bind with breadcrumb-coconut milk soaker. "
            "Golf-ball size — 30-35g; larger meatballs need longer sauce cooking and can develop dry interiors. "
            "Cook raw in the sauce — not pre-fried; the sauce penetrates the meatball from the outside."
        ),
        "common_mistakes": (
            "Lean pork mince — dry, crumbly, flavourless meatballs. "
            "Adding egg as binder — changes the texture to softer and more delicate than the traditional resilient bite. "
            "Pre-frying before saucing — sealed surface prevents sauce penetration. "
            "Too large — centre doesn't cook through in reasonable sauce-cooking time."
        ),
        "pro_tips": (
            "The breadcrumb-coconut milk soaker is the Kristang binding secret — soak 2 tablespoons of breadcrumbs in 3 tablespoons of coconut milk for 5 minutes, then squeeze out excess and add to the mince. "
            "Chill the meatball mixture for 30 minutes before forming — cold fat in the mixture holds the balls together more easily during forming. "
            "The Kristang version with tomato sauce uses canned whole tomatoes crushed by hand — the texture of crushed whole tomatoes is correct; blended tomato puree produces a too-smooth sauce that lacks body. "
            "Cross-cultural note: Kristang bidara and Portuguese almôndegas are essentially the same preparation — the Kristang spice additions (fresh coriander, white pepper, soy) are the local adaptations."
        ),
        "trigger_keywords": json.dumps(["bidara", "Kristang meatballs", "pork meatball Malacca", "Eurasian meatballs", "Kristang almondega", "bidara Malacca", "Portuguese meatball Kristang"]),
        "authority_tier": 1,
        "lives_or_dies": "The fat-to-lean ratio of the mince. A meatball made from lean pork will be dry, grainy, and flavourless after 15 minutes in sauce. A meatball made from 70/30 pork stays moist, tender, and absorbs the sauce flavours without losing its own character.",
        "flavour_context": "Savoury pork sweetness, lightly spiced with white pepper and fresh coriander, enriched by the coconut milk binder — the interior flavour is mild and fragrant. The sauce (whether tomato or coconut) provides the assertive flavour; the meatball provides the richness and textural platform."
    },
    {
        "name": "Feng spice mix: Kristang European aromatic blend",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The feng spice blend is one of the few primarily European-derived spice combinations in the Kristang culinary system — a mixture of black pepper, white pepper, cloves, cinnamon, star anise, and mustard seeds that forms the aromatic backbone of the feng pork stew. "
            "This spice combination, with its emphasis on pepper and cloves, has more in common with medieval Portuguese and Portuguese colonial spice use than with the galangal-lemongrass-turmeric framework of Malay cuisine, making it a valuable historical marker.\n\n"
            "The proportions: black pepper (2 parts) — white pepper (1 part) — cloves (0.5 part) — cinnamon bark (1 part) — star anise (0.5 part) — white mustard seeds (0.5 part). "
            "All dry spices are toasted and ground fresh. The pepper dominance (3 parts combined black and white pepper) is characteristic — feng without this peppery assertiveness is incorrect. "
            "The mustard seeds are different from the others: they are added whole to the hot fat at the start of cooking (before the rempah is fried), where they pop and add a nutty, faintly bitter layer that disperses through the oil.\n\n"
            "The cinnamon in this blend is significantly different in role from its use in Indian biryani or Moroccan tagine — in feng, it adds a sweet-warm background note that supports the pepper dominance rather than competing with it. "
            "The quantity must be carefully controlled: too much cinnamon (more than a single 5cm piece per pot) produces a medicinal, almost pharmaceutical quality that overwhelms the pork. "
            "This restraint with cinnamon is a Kristang cooking standard — it is used as a background element, not a headline spice."
        ),
        "key_principles": (
            "Toast and grind all dry spices fresh — the pepper volatiles particularly degrade quickly once ground. "
            "Mustard seeds added whole to hot fat before rempah — they must pop before the paste goes in. "
            "Black and white pepper together — black provides heat and aroma; white provides a different aromatic dimension. "
            "Restrained cinnamon — a background note, not a dominant flavour."
        ),
        "common_mistakes": (
            "Too much cinnamon — medicinal, pharmaceutical character overwhelms the pepper-pork base. "
            "Pre-ground stale spices — flat, dusty aromatic profile. "
            "Mustard seeds added with the paste — they don't pop correctly when buried in wet paste. "
            "Unequal pepper — all black pepper produces a different result from the traditional black-and-white combination."
        ),
        "pro_tips": (
            "The feng spice blend, when considered historically, is a snapshot of the spice trade's impact on Portuguese colonial cooking — cloves, pepper, and cinnamon were the three highest-value Spice Islands commodities that Portuguese ships carried, and their combination in a single dish reflects their trade route origin. "
            "White pepper (made from the fully ripe berry, soaked to remove the outer hull) has a fermented, slightly musty heat character completely different from black pepper — the combination of the two produces a more complex peppery dimension than either alone. "
            "Toast cloves and star anise together — they have similar heat tolerances. Toast pepper separately — it needs slightly longer. "
            "The feng spice blend works excellently as a dry rub for pork ribs before oven roasting."
        ),
        "trigger_keywords": json.dumps(["feng spice mix", "Kristang European spice blend", "feng pork spices", "Malacca pork spice", "Portuguese colonial spice", "feng spices Malacca", "Eurasian spice blend pork"]),
        "authority_tier": 1,
        "lives_or_dies": "The freshness of the pepper. Feng is a peppery dish — the pepper is the star, not the supporting cast. Old ground pepper contributes only mild heat without the sharp, volatile aromatic quality that fresh-ground pepper provides. Grind the pepper for feng on the day of cooking, never use pre-ground.",
        "flavour_context": "Pepper-forward, clove-sweet, cinnamon-warm, with the mustard seed's nutty-bitter pop — a European medieval spice profile in a Southeast Asian kitchen. The pepper dominance and the vinegar in the braise make feng taste more like a Portuguese cozido than a Malay curry, despite the shared Kristang kitchen."
    },
    {
        "name": "Kristang offal preparation: cleaning and prepping organ meats",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The Kristang tradition of whole-animal pork use — including liver, heart, kidney, stomach, and intestine — requires specific cleaning and preparation techniques that are absent from cuisines that avoid offal. "
            "The Kristang Catholic heritage, combined with the practical economics of the fishing and small-holding communities, produced a kitchen in which no part of the pig was wasted and offal was valued as much as muscle.\n\n"
            "Liver: pork liver for feng is sliced against the grain into 1cm pieces and soaked in cold water for 15-20 minutes to leach out excess blood and reduce the strong iron flavour. "
            "The soaking water is changed twice. After soaking, the liver is dried and added to the stew in the last 15-20 minutes of cooking — it reaches correct texture (firm but yielding, not grainy) in this time.\n\n"
            "Heart: pork heart is split, the connective tissue and interior chambers are trimmed, and it is quartered and treated similarly to muscle meat — braised in the stew from near the start due to its denser structure. "
            "Stomach (pork tripe): boiled for 1-2 hours with ginger and rice wine to remove odour, then sliced before adding to the braise. "
            "Intestine: cleaned with alternating salt and vinegar washes (3-4 times each), then blanched for 10 minutes before use. "
            "Each organ has a different cooking time and preparation requirement — the Kristang cook must know all of them to produce a correct feng."
        ),
        "key_principles": (
            "Each offal has a different preparation protocol — they cannot be treated uniformly. "
            "Liver goes in last — its shorter cooking time means it must not braise as long as muscle. "
            "Heart goes in with the muscle — it is dense and takes long cooking. "
            "Tripe and intestine require preliminary cooking and odour removal before entering the stew."
        ),
        "common_mistakes": (
            "All offal added at the start — liver overcooked and crumbly before the stew is finished. "
            "Insufficient liver soaking — strong iron-blood flavour that dominates the stew. "
            "Skipping odour removal for tripe — an ammonia-like off-note in the finished dish. "
            "Thin slices of liver — disintegrate completely in the braise rather than holding form."
        ),
        "pro_tips": (
            "Milk-soaking liver for 30 minutes (instead of water) produces an even milder, sweeter liver flavour — less traditional but appreciated by those sensitive to the iron note. "
            "The Kristang whole-animal tradition parallels the French charcuterie tradition in its valorisation of every part of the pig. "
            "Heart muscle is the most approachable offal for non-offal-eating diners — its texture closely resembles muscle meat and its flavour is deeply savoury without the organ intensity of liver. "
            "Intestine casings, after cleaning, can be used for sausage making — the Kristang smoked sausage tradition (influenced by Portuguese linguiça) uses cleaned intestine as the casing."
        ),
        "trigger_keywords": json.dumps(["Kristang offal", "pork organ preparation", "feng offal", "pork liver Malacca", "Kristang whole animal", "pork heart technique", "Eurasian offal cooking"]),
        "authority_tier": 1,
        "lives_or_dies": "The timing of liver addition. Add it too early and by the time the stew is finished the liver is grey, grainy, and dry — an unpleasant texture that undermines the whole dish. Add it in the last 15-20 minutes and it reaches perfect texture: firm, sliceable, still slightly rosy at the centre.",
        "flavour_context": "Iron-rich, deeply savoury, organ-sweet — pork liver has a sweetness beneath its iron intensity that is revealed when it is correctly cooked. Heart has a denser, meatier quality without the liver's specific iron note. Together in feng, they add layers of organ complexity to the spiced pork belly base."
    },
    {
        "name": "Kristang smoked sausage: chouriço influence",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The Kristang smoked sausage tradition is a direct descendant of Portuguese chouriço (choriz) — the paprika-spiced, garlic-forward, smoke-dried pork sausage that is one of the foundational elements of Portuguese charcuterie. "
            "In Malacca, the paprika of the original Portuguese chouriço was replaced by dried red chili (locally available and structurally similar as a fat-soluble red colourant and gentle heat provider), and the smoking technique adapted to local hardwoods rather than Portuguese oak.\n\n"
            "The Kristang sausage mixture: coarsely minced pork shoulder and back fat (75/25 lean-fat ratio), combined with dried red chili paste, garlic (pounded), white pepper, cumin, coriander, salt, and white vinegar. "
            "The mixture is worked thoroughly and left to marinate overnight before stuffing into cleaned pork intestine casings. "
            "The sausages are then either fresh-cooked (pan-fried or added to kari debal as the second protein layer) or hung and smoked over charcoal for 2-3 days to produce a semi-dried, shelf-stable smoked sausage.\n\n"
            "The fresh Kristang sausage is used as an additional protein in kari debal — the Devil's Curry Christmas dish traditionally uses leftover Christmas roast meats plus sliced fresh or smoked sausage. "
            "The smoked version is sliced and served cold with rice or bread, or added to rice porridge as a flavouring element. "
            "The flavour connection to Portuguese chouriço is clear — both are red, garlicky, mildly spiced pork sausages — but the Kristang version has a distinctly more aromatic, cumin-forward, Asian-spiced character."
        ),
        "key_principles": (
            "75/25 lean-fat ratio — fat is essential for juicy texture and flavour carrier. "
            "Overnight marination of the mince before stuffing — the spice penetration needs time. "
            "Dried red chili paste, not paprika — the correct local adaptation for colour and mild heat. "
            "Fresh sausages must be used within 2-3 days; smoked versions keep for weeks."
        ),
        "common_mistakes": (
            "Too lean — dry, crumbly sausage that lacks the fat necessary for juiciness. "
            "Short marination — surface flavour only. "
            "Under-smoking — pale, uncured sausage that does not keep. "
            "Over-smoking — bitter, acrid character from too much smoke exposure."
        ),
        "pro_tips": (
            "The Kristang sausage connection to chouriço is also a connection to Spanish chorizo and through Goa to the Indian beef or pork chouriço — all share the Portuguese dried-red-spice, garlic, vinegar construction. "
            "Fresh Kristang sausage sliced and fried in lard is one of the best breakfast preparations in the cuisine — the fat renders, the chili caramelises, and the garlic becomes golden. "
            "For smoking, coconut shell charcoal produces a clean, slightly sweet smoke that complements the pork better than hardwood chips. "
            "The smoked Kristang sausage added to kari debal provides a second flavour dimension — smoked, dense pork alongside the fresh-braised meat."
        ),
        "trigger_keywords": json.dumps(["Kristang sausage", "chouriço Malacca", "Portuguese sausage Malacca", "Kristang smoked sausage", "pork sausage Kristang", "Malacca Portuguese sausage", "Eurasian charcuterie"]),
        "authority_tier": 1,
        "lives_or_dies": "The fat content. A Kristang sausage with insufficient fat is a disappointment at the first bite — dry, crumbly, without the juicy, richly spiced character that is the point of the preparation. Fat is structural, not optional.",
        "flavour_context": "Garlicky, red-chili warm, cumin-aromatic, smoky if dried — the Portuguese chouriço character translated into the Kristang aromatic vocabulary. The chili substitute for paprika produces a brighter, more forward heat than the original paprika's warm-sweet character, but the structural flavour identity is preserved."
    },
    {
        "name": "Kristang pork with vegetables: babi lodeh technique",
        "category": "Kristang — Pork & Meat",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Babi lodeh is the Kristang version of the Malay lodeh (vegetable braise in coconut milk) adapted for pork — a preparation that uses the lodeh technique (light coconut milk broth with lemongrass, galangal, and mild spicing) but adds pork as the protein and uses lard as the cooking fat. "
            "It is the most domestically everyday Kristang pork dish — quicker to cook than feng or kari debal, lighter in spice, and adaptable to whatever vegetables are available.\n\n"
            "Vegetable selection: traditionally includes long beans (kacang panjang), cabbage, young jackfruit (nangka muda), tofu, tempeh, and occasional additions of carrots and aubergine. "
            "The light rempah (shallots, garlic, galangal, lemongrass, fresh chili, small amount of belacan) is fried in lard, thinly sliced pork belly is added and cooked briefly, then thin coconut milk is added with the vegetables in order of cooking time — hardest vegetables first, leafy greens last.\n\n"
            "The lodeh sauce should remain loose and brothy — this is not a curry and should not be reduced to a thick sauce. "
            "The light aromatics and brothy coconut milk allow the individual flavours of each vegetable to be clearly tasted. "
            "Kristang babi lodeh differs from Malay lodeh primarily through the pork and lard — the technique and vegetable selection are inherited. "
            "Service: poured over rice in a deep bowl, with the broth distributed throughout the grain."
        ),
        "key_principles": (
            "Vegetables added in order of cooking time — hardest first, softest last. "
            "Brothy sauce — not reduced; the liquid character of lodeh is intentional. "
            "Light rempah — less dried chili and no vinegar; milder than kari debal. "
            "Pork belly cut thin — lodeh is a quick-cook dish, not a long braise."
        ),
        "common_mistakes": (
            "Reducing the sauce — produces a curry, not a lodeh. "
            "All vegetables added together — some overcook while others remain raw. "
            "Too much dried chili in the rempah — the mild, brothy quality of lodeh is obscured. "
            "Thick pork cuts — they do not cook through in the lodeh's shorter cooking time."
        ),
        "pro_tips": (
            "Young jackfruit (nangka muda) in babi lodeh is the Kristang-Malay bridge ingredient — it has a meaty, slightly fibrous texture that absorbs the coconut broth and spices beautifully. "
            "The broth from babi lodeh, strained and seasoned, is an excellent base for a Kristang coconut noodle soup. "
            "Adding a bruised stalk of lemongrass and 3-4 kaffir lime leaves to the coconut milk (not the fried rempah) adds a fragrant top note to the finished broth. "
            "Tempeh in Kristang lodeh is fried separately in lard until golden before adding — this produces a crisp exterior that survives the broth and provides textural contrast."
        ),
        "trigger_keywords": json.dumps(["babi lodeh", "Kristang vegetable pork", "Kristang lodeh", "pork coconut broth Malacca", "Malay lodeh pork", "Eurasian vegetable braise", "Malacca everyday pork"]),
        "authority_tier": 1,
        "lives_or_dies": "The broth. Babi lodeh that has been reduced to a thick sauce has lost its identity — it becomes a curry by accident. The broth must be maintained by not over-reducing and by tasting: it should taste clean, fragrant, lightly coconut-sweet, and aromatic without being assertively spiced.",
        "flavour_context": "Light, fragrant, coconut-sweet with aromatic lemongrass and galangal threading through — the most approachable of the Kristang pork preparations. The pork belly fat enriches the coconut broth as it cooks; the vegetables absorb the spiced coconut character and lose their raw edges. Gentle, complete, satisfying."
    },
]

conn = psycopg2.connect(CONN)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

inserted = 0
for e in entries:
    s = slug(e["name"])
    cur.execute("SELECT id FROM technique_references WHERE slug = %s", (s,))
    if cur.fetchone():
        print(f"  ~ SKIP (slug exists): {s[:60]}")
        continue
    cur.execute(
        """INSERT INTO technique_references
           (name, slug, category, origin, description, key_principles, common_mistakes, pro_tips,
            trigger_keywords, authority_tier, lives_or_dies, flavour_context)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (e["name"], s, e["category"], e["origin"], e["description"],
         e["key_principles"], e["common_mistakes"], e["pro_tips"],
         e["trigger_keywords"], e["authority_tier"],
         e.get("lives_or_dies",""), e.get("flavour_context",""))
    )
    row = cur.fetchone()
    if row:
        inserted += 1
        print(f"  ✓ [{row['id']}] {e['name'][:70]}")

conn.commit()
cur.close()
conn.close()
print(f"\nBatch 4 complete: {inserted}/{len(entries)} inserted")
