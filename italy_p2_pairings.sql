-- Italy Phase 2: Pairing Intelligence for new Italian products
-- IDs 371-388: Barbera, Dolcetto, Moscato d'Asti, Gavi, Vino Nobile, Vernaccia, Prosecco
-- 5 pairings per product = 90 entries

BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- ============================================================
-- 371: Braida Bricco dell'Uccellone Barbera d'Asti Superiore
-- Full-bodied, dark plum, coffee, cedar, bright acidity
-- ============================================================
(371, 'wine_still', 'Barbera d''Asti Superiore DOCG', 'Full-bodied Barbera with dark plum, coffee, cedar, driving acidity and round tannins from Braida''s landmark oak-aged estate',
 'meat_poultry', 'rich_fatty_smoky', 'Slow-roasted pork shoulder with rosemary and garlic — the fat and herb richness echoing the cedar and coffee notes while acidity cuts the fattiness',
 'cleanse', 'Barbera''s naturally high acidity acts as the ideal counterbalance to pork fat; dark fruit mirrors the caramelised meat surface', 'main', 'classic', 2, true),

(371, 'wine_still', 'Barbera d''Asti Superiore DOCG', 'Full-bodied Barbera with dark plum, coffee, cedar, driving acidity and round tannins from Braida''s landmark oak-aged estate',
 'pasta_grain', 'umami_savoury', 'Tajarin with Piemontese beef ragù — the regional synergy is absolute; the ragù''s depth amplified by Barbera''s fruit and the pasta''s egg richness balanced by acidity',
 'complement', 'Classic Piedmont terroir pairing: Barbera d''Asti and tajarin ragù is the regional archetype. The wine''s acidity and dark fruit are made for this dish', 'main', 'classic', 2, true),

(371, 'wine_still', 'Barbera d''Asti Superiore DOCG', 'Full-bodied Barbera with dark plum, coffee, cedar, driving acidity and round tannins from Braida''s landmark oak-aged estate',
 'charcuterie_cheese', 'fermented_aged', 'Salumi board with Parmigiano-Reggiano, soppressata, and pickled vegetables — the fermented, salty, fatty elements find perfect counterpart in Barbera''s acidity',
 'cleanse', 'Barbera is Piedmont''s premier salumi companion: its acidity cuts through fat, its fruit complements the cured meat funk, and its tannins are gentle enough not to clash', 'starter', 'classic', 2, true),

(371, 'wine_still', 'Barbera d''Asti Superiore DOCG', 'Full-bodied Barbera with dark plum, coffee, cedar, driving acidity and round tannins from Braida''s landmark oak-aged estate',
 'meat_poultry', 'earthy_herbal', 'Braised oxtail with red wine, tomatoes, and gremolata — the collagen-rich meat and the wine''s structure create a textural and flavour synergy of the highest order',
 'complement', 'Oak-aged Barbera has the structure to match braised beef''s richness; the cedar notes echo slow-cooked connective tissue; acidity lifts the tomato base', 'main', 'established', 2, true),

(371, 'wine_still', 'Barbera d''Asti Superiore DOCG', 'Full-bodied Barbera with dark plum, coffee, cedar, driving acidity and round tannins from Braida''s landmark oak-aged estate',
 'pizza_flatbread', 'rich_fatty_smoky', 'Wood-fired pizza with nduja, buffalo mozzarella, and roasted peppers — the smoky, spicy, fatty pizza meets its ideal Italian companion',
 'complement', 'Barbera''s dark fruit and bright acidity are the classic Italian pizza companion; the smoky wood char echoes cedar notes from oak aging; nduja spice amplified by the wine''s fruit', 'casual', 'classic', 2, true),

-- ============================================================
-- 372: G.D. Vajra Dolcetto d'Alba
-- Medium-bodied, blueberry, black cherry, almond, soft tannins
-- ============================================================
(372, 'wine_still', 'Dolcetto d''Alba DOC', 'Medium-bodied Dolcetto with fresh blueberry, black cherry, almond, and characteristic bitter-almond finish; soft tannins with notable grip',
 'pasta_grain', 'umami_savoury', 'Pappardelle with wild boar ragù — Dolcetto''s dark berry fruit and almond character complement the gaminess while its soft tannins match the texture',
 'complement', 'Dolcetto is Piedmont''s everyday wine for meat-based pasta; its fruit softens gamey notes while its almond character echoes the pasta''s wheat', 'main', 'classic', 2, true),

(372, 'wine_still', 'Dolcetto d''Alba DOC', 'Medium-bodied Dolcetto with fresh blueberry, black cherry, almond, and characteristic bitter-almond finish; soft tannins with notable grip',
 'charcuterie_cheese', 'fermented_aged', 'Antipasto piemontese: salami, lardo, giardiniera, and Toma Piemontese cheese — the classic Piedmont start to any meal',
 'complement', 'Dolcetto is the canonical Piedmontese aperitivo/antipasto wine: its soft grip and bright fruit make it versatile; the lardo''s fat is cleansed by the acidity', 'starter', 'classic', 2, true),

(372, 'wine_still', 'Dolcetto d''Alba DOC', 'Medium-bodied Dolcetto with fresh blueberry, black cherry, almond, and characteristic bitter-almond finish; soft tannins with notable grip',
 'vegetables_legumes', 'earthy_herbal', 'Mushroom risotto with Parmigiano-Reggiano and truffle oil — the earthy mushroom and almond note in the Dolcetto create an aromatic bridge',
 'bridge', 'Dolcetto''s bitter almond finish bridges with the earthiness of porcini; its fruit prevents the dish from feeling too heavy; soft tannins don''t overwhelm the risotto texture', 'main', 'established', 2, true),

(372, 'wine_still', 'Dolcetto d''Alba DOC', 'Medium-bodied Dolcetto with fresh blueberry, black cherry, almond, and characteristic bitter-almond finish; soft tannins with notable grip',
 'pizza_flatbread', 'umami_savoury', 'Margherita pizza with fior di latte and fresh basil — Dolcetto''s simplicity and fruit match the purity of a great margherita',
 'complement', 'Dolcetto is Italy''s versatile everyday wine; its fresh fruit, moderate tannins, and bright acidity are perfectly proportioned for pizza margherita', 'casual', 'classic', 2, true),

(372, 'wine_still', 'Dolcetto d''Alba DOC', 'Medium-bodied Dolcetto with fresh blueberry, black cherry, almond, and characteristic bitter-almond finish; soft tannins with notable grip',
 'vegetables_legumes', 'bitter_astringent', 'Bitter greens (radicchio, endive) salad with walnuts and gorgonzola — the bitter almond finish of Dolcetto harmonises with bitter greens',
 'complement', 'Dolcetto''s characteristic bitter-almond finish is one of the few wines that harmonises with bitter greens rather than fighting them; the walnut echoes almond', 'starter', 'suggested', 2, true),

-- ============================================================
-- 373: Michele Chiarlo Barbera d'Asti Superiore La Court (Nizza DOCG)
-- Full-bodied, concentrated, blackberry, tobacco, mineral, complex
-- ============================================================
(373, 'wine_still', 'Nizza DOCG', 'Concentrated, complex Barbera from the historic La Court vineyard in Nizza — blackberry, tobacco, mineral grip, and the driving acidity of the variety elevated by precision viticulture',
 'meat_poultry', 'rich_fatty_smoky', 'Piemontese brasato al Barolo — slow-braised beef in wine with root vegetables, the regional prestige dish that demands a serious Piedmont red',
 'complement', 'Nizza-quality Barbera has the concentration and structure to stand beside the prestige braised beef dishes of Piedmont; tobacco and mineral echo the meat''s depth', 'main', 'classic', 2, true),

