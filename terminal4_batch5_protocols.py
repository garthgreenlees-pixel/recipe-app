#!/usr/bin/env python3
"""Terminal 4 — Batch 5: service_protocols — ceremonies and beverage service rituals"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """INSERT INTO service_protocols
  (name, category, beverage_family, description, procedure, rationale,
   common_errors, service_context, equipment_required, guest_communication,
   authority_tier, source_text, skill_level, is_published)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING RETURNING id, name"""

PROTOCOLS = [

# ============================================================
# ETHIOPIAN BUNA CEREMONY — THE ORIGIN OF COFFEE CULTURE
# ============================================================
{
  "name": "Ethiopian Buna Ceremony — The Origin of All Coffee Culture",
  "category": "coffee_service",
  "beverage_family": "coffee",
  "description": """The Ethiopian coffee ceremony (buna — pronounced 'boo-nah') is the oldest continuous coffee service ritual on Earth and the cultural template from which all coffee culture descends. Duration: 1-2 hours for a full ceremony. Three rounds: abol (first, strongest), tona (second, thinner), baraka (third — the blessing). The host roasts green beans on a flat iron pan over charcoal, grinds in a wooden mortar (mukecha), brews in a clay pot (jebena), serves in small handleless cups (cini). Frankincense burns. Fresh grass strewn on the floor. This is not a beverage service — it is a ceremony of hospitality, community, and blessing.

THIS IS A CULTURAL PRESERVATION ENTRY. The buna ceremony should be treated with the same reverence as Japanese chanoyu. If incorporating elements of the buna ceremony into a restaurant coffee service programme, do so with explicit acknowledgement of its Ethiopian origin and cultural significance.""",
  "procedure": """THE FULL BUNA CEREMONY — SEVEN STAGES:

1. PREPARATION OF THE SPACE:
Green grass (mitmita) or flower petals strewn on the floor beneath the service area. Frankincense (itan) or myrrh burned on charcoal in a clay censer. The ceremony space is deliberately made fragrant and beautiful before the guest arrives. Purpose: the guest enters into a prepared, welcoming environment.

2. WASHING AND ROASTING THE GREEN BEANS:
The host washes raw green coffee beans in a flat pan over charcoal fire. The host performs this washing in front of the guests — the transparency of the raw material is part of the ceremony. The beans are then roasted on a flat iron pan (menkeshkesh) over a charcoal brazier (qorqema), stirred continuously with a stick. Roasting time: 8-12 minutes. The host circulates the smoking pan of freshly roasted beans to each guest so they can smell the aroma and say 'Bun!' (appreciation). This moment is the ceremony's first communion — the shared sensory experience of fresh roast aroma.

3. GRINDING:
The roasted beans are poured into a wooden mortar (mukecha) and ground with a wooden pestle (zenezena). The rhythm of the grinding has a distinctive sound — in Ethiopia, you can hear when a buna ceremony is underway from outside the house. The grinding is done by the host personally — it cannot be delegated without diminishing the ceremony.

4. BREWING IN THE JEBENA:
The ground coffee is added to cold water in the jebena (clay pot, typically round-bottomed with a woven grass stopper/lid). The jebena is placed over the charcoal brazier and brought to a boil. The first boil produces the strongest coffee. The jebena is removed from heat, allowed to settle briefly, then placed back to heat until the brew reaches serving temperature.

