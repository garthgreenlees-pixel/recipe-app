#!/usr/bin/env python3
"""Kristang PCT-9 — Batch 7: Soups, Broths & Cultural Heritage (12 entries)"""
import psycopg2, psycopg2.extras, re, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

entries = [
    {
        "name": "Caldu kristang: Eurasian bone broth foundation",
        "category": "Kristang — Soups & Broths",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Caldu kristang is the Eurasian bone broth — a long-simmered stock of pork or chicken bones that forms the liquid foundation for Kristang soups and gravies, named directly from the Portuguese 'caldo' (broth). "
            "The caldu reflects the Portuguese colonial understanding that a kitchen without a proper stock is a kitchen working with one hand behind its back — an understanding that the Kristang community preserved through centuries while the surrounding Malay cuisine relied more on coconut milk and rempah as liquid flavour bases.\n\n"
            "Preparation: pork knuckle bones or chicken carcasses are blanched first (covered in cold water, brought to a boil, blanched for 5 minutes, drained and rinsed) — this removes the blood proteins that would produce a cloudy, bitter stock. "
            "The blanched bones are combined with cold water (3:1 water-to-bones ratio), brought slowly to a simmer, and held at a very gentle simmer for 2-3 hours (chicken) or 4-6 hours (pork). "
            "Aromatics: fresh ginger (bruised), garlic (smashed), white peppercorns, and a stalk of lemongrass. "
            "No strong spices — the caldu must be neutral enough to use as a base for multiple different dishes.\n\n"
            "The finished caldu is strained through muslin or a fine-mesh sieve and defatted when cold (the solidified fat lifts off cleanly). "
            "A correct caldu is clear, golden (chicken) or pale amber (pork), and has a subtle but present body from dissolved collagen. "
            "When chilled, the pork caldu should set to a light jelly — this gelatin content is the quality indicator that the stock has extractive value beyond merely flavoured water."
        ),
        "key_principles": (
            "Blanch the bones first — removes blood proteins that produce cloudy, bitter stock. "
            "Gentle simmer, never boiling — boiling emulsifies the fat and makes the stock cloudy. "
            "Start with cold water — brings out more collagen and protein than hot water. "
            "Neutral aromatics only — the stock must be versatile."
        ),
        "common_mistakes": (
            "Skipping the blanch — murky, slightly bitter stock. "
            "Boiling the stock — emulsified fat produces cloudy, greasy result. "
            "Strong spices in the stock — limits the stock's versatility as a base. "
            "Short cooking time — insufficient collagen extraction."
        ),
        "pro_tips": (
            "Kristang caldu with its lemongrass and ginger aromatics is distinct from French veal stock or Chinese pork broth — the aromatic profile is lighter, more citrus-forward, and more Southeast Asian. "
            "Use caldu as the base liquid in kari debal and babi lodeh instead of water — the depth and body it adds to both dishes is significant. "
            "Roasting the bones at 200°C for 30 minutes before blanching produces a darker, richer stock with Maillard development — a Kristang variation for richer braises. "
            "Caldu frozen in ice cube trays provides instant flavour additions to fried rice, sambal, and vegetable preparations."
        ),
        "trigger_keywords": json.dumps(["caldu kristang", "Eurasian bone broth", "Kristang stock", "Malacca broth", "caldo Malacca", "pork stock Kristang", "Portuguese broth Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "The blanching. Without it, the blood proteins that foam off the bones during cooking remain in the stock — they produce cloudiness and a background bitterness that no amount of simmering removes. Blanch first, every time.",
        "flavour_context": "Clean, golden, subtly aromatic — the lemongrass adds a citrus warmth; the ginger adds a gentle heat; the white peppercorns add faint spice. Not assertive, not complex — it is a foundation, designed to enhance everything it touches rather than announce itself."
    },
    {
        "name": "Canja kristang: Portuguese-Malay chicken rice soup",
        "category": "Kristang — Soups & Broths",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Canja kristang is the Eurasian chicken rice porridge-soup — directly descended from the Portuguese 'canja de galinha' (chicken broth with rice, the canonical Portuguese restorative soup) and adapted to the Malacca context with local aromatics and the Malay tradition of adding aromatic herbs. "
            "The name is unchanged from the Portuguese original, making it one of the most clearly traced culinary inheritances in the Kristang canon.\n\n"
            "The Portuguese original canja is a simple broth of chicken simmered until the meat falls from the bone, rice added and cooked until swollen and thickening the broth, finished with lemon juice and mint. "
            "The Kristang adaptation introduces lemongrass and ginger into the simmering broth, replaces lemon with calamansi juice, and adds daun sup (flat-leaf parsley substitute, often Chinese celery) and fried shallots as garnishes — the structure remains Portuguese but the aromatics are Southeast Asian.\n\n"
            "The rice is added directly to the simmering chicken broth (a whole chicken or bone-in pieces) and cooked until swollen and beginning to soften the broth to a thick, slightly starchy consistency. "
            "The chicken is removed, shredded, and returned to the soup. "
            "Kristang canja is served at recovery from illness (the Portuguese association with chicken soup as restorative medicine is fully preserved), at breakfast, and as an opening course at Kristang feasts."
        ),
        "key_principles": (
            "Whole chicken or bone-in pieces — the collagen from bones gives body. "
            "Rice added to the simmering broth, not cooked separately — the starch thickens the soup as the rice cooks. "
            "Calamansi added at service, not during cooking — the acid brightens but diminishes with heat. "
            "Fried shallot garnish — the crunch and aromatic depth is the finishing layer."
        ),
        "common_mistakes": (
            "Pre-cooked rice added — does not thicken the broth; produces floating rice in thin soup. "
            "Boneless chicken — lacks the collagen body. "
            "Calamansi added during cooking — acid is cooked away. "
            "No fried shallot — the soup feels incomplete without the textural and aromatic contrast."
        ),
        "pro_tips": (
            "Tie a pandan leaf knot into the simmering chicken broth — a Kristang addition that the Portuguese original does not have and that adds a green-floral depth. "
            "Chinese celery (daun sup) is the standard garnish in Kristang cooking — it has a stronger, more aromatic quality than flat-leaf parsley and is more appropriate to the Southeast Asian context. "
            "The longer the rice cooks, the thicker the soup — Kristang canja can be calibrated from a brothy soup to a congee-like porridge by adjusting the cooking time. "
            "Canja is the most direct evidence of the Portuguese caldo tradition surviving intact in Kristang cooking — the preparation is 500 years old."
        ),
        "trigger_keywords": json.dumps(["canja kristang", "Kristang chicken soup", "Portuguese chicken soup Malacca", "canja Malacca", "Eurasian chicken rice soup", "Kristang restorative soup", "caldo galinha Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "The rice cooking in the broth. The starch from the rice thickens the soup and creates the characteristic slightly viscous, satisfying body of canja. Rice cooked separately and added at the end produces a thin, watery soup with floating rice — the texture relationship between rice and broth is wrong.",
        "flavour_context": "Clean chicken sweetness, lemongrass-citrus background, ginger warmth, the bright hit of calamansi at service — a restorative soup that is simultaneously simple and deeply satisfying. The Kristang version has more aromatic complexity than the Portuguese original without abandoning the fundamental character."
    },
    {
        "name": "Kristang laksa: Eurasian coconut noodle soup",
        "category": "Kristang — Soups & Broths",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Kristang laksa is the Eurasian adaptation of the Nyonya curry laksa tradition — a spiced coconut milk noodle soup that reflects the convergence of the Portuguese-Kristang coconut curry technique with the Peranakan Chinese noodle tradition and the Malay aromatic vocabulary. "
            "The Kristang version is distinguished from Nyonya laksa by a more pronounced tamarind sourness (reflecting the Kristang preference for acid in coconut preparations) and the use of lard as the cooking fat.\n\n"
            "The laksa broth is built on a fried rempah of shallots, galangal, lemongrass, dried red chili, fresh turmeric, and belacan — fried until the paste breaks from the oil, then extended with concentrated prawn stock (from prawn heads and shells simmered for 30 minutes) and first-press coconut milk. "
            "The soup must have three clearly identifiable flavour dimensions: the spice aromatic from the rempah, the coconut richness from the coconut milk, and the sourness from the tamarind. "
            "If any one of the three is missing or dominant, the broth is unbalanced.\n\n"
            "Noodle selection: thick round rice noodles (laksa noodles or fresh round rice noodles — beehoon is too thin). "
            "Protein: cooked prawns (essential), tofu puffs (fried tofu, which absorbs the broth), and cockles (kerang). "
            "Garnish: laksa leaf (daun kesum), sliced fresh red chili, and bean sprouts. "
            "The standard Kristang bowl: hot broth poured over noodles and garnishes in a deep bowl, with a side of sambal belacan."
        ),
        "key_principles": (
            "Prawn stock is essential — plain water with coconut milk produces a thin, sweet broth without the depth. "
            "Three dimensions in the broth: spice, coconut, sour — all three must be identifiable. "
            "Daun kesum as garnish — its peppery-citrus note is the finishing aromatic identity of laksa. "
            "Do not boil after adding thick coconut milk — keep at a simmer."
        ),
        "common_mistakes": (
            "Water instead of prawn stock — thin, flat broth. "
            "Insufficient tamarind — one-dimensional sweet-spicy broth without the sour balance. "
            "Substituting regular coriander for daun kesum — different aromatic profile. "
            "Boiling after adding thick coconut milk — emulsion breaks."
        ),
        "pro_tips": (
            "The prawn head stock is the secret of excellent laksa broth — the natural umami and sweetness of the prawn heads and shells produces depth that nothing else replicates. "
            "Toast the coconut milk lightly (cook it with the fried rempah for 2-3 minutes before adding the prawn stock) — this caramelises the coconut milk solids and adds depth to the broth. "
            "A squeeze of calamansi at service into the finished bowl brightens the broth in the same way that lime brightens a Thai curry — optional but strongly recommended. "
            "Laksa should always be served very hot — the aromatic volatiles in the daun kesum and lemongrass dissipate quickly at lower temperatures."
        ),
        "trigger_keywords": json.dumps(["Kristang laksa", "Eurasian laksa", "Malacca laksa", "Kristang noodle soup", "coconut laksa Malacca", "curry laksa Kristang", "Nyonya laksa variation"]),
        "authority_tier": 1,
        "lives_or_dies": "The prawn stock. Laksa made without prawn stock — using water or even chicken stock — produces a pleasant coconut curry soup but not laksa. The prawn stock's natural sweetness and depth is the flavour bridge between the rempah and the coconut milk. Without it, the three-dimensional broth structure cannot be built.",
        "flavour_context": "Spiced, coconut-rich, sour, prawn-sweet — a complex, layered broth that is one of the most aromatic soups in Southeast Asian cooking. The daun kesum garnish adds a peppery-citrus top note that provides a fourth flavour dimension and lifts the entire bowl at the moment of eating."
    },
    {
        "name": "Kristang oxtail soup: Portuguese colonial braise",
        "category": "Kristang — Soups & Broths",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Oxtail soup is among the most clearly Portuguese-derived Kristang preparations — a long, slow braise of whole oxtail sections in a spiced tomato-onion broth that parallels the Portuguese rabo de boi (oxtail stew) while incorporating Kristang spice additions (lemongrass, galangal, fresh chili) that give it a distinctly Malaccan identity. "
            "The preparation demonstrates the Kristang capacity to cook the same cut of meat in a technique derived from Europe but with a flavour profile that is unmistakably Southeast Asian.\n\n"
            "The oxtail is blanched first (15 minutes in boiling water, then rinsed — essential for a clear soup), then browned in lard until deeply caramelised on all surfaces. "
            "The browned oxtail is braised in a mixture of fried shallots and garlic, canned or fresh tomatoes, beef stock or water, lemongrass (whole bruised stalk), galangal (sliced), fresh red chili, black pepper, and a small amount of soy sauce for colour. "
            "The braise takes 3-4 hours at a low simmer until the oxtail is falling-tender and the collagen has fully dissolved into the broth, making it silky and slightly gelatinous.\n\n"
            "Service: the soup is served in deep bowls with the oxtail sections in the broth, garnished with fried shallots, fresh green onion, and a squeeze of calamansi. "
            "A side of Kristang achar or fresh cut bird's eye chili provides the acid counterpoint. "
            "The oxtail soup is a dish of patience — 3-4 hours is the minimum and longer produces a more unctuous, deeply flavoured result."
        ),
        "key_principles": (
            "Blanch oxtail before browning — removes blood proteins and scum. "
            "Brown deeply in lard — the Maillard crust is the depth of the broth. "
            "Low simmer for minimum 3-4 hours — collagen dissolution is time-dependent. "
            "The broth should be slightly gelatinous when cold — this confirms proper collagen extraction."
        ),
        "common_mistakes": (
            "No blanching — murky, bitter-tinted broth. "
            "Insufficient browning — pale broth without depth. "
            "Short cooking time — tough oxtail and thin broth without gelatin body. "
            "High heat braise — the broth becomes cloudy and the oxtail surface breaks down to stringy fibres."
        ),
        "pro_tips": (
            "The collagen in oxtail is one of the richest of any cut — properly extracted, the broth sets to a firm jelly when cold. "
            "Adding a star anise and cinnamon stick to the braise (very small quantities — 1 star anise, half a cinnamon stick) is the Kristang-Portuguese spice bridge, adding a warm-sweet note without making the dish taste explicitly like Asian five-spice. "
            "The fat that rises to the surface during braising should be skimmed every 45 minutes — it produces a cleaner, less greasy broth. "
            "Oxtail soup, like all collagen-rich braises, is dramatically better the next day — the overnight rest allows the fat to solidify completely for easy removal and the flavours to fully integrate."
        ),
        "trigger_keywords": json.dumps(["Kristang oxtail soup", "oxtail braise Malacca", "Eurasian oxtail", "rabo de boi Malacca", "Kristang beef soup", "Malacca oxtail", "Portuguese oxtail Kristang"]),
        "authority_tier": 1,
        "lives_or_dies": "The collagen dissolution test. After 3-4 hours, take a spoonful of broth and allow it to cool on the spoon. If it does not become slightly sticky and viscous, the collagen has not yet dissolved — continue braising. The silky, slightly gelatinous quality of the finished broth is the mark of a correct preparation.",
        "flavour_context": "Deeply savoury, slightly gelatinous, tomato-acid, lemongrass-aromatic — a European braise character (tomato, onion, deep browning) layered with Southeast Asian aromatics (lemongrass, galangal, chili). The collagen from the oxtail makes the broth unctuous; the lemongrass prevents it from being heavy."
    },
    {
        "name": "Kristang mustard seed tempering: Portuguese-Malay fusion technique",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The use of white mustard seeds in Kristang cooking — specifically as whole seeds popped in hot fat at the start of the cooking process (tarka, or tempering, as the technique is known in the South Asian culinary tradition) — is the most clearly Indian-Portuguese hybrid technique in the Kristang kitchen. "
            "Mustard seeds do not appear in standard Malay cooking, but they are central to the Portuguese tradition (mostarda) and are an important element of Indian Tamil and Chettinad cooking — the two culinary traditions that met in Malacca.\n\n"
            "The technique: white or yellow mustard seeds (preferred over black — black mustard seeds are more pungent) are added to hot lard or fat in a covered pan or wok just before the rempah is added. "
            "The temperature must be high enough to pop the seeds immediately — if the seeds sizzle gently without popping, the fat is too cool. "
            "The seeds pop loudly (30-60 seconds) and must be covered to prevent them from flying out of the pan. "
            "Once the popping subsides, the heat is lowered and the rempah is added. "
            "The popped seeds remain in the dish and are eaten — they contribute a nutty, faintly bitter base note beneath the rempah aromatics.\n\n"
            "In kari debal specifically, the mustard seeds are a distinguishing element — their nutty-bitter note is one of the identifying tastes of the finished curry. "
            "Tasting a Kristang curry and detecting the mustard seed character (popped and nutty, not raw and bitter) is the indicator that the tempering was executed correctly."
        ),
        "key_principles": (
            "High heat for the pop — seeds at insufficient temperature become dark and bitter rather than nutty and fragrant. "
            "Cover the pan during popping — mustard seeds are violent; they will spray out of an uncovered pan. "
            "White/yellow mustard seeds, not black — less aggressive, more appropriate for the Kristang flavour profile. "
            "Add rempah immediately after popping subsides — do not let the seeds continue cooking."
        ),
        "common_mistakes": (
            "Insufficient fat temperature — seeds sizzle without popping, then burn. "
            "Uncovered pan — seeds spray out and the remaining seeds are unevenly popped. "
            "Black mustard seeds — too pungent for most Kristang applications. "
            "Adding seeds to cold fat and heating — same as insufficient temperature problem; the slow heat produces bitter rather than nutty."
        ),
        "pro_tips": (
            "The popping of mustard seeds in fat is a direct continuation of the Indian tarka technique — the South Indian Tamil community's influence on Kristang cooking is clearly visible in this single preparation step. "
            "A lid held loosely over the pan allows the seeds to pop fully without escaping while preventing steam buildup. "
            "The nutty quality of properly popped white mustard seeds is almost indistinguishable from sesame seeds in flavour — they add a toasty, slightly bitter depth. "
            "The mustard seed technique appears in dishes influenced by the South Indian community (fish head curry, vegetable curries) as well as the quintessential Kristang preparation (kari debal)."
        ),
        "trigger_keywords": json.dumps(["mustard seed tempering", "Kristang mustard seeds", "tarka Malacca", "mustard seed kari debal", "white mustard seeds", "mustard seed technique Kristang", "South Indian Kristang fusion"]),
        "authority_tier": 1,
        "lives_or_dies": "The heat. Mustard seeds in cold fat will never pop correctly — they cook slowly, become dark, and turn bitter. The fat must be hot enough that a single seed dropped in pops within 2-3 seconds. This temperature is the only condition under which the seeds will produce their characteristic nutty, fragrant pop.",
        "flavour_context": "Nutty, faintly bitter, toasty — the popped mustard seed adds a base note beneath the rempah that is specifically 'not Malay'. It is the Portuguese-Indian contribution that gives Kristang curry a dimension that standard Malay curry lacks. Subtle but identifiable; present in every mouthful."
    },
    {
        "name": "Kristang rice cooking: pandan-lemongrass aromatic method",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Kristang rice is not plain steamed rice — it is cooked with aromatic additions that infuse the grains with fragrance, making the rice itself an active part of the meal rather than a neutral starch backdrop. "
            "The Kristang aromatic rice method adds a pandan leaf knot, a bruised lemongrass stalk, and a small piece of ginger to the rice cooking water — a simple addition that transforms plain rice into an aromatic, fragrant accompaniment that enhances the entire table.\n\n"
            "The preparation: long-grain white rice (jasmine rice is standard) is rinsed 3-4 times until the water runs clear. "
            "A pandan leaf is tied into a knot (the knot bruises the cells and increases aromatic release during cooking). "
            "A lemongrass stalk is bruised by hitting it firmly along its length. "
            "A 2cm piece of fresh ginger is peeled and lightly smashed. "
            "All aromatics are placed in the rice cooker or pot with the water before the rice is added. "
            "Rice is cooked by absorption method — the aromatics are left in during the entire cooking process and removed before serving.\n\n"
            "The finished rice has a very subtle, barely-there fragrance — not sweet (from pandan), not sharply citrus (from lemongrass), but a combined gentle floral-grass note that lifts the entire bowl. "
            "This fragrance is the Kristang standard: the rice should smell slightly aromatic when the lid is lifted, and that fragrance should carry through each mouthful with the curry it accompanies."
        ),
        "key_principles": (
            "Knot the pandan leaf — bruising releases more aromatic compounds during cooking. "
            "Bruise the lemongrass stalk along its length — cracks the cells for aromatic release. "
            "Add all aromatics to the water before the rice — they infuse during the entire cooking period. "
            "Remove before serving — the aromatics are flavour tools, not edible components."
        ),
        "common_mistakes": (
            "Unbruised pandan leaf — no aromatic release into the rice. "
            "Adding aromatics after the rice — insufficient infusion time. "
            "Leaving the aromatics in the serving bowl — diners encounter whole lemongrass and pandan, which are not eaten. "
            "Too much ginger — the ginger note becomes dominant and clashes with delicate curries."
        ),
        "pro_tips": (
            "The Kristang triple aromatic (pandan + lemongrass + ginger) in rice is specifically designed to complement the curry flavours served alongside. "
            "Adding a half-teaspoon of coconut milk to the cooking water produces a slightly richer, more aromatic rice — Kristang nasi lemak style. "
            "Kaffir lime leaf (one or two, slightly bruised) can be added to the pandan-lemongrass combination for a more citrus-forward aromatic rice. "
            "The quality test: lift the lid when the rice is cooked and inhale — a faint, complex floral-grass fragrance should be identifiable. If the rice smells of nothing, the aromatics were insufficient or not bruised."
        ),
        "trigger_keywords": json.dumps(["Kristang aromatic rice", "pandan lemongrass rice", "Malacca rice cooking", "Eurasian rice method", "pandan rice", "Kristang nasi", "fragrant rice Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "The bruising. Unbruised aromatics produce minimal fragrance release — you can smell them individually if you hold them to your nose, but they contribute almost nothing to the rice cooking in the pot. The bruising (knot for pandan, heavy hit for lemongrass) cracks the aromatic-oil-bearing cells and allows the volatile compounds to infuse the cooking water and steam.",
        "flavour_context": "The rice itself should not taste strongly of anything — the aromatic additions are a background fragrance, not a dominant flavour. The Kristang test: eat a spoonful of rice alone and you should detect a very faint floral-citrus note. Eat the same rice alongside kari debal and the aromatic rice and curry should feel unified, not competing."
    },
    {
        "name": "Kristang ketupat: compressed rice in coconut leaf",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang and Malay community, Malacca, Malaysia",
        "description": (
            "Ketupat is compressed rice cooked in woven coconut leaf or palm leaf pouches — a preparation shared across the Malay Peninsula, Indonesia, and the Kristang community, used for festivals, celebrations, and as a portable food that keeps without refrigeration. "
            "The Kristang community cooks ketupat for Hari Raya (if there are Muslim neighbours to gift to), for community feasts, and sometimes for Christmas — it is a preparation that reflects the Kristang integration with Malay community life.\n\n"
            "The technique of woven ketupat pouches: young coconut leaves are woven into small diamond or rectangular pouches, raw parboiled rice is filled to half-capacity, and the pouch is sealed. "
            "When the rice cooks, it absorbs water and expands to fill the pouch completely — the pressure of expansion against the leaf walls is what produces the characteristic dense, compressed texture. "
            "The pouches are boiled in a large pot of water for 3-4 hours. "
            "Correct ketupat is very dense, almost cake-like in texture, slightly glossy from the coconut leaf tannins transferred during cooking, and subtly flavoured by the coconut leaf oil compounds.\n\n"
            "Service: ketupat is sliced after cooking (the leaf must be cut away, not torn — tearing shreds the rice surface) and served alongside satay, rendang, or Kristang curry. "
            "The dense, compressed rice texture is specifically designed to accompany sauce-heavy preparations — it absorbs the curry or satay sauce without falling apart as individual grains would."
        ),
        "key_principles": (
            "Half-fill the pouch only — room for expansion is the mechanism of the compression. "
            "Full 3-4 hour boil — insufficient cooking produces uneven rice with hard centres. "
            "Slice the leaf away cleanly — do not tear. "
            "Cool before slicing — warm ketupat crumbles; cold ketupat slices cleanly."
        ),
        "common_mistakes": (
            "Over-filling the pouch — the rice cannot expand, producing unevenly cooked ketupat with hard centres. "
            "Under-boiling — the centre remains uncooked. "
            "Tearing the leaf off — damages the surface of the compressed rice. "
            "Slicing while warm — crumbles rather than slicing cleanly."
        ),
        "pro_tips": (
            "The half-fill rule is critical and counterintuitive — it feels like under-filling. "
            "Store cooked ketupat in the leaf pouches, not unwrapped — the leaf continues to flavour the rice and protects its surface moisture. "
            "Ketupat keeps at room temperature for 1-2 days; refrigerated for 3-4 days. "
            "The ability to weave a ketupat pouch is a traditional Malay and Kristang cultural skill — increasingly rare among younger generations but preserved in community events."
        ),
        "trigger_keywords": json.dumps(["ketupat", "Kristang compressed rice", "woven leaf rice", "Malacca ketupat", "coconut leaf rice", "ketupat technique", "festival rice Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "The half-fill. Fill the pouch to half — the rice expands to fill the pouch completely during cooking and the pressure of expansion produces the dense, compressed texture. Over-fill and the rice cannot expand; the pressure is insufficient and the texture is wrong. Under-fill and there is too much space; the compression fails.",
        "flavour_context": "Subtly flavoured by the coconut leaf tannins and oils — a faint grassy, nutty note that plain rice lacks. The main quality is textural: the dense, cake-like compression is the contrast partner for the sauce-forward dishes that accompany it. Each cube holds its shape, absorbs the sauce, and delivers a satisfying, firm bite."
    },
    {
        "name": "Kristang Christmas food tradition: feast cycle and preparation",
        "category": "Kristang — Cultural Heritage",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The Kristang Christmas food tradition is one of the most coherent and complete festival food cultures in Southeast Asia — a specific, ordered set of preparations that have been maintained by the Kristang Catholic community for centuries and represent the intersection of Portuguese Catholic liturgical food tradition with the Malacca spice-and-coconut culinary context. "
            "Understanding the Christmas food cycle is understanding Kristang cuisine at its fullest expression.\n\n"
            "Christmas Eve (Vesperas): the table is light — fish preparations dominate (ikan assam pedas, steamed fish, fish curry) in the Catholic tradition of abstaining from meat on the eve of the feast day. "
            "The caldo (bone broth) is prepared on Christmas Eve to form the base for Christmas Day preparations. "
            "Christmas Day: the centrepiece is kari debal (Devil's Curry), traditionally made from the first cooked meats (pork, chicken) of the feast. "
            "Carne assada kristang (spiced roast meat) and Kristang smoked sausages are served. "
            "Sugee cake is the dessert centrepiece — prepared 2-3 days in advance to allow the flavours to mature. "
            "Boxing Day (St Stephen's Day, 26 December): the iconic kari debal day — Devil's Curry is made from the previous day's Christmas roast meats, now more intensely flavoured from the overnight rest and reheating in the rempah.\n\n"
            "The kari debal-from-leftovers tradition is one of the most culturally specific food practices in Kristang culture. "
            "The deliberate use of the previous day's roast meats in the curry produces a more complex dish than fresh meat would — the already-cooked protein has developed a flavour depth that raw meat lacks, and the curry penetrates more deeply into the fibres."
        ),
        "key_principles": (
            "Fish on Christmas Eve, meat on Christmas Day — the Catholic liturgical calendar governs the food calendar. "
            "Kari debal with leftover meats on Boxing Day — the tradition specifically requires previously cooked meat. "
            "Sugee cake prepared 2-3 days in advance — maturation improves the flavour. "
            "The full Kristang Christmas table is a performance of cultural identity as much as a meal."
        ),
        "common_mistakes": (
            "Fresh meat in Boxing Day kari debal — technically correct but culturally and gastronomically incorrect; the leftovers are the point. "
            "Sugee cake baked on Christmas Day — insufficient resting time. "
            "Serving kari debal without bread or rice — the dish requires a starch to absorb the thick sauce. "
            "Omitting any of the canonical dishes — the Kristang Christmas table is not modular."
        ),
        "pro_tips": (
            "The three-day Kristang Christmas food sequence (fish → roast meat → curry from leftovers) is a complete culinary narrative: restraint, abundance, and transformation. "
            "The Boxing Day kari debal tradition demonstrates a culinary sophistication about how previously cooked meat changes in curry — a practice that contemporary zero-waste cooking celebrates. "
            "Community preparation (gotong royong) is traditional for sugee cake and other large-batch preparations — the Kristang kitchen is a communal kitchen during festival periods. "
            "The full canon (canja, achar, kari debal, carne assada, sugee cake) represents every node of the PCT-9 Portuguese Colonial Trail in a single meal."
        ),
        "trigger_keywords": json.dumps(["Kristang Christmas food", "Malacca Christmas tradition", "kari debal Christmas", "sugee cake Christmas", "Kristang feast", "Eurasian Christmas Malacca", "Catholic Kristang food"]),
        "authority_tier": 1,
        "lives_or_dies": "The Boxing Day kari debal from leftover Christmas meats. This single practice is the most characteristic expression of Kristang culinary intelligence — the deliberate choice to make the curry from previously cooked rather than raw meat produces a demonstrably better dish and demonstrates an understanding of how flavour develops in cooked protein.",
        "flavour_context": "The Kristang Christmas table is not a single flavour but a sequence — restraint on Christmas Eve (clean fish flavours), abundance on Christmas Day (the full complexity of kari debal, roast meat, sugee cake), and transformation on Boxing Day (the leftover curry that is richer and more flavoured than the first day's version). Each day has its own flavour register."
    },
    {
        "name": "Kristang community cooking: tantu tradition",
        "category": "Kristang — Cultural Heritage",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Tantu (from the Portuguese 'tanto' — so much, abundant) is the Kristang term for communal cooking — the practice of gathering neighbours and extended family to prepare large quantities of food for festivals, weddings, and funerals. "
            "The tantu tradition is not merely practical (the volumes of food prepared are too large for a single cook) but deeply social and cultural — it is the mechanism by which culinary knowledge is transmitted between generations, techniques are taught through observation and practice, and the community's relationship with its food is maintained.\n\n"
            "The organisation of tantu follows specific traditional roles: the most experienced cook directs the rempah preparation and curry work (the highest-skill activities); younger cooks handle the grinding, peeling, and vegetable preparation; the senior women oversee the sweet preparations (sugee cake, onde onde, dodol). "
            "Tasks are distributed according to skill level and the work proceeds with a traditional order: rempah is prepared and fried first (it is the foundation of everything), then meats are braised, then sweets prepared, then assembly.\n\n"
            "The tantu system embeds culinary education into cultural practice — a young Kristang cook does not 'learn to cook' in isolation but participates in tantu from childhood, absorbing technique through hands-on participation in community preparation. "
            "The decline of tantu in contemporary Malacca is directly associated with the loss of culinary knowledge in the younger Kristang generation — when the communal cooking event disappears, the intergenerational transmission mechanism is broken."
        ),
        "key_principles": (
            "Role assignment by skill level — experienced cooks lead rempah and curry; newer cooks handle preparation tasks. "
            "Sequential order: rempah first, then braised meats, then sweets — the sequence builds on each stage. "
            "Transmission is oral and physical — no written recipes; knowledge moves through doing. "
            "The communal cooking event is the culinary education system."
        ),
        "common_mistakes": (
            "Not from a culinary perspective — the 'mistakes' here are social and systemic: not participating in tantu, not maintaining the tradition. "
            "In modern contexts: treating tantu as a practical efficiency rather than a cultural event. "
            "Relying on recipe books rather than observation and mentorship. "
            "Disconnecting the food from its community context."
        ),
        "pro_tips": (
            "For culinary professionals interested in Kristang cuisine: attend a tantu if any invitation arises. "
            "The tantu tradition parallels the Japanese shokunin system of transmission through supervised practice rather than explicit instruction. "
            "The Kristang community in Malacca has a Cultural Village (Kampung Portugis) where traditional preparations including tantu-style communal cooking can be observed. "
            "Documenting tantu practices — the specific role assignments, the preparation orders, the quality standards applied by experienced Kristang cooks — is urgent preservation work."
        ),
        "trigger_keywords": json.dumps(["tantu", "Kristang communal cooking", "Malacca community cooking", "Eurasian cooking tradition", "Kristang food culture", "tantu tradition", "Kristang culinary transmission"]),
        "authority_tier": 1,
        "lives_or_dies": "The continuation of tantu. When communal cooking events stop, culinary knowledge does not simply relocate to written recipes — it disappears. The techniques, standards, and judgements that experienced Kristang cooks apply are not fully expressible in text. Tantu is the technology of preservation.",
        "flavour_context": "Tantu does not have a flavour — it produces flavour. The food prepared in communal cooking reflects the accumulated knowledge of the community: the rempah is fried correctly because an experienced cook is watching and correcting; the sugee cake has the right butter ratio because the matriarch is measuring by hand and memory. The flavour of tantu-prepared food is the flavour of correct cultural transmission."
    },
    {
        "name": "Kristang cross-cultural food exchange: three-community Malacca kitchen",
        "category": "Kristang — Cultural Heritage",
        "origin": "Malacca, Malaysia — Kristang, Nyonya, and Tamil communities",
        "description": (
            "The Kristang kitchen did not develop in isolation — it evolved through five centuries of daily exchange with the Nyonya (Peranakan Chinese), Malay Muslim, South Indian Tamil, and Dutch colonial communities of Malacca. "
            "Understanding the lines of culinary influence — which techniques, ingredients, and dishes moved from each community into the Kristang kitchen — is essential for understanding why Kristang cuisine is what it is, and not merely what it is.\n\n"
            "From the Malay community: the rempah system (galangal, lemongrass, belacan, turmeric, dried chili as a paste), the coconut milk curry structure, fermented seafood condiments (belacan, cincalok), and the aromatic vocabulary (lemongrass, kaffir lime leaf, daun kesum). "
            "From the Nyonya (Peranakan Chinese) community: the Hokkien influence on dried shrimp use, the festive kueh tradition (pineapple tarts, onde onde, love letters), the wok technique, and the use of soy sauce. "
            "From the South Indian Tamil community: mustard seed tempering, curry leaf use, the fenugreek element in certain curries, and the influence of fresh turmeric. "
            "From the Portuguese ancestor tradition: the vinegar-based braising, the roasting and browning techniques, the enriched bread and pastry tradition, and the whole-animal pork cookery.\n\n"
            "The key diagnostic questions for any Kristang dish: where is the vinegar? Where is the rempah? Where are the mustard seeds? Where is the Portuguese whole-animal tradition? "
            "A dish that answers all four questions is clearly Kristang; a dish that answers only one or two is a cultural hybrid en route."
        ),
        "key_principles": (
            "Each community contribution is identifiable in finished Kristang dishes — none is hidden. "
            "The Portuguese base provides structure (braising, roasting, vinegar); the Malay base provides aromatics (rempah, spice paste, coconut milk). "
            "The synthesis is not fusion in the contemporary sense — it is the organic result of five centuries of daily community exchange. "
            "Cultural contribution is not dilution — the Kristang kitchen is more complex because of its multiple sources, not less."
        ),
        "common_mistakes": (
            "Attributing Kristang dishes entirely to Malay cuisine — ignores the Portuguese structural foundation. "
            "Attributing them entirely to Portuguese cuisine — ignores the fundamental Malay aromatic transformation. "
            "Treating the Nyonya influence as minor — the festive kueh tradition and wok techniques are significant. "
            "Overlooking the Tamil influence — mustard seeds, curry leaves, and fresh turmeric use are Tamil contributions."
        ),
        "pro_tips": (
            "The Malacca Straits UNESCO heritage designation protects the physical buildings but not the food knowledge — culinary preservation is entirely the community's responsibility. "
            "The Kristang community's current population in Malacca is approximately 2,000-3,000 — one of the smallest ethnic communities in Malaysia. "
            "For culinary professionals: understanding the Kristang kitchen provides a case study in how culinary traditions form, layer, and evolve — more useful than any theoretical model. "
            "The Portuguese Colonial Trail (PCT) in the Provenance system maps the movement of Portuguese food traditions from Portugal → Brazil → Goa → Malacca → Macau and the simultaneous local adaptations at each node."
        ),
        "trigger_keywords": json.dumps(["Kristang cross-cultural", "Malacca food history", "Eurasian food exchange", "Portuguese Malay synthesis", "Kristang food origin", "Malacca three community kitchen", "Peranakan Kristang food"]),
        "authority_tier": 1,
        "lives_or_dies": "The question of attribution. A Kristang dish described only as 'Malay curry' or only as 'Portuguese stew' has failed as documentation. The accurate description requires all four community contributions to be visible — that is the minimum standard for Kristang culinary documentation.",
        "flavour_context": "The flavour profile of Kristang cuisine is itself a description of its cultural history: the vinegar-depth of the Portuguese ancestors, the galangal-lemongrass brightness of the Malay aromatic system, the mustard-seed pop of the Tamil influence, and the festive kueh sweetness of the Nyonya exchange. Every mouthful carries five centuries."
    },
    {
        "name": "Kristang Portuguese Colonial Trail: PCT-9 culinary lineage",
        "category": "Kristang — Cultural Heritage",
        "origin": "Portuguese Colonial Trail — Malacca node, Malaysia",
        "description": (
            "The Kristang culinary tradition represents Node 9 of the Portuguese Colonial Trail (PCT-9) — a mapped lineage of culinary technique, ingredient, and preparation transfer along the Portuguese colonial trade and settlement network from Lisbon through the Atlantic islands, Brazil, coastal Africa, Goa, Malacca, and Macau. "
            "The PCT framework allows the Kristang kitchen to be understood not as an isolated regional cuisine but as a specific, datable, traceable transformation of the Portuguese culinary tradition in a Southeast Asian context.\n\n"
            "Key PCT-9 markers — preparations and techniques that can be traced directly to Portuguese culinary origin: "
            "(1) Caldo → caldu kristang (broth as foundational cooking liquid); "
            "(2) Escabeche → Kristang vinegar pickle (acid-preserved fried fish/vegetables); "
            "(3) Pão doce → pang susi (enriched milk bread with local coconut filling); "
            "(4) Chouriço → Kristang smoked sausage (red-spiced, garlic-pork sausage); "
            "(5) Rabo de boi → Kristang oxtail soup (slow-braised oxtail); "
            "(6) Vinha d'alhos → carne assada kristang (vinegar-garlic marinade for braised meat); "
            "(7) Pastel de nata → Kristang egg tart (custard tart in pastry shell); "
            "(8) Almôndega → bidara (pork meatball in sauce); "
            "(9) Bolo de mel/semolina cake → sugee cake; "
            "(10) Amor-perfeito/wafer → kueh kapit (love letters).\n\n"
            "The connecting markers from Goa (PCT-8): bebinca (shared exactly between Goan and Kristang kitchens), and the vinha d'alhos marinade which travels from Portugal → Goa → Malacca. "
            "The Kristang kitchen is the convergence point of the westward-moving Portuguese culinary tradition (following the trade route) and the northward-moving Malay culinary tradition — neither could have produced Kristang cuisine alone."
        ),
        "key_principles": (
            "Every dish in the Kristang kitchen can be classified by its origin community contribution. "
            "The Portuguese base is structural (braising methods, acid use, whole-animal cookery, pastry). "
            "The Malay base is aromatic (rempah, spice paste, coconut milk, fermented seafood). "
            "The Goan-PCT8 connection is the bridge between the Iberian origin and the Southeast Asian arrival."
        ),
        "common_mistakes": (
            "Treating the PCT as a single direction of influence — the Malay culinary tradition fundamentally transformed the Portuguese base, not just 'added spice to it'. "
            "Ignoring the Goan-Malacca food connection — bebinca and vinha d'alhos demonstrate direct Goa-Malacca culinary transfer. "
            "Treating Kristang cuisine as a dead tradition — it is an active, living culinary system in Malacca. "
            "Assuming Portuguese elements dominate — in most Kristang dishes, the Malay aromatic contribution is the majority of the flavour character."
        ),
        "pro_tips": (
            "When presenting Kristang dishes in a professional culinary context, the PCT framework provides an educational structure for guests: 'This is what happens when Portuguese cooking and Malay cooking meet in the Straits of Malacca.' "
            "The Goan bebinca connection is the strongest evidence of direct Goa-Malacca culinary transfer along the Portuguese colonial trade route. "
            "Arroz de coco (coconut rice) in Portuguese and Malay nasi lemak are independent parallel developments of the same basic idea — useful cross-cultural contrast. "
            "The Kristang community's official document of cultural practices is maintained by the Persatuan Kebajikan & Kebudayaan Kristang (Kristang Welfare & Cultural Association) in Malacca."
        ),
        "trigger_keywords": json.dumps(["PCT-9", "Portuguese Colonial Trail Malacca", "Kristang culinary lineage", "Malacca Portuguese heritage", "colonial food trail", "Portuguese culinary ancestry", "Kristang food history"]),
        "authority_tier": 1,
        "lives_or_dies": "For culinary professionals, the PCT-9 understanding lives or dies on whether the Goan connection is made. Kristang cuisine that is presented as purely Portuguese-Malay synthesis misses the Goa node — the vinha d'alhos-vindaloo-carne assada connection that demonstrates the Indian Ocean trade route carried culinary technique as efficiently as spices.",
        "flavour_context": "PCT-9 is not a single flavour but a framework for understanding why Kristang cuisine tastes the way it does. The Portuguese base explains the vinegar-depth and the structural braise techniques; the Malay node explains the aromatic brightness; the Goan node explains the mustard seeds and bebinca; the five-century local community explains the festival sweet tradition."
    },
    {
        "name": "Kristang sambal belacan: pounded condiment technique",
        "category": "Kristang — Sambal & Condiments",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Sambal belacan is the foundational Kristang table condiment — fresh or dried bird's eye chilies pounded with toasted belacan and calamansi juice, producing a fiery, intensely fermented, sour-savoury paste served in a small dish alongside almost every Kristang meal. "
            "It is the condiment equivalent of the Malay 'all-purpose sauce' — functional on rice, with grilled fish, alongside pork dishes, and as a dipping condiment for shellfish.\n\n"
            "Preparation: bird's eye chilies (cili padi — the small, intensely hot Southeast Asian chili) are pounded coarsely with toasted belacan in a mortar and pestle. "
            "The pounding is deliberately coarse — sambal belacan should have visible chili texture rather than a smooth paste; the bite of chili pieces is part of the eating experience. "
            "Fresh calamansi juice is squeezed in after pounding and mixed in — the ratio is approximately 1 tablespoon calamansi juice per 2 tablespoons pounded chili-belacan. "
            "Thinly sliced shallots are optionally added and lightly pounded to just bruise them — they add a sweet onion note without becoming dominant.\n\n"
            "The Kristang version is slightly more restrained in belacan intensity than the Malay version — reflecting the Portuguese influence that prefers a less fermented-dominant condiment — but the calibration is subtle. "
            "Heat level: Kristang sambal belacan made with predominantly bird's eye chili is intensely hot — it is a condiment used in tiny quantities, not a dipping sauce applied generously. "
            "A small quantity on the side of rice absorbs into the mouthful and amplifies the flavour of whatever it accompanies."
        ),
        "key_principles": (
            "Coarse pound — visible chili texture is correct; smooth paste is over-pounded. "
            "Calamansi juice after pounding — the acid activates the fermented compounds. "
            "Bird's eye chili (cili padi) for authentic heat — larger mild chilies produce a different condiment. "
            "Make fresh and serve immediately — sambal belacan loses complexity within hours."
        ),
        "common_mistakes": (
            "Over-pounding to a smooth paste — loses the textural identity. "
            "Omitting calamansi — the condiment is flat and one-dimensional without the acid. "
            "Making in advance — fresh sambal belacan has volatile compounds that dissipate within hours. "
            "Using untoasted belacan — raw belacan produces an ammonia note rather than roasted depth."
        ),
        "pro_tips": (
            "The calamansi juice is not just acid — it interacts with the belacan compounds to produce a combined sour-umami note that neither provides alone. "
            "For professional service: prepare sambal belacan at the last moment before service, or at most 30 minutes prior. "
            "Using a small granite mortar (not a large batch blender) is essential — the coarse crush from the mortar is structurally different from a blender chop. "
            "The Kristang standard: sambal belacan should make you catch your breath from the chili heat and immediately want to eat it again because of the complex sour-savoury-fermented depth."
        ),
        "trigger_keywords": json.dumps(["sambal belacan", "Kristang sambal", "pounded chilli belacan", "Malacca table condiment", "cili padi sambal", "Kristang condiment", "sambal belacan technique"]),
        "authority_tier": 1,
        "lives_or_dies": "The freshness. Sambal belacan made 3 hours ago has lost most of its volatile aromatic compounds — it tastes salty and hot, but the complex layering of fermented-sour-aromatic is gone. The 15-minute-old sambal belacan is a completely different condiment from the 3-hour-old one.",
        "flavour_context": "Intense, hot, fermented, sour — the condiment of maximum sensory impact in the Kristang kitchen. Bird's eye chili heat that builds on the palate; the fermented savoury depth of toasted belacan; the bright cut of calamansi juice. Used sparingly, it amplifies everything it touches. A small Kristang kitchen delivers this condiment with quiet confidence."
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
print(f"\nBatch 7 complete: {inserted}/{len(entries)} inserted")
