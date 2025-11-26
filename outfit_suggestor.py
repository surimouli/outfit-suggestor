import random

# -----------------------------
# Simple "virtual closet" data
# -----------------------------
WARDROBE = [
    # Tops
    {"name": "White graphic tee", "type": "top", "colors": ["white"], "occasions": ["casual"], "warmth": "warm"},
    {"name": "Black crop top", "type": "top", "colors": ["black"], "occasions": ["casual", "party"], "warmth": "warm"},
    {"name": "Blue button-up shirt", "type": "top", "colors": ["blue"], "occasions": ["casual", "work"], "warmth": "mild"},
    {"name": "Beige sweater", "type": "top", "colors": ["beige"], "occasions": ["casual", "work"], "warmth": "cold"},
    {"name": "Pink sweatshirt", "type": "top", "colors": ["pink"], "occasions": ["casual"], "warmth": "cold"},

    # Bottoms
    {"name": "Light-wash mom jeans", "type": "bottom", "colors": ["blue"], "occasions": ["casual"], "warmth": "mild"},
    {"name": "Black high-waisted jeans", "type": "bottom", "colors": ["black"], "occasions": ["casual", "work"], "warmth": "cold"},
    {"name": "Beige wide-leg trousers", "type": "bottom", "colors": ["beige"], "occasions": ["work"], "warmth": "mild"},
    {"name": "Black mini skirt", "type": "bottom", "colors": ["black"], "occasions": ["party", "casual"], "warmth": "warm"},
    {"name": "Grey joggers", "type": "bottom", "colors": ["grey"], "occasions": ["casual", "home"], "warmth": "mild"},

    # Outerwear
    {"name": "Denim jacket", "type": "outerwear", "colors": ["blue"], "occasions": ["casual"], "warmth": "mild"},
    {"name": "Black leather jacket", "type": "outerwear", "colors": ["black"], "occasions": ["casual", "party"], "warmth": "mild"},
    {"name": "Long beige coat", "type": "outerwear", "colors": ["beige"], "occasions": ["work", "casual"], "warmth": "cold"},
    {"name": "Cozy hoodie", "type": "outerwear", "colors": ["pink", "grey"], "occasions": ["casual", "home"], "warmth": "cold"},

    # Shoes
    {"name": "White sneakers", "type": "shoes", "colors": ["white"], "occasions": ["casual", "home"], "warmth": "any"},
    {"name": "Black ankle boots", "type": "shoes", "colors": ["black"], "occasions": ["casual", "work", "party"], "warmth": "cold"},
    {"name": "Nude heels", "type": "shoes", "colors": ["beige"], "occasions": ["party", "work"], "warmth": "mild"},
    {"name": "Fluffy house slippers", "type": "shoes", "colors": ["pink"], "occasions": ["home"], "warmth": "any"},

    # Accessories
    {"name": "Gold hoop earrings", "type": "accessory", "colors": ["gold"], "occasions": ["casual", "party", "work"], "warmth": "any"},
    {"name": "Simple silver necklace", "type": "accessory", "colors": ["silver"], "occasions": ["casual", "work"], "warmth": "any"},
    {"name": "Black tote bag", "type": "accessory", "colors": ["black"], "occasions": ["work", "casual"], "warmth": "any"},
    {"name": "Pink scrunchie", "type": "accessory", "colors": ["pink"], "occasions": ["home", "casual"], "warmth": "any"},
]


def ask_occasion():
    print("\n✨ What’s the occasion?")
    print("  1. Casual")
    print("  2. Work / Class")
    print("  3. Party / Night out")
    print("  4. Staying home / comfy")

    choice = input("Choose 1–4: ").strip()

    mapping = {
        "1": "casual",
        "2": "work",
        "3": "party",
        "4": "home",
    }
    return mapping.get(choice, "casual")


def ask_weather():
    print("\n🌤 What’s the weather like?")
    print("  1. Cold")
    print("  2. Mild")
    print("  3. Warm / Hot")

    choice = input("Choose 1–3: ").strip()
    mapping = {
        "1": "cold",
        "2": "mild",
        "3": "warm",
    }
    return mapping.get(choice, "mild")


