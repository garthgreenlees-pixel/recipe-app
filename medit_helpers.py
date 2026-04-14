#!/usr/bin/env python3
"""Shared helpers for the Mediterranean beverage extraction session.
Import this in each batch script.
"""
import psycopg2, json, re

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    return s.strip('-')

def get_conn():
    conn = psycopg2.connect(CONN)
    conn.autocommit = True
    return conn, conn.cursor()

def P(cur, name, producer_type, region_id, country="France",
      production_philosophy=None, philosophy_description=None,
      key_personnel=None, production_details=None,
      quality_tier=None, reputation_narrative=None,
      allocation_notes=None, price_positioning=None, authority_tier=1):
    """Insert or return existing beverage_producer."""
    cur.execute("SELECT id FROM beverage_producers WHERE LOWER(name)=LOWER(%s)", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ PRODUCER: {name} exists (id={row[0]})")
        return row[0]
    slug = slugify(name)
    cur.execute("""
        INSERT INTO beverage_producers
          (name, slug, producer_type, region_id, country, production_philosophy,
           philosophy_description, key_personnel, production_details, quality_tier,
           reputation_narrative, allocation_notes, price_positioning, authority_tier,
           is_verified, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE,TRUE)
        RETURNING id
    """, (name, slug, producer_type, region_id, country,
          production_philosophy, philosophy_description,
          json.dumps(key_personnel) if key_personnel else None,
          json.dumps(production_details) if production_details else None,
          quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier))
    row = cur.fetchone()
    if row:
        print(f"  ✓ PRODUCER: {name} (id={row[0]})")
        return row[0]
    return None

def PROD(cur, name, category, producer_id, region_id, origin_country="France",
         subcategory=None, description=None, quality_tier=None,
         quality_hierarchy=None, deductive_profile=None, service_specs=None,
         flavour_markers=None, flavour_weight=None, flavour_profile_type=None,
         price_tier=None, price_range_cad=None, technical_specs=None):
    """Insert or return existing beverage_product."""
    cur.execute("SELECT id FROM beverage_products WHERE LOWER(name)=LOWER(%s)", (name,))
    row = cur.fetchone()
    if row:
        print(f"    ~ PRODUCT: {name} exists (id={row[0]})")
        return row[0]
    slug = slugify(name)
    cur.execute("""
        INSERT INTO beverage_products
          (name, slug, category, subcategory, producer_id, region_id, origin_country,
           description, quality_tier, quality_hierarchy, deductive_profile, service_specs,
           flavour_markers, flavour_weight, flavour_profile_type,
           price_tier, price_range_cad, technical_specs, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE)
        RETURNING id
    """, (name, slug, category, subcategory, producer_id, region_id, origin_country,
          description, quality_tier,
          json.dumps(quality_hierarchy) if quality_hierarchy else None,
          json.dumps(deductive_profile) if deductive_profile else None,
          json.dumps(service_specs) if service_specs else None,
          flavour_markers, flavour_weight, flavour_profile_type,
          price_tier, price_range_cad,
          json.dumps(technical_specs) if technical_specs else None))
    row = cur.fetchone()
    if row:
        print(f"    ✓ PRODUCT: {name} (id={row[0]})")
        return row[0]
    return None

def REF(cur, name, category, description, key_principles,
        skill_level="advanced", service_context=None, source_text=None,
        authority_tier=1, common_mistakes=None, pro_tips=None):
    """Insert or return existing beverage_reference (checks by name)."""
    cur.execute("SELECT id FROM beverage_references WHERE LOWER(name)=LOWER(%s)", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ REF: {name} exists (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_references
          (name, category, description, key_principles, common_mistakes, pro_tips,
           skill_level, service_context, source_text, authority_tier, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE)
        RETURNING id
    """, (name, category, description, key_principles, common_mistakes, pro_tips,
          skill_level, service_context, source_text, authority_tier))
    row = cur.fetchone()
    if row:
        print(f"  ✓ REF: {name} (id={row[0]})")
        return row[0]
    return None

def PROTOCOL(cur, name, category, beverage_family, procedure, description=None,
             rationale=None, common_errors=None, service_context=None,
             equipment_required=None, guest_communication=None,
             skill_level="advanced", authority_tier=1, source_text=None):
    """Insert or return existing service_protocol (checks by name)."""
    cur.execute("SELECT id FROM service_protocols WHERE LOWER(name)=LOWER(%s)", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ PROTOCOL: {name} exists (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO service_protocols
          (name, category, beverage_family, description, procedure, rationale,
           common_errors, service_context, equipment_required, guest_communication,
           skill_level, authority_tier, source_text, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE)
        RETURNING id
    """, (name, category, beverage_family, description, procedure, rationale,
          common_errors, service_context, equipment_required, guest_communication,
          skill_level, authority_tier, source_text))
    row = cur.fetchone()
    if row:
        print(f"  ✓ PROTOCOL: {name} (id={row[0]})")
        return row[0]
    return None

def PAIR(cur, food_description, food_category, meal_context,
         confidence, pairing_type, flavour_logic, product_id,
         food_flavour_profile=None, beverage_category="wine_still"):
    """Insert a pairing_intelligence entry.
    meal_context valid: aperitif, amuse, starter, fish_course, main, cheese,
                        pre_dessert, dessert, digestif, celebration, casual, any
    confidence valid: classic, established, suggested, adventurous, experimental
    pairing_type valid: complement, contrast, bridge, cleanse, elevate
    """
    cur.execute("""
        INSERT INTO pairing_intelligence
          (food_description, food_category, food_flavour_profile, beverage_category,
           meal_context, confidence, pairing_type, flavour_logic, beverage_product_id,
           authority_tier, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,1,TRUE) RETURNING id
    """, (food_description, food_category, food_flavour_profile, beverage_category,
          meal_context, confidence, pairing_type, flavour_logic, product_id))
    row = cur.fetchone()
    if row:
        print(f"    ✓ PAIR: {food_description[:50]}... → product {product_id}")
        return row[0]
    return None
