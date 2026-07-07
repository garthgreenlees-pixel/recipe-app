-- Correction 2.4 (founder-ruled schema, Option A): pairings name DRINKS, not
-- beans. Canonical serves live here; beans/leaves are their expression.
-- The GRIND lane composes/deepens content; founder releases via is_published.
-- Idempotent.
CREATE TABLE IF NOT EXISTS beverage_preparations (
    id                   SERIAL PRIMARY KEY,
    name                 VARCHAR(120) NOT NULL,
    slug                 VARCHAR(140) UNIQUE,
    category             VARCHAR(40) NOT NULL,     -- matches beverage_products.category (coffee, tea, ...)
    description          TEXT,
    flavour_markers      TEXT[],                   -- same shape the grammar reads on products
    flavour_weight       VARCHAR(20),
    flavour_profile_type VARCHAR(60),
    deductive_profile    JSONB,
    service_specs        JSONB,                    -- temperature / vessel / pour, congruent with products
    source_note          TEXT,                     -- 'seed_v1' rows are craft-standard scaffolds; grind deepens
    is_published         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_bev_prep_pub ON beverage_preparations(is_published);

-- Seed: the serves the founder named in ruling 2.4, with craft-standard
-- structural markers so the grammar can rank them. Grind lane deepens and
-- extends; any seed can be unpublished by the founder's hand.
INSERT INTO beverage_preparations (name, slug, category, description, flavour_markers, flavour_weight, flavour_profile_type, service_specs, source_note, is_published) VALUES
('Espresso','espresso','coffee','A short, intense extraction — crema, concentration, the roast spoken plainly.',ARRAY['dark chocolate','roasted','crema','bittersweet','intense'],'full','roast_intense','{"temperature":"92–96°C water, served immediately","vessel":"demitasse","pour":"25–30 ml"}','seed_v1',TRUE),
('Ristretto','ristretto','coffee','The first, sweetest half of the shot — denser, less bitter, more syrup.',ARRAY['syrupy','dark chocolate','concentrated sweetness','crema'],'full','roast_intense','{"vessel":"demitasse","pour":"15–20 ml"}','seed_v1',TRUE),
('Macchiato','macchiato','coffee','Espresso marked with a spoon of foam — the roast softened at the edge.',ARRAY['roasted','milk foam','cocoa','softened bitter'],'medium-full','roast_softened','{"vessel":"demitasse","pour":"35–40 ml"}','seed_v1',TRUE),
('Americano','americano','coffee','Espresso lengthened with hot water — the roast at conversational strength.',ARRAY['roasted','toasted grain','clean bitter','light body'],'medium','roast_long','{"vessel":"cup","pour":"150–180 ml"}','seed_v1',TRUE),
('Café au lait','cafe-au-lait','coffee','Strong coffee met with hot milk in equal measure — the breakfast pour of France.',ARRAY['steamed milk','cream','gentle roast','round','comforting'],'medium','milk_round','{"vessel":"bowl or large cup","pour":"250 ml"}','seed_v1',TRUE),
('Cappuccino','cappuccino','coffee','Espresso under stretched milk and foam in thirds — texture as much as taste.',ARRAY['milk foam','cream','cocoa dust','roasted'],'medium','milk_textured','{"vessel":"cup","pour":"150–180 ml"}','seed_v1',TRUE),
('Flat white','flat-white','coffee','A double shot under thin microfoam — milk as gloss, not blanket.',ARRAY['microfoam','cream','roasted','silky'],'medium-full','milk_gloss','{"vessel":"cup","pour":"160 ml"}','seed_v1',TRUE),
('English Breakfast tea','english-breakfast-tea','tea','A brisk black blend built for the morning table — takes milk without apology.',ARRAY['brisk','black tea','malty','tannin'],'medium','brisk_black','{"temperature":"96–100°C","vessel":"pot and cup","pour":"steep 3–4 min"}','seed_v1',TRUE),
('Earl Grey','earl-grey','tea','Black tea scented with bergamot — citrus lift over a brisk base.',ARRAY['bergamot','citrus','black tea','brisk'],'medium-light','aromatic_black','{"temperature":"96°C","pour":"steep 3 min"}','seed_v1',TRUE),
('Sencha','sencha','tea','Japan''s everyday green — grassy, umami, quietly astringent.',ARRAY['grassy','umami','green','marine'],'light','green_umami','{"temperature":"70–80°C","pour":"steep 1–2 min"}','seed_v1',TRUE),
('Matcha','matcha','tea','Stone-ground green tea whisked whole — vegetal depth with real body.',ARRAY['vegetal','umami','sweet grass','creamy body'],'medium','green_whisked','{"temperature":"75–80°C","vessel":"chawan","pour":"whisked, 70 ml"}','seed_v1',TRUE),
('Genmaicha','genmaicha','tea','Green tea with roasted rice — toast and popcorn over grass.',ARRAY['toasted rice','popcorn','green','roasted'],'light','green_toasted','{"temperature":"80–85°C","pour":"steep 2 min"}','seed_v1',TRUE)
ON CONFLICT (slug) DO NOTHING;
