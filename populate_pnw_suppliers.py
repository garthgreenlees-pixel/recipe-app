#!/usr/bin/env python3
"""
PNW Supplier and Restaurant Data Population
Sashimi standard — every entity web-verified.
Corrected for actual DB schema constraints.
"""
import psycopg2
from psycopg2.extras import RealDictCursor

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

# ─────────────────────────────────────────────
# STEP 1: 15 verified PNW suppliers
# ─────────────────────────────────────────────
SUPPLIERS = [
    # BC
    {
        "name": "Moon Bay Ocean Farm",
        "city": None,
        "state_province": "BC",
        "country": "CA",
        "supplier_type": "producer",
        "website": None,
        "notes": "Kelp producer. Supplies Published on Main (Michelin ★) — 200kg pickled annually. Source: Scout Magazine Mar 2025.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Scout Magazine March 2025 — Published on Main spring menu",
    },
    {
        "name": "Wildest Foods",
        "city": None,
        "state_province": "BC",
        "country": "CA",
        "supplier_type": "producer",
        "website": None,
        "notes": "Wild foraged nettle and wild greens. Supplies Published on Main (Michelin ★). Source: Scout Magazine Mar 2025.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Scout Magazine March 2025",
    },
    {
        "name": "North Arm Farm",
        "city": "Pemberton",
        "state_province": "BC",
        "country": "CA",
        "supplier_type": "producer",
        "website": None,
        "notes": "Jordan & Trish Sturdy. 45 acres mixed vegetables and fruit, Pemberton BC. Supplies Published on Main + Savoury Chef. Est. 1995. Source: Scout Mar 2025 + Vancouver Guardian Feb 2026.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Scout Magazine March 2025 + Vancouver Guardian February 2026",
    },
    {
        "name": "Vive le Veg",
        "city": None,
        "state_province": "BC",
        "country": "CA",
        "supplier_type": "producer",
        "website": None,
        "notes": "Green garlic and alliums. Supplies Published on Main (Michelin ★). Source: Scout Magazine Mar 2025.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Scout Magazine March 2025",
    },
    {
        "name": "Cropthorne Farm",
        "city": None,
        "state_province": "BC",
        "country": "CA",
        "supplier_type": "producer",
        "website": None,
        "notes": "Seasonal produce, BC. Named by Chef Gus Stieffenhofer-Brandson (Published on Main) in interview. Source: Vancouver Guardian Feb 2026.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Vancouver Guardian February 2026",
    },
    {
        "name": "Glorious Organics",
        "city": None,
        "state_province": "BC",
        "country": "CA",
        "supplier_type": "producer",
        "website": None,
        "notes": "Mark Cormier. Certified organic 3.5-acre farm, 40-year history, Fraser Valley. 30+ salad varieties including Tiny Ivy potatoes. Supplies BOTH Published on Main AND St. Lawrence — two Michelin ★ restaurants. Source: Georgia Straight Aug 2025 + Chef Gus interviews.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Georgia Straight August 2025 + multiple chef interviews",
    },
    {
        "name": "Jane Squier — Salt Spring Citrus",
        "city": "Salt Spring Island",
        "state_province": "BC",
        "country": "CA",
        "supplier_type": "producer",
        "website": None,
        "notes": "43 types of citrus including Buddha's hand, finger limes, passion fruit. First citrus grower in Canada. Science-based sustainable growing. Supplies Burdock & Co (Michelin ★). Source: Michelin Guide interview Dec 2024.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Michelin Guide interview December 2024",
    },
    {
        "name": "Mikuni Wild Harvest",
        "city": None,
        "state_province": "BC",
        "country": "CA",
        "supplier_type": "producer",
        "website": None,
        "notes": "Wild foods exploration and supply company, BC. Source: Savoury Chef supplier showcase.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Savoury Chef website",
    },
    {
        "name": "Domenica Fiore",
        "city": "Vancouver",
        "state_province": "BC",
        "country": "CA",
        "supplier_type": "producer",
        "website": "domenicafiore.com",
        "notes": "Award-winning premium organic olive oil. Estate in Orvieto, Italy. Certified organic, numbered and dated bottles. Source: Savoury Chef supplier showcase.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Savoury Chef website",
    },
    # WA
    {
        "name": "Neils Bigleaf Maple Syrup",
        "city": "Acme",
        "state_province": "WA",
        "country": "US",
        "supplier_type": "producer",
        "website": None,
        "notes": "Washington-made bigleaf maple syrup with near-umami flavour profile, distinct from Eastern maple. Supplies Canlis (Food & Wine #2 US). Source: Seattle Magazine Nov 2025.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Seattle Magazine November 2025",
    },
    {
        "name": "Rockridge Orchards",
        "city": None,
        "state_province": "WA",
        "country": "US",
        "supplier_type": "producer",
        "website": None,
        "notes": "Apple-based balsamic vinegar, WA. Supplies Canlis. Source: Seattle Magazine Nov 2025.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Seattle Magazine November 2025",
    },
    {
        "name": "Westland Distillery",
        "city": "Seattle",
        "state_province": "WA",
        "country": "US",
        "supplier_type": "producer",
        "website": None,
        "notes": "American single malt whisky aged in Quercus garryana (Garry oak, native to the I-5 corridor — unique terroir-driven spirit). Supplies Canlis beverage program. Source: Seattle Magazine Nov 2025.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Seattle Magazine November 2025",
    },
    # OR
    {
        "name": "Gathering Together Farms",
        "city": None,
        "state_province": "OR",
        "country": "US",
        "supplier_type": "producer",
        "website": None,
        "notes": "Oregon seasonal produce. Supplies Kann (#27 North America 50 Best 2024, JBF Best New Restaurant 2023). Source: Civil Eats Sep 2022.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Civil Eats September 2022",
    },
    {
        "name": "Groundwork Organics",
        "city": None,
        "state_province": "OR",
        "country": "US",
        "supplier_type": "producer",
        "website": None,
        "notes": "Certified organic seasonal produce, Oregon. Supplies Kann. Source: Civil Eats Sep 2022.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Civil Eats September 2022",
    },
    {
        "name": "Maryhill Winery",
        "city": None,
        "state_province": "OR",
        "country": "US",
        "supplier_type": "producer",
        "website": None,
        "notes": "Berries, Columbia Gorge, OR/WA border. Supplies Kann. Source: Civil Eats Sep 2022.",
        "is_active": True,
        "verified_date": "2026-04-07",
        "verification_source": "Civil Eats September 2022",
    },
]

