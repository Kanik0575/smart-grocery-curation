"""
Smart Grocery Curation Engine — Claude API Prompt Chain
========================================================
3-stage pipeline:
  Stage 1: Classifier   → Understand user persona and needs
  Stage 2: SKU Matcher  → Select relevant products from catalog
  Stage 3: Basket Optimizer → Build final weekly basket with reasoning

Author: Kanik Kumar | CS '27, BITS Pilani
"""

import anthropic
import json
from catalog import get_catalog_json


def run_classifier(client: anthropic.Anthropic, user_profile: dict) -> dict:
    """
    Stage 1: Classify user into a grocery persona.
    Outputs: persona_type, key_priorities, avoid_list, budget_tier, household_size_est
    """
    prompt = f"""You are a grocery intelligence engine for a premium quality-first platform.

Given this user profile:
- Name: {user_profile.get('name', 'User')}
- Household: {user_profile.get('household', 'Just me')}
- Age group: {user_profile.get('age_group', '26-35')}
- Diet: {', '.join(user_profile.get('diet', ['Vegetarian']))}
- Trust signals: {', '.join(user_profile.get('trust_signals', ['Organic']))}
- Weekly budget: ₹{user_profile.get('budget', 1500)}
- Health goals: {user_profile.get('health_goals', 'General wellness')}
- Allergies/Avoid: {user_profile.get('allergies', 'None')}

Classify this user and output ONLY valid JSON (no markdown, no preamble):
{{
  "persona_type": "string (e.g. Health-Conscious Family, Active Professional, Vegan Explorer, etc.)",
  "persona_description": "2-sentence description of this person's grocery mindset",
  "key_priorities": ["list of 3-5 priorities in order"],
  "must_have_labels": ["list of label requirements from their trust signals"],
  "avoid_ingredients": ["list of ingredients/labels to avoid"],
  "budget_allocation": {{
    "fresh_produce_pct": number,
    "dairy_pct": number,
    "staples_pct": number,
    "snacks_health_pct": number,
    "other_pct": number
  }},
  "weekly_meal_pattern": "brief description of their likely meal patterns",
  "curation_tone": "string (e.g. discovery-led, efficiency-focused, health-obsessed)"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = response.content[0].text.strip()
    # Clean JSON if needed
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def run_sku_matcher(client: anthropic.Anthropic, user_profile: dict, persona: dict) -> dict:
    """
    Stage 2: Match relevant SKUs from the catalog.
    Outputs: selected SKUs with reasoning for each category
    """
    catalog_json = get_catalog_json()
    budget = user_profile.get('budget', 1500)
    
    prompt = f"""You are a premium grocery curator selecting products for a customer.

Customer Persona:
{json.dumps(persona, indent=2)}

Customer Profile:
- Diet: {', '.join(user_profile.get('diet', ['Vegetarian']))}
- Trust requirements: {', '.join(user_profile.get('trust_signals', ['Organic']))}
- Weekly budget: ₹{budget}
- Household: {user_profile.get('household', 'Just me')}
- Health goals: {user_profile.get('health_goals', 'General wellness')}
- Allergies/Avoid: {user_profile.get('allergies', 'None')}

Available Product Catalog (select from ONLY these products):
{catalog_json}

RULES:
- Select 12-18 products total
- Stay within ₹{budget} total budget
- Respect diet restrictions strictly (vegetarian = no meat/fish; vegan = no dairy/eggs)
- Prioritize products whose labels match the customer's trust signals
- Choose variety across categories
- Pick products that work together as a weekly basket

