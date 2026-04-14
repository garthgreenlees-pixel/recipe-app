-- Italy Phase 3a: Pairing backfill for existing Italian reds (low-pairing products)
-- IDs 325-345: Barolo, Barbaresco, Brunello, Sassicaia, Ornellaia, Tignanello, Venetian reds/whites
-- Targets 4 pairings each (some already have 1-2, adding 3-4 more)

BEGIN;

INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style, beverage_description,
   food_category, food_flavour_profile, food_description,
   pairing_type, flavour_logic, meal_context, confidence, authority_tier, is_published)
VALUES

-- ============================================================
-- 325: Gaja Barbaresco
-- Nebbiologreat: tar, roses, leather, dried cherry, mineral, 15+ years
-- ============================================================
(325, 'wine_still', 'Barbaresco DOCG', 'Angelo Gaja''s legendary Barbaresco — Nebbiolo of extraordinary precision: tar, roses, leather, dried cherry, mineral. The wine that introduced Piedmont to the world',
 'meat_poultry', 'earthy_herbal', 'Roasted rack of lamb with rosemary, garlic, and jus — the classic Nebbiolo pairing: the wine''s tannins grip the lamb fat while roses amplify the rosemary',
 'complement', 'Nebbiolo''s tar-rose character and the rosemary-lamb combination is one of Italy''s canonical food-wine pairings; the wine''s firm tannins structure the rich lamb', 'main', 'classic', 1, true),

(325, 'wine_still', 'Barbaresco DOCG', 'Angelo Gaja''s legendary Barbaresco — Nebbiolo of extraordinary precision: tar, roses, leather, dried cherry, mineral. The wine that introduced Piedmont to the world',
 'fungi_truffles', 'earthy_herbal', 'Tajarin with white truffle shavings (Alba white truffle) — the highest expression of Piedmontese cuisine paired with Piedmont''s greatest red',
 'complement', 'White truffle and Barbaresco is arguably the world''s greatest single regional food-wine pairing: the truffle''s sulfurous-earthy complexity mirrors the wine''s tar-earth depth', 'main', 'classic', 1, true),

(325, 'wine_still', 'Barbaresco DOCG', 'Angelo Gaja''s legendary Barbaresco — Nebbiolo of extraordinary precision: tar, roses, leather, dried cherry, mineral. The wine that introduced Piedmont to the world',
 'charcuterie_cheese', 'fermented_aged', 'Castelmagno DOP — the ancient Piedmontese cheese from mountain pastures near Cuneo; crumbly, intense, with blue mould undertones that match Gaja''s complexity',
 'complement', 'Castelmagno and Barbaresco are both rare Piedmontese expressions of intensity; the cheese''s mould-mineral character resonates with the wine''s tar-roses depth', 'cheese', 'classic', 1, true),

(325, 'wine_still', 'Barbaresco DOCG', 'Angelo Gaja''s legendary Barbaresco — Nebbiolo of extraordinary precision: tar, roses, leather, dried cherry, mineral. The wine that introduced Piedmont to the world',
 'meat_poultry', 'rich_fatty_smoky', 'Brasato al Barolo — the Piedmontese braised beef cooked in wine; a dish designed to be accompanied by the great red wines of the Langhe',
 'complement', 'Brasato al Barolo''s wine-braised beef is the quintessential Langhe accompaniment; the braising wine in the dish echoes the drinking wine, creating seamless integration', 'main', 'classic', 1, true),

-- ============================================================
-- 326: Gaja Sorì Tildìn
-- Single vineyard Barbaresco, more floral and perfumed than standard
-- ============================================================
(326, 'wine_still', 'Barbaresco DOCG', 'Gaja''s celebrated single-vineyard Sorì Tildìn — Nebbiolo from the estate''s most prized parcel; exceptional floral complexity layered over the classic tar-roses-leather signature',
 'fungi_truffles', 'earthy_herbal', 'Risotto al tartufo bianco d''Alba — white truffle risotto from the same Langhe hills where Sorì Tildìn''s vines grow',
 'complement', 'The terroir connection is absolute: Langhe white truffles and Barbaresco are born on the same hillsides. The truffle''s volatile earth amplifies the wine''s complexity', 'main', 'classic', 1, true),

(326, 'wine_still', 'Barbaresco DOCG', 'Gaja''s celebrated single-vineyard Sorì Tildìn — Nebbiolo from the estate''s most prized parcel; exceptional floral complexity layered over the classic tar-roses-leather signature',
 'meat_poultry', 'earthy_herbal', 'Cotechino with lentils (Piedmontese New Year''s tradition) — the rich, spiced pork sausage and its luck-bringing legumes meet Piedmont''s greatest single-vineyard wine',
 'complement', 'Cotechino''s spiced pork richness and the lentils'' earthy starch create the textural and flavour depth that matches Sorì Tildìn''s complexity', 'celebration', 'established', 1, true),

(326, 'wine_still', 'Barbaresco DOCG', 'Gaja''s celebrated single-vineyard Sorì Tildìn — Nebbiolo from the estate''s most prized parcel; exceptional floral complexity layered over the classic tar-roses-leather signature',
 'charcuterie_cheese', 'fermented_aged', 'Aged Parmigiano-Reggiano 48-month with truffle honey — the ultra-aged cheese''s umami and crystalline texture against the wine''s floral complexity',
 'complement', 'A 48-month Parmigiano has the concentrated savoury depth to match Sorì Tildìn''s extraordinary complexity; truffle honey bridges the wine''s earthy-floral character', 'cheese', 'established', 1, true),

(326, 'wine_still', 'Barbaresco DOCG', 'Gaja''s celebrated single-vineyard Sorì Tildìn — Nebbiolo from the estate''s most prized parcel; exceptional floral complexity layered over the classic tar-roses-leather signature',
 'meat_poultry', 'rich_fatty_smoky', 'Coniglio alla cacciatora (hunter''s rabbit) with olives, capers, and rosemary — the lean game-bird character of rabbit is a classic Nebbiolo partner',
 'complement', 'Rabbit''s delicate gaminess and the wine''s roses-leather notes create a classic Italian game-red pairing; the olive-caper acidity provides tension against the wine''s tannins', 'main', 'established', 1, true),

-- ============================================================
-- 327: Bruno Giacosa Barolo Falletto di Serralunga d'Alba
-- Traditional Barolo: tar, dried roses, licorice, leather, austere tannins
-- ============================================================
(327, 'wine_still', 'Barolo DOCG', 'Bruno Giacosa''s Falletto di Serralunga — one of the most celebrated single-vineyard Barolos; traditional vinification; tar, dried roses, licorice, leather; built for 20+ years',
 'meat_poultry', 'rich_fatty_smoky', 'Costolette di agnello alla griglia (grilled lamb chops) with herb butter — the simplest expression of the classic Nebbiolo-lamb pairing',
 'complement', 'Grilled lamb chops'' char and fat are among Barolo''s classic partners; Giacosa''s Serralunga tannins grip the char while dried roses lift the herb butter', 'main', 'classic', 1, true),

(327, 'wine_still', 'Barolo DOCG', 'Bruno Giacosa''s Falletto di Serralunga — one of the most celebrated single-vineyard Barolos; traditional vinification; tar, dried roses, licorice, leather; built for 20+ years',
 'fungi_truffles', 'earthy_herbal', 'Uova e tartufo — fried eggs with white truffle shavings; the elemental Piedmontese luxury dish',
 'complement', 'The egg''s fat softens Barolo''s tannins while the truffle''s complexity matches the wine''s depth; a classic Langhe simplicity pairing that showcases both ingredients', 'main', 'classic', 1, true),

