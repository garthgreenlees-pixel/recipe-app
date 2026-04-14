#!/usr/bin/env python3
"""Mediterranean Session — Batch 5: Champagne
Producers, Products, service_protocol (MOF depth), beverage_references, pairing_intelligence.
Region IDs: Champagne=143, Montagne de Reims=144, Côte des Blancs=145, Vallée de la Marne=146.
"""
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, P, PROD, REF, PAIR, PROTOCOL

conn, cur = get_conn()

# ════════════════════════════════════════════════════════════════════════════════
# CHAMPAGNE PRODUCERS
# ════════════════════════════════════════════════════════════════════════════════
print("=== CHAMPAGNE PRODUCERS ===")

krug = P(cur, "Krug", "winery", 143, "France",
    production_philosophy="champagne_absolutist",
    philosophy_description="Founded by Johann-Joseph Krug in 1843. Now owned by LVMH but maintains complete autonomy. Krug produces from the largest library of reserve wines (wines from multiple years kept for blending) in Champagne — up to 150 wines from 10+ years. Every Krug wine — including the multi-vintage Grande Cuvée — begins in oak barrels (1/8 of the total production capacity). The oak adds texture and breadth without domination. The Grande Cuvée is typically a blend of 120+ wines from 10+ harvests. Clos du Mesnil (single vineyard, single vintage blanc de blancs) and Clos d'Ambonnay (single vineyard Pinot Noir blanc de noirs) are among the rarest Champagnes made. BC importer: LVMH Moet Hennessy / Mark Anthony [NEEDS VERIFICATION].",
    key_personnel=[{"role": "chef de cave", "name": "Julie Cavil"}],
    production_details={"reserve_library": "150+ wines from 10+ years", "fermentation": "all in small oak barrels",
                        "flagship": "Grande Cuvée", "bc_importer": "Mark Anthony Group [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Krug is considered the producer most consistently making wine at the limit of Champagne's potential. Wine critics award 100 points to certain Krug bottlings. The Clos du Mesnil from exceptional years (1979, 1988, 1995, 2002, 2006) is priced near DRC wines.",
    price_positioning="ultra_premium", authority_tier=1)

salon = P(cur, "Salon", "winery", 145, "France",
    production_philosophy="single_terroir_absolute",
    philosophy_description="The most singular Champagne — produced only in exceptional years (approximately every 3–5 years), only from the single village of Le Mesnil-sur-Oger, only from Chardonnay (blanc de blancs), only from a single vineyard within Le Mesnil. Founded by Eugène-Aimé Salon in 1905 — he produced wine only for personal consumption until 1921. Salon is the most convincing argument that a single-village, single-vintage blanc de blancs can achieve the complexity of a multi-vintage house Champagne. Less than 60,000 bottles per vintage are produced — and vintages are not released every year.",
    key_personnel=[{"role": "chef de cave", "name": "Didier Depond"}],
    production_details={"production": "~60,000 bottles per vintage (not every year)", "style": "single vintage, single village, single variety, single vineyard",
                        "bc_importer": "Cas-Dri Pacific [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Salon is the 'Romanée-Conti of Champagne' — limited production, extreme rarity, extremely high auction prices (2002 Salon trades at $300–$500 per bottle). The wine is an argument for terroir over blending.",
    price_positioning="ultra_premium", authority_tier=1)

selosse = P(cur, "Jacques Selosse", "winery", 145, "France",
    production_philosophy="terroir_grower_champagne",
    philosophy_description="Anselme Selosse (Jacques's son) is the founding prophet of the Grower Champagne movement — the récoltant-manipulant (RM) who grows their own grapes and makes their own wine, the antithesis of the grande maison (NM) that blends from purchased fruit. Selosse introduced concepts from Burgundy to Champagne: barrel ageing, oxidative style, terroir expression, biodynamic farming. His Substance (a perpetual blend, solera-style) and Initiale (the entry-level expression) are unlike any other Champagne. Anselme's philosophy: 'A wine that does not express its soil is a costume, not a character.'",
    key_personnel=[{"role": "winemaker", "name": "Anselme Selosse"}],
    production_details={"farming": "biodynamic", "style": "oxidative, terroir-expressive",
                        "bc_importer": "Skye Import [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Anselme Selosse has influenced the next generation of Champagne producers more than any single figure. His questioning of the grande maison model opened the door to hundreds of grower producers finding a global audience.",
    price_positioning="ultra_premium", authority_tier=1)

dom_perignon = P(cur, "Dom Pérignon", "winery", 143, "France",
    production_philosophy="prestige_cuvee_icon",
    philosophy_description="The world's most famous Champagne brand and LVMH's prestige Champagne, produced by Moët & Chandon. Chef de cave Richard Geoffroy (1990–2018) and now Vincent Chaperon have established Dom Pérignon as a Champagne of genuine depth and cellaring potential. The wine is only vintage-dated — no non-vintage. Three 'plénitudes' (release windows): P1 (first release, 8–10 years on lees), P2 (15 years on lees), P3 (25 years on lees) — each represents a different maturity stage of the same wine. Only truly great years are declared.",
    key_personnel=[{"role": "chef de cave", "name": "Vincent Chaperon"}],
    production_details={"vintage_only": True, "plenitudes": "P1, P2, P3 release stages",
                        "bc_importer": "Mark Anthony Group [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

pierre_peters = P(cur, "Pierre Péters", "winery", 145, "France",
    production_philosophy="grower_blanc_de_blancs",
    philosophy_description="One of Le Mesnil-sur-Oger's finest grower producers. Rodolphe Péters produces blanc de blancs of extraordinary mineral precision from old vines in Le Mesnil-sur-Oger. The Cuvée de Réserve and the flagship Les Chétillons (a single-vineyard, older-vine expression) are among the most compelling grower Champagnes made. The wines demonstrate that grower Champagne can achieve complexity and depth that rivals the grandes maisons — at significantly lower price.",
    key_personnel=[{"role": "winemaker", "name": "Rodolphe Péters"}],
    production_details={"style": "blanc de blancs, grower RM", "bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="estate", price_positioning="premium", authority_tier=2)

bollinger = P(cur, "Bollinger", "winery", 144, "France",
    production_philosophy="pinot_noir_champagne_house",
    philosophy_description="The most famous Pinot Noir-focused grande maison. The Renaud-Cointreau family (still independent — no LVMH or Pernod Ricard ownership). Key: La Grande Année (vintage) is one of the most age-worthy non-prestige Champagnes. R.D. (Récemment Dégorgé — recently disgorged) is their prestige cuvée, aged an extraordinary 8+ years on lees then disgorged to order. Bollinger is the only grande maison still fermenting reserve wines in magnums (larger bottle = slower oxidation = fresher reserves). The BBC's James Bond has been a Bollinger devotee since the 1970s.",
    production_details={"reserve": "fermented in magnums", "bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

egly = P(cur, "Egly-Ouriet", "winery", 144, "France",
    production_philosophy="grower_pinot_noir_grand_cru",
    philosophy_description="The reference Ambonnay grower producer — and arguably the finest grower Pinot Noir Champagne producer. Francis Egly farms biodynamically from old vines (average 40 years, some over 70 years) in Ambonnay Grand Cru. The Blanc de Noirs Ambonnay Grand Cru is a revelation: a blanc de noirs (white wine from black-skinned grapes) of extraordinary depth. The Brut Tradition is an entry-point that can age 10+ years. Allocations are tiny; global demand is enormous.",
    key_personnel=[{"role": "winemaker", "name": "Francis Egly"}],
    production_details={"farming": "biodynamic", "bc_importer": "Classic Wine Imports [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

# ════════════════════════════════════════════════════════════════════════════════
# CHAMPAGNE PRODUCTS
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== CHAMPAGNE PRODUCTS ===")

krug_gc = PROD(cur, "Krug Grande Cuvée", "wine_sparkling", krug, 143,
    subcategory="blanc",
    description="The 'multi-vintage' benchmark for Champagne complexity — a blend of 120+ wines from 10+ harvests, all fermented in small oak barrels. The Grande Cuvée is one of the world's great wines despite being technically non-vintage. The current edition (171st, 172nd, etc.) carries an 'Edition' number that corresponds to a base year. The toasty, nutty, brioche, citrus, and mineral complexity of Grande Cuvée is the gold standard for multi-vintage Champagne. Drink on release or cellar 10–20 years. BC: Mark Anthony Group. CAD $250–$350.",
    quality_tier="reserve",
    deductive_profile={"colour": "golden", "nose": "brioche, toasted hazelnut, citrus, white fruit, honey, mineral",
                       "palate": "rich, complex, yeast autolysis dominant; extraordinarily long finish"},
    service_specs={"temp_c": 10, "glass": "white Burgundy tulip or wide Champagne flute",
                   "note": "serve in wider glass to allow aromatics to develop"},
    flavour_markers=["brioche", "toasted hazelnut", "citrus", "white peach", "honey", "mineral", "yeast autolysis"],
    flavour_weight="full", flavour_profile_type="yeast_dominant",
    price_tier="ultra_premium", price_range_cad="$250–$350")

salon_mesnil = PROD(cur, "Salon Blanc de Blancs Le Mesnil-sur-Oger", "wine_sparkling", salon, 145,
    subcategory="blanc de blancs",
    description="The most singular non-vintage Champagne: single village (Le Mesnil-sur-Oger), single variety (Chardonnay), single vineyard, single vintage (not produced every year). Aged minimum 10 years on lees — often released much later. The wine is intense, chalk-mineral, citrus-zest, and almost austere in youth — it needs a decade of bottle age to reveal the extraordinary complexity of Le Mesnil terroir. Recent vintages: 2007, 2008, 2012, 2013, 2014. BC: Cas-Dri Pacific. CAD $400–$800.",
    quality_tier="reserve",
    deductive_profile={"colour": "pale gold with green tints", "nose": "chalk, citrus zest, white flower, brioche — the most mineral Champagne nose",
                       "palate": "intense, searingly mineral, long; requires 10+ years to open"},
    service_specs={"temp_c": 10, "glass": "wide Champagne flute or white Burgundy tulip",
                   "note": "serve with 10+ years of cellaring for best results"},
    flavour_markers=["chalk mineral", "citrus zest", "white flower", "brioche", "oyster shell", "crystalline"],
    flavour_weight="medium-full", flavour_profile_type="mineral",
    price_tier="ultra_premium", price_range_cad="$400–$800")

dom_perignon_p1 = PROD(cur, "Dom Pérignon P1 Vintage", "wine_sparkling", dom_perignon, 143,
    subcategory="blanc vintage",
    description="The first plénitude of Dom Pérignon — released after 8–10 years on lees. A blend of Chardonnay (~55%) and Pinot Noir (~45%) from a single exceptional vintage. The P1 release represents the wine at its first maturity window — opulent, toasty, creamy, with the primary fruit still vibrant. Great vintages: 2008 (benchmark), 2012, 2013, 2015. The P2 (15 years on lees) and P3 (25 years on lees) represent deeper maturity stages. BC: Mark Anthony Group. CAD $250–$450 for P1.",
    quality_tier="reserve",
    deductive_profile={"colour": "golden", "nose": "cream, brioche, white stone fruit, mineral, subtle toast",
                       "palate": "opulent, creamy texture; exceptional vintage clarity; P1 shows primary fruit still present"},
    service_specs={"temp_c": 10, "glass": "wide Champagne flute"},
    flavour_markers=["cream", "brioche", "white stone fruit", "mineral", "toast", "almond"],
    flavour_weight="full", price_tier="ultra_premium", price_range_cad="$250–$450")

peters_les_chetillons = PROD(cur, "Pierre Péters Les Chétillons", "wine_sparkling", pierre_peters, 145,
    subcategory="blanc de blancs grower",
    description="Pierre Péters' single-vineyard old-vine blanc de blancs — one of the most compelling arguments for grower Champagne. Les Chétillons is a 3.5-hectare plot in Le Mesnil-sur-Oger with vines averaging 50+ years. The wine is the textbook example of Chardonnay terroir transparency in Champagne: chalk, citrus, mineral, ginger, white peach. At 10+ years of age, extraordinary complexity emerges. Available in BC through Lifford at a fraction of Salon's price with comparable terroir expression.",
    quality_tier="estate",
    deductive_profile={"colour": "pale gold", "nose": "chalk, citrus, ginger, white peach, mineral",
                       "palate": "precise, mineral-driven, 8–12 year ageing window"},
    service_specs={"temp_c": 10},
    flavour_markers=["chalk", "citrus", "ginger", "white peach", "mineral", "sea-salt"],
    flavour_weight="medium", flavour_profile_type="mineral",
    price_tier="premium", price_range_cad="$120–$200")

bollinger_rg = PROD(cur, "Bollinger Special Cuvée", "wine_sparkling", bollinger, 144,
    subcategory="blanc multi-vintage",
    description="Bollinger's non-vintage reference Champagne — and arguably the finest quality-to-price Champagne made. Pinot Noir dominant (60%+) with reserve wines fermented in magnums from multiple years. The wine has a distinctive autumnal richness: red apple, brioche, pain grillé, and a savouriness unusual in Champagne. More structured and food-friendly than most non-vintage. The Special Cuvée represents Bollinger's house philosophy — vinosity and complexity over delicacy. BC: Lifford. CAD $80–$100.",
    quality_tier="estate",
    deductive_profile={"colour": "golden", "nose": "red apple, brioche, pain grillé, savoury notes, subtle red fruit",
                       "palate": "rich, structured, vinous; excellent food Champagne"},
    service_specs={"temp_c": 10},
    flavour_markers=["red apple", "brioche", "pain grillé", "savoury", "yeast autolysis"],
    flavour_weight="medium-full", price_tier="premium", price_range_cad="$80–$100")

egly_bn = PROD(cur, "Egly-Ouriet Blanc de Noirs Ambonnay Grand Cru", "wine_sparkling", egly, 144,
    subcategory="blanc de noirs grower",
    description="The reference blanc de noirs Champagne — Pinot Noir from old-vine Ambonnay Grand Cru vineyards (biodynamic farming, average vine age 40+ years). White wine from a black-skinned grape, with no skin contact: the colour is near-colourless, yet the depth, structure, and richness are extraordinary. The wine ages beautifully for 10–15 years, developing extraordinary complexity. BC: Classic Wine Imports [NEEDS VERIFICATION]. CAD $150–$200.",
    quality_tier="reserve",
    deductive_profile={"colour": "pale gold", "nose": "red fruit impression (raspberry, strawberry) despite white colour, mineral, brioche, wild yeast",
                       "palate": "structured, full-bodied for Champagne; 10–15 year ageing"},
    service_specs={"temp_c": 10},
    flavour_markers=["raspberry", "strawberry", "mineral", "brioche", "wild yeast"],
    flavour_weight="medium-full", price_tier="ultra_premium", price_range_cad="$150–$200")

# ════════════════════════════════════════════════════════════════════════════════
# CHAMPAGNE SERVICE PROTOCOL — MOF DEPTH
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== CHAMPAGNE SERVICE PROTOCOL ===")

champagne_protocol = PROTOCOL(cur,
    "Champagne Service — Full MOF Sequence",
    "champagne_service",
    "wine",
    procedure="""FULL CHAMPAGNE SERVICE SEQUENCE (MOF/CMS Standard):

PRE-SERVICE:
1. TEMPERATURE VERIFICATION: Champagne should arrive at the table at 8–10°C. Non-vintage service temperature: 8°C. Vintage and prestige cuvée: 10–11°C (slightly warmer to allow aromatics to express). NEVER below 6°C (kills aromas) or above 13°C (excessive effervescence, flat).
2. GLASS SELECTION: Select glassware appropriate to the wine. Traditional flute (long and narrow) — preserves bubbles, limits aroma expression. White wine tulip (wider bowl) — preferred by sommeliers and producers for aromatic expression and palate complexity. Coupe — do not use except for theatrical occasions; kills effervescence immediately.
3. ICE BUCKET: Prepare ice and water (not ice alone — water conducts cold more efficiently). Wrap bottle in white cloth or napkin before service.

PRESENTATION:
4. Present the bottle to the host before opening. Label faces host. Announce vintage and house verbally: "I have here the [year] [house name], a [blanc de blancs/vintage/etc.] from [region]. Shall I proceed?"
5. Await confirmation from the host before opening.

FOIL REMOVAL:
6. Cut foil below the wire cage collar using the foil knife (or sommelier's knife point). Do NOT remove the entire foil — only cut below the cage. Remove the circular foil piece cleanly without tearing.

CAGE MANAGEMENT:
7. Loosen the cage — six half-turns counterclockwise (standard cage closes in exactly 6 half-turns). Do NOT remove the cage fully until ready to open. Keep your thumb firmly on the top of the cork through the cage at all times.
8. Keep the bottle at a 45-degree angle, pointed AWAY from all guests. A bottle held vertically is more likely to have the cork eject violently — the 45-degree angle controls the release.

THE OPENING — 'THE SIGH, NOT THE POP':
9. With the cage loosened (but still on or just removed), grasp the cork firmly with one hand (cloth napkin wrapped around the cork helps grip and absorbs any spillage). With the other hand, grip the bottle firmly at the base.
10. TWIST THE BOTTLE (not the cork). The cork should remain stationary while the bottle rotates. This is the critical distinction of professional service — amateurs twist the cork; professionals twist the bottle.
11. As the cork releases from the bottle, apply counter-pressure with the hand holding the cork. The release should be slow, controlled, and near-silent — 'the sigh of a contented woman' in the French idiom. A loud pop indicates loss of control and excess carbonation released. The sigh indicates correct service temperature and controlled release.
12. If the cork is stubborn: re-grip and continue twisting the bottle. Do NOT jerk or force. If a cork breaks, use a two-pronged cork puller (Ah-So) through the cage or a Champagne-specific cork extractor.

POURING:
13. Pour a small amount (1/3 glass) into the host's glass first for evaluation.
14. Await approval (brief nod or "thank you" is sufficient — the host is not doing a full tasting ritual for sparkling wine).
15. Pour in a single continuous motion for each guest. Hold the bottle by the base (NOT the label — fingerprints on the label are unprofessional). Tip the glass at approximately 45° to the bottle to control foam.
16. Pour to 2/3 of the glass height maximum. The classic rule: 'pour three-quarters full for flute, two-thirds for tulip.' Overfilling destroys the nose space.
17. Wipe the bottle lip after each pour with the napkin.
18. Return to the host's glass and complete the pour.

POST-SERVICE:
19. Return bottle to ice bucket with label facing the host.
20. Check effervescence levels in glasses every 8–10 minutes. Champagne served warm foams excessively; Champagne served too cold loses carbonation rapidly. Temperature management is continuous throughout service.

NV CHAMPAGNE: consume within 3 hours of opening.
VINTAGE/PRESTIGE: can hold 4–6 hours if kept cold and properly recorked.

RECORKING OPEN CHAMPAGNE: A Champagne stopper (the hinged metal clip with rubber seal) is significantly more effective than the original cork. Insert firmly into the bottle. The common belief that a silver spoon in the bottle neck preserves bubbles is a myth with no scientific basis.""",
    description="The complete Court of Master Sommeliers / MOF sommelier standard for Champagne service, from temperature management through the sigh-not-pop opening to pouring technique.",
    rationale="Champagne service is one of the most visible and tested skills in fine dining sommellerie. It is the most frequently examined practical skill at the CMS Certified and Advanced levels. The 'sigh not pop' is the defining distinction between professional and amateur service.",
    common_errors="""1. LOUD POP: Indicates too much force on the cork, incorrect technique (twisting cork not bottle), or wine served too warm. A pop loses carbonation and risks injury.
2. SPILLAGE: Usually from not controlling the cork as pressure builds, or bottle angle too steep (vertical rather than 45°).
3. FOIL CUTTING INCORRECTLY: Cutting the foil above the cage collar is incorrect and potentially dangerous (jagged foil can cut hands). Always cut below the cage collar.
4. POINTING BOTTLE AT GUESTS: The bottle must always be angled away from all persons.
5. WRONG GLASS: Using a coupe for a serious Champagne is inappropriate in fine dining; it kills effervescence too quickly and shows insufficient knowledge.
6. POURING TOO MUCH: Filling the glass above two-thirds allows the wine to go flat before it can be appreciated.
7. WARM SERVICE TEMPERATURE: Champagne served above 13°C foams excessively and loses delicacy.
8. IGNORING THE HOST CONFIRMATION: Always present and obtain confirmation before opening.""",
    guest_communication="Present: '[Vintage/House/Style] — shall I proceed?' After opening: 'I'll let this breathe momentarily before I complete your pour.' After pouring: 'I'll leave the bottle here for you — please let me know when you'd like your glasses refreshed.'",
    equipment_required=["ice bucket with ice and water", "white linen napkin", "foil knife or sommelier's knife",
                        "Champagne stopper for open bottles", "glass cloth for bottle drip"],
    skill_level="advanced", authority_tier=1,
    source_text="Court of Master Sommeliers Advanced Exam / Meilleur Ouvrier de France Sommelier")

# ════════════════════════════════════════════════════════════════════════════════
# CHAMPAGNE REFERENCES
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== CHAMPAGNE REFERENCES ===")

REF(cur,
    "Champagne — Traditional Method, Dosage, and the Style Spectrum",
    "wine_regions",
    description="Champagne's traditional method (méthode traditionnelle / méthode champenoise) is the most complex wine production process in the world — involving primary fermentation, assemblage (blending), secondary fermentation in bottle, lees ageing, riddling, disgorgement, and dosage. Each stage contributes to the wine's character. The dosage (the final addition of wine + sugar before corking) determines the style designation from Extra Brut to Doux.",
    key_principles="""THE TRADITIONAL METHOD STAGES:

1. HARVEST AND BASE WINE: Grapes are harvested and pressed gently (maximum 2,550 litres from 4,000kg of grapes under AOC rules). The first pressing (taille 1 + taille 2) gives the finest juice. Base wine is fermented to dryness — a high-acid, low-alcohol wine (approximately 10% ABV) that is not pleasant to drink alone.

2. ASSEMBLAGE (BLENDING): The most skilled stage. The chef de cave blends wines from multiple villages, varieties, and in non-vintage Champagne, multiple years. Reserve wines (older vintages held back) are added to maintain house style across years. A typical NV blend might include 30–40% reserve wines. This is where the creative intelligence of the house is expressed.

3. LIQUEUR DE TIRAGE: A mixture of sugar and yeast is added to the blended base wine before bottling. This triggers the secondary fermentation inside the sealed bottle — the source of Champagne's bubbles.

4. SECONDARY FERMENTATION AND LEES AGEING: The sealed bottle undergoes secondary fermentation (CO2 cannot escape — it is absorbed into the wine under pressure). The yeast cells then die and break down (autolysis), releasing amino acids, polysaccharides, and lipids that contribute to the characteristic Champagne complexity: brioche, toast, biscuit, cream, nuts. MINIMUM AGEING:
   - Non-vintage Champagne: 15 months on lees (minimum)
   - Vintage Champagne: 36 months on lees (minimum)
   - Most prestige cuvées: 5–10+ years on lees

5. RIDDLING (REMUAGE): The bottles are gradually tilted nose-down to collect the dead yeast cells (lees) in the bottle neck. Traditional riddling (pupitres — A-frame wooden racks) takes 6–8 weeks of daily quarter-turns. Modern gyropalettes (automated riddling machines) complete the process in 5–7 days. The finest houses (Krug, Bollinger) still use traditional riddling for prestige cuvées.

6. DISGORGEMENT (DÉGORGEMENT): The bottle neck (with accumulated lees) is frozen in a -27°C brine bath. The temporary crown cap is removed — the frozen plug of lees is ejected by the CO2 pressure. The wine is almost ready.

7. DOSAGE (LIQUEUR D'EXPÉDITION): A mixture of wine and sometimes sugar (the 'dosage') is added to replace the lost volume. The amount of sugar in the dosage determines the final style:

STYLE DESIGNATIONS BY DOSAGE (g/L residual sugar):
- Extra Brut: 0–6 g/L — bone dry, mineral, no perceivable sweetness
- Brut: 0–12 g/L — the most common designation; slightly off-dry (up to 12 g/L is effectively imperceptible on the palate due to acidity)
- Extra Sec (Extra Dry): 12–17 g/L — slightly sweet (paradoxically 'Extra Dry' is sweeter than 'Brut')
- Sec (Dry): 17–32 g/L — off-dry to medium
- Demi-Sec: 32–50 g/L — sweet, excellent with dessert
- Doux: 50+ g/L — very sweet, almost a dessert wine

GROWER CHAMPAGNE vs GRANDE MAISON:
NM (Négociant Manipulant): The grande maison — purchases grapes and makes its own Champagne from purchased fruit + owned vineyards. Moët, Veuve Clicquot, Krug, Bollinger, etc.
RM (Récoltant Manipulant): The grower — grows their own grapes, makes their own wine. Selosse, Egly-Ouriet, Pierre Péters, etc. The modern 'artisan Champagne' movement.
RC (Récoltant Coopérateur): Grower-cooperator — grows grapes but has them vinified at a cooperative.
CM (Coopérative de Manipulation): The cooperative — makes wine from members' grapes.
The code appears on every Champagne label below the EU lot number — look for NM, RM, RC, or CM followed by a number.""",
    skill_level="advanced", authority_tier=1,
    source_text="Tom Stevenson 'Christie's World Encyclopedia of Champagne & Sparkling Wine' / CMS")

# ════════════════════════════════════════════════════════════════════════════════
# CHAMPAGNE PAIRINGS
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== CHAMPAGNE PAIRINGS ===")

PAIR(cur, "Oscietra caviar with blinis and crème fraîche", "amuse", "amuse",
     "classic", "complement",
     "The textbook luxury pairing for vintage or prestige Champagne: caviar's saline, iodine, and egg-richness is cut perfectly by Champagne's acidity and carbonation. The bubbles cleanse the palate of caviar's fat; the yeast autolysis character of aged Champagne mirrors the caviar's umami depth. Krug Grande Cuvée's richness and complexity is the reference for this pairing.",
     krug_gc)

PAIR(cur, "Butter-poached Breton lobster with Champagne beurre blanc", "fish_course", "fish_course",
     "classic", "complement",
     "Rich butter-poached lobster is cut by Salon's electric chalk-mineral acidity. The Champagne beurre blanc creates a self-referential mirror. The Le Mesnil terroir's chalk minerality amplifies the lobster's sweetness. Serve at the same temperature — 10°C for the Champagne, lobster warm from the poaching liquor.",
     salon_mesnil)

PAIR(cur, "Chicken roasted in Champagne with morel mushrooms", "main", "main",
     "established", "complement",
     "Dom Pérignon's creamy richness and toasted hazelnut character aligns with roasted chicken's Maillard crust and morel mushrooms' earthy umami. The Champagne itself in the roasting sauce creates a complete terroir alignment. A classic grand occasion pairing.",
     dom_perignon_p1)

PAIR(cur, "Warm oysters with mignonette foam and cucumber", "starter", "starter",
     "classic", "complement",
     "Egly-Ouriet's blank de noirs (old-vine Ambonnay Pinot Noir) with warm oysters — the warmth of the oyster amplifies its brine character, which is perfectly absorbed by the Champagne's rich yet mineral structure. The blank de noirs provides the rare experience of a red fruit-impression white wine meeting saline mineral food.",
     egly_bn)

PAIR(cur, "Potato chips / pommes gaufrettes with crème fraîche", "amuse", "aperitif",
     "established", "contrast",
     "The ultimate accessible Champagne pairing — the salt and fat of the chips is one of the most effective combinations with non-vintage Champagne. Bollinger Special Cuvée's red apple and brioche character meets the potato's neutral fat. The contrast of luxury (fine Champagne) and simplicity (potato chip) is the heart of relaxed fine dining.",
     bollinger_rg)

PAIR(cur, "Comte cheese 24 months with walnut bread", "cheese", "cheese",
     "established", "complement",
     "Aged Comté's crystalline texture, caramel-salt, and hazelnut notes mirror Pierre Péters' chalk mineral and hazelnut character precisely. A surprising but classically aligned cheese-Champagne pairing — the wine's acidity cuts through the cheese fat while the lactic character creates continuity.",
     peters_les_chetillons)

print("\n✅ Champagne batch complete.")
cur.close()
conn.close()
