# Sprint 7 — Catalog Seed List
## Cross-Language Ingredient Aliases for Cycle 7C Seeder

*Cycle 7B, 2026-05-21. Review-gated artifact — do NOT run seeder until Garth approves.*
*135 entries. No code changes. No commits.*

---

## How the 7C Seeder Reads This File

Each YAML block below becomes two DB operations:

1. `INSERT INTO ingredient_master (canonical_name) VALUES (<canonical>) ON CONFLICT (lower(canonical_name)) DO NOTHING RETURNING id`
2. For each alias string: `INSERT INTO ingredient_aliases (ingredient_id, alias, source) VALUES (<id>, <alias>, 'ai_seed') ON CONFLICT (alias_lower) DO UPDATE SET ingredient_id = EXCLUDED.ingredient_id, source = EXCLUDED.source WHERE ingredient_aliases.ingredient_id IS NULL`

**Important:** The seeder must also insert a self-pointing canonical alias for each entry:
`INSERT INTO ingredient_aliases (ingredient_id, alias, source) VALUES (<id>, <canonical>, 'canonical') ON CONFLICT (alias_lower) DO NOTHING`

The `DO UPDATE WHERE ingredient_id IS NULL` logic (not plain `DO NOTHING`) is required to upgrade any existing NULL-linked placeholder rows from prior invoice scans — see Audit 2c Flag 1.

**Selection criteria applied:** Only ingredients whose foreign/trade-name invoice forms do NOT contain the English recipe term as a contiguous case-insensitive substring. Ingredients whose trade names already contain the English term (e.g. "Parmigiano Reggiano", "Persian Negin Saffron Threads") already work on the direct ILIKE pass and are excluded.

---

## French (25 entries)

```yaml
- canonical: Espelette Pepper
  cuisine: French
  origin_region: Basque Country, France
  aliases:
    - piment d'espelette
    - piment d'espelette aop
    - piment basque
    - espelette
  source_languages: [fr, eu]
  reference: chef knowledge + French cuisine canon doc
```

```yaml
- canonical: Mâche
  cuisine: French
  origin_region: France / Benelux
  aliases:
    - mache
    - mache rosette
    - salade de mache
    - lamb's lettuce
    - corn salad
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Porcini Mushrooms
  cuisine: French / Italian
  origin_region: France, Italy
  aliases:
    - cepes
    - cèpes
    - cepes seches
    - cèpes séchés
    - bolets
    - bolets seches
    - bolets séchés
  source_languages: [fr]
  reference: chef knowledge; French specialty importers use 'cèpes' while Italian suppliers use 'porcini'
```

```yaml
- canonical: Brown Butter
  cuisine: French
  origin_region: France
  aliases:
    - beurre noisette
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Veal Sweetbreads
  cuisine: French
  origin_region: France / Europe
  aliases:
    - ris de veau
    - ris de veau de lait
    - ris de veau boucherie
  source_languages: [fr]
  reference: chef knowledge; Two Rivers Specialty Meats and Hills Foods use French trade terms
```

```yaml
- canonical: Duck Confit
  cuisine: French
  origin_region: Gascony, France
  aliases:
    - confit de canard
    - confits de canard
    - confit canard
    - confit cuisse de canard
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Zucchini Blossoms
  cuisine: French / Italian
  origin_region: France, Italy
  aliases:
    - fleurs de courgette
    - fleur de courgette
    - fleurs de courge
    - fiori di zucca
  source_languages: [fr, it]
  reference: chef knowledge
```

```yaml
- canonical: Morello Cherries
  cuisine: French
  origin_region: France / Eastern Europe
  aliases:
    - cerises griottes
    - griottes
    - griotte
    - cerises morello
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Salt-Cured Anchovies
  cuisine: French / Mediterranean
  origin_region: Mediterranean
  aliases:
    - anchois marines
    - anchois marinés
    - filets d'anchois
    - anchois a l'huile
    - anchois en boite
    - anchois de collioure
  source_languages: [fr]
  reference: chef knowledge; Lekker and Classic Fine Foods use French labels
```

```yaml
- canonical: Caper Berries
  cuisine: French / Mediterranean
  origin_region: Mediterranean
  aliases:
    - caprons
    - câprons
    - capres capucines
    - câpres capucines
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Smoked Eel
  cuisine: French / Northern European
  origin_region: France, Netherlands
  aliases:
    - anguille fumee
    - anguille fumée
    - anguille fumée entière
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Blood Sausage
  cuisine: French
  origin_region: France
  aliases:
    - boudin noir
    - boudin noir artisanal
    - boudin noir au naturel
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Veal Kidneys
  cuisine: French
  origin_region: France
  aliases:
    - rognons de veau
    - rognons de veau entiers
  source_languages: [fr]
  reference: chef knowledge; Hills Foods and Two Rivers use French meat trade terms
```

```yaml
- canonical: Lamb Kidneys
  cuisine: French
  origin_region: France
  aliases:
    - rognons d'agneau
    - rognons agneau
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Buckwheat
  cuisine: French
  origin_region: Brittany, France
  aliases:
    - sarrasin
    - ble noir
    - blé noir
    - farine de sarrasin
    - sarrasin decortique
    - sarrasin décortiqué
    - gruau de sarrasin
  source_languages: [fr]
  reference: chef knowledge; Purely Artisan Foods and Lekker carry Breton buckwheat products
```

