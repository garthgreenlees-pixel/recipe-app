-- East Asian Phase 6: Chanoyu Service Protocols
-- 8 entries in service_protocols table
-- Columns: name, category, beverage_family, description, procedure, rationale,
--          common_errors, service_context, equipment_required, guest_communication,
--          authority_tier, skill_level, is_published

BEGIN;

INSERT INTO service_protocols (name, category, beverage_family, description, procedure, rationale, common_errors, service_context, equipment_required, guest_communication, authority_tier, skill_level, is_published) VALUES

-- 1. Usucha
(
  'Usucha — Thin Matcha Preparation',
  'tea_service',
  'tea',
  'Usucha is the foundational form of matcha preparation in chanoyu, producing a frothy bowl of vibrant green tea served individually to each guest. The technique emphasises rhythmic W-motion whisking, proper chakin cloth use, and the meditative sequence of fukusa purification of utensils. Usucha forms the second half of a formal chaji after koicha, and is the primary form served in informal chakai gatherings.',
  'Boil fresh water and cool to 70–75°C. Warm the chawan with hot water; discard and dry thoroughly with chakin. Ritually purify the natsume (tea caddy) and chashaku (tea scoop) with fukusa silk cloth. Sift 1.5–2 chashaku measures (approximately 2g) of ceremonial-grade matcha directly into the warmed, dry chawan. Add 60–70ml of 70–75°C water. Hold the chawan firmly with one hand; whisk with the chasen using rapid W-shaped strokes for 15–20 seconds until fine microfoam forms. Finish with a final smooth circular stroke to consolidate foam in the centre. Present the bowl with its front (omote) facing the guest. Inform the guest to rotate the bowl twice before drinking — this is not mere etiquette but a signal of respect for the craftsperson who made the bowl.',
  'Usucha embodies ichi-go ichi-e (one time, one meeting) — each bowl is prepared for this moment alone. The W-motion produces fine, stable microfoam by creating turbulence across the full whisking surface. Water at 70–75°C preserves the L-theanine responsible for matcha''s characteristic umami sweetness; higher temperatures destroy this compound and produce bitterness. The ritual purification of utensils with fukusa is not theatre — it focuses the host''s attention and signals to guests that the preparation is beginning.',
  'Using boiling water is the single most common and most damaging error — it destroys umami and produces harsh bitterness. Not warming the chawan causes uneven whisking and premature cooling. Over-packing the chashaku (scoop) results in a paste that resists foam formation. Circular whisking instead of W-motion produces large, coarse bubbles rather than fine microfoam. Presenting the front of the bowl without instructing the guest to rotate it breaks the etiquette that protects the bowl''s most beautiful face.',
  'fine_dining',
  ARRAY['Chawan (tea bowl)', 'Chasen (bamboo whisk, 80–100 tine for usucha)', 'Chashaku (bamboo tea scoop)', 'Natsume (lacquered tea caddy)', 'Fukusa (silk purification cloth)', 'Kensui (waste water bowl)', 'Chakin (white linen tea cloth)', 'Fine-mesh sifter'],
  'Describe usucha as the ''everyday'' form of chanoyu matcha — frothy, bright, and invigorating. Invite the guest to observe the preparation. When presenting, indicate that the bowl should be rotated twice before drinking so they do not sip from the most beautiful face. Mention the producer and cultivar: "This is Ippodo Ummon from Uji — a ceremonial grade made from Gokou cultivar shade-grown for 30 days."',
  2,
  'advanced',
  true
),

