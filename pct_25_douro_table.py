import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Portugal — Douro Superior and Cima Corgo (Niepoort Batuta, Field Blend Red, Douro Table Wine)',
    output_dir='.',
    starting_entry=1,
    session_number=26,
    running_total=84
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Niepoort Vinhos',
    'location': 'Porto and Quinta de Napoles, Cima Corgo, Douro Valley, Portugal',
    'description': 'Fifth-generation Dutch-Portuguese family wine house founded 1842, based in Porto with estate vineyards throughout the Douro Valley. Niepoort is simultaneously one of Portugal\'s most important Port producers and the most influential pioneer of Douro table wine — the family\'s embrace of dry red and white wine production from ancient Douro vines began in the 1990s and helped define the modern Douro as a world-class table wine region. Dirk Niepoort, current managing director and winemaker, is responsible for transforming the estate\'s direction toward unfortified wines while maintaining the Port legacy. Niepoort\'s table wine portfolio includes Batuta (the flagship red from pre-phylloxera schist vineyards), Charme (field blend red), Redoma (white and red), and the Twisted series for accessible drinking. The estate has become a pilgrimage destination for wine professionals studying the intersection of Port and table wine tradition in the Douro schist landscape.',
    'founded': '1842',
    'region': 'Douro Valley, Portugal',
    'website': 'niepoort-vinhos.com',
    'verified': True
})

session.add_producer({
    'tradition': 'wine',
    'name': 'Quinta do Vale Meão',
    'location': 'Douro Superior, Portugal (near the Spanish border)',
    'description': 'The most historically important estate in the Douro Superior — the upper, most extreme zone of the Douro Valley. Quinta do Vale Meão was the original property of the Ferreira family, the most powerful 19th-century Douro wine dynasty, and was the source of the grapes for Barca Velha — Portugal\'s first and most iconic Douro table wine, produced from 1952 to 1991 when the estate changed hands. The Olazabal family (Francisco de Olazabal), who acquired the property from A.A. Ferreira in 1998, immediately began producing their own wine — Quinta do Vale Meão — which quickly became one of Portugal\'s most sought-after reds. The estate sits at the far eastern extreme of the Douro at 400–600m elevation near the Barca de Alva crossing into Spain, in a climate far more extreme than the western Douro: summer temperatures reach 40–45°C and winter temperatures drop to -5°C, with annual rainfall under 400mm in severe drought years.',
    'founded': '1877 (Ferreira era); Olazabal era 1998',
    'region': 'Douro Superior, Portugal',
    'website': 'quintadovalemeao.pt',
    'verified': True
})

session.add_purveyor({
    'name': 'Quintessential Wines (US) / Broadbent Selections (UK) — Douro Portfolio',
    'type': 'importer',
    'description': 'Quintessential Wines handles Niepoort US import; Broadbent Selections handles UK. Quinta do Vale Meão is imported in the US by Kysela Père et Fils. Both estates are widely available through leading US and Canadian wine retailers at premium pricing. In BC Canada, Niepoort and Vale Meão are available through the BCLDB and private import channels.',
    'markets_served': ['US', 'Canada', 'UK', 'EU'],
    'traditions_carried': ['wine'],
    'website': 'quintessentialwines.com',
    'verified': False
})