(373, 'wine_still', 'Nizza DOCG', 'Concentrated, complex Barbera from the historic La Court vineyard in Nizza — blackberry, tobacco, mineral grip, and the driving acidity of the variety elevated by precision viticulture',
 'meat_poultry', 'umami_savoury', 'Vitello tonnato — thinly sliced veal with tuna-caper sauce, the paradoxical Piedmontese classic that requires a wine of acidity and restraint',
 'cleanse', 'Barbera''s acidity is essential to cut through tonnato''s richness while its fruit complements the veal''s delicacy; a classic Piedmontese combination', 'starter', 'established', 2, true),

(373, 'wine_still', 'Nizza DOCG', 'Concentrated, complex Barbera from the historic La Court vineyard in Nizza — blackberry, tobacco, mineral grip, and the driving acidity of the variety elevated by precision viticulture',
 'charcuterie_cheese', 'fermented_aged', 'Aged Castelmagno DOP with honey and walnuts — Piedmont''s great aged cheese alongside one of its great wines',
 'complement', 'Castelmagno''s crumbly texture, blue-mould notes, and intense umami are magnified by the wine''s concentration; tobacco notes echo the cheese''s complexity', 'cheese', 'established', 2, true),

(373, 'wine_still', 'Nizza DOCG', 'Concentrated, complex Barbera from the historic La Court vineyard in Nizza — blackberry, tobacco, mineral grip, and the driving acidity of the variety elevated by precision viticulture',
 'pasta_grain', 'rich_fatty_smoky', 'Agnolotti del plin filled with roasted meat and vegetables in beef broth — the most celebrated of Piedmont''s pastas demands the region''s finest Barbera',
 'complement', 'Agnolotti del plin''s concentrated roasted meat filling meets Nizza Barbera as natural equals; the broth''s depth is amplified by the wine''s mineral-tobacco character', 'main', 'classic', 2, true),

(373, 'wine_still', 'Nizza DOCG', 'Concentrated, complex Barbera from the historic La Court vineyard in Nizza — blackberry, tobacco, mineral grip, and the driving acidity of the variety elevated by precision viticulture',
 'meat_poultry', 'earthy_herbal', 'Grilled bistecca di Fassona Piemontese — the lean, intensely flavoured beef of Piedmont''s native cattle breed paired with the region''s finest Barbera',
 'complement', 'Fassona beef''s intense flavour and lean texture benefit from Barbera''s fruit and acidity more than tannic wines; the Nizza concentration matches the meat''s intensity', 'main', 'established', 2, true),

-- ============================================================
-- 374: La Spinetta Moscato d'Asti Bricco Quaglia
-- Low alcohol, sweet, frizzante, apricot, orange blossom, honey
-- ============================================================
(374, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Delicate frizzante from La Spinetta''s Bricco Quaglia vineyard in Canelli — 5.5% abv, intensely perfumed apricot, orange blossom, white peach, and honey',
 'dessert_pastry', 'sweet_fruity', 'Peach tart with almond cream and apricot glaze — the stone fruit aromatics of the wine and the dessert create a seamless aromatic bridge',
 'complement', 'The classic Moscato d''Asti pairing: stone fruit desserts mirror the wine''s peach-apricot character perfectly; low alcohol prevents dessert fatigue', 'dessert', 'classic', 2, true),

(374, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Delicate frizzante from La Spinetta''s Bricco Quaglia vineyard in Canelli — 5.5% abv, intensely perfumed apricot, orange blossom, white peach, and honey',
 'dessert_pastry', 'sweet_fruity', 'Biscotti di meliga (Piedmontese cornmeal shortbreads) and cantucci — the traditional Piedmontese cookie accompaniment to Moscato',
 'complement', 'Biscotti and Moscato d''Asti is the quintessential Piedmontese after-dinner ritual; the cookies'' butteriness is lightened by the wine''s delicate fizz', 'dessert', 'classic', 2, true),

(374, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Delicate frizzante from La Spinetta''s Bricco Quaglia vineyard in Canelli — 5.5% abv, intensely perfumed apricot, orange blossom, white peach, and honey',
 'dessert_pastry', 'floral_perfumed', 'Fresh raspberries and cream with meringue — the floral, delicate sweetness of Moscato d''Asti amplifies the berries'' perfume without competing',
 'elevate', 'Moscato d''Asti''s low alcohol and delicate sweetness are perfectly calibrated for fresh fruit desserts; orange blossom elevates berry perfume', 'dessert', 'classic', 2, true),

(374, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Delicate frizzante from La Spinetta''s Bricco Quaglia vineyard in Canelli — 5.5% abv, intensely perfumed apricot, orange blossom, white peach, and honey',
 'charcuterie_cheese', 'sweet_salty', 'Aged Parmigiano-Reggiano (36-month) with drizzled acacia honey — sweet-salty contrast that Moscato d''Asti was made to partner',
 'contrast', 'The sweet-salty bridge between aged Parmigiano and honey is amplified by Moscato''s floral sweetness; a classic Italian cheese course finale pairing', 'cheese', 'classic', 2, true),

(374, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Delicate frizzante from La Spinetta''s Bricco Quaglia vineyard in Canelli — 5.5% abv, intensely perfumed apricot, orange blossom, white peach, and honey',
 'dessert_pastry', 'sweet_fruity', 'Semifreddo al torrone — frozen nougat semifreddo, a Piedmontese classic. The almond-honey notes of torrone mirror the wine perfectly',
 'complement', 'Torrone''s honey and nut character is a natural companion to Moscato d''Asti''s honey and peach; low alcohol prevents richness fatigue', 'dessert', 'established', 2, true),

-- ============================================================
-- 375: Bera Moscato d'Asti
-- Light, frizzante, apricot, lemon blossom, white peach, honey
-- ============================================================
(375, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Family Moscato d''Asti from Bera in Canelli — delicate frizzante with apricot, lemon blossom, white peach, and gentle honey sweetness',
 'dessert_pastry', 'sweet_fruity', 'Torta di nocciole (Piedmontese hazelnut cake) — the local Langhe hazelnuts in the cake match the wine''s honey and floral character',
 'complement', 'Torta di nocciole is one of Piedmont''s great pastry traditions; Moscato d''Asti''s gentle sweetness and almond-adjacent character bridge with hazelnut', 'dessert', 'classic', 2, true),

(375, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Family Moscato d''Asti from Bera in Canelli — delicate frizzante with apricot, lemon blossom, white peach, and gentle honey sweetness',
 'dessert_pastry', 'sweet_fruity', 'Pavlova with seasonal berries and passionfruit — the floral, aromatic Moscato resonates with passionfruit''s tropical perfume and the meringue''s sweetness',
 'complement', 'Moscato d''Asti''s delicate sweetness and floral notes match meringue''s lightness and tropical fruit''s aromatic intensity', 'dessert', 'established', 2, true),

