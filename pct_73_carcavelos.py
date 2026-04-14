import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='fortified',
    region='Portugal — Cascais (Carcavelos DOC, Quinta dos Pesos, Fortified White, Near-Extinct Appellation, Atlantic Suburban)',
    output_dir='.',
    starting_entry=1,
    session_number=77,
    running_total=0
)

session.add_producer({
    'tradition': 'fortified',
    'name': 'Quinta dos Pesos — Carcavelos, Cascais, Lisboa',
    'location': 'Carcavelos, Cascais Municipality, Lisboa, Portugal',
    'description': (
        'Quinta dos Pesos is one of the last surviving producers of Carcavelos '
        'DOC — a near-extinct fortified wine appellation on the Estoril Coast '
        'west of Lisbon. The quinta has maintained production of the Carcavelos '
        'DOC wine against the sustained pressure of Lisbon suburban development '
        'that has eliminated nearly all the historic vineyard land of the '
        'Carcavelos appellation. At its peak in the 18th and 19th centuries, '
        'Carcavelos was an important Portuguese fortified wine traded through '
        'the colonial system to Brazil, Angola, and Mozambique — the Marquês '
        'de Pombal (who rebuilt Lisbon after the 1755 earthquake) owned '
        'vineyards at Carcavelos and promoted the wine commercially as a '
        'Portuguese colonial product. The appellation now covers fewer than '
        '5 hectares of producing vineyard — compared to the hundreds of '
        'hectares that existed before the Estoril railway line and the '
        'subsequent suburban development of the Cascais corridor in the '
        '20th century. Quinta dos Pesos is the only producer with '
        'consistent DOC production and commercial availability.'
    ),
    'founded': '18th century (modern winery era from 1990s)',
    'region': 'Carcavelos DOC, Cascais, Lisboa, Portugal',
    'website': 'quintadospesos.pt',
    'verified': True
})

session.add_purveyor({
    'name': 'Portuguese specialist importers / Wines of Portugal network',
    'type': 'importer',
    'description': (
        'Carcavelos DOC is among the rarest and hardest-to-source Portuguese '
        'wines in any market — the total DOC production of fewer than '
        '5 hectares makes it a specialist niche even within Portugal. '
        'Quinta dos Pesos distributes primarily through the domestic '
        'Portuguese market (Lisbon wine shops and restaurants). '
        'International distribution is extremely limited — occasional '
        'specialist Portuguese wine importers in the UK (Justerini & '
        'Brooks, Yapp Brothers) and the United States have listed '
        'Carcavelos DOC on special allocation. For North American '
        'professional buyers, the wine is primarily a research and '
        'education reference rather than a commercially sourceable '
        'programme wine, though specialist allocation through '
        'Wines of Portugal trade contacts can be arranged.'
    ),
    'markets_served': ['Portugal', 'UK'],
    'traditions_carried': ['fortified'],
    'website': 'quintadospesos.pt',
    'verified': False
})

