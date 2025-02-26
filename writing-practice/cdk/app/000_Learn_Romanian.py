import streamlit as st
from config import WORD_CATEGORIES

st.set_page_config(
    page_title="Romanian Learning App",
    page_icon="🇷🇴",
    layout="centered",
)

st.title("🇷🇴 Welcome to the Romanian Learning App!")
st.subheader("Use this page to learn Romanian words!")
st.divider()

# Display words by difficulty and category
for difficulty, categories in WORD_CATEGORIES.items():
    st.header(f"📚 {difficulty} Level")
    
    for category, words in categories.items():
        with st.expander(f"🔍 {category}"):
            # Create a nice looking table of words
            for romanian, english in words.items():
                st.markdown(f"**{romanian}** - {english}")
        st.divider()

# Footer
st.markdown(
    """
    🎯 **Practice Makes Perfect!**  
    👉 Visit the **Romanian to English** and **English to Romanian** pages to test your knowledge.  
    🌟 Keep practicing and track your progress regularly!
    """,
) 