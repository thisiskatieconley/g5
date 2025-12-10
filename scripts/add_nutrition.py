#!/usr/bin/env python3
"""
Add simple nutrition estimates to recipes.json using a best-effort ingredient-based lookup.

Estimates are rough approximations per serving and should NOT be used for medical/diet purposes.

Run: python3 scripts/add_nutrition.py
This updates `recipes.json` in place with a `nutrition` field per recipe.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RPATH = BASE / "recipes.json"

# Per-ingredient estimates (simplified, per ~1 unit/serving)
# Format: ingredient -> (calories, protein_g, carbs_g, fat_g)
INGREDIENT_NUTRITION = {
    "chicken": (165, 26, 0, 7),
    "beef": (250, 26, 0, 15),
    "pork": (242, 27, 0, 13),
    "tofu": (76, 8, 2, 5),
    "tempeh": (195, 19, 9, 11),
    "salmon": (280, 25, 0, 20),
    "tuna": (144, 30, 0, 1),
    "shrimp": (99, 24, 0, 0.3),
    "cod": (82, 18, 0, 1),
    "turkey": (189, 26, 0, 8.5),
    "rice": (206, 4, 45, 0.3),
    "pasta": (371, 13, 75, 1),
    "couscous": (376, 13, 77, 0.6),
    "quinoa": (368, 14, 64, 6),
    "bread": (265, 9, 49, 3),
    "potato": (77, 2, 17, 0.1),
    "sweet potato": (86, 2, 20, 0.1),
    "egg": (78, 6, 1, 6),
    "milk": (61, 3, 5, 3),
    "cheese": (402, 25, 1, 33),
    "yogurt": (59, 10, 3, 0.4),
    "butter": (717, 0, 0, 81),
    "olive oil": (884, 0, 0, 100),
    "tomato": (18, 1, 4, 0.2),
    "onion": (40, 1, 9, 0.1),
    "garlic": (49, 2, 11, 0.5),
    "carrot": (41, 1, 10, 0.2),
    "broccoli": (34, 3, 7, 0.4),
    "spinach": (23, 3, 4, 0.4),
    "mushroom": (22, 3, 3, 0.3),
    "bell pepper": (31, 1, 6, 0.3),
    "lentils": (116, 9, 20, 0.4),
    "chickpeas": (164, 9, 27, 3),
    "black beans": (132, 9, 24, 0.5),
    "avocado": (160, 2, 9, 15),
    "lemon": (17, 1, 5, 0.3),
    "coconut milk": (230, 2, 5, 24),
    "flour": (364, 10, 76, 1),
    "soy sauce": (80, 12, 7, 0),
}

def estimate_nutrition(ingredients):
    """Estimate total nutrition from ingredient list.
    
    Returns dict with calories, protein_g, carbs_g, fat_g (rough totals per recipe).
    """
    total_cal = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    for ing_name in ingredients:
        ing_lower = ing_name.lower()
        # Try exact match first
        if ing_lower in INGREDIENT_NUTRITION:
            cal, p, c, f = INGREDIENT_NUTRITION[ing_lower]
            total_cal += cal
            total_protein += p
            total_carbs += c
            total_fat += f
        else:
            # Try substring match on base ingredient word
            for key, (cal, p, c, f) in INGREDIENT_NUTRITION.items():
                if key in ing_lower:
                    total_cal += cal
                    total_protein += p
                    total_carbs += c
                    total_fat += f
                    break

    # Return rounded estimates
    return {
        "calories": round(total_cal),
        "protein_g": round(total_protein, 1),
        "carbs_g": round(total_carbs, 1),
        "fat_g": round(total_fat, 1),
    }

def main():
    if not RPATH.exists():
        print("recipes.json not found; aborting")
        return

    with open(RPATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for r in data:
        ingredients = r.get("ingredients", [])
        nutrition = estimate_nutrition(ingredients)
        r["nutrition"] = nutrition
        updated += 1

    with open(RPATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {updated} recipes with nutrition estimates.")
    print("Estimates are rough and should NOT be used for medical/diet purposes.")
    print("Sample recipe nutrition:")
    for r in data[:3]:
        n = r.get("nutrition", {})
        print(f" - {r.get('title')}: {n.get('calories')} cal, {n.get('protein_g')}g protein, {n.get('carbs_g')}g carbs, {n.get('fat_g')}g fat")

if __name__ == '__main__':
    main()