(327, 'wine_still', 'Barolo DOCG', 'Bruno Giacosa''s Falletto di Serralunga — one of the most celebrated single-vineyard Barolos; traditional vinification; tar, dried roses, licorice, leather; built for 20+ years',
 'meat_poultry', 'earthy_herbal', 'Lepre alla royale (royale of hare) — the most prestigious game preparation in French-Italian border cuisine; intense, reduced, complex',
 'complement', 'Traditional Barolo and hare royale is a prestige pairing of equals: both are austere, complex, and require patience; the licorice note in the wine bridges the gamey reduction', 'main', 'established', 1, true),

(327, 'wine_still', 'Barolo DOCG', 'Bruno Giacosa''s Falletto di Serralunga — one of the most celebrated single-vineyard Barolos; traditional vinification; tar, dried roses, licorice, leather; built for 20+ years',
 'charcuterie_cheese', 'fermented_aged', 'Toma Piemontese DOP (aged wheel, 90 days) with mostarda di frutta — the classic Piedmontese cheese board with the region''s iconic wine',
 'complement', 'Toma Piemontese''s buttery, milky character softened with mostarda''s mustard-fruit sweetness is the traditional Piedmontese cheese course companion for Barolo', 'cheese', 'classic', 1, true),

-- ============================================================
-- 328: Giacomo Conterno Barolo Monfortino Riserva
-- Italy's most collectible wine: intense, ethereal, 30+ year potential
-- ============================================================
(328, 'wine_still', 'Barolo DOCG', 'Giacomo Conterno Monfortino — Italy''s most collectible wine; traditional extended maceration (60+ days), massive tannin and acid; tar, roses, earth, forest floor; requires 30 years',
 'meat_poultry', 'rich_fatty_smoky', 'Filetto di bue al tartufo nero (beef fillet with black truffle) — the most prestige-appropriate dish for Italy''s most prestige-appropriate wine',
 'complement', 'Monfortino''s depth and austerity demand a dish of equivalent prestige; beef fillet''s lean richness and black truffle''s earthy intensity create the complexity this wine requires', 'main', 'classic', 1, true),

(328, 'wine_still', 'Barolo DOCG', 'Giacomo Conterno Monfortino — Italy''s most collectible wine; traditional extended maceration (60+ days), massive tannin and acid; tar, roses, earth, forest floor; requires 30 years',
 'fungi_truffles', 'earthy_herbal', 'Tajarin with white Alba truffle — serving this with any wine other than Nebbiolo would miss the terroir point entirely',
 'complement', 'Monfortino and white truffle tajarin is the apex of Piedmontese cuisine: two things of unparalleled complexity from the same soil, expressing that soil through different registers', 'main', 'classic', 1, true),

(328, 'wine_still', 'Barolo DOCG', 'Giacomo Conterno Monfortino — Italy''s most collectible wine; traditional extended maceration (60+ days), massive tannin and acid; tar, roses, earth, forest floor; requires 30 years',
 'charcuterie_cheese', 'fermented_aged', 'Grana Padano Riserva (24-month) — the broader, sweeter alternative to Parmigiano; its butterscotch notes echo Monfortino''s ethereal secondary complexity at maturity',
 'complement', 'An aged Monfortino at 20+ years develops butterscotch, dried fruit, and earth notes that resonate with aged Grana Padano''s crystalline richness', 'cheese', 'established', 1, true),

(328, 'wine_still', 'Barolo DOCG', 'Giacomo Conterno Monfortino — Italy''s most collectible wine; traditional extended maceration (60+ days), massive tannin and acid; tar, roses, earth, forest floor; requires 30 years',
 'meat_poultry', 'earthy_herbal', 'Cinghiale arrosto con polenta (roasted wild boar with polenta) — the hunter''s game dish from the same Piedmontese hills as the wine',
 'complement', 'Wild boar''s intense gaminess and forest-floor character is the classic match for serious aged Barolo; the polenta''s starch softens the tannins and creates a bridge', 'main', 'classic', 1, true),

-- ============================================================
-- 329: Bartolo Mascarello Barolo
-- Traditional Barolo: unfilterd, tar, roses, leather, licorice, 20+ years
-- ============================================================
(329, 'wine_still', 'Barolo DOCG', 'Bartolo Mascarello''s iconic Barolo — unfiltered, traditional; tar, roses, leather, licorice; Maria Teresa Mascarello continues her father''s uncompromising approach. A political and philosophical statement as much as a wine',
 'meat_poultry', 'earthy_herbal', 'Agnello da latte arrosto (roasted milk-fed lamb) with rosemary and garlic — the most delicate lamb preparation paired with Barolo''s floral complexity',
 'complement', 'Milk-fed lamb''s delicacy allows Mascarello''s roses-leather character to shine; the garlic-rosemary crust provides the bridge between the wine''s floral and earthy registers', 'main', 'classic', 1, true),

(329, 'wine_still', 'Barolo DOCG', 'Bartolo Mascarello''s iconic Barolo — unfiltered, traditional; tar, roses, leather, licorice; Maria Teresa Mascarello continues her father''s uncompromising approach. A political and philosophical statement as much as a wine',
 'fungi_truffles', 'earthy_herbal', 'Fonduta (Piedmontese cheese fondue) with white truffle — fondue''s richness softens the tannins while the truffle amplifies the wine''s earthy depth',
 'complement', 'Fonduta''s buttery, Fontina-based richness is one of the classic ways to tame Barolo''s tannins; white truffle shavings elevate the pairing to rare territory', 'main', 'established', 1, true),

(329, 'wine_still', 'Barolo DOCG', 'Bartolo Mascarello''s iconic Barolo — unfiltered, traditional; tar, roses, leather, licorice; Maria Teresa Mascarello continues her father''s uncompromising approach. A political and philosophical statement as much as a wine',
 'charcuterie_cheese', 'fermented_aged', 'Bra Duro DOP — the hard aged cheese from the Cuneo hills; its crystalline, intense character matches the wine''s austerity perfectly',
 'complement', 'Bra Duro''s austere, crystalline aged character is a Piedmontese mirror for Mascarello''s Barolo; both require patience, reward it generously, and speak of the same territory', 'cheese', 'established', 1, true),

(329, 'wine_still', 'Barolo DOCG', 'Bartolo Mascarello''s iconic Barolo — unfiltered, traditional; tar, roses, leather, licorice; Maria Teresa Mascarello continues her father''s uncompromising approach. A political and philosophical statement as much as a wine',
 'meat_poultry', 'rich_fatty_smoky', 'Fassona beef tartare with capers, anchovies, and egg yolk — the raw Piedmontese beef preparation that demands only the best local wine',
 'complement', 'Fassona tartare''s iron-rich intensity and caper-anchovy seasoning create the precise flavour intensity that Mascarello''s Barolo requires; the wine''s tannins structure the raw fat', 'starter', 'established', 1, true),