-- 2. Koicha
(
  'Koicha — Thick Matcha Preparation',
  'tea_service',
  'tea',
  'Koicha (thick tea) is the highest form of matcha preparation in chanoyu — reserved for formal chaji and requiring only the finest single-estate ceremonial-grade matcha. Unlike usucha, koicha is kneaded rather than whisked into a thick, paste-like consistency, then shared from a single bowl among all guests. This act of sharing from one vessel is the embodiment of chanoyu''s most profound social philosophy. Only matcha from the most established Uji tea families is appropriate.',
  'Select koicha-grade matcha from an established Uji producer (Ippodo Ummon or Marukyu Koyamaen Wako are the benchmarks). Boil fresh water; cool to 80°C — slightly higher than usucha to aid dissolution of the larger dose. Warm and dry the chawan thoroughly; koicha chawan are typically deeper and more sober than usucha bowls. Measure 3–4 chashaku scoops (approximately 6–8g) into the chawan. Add only 30–40ml of 80°C water — far less than usucha. Knead slowly and deliberately with the chasen using a figure-8 motion for 60–90 seconds until the tea is smooth, paste-like, glossy, and completely free of bubbles. Present to the first guest (shokyaku). Guests share the bowl in succession, each drinking a portion and wiping the rim with kaishi paper before passing.',
  'Koicha is the centrepiece of a formal chaji — it precedes usucha and represents the fullest expression of the gathering''s intention. The kneading motion (rather than whisking) produces a smooth, dense liquid without foam — koicha should have no bubbles. The shared bowl is not merely a practical choice; it is a philosophical statement that rank, wealth, and social distinction are equalised within the tea room. The cha-ire (ceramic container) used for koicha is typically an antique and may be the most valuable object in the room.',
  'Using usucha-grade matcha produces a koicha that is harsh and bitter at high concentration. Adding too much water makes the tea thin and runny rather than coating the sides of the bowl. Whisking instead of kneading creates foam completely inappropriate to koicha aesthetics. Rushing the preparation breaks the meditative atmosphere that koicha requires. Using a natsume (lacquered usucha caddy) instead of a cha-ire (ceramic koicha container) signals ignorance of the ceremony''s structure.',
  'fine_dining',
  ARRAY['Chawan (deep, sober koicha bowl)', 'Chasen (80-tine whisk, used for kneading)', 'Chashaku (tea scoop)', 'Cha-ire (ceramic tea container with shifuku silk pouch)', 'Fukusa (silk cloth)', 'Chakin (tea cloth)', 'Kaishi paper for guests'],
  'Explain to guests that koicha is shared from a single bowl — this is intentional and central to the ceremony''s meaning. The first guest (shokyaku) receives the bowl, drinks approximately one-third, wipes the rim with kaishi paper, and passes to the next guest. If guests are unfamiliar: "This bowl is shared among all of you as an act of connection — the tea at this concentration has almost no astringency, only deep umami and a lingering sweetness." Identify the matcha by producer and grade.',
  2,
  'master',
  true
),

-- 3. Kaiseki integration
(
  'Chaji Kaiseki — Tea Ceremony Meal Sequence',
  'tea_service',
  'tea',
  'In a formal chaji (full tea ceremony), kaiseki (懐石) is the ritual meal served before the tea. This is distinct from modern restaurant kaiseki — chanoyu kaiseki is minimal, seasonal, and purposefully humble, designed to prepare the palate for the intensity of koicha that follows. The host serves in silence; food is never the point. Understanding this sequence is essential for hospitality professionals working with Japanese tea culture or designing tea-inspired tasting menus.',
  'The chaji kaiseki follows a fixed sequence: Mukouke (向付) — seasonal raw preparation, typically sashimi or marinated vegetables in individual dishes. Wan (椀) — clear osuimono soup with a seasonal garnish, served hot in lacquered bowls. Yakimono (焼物) — small grilled item, typically fish, on individual ceramic plates. Sake service: host pours from tokkuri into ochoko cups; no more than 2–3 modest pours. Hassun (八寸) — a cedar tray with two items: one from the mountain (vegetables), one from the sea. Ko no mono (香の物) — pickles served with rice for palate cleansing. Yuto/Kogashi (湯斗) — hot water poured over scorched rice crust. Nakadate (中立) — intermission where guests walk the roji garden while the host prepares for tea. The entire sequence takes 60–90 minutes.',
  'Chanoyu kaiseki exists entirely in service of the tea that follows. Each course is calibrated to build and then cleanse the palate — the arc moves from delicate (sashimi) through umami depth (clear soup) to cleansing (pickles, rice). Sake is symbolic rather than convivial; excess disrupts the meditative preparation for koicha. The meal is never announced or explained — its appearance and disappearance are acts of hospitality without performance. For a contemporary hospitality team, the philosophy of purposeful restraint — every course in service of an overarching intention — is directly translatable.',
  'Over-elaborating courses violates the fundamental principle: kaiseki celebrates seasonal impermanence, not abundance. Explaining each course breaks the meditative atmosphere. Serving sake generously disrupts the clarity of mind needed for the tea that follows. Using imported or out-of-season ingredients is a philosophical contradiction. Allowing the meal to expand beyond its allotted 60–90 minutes compresses the tea ceremony that is the purpose of the gathering.',
  'fine_dining',
  ARRAY['Lacquered zen (individual tray stands)', 'Seasonal ceramics for each course', 'Cypress (hinoki) hassun tray', 'Individual tokkuri and ochoko for sake', 'Cast-iron kama (kettle) on ro or furo'],
  'For guests unfamiliar with chaji: "The meal you are about to experience exists entirely to prepare you for the tea. Each course is small and precise — the intention is not to fill you but to tune you." After the intermission: "The tea room is now prepared. Please rinse your hands at the tsukubai as you enter." Encourage silence once the roji walk begins.',
  1,
  'master',
  true
),

