#!/usr/bin/env python3
"""
PCT-1/PCT-8/PCT-13 — Portuguese Wine (Vinho Verde, Dão, Alentejo, Douro table)
+ Portuguese Spirits (Ginjinha, Licor Beirão, Medronho, Bagaço)
+ Goan Feni (PCT-8)
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

# Resume from last Madeira session handoff
session = BeverageSession(
    tradition="wine",
    region="Portugal — Vinho Verde",
    output_dir="./provenance_output/beverage",
    starting_entry=4,
    session_number=3,
    running_total=11
)

# ============================================================
# VINHO VERDE
# ============================================================

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "vinho verde alvarinho",
    "region": "Portugal — Minho / Monção e Melgaço",
    "name": "Alvarinho / Albariño — Vinho Verde (Monção e Melgaço)",
    "terroir_origin": (
        "Vinho Verde is the wine DOC covering Portugal's northwestern Minho region — the wettest, "
        "greenest part of Portugal, where Atlantic rainfall averages 1,500mm annually. The 'green wine' "
        "name refers not to colour but to the vine's fresh, youthful expression in this maritime climate. "
        "Within Vinho Verde, Monção e Melgaço is the prestige sub-appellation at the Spanish border "
        "(Galicia begins across the River Minho), where the Alvarinho grape — identical to Galicia's "
        "Albariño — reaches its maximum expression on granitic soils with lower rainfall than the "
        "coast. The Minho Valley's granite bedrock drains freely, preventing waterlogging, while the "
        "protection from Atlantic gales allows full Alvarinho ripening. Monção and Melgaço produce "
        "the most age-worthy, complex Vinho Verde — wines that can cellar 8–15 years and develop "
        "petrol/honey/dried citrus notes paralleling aged Riesling."
    ),
    "production_technique": (
        "Alvarinho is harvested in late September to early October — relatively late for the region. "
        "Whole-bunch pressing preserves the grape's characteristic stone-fruit aromatics. Cold-settled "
        "juice is fermented in stainless steel at 14–16°C to protect aromatic compounds. Low native "
        "sulphur dioxide at harvest allows limited natural fermentation. The key production distinction "
        "for premium Monção e Melgaço Alvarinho: extended lees contact (6–12+ months on fine lees) "
        "adds texture and complexity without losing the grape's citrus-saline precision. Some producers "
        "(Anselmo Mendes, Quinta de Santiago) use old oak or terracotta for partial fermentation to "
        "add further texture. Very light residual carbon dioxide (pétillance) is preserved in entry-"
        "level Vinho Verde through tank pressure; premium Alvarinho is typically still."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Rías Baixas Albariño (Galicia, Spain)",
         "connection": "The same grape variety across a political border — Alvarinho in Portugal, Albariño "
                       "in Spain. Rías Baixas Albariño is more widely known internationally; Monção e Melgaço "
                       "Alvarinho is frequently its equal or superior in structure and ageing potential. "
                       "Direct comparison demonstrates how PCT trail connections operate: the same "
                       "viticulture exists on both sides of the Minho River"},
        {"tradition": "wine", "beverage": "Mosel Riesling Spätlese (Germany)",
         "connection": "Both express maritime-influenced, high-acidity white wines with the ability to "
                       "develop striking complexity with age. Aged Alvarinho (8–12yr) develops petrol, "
                       "honey, and waxy complexity comparable to mature Mosel Riesling. Both challenge the "
                       "assumption that Atlantic white wines are exclusively for immediate consumption"}
    ],
    "sensory_profile": {
        "appearance": "Pale gold to light lemon; brilliantly clear; slight green highlights in youth. "
                      "Premium lees-contact examples show more golden hue; aged examples deepen to gold",
        "nose": "Young: lime zest, white peach, green apple, light saline/mineral, white blossom. "
                "Premium: added texture — stone fruit, lemon curd, light almond, ginger. "
                "Aged (6–10yr): petrol, honey, dried citrus, preserved lemon, wax — extraordinary transformation "
                "for what market perception assumes is a 'simple' fresh wine",
        "palate": "High natural acidity (pH 2.9–3.2 typical); mineral-saline character from granite soils; "
                  "medium body with lees-contact examples; crisp, precise finish; pétillance in entry-level "
                  "adds freshness without impeding fruit. Great Alvarinho: 45–60 second finish with mineral length",
        "conclusion": "The most underrated white wine in Portugal. Entry-level Vinho Verde is the world's "
                      "best aperitif value; Monção e Melgaço Alvarinho is the Douro Valley equivalent in "
                      "white wine terms — a serious, age-worthy, terroir expression."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Single Quinta Reserve Alvarinho", "criteria": "Single property sourcing, "
          "Monção e Melgaço sub-appellation, extended lees contact, 8+ months; ageable 8–15 years",
          "markers": "Anselmo Mendes 'Muros Antigos Reserva'; Quinta de Santiago; single quinta label; "
                     "Monção e Melgaço on label"},
        {"tier": 3, "tier_name": "Sub-appellation Alvarinho", "criteria": "Monção e Melgaço designation; "
          "estate or contracted grapes; stainless + lees contact; 6+ months",
          "markers": "Monção e Melgaço DOC on label; 'Alvarinho' prominence; premium restaurant pricing"},
        {"tier": 2, "tier_name": "Vinho Verde Alvarinho", "criteria": "Alvarinho-dominant (75%+ for varietal "
          "designation); Vinho Verde DOC; correct expression of the variety",
          "markers": "'Alvarinho' on label; Vinho Verde DOC; mid-range pricing"},
        {"tier": 1, "tier_name": "Vinho Verde (Blended)", "criteria": "Multi-variety blend (Alvarinho, Loureiro, "
          "Trajadura, Arinto); pétillant; entry-level; fresh and light",
          "markers": "'Vinho Verde' DOC without varietal; Casal Garcia, Gazela level; under $12"}
    ],
    "service_intelligence": {
        "temperature": "8–10°C (chilled); premium examples 10–12°C to allow aromatics to open",
        "vessel": "Standard white wine glass; premium examples benefit from a wider Burgundy-style glass",
        "technique": "Open and pour directly; no decanting needed for any Vinho Verde. By-the-glass: excellent "
                     "choice — holds 2–3 days under inert gas (Coravin compatible for premium bottles). "
                     "Entry-level Vinho Verde is the best value aperitif wine on any programme",
        "programme_position": "Aperitif; seafood course; shellfish pairing; summer patio programme anchor",
        "verbal_presentation": "Alvarinho from Monção e Melgaço — granite soils at the Spanish border, where "
                               "the Minho River separates Portugal from Galicia. The same grape, the same geology, "
                               "different countries. Nine months on fine lees. Try it with the oysters."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Anselmo Mendes (Muros Antigos Alvarinho and Reserva)",
        "producer_location": "Monção, Vinho Verde DOC, Portugal",
        "key_person": "Anselmo Mendes (winemaker, Alvarinho specialist)",
        "production_volume": "Medium-scale; Anselmo Mendes produces ~500,000 bottles annually across his range",
        "certifications": ["Vinho Verde DOC", "Monção e Melgaço sub-appellation"],
        "bc_distributor": "[NEEDS VERIFICATION — Skurnik is US-only; separate Canadian agent required]",
        "us_distributor": "Skurnik Wines & Spirits (Anselmo Mendes — confirmed national US importer; "
                          "note: Symington/Anselmo Mendes JV formed April 2024 may affect distribution going forward)",
        "uk_distributor": "Widely available; Liberty Wines, Jeroboams, Berry Bros.",
        "price_tier": "Market to Reserve (entry Vinho Verde ~$10–15; Alvarinho ~$18–28; Reserve ~$30–45)",
        "availability_notes": "Entry-level Vinho Verde (Casal Garcia, Gazela) widely available at BC Liquor. "
                              "Premium Alvarinho (Anselmo Mendes) through specialist wine merchants. "
                              "US: Folio Fine Wine Partners distributes some Vinho Verde producers."
    },
    "trail_connection": "PCT-1",
    "trail_note": "The Minho region's wine traditions predate Portuguese independence (1143). The Vinho Verde "
                  "DOC is one of Europe's largest wine regions (85,000+ hectares) and the cultural heartland "
                  "of Portuguese identity — the northwest was the original Portuguese kingdom. The PCT begins "
                  "here: the vines, the granite, the Atlantic rain, and the people who left for the empire "
                  "and left their wine culture everywhere they went.",
    "food_pairings": [
        {"technique_id": "", "dish": "Bacalhau à Brás (salt cod with eggs and potatoes)",
         "pairing_type": "complement",
         "rationale": "The canonical Minho pairing: high-acidity Alvarinho with salt cod's richness and "
                      "the egg's fat — the wine's saline mineral character amplifies the sea character of the dish"},
        {"technique_id": "", "dish": "Steamed clams (ameijoas à Bulhão Pato)",
         "pairing_type": "complement",
         "rationale": "Classic Minho shellfish pairing — the wine's saline-citrus profile echoes the "
                      "briny garlic-coriander broth of the ameijoas"}
    ],
    "source": "Vinho Verde Commission (CVRVV) official documentation; Anselmo Mendes winery notes; "
              "Oxford Companion to Wine — Vinho Verde; WSET materials",
})

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "dão touriga nacional",
    "region": "Portugal — Dão",
    "name": "Dão Touriga Nacional — Red",
    "terroir_origin": (
        "The Dão is an inland plateau in central Portugal, surrounded on three sides by mountain ranges "
        "(Serra da Estrela to the east, Serra do Caramulo to the west, Serra da Nave to the north). "
        "These mountains create a rain shadow that moderates the Atlantic influence — summers are warm "
        "and dry; winters are cold. The dominant geology is granite, giving the wines their characteristic "
        "mineral austerity. Touriga Nacional, Portugal's greatest red variety, reaches its most refined "
        "and Burgundy-like expression in the Dão — compared to the power and concentration it achieves "
        "in the Douro. The high-altitude Dão (400–700m) moderates Touriga's natural tendency toward "
        "excessive tannin extraction, producing wines of genuine elegance. Quinta dos Roques, Quinta "
        "das Maias, and Álvaro Castro are the prestige estates. Dão is sometimes called 'the Burgundy "
        "of Portugal' for its pinot-noir-like aromatic delicacy relative to the rest of Portugal's "
        "robust red wine landscape."
    ),
    "production_technique": (
        "Touriga Nacional is harvested in late September in the Dão. The granite soils drain freely "
        "and force low yields (20–35 hl/ha for quality estates) — key to the variety's aromatic "
        "concentration. Fermentation in stainless steel or cement (traditional Dão estates maintain "
        "old concrete lagares) at 26–28°C with limited cold soaking. Dão Touriga Nacional requires "
        "less extraction than Douro versions — shorter maceration (10–14 days vs 20+ in the Douro) "
        "to preserve the floral, red-fruit elegance that differentiates it from Port's raw material. "
        "Ageing typically 12–18 months in French oak (225L Bordeaux barriques), with the best estates "
        "using older barrels to avoid oak dominance over the variety's delicate aromatics. "
        "Quinta dos Roques ages in a combination of Portuguese and French oak."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Pinot Noir from Gevrey-Chambertin (Côte de Nuits, Burgundy)",
         "connection": "The 'Burgundy of Portugal' comparison is earned — Dão Touriga Nacional shares the "
                       "structural finesse, red-fruit aromatics, and granite-mineral character of Côte de Nuits "
                       "Pinot Noir. Both express a single dominant variety through cool-climate, high-altitude, "
                       "granite-influenced conditions. Both reward 5–15 years of ageing"},
        {"tradition": "wine", "beverage": "Ribera del Duero (Castile, Spain)",
         "connection": "Same grape variety across the border — Tinta Roriz (Portugal) is Tempranillo in Spain. "
                       "Both are premium Iberian reds on granite/limestone; Ribera del Duero is more extracted "
                       "and oak-influenced; Dão Touriga Nacional is more elegant and floral. Trail connection: "
                       "the 'Duero' and 'Douro' are the same river; the PCT follows its Portuguese course"}
    ],
    "sensory_profile": {
        "appearance": "Medium ruby to garnet; lighter than Douro equivalent; clear rim without colour staining",
        "nose": "Violet florals (the hallmark of Touriga Nacional), black cherry, blueberry, dark plum, "
                "light graphite, pencil shavings. With age (6–10yr): dried violets, leather, truffle, "
                "tobacco, cedar. The floral quality persists even in mature wines — Touriga Nacional's "
                "defining characteristic",
        "palate": "Medium to full body (lighter than Douro); fine tannins from granite soils and restrained "
                  "extraction; high natural acidity preserves freshness; long finish with violet-and-mineral "
                  "persistence. Balanced rather than powerful — the Dão style",
        "conclusion": "Portugal's most compelling argument for a serious red wine programme. Dão Touriga "
                      "Nacional at £25–40 competes with much more expensive Burgundy in the sommeliers' blind "
                      "tastings it regularly enters. Underpriced and under-known in North America."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Single Vineyard / Garrafeira Reserve", "criteria": "Specific vineyard designation, "
          "extended ageing (18–24+ months oak + 12+ months bottle), only in exceptional years",
          "markers": "Quinta dos Roques 'Encruzado' or Álvaro Castro 'Pelourinho'; single-vineyard label; £50+"},
        {"tier": 3, "tier_name": "Estate Reserve", "criteria": "Best lots from estate, 14–18 months French oak, "
          "consistent quality annual production",
          "markers": "'Reserva' designation; Quinta dos Roques standard red; £25–40"},
        {"tier": 2, "tier_name": "Estate Tinto", "criteria": "Estate production, Touriga Nacional dominant blend, "
          "12 months oak, correct Dão expression",
          "markers": "Estate label; £15–25; genuine granite minerality"},
        {"tier": 1, "tier_name": "Regional Dão Tinto", "criteria": "Sub-regional blend, multiple varieties, "
          "commercial production, correct but without the terroir expression of estate wines",
          "markers": "'Dão DOC' label; entry price; co-operative or négociant production"}
    ],
    "service_intelligence": {
        "temperature": "16–18°C",
        "vessel": "Burgundy glass (wider bowl than Bordeaux; the floral aromatics require room to open)",
        "technique": "Decant young examples (0–5yr) 45 minutes; mature (6–10yr) 20 minutes. "
                     "Dão Touriga Nacional's violet aromatics fade quickly in a decanter, so don't over-decant. "
                     "By-the-glass: holds 2–3 days Coravin; 1 day open",
        "programme_position": "Red wine by-glass; main course; cheese course alternative. "
                              "The best value 'serious red' on any Portuguese-focused wine list",
        "verbal_presentation": "Touriga Nacional from the Dão — granite plateau in central Portugal. The same "
                               "grape that makes Port wine here makes something entirely different: elegant, "
                               "floral, precise. Portugal's answer to Burgundy."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Quinta dos Roques (Dão)",
        "producer_location": "Cunha Baixa, Dão DOC, Portugal",
        "key_person": "Luís Lourenço (winemaker, Quinta dos Roques)",
        "production_volume": "Medium estate; ~250,000 bottles annually",
        "certifications": ["Dão DOC"],
        "bc_distributor": "[NEEDS VERIFICATION — Golden Ram is US-only; separate Canadian agent required]",
        "us_distributor": "Golden Ram Imports (Ramsey, NJ — confirmed national US importer for Quinta dos Roques)",
        "uk_distributor": "Liberty Wines (Quinta dos Roques UK); widely in specialist wine merchants",
        "price_tier": "Market to Reserve (BC ~$22–38; US ~$20–35)",
        "availability_notes": "BC: limited availability — specialist Portuguese wine merchants. "
                              "US: through Portuguese wine specialists and direct import. "
                              "UK: excellent availability through Liberty Wines and independent merchants."
    },
    "trail_connection": "PCT-1",
    "trail_note": "The Dão's granite highlands were the original training ground for Portugal's viticulture — "
                  "vines grown before the country's maritime expansion. The villages of the Serra da Estrela "
                  "produced the wine consumed by the soldiers and merchants who built the empire. "
                  "Touriga Nacional as a variety likely originated in the Dão before the Douro co-opted it "
                  "for Port production.",
    "food_pairings": [
        {"technique_id": "", "dish": "Roasted suckling pig (Leitão da Bairrada)",
         "pairing_type": "complement",
         "rationale": "The classic Dão-adjacent pairing: roasted pork from neighboring Bairrada region with "
                      "Dão's structured Touriga Nacional. The wine's tannin and acidity cut through pork fat"},
        {"technique_id": "", "dish": "Duck rice (arroz de pato)",
         "pairing_type": "bridge",
         "rationale": "Rich duck and rice absorbs the wine's tannin structure; the violet floral quality of "
                      "Touriga Nacional bridges with the duck's gamey character"}
    ],
    "source": "Dão Wine Commission official documentation; Quinta dos Roques winery notes; "
              "Oxford Companion to Wine — Dão; Jancis Robinson profiles; Decanter Portugal special issues",
})

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "alentejo red",
    "region": "Portugal — Alentejo",
    "name": "Alentejo — Herdade do Esporão and the Cork Country Reds",
    "terroir_origin": (
        "The Alentejo covers roughly one-third of Portugal's landmass — the warm, flat plains south of "
        "Lisbon stretching to the Spanish border and the Algarve. This is cork country: 34% of the world's "
        "cork oak forests grow in the Alentejo, making it the economic engine of the region before wine "
        "became its primary export product. The 'Alentejano' vineyard sits on schist (in the far south) "
        "and granite (near Évora) at 200–600m altitude. The climate is hot and dry — temperatures reach "
        "40°C+ in summer — with minimal Atlantic influence. Alentejano reds are structured and concentrated "
        "without Port wine's fortification. The principal red varieties: Aragonez (Tempranillo), Alicante "
        "Bouschet (rare variety with red pulp, unusual among wine grapes), Trincadeira, and Touriga Nacional "
        "as blending component. The Herdade do Esporão estate (2,000+ hectares, mixed farming, certified "
        "organic sections) is the benchmark and the Alentejo's most exported estate brand."
    ),
    "production_technique": (
        "Alentejo reds require heat management unavailable in the maritime north. Harvesting occurs in "
        "early September (earlier than Dão or Vinho Verde) before extreme heat degrades aroma compounds. "
        "Nocturnal harvesting is standard on quality estates — overnight temperatures drop to 18–22°C, "
        "compared to the 38–40°C of the day. Cold-chain transportation from vineyard to winery. "
        "Fermentation in temperature-controlled stainless steel or concrete tanks at 22–24°C to preserve "
        "fruit. Esporão's winemaker David Baverstock (Australian, permanent resident of the Alentejo since "
        "1992) pioneered the international winemaking standards that made Alentejo an export-quality region. "
        "Ageing typically in a combination of French and American oak — American oak's vanilla-coconut "
        "character integrates with the warm-climate fruit without overwhelm. Organic and biodynamic "
        "production increasing: Esporão's organic range is certified since 2012."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Priorat (Catalonia, Spain)",
         "connection": "Both are southern Iberian warm-climate reds with exceptional concentration from "
                       "stressed vines on schist soils. Priorat's garnacha-carignan blends and Alentejo's "
                       "Aragonez-Alicante Bouschet blends share structural power, dark fruit concentration, "
                       "and mineral depth. Both are priced below comparable French and Italian equivalents"},
        {"tradition": "wine", "beverage": "McLaren Vale Shiraz (South Australia)",
         "connection": "Both grow in warm continental climates producing full-bodied, fruit-forward reds "
                       "with moderate tannin and accessible structure. Both are commercial successes at the "
                       "mid-premium segment and both punch above their price-point vs. France/Italy. "
                       "The Australian connection is direct: David Baverstock brought McLaren Vale technique "
                       "to the Alentejo at Esporão"}
    ],
    "sensory_profile": {
        "appearance": "Deep ruby to dark garnet; full opacity; significant colour depth from Alicante Bouschet "
                      "(one of very few grapes with red-tinted flesh, contributing unusual colour intensity)",
        "nose": "Dark plum, blackberry, damson, black cherry, dark chocolate, cedar, coffee, warm earth. "
                "Alicante Bouschet adds iron-mineral depth unusual in other varieties. "
                "American oak: coconut, vanilla notes in commercially-positioned wines; "
                "French oak: more restrained cedar-spice in premium expressions",
        "palate": "Full body; moderate tannin (less than Douro); rich fruit concentration; "
                  "medium-high alcohol (13.5–14.5% ABV); warm, long finish; readily drinkable young "
                  "but rewards 3–8 years bottle ageing. The Alentejo style is riper and more generous "
                  "than the Dão's austerity",
        "conclusion": "The Alentejo's accessible luxury: consistently good value at the £15–35 segment. "
                      "Esporão Private Selection is one of the best-value serious reds on any programme."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Single Vineyard / Garrafeira Reserve", "criteria": "Specific parcel selection, "
          "18–24+ months French oak, only in exceptional vintages; Esporão 'Defesa' or 'Reserva' level",
          "markers": "Esporão 'Private Selection Reserva'; Herdade do Mouchão; single vineyard label; £40–80+"},
        {"tier": 3, "tier_name": "Estate Reserva", "criteria": "Selected lots, 14–18 months oak, consistent "
          "estate production; the benchmark restaurant quality level",
          "markers": "'Reserva' designation; Esporão Reserva; £20–35; solid restaurant glass choice"},
        {"tier": 2, "tier_name": "Estate Alentejano", "criteria": "Standard estate production; correct Alentejo "
          "character; accessible pricing; 12 months oak",
          "markers": "Estate label; Esporão Private Selection; £12–20; widely available"},
        {"tier": 1, "tier_name": "Regional Alentejano", "criteria": "Multi-estate blend; co-operative or "
          "négociant; correct but without estate character",
          "markers": "'Alentejano' DOC or 'Alentejo' only; entry pricing; supermarket distribution"}
    ],
    "service_intelligence": {
        "temperature": "16–18°C",
        "vessel": "Bordeaux glass (suits the wine's fuller body better than Burgundy)",
        "technique": "Open and allow 30 minutes air for younger wines. Young Reserva: decant 1 hour. "
                     "By-the-glass: holds well, 3 days under inert gas. "
                     "Excellent house red choice for modern European restaurants",
        "programme_position": "House red; main course red wine; cheese alternative to heavier French reds. "
                              "Excellent value flagship for a Portuguese wine section",
        "verbal_presentation": "Alentejo red from Herdade do Esporão — 2,000 hectares of organic estate in "
                               "Portugal's cork country, south of Lisbon. Aragonez and Alicante Bouschet, "
                               "harvested at night before the Alentejo heat concentrates the grapes."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Herdade do Esporão",
        "producer_location": "Reguengos de Monsaraz, Alentejo, Portugal",
        "key_person": "David Baverstock (chief winemaker since 1992); João Roquette (CEO)",
        "production_volume": "~3 million bottles annually; one of Portugal's largest single-estate producers",
        "certifications": ["Alentejo DOC", "Organic (partial estate, certified 2012)"],
        "bc_distributor": "[NEEDS VERIFICATION — Cultivamos is US-only; contact Esporão export directly for BC agent]",
        "us_distributor": "Cultivamos Inc. (confirmed October 2024 — new US importer for entire Esporão Group portfolio, replacing previous arrangement)",
        "uk_distributor": "Esporão widely available through Waitrose, Majestic, specialist merchants",
        "price_tier": "Market (Private Selection ~$16–20 BC; Reserva ~$22–30)",
        "availability_notes": "Esporão Private Selection: one of the most widely available Portuguese wines "
                              "in Canada and the US. BC Liquor stocks it regularly. US national distribution "
                              "through Vinho Imports — verify current arrangement."
    },
    "trail_connection": "PCT-1",
    "trail_note": "The Alentejo's cork oak forests were a Portuguese colonial resource — cork was harvested "
                  "and shipped throughout the empire for bottle stoppers, insulation, and floatation. "
                  "The Alentejo's cork trade preceded its wine export reputation and represents a PCT "
                  "industrial resource trail parallel to the wine cultural trail.",
    "food_pairings": [
        {"technique_id": "", "dish": "Black pork (porco preto alentejano) with clams (carne de porco à alentejana)",
         "pairing_type": "complement",
         "rationale": "The regional pairing: Alentejo's acorn-fed black pork with Alentejo wine. "
                      "The pork's richness and the clams' brine create a dish that requires the wine's "
                      "tannin and warm fruit to resolve"},
        {"technique_id": "", "dish": "Slow-roasted lamb shoulder with coriander and cumin",
         "pairing_type": "complement",
         "rationale": "The Alentejo's Arab-influenced cuisine (coriander, cumin, lamb) pairs with "
                      "the wine's warm spice notes from American oak ageing"}
    ],
    "source": "Herdade do Esporão official documentation; Alentejo Wine Commission; "
              "Oxford Companion to Wine — Alentejo; Decanter Portugal special issue",
})

session.commit_batch()
print(f"\n[BATCH 10 COMMITTED — Portuguese Wine Alvarinho + Dão + Alentejo]\n")

# ============================================================
# SWITCH TO PCT-1 SPIRITS — Ginjinha, Licor Beirão, etc.
# ============================================================

session.switch_region("spirits", "Portugal — Lisbon / Ginjinha and Portuguese Liqueurs")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "ginjinha cherry liqueur",
    "region": "Portugal — Lisbon / Óbidos",
    "name": "Ginjinha (Ginja)",
    "terroir_origin": (
        "Ginjinha is a Portuguese sour cherry liqueur with deep cultural roots in Lisbon's Rossio neighbourhood "
        "and the medieval town of Óbidos. The ginja sour cherry (Prunus cerasus — related to morello and "
        "amarena cherries) is grown across central Portugal, particularly in the highlands of Óbidos, "
        "Alcobaça, and the Serra da Lousã. The cherry's natural tartness and almond-like stone character "
        "define the liqueur's flavour profile. The ritual of ginjinha in Lisbon is as much cultural as "
        "culinary: the tiny bar 'A Ginjinha' on Largo de São Domingos (opened 1840 by Espinheiro) serves "
        "nothing but ginjinha in shot glasses for €1.50, either 'com ela' (with the pickled cherry inside) "
        "or 'sem ela' (without). The queue at this bar is one of Lisbon's great daily rituals."
    ),
    "production_technique": (
        "Ginjinha is produced by macerating sour cherries in aguardente (Portuguese grape spirit, "
        "typically 35–40% ABV neutral) with sugar and spices — most commonly a cinnamon stick, "
        "occasionally cloves or vanilla. The maceration lasts several weeks to months, extracting the "
        "cherry's colour, acid, and almond-kernel oils from the stones. The resulting liquid is sweetened "
        "with sugar syrup to the producer's style (typically 50–200 g/L residual sugar). The final "
        "ABV ranges 20–25%. Most ginjinha is not aged after maceration — it is bottled fresh with "
        "cherries included or strained out depending on the house style. Óbidos ginja has its own "
        "regional character, served in chocolate cups (the cup melts with the liqueur, consumed together). "
        "Commercial production: Ginjinha Espinheiro, Beirão, and Super Bock's Ginjinha are the major brands. "
        "The liqueur has been DOP protected in Óbidos since 2016."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Amaretto (Italy)",
         "connection": "Both are stone-fruit liqueurs derived from cherries/almonds sharing the benzaldehyde "
                       "aromatic compound that creates the almond-marzipan character; both are sweet, low-"
                       "alcohol digestifs; the Italian amaretto uses apricot/almond kernels while ginjinha "
                       "uses the cherry stone for the same compound. Both serve in small portions post-meal"},
        {"tradition": "spirits", "beverage": "Maraschino (Luxardo, Dalmatia/Italy)",
         "connection": "Both are sour cherry liqueurs (Marasca cherry for Luxardo; ginja for Portuguese style); "
                       "Maraschino is drier, more complex, and higher ABV (32%); ginjinha is sweeter, simpler, "
                       "and primarily a Portuguese domestic/cultural product. Both are produced by "
                       "cherry maceration in neutral spirit"}
    ],
    "sensory_profile": {
        "appearance": "Deep ruby-red to dark crimson; viscous; the pickled cherry in the glass adds visual drama",
        "nose": "Sour cherry, wild cherry jam, almonds, cinnamon, light vanilla; "
                "sweet rather than complex; intensely fruity; the almond-from-cherry-stones is distinctive",
        "palate": "Sweet (50–200 g/L sugar); full cherry fruit; low-moderate bitterness from cherry stones; "
                  "warm spirit backbone (20–25% ABV); medium-short finish with cherry-almond persistence. "
                  "The cherry inside adds texture and concentrated fruit to the final moments",
        "conclusion": "Ginjinha is not a complex spirit — it is a cultural object. The pleasure is the ritual: "
                      "the tiny bar, the 1.50€ shot, the choice of cherry or no cherry. On a cocktail programme, "
                      "it functions as a cherry liqueur with genuine Portuguese provenance story."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Artisanal Single-Source", "criteria": "Named ginja cherry variety and origin; "
          "longer maceration; minimal added sugar; small production",
          "markers": "Producers in Óbidos using DOP cherries; artisanal labels; limited distribution"},
        {"tier": 3, "tier_name": "Traditional House", "criteria": "Established producer with consistent recipe; "
          "'com ela' (with cherry); correct bittersweet balance",
          "markers": "Ginjinha Espinheiro; A Ginjinha bar recipe; historic Lisbon recipes"},
        {"tier": 2, "tier_name": "Commercial Standard", "criteria": "Major brand production; consistent but "
          "standardised sweetness; widespread distribution",
          "markers": "Ginja Sem Rival; commercial labels; bar and cocktail use"},
        {"tier": 1, "tier_name": "Industrial Production", "criteria": "Mass market; artificial cherry flavouring "
          "possible; no stone maceration; simplest expression",
          "markers": "Lowest price tier; supermarket own-brand; not genuine ginja culture"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature (18–20°C) for traditional Portuguese service; or slightly chilled (12°C) "
                       "for cocktail use",
        "vessel": "Traditional: tiny shot glass (30–40mL) or chocolate cup (Óbidos style). Cocktail: "
                  "coupe or Nick and Nora glass",
        "technique": "Traditional Portuguese service: pour 30mL into shot glass; add or omit the cherry. "
                     "Cocktail use: ginjinha as cherry modifier in sours (Ginja Sour: ginjinha + lemon + egg white); "
                     "or as topping for champagne. Chocolate cup service: pour ginjinha into small chocolate cup — "
                     "guest eats cup after drinking",
        "programme_position": "Post-dinner digestif; cocktail ingredient; cultural moment on a Portuguese menu. "
                              "The educational pause for a sommelier to explain Rossio Square and A Ginjinha bar",
        "verbal_presentation": "Ginjinha — the sour cherry liqueur of Lisbon's oldest neighbourhood. Since 1840, "
                               "served from a tiny bar that sells nothing else. Sour ginja cherries, grape spirit, "
                               "cinnamon. Drink it the Lisbon way: standing up, one shot, cherry inside."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Ginjinha Espinheiro (the original Rossio bar recipe)",
        "producer_location": "Largo de São Domingos, Lisbon (A Ginjinha bar); production in Alcobaça/Óbidos region",
        "key_person": "The Espinheiro family (descendants of founder Francisco Espinheiro, 1840)",
        "production_volume": "Small; primarily sold at the Rossio bar; commercial versions by larger producers",
        "certifications": ["Ginja de Óbidos DOP (2016)"],
        "bc_distributor": "[NEEDS VERIFICATION — Portuguese spirits rarely distributed in BC; check BCLDB special imports]",
        "us_distributor": "[NEEDS VERIFICATION — limited US distribution; check Portuguese wine importers for spirits portfolios]",
        "uk_distributor": "Widely available in specialist Portuguese delis and wine merchants; also sold at "
                          "duty-free and airport shops from Portugal",
        "price_tier": "Market (€1.50 at A Ginjinha; €8–15 per bottle commercial)",
        "availability_notes": "BC: very limited — specialty Portuguese/European delis or BCLDB special import. "
                              "US: better availability through Portuguese wine/spirits importers; some online. "
                              "For programme use: the cultural story is the selling point — any commercial ginjinha works."
    },
    "trail_connection": "PCT-1",
    "trail_note": "Ginjinha is one of the great unexported Portuguese cultural products — almost unknown outside "
                  "Portugal except in Portuguese diaspora communities in Newark, Toronto, and parts of Brazil. "
                  "The PCT trail note: the ginja cherry tree spread along Portuguese colonial routes to Brazil "
                  "and Africa where the fruit is used in local distillation traditions. The Rossio bar is "
                  "essentially unchanged since 1840 — a PCT terminus in the physical heart of Lisbon.",
    "food_pairings": [
        {"technique_id": "", "dish": "Dark chocolate truffle (70% cacao)", "pairing_type": "complement",
         "rationale": "The almond-cherry of ginjinha echoes dark chocolate's own cherry-almond terroir notes "
                      "(the same benzaldehyde compound appears in both cherry and high-cacao chocolate)"},
        {"technique_id": "", "dish": "Pastel de nata (Portuguese custard tart)", "pairing_type": "bridge",
         "rationale": "The custard's eggy richness and the pastry's flaky caramel meet ginjinha's cherry "
                      "sweetness in a classically Portuguese dessert pairing"}
    ],
    "source": "A Ginjinha bar history (Espinheiro family); Ginja de Óbidos DOP documentation; "
              "Portuguese food writer Edite Vieira writings on Lisbon drinks culture",
})

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "medronho arbutus spirit",
    "region": "Portugal — Algarve / Serra de Monchique",
    "name": "Medronho (Arbutus Berry Spirit)",
    "terroir_origin": (
        "Medronho is a Portuguese aguardente (brandy/eau-de-vie) distilled from the fruit of the arbutus "
        "tree (Arbutus unedo — the strawberry tree), a wild Mediterranean shrub that grows throughout "
        "southern Portugal, particularly in the Serra de Monchique in the Algarve and parts of the "
        "Alentejo and Trás-os-Montes. The arbutus berry (medronho) ripens to red-orange in October–"
        "November and contains 15–20% sugar — sufficient for natural fermentation. The fruit has a "
        "sandy, slightly astringent texture with strawberry-like flavour when fully ripe. Medronho is "
        "one of Portugal's most traditional distilled spirits — produced artisanally in small copper "
        "pot stills (alambiques) by farmers for domestic use for centuries, though commercial production "
        "remains limited."
    ),
    "production_technique": (
        "Arbutus berries are harvested by hand in October–November when fully red-ripe. Fermentation "
        "occurs in open clay pots or stone tanks — the fruit's natural wild yeasts ferment the pulp "
        "for 3–6 weeks to produce a 6–8% ABV wash. Single distillation in small copper pot stills "
        "produces medronho at 40–55% ABV. Premium medronho undergoes double distillation for greater "
        "aromatic refinement. Unlike most European fruit spirits, medronho is rarely aged in wood — "
        "it is typically presented unaged or with brief rest in stainless steel, preserving the "
        "arbutus berry's wild, floral character. The arbutus tree is not cultivated for commercial "
        "production — all medronho comes from wild-harvested fruit, severely limiting production volume. "
        "Lagoa in the Algarve is the centre of the industry's small commercial sector."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Eau-de-Vie de Framboise (Alsace/Switzerland)",
         "connection": "Both are unaged fruit eaux-de-vie distilled from wild or semi-wild berries; both "
                       "express the raw essence of the fruit without wood transformation; both are produced "
                       "in small pot stills at artisanal scale; both are regional specialities rarely exported"},
        {"tradition": "spirits", "beverage": "Pisco (Peru/Chile)",
         "connection": "Both are grape-free spirit categories from their respective national traditions; "
                       "both are unaged (or minimally aged); both face the challenge of export market "
                       "awareness. The PCT connection: pisco's grapevine was brought by Spanish colonists "
                       "(who learned viticulture from Portuguese Moors); medronho represents the pre-wine "
                       "Portuguese distillation tradition that preceded the aguardente grape spirit"}
    ],
    "sensory_profile": {
        "appearance": "Crystal clear; colourless; full transparency",
        "nose": "Wild strawberry, arbutus berry (distinctive sandy-sweet fruit), light floral notes, "
                "honey, mild wildness; uniquely Portuguese — nothing else smells quite like this "
                "in the spirits world",
        "palate": "Clean, direct fruit hit; medium body; warming alcohol (40–55% ABV); "
                  "slightly astringent tannic finish from arbutus skin contact; "
                  "short-to-medium length; fresh and pure",
        "conclusion": "Medronho is a spirits education piece rather than a commercial staple. Its scarcity, "
                      "artisanal production, and uniquely Portuguese character make it a culturally "
                      "irreplaceable item on any serious spirits programme covering Iberia."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Double-Distilled Artisanal", "criteria": "Wild-harvested fruit; "
          "double distillation; named producer; Monchique origin",
          "markers": "Hand-labeled bottles; farm name; Serra de Monchique; limited release"},
        {"tier": 3, "tier_name": "Single-Distilled Premium", "criteria": "Wild-harvested; single distillation; "
          "consistent commercial quality; Algarve DOP if applicable",
          "markers": "Commercial artisanal bottle; Lagoa or Monchique origin"},
        {"tier": 2, "tier_name": "Standard Commercial", "criteria": "Commercially produced; consistent; correct arbutus character",
          "markers": "National distribution in Portugal; tourist retail"},
        {"tier": 1, "tier_name": "Industrial / Blended", "criteria": "Blended with neutral spirit; reduced arbutus "
          "character; filler production",
          "markers": "Lowest price; tourist souvenir market; possibly with added colouring"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature (18–20°C) or very lightly chilled (14°C) to preserve arbutus aromatics",
        "vessel": "Grappa glass or small tulip glass (30–45mL pour)",
        "technique": "Serve neat post-dinner as a digestif. Cocktail use: medronho as the base spirit in "
                     "a Sour (medronho + citrus + sugar) or as an exotic modification in Iberian cocktail programmes",
        "programme_position": "Post-dinner digestif; spirits education piece; bar programme curiosity item "
                              "for a Portuguese or Iberian-themed programme",
        "verbal_presentation": "Medronho — from the arbutus trees of the Serra de Monchique in the Algarve. "
                               "Wild strawberry trees, harvested by hand, distilled in copper pot stills. "
                               "This has been made in the hills above the sea since before Portugal existed "
                               "as a country."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Quinta dos Poços (Lagoa, Algarve) and artisanal Monchique producers",
        "producer_location": "Serra de Monchique, Faro district, Algarve, Portugal",
        "key_person": "[NEEDS VERIFICATION — no single nationally prominent producer]",
        "production_volume": "Very small total production; wild harvest limits volume",
        "certifications": ["Aguardente de Medronho do Algarve — IGP protected"],
        "bc_distributor": "[NEEDS VERIFICATION — essentially unavailable commercially in BC]",
        "us_distributor": "[NEEDS VERIFICATION — extremely limited US availability; Portuguese food importers occasionally stock]",
        "uk_distributor": "[NEEDS VERIFICATION — Portugal-specialist wine merchants occasionally stock medronho]",
        "price_tier": "Reserve (€15–35 in Portugal; if available internationally, £30–60 premium for scarcity)",
        "availability_notes": "Essentially unavailable commercially in BC and US. For a professional programme: "
                              "source through direct import from Portugal, a Portuguese food importer, or "
                              "personal procurement on travel to the Algarve. "
                              "The cultural story justifies the effort on a serious Iberian programme."
    },
    "trail_connection": "PCT-1",
    "trail_note": "Medronho represents the pre-colonial layer of Portuguese distillation — the tradition that "
                  "existed before the grape-spirit (aguardente vinica) that defines Port production. "
                  "The arbutus tree grows wild along the entire Portuguese coast and was carried to "
                  "the Azores and Madeira by early Portuguese settlers. It is the original Portuguese spirit.",
    "food_pairings": [
        {"technique_id": "", "dish": "Presunto (Portuguese dry-cured ham) with fresh figs",
         "pairing_type": "bridge",
         "rationale": "The wild-fruit character of medronho bridges with fig sweetness; ham's salt "
                      "amplifies the spirit's clean finish"},
        {"technique_id": "", "dish": "Aged sheep's milk cheese (queijo de Évora)",
         "pairing_type": "complement",
         "rationale": "The cheese's lanolin-funk and the spirit's wild-fruit purity create a "
                      "traditional Algarve countryside pairing"}
    ],
    "source": "Aguardente de Medronho do Algarve IGP dossier; Portuguese Spirits Association documentation; "
              "Jancis Robinson Oxford Companion to Wine — Portugal spirits entry",
})

session.commit_batch()
print(f"\n[BATCH 11 COMMITTED — Ginjinha + Medronho]\n")

# ============================================================
# SWITCH TO PCT-8 — Goa Feni
# ============================================================

session.switch_region("spirits", "India — Goa (Feni)")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "cashew feni",
    "region": "India — Goa",
    "name": "Cashew Feni — Single and Double Distilled",
    "terroir_origin": (
        "Feni is a spirit unique to the Indian state of Goa — one of only two products from Goa with "
        "Geographical Indication (GI) status (the other being Goa cashew). The cashew apple (the "
        "swollen stalk of the cashew nut, Anacardium occidentale) is the primary fermentation base for "
        "cashew feni. Goa's cashew cultivation is a direct product of Portuguese colonialism: the cashew "
        "tree is native to northeastern Brazil and was brought to Goa by Portuguese merchants in the "
        "16th century as a ground-cover crop to prevent soil erosion on Goa's laterite hillsides. "
        "Over 400 years, the cashew became inseparable from Goan identity — the cashew apple season "
        "(March–May) is a cultural event in Goan villages, with the urrak (first distillation) flowing "
        "freely. The PCT node: Goa was a Portuguese colony from 1510 to 1961 (the last European colony "
        "in India, taken by India by military action). Feni is the PCT's most vivid example of "
        "how Portuguese agricultural transfers transformed the food and drink culture of their territories."
    ),
    "production_technique": (
        "Cashew feni production: ripe cashew apples are collected from the ground (never picked — "
        "the fruit must fall naturally at full ripeness). The apples are foot-trodden in stone troughs "
        "(a technique that parallels Port wine's lagar treading) to extract juice. The juice ferments "
        "naturally with indigenous wild yeasts for 2–3 days to produce a 5–8% ABV wash (the "
        "neero/niro — unfermented, it is a prized fresh juice). Single distillation produces "
        "urrak at 15–20% ABV — the seasonal first-run spirit consumed locally. Double distillation in "
        "traditional terracotta cazani (clay pot stills) — the traditional Goan still — produces "
        "cashew feni at 40–45% ABV. The cazani is a critical PCT artifact: a direct continuation of "
        "Portuguese copper alembic distillation technology adapted to local materials. Triple-distilled "
        "cashew feni (rare) reaches 55%+ ABV. Modern producers (Cazulo, Bhati Village) have introduced "
        "stainless steel pot stills and hygienic fermentation to standardise quality for export markets. "
        "GI protection (2009) restricts Feni production exclusively to Goa."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Cachaça (Brazil)",
         "connection": "The most direct PCT parallel: both Feni and Cachaça were created when Portuguese "
                       "agricultural transfers (cashew to Goa; sugarcane to Brazil) were fermented and "
                       "distilled using adapted Portuguese distillation techniques. Both are GI-protected "
                       "spirits unique to a single former Portuguese territory. Both face export challenges "
                       "due to unfamiliar flavour profiles in Western markets"},
        {"tradition": "spirits", "beverage": "Armagnac (Gascony, France)",
         "connection": "Both are copper-pot-distilled fruit spirits with strong terroir identity; "
                       "both are produced in geographically protected regions by small artisanal producers; "
                       "both face market pressure from industrial spirits. Armagnac uses column still "
                       "variation; Feni uses traditional cazani; both preserve the original pot-still "
                       "distillation character that column spirits lack"}
    ],
    "sensory_profile": {
        "appearance": "Urrak: clear, pale yellow; cashew feni: crystal clear to very pale golden. "
                      "Aged cashew feni: light amber from brief wood contact",
        "nose": "Unmistakably distinctive — tropical fruit (cashew apple has no Western parallel), "
                "slight acetone note (a Feni signature, reduces with premium production), "
                "wild fruit ferment character, coconut, light floral notes. Cazulo premium: "
                "refined, tropical citrus, cashew fruit candy, clean spirit backbone",
        "palate": "Urrak: light, sweet-sour, fresh; easy at 15–20% ABV. "
                  "Double-distilled Feni: full spirit weight (40–45%), pungent raw character in "
                  "standard production; refined in premium expressions with fruit-tropical-clean finish. "
                  "Acetone note distinguishes traditional from premium production. "
                  "With water or ice: opens dramatically",
        "conclusion": "Cashew Feni is the PCT's most challenging spirit for Western palates — and the most "
                      "educationally important. The acetone controversy is a production quality issue: "
                      "premium producers (Cazulo) have eliminated it. On a serious cocktail programme, "
                      "premium Feni serves as a tropical base spirit with no Western equivalent."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Aged Premium Single-Origin", "criteria": "Named cashew orchard; "
          "hygienic modern fermentation; stainless or clay still distillation; brief wood rest; "
          "reduced acetone; export quality",
          "markers": "Cazulo Premium Feni; wood-aged expressions; collector's packaging; international distribution"},
        {"tier": 3, "tier_name": "Double-Distilled Premium", "criteria": "Traditional cazani distillation; "
          "selected cashew apples; cleaner fermentation; reduced acetone",
          "markers": "Certified GI production; quality label; local Goan specialist market + export"},
        {"tier": 2, "tier_name": "Standard Cashew Feni", "criteria": "Traditional production; correct "
          "cashew feni character; some acetone typical; genuinely double-distilled",
          "markers": "Local Goan production; traditional bottle; the authentic experience"},
        {"tier": 1, "tier_name": "Urrak", "criteria": "Single-distilled; seasonal; 15–20% ABV; "
          "consumed fresh in Goa during cashew season; not for export",
          "markers": "Seasonal product March–May; local bars and homes only"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature (18–22°C) for neat; with ice or water for cocktail use",
        "vessel": "Shot glass for traditional service; coupe or rocks glass for cocktail",
        "technique": "Traditional Goan service: neat, room temperature, with a plate of sausages "
                     "(Goan pork chouriço — also a PCT artifact). Cocktail use: Feni Sour "
                     "(cashew feni + lime + palm sugar + soda); Feni-based fruit punch. "
                     "With coconut water: the Goan summer drink",
        "programme_position": "Specialty spirits education; cocktail innovation; Indian-focused or "
                              "Southeast Asian tasting menu pairing. A genuine conversation piece on "
                              "any programme discussing post-colonial terroir",
        "verbal_presentation": "Cashew Feni from Goa — the only spirit in the world made from cashew apples. "
                               "The cashew tree came to India on Portuguese ships from Brazil in the 1500s. "
                               "Five centuries later: this. GI-protected. Made only in Goa. "
                               "Foot-trodden, clay-pot distilled."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Cazulo Premium Feni (Nadia Coutinho, Goa)",
        "producer_location": "Cansaulim village, Goa, India",
        "key_person": "Nadia Coutinho (founder, Cazulo); Hansel Vaz (Goa Cashew Feni advocacy)",
        "production_volume": "Very limited; Cazulo produces ~5,000 bottles annually in export format",
        "certifications": ["GI — Feni (Goa only, since 2009)"],
        "bc_distributor": "[NEEDS VERIFICATION — Feni has essentially no BC commercial distribution]",
        "us_distributor": "[NEEDS VERIFICATION — Cazulo has limited US presence; check specialty Indian spirits importers]",
        "uk_distributor": "Cazulo available through UK specialists; some Indian food importers stock generic Feni",
        "price_tier": "Reserve to Estate (€25–50 in Goa for premium; £50–80 if available in UK; "
                      "extremely limited North American pricing)",
        "availability_notes": "BC: essentially unavailable through normal channels. US: Cazulo has been "
                              "attempting US market entry; check specialty South Asian grocery importers "
                              "or Indian restaurant supply companies. For a professional programme: "
                              "procure via direct import from Goa or UK specialist."
    },
    "trail_connection": "PCT-8",
    "trail_note": "Feni IS the PCT node in Goa — the distillation of 500 years of Portuguese presence compressed "
                  "into one bottle. The cashew tree (Brazil), the cazani still (adapted from Portuguese alembic), "
                  "and the Goan Catholic culture that produces and consumes Feni are all direct PCT artifacts. "
                  "Without the Portuguese, there would be no cashew in Goa; without the cashew, no Feni. "
                  "The 1961 Indian annexation of Goa ended the colonial period but Feni survives as the "
                  "most durable PCT food-production legacy in Asia.",
    "food_pairings": [
        {"technique_id": "", "dish": "Goan pork vindaloo", "pairing_type": "complement",
         "rationale": "Vindaloo (itself a PCT artifact: vinho d'alhos = Portuguese wine-garlic marinade) "
                      "with Feni is the classic pairing. The spirit's intensity matches the dish's heat; "
                      "its tropical fruit note balances the vinegar-chilli base"},
        {"technique_id": "", "dish": "Prawn recheado (Goan stuffed prawns)", "pairing_type": "bridge",
         "rationale": "Goan spiced prawns and cashew Feni share the same tropical-terroir register; "
                      "the masala's complexity is navigated by the spirit's clean fruit base"}
    ],
    "source": "GI registration documents for Feni (Government of Goa, 2009); Cazulo official documentation; "
              "Hansel Vaz advocacy materials for Goa Feni; The Hindu / Times of India Feni cultural coverage; "
              "Frederick Noronha food writing on Goa",
})

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "coconut feni",
    "region": "India — Goa",
    "name": "Coconut Feni (Coconut Toddy Spirit)",
    "terroir_origin": (
        "Coconut feni is produced from the fermented sap (toddy) of the coconut palm (Cocos nucifera) — "
        "collected from the immature flower spadix at the crown of the palm tree. Toddy collection "
        "in Goa is an ancient pre-Portuguese practice (the toddy tapper or rendi is among Goa's oldest "
        "professional traditions), but coconut feni as a distilled product developed during the "
        "Portuguese colonial period when distillation knowledge arrived from Europe. "
        "Coconut palms grow throughout coastal Goa, and the toddy tradition extends across Kerala, "
        "Karnataka, and coastal South Asia — but the distilled feni is unique to Goa. "
        "The coastal laterite soils and tropical monsoon climate of Goa's coastal belt define the "
        "coconut palm's productivity and the toddy's fermentation character."
    ),
    "production_technique": (
        "Toddy collection: the rendi (toddy tapper) climbs the coconut palm daily (at sunrise and "
        "sunset), cuts the flower spadix, and collects the sap that runs overnight into clay or "
        "modern plastic pots tied to the palm crown. Fresh sap (neera) is sweet and mildly alcoholic "
        "(2–4% ABV from ambient yeast fermentation); older sap (toddy) has fermented to 5–7% ABV. "
        "Fermentation lasts 24–36 hours in clay pots. Distillation in the traditional cazani "
        "(identical to cashew Feni production) produces coconut feni at 40–45% ABV. "
        "The two-still system: the daijem (first distillation) and moddso/cazulo (second distillation). "
        "Coconut feni is lighter and more delicate than cashew feni — the coconut sap produces fewer "
        "congeners than the cashew apple. Production volume is smaller than cashew feni as toddy "
        "collection is more labour-intensive and yields less per palm than cashew season production."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Palm Toddy / Ogogoro (West Africa)",
         "connection": "Both are palm-sap distillates from tropical colonial contexts; West African ogogoro "
                       "(from raffia palm, Nigeria) is produced by communities whose ancestors were connected "
                       "to the same colonial trade routes that brought the Portuguese to Goa. "
                       "The PCT and WADT trails converge here: Portuguese palm knowledge transferred across "
                       "Africa and Asia along the same sea routes"},
        {"tradition": "spirits", "beverage": "Arrack (Sri Lanka)",
         "connection": "Sri Lankan coconut arrack is the direct regional parallel — both use coconut palm "
                       "toddy as the fermentation base, both are GI-adjacent spirits in former South Asian "
                       "territories with colonial history. Arrack is more widely exported; coconut feni is "
                       "more artisanal and Goa-specific"}
    ],
    "sensory_profile": {
        "appearance": "Crystal clear; colourless",
        "nose": "Lighter than cashew feni: fresh coconut, slight sweetness, clean spirit, "
                "light tropical florals; less pungent, more delicate; the fresh toddy character is distinct "
                "from the artificial coconut of Caribbean spirits",
        "palate": "Clean, light-to-medium body; coconut sweetness in the background; "
                  "warming alcohol (40–45% ABV); shorter finish than cashew feni; "
                  "less complex but more delicate",
        "conclusion": "The lighter, more elegant expression of Goan distillation. Less challenging for "
                      "non-Indian palates than cashew feni; serves well in tropical cocktails as a coconut-"
                      "forward spirit with genuine provenance rather than artificial flavouring."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Double-Distilled Premium Coconut Feni", "criteria": "Daily-collected fresh toddy; "
          "hygienic fermentation; double distillation in clean cazani; consistent quality",
          "markers": "Named producer; export packaging; reduced congeners; light clean profile"},
        {"tier": 3, "tier_name": "Traditional Double-Distilled", "criteria": "Traditional cazani distillation; "
          "correct coconut feni character; genuine GI production",
          "markers": "Goa GI; traditional production; local quality"},
        {"tier": 2, "tier_name": "Standard Coconut Feni", "criteria": "Traditional production; typical "
          "coconut toddy character; local market quality",
          "markers": "Standard Goa village production; local bars"},
        {"tier": 1, "tier_name": "Neera / Fresh Toddy", "criteria": "Unfermented or lightly fermented; "
          "3–5% ABV; not distilled; consumed fresh or as mixer",
          "markers": "Street-side toddy stalls; seasonal availability"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature or over ice",
        "vessel": "Shot glass or rocks glass",
        "technique": "Coconut Feni & Tender Coconut Water: traditional Goan mixing. "
                     "Cocktail: coconut feni base for tropical sours and punches. "
                     "Neat: with Goan snacks (cashews, kokum, pork crackling)",
        "programme_position": "Tropical cocktail programme; Indian-focused bar; "
                              "education alongside cashew feni to demonstrate the full Goan spirits vocabulary",
        "verbal_presentation": "Coconut Feni — from the palm groves of coastal Goa. The toddy tapper "
                               "climbs each palm at sunrise, collects the sap overnight, and it becomes "
                               "this by afternoon. The lighter, more delicate side of Goa's distillation tradition."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Bhati Village Coconut Feni (Goa)",
        "producer_location": "Coastal Goa, India",
        "key_person": "[NEEDS VERIFICATION — no single nationally prominent coconut feni producer]",
        "production_volume": "Very small; even more limited than cashew feni",
        "certifications": ["GI — Feni (Goa only, coconut sub-category)"],
        "bc_distributor": "[NEEDS VERIFICATION — unavailable commercially in BC]",
        "us_distributor": "[NEEDS VERIFICATION — not commercially available in US mainstream channels]",
        "uk_distributor": "[NEEDS VERIFICATION — occasional UK specialist availability]",
        "price_tier": "Reserve (€20–40 in Goa; very limited international pricing)",
        "availability_notes": "Essentially unavailable outside Goa through normal commercial channels. "
                              "Direct procurement from Goa or UK specialist import required for any programme use."
    },
    "trail_connection": "PCT-8",
    "trail_note": "Coconut palm toddy traditions existed in Goa before Portuguese arrival, but distillation "
                  "of toddy into feni is attributed to Portuguese distillation knowledge transfer in the "
                  "16th century. The coconut palm itself spread along Portuguese trade routes from Southeast "
                  "Asia across the Indian Ocean — Goa's coastal coconut groves are a visible PCT landscape.",
    "food_pairings": [
        {"technique_id": "", "dish": "Fish curry with coconut milk (Goan fish curry)",
         "pairing_type": "complement",
         "rationale": "Coconut-on-coconut: the feni's fresh coconut base mirrors the curry's coconut milk "
                      "foundation; the spirit's alcohol cuts through the richness"},
        {"technique_id": "", "dish": "Dried prawn chutney (balchão)", "pairing_type": "bridge",
         "rationale": "The fermented-dried shrimp intensity of balchão meets the clean coconut spirit; "
                      "a classic Goan country pairing"}
    ],
    "source": "GI Feni documentation; Frederick Noronha food writing on Goa's toddy tradition; "
              "NDTV and Times of India coverage of Goa feni revival",
})

session.commit_batch()
print(f"\n[BATCH 12 COMMITTED — Goa Feni (Cashew + Coconut)]\n")

# ============================================================
# SWITCH TO PCT-13 — Cachaça (Brazil)
# ============================================================

session.switch_region("spirits", "Brazil — Cachaça")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "artisanal cachaça",
    "region": "Brazil — Minas Gerais / Paraty / São Paulo",
    "name": "Cachaça — Artisanal and Aged",
    "terroir_origin": (
        "Cachaça (pronounced kah-SHA-sah) is Brazil's national spirit and the world's third most-consumed "
        "spirit by volume (after Chinese baijiu and Indian whisky). It is distilled from fresh sugarcane "
        "juice (not molasses — this is the critical distinction from rum). Sugarcane (Saccharum officinarum) "
        "was brought to Brazil by Portuguese colonists in the early 16th century, with the first commercial "
        "plantations established in Pernambuco and Bahia around 1532. The PCT/WADT intersection: sugarcane "
        "was cultivated using enslaved African labour — the most brutal economic extraction of the colonial "
        "era — and cachaça emerged as the drink made FOR and BY enslaved Africans working the cane "
        "before it became the national drink of the free Brazilian republic. "
        "Three principal cachaça regions: Minas Gerais (highland plateau, clay soils, complex local "
        "wood ageing culture), São Paulo / Paraty (coastal climate, more delicate style), "
        "and Pernambuco/Nordeste (industrial scale, where the largest producers operate). "
        "Minas Gerais has the highest density of artisanal distilleries and is considered the spiritual "
        "home of quality cachaça."
    ),
    "production_technique": (
        "Fresh sugarcane juice (garapa) is pressed and fermented immediately — within hours of pressing — "
        "as the juice begins to oxidise rapidly. Natural fermentation uses wild yeasts or cultivated "
        "strains in open wooden fermentation vats (sometimes the same ancient wood maintained for decades "
        "as a yeast source). Fermentation to ~8% ABV takes 24–48 hours. Distillation in pot stills "
        "(alembics — Portuguese copper pot technology; column stills for industrial production). "
        "Artisanal cachaça is distilled once in copper alembic at 38–48% ABV. Industrial production "
        "uses continuous column stills at 96% ABV and diluted to 38–40%. "
        "The critical distinction from rum: molasses-based rum uses the residue after sugar extraction; "
        "cachaça uses fresh-pressed juice, which means the harvest window is narrow (18–24 weeks annually) "
        "and the spirit reflects the cane's terroir directly. "
        "Barrel ageing: artisanal cachaça is aged in native Brazilian woods — amburana (Torresea cearensis, "
        "gives vanilla/cinnamon/coumarin character), bálsamo (Myroxylon balsamum, rich and aromatic), "
        "jequitibá (Cariniana legalis, clean, integrative), ipê (Handroanthus spp.), umburana — not "
        "just French or American oak. This native wood ageing programme is cachaça's unique signature "
        "and the source of its most complex aged expressions."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Rhum Agricole (Martinique, AOC)",
         "connection": "The most direct parallel: both are fresh sugarcane juice spirits (not molasses), "
                       "both reflect cane terroir, both are AOC/GI-protected in their respective territories. "
                       "Rhum Agricole is French-colonially framed (Martinique AOC); cachaça is Portuguese/Brazilian. "
                       "The PCT and the broader Atlantic colonial sugar trade converge here: both were produced "
                       "on sugar plantations using enslaved labour"},
        {"tradition": "spirits", "beverage": "Armagnac aged in Gascon oak (Gascony, France)",
         "connection": "The comparison of regional native-wood ageing: Armagnac's use of black Monlezun "
                       "oak parallels cachaça's amburana and bálsamo ageing — both spirits develop "
                       "unique character impossible with standard French or American oak. Both represent "
                       "the argument that indigenous wood species produce spirits unavailable from "
                       "commodity cooperage"}
    ],
    "sensory_profile": {
        "appearance": "Unaged: crystal clear. Aged: light gold (amburana, 1–2yr) to deep amber (bálsamo, 5yr+). "
                      "Amburana gives faster colour development than oak",
        "nose": "Fresh (unaged): sugarcane juice, grassy, slight ferment note, fresh tropical fruit. "
                "Amburana-aged: extraordinary — vanilla, cinnamon, coconut cream, coumarin (sweet hay), "
                "dried fruit, marzipan. Bálsamo: resinous, complex, spiced, exotic wood. "
                "Oak-aged: more conventional whisky/brandy notes; less distinctive",
        "palate": "Unaged: clean, fresh, grassy-tropical; short finish. "
                  "Amburana-aged (2yr): remarkably complex for the age — spice, tropical fruit, long warm finish; "
                  "unlike any other aged spirit. Bálsamo: rich, resinous, lengthy. "
                  "ABV typically 38–40%",
        "conclusion": "Amburana-aged artisanal cachaça is one of the world's great undiscovered aged spirits. "
                      "It competes with premium aged rum and single malt Scotch in complexity at lower price. "
                      "Novo Fogo Barrel-Aged and Avuá Amburana are North American benchmark expressions."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Single-Harvest Native Wood Aged (3yr+)", "criteria": "Single harvest, named "
          "producer, amburana/bálsamo/umburana aged 3+ years, copper alembic distillation, export quality",
          "markers": "Avuá Amburana 3yr; Novo Fogo Single Barrel; named cane source; premium international pricing"},
        {"tier": 3, "tier_name": "Artisanal Aged (1–3yr)", "criteria": "Copper alembic, fresh juice, "
          "native wood or oak aged 1–3yr; artisanal Minas Gerais production",
          "markers": "Novo Fogo Silver/Gold; Leblon Reserva Especial; artisanal label; consistent quality"},
        {"tier": 2, "tier_name": "Artisanal Unaged (Prata)", "criteria": "Copper alembic, fresh juice, "
          "unaged or brief stainless rest; the standard for caipirinha",
          "markers": "Leblon; Novo Fogo Silver; Avuá Prata; the caipirinha standard"},
        {"tier": 1, "tier_name": "Industrial Cachaça", "criteria": "Column still, molasses possible, "
          "bulk production; correct but without artisanal character",
          "markers": "Ypioca; 51 (Pirassununga 51); supermarket pricing; caipirinha cocktail bars"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature for neat; chilled for caipirinha",
        "vessel": "Rocks glass for neat; tumbler/rocks glass for caipirinha",
        "technique": "The Caipirinha (Brazil's national cocktail): 60mL cachaça + 1 lime quartered "
                     "and muddled with 15g caster sugar + ice (crushed or cubed). "
                     "Aged cachaça neat: rocks glass, 45mL, single large ice cube, "
                     "5 minutes to open before drinking. "
                     "Premium sipping: amburana-aged, neat at room temperature, "
                     "treated as a premium aged spirit (small pour, nose, palate, finish)",
        "programme_position": "Cocktail programme anchor (caipirinha); premium spirits section for aged expressions; "
                              "Brazilian-focused tasting menus; WADT/PCT intersection conversation piece",
        "verbal_presentation": "Novo Fogo cachaça — from the cane fields of Paraná, Brazil. Distilled from "
                               "fresh-pressed sugarcane juice in a copper alembic, then aged in amburana wood — "
                               "a native Brazilian tree that gives a flavour impossible with any other spirit. "
                               "Not rum. Never rum."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Novo Fogo (Morretes, Paraná) and Avuá (Rio de Janeiro state)",
        "producer_location": "Novo Fogo: Morretes, Paraná (organic, Atlantic Forest-adjacent). "
                             "Avuá: Rio de Janeiro state / Minas Gerais sourcing",
        "key_person": "Dragos Axinte (Novo Fogo CEO); Kit Clancy / Chad Solomon (Avuá founders)",
        "production_volume": "Novo Fogo: ~100,000 bottles annually (organic certified); "
                             "Avuá: ~50,000 bottles annually",
        "certifications": ["Brazilian GI — Cachaça (GI since 2012)", "Novo Fogo: Certified Organic (IBD/IFOAM)"],
        "bc_distributor": "Avuá: Sovereign Canada (confirmed); Leblon: available at BC retail (Bacardi Canada or agent; name NEEDS VERIFICATION); Novo Fogo: limited BC availability, likely private import",
        "us_distributor": "Novo Fogo: Skurnik Wines NY/NJ (confirmed) + state-by-state distributors; "
                          "Leblon: Bacardi USA (confirmed — Bacardi acquired full ownership 2015); "
                          "Avuá: national US importer name NEEDS VERIFICATION (available at Total Wine nationally); "
                          "Ypióca: Diageo North America (confirmed — Diageo acquired Ypióca 2012)",
        "uk_distributor": "Novo Fogo through Masters of Malt; Leblon through various spirits merchants",
        "price_tier": "Market to Reserve (unaged BC ~$35–45; amburana aged BC ~$55–85; US ~$30–75)",
        "availability_notes": "Leblon: widely available BC Liquor and US national through Moët Hennessy. "
                              "Novo Fogo: BC limited — specialty spirits stores; US through Domaine Select. "
                              "Avuá: US specialist distribution; rare in BC."
    },
    "trail_connection": "PCT-13",
    "trail_note": "Cachaça is the PCT/WADT intersection in a glass. Portuguese colonialism brought sugarcane "
                  "to Brazil from Madeira and the Azores (the Portuguese Atlantic island chain where sugar "
                  "was first commercially cultivated). Enslaved West and Central African people (WADT) "
                  "worked the cane and first fermented and distilled the sugarcane juice — cachaça was "
                  "initially forbidden to the enslaved by colonial law (they were forced to drink the "
                  "inferior molasses rum while masters drank Portuguese wine), then became the drink of "
                  "resistance, community, and celebration. The caipirinha's lime is also a PCT artifact "
                  "(citrus arrived via Portuguese trade routes from Asia).",
    "food_pairings": [
        {"technique_id": "", "dish": "Feijoada (black bean and pork stew)", "pairing_type": "complement",
         "rationale": "Brazil's national dish with Brazil's national spirit. The caipirinha's acidity "
                      "cuts through feijoada's richness; the cachaça's sugarcane character bridges with "
                      "the dish's pork-and-bean depth"},
        {"technique_id": "", "dish": "Ceviche (PCT/WADT crossover dish)", "pairing_type": "bridge",
         "rationale": "Amburana-aged cachaça's vanilla-spice character bridges with ceviche's "
                      "citrus-ají amarillo complexity; the spirit's cane character echoes the "
                      "sugarcane history in the same Atlantic trade routes that brought the "
                      "techniques for both"}
    ],
    "source": "Brazilian GI documentation for Cachaça; Instituto Brasileiro da Cachaça (IBRAC) data; "
              "Novo Fogo official documentation; Avuá winery notes; "
              "Oxford Companion to Spirits — Cachaça entry",
})

session.commit_batch()
print(f"\n[BATCH 13 COMMITTED — Cachaça entry]\n")

# Producers for Cachaça
session.add_producer({
    "name": "Novo Fogo Cachaça",
    "location": "Morretes, Paraná, Brazil",
    "country": "Brazil",
    "region": "Paraná — Atlantic Forest",
    "tradition": "spirits",
    "key_person": "Dragos Axinte (CEO)",
    "founded": "2010",
    "production_volume": "~100,000 bottles annually; organic certified since inception",
    "notable_products": ["Novo Fogo Silver (unaged)", "Novo Fogo Gold (aged in Brazilian hardwood)",
                         "Novo Fogo Single Barrel", "Novo Fogo Tanager (aged in amburana)"],
    "certifications": ["Brazilian GI Cachaça", "IFOAM Organic Certified", "B Corp"],
    "website": "novofogo.com",
    "philosophy": "Carbon-negative production in the Atlantic Forest biome. All barrels from sustainably "
                  "harvested native Brazilian woods. Novo Fogo pioneered the North American market for "
                  "premium artisanal cachaça from a single certified-organic distillery. B Corp certified.",
    "trail_connection": "PCT-13",
    "source": "Novo Fogo official documentation; B Corp database; IBRAC certification records",
    "verified": True
})

session.add_producer({
    "name": "Leblon Cachaça",
    "location": "Patos de Minas, Minas Gerais, Brazil",
    "country": "Brazil",
    "region": "Minas Gerais",
    "tradition": "spirits",
    "key_person": "Steve Luttmann (founder, US side); Brazilian production team",
    "founded": "2005",
    "production_volume": "Large commercial volume; distributed nationally in US through Moët Hennessy",
    "notable_products": ["Leblon Cachaça (silver, unaged)", "Leblon Reserva Especial (Cognac cask aged)"],
    "certifications": ["Brazilian GI Cachaça"],
    "website": "leblon.com",
    "philosophy": "Founded by a New Yorker (Steve Luttmann) who fell in love with cachaça while working "
                  "in Brazil. Leblon was the pioneer in bringing premium cachaça to the US cocktail market "
                  "(2005–2010). Now owned/distributed by Moët Hennessy, making it the most widely "
                  "available premium cachaça in the US and Canada.",
    "trail_connection": "PCT-13",
    "source": "Leblon official history; Moët Hennessy portfolio documentation; IWSR distribution data",
    "verified": True
})

session.add_producer({
    "name": "Avuá Cachaça",
    "location": "Rio de Janeiro State / Minas Gerais, Brazil",
    "country": "Brazil",
    "region": "Southeastern Brazil",
    "tradition": "spirits",
    "key_person": "Kit Clancy, Chad Solomon (founders)",
    "founded": "2012",
    "production_volume": "Boutique; ~50,000 bottles annually",
    "notable_products": ["Avuá Prata (unaged)", "Avuá Amburana (amburana wood aged)",
                         "Avuá Tapinhoa (tapinhoa wood aged)", "Avuá Bálsamo"],
    "certifications": ["Brazilian GI Cachaça"],
    "website": "avuacachaca.com",
    "philosophy": "Avuá is the definitive artisanal cachaça brand for the North American on-trade spirits "
                  "market. Their native wood programme is the most extensive of any export-focused producer: "
                  "amburana, tapinhoa, bálsamo, and umburana expressions from small-batch Minas Gerais "
                  "production. Co-founders are bartenders, making the brand uniquely bar-programme oriented. "
                  "Canadian distribution through Sovereign Canada (confirmed).",
    "trail_connection": "PCT-13",
    "source": "Avuá official documentation; Tales of the Cocktail brand profile; Sovereign Canada portfolio",
    "verified": True
})

session.add_producer({
    "name": "Sovereign Canada",
    "location": "Canada",
    "country": "Canada",
    "region": "National",
    "tradition": "spirits",
    "key_person": "[NEEDS VERIFICATION]",
    "founded": "[NEEDS VERIFICATION]",
    "production_volume": "Distributor/agent only — not a producer",
    "notable_products": ["Avuá Cachaça (confirmed BC/Canada distribution)"],
    "certifications": [],
    "website": "sovereigncanada.com",
    "philosophy": "Canadian spirits importer/agent distributing premium artisanal spirits in BC and nationally. "
                  "Confirmed Canadian distributor for Avuá Cachaça based on Sovereign Canada brand page and "
                  "retail presence at ZYN.ca and Vine Arts (Alberta).",
    "trail_connection": "PCT-13",
    "source": "Sovereign Canada official website; ZYN.ca BC retail listing for Avuá",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 14 COMMITTED — Cachaça Producers]\n")

# Cachaça purveyors
session.add_purveyor({
    "name": "Bacardi USA",
    "type": "importer",
    "location": "Coral Gables, FL, USA",
    "markets_served": ["nationwide_US", "all_50_states"],
    "traditions_carried": ["spirits", "wine", "champagne"],
    "producer_relationships": ["Leblon Cachaça", "Grey Goose Vodka", "Bombay Sapphire Gin", "Bacardi Rum"],
    "website": "bacardi.com",
    "contact": "bacardi.com/contact",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Bacardi acquired full ownership of Leblon Cachaça in 2015 (completed from original "
                      "acquisition). Distributes through Bacardi USA's extensive national distribution network "
                      "across all 50 states. The most accessible route for US accounts wanting a premium "
                      "cachaça on their programme — widely available at Total Wine, BevMo, and major chains.",
    "verified": True
})

session.add_purveyor({
    "name": "Skurnik Wines & Spirits (Spirits Division)",
    "type": "importer",
    "location": "New York, NY, USA",
    "markets_served": ["New_York", "New_Jersey", "Connecticut", "Rhode_Island", "Pennsylvania", "Ohio", "California"],
    "traditions_carried": ["spirits", "wine", "fortified"],
    "producer_relationships": ["Novo Fogo Cachaça (NY/NJ confirmed)", "Churchill's Port (US national)", "Anselmo Mendes (Portuguese wine)"],
    "website": "skurnik.com",
    "contact": "skurnik.com/contact",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Skurnik confirmed as Novo Fogo importer for New York and New Jersey (since April 2019). "
                      "In other states, Novo Fogo uses state-by-state distributor network (Burke Distributing in MA/NE). "
                      "For Canadian/BC market: limited availability; Globe and Mail confirmed some BC/Alberta presence "
                      "in 2017 but current named BC agent not confirmed — likely private import.",
    "verified": False
})

session.commit_batch()
print(f"\n[BATCH 15 COMMITTED — Cachaça Purveyors]\n")

handoff = session.finish()
print(handoff)