-- ============================================================
-- 330: Vietti Barolo Castiglione
-- More approachable modern-traditional Barolo, still structured
-- ============================================================
(330, 'wine_still', 'Barolo DOCG', 'Vietti''s Castiglione — a blend from multiple vineyards in Castiglione Falletto; a gateway Barolo of exceptional quality: accessible earlier, still with the classic tar-roses-cherry profile',
 'pasta_grain', 'umami_savoury', 'Agnolotti al sugo arrosto (roasted meat-filled pasta in meat jus) — Vietti''s Castiglione accessibility makes it ideal for the classic pasta-Barolo pairing',
 'complement', 'Castiglione Barolo''s rounder tannins handle the pasta richness with more grace than the great single-vineyard wines; the meat jus echoes the wine''s cherry-earth notes', 'main', 'classic', 2, true),

(330, 'wine_still', 'Barolo DOCG', 'Vietti''s Castiglione — a blend from multiple vineyards in Castiglione Falletto; a gateway Barolo of exceptional quality: accessible earlier, still with the classic tar-roses-cherry profile',
 'meat_poultry', 'earthy_herbal', 'Osso buco alla Milanese with gremolata and saffron risotto — the classic Milanese preparation demands a northern Italian red of equal stature',
 'complement', 'Osso buco''s braised veal shank and marrow richness is perfectly balanced by Barolo''s tannins; the gremolata''s lemon-herb sharpness contrasts the wine''s earthiness', 'main', 'classic', 2, true),

(330, 'wine_still', 'Barolo DOCG', 'Vietti''s Castiglione — a blend from multiple vineyards in Castiglione Falletto; a gateway Barolo of exceptional quality: accessible earlier, still with the classic tar-roses-cherry profile',
 'charcuterie_cheese', 'fermented_aged', 'Pecorino Toscano stagionato with chestnut honey — the aged sheep''s milk with honey is a classic Italian cheese-wine combination that works with structured reds',
 'complement', 'Aged Pecorino''s sheep-lanolin character and chestnut honey''s earthy sweetness match the Barolo''s complexity; a simpler, accessible version of the classic Barolo-cheese pairing', 'cheese', 'established', 2, true),

(330, 'wine_still', 'Barolo DOCG', 'Vietti''s Castiglione — a blend from multiple vineyards in Castiglione Falletto; a gateway Barolo of exceptional quality: accessible earlier, still with the classic tar-roses-cherry profile',
 'meat_poultry', 'rich_fatty_smoky', 'Beef short rib braised with Barolo and root vegetables — the ultimate expression of regional cooking unity',
 'complement', 'Short rib braised with Barolo is cooked with the same wine you drink alongside it; the reduction amplifies the wine''s cherry and earth while fat softens the tannins', 'main', 'established', 2, true),

-- ============================================================
-- 331: G.D. Vajra Barolo Bricco delle Viole
-- High altitude Barolo (400m+), more floral, lighter texture, great elegance
-- ============================================================
(331, 'wine_still', 'Barolo DOCG', 'Vajra''s Bricco delle Viole — high-altitude vineyard (400m+) in Vergne, the highest cru in the Barolo zone; exceptional floral elegance, lighter texture, built for long aging',
 'seafood', 'delicate_fresh', 'Red mullet in cartoccio (baked in parchment with herbs and tomatoes) — the most elegant, floral Barolo can approach fish dishes of sufficient flavour intensity',
 'elevate', 'Bricco delle Viole''s exceptional floral character and lighter body make it one of the few Barolos that can approach flavourful fish preparations; a sophisticated pairing for elegant occasions', 'main', 'adventurous', 1, true),

(331, 'wine_still', 'Barolo DOCG', 'Vajra''s Bricco delle Viole — high-altitude vineyard (400m+) in Vergne, the highest cru in the Barolo zone; exceptional floral elegance, lighter texture, built for long aging',
 'meat_poultry', 'earthy_herbal', 'Quaglia (quail) arrosto with porcini and polenta — delicate game bird with the most elegant of Barolos',
 'complement', 'Quail''s delicacy and subtle gaminess are perfectly proportioned for Bricco delle Viole''s lighter, more floral style; porcini bridges the wine''s earthy character', 'main', 'established', 1, true),

(331, 'wine_still', 'Barolo DOCG', 'Vajra''s Bricco delle Viole — high-altitude vineyard (400m+) in Vergne, the highest cru in the Barolo zone; exceptional floral elegance, lighter texture, built for long aging',
 'fungi_truffles', 'earthy_herbal', 'Porcini mushroom soup with Parmigiano crostini — the earthy depth of porcini as a bridge into Barolo''s complexity in a more accessible format',
 'bridge', 'Porcini''s earthy depth creates an aromatic bridge to Bricco delle Viole''s forest-floor-floral character; the soup''s warmth softens the wine''s tannins', 'starter', 'established', 1, true),

(331, 'wine_still', 'Barolo DOCG', 'Vajra''s Bricco delle Viole — high-altitude vineyard (400m+) in Vergne, the highest cru in the Barolo zone; exceptional floral elegance, lighter texture, built for long aging',
 'charcuterie_cheese', 'fermented_aged', 'Fontina Val d''Aosta DOP fondue — the Alpine melting cheese; its grassiness and mild earthiness are calibrated for the floral Bricco delle Viole style',
 'complement', 'Fontina''s grassy-earthy character and melting texture soften the Barolo''s tannins while bridging with the wine''s Alpine-adjacent floral character from high altitude viticulture', 'main', 'established', 1, true),

-- ============================================================
-- 332: Roagna Barbaresco Crichet Pajè
-- Extremely traditional: unfiltered, no fining, 30+ months in large oak
-- ============================================================
(332, 'wine_still', 'Barbaresco DOCG', 'Roagna''s Crichet Pajè — among Barbaresco''s most traditional expressions: unfiltered, no fining, 30+ months large oak; extraordinary depth, forest floor, dried cherry, orange peel; extraordinary longevity',
 'meat_poultry', 'rich_fatty_smoky', 'Piccione (squab pigeon) arrosto with liver crostini and cherry reduction — the intensity of squab matches the extraordinary complexity of Crichet Pajè',
 'complement', 'Squab''s iron-rich, gamey intensity is one of the few birds that can match the Crichet Pajè''s depth; cherry reduction bridges the wine''s dried fruit character', 'main', 'established', 1, true),

(332, 'wine_still', 'Barbaresco DOCG', 'Roagna''s Crichet Pajè — among Barbaresco''s most traditional expressions: unfiltered, no fining, 30+ months large oak; extraordinary depth, forest floor, dried cherry, orange peel; extraordinary longevity',
 'fungi_truffles', 'earthy_herbal', 'Insalata di porcini crudi con tartufo nero e Parmigiano — raw porcini salad with black truffle and Parmigiano shavings; the raw fungal intensity is calibrated for Roagna''s depth',
 'complement', 'Raw porcini''s intense earthy-fungal character bridges with Crichet Pajè''s forest floor complexity; the raw preparation preserves flavour intensity to match the wine', 'starter', 'established', 1, true),

(332, 'wine_still', 'Barbaresco DOCG', 'Roagna''s Crichet Pajè — among Barbaresco''s most traditional expressions: unfiltered, no fining, 30+ months large oak; extraordinary depth, forest floor, dried cherry, orange peel; extraordinary longevity',
 'charcuterie_cheese', 'fermented_aged', 'Murazzano DOP (raw milk sheep/cow blend) aged 30 days — the delicate Langhe cheese that is Roagna''s local territory cheese',
 'complement', 'Murazzano''s local provenance (Langhe hills surrounding the Roagna estate) creates a terroir pairing; its delicate sheep-cow character needs the wine''s complexity to show its best', 'cheese', 'suggested', 1, true),

