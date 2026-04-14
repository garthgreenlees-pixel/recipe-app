import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='fortified',
    region='Portugal — Douro Valley (Colheita Port, Single-Vintage Tawny, Sandeman 1977, Extended Cask Aging)',
    output_dir='.',
    starting_entry=1,
    session_number=72,
    running_total=0
)

session.add_producer({
    'tradition': 'fortified',
    'name': 'Sandeman — Vila Nova de Gaia, Douro Valley',
    'location': 'Vila Nova de Gaia, Douro Valley, Portugal',
    'description': (
        'Sandeman is one of the founding Port shippers, established in 1790 by '
        'George Sandeman of Perth, Scotland — one of the earliest British Port '
        'trading houses in Vila Nova de Gaia and among the most recognizable '
        'Port brands in global markets through the distinctive "the Don" caped '
        'figure marketing identity. Sandeman operates significant vineyard '
        'holdings in the Douro Valley including Quinta do Seixo in the Pinhão '
        'Valley and sources from contracted growers across the Douro Superior, '
        'Cima Corgo, and Baixo Corgo sub-zones. The house is particularly known '
        'for its Colheita Port programme — extended single-vintage tawny Port '
        'aged in wood for minimum 7 years before release, with archive colheita '
        'expressions going back to the early 20th century. The 1977 Sandeman '
        'Colheita represents the house\'s Colheita programme at its mature '
        'peak — a single vintage aged in lodge barrels in Vila Nova de Gaia '
        'for decades before bottling, developing the characteristic amber-tawny '
        'color and rancio complexity that defines extended wood-aged Port.'
    ),
    'founded': '1790',
    'region': 'Vila Nova de Gaia, Porto, Portugal',
    'website': 'sandeman.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Sogrape Wines / Sandeman global distribution',
    'type': 'importer',
    'description': (
        'Sandeman is owned by the Sogrape group (Portugal\'s largest wine '
        'company) and distributed globally through the Sogrape/Sandeman '
        'international distribution network. In the United States, Sandeman '
        'is distributed through Enovation Brands, with the Colheita expressions '
        'available at specialist wine retailers and Port-focused wine shops. '
        'In Canada, BCLDB BC and LCBO Ontario carry Sandeman Colheita on '
        'regular allocation, with the 1977 and other historic colheita vintages '
        'available at auction and through specialist LCBO Vintages programme. '
        'The Colheita programme is Sandeman\'s most collectible Port category '
        'and the 1977 vintage — a declared Port vintage year of high quality — '
        'represents an accessible entry point to aged single-vintage Tawny '
        'Port at USD $60–100 per 750ml.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU', 'Global'],
    'traditions_carried': ['fortified'],
    'website': 'sandeman.com',
    'verified': True
})