```yaml
- canonical: Chestnuts
  cuisine: French
  origin_region: France / Southern Europe
  aliases:
    - chataignes
    - châtaignes
    - marrons
    - marrons frais
    - chataignes peelees
    - châtaignes pelées
    - puree de marron
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Tarragon
  cuisine: French
  origin_region: France
  aliases:
    - estragon
    - estragon frais
    - estragon français
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Chervil
  cuisine: French
  origin_region: France
  aliases:
    - cerfeuil
    - cerfeuil frais
    - cerfeuil bouquet
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: White Asparagus
  cuisine: French / German
  origin_region: France, Germany
  aliases:
    - asperges blanches
    - asperges blanches fraiches
    - asperges blanches du perigord
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Black Garlic
  cuisine: French / International
  origin_region: France / South Korea
  aliases:
    - ail noir
    - ail noir fermente
    - ail noir fermenté
    - ail noir français
    - aglio nero
  source_languages: [fr, it]
  reference: chef knowledge; Purely Artisan Fresh-As catalog; Lekker
```

```yaml
- canonical: Four Spice Blend
  cuisine: French
  origin_region: France
  aliases:
    - quatre epices
    - quatre épices
    - quatre epices moulu
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Sorrel
  cuisine: French
  origin_region: France
  aliases:
    - oseille
    - oseille fraiche
    - oseille fraîche
    - oseille jardiniere
    - oseille jardinière
  source_languages: [fr]
  reference: chef knowledge
```

```yaml
- canonical: Bottarga
  cuisine: Mediterranean
  origin_region: Sardinia, Italy / Provence, France
  aliases:
    - poutargue
    - boutargue
    - bottarga di muggine
    - bottarga di tonno
    - poutargue de martigues
  source_languages: [fr, it]
  reference: chef knowledge
```

```yaml
- canonical: Baby Eels
  cuisine: French / Spanish
  origin_region: Atlantic Coast, France / Basque Country, Spain
  aliases:
    - civelles
    - pibales
    - angulas
    - elvers
  source_languages: [fr, es]
  reference: chef knowledge
```

```yaml
- canonical: Smoked Salmon
  cuisine: French
  origin_region: France / Scotland / Norway
  aliases:
    - saumon fume
    - saumon fumé
    - saumon fumé atlantique
    - saumon fumé du pacifique
    - truite fumée
  source_languages: [fr]
  reference: chef knowledge
```

---

## Italian (25 entries)

```yaml
- canonical: White Truffle
  cuisine: Italian
  origin_region: Alba, Piedmont, Italy
  aliases:
    - tartufo bianco
    - tartufo bianco d'alba
    - tartufo bianco pregiato
    - tuber magnatum
    - tuber magnatum pico
  source_languages: [it, la]
  reference: chef knowledge; Italian cuisine canon doc
```

```yaml
- canonical: Black Truffle
  cuisine: Italian
  origin_region: Norcia, Umbria, Italy
  aliases:
    - tartufo nero
    - tartufo nero di norcia
    - tartufo estivo
    - scorzone
    - tuber melanosporum
    - tuber aestivum
  source_languages: [it, la]
  reference: chef knowledge; Italian cuisine canon doc
```

```yaml
- canonical: Anchovies
  cuisine: Italian / Mediterranean
  origin_region: Mediterranean
  aliases:
    - acciughe sotto sale
    - acciughe sott'olio
    - alici
    - alici di menaica
    - acciughe del cantabrico
  source_languages: [it]
  reference: chef knowledge; Lekker carries Italian-labeled anchovy products
```

```yaml
- canonical: Sun-Dried Tomatoes
  cuisine: Italian
  origin_region: Sicily, Italy
  aliases:
    - pomodori secchi
    - pomodori essiccati
    - pomodorini secchi
    - pomodori secchi sott'olio
    - pummarola secca
  source_languages: [it, nap]
  reference: chef knowledge
```

```yaml
- canonical: Capers
  cuisine: Italian / Mediterranean
  origin_region: Pantelleria, Sicily
  aliases:
    - capperi di pantelleria
    - capperi sotto sale
    - capperi sott'aceto
    - capperi in sale
    - cappero di salina
  source_languages: [it]
  reference: chef knowledge; Lekker stocks Pantelleria capers under Italian label
```

```yaml
- canonical: Pine Nuts
  cuisine: Italian / Mediterranean
  origin_region: Italy / Spain
  aliases:
    - pinoli
    - pinoli italiani
    - pinoli siciliani
    - pinoli tostati
    - pignons de pin
  source_languages: [it, fr]
  reference: chef knowledge
```

```yaml
- canonical: Fennel Pollen
  cuisine: Italian
  origin_region: Tuscany, Italy
  aliases:
    - polline di finocchio
    - polline di finocchio selvatico
    - finocchio polline
  source_languages: [it]
  reference: chef knowledge
```

```yaml
- canonical: Cuttlefish
  cuisine: Italian / Mediterranean
  origin_region: Mediterranean
  aliases:
    - seppie
    - seppia
    - seppie fresche
    - seppie pulite
  source_languages: [it]
  reference: chef knowledge
```

```yaml
- canonical: Sea Bass
  cuisine: Italian / Mediterranean
  origin_region: Mediterranean
  aliases:
    - branzino
    - spigola
    - spigola dell'adriatico
    - lupo di mare
  source_languages: [it]
  reference: chef knowledge; Classic Fine Foods imports Mediterranean sea bass under Italian trade names
```

