import streamlit as st
import os
from dotenv import load_dotenv
import json
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime
from textblob import TextBlob
import google.generativeai as genai

# Load environment
load_dotenv()
st.set_page_config(page_title="Mental Support Chatbot")

# API Key setup
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    api_key = st.secrets.get("GENAI_API_KEY")
    if not api_key:
        st.error("Please set your GENAI_API_KEY in .env or secrets.toml")
        st.stop()

genai.configure(api_key=api_key)

# Model configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Load conversation history
if os.path.exists("conversation_history.json"):
    with open("conversation_history.json", "r") as file:
        conversation_history = json.load(file)
else:
    conversation_history = []

# Initialize model
model = genai.GenerativeModel(
    model_name="models/gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
convo = model.start_chat(history=conversation_history)

# UI
st.title("🧠 Mental Health AI Companion")
user_input = st.text_input("You:")

if st.button("Send"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            convo.send_message(user_input)
            bot_response = convo.last.text

            # Sentiment
            sentiment = TextBlob(user_input).sentiment
            st.caption("🧠 Bot's Response:")
            st.write(bot_response)
            st.caption("📊 Sentiment Analysis:")
            st.write(f"Polarity: {sentiment.polarity:.2f}, Subjectivity: {sentiment.subjectivity:.2f}")

            # Mental Health Suggestion
            if sentiment.polarity < -0.2:
                st.info("🌱 You seem a bit down. Try this calming [3-min breathing video](https://www.youtube.com/watch?v=ZToicYcHIOU)")

            # Save conversation log
            os.makedirs("logs", exist_ok=True)
            log_data = {
                "timestamp": str(datetime.now()),
                "user": user_input,
                "bot": bot_response,
                "polarity": sentiment.polarity
            }
            with open(f"logs/chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
                json.dump(log_data, f, indent=2)
    else:
        st.warning("Please type something before sending.")

# Camera section
st.divider()
st.subheader("📷 Facial Mood Assessment")
camera_enabled = st.checkbox("Enable camera input")

if camera_enabled:
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer:
        vision_model = genai.GenerativeModel(
            model_name="models/gemini-pro-vision",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        vision_model.start_chat(history=conversation_history)
        img = Image.open(img_file_buffer)
        img_io = BytesIO()
        img.save(img_io, format="JPEG")
        img_bytes = img_io.getvalue()
        encoded_img = base64.b64encode(img_bytes).decode("utf-8")

        prompt_parts = [
            """Analyze the image and provide:
**Facial Expression:** ...
**Mood:** ...
**Mental Health:** ...""",
            {"mime_type": "image/jpeg", "data": encoded_img}
        ]

        response = vision_model.generate_content(prompt_parts)
        st.markdown(response.text)