def ask_color():
    print("\n🎨 Any color vibe?")
    print("Type a color (like pink, black, beige) or press Enter for 'surprise me'")
    color = input("Color: ").strip().lower()
    return color if color else None


def filter_items(item_type, occasion, weather, color):
    """
    Filter WARDROBE items by type, occasion, weather, and optional color.
    Returns a list of matching items.
    """
    matches = []
    for item in WARDROBE:
        if item["type"] != item_type:
            continue

        # Occasion check
        if occasion not in item["occasions"]:
            continue

        # Weather / warmth check
        warmth = item["warmth"]
        if warmth != "any":
            if weather == "cold" and warmth not in ["cold", "mild"]:
                continue
            if weather == "mild" and warmth not in ["mild", "any", "cold", "warm"]:
                # Basically allow anything but still keep logic explicit
                pass
            if weather == "warm" and warmth not in ["warm", "mild", "any"]:
                continue

        # Color preference check
        if color is not None and color not in item["colors"]:
            continue

        matches.append(item)

    return matches


def pick_item(item_type, occasion, weather, color):
    """Try to pick one item, relaxing color/weather if needed."""
    # 1. Try strict filter
    items = filter_items(item_type, occasion, weather, color)
    if items:
        return random.choice(items)

    # 2. Relax color
    if color is not None:
        items = filter_items(item_type, occasion, weather, None)
        if items:
            return random.choice(items)

    # 3. Relax weather (just match type + occasion)
    items = [i for i in WARDROBE if i["type"] == item_type and occasion in i["occasions"]]
    if items:
        return random.choice(items)

    # 4. Last resort: anything of that type
    items = [i for i in WARDROBE if i["type"] == item_type]
    if items:
        return random.choice(items)

    return None


def suggest_outfit():
    print("\n💖 Welcome to your Outfit Suggestor 💖")

    occasion = ask_occasion()
    weather = ask_weather()
    color = ask_color()

    top = pick_item("top", occasion, weather, color)
    bottom = pick_item("bottom", occasion, weather, color)
    shoes = pick_item("shoes", occasion, weather, color)

    # Outerwear only if cold or mild
    outerwear = None
    if weather in ["cold", "mild"]:
        outerwear = pick_item("outerwear", occasion, weather, color)

    accessory = pick_item("accessory", occasion, weather, color)

    print("\n------------------------------")
    print("👗 Your outfit suggestion is:")
    print("------------------------------")

    if top:
        print(f"   Top:        {top['name']}")
    if bottom:
        print(f"   Bottom:     {bottom['name']}")
    if outerwear:
        print(f"   Outerwear:  {outerwear['name']}")
    if shoes:
        print(f"   Shoes:      {shoes['name']}")
    if accessory:
        print(f"   Accessory:  {accessory['name']}")

    print("\nGo slay ✨🫶\n")


def show_wardrobe():
    print("\n🧥 Current wardrobe items:\n")
    by_type = {}
    for item in WARDROBE:
        by_type.setdefault(item["type"], []).append(item)

    for t, items in by_type.items():
        print(f"- {t.capitalize()}:")
        for i in items:
            colors = ", ".join(i["colors"])
            occasions = ", ".join(i["occasions"])
            print(f"    • {i['name']}  | colors: {colors} | occasions: {occasions} | warmth: {i['warmth']}")
        print()


def main_menu():
    while True:
        print("====== Outfit Suggestor ======")
        print("1. Get an outfit suggestion")
        print("2. View wardrobe items")
        print("3. Exit")

        choice = input("Choose 1–3: ").strip()

        if choice == "1":
            suggest_outfit()
        elif choice == "2":
            show_wardrobe()
        elif choice == "3":
            print("Bye bestie, see you next outfit 💅")
            break
        else:
            print("Please choose a valid option.\n")


if __name__ == "__main__":
    main_menu()