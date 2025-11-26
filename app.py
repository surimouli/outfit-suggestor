from flask import Flask, render_template, request
import random

app = Flask(__name__)

# -----------------------------
# Virtual closet data
# -----------------------------
WARDROBE = [
    # Tops
    {"name": "White graphic tee", "type": "top",
     "colors": ["white"], "occasions": ["casual", "coffee", "brunch"], "warmth": "warm"},
    {"name": "Black crop top", "type": "top",
     "colors": ["black"], "occasions": ["casual", "party", "night_out"], "warmth": "warm"},
    {"name": "Blue button-up shirt", "type": "top",
     "colors": ["blue"], "occasions": ["casual", "work"], "warmth": "mild"},
    {"name": "Beige sweater", "type": "top",
     "colors": ["beige"], "occasions": ["casual", "work", "coffee"], "warmth": "cold"},
    {"name": "Pink sweatshirt", "type": "top",
     "colors": ["pink"], "occasions": ["casual", "coffee", "brunch", "gym"], "warmth": "cold"},

    # Bottoms
    {"name": "Light-wash mom jeans", "type": "bottom",
     "colors": ["blue"], "occasions": ["casual", "coffee", "brunch"], "warmth": "mild"},
    {"name": "Black high-waisted jeans", "type": "bottom",
     "colors": ["black"], "occasions": ["casual", "work", "night_out"], "warmth": "cold"},
    {"name": "Beige wide-leg trousers", "type": "bottom",
     "colors": ["beige"], "occasions": ["work", "coffee", "brunch"], "warmth": "mild"},
    {"name": "Black mini skirt", "type": "bottom",
     "colors": ["black"], "occasions": ["party", "night_out", "casual"], "warmth": "warm"},
    {"name": "Grey joggers", "type": "bottom",
     "colors": ["grey"], "occasions": ["casual", "home", "gym"], "warmth": "mild"},

    # Outerwear
    {"name": "Denim jacket", "type": "outerwear",
     "colors": ["blue"], "occasions": ["casual", "coffee", "brunch"], "warmth": "mild"},
    {"name": "Black leather jacket", "type": "outerwear",
     "colors": ["black"], "occasions": ["casual", "party", "night_out"], "warmth": "mild"},
    {"name": "Long beige coat", "type": "outerwear",
     "colors": ["beige"], "occasions": ["work", "casual"], "warmth": "cold"},
    {"name": "Cozy hoodie", "type": "outerwear",
     "colors": ["pink", "grey"], "occasions": ["casual", "home", "gym"], "warmth": "cold"},

    # Shoes
    {"name": "White sneakers", "type": "shoes",
     "colors": ["white"], "occasions": ["casual", "home", "gym", "coffee"], "warmth": "any"},
    {"name": "Black ankle boots", "type": "shoes",
     "colors": ["black"], "occasions": ["casual", "work", "party", "night_out"], "warmth": "cold"},
    {"name": "Nude heels", "type": "shoes",
     "colors": ["beige"], "occasions": ["party", "work", "brunch"], "warmth": "mild"},
    {"name": "Fluffy house slippers", "type": "shoes",
     "colors": ["pink"], "occasions": ["home"], "warmth": "any"},

    # Accessories
    {"name": "Gold hoop earrings", "type": "accessory",
     "colors": ["gold"], "occasions": ["casual", "party", "work", "night_out"], "warmth": "any"},
    {"name": "Simple silver necklace", "type": "accessory",
     "colors": ["silver"], "occasions": ["casual", "work", "coffee"], "warmth": "any"},
    {"name": "Black tote bag", "type": "accessory",
     "colors": ["black"], "occasions": ["work", "casual", "coffee"], "warmth": "any"},
    {"name": "Pink scrunchie", "type": "accessory",
     "colors": ["pink"], "occasions": ["home", "casual", "gym"], "warmth": "any"},
]


def filter_items(item_type, occasion, weather, color):
    """Return wardrobe items matching the filters."""
    matches = []
    for item in WARDROBE:
        if item["type"] != item_type:
            continue

        # Occasion: treat some choices as aliases
        occ = occasion
        if occasion == "night_out":
            occ = "night_out"
        # if occasion label not present, we still fall back later

        if occ not in item["occasions"]:
            continue

        # Weather
        warmth = item["warmth"]
        if warmth != "any":
            if weather == "cold" and warmth not in ["cold", "mild"]:
                continue
            if weather == "warm" and warmth not in ["warm", "mild", "any"]:
                continue

        # Color focus
        if color is not None and color not in item["colors"]:
            continue

        matches.append(item)
    return matches


def pick_item(item_type, occasion, weather, color):
    """Pick a single item, relaxing filters if needed."""
    # 1. strict
    items = filter_items(item_type, occasion, weather, color)
    if items:
        return random.choice(items)

    # 2. ignore color
    if color is not None:
        items = filter_items(item_type, occasion, weather, None)
        if items:
            return random.choice(items)

    # 3. ignore weather, keep occasion
    items = [i for i in WARDROBE if i["type"] == item_type and occasion in i["occasions"]]
    if items:
        return random.choice(items)

    # 4. any item of that type
    items = [i for i in WARDROBE if i["type"] == item_type]
    if items:
        return random.choice(items)

    return None


@app.route("/", methods=["GET", "POST"])
def index():
    outfit = {}
    form_data = {
        "occasion": "casual",
        "weather": "mild",
        "color": "",
    }

    if request.method == "POST":
        occasion = request.form.get("occasion", "casual")
        weather = request.form.get("weather", "mild")
        color_raw = request.form.get("color", "").strip().lower()
        color = color_raw or None

        form_data["occasion"] = occasion
        form_data["weather"] = weather
        form_data["color"] = color_raw

        top = pick_item("top", occasion, weather, color)
        bottom = pick_item("bottom", occasion, weather, color)
        shoes = pick_item("shoes", occasion, weather, color)
        outerwear = pick_item("outerwear", occasion, weather, color) if weather in ["cold", "mild"] else None
        accessory = pick_item("accessory", occasion, weather, color)

        outfit = {
            "top": top,
            "bottom": bottom,
            "outerwear": outerwear,
            "shoes": shoes,
            "accessory": accessory,
        }

    return render_template("index.html", outfit=outfit, form=form_data)


if __name__ == "__main__":
    app.run(debug=True)