# ─────────────────────────────────────────────
# STEP 2: ingredient_products
# Note: category must be in DB enum; no spirits/sweeteners category exists
# Westland whisky omitted — no spirits category in ingredient_products
# Maple syrup → spices_seasonings (closest for a finishing condiment)
# ─────────────────────────────────────────────
PRODUCTS = [
    {
        "name": "BC Harvested Kelp — Moon Bay",
        "category": "produce_specialty",
        "description": "Hand-harvested kelp, Sunshine Coast BC. Moon Bay Ocean Farm. Used by Published on Main (Michelin ★) — Chef pickles 200kg annually.",
        "origin_country": "CA",
        "region_tags": ["BC", "Sunshine Coast", "Pacific"],
        "purveyor_tier": "specialty",
        "supplier_name": "Moon Bay Ocean Farm",
    },
    {
        "name": "Wild Nettle Greens — BC Foraged",
        "category": "produce_specialty",
        "description": "Wild foraged nettle greens, BC. Wildest Foods. Used by Published on Main (Michelin ★).",
        "origin_country": "CA",
        "region_tags": ["BC"],
        "purveyor_tier": "specialty",
        "supplier_name": "Wildest Foods",
    },
    {
        "name": "Pemberton Seasonal Vegetables — North Arm Farm",
        "category": "produce_specialty",
        "description": "Mixed seasonal vegetables and fruit. North Arm Farm, Pemberton BC. Jordan & Trish Sturdy, 45 acres, est. 1995. Supplies Published on Main and Savoury Chef.",
        "origin_country": "CA",
        "region_tags": ["BC", "Pemberton", "Sea to Sky"],
        "purveyor_tier": "specialty",
        "supplier_name": "North Arm Farm",
    },
    {
        "name": "Green Garlic — Vive le Veg",
        "category": "produce_specialty",
        "description": "Fresh green garlic and alliums, BC. Vive le Veg. Used by Published on Main (Michelin ★).",
        "origin_country": "CA",
        "region_tags": ["BC"],
        "purveyor_tier": "specialty",
        "supplier_name": "Vive le Veg",
    },
    {
        "name": "Cropthorne Farm Seasonal Produce",
        "category": "produce_specialty",
        "description": "Seasonal produce, BC. Cropthorne Farm. Used by Published on Main — named directly by Chef Gus Stieffenhofer-Brandson.",
        "origin_country": "CA",
        "region_tags": ["BC"],
        "purveyor_tier": "specialty",
        "supplier_name": "Cropthorne Farm",
    },
    {
        "name": "Organic Salad Greens (30+ Varieties) — Glorious Organics",
        "category": "produce_specialty",
        "description": "30+ varieties of certified organic salad greens. Glorious Organics, Fraser Valley BC. Mark Cormier, 40-year farm. Supplies Published on Main AND St. Lawrence — two Michelin ★ restaurants simultaneously.",
        "origin_country": "CA",
        "region_tags": ["BC", "Fraser Valley"],
        "purveyor_tier": "specialty",
        "supplier_name": "Glorious Organics",
    },
    {
        "name": "Tiny Ivy Potatoes — Glorious Organics",
        "category": "produce_specialty",
        "description": "Rare heritage potato variety. Glorious Organics, Fraser Valley BC. Featured in St. Lawrence Table Champêtre menu August 2025.",
        "origin_country": "CA",
        "region_tags": ["BC", "Fraser Valley"],
        "purveyor_tier": "specialty",
        "supplier_name": "Glorious Organics",
    },
    {
        "name": "Salt Spring Island Citrus — Jane Squier",
        "category": "produce_specialty",
        "description": "43 citrus varieties including Buddha's hand, finger limes, passion fruit. Jane Squier, first citrus grower in Canada, Salt Spring Island BC. Science-based sustainable growing. Used by Burdock & Co (Michelin ★).",
        "origin_country": "CA",
        "region_tags": ["BC", "Salt Spring Island", "Gulf Islands"],
        "purveyor_tier": "specialty",
        "supplier_name": "Jane Squier — Salt Spring Citrus",
    },
    {
        "name": "Washington Bigleaf Maple Syrup — Neils",
        "category": "spices_seasonings",
        "description": "Bigleaf maple (Acer macrophyllum) syrup, Acme WA. Neils Bigleaf Maple Syrup. Near-umami flavour profile — distinct from Eastern sugar maple. Used by Canlis (Food & Wine #2 restaurant in US).",
        "origin_country": "US",
        "region_tags": ["WA", "Pacific Northwest"],
        "purveyor_tier": "specialty",
        "supplier_name": "Neils Bigleaf Maple Syrup",
    },
    {
        "name": "Apple Balsamic Vinegar — Rockridge Orchards",
        "category": "oils_vinegars",
        "description": "Apple-based balsamic vinegar, Washington state. Rockridge Orchards. Used by Canlis.",
        "origin_country": "US",
        "region_tags": ["WA", "Pacific Northwest"],
        "purveyor_tier": "specialty",
        "supplier_name": "Rockridge Orchards",
    },
    {
        "name": "Oregon Seasonal Vegetables — Gathering Together Farms",
        "category": "produce_specialty",
        "description": "Seasonal vegetables, Oregon. Gathering Together Farms. Used by Kann (#27 North America 50 Best 2024).",
        "origin_country": "US",
        "region_tags": ["OR", "Pacific Northwest", "Willamette Valley"],
        "purveyor_tier": "specialty",
        "supplier_name": "Gathering Together Farms",
    },
    {
        "name": "Oregon Certified Organic Produce — Groundwork",
        "category": "produce_specialty",
        "description": "Certified organic seasonal produce, Oregon. Groundwork Organics. Used by Kann.",
        "origin_country": "US",
        "region_tags": ["OR", "Pacific Northwest"],
        "purveyor_tier": "specialty",
        "supplier_name": "Groundwork Organics",
    },
    {
        "name": "Columbia Gorge Berries — Maryhill",
        "category": "produce_specialty",
        "description": "Fresh seasonal berries, Columbia Gorge OR/WA border. Maryhill Winery farm. Used by Kann.",
        "origin_country": "US",
        "region_tags": ["OR", "Columbia Gorge", "Pacific Northwest"],
        "purveyor_tier": "specialty",
        "supplier_name": "Maryhill Winery",
    },
]


