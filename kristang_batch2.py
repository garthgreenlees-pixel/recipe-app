#!/usr/bin/env python3
"""Kristang PCT-9 — Batch 2: Fermentation & Preservation (10 entries)"""
import psycopg2, psycopg2.extras, re, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

entries = [
    {
        "name": "Cincalok: Kristang fermented baby shrimp condiment",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Kristang community and Malay Malacca, Malaysia",
        "description": (
            "Cincalok is the fermented baby shrimp condiment unique to Malacca and the surrounding coast — a dense, pungent, pinkish-grey paste of tiny udang geragau (Acetes shrimp) preserved with salt and cooked rice, then fermented in sealed jars for 3-5 days. "
            "In Kristang cooking it functions simultaneously as a condiment, a seasoning agent, and an umami amplifier, occupying the same structural position that fish sauce holds in Thai cooking or nam prik pla in Cambodian cuisine.\n\n"
            "The flavour profile of cincalok is sharply saline, intensely fermented, and distinctly oceanic — not the roasted depth of belacan but a raw, alive fermented-shrimp quality that tastes of the tidal flats of the Straits of Malacca. "
            "It is traditionally eaten as a table condiment with fresh bird's eye chili and shallot, and used as a flavouring in pork dishes, fried rice, and vegetable stir-fries. "
            "For the Kristang community it is a flavour marker of home — a taste that cannot be replicated outside Malacca's specific coast.\n\n"
            "Professional use: cincalok is added in very small quantities (1-2 teaspoons per dish) because its fermented intensity is powerful. "
            "It is never cooked for extended periods — heat kills the lactic acid bacteria and volatile fermented notes, reducing it to simple saltiness. "
            "The standard Kristang cincalok condiment is cincalok mixed with finely sliced shallots, calamansi lime juice, and thinly sliced bird's eye chilies — the acid of the lime activates the fermented compounds and creates a complex sour-savoury-spicy condiment that accompanies pork, rice, and vegetables."
        ),
        "key_principles": (
            "Add cincalok late in cooking or serve as a fresh condiment — extended heat destroys the fermented complexity. "
            "Small quantities only — it is a seasoning, not a sauce. 1-2 teaspoons per dish. "
            "Always combine with acid (calamansi, lime, tamarind) when serving as a condiment — the acid activates and brightens the fermented notes. "
            "Store in a sealed glass jar in the refrigerator after opening — cincalok is a live fermented product."
        ),
        "common_mistakes": (
            "Adding too much — the dish becomes overwhelmingly salty and fermented, masking all other flavours. "
            "Long cooking — destroys the volatile fermented compounds and reduces cincalok to plain salt. "
            "Using as a primary seasoning instead of a seasoning accent — it is not a replacement for salt. "
            "Buying substandard cincalok — low-quality brands are gluey, brownish, and taste only of salt rather than fresh fermented shrimp."
        ),
        "pro_tips": (
            "The best cincalok from Malacca has visible tiny whole shrimp and a pinkish-grey colour — not a homogenous grey paste. "
            "When used in fried rice, add cincalok in the last 30 seconds of cooking — enough to distribute heat but not enough to destroy the fermented notes. "
            "Cincalok brine (the liquid in the jar) is an excellent secret ingredient for marinades and dressings. "
            "In Sydney, Melbourne, or Vancouver, look for Malaysian-brand cincalok in glass jars at Chinese/Malay grocery stores — refrigerated section."
        ),
        "trigger_keywords": json.dumps(["cincalok", "fermented shrimp", "Malacca condiment", "udang geragau", "Kristang fermented", "cincalok paste", "Malacca shrimp paste"]),
        "authority_tier": 1,
        "lives_or_dies": "The cooking time after adding. Cincalok added too early to a hot pan loses everything that makes it distinctive — the result is indistinguishable from a pinch of salt. Add it in the last 30-60 seconds of cooking, or not at all and serve it as a raw condiment alongside.",
        "flavour_context": "Intensely saline, fermented, oceanic — raw and alive in a way that belacan's roasted depth is not. A small amount makes a dish taste more complex and complete; a large amount overwhelms everything else. Paired with calamansi and chili, it becomes a condiment of rare complexity — sour, salty, fermented, and hot in a single small spoon."
    },
    {
        "name": "Cincalok production: three-stage Malacca fermentation",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Malacca coast, Malaysia",
        "description": (
            "Traditional cincalok production follows a three-stage salt-and-rice fermentation process that has been practised on the Malacca coast for centuries, creating the lactic acid environment that transforms raw baby shrimp into a complex condiment. "
            "The process is governed by monsoon seasonality — udang geragau (Acetes shrimp) are harvested abundantly between November and January, and traditional producers process the full catch during this brief window.\n\n"
            "Stage 1 — Salting: freshly caught udang geragau are washed in multiple changes of water to remove sand and debris, then mixed with coarse sea salt at a ratio of approximately 1:3 (salt to shrimp by weight). "
            "The salted shrimp are packed into earthenware jars or glass containers. Stage 2 — Rice addition: cooked glutinous rice (a small portion, approximately 5-8% of total weight) is added to the jar and thoroughly mixed — the cooked rice provides the fermentable carbohydrates that feed the lactic acid bacteria. "
            "Stage 3 — Sealed fermentation: the jar is tightly sealed and left at ambient tropical temperature (28-32°C) for 3-5 days. The jar is opened and stirred daily to check progress.\n\n"
            "Quality markers: properly fermented cincalok turns a characteristic pinkish-grey, develops a sharp, pleasantly sour fermented smell (not rotting), and the shrimp retain their form without dissolving into slime. "
            "Over-fermentation produces a brownish, ammoniacal product. Under-fermentation produces a raw, salty shrimp product without the characteristic lactic complexity. "
            "After 3-5 days, the product is refrigerated or bottled for distribution. Unopened jarred cincalok keeps for 6-12 months refrigerated."
        ),
        "key_principles": (
            "Salt ratio is critical — too little salt allows spoilage; too much salt inhibits the lactic bacteria and prevents fermentation. "
            "Glutinous rice provides the fermentable carbohydrate — without it, the fermentation is purely proteolytic (rotting) rather than lactic. "
            "Temperature control: 28-32°C is optimal. Lower temperatures slow fermentation; higher risk pathogenic bacteria growth. "
            "Daily stirring prevents anaerobic pockets and distributes the fermenting brine evenly."
        ),
        "common_mistakes": (
            "Insufficient washing of shrimp — sand and organic debris introduce unwanted bacteria. "
            "Wrong salt ratio — either too little (spoilage) or too much (inhibited fermentation, only salty not complex). "
            "Skipping the rice — produces an ammoniacal, purely proteolytic product rather than a lactic-acid-fermented condiment. "
            "Over-fermentation — brown colour, ammonia smell, mushy texture indicate failure."
        ),
        "pro_tips": (
            "The rice-to-shrimp ratio can be adjusted for different fermented profiles: more rice = more lactic sourness; less rice = more saline seafood intensity. "
            "Professional producers in Malacca ferment in large earthenware urns (tempayan) that have been used for generations — the residual cultures in the clay accelerate fermentation. "
            "The pinkish colour comes from astaxanthin in the shrimp shells — a brownish product indicates that the shrimp have broken down too much. "
            "Cincalok production is a direct descendant of the same fermentation technology that produces Korean jeot (salted fermented seafood) — the rice addition is the shared technique."
        ),
        "trigger_keywords": json.dumps(["cincalok production", "fermented shrimp technique", "Malacca fermentation", "udang geragau processing", "lactic fermentation seafood", "cincalok making", "Malay shrimp fermentation"]),
        "authority_tier": 1,
        "lives_or_dies": "The colour and smell at day 3. Pinkish-grey with a sharp lactic-sour smell means success — the lactic bacteria are working and the product is developing correctly. Brown with an ammonia smell means failure — the proteolytic bacteria have dominated and the batch is lost. There is no rescue from an ammoniacal ferment.",
        "flavour_context": "Lactic-sour, saline, fermented-oceanic — the three sensory registers develop in sequence as fermentation progresses. At day 1 the product tastes only salty. At day 3 the lactic sourness emerges and the fermented complexity appears. At day 5 the full complexity is present. After day 7 at tropical temperatures, the complexity tips toward ammonia — the product must be refrigerated immediately."
    },
    {
        "name": "Kristang ikan masin: salt-dried fish technique",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Ikan masin (salted dried fish) is the deep-pantry staple of Kristang cooking, used in stir-fries, curries, fried rice, and as a standalone side dish. "
            "The Kristang tradition preserves fish in a specific style influenced by both the Portuguese bacalhau tradition (dry-salting) and the Malay coastal preservation method — producing a product that is distinctly more intensely seasoned than Cantonese ikan masin but less cured and dried than Portuguese salt cod.\n\n"
            "Traditional production: fresh fish (typically kurau/threadfin, tenggiri/Spanish mackerel, or kembung/Indian mackerel) are cleaned, butterflied or sliced into thick fillets, and rubbed generously with coarse sea salt at a ratio of 1:4 (salt to fish by weight). "
            "The salted fish are then sun-dried on bamboo racks for 2-4 days in the tropical heat, turned once daily, until firm and dry but not brittle. "
            "The dried fish is stored in a cool, dark place and keeps for weeks to months.\n\n"
            "In Kristang cooking, ikan masin is never used as a direct protein substitute for fresh fish — its intense saltiness means it functions more as a flavouring agent. "
            "Before use, pieces are soaked in cold water for 15-30 minutes to remove excess salt, then dried and fried in lard until golden and crispy. "
            "The rendered, crispy pieces are used to season fried rice, beans, or morning porridge. "
            "Quality marker: good ikan masin smells deeply savoury and oceanic when fried — not rancid, not musty."
        ),
        "key_principles": (
            "Soak before use — ikan masin is too salt-intense to use directly without desalination. "
            "Taste the soaking liquid — if still very salty after 15 minutes, change the water and soak further. "
            "Fry in lard until properly crispy — the Maillard reaction on the dried, salted flesh creates the characteristic nutty-savoury flavour. "
            "Use in small quantities as a seasoning, not as a primary protein."
        ),
        "common_mistakes": (
            "Using without soaking — the dish becomes inedibly salty. "
            "Under-frying — ikan masin that is not properly crisped tastes rubbery and intensely fishy rather than savoury. "
            "Using as a primary protein — its flavour intensity overwhelms rather than complements. "
            "Poor quality — rancid or musty ikan masin ruins any dish; the smell test on purchase is non-negotiable."
        ),
        "pro_tips": (
            "The best ikan masin for Kristang cooking is threadfin (kurau) — its fat content produces a richer, more complex flavour when dried and fried. "
            "After soaking, dry the fish on paper before frying — excess water causes violent splattering in hot lard. "
            "Crispy ikan masin pieces stored in an airtight jar keep for 3-4 days at room temperature and can be added to dishes as needed. "
            "The flavour parallel: ikan masin in Kristang cooking functions similarly to Italian bottarga — dried, salted, intense, used as a seasoning accent rather than a primary ingredient."
        ),
        "trigger_keywords": json.dumps(["ikan masin", "salted fish Malacca", "Kristang dried fish", "Malay salt fish", "dried fish technique", "ikan masin preparation", "Malacca preserved fish"]),
        "authority_tier": 1,
        "lives_or_dies": "The frying. Ikan masin that is insufficiently fried stays tough and has an aggressively fishy note without the nutty-savoury transformation that makes it valuable. The correct fried piece is golden, crispy, and smells of the sea but not of raw fish — the Maillard reaction has completed and the intensity has been transformed.",
        "flavour_context": "Intensely saline, oceanic, with a nutty-savoury depth when properly fried — the Maillard-fried dried fish note is distinct from any other fish flavour. A small piece in fried rice or vegetables changes the entire character of the dish from 'vegetable' to 'complete'."
    },
    {
        "name": "Kristang achar: Eurasian pickled vegetable relish",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Kristang achar is the pickled vegetable relish that accompanies the Eurasian table — a tangy, spiced condiment of cucumber, carrot, long beans, cabbage, and bird's eye chili in a turmeric-vinegar pickling liquor that bears the imprint of both Portuguese escabeche tradition and Malay acar technique. "
            "It is the table condiment that cuts the richness of pork stews and curries, provides textural contrast to soft braises, and acts as an appetite catalyst before and during the meal.\n\n"
            "Preparation: vegetables are cut into batons, salted, and left for 30 minutes to draw moisture, then rinsed and dried thoroughly — this step is critical to produce a crunchy pickle rather than a limp one. "
            "The pickling liquor is made by dissolving sugar and salt in white vinegar (or cane vinegar in traditional recipes), then frying a paste of dried chili, shallot, garlic, and fresh turmeric in peanut oil until fragrant. "
            "The fried paste is combined with the vinegar solution, poured over the dried vegetables, and left to cool to room temperature before serving. "
            "Kristang achar is not a long-fermented preserve — it is ready in 1-2 hours at room temperature and best consumed within 3 days.\n\n"
            "The critical difference from Nyonya achar (the Peranakan Chinese version): Kristang achar uses a more pronounced vinegar presence (reflecting the Portuguese escabeche influence) and is typically less sweet. "
            "Nyonya achar is usually more heavily sweetened and includes pineapple and sesame seeds. "
            "Both are important Straits Settlements pickles but they are distinct traditions."
        ),
        "key_principles": (
            "Salt and drain vegetables before pickling — removes excess moisture for crunch. "
            "Rinse and thoroughly dry after salting — excess water dilutes the pickling liquor. "
            "Fry the spice paste in oil before adding to vinegar — raw paste produces a raw, harsh pickle. "
            "Do not serve hot — achar must cool completely before the flavours integrate properly."
        ),
        "common_mistakes": (
            "Skipping the salting step — watery vegetables with diluted flavour and soft texture. "
            "Not drying vegetables after rinsing — residual water dilutes the vinegar solution. "
            "Adding raw paste directly to cold vinegar — harsh, uncooked spice flavour. "
            "Over-sweetening — obscures the vinegar's cutting function and makes it taste like a dessert pickle."
        ),
        "pro_tips": (
            "Cut all vegetables to the same size (batons approx. 5cm x 0.5cm) — uniform size means uniform texture in the finished pickle. "
            "Turmeric in the frying paste gives the characteristic golden-yellow colour — fresh turmeric produces a more vivid colour than powder. "
            "A teaspoon of peanut butter whisked into the pickling liquor is a Kristang secret — it adds body and a subtle nuttiness without being identifiable. "
            "Kristang achar improves over 24 hours as the flavours meld — make it the day before service."
        ),
        "trigger_keywords": json.dumps(["kristang achar", "Eurasian pickle", "Malacca achar", "Portuguese escabeche Malay", "turmeric pickle", "kristang condiment", "Malacca pickled vegetables"]),
        "authority_tier": 1,
        "lives_or_dies": "The texture of the vegetables. Achar that has not been properly salted and dried will be soft and limp — no amount of vinegar or spice compensates for vegetables that lost their crunch. The salting step is the only moment to build the crunch into the pickle; everything else adds flavour but crunch is structural.",
        "flavour_context": "Sharp, acidic, turmeric-warm, sweet-sour balance — a condiment of contrasts that refreshes the palate between mouthfuls of rich curry or pork stew. The vinegar front gives way to the aromatic fried spice base, then finishes with a gentle sweetness and a lingering chili warmth."
    },
    {
        "name": "Asam prawn pickle: Kristang tamarind-cured prawns",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Asam prawn pickle is a Kristang preparation of fresh prawns cured in a tamarind-chili-salt brine — a short-cure (2-4 hours) that partially denatures the prawn protein while preserving a raw-fresh quality, producing a product that occupies the textural and flavour space between a fresh prawn and a cured anchovy. "
            "It is served as a condiment alongside rice dishes and pork preparations, and is one of the more striking expressions of the Kristang affinity for acid-cured seafood.\n\n"
            "Preparation: medium prawns are shelled and deveined, then tossed with thick tamarind paste (asam pekat), sea salt, dried chili flakes, and a small quantity of palm sugar. "
            "The mixture is packed into a sealed container and refrigerated for 2-4 hours. During this time the tamarind acid partially denatures the outer prawn protein (similar to the citric acid action in ceviche leche de tigre), firming the texture and turning the exterior opaque while keeping the interior semi-translucent. "
            "The cured prawns are rinsed briefly before serving and garnished with fresh shallot and calamansi.\n\n"
            "The Kristang tradition of acid-curing seafood reflects the Portuguese escabeche inheritance — the Portuguese colonial kitchen consistently used vinegar and citrus to preserve and transform seafood in tropical climates where refrigeration was unavailable. "
            "Tamarind replaces the Portuguese vinegar here, adapted to the locally available souring agent and producing a result that is gentler and more fruity than a pure vinegar cure."
        ),
        "key_principles": (
            "Use fresh prawns only — previously frozen prawns have compromised texture that curing cannot improve. "
            "2-4 hours maximum — extended curing beyond 6 hours produces a mealy, over-denatured texture. "
            "Thick tamarind paste (asam pekat), not thin — the concentrated acid is what drives the cure. "
            "Rinse briefly before serving — removes excess surface salt and acid without undoing the cure."
        ),
        "common_mistakes": (
            "Over-curing — prawns become mealy and completely opaque rather than partially translucent. "
            "Using thin tamarind liquid — insufficient acid concentration for proper curing. "
            "Skipping the rinse — overpowering saltiness and sharpness on the palate. "
            "Using medium-large prawns — the cure does not penetrate thick prawns evenly; medium size is optimal."
        ),
        "pro_tips": (
            "The curing transforms the texture visibly: at 1 hour the exterior is opaque; at 2-3 hours the full prawn is semi-opaque with a firm but supple bite. "
            "A tiny addition of palm sugar in the cure improves the flavour integration — it rounds the tamarind sourness without sweetening the dish. "
            "Asam prawn pickle is the Kristang version of a ceviche — both are acid-cured seafood preparations. The parallel should be noted in professional contexts. "
            "Serve on banana leaf for a traditional Kristang presentation."
        ),
        "trigger_keywords": json.dumps(["asam prawn", "tamarind cured prawn", "Kristang prawn pickle", "Malacca acid cure", "asam udang", "prawn ceviche Malacca", "Kristang preserved seafood"]),
        "authority_tier": 1,
        "lives_or_dies": "The timing. At 2-3 hours, the prawn is perfectly cured — firm exterior, translucent interior, bright acid flavour. At 6 hours, it is mealy and flat. There is a 2-hour window of correct texture and it cannot be recovered from over-curing.",
        "flavour_context": "Tart-forward, saline, fresh-sweet prawn underneath — the tamarind acid transforms the flavour from raw-oceanic to bright-fruity-savoury without cooking. The texture sits between raw and cooked: firm but yielding, with a slight snap that is distinct from both fresh raw prawn and heat-cooked prawn."
    },
    {
        "name": "Tempoyak: Kristang fermented durian paste technique",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Malay-Kristang tradition, Malacca and Pahang, Malaysia",
        "description": (
            "Tempoyak is fermented durian paste — the preserved form of durian flesh that extends its seasonal availability and transforms its raw, intensely aromatic character into a more complex, sour-fermented condiment used in Malay and Kristang cooking to season fish curries, sambal, and rice dishes. "
            "Although primarily a Malay tradition, tempoyak appears in the Kristang kitchen through the community's close integration with Malay neighbours and is used as a flavouring base for certain fish preparations and as a condiment with fresh vegetables.\n\n"
            "Production: ripe durian flesh is removed from the fruit and mixed with a small quantity of salt (2-3% by weight), then packed into sealed glass jars and fermented at room temperature for 3-5 days. "
            "The fermentation is lactic — the natural sugars in durian provide the substrate — and the result is a paste that retains the characteristic durian aroma but gains a complex sourness and a slight effervescence. "
            "The texture becomes creamier and more homogenous than fresh durian as the cell walls break down.\n\n"
            "In Kristang fish cooking, tempoyak is used in small quantities (1-2 tablespoons per dish) to add a fermented-fruity-savoury depth to fish curries. "
            "Tempoyak ikan patin (fermented durian with silver catfish) is a regional speciality from Pahang that uses tempoyak as the primary seasoning — the fish is simmered in coconut milk and tempoyak until the fish is cooked and the sauce has absorbed the fermented durian complexity. "
            "The flavour is unmistakeable and deeply polarising to uninitiated palates."
        ),
        "key_principles": (
            "Use only fully ripe durian — unripe durian lacks sufficient sugar for lactic fermentation. "
            "Salt at 2-3% by weight — below 1.5% risks spoilage; above 4% inhibits fermentation. "
            "Sealed jar only during fermentation — exposure to air risks mould contamination. "
            "Check at day 3 — properly fermented tempoyak develops a pleasant sourness without the ammonia of over-fermentation."
        ),
        "common_mistakes": (
            "Using unripe durian — fermentation fails; the product is salty raw durian, not tempoyak. "
            "Too little salt — mould or spoilage bacteria dominate. "
            "Too much salt — fermentation is inhibited, product is only salty. "
            "Over-fermentation at high temperature — ammonia development from protein breakdown overwhelms the lactic sourness."
        ),
        "pro_tips": (
            "The best tempoyak uses the sweetest, creamiest durian varieties — D24 and Musang King are preferred in Malaysia. "
            "Refrigerate after 3-5 days to halt active fermentation and stabilise the product. "
            "Tempoyak keeps refrigerated for 2-3 months — the flavour continues to develop slowly. "
            "The professional note: tempoyak in a Kristang curry adds a fruit-fermented base note that is distinctive and cannot be replicated by any substitute — it is genuinely irreplaceable."
        ),
        "trigger_keywords": json.dumps(["tempoyak", "fermented durian", "durian paste Malacca", "Malay tempoyak", "lactic fermented durian", "tempoyak technique", "Kristang fermented"]),
        "authority_tier": 1,
        "lives_or_dies": "The fermentation assessment at day 3. Taste a small spoonful — it should be sour, fruity, and pungently aromatic but not ammoniacal. The durian aroma should be present but moderated, not intensified. If it smells strongly of ammonia, the protein breakdown has dominated and the batch is compromised.",
        "flavour_context": "Fermented-durian: the full spectrum of durian's fruity-custardy-sulphurous aroma now wrapped in lactic sourness and salt. Deeply complex and polarising — to those who appreciate fermented foods, tempoyak is one of the most complex single ingredients in Southeast Asian cooking. To those who find durian difficult, tempoyak is even more challenging."
    },
    {
        "name": "Kristang preserved lime: salted lime technique",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Salted preserved lime (limau masin) is a long-preserved condiment in Kristang cooking, made by packing whole or halved limes with coarse sea salt and leaving them to cure for 4-8 weeks until the skin softens, the flesh becomes translucent, and the bitter-sour character of fresh lime transforms into a complex, mellow, intensely savoury-sour preserved citrus. "
            "The technique is the Kristang expression of a preservation tradition found across many coastal cultures that produced preserved lemons in Morocco, umeboshi in Japan, and salt-pickled citrus across the Mediterranean and Arabic world.\n\n"
            "Preparation: small local limes (limau nipis — Citrus aurantifolia, the key lime variant) are used in preference to large Persian limes, as their thinner skin and higher essential oil content produce a more aromatic preserved product. "
            "The limes are washed, scored or quartered, packed into sterilised glass jars with layers of coarse salt (the salt draws moisture from the fruit by osmosis, creating its own brine), sealed tightly, and left at room temperature for a minimum of 4 weeks. "
            "The jar should be turned upside down daily for the first week to ensure even brine distribution.\n\n"
            "Use in Kristang cooking: the soft, translucent preserved skin (not the flesh, which is too intensely salty) is rinsed, finely diced, and added to fish curries and rice dishes in tiny quantities. "
            "It functions as a finishing acid and flavour amplifier — a few pieces of preserved lime rind raise a flat curry to clarity and depth without adding obvious sourness. "
            "The preserved lime skin also appears in Kristang chicken preparations and in certain cold noodle dishes as a sharp-savoury-citrus accent."
        ),
        "key_principles": (
            "Use limau nipis (key lime variant), not large Persian limes — smaller limes have thinner skin and more aromatic essential oils. "
            "4 weeks minimum fermentation — less time produces a product that is still raw-salty rather than mellow-savoury. "
            "Use only the preserved skin, rinsed — the flesh is overwhelmingly salty. "
            "Tiny quantities: 1-2 teaspoons of diced preserved rind per dish is typically enough."
        ),
        "common_mistakes": (
            "Under-curing — not enough time produces a harsh, salt-raw product without the mellow complexity. "
            "Using the flesh without rinsing — the flavour becomes overwhelming and harsh. "
            "Using large Persian limes — thicker skin takes longer to soften and the essential oil profile is different. "
            "Contaminating the jar with wet utensils — introduces bacteria that can spoil the brine."
        ),
        "pro_tips": (
            "After 4 weeks, taste the preserved rind: it should be soft, slightly slippery, salty but with a complex lime character underneath. If it is still hard or tastes only of salt, continue for another 2 weeks. "
            "Adding a few dried bird's eye chilies to the jar produces a chili-preserved lime with more complexity for curry use. "
            "The brine from preserved lime jars is as valuable as the limes themselves — a teaspoon of brine in a fish marinade adds preserved citrus depth without visible texture. "
            "Preserved lime parallels: Moroccan preserved lemons follow the exact same technique and can be used as a direct substitute when Kristang preserved lime is unavailable."
        ),
        "trigger_keywords": json.dumps(["preserved lime", "limau masin", "salted lime Malacca", "Kristang preserved citrus", "salted citrus technique", "Malacca preserved lime", "limau nipis preserved"]),
        "authority_tier": 1,
        "lives_or_dies": "The curing time. A 2-week preserved lime tastes of raw salt and bitter citrus — useful for nothing. A 6-week preserved lime tastes of complex savoury-sour-citrus depth that adds something irreplaceable to the dishes it touches. The transformation only happens with patience.",
        "flavour_context": "Mellow, salty-sour, complex citrus with a slight bitter-aromatic top note from the essential oils in the preserved rind — fundamentally different from fresh lime. The bitterness of fresh lime pith transforms into a pleasant, almost umami-adjacent savouriness after fermentation. In a curry, it adds citrus without sharpness."
    },
    {
        "name": "Kristang chilli oil: infused fat preservation method",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Kristang chili oil is an infused fat preparation — dried bird's eye chilies, shallots, garlic, and sometimes dried shrimp are slowly fried in lard or peanut oil until crispy and deeply flavoured, then the solids and fat are combined and stored as a condiment that functions simultaneously as a flavouring fat, a table sauce, and a preserving medium. "
            "The Portuguese colonial tradition of flavoured fats (notably manteca colorada — paprika-infused lard — still used in Portuguese and Spanish cooking) merges with the Malay tradition of sambal to produce something distinctly Kristang.\n\n"
            "The technique is a slow infusion: all aromatics are added to cold fat and brought up to temperature together, allowing controlled low-heat extraction of volatile compounds before the solids crisp and the Maillard reaction develops the deep savoury notes. "
            "This contrasts with a standard sambal, which uses high-heat frying. "
            "The slow technique produces a cleaner, more complex flavoured oil — shallot-sweet, garlic-deep, chili-warm — rather than the bold, direct punch of fried sambal.\n\n"
            "Storage and use: the oil and all solids are stored together in a sealed jar and keep refrigerated for 2-3 weeks. "
            "It is used as a table condiment (a spoonful over rice or noodles), as a finishing fat for stir-fries (added in the last 30 seconds), and as a flavour accent in marinades and dressings. "
            "The combination of preserved crispy aromatics and flavoured fat in a single jar is a model of Kristang culinary efficiency."
        ),
        "key_principles": (
            "Start all aromatics in cold fat and bring to heat together — this is slow infusion, not high-heat frying. "
            "Monitor carefully: shallots and garlic should become golden and crispy, not brown (bitter). "
            "Store solids and oil together — the continued infusion in the jar deepens the flavour over days. "
            "Use lard for richer, more complex results; peanut oil for a lighter version suitable for guests avoiding pork."
        ),
        "common_mistakes": (
            "High initial heat — the aromatics burn before extracting their full flavour into the fat. "
            "Discarding the crispy solids — they are the flavour, not waste. "
            "Over-crisping the garlic — it becomes bitter and sharp rather than golden and sweet. "
            "Using olive oil — the flavour is entirely incompatible with Kristang cooking and overpowers the aromatics."
        ),
        "pro_tips": (
            "Adding a small amount of dried shrimp (about 1 tablespoon per 200ml fat) to the infusion creates a more complex umami base in the oil. "
            "The temperature test: a wooden chopstick inserted in the fat should produce a steady, gentle stream of small bubbles — not a vigorous sizzle (too hot) and not silence (too cold). "
            "For a more aromatic oil, add a bruised lemongrass stalk and 2-3 kaffir lime leaves to the cold fat at the start — remove before the final solids crisp. "
            "Kristang chili oil on a bowl of plain congee is one of the great simple applications in the cuisine."
        ),
        "trigger_keywords": json.dumps(["kristang chilli oil", "Malacca infused fat", "chili lard", "Eurasian chili oil", "Kristang condiment", "shallot crisp oil", "Malacca table sauce"]),
        "authority_tier": 1,
        "lives_or_dies": "The temperature during frying. Too hot and the garlic burns in the first 2 minutes — the entire batch is bitter and must be discarded. The correct temperature produces gentle, consistent bubbling around every piece of aromatic, allowing slow extraction and gradual crisping without scorching.",
        "flavour_context": "Shallot-sweet, garlic-deep, chili-warm — the fat carries and amplifies all the volatile aromatic compounds extracted from the aromatics during the slow infusion. On rice or noodles, it adds richness, heat, and depth simultaneously. The crispy solids add texture and a concentrated burst of savoury-sweet."
    },
    {
        "name": "Batu lesung technique: Kristang mortar and pestle method",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The batu lesung (stone mortar and pestle) is the primary tool of Kristang rempah preparation and conditions the texture, flavour release, and aromatic integration of spice pastes in ways that mechanical blenders cannot replicate. "
            "While the batu lesung is categorised here among preservation tools (it is the grinding tool for cincalok sambal and preserved-lime preparations), its role extends throughout the entire Kristang kitchen.\n\n"
            "The technique is fundamentally different from blending: the pestle crushes and smears the ingredients against the mortar bowl, rupturing cell walls and releasing volatile aromatic compounds while also creating a physical friction that heats the paste slightly, beginning the aromatic extraction process before any cooking begins. "
            "Blenders shear rather than crush, producing a smoother but less aromatically complex paste — the difference is significant in finished dishes. "
            "Professional cooks who understand this use a mortar for paste preparation even when a blender is available, especially for sambal and small-batch rempah.\n\n"
            "Grinding order for full Kristang rempah: (1) dry spices, (2) hard aromatics sliced thin (galangal, lemongrass), (3) soft fresh aromatics (shallots, garlic, fresh chili), (4) wet rehydrated ingredients (soaked dried chili), (5) belacan last. "
            "This order ensures each component is fully worked before the next is added. "
            "The mortar should be preheated on a warm surface — cold granite inhibits aromatic release. "
            "The finished paste should be smooth to the eye and slightly gritty only under finger pressure — a sand-grain texture indicates under-grinding."
        ),
        "key_principles": (
            "Grind in stages: hard aromatics first, soft aromatics second, wet ingredients last. "
            "Crush and smear motion — pound to break, then push and rotate to smooth. "
            "The mortar produces a different paste than a blender — use it for sambals and small batches where flavour depth matters. "
            "Preheat the mortar in warm conditions — cold stone is less efficient."
        ),
        "common_mistakes": (
            "Adding all ingredients at once — hard aromatics prevent soft ones from grinding properly; order is critical. "
            "Only pounding, never smearing — pounding breaks structure but the smearing action against the bowl creates the smooth paste. "
            "Grinding too small a batch — the paste slides around rather than building against the mortar walls. "
            "Not cleaning the mortar between batches — residual flavours transfer; rinse and dry between uses."
        ),
        "pro_tips": (
            "For very aromatic sambals, use the mortar even for large batches — the flavour complexity of a mortar-pounded sambal is clearly distinguishable from a blended one. "
            "The size of the mortar matters: a mortar with a 20-25cm bowl diameter is the practical minimum for full rempah batches. "
            "A new granite mortar should be 'seasoned' by grinding uncooked rice in it until the rice is white rather than grey — this removes stone grit from the surface. "
            "The ideal batu lesung is granite — unpolished interior surface provides friction; polished marble mortars are decorative but functionally inferior."
        ),
        "trigger_keywords": json.dumps(["batu lesung", "mortar pestle Malacca", "Kristang grinding technique", "stone mortar Malay cooking", "rempah grinding method", "mortar paste technique", "batu giling"]),
        "authority_tier": 1,
        "lives_or_dies": "The smear. Pounding alone breaks the cells but leaves a chunky paste. The smearing motion — pushing the pestle firmly against the mortar wall in a rotating arc — is what creates the smooth, cohesive, aromatically integrated paste. A rempah that has only been pounded, not smeared, will cook differently and taste less unified than one that has been fully worked against the stone.",
        "flavour_context": "The batu lesung does not add flavour — it releases it. The crushing and smearing of galangal and lemongrass against granite produces a more complex volatile aromatic release than blading in a machine. This is not sentimentality: blind tasting consistently reveals mortar-pounded sambals as more aromatic and complex than blended equivalents."
    },
    {
        "name": "Kristang vinegar pickling: Portuguese acid preservation",
        "category": "Kristang — Fermentation & Preservation",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Vinegar-based pickling is one of the most clearly Portuguese-derived techniques in the Kristang kitchen — the Portuguese colonial tradition of escabeche (acid-preserved fried fish or meat) transferred directly to the Malacca context and blended with Malay spice and aromatics to produce the Kristang pickle tradition. "
            "While most Southeast Asian pickle traditions use either salt fermentation or quick salt-and-sugar cures, Kristang pickling is almost always vinegar-forward, reflecting the Portuguese use of vinho (wine vinegar) and later their adaptation to locally produced cane vinegar.\n\n"
            "The standard Kristang vinegar pickle uses white cane vinegar (cuka getah) as the primary acid, adjusted with sugar and salt to a sweet-sour-saline balance. "
            "The pickling liquor is heated to dissolve the sugar, combined with fried spice paste (turmeric, garlic, dried chili), and poured hot over prepared vegetables or fish. "
            "The hot pour on vegetables is a crucial technique — it slightly cooks the exterior of the vegetables, producing a consistent texture between completely raw and soft, while the hot vinegar also begins the flavour infusion immediately.\n\n"
            "The Kristang vinegar pickle is not a long-preservation method — it is designed for immediate consumption (hours to days), not weeks-long storage. "
            "This distinguishes it from Western-style vinegar canning and from Korean kimchi-style salt fermentation. "
            "The acid's primary function is flavour and textural transformation, not preservation per se — the Kristang table always had fresh produce available, and the pickle was a condiment of contrast rather than a survival food."
        ),
        "key_principles": (
            "Heat the vinegar liquor before pouring — this activates the spice paste and slightly softens the vegetable surface. "
            "Taste and balance the liquor before pouring — the ratio of vinegar to sugar to salt should produce a clear sweet-sour-saline balance. "
            "Allow to cool completely before serving — the flavour integrates only at room temperature or below. "
            "Use cane vinegar or white rice vinegar — red or balsamic vinegars are incompatible with the spice profile."
        ),
        "common_mistakes": (
            "Cold pour on vegetables — uneven flavour penetration and the spice paste settles rather than coating. "
            "Not tasting the liquor before pouring — sweet or sour imbalance ruins the finished pickle. "
            "Serving too soon — pickle needs at least 1-2 hours for flavour integration. "
            "Using malt or wine vinegar — the flavour profile overwhelms the aromatic spice base."
        ),
        "pro_tips": (
            "The classic Kristang vinegar pickle ratio: 3 parts vinegar : 2 parts sugar : 0.5 parts salt (by volume), adjusted to taste. "
            "Adding a bruised lemongrass stalk to the hot vinegar liquor before pouring infuses a subtle citrus note that elevates the aromatics. "
            "For fish escabeche (ikan goreng acar), the fried fish is submerged in the warm pickling liquor rather than having the liquor poured over — the fish rehydrates slightly in the pickle and becomes deeply flavoured through the interior. "
            "The escabeche technique is one of the clearest links between Portuguese cooking and Kristang cuisine — the Portuguese word and the technique are both preserved."
        ),
        "trigger_keywords": json.dumps(["Kristang vinegar pickle", "escabeche Malacca", "Portuguese pickle Malaysia", "cuka getah pickle", "Kristang achar vinegar", "acid preservation Kristang", "Malacca escabeche"]),
        "authority_tier": 1,
        "lives_or_dies": "The liquor balance. Too much vinegar and the pickle is harsh and one-dimensional — the spice paste is overwhelmed. Too little vinegar and it is merely sweet vegetable salad without the sharp-acid character that defines the condiment. The correct balance produces a liquid that makes your mouth water before anything touches the palate.",
        "flavour_context": "Sharp, acidic front followed by sweetness, then aromatic warmth from the fried turmeric and chili base — a three-beat flavour sequence that is complete in each mouthful. The acidity is the first impression and the last memory; the spice is the middle revelation."
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
print(f"\nBatch 2 complete: {inserted}/{len(entries)} inserted")
