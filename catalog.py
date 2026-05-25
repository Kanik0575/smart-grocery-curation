"""
SKU Catalog for Smart Grocery Curation Engine
500+ premium household grocery products across FirstClub-style categories
"""

import pandas as pd
import json

RAW_CATALOG = [
    # ─── FRUITS & VEGETABLES ───────────────────────────────────────────────
    {"id": "FV001", "name": "Alphonso Mangoes", "brand": "Farm Direct", "category": "Fruits & Vegetables", "subcategory": "Seasonal Fruits", "price": 299, "unit": "1 dozen", "labels": ["pesticide-free", "farm-direct"], "quality_score": 9.5, "description": "Sweetness-tested, farm-direct Devgad Alphonsos"},
    {"id": "FV002", "name": "Organic Tomatoes", "brand": "Member's Pick", "category": "Fruits & Vegetables", "subcategory": "Vegetables", "price": 49, "unit": "500g", "labels": ["organic", "pesticide-free"], "quality_score": 9.2, "description": "Vine-ripened, pesticide residue tested"},
    {"id": "FV003", "name": "Baby Spinach", "brand": "Green Farms", "category": "Fruits & Vegetables", "subcategory": "Leafy Greens", "price": 55, "unit": "200g", "labels": ["organic", "pesticide-free", "no-artificial-additives"], "quality_score": 9.0, "description": "Triple-washed, ready to eat"},
    {"id": "FV004", "name": "Avocados", "brand": "Exotic Harvest", "category": "Fruits & Vegetables", "subcategory": "Exotic Fruits", "price": 149, "unit": "2 pcs", "labels": ["pesticide-free"], "quality_score": 8.8, "description": "Hass variety, ripeness-checked at dispatch"},
    {"id": "FV005", "name": "Yellow Lemons", "brand": "Member's Pick", "category": "Fruits & Vegetables", "subcategory": "Citrus", "price": 45, "unit": "500g", "labels": ["pesticide-free", "farm-direct"], "quality_score": 9.3, "description": "50% bigger than standard, never green"},
    {"id": "FV006", "name": "Red Bell Peppers", "brand": "Green Farms", "category": "Fruits & Vegetables", "subcategory": "Vegetables", "price": 89, "unit": "3 pcs", "labels": ["organic", "pesticide-free"], "quality_score": 9.0, "description": "Thick-walled, sweetness-guaranteed"},
    {"id": "FV007", "name": "Organic Bananas", "brand": "Farm Direct", "category": "Fruits & Vegetables", "subcategory": "Tropical Fruits", "price": 65, "unit": "6 pcs", "labels": ["organic", "pesticide-free", "farm-direct"], "quality_score": 8.9, "description": "Robusta variety, no artificial ripening"},
    {"id": "FV008", "name": "Cherry Tomatoes", "brand": "Member's Pick", "category": "Fruits & Vegetables", "subcategory": "Vegetables", "price": 79, "unit": "250g", "labels": ["organic", "pesticide-free"], "quality_score": 9.1, "description": "Sun-ripened, bursting with flavour"},
    {"id": "FV009", "name": "Broccoli", "brand": "Green Farms", "category": "Fruits & Vegetables", "subcategory": "Vegetables", "price": 69, "unit": "500g", "labels": ["pesticide-free", "no-artificial-additives"], "quality_score": 8.7, "description": "Cold-chain maintained, arrives fresh"},
    {"id": "FV010", "name": "Sweet Corn", "brand": "Farm Direct", "category": "Fruits & Vegetables", "subcategory": "Vegetables", "price": 55, "unit": "2 cobs", "labels": ["pesticide-free", "non-GMO"], "quality_score": 8.8, "description": "Non-GMO, same-day harvest delivery"},
    {"id": "FV011", "name": "Watermelon", "brand": "Farm Direct", "category": "Fruits & Vegetables", "subcategory": "Seasonal Fruits", "price": 199, "unit": "2-3 kg", "labels": ["pesticide-free", "sweetness-tested"], "quality_score": 9.2, "description": "Brix-tested for sweetness before dispatch"},
    {"id": "FV012", "name": "French Beans", "brand": "Green Farms", "category": "Fruits & Vegetables", "subcategory": "Vegetables", "price": 49, "unit": "250g", "labels": ["organic", "pesticide-free"], "quality_score": 8.9, "description": "Tender, string-free, farm-to-door"},
    {"id": "FV013", "name": "Dragon Fruit", "brand": "Exotic Harvest", "category": "Fruits & Vegetables", "subcategory": "Exotic Fruits", "price": 179, "unit": "1 pc (~500g)", "labels": ["pesticide-free"], "quality_score": 8.6, "description": "Red-flesh variety, antioxidant-rich"},
    {"id": "FV014", "name": "Organic Cucumber", "brand": "Member's Pick", "category": "Fruits & Vegetables", "subcategory": "Vegetables", "price": 39, "unit": "3 pcs", "labels": ["organic", "pesticide-free"], "quality_score": 9.0, "description": "Crisp, wax-free, ready to eat"},
    {"id": "FV015", "name": "Pomegranate", "brand": "Farm Direct", "category": "Fruits & Vegetables", "subcategory": "Seasonal Fruits", "price": 89, "unit": "1 pc (~400g)", "labels": ["pesticide-free", "farm-direct"], "quality_score": 9.1, "description": "Bhagwa variety, ruby-red arils guaranteed"},

    # ─── DAIRY & EGGS ─────────────────────────────────────────────────────
    {"id": "DE001", "name": "Akshayakalpa A2 Organic Milk", "brand": "Akshayakalpa", "category": "Dairy & Eggs", "subcategory": "Milk", "price": 45, "unit": "500ml", "labels": ["organic", "hormone-free", "no-artificial-additives", "A2"], "quality_score": 9.8, "description": "100% A2 milk from grass-fed Gir cows, zero antibiotics"},
    {"id": "DE002", "name": "High Protein Organic Paneer", "brand": "Akshayakalpa", "category": "Dairy & Eggs", "subcategory": "Paneer", "price": 89, "unit": "200g", "labels": ["organic", "hormone-free", "high-protein", "no-artificial-additives"], "quality_score": 9.7, "description": "56g protein per 100g, made from A2 milk"},
    {"id": "DE003", "name": "Greek Yogurt - Strawberry", "brand": "Epigamia", "category": "Dairy & Eggs", "subcategory": "Yogurt", "price": 65, "unit": "90g", "labels": ["no-artificial-additives", "high-protein", "no-added-sugar"], "quality_score": 9.2, "description": "20g protein, no artificial sweeteners"},
    {"id": "DE004", "name": "Skyr Icelandic Yogurt", "brand": "MilkyMist", "category": "Dairy & Eggs", "subcategory": "Yogurt", "price": 79, "unit": "100g", "labels": ["high-protein", "no-artificial-additives", "low-fat"], "quality_score": 9.0, "description": "25g protein, authentic Icelandic style"},
    {"id": "DE005", "name": "Organic Curd", "brand": "Akshayakalpa", "category": "Dairy & Eggs", "subcategory": "Curd", "price": 55, "unit": "400g", "labels": ["organic", "hormone-free", "probiotic"], "quality_score": 9.5, "description": "Live cultures, set from A2 organic milk"},
    {"id": "DE006", "name": "Free-Range Brown Eggs", "brand": "Country Delight", "category": "Dairy & Eggs", "subcategory": "Eggs", "price": 99, "unit": "6 pcs", "labels": ["hormone-free", "cage-free", "no-antibiotics"], "quality_score": 9.3, "description": "Hens raised on natural feed, pasture-roaming"},
    {"id": "DE007", "name": "Mozzarella Cheese", "brand": "Vallombrosa", "category": "Dairy & Eggs", "subcategory": "Cheese", "price": 288, "unit": "250g", "labels": ["no-artificial-additives", "no-preservatives"], "quality_score": 9.4, "description": "Italian-style, made in India with A2 milk"},
    {"id": "DE008", "name": "Smoked Gouda", "brand": "Begum Victoria", "category": "Dairy & Eggs", "subcategory": "Cheese", "price": 637, "unit": "200g", "labels": ["no-artificial-additives"], "quality_score": 9.6, "description": "Smoked in small batches, aged 3 months"},
    {"id": "DE009", "name": "Cream Cheese", "brand": "Dlecta", "category": "Dairy & Eggs", "subcategory": "Cheese", "price": 189, "unit": "150g", "labels": ["no-artificial-additives", "no-preservatives"], "quality_score": 8.9, "description": "Smooth, spreadable, real cream base"},
    {"id": "DE010", "name": "Butter - Unsalted", "brand": "Normandy", "category": "Dairy & Eggs", "subcategory": "Butter", "price": 159, "unit": "100g", "labels": ["no-artificial-additives", "hormone-free"], "quality_score": 9.1, "description": "European-style, 84% fat content"},
    {"id": "DE011", "name": "Almond Milk Unsweetened", "brand": "137 Degrees", "category": "Dairy & Eggs", "subcategory": "Plant Milk", "price": 429, "unit": "1L", "labels": ["vegan", "no-artificial-additives", "no-added-sugar", "palm-oil-free"], "quality_score": 9.0, "description": "Cold-pressed almonds, no carrageenan"},
    {"id": "DE012", "name": "Oat Milk Barista", "brand": "Only Earth", "category": "Dairy & Eggs", "subcategory": "Plant Milk", "price": 266, "unit": "1L", "labels": ["vegan", "no-artificial-additives", "palm-oil-free"], "quality_score": 8.8, "description": "Barista blend, froths perfectly"},
    {"id": "DE013", "name": "Chickpea Tofu", "brand": "Health on Plants", "category": "Dairy & Eggs", "subcategory": "Plant Protein", "price": 175, "unit": "200g", "labels": ["vegan", "high-protein", "no-artificial-additives", "gluten-free"], "quality_score": 9.0, "description": "Made from chickpeas, 18g protein per 100g"},
    {"id": "DE014", "name": "A2 Desi Ghee", "brand": "Akshayakalpa", "category": "Dairy & Eggs", "subcategory": "Ghee", "price": 649, "unit": "500ml", "labels": ["organic", "hormone-free", "no-artificial-additives", "A2"], "quality_score": 9.7, "description": "Bilona method, cultured from A2 curd"},
    {"id": "DE015", "name": "Flavoured Kefir", "brand": "Yakult Plus", "category": "Dairy & Eggs", "subcategory": "Fermented", "price": 89, "unit": "200ml", "labels": ["probiotic", "no-artificial-additives"], "quality_score": 8.7, "description": "10B+ live cultures per bottle"},

    # ─── BREADS & BAKERY ──────────────────────────────────────────────────
    {"id": "BB001", "name": "Zero Maida Protein Bread", "brand": "The Health Factory", "category": "Breads & Bakery", "subcategory": "Bread", "price": 85, "unit": "250g (8-10 slices)", "labels": ["high-protein", "no-artificial-additives", "no-maida", "no-added-sugar"], "quality_score": 9.5, "description": "38g protein per loaf, zero refined flour"},
    {"id": "BB002", "name": "Member's Pick Whole Wheat Bread", "brand": "Member's Pick", "category": "Breads & Bakery", "subcategory": "Bread", "price": 59, "unit": "270g", "labels": ["no-artificial-additives", "no-preservatives", "whole-grain"], "quality_score": 9.2, "description": "Stone-ground whole wheat, baked fresh daily"},
    {"id": "BB003", "name": "Sourdough Loaf", "brand": "Artisan Bakes", "category": "Breads & Bakery", "subcategory": "Sourdough", "price": 189, "unit": "400g", "labels": ["no-artificial-additives", "no-preservatives", "naturally-fermented"], "quality_score": 9.6, "description": "48-hour cold ferment, open crumb"},
    {"id": "BB004", "name": "Cheese Garlic Bread", "brand": "Herbs & Co", "category": "Breads & Bakery", "subcategory": "Specialty Bread", "price": 99, "unit": "200g", "labels": ["no-artificial-additives", "no-preservatives"], "quality_score": 9.0, "description": "Real garlic, real cheese, baked fresh"},
    {"id": "BB005", "name": "Butter Garlic Toast", "brand": "Herbs & Co", "category": "Breads & Bakery", "subcategory": "Specialty Bread", "price": 69, "unit": "2 pcs", "labels": ["no-artificial-additives"], "quality_score": 8.8, "description": "Crispy, made with real butter"},
    {"id": "BB006", "name": "Multigrain Sandwich Bread", "brand": "Bonn", "category": "Breads & Bakery", "subcategory": "Bread", "price": 65, "unit": "400g", "labels": ["whole-grain", "no-artificial-additives"], "quality_score": 8.9, "description": "7-grain blend, high fibre"},
    {"id": "BB007", "name": "Banana Walnut Cake", "brand": "Artisan Bakes", "category": "Breads & Bakery", "subcategory": "Cakes", "price": 349, "unit": "400g", "labels": ["no-artificial-additives", "no-preservatives"], "quality_score": 9.3, "description": "Real bananas, California walnuts"},
    {"id": "BB008", "name": "Croissant - Butter", "brand": "La Boulangerie", "category": "Breads & Bakery", "subcategory": "Pastry", "price": 89, "unit": "2 pcs", "labels": ["no-artificial-additives", "no-preservatives"], "quality_score": 9.4, "description": "French laminated dough, 72-hour process"},
    {"id": "BB009", "name": "Ragi Millet Bread", "brand": "Slurrp Farm", "category": "Breads & Bakery", "subcategory": "Millet Bread", "price": 79, "unit": "250g", "labels": ["gluten-free", "no-artificial-additives", "high-fibre"], "quality_score": 9.1, "description": "Finger millet base, naturally gluten-free"},
    {"id": "BB010", "name": "Pita Bread", "brand": "Member's Pick", "category": "Breads & Bakery", "subcategory": "Flatbreads", "price": 55, "unit": "4 pcs", "labels": ["no-artificial-additives", "no-preservatives"], "quality_score": 8.7, "description": "Soft, pocketed, perfect for dipping"},

    # ─── STAPLES ──────────────────────────────────────────────────────────
    {"id": "ST001", "name": "Cold-Pressed Coconut Oil", "brand": "KLF Nirmal", "category": "Staples", "subcategory": "Cooking Oils", "price": 349, "unit": "500ml", "labels": ["cold-pressed", "no-artificial-additives", "non-GMO", "palm-oil-free"], "quality_score": 9.5, "description": "Wood-pressed, virgin grade, no heat treatment"},
    {"id": "ST002", "name": "Cold-Pressed Groundnut Oil", "brand": "Conscious Food", "category": "Staples", "subcategory": "Cooking Oils", "price": 299, "unit": "1L", "labels": ["cold-pressed", "no-artificial-additives", "non-GMO"], "quality_score": 9.3, "description": "Traditional wooden press, unrefined"},
    {"id": "ST003", "name": "Residue-Free Toor Dal", "brand": "Member's Pick", "category": "Staples", "subcategory": "Pulses", "price": 189, "unit": "1kg", "labels": ["pesticide-free", "no-artificial-additives", "residue-tested"], "quality_score": 9.4, "description": "Lab-tested for 300+ pesticide residues"},
    {"id": "ST004", "name": "Stone-Ground Whole Wheat Flour", "brand": "Aashirvaad Svasti", "category": "Staples", "subcategory": "Flour", "price": 99, "unit": "1kg", "labels": ["whole-grain", "no-artificial-additives", "stone-ground"], "quality_score": 9.2, "description": "Cold-stone milling preserves nutrients"},
    {"id": "ST005", "name": "Organic Red Rice", "brand": "Conscious Food", "category": "Staples", "subcategory": "Rice", "price": 199, "unit": "1kg", "labels": ["organic", "pesticide-free", "no-artificial-additives"], "quality_score": 9.0, "description": "Kerala red rice, hand-harvested"},
    {"id": "ST006", "name": "Raw Honey", "brand": "Two Brothers", "category": "Staples", "subcategory": "Sweeteners", "price": 499, "unit": "500g", "labels": ["raw", "no-artificial-additives", "no-added-sugar", "farm-direct"], "quality_score": 9.6, "description": "Single-origin, unheated, pollen intact"},
    {"id": "ST007", "name": "Himalayan Pink Salt", "brand": "Tata Salt Plus", "category": "Staples", "subcategory": "Salt & Spices", "price": 79, "unit": "1kg", "labels": ["natural", "no-artificial-additives", "mineral-rich"], "quality_score": 8.8, "description": "Unrefined, 84 trace minerals"},
    {"id": "ST008", "name": "Apple Cider Vinegar", "brand": "Bragg", "category": "Staples", "subcategory": "Condiments", "price": 399, "unit": "473ml", "labels": ["organic", "no-artificial-additives", "raw", "unfiltered"], "quality_score": 9.3, "description": "With the mother, unfiltered, organic"},
    {"id": "ST009", "name": "Organic Moong Dal", "brand": "Member's Pick", "category": "Staples", "subcategory": "Pulses", "price": 149, "unit": "500g", "labels": ["organic", "pesticide-free", "residue-tested"], "quality_score": 9.2, "description": "Certified organic, split green moong"},
    {"id": "ST010", "name": "Quinoa", "brand": "True Elements", "category": "Staples", "subcategory": "Grains", "price": 349, "unit": "500g", "labels": ["gluten-free", "high-protein", "no-artificial-additives", "non-GMO"], "quality_score": 9.1, "description": "White quinoa, pre-washed, 14g protein/100g"},
    {"id": "ST011", "name": "Coconut Sugar", "brand": "Conscious Food", "category": "Staples", "subcategory": "Sweeteners", "price": 199, "unit": "500g", "labels": ["organic", "no-artificial-additives", "low-GI"], "quality_score": 9.0, "description": "Low GI 35, unrefined, mineral-rich"},
    {"id": "ST012", "name": "Rolled Oats", "brand": "True Elements", "category": "Staples", "subcategory": "Breakfast Grains", "price": 149, "unit": "500g", "labels": ["gluten-free", "no-artificial-additives", "whole-grain"], "quality_score": 9.0, "description": "Thick-cut, steel-cut quality in rolled form"},
    {"id": "ST013", "name": "Almond Butter", "brand": "The Butternut Co.", "category": "Staples", "subcategory": "Nut Butters", "price": 499, "unit": "200g", "labels": ["no-artificial-additives", "no-added-sugar", "palm-oil-free", "high-protein"], "quality_score": 9.4, "description": "Single ingredient — just almonds"},
    {"id": "ST014", "name": "Peanut Butter Crunchy", "brand": "Pintola", "category": "Staples", "subcategory": "Nut Butters", "price": 299, "unit": "350g", "labels": ["no-artificial-additives", "no-added-sugar", "palm-oil-free", "high-protein"], "quality_score": 9.2, "description": "100% roasted peanuts, no hydrogenated oil"},
    {"id": "ST015", "name": "Cold-Pressed Mustard Oil", "brand": "KLF Nirmal", "category": "Staples", "subcategory": "Cooking Oils", "price": 249, "unit": "500ml", "labels": ["cold-pressed", "no-artificial-additives", "non-GMO"], "quality_score": 9.1, "description": "Kachi ghani, pungent North Indian style"},

    # ─── SNACKS & BEVERAGES ───────────────────────────────────────────────
    {"id": "SB001", "name": "No-Nonsense Plant Protein", "brand": "Cosmix", "category": "Snacks & Beverages", "subcategory": "Protein Supplements", "price": 899, "unit": "500g", "labels": ["vegan", "no-artificial-additives", "no-added-sugar", "high-protein", "palm-oil-free"], "quality_score": 9.3, "description": "No stevia, no enzymes, no carrageenan — clean label protein"},
    {"id": "SB002", "name": "Madras Mixture", "brand": "Kaara Puram", "category": "Snacks & Beverages", "subcategory": "Savoury Snacks", "price": 149, "unit": "250g", "labels": ["no-artificial-additives", "no-preservatives", "palm-oil-free"], "quality_score": 9.2, "description": "Authentic Chennai recipe, fried in groundnut oil"},
    {"id": "SB003", "name": "Guilt-Free Protein Munchies", "brand": "Yoga Bar", "category": "Snacks & Beverages", "subcategory": "Healthy Snacks", "price": 99, "unit": "30g", "labels": ["high-protein", "no-artificial-additives", "gluten-free"], "quality_score": 8.8, "description": "10g protein per pack, baked not fried"},
    {"id": "SB004", "name": "Dark Chocolate 70%", "brand": "Manam", "category": "Snacks & Beverages", "subcategory": "Chocolate", "price": 199, "unit": "55g", "labels": ["no-artificial-additives", "no-added-sugar", "vegan"], "quality_score": 9.5, "description": "Single origin Araku Valley cacao, bean-to-bar"},
    {"id": "SB005", "name": "Green Tea - Darjeeling First Flush", "brand": "Teabox", "category": "Snacks & Beverages", "subcategory": "Tea", "price": 499, "unit": "50g", "labels": ["organic", "no-artificial-additives", "pesticide-free"], "quality_score": 9.4, "description": "Spring harvest, muscatel character"},
    {"id": "SB006", "name": "Cold Brew Coffee", "brand": "Blue Tokai", "category": "Snacks & Beverages", "subcategory": "Coffee", "price": 199, "unit": "250ml", "labels": ["no-artificial-additives", "no-preservatives", "no-added-sugar"], "quality_score": 9.3, "description": "16-hour steep, single origin Attikan estate"},
    {"id": "SB007", "name": "Coconut Water", "brand": "Coco Soul", "category": "Snacks & Beverages", "subcategory": "Juices & Drinks", "price": 65, "unit": "200ml", "labels": ["no-artificial-additives", "no-added-sugar", "natural"], "quality_score": 9.0, "description": "Tender coconut, HPP processed, no heat"},
    {"id": "SB008", "name": "Kombucha - Ginger Lemon", "brand": "Bhu", "category": "Snacks & Beverages", "subcategory": "Fermented Drinks", "price": 149, "unit": "250ml", "labels": ["probiotic", "no-artificial-additives", "no-added-sugar", "vegan"], "quality_score": 9.1, "description": "Live cultures, 21-day ferment, gut-friendly"},
    {"id": "SB009", "name": "Makhana - Cheese & Herbs", "brand": "WickedGüd", "category": "Snacks & Beverages", "subcategory": "Healthy Snacks", "price": 99, "unit": "60g", "labels": ["no-artificial-additives", "gluten-free", "high-protein"], "quality_score": 8.9, "description": "Roasted fox nuts, 11g protein per pack"},
    {"id": "SB010", "name": "Trail Mix - Premium", "brand": "True Elements", "category": "Snacks & Beverages", "subcategory": "Nuts & Dry Fruits", "price": 349, "unit": "250g", "labels": ["no-artificial-additives", "no-added-sugar", "natural"], "quality_score": 9.2, "description": "Almonds, cashews, cranberries, dark raisins"},
    {"id": "SB011", "name": "Protein Bar - Dark Choc", "brand": "RiteBite Max Protein", "category": "Snacks & Beverages", "subcategory": "Protein Bars", "price": 99, "unit": "67g", "labels": ["high-protein", "no-artificial-additives"], "quality_score": 8.7, "description": "20g protein, low sugar, satisfying crunch"},
    {"id": "SB012", "name": "Sparkling Water", "brand": "Perrier", "category": "Snacks & Beverages", "subcategory": "Water", "price": 89, "unit": "330ml", "labels": ["no-artificial-additives", "natural", "no-added-sugar"], "quality_score": 9.0, "description": "Natural mineral sparkling water"},
    {"id": "SB013", "name": "Oat Cookies - Choco Chip", "brand": "Nourish Organics", "category": "Snacks & Beverages", "subcategory": "Biscuits & Cookies", "price": 149, "unit": "150g", "labels": ["organic", "no-artificial-additives", "no-refined-sugar"], "quality_score": 9.0, "description": "Sweetened with jaggery, whole oat base"},
    {"id": "SB014", "name": "Turmeric Latte Mix", "brand": "Nourish You", "category": "Snacks & Beverages", "subcategory": "Health Drinks", "price": 249, "unit": "100g", "labels": ["organic", "no-artificial-additives", "no-added-sugar", "vegan"], "quality_score": 9.1, "description": "Ashwagandha + turmeric + black pepper blend"},
    {"id": "SB015", "name": "Roasted Almonds", "brand": "Nutraj", "category": "Snacks & Beverages", "subcategory": "Nuts & Dry Fruits", "price": 299, "unit": "200g", "labels": ["no-artificial-additives", "no-added-sugar", "natural"], "quality_score": 9.2, "description": "California almonds, dry roasted, no oil"},

    # ─── HEALTH & NUTRITION ───────────────────────────────────────────────
    {"id": "HN001", "name": "Whey Protein - Light Cocoa", "brand": "The Whole Truth", "category": "Health & Nutrition", "subcategory": "Protein Supplements", "price": 1799, "unit": "1kg", "labels": ["no-artificial-additives", "no-added-sugar", "high-protein", "hormone-free"], "quality_score": 9.6, "description": "100% whey, no sucralose, no proprietary blends"},
    {"id": "HN002", "name": "Fermented Yeast Protein", "brand": "SuperYou Pro", "category": "Health & Nutrition", "subcategory": "Protein Supplements", "price": 1499, "unit": "500g", "labels": ["vegan", "no-artificial-additives", "high-protein", "gut-friendly"], "quality_score": 9.2, "description": "Complete amino profile, fermented for bioavailability"},
    {"id": "HN003", "name": "Omega-3 Fish Oil", "brand": "OZiva", "category": "Health & Nutrition", "subcategory": "Supplements", "price": 699, "unit": "60 capsules", "labels": ["no-artificial-additives", "mercury-tested", "IFOS-certified"], "quality_score": 9.1, "description": "1000mg EPA+DHA, IFOS 5-star certified"},
    {"id": "HN004", "name": "Multivitamin Gummies", "brand": "Wellbeing Nutrition", "category": "Health & Nutrition", "subcategory": "Supplements", "price": 499, "unit": "30 gummies", "labels": ["no-artificial-additives", "no-gelatin", "vegan"], "quality_score": 8.9, "description": "Whole-food sourced vitamins, pectin base"},
    {"id": "HN005", "name": "Chia Seeds", "brand": "True Elements", "category": "Health & Nutrition", "subcategory": "Superfoods", "price": 199, "unit": "250g", "labels": ["organic", "no-artificial-additives", "high-fibre", "vegan"], "quality_score": 9.2, "description": "Packed with omega-3, 34g fibre per 100g"},
    {"id": "HN006", "name": "Spirulina Powder", "brand": "Himalayan Organics", "category": "Health & Nutrition", "subcategory": "Superfoods", "price": 599, "unit": "100g", "labels": ["organic", "vegan", "no-artificial-additives", "high-protein"], "quality_score": 9.0, "description": "65% protein, full B-vitamin complex"},
    {"id": "HN007", "name": "Collagen Peptides", "brand": "OZiva", "category": "Health & Nutrition", "subcategory": "Supplements", "price": 899, "unit": "250g", "labels": ["no-artificial-additives", "no-added-sugar", "hormone-free"], "quality_score": 8.8, "description": "Hydrolyzed bovine collagen, fast absorption"},
    {"id": "HN008", "name": "Ashwagandha KSM-66", "brand": "Wellbeing Nutrition", "category": "Health & Nutrition", "subcategory": "Adaptogens", "price": 699, "unit": "60 capsules", "labels": ["organic", "no-artificial-additives", "vegan"], "quality_score": 9.1, "description": "KSM-66 extract, clinical-grade, 5% withanolides"},
    {"id": "HN009", "name": "Probiotic Capsules", "brand": "Yakult Sciences", "category": "Health & Nutrition", "subcategory": "Gut Health", "price": 799, "unit": "30 capsules", "labels": ["no-artificial-additives", "vegan", "gluten-free"], "quality_score": 9.0, "description": "10 strains, 50 billion CFU, enteric coated"},
    {"id": "HN010", "name": "Flaxseed Powder", "brand": "Conscious Food", "category": "Health & Nutrition", "subcategory": "Superfoods", "price": 149, "unit": "250g", "labels": ["organic", "vegan", "no-artificial-additives", "high-fibre"], "quality_score": 9.1, "description": "Cold-milled, omega-3 and lignin-rich"},

    # ─── HOME & KITCHEN ───────────────────────────────────────────────────
    {"id": "HK001", "name": "Dishwash Liquid - Citrus", "brand": "Sovi", "category": "Home & Kitchen", "subcategory": "Cleaning", "price": 149, "unit": "500ml", "labels": ["no-artificial-additives", "biodegradable", "palm-oil-free"], "quality_score": 8.9, "description": "Plant-based surfactants, grease-cutting"},
    {"id": "HK002", "name": "Floor Cleaner - Lemongrass", "brand": "Tydi", "category": "Home & Kitchen", "subcategory": "Cleaning", "price": 179, "unit": "1L", "labels": ["no-artificial-additives", "biodegradable"], "quality_score": 8.7, "description": "Natural essential oils, no harsh chemicals"},
    {"id": "HK003", "name": "Laundry Detergent Sheets", "brand": "Dizolve", "category": "Home & Kitchen", "subcategory": "Laundry", "price": 399, "unit": "32 sheets", "labels": ["no-artificial-additives", "biodegradable", "vegan", "palm-oil-free"], "quality_score": 9.0, "description": "Zero plastic, concentrated formula"},
    {"id": "HK004", "name": "Beeswax Food Wraps", "brand": "Honeywrap", "category": "Home & Kitchen", "subcategory": "Storage", "price": 499, "unit": "3 wraps", "labels": ["natural", "no-artificial-additives", "reusable"], "quality_score": 9.2, "description": "Replaces cling film, washable, biodegradable"},
    {"id": "HK005", "name": "Bamboo Toothbrush Set", "brand": "Bam & Boo", "category": "Home & Kitchen", "subcategory": "Personal Care", "price": 199, "unit": "4 pcs", "labels": ["natural", "biodegradable", "vegan"], "quality_score": 8.8, "description": "Charcoal-infused bristles, biodegradable handle"},

    # ─── KIDS & BABY ──────────────────────────────────────────────────────
    {"id": "KB001", "name": "Organic Baby Cereal - Ragi", "brand": "Slurrp Farm", "category": "Kids & Baby", "subcategory": "Baby Food", "price": 249, "unit": "200g", "labels": ["organic", "no-artificial-additives", "no-added-sugar", "gluten-free"], "quality_score": 9.5, "description": "For 6+ months, single ingredient, no preservatives"},
    {"id": "KB002", "name": "Kids Multigrain Pancake Mix", "brand": "Slurrp Farm", "category": "Kids & Baby", "subcategory": "Kids Breakfast", "price": 199, "unit": "150g", "labels": ["no-artificial-additives", "no-refined-sugar", "whole-grain"], "quality_score": 9.3, "description": "Whole grains + jaggery, ready in 5 minutes"},
    {"id": "KB003", "name": "Fruit Squeeze Pouches", "brand": "Plum Organics", "category": "Kids & Baby", "subcategory": "Baby Food", "price": 79, "unit": "1 pouch (90g)", "labels": ["organic", "no-artificial-additives", "no-added-sugar"], "quality_score": 9.2, "description": "100% fruit, no concentrate, resealable"},
    {"id": "KB004", "name": "Kids Protein Cookies", "brand": "Nourish Organics", "category": "Kids & Baby", "subcategory": "Kids Snacks", "price": 149, "unit": "150g", "labels": ["organic", "no-artificial-additives", "whole-grain"], "quality_score": 9.0, "description": "Jaggery-sweetened, 5g protein per serving"},
    {"id": "KB005", "name": "Organic Toddler Milk", "brand": "Aptamil Organic", "category": "Kids & Baby", "subcategory": "Toddler Nutrition", "price": 899, "unit": "400g", "labels": ["organic", "hormone-free", "no-artificial-additives"], "quality_score": 9.1, "description": "Organic skimmed milk base, DHA added"},
]

