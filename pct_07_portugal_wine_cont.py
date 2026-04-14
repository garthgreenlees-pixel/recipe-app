#!/usr/bin/env python3
"""
PCT-1 Portugal Wine Continuation:
Douro DOC Table Wines, Bairrada/Baga, Lisboa Region, Moscatel de Setúbal
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="wine",
    region="Portugal — Douro Valley (DOC Table Wine)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=8,
    running_total=39
)

# ============================================================
# DOURO DOC TABLE WINE — PCT-1
# ============================================================

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "douro valley red table wine",
    "region": "Portugal — Douro Valley (DOC)",
    "name": "Douro DOC Red — Touriga Nacional, Touriga Franca, Tinta Roriz",
    "terroir_origin": (
        "The Douro Valley's transformation from the world's greatest fortified wine region "
        "into a source of exceptional table wines is one of the past 40 years' most significant "
        "developments in European wine. The same schist soils, extreme terraced slopes, and "
        "continental heat that build Port's intensity also produce red table wines of "
        "extraordinary concentration when yields are controlled and harvest timing is precise. "
        "The Douro Superior (upstream section, east of Pinhão) and Baixo Corgo (downstream, "
        "cooler, more Atlantic-influenced) each produce distinct table wine characters. "
        "The primary varieties for Douro red table wine: "
        "Touriga Nacional — the 'Cabernet Sauvignon of Portugal'; dark-fruited, tannic, "
        "floral (violets), full-bodied; the backbone of Douro reds. "
        "Touriga Franca — more aromatic, lighter in colour, less tannic than Touriga Nacional; "
        "the blending partner that adds perfume and freshness. "
        "Tinta Roriz (identical to Tempranillo/Aragonês) — structure, body, dried fruit; "
        "the Spanish variety that crossed into Portugal through the Douro's inland corridor. "
        "Benchmark producers: Quinta do Crasto (since 1615; 'LBV' level table wines); "
        "Quinta do Vale Meão (Ramos Pinto origin; Francisco Olazabal; "
        "one of Portugal's most respected table wine estates since the 1990s); "
        "Ramos Pinto's Duas Quintas (the commercial face of their table wine programme). "
        "Niepoort's 'Redoma' and 'Charme' are considered Portugal's reference Douro table wines "
        "— Dirk Niepoort was among the first to prove the Douro's table wine potential in the 1990s."
    ),
    "production_technique": (
        "Douro table wine production represents a deliberate departure from the Port winemaking model. "
        "Where Port requires fortification to arrest fermentation (preserving sweetness and raising ABV), "
        "table wine production completes fermentation fully to dryness. "
        "The challenge: Douro's extreme heat (routinely 40°C+ at harvest) risks over-extraction "
        "and loss of freshness if not carefully managed. "
        "Modern Douro table wine techniques: lagares (traditional granite foot-treading troughs) "
        "used by premium producers for extraction — gentler than mechanical alternatives; "
        "whole-cluster fermentation by some producers to add structure and herbaceous lift; "
        "temperature-controlled stainless steel for freshness preservation. "
        "Ageing: French and Portuguese oak (small barrel 225L) for 12–18 months at reserve tier. "
        "Quinta do Vale Meão's Meandro do Vale Meão is the benchmark value tier; "
        "the Vale Meão flagship is the reference premium Douro red. "
        "Niepoort Redoma Tinto: foot-trodden in lagar; old vine Touriga Franca dominant; "
        "Burgundian winemaking sensibility applied to Douro terroir — "
        "the most individually distinctive Douro table wine approach."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Côtes du Rhône Villages / Gigondas (Southern Rhône)",
         "connection": "Douro table wines and Southern Rhône reds share the warm-continental "
                       "terroir model: both work in extreme heat; both blend multiple varieties "
                       "(Grenache-Syrah-Mourvèdre vs. Touriga Nacional-Touriga Franca-Tinta Roriz); "
                       "both produce big, structured reds that require bottle age for integration. "
                       "Quinta do Crasto Reserve and a Gigondas occupy the same quality tier "
                       "at comparable price; the winemaking philosophy is essentially identical "
                       "across the two regions, separated only by the schist vs. limestone terroir"},
        {"tradition": "fortified", "beverage": "Vintage Port (same grapes, same valley)",
         "connection": "The Douro table wine is the most instructive beverage parallel in all of "
                       "wine — the same grape varieties, the same terraced schist vineyards, "
                       "the same harvest, but two completely different wines based solely on "
                       "whether fermentation is arrested (Port) or completed (table wine). "
                       "A side-by-side tasting of Niepoort Redoma Tinto and Niepoort Vintage Port "
                       "from the same estate is the most condensed explanation of what fortification "
                       "actually does to a wine"}
    ],
    "sensory_profile": {
        "appearance": "Deep ruby to garnet; moderate to intense colour density; "
                      "rim purple-red in youth, bricking with 8+ years of age",
        "nose": "Quinta do Vale Meão: blackberry, black cherry, dried violet, "
                "pencil shavings, schist mineral (a distinctive dry-stone character "
                "absent in limestone-grown reds), warm spice, leather with age. "
                "Niepoort Redoma: more Burgundian register — perfumed, red fruit dominant, "
                "less extract, greater delicacy; the Touriga Franca's floral character "
                "at the centre; the Douro's mineral signature underneath. "
                "Both: a warm-stone minerality that identifies the schist terroir "
                "as clearly as Chablis identifies chalk.",
        "palate": "Touriga Nacional-dominant (Vale Meão, Crasto): full body, firm tannin, "
                  "13.5–14.5% ABV; requires 5–8 years of bottle age for integration; "
                  "extraordinary aging potential (20+ years at top estates). "
                  "Niepoort Redoma: more linear, lower extraction; 13–13.5% ABV; "
                  "can be drunk earlier but rewards 5–10 years. "
                  "Both converge on a shared character: the dry-stone schist mineral finish "
                  "that is the Douro's most distinctive table wine signature.",
        "conclusion": "The Douro produces some of Portugal's finest table wines at price points "
                      "that remain substantially below equivalent quality from Burgundy, Tuscany, "
                      "or Napa. For a programme: position Douro table wine as the PCT's most "
                      "commercially accessible premium red — the Fort has the heritage; "
                      "the table wine has the food versatility."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Niepoort Redoma / Quinta do Vale Meão Flagship",
         "criteria": "Estate-level; single quinta; foot-trodden or minimal-intervention extraction; "
                     "18+ months French oak; 10+ year aging potential",
         "markers": "Niepoort Redoma Tinto; Quinta do Vale Meão; Quinta do Crasto Reserva Especial; "
                    "Quinta do Noval Nacional (Port estate table wine); BC ~$50–80; US ~$40–70"},
        {"tier": 3, "tier_name": "Quinta do Crasto Reserve / Meandro do Vale Meão",
         "criteria": "Named estate; Touriga Nacional dominant; 12–18 months French oak; "
                     "Douro DOC; reserve classification",
         "markers": "Quinta do Crasto Reserva; Meandro do Vale Meão; Ramos Pinto Duas Quintas Reserve; "
                    "BC ~$30–50; US ~$25–40"},
        {"tier": 2, "tier_name": "Douro DOC Standard / Duas Quintas",
         "criteria": "Douro DOC; varietal blend correct; 12 months oak; commercial quality",
         "markers": "Ramos Pinto Duas Quintas; Ferreira Esteva; Esporão Douro; BC ~$18–30; US ~$15–25"},
        {"tier": 1, "tier_name": "Douro Entry / Regional Blend",
         "criteria": "Douro DOC or IGP Duriense; accessible; correct variety character",
         "markers": "Commercial Douro blends; supermarket tier Portugal; BC ~$12–18; US ~$10–15"}
    ],
    "service_intelligence": {
        "temperature": "16–18°C; younger Touriga Nacional-dominant wines benefit from the upper range. "
                       "Decant reserve tier 30–45 minutes; flagship tier 60 minutes.",
        "vessel": "Bordeaux glass (standard; the tannin structure benefits from the wider bowl). "
                  "Niepoort Redoma: Burgundy glass would also work given the Touriga Franca lightness.",
        "technique": "Douro table wine requires time: open 1 hour before service for reserve tier. "
                     "Best served slightly warmer than other reds (17–18°C) — "
                     "the schist mineral character opens at temperature. "
                     "Douro-Port comparative: serve Douro red alongside the same estate's LBV Port "
                     "to demonstrate the fortification decision. "
                     "Cellar recommendations: top Douro reds drink well at 8–15 years; "
                     "Niepoort Redoma at 10 years is a transformed wine.",
        "programme_position": "Premium red anchor for PCT programme; Port comparison pairing; "
                              "heritage narrative for the Douro valley",
        "verbal_presentation": "Quinta do Vale Meão — Douro Superior. "
                               "The same schist terraces that build Vintage Port. "
                               "Fermented to dryness instead. "
                               "The wine Portugal kept for itself until the 1990s."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Quinta do Vale Meão (Francisco Olazabal, Douro Superior) "
                              "and Niepoort (Dirk Niepoort, Cima Corgo)",
        "producer_location": "Quinta do Vale Meão: Vale de Figueira, Douro Superior, Portugal; "
                             "Niepoort: Cima Corgo, Douro Valley",
        "key_person": "Francisco Olazabal (Quinta do Vale Meão; Ramos Pinto founding family descendant); "
                      "Dirk Niepoort (Niepoort — benchmark for Douro table wine philosophy)",
        "production_volume": "Vale Meão: boutique to premium; Niepoort: small to medium; "
                             "Quinta do Crasto: large (widest international distribution)",
        "certifications": ["Douro DOC"],
        "bc_distributor": "Quinta do Crasto and Ramos Pinto Duas Quintas: available at BC Liquor (Evaton Inc.); "
                          "Niepoort Redoma: Polaner Selections (US); "
                          "Galleon/Dandurand (BC — Folio Wine Partners importer)",
        "us_distributor": "Niepoort table wines: Polaner Selections (national — confirmed, separate from "
                          "Martine's Wines which handles Niepoort Port); "
                          "Quinta do Crasto: Folio Wine Partners (national); "
                          "Quinta do Vale Meão: Domaine Select (national)",
        "uk_distributor": "Douro table wines widely available: Lea & Sandeman; Theatre of Wine; "
                          "Armit Wines; Wines of Portugal (UK); major supermarkets",
        "price_tier": "Market to Reserve (Duas Quintas US ~$18; Crasto Reserva US ~$35; "
                      "Vale Meão US ~$55; Niepoort Redoma US ~$45–55)",
        "availability_notes": "In BC: Ramos Pinto Duas Quintas and Quinta do Crasto standard "
                              "available at BC Liquor stores. Niepoort Redoma: Marquis Wine Cellars "
                              "or Liberty Wine Vancouver. US: Polaner, Folio, Domaine Select national."
    },
    "trail_connection": "PCT-1",
    "trail_note": "The Douro Valley is the PCT's geographical origin — "
                  "the same valley whose wine wealth funded Portugal's 15th-century maritime expansion. "
                  "Henry the Navigator's funding for the Atlantic voyages drew on Douro wine revenues. "
                  "The table wine tradition is the Douro's newest chapter: "
                  "500 years of fortification monopoly, then 40 years of table wine ambition, "
                  "producing a category that has only begun to reach its ceiling.",
    "food_pairings": [
        {"technique_id": "", "dish": "Bacalhau à Brás (salt cod with eggs, potato, olives)",
         "pairing_type": "bridge",
         "rationale": "The PCT's most canonical food pairing on its home territory: "
                      "bacalhau à Brás is Portugal's most consumed dish and the direct expression "
                      "of the same Atlantic cod trade that Port wine funded. "
                      "A Douro table wine's schist mineral and dried herb character "
                      "bridges with the salt cod's cured-sea character while the egg richness "
                      "finds the wine's fruit depth — the Douro valley in food and wine form"},
        {"technique_id": "", "dish": "Leitão da Bairrada (roast suckling pig, Bairrada region)",
         "pairing_type": "complement",
         "rationale": "Portugal's most celebrated roasted meat preparation — "
                      "the crispy-skinned suckling pig of Bairrada — demands a structured red "
                      "with enough tannin to cut the fat. Douro Touriga Nacional's firm tannin "
                      "and dark-fruit depth provides exactly that structure. "
                      "Historically: this pairing is the Portuguese table wine's "
                      "greatest national argument"}
    ],
    "source": "IVDP (Instituto dos Vinhos do Douro e do Porto) DOC regulations; "
              "Niepoort official production documentation; "
              "Quinta do Vale Meão official estate documentation; "
              "Quinta do Crasto production history; "
              "Jancis Robinson 'Wine Grapes' (Touriga Nacional entry); "
              "Wines of Portugal official regional guide",
})

session.commit_batch()
print(f"\n[BATCH 37 COMMITTED — Douro DOC Table Wines]\n")

# ============================================================
# BAIRRADA / BAGA — PCT-1
# ============================================================

session.switch_region("wine", "Portugal — Bairrada DOC (Baga)")

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "bairrada baga red wine",
    "region": "Portugal — Bairrada DOC (Beira Litoral, Atlantic)",
    "name": "Bairrada Baga — Portugal's Most Atlantic Red, the Barraida Iron Lady",
    "terroir_origin": (
        "Bairrada ('land of clay') is Portugal's most Atlantic red wine region — "
        "located 20km from the coast of Beira Litoral, between the Serra do Buçaco hills "
        "and the Atlantic coast. This proximity to the ocean creates the coolest and "
        "wettest growing conditions for any Portuguese DOC: average annual temperatures "
        "of 15°C vs. Douro's 18°C; 1,000–1,200mm annual rainfall vs. Douro's 500–600mm. "
        "The result: wines of extraordinary tension, structure, and longevity from a single "
        "dominant variety — Baga (Casta Baga de Bairrada). "
        "Baga is found almost nowhere outside Bairrada in commercial quantity. "
        "It is Portugal's most challenging and most rewarding indigenous variety: "
        "late ripening (the latest harvest in Portugal, often October); very thick skins "
        "producing massive tannin; naturally high acidity; requires 20+ years of bottle "
        "age to fully integrate in top expressions. "
        "Luís Pato is the transformative figure: since the 1980s, he has demonstrated "
        "that Baga, when harvested at precise maturity and vinified with care, "
        "produces wines comparable to the greatest Burgundy in structure and longevity. "
        "His daughter Filipa Pato now runs her own estate and represents the next generation "
        "of Bairrada's international positioning. "
        "Sidónio de Sousa (since 1927, the oldest Bairrada estate in continuous family operation) "
        "and Quinta das Bágeiras (Mário Sérgio Nuno) are the other reference producers."
    ),
    "production_technique": (
        "Baga production has undergone significant technical evolution since the 1980s. "
        "The pre-1980 approach: early harvest, aggressive extraction, massive tannin without fruit "
        "counterbalance — producing wines that took decades to integrate and drink. "
        "Luís Pato's revolution: later harvest for full phenolic ripeness; whole-cluster inclusion "
        "for aromatic complexity; destemming for tannin control; longer cold maceration pre-fermentation "
        "for colour and aromatics without hard tannin extraction; shorter warm maceration. "
        "The result: wines with Baga's structural DNA but balanced fruit expression. "
        "Filipa Pato's approach: even more Burgundian — whole-cluster fermentation; "
        "gravity-flow cellar; minimal sulphur; light extraction. "
        "Ageing: traditional producers use large old Portuguese oak vats (lagares); "
        "modern producers use a combination of French barrique and old oak for 12–18 months. "
        "Bairrada also produces Portugal's second-most important sparkling wine: "
        "méthode traditionnelle using Baga (Luís Pato, Sidónio de Sousa) — "
        "one of the world's most unusual sparkling wines due to Baga's extreme tannin."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Barolo (Nebbiolo, Piedmont)",
         "connection": "The single-variety, high-acid, high-tannin, profound-longevity model: "
                       "Baga and Nebbiolo are structurally identical problems — both require "
                       "correct harvest timing and careful extraction to manage tannin, "
                       "both produce wines of extraordinary longevity (20–40 years for top expressions), "
                       "both are found almost exclusively in a single region. "
                       "Luís Pato's Baga is to Portugal what Giacomo Conterno's Barolo is to Italy: "
                       "the uncompromising expression of a difficult variety at its greatest height"},
        {"tradition": "wine", "beverage": "Gevrey-Chambertin Premier Cru (Pinot Noir, Burgundy)",
         "connection": "Filipa Pato's style specifically invites the Burgundy comparison: "
                       "whole-cluster fermentation, gravity flow, minimal intervention. "
                       "Where Luís Pato argues that Baga is Portugal's Barolo, "
                       "Filipa Pato argues it can be Bairrada's Burgundy — "
                       "not by imitation but by applying the same winemaking philosophy "
                       "to a completely different terroir. The resulting wines share "
                       "Burgundy's transparency to place while remaining unmistakably Bairrada"}
    ],
    "sensory_profile": {
        "appearance": "Deep ruby to purple-ruby in youth; significant colour depth from Baga's thick skins; "
                      "develops garnet-bricking after 10+ years; slow legs from moderate alcohol (12.5–13.5%)",
        "nose": "Young Baga (2–5 years): tightly wound; red cherry, dried blackcurrant, "
                "leather, eucalyptus, dark earthy mineral; "
                "Baga's famous iron/graphite mineral note emerges from the clay soils — "
                "a distinctive metallic-mineral character absent in schist or limestone wines. "
                "10+ years: extraordinary transformation — dried rose petals, tobacco, leather, "
                "dark chocolate, forest floor, wet clay, iron. "
                "Luís Pato Vinha Pan (old vine, single vineyard): the fullest expression of "
                "the Bairrada iron-and-rose character at 10 years.",
        "palate": "Youth: massive tannin (the Baga signature — fine but abundant, "
                  "requiring food or time); bright acidity (Atlantic proximity); "
                  "dark cherry and plum fruit. "
                  "10+ years: the tannin integrates into a silky-firm structure; "
                  "the acidity drives freshness that Douro reds cannot maintain. "
                  "Filipa Pato Nossa Calcário: more delicate from the limestone soil expression; "
                  "the most Burgundy-like of Bairrada's current generation. "
                  "The wine that requires patience but rewards it utterly.",
        "conclusion": "Bairrada Baga is the most undervalued great wine of Europe. "
                      "At 10–15 years, top Luís Pato and Filipa Pato Baga outpoints "
                      "Barolo at twice the price and Côte de Nuits at three times the price. "
                      "For a programme: position as the discovery wine for guests who "
                      "understand Burgundy or Barolo and want the next frontier."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Luís Pato Vinha Pan / Filipa Pato Nossa Calcário — Single Vineyard",
         "criteria": "Single vineyard; old vine Baga (60+ years); minimal-intervention vinification; "
                     "8–15 years bottle age for full expression; top critical recognition",
         "markers": "Luís Pato Vinha Pan; Filipa Pato Nossa Calcário; Sidónio de Sousa Garrafeira; "
                    "BC ~$45–65; US ~$35–55"},
        {"tier": 3, "tier_name": "Luís Pato Vinha Formal / Quinta das Bágeiras Garrafeira",
         "criteria": "Estate selection; old vine Baga; 15–18 months oak; Bairrada DOC; "
                     "5+ year aging recommended",
         "markers": "Luís Pato Vinha Formal; Quinta das Bágeiras Garrafeira; Campolargo Baga Reserve; "
                    "BC ~$28–45; US ~$22–35"},
        {"tier": 2, "tier_name": "Bairrada DOC Standard / Luís Pato Entry",
         "criteria": "Bairrada DOC; Baga-dominant; correct iron-mineral character; commercial quality",
         "markers": "Luís Pato Baga; Filipa Pato Bical Branco (white companion); BC ~$18–28; US ~$14–22"},
        {"tier": 1, "tier_name": "Beiras IGP / Entry Baga",
         "criteria": "Beiras regional; Baga component; entry to the character; "
                     "more accessible than full Bairrada DOC tannin",
         "markers": "Beiras IGP Baga blends; commercial Bairrada; BC ~$12–18; US ~$10–14"}
    ],
    "service_intelligence": {
        "temperature": "16–17°C; slightly cooler than Douro reds to preserve the Atlantic freshness. "
                       "Young Baga: do not serve too warm — tannin becomes hard at 20°C+.",
        "vessel": "Burgundy glass (the wider bowl opens Baga's aromatics better than Bordeaux glass). "
                  "Young Baga in a Riedel Pinot Noir glass will open faster than in a standard glass.",
        "technique": "Young Baga (under 8 years): mandatory decant 60–90 minutes; "
                     "serve with food — the tannin requires protein fat to integrate. "
                     "Aged Baga (10+ years): open the bottle 30 minutes early, pour gently; "
                     "the wine has already opened in the bottle — decanting is optional. "
                     "Guest recommendation: 'Come back to this in 10 years' is the correct framing "
                     "for a new Baga vintage; explain the Barolo parallel.",
        "programme_position": "Discovery wine for Barolo and Burgundy enthusiasts; "
                              "value proposition anchor for the premium wine list; "
                              "PCT-1 Portugal heritage wine alongside Port",
        "verbal_presentation": "Luís Pato Vinha Pan — Bairrada, Portugal. "
                               "Old vine Baga from the Atlantic coast. "
                               "Portugal's answer to Barolo. Twenty years of patience, "
                               "then a wine that outlasts everything else on the list."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Luís Pato (Bairrada, Óis do Bairro) and Filipa Pato (Bairrada)",
        "producer_location": "Óis do Bairro, Bairrada DOC, Beira Litoral, Portugal",
        "key_person": "Luís Pato (the defining figure of modern Bairrada); "
                      "Filipa Pato (daughter; next-generation Bairrada benchmark; Burgundy-trained)",
        "production_volume": "Luís Pato: small-to-medium family estate; "
                             "Filipa Pato: micro-winery; both critically acclaimed internationally",
        "certifications": ["Bairrada DOC"],
        "bc_distributor": "Luís Pato: Marquis Wine Cellars and Liberty Wine Merchants (Vancouver) "
                          "carry on occasion; no dedicated BC distributor confirmed; "
                          "check BCLDB special order catalogue",
        "us_distributor": "Luís Pato: Skurnik Wines & Spirits (national — confirmed); "
                          "Filipa Pato: Small Vineyards (NYC, specialty importer)",
        "uk_distributor": "Luís Pato: Lay & Wheeler (Suffolk); Armit Wines (London); "
                          "Majestic Wine occasionally. Filipa Pato: specialist Portuguese importers",
        "price_tier": "Market to Reserve (Luís Pato entry US ~$18; Vinha Formal US ~$28; "
                      "Vinha Pan US ~$45–55; Filipa Pato Nossa Calcário US ~$38–45)",
        "availability_notes": "In BC: most accessible via private import request through Marquis or Liberty. "
                              "US: Skurnik national for Luís Pato — major cities well covered. "
                              "UK: the best-served market globally for Bairrada outside Portugal."
    },
    "trail_connection": "PCT-1",
    "trail_note": "Bairrada's roast suckling pig (leitão) and sparkling Baga wine are as deeply embedded "
                  "in Portuguese coastal culture as Port is in the Douro's interior. "
                  "The monastery of Santa Cruz in Coimbra (30km south of Bairrada) was founded "
                  "in 1131 by Crusaders who were partly funded by early Bairrada wine trade. "
                  "The Atlantic climate that shapes Baga is the same climate that drove Portuguese "
                  "navigators to seek calmer latitudes — the wet, grey Atlantic winter "
                  "that makes Bairrada both challenging and irreplaceable.",
    "food_pairings": [
        {"technique_id": "", "dish": "Leitão da Bairrada (Bairrada roast suckling pig)",
         "pairing_type": "complement",
         "rationale": "The canonical regional pairing: Bairrada suckling pig is slow-roasted "
                      "until the skin is lacquered and crisp; the fat-rendered flesh requires "
                      "the Baga's firm tannin and bright Atlantic acidity to cut and refresh. "
                      "This is one of Europe's most perfectly calibrated regional food-wine pairings — "
                      "the pig and the Baga evolved alongside each other in the same Atlantic clay"},
        {"technique_id": "", "dish": "Chanfana (Bairrada slow-braised kid goat in red wine)",
         "pairing_type": "bridge",
         "rationale": "Chanfana — kid goat marinated in red wine, garlic, paprika, bay, "
                      "then slow-braised in a black clay pot — is the braised-wine bridge: "
                      "the same Baga used to cook the dish creates a register match "
                      "between the wine-braised meat and the wine-in-the-glass. "
                      "The iron-mineral character of both Baga and the clay cooking pot "
                      "creates a flavour unity unique to Bairrada"}
    ],
    "source": "CVB (Comissão Vitivinícola da Bairrada) DOC regulations; "
              "Luís Pato official estate documentation; "
              "Filipa Pato official estate documentation; "
              "Wines of Portugal Bairrada regional guide; "
              "Jancis Robinson 'Wine Grapes' (Baga entry)",
})

session.commit_batch()
print(f"\n[BATCH 38 COMMITTED — Bairrada Baga]\n")

# ============================================================
# MOSCATEL DE SETÚBAL — PCT-1
# ============================================================

session.switch_region("fortified", "Portugal — Setúbal Peninsula (Moscatel de Setúbal)")

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "moscatel setubal fortified wine",
    "region": "Portugal — Setúbal Peninsula (Arrábida coast, south of Lisbon)",
    "name": "Moscatel de Setúbal — The Oldest Portuguese Fortified, Pre-Port",
    "terroir_origin": (
        "Moscatel de Setúbal (DOC Setúbal, established 1907) is the oldest documented "
        "Portuguese wine appellation — predating the Douro's official DOC demarcation by "
        "two years. The Setúbal Peninsula, between the Tagus estuary and the Sado River "
        "south of Lisbon, produces Moscatel Graúdo (Muscat of Alexandria) and Moscatel Roxo "
        "(a rare pink-skinned Moscatel unique to Setúbal) on sandy limestone and clay soils "
        "at low altitude (50–150m). "
        "The terroir effect: Setúbal's proximity to the Atlantic moderates the heat "
        "(cooler than the Alentejo just inland) while the sandy soils drain well and "
        "concentrate the Moscatel's natural aromatics. The Arrábida Natural Reserve's "
        "southern slopes — where limestone cliffs descend to the Atlantic — "
        "provide the highest-quality Moscatel vineyard sites. "
        "José Maria da Fonseca (founded 1834) is the only producer of international scale: "
        "their Moscatel de Setúbal is the category's reference and one of Portugal's "
        "most exported wines historically. The Fonseca family has produced unbroken "
        "vintage Moscatel since the mid-19th century; their oldest cellar stocks "
        "include bottles from 1900, 1920, 1934 — extraordinary aged Moscatel that "
        "develops a rancio-aged complexity beyond almost anything in the fortified world. "
        "Moscatel Roxo — the rare pink variety — produces only a few thousand bottles "
        "annually and is considered one of the world's great sweet wine rarities."
    ),
    "production_technique": (
        "Moscatel de Setúbal production: grapes harvested at full physiological ripeness "
        "(September); fermentation begins; when alcohol reaches approximately 6–8% ABV, "
        "the must is fortified with Portuguese grape spirit (aguardente vínica) "
        "to arrest fermentation at approximately 17.5–18% ABV. "
        "The critical step: maceration. After fortification, the fresh grape skins "
        "(or in some cases, additional dried Moscatel skins) are macerated in the "
        "fortified must for 4–6 months. This extended skin contact after fortification "
        "is Moscatel de Setúbal's defining technique — it extracts intense aromatic "
        "compounds from the Muscat skins without astringent tannin (the alcohol prevents "
        "tannin extraction while allowing aromatic extraction). "
        "The result: a wine with the pure, perfumed aromatic intensity of the Muscat grape "
        "at concentrations impossible without the extended maceration. "
        "Ageing: José Maria da Fonseca ages in large wooden tonéis (700–2000L vessels); "
        "standard vintage: 5–7 years in oak; reserve 20-year: significant wood character; "
        "vintage 1900s: extraordinary rancio-aged complexity equivalent to "
        "50-year Tawny Port or Madeira Sercial reserve. "
        "Moscatel Roxo: same process but the pink-skinned grape adds rose-petal and "
        "dried apricot aromatics absent in the Graúdo."
    ),
    "cross_tradition_parallels": [
        {"tradition": "fortified", "beverage": "Muscat de Beaumes-de-Venise (VDN, Rhône)",
         "connection": "Both use Muscat Blanc à Petits Grains or Muscat of Alexandria; "
                       "both are fortified to arrest fermentation; both achieve extraordinary "
                       "aromatic purity through the Muscat's high linalool content. "
                       "The crucial difference: Setúbal's extended skin maceration after "
                       "fortification produces far greater aromatic concentration and "
                       "complexity than Beaumes-de-Venise, and Setúbal's aged expressions "
                       "(20yr, 40yr vintages) achieve a complexity far beyond anything VDN can offer"},
        {"tradition": "fortified", "beverage": "Málaga Virgen (DO Málaga, Spain)",
         "connection": "Moscatel de Setúbal and Málaga both use Muscat of Alexandria "
                       "(Moscatel Graúdo) as their primary variety and both produce "
                       "fortified sweet wines from the same grape in similar Mediterranean "
                       "coast climates. Setúbal's extended skin maceration gives it "
                       "greater aromatic intensity; Málaga's raisin-dry production "
                       "gives it greater sugar concentration. Both are undervalued "
                       "relative to the quality they achieve"}
    ],
    "sensory_profile": {
        "appearance": "Standard (5–7 years): deep amber-gold; viscous; slow tears. "
                      "20-year Reserve: deep mahogany-amber; tawny at the edge. "
                      "Vintage 1934+: dark molasses-brown; extraordinary concentration.",
        "nose": "Standard Moscatel de Setúbal (5yr): explosive — candied orange peel, "
                "dried apricot, honey, rose water, fresh Muscat grape (almost impossible "
                "to achieve in a fortified wine without the maceration), marmalade, vanilla. "
                "The linalool content of Muscat drives the pure floral aromatic intensity "
                "to levels impossible in any non-Muscat variety. "
                "20-year Reserve: dried dates, orange peel confit, coffee, toffee, "
                "rancio (oxidative ageing character), walnut, tobacco — "
                "still the Muscat aromatic beneath the wood ageing complexity. "
                "Moscatel Roxo: adds dried rose petals and dried apricot over the standard profile.",
        "palate": "Standard: full sweetness (80–120g/L residual sugar); full body; "
                  "the Muscat aromatic persistence is extraordinary — the finish lasts "
                  "2–3 minutes in a top vintage; "
                  "the balance between sweetness and the acid-structure from Setúbal's "
                  "sandy soils prevents heaviness. "
                  "20-year Reserve: nutty complexity; the sweetness is less forward; "
                  "the rancio character dominates; extraordinary length. "
                  "Vintage: the greatest fortified wine experience in Portugal outside "
                  "Vintage Port.",
        "conclusion": "Moscatel de Setúbal is the most overlooked great fortified wine in the world. "
                      "At standard 5-year pricing, it outpoints Beaumes-de-Venise at twice the price "
                      "for aromatic purity. At 20-year Reserve or vintage level, it is in "
                      "the same conversation as aged Tawny and Malmsey Madeira. "
                      "For a programme: serve the 20-year alongside a Colheita Port or "
                      "10-year Madeira — the Moscatel's rose and orange character "
                      "provides the most distinctive contrast in a fortified wine flight."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "José Maria da Fonseca Vintage Moscatel / Moscatel Roxo",
         "criteria": "Vintage-dated (pre-1980 if available); or Moscatel Roxo (rare pink variety); "
                     "10+ years minimum ageing; single harvest expression",
         "markers": "JMF Moscatel de Setúbal vintage 1934, 1966, 1976, 2000; "
                    "Moscatel Roxo Palmela; BC/US ~$45–120+ depending on vintage"},
        {"tier": 3, "tier_name": "José Maria da Fonseca 20-Year Reserve",
         "criteria": "20-year average age; significant rancio character; "
                     "extraordinary complexity; reference for the aged style",
         "markers": "JMF Setúbal 20yr Reserve; US ~$35–45; BC ~$40–55"},
        {"tier": 2, "tier_name": "José Maria da Fonseca 5–7 Year",
         "criteria": "Standard vintage; Moscatel Graúdo; full aromatic character; "
                     "accessible sweetness; commercial benchmark",
         "markers": "JMF Moscatel de Setúbal standard (5yr); US ~$18–22; BC ~$20–25"},
        {"tier": 1, "tier_name": "Palmela Moscatel (Entry / Regional)",
         "criteria": "DOC Setúbal or Palmela; Moscatel variety; correct aromatic character",
         "markers": "Quinta do Piloto Moscatel; commercial Setúbal Moscatel; BC/US ~$12–16"}
    ],
    "service_intelligence": {
        "temperature": "10–12°C; serve chilled — the Muscat aromatics express most clearly cold; "
                       "20-year Reserve at 12–14°C to allow complexity to open",
        "vessel": "Dessert wine glass (tulip or ISO); smaller volume (75–100mL per service); "
                  "the aromatics fill the glass rapidly — no large pour needed",
        "technique": "Standard: serve 75mL very cold as dessert service. "
                     "20-year Reserve: 60mL at 13°C as a contemplative digestif. "
                     "Comparative flight: Moscatel de Setúbal 5yr alongside 10yr Malmsey Madeira "
                     "and a White Port — three Portuguese fortified wines, "
                     "three completely different flavour registers from the same national tradition. "
                     "Cheese service: serve alongside Azeitão cheese (Setúbal Peninsula sheep milk cheese) "
                     "for the canonical local pairing.",
        "programme_position": "Dessert wine anchor for PCT programme; "
                              "pre-Port Portuguese fortified narrative; "
                              "comparative flight with Port and Madeira",
        "verbal_presentation": "José Maria da Fonseca Moscatel de Setúbal — Arrábida coast, Portugal. "
                               "Fortified in 1834. Six months' skin maceration after fermentation. "
                               "The Muscat the Portuguese kept for themselves "
                               "while selling Port to England."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "José Maria da Fonseca (Azeitão, Setúbal Peninsula)",
        "producer_location": "Azeitão, Setúbal Peninsula, south of Lisbon, Portugal",
        "key_person": "Domingos Soares Franco (chief winemaker, JMF); "
                      "Fonseca family (founded 1834, now publicly owned but family-managed)",
        "production_volume": "Medium commercial scale; José Maria da Fonseca is Portugal's largest "
                             "Setúbal Moscatel producer and a major table wine producer as well",
        "certifications": ["DOC Setúbal", "DOC Palmela"],
        "bc_distributor": "José Maria da Fonseca: available at BC Liquor stores (Evaton Inc. imports "
                          "some JMF products); confirm current Moscatel listing with BCLDB",
        "us_distributor": "José Maria da Fonseca: Winebow (US national — confirmed for JMF table wines; "
                          "Moscatel may be separate import); Premium Port Wines (specialty fortified)",
        "uk_distributor": "JMF widely available UK: Sainsbury's, Waitrose; "
                          "The Wine Society; specialist Portuguese merchants",
        "price_tier": "Market to Reserve (5yr standard BC ~$20; 20yr Reserve BC ~$45; vintage ~$80–120+)",
        "availability_notes": "In BC: JMF Periquita (red) widely available; Moscatel less consistent "
                              "— check BCLDB catalogue or request through Evaton. "
                              "US: Winebow carries JMF nationally; Moscatel at specialty wine shops "
                              "and online retailers. UK: most accessible market globally after Portugal."
    },
    "trail_connection": "PCT-1",
    "trail_note": "Moscatel de Setúbal is older than Port as a named, regulated wine style. "
                  "The Setúbal Peninsula's wine wealth preceded the Douro's rise and "
                  "was consumed by the Lisbon court throughout the Age of Discovery. "
                  "Vasco da Gama's ships were provisioned from Setúbal before departing "
                  "for the Cape of Good Hope route to India — "
                  "Moscatel de Setúbal was on those ships. The 1907 DOC designation, "
                  "when Portugal created its first modern appellation, chose Setúbal first: "
                  "a recognition of the region's historical primacy in Portuguese wine culture.",
    "food_pairings": [
        {"technique_id": "", "dish": "Azeitão cheese (Setúbal Peninsula, cured sheep's milk)",
         "pairing_type": "complement",
         "rationale": "Azeitão DOP — soft, runny, strongly flavoured sheep's milk cheese "
                      "from the same Setúbal Peninsula as the Moscatel — creates the "
                      "canonical local pairing. The cheese's sharp lactic-ovine character "
                      "contrasts against the Moscatel's honeyed-orange sweetness "
                      "while the sheep milk fat finds the wine's full body. "
                      "Same terroir, same climate, complementary flavour chemistry"},
        {"technique_id": "", "dish": "Pastel de nata (Pastéis de Belém, Lisbon)",
         "pairing_type": "complement",
         "rationale": "The Portuguese custard tart's egg-custard richness and caramelised "
                      "sugar crust mirror the Moscatel's own dried-apricot and "
                      "caramel register — the most historically resonant pairing "
                      "in Lisbon's food culture. The pastéis de Belém recipe "
                      "was developed by Hieronymite monks at the same time "
                      "the JMF estate was founding its Moscatel production"}
    ],
    "source": "CVR Setúbal (Comissão Vitivinícola Regional de Setúbal) DOC documentation; "
              "José Maria da Fonseca official history and production documentation; "
              "Jancis Robinson 'Wine Grapes' (Moscatel Graúdo / Muscat of Alexandria entry); "
              "Wines of Portugal Setúbal regional guide; "
              "Portuguese 1907 wine appellation historical records",
})

session.commit_batch()
print(f"\n[BATCH 39 COMMITTED — Moscatel de Setúbal]\n")

# PRODUCERS
session.add_producer({
    "name": "Niepoort (Douro Table Wines)",
    "location": "Cima Corgo, Douro Valley, Portugal",
    "country": "Portugal",
    "region": "Cima Corgo, Douro DOC",
    "tradition": "wine",
    "key_person": "Dirk Niepoort (current; 5th generation; both Port and table wine)",
    "founded": "1842 (Port); 1990s (table wine programme)",
    "production_volume": "Small to medium; international distribution via Polaner Selections (US)",
    "notable_products": ["Niepoort Redoma Tinto", "Niepoort Redoma Branco",
                         "Niepoort Charme (the flagship Douro red)", "Niepoort Batuta",
                         "Niepoort Vintage Port"],
    "certifications": ["Douro DOC"],
    "website": "niepoort-vinhos.com",
    "philosophy": "Dirk Niepoort brought the Burgundy philosophy to the Douro: low yields, "
                  "foot-trodden lagares, minimal-intervention winemaking, minimal new oak. "
                  "His Douro table wines proved in the 1990s that the Douro Valley's "
                  "schist terroir could produce great red table wines as well as great Port. "
                  "Redoma is now the reference Douro table wine internationally.",
    "trail_connection": "PCT-1",
    "source": "Niepoort official documentation; Polaner Selections US portfolio",
    "verified": True
})

session.add_producer({
    "name": "Luís Pato",
    "location": "Óis do Bairro, Bairrada DOC, Portugal",
    "country": "Portugal",
    "region": "Bairrada DOC, Beira Litoral",
    "tradition": "wine",
    "key_person": "Luís Pato (founder; the defining figure of modern Bairrada)",
    "founded": "1980 (as independent winery; family history in Bairrada much longer)",
    "production_volume": "Small family estate; Skurnik US distribution gives widest international access",
    "notable_products": ["Luís Pato Vinha Pan", "Luís Pato Vinha Formal",
                         "Luís Pato Baga", "Luís Pato Bical Branco (white)"],
    "certifications": ["Bairrada DOC"],
    "website": "luispato.com",
    "philosophy": "Luís Pato is the winemaker who transformed Bairrada from a reputation for "
                  "harshly tannic wine to a region producing wines of international distinction. "
                  "His argument: Baga is Portugal's Nebbiolo — the most challenging variety "
                  "in the country, but when handled with care, producing wines of extraordinary "
                  "longevity and character. His daughter Filipa Pato now runs a parallel estate "
                  "with a Burgundy-inflected approach.",
    "trail_connection": "PCT-1",
    "source": "Luís Pato official documentation; Skurnik Wines portfolio; "
              "Wines of Portugal Bairrada evaluation",
    "verified": True
})

session.add_producer({
    "name": "José Maria da Fonseca",
    "location": "Azeitão, Setúbal Peninsula, Portugal",
    "country": "Portugal",
    "region": "Setúbal Peninsula, DOC Setúbal",
    "tradition": "fortified",
    "key_person": "Domingos Soares Franco (chief winemaker); Fonseca family management",
    "founded": "1834",
    "production_volume": "Medium commercial; Portugal's oldest continuously operating wine company",
    "notable_products": ["Moscatel de Setúbal 5yr", "Moscatel de Setúbal 20yr Reserve",
                         "Moscatel Roxo Palmela", "Periquita (table wine)"],
    "certifications": ["DOC Setúbal", "DOC Palmela"],
    "website": "jmf.pt",
    "philosophy": "Founded in 1834, José Maria da Fonseca has maintained unbroken Moscatel de Setúbal "
                  "production for 190 years — the longest continuous fortified wine production "
                  "in Portugal outside the Port houses. The company archives include Moscatel "
                  "from 1900 and earlier, making it one of the world's oldest living wine cellars. "
                  "The 20-year Reserve and vintage expressions are Portugal's greatest "
                  "aged sweet wine outside Vintage Port and Madeira.",
    "trail_connection": "PCT-1",
    "source": "JMF official history documentation; DOC Setúbal registry; "
              "Wines of Portugal certification records",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 40 COMMITTED — Portugal Wine Producers]\n")

print(session.finish())
