import streamlit as st
import random
from config import WORD_CATEGORIES, get_category_for_word

def get_all_words():
    """Get all words from all categories and difficulty levels."""
    return {k: v for d in WORD_CATEGORIES.values() for c in d.values() for k, v in c.items()}

def change_word():
    """Change the current word."""
    words = list(get_all_words().keys())
    if words:  # Check if we have words
        st.session_state.current_word = random.choice(words)
    else:
        st.error("No words available.")

# Page configuration
st.set_page_config(
    page_title="Romanian to English",
    page_icon="🇷🇴")

# Page title and description
st.title("🇷🇴 Romanian Practice")
st.subheader("Translate Romanian words to English!")

# Initialize all session state variables at the start
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'current_word': random.choice(list(get_all_words().keys())),
        'attempts': 0,
        'input_key': 0,  # Used to force clear the input field
        'show_answer': False,
        'is_correct': False
    }

# Helper functions to manage state
def reset_game_state():
    st.session_state.game_state['attempts'] = 0
    st.session_state.game_state['show_answer'] = False
    st.session_state.game_state['is_correct'] = False

def next_word():
    st.session_state.game_state['current_word'] = random.choice(list(get_all_words().keys()))
    st.session_state.game_state['input_key'] += 1
    reset_game_state()

# Display the current Romanian word and its category
_, category = get_category_for_word(st.session_state.game_state['current_word'])
st.subheader(st.session_state.game_state['current_word'])
st.caption(f"Category: {category}")

# Input form for translation
with st.form("translation_form", clear_on_submit=True):
    user_translation = st.text_input("Write your English translation here:", "", key=f"translation_{st.session_state.game_state['input_key']}")
    user_translation_lower = user_translation.lower()
    
    # Add multiple submit buttons to the form
    col1, col2 = st.columns(2)
    with col1:
        submitted = st.form_submit_button("Submit")
    with col2:
        next_word_button = st.form_submit_button("Next Word")
    
    if submitted:
        st.session_state.game_state['is_correct'] = True
        words = get_all_words()
        correct_translation = words[st.session_state.game_state['current_word']]
        
        # Get the actual translation text (handle both string and dict cases)
        st.session_state.translation_text = correct_translation["translation"] if isinstance(correct_translation, dict) else correct_translation
        
        # Clean up user input and correct translation for comparison
        user_clean = user_translation_lower.replace("(formal)", "").replace("(informal)", "").strip()
        correct_clean = st.session_state.translation_text.lower().replace("(formal)", "").replace("(informal)", "").strip()
        
        if user_clean == correct_clean:
            st.success(f'Correct! "{st.session_state.game_state["current_word"]}" means "{st.session_state.translation_text}"!', icon="✅")
            st.balloons()
            reset_game_state()
        else:
            st.session_state.game_state['attempts'] += 1
            if st.session_state.game_state['attempts'] == 1:
                st.error(
                    """
                    Sorry, this is not correct. Please try again.
                    
                    Îmi pare rău, acest răspuns nu este corect. Vă rugăm să încercați din nou.
                    """,
                    icon="🚨"
                )
            else:
                st.error(
                    """
                    Still not correct. Would you like to see the answer?
                    
                    Tot nu este corect. Doriți să vedeți răspunsul?
                    """,
                    icon="🚨"
                )

    if next_word_button:
        next_word()
        st.rerun()

# Get the translation text outside the form for the show answer button
if st.session_state.game_state['attempts'] >= 2:
    # Get the translation text before showing it
    words = get_all_words()
    correct_translation = words[st.session_state.game_state['current_word']]
    translation_text = correct_translation["translation"] if isinstance(correct_translation, dict) else correct_translation
    
    # Toggle button text based on state
    button_text = "Hide Answer / Ascunde răspunsul" if st.session_state.game_state['show_answer'] else "Show Answer / Vezi răspunsul"
    
    if st.button(button_text):
        st.session_state.game_state['show_answer'] = not st.session_state.game_state['show_answer']
        st.rerun()
    
    # Show answer if button was clicked
    if st.session_state.game_state['show_answer']:
        st.warning(
            f"""
            The correct translation for "{st.session_state.game_state['current_word']}" is "{translation_text}".
            
            Traducerea corectă pentru "{st.session_state.game_state['current_word']}" este "{translation_text}".
            """,
            icon="💡"
        )