-- 4. Ichi-go ichi-e philosophy
(
  'Ichi-go Ichi-e — The Philosophy of Unrepeatable Service',
  'sommelier_approach',
  'tea',
  'Ichi-go ichi-e (一期一会, one time, one meeting) is the philosophical heart of chanoyu — the recognition that every encounter is unique and will never recur exactly. This principle, articulated by Sen no Rikyu in the 16th century, has profound implications for hospitality professionals far beyond tea service. When applied deliberately, it transforms every guest interaction from a transaction into an event worthy of full presence and care.',
  'Begin by internalising the principle: this guest, this table, this moment will not recur. Before service, complete the mise en place not as routine but as preparation for a specific person. Enter the service sequence with the same deliberateness a host enters the tea room. Make choices — selection of glassware, arrangement of the table, the first words spoken — as if they are the only choices. During the encounter, resist the pull of distraction: other tables, incoming orders, phone notifications. When the guest leaves, do not immediately redirect — allow a moment of closure. In chanoyu, the roji walk after a chaji is time for reflection on what occurred.',
  'Sen no Rikyu taught that the four principles of chanoyu are wa (harmony), kei (respect), sei (purity), and jaku (tranquillity). These are not aesthetic guidelines but states of being cultivated through practice. For hospitality, wa means reading the table''s social dynamic; kei means honouring the guest''s time and trust; sei means precision and cleanliness in every detail; jaku means remaining unruffled regardless of kitchen delays, difficult guests, or personal distraction. The world''s greatest service professionals — whether in Tokyo, Copenhagen, or Vancouver — are practising ichi-go ichi-e without necessarily knowing the name.',
  'Treating every service as identical — the opposite of ichi-go ichi-e — produces technically correct but emotionally inert hospitality. Multitasking during a guest interaction signals that this moment is not unique. Over-scripting responses removes presence and replaces it with performance. Forgetting that restraint (what is not said, not placed, not poured) is as important as action.',
  'staff_training',
  ARRAY['No equipment required — this is a state of mind and practice'],
  'Share this principle with guests explicitly at high-value service moments: "In the Japanese tea tradition, there is a concept — ichi-go ichi-e — one time, one meeting. We try to approach every table with that intention. This evening will not happen again quite like this." For hospitality teams: introduce this as the philosophical frame for all pre-service briefings. Ask: what is unique about tonight? What will not recur? Let the answers shape the service.',
  1,
  'advanced',
  true
),

