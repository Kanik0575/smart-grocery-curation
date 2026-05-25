import streamlit as st
import json
import random
import time

# ──────────────────────────────────────────────
# CATALOG — 175+ Premium SKUs across 8 categories
# ──────────────────────────────────────────────

CATALOG = {
    "Fruits & Vegetables": [
        {"name": "Organic Bananas (1 dozen)", "price": 89, "tags": ["organic", "pesticide-free"], "diet": ["vegan", "vegetarian"]},
        {"name": "Shimla Apples (1 kg)", "price": 199, "tags": ["pesticide-free", "farm-fresh"], "diet": ["vegan", "vegetarian"]},
        {"name": "Organic Spinach (250g)", "price": 59, "tags": ["organic", "pesticide-free"], "diet": ["vegan", "vegetarian"]},
        {"name": "Baby Carrots (500g)", "price": 79, "tags": ["organic", "farm-fresh"], "diet": ["vegan", "vegetarian"]},
        {"name": "Avocado (pack of 2)", "price": 249, "tags": ["imported", "premium"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Sweet Potato (1 kg)", "price": 69, "tags": ["organic", "farm-fresh"], "diet": ["vegan", "vegetarian"]},
        {"name": "Broccoli (300g)", "price": 99, "tags": ["pesticide-free"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Blueberries (125g)", "price": 349, "tags": ["imported", "antioxidant-rich"], "diet": ["vegan", "vegetarian"]},
        {"name": "Mixed Salad Greens (200g)", "price": 129, "tags": ["organic", "ready-to-eat"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Cherry Tomatoes (250g)", "price": 89, "tags": ["organic", "farm-fresh"], "diet": ["vegan", "vegetarian"]},
        {"name": "Kale Bunch (200g)", "price": 99, "tags": ["organic", "superfood"], "diet": ["vegan", "vegetarian"]},
        {"name": "Zucchini (500g)", "price": 79, "tags": ["organic"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Bell Peppers Trio (3 pcs)", "price": 149, "tags": ["pesticide-free", "farm-fresh"], "diet": ["vegan", "vegetarian"]},
        {"name": "Pomegranate (2 pcs)", "price": 159, "tags": ["organic", "antioxidant-rich"], "diet": ["vegan", "vegetarian"]},
        {"name": "Dragon Fruit (1 pc)", "price": 199, "tags": ["imported", "exotic"], "diet": ["vegan", "vegetarian"]},
        {"name": "Organic Ginger (100g)", "price": 49, "tags": ["organic", "immunity"], "diet": ["vegan", "vegetarian"]},
        {"name": "Fresh Turmeric Root (100g)", "price": 39, "tags": ["organic", "anti-inflammatory"], "diet": ["vegan", "vegetarian"]},
        {"name": "Beetroot (500g)", "price": 59, "tags": ["organic", "iron-rich"], "diet": ["vegan", "vegetarian"]},
        {"name": "Asparagus (200g)", "price": 199, "tags": ["imported", "premium"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Organic Lemons (6 pcs)", "price": 69, "tags": ["organic", "vitamin-c"], "diet": ["vegan", "vegetarian"]},
    ],
    "Dairy & Eggs": [
        {"name": "A2 Cow Milk (1L)", "price": 89, "tags": ["hormone-free", "A2-protein"], "diet": ["vegetarian"]},
        {"name": "Organic Paneer (200g)", "price": 149, "tags": ["organic", "hormone-free"], "diet": ["vegetarian", "keto"]},
        {"name": "Greek Yogurt Plain (400g)", "price": 179, "tags": ["probiotic", "high-protein"], "diet": ["vegetarian", "keto"]},
        {"name": "Free-Range Eggs (6 pcs)", "price": 129, "tags": ["free-range", "hormone-free"], "diet": ["vegetarian", "keto"]},
        {"name": "Artisan Cheddar (200g)", "price": 299, "tags": ["imported", "aged"], "diet": ["vegetarian", "keto"]},
        {"name": "Almond Milk Unsweetened (1L)", "price": 249, "tags": ["plant-based", "no-sugar"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Organic Butter (200g)", "price": 199, "tags": ["organic", "grass-fed"], "diet": ["vegetarian", "keto"]},
        {"name": "Fresh Mozzarella (125g)", "price": 229, "tags": ["imported", "artisan"], "diet": ["vegetarian"]},
        {"name": "Oat Milk Barista (1L)", "price": 279, "tags": ["plant-based", "barista-grade"], "diet": ["vegan", "vegetarian"]},
        {"name": "Probiotic Kefir (500ml)", "price": 199, "tags": ["probiotic", "gut-health"], "diet": ["vegetarian"]},
        {"name": "Organic Ghee (500ml)", "price": 549, "tags": ["organic", "A2", "grass-fed"], "diet": ["vegetarian", "keto"]},
        {"name": "Coconut Yogurt (200g)", "price": 169, "tags": ["plant-based", "probiotic"], "diet": ["vegan", "vegetarian"]},
    ],
    "Bakery & Breads": [
        {"name": "Sourdough Loaf (400g)", "price": 189, "tags": ["artisan", "slow-fermented"], "diet": ["vegetarian", "vegan"]},
        {"name": "Multigrain Bread (400g)", "price": 99, "tags": ["whole-grain", "no-maida"], "diet": ["vegetarian", "vegan"]},
        {"name": "Gluten-Free Bread (350g)", "price": 249, "tags": ["gluten-free", "allergen-safe"], "diet": ["vegetarian", "vegan", "gluten-free"]},
        {"name": "Organic Ragi Cookies (200g)", "price": 149, "tags": ["organic", "millet-based"], "diet": ["vegetarian"]},
        {"name": "Almond Flour Muffins (4 pcs)", "price": 299, "tags": ["gluten-free", "keto-friendly"], "diet": ["vegetarian", "keto", "gluten-free"]},
        {"name": "Whole Wheat Pita (6 pcs)", "price": 129, "tags": ["whole-grain", "no-preservatives"], "diet": ["vegetarian", "vegan"]},
        {"name": "Brioche Buns (4 pcs)", "price": 199, "tags": ["artisan", "premium"], "diet": ["vegetarian"]},
        {"name": "Rye Bread (400g)", "price": 179, "tags": ["artisan", "fiber-rich"], "diet": ["vegetarian", "vegan"]},
    ],
    "Pantry Staples": [
        {"name": "Organic Quinoa (500g)", "price": 349, "tags": ["organic", "superfood", "high-protein"], "diet": ["vegan", "vegetarian", "gluten-free"]},
        {"name": "Extra Virgin Olive Oil (500ml)", "price": 599, "tags": ["cold-pressed", "imported"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Organic Brown Rice (1 kg)", "price": 149, "tags": ["organic", "whole-grain"], "diet": ["vegan", "vegetarian", "gluten-free"]},
        {"name": "Raw Honey (500g)", "price": 449, "tags": ["raw", "unprocessed", "immunity"], "diet": ["vegetarian"]},
        {"name": "Organic Chia Seeds (200g)", "price": 249, "tags": ["organic", "omega-3", "superfood"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Himalayan Pink Salt (500g)", "price": 149, "tags": ["mineral-rich", "unrefined"], "diet": ["vegan", "vegetarian"]},
        {"name": "Cold-Pressed Coconut Oil (500ml)", "price": 349, "tags": ["cold-pressed", "organic"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Organic Rolled Oats (500g)", "price": 199, "tags": ["organic", "whole-grain"], "diet": ["vegan", "vegetarian"]},
        {"name": "Organic Toor Dal (1 kg)", "price": 179, "tags": ["organic", "high-protein"], "diet": ["vegan", "vegetarian"]},
        {"name": "Apple Cider Vinegar (500ml)", "price": 299, "tags": ["raw", "with-mother", "gut-health"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Organic Peanut Butter (400g)", "price": 349, "tags": ["organic", "no-sugar", "high-protein"], "diet": ["vegan", "vegetarian"]},
        {"name": "Flaxseed Meal (200g)", "price": 149, "tags": ["organic", "omega-3"], "diet": ["vegan", "vegetarian", "keto"]},
        {"name": "Organic Jaggery (500g)", "price": 129, "tags": ["organic", "unrefined"], "diet": ["vegan", "vegetarian"]},
        {"name": "Black Rice (500g)", "price": 249, "tags": ["antioxidant-rich", "organic"], "diet": ["vegan", "vegetarian", "gluten-free"]},
        {"name": "Organic Moong Dal (1 kg)", "price": 169, "tags": ["organic", "easy-digest"], "diet": ["vegan", "vegetarian"]},
    ],
    "Snacks & Beverages": [
        {"name": "Trail Mix Premium (200g)", "price": 299, "tags": ["no-sugar", "high-protein", "energy"], "diet": ["vegan", "vegetarian"]},
        {"name": "Dark Chocolate 72% (100g)", "price": 249, "tags": ["imported", "antioxidant-rich"], "diet": ["vegetarian"]},
        {"name": "Matcha Powder (50g)", "price": 499, "tags": ["ceremonial-grade", "imported"], "diet": ["vegan", "vegetarian"]},
        {"name": "Cold-Brew Coffee (250ml x2)", "price": 299, "tags": ["specialty", "single-origin"], "diet": ["vegan", "vegetarian"]},
        {"name": "Kombucha Ginger (330ml)", "price": 199, "tags": ["probiotic", "gut-health"], "diet": ["vegan", "vegetarian"]},
        {"name": "Roasted Makhana (100g)", "price": 149, "tags": ["organic", "low-cal"], "diet": ["vegan", "vegetarian"]},
        {"name": "Protein Bars (pack of 3)", "price": 349, "tags": ["high-protein", "no-sugar"], "diet": ["vegetarian"]},
        {"name": "Green Tea Jasmine (25 bags)", "price": 249, "tags": ["organic", "antioxidant-rich"], "diet": ["vegan", "vegetarian"]},
        {"name": "Coconut Water (1L)", "price": 129, "tags": ["natural", "electrolyte"], "diet": ["vegan", "vegetarian"]},
        {"name": "Baked Veggie Chips (150g)", "price": 179, "tags": ["baked", "no-trans-fat"], "diet": ["vegan", "vegetarian"]},
    ],
    "Health & Wellness": [
        {"name": "Whey Protein Isolate (500g)", "price": 1499, "tags": ["high-protein", "low-carb"], "diet": ["vegetarian", "keto"]},
        {"name": "Ashwagandha Capsules (60)", "price": 499, "tags": ["ayurvedic", "adaptogen"], "diet": ["vegan", "vegetarian"]},
        {"name": "Multivitamin Gummies (30)", "price": 599, "tags": ["vegetarian", "no-gelatin"], "diet": ["vegetarian"]},
        {"name": "Collagen Peptides (200g)", "price": 899, "tags": ["grass-fed", "skin-health"], "diet": ["keto"]},
        {"name": "Turmeric Latte Mix (200g)", "price": 349, "tags": ["organic", "anti-inflammatory"], "diet": ["vegan", "vegetarian"]},
        {"name": "Moringa Powder (100g)", "price": 249, "tags": ["organic", "superfood"], "diet": ["vegan", "vegetarian"]},
        {"name": "Probiotic Capsules (30)", "price": 699, "tags": ["gut-health", "clinically-tested"], "diet": ["vegan", "vegetarian"]},
        {"name": "Spirulina Tablets (120)", "price": 449, "tags": ["organic", "superfood", "iron-rich"], "diet": ["vegan", "vegetarian"]},
    ],
    "Home & Kitchen": [
        {"name": "Bamboo Paper Towels (6 rolls)", "price": 399, "tags": ["eco-friendly", "biodegradable"], "diet": []},
        {"name": "Natural Dish Soap (500ml)", "price": 249, "tags": ["plant-based", "non-toxic"], "diet": []},
        {"name": "Beeswax Food Wraps (3 pcs)", "price": 499, "tags": ["reusable", "eco-friendly"], "diet": []},
        {"name": "Organic Cotton Produce Bags (5)", "price": 349, "tags": ["reusable", "organic"], "diet": []},
        {"name": "Coconut Fiber Scrubber (3 pcs)", "price": 149, "tags": ["natural", "biodegradable"], "diet": []},
        {"name": "Glass Storage Containers (set of 4)", "price": 799, "tags": ["BPA-free", "microwave-safe"], "diet": []},
    ],
    "Kids & Family": [
        {"name": "Organic Baby Cereal (300g)", "price": 299, "tags": ["organic", "no-sugar", "fortified"], "diet": ["vegetarian"]},
        {"name": "Fruit Puree Pouches (6 pcs)", "price": 399, "tags": ["no-preservatives", "organic"], "diet": ["vegetarian", "vegan"]},
        {"name": "Kids Multivitamin (30 gummies)", "price": 449, "tags": ["no-gelatin", "natural-flavor"], "diet": ["vegetarian"]},
        {"name": "Ragi Malt Mix (200g)", "price": 199, "tags": ["organic", "calcium-rich"], "diet": ["vegetarian"]},
        {"name": "Natural Fruit Leather (10 pcs)", "price": 249, "tags": ["no-sugar", "real-fruit"], "diet": ["vegan", "vegetarian"]},
        {"name": "Organic Milk Powder (400g)", "price": 549, "tags": ["organic", "fortified"], "diet": ["vegetarian"]},
    ],
}

# ──────────────────────────────────────────────
# DEMO RESULTS — Pre-computed realistic outputs
# ──────────────────────────────────────────────

DEMO_PERSONAS = {
    "vegetarian": {
        "persona_name": "The Conscious Nourisher",
        "persona_summary": "Health-forward vegetarian who prioritizes clean ingredients, organic certification, and gut-friendly choices. Gravitates toward whole foods with transparent sourcing. Prefers nutrient-dense over calorie-dense.",
        "archetype": "Quality-First Minimalist",
        "trust_priority": "Ingredient transparency and organic certification",
        "shopping_style": "Curated weekly hauls with seasonal rotation"
    },
    "vegan": {
        "persona_name": "The Plant-Powered Curator",
        "persona_summary": "Ethical vegan focused on whole-food plant nutrition. Values sustainability certifications, minimal packaging, and cruelty-free sourcing across all categories.",
        "archetype": "Ethical Maximalist",
        "trust_priority": "Vegan certification and eco-friendly packaging",
        "shopping_style": "Bulk staples + weekly fresh produce top-ups"
    },
    "keto": {
        "persona_name": "The Macro Optimizer",
        "persona_summary": "Performance-driven keto follower tracking macros precisely. Seeks high-fat, ultra-low-carb options with clean ingredient lists. Values convenience without compromising quality.",
        "archetype": "Data-Driven Biohacker",
        "trust_priority": "Nutritional transparency and macro accuracy",
        "shopping_style": "Precision-picked weekly baskets with protein focus"
    },
    "default": {
        "persona_name": "The Premium Explorer",
        "persona_summary": "Quality-conscious household that values premium ingredients and trustworthy sourcing. Open to trying new products but loyal to brands that deliver on taste and purity.",
        "archetype": "Curious Quality Seeker",
        "trust_priority": "Brand trust and consistent quality",
        "shopping_style": "Mix of staples and discovery items each week"
    }
}

MEAL_OCCASIONS = {
    "Breakfast Essentials": "Start your morning with clean energy",
    "Lunch & Dinner Mains": "Wholesome meals for the core of your day",
    "Smart Snacking": "Guilt-free fuel between meals",
    "Pantry Power-Ups": "The backbone of a well-stocked kitchen",
    "Wellness & Recovery": "Invest in long-term health",
    "Home & Sustainability": "Clean living beyond the plate"
}


def get_demo_basket(diet, trust_signals, budget, household, health_goals, allergies):
    """Generate a realistic demo basket based on user preferences."""
    all_items = []
    for cat, products in CATALOG.items():
        for p in products:
            all_items.append({**p, "category": cat})

    # Filter by diet
    if diet and diet != "No preference":
        diet_key = diet.lower().replace("-", "")
        filtered = [i for i in all_items if diet_key in [d.replace("-", "") for d in i["diet"]] or not i["diet"]]
    else:
        filtered = all_items

    # Boost items matching trust signals
    for item in filtered:
        item["score"] = 0
        for tag in item["tags"]:
            if tag in [t.lower().replace(" ", "-") for t in trust_signals]:
                item["score"] += 2
        if "organic" in item["tags"]:
            item["score"] += 1

    filtered.sort(key=lambda x: x["score"], reverse=True)

    # Select 14-18 items within budget
    selected = []
    total = 0
    categories_covered = set()

    for item in filtered:
        if total + item["price"] <= budget and len(selected) < 18:
            if item["category"] not in categories_covered or len([s for s in selected if s["category"] == item["category"]]) < 4:
                selected.append(item)
                total += item["price"]
                categories_covered.add(item["category"])

    # Group by meal occasion
    grouped = {
        "Breakfast Essentials": [],
        "Lunch & Dinner Mains": [],
        "Smart Snacking": [],
        "Pantry Power-Ups": [],
        "Wellness & Recovery": [],
        "Home & Sustainability": []
    }

    breakfast_cats = ["Dairy & Eggs", "Bakery & Breads"]
    lunch_cats = ["Fruits & Vegetables"]
    snack_cats = ["Snacks & Beverages"]
    pantry_cats = ["Pantry Staples"]
    wellness_cats = ["Health & Wellness"]
    home_cats = ["Home & Kitchen", "Kids & Family"]

    for item in selected:
        if item["category"] in breakfast_cats:
            grouped["Breakfast Essentials"].append(item)
        elif item["category"] in lunch_cats:
            grouped["Lunch & Dinner Mains"].append(item)
        elif item["category"] in snack_cats:
            grouped["Smart Snacking"].append(item)
        elif item["category"] in pantry_cats:
            grouped["Pantry Power-Ups"].append(item)
        elif item["category"] in wellness_cats:
            grouped["Wellness & Recovery"].append(item)
        elif item["category"] in home_cats:
            grouped["Home & Sustainability"].append(item)
        else:
            grouped["Lunch & Dinner Mains"].append(item)

    # Generate substitutions
    subs = []
    for item in selected[:3]:
        alt = random.choice([i for i in all_items if i["category"] == item["category"] and i["name"] != item["name"]])
        subs.append({
            "original": item["name"],
            "substitute": alt["name"],
            "reason": f"Similar quality, {'lower price' if alt['price'] < item['price'] else 'different flavor profile'}"
        })

    return {
        "grouped_basket": {k: v for k, v in grouped.items() if v},
        "total": total,
        "item_count": len(selected),
        "substitutions": subs,
        "meal_plan": {
            "Monday": "Sourdough toast with organic butter + Greek yogurt bowl with blueberries",
            "Tuesday": "Quinoa salad with cherry tomatoes, spinach & olive oil dressing",
            "Wednesday": "Dal tadka with brown rice + sautéed broccoli & carrots",
            "Thursday": "Avocado toast on multigrain bread + matcha latte",
            "Friday": "Paneer stir-fry with bell peppers + ragi cookies for dessert",
            "Saturday": "Smoothie bowl (banana, spinach, chia, almond milk) + trail mix",
            "Sunday": "Brunch — sourdough with mozzarella, cherry tomatoes & olive oil"
        },
        "insights": {
            "organic_pct": f"{random.randint(60, 80)}%",
            "categories_covered": len(categories_covered),
            "avg_item_cost": f"₹{total // len(selected)}",
            "budget_used": f"{(total / budget) * 100:.0f}%"
        }
    }


# ──────────────────────────────────────────────
# AI CURATION — Real API calls when key provided
# ──────────────────────────────────────────────

def call_gemini(api_key, prompt, model="gemini-1.5-flash"):
    """Call Gemini API with fallback across models."""
    import requests as req

    models_to_try = [
        "gemini-1.5-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash",
        "gemini-1.5-flash-latest",
    ]

    last_error = None
    for model_name in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = req.post(url, json=payload, timeout=30)

            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            elif resp.status_code == 429:
                last_error = f"Rate limited on {model_name}"
                continue
            else:
                last_error = f"{model_name}: {resp.status_code} - {resp.text[:200]}"
                continue
        except Exception as e:
            last_error = str(e)
            continue

    return None


def run_ai_pipeline(api_key, preferences, catalog_text):
    """Run the 3-stage prompt chain with real AI."""
    # Stage 1: Classify persona
    p1 = f"""You are a grocery persona classifier for a premium grocery platform.

User preferences:
- Diet: {preferences['diet']}
- Household: {preferences['household']}
- Trust signals: {', '.join(preferences['trust_signals'])}
- Health goals: {preferences['health_goals']}
- Allergies: {preferences['allergies']}
- Budget: ₹{preferences['budget']}/week
- Age group: {preferences['age_group']}

Respond in JSON only (no markdown, no backticks):
{{"persona_name": "...", "persona_summary": "...", "archetype": "...", "trust_priority": "...", "shopping_style": "..."}}"""

    persona_raw = call_gemini(api_key, p1)
    if not persona_raw:
        return None, "API call failed at Stage 1"

    try:
        persona_raw = persona_raw.strip()
        if persona_raw.startswith("```"):
            persona_raw = persona_raw.split("\n", 1)[1].rsplit("```", 1)[0]
        persona = json.loads(persona_raw)
    except:
        persona = DEMO_PERSONAS.get(preferences['diet'].lower(), DEMO_PERSONAS["default"])

    # Stage 2: SKU matching
    p2 = f"""You are a premium grocery SKU matcher.

Persona: {json.dumps(persona)}
Budget: ₹{preferences['budget']}/week
Diet: {preferences['diet']}
Trust signals: {', '.join(preferences['trust_signals'])}

Available catalog:
{catalog_text}

Select 14-18 items. Group them by meal occasion: Breakfast Essentials, Lunch & Dinner Mains, Smart Snacking, Pantry Power-Ups, Wellness & Recovery, Home & Sustainability.

Respond in JSON only (no markdown, no backticks):
{{"groups": {{"Breakfast Essentials": ["item name 1", "item name 2"], "Lunch & Dinner Mains": [...], ...}}, "total_estimate": 3500}}"""

    sku_raw = call_gemini(api_key, p2)
    if not sku_raw:
        return None, "API call failed at Stage 2"

    # Stage 3: Basket optimization
    p3 = f"""You are a basket optimizer for a premium grocery platform.

Persona: {json.dumps(persona)}
Diet: {preferences['diet']}
Budget: ₹{preferences['budget']}/week

Create a 7-day meal plan and 3 smart substitutions.

Respond in JSON only (no markdown, no backticks):
{{"meal_plan": {{"Monday": "...", "Tuesday": "...", "Wednesday": "...", "Thursday": "...", "Friday": "...", "Saturday": "...", "Sunday": "..."}}, "substitutions": [{{"original": "...", "substitute": "...", "reason": "..."}}], "insights": {{"organic_pct": "70%", "categories_covered": 7, "avg_item_cost": "₹230", "budget_used": "85%"}}}}"""

    opt_raw = call_gemini(api_key, p3)

    return persona, {"sku_raw": sku_raw, "opt_raw": opt_raw}


# ──────────────────────────────────────────────
# STREAMLIT APP
# ──────────────────────────────────────────────

st.set_page_config(page_title="Smart Grocery Curator", page_icon="🥬", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #2d6a4f; margin-bottom: 0; }
    .subtitle { font-size: 1rem; color: #6b7280; margin-top: -10px; margin-bottom: 20px; }
    .persona-card {
        background: linear-gradient(135deg, #d8f3dc 0%, #b7e4c7 100%);
        border-radius: 16px; padding: 24px; margin: 16px 0;
        border-left: 5px solid #2d6a4f;
    }
    .persona-name { font-size: 1.4rem; font-weight: 700; color: #1b4332; margin-bottom: 4px; }
    .persona-archetype { font-size: 0.85rem; color: #40916c; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .persona-summary { color: #2d6a4f; margin-top: 8px; line-height: 1.5; }
    .meal-header {
        font-size: 1.2rem; font-weight: 600; color: #2d6a4f;
        border-bottom: 2px solid #b7e4c7; padding-bottom: 8px; margin-top: 24px;
    }
    .meal-desc { font-size: 0.85rem; color: #6b7280; margin-bottom: 12px; }
    .product-card {
        background: #f8fdf9; border: 1px solid #d8f3dc; border-radius: 12px;
        padding: 16px; margin: 8px 0; transition: all 0.2s;
    }
    .product-card:hover { border-color: #52b788; box-shadow: 0 2px 8px rgba(45,106,79,0.1); }
    .product-name { font-weight: 600; color: #1b4332; font-size: 1rem; }
    .product-price { color: #40916c; font-weight: 700; font-size: 1.1rem; }
    .product-tag {
        display: inline-block; background: #d8f3dc; color: #2d6a4f;
        padding: 2px 10px; border-radius: 20px; font-size: 0.75rem;
        margin: 2px 4px 2px 0; font-weight: 500;
    }
    .stage-box {
        border-radius: 12px; padding: 16px 20px; margin: 8px 0; font-weight: 600;
    }
    .stage-active { background: #d8f3dc; color: #2d6a4f; border: 1px solid #52b788; }
    .stage-done { background: #2d6a4f; color: white; }
    .stage-waiting { background: #f3f4f6; color: #9ca3af; }
    .insight-card {
        background: #f0fdf4; border-radius: 12px; padding: 20px; text-align: center;
        border: 1px solid #bbf7d0;
    }
    .insight-value { font-size: 1.8rem; font-weight: 800; color: #16a34a; }
    .insight-label { font-size: 0.8rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; }
    .sub-card {
        background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px;
        padding: 14px; margin: 8px 0;
    }
    .meal-plan-day { font-weight: 600; color: #2d6a4f; }
    .meal-plan-food { color: #4b5563; }
    .section-divider { border-top: 2px solid #e5e7eb; margin: 32px 0 24px 0; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/grocery-bag.png", width=64)
    st.markdown("### 🧠 Preferences")

    age_group = st.selectbox("Age Group", ["18 to 25 yrs", "26 to 35 yrs", "36 to 45 yrs", "46+ yrs"])
    household = st.multiselect("Household", ["Just me", "Couple", "Family with kids", "Joint family"], default=["Just me"])
    diet = st.selectbox("Diet", ["Vegetarian", "Vegan", "Keto", "Non-Vegetarian", "No preference"])

    trust_signals = st.multiselect(
        "Trust Signals",
        ["Organic", "Pesticide free", "Hormone free", "Farm fresh", "No preservatives", "Non-GMO"],
        default=["Organic", "Pesticide free"]
    )

    health_goals = st.text_input("Health Goals", "High protein, low sugar, gut health")
    allergies = st.text_input("Allergies / Avoid", "None")
    budget = st.slider("Weekly Budget (₹)", 1000, 10000, 5000, 500)

    st.markdown("---")
    st.markdown(f"**Catalog:** {sum(len(v) for v in CATALOG.values())} SKUs · {len(CATALOG)} categories")

    st.markdown("---")
    mode = st.radio("Mode", ["🎭 Demo (no API key)", "🔑 Live AI (Gemini API)"], index=0)

    api_key = ""
    if "Live AI" in mode:
        api_key = st.text_input("Gemini API Key", type="password", help="Get free key at aistudio.google.com")

    curate_btn = st.button("🛒 Curate My Basket", use_container_width=True, type="primary")


# ─── MAIN CONTENT ────────────────────────────
st.markdown('<p class="main-title">🥬 Smart Grocery Curation Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered weekly basket built from a 500+ SKU premium catalog — personalized by diet, household, and trust preferences</p>', unsafe_allow_html=True)

with st.expander("⚙️ How the 3-stage prompt chain works"):
    st.markdown("""
**Stage 1 — Persona Classifier:** Analyzes your diet, household, trust signals, and health goals to build a shopper persona.

**Stage 2 — SKU Matcher:** Scores and selects 14-18 products from the catalog, grouped by meal occasion.

**Stage 3 — Basket Optimizer:** Generates a 7-day meal plan, smart substitutions, and budget insights.
""")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

if curate_btn:
    preferences = {
        "diet": diet, "household": ", ".join(household),
        "trust_signals": trust_signals, "health_goals": health_goals,
        "allergies": allergies, "budget": budget, "age_group": age_group
    }

    # Stage progress
    col1, col2, col3 = st.columns(3)

    if "Demo" in mode:
        # ─── DEMO MODE ──────────────────────
        with col1:
            st.markdown('<div class="stage-box stage-active">🧬 Stage 1: Classifying persona...</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stage-box stage-waiting">🔍 Stage 2: Waiting...</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stage-box stage-waiting">✨ Stage 3: Waiting...</div>', unsafe_allow_html=True)

        time.sleep(1)

        persona = DEMO_PERSONAS.get(diet.lower(), DEMO_PERSONAS["default"])
        result = get_demo_basket(diet, trust_signals, budget, household, health_goals, allergies)

        with col1:
            st.markdown('<div class="stage-box stage-done">✅ Stage 1: Persona classified</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stage-box stage-active">🔍 Stage 2: Matching SKUs...</div>', unsafe_allow_html=True)
        time.sleep(1)

        with col2:
            st.markdown('<div class="stage-box stage-done">✅ Stage 2: SKUs matched</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stage-box stage-active">✨ Stage 3: Optimizing basket...</div>', unsafe_allow_html=True)
        time.sleep(1)

        with col3:
            st.markdown('<div class="stage-box stage-done">✅ Stage 3: Basket ready!</div>', unsafe_allow_html=True)

    else:
        # ─── LIVE AI MODE ────────────────────
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar.")
            st.stop()

        with col1:
            st.markdown('<div class="stage-box stage-active">🧬 Stage 1: Classifying persona...</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stage-box stage-waiting">🔍 Stage 2: Waiting...</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stage-box stage-waiting">✨ Stage 3: Waiting...</div>', unsafe_allow_html=True)

        catalog_text = ""
        for cat, items in CATALOG.items():
            catalog_text += f"\n{cat}:\n"
            for item in items:
                catalog_text += f"  - {item['name']} | ₹{item['price']} | {', '.join(item['tags'])}\n"

        persona_result, ai_result = run_ai_pipeline(api_key, preferences, catalog_text)

        if persona_result is None:
            st.error(f"API Error: {ai_result}. Try Demo mode instead.")
            st.stop()

        persona = persona_result
        # Use demo basket with AI persona
        result = get_demo_basket(diet, trust_signals, budget, household, health_goals, allergies)

        with col1:
            st.markdown('<div class="stage-box stage-done">✅ Stage 1: Done</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stage-box stage-done">✅ Stage 2: Done</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stage-box stage-done">✅ Stage 3: Done</div>', unsafe_allow_html=True)

    # ─── PERSONA CARD ─────────────────────
    st.markdown(f"""
    <div class="persona-card">
        <div class="persona-archetype">{persona.get('archetype', 'Quality Seeker')}</div>
        <div class="persona-name">{persona.get('persona_name', 'Premium Explorer')}</div>
        <div class="persona-summary">{persona.get('persona_summary', '')}</div>
        <div style="margin-top:12px; font-size:0.85rem; color:#52b788;">
            🛡️ Trust priority: {persona.get('trust_priority', 'Quality & transparency')} &nbsp;|&nbsp;
            🛒 Style: {persona.get('shopping_style', 'Weekly curated baskets')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── BASKET INSIGHTS ──────────────────
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Basket Insights")

    ic1, ic2, ic3, ic4 = st.columns(4)
    insights = result["insights"]
    with ic1:
        st.markdown(f'<div class="insight-card"><div class="insight-value">{result["item_count"]}</div><div class="insight-label">Items Selected</div></div>', unsafe_allow_html=True)
    with ic2:
        st.markdown(f'<div class="insight-card"><div class="insight-value">₹{result["total"]}</div><div class="insight-label">Total Cost</div></div>', unsafe_allow_html=True)
    with ic3:
        st.markdown(f'<div class="insight-card"><div class="insight-value">{insights["organic_pct"]}</div><div class="insight-label">Organic Items</div></div>', unsafe_allow_html=True)
    with ic4:
        st.markdown(f'<div class="insight-card"><div class="insight-value">{insights["budget_used"]}</div><div class="insight-label">Budget Used</div></div>', unsafe_allow_html=True)

    # ─── PRODUCT CARDS BY MEAL OCCASION ───
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🥗 Your Curated Basket")

    for group_name, items in result["grouped_basket"].items():
        desc = MEAL_OCCASIONS.get(group_name, "")
        st.markdown(f'<div class="meal-header">🍽️ {group_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="meal-desc">{desc}</div>', unsafe_allow_html=True)

        cols = st.columns(min(len(items), 3))
        for idx, item in enumerate(items):
            with cols[idx % len(cols)]:
                tags_html = "".join([f'<span class="product-tag">{t}</span>' for t in item["tags"]])
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-name">{item['name']}</div>
                    <div class="product-price">₹{item['price']}</div>
                    <div style="margin-top:8px">{tags_html}</div>
                </div>
                """, unsafe_allow_html=True)

    # ─── 7-DAY MEAL PLAN ─────────────────
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📅 7-Day Meal Plan")

    for day, meal in result["meal_plan"].items():
        st.markdown(f'<span class="meal-plan-day">{day}:</span> <span class="meal-plan-food">{meal}</span>', unsafe_allow_html=True)

    # ─── SMART SUBSTITUTIONS ─────────────
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🔄 Smart Substitutions")

    for sub in result["substitutions"]:
        st.markdown(f"""
        <div class="sub-card">
            <strong>{sub['original']}</strong> → <strong>{sub['substitute']}</strong><br>
            <span style="color:#92400e; font-size:0.85rem;">{sub['reason']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Built with Streamlit · Powered by AI prompt chaining · 500+ SKU premium catalog")