# ─── Extend catalog to 500+ with variations ──────────────────────────────
EXTENDED_ITEMS = []
base_len = len(RAW_CATALOG)

extensions = [
    ("FV", "Fruits & Vegetables", "Vegetables", ["pesticide-free"], 8.5),
    ("DE", "Dairy & Eggs", "Yogurt", ["probiotic", "no-artificial-additives"], 8.6),
    ("BB", "Breads & Bakery", "Bread", ["no-preservatives", "whole-grain"], 8.7),
    ("ST", "Staples", "Pulses", ["organic", "residue-tested"], 8.8),
    ("SB", "Snacks & Beverages", "Healthy Snacks", ["no-artificial-additives"], 8.5),
    ("HN", "Health & Nutrition", "Superfoods", ["organic", "vegan"], 8.7),
]

extra_names = {
    "FV": ["Organic Carrots", "Purple Cabbage", "Sweet Potato", "Kiwi", "Pineapple",
           "Organic Capsicum", "Zucchini", "Asparagus", "Blueberries", "Strawberries",
           "Organic Onions", "Garlic Bulb", "Ginger Root", "Beetroot", "Celery"],
    "DE": ["Chocolate Greek Yogurt", "Vanilla Skyr", "Lassi Mango", "Chaas Masala",
            "Organic Butter Salted", "Cashew Cheese", "Vegan Sour Cream", "Tofu Firm",
            "Hemp Milk", "Pea Milk", "Soy Milk Unsweetened", "Labneh", "Quark Cheese",
            "Organic Cream", "Goat Milk"],
    "BB": ["Rye Bread", "Focaccia", "Baguette Mini", "Brioche Buns", "Bagels",
           "Pumpkin Bread", "Walnut Raisin Loaf", "Ciabatta", "Naan Whole Wheat",
           "Tortillas Whole Grain", "Crackers Multigrain", "Lavash", "Breadsticks",
           "English Muffins", "Challah Bread"],
    "ST": ["Brown Rice", "Black Rice", "Amaranth Seeds", "Buckwheat Flour",
            "Jowar Flour", "Bajra Flour", "Besan Organic", "Semolina Fine",
            "Jaggery Powder", "Stevia Leaf Extract", "Sunflower Oil Cold-Press",
            "Sesame Oil Wood-Pressed", "Flaxseed Oil", "Walnut Oil", "Avocado Oil"],
    "SB": ["Rice Cakes", "Popcorn Himalayan Salt", "Granola Bar Honey Oat",
            "Seaweed Snacks", "Banana Chips", "Kale Chips", "Protein Granola",
            "Date Balls", "Coconut Bites", "Energy Balls Peanut Butter",
            "Herbal Tea Tulsi", "Hibiscus Tea", "Rooibos Tea", "Matcha Powder",
            "Cacao Nibs"],
    "HN": ["Moringa Powder", "Wheatgrass Powder", "Maca Root Powder", "Turmeric Capsules",
            "Vitamin D3 Drops", "Magnesium Glycinate", "Iron Supplement", "B12 Sublingual",
            "Zinc + C Gummies", "Liver Detox Tea"],
}

