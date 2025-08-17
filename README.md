# 🧠 Mental Support Chatbot App

This is a **mental health companion app** built using **Streamlit** and **OpenAI’s GPT-3.5**. It allows users to express their thoughts, analyze emotional sentiment, and receive supportive responses in real time.

---

### 💡 Features

- Conversational chatbot trained to be empathetic and supportive  
- Sentiment analysis using `TextBlob` to detect mood  
- Smart suggestions like breathing exercises when negative sentiment is detected  
- Light & Dark mode toggle with full background color change  
- Logs chat history to local files for review  
- Reset chat button for fresh sessions  

---

### 🛠️ Tech Stack

- **Python 3.10+**  
- **Streamlit** for web UI  
- **OpenAI GPT-3.5 Turbo** via `openai` Python SDK  
- **TextBlob** for sentiment analysis  
- **dotenv** for securely loading API keys  
- Local logging to store conversation history  

---

### 🚀 How to Run

1. Clone this repository  
   ```bash
   git clone https://github.com/SameerDixit1/mental-health-ai-companion.git
2. cd mental-health-ai-companion
3. pip install -r requirements.txt
4. OPENAI_API_KEY=your_api_key_here
5. streamlit run App.py

