import streamlit as st

pg = st.navigation([
    st.Page(page="000_Learn_Romanian.py", url_path='Learn_Romanian'),
    st.Page(page="01_Romanian_to_English.py", url_path='Romanian_to_English'),
    st.Page(page="02_Image_Translation.py", url_path='Image_Translation')
])
pg.run()