(375, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Family Moscato d''Asti from Bera in Canelli — delicate frizzante with apricot, lemon blossom, white peach, and gentle honey sweetness',
 'dessert_pastry', 'sweet_spiced', 'Panettone with butter — the classic Milan Christmas bread finds its ideal Piedmontese wine companion',
 'complement', 'Panettone''s candied fruit and butter notes are lifted by Moscato''s frizzante; the honey sweetness of both are mutually reinforcing. Italy''s classic seasonal pairing', 'celebration', 'classic', 2, true),

(375, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Family Moscato d''Asti from Bera in Canelli — delicate frizzante with apricot, lemon blossom, white peach, and gentle honey sweetness',
 'dessert_pastry', 'floral_perfumed', 'Elderflower panna cotta with honey and almond tuile — the floral concordance between elderflower and Moscato''s orange blossom is exceptional',
 'complement', 'Elderflower''s delicate floral perfume harmonises precisely with Moscato d''Asti''s orange blossom and jasmine aromatics; honey in both creates seamless continuity', 'dessert', 'suggested', 2, true),

(375, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Family Moscato d''Asti from Bera in Canelli — delicate frizzante with apricot, lemon blossom, white peach, and gentle honey sweetness',
 'vegetables_legumes', 'sweet_fruity', 'Fresh figs with prosciutto di Parma and basil — the sweet-salty-herbal combination and the wine''s fruit create a multi-layered aperitivo experience',
 'complement', 'Moscato d''Asti''s sweetness and fruit complete the fig''s natural sweetness while contrasting the prosciutto''s salinity; a creative aperitivo approach', 'aperitif', 'adventurous', 2, true),

-- ============================================================
-- 376: Bera Asti Spumante DOCG
-- Fully sparkling, sweet, peach, apricot, orange zest, 7% abv
-- ============================================================
(376, 'wine_sparkling', 'Asti Spumante DOCG', 'Bera''s fully sparkling Asti Spumante from Canelli — more exuberant fizz than Moscato d''Asti, peach, apricot, orange zest, 7% abv',
 'dessert_pastry', 'sweet_spiced', 'Colomba di Pasqua (Italian Easter dove cake) with apricot jam — the seasonal pairing for Italy''s Easter traditions',
 'complement', 'Asti Spumante is the traditional Italian Easter wine; its stone fruit and orange peel match the candied fruit in Colomba; exuberant fizz lifts the richness', 'celebration', 'classic', 2, true),

(376, 'wine_sparkling', 'Asti Spumante DOCG', 'Bera''s fully sparkling Asti Spumante from Canelli — more exuberant fizz than Moscato d''Asti, peach, apricot, orange zest, 7% abv',
 'dessert_pastry', 'sweet_fruity', 'Fresh peach Melba with raspberry coulis and vanilla cream — the peach mirrors the wine''s dominant fruit perfectly',
 'complement', 'Classic stone fruit concordance: Asti''s peach-dominant aromatics create seamless harmony with poached peach; raspberry adds acidic contrast', 'dessert', 'classic', 2, true),

(376, 'wine_sparkling', 'Asti Spumante DOCG', 'Bera''s fully sparkling Asti Spumante from Canelli — more exuberant fizz than Moscato d''Asti, peach, apricot, orange zest, 7% abv',
 'dessert_pastry', 'sweet_fruity', 'Tiramisu — the classic Italian dessert works surprisingly well with the lower-alcohol Asti; coffee intensity is a counterpoint to the wine''s peach sweetness',
 'contrast', 'Tiramisu''s coffee-mascarpone richness and the wine''s sweet peach fizz create a contrast pairing that works precisely because they are so different', 'dessert', 'suggested', 2, true),

(376, 'wine_sparkling', 'Asti Spumante DOCG', 'Bera''s fully sparkling Asti Spumante from Canelli — more exuberant fizz than Moscato d''Asti, peach, apricot, orange zest, 7% abv',
 'dessert_pastry', 'sweet_spiced', 'Zabaione with seasonal berries — the eggy, sweet, Marsala-enriched zabaione is a natural partner for sparkling sweet wines',
 'complement', 'Zabaione and sparkling sweet wine is a classic Venetian and Piedmontese tradition; the wine''s fizz lifts the richness while its fruit complements the egg custard', 'dessert', 'established', 2, true),

(376, 'wine_sparkling', 'Asti Spumante DOCG', 'Bera''s fully sparkling Asti Spumante from Canelli — more exuberant fizz than Moscato d''Asti, peach, apricot, orange zest, 7% abv',
 'charcuterie_cheese', 'salty_mineral', 'Prosciutto di Parma with melon — the sweetness of Asti works brilliantly with the sweet-salty prosciutto and melon aperitivo',
 'complement', 'Asti Spumante''s sweetness amplifies melon''s sugar while contrasting the salt of prosciutto; the aperitivo application is underrated and highly effective', 'aperitif', 'suggested', 2, true),

-- ============================================================
-- 377: Michele Chiarlo Moscato d'Asti Nivole
-- Delicate, white peach, apricot, jasmine, rose petal, honey
-- ============================================================
(377, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Chiarlo''s flagship Moscato d''Asti Nivole from Santo Stefano Belbo — extraordinary perfume of white peach, apricot, jasmine, and rose petal with delicate sweetness',
 'dessert_pastry', 'floral_perfumed', 'Rose petal panna cotta with pistachio and Turkish delight — the rose and jasmine in the wine and the floral dessert create a stunning aromatic duet',
 'complement', 'Chiarlo Nivole''s rose petal and jasmine notes are amplified by floral desserts; a pairing that demonstrates Moscato d''Asti''s perfume intensity', 'dessert', 'suggested', 2, true),

(377, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Chiarlo''s flagship Moscato d''Asti Nivole from Santo Stefano Belbo — extraordinary perfume of white peach, apricot, jasmine, and rose petal with delicate sweetness',
 'dessert_pastry', 'sweet_fruity', 'Almond panna cotta with white peach compote — almond echoes the variety''s background nuttiness; white peach mirrors the wine''s dominant fruit',
 'complement', 'White peach in both dessert and wine creates seamless continuity; the almond note in Moscato bridges with the panna cotta''s richness', 'dessert', 'classic', 2, true),

(377, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Chiarlo''s flagship Moscato d''Asti Nivole from Santo Stefano Belbo — extraordinary perfume of white peach, apricot, jasmine, and rose petal with delicate sweetness',
 'dessert_pastry', 'sweet_spiced', 'Cantucci di mandorla with vin santo — in the absence of vin santo, Moscato d''Asti offers an equally classic dipping wine at lower alcohol',
 'complement', 'Almond biscotti and Moscato d''Asti echo the vin santo tradition with a more delicate, floral twist; the almond in both creates resonance', 'dessert', 'established', 2, true),

(377, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Chiarlo''s flagship Moscato d''Asti Nivole from Santo Stefano Belbo — extraordinary perfume of white peach, apricot, jasmine, and rose petal with delicate sweetness',
 'dessert_pastry', 'sweet_fruity', 'Fruit sorbet (apricot or peach) with almond tuile — the sorbet''s frozen stone fruit intensity is a mirror for the wine''s dominant aromatic profile',
 'complement', 'Frozen apricot or peach sorbet creates an intensified fruit echo with the wine; the cold temperature suppresses sweetness, making this contrast work beautifully', 'pre_dessert', 'classic', 2, true),