```yaml
- canonical: Sea Bream
  cuisine: Italian / Mediterranean
  origin_region: Mediterranean
  aliases:
    - orata
    - orata fresca
    - pagello
    - pagello fragolino
    - sarago
  source_languages: [it]
  reference: chef knowledge
```

```yaml
- canonical: Monkfish
  cuisine: Italian / French
  origin_region: Atlantic / Mediterranean
  aliases:
    - rana pescatrice
    - coda di rospo
    - lotte (fr)
    - baudroie
  source_languages: [it, fr]
  reference: chef knowledge
```

```yaml
- canonical: Swordfish
  cuisine: Italian / Mediterranean
  origin_region: Mediterranean / Atlantic
  aliases:
    - pesce spada
    - pesce spada siciliano
    - pesce spada dell'atlantico
  source_languages: [it]
  reference: chef knowledge
```

```yaml
- canonical: Octopus
  cuisine: Italian / Mediterranean
  origin_region: Mediterranean
  aliases:
    - polpo
    - polipo
    - moscardini
    - polpo verace
    - polpo del mediterraneo
  source_languages: [it]
  reference: chef knowledge
```

```yaml
- canonical: Razor Clams
  cuisine: Italian / Spanish
  origin_region: Atlantic / Mediterranean
  aliases:
    - cannolicchi
    - cape lunghe
    - capelunghe
    - navajas
  source_languages: [it, es]
  reference: chef knowledge
```

```yaml
- canonical: Scallops
  cuisine: Italian / French
  origin_region: Atlantic / Mediterranean
  aliases:
    - capesante
    - conchiglie di san giacomo
    - pettine di mare
    - coquilles saint-jacques
    - noix de saint-jacques
  source_languages: [it, fr]
  reference: chef knowledge
```

```yaml
- canonical: Balsamic Vinegar
  cuisine: Italian
  origin_region: Modena, Emilia-Romagna, Italy
  aliases:
    - aceto balsamico
    - aceto balsamico di modena
    - aceto balsamico tradizionale
    - aceto balsamico igp
    - aceto di vino balsamico
  source_languages: [it]
  reference: chef knowledge; Italian cuisine canon doc; Lekker carries Italian-labeled balsamic
```

```yaml
- canonical: Grape Must Syrup
  cuisine: Italian
  origin_region: Southern Italy
  aliases:
    - mosto cotto
    - vino cotto
    - sapa
    - vincotto
    - mosto d'uva cotto
  source_languages: [it]
  reference: chef knowledge
```

```yaml
- canonical: Wild Boar
  cuisine: Italian / French
  origin_region: Tuscany, Italy
  aliases:
    - cinghiale
    - cinghiale selvatico
    - carne di cinghiale
    - sanglier
  source_languages: [it, fr]
  reference: chef knowledge
```

```yaml
- canonical: Rabbit
  cuisine: Italian / French
  origin_region: Italy / France
  aliases:
    - coniglio
    - coniglio nostrano
    - coniglio intero
    - lapin
    - lapin entier
  source_languages: [it, fr]
  reference: chef knowledge
```

```yaml
- canonical: Squid Ink
  cuisine: Italian / Mediterranean
  origin_region: Mediterranean
  aliases:
    - nero di seppia
    - inchiostro di seppia
    - encre de seiche
    - tinta de calamar
  source_languages: [it, fr, es]
  reference: chef knowledge
```

```yaml
- canonical: Chestnut Flour
  cuisine: Italian
  origin_region: Tuscany / Liguria, Italy
  aliases:
    - farina di castagne
    - farina di marroni
    - farina di castagne del piemonte
    - farina dolce di castagne
  source_languages: [it]
  reference: chef knowledge
```

```yaml
- canonical: Spelt Flour
  cuisine: Italian
  origin_region: Italy / Central Europe
  aliases:
    - farina di farro
    - farro macinato
    - farro integrale
    - farine d'épeautre
  source_languages: [it, fr]
  reference: chef knowledge
```

```yaml
- canonical: Roman Spring Lamb
  cuisine: Italian
  origin_region: Lazio, Italy
  aliases:
    - abbacchio
    - abbacchio romano
    - agnello da latte
    - agnello da latte igp
  source_languages: [it]
  reference: chef knowledge; Italian cuisine canon doc
```

```yaml
- canonical: Calf's Liver
  cuisine: Italian / French
  origin_region: Italy / France
  aliases:
    - fegato di vitello
    - fegato di vitello veneto
    - foie de veau
  source_languages: [it, fr]
  reference: chef knowledge
```

```yaml
- canonical: Cannellini Beans
  cuisine: Italian
  origin_region: Tuscany, Italy
  aliases:
    - fagioli cannellini
    - cannellini secchi
    - fagioli di lamon
    - fagioli toscani
    - fagioli bianchi
  source_languages: [it]
  reference: chef knowledge
```

---

## Japanese (25 entries)

```yaml
- canonical: Bonito Flakes
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - katsuobushi
    - katsuo bushi
    - hanakatsuo
    - kezuribushi
    - katsuo dashi
  source_languages: [ja]
  reference: chef knowledge; Japanese cuisine canon doc
```

```yaml
- canonical: Pickled Ginger
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - gari
    - beni shoga
    - kizami shoga
    - amazu shoga
    - sushi ginger
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Rice Vinegar
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - komezu
    - kome su
    - junmai su
    - kokumotsu su
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Soy Sauce
  cuisine: Japanese / Chinese
  origin_region: Japan
  aliases:
    - shoyu
    - koikuchi shoyu
    - usukuchi shoyu
    - shiro shoyu
    - tamari shoyu
  source_languages: [ja]
  reference: chef knowledge; Japanese cuisine canon doc
```