(332, 'wine_still', 'Barbaresco DOCG', 'Roagna''s Crichet Pajè — among Barbaresco''s most traditional expressions: unfiltered, no fining, 30+ months large oak; extraordinary depth, forest floor, dried cherry, orange peel; extraordinary longevity',
 'meat_poultry', 'earthy_herbal', 'Guanciale brasato (braised pork cheek) with polenta and gremolata — the collagen-rich braised pork echoes the wine''s orange peel-dried fruit character',
 'complement', 'The orange peel complexity in aged Crichet Pajè bridges with gremolata''s lemon-orange zest; braised pork cheek''s richness is structured by the wine''s traditional tannins', 'main', 'established', 1, true),

-- ============================================================
-- 333: Ceretto Barolo Bricco Rocche (2 → 5 pairings target; add 3)
-- Modern Barolo from prestigious Castiglione Falletto cru
-- ============================================================
(333, 'wine_still', 'Barolo DOCG', 'Ceretto''s Bricco Rocche — a modern-leaning Barolo from the prestigious Castiglione Falletto cru; elegant, perfumed, with cedar, cherry, and tobacco notes',
 'meat_poultry', 'earthy_herbal', 'Agnello al forno con patate e rosmarino (roast leg of lamb with potatoes and rosemary) — the herbal-earthy combination and the wine''s tobacco-cedar character create a beautiful match',
 'complement', 'Ceretto''s modern style makes Bricco Rocche approachable with the classic Nebbiolo pairing of roast lamb; the cedar and tobacco echo the rosemary-herb crust', 'main', 'classic', 2, true),

(333, 'wine_still', 'Barolo DOCG', 'Ceretto''s Bricco Rocche — a modern-leaning Barolo from the prestigious Castiglione Falletto cru; elegant, perfumed, with cedar, cherry, and tobacco notes',
 'pasta_grain', 'rich_fatty_smoky', 'Plin al sugo di arrosto — the Langhe''s most celebrated small pasta filled with roasted meat in the roasting jus',
 'complement', 'Barolo and agnolotti del plin is the most classical Piedmontese pairing; Bricco Rocche''s approachability makes it ideal at the table where more austere Barolos might dominate', 'main', 'classic', 2, true),

(333, 'wine_still', 'Barolo DOCG', 'Ceretto''s Bricco Rocche — a modern-leaning Barolo from the prestigious Castiglione Falletto cru; elegant, perfumed, with cedar, cherry, and tobacco notes',
 'charcuterie_cheese', 'fermented_aged', 'Langres DOP (washed rind cow''s milk from Burgundy) — a prestige cross-regional pairing; the strong cheese''s pungency handled by the wine''s structure',
 'contrast', 'Strong washed-rind cheese and structured red wine is a classic European pairing pattern; Ceretto''s Barolo has the structure to handle the cheese''s pungency', 'cheese', 'suggested', 2, true),

-- ============================================================
-- 334: Biondi-Santi Brunello di Montalcino Riserva (2 → 5 target; add 3)
-- The original Brunello; legendary age-worthiness
-- ============================================================
(334, 'wine_still', 'Brunello di Montalcino DOCG', 'Biondi-Santi Brunello Riserva — the original Brunello; only made in exceptional vintages; extreme longevity (50+ years); dried cherry, leather, tobacco, violets, iron',
 'meat_poultry', 'rich_fatty_smoky', 'Bistecca alla Fiorentina from Chianina beef with sea salt — the Tuscan oak-grilled steak demands the original Tuscan Sangiovese Grosso',
 'complement', 'Brunello and bistecca alla Fiorentina is the Tuscan prestige pairing of the century; the wine''s iron-cherry character mirrors the char while its tannins grip the fat', 'main', 'classic', 1, true),

(334, 'wine_still', 'Brunello di Montalcino DOCG', 'Biondi-Santi Brunello Riserva — the original Brunello; only made in exceptional vintages; extreme longevity (50+ years); dried cherry, leather, tobacco, violets, iron',
 'fungi_truffles', 'earthy_herbal', 'Tajarin con sugo di lepre (pasta with hare ragù) — Tuscany''s game-pasta tradition demands the region''s most serious wine',
 'complement', 'Hare ragù''s concentrated gamey reduction and Brunello Riserva''s iron-leather-cherry character are natural equals; both require years of maturation to show their complexity', 'main', 'established', 1, true),

(334, 'wine_still', 'Brunello di Montalcino DOCG', 'Biondi-Santi Brunello Riserva — the original Brunello; only made in exceptional vintages; extreme longevity (50+ years); dried cherry, leather, tobacco, violets, iron',
 'charcuterie_cheese', 'fermented_aged', 'Pecorino di Pienza stagionato (12-month sheep''s milk from Pienza, 10km from Montalcino) — the most local possible cheese pairing',
 'complement', 'Pienza''s aged Pecorino and Montalcino''s Brunello share the same hilltop terroir; the cheese''s lanolin and salt create a perfect mineral-animal bridge with the wine''s iron and leather', 'cheese', 'classic', 1, true),

-- ============================================================
-- 335: Tenuta San Guido Sassicaia
-- The original Super Tuscan; Cabernet Sauvignon + Cabernet Franc
-- ============================================================
(335, 'wine_still', 'Bolgheri Sassicaia DOC', 'Sassicaia — the wine that created the Super Tuscan category; Cabernet Sauvignon + Cabernet Franc from coastal Bolgheri; cedar, blackcurrant, graphite, tobacco; 20+ year potential',
 'meat_poultry', 'rich_fatty_smoky', 'Grilled Chianina ribeye with green peppercorn and Chianti butter — Sassicaia''s Bordeaux character demands a Bordeaux-style food approach executed with Tuscan beef',
 'complement', 'Sassicaia''s Cabernet backbone (cedar, graphite, blackcurrant) pairs like a Left Bank Bordeaux with aged beef; the Chianina''s lean intensity matches the wine''s structure', 'main', 'classic', 1, true),

(335, 'wine_still', 'Bolgheri Sassicaia DOC', 'Sassicaia — the wine that created the Super Tuscan category; Cabernet Sauvignon + Cabernet Franc from coastal Bolgheri; cedar, blackcurrant, graphite, tobacco; 20+ year potential',
 'meat_poultry', 'earthy_herbal', 'Roasted squab with black truffle jus and morels — the prestige game preparation for a wine of Sassicaia''s stature',
 'complement', 'Sassicaia''s graphite-tobacco complexity and the truffle-morel earthiness create a luxury pairing; the squab''s iron-gamey character bridges with the wine''s dark fruit', 'main', 'established', 1, true),

(335, 'wine_still', 'Bolgheri Sassicaia DOC', 'Sassicaia — the wine that created the Super Tuscan category; Cabernet Sauvignon + Cabernet Franc from coastal Bolgheri; cedar, blackcurrant, graphite, tobacco; 20+ year potential',
 'charcuterie_cheese', 'fermented_aged', 'Aged Comté (24-month) with walnuts and quince paste — the Alpine cheese''s nutty-brown butter character against Sassicaia''s cedar-graphite',
 'complement', 'Aged Comté is one of the great cheese companions for Cabernet-based wines; its nutty complexity mirrors the wine''s secondary cedar notes; quince bridges dark fruit', 'cheese', 'established', 1, true),