(377, 'wine_sparkling', 'Moscato d''Asti DOCG', 'Chiarlo''s flagship Moscato d''Asti Nivole from Santo Stefano Belbo — extraordinary perfume of white peach, apricot, jasmine, and rose petal with delicate sweetness',
 'charcuterie_cheese', 'sweet_salty', 'Gorgonzola dolce with acacia honey and walnut bread — the noble rot meets noble sweetness pairing; Moscato d''Asti is a classic Gorgonzola companion',
 'contrast', 'Gorgonzola dolce''s creamy blue mould salt and sweetness is perfectly balanced by Moscato''s gentle sweetness and floral notes; a classic Italian cheese-dessert pairing', 'cheese', 'classic', 2, true),

-- ============================================================
-- 378: La Scolca Black Label Gavi di Gavi
-- Medium-light, lemon zest, white flower, green apple, almond, mineral-saline
-- ============================================================
(378, 'wine_still', 'Gavi di Gavi DOCG', 'La Scolca''s benchmark Gavi di Gavi — the defining wine of the Cortese grape: lemon zest, white flower, green apple, almonds, and a mineral-saline finish',
 'seafood', 'salty_mineral', 'Ligurian seafood platter: crudo di branzino, gamberi rossi, capesante — the saline finish of Gavi and the mineral sea character of the crudo create a synergistic coastal pairing',
 'complement', 'Gavi di Gavi''s mineral-saline finish and crisp acidity are one of Italy''s finest seafood companions; the lemon-almond character echoes the classic Italian seafood dressing', 'starter', 'classic', 2, true),

(378, 'wine_still', 'Gavi di Gavi DOCG', 'La Scolca''s benchmark Gavi di Gavi — the defining wine of the Cortese grape: lemon zest, white flower, green apple, almonds, and a mineral-saline finish',
 'seafood', 'delicate_fresh', 'Fritto misto di mare — mixed fried seafood with lemon and aioli; the acidity and mineral character of Gavi cut through the frying batter perfectly',
 'cleanse', 'Gavi''s high acidity and mineral finish are the ideal counterpart to fried seafood''s richness; the lemon in the dish mirrors the wine''s citrus character', 'main', 'classic', 2, true),

(378, 'wine_still', 'Gavi di Gavi DOCG', 'La Scolca''s benchmark Gavi di Gavi — the defining wine of the Cortese grape: lemon zest, white flower, green apple, almonds, and a mineral-saline finish',
 'pasta_grain', 'delicate_fresh', 'Linguine alle vongole veraci — spaghetti alle vongole (clams) with white wine, garlic, and parsley; the maritime minerality of Gavi is the natural accompaniment',
 'complement', 'The briny-mineral character of clams resonates perfectly with Gavi''s saline finish; white wine in the sauce mirrors the wine''s acidity; a classic coastal Italian pairing', 'main', 'classic', 2, true),

(378, 'wine_still', 'Gavi di Gavi DOCG', 'La Scolca''s benchmark Gavi di Gavi — the defining wine of the Cortese grape: lemon zest, white flower, green apple, almonds, and a mineral-saline finish',
 'vegetables_legumes', 'delicate_fresh', 'Burrata with vine-ripened tomatoes, basil, and Ligurian olive oil — the delicate freshness of burrata and the wine''s floral-mineral character are in harmony',
 'complement', 'Burrata''s milky creaminess and Gavi''s fresh acidity create textural contrast while the floral notes in both create aromatic harmony', 'starter', 'established', 2, true),

(378, 'wine_still', 'Gavi di Gavi DOCG', 'La Scolca''s benchmark Gavi di Gavi — the defining wine of the Cortese grape: lemon zest, white flower, green apple, almonds, and a mineral-saline finish',
 'seafood', 'umami_savoury', 'Risotto alla pescatora (seafood risotto) with Parmesan — the risotto''s creamy richness balanced by Gavi''s minerality and acidity',
 'cleanse', 'Gavi''s acidity cuts through risotto''s butter-cream richness while its mineral character resonates with the seafood; the almond note bridges with Parmigiano', 'main', 'established', 2, true),

-- ============================================================
-- 379: Broglia La Meirana Gavi di Gavi
-- Medium-light, citrus, flint, white flower, green apple, almond
-- ============================================================
(379, 'wine_still', 'Gavi di Gavi DOCG', 'Broglia''s single-estate La Meirana Gavi di Gavi — citrus-precise with flint, white flower, green apple, and almond; more mineral and structured than most Gavi',
 'seafood', 'delicate_fresh', 'Oysters with lemon and mignonette — the mineral flint character of Broglia''s Gavi is the ideal oyster wine; its saline-mineral finish echoes the oyster liquor',
 'complement', 'Flint and mineral Gavi with oysters is a classic Italian alternative to Chablis; the wine''s acidity lifts the brine, the minerality resonates with the shell', 'amuse', 'classic', 2, true),

(379, 'wine_still', 'Gavi di Gavi DOCG', 'Broglia''s single-estate La Meirana Gavi di Gavi — citrus-precise with flint, white flower, green apple, and almond; more mineral and structured than most Gavi',
 'seafood', 'salty_mineral', 'Grilled branzino with capers, olives, and lemon butter — the Mediterranean herb-caper-lemon profile and the wine''s mineral structure create a coastal Italian synergy',
 'complement', 'Gavi''s mineral precision and citrus acidity are made for Mediterranean grilled fish preparations; the olive-caper salinity resonates with the wine''s mineral finish', 'main', 'classic', 2, true),

(379, 'wine_still', 'Gavi di Gavi DOCG', 'Broglia''s single-estate La Meirana Gavi di Gavi — citrus-precise with flint, white flower, green apple, and almond; more mineral and structured than most Gavi',
 'seafood', 'delicate_fresh', 'Tuna crudo with citrus dressing and Ligurian olive oil — the raw tuna''s clean flavour and the wine''s flint-citrus precision are a natural match',
 'complement', 'Raw fish''s clean umami needs crisp mineral acidity; Gavi''s flint character and citrus notes are precision-matched to crudo preparations', 'starter', 'established', 2, true),

(379, 'wine_still', 'Gavi di Gavi DOCG', 'Broglia''s single-estate La Meirana Gavi di Gavi — citrus-precise with flint, white flower, green apple, and almond; more mineral and structured than most Gavi',
 'vegetables_legumes', 'delicate_fresh', 'Insalata di farro (spelt salad) with grilled vegetables and aged ricotta — the grain''s nuttiness bridges with Gavi''s almond character',
 'bridge', 'Farro''s nutty sweetness and Gavi''s almond finish create an aromatic bridge; the wine''s acidity lifts the grain dish''s earthiness', 'main', 'suggested', 2, true),

(379, 'wine_still', 'Gavi di Gavi DOCG', 'Broglia''s single-estate La Meirana Gavi di Gavi — citrus-precise with flint, white flower, green apple, and almond; more mineral and structured than most Gavi',
 'pasta_grain', 'delicate_fresh', 'Trofie al pesto genovese (Ligurian basil pesto pasta) — Gavi''s Piedmontese-Ligurian border origins make it the natural companion to pesto',
 'complement', 'Gavi''s production zone borders Liguria; its floral-herb character bridges with basil pesto''s green intensity while acidity prevents pesto''s oiliness from becoming heavy', 'main', 'classic', 2, true),