-- 5. Chanoyu dōgu utensil selection
(
  'Chanoyu Dōgu — Utensil Selection and Appreciation',
  'tea_service',
  'tea',
  'In chanoyu, the utensils (dōgu, 道具) are not tools but participants. The selection of chawan, chasen, chashaku, natsume, and cha-ire for a gathering is a creative, seasonal, and philosophical act. Sen no Rikyu elevated Korean and Japanese peasant pottery above Chinese imported wares, permanently shifting Japanese aesthetic culture. For the beverage professional, understanding dōgu enables credible engagement with guests who are knowledgeable about Japanese tea, and reveals how material culture shapes the experience of drinking.',
  'Chawan (茶碗): select for season — thick-walled in winter for warmth retention, wide-mouthed in summer for cooling. The three most respected styles: Raku (hand-formed, low-fire, Kyoto), Hagi (high-fire, porous, Yamaguchi), Karatsu (Korean-influenced, Kyushu). Chasen (茶筅): made in Takayama, Nara by a single family lineage for 500 years; 80-tine for koicha, 100–120-tine for usucha. Replace when tines splay or break — do not use a damaged chasen. Chashaku (茶杓): hand-carved from a single piece of bamboo; each is named by its carver with a poetic title. Natsume (棗): lacquered caddy for usucha matcha — selected by finish and season. Cha-ire (茶入): ceramic container for koicha; typically antique, with its own shifuku silk pouch and inscribed box. Clean all utensils with hot water and chakin only — no soap, ever.',
  'Every utensil in chanoyu carries history, intention, and aesthetic meaning. A Raku chawan used for decades develops yōhen — a patina of use that is part of its beauty and cannot be manufactured. The deliberate selection of wares that speak to each other across centuries (a 16th-century cha-ire with a contemporary chawan made in its spirit) is the host''s creative contribution to the gathering. For the hospitality team, this is the model for tableware curation: each piece chosen for its relationship to the season, the guest, and the intention, not simply for completeness of a set.',
  'Prioritising expensive over authentic — a humble Iga-ware chawan used for decades is more resonant than a pristine acquisition. Matching all utensils by period or style removes the creative tension that makes chanoyu alive. Over-polishing ceramics removes the accumulated beauty of use. Washing utensils with detergent destroys the oils that season and protect the ware.',
  'fine_dining',
  ARRAY['Chawan collection (seasonal range)', 'Chasen and chasen stand', 'Natsume set (seasonal)', 'Cha-ire with shifuku pouch', 'Named chashaku in bamboo tube', 'Kama (iron kettle)'],
  'When presenting matcha to a guest with apparent knowledge: name the chawan''s style and approximate period — "This is a Hagi-ware bowl from Yamaguchi, 1970s, by Miwa Kyusetsu''s school." If a guest asks about the whisk: "The chasen comes from a single workshop in Takayama, Nara — the same family has been making them for 500 years, each hand-tied from a single piece of bamboo." For educational service moments: place the named chashaku (tea scoop) visible on the presentation tray.',
  2,
  'advanced',
  true
),

