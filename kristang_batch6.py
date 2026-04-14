#!/usr/bin/env python3
"""Kristang PCT-9 — Batch 6: Desserts & Sweets + Bread & Pastry (12 entries)"""
import psycopg2, psycopg2.extras, re, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

entries = [
    {
        "name": "Sugee cake: Kristang semolina almond butter cake",
        "category": "Kristang — Desserts & Sweets",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Sugee cake is the prestige dessert of the Kristang kitchen — a dense, rich, golden cake made from fine semolina (suji), ground almonds, butter, ghee, eggs, and sugar, with the semolina pre-soaked in melted butter before the batter is assembled. "
            "The technique has direct roots in the Portuguese bolo de mel and Indian-Portuguese semolina cake tradition (the Goan baath and bolo sem rival), arriving in Malacca with the Portuguese colonial community in the 16th century and evolving into a distinctly Kristang preparation over 500 years.\n\n"
            "The pre-soaking is the technique's defining step: fine semolina (suji halus) is mixed with melted butter and left to absorb for a minimum of 4 hours, or overnight. "
            "This pre-hydration of the semolina grains prevents the characteristic grittiness of under-hydrated semolina cakes — without this step, the finished cake has a coarse, sandy texture that is a technical failure. "
            "After soaking, beaten eggs and sugar are folded in, followed by ground almonds (or almond flour), baking powder, and a small amount of rose water or pandan extract for fragrance.\n\n"
            "The finished sugee cake is golden, dense, and very moist — almost pudding-like in the centre while forming a firm, slightly crispy edge. "
            "It is traditionally baked in a square or rectangular tin (not a round cake pan), cooled completely, and cut into squares. "
            "The cake is glazed with royal icing or dusted with icing sugar. "
            "Sugee cake is the centrepiece of the Kristang Christmas table — no Christmas celebration is complete without it — and the quality of a family's sugee cake is a point of significant cultural pride."
        ),
        "key_principles": (
            "Pre-soak semolina in butter for minimum 4 hours — without this, the cake has a gritty texture. "
            "Fine semolina (suji halus) only — coarse semolina never fully hydrates. "
            "Fold, do not beat — over-mixing after adding eggs toughens the cake. "
            "Cool completely before cutting — the cake continues to set as it cools."
        ),
        "common_mistakes": (
            "Insufficient soaking time — gritty, coarse texture. "
            "Using coarse semolina — never fully hydrates regardless of soaking time. "
            "Over-beating the batter — tough, dense cake. "
            "Cutting while warm — the centre collapses and the squares do not hold their shape."
        ),
        "pro_tips": (
            "The butter-to-semolina ratio in high-quality Kristang sugee cake is approximately 1:1 by weight — an extraordinarily butter-rich preparation. "
            "Adding a tablespoon of brandy or Cointreau to the batter is a Kristang Christmas tradition — it adds fragrance and extends shelf life. "
            "Sugee cake keeps exceptionally well — it remains moist for 5-7 days at room temperature, or up to 2 weeks refrigerated. "
            "The quality test: a correctly made sugee cake pressed in the centre should leave a fingerprint and spring back slowly — neither bouncing back immediately (over-baked) nor staying depressed (under-baked)."
        ),
        "trigger_keywords": json.dumps(["sugee cake", "Kristang semolina cake", "Malacca Christmas cake", "suji cake", "Eurasian butter cake", "semolina cake Portuguese", "sugee kristang"]),
        "authority_tier": 1,
        "lives_or_dies": "The pre-soaking time. A sugee cake assembled without the minimum 4-hour butter soak has a gritty texture that no amount of baking corrects — the semolina grains never fully hydrate and remain perceptible as a coarse graininess against the teeth. This is the only non-negotiable step in the preparation.",
        "flavour_context": "Buttery, almond-rich, semolina-dense, with a subtle rose water or pandan fragrance — the flavour is rich and sweet without being cloying, with the semolina providing a slight earthiness that prevents the butteriness from being too heavy. The texture is the main event: dense, moist, satisfying."
    },
    {
        "name": "Sugee cake technique: semolina ghee pre-soak method",
        "category": "Kristang — Desserts & Sweets",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The pre-soaking technique for sugee cake is a specific and irreplaceable preparation method that requires detailed understanding. "
            "The fine semolina (suji halus) is heated with melted butter or ghee (the Kristang variation uses a blend of both) until the fat is fully absorbed — the mixture should look like very wet, golden sand at first, then absorb and become a cohesive, fatty, slightly firm mass over the soaking period.\n\n"
            "The ratio for the soak: 300g fine semolina to 250g clarified butter (or a mix of 150g butter + 100g ghee) — this is richer than most cake preparations and intentionally so. "
            "The mixture is allowed to cool to room temperature, then refrigerated for a minimum of 4 hours (overnight produces better results). "
            "At refrigerator temperature the soaked semolina becomes a crumbly, slightly firm, golden block that resembles shortcrust pastry crumbs. "
            "This is the correct texture — it indicates that the fat has fully coated and penetrated the semolina granules.\n\n"
            "When assembling the cake, the pre-soaked semolina is worked back to room temperature (if refrigerated) before adding the other wet ingredients (eggs, sugar). "
            "The egg-sugar mixture is beaten separately until pale and voluminous, then folded into the semolina base in three stages — alternating with almond flour additions. "
            "The folding must be complete but gentle: vigorous mixing knocks out the air from the beaten eggs and produces a denser cake."
        ),
        "key_principles": (
            "Semolina must return to room temperature before batter assembly — cold pre-soak causes butter to re-solidify and prevents even mixing. "
            "Fold in stages: one-third egg-sugar, almond flour, remaining egg-sugar in two parts. "
            "Beat the egg-sugar separately until ribbon stage — this air incorporation is the leavening. "
            "The mixture should look sandy-golden when soaked correctly — not wet, not dry."
        ),
        "common_mistakes": (
            "Working cold pre-soaked semolina — fat resolidifies and creates uneven lumps. "
            "Single addition of egg mixture — prevents even distribution and produces a streaky batter. "
            "Under-beating the egg-sugar — insufficient air incorporation produces a very dense, pudding-like (rather than cake-like) texture. "
            "Over-folding — knocks out all the air; same dense result as under-beating."
        ),
        "pro_tips": (
            "Using ghee (clarified butter) in the pre-soak adds a distinct milky-caramel note to the finished cake that pure butter alone does not provide — the traditional Kristang version uses both. "
            "The overnight refrigerated pre-soak produces a noticeably moister cake than the 4-hour version — the longer hydration time allows more complete absorption. "
            "A teaspoon of vanilla extract in the egg-sugar mixture (in addition to or replacing the rose water) is a modern Kristang adaptation that produces a slightly more Western-accessible flavour. "
            "The baked sugee cake should be tested with a skewer — it should come out with a few moist crumbs (not dry), as over-baking produces a drier cake that loses the characteristic dense moistness."
        ),
        "trigger_keywords": json.dumps(["sugee cake technique", "semolina pre-soak", "suji soak method", "Kristang cake technique", "semolina butter soak", "sugee baking method", "suji halus technique"]),
        "authority_tier": 1,
        "lives_or_dies": "The ribbon stage of the beaten egg-sugar. The eggs must be beaten until the batter flows off the beater in a continuous, slow ribbon that holds on the surface for 3-5 seconds before dissolving. Under-beaten eggs cannot create the correct texture; over-folded batter cannot maintain it.",
        "flavour_context": "The pre-soak is not a flavour technique — it is a texture technique. The flavour components (butter, ghee, semolina, almond) are the same whether pre-soaked or not. But the texture difference is dramatic: gritty and coarse without the soak, dense and smooth with it."
    },
    {
        "name": "Kristang dodol: coconut palm sugar confection",
        "category": "Kristang — Desserts & Sweets",
        "origin": "Kristang and Malay community, Malacca, Malaysia",
        "description": (
            "Dodol is the Kristang and Malay confection of coconut milk, glutinous rice flour, and palm sugar (gula melaka) — cooked together in a heavy pot over low heat with continuous stirring for 3-5 hours until the mixture reduces to a thick, dense, toffee-like sweet that sets firm on cooling. "
            "The technique is one of the most physically demanding in Southeast Asian confectionery — the cook must stir continuously without interruption for hours, preventing the thick mixture from scorching on the pot bottom.\n\n"
            "The mixture: first-press coconut milk (thick) is combined with palm sugar over moderate heat and stirred until the sugar dissolves. "
            "Glutinous rice flour dissolved in thin coconut milk is added gradually, in a thin stream, while stirring continuously. "
            "The mixture is then reduced to very low heat and stirred continuously for 3-5 hours — the correct stirring motion is a figure-eight pattern that covers the entire pot base, preventing any area from staying in contact with the heat for too long.\n\n"
            "The finished dodol is deep dark brown, thick enough to hold a wooden spoon upright, and glossy. "
            "It is poured into a greased tray or into banana leaf cups and left to cool for several hours. "
            "When set, it can be cut into squares and wrapped in banana leaf. "
            "Traditional Kristang and Malay dodol production is a communal activity — the continuous stirring is shared among multiple cooks working in shifts over an open wood fire."
        ),
        "key_principles": (
            "Continuous stirring for the entire cooking time — stopping even briefly risks scorching. "
            "Low heat after the initial boil — too much heat scorches the bottom despite stirring. "
            "Gula melaka (palm sugar), not refined sugar — the caramel-molasses quality is essential. "
            "The figure-eight stir pattern ensures the entire pot base is covered."
        ),
        "common_mistakes": (
            "Stopping stirring — scorching ruins the entire batch and the taste is impossible to correct. "
            "Too high heat — burns the mixture at the base faster than stirring can prevent. "
            "Substituting refined sugar — flat sweetness without the caramel complexity of palm sugar. "
            "Insufficient cooking time — soft, sticky dodol that does not set correctly."
        ),
        "pro_tips": (
            "Traditional Malacca dodol production uses a wood fire with a clay pot — the clay distributes heat more evenly than steel, reducing the risk of hot spots. "
            "In a professional kitchen, a heavy-based pot (cast iron or enamelled steel) over the lowest possible gas setting is the closest approximation. "
            "The final consistency test: drop a small amount from a spoon onto a plate — it should hold its shape without running and peel off the plate cleanly when set. "
            "Dodol keeps at room temperature for 1-2 weeks wrapped in banana leaf; refrigerated for up to a month."
        ),
        "trigger_keywords": json.dumps(["dodol", "Kristang dodol", "coconut palm sugar sweet", "gula melaka confection", "Malacca dodol", "dodol technique", "Malay confection Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "Continuous stirring. This is not metaphorical — stopping for even 60 seconds at the right temperature produces a scorched, bitter patch on the bottom that spreads through the entire mixture in minutes. Have multiple cooks available and stir in shifts without pausing.",
        "flavour_context": "Deep caramel-coconut, palm sugar richness, slight bitterness from the gula melaka — a confection of great depth and complexity. The palm sugar provides a caramel note that refined sugar cannot approximate; the coconut milk adds a richness that makes the sweetness round rather than sharp. Dense, chewy, deeply satisfying."
    },
    {
        "name": "Onde onde kristang: pandan glutinous rice ball technique",
        "category": "Kristang — Desserts & Sweets",
        "origin": "Kristang and Nyonya community, Malacca, Malaysia",
        "description": (
            "Onde onde (or ondeh ondeh) are small glutinous rice balls filled with a piece of gula melaka (palm sugar) and rolled in freshly grated coconut — a Peranakan and Kristang confection that is eaten as a street snack, presented as a dessert, and prepared for festivals. "
            "The technique is deceptively simple in concept and technically demanding in execution: the rice ball must be thin enough to bite through easily while being thick enough to contain the molten palm sugar filling without bursting during cooking.\n\n"
            "Dough preparation: glutinous rice flour is combined with freshly squeezed pandan juice (the green extract from pounded pandan leaves and water, strained) and a small amount of coconut milk until a smooth, pliable dough forms. "
            "The pandan juice provides the characteristic deep green colour and fresh, grassy-vanilla fragrance. "
            "Dough consistency: it should feel like soft, smooth Play-Doh — firm enough to handle but yielding under pressure.\n\n"
            "Assembly: the dough is pinched into portions (~15g each), flattened into a circle, a cube of gula melaka (or dark palm sugar, ~4-5g) is placed in the centre, and the dough is folded up and sealed tightly. "
            "The ball must be smooth with no cracks — any crack allows the molten sugar to leak into the boiling water. "
            "The balls are boiled in simmering water (not rapidly boiling — bubbles would cause them to crack) for 3-4 minutes until they float and stay floating. "
            "They are drained, rolled in freshly grated coconut, and served immediately while the sugar inside is still liquid."
        ),
        "key_principles": (
            "Pandan juice, not pandan extract or colouring — fresh-pressed juice provides both colour and fragrance. "
            "Seal completely — any crack releases the sugar into the water. "
            "Simmer gently — vigorous boiling cracks the dough. "
            "Serve immediately after rolling in coconut — the sugar inside cools and solidifies quickly."
        ),
        "common_mistakes": (
            "Cracks in the dough ball — the entire filling leaks and the ball is ruined. "
            "Vigorous boiling — bubbles batter the balls and cause cracking. "
            "Artificial pandan colouring without flavour — the fragrance is missing. "
            "Holding before service — the palm sugar cools and the effect of the molten filling is lost."
        ),
        "pro_tips": (
            "The molten palm sugar bursting in the mouth is the experiential centre of onde onde — the whole preparation serves this single moment. "
            "Freshly grated coconut (not desiccated) is essential — it must be soft and moist to adhere to the wet ball surface. "
            "A small amount of tapioca flour added to the rice flour (approximately 1:10 ratio) makes the dough more pliable and less likely to crack. "
            "The water must be at a gentle simmer when the balls are added — if it is too cool the dough becomes gluey and the balls stick together."
        ),
        "trigger_keywords": json.dumps(["onde onde", "ondeh ondeh", "Kristang onde onde", "pandan rice ball", "gula melaka ball", "Malacca onde onde", "glutinous rice ball sweet"]),
        "authority_tier": 1,
        "lives_or_dies": "The seal. A perfectly sealed onde onde delivers its payload — the molten palm sugar — in a single explosive moment when bitten. A cracked onde onde leaks into the water during cooking and arrives at the table hollow and sweet-water-soaked. The seal is the entire technique.",
        "flavour_context": "The first bite: chewy, pandan-fragrant rice dough, soft fresh coconut — then the molten palm sugar floods the mouth with warm, deep caramel sweetness. Three textures (dough, coconut, liquid sugar) and three flavour registers (pandan-grassy, coconut-sweet, palm sugar caramel) in one small ball."
    },
    {
        "name": "Kueh jala: Kristang lace crepe technique",
        "category": "Kristang — Desserts & Sweets",
        "origin": "Kristang and Malay community, Malacca, Malaysia",
        "description": (
            "Kueh jala (net cake, from 'jala' = net) is a Kristang and Malay thin lace crepe made from a thin batter of rice flour, coconut milk, eggs, and turmeric — poured through a specialised mould (the jala mould, a cup with small holes in the base) over a hot pan in a circular, net-like pattern. "
            "The result is a delicate, lacy, golden crepe that is traditionally served with chicken or lamb curry as a wrapper — the crepe is torn and used to scoop curry, providing a light, fragrant alternative to rice or bread.\n\n"
            "The batter: rice flour, coconut milk, water, eggs, and turmeric are combined and strained through a fine sieve to remove lumps — the batter must be completely smooth and thinner than standard crepe batter. "
            "Consistency check: the batter should flow through the jala mould holes without pressure, like water; if it requires squeezing, it is too thick. "
            "The jala mould is held approximately 30cm above the hot, lightly oiled pan and moved in a continuous circular motion — the batter falls in thin streams, creating overlapping circles that form the characteristic net pattern.\n\n"
            "Cooking: the crepe sets in 60-90 seconds on a medium-heat pan. "
            "It should be removed when just set and still pale gold — not browned. "
            "A folded and stacked pile of kueh jala, slightly yellow from the turmeric, is presented alongside the curry. "
            "The lace structure means each piece of kueh jala has a different amount of batter — some more solid, some almost entirely holes — creating textural variety within a single pile."
        ),
        "key_principles": (
            "Strain batter through fine sieve — any lumps block the mould holes. "
            "Batter must be water-thin — thick batter produces solid crepe, not lace. "
            "Continuous circular motion when pouring — stop and the pattern collapses. "
            "Remove when pale gold, not browned — overcooking makes them brittle."
        ),
        "common_mistakes": (
            "Batter too thick — solid, not lace; the holes are blocked. "
            "Stopping mid-circle — breaks in the pattern where the batter stops. "
            "Over-cooking — brittle, crispy kueh jala that shatters rather than folding. "
            "Insufficient oil on the pan — the delicate lace pattern tears on removal."
        ),
        "pro_tips": (
            "A jala mould can be made by puncturing a clean tin can base with a nail — the traditional kitchen improvisation. "
            "The distance between mould and pan matters: 25-30cm produces a fine, delicate lace; closer produces a denser, less defined pattern. "
            "Add a pinch of turmeric for colour but not so much that the flavour is noticeable — kueh jala should taste neutral and fragrant, not turmeric-heavy. "
            "Kueh jala is always served warm with curry — it should be made just before service, or kept warm in a covered basket."
        ),
        "trigger_keywords": json.dumps(["kueh jala", "lace crepe Kristang", "jala mould", "Malacca kueh jala", "Kristang crepe curry", "net crepe Malay", "turmeric lace crepe"]),
        "authority_tier": 1,
        "lives_or_dies": "The batter consistency. Too thick and the batter blocks the holes — what emerges is a thick splash pattern rather than a lace net. The batter must be genuinely water-thin. Test by holding the full mould over a bowl: it should flow freely and continuously through all holes without any pressure.",
        "flavour_context": "Neutral, fragrant from coconut milk, very gently flavoured — kueh jala is a vehicle rather than a flavour statement. Its role is textural: the lace structure allows curry sauce to penetrate each piece, so every mouthful combines the light crepe texture with the full flavour of the curry."
    },
    {
        "name": "Pang susi: Kristang sweet coconut buns",
        "category": "Kristang — Bread & Pastry",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Pang susi are soft, sweet, enriched buns filled with a mixture of fresh coconut and palm sugar — a Kristang pastry that demonstrates the Portuguese colonial legacy of enriched bread-making (the Portuguese pão doce, papo-seco, and bolo traditions) adapted to local Southeast Asian ingredients. "
            "The name 'pang' derives from Portuguese 'pão' (bread) and 'susi' from 'susu' (milk in Malay), indicating a milk-enriched dough — the name preserves the history of the preparation.\n\n"
            "The dough: plain flour, sugar, dried yeast, eggs, softened butter, and coconut milk — enriched similarly to brioche but less fat-heavy, producing a softer, more pillowy texture than European enriched rolls. "
            "The dough is kneaded until smooth and slightly tacky, then left to prove for 1 hour at room temperature. "
            "The filling: freshly grated coconut (not desiccated) mixed with palm sugar (gula melaka) and a pinch of salt — cooked briefly in a pan over low heat until the sugar melts and coats the coconut, then cooled.\n\n"
            "Assembly: the proved dough is divided into 50g portions, each flattened into a round, filled with 1 tablespoon of coconut filling, and the edges pinched shut and smoothed. "
            "The sealed bun is placed seam-down on a greased tray and left to prove again for 30 minutes before baking. "
            "The baked buns are glazed with an egg wash before baking (for shine) and sometimes dusted with icing sugar after cooling. "
            "The finished pang susi should be soft, pillowy, golden, and slightly sweet — the palm sugar-coconut filling gives each bite a caramel-sweet-coconut centre that contrasts with the neutral enriched bread."
        ),
        "key_principles": (
            "Fresh grated coconut only — desiccated coconut lacks the moisture that makes the filling work. "
            "Cool the filling completely before use — hot filling steams the dough and prevents proper sealing. "
            "Pinch seam completely shut — unfilled, hollow buns result from partial seals that burst during proving. "
            "Two proves (first: bulk dough; second: shaped buns) — both are necessary for texture."
        ),
        "common_mistakes": (
            "Desiccated coconut in filling — dry, crumbly filling that crumbles rather than staying cohesive. "
            "Hot filling — steams the dough from inside and prevents the seal from holding. "
            "Under-proving — dense, doughy buns without the soft, pillowy texture. "
            "Over-baking — buns become dry and the crust hardened."
        ),
        "pro_tips": (
            "The coconut-palm sugar filling can be enhanced with a pinch of salt and a drop of pandan extract — the pandan and coconut combination is a Kristang-Malay culinary signature. "
            "The baking temperature should be moderate (170-175°C) — these enriched doughs brown quickly at higher temperatures without cooking through. "
            "Pang susi, while traditionally baked, can also be steamed (mantou-style) — the steamed version is softer and whiter, a technique that shows the Chinese influence on Kristang baking. "
            "Day-old pang susi can be sliced and pan-fried in butter until golden — the caramelised exterior over the soft interior is excellent."
        ),
        "trigger_keywords": json.dumps(["pang susi", "Kristang coconut bun", "Malacca sweet bun", "Eurasian coconut pastry", "Portuguese bread Malacca", "pao susi", "coconut filled bun Kristang"]),
        "authority_tier": 1,
        "lives_or_dies": "The sealing of the bun. A pang susi with an imperfect seal will burst during the second prove or during baking — the filling expands as it heats, and if there is any weak point in the seal, the bun opens and the filling caramelises on the surface rather than staying inside. Pinch firmly and roll the sealed bun in your palms to confirm the seal.",
        "flavour_context": "Soft, slightly sweet enriched dough around a warm, caramel-sweet coconut filling — the contrast between the neutral bread exterior and the intense palm sugar-coconut interior is the experience. The butter and coconut milk in the dough add a gentle richness that makes the bun complete without the filling being overwhelming."
    },
    {
        "name": "Kristang love letters: kueh kapit wafer rolling",
        "category": "Kristang — Desserts & Sweets",
        "origin": "Kristang and Peranakan community, Malacca, Malaysia",
        "description": (
            "Kueh kapit — love letters — are delicate, thin wafers made from a batter of rice flour, coconut milk, eggs, and sugar, cooked on a pair of hinged iron moulds over a charcoal fire and rolled while still warm and pliable into tight cylinders or triangular packets. "
            "The preparation is one of the most labour-intensive in the Kristang kitchen and is traditionally made in large quantities for Chinese New Year and Christmas celebrations. "
            "The name 'love letters' refers to the shape of the rolled triangular version — resembling a folded letter.\n\n"
            "The batter: rice flour, thin coconut milk, eggs, sugar, and a pinch of salt combined until smooth and strained. "
            "Coconut milk gives the wafers their characteristic sweet, rich coconut flavour. "
            "The batter is thin — thinner than crepe batter — and produces a wafer approximately 1-2mm thick when cooked. "
            "The iron moulds are preheated over charcoal, lightly oiled, a tablespoon of batter is ladled onto the lower mould, the upper mould is pressed down, and the assembly is held over or in the charcoal for 45-60 seconds per side. "
            "The wafer is then immediately removed while warm and rolled around a dowel into a cylinder, or folded into a triangle.\n\n"
            "Speed is critical: as the wafer cools, it hardens rapidly and cannot be rolled without cracking. "
            "The entire rolling operation must occur within 15-20 seconds of the wafer being removed from the mould. "
            "Finished kueh kapit are stored in airtight tins and keep for 1-2 weeks in the tropical climate."
        ),
        "key_principles": (
            "Roll immediately while warm — the wafer hardens in seconds; delay means cracking. "
            "Batter must be water-thin — thick batter produces a chewy rather than crispy wafer. "
            "Consistent mould heat — the wafer must cook evenly; patchy heat produces unevenly browned wafers. "
            "Store in airtight tin — moisture from the air softens the wafers immediately."
        ),
        "common_mistakes": (
            "Delayed rolling — the wafer hardens before it can be shaped. "
            "Batter too thick — soft, chewy wafer rather than crispy. "
            "Uneven mould temperature — pale patches on the wafer. "
            "Storing without airtight seal — soft, limp wafers within hours."
        ),
        "pro_tips": (
            "Traditional kueh kapit production uses cast iron moulds with decorative pressed patterns — the pattern is transferred to the wafer surface and is part of the visual identity. "
            "A production rhythm of two people works well: one cooking, one rolling — maintains the speed required. "
            "The flavour of kueh kapit is almost identical to a Dutch stroopwafel batter — both are thin caramelised wafers with coconut or vanilla sweetness. The similarity demonstrates how colonial baking traditions converged across cultures. "
            "Pandan extract added to the batter produces green kueh kapit — a variation common during Chinese New Year."
        ),
        "trigger_keywords": json.dumps(["kueh kapit", "love letters cookie", "Kristang wafer", "Malacca love letters", "Eurasian wafer biscuit", "Chinese New Year wafer", "coconut wafer Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "The 15-second window after leaving the mould. In that time the wafer goes from perfectly pliable (rollable) to partially set (rollable with care) to fully set (unrollable without cracking). The entire production rhythm of love letter making is built around this window. Do not hesitate.",
        "flavour_context": "Crispy, coconut-sweet, slightly caramelised from the iron mould — the flavour is simple and clean, with no complexity beyond the gentle sweetness and coconut richness. The interest is entirely textural: the shattering crispness is the experience, and the flavour is the frame for that texture."
    },
    {
        "name": "Kristang egg tart: Portuguese pastel de nata adaptation",
        "category": "Kristang — Bread & Pastry",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The Kristang egg tart is the Malacca adaptation of the Portuguese pastel de nata — the custard tart that travelled from Lisbon's Jerónimos Monastery to Macau and Malacca via Portuguese colonial trade routes, arriving in the Kristang kitchen as a slightly modified version: the pastry is often a shortcrust rather than the laminated Portuguese puff pastry, and the custard is flavoured with coconut milk in place of pure cream, producing a distinctly Southeast Asian taste.\n\n"
            "The Kristang version uses a standard shortcrust pastry (butter, flour, icing sugar, egg yolk) pressed into small tart tins. "
            "The custard filling: eggs, sugar, coconut milk (replacing or blending with regular milk), and a very small amount of cornflour for stability, mixed until smooth and strained. "
            "The tarts are filled to three-quarters full (the custard expands as it heats) and baked at 200°C for 15-18 minutes — the custard must develop characteristic light brown caramelised patches on the top surface, and the pastry must be golden.\n\n"
            "The Kristang variation is sometimes further distinguished by the addition of pandan extract to the custard — producing a green-tinged egg tart with the characteristic pandan fragrance that signals Southeast Asian adaptation rather than European original. "
            "The pandan egg tart is a Kristang innovation that is now also found in Nyonya and Singaporean Chinese baking."
        ),
        "key_principles": (
            "High oven temperature (200°C) — the caramelised surface patches are essential and require high heat. "
            "Fill to three-quarters only — custard expands; overfilling produces spillage. "
            "Strain the custard — any lump or air bubble becomes visible in the set custard. "
            "Cool completely before removing from tins — warm custard is fragile."
        ),
        "common_mistakes": (
            "Low oven temperature — pale, uncaramelised custard surface. "
            "Overfilling — custard overflows and bakes onto the oven floor. "
            "Unstraining the custard — lumpy, visually imperfect tarts. "
            "Removing from tins while warm — custard collapses."
        ),
        "pro_tips": (
            "The Portuguese original uses laminated pastry (essentially rough puff) that is assembled cold and compressed into the tin — a skilled technique that produces a lighter, flakier shell than shortcrust. The shortcrust Kristang version is more accessible and still excellent. "
            "The caramelised spots on the custard surface are a quality marker: they indicate proper baking temperature and also contribute a slightly bitter caramel note that contrasts the sweet custard. "
            "Pandan extract in the custard: use sparingly — pandan is powerful and even a small amount produces a pronounced flavour. "
            "Macau custard tarts and Kristang egg tarts are 500-year-old cousins sharing the same ancestor preparation."
        ),
        "trigger_keywords": json.dumps(["Kristang egg tart", "pastel de nata Malacca", "Portuguese custard tart", "Eurasian egg tart", "coconut custard tart", "pandan egg tart", "Malacca custard tart"]),
        "authority_tier": 1,
        "lives_or_dies": "The oven temperature. The caramelised surface patches on a correctly baked egg tart are not just visual — they add a bitter-sweet caramel depth that makes the tart complete. A tart baked at too low a temperature has a uniformly pale surface and a one-dimensional sweet custard flavour. The browning is the point.",
        "flavour_context": "Silky, slightly caramelised custard in a short, buttery pastry shell — the contrast between the creamy custard and the crisp pastry is the primary textural experience. The coconut milk in the Kristang version adds a gentle sweetness and richness that distinguishes it from the original Portuguese version."
    },
    {
        "name": "Kristang pineapple tart: colonial nastar technique",
        "category": "Kristang — Bread & Pastry",
        "origin": "Kristang and Peranakan community, Malacca, Malaysia",
        "description": (
            "Pineapple tarts (nastar) are the most beloved Kristang and Nyonya festive pastry — small buttery shortcrust cookies topped with or filled with a jammy, caramelised pineapple filling, served at Chinese New Year and Christmas. "
            "The preparation requires two distinct skills: making the pineapple jam filling (cooked until thick and deeply caramelised) and making the short, crumbly, melt-in-the-mouth pastry that frames it.\n\n"
            "Pineapple jam: fresh pineapple is grated (not blended — the grating texture is important) and cooked in a wide pan with sugar and a piece of cinnamon and clove at very low heat for 1-2 hours, stirring regularly, until the mixture reduces to a thick, dark amber jam that holds its shape when a teaspoon is dropped on a cold plate. "
            "The jam must be deeply caramelised, not just reduced — the Maillard reactions in the pineapple give the filling its characteristic dark golden-brown colour and complex, bittersweet flavour.\n\n"
            "Pastry: butter, plain flour, icing sugar, egg yolk, and a small amount of cornflour are combined to a very short, crumbly dough. "
            "The high butter content is intentional and produces the characteristic melt-in-the-mouth quality. "
            "Open-top tarts: a pastry round is placed in a small tart ring, a ball of jam placed on top and shaped, and egg-wash applied around the exposed pastry. "
            "Rolled tarts: the pastry is wrapped around a ball of jam and shaped into a log or pineapple shape. "
            "Baked at 160°C for 18-22 minutes until the pastry is pale gold."
        ),
        "key_principles": (
            "Grate pineapple, do not blend — the grated texture produces better jam consistency. "
            "Cook jam to deep amber — only full caramelisation produces the correct flavour. "
            "High butter content in pastry — essential for the melt quality. "
            "Low baking temperature — the shortcrust burns easily at higher temperatures."
        ),
        "common_mistakes": (
            "Under-cooking the jam — too wet and too sweet; the tart becomes soggy and the jam lacks complexity. "
            "Blended pineapple — too smooth; loses the fibrous texture that gives the jam body. "
            "Under-butter pastry — produces a crumbly-dry result that lacks the melt quality. "
            "Over-baking — the pale golden pastry turns deep brown and loses its delicate flavour."
        ),
        "pro_tips": (
            "The cinnamon and clove in the pineapple jam is the Portuguese colonial spice signature — without these, the jam tastes only of pineapple sugar rather than complex pineapple-spice. "
            "Pressing the jam ball firmly onto the pastry base before baking prevents it from sitting loosely and falling off. "
            "Commercial nastar at Lunar New Year markets can be evaluated on the jam quality alone — dark amber, slightly chewy, deeply sweet with complex caramelised notes indicates proper jam cooking; pale golden and wet indicates under-cooked jam. "
            "Wrap finished pineapple tarts individually in small cellophane — the pastry absorbs moisture from the jam and softens within 24 hours if not sealed."
        ),
        "trigger_keywords": json.dumps(["pineapple tart", "nastar Malacca", "Kristang pineapple tart", "Nyonya pineapple tart", "pineapple jam tart", "Eurasian festive pastry", "Chinese New Year cookie Malacca"]),
        "authority_tier": 1,
        "lives_or_dies": "The jam. Under-cooked pineapple jam looks like jam but tastes like syrupy pineapple without depth — the tart becomes merely sweet. Properly caramelised jam is dark amber, slightly sticky when cool, and tastes complex: pineapple-sweet with caramel bitterness and faint cinnamon-clove warmth. The jam is the point of the tart.",
        "flavour_context": "The contrast of crumbly, melt-in-the-mouth buttery pastry against the concentrated, jammy, caramel-sweet pineapple filling — each element is simple but the combination is greater than the sum of its parts. The cinnamon and clove in the jam add a depth that makes the tart taste authentically Kristang rather than generically sweet."
    },
    {
        "name": "Bebinca kristang: layered coconut pancake technique",
        "category": "Kristang — Desserts & Sweets",
        "origin": "Goan-Kristang heritage, Malacca, Malaysia",
        "description": (
            "Bebinca (also bebinka) is a multi-layered coconut-egg sweet made by building thin layers of coconut milk-egg-palm sugar batter one at a time under a grill, each layer set and slightly caramelised before the next is added. "
            "The technique arrives in Malacca via the Goan-Portuguese colonial connection — bebinca is the signature sweet of Goa, and its presence in the Kristang kitchen marks the Goa-Malacca Portuguese trading route. "
            "The Kristang version uses palm sugar rather than Goa's white sugar, producing a darker, more complex-flavoured version.\n\n"
            "The batter: coconut milk (thick first press), eggs, palm sugar (gula melaka, dissolved and strained), rice flour, and ghee. "
            "The batter is divided into small portions — each layer requires approximately 3-4 tablespoons. "
            "The first layer is poured into a greased, heavy-based tin and grilled under a hot broiler for 3-5 minutes until just set and lightly browned on top. "
            "The second layer is poured directly over the first (still in the tin), and the process repeats for 7-10 layers — each layer adding more caramelised depth and visual striation.\n\n"
            "The finished bebinca is unmoulded cold (refrigerate for minimum 2 hours before unmoulding) and sliced to reveal the layered cross-section — each layer slightly different in shade from the caramelisation progression. "
            "The Kristang tradition serves bebinca thinly sliced at Christmas — the cross-section is the presentation, and the progressive caramelisation of successive layers is the flavour story told visually."
        ),
        "key_principles": (
            "Each layer must be set and lightly caramelised before the next is added — pouring over a raw layer merges them. "
            "Consistent layer thickness — inconsistent layers produce uneven cooking. "
            "Refrigerate completely before unmoulding — warm bebinca tears. "
            "Ghee brushed on the tin (not butter) — provides the characteristic rich flavour and prevents sticking."
        ),
        "common_mistakes": (
            "Pouring the second layer before the first is fully set — the layers merge and the layered structure is lost. "
            "Inconsistent broiler distance — some layers brown unevenly. "
            "Unmoulding while still warm — the soft, warm bebinca tears and loses its shape. "
            "Too few layers — bebinca with fewer than 7 layers lacks the characteristic visual and textural depth."
        ),
        "pro_tips": (
            "The number of layers is traditionally an odd number (7 or 9) in Goan bebinca. "
            "The palm sugar version (Kristang) is darker in colour than the white sugar version (Goan original) — the Maillard reactions in palm sugar produce a deeper caramelisation. "
            "A very thin layer of ghee brushed between each layer (after the grilling and before the next pour) adds richness and helps maintain the layer separation. "
            "Bebinca can be made 2-3 days ahead and refrigerated — the flavour deepens as the layers continue to exchange moisture overnight."
        ),
        "trigger_keywords": json.dumps(["bebinca kristang", "layered coconut pancake", "bebinka Malacca", "Goan Kristang sweet", "coconut layer cake", "bebinca technique", "Malacca layered sweet"]),
        "authority_tier": 1,
        "lives_or_dies": "Setting each layer before the next is poured. This is not optional — it is the mechanism of the entire preparation. A layer that is still liquid when the next batter is poured will merge with the fresh batter and the layered structure disappears completely.",
        "flavour_context": "Coconut-rich, caramelised palm sugar depth, slightly eggy, with a progression of caramelisation that deepens through the layers — the outer layers (most recently caramelised) are lighter; the inner layers (caramelised multiple times by the subsequent layers' grill exposure) are deeper and more complex. Each layer is a stage in a long caramelisation story."
    },
    {
        "name": "Kristang sago pudding: pearl sago setting technique",
        "category": "Kristang — Desserts & Sweets",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Sago pudding is a Kristang dessert preparation using pearl sago (tapioca pearls) set in coconut milk and palm sugar — a preparation that appears across Southeast Asia and the Pacific and connects the Kristang kitchen to the broader sago-based culinary tradition of island Southeast Asia. "
            "The Kristang version is distinguished by the use of gula melaka (palm sugar) for a deep caramel sweetness and the garnishing with freshly pressed, slightly salted coconut cream at serving — the sweet-savoury contrast between the dessert and its topping is a Kristang flavour signature.\n\n"
            "Preparation: pearl sago (small, white, completely dried tapioca pearls) is soaked in cold water for 30 minutes, drained, then simmered in water until the pearls turn from white to almost completely translucent (5-7 minutes) — each pearl should retain a tiny white dot at its centre at this point; full translucency means overcooked. "
            "The semi-cooked sago is drained and mixed with dissolved palm sugar and first-press coconut milk. "
            "The mixture is poured into moulds (individual cups or a large tray), covered, and refrigerated for minimum 2 hours until set.\n\n"
            "Service: the set sago pudding is unmoulded onto a plate or eaten directly from the cup, with a generous topping of slightly salted first-press coconut cream (santan with a pinch of salt). "
            "The salted coconut cream is the counterpoint that lifts the entire dessert — without it, the sago pudding is pleasant but unremarkable; with it, the sweet-savoury contrast is the characteristic Kristang-Malay dessert experience."
        ),
        "key_principles": (
            "Pre-soak sago before cooking — dry sago in water cooks unevenly. "
            "Cook until almost translucent with a white dot remaining — full transparency means overcooked and mushy. "
            "Set in the refrigerator for minimum 2 hours — the pudding must be completely cold before unmoulding. "
            "Salted coconut cream topping is essential — the sweet-savoury contrast defines the dish."
        ),
        "common_mistakes": (
            "Overcooked sago — completely translucent pearls dissolve into mush rather than holding their shape. "
            "Undersetting — warm sago pudding has not fully gelled and falls apart on unmoulding. "
            "Omitting the salt in the coconut cream — a sweet-on-sweet dessert without the contrast. "
            "Using thin coconut milk for the topping — insufficient richness to provide the contrast."
        ),
        "pro_tips": (
            "The tiny white dot at the centre of each sago pearl after cooking is the quality indicator — it disappears with overcooking. "
            "Gula melaka for the pudding: dissolve the palm sugar in the minimum amount of water, then strain to remove any grit or bark fragments. "
            "The pudding can be made in any mould — individual cups allow elegant unmoulding; a large tray allows slicing into squares. "
            "Pandan leaf tied into a knot and simmered with the sago cooking water adds a fragrant, grassy note to the pearls before they are mixed with coconut milk."
        ),
        "trigger_keywords": json.dumps(["kristang sago pudding", "pearl sago dessert", "sago coconut milk", "gula melaka sago", "Malacca sago pudding", "Kristang dessert sago", "sago setting technique"]),
        "authority_tier": 1,
        "lives_or_dies": "The white dot. Each sago pearl should have a tiny white dot remaining at its centre when removed from the cooking water. If all the pearls are completely translucent, they have overcooked and will dissolve rather than set in the mould. Remove from heat the moment the dot is at minimum size.",
        "flavour_context": "Mildly sweet, coconut-creamy, slightly chewy from the pearl texture — then the salted coconut cream topping arrives and the dessert becomes a contrast conversation between sweet and savoury, coconut-sweet and coconut-salt. The salt lifts the palm sugar caramel and makes it vivid."
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
print(f"\nBatch 6 complete: {inserted}/{len(entries)} inserted")