```yaml
- canonical: White Miso
  cuisine: Japanese
  origin_region: Kyoto, Japan
  aliases:
    - shiro miso
    - shiromiso
    - saikyo miso
    - kyoto miso
  source_languages: [ja]
  reference: chef knowledge; Japanese cuisine canon doc
```

```yaml
- canonical: Red Miso
  cuisine: Japanese
  origin_region: Nagoya, Japan
  aliases:
    - aka miso
    - akamiso
    - hatcho miso
    - sendai miso
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Salmon Roe
  cuisine: Japanese
  origin_region: Japan / Pacific Northwest
  aliases:
    - ikura
    - sake no ko
    - sake ikura
  source_languages: [ja]
  reference: chef knowledge; Organic Ocean and Taylor Shellfish carry BC salmon roe; Japanese importers label it 'ikura'
```

```yaml
- canonical: Sea Urchin
  cuisine: Japanese
  origin_region: Hokkaido, Japan / BC Coast
  aliases:
    - uni
    - bafun uni
    - murasaki uni
    - ezobafun uni
    - uni fresh
  source_languages: [ja]
  reference: chef knowledge; Organic Ocean carries BC uni; Japanese-export grade labeled 'uni' or 'bafun uni'
```

```yaml
- canonical: Yellowtail
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - hamachi
    - buri
    - inada
    - warasa
    - kanpachi
  source_languages: [ja]
  reference: chef knowledge; Japanese cuisine canon doc
```

```yaml
- canonical: Flying Fish Roe
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - tobiko
    - tobikko
    - tobiuo no ko
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Spicy Pollock Roe
  cuisine: Japanese
  origin_region: Hokkaido / Fukuoka, Japan
  aliases:
    - mentaiko
    - karashi mentaiko
    - tarako
    - spicy cod roe
  source_languages: [ja]
  reference: chef knowledge; Japanese cuisine canon doc
```

```yaml
- canonical: Monkfish Liver
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - ankimo
    - anko no kimo
  source_languages: [ja]
  reference: chef knowledge; Masayoshi and similar BC kaiseki-style restaurants source this
```

```yaml
- canonical: Burdock Root
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - gobo
    - gobou
    - fresh gobo
    - gobo root
    - gobou frais
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Lotus Root
  cuisine: Japanese / Chinese
  origin_region: Japan / China
  aliases:
    - renkon
    - hasu
    - renkon section
    - lian ou
    - lian root
  source_languages: [ja, zh]
  reference: chef knowledge
```

```yaml
- canonical: Mitsuba
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - mitsuba
    - san-mitsuba
    - japanese parsley
    - japanese wild parsley
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Myoga
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - myoga ginger
    - myoga buds
    - japanese ginger blossom
    - zingiber mioga
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Black Sesame Seeds
  cuisine: Japanese / Chinese
  origin_region: Japan / East Asia
  aliases:
    - kuro goma
    - kuro sesame
    - black goma
    - graines de sesame noir
  source_languages: [ja, fr]
  reference: chef knowledge
```

```yaml
- canonical: Sesame Paste
  cuisine: Japanese / Chinese
  origin_region: Japan / China
  aliases:
    - nerigoma
    - neri goma
    - white sesame paste
    - zhima jiang
    - zhī ma jiàng
  source_languages: [ja, zh]
  reference: chef knowledge
```

```yaml
- canonical: Mackerel
  cuisine: Japanese
  origin_region: Japan / Pacific
  aliases:
    - saba
    - ma-saba
    - goma-saba
    - saba fillet
    - saba whole
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Flounder
  cuisine: Japanese
  origin_region: Japan / Pacific
  aliases:
    - hirame
    - olive flounder
    - hirame sashimi
    - karei
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Cod Milt
  cuisine: Japanese
  origin_region: Japan / Pacific
  aliases:
    - shirako
    - tachi
    - shirako fresh
    - kiku
    - soft roe cod
  source_languages: [ja]
  reference: chef knowledge; Masayoshi and Maenam source shirako during BC albacore/cod season
```

```yaml
- canonical: Dried Daikon
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - kiriboshi daikon
    - kiriboshi daikon strips
    - kiri daikon
    - daikon dried strips
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Kinako
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - roasted soybean flour
    - kinako powder
    - soybean flour roasted
    - soya powder grillée
  source_languages: [ja]
  reference: chef knowledge
```

```yaml
- canonical: Bluefin Tuna
  cuisine: Japanese
  origin_region: Pacific / Atlantic
  aliases:
    - maguro
    - hon maguro
    - kihada maguro
    - thon rouge
    - thon rouge de l'atlantique
  source_languages: [ja, fr]
  reference: chef knowledge; Japanese cuisine canon doc
```

```yaml
- canonical: Japanese Sea Bream
  cuisine: Japanese
  origin_region: Japan
  aliases:
    - tai
    - madai
    - red sea bream
    - pagrus major
  source_languages: [ja]
  reference: chef knowledge; Japanese cuisine canon doc
```

---

## Spanish (10 entries)

```yaml
- canonical: Smoked Paprika
  cuisine: Spanish
  origin_region: Extremadura / Murcia, Spain
  aliases:
    - pimenton de la vera
    - pimentón de la vera
    - pimenton ahumado
    - pimentón ahumado
    - pimenton de murcia
    - pimenton dulce
    - pimenton picante
  source_languages: [es]
  reference: chef knowledge; Spanish cuisine canon doc; Lekker and Purely Artisan carry La Vera paprika
```

