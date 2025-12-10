#!/usr/bin/env python3
"""
Generate and append 100 simple recipe entries to `recipes.json`.

Run: python scripts/generate_recipes.py
"""
import json
import random
from pathlib import Path

BASE_INGREDIENTS = [
    # Proteins
    "chicken", "beef", "pork", "tofu", "tempeh", "salmon", "tuna", "shrimp",
    "cod", "turkey", "lamb", "duck", "ground turkey", "ground beef",
    # Grains & Legumes
    "rice", "pasta", "couscous", "quinoa", "soba noodles", "lentils", "chickpeas",
    "black beans", "kidney beans", "pinto beans",
    # Vegetables
    "potato", "sweet potato", "tomato", "onion", "garlic", "carrot", "bell pepper",
    "broccoli", "spinach", "mushroom", "zucchini", "eggplant", "celery", "cucumber",
    "lettuce", "kale", "chard", "asparagus", "green beans", "peas",
    # Fruits
    "avocado", "lemon", "lime", "orange", "apple", "banana",
    # Dairy & Eggs
    "egg", "milk", "cheese", "parmesan", "feta", "mozzarella", "cream", "yogurt",
    # Oils & Condiments
    "olive oil", "butter", "soy sauce", "teriyaki sauce", "vinegar", "honey",
    "mayonnaise", "salsa", "pesto",
    # Spices & Herbs
    "ginger", "cilantro", "basil", "parsley", "curry powder", "cumin", "chili powder",
    "paprika", "cinnamon", "turmeric", "garlic powder", "onion powder", "salt", "pepper",
    # Specialty
    "coconut milk", "stock", "bread", "tortillas", "seaweed", "pine nuts",
    "sesame seeds", "spring onion", "chili flakes", "coriander"
]

DIETS = [
    ["vegan"], ["vegetarian"], ["pescatarian"], ["halal"], ["kosher"], ["vegetarian", "kosher"], []
]

TEMPLATES = [
    ("{A} with {B}", [0,1]),
    ("{A} & {B} Stir-Fry", [0,1,3]),
    ("{A} Salad with {B}", [1,2]),
    ("{A} Pasta", [1,4]),
    ("{A} Soup", [1,5]),
    ("{A} Tacos", [1,6]),
    ("{A} Bowl", [1,7])
]

def make_recipe(i: int):
    # pick 4-7 random ingredients
    ings = random.sample(BASE_INGREDIENTS, k=random.randint(4,7))
    title = f"{ings[0].capitalize()} {random.choice(['Delight','Special','Bowl','Sauté','Medley','Salad','Skillet'])}"
    time = f"{random.choice([10,15,20,25,30,35,40,45])} minutes"
    diets = random.choice(DIETS)
    steps = [f"Prepare the {ings[0]} and other ingredients.", f"Cook {', '.join(ings[1:3])} until ready.", "Combine ingredients and serve."]
    tags = [ings[0]]
    return {
        "title": title,
        "ingredients": ings,
        "time": time,
        "diets": diets,
        "steps": steps,
        "tags": tags
    }

def main():
    repo = Path(__file__).resolve().parents[1]
    rpath = repo / "recipes.json"
    if not rpath.exists():
        print("recipes.json not found; aborting")
        return
    with open(rpath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print("Failed to read recipes.json:", e)
            return

    start = len(data) + 1
    to_add = 100
    for i in range(to_add):
        rec = make_recipe(start + i)
        data.append(rec)

    with open(rpath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Appended {to_add} recipes to {rpath}")

if __name__ == '__main__':
    main()
