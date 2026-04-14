#!/usr/bin/env python3
"""terminal4_batch16_protocols.py — 3 new service protocols for Italian digestifs, German beer, Pacific spirits"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """
INSERT INTO service_protocols
  (name, category, beverage_family, description, procedure, rationale, common_errors,
   service_context, equipment_required, guest_communication, authority_tier, source_text, skill_level)
VALUES
  (%(name)s, %(category)s, %(beverage_family)s, %(description)s, %(procedure)s, %(rationale)s,
   %(common_errors)s, %(service_context)s, %(equipment_required)s, %(guest_communication)s,
   %(authority_tier)s, %(source_text)s, %(skill_level)s)
RETURNING id, name
"""

PROTOCOLS = [
    {
        "name": "Italian Digestif Service — Amaro, Grappa, and Fernet-Branca",
        "category": "spirit_service",
        "beverage_family": "spirits",
        "description": "Service protocol for Italian digestifs including amaro, grappa, and bitter liqueurs, covering temperature, glassware, and the cultural context of fine Italian tableside service.",
        "procedure": (
            "1. Confirm guest preference: amaro (bitter, herbal), grappa (pomace spirit), or bitter liqueur such as Fernet-Branca. "
            "2. For amaro: serve at room temperature (18-20C) in a small stemmed glass or tulip; no ice unless guest requests. "
            "3. For grappa: serve chilled (8-10C) in a narrow tulip grappa glass that concentrates the aromatic compounds; hold the glass at the base. "
            "4. For Fernet-Branca: present bottle tableside, pour 30-45ml over a single ice cube in a rocks glass; acknowledge its bitter medicinal character with confidence. "
            "5. Present the digestif on a small service plate with a folded napkin. "
            "6. For flight service: arrange from lightest (Amaro Montenegro) to most intense (Fernet-Branca) left to right; explain each style briefly. "
            "7. Offer to describe the herb or botanical signature of each selection on request."
        ),
        "rationale": (
            "Italian digestifs are the traditional close to a fine dining meal in Italian culture. The variety of styles — from light amaro to intense bitter "
            "to pomace-derived grappa — requires the sommelier to match character to guest appetite for bitterness and the nature of their meal."
        ),
        "common_errors": (
            "Serving amaro too cold (dulls aromatics); over-icing Fernet-Branca (dilutes the complex bitters); presenting grappa in a wide wine glass "
            "(disperses volatile aromatics); failing to explain the bitter character of Fernet before pouring — this surprises unprepared guests."
        ),
        "service_context": "fine_dining",
        "equipment_required": ["grappa tulip glass", "rocks glass", "small stemmed glass", "service tray", "ice bucket", "tongs"],
        "guest_communication": (
            "This is a traditional Italian digestif — designed to settle the stomach and close the meal. [Name] has a signature bitter herb profile; "
            "I would describe it as [flavour brief]. Would you prefer it neat, or over ice?"
        ),
        "authority_tier": 2,
        "source_text": "CCI Italian Beverage Service Standards 2024",
        "skill_level": "advanced",
    },
    {
        "name": "Kolsch and Altbier German Specialty Beer Service",
        "category": "general_tableside",
        "beverage_family": "beer",
        "description": (
            "Traditional service protocol for Cologne Kolsch and Dusseldorf Altbier, respecting their regional glassware "
            "(Stange for Kolsch, Becher for Altbier), temperature standards, and continuous pour tradition."
        ),
        "procedure": (
            "1. For Kolsch: serve in a Stange (slender cylindrical glass, 200ml); chill glass to 4-6C; pour tilting at 45 degrees to minimise foam, "
            "then straighten as fill approaches top; target 3-4cm white foam crown. "
            "2. For Altbier: serve in a Becher (short cylindrical glass, 200ml); chill to 8-10C; pour with a controlled 3-4cm foam head. "
            "3. Traditional Cologne service: Kolsches are carried on a Kranz (circular tray); replenishment is continuous until the guest places a beer mat on "
            "top of their glass to signal they are done. Adapt this tradition for fine dining by offering refills proactively. "
            "4. Never serve either style with ice; both have served temperatures warmer than common lager — adjust guest expectations if required. "
            "5. Present the bottle or can with the label visible before opening; describe the brewery and city of origin briefly."
        ),
        "rationale": (
            "Kolsch and Altbier are protected regional styles (Kolsch is a geographically protected designation from Cologne; Altbier is associated "
            "exclusively with Dusseldorf). Both are served in small traditional glasses by design — the small vessel ensures the beer remains fresh and "
            "cold throughout consumption. This is not a shortcoming but a feature of the style."
        ),
        "common_errors": (
            "Serving in a large American pint glass (wrong glass, wrong temperature management); serving Kolsch too cold (below 4C dulls the delicate yeast "
            "character); explaining the small glass apologetically — it is traditional and correct; failing to offer refills proactively in the Cologne tradition."
        ),
        "service_context": "casual_dining",
        "equipment_required": ["Stange glass 200ml", "Becher glass 200ml", "service tray", "Kranz if available", "beer mat"],
        "guest_communication": (
            "This is [Gaffel/Uerige] — a [Kolsch/Altbier] from [Cologne/Dusseldorf]. In the German tradition it comes in a smaller glass to keep it "
            "fresh and cold; I will be happy to replenish it for you throughout the meal."
        ),
        "authority_tier": 3,
        "source_text": "German Beer Institute Service Standards 2024; VLB Berlin",
        "skill_level": "intermediate",
    },
    {
        "name": "Pacific and Southeast Asian Traditional Spirit Service",
        "category": "general_tableside",
        "beverage_family": "traditional",
        "description": (
            "Service and ceremony protocol for traditional Pacific and Southeast Asian spirits and fermented beverages including Philippine Lambanog, "
            "Filipino Basi, and related indigenous preparations for fine dining and cultural dining contexts."
        ),
        "procedure": (
            "1. For Lambanog: present the bottle with an explanation of its coconut sap origin and Quezon Province production. Serve at room temperature "
            "(20-22C) in a small shot glass (30-45ml) or a traditional buri palm coconut shell cup. Never serve with ice. "
            "2. For Basi (fermented sugarcane): decant slightly chilled (12-14C) into a small ceramic or clay cup; explain the camias-acidulated fermentation "
            "and its Ilocos Region heritage. "
            "3. Pulutan pairing: present suggested accompaniments — chicharon, kinilaw, or local equivalents — as traditional companions to these spirits. "
            "4. For ceremonial contexts: acknowledge the social and ritual dimension; sharing from a common vessel is traditional but hygienically adapted for "
            "restaurant service by providing individual pours from the same bottle. "
            "5. For guests unfamiliar with the category: begin with a small tasting pour (15ml) and describe the flavour profile before committing to full service. "
            "6. Describe alcohol content accurately — Lambanog 40-80% ABV depending on distillation; Basi 10-14% as a fermented wine."
        ),
        "rationale": (
            "Philippine Lambanog and Basi are among Southeast Asia's oldest indigenous spirit traditions with pre-colonial roots. They represent the "
            "Austronesian fermentation trail and carry significant cultural weight in Philippine dining contexts. Presenting them with confidence and cultural "
            "knowledge elevates the dining experience and honours the producer heritage."
        ),
        "common_errors": (
            "Apologising for unfamiliarity instead of expressing confidence in the cultural heritage; serving Lambanog over ice (dilutes the coconut terroir); "
            "neglecting to explain ABV of high-proof Lambanog (can exceed 70% in artisan variants); presenting without cultural context — the story is the "
            "most important element of service."
        ),
        "service_context": "fine_dining",
        "equipment_required": ["small shot glass or coconut shell cup", "ceramic pour vessel", "service tray", "pulutan accompaniments plate"],
        "guest_communication": (
            "This is [Lambanog/Basi] — a traditional [Filipino coconut spirit / fermented sugarcane wine] from [Quezon Province / Ilocos Region]. "
            "It has been produced in this tradition for over 400 years. The flavour is [brief descriptor]. Would you like a small tasting pour first?"
        ),
        "authority_tier": 3,
        "source_text": "Filipino Food and Beverage Heritage Institute; SCA Southeast Asia 2024",
        "skill_level": "intermediate",
    },
]

def main():
    conn = psycopg2.connect(CONN)
    for p in PROTOCOLS:
        try:
            with conn.cursor() as cur:
                cur.execute(SQL, p)
                row = cur.fetchone()
                conn.commit()
                print(f"  OK id={row[0]} name={row[1][:70]}")
        except Exception as e:
            conn.rollback()
            print(f"  FAIL {p['name'][:50]}: {e}")
    conn.close()

if __name__ == "__main__":
    main()
