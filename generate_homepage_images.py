import os
import fal_client
import json

os.environ["FAL_KEY"] = "bc3af9ee-d609-4abe-925a-75062339d8d1:89286252cf2dc3f929449ecce4f66dc9"

BASE = (
    "Very dark almost black background. "
    "Single directional side lighting, deep dramatic shadows. "
    "Moody, minimal, high contrast. "
    "No people, no text, no watermarks. "
    "Shot on medium format camera. "
    "Michelin-starred restaurant or bar presentation."
)

def generate(prompt, label):
    print(f"Generating: {label}...")
    try:
        result = fal_client.subscribe(
            "fal-ai/flux-pro/v1.1",
            arguments={
                "prompt": prompt,
                "width": 1280,
                "height": 768,
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
            }
        )
        url = result["images"][0]["url"]
        print(f"  ✓ {label}: {url}")
        return url
    except Exception as e:
        print(f"  ✗ {label}: {e}")
        return None

results = {}

# ── RECIPES ──
results["rendang"] = generate(
    f"Professional editorial food photography of Indonesian beef rendang. "
    f"Dark caramelised dry beef chunks coated in rich coconut spice paste, "
    f"served on matte black ceramic plate. Kaffir lime leaf and dried chilli garnish. "
    f"Slight overhead angle. {BASE}",
    "Rendang"
)

results["mole-negro-oaxacan-full-30-ingredient-method-charring-and-grinding"] = generate(
    f"Professional editorial food photography of Oaxacan mole negro. "
    f"Deep near-black sauce over turkey or chicken on a dark ceramic plate. "
    f"Sesame seeds and dried chilli garnish. Overhead angle. {BASE}",
    "Mole Negro"
)

results["dashi"] = generate(
    f"Professional editorial food photography of Japanese dashi broth. "
    f"Clear golden broth in a white ceramic bowl, kombu and bonito visible. "
    f"Minimal Japanese presentation. Slight overhead angle. {BASE}",
    "Dashi"
)

results["bouillabaisse"] = generate(
    f"Professional editorial food photography of French bouillabaisse. "
    f"Rich saffron broth with whole fish, mussels, prawns in a dark ceramic bowl. "
    f"Rouille toast on the side. Slight overhead angle. {BASE}",
    "Bouillabaisse"
)

results["ethiopian-injera-the-3000-year-old-fermented-flatbread"] = generate(
    f"Professional editorial food photography of Ethiopian injera. "
    f"Spongy grey-brown teff flatbread on a dark plate or communal platter, "
    f"small bowls of wat stew alongside. Overhead angle. {BASE}",
    "Injera"
)

results["ceviche"] = generate(
    f"Professional editorial food photography of Peruvian ceviche. "
    f"White sea bass in leche de tigre, thinly sliced red onion, rocoto chilli, "
    f"sweet potato, corn kernels. Served in a dark ceramic bowl. Overhead angle. {BASE}",
    "Ceviche"
)

# ── DRINKS ──
results["negroni"] = generate(
    f"Professional editorial cocktail photography of a Negroni. "
    f"Deep ruby red in a rocks glass with large ice cube, orange peel twist garnish. "
    f"Dark bar surface. Campari red glow. {BASE}",
    "Negroni"
)

results["espresso-martini"] = generate(
    f"Professional editorial cocktail photography of an espresso martini. "
    f"Dark coffee brown liquid in a coupe glass, thick white foam top, "
    f"three coffee beans on foam. Dark background. {BASE}",
    "Espresso Martini"
)

results["champagne"] = generate(
    f"Professional editorial drink photography of champagne. "
    f"Fine bubbles rising in a tall crystal flute, golden liquid. "
    f"Dark elegant background. {BASE}",
    "Champagne"
)

results["flat-white"] = generate(
    f"Professional editorial coffee photography of a flat white. "
    f"White ceramic cup on dark saucer, perfect latte art rosetta on surface. "
    f"Dark cafe background. {BASE}",
    "Flat White"
)

results["masala-chai"] = generate(
    f"Professional editorial drink photography of masala chai. "
    f"Spiced tea in a small glass or clay cup, cinnamon sticks and "
    f"cardamom pods as garnish, warm steam rising. {BASE}",
    "Masala Chai"
)

results["margarita"] = generate(
    f"Professional editorial cocktail photography of a margarita. "
    f"Classic coupe glass, salted rim, lime wheel garnish, "
    f"clear citrus liquid. Dark bar background. {BASE}",
    "Margarita"
)

print("\n\nFINAL RESULTS:")
print(json.dumps(results, indent=2))