-- ============================================================
-- 380: Poliziano Vino Nobile di Montepulciano Asinone
-- Full-bodied, dark cherry, dried rose, tobacco, leather, mineral, 10+ years
-- ============================================================
(380, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Poliziano''s reference Asinone single-vineyard Vino Nobile — dense ruby with dark cherry, dried rose, tobacco, leather, mineral; structured for a decade of aging',
 'meat_poultry', 'earthy_herbal', 'Bistecca alla Fiorentina with rosemary salt and Chianti butter — Tuscany''s great steak demands a great Tuscan Sangiovese',
 'complement', 'Vino Nobile''s Prugnolo Gentile (Sangiovese) and Florentine steak is one of Italy''s greatest regional food-wine pairings; the tannins match the char, the acidity cuts the fat', 'main', 'classic', 2, true),

(380, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Poliziano''s reference Asinone single-vineyard Vino Nobile — dense ruby with dark cherry, dried rose, tobacco, leather, mineral; structured for a decade of aging',
 'meat_poultry', 'rich_fatty_smoky', 'Cinghiale in umido (wild boar stew) with polenta — Tuscany''s iconic game dish pairs with the region''s structured red wines',
 'complement', 'Wild boar''s gamey richness and the polenta''s corn sweetness are perfectly structured for Vino Nobile''s tobacco-leather complexity and firm tannins', 'main', 'classic', 2, true),

(380, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Poliziano''s reference Asinone single-vineyard Vino Nobile — dense ruby with dark cherry, dried rose, tobacco, leather, mineral; structured for a decade of aging',
 'charcuterie_cheese', 'fermented_aged', 'Pecorino di Pienza stagionato (aged sheep''s milk cheese from Montepulciano''s neighbour) — the local cheese from the same hills as the wine',
 'complement', 'Pecorino di Pienza and Vino Nobile di Montepulciano are born 10km apart; the cheese''s lanolin and salt echo the wine''s earth and mineral; a perfect terroir pairing', 'cheese', 'classic', 2, true),

(380, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Poliziano''s reference Asinone single-vineyard Vino Nobile — dense ruby with dark cherry, dried rose, tobacco, leather, mineral; structured for a decade of aging',
 'pasta_grain', 'umami_savoury', 'Pici all''aglione (hand-rolled Tuscan pasta with tomato-garlic sauce) — the region''s most celebrated pasta with its greatest wine',
 'complement', 'Pici all''aglione''s rustic garlic-tomato intensity demands a serious Tuscan Sangiovese; the wine''s acidity matches the tomato''s tang while its structure holds against the garlic''s boldness', 'main', 'classic', 2, true),

(380, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Poliziano''s reference Asinone single-vineyard Vino Nobile — dense ruby with dark cherry, dried rose, tobacco, leather, mineral; structured for a decade of aging',
 'fungi_truffles', 'earthy_herbal', 'Risotto al tartufo bianco (white truffle risotto) — the Tuscan hills produce both truffles and Vino Nobile; the earthy-floral pairing is extraordinary',
 'bridge', 'White truffle''s volatile sulfur-earthy character bridges with Vino Nobile''s dried rose and mineral; the risotto''s richness balanced by the wine''s firm structure', 'main', 'suggested', 2, true),

-- ============================================================
-- 381: Avignonesi Vino Nobile di Montepulciano (biodynamic)
-- Full-bodied, dark cherry, dried herbs, spice, earth, tobacco
-- ============================================================
(381, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Avignonesi''s biodynamic Vino Nobile — dark cherry, dried herbs, spice, and earthy minerality from certified biodynamic vineyards around Montepulciano',
 'meat_poultry', 'earthy_herbal', 'Tagliata di manzo with rocket, Parmigiano shavings, and balsamic — the classic Tuscan beef salad presentation for a medium-weight Vino Nobile',
 'complement', 'Biodynamic Vino Nobile''s herbal and mineral complexity is amplified by the rocket''s bitterness and balsamic''s sweet acidity; a perfectly proportioned Tuscan pairing', 'main', 'classic', 2, true),

(381, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Avignonesi''s biodynamic Vino Nobile — dark cherry, dried herbs, spice, and earthy minerality from certified biodynamic vineyards around Montepulciano',
 'meat_poultry', 'earthy_herbal', 'Scottiglia (Tuscan mixed meat braise) with polenta — a dish from Avignonesi''s home territory requiring exactly this style of Sangiovese',
 'complement', 'Scottiglia''s multiple-meat braise has the complexity to match biodynamic Vino Nobile''s layered herbal-earth character; polenta softens the wine''s tannins', 'main', 'established', 2, true),

(381, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Avignonesi''s biodynamic Vino Nobile — dark cherry, dried herbs, spice, and earthy minerality from certified biodynamic vineyards around Montepulciano',
 'vegetables_legumes', 'earthy_herbal', 'Ribollita (Tuscan bread and bean soup) — the region''s peasant classic with a wine that grew on the same hillsides',
 'complement', 'Ribollita''s earthy, herbal depth (cannellini, lacinato kale, stale bread) pairs beautifully with Vino Nobile''s dried herb and earth character; biodynamic farming amplifies the terroir connection', 'main', 'classic', 2, true),

(381, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Avignonesi''s biodynamic Vino Nobile — dark cherry, dried herbs, spice, and earthy minerality from certified biodynamic vineyards around Montepulciano',
 'charcuterie_cheese', 'fermented_aged', 'Finocchiona (fennel-seed salami) with aged Pecorino and olives — the fennel seed''s anise note bridges with the wine''s spice and dried herb character',
 'bridge', 'Finocchiona''s fennel anise note is an aromatic bridge to Vino Nobile''s dried herb complexity; the Pecorino''s salt and fat balance the wine''s structure', 'starter', 'established', 2, true),

(381, 'wine_still', 'Vino Nobile di Montepulciano DOCG', 'Avignonesi''s biodynamic Vino Nobile — dark cherry, dried herbs, spice, and earthy minerality from certified biodynamic vineyards around Montepulciano',
 'fungi_truffles', 'earthy_herbal', 'Tagliatelle ai funghi porcini e tartufo nero (porcini and black truffle pasta) — the earthy double-funghi pasta matches biodynamic Vino Nobile''s earth character perfectly',
 'complement', 'Biodynamic farming often produces wines with heightened earthy and fungal complexity; porcini and black truffle amplify these notes through harmonic resonance', 'main', 'established', 2, true),

-- ============================================================
-- 382: Poliziano Rosso di Montepulciano
-- Medium-bodied, fresh cherry, herbs, dried tomato, spice
-- ============================================================
(382, 'wine_still', 'Rosso di Montepulciano DOC', 'Poliziano''s second wine — bright cherry, fresh herbs, dried tomato character; the accessible everyday Tuscan companion from one of Montepulciano''s finest estates',
 'pasta_grain', 'umami_savoury', 'Spaghetti al pomodoro e basilico — the perfect Italian pairing: good tomato sauce pasta and a fresh, food-friendly Tuscan red',
 'complement', 'Rosso di Montepulciano''s tomato-dried herb character is a natural mirror for classic tomato pasta; its bright acidity cuts through the pasta richness', 'main', 'classic', 2, true),