def main():
    conn = psycopg2.connect(CONN)
    conn.autocommit = False
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # ── STEP 1: Insert suppliers ──────────────────────────────
    print("STEP 1: Inserting suppliers...")
    inserted_suppliers = 0
    skipped_suppliers = 0
    for s in SUPPLIERS:
        try:
            cur.execute("""
                INSERT INTO suppliers (name, city, state_province, country, supplier_type,
                    website, notes, is_active, verified_date, verification_source)
                VALUES (%(name)s, %(city)s, %(state_province)s, %(country)s, %(supplier_type)s,
                    %(website)s, %(notes)s, %(is_active)s, %(verified_date)s, %(verification_source)s)
                ON CONFLICT (name) DO NOTHING
            """, s)
            if cur.rowcount > 0:
                inserted_suppliers += 1
                print(f"  ✓ {s['name']}")
            else:
                skipped_suppliers += 1
                print(f"  ~ SKIP (already exists): {s['name']}")
        except Exception as e:
            print(f"  ✗ ERROR on {s['name']}: {e}")
            conn.rollback()
            conn.autocommit = False

    conn.commit()
    print(f"\nSuppliers: {inserted_suppliers} inserted, {skipped_suppliers} skipped.\n")

    # ── Build supplier name → id lookup ──────────────────────
    cur.execute("SELECT id, name FROM suppliers")
    supplier_id = {row["name"]: row["id"] for row in cur.fetchall()}

    # ── STEP 2: Insert ingredient_products ───────────────────
    print("STEP 2: Inserting ingredient products...")
    inserted_products = 0
    skipped_products = 0
    product_id = {}

    for p in PRODUCTS:
        try:
            cur.execute("""
                INSERT INTO ingredient_products (name, category, description, origin_country,
                    region_tags, purveyor_tier)
                VALUES (%(name)s, %(category)s, %(description)s, %(origin_country)s,
                    %(region_tags)s, %(purveyor_tier)s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id
            """, p)
            row = cur.fetchone()
            if row:
                product_id[p["name"]] = row["id"]
                inserted_products += 1
                print(f"  ✓ {p['name']}")
            else:
                # Already exists — fetch the id
                cur.execute("SELECT id FROM ingredient_products WHERE name = %s", (p["name"],))
                existing = cur.fetchone()
                if existing:
                    product_id[p["name"]] = existing["id"]
                skipped_products += 1
                print(f"  ~ SKIP (already exists): {p['name']}")
        except Exception as e:
            print(f"  ✗ ERROR on {p['name']}: {e}")
            conn.rollback()
            conn.autocommit = False

    conn.commit()
    print(f"\nProducts: {inserted_products} inserted, {skipped_products} skipped.\n")

    # ── STEP 3: Link products to suppliers ───────────────────
    print("STEP 3: Creating product-supplier links (role=ORIGIN, is_primary=true)...")
    linked = 0
    link_errors = 0

    for p in PRODUCTS:
        pid = product_id.get(p["name"])
        sid = supplier_id.get(p["supplier_name"])
        if not pid:
            print(f"  ✗ No product_id for: {p['name']}")
            continue
        if not sid:
            print(f"  ✗ No supplier_id for: {p['supplier_name']}")
            continue
        try:
            cur.execute("""
                INSERT INTO product_suppliers (product_id, supplier_id, role, is_primary)
                VALUES (%s, %s, 'ORIGIN', true)
                ON CONFLICT (product_id, supplier_id, role) DO NOTHING
            """, (pid, sid))
            if cur.rowcount > 0:
                linked += 1
                print(f"  ✓ {p['name']} → {p['supplier_name']}")
            else:
                print(f"  ~ SKIP (link exists): {p['name']} → {p['supplier_name']}")
        except Exception as e:
            print(f"  ✗ ERROR linking {p['name']} → {p['supplier_name']}: {e}")
            link_errors += 1
            conn.rollback()
            conn.autocommit = False

    conn.commit()
    print(f"\nLinks: {linked} created, {link_errors} errors.\n")

    # ── SUMMARY ──────────────────────────────────────────────
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    cur.execute("SELECT COUNT(*) as n FROM suppliers WHERE is_active = true")
    print(f"Total active suppliers:    {cur.fetchone()['n']}")

    cur.execute("SELECT COUNT(*) as n FROM ingredient_products")
    print(f"Total ingredient products: {cur.fetchone()['n']}")

    cur.execute("SELECT COUNT(*) as n FROM product_suppliers")
    print(f"Total product-supplier links: {cur.fetchone()['n']}")

    print("\nNew PNW suppliers by region:")
    cur.execute("""
        SELECT state_province, COUNT(*) as n
        FROM suppliers
        WHERE verified_date = '2026-04-07'
        GROUP BY state_province
        ORDER BY state_province
    """)
    for row in cur.fetchall():
        print(f"  {row['state_province']}: {row['n']}")

    print("\nNew suppliers with their products:")
    cur.execute("""
        SELECT s.name as supplier, ip.name as product, ps.role
        FROM suppliers s
        JOIN product_suppliers ps ON s.id = ps.supplier_id
        JOIN ingredient_products ip ON ip.id = ps.product_id
        WHERE s.verified_date = '2026-04-07'
        ORDER BY s.state_province, s.name
    """)
    for row in cur.fetchall():
        print(f"  [{row['role']}] {row['supplier']} → {row['product']}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