(335, 'wine_still', 'Bolgheri Sassicaia DOC', 'Sassicaia — the wine that created the Super Tuscan category; Cabernet Sauvignon + Cabernet Franc from coastal Bolgheri; cedar, blackcurrant, graphite, tobacco; 20+ year potential',
 'meat_poultry', 'rich_fatty_smoky', 'Lamb rack with herb crust and pommes sarladaises — treating Sassicaia as the Bordeaux equivalent it inspired; the classic pairing applied to Italy''s finest Cabernet',
 'complement', 'Rack of lamb with herb crust is the defining pairing for Bordeaux Cabernet and transfers perfectly to Sassicaia; the wine''s Franc-derived cedar and graphite are ideally structured for lamb', 'main', 'classic', 1, true),

-- ============================================================
-- 336: Ornellaia Bolgheri Superiore (2 → 5 target; add 3)
-- Merlot-dominant Super Tuscan; velvet tannins, blackberry, cedar, violet
-- ============================================================
(336, 'wine_still', 'Bolgheri Superiore DOC', 'Ornellaia — the velvet Super Tuscan; Merlot-dominant (65%) with Cabernet Sauvignon and Cab Franc; blackberry, cedar, violet, chocolate, tobacco; exceptional approachability',
 'meat_poultry', 'rich_fatty_smoky', 'Duck breast with cherry-port reduction and duck fat roasted vegetables — the Merlot character and cherry sauce create a natural bridge',
 'complement', 'Ornellaia''s Merlot-dominant velvet and cherry character are perfectly matched to duck breast''s richness; the cherry-port reduction mirrors the wine''s fruit while fat softens the tannins', 'main', 'established', 1, true),

(336, 'wine_still', 'Bolgheri Superiore DOC', 'Ornellaia — the velvet Super Tuscan; Merlot-dominant (65%) with Cabernet Sauvignon and Cab Franc; blackberry, cedar, violet, chocolate, tobacco; exceptional approachability',
 'charcuterie_cheese', 'fermented_aged', 'Truffle-aged Gouda (12-month) with dark chocolate and almonds — the Merlot''s chocolate-cedar character resonates with truffle cheese and dark chocolate',
 'bridge', 'Ornellaia''s chocolate-violet notes and aged Gouda''s caramel-truffle complexity create an unusual but compelling bridge; dark chocolate amplifies both', 'cheese', 'suggested', 1, true),

(336, 'wine_still', 'Bolgheri Superiore DOC', 'Ornellaia — the velvet Super Tuscan; Merlot-dominant (65%) with Cabernet Sauvignon and Cab Franc; blackberry, cedar, violet, chocolate, tobacco; exceptional approachability',
 'meat_poultry', 'earthy_herbal', 'Wagyu beef tataki with ponzu and wasabi — Ornellaia''s approachable velvet tannins make it the Super Tuscan best suited for Japanese beef crossover pairings',
 'bridge', 'Ornellaia''s soft tannins and blackberry-cedar character survive the ponzu''s acidity better than Barolo; a contemporary cross-cultural luxury pairing', 'main', 'adventurous', 1, true),

-- ============================================================
-- 337: Antinori Tignanello
-- Sangiovese + Cabernet blend; the wine that modernised Chianti
-- ============================================================
(337, 'wine_still', 'Toscana IGT', 'Antinori Tignanello — Sangiovese (80%) + Cabernet Sauvignon (15%) + Cabernet Franc (5%); the wine that created the Super Tuscan category in 1971; dark cherry, cedar, tobacco, dried herb',
 'meat_poultry', 'rich_fatty_smoky', 'Bistecca alla Fiorentina with roasted garlic and herbs — the Florentine steak and Antinori are Tuscany''s most iconic house pairing',
 'complement', 'The Antinori family estates are at the heart of Florentine cuisine culture; Tignanello''s Sangiovese cherry and Cabernet cedar create the ideal Florentine steak companion', 'main', 'classic', 1, true),

(337, 'wine_still', 'Toscana IGT', 'Antinori Tignanello — Sangiovese (80%) + Cabernet Sauvignon (15%) + Cabernet Franc (5%); the wine that created the Super Tuscan category in 1971; dark cherry, cedar, tobacco, dried herb',
 'meat_poultry', 'earthy_herbal', 'Arista di maiale (Florentine roast pork loin) with fennel pollen, garlic, and rosemary — a Tuscan classic that was made for Sangiovese blends',
 'complement', 'Arista''s fennel-rosemary crust bridges with the Sangiovese-Cabernet blend''s dried herb character; the wine''s structure holds against the pork''s fat without overpowering', 'main', 'classic', 1, true),

(337, 'wine_still', 'Toscana IGT', 'Antinori Tignanello — Sangiovese (80%) + Cabernet Sauvignon (15%) + Cabernet Franc (5%); the wine that created the Super Tuscan category in 1971; dark cherry, cedar, tobacco, dried herb',
 'charcuterie_cheese', 'fermented_aged', 'Fiore Sardo (Sardinian aged pecorino) with black olive paste and grissini — the intensely flavoured aged sheep''s cheese from Sardinia tested against Tignanello''s complexity',
 'complement', 'Fiore Sardo''s intense sheep-smoke character (traditional smoking) finds a worthy partner in Tignanello''s tobacco-cedar complexity; a prestige Italian cheese-wine moment', 'cheese', 'established', 1, true),

(337, 'wine_still', 'Toscana IGT', 'Antinori Tignanello — Sangiovese (80%) + Cabernet Sauvignon (15%) + Cabernet Franc (5%); the wine that created the Super Tuscan category in 1971; dark cherry, cedar, tobacco, dried herb',
 'fungi_truffles', 'earthy_herbal', 'Porcini-stuffed tortellini in beef consommé — the umami depth of the broth and mushroom filling creates a elegant high-low contrast with Tignanello',
 'complement', 'The consommé''s concentrated beef-umami and the porcini''s earthiness are calibrated for Tignanello''s cherry-tobacco complexity; the pasta''s delicacy prevents the match from becoming too heavy', 'main', 'established', 1, true),

-- ============================================================
-- 338: Montevertine Le Pergole Torte
-- 100% Sangiovese; one of Chianti Classico's most revered artisan wines
-- ============================================================
(338, 'wine_still', 'Toscana IGT', 'Montevertine Le Pergole Torte — 100% Sangiovese, Chianti Classico''s great artisan dissenter; concentrated cherry, dried herbs, earth, violet, mineral; the definitive expression of Sangiovese''s elegance',
 'meat_poultry', 'earthy_herbal', 'Peposo alla Fornacina (Tuscan pepper beef stew) — the ancient Tuscan brick-kiln worker''s pepper beef stew, a dish of extraordinary earthiness for an equally earthy wine',
 'complement', 'Peposo''s black pepper-beef reduction and Le Pergole Torte''s earth-cherry character are both expressions of the same Tuscan terroir''s directness and power', 'main', 'classic', 1, true),