5. POURING — THE THREE ROUNDS:
The host pours from a height of 20-30cm into small handleless cups (cini or si'ni) placed on a ceremonial tray. Pouring from height aerates the coffee and creates a slight froth. The pour is continuous — never stopping mid-pour.
ABOL (First pour): The strongest, most concentrated round. Served with sugar (sukkar) — sometimes salt in some regions of Ethiopia; sometimes butter in some cultures. This is the round that carries the weight of the ceremony.
TONA (Second pour): Water is added to the jebena and rebrewed. Slightly weaker than Abol. The conversation has deepened by this point.
BARAKA (Third pour, 'the blessing'): Thinnest round but considered the most auspicious. In Amhara culture, refusing Baraka is considered disrespectful — to leave before the third round is to leave before the blessing.

6. ACCOMPANIMENTS:
Kolo (roasted barley or other grain) or popcorn (often popped corn) served in a shared bowl as a snack during the ceremony. In some regions: injera (sponge bread), date-filled pastries, or local sweets. The food is simple — the ceremony is about the coffee and the conversation, not elaborate eating.

7. THE CULTURAL CONTRACT:
The buna ceremony is an act of trust and welcome. Being invited to a buna ceremony is an honour. Accepting the invitation is agreeing to the pace — you cannot rush. The ceremony says: your time is worth this. The host says: you matter enough for me to spend two hours preparing coffee for you. This is the deepest hospitality code in Ethiopian culture.

ADAPTATION FOR RESTAURANT CONTEXT:
If offering a buna experience in a professional setting:
— Use freshly roasted Ethiopian heirloom beans (Yirgacheffe or Harrar)
— Roast tableside on a small flat pan if possible (or pre-roast and present the aroma)
— Use a jebena or clay vessel for brewing
— Serve in cini cups (available from Ethiopian specialty stores in Vancouver)
— Burn frankincense resin on a small charcoal disc alongside
— Offer the three rounds — even condensed into 20-30 minutes, the structure of abol/tona/baraka carries the ceremony's meaning
— Name the origin, the ceremony, and its meaning explicitly to guests""",
  "rationale": """The buna ceremony is the origin of all coffee culture. Every coffee service tradition — the Viennese coffeehouse, the Italian espresso bar, the Japanese café aesthetic — descends from this Ethiopian source. Acknowledging this origin in a professional coffee service context is both historically accurate and culturally respectful. The ceremony teaches the deepest truth about coffee: it is a medium of hospitality, not a commodity. The ceremony cannot be hurried, cannot be outsourced, cannot be made more efficient without ceasing to be the ceremony. In a world of instant coffee, the buna is a protest against urgency.""",
  "common_errors": """Rushing any phase of the ceremony — particularly the roasting (which must be done in full view of guests) and the pouring (which must be performed with deliberate ceremony, not efficiency). Using pre-ground coffee (the grinding in the mukecha is a ceremonial act, not a production step). Skipping the frankincense (the olfactory environment is as important as the coffee itself). Serving in modern coffee cups — the cini cups (small, handleless, handleless — note: 'handleless' is the mark of the tradition) are the correct vessel. Treating the buna as a 'coffee tasting' rather than a ceremony of welcome.""",
  "service_context": "fine_dining",
  "equipment_required": ["Flat iron pan (menkeshkesh) or heavy skillet", "Clay jebena with woven grass stopper", "Wooden mortar (mukecha) and pestle (zenezena)", "Small cini cups (handleless)", "Ceremonial tray", "Charcoal brazier or equivalent heat source", "Frankincense resin and small charcoal disc", "Green Ethiopian heirloom coffee beans (Yirgacheffe or Harrar)", "Small bowls for kolo or popcorn", "Sugar"],
  "guest_communication": """Introduction before beginning: 'We're going to perform the Ethiopian buna ceremony for you this evening — the oldest coffee service tradition on Earth, and the cultural origin of all coffee culture. It takes about 20-30 minutes and involves three rounds of coffee, each slightly different in strength. The first, abol, is the strongest. The second, tona, is softer. The third, baraka, means blessing — it's considered auspicious in Ethiopian tradition to complete all three rounds. We have Ethiopian frankincense burning alongside. Please let the aroma settle around you.'

After the roasting presentation: 'These are raw Ethiopian heirloom beans — you can see how green they are before roasting. The coffee you know comes from here. These same varieties grow wild in the Kaffa forest in southern Ethiopia — the forest where coffee originated.'

Before the third round: 'This is baraka — the blessing. In Ethiopia, completing the third round means you take something good with you when you leave.'""",
  "authority_tier": 1,
  "source_text": "Tadesse Meskela — OCFCU documentation; Abebe, H. — Ethiopian Coffee Ceremony (Addis Ababa University Press, 2003); personal accounts from Ethiopian community sources",
  "skill_level": "advanced"
},

# ============================================================
# KAVA CEREMONY — PACIFIC NAKAMAL SERVICE
# ============================================================
{
  "name": "Nakamal Kava Service — Pacific Ceremonial Presentation Protocol",
  "category": "general_tableside",
  "beverage_family": "traditional",
  "description": """The Pacific kava ceremony adapted for professional service contexts. Kava (Piper methysticum) is the primary ceremonial and social beverage of Oceania — a non-alcoholic, anxiolytic, muscle-relaxing beverage used continuously for 3,000+ years. The nakamal (Vanuatu kava bar) protocol is the most accessible ceremonial form for professional adaptation. The Fijian yaqona ceremony is the most formalised. THIS IS A CULTURAL PRESERVATION SERVICE — named traditions of specific Pacific cultures should be acknowledged explicitly when performing elements of their ceremony.""",
  "procedure": """NAKAMAL-STYLE SERVICE PROTOCOL (adapted for professional setting):

PRE-SERVICE PREPARATION:
Source: Noble variety kava only — Vanuatu Borogu or Melomelo, Fijian Waka grade, or verified Noble variety. NEVER Tudei (two-day) variety. Verify with supplier.
Preparation (best done 30-60 minutes before service): 60-80g course-ground dried root per litre of cold water. Kneading method:
  1. Combine kava and water in a large bowl
  2. Knead and squeeze through a muslin cloth or kava cloth for 8-10 minutes
  3. Strain through clean cloth, squeezing out all liquid
  4. Second strain through fresh cloth for clarity
  5. Final product should be opaque, grey-tan, slightly thick
Temperature: Room temperature (never refrigerate below 4°C — affects kavalactones) — serve within 2-3 hours of preparation

AT-TABLE PRESENTATION:
1. ARRIVAL: Bring the prepared kava in a covered vessel (clay bowl, carved wooden tanoa, or simple earthenware — NO glass, no plastic for service presentation). Bring coconut shell cups (bilo) or equivalent small vessels.
2. GREETING: 'We have prepared kava for you tonight from [origin — Vanuatu Borogu, Fijian Waka, etc.]. Kava has been the ceremonial beverage of the Pacific for 3,000 years — it's non-alcoholic, but you'll notice specific effects: a pleasant relaxation, some numbness in the mouth and lips. Please tell us if you'd like to know more.'
3. POURING: Fill the bilo (coconut shell) approximately 2/3 full. Do NOT overfill — the shell should be manageable to drink in one go.
4. PRESENTATION: Both hands when offering the shell — this is the universal Pacific gesture of respect.
5. RECEIVING INSTRUCTION: 'In the Fijian tradition, you clap once before receiving, drink the whole shell in one go, then clap three times. You can choose to do that, or simply drink in a way that's comfortable for you.'
6. FIRST SIPS: Some guests will immediately notice the oral numbness (a sign of kavalactone quality). Note: 'That numbness you're feeling — that's the kavalactones. It's a quality indicator.'
7. BETWEEN SHELLS: Conversation. Kava slows time. Do not rush to offer a second shell.
8. SECOND SHELL (optional): Offer after 10-15 minutes. The effects build — some guests will be satisfied with one.

FIJIAN YAQONA FORMAL PROTOCOL (if context warrants):
The clapping sequence is called cobo:
— One sharp clap (right palm into cupped left hand) BEFORE receiving the bilo
— Bow the head slightly while drinking (full cup, one go)
— Three leisurely claps AFTER
This sequence is an act of gratitude and respect — it should be taught to guests who choose to engage with it, not forced.

EFFECTS TIMELINE (communicate to guests):
0-15 minutes: Oral and facial numbness beginning
15-30 minutes: Muscle relaxation, slight cognitive calm-clarity
30-60 minutes: Peak effects — guests may prefer quieter conversation, less stimulation
Note: Kava is NOT intoxicating in the alcohol sense — there is no impairment of judgment or coordination at normal serving sizes (1-2 shells). The effect is specifically anxiolytic and muscle-relaxing.""",
  "rationale": """Kava is the Pacific Migration Trail's primary beverage — the cultural equivalent of sake for Japan, tea for China, or coffee for Ethiopia. To offer kava service without cultural context strips it of its meaning and reduces one of humanity's most significant ceremonial beverages to a novelty. The professional kava service protocol acknowledges the tradition, explains the pharmacology, and creates a genuinely educational experience for guests. It also positions the beverage programme as internationally literate — a programme that understands beverages as cultural objects, not commodities.""",
  "common_errors": """Serving kava hot — heat above 60°C destroys the primary kavalactones; the drink becomes ineffective and bitter. Using Tudei ('two-day') kava varieties — these produce nausea and 24-48 hour hangover effects from dihydromethysticin content; confirmed Noble variety sourcing is mandatory. Offering kava without contextual explanation — guests unfamiliar with the tradition need to understand what they are about to experience. Presenting in wine glasses or cocktail glasses — the coconut shell (or a small earthenware cup) is the correct vessel; the vessel is part of the meaning. Rushing multiple shells — kava is not a shot. Each shell should be served at a minimum 10-minute interval.""",
  "service_context": "ceremonial",
  "equipment_required": ["Coconut shell cups (bilo) or small earthenware bowls", "Carved wooden tanoa (mixing bowl) or large earthenware vessel", "Muslin cloth for straining (minimum 30cm x 30cm, clean)", "Noble variety kava (verified — Vanuatu Borogu or Fijian Waka preferred)", "Cold water for preparation (60-80g kava per litre)", "Covered transport vessel for table service", "Handwashing facilities (kava hands smell distinctly — wash before continuing other service)"],
  "guest_communication": """Opening statement: 'We're offering the Pacific kava ceremony this evening — the ceremonial beverage of Vanuatu, Fiji, Samoa, and Hawaii, used in these cultures for over 3,000 years. Kava is non-alcoholic but pharmacologically active — you'll feel a pleasant relaxation and some numbness in the mouth and lips from the kavalactones. These are the active compounds. This is Noble variety kava from [origin], which means clean effects and no adverse feelings the next day. Shall I explain the Fijian serving tradition?'

For the first-time guest who is uncertain: 'The numbness feeling is the quality indicator — the stronger the numbness, the more active the kava. It's completely safe at these serving sizes and the effects last 2-4 hours, less than a glass of wine in terms of duration.'

After completing the ceremony: 'The kava should make this the most relaxed part of your evening. If you'd like another shell in 15-20 minutes, we're happy to bring one. There's no rush.'""",
  "authority_tier": 1,
  "source_text": "Lebot, V., Merlin, M. & Lindstrom, L. — Kava: The Pacific Elixir (Yale, 1992); Bula Kava House service documentation; Vanuatu Cultural Centre protocols",
  "skill_level": "advanced"
},

