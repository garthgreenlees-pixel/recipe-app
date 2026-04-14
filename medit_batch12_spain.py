#!/usr/bin/env python3
"""Batch 12 — Spain: Rioja/Ribera/Priorat (25 targets) + Sherry (15 targets)
Producers: Vega Sicilia, Pingus, La Rioja Alta, Muga, Lopez de Heredia, Alvaro Palacios,
           Clos Erasmus, Bodegas Protos; Sherry: Lustau, Hidalgo La Gitana, Equipo Navazos,
           Gonzalez Byass, Bodegas Tradicion
Products: Vega Sicilia Unico, Pingus, Rioja Gran Reserva, Muga Prado Enea, Lopez de Heredia,
          L'Ermita, Priorat Clos Erasmus; Sherry: Manzanilla La Gitana, Amontillado Napoleon,
          Palo Cortado, Oloroso, Fino Tio Pepe, PX San Emilio, Equipo Navazos La Bota
References: Sherry Solera and Style Spectrum; Tempranillo and Rioja Aging Classifications
Pairings: jamon iberico, cochinillo, patatas bravas, tapas, Arzak-style
Protocols: Sherry service with tapas
"""
import sys
sys.path.insert(0, "/Users/garthgreenlees/Desktop/provenance-tester-1")
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

# Spanish region IDs from batch1:
# Rioja=175, Ribera del Duero=176, Priorat=177, Jerez=178
RIOJA = 175
RIBERA = 176
PRIORAT = 177
JEREZ = 178

print("\n=== SPANISH WINE PRODUCERS ===")

