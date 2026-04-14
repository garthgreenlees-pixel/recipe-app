#!/usr/bin/env python3
"""Terminal 10 — Batch 2: Vintages for Kremstal + Dão, Pairings for all T10 products"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

KREMSTAL = 228
DAO      = 234

def V(region_id, year, rating, descriptor, narrative, price_traj="stable", window_from=None, window_to=None):
    cur.execute("""
        INSERT INTO beverage_vintages
          (region_id, vintage_year, quality_rating, quality_descriptor, season_narrative, price_trajectory,
           drinking_window, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,1)
        ON CONFLICT (region_id, vintage_year) DO NOTHING
    """, (region_id, year, rating, descriptor, narrative, price_traj,
          json.dumps({"from": window_from, "to": window_to}) if window_from else None))
    action = "✓" if cur.rowcount else "~"
    print(f"  {action} {year} → region {region_id}: {descriptor} ({rating})")

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR: {food_description[:55]}... → product {product_id}")

def get_product(name):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    raise ValueError(f"Product not found: {name}")

# ─── KREMSTAL VINTAGES ───────────────────────────────────────────────────
print("=== KREMSTAL VINTAGES ===")
V(KREMSTAL, 2015, 96, "exceptional",
  "The greatest Kremstal vintage of the modern era: optimal growing season with warm, dry summer "
  "and extended September warmth produced Grüner Veltliner and Riesling of extraordinary richness "
  "and concentration. The gneis and primary rock terroir delivered maximum mineral expression. "
  "Critics universally rated 2015 Kremstal at the level of the finest Wachau vintages.",
  "rising", 2017, 2035)

V(KREMSTAL, 2017, 94, "exceptional",
  "A warm, precocious vintage in Kremstal — early harvest with fully ripe conditions. "
  "The primary rock terraces produced concentrated, generous Grüner Veltliner with rich texture "
  "and early accessibility. Riesling from the Stein sites shows excellent aromatic complexity. "
  "Best drunk 2020-2028; less age-worthy than 2015 but more immediately pleasurable.",
  "stable", 2019, 2028)

V(KREMSTAL, 2019, 93, "excellent",
  "A challenging vintage redeemed by an excellent September: Kremstal's elevated sites "
  "benefited from the late warm period to achieve optimal ripeness after a cool summer. "
  "The Grüner Veltliner shows the characteristic white pepper and mineral precision of the "
  "appellation without the heat of 2017. An ideal vintage for food pairing.",
  "stable", 2021, 2030)

V(KREMSTAL, 2021, 92, "excellent",
  "Classic Kremstal vintage: cool, long growing season producing wines of pristine acidity "
  "and crystalline mineral clarity. The gneis sites produced textbook 'pfeffer' Grüner Veltliner. "
  "Excellent structure for medium-term aging. Riesling from Stein shows the salty, smoky mineral "
  "character at its most defined.",
  "stable", 2023, 2030)

V(KREMSTAL, 2022, 91, "excellent",
  "Warm and dry throughout the growing season — Kremstal produced generous, approachable "
  "Grüner Veltliner with early accessibility. Less typical than 2021 but very consistent quality. "
  "The volcanic gneis retained enough moisture to avoid over-ripeness.",
  "stable", 2023, 2028)

# ─── DÃO DOC VINTAGES ───────────────────────────────────────────────────
print("\n=== DÃO DOC VINTAGES ===")
V(DAO, 2015, 95, "exceptional",
  "The best Dão vintage in a generation — hot July followed by an exceptional August-September "
  "in the high-altitude granite Serra da Estrela foothills. The old-vine Touriga Nacional produced "
  "extraordinary concentration with the acidity preserved by altitude. Quinta da Pellada's 2015 "
  "Primus is considered the finest Dão red ever produced. Age 20-25 years with confidence.",
  "rising", 2020, 2040)

V(DAO, 2017, 93, "excellent",
  "A warm, early vintage in Dão — the altitude advantage of the Serra da Estrela sites "
  "maintained freshness despite the heat. Touriga Nacional showed generous dark fruit and "
  "soft tannins, making 2017 the most immediately accessible recent vintage. "
  "Best drunk 2020-2028; less age-worthy than 2015.",
  "stable", 2020, 2028)

V(DAO, 2019, 94, "exceptional",
  "Dão's greatest recent cool vintage — extended September hang time in the high-altitude "
  "granite terroirs produced wines of extraordinary freshness and mineral precision. "
  "The natural acidity of indigenous varieties (Touriga Nacional, Alfrocheiro) is at its "
  "most expressive. Exceptional age-worthiness for 15-20 years.",
  "rising", 2022, 2035)

V(DAO, 2020, 91, "excellent",
  "Classic Dão growing season — warm, dry, with the altitude providing cooling influence. "
  "Consistent quality across the appellation. The old-vine field blends show excellent "
  "integration of Touriga Nacional's structure with Alfrocheiro's freshness.",
  "stable", 2023, 2030)

V(DAO, 2022, 90, "excellent",
  "Good Dão vintage with consistent quality across producers. The granite terroir delivered "
  "characteristic mineral precision and freshness. The Touriga Nacional shows bright red fruit "
  "and fine tannin structure — approachable young but with 8-12 year cellaring potential.",
  "stable", 2024, 2030)

# ─── PAIRINGS ─────────────────────────────────────────────────────────────
print("\n=== PAIRING INTELLIGENCE ===")

# Load all product IDs
NIGL_PRIV = get_product("Nigl Privat Grüner Veltliner")
NIGL_GV   = get_product("Nigl Kremstal Grüner Veltliner")
SAL_RIESL = get_product("Salomon Steiner Hund Riesling")
PELL_PRIM = get_product("Quinta da Pellada Primus Dão Red")
PELL_RED  = get_product("Quinta da Pellada Dão Red")
NIEP_DAL  = get_product("Niepoort Dialogo Dão Red")
JD_SB     = get_product("Jack Daniel's Single Barrel Select Tennessee Whiskey")
JD_NO7    = get_product("Jack Daniel's Old No. 7 Tennessee Whiskey")
DICKEL    = get_product("George Dickel No. 12 Superior Grade Tennessee Whisky")
BADIA     = get_product("Antinori Badia a Passignano Chianti Classico Gran Selezione")
FONT_GS   = get_product("Fontodi Chianti Classico Gran Selezione Vigna del Sorbo")
FONT_CC   = get_product("Fontodi Chianti Classico")
CLOS_MOG  = get_product("Clos Mogador Priorat")
print(f"IDs loaded: NIGL_PRIV={NIGL_PRIV}, JD_SB={JD_SB}, BADIA={BADIA}, FONT_CC={FONT_CC}")

# Kremstal Grüner Veltliner pairings
PAIR(NIGL_PRIV, "Roasted veal with wild mushroom and tarragon cream sauce",
    "elevate", "established", "main",
    "Nigl Privat Grüner Veltliner's complexity and mineral weight creates the ideal bridge for roasted veal — the wine's wild herb and white pepper character amplifies tarragon while the mineral spine penetrates the mushroom richness. One of the great white-wine-and-veal pairings in the Austrian canon.")

PAIR(NIGL_GV, "Asparagus and morel tart with chervil beurre blanc",
    "complement", "classic", "starter",
    "The quintessential Austrian Grüner Veltliner pairing: the wine's white pepper and herb character was designed by nature for asparagus. The morel adds an earthy depth the GV's mineral spine can match; chervil echoes the wine's anise-tinged freshness.")

PAIR(NIGL_GV, "Wiener Schnitzel with lemon and parsley",
    "complement", "classic", "main",
    "The most classical Austrian pairing: Grüner Veltliner and Wiener Schnitzel. The wine's acidity cuts through the fried breadcrumb coating, lemon amplifies the GV's citrus character, and the white pepper spice bridges the veal and wine. A national institution for good reason.")

PAIR(SAL_RIESL, "Slow-baked sea bass with fennel, lemon confit, and olive oil",
    "elevate", "established", "fish_course",
    "Salomon Steiner Hund Riesling's salty mineral character and pristine acidity pairs beautifully with delicate whole fish preparations. The fennel amplifies the wine's aromatic precision while lemon confit mirrors the Riesling's characteristic citrus-mineral interplay.")

# Dão DOC pairings
PAIR(PELL_PRIM, "Slow-roasted rack of lamb with rosemary, thyme, and olive jus",
    "elevate", "established", "main",
    "Quinta da Pellada Primus's elegant granite Touriga Nacional structure — fine tannins, herb character, mineral depth — pairs magnificently with rack of lamb. The herb crust echoes the wine's dried herb character; olive jus amplifies the granite mineral backbone. Portugal's most elegant lamb pairing.")

PAIR(PELL_RED, "Roasted duck with cherry and Port reduction, root vegetables",
    "complement", "established", "main",
    "Pellada estate Dão's lighter style and red fruit character pairs naturally with duck — the wine's violet and cherry matches the fruit reduction while the root vegetables provide an earthy base for the wine's granite mineral character. The Port reduction bridges Portuguese tradition with Dão's refinement.")

PAIR(NIEP_DAL, "Grilled sardines with lemon, parsley, and flor de sal",
    "complement", "classic", "main",
    "Niepoort Dialogo Dão's fresh, light structure and vivid fruit character is the perfect match for simple grilled sardines — a classic Portuguese pairing that demonstrates why indigenous varieties farmed at altitude produce the ideal food wine. The wine's acidity cuts the fish's oil while amplifying the salt and lemon.")

# Tennessee Whiskey pairings
PAIR(JD_SB, "Bourbon pecan pie with vanilla cream",
    "complement", "classic", "dessert",
    "Jack Daniel's Single Barrel's concentrated vanilla and oak complexity finds its perfect mirror in pecan pie — the roasted nut echoes the barrel char while bourbon vanilla mirrors the whiskey's oak character. The caramel sweetness bridges the natural sweetness of single-barrel Tennessee whiskey.")

PAIR(JD_SB, "Smoked brisket with BBQ sauce",
    "complement", "classic", "casual",
    "Single Barrel Tennessee whiskey and smoked barbecue: the charcoal mellowing of the Lincoln County Process creates the natural pairing with smoke-kissed brisket. The vanilla and caramel of the oak aging integrate perfectly with BBQ sauce's sweetness and acidity.")

PAIR(JD_NO7, "Whiskey sour with fresh lemon and Angostura",
    "bridge", "classic", "aperitif",
    "Old No. 7's accessible vanilla-banana-caramel character is the benchmark mixing Tennessee whiskey — the citrus and aromatic bitters bridge the whiskey's sweetness into a balanced cocktail expression. The Lincoln County Process smoothness is what makes Old No. 7 the world's most served whiskey in bars.")

PAIR(DICKEL, "Candied bacon wrapped dates with bourbon glaze",
    "complement", "established", "amuse",
    "George Dickel No. 12's chill-filtered smoothness and corn-forward sweetness pairs perfectly with sweet-savoury preparations — the smoky bacon and bourbon glaze mirror the whisky's oak character while dates amplify the natural sweetness of the Tennessee charcoal process.")

# Chianti Classico pairings
PAIR(BADIA, "Wild boar ragù with pappardelle and Parmigiano Reggiano",
    "complement", "classic", "main",
    "Antinori Badia a Passignano Gran Selezione's concentrated Sangiovese structure — the high acidity and firm tannin of aged DOCG Chianti — meets its natural partner in wild boar ragù. The gaminess of wild boar is tamed by the wine's tannin, the pappardelle provides the pasta base, and Parmigiano's umami depth amplifies the wine's complex finish.")

PAIR(FONT_GS, "Bistecca alla Fiorentina with rosemary oil and sea salt",
    "complement", "classic", "main",
    "The most Florentine pairing imaginable: Fontodi Gran Selezione and Bistecca alla Fiorentina. Sangiovese's natural acidity and cherry character cuts through the intense marbling of T-bone beef while the wine's iron mineral character mirrors the charred crust. Rosemary echoes the wine's dried herb notes.")

PAIR(FONT_CC, "Spaghetti all'amatriciana with guanciale and Pecorino",
    "complement", "classic", "main",
    "Fontodi Chianti Classico's bright Sangiovese acidity and sour cherry character is the definitive Italian table wine for pasta with cured pork — the wine cuts through guanciale fat while amplifying the tomato's acidity. Pecorino's sharpness bridges the wine's freshness with the pasta's richness.")

PAIR(FONT_CC, "Aged Parmigiano Reggiano with truffle honey",
    "elevate", "established", "cheese",
    "Chianti Classico's Sangiovese structure — high acidity, cherry fruit, leather — pairs classically with aged Parmigiano. The wine's acidity cuts the cheese's richness while the cherry fruit and leather notes complement the aged umami. Truffle honey amplifies both the wine's earthiness and the cheese's savory depth.")

PAIR(CLOS_MOG, "Slow-roasted leg of lamb with wild herbs and black olives",
    "complement", "classic", "main",
    "Clos Mogador's Grenache-dominant llicorella Priorat — dark fruit, dried herbs, black olive, mineral slate — pairs perfectly with Mediterranean herb-roasted lamb. The wild herbs (rosemary, thyme, herbes de Provence) mirror the wine's garrigue character; black olives amplify the wine's distinctive Priorat olive note. The lamb fat softens the wine's concentrated tannin.")

cur.close()
conn.close()
print("\n✅ Terminal 10 Batch 2 — Vintages + Pairings complete.")