# ============================================================
# ARGENTINE MATE CEREMONY
# ============================================================
{
  "name": "Argentine Mate — The Circular Sharing Ceremony",
  "category": "general_tableside",
  "beverage_family": "traditional",
  "description": """Yerba mate (Ilex paraguariensis) is the social beverage of the Southern Cone — Argentina, Uruguay, Paraguay, and southern Brazil. The mate ceremony is built on circular sharing: one designated server (cebador/a) prepares and passes the same gourd to all participants in sequence. The act of sharing a single vessel is the ceremony. It says: we are equal, we are together, our lips touch the same metal straw. This is Southern Cone hospitality distilled into a single object.""",
  "procedure": """THE COMPLETE MATE SERVICE:

EQUIPMENT:
Mate (calabaza gourd) — can be pumpkin gourd (most traditional), bull horn, wooden bowl, or ceramic. The gourd is cured (broken in with first uses) and develops a residue that contributes flavour.
Bombilla — metal straw with filter at lower end (spring or disc filter). Silver is traditional in Argentina; stainless is the common modern material.
Thermos of water — CRITICAL: 70-80°C. NEVER boiling water. Boiling (100°C) burns the yerba, producing bitter, harsh flavours and potentially releasing more caffeine than intended.
Yerba mate (dried, cured, or green) — Taragüi (Argentina), Cruz de Malta (Argentina), Rosamonte (Argentina), Canarias (Uruguay)
Small bowl of sugar (optional — mate amargo = bitter; mate dulce = sweet)

PREPARATION — THE CORRECT SEQUENCE:
1. Fill the gourd 2/3 with yerba mate. Tilt the gourd to consolidate the yerba to one side (creating a 'mountain' of yerba on one side, clear space on the other).
2. Insert the bombilla into the clear space at the bottom, leaning against the side of the gourd. DO NOT stir — the bombilla must not be moved after insertion.
3. Pour a small amount of cold water into the clear space near the bombilla first. This protects the herbs from the hot water and prevents scalding. Wait 30 seconds.
4. Pour 70-80°C water slowly into the clear space (not onto the herb 'mountain'). Fill until the water just reaches the top of the herb pile but does not fully saturate it.
5. The cebador (server) drinks the first mate — this is not honour, it is quality control. The first mate absorbs any dust or off-flavours from preparation. The cebador does not say 'thank you' after this first mate — it is not a gift, it is a test.
6. Refill and pass to the next guest, always filling to the same level before passing.

THE CIRCULAR SEQUENCE:
The gourd is passed clockwise (or counter-clockwise — varies by region, but consistent within each session). Each guest receives the gourd, drinks the full water content through the bombilla (until the sucking sound indicates empty), hands the gourd back to the cebador who refills and passes to the next person.
NEVER add more yerba in the middle of a session — the ratio is set at the beginning.
The cebador manages the water temperature — if the thermos has cooled, the last mates in the session are often less good. A skilled cebador compensates by adjusting the fill rate.

SOCIAL CODES:
'Gracias' (thank you) at any point during the session means 'I am done, I don't want another.' If you say gracias after receiving the gourd, the cebador will not offer you another round.
DO NOT say gracias unless you mean to stop — a guest who says gracias to be polite and then accepts another gourd confuses the social contract.
If you want to continue: simply receive and drink, hand back, no words necessary.
The session ends when the yerba is 'lavado' (washed out) — the flavour becomes thin and watery. The cebador will say 'se lavó' and prepare a fresh gourd.

PROFESSIONAL ADAPTATION:
For table service, the mate ceremony can be offered as an arrival drink, a digestif pairing, or as part of a cultural tasting menu.
Offer both mate amargo (bitter — traditional) and mate dulce (sweet — for guests unfamiliar with bitterness).
The bombilla must be thoroughly cleaned between guest groups (hot water rinse, brush).
For large tables: provide multiple gourds or circulate through sections of the table.""",
  "rationale": """Mate is one of the most social beverages on Earth — it is literally designed to prevent individual consumption. The shared gourd, the shared bombilla, the strict circulation protocol — all exist to create community. Offering mate in a professional context communicates: we understand South American culture deeply enough to prepare this correctly. It also provides a non-alcoholic, stimulating experience (theobromine + caffeine) that occupies the aperitif or digestif role without alcohol.""",
  "common_errors": """Using boiling water (100°C) — burns the yerba and produces harsh, bitter, astringent mate. The water temperature is THE most important variable. Adding new yerba mid-session — disrupts the flavour equilibrium. Saying 'gracias' when not intending to stop (social protocol confusion). Moving the bombilla after insertion — this dislodges the filter position and allows yerba to enter the straw. Rushing the circulation — each guest should have sufficient time to drink fully before the gourd is returned.""",
  "service_context": "ceremonial",
  "equipment_required": ["Calabaza gourd (cured)", "Bombilla (metal straw with filter)", "Thermos with 70-80°C water (not boiling)", "Yerba mate (Taragüi, Cruz de Malta, or Rosamonte)", "Small bowl of sugar (optional)", "Bombilla cleaning brush"],
  "guest_communication": """Introduction: 'We're going to share mate with you this evening — the traditional tea ceremony of Argentina and Uruguay. Mate is a shared beverage — one gourd, one bombilla, passed around the table. This is not about hygiene — it's about trust. The flavour is earthy, grassy, slightly bitter. It contains caffeine and theobromine — similar to a strong tea but with a calmer, more sustained energy. The server — in Argentina they're called the cebador — will pass the gourd clockwise, refilling with hot water each time. If you'd like to stop, just say "gracias" when you return the gourd. If you want to continue, just hand it back without saying thanks. That's the social contract of mate.'

Temperature explanation: 'The water is 70 degrees — intentionally below boiling. Boiling water burns the yerba and makes it harsh. A good cebador watches the water temperature the way a sommelier watches wine temperature.'""",
  "authority_tier": 1,
  "source_text": "Giberti, G.C. — Ilex paraguariensis (INTA Argentina, 1995); Argentinian Ministry of Culture documentation on yerba mate as national cultural heritage",
  "skill_level": "intermediate"
},

