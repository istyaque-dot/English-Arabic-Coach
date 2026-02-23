import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import os

# 1. API Key Setup (Streamlit Secrets se connect hoga)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    st.error("Please setup GOOGLE_API_KEY in Streamlit Secrets.")

# 2. Voice Function (Bot ki awaaz ke liye)
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

# 3. App UI Setup
st.set_page_config(page_title="AI Language Coach", page_icon="🗣️")
st.title("🗣️ AI Fluency Coach")
st.write("Hesitation khatam karein aur mastery hasil karein!")

# Language Selection
language = st.sidebar.radio("Sikhne wali zubaan (Language):", ("English", "Arabic"))
mode = "English Teacher" if language == "English" else "Arabic Language Mentor"
lang_code = 'en' if language == "English" else 'ar'

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Input & AI Logic
user_input = st.chat_input(f"Talk to me in {language}...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Mastery Instruction
    prompt = f"""
    Act as a {mode}. User said: '{user_input}'. 
    1. Give a natural reply in {language}. 
    2. Correct any grammar mistakes. 
    3. Suggest 2 better words to use instead of simple ones.
    Keep the reply short for speaking practice.
    """
    
    response = model.generate_content(prompt)
    bot_reply = response.text
    
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    
    # Audio Output
    speak(bot_reply, lang=lang_code)
