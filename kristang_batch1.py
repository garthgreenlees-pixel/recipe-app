#!/usr/bin/env python3
"""Kristang PCT-9 — Batch 1: Heritage Foundations (10 entries)"""
import psycopg2, psycopg2.extras, re, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

entries = [
    {
        "name": "Kristang rempah: Eurasian spice paste foundation",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "The rempah is the structural foundation of Kristang cuisine — a pounded wet spice paste that distinguishes the cooking of the Eurasian Kristang (Cristão) community of Malacca from both its Portuguese ancestors and its Malay neighbours. "
            "The base contains shallots, garlic, galangal (lengkuas), lemongrass (serai), dried red chilies (soaked and seeded), fresh turmeric, belacan (shrimp paste), and candlenut (buah keras) as thickener. "
            "The Portuguese colonial heritage is visible in the proportions — larger allium quantities and acid-tolerance — while the Malay tradition supplies the aromatic rhizome layer and the belacan salt platform.\n\n"
            "Traditional preparation uses a batu giling (stone grinding slab) or batu lesung (granite mortar and pestle). The correct grinding order is critical: dry spices and hard aromatics first (galangal, lemongrass), then wet ingredients (shallots, garlic), and belacan last. "
            "The paste is ready when it no longer sticks to the mortar walls and produces a unified, cohesive texture. Professional kitchens using a blender must add minimal water and work in short pulses to avoid aeration.\n\n"
            "Kristang rempah differs from standard Malay rempah in two key ways: it is fried in lard rather than vegetable oil, preserving the Portuguese pork tradition; and it frequently includes a small quantity of dried shrimp or cincalok brine as a secondary umami layer. "
            "The paste 'breaks' in hot fat when correct — separating from the oil as moisture evaporates — signalling that raw allium flavour has cooked out and aromatics are active."
        ),
        "key_principles": (
            "Grind in order: hard aromatics first, wet aromatics second, belacan last. "
            "Fry in lard, not vegetable oil — the fat carries the spice character. "
            "Cook until the paste breaks from the oil (tumis until pecah minyak). "
            "Use only the inner white stalk of lemongrass — outer sheaths are indigestible. "
            "Soaked and seeded dried chilies only — never raw fresh chilies in rempah."
        ),
        "common_mistakes": (
            "Adding belacan too early in the grinding — it burns the stone and produces a harsh paste. "
            "Insufficient frying — raw shallot and garlic flavour dominates the finished curry. "
            "Too much water when blending — dilutes aromatics and produces a watery paste that spatters on frying. "
            "Using dried galangal powder as a substitute — produces a dusty, one-dimensional base."
        ),
        "pro_tips": (
            "A properly fried rempah smells sweet and complex — not raw or aggressive. "
            "The colour test: correct rempah is deep brick-red after frying; orange means undercooked, brown means scorched. "
            "Kristang cooks add a splash of water during the frying if the paste dries too fast — this extends the tumis window without burning. "
            "Rempah can be made in bulk, portioned into 100g balls, and frozen for up to 3 months with minimal flavour loss."
        ),
        "trigger_keywords": json.dumps(["kristang rempah", "Eurasian spice paste", "Malacca curry base", "kristang paste", "rempah kristang", "pecah minyak", "Malacca cuisine foundation"]),
        "authority_tier": 1,
        "lives_or_dies": "The frying stage. Rempah that is not fried long enough produces a curry with a raw, sharp taste that no amount of simmering corrects. Rempah that is over-fried produces bitterness that pervades the entire dish. The window between under and over is approximately 3-4 minutes of attentive stirring — the paste must smell sweet and complex, not raw and not scorched.",
        "flavour_context": "Deep, layered aromatic heat — galangal's pine-camphor note underpinned by the sweetness of shallots, the earthiness of turmeric, and the savoury depth of belacan. In lard, the fat carries and extends the aromatic compounds differently than vegetable oil — rounder, richer, with a pork-sweetness base note."
    },
    {
        "name": "Belacan toasting: Kristang shrimp paste activation",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Belacan — the dried, compressed fermented shrimp paste of the Malay Peninsula — enters Kristang cooking primarily through toasting, a technique that transforms its raw, pungent ammonia character into a deep, savoury, roasted umami base. "
            "Kristang cooks use a smaller quantity of belacan than purely Malay preparations, reflecting the Portuguese preference for less aggressive fermented funk, but it remains non-negotiable in all rempah and sambal work.\n\n"
            "Toasting is done directly over a gas flame or charcoal, the block of belacan placed on a folded foil parcel or the back of a wok spatula. "
            "The paste is turned repeatedly until the exterior darkens from purplish-grey to reddish-brown and the aroma shifts from raw shellfish to a roasted, almost nutty depth — typically 3-4 minutes per side. "
            "Over-toasting produces bitterness. Under-toasted belacan releases raw ammonia during frying.\n\n"
            "Quality assessment: high-grade Malaysian belacan (particularly from Penang) crumbles dry and evenly after toasting, with a consistent deep brick-red colour and no visible pink raw patches. "
            "Inferior belacan stays moist and smells aggressively of ammonia even after full toasting. "
            "In Kristang cooking, the toasted belacan is cooled and broken into the paste with the fingers before being added to the mortar."
        ),
        "key_principles": (
            "Toast over direct heat — foil-wrapped or on a spatula — until the exterior is reddish-brown and aromatic. "
            "The aroma should shift from raw shellfish to roasted and nutty — that is the signal to stop. "
            "Cool completely before adding to the mortar — hot belacan sticks and creates uneven grinding. "
            "Crumble finely with the fingers before grinding to ensure even integration."
        ),
        "common_mistakes": (
            "Not toasting at all — raw belacan adds ammonia rather than umami. "
            "Over-toasting until the surface burns — produces bitter, acrid notes that pervade the whole dish. "
            "Toasting in a dry pan rather than over flame — the steam doesn't escape properly and the paste stews rather than roasts. "
            "Using belacan from a jar (wet paste) — requires different handling and is inferior in Kristang rempah."
        ),
        "pro_tips": (
            "The ammonia smell during initial toasting is normal — it dissipates as the paste dries and transforms. "
            "Penang belacan is considered the gold standard: drier, more consistent, finer crumble than other regional varieties. "
            "If you cannot smell the shift from raw to roasted, keep going — the olfactory signal is the only reliable test. "
            "Toasted belacan can be stored in an airtight container for 1-2 weeks without quality loss."
        ),
        "trigger_keywords": json.dumps(["belacan toasting", "shrimp paste preparation", "Malay belacan technique", "kristang belacan", "fermented shrimp paste Malacca", "toasted shrimp paste"]),
        "authority_tier": 1,
        "lives_or_dies": "The smell shift. Raw belacan smells of ammonia and shellfish. Properly toasted belacan smells of roasted seafood and faint nuttiness. If you cannot clearly identify that the smell has changed, the paste is not ready. This is not a visual test — the colour change follows the smell change, not the reverse.",
        "flavour_context": "Savoury, fermented, oceanic depth — roasted quality adds complexity without the raw ammonia edge. In a curry, correctly toasted belacan is unidentifiable as a single flavour but makes everything else taste more complete and rounder."
    },
    {
        "name": "Asam jawa extraction: Kristang tamarind souring method",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Tamarind (asam jawa) is the primary souring agent in Kristang cuisine, inherited from the Malay and Indian culinary traditions of the Peninsula and used to balance the fat-richness of Portuguese-influenced stews. "
            "The Kristang application differs from Indonesian or Thai uses in its emphasis on controlled sourness — tamarind complements vinegar (in Devil's Curry) or stands alone (in ikan assam pedas), never as an overwhelming dominant.\n\n"
            "Extraction method: compressed block tamarind is broken into segments and soaked in warm water for 10-15 minutes, then worked with the fingers to dissolve pulp from seeds and fibres. "
            "The standard ratio is 1 tablespoon compressed tamarind to 4-5 tablespoons warm water for medium-sour paste. "
            "The liquid is strained through the fingers or a coarse sieve; pressed pulp is discarded. "
            "The resulting liquid ranges from pale amber (mild) to dark brown and syrupy (concentrated, used in ikan assam pedas and pork belly braises).\n\n"
            "Kristang cooks distinguish between asam muda (young, pale, very sour tamarind used in pickles and quick dressings) and ripe tamarind (darker, sweeter, used in curries and braises). "
            "Jar paste is acceptable if sourness is confirmed first — commercial pastes vary widely and some contain added sugar. "
            "The calibration test: a teaspoon of correct Kristang tamarind liquid tastes immediately sour on the front palate with a faint tannin dryness on the finish — not sweet, not flat."
        ),
        "key_principles": (
            "Use warm water for soaking — cold water produces tough, grainy extraction that never fully dissolves. "
            "Work the pulp with the fingers — squeezing mechanical force releases more souring compounds than stirring. "
            "Strain carefully — seeds and fibres in the finished dish indicate careless extraction. "
            "Adjust concentration: pale amber for gentle sourness, dark syrup for assertive sourness in ikan assam pedas."
        ),
        "common_mistakes": (
            "Using cold water — incomplete extraction, watery and flat result. "
            "Skipping the soaking stage and trying to dissolve directly in hot curry — uneven sourness distribution. "
            "Using commercial tamarind paste without tasting first — some brands are heavily sweetened. "
            "Adding too much too early — tamarind sourness intensifies with cooking, always err low and adjust at end."
        ),
        "pro_tips": (
            "Taste the tamarind liquid before adding to any dish — sourness levels vary dramatically between batches. "
            "For ikan assam pedas, use a syrupy dark extraction (1:3 ratio) — the concentrated sourness is the spine of the dish. "
            "Tamarind works synergistically with sugar — a pinch of palm sugar added alongside tamarind rounds and integrates the sourness. "
            "Frozen tamarind blocks maintain quality far better than jarred paste — store excess blocks in the freezer."
        ),
        "trigger_keywords": json.dumps(["asam jawa", "tamarind extraction", "Kristang souring", "Malacca tamarind technique", "asam paste", "tamarind Malay cooking", "ikan assam base"]),
        "authority_tier": 1,
        "lives_or_dies": "The concentration decision. Tamarind added too dilute produces a flat, one-dimensional sourness. Added too concentrated, it overwhelms the rempah aromatics and reduces the dish to pure acidity. The correct level makes the sourness identifiable but not dominant — it should make your jaw tighten slightly, not wince.",
        "flavour_context": "Tart, fruity, slightly tannic — bright sourness that integrates with spice and fat rather than competing. Ripe tamarind carries a subtle sweetness underneath the acid that young tamarind lacks, making it the preferred choice for Kristang braised meats."
    },
    {
        "name": "Lard rendering: Kristang pork fat tradition",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Lard — rendered pork fat — is the defining cooking medium that separates Kristang cuisine from Malay and Indian Muslim cooking traditions and anchors it to its Portuguese colonial heritage. "
            "The Kristang (Cristão) community of Malacca are Catholic Christians; pork fat is not forbidden, and its use in frying rempah, crisping vegetables, and enriching pastry dough is a deliberate cultural marker as much as a culinary preference.\n\n"
            "Rendering: pork back fat or leaf lard is cut into small cubes and cooked in a dry pan over medium-low heat. "
            "The fat must be rendered slowly — high heat risks burning the solid cracklings and imparting bitterness to the rendered fat. "
            "The liquid lard is strained through muslin while hot and stored in a sealed jar; refrigerated, it keeps for 2-3 weeks. "
            "Well-rendered Kristang lard is pale cream-white when cold, almost water-clear when melted, and carries a subtle pork sweetness rather than a rancid or gamey note.\n\n"
            "In Kristang rempah frying, lard produces a deeper caramelisation of shallots and galangal than vegetable oil and extends the aromatic volatiles differently — rounder, with a pork-sweetness base note that vegetable oil cannot replicate. "
            "Some Kristang cooks blend lard with a small amount of coconut oil for dishes served to guests who avoid pork fat. "
            "When lard is unavailable, duck fat is the closest substitute in depth and aroma — never neutral vegetable oils, which strip the dish of its defining character."
        ),
        "key_principles": (
            "Render slowly over medium-low heat — high heat scorches the cracklings and taints the fat. "
            "Strain through muslin while still hot — fat solidifies quickly and becomes difficult to strain cold. "
            "Store in a sealed jar in the refrigerator — lard absorbs refrigerator odours if uncovered. "
            "The cracklings (crackling residue) are salted and eaten separately — waste nothing."
        ),
        "common_mistakes": (
            "High heat — burnt cracklings produce bitter, off-flavoured fat that ruins any dish it touches. "
            "Straining when already cool — partially solidified fat blocks the muslin. "
            "Using commercial hydrogenated lard — lacks the subtle pork-sweetness of fresh-rendered fat and carries trans fats. "
            "Substituting with neutral vegetable oil — produces a curry that is technically correct but culturally and gastronomically flattened."
        ),
        "pro_tips": (
            "Leaf lard (kidney fat) renders cleaner and whiter than back fat — preferred for pastry work. "
            "Back fat gives a slightly more flavourful lard — preferred for rempah frying. "
            "Keep a small jar of cracklings salted — they are the cook's reward during prep and can garnish rice dishes. "
            "For guests avoiding pork, ghee is a more culturally resonant substitute than vegetable oil in Kristang cooking — it was used in the Indian community influence."
        ),
        "trigger_keywords": json.dumps(["kristang lard", "pork fat rendering", "Eurasian cooking fat", "Malacca lard tradition", "babi fat", "pork lard Kristang", "Catholic Eurasian food"]),
        "authority_tier": 1,
        "lives_or_dies": "The rendering temperature. Too high and the fat scorches — the bitterness is permanent and no amount of aromatics will mask it. Too low and the fat takes too long, developing an off-flavour from the extended heat exposure. Slow and patient is always correct.",
        "flavour_context": "Clean, sweet, neutral pork fat — not heavy or greasy when properly rendered. Carries aromatic compounds through the curry in a way that vegetable oil does not, linking the spice paste to the protein and sauce into a cohesive whole."
    },
    {
        "name": "Candlenut preparation: buah keras as Kristang paste thickener",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Candlenut (buah keras, Aleurites moluccanus) is the paste-thickener and emulsifier in Kristang curry rempah, replacing the more neutral thickening role of starch or flour used in equivalent European stews. "
            "The nut contributes a subtle bitterness, a creamy mouthfeel, and a binding quality that prevents oil and curry liquid from separating during long braises — making it structurally essential rather than flavour-dominant.\n\n"
            "Candlenuts must never be eaten raw — they contain saponins and mild toxins neutralised by cooking. "
            "For rempah, they are added to the mortar with the dry aromatics and ground until completely smooth before any wet ingredients are added; gritty candlenut texture in a finished curry indicates under-grinding. "
            "The correct quantity is typically 3-5 nuts per batch of rempah for 4-6 portions — too many creates a stodgy paste and suppresses aromatic brightness.\n\n"
            "Substitution: raw macadamia nuts without skins are the closest substitute in fat content and texture; raw cashews are acceptable but impart a sweeter, less bitter note. "
            "Walnuts are inappropriate — their tannins clash with the fermented and acid notes in Kristang curries. "
            "Some Kristang home cooks lightly toast candlenuts before grinding, which produces a nuttier, slightly more bitter profile suitable for dry-style curries but not for coconut-milk versions where raw nuts are preferred."
        ),
        "key_principles": (
            "Grind candlenuts first, before any wet ingredients — they require more grinding time than shallots and garlic. "
            "Grind until completely smooth — any grittiness in the paste will survive cooking and mar the finished dish. "
            "Use raw (not toasted) candlenuts for coconut-milk curries — toasted nuts compete with the fresh aromatic notes. "
            "Never eat raw candlenut — the saponins require heat to neutralise."
        ),
        "common_mistakes": (
            "Under-grinding — gritty candlenut in the finished curry. "
            "Too many candlenuts — paste becomes stodgy and suppresses galangal and lemongrass aromatics. "
            "Using toasted walnuts as a substitute — tannin clash with belacan and tamarind. "
            "Adding candlenuts to the mortar after wet ingredients — they stick to the moist walls and do not grind properly."
        ),
        "pro_tips": (
            "Soak candlenuts in cold water for 10 minutes before grinding — slightly softens and helps them break down more evenly. "
            "In a blender, process candlenuts alone first with a small amount of water before adding other paste ingredients. "
            "Macadamia nuts are an excellent professional substitute — consistent fat content and neutral flavour allow the rempah aromatics to lead. "
            "The correct amount of candlenut makes the paste feel just slightly creamy on the tongue — not thick, not thin."
        ),
        "trigger_keywords": json.dumps(["candlenut", "buah keras", "Kristang curry thickener", "Malay rempah thickener", "aleurites moluccanus", "candlenut paste", "Malacca curry technique"]),
        "authority_tier": 1,
        "lives_or_dies": "The grinding. A smooth candlenut is invisible in the finished dish — you taste its creaminess without identifying it. A gritty candlenut announces itself on the palate as a textural flaw. There is no correcting under-ground paste once the curry is cooked.",
        "flavour_context": "Subtle, fatty, slightly bitter — functions as a flavour binder rather than a flavour contributor. Its primary role is textural: adding body and emulsifying the spice paste into the coconut milk or broth so the sauce is integrated rather than separated."
    },
    {
        "name": "Coconut milk pressing: Kristang first and second press",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Freshly pressed coconut milk is the curry and dessert medium of Kristang cuisine, and the distinction between first press (santan pekat — thick milk) and second press (santan cair — thin milk) is fundamental to building curry texture and controlling richness. "
            "Packaged coconut milk dominates professional kitchens today, but understanding the original technique remains essential for quality calibration.\n\n"
            "First press: grated mature coconut flesh (brown skin removed) is squeezed through muslin or a fine sieve without added water. "
            "The liquid extracted is thick, cream-like, and rich with fat — santan pekat, used at the end of curries for enrichment and in dessert cooking where fat stability is critical. "
            "Second press: warm water is worked into the already-squeezed coconut flesh and pressed again, producing thinner milk used as the bulk cooking liquid.\n\n"
            "In Kristang curry work, thin coconut milk is added first (to build the braise liquid), then thick milk is stirred in during the final 5-10 minutes. "
            "Adding thick coconut milk too early causes the emulsion to break — the fat separates visibly into pools on the surface. "
            "If separation occurs, vigorous stirring over moderate heat with a splash of thin coconut milk can re-emulsify. "
            "For Kristang desserts such as onde onde or dodol, only thick first-press milk is used — thin milk lacks the fat needed for proper set and richness."
        ),
        "key_principles": (
            "Add thin coconut milk first to build the cooking liquid, thick milk only in the final 5-10 minutes. "
            "Never boil thick coconut milk vigorously — sustained high heat breaks the emulsion permanently. "
            "Use only fresh or high-quality canned coconut milk with no added thickeners or preservatives. "
            "For desserts, only first-press thick milk — thin milk will not set correctly."
        ),
        "common_mistakes": (
            "Adding thick coconut milk at the start of cooking — emulsion breaks under sustained heat. "
            "Boiling vigorously after adding thick coconut milk — irreversible separation. "
            "Using low-fat or 'lite' coconut milk — produces thin, watery curry with no body. "
            "Buying coconut milk with guar gum or other thickeners — masks quality defects but produces gluey texture in desserts."
        ),
        "pro_tips": (
            "Shake canned coconut milk vigorously before opening — natural separation in the can is normal and should be re-emulsified before use. "
            "The best-quality canned coconut milk is from Thailand or Sri Lanka, with fat content above 17%. "
            "For Kristang curry, stir gently after adding thick milk — stirring too aggressively also breaks the emulsion. "
            "A surface film of coconut cream rising to the top of a finished Kristang curry is a sign of quality, not a flaw."
        ),
        "trigger_keywords": json.dumps(["santan", "coconut milk pressing", "santan pekat", "santan cair", "Kristang coconut milk", "Malay coconut milk technique", "first press coconut"]),
        "authority_tier": 1,
        "lives_or_dies": "When the thick coconut milk is added. Add it too early and the fat separates, leaving an oily surface and a thin sauce. Add it at the right moment — when the curry has built its spice character and only needs enrichment — and the sauce becomes creamy, cohesive, and glossy. The moment cannot be recovered once the oil separates.",
        "flavour_context": "Sweet, fatty, faintly floral — the neutral richness that carries and amplifies all the aromatics in the rempah. Thick press has a clean dairy-like sweetness; thin press is almost watery in comparison and serves primarily as a cooking medium."
    },
    {
        "name": "Dried chilli rehydration: Kristang rempah heat control",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Dried red chilies form the colour, heat, and body foundation of most Kristang rempah. "
            "The specific variety used in Malacca is cili kering — dried long red chilies, a milder, sweeter chili than bird's eye — which gives Kristang curries their characteristic deep terracotta-red colour without piercing heat. "
            "The preparation method directly determines whether a finished curry is vibrant red and aromatic or brown, flat, and aggressively hot.\n\n"
            "Method: dried chilies are stemmed and slit lengthwise, then seeds and white pith membrane are removed (the primary heat source — removing them reduces heat by approximately 50-60% while preserving colour). "
            "The seeded chilies are soaked in boiling water for 20-30 minutes until fully rehydrated and pliable; cold water is insufficient — it produces tough, grainy chili paste that never fully smooths. "
            "The soaking water is discarded (it contains leached bitterness from the seeds and skins). The drained chilies begin the first grinding stage.\n\n"
            "Kristang Devil's Curry (Kari Debal) uses a notably higher ratio of dried red chili to galangal and lemongrass than standard Malay curries — producing the characteristic deep red sauce. "
            "Heat calibration: 8-12 seeded dried chilies per portion produces medium heat; additional whole dried bird's eye chilies are added at finishing for guests requesting maximum heat. "
            "Colour test: properly fried rempah should be a rich, dark brick-red — orange indicates undercooked paste, brown indicates scorched."
        ),
        "key_principles": (
            "Soak in boiling water — cold water produces incomplete rehydration and gritty texture. "
            "Seed and de-pith before soaking — seeds release bitterness into soaking water, which is then discarded. "
            "Discard soaking water — it carries extracted bitterness. "
            "The seeding is the heat control mechanism: more seeds retained = more heat, all seeds removed = colour without aggression."
        ),
        "common_mistakes": (
            "Using cold water for soaking — incomplete rehydration, gritty paste. "
            "Keeping seeds for 'more flavour' — seeds add bitterness and aggressive heat, not complexity. "
            "Using soaking water in the curry — adds extracted bitterness. "
            "Under-soaking — chilies that are still stiff at the centre will not grind smooth."
        ),
        "pro_tips": (
            "Toast dried chilies briefly in a dry pan before soaking — enhances colour and adds a subtle smoky depth. "
            "For Devil's Curry specifically, use the full chili ratio — the deep red colour is half the visual identity of the dish. "
            "Blending soaked chilies produces a smoother paste than mortar pounding — acceptable in professional kitchens for large batches. "
            "Keep a small supply of dried bird's eye chilies for finishing heat adjustments at service — never add them to the base rempah."
        ),
        "trigger_keywords": json.dumps(["dried chilli rehydration", "cili kering", "Kristang chilli prep", "Malay chilli paste", "Devil's Curry chilli", "rempah chilli technique", "Malacca red curry colour"]),
        "authority_tier": 1,
        "lives_or_dies": "The soaking completeness. A chili that is not fully rehydrated will never grind smooth — the dried, stiff inner core resists the mortar or blender and produces visible specks in the finished paste that survive cooking. Touch the soaked chili: it should be completely pliable, with no firm centre.",
        "flavour_context": "Deep, fruity, earthy heat — not the sharp assault of fresh chili but a slow, building warmth with colour and body. Seeded long red chilies in Kristang rempah produce a sweet-savoury spice platform that supports the aromatic rhizomes rather than competing with them."
    },
    {
        "name": "Galangal preparation: Kristang rhizome slicing and grinding",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Galangal (lengkuas, Alpinia galanga) is the aromatic rhizome that most distinguishes Kristang curry from its Portuguese ancestral equivalent — no European spiced meat dish uses galangal, and its presence in rempah is the indelible marker of Malay Peninsula influence. "
            "In Kristang cooking, galangal provides a sharp, pine-like, camphor-tinged aromatic that lifts the paste and prevents the curry from tasting merely 'chili-hot' without aromatic depth.\n\n"
            "Young galangal (galangal muda) is pale, almost white, with thin pink skin and a fresh citrus-camphor bite — preferred for lighter chicken and fish curries. "
            "Old galangal (galangal tua) is fibrous, pungent, and difficult to grind — used in small quantities for deep meat braises and pork stews where its intensity is wanted. "
            "For rempah, young galangal is peeled then sliced across the grain before grinding — cutting across the fibres rather than along them makes grinding significantly easier and produces a smoother paste.\n\n"
            "Galangal must not be substituted with ginger in Kristang work — ginger produces a completely different aromatic profile (warm, spicy, sweet) versus galangal's sharp pine-camphor quality. "
            "Some Kristang cooks use both: galangal in the rempah base, and thin slices of fresh ginger added to pork stews in the last 20 minutes for a bright finishing note. "
            "Dried galangal powder (laos powder) is an inferior substitute — it loses the volatile aromatic compounds that fresh grinding releases."
        ),
        "key_principles": (
            "Slice across the grain (perpendicular to the fibres) before grinding — along the grain is almost impossible to grind smooth. "
            "Young galangal for curries, old galangal in small quantities for deep braises only. "
            "Peel before use — the skin adds bitterness. "
            "Never substitute with ginger — the aromatic profiles are incompatible in Kristang rempah."
        ),
        "common_mistakes": (
            "Substituting ginger — produces a completely different dish that does not taste Kristang. "
            "Using dried galangal powder — loses all volatile aromatic compounds, produces a flat, dusty curry. "
            "Not slicing across the grain — fibrous chunks resist grinding and create a stringy paste. "
            "Using old galangal in the same quantity as young — the intensity overwhelms the other aromatics."
        ),
        "pro_tips": (
            "Galangal is more aromatic than ginger but less enzymatic — it does not tenderise protein, so it can be added at any point in braising. "
            "When grinding by machine, add galangal with a small amount of water first — it grinds more efficiently when slightly wet. "
            "Freeze fresh galangal — it retains almost full aromatic quality frozen and is easier to peel when slightly thawed. "
            "The pine-camphor note of galangal is the quality check: if the paste does not have that distinctive sharp citrus-pine aroma, the galangal is old or dried."
        ),
        "trigger_keywords": json.dumps(["galangal", "lengkuas", "Kristang galangal", "laos", "Malay rhizome", "galangal preparation", "Malacca curry aromatic", "Alpinia galanga"]),
        "authority_tier": 1,
        "lives_or_dies": "Whether you used fresh or dried. Fresh galangal contributes a sharp, vivid, pine-citrus note that lifts the entire curry. Dried powder contributes a dusty, muted shadow of that note. There is no recovery — a curry made with dried galangal powder smells like a curry, but does not smell like Malacca.",
        "flavour_context": "Sharp, pine-camphor, citrus-eucalyptus — the aromatic note that distinguishes Southeast Asian curries from South Asian ones. In Kristang rempah, it is the counterpoint to the earthiness of turmeric and the sweetness of shallots."
    },
    {
        "name": "Lemongrass bruising: Kristang aromatic infusion technique",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Lemongrass (serai, Cymbopogon citratus) serves two distinct functions in Kristang cooking: ground into rempah paste (where the inner white stalk provides a citrus-eucalyptus aromatic layer), and bruised whole (added to curries and broths for volatile oil infusion without adding fibrous texture). "
            "Understanding which preparation to use in which context is a fundamental Kristang competency.\n\n"
            "For rempah: only the inner white-to-pale-yellow stalk (the bottom 10-15cm) is used — the outer green sheath is fibrous and indigestible. "
            "The inner stalk is sliced into thin rounds before grinding; thick slices do not break down and produce stringy paste. "
            "For braises and broths: the whole stalk is bruised with a heavy knife or pestle along its length to crack the outer cells and release aromatic oils, then tied into a knot to keep fibres together for easy removal.\n\n"
            "Fresh lemongrass is essential — dried or powdered lemongrass loses most of its volatile citral compounds within weeks. "
            "The freshness test: snap the cut end; it should exude a vivid lemon-eucalyptus scent immediately. "
            "Pale or brown-tipped lemongrass indicates age or improper storage. "
            "In Kristang Devil's Curry, lemongrass appears both in the rempah and as a bruised stalk in the braise — producing aromatic layering that is critical to the finished dish's complexity."
        ),
        "key_principles": (
            "Use only the inner white stalk for rempah — outer green sheaths are indigestible fibres. "
            "Slice into thin rounds before grinding — thick pieces resist breakdown. "
            "Bruise whole stalks for braises by hitting firmly along the length — all cells must be cracked. "
            "Tie bruised stalks into knots before adding to pot for easy removal."
        ),
        "common_mistakes": (
            "Using the green upper sheath in rempah — produces visible fibres in the finished paste. "
            "Thick slices before grinding — creates stringy, incompletely ground paste. "
            "Not bruising the stalk for braises — the volatile oils remain locked in unbroken cells. "
            "Using dried lemongrass powder — only a faint shadow of the fresh aromatic."
        ),
        "pro_tips": (
            "The dual use (rempah and whole stalk together) is specific to Kristang Devil's Curry — use both for maximum complexity. "
            "When storing fresh lemongrass, keep it in water like a flower — it stays fresh for 1-2 weeks. "
            "Lemongrass is the 'lift' note in Kristang curries — it provides the citrus brightness that prevents the dish from feeling heavy. "
            "For bruising, a single firm hit from the heel of a heavy knife is sufficient — excessive beating shreds the stalk and makes removal messy."
        ),
        "trigger_keywords": json.dumps(["lemongrass bruising", "serai", "Kristang lemongrass", "Malay aromatic preparation", "lemongrass rempah", "Malacca lemongrass", "citral extraction"]),
        "authority_tier": 1,
        "lives_or_dies": "The freshness of the stalk. Old lemongrass has lost its citral — the volatile compound responsible for the lemon-eucalyptus brightness. A bruised stalk should release a vivid scent immediately. If you have to lean in close to detect any scent, the lemongrass is spent and will contribute nothing meaningful to the dish.",
        "flavour_context": "Citrus-eucalyptus, clean, fresh — the aromatic note that prevents Kristang curries from feeling heavy or muddy. In rempah it fuses with galangal to create the characteristic sharp-bright top note of Southeast Asian curry; in braises it infuses more gently, contributing a floral lemon thread."
    },
    {
        "name": "Kaffir lime leaf: Kristang torn versus chiffonade technique",
        "category": "Kristang — Heritage Foundations",
        "origin": "Kristang community, Malacca, Malaysia",
        "description": (
            "Kaffir lime leaves (daun limau purut) are used in Kristang cooking both as a whole aromatic in braises and as a finely chiffonaded finishing garnish — the two preparations are functionally distinct and non-interchangeable. "
            "The central midrib is always removed before use; it is fibrous, contributes no flavour, and creates an unpleasant texture in finished dishes.\n\n"
            "Whole or torn leaves are used in curries, broths, and coconut rice where a gentle aromatic infusion over extended cooking is desired. "
            "The leaves are torn in half or lightly bruised with the fingers to crack oil-bearing cells, then added to the pot and removed before serving. "
            "This is the standard technique in Kristang kari ayam, batata baje (potato curry), and caldu.\n\n"
            "Chiffonade — the leaf rolled and cut into hair-thin ribbons — is used as a fresh garnish on finished sambals, fried rice, and certain desserts where a burst of raw lime fragrance is the objective. "
            "The cut must be extremely fine; thick strips taste coarse and bitter rather than perfumed. "
            "Frozen kaffir lime leaves retain acceptable aromatic quality for braises but lose the freshness needed for chiffonade garnish — fresh leaves only for finishing. "
            "The professional calibration: kaffir lime in a braise should be detectable as a subtle citrus-floral lift, not identifiable as a separate dominant note — when you can easily name it, there is too much."
        ),
        "key_principles": (
            "Always remove the central midrib — it adds bitterness and texture without flavour. "
            "Torn or bruised leaves for braises — infuse gently and are removed before service. "
            "Chiffonade only for fresh garnishing — must be hair-thin to avoid coarse, bitter texture. "
            "Never substitute dried kaffir lime leaves for fresh garnish — dried leaves have no aromatic volatile compounds left."
        ),
        "common_mistakes": (
            "Leaving the midrib in — produces fibrous, bitter fragments in the finished dish. "
            "Chiffonade cut too thick — coarse, bitter strips rather than perfumed ribbons. "
            "Using frozen leaves for fresh garnish — lost volatile compounds produce a flat, papery garnish. "
            "Too many leaves in a braise — the lime fragrance dominates and unbalances the dish."
        ),
        "pro_tips": (
            "For chiffonade: stack 5-6 leaves, roll them tightly lengthwise into a cigar, and slice with a very sharp knife. Dull knife bruises the leaf and releases bitter compounds. "
            "Kaffir lime trees grow well in tropical and subtropical pots — fresh supply from a tree produces incomparably better garnish than stored leaves. "
            "In Kristang coconut rice, 2-3 bruised leaves are tied into the knot with the lemongrass stalks — a classic triple aromatic cluster. "
            "The test for quality: a fresh leaf torn in half and held to the nose should smell immediately and intensely of lime zest and floral citrus."
        ),
        "trigger_keywords": json.dumps(["kaffir lime leaf", "daun limau purut", "Kristang lime leaf", "Malay aromatic leaf", "lime leaf chiffonade", "Malacca curry aromatic", "lime leaf torn vs cut"]),
        "authority_tier": 1,
        "lives_or_dies": "The cut thickness for chiffonade. A fine, hair-thin cut releases a burst of perfumed citrus oil without bitterness — the leaf almost disappears on the plate and the fragrance does the work. A thick cut adds coarse texture and a bitter lime pith note that sits unpleasantly on the tongue long after swallowing.",
        "flavour_context": "Floral, citrus-lime, clean and fresh — distinctly different from galangal and lemongrass in that it registers more as a 'scent' than a 'flavour' in the mouth. Its role in braises is atmospheric; in garnish it is a bright, clean top note that signals freshness and care."
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
print(f"\nBatch 1 complete: {inserted}/{len(entries)} inserted")
