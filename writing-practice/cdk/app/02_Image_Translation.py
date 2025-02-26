import streamlit as st
from openai import OpenAI
import base64
from dotenv import load_dotenv, find_dotenv
import os
from io import BytesIO
from datetime import datetime, timedelta
from collections import deque

# Debug information about environment
st.write("Current working directory:", os.getcwd())
st.write("Environment files in directory:", [f for f in os.listdir() if '.env' in f])

# Try to find .env file
env_file = find_dotenv()
st.write("Found .env file at:", env_file)

# Load environment variables with explicit file path
load_dotenv(env_file)

# Rate limiting configuration
RATE_LIMIT_PERIOD = 60  # seconds (1 minute)
MAX_REQUESTS = 4  # maximum 4 requests per minute
request_timestamps = deque(maxlen=MAX_REQUESTS)

def check_rate_limit():
    """Check if we've exceeded our rate limit"""
    now = datetime.now()
    while request_timestamps and (now - request_timestamps[0]) > timedelta(seconds=RATE_LIMIT_PERIOD):
        request_timestamps.popleft()
    
    if len(request_timestamps) >= MAX_REQUESTS:
        time_until_next = RATE_LIMIT_PERIOD - (now - request_timestamps[0]).total_seconds()
        return False, f"Rate limit exceeded. Please wait {int(time_until_next)} seconds."
    
    request_timestamps.append(now)
    return True, None

# Initialize OpenAI client with explicit configuration
try:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("OpenAI API key not found. Please check your .env file.")
        st.stop()
        
    client = OpenAI(
        api_key=api_key,
        timeout=60.0
    )
    
    # Test the client connection with the correct model name
    models = client.models.list()
    vision_models = ["gpt-4o", "gpt-4o-mini", "o1", "gpt-4-turbo"]  # Updated model list
    available_models = [model.id for model in models]
    
    # Find the first available vision model
    vision_model = next((m for m in vision_models if any(m in am for am in available_models)), None)
    
    if not vision_model:
        st.error("No vision models available. Please ensure you have access to GPT-4 vision models.")
        st.stop()
    else:
        st.success(f"Using vision model: {vision_model}")

except Exception as e:
    st.error(f"Failed to initialize OpenAI client: {str(e)}")
    st.stop()

def process_image(image_file):
    """Process the uploaded image and return the translation"""
    can_proceed, error_message = check_rate_limit()
    if not can_proceed:
        return error_message
    
    bytes_data = image_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using the mini model for faster response
            messages=[
                {
                    "role": "system",
                    "content": "You are a Romanian to English translator. Identify and translate Romanian text from images accurately."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Please identify and translate any Romanian text in this image to English. Format your response as:\nOriginal Romanian: [text]\nEnglish Translation: [translation]"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"  # Using high detail for better text recognition
                            }
                        }
                    ]
                }
            ],
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "model_not_found" in error_msg:
            return f"Error: Model '{vision_model}' not available. Available models: {', '.join(available_models)}"
        elif "billing" in error_msg.lower():
            return "Error: Please check your OpenAI account billing status."
        return f"Error processing image: {error_msg}"

# Initialize session state for request tracking
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = None

st.title("🖼️ Romanian Image Translation")
st.subheader("Upload an image containing Romanian text to translate it to English")

# Display rate limit info
st.sidebar.info(f"Rate Limit: {MAX_REQUESTS} requests per {RATE_LIMIT_PERIOD} seconds")
if request_timestamps:
    st.sidebar.text(f"Requests in current period: {len(request_timestamps)}")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Display the uploaded image using the new parameter
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    # Add a translate button
    if st.button("Translate Text"):
        with st.spinner("Translating..."):
            translation = process_image(uploaded_file)
            st.markdown("### Translation Result")
            st.write(translation)
            
st.markdown("""
---
**Note:** 
- Supported image formats: PNG, JPG, JPEG
- For best results, ensure the text in the image is clear and readable
- The translation service uses OpenAI's GPT-4 Vision API
- Rate limited to {} requests per {} seconds
""".format(MAX_REQUESTS, RATE_LIMIT_PERIOD)) 