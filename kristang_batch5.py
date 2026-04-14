#!/usr/bin/env python3
"""Kristang PCT-9 — Batch 5: Seafood Techniques (10 entries)"""
import psycopg2, psycopg2.extras, re, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

entries = [
    {
        "name": "Karang: Kristang stuffed crab technique",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Karang is the Kristang stuffed crab — whole mud crabs or blue swimmer crabs are steamed, cleaned, and the shell used as a vessel for a spiced, aromatic mixture of crab meat, prawn, shallots, garlic, fresh chili, coconut milk, and egg, which is then returned to the shell and grilled or baked until set. "
            "The dish is a direct expression of the Portuguese tradition of using seafood shells as cooking vessels — the Portuguese tradition of 'recheio' (stuffing) applied to the Malaccan crabs of the Straits of Malacca.\n\n"
            "The crab preparation: live mud crabs are killed humanely (spike between the eyes), steamed for 12-15 minutes until cooked, then cooled. "
            "The top shell (carapace) is removed intact and cleaned. "
            "All the crab meat is extracted from the body, claws, and legs — the quantity from a medium crab (500-600g) produces approximately 120-150g of meat. "
            "The filling is made by frying shallots and garlic in coconut oil until translucent, adding sambal berlado (the chili paste), then folding in the fresh crab meat, chopped raw prawns, coconut milk, and beaten egg. "
            "The mixture is seasoned with salt and white pepper, filled back into the cleaned shell, and grilled under a hot broiler or over charcoal for 8-10 minutes until the filling is set and the top is golden.\n\n"
            "The quality markers: the filling should be moist but set, with visible strands of crab meat rather than a homogenous paste. "
            "The shell provides both presentation and a subtle briny additional flavour as it heats. "
            "Over-cooking produces a dry, rubbery filling — the precise point between set and rubbery is the critical skill."
        ),
        "key_principles": (
            "Steam the crab first, extract all meat carefully — the claw meat is valuable and must not be discarded. "
            "Filling should contain visible crab strands, not be a smooth paste. "
            "Egg and coconut milk are the binding agents — too much egg produces a frittata; too little produces a crumbly filling. "
            "Grill until just set — remove immediately; residual heat continues cooking."
        ),
        "common_mistakes": (
            "Over-processing the crab meat — smooth paste rather than visible crab shreds. "
            "Over-cooking during the final grill — dry, rubbery filling. "
            "Insufficient cleaning of the shell — residual gills or dark paste in the shell adds bitterness. "
            "Insufficient seasoning — the crab meat is sweet and requires assertive seasoning to balance."
        ),
        "pro_tips": (
            "Mud crab (ketam batu) is preferred over blue swimmer for karang — denser meat, more flavour, stronger shell for re-stuffing. "
            "Adding finely minced preserved lime rind to the filling is a distinctive Kristang variation — the salty-citrus depth complements the crab sweetness. "
            "The shell must be thoroughly dried before filling — wet shells produce steaming rather than grilling during the final cook. "
            "A small amount of toasted breadcrumb mixed into the surface of the filling before grilling creates a crispy top layer over the soft filling."
        ),
        "trigger_keywords": json.dumps(["karang", "Kristang stuffed crab", "stuffed crab Malacca", "Eurasian crab recipe", "karang Malacca", "stuffed crab shell", "Portuguese stuffed crab"]),
        "authority_tier": 1,
        "lives_or_dies": "The grilling time. The stuffed filling sets within a narrow window — too short and the egg is still runny; too long and the crab meat has contracted to a dry, rubbery mass. Remove from the heat when the filling is just set — a slight wobble is acceptable and will firm as it rests.",
        "flavour_context": "Sweet crab, aromatic from the sambal berlado, rich from the coconut milk, with the egg binding giving a savoury depth — the stuffed crab format concentrates the sweet brininess of the crab and amplifies it with the spice mixture. Each bite delivers the full flavour of the sea in a spiced, textured form."
    },
    {
        "name": "Ikan assam pedas kristang: tamarind sour fish technique",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Ikan assam pedas — sour spiced fish — is perhaps the most widely known dish in the Kristang-adjacent Malay cooking tradition and one of the clearest examples of the Malacca cultural synthesis. "
            "The Kristang version is distinguished from the standard Malay assam pedas by a more assertive tamarind concentration and the use of lard instead of vegetable oil — the dish is sharper, richer, and more deeply aromatic. "
            "It is a daily fish preparation, adaptable to whatever firm fish the morning market offers.\n\n"
            "The preparation: a rempah of dried red chili, shallots, galangal, lemongrass, and belacan is fried in lard until fragrant. "
            "Concentrated tamarind liquid (asam pekat — dark, syrupy) is added with water to create the braising liquid. "
            "Whole fresh okra (lady's fingers), sliced tomatoes, and daun kesum (Vietnamese coriander) are added to the liquid. "
            "Thick fish steaks (Spanish mackerel or red snapper) are added and the pot is covered to steam-braise for 8-10 minutes. "
            "A single bruised whole dried chili is added to the lid interior — not to the sauce — to add gentle background heat without making the dish aggressively hot.\n\n"
            "The sauce should be intensely sour and dark from the tamarind — it should taste almost uncomfortably sour on first encounter, then reveal the sweetness of the fish and the aromatic depth of the rempah as the palate adjusts. "
            "This initial sourness-shock is the characteristic and correct experience of ikan assam pedas. "
            "The okra provides a slight mucilaginous thickness to the sauce; the tomatoes provide fruity acidity; the daun kesum provides a peppery-citrus finish."
        ),
        "key_principles": (
            "Concentrated tamarind (asam pekat) only — thin liquid produces insufficient sourness. "
            "Fish added to the simmering sauce last — no more than 8-10 minutes of cooking. "
            "Daun kesum added in the last 2 minutes — it loses its aromatic quality with extended heat. "
            "The sauce should taste aggressively sour — this is correct, not a mistake."
        ),
        "common_mistakes": (
            "Diluted tamarind — a flat, mildly sour sauce that lacks the defining intensity. "
            "Overcooked fish — disintegrates in the sauce. "
            "Substituting regular coriander for daun kesum — entirely different aromatic profile. "
            "Reducing the sauce too much — loses the brothy character that carries the fish."
        ),
        "pro_tips": (
            "Asam keping (dried tamarind slices) added to the pot alongside asam paste provides a slower-release sourness that deepens the flavour over time. "
            "The correct sour level test: taste the sauce before adding fish — if it makes your jaw tighten and mouth water simultaneously, the sourness is correct. "
            "Okra should retain a slight bite — 5-6 minutes in the sauce is sufficient. "
            "Ikan assam pedas is the Kristang equivalent of a French bouillabaisse in its broth-importance — the sauce must be excellent for the dish to succeed."
        ),
        "trigger_keywords": json.dumps(["ikan assam pedas", "Kristang sour fish", "assam pedas kristang", "Malacca tamarind fish", "Eurasian fish braise", "sour fish Malacca", "daun kesum fish"]),
        "authority_tier": 1,
        "lives_or_dies": "The tamarind concentration. Ikan assam pedas without the right tamarind intensity is a mild fish curry — pleasant but not the dish. The aggressive sourness is not a mistake to be corrected but the defining character of the preparation. Do not reduce the tamarind because it tastes too sour in the pot — it will balance against the fish and vegetables.",
        "flavour_context": "Aggressively sour-forward, then sweet fish and aromatic rempah depth, then the peppery-citrus finish of daun kesum — a sequential flavour experience that starts with a challenge and ends with satisfaction. The sourness is the hook; the aromatic depth is the payoff."
    },
    {
        "name": "Kristang prawn sambal: assam udang technique",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Assam udang is the Kristang tamarind-chili prawn preparation — large prawns (whole or head-on, shell-on) fried in sambal berlado and finished with tamarind liquid to produce a sticky, intensely flavoured coating that combines the sweetness of fresh prawn with the sour-chili complexity of the sambal. "
            "The shell-on preparation is non-negotiable — the shells are part of the eating experience, sucked clean of the sauce before removing the meat, and they contribute a briny depth to the sauce as the dish cooks.\n\n"
            "The prawns are prepared with the shells intact but the backs slit and deveined — the slit back allows the sauce to penetrate into the flesh. "
            "A pre-made sambal berlado (or fresh-fried chili-shallot paste) is heated in lard until sizzling, the prawns are added, and the heat is turned high to produce the characteristic wok-hei effect — the rapid, high-heat caramelisation that Kristang prawn sambal requires for the correct charred-caramelised shell exterior. "
            "Tamarind liquid is added after the initial high-heat sear, reduced quickly to a thick, clinging sauce, and the prawns are tossed to coat.\n\n"
            "The finished prawns should be glossy, deep red-orange, with a thick sauce coating each shell. "
            "The experience of eating assam udang — cracking through the caramelised shell, sucking the sauce from the shell's interior, tasting the sweet prawn meat — is irreducible. "
            "This is a dish that requires hands-on eating; chopsticks and knife-and-fork remove the full experience."
        ),
        "key_principles": (
            "Shell-on, head-on if possible — the shells are part of the dish. "
            "High heat for the initial sear — wok-hei development is essential. "
            "Tamarind added after searing — it reduces quickly and coats the shells. "
            "Serve immediately — the shells soften and lose their texture if held."
        ),
        "common_mistakes": (
            "Shelled prawns — the experience is fundamentally changed and the briny depth from the shells is lost. "
            "Low heat — the prawns steam rather than sear; no caramelisation develops. "
            "Too much tamarind liquid — the sauce does not reduce to a coating and the dish is soupy. "
            "Holding after cooking — the shells soften in the sauce and the texture deteriorates."
        ),
        "pro_tips": (
            "The head-on prawn is preferable — the prawn head fat adds richness to the sauce as it renders during cooking. "
            "After high-heat searing, a teaspoon of palm sugar added with the tamarind produces a more balanced sweet-sour glaze. "
            "King prawns (300g+ size) have sufficient shell thickness to withstand the high-heat sear without overcooking the meat. "
            "The palm sugar in the sauce caramelises at high heat — small dark sticky spots on the shell are the marker of correct caramelisation."
        ),
        "trigger_keywords": json.dumps(["assam udang", "Kristang prawn sambal", "tamarind prawn Malacca", "Eurasian prawn dish", "sambal prawn Kristang", "shell on prawn Malacca", "Malacca prawn technique"]),
        "authority_tier": 1,
        "lives_or_dies": "The heat during the initial sear. Insufficient heat produces steamed prawns in a sauce — correct but not the dish. The right heat produces caramelised, slightly charred shells that add depth to the sauce and a textural contrast to the prawn meat inside. The wok must be hot enough to sear and caramelise before the prawns release their moisture.",
        "flavour_context": "Caramelised prawn shell sweetness, sour-chili sambal depth, tamarind tang — layers of flavour that accumulate in the mouth as you work through the shell. The brine released from the shell interior as you suck adds a raw oceanic dimension that no sauce-only version can replicate."
    },
    {
        "name": "Kristang grilled fish: ikan panggang rempah technique",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Ikan panggang — grilled fish — is the Kristang preparation that most clearly demonstrates the synthesis of Portuguese grilling tradition (whole fish over charcoal) and Malay aromatic technique (rempah marinade). "
            "The fish is marinated in a simplified rempah of shallots, garlic, lemongrass, dried chili, turmeric, belacan, and calamansi juice, then grilled over charcoal on a folded banana leaf that both prevents sticking and infuses the fish with a subtle green-smoky aroma during the final minutes of cooking.\n\n"
            "Fish selection: stingray (ikan pari), Spanish mackerel (batang), or snapper (ikan merah) are the traditional choices. "
            "Stingray in particular is the Kristang ikan panggang signature — the cartilaginous wing section is marinated in the rempah and grilled flat on the banana leaf, producing a preparation that is unlike anything in European cooking and directly expresses the Malay coastline tradition.\n\n"
            "The marinade is spread thickly over all surfaces of the fish or stingray wing and left for minimum 30 minutes (up to 4 hours refrigerated). "
            "The banana leaf is placed directly over charcoal, the fish is placed on the leaf, and grilling proceeds for 8-12 minutes per side depending on thickness — the leaf protects the bottom from direct charcoal heat while the top chars directly. "
            "The fish is basted with additional marinade halfway through. "
            "The banana leaf browns, chars at the edges, and infuses a distinctive waxy-green-smoky note into the bottom of the fish — this aroma is the unmistakeable signature of Kristang and Malay ikan panggang."
        ),
        "key_principles": (
            "Banana leaf is not optional — it provides the characteristic aroma and prevents sticking on charcoal. "
            "Charcoal grill only — gas grill lacks the smoke interaction that is part of the dish. "
            "Baste with marinade during cooking — the repeated application builds flavour layers. "
            "Stingray wing or thick whole fish — thin fillets overcook before the exterior chars."
        ),
        "common_mistakes": (
            "Aluminium foil instead of banana leaf — no aroma infusion, no authentic result. "
            "Gas grill — technically acceptable but loses the charcoal smoke that is part of the dish identity. "
            "Thin fish fillets — they overcook while the rempah is still developing. "
            "Short marination time — the rempah stays on the surface rather than penetrating."
        ),
        "pro_tips": (
            "Banana leaves are available at Asian grocery stores — run over a gas flame briefly to soften and prevent cracking when folded. "
            "Stingray ikan panggang from the hawker centres of Malacca is the definitive benchmark — the combination of the cartilaginous wing, the charred rempah crust, and the banana leaf aroma is irreplaceable. "
            "The banana leaf should be wilted (slightly softened by heat) before use, not fresh and stiff — it needs to fold without breaking. "
            "Serve the grilled fish directly on the banana leaf — it continues to infuse the fish as it rests and provides a visual presentation that is part of the dining experience."
        ),
        "trigger_keywords": json.dumps(["ikan panggang", "Kristang grilled fish", "banana leaf grilled fish", "Malacca grilled fish", "stingray kristang", "charcoal fish Malacca", "ikan pari kristang"]),
        "authority_tier": 1,
        "lives_or_dies": "The banana leaf. Grilled fish without a banana leaf is just grilled fish — technically correct but not ikan panggang. The leaf provides the characteristic aroma (waxy, green, slightly smoky) that is part of the dish's identity. Substituting foil produces an identical taste but removes the experience.",
        "flavour_context": "Charcoal-smoky, rempah-aromatic, slightly sweet from the calamansi, with the waxy-green note of banana leaf underneath — a sensory combination that registers as distinctly Southeast Asian in a way that no other grilling method produces. The stingray wing's dense cartilage soaks up the marinade and releases it slowly as you eat."
    },
    {
        "name": "Sotong masak hitam kristang: squid in ink",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Sotong masak hitam — squid cooked in its own black ink — is a preparation that connects Kristang cooking directly to the Portuguese and Spanish tradition of squid in squid ink (arroz negro, chipirones en su tinta). "
            "The Portuguese brought this technique from the Iberian Peninsula to Malacca in the 16th century, and the Kristang community adapted it with the local spice vocabulary — producing a black sauce of extraordinary complexity: briny from the squid ink, aromatic from the galangal-lemongrass rempah, slightly sweet from coconut milk, and sharp from tamarind.\n\n"
            "The squid ink is harvested from the ink sac during cleaning — the sac is located behind the squid's quill (pen). "
            "Each medium squid produces approximately 1 tablespoon of ink. "
            "Multiple squids should be cleaned for a single dish to collect sufficient ink (minimum 3-4 tablespoons for 500g of squid). "
            "The ink is diluted with a tablespoon of water and reserved. "
            "The squid is cleaned, tubes and tentacles separated, and scored on the inside of the tube (a crosshatch at 5mm intervals) to prevent curling during cooking.\n\n"
            "Cooking: a light rempah (shallots, garlic, lemongrass, fresh chili, belacan) is fried, squid pieces are added and cooked briefly at high heat for 2-3 minutes, then the diluted ink is added along with a small amount of coconut milk and tamarind. "
            "The sauce turns intensely black immediately — a dramatic visual transformation. "
            "Cooking continues for no more than 3-4 additional minutes — squid is tender only in the first 3-4 minutes of cooking or after a long braise of 30+ minutes; the middle zone between 5-25 minutes produces rubbery texture."
        ),
        "key_principles": (
            "Harvest ink from sac carefully — rupture the sac into the reserved bowl, not into the pot. "
            "Cook squid quickly at high heat (2-3 minutes) or very long (30+ minutes) — the middle produces rubber. "
            "Score the inside of the tube — prevents curling and ensures even cooking. "
            "Ink added after the squid initial sear, not at the start."
        ),
        "common_mistakes": (
            "Cooking squid for 10-15 minutes — the rubber zone; inedibly tough texture. "
            "Not scoring the tube — it curls into a tight ball during cooking and cooks unevenly. "
            "Rupturing the ink sac during cleaning — ink in the wrong place, insufficient for the sauce. "
            "Too much coconut milk — dilutes the dramatic black character of the sauce."
        ),
        "pro_tips": (
            "The Portuguese-Kristang connection in this dish is direct: arroz negro (Portuguese/Spanish squid ink rice) and sotong masak hitam use the same fundamental technique — squid cooked in its own ink — adapted to two different culinary traditions. "
            "If insufficient fresh squid ink is available, small amounts of commercial squid ink (available as small packets at specialty food stores) can supplement, though the fresh ink has a more complex briny quality. "
            "Serve sotong masak hitam with steamed white rice — the black sauce against white rice is the visual statement of the dish. "
            "Warn diners: squid ink stains teeth temporarily and permanently stains white fabric."
        ),
        "trigger_keywords": json.dumps(["sotong masak hitam", "squid ink Kristang", "Malacca squid ink", "Portuguese squid ink Malacca", "Eurasian squid dish", "cuttlefish ink", "sotong hitam recipe"]),
        "authority_tier": 1,
        "lives_or_dies": "The squid cooking time. The window between tender and rubber in squid is narrow — cook for no more than 3-4 minutes at high heat. If the squid has been in the pan for 5+ minutes and is still not the texture you want, you are already past the first tender window and must continue cooking for at least 25-30 minutes more to reach the second tender window via collagen breakdown.",
        "flavour_context": "Intensely briny from the ink, aromatic from the rempah, with coconut milk sweetness and tamarind brightness threading through — the most visually dramatic Kristang seafood preparation and one of the most flavour-layered. The black ink sauce coats every grain of rice it touches and makes each mouthful complex."
    },
    {
        "name": "Kristang fish head curry: sour coconut technique",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The fish head curry of the Kristang kitchen is a preparation borrowed from and adapted with the Indian Tamil community of Malacca — one of the clearest examples of the three-way cultural synthesis (Portuguese + Malay + South Indian) that defines Kristang cuisine. "
            "The Kristang version uses a rempah base (rather than pure Indian spice blend), adds tamarind sourness (rather than kokum), and uses lard (rather than coconut oil), while retaining the Indian practice of cooking the fish head whole as the centrepiece — the cheek and collar meat, the lips, and the gelatinous eye socket are all consumed.\n\n"
            "Fish head selection: large red snapper (ikan merah) or grouper (ikan kerapu) heads — a minimum of 600-800g per head to justify the preparation. "
            "The head is cleaned, gills removed, and scored across the cheek. "
            "The rempah is fried with the addition of curry leaves (daun kari) — the Indian Tamil aromatic — which is unusual for Kristang cooking and marks the Indian influence in this specific dish. "
            "Thin coconut milk is added along with tamarind liquid and whole okra. "
            "The fish head is added to the simmering curry and covered for 12-15 minutes.\n\n"
            "The eating experience is essential to understanding the dish: the fish head provides a variety of textures and flavour densities in a single preparation — the flaky cheek meat, the gelatinous collar, the soft eye, and the firm lips all cook at different rates in the same liquid. "
            "Knowing how to navigate a fish head at the table is a Kristang cultural competency."
        ),
        "key_principles": (
            "Minimum 600g fish head — small heads provide insufficient meat for the preparation. "
            "Curry leaves in the rempah — they mark the Indian Tamil influence and are technically essential. "
            "Fish head added to simmering curry — not fried first. "
            "12-15 minutes maximum — the head's cheek meat cooks faster than the collar and lips."
        ),
        "common_mistakes": (
            "Using a small fish head — inadequate meat-to-curry ratio, the liquid overwhelms the protein. "
            "Omitting curry leaves — produces a technically correct Kristang curry but not a Kristang fish head curry. "
            "Over-cooking — the cheek meat dries out while waiting for the collar to cook; serve when the cheek is just done. "
            "Insufficient sourness — the tamarind must be clearly present as a balance to the coconut milk richness."
        ),
        "pro_tips": (
            "The fish eye is a delicacy in Kristang and Malay culture — the gelatinous fluid inside is sweet, briny, and rich. "
            "Scoring the cheek deeply allows the curry sauce to penetrate and flavour the flesh throughout. "
            "Red snapper fish head curry is a benchmark dish across Singapore and Malaysia — the Kristang version with lard rather than coconut oil has a richness that distinguishes it from the standard preparation. "
            "Serve in a deep bowl — the liquid should be visibly present as a soup component of the dish."
        ),
        "trigger_keywords": json.dumps(["Kristang fish head curry", "ikan kepala curry Malacca", "Eurasian fish head", "fish head curry Malacca", "red snapper head Kristang", "Malacca fish head", "curry leaves fish"]),
        "authority_tier": 1,
        "lives_or_dies": "The sourness balance. Fish head curry without sufficient tamarind acidity becomes rich, heavy, and one-dimensional — the tamarind is not just a flavouring but a structural counterweight to the coconut milk and fish oil richness. Taste the curry before adding the fish head — the acid level must already be correct.",
        "flavour_context": "Rich coconut-sour, aromatic with curry leaves and rempah, sweet-briny from the fish head gelatin — the gelatinous collagen from the fish head dissolves into the curry and gives it a body and richness that fillet-based curries cannot achieve. The sourness cuts through the gelatin richness."
    },
    {
        "name": "Kristang cockle preparation: quick-cooked shellfish",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The Kristang preparation of cockles (kerang) is one of the most time-sensitive in the cuisine — cockles must be cooked in the briefest possible exposure to heat (30-60 seconds in very hot water or wok), served immediately, and consumed before the meat toughens. "
            "The Kristang approach to cockles reflects both the Portuguese tradition of quick-cooked shellfish (the Portuguese amêijoas à bulhão pato uses a similar brief-heat technique) and the Malay preference for barely-cooked cockles, where the meat retains a slight rawness.\n\n"
            "Selection and preparation: cockles should be very fresh — alive, tightly closed, smelling of the sea rather than ammoniacal. "
            "They are soaked in salted water for 30 minutes to purge sand, then drained and transferred to a colander or perforated tray. "
            "Cooking: boiling water is poured directly over the cockles in the colander, held for exactly 30-45 seconds, then drained. "
            "The shells should be slightly open at this point — not wide open (overcooked). "
            "Alternatively, in the wok: the cockles are thrown into a very hot dry wok, wok is covered for 60 seconds — the steam within the shells cooks the meat from inside.\n\n"
            "Service and condiment: Kristang cockles are eaten with a dipping condiment of cincalok (or sambal belacan) mixed with calamansi juice and finely sliced bird's eye chili. "
            "The shell is pried open with a toothpick or directly by hand, the cockle meat extracted and dipped before eating. "
            "The slightly raw interior of correctly cooked cockles — warm but not fully cooked through — is the intended experience and a deliberate eating preference."
        ),
        "key_principles": (
            "30-45 seconds only — cockles become rubbery beyond 60 seconds. "
            "Only very fresh cockles — dead cockles should not be eaten; discard any that do not close when tapped. "
            "Purge in salted water before cooking — removes sand from interior. "
            "Serve and eat immediately — cockles toughen rapidly after cooking."
        ),
        "common_mistakes": (
            "Overcooking — rubbery, shrunken meat that has lost its sweet-briny character. "
            "Using doubtful freshness cockles — food safety risk and flavour quality issue simultaneously. "
            "Skipping the purge — gritty, sandy cockles in the mouth. "
            "Serving cold — cockles must be eaten hot from the cooking; cold cockles lose their appeal rapidly."
        ),
        "pro_tips": (
            "The sweet, briny, slightly metallic flavour of fresh cockle meat is the target — any off-flavour or blandness indicates old or dead stock. "
            "The cincalok dipping condiment for cockles is the definitive Kristang pairing — the fermented-acid sharpness of the condiment amplifies the brininess of the cockle. "
            "Blood cockles (kerang darah — the larger, blood-red variety) are the premium cockle for Kristang eating — richer flavour, larger meat, more dramatic presentation. "
            "In Malacca hawker culture, cockles appear in char kway teow — but the Kristang kitchen traditionally serves them as a standalone appetiser with condiment."
        ),
        "trigger_keywords": json.dumps(["Kristang cockles", "kerang Malacca", "cockle preparation", "quick cooked shellfish", "kerang darah", "Malacca cockles", "Kristang shellfish"]),
        "authority_tier": 1,
        "lives_or_dies": "30 seconds. This is the only window. Cockles that have been in heat for 60 seconds are already deteriorating toward rubber. The correct timing is when the shell has just barely opened — the meat inside is warm but still slightly translucent at the centre. Remove from heat immediately.",
        "flavour_context": "Sweet, briny, clean — fresh cockle flavour is direct and marine without complexity. The interest comes from the condiment: cincalok's fermented depth against the cockle's raw-ocean sweetness creates a contrast pairing of unusual elegance. The texture is the feature: soft, yielding, with a slight resistance that marks barely-cooked perfection."
    },
    {
        "name": "Kristang dried prawn paste: hae bi preparation",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Dried shrimp (hae bi in Hokkien, udang kering in Malay) is a dried, salted seafood seasoning used in Kristang cooking as a secondary umami layer in stir-fries, fried rice, sambal, and vegetable preparations. "
            "Its use in the Kristang kitchen reflects the multi-community culinary exchange of Malacca — dried shrimp is primarily a Chinese Hokkien pantry ingredient, but it entered the Kristang kitchen through centuries of community proximity and is now as naturalised in Kristang cooking as belacan.\n\n"
            "Selection: good dried shrimp are bright orange-pink, firm but not brittle, and smell intensely of dried seafood without off-notes. "
            "They should be uniform in size and whole, not fragmented. "
            "Poor-quality dried shrimp are grey, smell musty or of ammonia, and produce a flat flavour rather than the sweet-saline umami depth of quality product.\n\n"
            "Preparation for Kristang use: dried shrimp are soaked in warm water for 5-10 minutes to rehydrate slightly (this makes grinding easier), then drained and pounded or processed to the required texture. "
            "Coarsely pounded: used in sambal goreng and stir-fries where visible shrimp pieces are wanted. "
            "Finely ground: used in fried rice and certain curry pastes where texture is not desired. "
            "Toasted whole: added directly to stir-fries for a nutty, crunchy texture element. "
            "The Kristang method of frying dried shrimp in lard until golden before adding to dishes — rather than adding raw — produces a more complex, nutty umami depth."
        ),
        "key_principles": (
            "Soak briefly before grinding — dried shrimp too dry to pound smoothly. "
            "Quality check before use — grey, ammonia-smelling dried shrimp ruins any dish. "
            "Fry in lard before using as a flavouring — raw dried shrimp tastes flat; fried develops Maillard complexity. "
            "Different textures serve different applications — choose appropriate preparation for the dish."
        ),
        "common_mistakes": (
            "Using poor quality, grey dried shrimp — musty, flat flavour that adds nothing. "
            "Not soaking before grinding — impossible to achieve fine texture; produces irregular lumps. "
            "Adding raw to finished dishes — lacks the nutty development of fried dried shrimp. "
            "Too much in the dish — dried shrimp is intensely flavoured; a small quantity is usually sufficient."
        ),
        "pro_tips": (
            "The best-quality dried shrimp from Malaysia or Thailand has a natural sweetness beneath the saline intensity — this sweetness is what makes it valuable in cooking. "
            "Lard-fried dried shrimp stored in an airtight jar keeps at room temperature for 2 weeks and can be used as needed as a finishing element. "
            "The Kristang combination of dried shrimp and belacan in a single rempah (used in certain Kristang fried rice) creates a double-fermented-seafood umami base of unusual depth. "
            "Dried shrimp in stir-fried vegetable preparations (kang kong with dried shrimp, kangkong belacan) is one of the foundational Malaysian-Kristang vegetable techniques."
        ),
        "trigger_keywords": json.dumps(["dried shrimp", "hae bi", "udang kering Malacca", "Kristang dried prawn", "dried shrimp paste", "udang kering preparation", "Malacca dried shrimp"]),
        "authority_tier": 1,
        "lives_or_dies": "The frying. Dried shrimp added raw to a dish contributes a flat, one-dimensional saltiness. Dried shrimp fried in lard until golden contributes a nutty, complex, caramelised-seafood depth that is the actual ingredient. The frying is the activation step.",
        "flavour_context": "Intensely saline, sweet-oceanic, with a nutty-caramelised depth when fried — dried shrimp concentrates the flavour of fresh shrimp into a small, shelf-stable ingredient. In a dish, it is not identifiable as 'shrimp' — it reads as 'deep umami'. Its presence is noticed most obviously by its absence."
    },
    {
        "name": "Kristang steamed fish: Portuguese influence on gentle cooking",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The Kristang tradition of steaming whole fish reflects both the Portuguese approach of preserving fish flavour through gentle cooking and the Malay-Chinese practice of steaming as a primary fish technique. "
            "The Kristang version is distinguished by the use of rempah-based aromatics (rather than Chinese soy-ginger or plain salt) and the finishing with sambal berlado oil and calamansi — the combination produces a steamed fish with a distinctly Kristang aromatic signature.\n\n"
            "Preparation: whole fish (snapper, grouper, or sea bass — whole fish preferred over fillets for steaming) is scored 3-4 times deeply on each side. "
            "A paste of finely pounded shallots, garlic, lemongrass, and fresh turmeric is rubbed into the scored flesh and cavity. "
            "The fish is placed on a banana leaf in a steamer and steamed for 10-14 minutes depending on size (500g fish = 12 minutes). "
            "After steaming, hot sambal berlado oil (berlado paste fried in lard until sizzling) is poured directly over the fish — the hot oil crackles over the aromatics and steamed flesh, creating a secondary 'sear' effect. "
            "Fresh calamansi is squeezed over immediately and the dish is served.\n\n"
            "The two-stage cooking (steam + hot oil pour) is the defining Kristang technique — it produces a fish that is simultaneously moist and tender from steaming and aromatic and slightly crisped on the scored surface from the hot oil contact."
        ),
        "key_principles": (
            "Score deeply — the rempah and subsequent aromatics penetrate through the scores. "
            "Steam timing: 12 minutes per 500g as a baseline, adjusted for thickness. "
            "Hot oil pour immediately after steaming — the sizzle is the technique; the oil must be near-smoking hot. "
            "Calamansi added last, after the oil pour — heat destroys the fresh citrus volatile."
        ),
        "common_mistakes": (
            "Insufficient scoring — aromatics stay on the surface. "
            "Over-steaming — dry, flaky fish with no moisture retention. "
            "Cool oil pour — no sizzle effect, no aromatic activation. "
            "Adding calamansi before serving — the acid is destroyed by steam heat if added too early."
        ),
        "pro_tips": (
            "The hot oil pour technique is shared with Chinese steamed fish preparations (hot oil poured over scallion and ginger) — the Kristang version substitutes sambal berlado oil for the soy-ginger Chinese version, demonstrating parallel technique evolution. "
            "Insert a chopstick through the thickest part of the fish to test doneness — it should go through without resistance but the flesh should not yet be flaking from the bone. "
            "The banana leaf under the fish during steaming adds a subtle green-waxy note — not essential but traditional. "
            "Scored whole fish steamed this way and served at a Kristang table signals the cook's confidence — a whole fish requires more skill than fillets and is a traditional hospitality presentation."
        ),
        "trigger_keywords": json.dumps(["Kristang steamed fish", "ikan kukus kristang", "steamed fish Malacca", "Portuguese steamed fish", "hot oil fish", "Kristang fish technique", "Malacca whole fish"]),
        "authority_tier": 1,
        "lives_or_dies": "The temperature of the oil at the pour. If the oil is merely warm when poured over the fish, there is no sizzle, no aromatic activation, and no secondary crisping effect — the technique simply does not work. The oil must be near-smoking and poured from height to create the maximum contact sizzle.",
        "flavour_context": "Clean steamed sweetness of fresh fish, then the sharp aromatic blast of the hot sambal oil activating against the steamed flesh — chili-shallot-garlic in hot fat. The calamansi cuts through both and unifies the experience with a bright citrus top note. Three distinct stages in a single preparation."
    },
    {
        "name": "Kristang squid fritters: cumi goreng tepung",
        "category": "Kristang — Seafood Techniques",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Cumi goreng tepung — battered fried squid — is the Kristang everyday fried seafood preparation, reflecting both the Portuguese tradition of battered and fried seafood (peixinhos da horta, fritos de peixe) and the local hawker tradition of crispy fried snacks. "
            "The Kristang version is distinguished by the batter composition (rice flour and tapioca flour rather than wheat flour alone) and the seasoning of the squid itself with a small amount of belacan and white pepper before battering.\n\n"
            "The squid preparation: medium squid are cleaned, the skin can be left on or removed (removing it produces a more visually clean result; leaving it on adds a slight chewiness and colour). "
            "The tubes are scored inside and cut into rings; the tentacles are separated. "
            "The squid is marinated for 15 minutes in a mixture of belacan (1/4 teaspoon per 300g squid, dissolved in a teaspoon of water), white pepper, and salt.\n\n"
            "The batter: rice flour (60%), tapioca flour (30%), and wheat flour (10%) combined with very cold sparkling water to produce a thin, light batter. "
            "The rice and tapioca flours produce a distinctly different result from a wheat-only batter — lighter, crispier, and less prone to sogginess on standing. "
            "The squid pieces are lightly dusted in plain rice flour before dipping in batter — the dusting creates a micro-layer that helps the batter adhere and prevents steam pockets. "
            "Frying at 180°C for 2-3 minutes per batch until pale golden and crispy."
        ),
        "key_principles": (
            "Rice and tapioca flour batter — not wheat-only; the different starches produce a lighter, crispier result. "
            "Very cold sparkling water for the batter — the temperature and CO2 produce lightness. "
            "Dust in rice flour before battering — improves adhesion and prevents sogginess. "
            "Fry in small batches — the oil temperature must recover between batches."
        ),
        "common_mistakes": (
            "Wheat-only batter — heavier, less crispy, soggier on standing. "
            "Warm batter liquid — promotes gluten development in the wheat component, making the batter tough. "
            "Large frying batches — oil temperature drops; the batter absorbs more oil and becomes soggy. "
            "Over-marination — too much belacan produces an aggressively fishy taste."
        ),
        "pro_tips": (
            "The belacan in the squid marinade is the Kristang touch — it adds depth and complexity to what would otherwise be a standard battered squid. "
            "Serve with sambal berlado or cincalok condiment — both are traditional Kristang accompaniments. "
            "The mixed flour batter technique is widely used in Malaysian Chinese and Kristang frying — the rice flour provides crispness; the tapioca flour provides transparency; the wheat flour provides just enough structure. "
            "Rest the fried squid on a rack, not paper towels — paper towels trap steam underneath and promote sogginess on the base."
        ),
        "trigger_keywords": json.dumps(["cumi goreng tepung", "Kristang fried squid", "squid fritters Malacca", "battered squid Kristang", "Eurasian fried squid", "Malacca fried seafood", "rice flour squid batter"]),
        "authority_tier": 1,
        "lives_or_dies": "The oil temperature at the start of each batch. Temperature is everything in frying. Under-temperature produces oil-saturated, soggy batter that never achieves crispness. Correct temperature (180°C) produces an immediate sizzle and set of the batter exterior, trapping steam inside and creating lightness.",
        "flavour_context": "Crispy, light batter giving way to tender squid with a slight belacan-umami depth in the meat — the batter is neutral; the flavour interest comes from the seasoned squid and the dipping condiment. The rice-tapioca batter contributes a clean crispness without the heaviness of wheat batter."
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
print(f"\nBatch 5 complete: {inserted}/{len(entries)} inserted")