# ============================================================
# CACAO CEREMONY
# ============================================================
{
  "name": "Ceremonial Cacao Service — Mesoamerican Heart-Opening Tradition",
  "category": "general_tableside",
  "beverage_family": "traditional",
  "description": """Ceremonial cacao (Theobroma cacao — 'food of the gods') is NOT hot chocolate. It is minimally processed, stone-ground cacao consumed as a thick, bitter, sometimes spiced beverage — as the Maya and Aztec cultures consumed it. The distinction is critical: commercial hot chocolate uses cocoa powder stripped of its fat (cocoa butter) and cacao mass, mixed with dairy and sugar to produce a confection. Ceremonial cacao is the whole cacao bean ground to a paste, mixed with hot water (not milk) and sometimes chili, vanilla, or mayan spices — a bitter, full-flavoured, ceremonially charged beverage. THIS IS A CULTURAL PRESERVATION ENTRY — the cacao ceremony belongs to the Mesoamerican civilisations that created it, and should be acknowledged as such.""",
  "procedure": """THE CEREMONIAL CACAO SERVICE:

SOURCING — THE CRITICAL FIRST STEP:
Ceremonial cacao is distinguished from commercial cacao by:
— Single origin: specific farm, specific region (Guatemala, Peru, Colombia — the Maya/Aztec heartland zones most significant)
— Minimal processing: no added lecithin, vegetable fat, sugar, or other additives
— Fermentation quality: whole beans properly fermented and dried before grinding
— Cacao content: 100% pure ground cacao paste — no mixing agents
Verified ceremonial sources: Keith's Cacao (Guatemalan Criollo variety — considered the best), Ora Cacao (Ecuador), Firefly (Colombian), Captain Ahab's (BC-based import)

PREPARATION:
Standard serving: 40-50g of pure cacao paste per 200ml water
1. Chop or break the cacao paste into small pieces
2. Heat water to 70-80°C (not boiling — same logic as mate)
3. Combine cacao and water in a small blending vessel or whisking bowl
4. Whisk vigorously for 30-60 seconds to emulsify the cacao fats with water (the original Maya technique used a specific pouring method between vessels from height — 'xocolatl' means 'foamy water')
5. Optional additions: a pinch of cayenne (Aztec tradition — the heat activates theobromine), vanilla pod scraped, pinch of cardamom (modern ceremony adaptation), pinch of cinnamon
6. No milk — this dilutes both the flavour and the pharmacological effect
7. No sugar (ceremony practitioners) — or small amount of raw honey or cane sugar for guests unfamiliar with bitterness

SERVING:
Small cups (90-120ml serving is sufficient — this is concentrated)
Temperature: Serve warm, not hot
Presentation: On a small wooden tray, possibly with a cacao pod or raw bean for visual context

THE THEOBROMINE EFFECT:
Cacao's primary active compound is theobromine (not caffeine — though cacao contains small amounts). Theobromine is a mild vasodilator and heart muscle stimulant — at ceremonial doses (40-50g pure cacao) it produces a gentle, warm, expansive feeling in the chest (hence the 'heart-opening' ceremonial description). This is pharmacologically real: theobromine expands blood vessels, increases heart rate slightly, and produces mild euphoria. It is why cacao was called 'food of the gods.'

THE CEREMONIAL CONTEXT:
In contemporary ceremonial use, cacao circles (groups of 8-30 people gathering to share ceremonial cacao) set an intention, sit in silence or with music, and spend 1-2 hours in the cacao experience. The facilitator often guides reflection, creative practice, or conversation during this period. This is not mandatory in a restaurant context — but acknowledging that the cacao has real effects, and creating space for those effects to be noticed, elevates the service.""",
  "rationale": """Ceremonial cacao occupies the digestif or pre-dessert role with pharmacological interest: the theobromine creates a sustained gentle energy, the bitterness is palate-cleansing, and the cultural weight of the beverage creates a conversation touchstone. Distinguishing ceremonial cacao from hot chocolate is one of the most effective demonstrations of beverage programme depth — most guests have never encountered pure cacao as a beverage, and the experience of drinking it is genuinely surprising.""",
  "common_errors": """Using commercial hot chocolate or cocoa powder instead of ceremonial-grade paste. Adding dairy milk (negates the traditional character and reduces bioavailability of cacao's active compounds). Serving at boiling temperature. Failing to explain the distinction between ceremonial cacao and hot chocolate — guests need context to understand what they are experiencing. Using very low-quality 'ceremonial' cacao (many brands now use the ceremonial marketing but source low-grade commodity cacao).""",
  "service_context": "fine_dining",
  "equipment_required": ["Ceremonial grade cacao paste (Keith's, Ora Cacao, Firefly, or equivalent)", "Small stainless whisking bowl or milk frother", "Wooden tray for presentation", "Small cups (90-120ml)", "Water thermometer or kettle with temperature control", "Optional: whole cayenne, vanilla pod, cinnamon, cardamom", "Optional: cacao pod or raw cacao beans for visual display"],
  "guest_communication": """Opening statement: 'We're offering you ceremonial cacao this evening — not hot chocolate. This is the pure cacao bean, stone-ground, mixed with water the way the Maya and Aztec peoples prepared it. Theobroma cacao literally means "food of the gods." It contains theobromine — a compound that gently opens the chest and creates a warm, expansive feeling. You'll notice the bitterness: this is what chocolate tasted like before sugar. There is a small amount of cayenne — this is the Aztec way of preparing xocolatl, which means "foamy water." Please sit with it for a moment when it arrives before drinking. The aroma is part of the experience.'

After service: 'The theobromine takes 15-20 minutes to reach its peak effect — you may notice a pleasant warmth in your chest over the next half hour. This is what made cacao so sacred to the cultures that discovered it.'""",
  "authority_tier": 1,
  "source_text": "Coe, S. & Coe, M. — The True History of Chocolate (Thames and Hudson, 1996); Keith's Cacao product documentation; Maya Ethnobotanical Research (Kufer, J. et al., 2006)",
  "skill_level": "advanced"
},

]

def main():
    conn = psycopg2.connect(CONN)
    cur = conn.cursor()
    inserted = 0
    for p in PROTOCOLS:
        try:
            cur.execute(SQL, (
                p["name"], p["category"], p.get("beverage_family"),
                p.get("description"), p["procedure"],
                p.get("rationale"), p.get("common_errors"),
                p.get("service_context"), p.get("equipment_required"),
                p.get("guest_communication"),
                p.get("authority_tier"), p.get("source_text"),
                p.get("skill_level"), True
            ))
            row = cur.fetchone()
            if row:
                print(f"  INSERT protocol id={row[0]}: {row[1]}")
                inserted += 1
            else:
                print(f"  SKIP (exists): {p['name']}")
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"  ERROR {p['name']}: {e}")
    print(f"\nDone. {inserted} protocols inserted.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