-- 6. Ceremonial matcha — restaurant and bar context
(
  'Ceremonial Matcha — Restaurant and Bar Service',
  'tea_service',
  'tea',
  'Translating chanoyu matcha preparation into a contemporary restaurant or café context requires maintaining the essence of the ritual — presence, precision, quality — while adapting for professional service throughput. A well-executed matcha service signals depth of beverage knowledge and provides a genuinely distinctive guest experience. This protocol covers both tableside preparation and bar-prepared ceremonial matcha service.',
  'Source only ceremonial-grade matcha: Ippodo Ummon or Kan-un, Marukyu Koyamaen Wako or Aoarashi. Store sealed and refrigerated at 4°C; bring to room temperature 30 minutes before service to prevent condensation contamination. Warm the chawan with boiling water; discard and dry completely. Sift exactly 2g matcha into the warmed bowl — sifting is non-negotiable at this price point. Add 70ml of precisely 75°C water (temperature-controlled kettle required). Whisk with chasen in W-motion for 20 seconds to fine foam. Present immediately — matcha oxidises; whisk-to-guest must be under 90 seconds. For tableside service: pre-measure and sift matcha into a small covered vessel; add water and whisk in front of the guest. For a bar programme: prepare to order using identical protocol; never pre-batch.',
  'Ceremonial matcha served at 75°C (water temperature) arrives at the guest at approximately 65–68°C — the ideal drinking temperature. The sifting step removes all clumps before water contact, enabling a smooth, even foam. Using ceremonial-grade matcha (Ippodo Ummon is $80–120 per 40g) at this precision produces a flavour profile that cannot be achieved with culinary grades: deep umami, long sweetness, vivid colour, zero bitterness. The cost per serving is $4–6 — justified at a menu price of $18–28 as a beverage course.',
  'Skipping sifting produces visible clumps in the foam — unacceptable at any price point. Using water above 80°C is the most common error and produces immediate bitterness. Preparing in advance — matcha must be made to order; foam deflates in under 3 minutes. Using culinary-grade matcha for ceremonial service — the colour difference alone is visible from across the table.',
  'fine_dining',
  ARRAY['Chasen (bamboo whisk)', 'Fine-mesh sifter (60–80 mesh)', 'Temperature-controlled kettle (set to 75°C)', 'Ceramic chawan or equivalent bowl', 'Chakin or clean linen cloth', 'Pre-measured matcha vessel for tableside service', 'Digital scale'],
  'Introduce the matcha by producer and grade: "This is Ippodo Ummon from Uji, Kyoto — a ceremonial-grade matcha made from Gokou cultivar, shade-grown for 30 days. The powder is bright green, and the taste will be intensely umami with no bitterness." For pairing recommendations: "We pair this with a single piece of seasonal wagashi to balance the savouriness of the tea." BC sources to mention: Fujiya Foods on Robson Street stocks Ippodo; T. Amano Foods carries Marukyu Koyamaen.',
  2,
  'advanced',
  true
),

-- 7. Gyokuro cold brew
(
  'Gyokuro Slow Cold Brew — Professional Preparation',
  'tea_service',
  'tea',
  'Gyokuro (玉露, jewel dew) is the pinnacle of shaded Japanese green tea — grown under 90% shade cover for 20–30 days before harvest, suppressing catechins (bitterness) and amplifying L-theanine (umami sweetness). Traditional preparation uses remarkably cool water and small volumes to produce a thick, savoury, broth-like liquor with minimal astringency. Gyokuro cold brew extends this principle: 8–12 hours of cold extraction produces a concentrated, emerald-green beverage of extraordinary depth appropriate for fine dining beverage programmes.',
  'Source single-origin Uji gyokuro: Ippodo Sayamakaori or Marukyu Koyamaen Unkaku. Use filtered, soft water at 4°C. Measure 10g gyokuro per 200ml water (a 1:20 ratio, much richer than standard cold brew). Combine in a sealed glass vessel. Steep in the refrigerator for 8–12 hours — do not exceed 14 hours. Strain through a fine-mesh sieve using gravity only; do not press the leaves. The resulting liquor is deep emerald, slightly viscous, intensely savoury with a long umami finish. Serve in small vessels (40–60ml per portion) at 8–12°C. Optional: add a single drop of fresh yuzu juice as a modern counterpoint. The spent leaves may be seasoned with soy and sesame for a staff meal.',
  'Cold water extraction at 4°C selectively extracts L-theanine (amino acid, savoury) while leaving the majority of catechins (polyphenols, astringent) in the leaf. This produces a flavour profile opposite to hot extraction: intense umami with almost no bitterness. The 1:20 ratio reflects gyokuro''s density relative to standard green teas. At 40–60ml per serving, a single batch (200ml) serves 3–4 guests as a beverage course. Cost per serving at Ippodo Sayamakaori pricing: approximately $3–5 — appropriate for a pre-starter or pre-dessert placement.',
  'Using warm or hot water on gyokuro destroys the L-theanine structure and creates astringency that defeats the purpose. Steeping beyond 14 hours over-extracts bitter compounds even at cold temperatures. Pressing the leaves during straining forces bitter catechins into the liquor. Serving in a large glass misrepresents the concentration — gyokuro cold brew is an amuse, not a pint.',
  'fine_dining',
  ARRAY['Glass or ceramic cold steep vessel (sealed)', 'Fine-mesh sieve', 'Small serving glasses (40–60ml)', 'Digital scale', 'Refrigerator space for overnight steep', 'Soft filtered water'],
  'Describe gyokuro cold brew in terms guests understand: "This is cold-brewed gyokuro — it has been steeping overnight at 4°C. The result is more like a savoury broth than a tea. The shade-growing process that produces this tea suppresses bitterness and amplifies a compound called L-theanine — the same molecule responsible for the calm focus that follows matcha." Serve as a pre-starter or pre-dessert amuse. Mention that Ippodo Sayamakaori and Marukyu Unkaku are available in Vancouver through Fujiya Foods.',
  2,
  'advanced',
  true
),