```yaml
- canonical: Spanish Saffron
  cuisine: Spanish
  origin_region: La Mancha, Spain
  aliases:
    - azafran
    - azafrán
    - azafran de la mancha
    - azafran en hebras
    - azafran molido
    - safran espagnol
  source_languages: [es, fr]
  reference: chef knowledge; Spanish cuisine canon doc
```

```yaml
- canonical: Salt Cod
  cuisine: Spanish / Portuguese
  origin_region: Atlantic
  aliases:
    - bacalao
    - bacalao salado
    - bacalla
    - bacalà
    - bacalhau
    - bacalao desalado
  source_languages: [es, ca, pt, it]
  reference: chef knowledge; Spanish cuisine canon doc; Lekker carries bacalao
```

```yaml
- canonical: Ibérico Ham
  cuisine: Spanish
  origin_region: Extremadura / Andalusia, Spain
  aliases:
    - jamon iberico
    - jamón ibérico
    - jamon iberico de bellota
    - jamón ibérico de bellota
    - pata negra
    - jamon de bellota
  source_languages: [es]
  reference: chef knowledge; Spanish cuisine canon doc
```

```yaml
- canonical: Serrano Ham
  cuisine: Spanish
  origin_region: Spain
  aliases:
    - jamon serrano
    - jamón serrano
    - serrano curado
    - serrano gran reserva
  source_languages: [es]
  reference: chef knowledge
```

```yaml
- canonical: Cockles
  cuisine: Spanish / British
  origin_region: Atlantic / Mediterranean
  aliases:
    - berberechos
    - berberechos al natural
    - berberechos en conserva
    - clovisses
  source_languages: [es, fr]
  reference: chef knowledge
```

```yaml
- canonical: Morcilla
  cuisine: Spanish
  origin_region: Burgos / León, Spain
  aliases:
    - morcilla de burgos
    - morcilla ibérica
    - morcilla de cebolla
    - morcilla asturiana
  source_languages: [es]
  reference: chef knowledge; Spanish cuisine canon doc
```

```yaml
- canonical: Quince Paste
  cuisine: Spanish / Portuguese
  origin_region: Spain
  aliases:
    - membrillo
    - dulce de membrillo
    - queso de membrillo
    - pasta de marmelo
    - cotignac
  source_languages: [es, pt, fr]
  reference: chef knowledge; Lekker and specialty importers carry Spanish membrillo
```

```yaml
- canonical: Sherry Vinegar
  cuisine: Spanish
  origin_region: Jerez de la Frontera, Andalusia
  aliases:
    - vinagre de jerez
    - vinagre de jerez reserva
    - jerez vinagre
    - vinaigre de xeres
  source_languages: [es, fr]
  reference: chef knowledge; Spanish cuisine canon doc; Lekker stocks Jerez DO vinegar
```

```yaml
- canonical: Aleppo Pepper
  cuisine: Spanish / Levantine
  origin_region: Aleppo, Syria / Turkey
  aliases:
    - pul biber
    - isot biber
    - biber pul
    - halaby pepper
    - poivre d'alep
  source_languages: [tr, ar, fr]
  reference: chef knowledge; Greek/Levantine cuisine canon doc
```

---

## Mexican (10 entries)

```yaml
- canonical: Ancho Chile
  cuisine: Mexican
  origin_region: Puebla, Mexico
  aliases:
    - chile ancho
    - ancho seco
    - ancho chile seco
  source_languages: [es]
  reference: chef knowledge; Mexican cuisine canon doc
```

```yaml
- canonical: Guajillo Chile
  cuisine: Mexican
  origin_region: Zacatecas / Aguascalientes, Mexico
  aliases:
    - chile guajillo
    - guajillo seco
    - chile guajillo desvenado
    - guajillo entero
  source_languages: [es]
  reference: chef knowledge; Mexican cuisine canon doc
```

```yaml
- canonical: Pasilla Chile
  cuisine: Mexican
  origin_region: Oaxaca, Mexico
  aliases:
    - chile pasilla
    - chile negro
    - pasilla negro
    - chile pasilla oaxaqueno
  source_languages: [es]
  reference: chef knowledge; Mexican cuisine canon doc
```

```yaml
- canonical: Dried Hibiscus
  cuisine: Mexican
  origin_region: Mexico / Caribbean
  aliases:
    - flor de jamaica
    - jamaica
    - hibisco seco
    - flor de hibisco
    - fleurs d'hibiscus seches
  source_languages: [es, fr]
  reference: chef knowledge; Mexican cuisine canon doc; Purely Artisan carries dried hibiscus
```

```yaml
- canonical: Cacao Nibs
  cuisine: Mexican / International
  origin_region: Mexico / Ecuador / Peru
  aliases:
    - grue de cacao
    - grué de cacao
    - cacao en grano
    - cacao tostado en grano
    - éclats de cacao
  source_languages: [es, fr]
  reference: chef knowledge; Purely Artisan carries Valrhona and Mexican cacao nibs under French labeling
```

```yaml
- canonical: Pozole Corn
  cuisine: Mexican
  origin_region: Guerrero / Jalisco, Mexico
  aliases:
    - maiz cacahuazintle
    - maíz cacahuazintle
    - maiz pozolero
    - cacahuazintle
    - hominy dried
  source_languages: [es, nah]
  reference: chef knowledge; Mexican cuisine canon doc
```

