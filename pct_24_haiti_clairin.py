import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Haiti — Artibonite and Grand Anse Departments (Clairin Single-Village Cane Spirits, Unaged)',
    output_dir='.',
    starting_entry=1,
    session_number=25,
    running_total=82
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Fritz Sajous — Clairin Sajous, Saint-Michel-de-l\'Attalaye',
    'location': 'Saint-Michel-de-l\'Attalaye, Artibonite Department, Haiti',
    'description': 'Fourth-generation distiller Fritz Sajous produces Clairin from sugar cane grown on 200 acres surrounding his family\'s distillery in the Artibonite Department — Haiti\'s agricultural heartland at 300–500m elevation in the central plateau. Sajous works with a local wild cane variety called "batterie" — a heritage heirloom variety maintained on the property without commercial hybrid introduction — and distills in a copper alembic pot still that Fritz reconstructed from his great-grandfather\'s original equipment. The Sajous production represents the "clean and fruity" end of the Clairin spectrum: relatively short fermentation (3–5 days), fresh cane character, and distillation at 55–58% ABV before immediate bottling without aging. Sajous was one of the original producers in the Velier-Luca Gargano Clairin project launched in 2012, which brought Haitian artisan cane spirits to international attention for the first time.',
    'founded': 'ca. 1900 (family tradition); current export label 2012',
    'region': 'Artibonite Department, Haiti',
    'website': None,
    'verified': False
})

session.add_producer({
    'tradition': 'spirits',
    'name': 'Chelo Bellizaire — Clairin Le Rocher, Cavaillon',
    'location': 'Cavaillon, Sud Department, Haiti',
    'description': 'Chelo Bellizaire produces Clairin Le Rocher from sugar cane grown in the Sud Department near Cavaillon, at lower elevation (50–150m) near Haiti\'s southern coast. Le Rocher (meaning "the rock") refers to the rocky limestone coastal terroir where Bellizaire\'s cane grows in shallow soils over exposed karst. The production style at Le Rocher is the most tropical and fruit-forward in the Clairin family: longer fermentation periods (8–12 days in open wooden vats), higher proportion of volatile esters from the humid coastal environment, and distillation at a lower cut point that preserves more of the heads-forward congener character. Le Rocher represents the "wild and intense" pole of Clairin production, contrasting with Sajous\'s cleaner style.',
    'founded': 'ca. 1940s (family tradition); export label from 2013',
    'region': 'Sud Department, Haiti',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Velier SpA — Clairin Series',
    'type': 'importer_bottler',
    'description': 'Velier\'s founder Luca Gargano initiated the Clairin documentation project in 2012 with field researcher Alexandre Vingtier, traveling to identify exceptional small-scale Haitian distillers producing artisan cane spirits that had never been exported. The resulting Clairin series — Sajous, Le Rocher, Casimir, Vaval, Vieux Labbé, and others — brought Haitian rural distillation tradition to the international spirits market for the first time. Velier distributes Clairin through its standard import channels: US through specialty importers by state; Canada through private import; UK through Master of Malt and Whisky Exchange.',
    'markets_served': ['EU', 'US', 'Canada', 'UK', 'Japan'],
    'traditions_carried': ['spirits'],
    'website': 'velier.it',
    'verified': True
})

