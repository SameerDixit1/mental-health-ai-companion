import streamlit as st
from textblob import TextBlob
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please set your OPENAI_API_KEY in a .env file.")
    st.stop()

client = openai.OpenAI(api_key=api_key)

# UI Config
st.set_page_config(page_title="🧠 Mental Health AI Companion", layout="centered")

# Theme toggle
dark_mode = st.toggle("🌙 Dark Mode", value=True)
if dark_mode:
    st.markdown("""
        <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stAppView"], .main {
                background-color: #121212;
                color: white;
            }
            textarea, input, .stTextInput, .stTextArea {
                background-color: #1e1e1e !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stAppView"], .main {
                background-color: #ffffff;
                color: black;
            }
            textarea, input, .stTextInput, .stTextArea {
                background-color: #f0f0f0 !important;
                color: black !important;
            }
        </style>
    """, unsafe_allow_html=True)

# App Title
st.title("🧠 Mental Health AI Companion")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful and empathetic mental health assistant."}
    ]

# Display previous messages
for msg in st.session_state.messages[1:]:
    sender = "🧍 You" if msg["role"] == "user" else "🤖 Assistant"
    st.markdown(f"**{sender}:** {msg['content']}")

# Input
user_input = st.text_input("What's on your mind?", key="user_input")

# Process input
if user_input:
    # Analyze sentiment
    sentiment = TextBlob(user_input).sentiment

    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            bot_message = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": bot_message})
        except Exception as e:
            st.error(f"OpenAI API Error: {e}")
            st.stop()

    # Show response
    st.markdown(f"**🤖 Assistant:** {bot_message}")

    # Sentiment result
    st.caption("📊 Sentiment Analysis:")
    st.write(f"Polarity: `{sentiment.polarity:.2f}`, Subjectivity: `{sentiment.subjectivity:.2f}`")

    # Suggest activity
    if sentiment.polarity < -0.2:
        st.info("🌱 You seem a bit down. Try this [3-minute breathing video](https://www.youtube.com/watch?v=ZToicYcHIOU)")

    # Save log
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
        f.write(f"User: {user_input}\nBot: {bot_message}\nPolarity: {sentiment.polarity:.2f}\n")

# Reset chat
if st.button("🔄 Reset Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful and empathetic mental health assistant."}
    ]
    st.experimental_rerun()