(382, 'wine_still', 'Rosso di Montepulciano DOC', 'Poliziano''s second wine — bright cherry, fresh herbs, dried tomato character; the accessible everyday Tuscan companion from one of Montepulciano''s finest estates',
 'pizza_flatbread', 'umami_savoury', 'Pizza diavola with spicy salami, San Marzano tomatoes, and chilli — Rosso di Montepulciano''s bright fruit handles spice well while matching the tomato base',
 'complement', 'The Sangiovese in Rosso di Montepulciano and San Marzano tomatoes are natural companions; the wine''s acidity meets the tomato, its fruit matches the salami', 'casual', 'classic', 2, true),

(382, 'wine_still', 'Rosso di Montepulciano DOC', 'Poliziano''s second wine — bright cherry, fresh herbs, dried tomato character; the accessible everyday Tuscan companion from one of Montepulciano''s finest estates',
 'meat_poultry', 'earthy_herbal', 'Pollo alla cacciatora (hunter-style chicken) with olives, tomatoes, and herbs — a classic Tuscan stew for a classic Tuscan wine',
 'complement', 'Cacciatore''s tomato-herb-olive profile mirrors Rosso di Montepulciano''s herbal-cherry character; the chicken''s approachability matches the wine''s accessible structure', 'main', 'classic', 2, true),

(382, 'wine_still', 'Rosso di Montepulciano DOC', 'Poliziano''s second wine — bright cherry, fresh herbs, dried tomato character; the accessible everyday Tuscan companion from one of Montepulciano''s finest estates',
 'charcuterie_cheese', 'fermented_aged', 'Prosciutto Toscano DOP, pecorino fresco, and bruschetta — simple Tuscan charcuterie for an approachable Tuscan red',
 'complement', 'Rosso di Montepulciano''s light tannins and bright cherry make it versatile for antipasto boards; its Tuscan character and Tuscan charcuterie are natural companions', 'starter', 'classic', 2, true),

(382, 'wine_still', 'Rosso di Montepulciano DOC', 'Poliziano''s second wine — bright cherry, fresh herbs, dried tomato character; the accessible everyday Tuscan companion from one of Montepulciano''s finest estates',
 'vegetables_legumes', 'umami_savoury', 'Bruschetta with chicken liver crostini (crostini neri) — the classic Tuscan starter, the bitter-iron note of liver finding an unexpected complement in bright Sangiovese',
 'complement', 'Chicken liver''s iron-bitter character is softened by Rosso di Montepulciano''s cherry fruit and acidity; a classic Tuscan combination', 'starter', 'established', 2, true),

-- ============================================================
-- 383: Montenidoli Vernaccia di San Gimignano Tradizionale (skin contact)
-- Golden, quince, dried apricot, almond, beeswax, saline, tannic
-- ============================================================
(383, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Montenidoli''s skin-contact Vernaccia Tradizionale — golden-orange; quince, dried apricot, almond, beeswax, saline mineral finish; serious structure for aging',
 'charcuterie_cheese', 'fermented_aged', 'Aged Pecorino di Fossa (cave-aged sheep''s milk cheese) with quince paste — the oxidative notes in cave-aged cheese and the skin-contact wine create a complex harmony',
 'complement', 'Cave-aged Pecorino''s oxidative, complex character resonates with the Tradizionale''s skin-contact depth; quince paste mirrors the wine''s quince aromatics', 'cheese', 'established', 2, true),

(383, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Montenidoli''s skin-contact Vernaccia Tradizionale — golden-orange; quince, dried apricot, almond, beeswax, saline mineral finish; serious structure for aging',
 'seafood', 'umami_savoury', 'Salt cod (baccalà mantecato) with polenta bianca and crispy capers — the skin-contact wine''s tannins and oxidative notes match salt cod''s intensity perfectly',
 'complement', 'Baccalà''s salt-preserved character and the wine''s skin-contact structure are both acquired tastes that understand each other; capers bridge the saline connection', 'main', 'suggested', 2, true),

(383, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Montenidoli''s skin-contact Vernaccia Tradizionale — golden-orange; quince, dried apricot, almond, beeswax, saline mineral finish; serious structure for aging',
 'meat_poultry', 'rich_fatty_smoky', 'Porchetta on grilled bread with salsa verde — the rosemary-fennel-garlic pork roast and the wine''s beeswax-herbal notes are surprisingly compatible',
 'bridge', 'Porchetta''s fennel-rosemary herb crust bridges with the Tradizionale''s herbal-beeswax character; skin tannins hold against the pork fat better than a conventional white wine would', 'main', 'adventurous', 2, true),

(383, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Montenidoli''s skin-contact Vernaccia Tradizionale — golden-orange; quince, dried apricot, almond, beeswax, saline mineral finish; serious structure for aging',
 'vegetables_legumes', 'bitter_astringent', 'Panzanella with anchovies and capers — the Tuscan bread salad with its acidic-salty notes is elevated by the wine''s tannic grip and mineral character',
 'complement', 'Panzanella''s vinegar-caper-anchovy notes need a wine with structure; the Tradizionale''s tannins prevent the dish from flattening; saline finish resonates with anchovies', 'starter', 'established', 2, true),

(383, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Montenidoli''s skin-contact Vernaccia Tradizionale — golden-orange; quince, dried apricot, almond, beeswax, saline mineral finish; serious structure for aging',
 'dessert_pastry', 'sweet_fruity', 'Quince tarte tatin with créme fraîche and almonds — the quince mirrors precisely the wine''s leading aromatic',
 'complement', 'Quince is the Tradizionale''s dominant aromatic note; quince tarte tatin creates a seamless fruit mirror while the almond''s bitterness bridges with the wine''s finish', 'dessert', 'suggested', 2, true),

-- ============================================================
-- 384: Teruzzi Vernaccia di San Gimignano
-- Light, lemon, white flower, almond, bitter almond, saline
-- ============================================================
(384, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Teruzzi''s standard Vernaccia — pale, crisp, white flower, lemon, almond with characteristic bitter-almond finish; the accessible appellation benchmark',
 'seafood', 'delicate_fresh', 'Acqua pazza (fish poached in white wine and tomatoes) with sea bass — the classic Tuscan coastal preparation for a classic Tuscan white',
 'complement', 'Vernaccia''s lemon-almond acidity is made for delicate fish preparations; the white wine used in cooking mirrors the drinking wine, creating seamless integration', 'main', 'classic', 2, true),

(384, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Teruzzi''s standard Vernaccia — pale, crisp, white flower, lemon, almond with characteristic bitter-almond finish; the accessible appellation benchmark',
 'pasta_grain', 'delicate_fresh', 'Risotto con asparagi e Parmigiano — asparagus risotto, where the bitter-almond finish of Vernaccia harmonises with the asparagus''s natural bitterness',
 'complement', 'Vernaccia''s characteristic bitter almond finish is one of the few white wines that works with asparagus''s bitterness rather than fighting it; a classic Tuscan spring pairing', 'main', 'established', 2, true),

(384, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Teruzzi''s standard Vernaccia — pale, crisp, white flower, lemon, almond with characteristic bitter-almond finish; the accessible appellation benchmark',
 'vegetables_legumes', 'delicate_fresh', 'Insalata di carciofi crudi (raw artichoke salad) with lemon and Parmigiano — artichoke''s metallic-bitter note and Vernaccia''s bitter almond are natural companions',
 'complement', 'Artichoke''s challenging metallic-bitter flavour finds a partner in Vernaccia''s own bitter almond character; both share bitterness as a defining trait', 'starter', 'suggested', 2, true),