```yaml
- canonical: Piloncillo
  cuisine: Mexican
  origin_region: Mexico / Colombia
  aliases:
    - panela
    - piloncillo oscuro
    - piloncillo conico
    - piloncillo cónico
    - papelon
    - chancaca
  source_languages: [es]
  reference: chef knowledge; Mexican cuisine canon doc
```

```yaml
- canonical: Achiote Paste
  cuisine: Mexican
  origin_region: Yucatán, Mexico
  aliases:
    - pasta de achiote
    - recado rojo
    - achiote molido
    - annatto paste
    - recado de bistec
  source_languages: [es, yua]
  reference: chef knowledge; Mexican cuisine canon doc
```

```yaml
- canonical: Banana Leaves
  cuisine: Mexican / Southeast Asian
  origin_region: Mexico / Southeast Asia
  aliases:
    - hojas de platano
    - hojas de plátano
    - hojas platano congeladas
    - feuilles de bananier
    - bananenblaetter
  source_languages: [es, fr]
  reference: chef knowledge; Mexican cuisine canon doc
```

```yaml
- canonical: Mulato Chile
  cuisine: Mexican
  origin_region: Puebla, Mexico
  aliases:
    - chile mulato
    - mulato seco
    - chile mulato entero
  source_languages: [es]
  reference: chef knowledge; Mexican cuisine canon doc
```

---

## Indian (10 entries)

```yaml
- canonical: Asafoetida
  cuisine: Indian
  origin_region: Iran / Afghanistan / India
  aliases:
    - hing
    - heeng
    - asafetida powder
    - kayam
    - perunkayam
    - ferula asafoetida powder
  source_languages: [hi, ta, en]
  reference: chef knowledge; Indian cuisine canon doc
```

```yaml
- canonical: Fenugreek Leaves
  cuisine: Indian
  origin_region: India
  aliases:
    - methi
    - kasoori methi
    - kasuri methi
    - methi saag
    - methi patta
    - dried fenugreek leaf
  source_languages: [hi, ur]
  reference: chef knowledge; Indian cuisine canon doc
```

```yaml
- canonical: Curry Leaves
  cuisine: Indian / Sri Lankan
  origin_region: Southern India / Sri Lanka
  aliases:
    - kadi patta
    - kadhi patta
    - meetha neem
    - curry patta
    - murraya koenigii
    - kariveppilai
  source_languages: [hi, ta]
  reference: chef knowledge; Indian cuisine canon doc
```

```yaml
- canonical: Black Cardamom
  cuisine: Indian
  origin_region: Sikkim / Nepal / Eastern Himalayas
  aliases:
    - badi elaichi
    - kali elaichi
    - moti elaichi
    - brown cardamom
    - nepal cardamom
    - tsao-ko
  source_languages: [hi, zh]
  reference: chef knowledge; Indian cuisine canon doc
```

```yaml
- canonical: Dried Mango Powder
  cuisine: Indian
  origin_region: India
  aliases:
    - amchur
    - amchoor
    - mango amchur powder
    - amchoor powder
    - poudre de mangue verte
  source_languages: [hi, fr]
  reference: chef knowledge; Indian cuisine canon doc
```

```yaml
- canonical: Black Salt
  cuisine: Indian
  origin_region: India / Pakistan
  aliases:
    - kala namak
    - sanchal
    - sulem salt
    - himalayan black salt
    - sel noir indien
  source_languages: [hi, fr]
  reference: chef knowledge; Indian cuisine canon doc
```

```yaml
- canonical: Carom Seeds
  cuisine: Indian / Middle Eastern
  origin_region: India / Egypt
  aliases:
    - ajwain
    - ajowan
    - ajowan caraway
    - bishop's weed seeds
    - thymol seeds
    - omum
  source_languages: [hi, en]
  reference: chef knowledge; Indian cuisine canon doc
```

```yaml
- canonical: Tamarind
  cuisine: Indian / Southeast Asian / Mexican
  origin_region: India / West Africa
  aliases:
    - imli
    - imlee
    - tamarind block
    - tamarind seedless
    - tamarin
    - tamarindo
  source_languages: [hi, fr, es]
  reference: chef knowledge; Indian cuisine canon doc
```

```yaml
- canonical: Dried Pomegranate Seeds
  cuisine: Indian
  origin_region: Afghanistan / India
  aliases:
    - anardana
    - anaar dana
    - pomegranate seed powder
    - anardana crushed
  source_languages: [hi, ur]
  reference: chef knowledge; Indian cuisine canon doc
```

```yaml
- canonical: Kokum
  cuisine: Indian
  origin_region: Konkan Coast, India
  aliases:
    - kokum dried
    - kokum fruit
    - gamboge
    - kudampuli
    - malabar tamarind
    - garcinia indica
  source_languages: [hi, ml, en]
  reference: chef knowledge; Indian cuisine canon doc
```

---

## Greek / Levantine (10 entries)

```yaml
- canonical: Pomegranate Molasses
  cuisine: Levantine
  origin_region: Lebanon / Syria / Iran
  aliases:
    - dibs al rumman
    - dibs el rumman
    - robb al rumman
    - melasse de grenade
    - molasses grenade
  source_languages: [ar, fr]
  reference: chef knowledge; Greek/Levantine cuisine canon doc
```

```yaml
- canonical: Grape Molasses
  cuisine: Greek / Turkish / Levantine
  origin_region: Greece / Turkey / Lebanon
  aliases:
    - petimezi
    - pekmez
    - dibs al inab
    - dibs el inab
    - grape syrup concentrated
    - melas oinos
  source_languages: [el, tr, ar]
  reference: chef knowledge; Greek/Levantine cuisine canon doc
```

