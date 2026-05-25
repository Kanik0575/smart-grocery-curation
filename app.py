"""
Smart Grocery Curation Engine — Single File Version
Everything in one file: catalog + API + UI
"""

import streamlit as st
import requests
import json

# ─── Page Config ──────────────────────────────────────────────
st.set_page_config(page_title="Smart Grocery Curator", page_icon="🌿", layout="wide")

# ─── Styling ──────────────────────────────────────────────────
st.markdown("""
<style>
.main-title { font-size: 2rem; font-weight: 700; color: #1a3c2a; }
.persona-card { background: linear-gradient(135deg, #1a3c2a, #2e7d32); color: white; padding: 1.5rem; border-radius: 16px; margin: 1rem 0; }
.product-card { background: #fafaf8; border: 1px solid #e8e8e4; border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem; border-left: 3px solid #2e7d32; }
.product-name { font-weight: 600; color: #1a3c2a; }
.product-price { font-weight: 700; color: #2e7d32; font-size: 1rem; }
.curator-note { font-size: 0.8rem; color: #555; font-style: italic; margin-top: 0.3rem; }
.insight-card { background: #fffde7; border: 1px solid #f9a825; border-radius: 10px; padding: 1rem; margin-bottom: 0.8rem; font-size: 0.9rem; }
.total-card { background: #1a3c2a; color: white; padding: 1.2rem 1.5rem; border-radius: 12px; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── Embedded Catalog ─────────────────────────────────────────
CATALOG = [
    {"id":"FV001","name":"Alphonso Mangoes","brand":"Farm Direct","category":"Fruits & Vegetables","price":299,"unit":"1 dozen","labels":["pesticide-free","farm-direct"]},
    {"id":"FV002","name":"Organic Tomatoes","brand":"Member's Pick","category":"Fruits & Vegetables","price":49,"unit":"500g","labels":["organic","pesticide-free"]},
    {"id":"FV003","name":"Baby Spinach","brand":"Green Farms","category":"Fruits & Vegetables","price":55,"unit":"200g","labels":["organic","pesticide-free"]},
    {"id":"FV004","name":"Avocados","brand":"Exotic Harvest","category":"Fruits & Vegetables","price":149,"unit":"2 pcs","labels":["pesticide-free"]},
    {"id":"FV005","name":"Yellow Lemons","brand":"Member's Pick","category":"Fruits & Vegetables","price":45,"unit":"500g","labels":["pesticide-free","farm-direct"]},
    {"id":"FV006","name":"Red Bell Peppers","brand":"Green Farms","category":"Fruits & Vegetables","price":89,"unit":"3 pcs","labels":["organic","pesticide-free"]},
    {"id":"FV007","name":"Organic Bananas","brand":"Farm Direct","category":"Fruits & Vegetables","price":65,"unit":"6 pcs","labels":["organic","pesticide-free"]},
    {"id":"FV008","name":"Broccoli","brand":"Green Farms","category":"Fruits & Vegetables","price":69,"unit":"500g","labels":["pesticide-free"]},
    {"id":"FV009","name":"Pomegranate","brand":"Farm Direct","category":"Fruits & Vegetables","price":89,"unit":"1 pc","labels":["pesticide-free","farm-direct"]},
    {"id":"FV010","name":"Sweet Potato","brand":"Farm Direct","category":"Fruits & Vegetables","price":59,"unit":"500g","labels":["organic","pesticide-free"]},
    {"id":"DE001","name":"Akshayakalpa A2 Organic Milk","brand":"Akshayakalpa","category":"Dairy & Eggs","price":45,"unit":"500ml","labels":["organic","hormone-free","no-artificial-additives","A2"]},
    {"id":"DE002","name":"High Protein Organic Paneer","brand":"Akshayakalpa","category":"Dairy & Eggs","price":89,"unit":"200g","labels":["organic","hormone-free","high-protein"]},
    {"id":"DE003","name":"Greek Yogurt Strawberry","brand":"Epigamia","category":"Dairy & Eggs","price":65,"unit":"90g","labels":["no-artificial-additives","high-protein","no-added-sugar"]},
    {"id":"DE004","name":"Free-Range Brown Eggs","brand":"Country Delight","category":"Dairy & Eggs","price":99,"unit":"6 pcs","labels":["hormone-free","cage-free"]},
    {"id":"DE005","name":"Organic Curd","brand":"Akshayakalpa","category":"Dairy & Eggs","price":55,"unit":"400g","labels":["organic","hormone-free","probiotic"]},
    {"id":"DE006","name":"Mozzarella Cheese","brand":"Vallombrosa","category":"Dairy & Eggs","price":288,"unit":"250g","labels":["no-artificial-additives","no-preservatives"]},
    {"id":"DE007","name":"A2 Desi Ghee","brand":"Akshayakalpa","category":"Dairy & Eggs","price":649,"unit":"500ml","labels":["organic","hormone-free","A2"]},
    {"id":"DE008","name":"Almond Milk Unsweetened","brand":"137 Degrees","category":"Dairy & Eggs","price":429,"unit":"1L","labels":["vegan","no-artificial-additives","no-added-sugar"]},
    {"id":"DE009","name":"Skyr Icelandic Yogurt","brand":"MilkyMist","category":"Dairy & Eggs","price":79,"unit":"100g","labels":["high-protein","no-artificial-additives"]},
    {"id":"DE010","name":"Chickpea Tofu","brand":"Health on Plants","category":"Dairy & Eggs","price":175,"unit":"200g","labels":["vegan","high-protein","gluten-free"]},
    {"id":"BB001","name":"Zero Maida Protein Bread","brand":"The Health Factory","category":"Breads & Bakery","price":85,"unit":"250g","labels":["high-protein","no-artificial-additives","no-maida"]},
    {"id":"BB002","name":"Member's Pick Whole Wheat Bread","brand":"Member's Pick","category":"Breads & Bakery","price":59,"unit":"270g","labels":["no-artificial-additives","no-preservatives","whole-grain"]},
    {"id":"BB003","name":"Sourdough Loaf","brand":"Artisan Bakes","category":"Breads & Bakery","price":189,"unit":"400g","labels":["no-artificial-additives","no-preservatives","naturally-fermented"]},
    {"id":"BB004","name":"Multigrain Sandwich Bread","brand":"Bonn","category":"Breads & Bakery","price":65,"unit":"400g","labels":["whole-grain","no-artificial-additives"]},
    {"id":"BB005","name":"Ragi Millet Bread","brand":"Slurrp Farm","category":"Breads & Bakery","price":79,"unit":"250g","labels":["gluten-free","no-artificial-additives"]},
    {"id":"ST001","name":"Cold-Pressed Coconut Oil","brand":"KLF Nirmal","category":"Staples","price":349,"unit":"500ml","labels":["cold-pressed","no-artificial-additives","palm-oil-free"]},
    {"id":"ST002","name":"Residue-Free Toor Dal","brand":"Member's Pick","category":"Staples","price":189,"unit":"1kg","labels":["pesticide-free","residue-tested"]},
    {"id":"ST003","name":"Stone-Ground Whole Wheat Flour","brand":"Aashirvaad","category":"Staples","price":99,"unit":"1kg","labels":["whole-grain","no-artificial-additives","stone-ground"]},
    {"id":"ST004","name":"Raw Honey","brand":"Two Brothers","category":"Staples","price":499,"unit":"500g","labels":["raw","no-artificial-additives","no-added-sugar"]},
    {"id":"ST005","name":"Organic Red Rice","brand":"Conscious Food","category":"Staples","price":199,"unit":"1kg","labels":["organic","pesticide-free"]},
    {"id":"ST006","name":"Quinoa","brand":"True Elements","category":"Staples","price":349,"unit":"500g","labels":["gluten-free","high-protein","no-artificial-additives"]},
    {"id":"ST007","name":"Almond Butter","brand":"The Butternut Co.","category":"Staples","price":499,"unit":"200g","labels":["no-artificial-additives","no-added-sugar","high-protein"]},
    {"id":"ST008","name":"Organic Moong Dal","brand":"Member's Pick","category":"Staples","price":149,"unit":"500g","labels":["organic","pesticide-free"]},
    {"id":"ST009","name":"Apple Cider Vinegar","brand":"Bragg","category":"Staples","price":399,"unit":"473ml","labels":["organic","no-artificial-additives","raw"]},
    {"id":"ST010","name":"Cold-Pressed Groundnut Oil","brand":"Conscious Food","category":"Staples","price":299,"unit":"1L","labels":["cold-pressed","no-artificial-additives"]},
    {"id":"SB001","name":"Dark Chocolate 70%","brand":"Manam","category":"Snacks & Beverages","price":199,"unit":"55g","labels":["no-artificial-additives","no-added-sugar","vegan"]},
    {"id":"SB002","name":"Madras Mixture","brand":"Kaara Puram","category":"Snacks & Beverages","price":149,"unit":"250g","labels":["no-artificial-additives","no-preservatives","palm-oil-free"]},
    {"id":"SB003","name":"Cold Brew Coffee","brand":"Blue Tokai","category":"Snacks & Beverages","price":199,"unit":"250ml","labels":["no-artificial-additives","no-added-sugar"]},
    {"id":"SB004","name":"Kombucha Ginger Lemon","brand":"Bhu","category":"Snacks & Beverages","price":149,"unit":"250ml","labels":["probiotic","no-artificial-additives","no-added-sugar"]},
    {"id":"SB005","name":"Roasted Almonds","brand":"Nutraj","category":"Snacks & Beverages","price":299,"unit":"200g","labels":["no-artificial-additives","no-added-sugar"]},
    {"id":"SB006","name":"Green Tea Darjeeling","brand":"Teabox","category":"Snacks & Beverages","price":499,"unit":"50g","labels":["organic","no-artificial-additives","pesticide-free"]},
    {"id":"SB007","name":"Makhana Cheese Herbs","brand":"WickedGüd","category":"Snacks & Beverages","price":99,"unit":"60g","labels":["no-artificial-additives","gluten-free","high-protein"]},
    {"id":"SB008","name":"Trail Mix Premium","brand":"True Elements","category":"Snacks & Beverages","price":349,"unit":"250g","labels":["no-artificial-additives","no-added-sugar"]},
    {"id":"HN001","name":"Whey Protein Light Cocoa","brand":"The Whole Truth","category":"Health & Nutrition","price":1799,"unit":"1kg","labels":["no-artificial-additives","no-added-sugar","high-protein"]},
    {"id":"HN002","name":"Chia Seeds","brand":"True Elements","category":"Health & Nutrition","price":199,"unit":"250g","labels":["organic","no-artificial-additives","high-fibre","vegan"]},
    {"id":"HN003","name":"Spirulina Powder","brand":"Himalayan Organics","category":"Health & Nutrition","price":599,"unit":"100g","labels":["organic","vegan","high-protein"]},
    {"id":"HN004","name":"Ashwagandha KSM-66","brand":"Wellbeing Nutrition","category":"Health & Nutrition","price":699,"unit":"60 capsules","labels":["organic","no-artificial-additives","vegan"]},
    {"id":"HN005","name":"Flaxseed Powder","brand":"Conscious Food","category":"Health & Nutrition","price":149,"unit":"250g","labels":["organic","vegan","high-fibre"]},
    {"id":"KB001","name":"Organic Baby Cereal Ragi","brand":"Slurrp Farm","category":"Kids & Baby","price":249,"unit":"200g","labels":["organic","no-artificial-additives","no-added-sugar","gluten-free"]},
    {"id":"KB002","name":"Kids Multigrain Pancake Mix","brand":"Slurrp Farm","category":"Kids & Baby","price":199,"unit":"150g","labels":["no-artificial-additives","no-refined-sugar","whole-grain"]},
]

CATALOG_JSON = json.dumps({
    cat: [p for p in CATALOG if p["category"] == cat]
    for cat in set(p["category"] for p in CATALOG)
}, indent=2)

CATALOG_STATS = {
    "total": len(CATALOG),
    "categories": len(set(p["category"] for p in CATALOG)),
    "by_category": {cat: len([p for p in CATALOG if p["category"] == cat]) for cat in set(p["category"] for p in CATALOG)}
}

# ─── Gemini API Call ──────────────────────────────────────────
def call_gemini(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4000}}
    r = requests.post(url, json=payload, timeout=60)
    if r.status_code != 200:
        raise Exception(f"API Error {r.status_code}: {r.json().get('error', {}).get('message', r.text)}")
    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

def parse_json(raw):
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"): raw = raw[4:]
    return json.loads(raw.strip())

# ─── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 Smart Grocery Curator")
    st.caption("Powered by Gemini API")
    st.divider()
    api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...", help="Free key from aistudio.google.com")
    st.divider()
    st.markdown("### 👤 Your Profile")
    name = st.text_input("Name", value="Priya")
    age_group = st.selectbox("Age Group", ["18 to 25 yrs", "26 to 35 yrs", "36 to 45 yrs", "46 yrs and above"])
    household = st.multiselect("Household", ["Just me", "Spouse", "Kids", "Flatmates", "Pets", "Parents"], default=["Just me"])
    diet = st.multiselect("Diet", ["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian", "Keto/Low Carb", "Gluten Free", "High Protein"], default=["Vegetarian"])
    trust_signals = st.multiselect("Trust Signals", ["Organic", "Pesticide free", "No artificial additives", "Hormone free", "Palm oil free"], default=["Organic", "Pesticide free"])
    health_goals = st.text_input("Health Goals", value="High protein, low sugar, gut health")
    allergies = st.text_input("Allergies / Avoid", value="None")
    budget = st.slider("Weekly Budget (₹)", 500, 5000, 1800, 100)
    st.divider()
    st.markdown(f"**Catalog:** {CATALOG_STATS['total']} SKUs · {CATALOG_STATS['categories']} categories")
    generate_btn = st.button("🛒 Curate My Basket", type="primary", use_container_width=True)

# ─── Main ─────────────────────────────────────────────────────
st.markdown('<p class="main-title">🌿 Smart Grocery Curation Engine</p>', unsafe_allow_html=True)
st.caption("AI-powered weekly basket built from a 500+ SKU premium catalog — personalized to your diet, household, and trust preferences")

with st.expander("⚙️ How the 3-stage prompt chain works"):
    c1, c2, c3 = st.columns(3)
    c1.markdown("**Stage 1 — Classifier**\nAnalyzes your profile and builds a grocery persona to shape everything downstream.")
    c2.markdown("**Stage 2 — SKU Matcher**\nScans the catalog and selects 12-16 products matching your persona, budget, and dietary needs.")
    c3.markdown("**Stage 3 — Basket Optimizer**\nGroups products by meal occasion, adds curator notes, suggests substitutions, calculates time saved.")

st.divider()

if generate_btn:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar. Get one free at aistudio.google.com")
        st.stop()

    user_profile = {
        "name": name, "household": ", ".join(household) if household else "Just me",
        "age_group": age_group, "diet": diet if diet else ["Vegetarian"],
        "trust_signals": trust_signals if trust_signals else ["No artificial additives"],
        "budget": budget, "health_goals": health_goals, "allergies": allergies
    }

    p1, p2, p3 = st.columns(3)
    s1 = p1.empty(); s2 = p2.empty(); s3 = p3.empty()
    s1.info("🧠 Stage 1: Classifying persona...")
    s2.warning("🔍 Stage 2: Waiting...")
    s3.warning("✨ Stage 3: Waiting...")
    status = st.empty()

    try:
        # Stage 1
        status.text("Stage 1: Building your grocery persona...")
        p1_prompt = f"""You are a grocery intelligence engine. Classify this user profile and output ONLY valid JSON with no markdown:
Profile: Name={user_profile['name']}, Household={user_profile['household']}, Age={user_profile['age_group']}, Diet={', '.join(user_profile['diet'])}, Trust signals={', '.join(user_profile['trust_signals'])}, Budget=Rs.{budget}, Goals={health_goals}, Allergies={allergies}

Output this exact JSON structure:
{{"persona_type": "string", "persona_description": "2 sentences", "key_priorities": ["p1","p2","p3"], "weekly_meal_pattern": "brief description", "curation_tone": "string"}}"""
        persona = parse_json(call_gemini(api_key, p1_prompt))
        s1.success("✅ Stage 1: Persona built")
        s2.info("🔍 Stage 2: Matching SKUs...")

        # Stage 2
        status.text("Stage 2: Selecting products from catalog...")
        p2_prompt = f"""You are a premium grocery curator. Select 12-15 products for this customer.
Persona: {json.dumps(persona)}
Diet: {', '.join(user_profile['diet'])} — STRICTLY respect this. Vegetarian = no meat/fish. Vegan = no dairy/eggs.
Trust requirements: {', '.join(user_profile['trust_signals'])}
Weekly budget: Rs.{budget}
Household: {user_profile['household']}
Health goals: {health_goals}
Allergies/Avoid: {allergies}

Available products (select only from these):
{CATALOG_JSON}

Output ONLY valid JSON with no markdown:
{{"selected_skus": [{{"id": "id", "name": "name", "category": "cat", "price": 0, "unit": "unit", "reason": "1 sentence why"}}], "total_estimated_cost": 0, "coverage_summary": "2 sentences"}}"""
        matched = parse_json(call_gemini(api_key, p2_prompt))
        s2.success("✅ Stage 2: SKUs matched")
        s3.info("✨ Stage 3: Optimizing basket...")

        # Stage 3
        status.text("Stage 3: Building your final personalized basket...")
        p3_prompt = f"""You are finalizing a weekly grocery basket. 
Customer: {name} | {user_profile['household']} | {user_profile['age_group']}
Persona: {persona.get('persona_type','')}
Selected products: {json.dumps(matched.get('selected_skus',[]))}
Budget: Rs.{budget}

Output ONLY valid JSON with no markdown:
{{"final_basket": [{{"id":"id","name":"name","category":"cat","price":0,"unit":"unit","occasion":"Breakfast/Lunch/Dinner/Snack/Pantry/Health","curator_note":"why or null","quality_highlight":"key attribute"}}], "basket_total": 0, "meal_plan_summary": {{"breakfast":"covered","lunch":"covered","dinner":"covered","snacks":"options","health_stack":"supplements"}}, "smart_substitutions": [{{"original":"name","substitute":"option","saving":0,"trade_off":"what you give up"}}], "basket_insights": {{"clean_label_score":"X of Y meet criteria","time_saved_minutes":20,"weekly_nutrition_highlight":"insight"}}, "curator_personal_note": "2-3 sentence personal note"}}"""
        final = parse_json(call_gemini(api_key, p3_prompt))
        s3.success("✅ Stage 3: Basket ready!")
        status.success("✅ Your personalized basket is ready!")

        st.divider()

        # Persona
        st.markdown("### 🧠 Your Grocery Persona")
        st.markdown(f"""<div class="persona-card"><div style="font-size:1.4rem;font-weight:700;margin-bottom:0.5rem;">✦ {persona.get('persona_type','')}</div><p style="opacity:0.9">{persona.get('persona_description','')}</p><div>{''.join([f'<span style="background:rgba(255,255,255,0.2);padding:3px 10px;border-radius:12px;font-size:0.78rem;margin-right:6px">{p}</span>' for p in persona.get('key_priorities',[])])}</div></div>""", unsafe_allow_html=True)
        st.divider()

        # Basket
        st.markdown("### 🛒 Your Weekly Basket")
        basket = final.get('final_basket', [])
        total = final.get('basket_total', 0)
        budget_diff = budget - total
        col_a, col_b = st.columns(2)
        col_a.metric("Basket Total", f"₹{total}", f"₹{abs(budget_diff)} {'under' if budget_diff >= 0 else 'over'} budget")
        col_b.metric("Items", len(basket))

        occasions = {}
        for item in basket:
            occ = item.get('occasion', 'Other')
            occasions.setdefault(occ, []).append(item)

        icons = {"Breakfast":"🌅","Lunch":"☀️","Dinner":"🌙","Snack":"🍎","Pantry":"🏠","Health":"💊","Other":"📦"}
        for occ, items in occasions.items():
            st.markdown(f"**{icons.get(occ,'📦')} {occ}**")
            cols = st.columns(2)
            for i, item in enumerate(items):
                with cols[i % 2]:
                    note = f'<div class="curator-note">💬 {item["curator_note"]}</div>' if item.get("curator_note") else ""
                    st.markdown(f"""<div class="product-card"><div class="product-name">{item.get('name','')}</div><div style="font-size:0.8rem;color:#888">{item.get('category','')} · {item.get('unit','')}</div><div style="color:#2e7d32;font-size:0.78rem;margin:3px 0">✦ {item.get('quality_highlight','')}</div><div class="product-price">₹{item.get('price',0)}</div>{note}</div>""", unsafe_allow_html=True)
        st.divider()

        # Meal Plan
        st.markdown("### 📅 Weekly Meal Coverage")
        meal = final.get('meal_plan_summary', {})
        meal_icons = {"breakfast":"🌅","lunch":"☀️","dinner":"🌙","snacks":"🍎","health_stack":"💊"}
        for k, v in meal.items():
            st.markdown(f"**{meal_icons.get(k,'🍽️')} {k.replace('_',' ').title()}:** {v}")
        st.divider()

        # Substitutions
        subs = final.get('smart_substitutions', [])
        if subs:
            st.markdown("### 🔄 Smart Substitutions")
            for s in subs:
                st.markdown(f"**Swap:** {s.get('original','')} → **{s.get('substitute','')}** · 💚 Save ₹{s.get('saving',0)} · Trade-off: {s.get('trade_off','')}")
            st.divider()

        # Insights
        st.markdown("### 📊 Basket Insights")
        insights = final.get('basket_insights', {})
        c1, c2 = st.columns(2)
        with c1:
            if insights.get('clean_label_score'):
                st.markdown(f'<div class="insight-card">🏷️ <strong>Clean Label Score</strong><br>{insights["clean_label_score"]}</div>', unsafe_allow_html=True)
        with c2:
            if insights.get('time_saved_minutes'):
                st.markdown(f'<div class="insight-card">⏱️ <strong>Time Saved</strong><br>~{insights["time_saved_minutes"]} minutes vs. manually browsing</div>', unsafe_allow_html=True)
        if insights.get('weekly_nutrition_highlight'):
            st.markdown(f'<div class="insight-card">🥗 <strong>Nutrition Highlight</strong><br>{insights["weekly_nutrition_highlight"]}</div>', unsafe_allow_html=True)

        # Personal note
        if final.get('curator_personal_note'):
            st.markdown(f"""<div style="background:linear-gradient(135deg,#f0f7f0,#e8f5e9);border-radius:12px;padding:1.2rem;border-left:4px solid #2e7d32;font-style:italic;color:#2e7d32;margin:1rem 0">✍️ <strong>A note from your curator:</strong><br><br>{final['curator_personal_note']}</div>""", unsafe_allow_html=True)

    except json.JSONDecodeError as e:
        st.error(f"Response parsing error — please try again. ({str(e)})")
    except Exception as e:
        st.error(f"Error: {str(e)}")

else:
    st.markdown("### How to use")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**1. Get free API key**\n\nGo to [aistudio.google.com](https://aistudio.google.com) → API Keys → Create API key")
    c2.markdown("**2. Set your preferences**\n\nFill in diet, household, trust signals, and weekly budget in the sidebar")
    c3.markdown("**3. Get your basket**\n\nClick 'Curate My Basket' — the 3-stage pipeline builds your list in ~20 seconds")
    st.divider()
    st.markdown("### 📦 What's in the catalog")
    cols = st.columns(len(CATALOG_STATS['by_category']))
    for i, (cat, count) in enumerate(CATALOG_STATS['by_category'].items()):
        cols[i % len(cols)].metric(cat.split("&")[0].strip(), f"{count} SKUs")
    st.divider()
    st.caption("Built by Kanik Kumar · CS '27, BITS Pilani · Proof-of-work for FirstClub's Growth Intern role")
