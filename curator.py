"""
Smart Grocery Curation Engine — Gemini API Prompt Chain
3-stage pipeline: Classifier → SKU Matcher → Basket Optimizer
"""

import google.generativeai as genai
import json
from catalog import get_catalog_json


def call_gemini(api_key: str, prompt: str, max_tokens: int = 2000) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text.strip()


def clean_json(raw: str) -> dict:
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def run_classifier(api_key: str, user_profile: dict) -> dict:
    prompt = f"""You are a grocery intelligence engine for a premium quality-first platform.

Given this user profile:
- Name: {user_profile.get('name', 'User')}
- Household: {user_profile.get('household', 'Just me')}
- Age group: {user_profile.get('age_group', '26-35')}
- Diet: {', '.join(user_profile.get('diet', ['Vegetarian']))}
- Trust signals: {', '.join(user_profile.get('trust_signals', ['Organic']))}
- Weekly budget: Rs.{user_profile.get('budget', 1500)}
- Health goals: {user_profile.get('health_goals', 'General wellness')}
- Allergies/Avoid: {user_profile.get('allergies', 'None')}

Classify this user. Output ONLY valid JSON, no markdown, no explanation:
{{
  "persona_type": "string",
  "persona_description": "2-sentence description",
  "key_priorities": ["priority1", "priority2", "priority3"],
  "must_have_labels": ["label1", "label2"],
  "avoid_ingredients": ["item1"],
  "weekly_meal_pattern": "brief description",
  "curation_tone": "string"
}}"""

    raw = call_gemini(api_key, prompt)
    return clean_json(raw)


def run_sku_matcher(api_key: str, user_profile: dict, persona: dict) -> dict:
    catalog_json = get_catalog_json()
    budget = user_profile.get('budget', 1500)

    prompt = f"""You are a premium grocery curator selecting products.

Customer Persona: {json.dumps(persona)}
Diet: {', '.join(user_profile.get('diet', ['Vegetarian']))}
Trust requirements: {', '.join(user_profile.get('trust_signals', ['Organic']))}
Weekly budget: Rs.{budget}
Household: {user_profile.get('household', 'Just me')}
Health goals: {user_profile.get('health_goals', 'General wellness')}
Allergies: {user_profile.get('allergies', 'None')}

Available catalog:
{catalog_json}

Select 12-16 products. Stay within Rs.{budget}. Respect diet restrictions strictly.
Output ONLY valid JSON, no markdown:
{{
  "selected_skus": [
    {{
      "id": "product_id",
      "name": "product_name",
      "category": "category",
      "price": 0,
      "unit": "unit",
      "reason": "1 sentence why this product for this person"
    }}
  ],
  "total_estimated_cost": 0,
  "coverage_summary": "2-3 sentences on what this covers"
}}"""

    raw = call_gemini(api_key, prompt, max_tokens=3000)
    return clean_json(raw)


def run_basket_optimizer(api_key: str, user_profile: dict, persona: dict, matched_skus: dict) -> dict:
    selected = matched_skus.get('selected_skus', [])
    budget = user_profile.get('budget', 1500)

    prompt = f"""You are finalizing a personalized weekly grocery basket.

Customer: {user_profile.get('name', 'User')} | {user_profile.get('household', 'Just me')}
Persona: {persona.get('persona_type', '')}
Diet: {', '.join(user_profile.get('diet', []))}
Health goals: {user_profile.get('health_goals', '')}
Budget: Rs.{budget}

Selected products: {json.dumps(selected)}

Create the final optimized basket. Output ONLY valid JSON, no markdown:
{{
  "final_basket": [
    {{
      "id": "product_id",
      "name": "product_name",
      "category": "category",
      "price": 0,
      "unit": "unit",
      "occasion": "Breakfast/Lunch/Dinner/Snack/Pantry/Health",
      "curator_note": "why this product or null",
      "quality_highlight": "key quality attribute"
    }}
  ],
  "basket_total": 0,
  "meal_plan_summary": {{
    "breakfast": "what is covered",
    "lunch": "what is covered",
    "dinner": "what is covered",
    "snacks": "snack options",
    "health_stack": "supplements/health items"
  }},
  "smart_substitutions": [
    {{
      "original": "product name",
      "substitute": "cheaper option",
      "saving": 0,
      "trade_off": "what you give up"
    }}
  ],
  "basket_insights": {{
    "clean_label_score": "X of Y products meet your trust criteria",
    "time_saved_minutes": 20,
    "quality_vs_generic_saving": "explanation",
    "weekly_nutrition_highlight": "key nutrition insight"
  }},
  "curator_personal_note": "2-3 sentence personal note to this customer"
}}"""

    raw = call_gemini(api_key, prompt, max_tokens=4000)
    return clean_json(raw)


def generate_basket(api_key: str, user_profile: dict) -> dict:
    results = {
        "user_profile": user_profile,
        "stage_1_persona": None,
        "stage_2_matched": None,
        "stage_3_final": None,
        "error": None
    }

    try:
        results["stage_1_persona"] = run_classifier(api_key, user_profile)
        results["stage_2_matched"] = run_sku_matcher(api_key, user_profile, results["stage_1_persona"])
        results["stage_3_final"] = run_basket_optimizer(api_key, user_profile, results["stage_1_persona"], results["stage_2_matched"])
    except json.JSONDecodeError as e:
        results["error"] = f"JSON parsing error: {str(e)}"
    except Exception as e:
        results["error"] = f"Error: {str(e)}"

    return results