```yaml
- canonical: Dried Limes
  cuisine: Levantine / Persian
  origin_region: Oman / Iran / Iraq
  aliases:
    - loomi
    - noomi basra
    - omani dried limes
    - limu omani
    - black lime dried
  source_languages: [ar]
  reference: chef knowledge; Greek/Levantine cuisine canon doc
```

```yaml
- canonical: Mastic Gum
  cuisine: Greek
  origin_region: Chios, Greece
  aliases:
    - mastiha
    - mastika
    - chios mastiha
    - retsina mastiha
    - gomme mastic
    - mastic de chios
  source_languages: [el, fr]
  reference: chef knowledge; Greek/Levantine cuisine canon doc; Lekker carries Chios mastiha products
```

```yaml
- canonical: Dried Barberries
  cuisine: Persian / Levantine
  origin_region: Iran
  aliases:
    - zereshk
    - zereshk dried
    - barberry dried
    - berberis vulgaris dried
    - epine vinette seche
  source_languages: [fa, fr]
  reference: chef knowledge; Greek/Levantine cuisine canon doc
```

```yaml
- canonical: Rose Water
  cuisine: Persian / Levantine / Indian
  origin_region: Iran / Lebanon / India
  aliases:
    - mazaher
    - ma el ward
    - maward
    - gulkand water
    - eau de rose
    - gulab jal
  source_languages: [ar, fa, fr, hi]
  reference: chef knowledge; Greek/Levantine cuisine canon doc
```

```yaml
- canonical: Nigella Seeds
  cuisine: Indian / Levantine
  origin_region: Southwest Asia
  aliases:
    - kalonji
    - habbatus sawda
    - haba al baraka
    - black seed
    - charnushka
    - siyah daneh
  source_languages: [hi, ar, fa, ru]
  reference: chef knowledge; Indian cuisine canon doc; Greek/Levantine cuisine canon doc
```

```yaml
- canonical: Freekeh
  cuisine: Levantine
  origin_region: Levant / North Africa
  aliases:
    - farrik
    - farik
    - farikeh
    - green wheat freekeh
    - roasted green wheat
  source_languages: [ar]
  reference: chef knowledge; Greek/Levantine cuisine canon doc
```

```yaml
- canonical: Carob Powder
  cuisine: Greek / Levantine
  origin_region: Eastern Mediterranean
  aliases:
    - kharoob
    - dibis al kharoob
    - carob molasses
    - poudre de caroube
    - farine de caroube
    - haruv
  source_languages: [ar, fr, he]
  reference: chef knowledge; Greek/Levantine cuisine canon doc
```

```yaml
- canonical: Dried Figs
  cuisine: Greek / Turkish
  origin_region: Turkey / Greece / Iran
  aliases:
    - syka xera
    - anjeer
    - teen mujaffaf
    - incir kurusu
    - figue seche
    - figues sechees
  source_languages: [el, hi, ar, tr, fr]
  reference: chef knowledge; Greek/Levantine cuisine canon doc; Purely Artisan carries dried Turkish figs
```

---

## Chinese (10 entries)

```yaml
- canonical: Sichuan Peppercorns
  cuisine: Chinese
  origin_region: Sichuan, China
  aliases:
    - hua jiao
    - huajiao
    - flower pepper
    - mala pepper
    - zanthoxylum
    - poivre du sichuan
  source_languages: [zh, fr]
  reference: chef knowledge; Chinese cuisine canon doc
```

```yaml
- canonical: Fermented Black Beans
  cuisine: Chinese
  origin_region: Hunan / Guangdong, China
  aliases:
    - douchi
    - dou chi
    - salted black beans
    - dow see
    - harusame mame
  source_languages: [zh, ja]
  reference: chef knowledge; Chinese cuisine canon doc
```

```yaml
- canonical: Chinese Five Spice
  cuisine: Chinese
  origin_region: China
  aliases:
    - wu xiang fen
    - wuxiang powder
    - ng heong fun
    - cinq epices chinoises
    - cinq epices
  source_languages: [zh, yue, fr]
  reference: chef knowledge; Chinese cuisine canon doc
```

```yaml
- canonical: Wood Ear Mushrooms
  cuisine: Chinese / Japanese
  origin_region: China / Japan
  aliases:
    - mu er
    - muer
    - cloud ear fungus
    - black fungus
    - kikurage
    - auricularia auricula
  source_languages: [zh, ja]
  reference: chef knowledge; Chinese cuisine canon doc
```

```yaml
- canonical: Shaoxing Rice Wine
  cuisine: Chinese
  origin_region: Shaoxing, Zhejiang, China
  aliases:
    - hua diao wine
    - hua tiao jiu
    - yellow rice wine
    - michiu rice wine
    - huangjiu
    - vin de riz shaoxing
  source_languages: [zh, fr]
  reference: chef knowledge; Chinese cuisine canon doc
```

```yaml
- canonical: Chili Bean Paste
  cuisine: Chinese
  origin_region: Pixian, Sichuan, China
  aliases:
    - doubanjiang
    - dou ban jiang
    - pixian doubanjiang
    - toban djan
    - la dou ban
    - broad bean chili paste
  source_languages: [zh]
  reference: chef knowledge; Chinese cuisine canon doc
```