Output ONLY valid JSON (no markdown):
{{
  "selected_skus": [
    {{
      "id": "product_id",
      "name": "product_name",
      "category": "category",
      "price": number,
      "unit": "unit",
      "reason": "1 sentence why this specific product for this specific person"
    }}
  ],
  "total_estimated_cost": number,
  "coverage_summary": "2-3 sentences on what meals/needs this covers"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def run_basket_optimizer(client: anthropic.Anthropic, user_profile: dict, persona: dict, matched_skus: dict) -> dict:
    """
    Stage 3: Optimize the basket with meal planning, substitutions, and insights.
    Outputs: final basket, meal plan, substitutions, savings insights
    """
    selected = matched_skus.get('selected_skus', [])
    budget = user_profile.get('budget', 1500)
    
    prompt = f"""You are finalizing a personalized weekly grocery basket for a premium household.

Customer: {user_profile.get('name', 'User')} | {user_profile.get('household', 'Just me')}
Persona: {persona.get('persona_type', '')} — {persona.get('persona_description', '')}
Diet: {', '.join(user_profile.get('diet', []))}
Health goals: {user_profile.get('health_goals', 'General wellness')}
Budget: ₹{budget}/week

Selected Products:
{json.dumps(selected, indent=2)}

Total estimated cost: ₹{matched_skus.get('total_estimated_cost', 0)}

Now create the FINAL basket with:
1. Group products into meal/usage occasions
2. Add a "curator's note" for any premium/unfamiliar item (max 1 sentence)
3. Suggest 1-2 smart substitutions if over budget
4. Calculate time-to-checkout reduction vs. manually building a basket
5. Write a personal note from the curator

Output ONLY valid JSON (no markdown):
{{
  "final_basket": [
    {{
      "id": "product_id",
      "name": "product_name", 
      "category": "category",
      "subcategory": "subcategory",
      "price": number,
      "unit": "unit",
      "occasion": "Breakfast / Lunch / Dinner / Snack / Pantry / Health",
      "curator_note": "why this product specifically (or null if obvious)",
      "quality_highlight": "the 1 quality attribute that makes this a FirstClub pick"
    }}
  ],
  "basket_total": number,
  "meal_plan_summary": {{
    "breakfast": "what's covered for breakfast",
    "lunch": "what's covered for lunch", 
    "dinner": "what's covered for dinner",
    "snacks": "snack options available",
    "health_stack": "supplements/health items"
  }},
  "smart_substitutions": [
    {{
      "original": "product name",
      "substitute": "cheaper/equivalent option",
      "saving": number,
      "trade_off": "what you give up"
    }}
  ],
  "basket_insights": {{
    "clean_label_score": "X out of {len(selected)} products meet your trust criteria",
    "time_saved_minutes": number,
    "quality_vs_generic_saving": "explanation of value vs. buying same at Blinkit",
    "weekly_nutrition_highlight": "1 key nutrition insight from this basket"
  }},
  "curator_personal_note": "2-3 sentence personal note from the curator to this specific customer about their basket"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def generate_basket(api_key: str, user_profile: dict) -> dict:
    """
    Main entry point. Runs the full 3-stage prompt chain.
    Returns complete basket with all metadata.
    """
    client = anthropic.Anthropic(api_key=api_key)
    
    results = {
        "user_profile": user_profile,
        "stage_1_persona": None,
        "stage_2_matched": None,
        "stage_3_final": None,
        "error": None
    }
    
    try:
        # Stage 1: Classify
        results["stage_1_persona"] = run_classifier(client, user_profile)
        
        # Stage 2: Match SKUs
        results["stage_2_matched"] = run_sku_matcher(
            client, user_profile, results["stage_1_persona"]
        )
        
        # Stage 3: Optimize basket
        results["stage_3_final"] = run_basket_optimizer(
            client, user_profile, 
            results["stage_1_persona"], 
            results["stage_2_matched"]
        )
        
    except json.JSONDecodeError as e:
        results["error"] = f"JSON parsing error: {str(e)}"
    except anthropic.APIError as e:
        results["error"] = f"API error: {str(e)}"
    except Exception as e:
        results["error"] = f"Unexpected error: {str(e)}"
    
    return results


if __name__ == "__main__":
    import os
    
    test_profile = {
        "name": "Priya",
        "household": "Spouse + Kids",
        "age_group": "36-45",
        "diet": ["Vegetarian"],
        "trust_signals": ["Organic", "Pesticide free", "No artificial additives"],
        "budget": 2000,
        "health_goals": "High protein for kids, low sugar family meals",
        "allergies": "None"
    }
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        result = generate_basket(api_key, test_profile)
        print(json.dumps(result["stage_1_persona"], indent=2))
    else:
        print("Set ANTHROPIC_API_KEY to test")
