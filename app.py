import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import os

# 1. API Key Setup
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Latest model use kar rahe hain taaki NotFound error na aaye
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Setup Error: {e}")

# 2. Voice Function
def speak(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.write("Audio error:", e)

# 3. App UI
st.set_page_config(page_title="AI Fluency Coach", page_icon="🗣️")
st.title("🗣️ AI Fluency Coach")

language = st.sidebar.radio("Sikhne wali zubaan (Language):", ("English", "Arabic"))
lang_code = 'en' if language == "English" else 'ar'

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Input & Logic
user_input = st.chat_input(f"Talk to me in {language}...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    prompt = f"Act as a friendly {language} teacher. User said: '{user_input}'. Reply naturally, correct mistakes, and suggest 2 better words. Keep it short."
    
    try:
        response = model.generate_content(prompt)
        bot_reply = response.text
        
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        
        speak(bot_reply, lang=lang_code)
    except Exception as e:
        st.error(f"AI Error: {e}")