(338, 'wine_still', 'Toscana IGT', 'Montevertine Le Pergole Torte — 100% Sangiovese, Chianti Classico''s great artisan dissenter; concentrated cherry, dried herbs, earth, violet, mineral; the definitive expression of Sangiovese''s elegance',
 'meat_poultry', 'rich_fatty_smoky', 'Tagliata di Chianina with rocket and Parmigiano — the simplest Tuscan beef preparation lets Le Pergole Torte''s elegance speak',
 'complement', 'The simplicity of tagliata (sliced grilled beef) is the ideal canvas for an artisan wine of Le Pergole Torte''s elegance; the rocket''s bitterness amplifies the wine''s herb notes', 'main', 'classic', 1, true),

(338, 'wine_still', 'Toscana IGT', 'Montevertine Le Pergole Torte — 100% Sangiovese, Chianti Classico''s great artisan dissenter; concentrated cherry, dried herbs, earth, violet, mineral; the definitive expression of Sangiovese''s elegance',
 'charcuterie_cheese', 'fermented_aged', 'Marzolino (fresh sheep''s milk cheese) with Tuscan herbs and olive oil — the delicate spring sheep''s milk against the wine''s violet-cherry elegance',
 'complement', 'Marzolino''s delicate freshness (March sheep''s milk, traditionally) and the wine''s floral-mineral elegance create an understated but beautiful pairing; Tuscan herbs bridge the terroir', 'cheese', 'suggested', 1, true),

(338, 'wine_still', 'Toscana IGT', 'Montevertine Le Pergole Torte — 100% Sangiovese, Chianti Classico''s great artisan dissenter; concentrated cherry, dried herbs, earth, violet, mineral; the definitive expression of Sangiovese''s elegance',
 'vegetables_legumes', 'earthy_herbal', 'Fagioli all''uccelletto (white beans with sage, garlic, and tomato) — the Tuscan peasant dish that demonstrates Sangiovese''s affinity for legumes',
 'complement', 'White beans'' earthy creaminess and sage-garlic-tomato preparation create the Tuscan rusticity that Le Pergole Torte''s artisan character responds to; a pairing that celebrates Sangiovese''s terroir roots', 'main', 'established', 1, true),

-- ============================================================
-- 339: Fontodi Flaccianello della Pieve
-- 100% Sangiovese from Panzano ''amphitheatre''; intense, mineral
-- ============================================================
(339, 'wine_still', 'Colli della Toscana Centrale IGT', 'Fontodi Flaccianello — 100% Sangiovese from the legendary Conca d''Oro ''golden amphitheatre'' in Panzano; concentrated cherry, dried flowers, mineral precision, 15+ year aging',
 'meat_poultry', 'rich_fatty_smoky', 'Florentine tomahawk bistecca (3kg) with truffle salt and aged balsamic — the most dramatic Tuscan beef presentation for a landmark Sangiovese',
 'complement', 'Flaccianello''s mineral precision and cherry concentration are calibrated for the Florentine steak''s intense char-fat character; truffle salt bridges the wine''s mineral depth', 'main', 'classic', 1, true),

(339, 'wine_still', 'Colli della Toscana Centrale IGT', 'Fontodi Flaccianello — 100% Sangiovese from the legendary Conca d''Oro ''golden amphitheatre'' in Panzano; concentrated cherry, dried flowers, mineral precision, 15+ year aging',
 'fungi_truffles', 'earthy_herbal', 'Crostini di fegatini con tartufo nero (chicken liver toasts with black truffle) — the classic Tuscan starter elevated with truffle to match Flaccianello''s intensity',
 'complement', 'Chicken liver''s iron-bitter character bridges with Flaccianello''s earth-mineral depth; black truffle elevates the combination to match the wine''s concentration', 'starter', 'established', 1, true),

(339, 'wine_still', 'Colli della Toscana Centrale IGT', 'Fontodi Flaccianello — 100% Sangiovese from the legendary Conca d''Oro ''golden amphitheatre'' in Panzano; concentrated cherry, dried flowers, mineral precision, 15+ year aging',
 'charcuterie_cheese', 'fermented_aged', 'Stagionato di fossa (cave-aged cheese, 90 days in tuff caves) — the oxidative character of cave aging paired with a wine of mineral precision',
 'complement', 'Cave-aged cheese''s unusual oxidative-mineral character is an intriguing match for Flaccianello''s mineral precision; both have a distinctive ''place'' quality that makes them natural companions', 'cheese', 'established', 1, true),

(339, 'wine_still', 'Colli della Toscana Centrale IGT', 'Fontodi Flaccianello — 100% Sangiovese from the legendary Conca d''Oro ''golden amphitheatre'' in Panzano; concentrated cherry, dried flowers, mineral precision, 15+ year aging',
 'meat_poultry', 'earthy_herbal', 'Cinghiale al Chianti con polenta (wild boar braised in Chianti) — the Tuscan game preparation that mirrors the appellation and the wine''s character',
 'complement', 'Wild boar braised in Chianti is the regional expression: the wine in the braise mirrors the wine at the table; forest-earth character of boar amplified by Flaccianello''s mineral depth', 'main', 'classic', 1, true),

-- ============================================================
-- 340: Isole e Olena Cepparello
-- 100% Sangiovese; elegant, precise, one of Chianti Classico's quiet greats
-- ============================================================
(340, 'wine_still', 'Toscana IGT', 'Isole e Olena Cepparello — Paolo De Marchi''s great 100% Sangiovese; extraordinary precision and restraint; cherry, dried rose, earth, mineral; consistently one of Chianti Classico''s finest wines',
 'meat_poultry', 'earthy_herbal', 'Lombata di vitello (veal loin) with morel cream and herb jus — veal''s delicacy is an elegant pairing for Cepparello''s restraint',
 'complement', 'Cepparello''s precision and elegance are calibrated for veal''s delicacy rather than beef''s intensity; the morel cream bridges the wine''s earth-mushroom secondary notes', 'main', 'established', 1, true),

(340, 'wine_still', 'Toscana IGT', 'Isole e Olena Cepparello — Paolo De Marchi''s great 100% Sangiovese; extraordinary precision and restraint; cherry, dried rose, earth, mineral; consistently one of Chianti Classico''s finest wines',
 'pasta_grain', 'umami_savoury', 'Pappardelle al ragù di lepre (pasta with hare ragù) — the depth and complexity of hare ragù demands Cepparello''s concentration',
 'complement', 'Hare ragù''s gamey concentration and Sangiovese''s cherry-earth character create one of Tuscany''s great pasta-wine pairings; the wine''s precision prevents the dish from becoming too heavy', 'main', 'classic', 1, true),

(340, 'wine_still', 'Toscana IGT', 'Isole e Olena Cepparello — Paolo De Marchi''s great 100% Sangiovese; extraordinary precision and restraint; cherry, dried rose, earth, mineral; consistently one of Chianti Classico''s finest wines',
 'charcuterie_cheese', 'fermented_aged', 'Colonnata lardo (aged in Carrara marble) with sage and aged Parmigiano — the extraordinary Tuscan/Ligurian border product against a Tuscan red of elegance',
 'bridge', 'Colonnata lardo''s unique rosemary-herb-marble-aged pork fat creates an aromatic bridge with Cepparello''s dried rose and earth; Parmigiano''s salt structures the fat', 'starter', 'established', 1, true),

