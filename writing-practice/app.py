import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Romanian Writing Practice")

# Basic writing interface
text = st.text_area("Write your Romanian text here:", height=200)

if st.button("Check Writing"):
    if text:
        # Here you'll add your writing check logic
        st.success("Text submitted successfully!")
    else:
        st.error("Please enter some text first")

# Add backend URL to connect to main application
backend_url = os.getenv('BACKEND_URL', 'http://backend:5000') 