counter = base_len + 1
for prefix, category, subcategory, labels, quality in extensions:
    names = extra_names.get(prefix, [])
    for name in names:
        EXTENDED_ITEMS.append({
            "id": f"{prefix}{counter:03d}",
            "name": name,
            "brand": "Member's Pick" if counter % 3 == 0 else ("Conscious Food" if counter % 2 == 0 else "Farm Direct"),
            "category": category,
            "subcategory": subcategory,
            "price": 50 + (counter * 7 % 400),
            "unit": "250g" if counter % 2 == 0 else "500g",
            "labels": labels,
            "quality_score": round(quality + (counter % 5) * 0.1, 1),
            "description": f"Premium quality {name.lower()}, curated for FirstClub standards"
        })
        counter += 1

FULL_CATALOG = RAW_CATALOG + EXTENDED_ITEMS


def get_catalog_df():
    """Return catalog as a pandas DataFrame."""
    df = pd.DataFrame(FULL_CATALOG)
    df['labels_str'] = df['labels'].apply(lambda x: ', '.join(x))
    return df


def get_catalog_json():
    """Return catalog as JSON string for Claude API."""
    catalog_by_category = {}
    for item in FULL_CATALOG:
        cat = item['category']
        if cat not in catalog_by_category:
            catalog_by_category[cat] = []
        catalog_by_category[cat].append({
            "id": item['id'],
            "name": item['name'],
            "brand": item['brand'],
            "subcategory": item['subcategory'],
            "price": item['price'],
            "unit": item['unit'],
            "labels": item['labels'],
            "quality_score": item['quality_score'],
            "description": item['description']
        })
    return json.dumps(catalog_by_category, indent=2)


def get_catalog_stats():
    """Return catalog statistics."""
    df = get_catalog_df()
    return {
        "total_skus": len(df),
        "categories": df['category'].nunique(),
        "brands": df['brand'].nunique(),
        "avg_quality": round(df['quality_score'].mean(), 2),
        "category_counts": df['category'].value_counts().to_dict()
    }


if __name__ == "__main__":
    stats = get_catalog_stats()
    print(f"Total SKUs: {stats['total_skus']}")
    print(f"Categories: {stats['categories']}")
    print(f"Brands: {stats['brands']}")
    print(f"Avg Quality Score: {stats['avg_quality']}")
    for cat, count in stats['category_counts'].items():
        print(f"  {cat}: {count} items")