(384, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Teruzzi''s standard Vernaccia — pale, crisp, white flower, lemon, almond with characteristic bitter-almond finish; the accessible appellation benchmark',
 'seafood', 'salty_mineral', 'Gamberoni alla griglia (grilled king prawns) with garlic, chilli, and lemon — the wine''s saline mineral finish and citrus acidity are ideal for grilled shellfish',
 'complement', 'Grilled shellfish needs acidity and mineral depth; Vernaccia''s saline finish mirrors the sea-character of the prawns while lemon in both creates continuity', 'main', 'classic', 2, true),

(384, 'wine_still', 'Vernaccia di San Gimignano DOCG', 'Teruzzi''s standard Vernaccia — pale, crisp, white flower, lemon, almond with characteristic bitter-almond finish; the accessible appellation benchmark',
 'charcuterie_cheese', 'delicate_fresh', 'Caprese salad with buffalo mozzarella, heirloom tomatoes, and fresh basil — the simplest Tuscan summer dish with an equally simple, honest wine',
 'complement', 'Vernaccia''s delicate floral notes and lemony acidity are perfectly proportioned for the simplicity of caprese; the almond finish adds a layer of complexity without overpowering', 'starter', 'classic', 2, true),

-- ============================================================
-- 385: Bisol Cartizze Dry
-- Fine mousse, white peach, apple blossom, pear, honey, mineral
-- ============================================================
(385, 'wine_sparkling', 'Prosecco Superiore DOCG Cartizze', 'Bisol''s Grand Cru Cartizze from the 107ha single hill — fine mousse, white peach, apple blossom, pear, honey, and mineral finish; 25 g/L RS Dry designation',
 'seafood', 'delicate_fresh', 'King crab with drawn butter and lemon — the wine''s delicate sweetness and mineral depth are an exquisite match for the sweet crab meat',
 'complement', 'Cartizze''s gentle sweetness (25 g/L RS) mirrors the natural sweetness of crab while the mineral finish creates tension; butter resonates with the wine''s creamy texture', 'main', 'established', 2, true),

(385, 'wine_sparkling', 'Prosecco Superiore DOCG Cartizze', 'Bisol''s Grand Cru Cartizze from the 107ha single hill — fine mousse, white peach, apple blossom, pear, honey, and mineral finish; 25 g/L RS Dry designation',
 'dessert_pastry', 'sweet_fruity', 'Apple tarte tatin with crème fraîche and caramel — the apple blossom in the wine mirrors the baked apple while the caramel echoes the honey character',
 'complement', 'Apple blossom in Cartizze and the baked apple of tarte tatin create a flavour mirror; the Dry designation''s sweetness is calibrated precisely for the caramel''s richness', 'dessert', 'established', 2, true),

(385, 'wine_sparkling', 'Prosecco Superiore DOCG Cartizze', 'Bisol''s Grand Cru Cartizze from the 107ha single hill — fine mousse, white peach, apple blossom, pear, honey, and mineral finish; 25 g/L RS Dry designation',
 'seafood', 'salty_mineral', 'Smoked salmon blinis with crème fraîche, dill, and caviar — the prestige aperitivo that matches the Grand Cru designation of this wine',
 'complement', 'Cartizze''s prestige demands prestige food: smoked salmon and caviar''s brine-salt-cream character is lifted by the fine mousse and mineral finish; honey sweetness contrasts the salt', 'aperitif', 'established', 2, true),

(385, 'wine_sparkling', 'Prosecco Superiore DOCG Cartizze', 'Bisol''s Grand Cru Cartizze from the 107ha single hill — fine mousse, white peach, apple blossom, pear, honey, and mineral finish; 25 g/L RS Dry designation',
 'dessert_pastry', 'sweet_fruity', 'Peach and almond tart with amaretto cream — the peach-honey-almond flavour triad in the wine and the tart is a seamless Venetian pairing',
 'complement', 'The flavour mirror between Cartizze''s white peach-honey and the tart''s peach-almond-amaretto is unusually precise; a prestige dessert for a prestige wine', 'dessert', 'classic', 2, true),

(385, 'wine_sparkling', 'Prosecco Superiore DOCG Cartizze', 'Bisol''s Grand Cru Cartizze from the 107ha single hill — fine mousse, white peach, apple blossom, pear, honey, and mineral finish; 25 g/L RS Dry designation',
 'charcuterie_cheese', 'sweet_salty', 'Burrata with white peach, prosciutto di San Daniele, and lemon zest — the summer prestige dish that showcases the wine''s full character',
 'complement', 'White peach in the dish mirrors the wine''s dominant fruit; the prosciutto''s salt contrasts the Dry sweetness; burrata''s cream resonates with the wine''s texture', 'starter', 'established', 2, true),

-- ============================================================
-- 386: Ruggeri Giustino B. Extra Brut
-- Dry (<6 g/L RS), fine mousse, green apple, lemon zest, mineral, yeast
-- ============================================================
(386, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Ruggeri Giustino B. Extra Brut — dry Prosecco Superiore with fine mousse, green apple, lemon zest, mineral, and yeast notes; demonstrates Glera''s gastronomy potential',
 'seafood', 'salty_mineral', 'Venetian cicchetti: sarde in saor, baccalà mantecato, and crostini with anchovy — the Venice canal-side bar snacks with the Veneto''s finest sparkling',
 'complement', 'Ruggeri''s dry, mineral Prosecco is made for Venetian cicchetti; the sarde in saor''s vinegar-pine nut-raisin profile finds tension with the wine''s dry acidity', 'aperitif', 'classic', 2, true),

(386, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Ruggeri Giustino B. Extra Brut — dry Prosecco Superiore with fine mousse, green apple, lemon zest, mineral, and yeast notes; demonstrates Glera''s gastronomy potential',
 'seafood', 'delicate_fresh', 'Scallops carpaccio with truffle oil, lemon, and sea salt — the Extra Brut''s mineral precision and low RS are ideal for delicate raw preparations',
 'complement', 'Extra Brut''s dryness (< 6 g/L RS) prevents sweet interference with delicate scallop; mineral finish mirrors the shellfish''s sea character', 'starter', 'established', 2, true),

(386, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Ruggeri Giustino B. Extra Brut — dry Prosecco Superiore with fine mousse, green apple, lemon zest, mineral, and yeast notes; demonstrates Glera''s gastronomy potential',
 'seafood', 'umami_savoury', 'Risotto al nero di seppia (black squid ink risotto) with grilled squid — the wine''s mineral and yeast character creates an unusual but compelling bridge with the squid ink',
 'bridge', 'Squid ink''s intense mineral-brine flavour bridges with Ruggeri''s mineral-yeast complexity; the Extra Brut''s dryness prevents sweetness from competing with the ink''s character', 'main', 'adventurous', 2, true),

(386, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Ruggeri Giustino B. Extra Brut — dry Prosecco Superiore with fine mousse, green apple, lemon zest, mineral, and yeast notes; demonstrates Glera''s gastronomy potential',
 'vegetables_legumes', 'delicate_fresh', 'Zucchini flower fritti stuffed with ricotta and anchovies — the delicate fried flower with the crisp mineral Prosecco is a perfect Venetian summer pairing',
 'complement', 'Fried zucchini flowers need acidity and mineral lift; the Extra Brut''s dryness and fine mousse refresh the frying without competing with the ricotta-anchovy filling', 'amuse', 'established', 2, true),