session.add_beverage({
    'name': (
        'Sandeman Colheita 1977 — Single-Vintage Tawny Port, Extended Cask Aging, '
        'Douro Valley, Vila Nova de Gaia Lodge'
    ),
    'category': 'fortified',
    'subcategory': 'port_colheita',
    'origin': 'Portugal',
    'region': 'Portugal — Douro Valley (Colheita Port, Single-Vintage Tawny, Sandeman 1977, Extended Cask Aging)',
    'producer': 'Sandeman — Vila Nova de Gaia, Douro Valley',
    'alcohol_content': 20.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Colheita Port is sourced from the Douro Valley DOC — the steep schist '
        'valley of the Douro River in northeastern Portugal, 80–200km upstream '
        'from Porto, where the demarcated Port wine region occupies the '
        'terraced schist and granite hillsides at 100–700m elevation. The '
        'Douro Valley Port region is divided into three sub-zones: Baixo '
        'Corgo (westernmost, lowest quality), Cima Corgo (central, the heart '
        'of premium Port production centred on the Pinhão Valley), and Douro '
        'Superior (eastern, hottest, lowest rainfall, increasingly important '
        'for premium Port). Sandeman\'s 1977 Colheita fruit would have been '
        'sourced primarily from Cima Corgo — the Pinhão valley schist terraces '
        'at 200–500m elevation where the combination of extreme summer heat '
        '(35–40°C maximum), low rainfall (400–500mm annually), and the '
        'heat-retaining dark schist soil produces the dark, concentrated, '
        'high-alcohol base wine necessary for Colheita Port. The schist soil '
        'of the Douro is the single most important terroir factor in Port '
        'production: the fractured dark phyllite and schist retains minimal '
        'moisture, forces vine roots to penetrate 10–15 metres into the '
        'rock fissures seeking water and nutrients, and accumulates and '
        'radiates exceptional heat, achieving the extreme sugar concentrations '
        '(13–14% alcohol in the base wine before fortification) that define '
        'Port\'s power. The Gaia lodges where Colheita ages are at sea level '
        '(Vila Nova de Gaia, across the Douro from Porto) — the cool, '
        'maritime air from the Atlantic moderates the aging temperature '
        'versus the Douro Valley\'s extreme heat, producing a slower, '
        'more complex oxidative aging trajectory than Douro Valley-aged wine.'
    ),
    'production_technique': (
        'Colheita Port is a single-vintage tawny Port aged in wood for a minimum '
        'of 7 years before bottling — the critical distinction from Vintage Port '
        '(which ages in bottle) and from blended age-indicated Tawny (10, 20, 30, '
        '40-year, which are blends of multiple vintages). The 1977 Sandeman '
        'Colheita represents a 1977-harvest single vintage aged in the Sandeman '
        'Gaia lodge for decades in small 550L seasoned oak pipes (the traditional '
        'Douro Port barrel). The production chain is as follows: Douro Valley '
        'Touriga Nacional, Touriga Franca, Tinta Roriz, and Tinta Barroca '
        'grapes are foot-trodden in stone lagares at Quinta do Seixo and '
        'contracted Douro Valley estates, with 3–4 days of intensive skin '
        'contact maceration to extract maximum colour (4.0–6.0 g/L anthocyanins) '
        'before fortification with 77% ABV neutral grape spirit (aguardente '
        'vínica) — the fortification arresting fermentation at 6–8% ABV '
        'achieved, preserving 80–120 g/L residual grape sugar and producing '
        'a wine of 19–21% ABV. The fortified young wine is transported '
        'in January (the traditional "Barco Rabelo" river journey, now by '
        'tanker truck) to the Vila Nova de Gaia lodges where it enters '
        'the Colheita program: small 550L oak pipes for extended oxidative '
        'aging. The Colheita is never part of the solera or blending system '
        '— it remains as a single-vintage lot, tested and tasted annually '
        'by the winemaker to determine the bottling date. The 1977 vintage '
        'was of exceptional quality (declared by Port houses as a Vintage '
        'Port year), and the Colheita expression aged far beyond the minimum '
        '7 years — reaching its peak oxidative complexity after 30–40 years '
        'in barrel. The wine is bottled to order as a colheita with the '
        'bottling date on the label (a legal requirement for Colheita Port), '
        'and the label must state both the vintage year (1977) and the date '
        'of bottling — critical information for understanding how much '
        'additional bottle aging the wine has received. Colheita is not '
        'designed for further aging after bottling; it is ready at bottling '
        'date and should be consumed within 5–10 years of the bottling date.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Madeira Colheita (single-vintage oxidative barrel aging, bottling date mandatory)',
            'connection': (
                'Port Colheita and Madeira Colheita are direct structural parallels '
                'within the Portuguese fortified wine tradition: both are single-vintage '
                'expressions aged in wood for extended periods (minimum 7 years for '
                'Port Colheita; minimum 5 years for Madeira Colheita) before bottling '
                'to order; both carry mandatory bottling-date labeling; and both '
                'differ fundamentally from their respective blended age-indicated '
                'counterparts (Tawny 20-year; Madeira 20-year) in offering single-vintage '
                'traceability rather than solera-blended averages. The oxidative '
                'chemistry is identical: both develop amber-tawny color through '
                'anthocyanin breakdown and phenolic oxidation, rancio through ester '
                'development, and dried fruit and caramel through Maillard reactions '
                'in warm barrel conditions.'
            )
        },
        {
            'tradition': 'Vintage Port (same vintage declared, bottle-aged versus wood-aged)',
            'connection': (
                'The 1977 Port vintage was a declared vintage — the same year, '
                'the same Douro fruit, the same fortification method — but Vintage '
                'Port from 1977 and the 1977 Colheita represent two completely '
                'different aging philosophies from the same base material. Vintage '
                'Port ages in bottle: 2 years in lodge, then decades in bottle, '
                'developing the reduced, complex, primary-fruit-retaining character '
                'of reductive bottle aging. Colheita ages in barrel: decades of '
                'oxidative wood contact that strips the primary fruit character and '
                'replaces it with the tawny, rancio, dried-fruit oxidative register. '
                'The same 1977 harvest thus produces two completely different wines '
                'depending on the aging pathway — making the 1977 vintage a '
                'unique teaching tool for the distinction between oxidative '
                'and reductive aging in fortified wine.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Tawny amber with orange-gold rim — the defining visual marker of '
            'extended oxidative barrel aging; the deep ruby-garnet of the '
            '1977 harvest has been completely transformed over decades in barrel '
            'through anthocyanin breakdown and oxidative browning into the '
            'characteristic tawny-amber of a mature Colheita; the color intensity '
            'is greater than blended 20-year Tawny due to the single-vintage '
            'concentration; brilliant clarity from filtration before bottling; '
            'viscous legs from 19–20% ABV and 80–100 g/L residual sugar.'
        ),
        'nose': (
            'Dried fig and apricot as the primary fruit register — the '
            'red fruit of the 1977 Douro harvest completely transformed '
            'by decades of oxidative aging into concentrated dried fruit; '
            'rancio (oxidative walnut oil, hazelnut) from the long ester '
            'development in seasoned oak pipes; honey and beeswax from '
            'the interaction of high residual sugar and oxidative environment; '
            'orange peel and caramel from the Maillard browning of sugars '
            'during barrel aging; beneath these oxidative registers, a '
            'mineral schist character from the Douro terroir that survives '
            'even extreme oxidative aging; the integration of the fortification '
            'spirit is complete — no raw alcohol character remains after '
            '40+ years in barrel.'
        ),
        'palate': (
            'Medium-sweet with excellent balancing acidity; the dried fig, '
            'apricot, and raisin register from the nose carries through '
            'the entry and mid-palate; rancio and hazelnut from the oxidative '
            'complexity building through the mid-palate; very long finish '
            '(60–90 seconds) from the combination of sugar concentration, '
            'rancio ester complexity, and the Douro tannin that has softened '
            'through decades of oxidative barrel transformation but still '
            'provides structural backbone; the schist mineral of the Douro '
            'terroir persists as a dry, earthy persistence on the '
            'finish — the only dimension of the 1977 Douro origin that '
            'remains perceptible after the oxidative transformation.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Standard Colheita (7-10 years wood aging, minimum legal requirement)',
            'criteria': (
                'Colheita Port bottled at or just after the minimum 7-year wood '
                'aging requirement; the tawny color still shows orange-garnet '
                'hues from incomplete oxidative transformation; the rancio '
                'character is present but not fully developed; dried fruit '
                'character beginning to replace primary red fruit; the least '
                'complex expression of the Colheita style.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Medium-aged Colheita (15-25 years wood aging, full tawny development)',
            'criteria': (
                'Colheita aged 15–25 years in barrel before bottling; fully '
                'developed tawny-amber color; complete rancio character; '
                'dried fruit and caramel at full intensity; the '
                'Douro terroir mineral beginning to emerge from beneath '
                'the oxidative complexity; the optimal commercial tier '
                'for Colheita quality, balancing oxidative development '
                'with retained structural backbone.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Long-aged Colheita (30+ years wood aging, Sandeman 1977 tier)',
            'criteria': (
                'Colheita aged 30–40+ years in barrel; the apex of tawny '
                'oxidative complexity with maximum rancio and dried fruit '
                'concentration; the Sandeman 1977 represents this tier — '
                'a wine from a declared vintage year aged far beyond minimum '
                'requirements; the Douro terroir schist mineral character '
                'survives even at this oxidative intensity as a dry, earthy '
                'persistence; extremely rare category with limited production '
                'as most houses bottle earlier.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Archive Colheita (50+ years, pre-war vintages, collector tier)',
            'criteria': (
                'Historic Colheita from pre-1960s vintages held in lodge archives '
                'at Sandeman, Graham\'s, or Niepoort — the ultra-rare apex of '
                'the Colheita category with documented 50–70+ year aging records; '
                'at this level the wine has transcended the dried fruit register '
                'into extraordinary rancio and mineral complexity with almost no '
                'residual primary fruit character; comparable in scarcity and '
                'collector positioning to pre-war Madeira colheita expressions '
                'from D\'Oliveiras archive; pricing USD $300–1,000+ per bottle.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Colheita Port 1977 at 14–16°C — slightly cooler than room '
            'temperature to preserve the delicate rancio and dried fruit '
            'aromatic complexity, which volatilizes rapidly above 18°C; do '
            'not chill below 12°C as the viscosity of the residual sugar '
            'becomes texturally dominant and the rancio aromatic register '
            'is suppressed at lower temperatures. After opening, Colheita '
            'Port is stable for 4–8 weeks if recorked and kept cool — '
            'unlike Vintage Port, Colheita has already completed its '
            'oxidative aging and is not further improved by additional '
            'air exposure; serve all in one evening or within 2–3 days '
            'of opening for optimal aromatic expression.'
        ),
        'vessel': (
            'Serve in a Port copita (traditional 80–100ml tulip glass) or '
            'a small-format white wine tulip; pour 60–80ml per service; '
            'the narrow aperture of the copita concentrates the rancio '
            'and dried fruit aromatic intensity above the wine surface; '
            'present with the label visible showing both the 1977 vintage '
            'date and the bottling date — these two dates together communicate '
            'the entire aging biography of the wine and merit a verbal '
            'explanation to the guest; the Colheita style is frequently '
            'misunderstood as blended Tawny Port and the distinction '
            '(single vintage, specific wood-aging duration, mandatory '
            'bottling date) requires direct table explanation.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Sandeman — Vila Nova de Gaia (1790; benchmark Colheita programme '
            'with archive vintages going back to the early 20th century); '
            'also: Niepoort (the most celebrated Colheita specialist in Porto, '
            'with archive Colheita going back to the 1870s); Graham\'s (1820; '
            'strong Colheita archive); Ramos Pinto (Colheita specialist with '
            'consistent quality across multiple declared vintages). The 1977 '
            'vintage is also available as Colheita from Ramos Pinto and '
            'Borges, offering direct comparison between house styles '
            'from the same exceptional harvest year.'
        ),
        'north_america_access': (
            'Sandeman Colheita 1977 is available through specialist Port wine '
            'retailers in the United States at USD $60–100 per 750ml — the '
            'price reflecting the rarity of the 1977 vintage colheita rather '
            'than exceptional scarcity, as Sandeman continues to bottle '
            '1977 to order from the lodge reserve. LCBO Vintages programme '
            'and BCLDB specialty wine carry selected Sandeman Colheita '
            'vintages. Niepoort Colheita (available at specialist Portuguese '
            'wine retailers in US and Canada) is the recommended quality '
            'comparison point for trade buyers evaluating the Colheita style.'
        ),
        'culinary_application': (
            'Colheita Port 1977 is the canonical Port style for cheese service '
            '— specifically with aged sheep\'s milk cheese (Manchego reserva, '
            'Pecorino stagionato, Portuguese Queijo Serrano) where the rancio '
            'and dried fruit character of the Colheita mirrors the nutty, '
            'crystalline character of long-aged hard sheep\'s milk cheese. '
            'The combination works because both the cheese and the Colheita '
            'share the same oxidative flavour development pathway: extended '
            'aging under controlled oxidative conditions producing rancio, '
            'crystallized amino acids (in the cheese), and dried fruit '
            'concentration in the wine.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
