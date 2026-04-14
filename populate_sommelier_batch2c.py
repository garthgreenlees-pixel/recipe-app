#!/usr/bin/env python3
"""Canon 4 Batch 2c — entries 16-18: Service Protocols, Business, Food & Wine Pairing"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """INSERT INTO technique_references
  (name,slug,category,tier_level,authority_tier,source_book,
   description,key_principles,common_mistakes,pro_tips,trigger_keywords)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""

ENTRIES = [

{
"name": "MS Theory — Service Protocols",
"slug": "ms-theory-service-protocols",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers — Service Manual",
"description": """Wine service is the practical dimension of the Master Sommelier examination — the component where candidates are judged not only on knowledge but on physical execution, timing, guest communication, and professional demeanour under examination pressure. The MS practical service exam is conducted in a simulated fine dining environment and requires candidates to execute a complete tableside service sequence across multiple beverage types, including still wine presentation and opening, sparkling wine service, decanting, and by-the-glass service.

Professional service is not ceremony for its own sake. Each service protocol exists for a functional reason: bottle presentation confirms the wine before opening; the sommelier's thumb in the punt during pouring prevents fingerprints on the label; decanting removes sediment and aerates wine; temperature management preserves the wine's intended profile. A Master Sommelier can explain WHY every element of service exists, not merely perform it.""",

"key_principles": """APPROACH SEQUENCE (tableside sequence)
1. Approach within 2 minutes of guests being seated. Introduce yourself: 'Good evening. My name is [name] and I'll be your sommelier tonight.'
2. Present the wine list (to the host or the person who requested it). Step back. Allow time to review. Do not hover.
3. Return promptly. Offer recommendations proactively based on menu choices, budget signals, or stated preferences.
4. Confirm the selection by reading it back: 'Excellent choice — that's the [producer], [region], [vintage]. I'll bring that right out.'

STILL WINE SERVICE
Presentation: Bring the bottle in a wine basket or by hand (basket appropriate for aged wine with potential sediment; hand carriage for young wine). Present the bottle label-facing-the-host. Confirm aloud: 'This is the [producer], [wine name], [vintage], [region].' Wait for host confirmation. Do not open without confirmation.
Opening:
  1. Cut the capsule below the second lip of the bottle (not the first) — this prevents the wine from touching the cut foil and potentially acquiring a metallic taste. Use the foil cutter or the knife on the waiter's friend.
  2. Wipe the top of the cork and bottle neck with a service cloth.
  3. Insert the worm of the waiter's friend at a slight angle, then straighten. Engage the first lever. Pull smoothly. Engage the second lever. Extract the remaining cork. Remove the cork silently — no 'pop' for still wine.
  4. Inspect the cork: check for any mould, faults, or excessive compression. Place the cork to the right of the host (not on the table; off to the side on a bread plate or cork dish) for the host to inspect if desired. Do NOT sniff the cork dramatically — it reveals nothing about the wine's condition.
  5. Wipe the bottle mouth with the service cloth.
  6. Pour a small tasting pour (25–30ml) for the host. Wait. The host should assess the wine's condition.
  7. If the host approves, proceed around the table. Ladies first (traditional European service); or guest of honour first; then proceeding clockwise. Host last.
  8. Service amounts: 125ml for standard glass (1/3 of a standard 375ml pour for a wine glass; never fill beyond 2/3 of the glass).
  9. Thumb position: right hand on the bottle body; thumb in the punt; the label faces up and toward the guest during pouring so they can see it.
  10. Twist the bottle slightly at the end of each pour to prevent dripping. Use the service cloth to catch any drips.
  11. Place the bottle on the table to the right of the host, label facing outward (so guests can see the label).

SPARKLING WINE SERVICE
Temperature: Champagne and sparkling wine served at 6–8°C. Under no circumstances open warm sparkling wine — the pressure increase will cause an uncontrolled opening.
Opening: The Six-Step Champagne Protocol:
  1. Cut the foil at or below the wire cage.
  2. Loosen the wire cage (muselet) with 6 half-turns counterclockwise. Do NOT remove the cage — hold it in place with your thumb over the cork.
  3. Tilt the bottle at 45°. Point the cork away from guests and away from any glass.
  4. Hold the cork and cage together firmly with one hand. With the other hand, rotate the BOTTLE (not the cork) slowly.
  5. As the cork loosens, resist its movement — allow it to emerge slowly, silently. The CO₂ should exhale as a gentle sigh, not explode with a pop. A loud pop wastes gas and may mean the next glass is flat.
  6. Wipe the bottle neck. Taste/present the poured glass to the host. Proceed with service.
  Note: The host is NOT expected to sniff or extensively assess a Champagne opening; a brief visual check and taste is appropriate.

DECANTING PROTOCOL
Two purposes: (1) Sediment removal in older wines; (2) Aeration (breathing) in young, tannic, or reductive wines.
When to decant: Vintage Port (always — sediment forms after 5–8 years in bottle); aged red wine with 10+ years in bottle (inspect for sediment by holding to light); young tannic red wine (Barolo, young Napa Cabernet — 30–60 minutes contact with air opens them dramatically); reductive wine (struck flint on nose — exposure to air blows off reduction).
When NOT to decant: Fragile old wines (over 30 years — they may fade within 10–15 minutes of decanting); any wine the host has specifically declined decanting for; most white wines (exception: rich oxidative whites, white Burgundy, skin-contact whites).
Decanting procedure:
  1. Allow the bottle to stand upright for minimum 24 hours if from a horizontal cellar (sediment settles to the bottom punt).
  2. Source the decanter: rinse with a small amount of the same wine (or neutral still water) before decanting. The decanter should be clean and odour-free.
  3. Hold the bottle in one hand, the decanter in the other. Tilt the bottle slowly. Hold a candle or light source below the neck of the bottle. Begin pouring slowly in a continuous stream.
  4. Watch the bottle's shoulder — sediment will approach the neck. Stop pouring when you see sediment crossing the shoulder toward the neck. Never pour sediment into the decanter.
  5. Typically, 25–50ml of wine (and sediment) will remain in the bottle. This is acceptable loss.
  6. Set the decanter on the table (on a coaster or service plate) with the label of the decanter (if marked) or the wine label displayed.
  Double decanting: For young tannic wines needing extended aeration — decant into the decanter, allow to breathe 30–60 minutes (or as required), then return to the original (rinsed) bottle for presentation. This retains the original label and bottle for the table while still providing aeration.

BY-THE-GLASS SERVICE
Each glass poured from a bottle at the table should be presented as a full service: describe the wine, pour the appropriate measure, ensure the glass is placed correctly. 'By the glass' does not mean pouring without attention.
Glass management: Ensure correct glass for each wine type (Bordeaux glass for full-bodied reds; Burgundy/Pinot glass for lighter reds and Chardonnay; flute or coupe for Champagne; white wine glass for crisp whites; Riedel Sommelier series for fine wine).
Pour cost management: By-the-glass portion should be measured (typically 150–175ml for a standard BTG glass) to maintain pour cost targets.

TEMPERATURE MANAGEMENT
Serving temperature ranges:
  Sparkling wines: 6–8°C (Champagne and premium traditional method) · 7–10°C (Prosecco, Cava).
  Full-bodied whites (Chardonnay, white Burgundy): 12–14°C.
  Light-medium whites (Sauvignon Blanc, Pinot Grigio, Riesling): 8–12°C.
  Rosé: 8–12°C.
  Light reds (Beaujolais, Pinot Noir): 14–16°C.
  Medium reds (Côtes du Rhône, Chianti, Merlot): 16–18°C.
  Full-bodied reds (Barolo, Napa Cabernet, Shiraz): 18°C (not 'room temperature' — most dining rooms are 20–24°C; serve at 18°C and the guest's room temperature will warm it).
  Sweet/dessert wines: 6–8°C.
  Port — Vintage: 18°C. Port — Tawny/Colheita: 12–14°C (slightly chilled).

GLASSWARE — Selection and Polishing
Standard glass shapes:
  Bordeaux glass: Tall, straight sides — concentrates blackcurrant and tannic reds.
  Burgundy/Pinot Noir glass: Wide, balloon bowl — diffuses delicate aromatics; also used for fine Chardonnay.
  White wine glass: Narrower bowl — retains cool temperature.
  Champagne flute: Tall, narrow — preserves carbonation, concentrates aroma; alternative coupe (for expression of broader aromatics in aged Champagne — coupe loses carbonation faster).
  Sweet wine glass: Smaller — appropriate pour for high-sugar, high-alcohol wines.
  Port glass: Narrow, smaller — appropriate serve size.
Polishing: Use clean, lint-free cloth; steam from hot water or kettle; polish before each service. Lipstick, oils, detergent residue must be removed — they affect the wine's aroma and foam in sparkling wines.

COMPLAINT HANDLING
Corked wine (TCA): If the guest states the wine is corked, evaluate it yourself. If confirmed: 'I agree — I'll bring a replacement immediately.' Remove the bottle; replace at no charge; notify your floor manager. Document in service log.
Oxidised wine: If a by-the-glass wine tastes flat, oxidised, or slightly vinegary — replace it. Bottles opened more than 2 days (without preservation) should be rotated off the BTG list.
Incorrect temperature: If a guest receives a wine too warm or too cold — remedy immediately. Warm wine: ice bucket. Cold wine: leave out of ice, remove from refrigerator. Never apologise excessively; remediate efficiently and confidently.

CELLAR MANAGEMENT
FIFO (First In, First Out): Wine received earliest should be sold first, unless the wine benefits from ageing (vintage Port, aged Bordeaux).
Par levels: Maintain minimum par stock for each BTG and BTB wine. Trigger reorders when stock falls to par level.
Storage: 12–14°C, 60–70% humidity, horizontal bottles (to keep corks moist), away from vibration and light. Separate storage for white wines (slightly cooler) and red wines.
Inventory: Weekly or bi-weekly. Count all stock including reserve cellar. Record losses (breakage, spillage, complementary pours).""",

"common_mistakes": """1. Cutting the capsule above the first lip instead of below the second — wine that contacts the cut foil edge picks up a metallic taste; always cut below the second collar.
2. Twisting the cork instead of the bottle when opening sparkling wine — you must rotate the bottle while holding the cork/cage stationary; this gives maximum control over cork release pressure.
3. Placing the cork on the table in front of the host — the cork goes to the side on a plate or dedicated holder; it is available for inspection if the host wishes, but placing it in the centre of the table is not a service convention.
4. Sniffing the cork theatrically — the condition of the cork tells you almost nothing about the wine's condition. The wine itself must be assessed. Holding the cork up and sniffing it in an exaggerated way is both uninformative and poor theatre.
5. Over-decanting fragile old wine — wines over 25–30 years old may fade rapidly after decanting; the window of peak expression may be 10–30 minutes. Decant just before service; monitor the wine.
6. Not adjusting for table temperature — if a dining room is 23°C and the wine is served at 'cellar temperature' (14°C), the wine will be 18°C within 20 minutes in the glass. Adjust service temperature downward accordingly, especially for reds.
7. Ignoring BTG wine oxidation — an open bottle of red wine left without preservation for more than 24 hours is progressively deteriorating. Rotating BTG wines frequently and using preservation systems (Coravin, Vacu Vin) is service quality, not cost management only.
8. Failing to confirm the wine verbally before opening — at MS exam level, not confirming the label and vintage before opening is an automatic service error. Always read the label aloud to the host.""",

"pro_tips": """1. In the MS service exam, speed and confidence are assessed alongside technical accuracy. Hesitation is interpreted as uncertainty. Practise the full service sequence (presentation, cut, open, taste, pour, table placement) until it is completely fluent at a rehearsed pace — not rushed, not slow.
2. Decanting a wine in front of a guest is one of the highest-value sommelier moments — it is an opportunity to explain why (this wine needs air / this wine has sediment / this wine will reward 45 minutes of breathing), which educates and engages the guest simultaneously.
3. Know by heart which wines classically require decanting: young Barolo (minimum 1 hour), young Hermitage (1–2 hours), vintage Port (minimum 1 hour for younger vintages, 30 minutes for older), young Napa Cabernet (30–60 minutes), reductive Burgundy (15–30 minutes to blow off reduction).
4. The coupe glass for Champagne has a legitimate application: for aged vintage Champagne (over 10 years on cork), the broader surface area of the coupe allows the autolytic, tertiary aromas (toast, brioche, honey) to express more completely than the narrow flute.
5. Practice Coravin technique if your programme uses it — the Coravin needle allows wine to be removed from a bottle without removing the cork, replacing the extracted wine with argon gas. Proper Coravin use (angle, needle placement, pouring technique) is a practical skill at the premium BTG level.
6. Temperature service is the most commonly neglected service standard in professional dining. Build a personal protocol: every white wine and sparkling wine goes into service with a temperature check; every red wine served in a warm room should be served slightly below the target temperature.
7. For the MS practical exam: the examiners look for natural guest interaction, not a robotic protocol recitation. Speak to the 'guest' (the examiner) naturally while executing the protocol — 'I'll just let this breathe for a moment before I pour' shows fluency.
8. Know the complimentary pour protocol — when a wine is replaced due to a fault, the replacement pour is typically full, at no charge. If the guest has already consumed most of the bottle before noting the fault, use judgement — at MS level, the answer is always to resolve the guest's experience first, cost second.""",
"trigger_keywords": json.dumps(["wine service", "decanting", "sparkling wine service", "sommelier service", "bottle presentation", "MS exam service", "tableside service", "temperature service", "complaint handling", "cellar management"])
},

{
"name": "MS Theory — Business of the Sommelier",
"slug": "ms-theory-business-of-sommelier",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers — Beverage Business",
"description": """The Master Sommelier examination tests not only knowledge and service but the commercial intelligence to run a wine programme as a business. A Master Sommelier who cannot cost a wine list, calculate a pour cost, design a list that serves both the guest experience and the restaurant's profitability, or manage vendor relationships is professionally incomplete. The business components of the MS exam reflect the reality of the profession: most Master Sommeliers manage multi-million dollar beverage inventories and must operate with hospitality business discipline.

The business of the sommelier encompasses wine list design, inventory management, financial modelling of the beverage programme, staff training, and vendor relationship management. Each of these domains has professional standards and best practices. A Master Sommelier candidate must demonstrate command of all of them.""",

"key_principles": """WINE LIST DESIGN
Organisation approaches: By region (traditional — requires wine knowledge from the guest or sommelier assistance); by style (accessible — light to full-bodied, grouped by character); by price (transactional — least sommelier-forward); progressive (light-to-full within region or varietal groupings — the current professional standard). Most fine dining lists combine regional organisation with progressive structure within each region.

Depth vs breadth: A list with 8 excellent producers per major region (200 selections) is more useful and more serviceable than a list with 50 producers per region (800 selections). Depth in your signature categories (if you are a French restaurant, your Burgundy list should have 40–60 selections); breadth across supporting categories. Never list a wine you cannot speak confidently about.

Price range: Every category should have an accessible entry price (within the first 30% of the menu price range for that category), a value middle (the largest selection), and a premium ceiling. A list with no wines under $50 loses casual diners; a list with no wines over $200 loses high-value celebrations.

By-the-glass (BTG) programme: BTG wines drive the highest per-seat beverage revenue and provide the widest guest accessibility. Minimum 6–8 wines by the glass; ideal 12–16 for a full-service restaurant. BTG wines should span: 2 sparkling, 2–3 white, 1 rosé, 2–3 red, 1 dessert/fortified. Each BTG wine should be replaced within 3–4 days of opening (or sooner with preservation).

List maintenance: Price every wine. Review pricing quarterly — supplier cost increases must be passed through or margins suffer. Remove sold-out wines immediately (a guest who orders a wine you don't have is a service failure). Mark vintage changes.

FINANCIAL MANAGEMENT

Pour Cost: The most fundamental beverage metric. Pour cost % = (Cost of goods sold / Revenue) × 100. For wine by the glass: Bottle cost ÷ Number of pours per bottle × Retail price per glass = pour cost %. Target pour cost for wine BTG: 25–33%. Premium programmes may run 28–35% on fine wine BTG.

Markup structures: Standard industry markups vary by price tier. Low-cost wines (under $12 wholesale): 3.5–4× markup. Mid-range ($12–30): 2.5–3× markup. Premium ($30–60): 2–2.5× markup. High-end ($60+): 1.5–2× markup. Flat markup destroys value perception at the high end; taper as price increases.

Bottle vs glass economics: A 750ml bottle provides 4–5 full glasses (125–150ml each) plus a host taste. A BTG wine at $15/glass on a $40 bottle = 4 glasses × $15 = $60 revenue on $40 cost = $20 gross profit, 67% gross margin = 33% pour cost. If the bottle is sold for $75: $75 revenue on $40 cost = 47% gross margin = 53% pour cost. Both are acceptable; the BTG programme provides more flexibility to maximise gross profit per seat.

Inventory management: FIFO (First In, First Out): the oldest stock of any SKU should sell before newer deliveries. LIFO (Last In, First Out) is inappropriate for food and beverage (wine is not a commodity; it changes with age). Par levels: maintain a minimum 2 weeks of par for any wine on the list; 4 weeks for anchor BTG wines; 6–8 weeks for fine wine purchases requiring lead time.

Dead stock identification: Any wine that has not sold in 90 days should be reviewed. Is the price too high? Is it not being recommended? Does the staff know the wine? Move dead stock proactively through: staff education, feature/promotion, sommelier recommendation, offering by-the-glass.

STAFF TRAINING
Wine knowledge for FOH staff: The minimum standard for any server is the ability to describe each wine on the menu in 2–3 sensory sentences and recommend a food pairing. For sommeliers and lead servers: full knowledge of all producers, vintages, and regions represented.
Training formats: Weekly 15-minute pre-shift tastings (3–4 wines each; focused on new additions and BTG wines); monthly extended training sessions (producer-led or regional focus); staff wine lists with tasting notes; blind tasting games during slow service periods.
Service training: Every FOH team member should be able to: present a wine list, take a wine order, open and serve a still wine, open and serve sparkling wine, and upsell within the guest's apparent budget range.

SUGGESTIVE SELLING
The sommelier's most valuable skill in the commercial context: making appropriate recommendations that enhance the guest experience while increasing check average. Rule of engagement: recommend within the guest's stated or apparent budget range, but offer one elevated option at 20–30% above their apparent ceiling with a brief, specific reason: 'If you're open to it, there's a Premier Cru Chablis that would be beautiful with the scallops — it's $85 rather than $65, but the extra mineral depth really complements the beurre blanc sauce.' Specific reasoning outperforms generic upsell language.
Never pressure. Never shame. Never make a guest feel their first choice was wrong. Sommelier service that creates anxiety instead of pleasure drives guests away from wine.

VENDOR RELATIONS
Establish relationships with 3–5 primary distributors and 2–3 direct import or winery-direct suppliers. Primary distributors provide: delivery reliability, credit terms, inventory support, and representative access to new releases. Direct relationships provide: access to allocations (wine too small in production for distributor representation), producer dinners, better margins, and exclusivity on key wines.
Allocation management: The most prestigious wines (Burgundy Grand Crus, premium California Cult wines, allocated Italian reds) are available only by allocation — quantities assigned by the producer or importer based on purchase history and relationship. Maintaining purchasing relationships (buying consistently, paying promptly, representing the producer well) is how allocation access is preserved.

WINE PROGRAMME DEVELOPMENT
The wine programme should express the restaurant's concept. A farm-to-table restaurant with local ingredients should have a meaningful local and regional wine section. A modern Japanese omakase should have an excellent sake programme. A French bistro should have affordable, authentic French producers. The programme is an extension of the chef's culinary identity, not a separate commercial entity.
Price point strategy: The 'anchor and aspiration' model. Anchor = affordable entry-level wines that welcome budget-conscious guests without shame. Aspiration = prestigious bottles that give high-value guests something to celebrate. The profitable middle is the 'sweet spot' — well-chosen, correctly priced wines at 2–2.5× markup that serve the majority of the dining room and generate consistent revenue.
BTG rotation: Rotating 2–4 BTG wines per month keeps the list fresh, provides staff training opportunities, and reduces dead stock. Announce seasonal BTG changes as a service feature: 'We've just added a beautiful Vermentino from Sardinia as our summer white by the glass.'""",

"common_mistakes": """1. Pricing all wines at a flat multiple of cost — the flat markup approach (e.g., always 3× cost regardless of price) overprices premium wines and underprices entry-level wines, creating both a price-barrier at the high end and margin erosion at the low end.
2. Not rotating BTG wines before oxidation — a BTG wine open for 4+ days without preservation is likely deteriorating. Serving oxidised BTG wine destroys guest trust faster than almost any other service failure.
3. Listing too many wines and knowing too few — a list of 600 wines that the sommelier cannot confidently describe is a liability. A tightly edited list of 150 wines the team knows intimately serves guests better.
4. Treating vendor relationships as purely transactional — allocation access to the most prestigious wines is relationship-based. Wineries and importers provide allocations to restaurants that represent them well, pay on time, and place those wines appropriately. Purely transactional relationships lose allocation access.
5. Not tracking dead stock — wine that sits for 90+ days without moving is capital locked in inventory. Regular dead stock review and proactive management (recommendation, promotion, price adjustment) is a basic inventory discipline that many programmes neglect.
6. Confusing gross profit with profitability — a high-margin wine with low volume generates less gross profit than a mid-margin wine with high velocity. Optimise for a balance of margin and velocity, not margin alone.
7. Failing to train FOH staff to the minimum service standard — servers who cannot describe a wine or make a basic pairing recommendation actively damage BTG sales. Every FOH team member is a beverage salesperson; equipping them is a manager's responsibility.
8. Building a wine list without considering cellaring requirements — fine wine lists must account for the peak drinking windows of aged wines. Listing a 2019 Barolo on a list being compiled in 2026 requires knowing it will need 5–8 more years of bottle age; if you offer it, guide the guest to its current state and appropriate food pairing.""",

"pro_tips": """1. The 'anchor and aspiration' wine list design principle is directly analogous to restaurant menu engineering — the anchor wines generate traffic and accessibility; the aspiration wines generate revenue per seat; the profitable middle wines generate consistent margin. Map your list against this framework.
2. Pour cost targets for premium wine programmes can be misleading — a high-end restaurant where most guests are drinking $200+ bottles may have a nominal pour cost of 40%+ but extremely high gross profit per seat. Focus on gross profit per seat-turn, not pour cost percentage in isolation.
3. For allocation access to the world's most prestigious wines: the foundational relationship investment is purchasing your allocated quantity consistently, paying invoices within terms (30 days), and placing the wine correctly — on a list where it will be sold at an appropriate price, in the right dining context. Importers talk to each other. Your reputation as a buyer follows you.
4. Coravin has transformed the BTG programme economics for fine wine — the ability to serve a glass of 2009 Domaine Leroy Chambolle-Musigny (retail $1500+) by the glass at $350 per glass is commercially viable only with Coravin preservation. Know the system, its limitations (it does not work with sparkling wine), and its service protocol.
5. Wine list software (Bevager, MarketMan, BlueCart, BinWise) automates many inventory and ordering functions. At the MS level, you should understand how to manage a programme with or without software — the principles (par levels, FIFO, dead stock analysis) apply regardless of tool.
6. Staff tastings are not a cost — they are the highest-ROI training investment. A server who can authentically describe a wine ('this Grüner Veltliner has this beautiful white pepper nose — it's so clean, I think it works with the asparagus starter') will sell more of it than any printed tasting note. Taste your team regularly and make it engaging.
7. Understand the difference between a négociant-level wine (purchased as finished wine or bulk wine from multiple producers, blended under the négociant's label) and a domaine/estate wine (grown, produced, and bottled on-site). Négociant wines (Jadot, Drouhin) offer consistency and reliable supply; estate wines offer terroir expression and often better cellar age potential. Both belong on a well-curated list.
8. For the MS theory exam: know the standard food and beverage cost targets for fine dining (food cost 28–32%; beverage cost 25–33% for full programme; wine-specific 28–35% for BTG). These industry benchmarks are testable and contextualise financial management questions.""",
"trigger_keywords": json.dumps(["wine list design", "pour cost", "beverage business", "sommelier business", "inventory management", "BTG programme", "markup structure", "MS exam business", "wine programme", "vendor relations"])
},

{
"name": "MS Theory — Food and Wine Pairing",
"slug": "ms-theory-food-and-wine-pairing",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers / Escoffier Foundation",
"description": """Food and wine pairing is both the most creative and the most technically grounded discipline in the sommelier's professional toolkit. At the Master Sommelier level, pairing is not a matter of rules or traditions ('white wine with fish') but an understanding of the chemical and structural interactions between food components and wine components. The MS examiner expects candidates to explain WHY a pairing works — which specific elements of the food are engaged by which specific elements of the wine — not simply state that a pairing is traditional.

The five pairing types established by professional sommelier education (complement, contrast, bridge, cleanse, elevate) provide a logical framework for generating and evaluating pairings. Equally important is understanding WHY certain classic pairings succeed (Chablis with oysters — shared saline mineral; Sancerre with goat cheese — shared Loire terroir and acidity; Sauternes with foie gras — sweetness matching fat richness) and WHY certain food components create specific wine difficulties (artichoke, asparagus, chocolate, chilli heat, egg yolk).""",

"key_principles": """FIVE PAIRING TYPES

1. COMPLEMENT (similar meets similar)
The wine shares a flavour compound or structural characteristic with the food, creating harmony through similarity. Examples:
  Oaky Chardonnay + creamy butter sauce: both have a buttery, round, vanilla-like character from diacetyl (wine) and actual butterfat (sauce). The shared texture and flavour reinforces both.
  Aged Rioja + roasted lamb: the cedar/leather/dried fruit of aged Tempranillo mirrors the savoury, slow-roasted character of the lamb. Both have secondary (aged) complexity.
  Sauternes + foie gras: iconic complementary pairing. Fat and sweetness mirror each other; the wine's high acidity prevents both from becoming cloying; the shared richness elevates both.

2. CONTRAST (opposite meets opposite)
The wine's structural characteristic provides a counterpoint that refreshes or balances a dominant food element. Examples:
  High-acid Riesling (off-dry) + spicy Thai cuisine: the wine's sweetness counterbalances heat; the acidity refreshes the palate. Alcohol-forward wines amplify chilli heat; this is why low-ABV, off-dry Riesling is the ideal pairing for spicy food.
  Champagne Brut + deep-fried food: the acidity and carbonation of Champagne cuts through fat and refreshes after each bite. Bubbles mechanically remove fat molecules from the palate.
  Crisp Muscadet (bone dry, high acid) + fatty, oily fresh oysters: acid cuts through the brine and fat; cleanses for the next oyster. Shared coastal mineral adds a complement layer.

3. BRIDGE (shared aromatic compound links food and wine)
A specific compound appears in both the food and the wine, creating a flavour bridge. Examples:
  Sauvignon Blanc (pyrazines) + asparagus or bell pepper (pyrazines): both contain methoxypyrazines (green, vegetal, capsicum character). The shared compound intensifies the connection.
  Grüner Veltliner + white asparagus: Grüner's white pepper character (rotundone) and herbal edge bridging with the vegetal, slightly bitter asparagus.
  Pinot Noir + salmon (Pacific Salmon, seared): the earthy, red berry character of Oregon or Burgundy Pinot bridges with the richness and slightly savoury umami of seared salmon. The fat in salmon handles the modest Pinot tannin.
  Sancerre/Pouilly-Fumé + fresh goat's cheese (chèvre): both from the Loire; both carry a distinct chalk/mineral/herbal quality; the bridge is geological and chemical simultaneously. Loire goat cheese + Loire Sauvignon Blanc is one of the most reliably successful regional pairings.

4. CLEANSE (the wine resets the palate between bites)
The wine removes fat, protein coating, or lingering spice from the palate, resetting for the next bite. Examples:
  High-acid sparkling wine + any fatty or creamy dish: bubbles + acid = mechanical and chemical cleanse.
  Tannic red wine + aged fatty cheese (Comté, aged Cheddar): tannin binds to the fat and protein in the cheese, literally removing them from the palate coating. The cheese also softens the perception of tannin — a mutual cleanse.
  Dry Sherry (Fino or Manzanilla) + jamon ibérico: acidity and sherry's oxidative character cleanse the rich fat and salt of cured ham; the almond nuttiness of the sherry bridges with the ham's savoury depth.

5. ELEVATE (the pairing exceeds the sum of its parts — wine enhances dish; dish enhances wine)
The most sophisticated pairing outcome. The dish reveals aspects of the wine not apparent without the food, and the wine elevates the dish beyond what it achieves alone. Examples:
  Aged Burgundy + wild mushroom risotto: the earthy, forest floor, truffle notes in aged Pinot Noir are amplified by the mushroom's umami; the risotto's cream and parmesan soften the Pinot's structure; the wine's complexity and the dish's depth create a result neither achieves separately.
  Premier Cru Chablis + oysters: the wine's saline chalk mineral character mirrors the oyster's brine; the wine's acidity illuminates the oyster's sweetness; the oyster's fat and mineral softens the wine's edge. This is a world-class elevating pairing.
  Sauternes + Roquefort cheese: sweetness in the wine, saltiness in the cheese, and shared stonefruit/honey compounds in both. One of the world's great elevating pairings.

STRUCTURAL PAIRING PRINCIPLES

Weight with weight: A delicate wine with a heavy dish loses; a robust wine with a delicate dish overwhelms. Always match body and intensity. A 15% Barossa Shiraz overwhelms sushi; a 12% Muscadet is overwhelmed by a beef braised in Bordeaux. Weight matching is the foundational rule.

Acidity: High-acid wines pair with high-acid foods (tomato-based pasta with Sangiovese — both have natural acidity; neither seems sharp against the other). High-acid wine with non-acidic rich food provides contrast (Champagne with cream sauce). Low-acid wine with high-acid food (oaky New World Chardonnay with a lemon vinaigrette) results in the food making the wine taste flat and flabby.

Tannin: Tannin binds to protein and fat, which explains the classic red wine + steak pairing: the tannin in a young Cabernet binds to the muscle protein and fat in the steak, softening the tannin while the fat/protein coating on the palate from the meat is removed. Tannin + low-fat/low-protein food (delicate fish, salad greens) = harsh, astringent: no fat/protein to buffer the tannin.

Sweetness: The food should be no sweeter than the wine. A bone-dry Riesling with a sweet dessert (crème brûlée) will taste sharply acidic and bitter because the dessert's sweetness makes the wine seem austere. A Sauternes with the same dessert works because the wine matches or exceeds the dessert's sweetness. The rule: wine must always be as sweet as or sweeter than the food it accompanies.

Alcohol: Chilli heat + high-alcohol wine = amplified burning sensation. The fat-soluble capsaicin in chilli is amplified by alcohol. Low-ABV, off-dry wines (Mosel Riesling, Gewurztraminer) are the correct structural response to spicy food. This is chemistry, not preference.

Umami: High-umami food (soy, fish sauce, aged cheese, mushrooms, anchovies, miso) amplifies the perception of tannin and bitterness in wine. Tannic red wine + high-umami food = harsh, metallic, bitter. Correct response: low-tannin or no-tannin wines (Pinot Noir, Beaujolais, Grenache; or dry whites; or sake — whose own umami harmonises rather than clashes).

DIFFICULT PAIRINGS — WHY THEY'RE HARD

Artichoke (Cynara scolymus): Contains cynarin — a chemical compound that inhibits sweet taste receptors on the tongue, causing any liquid consumed after eating artichoke to seem artificially sweet. Any wine served with artichoke will taste unexpectedly sweet and often cheap. The only partial solution: high-acid, dry white wine (Sauvignon Blanc, Verdicchio, Grüner Veltliner) where the sweetness effect is less disorienting.

Asparagus: High in sulfur compounds (methyl mercaptan and dimethyl sulfide) that react poorly with wine to create a rubbery or metallic note. Additionally contains pyrazines (green/vegetal) that clash with tannic red wines. Correct pairing: Grüner Veltliner (bridges the vegetal character) or Sauvignon Blanc (complements the pyrazine character) — both dry, aromatic, high-acid.

Chocolate (dark): Bitterness compounds in chocolate clash with tannins in red wine, creating a harsh double-bitterness. Dark chocolate + tannic red wine = aggressive bitterness. Correct approach: sweet red wine (Banyuls — the French fortified Grenache from Roussillon — is the traditional classic pairing for chocolate; LBV Port; Italian Brachetto d'Acqui for milk chocolate).

Egg yolk: The sulphur compounds in egg yolk (particularly fried or soft-boiled) react with tannins to produce a metallic note. Egg yolk + tannic red wine = unpleasant metallicity. Correct pairing: Champagne (the classic brunch pairing for eggs Benedict — Champagne's acidity and carbonation cut through the yolk's richness without a tannin reaction), dry Sherry, or Chablis.

Spicy food: See alcohol point above. The general pairing principle: off-dry, low-ABV wines (German Riesling Spätlese or Kabinett, off-dry Gewurztraminer, Chenin Blanc demi-sec) provide cooling relief; beer (lager, wheat beer) also works via carbonation + low ABV; high-alcohol wine amplifies the burn.

CLASSICAL PAIRINGS AND THE SCIENCE BEHIND THEM
Chablis + oysters: Shared Kimmeridgian limestone; oyster's saline mineral echoed in Chablis's saline mineral; Chablis's high acidity cuts through oyster's natural fat and protein; the wine's low residual sugar keeps the brine-mineral impression clean.
Sancerre + goat cheese (chèvre): Same Loire chalk terroir; Sauvignon Blanc's herbal, citrus, mineral character mirrors the grassy, lemony, chalk character of fresh chèvre; the wine's acidity counterbalances the cheese's creaminess.
Burgundy Pinot Noir + roasted chicken or duck: Classic weight match; Pinot Noir's red fruit, modest tannin, and earthy depth matches poultry's protein weight and savoury quality without overpower; the wine's acid complements the rendered fat.
Champagne + fried food (fried chicken, tempura): Carbonation + high acidity = mechanical cleanse; bubbles break fat films on the palate; the wine's yeasty, biscuity character bridges with the fried crust; the contrasting freshness of Champagne is the perfect foil for fat and salt.
Sauternes + foie gras: The paradigmatic luxury pairing; sweetness meeting richness; Sauternes's botrytis complexity (apricot, honey, ginger) mirrors the liver's unctuous, slightly gamey richness; the wine's exceptional acidity prevents the pairing from becoming too sweet or heavy.

REGIONAL PAIRING LOGIC (What Grows Together Goes Together)
The traditional culinary pairings of any wine region evolved over centuries in response to the actual food grown or produced in that region. Sangiovese developed alongside Tuscan olive oil cooking; Albariño developed alongside Galician seafood; Barolo developed alongside white truffle and Piedmontese beef. These regional pairings are not accidental — they reflect centuries of co-evolution. The Master Sommelier should use regional pairing as the first reference point, then adjust for specific dish and wine variables.""",

"common_mistakes": """1. Applying weight without considering structure — matching body is necessary but not sufficient. A full-bodied oaked Chardonnay is the same weight as a full-bodied aged white Burgundy, but the oak structure of one may overwhelm a delicate dish that the aged Burgundy would elevate.
2. Serving tannic red wine with egg or high-umami dishes — the tannin-sulphur and tannin-glutamate reactions create metallic and harsh notes. Candidates who know the classic red wine with steak pairing but not its underlying chemistry will misapply it to inappropriate dishes.
3. Not knowing the artichoke problem — a candidate who recommends any wine for an artichoke course without addressing cynarin is demonstrating incomplete pairing knowledge. The answer is: this is one of the most difficult pairings; dry, high-acid white is the best mitigation.
4. Recommending high-alcohol wine with spicy food — the incorrect recommendation ('this Barossa Shiraz will stand up to the heat') actively worsens the dining experience. Alcohol amplifies capsaicin burn. This is chemistry.
5. Treating 'regional pairing' as an infallible rule — 'drink what grows together' is a useful starting point, not a rule. The specific dish and wine must be assessed on their structural merits; regional heritage is a first hypothesis, not a final answer.
6. Not knowing the Sauternes + Roquefort pairing — this is one of the world's great pairings and is reliably testable at MS level. The sweetness of Sauternes balancing the salt of Roquefort; the botrytis honey and the blue mould complexity harmonising. Know it and know why it works.
7. Confusing complement and bridge pairings — complement = shared structural characteristic (weight, texture, richness); bridge = shared specific compound (aromatic, flavour). An oaky Chardonnay with a butter sauce is a complement (shared richness and butter compounds). A Sauvignon Blanc with asparagus is a bridge (shared pyrazines). The distinction matters for exam precision.
8. Not addressing the sweetness rule — wine must always be at least as sweet as the food. A candidate who recommends a dry wine with a sweet dessert is making a fundamental structural error regardless of other pairing logic they apply correctly.""",

"pro_tips": """1. The most reliable universal pairing principle: match intensity. A dish with 3 intense flavour components (umami-rich braised meat, truffle, aged cheese sauce) needs a wine of equal intensity (aged Burgundy, Barolo, Hermitage). Mismatch intensity before you mismatch anything else and the pairing will always fail.
2. Build a personal 'pairing matrix' — rows are food components (fatty, acidic, sweet, spicy, bitter, umami), columns are wine structural elements (high acid, tannic, sweet, low-tannin, high-alcohol, sparkling). Fill in the interactions: fat + tannin = works; umami + tannin = problematic; sweet food + sweet wine = works if wine is sweeter. Reference this matrix when building pairings under pressure.
3. For the MS theory exam, cite the chemistry when it matters: 'Cynarin in artichoke inhibits sweetness receptors — any wine will be altered. High-acid dry white minimises the distortion.' This level of mechanistic explanation distinguishes a Master-level answer from an Advanced-level answer.
4. Know the Banyuls pairing for chocolate cold — it is the only reliable answer for dark chocolate pairing in traditional French cuisine. Banyuls is a French VDN (Vin Doux Naturel — fortified wine from Grenache, from Roussillon) with a dried fruit, chocolate, coffee character that meets dark chocolate as an equal.
5. Study the Japanese food + sake pairing rules: umami + umami = synergy (unlike tannin + umami = conflict). This is why sake pairs with almost all Japanese cuisine — the glutamates in sake harmonise with the glutamates in dashi, miso, and soy, while wine tannins would conflict with those same compounds.
6. The 'difficult pairing' questions at MS theory level include: artichoke, asparagus, chocolate, eggs, anchovies, and kimchi/fermented Korean dishes. Know each one's specific chemistry and the wine response. These are reliable exam topics because they test understanding beyond pattern-matching.
7. When in doubt at the MS exam: if you cannot identify the ideal pairing, identify the structural requirements and eliminate what cannot work. 'This dish is high in fat and umami. That means low tannin, high acidity is required. Red wines with high tannin are excluded. I'd recommend Pinot Noir, Gamay, or a high-acid white — Chablis or Riesling.' Structural elimination is a valid exam methodology.
8. The Champagne + fried chicken pairing (popularised by Thomas Keller at The French Laundry and now celebrated in New Orleans cuisine) is both a reliable pairing principle and a culturally significant food moment — it demonstrates that 'prestige' pairings are not limited to classical European fine dining combinations. The MS exam increasingly reflects the diversity of global cuisine, and great pairings can come from any culinary tradition.""",
"trigger_keywords": json.dumps(["food wine pairing", "pairing principles", "complement contrast bridge", "tannin fat pairing", "artichoke wine", "spicy food wine", "MS exam pairing", "umami wine", "Sauternes foie gras", "regional pairing"])
},

]

def main():
    conn = psycopg2.connect(CONN)
    cur = conn.cursor()
    inserted = 0
    errors = 0
    for e in ENTRIES:
        try:
            cur.execute(SQL, (
                e["name"], e["slug"], e["category"], e["tier_level"],
                e["authority_tier"], e["source_book"],
                e["description"], e["key_principles"],
                e["common_mistakes"], e["pro_tips"],
                e["trigger_keywords"]
            ))
            inserted += 1
        except Exception as ex:
            print(f"ERROR on {e['slug']}: {ex}")
            conn.rollback()
            errors += 1
            continue
        conn.commit()
    cur.close()
    conn.close()
    print(f"Done. {inserted} inserted, {errors} errors.")

if __name__ == "__main__":
    main()
