#!/usr/bin/env python3
"""Kristang PCT-9 — Batch 3: Curry & Spice Pastes (12 entries)"""
import psycopg2, psycopg2.extras, re, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

entries = [
    {
        "name": "Kari debal: Kristang Devil's Curry technique",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Kari debal — Devil's Curry — is the signature preparation of the Kristang culinary canon: a fiercely complex, deep-red, vinegar-bright curry of meat (traditionally pork, chicken, or leftover Christmas meats) in a thick spice paste that synthesises the Portuguese colonial tradition of using vinegar as a cooking acid with the Malay rempah system of ground rhizomes and dried chilies. "
            "The name 'devil' refers not to heat but to the assertive complexity and the deep red colour — a curry that makes its presence unambiguously known.\n\n"
            "The curry paste (rempah debal) is distinguished by two features absent from standard Malay curries: white or black mustard seeds (a Portuguese influence, possibly via Goa and the Indian trading network), and white vinegar added during the frying of the rempah — not as a finishing acid but as an integral cooking component that caramelises into the paste. "
            "The vinegar contributes a roundness and depth that tamarind cannot replicate — it is the defining flavour marker that makes kari debal unmistakably Kristang rather than Malay. "
            "The meats traditionally used are leftovers — pork, chicken, sausage — which take on the complex marinade of the curry paste over a slow braise.\n\n"
            "Service: kari debal is the centrepiece of the Kristang Christmas table, served on 26 December as the Boxing Day dish using Christmas Day roast meats. "
            "It is not a delicate dish — it is assertively seasoned, deeply coloured, and served in generous portions with white rice or bread. "
            "The professional standard: the sauce should be thick enough to coat a spoon without running off, dark red-brown with flecks of chili and whole mustard seeds, and aromatic enough to be identifiable from across the kitchen."
        ),
        "key_principles": (
            "Add white vinegar during rempah frying — not at the end as a finishing acid but as an integral cooking component. "
            "Mustard seeds are toasted whole in fat before adding the paste — they must pop before the paste goes in. "
            "Long, slow braise develops the collagen and allows the rempah to fully penetrate the meat. "
            "The sauce reduces to thick coating consistency — not a broth, not a gravy, but a clinging paste-sauce."
        ),
        "common_mistakes": (
            "Skipping the vinegar in the rempah frying — produces a technically correct Malay curry but not kari debal. "
            "Adding vinegar at the end — provides sourness without the deep caramelised roundness of vinegar cooked into the paste. "
            "Under-reducing — a thin sauce loses the clinging quality that makes Devil's Curry satisfying. "
            "Using fresh chilies for the primary heat — the dried chili base is essential for depth and colour."
        ),
        "pro_tips": (
            "Traditionally made with the previous day's roast meats — the already-cooked protein absorbs the rempah more efficiently than raw meat. "
            "The vinegar quantity: approximately 2 tablespoons of white vinegar per 500g of rempah paste, added after the paste has fried for 5 minutes. "
            "Mustard seeds should be yellow/white, not black — white mustard seeds are milder and specifically correct for kari debal. "
            "The colour test: the finished sauce should be the colour of dark terracotta — not orange (undercooked paste) and not brown (scorched or over-soy-sauce)."
        ),
        "trigger_keywords": json.dumps(["kari debal", "Devil's Curry", "Kristang devil curry", "Malacca devil curry", "Christmas curry Malacca", "Eurasian curry vinegar", "kari kristang"]),
        "authority_tier": 1,
        "lives_or_dies": "The vinegar integration during rempah frying. Add it too late and the dish tastes like a Malay curry with vinegar drizzled on top. Add it correctly — mid-fry, while the paste is still hot and active — and it caramelises into the paste, creating a roundness and depth that is unmistakably Devil's Curry. The difference is not subtle.",
        "flavour_context": "Deep, layered, complex — initial heat from the dried chili base, then the sharp aromatic brightness of galangal and lemongrass, then the rounded vinegar depth, then a lingering warmth from mustard seeds. Richer and more complex than standard Malay curry. Each mouthful reveals something new."
    },
    {
        "name": "Kari debal rempah: Devil's Curry spice paste construction",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The rempah for kari debal is the most complex paste in the Kristang system — a 12-15 ingredient construction that integrates the standard Malay aromatic base (galangal, lemongrass, shallots, garlic, dried chili, belacan, turmeric, candlenut) with the distinctively Kristang additions of fresh ginger, lemon zest or preserved lime, and the Portuguese-derived mustard seeds. "
            "The paste is ground to a very smooth consistency — smoother than standard Malay rempah — because the longer braise requires a paste that integrates completely into the sauce rather than remaining as visible grained particles.\n\n"
            "Grinding sequence: (1) dried and soaked chilies with turmeric and candlenut; (2) galangal and lemongrass; (3) fresh ginger; (4) shallots and garlic; (5) belacan; (6) optional: a small piece of fresh lemon zest or preserved lime rind. "
            "The paste should be ground finer than standard rempah — use a blender for final passes if using a mortar, adding minimal water. "
            "The finished paste is deep red with an orange undertone from the turmeric, and smells of overlapping citrus (lemongrass, lime), earth (galangal, turmeric), heat (chili), and sea (belacan).\n\n"
            "Frying the rempah: in lard, over medium heat, until the paste breaks from the oil and the colour deepens from orange-red to terracotta. "
            "The vinegar addition (2 tablespoons white vinegar) is made at the 5-minute mark of frying — the paste sizzles loudly as the vinegar contacts the hot fat, then subsides as the acidity cooks in. "
            "Continue frying for 3-4 more minutes after the vinegar addition until the paste is deeply fragrant and the colour has deepened further."
        ),
        "key_principles": (
            "Grind finer than standard rempah — the long braise requires complete paste integration. "
            "Vinegar is added mid-fry at the 5-minute mark, not at the end. "
            "Lemon zest or preserved lime is optional but adds a floral-citrus dimension characteristic of the finest kari debal. "
            "The colour indicator: correct fried rempah debal is deep terracotta, not orange."
        ),
        "common_mistakes": (
            "Grinding too coarse — visible paste particles that do not dissolve during braising. "
            "Too much vinegar in the paste — overpowering sourness that dominates rather than deepens. "
            "Omitting fresh ginger — loses the bright-sharp counterpoint to galangal's camphor depth. "
            "Frying at too high a temperature — the paste burns before the vinegar can integrate."
        ),
        "pro_tips": (
            "A small piece of candle nut (2-3 extra nuts) in kari debal rempah produces a creamier paste that integrates better into the long-braised sauce. "
            "The lemon zest variation is believed to be Portuguese in origin — Malaccan Portuguese used the Mediterranean citrus tradition of adding zest to spiced meat dishes. "
            "Make rempah debal in large batches — it freezes exceptionally well and is one of the most time-consuming preparations in the cuisine. "
            "The paste is correctly fried when you can hear the fat 'talking quietly' — a gentle, consistent sizzle rather than aggressive spattering."
        ),
        "trigger_keywords": json.dumps(["rempah debal", "Devil's Curry paste", "kari debal spice paste", "Kristang curry paste", "Malacca curry paste construction", "debal rempah recipe", "Eurasian rempah"]),
        "authority_tier": 1,
        "lives_or_dies": "The fineness of the grind. A rempah debal that has not been ground sufficiently smooth will never fully dissolve into the braise — there will be gritty paste particles in the sauce that announce under-processed paste. Touch a small amount between the fingers: it should feel smooth with the faintest grain, like very fine cornmeal.",
        "flavour_context": "Red-complex, citrus-aromatic, vinegar-deep, earthy — all the dimensions of the Southeast Asian aromatic vocabulary (galangal, lemongrass, turmeric) plus the Portuguese contribution (vinegar, ginger, possibly lemon zest). No single note dominates; the balance is the point."
    },
    {
        "name": "Batata baje: Kristang potato curry technique",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Batata baje is the Kristang potato curry — a gentler, more restrained preparation than kari debal that showcases how the Eurasian kitchen adapted the potato (a New World crop that arrived via Portuguese colonial trade routes) into the Southeast Asian spice framework. "
            "The dish is one of the clearest examples of the Portuguese-Malay synthesis: the potato (Portuguese 'batata') is cooked in a coconut milk-based Malay curry sauce.\n\n"
            "The rempah for batata baje is lighter than kari debal — fewer dried chilies, no vinegar, a softer aromatic profile with emphasis on fresh turmeric, shallots, lemongrass, and a small amount of curry powder (the Indian influence visible in the Kristang kitchen). "
            "Potatoes are cut into large chunks (4-5cm), parboiled until just resistant to a skewer, then added to the fried rempah with thin coconut milk and simmered until the sauce thickens and the potato is fully cooked through. "
            "Thick coconut milk is added in the last 5 minutes for richness and a smooth finish.\n\n"
            "The dish often includes long beans (kacang panjang), sliced at an angle and added 5 minutes before the end — they should remain crisp-tender. "
            "Ikan masin (salted dried fish) is sometimes crumbled over the finished dish as a savoury garnish. "
            "The finished batata baje should have a sauce that is firmly golden-yellow (from the turmeric), moderately thick, and fragrant with lemongrass and kaffir lime — a direct, honest curry with no pretensions and great depth."
        ),
        "key_principles": (
            "Parboil potatoes before adding to curry — raw potato added to curry liquid produces uneven cooking. "
            "Use large potato chunks — small pieces disintegrate and muddy the sauce. "
            "Add thick coconut milk only in the final 5 minutes — early addition causes emulsion break. "
            "Long beans added at the end only — they should remain vibrant green and crisp-tender, not yellow and soft."
        ),
        "common_mistakes": (
            "Small potato dice — they disintegrate into the sauce before fully absorbing the spice flavours. "
            "Adding thick coconut milk too early — sauce breaks and becomes greasy. "
            "Overcooking the long beans — they lose their colour and become stringy. "
            "Insufficient fried rempah — the curry tastes flat and raw rather than richly aromatic."
        ),
        "pro_tips": (
            "Waxy potatoes (Desiree, Charlotte, Dutch Cream) hold their shape better in the curry than floury varieties. "
            "The colour test: correct batata baje is golden-yellow from fresh turmeric — if it looks pale yellow or cream, there is not enough turmeric or the turmeric is old. "
            "A pinch of palm sugar added with the thin coconut milk rounds the sourness of the tamarind and produces a more balanced flavour. "
            "Batata baje is better the next day — the potato continues to absorb the rempah flavours overnight and the sauce deepens."
        ),
        "trigger_keywords": json.dumps(["batata baje", "Kristang potato curry", "Eurasian potato curry", "Malacca potato curry", "batata kristang", "coconut milk potato", "Portuguese potato Malay"]),
        "authority_tier": 1,
        "lives_or_dies": "The potato texture. Potatoes that dissolve into the curry produce a thick, starchy sauce that tastes heavy and defeats the purpose of the dish. Each chunk should hold its shape while being completely cooked through — yielding under pressure but not collapsing. This requires parboiling to the right point: resistant to a skewer but not raw-hard.",
        "flavour_context": "Golden-turmeric warmth, coconut sweetness, lemongrass brightness, a gentle heat from the chili base — a more approachable curry than kari debal with a round, creamy quality. The potato absorbs the sauce and carries the aromatics through its interior, so each chunk delivers a full taste of the curry with every bite."
    },
    {
        "name": "Kari kapitan: Kristang chicken curry technique",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Peranakan and Kristang tradition, Malacca and Penang, Malaysia",
        "description": (
            "Kari kapitan — Kapitan's Curry — is a chicken curry of the Straits Settlements, claimed by both Nyonya (Peranakan Chinese) and Kristang kitchens, with enough cross-community exchange in the history of Malacca that the distinction is productive rather than exclusionary. "
            "The Kristang version is slightly less sweet and more vinegar-influenced than the Nyonya version, with lard replacing the Nyonya use of coconut oil and a slightly more pronounced belacan character.\n\n"
            "The rempah includes the standard aromatic base (dried chili, shallots, garlic, galangal, lemongrass, turmeric, candlenut) plus a distinctive use of coriander seed (ketumbar) ground fresh — the coriander is toasted and added with the dried chili in the first grinding stage. "
            "The name 'Kapitan' refers to the Portuguese-Malay merchant leader (Kapitan China or Kapitan Cina) of the Malacca trading community — the curry is said to have been developed to serve at the Kapitan's table and reflects the elevated standards of the Straits merchant class.\n\n"
            "Chicken on the bone is essential — bone-in pieces release collagen during the braise, thickening the sauce naturally and contributing body that boneless chicken cannot provide. "
            "The chicken is jointed, browned in lard, then simmered in the fried rempah and coconut milk until the sauce reduces to a glossy, thick, deeply coloured coating. "
            "Fresh calamansi juice is added at the end — a few squeezes that brighten the entire dish and cut through the richness."
        ),
        "key_principles": (
            "Bone-in chicken only — the collagen from bones thickens the sauce and adds body. "
            "Brown the chicken in lard before adding to the curry — creates Maillard flavour on the skin. "
            "Toast and grind coriander fresh — stale pre-ground coriander produces a flat, dusty curry. "
            "Calamansi juice added at the very end, off the heat — acid brightening."
        ),
        "common_mistakes": (
            "Boneless chicken — sauce remains thin and lacks body. "
            "Skipping the browning step — the curry lacks the layered Maillard complexity. "
            "Pre-ground coriander — flat, dusty taste. "
            "Adding calamansi too early — the acid is destroyed by heat; all brightness is lost."
        ),
        "pro_tips": (
            "The coriander seed quantity is approximately 1 teaspoon per batch of rempah — enough for the toasty-citrus note to register without dominating. "
            "Kari kapitan should have a visible oil ring at the surface — this signals that the coconut milk has reduced properly and the fat has separated. "
            "Serve with prawn crackers (keropok) alongside — a traditional Kristang and Nyonya accompaniment that provides textural contrast. "
            "The calamansi lime is non-negotiable as a finishing acid — substituting lemon juice changes the flavour profile significantly."
        ),
        "trigger_keywords": json.dumps(["kari kapitan", "kapitan curry", "Kristang chicken curry", "Malacca chicken curry", "Nyonya kapitan", "Straits curry chicken", "captain curry Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "The calamansi at the end. Without it, kari kapitan is a good chicken curry. With it — a few quick squeezes off the heat — the richness lifts, the aromatics brighten, and the dish becomes complete. It is a small addition with an outsized effect.",
        "flavour_context": "Rich coconut base, aromatic chili-galangal depth, toasted coriander warmth, then the finishing brightness of calamansi — a four-part flavour sequence that moves from rich to bright. The oil ring at the surface is part of the aesthetic and tells the diner that they are eating something properly made."
    },
    {
        "name": "Gulai kristang: Eurasian coconut braise technique",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Gulai kristang is the Eurasian coconut-based braise — a technique of cooking protein (fish, chicken, or vegetables) in a spiced coconut milk broth that is richer and more aromatic than standard Malay gulai but less complex and reduced than a curry. "
            "The 'gulai' refers to the sauce consistency: looser than a curry, with visible broth character, but still aromatically substantial.\n\n"
            "The rempah for gulai kristang uses a lighter hand than kari debal — fewer dried chilies, more fresh turmeric, and often the addition of fresh lemongrass stalks rather than just the ground paste. "
            "Fish or chicken is added raw to the rempah after frying (not pre-browned), and thin coconut milk is added to create the broth. "
            "The protein simmers in the aromatic broth for 15-25 minutes, then thick coconut milk is stirred in and the heat is lowered to prevent breaking. "
            "Daun kesum (Vietnamese coriander / laksa leaf) is the finishing herb in many Kristang gulai — its peppery, slightly citrus character is different from regular coriander and important to the dish's identity.\n\n"
            "Gulai kristang is not a simplified curry — it is a different dish with a different function at the table. "
            "Served in a bowl with the broth visible, it is eaten by pouring over rice and letting the aromatic liquid carry through the grain. "
            "The broth character is the feature — not reduced, not thickened to gravy, but clearly liquid and aromatic."
        ),
        "key_principles": (
            "Do not pre-brown the protein — gulai uses raw protein added to the fried rempah, producing a gentler, more integrated flavour. "
            "Keep the sauce loose — gulai is not reduced like curry; the liquid character is intentional. "
            "Daun kesum is the correct finishing herb where authentic — it is not optional. "
            "Do not boil after adding thick coconut milk — lower heat to a gentle simmer."
        ),
        "common_mistakes": (
            "Over-reducing — gulai reduced to curry consistency loses its broth character. "
            "Pre-browning protein — changes the texture and flavour profile away from gulai to curry. "
            "Substituting regular coriander for daun kesum — different aromatic profile. "
            "Boiling vigorously after thick coconut milk addition — breaks the emulsion."
        ),
        "pro_tips": (
            "Gulai is an excellent technique for firm fish (batang/Spanish mackerel, kembung/Indian mackerel) — the loose broth cooks the fish gently without drying. "
            "The Kristang gulai broth, cooled and strained, makes an excellent base for coconut soup or a laksa broth. "
            "Fresh turmeric root produces a more vivid, slightly earthy flavour than powder — essential for gulai where the turmeric is a featured flavour. "
            "Serve in deep bowls rather than plates — the broth must be visible as part of the dish presentation."
        ),
        "trigger_keywords": json.dumps(["gulai kristang", "Kristang coconut braise", "Eurasian gulai", "Malacca coconut curry broth", "gulai ikan kristang", "loose coconut curry", "daun kesum kristang"]),
        "authority_tier": 1,
        "lives_or_dies": "The sauce consistency decision. A gulai that is over-reduced becomes a curry — entirely valid as a dish, but no longer a gulai. The deliberate choice to stop the reduction while the sauce is still brothy and pourable is the discipline that defines the technique.",
        "flavour_context": "Aromatic, lightly spiced, coconut-forward broth — the gentler, more liquid face of Kristang curry work. The turmeric gives colour and earthy warmth; the lemongrass provides fresh citrus lift; the coconut milk provides richness without heaviness. The daun kesum finishing herb adds a peppery-citrus top note."
    },
    {
        "name": "Tumis rempah: Kristang paste frying activation",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Tumis — the frying of rempah in fat to activate and develop its aromatic compounds — is the most important single technique in Kristang curry cooking and the step most often executed incorrectly by those unfamiliar with Southeast Asian cooking. "
            "The transformation from raw, pungent, harsh paste to fragrant, complex, rounded rempah happens entirely in the tumis stage; no amount of subsequent braising or simmering corrects an under-tumis paste.\n\n"
            "The process: lard or oil is heated in a wok or heavy pot until shimmering. The rempah is added all at once and spread across the hot surface. "
            "The paste immediately sizzles and spits — this violent initial reaction is expected. "
            "The cook stirs continuously, scraping the paste from the bottom and turning it to prevent burning, while monitoring the colour and smell. "
            "The process takes 8-12 minutes over medium heat. "
            "In the first 3-4 minutes, the paste releases water and the high moisture content produces steam. "
            "In minutes 4-8, the water evaporates and the actual frying begins — the temperature rises and the Maillard reactions start. "
            "In minutes 8-12, the paste 'breaks' (pecah minyak) — the oil separates from the paste, pooling around it, and the paste turns from an orange-red to a deeper terracotta. At this point, the aromatics are correctly activated.\n\n"
            "The smell indicator is the most reliable guide: raw rempah smells sharp, pungent, and harsh (raw shallots, raw galangal). "
            "Half-cooked rempah smells cooked but one-dimensional. "
            "Correctly tumis rempah smells complex, sweet, and deeply aromatic — a unified whole rather than identifiable individual components. "
            "This smell transformation is the clearest signal that tumis is complete."
        ),
        "key_principles": (
            "Continuous stirring — the paste burns in seconds if left unattended on a hot surface. "
            "Medium heat, not high — high heat causes rapid browning on the outside while the paste interior remains raw. "
            "Wait for pecah minyak (oil separation) — the visual signal that sufficient water has been driven off and frying is complete. "
            "Follow the smell, not just the clock — some pastes take longer depending on water content."
        ),
        "common_mistakes": (
            "Insufficient tumis time — raw shallot and garlic flavour survives into the finished curry. "
            "Too high heat — burns the surface before the interior cooks, producing scorched rempah. "
            "Leaving the paste unattended — guaranteed burning in 30-60 seconds at tumis temperatures. "
            "Adding protein or liquid before pecah minyak — prematurely halts the frying and leaves the paste under-activated."
        ),
        "pro_tips": (
            "Add 1-2 tablespoons of water if the paste starts to dry too fast (before pecah minyak) — this extends the tumis window and prevents burning. "
            "The wok is preferred over a saucepan for tumis — the large surface area allows faster evaporation and better heat distribution. "
            "For very large batches, tumis in two stages — the paste needs room to fry rather than steam. "
            "A few curry leaves (daun kari) thrown in during the last 2 minutes of tumis add a distinct aromatic dimension specific to South Indian-influenced Kristang cooking."
        ),
        "trigger_keywords": json.dumps(["tumis", "pecah minyak", "rempah frying", "Kristang paste activation", "frying spice paste", "Malay tumis technique", "rempah fry Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "Pecah minyak — the moment the oil separates from the paste. Before this point, the paste is still under-cooked — it smells good but the raw aromatic compounds haven't fully developed. After this point, the window to add liquid is short before the paste starts to scorch. The separation is the green light, not just the target.",
        "flavour_context": "Before tumis: harsh, raw, pungent. After correct tumis: complex, sweet, deeply aromatic, unified. The transformation is total and irreversible. A well-tumis rempah fills a kitchen with the smell of Southeast Asian cooking in a way that no other technique produces."
    },
    {
        "name": "Dry Kristang curry: concentrated spice crust technique",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The dry Kristang curry — a preparation where the braise liquid is completely reduced until the sauce disappears and the spice paste forms a concentrated, caramelised crust on the protein — is the most technically demanding version of the Kristang curry system. "
            "It requires continuous monitoring during the reduction stage and produces a dish of extraordinary intensity — each piece of meat coated in a thick, fragrant, slightly caramelised spice crust.\n\n"
            "The technique begins identically to a wet curry: rempah is fried, protein is added, coconut milk is added, and the dish braises for the appropriate time. "
            "At the point where a wet curry would be finished, the dry curry cook increases the heat and removes the lid, allowing the liquid to reduce aggressively. "
            "As the liquid reduces, the spice paste concentrates on the protein surface. "
            "When almost all liquid has evaporated, the heat must be lowered to prevent burning — the paste will start to fry directly in the rendered fat from the protein and the remaining coconut oil. "
            "This second frying stage crisps and caramelises the spice crust without burning it.\n\n"
            "The dry Kristang curry is most commonly made with pork belly or chicken thighs — proteins with sufficient fat to survive the reduction stage without drying. "
            "Lean proteins (fish, prawns) are not suitable for this technique — they will overcook and dry out before the sauce reduces. "
            "The finished dish should have minimal sauce — only the concentrated spice crust coating each piece, with perhaps a tablespoon of rendered oil at the bottom of the pan."
        ),
        "key_principles": (
            "Start as a wet curry and reduce actively — never start with insufficient liquid. "
            "Reduce heat as liquid evaporates — the remaining paste will burn easily without the moisture buffer. "
            "Continuous stirring during the reduction and crust stage — the crust must not stick and scorch. "
            "High-fat proteins only — lean proteins will dry out before the technique completes."
        ),
        "common_mistakes": (
            "Starting with too little liquid — the technique requires volume to build the sauce concentration. "
            "Insufficient heat monitoring during reduction — the crust burns in the final stage. "
            "Using lean protein — dried out meat with a burnt crust. "
            "Stopping too early — the crust hasn't fully caramelised and the dish tastes like an under-reduced curry."
        ),
        "pro_tips": (
            "Pork belly cut into 3cm cubes is the definitive dry Kristang curry protein — the fat renders into the caramelised spice crust, producing a unified flavour. "
            "The final stage — crust frying in rendered fat — is exactly the same process as the original tumis; the dish essentially re-fries its own spice paste using the protein's rendered fat. "
            "Serve with rice only — the concentrated spice crust is too intense for bread. "
            "The dry curry reheats excellently: add 2-3 tablespoons of water, cover, and heat gently — the crust softens slightly and the sauce reconstitutes."
        ),
        "trigger_keywords": json.dumps(["dry Kristang curry", "rendang technique Malacca", "concentrated spice crust", "Kristang dry curry", "reduced curry Malacca", "caramelised curry crust", "Eurasian dry curry"]),
        "authority_tier": 1,
        "lives_or_dies": "The heat management in the final 10 minutes. When the liquid is almost gone, the paste becomes intensely concentrated and the temperature rises rapidly — the crust caramelises beautifully at the right temperature and burns to bitterness at slightly too high. Keep a close watch and lower the heat as the last of the liquid evaporates. Nothing can recover a burnt crust.",
        "flavour_context": "Concentrated, caramelised, intense — the flavours of a full wet curry compressed and Maillard-developed on the protein surface. The crust is simultaneously crispy, sticky, spiced, and slightly sweet from the caramelised coconut milk reduction. Each bite is a full curry experience in a small package."
    },
    {
        "name": "Kristang curry balance: adjusting sweet, sour, salt, heat",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The four-flavour balancing framework of Kristang curry is a systematic calibration approach passed down through Kristang kitchens: every curry is tasted and adjusted on four axes — manis (sweet, typically palm sugar), masam (sour, tamarind or vinegar), masin (salty, belacan, salt, or ikan masin), and pedas (hot, dried chili). "
            "No Kristang curry is considered complete until all four axes are in conscious, deliberate balance. "
            "This is not a Malay invention — it is the Malay articulation of a universal Southeast Asian cooking intelligence that the Kristang absorbed into their cooking through centuries of Malacca community life.\n\n"
            "The balancing order matters: sourness is tasted and adjusted first (tamarind liquid or vinegar), because if the acid level is correct, salt and sweet follow more easily. "
            "Saltiness is adjusted second (a pinch of sea salt or an extra teaspoon of cincalok brine). "
            "Sweetness is adjusted third (palm sugar, never white sugar — palm sugar has a caramel-molasses dimension that white sugar lacks). "
            "Heat is adjusted last — chili can always be added but cannot be removed.\n\n"
            "The professional test for correct Kristang curry balance: a small mouthful on a clean spoon should register at least two of the four tastes clearly. "
            "If you can only identify one (only sour, or only salty), the balance is incorrect. "
            "A correctly balanced Kristang curry produces a complex, immediate response — the palate recognises multiple sensations in a single mouthful, each supporting rather than overwhelming the others."
        ),
        "key_principles": (
            "Taste and adjust in order: sour first, salt second, sweet third, heat last. "
            "Palm sugar, not white sugar — palm sugar adds depth; white sugar adds only sweetness. "
            "Small adjustments — each addition shifts all four axes simultaneously. "
            "The balance test: a spoonful should register at least two taste dimensions clearly."
        ),
        "common_mistakes": (
            "Adjusting heat first — it is irreversible; all other adjustments are made easier by leaving heat last. "
            "Using white sugar — flat, one-dimensional sweetness without the depth that palm sugar adds. "
            "Over-adjusting — adding large quantities of any seasoning disrupts the whole balance. "
            "Tasting from a hot pan — heat distorts the perception of sourness; allow the spoon sample to cool slightly."
        ),
        "pro_tips": (
            "A tiny addition of palm sugar (literally a thumbnail-sized piece) can resolve a curry that tastes too sharp or aggressive — it rounds all four dimensions simultaneously. "
            "The sourness of tamarind changes as it cooks — always taste at the end rather than relying on quantity measured at the start. "
            "Cincalok brine (the liquid from the jar) is an excellent precision salt adjustment — it adds both salt and fermented-umami simultaneously. "
            "The four-flavour balance applies to every Kristang preparation, not just curry — sambal, achar, and desserts all benefit from the same calibration thinking."
        ),
        "trigger_keywords": json.dumps(["Kristang curry balance", "manis masam masin pedas", "four flavour balance", "curry calibration", "Malay cooking balance", "Malacca seasoning technique", "palm sugar tamarind balance"]),
        "authority_tier": 1,
        "lives_or_dies": "The final taste, 5 minutes before service. This is the last moment to adjust. Taste with a clean palate (no earlier tasting for 10+ minutes if possible) and identify clearly which of the four axes is out of balance. The correction is usually small — a pinch, a squeeze, a pinch — and it transforms a good curry into an exceptional one.",
        "flavour_context": "The four-flavour balance is not a flavour itself — it is a state of integration. A correctly balanced Kristang curry does not taste sweet, sour, salty, or hot in isolation — it tastes complete and complex, with each sensation supporting the others. Imbalance announces itself immediately: a one-note curry is always imbalanced."
    },
    {
        "name": "Kristang fish curry: sour-spiced ikan technique",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Kristang fish curry is built on the same rempah system as other Kristang curries but with critical adaptations for the specific demands of fish protein — shorter cooking time (fish overcooks quickly), more pronounced sourness (acid complements fish fat), and the addition of whole tomatoes or tomato pieces as both souring agent and textural contrast, a technique that reflects the Portuguese colonial use of Mediterranean tomatoes introduced to Asia via Goa.\n\n"
            "The rempah for fish curry uses more turmeric and less dried chili than kari debal — producing a bright golden-yellow sauce that emphasises the sweetness of fresh fish rather than assertive spice. "
            "Thick-fleshed firm fish are preferred: batang (Spanish mackerel), kembung (Indian mackerel), or ikan merah (red snapper). "
            "The fish is cut into thick steaks (not fillets), marinated briefly in turmeric and salt, then added to the fried rempah after the coconut milk has been poured in — the fish cooks in the simmering sauce for no more than 8-12 minutes.\n\n"
            "The tomato addition is characteristically Kristang: whole small tomatoes or quartered large tomatoes are added 5 minutes before the end of cooking. "
            "They soften but do not dissolve — they contribute a fresh, slightly tart acidity and a textural softness that contrasts with the fish's firmness. "
            "Tamarind liquid is added as a secondary souring agent, and the final flavour is brighter and more forward than meat curries — the sourness is the first note on the palate, not the last."
        ),
        "key_principles": (
            "Fish goes into the simmering sauce, not onto the fried rempah — overcooked fish from contact with dry hot paste. "
            "Maximum 8-12 minutes of cooking — fish continues cooking in residual heat; remove from heat slightly before done. "
            "Tomatoes added 5 minutes before end — they soften but do not dissolve. "
            "More turmeric, less chili than meat curry — the sauce colour should be golden-yellow, not dark red."
        ),
        "common_mistakes": (
            "Adding fish to the fried rempah before adding coconut milk — the dry heat overcooks the outside instantly. "
            "Extended cooking — the fish turns dry, crumbly, and loses its flavour into the sauce. "
            "Too much dried chili — the sauce overpowers the fish rather than complementing it. "
            "Insufficient sourness — fish curry without a clear acid note tastes flat and heavy."
        ),
        "pro_tips": (
            "Marinate the fish in turmeric and salt for 15 minutes before cooking — this firms the exterior and improves texture in the curry. "
            "Thick fish steaks hold up better than fillets — the skin and bone provide structural support during cooking. "
            "The tomato addition is the Kristang signature — it distinguishes this fish curry from Malay ikan masak lemak (no tomato) and the Indian fish curry tradition. "
            "Fresh tamarind leaf (daun asam) thrown into the curry liquid briefly before removing adds a fragrant sourness distinct from tamarind paste."
        ),
        "trigger_keywords": json.dumps(["kristang fish curry", "ikan curry Malacca", "Eurasian fish curry", "Malacca fish curry", "tomato fish curry", "golden fish curry", "Kristang ikan masak"]),
        "authority_tier": 1,
        "lives_or_dies": "The fish cooking time. Fish in curry occupies a narrow window between raw and overcooked — 8-12 minutes depending on thickness. Overcooked fish breaks apart in the sauce and contributes dry, flavourless flakes. The correct moment is when the fish just yields to a probe at the thickest point — remove from heat immediately.",
        "flavour_context": "Golden-sour, aromatic, fresh — the brightness of the tamarind and tomato sourness leads, followed by the warmth of turmeric and galangal, then the sweetness of coconut milk. The fish must taste fresh and sweet through the sauce — if the fish disappears into the curry flavour, it has been overcooked."
    },
    {
        "name": "Sambal berlado: Kristang red chilli curry paste",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Sambal berlado is the Kristang term for a spiced red chili paste used as a cooking base and condiment — distinct from a standard sambal belacan (raw pounded condiment) in that berlado is cooked, reduced, and used as a pre-made paste for stir-frying vegetables, seafood, and egg preparations. "
            "The name 'berlado' is itself Kristang Portuguese — derived from 'malagueta' (chili pepper, literally 'malagueta pepper' in Portuguese), marking the term's colonial linguistic origin.\n\n"
            "Berlado paste: dried long red chilies (soaked and seeded), fresh red chilies, shallots, garlic, and a small amount of belacan are pounded or blended to a smooth paste, then fried in lard over medium heat until the colour deepens and the paste breaks from the oil. "
            "No galangal or lemongrass — berlado is deliberately simple, intended as a quick-application paste rather than a complex rempah. "
            "After frying, palm sugar and salt are added, and the paste is reduced until thick and almost jam-like.\n\n"
            "The finished berlado keeps refrigerated for 2-3 weeks and is used as the Kristang equivalent of a chili paste — added by spoonfuls to morning egg preparations, mixed into noodle dishes, used as a base for stir-fried vegetables, or simply served as a table condiment alongside rice. "
            "Its use distinguishes the Kristang kitchen from the Malay kitchen at a daily, domestic level — berlado is the everyday quick condiment, while the full rempah system is reserved for feast cooking."
        ),
        "key_principles": (
            "Cook until the paste is thick and jam-like — under-cooked berlado is watery and lacks the concentrated intensity. "
            "No galangal or lemongrass — berlado is a simple chili paste, not a full rempah. "
            "Palm sugar balances the chili — essential for the characteristic sweet-spicy character. "
            "Make in advance and store — berlado improves after a day as the flavours meld."
        ),
        "common_mistakes": (
            "Under-reducing — watery berlado lacks the jam-like intensity and doesn't coat vegetables correctly. "
            "Adding galangal or lemongrass — produces a rempah, not berlado; different dish. "
            "Omitting palm sugar — one-dimensional heat without the sweet-spicy balance that defines berlado. "
            "Using fresh red chilies only — dried and fresh combination gives both colour and depth."
        ),
        "pro_tips": (
            "A spoonful of berlado fried with shallots and an egg (sambal telur) is one of the fastest Kristang preparations. "
            "Berlado on toast — the Kristang equivalent of chili toast — is a daily breakfast preparation. "
            "The jam-like consistency means berlado can also be served as a relish alongside roast meats — the sweet-spicy quality works as a counterpoint to rich pork. "
            "Adding a tablespoon of tamarind liquid to berlado produces a sweeter-sourer version used specifically for seafood applications."
        ),
        "trigger_keywords": json.dumps(["sambal berlado", "Kristang chili paste", "berlado paste", "Malacca sambal", "quick Kristang condiment", "berlado Malacca", "Eurasian chili jam"]),
        "authority_tier": 1,
        "lives_or_dies": "The jam consistency. Berlado that has not reduced sufficiently is a liquid chili sauce — useful but not berlado. The correct consistency allows a spoonful to stand on the plate without running — thick, dark, sticky, and intensely aromatic.",
        "flavour_context": "Sweet-spicy, deeply red, slightly caramelised from the palm sugar reduction — the most approachable Kristang condiment. The heat is present but controlled by the sweetness; the flavour is direct and uncomplicated, meant for quick everyday use rather than the layered complexity of festival cooking."
    },
    {
        "name": "Kristang curry powder blend: spice proportion technique",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "While the Kristang kitchen is primarily a wet rempah-based system, a dry spice powder blend (a mixture influenced by the Indian South Asian curry powder tradition that entered Malacca via the Indian Tamil, Chettinad, and Muslim trading communities) is used in certain preparations — most notably batata baje, gulai, and some pork preparations — as a secondary spice layer added to the wet rempah. "
            "The Kristang dry blend is not identical to any Indian curry powder; it is a regional adaptation.\n\n"
            "Kristang dry spice proportions (roasted and ground): coriander (3 parts) — cumin (1.5 parts) — fennel (1 part) — turmeric (1 part) — dried red chili (1 part) — cinnamon (0.5 part) — cardamom (0.5 part) — cloves (0.25 part) — black pepper (0.25 part). "
            "All whole spices are dry-roasted separately in a pan until fragrant (30-60 seconds each), then combined and ground together in small batches — freshly ground powder is non-negotiable for quality. "
            "Pre-ground commercial curry powder lacks the volatile aromatic compounds that fresh grinding releases.\n\n"
            "Use: 1-2 teaspoons of dry blend is added to the rempah after the initial frying (not before — the rempah must fry first), then cooked together for 2-3 minutes before liquid is added. "
            "This secondary frying of the dry blend activates the fat-soluble aromatic compounds in the spices and integrates them into the rempah. "
            "Adding the dry blend to liquid rather than fat inhibits aromatic extraction and produces a flat, dusty-spiced curry."
        ),
        "key_principles": (
            "Dry-roast each spice separately — different spices have different roasting times and burn easily together. "
            "Grind fresh before use — pre-ground loses volatile aromatics within days of grinding. "
            "Add to the frying rempah (not to liquid) — fat-soluble aromatic compounds require fat activation. "
            "Small quantities — the dry blend is a supporting layer, not the primary spice source."
        ),
        "common_mistakes": (
            "Using pre-ground commercial curry powder — flat, stale aromatics. "
            "Adding the dry blend to cooking liquid — aromatic compounds are fat-soluble, not water-soluble. "
            "Too much dry blend — it becomes the dominant flavour and overwhelms the wet rempah aromatics. "
            "Not roasting the whole spices — raw coriander and cumin have a dusty, slightly bitter quality."
        ),
        "pro_tips": (
            "Fennel seed in the Kristang blend is a South Indian Tamil influence — it adds a sweet, anise note that distinguishes this blend from purely Malay-influenced versions. "
            "Store the dry blend in an airtight jar away from light and heat — it holds aromatic quality for 2-3 weeks. "
            "Toast the blend very briefly (30 seconds) in the residual heat of the rempah pan before adding to liquid — this reactivates the volatile compounds. "
            "The coriander-to-cumin ratio of 2:1 is the identifying proportion of the South Indian influence — North Indian-influenced blends reverse this ratio."
        ),
        "trigger_keywords": json.dumps(["Kristang curry powder", "dry spice blend Malacca", "Eurasian curry spice", "Kristang spice mix", "Malacca curry blend", "Tamil influence Kristang", "Kristang masala"]),
        "authority_tier": 1,
        "lives_or_dies": "The freshness of the grind. Curry powder ground more than a week ago has lost most of its volatile aromatic content — the coriander's fresh citrus note, the cumin's earthy warmth, the fennel's sweet anise are all gone. The only test is smell: fresh-ground curry powder should fill the room with aromatic complexity. Old powder smells only of old paper.",
        "flavour_context": "Warm, earthy, citrus-coriander-forward, with sweet fennel and cardamom dimensions — the South Indian Tamil contribution to the Kristang aromatic vocabulary. It adds warmth and depth beneath the galangal-lemongrass brightness of the wet rempah, producing a more rounded, multi-dimensional curry base."
    },
    {
        "name": "Carne assada kristang: Portuguese braised spiced meat",
        "category": "Kristang — Curry & Spice Pastes",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Carne assada kristang — literally 'roasted meat' in Portuguese, though the cooking technique has transformed from roasting to braising in the tropical Malacca context — is the slow-cooked, spiced beef or pork preparation that most clearly preserves the Portuguese culinary structure within the Kristang kitchen. "
            "The dish uses a spice profile that is unmistakably European (cumin, coriander, black pepper, cloves) applied to a braising technique (slow cooking in liquid with vegetables and aromatics), with Southeast Asian additions (belacan, lemongrass) that signal the Malay synthesis.\n\n"
            "The meat (traditionally beef short rib, or pork shoulder) is marinated overnight in a paste of toasted-and-ground cumin, coriander, black pepper, garlic, and vinegar — the Portuguese 'vinha d'alhos' marinade tradition adapted to available tropical spices. "
            "The marinated meat is browned deeply in lard, then braised in a mixture of fried rempah (basic shallot-garlic-lemongrass), the marinade liquid, coconut milk, and a small amount of palm sugar for 1.5-2.5 hours until falling-tender. "
            "The sauce is a deep, complex braising liquid — not a curry sauce, but something between a European braise jus and a Southeast Asian curry base.\n\n"
            "Service: carne assada kristang is served at the Kristang Christmas table alongside kari debal and sugee cake — it is the most clearly 'Portuguese' preparation among the Kristang feast dishes. "
            "In professional culinary context, it demonstrates the Kristang position as living bridge between Portuguese colonial cuisine and Malay-Southeast Asian cooking — neither fully one nor the other."
        ),
        "key_principles": (
            "Overnight marinade is not optional — it penetrates the meat and creates the flavour foundation. "
            "Deep browning before braising — Maillard crust is essential for the sauce depth. "
            "Long, slow braise — short-rib collagen requires 1.5-2.5 hours at minimum to dissolve. "
            "Vinegar in the marinade is the Portuguese signature — it tenderises and flavours simultaneously."
        ),
        "common_mistakes": (
            "Insufficient marination time — 2 hours is not overnight; the spice penetration is inadequate. "
            "Under-browning — pale braised meat lacks the Maillard depth that the braise liquid builds on. "
            "Too much coconut milk — the dish becomes a curry rather than a braise; the European structure is lost. "
            "Lean cuts — collagen-rich cuts are essential for the silky braising sauce."
        ),
        "pro_tips": (
            "The 'vinha d'alhos' marinade is one of the clearest surviving connections between modern Kristang cooking and 16th-century Portuguese culinary technique — the same marinade produced the Caribbean 'vindaloo' through the Goa trading connection. "
            "Adding a cinnamon stick and 2 cloves to the braise liquid adds a Portuguese confectionery-spice dimension to the otherwise savoury preparation. "
            "The braising liquid, reduced and strained, makes an exceptional sauce — complex, dark, deeply flavoured, with the combined character of both European braise and Southeast Asian rempah. "
            "Carne assada kristang served with white rice and achar is a complete Kristang feast in three components."
        ),
        "trigger_keywords": json.dumps(["carne assada kristang", "Kristang braised meat", "Portuguese braise Malacca", "vinha d'alhos Malacca", "Eurasian spiced beef", "Kristang Christmas meat", "Portuguese pork braise"]),
        "authority_tier": 1,
        "lives_or_dies": "The browning. Carne assada kristang braised without proper Maillard browning produces a pale, flat-tasting stew — the dark, caramelised crust on the exterior of the meat is what gives the braising liquid its colour and depth. Every surface of every piece of meat must be browned before the liquid goes in.",
        "flavour_context": "Deep, dark, complex — the European cumin-coriander-pepper marinade base provides a warmth and structure that the Southeast Asian curries lack, while the rempah and coconut milk additions round and deepen the Portuguese spice platform. The braising liquid tastes of two culinary traditions in genuine dialogue."
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
print(f"\nBatch 3 complete: {inserted}/{len(entries)} inserted")