session.add_beverage({
    'name': (
        'Quinta dos Pesos Carcavelos DOC — Near-Extinct Atlantic Fortified White, '
        'Arinto and Galego Dourado, Estoril Coast, Pre-Colonial Heritage Wine'
    ),
    'category': 'fortified',
    'subcategory': 'carcavelos',
    'origin': 'Portugal',
    'region': 'Portugal — Cascais (Carcavelos DOC, Quinta dos Pesos, Fortified White, Near-Extinct Appellation, Atlantic Suburban)',
    'producer': 'Quinta dos Pesos — Carcavelos, Cascais, Lisboa',
    'alcohol_content': 18.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Carcavelos DOC occupies the narrow coastal plain between the '
        'Serra de Sintra granite and the Atlantic Ocean at Carcavelos village '
        'in the Cascais municipality, 15km west of Lisbon at sea level to '
        '50m elevation. The surviving vineyard land of Quinta dos Pesos is '
        'on sandy limestone and clay soil with direct Atlantic influence — '
        'the Atlantic Ocean is less than 2km distant, and the persistent '
        'westerly winds and Atlantic fog from the Estoril Coast moderate '
        'temperatures year-round (mean summer temperatures of 20–22°C, '
        'significantly cooler than Lisbon\'s 26–28°C). The sandy-limestone '
        'coastal soil, similar in texture to Colares DOC further north '
        'on the Sintra Peninsula, provides the warm, well-draining '
        'conditions that the white Carcavelos grape varieties require '
        'for full sugar development: Galego Dourado (the primary '
        'Carcavelos DOC variety, permitted only in this DOC), '
        'Arinto, Boal de Alicante, Ratinho, and Torneiro. The '
        'surviving vineyard area at Quinta dos Pesos has been reduced '
        'to fewer than 3 hectares by the surrounding suburban '
        'infrastructure — the quinta is now an island of active '
        'viticulture within the fully urbanized Cascais corridor, '
        'a situation that makes the continuing DOC production more '
        'an act of heritage preservation than commercial viticulture. '
        'Historic Carcavelos was produced from much larger vineyard '
        'areas that once covered the Estoril Coast between Carcavelos '
        'village and the Tagus estuary — virtually all eliminated '
        'between 1950 and 1990 by residential and commercial development.'
    ),
    'production_technique': (
        'Carcavelos DOC production at Quinta dos Pesos follows the '
        'traditional Portuguese fortified white wine method, producing '
        'a medium-dry to medium-sweet fortified wine of 18–20% ABV '
        'from the distinctive blend of Atlantic coastal white varieties. '
        'Galego Dourado — the indigenous variety permitted only in '
        'the Carcavelos DOC — is the backbone of the blend, providing '
        'the characteristic nutty, almond character that distinguishes '
        'Carcavelos from Setúbal Moscatel and Douro White Port. '
        'The grapes are harvested in late September at 12–13% '
        'potential alcohol when the Atlantic coastal conditions '
        'have achieved full sugar ripeness; foot-treading or '
        'pneumatic pressing produces a free-run and first-press '
        'juice blend that ferments at 18–20°C until 7–8% ABV '
        'is achieved. Fortification with 77% ABV aguardente '
        'vínica arrests fermentation, preserving 60–90 g/L '
        'residual sugar and producing the 18–20% ABV Carcavelos '
        'DOC wine. Aging takes place in old seasoned oak toneis '
        '(300–600L) for a minimum of 6 months under the DOC '
        'regulations, but Quinta dos Pesos typically ages the '
        'Carcavelos 12–18 months before bottling to develop '
        'the characteristic amber color and the nutty-almond '
        'Galego Dourado complexity. The wine is bottled without '
        'age statement and in 375ml or 500ml formats consistent '
        'with Portuguese fortified wine tradition. The very '
        'limited production (fewer than 5,000 bottles annually) '
        'makes Carcavelos DOC one of the smallest-production '
        'legally denominated fortified wines in Europe, '
        'surpassed in rarity only by wines from similarly '
        'near-extinct appellations such as Málaga DOC in Spain.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Colares DOC Ramisco (near-extinct Portuguese Atlantic DOC, heritage preservation)',
            'connection': (
                'Carcavelos DOC and Colares DOC are the twin near-extinct '
                'Atlantic-coast Portuguese wine appellations — both located '
                'on the Sintra and Estoril coastline west of Lisbon, both '
                'eliminated by suburban development from much larger historic '
                'production areas, and both surviving in a single-producer '
                'or single-cooperative format that constitutes the last '
                'commercial production of their respective DOC wines. '
                'Colares survives because of its sandy phylloxera-resistant '
                'soil; Carcavelos survives because of the determination of '
                'a single quinta (Quinta dos Pesos) within the fully urbanized '
                'Cascais corridor. Both wines are heritage preservation '
                'projects as much as commercial wine production — the '
                'DOC designations maintained by the surviving producer '
                'as a matter of historical record against the economic '
                'logic of suburban land value that makes vineyard '
                'maintenance in Cascais and Sintra functionally uneconomic.'
            )
        },
        {
            'tradition': 'Málaga DO Moscatel (Spanish near-extinct fortified, urban encroachment, single producer)',
            'connection': (
                'Carcavelos DOC and Málaga DO represent parallel cases of '
                'once-important colonial-era fortified wine appellations '
                'that were severely reduced by 20th-century urban expansion '
                'around major Iberian port cities (Lisbon; Málaga). Both '
                'were significant fortified wine exports through the '
                'respective colonial trade systems in the 18th and 19th '
                'centuries; both lost the majority of their vineyard land '
                'to suburban development; and both survive primarily '
                'through the efforts of individual producers committed '
                'to maintaining the DOC/DO designation as a heritage '
                'category. The parallel demonstrates a wider pattern of '
                'urban encroachment on historically significant wine '
                'territories that has affected Atlantic-coast European '
                'wine DOCs disproportionately relative to inland '
                'wine regions with lower land values.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Amber-gold with orange highlights — the characteristic color '
            'of 12–18 months in old oak toneis; lighter than Tawny Port '
            'at equivalent aging due to the white variety base (no red '
            'fruit anthocyanins to break down); brilliant clarity after '
            'light filtration; medium viscosity from the 60–90 g/L '
            'residual sugar and 18–20% ABV; the amber-gold color '
            'with orange highlights is the defining visual marker '
            'of correctly aged Carcavelos DOC at the Quinta dos '
            'Pesos production standard.'
        ),
        'nose': (
            'Roasted almond and walnut as the primary aromatic register — '
            'the Galego Dourado variety\'s characteristic nutty character '
            'that distinguishes Carcavelos from other Atlantic Portuguese '
            'fortified wines; beneath the almond-walnut, orange peel '
            'and dried citrus from the Arinto component; caramel and '
            'toffee from the barrel aging and the natural sugar '
            'concentration; a distinctive Atlantic salt-iodine '
            'quality from the proximity of the vineyard to the '
            'Estoril Coast; honey from the high residual sugar; '
            'the aromatic profile is closer to an Amontillado Sherry '
            'or Malmsey Madeira than to Setúbal Moscatel, due to '
            'the nutty-caramel register of Galego Dourado rather '
            'than the terpene-floral Muscat aromatic foundation.'
        ),
        'palate': (
            'Medium-sweet to medium-dry (60–90 g/L residual sugar) '
            'with bright Atlantic acidity from the Arinto component '
            'balancing the fortification sweetness; the roasted almond '
            'and walnut character from the nose carrying through the '
            'entry and mid-palate; orange peel and caramel building '
            'toward the finish; the Atlantic salt-mineral character '
            'threading through the mid-palate; medium to long '
            'finish from the sugar concentration and the nutty '
            'Galego Dourado persistence; the fortification spirit '
            'warming but fully integrated; the overall palate '
            'profile is the closest Portuguese approximation to '
            'an aged Amontillado or dry Oloroso in the fortified '
            'white wine register — demanding, mineral, and '
            'structurally coherent despite the unconventional DOC context.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Historic commercial Carcavelos (pre-1970s large-scale production)',
            'criteria': (
                'The lost commercial-scale Carcavelos production from the '
                'era when the DOC covered hundreds of hectares; historic '
                'records describe a wine of medium-sweet fortified '
                'character traded through the Portuguese colonial '
                'system to Brazil, Mozambique, and Angola; the wine '
                'at large scale before the vineyard losses of '
                'suburban expansion was a reliable colonial fortified '
                'product rather than a collector or artisan wine.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Quinta dos Pesos standard Carcavelos DOC (current production)',
            'criteria': (
                'The surviving DOC production from fewer than 3 hectares '
                'at Quinta dos Pesos; 12–18 months in old oak toneis; '
                'the Galego Dourado nutty character and Atlantic mineral '
                'at standard commercial expression; fewer than 5,000 '
                'bottles annually; the reference expression for the '
                'Carcavelos DOC at the only reliable commercial source '
                'currently available.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Extended-aged Carcavelos (3+ years toneis, reserve selection)',
            'criteria': (
                'Selected lots from Quinta dos Pesos with 3+ years of '
                'barrel aging in old seasoned oak; greater amber development '
                'and rancio complexity; the nutty-caramel register at '
                'full expression; extremely limited production within '
                'an already tiny DOC; the reserve tier of Carcavelos '
                'DOC production that demonstrates the aging potential '
                'of the Galego Dourado variety at extended wood contact.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Historic Carcavelos archive bottles (pre-1960s, collector documentation)',
            'criteria': (
                'Pre-1960s Carcavelos bottles from the historic peak '
                'production era — a collector-documentation category '
                'rather than a commercially available wine; surviving '
                'examples exist in Portuguese wine archives, the '
                'Wines of Portugal museum collection, and specialist '
                'Portuguese wine auction; these bottles represent '
                'the historical evidence that Carcavelos was once '
                'a serious commercial fortified wine category with '
                'colonial-era global distribution.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Carcavelos DOC at 12–14°C — the medium-sweet sugar '
            'concentration and Atlantic mineral character are best '
            'expressed at slightly below room temperature, where '
            'the nutty-almond Galego Dourado aromatics are most '
            'volatile and the Atlantic salt-mineral quality is most '
            'perceptible; above 16°C the fortification spirit '
            'becomes dominant and the delicate nutty character is '
            'obscured; serve as a digestif or as an aperitif '
            'before a formal Portuguese dinner programme where '
            'the historical significance of the DOC is part '
            'of the educational context; stable after opening '
            'for 4–6 weeks recorked and refrigerated.'
        ),
        'vessel': (
            'Serve in a small white wine tulip (150ml format) with '
            '60–80ml pour; the nutty-caramel aromatic profile '
            'benefits from a wider aperture than a Port copita — '
            'the Amontillado-like aromatic register of Carcavelos '
            'requires more surface area to express than the denser '
            'rancio of Tawny Port; present with the full historical '
            'context of the near-extinct DOC, the Galego Dourado '
            'variety found nowhere else in the world, and the '
            'Marquês de Pombal colonial heritage — the wine '
            'is as much a historical document as a sensory '
            'experience, and the professional presentation '
            'should reflect both dimensions.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Quinta dos Pesos — Carcavelos, Cascais (the only commercially '
            'active producer of Carcavelos DOC with consistent availability; '
            'without Quinta dos Pesos, the Carcavelos DOC would cease '
            'commercial production; the quinta is the sole guardian of '
            'the Galego Dourado variety in its natural Atlantic coastal '
            'habitat and the only source for the DOC wine in professional '
            'trade).'
        ),
        'north_america_access': (
            'Carcavelos DOC is not commercially available through regular '
            'North American distribution channels due to its extremely '
            'limited production. Professional buyers seeking Carcavelos '
            'for educational or collector purposes should contact '
            'Quinta dos Pesos directly through the Wines of Portugal '
            'trade network or through specialist Portuguese wine '
            'importers in the UK (Justerini & Brooks, Yapp Brothers) '
            'who occasionally source Carcavelos on special allocation. '
            'The wine is primarily a trade education reference — '
            'the defining example of a once-important fortified '
            'wine DOC reduced to near-extinction by urban expansion.'
        ),
        'culinary_application': (
            'Carcavelos DOC is the canonical pairing with Lisbon '
            'pastry culture — particularly the almond and egg '
            'custard pastry of the Cascais and Sintra coast '
            '(queijada de Sintra, tarte de amêndoa) where the '
            'nutty-almond Galego Dourado character of the wine '
            'creates a direct flavour echo in the almond pastry '
            'shell. The Atlantic mineral-saline character also '
            'functions as an aperitif alongside fresh Atlantic '
            'shellfish and grilled sardines from the Cascais '
            'fishing fleet — the salt-mineral bridge between '
            'the wine and the Atlantic seafood of the '
            'Estoril Coast is the most historically '
            'authentic pairing for the DOC.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