-- 8. Sencha daily service
(
  'Sencha Daily Service — Hospitality Context',
  'tea_service',
  'tea',
  'Sencha (煎茶) is the everyday green tea of Japan, accounting for approximately 80% of domestic production. Its preparation requires significantly more attention than is typically given in Western contexts — water temperature and steep time are critical variables that separate a vibrant, sweet, grassy sencha from a flat or bitter one. For hospitality teams, sencha is the accessible entry point to Japanese tea culture: familiar in format, rewarding in depth, and capable of expressing terroir as clearly as wine when sourced and prepared with care.',
  'Select sencha appropriate to service context: Ippodo Shogyokuro or Marukyu Tsujikaze for fine dining; Nishide Fukamushi for a richer, umami-forward style. Heat filtered water to 70–80°C: use 70°C for premium first-flush ichibancha, 80°C for fukamushi (deep-steamed) styles. Warm the kyusu or vessel briefly; pour off. Measure 4–5g sencha per 150ml water. Add water at target temperature; steep for 60 seconds for the first infusion — set a timer without exception. Pour in a circular motion between cups to equalise the concentration; pour out completely — no water should remain on the leaves. Second infusion: 30 seconds at 80°C. Third infusion: 20 seconds at 85°C. Decreasing time with increasing temperature compensates for the reduced extractable compounds in later infusions.',
  'Water temperature is the single most important variable in sencha preparation. At 70°C, extraction is dominated by amino acids (sweet, umami); at 90°C+, catechins (bitter, astringent) dominate. Premium first-flush sencha contains the highest amino acid concentration of the tea year — a reflection of the leaf''s energy stores after winter dormancy. Leaving residual water on the leaves between infusions continues extraction under residual heat, producing bitterness in subsequent infusions. The multi-infusion protocol (3–4 infusions from the same leaves) is standard in Japan and should be communicated to guests as a feature, not a limitation.',
  'Using boiling water is the most common and most damaging error. Under-dosing the leaf produces thin, pale liquor. Leaving water on the leaves between infusions causes bitterness in subsequent pours. Serving in oversized cups misrepresents the concentration — sencha is served in 80–100ml yunomi cups, not 300ml mugs.',
  'fine_dining',
  ARRAY['Kyusu (side-handle teapot) or small tokoname teapot', 'Yunomi (tea cups, 80–100ml)', 'Temperature-controlled kettle', 'Timer', 'Digital scale'],
  'Describe sencha in wine-adjacent language: "This is first-flush Shizuoka sencha from Ippodo — think of it as the equivalent of a premier cru, harvested in May when the leaf energy is highest. The cultivar is Yabukita — the same relationship a Chardonnay clone has to Burgundy. We will make three infusions from the same leaves, and each one will be different." For the beverage pairing context: first-flush sencha pairs with delicate white fish, spring vegetables, tofu. BC importers: Fujiya Foods carries Ippodo sencha; order seasonal first-flush (ichibancha) in March for May arrival.',
  2,
  'intermediate',
  true
);

COMMIT;