```yaml
- canonical: Lotus Seeds
  cuisine: Chinese / Vietnamese
  origin_region: China / Vietnam
  aliases:
    - lian zi
    - lianzi
    - dried lotus seed
    - hat sen
    - lian rou
  source_languages: [zh, vi]
  reference: chef knowledge
```

```yaml
- canonical: Winter Melon
  cuisine: Chinese / Vietnamese
  origin_region: China / Southeast Asia
  aliases:
    - dong gua
    - dong kua
    - white gourd
    - ash gourd
    - bi dao
    - bi qua
  source_languages: [zh, vi]
  reference: chef knowledge
```

```yaml
- canonical: Dried Lily Buds
  cuisine: Chinese
  origin_region: China
  aliases:
    - jin zhen cai
    - golden needles dried
    - gum jum
    - lily buds dried
    - huang hua cai
  source_languages: [zh, yue]
  reference: chef knowledge
```

```yaml
- canonical: Fermented Tofu
  cuisine: Chinese
  origin_region: China
  aliases:
    - fu ru
    - furu
    - nam yu
    - nan ru
    - fermented bean curd
    - white fermented tofu
    - red fermented tofu
  source_languages: [zh, yue]
  reference: chef knowledge
```

---

## Thai / Vietnamese (10 entries)

```yaml
- canonical: Fish Sauce
  cuisine: Thai / Vietnamese
  origin_region: Thailand / Vietnam
  aliases:
    - nuoc mam
    - nuoc mam nhi
    - nam pla
    - tiparos
    - pla ra
    - sauce poisson
  source_languages: [vi, th, fr]
  reference: chef knowledge; Thai/Vietnamese cuisine canon doc
```

```yaml
- canonical: Makrut Lime Leaves
  cuisine: Thai / Cambodian
  origin_region: Southeast Asia
  aliases:
    - bai makrut
    - bai magrood
    - bai ma grood
    - kaffir lime leaf
    - feuille de combava
  source_languages: [th, fr]
  reference: chef knowledge; Thai/Vietnamese cuisine canon doc
```

```yaml
- canonical: Galangal
  cuisine: Thai / Indonesian / Malaysian
  origin_region: Southeast Asia
  aliases:
    - kha
    - khaa
    - galanga root
    - laos powder
    - galanga rhizome
    - lengkuas
    - galgant
  source_languages: [th, id, ms, de]
  reference: chef knowledge; Thai/Vietnamese cuisine canon doc
```

```yaml
- canonical: Lemongrass
  cuisine: Thai / Vietnamese / Khmer
  origin_region: Southeast Asia
  aliases:
    - sa
    - sả
    - ta-khrai
    - takrai
    - citronelle
    - sereh
    - serai
  source_languages: [vi, th, fr, id]
  reference: chef knowledge; Thai/Vietnamese cuisine canon doc
```

```yaml
- canonical: Palm Sugar
  cuisine: Thai / Malaysian / Indonesian
  origin_region: Southeast Asia
  aliases:
    - gula melaka
    - gula malaka
    - nam tan pip
    - gula jawa
    - coconut sugar block
    - jaggery palm
  source_languages: [ms, th, id]
  reference: chef knowledge; Thai/Vietnamese cuisine canon doc
```

```yaml
- canonical: Shrimp Paste
  cuisine: Thai / Malaysian / Vietnamese
  origin_region: Southeast Asia
  aliases:
    - kapi
    - trassi
    - belacan
    - mam tom
    - belachan
    - terasi
  source_languages: [th, ms, vi, id]
  reference: chef knowledge; Thai/Vietnamese cuisine canon doc
```

```yaml
- canonical: Thai Basil
  cuisine: Thai
  origin_region: Southeast Asia
  aliases:
    - bai horapa
    - horapa
    - bai krapao
    - basilic thai
    - rau hung que
  source_languages: [th, fr, vi]
  reference: chef knowledge; Thai/Vietnamese cuisine canon doc
```

```yaml
- canonical: Vietnamese Coriander
  cuisine: Vietnamese
  origin_region: Vietnam / Malaysia
  aliases:
    - rau ram
    - laksa leaf
    - hot mint
    - persicaria odorata
    - rau ram frais
  source_languages: [vi, ms, fr]
  reference: chef knowledge
```

```yaml
- canonical: Pandan Leaves
  cuisine: Thai / Vietnamese / Indonesian
  origin_region: Southeast Asia
  aliases:
    - bai toey
    - la dua
    - daun pandan
    - pandan leaf fresh
    - feuille de pandan
  source_languages: [th, vi, id, fr]
  reference: chef knowledge; Thai/Vietnamese cuisine canon doc
```

```yaml
- canonical: Rice Paper Wrappers
  cuisine: Vietnamese
  origin_region: Vietnam
  aliases:
    - banh trang
    - bahn trang
    - banh cuon wrapper
    - galettes de riz
    - feuilles de riz
  source_languages: [vi, fr]
  reference: chef knowledge
```

---

## Entry Count Summary

| Cuisine | Entries |
|---|---|
| French | 25 |
| Italian | 25 |
| Japanese | 25 |
| Spanish | 10 |
| Mexican | 10 |
| Indian | 10 |
| Greek / Levantine | 10 |
| Chinese | 10 |
| Thai / Vietnamese | 10 |
| **Total** | **135** |

## Status

All entries approved 2026-05-21. Ancho/Mulato conflict resolved: `chile mulato` removed from Ancho Chile aliases; Mulato Chile owns that alias_lower exclusively. Ready for Cycle 7C seeder.