(340, 'wine_still', 'Toscana IGT', 'Isole e Olena Cepparello — Paolo De Marchi''s great 100% Sangiovese; extraordinary precision and restraint; cherry, dried rose, earth, mineral; consistently one of Chianti Classico''s finest wines',
 'meat_poultry', 'rich_fatty_smoky', 'Pollo al mattone (chicken under a brick) with Tuscan herbs and lemon — a Florentine classic for a Florentine wine of precision',
 'complement', 'Chicken al mattone''s crispy herb-lemon character is perfectly proportioned for Cepparello''s elegance; the Sangiovese''s acidity lifts the chicken without overpowering its delicacy', 'main', 'established', 1, true),

-- ============================================================
-- 341: Bibi Graetz Testamatta
-- Modern Sangiovese from overlooked Fiesole terroir; dark, concentrated
-- ============================================================
(341, 'wine_still', 'Toscana IGT', 'Bibi Graetz Testamatta — ''madman'' Sangiovese from forgotten Fiesole hillside vineyards overlooking Florence; concentrated, modern, dark cherry, spice, tobacco, violets',
 'meat_poultry', 'rich_fatty_smoky', 'Peppered venison loin with root vegetable gratin — the wine''s concentration and spice match the venison''s gamey intensity',
 'complement', 'Testamatta''s concentration and spice are well-matched to venison''s gamey-iron character; the root vegetable gratin bridges the wine''s earthy complexity', 'main', 'established', 2, true),

(341, 'wine_still', 'Toscana IGT', 'Bibi Graetz Testamatta — ''madman'' Sangiovese from forgotten Fiesole hillside vineyards overlooking Florence; concentrated, modern, dark cherry, spice, tobacco, violets',
 'meat_poultry', 'earthy_herbal', 'Fiorentina steak with green peppercorn butter and crispy rosemary potatoes — the local Florence connection: Testamatta grows on the hills above the city that invented this steak',
 'complement', 'The geographic provenance is unusual (Fiesole is above Florence, not Chianti) making Testamatta and Florentine steak a local pairing of surprising specificity', 'main', 'classic', 2, true),

(341, 'wine_still', 'Toscana IGT', 'Bibi Graetz Testamatta — ''madman'' Sangiovese from forgotten Fiesole hillside vineyards overlooking Florence; concentrated, modern, dark cherry, spice, tobacco, violets',
 'charcuterie_cheese', 'fermented_aged', 'Aged Asiago Pressato with roasted hazelnuts and dark cherry jam — the concentrated modern Sangiovese and the aged Veneto cheese with sweet-fruit accompaniment',
 'complement', 'Testamatta''s dark cherry and spice find resonance in cherry jam accompaniment; Asiago''s mild nuttiness bridges with the wine''s concentration without competing', 'cheese', 'suggested', 2, true),

(341, 'wine_still', 'Toscana IGT', 'Bibi Graetz Testamatta — ''madman'' Sangiovese from forgotten Fiesole hillside vineyards overlooking Florence; concentrated, modern, dark cherry, spice, tobacco, violets',
 'pasta_grain', 'umami_savoury', 'Tagliatelle with truffled beef Bolognese — concentrating both the meat and truffle intensity to match the wine''s power',
 'complement', 'Testamatta''s concentration demands an equally intense pasta sauce; truffled Bolognese''s earthy-meat depth is calibrated for the wine''s power while the pasta structure softens tannins', 'main', 'established', 2, true),

-- ============================================================
-- 342: Dal Forno Romano Amarone della Valpolicella
-- Italy's most concentrated wine; 17% abv, 3-4 years drying; prune, chocolate, fig
-- ============================================================
(342, 'wine_still', 'Amarone della Valpolicella DOCG', 'Dal Forno Romano Amarone — among Italy''s most concentrated wines; 3-4 years appassimento, 17%+ abv; prune, dark chocolate, fig, coffee, dried flowers; extraordinary longevity',
 'meat_poultry', 'rich_fatty_smoky', 'Brasato al Amarone (beef braised in Amarone) — the most prestigious Venetian preparation; only Dal Forno''s intensity can both be drunk and used in this dish''s reduction',
 'complement', 'Brasato al Amarone is the ultimate ''wine in the dish + wine in the glass'' pairing; the reduction concentrates the wine''s prune-chocolate character; drinking wine mirrors cooking wine', 'main', 'classic', 1, true),

(342, 'wine_still', 'Amarone della Valpolicella DOCG', 'Dal Forno Romano Amarone — among Italy''s most concentrated wines; 3-4 years appassimento, 17%+ abv; prune, dark chocolate, fig, coffee, dried flowers; extraordinary longevity',
 'charcuterie_cheese', 'fermented_aged', 'Monte Veronese Stagionato d''Allevo (36-month aged cow''s milk from the Lessini mountains) — the local cheese of the Valpolicella hills aged to match Amarone''s complexity',
 'complement', 'Monte Veronese''s crystalline aged character (36+ months) and butterscotch notes are calibrated for Amarone''s prune-chocolate depth; a local cheese-wine pairing of extraordinary quality', 'cheese', 'classic', 1, true),

(342, 'wine_still', 'Amarone della Valpolicella DOCG', 'Dal Forno Romano Amarone — among Italy''s most concentrated wines; 3-4 years appassimento, 17%+ abv; prune, dark chocolate, fig, coffee, dried flowers; extraordinary longevity',
 'dessert_pastry', 'sweet_spiced', 'Dark chocolate fondant with espresso gelato and sea salt — the wine''s chocolate-coffee character creates a dessert pairing of profound intensity',
 'complement', 'Dal Forno''s extraordinary chocolate-coffee concentration at full maturity is rich enough to partner with dark chocolate desserts; a digestif-dessert pairing of maximum intensity', 'dessert', 'established', 1, true),

(342, 'wine_still', 'Amarone della Valpolicella DOCG', 'Dal Forno Romano Amarone — among Italy''s most concentrated wines; 3-4 years appassimento, 17%+ abv; prune, dark chocolate, fig, coffee, dried flowers; extraordinary longevity',
 'meat_poultry', 'rich_fatty_smoky', 'Ossobuco della Valpolicella — braised veal osso buco in the local style with Soave and Amarone in the braise; gremolata, saffron risotto',
 'complement', 'Valpolicella''s most celebrated braise pairs with the region''s most celebrated wine; the collagen-rich shank and the wine''s power are matched in intensity', 'main', 'classic', 1, true),

-- ============================================================
-- 343: Giuseppe Quintarelli Amarone Classico
-- Legendary traditional Amarone; longest aging (7+ years in wood)
-- ============================================================
(343, 'wine_still', 'Amarone della Valpolicella Classico DOCG', 'Quintarelli Amarone Classico — the most revered traditional Amarone; 7+ years in wood before release; dried fig, prune, tar, violets, anise, tobacco; 50-year potential',
 'charcuterie_cheese', 'fermented_aged', 'Grana Padano Riserva (20-month) with walnut honey — the broader, sweeter cousin of Parmigiano finds resonance in the Amarone''s fig-walnut complexity',
 'complement', 'Quintarelli Amarone at 15+ years develops fig, walnut, and honey notes that mirror Grana Padano''s butterscotch-crystal character; the most sophisticated Italian cheese-wine pairing', 'cheese', 'classic', 1, true),

