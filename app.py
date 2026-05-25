"""
Smart Grocery Curation Engine for Premium Households
=====================================================
AI-powered weekly basket curation using Claude API
3-stage prompt chain: Classify → Match → Optimize

Author: Kanik Kumar | CS '27, BITS Pilani
"""

import streamlit as st
import json
import time
from catalog import get_catalog_stats
from curator import generate_basket

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Grocery Curator",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #1a3c2a;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    .stage-badge {
        background: #e8f5e9;
        color: #1a3c2a;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .persona-card {
        background: linear-gradient(135deg, #1a3c2a 0%, #2e7d32 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }
    .persona-type {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .product-card {
        background: #fafaf8;
        border: 1px solid #e8e8e4;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border-left: 3px solid #2e7d32;
        font-family: 'Inter', sans-serif;
    }
    .product-name {
        font-weight: 600;
        font-size: 0.95rem;
        color: #1a3c2a;
    }
    .product-brand {
        font-size: 0.8rem;
        color: #888;
        margin-bottom: 0.3rem;
    }
    .product-price {
        font-weight: 700;
        color: #2e7d32;
        font-size: 1rem;
    }
    .label-chip {
        background: #e8f5e9;
        color: #1a3c2a;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 500;
        margin-right: 4px;
        display: inline-block;
        margin-bottom: 2px;
    }
    .occasion-tag {
        background: #fff3e0;
        color: #e65100;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 6px;
    }
    .curator-note {
        font-size: 0.8rem;
        color: #555;
        font-style: italic;
        margin-top: 0.3rem;
    }
    .insight-card {
        background: #fffde7;
        border: 1px solid #f9a825;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    .total-card {
        background: #1a3c2a;
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }
    .pipeline-step {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
    }
    .step-active { background: #e8f5e9; border: 2px solid #2e7d32; }
    .step-done { background: #c8e6c9; border: 2px solid #388e3c; }
    .step-pending { background: #f5f5f5; border: 2px dashed #ccc; }
    .sub-card {
        background: #fff8e1;
        border: 1px solid #ffcc02;
        border-radius: 10px;
        padding: 0.8rem;
        margin-bottom: 0.6rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }
    .meal-plan-item {
        padding: 0.6rem 0;
        border-bottom: 1px solid #eee;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }
    .personal-note {
        background: linear-gradient(135deg, #f0f7f0 0%, #e8f5e9 100%);
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid #2e7d32;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-style: italic;
        color: #2e7d32;
        margin: 1rem 0;
    }
    .quality-badge {
        background: #ff6f00;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 Smart Grocery Curator")
    st.markdown("*Powered by Gemini API*")
    st.divider()
    
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Get your free key at aistudio.google.com",
        placeholder="AIza...."
    )
    
    st.divider()
    st.markdown("### 👤 Your Profile")
    
    name = st.text_input("Name", value="Priya", placeholder="Your name")
    
    age_group = st.selectbox(
        "Age Group",
        ["18 to 25 yrs", "26 to 35 yrs", "36 to 45 yrs", "46 yrs and above"]
    )
    
    household = st.multiselect(
        "Household",
        ["Just me", "Spouse", "Kids", "Flatmates", "Pets", "Parents"],
        default=["Just me"]
    )
    
    diet = st.multiselect(
        "Diet",
        ["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian", "Keto/Low Carb", "Gluten Free", "High Protein"],
        default=["Vegetarian"]
    )
    
    trust_signals = st.multiselect(
        "Trust Signals",
        ["Organic", "Pesticide free", "No artificial additives", "Hormone free", "Palm oil free"],
        default=["Organic", "Pesticide free"]
    )
    
    health_goals = st.text_input(
        "Health Goals",
        value="High protein, low sugar, gut health",
        placeholder="e.g. weight loss, high protein..."
    )
    
    allergies = st.text_input(
        "Allergies / Avoid",
        value="None",
        placeholder="e.g. lactose, nuts, gluten"
    )
    
    budget = st.slider(
        "Weekly Budget (₹)",
        min_value=500, max_value=5000, value=1800, step=100
    )
    
    st.divider()
    
    # Catalog stats
    stats = get_catalog_stats()
    st.markdown(f"**Catalog:** {stats['total_skus']} SKUs · {stats['categories']} categories")
    st.markdown(f"**Avg Quality Score:** {stats['avg_quality']}/10")
    
    generate_btn = st.button("🛒 Curate My Basket", type="primary", use_container_width=True)


# ─── Main Content ─────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">Smart Grocery Curation Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">AI-powered weekly basket built from a 500+ SKU premium catalog — personalized to your diet, household, and trust preferences</p>', unsafe_allow_html=True)

# How it works
with st.expander("⚙️ How the 3-stage prompt chain works", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        **Stage 1 — Classifier**
        
        Claude analyzes your profile (diet, household, trust signals, goals) and builds a grocery persona. This shapes everything downstream — not just what to buy, but *why* and *how* to present it.
        """)
    with c2:
        st.markdown("""
        **Stage 2 — SKU Matcher**
        
        Claude scans 500+ SKUs and selects 12-18 products that match your persona, budget, and dietary needs. Every product must pass your trust signal requirements.
        """)
    with c3:
        st.markdown("""
        **Stage 3 — Basket Optimizer**
        
        Claude groups products into meal occasions, writes curator notes for premium items, suggests substitutions if over budget, and calculates time saved vs. manually building a basket.
        """)

st.divider()

# ─── Generation ───────────────────────────────────────────────────────────────
if generate_btn:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
        st.stop()
    
    if len(api_key) < 10:
        st.error("Please enter a valid Gemini API key.")
        st.stop()
    
    user_profile = {
        "name": name,
        "household": ", ".join(household) if household else "Just me",
        "age_group": age_group,
        "diet": diet if diet else ["Vegetarian"],
        "trust_signals": trust_signals if trust_signals else ["No artificial additives"],
        "budget": budget,
        "health_goals": health_goals,
        "allergies": allergies
    }
    
    # Pipeline progress
    st.markdown("### 🔄 Running Curation Pipeline")
    
    p1, p2, p3 = st.columns(3)
    
    with p1:
        stage1_placeholder = st.empty()
        stage1_placeholder.markdown('<div class="pipeline-step step-active">🧠 Stage 1<br><small>Classifying your persona...</small></div>', unsafe_allow_html=True)
    with p2:
        stage2_placeholder = st.empty()
        stage2_placeholder.markdown('<div class="pipeline-step step-pending">🔍 Stage 2<br><small>Waiting...</small></div>', unsafe_allow_html=True)
    with p3:
        stage3_placeholder = st.empty()
        stage3_placeholder.markdown('<div class="pipeline-step step-pending">✨ Stage 3<br><small>Waiting...</small></div>', unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    start_time = time.time()
    
    status_text.text("Stage 1: Analyzing your profile and building persona...")
    progress_bar.progress(10)
    
    result = generate_basket(api_key, user_profile)
    
    if result["error"]:
        st.error(f"Error: {result['error']}")
        st.stop()
    
    # Update pipeline visuals
    stage1_placeholder.markdown('<div class="pipeline-step step-done">✅ Stage 1<br><small>Persona built</small></div>', unsafe_allow_html=True)
    stage2_placeholder.markdown('<div class="pipeline-step step-done">✅ Stage 2<br><small>SKUs matched</small></div>', unsafe_allow_html=True)
    stage3_placeholder.markdown('<div class="pipeline-step step-done">✅ Stage 3<br><small>Basket optimized</small></div>', unsafe_allow_html=True)
    progress_bar.progress(100)
    
    elapsed = round(time.time() - start_time, 1)
    status_text.success(f"✅ Basket curated in {elapsed}s")
    
    st.divider()
    
    persona = result["stage_1_persona"]
    matched = result["stage_2_matched"]
    final = result["stage_3_final"]
    
    # ─── Persona Card ─────────────────────────────────────────────────────
    st.markdown("### 🧠 Your Grocery Persona")
    
    st.markdown(f"""
    <div class="persona-card">
        <div class="persona-type">✦ {persona.get('persona_type', '')}</div>
        <p style="opacity: 0.9; margin: 0.3rem 0 0.8rem 0;">{persona.get('persona_description', '')}</p>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            {''.join([f'<span style="background: rgba(255,255,255,0.2); padding: 3px 10px; border-radius: 12px; font-size: 0.78rem;">{p}</span>' for p in persona.get('key_priorities', [])])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Meal Pattern:**")
        st.caption(persona.get('weekly_meal_pattern', ''))
    with col2:
        st.markdown("**Curation Style:**")
        st.caption(f"_{persona.get('curation_tone', '')}_")
    
    st.divider()
    
    # ─── Final Basket ─────────────────────────────────────────────────────
    st.markdown("### 🛒 Your Weekly Basket")
    
    basket = final.get('final_basket', [])
    total = final.get('basket_total', 0)
    
    # Total card
    budget_remaining = budget - total
    budget_color = "#c8e6c9" if budget_remaining >= 0 else "#ffcdd2"
    st.markdown(f"""
    <div class="total-card">
        <div>
            <div style="font-size: 0.8rem; opacity: 0.7;">BASKET TOTAL</div>
            <div style="font-size: 1.8rem; font-weight: 700;">₹{total}</div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.8rem; opacity: 0.7;">BUDGET: ₹{budget}</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: {'#a5d6a7' if budget_remaining >= 0 else '#ef9a9a'}">
                {'₹'+str(abs(budget_remaining))+' under budget' if budget_remaining >= 0 else '₹'+str(abs(budget_remaining))+' over budget'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Group by occasion
    occasions = {}
    for item in basket:
        occ = item.get('occasion', 'Other')
        if occ not in occasions:
            occasions[occ] = []
        occasions[occ].append(item)
    
    occasion_icons = {
        "Breakfast": "🌅",
        "Lunch": "☀️",
        "Dinner": "🌙",
        "Snack": "🍎",
        "Pantry": "🏠",
        "Health": "💊",
        "Other": "📦"
    }
    
    for occasion, items in occasions.items():
        icon = occasion_icons.get(occasion, "📦")
        st.markdown(f"**{icon} {occasion}**")
        
        cols = st.columns(2)
        for i, item in enumerate(items):
            with cols[i % 2]:
                quality_highlight = item.get('quality_highlight', '')
                curator_note = item.get('curator_note', '')
                
                note_html = f'<div class="curator-note">💬 {curator_note}</div>' if curator_note else ''
                quality_html = f'<span class="quality-badge">✦ {quality_highlight}</span>' if quality_highlight else ''
                
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-name">{item.get('name', '')} <span class="occasion-tag">{occasion}</span></div>
                    <div class="product-brand">{item.get('category', '')} · {item.get('unit', '')}</div>
                    <div style="margin: 0.3rem 0;">{quality_html}</div>
                    <div class="product-price">₹{item.get('price', 0)}</div>
                    {note_html}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("")
    
    st.divider()
    
    # ─── Meal Plan ────────────────────────────────────────────────────────
    st.markdown("### 📅 Weekly Meal Coverage")
    
    meal_plan = final.get('meal_plan_summary', {})
    meal_icons = {"breakfast": "🌅", "lunch": "☀️", "dinner": "🌙", "snacks": "🍎", "health_stack": "💊"}
    
    for meal, description in meal_plan.items():
        icon = meal_icons.get(meal, "🍽️")
        st.markdown(f"""
        <div class="meal-plan-item">
            <strong>{icon} {meal.replace('_', ' ').title()}:</strong> {description}
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ─── Smart Substitutions ──────────────────────────────────────────────
    substitutions = final.get('smart_substitutions', [])
    if substitutions:
        st.markdown("### 🔄 Smart Substitutions")
        st.caption("If you want to save more without losing quality:")
        
        for sub in substitutions:
            st.markdown(f"""
            <div class="sub-card">
                <strong>Swap:</strong> {sub.get('original', '')} → <strong>{sub.get('substitute', '')}</strong><br>
                <span style="color: #2e7d32; font-weight: 600;">Save ₹{sub.get('saving', 0)}</span>
                <span style="color: #888; margin-left: 8px;">· Trade-off: {sub.get('trade_off', '')}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
    
    # ─── Basket Insights ──────────────────────────────────────────────────
    st.markdown("### 📊 Basket Insights")
    
    insights = final.get('basket_insights', {})
    
    i1, i2 = st.columns(2)
    with i1:
        if insights.get('clean_label_score'):
            st.markdown(f"""
            <div class="insight-card">
                🏷️ <strong>Clean Label Score</strong><br>
                {insights['clean_label_score']}
            </div>
            """, unsafe_allow_html=True)
        
        if insights.get('weekly_nutrition_highlight'):
            st.markdown(f"""
            <div class="insight-card">
                🥗 <strong>Nutrition Highlight</strong><br>
                {insights['weekly_nutrition_highlight']}
            </div>
            """, unsafe_allow_html=True)
    
    with i2:
        if insights.get('time_saved_minutes'):
            st.markdown(f"""
            <div class="insight-card">
                ⏱️ <strong>Time Saved</strong><br>
                ~{insights['time_saved_minutes']} minutes vs. manually building this basket
            </div>
            """, unsafe_allow_html=True)
        
        if insights.get('quality_vs_generic_saving'):
            st.markdown(f"""
            <div class="insight-card">
                💰 <strong>Quality vs. Generic</strong><br>
                {insights['quality_vs_generic_saving']}
            </div>
            """, unsafe_allow_html=True)
    
    # ─── Curator's Personal Note ───────────────────────────────────────────
    if final.get('curator_personal_note'):
        st.markdown(f"""
        <div class="personal-note">
            ✍️ <strong>A note from your curator:</strong><br><br>
            {final['curator_personal_note']}
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ─── Raw Pipeline Output ──────────────────────────────────────────────
    with st.expander("🔬 View raw pipeline output (all 3 stages)", expanded=False):
        st.markdown("**Stage 1 — Persona Classification:**")
        st.json(persona)
        
        st.markdown("**Stage 2 — SKU Matching:**")
        st.json({"total_cost": matched.get('total_estimated_cost'), 
                 "count": len(matched.get('selected_skus', [])),
                 "coverage": matched.get('coverage_summary')})
        
        st.markdown("**Stage 3 — Optimized Basket:**")
        st.json(insights)

else:
    # ─── Landing State ────────────────────────────────────────────────────
    st.markdown("### How to use")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        **1. Add your API key**
        
        Enter your Anthropic API key in the sidebar. Get one free at [console.anthropic.com](https://console.anthropic.com).
        """)
    with c2:
        st.markdown("""
        **2. Set your preferences**
        
        Fill in your diet, household, trust signals, and weekly budget. The more specific, the better your basket.
        """)
    with c3:
        st.markdown("""
        **3. Get your basket**
        
        Click "Curate My Basket" and the 3-stage Claude pipeline builds a personalized weekly grocery list in ~15 seconds.
        """)
    
    st.divider()
    
    # Catalog preview
    st.markdown("### 📦 What's in the catalog")
    
    stats = get_catalog_stats()
    cols = st.columns(len(stats['category_counts']))
    for i, (cat, count) in enumerate(stats['category_counts'].items()):
        with cols[i % len(cols)]:
            st.metric(cat.split("&")[0].strip(), f"{count} SKUs")
    
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #aaa; font-size: 0.85rem; font-family: 'Inter', sans-serif; padding: 1rem;">
        Built by <strong>Kanik Kumar</strong> · CS '27, BITS Pilani · 
        Proof-of-work for FirstClub's Growth Intern role<br>
        Claude API · Streamlit · 500+ curated SKUs · 3-stage prompt chain
    </div>
    """, unsafe_allow_html=True)