vega_sicilia = P(cur, "Vega Sicilia",
    producer_type="winery", region_id=RIBERA, country="Spain",
    production_philosophy="conventional",
    philosophy_description=(
        "Vega Sicilia is Spain's most prestigious wine estate — founded in 1864 in Valbuena "
        "de Duero and producing Unico, Spain's most celebrated and age-worthy red wine. "
        "Unico is a blend of Tempranillo with a proportion of Cabernet Sauvignon, aged "
        "minimum 10 years before release (Tinto Fino 60%, Cabernet Sauvignon 24%, Merlot and others). "
        "The estate is owned by the Álvarez family and also produces Valbuena 5, "
        "Pintia (Toro), and Alion (Ribera del Duero)."
    ),
    key_personnel=["David Alvarez", "Pablo Alvarez", "Gonzalo Larrea (cellar master)"],
    production_details={
        "founded": 1864,
        "key_wines": ["Unico (10+ years aging, limited releases)", "Valbuena 5 (5 years)", "Alion (Ribera)"],
        "unico_grapes": "Tempranillo 60%, Cabernet Sauvignon 24%, Merlot + others",
        "unico_aging": "minimum 10 years before release (oak + bottle)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Vega Sicilia Unico is Spain's most iconic wine — collected internationally. "
        "The estate pioneered premium Spanish wine before the modern boom. "
        "Limited allocation; BC through specialist importers."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

pingus = P(cur, "Dominio de Pingus",
    producer_type="winery", region_id=RIBERA, country="Spain",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Peter Sisseck (a Danish winemaker) arrived in Ribera del Duero in 1995 and "
        "found ancient, ungrafted Tempranillo vines of extreme age (60-100+ years) "
        "growing in the village of La Horra. His first vintage of Pingus (1995) "
        "received 96-100 points internationally and became a sensation. "
        "The wine is made in tiny quantities (500-800 cases) from these exceptional old vines, "
        "biodynamically farmed, with minimal intervention."
    ),
    key_personnel=["Peter Sisseck"],
    production_details={
        "founded": 1995,
        "key_wines": ["Pingus (500-800 cases)", "Flor de Pingus (second wine)"],
        "vine_age": "60-100+ year old ungrafted Tempranillo",
        "farming": "biodynamic (Demeter certified)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Pingus is Spain's most prestigious wine by wine critic consensus. "
        "Ultra-limited; commands Petrus-level prices globally."
    ),
    allocation_notes="Ultra-allocation; BC importer [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

rioja_alta = P(cur, "La Rioja Alta",
    producer_type="winery", region_id=RIOJA, country="Spain",
    production_philosophy="conventional",
    philosophy_description=(
        "La Rioja Alta is one of Rioja's founding estates (1890) and the definitive "
        "address for the traditional Rioja Gran Reserva style. Their Viña Ardanza Reserva "
        "and Gran Reserva 890 / 904 are benchmarks for the Rioja aging hierarchy. "
        "The house is committed to long barrel aging in American oak — creating the "
        "vanilla-coconut-cedar character that defines classic Rioja."
    ),
    key_personnel=["Julio Saenz (CEO)"],
    production_details={
        "founded": 1890,
        "key_wines": ["Gran Reserva 890", "Gran Reserva 904", "Vina Ardanza Reserva"],
        "oak": "American oak — creating vanilla-coconut Rioja character",
        "style": "traditional — long aging in American oak"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "La Rioja Alta is the reference for traditional Rioja Gran Reserva. "
        "Gran Reserva 890 is one of Spain's most age-worthy wines. Good BC distribution."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

muga = P(cur, "Bodegas Muga",
    producer_type="winery", region_id=RIOJA, country="Spain",
    production_philosophy="conventional",
    philosophy_description=(
        "Muga in Haro (Rioja Alta) is the most craft-focused of Rioja's traditional houses — "
        "the only major bodega that still makes its own barrels. Their wines are aged in "
        "American oak (traditional) and French oak (modern expressions). "
        "Prado Enea Gran Reserva is the flagship — only produced in great years; "
        "one of Rioja's most elegant and complex traditional wines."
    ),
    key_personnel=["Isaac Muga", "Jorge Muga"],
    production_details={
        "founded": 1932,
        "key_wines": ["Prado Enea Gran Reserva", "Torre Muga", "Aro"],
        "unique": "only major Rioja bodega that makes own barrels in-house",
        "oak": "American + French oak combination"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Muga is beloved among sommeliers for craft quality and consistency. "
        "Prado Enea is a benchmark traditional Rioja. Strong BC distribution."
    ),
    allocation_notes="BC — Mark Anthony Group [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

lopez_de_heredia = P(cur, "Lopez de Heredia",
    producer_type="winery", region_id=RIOJA, country="Spain",
    production_philosophy="conventional",
    philosophy_description=(
        "Lopez de Heredia in Haro is the most extreme traditional Rioja producer — "
        "wines aged for extraordinary periods in barrel before release. Their Vina Tondonia "
        "Gran Reserva is aged 6+ years in barrel and several more in bottle before "
        "commercial release. When purchased, the wine is already 10-15 years old. "
        "The result is one of Spain's most extraordinary wines — complex, oxidative, "
        "and utterly unique. Also exceptional: Vina Gravonia white (Viura, aged similarly)."
    ),
    key_personnel=["Maria Jose Lopez de Heredia"],
    production_details={
        "founded": 1877,
        "key_wines": ["Vina Tondonia Gran Reserva", "Vina Gravonia (white)", "Vina Bosconia"],
        "aging": "6+ years in barrel + several years bottle before release",
        "style": "most traditional and oxidative style in Rioja"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Lopez de Heredia is one of Spain's most important wine estates — producing "
        "Spain's most extreme traditional wines. Vina Tondonia is a benchmark for "
        "sommeliers studying oxidative aging and traditional Rioja."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

alvaro_palacios = P(cur, "Alvaro Palacios",
    producer_type="winery", region_id=PRIORAT, country="Spain",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Alvaro Palacios transformed Priorat from an obscure, abandoned wine region "
        "to one of Spain's greatest in a single decade (1989-2000). Working with "
        "Rene Barbier, he founded Clos Mogador and then his own estate, producing "
        "L'Ermita — from ancient Garnacha vines on llicorella (slate-mica schist) soils. "
        "L'Ermita is Spain's most expensive wine and one of the world's great reds. "
        "Also produces Finca Dofi, Les Terrasses, and Camins del Priorat."
    ),
    key_personnel=["Alvaro Palacios"],
    production_details={
        "founded": 1989,
        "key_wines": ["L'Ermita (Garnacha old vines)", "Finca Dofi", "Les Terrasses"],
        "l_ermita": "ancient Garnacha on llicorella (slate-mica schist) — Spain's most expensive wine",
        "farming": "biodynamic"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Alvaro Palacios is the person most responsible for Priorat's renaissance. "
        "L'Ermita from old-vine Garnacha on slate is among the world's great red wines."
    ),
    allocation_notes="Ultra-limited; BC allocation [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

print("\n=== SPANISH WINE PRODUCTS ===")

unico = PROD(cur, "Vega Sicilia Unico",
    category="wine_still", producer_id=vega_sicilia, region_id=RIBERA,
    subcategory="red",
    description=(
        "Vega Sicilia Unico is Spain's most prestigious red wine — a Tempranillo-based blend "
        "aged a minimum 10 years before release. The wine is known for extraordinary structure "
        "and longevity — great vintages age 40-50 years. It is released in non-consecutive "
        "years depending on quality; each release carries a vintage year and a release year. "
        "The style blends Tempranillo's cherry-tobacco character with Cabernet Sauvignon's "
        "structure and aging potential."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Spain's most prestigious red wine",
        "aging_potential": "40-60 years",
        "release": "minimum 10 years from vintage"
    }],
    deductive_profile={
        "appearance": "deep garnet-ruby",
        "nose": "black cherry, cedar, tobacco, vanilla-oak, leather, dried flower",
        "palate": "full body, polished tannin, exceptional length, 40+ second finish",
        "signature": "Spanish power with French-inspired structure — unique national treasure"
    },
    service_specs={
        "temperature": "17-18C",
        "decanting": "2-3 hours",
        "aging": "already released at 10 years; peaks 20-40 years from vintage"
    },
    flavour_markers=["black cherry", "cedar", "tobacco", "vanilla oak", "leather", "dried flower"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$600-$1200+",
    technical_specs={
        "grape": "Tempranillo 60%, Cabernet Sauvignon 24%, Merlot+others",
        "appellation": "Ribera del Duero DO",
        "aging": "minimum 10 years (American + French oak + bottle)"
    })

pingus_wine = PROD(cur, "Dominio de Pingus Pingus",
    category="wine_still", producer_id=pingus, region_id=RIBERA,
    subcategory="red",
    description=(
        "Pingus is made from 500-800 cases per year from ancient ungrafted Tempranillo vines "
        "in La Horra, biodynamically farmed. The wine has extraordinary concentration, "
        "complexity, and aging potential — regularly scoring 99-100 points from international critics. "
        "The 1995 vintage put Peter Sisseck (and Ribera del Duero) on the world map. "
        "Extremely limited; prices rival Petrus and DRC."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Spain's most trophy wine by critics",
        "aging_potential": "30-50 years",
        "production": "500-800 cases per year"
    }],
    deductive_profile={
        "nose": "blackberry, dark plum, tobacco, cedar, mineral, subtle oak",
        "palate": "extraordinary concentration, dense tannin, exceptional length",
        "signature": "old-vine Tempranillo on slate soils — Spanish wine at its most extreme"
    },
    service_specs={"temperature": "17C", "decanting": "3-4 hours", "aging": "15-40 years"},
    flavour_markers=["blackberry", "dark plum", "tobacco", "cedar", "slate mineral"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$800-$1500+",
    technical_specs={
        "grape": "Tinto Fino (Tempranillo) 100%",
        "vine_age": "60-100+ years old, ungrafted",
        "appellation": "Ribera del Duero DO"
    })

muga_prado_enea = PROD(cur, "Muga Prado Enea Gran Reserva",
    category="wine_still", producer_id=muga, region_id=RIOJA,
    subcategory="red",
    description=(
        "Prado Enea Gran Reserva is Muga's only wine eligible for the Gran Reserva designation — "
        "made only in great years. Aged a minimum 3 years in oak (American, French, and local "
        "oak — Muga makes its own barrels) and 3 years in bottle before release. "
        "The result is one of Rioja's most elegant and long-lived expressions — complex, "
        "more restrained than some, with extraordinary secondary character."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "designation": "Gran Reserva — made only in great vintages",
        "aging": "3+ years oak + 3+ years bottle",
        "aging_potential": "20-30 years"
    }],
    deductive_profile={
        "nose": "cherry, dried rose, vanilla, leather, tobacco, light American oak spice",
        "palate": "elegant, medium-full body, firm tannin, long spice finish",
        "signature": "Rioja Grand Reserva elegance — vanilla-cherry with traditional oak"
    },
    service_specs={"temperature": "17C", "decanting": "1-2 hours", "aging": "optimal 8-20 years"},
    flavour_markers=["cherry", "dried rose", "vanilla", "leather", "tobacco", "spice"],
    flavour_weight="medium-full",
    flavour_profile_type="oak-aged traditional",
    price_tier="premium",
    price_range_cad="$120-$200",
    technical_specs={
        "grape": "Tempranillo 80%, Garnacha, Mazuelo, Graciano",
        "appellation": "Rioja DOCa Gran Reserva",
        "oak": "American + French (Muga-made barrels)"
    })

vina_tondonia_gr = PROD(cur, "Lopez de Heredia Vina Tondonia Gran Reserva",
    category="wine_still", producer_id=lopez_de_heredia, region_id=RIOJA,
    subcategory="red",
    description=(
        "Vina Tondonia Gran Reserva is one of the world's great traditional wines — "
        "aged 6+ years in barrel and several more in bottle before release. "
        "When purchased, the wine is already 10-15 years old. "
        "The oxidative barrel aging creates complex secondary character: "
        "leather, tobacco, dried rose, and a haunting savory depth unlike any other wine. "
        "It represents the apex of the traditional Rioja aging philosophy."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "aging": "6+ years barrel + bottle aging — released 10-15 years after harvest",
        "style": "most traditional and oxidative Rioja producer",
        "aging_potential": "20-40 years from purchase"
    }],
    deductive_profile={
        "appearance": "orange-brick rim; mahogany at maturity",
        "nose": "dried cherry, leather, tobacco, cedar, dried rose, savory herbs, subtle oxidation",
        "palate": "light-medium body, silky tannin, extraordinary secondary complexity",
        "signature": "oxidative Rioja — the most complex and traditional expression; Burgundy comparison"
    },
    service_specs={
        "temperature": "16-17C (slightly cooler — complex wine shows better)",
        "decanting": "1 hour (paradoxically — already complex)",
        "note": "the wine is already aged when released — do not store for more than 10-15 years"
    },
    flavour_markers=["dried cherry", "leather", "tobacco", "dried rose", "cedar", "savory herb"],
    flavour_weight="medium",
    flavour_profile_type="oxidative aged",
    price_tier="premium",
    price_range_cad="$100-$180",
    technical_specs={
        "grape": "Tempranillo 75%, Garnacha, Graciano, Mazuelo",
        "appellation": "Rioja DOCa Gran Reserva",
        "aging": "6+ years American oak barrel"
    })

l_ermita = PROD(cur, "Alvaro Palacios L'Ermita",
    category="wine_still", producer_id=alvaro_palacios, region_id=PRIORAT,
    subcategory="red",
    description=(
        "L'Ermita is Spain's most expensive wine — made from tiny quantities of ancient "
        "Garnacha vines (50-100+ years old) on llicorella (slate-mica schist) terraces "
        "above the village of Gratallops in Priorat. The slate soils impart extraordinary "
        "mineral complexity and translucency; the old vines concentrate the essential "
        "Garnacha character: dark fruit, liquorice, and a floral spice unique to old Garnacha. "
        "Aged in French oak (50% new); only 400-600 cases produced annually."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Spain's most expensive wine — old-vine Garnacha",
        "production": "400-600 cases",
        "aging_potential": "30-50 years"
    }],
    deductive_profile={
        "appearance": "deep ruby-garnet",
        "nose": "dark cherry, liquorice, black olive, slate mineral, dried violet, dark spice",
        "palate": "enormous but translucent — concentration with mineral precision",
        "signature": "llicorella slate mineral + old Garnacha = the essence of Priorat"
    },
    service_specs={"temperature": "17C", "decanting": "3-4 hours", "aging": "15-40 years"},
    flavour_markers=["dark cherry", "liquorice", "black olive", "slate mineral", "dried violet"],
    flavour_weight="full",
    flavour_profile_type="mineral tannic",
    price_tier="ultra_premium",
    price_range_cad="$800-$1500+",
    technical_specs={
        "grape": "Garnacha 90%+ (with Cabernet Sauvignon and Carinena)",
        "appellation": "DOQ Priorat",
        "soil": "llicorella (slate-mica schist)",
        "vine_age": "50-100+ years"
    })

print("\n=== SHERRY PRODUCERS ===")

lustau = P(cur, "Bodegas Lustau",
    producer_type="winery", region_id=JEREZ, country="Spain",
    production_philosophy="conventional",
    philosophy_description=(
        "Lustau is widely considered the most quality-conscious of the major Sherry houses, "
        "known especially for their Almacenista programme — buying and bottling single-warehouse "
        "Sherries from small private producers (almacenistas) who have no commercial label. "
        "These single-almacenista bottlings represent Sherry in its most diverse and authentic form. "
        "Also excellent: their Emilio Lustau range across all Sherry styles."
    ),
    key_personnel=["Manuel Lozano (CEO)"],
    production_details={
        "founded": 1896,
        "specialty": "Almacenista programme — single-warehouse Sherries",
        "key_wines": ["Amontillado del Puerto", "Palo Cortado Peninsula", "Los Arcos Dry Amontillado", "Manzanilla Papirusa"],
        "style": "all Sherry categories; specialises in aged and complex expressions"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Lustau is the sommelier's Sherry house — the reference for quality across all styles. "
        "Almacenista programme is unique and educationally valuable. "
        "Strong BC distribution through specialty retailers."
    ),
    allocation_notes="BC — agents / specialty retailers",
    price_positioning="premium", authority_tier=1)

hidalgo_la_gitana = P(cur, "Bodegas Hidalgo La Gitana",
    producer_type="winery", region_id=JEREZ, country="Spain",
    production_philosophy="conventional",
    philosophy_description=(
        "Hidalgo La Gitana in Sanlucar de Barrameda is the reference producer for Manzanilla — "
        "the most delicate and saline of all Sherries. La Gitana (The Gypsy) is the most "
        "iconic Manzanilla brand in Spain and has defined the category for generations. "
        "Their bodegas are in Sanlucar, where the flor (yeast film) grows thicker and more "
        "continuously than in Jerez — imparting the unique saline, chamomile character "
        "that distinguishes Manzanilla from Fino."
    ),
    key_personnel=["Javier Hidalgo"],
    production_details={
        "founded": 1792,
        "location": "Sanlucar de Barrameda — maritime microclimate",
        "key_wines": ["La Gitana Manzanilla", "Pastrana Manzanilla Pasada", "Napoleon Amontillado"],
        "flor": "continuous thick flor from maritime influence"
    },
    quality_tier="estate",
    reputation_narrative=(
        "Hidalgo La Gitana is the Manzanilla benchmark — La Gitana has defined the category. "
        "Napoleon Amontillado is excellent. Good BC availability."
    ),
    allocation_notes="BC — specialty retailers",
    price_positioning="mid_range", authority_tier=1)

gonzalez_byass = P(cur, "Gonzalez Byass",
    producer_type="winery", region_id=JEREZ, country="Spain",
    production_philosophy="conventional",
    philosophy_description=(
        "Gonzalez Byass is the world's most famous Sherry house — Tio Pepe Fino is the "
        "most recognised Sherry brand globally. Founded 1835 in Jerez; still family-owned. "
        "Their solera system contains some of the oldest wines in existence — the Del Duque "
        "VORS Amontillado is over 30 years old on average. "
        "The Apostoles Palo Cortado and Matusalem Oloroso Cream are benchmarks."
    ),
    key_personnel=["Mauricio Gonzalez Gordon"],
    production_details={
        "founded": 1835,
        "key_wines": ["Tio Pepe Fino", "Apostoles Palo Cortado VORS", "Matusalem Oloroso VORS", "Noe PX"],
        "oldest_solera": "Del Duque Amontillado — some wine over 100 years old"
    },
    quality_tier="estate",
    reputation_narrative=(
        "Gonzalez Byass is the world's leading Sherry producer. Tio Pepe is the "
        "reference Fino globally. Apostoles and Matusalem VORS are exceptional. "
        "Very strong BC distribution."
    ),
    allocation_notes="BC — wide distribution",
    price_positioning="premium", authority_tier=1)

navazos = P(cur, "Equipo Navazos",
    producer_type="winery", region_id=JEREZ, country="Spain",
    production_philosophy="natural",
    philosophy_description=(
        "Equipo Navazos is not a bodega — it is a buying and bottling project founded in 2005 "
        "by two Sherry lovers (Jesus Barquin and Eduardo Ojeda). They select exceptional "
        "individual barrels from bodegas across the Jerez triangle, bottle them unfiltered, "
        "and release them as numbered La Bota editions. Each La Bota is unique and unrepeatable — "
        "a specific barrel, a specific moment. They have single-handedly transformed "
        "how the wine world perceives Sherry."
    ),
    key_personnel=["Jesus Barquin", "Eduardo Ojeda"],
    production_details={
        "model": "barrel-selection buying project — no own solera",
        "key_series": "La Bota (numbered editions) — single barrel bottlings from various bodegas",
        "philosophy": "treat Sherry like aged Burgundy — single barrel, unfiltered, limited"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Equipo Navazos is the most critically acclaimed Sherry project globally. "
        "La Bota editions sell out immediately and are collected. "
        "Essential knowledge for serious Sherry service."
    ),
    allocation_notes="BC — Select Wine Merchants / agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

tradicion = P(cur, "Bodegas Tradicion",
    producer_type="winery", region_id=JEREZ, country="Spain",
    production_philosophy="conventional",
    philosophy_description=(
        "Bodegas Tradicion specialises exclusively in VORS (Very Old Rare Sherry) — "
        "wines with an average age of 30+ years in the solera. Founded 1998 by wine "
        "collector Joaquin Rivero, who purchased old soleras from closed bodegas and "
        "assembled them into a museum of aged Sherry. Their Palo Cortado VORS and "
        "Amontillado VORS are reference expressions of extreme aged Sherry."
    ),
    key_personnel=["Joaquin Rivero (founder)"],
    production_details={
        "specialty": "VORS exclusively (minimum 30 years average age)",
        "key_wines": ["Palo Cortado VORS", "Amontillado VORS", "Oloroso VORS", "PX VORS"],
        "unique": "museum of aged Sherry soleras assembled from closed bodegas"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Tradicion VORS Sherries are among the most complex and ancient wines in the world. "
        "Essential for any serious aged-Sherry program."
    ),
    allocation_notes="BC — specialty retailers / agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

print("\n=== SHERRY PRODUCTS ===")

la_gitana_manzanilla = PROD(cur, "Hidalgo La Gitana Manzanilla",
    category="wine_fortified", producer_id=hidalgo_la_gitana, region_id=JEREZ,
    subcategory="manzanilla",
    description=(
        "La Gitana Manzanilla is the most iconic Manzanilla in Spain — a bone-dry, "
        "flor-aged Sherry from Sanlucar de Barrameda. The maritime influence of Sanlucar "
        "(where Atlantic air flows inland) means the flor yeast film on the wine's surface "
        "is thicker and more continuous than in Jerez — imparting a distinctive saline, "
        "chamomile, and sea air character unique to Manzanilla."
    ),
    origin_country="Spain",
    quality_tier="estate",
    quality_hierarchy=[{"tier": "Manzanilla benchmark — Sanlucar maritime flor", "serve": "aperitif only"}],
    deductive_profile={
        "appearance": "pale straw, brilliant",
        "nose": "saline, chamomile, sea air, green olive, fresh almond, yeast",
        "palate": "bone dry, light body, saline finish, very refreshing",
        "signature": "the saltiest and most delicate Sherry style — Sanlucar maritime character"
    },
    service_specs={
        "temperature": "6-8C — serve very cold, straight from refrigerator",
        "glass": "copita (traditional) or white wine glass",
        "consume": "once opened, consume within 1-2 days; or serve from fresh bottle",
        "food": "jamon iberico, marcona almonds, boquerones (anchovies), fried fish"
    },
    flavour_markers=["saline", "chamomile", "sea air", "green olive", "fresh almond"],
    flavour_weight="light",
    flavour_profile_type="saline flor-aged",
    price_tier="mid_range",
    price_range_cad="$20-$35",
    technical_specs={
        "grape": "Palomino Fino 100%",
        "style": "Manzanilla (flor-aged, under flor, Sanlucar)",
        "abv": "15%",
        "rs": "under 5g/L"
    })

tio_pepe_fino = PROD(cur, "Gonzalez Byass Tio Pepe Fino",
    category="wine_fortified", producer_id=gonzalez_byass, region_id=JEREZ,
    subcategory="fino",
    description=(
        "Tio Pepe is the world's most recognisable Fino Sherry — the reference against which "
        "all other Finos are measured. Made from Palomino grapes grown in the Jerez albariza "
        "soils (chalky white, highly reflective), fortified to 15% ABV, and aged under a "
        "continuous layer of flor yeast for at least 4 years. The result: bone dry, pale, "
        "nutty-almond, with a clean bitter finish. The global benchmark for aperitif Sherry."
    ),
    origin_country="Spain",
    quality_tier="market",
    quality_hierarchy=[{"tier": "Fino benchmark — global reference for the style"}],
    deductive_profile={
        "appearance": "pale straw",
        "nose": "almond, green apple, yeast, subtle flor, hint of chamomile",
        "palate": "bone dry, light-medium body, clean bitter almond finish",
        "signature": "the definitive Fino — almond-dry-clean is Tio Pepe's fingerprint"
    },
    service_specs={
        "temperature": "6-8C — serve very cold",
        "glass": "copita",
        "consume": "1-2 days after opening (keep refrigerated)"
    },
    flavour_markers=["almond", "green apple", "yeast", "chamomile", "clean bitter"],
    flavour_weight="light",
    flavour_profile_type="saline flor-aged",
    price_tier="mid_range",
    price_range_cad="$22-$35",
    technical_specs={
        "grape": "Palomino Fino",
        "style": "Fino (under flor, Jerez)",
        "abv": "15%"
    })

lustau_amontillado = PROD(cur, "Lustau Los Arcos Dry Amontillado",
    category="wine_fortified", producer_id=lustau, region_id=JEREZ,
    subcategory="amontillado",
    description=(
        "Amontillado begins as Fino but loses its flor protection — either by accident "
        "or design — and oxidises under the influence of the solera system. "
        "Los Arcos is Lustau's benchmark dry Amontillado: hazelnut, amber, tobacco, "
        "with an oxidative nutty depth absent in Fino. Medium-dry but not sweet — "
        "the most complex of the everyday Sherry styles."
    ),
    origin_country="Spain",
    quality_tier="estate",
    quality_hierarchy=[{"tier": "Dry Amontillado benchmark", "evolution": "Fino that lost its flor and oxidised"}],
    deductive_profile={
        "appearance": "amber-gold",
        "nose": "hazelnut, roasted almond, tobacco, dried apricot, caramel, dried mushroom",
        "palate": "dry, medium body, rich nutty-oxidative complexity, long finish",
        "signature": "hazelnut + tobacco = Amontillado; more complex and nutty than Fino"
    },
    service_specs={
        "temperature": "10-12C",
        "glass": "copita or standard white glass",
        "food": "jamon, manchego, almonds, chicken broth, medium-rich tapas"
    },
    flavour_markers=["hazelnut", "roasted almond", "tobacco", "dried apricot", "caramel"],
    flavour_weight="medium",
    flavour_profile_type="oxidative nutty",
    price_tier="mid_range",
    price_range_cad="$25-$45",
    technical_specs={
        "grape": "Palomino Fino",
        "style": "Amontillado (flor-then-oxidative aging)",
        "abv": "18-19%"
    })

lustau_palo_cortado = PROD(cur, "Lustau Peninsula Palo Cortado",
    category="wine_fortified", producer_id=lustau, region_id=JEREZ,
    subcategory="palo_cortado",
    description=(
        "Palo Cortado is the rarest and most enigmatic Sherry style — it begins as a Fino "
        "(under flor) but spontaneously loses its flor protection and develops in an "
        "Oloroso-like oxidative direction, while retaining the aromatic delicacy of an "
        "Amontillado. Lustau Peninsula is a reference Palo Cortado: the most complex of "
        "all Sherry styles — combining the elegance of Amontillado with the richness of Oloroso."
    ),
    origin_country="Spain",
    quality_tier="reserve",
    quality_hierarchy=[{"tier": "Palo Cortado — rarest and most complex Sherry style"}],
    deductive_profile={
        "appearance": "amber to mahogany",
        "nose": "hazelnut, dark chocolate, tobacco, dried orange peel, walnut, roasted coffee",
        "palate": "dry but rich, medium-full body, extraordinary complexity, very long finish",
        "signature": "the Sherry paradox — Amontillado delicacy + Oloroso richness simultaneously"
    },
    service_specs={
        "temperature": "12-14C",
        "glass": "standard white wine glass (to show complexity)",
        "food": "manchego, jamon iberico, duck, game, dark chocolate"
    },
    flavour_markers=["hazelnut", "dark chocolate", "tobacco", "dried orange", "walnut"],
    flavour_weight="medium-full",
    flavour_profile_type="oxidative complex",
    price_tier="premium",
    price_range_cad="$40-$80",
    technical_specs={
        "grape": "Palomino Fino",
        "style": "Palo Cortado (spontaneous — rarest Sherry)",
        "abv": "19-20%"
    })

gonzalez_px = PROD(cur, "Gonzalez Byass Noe Pedro Ximenez VORS",
    category="wine_fortified", producer_id=gonzalez_byass, region_id=JEREZ,
    subcategory="pedro_ximenez",
    description=(
        "Noe Pedro Ximenez VORS (Very Old Rare Sherry) is made from Pedro Ximenez grapes "
        "that are sun-dried on esparto mats until they become raisins (passito technique). "
        "The resulting wine has 400-500g/L residual sugar — so sweet it pours like "
        "molasses and tastes of raisin, coffee, chocolate, and brown sugar. "
        "With an average age of 30+ years, Noe develops extraordinary dried fruit complexity. "
        "Traditionally poured over vanilla ice cream — one of gastronomy's great simple pleasures."
    ),
    origin_country="Spain",
    quality_tier="reserve",
    quality_hierarchy=[{
        "designation": "VORS — minimum 30 years average age",
        "rs": "400-500g/L residual sugar",
        "appassimento": "sun-dried PX grapes"
    }],
    deductive_profile={
        "appearance": "black-brown, viscous, syrupy",
        "nose": "raisin, date, coffee, dark chocolate, molasses, walnut, tobacco",
        "palate": "intensely sweet, viscous, extraordinary concentrated dried fruit",
        "signature": "the sweetest wine in the world — PX VORS at 30+ years of age"
    },
    service_specs={
        "temperature": "room temperature or slightly cool",
        "pour": "30ml maximum — extremely concentrated",
        "glass": "dessert wine glass",
        "use": "poured over vanilla ice cream; with blue cheese; with dark chocolate"
    },
    flavour_markers=["raisin", "date", "coffee", "dark chocolate", "molasses", "walnut"],
    flavour_weight="full",
    flavour_profile_type="sweet concentrated",
    price_tier="ultra_premium",
    price_range_cad="$80-$150",
    technical_specs={
        "grape": "Pedro Ximenez 100%",
        "style": "Pedro Ximenez VORS",
        "rs": "400-500g/L",
        "abv": "15-16%"
    })

la_bota_amontillado = PROD(cur, "Equipo Navazos La Bota de Amontillado",
    category="wine_fortified", producer_id=navazos, region_id=JEREZ,
    subcategory="amontillado",
    description=(
        "La Bota is Equipo Navazos's numbered single-barrel series — each edition unique "
        "and unrepeatable. La Bota de Amontillado editions (various numbers) are drawn from "
        "exceptional barrels at various bodegas in the Jerez triangle. Unfiltered, unfined, "
        "and bottled at natural strength — these are Sherries that demand the same attention "
        "as great Burgundy. Each edition is released without knowing when or if a similar "
        "one will be available again."
    ),
    origin_country="Spain",
    quality_tier="reserve",
    quality_hierarchy=[{
        "model": "single-barrel unfiltered — Sherry as fine wine",
        "edition": "numbered — each unique, irreplaceable"
    }],
    deductive_profile={
        "nose": "intense hazelnut, tobacco, dried mushroom, salt air, savory depth",
        "palate": "complex, unfiltered richness, extraordinary depth",
        "signature": "Amontillado at maximum complexity — as close to Burgundy as Sherry gets"
    },
    service_specs={"temperature": "12C", "glass": "white wine glass", "consume": "within 5 days of opening"},
    flavour_markers=["hazelnut", "tobacco", "dried mushroom", "salt air", "complex savory"],
    flavour_weight="medium-full",
    flavour_profile_type="oxidative complex",
    price_tier="ultra_premium",
    price_range_cad="$80-$180",
    technical_specs={
        "grape": "Palomino Fino",
        "style": "Amontillado — single barrel, unfiltered",
        "model": "Equipo Navazos La Bota series"
    })

print("\n=== SPANISH REFERENCES ===")

ref_sherry = REF(cur,
    "Sherry — Solera System, Style Spectrum, and the Flor Yeast Biology",
    category="wine_knowledge", skill_level="master",
    description=(
        "Sherry is Spain's greatest wine and one of the world's most misunderstood. "
        "Understanding the solera system, flor yeast biology, and the full style spectrum "
        "is essential for confident service and recommendation."
    ),
    key_principles=(
        "THE SOLERA SYSTEM: "
        "Sherry is produced in a fractional blending system. Barrels are arranged in "
        "tiers (criaderas). Wine flows from young barrels (upper criaderas) down to the "
        "oldest (the solera — floor level). Each year, a portion (typically 20-30%) is "
        "drawn from the solera and replaced with younger wine from above. "
        "This produces a wine of consistent average age rather than a single vintage. "
        "\nFLOR YEAST: "
        "Fino and Manzanilla are aged under flor — a floating film of Saccharomyces yeasts "
        "that consume glycerol and acetaldehyde, creating the distinctive pungent, slightly "
        "saline character. Flor requires: cool temp (15-20C), specific humidity, and "
        "moderate alcohol (14.5-15.5% — too high kills the flor). "
        "Manzanilla (Sanlucar): flor grows year-round; more saline and delicate. "
        "Fino (Jerez): flor is seasonal; slightly less saline. "
        "\nSTYLE SPECTRUM (dry to sweet, aged complexity): "
        "MANZANILLA: lightest, most saline, 15% ABV; serve at 6-8C; drink fresh "
        "FINO: similar but less saline; 15% ABV; serve at 6-8C; drink fresh "
        "AMONTILLADO: began as Fino but lost flor and oxidised; 18-19% ABV; hazelnut, tobacco "
        "PALO CORTADO: spontaneous — began as Fino, evolved like Oloroso but retained elegance "
        "OLOROSO: aged fully oxidatively from the start (no flor); dark, rich, nutty, dry "
        "CREAM: Oloroso sweetened with PX; accessible commercial style "
        "PEDRO XIMENEZ (PX): intensely sweet; sun-dried grapes; 400+ g/L RS; pour over ice cream "
        "\nAGING DESIGNATIONS: "
        "VOS (Very Old Sherry): 20+ years average age "
        "VORS (Very Old Rare Sherry): 30+ years average age "
        "\nSERVICE TEMPERATURES: "
        "Manzanilla/Fino: 6-8C (from fridge) "
        "Amontillado: 10-12C "
        "Palo Cortado/Oloroso: 12-14C "
        "PX: room temperature "
        "\nSERVICE PORTIONS: "
        "125-150ml for Manzanilla/Fino (aperitif) "
        "60-75ml for Amontillado/Oloroso "
        "30-45ml for PX and VORS expressions"
    ),
    common_mistakes=(
        "Serving Fino or Manzanilla warm — must be cold (6-8C). "
        "Not replacing Sherry after opening — Fino is perishable, consume within 2-3 days. "
        "Pouring 150ml of PX — 30ml is the appropriate pour. "
        "Recommending only 'sweet Sherry' to guests — the entire dry range is extraordinary. "
        "Confusing the solera average age with a vintage — Sherry is non-vintage (mostly)."
    ),
    pro_tips=(
        "The greatest sommelier pitch for Sherry: 'This Amontillado has an average age of "
        "30 years and costs $45 a bottle. Show me another wine with this complexity at this price.' "
        "La Bota editions are the best argument for treating Sherry as fine wine. "
        "Manzanilla La Gitana with jamon iberico pata negra is one of gastronomy's "
        "most perfect food-wine experiences — saline-mineral matching fatty cured pork fat."
    ),
    authority_tier=1,
    source_text="Consejo Regulador de Vinos de Jerez; CMS Advanced Sommelier curriculum; "
                "Gareth Elias 'Sherry'; Jan Read 'Sherry and the Sherry Bodegas'"
)

ref_tempranillo_rioja = REF(cur,
    "Tempranillo and Spanish Red Wine — Rioja Aging Classifications and Regional Context",
    category="wine_regions", skill_level="advanced",
    description=(
        "Tempranillo is Spain's most important red grape, producing wines across Rioja, "
        "Ribera del Duero, Navarra, La Mancha, and beyond. Understanding the Rioja aging "
        "hierarchy, Tempranillo's deductive profile, and the distinction between Rioja "
        "and Ribera del Duero is essential for Spanish wine service."
    ),
    key_principles=(
        "RIOJA AGING CLASSIFICATIONS (Rioja DOCa): "
        "Joven: no oak aging; early drinking "
        "Crianza: minimum 2 years (1 year in oak minimum) "
        "Reserva: minimum 3 years (1 year in oak minimum) "
        "Gran Reserva: minimum 5 years (2 years in oak, 3 in bottle minimum) "
        "Gran Reserva is only made in declared great vintages by quality producers. "
        "\nRIOJA SUB-ZONES: "
        "RIOJA ALTA (Haro): highest altitude, coolest; most structured; La Rioja Alta, Muga. "
        "RIOJA ALAVESA (Basque side): newer plantings, modern style. "
        "RIOJA ORIENTAL (formerly Baja): warmer, lower; higher alcohol; blending component. "
        "\nRIOJA vs RIBERA DEL DUERO: "
        "Rioja: blended typically (Tempranillo + Garnacha, Mazuelo, Graciano); American oak tradition. "
        "Ribera: typically 100% Tinto Fino (Tempranillo clone); French oak; more powerful. "
        "Ribera is higher altitude (800-900m) and colder; more structured and age-worthy. "
        "\nTEMPRANILLO DEDUCTIVE PROFILE: "
        "Cherry (not black fruit), dried rose, tobacco, cedar, vanilla (from oak), leather. "
        "Medium-high acidity; medium tannin (approachable earlier than Nebbiolo). "
        "In Rioja: more vanilla-coconut from American oak. "
        "In Ribera: more dark fruit and structure from French oak and altitude."
    ),
    common_mistakes=(
        "Assuming all Rioja is Gran Reserva quality — most is Joven or Crianza. "
        "Confusing Rioja and Ribera del Duero (different grapes, different oak tradition). "
        "Missing the vanilla-coconut American oak signature as Rioja's blind clue. "
        "Not knowing that Tinto Fino = Tempranillo clone (Ribera del Duero dialect)."
    ),
    pro_tips=(
        "For blind tasting: cherry + dried rose + vanilla-coconut = Rioja Reserva/Gran Reserva. "
        "If more powerful and dark fruited = Ribera del Duero. "
        "Lopez de Heredia oxidative style is the most confusing for students — "
        "use it to demonstrate that Spanish wine can age as long as Bordeaux."
    ),
    authority_tier=1,
    source_text="WSET Diploma Unit 3; CMS Advanced Sommelier; Jancis Robinson Oxford Companion"
)

print("\n=== SPANISH PAIRINGS ===")

PAIR(cur, "Jamon iberico de bellota with pan con tomate",
     "charcuterie_cured", "aperitif",
     "classic", "complement",
     "The most celebrated food pairing in Spanish gastronomy — iberica acorn-fed ham "
     "with saline Manzanilla. The fat of jamon iberico (oleic acid, similar to olive oil) "
     "is perfectly matched by Manzanilla's saline, chamomile character. "
     "The sea air in the wine mirrors the cured air around the jamon.",
     la_gitana_manzanilla, food_flavour_profile="fatty cured pork, acorn-fed, sweet, salt", beverage_category="wine_fortified")

PAIR(cur, "Gambas al ajillo — sauteed prawns with garlic and olive oil",
     "seafood_general", "aperitif",
     "classic", "complement",
     "Gambas al ajillo is the quintessential Spanish tapas. Tio Pepe Fino's almond-dry "
     "character and light body pairs classically with shellfish; the garlic and olive oil "
     "are lifted by the wine's clean bitterness.",
     tio_pepe_fino, food_flavour_profile="shrimp, garlic, olive oil, paprika", beverage_category="wine_fortified")

PAIR(cur, "Manchego DOP curado with marcona almonds and membrillo",
     "dairy_fermented", "cheese",
     "classic", "complement",
     "Manchego and Amontillado is a classic Spanish cheese pairing. "
     "Lustau Amontillado's hazelnut-oxidative complexity resonates with the "
     "sheep milk nuttiness of aged Manchego; quince paste mirrors the wine's dried fruit.",
     lustau_amontillado, food_flavour_profile="aged sheep cheese, nutty, sweet quince", beverage_category="wine_fortified")

PAIR(cur, "Lechazo asado — suckling lamb roasted in wood oven",
     "wagyu_premium_protein", "main",
     "classic", "complement",
     "Lechazo asado (roasted suckling lamb) is the ceremonial dish of Castilla. "
     "Muga Prado Enea Gran Reserva's vanilla-cherry-tobacco complexity and elegant structure "
     "pairs beautifully with the delicate, fatty richness of suckling lamb.",
     muga_prado_enea, food_flavour_profile="roasted suckling lamb, fat, wood smoke, rosemary", beverage_category="wine_still")

PAIR(cur, "Cochinillo segoviano — roasted suckling pig",
     "wagyu_premium_protein", "main",
     "classic", "complement",
     "Cochinillo (suckling pig) roasted in a wood-fired oven until the skin crackles "
     "like glass is Segovia's most famous dish. Vega Sicilia Unico's extraordinary structure "
     "and length matches the richness of roasted pork while the tobacco-cedar "
     "cedar notes echo the wood smoke.",
     unico, food_flavour_profile="roasted suckling pig, crackling skin, wood smoke, lemon", beverage_category="wine_still")

PAIR(cur, "Pedro Ximenez over vanilla ice cream",
     "dairy_fermented", "dessert",
     "classic", "complement",
     "The most theatrical and simple Spanish dessert pairing — a pool of viscous, "
     "black PX poured over vanilla ice cream. The contrast of hot-sweet molasses "
     "against cold ice cream creates an extraordinary textural moment. "
     "The PX's coffee-raisin-chocolate resonates with vanilla.",
     gonzalez_px, food_flavour_profile="vanilla ice cream, cold cream, sweet", beverage_category="wine_fortified")

PAIR(cur, "Ternera a la brasa with romesco and calçots",
     "wagyu_premium_protein", "main",
     "established", "complement",
     "Grilled veal with Catalan romesco (roasted pepper-almond-bread sauce) and calçots "
     "(green onion). L'Ermita's slate-mineral Garnacha and the Catalan origin of Priorat "
     "creates a regional food-wine pairing; the wine's liquorice and dark fruit matches "
     "the charred pepper richness of romesco.",
     l_ermita, food_flavour_profile="grilled veal, roasted pepper, almond, charred onion", beverage_category="wine_still")

PAIR(cur, "Tortilla Espanola with piquillo peppers and Manchego",
     "produce_specialty", "casual",
     "established", "complement",
     "Tortilla Espanola (Spanish omelette with potato and onion) is the great everyday "
     "Spanish dish. Lopez de Heredia Vina Tondonia's oxidative complexity and restrained "
     "structure is ideal for everyday food — the wine's savory tobacco notes "
     "complement egg and potato.",
     vina_tondonia_gr, food_flavour_profile="egg, potato, onion, piquillo pepper", beverage_category="wine_still")

print("\n=== SHERRY SERVICE PROTOCOL ===")

PROTOCOL(cur,
    "Sherry Service — By-the-Glass and Flight Presentation",
    category="wine_presentation", beverage_family="wine",
    procedure=(
        "1. TEMPERATURE: Manzanilla/Fino must be served directly from the refrigerator (6-8C). "
        "For Amontillado: 10-12C (slightly chilled). Palo Cortado/Oloroso: 12-14C. PX: room temp. "
        "2. GLASSES: Traditional copita for Manzanilla/Fino (shows the flor aromatics best). "
        "Standard white wine glass for Amontillado and aged styles. Small dessert glass for PX. "
        "3. PORTION SIZES: "
        "Manzanilla/Fino: 100-125ml (aperitif portion) "
        "Amontillado/Oloroso: 60-75ml "
        "Palo Cortado: 60ml "
        "PX: 30-45ml maximum (intensely concentrated) "
        "4. FLIGHT PRESENTATION (recommended): "
        "Present a Sherry flight dry-to-sweet: "
        "Manzanilla (30ml) → Amontillado (30ml) → Palo Cortado (30ml) → PX (15ml). "
        "This narrative arc is educational and showcases Sherry's diversity. "
        "5. FOOD PAIRING COMMUNICATION: "
        "Manzanilla: 'Pair with anything from the sea — oysters, fried fish, jamon.' "
        "Amontillado: 'With chicken broth, manchego, almonds, mushrooms.' "
        "Palo Cortado: 'With duck, game, dark chocolate.' "
        "PX: 'Pour over vanilla ice cream — it is extraordinary.' "
        "6. FRESHNESS: Remind guests that Fino and Manzanilla are perishable — "
        "once opened, refrigerate and consume within 3-5 days."
    ),
    description=(
        "Service protocol for Sherry across all styles — aperitif, tapas service, "
        "and flight presentation. Covers temperatures, glass selection, portion sizes, "
        "and guest communication."
    ),
    rationale=(
        "Sherry is among the most misunderstood and undersold wine categories. "
        "A confident, systematic service presentation — especially as a flight — "
        "converts skeptical guests into advocates. The key is temperature, portion, "
        "and food pairing confidence."
    ),
    common_errors=(
        "Serving Manzanilla or Fino warm — destroys the delicate flor character. "
        "Serving PX in a 150ml pour — it is too concentrated; 30-45ml maximum. "
        "Not explaining that old, open Sherry (especially Fino) is perishable. "
        "Using a large red wine glass for Manzanilla — dilutes the aromatics."
    ),
    service_context="fine_dining, sommelier_recommendation",
    equipment_required=["copita glass", "standard white wine glass", "dessert wine glass"],
    guest_communication=(
        "'Sherry is Spain's greatest secret — aged using a system unique in the wine world. "
        "This Amontillado has an average age of 20 years and pairs with almost everything savoury. "
        "The Manzanilla is the most delicate — serve it very cold as an aperitif.'"
    ),
    skill_level="advanced", authority_tier=1,
    source_text="Consejo Regulador de Jerez; CMS Advanced Sommelier curriculum"
)

print("\n✅ Spain batch complete.")
cur.close()
conn.close()