session.add_beverage({
    'name': 'Clairin Sajous — Single-Village Unaged Haitian Cane Spirit, Artibonite Heritage Batterie Cane',
    'category': 'spirits',
    'subcategory': 'cane_spirit',
    'origin': 'Haiti',
    'region': 'Artibonite Department, Haiti',
    'producer': 'Fritz Sajous — Clairin Sajous, Saint-Michel-de-l\'Attalaye',
    'alcohol_content': 48.8,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Artibonite Department is Haiti\'s most productive agricultural zone — a high central plateau at 300–600m elevation, drained by the Artibonite River (the longest river in Hispaniola), with fertile alluvial soils and a reliable bimodal rainfall pattern. Saint-Michel-de-l\'Attalaye sits at the northern edge of the Artibonite plain where the plateau meets the Central Massif foothills, at approximately 450m elevation. Sajous\'s cane fields grow in deep red clay soils over basaltic parent rock — the same geological substrate that underlies much of the Haitian Central Plateau, contributing mineral depth through natural root uptake. The "batterie" cane variety cultivated by the Sajous family is a non-hybrid heritage cane strain maintained without commercial variety introduction for at least four generations. Heritage cane varieties accumulate distinctive volatile compound profiles from their specific soil and climate interactions that commercial Saccharum officinarum hybrids optimize away for yield rather than flavor. Haiti was once the wealthiest colony in the Americas (Saint-Domingue, to the French) — producing 40% of Europe\'s sugar and 60% of its coffee in 1789. The 1791 Haitian Revolution and 1804 independence created the conditions for the agricultural fragmentation that preserved artisanal cane spirit production: large plantation sugar monoculture was replaced by smallholder polyculture, with cane distilled for local clairin production rather than commercial export — an accidental preservation of heritage variety diversity and artisanal production methods that survived because Haiti never re-industrialized its agriculture.'
    ),
    'production_technique': (
        'Sajous harvests his batterie cane by machete at approximately 14 months growth — longer than commercial cane (10–12 months) to allow maximum sucrose concentration in the stalk. Harvested cane is crushed within 24 hours in a traditional three-roller cane press (moulin à canne) powered by a small diesel engine that replaced the original animal-powered mill. Fresh cane juice is collected directly in open wooden fermentation vats, with no clarification or sulfur addition. Wild yeast fermentation begins spontaneously within 2–4 hours from the wild Saccharomyces, Pichia, and Candida populations on the cane stalks and in the distillery environment. The Sajous fermentation runs 3–5 days — shorter than most Clairin producers — at ambient plateau temperature (24–28°C), producing a wash at 6–9% ABV with a characteristically clean, fruity profile. No dunder addition, no acidification, no temperature control. The wash is distilled in Fritz Sajous\'s copper alembic pot still in a single pass, taking hearts at approximately 55–70% ABV output. Sajous takes a wide hearts cut — wider than European spirits convention — to preserve the fruity complexity of the heads fraction that would normally be discarded. The resulting spirit is immediately reduced to bottling strength (48.8% for the Velier release) with pure spring water from the property and bottled without aging, filtration, or additive. Every bottle of Clairin Sajous represents a specific harvest season: the production volume is approximately 2,000–4,000 bottles per year, fully traceable to the property.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Rhum agricole AOC Martinique (Neisson Cuvée Speciale)',
            'connection': 'Both Clairin Sajous and rhum agricole are unaged single-territory fresh cane juice distillates that capture the botanical and mineral character of their specific cane variety and growing environment in transparent, unaged form — but Clairin is legally unregulated (no appellation) while rhum agricole operates within the most rigorous rum regulatory framework in the world: the contrast shows both the freedom and the risk of production without institutional oversight'
        },
        {
            'tradition': 'Natural wine (raw, unfiltered, terroir-first)',
            'connection': 'Clairin Sajous occupies the same philosophical position in rum as natural wine in the wine world: wild fermentation, no additives, no filtration, no standardization — each production is a snapshot of a specific year\'s cane crop fermented by the ambient yeast population of that property, making every batch unique and somewhat variable in the way that natural wine is variable'
        },
        {
            'tradition': 'Mezcal Tobaziche (heirloom agave variety, village production)',
            'connection': 'Clairin Sajous\'s heritage batterie cane variety, village-specific production, and artisanal pot still technique mirror the mezcal tradition of single-variety, single-producer expressions from named Mexican villages — both represent survival of pre-industrial agricultural distillation practices in rural communities that modernization and certification overlooked until connoisseur discovery brought international attention'
        }
    ],
    'sensory_profile': {
        'appearance': 'Crystal clear, water-white; zero color from the absence of aging; light viscosity at 48.8%; nothing to visually distinguish it from vodka — the character is entirely in the nose and palate',
        'nose': 'Bright and vivid: green cane, fresh-cut grass, unripe banana, ripe guava, lime zest, light floral freshness, distant agricultural note that reminds of the field rather than the distillery — more agricole rhum than Jamaican rum in aromatic architecture; remarkably clean for an unaged pot still spirit',
        'palate': 'Medium body, immediate cane sweetness, fresh tropical fruit, light floral mid-palate, moderate alcohol heat from 48.8%, clean finish with lingering green cane and guava — the "terroir of the cane" expression in its most direct form; the wide hearts cut adds a faint glycerol richness that rounds the finish'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Domestic Clairin (Village Direct)',
            'criteria': 'Unbranded clairin sold from the distillery in plastic bottles or recycled spirits bottles for local consumption — the base product of Haitian rural culture at sub-$5 per liter; variable quality, often 50–65% ABV from uncontrolled distillation cuts'
        },
        {
            'tier': 2,
            'tier_name': 'Clairin Sajous Annual Release (Velier Bottling)',
            'criteria': 'Fritz Sajous\'s Velier-bottled annual production — fully traceable, consistent process, harvest-variable character; the internationally accessible reference for the Artibonite terroir and batterie cane variety'
        },
        {
            'tier': 3,
            'tier_name': 'Clairin Sajous Special Edition',
            'criteria': 'Velier-selected exceptional harvest batches, sometimes aged briefly in ex-rum or ex-cognac wood, bottled at variable cask strength — released as named limited editions when the harvest produces distinctive character'
        },
        {
            'tier': 4,
            'tier_name': 'Clairin Sajous Vieux (Aged Reserve)',
            'criteria': 'Extended wood aging (1–3 years in small oak) producing Clairin\'s first "vieux" (aged) expression — an experiment in how the batterie cane terroir character transforms with wood contact; produced in quantities under 500 bottles; the frontier of the Sajous production evolution'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature (20–22°C) or a single small ice rock; Clairin Sajous\'s clean agricultural character benefits from slight dilution — 3–5ml water opens the green cane aromatics dramatically; avoid serving ice-cold which closes the tropical fruit complexity',
        'vessel': 'Clean tulip glass or nosing glass to concentrate the delicate green cane aromatics; wide-open wine glass acceptable but disperses the subtle floral notes faster; avoid Glencairn-style narrow opening which focuses the alcohol spike before the fruit follows',
        'cocktail_applications': 'Outstanding in Ti\' Punch (fresh lime, cane syrup, clairin over a single ice cube) — the classic Martinique cocktail formula works perfectly with Sajous; also excellent in Daiquiri where the clean cane character lets the citrus lead rather than competing; the Haitian cultural context makes it an exceptional spirit for restaurants serving Caribbean-inspired menus'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Fritz Sajous — Clairin Sajous via Velier SpA international bottling',
        'north_america_access': 'Clairin Sajous available through Velier US distribution (state-by-state importers); Astor Wines (NYC), K&L Wine Merchants (CA), Spec\'s (TX); Canada private import through specialty spirits retailers; limited BC Liquor listing as of 2024',
        'culinary_application': 'Sajous works as a base for Haitian-influenced cocktail programs in restaurants with Caribbean menus; the green cane character makes it an outstanding substitute for cachaça in Caipirinha variations with tropical fruit; Haitian culinary cultural narrative (revolution of 1791, oldest Black republic, agricultural smallholder tradition) provides powerful menu storytelling for provenance-focused restaurants'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('spirits', 'Haiti — Sud Department Cavaillon (Clairin Le Rocher, Wild Tropical, Limestone Coast)')

session.add_beverage({
    'name': 'Clairin Le Rocher — Wild Tropical Single-Village, Cavaillon Sud Haiti Limestone Coast',
    'category': 'spirits',
    'subcategory': 'cane_spirit',
    'origin': 'Haiti',
    'region': 'Sud Department, Haiti',
    'producer': 'Chelo Bellizaire — Clairin Le Rocher, Cavaillon',
    'alcohol_content': 51.4,
    'price_tier': 'premium',
    'terroir_origin': (
        'Cavaillon sits in Haiti\'s Sud Department on the southern peninsula, at approximately 100m elevation in a transitional zone between the coastal limestone plain and the interior Massif de la Hotte mountain range. The southern peninsula receives higher rainfall than the Artibonite plateau (1,800–2,200mm annually from Atlantic and Caribbean moisture) and maintains higher ambient humidity (75–85% RH) throughout the year. Bellizaire\'s cane fields occupy shallow red clay soils over exposed limestone karst — the "rocher" (rock) of the name refers to the visible limestone outcrops in the cane fields where bedrock breaks through the thin soil layer. This limestone karst drainage creates a distinct mineral quality in the water used for fermentation, contributing calcium and magnesium to the fermentation environment. The coastal location exposes the cane to sea breeze throughout the growing season, a maritime influence that contributes saline precursors to the cane\'s volatile compound profile. The combination of humid coastal environment, limestone terroir, and longer fermentation duration creates Le Rocher\'s distinctly wild, aromatic, and complex profile compared to the highland-cool, cleaner Sajous. Le Rocher demonstrates how the same production philosophy — unaged cane spirit, wild fermentation, pot still — produces fundamentally different spirits when applied to different Haitian microclimates and geological substrates.'
    ),
    'production_technique': (
        'Bellizaire harvests cane from his limestone-terrace fields in a single annual cutting (December–March), crushing immediately at a traditional moulin located on the property. The fresh juice is transferred to open wooden fermentation vats — larger than Sajous\'s — and left to ferment with wild yeast populations for 8–12 days: more than double the Sajous fermentation time. The extended fermentation at higher ambient humidity and temperature (28–34°C coastal range vs 24–28°C at Artibonite altitude) produces a dramatically different fermentation profile: higher volatile acidity from Acetobacter activity, more complex ester formation from the extended contact between yeast metabolites and organic acids, and a characteristic wild fruit-forward aromatics from Pichia and Candida yeast strains that thrive in the more tropical fermentation environment. Some batches show active co-fermentation with local wild flowers added to the fermentation vat — a traditional practice that adds floral terpene complexity to the wash. Distillation occurs in Bellizaire\'s copper pot still (smaller than Sajous\'s at approximately 500-litre capacity) in a direct-fire single distillation, with a slightly more aggressive heads fraction inclusion than Sajous — the Le Rocher house style deliberately captures more of the volatile heads character. Bottling at 51.4% for the Velier release without water addition to preserve the concentrated tropical intensity. Annual production is approximately 1,500–3,000 bottles, fully batch-identified.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Clairin Sajous (direct contrast within same tradition)',
            'connection': 'Le Rocher and Sajous are the defining contrast pair within the Clairin tradition: Sajous represents the clean, fruity, highland-cool expression at 3–5 day fermentation, while Le Rocher represents the wild, intense, coastal-humid expression at 8–12 day fermentation — the same unaged cane spirit philosophy producing dramatically different outcomes from different Haitian microclimates, like comparing two Burgundy villages from opposite ends of the Côte d\'Or'
        },
        {
            'tradition': 'Mezcal Tobaziche vs Tobalá (wild vs semi-wild agave)',
            'connection': 'The Clairin Sajous/Le Rocher contrast mirrors the mezcal wild vs cultivated agave spectrum: Tobaziche (wild-growing) produces intense, complex, terroir-specific mezcal while cultivated Espadín produces more consistent, accessible mezcal — both pairs show how the degree of "wildness" in the primary substrate directly translates to spirit complexity and variability'
        },
        {
            'tradition': 'Cachaça artesanal (Minas Gerais copper alembic)',
            'connection': 'Le Rocher\'s extended wild fermentation and immediate pot still distillation without aging share production principles with the finest Minas Gerais artisanal cachaça producers (Novo Fogo, Leblon artesanal) — both represent unaged fresh cane spirits where the fermentation duration and yeast diversity create the complexity that aging provides in commercial rum'
        }
    ],
    'sensory_profile': {
        'appearance': 'Crystal clear with a faint green-gold tint from extended fermentation congeners; slightly more viscous than Sajous at 51.4%; visible oil droplets when swirled in glass',
        'nose': 'Wild and complex: ripe tropical fruit (mango, guava, overripe banana), white flowers, earthy limestone mineral, light smoke from direct-fire distillation, fermented fruit (near-overripe intensity), sea salt-mineral in background — dramatically different from Sajous; the extra fermentation days are immediately apparent in the aromatic complexity',
        'palate': 'Full body, tropical fruit intensity, significant alcohol presence at 51.4%, complex mid-palate with simultaneous fruit sweetness and mineral-earth depth, long finish with limestone mineral and dried mango — a spirit that demands attention and rewards it with the most complex flavor journey in the Clairin range'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Domestic Clairin (Village Production)',
            'criteria': 'Unbranded village clairin from the Cavaillon area — the base product available locally without export traceability'
        },
        {
            'tier': 2,
            'tier_name': 'Clairin Le Rocher Annual (Velier Bottling)',
            'criteria': 'Chelo Bellizaire\'s Velier-bottled annual production at 51.4%, with harvest-year character variation as the primary quality variable — the international reference for southern Haiti coastal terroir'
        },
        {
            'tier': 3,
            'tier_name': 'Clairin Le Rocher Millesime (Selected Harvest)',
            'criteria': 'Exceptional harvest batches identified by Velier\'s Luca Gargano as representing peak Le Rocher terroir expression — limited to 1,000–2,000 bottles per identified batch'
        },
        {
            'tier': 4,
            'tier_name': 'Clairin Le Rocher Reserve',
            'criteria': 'The aspirational aged tier: Le Rocher\'s intensity in ex-bourbon or ex-rum wood would theoretically produce one of the Caribbean\'s most complex aged spirits — currently only experimental quantities exist, as Bellizaire\'s production is primarily oriented toward the fresh, unaged style'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature or with a single large ice rock for initial temperature reduction; the complexity of Le Rocher benefits from slow warming in the glass over 15–20 minutes — the evolving aromatic reveal as temperature rises is part of the tasting experience; at 51.4% it is strong enough to handle a small water addition (5–10ml) without losing character',
        'vessel': 'Wide tulip glass to contain and concentrate the complex floral-fruit-mineral aromatics without trapping the alcohol spike; the complexity rewards a wider bowl than spirits typically receive — a white Burgundy glass is ideal for exploring the full aromatic range',
        'service_context': 'Le Rocher\'s intensity makes it better as a contemplative single-spirit experience than a casual cocktail base — though it works brilliantly in Ti\' Punch where the lime acid cuts through the tropical intensity; for restaurant service, position it as the "exploration" spirit on a Caribbean spirits menu rather than the first pour'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Chelo Bellizaire — Clairin Le Rocher via Velier SpA',
        'north_america_access': 'Same Velier distribution as Clairin Sajous; slightly harder to find than Sajous due to lower production volume; Whisky Exchange online ships internationally; Clairin.com (Velier direct) lists current inventory; The Rum Howler (online specialist) carries the range',
        'culinary_application': 'Le Rocher\'s wild tropical intensity makes it challenging in food applications that require subtlety; works best in applications where its intensity IS the point — tropical punch reductions for dessert sauces, mango-clairin ceviche preparation where the raw cane wildness mirrors the fish\'s rawness, or as a finishing spirit in pineapple-based cocktails where its complexity reads as depth rather than competition'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