session.add_beverage({
    'name': 'Niepoort Batuta — Pre-Phylloxera Field Blend Red, Cima Corgo Douro Superior Schist',
    'category': 'wine',
    'subcategory': 'red_wine',
    'origin': 'Portugal',
    'region': 'Cima Corgo, Douro Valley, Portugal',
    'producer': 'Niepoort Vinhos',
    'alcohol_content': 13.5,
    'price_tier': 'super_premium',
    'terroir_origin': (
        'Batuta is produced from a single pre-phylloxera vineyard plot in the Cima Corgo subzone of the Douro Valley — the central and most classically regarded of the three Douro subzones, where steep schist slopes above the Douro River produce the most concentrated expression of Portuguese red varieties under extreme continental climate conditions. The schist (xisto) bedrock that defines the Douro\'s viticultural character is a metamorphic rock formation created by intense heat and pressure applied to ancient marine sediments over 500 million years: the resulting rock fractures vertically rather than horizontally, allowing vine roots to penetrate to depths of 10–15 meters following fracture planes toward deep subsoil water. This root depth — essential for vine survival in the Douro\'s summer drought (under 400mm annual rainfall in drier years) — creates the mineral complexity that defines Douro red wine. The vineyards for Batuta are ungrafted pre-phylloxera field blends: original Douro varieties growing on their own rootstocks, planted before 1880 before phylloxera forced grafting onto American rootstock. These ungrafted vines — Touriga Nacional, Touriga Franca, Tinta Roriz (Tempranillo), Tinta Barroca, Tinto Cão and many others — co-exist in the same rows in proportions determined by who planted them more than a century ago. The field blend is harvested and vinified together, preserving the ecological complexity of the original planting rather than creating a "laboratory blend" of separately fermented varieties. Niepoort identifies Batuta\'s terroir through the concept of "geological memory" — the schist composition, soil depth, and fracture pattern of the specific vineyard plot embedded in the wine through root mineral uptake over more than 100 years of vine-soil interaction.'
    ),
    'production_technique': (
        'Batuta grapes are harvested by hand from the ungrafted field-blend vineyard in late September to early October, when Dirk Niepoort judges the combination of sugar, acid, and phenolic maturity rather than any individual parameter. The field blend is harvested together (all varieties co-harvested from the mixed planting), sorted by hand twice, and destemmed with partial whole-cluster inclusion (20–30% whole clusters, varying by vintage) before transfer to open-top lagares — the traditional Douro flat granite fermentation troughs where foot-treading was historically used to extract color and tannin. Niepoort uses foot treading (pisa) for Batuta as a deliberate choice: the gentle, variable pressure of human feet extracts phenolics at lower intensity than mechanical pumping or pigeage, producing finer tannin structure and preserving more of the delicate aromatic compounds. Fermentation occurs with indigenous yeast populations over 10–14 days at 26–30°C, with daily foot-treading sessions for the first 7–8 days. Extended maceration post-fermentation continues for 3–5 additional weeks to extract secondary phenolic complexity from the schist-influenced skins and seeds. Malolactic fermentation proceeds naturally in spring. Aging occurs in small (225–500 litre) used French oak barrels for 18–24 months — no new oak, as Dirk Niepoort believes new wood destroys the schist mineral signature. Batuta is bottled unfined and unfiltered after barrel aging, requiring 5–10+ years of bottle aging before reaching optimum expression. Annual production ranges from 3,000–8,000 bottles depending on vintage quality and yield.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Burgundy Premier Cru Pinot Noir (pre-phylloxera vineyard character)',
            'connection': 'Batuta\'s ungrafted pre-phylloxera field blend parallel the theoretical ideal of pre-phylloxera Burgundy — wine from vines growing on their own roots in limestone-clay, expressing the vineyard\'s geological character through direct root-mineral interaction rather than filtered through American rootstock grafting; both represent what European viticulture was before 1870'
        },
        {
            'tradition': 'Barolo from Serralunga d\'Alba (Nebbiolo on schist-limestone, austere structure)',
            'connection': 'Batuta\'s austere structure in youth, long aging requirement, and eventual emergence into complex tertiary-mineral-fruit integration mirrors the arc of great Barolo from Serralunga\'s compact limestone-clay soils — both wines reward decades of patience and reveal the geological character of their schist/limestone parents progressively with bottle age'
        },
        {
            'tradition': 'Vintage Port (same vineyard, fortified expression)',
            'connection': 'Batuta is the table wine expression of the same vineyard ecology that produces Niepoort\'s vintage Port — demonstrating how the Douro\'s ungrafted schist terroir expresses itself with and without fortification, and how the addition of brandy spirit in Port preserves aromatic freshness while removing the tannin arc that makes Batuta structurally demanding'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep ruby-garnet with purple tint in youth; brick-garnet rim at 10+ years; medium opacity appropriate to the multiple varieties; significant legs from 13.5% on polished glass',
        'nose': 'In youth: dark cherry, crushed schist mineral, violet, dried rosemary, black pepper, high aromatic tension from polyphenol concentration — the nose is powerful but closed; at 8–10 years: the schist mineral emerges dominant (wet slate, graphite), cherry transforms to dried plum and leather, spice becomes warm and integrated',
        'palate': 'Full body, structured tannin (grippy and drying in youth, silky at 10+ years), dark fruit core, high natural acidity from Douro continental climate, long finish with schist mineral and iron — a wine that communicates its geological identity more clearly than almost any other Portuguese red'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Niepoort Twisted (entry) / Redoma',
            'criteria': 'Accessible expressions of Niepoort\'s Douro sourcing philosophy — younger vines, commercial yeast, new oak components — introducing the house character without the complexity investment of Batuta'
        },
        {
            'tier': 2,
            'tier_name': 'Niepoort Charme',
            'criteria': 'Field blend red from identified old-vine plots, pre-phylloxera percentage, indigenous yeast, neutral barrel aging — the step below Batuta in specificity and intensity, available at premium rather than super-premium pricing'
        },
        {
            'tier': 3,
            'tier_name': 'Niepoort Batuta',
            'criteria': 'The flagship: single ungrafted pre-phylloxera vineyard, foot treading, extended maceration, no new oak — the fullest geological expression of the specific Cima Corgo schist plot; requires 5–10+ years aging to show full character'
        },
        {
            'tier': 4,
            'tier_name': 'Niepoort Batuta Rarissima',
            'criteria': 'Exceptional vintage selection (only declared in outstanding years), single barrel or micro-batch from the oldest vine sections of the Batuta vineyard — production under 1,000 bottles, priced at collector level'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 18–20°C — slightly warmer than most reds to open the schist mineral aromatics; young Batuta (under 7 years) benefits from 2–3 hours decanting to soften tannin; mature Batuta (8+ years) can be served directly from bottle with 30 minutes air',
        'vessel': 'Large Burgundy or Bordeaux format glass — the tannin structure needs the oxygen contact of a wide bowl; do not use the smaller decanting vessels appropriate for aged Burgundy, as Batuta\'s higher tannin concentration requires more generous aeration',
        'decanting_philosophy': 'Dirk Niepoort recommends standing Batuta upright for 24 hours before service to allow natural sediment to settle; decant slowly over a candle flame, stopping at the first sign of sediment — the older the vintage, the more careful the decanting required'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Niepoort Vinhos — Batuta is the benchmark Douro table wine for schist mineral terroir expression',
        'north_america_access': 'Niepoort through Quintessential Wines (US national); widely available in NY, CA, BC Canada; LCBO Ontario carries several Niepoort wines; Vancouver wine shops (Liberty Wine Merchants, Marquis Wine Cellars) stock Batuta by special order',
        'culinary_application': 'Batuta\'s schist mineral-iron character creates exceptional harmony with blood-forward preparations: Portuguese caldo verde with chouriço, lamb chops with rosemary on schist rock slab, foie gras torchon where the iron-mineral wine mirrors the liver\'s metallic intensity; for PNW application: aged Duck Confit, beef tartare, venison loin — preparations where the schist mineral register becomes part of the flavor experience'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('wine', 'Portugal — Douro Superior (Quinta do Vale Meão, Barca Velha Legacy, Continental Extreme)')

session.add_beverage({
    'name': 'Quinta do Vale Meão Red — Douro Superior Continental Extreme, Barca Velha Legacy Estate',
    'category': 'wine',
    'subcategory': 'red_wine',
    'origin': 'Portugal',
    'region': 'Douro Superior, Portugal',
    'producer': 'Quinta do Vale Meão',
    'alcohol_content': 14.5,
    'price_tier': 'super_premium',
    'terroir_origin': (
        'Quinta do Vale Meão occupies 130 hectares of schist slopes in the Douro Superior — the easternmost and most extreme subzone of the Douro Valley, near the Spanish border at Barca de Alva. The Superior is the most challenging viticulture zone in Portugal: summer temperatures regularly exceed 40°C (often reaching 45°C in heat waves), winter temperatures drop below -5°C, annual rainfall averages 300–450mm (among the lowest in any European wine region), and the schist slopes are among the steepest in the Douro (30–60% gradient). The estate sits at 400–600m elevation above the Douro River, where the river gorge channeling creates thermal variation between the river bottom (extreme heat) and the upper terraces (cooler by 5–8°C). The specific schist formation at Vale Meão is the "Bateiras" schist — a blue-grey metamorphic rock that weathers into extremely thin, fast-draining soils of 15–30cm depth overlying deep fracture-accessible bedrock. Vine root systems penetrate 8–12m into the schist to reach deep moisture reserves, creating the concentrated, mineral-laden must that defines the Vale Meão wine. The estate is historically significant as the source of Barca Velha grapes from 1952–1991 — Portugal\'s first and most iconic Douro red table wine — produced by Ferreira winemaker João Nicolau de Almeida, whose work here established that the Douro could produce great unfortified red wine long before this was understood internationally.'
    ),
    'production_technique': (
        'Vale Meão\'s harvest occurs in September — earlier than western Douro estates despite higher latitude, because the extreme continental heat of the Superior forces faster sugar accumulation and earlier physiological maturity. Francisco de Olazabal\'s team harvests by hand on steep schist terraces where mechanical access is impossible, carrying baskets to tractor roads every 200–400m of horizontal distance. The estate grows Touriga Nacional, Touriga Franca, Tinta Roriz, Tinta Barroca, and Sousão as identified individual varieties (unlike Niepoort\'s unmapped field blend). Each variety is harvested and vinified separately in stainless steel tanks at controlled temperature (22–26°C) for variety-specific extraction — Touriga Nacional runs 25 days of maceration; Tinta Roriz runs 18 days for aromatic freshness; Sousão runs 12 days to contribute color without excess tannin. The varieties are blended after primary fermentation, with the Olazabal team tasting across vintages to maintain the estate\'s characteristic concentration-with-freshness balance despite the extreme Superior climate. Malolactic fermentation occurs naturally in spring. Aging in 225-litre French oak barrels, 30–40% new oak per vintage — more new oak than Batuta, reflecting the Vale Meão style of slightly more structured, oaked architecture to contain the Superior\'s power. Bottle aging of 5–8 years minimum recommended before peak expression; the wine regularly shows complexity at 15–20 years.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Ribera del Duero Gran Reserva (Vega Sicilia, same river basin)',
            'connection': 'Quinta do Vale Meão and Vega Sicilia share the same geological river basin — the Douro/Duero River — separated by the Portuguese-Spanish border at Barca de Alva. Both produce the region\'s benchmark red wines from extreme continental continental climates, with Tempranillo-dominant blends aged in French oak, producing wines of exceptional concentration and longevity; the border has created regulatory separation but not terroir separation'
        },
        {
            'tradition': 'Penfolds Grange (Australian Shiraz, extreme heat concentration)',
            'connection': 'Vale Meão Red and Penfolds Grange occupy the same global category of extreme-climate red wines of uncompromising concentration — both produced in environments that push vines to survival extremes (40°C+ in both cases), both requiring significant aging, both representing the pinnacle of their national wine traditions in terms of structure and longevity'
        },
        {
            'tradition': 'Barca Velha (same estate, historical predecessor)',
            'connection': 'Vale Meão Red is the direct continuation of the Barca Velha tradition: same estate, same schist terroir, same varieties, but under new ownership (Olazabal rather than Ferreira) and with a more consistent annual release philosophy than the highly selective Barca Velha declarations (only 13 declared vintages in 40 years)'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep opaque ruby-purple in youth; slow clearing to garnet with 10+ years of aging; concentrated pigment visible from thick extract; significant viscous legs from 14.5% alcohol and high glycerol',
        'nose': 'In youth: blackberry, cassis, schist minerality, dense new oak (vanilla, cedar from barrel), dark chocolate, dried violets — opulently concentrated; at 10 years: iron-mineral emerges alongside dried fig, plum, tobacco, leather, fading but persistent fruit — a wine that shows its terroir more in age than in youth',
        'palate': 'Full-bodied (Vale Meão\'s most complete expression), massive tannic structure in youth that requires 8+ years to integrate, extraordinary concentration of extract and phenolics from the extreme Superior heat, long finish with schist mineral, iron, and dried dark fruit — the most powerful table wine in Portugal\'s portfolio'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Meandro do Vale Meão (second wine)',
            'criteria': 'The estate\'s second wine from younger vine selections and cooler vineyard plots — accessible expression of the Vale Meão terroir at premium pricing without the longevity expectation of the flagship'
        },
        {
            'tier': 2,
            'tier_name': 'Quinta do Vale Meão Standard Release',
            'criteria': 'The estate flagship: full blend of estate varieties, 30–40% new French oak, 5+ year aging recommended — the internationally distributed benchmark of Douro Superior wine'
        },
        {
            'tier': 3,
            'tier_name': 'Quinta do Vale Meão Selected Vintages',
            'criteria': 'Exceptional vintage declarations from years where the extreme Superior climate produces concentrated yet balanced fruit — Francisco de Olazabal\'s selection of the best barrels for extended cellaring beyond the standard release'
        },
        {
            'tier': 4,
            'tier_name': 'Barca Velha (A.A. Ferreira legacy / no longer produced from this estate)',
            'criteria': 'The historical tier: Barca Velha (now produced by Sogrape from non-Vale Meão grapes) represents the original benchmark that established the estate\'s global significance; collectors seek pre-1998 Barca Velha bottles from the original Vale Meão grapes as the historical maximum expression of the estate\'s terroir potential'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 18–20°C with 3–4 hours decanting for wines under 10 years old; mature expressions (10+ years) can be served with 1 hour decanting; the exceptional tannin structure requires generous oxygen exposure before palate assessment',
        'vessel': 'Large Bordeaux format glass or dedicated Douro Superior decanter — the concentration of Vale Meão requires more oxygen contact than lighter Douro wines; allow 20 minutes of glass exposure before initial assessment as the aromatics need significant time to open',
        'aging_philosophy': 'Vale Meão rewards cellar investment more than almost any other Portuguese table wine: at 5 years it is impressive but tight; at 10 years it shows the schist mineral fully integrated; at 20 years it produces a tertiary complexity (truffled earth, iron, dried fruit, tobacco) that represents the high-altitude extreme continental terroir at its most complete expression'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Quinta do Vale Meão — the benchmark Douro Superior red and successor to the Barca Velha legacy',
        'north_america_access': 'Kysela Père et Fils handles US import; available at Crush Wine (NYC), K&L Wine Merchants (CA), Wine Access (online); in Canada through LCBO and BCLDB by special order; the wine\'s extraordinary aging potential makes it a compelling restaurant cellar investment',
        'culinary_application': 'Vale Meão\'s power and concentration makes it the natural partner for the most robust preparations in the PNW repertoire: dry-aged côte de boeuf, bone marrow preparations, mushroom-truffle risotto where the iron-schist register resonates with the earthy umami; the Douro Superior extremity makes it work with the most aggressively flavored game birds — grouse, ptarmigan, woodcock — where the wine\'s structural authority matches rather than overwhelms'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