(386, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Ruggeri Giustino B. Extra Brut — dry Prosecco Superiore with fine mousse, green apple, lemon zest, mineral, and yeast notes; demonstrates Glera''s gastronomy potential',
 'charcuterie_cheese', 'fermented_aged', 'Sopressa Vicentina DOP (Veneto fennel-spiced salume) with Asiago d''Allevo — regional Veneto charcuterie and cheese with the region''s finest dry Prosecco',
 'complement', 'Sopressa''s fennel-spice and Asiago''s nutty-fruity character need a wine with mineral precision and fine acidity; the Extra Brut''s dryness prevents the fat from becoming heavy', 'starter', 'classic', 2, true),

-- ============================================================
-- 387: Nino Franco Rustico Valdobbiadene Prosecco Superiore
-- Extra Dry, fine mousse, fresh apple, pear, white flower, cream
-- ============================================================
(387, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Nino Franco Rustico NV — benchmark accessible Prosecco Superiore DOCG; fine mousse, fresh apple, pear, white flower, clean cream; Extra Dry (20 g/L RS)',
 'seafood', 'delicate_fresh', 'Prawn cocktail with Marie Rose and lemon — the classic British-Italian aperitivo; the wine''s freshness and gentle sweetness are ideal for prawn cocktail''s sweet-tangy profile',
 'complement', 'Rustico''s fresh apple-pear fruit and clean finish are the ideal introduction to quality Prosecco with food; the prawn''s sweetness mirrors the Extra Dry''s gentle RS', 'aperitif', 'classic', 2, true),

(387, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Nino Franco Rustico NV — benchmark accessible Prosecco Superiore DOCG; fine mousse, fresh apple, pear, white flower, clean cream; Extra Dry (20 g/L RS)',
 'vegetables_legumes', 'delicate_fresh', 'Melon and prosciutto — the summer aperitivo classic; Prosecco''s gentle sweetness bridges the melon''s sugar and the prosciutto''s salt',
 'complement', 'Melon-prosciutto is one of the world''s great food-wine aperitivo templates; Rustico Prosecco''s fresh fruit and gentle sweetness perfectly bridge the sweet-salty contrast', 'aperitif', 'classic', 2, true),

(387, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Nino Franco Rustico NV — benchmark accessible Prosecco Superiore DOCG; fine mousse, fresh apple, pear, white flower, clean cream; Extra Dry (20 g/L RS)',
 'charcuterie_cheese', 'delicate_fresh', 'Fresh ricotta crostini with herbs, lemon, and honey — the creamy ricotta and the wine''s floral-cream character create a delicate and seamless combination',
 'complement', 'Rustico''s floral freshness and cream notes match ricotta''s milky delicacy; honey in the dish echoes the wine''s mild sweetness; a perfect light aperitivo combination', 'aperitif', 'established', 2, true),

(387, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Nino Franco Rustico NV — benchmark accessible Prosecco Superiore DOCG; fine mousse, fresh apple, pear, white flower, clean cream; Extra Dry (20 g/L RS)',
 'dessert_pastry', 'sweet_fruity', 'Fruit salad with mint and elderflower — the light fruit salad and the floral Prosecco create a refreshing, low-intensity dessert pairing',
 'complement', 'Rustico Prosecco''s freshness and mild sweetness are perfectly proportioned for fresh fruit salad; elderflower bridges with the wine''s floral character', 'dessert', 'classic', 2, true),

(387, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Nino Franco Rustico NV — benchmark accessible Prosecco Superiore DOCG; fine mousse, fresh apple, pear, white flower, clean cream; Extra Dry (20 g/L RS)',
 'seafood', 'umami_savoury', 'Pasta al granchio (crab pasta) with chilli and parsley — Venetian crab pasta with the Veneto''s most accessible sparkling wine',
 'complement', 'Crab''s sweetness and the wine''s mild Extra Dry character are natural companions; the chilli''s heat is cooled by the fine mousse while parsley''s freshness mirrors floral notes', 'main', 'established', 2, true),

-- ============================================================
-- 388: Bisol Crede Valdobbiadene Prosecco Superiore
-- Brut (<12 g/L RS), fine mousse, white flower, green apple, almond, mineral
-- ============================================================
(388, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Bisol Crede from clay-glacial (crede) soils — Brut Prosecco Superiore with fine mousse, white flower, green apple, almond, and distinctive chalky mineral finish',
 'seafood', 'salty_mineral', 'Oysters on the half shell with lemon — Bisol Crede''s chalky mineral finish is the ideal oyster pairing from the Prosecco appellation',
 'complement', 'Crede''s mineral character (from the clay-glacial soil the wine is named for) creates the same mineral resonance as Chablis with oysters; brut dryness prevents sweetness interference', 'amuse', 'established', 2, true),

(388, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Bisol Crede from clay-glacial (crede) soils — Brut Prosecco Superiore with fine mousse, white flower, green apple, almond, and distinctive chalky mineral finish',
 'seafood', 'delicate_fresh', 'Sea bass ceviche with lime, coriander, and chilli — the citrus-mineral acidity of Crede provides the same refreshing structure as the ceviche''s lime',
 'complement', 'Brut Prosecco''s acidity and mineral finish work similarly to the lime in ceviche; the fine mousse refreshes the palate between bites of chilli-hot fish', 'starter', 'suggested', 2, true),

(388, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Bisol Crede from clay-glacial (crede) soils — Brut Prosecco Superiore with fine mousse, white flower, green apple, almond, and distinctive chalky mineral finish',
 'vegetables_legumes', 'delicate_fresh', 'White asparagus with Hollandaise sauce and lemon — the almond-mineral character of Crede and the white asparagus''s vegetal-almond notes create a rare harmony',
 'bridge', 'White asparagus has an almond-vegetal character that bridges with Crede''s almond note; the mineral finish and Hollandaise''s richness are balanced by fine acidity', 'starter', 'established', 2, true),

(388, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Bisol Crede from clay-glacial (crede) soils — Brut Prosecco Superiore with fine mousse, white flower, green apple, almond, and distinctive chalky mineral finish',
 'charcuterie_cheese', 'delicate_fresh', 'Burrata with Ligurian olive oil and sea salt — the cream character of burrata and the wine''s texture create an Italian simplicity pairing',
 'complement', 'Bisol Crede''s mineral chalk and cream notes match burrata''s milky richness; the Brut dryness prevents the dish from becoming overly rich', 'aperitif', 'classic', 2, true),

(388, 'wine_sparkling', 'Prosecco Superiore DOCG', 'Bisol Crede from clay-glacial (crede) soils — Brut Prosecco Superiore with fine mousse, white flower, green apple, almond, and distinctive chalky mineral finish',
 'seafood', 'umami_savoury', 'Spaghetti alle vongole veraci (clams) with white wine, garlic, and parsley — the briny mineral Prosecco echoes the clam brine of this Venetian classic',
 'complement', 'Crede''s mineral chalk and brut dryness are made for clam-based pasta; the white wine in the sauce mirrors the wine; mineral finish resonates with the sea-clam character', 'main', 'established', 2, true);

COMMIT;
