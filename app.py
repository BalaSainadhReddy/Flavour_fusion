import streamlit as st
import google.generativeai as genai
import json
import random

# ────────────────────────────────────────────────
st.set_page_config(page_title="Flavour Fusion", layout="wide", page_icon="🧑‍🍳")

API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    st.error("Gemini API key is missing! Add it in Streamlit Cloud secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# ────────────────────────────────────────────────
# Styling & Header
# ────────────────────────────────────────────────
st.markdown(
    """
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .stButton > button { background-color: #ff4b4b; color: white; border: none; }
        .stTextInput > div > div > input { background-color: #262730; color: white; }
        .stSelectbox > div > div > div { background-color: #262730; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="background-color:#1a1c2e; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h1 style="color:#ff8c00; margin:0;">🧑‍🍳 Flavour Fusion</h1>
        <p style="color:#bbb; margin:10px 0 0;">AI-Driven Recipe Blogging • Powered by Gemini</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.success("✨ AI-powered recipe blogging made simple!")

st.markdown("---")

# ────────────────────────────────────────────────
# Input Section
# ────────────────────────────────────────────────
st.subheader("Cook Up Something New 🍳")

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    topic = st.text_input(
        "Recipe Topic",
        placeholder="e.g. Vegan Chocolate Cake, Spicy Paneer Tikka..."
    )

with col2:
    word_count_options = [500, 800, 1000, 1200, 1500, 2000]
    word_count = st.selectbox("Target Word Count", word_count_options, index=1)

with col3:
    category = st.selectbox(
        "Category",
        ["General", "Vegan", "Vegetarian", "High Protein", "Quick Meals", "Dessert"]
    )

# ────────────────────────────────────────────────
# Generate Button
# ────────────────────────────────────────────────
if st.button("⭐ Generate Recipe", type="primary", use_container_width=True):

    if not topic.strip():
        st.error("Please enter a recipe topic!")
    else:

        jokes = [
            "Why did the tomato turn red? Because it saw the salad dressing! 🥗",
            "What do you call cheese that isn't yours? Nacho cheese! 🧀",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚",
            "I'm on a seafood diet. I see food and I eat it. 🍔",
            "What do you call a fake noodle? An impasta! 😏"
        ]

        random_joke = random.choice(jokes)

        with st.spinner("🍲 Cooking up your recipe..."):
            st.info(f"**While you wait...**  \n{random_joke}")

            try:
                prompt = f"""
Generate a detailed, engaging {category} recipe blog post for the topic: "{topic}".
Aim for approximately {word_count} words.
Make it professional, appealing for a food blog, and well-structured.

Output ONLY valid JSON with:
{{
  "title": "string",
  "difficulty": "Easy/Medium/Hard",
  "prep_time": "string",
  "cook_time": "string",
  "servings": integer,
  "introduction": "string",
  "ingredients": [],
  "instructions": [],
  "tips": [],
  "serving_suggestions": [],
  "storage": "string"
}}
"""

                model = genai.GenerativeModel(MODEL_NAME)

                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.75,
                        top_p=0.95,
                        top_k=64,
                        max_output_tokens=8192,
                        response_mime_type="application/json"
                    )
                )

                data = json.loads(response.text.strip())

                st.session_state["recipe_data"] = data
                st.session_state["word_count"] = word_count
                st.session_state["show_output"] = True
                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")

# ────────────────────────────────────────────────
# Output Section
# ────────────────────────────────────────────────
if "show_output" in st.session_state and st.session_state.show_output:

    data = st.session_state.recipe_data
    wc = st.session_state.word_count

    st.markdown("---")
    st.subheader(f"{data['title']} ({wc} words)")
    st.caption(f"Difficulty: **{data['difficulty']}**")

    cols = st.columns(3)
    cols[0].metric("Prep Time", data["prep_time"])
    cols[1].metric("Cook Time", data["cook_time"])
    cols[2].metric("Servings", data["servings"])

    st.markdown("### Introduction")
    st.write(data["introduction"])

    st.markdown("### Ingredients")
    for ing in data.get("ingredients", []):
        st.markdown(f"- {ing}")

    st.markdown("### Instructions")
    for i, step in enumerate(data.get("instructions", []), 1):
        st.markdown(f"{i}. {step}")

    st.markdown("### Tips for Success")
    for tip in data.get("tips", []):
        st.markdown(f"- {tip}")

    st.markdown("### Serving Suggestions")
    for sug in data.get("serving_suggestions", []):
        st.markdown(f"- {sug}")

    st.markdown("### Storage")
    st.write(data.get("storage", "Not specified."))

    # ⭐ NEW FEATURES
    st.download_button(
        "📄 Download Recipe",
        data=json.dumps(data, indent=2),
        file_name="recipe_blog.txt",
        mime="text/plain"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Regenerate Recipe"):
            st.session_state.pop("recipe_data", None)
            st.session_state.pop("show_output", None)
            st.rerun()

    with col2:
        if st.button("Generate Another Recipe"):
            for key in ["show_output", "recipe_data", "word_count"]:
                st.session_state.pop(key, None)
            st.rerun()

# ────────────────────────────────────────────────
# Footer
# ────────────────────────────────────────────────
st.markdown("---")
st.subheader("Why Food Bloggers Love Flavour Fusion")

cols = st.columns(3)
with cols[0]:
    st.markdown("**💡 Endless Inspiration**  \nAny cuisine, any diet, instant ideas.")
with cols[1]:
    st.markdown("**⏱️ Save Time**  \nBlog-ready in seconds.")
with cols[2]:
    st.markdown("**📖 Pro Quality**  \nStructured & engaging content.")

st.markdown("---")
st.caption("🧑‍🍳 Flavour Fusion • AI-Driven Recipe Blogging • Made by AVAITOR(MOIN)")