(343, 'wine_still', 'Amarone della Valpolicella Classico DOCG', 'Quintarelli Amarone Classico — the most revered traditional Amarone; 7+ years in wood before release; dried fig, prune, tar, violets, anise, tobacco; 50-year potential',
 'dessert_pastry', 'sweet_fruity', 'Dried fig and walnut tart with vin santo cream — the dried fruit concentration in the tart mirrors the wine''s appassimento character',
 'complement', 'Quintarelli''s dried fruit complexity (a direct result of the appassimento process) resonates perfectly with dried fig and walnut desserts; vin santo cream creates a regional continuity', 'dessert', 'established', 1, true),

(343, 'wine_still', 'Amarone della Valpolicella Classico DOCG', 'Quintarelli Amarone Classico — the most revered traditional Amarone; 7+ years in wood before release; dried fig, prune, tar, violets, anise, tobacco; 50-year potential',
 'meat_poultry', 'rich_fatty_smoky', 'Maialino al forno con finocchio (roast suckling pig with fennel) — the anise character in both the fennel and the wine''s natural anise note create a remarkable bridge',
 'bridge', 'Quintarelli''s anise-tar complexity and fennel''s anise character create an aromatic bridge that works surprisingly well; suckling pig''s fat is structured by the wine''s enormous tannins', 'main', 'established', 1, true),

(343, 'wine_still', 'Amarone della Valpolicella Classico DOCG', 'Quintarelli Amarone Classico — the most revered traditional Amarone; 7+ years in wood before release; dried fig, prune, tar, violets, anise, tobacco; 50-year potential',
 'meat_poultry', 'earthy_herbal', 'Faraona (guinea fowl) al vin santo with chestnuts and preserved lemon — the nuanced game bird prepared with alpine ingredients',
 'complement', 'Guinea fowl''s delicate gaminess and the chestnut''s earthy sweetness are appropriate in proportion to Quintarelli''s complexity; the vin santo in the sauce bridges the wine''s dried fruit notes', 'main', 'established', 1, true),

-- ============================================================
-- 344: Pieropan Soave Classico Calvarino
-- White Garganega; lemon, almond, mineral, floral; benchmark Soave
-- ============================================================
(344, 'wine_still', 'Soave Classico DOC', 'Pieropan Calvarino — one of Italy''s great white wines; Garganega from the volcanic Calvarino cru in Soave Classico; lemon, almond, mineral, floral; extraordinary age-worthiness for a white wine',
 'seafood', 'salty_mineral', 'Sarde in saor (sweet-sour marinated sardines with onions, pine nuts, and raisins) — the Venetian classic that requires a white wine of acidity and mineral weight',
 'complement', 'Soave Calvarino''s volcanic mineral character and almond note are the perfect match for sarde in saor''s complex sweet-sour-pine nut flavor; a classic Venetian pairing', 'starter', 'classic', 2, true),

(344, 'wine_still', 'Soave Classico DOC', 'Pieropan Calvarino — one of Italy''s great white wines; Garganega from the volcanic Calvarino cru in Soave Classico; lemon, almond, mineral, floral; extraordinary age-worthiness for a white wine',
 'seafood', 'delicate_fresh', 'Risotto all''anguilla (eel risotto) — the Veneto''s most ancient freshwater fish preparation with the region''s finest white wine',
 'complement', 'Eel''s richness and the risotto''s butter-cream need a white wine with mineral weight and almond character; Calvarino''s volcanic minerality creates exactly the right counterpoint', 'main', 'established', 2, true),

(344, 'wine_still', 'Soave Classico DOC', 'Pieropan Calvarino — one of Italy''s great white wines; Garganega from the volcanic Calvarino cru in Soave Classico; lemon, almond, mineral, floral; extraordinary age-worthiness for a white wine',
 'vegetables_legumes', 'delicate_fresh', 'Pasta e fagioli (pasta and bean soup) — the simplest Venetian peasant dish with the region''s finest white wine; a demonstration of proportion',
 'complement', 'Soave Calvarino''s mineral acidity and almond finish are perfectly proportioned for the humble creamy bean soup; the floral notes lift the dish without competing with its simplicity', 'main', 'established', 2, true),

(344, 'wine_still', 'Soave Classico DOC', 'Pieropan Calvarino — one of Italy''s great white wines; Garganega from the volcanic Calvarino cru in Soave Classico; lemon, almond, mineral, floral; extraordinary age-worthiness for a white wine',
 'seafood', 'umami_savoury', 'Grilled branzino (sea bass) with lemon, capers, and Venetian-style soffritto — the simplest preparation of Italy''s finest Mediterranean fish',
 'complement', 'The lemon-caper Mediterranean dressing and Calvarino''s citrus-almond character create a seamless aromatic bridge; the wine''s mineral weight supports the sea bass''s flavour', 'main', 'classic', 2, true),

-- ============================================================
-- 345: Allegrini Amarone della Valpolicella Classico
-- Modern Amarone; more accessible than Dal Forno or Quintarelli
-- ============================================================
(345, 'wine_still', 'Amarone della Valpolicella Classico DOCG', 'Allegrini Amarone Classico — a more accessible expression of great Amarone; modern vinification; dark cherry, chocolate, dried herbs, tobacco; excellent but approachable earlier than Dal Forno',
 'charcuterie_cheese', 'fermented_aged', 'Aged Asiago d''Allevo (12-month) with figs and balsamic — the Veronese cheese from the same hillside as the wine',
 'complement', 'Asiago d''Allevo and Amarone della Valpolicella are born on the same Veronese hillsides; the cheese''s fruity-nutty character bridges with the Amarone''s dried cherry-fig complexity', 'cheese', 'classic', 2, true),

(345, 'wine_still', 'Amarone della Valpolicella Classico DOCG', 'Allegrini Amarone Classico — a more accessible expression of great Amarone; modern vinification; dark cherry, chocolate, dried herbs, tobacco; excellent but approachable earlier than Dal Forno',
 'meat_poultry', 'rich_fatty_smoky', 'Brasato al Amarone (beef cheek braised in Amarone) — the classic Veronese preparation; Allegrini is used in the braise itself',
 'complement', 'Using Amarone in the braise and serving the same wine is the Veronese tradition; Allegrini''s accessibility (vs. Dal Forno) makes it the practical choice for this preparation', 'main', 'classic', 2, true),

(345, 'wine_still', 'Amarone della Valpolicella Classico DOCG', 'Allegrini Amarone Classico — a more accessible expression of great Amarone; modern vinification; dark cherry, chocolate, dried herbs, tobacco; excellent but approachable earlier than Dal Forno',
 'dessert_pastry', 'sweet_spiced', 'Pandoro with mascarpone cream and dark cherry compote — the Veronese Christmas bread (Pandoro is from Verona) with the city''s greatest wine',
 'complement', 'Pandoro and Amarone is Verona''s Christmas tradition; the bread''s buttery vanilla richness and the cherry compote mirror the wine''s dried cherry-chocolate character', 'celebration', 'classic', 2, true),

(345, 'wine_still', 'Amarone della Valpolicella Classico DOCG', 'Allegrini Amarone Classico — a more accessible expression of great Amarone; modern vinification; dark cherry, chocolate, dried herbs, tobacco; excellent but approachable earlier than Dal Forno',
 'meat_poultry', 'earthy_herbal', 'Pasta e fagioli alla veneta with cotechino (white bean soup with spiced sausage) — a hearty Venetian classic for a hearty Venetian wine',
 'complement', 'Cotechino''s spiced pork richness and the white beans'' earthiness create the substance that matches Amarone''s power; the wine''s structure cuts through the fat', 'main', 'established', 2, true);

COMMIT;
